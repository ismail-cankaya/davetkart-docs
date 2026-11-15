// AUD-2026-11-12 · D1 · frontend mimari ölçümleri ve sözleşme tablosu (yalnızca okur).
// Kullanım: node fe-d1-metrics.mjs   (kopya: _audit-snap/frontend @44caa49, _audit-snap/backend @d810410)
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const FE = 'D:/Projects/davetkart/_audit-snap/frontend';
const BE = 'D:/Projects/davetkart/_audit-snap/backend';
const read = (p) => readFileSync(p, 'utf8');
const walk = (dir, out = []) => {
  for (const n of readdirSync(dir)) {
    const p = join(dir, n);
    if (statSync(p).isDirectory()) walk(p, out);
    else out.push(p.replace(/\\/g, '/'));
  }
  return out;
};
const rel = (p) => relative(FE, p).replace(/\\/g, '/');
const h = (t) => console.log(`\n# ===== ${t}`);

const all = walk(`${FE}/src`);
const code = all.filter((f) => /\.(ts|tsx)$/.test(f));
const isTpl = (f) => f.includes('/components/templates/');
const core = code.filter((f) => !isTpl(f));
const tpl = code.filter(isTpl);
const src = new Map(code.map((f) => [f, read(f)]));

// ---------- 0) sürümler ----------
h('0) Kurulu sürümler (node_modules/*/package.json)');
for (const p of ['react', 'react-dom', 'react-router-dom', 'zustand', 'i18next', 'react-i18next', 'i18next-browser-languagedetector', 'axios', 'vite', 'typescript', 'motion', 'three', '@react-three/fiber', 'tailwindcss', '@vitejs/plugin-react', 'lenis']) {
  const f = `${FE}/node_modules/${p}/package.json`;
  console.log(p.padEnd(34), existsSync(f) ? JSON.parse(read(f)).version : '(yok)');
}
console.log('@types/react'.padEnd(34), existsSync(`${FE}/node_modules/@types/react/package.json`) ? JSON.parse(read(`${FE}/node_modules/@types/react/package.json`)).version : '(yok)');

