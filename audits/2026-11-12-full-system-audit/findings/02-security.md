# Güvenlik (backend + frontend) — AUD-2026-11-12

> Yürüten: ana oturum (Fable 5.2) · Kopyalar: `_audit-snap\backend-e2e` (canlı sonda, `http://127.0.0.1:8000`), `_audit-snap\backend` ve `frontend` (okuma), `frontend-tst` (build, `npm audit`) · Commit: backend `d810410`, frontend `44caa49` · Tarih: 13 Kasım 2026
> Referans: OWASP ASVS 4.0.3 Seviye 2 · OWASP API Security Top 10 (2023). İki dilim ajanı (B1, B2) kullanım sınırına takıldı; bu dosyayı ana oturum tek başına yazdı.

## Özet

Çekirdek savunmalar yerinde ve canlı sondada doğrulandı: 102 denemenin 95'inde beklenen güvenli davranış
görüldü. İkinci kullanıcı başkasının hiçbir nesnesine ulaşamadı, fiyat ve durum istekten enjekte edilemedi,
yayındaki davetiyede üst plan modülü açılamadı (K-1 kapalı), webhook tekrar oynatılamadı, bozuk girdi 400
döndü, yüklenen görselden EXIF ve dosya sonuna eklenen PHP kuyruğu temizlendi, e-posta değişikliği ve parola
sıfırlama bağlantıları kurcalamaya ve yeniden kullanıma dayandı.

Para etkisi olan iki iş kuralı boşluğu var ve ikisi de canlı gösterildi: "ilk yayın" indirimi aynı anda açılan
her siparişe uygulanıyor (`SEC-01`), kullanılıp üç gün içinde silinen davetiyenin hakkı için iade talebi kabul
ediliyor ve yönetici bunu göremiyor (`SEC-02`). Yayından önce kapatılması gereken iki yapılandırma eksiği:
Shopier `callback` kipinde `status` imzasız (`SEC-03`) ve frontend sayfaları hiçbir güvenlik başlığı taşımıyor
(`SEC-04`). Git geçmişinde commit'lenmiş gerçek sır bulunmadı.

**Koşturulamayanlar (B7):** Shopier, S3, SES, Gemini ve Sentry yolları yalnızca okundu. Hediye kodu yarışı
(eşzamanlı kullanım) koşturulmadı; kilit kodu okundu. Shopier'in başarısız ödemede imzalı callback gönderip
göndermediği **varsayım**.

Seviye sayıları: 🔴 0 · 🟠 4 · 🟡 9 · 🟢 4 · 💡 1 — Kanıt: KOŞTURULDU 10 · KOD OKUMASI 8 · VARSAYIM 0

## Özet tablosu

