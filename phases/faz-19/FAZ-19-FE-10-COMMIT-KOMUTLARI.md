# Faz 19.24 — `FE-10` commit komutları

## Beklenen durum

**`D:\Projects\davetkart-hat-b\davetkart-frontent`** (`fix/2026-11-23-fe-10-bundle-split`): ` M` 18 dosya, `??` 4 dosya (`src/templateCatalog.ts`, `scripts/verify-bundle.ts`, iki kılavuz).

**`D:\Projects\davetkart-hat-b\davetkart-docs`** (`docs/2026-11-23-fe-10-bundle-split`): `??` kayıt + bu dosya. Backend: değişiklik yok.

19.24.3 (D3) 19.24.1'e katıldı (`TemplateRenderer.tsx` iki değişikliği de taşıyor).

## 19.24.1 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/templateCatalog.ts
git add src/data.ts
git add src/components/templates/TemplateRenderer.tsx
git add src/stores/useInvitationStore.ts
git add src/stores/useSubscriptionStore.ts
git add src/components/create/CategoryStep.tsx
git add src/components/create/ThemeStep.tsx
git add src/components/editor/DesignerPanel.tsx
git add src/components/preview/TemplateGrid.tsx
git add src/pages/DashboardPage.tsx
git add src/pages/InvitePage.tsx
git add scripts/onizleme/main.tsx
git add scripts/verify-payment.ts
git add scripts/verify-plan-rules.ts
git add scripts/verify-render.tsx
git add docs/rehber/src/templateCatalog.md
git add docs/rehber/src/components/templates/TemplateRenderer.md
git commit -m "19.24.1 - perf(templates): Lazy-load each template and split the template catalog out of data.ts"
git status --short
```

## 19.24.2 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/pages/HomePage.tsx
git commit -m "19.24.2 - perf(home): Lazy-load the live preview section"
git status --short
```

## 19.24.4 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add scripts/verify-bundle.ts
git add package.json
git add docs/rehber/scripts/verify-bundle.md
git commit -m "19.24.4 - test(verify): Add a bundle budget check to npm run check"
git status --short
```

## 19.24.5 — docs

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-docs
git add phases/faz-19/kayit/19-24-FE-10.md
git add phases/faz-19/FAZ-19-FE-10-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add 19.24 FE-10 record and commit commands (K227)"
git status --short
```

## Birleştirme — ana klasör

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-23-fe-10-bundle-split -m "Merge FE-10 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-23-fe-10-bundle-split -m "Merge FE-10 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `prompts/faz-19-agent/19-CAKISMA.md`.
