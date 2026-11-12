# Envanter — davetkart-docs (2026-11-12)

> Betikle üretildi: `python -I _restructure/restructure.py inventory`. Tarih sütunları:
> **dosyada** = dosyanın ilk 3000 karakterinde geçen ilk tarih; **eski git** = eski
> `davetkart-claude` deposundaki son commit (`claude/` dışındakiler hiç commit'lenmemişti).
> Dosyalar başlangıç commit'i `9e428a8` anındaki yollarıyla listelenir.

## 1. Sınıflara dağılım

| Sınıf | Dosya |
|---|---|
| `context` | 1 |
| `decisions` | 2 |
| `phases` | 180 |
| `prompts` | 3 |
| `operations` | 2 |
| `product` | 82 |
| `notes` | 3 |
| `archive` | 4 |
| `archive-local` | 16 |
| **Toplam** | **293** |

## 2. Dosyalar

| Yol | Boyut | İlk başlık | Dosyada tarih | Eski git | Sınıf | Durum |
|---|---:|---|---|---|---|---|
| `Claude outputs/FAZ-11-COMMIT-KOMUTLARI.md` | 8,094 | Faz 11 — commit komutları (backend + claude) |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/FAZ-11-FRONTEND-COMMIT-KOMUTLARI.md` | 3,298 | Faz 11 — frontend commit komutları |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/FAZ-12-RAPOR.md` | 11,793 | Faz 12 — Rapor (24 Ekim 2026) | 24 Ekim 2026 | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/FAZ-13-COMMIT-KOMUTLARI.md` | 7,267 | Faz 13 — commit komutları (backend) |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/FAZ-13-FRONTEND-COMMIT-KOMUTLARI.md` | 3,980 | Faz 13 — commit komutları (frontend) |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/FAZ-14-COMMIT-KOMUTLARI.md` | 11,112 | Faz 14 — commit komutları (backend) |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/FAZ-14-FRONTEND-COMMIT-KOMUTLARI.md` | 3,063 | Faz 14 — commit komutları (frontend) |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/FRONTEND-YAKALAMA-PLANI.md` | 24,542 | Frontend Yakalama Planı | 11 Eylül 2026 | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/_snap/_partial-snapshot.tgz` | 25,427,968 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/f13-ara.tar` | 71,680 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/f13-backend.tgz` | 1,588,499 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/f13-be.tar` | 542,720 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/f13-fe.tar` | 532,480 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/f13-frontend.tgz` | 30,593,843 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/faz11-backend.tar` | 593,920 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/faz11-frontend.tar` | 286,720 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/fe.tgz` | 30,579,829 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/repo.tgz` | 20,288,504 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/v-aws.tgz` | 6,057,355 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/v-laravel.tgz` | 16,722,401 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/v-phpstan.tgz` | 12,004,393 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_snap/v-rest.tgz` | 8,029,062 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_to_delete/f14-bundle/backend.bundle.lock` | 63 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/_to_delete/f14.tar` | 1,361,920 |  |  | — (git'e hiç girmemişti) | archive-local | yerel, git dışı |
| `Claude outputs/f13-ara/13.2/Order.php` | 5,897 | [Fillable([])] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f13-ara/13.9/types.ts` | 22,381 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f13-ara/son/Order.php` | 6,170 | [Fillable([])] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f13-ara/son/types.ts` | 22,723 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.1/app/Actions/Invitation/DeleteInvitationAction.php` | 4,669 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.1/app/Actions/Payment/ClaimReleasedOrderAction.php` | 3,707 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.1/app/Models/Order.php` | 6,914 | [Fillable([])] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.1/database/migrations/2026_10_26_100000_add_consumed_at_to_orders_table.php` | 2,363 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.1/docs/rehber/app/Actions/Invitation/DeleteInvitationAction.md` | 11,184 | `app/Actions/Invitation/DeleteInvitationAction.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.1/docs/rehber/app/Actions/Payment/ClaimReleasedOrderAction.md` | 7,675 | `app/Actions/Payment/ClaimReleasedOrderAction.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.1/docs/rehber/app/Models/Order.md` | 11,878 | `app/Models/Order.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.1/docs/rehber/database/migrations/2026_10_26_100000_add_consumed_at_to_orders_table.md` | 2,626 | `2026_10_26_100000_add_consumed_at_to_orders_table` — yanmış hakkın damgası |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.1/docs/rehber/tests/Feature/OrderConsumptionTest.md` | 831 | `tests/Feature/OrderConsumptionTest.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.1/tests/Feature/OrderConsumptionTest.php` | 4,082 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/app/Actions/Account/ConfirmEmailChangeAction.php` | 2,820 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/app/Actions/Account/RequestEmailChangeAction.php` | 1,183 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/app/Enums/ErrorCode.php` | 9,241 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/app/Exceptions/EmailChangeFailedException.php` | 892 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/app/Http/Controllers/Api/V1/EmailChangeController.php` | 919 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/app/Http/Controllers/Api/V1/PublicEmailChangeController.php` | 699 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/app/Http/Requests/Account/ConfirmEmailChangeRequest.php` | 2,238 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/app/Http/Requests/Account/RequestEmailChangeRequest.php` | 1,692 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/app/Notifications/EmailChangeConfirmationNotification.php` | 1,681 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/app/Notifications/EmailChangedNotification.php` | 1,811 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/app/Support/EmailChangeLink.php` | 1,968 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/config/davetkart.php` | 13,415 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/contracts/error-codes.json` | 4,149 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/docs/08-HATA-SOZLESMESI.md` | 14,173 | DavetKart Backend — Hata Sözleşmesi | 31 Temmuz 2026 | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/docs/rehber/app/Actions/Account/RequestEmailChangeAction.md` | 4,932 | E-posta değişikliği: istek + imzalı onay |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/docs/rehber/app/Enums/ErrorCode.md` | 24,742 | `app/Enums/ErrorCode.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/docs/rehber/config/davetkart.md` | 28,219 | `config/davetkart.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/docs/rehber/routes/api.md` | 41,291 | `routes/api.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/docs/rehber/tests/Feature/EmailChangeTest.md` | 1,111 | `tests/Feature/EmailChangeTest.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/routes/api.php` | 20,679 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/tests/Feature/EmailChangeTest.php` | 7,677 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.10/tests/Unit/EmailChangedNotificationTest.php` | 663 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.11/docs/rehber/fazlar/FAZ-14-ELLE-DOGRULAMA.md` | 2,965 | FAZ 14 — Elle Doğrulama Betiği | 25 Ekim 2026 | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.11/docs/rehber/fazlar/FAZ-14.md` | 9,015 | FAZ 14 — Hesap ayarları: Planlarım, iptal/iade, profil, parola, oturumlar, e-pos | 25 Ekim 2026 | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.11/docs/rehber/fazlar/README.md` | 4,227 | `docs/rehber/fazlar/` — Faz Özetleri | 23 Eylül 2026 | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/app/Enums/RefundRequestStatus.php` | 1,660 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/app/Models/Order.php` | 7,792 | [Fillable([])] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/app/Models/RefundRequest.php` | 1,952 | [Fillable([])] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/database/factories/RefundRequestFactory.php` | 1,902 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/database/migrations/2026_10_26_110000_create_refund_requests_table.php` | 2,642 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/docs/rehber/app/Enums/RefundRequestStatus.md` | 1,534 | `app/Enums/RefundRequestStatus.php` — iade talebinin durumları |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/docs/rehber/app/Models/Order.md` | 12,173 | `app/Models/Order.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/docs/rehber/app/Models/RefundRequest.md` | 908 | `app/Models/RefundRequest.php` · `database/factories/RefundRequestFactory.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/docs/rehber/database/migrations/2026_10_26_110000_create_refund_requests_table.md` | 1,598 | `2026_10_26_110000_create_refund_requests_table` — iade talepleri |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/docs/rehber/tests/Feature/RefundRequestConstraintsTest.md` | 863 | `tests/Feature/RefundRequestConstraintsTest.php` · `tests/Unit/RefundRequestStat |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/tests/Feature/RefundRequestConstraintsTest.php` | 3,310 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.2/tests/Unit/RefundRequestStatusTest.php` | 1,398 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/app/Actions/Account/EntitlementRight.php` | 719 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/app/Actions/Account/EntitlementSummary.php` | 1,165 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/app/Actions/Account/SummarizeEntitlementsAction.php` | 5,180 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/app/Actions/Account/TierEntitlements.php` | 601 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/app/Enums/EntitlementState.php` | 1,439 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/app/Enums/RefundBlocker.php` | 1,030 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/app/Services/Refund/RefundEligibility.php` | 2,024 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/config/davetkart.php` | 13,114 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/docs/rehber/app/Actions/Account/SummarizeEntitlementsAction.md` | 3,478 | `SummarizeEntitlementsAction` — "Planlarım" hak sayacı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/docs/rehber/app/Services/Refund/RefundEligibility.md` | 1,798 | `RefundEligibility` · `RefundBlocker` — "bu hak iptal edilebilir mi?" |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/docs/rehber/config/davetkart.md` | 27,935 | `config/davetkart.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/docs/rehber/tests/Feature/SummarizeEntitlementsActionTest.md` | 1,003 | `tests/Feature/SummarizeEntitlementsActionTest.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.3/tests/Feature/SummarizeEntitlementsActionTest.php` | 8,349 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.4/app/Http/Controllers/Api/V1/AccountController.php` | 995 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.4/app/Http/Resources/EntitlementSummaryResource.php` | 3,569 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.4/docs/rehber/app/Http/Controllers/Api/V1/AccountController.md` | 685 | `AccountController` — hesap ayarlarının okuma uçları |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.4/docs/rehber/app/Http/Resources/EntitlementSummaryResource.md` | 1,838 | `EntitlementSummaryResource` — "Planlarım" sözleşmesi |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.4/docs/rehber/routes/api.md` | 40,448 | `routes/api.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.4/docs/rehber/tests/Feature/AccountEntitlementsTest.md` | 542 | `tests/Feature/AccountEntitlementsTest.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.4/routes/api.php` | 17,671 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.4/tests/Feature/AccountEntitlementsTest.php` | 5,616 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/app/Actions/Payment/ClaimReleasedOrderAction.php` | 3,791 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/app/Actions/Refund/RequestRefundAction.php` | 2,477 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/app/Actions/Refund/WithdrawRefundRequestAction.php` | 1,176 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/app/Enums/ErrorCode.php` | 8,791 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/app/Exceptions/RefundNotAllowedException.php` | 811 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/app/Http/Controllers/Api/V1/RefundRequestController.php` | 1,296 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/app/Http/Requests/Refund/StoreRefundRequestRequest.php` | 1,082 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/app/Http/Resources/RefundRequestResource.php` | 690 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/contracts/error-codes.json` | 4,020 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/docs/08-HATA-SOZLESMESI.md` | 14,140 | DavetKart Backend — Hata Sözleşmesi | 31 Temmuz 2026 | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/docs/rehber/app/Actions/Payment/ClaimReleasedOrderAction.md` | 7,888 | `app/Actions/Payment/ClaimReleasedOrderAction.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/docs/rehber/app/Actions/Refund/RequestRefundAction.md` | 3,100 | Hakkı iptal et: `RequestRefundAction` · `WithdrawRefundRequestAction` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/docs/rehber/app/Enums/ErrorCode.md` | 24,363 | `app/Enums/ErrorCode.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/docs/rehber/routes/api.md` | 40,656 | `routes/api.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/docs/rehber/tests/Feature/RefundRequestTest.md` | 939 | `tests/Feature/RefundRequestTest.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/routes/api.php` | 18,392 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.5/tests/Feature/RefundRequestTest.php` | 8,352 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.6/app/Actions/Refund/ResolveRefundRequestAction.php` | 3,337 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.6/app/Console/Commands/ApproveRefundRequest.php` | 1,417 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.6/app/Console/Commands/Concerns/ResolvesRefundRequests.php` | 1,207 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.6/app/Console/Commands/ListRefundRequests.php` | 2,791 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.6/app/Console/Commands/RejectRefundRequest.php` | 1,022 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.6/app/Notifications/RefundRequestResolvedNotification.php` | 2,277 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.6/docs/rehber/PROJE-KOMUTLARI.md` | 12,367 | DavetKart'a özel terminal komutları — kullanım kılavuzu | 2027-01-07 | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.6/docs/rehber/app/Actions/Refund/ResolveRefundRequestAction.md` | 1,586 | `ResolveRefundRequestAction` · `RefundRequestResolvedNotification` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.6/docs/rehber/app/Console/Commands/RefundCommands.md` | 1,665 | `refunds:list` · `refunds:approve` · `refunds:reject` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.6/docs/rehber/tests/Feature/RefundCommandsTest.md` | 884 | `tests/Feature/RefundCommandsTest.php` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.6/tests/Feature/RefundCommandsTest.php` | 7,480 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.7/app/Actions/Account/UpdateProfileAction.php` | 789 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.7/app/Http/Controllers/Api/V1/ProfileController.php` | 766 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.7/app/Http/Requests/Account/UpdateProfileRequest.php` | 1,646 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.7/docs/rehber/app/Actions/Account/UpdateProfileAction.md` | 1,467 | Profil güncelleme: `PATCH /api/auth/me` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.7/docs/rehber/routes/api.md` | 40,721 | `routes/api.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.7/routes/api.php` | 18,622 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.7/tests/Feature/ProfileUpdateTest.php` | 2,607 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.8/app/Actions/Account/ChangePasswordAction.php` | 1,765 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.8/app/Http/Controllers/Api/V1/PasswordController.php` | 1,076 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.8/app/Http/Requests/Account/ChangePasswordRequest.php` | 1,375 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.8/app/Notifications/PasswordChangedNotification.php` | 1,508 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.8/docs/rehber/app/Actions/Account/ChangePasswordAction.md` | 2,660 | Parola değiştirme: `PUT /api/auth/password` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.8/docs/rehber/routes/api.md` | 40,817 | `routes/api.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.8/routes/api.php` | 18,980 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.8/tests/Feature/PasswordChangeTest.php` | 4,444 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/app/Actions/Auth/IssueApiTokenAction.php` | 1,168 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/app/Actions/Auth/LoginUserAction.php` | 2,704 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/app/Actions/Auth/RegisterUserAction.php` | 1,591 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/app/Actions/Auth/RevokeOtherSessionsAction.php` | 511 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/app/Actions/Auth/RevokeSessionAction.php` | 753 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/app/Http/Controllers/Api/V1/AuthController.php` | 4,053 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/app/Http/Controllers/Api/V1/SessionController.php` | 2,358 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/app/Http/Resources/SessionResource.php` | 1,458 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/app/Support/DeviceLabel.php` | 1,945 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/database/migrations/2026_10_26_120000_add_user_agent_to_personal_access_tokens_table.php` | 1,197 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/docs/rehber/app/Actions/Auth/IssueApiTokenAction.md` | 3,689 | Oturumlar: `IssueApiTokenAction` · `SessionController` · `DeviceLabel` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/docs/rehber/app/Actions/Auth/LoginUserAction.md` | 16,183 | `app/Actions/Auth/LoginUserAction.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/docs/rehber/app/Actions/Auth/RegisterUserAction.md` | 14,022 | `app/Actions/Auth/RegisterUserAction.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/docs/rehber/database/migrations/2026_10_26_120000_add_user_agent_to_personal_access_tokens_table.md` | 1,051 | `2026_10_26_120000_add_user_agent_to_personal_access_tokens_table` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/docs/rehber/routes/api.md` | 41,075 | `routes/api.php` — Eğitim Dokümanı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/routes/api.php` | 19,610 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/tests/Feature/SessionTest.php` | 6,622 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/backend/14.9/tests/Unit/DeviceLabelTest.php` | 2,046 | [Test] |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/docs/rehber/src/services/account.md` | 1,308 | `src/services/account.ts` — hesap ayarlarının backend sınırı |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/docs/rehber/src/stores/useAccountStore.md` | 739 | `src/stores/useAccountStore.ts` |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/scripts/verify-endpoints.ts` | 23,736 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/src/contracts/error-codes.json` | 4,149 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/src/locales/en/errors.json` | 10,619 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/src/locales/tr/errors.json` | 11,233 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/src/services/account.ts` | 4,354 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/src/stores/sessionActions.ts` | 2,309 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/src/stores/useAccountStore.ts` | 2,735 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/src/stores/useAuthStore.ts` | 3,436 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/src/types.ts` | 25,170 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.12/src/utils/toDisplayError.ts` | 8,058 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/components/account/AccountCard.tsx` | 2,050 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/components/account/AccountNav.tsx` | 2,415 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/components/account/DeleteAccountCard.tsx` | 6,401 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/components/account/EmailChangeForm.tsx` | 4,502 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/components/account/FormField.tsx` | 1,948 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/components/account/OrdersList.tsx` | 3,423 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/components/account/PasswordForm.tsx` | 3,568 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/components/account/ProfileForm.tsx` | 2,625 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/components/account/RightRow.tsx` | 8,097 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/components/account/SessionList.tsx` | 5,651 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/components/account/TierRightsGrid.tsx` | 3,397 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/hooks/useAccountEntitlements.ts` | 823 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.13/src/utils/accountLabels.ts` | 2,606 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/docs/rehber/src/pages/AccountPage.md` | 7,303 | `src/pages/AccountPage.tsx` — Hesap ayarları ve hesabı silme (`/hesap`) |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/docs/rehber/src/pages/account/README.md` | 3,178 | Hesap ayarları — Faz 14 (frontend) |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/src/App.tsx` | 6,153 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/src/pages/AccountPage.tsx` | 2,576 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/src/pages/DashboardPage.tsx` | 27,090 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/src/pages/EmailChangeConfirmPage.tsx` | 3,957 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/src/pages/PricingPage.tsx` | 12,928 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/src/pages/account/AccountOrdersSection.tsx` | 1,771 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/src/pages/account/AccountOverviewSection.tsx` | 1,597 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/src/pages/account/AccountPlansSection.tsx` | 3,122 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/src/pages/account/AccountPrivacySection.tsx` | 1,322 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/f14/frontend/14.14/src/pages/account/AccountSecuritySection.tsx` | 1,249 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/php-herdsiz.ini` | 72,769 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `Claude outputs/teshis.php` | 1,420 |  |  | — (git'e hiç girmemişti) | phases | tamamlandı (tarihsel) |
| `PROMPT-FAZ-11.md` | 21,904 | PROMPT — FAZ 11: Hediye Kodu (indirim + ücretsiz plan) | 23 Ekim 2026 | — (git'e hiç girmemişti) | prompts | tamamlandı (tarihsel) |
| `PROMPT-FAZ-12.md` | 20,299 | PROMPT — FAZ 12: Shopier ile kartla ödeme | 23 Ekim 2026 | — (git'e hiç girmemişti) | prompts | tamamlandı (tarihsel) |
| `PROMPT-YAYIN.md` | 2,229 | Yeni asistan için başlangıç mesajı |  | — (git'e hiç girmemişti) | prompts | güncel |
| `YAYIN-DEVIR.md` | 16,045 | YAYIN DEVİR NOTU — DavetKart'ı AWS'e Alma | 15 Ekim 2026 | — (git'e hiç girmemişti) | operations | güncel |
| `YAYIN-PLANI.md` | 52,567 | YAYIN PLANI — DavetKart'ı AWS Lightsail'e Almak | 3 Ekim 2026 | — (git'e hiç girmemişti) | operations | güncel |
| `claude/Notlar/01-FRONTEND-ANALIZI.md` | 14,892 | DavetKart Backend — Frontend Gereksinim Analizi | 2026-07-27 | 2026-07-29 | notes | tarihsel not |
| `claude/Notlar/02-FRONTEND-BACKEND-TEMAS-NOKTALARI.md` | 30,413 | Frontend'in Backend'e Dokunan Her Yeri — Rehberli Gezinti |  | 2026-07-29 | notes | tarihsel not |
| `claude/Notlar/03-FRONTEND-YAPILACAKLAR.md` | 25,930 | Frontend Yapılacaklar — Hata Sözleşmesi Uyarlaması | 31 Temmuz 2026 | 2026-08-28 | notes | tarihsel not |
| `claude/PHP-LARAVEL-SETUP-EK-FAZ-11.md` | 6,600 | `PHP-LARAVEL-SETUP.md` — Faz 11 Yaması | 23 Ekim 2026 | — (eski depoda commit'lenmemişti) | decisions | güncel (ana dosyaya işlenmedi) |
| `claude/PHP-LARAVEL-SETUP-EK-FAZ-12.md` | 8,307 | `PHP-LARAVEL-SETUP.md` — Faz 12 Yaması | 24 Ekim 2026 | — (eski depoda commit'lenmemişti) | decisions | güncel (ana dosyaya işlenmedi) |
| `claude/PHP-LARAVEL-SETUP.md` | 99,707 | DavetKart — Proje Devir Dosyası | 23 Eylül 2026 | 2026-09-04 | context | güncel (EK-11/12 işlenmeyi bekliyor) |
| `claude/PROMPT-ARSIV-FAZ-4.md` | 16,344 | Yeni AI Asistanı İçin Başlangıç Prompt'u | 27 Ağustos 2026 | 2026-09-04 | archive | geçersiz kılındı → claude/PROMPT.md (o da arşivde) |
| `claude/PROMPT.md` | 6,164 | Yeni AI Asistanı İçin Başlangıç Prompt'u | 4 Eylül 2026 | 2026-09-04 | archive | geçersiz kılındı → context/PHP-LARAVEL-SETUP.md + prompts/ |
| `claude/README.md` | 42 | davetkart-claude |  | 2026-07-29 | archive | geçersiz kılındı → README.md |
| `claude/hero-video-onay/generate_hero_video.py` | 11,703 | ---------------------------------------------------------------------------- |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/hero-video-onay/hero-bg-poster.jpg` | 32,998 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/hero-video-onay/hero-bg.mp4` | 2,377,654 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/hero-video-onay/hero-bg.webm` | 206,290 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/hero-video-onay/onizleme.html` | 8,085 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-desktop-poster.jpg` | 17,332 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-desktop.mp4` | 427,957 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-desktop.webm` | 94,731 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-mobile-poster.jpg` | 15,021 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-mobile.mp4` | 276,940 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-mobile.webm` | 62,769 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-desktop-poster.jpg` | 19,367 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-desktop.mp4` | 420,622 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-desktop.webm` | 129,553 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-mobile-poster.jpg` | 19,550 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-mobile.mp4` | 370,228 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-mobile.webm` | 105,354 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-desktop-poster.jpg` | 20,516 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-desktop.mp4` | 433,748 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-desktop.webm` | 253,405 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-mobile-poster.jpg` | 15,354 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-mobile.mp4` | 248,351 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-mobile.webm` | 154,282 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/generate_category_videos.py` | 16,472 | --------------------------------------------------------------------------- |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/generate_premium_videos.py` | 9,338 | Palet - sinematik gün batımı |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/generate_wedding_videos.py` | 19,642 | --------------------------------------------------------------------------- |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gokyuzu-ruyasi/generate_sky_video.py` | 16,913 | --------------------------------------------------------------------------- |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-desktop-poster.jpg` | 18,291 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-desktop.mp4` | 370,687 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-desktop.webm` | 96,816 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-mobile-poster.jpg` | 17,460 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-mobile.mp4` | 265,465 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-mobile.webm` | 79,505 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gokyuzu-ruyasi/onizleme.html` | 6,292 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gokyuzu-ruyasi/render.log` | 51 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-desktop-poster.jpg` | 21,768 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-desktop.mp4` | 558,843 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-desktop.webm` | 272,535 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-mobile-poster.jpg` | 16,524 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-mobile.mp4` | 278,217 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-mobile.webm` | 159,254 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/kina-bordo/kina-bordo-desktop-poster.jpg` | 16,923 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/kina-bordo/kina-bordo-desktop.mp4` | 381,870 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/kina-bordo/kina-bordo-desktop.webm` | 84,303 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/kina-bordo/kina-bordo-mobile-poster.jpg` | 16,641 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/kina-bordo/kina-bordo-mobile.mp4` | 314,150 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/kina-bordo/kina-bordo-mobile.webm` | 74,637 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-desktop-poster.jpg` | 16,603 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-desktop.mp4` | 437,161 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-desktop.webm` | 122,403 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-mobile-poster.jpg` | 15,996 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-mobile.mp4` | 349,461 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-mobile.webm` | 117,063 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mum-isigi/mum-isigi-desktop-poster.jpg` | 17,706 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mum-isigi/mum-isigi-desktop.mp4` | 326,816 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mum-isigi/mum-isigi-desktop.webm` | 83,625 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mum-isigi/mum-isigi-mobile-poster.jpg` | 15,776 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mum-isigi/mum-isigi-mobile.mp4` | 231,489 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/mum-isigi/mum-isigi-mobile.webm` | 59,332 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-desktop-poster.jpg` | 15,737 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-desktop.mp4` | 322,203 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-desktop.webm` | 69,704 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-mobile-poster.jpg` | 15,486 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-mobile.mp4` | 303,462 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-mobile.webm` | 64,532 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/onizleme-tumu.html` | 7,854 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/parti-aurora/parti-aurora-desktop-poster.jpg` | 38,753 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/parti-aurora/parti-aurora-desktop.mp4` | 819,802 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/parti-aurora/parti-aurora-desktop.webm` | 294,119 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/parti-aurora/parti-aurora-mobile-poster.jpg` | 39,875 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/parti-aurora/parti-aurora-mobile.mp4` | 611,868 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/parti-aurora/parti-aurora-mobile.webm` | 213,727 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/premium-lab/dugun-onyx.html` | 18,579 | 07070a gibi hafif mavi-siyah derinlik verir. |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/premium-lab/dugun-sahil.html` | 22,830 | bg{width:100%;height:100%;object-fit:cover;display:block;opacity:0; |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/premium-lab/index.html` | 3,976 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-desktop-poster.jpg` | 19,648 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-desktop.mp4` | 222,621 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-desktop.webm` | 95,732 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-mobile-poster.jpg` | 17,838 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-mobile.mp4` | 157,981 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-mobile.webm` | 72,307 |  |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `claude/video-onay/video_engine.py` | 11,799 | --------------------------------------------------------------------------- |  | 2026-09-04 | product | tamamlandı (tarihsel) |
| `scaffold-structure.ps1` | 4,859 | ============================================================================= |  | — (git'e hiç girmemişti) | archive | geçersiz kılındı (Faz 0'da çalıştı) |

## 3. Başlangıç durumu (2026-11-12)

- `davetkart-docs`'ta hiç commit yoktu; bütün dosyalar takip edilmiyordu.
- `claude/` kendi `.git`'i olan ayrı bir depoydu (`davetkart-claude`, 5 commit, son 2026-09-04).
  Çalışma ağacında `PHP-LARAVEL-SETUP.md` değişmiş (+200/−53 satır), `EK-FAZ-11/12` eklenmemişti.
- İsmail'in kararı (**B seçeneği**): sıfırdan başla. `claude/.git` →
  `D:\Projects\davetkart\_backup\davetkart-claude.git` (depo dışı; silinmedi). Eski commit listesi
  `_restructure/claude-git-log.txt`, dosya bazında son commit tarihleri `claude-git-dates.tsv`.
- Başlangıç commit'i `9e428a8` (`main`): o anki hâl, olduğu gibi. `PHP-LARAVEL-SETUP.md`'nin
  bekleyen değişikliği de bu commit'e girdi; EK-11/12'nin "önce o commit'lensin" ön koşulu artık sağlandı.
- 🔴 `Claude outputs/_snap/` içindeki 3 arşivde `.env` var (`repo.tgz`, `fe.tgz`,
  `_partial-snapshot.tgz`). Hiçbir `.tgz/.tar/.bundle` git'e alınmadı (`.gitignore`); diskte duruyor.
- Metin dosyalarında sır taraması (AWS anahtarı, `APP_KEY`, özel anahtar, IBAN deseni): bulgu yok.

## 4. Mükerrerler

Belge düzeyinde mükerrer yok. Benzer görünenler:

| Dosyalar | Sonuç |
|---|---|
| `claude/PROMPT.md` ↔ `claude/PROMPT-ARSIV-FAZ-4.md` | Aynı başlık, farklı dönem. ARSIV, PROMPT'un Faz 4'e kadarki eski sürümü (PROMPT.md bunu kendisi söylüyor). İkisi de arşive. |
| `Claude outputs/f14/backend/14.x/...` içinde aynı dosyanın birkaç sürümü (`routes/api.php`, `docs/rehber/routes/api.md`, `config/davetkart.php`, `ErrorCode.php`) | Mükerrer değil: her adım klasörü o adımdaki hâldir. Klasör bütün olarak taşındı. |
| `f13-ara/13.2` ↔ `f13-ara/son` | Aynı, ara ve son sürüm. Bütün olarak taşındı. |

## 5. Karar kaydı (K numaraları)

Taranan yerler: bu depodaki `PHP-LARAVEL-SETUP.md` + `EK-FAZ-11/12`, ve **salt okunur**
olarak backend deposundaki `claude/PHP-LARAVEL-SETUP-EK-FAZ-5…9.md`, `claude/FAZ-10-PLANI.md`,
`docs/rehber/fazlar/FAZ-*.md`, `docs/07`.

| Aralık | Tanımlandığı yer | Ana dosyada (`§7`)? |
|---|---|---|
| K1–K48 | `PHP-LARAVEL-SETUP.md` §7 | ✅ |
| K49–K53 | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md` | ❌ |
| K54–K63 | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` | ❌ |
| K64–K71 | backend `claude/…-EK-FAZ-7.md` | ✅ (işlenmiş) |
| K72–K79 | backend `claude/…-EK-FAZ-8.md` | ❌ |
| K80–K86 | backend `claude/…-EK-FAZ-9.md` | ❌ |
| K87–K93, K95–K106 | backend `claude/FAZ-10-PLANI.md` (`EK-FAZ-10` hiç yazılmadı) | ❌ |
| K94 | Faz 10 planında Shopier için ayrıldı; Faz 12'de `EK-FAZ-12` + `FAZ-12.md`'de tanımlandı | ❌ |
| K107–K116 | `EK-FAZ-11.md` | ❌ |
| K117–K127 | `EK-FAZ-12.md` | ❌ |

- **Eksik numara:** yok. K1–K127 arası her numaranın bir tanımı var. K9 `K9'` olarak yazılı
  (MySQL kararı PostgreSQL ile değişti, numara asal işaretle korunmuş).
- **Çakışma:** daha önce görülen ikinci **K18** backend `docs/07` §8'deydi (Pest/PHPUnit satırı).
  Orada zaten **K24** olarak düzeltilmiş, satırda not var (`docs/07:958`). Bu depoda çakışma yok.
  ⚠️ Sıra dışı: K94, K95–K106'dan sonra (Faz 12'de) tanımlandı. Çakışma değil, numara önceden ayrılmıştı.
- **Geçersiz kılınan / sapılan:** K9 → K9' · K66 "public_slug üretilmiyor" (K40'ın sonucu) ·
  K122 callback'te **K69'dan bilinçli sapma** (OSB ucunda K69 geçerli) · K43 ⚠️ "Faz 7'de uygulanmadı"
  (açık ticari karar) · K67 ↔ frontend 11.6 çelişki sorusu açık (`EK-FAZ-12` §F-7) ·
  K11'in durumu ana dosyada hâlâ "📋 Faz 2'de uygulanacak" (eskimiş durum metni).
- **Ana dosyaya işlenmemiş:** K49–K63, K72–K127 (yukarıdaki ❌ satırlar). Ana dosyanın başındaki
  uyarı K49–K63 ve K72–K86 için bunu zaten söylüyor; K87 sonrası için bir uyarı yok.

## 6. Bağlantılar (düzenleme öncesi)

- Markdown bağlantısı: belge katmanında yalnızca 1 tane var
  (`claude/PROMPT.md` → `PROMPT-ARSIV-FAZ-4.md`, hedef var). `f14/` içindeki bağlantılar kod deposunun
  `docs/rehber/` ağacına göre yazılmış; bu depoda kırık görünmeleri doğal, kapsam dışı.
- Düz metin yollar (`claude\…`, `claude/…`): ~40 atıf. Çoğu **backend deposunun** `claude/`
  klasörüne (`GOZDEN-GECIRME-RAPORU.md`, `FAZ-9-DEVIR.md`, `EK-FAZ-5…9`, `FAZ-10-PLANI.md`) gidiyor,
  taşımadan etkilenmiyor. Bu depodaki dosyalara giden düz metin yollar (`claude\Notlar\…`,
  `claude/PHP-LARAVEL-SETUP.md`, `claude/YAYIN-PLANI.md`, `Claude outputs\f14` …) tarihsel
  anlatımın parçası. **Değiştirilmedi**; eski → yeni karşılıkları kök `README.md`'de tablo olarak var.

## 7. Dış atıflar (salt okunur, listelendi)

Backend (`davetkart-backend-php-laravel`) — `CLAUDE.md`/`README.md`/`docs/` içinde 58 satır,
frontend (`davetkart-frontent`) — 1 satır. **Bu depoya** işaret edenler:

| Hedef (eski) | Yeni yol | Atıf yapan dosyalar |
|---|---|---|
| `claude/PHP-LARAVEL-SETUP.md` | `context/PHP-LARAVEL-SETUP.md` | backend `docs/09:888`, `docs/11:2906`, `docs/11:2981`, `docs/rehber/fazlar/FAZ-0.md:266`, `FAZ-1.md:314`, `FAZ-2.md:381`, `FAZ-3.md:444`, `FAZ-5.md:431`, `FAZ-6.md:325`, `FAZ-12.md:74` |
| `claude/Notlar/03-FRONTEND-YAPILACAKLAR.md` | `notes/03-FRONTEND-YAPILACAKLAR.md` | backend `docs/03:314`, `docs/07:382`, `docs/08:300`, `rehber/app/Exceptions/InvalidCredentialsException.md:107`, `rehber/app/Http/Resources/UserResource.md:222`, `rehber/database/migrations/2026_08_19_120100_create_timeline_events_table.md:235`, `rehber/fazlar/FAZ-0.md:75`, `FAZ-0.md:267`, `FAZ-2.md:298`, `FAZ-2.md:380`, `FAZ-3.md:443`, `FAZ-5.md:432`, `rehber/tests/Feature/InvitationTest.md:360`; frontend `docs/rehber/src/data.md:136` |
| `claude/Notlar/04` | — (bu depoda yok; backend `claude/Notlar/`'a bakılmalı) | backend `docs/07:557` |
| `claude/PHP-LARAVEL-SETUP-EK-FAZ-11.md` | `decisions/addenda/…` | backend `docs/rehber/fazlar/FAZ-11.md` |

Geri kalan atıflar backend deposunun **kendi** `claude/` klasörüne gidiyor (22 dosya, git'te
takipli): `GOZDEN-GECIRME-RAPORU.md`, `GOZDEN-GECIRME-2026-10-09-{BACKEND,FRONTEND}.md`,
`TEST-DENETIMI-2026-09-24.md`, `FAZ-{5,6,7,9}-DEVIR.md`, `FAZ-10-PLANI.md`, `PROMPT-FAZ-{6,7,8,9}*.md`,
`OKUBENI-FAZ-5.md`, `PHP-LARAVEL-SETUP-EK-FAZ-5…9.md`, `Notlar/`. Atıflar arasında
`claude/FAZ-13-PLANI.md`, `claude/FAZ-14-PLANI.md`, `claude/PROMPT-FAZ-12.md` de var; ilk ikisi hiçbir
depoda bulunamadı.

