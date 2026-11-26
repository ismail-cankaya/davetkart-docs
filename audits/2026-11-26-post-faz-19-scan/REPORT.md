# AUD-2026-11-26 — Faz 19 sonrası hata taraması

| | |
|---|---|
| **Kimlik** | `AUD-2026-11-26` |
| **Tetikleyen** | İsmail (26 Kasım 2026): Faz 19'dan sonra Hesap Ayarları → **Genel Bakış**, **Planlarım**, **Gizlilik ve Hesap** "Bir aksaklık oldu" diyor. İstek: önce analiz, sonra bütün hataları tara, Faz 20'de kritikten başlayarak düzelt. |
| **Yürüten** | Claude Code (Opus 5.5), İsmail'in makinesi, ana çalışma klasörleri |
| **Taranan uçlar** | backend `faz-19-fix` @ `7f589e7` · frontend `faz-19-fix` @ `5c68df3` · docs `docs/2026-11-20-faz-19-audit-fixes` @ `ee7f729` (üçü de `origin` ile eşit, temiz) |
| **Düzeltme** | [`phases/faz-20/README.md`](../../phases/faz-20/README.md) — dallar backend `faz-20-critical-fixes` (frontend kodu değişmedi) · `docs/2026-11-26-faz-20-critical-fixes` |
| **Sonuç** | 🔴 1 (ortamda kapandı, kalıcı önlem Faz 20.1) · 🟠 2 (biri `OPS-06` ↑) · 🟡 2 + 1 bilgi · 🟢 2 + 1 bilgi. Kod tabanında bildirilen hatayı üreten bir kod hatası **yok**; kök neden yerel ortamın koddan geri kalması. |

## 1. Bildirilen hata: Hesap Ayarları'nın üç sayfası

### 1.1 Belirti → istek

Üç sayfa da aynı kancayı kullanıyor: `useAccountEntitlements()` → `GET /api/account/entitlements`
(`AccountOverviewSection.tsx`, `AccountPlansSection.tsx`, `AccountPrivacySection.tsx`; Gizlilik sayfası hesap silme
uyarısı için yükler). Uç 500 dönünce `toDisplayError` → `errors.json` `SERVER_ERROR` = "Bir aksaklık oldu…".
Siparişler ve Güvenlik sayfaları bu ucu çağırmadığı için açılıyordu. Panel aynı ucu çağırır ama hatayı yutar
(`DashboardPage.tsx:203`), o yüzden panel sağlam görünüyordu.

### 1.2 Kanıt

| Kaynak | Görülen |
|---|---|
| `storage/logs/laravel-2026-11-25.log`, `-26.log` | 58 kez `MissingAttributeException: The attribute [first_published_at] either does not exist or was not retrieved for model [App\Models\Order]`, hep `userId: 2`. Yığın: `AccountController::entitlements` → `SummarizeEntitlementsAction:59` → `RefundEligibility::blockerFor` → `usageBlockerFor:60` → `Order::hasPublished():177` |
| `php artisan migrate:status --pending` | 4 göç bekliyor: `2026_11_16_100000_add_one_pending_first_publish_index_to_orders` (18.3), `2026_11_17_100000_add_first_published_at_to_orders_table` (18.4), `2026_11_25_100000_mark_existing_accounts_as_verified` (K260), `2026_11_25_110000_add_buyer_phone_to_orders_table` (K262) |
| `migrations` tablosu | Son batch 11: `2026_10_26_120000_…` — yerel veritabanı **26 Ekim'den beri** göç almamış (Faz 14 sonu) |
| `information_schema.columns` | `orders.first_published_at` ve `orders.buyer_phone` **yok** |
| Salt okunur yeniden üretim (tinker, her kullanıcı için `SummarizeEntitlementsAction`) | user 2: `MissingAttributeException`; user 1, 3, 4, 5: OK |

### 1.3 Kök neden zinciri

