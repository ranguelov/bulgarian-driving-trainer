/**
 * PDD Image Uploader — Figma Plugin (backend)
 *
 * Receives image data from the UI, finds matching frames by name,
 * and sets the image as a fill (PNG/JPG/WEBP) or inserts SVG as vector node.
 *
 * Frame naming convention: t{topic}_question_{group}_{num}_img_{index}
 * (e.g. t4_question_5_1_img_1)
 */

figma.showUI(__html__, { width: 420, height: 560, title: 'PDD Image Uploader' });

// Build a name → FrameNode lookup map once on startup
let frameMap = null;

function buildFrameMap() {
  if (frameMap) return frameMap;
  frameMap = new Map();

  function traverse(node) {
    if (node.type === 'FRAME') {
      // Only map frames whose names follow the PDD naming pattern
      if (/^t\d+_question_/.test(node.name)) {
        frameMap.set(node.name, node);
      }
    }
    if ('children' in node) {
      for (const child of node.children) {
        traverse(child);
      }
    }
  }

  for (const child of figma.currentPage.children) {
    traverse(child);
  }

  console.log(`[PDD] Frame map built: ${frameMap.size} frames found`);
  return frameMap;
}

figma.ui.onmessage = async (msg) => {
  if (msg.type === 'init') {
    const map = buildFrameMap();
    figma.ui.postMessage({ type: 'init-ok', frameCount: map.size });
    return;
  }

  if (msg.type === 'upload-png') {
    // msg.name     — frame name (filename without extension)
    // msg.bytes    — Uint8Array data transferred from UI
    // msg.force    — if true, overwrite even if already filled
    const map = buildFrameMap();
    const frame = map.get(msg.name);

    if (!frame) {
      figma.ui.postMessage({ type: 'ack', name: msg.name, ok: false, error: 'Frame not found' });
      return;
    }

    // Skip frames that already have a valid image fill (resume support)
    if (!msg.force && frame.fills && frame.fills.some(f => f.type === 'IMAGE' && f.imageHash)) {
      figma.ui.postMessage({ type: 'ack', name: msg.name, ok: true, skipped: true });
      return;
    }

    try {
      const image = figma.createImage(new Uint8Array(msg.bytes));

      // Replace frame background with image fill, keep corner radius
      frame.fills = [{
        type: 'IMAGE',
        imageHash: image.hash,
        scaleMode: 'FIT',
      }];

      figma.ui.postMessage({ type: 'ack', name: msg.name, ok: true });
    } catch (e) {
      figma.ui.postMessage({ type: 'ack', name: msg.name, ok: false, error: String(e) });
    }
    return;
  }

  if (msg.type === 'upload-svg') {
    // msg.name      — frame name
    // msg.svgString — SVG file content as string
    // msg.force     — if true, overwrite even if already filled
    const map = buildFrameMap();
    const frame = map.get(msg.name);

    if (!frame) {
      figma.ui.postMessage({ type: 'ack', name: msg.name, ok: false, error: 'Frame not found' });
      return;
    }

    // Check for existing vector content (GROUP/VECTOR nodes — not TEXT labels)
    const vectorChildren = frame.children
      ? frame.children.filter(c => c.type !== 'TEXT')
      : [];
    const hasVector = vectorChildren.length > 0;

    // Skip frames that already have valid SVG content (resume support)
    if (!msg.force && hasVector) {
      figma.ui.postMessage({ type: 'ack', name: msg.name, ok: true, skipped: true });
      return;
    }

    try {
      // Remove any leftover vector children from previous broken runs
      for (const c of vectorChildren) {
        try { c.remove(); } catch (_) {}
      }

      const svgNode = figma.createNodeFromSvg(msg.svgString);

      // Scale to fit inside the frame, maintaining aspect ratio
      const scaleX = (frame.width - 16) / svgNode.width;
      const scaleY = (frame.height - 16) / svgNode.height;
      const scale = Math.min(scaleX, scaleY, 1); // never upscale beyond 1

      if (svgNode.width > 0 && svgNode.height > 0) {
        svgNode.resize(svgNode.width * scale, svgNode.height * scale);
      }

      // Center inside frame
      svgNode.x = Math.round((frame.width - svgNode.width) / 2);
      svgNode.y = Math.round((frame.height - svgNode.height) / 2);

      // Clear grey background fill
      frame.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 }, opacity: 1 }];
      frame.appendChild(svgNode);

      figma.ui.postMessage({ type: 'ack', name: msg.name, ok: true });
    } catch (e) {
      figma.ui.postMessage({ type: 'ack', name: msg.name, ok: false, error: String(e) });
    }
    return;
  }
};
