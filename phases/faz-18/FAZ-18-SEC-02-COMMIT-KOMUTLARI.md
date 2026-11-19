# Faz 18.4 — `SEC-02` commit komutları

> **Tarih:** 17–20 Kasım 2026 · **Kararlar:** K164–K169 · **Faz kaydı:** backend `docs/rehber/fazlar/FAZ-18.md` §18.4
> Her blok bir commit. Dosyalar tek tek, açık yolla eklenir; joker, klasör yolu ve `-A` yok.
> Her blok `git status --short` ile biter. Sıra: backend → frontend → docs → birleştirme.
> Dal adı iki kod deposunda aynı: `fix/2026-11-17-sec-02-refund-after-publish`.

## Başlamadan: çalışma ağaçlarında ne olmalı

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-17-sec-02-refund-after-publish
git status --short --untracked-files=all
```

Beklenen (33 satır, başka bir şey yok):

```
 M app/Actions/Invitation/DeleteInvitationAction.php
 M app/Actions/Invitation/PublishInvitationAction.php
 M app/Actions/Refund/ResolveRefundRequestAction.php
 M app/Console/Commands/ApproveRefundRequest.php
 M app/Console/Commands/ListRefundRequests.php
 M app/Enums/RefundBlocker.php
 M app/Models/Order.php
 M app/Services/Refund/RefundEligibility.php
 M database/factories/OrderFactory.php
 M docs/rehber/PROJE-KOMUTLARI.md
 M docs/rehber/app/Actions/Invitation/DeleteInvitationAction.md
 M docs/rehber/app/Actions/Invitation/PublishInvitationAction.md
 M docs/rehber/app/Actions/Refund/RequestRefundAction.md
 M docs/rehber/app/Actions/Refund/ResolveRefundRequestAction.md
 M docs/rehber/app/Console/Commands/RefundCommands.md
 M docs/rehber/app/Enums/ErrorCode.md
 M docs/rehber/app/Models/Order.md
 M docs/rehber/app/Services/Refund/RefundEligibility.md
 M docs/rehber/database/factories/OrderFactory.md
 M docs/rehber/fazlar/FAZ-14.md
 M docs/rehber/fazlar/FAZ-18.md
 M docs/rehber/fazlar/README.md
 M docs/rehber/tests/Feature/RefundCommandsTest.md
 M docs/rehber/tests/Feature/RefundRequestTest.md
 M tests/Feature/RefundCommandsTest.php
 M tests/Feature/RefundRequestTest.php
?? app/Actions/Payment/StampFirstPublishAction.php
?? database/migrations/2026_11_17_100000_add_first_published_at_to_orders_table.php
?? docs/rehber/app/Actions/Payment/StampFirstPublishAction.md
?? docs/rehber/database/migrations/2026_11_17_100000_add_first_published_at_to_orders_table.md
?? tests/Feature/OrderFirstPublishStampTest.php
?? tests/Feature/OrderFirstPublishedAtTest.php
?? tests/Feature/RefundApprovalRecheckTest.php
```

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git switch fix/2026-11-17-sec-02-refund-after-publish
git status --short --untracked-files=all
```

Beklenen (7 satır; ayrıca `?? .claude/` görünebilir, eklenmez):

```
 M docs/rehber/src/pages/PricingPage.md
 M docs/rehber/src/pages/account/README.md
 M src/components/account/RightRow.tsx
 M src/locales/en/errors.json
 M src/locales/tr/errors.json
 M src/pages/PricingPage.tsx
 M src/types.ts
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-16-faz-18-audit-fixes
git status --short --untracked-files=all
```

Beklenen (6 satır):

```
 M CHANGELOG.md
 M decisions/DECISION-INDEX.md
 M decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md
 M phases/faz-18/README.md
 M prompts/PROMPT-FAZ-18-3-SEC-01.md
?? phases/faz-18/FAZ-18-SEC-02-COMMIT-KOMUTLARI.md
```

⚠️ `prompts/PROMPT-FAZ-18-3-SEC-01.md` **bu işin parçası değil**: 18.4 başladığında zaten değişmişti
(`## 10. Rapor` başlığının altına tek boş satır eklenmiş). Docs bloğu onu eklemez. Ne yapacağına sen
karar ver: `git diff prompts/PROMPT-FAZ-18-3-SEC-01.md` ile bak; istemiyorsan
`git restore prompts/PROMPT-FAZ-18-3-SEC-01.md` (bunu ben çalıştırmadım).

