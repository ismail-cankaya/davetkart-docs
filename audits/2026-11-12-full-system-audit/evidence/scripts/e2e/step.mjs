// AUD-2026-11-12 · D2 · komut satırından sürülen adım koşucusu. Tek tarayıcı bağlamında sırayla eylem koşturur,
// her eylemden sonra yol + yazma istekleri + yeni hataları basar; --rec ile evidence/commands/E2E-<ad>.json'a yazar.
//
// node step.mjs [--anon] [--mobile] [--reduced] [--rec <ad>] <başlangıç yolu (başında / YOK)> <eylem>…
// Eylemler:
//   click:<metin regex>        ana içerikte düğme/bağlantı/sekme (ilk eşleşen)        clickany:<regex> → bütün sayfada
//   css:<seçici>               CSS seçicisine tıkla                                    fill:<etiket>=<değer>   fillcss:<seçici>=<değer>
//   check:<etiket regex>       anahtar/onay kutusuna tıkla                             select:<etiket>=<değer>
//   upload:<css>=<dosya yolu>  dosya seç                                               key:<tuş>
//   goto:<yol>                 başka yola git                                          wait:<ms>   waitfor:<metin>
//   shot:<ad>                  ekran görüntüsü (evidence/screenshots/<ad>.png)          fullshot:<ad>
//   dump[:<css kapsam>]        sayfanın kısa dökümü                                    text:<css> → innerText (ilk 600)
//   mobile | desktop           görünümü değiştir                                       eval:<js ifadesi> (sayfada)
//   api:<METHOD> <yol> [json]  oturum token'ıyla doğrudan API isteği (sayfanın içinden fetch)
import { BASE, DESKTOP, MOBILE, describe, open, overflowX, recorder, saveState, shot, state } from './lib.mjs';

