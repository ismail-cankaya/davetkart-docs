# PROMPT — FAZ 12: Shopier ile kartla ödeme

> **Hazırlanma:** 23 Ekim 2026 · **Önkoşul:** Faz 11 (Hediye Kodu) commit'lenmiş olmalı (`PROMPT-FAZ-11.md`)
> **Kullanım:** ① Önce **§A'yı sen doldur** (Shopier paneli). ② Sonra çizgiler arasını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır.

---

## §A — K94 GİRDİSİ (İsmail doldurur, prompt'u yapıştırmadan önce)

> 🔴 API **Secret**'ı buraya YAZMA. O yalnızca sunucudaki `.env` dosyasına girer.

| # | Soru | Cevap (Shopier panelinden ya da resmi dokümandan) |
|---|---|---|
| a | Klasik "harici site / API ile ödeme" akışı mı kullanılacak (`https://www.shopier.com/ShowProduct/api_pay4.php`)? Panelde bu ayarın menü yolu ne? | |
| b | Callback imzasında hangi alanlar var? (Topluluk SDK'sına göre: `random_nr + platform_order_id`; `status` **imzalı değil**). Resmi doküman ne diyor? | |
| c | Panelde **Otomatik Sipariş Bildirimi (OSB)** ya da webhook var mı? API ile başlatılan ödemelerde de geliyor mu? İçinde bizim `platform_order_id` (ya da eşlenebilir bir alan) var mı? Kullanıcı adı ve anahtar alanları var mı? | |
| d | **Başarısız** ödemede callback adresine POST geliyor mu? | (bilinmiyorsa "bilinmiyor"; Faz 12 sonunda elle denenecek) |
| e | `buyer_id_nr` (TCKN), telefon ve adres alanları zorunlu mu? Dijital ürün için yer tutucu değer kabul ediliyor mu? | |
| f | Test ortamı ya da test kartı var mı? | |
| g | `website_index` değeri | (genelde 1) |
| h | Resmi doküman bağlantısı ya da PDF'in `claude\Notlar\` altındaki yolu | |

**Boş bırakılan satırlar için ajan §4'teki güvenli varsayılanı uygular.**

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action mimarisi; frontend React 19 + TypeScript) **Faz 12: Shopier entegrasyonu** yapacağız. Kart bilgisi Shopier'in sayfasında girilecek, ödeme sitemizde onaylanacak. Yukarıdaki §A tablosu, Shopier panelinden benim topladığım bilgiler (karar kaydı **K94**'ün girdisi).

## 0. Bu fazda çalışma biçimi

1. **Bütün adımları (12.1 → 12.15) tek seferde, durmadan uygula.** Yalnızca §9'daki durumlarda dur.
2. 🔴 **`git add`, `git commit`, `git push`, `git stash`, `git reset`, `git checkout -- <dosya>` ÇALIŞTIRMA.** Commit'leri ben adım adım atacağım. Tek git yazma işlemin §2'deki dal oluşturma.
3. **Dosya sahipliği:** her dosya tek bir adıma ait olsun. İkinci kez dokunman gereken dosyayı sonraki adımın commit'ine taşı ve raporda belirt.
4. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `phpstan` ve ilgili testler. Sonda tam `composer check` ve frontend'de `npm run check`.
5. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı" yazma.
6. Koddaki yorumlar kısa olsun. Her yeni ya da anlamlı ölçüde değişen dosya için `docs/rehber/<aynı-yol>.md` kılavuzu yaz (öğrenen biri için: neden, hangi desen, hangi saldırı, sık hatalar, tinker ile deneme). Kılavuz kendi kod dosyasının commit'ine girer.
7. Türkçe yaz. Commit mesajları İngilizce: `12.6 - feat(payment): Add the Shopier gateway`.
8. **Gerçek Shopier'e hiçbir istek atma.** Testler sahte sır ve kendi hesapladığın imzalarla çalışır.

## 1. Başlamadan önce oku

