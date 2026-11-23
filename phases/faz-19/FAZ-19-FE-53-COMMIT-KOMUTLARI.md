# Faz 19.25 — `FE-53` commit komutları

## Beklenen durum

**`D:\Projects\davetkart-hat-b\davetkart-frontent`** (`fix/2026-11-23-fe-53-mobile-vitals`): ` M` 10 dosya, `??` 4 dosya (`playwright.perf.config.ts`, `e2e/perf/vitals.perf.ts`, `scripts/perf/server.mjs`, `docs/rehber/playwright.perf.config.md`).

**`D:\Projects\davetkart-hat-b\davetkart-docs`** (`docs/2026-11-23-fe-53-mobile-vitals`): `??` kayıt + bu dosya. Backend: değişiklik yok.

## 19.25.1 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add playwright.perf.config.ts
git add e2e/perf/vitals.perf.ts
git add scripts/perf/server.mjs
git add package.json
git add .gitignore
git add docs/rehber/playwright.perf.config.md
git add scripts/e2e/backend.ps1
git add e2e/support/flows.ts
git add docs/rehber/scripts/e2e/backend.md
git commit -m "19.25.1 - test(perf): Add npm run perf with mobile LCP and CLS budgets"
git status --short
```

## 19.25.2 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/styles/fonts.css
git add src/index.css
git add docs/rehber/src/styles/fonts.md
git commit -m "19.25.2 - perf(fonts): Add metric-matched fallback fonts to stop swap reflow"
git status --short
```

## 19.25.3 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/components/layout/AppLayout.tsx
git commit -m "19.25.3 - perf(layout): Reserve a screen for lazy pages so the footer does not shift"
git status --short
```

## 19.25.4 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/components/home/Hero.tsx
git commit -m "19.25.4 - perf(home): Load the hero video after the window load event"
git status --short
```

## 19.25.5 — docs

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-docs
git add phases/faz-19/kayit/19-25-FE-53.md
git add phases/faz-19/FAZ-19-FE-53-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add 19.25 FE-53 record and commit commands (K228)"
git status --short
```

## Birleştirme — ana klasör

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-23-fe-53-mobile-vitals -m "Merge FE-53 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-23-fe-53-mobile-vitals -m "Merge FE-53 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `prompts/faz-19-agent/19-CAKISMA.md`.