1. Faz 18.4 (`SEC-02`) `Order::hasPublished()` ile `orders.first_published_at`'i okumaya başladı; sütun göçle geldi.
2. Ana çalışma klasöründeki geliştirme veritabanı (`davetkart`) bu göçü hiç almadı. Faz 18–19 kapıları
   `RefreshDatabase` ile **test veritabanlarında** (`davetkart_test`, `davetkart_test_hat_*`) koştu; orada şema hep
   günceldi. Faz 19 hatları da ayrı worktree'lerdeydi. Ana klasörü koda eşitleyen bir adım yok (bkz. `OPS-11`).
3. Geliştirmede Eloquent katı kipte (`AppServiceProvider:374`, `shouldBeStrict(! isProduction())`): seçilen satırda
   olmayan sütunu okumak `null` değil istisna.
4. **Neden yalnızca user 2:** `usageBlockerFor()` önce `invitation_id !== null || isConsumed()`'a bakar ve
   `InUse`'ta kısa devre yapar. Bütün hakları bağlı ya da yanmış kullanıcıda `hasPublished()` hiç çağrılmaz. User 2'nin
   davetiyeye bağlanmamış (kullanılabilir) bir hakkı var → sütun okunur → istisna.

### 1.4 Aynı kökten gelen, henüz görülmemiş kırıklar (yerel)

| Akış | Ne olurdu |
|---|---|
| Davetiye yayınlama | `StampFirstPublishAction` olmayan sütuna yazar → SQL hatası, 500 |
| Kartla ödeme | `orders.buyer_phone` yok → sipariş oluşturma 500 |
| Ödeme / yayın (doğrulama) | K260 göçü koşmadığı için 5 hesaptan 3'ü doğrulanmamış görünüyordu → `403 EMAIL_NOT_VERIFIED` |
| İlk yayın indirimi | `orders_one_pending_first_publish_per_user` kısmi UNIQUE index yok → 18.3'ün veritabanı katmanı yerelde kapalı |

### 1.5 Ortamda yapılan düzeltme (26 Kasım 2026)

