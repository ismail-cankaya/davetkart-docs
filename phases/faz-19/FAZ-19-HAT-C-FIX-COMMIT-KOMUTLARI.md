# Faz 19 ortak düzeltme — Hat C açık hataları (`HAT-C-ACIK-HATALAR.md`) commit komutları

> **Tarih:** 25 Kasım 2026 · **Hat:** C · **Girdi:** [`HAT-C-ACIK-HATALAR.md`](HAT-C-ACIK-HATALAR.md) · **Yeni karar:** yok
> **Dallar:** backend ve frontend `fix/2026-11-25-hat-c-open-issues` (`faz-19-fix`'ten, `78c1cc4` / `fe70b62`) ·
> docs `docs/2026-11-25-hat-c-fixes` (`docs/2026-11-20-faz-19-audit-fixes`'ten). Birleştirme: kod → `faz-19-fix`, docs → docs entegrasyon dalı.
> Bütün blokları İsmail'in izniyle (23 ve 25 Kasım) ajan çalıştırdı; dosya kayıt içindir.

## 1. Backend — 19.91.1–19.91.8 (çalıştırıldı)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
# 19.91.1 — #11, #12 (kök neden: PHPStan sonuç önbelleği bütün worktree'lerde ortaktı; §1.1'de Hat B'ninkiyle değişti)
git add phpstan.neon
git add storage/phpstan/.gitignore
git commit -m "19.91.1 - chore(phpstan): Keep the result cache per worktree"
# 19.91.2 — #1
git add app/Console/Commands/Concerns/ResolvesRefundRequests.php
git add docs/rehber/app/Console/Commands/Concerns/ResolvesRefundRequests.md
git commit -m "19.91.2 - fix(refunds): Narrow the refund id argument instead of casting it"
# 19.91.3 — ReadinessTest:175 (Hat A H1, Hat B B-H1)
git add tests/Feature/ReadinessTest.php
git commit -m "19.91.3 - test(readiness): Pass a real queue job to JobFailed"
# 19.91.4 — #19 (CheckK18, K18CheckTest tipleri), #16, #17
git add app/Console/Commands/CheckK18.php
git add app/Support/K18Inspector.php
git add docs/rehber/app/Support/K18Inspector.md
git add tests/Feature/K18CheckTest.php
git add docs/rehber/tests/Feature/K18CheckTest.md
git commit -m "19.91.4 - fix(k18): Narrow the command input, stop trailing comments from starting a block and keep the test file out of the repo"
# 19.91.5 — #13 (9 kılavuz + genel bakışa not)
git add docs/rehber/app/Contracts/HealthCheck.md
git add docs/rehber/app/Contracts/DiskUsage.md
git add docs/rehber/app/Support/Health/DatabaseCheck.md
git add docs/rehber/app/Support/Health/DiskSpaceCheck.md
git add docs/rehber/app/Support/Health/LocalDiskUsage.md
git add docs/rehber/app/Support/Health/QueueBacklogCheck.md
git add docs/rehber/app/Support/Health/RecordSchedulerHeartbeat.md
git add docs/rehber/app/Support/Health/SchedulerHeartbeatCheck.md
git add docs/rehber/app/Http/Controllers/Api/V1/ReadinessController.md
git add docs/rehber/app/Support/Health/ReadinessProbe.md
git commit -m "19.91.5 - docs(health): Add the missing guides for the readiness checks (K18)"
# 19.91.6 — #14
git add routes/api.php
git add app/Providers/AppServiceProvider.php
git commit -m "19.91.6 - docs(k18): Replace the three truncated code summaries with whole sentences"
# 19.91.7 — #15
git add docs/rehber/routes/api.md
git commit -m "19.91.7 - docs(routes): Restore the lists and paragraphs lost in the moved route notes"
# 19.91.8 — #20
git add docs/rehber/fazlar/FAZ-19.md
git commit -m "19.91.8 - docs(faz-19): Record the real K18 inventory measured with K18Inspector"
# 19.91.10 — FAZ-19.md durum satırı
git add docs/rehber/fazlar/FAZ-19.md
git commit -m "19.91.10 - docs(faz-19): Mark composer check green after the shared fixes"
git status --short
```

### 1.1 Hat B ile çakışma (çalıştırıldı)

Hat B aynı arada `faz-19-fix`'e B-H7 (`tmpDir`) ve B-H1'i (aynı PHPStan hataları) birleştirdi. Hat C dalına önce
`faz-19-fix` alındı; eşdeğer düzeltmelerde **Hat B'nin hâli** tutuldu (`phpstan.neon` + kök `.gitignore`,
`ResolvesRefundRequests` + kılavuzu, `CheckK18`, `ReadinessTest` PHPUnit stub'ı). Hat C'den kalan: `K18Inspector`
sınırları (#17), `K18CheckTest` geçici kökü (#16, Hat B'nin `k18()` yardımcısıyla), OPS-03 kılavuzları ve doküman işleri.
Tekrar eden `storage/phpstan/.gitignore` silindi. Birleşik hâlde `composer check` yeniden yeşil (1273/1273).

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git merge --no-ff --no-commit faz-19-fix
git checkout --theirs app/Console/Commands/CheckK18.php app/Console/Commands/Concerns/ResolvesRefundRequests.php docs/rehber/app/Console/Commands/Concerns/ResolvesRefundRequests.md phpstan.neon tests/Feature/ReadinessTest.php
# K18CheckTest.php elle: Hat B'nin k18() adı + Hat C'nin geçici kökü
git rm --cached storage/phpstan/.gitignore
git commit -m "Merge faz-19-fix into fix/2026-11-25-hat-c-open-issues"
```

## 2. Frontend — 19.91.9 (çalıştırıldı)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-frontent
# #27
git add src/components/account/PasswordForm.tsx
git add src/locales/tr/translation.json
git add src/locales/en/translation.json
git commit -m "19.91.9 - fix(account): Tell users that common passwords are not accepted"
git status --short
```

## 3. Docs (çalıştırıldı)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add phases/faz-19/HAT-C-ACIK-HATALAR.md
git add phases/faz-19/FAZ-19-HAT-C-FIX-COMMIT-KOMUTLARI.md
git add phases/faz-19/README.md
git add CHANGELOG.md
git commit -m "docs(faz-19): Record the Hat C fixes on the shared Faz 19 fix branch"
git status --short
```

## 4. Birleştirme — ana klasör (çalıştırıldı)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git status --short
git merge --no-ff fix/2026-11-25-hat-c-open-issues -m "Merge Hat C open issues into faz-19-fix"
cd D:\Projects\davetkart\davetkart-frontent
git status --short
git merge --no-ff fix/2026-11-25-hat-c-open-issues -m "Merge Hat C open issues into faz-19-fix"
cd D:\Projects\davetkart\davetkart-docs
git status --short
git merge --no-ff docs/2026-11-25-hat-c-fixes -m "Merge Hat C fixes into docs/2026-11-20-faz-19-audit-fixes"
```

## 5. İsmail'e kalan

- `push` yok (ajan push etmez). İlk push'ta CI özetinde `k18:` satırı görülmeli (#31).
- `v1.2.0` ve öncekiler (#21): `composer check` artık yeşil; sıra [`FAZ-19-ARC-03-COMMIT-KOMUTLARI.md`](FAZ-19-ARC-03-COMMIT-KOMUTLARI.md) §5–§7.
- #28 (eski zayıf parolalar), #26 (frontend `verify:k18`), §D elle işleri: karar/eylem İsmail'in.
