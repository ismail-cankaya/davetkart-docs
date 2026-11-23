# 19.13 `SEC-08` — commit komutları

> Dallar entegrasyon dallarından açıldı (FE-51 birleşmişti). 19.13.1 (göç) gerekmedi; 19.13.4 (D3) seçilmedi.
> ⚠️ Backend `composer check` PHPStan adımında kırmızı: `ResolvesRefundRequests.php:29` ve `ReadinessTest.php:175` (ikisi de bu bulgunun dışında).

## Beklenen `git status --short --untracked-files=all`

**davetkart-backend-php-laravel** (`fix/2026-11-23-sec-08-guest-upload-budget`)

```
 M app/Actions/Media/StoreUploadedMediaAction.php
 M app/Console/Commands/PruneOrphanMedia.php
 M app/Models/Media.php
 M config/davetkart.php
 M docs/rehber/app/Actions/Media/StoreUploadedMediaAction.md
 M docs/rehber/app/Console/Commands/PruneOrphanMedia.md
 M docs/rehber/app/Models/Media.md
 M docs/rehber/config/davetkart.md
 M docs/rehber/routes/console.md
 M docs/rehber/tests/Support/LockAssertions.md
 M routes/console.php
 M tests/Feature/LockInventoryTest.php
 M tests/Feature/MaintenanceTest.php
 M tests/Feature/MediaTest.php
```

**davetkart-frontent:** dal yok · **davetkart-docs** (`docs/2026-11-23-sec-08-guest-upload-budget`)

```
?? phases/faz-19/FAZ-19-SEC-08-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-13-SEC-08.md
```

## 19.13.2 — backend: bayt bütçesi ve bekleyen kota (D1 + D2 + D4)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add app/Models/Media.php
git add app/Actions/Media/StoreUploadedMediaAction.php
git add config/davetkart.php
git add docs/rehber/app/Models/Media.md
git add docs/rehber/app/Actions/Media/StoreUploadedMediaAction.md
git add docs/rehber/config/davetkart.md
git add docs/rehber/tests/Support/LockAssertions.md
git add tests/Feature/MediaTest.php
git add tests/Feature/LockInventoryTest.php
git commit -m "19.13.2 - fix(media): Cap guest uploads by attached bytes and keep pending uploads in their own quota (K190)"
git status --short
```

## 19.13.3 — backend: yetim temizliği saatlik (D2)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add app/Console/Commands/PruneOrphanMedia.php
git add routes/console.php
git add docs/rehber/app/Console/Commands/PruneOrphanMedia.md
git add docs/rehber/routes/console.md
git add tests/Feature/MaintenanceTest.php
git commit -m "19.13.3 - fix(media): Prune orphaned guest uploads every hour (K190)"
git status --short
```

## 19.13.6 — docs: kayıt ve commit komutları

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-docs
git add phases/faz-19/kayit/19-13-SEC-08.md
git add phases/faz-19/FAZ-19-SEC-08-COMMIT-KOMUTLARI.md
git commit -m "docs(decisions): Add K190 record and commit commands for SEC-08"
git status --short
```

## Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-23-sec-08-guest-upload-budget -m "Merge SEC-08 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-23-sec-08-guest-upload-budget -m "Merge SEC-08 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md`.
