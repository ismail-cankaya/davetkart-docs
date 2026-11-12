# `PHP-LARAVEL-SETUP.md` — Faz 12 Yaması

> **Tarih:** 24 Ekim 2026
> **Ne bu:** Ana devir dosyasına (`claude/PHP-LARAVEL-SETUP.md`) **işlenmeyi bekleyen** Faz 12
> kayıtları. `-EK-FAZ-5…11` dosyalarıyla aynı biçim.
> **Tam kayıt:** `davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-12.md`
> 🔴 **Ana dosyaya işlenmedi:** `PHP-LARAVEL-SETUP.md`'de hâlâ commit'lenmemiş bir değişiklik
> var ve `EK-FAZ-11` de işlenmeyi bekliyor. Sıra: o değişiklik commit'lenir → EK-11 işlenir →
> bu dosyanın A–F bölümleri işlenir.

---

## A. Karar Kaydı'na eklenecek (§7)

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K94** | **§A girdisi: BOŞ.** Varsayılanlar: klasik `api_pay4.php`; ödeme imzası `base64(HMAC(random_nr·order_id·tutar·para_birimi))`; callback imzası `random_nr·platform_order_id` (`status` imzasız); OSB `res`+`hash = hex(HMAC(res·kullanıcı_adı, anahtar))`, yanıt `success`; `website_index=1`; alıcı yer tutucuları | Kaynak topluluk SDK'sı (`erkineren/shopier`) ve OSB örnekleri, resmi doküman değil. Kural 11 ("tahminle kod yazılmaz") prompt'un §4 güvenli varsayılanlarıyla dengelendi | ⚠️ elle doğrulamadan sonra güncellenecek |
| **K117** | Onay kanalı `SHOPIER_CONFIRMATION`, varsayılan **`osb`**: tarayıcı callback'i yalnızca yönlendirir, `paid`'i yalnızca imzalı OSB verir | Callback'te `status` imzasız: başarısız ödemenin imzalı gövdesinde `status=success` yapan bedava plan alır. `callback` modu ancak `status` imzalıysa ya da başarısızda callback gelmiyorsa | ✅ Faz 12 |
| **K118** | `CheckoutSession` bir `CheckoutAction` taşır: `RedirectAction(url)` \| `FormPostAction(url, fields)`. `PaymentGateway::parseNotification(Request)` | Geçersiz durumlar temsil edilemesin. İmzanın nerede durduğu sürücünün bilgisi (O/C). Bedel: Services katmanı `Request`'i tanıyor | ✅ Faz 12 |
| **K119** | `OrderResource.checkout = {type:'redirect',url} \| {type:'form',url,fields}`; `redirectUrl` `type=redirect` iken korunur | Frontend kırılmasın; iki depo ayrı yayınlanabilsin | ✅ Faz 12 |
| **K120** | Shopier paketi eklenmez, kendi sürücümüz | SDK HTML basıp `die` ediyor; alınacak şey birkaç satırlık formül | ✅ Faz 12 |
| **K121** | `platform_order_id = orders.id = provider_ref` (M8 korunur); Shopier'in kimliği `orders.provider_payment_id` (nullable, index, UNIQUE değil) | Destek/iade için Shopier'in kimliği gerekli; idempotans `provider_ref`'te | ✅ Faz 12 |
| **K122** | Callback yanıtı **303**, hedef `config('payment.return_urls')`'ten, `order` yalnızca ULID ise; geçersiz imza → `/odeme/hata` + `warning` | **K69'dan bilinçli sapma:** karşıda insan var, 404 JSON ona boş sayfa. OSB makine ucu: K69 geçerli | ✅ Faz 12 |
| **K123** | Sır, mod ya da (`osb` modunda) OSB kimliği eksikse `ShopierGateway` kurulmaz → 503 | Boş sırla HMAC'i herkes üretir. Kontrol kurucuda: controller'lar sürücüyü doğrudan istiyor | ✅ Faz 12 |
| **K124** | Tutar metni `sprintf('%d.%02d', intdiv, %)`; imzaya giren ve forma yazılan aynı değişken | Float yasak; tek bayt fark = imza hatası | ✅ Faz 12 |
| **K125** | Ad/soyad/e-posta kullanıcıdan; TCKN, telefon, adres `config('payment.providers.shopier.buyer_placeholders')` | KVKK: toplamadığımız veriyi istemeyelim. §A-e "kabul edilmiyor" derse değişir | ⚠️ elle doğrulama |
| **K126** | Bildirim tutar taşıyorsa (OSB) siparişin `amount_minor` + `currency`'siyle eşleşmeli; uymazsa geçiş yok + `Log::critical`. `istest=1` üretimde 400 | İmza "kimden" der, "neyin bedeli" demez (FAZ-10 denetiminin bulgusu) | ✅ Faz 12 |
| **K127** | Tarayıcı callback'i ayrı metot (`parseCallback`) ve ayrı tip (`ShopierCallback`); `osb` modunda bildirim nesnesi **hiç üretilmez**. Arayüzün `parseNotification`'ı Shopier'de OSB | `PaymentNotification`'ın sözü "işlenebilir bildirim"; istisna eklemek yerine imkânsız kıl | ✅ Faz 12 |

---

## B. Kurallar'a eklenecek (§11)

