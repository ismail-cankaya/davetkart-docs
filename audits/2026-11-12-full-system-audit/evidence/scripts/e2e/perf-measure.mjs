// AUD-2026-11-12 · D2 · performans: üretim build'i (perf-server.mjs, localhost:4173) üzerinde LCP / CLS / TBT.
// Koşullar Lighthouse mobil varsayılanına yakın: 390×844, CPU 4× yavaş, ağ 1,6 Mbps indirme / 750 kbps yükleme / 150 ms RTT.
// SINIR: başsız Chromium + yerel sunucu; laboratuvar ölçümüdür, gerçek kullanıcı verisi değildir. Her sayfa 3 kez, ortanca.
import { MOBILE, ROOT, state } from './lib.mjs';
import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/ismail/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright-core');
const BASE = 'http://localhost:4173';
const inv = state.invitationId;
const PAGES = [['Ana sayfa', '/'], ['Misafir sayfası', `/invite/${inv}`], ['Giriş', '/login'], ['Fiyatlar', '/pricing']];
const median = (a) => [...a].sort((x, y) => x - y)[Math.floor(a.length / 2)];

async function run(path, throttled) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: MOBILE, isMobile: true, hasTouch: true, locale: 'tr-TR' });
  const page = await context.newPage();
  const cdp = await context.newCDPSession(page);
  await cdp.send('Network.enable');
  if (throttled) {
    await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: (1.6 * 1024 * 1024) / 8, uploadThroughput: (750 * 1024) / 8 });
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  }
  const bytes = { js: 0, css: 0, img: 0, media: 0, font: 0, other: 0, total: 0, requests: 0 };
  const types = new Map();
  cdp.on('Network.responseReceived', (e) => types.set(e.requestId, { type: e.type, url: e.response.url }));
  cdp.on('Network.loadingFinished', (e) => {
    const t = types.get(e.requestId); if (!t || t.url.includes('/api/')) return;
    const k = t.type === 'Script' ? 'js' : t.type === 'Stylesheet' ? 'css' : t.type === 'Image' ? 'img' : t.type === 'Media' ? 'media' : t.type === 'Font' ? 'font' : 'other';
    bytes[k] += e.encodedDataLength; bytes.total += e.encodedDataLength; bytes.requests++;
  });
  await page.addInitScript(() => {
    window.__m = { lcp: 0, cls: 0, tbt: 0, long: 0, fcp: 0 };
    new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__m.lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true });
    new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__m.cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
    new PerformanceObserver((l) => { for (const e of l.getEntries()) { window.__m.long++; window.__m.tbt += Math.max(0, e.duration - 50); } }).observe({ type: 'longtask', buffered: true });
    new PerformanceObserver((l) => { for (const e of l.getEntries()) if (e.name === 'first-contentful-paint') window.__m.fcp = e.startTime; }).observe({ type: 'paint', buffered: true });
  });
  const t0 = Date.now();
  await page.goto(BASE + path, { waitUntil: 'load', timeout: 120000 });
  const loadMs = Date.now() - t0;
  await page.waitForTimeout(throttled ? 6000 : 3000);
  const m = await page.evaluate(() => ({ ...window.__m, dcl: performance.getEntriesByType('navigation')[0]?.domContentLoadedEventEnd ?? 0 }));
  await browser.close();
  return { ...m, loadMs, bytes };
}

const rows = [];
for (const [name, path] of PAGES) {
  for (const throttled of [true, false]) {
    const runs = [];
    for (let i = 0; i < 3; i++) runs.push(await run(path, throttled));
    const r = { page: name, path: path.replace(inv, '<id>'), throttled, fcp: Math.round(median(runs.map((x) => x.fcp))), lcp: Math.round(median(runs.map((x) => x.lcp))), cls: Number(median(runs.map((x) => x.cls)).toFixed(3)), tbt: Math.round(median(runs.map((x) => x.tbt))), longTasks: median(runs.map((x) => x.long)), loadMs: median(runs.map((x) => x.loadMs)), bytes: runs[0].bytes };
    rows.push(r);
    const kb = (n) => Math.round(n / 1024);
    console.log(`${name.padEnd(16)} ${throttled ? 'yavaş 4G + CPU 4×' : 'kısıtsız         '} FCP ${String(r.fcp).padStart(5)} ms · LCP ${String(r.lcp).padStart(5)} ms · CLS ${r.cls} · TBT ${String(r.tbt).padStart(5)} ms (${r.longTasks} uzun görev) · load ${r.loadMs} ms · aktarım ${kb(r.bytes.total)} kB / ${r.bytes.requests} istek (js ${kb(r.bytes.js)} · css ${kb(r.bytes.css)} · görsel ${kb(r.bytes.img)} · video ${kb(r.bytes.media)} · diğer ${kb(r.bytes.other + r.bytes.font)})`);
  }
}
writeFileSync(`${ROOT}/commands/E2E-perf.json`, JSON.stringify({ tool: 'playwright-core 1.61.1 + CDP', ranAt: new Date().toISOString(), conditions: '390x844, CPU 4x, 1.6 Mbps / 750 kbps / 150 ms RTT; 3 koşu ortanca; üretim build + gzip (perf-server.mjs)', rows }, null, 1));
