# Faz 11 — frontend commit komutları

> 🔴 `git add -A` YASAK (CRLF). Dosyalar tek tek. Dal: `faz-11-hediye-kodu` (`main`'den). Her commit tek başına `npm run check`'ten geçti (bulut çalışma alanında).
> Not: 11.15'teki bileşenler `giftCode.*` çeviri anahtarlarını kullanır, anahtarlar 11.16'da gelir. Arada derleme yeşil; yalnızca ekranda anahtar adı görünür.

## 11.12

```powershell
# 11.12 — Add the gift code error codes and messages
cd D:\Projects\davetkart\davetkart-frontent
git add src/contracts/error-codes.json src/contracts/errorCodes.ts src/locales/tr/errors.json
git add src/locales/en/errors.json src/utils/toDisplayError.ts scripts/verify-error-contract.ts
git add docs/rehber/src/utils/toDisplayError.md
git commit -m "11.1 - feat(gift-codes): Add the gift code error codes and messages"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.13

```powershell
# 11.13 — Preview gift codes and send them at checkout
cd D:\Projects\davetkart\davetkart-frontent
git add src/types.ts src/services/payments.ts src/utils/currency.ts
git add scripts/verify-endpoints.ts scripts/verify-payment.ts docs/rehber/src/services/payments.md
git add docs/rehber/src/types.md docs/rehber/src/utils/currency.md
git commit -m "11.2 - feat(gift-codes): Preview gift codes and send them at checkout"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.14

```powershell
# 11.14 — Keep the applied gift code in the checkout store
cd D:\Projects\davetkart\davetkart-frontent
git add src/stores/useCheckoutStore.ts scripts/verify-gift-code.ts package.json
git add docs/rehber/src/stores/useCheckoutStore.md docs/rehber/scripts/verify-gift-code.md
git commit -m "11.3 - feat(gift-codes): Keep the applied gift code in the checkout store"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.15

```powershell
# 11.15 — Add the gift code field and free activation to checkout
cd D:\Projects\davetkart\davetkart-frontent
git add src/components/payment/checkout/GiftCodeField.tsx src/components/payment/checkout/FreeActivationPanel.tsx src/components/payment/checkout/OrderSummary.tsx
git add src/components/payment/checkout/CardPaymentForm.tsx src/components/payment/checkout/PaymentMethodSelector.tsx src/pages/CheckoutPage.tsx
git add docs/rehber/src/components/payment/checkout/GiftCodeField.md docs/rehber/src/pages/CheckoutPage.md
git commit -m "11.4 - feat(gift-codes): Add the gift code field and free activation to checkout"
git status --short    # bu adımın dosyası kalmamalı
```

## 11.16

```powershell
# 11.16 — Translate the gift code texts into ten languages
cd D:\Projects\davetkart\davetkart-frontent
git add src/locales/tr/translation.json src/locales/en/translation.json src/locales/es/translation.json
git add src/locales/fr/translation.json src/locales/de/translation.json src/locales/zh/translation.json
git add src/locales/hi/translation.json src/locales/ar/translation.json src/locales/ru/translation.json
git add src/locales/pt/translation.json
git commit -m "11.5 - feat(gift-codes): Translate the gift code texts into ten languages"
git status --short    # bu adımın dosyası kalmamalı
```

## Push

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git push -u origin faz-11-hediye-kodu
```
