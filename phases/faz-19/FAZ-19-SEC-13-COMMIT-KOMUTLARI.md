# Faz 19.16 — `SEC-13` (tarihsiz davetiyenin misafir verisi) commit komutları

> **Tarih:** 23 Kasım 2026 · **Karar:** K257 · **Kayıt:** [`kayit/19-16-SEC-13.md`](kayit/19-16-SEC-13.md)
> **Dallar:** backend `fix/2026-11-23-sec-13-purge-undated` · docs `docs/2026-11-23-sec-13-purge-undated` · frontend değişmedi.
> İsmail'in 23 Kasım izniyle commit ve birleştirmeyi ajan çalıştırdı; komutlar kayıt için. ⚠️ Backend `composer check` bu
> daldan bağımsız nedenle kırmızı ([`HAT-C-ACIK-HATALAR.md`](HAT-C-ACIK-HATALAR.md) #1, #11).

## Başlamadan

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git branch --show-current                     # fix/2026-11-23-sec-13-purge-undated
git status --short --untracked-files=all
```

```
 M app/Console/Commands/PurgeExpiredData.php
 M docs/rehber/app/Console/Commands/PurgeExpiredData.md
 M tests/Feature/MaintenanceTest.php
```

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git branch --show-current                     # docs/2026-11-23-sec-13-purge-undated
git status --short --untracked-files=all
```

```
 M phases/faz-19/HAT-C-ACIK-HATALAR.md
?? phases/faz-19/FAZ-19-SEC-13-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-16-SEC-13.md
```

## 1. Backend — 19.16.1 (yedek kural + `--dry-run` satırı)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git add app/Console/Commands/PurgeExpiredData.php
git add tests/Feature/MaintenanceTest.php
git add docs/rehber/app/Console/Commands/PurgeExpiredData.md
git commit -m "19.16.1 - fix(privacy): Purge guest data of undated invitations twelve months after publish or creation (K257)"
git status --short
```

## 2. Docs — 19.16.3 (kayıt + commit komutları)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add phases/faz-19/kayit/19-16-SEC-13.md
git add phases/faz-19/FAZ-19-SEC-13-COMMIT-KOMUTLARI.md
git add phases/faz-19/HAT-C-ACIK-HATALAR.md
git commit -m "docs(faz-19): Add the SEC-13 record and commit commands (K257)"
git status --short
```

## 3. Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-23-sec-13-purge-undated -m "Merge SEC-13 into faz-19-audit-fixes"
git status --short
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-23-sec-13-purge-undated -m "Merge SEC-13 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md` (olası yer: `tests/Feature/MaintenanceTest.php`).
