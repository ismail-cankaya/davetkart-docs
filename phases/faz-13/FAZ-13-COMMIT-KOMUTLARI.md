# Faz 13 — commit komutları (backend)

> Her blok bir commit. Dosyalar tek tek, açık yolla. Blokları **sırayla** çalıştır; her bloğun sonundaki `git status --short` o adımın dosyalarını artık göstermemeli.
> Dal: `faz-13-payment-settings` (zaten bu daldasın). Her commit tek başına derlendi ve testleri geçti (bulut çalışma alanında, PHP 8.5 + PostgreSQL 16, adım adım). Son commit'te: 865 test, PHPStan 0 hata, Pint temiz.
> Dosyaların hepsi şu an çalışma ağacında; commit'ler yalnızca onları adımlara bölüyor.

## 13.1

```powershell
# 13.1 — Ödeme yöntemi anahtarı ve havale hesabı backend'e
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add .env.example app/Enums/ErrorCode.php app/Enums/PaymentMethod.php app/Exceptions/PaymentMethodException.php app/Services/Payment/BankTransferAccount.php app/Services/Payment/PaymentMethods.php config/davetkart.php
git add config/payment.php contracts/error-codes.json docs/08-HATA-SOZLESMESI.md docs/10-URETIM-ENV-SABLONU.md docs/rehber/app/Enums/ErrorCode.md docs/rehber/app/Enums/PaymentMethod.md docs/rehber/app/Exceptions/PaymentMethodException.md
git add docs/rehber/app/Services/Payment/PaymentMethods.md docs/rehber/config/davetkart.md docs/rehber/config/payment.md docs/rehber/tests/Feature/PaymentMethodsTest.md phpunit.xml tests/Feature/PaymentMethodsTest.php
git commit -m "13.1 - feat(payment): Add the payment method switch and move the bank account to the backend"
git status --short    # bu adımın dosyası kalmamalı
```

## 13.2

```powershell
# 13.2 — Kampanya tablosu ve siparişe otomatik indirim kolonları
cd D:\Projects\davetkart\davetkart-backend-php-laravel
# 🔴 Bu dosya sonraki adımda tekrar değişiyor: önce bu adımın ARA sürümü yerine konur, commit sonrası son hâli geri gelir.
Copy-Item -Force "..\Claude outputs\f13-ara\13.2\Order.php" app\Models\Order.php
git add app/Enums/PromotionKind.php app/Models/Order.php database/migrations/2026_10_25_100000_create_price_campaigns_table.php database/migrations/2026_10_25_100100_add_promotion_to_orders.php docs/rehber/app/Enums/PromotionKind.md
git add docs/rehber/app/Models/Order.md docs/rehber/database/migrations/2026_10_25_100000_create_price_campaigns_table.md docs/rehber/database/migrations/2026_10_25_100100_add_promotion_to_orders.md
git add docs/rehber/tests/Feature/OrderPromotionConstraintsTest.md tests/Feature/OrderPromotionConstraintsTest.php
git commit -m "13.2 - feat(pricing): Add the price campaign table and the order promotion columns"
Copy-Item -Force "..\Claude outputs\f13-ara\son\Order.php" app\Models\Order.php    # son hâli geri
git status --short    # bu adımın dosyası kalmamalı (Order.php "M" görünür: 13.3 adımının)
```

## 13.3

```powershell
# 13.3 — pricing:campaign:start / list / stop
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Actions/Pricing/PriceCampaignSpec.php app/Actions/Pricing/StartPriceCampaignAction.php app/Actions/Pricing/StopPriceCampaignAction.php app/Console/Commands/ListPriceCampaigns.php app/Console/Commands/StartPriceCampaign.php
git add app/Console/Commands/StopPriceCampaign.php app/Models/Order.php app/Models/PriceCampaign.php database/factories/PriceCampaignFactory.php docs/rehber/app/Actions/Pricing/StartPriceCampaignAction.md
git add docs/rehber/app/Console/Commands/PriceCampaignCommands.md docs/rehber/app/Models/PriceCampaign.md docs/rehber/tests/Feature/PriceCampaignCommandsTest.md tests/Feature/PriceCampaignCommandsTest.php
git commit -m "13.3 - feat(pricing): Start, list and stop price campaigns from the console"
git status --short    # bu adımın dosyası kalmamalı
```