| # | Kural | En kısa hâli |
|---|---|---|
| **W4** | İmzalı bir mesajda yalnızca imzanın **kapsadığı** alanlara güvenilir | *İmza neyi kapsıyorsa onu kanıtlar, fazlasını değil* |
| **W5** | Sağlayıcı tutar bildiriyorsa siparişin tutarıyla karşılaştırılır | *İmza göndereni kanıtlar, bedeli kanıtlamaz* |

> **Toplam:** … + FAZ-11: 2 + **FAZ-12: 2**

---

## C. Dersler'e eklenecek (§13)

**69. İmza, kapsadığı alanlardan fazlasını kanıtlamaz.** Shopier callback'inde `status` imzanın
dışında. "İmzalı istek" demeden önce "imzaya hangi baytlar giriyor?" sorulur.

**70. İmza "kimden" der, "neyin bedeli" demez.** Doğru imzalı bir bildirim yanlış siparişle
eşleşebilir; tutar karşılaştırması kimlik doğrulamasını tamamlar.

**71. Bir değeri onu üreten fonksiyonla sınamak, onu kendisiyle karşılaştırmaktır.** İmza test
vektörleri bağımsız bir araçla (Python `hmac`) hesaplandı.

**72. Bulut çalışma alanında PHP 8.5 kurulumu.** Ubuntu deposu PHP 8.3 veriyor (Symfony 8.1
açılmıyor). conda-forge'dan `php-8.5.12` + bağımlılıkları indirildi, `icu` 78'e sabitlendi,
GD eklentisi `php-src` (8.5.12 etiketi) `ext/gd`'den `phpize` ile derlendi. `phpstan/phpstan`
paketi GitHub API'si kapalı olduğu için İsmail'in `vendor/` klasöründen alındı.

---

## D. §9 Teknik Durum: güncelleme

### Çalışan uç noktalar (yeni ve değişen)

| Uç | Ne |
|---|---|
| `POST /api/invitations/{id}/checkout`, `/api/payments/checkout` | + `checkout: {type, url, fields?}`; Shopier'de `redirectUrl` yok |
| `POST /api/public/payments/shopier/callback` | Tarayıcı dönüşü, form gövdesi → 303 `/odeme/basarili?order=…` ya da `/odeme/hata` |
| `POST /api/public/payments/shopier/osb` | Shopier sunucusu, `res`+`hash` → `200 success` · imza hatası 404 |
| `POST /api/public/payments/webhook` | Değişmedi (Fake) |

### Tablolar

`orders.provider_payment_id` (varchar 64, nullable, index)

### Config / env

`SHOPIER_API_KEY` · `SHOPIER_API_SECRET` · `SHOPIER_WEBSITE_INDEX` · `SHOPIER_CONFIRMATION` ·
`SHOPIER_OSB_USERNAME` · `SHOPIER_OSB_KEY`. Silinen: `IYZICO_*`, `payment.webhook.*`.

### Kalite kapısı

`composer check` **781/781** (bulut çalışma alanı, PHP 8.5.12 + PostgreSQL 16; İsmail'in
makinesinde koşmadı). Adım adım: 694 → 694 → 694 → 699 → 728 → 751 → 774 → 781.
Frontend `npm run check` yeşil (her adım ayrı ayrı).

---

## E. §10 Yol Haritası: güncelleme

| Faz | Konu | Durum |
|---|---|---|
| **11** | Hediye kodu | ⚠️ elle doğrulama bekliyor |
| **12** | Shopier ile kartla ödeme | ⚠️ backend ✅ (12.1–12.9) · frontend ✅ (12.10–12.14) · 🔴 §A boş · canlı elle doğrulama bekliyor |

---

## F. §15 Açık Sorular: güncelleme

### ✅ Kapananlar

- ~~Gerçek ödeme sürücüsü + imza sırrı~~ → `ShopierGateway` (K117–K127). W1'in Shopier karşılığı: *alanların belgelenmiş birleşim sırası* (`ShopierSignature`)
- ~~`payment.webhook.tolerance_seconds` — ya uygula ya sil~~ → **silindi** (Shopier imzasında zaman damgası yok; tekrar gönderimi durum makinesi kapatıyor)
- ~~`SubscriptionTier::label()` hiçbir yerden çağrılmıyor~~ → Shopier `product_name`'i
- ~~23 Eylül #9: Shopier — arayüz uyumu~~ → K118, K119

### ⬜ Faz 12'nin eklediği

1. 🔴 §A'nın sekiz satırı (Shopier paneli) → K94
2. 🔴 OSB → sipariş eşlemesi (`ShopierGateway::matchOsbToOrder`) — elle doğrulama adım 7
3. Shopier iadesi bize bildirilmiyorsa `orders:refund` komutu (K100 ancak `refunded` ile tetiklenir)
4. Yer tutucu TCKN reddedilirse: kullanıcıdan TCKN istemek (KVKK kararı)
5. Kullanılmayan eski kart arayüzü (`CardPreview`, `CardBrandMark`, `utils/paymentCard.ts`) silinsin mi?
6. `PaymentReturnPage`'in eski metinleri çeviriye taşınsın mı?
7. 🔴 **K67 ile frontend 11.6 çelişiyor mu?** K67 "ödeme yayınlamaz" diyor; frontend 11.6 (Faz 12 sırasında commit'lendi) dönüş sayfasında `paid` olunca `POST …/publish`'i kendiliğinden çağırıyor. Backend tarafında K67 hâlâ doğru (yayın ayrı bir istek, 402 kontrolü sunucuda). K67'nin metni "ödeme bildirimi yayınlamaz; dönüş sayfası kullanıcı adına yayın isteği atar" diye güncellensin mi?
