# Faz 19.27 — `FE-54` commit komutları

## Beklenen durum

**`D:\Projects\davetkart-hat-b\davetkart-frontent`** (`fix/2026-11-23-fe-54-accessibility`): ` M` 15 dosya, `??` `e2e/a11y.spec.ts`, `docs/rehber/e2e/a11y.md` (+ yoksa `docs/rehber/src/components/ui/Toast.md`).

**`D:\Projects\davetkart-hat-b\davetkart-docs`** (`docs/2026-11-23-fe-54-accessibility`): `??` kayıt + bu dosya. Backend: değişiklik yok.

## 19.27.1 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/components/ui/Toast.tsx
git add scripts/verify-render.tsx
git add docs/rehber/src/components/ui/Toast.md
git commit -m "19.27.1 - fix(a11y): Announce toasts through always-present live regions"
git status --short
```

## 19.27.2 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/components/layout/Footer.tsx
git add src/pages/PricingPage.tsx
git add src/pages/DashboardPage.tsx
git add src/components/layout/Header.tsx
git add src/components/legal/LegalPageLayout.tsx
git add src/index.css
git add src/components/templates/shared/Envelope.tsx
git add src/locales/tr/translation.json
git add src/locales/en/translation.json
git add docs/rehber/e2e/a11y.md
git commit -m "19.27.2 - fix(a11y): Raise text contrast to WCAG AA and label the main navigation"
git status --short
```

## 19.27.3 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/pages/InvitePage.tsx
git commit -m "19.27.3 - fix(a11y): Wrap the guest page in a main landmark"
git status --short
```

## 19.27.4 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add package.json
git add package-lock.json
git add e2e/a11y.spec.ts
git add playwright.config.ts
git add docs/rehber/e2e/README.md
git commit -m "19.27.4 - test(e2e): Add an axe scan of 14 pages to npm run e2e"
git status --short
```

## 19.27.5 — docs

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-docs
git add phases/faz-19/kayit/19-27-FE-54.md
git add phases/faz-19/FAZ-19-FE-54-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add 19.27 FE-54 record and commit commands (K229)"
git status --short
```

## Birleştirme — ana klasör

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-23-fe-54-accessibility -m "Merge FE-54 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-23-fe-54-accessibility -m "Merge FE-54 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `prompts/faz-19-agent/19-CAKISMA.md`.