## 13.4

```powershell
# 13.4 — Fiyatın tek hesabı: QuotePriceAction
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Actions/GiftCode/QuoteGiftCodeAction.php app/Actions/GiftCode/ReserveGiftCodeAction.php app/Actions/Pricing/PriceQuote.php app/Actions/Pricing/Promotion.php app/Actions/Pricing/QuotePriceAction.php app/Models/GiftCode.php
git add docs/rehber/app/Actions/GiftCode/ReserveGiftCodeAction.md docs/rehber/app/Actions/Pricing/QuotePriceAction.md docs/rehber/app/Models/GiftCode.md docs/rehber/tests/Feature/QuotePriceActionTest.md
git add tests/Feature/QuotePriceActionTest.php
git commit -m "13.4 - feat(pricing): Quote prices with the first-publish discount and campaigns"
git status --short    # bu adımın dosyası kalmamalı
```

## 13.5

```powershell
# 13.5 — Checkout yeni fiyatla; kapalı yöntem 403
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Actions/GiftCode/PreviewGiftCodeAction.php app/Actions/Payment/StartCheckoutAction.php app/Http/Resources/GiftCodeQuoteResource.php app/Http/Resources/PriceQuoteResource.php app/Services/Payment/PaymentGatewayResolver.php
git add docs/rehber/app/Actions/GiftCode/PreviewGiftCodeAction.md docs/rehber/app/Actions/Payment/StartCheckoutAction.md docs/rehber/app/Http/Resources/GiftCodeQuoteResource.md docs/rehber/app/Http/Resources/PriceQuoteResource.md
git add docs/rehber/app/Services/Payment/PaymentGatewayResolver.md docs/rehber/tests/Feature/FirstPublishCheckoutTest.md docs/rehber/tests/Feature/PaymentMethodGateTest.md docs/rehber/tests/TestCase.md
git add tests/Feature/FirstPublishCheckoutTest.php tests/Feature/GiftCodePreviewTest.php tests/Feature/PaymentMethodGateTest.php tests/TestCase.php
git commit -m "13.5 - feat(payment): Charge the quoted price and refuse closed payment methods"
git status --short    # bu adımın dosyası kalmamalı
```

## 13.6

```powershell
# 13.6 — GET /api/public/plans ve GET /api/pricing
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Actions/Pricing/PricingOverview.php app/Actions/Pricing/ShowPricingAction.php app/Http/Controllers/Api/V1/PricingController.php app/Http/Resources/PricingResource.php docs/rehber/app/Actions/Pricing/ShowPricingAction.md
git add docs/rehber/app/Http/Controllers/Api/V1/PricingController.md docs/rehber/app/Http/Resources/PricingResource.md docs/rehber/routes/api.md docs/rehber/tests/Feature/PricingTest.md routes/api.php tests/Feature/PricingTest.php
git commit -m "13.6 - feat(pricing): Expose the price catalogue to guests and users"
git status --short    # bu adımın dosyası kalmamalı
```

## 13.7

```powershell
# 13.7 — Sipariş yanıtına tutar dökümü
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Http/Resources/OrderResource.php docs/rehber/app/Http/Resources/OrderResource.md tests/Feature/OrderTest.php
git commit -m "13.7 - feat(orders): Return the frozen price breakdown with each order"
git status --short    # bu adımın dosyası kalmamalı
```

## 13.8

```powershell
# 13.8 — Faz özeti, elle doğrulama, işletme kılavuzu
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add docs/rehber/FIYAT-VE-INDIRIM-YONETIMI.md docs/rehber/fazlar/FAZ-13-ELLE-DOGRULAMA.md docs/rehber/fazlar/FAZ-13.md docs/rehber/fazlar/README.md
git commit -m "13.8 - docs(pricing): Record Phase 13 and the pricing operations guide"
git status --short    # bu adımın dosyası kalmamalı
```

## Son

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
php artisan migrate
composer check    # beklenen: 865 test
```

