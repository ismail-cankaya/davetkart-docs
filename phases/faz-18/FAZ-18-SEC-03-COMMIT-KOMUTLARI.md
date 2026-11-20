# Faz 18.5 — `SEC-03` commit komutları

> **Tarih:** 20 Kasım 2026 · **Kararlar:** K170–K172 · **Faz kaydı:** backend `docs/rehber/fazlar/FAZ-18.md` §18.5
> Her blok bir commit. Dosyalar tek tek, açık yolla eklenir; joker, klasör yolu ve `-A` yok.
> Her blok `git status --short` ile biter. Sıra: backend → docs → birleştirme. Frontend değişmedi.
> Backend dalı: `fix/2026-11-20-sec-03-shopier-callback-mode`.

## Başlamadan: çalışma ağaçlarında ne olmalı

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-03-shopier-callback-mode
git status --short --untracked-files=all
```

Beklenen (19 satır, başka bir şey yok):

```
 M app/Actions/Payment/HandlePaymentCallbackAction.php
 M app/Http/Controllers/Api/V1/ShopierCallbackController.php
 M app/Services/Payment/Shopier/ShopierConfirmation.php
 M app/Services/Payment/ShopierGateway.php
 M config/payment.php
 M docs/10-URETIM-ENV-SABLONU.md
 M docs/rehber/app/Actions/Payment/HandlePaymentCallbackAction.md
 M docs/rehber/app/Http/Controllers/Api/V1/ShopierCallbackController.md
 M docs/rehber/app/Services/Payment/ShopierGateway.md
 M docs/rehber/config/payment.md
 M docs/rehber/fazlar/FAZ-12.md
 M docs/rehber/fazlar/FAZ-18.md
 M docs/rehber/fazlar/README.md
 M docs/rehber/tests/Feature/PaymentDriverResolutionTest.md
 M docs/rehber/tests/Feature/PaymentNotificationAmountTest.md
 M docs/rehber/tests/Feature/ShopierCallbackTest.md
 M tests/Feature/PaymentDriverResolutionTest.php
 M tests/Feature/PaymentNotificationAmountTest.php
 M tests/Feature/ShopierCallbackTest.php
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-16-faz-18-audit-fixes
git status --short --untracked-files=all
```

Beklenen (6 satır):

```
 M CHANGELOG.md
 M decisions/DECISION-INDEX.md
 M decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md
 M phases/faz-18/README.md
 M prompts/PROMPT-FAZ-18-3-SEC-01.md
?? phases/faz-18/FAZ-18-SEC-03-COMMIT-KOMUTLARI.md
```

⚠️ `prompts/PROMPT-FAZ-18-3-SEC-01.md` **bu işin parçası değil**: 18.4'te de görülen aynı değişiklik
(`## 10. Rapor` başlığının altına tek boş satır). Docs bloğu onu eklemez. Ne yapacağına sen karar ver:
`git diff prompts/PROMPT-FAZ-18-3-SEC-01.md` ile bak; istemiyorsan
`git restore prompts/PROMPT-FAZ-18-3-SEC-01.md` (bunu ben çalıştırmadım).

## 1. Backend

Her commit tek başına yeşil olmalı. 18.5.2'nin `a_forged_success_in_callback_mode_does_not_pay_in_production`
testi 18.5.1'in kurucu kuralına dayanır; 18.5.3 bağımsız. ⚠️ Ara commit'ler ayrı ayrı **koşulmadı**
(stash/checkout yasaktı); yalnızca son ağaç (`composer check`, 1166 test) koştu.

```powershell
# 18.5.1 — üretimde `callback` kipi sürücüyü kurdurmaz: 503 + critical log (K170)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-03-shopier-callback-mode
git add app/Services/Payment/ShopierGateway.php
git add app/Services/Payment/Shopier/ShopierConfirmation.php
git add docs/rehber/app/Services/Payment/ShopierGateway.md
git add config/payment.php
git add docs/rehber/config/payment.md
git add tests/Feature/PaymentDriverResolutionTest.php
git add docs/rehber/tests/Feature/PaymentDriverResolutionTest.md
git commit -m "18.5.1 - fix(payments): Refuse the Shopier callback confirmation mode in production"
git status --short
```

