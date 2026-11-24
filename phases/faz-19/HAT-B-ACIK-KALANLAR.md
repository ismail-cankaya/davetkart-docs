# Faz 19 — Hat B: açık kalanlar, bilinen hatalar, yapılmayanlar

> **Tarih:** 24 Kasım 2026 · **Kapsam:** Hat B'nin 10 işi (19.17, 19.18, 19.19, 19.20, 19.21, 19.22, 19.23, 19.24, 19.25, 19.27) · **Kararlar:** K224–K232
> **Kaynak:** `kayit/` altındaki 10 kaydın "Plandan sapma", "B7", "Gördüm, dokunmadım" ve "İsmail'e kalan" bölümleri ile oturumda görülenler.
> **Durum:** 10 işin hepsi entegrasyon dallarına birleşmiş; birleşmemiş Hat B dalı yok.

## 0. Özet

| Bölüm | Adet | En önemlisi |
|---|---|---|
| 1. Bilinen hatalar | 6 | `composer check` phpstan'da kırmızı; LCV formunda yazılan ad silinebiliyor |
| 2. Eksikler | 10 | Yedekten geri yüklemede silinmiş veri geri dönebilir |
| 3. Koşulmayan doğrulamalar | 15 | Nginx (FE-04, SEC-12) hiç koşulmadı |
| 4. Elle yapman gerekenler | 13 | Herd Nginx duman testleri, AWS paneli, hukukçu okuması |
| 5. Bekleyen kararlar | 6 | §A'sı boş geçilen işlerde varsayılanların onayı |
| 6. Temizlik ve devir | 4 | Ortak dosyalar (DECISION-INDEX, CHANGELOG, FAZ-19.md) K224–K232 ile güncellenmedi |

## 1. Bilinen hatalar (bugün kırmızı ya da yanlış çalışan)

