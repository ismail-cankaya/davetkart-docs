# Faz 14 — commit komutları (backend)

> Her blok bir commit. Blokları **sırayla** çalıştır. Her blok önce o adımın dosyalarını
> `Claude outputs\f14\backend\<adım>\` klasöründen depoya kopyalar (`robocopy`), sonra yalnızca onları ekler.
> Birden çok adımda değişen dosyalar (`routes/api.php`, `Order.php`, `ErrorCode.php`, `config/davetkart.php`, bazı md'ler)
> her adımın klasöründe **o adımdaki hâliyle** duruyor; son adımdan sonra çalışma ağacı son hâle gelmiş olur.
> Dal: `faz-14-account-settings` (zaten bu daldasın, `ec0ecb3`'ün üstü).
> Her commit tek başına sınandı (bulut çalışma alanında, PHP 8.5.9 + PostgreSQL 16): pint ✅ · phpstan 0 ✅ · `errors:export --check` ✅ · testler ✅.
> Test sayıları: 14.1 → 870 · 14.2 → 879 · 14.3 → 890 · 14.4 → 896 · 14.5 → 910 · 14.6 → 920 · 14.7 → 924 · 14.8 → 930 · 14.9 → 947 · 14.10 → **958**.
> 🔴 Migration'lar 14.1, 14.2 ve 14.9'da. Hepsi bittikten sonra `php artisan migrate` ve `composer check`.

## 14.1

```powershell
# 14.1 — Yanmış hak, çöp kutusu boşalınca geri doğmasın (consumed_at)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
robocopy "..\Claude outputs\f14\backend\14.1" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add database/migrations/2026_10_26_100000_add_consumed_at_to_orders_table.php app/Models/Order.php app/Actions/Invitation/DeleteInvitationAction.php app/Actions/Payment/ClaimReleasedOrderAction.php tests/Feature/OrderConsumptionTest.php docs/rehber/database/migrations/2026_10_26_100000_add_consumed_at_to_orders_table.md
git add docs/rehber/app/Models/Order.md docs/rehber/app/Actions/Invitation/DeleteInvitationAction.md docs/rehber/app/Actions/Payment/ClaimReleasedOrderAction.md docs/rehber/tests/Feature/OrderConsumptionTest.md
git commit -m "14.1 - fix(orders): Keep a burned publish right burned after the trash is purged"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.2

```powershell
# 14.2 — İade talebi tablosu ve durum makinesi
cd D:\Projects\davetkart\davetkart-backend-php-laravel
robocopy "..\Claude outputs\f14\backend\14.2" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add app/Enums/RefundRequestStatus.php database/migrations/2026_10_26_110000_create_refund_requests_table.php app/Models/RefundRequest.php database/factories/RefundRequestFactory.php app/Models/Order.php tests/Feature/RefundRequestConstraintsTest.php
git add tests/Unit/RefundRequestStatusTest.php docs/rehber/app/Enums/RefundRequestStatus.md docs/rehber/database/migrations/2026_10_26_110000_create_refund_requests_table.md docs/rehber/app/Models/RefundRequest.md docs/rehber/tests/Feature/RefundRequestConstraintsTest.md docs/rehber/app/Models/Order.md
git commit -m "14.2 - feat(refunds): Add the refund request table and its status machine"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.3

```powershell
# 14.3 — Hak özeti (Planlarım okuma modeli) + iptal edilebilirlik kuralı
cd D:\Projects\davetkart\davetkart-backend-php-laravel
robocopy "..\Claude outputs\f14\backend\14.3" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add config/davetkart.php app/Enums/RefundBlocker.php app/Services/Refund/RefundEligibility.php app/Enums/EntitlementState.php app/Actions/Account/TierEntitlements.php app/Actions/Account/EntitlementRight.php
git add app/Actions/Account/EntitlementSummary.php app/Actions/Account/SummarizeEntitlementsAction.php tests/Feature/SummarizeEntitlementsActionTest.php docs/rehber/app/Actions/Account/SummarizeEntitlementsAction.md docs/rehber/app/Services/Refund/RefundEligibility.md docs/rehber/tests/Feature/SummarizeEntitlementsActionTest.md
git add docs/rehber/config/davetkart.md
git commit -m "14.3 - feat(account): Summarize plan rights per tier and decide refund eligibility"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.4

