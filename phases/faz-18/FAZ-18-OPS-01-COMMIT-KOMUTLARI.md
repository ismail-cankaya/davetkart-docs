# Faz 18.1 — `OPS-01` commit komutları

> **Tarih:** 16 Kasım 2026 · **Kararlar:** K146–K150 · **Faz kaydı:** backend `docs/rehber/fazlar/FAZ-18.md` §18.1
> Her blok bir commit. Dosyalar tek tek, açık yolla eklenir; joker, klasör yolu ve `-A` yok
> (frontend'de CRLF tuzağı). Her blok `git status --short` ile biter.

## Durum (16 Kasım 2026, 09:20)

| Depo | Yapıldı | Kalan |
|---|---|---|
| backend | `5b4ae25` 18.1.1 · `700785d` 18.1.2 · `d941945` 18.1.3 · `660c5b3` 18.1.4 · `162c985` birleştirme | §2: 18.1.7 (faz kaydına frontend sonucu) + ikinci birleştirme |
| frontend | `f35aa2c` birleştirme (18.1.0) | §1: 18.1.5 (`package.json`) + birleştirme |
| docs | `6fba0f0` 18.1.6 | §3: bu dosya, takip tablosu, `CHANGELOG.md` |

⚠️ `f35aa2c` yalnızca `package.json` ve `package-lock.json`'ı değil, 18.1.5'in dört yeni dosyasını da
içeriyor (`src/contracts/plan-rules.json`, `src/contracts/planRules.ts`, `scripts/verify-plan-rules.ts`,
`docs/rehber/scripts/verify-plan-rules.md`): commit atılırken izlenmeyen dosya olarak bekliyorlardı.
İçerik doğru; 18.1.5 commit'i bu yüzden tek dosya. Geçmişi yeniden yazmaya gerek yok.

## 1. Frontend — kalan

```powershell
# 18.1.5 — verify:plans betiğini verify zincirine bağla
cd D:\Projects\davetkart\davetkart-frontent
git switch fix/2026-11-16-ops-01-release-alignment
git add package.json
git commit -m "18.1.5 - feat(verify): Wire verify:plans into the verify chain"
git status --short                                   # boş olmalı ('?? .claude/' olabilir)
```

```powershell
# Birleştirme
cd D:\Projects\davetkart\davetkart-frontent
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-16-ops-01-release-alignment -m "Merge OPS-01 fix into faz-18-audit-fixes"
git status --short
# git push -u origin faz-18-audit-fixes
# git push -u origin fix/2026-11-16-ops-01-release-alignment
```

## 2. Backend — kalan

`FAZ-18.md` 18.1.4'te commit'lendikten sonra frontend'in son doğrulama sonuçlarıyla güncellendi.

```powershell
# 18.1.7 — faz kaydı: frontend doğrulama sonuçları ve birleştirme commit'i notu
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-ops-01-release-alignment
git add docs/rehber/fazlar/FAZ-18.md
git commit -m "18.1.7 - docs(phases): Record the frontend verification results for OPS-01"
git status --short                                   # boş olmalı
```

```powershell
# İkinci birleştirme (tek commit taşır)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-16-ops-01-release-alignment -m "Merge OPS-01 record update into faz-18-audit-fixes"
git status --short
# git push -u origin faz-18-audit-fixes
# git push -u origin fix/2026-11-16-ops-01-release-alignment
```

🔴 18.1.7'yi commit'leyip birleştirmeyi atlama: sonraki prompt (18.2, `OPS-02`) backend'de
`git branch --merged faz-18-audit-fixes | Select-String "ops-01-"` ile bakar; düzeltme dalında
birleşmemiş commit kalırsa bu satır boş döner ve 18.2 durur.

## 3. Docs — kalan

```powershell
# Takip tablosu ve commit komutları gerçek duruma göre
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-16-faz-18-audit-fixes
git add phases/faz-18/README.md
git add phases/faz-18/FAZ-18-OPS-01-COMMIT-KOMUTLARI.md
git add CHANGELOG.md
git commit -m "docs(faz-18): Record the final OPS-01 state and remaining commit commands"
git status --short                                   # boş olmalı
# git push -u origin docs/2026-11-16-faz-18-audit-fixes
```

Üç bölüm de bitince `phases/faz-18/README.md`'de `OPS-01` satırını `birleşti` yap.

## 4. Etiket

Bu fazda **atılmaz.** `v1.1.0` Faz 18 sonunda, 18.6 §11'deki dört komut yeşilken atılır; komutlar
[`operations/deployment/YAYIN-SIRASI.md`](../../operations/deployment/YAYIN-SIRASI.md) §3'te.

---

## Çalıştırıldı (kayıt)

Aşağıdaki bloklar 16 Kasım'da çalıştırıldı; yeniden çalıştırma.

```powershell
# 18.1.0 — yarıda kalan birleştirme → f35aa2c
cd D:\Projects\davetkart\davetkart-frontent
git add package.json
git add package-lock.json
git commit -m "Merge main (47aedc8 dependency cleanup) into faz-18-audit-fixes"
```

```powershell
# 18.1.1 → 5b4ae25
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-ops-01-release-alignment
git add tests/Feature/TemplateCatalogueTest.php
git commit -m "18.1.1 - style(tests): Apply Pint class element order to TemplateCatalogueTest"
```

```powershell
# 18.1.2 → 700785d
git add app/Console/Commands/ExportPlanRules.php
git add contracts/plan-rules.json
git add tests/Feature/PlanRulesContractTest.php
git add composer.json
git add docs/rehber/app/Console/Commands/ExportPlanRules.md
git add docs/rehber/tests/Feature/PlanRulesContractTest.md
git add docs/rehber/PROJE-KOMUTLARI.md
git add docs/rehber/kavramlar/komutlar.md
git add README.md
git commit -m "18.1.2 - feat(contracts): Export plan rules to contracts/plan-rules.json and gate on plans:export"
```

```powershell
# 18.1.3 → d941945
git add deploy/deploy.sh
git add deploy/deploy-frontend.sh
git add docs/rehber/deploy/deploy.md
git add docs/rehber/deploy/deploy-frontend.md
git commit -m "18.1.3 - feat(deploy): Log the release tag and warn on untagged or mismatched releases"
```

```powershell
# 18.1.4 → 660c5b3, ardından birleştirme → 162c985
git add docs/rehber/fazlar/FAZ-18.md
git add docs/rehber/fazlar/README.md
git commit -m "18.1.4 - docs(phases): Record Phase 18.1 (OPS-01 release alignment)"
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-16-ops-01-release-alignment -m "Merge OPS-01 fix into faz-18-audit-fixes"
```

```powershell
# 18.1.6 → 6fba0f0 (docs; sekiz dosya)
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-16-faz-18-audit-fixes
git commit -m "docs: Update CHANGELOG.md for Phase 18.1 `OPS-01` records and related documentation"
```
