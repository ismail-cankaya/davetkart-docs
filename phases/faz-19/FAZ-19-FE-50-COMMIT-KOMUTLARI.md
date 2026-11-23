# 19.26 `FE-50` — commit komutları

> Dallar entegrasyon dallarından. ⚠️ Backend `composer check` PHPStan adımında kırmızı: `ResolvesRefundRequests.php:29`, `ReadinessTest.php:175` (bu bulgunun dışında).

## 19.26.1 — backend: taslak tavanı (D3)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add app/Exceptions/DraftLimitReachedException.php
git add app/Actions/Invitation/CreateInvitationAction.php
git add app/Enums/ErrorCode.php
git add contracts/error-codes.json
git add config/davetkart.php
git add tests/Feature/InvitationTest.php
git add docs/rehber/app/Actions/Invitation/CreateInvitationAction.md
git add docs/rehber/config/davetkart.md
git commit -m "19.26.1 - fix(invitations): Cap unpublished invitations per user under a row lock (K192)"
git status --short
```

## 19.26.3 — frontend: ilk taslak yalnızca gerçek içerikte (D1)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-frontent
git add src/utils/draftContent.ts
git add src/hooks/useInvitationAutoSave.ts
git add src/components/create/DetailsFormStep.tsx
git add docs/rehber/src/hooks/useInvitationAutoSave.md
git commit -m "19.26.3 - fix(editor): Open the first draft only on real content or an explicit create (K192)"
git status --short
```

## 19.26.4 — frontend: adres kaydı taşır (D2)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-frontent
git add src/routes.tsx
git add src/pages/CreatePage.tsx
git add src/pages/DashboardPage.tsx
git add docs/rehber/src/pages/CreatePage.md
git add docs/rehber/src/pages/DashboardPage.md
git commit -m "19.26.4 - feat(editor): Keep the draft id in the URL and reload it on /create/:id (K192)"
git status --short
```

## 19.26.5 — frontend: hata kodu, verify:state, E2E (D3)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-frontent
git add src/contracts/error-codes.json
git add src/locales/tr/errors.json
git add src/locales/en/errors.json
git add scripts/verify-editor-state.ts
git add e2e/support/flows.ts
git add e2e/publish-with-gift-code.spec.ts
git add docs/rehber/e2e/README.md
git commit -m "19.26.5 - test(editor): Cover the draft gate in verify:state and the reload in journey 1 (K192)"
git status --short
```

## 19.26.6 — docs: kayıt ve commit komutları

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-docs
git add phases/faz-19/kayit/19-26-FE-50.md
git add phases/faz-19/FAZ-19-FE-50-COMMIT-KOMUTLARI.md
git commit -m "docs(decisions): Add K192 record and commit commands for FE-50"
git status --short
```

## Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-23-fe-50-draft-lifecycle -m "Merge FE-50 into faz-19-audit-fixes"
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-23-fe-50-draft-lifecycle -m "Merge FE-50 into faz-19-audit-fixes"
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-23-fe-50-draft-lifecycle -m "Merge FE-50 into docs/2026-11-20-faz-19-audit-fixes"
```

Çakışma çıkarsa: `19-CAKISMA.md`.
