// AUD-2026-11-12 · D1 · contracts/error-codes.json iki depoda aynı mı? (yalnızca okur)
// Üç karşılaştırma: ham bayt (sha256), satır sonu normalize (CRLF→LF) sha256, JSON anlamsal eşitlik.
// Ayrıca: sözleşmedeki her kodun tr/en errors.json çevirisi var mı; sözlükte fazladan kod var mı;
// backend ErrorCode enum'undaki kodlar sözleşmeyle aynı mı.
import { createHash } from 'node:crypto';
import { readFileSync, existsSync } from 'node:fs';

const SNAP = 'D:/Projects/davetkart/_audit-snap';
const fePath = `${SNAP}/frontend/src/contracts/error-codes.json`;
const bePath = `${SNAP}/backend/contracts/error-codes.json`;

const sha = (buf) => createHash('sha256').update(buf).digest('hex');
const fe = readFileSync(fePath);
const be = readFileSync(bePath);

const count = (buf, byte) => buf.reduce((n, b) => n + (b === byte ? 1 : 0), 0);
console.log('== ham bayt ==');
console.log(`frontend  ${fe.length} bayt  sha256=${sha(fe)}  CR=${count(fe, 13)} LF=${count(fe, 10)}`);
console.log(`backend   ${be.length} bayt  sha256=${sha(be)}  CR=${count(be, 13)} LF=${count(be, 10)}`);
console.log(`bayt bayt aynı mı: ${fe.equals(be)}`);

const norm = (buf) => Buffer.from(buf.toString('utf8').replace(/\r\n/g, '\n'), 'utf8');
console.log('\n== satır sonu normalize (CRLF→LF) ==');
console.log(`frontend  sha256=${sha(norm(fe))}`);
console.log(`backend   sha256=${sha(norm(be))}`);
console.log(`normalize sonrası aynı mı: ${norm(fe).equals(norm(be))}`);

const feJson = JSON.parse(fe.toString('utf8'));
const beJson = JSON.parse(be.toString('utf8'));
const canon = (v) => JSON.stringify(v, (k, val) => (val && typeof val === 'object' && !Array.isArray(val)
  ? Object.fromEntries(Object.entries(val).sort(([a], [b]) => a.localeCompare(b))) : val));
console.log('\n== JSON anlamsal ==');
console.log(`anlamsal eşit mi: ${canon(feJson) === canon(beJson)}`);
const feCodes = Object.keys(feJson.codes ?? {});
const beCodes = Object.keys(beJson.codes ?? {});
console.log(`kod sayısı: frontend ${feCodes.length} · backend ${beCodes.length}`);
console.log(`yalnız frontend: ${feCodes.filter((c) => !beCodes.includes(c)).join(', ') || '-'}`);
console.log(`yalnız backend : ${beCodes.filter((c) => !feCodes.includes(c)).join(', ') || '-'}`);
console.log(`üst düzey anahtarlar: ${Object.keys(feJson).join(', ')}`);

console.log('\n== kod tablosu (sözleşme) ==');
for (const c of feCodes) {
  const m = feJson.codes[c];
  console.log(`${c.padEnd(34)} ${String(m.status).padEnd(4)} retryable=${String(m.retryable).padEnd(5)} params=[${(m.params ?? []).join(',')}]`);
}

console.log('\n== çeviri kapsaması (errors.json → codes.*) ==');
for (const lng of ['tr', 'en', 'es', 'fr', 'de', 'zh', 'hi', 'ar', 'ru', 'pt']) {
  const p = `${SNAP}/frontend/src/locales/${lng}/errors.json`;
  if (!existsSync(p)) { console.log(`${lng}: errors.json YOK (fallbackLng=en metni gösterilir)`); continue; }
  const dict = JSON.parse(readFileSync(p, 'utf8'));
  const codes = dict.codes ?? {};
  const missing = feCodes.filter((c) => !(c in codes));
  const extra = Object.keys(codes).filter((c) => !feCodes.includes(c));
  // params taşıyan kodlarda .detailed/.base biçimi var mı?
  const shape = [];
  for (const c of feCodes) {
    const entry = codes[c];
    const wantsDetail = (feJson.codes[c].params ?? []).length > 0;
    if (entry === undefined) continue;
    if (typeof entry === 'string') { if (wantsDetail) shape.push(`${c}: params var ama düz metin (detailed yok)`); }
    else {
      if (!('base' in entry)) shape.push(`${c}: nesne ama base yok`);
      if (wantsDetail && !('detailed' in entry)) shape.push(`${c}: params var, detailed yok`);
      if ('detailed' in entry) {
        const used = [...String(entry.detailed).matchAll(/\{\{\s*([\w.]+)/g)].map((m) => m[1]);
        const allowed = feJson.codes[c].params ?? [];
        const unknown = used.filter((u) => !allowed.includes(u) && u !== 'count');
        if (unknown.length) shape.push(`${c}: detailed sözleşmede olmayan parametre kullanıyor: ${unknown.join(',')}`);
      }
    }
  }
  console.log(`${lng}: eksik kod ${missing.length} [${missing.join(', ')}] · fazla kod ${extra.length} [${extra.join(', ')}]`);
  for (const s of shape) console.log(`   biçim: ${s}`);
}

console.log('\n== backend ErrorCode enum ↔ sözleşme ==');
const enumPathCandidates = [
  `${SNAP}/backend/app/Enums/ErrorCode.php`,
  `${SNAP}/backend/app/Support/ErrorCode.php`,
  `${SNAP}/backend/app/Exceptions/ErrorCode.php`,
];
const enumPath = enumPathCandidates.find((p) => existsSync(p));
if (!enumPath) console.log('ErrorCode enum dosyası aday yollarda bulunamadı');
else {
  const src = readFileSync(enumPath, 'utf8');
  const enumCodes = [...src.matchAll(/case\s+\w+\s*=\s*'([A-Z_]+)'/g)].map((m) => m[1]);
  console.log(`enum dosyası: ${enumPath.replace(SNAP + '/', '')} · case sayısı ${enumCodes.length}`);
  console.log(`enum'da olup sözleşmede olmayan: ${enumCodes.filter((c) => !beCodes.includes(c)).join(', ') || '-'}`);
  console.log(`sözleşmede olup enum'da olmayan: ${beCodes.filter((c) => !enumCodes.includes(c)).join(', ') || '-'}`);
}
