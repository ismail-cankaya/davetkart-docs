# Faz 14 — commit komutları (frontend)

> Her blok bir commit. 🔴 Frontend deposunda `git add -A` YASAK (CRLF): dosyalar tek tek ekleniyor.
> Dosyalar `Claude outputs\f14\frontend\<adım>\` klasöründen kopyalanır. LF satır sonuyla gelir (commit'lenmiş blob'larla aynı).
> Her commit tek başına `npm run check` ✅ (tsc + build + 11 doğrulama).

## 0 — Dal

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git fetch
git switch faz-14-account-settings    # origin'de var, main ile aynı commit (5bd6317)
```

## 14.12

```powershell
# 14.12 — Veri katmanı: tipler, servis, store, hata metinleri
cd D:\Projects\davetkart\davetkart-frontent
robocopy "..\Claude outputs\f14\frontend\14.12" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add src/types.ts src/services/account.ts src/stores/useAccountStore.ts src/stores/useAuthStore.ts src/stores/sessionActions.ts src/contracts/error-codes.json
git add src/locales/tr/errors.json src/locales/en/errors.json src/utils/toDisplayError.ts scripts/verify-endpoints.ts docs/rehber/src/services/account.md docs/rehber/src/stores/useAccountStore.md
git commit -m "14.1 - feat(account): Add the account settings data layer and error texts"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.13

```powershell
# 14.13 — Hesap ayarları bileşenleri
cd D:\Projects\davetkart\davetkart-frontent
robocopy "..\Claude outputs\f14\frontend\14.13" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add src/components/account/AccountCard.tsx src/components/account/AccountNav.tsx src/components/account/DeleteAccountCard.tsx src/components/account/EmailChangeForm.tsx src/components/account/FormField.tsx src/components/account/OrdersList.tsx
git add src/components/account/PasswordForm.tsx src/components/account/ProfileForm.tsx src/components/account/RightRow.tsx src/components/account/SessionList.tsx src/components/account/TierRightsGrid.tsx src/utils/accountLabels.ts
git add src/hooks/useAccountEntitlements.ts
git commit -m "14.2 - feat(account): Add the account settings components"
git status --short    # bu adımın dosyası kalmamalı
```

## 14.14

```powershell
# 14.14 — Bölümlü hesap sayfası, /eposta-onay, panel rozeti
cd D:\Projects\davetkart\davetkart-frontent
robocopy "..\Claude outputs\f14\frontend\14.14" . /E /NFL /NDL /NJH /NJS /NP | Out-Null
git add src/pages/AccountPage.tsx src/pages/account/AccountOrdersSection.tsx src/pages/account/AccountOverviewSection.tsx src/pages/account/AccountPlansSection.tsx src/pages/account/AccountPrivacySection.tsx src/pages/account/AccountSecuritySection.tsx
git add src/pages/EmailChangeConfirmPage.tsx src/App.tsx src/pages/DashboardPage.tsx src/pages/PricingPage.tsx docs/rehber/src/pages/AccountPage.md docs/rehber/src/pages/account/README.md
git commit -m "14.3 - feat(account): Split the account page into sections with plans, orders and security"
git status --short    # bu adımın dosyası kalmamalı
```

## Son

```powershell
cd D:\Projects\davetkart\davetkart-frontent
npm run check
git log --oneline -3
git push
```
