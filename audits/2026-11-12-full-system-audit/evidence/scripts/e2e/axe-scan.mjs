// AUD-2026-11-12 · D2 · erişilebilirlik taraması: axe-core 4.10.3 (npm kaydından indirildi, sayfaya yerel dosyadan
// enjekte edilir; CDN yok). Kurallar: WCAG 2.0/2.1 A ve AA + best-practice. Ayrıca klavye odağı denetimi.
import { BASE, DESKTOP, MOBILE, ROOT, open, state } from './lib.mjs';
import { writeFileSync } from 'node:fs';

const AXE = 'C:/Users/ismail/AppData/Local/Temp/claude/463f4585dc61a024/3eeef7b2-d787-4740-abef-350da1b4a3d0/scratchpad/axe-dl/package/axe.min.js';
const inv = state.invitationId;
const PAGES = [
  ['Ana sayfa', '/', false, DESKTOP], ['Giriş', '/login', false, DESKTOP], ['Kayıt', '/register', false, DESKTOP],
  ['Fiyatlar', '/pricing', false, DESKTOP], ['İletişim', '/contact', false, DESKTOP], ['Gizlilik', '/privacy', false, DESKTOP],
  ['Sihirbaz (adım 1)', '/create', true, DESKTOP], ['Panel', '/dashboard', true, DESKTOP], ['Ödeme', `/odeme?tier=gold&invitation=${inv}`, true, DESKTOP],
  ['Hesap · güvenlik', '/hesap/guvenlik', true, DESKTOP], ['Hesap · planlarım', '/hesap/planlarim', true, DESKTOP],
  ['Misafir sayfası (390)', `/invite/${inv}`, false, MOBILE], ['Ana sayfa (390)', '/', false, MOBILE], ['Panel (390)', '/dashboard', true, MOBILE],
];

const out = [];
const totals = new Map();
for (const [name, path, auth, viewport] of PAGES) {
  const { browser, page } = await open({ auth, viewport, reducedMotion: 'reduce' });
  await page.goto(BASE + path, { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(1500);
  if (path.startsWith('/invite/')) { await page.getByRole('button', { name: /Davetiyeyi aç/ }).click().catch(() => {}); await page.waitForTimeout(3000); }
  await page.addScriptTag({ path: AXE });
  const res = await page.evaluate(async () => {
    const r = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'] }, resultTypes: ['violations'] });
    return r.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, help: v.help, tags: v.tags.filter((t) => /^wcag\d{3,4}$|best-practice/.test(t)), sample: v.nodes.slice(0, 2).map((n) => n.target.join(' ').slice(0, 90) + ' :: ' + (n.failureSummary ?? '').replace(/\s+/g, ' ').slice(0, 130)) }));
  });
  // Klavye: ilk 25 Tab'da odak görünür bir öğeye gidiyor mu, odak halkası var mı?
  const kb = await (async () => {
    await page.evaluate(() => { document.activeElement?.blur?.(); window.scrollTo(0, 0); });
    let noRing = 0, hidden = 0; const seq = [];
    for (let i = 0; i < 25; i++) {
      await page.keyboard.press('Tab');
      const f = await page.evaluate(() => {
        const e = document.activeElement; if (!e || e === document.body) return null;
        const cs = getComputedStyle(e); const r = e.getBoundingClientRect();
        const ring = cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0 || cs.boxShadow !== 'none';
        return { tag: e.tagName, text: (e.innerText || e.getAttribute('aria-label') || e.placeholder || '').trim().slice(0, 24), ring, visible: r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0 };
      });
      if (!f) continue;
      seq.push(f.text || f.tag);
      if (!f.ring) noRing++;
      if (!f.visible) hidden++;
    }
    return { focused: seq.length, noRing, hidden, first: seq.slice(0, 6) };
  })();
  await browser.close();
  for (const v of res) { const t = totals.get(v.id) ?? { impact: v.impact, help: v.help, pages: 0, nodes: 0, tags: v.tags }; t.pages++; t.nodes += v.nodes; totals.set(v.id, t); }
  out.push({ page: name, path: path.replace(inv, '<id>'), viewport: viewport.width, violations: res, keyboard: kb });
  const by = (imp) => res.filter((v) => v.impact === imp).reduce((a, v) => a + v.nodes, 0);
  console.log(`${name.padEnd(24)} kritik ${by('critical')} · ciddi ${by('serious')} · orta ${by('moderate')} · küçük ${by('minor')} | kurallar: ${res.map((v) => `${v.id}(${v.nodes})`).join(', ') || '—'} | klavye: ${kb.focused} odak, halkasız ${kb.noRing}, görünmez ${kb.hidden}`);
}
console.log('\n# Kural özeti');
for (const [id, t] of [...totals].sort((a, b) => b[1].nodes - a[1].nodes)) console.log(`${id.padEnd(34)} ${String(t.impact).padEnd(9)} ${String(t.pages).padStart(2)} sayfa ${String(t.nodes).padStart(4)} öğe · ${t.tags.join(',')} · ${t.help}`);
writeFileSync(`${ROOT}/commands/E2E-axe.json`, JSON.stringify({ tool: 'axe-core 4.10.3', ranAt: new Date().toISOString(), pages: out, totals: Object.fromEntries(totals) }, null, 1));
