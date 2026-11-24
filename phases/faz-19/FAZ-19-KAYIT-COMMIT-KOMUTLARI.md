# Faz 19.90 — hat kayıtlarını birleştirme commit komutları

> **Tarih:** 24 Kasım 2026 · **Hat:** C · **Kararlar:** yeni K yok (K182, K183–K192, K220–K232, K250–K258 işlendi; sıradaki K259)
> **Dallar:** backend `fix/2026-11-24-faz19-records` · docs `docs/2026-11-24-faz19-records` (entegrasyon dallarından).
> İsmail'in 23 Kasım izniyle commit ve birleştirmeyi ajan çalıştırdı; komutlar kayıt için. Kod değişmedi; backend'de
> yalnızca `vendor/bin/pint --test` koştu (✅). Docs `python -I _restructure/build_decision_index.py --check` → 0
> (indeks 215 · tanım 215 · bekleyen 0).

## Başlamadan

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git branch --show-current                     # fix/2026-11-24-faz19-records
git status --short
```

```
 M docs/rehber/fazlar/FAZ-19.md
 M docs/rehber/fazlar/README.md
```

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git branch --show-current                     # docs/2026-11-24-faz19-records
git status --short
```

Beklenen: `CHANGELOG.md`, `_restructure/build_decision_index.py`, `decisions/DECISION-INDEX.md`,
`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`, `phases/faz-19/README.md`, `prompts/README.md`, 27 kayıt
dosyası (`phases/faz-19/kayit/19-00` … `19-27`) ve yeni `phases/faz-19/FAZ-19-KAYIT-COMMIT-KOMUTLARI.md`.

## 1. Backend — 19.90.1 (faz kaydı)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git add docs/rehber/fazlar/FAZ-19.md
git add docs/rehber/fazlar/README.md
git commit -m "19.90.1 - docs(faz-19): Add the 19.0 and 19.2-19.27 sections from the lane records to the phase record"
git status --short
```

## 2. Docs — paylaşılan dosyalar

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md
git add decisions/DECISION-INDEX.md
git add _restructure/build_decision_index.py
git add CHANGELOG.md
git add phases/faz-19/README.md
git add prompts/README.md
git commit -m "docs(faz-19): Merge the lane decisions K182-K258 into the shared records"
git status --short
```

## 3. Docs — kayıt notları + bu dosya

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add phases/faz-19/kayit/19-00-HAZIRLIK.md
git add phases/faz-19/kayit/19-02-ARC-01.md
git add phases/faz-19/kayit/19-03-ARC-02.md
git add phases/faz-19/kayit/19-04-ARC-05.md
git add phases/faz-19/kayit/19-05-ARC-04.md
git add phases/faz-19/kayit/19-06-OPS-04.md
git add phases/faz-19/kayit/19-07-OPS-03.md
git add phases/faz-19/kayit/19-08-OPS-05.md
git add phases/faz-19/kayit/19-09-SEC-05.md
git add phases/faz-19/kayit/19-10-SEC-06.md
git add phases/faz-19/kayit/19-11-TST-02.md
git add phases/faz-19/kayit/19-12-FE-51.md
git add phases/faz-19/kayit/19-13-SEC-08.md
git add phases/faz-19/kayit/19-14-SEC-09.md
git add phases/faz-19/kayit/19-15-SEC-10.md
git add phases/faz-19/kayit/19-16-SEC-13.md
git add phases/faz-19/kayit/19-17-SEC-12.md
git add phases/faz-19/kayit/19-18-SEC-11.md
git add phases/faz-19/kayit/19-19-FE-52.md
git add phases/faz-19/kayit/19-20-FE-01.md
git add phases/faz-19/kayit/19-21-FE-02.md
git add phases/faz-19/kayit/19-22-TST-04.md
git add phases/faz-19/kayit/19-23-FE-04.md
git add phases/faz-19/kayit/19-24-FE-10.md
git add phases/faz-19/kayit/19-25-FE-53.md
git add phases/faz-19/kayit/19-26-FE-50.md
git add phases/faz-19/kayit/19-27-FE-54.md
git add phases/faz-19/FAZ-19-KAYIT-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Mark the lane records as merged in 19.90 and add the commit commands"
git status --short
```

## 4. Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-24-faz19-records -m "Merge 19.90 records into faz-19-audit-fixes"
git status --short
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-24-faz19-records -m "Merge 19.90 records into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Sonra: 19.28 `ARC-03` (K259'dan başlar).
