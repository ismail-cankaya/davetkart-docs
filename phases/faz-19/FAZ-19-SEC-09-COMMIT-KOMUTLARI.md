# 19.14 `SEC-09` — commit komutları

> Dallar entegrasyon dallarından. 19.14.1 (göç) gerekmedi; D1+D4 tek commit (19.14.2), D2+D3 tek commit (19.14.3).
> ⚠️ Backend `composer check` PHPStan adımında kırmızı: `ResolvesRefundRequests.php:29`, `ReadinessTest.php:175` (bu bulgunun dışında).

## 19.14.2 — backend: doğrulama bağlantısı, posta, onay ve yeniden gönderme (D1 + D4)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add app/Support/EmailVerificationLink.php
git add app/Notifications/VerifyEmailNotification.php
git add app/Exceptions/EmailVerificationFailedException.php
git add app/Actions/Account/SendEmailVerificationAction.php
git add app/Actions/Account/ConfirmEmailVerificationAction.php
git add app/Http/Requests/Account/ConfirmEmailVerificationRequest.php
git add app/Http/Controllers/Api/V1/EmailVerificationController.php
git add app/Actions/Auth/RegisterUserAction.php
git add app/Http/Resources/UserResource.php
git add app/Models/User.php
git add app/Enums/ErrorCode.php
git add contracts/error-codes.json
git add app/Providers/AppServiceProvider.php
git add config/davetkart.php
git add routes/api.php
git add tests/Feature/ProfileUpdateTest.php
git add docs/rehber/app/Support/EmailVerificationLink.md
git add docs/rehber/app/Http/Controllers/Api/V1/EmailVerificationController.md
git add docs/rehber/app/Actions/Auth/RegisterUserAction.md
git add docs/rehber/app/Http/Resources/UserResource.md
git add docs/rehber/app/Providers/AppServiceProvider.md
git add docs/rehber/config/davetkart.md
git commit -m "19.14.2 - feat(auth): Send a signed verification link on registration and let users resend it (K191)"
git status --short
```

## 19.14.3 — backend: ödeme ve yayın kapısı + indirim (D2 + D3)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add app/Support/VerifiedEmailGuard.php
git add app/Exceptions/EmailNotVerifiedException.php
git add app/Actions/Payment/StartCheckoutAction.php
git add app/Actions/Invitation/PublishInvitationAction.php
git add app/Services/Pricing/FirstPublishEligibility.php
git add tests/Feature/EmailVerificationTest.php
git add tests/Feature/InvitationTest.php
git add docs/rehber/app/Support/VerifiedEmailGuard.md
git add docs/rehber/app/Actions/Payment/StartCheckoutAction.md
git add docs/rehber/app/Actions/Invitation/PublishInvitationAction.md
git add docs/rehber/app/Services/Pricing/FirstPublishEligibility.md
git commit -m "19.14.3 - fix(auth): Require a verified email to check out, publish and get the first publish discount (K191)"
git status --short
```

## 19.14.7 — frontend: servis, sözleşme kopyası, çeviriler

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-frontent
git add src/services/account.ts
git add src/types.ts
git add src/contracts/error-codes.json
git add src/locales/tr/errors.json
git add src/locales/en/errors.json
git add src/locales/tr/translation.json
git add src/locales/en/translation.json
git add scripts/verify-endpoints.ts
git add docs/rehber/src/services/account.md
git commit -m "19.14.7 - feat(auth): Add the email verification endpoints, error codes and translations (K191)"
git status --short
```

## 19.14.8 — frontend: bant, doğrulama sayfası, E2E kancası

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-frontent
git add src/components/account/EmailVerificationBanner.tsx
git add src/pages/EmailVerificationPage.tsx
git add src/routes.tsx
git add src/components/layout/AppLayout.tsx
git add e2e/support/flows.ts
git add docs/rehber/src/components/account/EmailVerificationBanner.md
git add docs/rehber/src/pages/EmailVerificationPage.md
git add docs/rehber/e2e/README.md
git commit -m "19.14.8 - feat(auth): Show a verify-your-email banner and the verification page (K191)"
git status --short
```

## 19.14.9 — docs: kayıt ve commit komutları

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-docs
git add phases/faz-19/kayit/19-14-SEC-09.md
git add phases/faz-19/FAZ-19-SEC-09-COMMIT-KOMUTLARI.md
git commit -m "docs(decisions): Add K191 record and commit commands for SEC-09"
git status --short
```

## Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-23-sec-09-email-verification -m "Merge SEC-09 into faz-19-audit-fixes"
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-23-sec-09-email-verification -m "Merge SEC-09 into faz-19-audit-fixes"
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-23-sec-09-email-verification -m "Merge SEC-09 into docs/2026-11-20-faz-19-audit-fixes"
```

Çakışma çıkarsa: `19-CAKISMA.md`.
