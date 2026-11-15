# Testler ve kalite kapısı — AUD-2026-11-12

> Yürüten: ana oturum (Fable 5.2) · Kopyalar: `_audit-snap\backend-tst`, `_audit-snap\frontend-tst` · Commit: backend `d810410`, frontend `44caa49` · Tarih: 13 ve 15 Kasım 2026
> Dilim ajanı (C) 13 Kasım'da kullanım sınırına takıldı. Kalite kapısı ve ilk 46 mutant 13 Kasım'da ana oturumda koştu; M23'ün yeniden koşusu, M47–M51, kapsam haritası ve bu dosya 15 Kasım'da.

## Özet

Backend test paketi güçlü: 1056 test, 3921 doğrulama, 143 saniye. Kritik iş kurallarına yazılan 47 mantık
mutantının **47'si öldü** (paywall, sipariş durum makinesi, fiyat, imza, hediye kodu, sahiplik, LCV kotası,
girdi sertleştirme, iade, hesap silme). 24 Eylül denetiminde hayatta kalan mutantların hepsi bugün ölüyor.
Testler yanıtı değil etkiyi doğruluyor (`refresh()` 129, `assertDatabase*` 132 kez), kimlik gerçek token'la
taşınıyor (`withToken` 198, `actingAs` 0), sahtesi kurulmamış HTTP çağrısı kırmızı yanıyor.

Üç boşluk var. Kalite kapısı bu dalda **kırmızı**: `composer check` ilk adımda (Pint) duruyor (`TST-01`).
Eşzamanlılığı koruyan 17 `lockForUpdate()` çağrısının hiçbiri testle korunmuyor: denenen dört kilit
mutantının dördü de tam paketi yeşil geçti (`TST-02`). Gerçek frontend ile gerçek backend'i birlikte koşturan
otomatik test yok (`TST-04`).

**Koşturulamayanlar (B7):** satır kapsamı ölçülemedi (Xdebug/PCOV kurulu değil); kapsam haritası statik bir
yaklaşımdır. GitHub Actions'ın bu dal için sonucu görülmedi (GitHub'a istek atılmadı).

Seviye sayıları: 🔴 0 · 🟠 0 · 🟡 3 · 🟢 2 · 💡 1 — Kanıt: KOŞTURULDU 5 · KOD OKUMASI 1

## Özet tablosu

| ID | Seviye | Kanıt türü | Başlık | Nerede | Efor | Tek satır öneri |
|---|---|---|---|---|---|---|
| TST-01 | 🟡 | KOŞTURULDU | `composer check` bu dalda kırmızı (Pint); CI iki adımda kırmızı olmalı | `backend:tests/Feature/TemplateCatalogueTest.php:114` | S | `vendor/bin/pint` koş, sonucu Faz 15–17 kaydına işle |
| TST-02 | 🟡 | KOŞTURULDU | Kilitlerin hiçbiri testle korunmuyor: 4 kilit mutantının 4'ü hayatta | `backend:app/Actions/**` (17 `lockForUpdate()`) | M | Kilidi SQL düzeyinde doğrulayan test + iki bağlantılı yarış testi |
| TST-03 | 🟢 | KOŞTURULDU | Satır kapsamı ölçülmüyor; eşik yok | `backend:.github/workflows/ci.yml` (`coverage: none`) | S | CI'da PCOV + `app/Actions` için alt sınır |
| TST-04 | 🟡 | KOD OKUMASI | Gerçek frontend + gerçek backend'i koşturan otomatik test yok | iki depo | L | Sahte ödeme sürücüsüyle üç yolculukluk Playwright duman testi |
| TST-05 | 🟢 | KOŞTURULDU | Frontend CI Node 22, yerel ortam Node 24; sürüm sabitlenmemiş | `frontend:.github/workflows/ci.yml` | S | `.nvmrc` + `engines`; CI aynı dosyadan okusun |
| TST-06 | 💡 | KOŞTURULDU | Paket 143 sn ve neredeyse tamamı Feature testi; mutasyon başına 2,5 dk | `backend:tests/` (50 Feature, 11 Unit dosyası) | M | `--parallel`; saf kuralları birim testine indir |

## Neler iyi

1. **Kritik kuralların mutantları ölüyor.** 47/47 mantık mutantı kırmızı yaktı; çoğunu birden fazla test
   öldürdü (`evidence/commands/TST-mutation-summary.txt`). Örnek: M01 (yayındaki davetiyede plan kontrolü
   kaldırıldı) üç ayrı `PaywallTest` testini düşürdü.
2. **Önceki denetimin boş yeşilleri kapanmış.** `SubscriptionTier::price()` → `1` (M06, 24 kırmızı), para
   birimi → `USD` (M50, 7 kırmızı), zarf modülü Gold → Standart (M51), cache anahtarından kimlik (M18), HSTS
   (M26), `getClientMimeType()` (M29): 24 Eylül'de hepsi yeşildi, bugün hepsi kırmızı.
