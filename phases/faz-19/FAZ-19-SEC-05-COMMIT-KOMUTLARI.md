# Faz 19.9 — `SEC-05` (parola politikası) commit komutları

> **Tarih:** 23 Kasım 2026 · **Karar:** K258 · **Kayıt:** [`kayit/19-09-SEC-05.md`](kayit/19-09-SEC-05.md)
> **Dallar:** backend ve frontend `fix/2026-11-23-sec-05-password-policy` · docs `docs/2026-11-23-sec-05-password-policy`.
> İsmail'in 23 Kasım izniyle commit ve birleştirmeyi ajan çalıştırdı; komutlar kayıt için. ⚠️ Backend `composer check` bu
> daldan bağımsız nedenle kırmızı ([`HAT-C-ACIK-HATALAR.md`](HAT-C-ACIK-HATALAR.md) #1, #11).

## Başlamadan

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git branch --show-current                     # fix/2026-11-23-sec-05-password-policy
git status --short --untracked-files=all
```

```
 M app/Http/Requests/Account/ChangePasswordRequest.php
 M app/Http/Requests/Auth/RegisterRequest.php
 M app/Http/Requests/Auth/ResetPasswordRequest.php
 M bootstrap/providers.php
 M docs/rehber/app/Http/Requests/Auth/RegisterRequest.md
 M tests/Feature/PasswordChangeTest.php
?? app/Providers/ValidationServiceProvider.php
?? app/Rules/PasswordPolicy.php
?? docs/rehber/app/Rules/PasswordPolicy.md
?? docs/rehber/tests/Feature/PasswordPolicyTest.md
?? resources/security/common-passwords.LICENSE
?? resources/security/common-passwords.txt
?? tests/Feature/PasswordPolicyTest.php
```

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-frontent
git branch --show-current                     # fix/2026-11-23-sec-05-password-policy
git status --short
```

```
 M scripts/verify-error-contract.ts
 M src/locales/en/errors.json
 M src/locales/tr/errors.json
 M src/pages/RegisterPage.tsx
 M src/pages/ResetPasswordPage.tsx
```

## 1. Backend — 19.9.1 (kural + liste)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git add app/Rules/PasswordPolicy.php
git add app/Providers/ValidationServiceProvider.php
git add bootstrap/providers.php
git add resources/security/common-passwords.txt
git add resources/security/common-passwords.LICENSE
git add docs/rehber/app/Rules/PasswordPolicy.md
git commit -m "19.9.1 - feat(auth): Add a single password policy that rejects the 10,000 most common passwords (K258)"
git status --short
```

## 2. Backend — 19.9.2 (üç istek + testler)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git add app/Http/Requests/Auth/RegisterRequest.php
git add app/Http/Requests/Auth/ResetPasswordRequest.php
git add app/Http/Requests/Account/ChangePasswordRequest.php
git add docs/rehber/app/Http/Requests/Auth/RegisterRequest.md
git add tests/Feature/PasswordPolicyTest.php
git add tests/Feature/PasswordChangeTest.php
git add docs/rehber/tests/Feature/PasswordPolicyTest.md
git commit -m "19.9.2 - fix(auth): Apply the password policy to registration, reset and password change (K258)"
git status --short
```

## 3. Frontend — 19.9.4 (çeviri + denetim + yorumlar) — 🔴 `git add -A` yok

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-frontent
git add src/locales/tr/errors.json
git add src/locales/en/errors.json
git add scripts/verify-error-contract.ts
git add src/pages/RegisterPage.tsx
git add src/pages/ResetPasswordPage.tsx
git commit -m "19.9.4 - feat(auth): Show the common password error and check its translation (K258)"
git status --short
```

## 4. Docs — 19.9.5 (kayıt + commit komutları)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add phases/faz-19/kayit/19-09-SEC-05.md
git add phases/faz-19/FAZ-19-SEC-05-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add the SEC-05 record and commit commands (K258)"
git status --short
```

## 5. Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-23-sec-05-password-policy -m "Merge SEC-05 into faz-19-audit-fixes"
git status --short
```

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-23-sec-05-password-policy -m "Merge SEC-05 into faz-19-audit-fixes"
git status --short
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-23-sec-05-password-policy -m "Merge SEC-05 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md` (olası yerler: `bootstrap/providers.php`, `src/locales/*/errors.json`).
