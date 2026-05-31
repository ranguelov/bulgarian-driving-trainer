/**
 * Bulgarian Driving Trainer — Cloudflare Worker
 *
 * Routes:
 *   GET  /api/overrides              → public: get all media overrides (for quiz)
 *   GET  /api/admin/overrides        → admin: same + extra metadata
 *   POST /api/admin/upload           → admin: upload file to R2, store metadata in KV
 *   PUT  /api/admin/override/:k      → admin: update type tag or notes
 *   DELETE /api/admin/override/:k   → admin: remove override
 *   GET  /media/:filename            → serve file from R2
 *   GET  /api/review/statuses        → admin: get all review statuses
 *   PUT  /api/review/status/:qid     → admin: set review status
 *   DELETE /api/review/status/:qid  → admin: remove review status
 *   *                                → pass through to static assets
 *
 * Auth: Authorization: Bearer <ADMIN_TOKEN>
 *   Set via: npx wrangler secret put ADMIN_TOKEN
 */

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: CORS_HEADERS });
    }

    // ── Public API ──────────────────────────────────────────────
    if (url.pathname === '/api/overrides' && request.method === 'GET') {
      return withCors(await getOverrides(env));
    }

    // ── R2 media files ──────────────────────────────────────────
    if (url.pathname.startsWith('/media/')) {
      return serveMedia(url, env);
    }

    // ── Admin API (auth required) ───────────────────────────────
    if (url.pathname.startsWith('/api/admin/')) {
      const authErr = checkAuth(request, env);
      if (authErr) return withCors(authErr);
      return withCors(await handleAdmin(request, env, url));
    }

    // ── Review API (auth required) ──────────────────────────────
    if (url.pathname.startsWith('/api/review/')) {
      const authErr = checkAuth(request, env);
      if (authErr) return withCors(authErr);
      return withCors(await handleReview(request, env, url));
    }

    // ── /admin → admin.html ─────────────────────────────────────
    if (url.pathname === '/admin' || url.pathname === '/admin/') {
      const adminUrl = new URL('/admin.html', request.url);
      return env.ASSETS.fetch(adminUrl.toString());
    }

    // ── /admin-review → admin-review.html ──────────────────────
    if (url.pathname === '/admin-review' || url.pathname === '/admin-review/') {
      return Response.redirect(new URL('/admin-review.html', request.url).toString(), 301);
    }

    // ── Static assets (index.html, questions.js, admin.html …) ──
    return env.ASSETS.fetch(request);
  },
};

// ── Auth ────────────────────────────────────────────────────────────────────

function checkAuth(request, env) {
  const header = request.headers.get('Authorization') ?? '';
  const token = header.startsWith('Bearer ') ? header.slice(7) : null;
  if (!token || token !== env.ADMIN_TOKEN) {
    return json({ error: 'Unauthorized' }, 401);
  }
  return null;
}

// ── Overrides ───────────────────────────────────────────────────────────────

async function getOverrides(env) {
  try {
    const list = await env.ADMIN_KV.list({ prefix: 'override:' });
    const overrides = {};
    // Fetch values in parallel (up to 50 at a time)
    const keys = list.keys.map(k => k.name);
    for (let i = 0; i < keys.length; i += 50) {
      const batch = keys.slice(i, i + 50);
      await Promise.all(batch.map(async key => {
        const val = await env.ADMIN_KV.get(key, 'json');
        if (val) overrides[key.replace('override:', '')] = val;
      }));
    }
    return json(overrides);
  } catch (e) {
    return json({ error: e.message }, 500);
  }
}

// ── R2 media ─────────────────────────────────────────────────────────────────

async function serveMedia(url, env) {
  const key = decodeURIComponent(url.pathname.slice('/media/'.length));
  if (!key) return new Response('Not Found', { status: 404 });

  try {
    const obj = await env.MEDIA_BUCKET.get(key);
    if (!obj) return new Response('Not Found', { status: 404 });

    const headers = new Headers(CORS_HEADERS);
    obj.writeHttpMetadata(headers);
    headers.set('Cache-Control', 'public, max-age=300');
    return new Response(obj.body, { headers });
  } catch (e) {
    return new Response('Error: ' + e.message, { status: 500 });
  }
}

// ── Admin handlers ───────────────────────────────────────────────────────────

