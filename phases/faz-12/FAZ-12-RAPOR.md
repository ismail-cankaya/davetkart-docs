# Faz 12 — Rapor (24 Ekim 2026)

## 1. Özet

- **§A (K94): sekiz satırın hiçbiri dolu değildi.** §4'ün güvenli varsayılanları uygulandı. Formüller topluluk kaynaklarından (`erkineren/shopier`, OSB örnekleri). Gerçek Shopier'e hiç istek atılmadı.
- **E1: `osb` kolu** (varsayılan). Sebep: callback'te `status` imzasız. `osb` modunda tarayıcı callback'i yalnızca yönlendiriyor, `paid` kararını yalnızca imzalı OSB veriyor. 🔴 Panelde OSB kurulmazsa canlıda ödemeler `pending` kalır.
- **Atanan K'ler:** K94 (§A) · K117 onay kanalı · K118 `CheckoutAction` + `parseNotification(Request)` · K119 `OrderResource.checkout` · K120 paket yok · K121 kimlikler + `provider_payment_id` · K122 callback 303 (K69'dan sapma) · K123 sır koruması · K124 tutar biçimi · K125 alıcı yer tutucuları · K126 tutar karşılaştırması + `istest` · K127 callback ayrı metot. Yeni kurallar **W4, W5** (W3 doluydu). Dersler **69–72**.
- **Sapmalar:**
  - Callback ayrı metot (`parseCallback`). Arayüzün `parseNotification`'ı Shopier'de OSB.
  - Sır kontrolü `AppServiceProvider`'da değil, `ShopierGateway` kurucusunda.
  - Callback adresi bir sabit (`CALLBACK_PATH`); rota ile eşitliği testle kilitli.
  - `claude/PHP-LARAVEL-SETUP.md`'ye dokunulmadı: commit'lenmemiş değişiklik + işlenmemiş EK-11 var. Kayıt `EK-FAZ-12`'de.
  - 🔴 **Frontend'e Faz 12 sırasında `911fa28 11.6` (otomatik yayın) commit'i geldi.** İlk teslimde `PaymentReturnPage.tsx/.md` o commit'in üstüne yazılmıştı. Fark edilip düzeltildi: 12.10–12.14 11.6'nın üstüne yeniden kuruldu, `useAutoPublish` aynen korunuyor, "Davetiyeni yayınla" düğmesi yazılmadı. Diğer iki 11.6 dosyasına (`PaywallModal`, `useAutoPublish`) hiç dokunulmadı.

## 2. Kalite kapısı (bulut çalışma alanı: PHP 8.5.12 + GD + PostgreSQL 16, Node 22)

- Backend `composer check`: **781/781**, pint passed, phpstan 0 hata, `Katalog guncel`. Başlangıç 684/684.
- Her adım ayrı ayrı: 12.1 694 · 12.2 694 · 12.3 694 · 12.4 699 · 12.5 728 · 12.6 751 · 12.7 774 · 12.8 781.
- Frontend `npm run check`: yeşil. 12.10–12.14'ün her biri 11.6'nın üstünde ayrı ayrı yeşil.
- **Senin makinende koşmadı.**

## 3. Commit komutları

```powershell
# 12.1
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Services/Payment/CheckoutAction.php app/Services/Payment/FormPostAction.php app/Services/Payment/RedirectAction.php docs/rehber/app/Services/Payment/CheckoutAction.md
git add tests/Unit/CheckoutActionTest.php
git commit -m "12.1 - feat(payment): Model checkout actions as redirect or signed form post"
git status --short
```

```powershell
# 12.2
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Actions/Payment/CheckoutResult.php app/Actions/Payment/StartCheckoutAction.php app/Http/Controllers/Api/V1/PaymentController.php app/Http/Controllers/Api/V1/PublicPaymentWebhookController.php
git add app/Http/Resources/OrderResource.php app/Services/Payment/CheckoutSession.php app/Services/Payment/FakeGateway.php app/Services/Payment/PaymentGateway.php
git add docs/rehber/app/Actions/Payment/StartCheckoutAction.md docs/rehber/app/Http/Controllers/Api/V1/PaymentController.md docs/rehber/app/Http/Controllers/Api/V1/PublicPaymentWebhookController.md docs/rehber/app/Http/Resources/OrderResource.md
git add docs/rehber/app/Services/Payment/FakeGateway.md docs/rehber/app/Services/Payment/PaymentGateway.md docs/rehber/tests/Feature/GiftCodeCheckoutTest.md docs/rehber/tests/Feature/PaywallTest.md
git add tests/Feature/GiftCodeCheckoutTest.php tests/Feature/PaywallTest.php
git commit -m "12.2 - refactor(payment): Let drivers read their own notification requests"
git status --short
```