| ID | Seviye | Kanıt türü | Başlık | Nerede | Efor | Tek satır öneri |
|---|---|---|---|---|---|---|
| SEC-01 | 🟠 | KOŞTURULDU | "İlk yayın" indirimi aynı anda açılan her siparişe uygulanıyor | `backend:app/Actions/Pricing/QuotePriceAction.php:90-104` | M | İndirimi ödeme anında da doğrula ya da açık indirimli sipariş varken ikincisini indirimsiz aç |
| SEC-02 | 🟠 | KOŞTURULDU | Kullanılıp silinen davetiyenin hakkı iade edilebiliyor; yönetici göremiyor | `backend:app/Services/Refund/RefundEligibility.php:33-43` | M | Siparişe "ilk yayınlandığı an" damgası; damgalıysa iade yok |
| SEC-03 | 🟠 | KOD OKUMASI | Shopier `callback` kipinde `status` ve tutar imzasız | `backend:app/Services/Payment/ShopierGateway.php:156-192` | S | Üretimde `callback` kipini reddet |
| SEC-04 | 🟠 | KOD OKUMASI | Frontend sayfalarında güvenlik başlığı yok; token `localStorage`'da | `backend:deploy/nginx/davetkart.conf:53-108` | S | Nginx'e CSP, `frame-ancestors`, `nosniff`, HSTS ekle |
| SEC-05 | 🟡 | KOŞTURULDU | Zayıf parolalar kabul ediliyor | `backend:app/Http/Requests/Auth/RegisterRequest.php:37` | S | `Password::min(12)` + yaygın parola listesi |
| SEC-06 | 🟡 | KOŞTURULDU | Genel hız sınırı IP anahtarlı: misafir trafiği davetiye sahibini de kilitliyor | `backend:app/Providers/AppServiceProvider.php:363-368` | M | Girişli kullanıcıyı kimliğiyle, misafiri davetiye + IP ile kovala |
| SEC-07 | 🟡 | KOŞTURULDU | Composer bağımlılıklarında 8 bilinen açık; `composer audit` kırmızı | `backend:composer.lock` (Symfony 8.1.0–8.1.9) | S | `composer update` (semver güvenli) |
| SEC-08 | 🟡 | KOD OKUMASI | Kimliksiz misafir davetiye başına 5 GB yükleyebilir; yetim dosya kotayı 24 saat tutar | `backend:config/davetkart.php:139-150` | M | Kotaları düşür, toplam bayt sınırı ekle, yetim süresini kısalt |
| SEC-09 | 🟡 | KOŞTURULDU | E-posta doğrulaması yok | `backend:app/Actions/Auth/RegisterUserAction.php:31-41` | L | Doğrulanmamış hesapta ödeme/indirim kapalı |
| SEC-10 | 🟡 | KOD OKUMASI | Shopier'e uydurma TCKN ve telefon gönderiliyor | `backend:config/payment.php:54-61` | S | Shopier'den yazılı teyit ya da gerçek veri |
| SEC-11 | 🟡 | KOD OKUMASI | Gizlilik metni "hemen silinir" diyor; yedekler 7–30 gün tutuyor; üçüncü taraflar adıyla yok | `frontend:src/pages/legal/PrivacyPage.tsx` | S | Metne yedek süresini ve işleyenleri ekle |
| SEC-12 | 🟡 | KOŞTURULDU | Her sayfa Google Fonts'u Google'dan yüklüyor | `frontend:src/index.css:1` | S | Fontları kendi alan adından sun |
| SEC-13 | 🟡 | KOD OKUMASI | `data:purge` tarihi olmayan davetiyelerin misafir verisini hiç silmiyor | `backend:app/Console/Commands/PurgeExpiredData.php:103-106` | S | Tarih yoksa `created_at` + süre |
| SEC-14 | 🟢 | KOŞTURULDU | `main`'deki bağımlılık temizliği denetlenen dalda yok | `frontend:package.json` | S | `main`'i dala birleştir |
| SEC-15 | 🟢 | KOŞTURULDU | Kayıt ucu e-postanın kayıtlı olduğunu söylüyor | `backend:app/Actions/Auth/RegisterUserAction.php:42-45` | M | Doğrulamalı kayıtla birlikte çöz |
| SEC-16 | 🟢 | KOD OKUMASI | Hesap bazlı (IP'den bağımsız) kaba kuvvet freni yok | `backend:app/Providers/AppServiceProvider.php:380-389` | S | E-posta başına saatlik üçüncü kova |
| SEC-17 | 🟢 | KOŞTURULDU | Doküman deposunda git dışı 15 kod arşivi var, 3'ünde `.env` | `davetkart-docs/archive/local-snapshots/` | S | Sil ya da şifreli sakla; içindeki anahtarları döndür |
| SEC-18 | 💡 | KOD OKUMASI | Token'ı `localStorage` yerine `httpOnly` çerezde tut | `frontend:src/services/auth.ts:136-156` | L | Sanctum SPA (çerez) kipi |

## Neler iyi

1. **Nesne düzeyinde yetki her uçta, iki katmanda.** Tekil uçlarda Policy (`InvitationPolicy.php:72-75`,
   `OrderPolicy.php:38-41`), koleksiyonlarda sorgu (`$user->invitations()`, `$user->orders()`), iç içe kaynaklarda
   üst kaydın ilişkisi (`$invitation->rsvps()->whereKey(...)`). Sonda: on bir BOLA denemesinin hepsi 404.
2. **Toplu atama kapalı.** `$guarded` hiç yok, `fillable` beyaz liste (`Invitation.php:34-40`); sonda P09–P10:
   `status`, `user_id`, `published_at`, `id` enjeksiyonu yok sayıldı.
3. **Kimlik uçları sızdırmıyor.** Giriş: olmayan hesap ve yanlış parola aynı yanıt, aynı hash maliyeti
   (`LoginUserAction.php:39-50`; P63). Parola sıfırlama ve e-posta değişikliği her zaman 202 (P64, Q01).
4. **Tek kullanımlık bağlantılar gerçekten tek kullanımlık.** E-posta değişikliği imzası kullanıcıyı, yeni adresi,
   süreyi ve **eski adresin parmak izini** kapsıyor (`EmailChangeLink.php:30-38`); adres değişince bağlantı kendini
   geçersiz kılıyor. Q03–Q07: üç kurcalama ve yeniden kullanım 422.
5. **Hassas eylemler mevcut parolayı istiyor**: hesap silme, parola değişikliği, e-posta değişikliği
   (`current_password:sanctum`; P72, P80).
6. **Oturum hijyeni.** Token sha256 ile saklanıyor (P71), 30 günde ölüyor (P70), çıkışta siliniyor (P69); parola
   sıfırlama, parola değişikliği ve e-posta değişikliği diğer oturumları kapatıyor (Q06, Q12).
7. **Dosya yükleme katmanlı.** MIME içerikten (`StoreUploadedMediaAction.php:53`), ad sunucudan, uzantı MIME'dan,
   boyut ve piksel sınırı doğrulamada; görüntü yeniden kodlanıyor. P50–P55: PHP-as-JPG, SVG, GIF başlıklı HTML ve
   yol geçişli dosya adı reddedildi ya da etkisizleştirildi.
8. **Webhook imzası ham gövde üzerinde, `hash_equals` ile** (`FakeGateway.php:135-141`, `ShopierSignature.php:59-79`);
   geçersiz imza 404 (P19), tutar ve para birimi siparişle karşılaştırılıyor (`HandlePaymentCallbackAction.php:170-178`).
9. **Kişisel veri azaltılmış.** IP yalnızca HMAC'li saklanıyor (P24), oturum listesinde IP yok (K143), loglarda
   e-posta/ad yok (grep), hediye kodu düz metin saklanmıyor (`GiftCodeFormat.php:42-51`).
10. **Open redirect yok.** Dönüş adresi config'ten, sipariş kimliği yalnızca ULID ise eklenir
    (`ShopierCallbackController.php:63-71`).
11. **Frontend'de tehlikeli render kalıbı yok**: `dangerouslySetInnerHTML`, `innerHTML`, `eval` taraması boş;
    build'de kaynak haritası yok; frontend'de sır yok (`import.meta.env` yalnızca `VITE_API_BASE_URL` ve bir bayrak).

## Bulgular

### SEC-01 "İlk yayın" indirimi aynı anda açılan her siparişe uygulanıyor
- Seviye: 🟠 Yüksek
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:app/Actions/Pricing/QuotePriceAction.php:90-104` · `backend:app/Actions/Payment/StartCheckoutAction.php:111-142` · `backend:app/Actions/Payment/HandlePaymentCallbackAction.php:170-178`
- Senaryo: 1) Yeni kullanıcı ödeme sayfasını iki sekmede açar (ya da bir davetiye, bir paket siparişi başlatır). 2) İki sipariş de `pending` ve ikisi de %60 indirimli (249,00 → 99,60 TL), çünkü kural "`paid_at` damgalı sipariş yoksa ilk yayındır" ve bekleyen sipariş sayılmıyor (K131). 3) Kullanıcı ikisini de öder. 4) Ödeme bildirimi tutarı siparişteki donmuş tutarla karşılaştırır; indirimin hâlâ geçerli olup olmadığına bakmaz. İki hak da 99,60 TL'ye alınmış olur. Sınır yok: on sekme, on indirimli hak.
- Kanıt: `evidence/commands/SEC-api-probe.txt` → `[ACIK] P13 — sipariş1 paid 9960 kuruş (first_publish) · sipariş2 paid 9960 kuruş (first_publish) · webhook 204/204`; karşılaştırma için `P13b — ödeme sonrası üçüncü sipariş … totalMinor=24900 promotion=null`.
- Etki: Her ek hak 149,40 TL (Elit'te 329,40 TL) eksik tahsil edilir. Birden çok etkinliği olan ya da davetiye hazırlayıp satan biri için "ilk yayın" fiyatı kalıcı fiyat olur.
- Neden önemli (öğretici not): Bu bir **TOCTOU** (kontrol anı ≠ kullanım anı) hatası. Karar "henüz ödeme yok" gözlemine dayanıyor, ama gözlemle ödeme arasında durum değişebiliyor ve karar yeniden sınanmıyor. Tek kullanımlık bir hakkı (ilk alış indirimi) korumanın yolu, hakkı **ayırmak** (reserve) ya da kullanım anında yeniden doğrulamaktır. Hediye kodunda bu doğru yapılmış: kod satırı kilitlenip kullanım kaydı siparişle aynı transaction'da yazılıyor (K111). İlk yayın indiriminde aynı desen yok.
- Öneri: En ucuz: `StartCheckoutAction` transaction'ında kullanıcı satırını `lockForUpdate()` ile kilitle ve kullanıcının süresi dolmamış, `promotion = first_publish` taşıyan başka bir `pending` siparişi varsa yenisini indirimsiz fiyatla. Daha sağlam: `HandlePaymentCallbackAction`'da `paid`'e geçerken "bu kullanıcının başka `paid_at` damgalı first_publish siparişi var mı" diye bak; varsa geçişi yap ama `Log::critical` + yönetici bildirimi (para alınmış, geri çevrilemez). En sağlam: `ARC-09`'daki idempotent checkout ile birlikte, kullanıcı başına tek açık indirimli sipariş değişmezini kısmi UNIQUE index'e yaz (`WHERE status='pending' AND promotion='first_publish'`).
- Test önerisi: `the_first_publish_discount_is_granted_to_one_order_only`: aynı kullanıcı iki checkout açar; ikincinin `promotion`'ı `null` ve tutarı liste fiyatı. Öldürmesi gereken mutant: "açık indirimli sipariş var mı" sorgusunu kaldırmak.
- Efor: M
- İlgili: K130, K131 · R16 · `ARC-09`

### SEC-02 Kullanılıp silinen davetiyenin hakkı iade edilebiliyor; yönetici göremiyor
- Seviye: 🟠 Yüksek
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:app/Services/Refund/RefundEligibility.php:33-43` · `backend:app/Actions/Invitation/DeleteInvitationAction.php:51-59` · `backend:app/Console/Commands/ListRefundRequests.php`
- Senaryo: 1) Kullanıcı Standart alır, davetiyeyi yayınlar, bağlantıyı dağıtır, misafirler LCV bırakır. 2) Etkinlik yayından sonraki üç gün içindeyse (ya da kullanıcı işini görmüşse) davetiyeyi siler. Üç günlük pencere açık olduğu için sipariş serbest kalır: `invitation_id = NULL`, `consumed_at = NULL` (K82). 3) Kullanıcı "hakkı iptal et" der. Uygunluk kuralı yalnızca "bağlı mı, yanmış mı" diye bakar; sipariş ikisi de değil, ödeme üzerinden 14 gün geçmemiş. Talep 201 ile açılır. 4) Yönetici `refunds:list` çıktısında plan, tutar ve e-postayı görür; bu hakkın bir davetiyeyi yayınladığını gösteren hiçbir sütun yok. Onaylar, parayı Shopier'den iade eder.
- Kanıt: `evidence/commands/SEC-api-probe.txt` → `[ACIK] P47 — yayın 200 · misafir ucu 200 · LCV 201 · silme 204 · iade talebi 201 · sipariş invitation_id=NULL consumed_at=NULL` ve `[BILGI] P49 — … çıktıda "yayın"/"publish"/"kullan" geçiyor mu=false · sütunlar: | Talep | Tarih | Durum | Plan | Tutar | Shopier ödeme | E-posta | Açıklama |`.
- Etki: Hizmet kullanılıp parası geri alınabilir. Son savunma insan onayı, ama onaylayan kişi kararı verecek bilgiye sahip değil.
- Neden önemli (öğretici not): İki kural ayrı ayrı doğru: "yanlışlıkla yayınlayan üç gün içinde vazgeçebilsin" (K82) ve "kullanılmamış hak iade edilebilsin" (K139). Hata **birleşim yerinde**: birincisi "kullanılmış" bilgisini siliyor, ikincisi o bilgiye güveniyor. Bir durumu (kullanıldı) bir **bağın yokluğundan** türetmek kırılgandır; Faz 14 aynı dersi `consumed_at` için almış ("yanmış hak bir damgadır, bağ değil", K137) ama damga yalnızca pencere kapandıktan sonra basılıyor.
- Öneri: `orders.first_published_at` (ya da `published_count`) kolonu: `PublishInvitationAction` siparişi ilk kez yayın için kullandığında damgalar ve bu damga serbest bırakmada **silinmez**. `RefundEligibility`'ye `$order->first_published_at !== null → RefundBlocker::InUse` ekle. Ara çözüm (bugün, kod değişmeden): `refunds:list`'e kullanıcının silinmiş (çöp kutusundaki) yayınlanmış davetiyelerini gösteren bir sütun ve onay öncesi uyarı.
- Test önerisi: `a_right_that_published_an_invitation_cannot_be_refunded_after_release`: öde → yayınla → sil → iade talebi 409 `in_use`. Öldürmesi gereken mutant: yeni koşulu `RefundEligibility`'den çıkarmak.
- Efor: M
- İlgili: K82, K137, K139 · R15

