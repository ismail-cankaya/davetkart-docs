# Faz 18.3 — `SEC-01` commit komutları

> **Tarih:** 16 Kasım 2026 · **Kararlar:** K158–K163 · **Faz kaydı:** backend `docs/rehber/fazlar/FAZ-18.md` §18.3
> Her blok bir commit. Dosyalar tek tek, açık yolla eklenir; joker, klasör yolu ve `-A` yok.
> Her blok `git status --short` ile biter. Sıra: backend → frontend → docs → birleştirme.
> ⚠️ Bu bulguda **frontend de değişti** (plandan sapma, K163): ödeme sayfası fiyatı kendi hedefi için soruyor.

## Başlamadan: çalışma ağaçlarında ne olmalı

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-sec-01-first-publish-once
git status --short --untracked-files=all
```

Beklenen (41 satır, başka bir şey yok):

```
 M app/Actions/GiftCode/PreviewGiftCodeAction.php
 M app/Actions/Payment/HandlePaymentCallbackAction.php
 M app/Actions/Payment/StartCheckoutAction.php
 M app/Actions/Pricing/QuotePriceAction.php
 M app/Actions/Pricing/ShowPricingAction.php
 M app/Http/Controllers/Api/V1/GiftCodeController.php
 M app/Http/Controllers/Api/V1/PricingController.php
 M app/Http/Requests/GiftCode/PreviewGiftCodeRequest.php
 M app/Models/Order.php
 M database/factories/OrderFactory.php
 M docs/rehber/app/Actions/GiftCode/PreviewGiftCodeAction.md
 M docs/rehber/app/Actions/Payment/HandlePaymentCallbackAction.md
 M docs/rehber/app/Actions/Payment/StartCheckoutAction.md
 M docs/rehber/app/Actions/Pricing/QuotePriceAction.md
 M docs/rehber/app/Actions/Pricing/ShowPricingAction.md
 M docs/rehber/app/Http/Controllers/Api/V1/GiftCodeController.md
 M docs/rehber/app/Http/Controllers/Api/V1/PricingController.md
 M docs/rehber/app/Http/Requests/GiftCode/PreviewGiftCodeRequest.md
 M docs/rehber/app/Models/Order.md
 M docs/rehber/database/factories/OrderFactory.md
 M docs/rehber/fazlar/FAZ-13.md
 M docs/rehber/fazlar/FAZ-18.md
 M docs/rehber/fazlar/README.md
 M docs/rehber/tests/Feature/FirstPublishCheckoutTest.md
 M docs/rehber/tests/Feature/GiftCodeCheckoutTest.md
 M docs/rehber/tests/Feature/GiftCodePreviewTest.md
 M docs/rehber/tests/Feature/PricingTest.md
 M tests/Feature/FirstPublishCheckoutTest.php
 M tests/Feature/GiftCodeCheckoutTest.php
 M tests/Feature/GiftCodePreviewTest.php
 M tests/Feature/PricingTest.php
 M tests/Feature/QuotePriceActionTest.php
?? app/Http/Requests/Pricing/ShowPricingRequest.php
?? app/Services/Pricing/FirstPublishEligibility.php
?? database/migrations/2026_11_16_100000_add_one_pending_first_publish_index_to_orders.php
?? docs/rehber/app/Http/Requests/Pricing/ShowPricingRequest.md
?? docs/rehber/app/Services/Pricing/FirstPublishEligibility.md
?? docs/rehber/database/migrations/2026_11_16_100000_add_one_pending_first_publish_index_to_orders.md
?? tests/Feature/FirstPublishEligibilityTest.php
?? tests/Feature/FirstPublishFinalGateTest.php
?? tests/Feature/OrderFirstPublishIndexTest.php
```

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git switch fix/2026-11-16-sec-01-first-publish-once
git status --short --untracked-files=all
```

Beklenen (17 satır; ayrıca `?? .claude/` görünebilir, eklenmez):

```
 M docs/rehber/scripts/verify-pricing.md
 M docs/rehber/src/components/payment/checkout/GiftCodeField.md
 M docs/rehber/src/pages/CheckoutPage.md
 M docs/rehber/src/services/payments.md
 M docs/rehber/src/services/pricing.md
 M docs/rehber/src/stores/useCheckoutStore.md
 M docs/rehber/src/stores/usePricingStore.md
 M scripts/verify-endpoints.ts
 M scripts/verify-pricing.ts
 M src/components/payment/checkout/FreeActivationPanel.tsx
 M src/components/payment/checkout/GiftCodeField.tsx
 M src/hooks/usePricing.ts
 M src/pages/CheckoutPage.tsx
 M src/services/payments.ts
 M src/services/pricing.ts
 M src/stores/useCheckoutStore.ts
 M src/stores/usePricingStore.ts
```

