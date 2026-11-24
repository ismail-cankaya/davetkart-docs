# Faz 19.19 — `FE-52` commit komutları

## Beklenen durum

**`D:\Projects\davetkart-hat-b\davetkart-frontent`** (`fix/2026-11-24-fe-52-pricing-faq`): ` M` 7 dosya (19.19.1 + 19.19.2 listeleri).

**`D:\Projects\davetkart-hat-b\davetkart-docs`** (`docs/2026-11-24-fe-52-pricing-faq`): `??` kayıt + bu dosya. Backend değişmedi.

Sıra: frontend → docs.

## 19.19.1 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/legal/retention.ts
git add src/pages/PricingPage.tsx
git add src/pages/legal/PrivacyPage.tsx
git add docs/rehber/src/pages/PricingPage.md
git add docs/rehber/src/legal/retention.md
git commit -m "19.19.1 - fix(pricing): Stop promising a publication period and paid extension in the FAQ"
git status --short
```

## 19.19.2 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add scripts/verify-render.tsx
git add docs/rehber/scripts/verify-render.md
git commit -m "19.19.2 - test(verify): Lock the pricing FAQ against publication period promises"
git status --short
```

## 19.19.3 — docs

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-docs
git add phases/faz-19/kayit/19-19-FE-52.md
git add phases/faz-19/FAZ-19-FE-52-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add 19.19 FE-52 record and commit commands (K232)"
git status --short
```

## Birleştirme — ana klasör

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-24-fe-52-pricing-faq -m "Merge FE-52 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-24-fe-52-pricing-faq -m "Merge FE-52 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `prompts/faz-19-agent/19-CAKISMA.md`.