async function handleAdmin(request, env, url) {
  const sub = url.pathname.replace('/api/admin/', '');

  // GET /api/admin/overrides — full list with metadata
  if (sub === 'overrides' && request.method === 'GET') {
    return getOverrides(env);
  }

  // POST /api/admin/upload — multipart: file + key
  if (sub === 'upload' && request.method === 'POST') {
    return uploadFile(request, env);
  }

  // PUT /api/admin/override/<key> — update metadata
  if (sub.startsWith('override/') && request.method === 'PUT') {
    const key = sub.slice('override/'.length);
    const body = await request.json().catch(() => null);
    if (!body) return json({ error: 'Invalid JSON' }, 400);

    // Merge with existing
    const existing = (await env.ADMIN_KV.get(`override:${key}`, 'json')) ?? {};
    const updated = { ...existing, ...body, key, updatedAt: new Date().toISOString() };
    await env.ADMIN_KV.put(`override:${key}`, JSON.stringify(updated));
    return json({ ok: true, data: updated });
  }

  // DELETE /api/admin/override/<key>
  if (sub.startsWith('override/') && request.method === 'DELETE') {
    const key = sub.slice('override/'.length);
    const existing = await env.ADMIN_KV.get(`override:${key}`, 'json');

    // Also delete R2 file if we stored its filename
    if (existing?.r2key && env.MEDIA_BUCKET) {
      try { await env.MEDIA_BUCKET.delete(existing.r2key); } catch (_) {}
    }

    await env.ADMIN_KV.delete(`override:${key}`);
    return json({ ok: true });
  }

  return json({ error: 'Not found' }, 404);
}

async function uploadFile(request, env) {
  let formData;
  try {
    formData = await request.formData();
  } catch (e) {
    return json({ error: 'Invalid form data: ' + e.message }, 400);
  }

  const file = formData.get('file');
  const key  = formData.get('key');   // e.g. "t2_question_1_1_img_1"
  const type = formData.get('type') ?? 'image';  // "image" | "video"

  if (!file || !key) return json({ error: 'Missing file or key' }, 400);

  const ext = file.name.split('.').pop().toLowerCase();
  const r2key = `${key}.${ext}`;
  // Add timestamp so each upload gets a unique URL → bypasses CDN cache for old versions
  const mediaUrl = `/media/${r2key}?v=${Date.now()}`;

  try {
    // Upload to R2
    const arrayBuffer = await file.arrayBuffer();
    await env.MEDIA_BUCKET.put(r2key, arrayBuffer, {
      httpMetadata: { contentType: file.type || guessMime(ext) },
    });

    // Store metadata in KV
    const meta = {
      key,
      type,
      r2key,
      url: mediaUrl,
      filename: file.name,
      size: file.size,
      mime: file.type,
      uploadedAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    await env.ADMIN_KV.put(`override:${key}`, JSON.stringify(meta));

    return json({ ok: true, url: mediaUrl, meta });
  } catch (e) {
    return json({ error: 'Upload failed: ' + e.message }, 500);
  }
}

// ── Review status handlers ───────────────────────────────────────────────────

async function handleReview(request, env, url) {
  const sub = url.pathname.replace('/api/review/', '');

  // GET /api/review/statuses — return all review statuses
  if (sub === 'statuses' && request.method === 'GET') {
    try {
      const list = await env.ADMIN_KV.list({ prefix: 'review:' });
      const statuses = {};
      const keys = list.keys.map(k => k.name);
      for (let i = 0; i < keys.length; i += 50) {
        const batch = keys.slice(i, i + 50);
        await Promise.all(batch.map(async key => {
          const val = await env.ADMIN_KV.get(key, 'json');
          if (val) statuses[key.replace('review:', '')] = val;
        }));
      }
      return json(statuses);
    } catch (e) {
      return json({ error: e.message }, 500);
    }
  }

  // PUT /api/review/status/<qid> — set status
  if (sub.startsWith('status/') && request.method === 'PUT') {
    const qid = sub.slice('status/'.length);
    const body = await request.json().catch(() => null);
    if (!body || !body.status) return json({ error: 'Missing status' }, 400);
    const record = { qid, status: body.status, updatedAt: new Date().toISOString() };
    await env.ADMIN_KV.put(`review:${qid}`, JSON.stringify(record));
    return json({ ok: true, data: record });
  }

  // DELETE /api/review/status/<qid> — remove status
  if (sub.startsWith('status/') && request.method === 'DELETE') {
    const qid = sub.slice('status/'.length);
    await env.ADMIN_KV.delete(`review:${qid}`);
    return json({ ok: true });
  }

  return json({ error: 'Not found' }, 404);
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function withCors(response) {
  const r = new Response(response.body, response);
  Object.entries(CORS_HEADERS).forEach(([k, v]) => r.headers.set(k, v));
  return r;
}

function guessMime(ext) {
  const map = {
    png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg',
    svg: 'image/svg+xml', webp: 'image/webp', gif: 'image/gif',
    mp4: 'video/mp4', webm: 'video/webm', mov: 'video/quicktime',
  };
  return map[ext] ?? 'application/octet-stream';
}
