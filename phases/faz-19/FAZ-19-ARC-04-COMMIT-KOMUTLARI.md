# 19.5 `ARC-04` — commit komutları

> ⚠️ Backend `composer check` PHPStan adımında kırmızı: `app/Console/Commands/Concerns/ResolvesRefundRequests.php:29` (bu bulgunun dışında, dokunulmadı). Önce kararı ver (kayıt §İsmail'e kalan elle işler 1).

## Beklenen `git status --short --untracked-files=all`

**davetkart-backend-php-laravel** (`fix/2026-11-20-arc-04-media-disk`)

```
 M app/Actions/Media/StoreUploadedMediaAction.php
 M app/Providers/AppServiceProvider.php
 M docs/10-URETIM-ENV-SABLONU.md
 M docs/11-PROJE-TARIHCESI-VE-IS-AKISLARI.md
?? app/Exceptions/MediaStorageUnavailableException.php
?? app/Support/MediaDiskGuard.php
?? docs/rehber/app/Support/MediaDiskGuard.md
?? tests/Feature/MediaDiskGuardTest.php
```

**davetkart-frontent:** boş · **davetkart-docs** (`docs/2026-11-20-arc-04-media-disk`)

```
?? phases/faz-19/FAZ-19-ARC-04-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-05-ARC-04.md
```

## 19.5.1 — backend: guard + about satırı + kılavuz + testler

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add app/Support/MediaDiskGuard.php
git add app/Exceptions/MediaStorageUnavailableException.php
git add app/Actions/Media/StoreUploadedMediaAction.php
git add app/Providers/AppServiceProvider.php
git add docs/rehber/app/Support/MediaDiskGuard.md
git add tests/Feature/MediaDiskGuardTest.php
git commit -m "19.5.1 - feat(media): Refuse uploads in production unless the media disk is s3 (K183)"
git status --short
```

## 19.5.3 — backend: üretim env şablonu ve tarihçe tablosu

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add docs/10-URETIM-ENV-SABLONU.md
git add docs/11-PROJE-TARIHCESI-VE-IS-AKISLARI.md
git commit -m "19.5.3 - docs(env): Document that production requires DAVETKART_MEDIA_DISK=s3 (K183)"
git status --short
```

## 19.5.4 — docs: kayıt ve commit komutları

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-docs
git add phases/faz-19/kayit/19-05-ARC-04.md
git add phases/faz-19/FAZ-19-ARC-04-COMMIT-KOMUTLARI.md
git commit -m "docs(decisions): Add K183 record and commit commands for ARC-04"
git status --short
```

## Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-20-arc-04-media-disk -m "Merge ARC-04 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-20-arc-04-media-disk -m "Merge ARC-04 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md`.