## 1. Backend

⚠️ 18.3.1 ve 18.3.2 tek başlarına **bir testi kırmızı bırakır**
(`FirstPublishCheckoutTest::an_abandoned_checkout_keeps_the_discount_for_the_next_try`): index
vardır ama onu gözeten checkout 18.3.3'te gelir. Dal, 18.3.3'ten itibaren yeşildir; arada
`composer check` koşma.

```powershell
# 18.3.1 — kısmi UNIQUE index (K158, K162), fabrikanın firstPublish() durumu, index testi
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-sec-01-first-publish-once
git add database/migrations/2026_11_16_100000_add_one_pending_first_publish_index_to_orders.php
git add docs/rehber/database/migrations/2026_11_16_100000_add_one_pending_first_publish_index_to_orders.md
git add database/factories/OrderFactory.php
git add docs/rehber/database/factories/OrderFactory.md
git add tests/Feature/OrderFirstPublishIndexTest.php
git commit -m "18.3.1 - feat(orders): Add partial unique index for one pending first-publish order per user"
git status --short
```

```powershell
# 18.3.2 — uygunluk tek yerde (K159); fiyat bir hedef için sorulur (K163)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-sec-01-first-publish-once
git add app/Services/Pricing/FirstPublishEligibility.php
git add docs/rehber/app/Services/Pricing/FirstPublishEligibility.md
git add app/Models/Order.php
git add docs/rehber/app/Models/Order.md
git add app/Actions/Pricing/QuotePriceAction.php
git add docs/rehber/app/Actions/Pricing/QuotePriceAction.md
git add app/Actions/Pricing/ShowPricingAction.php
git add docs/rehber/app/Actions/Pricing/ShowPricingAction.md
git add app/Http/Requests/Pricing/ShowPricingRequest.php
git add docs/rehber/app/Http/Requests/Pricing/ShowPricingRequest.md
git add app/Http/Controllers/Api/V1/PricingController.php
git add docs/rehber/app/Http/Controllers/Api/V1/PricingController.md
git add app/Http/Requests/GiftCode/PreviewGiftCodeRequest.php
git add docs/rehber/app/Http/Requests/GiftCode/PreviewGiftCodeRequest.md
git add app/Http/Controllers/Api/V1/GiftCodeController.php
git add docs/rehber/app/Http/Controllers/Api/V1/GiftCodeController.md
git add app/Actions/GiftCode/PreviewGiftCodeAction.php
git add docs/rehber/app/Actions/GiftCode/PreviewGiftCodeAction.md
git add tests/Feature/FirstPublishEligibilityTest.php
git add tests/Feature/QuotePriceActionTest.php
git add tests/Feature/PricingTest.php
git add docs/rehber/tests/Feature/PricingTest.md
git add tests/Feature/GiftCodePreviewTest.php
git add docs/rehber/tests/Feature/GiftCodePreviewTest.md
git commit -m "18.3.2 - feat(pricing): Decide first-publish eligibility in one place and price a target"
git status --short
```

```powershell
# 18.3.3 — checkout: kullanıcı kilidi (K158), yeniden kullanma (K160), eskiyi kapatma (K161)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-sec-01-first-publish-once
git add app/Actions/Payment/StartCheckoutAction.php
git add docs/rehber/app/Actions/Payment/StartCheckoutAction.md
git add tests/Feature/FirstPublishCheckoutTest.php
git add docs/rehber/tests/Feature/FirstPublishCheckoutTest.md
git add tests/Feature/GiftCodeCheckoutTest.php
git add docs/rehber/tests/Feature/GiftCodeCheckoutTest.md
git commit -m "18.3.3 - fix(checkout): Lock the user row, reuse the pending order and close superseded ones"
git status --short
```

```powershell
# 18.3.4 — ödeme bildirimi: son kapı (K158, 3. katman)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-sec-01-first-publish-once
git add app/Actions/Payment/HandlePaymentCallbackAction.php
git add docs/rehber/app/Actions/Payment/HandlePaymentCallbackAction.md
git add tests/Feature/FirstPublishFinalGateTest.php
git commit -m "18.3.4 - feat(payments): Log a critical event when the first-publish discount is paid twice"
git status --short
```

```powershell
# 18.3.5 — faz kaydı; K131'in durum notu
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-sec-01-first-publish-once
git add docs/rehber/fazlar/FAZ-18.md
git add docs/rehber/fazlar/README.md
git add docs/rehber/fazlar/FAZ-13.md
git commit -m "18.3.5 - docs(phases): Record Phase 18.3 (SEC-01 first-publish discount granted once)"
git status --short                                   # boş olmalı
```

