# 19.10 `SEC-06` — commit komutları

> ⚠️ Dallar OPS-04 dallarının üstünde (yığılmış: ARC-04 → OPS-04 → SEC-06). Birleştirmede bu sırayı koru.
> ⚠️ Backend `composer check` PHPStan adımında kırmızı: `ResolvesRefundRequests.php:29` (bu bulgunun dışında).

## Beklenen `git status --short --untracked-files=all`

**davetkart-backend-php-laravel** (`fix/2026-11-22-sec-06-rate-limit-keys`)

```
 M app/Providers/AppServiceProvider.php
 M config/davetkart.php
 M docs/rehber/app/Providers/AppServiceProvider.md
 M docs/rehber/config/davetkart.md
 M routes/api.php
 M tests/Feature/RateLimitTest.php
?? tests/Feature/ApiRateLimitTest.php
```

**davetkart-frontent:** boş · **davetkart-docs** (`docs/2026-11-22-sec-06-rate-limit-keys`)

```
?? phases/faz-19/FAZ-19-SEC-06-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-10-SEC-06.md
```

## 19.10.1 — backend: kimlik anahtarlı `api` kovası, config sayıları, medya IP 60 (D1 + D3 + D4)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add app/Providers/AppServiceProvider.php
git add config/davetkart.php
git add docs/rehber/app/Providers/AppServiceProvider.md
git add docs/rehber/config/davetkart.md
git add tests/Feature/RateLimitTest.php
git commit -m "19.10.1 - fix(rate-limit): Key the api bucket by user when authenticated and move limits to config (K186)"
git status --short
```

## 19.10.2 — backend: misafir okuması kendi kovasında (D2) + testler

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add routes/api.php
git add tests/Feature/ApiRateLimitTest.php
git commit -m "19.10.2 - fix(rate-limit): Give the public invitation read its own bucket (K186)"
git status --short
```

## 19.10.5 — docs: kayıt ve commit komutları

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-docs
git add phases/faz-19/kayit/19-10-SEC-06.md
git add phases/faz-19/FAZ-19-SEC-06-COMMIT-KOMUTLARI.md
git commit -m "docs(decisions): Add K186 record and commit commands for SEC-06"
git status --short
```

## Birleştirme (ana klasör, ARC-04 ve OPS-04'ten SONRA)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-22-sec-06-rate-limit-keys -m "Merge SEC-06 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-22-sec-06-rate-limit-keys -m "Merge SEC-06 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md`.