3. **Etki doğrulanıyor (T14).** `->refresh()` 129, `assertDatabaseHas` 70, `assertDatabaseCount` 55,
   `assertDatabaseMissing` 7, `assertModelMissing` 6, depolama doğrulaması 7. Veritabanı etkisine bakmayan 13
   Feature dosyasının hepsi salt okunur uçları ya da ara katmanları sınıyor (`HardeningTest`, `PricingTest`,
   `PublicInvitationTest`…).
4. **Kimlik gerçek yoldan (T10).** `withToken(` 198 kez, `actingAs(` yalnızca iki yorum satırında.
   `forgetAuthState()` 67 kez: aynı testte ikinci kimlikli istek guard önbelleğine takılmıyor.
5. **Dış dünya kapalı.** `Http::preventStrayRequests()` `TestCase::setUp`'ta (`tests/TestCase.php:30`) ve
   bunu sınayan test var (`TestSuiteIsolationTest.php:60-66`); Sentry DSN'i testte boş ve doğrulanıyor
   (`phpunit.xml`, `TestSuiteIsolationTest::the_test_suite_has_no_sentry_dsn`).
6. **Gerçekçi veri.** 61 test dosyasının 61'i Türkçe harf içeriyor; "foo/bar" bir kez, `lorem` hiç.
   Zaman `travelTo`/`freezeTime` ile sabitleniyor (53), `sleep` yok, atlanan test yok.
7. **Her rota ve komut bir testte.** 44 API rotasının hepsi testlerde rota adıyla geçiyor; 16 konsol
   komutunun 15'i `artisan('…')` ile çağrılıyor, 16'ncısı (`errors:export`) kapının kendi adımı
   (`evidence/commands/TST-coverage-map.txt`, `TST-test-quality-metrics.txt`).
8. **PHPStan temiz, hata kataloğu güncel.** `phpstan analyse` 0 hata (79,8 sn), `errors:export --check`
   "Katalog güncel".
9. **Frontend kapısı yeşil.** `npm run check`: `tsc --noEmit` + build + 11 `verify` betiği, 39,3 sn, çıkış 0.

## Bulgular

