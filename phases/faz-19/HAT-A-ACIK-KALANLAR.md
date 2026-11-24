# Faz 19 — Hat A: açık kalanlar, bilinen hatalar, yapılmayanlar

> **Tarih:** 25 Kasım 2026 · **Kapsam:** Hat A'nın 9 işi (19.5, 19.6, 19.10, 19.11, 19.12, 19.13, 19.14, 19.15, 19.26) · **Kararlar:** K183–K192
> **Kaynak:** `kayit/` altındaki 9 kaydın "Plandan sapma", "B7", "Gördüm, dokunmadım" ve "İsmail'e kalan" bölümleri, oturumda görülenler
> ve 25 Kasım'da birleşik dallarda (backend `faz-19-audit-fixes` @ `0743874`, frontend @ `fe70b62`) koşulan kapılar.
> **Durum:** 9 işin hepsi entegrasyon dallarına birleşmiş, 19.90 kayıtları ortak dosyalara aktarmış; birleşmemiş Hat A dalı yok.

## 0. Özet

| Bölüm | Adet | En önemlisi |
|---|---|---|
| 1. Bilinen hatalar | 4 (1'i kapandı) | Taslak tavanı dolunca editör "bağlantınızı kontrol edin" diyor (FE-50); PHPStan önbelleği hatlar arasında ortak |
| 2. Eksikler | 9 | Mevcut hesaplar doğrulanmamış sayılıyor: canlıya çıkınca hiçbiri ödeme/yayın yapamaz (SEC-09) |
| 3. Koşulmayan doğrulamalar | 9 | Sunucuda `about` / `schedule:list` / SES; tarayıcıda doğrulama bandı ve sayfası |
| 4. Elle yapman gerekenler | 8 | Shopier sorusu, sunucu `.env` anahtar karşılaştırması |
| 5. Bekleyen kararlar | 9 | §A'sı boş geçilen 8 işin varsayılanları + PHPStan |
| 6. Temizlik ve devir | 5 | 20 birleşmiş Hat A dalı silinebilir |

## 1. Bilinen hatalar (bugün kırmızı ya da yanlış çalışan)

| # | Hata | Nerede | Kaynak | Hat A'nın mı? | Önerilen düzeltme |
|---|---|---|---|---|---|
| H1 | `composer check` PHPStan adımında kırmızı; zincir orada durduğu için sonraki adımlar (`errors`/`plans`/`env`/test) `composer check` içinden hiç koşmadı, her işte elle koşuldu | backend `app/Console/Commands/Concerns/ResolvesRefundRequests.php:29` (×2) · `tests/…/ReadinessTest.php:175` | 9 kaydın B7 tabloları · Hat C #1, #11 | Hayır (14.6 ve Hat C 19.7.1); Hat A dosyaları PHPStan'da temiz | Hat C `HAT-C-ACIK-HATALAR.md` #1 (`is_string` daraltması) + `ReadinessTest` tip düzeltmesi; `ignoreErrors` değil |
| H2 | Taslak tavanı (50) dolunca sihirbazın ilk kaydı `403 DRAFT_LIMIT_REACHED` alıyor ama editör yalnızca genel notu gösteriyor: "Kaydedilemedi — bağlantınızı kontrol edin, bir sonraki değişiklikte yeniden denenir". `errors.json`'daki doğru mesaj ("kullanmadığınız taslakları silin") hiç görünmüyor; her düzenleme aynı 403'ü yeniden üretiyor. "Davetiyeni Oluştur" `void saveInvitation()` ile hatayı yutuyor | frontend `src/stores/useInvitationStore.ts` `runSave` `catch` · `src/components/create/EditorWorkspace.tsx` kaydetme notu · `src/components/create/DetailsFormStep.tsx` `handleSubmit` | FE-50 (bu rapor için kod okundu; tarayıcıda denenmedi) | **Evet** | `runSave` `catch`'inde `apiErrorCode(error) === 'DRAFT_LIMIT_REACHED'` → `toast(toDisplayError(error), 'error')` + yeniden denemeyi durduran ayrı `saveState` (ör. `'rejected'`) ya da `/dashboard`'a yönlendirme. `verify:state`'e bir kontrol. Yayın yolu doğru: `publishInvitation` hatayı fırlatıyor, `EditorWorkspace` `toDisplayError` gösteriyor |
| H3 | **PHPStan sonuç önbelleği bütün worktree'lerde ortak** (`tmpDir` ayarı yok → `%TEMP%\phpstan`). 25 Kasım'da birleşik dalda aynı komut **501 hata** verdi (çoğu `missingType.iterableValue`, `TRelatedModel given`); `tmpDir` ayrı bir klasöre verilince aynı kod **3 hata** (H1). Hatlar aynı anda analiz koşunca biri ötekinin önbelleğini okuyup yanlış rapor alıyor; Hat C #11'deki iç hata da büyük olasılıkla bu | backend `phpstan.neon` | bu rapor (kanıt §7) | Hayır (ortak araç ayarı); ortak dalda çalışmayı doğrudan etkiler | `phpstan.neon` → `tmpDir: storage/phpstan` (klasör `.gitignore`'da olmalı); düzelene kadar her koşudan önce `vendor/bin/phpstan clear-result-cache` |
| H4 | SEC-09'un e2e doğrulama kancası `storage/logs/laravel.log`'u okuyordu; `.env` `daily` kanalda olduğu için dosya hiç oluşmuyor, yolculuk 1 ilk adımda düşüyordu | frontend `e2e/support/flows.ts` `verifyEmailIfRequired` | FE-53 kaydı "Ön koşul onarımı" | **Evet** | ✅ **Kapandı** — Hat B 19.25'te `scripts/e2e/backend.ps1` → `LOG_CHANNEL=single`; FE-53 e2e 3/3, FE-54 4/4 (doğrulama dahil) |

## 2. Eksikler (söz verilmiş ya da beklenen ama yapılmamış)

| # | Eksik | Neden önemli | Kaynak |
|---|---|---|---|
| E1 | **Mevcut hesaplar için göç yok.** `email_verified_at` boş olan her hesap (19.14'ten önce açılanların hepsi) canlıya çıkınca ödeme başlatamaz, yayınlayamaz ve ilk yayın indirimini alamaz. Doğrulama postası hiç gitmemiş; kullanıcı yalnızca banttaki "yeniden gönder" ile kurtulur | Canlıda kullanıcı varsa yayın akışı bir gecede kırılır | SEC-09 §A varsayılanı ("göç yok") |
| E2 | 19.26'dan önce açılmış boş taslaklar silinmedi; 50'lik tavana sayılıyorlar. Otomatik temizlik işi yok | Çok gezinen eski kullanıcı tavana boş "Düğün"lerle yaklaşabilir; H2 ile birlikte kafa karıştırır | FE-50 §A-2 |
| E3 | `guestUploads` alanı davetiye önbelleğinde en çok 6 saat eski kalabilir; bayrak değişince otomatik geçersiz kılma yok, `php artisan cache:clear` gerekir | Bayrak açılırsa arayüz 6 saate kadar yüklemeyi göstermez (uç hemen açılır) | FE-51 "Bilinen gecikme" |
| E4 | Bekleyen dosya sonradan iliştirilirse 1 GB bütçe en çok 200 MB aşılabilir | Kasıtlı (yetimleri bütçeye katmak DoS'u geri getirir); belgelenmiş sınır | SEC-08 |
| E5 | Shopier'e her alıcı için aynı yer tutucu TCKN/telefon/adres gidiyor; kod değişmedi (D4) | K125 ⚠️; Hat B E3 ile aynı madde | SEC-10 |
| E6 | Yerelde `public` diskte biriken medya S3'e taşınmadı | Canlıda `public`'te dosya varsa K183 sonrası okunur ama yeni yükleme S3'e gider; iki yerde medya | ARC-04 (kapsam dışı) |
| E7 | Sunucudaki gerçek `.env` anahtar listesi görülmedi; şablon yalnızca Y8.3b düzeltmeleriyle eşitlendi | Sunucuda şablonda olmayan bir anahtar varsa yeniden kurulumda kaybolur | OPS-04 §A-1 |
| E8 | M47 (`HandlePaymentCallbackAction`) ve M49 (`ClaimReleasedOrderAction`) kilit silinince iki bağlantılı bekleme testleri **yeşil kaldı**; yalnızca SQL envanter testi öldürdü (sonraki `UPDATE` de beklediği için) | Bu iki kilidin eşzamanlılık davranışını kanıtlayan test yok; yalnızca "sorguda `for update` var" kanıtı var | TST-02 mutant tablosu |
| E9 | `a_user_cannot_open_someone_elses_draft_by_url`, mevcut `owner_cannot_read_another_users_invitation`'ın taslak kopyası | Tekrar eden test (zararsız) | FE-50 plandan sapma |

## 3. Koşulmayan doğrulamalar (B7 ⏳)

| # | Doğrulanmayan | İş | Neden |
|---|---|---|---|
| D1 | `php artisan about --only=davetkart` → `Media disk: s3`, `Mail mailer: ses` | ARC-04, OPS-04 | Canlı sunucu (istek yasağı) |
| D2 | `php artisan schedule:list` → `media:prune-orphans` `15 * * * *` | SEC-08 | Canlı sunucu |
| D3 | Doğrulama postasının SES ile gerçekten gittiği; kuyruk işçisi çalışıyor (`VerifyEmailNotification` kuyrukta) | SEC-09 | Canlı sunucu |
| D4 | Tarayıcıda: doğrulama bandı, `/eposta-dogrula` sayfası, yayında `EMAIL_NOT_VERIFIED` mesajı | SEC-09 | Yalnızca `verify:*` ve e2e (log'dan bağlantı) |
| D5 | Tarayıcıda: tavan dolu hesapta sihirbaz (H2'yi gösterir), `/create/<başkasının-id>` → mesaj + panel | FE-50 | Denenmedi |
| D6 | Misafir sayfasında hiçbir şablonda dosya alanı yok | FE-51 | `verify:render` metin taraması; tarayıcıda bakılmadı |
| D7 | `npm run e2e` FE-50'nin `draftSurvivesReload` adımıyla | FE-50 | Hat A koşmadı. FE-54'ün dalı FE-50 birleşmesini içeriyor ve e2e'si 4/4 yeşil; kayıt adımı adıyla yazmıyor. SEC-11 · FE-52'den sonra yeniden koşulmadı (Hat B D9) |
| D8 | `concurrency` grubunun (`lock_timeout = 200ms`, alt süreç 800 ms) yavaş makinede / CI'da kararlılığı | TST-02 | Yalnızca bu makinede ölçüldü |
| D9 | Tam backend paketi `composer check` içinden | hepsi | H1 yüzünden PHPStan'da duruyor; adımlar elle koşuldu (bkz. §7) |

## 4. Senin elle yapman gerekenler

| # | İş | Komut / yer | Kaynak |
|---|---|---|---|
| İ1 | Shopier sorusunu göndermek; cevabı `prompts/faz-19-agent/19-15-SEC-10.md` §A-1'e yazıp 19.15'i yeniden koşmak | `notes/04-SHOPIER-ALICI-ALANLARI-SORUSU.md` | SEC-10 |
| İ2 | Sunucuda anahtar listesini şablonla karşılaştırmak | `cut -d= -f1 .env \| sort` ↔ `docs/10-URETIM-ENV-SABLONU.md` | OPS-04 |
| İ3 | Sunucuda D1 ve D2 komutları | `php artisan about --only=davetkart` · `php artisan schedule:list` | ARC-04 · OPS-04 · SEC-08 |
| İ4 | Canlıya çıkmadan E1 kararı; göç seçilirse tek seferlik komut/göç | — | SEC-09 |
| İ5 | Yerel deneme hesaplarını doğrulamak | `docs/rehber/app/Support/VerifiedEmailGuard.md` (`tinker`) | SEC-09 |
| İ6 | `DAVETKART_GUEST_UPLOADS` değişirse `php artisan cache:clear` | sunucu | FE-51 |
| İ7 | Son birleşmelerden sonra tam `npm run e2e` (D7) | frontend, Hat B ortamı | FE-50 · SEC-09 |
| İ8 | Canlıda `public` diskte medya varsa S3'e taşıma kararı | — | ARC-04 |

## 5. Bekleyen kararlar (§A boş → varsayılan, "İsmail cevaplamadı")

| # | Karar | Şu an geçerli varsayılan | Kaynak |
|---|---|---|---|
| K-1 | Üretimde yanlış medya diski | Fail-closed 503 `PROVIDER_UNAVAILABLE`; beklenen disk `s3` (K183) | ARC-04 §A-1/2 |
| K-2 | Üretimde `log` posta sürücüsü | Durdurmaz; CRITICAL log + `about` uyarısı (K185) | OPS-04 §A-2 |
| K-3 | Hız sınırı sayıları | Girişli 120/dk · misafir okuma 300/dk IP · misafir medya 60/dk IP · Nginx mikro-cache yok (K186) | SEC-06 §A |
| K-4 | Misafir yükleme özelliği | Kapalı (bayrak, 404); istenirse §A-1 "evet" → 19.12'yi D2 ile yeniden koş (K189) | FE-51 §A-1 |
| K-5 | Misafir bütçesi | 1 GB tek bütçe · yetim 1 saat · video 20 MB · bekleyen 50 dosya / 200 MB; plan bazlı değil (K190) | SEC-08 §A |
| K-6 | E-posta doğrulaması | Giriş/taslak serbest, ödeme/yayın 403; bağlantı 24 saat; saatte 3; **mevcut hesaplara göç yok** (E1) (K191) | SEC-09 §A |
| K-7 | Taslak yaşam döngüsü | Tavan 50, yayındakiler sayılmaz; boş taslak temizliği yok (E2) (K192) | FE-50 §A |
| K-8 | Shopier alıcı alanları | D4: kod değişmez, soru hazır | SEC-10 §A-1 |
| K-9 | PHPStan kırmızısı | Hat A'da "bağımsız" diye kayıtlı; ortak dalda düzeltilecek (H1) | ARC-04 İ(1) |

## 6. Temizlik ve devir

- **Birleşmiş dallar (silinebilir, 20):** backend 8 (`fix/2026-11-20-arc-04-media-disk`, `…-ops-04-env-template`, `…-sec-06-rate-limit-keys`,
  `…-tst-02-lock-tests`, `…-fe-51-guest-media-upload`, `…-sec-08-guest-upload-budget`, `…-sec-09-email-verification`, `…-fe-50-draft-lifecycle`),
  frontend 3 (`fe-51`, `sec-09`, `fe-50`), docs 9 (yukarıdakiler + `docs/2026-11-22-sec-10-shopier-buyer-fields`). Silmeden önce hiçbir worktree'nin o dalda olmadığına bak.
- **Hat A worktree'leri:** backend ve frontend bu rapor için birleşik dalların ucuna `--detach` alındı (dal açılmadı, değişiklik yok);
  docs bu raporun dalında (`docs/2026-11-25-hat-a-open-items`). Ortak dalda çalışmaya geçerken worktree'lerin dal durumu kontrol edilmeli.
- **`notes/` içinde iki `04-` önekli dosya** (`04-FAZ-5-FRONTEND-YAPILACAKLAR.md`, `04-SHOPIER-ALICI-ALANLARI-SORUSU.md`); Shopier notu `05-`'e taşınabilir (bağlantıları: SEC-10/SEC-11 kayıtları, Hat B raporu).
- **`phases/faz-19/README.md`** üç hat raporunu (`HAT-A-ACIK-KALANLAR.md`, `HAT-B-ACIK-KALANLAR.md`, `HAT-C-ACIK-HATALAR.md`) listelemiyor.
- **K aralığı:** Hat A K183–K192'yi kullandı; K193–K219 boş.

## 7. Birleşik dallarda kapılar (25 Kasım 2026)

Hat A worktree'lerinde, birleşik dalların ucunda (`--detach`), test veritabanı `hat_a`:

| Kontrol | Sonuç (görülen çıktı) |
|---|---|
| Backend `pint --test` | geçti |
| Backend `phpstan analyse` (ortak önbellek, `composer check`'teki komut) | 🔴 501 hata — sahte (H3) |
| Backend `phpstan analyse` (ayrı `tmpDir`, temiz önbellek) | 🔴 3 hata — `ResolvesRefundRequests.php:29` ×2, `ReadinessTest.php:175` (H1); başka hata yok |
| Backend `errors:export --check` · `plans:export --check` · `env:template --check` | geçti · geçti · geçti |
| Backend `php artisan test` (tam) | geçti — 1264 test, 4599 doğrulama |
| `composer audit` | geçti — açık yok |
| Frontend `npm ci` + `npm run check` | çıkış 0 — `verify:errors` 31 kod, `verify:i18n` 781 parça, `verify:bundle` 710,3 / 720 kB, `verify:state` ve `verify:render` yeşil |
| `npm run e2e` | koşulmadı (Hat B'nin portu ve veritabanı) |