1. `davetkart-backend-php-laravel\CLAUDE.md` · `claude\PHP-LARAVEL-SETUP.md` (§11, §13, §15) ve `PHP-LARAVEL-SETUP-EK-*.md` (son K numarası) · `docs\rehber\fazlar\FAZ-11.md` · `docs\08-HATA-SOZLESMESI.md` · `docs\10-URETIM-ENV-SABLONU.md`.
2. `claude.ai` projesindeki `claude/GOZDEN-GECIRME-RAPORU-2026-09-23.md` §4 dosyası diskte varsa onu da oku. Bu dosya Shopier ile mevcut arayüz arasındaki uyumsuzluk tablosunu içerir.
3. Ödeme katmanının tamamı: `app/Services/Payment/*`, `app/Actions/Payment/*`, `app/Actions/GiftCode/*`, `app/Http/Controllers/Api/V1/{PaymentController,PublicPaymentWebhookController,OrderController}.php`, `app/Http/Resources/OrderResource.php`, `config/payment.php`, `routes/api.php`, `AppServiceProvider::resolvePaymentGateway`, `tests/Feature/{PaywallTest,OrderTest,GiftCodeCheckoutTest}.php` (webhook'u çağıran yardımcı metotlar dahil).
4. Frontend: `src/pages/{CheckoutPage,PaymentReturnPage}.tsx`, `src/components/payment/checkout/*` (özellikle `CardPaymentForm.tsx`'in başındaki yorum tablosu), `src/stores/useCheckoutStore.ts`, `src/services/payments.ts`, `src/types*`, `src/locales/*`.
5. Referans: topluluk SDK'sı `erkineren/shopier` (GitHub). İmza formülleri §5'te özetlendi. **Paketi bağımlılık olarak EKLEME** (gerekçe §4-E4).

Okuduktan sonra 5–10 satırlık bir özet ver: §A'da hangi satırlar dolu, §4'ün hangi kolu seçildi, son K numarası. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git status                                # temiz değilse DUR
git log --oneline -20 | Select-String "^.{7} 11\."   # Faz 11 commit'leri yoksa DUR
git switch -c faz-12-shopier              # Faz 11'in bittiği daldan (main'e birleştiyse main'den)

cd D:\Projects\davetkart\davetkart-frontent
git status
git switch -c faz-12-shopier              # Faz 11 frontend dalından / main'den
```

## 3. Hedef akış

```
1. POST /api/v1/invitations/{id}/checkout {tier, giftCode?}
     → StartCheckoutAction (DEĞİŞMİYOR: fiyat sunucudan, Faz 11 indirimi dahil)
     → ShopierGateway::startCheckout → FormPostAction(url, imzalı alanlar)
   (tutar 0 → Faz 11'in gift yolu → RedirectAction(başarı sayfası), Shopier'e hiç gidilmez)
2. Frontend gizli <form>'u Shopier'e otomatik POST eder → kart Shopier'de yazılır
3a. Tarayıcı → POST /api/public/payments/shopier/callback → 303 → /odeme/basarili?order=…
3b. (OSB varsa) Shopier sunucusu → POST /api/public/payments/shopier/osb
4. HandlePaymentCallbackAction (DEĞİŞMİYOR: idempotans, kilit, K89, K100, K102)
5. /odeme/basarili → GET /orders/{id} ile durum sorgulanır → "Davetiyeni yayınla" (K67: ödeme yayınlamaz)
```

## 4. Kararlar (sıradaki boş K numaralarını sen ver; K94 = §A'nın kaydı)

| # | Karar |
|---|---|
| **E1 — Onay kanalı** | `config('payment.providers.shopier.confirmation')`, değerleri `osb` veya `callback`, env adı `SHOPIER_CONFIRMATION`. **`osb` modu:** tarayıcı callback'i hiçbir siparişi `paid` yapmaz, yalnızca kullanıcıyı yönlendirir; `paid` kararını yalnızca imzalı OSB bildirimi verir. **`callback` modu:** imzası doğrulanmış tarayıcı callback'i durumu işler. 🔴 **Varsayılan `osb`'dir** (fail-safe, K70 ruhu). Sebep: §A-b'ye göre `status` imzalı değil. Kendi başarısız ödemesinden geçerli bir imza alan kullanıcı, gövdeyi `status=success` yapıp tekrar gönderebilir. `callback` modu ancak §A-b `status`'ün imzalı olduğunu ya da §A-d başarısız ödemede callback gelmediğini **gösterirse** açılır. Bu karar `.env`'de bilinçli bir değişikliktir ve K94'e yazılır. §A-c "OSB yok" diyorsa yine `osb` varsayılanıyla yaz ve raporda bu durumu 🔴 olarak işaretle: canlıda ödemeler `pending` kalır ve karar İsmail'e düşer |
| **E2 — Arayüz** | `CheckoutSession` artık `CheckoutAction` taşır (tagged union): `RedirectAction(url)` ya da `FormPostAction(url, array<string,string> fields)`. "İkisi de dolu" gibi anlamsız durumlar temsil edilemez. `parseNotification(Request $request)`: imzanın nerede durduğu (başlık, form alanı) sürücünün bilgisidir (O/C). Bedeli: Services katmanı `Illuminate\Http\Request`'e bağlanır; kılavuzda tartış |
| **E3 — Sözleşme** | `OrderResource` yeni bir `checkout: {type:'redirect',url} \| {type:'form',url,fields}` alanı taşır. Eski `redirectUrl` alanı **`type=redirect` olduğu sürece korunur** (frontend kırılmasın; kaldırılması ayrı bir karar) |
| **E4 — Kendi sürücümüz** | `erkineren/shopier` HTML basıp `die` ediyor; bizim mimarimizde form gönderimini frontend yapıyor. Paketten alınacak şey birkaç satırlık bir formül; bağımlılık eklemeye değmez. Kaynak olarak kılavuzda anılır |
| **E5 — Kimlikler** | `platform_order_id` = `orders.id` (ULID) = `provider_ref` (UNIQUE, M8 korunur). Shopier'in `payment_id`'si yeni `orders.provider_payment_id` kolonuna yazılır (destek ve iade için) |
| **E6 — Callback yanıtı** | `303 See Other`. Hedef **istekten değil** `config('payment.return_urls')`'ten alınır (open redirect koruması). `order` parametresi yalnızca geçerli bir ULID ise eklenir. Geçersiz imza → `warning` log + `/odeme/hata` sayfasına yönlendirme. Bu, K69'dan bilinçli bir sapma (karşıda bir makine değil bir insan var), K kaydına gerekçesiyle yazılır. OSB ucu bir makine ucudur: K69 geçerli (imza hatası 404), başarı yanıtı Shopier'in beklediği gövdedir (§A/doküman; bilinmiyorsa `200 "success"`) |
| **E7 — Sır koruması** | `shopier` seçili ama `api_key` ya da `api_secret` boşsa (`osb` modunda OSB kimlikleri de) sürücü kurulmaz → 503 `PROVIDER_UNAVAILABLE`. Boş sırla hesaplanan HMAC'i herkes üretebilir |
| **E8 — Tutar biçimi** | `total_order_value` metni `amount_minor`'dan **tamsayı aritmetiğiyle** üretilir (`39900 → "399.00"`, `sprintf('%d.%02d', intdiv(..), ..%100)`). Float yasak. İmzaya giren metin ile forma yazılan metin aynı değişkenden gelir |
| **E9 — Alıcı alanları** | Ad, soyad ve e-posta kullanıcıdan alınır. Diğer zorunlu alanlar (§A-e) için `config`'te tanımlı yer tutucular kullanılır. §A-e "kabul edilmiyor" diyorsa DUR (§9) |

## 5. Shopier formülleri (topluluk SDK'sından; §A resmi dokümanla çelişirse **§A kazanır**)

- **Ödeme URL'i:** `https://www.shopier.com/ShowProduct/api_pay4.php` (POST, form-urlencoded)
- **Form alanları:** `API_key, website_index, platform_order_id, product_name, product_type (1 = dijital), buyer_name, buyer_surname, buyer_email, buyer_account_age, buyer_id_nr, buyer_phone, billing_address, billing_city, billing_country, billing_postcode, shipping_address, shipping_city, shipping_country, shipping_postcode, total_order_value, currency (0 = TL), platform (0), is_in_frame (0), current_language (0 = TR, 1 = EN), modul_version, random_nr, signature, callback`
- **İstek imzası:** `base64_encode(hash_hmac('sha256', random_nr . platform_order_id . total_order_value . currency, API_SECRET, true))`. `random_nr` değeri `random_int(100000, 999999)` ile üretilir
- **Callback alanları:** `platform_order_id, status ('success'|'failed'), installment, payment_id, random_nr, signature`
- **Callback imzası:** `hash_equals(hash_hmac('sha256', random_nr . platform_order_id, API_SECRET, true), base64_decode(signature))`
- **OSB (topluluk örneği):** iki alan gelir: `res` (base64 JSON) ve `hash`. Doğrulama: `hash_hmac('sha256', res . OSB_USERNAME, OSB_KEY)` (hex) ile `hash` alanı `hash_equals` üzerinden karşılaştırılır. Çözülen JSON alanları: `email, orderid, currency, price, buyername, buyersurname, productcount, productid, productlist, istest …`. 🔴 OSB'de **tutar ve para birimi** de doğrulanır: `price` değeri siparişin `amount_minor`'ıyla eşleşmezse `Log::critical` yazılır ve sipariş `paid` yapılmaz. `istest=1` ise yalnızca `APP_ENV != production` ortamında kabul edilir. OSB'nin siparişimizle nasıl eşleşeceği (§A-c) belirsizse eşleme adımını tek bir özel metotta topla ve raporda 🔴 olarak işaretle

## 6. Adımlar ve dosya sahipliği

### Backend

| # | Dosyalar | İş |
|---|---|---|
| **12.1** | `app/Services/Payment/{CheckoutAction,RedirectAction,FormPostAction}.php` | E2'deki değer nesneleri (`final readonly`). `FormPostAction` alan adı ve değerlerinin string olduğunu kurucuda doğrular |
| **12.2** | `app/Services/Payment/{CheckoutSession,PaymentGateway,FakeGateway}.php` · `app/Actions/Payment/{CheckoutResult,StartCheckoutAction}.php` · `app/Http/Controllers/Api/V1/{PaymentController,PublicPaymentWebhookController}.php` · `app/Http/Resources/OrderResource.php` · testlerdeki webhook yardımcı metodu (yalnızca o) | E2/E3 arayüz revizyonu. Faz 11'in gift yolu artık `RedirectAction(başarı url'i)` döner. Fake sürücünün imza başlığı ayarı sürücüye taşınır. 🔴 Ölçüt: `PaywallTest`, `OrderTest` ve `GiftCodeCheckoutTest` **iddiaları değiştirilmeden** yeşil kalır |
| **12.3** | `config/payment.php` · `.env.example` · `docs/10-URETIM-ENV-SABLONU.md` | `shopier` bloğu: `api_key, api_secret, website_index, payment_url, confirmation (osb), osb.username, osb.key, buyer_placeholders`. `iyzico` bloğu silinir. Kullanılmayan `webhook.tolerance_seconds` silinir (ders 26). Env adları: `SHOPIER_API_KEY, SHOPIER_API_SECRET, SHOPIER_WEBSITE_INDEX, SHOPIER_CONFIRMATION, SHOPIER_OSB_USERNAME, SHOPIER_OSB_KEY` |
| **12.4** | migration `…_add_provider_payment_id_to_orders` · `app/Models/Order.php` · `app/Services/Payment/PaymentNotification.php` · `app/Actions/Payment/HandlePaymentCallbackAction.php` | E5: nullable kolon + index. Bildirimde isteğe bağlı `providerPaymentId` ve (OSB için) isteğe bağlı `amountMinor`/`currency`. Action: ilerleyen geçişte `provider_payment_id` yazılır; bildirim tutar taşıyorsa ve tutar uyuşmuyorsa geçiş reddedilir + `Log::critical` (FAZ-10 denetiminin "bildirim tutar taşımıyor" bulgusu) |
| **12.5** | `app/Services/Payment/Shopier/ShopierSignature.php` · `app/Services/Payment/Shopier/ShopierAmount.php` · `tests/Unit/ShopierSignatureTest.php` | Saf fonksiyonlar: istek imzası, callback doğrulaması, OSB doğrulaması, E8 biçimlemesi. SDK'daki örnek değerlerle elle hesaplanmış sabit test vektörleri |
| **12.6** | `app/Services/Payment/ShopierGateway.php` · `tests/Feature/ShopierGatewayTest.php` | `name()='shopier'`. `startCheckout`: §5 alanları, E8, E9 → `FormPostAction`; `callback` alanı = callback rotasının mutlak URL'i. `parseNotification(Request)`: zorunlu alan → imza → durum çevirisi (`success→Paid`, `failed→Failed`, diğer → 400) → E1 moduna göre `callback` modunda bildirim döner, `osb` modunda **durum ilerletilmeyecek** bir sonuç döner (tasarımı sen seç: ayrı bir metot ya da sonuç tipi; arayüzü kirletmeden, kılavuzda gerekçelendir). OSB ayrıştırması ayrı bir metotta (`parseOsb(Request)`) |
| **12.7** | `app/Http/Controllers/Api/V1/{ShopierCallbackController,ShopierOsbController}.php` · `routes/api.php` · `tests/Feature/ShopierCallbackTest.php` · `tests/Feature/ShopierOsbTest.php` | İki auth'suz uç, K12 gereği `public` grubunda: `POST /api/public/payments/shopier/callback` ve `/osb`. E6 yanıtları. Mevcut `/payments/webhook` Fake için kalır. Testler (iki modda): geçerli success → paid + provider_payment_id; tekrar → tek geçiş; yanlış imza → DB değişmez + hata sayfası; 🔴 **failed imzasıyla status=success → `osb` modunda paid DEĞİL**; `callback` modunda bu riskin test adıyla belgelenmesi; bilinmeyen sipariş; süresi dolmuş siparişe geç ödeme (K89); open redirect denemesi; OSB tutar uyuşmazlığı → paid değil; OSB `istest` + production |
| **12.8** | `app/Providers/AppServiceProvider.php` · `tests/Feature/PaymentDriverResolutionTest.php` | `'shopier' => ShopierGateway`. E7: sır ya da OSB kimliği eksikse 503. Bilinmeyen sürücü yine 503 (K70) |
| **12.9** | `docs/rehber/fazlar/{FAZ-12,FAZ-12-ELLE-DOGRULAMA}.md` · `docs/rehber/fazlar/README.md` | Faz kaydı ve canlı doğrulama betiği (§8) |

### Frontend. 🔴 `git add -A` yasak

| # | Dosyalar | İş |
|---|---|---|
| **12.10** | `src/types*` · `src/services/payments.ts` | `checkout` birleşik tipi (E3). Eski `redirectUrl` geri dönüşü korunur |
| **12.11** | `src/stores/useCheckoutStore.ts` · `src/utils/submitProviderForm.ts` (yeni) | `form` tipinde: DOM'da gizli `<form method="post">` oluşturulur, değerler `input.value` ile atanır (HTML birleştirme yok, XSS yok), `submit()` çağrılır. `redirect` tipinde `window.location.assign` |
| **12.12** | `src/components/payment/checkout/CardPaymentForm.tsx` | Kart alanları **tamamen kalkar** (PCI DSS kapsamı dışı kalınır). Düğme "Güvenli ödeme sayfasına geç" olur, altında "Ödemeniz Shopier altyapısıyla alınır" notu. Dosya başındaki tablo yorumu güncellenir |
| **12.13** | `src/pages/PaymentReturnPage.tsx` | `?order=` ile `GET /orders/{id}`. Durum `pending` ise 3 sn arayla en fazla ~60 sn tekrar sorgulanır (OSB gecikmesi), sonra "Ödemeniz doğrulanıyor, birkaç dakika içinde Siparişlerim'de görünecek" mesajı. `paid` → "Davetiyeni yayınla" düğmesi. `failed`/`expired` → tekrar dene |
| **12.14** | `src/locales/*/translation.json` (10 dil) | Yeni metinler |

### Bağlam deposu

| # | Dosyalar | İş |
|---|---|---|
| **12.15** | `claude/PHP-LARAVEL-SETUP-EK-FAZ-12.md` (yeni) · `claude/PHP-LARAVEL-SETUP.md` | K94 (§A'nın tamamı ve seçilen E1 kolu) ve diğer K'lar; yol haritası; çalışan uçlar; §15'ten "Gerçek ödeme sürücüsü" satırının kapanması |

## 7. Güvenlik kontrol listesi

- [ ] Kart verisi hiçbir bileşenin state'ine, store'a, URL'ye ya da API'mize girmiyor (kart alanları yok).
- [ ] Fiyat ve indirim sunucuda hesaplanıyor; Shopier'e giden tutar imzanın içinde (değiştirilen form Shopier'de reddedilir).
- [ ] Bütün imza karşılaştırmaları `hash_equals` ile (W2); karşılaştırmadan önce `base64_decode(..., true)` kullanılıyor, başarısızsa red.
- [ ] Varsayılan mod `osb`; `callback` modunun riski K kaydında ve kılavuzda yazılı.
- [ ] Yönlendirme hedefi config'ten geliyor; `order` parametresi ULID doğrulamasından geçiyor.
- [ ] Sır eksikse 503; log'larda ve Sentry'de sır ya da imza yok.
- [ ] Callback ve OSB idempotan (aynı bildirim iki kez geldiğinde tek geçiş).
- [ ] Mevcut testlerin iddiaları değişmedi.

## 8. Canlı elle doğrulama betiği (12.9'da yazılacak, ben çalıştıracağım)

1. Deploy (`deploy.sh`). `.env`: `PAYMENT_PROVIDER=shopier`, `SHOPIER_*`. `php artisan config:cache` (unutulursa eski config okunur).
2. Shopier paneline callback ve OSB adreslerini gir.
3. Mutlu yol: gerçek kartla ödeme → başarı sayfası → DB'de `paid` + `provider_payment_id` → yayınla.
4. %50 hediye koduyla ödeme → Shopier sayfasındaki tutar indirimli mi?
5. Reddedilen kart → callback geliyor mu? (§A-d'yi kanıtlar ve K94'e işlenir)
6. 5. adımda gelen imzalı gövdeyi `curl` ile `status=success` yapıp tekrar gönder → `paid` **olmamalı**.
7. Ödedikten sonra dönüş sekmesini kapat → OSB ile yine `paid` oluyor mu?
8. Panelden iade → bize bildirim geliyor mu? Gelmiyorsa davetiyeyi yayından elle kaldırma (`orders:refund` komutu ihtiyacı) §15'e yazılır.
9. Sonuçlara göre `SHOPIER_CONFIRMATION` kararı kesinleşir ve K94 güncellenir.

## 9. Dur ve sor

- Çalışma ağacı temiz değil ya da Faz 11 commit'leri yok.
- §A-e alıcı alanlarında yer tutucu değerin kabul edilmediğini söylüyor.
- §A, §5'teki formüllerle çelişiyor ama yeni formülü kesin olarak çıkaramıyorsun.
- Mevcut bir testin **iddiasını** değiştirmeden geçiremiyorsun, ya da frontend'in okuduğu bir alanı kaldırman gerekiyor.

## 10. Rapor

1. Özet: §A'dan ne kullanıldı, E1'in hangi kolu seçildi ve neden, atanan K numaraları, sapmalar.
2. `composer check` ve `npm run check` çıktılarının son satırları (koşmadıysa "koşmadı").
3. **Commit komutları:** her adım için ayrı bir PowerShell bloğu. Dosyalar tek tek, açık yolla eklenir (joker ve `-A` yok); her bloğun sonunda `git status --short`. Biçim:

```powershell
# 12.1 — Checkout action value objects
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Services/Payment/CheckoutAction.php app/Services/Payment/RedirectAction.php app/Services/Payment/FormPostAction.php docs/rehber/app/Services/Payment/CheckoutAction.md
git commit -m "12.1 - feat(payment): Model checkout actions as redirect or signed form post"
git status --short
```
   En sonda `git push -u origin faz-12-shopier` komutları ayrı bir blokta.
4. Dosya sahipliği istisnaları.
5. Bana kalanlar: `.env` satırları (değersiz), panel ayarları, §8 betiği, açık 🔴'ler.

Başla: §1'i oku ve özetle, sonra §2'den itibaren durmadan devam et.

---
