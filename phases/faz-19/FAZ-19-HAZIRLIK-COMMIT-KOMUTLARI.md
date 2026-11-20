# Faz 19.0 — Hazırlık (hat başına test veritabanı) commit komutları

> **Tarih:** 20 Kasım 2026 · **Karar:** K182 · **Kayıt:** [`kayit/19-00-HAZIRLIK.md`](kayit/19-00-HAZIRLIK.md)
> **Dallar:** backend `fix/2026-11-20-faz19-parallel-test-db` (← `faz-19-audit-fixes`) ·
> docs `docs/2026-11-20-faz19-parallel-test-db` (← `docs/2026-11-20-faz-19-audit-fixes`) · frontend değişmedi.
> Bu prompt **ana klasörde** çalıştı (BAGLAM §2 istisnası); bütün bloklar `D:\Projects\davetkart\` altında.
> Komutları İsmail çalıştırır.

## Başlamadan: çalışma ağaçlarında ne olmalı

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git branch --show-current                     # fix/2026-11-20-faz19-parallel-test-db
git status --short --untracked-files=all
```

```
 M config/database.php
 M docs/rehber/config/database.md
 M docs/rehber/tests/Feature/TestSuiteIsolationTest.md
 M tests/Feature/TestSuiteIsolationTest.php
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git branch --show-current                     # docs/2026-11-20-faz19-parallel-test-db
git status --short --untracked-files=all
```

```
?? phases/faz-19/FAZ-19-HAZIRLIK-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-00-HAZIRLIK.md
```

## 1. Backend — 19.0.1

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git add config/database.php
git add tests/Feature/TestSuiteIsolationTest.php
git add docs/rehber/config/database.md
git add docs/rehber/tests/Feature/TestSuiteIsolationTest.md
git commit -m "19.0.1 - feat(testing): Add per-lane test database suffix for parallel runs (K182)"
git status --short
```

## 2. Docs — kayıt

```powershell
cd D:\Projects\davetkart\davetkart-docs
git add phases/faz-19/kayit/19-00-HAZIRLIK.md
git add phases/faz-19/FAZ-19-HAZIRLIK-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add 19.0 prep record for per-lane test databases (K182)"
git status --short
```

## 3. Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-19-audit-fixes
git merge --no-ff fix/2026-11-20-faz19-parallel-test-db -m "Merge faz19-parallel-test-db into faz-19-audit-fixes"
git status --short
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-20-faz-19-audit-fixes
git merge --no-ff docs/2026-11-20-faz19-parallel-test-db -m "Merge faz19-parallel-test-db into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: [`19-CAKISMA.md`](../../prompts/faz-19-agent/19-CAKISMA.md).

## 4. Hatları hazırla (birleştirmeden sonra, elle)

```powershell
& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres davetkart_test_hat_a
& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres davetkart_test_hat_b
& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres davetkart_test_hat_c
```

Her hattın backend worktree'sinin `.env`'ine (dosya satır sonuyla bitmiyorsa önce yeni satır):
`DAVETKART_TEST_DB_SUFFIX=hat_a` / `hat_b` / `hat_c`. Sonra her hatta:

```powershell
php artisan test --compact --filter=TestSuiteIsolationTest   # 4 passed
```
