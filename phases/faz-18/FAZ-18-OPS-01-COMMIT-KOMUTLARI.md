# Faz 18.1 — `OPS-01` commit komutları

> **Tarih:** 16 Kasım 2026 · **Kararlar:** K146–K150 · **Faz kaydı:** backend `docs/rehber/fazlar/FAZ-18.md` §18.1
> Her blok bir commit. Blokları **sırayla** çalıştır: önce §0, sonra backend → frontend → docs → birleştirme.
> Dosyalar tek tek, açık yolla eklenir; joker, klasör yolu ve `-A` yok (frontend'de CRLF tuzağı).
> Her blok `git status --short` ile biter: o adımın dosyası listede kalmamalı.

## 0. Önce: frontend birleştirmesini tamamla (18.1.0)

§A'daki `git merge --no-ff origin/main` `package.json` ve `package-lock.json`'da çakıştı. Çakışma çözüldü
(`47aedc8`'in temizliği + dalın `three` / `@react-three/fiber` / `@types/three` eklemeleri), kilit
`npm install` ile yeniden üretildi; `npm ci` ve `npm run check` çıkış 0 verdi.

```powershell
# 18.1.0 — yarıda kalan birleştirmeyi commit'le
cd D:\Projects\davetkart\davetkart-frontent
git branch --show-current                            # faz-18-audit-fixes olmalı
git add package.json
git add package-lock.json
git commit -m "Merge main (47aedc8 dependency cleanup) into faz-18-audit-fixes"
git status --short                                   # yalnızca 18.1.5'in '??' dosyaları kalır
```

⛔ **Bu commit'ten sonra dur ve Claude'a "devam" yaz.** Frontend düzeltme dalı
(`fix/2026-11-16-ops-01-release-alignment`) ancak bu commit'in üstüne açılabilir; `package.json`'a
`verify:plans` satırı ve son `npm ci` + `npm run check` o zaman yapılır. 18.1.5'in diğer dört dosyası
çalışma ağacında hazır bekliyor (izlenmeyen dosyalar; birleştirme commit'ine girmezler).

## 1. Backend — `fix/2026-11-16-ops-01-release-alignment`

```powershell
# 18.1.1 — TST-01: Pint'in istediği sıra (sabit, metotlardan önce)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-ops-01-release-alignment
git add tests/Feature/TemplateCatalogueTest.php
git commit -m "18.1.1 - style(tests): Apply Pint class element order to TemplateCatalogueTest"
git status --short
```

```powershell
# 18.1.2 — plans:export + contracts/plan-rules.json + test + composer check zinciri
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-ops-01-release-alignment
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
git status --short
```

```powershell
# 18.1.3 — deploy betikleri: yayınlanan commit'in etiketi günlüğe, etiketsiz/farklı etiket uyarı
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-ops-01-release-alignment
git add deploy/deploy.sh
git add deploy/deploy-frontend.sh
git add docs/rehber/deploy/deploy.md
git add docs/rehber/deploy/deploy-frontend.md
git commit -m "18.1.3 - feat(deploy): Log the release tag and warn on untagged or mismatched releases"
git status --short
```

```powershell
# 18.1.4 — faz kaydı
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-ops-01-release-alignment
git add docs/rehber/fazlar/FAZ-18.md
git add docs/rehber/fazlar/README.md
git commit -m "18.1.4 - docs(phases): Record Phase 18.1 (OPS-01 release alignment)" 
git status --short                                   # boş olmalı
```

## 2. Frontend — `fix/2026-11-16-ops-01-release-alignment`

⛔ **Önkoşul:** §0 commit'i atıldı **ve** Claude 18.1.5'i bitirdi (dal açıldı, `package.json` güncellendi,
`npm run check` yeşil). Öncesinde bu blok `package.json`'ı değişmemiş bulur ve eksik bir commit üretir.
🔴 `git add -A` yasak.

```powershell
# 18.1.5 — verify:plans: sözleşme kopyası + okuyucu + betik + verify zinciri
cd D:\Projects\davetkart\davetkart-frontent
git switch fix/2026-11-16-ops-01-release-alignment
git add src/contracts/plan-rules.json
git add src/contracts/planRules.ts
git add scripts/verify-plan-rules.ts
git add package.json
git add docs/rehber/scripts/verify-plan-rules.md
git commit -m "18.1.5 - feat(verify): Check plan rules against the backend contract (verify:plans)"
git status --short                                   # yalnızca '?? .claude/' olabilir
```

## 3. Docs — `docs/2026-11-16-faz-18-audit-fixes`

```powershell
# 18.1.6 — çalıştırma kitabı, K146–K150, takip tablosu
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-16-faz-18-audit-fixes
git add operations/deployment/YAYIN-SIRASI.md
git add operations/README.md
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md
git add decisions/DECISION-INDEX.md
git add decisions/README.md
git add phases/faz-18/README.md
git add phases/faz-18/FAZ-18-OPS-01-COMMIT-KOMUTLARI.md
git add CHANGELOG.md
git commit -m "docs(faz-18): Add release order runbook and K146-K150 for OPS-01"
git status --short                                   # boş olmalı
```

## 4. Birleştirme — düzeltme dalları → `faz-18-audit-fixes`

```powershell
# Backend
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-16-ops-01-release-alignment -m "Merge OPS-01 fix into faz-18-audit-fixes"
git status --short
# git push -u origin faz-18-audit-fixes
# git push -u origin fix/2026-11-16-ops-01-release-alignment
```

```powershell
# Frontend (§2'den sonra)
cd D:\Projects\davetkart\davetkart-frontent
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-16-ops-01-release-alignment -m "Merge OPS-01 fix into faz-18-audit-fixes"
git status --short
# git push -u origin faz-18-audit-fixes
# git push -u origin fix/2026-11-16-ops-01-release-alignment
```

```powershell
# Docs (isteğe bağlı)
# cd D:\Projects\davetkart\davetkart-docs
# git push -u origin docs/2026-11-16-faz-18-audit-fixes
```

Sonraki prompt (18.2, `OPS-02`) backend'de `git branch --merged faz-18-audit-fixes | Select-String "ops-01-"`
ile bu birleştirmeyi arar.

## 5. Etiket

Bu fazda **atılmaz.** `v1.1.0` Faz 18 sonunda, 18.6 §11'deki dört komut yeşilken atılır; komutlar
[`operations/deployment/YAYIN-SIRASI.md`](../../operations/deployment/YAYIN-SIRASI.md) §3'te.
