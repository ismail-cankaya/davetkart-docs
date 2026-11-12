# Faz 11 — commit komutları (backend + claude)
> Her blok bir commit. Dosyalar tek tek, açık yolla. Blokları **sırayla** çalıştır; her bloğun sonundaki `git status --short` o adımın dosyalarını artık göstermemeli.
> Not: 11.3 ve 11.4 prompttaki sıranın tersine: 11.3 = `GiftCodeFormat`, 11.4 = modeller (fabrika `GiftCodeFormat`'a bağlı). Her commit tek başına derlendi ve testleri geçti (bulut çalışma alanında, adım adım).

## 11.1

```powershell
# 11.1 — Add the gift code benefit enum and table
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Enums/GiftCodeBenefit.php database/migrations/2026_10_23_100000_create_gift_codes_table.php docs/rehber/app/Enums/GiftCodeBenefit.md docs/rehber/database/migrations/2026_10_23_100000_create_gift_codes_table.md
git commit -m "11.1 - feat(gift-codes): Add the gift code benefit enum and table"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.2

```powershell
# 11.2 — Add the redemptions table and the gift order rules
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add database/migrations/2026_10_23_100100_create_gift_code_redemptions_table.php database/migrations/2026_10_23_100200_add_discount_and_gift_rules_to_orders.php docs/rehber/database/migrations/2026_10_23_100100_create_gift_code_redemptions_table.md docs/rehber/database/migrations/2026_10_23_100200_add_discount_and_gift_rules_to_orders.md
git commit -m "11.2 - feat(gift-codes): Add the redemptions table and the gift order rules"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.3

```powershell
# 11.3 — Normalize, hash and generate gift codes
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Support/GiftCodes/GiftCodeFormat.php tests/Unit/GiftCodeFormatTest.php docs/rehber/app/Support/GiftCodes/GiftCodeFormat.md
git commit -m "11.3 - feat(gift-codes): Normalize, hash and generate gift codes"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.4

```powershell
# 11.4 — Add the gift code models and factories
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Models/GiftCode.php app/Models/GiftCodeRedemption.php database/factories/GiftCodeFactory.php database/factories/GiftCodeRedemptionFactory.php
git add app/Models/Order.php tests/Feature/GiftCodeModelTest.php docs/rehber/app/Models/GiftCode.md docs/rehber/app/Models/GiftCodeRedemption.md
git add docs/rehber/database/factories/GiftCodeFactory.md docs/rehber/app/Models/Order.md
git commit -m "11.4 - feat(gift-codes): Add the gift code models and factories"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.5

```powershell
# 11.5 — Add the gift code error codes
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Enums/ErrorCode.php app/Exceptions/GiftCodeException.php docs/08-HATA-SOZLESMESI.md contracts/error-codes.json
git add docs/rehber/app/Enums/ErrorCode.md docs/rehber/app/Exceptions/GiftCodeException.md
git commit -m "11.5 - feat(gift-codes): Add the gift code error codes"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.6

```powershell
# 11.6 — Reserve a gift code under a row lock
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Actions/GiftCode/ReserveGiftCodeAction.php app/Actions/GiftCode/QuoteGiftCodeAction.php app/Actions/GiftCode/GiftCodeQuote.php docs/rehber/app/Actions/GiftCode/ReserveGiftCodeAction.md
git commit -m "11.6 - feat(gift-codes): Reserve a gift code under a row lock"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.7

```powershell
# 11.7 — Apply gift codes at checkout
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Actions/Payment/StartCheckoutAction.php app/Http/Requests/Payment/StoreCheckoutRequest.php app/Http/Controllers/Api/V1/PaymentController.php app/Http/Resources/OrderResource.php
git add tests/Feature/GiftCodeCheckoutTest.php docs/rehber/app/Actions/Payment/StartCheckoutAction.md docs/rehber/app/Http/Requests/Payment/StoreCheckoutRequest.md docs/rehber/app/Http/Controllers/Api/V1/PaymentController.md
git add docs/rehber/app/Http/Resources/OrderResource.md docs/rehber/tests/Feature/GiftCodeCheckoutTest.md
git commit -m "11.7 - feat(gift-codes): Apply gift codes at checkout"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.8

```powershell
# 11.8 — Preview gift codes and rate limit guesses
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Actions/GiftCode/PreviewGiftCodeAction.php app/Http/Requests/GiftCode/PreviewGiftCodeRequest.php app/Http/Controllers/Api/V1/GiftCodeController.php app/Http/Resources/GiftCodeQuoteResource.php
git add routes/api.php app/Providers/AppServiceProvider.php config/davetkart.php tests/Feature/GiftCodePreviewTest.php
git add docs/rehber/app/Actions/GiftCode/PreviewGiftCodeAction.md docs/rehber/app/Http/Requests/GiftCode/PreviewGiftCodeRequest.md docs/rehber/app/Http/Controllers/Api/V1/GiftCodeController.md docs/rehber/app/Http/Resources/GiftCodeQuoteResource.md
git add docs/rehber/app/Providers/AppServiceProvider.md docs/rehber/config/davetkart.md docs/rehber/routes/api.md docs/rehber/tests/Feature/GiftCodePreviewTest.md
git commit -m "11.8 - feat(gift-codes): Preview gift codes and rate limit guesses"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.9

```powershell
# 11.9 — Add the create and generate commands
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Actions/GiftCode/GiftCodeSpec.php app/Actions/GiftCode/CreateGiftCodeAction.php app/Actions/GiftCode/GenerateGiftCodeBatchAction.php app/Console/Commands/CreateGiftCode.php
git add app/Console/Commands/GenerateGiftCodes.php tests/Feature/GiftCodeCreateCommandsTest.php docs/rehber/app/Actions/GiftCode/GiftCodeSpec.md docs/rehber/app/Actions/GiftCode/CreateGiftCodeAction.md
git add docs/rehber/app/Actions/GiftCode/GenerateGiftCodeBatchAction.md docs/rehber/app/Console/Commands/CreateGiftCode.md docs/rehber/app/Console/Commands/GenerateGiftCodes.md
git commit -m "11.9 - feat(gift-codes): Add the create and generate commands"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.10

```powershell
# 11.10 — Add the list and disable commands
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add app/Console/Commands/ListGiftCodes.php app/Console/Commands/DisableGiftCode.php app/Actions/GiftCode/DisableGiftCodeAction.php tests/Feature/GiftCodeAdminCommandsTest.php
git add docs/rehber/app/Console/Commands/ListGiftCodes.md docs/rehber/app/Console/Commands/DisableGiftCode.md docs/rehber/app/Actions/GiftCode/DisableGiftCodeAction.md
git commit -m "11.10 - feat(gift-codes): Add the list and disable commands"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.11

```powershell
# 11.11 — Record Phase 11 and its manual verification script
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add docs/rehber/fazlar/FAZ-11.md docs/rehber/fazlar/FAZ-11-ELLE-DOGRULAMA.md docs/rehber/fazlar/README.md README.md
git commit -m "11.11 - docs(gift-codes): Record Phase 11 and its manual verification script"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.17 — claude deposu (YALNIZCA EK dosyası)

🔴 Önce `PHP-LARAVEL-SETUP.md`'deki **kendi** commit'lenmemiş değişikliğini commit'le (senin kararın). Ana dosyaya Faz 11 kayıtları bu oturumda **işlenmedi**; EK dosyası "işlenmeyi bekleyen yama" biçiminde (EK-FAZ-5…9 gibi).

```powershell
# 11.17 — Phase 11 context patch
cd D:\Projects\davetkart\claude
git status --short    # yalnızca PHP-LARAVEL-SETUP.md (senin) + EK-FAZ-11.md görünmeli
git add PHP-LARAVEL-SETUP-EK-FAZ-11.md
git commit -m "11.17 - docs: Record the Phase 11 context patch (gift codes)"
git status --short
```

## Push (ayrı blok)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git push -u origin faz-11-hediye-kodu

cd D:\Projects\davetkart\claude
git push -u origin main
```

> Frontend dalı açılmadı (frontend sonraki adıma kaldı); frontend push'u yok.