### SEC-03 Shopier `callback` kipinde `status` ve tutar imzasız
- Seviye: 🟠 Yüksek
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:app/Services/Payment/ShopierGateway.php:156-192` · `backend:app/Services/Payment/Shopier/ShopierSignature.php:49-62` · `backend:config/payment.php:44` · `backend:app/Actions/Payment/HandlePaymentCallbackAction.php:170-174`
- Senaryo: `SHOPIER_CONFIRMATION=callback` seçilirse siparişi `paid` yapan şey tarayıcının getirdiği form olur. İmza yalnızca `random_nr + platform_order_id`'yi kapsıyor; `status` alanı ve tutar imzanın dışında. 1) Kullanıcı ödeme sayfasına gider, ödemeyi başarısız bırakır ya da iptal eder. 2) Shopier tarayıcıyı imzalı bir callback ile geri yollarsa (bu **varsayım**: Shopier'in başarısız ödemede de imza üretip üretmediği doğrulanmadı), kullanıcı formdaki `status=failed` değerini `success` yapar. 3) İmza geçerli, sipariş `paid`. Bu kipte bildirim tutar da taşımadığı için `amountMatches()` `true` döner.
- Kanıt: kod okuması. Varsayılan kip `osb` ve o kipte callback hiçbir siparişi değiştirmiyor (`ShopierGateway.php:183-189`); K117 bunu bilerek seçmiş. Shopier'e istek atılmadı.
- Etki: Yanlış kip seçilirse ödenmemiş sipariş yayın hakkı verir. Kip tek bir `.env` satırı ve `docs/10` onu geçerli bir seçenek olarak anlatıyor.
- Neden önemli (öğretici not): Bir imza yalnızca **kapsadığı** alanları korur. Karar veren alan (`status`) imzanın dışındaysa imza kararı korumaz. Tarayıcıdan gelen her şey kullanıcının elindedir; para kararını sunucudan sunucuya giden kanala (OSB) bırakmak doğru desen. Güvensiz olduğu bilinen bir seçeneği "kapatılabilir" bırakmak yerine **kaldırmak** fail-safe tasarımdır.
- Öneri: En ucuz: `ShopierGateway::__construct` içinde `App::isProduction() && confirmation === Callback` ise `PaymentProviderException::unavailable` fırlat (sır eksikliğiyle aynı davranış, K123). Daha sağlam: `callback` kipini tamamen kaldır; canlı doğrulama (K94) OSB ile yapılsın.
- Test önerisi: `the_callback_confirmation_mode_is_refused_in_production`: üretim ortamı + `callback` → checkout 503. Öldürmesi gereken mutant: ortam kontrolünü kaldırmak.
- Efor: S
- İlgili: K94 (⚠️ geçici), K117, K127 · R14 · ASVS V13.2 · OWASP API8

### SEC-04 Frontend sayfalarında güvenlik başlığı yok; token `localStorage`'da
- Seviye: 🟠 Yüksek
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:deploy/nginx/davetkart.conf:53-108` (hiç `add_header` güvenlik başlığı yok; yalnızca `/assets/` ve `/index.html` için `Cache-Control`) · `backend:app/Http/Middleware/SecurityHeaders.php:40-77` (yalnızca Laravel yanıtları) · `frontend:src/services/auth.ts:136-156`
- Senaryo: Güvenlik başlıkları Laravel ara katmanında (K85) ve yalnızca `/api/*` yanıtlarına ekleniyor. `index.html`, JS, CSS ve videolar Nginx'ten doğrudan çıkıyor ve hiçbir başlık taşımıyor: CSP yok, `X-Frame-Options`/`frame-ancestors` yok, `X-Content-Type-Options` yok, HSTS yok (tarayıcı HSTS'yi ancak ilk `/api` yanıtından öğrenir). Uygulama oturum token'ını `localStorage`'da tutuyor. 1) Saldırgan DavetKart'ı kendi sayfasında görünmez bir çerçeveye koyar ve kullanıcıyı "hesabı sil" ya da "yayınla" düğmesine tıklatır (clickjacking). 2) Ya da herhangi bir XSS (bugün yok; yarın bir şablonda ya da bağımlılıkta çıkabilir) token'ı okur; CSP olmadığı için dışarı göndermesini durduran ikinci bir katman yok.
- Kanıt: Nginx dosyasının okunması; üretim sunucusuna istek atılmadı (yasak). API tarafındaki başlıklar sondada görüldü (P57).
- Etki: Hesap ele geçirme için tek hata yetiyor; arayüz çerçevelenebiliyor. Bugün bilinen bir XSS yok, bu yüzden "özel koşul gerektirir".
- Neden önemli (öğretici not): **Derinlemesine savunma**: `localStorage`'daki token XSS'e karşı korumasızdır; onu tutmayı seçtiysen CSP ikinci kilittir. K85 "başlıklar nginx'te değil middleware'de" derken API'yi düşündü; SPA'yı sunan katman Nginx olduğu için karar frontend'i kapsamıyor. ASVS V14.4.3–14.4.7 bu başlıkları **her** yanıtta ister.
- Öneri: `davetkart.conf` içindeki `davetkart.com` sunucu bloğuna (ve `location` blokları `add_header` kullandığı için o bloklara da; Nginx'te `add_header` miras alınmaz):
  ```nginx
  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
  add_header X-Content-Type-Options "nosniff" always;
  add_header Referrer-Policy "strict-origin-when-cross-origin" always;
  add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
  add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob: https://media.davetkart.com; media-src 'self' blob: https://media.davetkart.com; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self' https://www.shopier.com" always;
  ```
  Önce `Content-Security-Policy-Report-Only` ile yayınla; şablonların WebGL, jiroskop (`Permissions-Policy`'de `gyroscope`, `accelerometer`) ve harita ihtiyaçlarını ölç. `SEC-12` çözülürse Google alan adları CSP'den çıkar.
- Test önerisi: Dağıtım sonrası duman testi: `curl -sI https://davetkart.com/ | grep -ci "content-security-policy\|strict-transport-security\|x-content-type-options"` → 3. Yerelde: Nginx yapılandırmasını `nginx -t` ve bir konteynerde başlık testiyle doğrula.
- Efor: S
- İlgili: K85 · ASVS V14.4 · `SEC-18`

### SEC-05 Zayıf parolalar kabul ediliyor
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:app/Http/Requests/Auth/RegisterRequest.php:37` · `ResetPasswordRequest.php:35` · `Account/ChangePasswordRequest.php:35` (hepsi `min:8, max:255`)
- Senaryo: Kayıtta `12345678`, `password`, `aaaaaaaa` kabul ediliyor.
- Kanıt: `evidence/commands/SEC-api-probe.txt` → üç `[ACIK] P67 — zayıf parola kabulü: … — 201`.
- Etki: Kimlik bilgisi doldurma (credential stuffing) saldırısında en çok denenen parolalar geçerli. Hız sınırı (5/dk) yavaşlatır, durdurmaz (`SEC-16`).
- Neden önemli (öğretici not): ASVS 2.1.1 en az 12 karakter, 2.1.7 bilinen sızıntı listelerine karşı denetim ister. Karmaşıklık kuralı (büyük harf, rakam) **istenmez**; uzunluk ve "yaygın değil" yeter.
- Öneri: Üç istekte ortak bir kural nesnesi: `Password::min(12)`. Sızıntı denetimi için `->uncompromised()` Have I Been Pwned'a (k-anonimlik, parolanın kendisi gitmez) istek atar; dış bağımlılık istemiyorsan depoya en yaygın 10.000 parolalık bir liste koy ve `not_in` ile reddet.
- Test önerisi: `registration_rejects_common_passwords` (veri sağlayıcılı: `12345678`, `password`, `qwerty123456`). Öldürmesi gereken mutant: kuralı `min:8`'e geri almak.
- Efor: S
- İlgili: ASVS V2.1.1, V2.1.7 · A-serisi kurallar

### SEC-06 Genel hız sınırı IP anahtarlı: misafir trafiği davetiye sahibini de kilitliyor
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:app/Providers/AppServiceProvider.php:363-368` (`api` kovası: 60/dk, yalnızca IP) · `backend:config/davetkart.php:131` (misafir medya: IP başına 15/dk) · `bootstrap/app.php:39`
- Senaryo: Düğün salonu. Masalarda QR kod, yüz misafir salonun Wi-Fi'ında, yani tek bir dış IP'de. 1) Bir dakika içinde 60'tan fazla kişi davetiyeyi açar: 61. istek 429. 2) Aynı Wi-Fi'daki davetiye sahibi panelini açmak ister: o da 429, çünkü girişli kullanıcı da aynı IP kovasında. 3) Misafirler fotoğraf yükler: bütün salon için dakikada 15 dosya. Aynı durum mobil operatörlerin CGNAT'ı için de geçerli.
- Kanıt: `evidence/commands/SEC-api-probe.txt` → `[BILGI] P85 — … ilk 429 istek no=61 Retry-After=58` ve `[ACIK] P86 — aynı IP'deki GİRİŞ YAPMIŞ kullanıcı da aynı kovada mı — 429 RATE_LIMITED`.
- Etki: Ürünün en görünür anında (etkinlik saati) meşru kullanıcılar hata görür. Veri ya da para kaybı yok.
- Neden önemli (öğretici not): Hız sınırının anahtarı, **korumak istediğin kaynağı tüketen kimliği** temsil etmeli. IP, kimliği bilinmeyen biri için elimizdeki en iyi yaklaşımdır; kimliği bilinen biri için kötü bir yaklaşımdır. K104 LCV ve medya kovalarını düğüne göre ayarladı ama genel tavanı ve kimlikli kullanıcıyı atladı.
- Öneri: `apiLimits`: `$request->user()` varsa `by('api|user|'.$id)` ve 120/dk; yoksa IP. Misafir okuma ucu (`GET /public/invitations/{id}`) zaten cache'li ve ETag'li: ona ayrı, geniş bir kova (IP başına 300/dk) ya da Nginx'te mikro-cache. Misafir medya IP kovasını 15 → 60 yap; davetiye başına saatlik kova (150) asıl freni tutuyor.
- Test önerisi: `an_authenticated_user_is_not_throttled_by_guests_on_the_same_ip`: aynı IP'den 61 misafir isteği + 1 girişli istek → girişli istek 200. Öldürmesi gereken mutant: kovayı yeniden yalnızca IP'ye bağlamak.
- Efor: M
- İlgili: K104 · R9 (Review §5.4) · OWASP API4

