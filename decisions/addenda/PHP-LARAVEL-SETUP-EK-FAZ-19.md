# `PHP-LARAVEL-SETUP.md` — Faz 19 Yaması

> **Tarih:** 20 Kasım 2026'da açıldı; Faz 19'un 28 bulgusu kapandıkça bölüm eklenir.
> **Ne bu:** Ana devir dosyasına (`context/PHP-LARAVEL-SETUP.md`) **işlenmeyi bekleyen** Faz 19 kayıtları.
> `-EK-FAZ-18` ile aynı biçim.
> **Tam kayıt:** `davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-19.md`
> **Kaynak:** `AUD-2026-11-12` ([`REPORT.md`](../../audits/2026-11-12-full-system-audit/REPORT.md) §5.1) ·
> takip tablosu [`phases/faz-19/README.md`](../../phases/faz-19/README.md)
> Numaralar K179'dan başlar ([`DECISION-INDEX.md`](../DECISION-INDEX.md), 20 Kasım).

---

## A. Karar Kaydı'na eklenecek (§7)

### 19.1 — `SEC-07` (Composer bağımlılıklarında bilinen açıklar; `composer audit` kırmızı)

Kod kılavuzları (backend `docs/rehber/`): `composer.md` · `app/Services/Payment/ShopierGateway.md` §12 ·
`tests/Feature/PaymentDriverResolutionTest.md` · `config/trustedproxy.md` (durum notu). Frontend değişmedi.

**§A:** iki satır da **boş** bırakıldı; varsayılanlar uygulandı. §A-1'in varsayılan komutu dolaylı
bağımlılıklarda majör sürüm atlattığı için iş durdu (prompt §8) ve İsmail oturumda majörsüz yolu seçti.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K179** | **Güvenlik güncellemesinin kapsamı:** `composer update "symfony/*" laravel/framework --with-all-dependencies` + üç geçici `--with` kısıtı (`guzzlehttp/psr7:^2.13`, `guzzlehttp/uri-template:^1.0.10`, `brick/math:^0.18`). Yalnızca `composer.lock` değişir: 55 paket (`laravel/framework` 13.35.0 → 13.43.0; açık taşıyan altı Symfony paketi 8.1.10/8.1.11); `composer.json` aynı (`content-hash` değişmedi); majör yok. Guzzle 8 / PSR-7 3 / `brick/math` 1.0 geçişi **ayrı karar** | Güvenlik yaması davranış değişikliği taşımamalı. `-W` tek başına beş dolaylı paketi majör atlatıyordu (`guzzle` 7 → 8 Laravel HTTP istemcisinin, AWS SDK'nın ve Sentry'nin altında). `-W` şart: Laravel 13.40+ `laravel/prompts ^0.3.25` istiyor, adı geçen paketlerle sınırlı güncelleme çözülmüyor. Alt sınır bugünkü sürüm: `^1.0` çözücüyü `uri-template`'i 1.0.0'a düşürmeye götürdü | ✅ Faz 19.1 (lock; `audit --locked` çıkış 0) · §A-1 varsayılanı (İsmail cevaplamadı) → §8 (majör) → İsmail "majörsüz"ü seçti · ⚠️ yeni `vendor` ile `composer check` koşmadı (GitHub erişilemedi; eski `vendor` ile 1168 test ✅) · ⚠️ sonraki düz `composer update` majörleri getirir |
| **K180** | **Dışarıya verilen mutlak adresler istekten değil yapılandırmadan üretilir.** Shopier callback = `rtrim(config('app.url'), '/')` + `ShopierGateway::CALLBACK_PATH`; açık üretim, küresel `URL::forceRootUrl` yok. Diğerleri zaten böyleydi: postalar `davetkart.frontend.url`, ödeme dönüşü `payment.return_urls` (K122), e-posta değişikliği göreli imza (K144), medya disk `url`'i | `url()` / `route()` kökü isteğin `Host`'undan (güvenilen vekil varsa `X-Forwarded-Host`'tan) alır; ikisi de istemcinin elinde (host header injection). Bugün sömürü yolu yok: Nginx tanımadığı host'u `444` ile keser, `TRUSTED_PROXIES` boş, saldırgan yalnızca kendi formunu bozabilir. Yani derinlemesine savunma. Küresel ayar her `url()`'yi etkiler ve etkisi çağrının yanında görünmez | ✅ Faz 19.1 · §A-2 varsayılanı (İsmail cevaplamadı) · ⚠️ `APP_URL` artık ödeme dönüşü için kritik; sunucudaki değer gözle doğrulanmadı · `docs/10` şablonu eski `api.davetkart.com`'u gösteriyor (`OPS-04`) |
| **K181** | **Yayın adayı = `composer check` ✅ ve `composer audit` ✅.** `composer audit` `composer check` zincirine **girmez**: CI'da ayrı adım ("Composer güvenlik taraması"), yayın kontrol listesinde ayrı madde ([`YAYIN-SIRASI.md`](../../operations/deployment/YAYIN-SIRASI.md) §2, madde 2). **K150'yi tamamlar** | `check` deterministik ve çevrimdışı: aynı commit, aynı sonuç. `audit` ağ ister ve zamana bağlı: aynı lock 13 Kasım sabahı 8, akşamı 9 açık verdi. Birleşirse ağ sorunu "kod bozuk" gibi görünür (19.1'de GitHub 40 dakikadan uzun erişilemedi) ve kapı zamana bağlanır. Ayrı adım olunca CI özetinde hangisinin patladığı tek bakışta görünür | ✅ Faz 19.1 |

**Tamamlanan karar:** K150 → **K181** (K150 geçerli; "kalite kapısı" yayın için iki parçalı oldu). Durum
notu [`DECISION-INDEX.md`](../DECISION-INDEX.md)'de. Geçersiz kılınan karar: yok.

Açık kalanlar (karar İsmail'in): Guzzle 8 / PSR-7 3 / `brick/math` 1.0 geçişi (ayrı dal; HTTP istemcisi,
S3 ve Sentry yolları sınanarak) · sunucudaki `APP_URL`'in yayından önce gözle doğrulanması
(`https://davetkart.com` olmalı) · `docs/10` üretim şablonunun düzeltilmesi (`OPS-04`, Faz 19.6).
