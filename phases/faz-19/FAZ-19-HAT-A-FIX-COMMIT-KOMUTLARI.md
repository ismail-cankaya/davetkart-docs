# Faz 19 ortak düzeltme — Hat A açık kalanları (`HAT-A-ACIK-KALANLAR.md`) commit komutları

> **Tarih:** 25 Kasım 2026 · **Hat:** A · **Girdi:** [`HAT-A-ACIK-KALANLAR.md`](HAT-A-ACIK-KALANLAR.md) §1 (H2), §2 (E1, E2, E3, E8, E9) · **Yeni karar:** K260, K261
> **Dallar:** her madde için ayrı dal, `faz-19-fix`'ten (`fix/2026-11-25-a-<id>-<kısa-ad>`); docs `docs/2026-11-25-hat-a-fixes`.
> Birleştirme: kod → `faz-19-fix` (`--no-ff`), docs → `docs/2026-11-20-faz-19-audit-fixes`.
> Bütün blokları İsmail'in izniyle (25 Kasım) ajan çalıştırdı; dosya kayıt içindir. Sıra: H2 → E3 → E8/E9 → E1 → E2.

## 1. Frontend (çalıştırıldı)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-frontent
# A-H2 — dal fix/2026-11-25-a-h2-draft-limit-message
git add src/types.ts
git add src/utils/draftContent.ts
git add src/stores/useInvitationStore.ts
git add src/components/create/EditorWorkspace.tsx
git add src/components/errors/RouteError.tsx
git add src/locales/tr/translation.json
git add src/locales/en/translation.json
git add docs/rehber/src/stores/useInvitationStore.md
git add docs/rehber/src/hooks/useInvitationAutoSave.md
git add docs/rehber/src/components/create/EditorWorkspace.md
git add docs/rehber/src/components/errors/RouteError.md
git commit -m "A-H2 - fix(editor): Show the draft limit message and stop auto-save from repeating the rejected save"
git add scripts/verify-editor-state.ts
git commit -m "A-H2 - test(verify): Lock the draft limit rejection in verify:state"
git status --short

cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-25-a-h2-draft-limit-message -m "Merge A-H2 into faz-19-fix"
git status --short
```

## 2. Backend (çalıştırıldı)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
# A-E3 — dal fix/2026-11-25-a-e3-guest-uploads-cache
git add app/Actions/Invitation/PublicInvitationPayloadAction.php
git add docs/rehber/app/Actions/Invitation/PublicInvitationPayloadAction.md
git add docs/rehber/app/Http/Resources/PublicInvitationResource.md
git add docs/rehber/fazlar/FAZ-19.md
git commit -m "A-E3 - fix(public): Read the guest upload flag on every request instead of freezing it in the cache"
git add tests/Feature/PublicInvitationTest.php
git commit -m "A-E3 - test(public): Lock the live guest upload flag behind a warm cache"

# A-E8 / A-E9 — dal fix/2026-11-25-a-e8-e9-tests
git add tests/Feature/LockRaceTest.php
git add docs/rehber/tests/Support/LockAssertions.md
git commit -m "A-E8 - test(locks): Prove the payment and claim locks with a real interleaving instead of a wait"
git add tests/Feature/InvitationTest.php
git add docs/rehber/app/Actions/Invitation/CreateInvitationAction.md
git commit -m "A-E9 - test(invitations): Drop the draft copy of the cross-user read test"
git add docs/rehber/fazlar/FAZ-19.md
git commit -m "A-E8 - docs(faz-19): Note the new lock interleaving tests and the removed duplicate test"

# A-E1 — dal fix/2026-11-25-a-e1-verify-existing-accounts
git add database/migrations/2026_11_25_100000_mark_existing_accounts_as_verified.php
git add docs/rehber/database/migrations/2026_11_25_100000_mark_existing_accounts_as_verified.md
git add docs/rehber/app/Support/VerifiedEmailGuard.md
git add docs/rehber/fazlar/FAZ-19.md
git commit -m "A-E1 - feat(accounts): Mark the accounts opened before email verification as verified (K260)"
git add tests/Feature/MarkExistingAccountsVerifiedMigrationTest.php
git commit -m "A-E1 - test(accounts): Lock which accounts the verification backfill marks"

# A-E2 — dal fix/2026-11-25-a-e2-prune-empty-drafts
git add app/Console/Commands/PruneEmptyDrafts.php
git add docs/rehber/app/Console/Commands/PruneEmptyDrafts.md
git add docs/rehber/app/Actions/Invitation/CreateInvitationAction.md
git add docs/rehber/fazlar/FAZ-19.md
git commit -m "A-E2 - feat(invitations): Add a one-off command that prunes old empty drafts (K261)"
git add tests/Feature/PruneEmptyDraftsTest.php
git commit -m "A-E2 - test(invitations): Lock which drafts the empty draft prune deletes"
git status --short

cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-25-a-e3-guest-uploads-cache -m "Merge A-E3 into faz-19-fix"
git merge --no-ff fix/2026-11-25-a-e8-e9-tests -m "Merge A-E8 and A-E9 into faz-19-fix"
git merge --no-ff fix/2026-11-25-a-e1-verify-existing-accounts -m "Merge A-E1 into faz-19-fix"
git merge --no-ff fix/2026-11-25-a-e2-prune-empty-drafts -m "Merge A-E2 into faz-19-fix"
git status --short
```

## 3. Docs (çalıştırıldı)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-docs
# dal docs/2026-11-25-hat-a-fixes
git add decisions/DECISION-INDEX.md
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md
git add phases/faz-19/HAT-A-ACIK-KALANLAR.md
git add phases/faz-19/FAZ-19-HAT-A-FIX-COMMIT-KOMUTLARI.md
git add phases/faz-19/README.md
git add CHANGELOG.md
git commit -m "docs(faz-19): Record the Hat A fixes and K260-K261 on the shared Faz 19 fix branch"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-25-hat-a-fixes -m "Merge Hat A fixes into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

## 4. Canlıya çıkarken (İsmail)

```powershell
php artisan migrate                                   # K260 göçü dahil
php artisan invitations:prune-empty-drafts --dry-run  # K261: önce say
php artisan invitations:prune-empty-drafts            # sonra sil
```