| Adım | Sonuç (görülen çıktı) |
|---|---|
| Yedek | `pg_dump -Fc davetkart` → oturumun geçici klasöründe (`davetkart-before-migrate-2026-11-26.dump`, 66 978 bayt), exit 0 |
| Ön koşul | `2026_11_16` göçünün çakışma sorgusu: 0 kullanıcı (göç veri değiştirmeden durmaz) |
| `php artisan migrate` | 4 göç `DONE`; `migrate:status --pending` → "No pending migrations" |
| Yeniden üretim | 5 kullanıcının hepsi OK (user 2: 4 hak) |
| API duman testi | Her kullanıcıya geçici token, oturumlu bütün GET uçları (`/account/entitlements`, `/auth/me`, `/auth/sessions`, `/invitations`, `/invitations/{id}`, `/invitations/{id}/rsvps`, `/orders`, `/orders/{id}`, `/pricing`) + `/public/invitations/{id}` + `/public/plans`: **112 istek, 0 hata**. Token'lar silindi (5/5) |
| Tarayıcı taraması | Başsız Chromium, çalışan Vite (3000) üzerinden user 2 ile 18 rota: `/dashboard`, `/hesap` + 5 alt sayfa, `/pricing`, `/odeme/basarili`, `/odeme/hata`, `/eposta-dogrula`, 7 açık sayfa, yayındaki davetiye. **17 rota temiz** (konsol hatası, ≥400 API yanıtı, hata toast'ı yok); `/eposta-dogrula` bağlantısız açılınca 422 (`FE-59`). Token silindi |

## 2. Tarama yöntemi

| Kontrol | Sonuç |
|---|---|
| Backend `composer check` (eski `vendor/`) | ✅ pint · PHPStan 0 · errors/plans/env:template · `k18: 30 dosya, 0 ihlal` · **1301/1301 test** |
| Backend `composer check` (`vendor/` kilide eşitlendikten sonra) | ✅ aynı, 1301/1301 |
| `composer audit` | 🔴 **5 bildirim, 3 paket** (`SEC-51`) |
| Frontend `npm run check` (ilk) | 🔴 `tsc`: `TS2307 Cannot find module '@playwright/test'` ×11 (`OPS-11`) |
| Frontend `npm run check` (`node_modules` onarıldıktan sonra) | ✅ tsc · build · 15 `verify:*` · ilk yükleme **712,0 / 720 kB** · misafir **790,2 / 800 kB** |
| `npm audit` (tam ve `--omit=dev`) | ✅ 0 açık |
| Log taraması (15–26 Kasım, `ERROR`/`CRITICAL`/`WARNING`) | `first_published_at` dışında: 1 Gemini uyarısı, 1 eski deneme veritabanı (`davetkart_sec04_yok`) bağlantı hatası — ikisi de beklenen |
| Aynı hata sınıfı (kısmi `select` + katı kip) için kod araması | `->select(`/`->get([...])` 5 yer; hepsi yalnızca seçtiği sütunları okuyor |
| `TODO`/`FIXME` | Yok |
| Faz 19 açık listeleri | `HAT-A-ACIK-KALANLAR.md`, `HAT-B-ACIK-KALANLAR.md`, `HAT-C-ACIK-HATALAR.md` okundu; kapanmış maddeler yeniden raporlanmadı (§4) |
| `npm run e2e` | Faz 20 backend ucuna karşı ✅ 6/6 ([`phases/faz-20/README.md`](../../phases/faz-20/README.md) §Doğrulama) |

## 3. Bulgular

Yeni kimlikler `AUD-2026-11-12`'nin en büyük numaralarından devam eder (çakışma olmasın diye); önceki denetimde kayıtlı olup önemi değişen bulgu eski kimliğiyle ve ↑ işaretiyle yazılır.

### 🔴 Kritik

| # | Bulgu | Kanıt | Durum |
|---|---|---|---|
| **OPS-10** | Yerel veritabanı 4 göç geride: Hesap Ayarları'nın üç sayfası 500; yayın, kartla ödeme ve doğrulama da kırık (§1) | §1.2 | ✅ ortamda kapandı (§1.5). Kalıcı önlem: **20.1** `/api/health`'e `schema` kontrolü (K263) |

### 🟠 Yüksek

| # | Bulgu | Kanıt | Öneri |
|---|---|---|---|
| **OPS-06** ↑ | **`AUD-2026-11-12`'nin `OPS-06`'sı (🟢 "dağıtım yerinde, bakım kipi yok") 🟠'ye yükseltildi: canlıda aynı durum sessiz ve para kaybettirir.** (a) Katı kip canlıda kapalı: eksik `first_published_at` `null` okunur, `hasPublished()` `false` → yayın yapmış hak iade edilebilir görünür (SEC-02 savunması kapanır), yazan yollar 500 verir. (b) `deploy/deploy.sh` kodu `git pull` ile **göçten önce** yerine koyar; repoda OPcache `validate_timestamps` ayarı yok (varsayılan açık → yeni dosyalar ≤2 sn'de devrede). Her deploy'da `composer install` + önbellek + göç süresince yeni kod eski şemayla çalışır; göç yarıda kalırsa (`2026_11_16` çakışan veride **bilerek** durur) bu durum kalıcı olur. `docs/rehber/deploy/deploy.md` §1 "`set -e` … yeni kod eski veritabanıyla canlıya çıkardı" diyerek bunun önlendiğini söylüyor: önlenmiyor (B4) | `deploy.sh:39-68`; `AppServiceProvider.php:374`; `deploy.md` §1, §5 ("`artisan down` bilerek eklenmedi") | ✅ **20.4** (İsmail: seçenek A, K264): deploy bakım kipinde; `set -E` ile ERR tuzağı artık `artisan()` içinde de çalışıyor (önce göç hatasında hata mesajı hiç basılmıyordu, stub'lı denemede görüldü); `PROVIDER_UNAVAILABLE` metni tarafsız. Sunucudaki OPcache ayarı koşmadı (B7) |
| **SEC-51** | `composer audit` kırmızı (25 Kasım'da yayımlandı): `symfony/http-kernel` CVE-2026-133743 · `symfony/mailer` CVE-2026-133751, CVE-2026-133755 (STARTTLS) · `symfony/routing` CVE-2026-133746, CVE-2026-133754 (UrlGenerator başka host). Kurulu 8.1.10–8.1.11; düzeltme 8.1.12. K181: audit kırmızıyken dal yayın adayı değil | `composer audit` çıktısı | ✅ **20.2**: `composer update "symfony/*" -W` (K179 deseni; yalnızca `composer.lock`, 14 yama sürümü) |

### 🟡 Orta

| # | Bulgu | Kanıt | Öneri |
|---|---|---|---|
| **OPS-11** | Ana çalışma klasörleri koddan geride (`OPS-10` ile aynı kök: pull/birleştirme sonrası eşitleme adımı yok). Backend `vendor/` kilidin **55 paket** gerisinde (Laravel 13.35.0 ↔ 13.43.0, `symfony/polyfill-time` eksik): yerel sunucu ve testler Faz 19.1'in kilidiyle değil eski paketlerle koşuyordu. Frontend `node_modules`'te 5 paket eksik (`@playwright/test`, `@axe-core/playwright`, `playwright`, `playwright-core`, `axe-core`; TST-04 ile geldi) → `npm run lint` kırmızı | `composer install --dry-run`; `node_modules/.package-lock.json` ↔ `package-lock.json` karşılaştırması | ✅ ortamda kapandı (`composer install`, `npm install`). ✅ **20.3**: `composer sync` (bağımlılık + göç) ve kılavuza "dal değiştirince / çekince" adımı. ⚠️ `npm ci` çalışan Vite varken `EPERM` ile yarıda kalıp `node_modules`'ü yarım bırakıyor (bu taramada oldu, `npm install` ile onarıldı): önce Vite durdurulur |
| **OPS-12** | `phases/README.md` Faz 19 satırı ve backend `fazlar/README.md` "`composer check` 🔴 PHPStan iç hatası (#11) → `v1.2.0` bekliyor" diyor; Hat C §E ve bu tarama `composer check`'i yeşil gördü. Etiketlerin gerçek engeli artık `SEC-51` idi. Depolarda hiç sürüm etiketi yok (Hat C #21) | iki README; `git tag -l` | ✅ Faz 20 kaydında iki satır düzeltildi; etiketler İsmail'in (Hat C #21, sıra: `main` birleştirme → `v1.0.0`…`v1.2.0`) |
| — | Paket bütçesi payı dar: ilk yükleme 8 kB, misafir 9,8 kB (B-E6, K237 cırcır) | `verify:bundle` | Bilgi; yeni özellik eklerken kapı kırmızıya döner |

### 🟢 Düşük

| # | Bulgu | Öneri |
|---|---|---|
| **FE-59** | `/eposta-dogrula` bağlantısız (sorgusuz) açılınca da `POST /api/public/email-verification/confirm?` gidiyor → 422 + konsol hatası. Ekran doğru ("doğrulanamadı") | Faz 20.5'te incelendi: **değişiklik yok**. Sunucu doğru kodu (`EMAIL_VERIFICATION_INVALID`) döndürüyor, ekran doğru mesajı gösteriyor; frontend'de imza kontrolü kuralın ikinci kopyası olurdu |
| **OPS-13** | `composer setup` (Laravel iskeleti) mevcut kurulumda `php artisan key:generate`'i yerelde **sorusuz** çalıştırır: `APP_KEY` değişir, IP hash'leri, e-posta değişikliği bağlantıları ve sahte ödeme imzaları geçersiz olur | ✅ Faz 20.6: `setup` yalnızca `APP_KEY` boşsa üretir |
| — | Yerelde kuyruk işçisi yok: 24 Kasım'dan beri 2 iş bekliyor (`MAIL_MAILER=log`, zararsız). `/api/health` yerelde `queue`, `scheduler` der | Bilgi: gerekirse `php artisan queue:work` |

## 4. Önceden bilinen, hâlâ açık (yeniden raporlanmadı)

Tek ev açık listelerdir; burada yalnızca sayım ve en acil olanlar:

- **Tarihi yaklaşan:** Natro posta barındırma kararı **11 Aralık 2026**'ya kadar ([`SURE-TAKVIMI.md`](../../operations/deployment/SURE-TAKVIMI.md) §3); `davetkart.com` otomatik yenileme hatırlatıcısı 25 Kasım'dı, durum bilinmiyor (alan adı 11 Eylül 2027'de bitiyor).
- **Hat A:** E5 (Shopier TCKN/adres, İ1), sunucu komutları İ2, İ3, İ8, doğrulanmayanlar D1–D6, D8 ([`HAT-A-ACIK-KALANLAR.md`](../../phases/faz-19/HAT-A-ACIK-KALANLAR.md)).
- **Hat B:** elle yapılacaklar B-İ1…B-İ13, kararlar K-1…K-7 ([`HAT-B-ACIK-KALANLAR.md`](../../phases/faz-19/HAT-B-ACIK-KALANLAR.md)).
- **Hat C:** #21 sürüm etiketleri, #28 zayıf parolalı mevcut hesaplar kararı, #29 dal temizliği, #31, §D elle işler ([`HAT-C-ACIK-HATALAR.md`](../../phases/faz-19/HAT-C-ACIK-HATALAR.md)).
- **Temizlik:** `D:\Projects\davetkart-hat-{a,b,c}` worktree'leri hâlâ kayıtlı (ayrık uçlarda).

## 4b. İkinci tarama (26 Kasım, İsmail: "başka hata var mı")

- **Hesap ayarlarının yazma akışları:** Faz 14 elle doğrulaması (15 adım + satın alma) ilk kez, başsız Chromium ile
  `davetkart_e2e` üzerinde: **16/16 geçti**. Bulunan tek hata: 401 yakalayıcısı ölü token'la `POST /auth/logout` gönderiyordu
  (ikinci 401). İnceleme sırasında iki komşu sorun: oturum açıklamasız düşüyordu (`FE-57` A) ve 401 sonrası aynı sekmede
  başka hesap girerse önceki hesabın hakları bellekte kalıyordu. Üçü de Faz 20.7.
- **`AUD-2026-11-12` düşük/öneri bulguları (27) kodda yeniden tarandı:** kapanmış `ARC-09`, `FE-09`, `FE-56`; düzeltilen
  `FE-06` (20.10), `FE-55` + `FE-57` C (20.8), `FE-57` B (20.9); karar isteyen `SEC-15`, `SEC-16`, `FE-58`, `ARC-06`, `ARC-07`
  ([`phases/faz-20/README.md`](../../phases/faz-20/README.md) §İkinci tarama). Hepsi Faz 22'de: [`phases/faz-21/README.md`](../../phases/faz-21/README.md) (26 Kasım'da Faz 21 olarak yeniden numaralandı).

## 5. Koşmadı (B7)

- Canlı sunucu: OPcache ayarı, `/api/health`, deploy penceresinin gerçekte ölçülmesi.
- Gerçek tarayıcıda (İsmail'in oturumu) üç sayfanın yeniden açılması: aynı Vite ve backend üzerinden başsız Chromium ile görüldü (§1.5), İsmail'in kendi tarayıcısında değil.