// ---------- 1) sözleşme ----------
h('1) Sözleşme: frontend çağrısı ↔ backend rotası (evidence/commands/FE-route-list.json)');
const routes = JSON.parse(read(join(here, '..', 'commands', 'FE-route-list.json'))).filter((r) => r.uri.startsWith('api/'));
const norm = (p) => p.replace(/\{[^}]+\}/g, '{}');
const routeKey = new Map(routes.map((r) => [`${r.method.split('|')[0]} ${norm('/' + r.uri.replace(/^api\//, ''))}`, r]));
// Elle çıkarıldı: grep "api\.(get|post|put|patch|delete)" + conditionalGet + upload(); dosya:satır yanında.
const calls = [
  ['GET', '/account/entitlements', 'services/account.ts:50'], ['POST', '/orders/{}/refund-request', 'services/account.ts:61'],
  ['DELETE', '/orders/{}/refund-request', 'services/account.ts:66'], ['PATCH', '/auth/me', 'services/account.ts:71'],
  ['PUT', '/auth/password', 'services/account.ts:79'], ['POST', '/auth/email-change', 'services/account.ts:87'],
  ['POST', '/public/email-change/confirm', 'services/account.ts:99'], ['GET', '/auth/sessions', 'services/account.ts:103'],
  ['DELETE', '/auth/sessions/{}', 'services/account.ts:110'], ['DELETE', '/auth/sessions', 'services/account.ts:114'],
  ['POST', '/assistant/chat', 'services/assistant.ts:41'], ['POST', '/auth/login', 'services/auth.ts:89'],
  ['POST', '/auth/register', 'services/auth.ts:94'], ['POST', '/auth/logout', 'services/auth.ts:101'],
  ['GET', '/auth/me', 'services/auth.ts:111'], ['POST', '/auth/forgot-password', 'services/auth.ts:122'],
  ['POST', '/auth/reset-password', 'services/auth.ts:126'], ['DELETE', '/auth/me', 'services/auth.ts:131'],
  ['POST', '/public/contact', 'services/contact.ts:37'], ['GET', '/invitations', 'services/invitations.ts:111'],
  ['GET', '/invitations/{}', 'services/invitations.ts:117'], ['POST', '/invitations', 'services/invitations.ts:122'],
  ['PUT', '/invitations/{}', 'services/invitations.ts:127'], ['POST', '/invitations/{}/publish', 'services/invitations.ts:148'],
  ['DELETE', '/invitations/{}', 'services/invitations.ts:154'], ['POST', '/invitations/{}/media', 'services/media.ts:147'],
  ['POST', '/public/invitations/{}/media', 'services/media.ts:151'], ['DELETE', '/invitations/{}/media/{}', 'services/media.ts:155'],
  ['POST', '/invitations/{}/checkout', 'services/payments.ts:153'], ['POST', '/payments/checkout', 'services/payments.ts:159'],
  ['POST', '/gift-codes/preview', 'services/payments.ts:169'], ['GET', '/orders/{}', 'services/payments.ts:189'],
  ['GET', '/orders', 'services/payments.ts:195'], ['GET', '/public/plans', 'services/pricing.ts:97'],
  ['GET', '/pricing', 'services/pricing.ts:103'], ['GET', '/invitations/{}/rsvps', 'services/rsvps.ts:55'],
  ['POST', '/public/invitations/{}/rsvps', 'services/rsvps.ts:68'], ['PUT', '/public/invitations/{}/rsvps/{}', 'services/rsvps.ts:89'],
  ['DELETE', '/rsvps/{}', 'services/rsvps.ts:97'], ['GET', '/public/invitations/{}', 'services/publicInvitation.ts:106'],
  ['GET', '/public/places/search', 'services/places.ts:24 (VITE_PLACES_SEARCH_ENABLED kapalıyken ağa çıkmaz)'],
];
const used = new Set();
for (const [m, p, where] of calls) {
  const r = routeKey.get(`${m} ${p}`);
  if (r) used.add(`${m} ${p}`);
  const mw = r ? (r.middleware.some((x) => x.includes('Authenticate')) ? 'auth' : 'public') : '';
  console.log(`${r ? 'VAR ' : 'YOK '} ${m.padEnd(6)} ${p.padEnd(40)} ${mw.padEnd(6)} ${where}`);
}
console.log(`\nfrontend çağrısı: ${calls.length} · backend'de karşılığı olan: ${used.size} · backend api rotası: ${routeKey.size}`);
console.log('Frontend’in çağırmadığı backend rotaları:');
for (const k of routeKey.keys()) if (!used.has(k)) console.log('  ' + k);
// services dışında doğrudan ağ çağrısı
const stray = core.filter((f) => !f.includes('/services/') && /\baxios\b|\bfetch\(|XMLHttpRequest|\bapi\.(get|post|put|patch|delete)\b/.test(src.get(f)));
console.log(`services/ dışında doğrudan ağ çağrısı yapan dosya: ${stray.length}${stray.length ? ' → ' + stray.map(rel).join(', ') : ''}`);

// ---------- 2) i18n ----------
h('2) i18n: anahtar kümeleri');
const flat = (o, pre = '', out = []) => {
  for (const [k, v] of Object.entries(o)) {
    if (v && typeof v === 'object' && !Array.isArray(v)) flat(v, `${pre}${k}.`, out);
    else out.push(pre + k);
  }
  return out;
};
const langs = readdirSync(`${FE}/src/locales`);
const keys = {};
for (const l of langs) keys[l] = new Set(flat(JSON.parse(read(`${FE}/src/locales/${l}/translation.json`))));
const base = keys.en;
for (const l of langs) {
  const missing = [...base].filter((k) => !keys[l].has(k));
  const extra = [...keys[l]].filter((k) => !base.has(k));
  console.log(`${l}: ${keys[l].size} anahtar · en'e göre eksik ${missing.length} · fazla ${extra.length}${missing.length ? ' · eksik: ' + missing.slice(0, 6).join(', ') : ''}${extra.length ? ' · fazla: ' + extra.slice(0, 6).join(', ') : ''}`);
}
const errTr = new Set(flat(JSON.parse(read(`${FE}/src/locales/tr/errors.json`))));
const errEn = new Set(flat(JSON.parse(read(`${FE}/src/locales/en/errors.json`))));
console.log(`errors.json: tr ${errTr.size} · en ${errEn.size} · tr'de olup en'de olmayan ${[...errTr].filter((k) => !errEn.has(k)).length} · tersi ${[...errEn].filter((k) => !errTr.has(k)).length} · diğer 8 dilde errors.json YOK (fallback en)`);

const usedKeys = new Set();
let tCalls = 0;
const filesWithT = [];
for (const f of code) {
  const s = src.get(f);
  if (/useTranslation\(|i18n\.t\(|\bt\(/.test(s) && /react-i18next|i18next|\.\/i18n|\/i18n'/.test(s)) filesWithT.push(f);
  for (const m of s.matchAll(/\bt\(\s*['"`]([A-Za-z0-9_.:-]+)['"`]/g)) {
    tCalls++;
    usedKeys.add(m[1]);
  }
}
const plain = [...usedKeys].filter((k) => !k.includes(':'));
console.log(`t('…') çağrısı: ${tCalls} · farklı anahtar: ${usedKeys.size} · i18n kullanan dosya: ${filesWithT.length} (çekirdek ${filesWithT.filter((f) => !isTpl(f)).length}, şablon ${filesWithT.filter(isTpl).length})`);
console.log(`kodda kullanılıp en/translation.json'da olmayan: ${plain.filter((k) => !base.has(k)).length} → ${plain.filter((k) => !base.has(k)).slice(0, 12).join(', ')}`);
console.log(`en/translation.json'da olup kodda düz dizgiyle geçmeyen: ${[...base].filter((k) => !usedKeys.has(k)).length} (dinamik anahtarlar bu sayıya dahil olabilir)`);

h('2b) i18n kapsaması: Türkçe metni koda gömülü dosyalar');
const TR = /[şŞğĞıİçÇöÖüÜ]/;
const stripComments = (s) => s.replace(/\/\*[\s\S]*?\*\//g, '').replace(/(^|[^:])\/\/.*$/gm, '$1');
const groups = { pages: [], components: [], templates: [], other: [] };
for (const f of code.filter((x) => x.endsWith('.tsx'))) {
  const body = stripComments(src.get(f));
  const lits = (body.match(/>[^<>{}]*[şŞğĞıİçÇöÖüÜ][^<>{}]*</g) ?? []).length + (body.match(/['"`][^'"`\n]*[şŞğĞıİçÇöÖüÜ][^'"`\n]*['"`]/g) ?? []).length;
  if (!lits) continue;
  const g = isTpl(f) ? 'templates' : f.includes('/pages/') ? 'pages' : f.includes('/components/') ? 'components' : 'other';
  groups[g].push([lits, rel(f), filesWithT.includes(f)]);
}
for (const [g, list] of Object.entries(groups)) {
  const total = list.reduce((a, b) => a + b[0], 0);
  console.log(`${g}: gömülü Türkçe metin içeren ${list.length} .tsx dosyası, ~${total} metin parçası · bunlardan i18n de kullanan ${list.filter((x) => x[2]).length}`);
  if (g !== 'templates') for (const [n, f, t] of list.sort((a, b) => b[0] - a[0]).slice(0, 8)) console.log(`    ${String(n).padStart(4)}  ${f}${t ? '  (t() da var)' : ''}`);
}
console.log(`çekirdek .tsx dosyası toplam: ${core.filter((f) => f.endsWith('.tsx')).length}`);

// ---------- 3) tip güvenliği ----------
h('3) Tip güvenliği (yorumlar ayıklandı)');
const pats = {
  ': any / any[] / <any>': /(:\s*any\b|\bany\[\]|<any>|Array<any>|Record<string,\s*any>)/g,
  'as any': /\bas any\b/g,
  'as unknown as': /\bas unknown as\b/g,
  '@ts-ignore / @ts-expect-error / @ts-nocheck': /@ts-(ignore|expect-error|nocheck)/g,
  'as <Tip> (as const hariç)': /\bas (?!const\b|any\b|unknown\b)[A-Z][\w.<>\[\]| ]*/g,
  'non-null !': /[\w\])]!(?=[.;,)\]\s])/g,
  'eslint-disable': /eslint-disable/g,
};
for (const [name, re] of Object.entries(pats)) {
  const count = (files) => files.reduce((a, f) => a + ((name.startsWith('@ts') || name === 'eslint-disable' ? src.get(f) : stripComments(src.get(f))).match(re) ?? []).length, 0);
  console.log(name.padEnd(46), 'çekirdek', String(count(core)).padStart(5), '· şablonlar', String(count(tpl)).padStart(5));
}
console.log(`dosya: çekirdek ${core.length} · şablonlar ${tpl.length} · tsconfig strict: ${/"strict"\s*:\s*true/.test(read(`${FE}/tsconfig.json`)) ? 'AÇIK' : 'KAPALI (strict, noImplicitAny, strictNullChecks yok)'}`);
const topAs = core.map((f) => [(stripComments(src.get(f)).match(pats['as <Tip> (as const hariç)']) ?? []).length, rel(f)]).sort((a, b) => b[0] - a[0]).slice(0, 8);
console.log('en çok "as <Tip>" içeren çekirdek dosyalar:', topAs.map(([n, f]) => `${f}(${n})`).join(' · '));

// ---------- 4) React / router / zustand kalıpları ----------
h('4) React 19 / router / Zustand kalıpları (çekirdek + şablon)');
const countAll = (re, files = code) => files.reduce((a, f) => a + (src.get(f).match(re) ?? []).length, 0);
const filesWith = (re, files = code) => files.filter((f) => re.test(src.get(f))).map(rel);
const rows = [
  ['React.lazy / lazy(', /\b(React\.)?lazy\(/g], ['<Suspense', /<(React\.)?Suspense/g], ['ErrorBoundary / componentDidCatch / errorElement', /ErrorBoundary|componentDidCatch|getDerivedStateFromError|errorElement/g],
  ['forwardRef(', /\bforwardRef\(/g], ['defaultProps', /\.defaultProps\b/g], ['propTypes', /\.propTypes\b/g], ['findDOMNode / ReactDOM.render', /findDOMNode|ReactDOM\.render\(/g],
  ['useEffect(', /\buseEffect\(/g], ['useLayoutEffect(', /\buseLayoutEffect\(/g], ['useMemo( / useCallback(', /\buse(Memo|Callback)\(/g],
  ['dangerouslySetInnerHTML', /dangerouslySetInnerHTML/g], ['localStorage / sessionStorage', /\b(localStorage|sessionStorage)\b/g],
  ['create< (zustand store)', /\bcreate<|\bcreate\(\)\(/g], ['persist(', /\bpersist\(/g], ['useNavigate( / <Navigate', /useNavigate\(|<Navigate/g], ['useLoaderData / loader:', /useLoaderData|\bloader:/g],
  ['console.log / console.error / console.warn', /console\.(log|error|warn|info)\(/g], ['TODO / FIXME / HACK', /\b(TODO|FIXME|HACK)\b/g], ['prefers-reduced-motion / useReducedMotion', /prefers-reduced-motion|useReducedMotion/g],
];
for (const [name, re] of rows) console.log(name.padEnd(50), 'çekirdek', String(countAll(re, core)).padStart(4), '· şablon', String(countAll(re, tpl)).padStart(5));
console.log('seçicisiz store kullanımı (useXStore() — her değişiklikte yeniden çizim):', countAll(/\buse[A-Z]\w*Store\(\s*\)/g, core), '→', filesWith(/\buse[A-Z]\w*Store\(\s*\)/, core).slice(0, 10).join(', '));
console.log('localStorage/sessionStorage kullanan çekirdek dosyalar:', filesWith(/\b(localStorage|sessionStorage)\b/, core).join(', '));
console.log('index.css CSS reduced-motion kuralı:', (read(`${FE}/src/index.css`).match(/prefers-reduced-motion/g) ?? []).length);

// ---------- 5) şablon kataloğu ↔ backend preset_tiers ----------
h('5) Şablonlar: data.ts minimumTier ↔ backend config/davetkart.php preset_tiers');
const data = read(`${FE}/src/data.ts`);
const fe = new Map();
let lastId = null;
let presetCount = 0;
const start = data.indexOf('TEMPLATE_PRESETS');
for (const line of data.slice(start).split('\n')) {
  const id = line.match(/^\s*id:\s*'([a-z0-9-]+)'/);
  if (id) {
    lastId = id[1];
    presetCount++;
  }
  const t = line.match(/minimumTier:\s*'([a-z]+)'/);
  if (t && lastId) fe.set(lastId, t[1]);
}
const cfg = read(`${BE}/config/davetkart.php`);
const block = cfg.slice(cfg.indexOf("'preset_tiers'"), cfg.indexOf("'rsvp'"));
const be = new Map([...block.matchAll(/'([a-z0-9-]+)'\s*=>\s*'([a-z]+)'/g)].map((m) => [m[1], m[2]]));
console.log(`data.ts: TEMPLATE_PRESETS sonrası id satırı ${presetCount} · minimumTier taşıyan ${fe.size} · backend preset_tiers ${be.size}`);
console.log('frontend’de premium, backend’de değil:', [...fe.keys()].filter((k) => !be.has(k)).join(', ') || '(yok)');
console.log('backend’de premium, frontend’de değil:', [...be.keys()].filter((k) => !fe.has(k)).join(', ') || '(yok)');
console.log('plan farkı:', [...fe].filter(([k, v]) => be.has(k) && be.get(k) !== v).map(([k, v]) => `${k}: fe=${v} be=${be.get(k)}`).join(', ') || '(yok)');
const lazySrc = read(`${FE}/src/components/templates/lazyPresets.ts`);
console.log(`lazyPresets.ts: tembel kayıt ${(lazySrc.match(/^\s*'[a-z0-9-]+':/gm) ?? []).length} · dinamik import() ${(lazySrc.match(/import\(/g) ?? []).length}`);
const tr = read(`${FE}/src/components/templates/TemplateRenderer.tsx`);
console.log(`TemplateRenderer.tsx: statik şablon importu ${(tr.match(/^import .* from '\.\//gm) ?? []).length} satır · lazy( ${(tr.match(/\blazy\(/g) ?? []).length} · Suspense ${(tr.match(/Suspense/g) ?? []).length}`);

// ---------- 6) sabit fiyat ----------
h('6) Sabit fiyat taraması (src/, yorumlar dahil; ₺ / TL / sayısal tutar)');
let priceHits = 0;
for (const f of all.filter((x) => /\.(ts|tsx|json)$/.test(x))) {
  const lines = read(f).split('\n');
  lines.forEach((ln, i) => {
    if (/(\d[\d.,]*\s?(₺|TL\b)|₺\s?\d|\bprice\s*[:=]\s*\d|amount(Minor)?\s*[:=]\s*\d{3,})/.test(ln)) {
      priceHits++;
      if (priceHits <= 25) console.log(`  ${rel(f)}:${i + 1}: ${ln.trim().slice(0, 130)}`);
    }
  });
}
console.log(`toplam eşleşme: ${priceHits}`);