const argv = process.argv.slice(2);
const flag = (f) => argv.includes(f);
const recName = flag('--rec') ? argv[argv.indexOf('--rec') + 1] : null;
const rest = argv.filter((a, i) => !a.startsWith('--') && argv[i - 1] !== '--rec');
const start = '/' + rest[0].replace(/^\//, '');
const actions = rest.slice(1);

const { browser, page, log } = await open({ auth: !flag('--anon'), viewport: flag('--mobile') ? MOBILE : DESKTOP, reducedMotion: flag('--reduced') ? 'reduce' : undefined });
const writes = [];
page.on('response', (r) => {
  if (r.url().includes('/api/') && r.request().method() !== 'GET') writes.push(`${r.status()} ${r.request().method()} ${new URL(r.url()).pathname}`);
});
const rec = recName ? recorder(recName) : null;
const marks = { w: 0, c: 0, n: 0 };
const delta = () => {
  const d = { writes: writes.slice(marks.w), console: log.console.slice(marks.c), net: log.net.slice(marks.n) };
  marks.w = writes.length; marks.c = log.console.length; marks.n = log.net.length;
  return d;
};
// İmzalı bağlantıların sorgu kısmı (signature, token) çıktıya yazılmaz.
const where = () => { const u = new URL(page.url()); return u.pathname + (/signature|token|expires/.test(u.search) ? '?…(imzalı sorgu gizlendi)' : u.search); };
const out = (label, extra) => {
  const d = delta();
  const line = { a: label, url: where(), ...(d.writes.length ? { writes: d.writes } : {}), ...(d.net.length ? { net: d.net } : {}), ...(d.console.length ? { console: d.console.map((c) => c.slice(0, 140)) } : {}), ...(extra !== undefined ? { r: extra } : {}) };
  console.log(JSON.stringify(line));
  rec?.rows.push(line);
};

await page.goto(BASE + start, { waitUntil: 'domcontentloaded' });
await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
out(`goto ${start}`);

for (const act of actions) {
  const i = act.indexOf(':');
  const verb = i === -1 ? act : act.slice(0, i);
  const arg = i === -1 ? '' : act.slice(i + 1);
  let extra;
  try {
    if (verb === 'click' || verb === 'clickany') {
      const scope = verb === 'click' ? page.locator('main') : page;
      const re = new RegExp(arg);
      const cands = [scope.getByRole('button', { name: re }), scope.getByRole('link', { name: re }), scope.getByRole('tab', { name: re }), scope.getByRole('switch', { name: re }), scope.getByRole('radio', { name: re }), scope.getByText(re)];
      let done = false;
      for (const c of cands) {
        if (await c.first().isVisible().catch(() => false)) { await c.first().click({ timeout: 8000 }); done = true; break; }
      }
      if (!done) throw new Error('eşleşen görünür öğe yok');
      await page.waitForTimeout(900);
    } else if (verb === 'css') { await page.locator(arg).first().click({ timeout: 8000 }); await page.waitForTimeout(700); }
    else if (verb === 'tick') { await page.locator(arg).first().evaluate((el) => el.click()); await page.waitForTimeout(400); } // görsel olarak gizli onay kutuları
    else if (verb === 'fill') { const [l, v] = arg.split(/=(.*)/s); await page.getByLabel(new RegExp(l)).first().fill(v); }
    else if (verb === 'fillcss') { const [s, v] = arg.split(/=(.*)/s); await page.locator(s).first().fill(v); }
    else if (verb === 'check') { await page.getByRole('switch', { name: new RegExp(arg) }).first().click({ timeout: 8000 }); await page.waitForTimeout(600); }
    else if (verb === 'select') { const [l, v] = arg.split(/=(.*)/s); await page.getByLabel(new RegExp(l)).first().selectOption({ label: v }); }
    else if (verb === 'upload') { const [s, f] = arg.split(/=(.*)/s); await page.locator(s).first().setInputFiles(f); await page.waitForTimeout(2500); }
    else if (verb === 'key') { await page.keyboard.press(arg); await page.waitForTimeout(400); }
    else if (verb === 'goto') { await page.goto(BASE + '/' + arg.replace(/^\//, ''), { waitUntil: 'domcontentloaded' }); await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {}); }
    else if (verb === 'wait') { await page.waitForTimeout(Number(arg)); }
    else if (verb === 'waitfor') { await page.getByText(new RegExp(arg)).first().waitFor({ timeout: 20000 }); }
    else if (verb === 'shot') { extra = await shot(page, arg); }
    else if (verb === 'fullshot') { extra = await shot(page, arg, { fullPage: true }); }
    else if (verb === 'dump') { extra = await describe(page, arg || 'main'); }
    else if (verb === 'text') { extra = (await page.locator(arg).first().innerText({ timeout: 5000 })).replace(/\s+/g, ' ').slice(0, 600); }
    else if (verb === 'mobile') { await page.setViewportSize(MOBILE); await page.waitForTimeout(500); extra = { overflowX: await overflowX(page) }; }
    else if (verb === 'desktop') { await page.setViewportSize(DESKTOP); await page.waitForTimeout(500); }
    else if (verb === 'eval') { extra = await page.evaluate(arg); }
    else if (verb === 'api') {
      const m = arg.match(/^(\w+) (\S+)(?: (.*))?$/s);
      extra = await page.evaluate(async ([method, path, body]) => {
        const t = JSON.parse(localStorage.getItem('davetkart_auth_session') ?? '{}').token;
        const r = await fetch('/api' + path, { method, headers: { Accept: 'application/json', ...(t ? { Authorization: `Bearer ${t}` } : {}), ...(body ? { 'Content-Type': 'application/json' } : {}) }, body: body || undefined });
        const text = await r.text();
        return { status: r.status, body: text.slice(0, 700) };
      }, [m[1], m[2], m[3] ?? null]);
    } else if (verb === 'webhook') {
      // Sahte sürücünün (PAYMENT_PROVIDER=fake) imzalı bildirimi: en yeni siparişe `arg` durumunu (paid|failed|refunded)
      // gönderir. İmza backend-e2e kopyasının kendi APP_KEY'iyle PHP içinde hesaplanır; anahtar hiçbir yere yazılmaz.
      const code = `$o = App\\Models\\Order::query()->latest('created_at')->first(); $p = json_encode(['providerRef' => $o->provider_ref, 'status' => '${arg}']); $s = hash_hmac('sha256', $p, config('app.key')); $r = Illuminate\\Support\\Facades\\Http::withHeaders(['X-Signature' => $s])->withBody($p, 'application/json')->post('http://127.0.0.1:8000/api/public/payments/webhook'); echo 'webhook='.$r->status().' order='.$o->id.' before='.$o->status->value.' after='.$o->fresh()->status->value;`;
      const { execFileSync } = await import('node:child_process');
      extra = execFileSync('C:/Users/ismail/.config/herd/bin/php85/php.exe', ['artisan', 'tinker', '--execute', code], { cwd: 'D:/Projects/davetkart/_audit-snap/backend-e2e', encoding: 'utf8' }).trim().split('\n').pop();
      await page.waitForTimeout(500);
    } else if (verb === 'maillink') {
      // MAIL_MAILER=log: backend-e2e/storage/logs/laravel.log içindeki EN SON <arg> yollu bağlantıya gider
      // (ör. maillink:eposta-onay). Bağlantının imzalı sorgu kısmı çıktıya ve kanıta YAZILMAZ.
      const { readFileSync } = await import('node:fs');
      const raw = readFileSync('D:/Projects/davetkart/_audit-snap/backend-e2e/storage/logs/laravel.log', 'utf8').slice(-400000)
        .replace(/=\r?\n/g, '').replace(/=3D/g, '=').replace(/&amp;/g, '&');
      const hits = [...raw.matchAll(new RegExp(`https?://[^\\s"'<>]*/${arg}\\?[^\\s"'<>]+`, 'g'))];
      if (!hits.length) throw new Error('logda bağlantı yok');
      const u = new URL(hits[hits.length - 1][0]);
      await page.goto(BASE + u.pathname + u.search, { waitUntil: 'domcontentloaded' });
      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
      await page.waitForTimeout(1500);
      extra = { path: u.pathname, queryKeys: [...u.searchParams.keys()] };
    } else throw new Error('bilinmeyen eylem');
  } catch (e) {
    extra = { HATA: String(e.message ?? e).split('\n')[0].slice(0, 200) };
    out(act, extra);
    break;
  }
  out(act, extra);
}
if (flag('--keep')) { state.storage = await page.context().storageState(); saveState(); }
rec?.save({ console: log.console, net: log.net, writes, command: process.argv.slice(2).join(' ') });
await browser.close();
