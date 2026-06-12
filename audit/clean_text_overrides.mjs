#!/usr/bin/env node
/**
 * Очистка УСТАРЕВШИХ ТЕКСТОВЫХ оверрайдов из KV (медиа не трогает).
 *
 * Текстовые оверрайды (type === "text_override") накладываются поверх
 * questions.js и могут вернуть старые ошибки после аудита 2026-06-12.
 *
 * Использование:
 *   node audit/clean_text_overrides.mjs <ADMIN_TOKEN>            # просмотр (dry-run)
 *   node audit/clean_text_overrides.mjs <ADMIN_TOKEN> --delete   # удаление
 */
const BASE = 'https://bulgarian-driving-trainer.gurd-6ab.workers.dev';

const doDelete = process.argv.includes('--delete');
let token = process.argv.slice(2).find(a => a !== '--delete');

if (!token) {
  // интерактивный запрос токена
  const readline = await import('node:readline/promises');
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  token = (await rl.question('Вставь ADMIN_TOKEN и нажми Enter: ')).trim();
  rl.close();
}
token = token.trim();

// проверка: токен должен состоять только из латиницы/цифр/ASCII-символов
const badIdx = [...token].findIndex(c => c.charCodeAt(0) < 0x21 || c.charCodeAt(0) > 0x7e);
if (!token || badIdx !== -1) {
  console.error(badIdx !== -1
    ? `\n✗ В токене недопустимый символ «${token[badIdx]}» (позиция ${badIdx + 1}).`
    : '\n✗ Пустой токен.');
  console.error('Похоже, вставлен не настоящий токен. Токен — это пароль латиницей,');
  console.error('который ты задавал командой: npx wrangler secret put ADMIN_TOKEN');
  process.exit(1);
}
const auth = { Authorization: `Bearer ${token}` };

const res = await fetch(`${BASE}/api/admin/overrides`, { headers: auth });
if (!res.ok) {
  console.error(`Ошибка ${res.status}: ${await res.text()}`);
  process.exit(1);
}
const overrides = await res.json();
const entries = Object.entries(overrides);
const textKeys = entries.filter(([, v]) => v && v.type === 'text_override');
const mediaKeys = entries.filter(([, v]) => !v || v.type !== 'text_override');

console.log(`Всего оверрайдов: ${entries.length}`);
console.log(`  медиа (не трогаем): ${mediaKeys.length}`);
console.log(`  текстовых (к удалению): ${textKeys.length}\n`);

for (const [key, v] of textKeys) {
  const preview = (v.question || (v.answers && v.answers[0] && v.answers[0].text) || '').slice(0, 60);
  console.log(`  ${key}  | ${preview}`);
}

if (!textKeys.length) {
  console.log('Текстовых оверрайдов нет — чистить нечего. ✓');
  process.exit(0);
}

if (!doDelete) {
  console.log('\nDry-run. Для удаления запусти с флагом --delete');
  process.exit(0);
}

let ok = 0, fail = 0;
for (const [key] of textKeys) {
  const r = await fetch(`${BASE}/api/admin/override/${encodeURIComponent(key)}`, {
    method: 'DELETE', headers: auth,
  });
  if (r.ok) { ok++; console.log(`удалён: ${key}`); }
  else { fail++; console.error(`ОШИБКА ${r.status}: ${key}`); }
}
console.log(`\nГотово: удалено ${ok}, ошибок ${fail}`);
