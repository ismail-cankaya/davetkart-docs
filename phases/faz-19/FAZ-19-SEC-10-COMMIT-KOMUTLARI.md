# 19.15 `SEC-10` — commit komutları (D4: yalnızca docs)

> Backend ve frontend dalı **yok** (§A-1 boş → D4). Docs dalı TST-02 docs dalının üstünde (hat zinciri).

## Beklenen `git status --short --untracked-files=all`

**davetkart-backend-php-laravel:** dal değişmedi (`fix/2026-11-22-tst-02-lock-tests`), boş · **davetkart-frontent:** boş

**davetkart-docs** (`docs/2026-11-22-sec-10-shopier-buyer-fields`)

```
 M notes/README.md
?? notes/04-SHOPIER-ALICI-ALANLARI-SORUSU.md
?? phases/faz-19/FAZ-19-SEC-10-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-15-SEC-10.md
```

## 19.15.5 — docs: Shopier sorusu + kayıt + commit komutları

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-docs
git add notes/04-SHOPIER-ALICI-ALANLARI-SORUSU.md
git add notes/README.md
git add phases/faz-19/kayit/19-15-SEC-10.md
git add phases/faz-19/FAZ-19-SEC-10-COMMIT-KOMUTLARI.md
git commit -m "docs(notes): Add the Shopier buyer fields question and the SEC-10 record"
git status --short
```

## Birleştirme (ana klasör, TST-02 docs dalından SONRA)

```powershell
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-22-sec-10-shopier-buyer-fields -m "Merge SEC-10 prep into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md`.
