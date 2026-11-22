# Faz 19.8 — `OPS-05` (süre takvimi) commit komutları

> **Tarih:** 22 Kasım 2026 · **Karar:** yok · **Kayıt:** [`kayit/19-08-OPS-05.md`](kayit/19-08-OPS-05.md)
> **Dal:** docs `docs/2026-11-22-ops-05-expiry-calendar` (← `docs/2026-11-20-faz-19-audit-fixes`) · backend ve frontend değişmedi.
> Komutları İsmail çalıştırır.

## Başlamadan

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel; git status --short --untracked-files=all
cd D:\Projects\davetkart-hat-c\davetkart-frontent; git status --short --untracked-files=all
```

```
(ikisi de boş)
```

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git branch --show-current                     # docs/2026-11-22-ops-05-expiry-calendar
git status --short --untracked-files=all
```

```
 M .gitattributes
 M operations/README.md
 M operations/deployment/YAYIN-PLANI.md
 M phases/faz-19/HAT-C-ACIK-HATALAR.md
?? operations/deployment/SURE-TAKVIMI.md
?? operations/deployment/davetkart-sure-takvimi.ics
?? phases/faz-19/FAZ-19-OPS-05-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-08-OPS-05.md
```

## 1. Docs — 19.8.1 (takvim)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add operations/deployment/SURE-TAKVIMI.md
git add operations/README.md
git add operations/deployment/YAYIN-PLANI.md
git commit -m "docs(operations): Add the expiry calendar as the single home for renewal dates"
git status --short
```

## 2. Docs — 19.8.2 (`.ics`)

`.gitattributes` aynı commit'te: önce kural, sonra dosya (yoksa `.ics` LF'ye çevrilerek saklanır).

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add .gitattributes
git add operations/deployment/davetkart-sure-takvimi.ics
git commit -m "docs(operations): Add calendar reminders for the domain, mail and AWS credit expiries"
git status --short
```

## 3. Docs — 19.8.3 (kayıt)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add phases/faz-19/kayit/19-08-OPS-05.md
git add phases/faz-19/HAT-C-ACIK-HATALAR.md
git add phases/faz-19/FAZ-19-OPS-05-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add the OPS-05 record and commit commands"
git status --short
```

## 4. Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-22-ops-05-expiry-calendar -m "Merge OPS-05 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md`.
