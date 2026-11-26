# `PHP-LARAVEL-SETUP.md` — Faz 20 Yaması

> **Tarih:** 26 Kasım 2026 · **Kaynak:** `AUD-2026-11-26` ([`REPORT.md`](../../audits/2026-11-26-post-faz-19-scan/REPORT.md)) ·
> takip tablosu [`phases/faz-20/README.md`](../../phases/faz-20/README.md)
> **Ne bu:** Ana devir dosyasına (`context/PHP-LARAVEL-SETUP.md`) **işlenmeyi bekleyen** Faz 20 kayıtları. `-EK-FAZ-19` ile aynı biçim.
> **Tam kayıt:** `davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-20.md` · Numaralar K263'ten başlar (K263–K264).

---

## A. Karar Kaydı'na eklenecek (§7)

### 20.1 — `OPS-10` (kod şemanın önünde: yerel veritabanı 4 göç geride, Hesap Ayarları 500)

Dal: backend `fix/2026-11-26-ops-10-schema-readiness` → `faz-20-critical-fixes`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K263** | Hazır olma ucu (`GET /api/health`) beşinci kontrol `schema`'yı taşır: göç dosyalarından (`database/migrations` + `Migrator::paths()`, `migrate:status` ile aynı) biri `migrations` tablosunda yoksa ya da tablo yoksa 503. Dosyası olmayan fazla kayıt başarısızlık değildir. Veritabanına ulaşılamazken `["database","schema"]` birlikte döner (fail-closed) | Yerelde katı kip eksik sütunu 500'e çevirdi; canlıda katı kip kapalı (`shouldBeStrict(! isProduction())`), eksik sütun `null` okunur ve `hasPublished()` gibi savunmalar sessizce kapanır. `/api/ping` ve `database` kontrolü bu durumu görmez; dış izleyici (`IZLEME.md`) ancak bu adla alarm verir | geçerli · Faz 20.1 (26 Kas) |

**Eski kararların durum notları:**

- K255 → geçerli; kontrol listesi dörtten beşe çıktı (`schema`, K263).

### 20.4 — `OPS-06` ↑ (deploy sırasında kod şemanın önünde)

Dallar: backend `fix/2026-11-26-ops-06-deploy-maintenance`, frontend `fix/2026-11-26-ops-06-neutral-unavailable-message`
→ `faz-20-critical-fixes`. Seçenekler [`phases/faz-20/README.md`](../../phases/faz-20/README.md) §20.4; İsmail'in cevabı (26 Kasım 2026): **A**.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K264** | Backend deploy'u bakım kipinde yapılır: `deploy.sh` güvenlik kontrollerinden sonra, `git pull`'dan **önce** `artisan down --retry=60` (şablonsuz: API Laravel'e ulaşır, `503 PROVIDER_UNAVAILABLE` zarfı döner); `migrate` + FPM reload + `queue:restart`'tan sonra `artisan up`. Hata olursa bakımda kalır ve betik bunu yazar; elle `up` yapılmaz. Betik `set -Eeuo pipefail` (ERR tuzağı fonksiyon içinde de). Frontend `PROVIDER_UNAVAILABLE` metni tarafsız ("Hizmet şu anda yanıt veremiyor") | `git pull` kodu göçten önce canlıya alıyordu; canlıda katı kip kapalı olduğu için yarım şema 500 değil sessiz yanlış cevap verir (`hasPublished()` → `false`). Her deploy'da 30–60 sn kesinti, tutarsız cevaba tercih edildi. Sürüm klasörü + sembolik bağ (kesintisiz) daha büyük sunucu değişikliği istediği için seçilmedi | geçerli · İsmail'in kararı · Faz 20.4 (26 Kas) |

- `deploy.md` §5 "`artisan down` bilerek eklenmedi" maddesi K264 ile kalktı (karar kaydı değildi, kılavuz notuydu).
- `AUD-2026-11-12` `OPS-06` (🟢) → `AUD-2026-11-26`'da 🟠, K264 ile kapandı.
