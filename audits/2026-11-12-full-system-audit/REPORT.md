# DavetKart genel sistem denetimi — nihai rapor

| | |
|---|---|
| **Denetim kimliği** | `AUD-2026-11-12` |
| **Tarih** | 12–15 Kasım 2026 |
| **Kapsam** | Backend (PHP 8.5, Laravel 13) · Frontend (React 19, Vite 6, TypeScript 5.8) · yayın altyapısı (`deploy/`, yayın planı) |
| **Denetlenen kod** | backend `origin/ccr-9a346997-bu6gve` @ `d810410` · frontend `origin/ccr-9a346997-bu6gve` @ `44caa49` |
| **Yöntem** | Salt okunur. Uzak dalların anlık görüntüsü depo dışında, yalıtılmış kopyalarda koşturuldu; hiçbir kod değişmedi, canlı sisteme istek atılmadı |
| **Yürüten** | Claude Code, Fable 5.2 (ana oturum; dilim ajanları kullanım sınırına takıldığı için dilimlerin hepsini ana oturum yürüttü) |
| **Çıktılar** | Bu rapor · [`findings/`](findings/) (beş dosya, 62 bulgu) · [`evidence/`](evidence/) (komut çıktıları, betikler, 51 mutasyon kaydı, 80 ekran görüntüsü) · [`PLAN.md`](PLAN.md) · [`README.md`](README.md) |

Kanıt türleri (B7): **KOŞTURULDU** = komut, test ya da tarayıcı çıktısı kanıt klasöründe · **KOD OKUMASI** = yalnızca
okuyarak · **VARSAYIM** = doğrulanmadı. Koşmayan her şey "koşmadı" diye yazıldı; liste Ek B'de.

---

## 1. Yönetici özeti

**Karar: koşullu hazır.** Kodun çekirdeği sağlam ve bu denetimde bunu gösteren kanıt çok: canlı sondada 102
denemenin 95'i beklenen güvenli davranışı verdi, kritik iş kurallarına yazılan 47 mantık mutantının 47'si
testler tarafından yakalandı, frontend'in 41 API çağrısının 40'ı backend'le birebir eşleşiyor, sekiz kullanıcı
yolculuğu tarayıcıda koşturuldu ve para kazandıran zincir (kayıt → davetiye → ödeme → yayın → misafir yanıtı)
uçtan uca çalıştı; iki adım koşturulamadı (Ek B). **Kritik (🔴) bulgu yok.** Yayından önce kapatılması gereken
altı yüksek (🟠) bulgu var; altısı da küçük ya da orta eforlu.

| # | Yayından önce kapatılacak | Bulgu | Efor |
|---|---|---|---|
| 1 | Hangi iki commit'in yayına çıkacağı belli değil; iki depo ayrı yükseltilirse 19 premium şablon Standart planla yayınlanabilir | `OPS-01` | S |
| 2 | Veritabanı yedeği ve geri yükleme provası yok | `OPS-02` | M |
| 3 | "İlk yayın" indirimi aynı anda açılan her siparişe uygulanıyor | `SEC-01` | M |
| 4 | Kullanılıp silinen davetiyenin hakkı için iade talebi kabul ediliyor | `SEC-02` | M |
| 5 | Shopier `callback` kipinde ödeme durumu ve tutarı imzasız | `SEC-03` | S |
| 6 | Frontend sayfaları güvenlik başlığı taşımıyor | `SEC-04` | S |

Bunlara ek olarak kalite kapısı bu dalda kırmızı (`TST-01`: tek dosyada biçim hatası; `SEC-07`: `composer audit`
sekiz bilinen açık gösteriyor). İkisi de birer komutla kapanır ama kapanmadan "doğrulanmış commit" yoktur.

**Üç tema** bulguların çoğunu açıklıyor:

1. **Kod iyi, kayıt geride.** Karar indeksi koddan 18 karar geride (`ARC-01`), Faz 16–17'nin kaydı yok
   (`ARC-02`), üretim ortam şablonu sunucudaki gerçek dosyadan sapmış (`OPS-04`), fiyat sayfası backend'de
   olmayan bir kuralı anlatıyor (`FE-52`). Sorunların yarısı kodda değil, kodu anlatan metinlerde.
2. **İki depo arasındaki sözleşme elle taşınıyor.** Hata kodları için kurulan desen (ortak dosya + doğrulama
   betiği) plan kurallarına uzatılmamış (`FE-05`); bu yüzden dağıtım sırası bir doğruluk koşulu hâline geliyor
   (`OPS-01`).
3. **Tek tek doğru, birlikte denenmemiş.** Kilitler yerinde ama hiçbir test onları korumuyor (`TST-02`);
   uçlar ve sayfalar var ama aralarında bağlanmamış yollar çıktı (`FE-51`, `FE-55`); sihirbaz her ziyarette
   taslak bırakıyor (`FE-50`). Bunları tek tek dosyalar değil, uçtan uca koşu gösterdi.

**Korunması gerekenler:** fiyatın istekten okunamadığı veri akışı, her uçta iki katmanlı sahiplik denetimi,
durum makinesi + kilit + UNIQUE ile üç katmanlı idempotans, etkiyi doğrulayan testler, sözleşme betikleri
(`npm run verify`), hataya karşı yazılmış dağıtım betikleri.

---

## 2. Puan kartı

