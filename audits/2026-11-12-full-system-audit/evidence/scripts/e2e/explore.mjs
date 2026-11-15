// AUD-2026-11-12 · D2 · keşif: verilen yolların kısa dökümünü basar. Kullanım: node explore.mjs [--anon] /login /create …
import { BASE, describe, open } from './lib.mjs';

const args = process.argv.slice(2);
const anon = args.includes('--anon');
const mobile = args.includes('--mobile');
const { browser, page, log } = await open({ auth: !anon, viewport: mobile ? { width: 390, height: 844 } : undefined });
// Yollar baştaki "/" OLMADAN verilir (Git Bash "/login"i Windows yoluna çevirir): node explore.mjs login create
for (const path of args.filter((a) => !a.startsWith('--')).map((a) => '/' + a.replace(/^\//, ''))) {
  await page.goto(BASE + path, { waitUntil: 'networkidle' }).catch(() => {});
  await page.waitForTimeout(800);
  console.log(`\n## ${path}\n` + JSON.stringify(await describe(page), null, 0));
}
if (log.console.length || log.net.length) console.log('\nconsole/net:', JSON.stringify(log));
await browser.close();