### TST-01 `composer check` bu dalda kırmızı (Pint); CI iki adımda kırmızı olmalı
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:tests/Feature/TemplateCatalogueTest.php:114` (`private const FAZ17_PRESETS` metotlardan sonra) · `backend:.github/workflows/ci.yml` (adımlar: `composer check`, `composer audit`)
- Senaryo: 1) Faz 15–17 PHP 8.3'lü bulut ortamında yazıldı; `composer check` orada koşamadı (`docs/rehber/fazlar/FAZ-15.md` §3: "Bu dalın testi koşmadı"). 2) Faz 17, test dosyasına ikinci bir sabiti metotların arasına ekledi. 3) Pint'in `ordered_class_elements` kuralı bunu reddediyor; `composer check` ilk adımda çıkış 1 veriyor ve PHPStan ile testlere **hiç geçmiyor**.
- Kanıt: `evidence/commands/TST-composer-check.txt` → `{"tool":"pint","result":"fail","files":[{"path":"tests\\Feature\\TemplateCatalogueTest.php","fixers":["ordered_class_elements"]}]}`, çıkış 1, 47,7 sn. Adımlar tek tek: Pint ❌ (`TST-step1-pint.txt`) · PHPStan ✅ 0 hata (`TST-step2-phpstan.txt`) · `errors:export --check` ✅ (`TST-step3-errors-export.txt`) · testler: 1056 test, 1055 yeşil (`TST-step4-artisan-test.txt`).
- Sınıflandırma: Pint hatası **gerçek** (sınıf öğelerinin sırası; satır sonu ya da ortam farkı değil). Tek kırmızı test `TestSuiteIsolationTest::the_test_suite_runs_on_its_own_database` **ortam kaynaklı**: kopyada `phpunit.xml` veritabanı adı bilerek değiştirildi (`davetkart_aud_tst_test`), test `davetkart_test` bekliyor. Gerçek depoda yeşil olması beklenir (koşmadı).
- Etki: Kod davranışı doğru; bozuk olan kapının kendisi. CI her push'ta çalışıyorsa (`on: push: branches: ["**"]`) bu dal iki adımda kırmızı olmalı: Pint ve `composer audit` (`SEC-07`: 8 bilinen açık). Kırmızıya alışılmış bir kapı, gerçek bir hatayı da geçirir.
- Neden önemli (öğretici not): Kalite kapısı zincirdir; ilk halka koptuğunda sonrakiler koşmaz. "Yalnızca biçim hatası" denip geçilen kırmızı, arkasındaki 1056 testin o gün koşmadığı anlamına gelir. Kapının değeri yeşilken değil, kırmızıyken ne yapıldığıyla ölçülür.
- Öneri: `vendor/bin/pint tests/Feature/TemplateCatalogueTest.php` (sabiti yukarı taşır) → `composer check` → sonucu `FAZ-15.md` §3'e ve yazılacak `FAZ-16.md`/`FAZ-17.md`'ye işle. Bulut ortamı PHP 8.5 kuramıyorsa faz kapanış kanıtı olarak GitHub Actions koşusunun bağlantısını kullan.
- Test önerisi: Yok (kapının kendisi).
- Efor: S
- İlgili: `ARC-02` · `SEC-07` · T16 · B7

### TST-02 Kilitlerin hiçbiri testle korunmuyor: 4 kilit mutantının 4'ü hayatta
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:app/Actions/GiftCode/ReserveGiftCodeAction.php:45` (M14) · `app/Actions/Payment/HandlePaymentCallbackAction.php:59` (M47) · `app/Actions/Rsvp/EnsureRsvpQuotaAction.php:54` (M48) · `app/Actions/Payment/ClaimReleasedOrderAction.php:71` (M49) · toplam 17 `lockForUpdate()` çağrısı, 14 dosyada
- Senaryo: 1) Bir yeniden düzenlemede `->lockForUpdate()` satırı düşer (ör. sorgu `firstOrFail()`'e sadeleştirilir). 2) `composer check` yeşil kalır: 1052 testin hiçbiri iki isteği aynı anda koşturmuyor. 3) Üretimde: aynı tek kullanımlık hediye kodu iki siparişe yazılır (M14); aynı ödeme bildirimi iki kez işlenir (M47); 100 kişilik LCV kotası son iki yanıtla 101'e çıkar (M48); serbest kalan bir hak iki davetiyeye birden bağlanır (M49).
- Kanıt: `evidence/mutation/M14.txt`, `M47.txt`, `M48.txt`, `M49.txt`: her birinde kilit silindi, hedefli testler yeşil, **tam paket 1052 test 0 kırmızı**, sonuç `HAYATTA`, dosya `GERİ ALINDI`. `TST-test-quality-metrics.txt` §4: `pcntl_fork|Process::|DB::connection(` → 0.
- Etki: Bugün kilitler yerinde ve güvenlik denetimi onları okudu (`02-security.md`, "Neler iyi"). Risk gelecekte: para ve kota değişmezlerini koruyan satırların silinmesini hiçbir şey fark etmez.
- Neden önemli (öğretici not): Tek süreçli test paketi **sıralı** doğruluğu kanıtlar; yarış durumu ise iki işlemin araya girmesiyle ortaya çıkar. Kilit, sıralı koşuda görünmez bir satırdır: silinince hiçbir test bozulmaz çünkü hiçbir test onun engellediği durumu üretmez. Bu, "testler yeşil = kod doğru" eşitliğinin en bilinen istisnasıdır.
- Öneri: İki katman. Ucuz ve kesin: Action testinde `DB::listen` ile koşan SQL'i yakala, `for update` içerdiğini doğrula (dört mutantı da öldürür, 5 satır). Sağlam: iki PostgreSQL bağlantısıyla gerçek yarış testi: A bağlantısı transaction açıp satırı kilitler, B bağlantısı `SET LOCAL lock_timeout = '200ms'` ile aynı Action'ı çağırır ve `QueryException` (55P03) bekler.
- Test önerisi: `ReserveGiftCodeActionTest::the_code_row_is_locked_while_it_is_reserved` (öldürmesi gereken: M14) · `HandlePaymentCallbackActionTest::the_order_row_is_locked` (M47) · `EnsureRsvpQuotaActionTest::the_invitation_row_is_locked` (M48) · `ClaimReleasedOrderActionTest::the_released_order_is_locked` (M49).
- Efor: M
- İlgili: K111 · backend `CLAUDE.md` §3 ("İki katman, iki farklı yarış") · `SEC-01` (aynı ailenin kilitle çözülmeyen üyesi)

### TST-03 Satır kapsamı ölçülmüyor; eşik yok
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:.github/workflows/ci.yml` (`coverage: none`) · yerel PHP (Herd): `php -m` çıktısında `xdebug`/`pcov` yok
- Senaryo: Yeni bir Action eklenir, testi yazılmaz; kapı bunu göremez çünkü "hangi satır hiç koşmadı" bilgisi hiçbir yerde üretilmiyor.
- Kanıt: `php -m | Select-String 'xdebug|pcov'` → boş. Yerine statik harita: `evidence/commands/TST-coverage-map.txt` (rota adı ve sınıf adı eşleşmesi). Harita 59 Action dosyasının 44'ünün adının testlerde geçmediğini gösteriyor; bunların hepsi bir Controller ya da başka bir Action üzerinden dolaylı çağrılıyor ve mutasyon örneklemi (ör. M12, M30, M38) bu dolaylı kapsamın gerçek olduğunu doğruluyor.
- Etki: Bugünkü kapsam iyi görünüyor ama bir sayı yok; gerilemesi fark edilmez.
- Neden önemli (öğretici not): Kapsam "testler iyi" demez (mutasyon onu söyler), ama "burası hiç koşmadı"yı kesin söyler. İkisi birbirinin eksiğini kapatır: kapsam nereye bakılacağını, mutasyon bakılan yerin sağlamlığını gösterir.
- Öneri: CI'da `coverage: pcov` + `php artisan test --coverage --min=85` (önce ölç, eşiği ölçülen değerin birkaç puan altına koy). Mutasyon için bu denetimin koşucusu (`evidence/scripts/tst-mutation-runner.php`) elle koşulan bir araç olarak depoya alınabilir.
- Test önerisi: —
- Efor: S
- İlgili: `TEST-DENETIMI-2026-09-24.md` §4

### TST-04 Gerçek frontend + gerçek backend'i koşturan otomatik test yok
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `frontend:package.json` (test koşucusu yok: Vitest, Jest, Playwright, Cypress bağımlılığı yok) · `frontend:scripts/verify-*.ts` (taşıma katmanı sahte) · `backend:docs/rehber/fazlar/FAZ-*-ELLE-DOGRULAMA.md` (12 dosya)
- Senaryo: 1) Backend bir Resource alanının adını değiştirir; backend testleri yeni adla güncellenir, yeşil. 2) Frontend `verify:endpoints` kendi beklediği gövdeyle sınar, yeşil. 3) İki yeşil kapıdan geçen sürümde arayüz boş alan gösterir. Bugün bu boşluğu elle doğrulama listeleri kapatıyor.
- Kanıt: `package.json` bağımlılık listesi (`FE-d1-metrics.txt` §0); `scripts/verify-endpoints.ts:44-56` (`mockAdapter`: istek ağa çıkmadan yakalanıyor).
- Etki: Sözleşme kayması ancak elle denemede ya da üretimde görülür. Kayıt → davetiye → ödeme → yayın → LCV zinciri, ürünün para kazandığı tek yol ve hiçbir otomatik test onu baştan sona koşturmuyor.
- Neden önemli (öğretici not): Test piramidinin tepesi dar olmalı ama **boş olmamalı**. İki ayrı deponun her biri kendi içinde tutarlı olabilir; sözleşme testleri iki tarafın aynı belgeyi okuduğunu kanıtlar, aynı şeyi anladığını değil. Birkaç uçtan uca test bu son boşluğu kapatır.
- Öneri: Sahte ödeme sürücüsüyle (`PAYMENT_PROVIDER=fake`) üç Playwright yolculuğu: (1) kayıt → davetiye → hediye koduyla yayın, (2) misafir LCV'si → sahibin panelinde görünmesi, (3) yayındaki davetiyede üst plan modülü → plan duvarı (K-1). Bu denetimin D2 dilimi aynı yolculukları elle koşturdu (`04-frontend-e2e.md`); adımlar oradan alınabilir.
- Test önerisi: `e2e/publish-with-gift-code.spec.ts`, `e2e/guest-rsvp.spec.ts`, `e2e/paywall-after-publish.spec.ts`. Öldürmesi gereken mutant: `OrderResource`'ta `orderId` anahtarını `id` yapmak (bugün iki kapı da yeşil kalır).
- Efor: L
- İlgili: `FAZ-*-ELLE-DOGRULAMA.md`

### TST-05 Frontend CI Node 22, yerel ortam Node 24; sürüm sabitlenmemiş
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:.github/workflows/ci.yml` (`node-version: "22"`) · denetim ortamı Node 24.18.0 (`README.md` → Ortam)
- Senaryo: Yerelde Node 24 ile yeşil olan `npm run check`, CI'da Node 22 ile koşar (ya da tersi); `verify` betikleri `tsx` ile Node üzerinde çalıştığı için çalışma zamanı farkı sonucu değiştirebilir.
- Kanıt: CI dosyası okundu; `npm run check` Node 24'te yeşil (`TST-npm-run-check.txt`). Node 22'de koşmadı.
- Etki: Küçük. "Bende çalışıyor" türü farkların kaynağı.
- Neden önemli (öğretici not): Kapının koştuğu ortam, kodun koşacağı ortamla aynı olmalı; fark her zaman en kötü anda görünür.
- Öneri: `.nvmrc` (ya da `package.json` `engines.node`) + CI'da `node-version-file: .nvmrc`. Üretimde Node yalnızca build için gerekli; sunucudaki sürüm de aynı dosyadan okunmalı.
- Test önerisi: —
- Efor: S
- İlgili: plan kaydı Y6.5c (sunucuda Node 24)

### TST-06 Paket 143 sn ve neredeyse tamamı Feature testi; mutasyon başına 2,5 dk
- Seviye: 💡 Öneri
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:tests/Feature/` (50 dosya, 707 metot) · `backend:tests/Unit/` (11 dosya, 46 metot)
- Senaryo: Hayatta kalan her mutant tam paketle doğrulanmak zorunda (144–173 sn). 17 kilidin hepsini denemek 45 dakika sürer; düzenli mutasyon testi bu hızda yapılmaz.
- Kanıt: `TST-step4-artisan-test.txt` (`"duration_ms":143103`), `TST-mutation-summary.txt` (tam paket koşuları 144–173 sn), `TST-test-quality-metrics.txt` §6.
- Etki: Geri bildirim döngüsü uzuyor. Feature ağırlığı bir API için doğru tercih (sözleşmeyi sınar); sorun süre.
- Neden önemli (öğretici not): Test hızının değeri doğrusal değildir: 15 saniyelik paket her kayıtta koşulur, 150 saniyelik paket "sonra" koşulur.
- Öneri: `php artisan test --parallel` (PostgreSQL'de süreç başına veritabanı; `TestSuiteIsolationTest` veritabanı adı önekine göre güncellenmeli). Saf kurallar (`RefundEligibility`, `OrderStatus`, `TierResolver`, `QuotePriceAction`) zaten birim teste uygun; yeni kural önce orada sınanabilir.
- Test önerisi: —
- Efor: M
- İlgili: —

## Tablolar

### Kalite kapısı

| Adım | Komut | Sonuç | Süre | Kanıt |
|---|---|---|---|---|
| Backend kapısı (bütün) | `composer check` | ❌ çıkış 1 (Pint'te durdu) | 47,7 sn | `TST-composer-check.txt` |
| 1. Biçim | `vendor/bin/pint --test` | ❌ 1 dosya, `ordered_class_elements` (gerçek) | 1,2 sn | `TST-step1-pint.txt` |
| 2. Statik analiz | `phpstan analyse --memory-limit=1G` | ✅ 0 hata | 79,8 sn | `TST-step2-phpstan.txt` |
| 3. Hata kataloğu | `artisan errors:export --check` | ✅ güncel | 1,7 sn | `TST-step3-errors-export.txt` |
| 4. Testler | `artisan test` | 1056 test · 1055 ✅ · 1 ❌ (ortam: kopyanın veritabanı adı) · 3921 doğrulama | 144,7 sn | `TST-step4-artisan-test.txt` |
| Frontend kapısı | `npm run check` | ✅ çıkış 0 (`tsc` + build + 11 `verify`) | 39,3 sn | `TST-npm-run-check.txt` |

### Frontend build çıktısı (`vite build`, 11,8 sn, 3090 modül, 204 dosya, `dist/` 104 MB)

| # | Parça | Boyut | gzip |
|---|---|---|---|
| 1 | `index-DfFic9Bg.js` (**ana giriş**; her sayfada yüklenir) | 1 637,83 kB | 442,06 kB |
| 2 | `index-B4g3laWs.css` (tek stil dosyası; her sayfada) | 1 171,53 kB | 132,84 kB |
| 3 | `SceneCanvas-*.js` (three.js; dört 3B şablon) | 886,61 kB | 239,71 kB |
| 4 | `CreatePage-*.js` | 78,83 kB | 23,19 kB |
| 5 | `CarsiPlani-*.js` | 50,58 kB | 16,64 kB |
| 6 | `CheckoutPage-*.js` | 42,81 kB | 11,71 kB |
| 7 | `index-E2pJEatt.js` | 24,94 kB | 8,95 kB |
| 8 | `DashboardPage-*.js` | 17,95 kB | 5,70 kB |
| 9 | `index-Dvo3SYJG.js` | 17,39 kB | 6,85 kB |
| 10 | `index-NnhJYHNY.js` | 17,27 kB | 6,75 kB |

169 JavaScript parçası, toplam 3,6 MB. `dist/`'in 90 MB'ı `public/videos` (`FE-09`). Vite uyarısı: "Some
chunks are larger than 500 kB"; ana giriş paketinin neden bu kadar büyük olduğu `FE-10`'da. (İlk sıralama
betiği Vite'ın `1,637.83 kB` yazımındaki binlik ayırıcıya takılıp ilk iki satırı atlamıştı; tablo ayırıcı
temizlenerek yeniden üretildi.)

### Test piramidi

| Katman | Dosya | Test metodu | Not |
|---|---|---|---|
| Birim (`tests/Unit`) | 11 | 46 | Saf sınıflar: `EmailNormalizer`, `IpBucket`, `Iban`, `OrderStatus`… |
| Özellik (`tests/Feature`) | 50 | 707 | HTTP üzerinden; veri sağlayıcılarla 1056 vakaya açılıyor |
| Uçtan uca (tarayıcı) | 0 | 0 | `TST-04` |
| Frontend `verify` betikleri | 11 | (betik başına onlarca `✓`) | Sözleşme ve saf mantık; tarayıcı yok |

Üretim kodu 235 dosya / 17 893 satır; test kodu 62 dosya / 17 054 satır.

### Statik kapsam haritası (özet; ayrıntı `TST-coverage-map.txt`)

| Grup | Dosya | Testlerde adı geçen | Geçmeyen | Yorum |
|---|---|---|---|---|
| API rotaları | 44 | 44 (rota adıyla) | 0 | En az referans: `auth.forgot-password`, `auth.reset-password`, `sessions.destroy-others`, medya uçları, `shopier.osb` (birer dosyada) |
| `app/Actions` | 59 | 15 | 44 | Hepsi Controller ya da başka Action üzerinden dolaylı; `(çağıran yok!)` satırı yok |
| Konsol komutları | 16 imza | 15 (`artisan('…')`) | 1 | `errors:export` kapının adımı |
| `app/Policies` | 3 | 0 | 3 | Dolaylı; M15 ve M16 (sahiplik mutantları) öldü |
| `app/Services` | 22 | 14 | 8 | Dolaylı; `ShopierCallback`/`ShopierConfirmation` `ShopierGatewayTest` üzerinden |
| `app/Http/Middleware` | 4 | 2 | 2 | `SecurityHeaders` M26 ile, `SetEtag` dolaylı |

### Mutasyon tablosu (51 mutant · 47 öldü · 4 hayatta · 0 atlandı)

Her satır: üretim kodunda tek değişiklik → hedefli testler → (yeşilse) tam paket → geri alma + sha256
karşılaştırması. Koşan test sayısı 0 olan sonuç yok. Öldüren testlerin adları ve çıktı sonları:
`evidence/mutation/M<NN>.txt`; tek satırlık özet: `evidence/commands/TST-mutation-summary.txt`.

| ID | Kural | Dosya:satır | Koşan test | Sonuç |
|---|---|---|---|---|
| M01 | K-1: yayındaki davetiyede plan kontrolü | `UpdateInvitationAction.php:62` | 159 | ✅ öldü |
| M02 | K-1: sahip olunan plan yükseltileni kapsamalı | `UpdateInvitationAction.php:107` | 84 | ✅ öldü |
| M03 | Yayın: plan yetmezse 402 | `PublishInvitationAction.php:106` | 84 | ✅ öldü |
| M04 | K-4/K89: `expired → paid` geçişi | `OrderStatus.php:118` | 118 | ✅ öldü |
| M05 | `paid` yalnızca `refunded` olabilir | `OrderStatus.php:119` | 89 | ✅ öldü |
| M06 | Fiyat config'ten (`price()` → 1) | `SubscriptionTier.php:29` | 120 | ✅ öldü (24 kırmızı) |
| M07 | K126: bildirim tutarı siparişle eşleşmeli | `HandlePaymentCallbackAction.php:176` | 15 | ✅ öldü |
| M08 | K126: bildirim para birimi eşleşmeli | `HandlePaymentCallbackAction.php:177` | 15 | ✅ öldü |
| M09 | Sahte ağ geçidi imzası | `FakeGateway.php:139` | 84 | ✅ öldü |
| M10 | Shopier OSB imzası | `ShopierSignature.php:79` | 39 | ✅ öldü |
| M11 | Shopier callback imzası | `ShopierSignature.php:61` | 42 | ✅ öldü |
| M12 | K111: kişi başı tek kullanım | `QuoteGiftCodeAction.php:45` | 133 | ✅ öldü |
| M13 | K110: kullanım tavanı | `QuoteGiftCodeAction.php:55` | 133 | ✅ öldü |
| M14 | K111: kod satırı kilidi | `ReserveGiftCodeAction.php:45` | 1052 (tam) | ❌ **hayatta** |
| M15 | Sahiplik: davetiye | `InvitationPolicy.php:74` | 294 | ✅ öldü |
| M16 | Sahiplik: sipariş | `OrderPolicy.php:40` | 28 | ✅ öldü |
| M17 | LCV kotası `SUM(guest_count)` | `EnsureRsvpQuotaAction.php:59` | 98 | ✅ öldü |
| M18 | Misafir cache anahtarında kimlik | `Invitation.php:106` | 37 | ✅ öldü |
| M19 | K90: token ömrü 30 gün | `config/sanctum.php:66` | 31 | ✅ öldü |
| M20 | K91: NUL baytı → 400 | `RejectMalformedInput.php:36` | 106 | ✅ öldü |
| M21 | K91: yarım JSON → 400 | `RejectMalformedInput.php:52` | 106 | ✅ öldü |
| M22 | K92: `giftOptions` `integer:strict` | `InvitationRequest.php:111` | 75 | ✅ öldü |
| M23 | K92: `guestCount` `integer:strict` | `RsvpRequest.php:69` | 87 | ✅ öldü (ilk koşuda arama metni iki kez geçtiği için atlandı; 15 Kasım'da yeniden koştu) |
| M24 | K-8: `mapUrl` yalnızca http/https | `InvitationRequest.php:84` | 75 | ✅ öldü |
| M25 | K93: `Retry-After` başlığı | `ApiExceptionRenderer.php:96` | 48 | ✅ öldü |
| M26 | HSTS yalnızca HTTPS'te | `SecurityHeaders.php:72` | 9 | ✅ öldü |
| M27 | K-3: Türkçe `İ` normalizasyonu | `EmailNormalizer.php:46` | 58 | ✅ öldü |
| M28 | K36: giriş hız sınırı 5/dk | `AppServiceProvider.php:386` | 47 | ✅ öldü |
| M29 | MIME içerikten | `StoreUploadedMediaAction.php:53` | 48 | ✅ öldü |
| M30 | K139: kullanımdaki hak iade edilemez | `RefundEligibility.php:38` | 31 | ✅ öldü |
| M31 | K139: iade penceresi 14 gün | `RefundEligibility.php:40` | 31 | ✅ öldü |
| M32 | K144: e-posta bağlantısı tek kullanımlık | `ConfirmEmailChangeAction.php:50` | 10 | ✅ öldü |
| M33 | K97: hesap silinince token'lar silinir | `DeleteAccountAction.php:68` | 7 | ✅ öldü |
| M34 | K98: çöp kutusu 30 gün | `PurgeExpiredData.php:67` | 29 | ✅ öldü |
| M35 | Faz 17: şablon Gold | `config/davetkart.php:99` | 182 | ✅ öldü |
| M36 | K131: ilk yayın yalnızca hiç ödeme yokken | `QuotePriceAction.php:103` | 36 | ✅ öldü |
| M37 | K134: kapalı ödeme yöntemi reddedilir | `PaymentMethods.php:66` | 19 | ✅ öldü |
| M38 | K82: 3 günlük serbest bırakma penceresi | `DeleteInvitationAction.php:100` | 193 | ✅ öldü |
| M39 | Misafir ucu yalnızca yayınlanmışı gösterir | `ResolvePublicInvitationAction.php:31` | 124 | ✅ öldü |
| M40 | K101: LCV düzenleme kodu | `UpdateRsvpAction.php:58` | 11 | ✅ öldü |
| M41 | Checkout: plan davetiyeyi kapsamalı | `StartCheckoutAction.php:96` | 94 | ✅ öldü |
| M42 | Hesap silme mevcut parolayı ister | `DeleteAccountRequest.php:36` | 7 | ✅ öldü |
| M43 | R7: 4xx Sentry'ye gitmez | `bootstrap/app.php:57` | 5 | ✅ öldü |
| M44 | K102: imza yalnızca Elit'te kalkar | `ResolveBrandingAction.php:43` | 159 | ✅ öldü |
| M45 | K137: yanmış hak yeniden kullanılamaz | `ClaimReleasedOrderAction.php:67` | 89 | ✅ öldü |
| M46 | K138: iade talebi açık hak donuk | `ClaimReleasedOrderAction.php:68` | 98 | ✅ öldü |
| M47 | Kilit: ödeme bildirimi sipariş satırı | `HandlePaymentCallbackAction.php:59` | 1052 (tam) | ❌ **hayatta** |
| M48 | Kilit: LCV kotası davetiye satırı | `EnsureRsvpQuotaAction.php:54` | 1052 (tam) | ❌ **hayatta** |
| M49 | Kilit: serbest hakkın sahiplenilmesi | `ClaimReleasedOrderAction.php:71` | 1052 (tam) | ❌ **hayatta** |
| M50 | R12: para birimi `TRY` → `USD` | `config/davetkart.php:21` | 107 | ✅ öldü (7 kırmızı) |
| M51 | R12: zarf modülü Gold → Standart | `config/davetkart.php:54` | 84 | ✅ öldü |

Her koşudan sonra `diff -rq backend backend-tst` (hariç: `vendor`, `storage`, `cache`, `.env`,
`.phpunit.cache`) yalnızca beklenen `phpunit.xml` farkını verdi; son denetim 15 Kasım, M51'den sonra.

## Regresyon

| # | Kaynak | Bulgu | Durum | Kanıt türü | Kanıt |
|---|---|---|---|---|---|
| R1 (mutasyon) | Review §1.1 / K-1 | Yayından sonra `PUT` ile üst plan modülü | ✅ kapandı | KOŞTURULDU | M01, M02 öldü (`PaywallTest::a_published_invitation_cannot_enable_a_module_above_its_tier` ve iki test daha) |
| R2 (mutasyon) | Review §1.2 / K-4 | Geç gelen `paid` bildirimi | ✅ kapandı | KOŞTURULDU | M04 öldü (`PaywallTest::a_paid_webhook_after_expiry_still_grants_the_order`, `OrderStatusTest` üç test) |
| R10 | Review §6.3–6.4 | `preventStrayRequests`, `SENTRY_LARAVEL_DSN` testte | ✅ kapandı | KOŞTURULDU | `tests/TestCase.php:30`; `phpunit.xml` `<server name="SENTRY_LARAVEL_DSN" value=""/>`; `TestSuiteIsolationTest` dört testinden üçü yeşil (dördüncüsü kopyanın veritabanı adı, ortam) |
| R11 | Test denetimi K-2…K-8 | NUL, `İ`, `Retry-After`, yarım JSON, `integer:strict`, `mapUrl` | ✅ kapandı | KOŞTURULDU | K-2: M20 · K-3: M27 · K-5: M25 · K-6: M21 · K-7: M22, M23 · K-8: M24, hepsi öldü |
| R12 | Test denetimi §2 | Hayatta kalan mutantlar | ✅ kapandı | KOŞTURULDU | `InvitationTest`: M15, M22, M24 · `PublicInvitationTest` cache anahtarı: M18 · `PaywallTest` fiyat: M06, para birimi: M50, zarf: M51 · `AuthTest`: M19, M27, M28 · `HardeningTest` HSTS: M26 · `MediaTest` MIME: M29. Denenmeyenler: `InvitationTest` istek eşlemesi (13 alan), `AssistantTest` `retryAfter`, `ContactTest` saatlik kova |

## Kullanılan araçlar ve skill'ler / kullanılamayanlar

- Kullanılan: `composer check` ve adımları, `npm run check`, bu denetim için yazılan mutasyon koşucusu
  (`evidence/scripts/tst-mutation-runner.php`), statik kapsam haritası (`tst-coverage-map.php`), `grep` sayımları.
- Skill: `superpowers:executing-plans`. `superpowers:verification-before-completion` adımı: her `KOŞTURULDU`
  satırının kanıt dosyası açılıp iddiayla karşılaştırıldı.
- Kullanılamayan: Xdebug/PCOV (kurulu değil → satır kapsamı yok). Infection (kurulu değil; kopyaya paket
  eklemek `composer.lock`'u değiştirirdi, elle koşucu tercih edildi). GitHub Actions sonuçları (istek atılmadı).

## Koşturulan komutlar

| Kanıt | Komut |
|---|---|
| `evidence/commands/TST-composer-check.txt` | `composer check` (`backend-tst`) |
| `evidence/commands/TST-step1-pint.txt` … `TST-step4-artisan-test.txt` | kapının dört adımı tek tek (`evidence/scripts/TST-run-step.ps1`) |
| `evidence/commands/TST-npm-run-check.txt` | `npm run check` (`frontend-tst`) |
| `evidence/commands/TST-mutation-summary.txt` + `evidence/mutation/M01…M51.txt` | `php evidence/scripts/tst-mutation-runner.php` (13 Kasım: hepsi; 15 Kasım: `M23`, `M47 M48 M49`, `M50 M51`) |
| `evidence/commands/TST-coverage-map.txt` | `php evidence/scripts/tst-coverage-map.php` |
| `evidence/commands/TST-test-quality-metrics.txt` | `bash` içinde `grep` sayımları (komutlar dosyanın bölüm başlıklarında) |
| (dosyasız) kopya temizliği | `diff -rq backend backend-tst -x vendor -x storage -x cache -x .env -x .phpunit.cache -x node_modules` → yalnızca `phpunit.xml` |

## İsmail'e sorular

1. **CI durumu:** GitHub Actions `origin/ccr-9a346997-bu6gve` için gerçekten kırmızı mı? Kırmızıysa bildirimi
   gören oldu mu; yeşilse Pint adımı orada neden geçiyor? (Denetim GitHub'a istek atmadı.)
2. **Kapsam eşiği (`TST-03`):** CI'a PCOV eklemek süreyi uzatır (tahminen 1,5–2 kat). Kabul edilebilir mi?
3. **Mutasyon koşucusu:** `tst-mutation-runner.php` backend deposuna (`scripts/` ya da `tests/mutation/`)
   alınsın mı? 47 mantık mutantı bugün ölüyor; faz kapanışında yeniden koşmak 12 dakika sürüyor.