```powershell
# 18.5.2 — callback ucu: sürücü kurulamazsa 503 JSON değil hata sayfası (K172)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-03-shopier-callback-mode
git add app/Http/Controllers/Api/V1/ShopierCallbackController.php
git add docs/rehber/app/Http/Controllers/Api/V1/ShopierCallbackController.md
git add tests/Feature/ShopierCallbackTest.php
git add docs/rehber/tests/Feature/ShopierCallbackTest.md
git commit -m "18.5.2 - fix(payments): Send the browser to the failure page when the Shopier driver cannot start"
git status --short
```

```powershell
# 18.5.3 — üretimde tutar taşımayan `paid` bildirimi reddedilir (K171)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-03-shopier-callback-mode
git add app/Actions/Payment/HandlePaymentCallbackAction.php
git add docs/rehber/app/Actions/Payment/HandlePaymentCallbackAction.md
git add tests/Feature/PaymentNotificationAmountTest.php
git add docs/rehber/tests/Feature/PaymentNotificationAmountTest.md
git commit -m "18.5.3 - fix(payments): Refuse a paid notification without an amount in production"
git status --short
```

```powershell
# 18.5.4 — üretim .env şablonu (D4), faz kaydı; K94, K117, K122, K126 durum notları
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-03-shopier-callback-mode
git add docs/10-URETIM-ENV-SABLONU.md
git add docs/rehber/fazlar/FAZ-18.md
git add docs/rehber/fazlar/README.md
git add docs/rehber/fazlar/FAZ-12.md
git commit -m "18.5.4 - docs(phases): Record Phase 18.5 (SEC-03 Shopier callback mode refused in production)"
git status --short                                   # boş olmalı
```

## 2. Docs

```powershell
# 18.5.5 — kararlar (K170–K172), indeks (K94, K117, K122, K126 notları), takip tablosu, bu dosya
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-16-faz-18-audit-fixes
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md
git add decisions/DECISION-INDEX.md
git add phases/faz-18/README.md
git add phases/faz-18/FAZ-18-SEC-03-COMMIT-KOMUTLARI.md
git add CHANGELOG.md
git commit -m "docs(decisions): Add K170-K172 and commit commands for SEC-03"
git status --short                                   # yalnızca ' M prompts/PROMPT-FAZ-18-3-SEC-01.md' (yukarıdaki ⚠️)
# git push -u origin docs/2026-11-16-faz-18-audit-fixes
```

## 3. Birleştirme (yalnızca backend)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-20-sec-03-shopier-callback-mode -m "Merge SEC-03 fix into faz-18-audit-fixes"
git status --short
# git push -u origin faz-18-audit-fixes
# git push -u origin fix/2026-11-20-sec-03-shopier-callback-mode
```

🔴 Birleştirmeyi atlama: sonraki prompt (18.6, `SEC-04`) önceki bulgunun birleşmiş olmasını denetler.

Bitince `phases/faz-18/README.md`'de `SEC-03` satırını `birleşti` yap.

## 4. Commit'ten sonra: elle işler

1. **Yayından önce, sunucuda salt okunur:** `grep -n '^SHOPIER_CONFIRMATION' <backend dizini>/.env`.
   `osb` ya da satır yok (varsayılan `osb`) olmalı. `callback` görürsen bu kod yayına çıktığı an kartla
   ödeme 503 olur: önce satırı `osb` yap, sonra `php artisan config:cache`. Yayın kaydı (Y8.3b) değerin
   şablondan (`osb`) geldiğini söylüyor; gözle doğrulanmadı.
2. **Yerelde kuralın kendisi** (`php artisan tinker`): backend `FAZ-18.md` §18.5 "Elle doğrulama" 3.
   adım. Log'da `CRITICAL: Shopier callback confirmation mode refused in production` görünmeli.
3. **Kart açıldığında** (`PAYMENT_METHODS=card,…`): `FAZ-12-ELLE-DOGRULAMA.md` adım 6 ve 7. Adım 7'nin
   sonucu K94'e ve `callback` kipinin tamamen kaldırılması kararına girer (açık karar).
4. **PHPStan'i elle çalıştırırken** önce `$env:PHPSTAN_TURBO = "0"`. Turbo açıkken bir kez koşulursa
   `%TEMP%\phpstan` önbelleği bozulur ve sonraki koşular docblock'ları görmez (backend `docs/rehber/phpstan.md`).
   `composer check` bunu kendisi ayarlıyor.