## 1. Backend

Her commit tek başına yeşil olmalı: her adımın testi yalnızca kendisinden önceki adımların koduna
dayanır. ⚠️ Ara commit'ler ayrı ayrı **koşulmadı** (stash/checkout yasaktı); yalnızca son ağaç
(`composer check`, 1159 test) koştu.

```powershell
# 18.4.1 — yayın damgası kolonu, kısıtı ve geriye dönük doldurma (K164, K169); model ve fabrika
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-17-sec-02-refund-after-publish
git add database/migrations/2026_11_17_100000_add_first_published_at_to_orders_table.php
git add docs/rehber/database/migrations/2026_11_17_100000_add_first_published_at_to_orders_table.md
git add app/Models/Order.php
git add docs/rehber/app/Models/Order.md
git add database/factories/OrderFactory.php
git add docs/rehber/database/factories/OrderFactory.md
git add tests/Feature/OrderFirstPublishedAtTest.php
git commit -m "18.4.1 - feat(orders): Add the first_published_at stamp with a backfill"
git status --short
```

```powershell
# 18.4.2 — damga yayında basılır, serbest bırakmada kalır; silme akışı eksik damgayı basar (K164, K165)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-17-sec-02-refund-after-publish
git add app/Actions/Payment/StampFirstPublishAction.php
git add docs/rehber/app/Actions/Payment/StampFirstPublishAction.md
git add app/Actions/Invitation/PublishInvitationAction.php
git add docs/rehber/app/Actions/Invitation/PublishInvitationAction.md
git add app/Actions/Invitation/DeleteInvitationAction.php
git add docs/rehber/app/Actions/Invitation/DeleteInvitationAction.md
git add tests/Feature/OrderFirstPublishStampTest.php
git commit -m "18.4.2 - feat(orders): Stamp the orders that publish an invitation and keep the stamp on release"
git status --short
```

```powershell
# 18.4.3 — iade uygunluğu: yayın yapmış hak `used` ile reddedilir (K166) — SEC-02'nin kendisi
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-17-sec-02-refund-after-publish
git add app/Enums/RefundBlocker.php
git add app/Services/Refund/RefundEligibility.php
git add docs/rehber/app/Services/Refund/RefundEligibility.md
git add docs/rehber/app/Enums/ErrorCode.md
git add docs/rehber/app/Actions/Refund/RequestRefundAction.md
git add tests/Feature/RefundRequestTest.php
git add docs/rehber/tests/Feature/RefundRequestTest.md
git commit -m "18.4.3 - fix(refunds): Refuse a refund for a right that has published an invitation"
git status --short
```

```powershell
# 18.4.4 — onay anında yeniden sınama; komut para sorusundan önce durur (K167)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-17-sec-02-refund-after-publish
git add app/Actions/Refund/ResolveRefundRequestAction.php
git add docs/rehber/app/Actions/Refund/ResolveRefundRequestAction.md
git add app/Console/Commands/ApproveRefundRequest.php
git add tests/Feature/RefundApprovalRecheckTest.php
git commit -m "18.4.4 - fix(refunds): Recheck that the right is unused when a refund is approved"
git status --short
```

```powershell
# 18.4.5 — `refunds:list` "Yayın" sütunu (K168); komut kılavuzu 18.4.4'ün ön denetimini de anlatır
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-17-sec-02-refund-after-publish
git add app/Console/Commands/ListRefundRequests.php
git add docs/rehber/app/Console/Commands/RefundCommands.md
git add tests/Feature/RefundCommandsTest.php
git add docs/rehber/tests/Feature/RefundCommandsTest.md
git add docs/rehber/PROJE-KOMUTLARI.md
git commit -m "18.4.5 - feat(refunds): Show when the right was first published in refunds:list"
git status --short
```

```powershell
# 18.4.6 — faz kaydı; K139'un durum notu
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-17-sec-02-refund-after-publish
git add docs/rehber/fazlar/FAZ-18.md
git add docs/rehber/fazlar/README.md
git add docs/rehber/fazlar/FAZ-14.md
git commit -m "18.4.6 - docs(phases): Record Phase 18.4 (SEC-02 no refund after publish)"
git status --short                                   # boş olmalı
```

