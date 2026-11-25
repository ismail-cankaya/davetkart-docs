# Faz 19 ortak düzeltme — Hat A açık kalanları (`HAT-A-ACIK-KALANLAR.md`) commit komutları

> **Tarih:** 25 Kasım 2026 · **Hat:** A · **Girdi:** [`HAT-A-ACIK-KALANLAR.md`](HAT-A-ACIK-KALANLAR.md) §1 (H2), §2 (E1–E9) · **Yeni karar:** K260, K261, K262
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

## 5. İkinci tur: E4, E7, E6, E5 (çalıştırıldı)

```powershell
cd D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel
# A-E4 — dal fix/2026-11-25-a-e4-attach-budget
git add app/Actions/Rsvp/ResolveGuestMediaAction.php
git add app/Actions/Rsvp/SubmitRsvpAction.php
git add app/Actions/Rsvp/UpdateRsvpAction.php
git add docs/rehber/app/Actions/Rsvp/ResolveGuestMediaAction.md
git add docs/rehber/app/Actions/Rsvp/SubmitRsvpAction.md
git add docs/rehber/app/Actions/Rsvp/UpdateRsvpAction.md
git add docs/rehber/fazlar/FAZ-19.md
git commit -m "A-E4 - fix(rsvp): Recheck the guest byte budget under the invitation lock when a pending upload is attached"
git add tests/Feature/MediaTest.php
git commit -m "A-E4 - test(media): Lock the attach-time guest budget and the replaced photo exclusion"

# A-E7 — dal fix/2026-11-25-a-e7-env-key-compare
git add app/Console/Commands/CheckEnvTemplate.php
git add docs/rehber/app/Console/Commands/CheckEnvTemplate.md
git commit -m "A-E7 - feat(ops): Compare a real .env file with the production template by keys only"
git add tests/Feature/ProductionConfigTest.php
git commit -m "A-E7 - test(ops): Lock the key-only .env comparison and keep values out of the output"

# A-E6 — dal fix/2026-11-25-a-e6-move-media-disk
git add app/Console/Commands/MoveMediaDisk.php
git add docs/rehber/app/Console/Commands/MoveMediaDisk.md
git add docs/rehber/fazlar/FAZ-19.md
git commit -m "A-E6 - feat(media): Add a command that moves media files between disks and repoints their rows"
git add tests/Feature/MoveMediaDiskTest.php
git commit -m "A-E6 - test(media): Lock the disk move, the missing file report and the cache refresh"

# A-E5 — dal fix/2026-11-25-a-e5-buyer-phone
git add database/migrations/2026_11_25_110000_add_buyer_phone_to_orders_table.php
git add docs/rehber/database/migrations/2026_11_25_110000_add_buyer_phone_to_orders_table.md
git add app/Services/Payment/RequiresBuyerPhone.php
git add docs/rehber/app/Services/Payment/RequiresBuyerPhone.md
git add app/Http/Requests/Payment/StoreCheckoutRequest.php
git add docs/rehber/app/Http/Requests/Payment/StoreCheckoutRequest.md
git add app/Actions/Payment/StartCheckoutAction.php
git add docs/rehber/app/Actions/Payment/StartCheckoutAction.md
git add app/Http/Controllers/Api/V1/PaymentController.php
git add docs/rehber/app/Http/Controllers/Api/V1/PaymentController.md
git add app/Services/Payment/ShopierGateway.php
git add docs/rehber/app/Services/Payment/ShopierGateway.md
git add config/payment.php
git add docs/rehber/config/payment.md
git add docs/rehber/fazlar/FAZ-19.md
git commit -m "A-E5 - feat(payment): Ask the buyer's mobile phone at checkout and send it to Shopier instead of a placeholder (K262)"
git add app/Actions/Auth/DeleteAccountAction.php
git add docs/rehber/app/Actions/Auth/DeleteAccountAction.md
git add tests/Feature/AccountDeletionTest.php
git commit -m "A-E5 - fix(accounts): Drop the buyer phone from anonymous orders when an account is deleted"
git add tests/Feature/CheckoutBuyerPhoneTest.php
git add tests/Feature/ShopierGatewayTest.php
git add tests/Feature/PaymentDriverResolutionTest.php
git commit -m "A-E5 - test(payment): Lock the buyer phone rules at checkout and in the Shopier form"
git status --short

cd D:\Projects\davetkart-hat-a\davetkart-frontent
# A-E5 — dal fix/2026-11-25-a-e5-buyer-phone
git add src/utils/trMobile.ts
git add docs/rehber/src/utils/trMobile.md
git add src/types.ts
git add src/services/payments.ts
git add docs/rehber/src/services/payments.md
git add src/stores/useCheckoutStore.ts
git add docs/rehber/src/stores/useCheckoutStore.md
git add src/components/payment/checkout/CardPaymentForm.tsx
git add docs/rehber/src/components/payment/checkout/CardPaymentForm.md
git add src/locales/tr/translation.json
git add src/locales/en/translation.json
git commit -m "A-E5 - feat(checkout): Ask the buyer's mobile phone on the card payment form (K262)"
git add src/pages/legal/PrivacyPage.tsx
git add docs/rehber/src/pages/legal/PrivacyPage.md
git commit -m "A-E5 - docs(privacy): List the buyer phone in the Shopier row of the privacy policy"
git add scripts/verify-payment.ts
git commit -m "A-E5 - test(verify): Lock the phone normalisation and the checkout body"
git status --short

cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-25-a-e4-attach-budget -m "Merge A-E4 into faz-19-fix"
git merge --no-ff fix/2026-11-25-a-e7-env-key-compare -m "Merge A-E7 into faz-19-fix"
git merge --no-ff fix/2026-11-25-a-e6-move-media-disk -m "Merge A-E6 into faz-19-fix"
git merge --no-ff fix/2026-11-25-a-e5-buyer-phone -m "Merge A-E5 into faz-19-fix"
cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-25-a-e5-buyer-phone -m "Merge A-E5 into faz-19-fix"

cd D:\Projects\davetkart-hat-a\davetkart-docs
# dal docs/2026-11-25-hat-a-fixes-2
git add decisions/DECISION-INDEX.md
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md
git add notes/04-SHOPIER-ALICI-ALANLARI-SORUSU.md
git add phases/faz-19/HAT-A-ACIK-KALANLAR.md
git add phases/faz-19/FAZ-19-HAT-A-FIX-COMMIT-KOMUTLARI.md
git add CHANGELOG.md
git commit -m "docs(faz-19): Record the second round of Hat A fixes and K262"
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-25-hat-a-fixes-2 -m "Merge Hat A second round into docs/2026-11-20-faz-19-audit-fixes"
```

## 6. Canlıya çıkarken, ikinci tur (İsmail)

```bash
php artisan migrate                                   # K262: orders.buyer_phone
php artisan env:template --env=.env --check          # E7: sunucu .env anahtarları ↔ şablon
php artisan media:move-disk --dry-run                # E6: public'te kalan medya
php artisan media:move-disk                          # kopyala + satırları çevir
php artisan media:move-disk --delete-source          # doğruladıktan sonra kaynağı sil
```