# Faz 19.2 — `ARC-01` (karar indeksi) commit komutları

> **Tarih:** 20 Kasım 2026 · **Kararlar:** K250, K251 · **Kayıt:** [`kayit/19-02-ARC-01.md`](kayit/19-02-ARC-01.md)
> **Dal:** docs `docs/2026-11-20-arc-01-decision-index-hat-c` (← `docs/2026-11-20-faz-19-audit-fixes`) ·
> backend ve frontend değişmedi. Komutları İsmail çalıştırır.

## Başlamadan: çalışma ağaçlarında ne olmalı

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel; git status --short --untracked-files=all
cd D:\Projects\davetkart-hat-c\davetkart-frontent; git status --short --untracked-files=all
```

```
(ikisi de boş)
```

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git branch --show-current                     # docs/2026-11-20-arc-01-decision-index-hat-c
git status --short --untracked-files=all
```

```
 M _restructure/build_decision_index.py
 M decisions/DECISION-INDEX.md
?? phases/faz-19/FAZ-19-ARC-01-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-02-ARC-01.md
```

## 1. Docs — 19.2.1 (`--check`)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add _restructure/build_decision_index.py
git commit -m "docs(decisions): Add a --check mode that compares the decision index with every K definition (K250, K251)"
git status --short
```

## 2. Docs — 19.2.2 (K128–K145)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add decisions/DECISION-INDEX.md
git commit -m "docs(decisions): Add K128-K145 to the decision index and reserve the Faz 19 lane ranges"
git status --short
```

## 3. Docs — 19.2.3 (kayıt)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add phases/faz-19/kayit/19-02-ARC-01.md
git add phases/faz-19/FAZ-19-ARC-01-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add the ARC-01 record and commit commands (K250, K251)"
git status --short
```

## 4. İsteğe bağlı: eski boş ARC-01 worktree'si

`docs/2026-11-20-arc-01-decision-index` dalı 625a733'te, commit'siz; worktree'si temizdi. Önce bak, temizse kaldır:

```powershell
cd D:\Projects\davetkart\davetkart-docs
git -C D:\Projects\davetkart\davetkart-docs.worktrees\arc-01-decision-index status --short
git worktree remove D:\Projects\davetkart\davetkart-docs.worktrees\arc-01-decision-index
git branch -d docs/2026-11-20-arc-01-decision-index
```

## 5. Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-20-arc-01-decision-index-hat-c -m "Merge ARC-01 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
python -I _restructure/build_decision_index.py --check   # beklenen: çıkış 0
```

Çakışma çıkarsa: `19-CAKISMA.md`.
