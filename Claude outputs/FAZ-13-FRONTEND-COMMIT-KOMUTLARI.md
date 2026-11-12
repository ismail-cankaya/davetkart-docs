# Faz 13 — commit komutları (frontend)

> 🔴 Frontend'de `git add -A` YASAK (CRLF): dosyalar tek tek eklenir, aşağıdaki gibi.
> Dal: `faz-13-payment-settings`. Her commit tek başına `tsc` geçti; son commit'te `npm run check` yeşil (tsc + build + 11 doğrulama).
> Önce backend commit'lerini at: 13.9'daki hediye kodu önizlemesi backend 13.5'in yanıtını bekliyor.

## 13.9

```powershell
# 13.9 — Fiyat kataloğu servisi, store ve tipler
cd D:\Projects\davetkart\davetkart-frontent
# 🔴 Bu dosya sonraki adımda tekrar değişiyor: önce bu adımın ARA sürümü yerine konur, commit sonrası son hâli geri gelir.
Copy-Item -Force "..\Claude outputs\f13-ara\13.9\types.ts" src\types.ts
git add docs/rehber/src/components/payment/checkout/GiftCodeField.md docs/rehber/src/services/payments.md docs/rehber/src/services/pricing.md docs/rehber/src/stores/usePricingStore.md docs/rehber/src/types.md scripts/verify-endpoints.ts
git add scripts/verify-gift-code.ts src/components/payment/checkout/GiftCodeField.tsx src/contracts/error-codes.json src/hooks/usePricing.ts src/locales/en/errors.json src/locales/tr/errors.json src/services/payments.ts
git add src/services/pricing.ts src/stores/usePricingStore.ts src/types.ts src/utils/paymentMethods.ts
git commit -m "13.1 - feat(pricing): Read the price catalogue from the backend"
Copy-Item -Force "..\Claude outputs\f13-ara\son\types.ts" src\types.ts    # son hâli geri
git status --short    # bu adımın dosyası kalmamalı (types.ts "M" görünür: 13.11 adımının)
```

## 13.10

```powershell
# 13.10 — Fiyat metinleri, 10 dil
cd D:\Projects\davetkart\davetkart-frontent
git add src/locales/ar/translation.json src/locales/de/translation.json src/locales/en/translation.json src/locales/es/translation.json src/locales/fr/translation.json src/locales/hi/translation.json src/locales/pt/translation.json
git add src/locales/ru/translation.json src/locales/tr/translation.json src/locales/zh/translation.json
git commit -m "13.2 - feat(i18n): Translate the pricing texts into ten languages"
git status --short    # bu adımın dosyası kalmamalı
```

## 13.11

```powershell
# 13.11 — data.ts'ten fiyat silindi; paywall ve ödeme sayfası API'den
cd D:\Projects\davetkart\davetkart-frontent
git add .env.example docs/rehber/src/components/payment/PlanPriceTag.md docs/rehber/src/data.md docs/rehber/src/pages/CheckoutPage.md docs/rehber/src/stores/useCheckoutStore.md scripts/verify-payment.ts
git add src/components/payment/PaywallModal.tsx src/components/payment/PlanPriceTag.tsx src/components/payment/checkout/OrderSummary.tsx src/components/payment/checkout/PaymentMethodSelector.tsx src/data.ts src/pages/CheckoutPage.tsx
git add src/pages/PaymentReturnPage.tsx src/services/bankTransfer.ts src/stores/useCheckoutStore.ts src/types.ts src/vite-env.d.ts
git commit -m "13.3 - feat(pricing): Show backend prices in the paywall and checkout"
git status --short    # bu adımın dosyası kalmamalı
```

## 13.12

```powershell
# 13.12 — Fiyat sayfası gerçek üç pakete bağlandı
cd D:\Projects\davetkart\davetkart-frontent
git add docs/rehber/src/pages/PricingPage.md src/components/home/Features.tsx src/pages/HomePage.tsx src/pages/PricingPage.tsx src/pages/RegisterPage.tsx
git commit -m "13.4 - feat(pricing): Rebuild the pricing page on the real plans"
git status --short    # bu adımın dosyası kalmamalı
```

## 13.13

```powershell
# 13.13 — verify:pricing
cd D:\Projects\davetkart\davetkart-frontent
git add docs/rehber/scripts/verify-pricing.md package.json scripts/verify-pricing.ts
git commit -m "13.5 - test(pricing): Verify that no price is hard-coded in the frontend"
git status --short    # bu adımın dosyası kalmamalı
```

## Son

```powershell
cd D:\Projects\davetkart\davetkart-frontent
npm run check
```

Yerel `.env` dosyandaki `VITE_BANK_TRANSFER_*` satırları artık okunmuyor; silebilirsin. Havale hesabı backend `.env`'ine taşındı (`BANK_TRANSFER_*`).

