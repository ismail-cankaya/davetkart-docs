// AUD-2026-11-12 · D2 · Yolculuk 1: giriş → çıkış → hatalı parola → hız sınırı mesajı → yeniden giriş.
// Kayıt adımı (1a) Playwright MCP ile koştu: j1a-register.js (hesap: elif.yildirim.aud996311@example.com).
import { BASE, DESKTOP, MOBILE, open, overflowX, recorder, saveState, shot, state } from './lib.mjs';

const user = (state.user ??= { email: 'elif.yildirim.aud996311@example.com', password: process.env.AUD_TEST_PASSWORD });
const rec = recorder('J1-auth');
const alertText = (page) => page.evaluate(() => [...document.querySelectorAll('main [role=alert], main [aria-live], main form p, main form div')]
  .map((e) => e.innerText?.trim()).filter((t) => t && t.length < 220 && /hata|yanlış|geçersiz|deneme|bekle|saniye|dakika|eşleş|bulunamadı/i.test(t)).slice(-1)[0] ?? null);

const { browser, page, log } = await open({ auth: false });

// 1) doğru giriş
await page.goto(`${BASE}/login`);
await page.fill('#login-email', user.email);
await page.fill('#login-password', user.password);
await shot(page, 'J1-giris-form-1440');
let [resp] = await Promise.all([page.waitForResponse((r) => r.url().includes('/api/auth/login')), page.locator('main').getByRole('button', { name: 'Giriş Yap' }).click()]);
await page.waitForURL('**/dashboard', { timeout: 8000 }).catch(() => {});
rec.add('Doğru e-posta ve parolayla giriş', '200, /dashboard', `${resp.status()}, ${new URL(page.url()).pathname}`, resp.status() === 200 && page.url().endsWith('/dashboard'));
await shot(page, 'J1-giris-sonrasi-1440');
const oldToken = await page.evaluate(() => JSON.parse(localStorage.getItem('davetkart_auth_session') ?? '{}').token ?? null);

// 2) çıkış
[resp] = await Promise.all([page.waitForResponse((r) => r.url().includes('/api/auth/logout')), page.getByRole('button', { name: 'Çıkış Yap' }).first().click()]);
await page.waitForTimeout(800);
const afterLogout = await page.evaluate(() => ({ path: location.pathname, session: localStorage.getItem('davetkart_auth_session') }));
rec.add('Çıkış', 'logout 2xx, oturum anahtarı silinir', `${resp.status()}, yol ${afterLogout.path}, localStorage oturumu ${afterLogout.session === null ? 'yok' : 'DURUYOR'}`, resp.status() < 300 && afterLogout.session === null);
const me = await page.evaluate(async (t) => (await fetch('/api/auth/me', { headers: { Authorization: `Bearer ${t}`, Accept: 'application/json' } })).status, oldToken);
rec.add('Çıkıştan sonra eski token', '401 (sunucuda iptal)', String(me), me === 401);
await page.goto(`${BASE}/dashboard`);
await page.waitForTimeout(600);
rec.add('Çıkıştan sonra /dashboard', '/login’e yönlenir', new URL(page.url()).pathname, page.url().includes('/login'));
await shot(page, 'J1-cikis-sonrasi-1440');

// 3) hatalı parola → 4) hız sınırı
await page.goto(`${BASE}/login`);
let limitedAt = null;
let firstWrong = null;
for (let i = 1; i <= 8 && !limitedAt; i++) {
  await page.fill('#login-email', user.email);
  await page.fill('#login-password', 'YanlisParola-123');
  [resp] = await Promise.all([page.waitForResponse((r) => r.url().includes('/api/auth/login')), page.locator('main').getByRole('button', { name: 'Giriş Yap' }).click()]);
  await page.waitForTimeout(500);
  const body = await resp.json().catch(() => ({}));
  const msg = await alertText(page);
  if (i === 1) {
    firstWrong = { status: resp.status(), code: body?.error?.code, msg, path: new URL(page.url()).pathname, emailKept: await page.inputValue('#login-email') };
    await shot(page, 'J1-hatali-parola-1440');
  }
  if (resp.status() === 429) {
    limitedAt = { attempt: i, code: body?.error?.code, retryAfterHeader: resp.headers()['retry-after'] ?? null, params: body?.error?.params ?? null, msg };
    await shot(page, 'J1-hiz-siniri-1440');
  }
}
rec.add('Hatalı parola (1. deneme)', '401 INVALID_CREDENTIALS, formda kalır, e-posta silinmez, Türkçe mesaj', firstWrong, firstWrong?.status === 401 && firstWrong.code === 'INVALID_CREDENTIALS' && firstWrong.path === '/login' && firstWrong.emailKept === user.email && !!firstWrong.msg);
rec.add('Hız sınırı', '5 hatalı denemeden sonra 429 RATE_LIMITED + Retry-After + süreli mesaj', limitedAt, !!limitedAt && limitedAt.code === 'RATE_LIMITED' && !!limitedAt.retryAfterHeader && /saniye|dakika/.test(limitedAt.msg ?? ''));

// mobil görünüm: sınır hâlâ sürerken
await page.setViewportSize(MOBILE);
await page.fill('#login-email', user.email);
await page.fill('#login-password', 'YanlisParola-123');
await Promise.all([page.waitForResponse((r) => r.url().includes('/api/auth/login')), page.locator('main').getByRole('button', { name: 'Giriş Yap' }).click()]);
await page.waitForTimeout(500);
await shot(page, 'J1-hiz-siniri-390', { fullPage: true });
rec.add('Mobil (390) giriş formu', 'yatay taşma yok', `taşma ${await overflowX(page)} px`, (await overflowX(page)) <= 0);
await page.setViewportSize(DESKTOP);

// 5) sınır dolunca doğru giriş (sonraki yolculuklar için oturum kaydı)
const wait = Number(limitedAt?.retryAfterHeader ?? 60) + 2;
console.log(`… hız sınırı için ${wait} sn bekleniyor`);
await page.waitForTimeout(wait * 1000);
await page.fill('#login-email', user.email);
await page.fill('#login-password', user.password);
[resp] = await Promise.all([page.waitForResponse((r) => r.url().includes('/api/auth/login')), page.locator('main').getByRole('button', { name: 'Giriş Yap' }).click()]);
await page.waitForURL('**/dashboard', { timeout: 8000 }).catch(() => {});
rec.add('Sınır dolduktan sonra doğru giriş', '200, /dashboard', `${resp.status()}, ${new URL(page.url()).pathname}`, resp.status() === 200);
state.storage = await page.context().storageState();
saveState();

rec.save({ console: log.console, net: log.net });
console.log('console:', JSON.stringify(log.console), '\nnet:', JSON.stringify(log.net));
await browser.close();
