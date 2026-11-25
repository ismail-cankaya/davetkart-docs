# Faz 19 ortak düzeltme — Hat B bilinen hataları (`HAT-B-ACIK-KALANLAR.md` §1) commit komutları

> **Tarih:** 25 Kasım 2026 · **Hat:** B · **Girdi:** [`HAT-B-ACIK-KALANLAR.md`](HAT-B-ACIK-KALANLAR.md) §1 (B-H1–B-H7) · **Yeni karar:** yok
> **Dallar:** her hata için ayrı dal, `faz-19-fix`'ten (`fix/2026-11-25-b-h<n>-<kısa-ad>`); docs `docs/2026-11-25-hat-b-fixes`.
> Birleştirme: kod → `faz-19-fix` (`--no-ff`), docs → `docs/2026-11-20-faz-19-audit-fixes`.
> Bütün blokları İsmail'in izniyle (25 Kasım) ajan çalıştırdı; dosya kayıt içindir. Sıra raporun önerdiği gibi: B-H7 → B-H1 → B-H2 → B-H3 → B-H5 → B-H6 → B-H4.

## 1. Backend (çalıştırıldı)

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-backend-php-laravel
# B-H7 — dal fix/2026-11-25-b-h7-phpstan-tmpdir
git add phpstan.neon
git add .gitignore
git add docs/rehber/phpstan.md
git commit -m "B-H7 - fix(phpstan): Keep the result cache inside each worktree"
# B-H1 — dal fix/2026-11-25-b-h1-phpstan-errors
git add app/Console/Commands/Concerns/ResolvesRefundRequests.php
git add docs/rehber/app/Console/Commands/Concerns/ResolvesRefundRequests.md
git commit -m "B-H1 - fix(refunds): Narrow the refund request id instead of casting it"
git add app/Console/Commands/CheckK18.php
git add app/Support/K18Inspector.php
git add tests/Feature/K18CheckTest.php
git commit -m "B-H1 - fix(k18): Narrow the k18:check inputs and keep the block list typed"
git add tests/Feature/ReadinessTest.php
git commit -m "B-H1 - test(health): Stub the failed queue job with a typed PHPUnit stub"
git status --short

cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-25-b-h7-phpstan-tmpdir -m "Merge B-H7 into faz-19-fix"
git merge --no-ff fix/2026-11-25-b-h1-phpstan-errors -m "Merge B-H1 into faz-19-fix"
git status --short
```

## 2. Frontend (çalıştırıldı)

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
# B-H2 — dal fix/2026-11-25-b-h2-rsvp-name-reset
git add e2e/support/flows.ts
git add e2e/guest-rsvp.spec.ts
git add docs/rehber/e2e/README.md
git commit -m "B-H2 - test(e2e): Wait for the envelope to unmount before filling the guest form"
# B-H3 — dal fix/2026-11-25-b-h3-paywall-dialog
git add src/hooks/useFocusTrap.ts
git add docs/rehber/src/hooks/useFocusTrap.md
git commit -m "B-H3 - feat(a11y): Add a focus trap hook for modal windows"
git add src/components/payment/PaywallModal.tsx
git add docs/rehber/src/components/payment/PaywallModal.md
git commit -m "B-H3 - fix(paywall): Announce the plan wall as a modal dialog and keep focus inside it"
git add e2e/paywall-after-publish.spec.ts
git commit -m "B-H3 - test(e2e): Check the open plan wall for dialog role, focus trap and axe"
git add src/components/payment/PaywallModal.tsx
git add docs/rehber/src/components/payment/PaywallModal.md
git commit -m "B-H3 - fix(paywall): Raise the contrast of locked plans and excluded features"
# B-H5 — dal fix/2026-11-25-b-h5-cookie-rsvp-receipt
git add src/services/rsvpReceipts.ts
git add src/pages/legal/CookiesPage.tsx
git add src/locales/tr/translation.json
git add src/locales/en/translation.json
git add docs/rehber/src/pages/legal/PrivacyPage.md
git commit -m "B-H5 - fix(legal): List the guest RSVP edit code in the cookie policy"
git add scripts/verify-render.tsx
git add docs/rehber/scripts/verify-render.md
git commit -m "B-H5 - test(verify): Lock the RSVP edit code row in the cookie policy"
# B-H6 — dal fix/2026-11-25-b-h6-font-guides (10 kılavuz, tek tek eklendi)
git add docs/rehber/src/components/templates/konsept/harita/fontlar.md
git add docs/rehber/src/components/templates/konsept/kitap/fontlar.md
git add docs/rehber/src/components/templates/konsept/sergi/fontlar.md
git add docs/rehber/src/components/templates/shared/paper/fontlar.md
git add docs/rehber/src/components/templates/oniki-etkilesimli-sablon.md
git add docs/rehber/src/components/templates/premium-videolu.md
git add docs/rehber/tasarim/HARITA-KONSEPTI.md
git add docs/rehber/tasarim/KAGIT-KONSEPTI.md
git add docs/rehber/tasarim/KITAP-KONSEPTI.md
git add docs/rehber/tasarim/SERGI-KONSEPTI.md
git commit -m "B-H6 - docs(fonts): Stop describing Google Fonts loading in the template guides"
# B-H4 — dal fix/2026-11-25-b-h4-heading-order
git add src/components/layout/Footer.tsx
git add src/pages/DashboardPage.tsx
git commit -m "B-H4 - fix(a11y): Stop skipping heading levels in the footer and the dashboard cards"
git add e2e/a11y.spec.ts
git add docs/rehber/e2e/a11y.md
git commit -m "B-H4 - test(e2e): Gate heading-order in the accessibility scan"
git status --short

cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-25-b-h2-rsvp-name-reset -m "Merge B-H2 into faz-19-fix"
git merge --no-ff fix/2026-11-25-b-h3-paywall-dialog -m "Merge B-H3 into faz-19-fix"
git merge --no-ff fix/2026-11-25-b-h5-cookie-rsvp-receipt -m "Merge B-H5 into faz-19-fix"
git merge --no-ff fix/2026-11-25-b-h6-font-guides -m "Merge B-H6 into faz-19-fix"
git merge --no-ff fix/2026-11-25-b-h4-heading-order -m "Merge B-H4 into faz-19-fix"
git status --short
```

## 3. Docs

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-docs
git add phases/faz-19/HAT-B-ACIK-KALANLAR.md
git add phases/faz-19/FAZ-19-HAT-B-FIX-COMMIT-KOMUTLARI.md
git add phases/faz-19/README.md
git add CHANGELOG.md
git commit -m "docs(faz-19): Record the Hat B fixes on the shared Faz 19 fix branch"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-25-hat-b-fixes -m "Merge Hat B fixes into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Push yapılmadı.
