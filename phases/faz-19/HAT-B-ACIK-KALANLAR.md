# Faz 19 — Hat B: açık kalanlar, bilinen hatalar, yapılmayanlar

> **Güncelleme:** 25 Kasım 2026 (ilk sürüm 24 Kasım) · **Kapsam:** Hat B'nin 10 işi (19.17, 19.18, 19.19, 19.20, 19.21, 19.22, 19.23, 19.24, 19.25, 19.27) · **Kararlar:** K224–K232
> **Amaç:** sonraki adımda bütün hatlar `faz-19-audit-fixes` (backend, frontend) ve `docs/2026-11-20-faz-19-audit-fixes` (docs) üzerinde birlikte düzeltecek. Her satırın kimliği (`B-…`) hatlar arası atıf için sabit.
> **Kaynak:** 10 kaydın "Plandan sapma", "B7", "Gördüm, dokunmadım", "İsmail'e kalan" bölümleri + 25 Kasım'da entegrasyon başında yeniden koşulan kapılar (§7).
> **Durum:** Hat B'nin 10 işi birleşmiş; birleşmemiş Hat B dalı yok.
> **25 Kasım 2026 (ortak düzeltme):** §1'in 7 hatasının hepsi `faz-19-fix`'te kapandı (B-H1–B-H7); B-D9 ve B-D15 koşuldu. Ayrıntı §8.

## 0. Özet

| Bölüm | Adet | En önemlisi |
|---|---|---|
| 1. Bilinen hatalar | 7 (✅ 7 kapandı) | `composer check` phpstan'da kırmızı (9 gerçek hata; 3'ü eski, 6'sı 19.28'den); misafir LCV formunda yazılan ad silinebiliyor |
| 2. Eksikler | 10 | Yedekten geri yüklemede silinmiş veri geri dönebilir; bundle payı 10 kB'a indi |
| 3. Koşulmayan doğrulamalar | 15 | Nginx (FE-04, SEC-12) hiç koşulmadı; son birleşmelerden sonra e2e koşulmadı |
| 4. Elle yapman gerekenler | 13 | Herd duman testleri, AWS paneli, hukukçu okuması |
| 5. Bekleyen kararlar | 6 | §A'sı boş geçilen işlerde varsayılanların onayı |
| 6. Temizlik ve devir | 4 | Ortak dosyalar K224–K232 ile güncellenmedi |
| 7. Entegrasyon kapıları (25 Kas) | 7 | Frontend ve backend testleri yeşil (1271/1271); yalnızca phpstan kırmızı |

**Ortak adımda önerilen sıra:** B-H1 (kapıyı yeşile çevir) → B-H2 (misafir veri kaybı) → B-H3, B-H5 (küçük, erişilebilirlik/yasal) → B-E6 (bundle payı) → gerisi.

## 1. Bilinen hatalar (bugün kırmızı ya da yanlış çalışan)

