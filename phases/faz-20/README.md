# Faz 20 — Faz 19 sonrası kritik hatalar (`AUD-2026-11-26`)

Kaynak: [`audits/2026-11-26-post-faz-19-scan/REPORT.md`](../../audits/2026-11-26-post-faz-19-scan/REPORT.md).
Sıra kritikten aşağı. **Commit'leri bu fazda ajan atar** (İsmail'in 26 Kasım isteği; Claude etiketi yok). Push yok.
Frontend yalnızca 20.4'te değişti (`errors.json` metni); frontend `faz-20-critical-fixes` o adımda açıldı.

- **Entegrasyon dalı (backend, frontend):** `faz-20-critical-fixes` — `faz-19-fix`'in ucundan. Düzeltme dalları
  `fix/2026-11-26-<bulgu-id>-<kısa-ad>`, `--no-ff` ile buna birleşir.
- **Docs dalı:** `docs/2026-11-26-faz-20-critical-fixes` (`docs/2026-11-20-faz-19-audit-fixes` ucundan).
- **Resmî faz kaydı:** backend `docs/rehber/fazlar/FAZ-20.md` · kararlar [`EK-FAZ-20`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-20.md).

## Önce yapılan (kod dışı, 26 Kasım)

Yerel ortam koda eşitlendi; bildirilen hata bununla kapandı (rapor §1.5):
`pg_dump` yedeği → `php artisan migrate` (4 göç) · backend `composer install` (55 paket) · frontend `npm install` (5 paket).

## Takip