```powershell
# 12.3
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add .env.example config/payment.php docs/10-URETIM-ENV-SABLONU.md docs/rehber/config/payment.md
git commit -m "12.3 - chore(payment): Replace the Iyzico config with Shopier settings"
git status --short
```

```powershell
# 12.4
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Actions/Payment/HandlePaymentCallbackAction.php app/Models/Order.php app/Services/Payment/PaymentNotification.php database/migrations/2026_10_24_100000_add_provider_payment_id_to_orders.php
git add docs/rehber/app/Actions/Payment/HandlePaymentCallbackAction.md docs/rehber/app/Models/Order.md docs/rehber/database/migrations/2026_10_24_100000_add_provider_payment_id_to_orders.md docs/rehber/tests/Feature/PaymentNotificationAmountTest.md
git add tests/Feature/PaymentNotificationAmountTest.php
git commit -m "12.4 - feat(payment): Record the provider payment id and reject mismatched amounts"
git status --short
```

```powershell
# 12.5
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Services/Payment/Shopier/ShopierAmount.php app/Services/Payment/Shopier/ShopierSignature.php docs/rehber/app/Services/Payment/Shopier/ShopierAmount.md docs/rehber/app/Services/Payment/Shopier/ShopierSignature.md
git add tests/Unit/ShopierSignatureTest.php
git commit -m "12.5 - feat(payment): Add the Shopier signature and amount helpers"
git status --short
```

```powershell
# 12.6
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Services/Payment/Shopier/ShopierCallback.php app/Services/Payment/Shopier/ShopierConfirmation.php app/Services/Payment/ShopierGateway.php docs/rehber/app/Services/Payment/ShopierGateway.md
git add docs/rehber/tests/Feature/ShopierGatewayTest.md tests/Feature/ShopierGatewayTest.php
git commit -m "12.6 - feat(payment): Add the Shopier gateway"
git status --short
```

```powershell
# 12.7
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Http/Controllers/Api/V1/ShopierCallbackController.php app/Http/Controllers/Api/V1/ShopierOsbController.php docs/rehber/app/Http/Controllers/Api/V1/ShopierCallbackController.md docs/rehber/app/Http/Controllers/Api/V1/ShopierOsbController.md
git add docs/rehber/routes/api.md docs/rehber/tests/Feature/ShopierCallbackTest.md docs/rehber/tests/Feature/ShopierOsbTest.md routes/api.php
git add tests/Feature/ShopierCallbackTest.php tests/Feature/ShopierOsbTest.php
git commit -m "12.7 - feat(payment): Add the Shopier callback and OSB endpoints"
git status --short
```

```powershell
# 12.8
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Providers/AppServiceProvider.php docs/rehber/app/Providers/AppServiceProvider.md docs/rehber/tests/Feature/PaymentDriverResolutionTest.md tests/Feature/PaymentDriverResolutionTest.php
git commit -m "12.8 - feat(payment): Resolve the Shopier driver and refuse missing secrets"
git status --short
```

```powershell
# 12.9
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add docs/rehber/fazlar/FAZ-12-ELLE-DOGRULAMA.md docs/rehber/fazlar/FAZ-12.md docs/rehber/fazlar/README.md
git commit -m "12.9 - docs(payment): Record Phase 12 and its live verification script"
git status --short
```

```powershell
# 12.10  (🔴 git add -A YASAK — dosyalar tek tek)
cd D:\Projects\davetkart\davetkart-frontent
git add docs/rehber/src/services/payments.md docs/rehber/src/types.md src/services/payments.ts src/types.ts
git commit -m "12.1 - feat(payment): Read the checkout action from the order response"
git status --short
```

```powershell
# 12.11  (🔴 git add -A YASAK — dosyalar tek tek)
cd D:\Projects\davetkart\davetkart-frontent
git add docs/rehber/src/services/payments.md docs/rehber/src/stores/useCheckoutStore.md docs/rehber/src/utils/submitProviderForm.md scripts/verify-payment.ts
git add src/stores/useCheckoutStore.ts src/utils/submitProviderForm.ts
git commit -m "12.2 - feat(payment): Post the signed provider form from the checkout store"
git status --short
```

```powershell
# 12.12  (🔴 git add -A YASAK — dosyalar tek tek)
cd D:\Projects\davetkart\davetkart-frontent
git add docs/rehber/src/components/payment/checkout/CardPaymentForm.md src/components/payment/checkout/CardPaymentForm.tsx
git commit -m "12.3 - feat(payment): Replace the card fields with the secure payment page button"
git status --short
```

