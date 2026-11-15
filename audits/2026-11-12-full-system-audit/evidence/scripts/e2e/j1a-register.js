// AUD-2026-11-12 · D2 · Yolculuk 1a: kayıt (1440 + 390). Playwright MCP `browser_run_code_unsafe` ile koşar.
async (page) => {
  const SHOT = 'D:/Projects/davetkart/davetkart-docs/audits/2026-11-12-full-system-audit/evidence/screenshots';
  // Dinleyiciler ve durum `page` nesnesinde tutulur: run_code çağrıları arasında globalThis kalıcı değil.
  if (!page.__aud) {
    page.__aud = { console: [], net: [] };
    page.on('console', (m) => { if (['error', 'warning'].includes(m.type())) page.__aud.console.push(`${m.type()}: ${m.text().slice(0, 220)}`); });
    page.on('pageerror', (e) => page.__aud.console.push(`pageerror: ${String(e).slice(0, 220)}`));
    page.on('requestfailed', (r) => page.__aud.net.push(`FAILED ${r.method()} ${r.url().replace('http://localhost:3000', '')} ${r.failure()?.errorText ?? ''}`));
    page.on('response', (r) => { if (r.status() >= 400) page.__aud.net.push(`${r.status()} ${r.request().method()} ${r.url().replace('http://localhost:3000', '')}`); });
  }
  const A = page.__aud;
  const mark = { c: A.console.length, n: A.net.length };
  const out = {};
  const email = `elif.yildirim.aud${Date.now().toString().slice(-6)}@example.com`;
  page.__audUser ={ email, password: process.env.AUD_TEST_PASSWORD, first: 'Elif', last: 'Yıldırım' };

  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('http://localhost:3000/register');
  await page.waitForSelector('#register-email');
  await page.screenshot({ path: `${SHOT}/J1-kayit-form-390.png`, fullPage: true });
  out.mobileOverflowX = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);

  await page.setViewportSize({ width: 1440, height: 900 });
  await page.screenshot({ path: `${SHOT}/J1-kayit-form-1440.png` });

  // boş gönderim: tarayıcı doğrulaması mı, uygulama mesajı mı?
  await page.getByRole('button', { name: 'Ücretsiz Kayıt Ol' }).click();
  out.emptySubmit = await page.evaluate(() => ({ invalid: document.querySelectorAll('main input:invalid').length, url: location.pathname }));

  await page.fill('#register-first-name', 'Elif');
  await page.fill('#register-last-name', 'Yıldırım');
  await page.fill('#register-email', email);
  await page.fill('#register-password', '<AUD_TEST_PAROLASI>');
  const [resp] = await Promise.all([
    page.waitForResponse((r) => r.url().includes('/api/auth/register')),
    page.getByRole('button', { name: 'Ücretsiz Kayıt Ol' }).click(),
  ]);
  out.registerStatus = resp.status();
  await page.waitForTimeout(1500);
  out.urlAfter = page.url().replace('http://localhost:3000', '');
  await page.screenshot({ path: `${SHOT}/J1-kayit-sonrasi-1440.png` });
  out.storageKeys = await page.evaluate(() => Object.keys(localStorage));
  out.header = await page.evaluate(() => [...document.querySelectorAll('header a, header button')].map((e) => `${e.tagName}:${(e.innerText || e.getAttribute('aria-label') || e.title || '').trim().slice(0, 30)}${e.getAttribute('href') ? '→' + e.getAttribute('href') : ''}`));
  out.h = await page.evaluate(() => [...document.querySelectorAll('h1,h2')].map((e) => e.innerText.trim().slice(0, 60)));
  out.console = A.console.slice(mark.c);
  out.net = A.net.slice(mark.n);
  out.email = email;
  return JSON.stringify(out);
}
