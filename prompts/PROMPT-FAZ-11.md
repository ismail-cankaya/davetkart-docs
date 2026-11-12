# PROMPT — FAZ 11: Hediye Kodu (indirim + ücretsiz plan)

> **Hazırlanma:** 23 Ekim 2026 · **Önceki faz:** Faz 10 + yayın (`release-2026-10-20`)
> **Sonraki faz:** Faz 12 — Shopier (`PROMPT-FAZ-12.md`). Faz 12, bu fazın kodu commit'lendikten sonra başlar.
> **Kullanım:** Çizgiler arasındaki metni Claude Code'a (Windows, `D:\Projects\davetkart` klasöründe) **olduğu gibi** yapıştır.

---

Merhaba. DavetKart projemde (dijital davetiye SaaS'ı: backend PHP 8.5 + Laravel 13, modüler monolit + Action mimarisi; frontend React 19 + TypeScript) **Faz 11: Hediye Kodu** özelliğini geliştireceğiz.

## 0. Bu fazda çalışma biçimi (önceki fazlardan FARKLI)

1. **Bütün adımları (11.1 → 11.18) tek seferde, durmadan uygula.** Her dosyadan sonra onay bekleme. Yalnızca §9'daki "dur ve sor" durumlarında dur.
2. 🔴 **`git add`, `git commit`, `git push`, `git stash`, `git reset`, `git checkout -- <dosya>` ÇALIŞTIRMA.** Commit'leri ben adım adım atacağım. Senin tek git yazma işlemin §2'deki dal oluşturma.
3. **Dosya sahipliği kuralı:** Her dosya **tek bir adıma** ait olsun. Ben her adımı ayrı commit'leyeceğim; bir dosya iki adımda değişirse o dosyayı ayrı commit'lere bölemem. Bir dosyaya ikinci kez dokunman gerekirse, o dosyayı **sonraki adımın** commit listesine taşı ve bunu §10'daki rapora yaz.
4. **Kalite kapısı:** Her backend adımından sonra en azından `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testleri (`php artisan test --filter=...`) çalıştır. Kırmızıysa düzeltmeden ilerleme. Fazın sonunda **tam** `composer check`, frontend'de `npm run check` çalıştır.
5. 🔴 **B7 (dürüstlük kuralı):** Bir komutun çıktısını görmeden hiçbir dokümana "doğrulandı / geçti" yazma. Çalıştıramadığın bir şey varsa "koşmadı" yaz.
6. **Açıklama yeri:** Koddaki yorumlar kısa olsun (1–3 satır, "ne" ve kritik kural). Her yeni ya da anlamlı ölçüde değişen kod dosyası için `docs/rehber/<aynı-yol>.md` eğitim kılavuzu yaz ya da güncelle. Kılavuz PHP/Laravel'i öğrenen biri için yazılır: neden bu yaklaşım, hangi tasarım deseni, hangi saldırıyı ya da yarışı engelliyor, sık yapılan hatalar tablosu, `php artisan tinker` ile deneme. Frontend'de karşılığı `docs/rehber/src/...`. Kılavuz, ait olduğu kod dosyasıyla **aynı adımın** commit'ine girer.
7. Türkçe yaz. Commit mesajları İngilizce ve mevcut biçimde olsun: `11.7 - feat(gift-codes): Apply gift codes at checkout`.

## 1. Başlamadan önce oku

Okuma sırası:
1. `davetkart-backend-php-laravel\CLAUDE.md`: mimari katman kuralları.
2. `claude\PHP-LARAVEL-SETUP.md`: özellikle §11 İhlal Edilemez Kurallar, §13 Öğrenilen Dersler, §15 Açık Sorular. EK dosyaları da var (`PHP-LARAVEL-SETUP-EK-*.md`); son karar numarasını (K…) buradan bul.
3. `davetkart-backend-php-laravel\docs\rehber\fazlar\FAZ-10.md` ve `docs\08-HATA-SOZLESMESI.md`.
4. Ödeme katmanının tamamı: `app/Actions/Payment/*`, `app/Services/Payment/*`, `app/Services/Pricing/*`, `app/Enums/{OrderStatus,OrderScope,SubscriptionTier,ErrorCode}.php`, `app/Models/Order.php`, `orders` migration'larının hepsi, `app/Http/Controllers/Api/V1/{PaymentController,OrderController}.php`, `app/Http/Requests/Payment/StoreCheckoutRequest.php`, `app/Http/Resources/OrderResource.php`, `routes/api.php`, `app/Providers/AppServiceProvider.php` (rate limiter'lar), `app/Console/Commands/*` (örnek: `ListContactMessages`, `ExpireStaleOrders`), `tests/Feature/{PaywallTest,OrderTest}.php`.
5. Frontend: `src/pages/{CheckoutPage,PaymentReturnPage,PricingPage}.tsx`, `src/components/payment/**`, `src/stores/useCheckoutStore.ts`, `src/services/payments.ts`, `src/types*`, `src/contracts/{error-codes.json,errorCodes.ts}`, `src/locales/*`.

Okuduktan sonra bana **5–10 satırlık bir özet** ver: mevcut ödeme akışı, son K numarası, dal durumu. **Sonra durmadan** uygulamaya geç.

## 2. Dallar

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git status                      # temiz değilse DUR ve sor
git switch -c faz-11-hediye-kodu release-2026-10-20

cd D:\Projects\davetkart\davetkart-frontent
git status                      # temiz değilse DUR ve sor
git switch -c faz-11-hediye-kodu main
```

⚠️ Frontend şu an `design/kagit` dalında olabilir ve bu dal `main`'e birleşmemiş olabilir. Durum böyleyse **DUR ve bana sor:** dalı `main`'den mi yoksa `design/kagit`'ten mi açayım? `claude\` deposunda dal açma, mevcut dalında çalış.

## 3. Ürün gereksinimi (İsmail'in kararları)

- Hediye kodu, **koddan koda değişen** bir fayda verir:
  - **free**: belirli bir planı (tier) **ücretsiz** açar.
  - **percent**: yüzde indirim (1–100).
  - **fixed**: sabit tutar indirimi (₺).
- İki dağıtım biçimi var:
  - **Sabit kod**: elle belirlenen, akılda kalır bir kod (`DUGUN2026` gibi), toplamda **N kez** kullanılabilir.
  - **Tek kullanımlık kodlar**: toplu üretilir (`DK-7KQ2-M9XA-P4TR` gibi), her biri **1 kez** kullanılır.
- **Bir kullanıcı aynı kodu yalnızca bir kez kullanabilir.**
- Kodları ben **artisan komutlarıyla** üretip yöneteceğim. Admin paneli yok. Komutlar canlıda SSH üzerinden sunucuda çalışacak.
- **Bir siparişte yalnızca bir kod** kullanılabilir.

## 4. Mimari kararlar (bu fazda kayda geçecek; sıradaki boş K numaralarını sen ver)

| # | Karar | Gerekçe |
|---|---|---|
| D1 | **Hediye = sipariş.** İndirim sonrası tutar **0** olursa sağlayıcıya gidilmez. `provider='gift'`, `status=paid`, `amount_minor=0` olan bir `Order` yazılır | Yayın hakkı (`OrderEntitlementResolver`), bağlanmamış siparişi davetiyeye bağlama (`ClaimReleasedOrderAction`), paywall 402 kontrolü ve iade sonrası yayından kaldırma **hiç değişmeden** hediyeyi tanır. Ayrı bir hak kaynağı yazılsaydı her paywall noktası iki yere bakmak zorunda kalırdı |
| D2 | Tutar > 0 ise (kısmi indirim) normal ödeme akışı çalışır. Ödenecek tutar `price − discount` olur ve sipariş `discount_minor` alanını taşır | Faz 12'de Shopier imzalı tutarı doğrudan `amount_minor`'dan alacak; indirim sağlayıcıya şeffaf kalır |
| D3 | Veritabanında kodun kendisi değil, **SHA-256 özeti** (`code_hash`) saklanır. Listeleme için yalnızca son 4 karakter (`code_hint`) tutulur | Kod para değerinde. Veritabanı sızarsa tek kullanımlık kodlar ele geçmemeli. Tek kullanımlık kodlar yaklaşık 60 bit entropi taşır, özetten geri bulunamaz |
| D4 | **Kullanım sayısı saklanmaz, sipariş durumundan türetilir.** Bir kullanım, bağlı siparişi `pending`, `paid` veya `refunded` ise "aktif" sayılır; `failed` veya `expired` ise kullanım kendiliğinden iade olur | Sayaç kolonu (`redemptions_count`) terk edilen ödemelerde hiç geri düşmezdi, düşürmek için de her başarısızlık yoluna kod gerekirdi. Tek doğruluk kaynağı sipariş durumu. Yarış koşulu `gift_codes` satırındaki `lockForUpdate` ile kapanır |
| D5 | Kişi başı limit **1 aktif kullanım**. Kontrol, kod satırı kilitliyken yapılır | Kilit aynı kodun bütün kullanımlarını sıraya koyduğu için uygulama içi kontrol yarışsızdır. Ödemesi süresi dolan kullanıcı kodu tekrar deneyebilir; partial unique index gerekmez |
| D6 | İndirim **aşağı yuvarlanır**: `intdiv(price * percent, 100)`. Sabit indirim fiyatı aşamaz (`min`). `free` yalnızca kendi `tier`'ında geçerlidir. `percent`/`fixed` kodlarda `tier = null` "bütün planlar" demektir | Kuruş farkı işletmenin lehine. Tutarlar her zaman `int` kuruştur, float yasak |
| D7 | Bulunamadı, devre dışı, süresi doldu ve tükendi durumlarının hepsi **tek hata kodu** döner: `GIFT_CODE_INVALID` | Kod tahmin etmeye çalışana hangi kodların var olduğunu sızdırmaz. Ayrı kodlar: `GIFT_CODE_ALREADY_USED` ve `GIFT_CODE_NOT_APPLICABLE` (plan uyuşmazlığı). Hepsi 422 |
| D8 | İade edilen sipariş kullanımı **geri vermez** | Aksi halde iade et, tekrar kullan döngüsü kurulurdu |
| D9 | Tek kullanımlık kodlar **bir kez gösterilir**: CSV dosyasına yazılır, veritabanından geri okunamaz | D3'ün sonucu. CSV `storage/app/private/gift-codes/<batch>.csv` konumuna yazılır |
| D10 | K89'daki geç ödeme durumu: süresi dolup kullanımı iade olmuş bir sipariş sonradan `paid` olursa kullanım yeniden aktifleşir ve kod `max_redemptions`'ı 1 aşabilir. **Bilinen ve kabul edilen sınır** olarak belgelenir, kod yazılmaz | Nadir bir durum, kullanıcı parasını ödemiş oluyor. Engellemek, ödeme alınmış bir siparişi reddetmek demek olurdu |

## 5. Veri modeli

**`gift_codes`**
| Kolon | Tip | Not |
|---|---|---|
| `id` | ulid PK | |
| `code_hash` | char(64) UNIQUE | `hash('sha256', normalize(code))` |
| `code_hint` | varchar(8) | son 4 karakter |
| `label` | varchar(120) null | "Instagram çekilişi" gibi |
| `batch_id` | ulid null, index | toplu üretimin kimliği; sabit kodda null |
| `benefit` | varchar(16) | CHECK `IN ('free','percent','fixed')`, `GiftCodeBenefit` enum'undan türetilir |
| `tier` | varchar(16) null | CHECK tier listesi. `free` ise NOT NULL (CHECK) |
| `percent_off` | smallint null | CHECK 1–100. `benefit='percent'` ⇔ NOT NULL |
| `amount_off_minor` | unsigned int null | CHECK > 0. `benefit='fixed'` ⇔ NOT NULL |
| `max_redemptions` | unsigned int | CHECK ≥ 1 |
| `expires_at` | timestamp null | |
| `disabled_at` | timestamp null | silmek yerine devre dışı bırakılır (denetim izi) |
| timestamps | | |

**`gift_code_redemptions`**: `id` ulid · `gift_code_id` FK restrictOnDelete · `user_id` FK **nullOnDelete** (hesap silinince sayım korunur; sipariş tablosundaki uygulamanın aynısı) · `order_id` FK **UNIQUE** restrictOnDelete · `discount_minor` uint (o anki değer) · `created_at` · index `(gift_code_id, user_id)`.

**`orders` değişikliği:**
- `discount_minor` uint default 0, CHECK ≥ 0.
- `orders_amount_minor_check` kaldırılır, yerine şunlar gelir: `amount_minor >= 0`, `(amount_minor > 0) OR (provider = 'gift')` ve `(provider <> 'gift') OR (amount_minor = 0)`. Bu kural `if` ile değil kısıtla kurulur (E2).
- Migration'ın `down()` metodu eski kısıtı geri koyar (0 tutarlı satır varsa bunu kılavuzda uyarı olarak yaz).

## 6. Adımlar ve dosya sahipliği

Her satır bir commit'tir. Adım numarası commit mesajının önekidir. Her adımın kılavuz md'leri kendi commit'ine girer.

### Backend (`davetkart-backend-php-laravel`)

| # | Dosyalar | İş |
|---|---|---|
| **11.1** | `app/Enums/GiftCodeBenefit.php` · `database/migrations/…_create_gift_codes_table.php` | Enum: `values()`, `label()` yok. Migration: §5'teki kolonlar ve CHECK'ler (enum'dan türetilir, mevcut orders migration'ının kalıbında) |
| **11.2** | `database/migrations/…_create_gift_code_redemptions_table.php` · `database/migrations/…_add_discount_and_gift_rules_to_orders.php` | §5 |
| **11.3** | `app/Models/GiftCode.php` · `app/Models/GiftCodeRedemption.php` · `database/factories/{GiftCode,GiftCodeRedemption}Factory.php` · `app/Models/Order.php` | `#[Fillable]` boş (E7), alanlar açıkça atanır. Cast'ler (enum, tarih). İlişkiler. `GiftCode::discountFor(SubscriptionTier): int` (D6) ve `isApplicableTo(SubscriptionTier): bool`. Aktif kullanım sayımı için bir scope (D4). `Order::GIFT_PROVIDER = 'gift'` sabiti, `discount_minor` cast'i ve `giftCodeRedemption` ilişkisi |
| **11.4** | `app/Support/GiftCodes/GiftCodeFormat.php` · `tests/Unit/GiftCodeFormatTest.php` | `normalize()`: büyük harf, boşluk/tire temizleme. `hash()`. `generate()`: `random_int` + Crockford base32 alfabesi (0/O, 1/I/L yok), `DK` + 12 karakter, gösterim biçimi `DK-XXXX-XXXX-XXXX`. `isValidCustom()`: elle girilen kod için 4–32 karakter, `[A-Z0-9]` (normalize edildikten sonra) |
| **11.5** | `app/Enums/ErrorCode.php` · `app/Exceptions/GiftCodeException.php` · istisna→yanıt eşlemesi nerede yapılıyorsa orası (`bootstrap/app.php` ya da mevcut kalıp; `PaywallViolationException` nasıl render ediliyorsa öyle) · `docs/08-HATA-SOZLESMESI.md` | Üç yeni kod (D7). İsimli kurucular: `invalid()`, `alreadyUsed()`, `notApplicable(SubscriptionTier)` |
| **11.6** | `app/Actions/GiftCode/ReserveGiftCodeAction.php` · `app/Actions/GiftCode/GiftCodeQuote.php` | **Çağıranın açtığı transaction içinde** çalışır: kodu `code_hash` ile `lockForUpdate` ederek bulur → devre dışı/süre/tükenme kontrolü (D4: aktif sayım < max) → kişi başı kontrol (D5) → plan uygunluğu → `GiftCodeQuote{giftCode, discountMinor}` döner. Transaction dışında çağrılırsa kilit anlamsız olur: bunu `DB::transactionLevel() > 0` ile savunmacı olarak denetle |
| **11.7** | `app/Actions/Payment/StartCheckoutAction.php` · `app/Http/Requests/Payment/StoreCheckoutRequest.php` · `app/Http/Controllers/Api/V1/PaymentController.php` · `app/Http/Resources/OrderResource.php` · `tests/Feature/GiftCodeCheckoutTest.php` | İstek gövdesine isteğe bağlı `giftCode` alanı (string, en fazla 64 karakter; mevcut alan adlandırma kuralını izle). Action içinde **tek transaction**: kod rezervasyonu → sipariş (tutar = fiyat − indirim, `discount_minor`) → kullanım satırı. Tutar **0 ise** sipariş doğrudan `paid` olur: `paid_at=now`, `provider=gift`, `provider_ref='gift_'.ulid`, `expires_at=null`; gateway çağrılmaz; davetiye bağlıysa `InvitationChanged` olayı (K102 kalıbı); `redirectUrl` = `payment.return_urls.success?order={id}`. Tutar > 0 ise gateway çağrısı **transaction'dan sonra** yapılır (F3 kuralı korunur); başarısızlıkta sipariş `failed` olur ve kullanım D4 gereği kendiliğinden iade olur. `OrderResource` indirimi gösterir (mevcut para alanı biçimini izle). Testler: her fayda türü; `fixed` ≥ fiyat → gift yolu; yanlış plan; süresi dolmuş, devre dışı ve tükenmiş kod → INVALID; aynı kullanıcının ikinci denemesi → ALREADY_USED; ilk siparişi `expired` olduktan sonra tekrar kullanabilme; max 1 olan kodu ikinci kullanıcı deneyince INVALID; gift siparişiyle **yayınlayabilme** (paywall); bağlanmamış gift siparişinin `ClaimReleasedOrderAction` ile bağlanması; tutar istekten okunamaz |
| **11.8** | `app/Actions/GiftCode/PreviewGiftCodeAction.php` · `app/Http/Requests/GiftCode/PreviewGiftCodeRequest.php` · `app/Http/Controllers/Api/V1/GiftCodeController.php` · `routes/api.php` · `app/Providers/AppServiceProvider.php` · `tests/Feature/GiftCodePreviewTest.php` | `POST /api/v1/gift-codes/preview` `{code, tier}` → `{benefit, tier, discount, total, currency}`. Salt okunur: kilit yok, rezervasyon yok, ama aynı kurallar (kişi başı dahil) uygulanır. Yeni `gift-code` limiter'ı: kullanıcı başına dakikada 10, saatte 30. Hem preview hem iki checkout rotasına uygulanır. Testler: her fayda türü, hata kodları, 429 |
| **11.9** | `app/Actions/GiftCode/{CreateGiftCodeAction,GenerateGiftCodeBatchAction,GiftCodeSpec}.php` · `app/Console/Commands/{CreateGiftCode,GenerateGiftCodes}.php` · `tests/Feature/GiftCodeCreateCommandsTest.php` | Komutlar ince kalır (controller gibi); iş Action'dadır. `gift-codes:create {code} --benefit=free\|percent\|fixed --tier= --percent= --amount= --max-uses=1 --expires=YYYY-MM-DD --label=`. `gift-codes:generate --count= …` (1–1000, max-uses zorla 1; CSV yazılır; yol ve özet tablo basılır; kodlar konsola basılmaz). `--amount` ₺ cinsindendir ("150" ya da "150.50"), float kullanmadan kuruşa çevrilir. `--expires` günün sonudur ve `davetkart.default_timezone` ile yorumlanır. Geçersiz seçenek birleşimi açık bir hata mesajıyla reddedilir (free + percent gibi). Elle girilen kod zaten varsa açık hata (UNIQUE). Testler: `Storage::fake`; veritabanında kodun **düz hali olmadığını** doğrula; CSV içeriği |
| **11.10** | `app/Console/Commands/{ListGiftCodes,DisableGiftCode}.php` · `app/Actions/GiftCode/DisableGiftCodeAction.php` · `tests/Feature/GiftCodeAdminCommandsTest.php` | `gift-codes:list --active --batch=` tablosu: id, ipucu/etiket, fayda, plan, aktif/max, bitiş, durum. Sayım D4'teki scope ile yapılır ve N+1 sorgu olmaz (`withCount` + koşul). `gift-codes:disable {id}` (`disabled_at` atar, silmez; zaten kapalıysa bilgi verir) |
| **11.11** | `docs/rehber/fazlar/FAZ-11.md` · `docs/rehber/fazlar/FAZ-11-ELLE-DOGRULAMA.md` · `docs/rehber/fazlar/README.md` · `docs/10-URETIM-ENV-SABLONU.md` (gerekirse) · `README.md` (komut listesi varsa) | Faz kaydı: kararlar D1–D10 (atanan K numaralarıyla), sapmalar, dersler, bilinen sınırlar. Elle doğrulama: yerelde komutlar → preview → %50 kodla fake ödeme → free kodla anında yayın hakkı → aynı kodu ikinci kez deneme → disable → **canlıda** SSH komut örnekleri ve CSV'yi `scp` ile indirme |

### Frontend (`davetkart-frontent`). 🔴 `git add -A` yasak, dosyalar tek tek eklenir (CRLF)

| # | Dosyalar | İş |
|---|---|---|
| **11.12** | `src/contracts/error-codes.json` (backend'de `php artisan errors:export` çıktısıyla güncelle) · `src/contracts/errorCodes.ts` (gerekirse) · `src/locales/{tr,en}/errors.json` | Üç yeni hata kodunun metinleri |
| **11.13** | `src/types*` (ilgili dosya) · `src/services/payments.ts` · ilgili kılavuz | `previewGiftCode(code, tier)`; checkout çağrılarına isteğe bağlı `giftCode` eklenir |
| **11.14** | `src/stores/useCheckoutStore.ts` | `giftCode`, `giftPreview` ve uygula/kaldır eylemleri. `startCardCheckout` kodu iletir. Plan değişince önizleme yeniden hesaplanır |
| **11.15** | `src/components/payment/checkout/GiftCodeField.tsx` (yeni) · `src/pages/CheckoutPage.tsx` · özet/tutar bileşeni (hangisiyse) · `src/pages/PaymentReturnPage.tsx` (gerekirse) | "Hediye kodum var" açılır alanı → Uygula → indirim satırı ve yeni toplam. **Toplam 0 ise** kart/havale bölümü gizlenir, düğme "Ücretsiz etkinleştir" olur, checkout çağrılır ve dönen `redirectUrl`'e (başarı sayfası) gidilir. Hata kodları i18n'den okunur |
| **11.16** | `src/locales/*/translation.json` (10 dil) | Yeni arayüz metinleri; hiçbir dil eksik kalmasın (`npm run verify` bunu denetliyorsa çalıştır) |

### Bağlam deposu (`claude`)

| # | Dosyalar | İş |
|---|---|---|
| **11.17** | `claude/PHP-LARAVEL-SETUP-EK-FAZ-11.md` (yeni) · `claude/PHP-LARAVEL-SETUP.md` | Atanan K numaraları; §10 yol haritasına Faz 11 satırı (Faz 12 = Shopier); çalışan uç noktalar; §11'e eklenen kurallar; §15 açık sorular |

> 11.18 yok. Toplam 17 commit. Bir adımı birleştirmen ya da bölmen gerekirse sebebini §10 raporuna yaz.

## 7. Güvenlik ve doğruluk kontrol listesi (bitirmeden önce kendin denetle)

- [ ] Tutar ve indirim **her zaman** sunucuda hesaplanıyor; istekte `amount` ya da `discount` alanı varsa yok sayılıyor (testle kanıtla).
- [ ] Rezervasyon + sipariş + kullanım satırı **tek transaction**, gateway çağrısı transaction'ın **dışında ve sonrasında**.
- [ ] `lockForUpdate` kod satırında. Kişi başı ve toplam kontrol **kilit alındıktan sonra** yapılıyor (E9 check-then-act).
- [ ] Bütün para değerleri `int` kuruş; `float` yok (komut seçeneği ayrıştırması dahil).
- [ ] Bilinmeyen, devre dışı, süresi dolmuş ve tükenmiş kodun yanıtı **bayt bayt aynı**.
- [ ] Veritabanında, log'larda ve Sentry bağlamında düz kod yok (log'a en fazla `code_hint` yazılır).
- [ ] Gift siparişi `orders_paid_at_check` ve yeni CHECK'lerle uyumlu; DB seviyesinde `provider='gift'` + `amount_minor>0` reddediliyor (testle kanıtla).
- [ ] Mevcut `PaywallTest` ve `OrderTest` **değiştirilmeden** yeşil.
- [ ] Yeni hata kodları `errors:export --check`'ten geçiyor ve frontend kataloğunda var.

## 8. Kapsam dışı (yapma)

Shopier ve `PaymentGateway` arayüzü değişikliği (Faz 12) · admin paneli · kod başına kişi limiti seçeneği (sabit 1) · birden fazla kodu birleştirme · kampanya başlangıç tarihi · `.env` dosyasına dokunmak (`.env.example` serbest).

## 9. Dur ve sor (yalnızca bu durumlarda)

- Çalışma ağacı başta temiz değil, ya da frontend dal tabanı belirsiz (§2).
- Mevcut bir **sözleşme** alanını (frontend'in okuduğu JSON alanı) kaldırman ya da yeniden adlandırman gerekiyor.
- Mevcut bir testi **değiştirmeden** geçiremiyorsun.
- §4'teki bir kararla çelişen bir kod gerçeği buldun.

## 10. Bitirdiğinde bana vereceğin rapor

1. **Özet:** ne yapıldı, §4'teki kararlara hangi K numaraları verildi, plandan sapmalar ve gerekçeleri.
2. **Kalite kapısı:** `composer check` ve `npm run check` çıktılarının **son satırları** (kopyala; koşmadıysa "koşmadı" yaz).
3. **Commit komutları:** her adım için ayrı bir PowerShell bloğu. Dosyalar **tek tek ve açık yolla** eklenir; joker ve `-A` yok. Biçim:

```powershell
# 11.1 — Gift code enum + table
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Enums/GiftCodeBenefit.php database/migrations/2026_10_23_100000_create_gift_codes_table.php docs/rehber/app/Enums/GiftCodeBenefit.md docs/rehber/database/migrations/2026_10_23_100000_create_gift_codes_table.md
git commit -m "11.1 - feat(gift-codes): Add the gift code benefit enum and table"
git status --short    # bu adımın dosyası kalmamalı
```

   Her bloğun sonunda `git status --short` olsun. En sonda üç depo için `git push -u origin faz-11-hediye-kodu` komutlarını **ayrı** bir blokta ver (claude deposu için mevcut dal adıyla).
4. **Dosya sahipliği istisnaları:** birden fazla adımda değişen dosyalar ve hangi commit'e konuldukları.
5. **Sana kalanlar:** yerelde `php artisan migrate`, elle doğrulama betiği (`FAZ-11-ELLE-DOGRULAMA.md`), canlıya alırken çalıştırılacak komutlar.

Başla: önce §1'deki dosyaları oku ve özetle, sonra §2'den itibaren durmadan devam et.

---
