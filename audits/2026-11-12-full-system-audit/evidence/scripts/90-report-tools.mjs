// AUD-2026-11-12 — bulgu dosyalarını ayrıştırır; REPORT.md için sayım, tablo ve tam metin parçaları üretir.
// Kullanım:
//   node 90-report-tools.mjs stats                 → dosya başına seviye ve kanıt türü sayıları + biçim uyarıları
//   node 90-report-tools.mjs table [seviyeler]     → Markdown tablo (ör. "🟡🟢💡"); varsayılan hepsi
//   node 90-report-tools.mjs full  [seviyeler]     → seçilen seviyelerdeki bulguların tam metni (varsayılan "🔴🟠")
//   node 90-report-tools.mjs ids                   → ID · seviye · başlık (tek satır)
// Yalnızca okur; findings/ klasörüne yazmaz.
import { readdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const findingsDir = join(here, '..', '..', 'findings');
const LEVELS = ['🔴', '🟠', '🟡', '🟢', '💡'];
const LEVEL_NAMES = { '🔴': 'Kritik', '🟠': 'Yüksek', '🟡': 'Orta', '🟢': 'Düşük', '💡': 'Öneri' };
const ID_RE = /^###\s+((?:ARC|SEC|TST|FE|OPS)-\d+)\s+(.*)$/;

function field(block, name) {
  const re = new RegExp(`^-\\s*${name}\\s*:\\s*(.*)$`, 'mi');
  const m = block.match(re);
  return m ? m[1].trim() : '';
}

function parseFile(file) {
  const text = readFileSync(join(findingsDir, file), 'utf8').replace(/\r\n/g, '\n');
  const lines = text.split('\n');
  const findings = [];
  let cur = null;
  let inFence = false;
  for (const line of lines) {
    if (/^\s*```/.test(line)) inFence = !inFence;
    const m = !inFence && line.match(ID_RE);
    if (m) {
      if (cur) findings.push(cur);
      cur = { file, id: m[1], title: m[2].trim(), body: [line] };
      continue;
    }
    if (cur && !inFence && /^#{1,2}\s/.test(line)) {
      findings.push(cur);
      cur = null;
      continue;
    }
    if (cur) cur.body.push(line);
  }
  if (cur) findings.push(cur);
  return findings.map((f) => {
    const block = f.body.join('\n').trimEnd();
    const sev = field(block, 'Seviye');
    const levels = LEVELS.filter((l) => sev.includes(l));
    const ev = field(block, 'Kanıt türü').toUpperCase();
    const evidence = ev.includes('KOŞTURULDU') ? 'KOŞTURULDU' : ev.includes('KOD OKUMASI') ? 'KOD OKUMASI' : ev.includes('VARSAYIM') ? 'VARSAYIM' : '?';
    return {
      ...f,
      block,
      level: levels.length === 1 ? levels[0] : '?',
      levelRaw: sev,
      evidence,
      where: field(block, 'Nerede'),
      effort: (field(block, 'Efor').match(/\b(XL|S|M|L)\b/) || ['?'])[0],
      suggestion: field(block, 'Öneri'),
      related: field(block, 'İlgili'),
    };
  });
}

const files = readdirSync(findingsDir).filter((f) => f.endsWith('.md')).sort();
const all = files.flatMap(parseFile);
const cmd = process.argv[2] || 'stats';
const pick = process.argv[3];
const wanted = (def) => (pick ? LEVELS.filter((l) => pick.includes(l)) : def);
const cell = (s, n = 160) => {
  const one = String(s || '').replace(/\s+/g, ' ').replace(/\|/g, '\\|').trim();
  return one.length > n ? one.slice(0, n - 1) + '…' : one;
};

if (cmd === 'stats') {
  const rows = [];
  for (const file of files) {
    const fs = all.filter((f) => f.file === file);
    rows.push(`${file}: ${fs.length} bulgu · ` + LEVELS.map((l) => `${l}${fs.filter((f) => f.level === l).length}`).join(' ') + ` · ?${fs.filter((f) => f.level === '?').length}` + ` · KOŞTURULDU ${fs.filter((f) => f.evidence === 'KOŞTURULDU').length} / KOD OKUMASI ${fs.filter((f) => f.evidence === 'KOD OKUMASI').length} / VARSAYIM ${fs.filter((f) => f.evidence === 'VARSAYIM').length} / ? ${fs.filter((f) => f.evidence === '?').length}`);
  }
  console.log(rows.join('\n'));
  console.log(`TOPLAM: ${all.length} bulgu · ` + LEVELS.map((l) => `${l} ${LEVEL_NAMES[l]} ${all.filter((f) => f.level === l).length}`).join(' · '));
  console.log(`Kanıt: KOŞTURULDU ${all.filter((f) => f.evidence === 'KOŞTURULDU').length} · KOD OKUMASI ${all.filter((f) => f.evidence === 'KOD OKUMASI').length} · VARSAYIM ${all.filter((f) => f.evidence === 'VARSAYIM').length}`);
  const seen = new Map();
  for (const f of all) {
    if (seen.has(f.id)) console.log(`UYARI yinelenen ID: ${f.id} (${seen.get(f.id)} ve ${f.file})`);
    seen.set(f.id, f.file);
    if (f.level === '?') console.log(`UYARI seviye ayrıştırılamadı: ${f.id} → "${f.levelRaw}"`);
    if (f.evidence === '?') console.log(`UYARI kanıt türü yok: ${f.id}`);
    for (const k of ['Nerede', 'Senaryo', 'Kanıt', 'Etki', 'Öneri', 'Efor']) {
      if (!new RegExp(`^-\\s*${k}\\s*:`, 'mi').test(f.block)) console.log(`UYARI alan eksik: ${f.id} → ${k}`);
    }
  }
} else if (cmd === 'ids') {
  for (const f of all) console.log(`${f.id}\t${f.level}\t${f.evidence}\t${f.effort}\t${f.title}`);
} else if (cmd === 'table') {
  const lv = wanted(LEVELS);
  console.log('| ID | Seviye | Kanıt | Başlık | Nerede | Öneri | Efor |');
  console.log('|---|---|---|---|---|---|---|');
  for (const l of lv) {
    for (const f of all.filter((x) => x.level === l)) {
      console.log(`| ${f.id} | ${f.level} | ${f.evidence === 'KOŞTURULDU' ? 'K' : f.evidence === 'KOD OKUMASI' ? 'O' : 'V'} | ${cell(f.title, 110)} | ${cell(f.where, 90)} | ${cell(f.suggestion, 170)} | ${f.effort} |`);
    }
  }
} else if (cmd === 'full') {
  const lv = wanted(['🔴', '🟠']);
  for (const l of lv) {
    for (const f of all.filter((x) => x.level === l)) {
      console.log(f.block.replace(/^###\s+/, '### '));
      console.log('');
    }
  }
} else {
  console.error('Bilinmeyen komut: ' + cmd);
  process.exit(1);
}
