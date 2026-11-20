# Faz 19.20 — `FE-01` commit komutları

## Beklenen `git status --short --untracked-files=all`

**`D:\Projects\davetkart-hat-b\davetkart-frontent`** (`fix/2026-11-20-fe-01-language-scope`)

```
 M docs/rehber/scripts/verify-render.md
 M package.json
 M scripts/render-env.ts
 M scripts/verify-render.tsx
 M src/components/LanguageSwitcher.tsx
 M src/i18n.ts
?? docs/rehber/scripts/verify-i18n.md
?? docs/rehber/src/i18n.md
?? scripts/i18n-baseline.json
?? scripts/verify-i18n.ts
```

**`D:\Projects\davetkart-hat-b\davetkart-docs`** (`docs/2026-11-20-fe-01-language-scope`)

```
?? phases/faz-19/FAZ-19-FE-01-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-20-FE-01.md
```

Backend: değişiklik yok.

## 19.20.1 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/i18n.ts
git add src/components/LanguageSwitcher.tsx
git add scripts/render-env.ts
git add scripts/verify-render.tsx
git add docs/rehber/src/i18n.md
git add docs/rehber/scripts/verify-render.md
git commit -m "19.20.1 - fix(i18n): Offer only tr and en and send stale stored languages to tr"
git status --short
```

## 19.20.2 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add scripts/verify-i18n.ts
git add scripts/i18n-baseline.json
git add package.json
git add docs/rehber/scripts/verify-i18n.md
git commit -m "19.20.2 - feat(verify): Add verify:i18n ratchet for embedded Turkish text"
git status --short
```

## 19.20.3 — docs

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-docs
git add phases/faz-19/kayit/19-20-FE-01.md
git add phases/faz-19/FAZ-19-FE-01-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add 19.20 FE-01 record and commit commands (K220-K221)"
git status --short
```

## Birleştirme — ana klasör

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-20-fe-01-language-scope -m "Merge FE-01 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-20-fe-01-language-scope -m "Merge FE-01 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `prompts/faz-19-agent/19-CAKISMA.md`.