```powershell
# 12.13  (🔴 git add -A YASAK — dosyalar tek tek)
cd D:\Projects\davetkart\davetkart-frontent
git add docs/rehber/src/pages/PaymentReturnPage.md src/pages/PaymentReturnPage.tsx src/utils/paymentReturn.ts
git commit -m "12.4 - feat(payment): Poll the return page for a minute while Shopier confirms"
git status --short
```

```powershell
# 12.14  (🔴 git add -A YASAK — dosyalar tek tek)
cd D:\Projects\davetkart\davetkart-frontent
git add src/locales/ar/translation.json src/locales/de/translation.json src/locales/en/translation.json src/locales/es/translation.json
git add src/locales/fr/translation.json src/locales/hi/translation.json src/locales/pt/translation.json src/locales/ru/translation.json
git add src/locales/tr/translation.json src/locales/zh/translation.json
git commit -m "12.5 - feat(i18n): Translate the Shopier checkout texts into ten languages"
git status --short
```

```powershell
# 12.15 — bağlam deposu (yalnızca yeni dosya; PHP-LARAVEL-SETUP.md'deki eski değişikliğe dokunma)
cd D:\Projects\davetkart\claude
git add PHP-LARAVEL-SETUP-EK-FAZ-12.md
git commit -m "12.6 - docs: Record the Phase 12 decisions for the context repo"
git status --short
```

```powershell
# push
cd D:\Projects\davetkart\davetkart-backend-php-laravel ; git push -u origin faz-12-shopier
cd D:\Projects\davetkart\davetkart-frontent ; git push -u origin faz-12-shopier
```

## 4. Dosya sahipliği istisnaları

| Dosya | Adım | Not |
|---|---|---|
| `tests/Unit/CheckoutActionTest.php` | 12.1 | Listede yoktu |
| `tests/Feature/PaymentNotificationAmountTest.php` | 12.4 | Listede yoktu |
| `Shopier/ShopierConfirmation.php`, `Shopier/ShopierCallback.php` | 12.6 | Listede yoktu |
| Test kılavuzları (`docs/rehber/tests/...`) | ilgili adım | — |
| `scripts/verify-payment.ts` | 12.11 | 12.10 ve 12.11'in kodunu birlikte sınıyor; tek adımda |
| `src/utils/paymentReturn.ts` | 12.13 | Yoklama sabitleri orada |
| `FAZ-12.md` iki kez düzenlendi | 12.9 | 11.6 düzeltmesi; ikisi de 12.9 commit'inde |
| `PaywallTest.php`, `GiftCodeCheckoutTest.php` | 12.2 | Yalnızca yardımcılar (`parseNotification` imzası, `FakeGateway::SIGNATURE_HEADER`). **Hiçbir iddia değişmedi** |

## 5. Sana kalanlar

**`.env` (değersiz):**

```dotenv
PAYMENT_PROVIDER=shopier
SHOPIER_API_KEY=
SHOPIER_API_SECRET=
SHOPIER_WEBSITE_INDEX=1
SHOPIER_CONFIRMATION=osb
SHOPIER_OSB_USERNAME=
SHOPIER_OSB_KEY=
PAYMENT_SUCCESS_URL=https://davetkart.com/odeme/basarili   # MUTLAK adres
PAYMENT_FAILURE_URL=https://davetkart.com/odeme/hata
```

**Panel:** callback → `https://api.davetkart.com/api/public/payments/shopier/callback` · OSB → `https://api.davetkart.com/api/public/payments/shopier/osb`

**Betik:** `docs/rehber/fazlar/FAZ-12-ELLE-DOGRULAMA.md` (9 adım, canlı, gerçek kart)

**Açık 🔴'ler:**
1. §A'nın sekiz satırı → K94.
2. OSB → sipariş eşlemesi bir tahmin (`matchOsbToOrder`): OSB bizim `platform_order_id`'mizi taşımıyorsa hiçbir sipariş ödenmez. Elle doğrulama adım 7.
3. OSB yanıt gövdesi (`success`) ve alan adları resmi dokümanla doğrulanmadı.
4. Yer tutucu TCKN (`11111111110`) Shopier'de reddedilebilir.
5. Shopier iadesi bize bildirilmiyor olabilir → `orders:refund` ihtiyacı.
6. K67 ("ödeme yayınlamaz") ile frontend 11.6'nın otomatik yayını: metin güncellensin mi?
7. Kullanılmayan eski kart arayüzü (`CardPreview`, `CardBrandMark`, `utils/paymentCard.ts`) silinsin mi?

**Temizlik:** backend deposunun `.git\_claude_tmp\` klasörü benim geçici dosyalarım (bundle, patch). Silme iznim olmadığı için kaldıramadım; elle silebilirsin. Çalışma ağacına etkisi yok.
