// AUD-2026-11-12 · D1 · backend route:list JSON'unu okunur tabloya çevirir (yalnızca okur).
// Kullanım: node fe-routes.mjs
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const routes = JSON.parse(readFileSync(join(here, '..', 'commands', 'FE-route-list.json'), 'utf8'));

console.log(`toplam rota: ${routes.length}`);
for (const r of routes) {
  const action = String(r.action ?? '').replace(/^App\\Http\\Controllers\\/, '');
  const mw = (r.middleware ?? []).map((m) => String(m).replace(/^App\\Http\\Middleware\\/, '')).join(',');
  console.log([r.method.padEnd(10), ('/' + r.uri).padEnd(52), action.padEnd(58), mw].join(' '));
}
