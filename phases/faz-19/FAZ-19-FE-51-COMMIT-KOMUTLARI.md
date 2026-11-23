# 19.12 `FE-51` — commit komutları

> ⚠️ Backend dalı TST-02 dalının üstünde (zincir: ARC-04 → OPS-04 → SEC-06 → TST-02 → FE-51). Frontend dalı `faz-19-audit-fixes`'ten.
> ⚠️ Docs: önce **SEC-10 docs commit'ini** at (`FAZ-19-SEC-10-COMMIT-KOMUTLARI.md`), sonra aşağıdaki 19.12.6 bloğu FE-51 docs dalını açar.
> ⚠️ Backend `composer check` PHPStan adımında kırmızı: `ResolvesRefundRequests.php:29` (bu bulgunun dışında).

## Beklenen `git status --short --untracked-files=all`

**davetkart-backend-php-laravel** (`fix/2026-11-23-fe-51-guest-media-upload`)

```
 M app/Actions/Media/StoreGuestMediaAction.php
 M app/Http/Resources/PublicInvitationResource.php
 M config/davetkart.php
 M docs/10-URETIM-ENV-SABLONU.md
 M docs/rehber/app/Actions/Media/StoreGuestMediaAction.md
 M docs/rehber/app/Http/Resources/PublicInvitationResource.md
 M docs/rehber/config/davetkart.md
 M tests/Feature/MediaDiskGuardTest.php
 M tests/Feature/MediaTest.php
 M tests/Feature/PublicInvitationTest.php
 M tests/Feature/RateLimitTest.php
```

**davetkart-frontent** (`fix/2026-11-23-fe-51-guest-media-upload`)

```
 M docs/rehber/scripts/verify-render.md
 M docs/rehber/src/components/templates/yedi-davetiye-acik-isler.md
 M docs/rehber/src/pages/InvitePage.md
 M docs/rehber/src/services/media.md
 M docs/rehber/src/services/publicInvitation.md
 M docs/rehber/src/services/rsvpReceipts.md
 M scripts/i18n-baseline.json
 M scripts/onizleme/main.tsx
 M scripts/verify-endpoints.ts
 M scripts/verify-render.tsx
 M src/components/preview/DeviceSimulator.tsx
 D src/components/preview/RsvpModal.tsx
 M src/components/templates/TemplateRenderer.tsx
 M src/components/templates/types.ts
 M src/data.ts
 M src/pages/InvitePage.tsx
 M src/services/media.ts
 M src/services/publicInvitation.ts
 M src/stores/useRsvpStore.ts
 M src/stores/useUIStore.ts
 M src/types.ts
```

**davetkart-docs** (SEC-10 commit'inden sonra; şu an `docs/2026-11-22-sec-10-shopier-buyer-fields`)

```
?? phases/faz-19/FAZ-19-FE-51-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-12-FE-51.md
```

## 19.12.1 — backend: misafir yükleme bayrağı (D1)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add config/davetkart.php
git add app/Actions/Media/StoreGuestMediaAction.php
git add docs/10-URETIM-ENV-SABLONU.md
git add docs/rehber/app/Actions/Media/StoreGuestMediaAction.md
git add docs/rehber/config/davetkart.md
git add tests/Feature/MediaTest.php
git add tests/Feature/MediaDiskGuardTest.php
git add tests/Feature/RateLimitTest.php
git commit -m "19.12.1 - fix(media): Put guest uploads behind a flag that is off by default (K189)"
git status --short
```

## 19.12.2 — backend: bayrak public davetiye yanıtında (D3)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
git add app/Http/Resources/PublicInvitationResource.php
git add docs/rehber/app/Http/Resources/PublicInvitationResource.md
git add tests/Feature/PublicInvitationTest.php
git commit -m "19.12.2 - feat(invitations): Publish the guest upload flag in the public invitation (K189)"
git status --short
```

## 19.12.4 — frontend: ölü misafir yükleme kodunu kaldır (D1 + D3)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-frontent
git add src/components/preview/RsvpModal.tsx
git add src/components/preview/DeviceSimulator.tsx
git add src/components/templates/TemplateRenderer.tsx
git add src/components/templates/types.ts
git add src/pages/InvitePage.tsx
git add src/stores/useUIStore.ts
git add src/stores/useRsvpStore.ts
git add src/types.ts
git add src/data.ts
git add src/services/media.ts
git add src/services/publicInvitation.ts
git add scripts/onizleme/main.tsx
git add scripts/verify-endpoints.ts
git add scripts/i18n-baseline.json
git add docs/rehber/src/pages/InvitePage.md
git add docs/rehber/src/services/media.md
git add docs/rehber/src/services/publicInvitation.md
git add docs/rehber/src/services/rsvpReceipts.md
git add docs/rehber/src/components/templates/yedi-davetiye-acik-isler.md
git commit -m "19.12.4 - fix(rsvp): Remove the unreachable guest upload modal and read the flag from the server (K189)"
git status --short
```

(`git add` silinen dosyanın silinmesini de sahneler.)

## 19.12.5 — frontend: `verify:render` vakası

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-frontent
git add scripts/verify-render.tsx
git add docs/rehber/scripts/verify-render.md
git commit -m "19.12.5 - test(rsvp): Assert the guest page draws no file field while uploads are off (K189)"
git status --short
```

## 19.12.6 — docs: kayıt ve commit komutları (SEC-10 commit'inden SONRA)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-docs
git switch -c docs/2026-11-23-fe-51-guest-media-upload
git add phases/faz-19/kayit/19-12-FE-51.md
git add phases/faz-19/FAZ-19-FE-51-COMMIT-KOMUTLARI.md
git commit -m "docs(decisions): Add K189 record and commit commands for FE-51"
git status --short
```

## Birleştirme (ana klasör; backend TST-02'den, docs SEC-10'dan SONRA)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-23-fe-51-guest-media-upload -m "Merge FE-51 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-23-fe-51-guest-media-upload -m "Merge FE-51 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-23-fe-51-guest-media-upload -m "Merge FE-51 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md`.