Puanlar bu denetimin yargısıdır (0–10; 9–10 yayına hazır · 7–8 küçük işlerle hazır · 5–6 yayından önce iş var ·
5'in altı ciddi eksik). Gerekçe sütunu puanı bulgulara bağlar.

| Alan | Puan | 🟠 | 🟡 | 🟢 | 💡 | Gerekçe |
|---|---|---|---|---|---|---|
| Backend mimarisi ve kod kalitesi | **8,5** | 0 | 5 | 4 | 1 | Katmanlar okunan her uçta tutuluyor; para tam sayı, durumlar enum, 30 CHECK kısıtı. Eksikler kayıt ve belge tarafında (`ARC-01…05`) |
| Güvenlik | **7** | 4 | 9 | 4 | 1 | Çekirdek savunmalar canlı sondada doğrulandı; para etkili iki iş kuralı boşluğu ve iki yapılandırma eksiği yayından önce kapanmalı |
| Testler ve kalite kapısı | **8** | 0 | 3 | 2 | 1 | 1056 test, 47/47 mantık mutantı öldü. Kapı bu dalda kırmızı, kilitler testsiz, tarayıcı testi yok |
| Frontend mimarisi ve sözleşme | **7,5** | 0 | 4 | 6 | 0 | Sözleşme temiz, `any` yok, ağ tek kapıdan. Ana paket 1,64 MB, çeviri yarım, hata sınırı yok |
| Kullanıcı yolculukları, erişilebilirlik, performans | **7** | 0 | 5 | 3 | 1 | Sekiz yolculuk koştu, ana zincir çalışıyor. Taslak birikmesi, ulaşılamayan misafir yüklemesi, yavaş mobil ilk yükleme, duyurulmayan hata mesajları |
| İşletim ve yayına hazırlık | **5,5** | 2 | 3 | 3 | 1 | Betikler özenli; yedek, izleme ve "hangi commit" sorusu açık |
| Dokümantasyon ve karar kaydı | **6,5** | — | — | — | — | Çok ve nitelikli belge var; güncellik sorunu (`ARC-01`, `ARC-02`, `ARC-05`, `FE-07`, `OPS-04`). Ayrı bulgu sayımı yok, ilgili bulgular yukarıdaki satırlarda |

| Toplam | 🔴 Kritik | 🟠 Yüksek | 🟡 Orta | 🟢 Düşük | 💡 Öneri | KOŞTURULDU | KOD OKUMASI | VARSAYIM |
|---|---|---|---|---|---|---|---|---|
| **62 bulgu** | 0 | 6 | 29 | 22 | 5 | 36 | 26 | 0 |

Dosya başına: mimari 10 · güvenlik 18 · test 6 · frontend ve uçtan uca 19 · işletim 9
(`node evidence/scripts/90-report-tools.mjs stats`).

---

## 3. Tam / eksik

Ürün yetenekleri açısından neyin çalıştığı görüldü, neyin eksik ya da doğrulanmamış olduğu. "Görüldü" sütunu
kanıtın türünü söyler.

### 3.1 Tam (çalıştığı görüldü)

| Yetenek | Nasıl görüldü |
|---|---|
| Kayıt, giriş, çıkış, oturum listesi, hız sınırı | Tarayıcı (yolculuk 1) + canlı sonda + mutasyon (M19, M28) |
| Davetiye oluşturma, düzenleme, otomatik kaydetme | Tarayıcı (yolculuk 2) |
| Plan duvarı: yayında ve güncellemede plan denetimi (K-1) | Sonda P15 + mutasyon M01–M03 + tarayıcı (yolculuk 4) |
| Fiyatın sunucuda hesaplanması, ilk yayın indirimi, hediye kodu | Sonda P12 + mutasyon M06, M12, M13, M36 + tarayıcı (yolculuk 3) |
| Ödeme → dönüş sayfası → yayın (sahte sürücü) | Tarayıcı (yolculuk 3); gerçek sağlayıcı koşmadı |
| Geç gelen ödeme bildirimi, tekrar oynatma, tutar doğrulaması | Sonda P21–P23 + mutasyon M04, M05, M07, M08 |
| Misafir sayfası, LCV, kota, kendi yanıtını güncelleme | Tarayıcı (yolculuk 5) + mutasyon M17, M39, M40 |
| Hesap ayarları: plan hakları, iade talebi, e-posta değişikliği | Tarayıcı (yolculuk 6) + sonda Q01–Q08 + mutasyon M30–M32 |
| 373 şablonun çizimi; Faz 15–17'den 17 şablon mobilde | `verify:render` + tarayıcı (yolculuk 7) |
| Hata sözleşmesi (28 kod, iki depoda aynı) | Betik (`FE-error-codes-compare.txt`) |
| Dağıtım betikleri, kuyruk servisi, zamanlayıcı | Kod okuması (sunucuda koşmadı) |

### 3.2 Eksik ya da yarım

| Eksik | Bulgu | Not |
|---|---|---|
| E-posta doğrulaması | `SEC-09` | Kayıt anında adres doğrulanmıyor |
| Misafir fotoğraf/video yüklemesinin arayüzü | `FE-51` | Uç açık, arayüzden ulaşılamıyor |
| "Yayın süresi" ve ücretli uzatma | `FE-52` | Fiyat sayfası anlatıyor, kodda yok |
| Davetiyeye bağlı olmayan paket alımının arayüz yolu | `FE-55` | Yalnızca doğrudan adresle |
| Konum araması | `FE-08` | Frontend hazır, backend ucu yok |
| Sekiz dilin çevirisi | `FE-01` | Menüler çevrili, içerik Türkçe |
| Hata sınırı, 404 sayfası, paylaşım önizlemesi | `FE-02`, `FE-06`, `FE-04` | — |
| Veritabanı yedeği, izleme, alarm | `OPS-02`, `OPS-03` | Yayın planında Y11 |
| Tarayıcı testleri, satır kapsamı, kilit testleri | `TST-04`, `TST-03`, `TST-02` | — |
| Havale/EFT | — | Ayarla kapalı (`PAYMENT_METHODS`); denetlenmedi |

### 3.3 Var ama bu denetimde doğrulanamadı

Shopier (gerçek ödeme), S3, SES, Gemini ve Sentry yolları yalnızca okundu. Hediye kodu yarışı (eşzamanlı
kullanım) koşturulmadı. Sunucunun bugünkü durumu yalnızca yayın planı kaydından biliniyor. Ayrıntı: Ek B.

---

## 4. Yüksek öncelikli bulgular (tam metin)

Altı bulgunun tam metni, bulgu dosyalarından aynen alınmıştır.

#### SEC-01 "İlk yayın" indirimi aynı anda açılan her siparişe uygulanıyor
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

#### SEC-02 Kullanılıp silinen davetiyenin hakkı iade edilebiliyor; yönetici göremiyor
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

#### SEC-03 Shopier `callback` kipinde `status` ve tutar imzasız
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

#### SEC-04 Frontend sayfalarında güvenlik başlığı yok; token `localStorage`'da
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

#### OPS-01 Yayına çıkacak commit belirsiz; iki depo ayrı yükseltilirse 19 premium şablon korumasız
- Seviye: 🟠 Yüksek
- Kanıt türü: KOŞTURULDU
- Nerede: backend `origin/main` = `origin/release-v1.0` = `03d3940` (26 Ekim) ↔ denetlenen `d810410` (4 commit ileride) · frontend `origin/main` = `47aedc8` ↔ denetlenen `44caa49` (71 commit ileride, 1 geride) · frontend'de `release-v1.0` dalı yok · iki depoda etiket yok
- Senaryo: 1) Sunucu `main`'i çekiyor (plan kaydı Y8.2a). Backend `main`'inde 13 premium şablon Gold'a bağlı. 2) Frontend'in yeni şablonları (Faz 15–17, 71 commit) `main`'e alınıp Y10'da yayınlanır; backend'in dört commit'i (Faz 16–17 `preset_tiers`) unutulur ya da sonraya kalır. 3) Arayüz 32 şablonu "Premium · Gold+" diye gösterir; sunucu yalnızca 13'ünü tanır. 4) Kullanıcı Standart planla (249 ₺) premium bir şablon seçip yayınlar; sunucu 402 dönmez. Fark şablon başına 150 ₺.
- Kanıt: `evidence/commands/OPS-branch-state.txt`: `rev-list --count origin/main..origin/ccr-9a346997-bu6gve` → backend 4, frontend 71 (tersi 0 ve 1); `git show origin/main:config/davetkart.php | grep -c "=> 'gold',"` → 15 (13 şablon + 2 modül), denetlenen dalda 34 (32 + 2); frontend `minimumTier` sayısı `main`'de 13, denetlenen dalda 32.
- Etki: Para kaybı ve geri alınması zor bir durum: Standart'la yayınlanmış premium davetiyeler sonradan kapatılırsa müşteri şikâyeti, açık bırakılırsa fiyatlandırma delinmiş olur. Ayrıca denetlenen dalın kalite kapısı kırmızı (`TST-01`) ve Faz 16–17'nin kaydı yok (`ARC-02`); yani "yayına hazır commit" bugün hiçbir dalda işaretli değil.
- Neden önemli (öğretici not): İki depo tek bir ürünün iki yarısıdır ve aralarındaki sözleşme (hangi şablon hangi planda) iki tarafta ayrı ayrı durur (`FE-05`). Böyle bir sözleşmede **dağıtım sırası** bir doğruluk koşuludur: kuralı uygulayan taraf (sunucu) önce, kuralı gösteren taraf (arayüz) sonra yayınlanır. Etiket, "hangi iki commit birlikte doğrulandı" sorusunun tek dürüst cevabıdır.
- Öneri: 1) Sıra: backend'in dört commit'i → `main` (`composer check` yeşil olduktan sonra) → `deploy.sh`; ardından frontend → `main` → Y10. 2) İki depoda aynı adla etiket (`v1.1.0`); `deploy.sh` yayınlanan commit'i günlüğe yazıyor, etiketi de yazsın. 3) Frontend `npm run check`'e "premium şablon listesi backend sözleşmesiyle aynı" denetimi (`FE-05`'teki `verify:plans`). 4) Frontend `main`'deki `47aedc8` (bağımlılık temizliği) denetlenen dala alınmalı (`SEC-14`).
- Test önerisi: `verify:plans`: `src/data.ts`'teki `minimumTier` kimlikleri ↔ `contracts/plan-rules.json`. Öldürmesi gereken mutant: sözleşme dosyasından bir premium kimliği silmek.
- Efor: S
- İlgili: `ARC-08` (dal hijyeni) · `ARC-02` · `TST-01` · `FE-05` · `SEC-14`

#### OPS-02 Veritabanı yedeği ve geri yükleme provası yok
- Seviye: 🟠 Yüksek
- Kanıt türü: KOD OKUMASI
- Nerede: `YAYIN-PLANI.md` Y11.5 (gece `pg_dump` → S3), Y11.6 (geri yükleme provası): ilerleme kaydında yok · `backend:deploy/` (yedek betiği yok; `deploy/cron/davetkart` yalnızca `schedule:run`) · tek yedek: Lightsail günlük disk görüntüsü, son 7 gün (plan kaydı Y4.4)
- Senaryo: A) Hatalı bir göç ya da elle çalıştırılan bir `DELETE` siparişleri bozar. Disk görüntüsü bütün sunucuyu dünkü hâline döndürür: aradaki ödemeler ve LCV'ler de gider; tek tabloyu geri getirmek mümkün değil. B) Lightsail hesabı ya da bölgesi erişilemez olur; görüntüler aynı hesapta. C) Yedek alınıyor sanılır, ilk ihtiyaçta dosyanın açılmadığı görülür.
- Kanıt: `grep -rl pg_dump backend/deploy backend/docs/rehber/deploy` → boş; `YAYIN-PLANI.md` §8'de Y11 satırı yok; `YAYIN-DEVIR.md:119` Y11'i "yapılacak" diye listeliyor.
- Etki: Sipariş, hak ve misafir yanıtı kaybı; kurtarma noktası 24 saat. Bugün canlıda müşteri verisi yok (frontend yayında değil), yani bu açığın kapatılması için en ucuz an şimdi.
- Neden önemli (öğretici not): Yedeğin iki ölçüsü vardır: ne kadar veri kaybedersin (RPO) ve ne kadar sürede dönersin (RTO). Disk görüntüsü "sunucu yandı"yı, mantıksal döküm (`pg_dump`) "veri bozuldu"yu çözer; ikisi farklı felaketlerdir. Ve denenmemiş yedek bir umuttur: geri yükleme provası yedeğin testidir.
- Öneri: `deploy/backup/pg-dump.sh` (`pg_dump -Fc` → `gzip` gerekmez → `aws s3 cp` ayrı bucket'a, başarısızlıkta sıfır dışı çıkış) + `/etc/cron.d` satırı 02:00 UTC + S3 ömür kuralı (30 gün) + Sentry Crons izleyicisi. Bir kez: dünkü dökümü yerelde `pg_restore` ile aç, `orders` ve `invitations` sayılarını karşılaştır, süreyi plana yaz. Kayıt açılmadan önce tamamlanmalı.
- Test önerisi: Aylık geri yükleme provası (takvim işi); betik için: boş veritabanında döküm → geri yükle → satır sayıları eşit.
- Efor: M
- İlgili: Y11.5, Y11.6 · `SEC-11` (yedeklerde saklama süresi ve gizlilik metni)

---

## 5. Diğer bulgular

Tam metinler bulgu dosyalarında: [`01-architecture.md`](findings/01-architecture.md) ·
[`02-security.md`](findings/02-security.md) · [`03-testing.md`](findings/03-testing.md) ·
[`04-frontend-e2e.md`](findings/04-frontend-e2e.md) · [`05-operations.md`](findings/05-operations.md).
"Kanıt" sütunu: K = KOŞTURULDU, O = KOD OKUMASI.

### 5.1 Orta (🟡) — 29 bulgu

| ID | Seviye | Kanıt | Başlık | Nerede | Öneri | Efor |
|---|---|---|---|---|---|---|
| ARC-01 | 🟡 | K | Karar indeksi K128–K145'i bilmiyor; "sıradaki boş numara" yanlış | `davetkart-docs/decisions/DECISION-INDEX.md:8` ("Sıradaki boş numara: K128") · `backend:d… | İndekse K128–K145 satırlarını ekle (kaynak sütunu: backend `docs/rehber/fazlar/FAZ-13.md` §4 ve `FAZ-14.md`), başlığı "Sıradaki boş numara: **K146**" yap. `_restructure/… | S |
| ARC-02 | 🟡 | K | Faz 16 ve 17'nin faz kaydı yok; Faz 15 kaydı "kalite kapısı koşmadı" diyor | `backend:docs/rehber/fazlar/` (en yeni dosya `FAZ-15.md`) · `backend:docs/rehber/fazlar/F… | `FAZ-16.md` ve `FAZ-17.md` (ne eklendi, hangi karar, doğrulama durumu) + hangi şablonun neden Gold olduğu kararını K numarasıyla kaydet. Bulut ortamına PHP 8.5 kurulamıy… | S |
| ARC-03 | 🟡 | K | K18 dosyaların %92'sinde çiğneniyor; 79 dosyanın kılavuzu yok | `backend:routes/api.php` (437 satırın büyük kısmı açıklama bloğu) · `backend:app/Provider… | 1) En ucuz: kuralı gevşetip gerçeği kabul et (ör. "en fazla 8 satır") ve bunu karar olarak yaz. 2) Sağlam: uzun blokları kılavuza taşı, `composer check`'e yorum bloğu uz… | L |
| ARC-04 | 🟡 | O | K55 "yerel disk kalır" geçerli görünüyor ama yayın planı S3 kuruyor | `davetkart-docs/decisions/DECISION-INDEX.md:67` (K55, "geçerli · ⚠️") · `backend:config/d… | K55'i "geçersiz kılındı → K146" yap ve yeni kararı yaz. `APP_ENV=production` iken `davetkart.media.disk === 'public'` ise açılışta uyarı logla (ya da `about` komutunda g… | S |
| ARC-05 | 🟡 | K | Eski `claude/…` yolları: backend'de 25 dosya; backend'in kendi `claude/` klasörü ikinci ev | `backend:docs/03-MIMARI-PLAN.md:314` · `backend:docs/07-GELISTIRME-YOL-HARITASI.md:382,55… | `backend/claude/` içeriğini `davetkart-docs`'a taşı (`decisions/addenda/`, `phases/faz-05…10/`, `audits/2026-09-23-…`, `audits/2026-09-24-test-audit/`, `audits/2026-10-0… | M |
| SEC-05 | 🟡 | K | Zayıf parolalar kabul ediliyor | `backend:app/Http/Requests/Auth/RegisterRequest.php:37` · `ResetPasswordRequest.php:35` ·… | Üç istekte ortak bir kural nesnesi: `Password::min(12)`. Sızıntı denetimi için `->uncompromised()` Have I Been Pwned'a (k-anonimlik, parolanın kendisi gitmez) istek atar… | S |
| SEC-06 | 🟡 | K | Genel hız sınırı IP anahtarlı: misafir trafiği davetiye sahibini de kilitliyor | `backend:app/Providers/AppServiceProvider.php:363-368` (`api` kovası: 60/dk, yalnızca IP)… | `apiLimits`: `$request->user()` varsa `by('api\|user\|'.$id)` ve 120/dk; yoksa IP. Misafir okuma ucu (`GET /public/invitations/{id}`) zaten cache'li ve ETag'li: ona ayrı… | M |
| SEC-07 | 🟡 | K | Composer bağımlılıklarında 8 bilinen açık; `composer audit` kırmızı | `backend:composer.lock` → `symfony/http-foundation v8.1.9` (4 tavsiye), `symfony/http-ker… | `composer update "symfony/*" laravel/framework --with-all-dependencies` (hepsi semver güvenli: `laravel/framework` 13.35 → 13.42), ardından `composer check`. `ShopierGat… | S |
| SEC-08 | 🟡 | O | Kimliksiz misafir davetiye başına 5 GB yükleyebilir; yetim dosya kotayı 24 saat tutar | `backend:config/davetkart.php:139-150` (LCV fotoğrafı 200 × 15 MB, LCV videosu 100 × 20 M… | Davetiye başına toplam misafir baytı sınırı (ör. 1 GB) ve plan bazlı kota; yetim süresini 24 saat → 1 saat; yetimleri kota sayımından çıkar ya da ayrı, küçük bir "bekley… | M |
| SEC-09 | 🟡 | K | E-posta doğrulaması yok | `backend:app/Actions/Auth/RegisterUserAction.php:31-41` (kayıt anında token) · `backend:a… | Kademeli: 1) Kayıtta doğrulama postası gönder (`EmailChangeLink` deseninin aynısı yeniden kullanılabilir). 2) Doğrulanmamış hesap davetiye hazırlayabilsin ama checkout v… | L |
| SEC-10 | 🟡 | O | Shopier'e uydurma TCKN ve telefon gönderiliyor | `backend:config/payment.php:54-61` (`id_nr => '11111111110'`, `phone => '05000000000'`, s… | Shopier desteğinden dijital ürün için bu alanların zorunlu olup olmadığını yazılı sor; cevaba göre ya alanları kaldır ya da checkout'ta kullanıcıdan telefon iste. Kararı… | S |
| SEC-11 | 🟡 | O | Gizlilik metni "hemen silinir" diyor; yedekler 7–30 gün tutuyor; üçüncü taraflar adıyla yok | `frontend:src/pages/legal/PrivacyPage.tsx` · `davetkart-docs/operations/deployment/YAYIN-… | Metne "yedeklerden en geç 30 gün içinde silinir" cümlesini ve veri işleyenlerin listesini ekle; `verify-render`'daki beklenen ifadeyi buna göre güncelle. Yedek bucket'ın… | S |
| SEC-12 | 🟡 | K | Her sayfa Google Fonts'u Google'dan yüklüyor | `frontend:src/index.css:1` (`@import url('https://fonts.googleapis.com/css2?…')`) · `fron… | Fontları `@fontsource/*` paketleriyle ya da `public/fonts/` altında kendi alan adından sun; şablonlardaki `fontlar.ts` yardımcılarını yerel `@font-face` tanımlarına çevi… | S |
| SEC-13 | 🟡 | O | `data:purge` tarihi olmayan davetiyelerin misafir verisini hiç silmiyor | `backend:app/Console/Commands/PurgeExpiredData.php:99-106` (`->whereNotNull('event_at')->… | Tarih yoksa `published_at` (o da yoksa `created_at`) + 12 ay gibi bir yedek kural; kararı K98'e ek olarak yaz. | S |
| TST-01 | 🟡 | K | `composer check` bu dalda kırmızı (Pint); CI iki adımda kırmızı olmalı | `backend:tests/Feature/TemplateCatalogueTest.php:114` (`private const FAZ17_PRESETS` meto… | `vendor/bin/pint tests/Feature/TemplateCatalogueTest.php` (sabiti yukarı taşır) → `composer check` → sonucu `FAZ-15.md` §3'e ve yazılacak `FAZ-16.md`/`FAZ-17.md`'ye işle… | S |
| TST-02 | 🟡 | K | Kilitlerin hiçbiri testle korunmuyor: 4 kilit mutantının 4'ü hayatta | `backend:app/Actions/GiftCode/ReserveGiftCodeAction.php:45` (M14) · `app/Actions/Payment/… | İki katman. Ucuz ve kesin: Action testinde `DB::listen` ile koşan SQL'i yakala, `for update` içerdiğini doğrula (dört mutantı da öldürür, 5 satır). Sağlam: iki PostgreSQ… | M |
| TST-04 | 🟡 | O | Gerçek frontend + gerçek backend'i koşturan otomatik test yok | `frontend:package.json` (test koşucusu yok: Vitest, Jest, Playwright, Cypress bağımlılığı… | Sahte ödeme sürücüsüyle (`PAYMENT_PROVIDER=fake`) üç Playwright yolculuğu: (1) kayıt → davetiye → hediye koduyla yayın, (2) misafir LCV'si → sahibin panelinde görünmesi,… | L |
| FE-01 | 🟡 | K | Dil seçici on dil sunuyor, arayüzün büyük kısmı yalnızca Türkçe | `frontend:src/i18n.ts:32-43` (on dil) · `frontend:src/locales/*/translation.json` (dil ba… | En ucuz: `SUPPORTED_LANGUAGES`'ı `tr` ve `en` ile sınırla (hata sözlüğü zaten bu ikisinde), diğer sekiz dili gerçekten çevrilene kadar gizle. Sağlam: çekirdek 66 dosyanı… | L |
| FE-02 | 🟡 | O | Hata sınırı yok: render hatası ve yüklenemeyen chunk ham hata ekranı veriyor | `frontend:src/App.tsx:38-127` (hiçbir rotada `errorElement` yok) · `frontend:src/componen… | 1) Kök rotaya `errorElement: <RouteError />` (marka, "Sayfayı yenile", "Ana sayfa"). 2) `window.addEventListener('vite:preloadError', …)` ile chunk hatasında tek seferli… | S |
| FE-04 | 🟡 | O | Davetiye bağlantısının paylaşım önizlemesi yok (Open Graph) | `frontend:index.html:1-12` (`description`, `og:*`, `twitter:*` etiketi yok) · `backend:de… | En ucuz: `index.html`'e site genelinde `og:title`, `og:description`, `og:image` (bütün davetiyeler aynı önizlemeyi alır). Sağlam: Nginx'te bilinen bot `User-Agent`'ları … | M |
| FE-10 | 🟡 | K | Ana giriş paketi 1,64 MB: 299 şablon her sayfaya, misafir sayfasına bile yükleniyor | `frontend:src/components/templates/TemplateRenderer.tsx:2-88` (dokuz kategori barrel'ının… | 1) `TemplateRenderer`'daki dokuz barrel içe aktarımını `lazyPresets.ts` desenine taşı: şablon kimliği → `lazy(() => import(...))` haritası; misafir yalnızca kendi şablon… | M |
| FE-50 | 🟡 | K | Sihirbaz her ziyarette sunucuda boş taslak açıyor; yenilemede editör kayboluyor | `frontend:src/hooks/useInvitationAutoSave.ts` (her `editRevision` değişikliğinde 1,5 sn s… | 1) İlk `POST`'u kategori/tema seçimine değil ilk metin alanına (ad, tarih, konum) ya da "Davetiyeni Oluştur"a bağla. 2) Kayıt açılınca adresi `/create/<id>` yap (`naviga… | M |
| FE-51 | 🟡 | K | Misafir fotoğraf/video yüklemesine arayüzden ulaşılamıyor | `frontend:src/pages/InvitePage.tsx:123-127` (`onRsvpClick={() => setRsvpModalOpen(true)}`… | Karar ver. Özellik isteniyorsa: yüklemeyi satır içi forma (`templates/shared/RSVPForm.tsx`) taşı, `RsvpModal`'ı kaldır. İstenmiyorsa: `RsvpModal`, `useRsvpStore` medya k… | M |
| FE-52 | 🟡 | O | Fiyat sayfası SSS'si backend'de olmayan "yayın süresi" ve ücretli uzatmayı anlatıyor | `frontend:src/pages/PricingPage.tsx:41` ("davetiyeniz paketinizin yayın süresi boyunca ya… | Önce karar: yayın süresi olacak mı? Olmayacaksa iki cevabı gerçeğe göre yaz ("Davetiyeniz yayında kalır; misafir yanıtları etkinlikten 6 ay sonra silinir"). Olacaksa sür… | S |
| FE-53 | 🟡 | K | Kısıtlı mobil koşulda LCP 3,9–5,7 sn; giriş ve fiyat sayfalarında CLS 0,33–0,63 | ana sayfa, misafir sayfası, giriş, fiyatlar (üretim build'i) · kök nedenler: `FE-10` (ana… | 1) `FE-10` (paketi küçült). 2) Fontları kendi alan adından sun, `<link rel="preload">` ile ön yükle, `size-adjust` ile yedek fontu eşle (`SEC-12` ile aynı iş). 3) Fiyat … | M |
| FE-54 | 🟡 | K | Hata ve başarı mesajları ekran okuyucuya duyurulmuyor; alt bilgi ve fiyat kartında kontrast yetersiz | `frontend:src/components/ui/Toast.tsx:51` (kapta `role`/`aria-live` yok) · `frontend:src/… | Toast kabına `role="status" aria-live="polite"`, hata türündekilere `role="alert"`. Alt bilgide `text-emerald-100/50` → `/70`; alt şeritte bir ton açık renk; fiyat kartı… | S |
| OPS-03 | 🟡 | O | İzleme ve alarm kurulmamış; sağlık ucu yalnızca PHP'nin ayakta olduğunu söylüyor | `backend:app/Http/Controllers/Api/V1/HealthController.php:19-22` (`return response()->jso… | 1) `GET /api/ping` aynen kalsın (ucuz, dağıtım için). 2) `GET /api/health`: `DB::select('select 1')`, `jobs` tablosundaki en eski işin yaşı, son `schedule:run` zamanı (c… | S |
| OPS-04 | 🟡 | O | Üretim `.env` şablonu sunucudaki gerçek dosyadan sapmış | `backend:docs/10-URETIM-ENV-SABLONU.md:59` (`APP_URL=https://api.davetkart.com`) · `:123`… | Şablonu güncelle: `APP_URL=https://davetkart.com`, `AWS_URL=https://media.davetkart.com`, `AWS_BUCKET` örnek değeri; `MAIL_MAILER` için üretimde `log` kalırsa açılışta u… | S |
| OPS-05 | 🟡 | O | Tek hata noktaları: alan adı otomatik yenilemesi kapalı, posta ve kredi bitiş tarihleri | `YAYIN-PLANI.md` §8 "Süre takvimi": alan adı `davetkart.com` 11 Eylül 2027 ("Otomatik yen… | Alan adında otomatik yenilemeyi aç ve kartı doğrula; posta için karar ver (yenile ya da taşı) ve 11 Aralık'a hatırlatıcı; kredi bitişinden bir ay önceye hatırlatıcı. Dış… | S |

### 5.2 Düşük (🟢) ve öneri (💡) — 27 bulgu

| ID | Seviye | Kanıt | Başlık | Nerede | Öneri | Efor |
|---|---|---|---|---|---|---|
| ARC-06 | 🟢 | K | Üç hata kodu hiçbir yerde fırlatılmıyor | `backend:app/Enums/ErrorCode.php:22` (`TOKEN_EXPIRED`) · `:29` (`INVITATION_LOCKED`) · `:… | `SLUG_TAKEN` ve `INVITATION_LOCKED`'ı sil (K66: slug üretilmiyor). `TOKEN_EXPIRED` için karar ver: ya Sanctum'un süre kontrolünü bu koda bağla ya da sil. | S |
| ARC-07 | 🟢 | K | Frontend'de `.gitattributes` yok; sözleşme dosyası CRLF | `frontend:` (kökte `.gitattributes` yok) · `frontend:src/contracts/error-codes.json` (170… | Frontend köküne `* text=auto eol=lf` + ikili dosya kalıpları; ardından tek seferlik `git add --renormalize .` commit'i. | S |
| ARC-08 | 🟢 | K | Dal hijyeni: 30+ dal, yazım hatalı adlar, etiket yok | backend ve frontend depoları (`git branch -a`, `git tag`) | Yayın commit'lerini etiketle (`v1.0.0`), birleşmiş dalları sil, tek bir entegrasyon dalı belirle ve yerel depoları ona göre güncel tut. | M |
| ARC-09 | 🟢 | O | Checkout idempotent değil: her çağrı yeni `pending` sipariş açar | `backend:app/Actions/Payment/StartCheckoutAction.php:111-142,195-243` | Transaction içinde, kullanıcı satırı kilitliyken aynı (kullanıcı, davetiye, plan) için süresi dolmamış `pending` sipariş varsa onu döndür; yoksa aç. | M |
| SEC-14 | 🟢 | K | `main`'deki bağımlılık temizliği denetlenen dalda yok | `frontend:package.json` (denetlenen dal: `express`, `dotenv`, `@types/express` duruyor; `… | `main`'i şablon dalına birleştir (ya da tersini), `npm ci && npm run check` ile doğrula. | S |
| SEC-15 | 🟢 | K | Kayıt ucu e-postanın kayıtlı olduğunu söylüyor | `backend:app/Actions/Auth/RegisterUserAction.php:42-45` | `SEC-09` ile birlikte çöz. | M |
| SEC-16 | 🟢 | O | Hesap bazlı (IP'den bağımsız) kaba kuvvet freni yok | `backend:app/Providers/AppServiceProvider.php:380-389` (kovalar: e-posta + IP başına 5/dk… | Üçüncü kova: e-posta başına saatte 30 deneme (IP'den bağımsız); aşılınca kilit yerine yanıtı geciktir ve hesap sahibine "şüpheli giriş denemesi" postası. | S |
| SEC-17 | 🟢 | K | Doküman deposunda git dışı 15 kod arşivi var, 3'ünde `.env` | `davetkart-docs/archive/local-snapshots/` (148 MB, 15 arşiv; `.gitignore:5` ile git dışı) | Arşivleri sil ya da şifreli bir kasaya taşı; içlerindeki anahtarlar hâlâ geçerliyse döndür (bu senin işin). | S |
| TST-03 | 🟢 | K | Satır kapsamı ölçülmüyor; eşik yok | `backend:.github/workflows/ci.yml` (`coverage: none`) · yerel PHP (Herd): `php -m` çıktıs… | CI'da `coverage: pcov` + `php artisan test --coverage --min=85` (önce ölç, eşiği ölçülen değerin birkaç puan altına koy). Mutasyon için bu denetimin koşucusu (`evidence/… | S |
| TST-05 | 🟢 | K | Frontend CI Node 22, yerel ortam Node 24; sürüm sabitlenmemiş | `frontend:.github/workflows/ci.yml` (`node-version: "22"`) · denetim ortamı Node 24.18.0 … | `.nvmrc` (ya da `package.json` `engines.node`) + CI'da `node-version-file: .nvmrc`. Üretimde Node yalnızca build için gerekli; sunucudaki sürüm de aynı dosyadan okunmalı. | S |
| FE-03 | 🟢 | K | `tsconfig` `strict` kapalı; açmak yalnızca 19 hata | `frontend:tsconfig.json` (`strict`, `strictNullChecks`, `noImplicitAny` yok) · `frontend:… | `"strict": true` ekle; `particleEngine.ts`'teki 15 `possibly null` hatasını erken dönüşle kapat. Ardından `noUncheckedIndexedAccess` ayrı bir adım olarak değerlendirileb… | S |
| FE-05 | 🟢 | O | Plan kuralları frontend'de elle kopyalanmış | `frontend:src/data.ts:4018-4066` (fiyat kartı özellik matrisi, "LCV — maksimum 100 kişi")… | `GET /public/plans` yanıtına plan başına `rsvpLimit`, `modules` ve `whiteLabel` ekle; ya da `contracts/plan-rules.json` + `verify:plans` betiği (hata sözleşmesiyle aynı … | M |
| FE-06 | 🟢 | K | 404 sayfası yok; bilinmeyen adres ana sayfaya atıyor | `frontend:src/App.tsx:126` (`{ path: '*', element: <Navigate to="/" replace /> }`) · `fro… | `NotFoundPage` (başlık, ana sayfa ve panel bağlantısı); `*` rotası onu çizsin. Misafir yolu `/invite/:id` için ayrı metin ("Bu davetiye yayında değil"). | S |
| FE-07 | 🟢 | K | `README.md` boş; `CLAUDE.md` kodla çelişiyor | `frontend:README.md` (0 satır) · `frontend:CLAUDE.md:9` ("AI Integration: Google GenAI (`… | `README.md`: kurulum, `npm run check`, ortam değişkenleri, backend'le ilişki. `CLAUDE.md`: GenAI satırını "asistan backend üzerinden" diye düzelt, `verify` betiklerini v… | S |
| FE-08 | 🟢 | O | Konum araması: backend ucu olmayan, bayrakla kapalı kod | `frontend:src/services/places.ts:22-24` · `frontend:src/hooks/usePlaceSearch.ts` · `front… | Karar ver: backend ucunu yaz (Places anahtarı sunucuda, önbellek, `throttle`) ya da üç dosyayı kaldırıp "haritadan seç" akışını tek yol yap. | S |
| FE-09 | 🟢 | O | 95 MB video depoda ve önbellek başlığı olmadan sunuluyor | `frontend:public/videos/` (126 dosya, 90 MB) · `backend:deploy/nginx/davetkart.conf` (`Ca… | Kısa vade: Nginx'e `location ^~ /videos/ { add_header Cache-Control "public, max-age=604800"; }`. Sağlam: videoları `src/` altından içe aktar (Vite hash'ler) ya da nesne… | M |
| FE-55 | 🟢 | K | "Planlarım" fiyat sayfasından plan alınabileceğini söylüyor; orada satın alma düğmesi yok | `frontend:src/pages/account/AccountPlansSection.tsx:45` · `frontend:src/pages/PricingPage… | Girişli kullanıcı için fiyat kartlarına "Bu planı satın al" (`checkoutHref({ tier })`); ya da metni "davetiyenizi yayınlarken" ile sınırla. | S |
| FE-56 | 🟢 | K | `dugun-gul-3d` "hareketi azalt" tercihinde hareket etmeye devam ediyor | `frontend:src/components/templates/dugun/DugunGul3d/` | Sahnede `useReducedMotion()` true ise döngüyü durdur, tek kare çiz (diğer 3B şablonlar, ör. `dugun-kelebek`, bunu yapıyor). | S |
| FE-58 | 🟢 | K | Ödeme dönüşünde davetiye kullanıcı onayı olmadan yayınlanıyor; K67 ile çelişki sorusu açık | `frontend:src/hooks/useAutoPublish.ts` (sipariş `paid` ve davetiyeye bağlıysa `publishInv… | Kararı kapat. Otomatik yayın isteniyorsa K67'yi "ödeme **sunucuda** yayınlamaz; frontend, yayın niyetiyle başlayan ödemenin dönüşünde yayınlar" diye daralt ve yeni K num… | S |
| OPS-06 | 🟢 | O | Dağıtım yerinde yapılıyor, bakım kipi yok | `backend:deploy/deploy.sh` (sıra: `git pull` → `composer install` → `config:cache`, `rout… | Ucuz: göç içeren dağıtımlarda `artisan down --retry=15` … `artisan up`. Sağlam: backend için de `releases/<commit>` + `current` bağı; göçler geriye uyumlu yazılır (önce … | M |
| OPS-07 | 🟢 | O | PHP-FPM havuzu ve OPcache ayarı depoda yok; bellek bütçesi yazılı değil | `backend:deploy/php/davetkart.ini` (yalnızca yükleme sınırları, `memory_limit=256M`, hata… | `deploy/php-fpm/davetkart.conf`: `pm = dynamic`, `pm.max_children = 4`, `pm.max_requests = 500`; `deploy/php/davetkart.ini`'ye `opcache.memory_consumption`, `opcache.val… | S |
| OPS-08 | 🟢 | O | Günlüklerde istek kimliği yok | `backend:config/logging.php` (satır biçimi, JSON biçimlendirici yok) · `backend:bootstrap… | Ara katman: gelen `X-Request-Id` yoksa ULID üret, `Log::shareContext(['request_id' => …])`, yanıta başlık olarak ekle; hata zarfına `requestId` alanı (sözleşmeye bir sat… | S |
| ARC-10 | 💡 | O | `OptimizeUploadedImage` 664 satır, tek sınıfta dört sorumluluk | `backend:app/Jobs/OptimizeUploadedImage.php` (664 satır; 301 kod, 264 yorum) | `ImageDecoder`, `ExifOrientation`, `ImageEncoder`, `MediaFileSwap` gibi küçük sınıflara ayır; job yalnızca sırayı yönetsin. | M |
| SEC-18 | 💡 | O | Token'ı `localStorage` yerine `httpOnly` çerezde tut | `frontend:src/services/auth.ts:136-156` | Yayından sonra: Sanctum'un çerez tabanlı SPA kimlik doğrulamasına geç. Önce `SEC-04` (CSP) ile ikinci kilidi kur. | L |
| TST-06 | 💡 | K | Paket 143 sn ve neredeyse tamamı Feature testi; mutasyon başına 2,5 dk | `backend:tests/Feature/` (50 dosya, 707 metot) · `backend:tests/Unit/` (11 dosya, 46 meto… | `php artisan test --parallel` (PostgreSQL'de süreç başına veritabanı; `TestSuiteIsolationTest` veritabanı adı önekine göre güncellenmeli). Saf kurallar (`RefundEligibili… | M |
| FE-57 | 💡 | K | Küçük arayüz pürüzleri: düşen oturumda açıklama yok, yığılan hata bildirimleri, eski ipucu metni | `frontend:src/services/api.ts:178-191` (401 → `logout()`, bildirim yok) · `frontend:src/c… | A) Yönlendirirken `state: { reason: 'expired' }` ve girişte tek satır "Oturumunuz sona erdi". B) Aynı metinli bildirimi yenilemek yerine süresini uzat. C) Metni panele g… | S |
| OPS-09 | 💡 | O | Yatay ölçeğin önündeki tasarım kararları | `docs/10-URETIM-ENV-SABLONU.md` (`CACHE_STORE=file`, `QUEUE_CONNECTION=database`, `SESSIO… | Dokunma. `YAYIN-PLANI.md` §6'daki "ne zaman Lightsail'den çıkılır" eşiklerine ölçülebilir sayılar ekle (FPM kuyruğu, bellek, p95 yanıt süresi). İlk adım büyük olasılıkla… | L |

---

## 6. Dilimler arası tekrar ve kök nedenler

Aynı kök neden birden çok dilimde göründü. Kimlikler korunmuştur; aşağıdaki çiftler **tek iş** olarak ele
alınmalıdır.

| Kök neden | İlgili bulgular | Tek iş olarak |
|---|---|---|
| Kalite kapısı koşmadan birleşen Faz 15–17 | `ARC-02` · `TST-01` · `OPS-01` | Kapıyı koş, faz kaydını yaz, commit'i etiketle |
| Plan kuralları iki depoda elle | `FE-05` · `OPS-01` · R8 | Kuralları sözleşme dosyasına ya da API'ye al |
| Nginx yapılandırması | `SEC-04` · `FE-09` | Güvenlik başlıkları ve önbellek başlıkları aynı dosyada, tek değişiklik |
| Google Fonts'un dışarıdan yüklenmesi | `SEC-12` (gizlilik) · `FE-53` (performans) | Fontları kendi alan adından sun |
| Misafir medyası | `SEC-08` (kota) · `FE-51` (arayüz yok) | Önce karar: özellik var mı? |
| Kayıt açan uçlarda tavan ve tekrar kullanım yok | `ARC-09` (sipariş) · `FE-50` (taslak) | Aynı desen: açık kaydı yeniden kullan, tavan koy |
| Eşzamanlılık | `SEC-01` (indirim) · `TST-02` (kilit testi) · R14 (yarış koşmadı) | Kilit + iki bağlantılı yarış testi |
| Kayıt ve belge güncelliği | `ARC-01` · `ARC-05` · `FE-07` · `OPS-04` · `FE-52` · `FE-58` | "Kod değişti, kaydı da değişti mi" adımını faz kapanışına ekle |
| Bağımlılıklar | `SEC-07` · `SEC-14` · `OPS-01` | `composer update` + frontend `main`'deki temizlik commit'ini dala al |
| E-posta sahipliği | `SEC-09` · `SEC-15` · `SEC-01` | Doğrulamalı kayıt üçünü birden hafifletir |

Çelişki bulunmadı; bir düzeltme yapıldı: `FE-02`'nin "yayın sonrası bulunamayan chunk" senaryosu, dağıtım
betiğinin eski parçaları 14 gün tuttuğu görülünce daraltıldı (`05-operations.md`, "Neler iyi" 2).

---

## 7. Regresyon: önceki bulguların durumu

✅ kapandı · 🟡 kısmen · ❌ açık · ❓ doğrulanamadı. Ayrıntılı kanıt her bulgu dosyasının "Regresyon" bölümünde.

| # | Kaynak | Bulgu | Durum | Kanıt | Açık kalan |
|---|---|---|---|---|---|
| R1 | Review §1.1 / K-1 | Yayından sonra üst plan modülü açılıyor | ✅ | Sonda P15–P16 · mutasyon M01, M02 · tarayıcı yolculuk 4 | — |
| R2 | Review §1.2 / K-4 | Geç gelen `paid` bildirimi yutuluyor | ✅ | Sonda P23 · mutasyon M04 | — |
| R3 | Review §2.1 | Ödeme dönüş sayfası, `GET /orders/{id}`, `publishedAt` | ✅ | Tarayıcı yolculuk 3 | Dönüşte otomatik yayın K67 ile çelişki sorusu (`FE-58`) |
| R4 | Review §2.2 | Token ömrü, `sanctum:prune-expired` | ✅ | Sonda P70 · mutasyon M19 | — |
| R5 | Review §2.3 | `TrustProxies`, gerçek istemci IP'si | ✅ | Sonda P24 · Nginx dosyası | Canlıda doğrulama (Y12.3) koşmadı |
| R6 | Review §2.4 | Parola sıfırlama, e-posta doğrulama, hesap silme, saklama süresi | 🟡 | Sonda Q09–Q13, P80–P82 · mutasyon M33, M34, M42 | E-posta doğrulama yok (`SEC-09`); saklama boşlukları (`SEC-11`, `SEC-13`) |
| R7 | Review §5.1 | 4xx istisnaları Sentry'ye gidiyor | ✅ | `bootstrap/app.php:56-58` · mutasyon M43 | Sentry'ye istek atılmadı |
| R8 | Review §5.2 | Fiyat sayfası vaatleri ↔ sunucu kuralları | 🟡 | Özellik matrisi dokuz satır tutarlı · sonda P15, P16 | SSS'deki "yayın süresi" (`FE-52`); kopya kural (`FE-05`) |
| R9 | Review §5.4–5.5 | Hız sınırları, video boyutu, mükerrer LCV | 🟡 | Sonda P26 · tarayıcı yolculuk 1 | Genel tavan IP'ye bağlı (`SEC-06`); misafir kotası (`SEC-08`) |
| R10 | Review §6.1–6.10 | Ölü kod, `preventStrayRequests`, Sentry testte, git hijyeni, CRLF | 🟡 | `TestCase.php:30` · `phpunit.xml` · `TestSuiteIsolationTest` | `ARC-06`, `ARC-07`, `ARC-08` |
| R11 | Test denetimi K-2…K-8 | NUL, `İ`, `Retry-After`, yarım JSON, `integer:strict`, `mapUrl` | ✅ | Sonda P31–P35, P66 · mutasyon M20–M25, M27 | — |
| R12 | Test denetimi §2 | Hayatta kalan mutantlar | ✅ | Mutasyon M06, M15, M18, M19, M26, M29, M50, M51 | Üç dosya yeniden denenmedi (`03-testing.md`, R12 satırı) |
| R13 | Faz 7 | Paket kaç yayın açar | ✅ | `ClaimReleasedOrderAction.php:45` · tarayıcı yolculuk 6 | Paket alımının arayüz yolu yok (`FE-55`) |
| R14 | Faz 11–12 | Hediye kodu, Shopier imzası, open redirect, tutar | 🟡 | Sonda P38–P43 · mutasyon M07–M13 | Yarış koşmadı, kilit testsiz (`TST-02`); `callback` kipi (`SEC-03`) |
| R15 | Faz 14 | Plan hakkı, hak iptali, e-posta değişikliği | 🟡 | Tarayıcı yolculuk 6 · sonda Q01–Q08 · mutasyon M30–M32 | Kullanılmış hakkın iadesi (`SEC-02`) |
| R16 | Fiyat kararı | Fiyat yalnızca backend'den, indirim, ödeme yöntemi anahtarı | 🟡 | `verify:pricing` · sonda P12 · mutasyon M36, M37 | İlk yayın indirimi birden çok siparişe (`SEC-01`) |
| R17 | `DECISION-INDEX.md` | "Geçerli" kararlar kodda mı | 🟡 | 60'tan fazla karar örneklendi, hepsi kodda | İndeks K128–K145'i içermiyor (`ARC-01`) |

Özet: 17 satırın 9'u kapandı, 8'i kısmen; açık ya da doğrulanamayan satır yok. Kısmen kalan sekiz satırın her
biri bu raporda numaralı bir bulguya bağlı.

---

## 8. Yayın öncesi kapı

Yayına çıkmadan önce her satırın ✅ olması önerilir. Bugünkü durum bu denetimin gördüğüdür.

| Koşul | Bulgu | Bugün |
|---|---|---|
| Yayınlanacak iki commit belli, etiketli; backend frontend'den önce | `OPS-01` | ❌ |
| `composer check` yeşil | `TST-01` | ❌ (Pint) |
| `composer audit` temiz | `SEC-07` | ❌ (8 açık) |
| Veritabanı yedeği ve bir geri yükleme provası | `OPS-02` | ❌ |
| Hata izleme (Sentry) ve dış izleme | `OPS-03` | ❌ |
| Shopier `callback` kipi üretimde reddediliyor | `SEC-03` | ❌ |
| Frontend güvenlik başlıkları | `SEC-04` | ❌ |
| İlk yayın indirimi tek siparişe | `SEC-01` | ❌ |
| Kullanılmış hak iade edilemiyor | `SEC-02` | ❌ |
| Fiyat sayfası metni gerçek kuralla aynı | `FE-52` | ❌ |
| Üretim `.env` şablonu güncel; posta sürücüsü `log` değil | `OPS-04` | ❓ (sunucu görülmedi) |
| Alan adı otomatik yenileme açık | `OPS-05` | ❓ (panel görülmedi) |
| Gizlilik metni yedek süresini ve işleyenleri söylüyor | `SEC-11` | ❌ |

---

## 9. Sözleşme tablosu (frontend çağrısı ↔ backend rotası)

Kaynak: [`findings/04-frontend-e2e.md`](findings/04-frontend-e2e.md), `evidence/commands/FE-d1-metrics.txt` §1.

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

Ek eşleşmeler: 16 Resource'un 170 alanının hepsi frontend'de okunuyor; sekiz enum'un değerleri iki tarafta aynı;
28 hata kodu iki depoda anlamsal olarak aynı; premium şablon listesi 32 = 32.

---

## 10. Bağımlılık tablosu

Kaynak: Packagist ve npm kaydı, 13 Kasım 2026 (`composer show --direct --latest`, `npm outdated`,
`composer audit`, `npm audit`; kanıt dosyaları `evidence/commands/B2-*.txt`). Context7 bağlı değildi; büyük sürüm
geçişlerinin içeriği resmî belgelerden okunmadı, "aksiyon" sütunu bu yüzden temkinlidir.

### 10.1 Backend (`composer.json`)

| Paket | Tür | Kurulu | Güncel kararlı | Güvenlik notu | Aksiyon |
|---|---|---|---|---|---|
| `laravel/framework` | üretim | 13.35.0 | 13.42.0 | Bağımlı Symfony paketlerinde 8 bilinen açık (`SEC-07`) | `composer update` (semver güvenli); yayından önce |
| `laravel/sanctum` | üretim | 4.3.3 | 4.4.0 | — | semver güvenli güncelle |
| `laravel/tinker` | üretim | 3.0.2 | 3.1.0 | — | semver güvenli güncelle |
| `league/flysystem-aws-s3-v3` | üretim | 3.35.3 | 3.35.3 | — | güncel |
| `sentry/sentry-laravel` | üretim | 4.27.0 | 4.30.0 | — | semver güvenli güncelle |
| `fakerphp/faker` | geliştirme | 1.24.1 | 1.24.1 | — | güncel |
| `larastan/larastan` | geliştirme | 3.10.0 | 3.15.0 | — | güncelle; yeni kurallar yeni hata çıkarabilir |
| `laravel/pail` | geliştirme | 1.2.7 | 1.3.0 | — | güncelle |
| `laravel/pao` | geliştirme | 1.1.2 | 1.1.5 | — | güncelle |
| `laravel/pint` | geliştirme | 1.29.3 | 1.32.3 | — | güncelle; biçim kuralları değişebilir, ardından `pint` koş |
| `mockery/mockery` | geliştirme | 1.6.12 | 1.6.15 | — | güncelle |
| `nunomaduro/collision` | geliştirme | 8.9.5 | 8.9.6 | — | güncelle |
| `phpunit/phpunit` | geliştirme | 12.5.33 | 13.4.6 | — | büyük sürüm: ertele, ayrı iş |

Dolaylı paketlerdeki açıklar (`composer audit`, 8 kayıt): `symfony/http-foundation`, `symfony/http-kernel`,
`symfony/mime`, `symfony/routing`, `symfony/filesystem` (8.1.0–8.1.9 aralığı). Ayrıntı `SEC-07`.

### 10.2 Frontend (`package.json`)

`npm audit` (üretim ve bütün ağaç): 0 açık.

| Paket | Tür | Kurulu | Güncel kararlı | Aksiyon |
|---|---|---|---|---|
| `react` · `react-dom` | üretim | 19.2.7 | 19.3.1 | semver güvenli güncelle |
| `react-router-dom` | üretim | 7.18.5 | 7.18.5 | güncel |
| `zustand` | üretim | 5.0.14 | 5.1.0 | güncelle |
| `axios` | üretim | 1.21.0 | 1.21.1 | güncelle |
| `i18next` | üretim | 26.3.4 | 27.1.1 | büyük sürüm: ertele (`FE-01` kararıyla birlikte) |
| `react-i18next` | üretim | 17.0.8 | 18.0.1 | büyük sürüm: ertele |
| `i18next-browser-languagedetector` | üretim | 8.2.1 | 8.3.0 | güncelle |
| `motion` | üretim | 12.40.0 | 14.13.0 | büyük sürüm: ertele; 373 şablon etkilenir |
| `three` · `@types/three` | üretim · geliştirme | 0.180.0 | 0.187.0 | `FE-10` ile birlikte değerlendir |
| `@react-three/fiber` | üretim | 9.8.2 | 9.8.2 | güncel |
| `lucide-react` | üretim | 0.546.0 | 1.72.0 | büyük sürüm: ertele |
| `lenis` | üretim | 1.3.25 | 1.3.27 | güncelle |
| `clsx` · `use-debounce` | üretim | 2.1.1 · 10.1.1 | aynı | güncel |
| `tailwind-merge` | üretim | 3.6.0 | 3.7.0 | güncelle |
| `vite` | üretim (yanlış yerde) | 6.4.5 | 8.3.8 | `devDependencies`'e taşı (`main`'deki `47aedc8` yapıyor); büyük sürüm ertelensin |
| `@vitejs/plugin-react` | üretim (yanlış yerde) | 5.2.0 | 6.3.0 | aynı |
| `@tailwindcss/vite` · `tailwindcss` | üretim · geliştirme | 4.3.1 | 4.3.5 | güncelle; ilki `devDependencies`'e |
| `express` · `@types/express` | üretim · geliştirme | 4.22.3 · 4.17.25 | 5.3.0 · 5.0.6 | **kaldır**: kodda kullanılmıyor (`47aedc8` kaldırıyor, `SEC-14`) |
| `dotenv` | üretim | 17.4.2 | 18.0.10 | **kaldır**: kodda kullanılmıyor |
| `typescript` | geliştirme | 5.8.3 | 7.0.2 | büyük sürüm: ertele; önce `strict` (`FE-03`) |
| `@types/node` | geliştirme | 22.20.0 | 26.6.6 | Node 24 ile hizala (24.x); `TST-05` |
| `@types/react` · `@types/react-dom` | geliştirme | 19.3.0 | 19.3.0 | güncel |
| `esbuild` | geliştirme | 0.25.12 | 0.28.2 | Vite ile birlikte |
| `tsx` | geliştirme | 4.22.4 | 4.23.15 | güncelle |
| `autoprefixer` | geliştirme | 10.5.0 | 10.6.2 | güncelle |

---

## 11. Yol haritası

Efor: S ≤ 1 saat · M yarım gün · L 1–2 gün. Sıra, etki ve bağımlılığa göredir; tahminler kaba.

### Aşama 0 — yayından önce (kapı)

| Sıra | İş | Bulgular | Efor |
|---|---|---|---|
| 1 | `composer update` (semver güvenli) → `vendor/bin/pint` → `composer check` yeşil; frontend `main`'deki bağımlılık temizliğini dala al | `SEC-07`, `TST-01`, `SEC-14` | S |
| 2 | Faz 16–17 kaydını yaz; iki depoyu sırayla `main`'e al (önce backend), etiketle | `ARC-02`, `OPS-01` | S |
| 3 | Shopier `callback` kipini üretimde reddet | `SEC-03` | S |
| 4 | Nginx: güvenlik başlıkları + video önbellek başlığı | `SEC-04`, `FE-09` | S |
| 5 | İlk yayın indirimini tek siparişe bağla; kullanılmış hakkı iade dışı bırak | `SEC-01`, `SEC-02` | M + M |
| 6 | `pg_dump` betiği + cron + bir geri yükleme provası | `OPS-02` | M |
| 7 | Sentry DSN, dış izleme, hazır olma ucu | `OPS-03` | S |
| 8 | Fiyat sayfası SSS'sini ve gizlilik metnini gerçeğe göre yaz | `FE-52`, `SEC-11` | S |
| 9 | Üretim `.env` şablonunu güncelle; alan adı otomatik yenileme | `OPS-04`, `OPS-05` | S |

Kaba toplam: iki-üç iş günü.

### Aşama 1 — yayından sonraki ilk iki hafta

| İş | Bulgular | Efor |
|---|---|---|
| Kilit testleri (SQL düzeyinde + iki bağlantılı yarış) | `TST-02` | M |
| Sihirbaz: taslağı ilk içerikte aç, adrese kimlik koy, taslak tavanı | `FE-50` | M |
| Şablonları kimliğe göre tembel yükle; paket bütçesi | `FE-10` | M |
| Fontları kendi alan adından sun; fiyat ve giriş kartlarına yer tut | `SEC-12`, `FE-53` | M |
| Bildirimlere canlı bölge; kontrast düzeltmeleri | `FE-54` | S |
| Hata sınırı, 404 sayfası | `FE-02`, `FE-06` | S |
| Paylaşım önizlemesi (Open Graph) | `FE-04` | M |
| Parola politikası; hız sınırını kimliğe bağla; hesap bazlı fren | `SEC-05`, `SEC-06`, `SEC-16` | S + M + S |
| Misafir medyası kararı: bağla ya da kapat; kotaları düşür | `FE-51`, `SEC-08` | M |
| `data:purge`: tarihsiz davetiyeler | `SEC-13` | S |
| Karar indeksini güncelle (K128–K145, K55, K67) | `ARC-01`, `ARC-04`, `FE-58` | S |

### Aşama 2 — ilk çeyrek

| İş | Bulgular | Efor |
|---|---|---|
| E-posta doğrulamalı kayıt | `SEC-09`, `SEC-15` | L |
| Üç yolculukluk Playwright duman testi; CI'da kapsam ölçümü | `TST-04`, `TST-03` | L + S |
| Plan kurallarını sözleşmeye ya da API'ye al | `FE-05` | M |
| Dil kararı: tr/en ile sınırla ya da çevir | `FE-01` | S ya da L |
| `strict` TypeScript; README ve CLAUDE.md | `FE-03`, `FE-07` | S + S |
| K18 kararı; eski `claude/` yolları | `ARC-03`, `ARC-05` | L + M |
| Checkout'ta açık siparişi yeniden kullan | `ARC-09` | M |
| Bakım kipli ya da sürüm klasörlü dağıtım; FPM havuzu; istek kimliği | `OPS-06`, `OPS-07`, `OPS-08` | M + S + S |
| Dal ve etiket hijyeni; `.gitattributes`; ölü hata kodları | `ARC-08`, `ARC-07`, `ARC-06` | M + S + S |
| Shopier'e gönderilen yer tutucu veriler için yazılı teyit | `SEC-10` | S |

### Sonra / ihtiyaç doğunca

`SEC-18` (token'ı `httpOnly` çereze taşımak) · `OPS-09` (yatay ölçek) · `ARC-10` (`OptimizeUploadedImage`'ı bölmek) ·
`TST-06` (paralel test) · `FE-08` (konum araması) · `FE-55`, `FE-56`, `FE-57`, `FE-58` · `SEC-17` (yerel kod arşivleri).

---

## 12. Kararlar (İsmail'in vermesi gerekenler)

Bulguların bir kısmı kod değil karar bekliyor. Her satırda bu denetimin önerisi var; karar senin.

| # | Soru | Öneri | Bulgu |
|---|---|---|---|
| 1 | Faz 15–17 ilk yayında olacak mı; iki depo hangi sırayla `main`'e alınacak? | Olacaksa önce backend, sonra frontend; ikisi aynı etiketle | `OPS-01` |
| 2 | "İlk yayın" indirimi kullanıcı başına bir kez mi? | Evet; açık indirimli sipariş varken ikincisi liste fiyatından | `SEC-01` |
| 3 | Yayınlanıp silinen davetiyenin hakkı iade edilebilir mi? | Hayır; üç günlük pencere yeniden kullanıma izin versin, paraya değil | `SEC-02` |
| 4 | Shopier `callback` kipi kaldırılsın mı? | Üretimde reddet; canlı doğrulamayı OSB ile yap | `SEC-03` |
| 5 | Paketlerin bir yayın süresi olacak mı? | Olmayacaksa SSS'yi düzelt; olacaksa önce kuralı yaz | `FE-52` |
| 6 | Misafir fotoğraf/video yüklemesi ürün kapsamında mı? | Kapsamdaysa satır içi forma bağla; değilse ucu kapat | `FE-51`, `SEC-08` |
| 7 | Ödeme dönüşünde otomatik yayın kalsın mı (K67)? | Kalsın; K67'yi daraltan yeni kararı kaydet | `FE-58` |
| 8 | E-posta doğrulaması yayından önce mi? | En azından ilk yayın indirimi doğrulanmış hesaba | `SEC-09` |
| 9 | On dil bir hedef mi? | Değilse dil seçiciyi tr/en'e indir | `FE-01` |
| 10 | K18 (kısa yorum) gevşetilsin mi, uygulatılsın mı? | Gerçeğe göre gevşet ya da kapıda ölç; ikisinden biri | `ARC-03` |
| 11 | K55'in yerine geçen karar (üretimde medya S3'te) | Yeni K numarasıyla kaydet | `ARC-04` |
| 12 | Faz 16–17'de hangi şablonun Gold olduğu kararı | K numarasıyla kaydet (ölçüt: "premium etkileşimli") | `ARC-02` |
| 13 | Shopier'e yer tutucu TCKN/telefon gönderimi | Shopier'den yazılı teyit | `SEC-10` |
| 14 | Gold'dan Elit'e yükseltmede tam fiyat mı, fark mı? | Karar ver ve fiyat sayfasına yaz | `04-frontend-e2e.md`, soru 6 |
| 15 | Yeni davetiyede zarf ve program akışı (Gold) açık gelsin mi? | Karar ver; Standart kullanıcının ilk yayın deneyimini belirliyor | `04-frontend-e2e.md`, soru 7 |
| 16 | Konum araması yazılacak mı? | Yazılmayacaksa üç dosyayı kaldır | `FE-08` |
| 17 | CI'da kapsam ölçümü ve mutasyon koşucusu depoya alınsın mı? | Evet (süre 1,5–2 kat) | `TST-03` |

Sunucudan öğrenilmesi gerekenler (değer değil, durum): posta sürücüsü (`log` mu `ses` mi), `pm.max_children`,
yedek bucket'ının varlığı, alan adı otomatik yenilemesi, GitHub Actions'ın bu dal için sonucu.

---

## 13. Dersler

Bu bölüm denetimin öğretici çıktısıdır: bulguların arkasındaki genel ilkeler.

1. **Kapı koşmadan birleşen iş bitmemiştir.** Faz 15–17, kalite kapısını koşturamayan bir ortamda yazıldı ve
   "sonra koşarız" diye birleştirildi. Kapı ilk kez bu denetimde koştu ve kırmızı çıktı. Kuralın değeri,
   uygulanamadığı gün ne yapıldığıyla ölçülür: o gün için açık bir "bitmedi" işareti gerekir.
2. **Yeşil test paketi sıralı doğruluğu kanıtlar, eşzamanlı doğruluğu değil.** 1056 testin hiçbiri iki isteği
   aynı anda koşturmuyor; bu yüzden para ve kotayı koruyan 17 kilidin silinmesini hiçbir şey fark etmiyor.
   Mutasyon testi "testler neyi korumuyor" sorusunun en dürüst cevabıdır.
3. **İki depolu bir üründe sözleşme ya makinece doğrulanır ya da dağıtım sırasına emanet edilir.** Hata kodları
   birincisine örnek (ortak dosya + betik), plan kuralları ikincisine. İkincisi bir gün yanlış sırayla
   yayınlanır.
4. **Belge de koddur ve o da eskir.** Karar indeksi, ortam şablonu, asistan kuralları dosyası, fiyat sayfası
   SSS'si: dördü de bir zamanlar doğruydu. Kodun testi var, metnin yok; metni koda bağlayan küçük denetimler
   (projedeki `verify:render`'ın gizlilik metni denetimi iyi bir örnek) bu boşluğu kapatır.
5. **Parçalar tek tek doğruyken ürün yine de eksik olabilir.** Misafir yükleme ucu çalışıyor, yükleme penceresi
   çalışıyor, ikisini bağlayan çağrı yok. Bunu birim testi ya da kod okuması değil, kullanıcı gibi dolaşmak
   gösterdi.
6. **Kayıt açan her uç iki soru sorar: tekrar çağrılırsa ne olur, sınırsız çağrılırsa ne olur.** Sipariş ve
   taslak uçlarında ikisinin de cevabı "yeni kayıt". İdempotans yalnızca ödeme bildirimleri için değildir.
7. **Güvenlik çoğu zaman bir `if` değil, veri akışının şeklidir.** Fiyatın istekten okunamaması bir denetim
   satırı değil; istek nesnesinde fiyat alanı olmadığı için mümkün değil. En sağlam kurallar ihlal edilemeyecek
   biçimde kurulanlardır.
8. **Ölçümün kendisi de denetlenmeli.** Bu denetimde bir betik, Vite'ın `1,637.83 kB` yazımındaki binlik
   ayırıcıya takılıp en büyük iki dosyayı atladı ve "en büyük parça 887 kB" sonucunu üretti; gerçek 1,64 MB'tı.
   Hata, sonucu bağımsız bir yoldan (dosya boyutuna bakarak) sınayınca bulundu. Bir sayı şaşırtıcı derecede iyi
   görünüyorsa önce ölçümden şüphelen.
9. **Denetimin süreci hakkında:** dilim ajanları kullanım sınırına takıldı ve oturum iki kez kesildi. İşi
   kurtaran, bulgu dosyalarının en baştan taslak olarak açılması ve kanıtın dosyalara yazılmasıydı: her kesintiden
   sonra kaldığı yer dosyalardan okundu.

---

## 14. Ekler

### Ek A — Şartnameden ve plandan sapmalar

| Sapma | Neden |
|---|---|
| Çalışma ağacı yerine uzak dalların anlık görüntüsü denetlendi | Yerel ağaçlar geride; `git switch`/`pull` yasak (İsmail'in kararı, 13 Kasım) |
| Kopyalarda `phpunit.xml` veritabanı adı değişti | `RefreshDatabase` gerçek test veritabanını silmesin diye |
| Dilimleri ajanlar değil ana oturum yürüttü | Altı dilim ajanı kullanım sınırına takıldı; taslak dosyaları boş kaldı |
| Denetim 12–15 Kasım'a yayıldı | Oturum iki kez kullanım sınırında kesildi; kaldığı yer bulgu dosyalarından sürdürüldü |
| Tarayıcı yolculukları Playwright MCP yerine bağımsız Playwright betikleriyle koştu | MCP her çağrıda betiği geri yazıyordu; yalnızca kayıt adımı MCP ile koştu |
| Performans ölçümü `localhost:3000` yerine `localhost:4173`'te (üretim build'i) | Geliştirme sunucusu paketlenmemiş modül sunar; ölçüm anlamsız olurdu |
| Lighthouse yerine `PerformanceObserver` + CDP | Lighthouse kurulu değil; aynı ölçütler alındı |
| axe-core npm kaydından indirildi | Frontend `node_modules`'unda yok; sayfaya yerel dosyadan enjekte edildi |
| Context7 kullanılamadı | Bağlı değil; sürümler kayıtlardan, API doğruluğu kaldırılmış API taramasıyla |
| Dört parça dosyası (`02-security-b1/b2.md`, `04-frontend-d1/d2.md`) silindi | Plan gereği; dördü de boş iskeletti, hiç commit'lenmemişti |
| Mutasyon ve geçici testler gerçek depoda değil `backend-tst` kopyasında | Anlık görüntü kararı |
| Şartname dosyası depoda yok | Sohbette verildi; gereken bölümleri `PLAN.md`'ye aynen alındı |

### Ek B — Koşmayanlar ve doğrulanamayanlar (B7)

| Ne | Durum |
|---|---|
| Shopier ile gerçek ödeme, OSB ve callback'in canlı davranışı | Koşmadı; kod okundu, sahte imzalı yerel istekler atıldı |
| S3, CloudFront, SES, Gemini, Sentry | Koşmadı; yalnızca kod ve yapılandırma okundu |
| Hediye kodu ve sipariş yarışları (eşzamanlı istek) | Koşmadı; kilit kodu okundu, kilit mutantları hayatta kaldı |
| Canlı sunucu: `.env`, FPM havuzu, cron, kuyruk, sertifika | Görülmedi; durum yayın planı kaydından |
| GitHub Actions sonuçları | Görülmedi |
| Satır kapsamı | Ölçülemedi (Xdebug/PCOV yok); statik harita üretildi |
| Hesap silme ve parola değiştirme (arayüzden) | Tamamlanmadı; API'de yanlış parola reddi görüldü |
| Misafir fotoğraf yükleme (arayüzden) | Koşturulamadı: arayüzde yolu yok (`FE-51`) |
| Hata sınırı senaryosu (bileşen hatası, yüklenemeyen chunk) | Koşmadı |
| Gerçek telefon, Safari, Firefox, ekran okuyucu | Koşmadı; başsız Chromium |
| Havale/EFT akışı | Denetlenmedi (ayarla kapalı) |
| Resmî belgelerle API karşılaştırması (Laravel 13, React Router 7 ve diğerleri) | Yapılmadı; kaldırılmış API taraması yapıldı |
| `app/` altındaki 235 dosyanın tamamının satır satır okunması | Yaklaşık 75 dosya okundu, kalanı kalıp taramasıyla geçildi |
| 373 şablonun tarayıcıda açılması | 17'si açıldı; hepsi `verify:render` ile çizildi |
| Hukuki değerlendirme (KVKK, mesafeli satış) | Kapsam dışı; teknik gözlemler yazıldı |

### Ek C — `CLAUDE.md` ile çelişkiler

| Konu | `davetkart-docs/CLAUDE.md` | Bu denetimde | Sonuç |
|---|---|---|---|
| Dosya silme | §8: "Dosya silme: arşivle" | Dört boş taslak parça dosyası silindi | Dosyalar bu denetimin kendi ürettiği, içeriksiz ve commit'lenmemiş taslaklardı; arşivlenecek içerik yoktu. Plan (§4, R) silinmesini söylüyordu |
| Git yazma | §7: commit komutlarını ver, sen çalıştırma | Hiçbir git yazma komutu koşmadı | Uyumlu; commit komutları Ek F'de |
| Sırlar | §7: sırlar bu depoya yazılmaz | Test hesabının parolası ve bir onay bağlantısının imzası kanıtlara düşmüştü; ikisi de silindi | Uyumlu (düzeltildi). İkisi de yerel, atılacak bir test veritabanına aitti |
| Başka dokümanlara dokunma | Şartname §0-1: yalnızca `audits/README.md` ve `CHANGELOG.md`'ye birer satır | Yalnızca bu iki dosya değişti. `audits/README.md`'de artık yanlış olan "Bu depoda henüz denetim yok" cümlesinin yerine tek satırlık bir tablo; `CHANGELOG.md`'ye başlığıyla birlikte tek madde | Uyumlu (tablo başlığı nedeniyle birden fazla satır) |
| Karar numarası | §5: sıradaki boş numara indeksten | İndeks yanlış numara gösteriyor (`ARC-01`) | Denetim yeni karar yazmadı; önerilen numara K146'dan başlar |

### Ek D — Kanıt dizini

| Tür | Yer | Sayı |
|---|---|---|
| Komut çıktıları | `evidence/commands/` | 50 dosya (kurulum 3 · mimari 4 · güvenlik 4 · bağımlılık 6 · test 9 · frontend 4 · işletim 1 · uçtan uca 19) |
| Betikler | `evidence/scripts/` (16) ve `evidence/scripts/e2e/` (11) | 27 dosya |
| Mutasyon kayıtları | `evidence/mutation/M01…M51.txt` | 51 |
| Ekran görüntüleri | `evidence/screenshots/J1…J8-*.png` | 80 |

Sayılar raporun yazıldığı andaki dizin dökümünden alınmıştır (`ls evidence/<klasör> | wc -l`).

### Ek E — Temizlik (denetim bitince, İsmail)

- `D:\Projects\davetkart\_audit-snap\` klasörü (altı kod kopyası): silinebilir. Kanıt dosyaları
  bu klasöre bağımlı değil.
- Yerel PostgreSQL'de sekiz veritabanı: `davetkart_aud_{arc,sec,tst,e2e}` ve `…_test` eşleri. `davetkart_aud_e2e`
  içinde denetimin test hesabı, 4 davetiye, 2 sipariş, 2 LCV ve `AUDYUZDE20` hediye kodu var; hepsi sahte.
- `D:\Projects\davetkart\.playwright-mcp\` altındaki günlükler (Playwright MCP'nin kendi dosyaları).
- Frontend'in `node_modules/.vite` önbelleği kopyanın içindedir, kopyayla birlikte gider.

### Ek F — Commit komutları (çalıştırmak İsmail'e ait)

Denetim klasörü commit'lenmemiş durumda (`git status --short`: `?? audits/2026-11-12-full-system-audit/`,
` M audits/README.md`, ` M CHANGELOG.md`). `CLAUDE.md` §7 dosyaların tek tek eklenmesini istiyor; kanıt
klasöründe 200'den fazla dosya olduğu için aşağıda klasör yolları açıkça yazıldı (joker ve `-A` yok). Bu bir
sapmadır; uygun görmezsen dosya listesi `git status --short -uall` ile alınabilir.

```powershell
cd D:\Projects\davetkart\davetkart-docs
git add audits/2026-11-12-full-system-audit/README.md audits/2026-11-12-full-system-audit/PLAN.md audits/2026-11-12-full-system-audit/REPORT.md
git add audits/2026-11-12-full-system-audit/findings/01-architecture.md audits/2026-11-12-full-system-audit/findings/02-security.md audits/2026-11-12-full-system-audit/findings/03-testing.md audits/2026-11-12-full-system-audit/findings/04-frontend-e2e.md audits/2026-11-12-full-system-audit/findings/05-operations.md
git commit -m "docs(audits): Add AUD-2026-11-12 full system audit report and findings"
git status --short
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git add audits/2026-11-12-full-system-audit/evidence/commands audits/2026-11-12-full-system-audit/evidence/scripts audits/2026-11-12-full-system-audit/evidence/mutation audits/2026-11-12-full-system-audit/evidence/screenshots
git commit -m "docs(audits): Add AUD-2026-11-12 evidence (commands, scripts, mutation, screenshots)"
git status --short
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git add audits/README.md CHANGELOG.md
git commit -m "docs(audits): Register AUD-2026-11-12 in the audits index and changelog"
git status --short
```