| # | Hata | Nerede | Kaynak | Hat B'nin mi? |
|---|---|---|---|---|
| H1 | `composer check` phpstan adımında kırmızı: `cast.string` ×2 ve bir `ReadinessTest` hatası. Sonraki adımlar (testler) `composer check` içinden hiç koşmuyor | backend `app/Console/Commands/Concerns/ResolvesRefundRequests.php:29` · `tests/…/ReadinessTest` | TST-04, SEC-12, FE-04 kayıtları | Hayır (Faz 14.6'dan kalma); Hat B dosyaları phpstan'da temiz |
| H2 | Misafir LCV formu zarf açıldıktan sonra bir kez yeniden çizilebiliyor; o arada yazılan ad siliniyor (`RSVPForm` yerel durumu). e2e'de `toPass` ile aşıldı, kök neden düzeltilmedi | frontend `RSVPForm` | TST-04 | Hayır; gerçek misafirde de olabilir |
| H3 | Plan duvarında `role="dialog"` / `aria-modal` yok; ekran okuyucu kipin değiştiğini bilmez | frontend plan duvarı (paywall) | TST-04 | Hayır |
| H4 | `heading-order` ihlali 12 sayfada (axe best-practice; WCAG AA kapısında değil) | birden çok sayfa | FE-54 | Kapsam dışı bırakıldı |
| H5 | Çerez Politikası'nın yerel depolama listesinde LCV düzenleme kodu (`davetkart_rsvp_receipt:*`) yok | frontend `src/pages/legal/CookiesPage.tsx` | SEC-11 · PrivacyPage kılavuzu | Hayır |
| H6 | Birkaç kılavuz hâlâ Google Fonts sorgusunu anlatıyor (tarihçe; bilgi yanlış) | frontend `docs/rehber/…/index.md`, `oniki-etkilesimli-sablon.md`, `premium-videolu.md`, `tasarim/*-KONSEPTI.md` | SEC-12 | Evet (yalnızca dört `fontlar.md`'ye not düşüldü) |

## 2. Eksikler (söz verilmiş ya da beklenen ama yapılmamış)

| # | Eksik | Neden önemli | Kaynak |
|---|---|---|---|
| E1 | Yedekten geri yükleme kitabında "silinmiş veriyi yeniden sil" adımı yok; döküm geri yüklenirse son 40 günde silinen hesap/misafir verisi canlıya dönebilir | Gizlilik metni (K231) yedeklerden silinmeyi söylüyor | SEC-11 |
| E2 | 10 yıl dolunca `orders` satırlarını silen iş yok; metin "10 yıl" diyor | Söz verilmiş saklama süresi | SEC-11 · PrivacyPage kılavuzu |
| E3 | Shopier'e her alıcı için aynı yer tutucu TCKN/telefon/adres gidiyor; Shopier'in cevabı bekleniyor | Gizlilik metni bugünkü alanları yazıyor; cevap gelince metin de değişir | SEC-10 (Hat A, yalnızca hazırlık) → SEC-11 |
| E4 | Davetiyeye özel kapak alanı yok; paylaşım önizlemesinde şablon kapağı kullanılamıyor (frontend derlemesinde dosya adı hash'li) | WhatsApp önizlemesi galerisi olmayan davetiyede genel poster gösterir | FE-04 |
| E5 | Misafir sayfası şablon kataloğunu hâlâ indiriyor (~104 kB); `motion` ilk yüklemede (144 kB) | Mobil ilk yükleme ve LCP | FE-10 · FE-53 |
| E6 | `verify:bundle` ilk yükleme 709 / 720 kB: pay 11 kB | Bir sonraki özellik kapıyı kırmızıya çevirebilir | FE-53 |
| E7 | Form hata mesajlarının `aria-describedby` bağı axe ile taranmadı; `Features.tsx` / `AboutPage.tsx`'te aynı küçük `text-gold` numara deseni duruyor | Erişilebilirlik | FE-54 |
| E8 | Tarihsiz davetiye için 12 ay kuralı (K257) fiyat sayfası SSS'sinde yok (gizlilik metninde var) | Tutarlılık | FE-52 |
| E9 | Çekirdek akışların İngilizce çevirisi yok; yasal metinler ve SSS yalnızca Türkçe (`verify:i18n` tabanında PrivacyPage 88) | `en` seçen kullanıcı karışık dil görür | FE-01 · SEC-11 |
| E10 | e2e için CI iş akışı yalnızca taslak; GitHub'da çalışmıyor | e2e yalnızca elle koşuluyor | TST-04 (§A-1) |

## 3. Koşulmayan doğrulamalar (B7 ⏳)

| # | Doğrulanmayan | İş | Neden |
|---|---|---|---|
| D1 | Yerel Nginx: bot UA → önizleme sayfası, insan → SPA | FE-04 | Bütçe |
| D2 | Bot listesindeki platform belgesi bağlantıları açılıp kontrol edilmedi | FE-04 | Dış istek yok kuralı |
| D3 | WhatsApp'ta gerçek önizleme | FE-04 | Canlı ortam gerekir |
| D4 | Yerel Nginx: daraltılmış CSP ile font ihlali yok, `/fonts/` önbellek başlıkları | SEC-12 | Bütçe |
| D5 | Yedek bucket'ı ömür kuralı gerçekten 30 + 7 gün; Lightsail görüntüsü 7 gün; medya eski sürümü 7 gün | SEC-11 | AWS paneli (bucket henüz açılmadı, K152 ⚠️) |
| D6 | Natro posta verisinin Türkiye'de tutulduğu | SEC-11 | Doğrulanmadı |
| D7 | Gizlilik metninin hukuki uygunluğu | SEC-11 | Kapsam dışı |
| D8 | Fiyat sayfasının tarayıcı görünümü | FE-52 | Yalnızca metin değişti |
| D9 | `npm run e2e` | FE-01, FE-02; ayrıca FE-04 · SEC-11 · FE-52'den sonra yeniden koşulmadı | Bütçe |
| D10 | Editör çökünce bekleyen kaydın `flush` edilmesi | FE-02 | Koddan çıkarım; tarayıcıda denenmedi |
| D11 | Ana sayfada CLS yok | FE-10 | Ölçülmedi |
| D12 | Mobil web vitals gerçek cihazda | FE-53 | RUM kapsam dışı |
| D13 | Narrator yanlış parolayı duyuruyor | FE-54 | Ajan ekran okuyucu çalıştıramaz |
| D14 | Zarf ipucu kontrastı ≥ 4,5 bütün şablonlarda | FE-54 | Yalnızca e2e şablonunda ölçüldü |
| D15 | Tam backend paketi `composer check` içinden | TST-04, SEC-12 | H1 yüzünden phpstan'da duruyor (FE-04'te `php artisan test` ayrıca koşuldu: 1264/1264) |

## 4. Senin elle yapman gerekenler

| # | İş | Komut / yer | Kaynak |
|---|---|---|---|
| İ1 | Paylaşım önizlemesi duman testi | `bash deploy/smoke/check-share-preview.sh -k https://davetkart.test <yayındaki-id>` | FE-04 |
| İ2 | Güvenlik başlıkları + font duman testi | `bash deploy/smoke/check-security-headers.sh -k https://davetkart.test` · tarayıcıda bir sinema şablonu → ağ sekmesinde `/fonts/` dışı font isteği yok | SEC-12 |
| İ3 | Canlıya çıkınca WhatsApp'ta davetiye bağlantısı paylaşmak; Facebook Sharing Debugger ile `og:image` | — | FE-04 |
| İ4 | Yedek bucket'ı açılınca ömür kuralını (30 + 7) ve Lightsail görüntü saklamasını (7) panelde doğrulamak; farklıysa `src/legal/retention.ts` → `BACKUP_PURGE_DAYS` | AWS konsolu | SEC-11 |
| İ5 | Gizlilik metnini yayından önce bir hukukçuya okutmak | `/privacy` | SEC-11 |
| İ6 | Sentry ya da Gemini açılırsa veri bölgelerini gizlilik metnine işlemek | `PrivacyPage` `veri-isleyenler` | SEC-11 |
| İ7 | Shopier sorusunu göndermek; cevap gelince 19.15'i yeniden koşmak, sonra gizlilik metnindeki Shopier satırını güncellemek | `notes/04-SHOPIER-ALICI-ALANLARI-SORUSU.md` | SEC-10 → SEC-11 |
| İ8 | Tarayıcıda dil kapsamı: `localStorage.setItem('davetkart-language','de')` → yenile → Türkçe, seçicide iki dil | — | FE-01 |
| İ9 | Oturumlu editörde hata tetikleyip kaydetme notunun `saving → saved` geçişini görmek | — | FE-02 |
| İ10 | Narrator ile giriş sayfasında yanlış parola: hata duyuruluyor mu; klavye gezinmesi denetimi | — | FE-54 |
| İ11 | Yayından önce `npm run perf` | frontend | FE-53 |
| İ12 | Son birleşmelerden sonra tam `npm run e2e` (D9) | frontend | — |
| İ13 | CI isteniyorsa taslağı `e2e.yml` yapıp backend deposu erişimini ayarlamak | frontend `.github/` | TST-04 |

## 5. Bekleyen kararlar

| # | Karar | Şu an geçerli varsayılan | Kaynak |
|---|---|---|---|
| K-1 | Paylaşım önizlemesi görseli | Galeri açıksa ilk fotoğraf, yoksa ana sayfa posteri; Elit'te site adı yok | FE-04 §A |
| K-2 | Veri işleyen listesi ve yedek süresi | AWS, CloudFront, SES, Shopier, Natro; Sentry/Gemini koşullu; "en geç 40 gün" | SEC-11 §A |
| K-3 | Yayın süresi olacak mı | Hayır: davetiye siz silene kadar yayında (K232) | FE-52 §A |
| K-4 | Bundle bütçesi: cırcır (720 / 900 kB) mı, hedef sayı mı | Cırcır | FE-10 |
| K-5 | Ana sayfa LCP için ayrı bütçe isteniyor mu | Yok | FE-53 |
| K-6 | e2e CI'da koşsun mu | Hayır (taslak) | TST-04 §A-1 |

## 6. Temizlik ve devir

- **Ortak dosyalar güncellenmedi** (BAGLAM gereği): `DECISION-INDEX.md`, `CHANGELOG.md`, `EK-FAZ-19.md`, `phases/faz-19/README.md`,
  backend `FAZ-19.md`. K224–K232 ve CHANGELOG satırları her kaydın "## Kararlar" ve "## CHANGELOG satırı" bölümünde hazır;
  toplu adımda (19.90) aktarılacak.
- **Boş backend dalı:** `fix/2026-11-22-tst-04-e2e` (commit yok) silinebilir.
- **Birleşmiş dallar** (silinebilir): frontend 10, docs 10, backend 2 (`sec-12-self-hosted-fonts`, `fe-04-share-preview`).
  Ana klasörde `git branch --merged` ile görülür; silmeden önce worktree'lerin o dalda olmadığına bak.
- **Hat B worktree'leri** son dallarda duruyor (backend `fix/2026-11-23-fe-04-share-preview`, frontend
  `fix/2026-11-24-fe-52-pricing-faq`, docs `docs/2026-11-24-fe-52-pricing-faq`); yeni işe başlamadan entegrasyona alınmalı.
