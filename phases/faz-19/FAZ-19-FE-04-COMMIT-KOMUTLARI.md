# Faz 19.23 — `FE-04` commit komutları

## Beklenen durum

**`D:\Projects\davetkart-hat-b\davetkart-backend-php-laravel`** (`fix/2026-11-23-fe-04-share-preview`): ` M` 7, `??` 11 (19.23.1 + 19.23.2 listeleri).

**`D:\Projects\davetkart-hat-b\davetkart-frontent`** (`fix/2026-11-23-fe-04-share-preview`): ` M index.html`, `?? docs/rehber/index.html.md`.

**`D:\Projects\davetkart-hat-b\davetkart-docs`** (`docs/2026-11-23-fe-04-share-preview`): `??` kayıt + bu dosya. 19.23.3 (kayıt) docs adımına katıldı.

Sıra: backend → frontend → docs.

## 19.23.1 — backend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-backend-php-laravel
git add app/Actions/Invitation/PublicInvitationPayloadAction.php
git add app/Actions/Invitation/BuildSharePreviewAction.php
git add app/Http/Controllers/SharePreviewController.php
git add resources/views/share-preview.blade.php
git add routes/web.php
git add bootstrap/app.php
git add config/davetkart.php
git add app/Http/Controllers/Api/V1/PublicInvitationController.php
git add tests/Feature/SharePreviewTest.php
git add docs/rehber/app/Actions/Invitation/PublicInvitationPayloadAction.md
git add docs/rehber/app/Actions/Invitation/BuildSharePreviewAction.md
git add docs/rehber/app/Http/Controllers/SharePreviewController.md
git add docs/rehber/app/Http/Controllers/Api/V1/PublicInvitationController.md
git add docs/rehber/tests/Feature/SharePreviewTest.md
git commit -m "19.23.1 - feat(share): Serve an Open Graph preview page for published invitations to link bots"
git status --short
```

## 19.23.2 — backend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-backend-php-laravel
git add deploy/nginx/davetkart.conf
git add deploy/smoke/check-share-preview.sh
git add docs/rehber/deploy/nginx/davetkart.md
git add docs/rehber/deploy/smoke/check-share-preview.md
git commit -m "19.23.2 - feat(nginx): Route link preview bots on /invite/ to the preview page"
git status --short
```

## 19.23.4 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add index.html
git add docs/rehber/index.html.md
git commit -m "19.23.4 - feat(seo): Add site-wide Open Graph and description tags"
git status --short
```

## 19.23.5 — docs

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-docs
git add phases/faz-19/kayit/19-23-FE-04.md
git add phases/faz-19/FAZ-19-FE-04-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add 19.23 FE-04 record and commit commands (K230)"
git status --short
```

## Birleştirme — ana klasör

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-23-fe-04-share-preview -m "Merge FE-04 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-23-fe-04-share-preview -m "Merge FE-04 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-23-fe-04-share-preview -m "Merge FE-04 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `prompts/faz-19-agent/19-CAKISMA.md`.
