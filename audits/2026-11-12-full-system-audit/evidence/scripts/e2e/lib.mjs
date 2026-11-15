// AUD-2026-11-12 · D2 · uçtan uca yolculukların ortak kitaplığı.
// Playwright MCP her çağrıda betiği geri yazdığı için yolculuklar bağımsız Node betikleriyle koşar:
// npx önbelleğindeki playwright-core 1.61.1 + kurulu chromium-1228. Yalnızca http://localhost:3000'e gider
// (Vite dev sunucusu; /api → backend-e2e:8000). Kullanım: node j<N>-*.mjs
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';

const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/ismail/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright-core');

export const BASE = process.env.AUD_BASE ?? 'http://localhost:3000';
export const ROOT = 'D:/Projects/davetkart/davetkart-docs/audits/2026-11-12-full-system-audit/evidence';
// Durum (test hesabı, oturum, davetiye kimliği) kanıt klasörüne DEĞİL oturumun geçici klasörüne yazılır.
const STATE_FILE = 'C:/Users/ismail/AppData/Local/Temp/claude/463f4585dc61a024/3eeef7b2-d787-4740-abef-350da1b4a3d0/scratchpad/e2e-state.json';
export const state = existsSync(STATE_FILE) ? JSON.parse(readFileSync(STATE_FILE, 'utf8')) : {};
export const saveState = () => writeFileSync(STATE_FILE, JSON.stringify(state, null, 1));

export const DESKTOP = { width: 1440, height: 900 };
export const MOBILE = { width: 390, height: 844 };

/** Yeni tarayıcı + bağlam. `auth: true` ise kayıtlı oturum (localStorage) yüklenir. */
export async function open({ viewport = DESKTOP, auth = true, reducedMotion, storage } = {}) {
  const browser = await chromium.launch({ headless: true });
  const mobile = viewport.width < 600;
  const context = await browser.newContext({
    viewport,
    locale: 'tr-TR',
    timezoneId: 'Europe/Istanbul',
    reducedMotion,
    isMobile: mobile,
    hasTouch: mobile,
    storageState: storage ?? (auth && state.storage ? state.storage : undefined),
  });
  const page = await context.newPage();
  const log = { console: [], net: [] };
  page.on('console', (m) => {
    if (m.type() === 'error' || m.type() === 'warning') log.console.push(`${m.type()}: ${m.text().slice(0, 240)}`);
  });
  page.on('pageerror', (e) => log.console.push(`pageerror: ${String(e).slice(0, 240)}`));
  page.on('requestfailed', (r) => {
    const why = r.failure()?.errorText ?? '';
    if (why.includes('ERR_ABORTED')) return; // gezinmeyle iptal edilen istekler (video, yoklama) hata değil
    log.net.push(`FAILED ${r.method()} ${r.url().replace(BASE, '')} ${why}`);
  });
  page.on('response', (r) => {
    // İmzalı bağlantıların sorgusu (signature, token) kanıta yazılmaz.
    if (r.status() >= 400) log.net.push(`${r.status()} ${r.request().method()} ${r.url().replace(BASE, '').replace(/\?.*(signature|token)=.*$/, '?…(imzalı sorgu gizlendi)')}`);
  });
  return { browser, context, page, log };
}

/** Ekran görüntüsü: evidence/screenshots/<ad>.png (CSS pikseli). */
export async function shot(page, name, opts = {}) {
  mkdirSync(`${ROOT}/screenshots`, { recursive: true });
  await page.screenshot({ path: `${ROOT}/screenshots/${name}.png`, scale: 'css', animations: 'disabled', ...opts });
  return `screenshots/${name}.png`;
}

/** Sayfanın kısa dökümü: başlıklar, alanlar, düğmeler (keşif için). */
export function describe(page, scope = 'body') {
  return page.evaluate((sel) => {
    const root = document.querySelector(sel) ?? document.body;
    const vis = (e) => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length);
    const t = (e) => (e.innerText || e.value || e.getAttribute('aria-label') || e.title || '').trim().replace(/\s+/g, ' ').slice(0, 48);
    return {
      url: location.pathname + location.search,
      h: [...root.querySelectorAll('h1,h2,h3')].filter(vis).map(t).slice(0, 14),
      inputs: [...root.querySelectorAll('input,select,textarea')].filter((i) => vis(i) || i.type === 'file').map((i) =>
        [i.tagName === 'INPUT' ? i.type : i.tagName.toLowerCase(), i.id ? '#' + i.id : i.name ? `[name=${i.name}]` : '', (i.labels?.[0]?.innerText ?? i.getAttribute('aria-label') ?? i.placeholder ?? '').trim().slice(0, 36), i.type === 'checkbox' ? String(i.checked) : (i.value ?? '').slice(0, 24)].join('|')),
      buttons: [...root.querySelectorAll('button,[role=button],[role=switch],[role=tab]')].filter(vis).map((b) => t(b) + (b.disabled ? ' (disabled)' : '') + (b.getAttribute('aria-checked') ? ` [${b.getAttribute('aria-checked')}]` : '')).filter(Boolean).slice(0, 60),
      links: [...root.querySelectorAll('main a[href]')].filter(vis).map((a) => `${t(a)}→${a.getAttribute('href')}`).slice(0, 25),
      alerts: [...root.querySelectorAll('[role=alert],[role=status],[aria-live]')].filter(vis).map(t).filter(Boolean).slice(0, 6),
    };
  }, scope);
}

/** Yolculuk kaydı: adım tablosu + konsol + ağ → evidence/commands/E2E-<ad>.json */
export function recorder(name) {
  const rows = [];
  return {
    rows,
    add(step, expected, observed, ok, extra = {}) {
      rows.push({ step, expected, observed: typeof observed === 'string' ? observed : JSON.stringify(observed), ok, ...extra });
      console.log(`${ok ? 'OK ' : 'XX '} ${step} — ${typeof observed === 'string' ? observed : JSON.stringify(observed)}`.slice(0, 300));
    },
    save(extra = {}) {
      writeFileSync(`${ROOT}/commands/E2E-${name}.json`, JSON.stringify({ journey: name, ranAt: new Date().toISOString(), base: BASE, steps: rows, ...extra }, null, 1));
    },
  };
}

export const overflowX = (page) => page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
