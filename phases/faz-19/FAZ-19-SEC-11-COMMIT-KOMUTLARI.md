# Faz 19.18 — `SEC-11` commit komutları

## Beklenen durum

**`D:\Projects\davetkart-hat-b\davetkart-frontent`** (`fix/2026-11-24-sec-11-privacy-text`): ` M` src/pages/legal/PrivacyPage.tsx, docs/rehber/src/pages/legal/PrivacyPage.md, scripts/verify-render.tsx,
scripts/i18n-baseline.json, docs/rehber/scripts/verify-render.md · `??` src/legal/retention.ts, docs/rehber/src/legal/retention.md

**`D:\Projects\davetkart-hat-b\davetkart-docs`** (`docs/2026-11-24-sec-11-privacy-text`): `??` kayıt + bu dosya. Backend değişmedi.

Sıra: frontend → docs.

## 19.18.1 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/legal/retention.ts
git add docs/rehber/src/legal/retention.md
git commit -m "19.18.1 - feat(legal): Add the backup purge period constant"
git status --short
```

## 19.18.2 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/pages/legal/PrivacyPage.tsx
git add docs/rehber/src/pages/legal/PrivacyPage.md
git commit -m "19.18.2 - fix(legal): State backup retention and name the data processors in the privacy text"
git status --short
```

## 19.18.3 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add scripts/verify-render.tsx
git add scripts/i18n-baseline.json
git add docs/rehber/scripts/verify-render.md
git commit -m "19.18.3 - test(verify): Lock the backup period and processor names in verify-render"
git status --short
```

## 19.18.4 — docs

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-docs
git add phases/faz-19/kayit/19-18-SEC-11.md
git add phases/faz-19/FAZ-19-SEC-11-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add 19.18 SEC-11 record and commit commands (K231)"
git status --short
```

## Birleştirme — ana klasör

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-24-sec-11-privacy-text -m "Merge SEC-11 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-24-sec-11-privacy-text -m "Merge SEC-11 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `prompts/faz-19-agent/19-CAKISMA.md`.
