// AUD-2026-11-12 · D2 · keşif: sihirbaz adımlarını sırayla tıklar, her adımın kısa dökümünü basar.
// Kullanım: node j2-explore.mjs "<düğme metni>" "<düğme metni>" …   (her argüman sırayla tıklanır)
import { BASE, describe, open } from './lib.mjs';

const { browser, page, log } = await open();
await page.goto(`${BASE}/create`, { waitUntil: 'networkidle' });
for (const label of process.argv.slice(2)) {
  const target = label.startsWith('css=') ? page.locator(label.slice(4)).first() : page.locator('main').getByRole('button', { name: new RegExp(label) }).first();
  await target.click({ timeout: 8000 });
  await page.waitForTimeout(1500);
  console.log(`\n## tıklandı: ${label}`);
}
await page.waitForTimeout(1000);
console.log(JSON.stringify(await describe(page, 'main')));
console.log('net:', JSON.stringify(log.net), 'console:', JSON.stringify(log.console.slice(0, 5)));
await browser.close();