```powershell
# 14.4 — GET /api/account/entitlements
cd D:\Projects\davetkart\davetkart-backend-php-laravel
robocopy "..\Claude outputs\f14\backend\14.4" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add app/Http/Resources/EntitlementSummaryResource.php app/Http/Controllers/Api/V1/AccountController.php routes/api.php tests/Feature/AccountEntitlementsTest.php docs/rehber/app/Http/Resources/EntitlementSummaryResource.md docs/rehber/app/Http/Controllers/Api/V1/AccountController.md
git add docs/rehber/routes/api.md docs/rehber/tests/Feature/AccountEntitlementsTest.md
git commit -m "14.4 - feat(account): Expose the plan rights summary to the owner"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.5

```powershell
# 14.5 — Hakkı iptal et / vazgeç + REFUND_NOT_ALLOWED
cd D:\Projects\davetkart\davetkart-backend-php-laravel
robocopy "..\Claude outputs\f14\backend\14.5" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add app/Enums/ErrorCode.php app/Actions/Payment/ClaimReleasedOrderAction.php app/Exceptions/RefundNotAllowedException.php app/Actions/Refund/RequestRefundAction.php app/Actions/Refund/WithdrawRefundRequestAction.php app/Http/Requests/Refund/StoreRefundRequestRequest.php
git add app/Http/Resources/RefundRequestResource.php app/Http/Controllers/Api/V1/RefundRequestController.php routes/api.php contracts/error-codes.json docs/08-HATA-SOZLESMESI.md tests/Feature/RefundRequestTest.php
git add docs/rehber/app/Actions/Refund/RequestRefundAction.md docs/rehber/tests/Feature/RefundRequestTest.md docs/rehber/routes/api.md docs/rehber/app/Actions/Payment/ClaimReleasedOrderAction.md docs/rehber/app/Enums/ErrorCode.md
git commit -m "14.5 - feat(refunds): Let the owner cancel an unused right and freeze it"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.6

```powershell
# 14.6 — refunds:list / approve / reject
cd D:\Projects\davetkart\davetkart-backend-php-laravel
robocopy "..\Claude outputs\f14\backend\14.6" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add app/Actions/Refund/ResolveRefundRequestAction.php app/Notifications/RefundRequestResolvedNotification.php app/Console/Commands/ListRefundRequests.php app/Console/Commands/ApproveRefundRequest.php app/Console/Commands/RejectRefundRequest.php app/Console/Commands/Concerns/ResolvesRefundRequests.php
git add tests/Feature/RefundCommandsTest.php docs/rehber/PROJE-KOMUTLARI.md docs/rehber/app/Console/Commands/RefundCommands.md docs/rehber/app/Actions/Refund/ResolveRefundRequestAction.md docs/rehber/tests/Feature/RefundCommandsTest.md
git commit -m "14.6 - feat(refunds): Approve or reject refund requests from the console"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.7

```powershell
# 14.7 — PATCH /api/auth/me (ad/soyad)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
robocopy "..\Claude outputs\f14\backend\14.7" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add app/Http/Requests/Account/UpdateProfileRequest.php app/Actions/Account/UpdateProfileAction.php app/Http/Controllers/Api/V1/ProfileController.php routes/api.php tests/Feature/ProfileUpdateTest.php docs/rehber/app/Actions/Account/UpdateProfileAction.md
git add docs/rehber/routes/api.md
git commit -m "14.7 - feat(account): Let the user edit their name"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.8

