# Frontend mimarisi, backend sözleşmesi ve uçtan uca test — AUD-2026-11-12

> Yürüten: ana oturum (Fable 5.2) · Kopyalar: `_audit-snap\frontend` (okuma + dev sunucu 3000), `_audit-snap\frontend-tst` (build, `tsc`), `_audit-snap\backend` (okuma), `_audit-snap\backend-e2e` (sunucu 8000) · Commit: frontend `44caa49`, backend `d810410` · Tarih: 15 Kasım 2026
> Dilim ajanları (D1, D2) 13 Kasım'da kullanım sınırına takıldı; bu dosyayı ana oturum 15 Kasım'da tek başına yazdı. `FE-01…FE-49` mimari ve sözleşme (D1), `FE-50…` tarayıcı (D2).
> Tarayıcı: Chromium (başsız), Playwright 1.61.1. Yolculuklar `http://localhost:3000` (Vite dev), performans ölçümü `http://localhost:4173` (üretim build'i). Görünümler 1440×900 ve 390×844.

## Özet

Frontend'in backend'le konuştuğu yüzey temiz: 41 çağrının 40'ı `route:list`'teki bir rotayla birebir eşleşiyor
(41'incisi bayrakla kapalı, henüz yazılmamış konum araması), 16 Resource'un 170 alanının hepsi frontend'de
okunuyor, sekiz enum'un değerleri iki tarafta aynı, premium şablon listesi (32 kimlik) iki depoda aynı ve
`src/` altında tek bir sabit fiyat yok. Ağa yalnızca `src/services/` çıkıyor, `any` ve `@ts-ignore` sayısı sıfır.

Zayıf taraf kullanıcının gördüğü kabukta: dil seçici on dil sunuyor ama metinlerin yalnızca 72 anahtarı
çevrilmiş, geri kalanı (66 dosyada ~800 parça) koda gömülü Türkçe (`FE-01`); bir render hatası ya da
yüklenemeyen bir chunk kullanıcıya React Router'ın ham hata ekranını gösteriyor (`FE-02`); ana giriş paketi
1,64 MB ve 299 şablonu her sayfaya taşıyor (`FE-10`); davetiye
bağlantısı WhatsApp'ta önizlemesiz çıkıyor (`FE-04`).

Sekiz yolculuğun hepsi tarayıcıda koştu ve para kazandıran zincir çalışıyor: kayıt → davetiye → plan duvarı →
ödeme → dönüş sayfası → otomatik yayın → misafir LCV'si → panel. Yayındaki Gold davetiyede Elit modülü
açılamıyor (K-1 arayüzde de kapalı), hız sınırı ve oturum iptali beklendiği gibi. Tarayıcının gösterdiği
sorunlar: sihirbaz her ziyarette sunucuda boş taslak bırakıyor ve yenilemede editör kayboluyor (`FE-50`),
misafir fotoğraf/video yüklemesine arayüzden ulaşılamıyor (`FE-51`), fiyat sayfası backend'de olmayan bir
"yayın süresi" kuralını anlatıyor (`FE-52`), kısıtlı mobil koşulda LCP 3,9–5,7 saniye (`FE-53`).

**Kapsam dürüstlüğü:** 846 TS/TSX dosyasının 156'sı çekirdek (sayfalar, bileşenler, servisler, store'lar),
690'ı şablon. Çekirdekte `App.tsx`, `main.tsx`, `i18n.ts`, `services/api.ts`, `services/places.ts`,
`AppLayout`, `ProtectedRoute`, `PaymentReturnPage`, `utils/paymentReturn.ts`, `EmailChangeForm` satır satır
okundu; geri kalanı betikle ölçüldü (`evidence/scripts/fe-d1-metrics.mjs`). Şablonların gövdesi okunmadı;
373 şablonun 17'si tarayıcıda açıldı. **Koşmayanlar:** hesap silme ve parola değiştirme arayüzden
tamamlanmadı (test hesabı sonraki adımlar için gerekliydi; yanlış parolanın reddi API'den görüldü); Shopier ve
havale yolları (sahte sürücü kullanıldı); gerçek telefon ve Safari/Firefox; Lighthouse (yerine aynı ölçütler
CDP ile alındı).

Seviye sayıları: 🔴 0 · 🟠 0 · 🟡 9 · 🟢 9 · 💡 1 — Kanıt: KOŞTURULDU 13 · KOD OKUMASI 6

## Özet tablosu

| ID | Seviye | Kanıt türü | Başlık | Nerede | Efor | Tek satır öneri |
|---|---|---|---|---|---|---|
| FE-01 | 🟡 | KOŞTURULDU | Dil seçici on dil sunuyor, arayüzün büyük kısmı yalnızca Türkçe | `frontend:src/i18n.ts:32-43`, 66 `.tsx` dosyası | L | Ya dil listesini tr/en'e indir ya da metinleri sözlüğe taşı |
| FE-02 | 🟡 | KOD OKUMASI | Hata sınırı yok: render hatası ve yüklenemeyen chunk ham hata ekranı veriyor | `frontend:src/App.tsx:38-127` | S | Kök rotaya `errorElement` + chunk hatasında tek seferlik yenileme |
| FE-03 | 🟢 | KOŞTURULDU | `tsconfig` `strict` kapalı; açmak yalnızca 19 hata | `frontend:tsconfig.json` | S | `"strict": true` ekle, 19 hatayı düzelt |
| FE-04 | 🟡 | KOD OKUMASI | Davetiye bağlantısının paylaşım önizlemesi yok (Open Graph) | `frontend:index.html:1-12` | M | Bot isteklerine `/invite/{id}` için OG etiketli HTML dön |
| FE-05 | 🟢 | KOD OKUMASI | Plan kuralları frontend'de elle kopyalanmış | `frontend:src/data.ts:4018-4066`, `src/stores/useSubscriptionStore.ts:27-28` | M | Kuralları `/public/plans` yanıtına ekle ya da sözleşme dosyası + `verify` betiği |
| FE-06 | 🟢 | KOŞTURULDU | 404 sayfası yok; bilinmeyen adres ana sayfaya atıyor | `frontend:src/App.tsx:126` | S | "Sayfa bulunamadı" bileşeni |
| FE-07 | 🟢 | KOŞTURULDU | `README.md` boş; `CLAUDE.md` kodla çelişiyor | `frontend:README.md`, `frontend:CLAUDE.md:9,43` | S | README yaz, CLAUDE.md'yi güncelle |
| FE-08 | 🟢 | KOD OKUMASI | Konum araması: backend ucu olmayan, bayrakla kapalı kod | `frontend:src/services/places.ts:22-24` | S | Ucu yaz ya da kodu kaldır |
| FE-09 | 🟢 | KOD OKUMASI | 95 MB video depoda ve önbellek başlığı olmadan sunuluyor | `frontend:public/videos/`, `backend:deploy/nginx/davetkart.conf` | M | Videolara `Cache-Control`; dosyaları nesne deposuna taşı |
| FE-10 | 🟡 | KOŞTURULDU | Ana giriş paketi 1,64 MB: 299 şablon her sayfaya, misafir sayfasına bile yükleniyor | `frontend:src/components/templates/TemplateRenderer.tsx:2-88` | M | Şablonları kimliğe göre tembel yükle; paket bütçesi koy |
| FE-50 | 🟡 | KOŞTURULDU | Sihirbaz her ziyarette sunucuda boş taslak açıyor; yenilemede editör kayboluyor | `frontend:src/hooks/useInvitationAutoSave.ts`, `src/App.tsx:43` | M | Taslağı ilk gerçek içerikte oluştur; editör adresine kimlik koy |
| FE-51 | 🟡 | KOŞTURULDU | Misafir fotoğraf/video yüklemesine arayüzden ulaşılamıyor | `frontend:src/pages/InvitePage.tsx:123-127`, `src/components/preview/RsvpModal.tsx:177-188` | M | Yüklemeyi satır içi LCV formuna bağla ya da ucu kapat |
| FE-52 | 🟡 | KOD OKUMASI | Fiyat sayfası SSS'si backend'de olmayan "yayın süresi" ve ücretli uzatmayı anlatıyor | `frontend:src/pages/PricingPage.tsx:41,48-49` | S | Metni gerçek kurala göre yaz ya da kuralı karara bağla |
| FE-53 | 🟡 | KOŞTURULDU | Kısıtlı mobil koşulda LCP 3,9–5,7 sn; giriş ve fiyat sayfalarında CLS 0,33–0,63 | ana sayfa, misafir, giriş, fiyatlar | M | `FE-10` + fontları kendi alan adından ön yükle + fiyat kartlarına yer tut |
| FE-54 | 🟡 | KOŞTURULDU | Hata ve başarı mesajları ekran okuyucuya duyurulmuyor; alt bilgi ve fiyat kartında kontrast yetersiz | `frontend:src/components/ui/Toast.tsx:51`, `src/components/layout/Footer.tsx` | S | Toast kabına `role="status"`/`aria-live`; iki renk tonunu koyulaştır |
| FE-55 | 🟢 | KOŞTURULDU | "Planlarım" fiyat sayfasından plan alınabileceğini söylüyor; orada satın alma düğmesi yok | `frontend:src/pages/account/AccountPlansSection.tsx`, `src/pages/PricingPage.tsx` | S | Fiyat kartlarına girişli kullanıcı için "Satın al" bağlantısı |
| FE-56 | 🟢 | KOŞTURULDU | `dugun-gul-3d` "hareketi azalt" tercihinde hareket etmeye devam ediyor | `frontend:src/components/templates/dugun/DugunGul3d/` | S | Sahneyi `useReducedMotion` ile durdur |
| FE-58 | 🟢 | KOŞTURULDU | Ödeme dönüşünde davetiye kullanıcı onayı olmadan yayınlanıyor; K67 ile çelişki sorusu açık | `frontend:src/hooks/useAutoPublish.ts` | S | Kararı kapat: K67'yi daralt ya da "Şimdi yayınla" düğmesi |
| FE-57 | 💡 | KOŞTURULDU | Küçük arayüz pürüzleri: düşen oturumda açıklama yok, yığılan hata bildirimleri, eski ipucu metni | `frontend:src/services/api.ts:178-191`, `src/components/rsvp/LiveRsvpPanel.tsx:261` | S | Girişe yönlendirirken tek satır bilgi; aynı bildirimi yineleme |

## Neler iyi

1. **Ağ tek kapıdan çıkıyor.** `src/services/` dışında `axios`, `fetch` ya da `api.*` çağıran dosya yok
   (`FE-d1-metrics.txt` §1: 0 dosya). Token enjeksiyonu ve 401 davranışı tek interceptor'da
   (`services/api.ts:80-86,178-191`).
2. **401'in iki anlamı ayrılmış.** `INVALID_CREDENTIALS` formda kalır, `UNAUTHENTICATED` oturumu düşürür;
   eski token'ın geç gelen 401'i yeni oturumu düşürmez (`api.ts:178-204`). Bu, çoğu SPA'nın atladığı bir yarış.
3. **Sözleşme kendi testine sahip.** `npm run verify` on bir betikle uç yollarını, hata kodlarını, ETag
   davranışını, fiyat kataloğunu ve çizimi sınıyor (`evidence/commands/TST-npm-run-check.txt`: on bir `✓`).
   Yanlış bir uç derleme hatası vermez; bu betikler o boşluğu kapatıyor.
4. **Tip disiplini.** `any`: 0 · `as any`: 0 · `@ts-ignore`: 0 (846 dosyada). Ağ sınırında yanıtlar `unknown`
   alınıp tip koruyucularla daraltılıyor (`services/places.ts:33-52`).
5. **Fiyat yalnızca backend'den.** `₺`/`TL`/sayısal tutar taraması 4 eşleşme verdi, dördü de yorum satırı
   (`FE-d1-metrics.txt` §6); `verify:pricing` "src/ fiyat taşımıyor" diyor.
6. **Yeni şablonlar doğru desenle eklenmiş.** Ana sayfa dışındaki 23 sayfa `React.lazy` (`App.tsx:10-36`),
   Faz 15–17'nin 74 şablonu `lazyPresets.ts` üzerinden ayrı chunk; `three.js` yalnızca dört 3B şablonda
   yükleniyor. (Eski 299 şablon bu desende değil: `FE-10`.)
7. **Store'lar seçiciyle okunuyor.** Seçicisiz `useXStore()` çağrısı 0; dokuz Zustand store alan adına göre
   bölünmüş. `persist` ara katmanı yok, oturumun saklanması tek serviste (`services/auth.ts`).
8. **Hareket azaltma her katmanda.** `MotionConfig reducedMotion="user"` (`App.tsx:136`), `index.css`'te üç
   `prefers-reduced-motion` kuralı, şablonlarda 213 kullanım.
9. **Frontend ↔ backend yol ikilileri aynı.** `/sifre-sifirla`, `/eposta-onay`, `/odeme/basarili`,
   `/odeme/hata` (`backend:config/davetkart.php:297-299`, `config/payment.php:93-94` ↔ `App.tsx:50,69,100,108`).

## Bulgular

### FE-01 Dil seçici on dil sunuyor, arayüzün büyük kısmı yalnızca Türkçe
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:src/i18n.ts:32-43` (on dil) · `frontend:src/locales/*/translation.json` (dil başına 72 anahtar) · gömülü metin: `src/pages/` 23 dosya (~435 parça), `src/components/` 43 dosya (~361 parça), şablonlar 145 dosya (~610 parça)
- Senaryo: 1) Ziyaretçi dil seçiciden "Deutsch" ya da "العربية" seçer. 2) Üst menü ve ana sayfa başlıkları çevrilir (72 anahtar). 3) Kayıt sonrası gördüğü her şey (panel, editör, ödeme, hesap, LCV penceresi, yasal metinler, misafir sayfasındaki sabit etiketler) Türkçe kalır. 4) Arapçada `dir="rtl"` sayfa düzenini çevirir, metin Türkçe kalır.
- Kanıt: `evidence/commands/FE-d1-metrics.txt` §2–§2b: `t('…') çağrısı: 60 · i18n kullanan dosya: 15 (çekirdek 15, şablon 0)`; `pages: gömülü Türkçe metin içeren 23 .tsx dosyası, ~435 metin parçası · bunlardan i18n de kullanan 3`. Sayım kabadır (JSX metni ve dizgi sabitleri; yorumlar ayıklandı), oran güvenilirdir.
- Etki: Türkçe bilmeyen kullanıcı ilk ekranda çeviri görüp ödeme adımında Türkçe'yle karşılaşır. Hata mesajları yalnızca tr/en. Ürün bugün Türkiye pazarına satılıyorsa etki küçük; sorun, arayüzün veremediği bir sözü vermesi.
- Neden önemli (öğretici not): Uluslararasılaştırma "sözlük dosyası eklemek" değil, **metnin koddan ayrılması**dır. Yarım kalan i18n hiç olmayandan kötüdür: kullanıcıya desteklenmeyen bir dili desteklenir diye sunar ve her yeni ekran "bunu da çevirecek miyiz" kararını sessizce erteler.
- Öneri: En ucuz: `SUPPORTED_LANGUAGES`'ı `tr` ve `en` ile sınırla (hata sözlüğü zaten bu ikisinde), diğer sekiz dili gerçekten çevrilene kadar gizle. Sağlam: çekirdek 66 dosyanın metnini alan adına göre namespace'lere taşı (`dashboard`, `editor`, `checkout`, `account`, `legal`), CI'da "JSX içinde Türkçe harf" taraması.
- Test önerisi: `verify:i18n`: çekirdek `.tsx` dosyalarında `t()` dışında Türkçe harf içeren JSX metni varsa kırmızı. Öldürmesi gereken mutant: bir `t('…')` çağrısını düz metne çevirmek.
- Efor: L (sınırlama seçeneği S)
- İlgili: `notes/03-FRONTEND-YAPILACAKLAR.md`

### FE-02 Hata sınırı yok: render hatası ve yüklenemeyen chunk ham hata ekranı veriyor
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `frontend:src/App.tsx:38-127` (hiçbir rotada `errorElement` yok) · `frontend:src/components/layout/AppLayout.tsx:38-40` (`Suspense` var, sınır yok) · tek sınır `src/components/templates/shared/three/ThreeStage.tsx:24-27` (yalnızca WebGL sahnesi)
- Senaryo: A) Bir sayfa bileşeni beklenmeyen bir yanıtla `undefined` üzerinde alan okur → React ağacı düşer → React Router varsayılan ekranı: "Unexpected Application Error!". B) Tembel yüklenen bir sayfanın chunk'ı yüklenemez (mobil bağlantı kopması, zaman aşımı ya da 14 günden eski bir sekme) → `import()` reddedilir → aynı ham ekran. Yayın sonrası "eski chunk 404" hâli dağıtım betiğinde düşünülmüş: `backend:deploy/deploy-frontend.sh` eski `assets/` dosyalarını 14 gün tutuyor (`KEEP_OLD_ASSETS_DAYS=14`); geriye ağ hatası ve çok eski sekmeler kalıyor.
- Kanıt: `evidence/commands/FE-d1-metrics.txt` §4: `ErrorBoundary / componentDidCatch / errorElement — çekirdek 0 · şablon 2`. Tarayıcıda hata sınırı senaryosu (bileşen hatası, bulunamayan chunk) **koşturulmadı**.
- Etki: Kullanıcı İngilizce, markasız bir hata ekranında kalır; editördeki kaydedilmemiş değişiklik kaybolur. B senaryosu zayıf mobil bağlantıda, yani misafirlerin tipik koşulunda görülür.
- Neden önemli (öğretici not): `Suspense` yüklemenin **beklemesini** yönetir, **başarısızlığını** değil. Tembel yüklenen her modül bir ağ isteğidir ve her ağ isteği başarısız olabilir. Hata sınırı, hatanın yayılacağı alanı senin seçtiğin yerdir; seçmezsen çerçeve en dışta seçer.
- Öneri: 1) Kök rotaya `errorElement: <RouteError />` (marka, "Sayfayı yenile", "Ana sayfa"). 2) `window.addEventListener('vite:preloadError', …)` ile chunk hatasında tek seferlik `location.reload()` (sonsuz döngüye karşı `sessionStorage` bayrağı).
- Test önerisi: `verify:render`'a "çocuğu hata fırlatan rota `RouteError` çiziyor" vakası. Öldürmesi gereken mutant: `errorElement` satırını silmek.
- Efor: S
- İlgili: `05-operations.md` "Neler iyi" 2 (eski parçaların 14 gün tutulması) · React Router belgeleri: "Error Boundaries"

### FE-03 `tsconfig` `strict` kapalı; açmak yalnızca 19 hata
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:tsconfig.json` (`strict`, `strictNullChecks`, `noImplicitAny` yok) · `frontend:CLAUDE.md:43` ("Strict TypeScript")
- Senaryo: 1) Tipler `publishedAt: string | null` gibi `null`'ı beyan ediyor (`src/types.ts:441`). 2) `strictNullChecks` kapalıyken derleyici `null`'ı her tipe atanabilir sayar; `record.publishedAt.slice(0, 10)` derlenir, çalışırken düşer. 3) `npm run lint` yeşil kalır.
- Kanıt: `evidence/commands/FE-tsc-strict.txt`: `npx tsc --noEmit --strict` → 19 hata (çekirdek 3, şablonlar 16; 15'i tek dosyada: `shared/effects/particleEngine.ts`). `--strictNullChecks` tek başına 18.
- Etki: Bugün hata yok denecek kadar az; yani kod zaten katı kipe göre yazılmış ama derleyici bunu **korumuyor**. Bir sonraki `null` hatası derlemede değil kullanıcıda çıkar.
- Neden önemli (öğretici not): Tip sistemi bir sözleşmedir; `strict` kapalıyken sözleşmenin en değerli maddesi (`null` olabilir) uygulanmaz. 19 hata, kuralı açmanın en ucuz olduğu andır; her yeni dosya bu sayıyı büyütür.
- Öneri: `"strict": true` ekle; `particleEngine.ts`'teki 15 `possibly null` hatasını erken dönüşle kapat. Ardından `noUncheckedIndexedAccess` ayrı bir adım olarak değerlendirilebilir.
- Test önerisi: Yok; kural `npm run lint`'in kendisi olur.
- Efor: S
- İlgili: `GOZDEN-GECIRME-2026-10-09-FRONTEND.md`

### FE-04 Davetiye bağlantısının paylaşım önizlemesi yok (Open Graph)
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `frontend:index.html:1-12` (`description`, `og:*`, `twitter:*` etiketi yok) · `backend:deploy/nginx/davetkart.conf` (`location / { try_files $uri /index.html; }`, bot ayrımı yok)
- Senaryo: 1) Çift davetiyesini yayınlar ve bağlantıyı WhatsApp'tan gönderir. 2) WhatsApp'ın önizleme botu `/invite/<id>`'yi ister; JavaScript çalıştırmaz. 3) Aldığı HTML her adres için aynı `index.html`: başlık "DavetKart — Premium Dijital Davetiyeler", açıklama ve görsel yok. 4) Sohbette çiftin adı ve kapak görseli yerine çıplak bir bağlantı görünür.
- Kanıt: `index.html` 12 satır; `<head>` içinde yalnızca `charset`, `viewport`, `icon`, `title`. Gerçek bir botla koşturulmadı (canlı sisteme istek yasak).
- Etki: Ürünün dağıtım kanalı mesajlaşma uygulamaları. Önizleme, davetiyenin ilk izlenimi ve tıklanma oranının en büyük belirleyicisi; Elit planın "logosuz yayın" vaadi de önizlemede "DavetKart" başlığıyla zayıflıyor.
- Neden önemli (öğretici not): Tek sayfa uygulaması (SPA) içeriğini tarayıcıda üretir; bağlantı önizleme botları tarayıcı değildir. "Sunucu ilk yanıtta ne dönüyor" sorusu SEO'dan önce **paylaşılabilirlik** sorusudur.
- Öneri: En ucuz: `index.html`'e site genelinde `og:title`, `og:description`, `og:image` (bütün davetiyeler aynı önizlemeyi alır). Sağlam: Nginx'te bilinen bot `User-Agent`'ları için `/invite/{id}` isteğini Laravel'e yönlendir; Laravel yayınlanmış davetiyenin adlarını, tarihini ve kapak görselini OG etiketleriyle dönen küçük bir Blade şablonu çizsin (veri zaten `GET /api/public/invitations/{id}` ile herkese açık). Elit'te `og:site_name` boş bırakılır.
- Test önerisi: `PublicInvitationPreviewTest::a_bot_gets_the_couples_names_in_og_title` ve `::an_unpublished_invitation_gets_the_generic_preview`. Öldürmesi gereken mutant: yayın durumu koşulunu kaldırmak (taslak adları sızar).
- Efor: M
- İlgili: K102 (logosuz yayın)

### FE-05 Plan kuralları frontend'de elle kopyalanmış
- Seviye: 🟢 Düşük
- Kanıt türü: KOD OKUMASI
- Nerede: `frontend:src/data.ts:4018-4066` (fiyat kartı özellik matrisi, "LCV — maksimum 100 kişi") · `frontend:src/stores/useSubscriptionStore.ts:27-28` (`getRequiredTier`) · `frontend:src/data.ts` (32 `minimumTier`) ↔ `backend:config/davetkart.php` (`tiers.*.rsvp_limit`, `module_tiers`, `preset_tiers`, `branding.white_label_tier`)
- Senaryo: 1) Fiyat backend'den okunuyor (K128). 2) "Hangi planda ne var" ise frontend'de sabit: galeri ve hediye Elit, zarf ve zaman çizelgesi Gold, LCV sınırı 100. 3) Backend'de `show_gallery` Gold'a indirilirse fiyat kartı ve editör eski kuralı göstermeye devam eder; sunucu doğru davranır, arayüz yanlış söz verir.
- Kanıt: Bugün iki taraf **aynı**: `FE-d1-metrics.txt` §5 (`frontend'de premium, backend'de değil: (yok)` · tersi `(yok)`), özellik matrisi `module_tiers` ile satır satır karşılaştırıldı (R8).
- Etki: Bugün yok. Sunucu her durumda son sözü söylüyor (`requiredTier` hata parametresinden okunuyor, `useSubscriptionStore.ts:78-81`); risk yalnızca yanıltıcı arayüz.
- Neden önemli (öğretici not): Fiyat için kurulan "tek kaynak" ilkesi, fiyatın anlamını veren kurallara uzatılmamış. Kopyalanan kural iki yerde değiştirilmek zorundadır ve bunu hatırlatan bir şey yoktur; hata kodlarında bu sorun `contracts/error-codes.json` + `verify:errors` ile çözülmüştü.
- Öneri: `GET /public/plans` yanıtına plan başına `rsvpLimit`, `modules` ve `whiteLabel` ekle; ya da `contracts/plan-rules.json` + `verify:plans` betiği (hata sözleşmesiyle aynı desen).
- Test önerisi: `verify:plans`: frontend matrisi ↔ sözleşme dosyası. Öldürmesi gereken mutant: `data.ts`'te Gold'un galeri satırını `included: true` yapmak.
- Efor: M
- İlgili: K128 · R8 · R16

### FE-06 404 sayfası yok; bilinmeyen adres ana sayfaya atıyor
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:src/App.tsx:126` (`{ path: '*', element: <Navigate to="/" replace /> }`) · `frontend:src/App.tsx:84` (`/hesap/*` → `/hesap`)
- Senaryo: Kullanıcı yanlış yazılmış ya da eskimiş bir bağlantıya tıklar (`/fiyatlar`, `/davet/abc`) → hiçbir açıklama olmadan ana sayfaya düşer.
- Kanıt: Yolculuk 8: `/olmayan-sayfa` → `/` (`evidence/commands/E2E-J8-notfound.json`, `screenshots/J8-404-1440.png`). Misafir yolu ayrı: olmayan davetiye için "Bu davetiye bulunamadı" metni çiziliyor.
- Etki: Kullanıcı hatanın kendisinde mi sitede mi olduğunu anlayamaz; arama motorları her bilinmeyen adresi ana sayfanın kopyası sayar (soft 404).
- Neden önemli (öğretici not): Yönlendirme bir cevaptır: "aradığın şey burada". Yanlış adrese verilecek dürüst cevap "bulunamadı"dır.
- Öneri: `NotFoundPage` (başlık, ana sayfa ve panel bağlantısı); `*` rotası onu çizsin. Misafir yolu `/invite/:id` için ayrı metin ("Bu davetiye yayında değil").
- Test önerisi: `verify:render`: bilinmeyen yol `NotFoundPage` çiziyor.
- Efor: S
- İlgili: yolculuk 8

### FE-07 `README.md` boş; `CLAUDE.md` kodla çelişiyor
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:README.md` (0 satır) · `frontend:CLAUDE.md:9` ("AI Integration: Google GenAI (`@google/genai`)") · `frontend:CLAUDE.md:43` ("Strict TypeScript") · `frontend:vite.config.ts:15-18` (AI Studio kalıntısı yorum, bozuk karakter)
- Senaryo: Depoya yeni giren kişi ya da asistan `CLAUDE.md`'yi okur: AI çağrısının frontend'den yapıldığını ve TypeScript'in katı kipte olduğunu sanır. İkisi de yanlış (`package.json`'da `@google/genai` yok, asistan `POST /assistant/chat` ile backend'den gidiyor; `tsconfig` katı değil).
- Kanıt: `wc -l README.md` → 0 · `FE-d1-metrics.txt` §0 (bağımlılık listesi) · `grep genai src scripts` → boş.
- Etki: Yanlış yönlendirilmiş bir asistan frontend'e AI anahtarı eklemeye çalışabilir; bu, projenin en önemli güvenlik kuralının (anahtar frontend'e inmez) tersidir.
- Neden önemli (öğretici not): Asistanlar için yazılmış kural dosyası koddur; eskidiğinde sessizce yanlış davranış üretir. Kodda karşılığı olmayan açıklama, açıklama değildir (projenin kendi B4 kuralı).
- Öneri: `README.md`: kurulum, `npm run check`, ortam değişkenleri, backend'le ilişki. `CLAUDE.md`: GenAI satırını "asistan backend üzerinden" diye düzelt, `verify` betiklerini ve "fiyat frontend'de durmaz" kuralını ekle.
- Test önerisi: —
- Efor: S
- İlgili: `ARC-05` (backend'deki doküman kayması)

### FE-08 Konum araması: backend ucu olmayan, bayrakla kapalı kod
- Seviye: 🟢 Düşük
- Kanıt türü: KOD OKUMASI
- Nerede: `frontend:src/services/places.ts:22-24` · `frontend:src/hooks/usePlaceSearch.ts` · `frontend:src/components/create/location/LocationSearchField.tsx` · backend'de `places` rotası yok
- Senaryo: `VITE_PLACES_SEARCH_ENABLED=true` yapılırsa editördeki konum alanı her tuşta `GET /api/public/places/search`'e gider ve 404 alır.
- Kanıt: `FE-d1-metrics.txt` §1: `YOK GET /public/places/search`; `grep places backend/routes backend/app/Http/Controllers` → boş. Bayrak kapalıyken servis ağa çıkmıyor (`places.ts:66-68`).
- Etki: Bugün yok. Üç dosyalık, sözleşmesi tek tarafta duran yarım özellik.
- Neden önemli (öğretici not): Bayrakla kapatılmış kod, karar verilmemiş bir karardır. Uzun yaşayan bayrak ölü kodun en pahalı türüdür: derlenir, bakımı yapılır, ama kimse çalıştırmaz.
- Öneri: Karar ver: backend ucunu yaz (Places anahtarı sunucuda, önbellek, `throttle`) ya da üç dosyayı kaldırıp "haritadan seç" akışını tek yol yap.
- Test önerisi: Uç yazılırsa `verify:endpoints`'e satır.
- Efor: S (kaldırma) · L (uç)
- İlgili: `docs/rehber/src/services/places.md`

### FE-09 95 MB video depoda ve önbellek başlığı olmadan sunuluyor
- Seviye: 🟢 Düşük
- Kanıt türü: KOD OKUMASI
- Nerede: `frontend:public/videos/` (126 dosya, 90 MB) · `backend:deploy/nginx/davetkart.conf` (`Cache-Control` yalnızca `/assets/` ve `/index.html` için)
- Senaryo: 1) Premium şablonların arka plan videoları `public/` altında; Vite bunları ad değiştirmeden `dist/`'e kopyalar (hash yok). 2) Nginx `/videos/…` için `Cache-Control` göndermez; tarayıcı sezgisel önbellek kullanır. 3) Aynı adla değiştirilen bir video eski hâliyle görünmeye devam edebilir; öte yandan `immutable` de denemez çünkü adlar sabit.
- Kanıt: `du -sh public` → 95M; `find dist -type f` → 63 `.mp4` + 63 `.webm`, en büyüğü 2,4 MB. Nginx dosyasında `/videos/` ya da `/images/` bloğu yok.
- Etki: Depo her video değişikliğinde kalıcı olarak büyür; misafir sayfasının en ağır varlığı için önbellek davranışı tanımsız.
- Neden önemli (öğretici not): Uzun önbellek ancak **içerik adresli** (adında hash olan) dosyada güvenlidir. Sabit adlı dosyada iki kötü seçenek kalır: kısa önbellek (yavaş) ya da uzun önbellek (bayat).
- Öneri: Kısa vade: Nginx'e `location ^~ /videos/ { add_header Cache-Control "public, max-age=604800"; }`. Sağlam: videoları `src/` altından içe aktar (Vite hash'ler) ya da nesne deposuna sürüm önekiyle yükle; depodan çıkar.
- Test önerisi: —
- Efor: M
- İlgili: `OPS-01` (yayın) · `SEC-04` (aynı Nginx dosyası)

### FE-10 Ana giriş paketi 1,64 MB: 299 şablon her sayfaya, misafir sayfasına bile yükleniyor
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:src/components/templates/TemplateRenderer.tsx:2-88` (dokuz kategori barrel'ının statik içe aktarımı) · içe aktaranlar: `src/components/preview/DeviceSimulator.tsx:5` (ana sayfa, `HomePage` → `PreviewSection`) ve `src/pages/InvitePage.tsx:4` · `frontend:src/data.ts` (4188 satır, 373 şablon kaydı + kapak görseli içe aktarımları)
- Senaryo: 1) Misafir WhatsApp'tan gelen bağlantıya telefonundan tıklar. 2) Tarayıcı tek bir davetiyeyi çizmek için ana giriş paketini (1 637,83 kB, gzip 442,06 kB) ve tek stil dosyasını (1 171,53 kB, gzip 132,84 kB) indirir. 3) Paketin içinde tembel olmayan 299 şablonun hepsi var; misafirin göreceği şablon bunlardan biri. 4) Aynı paket ana sayfada, giriş sayfasında ve panelde de yüklenir.
- Kanıt: `evidence/commands/TST-npm-run-check.txt`: `dist/assets/index-DfFic9Bg.js 1,637.83 kB │ gzip: 442.06 kB`, `dist/assets/index-B4g3laWs.css 1,171.53 kB │ gzip: 132.84 kB`, Vite uyarısı "Some chunks are larger than 500 kB". `dist/index.html` yalnızca bu iki dosyaya bağlanıyor. Şablon sayısı: 373 kayıt − 74 tembel = 299. Üçüncü büyük parça `SceneCanvas` (three.js, 886,61 kB, gzip 239,71 kB) yalnızca dört 3B şablonda yükleniyor.
- Etki: Misafir sayfasının ilk yüklemesi yaklaşık 575 kB sıkıştırılmış kod ve stil; orta sınıf bir telefonda 1,6 MB JavaScript'in ayrıştırılması saniyeler alır (ölçüm: kısıtlı mobil koşulda misafir sayfası LCP 4,45 sn, bkz. `FE-53` ve performans tablosu). Ürünün en çok açılan sayfası en ağır sayfası.
- Neden önemli (öğretici not): Kod bölme, **içe aktarım grafiğini** izler. `React.lazy` ile ayrılmış bir sayfa (`InvitePage`), statik yüklenen başka bir sayfanın (`HomePage`) da içe aktardığı bir modüle bağlıysa o modül ana pakete düşer; tembellik kâğıt üstünde kalır. Faz 15–17'nin 74 şablonu doğru desenle (`lazyPresets.ts`) eklenmiş; eski 299 şablon barrel dosyaları üzerinden statik.
- Öneri: 1) `TemplateRenderer`'daki dokuz barrel içe aktarımını `lazyPresets.ts` desenine taşı: şablon kimliği → `lazy(() => import(...))` haritası; misafir yalnızca kendi şablonunu indirir. 2) Ana sayfadaki önizlemeyi (`DeviceSimulator`) `DeferredSection` içinde tembel yükle. 3) `data.ts`'i katalog verisi (metin) ve kapak görseli içe aktarımları olarak ikiye böl. 4) CSS için ikinci adım: şablon stillerinin ana dosyadan ayrılması.
- Test önerisi: `npm run check`'e paket bütçesi: ana giriş 400 kB (ham) üstündeyse kırmızı. Öldürmesi gereken mutant: `TemplateRenderer`'a bir şablonun statik içe aktarımını geri eklemek.
- Efor: M
- İlgili: Faz 15–17 (`lazyPresets.ts`) · `FE-09`

### FE-50 Sihirbaz her ziyarette sunucuda boş taslak açıyor; yenilemede editör kayboluyor
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:src/hooks/useInvitationAutoSave.ts` (her `editRevision` değişikliğinde 1,5 sn sonra kayıt) · `frontend:src/App.tsx:43` (`/create` adresi davetiye kimliği taşımıyor) · backend: kullanıcı başına davetiye sınırı yok (`grep -rniE "max_invitations|invitation_limit|max_drafts" config app` → boş)
- Senaryo: 1) Girişli kullanıcı "Davetiye Tasarla"ya girer, bir kategoriye ve bir temaya tıklar, vazgeçer. 2) Otomatik kaydetme bu iki tıklamayı "düzenleme" sayar ve `POST /api/invitations` ile adsız bir taslak açar. 3) Kullanıcı üç kez göz atarsa panelinde üç boş "Düğün" taslağı birikir. 4) Editördeyken sayfayı yenilerse (ya da telefon sekmeyi bellekten atarsa) `/create` 1. adımdan açılır; taslak sunucudadır ama ekranda değildir. 5) Kullanıcı baştan başlar ve bir taslak daha açılır.
- Kanıt: `evidence/commands/E2E-J2-create.json` (`api`: `201 POST /api/invitations` "Davetiyeni Oluştur"a basılmadan önce; "Sayfa yenilendi" adımı `valueKept:false`) · `screenshots/J2-panel-taslaklar-1440.png` (bir gerçek, üç adsız taslak; üçü bu denetimin keşif koşularından) · `screenshots/J2-editor-390.png` (yenileme sonrası "ADIM 1 / 3")
- Etki: Panel kullanıcının açtığını bilmediği taslaklarla dolar; yenileme "işim kayboldu" izlenimi verir (kaybolmadı, panelde "Düzenlemeye Devam Et" ile açılıyor). Sunucuda sınırsız satır: tek hesap API hız sınırı içinde binlerce taslak açabilir.
- Neden önemli (öğretici not): Otomatik kaydetme iki soruya cevap vermek zorunda: **ne zaman** kayıt açılır ve kayıt **nerede** bulunur. Kayıt, kullanıcının "bir şey yaptım" dediği anda (ilk gerçek içerik) açılmalı; kimliği de adreste durmalı ki yenileme, geri tuşu ve bağlantı paylaşımı aynı belgeye dönsün. Adres, tek sayfa uygulamasının en dayanıklı durum deposudur.
- Öneri: 1) İlk `POST`'u kategori/tema seçimine değil ilk metin alanına (ad, tarih, konum) ya da "Davetiyeni Oluştur"a bağla. 2) Kayıt açılınca adresi `/create/<id>` yap (`navigate(..., { replace: true })`); `/create/:id` açılışta `GET /invitations/{id}` ile yüklesin. 3) Backend'de kullanıcı başına taslak tavanı (ör. 50) ve yeni hata kodu.
- Test önerisi: `verify:state`: "yalnızca kategori ve tema seçimi kayıt isteği üretmez". Backend: `InvitationTest::a_user_cannot_keep_more_than_the_draft_limit`. Öldürmesi gereken mutant: tavan koşulunu kaldırmak.
- Efor: M
- İlgili: `ARC-09` (checkout'ta aynı desen: her çağrı yeni kayıt)

### FE-51 Misafir fotoğraf/video yüklemesine arayüzden ulaşılamıyor
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:src/pages/InvitePage.tsx:123-127` (`onRsvpClick={() => setRsvpModalOpen(true)}`) · `frontend:src/components/preview/RsvpModal.tsx:177-188` (tek fotoğraf/video girişi) · `frontend:src/components/templates/` (`onRsvpClick` yalnızca `TemplateRenderer.tsx` ve `types.ts`'te geçiyor; hiçbir şablon çağırmıyor)
- Senaryo: 1) Misafir davetiyeyi açar, LCV'sini şablonun içindeki satır içi formla gönderir. 2) Satır içi formda dosya alanı yok. 3) Dosya alanı olan `RsvpModal` yalnızca `onRsvpClick` çağrılınca açılır ve bu işlevi çağıran şablon kalmamış. 4) `POST /api/public/invitations/{id}/media` ucu ise açık ve kimliksiz.
- Kanıt: `grep -rl onRsvpClick src/components/templates` → 2 dosya (`TemplateRenderer.tsx`, `types.ts`) · `evidence/commands/E2E-J5-guest-rsvp.json` (misafir sayfası dökümü: girişler `#rsvp-name`, `#rsvp-menu`, bal küpü alanı; dosya girişi yok) · `screenshots/J5-lcv-bos-390.png`
- Etki: "Misafirler fotoğraf yükleyebilir" özelliği ürün yüzeyinde yok; arkasındaki uç, depolama kotası ve temizleme işi (`SEC-08`: davetiye başına 5 GB) çalışıyor. Yani risk var, fayda yok. Yolculuk 5'in "fotoğraf yükle" adımı bu yüzden arayüzden koşturulamadı.
- Neden önemli (öğretici not): Kullanılmayan bir uç da bir saldırı yüzeyidir. Bir özelliğin arayüzü kaldırıldığında sunucu tarafı da ya kaldırılmalı ya da bayrakla kapatılmalı; "nasılsa kimse çağırmıyor" yalnızca dürüst kullanıcılar için doğrudur.
- Öneri: Karar ver. Özellik isteniyorsa: yüklemeyi satır içi forma (`templates/shared/RSVPForm.tsx`) taşı, `RsvpModal`'ı kaldır. İstenmiyorsa: `RsvpModal`, `useRsvpStore` medya kolu ve `mediaService.uploadAsGuest` ile birlikte misafir yükleme ucunu config bayrağıyla kapat.
- Test önerisi: `verify:render`: "LCV formu, medya açıkken dosya alanı çiziyor". Backend: bayrak kapalıyken `MediaTest::guest_upload_is_refused_when_disabled`.
- Efor: M
- İlgili: `SEC-08` · R9

### FE-52 Fiyat sayfası SSS'si backend'de olmayan "yayın süresi" ve ücretli uzatmayı anlatıyor
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `frontend:src/pages/PricingPage.tsx:41` ("davetiyeniz paketinizin yayın süresi boyunca yayında kalır") · `:48-49` ("Yayın süresi sonunda davetiyeniz erişime kapanır… Dilerseniz küçük bir ücretle yayın sürenizi uzatabilirsiniz")
- Senaryo: 1) Müşteri satın almadan önce SSS'yi okur: paketin bir yayın süresi var, bitince davetiye kapanıyor, ücretle uzatılıyor. 2) Backend'de yayınlanmış davetiyenin süresi, kapanma tarihi ya da uzatma siparişi diye bir kavram yok. 3) Müşteri "süre ne kadar?" diye sorduğunda verilecek bir cevap yok; hiçbir sayfada süre yazmıyor.
- Kanıt: `grep -rnEi "published_until|publish_until|unpublish|publication_days|publish_duration|extend" backend/app backend/config backend/database/migrations backend/routes` → yalnızca iade sonrası yayından kaldırma günlüğü (`HandlePaymentCallbackAction.php:156`); süre alanı ya da uzatma ucu yok. Tek zaman kuralı misafir verisinin etkinlikten 6 ay sonra silinmesi (`data:purge`).
- Etki: Satış öncesi bilgilendirme gerçek hizmetle uyuşmuyor. Bugün müşterinin lehine (davetiye süresiz yayında), ama "ücretli uzatma" yazılı bir vaat ve ileride süre konursa bugünkü alıcılar için tartışma konusu. Mesafeli satışta ön bilgilendirmenin doğruluğu hukuki bir konudur (hukuki değerlendirme bu denetimin kapsamı dışında).
- Neden önemli (öğretici not): R8'in özü: fiyat sayfası bir **sözleşme taslağıdır**. Özellik matrisi kodla karşılaştırılıp düzeltilmiş (`FE-05`), SSS metni atlanmış. Metinler de kural taşır ve onların testi yoktur; o yüzden kural değiştiğinde ilk eskiyen onlardır.
- Öneri: Önce karar: yayın süresi olacak mı? Olmayacaksa iki cevabı gerçeğe göre yaz ("Davetiyeniz yayında kalır; misafir yanıtları etkinlikten 6 ay sonra silinir"). Olacaksa süre, kapanma ve uzatma backend'de kural olarak yazılana kadar metni kaldır.
- Test önerisi: `verify:render`'daki gizlilik metni denetiminin benzeri: SSS'de "yayın süresi" geçiyorsa backend config'inde karşılığı olmalı.
- Efor: S
- İlgili: R8 · K98 (saklama süreleri)

### FE-53 Kısıtlı mobil koşulda LCP 3,9–5,7 sn; giriş ve fiyat sayfalarında CLS 0,33–0,63
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: ana sayfa, misafir sayfası, giriş, fiyatlar (üretim build'i) · kök nedenler: `FE-10` (ana paket), `frontend:src/index.css:1` (Google Fonts `@import`), fiyat kartlarının API yanıtından sonra çizilmesi
- Senaryo: Orta sınıf bir telefon ve zayıf mobil bağlantı (CPU 4× yavaş, 1,6 Mbps, 150 ms gecikme) ile sayfa ilk kez açılır.
- Kanıt: `evidence/commands/E2E-perf.json` (üç koşunun ortancası): ana sayfa LCP 5 680 ms · CLS 0,182 · TBT 797 ms · 1 542 kB; misafir sayfası LCP 4 452 ms · CLS 0 · TBT 267 ms · 922 kB; giriş LCP 3 940 ms · CLS 0,329; fiyatlar LCP 5 180 ms · CLS 0,625. Kısıtsız koşulda dört sayfa da LCP < 1 sn, CLS 0. Eşikler (Core Web Vitals): LCP iyi ≤ 2,5 sn, kötü > 4 sn; CLS iyi ≤ 0,1, kötü > 0,25.
- Etki: Misafirlerin çoğu davetiyeyi telefondan, mobil veriyle açar; ilk içerik 4,5 saniyede geliyor. Giriş ve fiyat sayfalarında içerik yüklenirken zıplıyor (yanlış yere dokunma). Laboratuvar ölçümüdür; gerçek kullanıcı verisi değildir.
- Neden önemli (öğretici not): Kısıtsız ölçümde her şey iyi görünür; fark **yavaş koşulda** ortaya çıkar çünkü darboğaz ağ ve ayrıştırma süresidir. CLS'in yalnızca yavaş koşulda çıkması tipik bir işarettir: geç gelen font ve geç gelen veri, önceden yer ayrılmamış alanı iter.
- Öneri: 1) `FE-10` (paketi küçült). 2) Fontları kendi alan adından sun, `<link rel="preload">` ile ön yükle, `size-adjust` ile yedek fontu eşle (`SEC-12` ile aynı iş). 3) Fiyat kartlarına ve giriş kartına sabit en küçük yükseklik ya da iskelet. 4) Ana sayfa videosunu (`hero-bg.mp4`) `preload="none"` + poster.
- Test önerisi: CI'da Lighthouse CI ya da bu betik (`evidence/scripts/e2e/perf-measure.mjs`) ile bütçe: misafir sayfası LCP < 3 sn, CLS < 0,1.
- Efor: M
- İlgili: `FE-10` · `FE-09` · `SEC-12`

### FE-54 Hata ve başarı mesajları ekran okuyucuya duyurulmuyor; alt bilgi ve fiyat kartında kontrast yetersiz
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:src/components/ui/Toast.tsx:51` (kapta `role`/`aria-live` yok) · `frontend:src/components/layout/Footer.tsx:33,40,51,62` (`text-emerald-100/50`) · fiyat kartındaki üstü çizili özellikler (`text-stone-400`) · misafir şablonlarında `<main>` yok
- Senaryo: 1) Ekran okuyucu kullanan kişi yanlış parola girer; "E-posta veya parola hatalı" bildirimi görsel olarak çıkar, okuyucuya duyurulmaz. 2) Az gören kullanıcı alt bilgideki bağlantıları ve fiyat kartında "bu planda yok" satırlarını okumakta zorlanır.
- Kanıt: `grep -nE "role=|aria-live" src/components/ui/Toast.tsx` → eşleşme yok. `evidence/commands/E2E-axe.json` (axe-core 4.10.3, 14 sayfa): kritik 0; `color-contrast` (ciddi, WCAG 1.4.3) 13 sayfada 196 öğe: alt bilgi bağlantıları 4,45:1 ve alt şerit 3,51:1 (gerekli 4,5:1), fiyat kartında üstü çizili satırlar 2,58:1; misafir sayfasında `landmark-one-main` ve `region` (21 öğe). Logodaki altın yazı (2,08:1) logotip istisnasına girer, sayılmadı.
- Etki: Hata mesajını duyamayan kullanıcı formun neden ilerlemediğini anlayamaz (WCAG 4.1.3). Kontrast ihlalleri her sayfada tekrarlanıyor çünkü ortak alt bilgiden geliyor; iki renk tonu değişince çoğu kapanır.
- Neden önemli (öğretici not): Görsel olarak beliren ama DOM'da "canlı bölge" olmayan içerik, yardımcı teknolojiler için hiç olmamış gibidir. Erişilebilirlik çoğu zaman yeni bileşen değil, mevcut bileşene iki öznitelik demektir.
- Öneri: Toast kabına `role="status" aria-live="polite"`, hata türündekilere `role="alert"`. Alt bilgide `text-emerald-100/50` → `/70`; alt şeritte bir ton açık renk; fiyat kartında `text-stone-400` → `text-stone-500`. Şablon köküne `<main>`.
- Test önerisi: CI'da axe taraması (`evidence/scripts/e2e/axe-scan.mjs` taşınabilir): `color-contrast` ihlali sıfır.
- Efor: S
- İlgili: WCAG 2.1 AA 1.4.3, 4.1.3

### FE-55 "Planlarım" fiyat sayfasından plan alınabileceğini söylüyor; orada satın alma düğmesi yok
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:src/pages/account/AccountPlansSection.tsx:45` · `frontend:src/pages/PricingPage.tsx` (üç kartta yalnızca "Tasarlamaya Başla → /create") · `frontend:src/utils/checkoutRoute.ts` (`checkoutHref` yalnızca plan duvarından ve dönüş sayfasından çağrılıyor)
- Senaryo: Kullanıcı "Planlarım"daki "Planları gör"e tıklar, fiyat sayfasına gelir; plan satın alacak bir düğme bulamaz. Davetiyeye bağlı olmayan paket alımı (`POST /payments/checkout`) yalnızca adres çubuğuna `/odeme?tier=standart` yazılarak yapılabiliyor.
- Kanıt: `evidence/commands/E2E-J6-package-refund.json`: fiyat sayfası dökümünde üç bağlantı da `/create`; `/odeme?tier=standart` doğrudan açılınca sipariş 201, ödeme sonrası "Planınız tanımlandı", `screenshots/J6-planlarim-hak-1440.png`.
- Etki: Çalışan bir satın alma yolu arayüzde yok; metin olmayan bir yolu tarif ediyor.
- Neden önemli (öğretici not): Uçtan uca test, tek tek doğru çalışan parçaların **birbirine bağlanmadığını** gösterir: uç var, sayfa var, aradaki bağlantı yok.
- Öneri: Girişli kullanıcı için fiyat kartlarına "Bu planı satın al" (`checkoutHref({ tier })`); ya da metni "davetiyenizi yayınlarken" ile sınırla.
- Test önerisi: `verify:render`: girişli kullanıcıda fiyat kartı `/odeme?tier=…` bağlantısı çiziyor.
- Efor: S
- İlgili: R13 (paket alımı), K133

### FE-56 `dugun-gul-3d` "hareketi azalt" tercihinde hareket etmeye devam ediyor
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:src/components/templates/dugun/DugunGul3d/`
- Senaryo: İşletim sisteminde "hareketi azalt" açık olan misafir bu şablonla hazırlanmış davetiyeyi açar; 3B sahne dönmeye devam eder.
- Kanıt: `evidence/commands/E2E-J7-templates.json`: 17 şablondan 16'sında `reduced.moving:false`, yalnızca `dugun-gul-3d`'de `true` (700 ms arayla alınan iki ekran görüntüsü farklı; 2 sonsuz animasyon 0'a inmiş ama tuval çizimi sürüyor).
- Etki: Tek şablon; hareket duyarlılığı olan kullanıcı için rahatsız edici olabilir (WCAG 2.3.3, AAA düzeyi).
- Neden önemli (öğretici not): `MotionConfig reducedMotion="user"` yalnızca Motion kütüphanesinin animasyonlarını durdurur; `requestAnimationFrame` ile dönen bir WebGL sahnesi bunu bilmez. Her animasyon kaynağı tercihi kendisi okumalı.
- Öneri: Sahnede `useReducedMotion()` true ise döngüyü durdur, tek kare çiz (diğer 3B şablonlar, ör. `dugun-kelebek`, bunu yapıyor).
- Test önerisi: `j7-templates.mjs` benzeri bir `verify` adımı: indirgenmiş harekette iki kare aynı.
- Efor: S
- İlgili: Faz 15

### FE-58 Ödeme dönüşünde davetiye kullanıcı onayı olmadan yayınlanıyor; K67 ile çelişki sorusu açık
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:src/hooks/useAutoPublish.ts` (sipariş `paid` ve davetiyeye bağlıysa `publishInvitation` çağrısı) · `frontend:src/pages/PaymentReturnPage.tsx:112` · karar: `davetkart-docs/decisions/DECISION-INDEX.md:79` (K67: "Ödeme yayınlamaz; yayın ayrı bir kullanıcı eylemidir", "⚠️ frontend 11.6 ile çelişki sorusu açık")
- Senaryo: 1) Kullanıcı editörde "Tasarımını Yayınla"ya basar, plan duvarından ödemeye geçer. 2) Ödeme onaylanır. 3) Dönüş sayfası hiçbir düğmeye basılmadan `POST /invitations/{id}/publish` gönderir; davetiye yayındadır.
- Kanıt: `evidence/commands/E2E-J3-checkout.json`: `webhook:paid` adımından sonraki bekleme satırında `200 POST /api/invitations/…/publish` (arada tıklama yok); `screenshots/J3-donus-yayinlandi-1440.png` ("Davetiyeniz yayında").
- Etki: Bu akışta kullanıcı yayınlamayı zaten istemişti; davranış makul. Risk iki uçta: ödeme sayfasına geri dönüp tasarımı değiştirmek isteyen kullanıcı (yayın ve üç günlük serbest bırakma penceresi başlamış olur) ve karar kaydının kodla çelişmesi. Sunucu K67'ye uyuyor: ödeme bildirimi tek başına yayınlamıyor.
- Neden önemli (öğretici not): Karar kaydındaki ⚠️ işareti "bunu sonra konuşalım" demektir ve kod o konuşmayı beklemez. Açık bırakılan karar, kodun fiilen verdiği karar olur; kaydı güncellemek kodu değiştirmekten ucuzdur.
- Öneri: Kararı kapat. Otomatik yayın isteniyorsa K67'yi "ödeme **sunucuda** yayınlamaz; frontend, yayın niyetiyle başlayan ödemenin dönüşünde yayınlar" diye daralt ve yeni K numarasıyla kaydet. İstenmiyorsa dönüş sayfasında "Şimdi yayınla" düğmesi.
- Test önerisi: `verify:payment`: "davetiyeye bağlı ödenmiş sipariş dönüşte yayın isteği üretir" (seçilen davranışı kilitler).
- Efor: S
- İlgili: K67 · `ARC-01` (karar indeksi) · R3

### FE-57 Küçük arayüz pürüzleri: düşen oturumda açıklama yok, yığılan hata bildirimleri, eski ipucu metni
- Seviye: 💡 Öneri
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:src/services/api.ts:178-191` (401 → `logout()`, bildirim yok) · `frontend:src/components/ui/Toast.tsx` (aynı mesaj üst üste) · `frontend:src/components/rsvp/LiveRsvpPanel.tsx:261` ("Yukarıdaki telefon önizlemesinden…")
- Senaryo: A) Oturumu sunucuda düşmüş kullanıcı bir sayfaya gider; açıklama görmeden giriş sayfasına düşer (girişten sonra kaldığı sayfaya dönüyor, bu iyi). B) Üç kez yanlış parola giren kullanıcı üç ayrı bildirimi üst üste görür; bildirimler giriş kartının altındaki "Kayıt olun" satırını örter. C) Paneldeki ipucu, panelde bulunmayan bir "telefon önizlemesi"nden söz ediyor.
- Kanıt: `evidence/commands/E2E-J8-expired-session.json` (`toast: []`, yol `/login`, girişten sonra `/hesap/planlarim`) · `screenshots/J1-hiz-siniri-1440.png` (üç bildirim) · `evidence/commands/E2E-J5-owner-panel.json` (panel metni).
- Etki: Kozmetik; güven duygusunu etkiler.
- Neden önemli (öğretici not): Sessiz yönlendirme kullanıcıya "ne oldu" sorusunu sordurur. Sistem kullanıcı adına bir karar verdiğinde (oturumu kapatmak) bunu söylemelidir.
- Öneri: A) Yönlendirirken `state: { reason: 'expired' }` ve girişte tek satır "Oturumunuz sona erdi". B) Aynı metinli bildirimi yenilemek yerine süresini uzat. C) Metni panele göre yaz ya da kaldır.
- Test önerisi: —
- Efor: S
- İlgili: yolculuk 1, 5, 8

## Tablolar

### Sözleşme tablosu (rapor §9)

Kaynak: `evidence/commands/FE-d1-metrics.txt` §1 (frontend çağrıları `src/services/` içinden elle çıkarıldı,
backend tarafı `evidence/commands/FE-route-list.json`). ✅ = aynı fiil ve yol backend'de var.

| Uç | Frontend çağrısı | Kimlik | Durum |
|---|---|---|---|
| `GET /account/entitlements` | `services/account.ts:50` | auth | ✅ |
| `POST` · `DELETE /orders/{id}/refund-request` | `services/account.ts:61,66` | auth | ✅ |
| `PATCH /auth/me` · `PUT /auth/password` | `services/account.ts:71,79` | auth | ✅ |
| `POST /auth/email-change` | `services/account.ts:87` | auth | ✅ |
| `POST /public/email-change/confirm` | `services/account.ts:99` | public | ✅ |
| `GET` · `DELETE /auth/sessions` · `DELETE /auth/sessions/{id}` | `services/account.ts:103,114,110` | auth | ✅ |
| `POST /assistant/chat` | `services/assistant.ts:41` | auth | ✅ |
| `POST /auth/login` · `/auth/register` | `services/auth.ts:89,94` | public | ✅ |
| `POST /auth/logout` · `GET` · `DELETE /auth/me` | `services/auth.ts:101,111,131` | auth | ✅ |
| `POST /auth/forgot-password` · `/auth/reset-password` | `services/auth.ts:122,126` | public | ✅ |
| `POST /public/contact` | `services/contact.ts:37` | public | ✅ |
| `GET` · `POST /invitations` | `services/invitations.ts:111,122` | auth | ✅ |
| `GET` · `PUT` · `DELETE /invitations/{id}` | `services/invitations.ts:117,127,154` | auth | ✅ |
| `POST /invitations/{id}/publish` | `services/invitations.ts:148` | auth | ✅ |
| `POST /invitations/{id}/media` · `DELETE …/media/{mediaId}` | `services/media.ts:147,155` | auth | ✅ |
| `POST /public/invitations/{id}/media` | `services/media.ts:151` | public | ✅ |
| `POST /invitations/{id}/checkout` · `POST /payments/checkout` | `services/payments.ts:153,159` | auth | ✅ |
| `POST /gift-codes/preview` | `services/payments.ts:169` | auth | ✅ |
| `GET /orders` · `GET /orders/{id}` | `services/payments.ts:195,189` | auth | ✅ |
| `GET /public/plans` | `services/pricing.ts:97` | public | ✅ |
| `GET /pricing` | `services/pricing.ts:103` | auth | ✅ |
| `GET /invitations/{id}/rsvps` | `services/rsvps.ts:55` | auth | ✅ |
| `POST /public/invitations/{id}/rsvps` · `PUT …/rsvps/{rsvpId}` | `services/rsvps.ts:68,89` | public | ✅ |
| `DELETE /rsvps/{id}` | `services/rsvps.ts:97` | auth | ✅ |
| `GET /public/invitations/{id}` | `services/publicInvitation.ts:106` | public | ✅ |
| `GET /public/places/search` | `services/places.ts:24` | public | ❌ backend'de yok; bayrakla kapalı (`FE-08`) |
| `GET /ping` | — | public | frontend çağırmıyor (sağlık ucu) |
| `POST /public/payments/webhook` · `…/shopier/callback` · `…/shopier/osb` | — | public | frontend çağırmıyor (sağlayıcı çağırır) |

Toplam: frontend 41 çağrı · eşleşen 40 · backend 44 API rotası · frontend'in çağırmadığı 4 (beklenen).

### Tip ↔ Resource ve enum eşleşmesi

| Denetim | Sonuç | Kanıt |
|---|---|---|
| 16 Resource'un `toArray` anahtarları frontend çekirdeğinde geçiyor mu | 170 alanın hepsi geçiyor; `snake_case` anahtar yok | bu dosyanın "Koşturulan komutlar" bölümündeki döngü |
| 8 enum'un değerleri (`OrderStatus`, `SubscriptionTier`, `InvitationStatus`, `RefundBlocker`, `RefundRequestStatus`, `PaymentMethod`, `MediaKind`, `RsvpStatus`) | hepsi frontend tiplerinde var | aynı |
| Hata kodları (`contracts/error-codes.json`) | 28 kod, iki depoda anlamsal olarak aynı | `evidence/commands/FE-error-codes-compare.txt` |
| Premium şablon listesi | frontend 32 `minimumTier` = backend 32 `preset_tiers`, plan farkı yok | `FE-d1-metrics.txt` §5 |

Sınır: bu denetim "backend'in gönderdiği alan frontend'de okunuyor mu" yönündedir. Ters yön (frontend'in
beklediği ama backend'in göndermediği alan) için `verify:endpoints` ve D2 yolculukları kanıttır.

### i18n anahtar kümeleri

| Dil | `translation.json` anahtarı | `en`'e göre eksik / fazla | `errors.json` |
|---|---|---|---|
| en, tr | 72 | 0 / 0 | 184 anahtar, iki dilde aynı küme |
| es, fr, de, zh, hi, ar, ru, pt | 72 | 0 / 0 | yok (`fallbackLng: 'en'`) |

Kodda kullanılıp sözlükte olmayan anahtar: 0 (betiğin gösterdiği beş anahtar `errors` namespace'inde,
`utils/toDisplayError.ts:40-45,157,162`).

### Kütüphane sürümleri ve API kullanımı

| Kütüphane | Kurulu | Kullanım | Değerlendirme |
|---|---|---|---|
| React / React DOM | 19.2.7 | `createRoot`, `StrictMode`, `lazy`, `Suspense`; `forwardRef`, `defaultProps`, `propTypes`, `findDOMNode`: 0 | Kaldırılmış ya da eskimiş API yok |
| React Router (`react-router-dom`) | 7.18.5 | `createBrowserRouter` + `RouterProvider`, iç içe rotalar, `Navigate` | Doğru. `errorElement` yok (`FE-02`); v7'de `react-router` paketinden içe aktarım önerilir, `react-router-dom` hâlâ geçerli (resmî belgeye bakılmadı: **doğrulanamadı**) |
| Zustand | 5.0.14 | `create<T>()(…)`, seçicili okuma | Doğru; v5'in çift çağrılı tip kalıbı kullanılmış |
| i18next / react-i18next | 26.3.4 / 17.0.8 | `init` kaynakları gömülü, iki namespace, `LanguageDetector` | Doğru; kapsama `FE-01` |
| Vite | 6.4.5 | `defineConfig`, dev proxy, kaynak haritası kapalı | Doğru; `manualChunks` yok (`FE-10`) |
| TypeScript | 5.8.3 | `strict` kapalı | `FE-03` |

Context7 bağlı değildi; sürümler `node_modules/*/package.json`'dan okundu. API doğruluğu kaldırılmış API
taramasıyla (betik §4) ve kod okumasıyla değerlendirildi, resmî belgelerle satır satır karşılaştırılmadı.

### Şablon tablosu (Faz 15–17)

| Ölçü | Değer | Kanıt |
|---|---|---|
| `data.ts` şablon kaydı | 373 (`verify:render` "373 şablonun hepsinde") | `TST-npm-run-check.txt` |
| Tembel yüklenen şablon | 74 kayıt, 65 dinamik `import()` | `FE-d1-metrics.txt` §5 |
| Premium (Gold) şablon | 32, backend ile birebir | aynı |
| `TemplateRenderer.tsx` statik şablon içe aktarımı | 2 satır (kategori barrel'ları), 3 `Suspense` | aynı |
| Boş veride çizim | "boş veride çizim kırılmıyor" ✓ (74 tembel şablon) | `TST-npm-run-check.txt` |

### Yolculuk tablosu

Her satırın adım kaydı `evidence/commands/E2E-<ad>.json`, ekran görüntüleri `evidence/screenshots/` altında.
"Konsol/ağ" sütunu beklenmeyen hataları sayar; beklenen 401/402/404/422/429 yanıtları (ve tarayıcının bunlar
için yazdığı "Failed to load resource" satırları) beklenen sütununda belirtilmiştir.

| # | Yolculuk · adım | Beklenen | Gözlenen | Görünüm | Ekran görüntüsü | Beklenmeyen konsol / ağ hatası |
|---|---|---|---|---|---|---|
| 1 | Kayıt | 201, panele geçiş | 201 → `/dashboard`; boş gönderimde 4 alan tarayıcı doğrulamasında | 1440, 390 | `J1-kayit-form-*`, `J1-kayit-sonrasi-1440` | yok |
| 1 | Giriş → çıkış | 200; çıkışta token sunucuda iptal | 200 → `/dashboard`; çıkış 204, eski token `GET /auth/me` 401, `/dashboard` → `/login` | 1440 | `J1-giris-*`, `J1-cikis-sonrasi-1440` | çıkış anında panelin yoldaki iki isteği 401 (zararsız) |
| 1 | Hatalı parola | 401 `INVALID_CREDENTIALS`, formda kalır | 401, `/login`, e-posta alanı korunur, "E-posta veya parola hatalı. Kontrol edip tekrar deneyin." | 1440 | `J1-hatali-parola-1440` | yok |
| 1 | Hız sınırı | 5/dk sonrası 429 + `Retry-After` | 5. giriş isteğinde 429 `RATE_LIMITED`, `Retry-After: 45`, "Çok hızlı ilerliyorsunuz. 45 saniye sonra tekrar deneyin."; süre dolunca giriş 200 | 1440, 390 | `J1-hiz-siniri-*` | yok |
| 2 | Sihirbaz: Düğün → Zarif Sadelik → bilgiler | kayıt açılır, editör gelir | `201 POST /invitations` (otomatik kaydetme, düğmeden önce), editör "ADIM 3 / 3" | 1440 | `J2-kategori`, `J2-tema`, `J2-bilgiler`, `J2-editor` | yok |
| 2 | Otomatik kaydetme | alan değişince `PUT` 200 | konum değişti → `PUT` 200, sunucuda yeni değer | 1440 | `J2-editor-kayit-sonrasi-1440` | yok |
| 2 | Yenileme | editör aynı taslakla açılır | ❌ `/create` 1. adımdan açıldı (`FE-50`); panelde "Düzenlemeye Devam Et" ile taslak geri geliyor | 1440, 390 | `J2-editor-390`, `J2-panel-taslaklar-1440` | yok |
| 3 | Yayınla → plan duvarı | 402, önerilen plan Gold | `402 POST …/publish`; Standart "yetersiz", Gold 399 → 159,60 ₺ (ilk yayın %60) | 1440 | `J3-plan-duvari-1440` | yok |
| 3 | Ödeme: hediye kodu | önizleme, toplam düşer | `AUDYUZDE20`: −31,92 ₺ → toplam 127,68 ₺ (kod, otomatik indirimden sonra kalan tutara) | 1440, 390 | `J3-odeme-kod-1440`, `J3-odeme-390` | yok |
| 3 | Ödeme: onaysız gönderim | sipariş açılmaz | istek gitmedi (onay kutusu zorunlu) | 1440 | `J3-odeme-onaysiz-1440` | yok |
| 3 | Ödeme → dönüş → yayın | sipariş 201 → dönüş sayfası yoklar → `paid` → otomatik yayın | `201 POST …/checkout` → `/odeme/basarili?order=…` "Ödemeniz doğrulanıyor" → imzalı webhook 204 → `200 POST …/publish` → "Davetiyeniz yayında · ₺127,68"; kayıt `published`, `publishedAt` dolu | 1440, 390 | `J3-donus-dogrulaniyor-1440`, `J3-donus-yayinlandi-*` | yok |
| 4 | Yayındaki Gold davetiyede "Fotoğraf Galerisi" (Elit) | 402, modül açılmaz | `402 PUT /invitations/{id}` → "Mevcut planınız bu davetiyeye yetmiyor" (Elit ₺549); misafir ucunda `showGallery:false` | 1440 | `J4-moduller-once-1440`, `J4-galeri-acildi-1440` | yok |
| 5 | Misafir: zarf → davetiye | açılır, içerik doğru | zarf açıldı; adlar, tarih, mekân, geri sayım, program doğru | 390 | `J5-misafir-zarf-390`, `J5-misafir-acik-390` | yok |
| 5 | Misafir: LCV | 201, onay | 201, "Başarıyla katılımınız oluşturuldu", takvim düğmesi, makbuz `localStorage`'da | 390 | `J5-lcv-bos-390`, `J5-lcv-gonderildi-390` | yok |
| 5 | Misafir: fotoğraf yükle | dosya seçilir, yüklenir | ❌ arayüzde dosya alanı yok (`FE-51`); **koşmadı** | 390 | — | — |
| 5 | Sahip paneli | yanıt görünür | "KATILIYOR 3 kişi · Ayşe Demir · 3 Kişi • Et Menü" | 1440, 390 | `J5-panel-lcv-*` | yok |
| 5 | Aynı adla ikinci cihazdan yanıt | (gözlem) | 201; ikinci kayıt açıldı (kimliksiz misafirde beklenen davranış; aynı cihazdan gelen güncelleme yeni satır açmıyor: `02-security.md` P26) | 390 | — | yok |
| 6 | Hesap: genel, planlarım, siparişler | haklar ve dökümler doğru | Gold "Kullanımda" (iptal düğmesi yok); sipariş: ₺399 − ₺239,40 − ₺31,92 = ₺127,68 | 1440 | `J6-hesap-genel`, `J6-planlarim`, `J6-siparisler` | yok |
| 6 | Paket alımı (`/odeme?tier=standart`) | hak tanımlanır | 201 → ödeme → "Planınız tanımlandı" (₺249; ilk yayın indirimi artık yok) → Planlarım'da "İptal Et" | 1440 | `J6-paket-donus-1440`, `J6-planlarim-hak-1440` | yok |
| 6 | Hak iptali / iade talebi → geri çekme | talep açılır, hak donar; geri çekilince döner | "İptal talebi bekliyor", kullanılabilir hak 0; "Talebi Geri Çek" → 204 → "İptal Et" geri geldi | 1440, 390 | `J6-iptal-onay-1440`, `J6-iade-talebi-*` | yok |
| 6 | E-posta değişikliği | yanlış parola reddi; doğru parolada 202; bağlantı tek kullanımlık; oturumlar kapanır | yanlış parola 422 "Mevcut parola hatalı." (alanın altında); doğru 202; bağlantı 204 "E-posta adresiniz değişti"; eski token 401; bağlantı ikinci kez 422 "Bağlantı kullanılamadı"; eski adresle giriş 401, yenisiyle 200; oturum listesinde tek cihaz | 1440 | `J6-eposta-*`, `J6-oturumlar-1440` | bir koşuda düğme "Gönderiliyor…"da kaldı, iki tekrar koşuda yeniden üretilemedi (tek iş parçacıklı `artisan serve` olması muhtemel: VARSAYIM) |
| 6 | Hesap silme, parola değiştirme | — | **koşmadı** (arayüzden tamamlanmadı; yanlış mevcut parola API'de 422) | — | `J6-gizlilik-1440`, `J6-guvenlik-1440` | — |
| 7 | Faz 15–17 şablonları (17 şablon) | çizilir, hata yok; indirgenmiş harekette durur | 17/17 çizildi, konsol ve ağ hatası 0; 16/17 indirgenmiş harekette durdu (`FE-56`) | 390 | `J7-<şablon>-390`, dört şablonda `-azaltilmis-390` | yok |
| 8 | Dil: Arapça | arayüz çevrilir | `lang="ar" dir="rtl"`; üst menü Arapça, sayfa içeriği Türkçe (`FE-01`) | 1440, 390 | `J8-dil-menusu`, `J8-arapca-*` | yok |
| 8 | Bilinmeyen adres | 404 sayfası | `/olmayan-sayfa` → `/` (`FE-06`) | 1440 | `J8-404-1440` | yok |
| 8 | Olmayan / yayınlanmamış davetiye | "bulunamadı" | "Bu davetiye bulunamadı. Bağlantı hatalı olabilir ya da davetiye yayından kaldırılmış olabilir." (taslak ile olmayan ayırt edilemiyor) | 1440, 390 | `J8-davetiye-yok-*` | yok |
| 8 | Düşmüş oturum (geçersiz token) | girişe yönlenir, sonra geri döner | `GET /auth/me` 401 → oturum silindi → `/login` (açıklama yok, `FE-57`) → girişten sonra `/hesap/planlarim` | 1440 | `J8-oturum-dustu-1440` | geçersiz token'la gereksiz `POST /auth/logout` 401 |

### axe özeti (axe-core 4.10.3; WCAG 2.0/2.1 A + AA ve en iyi uygulamalar)

| Sayfa | Kritik | Ciddi | Orta | Kurallar (öğe sayısı) | Klavye: 25 Tab'da odak halkası olmayan / görünmeyen |
|---|---|---|---|---|---|
| Ana sayfa | 0 | 14 | 1 | `color-contrast` (14), `heading-order` (1) | 0 / 0 |
| Giriş · Kayıt · İletişim · Sihirbaz | 0 | 15 | 1 | `color-contrast` (15), `heading-order` (1) | 0 / 0 |
| Fiyatlar | 0 | 23 | 1 | `color-contrast` (23), `heading-order` (1) | 0 / 0 |
| Gizlilik | 0 | 28 | 1 | `color-contrast` (28), `landmark-unique` (1) | 0 / 0 |
| Panel | 0 | 16 | 1 | `color-contrast` (16), `heading-order` (1) | 0 / 0 |
| Ödeme · Hesap (güvenlik, planlarım) | 0 | 15 | 2 | `color-contrast` (15), `heading-order` (1), `landmark-complementary-is-top-level` (1) | 0 / 0 |
| Misafir sayfası (390) | 0 | 0 | 22 | `landmark-one-main` (1), `region` (21) | 0 / 0 |
| Ana sayfa (390) · Panel (390) | 0 | 4 · 6 | 1 | `color-contrast`, `heading-order` | 0 / 0 |

Kontrast ihlallerinin kaynağı: ortak alt bilgi (4,45:1 ve 3,51:1), logodaki altın yazı (2,08:1; logotip
istisnası), fiyat kartında üstü çizili satırlar (2,58:1). Klavye: denetlenen her sayfada ilk 25 odak durağının
hepsinde görünür odak halkası var. Elle bakılan ve axe'ın görmediği: bildirimlerin canlı bölge olmaması
(`FE-54`). Onay penceresi (`ConfirmDialog`) `role="dialog"`, `aria-modal`, `aria-labelledby` ve Escape
desteği taşıyor (kod okuması). Ekran okuyucuyla elle deneme **yapılmadı**.

### Performans tablosu (üretim build'i, gzip; 390×844; üç koşunun ortancası)

| Sayfa | Koşul | FCP | LCP | CLS | TBT | Aktarım (istek) |
|---|---|---|---|---|---|---|
| Ana sayfa | CPU 4× · 1,6 Mbps · 150 ms | 4 240 ms | **5 680 ms** | 0,182 | 797 ms | 1 542 kB (37): js 459 · css 132 · görsel 320 · video 202 · diğer 431 |
| Ana sayfa | kısıtsız | 736 ms | 760 ms | 0 | 10 ms | aynı |
| Misafir sayfası | CPU 4× · 1,6 Mbps · 150 ms | 4 452 ms | **4 452 ms** | 0 | 267 ms | 922 kB (15): js 441 · css 132 · diğer 349 |
| Misafir sayfası | kısıtsız | 952 ms | 952 ms | 0 | 3 ms | aynı |
| Giriş | CPU 4× · 1,6 Mbps · 150 ms | 3 940 ms | 3 940 ms | **0,329** | 320 ms | 874 kB (15) |
| Fiyatlar | CPU 4× · 1,6 Mbps · 150 ms | 3 936 ms | **5 180 ms** | **0,625** | 390 ms | 879 kB (21) |

Yöntem: Lighthouse yerine aynı ölçütler tarayıcının `PerformanceObserver` API'si ve CDP ağ/CPU kısıtlamasıyla
alındı (`evidence/scripts/e2e/perf-measure.mjs`); build, Nginx kurallarını taklit eden yerel bir sunucudan
sunuldu (`perf-server.mjs`: gzip, `/assets/` immutable). "Diğer" kalemi ağırlıkla Google Fonts dosyalarıdır;
ölçüm sırasında tarayıcı `fonts.googleapis.com`'a gitti (uygulamanın kendi davranışı, `SEC-12`). Başsız
Chromium ve yerel ağ: sayılar laboratuvar değeridir, sıralama ve büyüklük mertebesi için kullanılmalıdır.

### Şablon ölçümleri (yolculuk 7; 390×844, CPU 4×, geliştirme sunucusu)

| Şablon | Faz · plan | FPS (normal → indirgenmiş) | Uzun görev (sayı / engelleme) | Video (oynayan) | İndirgenmiş harekette durdu mu |
|---|---|---|---|---|---|
| `kurumsal-lansman` | 17 · Gold | 35 → 60 | 3 / 614 ms | 1 → 0 | ✅ |
| `kina-bugulu-ayna` | 17 · Gold | 25 → 60 | 1 / 525 ms | 2 → 0 | ✅ |
| `sunnet-ucan-hali` | 17 · Gold | 42 → 59 | 2 / 367 ms | 1 → 0 | ✅ |
| `parti-lazer` | 17 · Gold | 28 → 60 | 2 / 168 ms | 1 → 0 | ✅ |
| `dugun-kelebek` (3B) | 17 · Gold | 34 → 61 | 2 / 458 ms | — | ✅ |
| `dugun-karanlik-oda` | 17 · Gold | 32 → 60 | 3 / 470 ms | — | ✅ |
| `nisan-koi` | 17 · Gold | **17** → 61 | **30** / 201 ms | — | ✅ |
| `parti-kokteyl` | 17 · Gold | 32 → 60 | 2 / 413 ms | — | ✅ |
| `mezuniyet-yillik` | 17 · Gold | 35 → 49 | 4 / 525 ms | — | ✅ |
| `dogum-gunu-surpriz-makinesi` | 17 · Standart | 54 → 61 | 1 / 309 ms | — | ✅ |
| `baby-kazi-kazan` | 17 · Standart | 37 → 49 | 5 / 670 ms | — | ✅ |
| `dugun-saray-kapisi` | 16 · Gold | 47 → 60 | 1 / 499 ms | 1 → 0 | ✅ |
| `dogum-gunu-havai-fisek` | 16 · Gold | 33 → 60 | 3 / 433 ms | 1 → 0 | ✅ |
| `parti-havuz` | 16 · Gold | 25 → 60 | 1 / 185 ms | 1 → 0 | ✅ |
| `dugun-gul-3d` (3B) | 15 | 33 → 53 | 1 / 16 ms | — | ❌ (`FE-56`) |
| `dugun-fener` (3B) | 15 | 30 → 60 | 3 / 536 ms | — | ✅ |
| `dugun-kitap-ic-kapak` | 15 | 61 → 61 | 0 / 0 | — | ✅ (zaten durağan) |

FPS başsız Chromium'da yazılımsal WebGL ile ölçüldü; gerçek telefonun değeri **değildir**. Şablonlar arası
karşılaştırma için okunmalı: `nisan-koi` (17 fps, 30 uzun görev) ve videolu üç şablon (25–28 fps) en ağırları;
gerçek bir orta sınıf Android'de elle denenmeleri önerilir. On yedi şablonun hiçbirinde konsol hatası, başarısız
istek ya da yatay taşma yok.

## Regresyon

| # | Kaynak | Bulgu | Durum | Kanıt türü | Kanıt |
|---|---|---|---|---|---|
| R3 | Review §2.1 | Ödeme dönüş sayfası + `GET /orders/{id}` + `publishedAt` | ✅ kapandı | KOŞTURULDU | Yolculuk 3: `201 POST …/checkout` → `/odeme/basarili?order=…` "Ödemeniz doğrulanıyor" → imzalı webhook → `200 POST …/publish` → "Davetiyeniz yayında"; `GET /invitations/{id}` `status: published`, `publishedAt` dolu (`evidence/commands/E2E-J3-checkout.json`). Sözleşme: rotalar `App.tsx:90-115`, yoklama 20 × 3 sn (`utils/paymentReturn.ts`) |
| R8 | Review §5.2 | Fiyat sayfası vaatleri ↔ sunucu kuralları | 🟡 kısmen | KOD OKUMASI | Özellik matrisi (`data.ts:4018-4066`) ↔ `config/davetkart.php` `module_tiers`, `tiers.*.rsvp_limit`, `branding.white_label_tier`, `preset_tiers`: dokuz satırın hepsi tutarlı; "video galerisi" vaadi kartta yok. **Açık kalan:** SSS'deki "yayın süresi" ve ücretli uzatma backend'de yok (`FE-52`); kurallar frontend'de kopya (`FE-05`) |
| R16 (frontend) | Fiyat kararı | Fiyatlar yalnızca backend'den; indirim; ödeme yöntemleri | ✅ kapandı | KOŞTURULDU | `verify:pricing` ✓ ("src/ fiyat taşımıyor, kimlik değişince katalog yenileniyor"); sabit fiyat taraması 0 kod satırı; `PricingResource` `paymentMethods` ve `firstPublishPercent` taşıyor |
| R1 (arayüz) | Review §1.1 / K-1 | Yayından sonra üst plan modülü | ✅ kapandı | KOŞTURULDU | Yolculuk 4: yayındaki Gold davetiyede galeri açılınca `402 PUT /invitations/{id}` + plan duvarı; misafir ucunda `showGallery:false` (`evidence/commands/E2E-J4-k1-paywall.json`, `screenshots/J4-galeri-acildi-1440.png`) |
| R15 | Faz 14 | Plan hakkı sayısı, hak iptali / iade talebi, güvenli e-posta değişikliği | ✅ kapandı | KOŞTURULDU | Yolculuk 6: hak sayıları ve durumları doğru; iade talebi hakkı donduruyor, geri çekme 204; e-posta değişikliği mevcut parolayı istiyor, bağlantı tek kullanımlık, onayda bütün oturumlar kapanıyor (`E2E-J6-*.json`) |

## Kullanılan araçlar ve skill'ler / kullanılamayanlar

- Kullanılan: Node betikleri (`evidence/scripts/fe-d1-metrics.mjs`, önceki oturumdan `fe-routes.mjs`,
  `fe-error-codes-compare.mjs`), `tsc`, `grep`, `du`.
- Tarayıcı (D2): Playwright 1.61.1 + Chromium (npx önbelleğindeki kurulum), bağımsız Node betikleriyle
  (`evidence/scripts/e2e/`): `lib.mjs` (ortak), `step.mjs` (komut satırından adım koşucusu), `j1-auth.mjs`,
  `j2-create.mjs`, `j7-templates.mjs`, `axe-scan.mjs`, `perf-server.mjs`, `perf-measure.mjs`. Yalnızca kayıt adımı
  Playwright MCP ile koştu (`j1a-register.js`). **Plandan sapma:** plan Playwright MCP diyordu; MCP her çağrıda
  betiği geri yazdığı için bağımsız betiklere geçildi. Tek tarayıcı kuralı korundu (aynı anda tek koşu).
- axe-core 4.10.3: npm kaydından geçici klasöre indirildi, sayfaya yerel dosyadan enjekte edildi (CDN yok).
- Sahte ödeme: `PAYMENT_PROVIDER=fake`; "ödendi" bildirimi `backend-e2e` kopyasının kendi anahtarıyla PHP içinde
  imzalanıp `localhost:8000`'e gönderildi (`step.mjs` → `webhook:`). Anahtar hiçbir dosyaya yazılmadı.
- Test hesabının parolası betiklerde ve kanıtlarda yer tutucuyla (`<AUD_TEST_PAROLASI>`) değiştirildi; e-posta
  onay bağlantısının imzalı sorgusu kanıtlardan silindi.
- Skill: `superpowers:executing-plans` (planın ana oturumda yürütülmesi). `mattpocock-skills:codebase-design`,
  `…:diagnosing-bugs`, `…:tdd` **kullanılmadı**: bu dilimde kod yazılmadı ve teşhis gerektiren bir hata çıkmadı.
- Kullanılamayan: Context7 (bağlı değil). Resmî belgelerle API karşılaştırması yapılmadı; ilgili satırlar
  "doğrulanamadı" diye işaretli. Lighthouse (kurulu değil; ölçütler CDP ile alındı). Gerçek telefon, Safari,
  Firefox, ekran okuyucu.
- Denetimin bıraktığı veri: `davetkart_aud_e2e` veritabanında test hesabı (`elif.yildirim.yeni996311@example.com`),
  4 davetiye (1 yayında, 3 boş taslak), 2 ödenmiş sipariş, 2 LCV ve `AUDYUZDE20` hediye kodu. Veritabanı
  denetim bitince silinecekler listesinde (`README.md` → Temizlik).

## Koşturulan komutlar

| Kanıt | Komut |
|---|---|
| `evidence/commands/FE-d1-metrics.txt` | `node evidence/scripts/fe-d1-metrics.mjs` |
| `evidence/commands/FE-tsc-strict.txt` | `npx tsc --noEmit --strict` ve `--strictNullChecks` (`frontend-tst`; `tsconfig` değişmedi) |
| `evidence/commands/FE-route-list.json` | `php artisan route:list --json` (önceki oturum, `backend`) |
| `evidence/commands/FE-error-codes-compare.txt` | `node evidence/scripts/fe-error-codes-compare.mjs` (önceki oturum) |
| (dosyasız) Resource alanları | `for r in backend/app/Http/Resources/*.php`: `'anahtar' =>` satırlarını çıkar, her anahtarı `grep -rqw` ile `frontend/src` (şablonlar hariç) içinde ara → 16 Resource'ta "geçmeyen: (yok)" |
| (dosyasız) Enum değerleri | sekiz enum için `case X = 'değer'` satırlarını çıkar, `frontend/src/{types.ts,services,utils,stores}` içinde ara → hepsi "(yok)" |
| `evidence/commands/E2E-J1-auth.json` | `node evidence/scripts/e2e/j1-auth.mjs` (kayıt: `j1a-register.js`, Playwright MCP) |
| `evidence/commands/E2E-J2-create.json` | `node evidence/scripts/e2e/j2-create.mjs --dump` |
| `evidence/commands/E2E-J3…J6-*.json`, `E2E-J8-*.json` | `node evidence/scripts/e2e/step.mjs --rec <ad> <yol> <eylem>…` (tam komut her dosyanın `command` alanında) |
| `evidence/commands/E2E-J7-templates.json` | `node evidence/scripts/e2e/j7-templates.mjs` |
| `evidence/commands/E2E-axe.json` | `node evidence/scripts/e2e/axe-scan.mjs` |
| `evidence/commands/E2E-perf.json` | `node evidence/scripts/e2e/perf-server.mjs` (arka planda) + `node evidence/scripts/e2e/perf-measure.mjs` |
| `evidence/screenshots/J1…J8-*.png` | 80 ekran görüntüsü (yolculuk tablosunda adlarıyla) |
| (dosyasız) Boyutlar | `du -sh public` → 95M · `du -sh frontend-tst/dist` → 104M |

## İsmail'e sorular

1. **Diller (`FE-01`):** on dil bir ürün hedefi mi, yoksa şablondan kalan bir liste mi? Hedef değilse dil
   seçiciyi tr/en'e indirmek bir saatlik iş.
2. **Konum araması (`FE-08`):** Google Places ucu yazılacak mı? Yazılmayacaksa üç dosya kaldırılabilir.
3. **Paylaşım önizlemesi (`FE-04`):** Elit planda önizlemede "DavetKart" adı görünsün mü?
4. **Yayın süresi (`FE-52`):** paketlerin bir yayın süresi olacak mı? Olmayacaksa SSS'deki iki cevap değişmeli.
5. **Misafir medyası (`FE-51`):** misafirlerin fotoğraf/video yüklemesi ürün kapsamında mı? Değilse uç kapatılabilir.
6. **Yükseltme fiyatı:** Gold'dan Elit'e yükseltmede plan duvarı tam fiyatı (₺549) gösteriyor; ödenen Gold tutarı
   düşülmüyor. Bu bilinçli bir karar mı? (Bulgu olarak yazılmadı.)
7. **Varsayılan modüller:** yeni davetiyede zarf ve program akışı açık geliyor, ikisi de Gold. "Temel" bir tema
   seçen kullanıcı yayın anında Standart'ın "yetersiz" olduğunu görüyor. İstenen davranış bu mu?