### SEC-07 Composer bağımlılıklarında 8 bilinen açık; `composer audit` kırmızı
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:composer.lock` → `symfony/http-foundation v8.1.9` (4 tavsiye), `symfony/http-kernel v8.1.1`, `symfony/routing v8.1.0`, `symfony/mime v8.1.0`, `symfony/filesystem v8.1.9`
- Senaryo: 4 Kasım 2026'da yayımlanan Symfony güvenlik tavsiyeleri kurulu sürümleri kapsıyor; düzeltmeler 8.1.10/8.1.11'de. `backend:.github/workflows/ci.yml:95` `composer audit` koşturduğu için bu dalın CI'ı bu adımda da kırmızıdır (GitHub'a bakılmadı; yerel çıkış kodu 1).
- Kanıt: `evidence/commands/B2-composer-audit.txt` (çıkış kodu 1): `CVE-2026-118514` (HEAD istekleri), `CVE-2026-123339` (iletilen başlıklarla üretilen URL'ler), `CVE-2026-118516` (yönlendirme), `CVE-2026-45070` (posta başlığı enjeksiyonu, orta) ve dört PKSA kaydı ("üretilen URL'ler istemcinin seçtiği host'u gösterebilir", "`private_ranges` güvenilen vekil kısayolu", "PHP önündeki yol kuralları atlatılabilir", dosya sistemi yolu).
- Etki: Bu uygulamada doğrudan sömürü yolu görmedim: bağlantılar `config('davetkart.frontend.url')`'den üretiliyor, güvenilen vekil listesi boş, Nginx yalnızca `index.php`'yi çalıştırıyor. Yine de "üretilen URL'ler" maddesi `ShopierGateway::startCheckout`'taki `url(CALLBACK_PATH)` çağrısına dokunuyor (istek host'undan üretilir).
- Neden önemli (öğretici not): Bağımlılık açığı, senin yazmadığın ama senin sorumluluğunda olan koddur. Kırmızı bir kapı okunmaz hâle gelir; `composer audit` kırmızı kaldıkça gerçek bir kritik açık da aynı gürültünün içinde kaybolur.
- Öneri: `composer update "symfony/*" laravel/framework --with-all-dependencies` (hepsi semver güvenli: `laravel/framework` 13.35 → 13.42), ardından `composer check`. `ShopierGateway`'de callback adresini `config('app.url')`'den üret.
- Test önerisi: CI'daki `composer audit` adımı zaten test; yeşile döndüğünü gör.
- Efor: S
- İlgili: ASVS V14.2.1 · OWASP API8

### SEC-08 Kimliksiz misafir davetiye başına 5 GB yükleyebilir; yetim dosya kotayı 24 saat tutar
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:config/davetkart.php:139-150` (LCV fotoğrafı 200 × 15 MB, LCV videosu 100 × 20 MB) · `:126` (`orphan_grace_hours` 24) · `backend:app/Actions/Media/StoreUploadedMediaAction.php:139-154`
- Senaryo: Yayındaki bir davetiyenin bağlantısını bilen herkes, giriş yapmadan, 200 fotoğraf (3 GB) ve 100 video (2 GB) yükleyebilir. Hız sınırı davetiye başına saatte 150 dosya; kota iki saatte dolar. Kota, LCV'ye iliştirilmemiş (yetim) dosyaları da sayıyor ve yetimler 24 saat sonra temizleniyor. 1) Saldırgan kotayı yetim dosyalarla doldurur: gerçek misafirler 24 saat boyunca fotoğraf yükleyemez. 2) Ertesi gün tekrarlar. 3) On iki davetiyede aynı şeyi yapan biri 60 GB'lık sunucu diskini (medya yereldeyse) ya da S3 faturasını doldurur.
- Kanıt: config değerleri ve kota sorgusu okundu. Yük testi yapılmadı (yasak ve gereksiz).
- Etki: Özellik düzeyinde hizmet engelleme ve depolama maliyeti. Veri sızıntısı yok.
- Neden önemli (öğretici not): OWASP API4 (kaynak tüketimi). Kimliksiz bir yazma ucunda sınır yalnızca **adet** olmamalı; **toplam bayt** ve **zaman** da sınırlanmalı. Bir kaynağı "ayırıp kullanmayan" (yetim) taraf kotayı uzun süre tutabiliyorsa, kota bir DoS aracına dönüşür.
- Öneri: Davetiye başına toplam misafir baytı sınırı (ör. 1 GB) ve plan bazlı kota; yetim süresini 24 saat → 1 saat; yetimleri kota sayımından çıkar ya da ayrı, küçük bir "bekleyen" kotası tanımla; video süresini/boyutunu düşür (20 MB cep telefonu videosunda ~10 saniye).
- Test önerisi: `orphaned_guest_uploads_do_not_consume_the_attached_media_quota` ve `guest_uploads_stop_at_the_byte_budget`. Öldürmesi gereken mutant: kota sorgusuna yetimleri yeniden dahil etmek.
- Efor: M
- İlgili: K55, K61 · R9 (video boyutu) · OWASP API4

