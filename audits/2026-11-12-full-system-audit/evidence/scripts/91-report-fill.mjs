// AUD-2026-11-12 — REPORT.md içindeki yer tutucuları bulgu dosyalarından üretilen içerikle doldurur.
//   {{TAM:<seviyeler>}}    → 90-report-tools.mjs full  <seviyeler>
//   {{TABLO:<seviyeler>}}  → 90-report-tools.mjs table <seviyeler>
//   {{SOZLESME}}           → findings/04-frontend-e2e.md içindeki "Sözleşme tablosu" (tablo satırları + toplam satırı)
// Kullanım: node 91-report-fill.mjs   (yer tutucu kalmadıysa hiçbir şey yapmaz)
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..', '..');
const reportPath = join(root, 'REPORT.md');
const tool = (...args) => execFileSync(process.execPath, [join(here, '90-report-tools.mjs'), ...args], { encoding: 'utf8' }).trim();

let report = readFileSync(reportPath, 'utf8');
let filled = 0;

report = report.replace(/\{\{(TAM|TABLO):([^}]+)\}\}/g, (_, kind, levels) => {
  filled++;
  // Tam metinde bulgu başlıkları rapor hiyerarşisine uysun diye bir düzey içeri alınır (### → ####).
  return kind === 'TAM' ? tool('full', levels).replace(/^### /gm, '#### ') : tool('table', levels);
});

if (report.includes('{{SOZLESME}}')) {
  const fe = readFileSync(join(root, 'findings', '04-frontend-e2e.md'), 'utf8').replace(/\r\n/g, '\n');
  const start = fe.indexOf('### Sözleşme tablosu');
  const end = fe.indexOf('### ', start + 10);
  const block = fe.slice(start, end).split('\n');
  const table = block.filter((l) => l.startsWith('|'));
  const total = block.find((l) => l.startsWith('Toplam:')) ?? '';
  report = report.replace('{{SOZLESME}}', `${table.join('\n')}\n\n${total}`);
  filled++;
}

writeFileSync(reportPath, report);
console.log(`doldurulan yer tutucu: ${filled} · kalan: ${(report.match(/\{\{[A-Z]+[:}]/g) ?? []).length} · rapor ${report.length} karakter`);
