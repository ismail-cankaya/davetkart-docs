# Faz 19.3 — `ARC-02` (Faz 16–17 kayıtları) commit komutları

> **Tarih:** 20 Kasım 2026 · **Karar:** K252 · **Kayıt:** [`kayit/19-03-ARC-02.md`](kayit/19-03-ARC-02.md)
> **Dallar:** backend `fix/2026-11-20-arc-02-phase-16-17-records` (← `faz-19-audit-fixes`) · docs
> `docs/2026-11-20-arc-02-phase-16-17-records` (§3'te açılır) · frontend değişmedi. Komutları İsmail çalıştırır.
> **Sıra:** önce `FAZ-19-ARC-01-COMMIT-KOMUTLARI.md` §1–§3 (docs worktree'sinde ARC-01 değişiklikleri
> commit'siz duruyordu; ARC-02'nin docs dalı bu yüzden açılmadı, iki dosyası untracked bekliyor).

## Başlamadan: çalışma ağaçlarında ne olmalı

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git branch --show-current                     # fix/2026-11-20-arc-02-phase-16-17-records
git status --short --untracked-files=all
```

```
 M docs/rehber/fazlar/FAZ-15.md
?? docs/rehber/fazlar/FAZ-16-ELLE-DOGRULAMA.md
?? docs/rehber/fazlar/FAZ-16.md
?? docs/rehber/fazlar/FAZ-17-ELLE-DOGRULAMA.md
?? docs/rehber/fazlar/FAZ-17.md
```

Docs (ARC-01 commit'lerinden sonra), `git status --short --untracked-files=all`:

```
?? phases/faz-19/FAZ-19-ARC-02-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-03-ARC-02.md
```

## 1. Backend — 19.3.1 (Faz 16)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git add docs/rehber/fazlar/FAZ-16.md
git add docs/rehber/fazlar/FAZ-16-ELLE-DOGRULAMA.md
git commit -m "19.3.1 - docs(phases): Add the Phase 16 record and its manual check list (K252)"
git status --short
```

## 2. Backend — 19.3.2 (Faz 17) + 19.3.3 (Faz 15 durum notu)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git add docs/rehber/fazlar/FAZ-17.md
git add docs/rehber/fazlar/FAZ-17-ELLE-DOGRULAMA.md
git commit -m "19.3.2 - docs(phases): Add the Phase 17 record and its manual check list (K252)"
git add docs/rehber/fazlar/FAZ-15.md
git commit -m "19.3.3 - docs(phases): Add a gate status note to the Phase 15 record"
git status --short
```

## 3. Docs — 19.3.4 (kayıt)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git switch -c docs/2026-11-20-arc-02-phase-16-17-records docs/2026-11-20-faz-19-audit-fixes
git add phases/faz-19/kayit/19-03-ARC-02.md
git add phases/faz-19/FAZ-19-ARC-02-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add the ARC-02 record and commit commands (K252)"
git status --short
```

## 4. Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-20-arc-02-phase-16-17-records -m "Merge ARC-02 into faz-19-audit-fixes"
git status --short
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-20-arc-02-phase-16-17-records -m "Merge ARC-02 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md`. ⚠️ Backend kapısı (`composer check`) bu daldan bağımsız nedenle kırmızı: kayıt §"Kapı kırmızı".
