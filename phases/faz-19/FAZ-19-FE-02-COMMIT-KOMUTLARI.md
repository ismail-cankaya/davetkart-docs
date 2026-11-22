# Faz 19.21 — `FE-02` commit komutları

## Beklenen `git status --short --untracked-files=all`

**`D:\Projects\davetkart-hat-b\davetkart-frontent`** (`fix/2026-11-20-fe-02-error-boundary`)

```
 M docs/rehber/scripts/verify-render.md
 M scripts/verify-render.tsx
 M src/App.tsx
 M src/locales/en/translation.json
 M src/locales/tr/translation.json
 M src/main.tsx
?? docs/rehber/src/components/errors/RouteError.md
?? docs/rehber/src/routes.md
?? docs/rehber/src/utils/preloadRecovery.md
?? src/components/errors/RouteError.tsx
?? src/routes.tsx
?? src/utils/preloadRecovery.ts
```

**`D:\Projects\davetkart-hat-b\davetkart-docs`** (`docs/2026-11-20-fe-02-error-boundary`)

```
?? phases/faz-19/FAZ-19-FE-02-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-21-FE-02.md
```

Backend: değişiklik yok.

## 19.21.1 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/routes.tsx
git add src/App.tsx
git add src/components/errors/RouteError.tsx
git add src/locales/tr/translation.json
git add src/locales/en/translation.json
git add docs/rehber/src/routes.md
git add docs/rehber/src/components/errors/RouteError.md
git commit -m "19.21.1 - feat(routes): Add branded route error boundaries for pages, editor and guest page"
git status --short
```

## 19.21.2 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/utils/preloadRecovery.ts
git add src/main.tsx
git add docs/rehber/src/utils/preloadRecovery.md
git commit -m "19.21.2 - feat(app): Reload once when a lazy chunk fails to load"
git status --short
```

## 19.21.3 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add scripts/verify-render.tsx
git add docs/rehber/scripts/verify-render.md
git commit -m "19.21.3 - test(verify): Cover route error boundaries and preload recovery in verify:render"
git status --short
```

## 19.21.4 — docs

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-docs
git add phases/faz-19/kayit/19-21-FE-02.md
git add phases/faz-19/FAZ-19-FE-02-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add 19.21 FE-02 record and commit commands (K222-K223)"
git status --short
```

## Birleştirme — ana klasör

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-20-fe-02-error-boundary -m "Merge FE-02 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-20-fe-02-error-boundary -m "Merge FE-02 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `prompts/faz-19-agent/19-CAKISMA.md`.
