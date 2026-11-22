# 19.11 `TST-02` — commit komutları

> ⚠️ Dallar SEC-06 dallarının üstünde (zincir: ARC-04 → OPS-04 → SEC-06 → TST-02). Birleştirmede bu sırayı koru.
> ⚠️ Backend `composer check` PHPStan adımında kırmızı: `ResolvesRefundRequests.php:29` (bu bulgunun dışında).

## Beklenen `git status --short --untracked-files=all`

**davetkart-backend-php-laravel** (`fix/2026-11-22-tst-02-lock-tests`)

```
 M app/Actions/Payment/ClaimReleasedOrderAction.php
 M docs/rehber/app/Actions/Payment/ClaimReleasedOrderAction.md
?? docs/rehber/tests/Support/LockAssertions.md
?? tests/Feature/LockInventoryTest.php
?? tests/Feature/LockRaceTest.php
?? tests/Support/LockAssertions.php
?? tests/Support/hold-row-lock.php
```

**davetkart-frontent:** boş · **davetkart-docs** (`docs/2026-11-22-tst-02-lock-tests`)

```
?? phases/faz-19/FAZ-19-TST-02-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-11-TST-02.md
```

## 19.11.1 — backend: kilit test yardımcısı + kılavuz + envanter

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add tests/Support/LockAssertions.php
git add tests/Support/hold-row-lock.php
git add docs/rehber/tests/Support/LockAssertions.md
git commit -m "19.11.1 - test(locks): Add lock assertions and the lockForUpdate inventory (K187)"
git status --short
```

## 19.11.2 — backend: her kilit için SQL düzeyi test

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add tests/Feature/LockInventoryTest.php
git commit -m "19.11.2 - test(locks): Assert every lockForUpdate call at the SQL level (K187)"
git status --short
```

## 19.11.3 — backend: iki bağlantılı kilit testleri + serbest hak yarışı düzeltmesi (D2 + D3)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add tests/Feature/LockRaceTest.php
git add app/Actions/Payment/ClaimReleasedOrderAction.php
git add docs/rehber/app/Actions/Payment/ClaimReleasedOrderAction.md
git commit -m "19.11.3 - fix(payments): Recheck a released order after the lock so a refund request keeps it frozen (K187, K188)"
git status --short
```

## 19.11.6 — docs: kayıt ve commit komutları

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-docs
git add phases/faz-19/kayit/19-11-TST-02.md
git add phases/faz-19/FAZ-19-TST-02-COMMIT-KOMUTLARI.md
git commit -m "docs(decisions): Add K187-K188 record and commit commands for TST-02"
git status --short
```

## Birleştirme (ana klasör, ARC-04 → OPS-04 → SEC-06'dan SONRA)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-22-tst-02-lock-tests -m "Merge TST-02 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-22-tst-02-lock-tests -m "Merge TST-02 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md`.