### SEC-09 E-posta doğrulaması yok
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:app/Actions/Auth/RegisterUserAction.php:31-41` (kayıt anında token) · `backend:app/Models/User.php` (`MustVerifyEmail` yok) · `email_verified_at` yalnızca `ConfirmEmailChangeAction.php:60`'ta yazılıyor
- Senaryo: Kayıt herhangi bir adresle tamamlanır ve hemen tam yetkili oturum açılır. 1) Başkasının adresiyle hesap açılabilir; o kişi sonra kayıt olamaz (parola sıfırlamayla hesabı alabilir, ama içinde yabancı veri bulur). 2) "İlk yayın %60" indirimi hesap başına verildiği için, her davetiyede yeni bir uydurma adresle kayıt olan biri hiçbir zaman liste fiyatı ödemez. 3) İade, parola ve bilgilendirme postaları doğrulanmamış adreslere gider; SES itibarını düşürür.
- Kanıt: sonda boyunca sekiz hesap `@example.test` adresleriyle açıldı ve hepsi anında checkout yapabildi (`SEC-api-probe.txt` S00, P37–P39); `grep -rnE "MustVerifyEmail|VerifyEmail" app routes` boş.
- Etki: İndirim kuralının hesap açarak aşılması (gelir), posta itibarı, hesap gaspı sürtünmesi.
- Neden önemli (öğretici not): Doğrulanmamış bir e-posta bir **iddiadır**, kimlik değildir. Kimliğe bağlı her ayrıcalık (indirim, bildirim, hesap kurtarma) iddiaya değil kanıta bağlanmalı.
- Öneri: Kademeli: 1) Kayıtta doğrulama postası gönder (`EmailChangeLink` deseninin aynısı yeniden kullanılabilir). 2) Doğrulanmamış hesap davetiye hazırlayabilsin ama checkout ve yayın `403 EMAIL_NOT_VERIFIED` dönsün. 3) İlk yayın indirimi yalnızca doğrulanmış hesaba.
- Test önerisi: `an_unverified_account_cannot_start_a_checkout`. Öldürmesi gereken mutant: doğrulama kontrolünü `StartCheckoutAction`'dan kaldırmak.
- Efor: L
- İlgili: R6 (Review §2.4) · ASVS V2.5 · `SEC-01`, `SEC-15`

### SEC-10 Shopier'e uydurma TCKN ve telefon gönderiliyor
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:config/payment.php:54-61` (`id_nr => '11111111110'`, `phone => '05000000000'`, sabit adres) · `backend:app/Services/Payment/ShopierGateway.php:306-331`
- Senaryo: Ödeme formunda alıcının T.C. kimlik numarası, telefonu ve adresi yerine herkes için aynı yer tutucu değerler gidiyor. Karar kaydı bunu "elle doğrulama bekliyor" diye işaretlemiş (K125 ⚠️).
- Kanıt: config ve sürücü okundu. Shopier'e istek atılmadı; Shopier'in bu değerleri kabul edip etmediği **doğrulanmadı**.
- Etki: Ödeme sağlayıcısı sahte kimlik verisini sözleşme ihlali ya da dolandırıcılık sinyali sayarsa hesap askıya alınabilir; itiraz (chargeback) süreçlerinde alıcı bilgisi eşleşmez. Hukuki değerlendirme bu denetimin dışında.
- Neden önemli (öğretici not): "Çalışıyor" ile "izin verilmiş" aynı şey değil. Üçüncü tarafa giden kişisel veri alanları ya gerçek olmalı ya da sağlayıcının yazılı olarak kabul ettiği bir muafiyete dayanmalı.
- Öneri: Shopier desteğinden dijital ürün için bu alanların zorunlu olup olmadığını yazılı sor; cevaba göre ya alanları kaldır ya da checkout'ta kullanıcıdan telefon iste. Kararı K125'e işle.
- Test önerisi: —
- Efor: S
- İlgili: K125 (⚠️)

### SEC-11 Gizlilik metni "hemen silinir" diyor; yedekler 7–30 gün tutuyor; üçüncü taraflar adıyla yok
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `frontend:src/pages/legal/PrivacyPage.tsx` · `davetkart-docs/operations/deployment/YAYIN-PLANI.md:128-130,205,324,335` · `backend:app/Actions/Auth/DeleteAccountAction.php`
- Senaryo: Gizlilik metni hesap silinince verinin hemen silindiğini söylüyor ve frontend'in kendi doğrulama betiği bu cümleyi kilitliyor (`verify-render`: "hesap silinince veriler hemen silinir (K97)"). Kod canlı veritabanında ve diskte gerçekten hemen siliyor (sonda P81). Ama yayın planına göre: gece `pg_dump` yedekleri S3'te 30 gün, Lightsail anlık görüntüleri 7 gün, medya bucket'ında sürümleme açık ve eski sürümler 7 gün sonra siliniyor. Silinen misafir adı, mesajı ve fotoğrafı bu süre boyunca yedeklerde duruyor. Ayrıca metinde "yurt dışı" bir kez geçiyor ama veriyi işleyenler (AWS Frankfurt, Google Fonts, Shopier, Sentry, açılırsa Gemini) adıyla sayılmıyor.
- Kanıt: metin ve plan okundu; `grep -rnoiE "google fonts|sentry|amazon|aws|gemini|shopier|yurt ?dışı" frontend/src/pages/legal/*.tsx` → yalnızca bir "yurt dışı". AWS'ye bakılmadı; sürümleme ve ömür kuralı bilgisi yayın planındaki kayıttan.
- Etki: Aydınlatma metni ile gerçek saklama arasında fark. Hukuki sonucu bu denetim değerlendirmez; teknik olarak metin doğru değil.
- Neden önemli (öğretici not): "Silme" bir an değil bir **süreçtir**: canlı veri, yedek, anlık görüntü, nesne sürümleri. Dürüst bir saklama beyanı en uzun yaşayan kopyanın süresini söyler.
- Öneri: Metne "yedeklerden en geç 30 gün içinde silinir" cümlesini ve veri işleyenlerin listesini ekle; `verify-render`'daki beklenen ifadeyi buna göre güncelle. Yedek bucket'ının ömür kuralının gerçekten 30 gün olduğunu AWS panelinden doğrula (ben doğrulayamam).
- Test önerisi: `verify-render` içinde "yedek" ve "30 gün" ifadelerinin varlığı.
- Efor: S
- İlgili: K97, K98 · R6 (KVKK)