## 2. Frontend

🔴 `git add -A` yok (CRLF tuzağı). `.claude/` eklenmez.

```powershell
# 18.3.6 — ödeme sayfası fiyatı ve kod önizlemesini kendi hedefi için sorar (backend K159, K163)
cd D:\Projects\davetkart\davetkart-frontent
git switch fix/2026-11-16-sec-01-first-publish-once
git add src/services/pricing.ts
git add docs/rehber/src/services/pricing.md
git add src/stores/usePricingStore.ts
git add docs/rehber/src/stores/usePricingStore.md
git add src/hooks/usePricing.ts
git add src/services/payments.ts
git add docs/rehber/src/services/payments.md
git add src/stores/useCheckoutStore.ts
git add docs/rehber/src/stores/useCheckoutStore.md
git add src/components/payment/checkout/GiftCodeField.tsx
git add src/components/payment/checkout/FreeActivationPanel.tsx
git add docs/rehber/src/components/payment/checkout/GiftCodeField.md
git add src/pages/CheckoutPage.tsx
git add docs/rehber/src/pages/CheckoutPage.md
git add scripts/verify-pricing.ts
git add docs/rehber/scripts/verify-pricing.md
git add scripts/verify-endpoints.ts
git commit -m "18.3.6 - feat(checkout): Ask the price and gift code preview for the checkout target"
git status --short                                   # boş ya da yalnızca '?? .claude/'
```

## 3. Docs

```powershell
# 18.3.7 — kararlar, takip tablosu, bu dosya
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-16-faz-18-audit-fixes
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md
git add decisions/DECISION-INDEX.md
git add phases/faz-18/README.md
git add phases/faz-18/FAZ-18-SEC-01-COMMIT-KOMUTLARI.md
git add CHANGELOG.md
git commit -m "docs(decisions): Add K158-K163 and commit commands for SEC-01"
git status --short                                   # boş olmalı
# git push -u origin docs/2026-11-16-faz-18-audit-fixes
```

## 4. Birleştirme (backend ve frontend)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-16-sec-01-first-publish-once -m "Merge SEC-01 fix into faz-18-audit-fixes"
git status --short
# git push -u origin faz-18-audit-fixes
# git push -u origin fix/2026-11-16-sec-01-first-publish-once
```

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-16-sec-01-first-publish-once -m "Merge SEC-01 fix into faz-18-audit-fixes"
git status --short
# git push -u origin faz-18-audit-fixes
# git push -u origin fix/2026-11-16-sec-01-first-publish-once
```

🔴 Birleştirmeyi atlama: sonraki prompt (18.4, `SEC-02`) önceki bulgunun birleşmiş olmasını denetler.

Bitince `phases/faz-18/README.md`'de `SEC-01` satırını `birleşti` yap.

## 5. Commit'ten sonra: elle işler

1. **Yerel göç** (backend, birleştirmeden sonra): `php artisan migrate`. 16 Kasım'da yerel `davetkart`
   veritabanında çakışan satır yoktu; göç durursa mesajdaki kılavuzun §4'üne bak
   (`docs/rehber/database/migrations/2026_11_16_100000_add_one_pending_first_publish_index_to_orders.md`).
2. **Elle deneme** (yerel, `PAYMENT_DRIVER=fake`, yeni bir kullanıcı, iki davetiye): frontend
   `docs/rehber/src/pages/CheckoutPage.md` §Faz 18.3 "Elle deneme" (dört adım).
3. **Yayında** (`v1.1.0`, sıra K148): önce backend (göç `deploy.sh` ile koşar), sonra frontend. Arada
   kalan pencerede eski frontend fiyatı hedefsiz sorar: ödeme sayfasına geri dönen kullanıcı liste
   fiyatı görür ama indirimli siparişi öder (lehine). Kayıt açılmadan önce ikisi birlikte çıkmalı.
4. **Log'u izle:** `First publish discount paid on more than one order` (`critical`). Çıkarsa karar
   senin: farkı tahsil et ya da siparişi iade et. Alarm bağlantısı `OPS-03`.

## 6. Bayat kilit dosyası (frontend, bu işle ilgisiz)

`davetkart-frontent/.git/packed-refs.lock` 4 Kasım 2026'dan kalma (0 bayt). Dal açarken
`Unable to create '…/packed-refs.lock': File exists` uyarısı verdi; dal yine de açıldı. Başka bir
git işlemi çalışmıyorken silinebilir:

```powershell
Remove-Item D:\Projects\davetkart\davetkart-frontent\.git\packed-refs.lock
```