| # | Hata | Nerede | Kaynak | Hat B'nin mi? | Önerilen düzeltme |
|---|---|---|---|---|---|
| ✅ B-H1 | `composer check` phpstan adımında kırmızı; testler `composer check` içinden hiç koşmuyor. **9 gerçek hata** (tek süreçte, §7): `ResolvesRefundRequests.php:29` `cast.string` ×2 · `ReadinessTest.php:175` `argument.type` (Mockery) · `CheckK18.php:29` `cast.string`, `:38` `argument.type` · `K18Inspector.php:83` `return.type` · `K18CheckTest.php:84, 90, 99` `method.nonObject` | backend | TST-04, SEC-12, FE-04 kayıtları; §7 | Hayır: 3'ü Faz 14.6'dan, 6'sı 19.28 (`k18:check`, K259). Hat B dosyaları temiz | `option()`/`argument()` dönüşünü `is_string` ile daralt (cast yerine); `ReadinessTest`'te `Mockery::mock(Job::class)`; `K18Inspector` dönüşünü `list<array{int,int}>` olarak kur (`array_values`); testte `$this->artisan(...)` sonucunu `PendingCommand` olarak al. Kabul: `composer check` exit 0 |
| ✅ B-H2 | Misafir LCV formu zarf açıldıktan sonra bir kez yeniden çiziliyor; o arada yazılan ad siliniyor (`guestName` yerel `useState`). e2e'de `toPass` döngüsüyle aşıldı, kök neden düzeltilmedi | frontend `src/components/templates/shared/RSVPForm.tsx:38` | TST-04 | Hayır (Hat B görüp bıraktı) | Önce neden: üst bileşende `key` değişimi mi, koşullu yeniden bağlama mı (zarf → içerik geçişi)? Durumu bileşenin dışına (misafir store'u) ya da sabit `key`'e taşı. Kabul: `guest-rsvp.spec.ts`'teki `toPass` döngüsü kaldırılınca e2e yeşil |
| ✅ B-H3 | Ödeme penceresinde (`PaywallModal`) `role="dialog"` / `aria-modal` yok; ekran okuyucu kipin değiştiğini bilmez | frontend `src/components/payment/PaywallModal.tsx` | TST-04 · 25 Kas'ta yeniden görüldü | Hayır | `role="dialog" aria-modal="true" aria-labelledby` + odak tuzağı + Esc. Kabul: `e2e/a11y.spec.ts`'e pencere açık hâli eklenir |
| ✅ B-H4 | `heading-order` ihlali 12 sayfada (axe best-practice; WCAG AA kapısında değil) | frontend, birden çok sayfa | FE-54 | Kapsam dışı bırakıldı | Başlık düzeyleri sırayla; sonra `a11y.spec.ts`'e `heading-order` kuralı eklenir |
| ✅ B-H5 | Çerez Politikası'nın yerel depolama listesinde LCV düzenleme kodu (`davetkart_rsvp_receipt:*`) yok | frontend `src/pages/legal/CookiesPage.tsx` | SEC-11 · 25 Kas'ta yeniden görüldü | Hayır | Listeye satır: ad, amaç (misafirin yanıtını düzenleyebilmesi), süre. `verify-render`'a ad denetimi |
| ✅ B-H6 | 9 kılavuz hâlâ Google Fonts sorgusunu anlatıyor (bilgi yanlış; kod doğru, `src`'de Google isteği yok) | frontend `docs/rehber/` (`index.md`, `oniki-etkilesimli-sablon.md`, `premium-videolu.md`, `tasarim/*-KONSEPTI.md` …) | SEC-12 | **Evet** | Her birine tek satır not ("SEC-12 / K226: fontlar `/fonts/`'tan") ya da ilgili paragrafı güncelle |
| ✅ B-H7 | PHPStan **paralel** koşusu 512 sahte hata veriyor (belgelenmiş tipler "yok" sayılıyor); tek süreçte 9. Hat A da gördü: sonuç önbelleği hatlar (worktree'ler) arasında ortak | backend, ortam | §7 · Hat A raporu §1 | Hayır (ortam) | `phpstan.neon`'a worktree'ye özgü `tmpDir` (ör. `storage/phpstan`) + `.gitignore`. Kabul: iki worktree'de art arda paralel koşu aynı sayıyı verir |

## 2. Eksikler (söz verilmiş ya da beklenen ama yapılmamış)

| # | Eksik | Neden önemli | Kaynak | Önerilen düzeltme |
|---|---|---|---|---|
| B-E1 | Yedekten geri yükleme kitabında "silinmiş veriyi yeniden sil" adımı yok; döküm geri yüklenirse son 40 günde silinen hesap/misafir verisi canlıya dönebilir | Gizlilik metni (K231) yedeklerden silinmeyi söylüyor | SEC-11 | **Karar gerekli** (§5 K-7): silme günlüğü (yalnızca kimlik + tarih) tutulup geri yüklemeden sonra yeniden uygulanır mı? Sonra `YEDEK-VE-GERI-YUKLEME.md` §7'ye adım |
| B-E2 | 10 yıl dolunca `orders` satırlarını silen iş yok; metin "10 yıl" diyor | Söz verilmiş saklama süresi | SEC-11 | `data:purge`'a `orders` (`created_at` + 10 yıl) kolu + test. Acil değil, ama söz yazılı |
| B-E3 | Shopier'e her alıcı için aynı yer tutucu TCKN/telefon/adres gidiyor; Shopier'in cevabı bekleniyor | Gizlilik metni bugünkü alanları yazıyor; cevap gelince o da değişir | SEC-10 (Hat A) → SEC-11 | Cevap gelince 19.15 + `PrivacyPage` `veri-isleyenler` Shopier satırı |
| B-E4 | Davetiyeye özel kapak alanı yok; paylaşım önizlemesinde şablon kapağı kullanılamıyor (frontend derlemesinde adı hash'li) | Galerisi olmayan davetiye WhatsApp'ta genel poster gösterir | FE-04 | Kapakları `public/covers/<preset>.jpg` sabit adla da yayımla; backend `share_preview` `preset → yol` eşlemesi. Ya da ürün kararıyla bırak |
| B-E5 | Misafir sayfası şablon kataloğunu hâlâ indiriyor (~104 kB); `motion` ilk yüklemede (144 kB) | Mobil ilk yükleme ve LCP | FE-10 · FE-53 | `InvitePage`'in `resolvePresetId`'si ve `TemplateRenderer` renk haritası katalogsuz bir modüle; ilk sayfada `motion` yerine CSS geçişi |
| B-E6 | Bundle payı daraldı: ilk yükleme **710,3 / 720 kB**, misafir sayfası **883,5 / 900 kB** (25 Kas) | Bir sonraki özellik kapıyı kırmızıya çevirir | FE-10 · FE-53 · §7 | B-E5; sonra bütçe kararı (§5 K-4) |
| B-E7 | Form hata mesajlarının `aria-describedby` bağı axe ile taranmadı; `Features.tsx` / `AboutPage.tsx`'te aynı küçük `text-gold` numara deseni duruyor | Erişilebilirlik | FE-54 | `a11y.spec.ts`'e hatalı form hâlleri; `text-gold` → `--color-gold-ink` |
| B-E8 | Tarihsiz davetiye için 12 ay kuralı (K257) fiyat sayfası SSS'sinde yok (gizlilik metninde var) | Tutarlılık | FE-52 | `retention.ts`'e `UNDATED_GUEST_DATA_MONTHS = 12`; SSS + gizlilik metni sabiti kullanır |
| B-E9 | Çekirdek akışların İngilizce çevirisi yok; yasal metinler ve SSS yalnızca Türkçe (`verify:i18n` tabanı 781, PrivacyPage 88) | `en` seçen kullanıcı karışık dil görür | FE-01 · SEC-11 | Ayrı faz (çeviri); bu adımda değil |
| B-E10 | e2e için CI iş akışı yalnızca taslak | e2e yalnızca elle koşuluyor | TST-04 (§A-1) | §5 K-6 kararından sonra |

## 3. Koşulmayan doğrulamalar (B7 ⏳)

| # | Doğrulanmayan | İş | Neden | Kim koşabilir |
|---|---|---|---|---|
| B-D1 | Yerel Nginx: bot UA → önizleme sayfası, insan → SPA | FE-04 | Bütçe | Ajan (Herd) ya da İsmail: `check-share-preview.sh` |
| B-D2 | Bot listesindeki platform belgesi bağlantıları | FE-04 | Dış istek yok kuralı | İsmail |
| B-D3 | WhatsApp'ta gerçek önizleme | FE-04 | Canlı ortam | İsmail |
| B-D4 | Yerel Nginx: daraltılmış CSP ile font ihlali yok, `/fonts/` başlıkları | SEC-12 | Bütçe | Ajan (Herd) ya da İsmail |
| B-D5 | Yedek bucket'ı ömür kuralı 30 + 7 gün; Lightsail görüntüsü 7 gün; medya eski sürümü 7 gün | SEC-11 | AWS paneli (bucket henüz açılmadı, K152 ⚠️) | İsmail |
| B-D6 | Natro posta verisinin Türkiye'de tutulduğu | SEC-11 | Doğrulanmadı | İsmail |
| B-D7 | Gizlilik metninin hukuki uygunluğu | SEC-11 | Kapsam dışı | Hukukçu |
| B-D8 | Fiyat sayfasının tarayıcı görünümü | FE-52 | Yalnızca metin değişti | Ajan |
| ✅ B-D9 | `npm run e2e` — FE-01, FE-02'de koşulmadı; FE-04 · SEC-11 · FE-52 ve diğer hatların birleşmelerinden sonra entegrasyonda hiç koşulmadı | — | Bütçe; `davetkart_e2e` DB'si hatlar arasında ortak (aynı anda iki hat koşmamalı) | Ajan (tek hat, sırayla) |
| B-D10 | Editör çökünce bekleyen kaydın `flush` edilmesi | FE-02 | Koddan çıkarım | Ajan (e2e vakası) ya da İsmail |
| B-D11 | Ana sayfada CLS yok | FE-10 | Ölçülmedi | Ajan (`npm run perf`) |
| B-D12 | Mobil web vitals gerçek cihazda | FE-53 | RUM kapsam dışı | İsmail |
| B-D13 | Narrator yanlış parolayı duyuruyor | FE-54 | Ajan ekran okuyucu çalıştıramaz | İsmail |
| B-D14 | Zarf ipucu kontrastı ≥ 4,5 bütün şablonlarda | FE-54 | Yalnızca e2e şablonunda ölçüldü | Ajan (betik) |
| ✅ B-D15 | `composer check` uçtan uca (testler dahil) | TST-04, SEC-12 | B-H1 yüzünden phpstan'da duruyor | B-H1'den sonra ajan |

## 4. Senin elle yapman gerekenler

| # | İş | Komut / yer | Kaynak |
|---|---|---|---|
| B-İ1 | Paylaşım önizlemesi duman testi | `bash deploy/smoke/check-share-preview.sh -k https://davetkart.test <yayındaki-id>` | FE-04 |
| B-İ2 | Güvenlik başlıkları + font duman testi | `bash deploy/smoke/check-security-headers.sh -k https://davetkart.test` · tarayıcıda bir sinema şablonu → ağ sekmesinde `/fonts/` dışı font isteği yok | SEC-12 |
| B-İ3 | Canlıya çıkınca WhatsApp'ta davetiye bağlantısı paylaşmak; Facebook Sharing Debugger ile `og:image` | — | FE-04 |
| B-İ4 | Yedek bucket'ı açılınca ömür kuralını (30 + 7) ve Lightsail görüntü saklamasını (7) panelde doğrulamak; farklıysa `src/legal/retention.ts` → `BACKUP_PURGE_DAYS` | AWS konsolu | SEC-11 |
| B-İ5 | Gizlilik metnini yayından önce bir hukukçuya okutmak | `/privacy` | SEC-11 |
| B-İ6 | Sentry ya da Gemini açılırsa veri bölgelerini gizlilik metnine işlemek | `PrivacyPage` `veri-isleyenler` | SEC-11 |
| B-İ7 | Shopier sorusunu göndermek; cevap gelince 19.15'i yeniden koşmak, sonra gizlilik metnindeki Shopier satırını güncellemek | `notes/04-SHOPIER-ALICI-ALANLARI-SORUSU.md` | SEC-10 → SEC-11 |
| B-İ8 | Tarayıcıda dil kapsamı: `localStorage.setItem('davetkart-language','de')` → yenile → Türkçe, seçicide iki dil | — | FE-01 |
| B-İ9 | Oturumlu editörde hata tetikleyip kaydetme notunun `saving → saved` geçişini görmek | — | FE-02 |
| B-İ10 | Narrator ile giriş sayfasında yanlış parola: hata duyuruluyor mu; klavye gezinmesi denetimi | — | FE-54 |
| B-İ11 | Yayından önce `npm run perf` | frontend | FE-53 |
| B-İ12 | Gerçek cihazda mobil ölçüm (B-D12) | — | FE-53 |
| B-İ13 | CI isteniyorsa taslağı `e2e.yml` yapıp backend deposu erişimini ayarlamak | frontend `.github/` | TST-04 |

## 5. Bekleyen kararlar (§A boş → varsayılan, "İsmail cevaplamadı")

| # | Karar | Şu an geçerli varsayılan | Kaynak |
|---|---|---|---|
| K-1 | Paylaşım önizlemesi görseli | Galeri açıksa ilk fotoğraf, yoksa ana sayfa posteri; Elit'te site adı yok (B-E4) | FE-04 §A |
| K-2 | Veri işleyen listesi ve yedek süresi | AWS, CloudFront, SES, Shopier, Natro; Sentry/Gemini koşullu; "en geç 40 gün" | SEC-11 §A |
| K-3 | Yayın süresi olacak mı | Hayır: davetiye siz silene kadar yayında (K232) | FE-52 §A |
| K-4 | Bundle bütçesi: cırcır (720 / 900 kB) mı, hedef sayı mı | Cırcır (B-E6) | FE-10 |
| K-5 | Ana sayfa LCP için ayrı bütçe isteniyor mu | Yok | FE-53 |
| K-6 | e2e CI'da koşsun mu | Hayır (taslak) | TST-04 §A-1 |
| K-7 | Geri yüklemeden sonra silmeler yeniden uygulanacak mı (silme günlüğü) | Karar yok (B-E1) | SEC-11 |

## 6. Temizlik ve devir

- **Ortak dosyalar güncellenmedi** (BAGLAM gereği): `DECISION-INDEX.md`, `CHANGELOG.md`, `EK-FAZ-19.md`, `phases/faz-19/README.md`,
  backend `FAZ-19.md`. K224–K232 ve CHANGELOG satırları her kaydın "## Kararlar" ve "## CHANGELOG satırı" bölümünde hazır;
  toplu adımda (19.90) aktarılacak. Bu rapor da `phases/faz-19/README.md`'ye o adımda eklenmeli.
- **Boş backend dalı:** `fix/2026-11-22-tst-04-e2e` (commit yok) silinebilir.
- **Birleşmiş dallar** (silinebilir): frontend 10, docs 11 (bu rapor dahil), backend 2 (`sec-12-self-hosted-fonts`, `fe-04-share-preview`).
  Ana klasörde `git branch --merged` ile görülür.
- **Hat B worktree'leri** 25 Kasım'da entegrasyon başına ayrık (detached) alındı: backend `78c1cc4`, frontend `fe70b62`,
  docs `fb86574`. Ortak adımda bu worktree'ler kullanılacaksa önce entegrasyon dalına geçilmeli; aynı dal iki worktree'de açık olamaz.

## 7. Entegrasyon başında kapılar (25 Kasım 2026)

Hat B worktree'leri: backend `78c1cc4` (Merge ARC-03), frontend `fe70b62` (Merge FE-52).

| Kapı | Sonuç |
|---|---|
| frontend `npm run check` | ✅ exit 0 · ilk yükleme 710,3 / 720 kB · misafir 883,5 / 900 kB · gömülü Türkçe 781 |
| backend `pint --test` | ✅ |
| backend `php artisan k18:check` | ✅ 0 ihlal |
| backend phpstan, paralel (`composer analyse`) | 🔴 512 — **sahte** (B-H7); sonuç önbelleği temizlenince de aynı |
| backend phpstan, tek süreç (`--debug`) | 🔴 9 gerçek hata (B-H1) |
| backend `php artisan test` (`DAVETKART_TEST_DB_SUFFIX=hat_b`) | ✅ 1271 / 1271 (4613 doğrulama, ~162 sn) |
| `npm run e2e` | ⏳ koşmadı (B-D9) |

## 8. Ortak düzeltme dalında kapananlar (25 Kasım 2026)

Her hata `faz-19-fix`'ten kendi dalında düzeltildi ve `--no-ff` ile birleşti. Komutlar:
[`FAZ-19-HAT-B-FIX-COMMIT-KOMUTLARI.md`](FAZ-19-HAT-B-FIX-COMMIT-KOMUTLARI.md). Yeni karar yok.

| # | Ne yapıldı | Kanıt (görülen çıktı) |
|---|---|---|
| B-H7 | `phpstan.neon` → `tmpDir: storage/phpstan` (+ `.gitignore`, `phpstan.md` bölümü). Hat C #11 ve Hat A H3 ile aynı kök; birleşik dalda bu hâli geçerli | Art arda iki koşu aynı sayı (8 gerçek hata, soğuk 34 sn / sıcak 2 sn) |
| B-H1 | `ResolvesRefundRequests`: `is_string` daraltması + kılavuz (K18). `CheckK18`: `paths`/`--base` daraltması. `K18Inspector::close`: `@param-out list<…>`. `K18CheckTest`: `PendingCommand` yardımcısı (projedeki desen). `ReadinessTest`: Mockery yerine tipli PHPUnit `createStub(Job::class)`. `ignoreErrors`/cast yok | PHPStan 0 hata; `composer check` exit 0 (1271/1271); Hat C birleşmesinden sonra birleşik uçta yine exit 0 (1273/1273) |
| B-H2 | **Kök neden form yeniden bağlanması değildi.** Mühür tıklanınca hemen `scale(0)` olur (Playwright'a göre gizli), ama zarf kayıp sökülene kadar içerik `inert`'tir; `fill` alana ulaşmıyordu. `openGuestPage` artık zarfın DOM'dan kalkmasını bekliyor (`toHaveCount(0)`); `toPass` döngüsü kaldırıldı. Gerçek misafir için veri kaybı yok (`inert` yazmayı engeller) | Ölçüm: devirde `{"inert":true,"gate":true}`, zarf kalkınca `inert=false`; tek `fill` tuttu. e2e 4/4 |
| B-H3 | `PaywallModal` kartı `role="dialog"` `aria-modal` `aria-labelledby`; yeni `useFocusTrap` (açılınca "Kapat", Tab içeride, kapanınca açan öğeye dönüş). axe pencere açıkken 3 `color-contrast` buldu → kilitli plan `opacity-55` kalktı, dahil olmayan özellik `text-stone-500` | `paywall-after-publish.spec.ts`: rol + ad, odak 12 tuşta içeride, axe (WCAG A/AA) temiz, Esc kapatır, odak galeri anahtarına döner. e2e 4/4 |
| B-H5 | Çerez Politikası "Kesinlikle Gerekli" listesine LCV düzenleme kodu (ad `RSVP_RECEIPT_KEY_PREFIX`, amaç, süre). Satır `t()` ile (tr/en): gömülü yazılsaydı `verify:i18n` tabanı 781 → 782 olurdu | `verify-render` ✓ "LCV düzenleme kodu (davetkart_rsvp_receipt:*) listede"; `verify:i18n` 781 |
| B-H6 | 10 kılavuz (4 `fontlar.md`, `oniki-…`, `premium-videolu`, 4 `tasarim/*-KONSEPTI.md`): Google Fonts anlatımı SEC-12/K226'ya göre düzeltildi | `docs/rehber`'de "Google Fonts'a bağlı" kalmadı (grep) |
| B-H4 | Yalnızca iki kaynak vardı: alt bilgi sütun başlıkları `h4` → `h2` (11 sayfa), paneldeki davetiye kartı `h3` → `h2` (2 sayfa). `a11y.spec.ts` `heading-order`'ı kapıya aldı | e2e a11y 14 sayfada 0 ihlal |

**Birleşik uçta kapılar** (frontend `798cbb5`, backend `3f525ef` — Hat C dahil):

| Kapı | Sonuç |
|---|---|
| frontend `npm run check` | ✅ exit 0 · ilk yükleme 711,0 / 720 kB · misafir 884,3 / 900 kB (B-E6 payı daha da daraldı) |
| `npm run e2e` (B-D9) | ✅ 4/4 (B-H4 dalında, birleşmeden önce; B-H5/B-H6 e2e'ye dokunmuyor) |
| backend `composer check` (B-D15) | ✅ exit 0 · pint, phpstan 0, errors/plans/env, `k18:check` 0 ihlal, 1273/1273 |

**Açık kalan:** §2–§6 (eksikler, elle işler, kararlar) bu adımın kapsamı dışında; değişmedi.