## 2. Frontend

🔴 `git add -A` yok (CRLF tuzağı). `.claude/` eklenmez.

```powershell
# 18.4.7 — yayın yapmış hakkın engeli (`used`): tip, çeviri, Planlarım açıklaması, SSS cevabı (backend K166)
cd D:\Projects\davetkart\davetkart-frontent
git switch fix/2026-11-17-sec-02-refund-after-publish
git add src/types.ts
git add src/locales/tr/errors.json
git add src/locales/en/errors.json
git add src/components/account/RightRow.tsx
git add docs/rehber/src/pages/account/README.md
git add src/pages/PricingPage.tsx
git add docs/rehber/src/pages/PricingPage.md
git commit -m "18.4.7 - feat(account): Explain why a right that published an invitation cannot be cancelled"
git status --short                                   # boş ya da yalnızca '?? .claude/'
```

## 3. Docs

```powershell
# 18.4.8 — kararlar (K164–K169), indeks (K82 ve K139 notları), takip tablosu, bu dosya
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-16-faz-18-audit-fixes
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md
git add decisions/DECISION-INDEX.md
git add phases/faz-18/README.md
git add phases/faz-18/FAZ-18-SEC-02-COMMIT-KOMUTLARI.md
git add CHANGELOG.md
git commit -m "docs(decisions): Add K164-K169 and commit commands for SEC-02"
git status --short                                   # yalnızca ' M prompts/PROMPT-FAZ-18-3-SEC-01.md' (yukarıdaki ⚠️)
# git push -u origin docs/2026-11-16-faz-18-audit-fixes
```

## 4. Birleştirme (backend ve frontend)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-17-sec-02-refund-after-publish -m "Merge SEC-02 fix into faz-18-audit-fixes"
git status --short
# git push -u origin faz-18-audit-fixes
# git push -u origin fix/2026-11-17-sec-02-refund-after-publish
```

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-17-sec-02-refund-after-publish -m "Merge SEC-02 fix into faz-18-audit-fixes"
git status --short
# git push -u origin faz-18-audit-fixes
# git push -u origin fix/2026-11-17-sec-02-refund-after-publish
```

🔴 Birleştirmeyi atlama: sonraki prompt (18.5, `SEC-03`) önceki bulgunun birleşmiş olmasını denetler.

Bitince `phases/faz-18/README.md`'de `SEC-02` satırını `birleşti` yap.

## 5. Commit'ten sonra: elle işler

1. **Yerel göç** (backend, birleştirmeden sonra): `php artisan migrate`. 17 Kasım'daki salt okunur
   sayıma göre yerel `davetkart` veritabanında 6 sipariş damgalanır (5 bağlı + 1 izlenen serbest hak).
   Bak: `php artisan tinker` →
   `App\Models\Order::query()->whereNotNull('first_published_at')->get(['id','tier','paid_at','first_published_at','invitation_id']);`
   Yanlış damga varsa: backend `docs/rehber/database/migrations/2026_11_17_100000_add_first_published_at_to_orders_table.md` §4.
2. **Elle deneme** (yerel, `PAYMENT_DRIVER=fake`, yeni kullanıcı): backend `FAZ-18.md` §18.4 "Elle doğrulama"
   3. ve 4. adımlar (Planlarım'da açıklama satırı, 409 `used`, `refunds:list` "Yayın" sütunu,
   `refunds:approve`'un soru sormadan durması).
3. **Yayında** (`v1.1.0`, sıra K148): önce backend (göç `deploy.sh` ile koşar), sonra frontend. Arada
   kalan pencerede eski frontend `used` sebebini çeviremez; 409 toast'ı "Bu hak iptal edilemiyor: used"
   der ve "İptal Et" düğmesi zaten görünmez. Kayıt açılmadan önce ikisi birlikte çıkmalı.
4. **İade onaylamadan önce** her seferinde `refunds:list`'in "Yayın" sütununa bak: tarih ya da
   `davetiyeye bağlı` yazıyorsa parayı gönderme, `refunds:reject` ile kapat.
