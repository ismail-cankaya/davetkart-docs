# Faz 19.22 — `TST-04` commit komutları

## Beklenen `git status --short --untracked-files=all`

**`D:\Projects\davetkart-hat-b\davetkart-frontent`** (`fix/2026-11-22-tst-04-e2e`)

```
 M .gitignore
 M package-lock.json
 M package.json
 M vite.config.ts
?? .github/workflows/e2e.yml.example
?? docs/rehber/e2e/README.md
?? docs/rehber/playwright.config.md
?? docs/rehber/scripts/e2e/backend.md
?? e2e/guest-rsvp.spec.ts
?? e2e/paywall-after-publish.spec.ts
?? e2e/publish-with-gift-code.spec.ts
?? e2e/support/flows.ts
?? e2e/support/state.ts
?? playwright.config.ts
?? scripts/e2e/backend.ps1
```

**`D:\Projects\davetkart-hat-b\davetkart-docs`** (`docs/2026-11-22-tst-04-e2e`)

```
?? phases/faz-19/FAZ-19-TST-04-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-22-TST-04.md
```

Backend: değişiklik yok (19.22.5 atlandı; `fix/2026-11-22-tst-04-e2e` boş dal).

## 19.22.1 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add package.json
git add package-lock.json
git add playwright.config.ts
git add vite.config.ts
git add .gitignore
git add docs/rehber/playwright.config.md
git commit -m "19.22.1 - build(e2e): Add Playwright with a Chromium config and npm run e2e"
git status --short
```

## 19.22.2 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add scripts/e2e/backend.ps1
git add docs/rehber/scripts/e2e/backend.md
git commit -m "19.22.2 - build(e2e): Add a one-command backend setup on a fresh e2e database"
git status --short
```

## 19.22.3 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add e2e/support/state.ts
git add e2e/support/flows.ts
git add e2e/publish-with-gift-code.spec.ts
git add e2e/guest-rsvp.spec.ts
git add e2e/paywall-after-publish.spec.ts
git add docs/rehber/e2e/README.md
git commit -m "19.22.3 - test(e2e): Cover publish with a gift code, guest RSVP and the post-publish paywall"
git status --short
```

## 19.22.4 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add .github/workflows/e2e.yml.example
git commit -m "19.22.4 - ci(e2e): Add a draft e2e workflow"
git status --short
```

## 19.22.6 — docs

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-docs
git add phases/faz-19/kayit/19-22-TST-04.md
git add phases/faz-19/FAZ-19-TST-04-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add 19.22 TST-04 record and commit commands (K224-K225)"
git status --short
```

## Birleştirme — ana klasör

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-22-tst-04-e2e -m "Merge TST-04 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-22-tst-04-e2e -m "Merge TST-04 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `prompts/faz-19-agent/19-CAKISMA.md`.
