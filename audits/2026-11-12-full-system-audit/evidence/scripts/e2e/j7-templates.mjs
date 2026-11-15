// AUD-2026-11-12 · D2 · Yolculuk 7: Faz 15–17 şablonları mobilde (390×844, CPU 4× yavaşlatma) ve
// `prefers-reduced-motion: reduce` altında. Şablonlar depodaki önizleme düzeneğiyle açılır:
//   /onizleme.html?preset=<kimlik>&senaryo=dolu&mod=live
// SINIR: başsız Chromium + yazılımsal WebGL. FPS gerçek telefonun ölçümü DEĞİLDİR; şablonlar arası
// karşılaştırma ve "hareket azaltılıyor mu" sorusu için kullanılır.
import { BASE, MOBILE, ROOT, open, shot } from './lib.mjs';
import { writeFileSync } from 'node:fs';

const PRESETS = [
  // Faz 17 (config/davetkart.php preset_tiers)
  'kurumsal-lansman', 'kina-bugulu-ayna', 'sunnet-ucan-hali', 'parti-lazer', 'dugun-kelebek', 'dugun-karanlik-oda', 'nisan-koi', 'parti-kokteyl', 'mezuniyet-yillik',
  // Faz 17 Standart
  'dogum-gunu-surpriz-makinesi', 'baby-kazi-kazan',
  // Faz 16
  'dugun-saray-kapisi', 'dogum-gunu-havai-fisek', 'parti-havuz',
  // Faz 15 (3B ve konsept)
  'dugun-gul-3d', 'dugun-fener', 'dugun-kitap-ic-kapak',
];

async function measure(preset, reduced) {
  const { browser, page, log } = await open({ auth: false, viewport: MOBILE, reducedMotion: reduced ? 'reduce' : 'no-preference' });
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  const t0 = Date.now();
  await page.goto(`${BASE}/onizleme.html?preset=${preset}&senaryo=dolu&mod=live`, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => (document.getElementById('kok')?.innerText ?? '').length > 20 || document.querySelector('#kok canvas, #kok video'), null, { timeout: 30000 }).catch(() => {});
  const firstContentMs = Date.now() - t0;
  await page.waitForTimeout(2500);
  const m = await page.evaluate(async () => {
    let long = 0, blocked = 0;
    const po = new PerformanceObserver((l) => l.getEntries().forEach((e) => { long++; blocked += Math.max(0, e.duration - 50); }));
    try { po.observe({ entryTypes: ['longtask'] }); } catch {}
    const frames = await new Promise((res) => { let n = 0; const s = performance.now(); const tick = () => { n++; performance.now() - s < 3000 ? requestAnimationFrame(tick) : res(n); }; requestAnimationFrame(tick); });
    po.disconnect();
    const anims = document.getAnimations();
    const vids = [...document.querySelectorAll('video')];
    return {
      fps: Math.round(frames / 3),
      longTasks: long,
      blockedMs: Math.round(blocked),
      runningAnims: anims.filter((a) => a.playState === 'running').length,
      infiniteAnims: anims.filter((a) => a.playState === 'running' && a.effect?.getComputedTiming?.().iterations === Infinity).length,
      videos: vids.length,
      videosPlaying: vids.filter((v) => !v.paused).length,
      canvases: document.querySelectorAll('canvas').length,
      text: (document.getElementById('kok')?.innerText ?? '').replace(/\s+/g, ' ').slice(0, 60),
      overflowX: document.documentElement.scrollWidth - window.innerWidth,
    };
  });
  // hareket var mı: 700 ms arayla iki görüntü
  const a = await page.screenshot({ scale: 'css' });
  await page.waitForTimeout(700);
  const b = await page.screenshot({ scale: 'css' });
  m.moving = !a.equals(b);
  m.firstContentMs = firstContentMs;
  m.errors = log.console.filter((c) => c.startsWith('error') || c.startsWith('pageerror')).map((c) => c.slice(0, 160));
  m.failed = log.net;
  if (!reduced) await shot(page, `J7-${preset}-390`);
  else if (['dugun-kelebek', 'parti-lazer', 'dogum-gunu-havai-fisek', 'nisan-koi'].includes(preset)) await shot(page, `J7-${preset}-azaltilmis-390`);
  await browser.close();
  return m;
}

const rows = [];
for (const p of PRESETS) {
  const normal = await measure(p, false);
  const reduced = await measure(p, true);
  rows.push({ preset: p, normal, reduced });
  console.log(`${p.padEnd(30)} fps ${String(normal.fps).padStart(2)}→${String(reduced.fps).padStart(2)} · ilk ${normal.firstContentMs}ms · uzun görev ${normal.longTasks}/${normal.blockedMs}ms · anim ${normal.runningAnims}(∞${normal.infiniteAnims})→${reduced.runningAnims}(∞${reduced.infiniteAnims}) · video ${normal.videosPlaying}/${normal.videos}→${reduced.videosPlaying}/${reduced.videos} · canvas ${normal.canvases} · hareket ${normal.moving ? 'var' : 'yok'}→${reduced.moving ? 'VAR' : 'yok'} · hata ${normal.errors.length + normal.failed.length}${normal.text ? '' : ' · BOŞ'}`);
}
writeFileSync(`${ROOT}/commands/E2E-J7-templates.json`, JSON.stringify({ journey: 'J7-templates', ranAt: new Date().toISOString(), note: 'başsız Chromium, yazılımsal WebGL, CPU 4x; FPS göstergedir', rows }, null, 1));
