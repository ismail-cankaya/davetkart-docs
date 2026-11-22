# 19.6 `OPS-04` — commit komutları

> ⚠️ Dallar ARC-04 dallarının üstünde (yığılmış). Birleştirmede **önce ARC-04** (`FAZ-19-ARC-04-COMMIT-KOMUTLARI.md` son blok), sonra bu dosyanın son bloğu.
> ⚠️ Backend `composer check` PHPStan adımında kırmızı: `ResolvesRefundRequests.php:29` (bu bulgunun dışında).

## Beklenen `git status --short --untracked-files=all`

**davetkart-backend-php-laravel** (`fix/2026-11-22-ops-04-env-template`)

```
 M app/Providers/AppServiceProvider.php
 M composer.json
 M docs/10-URETIM-ENV-SABLONU.md
?? app/Console/Commands/CheckEnvTemplate.php
?? app/Support/ProductionMailCheck.php
?? docs/rehber/app/Console/Commands/CheckEnvTemplate.md
?? docs/rehber/app/Support/ProductionMailCheck.md
?? tests/Feature/ProductionConfigTest.php
```

**davetkart-frontent:** boş · **davetkart-docs** (`docs/2026-11-22-ops-04-env-template`)

```
?? phases/faz-19/FAZ-19-OPS-04-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-06-OPS-04.md
```

## 19.6.1 — backend: şablon düzeltmeleri

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add docs/10-URETIM-ENV-SABLONU.md
git commit -m "19.6.1 - docs(env): Bring the production env template in line with the live server (K184)"
git status --short
```

## 19.6.2 — backend: `env:template --check`

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add app/Console/Commands/CheckEnvTemplate.php
git add docs/rehber/app/Console/Commands/CheckEnvTemplate.md
git add composer.json
git commit -m "19.6.2 - feat(console): Add env:template to check the template against config env keys (K184)"
git status --short
```

## 19.6.3 — backend: üretimde `log` posta sürücüsü uyarısı + testler

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add app/Support/ProductionMailCheck.php
git add app/Providers/AppServiceProvider.php
git add docs/rehber/app/Support/ProductionMailCheck.md
git add tests/Feature/ProductionConfigTest.php
git commit -m "19.6.3 - feat(mail): Log a critical when production mail goes to the log mailer (K185)"
git status --short
```

## 19.6.5 — docs: kayıt ve commit komutları

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-docs
git add phases/faz-19/kayit/19-06-OPS-04.md
git add phases/faz-19/FAZ-19-OPS-04-COMMIT-KOMUTLARI.md
git commit -m "docs(decisions): Add K184-K185 record and commit commands for OPS-04"
git status --short
```

## Birleştirme (ana klasör, ARC-04'ten SONRA)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-22-ops-04-env-template -m "Merge OPS-04 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-22-ops-04-env-template -m "Merge OPS-04 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md`.
