// AUD-2026-11-12 · D2 · Yolculuk 2: davetiye oluştur → editör → otomatik kaydetme → önizleme.
// Kullanım: node j2-create.mjs [--dump]   (--dump: editörün dökümünü basar, keşif için)
import { BASE, DESKTOP, MOBILE, describe, open, overflowX, recorder, saveState, shot, state } from './lib.mjs';

const rec = recorder('J2-create');
const { browser, page, log } = await open();
const api = [];
page.on('response', (r) => {
  if (r.url().includes('/api/') && r.request().method() !== 'GET') api.push(`${r.status()} ${r.request().method()} ${new URL(r.url()).pathname}`);
});

await page.goto(`${BASE}/create`, { waitUntil: 'networkidle' });
await shot(page, 'J2-kategori-1440');
await page.locator('main').getByRole('button', { name: /^Düğün/ }).first().click();
await page.waitForTimeout(1200);
await shot(page, 'J2-tema-1440');
await page.locator('main').getByRole('button', { name: /^Zarif Sadelik/ }).first().click();
await page.waitForTimeout(1200);

await page.getByLabel('Gelin Adı').fill('Zeynep');
await page.getByLabel('Damat Adı').fill('Emre');
await page.getByLabel(/Etkinlik Tarihi/).fill('2027-06-12T19:00');
await page.getByLabel('Davet Konumu').fill('Çırağan Sarayı, Beşiktaş / İstanbul');
await page.getByLabel('1. adımın saati').fill('19:00');
await page.getByLabel('1. adımın başlığı').fill('Nikâh Töreni');
await page.getByLabel('2. adımın saati').fill('20:30');
await page.getByLabel('2. adımın başlığı').fill('Yemek ve Kutlama');
await shot(page, 'J2-bilgiler-1440', { fullPage: true });

const before = api.length;
await page.locator('main').getByRole('button', { name: 'Davetiyeni Oluştur' }).click();
await page.waitForTimeout(9000); // "oluşturuluyor" animasyonu + ilk kayıt
const created = api.slice(before);
rec.add('Sihirbaz: Düğün → Zarif Sadelik → bilgiler → "Davetiyeni Oluştur"', 'POST /api/invitations 201, editör açılır', { api: created, url: new URL(page.url()).pathname + new URL(page.url()).search }, created.some((c) => c.startsWith('201 POST /api/invitations')));
await shot(page, 'J2-editor-1440');
const d = await describe(page, 'main');
if (process.argv.includes('--dump')) console.log(JSON.stringify(d));

// kayıt kimliği: sunucudaki listeden
const list = await page.evaluate(async () => {
  const t = JSON.parse(localStorage.getItem('davetkart_auth_session')).token;
  const r = await fetch('/api/invitations', { headers: { Authorization: `Bearer ${t}`, Accept: 'application/json' } });
  return (await r.json()).data.map((x) => ({ id: x.id, status: x.status, names: x.invitation?.names, updatedAt: x.updatedAt }));
});
state.invitationId = list[0]?.id;
saveState();
rec.add('Sunucuda kayıt', '1 davetiye, durum saved, adlar "Zeynep & Emre"', list, list.length === 1 && list[0].status === 'saved');

// otomatik kaydetme: editörde bir alanı değiştir, PUT bekle
const venue = page.getByLabel('Davet Konumu');
if (await venue.count()) {
  const mark = api.length;
  await venue.fill('Çırağan Sarayı Balo Salonu, Beşiktaş / İstanbul');
  const put = await page.waitForResponse((r) => r.request().method() === 'PUT' && r.url().includes('/api/invitations/'), { timeout: 15000 }).catch(() => null);
  await page.waitForTimeout(800);
  const server = await page.evaluate(async (id) => {
    const t = JSON.parse(localStorage.getItem('davetkart_auth_session')).token;
    const r = await fetch(`/api/invitations/${id}`, { headers: { Authorization: `Bearer ${t}`, Accept: 'application/json' } });
    return (await r.json()).data.invitation.venue;
  }, state.invitationId);
  rec.add('Otomatik kaydetme: konum değiştirildi, "Kaydet"e basılmadı', 'PUT /api/invitations/{id} 200; sunucuda yeni değer', { put: put?.status() ?? null, api: api.slice(mark), server }, put?.status() === 200 && server.includes('Balo Salonu'));
} else {
  rec.add('Otomatik kaydetme', 'editörde konum alanı', 'alan bulunamadı', false);
}
await shot(page, 'J2-editor-kayit-sonrasi-1440');

// yenileme: taslak sunucudan geri geliyor mu
await page.reload({ waitUntil: 'networkidle' });
await page.waitForTimeout(1500);
const afterReload = await page.evaluate(() => document.body.innerText.includes('Balo Salonu') || [...document.querySelectorAll('input')].some((i) => i.value.includes('Balo Salonu')));
rec.add('Sayfa yenilendi', 'editör aynı davetiyeyle açılır', { url: new URL(page.url()).pathname + new URL(page.url()).search, valueKept: afterReload }, afterReload);

// mobil
await page.setViewportSize(MOBILE);
await page.waitForTimeout(800);
await shot(page, 'J2-editor-390');
rec.add('Editör mobil (390)', 'yatay taşma yok', `taşma ${await overflowX(page)} px`, (await overflowX(page)) <= 0);
await page.setViewportSize(DESKTOP);

rec.save({ console: log.console, net: log.net, api });
console.log('net:', JSON.stringify(log.net), '\nconsole:', JSON.stringify(log.console.slice(0, 6)));
await browser.close();