| Sıra | Bulgu | Önem | Konu | Depolar | Dal | K | Durum |
|---|---|---|---|---|---|---|---|
| 20.1 | `OPS-10` | 🔴 | `/api/health`'e `schema` kontrolü: bekleyen göç ya da `migrations` tablosu yoksa 503 | backend · docs | `fix/2026-11-26-ops-10-schema-readiness` | K263 | birleşti |
| 20.2 | `SEC-51` | 🟠 | Symfony 8.1.12 güvenlik yaması (`composer.lock`; `composer audit` yeşil) | backend | `fix/2026-11-26-sec-51-symfony-patch` | — (K179 deseni) | birleşti |
| 20.3 | `OPS-11` | 🟡 | `composer sync`: dal değiştirince/çekince bağımlılık + göç tek komut; kılavuz | backend · docs | `fix/2026-11-26-ops-11-local-sync` | — | birleşti |
| 20.4 | `OPS-06` ↑ | 🟠 | Deploy bakım kipinde (`artisan down` pull'dan önce, `up` göçten sonra); `set -E`; `PROVIDER_UNAVAILABLE` metni tarafsız | backend (`deploy/`, test) · frontend (`errors.json`) · docs | `fix/2026-11-26-ops-06-deploy-maintenance` · frontend `fix/2026-11-26-ops-06-neutral-unavailable-message` | K264 | birleşti (İsmail: seçenek **A**) |
| 20.5 | `FE-59` | 🟢 | `/eposta-dogrula` bağlantısız açılınca istek atma | frontend | — | — | **değişiklik yok**: sunucu doğru kodu (`EMAIL_VERIFICATION_INVALID`) veriyor, ekran doğru; frontend'de imza kontrolü kuralın ikinci kopyası olurdu |
| 20.6 | `OPS-13` | 🟢 | `composer setup` `APP_KEY`'i yerelde sorusuz yeniliyor → yalnızca boşsa üretir | backend · docs | `fix/2026-11-26-ops-13-setup-app-key` | — | birleşti |
| docs | `OPS-12` | 🟡 | Faz 19 satırları "PHPStan #11" diyor; gerçek engel `SEC-51`'di | docs · backend `fazlar/README.md` | bu dal | — | düzeltildi |

## 20.4 kararı (`OPS-06`) — İsmail: **A** (26 Kasım), K264

Bugün `deploy.sh`: `git pull` → `composer install` → önbellek → `migrate --force` → FPM reload. Kod ilk adımda
canlıda (OPcache varsayılanı dosyayı ≤2 sn'de yeniden okur); göç bitene kadar yeni kod eski şemayla çalışır, göç
yarıda kalırsa öyle kalır. Canlıda katı kip kapalı olduğu için belirti 500 değil, sessiz yanlış cevap olabilir
(`hasPublished()` → `false`).

| Seçenek | Kesinti | Değişiklik | Göç hata verirse |
|---|---|---|---|
| **A. Bakım kipi** (önerilen) | Her deploy'da ~30–60 sn 503 (`Retry-After`) | `deploy.sh`'ye `artisan down` / `up` + kılavuz; `deploy.md` §5 kararı değişir | Site bakımda kalır; yarım şemayla cevap vermez |
| B. Sürüm klasörü + sembolik bağ | Yok (bağ değişimi anlık) | `releases/<sha>`, paylaşılan `storage/`, `.env`; FPM kökü ve Nginx değişir | Bağ eski sürümde kalır; yalnızca geriye uyumlu göçlerle güvenli |
| C. Bugünkü gibi + 20.1 alarmı | Yok | Yok | Alarm gelir, el ile müdahale |

## Doğrulama

Backend `faz-20-critical-fixes` @ `18fb74e` (kod ucu `6b3b450`) · frontend `faz-20-critical-fixes` @ `d10e7b2` · 26 Kasım 2026.

| Kapı | Sonuç (görülen çıktı) |
|---|---|
| Backend `composer check` | ✅ pint · PHPStan 0 · errors/plans/env:template · `k18: 32 dosya, 0 ihlal` · **1306/1306** test (4765 doğrulama; 20.4 öncesi 1304/1304) |
| Backend `composer audit` | ✅ "No security vulnerability advisories found." (20.2'den önce: 5 bildirim, 3 paket) |
| 20.1 mutantları | `array_diff` yönü ters → 2 test kırmızı · tablo yokken `true` → 1 test kırmızı · kontrol kayıtsız → 200 (yazılmadan önce görüldü) |
| 20.6 koruma | Ayrı klasörde 5 `.env` biçimi: boş LF / boş CRLF / yalnızca boşluk → `key:generate`; dolu / tırnaklı → dokunulmadı |
| Yerel eşitlik | `composer install --dry-run` "Nothing to install…" · `migrate:status --pending` "No pending migrations" · `composer sync` çıkış 0 |
| Frontend `npm run check` | ✅ tsc · build · 15 `verify:*` · 712,0 / 720 kB · 790,2 / 800 kB |
| Frontend `npm run e2e` | ✅ **6/6** iki kez: 20.4 öncesi (frontend `5c68df3`) ve sonrası (frontend `d10e7b2` + backend `6b3b450`) |
| 20.4 deploy betiği (stub'lı, sunucusuz) | ✅ 5 senaryo: başarı · `migrate` / `config:cache` düşer → bakımda kalır + mesaj · `up` sonrası ping düşer → yalnızca `HATA` · `down` düşer. Eski betikte göç hatası mesajsızdı (`set -E` eksikti) |
| `MaintenanceModeTest` | ✅ bakımda `503 PROVIDER_UNAVAILABLE` zarfı; mutant (`deactivate`) kırmızı |
| Hesap sayfaları (başsız Chromium, çalışan Vite + backend, user 2) | ✅ 6 hesap sayfası dahil 17/18 rota temiz; `/eposta-dogrula` sorgusuz 422 (20.5: beklenen) |
| İsmail'in tarayıcısı · canlı sunucu | koşmadı |

## İsmail'e kalan

1. Tarayıcında Hesap Ayarları'nın üç sayfasını aç (sunucuyu yeniden başlatmana gerek yok; `artisan serve` her istekte yeni kodu okur).
2. ~~20.4 kararı~~ → A (K264). Canlıdaki **ilk** deploy eski betikle başlar; `down` o seferlik pull'dan sonra açılır (`deploy.md` adım 0b). Deploy'dan önce izleyicide bakım penceresi aç (`IZLEME.md`).
3. Dalları `faz-19-fix` → `main` sırasına göre ne zaman birleştireceğin ve push (bu fazda push yapılmadı).
4. Bundan sonra `git pull` / dal değişiminden sonra: backend `composer sync`, frontend Vite'ı durdurup `npm ci`.
5. Natro posta kararı **11 Aralık**'a kadar (rapor §4).