### SEC-12 Her sayfa Google Fonts'u Google'dan yüklüyor
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:src/index.css:1` (`@import url('https://fonts.googleapis.com/css2?…')`) · `frontend:src/components/templates/**/fontlar.ts` (beş şablon ailesi çalışma anında `<link>` ekliyor)
- Senaryo: Ana stil dosyası ilk satırda Google Fonts'u içe aktarıyor; misafir sayfası dahil her sayfa açılışında ziyaretçinin tarayıcısı `fonts.googleapis.com` ve `fonts.gstatic.com`'a bağlanıyor. Ziyaretçinin IP adresi ve hangi davetiyeye baktığı (Referer politikasına bağlı olarak) Google'a gidiyor. Misafir bu aktarıma rıza vermedi ve gizlilik metni bunu adıyla söylemiyor (`SEC-11`).
- Kanıt: `grep -rnE "fonts\.googleapis" frontend/src frontend/index.html` → 6 yer; build çıktısında CSS 1.171 kB ve ilk satırı bu içe aktarma.
- Etki: Üçüncü tarafa kişisel veri (IP) aktarımı; ayrıca render'ı bloke eden bir dış istek (performans) ve CSP'yi gevşetme zorunluluğu (`SEC-04`).
- Neden önemli (öğretici not): Üçüncü taraf kaynağı, kullanıcının tarayıcısına "şu sunucuya da git" demektir. Font gibi statik bir varlık için bunun hiçbir teknik gereği yok; kendi alan adından sunmak hem mahremiyet hem hız kazandırır.
- Öneri: Fontları `@fontsource/*` paketleriyle ya da `public/fonts/` altında kendi alan adından sun; şablonlardaki `fontlar.ts` yardımcılarını yerel `@font-face` tanımlarına çevir.
- Test önerisi: Build sonrası `grep -c "fonts.googleapis" dist/assets/*.css dist/assets/*.js` → 0 (bir `verify-*` betiğine eklenebilir).
- Efor: S
- İlgili: `SEC-04`, `SEC-11`

### SEC-13 `data:purge` tarihi olmayan davetiyelerin misafir verisini hiç silmiyor
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:app/Console/Commands/PurgeExpiredData.php:99-106` (`->whereNotNull('event_at')->where('event_at', '<', $cutoff)`)
- Senaryo: K98 "misafir verisi etkinlikten 6 ay sonra silinir" diyor. Etkinlik tarihi isteğe bağlı bir alan (`invitation.date` `nullable`). Tarihi girilmemiş yayınlanmış bir davetiyenin LCV yanıtları ve misafir dosyaları, sahibi hesabını ya da davetiyeyi silene kadar süresiz kalır.
- Kanıt: sorgu okundu; komut koşturulmadı.
- Etki: Saklama süresi taahhüdü bir alt kümede tutulmuyor.
- Neden önemli (öğretici not): Bir temizlik kuralı "X'ten N süre sonra" diyorsa, X'in **olmadığı** durum da tanımlanmalı. `NULL` ne geçmiş ne gelecek; sorgu onu sessizce atlar.
- Öneri: Tarih yoksa `published_at` (o da yoksa `created_at`) + 12 ay gibi bir yedek kural; kararı K98'e ek olarak yaz.
- Test önerisi: `guest_data_of_an_undated_invitation_is_purged_after_the_fallback_period`. Öldürmesi gereken mutant: yedek koşulu kaldırmak.
- Efor: S
- İlgili: K98 · R6

### SEC-14 `main`'deki bağımlılık temizliği denetlenen dalda yok
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:package.json` (denetlenen dal: `express`, `dotenv`, `@types/express` duruyor; `vite`, `@vitejs/plugin-react`, `@tailwindcss/vite` üretim bağımlılığı) ↔ `main@47aedc8`
- Senaryo: 26 Ekim'de `main`'e giren `47aedc8` kullanılmayan `express`/`dotenv`'i kaldırdı ve derleme araçlarını `devDependencies`'e taşıdı. Şablon dalları ondan önce ayrıldığı için düzeltme 60 commit'lik işte yok.
- Kanıt: `git -C davetkart-frontent diff origin/ccr-9a346997-bu6gve 47aedc8 -- package.json`. Bugün için `npm audit` iki ağaçta da temiz: `evidence/commands/B2-npm-audit-omit-dev.txt` ve `B2-npm-audit-all.txt` → `total: 0`.
- Etki: Saldırı yüzeyinde gereksiz paketler; dal `main`'e birleşirken `package-lock.json` çakışması.
- Neden önemli (öğretici not): Uzun yaşayan dal, ana dalın düzeltmelerini kaçırır. Düzeltme ne kadar küçükse o kadar kolay unutulur.
- Öneri: `main`'i şablon dalına birleştir (ya da tersini), `npm ci && npm run check` ile doğrula.
- Test önerisi: —
- Efor: S
- İlgili: `ARC-08`

### SEC-15 Kayıt ucu e-postanın kayıtlı olduğunu söylüyor
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:app/Actions/Auth/RegisterUserAction.php:42-45`
- Senaryo: Var olan adresle kayıt `422 REGISTRATION_FAILED` döner; olmayan adresle 201. Fark, adresin sistemde olup olmadığını söyler. Alan bazlı hata yok (iyi), ama durum kodu yeterli.
- Kanıt: `SEC-api-probe.txt` → `[BILGI] P65 — 422 REGISTRATION_FAILED … fields=null`.
- Etki: Bir adresin DavetKart müşterisi olup olmadığı öğrenilebilir (hız sınırı: IP başına 20/dk).
- Neden önemli (öğretici not): Giriş ve sıfırlama uçları özenle sızdırmaz yapılmış; zincirin en zayıf halkası kayıt. Tam çözüm doğrulamalı kayıttır: her adrese "kayıt bağlantısı gönderildi" denir, var olan hesaba "zaten hesabınız var" postası gider.
- Öneri: `SEC-09` ile birlikte çöz.
- Test önerisi: `registering_an_existing_email_is_indistinguishable_from_a_new_one`.
- Efor: M
- İlgili: A1 · ASVS V3.2.3

### SEC-16 Hesap bazlı (IP'den bağımsız) kaba kuvvet freni yok
- Seviye: 🟢 Düşük
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:app/Providers/AppServiceProvider.php:380-389` (kovalar: e-posta + IP başına 5/dk; IP başına 20/dk)
- Senaryo: Tek bir hesaba karşı çok sayıda IP'den (botnet, konut vekilleri) yapılan denemeler hiçbir kovada birikmez: her IP kendi 5/dk hakkını kullanır. Sonda P83–P84 tek IP davranışını doğruladı (6. denemede 429; hesap sahibi başka IP'den kilitlenmez, bu iyi).
- Kanıt: kod okuması.
- Etki: Zayıf parolalı hesaplarda (`SEC-05`) dağıtık deneme mümkün. Argon2id maliyeti sunucuyu da yorar.
- Neden önemli (öğretici not): IP'ye bağlı fren saldırganın maliyetini IP sayısına bağlar; hesaba bağlı fren (kilitlemeden, artan gecikmeyle) hedefi korur. İkisi birlikte kullanılır; yalnızca hesaba bağlı kilit ise hesap sahibine karşı DoS olur.
- Öneri: Üçüncü kova: e-posta başına saatte 30 deneme (IP'den bağımsız); aşılınca kilit yerine yanıtı geciktir ve hesap sahibine "şüpheli giriş denemesi" postası.
- Test önerisi: `login_attempts_from_many_ips_share_an_account_bucket`.
- Efor: S
- İlgili: K36 · ASVS V2.2.1

### SEC-17 Doküman deposunda git dışı 15 kod arşivi var, 3'ünde `.env`
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `davetkart-docs/archive/local-snapshots/` (148 MB, 15 arşiv; `.gitignore:5` ile git dışı)
- Senaryo: Eski faz çalışmalarının `.tgz` arşivleri diskte duruyor; üçünün dosya listesinde `.env` var. Arşivler git'e girmiyor (doğrulandı), ama klasör bulut eşitlemesine, yedeğe ya da yanlışlıkla paylaşıma açık.
- Kanıt: `evidence/commands/SEC-local-archives.txt` (`git ls-files` → 0; `.env içeren arşiv sayısı` → 3). Arşivler **açılmadı**; yalnızca dosya adı listeleri okundu.
- Etki: O `.env` dosyalarındaki anahtarlar (yerel veritabanı parolası, olası Gemini anahtarı) arşivle birlikte dolaşır.
- Neden önemli (öğretici not): `.gitignore` bir dosyayı **depodan** korur, diskten değil. Sır içeren bir dosyanın kopyası, sırrın kendisidir.
- Öneri: Arşivleri sil ya da şifreli bir kasaya taşı; içlerindeki anahtarlar hâlâ geçerliyse döndür (bu senin işin).
- Test önerisi: —
- Efor: S
- İlgili: `_restructure/REPORT.md` §2 · H14

### SEC-18 Token'ı `localStorage` yerine `httpOnly` çerezde tut
- Seviye: 💡 Öneri
- Kanıt türü: KOD OKUMASI
- Nerede: `frontend:src/services/auth.ts:136-156`
- Senaryo: Oturum token'ı `localStorage`'da; sayfada çalışan her betik okuyabilir. Bugün tehlikeli render kalıbı yok (tarama boş), ama 165 şablon bileşeni ve üç boyutlu kütüphaneler büyük bir yüzey.
- Kanıt: dosya okundu.
- Etki: XSS çıkarsa oturum çalınır ve 30 gün geçerlidir.
- Neden önemli (öğretici not): `httpOnly` çerez JavaScript'ten okunamaz; XSS oturumu **kullanabilir** ama **çalamaz**. Bedeli CSRF savunmasıdır (Sanctum SPA kipi bunu `SameSite` ve XSRF token'la çözer). API ve SPA aynı alan adında olduğu için (Nginx yapılandırması) bu geçiş mümkün.
- Öneri: Yayından sonra: Sanctum'un çerez tabanlı SPA kimlik doğrulamasına geç. Önce `SEC-04` (CSP) ile ikinci kilidi kur.
- Test önerisi: —
- Efor: L
- İlgili: K5 · ASVS V3.4

## Tablolar

### Rota sahiplik tablosu

Kaynak: `routes/api.php` (okundu) ve `evidence/commands/FE-route-list.json`. "K" = sondada koşturuldu, "O" = kod okuması.

| Uç | Kimlik | Sahiplik kontrolü | Hız sınırı | Kanıt |
|---|---|---|---|---|
| `POST /auth/register`, `/login`, `/forgot-password`, `/reset-password` | yok | — | `auth` (e-posta+IP 5/dk, IP 20/dk) | K (P63–P67, P83, Q09–Q13) |
| `POST /auth/logout`, `GET/PATCH /auth/me` | token | kendi kaydı (`$request->user()`) | `api` | K (P69) |
| `DELETE /auth/me`, `PUT /auth/password`, `POST /auth/email-change` | token + mevcut parola | kendi kaydı | `auth` | K (P72, P80, P81) |
| `GET/DELETE /auth/sessions[/{id}]` | token | `$user->tokens()->whereKey()` (`RevokeSessionAction.php:24`) | `api` | K (P68) |
| `GET/POST /invitations` | token | `$user->invitations()` | `api` | K (P08, P09) |
| `GET/PUT/DELETE /invitations/{id}` | token | `InvitationPolicy` | `api` | K (P02, P03, P07) |
| `POST /invitations/{id}/publish` | token | `InvitationPolicy::publish` + paywall | `api` | K (P04, P11, P14) |
| `POST /invitations/{id}/checkout` | token | `Gate::authorize('publish')` (`PaymentController.php:43`) | `gift-code` (kod varsa) | K (P05, P12) |
| `POST /payments/checkout` | token | kullanıcının kendisi | `gift-code` (kod varsa) | K (P13a) |
| `GET /invitations/{id}/rsvps` | token | Policy (üst kayıt) | `api` | K (P06) |
| `DELETE /rsvps/{id}` | token | `RsvpPolicy::delete` → davetiye sahibi | `api` | K (P27) |
| `POST /invitations/{id}/media`, `DELETE …/media/{id}` | token | Policy + davetiyenin galeri ilişkisi | `api` | K (P50, P54) · silme O |
| `GET /orders`, `GET /orders/{id}` | token | `$user->orders()` / `OrderPolicy` | `api` | K (P46) |
| `POST/DELETE /orders/{id}/refund-request` | token | `OrderPolicy::view` | `api` | K (P44, P45, P47) |
| `GET /pricing`, `GET /account/entitlements` | token | parametre yok, kullanıcının kendisi | `api` | K (P01) · içerik O |
| `POST /gift-codes/preview` | token | — | `gift-code` (10/dk, 30/saat) | K (P37, P43) |
| `POST /assistant/chat` | token | kullanıcı kotası | `assistant` | K (P01 kimliksiz 401) · gövde koşturulmadı |
| `GET /public/plans`, `GET /public/invitations/{id}` | yok | yalnızca `published` | `api` | K (P16, P30, P85) |
| `POST/PUT /public/invitations/{id}/rsvps[/{rsvp}]` | yok | davetiyenin ilişkisi + düzenleme kodu | `rsvp` | K (P24–P29) |
| `POST /public/invitations/{id}/media` | yok | yalnızca `published`; tür beyaz listesi | `media` | K (P51–P55) |
| `POST /public/payments/webhook` | imza | `provider_ref` | `api` | K (P19–P23) |
| `POST /public/payments/shopier/callback`, `/osb` | imza | `platform_order_id` (ULID) | `api` | O (`SEC-03`) |
| `POST /public/contact` | yok | — | `contact` (3/dk, 10/saat) | O |
| `POST /public/email-change/confirm` | imzalı bağlantı | imza kullanıcıyı ve eski adresi kapsar | `auth` | K (Q03–Q07) |

### OWASP ASVS 4.0.3 Seviye 2 (başlık düzeyinde)

| Başlık | Durum | Not ve kanıt |
|---|---|---|
| V2 Kimlik doğrulama | ❌ kısmi | Argon2id, sabit zamanlı giriş, sıfırlama ✅ · parola uzunluğu ve sızıntı denetimi ❌ (`SEC-05`) · e-posta doğrulama ❌ (`SEC-09`) · hesap bazlı fren ❌ (`SEC-16`) · çok etkenli doğrulama yok (N-A sayılmadı: L2 önerir) |
| V3 Oturum yönetimi | ✅ | 30 gün mutlak ömür, çıkışta iptal, parola değişince diğerleri kapanır (P69, P70, Q06, Q12) · token `localStorage`'da (`SEC-18`) |
| V4 Erişim denetimi | ✅ | 11 BOLA denemesi 404; toplu atama kapalı (P02–P10, P27, P45, P46, P68) |
| V5 Doğrulama, temizleme, kodlama | ✅ | NUL, yarım JSON, `integer:strict`, URL şeması (P31–P36); frontend'de ham HTML render'ı yok |
| V7 Hata işleme ve loglama | ✅ | Zarf tek tip; `debug` yalnızca `APP_DEBUG=true` (sondada görüldü: P83; üretimde kapalı olmalı, `docs/10`) · loglarda kişisel veri taraması temiz |
| V8 Veri koruma | ❌ kısmi | IP hash'li, kod hash'li ✅ · saklama beyanı ve yedekler (`SEC-11`), tarihsiz davetiye (`SEC-13`), üçüncü taraf font (`SEC-12`) |
| V9 İletişim | ❓ | TLS yapılandırması certbot varsayılanı (`davetkart.conf:42-45`); canlı sunucu test edilmedi · SPA'da HSTS yok (`SEC-04`) |
| V11 İş mantığı | ❌ | `SEC-01`, `SEC-02` |
| V12 Dosyalar | ✅ | İçerikten MIME, sunucu adı, yeniden kodlama (P50–P55) · kota tasarımı (`SEC-08`) |
| V13 API | ✅ kısmi | Sözleşme tutarlı, JSON zorlaması, CORS dar (P57–P61) · Shopier callback kipi (`SEC-03`) |
| V14 Yapılandırma | ❌ | Bağımlılık açıkları (`SEC-07`), frontend başlıkları (`SEC-04`) |

### OWASP API Security Top 10 (2023)

| # | Risk | Durum | Kanıt |
|---|---|---|---|
| API1 | Nesne düzeyinde yetki | ✅ | P02–P08, P27, P45, P46, P68 |
| API2 | Kimlik doğrulama | ✅ kısmi | P01, P63–P71 · `SEC-05`, `SEC-09`, `SEC-16` |
| API3 | Özellik düzeyinde yetki | ✅ | P09, P10, P12, P16 (kapalı modülün verisi yanıtta yok) |
| API4 | Kaynak tüketimi | ❌ kısmi | Sınırlar var (P43, P83, P85) · `SEC-06`, `SEC-08` |
| API5 | İşlev düzeyinde yetki | ✅ | Yönetici işlemleri yalnızca konsolda (`refunds:*`, `gift-codes:*`, `pricing:*`); HTTP'de yönetici ucu yok |
| API6 | Hassas iş akışlarına sınırsız erişim | ❌ | `SEC-01` (indirim), `SEC-02` (iade) |
| API7 | SSRF | N-A | Sunucu kullanıcı girdisinden URL çağırmıyor (`mapUrl` yalnızca saklanıyor); AI sağlayıcı adresi sabit |
| API8 | Güvenlik yapılandırması | ❌ kısmi | `SEC-03`, `SEC-04`, `SEC-07` |
| API9 | Envanter yönetimi | ✅ | Tek sürüm, 40 rota, hepsi `routes/api.php`'de; ölü rota görülmedi |
| API10 | Üçüncü taraf API'lerinin güvensiz tüketimi | ✅ kısmi | Shopier OSB imza + tutar doğrulaması (kod) · callback kipi (`SEC-03`) · Gemini anahtarı başlıkta, URL'de değil (`GeminiProvider.php:87`) |

### Canlı sonda özeti

| Dosya | OK | Açık | Bilgi | Not |
|---|---|---|---|---|
| `evidence/commands/SEC-api-probe.txt` | 81 | 8 | 15 | Açıkların dağılımı: P13 (`SEC-01`), P47 (`SEC-02`), P67 ×3 (`SEC-05`), P86 (`SEC-06`), P59 (yalnızca `artisan serve`; üretim `php.ini`'sinde `expose_php = Off`, bulgu değil), P60 (yanlış alarm: açıklaması `SEC-api-probe-2.txt` başında) |
| `evidence/commands/SEC-api-probe-2.txt` | 9 | 0 | 5 | E-posta değişikliği ve parola sıfırlama bağlantıları |

Sondanın `.env` farkları: `PAYMENT_METHODS=card,gift_code`, `QUEUE_CONNECTION=sync`, `APP_DEBUG=true` (kopya `.env.example`'dan üretildi). Bu yüzden 429 yanıtında `debug` bloğu görünüyor; üretimde görünmemeli.

## Regresyon

| # | Kaynak | Bulgu | Durum | Kanıt türü | Kanıt |
|---|---|---|---|---|---|
| R1 | Review §1.1 / K-1 | Yayından sonra `PUT` ile üst plan modülü (paywall bypass) | ✅ kapandı | KOŞTURULDU | P15: dört modül ve iki Gold şablonu 402 `PAYWALL_TIER_INSUFFICIENT`; P16: misafir yanıtında modül ve IBAN yok |
| R2 | Review §1.2 / K-4 | Geç gelen `paid` yutuluyor | ✅ kapandı | KOŞTURULDU | P23: `expired → paid`; kod `Log::warning` yazıyor (`HandlePaymentCallbackAction.php:134-139`) |
| R4 | Review §2.2 | Token ömrü; `sanctum:prune-expired` | ✅ kapandı | KOŞTURULDU | P70 (31 günlük token 401); `config/sanctum.php:66`; zamanlayıcı `routes/console.php:82` |
| R5 | Review §2.3 | `TrustProxies` / gerçek IP | ✅ kapandı (bu topolojide) | KOŞTURULDU | P24: güvenilmeyen `X-Forwarded-For` yok sayıldı. Nginx → PHP-FPM doğrudan olduğu için vekil yok. CloudFront/ALB API'nin önüne gelirse `TRUSTED_PROXIES` şart (`05-operations.md`, R5 satırı) |
| R6 | Review §2.4 (akışlar) | Parola sıfırlama, e-posta doğrulama, hesap silme | 🟡 kısmen | KOŞTURULDU | Sıfırlama ✅ (Q09–Q13), hesap silme ✅ (P80–P82), **e-posta doğrulama yok** (`SEC-09`) |
| R6 | Review §2.4 (KVKK) | Saklama süresi, `data:purge` | 🟡 kısmen | KOD OKUMASI | `PurgeExpiredData.php` üç kuralı uyguluyor ve günlük zamanlanmış; boşluklar `SEC-11`, `SEC-13` |
| R9 | Review §5.4–5.5 | Hız sınırları (CGNAT), video boyutu, mükerrer LCV | 🟡 kısmen | KOŞTURULDU | Mükerrer LCV ✅ (P26). LCV/medya kovaları genişletilmiş ama genel tavan IP'ye bağlı (`SEC-06`). Video 20 MB, davetiye başına 100 adet (`SEC-08`) |
| R11 | Test denetimi K-2…K-8 (canlı) | NUL, `İ`, `Retry-After`, yarım JSON, `integer:strict`, `mapUrl` | ✅ kapandı | KOŞTURULDU | P31–P35, P66, P43/P83 (`Retry-After` başlığı) |
| R14 | Faz 11–12 | Hediye kodu kötüye kullanımı · Shopier · open redirect · tutar | 🟡 kısmen | KOŞTURULDU + KOD OKUMASI | Hediye kodu: tekrar kullanım, plan, tükenme, tahmin freni ✅ (P38–P43); **yarış koşturulmadı** (kilit kodu okundu: `ReserveGiftCodeAction.php:43-46`). Shopier OSB imza + tutar ✅ (kod), `status` imzasızlığı `callback` kipinde açık (`SEC-03`). Open redirect yok (kod) |
| R15 | Faz 14 (güvenlik) | Hak iptali, e-posta değişikliği | 🟡 kısmen | KOŞTURULDU | E-posta değişikliği ✅ (Q01–Q08), sahiplik ✅ (P45), donmuş hak ✅ (P48); boşluk `SEC-02` |

## Kullanılan araçlar ve skill'ler / kullanılamayanlar

- Kullanılan: canlı sonda (`evidence/scripts/sec-api-probe.php`, `sec-api-probe-2.php`: Laravel'i kopyadan önyükleyen, yalnızca `127.0.0.1:8000`'e istek atan betikler), sır taraması (`sec-secret-scan.sh`, değerleri maskeler), `composer audit`, `npm audit` (ikisi de dilim ajanının kesilmeden önce kaydettiği çıktılar), `grep`/`awk`.
- Kullanılamayan: **Context7** (bağlı değil). GitHub Advisory ile çapraz doğrulama **yapılmadı**; tavsiye kimlikleri ve etkilenen sürümler `composer audit` çıktısından (kaynak: FriendsOfPHP/security-advisories).
- Koşturulmayan: yarış durumu betikleri (Windows'ta `artisan serve` tek süreç; eşzamanlı CLI süreçleriyle kanıt üretmek token bütçesi nedeniyle atlandı), asistan ucu gövdesi, iletişim formu, Shopier uçlarına sahte imzalı istek.
- Skill: `superpowers:systematic-debugging` ve `verification-before-completion` ayrıca çağrılmadı; sondanın iki yanlış değerlendirmesi (P60, P81) elle doğrulanıp `SEC-api-probe-2.txt` başına düzeltme notu olarak yazıldı.

## Koşturulan komutlar

| Dosya | İçerik |
|---|---|
| `evidence/commands/SEC-api-probe.txt` | `php evidence/scripts/sec-api-probe.php` (P01–P86) |
| `evidence/commands/SEC-api-probe-2.txt` | `php evidence/scripts/sec-api-probe-2.php` (Q01–Q14) |
| `evidence/commands/SEC-secret-scan.txt` | `bash evidence/scripts/sec-secret-scan.sh` (üç depo, bütün dallar; yalnızca test sabitleri ve yer tutucular) |
| `evidence/commands/SEC-local-archives.txt` | git dışı arşiv sayımı |
| `evidence/commands/B2-composer-audit.txt`, `B2-composer-outdated-direct.txt`, `B2-composer-show-direct-latest.txt` | backend bağımlılıkları |
| `evidence/commands/B2-npm-audit-omit-dev.txt`, `B2-npm-audit-all.txt`, `B2-npm-outdated.txt` | frontend bağımlılıkları |

## İsmail'e sorular

1. **`SEC-01`:** "İlk yayın" indirimi kullanıcı başına bir kez mi olmalı, yoksa "ilk ödeme tamamlanana kadar açılan her sipariş" bilinçli bir tercih mi (K131 "bekleyen sayılmaz" diyor)?
2. **`SEC-02`:** Yayınlanmış ve silinmiş bir davetiyenin hakkı iade edilebilir mi? Önerim: hayır; üç günlük pencere hakkı **yeniden kullanmaya** izin versin, paraya değil.
3. **`SEC-03`:** Shopier `callback` kipini tamamen kaldırayım mı diye önerim var; canlı doğrulamayı (K94) OSB ile yapmak senin için mümkün mü?
4. **`SEC-09`:** E-posta doğrulaması yayından önce mi, sonra mı? Önerim: yayından önce en azından ilk yayın indirimini doğrulanmış hesaba bağlamak.
5. **`SEC-10`:** Shopier'e yer tutucu TCKN/telefon göndermek konusunda Shopier'den yazılı bir teyidin var mı?