```powershell
# 14.8 — PUT /api/auth/password
cd D:\Projects\davetkart\davetkart-backend-php-laravel
robocopy "..\Claude outputs\f14\backend\14.8" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add app/Http/Requests/Account/ChangePasswordRequest.php app/Actions/Account/ChangePasswordAction.php app/Notifications/PasswordChangedNotification.php app/Http/Controllers/Api/V1/PasswordController.php routes/api.php tests/Feature/PasswordChangeTest.php
git add docs/rehber/app/Actions/Account/ChangePasswordAction.md docs/rehber/routes/api.md
git commit -m "14.8 - feat(account): Change the password while signed in and close other sessions"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.9

```powershell
# 14.9 — Aktif oturumlar (user_agent, IssueApiTokenAction)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
robocopy "..\Claude outputs\f14\backend\14.9" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add database/migrations/2026_10_26_120000_add_user_agent_to_personal_access_tokens_table.php app/Actions/Auth/IssueApiTokenAction.php app/Actions/Auth/LoginUserAction.php app/Actions/Auth/RegisterUserAction.php app/Http/Controllers/Api/V1/AuthController.php app/Support/DeviceLabel.php
git add app/Http/Resources/SessionResource.php app/Actions/Auth/RevokeSessionAction.php app/Actions/Auth/RevokeOtherSessionsAction.php app/Http/Controllers/Api/V1/SessionController.php routes/api.php tests/Feature/SessionTest.php
git add tests/Unit/DeviceLabelTest.php docs/rehber/database/migrations/2026_10_26_120000_add_user_agent_to_personal_access_tokens_table.md docs/rehber/app/Actions/Auth/IssueApiTokenAction.md docs/rehber/app/Actions/Auth/LoginUserAction.md docs/rehber/app/Actions/Auth/RegisterUserAction.md docs/rehber/routes/api.md
git commit -m "14.9 - feat(auth): List and revoke active sessions with their device"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.10

```powershell
# 14.10 — E-posta değişikliği (imzalı, tek kullanımlık bağlantı)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
robocopy "..\Claude outputs\f14\backend\14.10" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add config/davetkart.php app/Enums/ErrorCode.php app/Support/EmailChangeLink.php app/Http/Requests/Account/RequestEmailChangeRequest.php app/Actions/Account/RequestEmailChangeAction.php app/Notifications/EmailChangeConfirmationNotification.php
git add app/Http/Controllers/Api/V1/EmailChangeController.php app/Exceptions/EmailChangeFailedException.php app/Http/Requests/Account/ConfirmEmailChangeRequest.php app/Actions/Account/ConfirmEmailChangeAction.php app/Notifications/EmailChangedNotification.php app/Http/Controllers/Api/V1/PublicEmailChangeController.php
git add routes/api.php contracts/error-codes.json docs/08-HATA-SOZLESMESI.md tests/Feature/EmailChangeTest.php tests/Unit/EmailChangedNotificationTest.php docs/rehber/app/Actions/Account/RequestEmailChangeAction.md
git add docs/rehber/tests/Feature/EmailChangeTest.md docs/rehber/routes/api.md docs/rehber/app/Enums/ErrorCode.md docs/rehber/config/davetkart.md
git commit -m "14.10 - feat(account): Change the email address through a signed, single-use link"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.11

```powershell
# 14.11 — Faz 14 özeti ve elle doğrulama
cd D:\Projects\davetkart\davetkart-backend-php-laravel
robocopy "..\Claude outputs\f14\backend\14.11" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add docs/rehber/fazlar/FAZ-14.md docs/rehber/fazlar/FAZ-14-ELLE-DOGRULAMA.md docs/rehber/fazlar/README.md
git commit -m "14.11 - docs(account): Record Phase 14 and its manual verification"
git status --short    # bu adımın dosyası kalmamalı
```

## Son

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
php artisan migrate
composer check          # beklenen: 958 test
git log --oneline -11
git push
```
