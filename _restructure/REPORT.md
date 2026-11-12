# Düzenleme Raporu — davetkart-docs (2026-11-12)

> Dal: `docs/2026-11-12-restructure` (başlangıç `main` = `9e428a8`). Envanter: [`INVENTORY.md`](INVENTORY.md) ·
> Plan ve sapmalar: [`MIGRATION-PLAN.md`](MIGRATION-PLAN.md).

## 0. Başlangıçta ne oldu

- Depoda hiç commit yoktu ve `claude/` iç içe ayrı bir git deposuydu. İsmail **B seçeneğini**
  seçti (sıfırdan başla) ve commit'leri asistanın atmasını istedi.
- `claude/.git` → `D:\Projects\davetkart\_backup\davetkart-claude.git` (silinmedi). Eski 5 commit:
  [`claude-git-log.txt`](claude-git-log.txt).
- `9e428a8` başlangıç commit'i: o anki hâl + `.gitignore` (kod arşivleri; 3'ünde `.env`) +
  `.gitattributes` (`eol=lf`). Yan etki: envanter için önceden yazılan
  `_restructure/claude-git-dates.tsv` de bu commit'e girdi.

## 1. Önce / sonra (2 seviye)

```
ÖNCE                                  SONRA
.                                     .
├── Claude outputs/                   ├── AGENTS.md            (yeni)
│   ├── f13-ara/  f14/                ├── CHANGELOG.md         (yeni)
│   ├── _snap/  _to_delete/ (git dışı)├── CLAUDE.md            (yeni)
│   └── FAZ-1x-*.md, ...              ├── README.md            (yeni)
├── claude/            (ayrı .git)    ├── context/             PHP-LARAVEL-SETUP.md
│   ├── Notlar/                       ├── decisions/           DECISION-INDEX.md, addenda/
│   ├── hero-video-onay/              ├── phases/              faz-11..14/, frontend-catch-up/
│   ├── video-onay/                   ├── prompts/             PROMPT-FAZ-11/12, PROMPT-YAYIN
│   └── PHP-LARAVEL-SETUP*.md, ...    ├── audits/              (yalnızca README)
├── PROMPT-FAZ-11.md                  ├── operations/          deployment/
├── PROMPT-FAZ-12.md                  ├── product/             hero-video-onay/, video-onay/
├── PROMPT-YAYIN.md                   ├── notes/               01..03-*.md
├── YAYIN-DEVIR.md                    ├── archive/             PROMPT*.md, davetkart-claude/, .ps1,
├── YAYIN-PLANI.md                    │                        local-snapshots/ (git dışı)
└── scaffold-structure.ps1            └── _restructure/        bu işin kayıtları
```

## 2. Arşiv ve `_triage/`

| Arşive giden | Gerekçe |
|---|---|
| `claude/PROMPT.md` → `archive/PROMPT.md` | 4 Eylül 2026 başlangıç prompt'u; "Faz 7'yi kapat" diyor |
| `claude/PROMPT-ARSIV-FAZ-4.md` → `archive/` | PROMPT.md'nin eski sürümü |
| `claude/README.md` → `archive/davetkart-claude/README.md` | Eski deponun README'si; UTF-16, bant eklenmedi |
| `scaffold-structure.ps1` → `archive/` | Faz 0 iskelet betiği; hedef yol artık yok |
| `Claude outputs/_snap/`, `_to_delete/` → `archive/local-snapshots/` | Git dışı kod arşivleri, `.env` içeriyor |

`_triage/` **boş**, açılmadı. Yine de iki konuda kararın gerekebilir:

1. `archive/local-snapshots/` içindeki 16 arşiv (~155 MB, 3'ünde `.env`) diskte duruyor. Saklamak
   istiyor musun, yoksa elle mi sileceksin? (Ben silmedim.)
2. `phases/faz-13/php-herdsiz.ini` + `teshis.php`: Faz 13'ün PHPStan teşhisi olarak sınıflandırdım
   (teshis.php'nin ilk satırı). `.ini` dosyasının kaynağı dosyadan anlaşılmıyor.

## 3. Karar kaydı bulguları

Ayrıntı: [`INVENTORY.md`](INVENTORY.md) §5 ve [`../decisions/DECISION-INDEX.md`](../decisions/DECISION-INDEX.md).

- **Eksik numara yok.** K1–K127'nin her birinin tanımı var. **Sıradaki boş numara K128.**
- **Çakışma yok** (bu depoda). Eski ikinci K18 backend `docs/07`'de zaten K24'e çevrilmiş.
  K94 sıra dışı (Faz 10'da ayrıldı, Faz 12'de tanımlandı).
- **Geçersiz kılınan:** K9 → K9' · K53 → K62 → K79 · K63 → K71.
- **⚠️ Açık:** K43 uygulanmadı · K67 ↔ frontend 11.6 · K94 ve K125 elle doğrulama bekliyor ·
  K55 "yerel disk" ama yayın planı S3 diski kuruyor (yerine geçen K yok) · K11'in durum metni eskimiş.
- **Ana dosyaya işlenmemiş:** K49–K63, K72–K127 (yalnızca K1–K48 ve K64–K71 işlenmiş).
  `EK-FAZ-11/12`'nin ön koşulu ("bekleyen değişiklik önce commit'lensin") `9e428a8` ile sağlandı.
  `EK-FAZ-10` hiç yazılmadı (K87–K106 yalnızca backend `claude/FAZ-10-PLANI.md`'de).

## 4. Dış atıflar (senin düzelteceklerin)

**Backend / frontend depoları:** bu depoya giden 26 satır. Liste: [`INVENTORY.md`](INVENTORY.md) §7.
Özet: `claude/PHP-LARAVEL-SETUP.md` → `context/PHP-LARAVEL-SETUP.md` (10 satır),
`claude/Notlar/03-FRONTEND-YAPILACAKLAR.md` → `notes/03-FRONTEND-YAPILACAKLAR.md` (14 satır),
`claude/PHP-LARAVEL-SETUP-EK-FAZ-11.md` → `decisions/addenda/` (1), `claude/Notlar/04` (1; backend'in kendi `claude/Notlar/`'ı).

**Backend deposunun kendi `claude/` klasörü** (22 takipli dosya: EK-FAZ-5…9, FAZ-10-PLANI, devirler,
denetimler, Faz 6–9 prompt'ları) bu depoya ait içerik. Kapsam dışı olduğu için dokunulmadı; ayrı bir
işte buraya taşınması önerilir (`decisions/addenda/`, `phases/faz-05…10/`, `audits/2026-09-23-…`,
`audits/2026-09-24-test-audit/`, `audits/2026-10-09-…`, `prompts/`).

**Claude Code hafızası:** `C:\Users\ismail\.claude\projects\D--Projects-davetkart-davetkart-docs\memory\`
bu oturumda okunmadı ya da değiştirilmedi. İçinde `claude/…` yolu varsa güncellenmeli.

**claude.ai Project:** `PROMPT-YAYIN.md` ve `YAYIN-DEVIR.md` dosyaları claude.ai projesinde
`claude/YAYIN-PLANI.md` gibi yollar varsayıyor. Projedeki dosya yollarını/adlarını yeni yapıya göre
güncellemek isteyebilirsin (`context/`, `operations/deployment/`, `prompts/`).

## 5. Commit'ler

Commit'leri İsmail'in talimatıyla asistan attı. `main`'de yalnızca başlangıç commit'i var:

```
9e428a8 chore: Import existing documents as baseline                     (main)
```

Dalda (`docs/2026-11-12-restructure`), eskiden yeniye:

```
ec8af0d docs(restructure): Add inventory and migration plan
6b72b35 docs(structure): Add folder skeleton
fbf93da docs(structure): Move the project context file under context/
527f949 docs(structure): Move decision addenda under decisions/addenda/
3576ed9 docs(structure): Move phase records under phases/
619d192 docs(structure): Move agent prompts under prompts/
4baf2a1 docs(structure): Move deployment docs under operations/
39e7622 docs(structure): Move design approval assets under product/
0dfbe4a docs(structure): Move free notes under notes/
5b0f20b docs(structure): Move superseded files under archive/
b56cbd5 docs(archive): Mark superseded documents
31c1b9b docs(decisions): Add decision index
22c9d8a docs(readme): Describe each section
07abf52 docs(readme): Add repository map
70d1fe5 docs(agents): Add repository rules for AI assistants
(+ bu rapor) docs(restructure): Add restructure report
```

`docs(links): Update paths after restructure` commit'i **yok**: taşımadan sonra kırık Markdown bağlantısı
çıkmadı (belge katmanındaki tek bağlantı aynı klasöre birlikte taşındı). Düz metin yollar bilerek
değiştirilmedi (`MIGRATION-PLAN.md` §2 madde 7).

Birleştirme (henüz yapılmadı; `origin` = `davetkart-docs.git`):

```powershell
cd D:\Projects\davetkart\davetkart-docs
git switch main
git merge --no-ff docs/2026-11-12-restructure -m "docs: Restructure repository"
git push -u origin main
git switch -c audit/2026-11-12-full-system-audit
```

## 6. Eski yol → yeni yol (dosya dosya, git'in tanıdığı 277 yeniden adlandırma)

| Eski | Yeni |
|---|---|
| `claude/PROMPT-ARSIV-FAZ-4.md` | `archive/PROMPT-ARSIV-FAZ-4.md` |
| `claude/PROMPT.md` | `archive/PROMPT.md` |
| `claude/README.md` | `archive/davetkart-claude/README.md` |
| `scaffold-structure.ps1` | `archive/scaffold-structure.ps1` |
| `claude/PHP-LARAVEL-SETUP.md` | `context/PHP-LARAVEL-SETUP.md` |
| `claude/PHP-LARAVEL-SETUP-EK-FAZ-11.md` | `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` |
| `claude/PHP-LARAVEL-SETUP-EK-FAZ-12.md` | `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` |
| `claude/Notlar/01-FRONTEND-ANALIZI.md` | `notes/01-FRONTEND-ANALIZI.md` |
| `claude/Notlar/02-FRONTEND-BACKEND-TEMAS-NOKTALARI.md` | `notes/02-FRONTEND-BACKEND-TEMAS-NOKTALARI.md` |
| `claude/Notlar/03-FRONTEND-YAPILACAKLAR.md` | `notes/03-FRONTEND-YAPILACAKLAR.md` |
| `YAYIN-DEVIR.md` | `operations/deployment/YAYIN-DEVIR.md` |
| `YAYIN-PLANI.md` | `operations/deployment/YAYIN-PLANI.md` |
| `Claude outputs/FAZ-11-COMMIT-KOMUTLARI.md` | `phases/faz-11/FAZ-11-COMMIT-KOMUTLARI.md` |
| `Claude outputs/FAZ-11-FRONTEND-COMMIT-KOMUTLARI.md` | `phases/faz-11/FAZ-11-FRONTEND-COMMIT-KOMUTLARI.md` |
| `Claude outputs/FAZ-12-RAPOR.md` | `phases/faz-12/FAZ-12-RAPOR.md` |
| `Claude outputs/FAZ-13-COMMIT-KOMUTLARI.md` | `phases/faz-13/FAZ-13-COMMIT-KOMUTLARI.md` |
| `Claude outputs/FAZ-13-FRONTEND-COMMIT-KOMUTLARI.md` | `phases/faz-13/FAZ-13-FRONTEND-COMMIT-KOMUTLARI.md` |
| `Claude outputs/f13-ara/13.2/Order.php` | `phases/faz-13/f13-ara/13.2/Order.php` |
| `Claude outputs/f13-ara/13.9/types.ts` | `phases/faz-13/f13-ara/13.9/types.ts` |
| `Claude outputs/f13-ara/son/Order.php` | `phases/faz-13/f13-ara/son/Order.php` |
| `Claude outputs/f13-ara/son/types.ts` | `phases/faz-13/f13-ara/son/types.ts` |
| `Claude outputs/php-herdsiz.ini` | `phases/faz-13/php-herdsiz.ini` |
| `Claude outputs/teshis.php` | `phases/faz-13/teshis.php` |
| `Claude outputs/FAZ-14-COMMIT-KOMUTLARI.md` | `phases/faz-14/FAZ-14-COMMIT-KOMUTLARI.md` |
| `Claude outputs/FAZ-14-FRONTEND-COMMIT-KOMUTLARI.md` | `phases/faz-14/FAZ-14-FRONTEND-COMMIT-KOMUTLARI.md` |
| `Claude outputs/f14/backend/14.1/app/Actions/Invitation/DeleteInvitationAction.php` | `phases/faz-14/f14/backend/14.1/app/Actions/Invitation/DeleteInvitationAction.php` |
| `Claude outputs/f14/backend/14.1/app/Actions/Payment/ClaimReleasedOrderAction.php` | `phases/faz-14/f14/backend/14.1/app/Actions/Payment/ClaimReleasedOrderAction.php` |
| `Claude outputs/f14/backend/14.1/app/Models/Order.php` | `phases/faz-14/f14/backend/14.1/app/Models/Order.php` |
| `Claude outputs/f14/backend/14.1/database/migrations/2026_10_26_100000_add_consumed_at_to_orders_table.php` | `phases/faz-14/f14/backend/14.1/database/migrations/2026_10_26_100000_add_consumed_at_to_orders_table.php` |
| `Claude outputs/f14/backend/14.1/docs/rehber/app/Actions/Invitation/DeleteInvitationAction.md` | `phases/faz-14/f14/backend/14.1/docs/rehber/app/Actions/Invitation/DeleteInvitationAction.md` |
| `Claude outputs/f14/backend/14.1/docs/rehber/app/Actions/Payment/ClaimReleasedOrderAction.md` | `phases/faz-14/f14/backend/14.1/docs/rehber/app/Actions/Payment/ClaimReleasedOrderAction.md` |
| `Claude outputs/f14/backend/14.1/docs/rehber/app/Models/Order.md` | `phases/faz-14/f14/backend/14.1/docs/rehber/app/Models/Order.md` |
| `Claude outputs/f14/backend/14.1/docs/rehber/database/migrations/2026_10_26_100000_add_consumed_at_to_orders_table.md` | `phases/faz-14/f14/backend/14.1/docs/rehber/database/migrations/2026_10_26_100000_add_consumed_at_to_orders_table.md` |
| `Claude outputs/f14/backend/14.1/docs/rehber/tests/Feature/OrderConsumptionTest.md` | `phases/faz-14/f14/backend/14.1/docs/rehber/tests/Feature/OrderConsumptionTest.md` |
| `Claude outputs/f14/backend/14.1/tests/Feature/OrderConsumptionTest.php` | `phases/faz-14/f14/backend/14.1/tests/Feature/OrderConsumptionTest.php` |
| `Claude outputs/f14/backend/14.10/app/Actions/Account/ConfirmEmailChangeAction.php` | `phases/faz-14/f14/backend/14.10/app/Actions/Account/ConfirmEmailChangeAction.php` |
| `Claude outputs/f14/backend/14.10/app/Actions/Account/RequestEmailChangeAction.php` | `phases/faz-14/f14/backend/14.10/app/Actions/Account/RequestEmailChangeAction.php` |
| `Claude outputs/f14/backend/14.10/app/Enums/ErrorCode.php` | `phases/faz-14/f14/backend/14.10/app/Enums/ErrorCode.php` |
| `Claude outputs/f14/backend/14.10/app/Exceptions/EmailChangeFailedException.php` | `phases/faz-14/f14/backend/14.10/app/Exceptions/EmailChangeFailedException.php` |
| `Claude outputs/f14/backend/14.10/app/Http/Controllers/Api/V1/EmailChangeController.php` | `phases/faz-14/f14/backend/14.10/app/Http/Controllers/Api/V1/EmailChangeController.php` |
| `Claude outputs/f14/backend/14.10/app/Http/Controllers/Api/V1/PublicEmailChangeController.php` | `phases/faz-14/f14/backend/14.10/app/Http/Controllers/Api/V1/PublicEmailChangeController.php` |
| `Claude outputs/f14/backend/14.10/app/Http/Requests/Account/ConfirmEmailChangeRequest.php` | `phases/faz-14/f14/backend/14.10/app/Http/Requests/Account/ConfirmEmailChangeRequest.php` |
| `Claude outputs/f14/backend/14.10/app/Http/Requests/Account/RequestEmailChangeRequest.php` | `phases/faz-14/f14/backend/14.10/app/Http/Requests/Account/RequestEmailChangeRequest.php` |
| `Claude outputs/f14/backend/14.10/app/Notifications/EmailChangeConfirmationNotification.php` | `phases/faz-14/f14/backend/14.10/app/Notifications/EmailChangeConfirmationNotification.php` |
| `Claude outputs/f14/backend/14.10/app/Notifications/EmailChangedNotification.php` | `phases/faz-14/f14/backend/14.10/app/Notifications/EmailChangedNotification.php` |
| `Claude outputs/f14/backend/14.10/app/Support/EmailChangeLink.php` | `phases/faz-14/f14/backend/14.10/app/Support/EmailChangeLink.php` |
| `Claude outputs/f14/backend/14.10/config/davetkart.php` | `phases/faz-14/f14/backend/14.10/config/davetkart.php` |
| `Claude outputs/f14/backend/14.10/contracts/error-codes.json` | `phases/faz-14/f14/backend/14.10/contracts/error-codes.json` |
| `Claude outputs/f14/backend/14.10/docs/08-HATA-SOZLESMESI.md` | `phases/faz-14/f14/backend/14.10/docs/08-HATA-SOZLESMESI.md` |
| `Claude outputs/f14/backend/14.10/docs/rehber/app/Actions/Account/RequestEmailChangeAction.md` | `phases/faz-14/f14/backend/14.10/docs/rehber/app/Actions/Account/RequestEmailChangeAction.md` |
| `Claude outputs/f14/backend/14.10/docs/rehber/app/Enums/ErrorCode.md` | `phases/faz-14/f14/backend/14.10/docs/rehber/app/Enums/ErrorCode.md` |
| `Claude outputs/f14/backend/14.10/docs/rehber/config/davetkart.md` | `phases/faz-14/f14/backend/14.10/docs/rehber/config/davetkart.md` |
| `Claude outputs/f14/backend/14.10/docs/rehber/routes/api.md` | `phases/faz-14/f14/backend/14.10/docs/rehber/routes/api.md` |
| `Claude outputs/f14/backend/14.10/docs/rehber/tests/Feature/EmailChangeTest.md` | `phases/faz-14/f14/backend/14.10/docs/rehber/tests/Feature/EmailChangeTest.md` |
| `Claude outputs/f14/backend/14.10/routes/api.php` | `phases/faz-14/f14/backend/14.10/routes/api.php` |
| `Claude outputs/f14/backend/14.10/tests/Feature/EmailChangeTest.php` | `phases/faz-14/f14/backend/14.10/tests/Feature/EmailChangeTest.php` |
| `Claude outputs/f14/backend/14.10/tests/Unit/EmailChangedNotificationTest.php` | `phases/faz-14/f14/backend/14.10/tests/Unit/EmailChangedNotificationTest.php` |
| `Claude outputs/f14/backend/14.11/docs/rehber/fazlar/FAZ-14-ELLE-DOGRULAMA.md` | `phases/faz-14/f14/backend/14.11/docs/rehber/fazlar/FAZ-14-ELLE-DOGRULAMA.md` |
| `Claude outputs/f14/backend/14.11/docs/rehber/fazlar/FAZ-14.md` | `phases/faz-14/f14/backend/14.11/docs/rehber/fazlar/FAZ-14.md` |
| `Claude outputs/f14/backend/14.11/docs/rehber/fazlar/README.md` | `phases/faz-14/f14/backend/14.11/docs/rehber/fazlar/README.md` |
| `Claude outputs/f14/backend/14.2/app/Enums/RefundRequestStatus.php` | `phases/faz-14/f14/backend/14.2/app/Enums/RefundRequestStatus.php` |
| `Claude outputs/f14/backend/14.2/app/Models/Order.php` | `phases/faz-14/f14/backend/14.2/app/Models/Order.php` |
| `Claude outputs/f14/backend/14.2/app/Models/RefundRequest.php` | `phases/faz-14/f14/backend/14.2/app/Models/RefundRequest.php` |
| `Claude outputs/f14/backend/14.2/database/factories/RefundRequestFactory.php` | `phases/faz-14/f14/backend/14.2/database/factories/RefundRequestFactory.php` |
| `Claude outputs/f14/backend/14.2/database/migrations/2026_10_26_110000_create_refund_requests_table.php` | `phases/faz-14/f14/backend/14.2/database/migrations/2026_10_26_110000_create_refund_requests_table.php` |
| `Claude outputs/f14/backend/14.2/docs/rehber/app/Enums/RefundRequestStatus.md` | `phases/faz-14/f14/backend/14.2/docs/rehber/app/Enums/RefundRequestStatus.md` |
| `Claude outputs/f14/backend/14.2/docs/rehber/app/Models/Order.md` | `phases/faz-14/f14/backend/14.2/docs/rehber/app/Models/Order.md` |
| `Claude outputs/f14/backend/14.2/docs/rehber/app/Models/RefundRequest.md` | `phases/faz-14/f14/backend/14.2/docs/rehber/app/Models/RefundRequest.md` |
| `Claude outputs/f14/backend/14.2/docs/rehber/database/migrations/2026_10_26_110000_create_refund_requests_table.md` | `phases/faz-14/f14/backend/14.2/docs/rehber/database/migrations/2026_10_26_110000_create_refund_requests_table.md` |
| `Claude outputs/f14/backend/14.2/docs/rehber/tests/Feature/RefundRequestConstraintsTest.md` | `phases/faz-14/f14/backend/14.2/docs/rehber/tests/Feature/RefundRequestConstraintsTest.md` |
| `Claude outputs/f14/backend/14.2/tests/Feature/RefundRequestConstraintsTest.php` | `phases/faz-14/f14/backend/14.2/tests/Feature/RefundRequestConstraintsTest.php` |
| `Claude outputs/f14/backend/14.2/tests/Unit/RefundRequestStatusTest.php` | `phases/faz-14/f14/backend/14.2/tests/Unit/RefundRequestStatusTest.php` |
| `Claude outputs/f14/backend/14.3/app/Actions/Account/EntitlementRight.php` | `phases/faz-14/f14/backend/14.3/app/Actions/Account/EntitlementRight.php` |
| `Claude outputs/f14/backend/14.3/app/Actions/Account/EntitlementSummary.php` | `phases/faz-14/f14/backend/14.3/app/Actions/Account/EntitlementSummary.php` |
| `Claude outputs/f14/backend/14.3/app/Actions/Account/SummarizeEntitlementsAction.php` | `phases/faz-14/f14/backend/14.3/app/Actions/Account/SummarizeEntitlementsAction.php` |
| `Claude outputs/f14/backend/14.3/app/Actions/Account/TierEntitlements.php` | `phases/faz-14/f14/backend/14.3/app/Actions/Account/TierEntitlements.php` |
| `Claude outputs/f14/backend/14.3/app/Enums/EntitlementState.php` | `phases/faz-14/f14/backend/14.3/app/Enums/EntitlementState.php` |
| `Claude outputs/f14/backend/14.3/app/Enums/RefundBlocker.php` | `phases/faz-14/f14/backend/14.3/app/Enums/RefundBlocker.php` |
| `Claude outputs/f14/backend/14.3/app/Services/Refund/RefundEligibility.php` | `phases/faz-14/f14/backend/14.3/app/Services/Refund/RefundEligibility.php` |
| `Claude outputs/f14/backend/14.3/config/davetkart.php` | `phases/faz-14/f14/backend/14.3/config/davetkart.php` |
| `Claude outputs/f14/backend/14.3/docs/rehber/app/Actions/Account/SummarizeEntitlementsAction.md` | `phases/faz-14/f14/backend/14.3/docs/rehber/app/Actions/Account/SummarizeEntitlementsAction.md` |
| `Claude outputs/f14/backend/14.3/docs/rehber/app/Services/Refund/RefundEligibility.md` | `phases/faz-14/f14/backend/14.3/docs/rehber/app/Services/Refund/RefundEligibility.md` |
| `Claude outputs/f14/backend/14.3/docs/rehber/config/davetkart.md` | `phases/faz-14/f14/backend/14.3/docs/rehber/config/davetkart.md` |
| `Claude outputs/f14/backend/14.3/docs/rehber/tests/Feature/SummarizeEntitlementsActionTest.md` | `phases/faz-14/f14/backend/14.3/docs/rehber/tests/Feature/SummarizeEntitlementsActionTest.md` |
| `Claude outputs/f14/backend/14.3/tests/Feature/SummarizeEntitlementsActionTest.php` | `phases/faz-14/f14/backend/14.3/tests/Feature/SummarizeEntitlementsActionTest.php` |
| `Claude outputs/f14/backend/14.4/app/Http/Controllers/Api/V1/AccountController.php` | `phases/faz-14/f14/backend/14.4/app/Http/Controllers/Api/V1/AccountController.php` |
| `Claude outputs/f14/backend/14.4/app/Http/Resources/EntitlementSummaryResource.php` | `phases/faz-14/f14/backend/14.4/app/Http/Resources/EntitlementSummaryResource.php` |
| `Claude outputs/f14/backend/14.4/docs/rehber/app/Http/Controllers/Api/V1/AccountController.md` | `phases/faz-14/f14/backend/14.4/docs/rehber/app/Http/Controllers/Api/V1/AccountController.md` |
| `Claude outputs/f14/backend/14.4/docs/rehber/app/Http/Resources/EntitlementSummaryResource.md` | `phases/faz-14/f14/backend/14.4/docs/rehber/app/Http/Resources/EntitlementSummaryResource.md` |
| `Claude outputs/f14/backend/14.4/docs/rehber/routes/api.md` | `phases/faz-14/f14/backend/14.4/docs/rehber/routes/api.md` |
| `Claude outputs/f14/backend/14.4/docs/rehber/tests/Feature/AccountEntitlementsTest.md` | `phases/faz-14/f14/backend/14.4/docs/rehber/tests/Feature/AccountEntitlementsTest.md` |
| `Claude outputs/f14/backend/14.4/routes/api.php` | `phases/faz-14/f14/backend/14.4/routes/api.php` |
| `Claude outputs/f14/backend/14.4/tests/Feature/AccountEntitlementsTest.php` | `phases/faz-14/f14/backend/14.4/tests/Feature/AccountEntitlementsTest.php` |
| `Claude outputs/f14/backend/14.5/app/Actions/Payment/ClaimReleasedOrderAction.php` | `phases/faz-14/f14/backend/14.5/app/Actions/Payment/ClaimReleasedOrderAction.php` |
| `Claude outputs/f14/backend/14.5/app/Actions/Refund/RequestRefundAction.php` | `phases/faz-14/f14/backend/14.5/app/Actions/Refund/RequestRefundAction.php` |
| `Claude outputs/f14/backend/14.5/app/Actions/Refund/WithdrawRefundRequestAction.php` | `phases/faz-14/f14/backend/14.5/app/Actions/Refund/WithdrawRefundRequestAction.php` |
| `Claude outputs/f14/backend/14.5/app/Enums/ErrorCode.php` | `phases/faz-14/f14/backend/14.5/app/Enums/ErrorCode.php` |
| `Claude outputs/f14/backend/14.5/app/Exceptions/RefundNotAllowedException.php` | `phases/faz-14/f14/backend/14.5/app/Exceptions/RefundNotAllowedException.php` |
| `Claude outputs/f14/backend/14.5/app/Http/Controllers/Api/V1/RefundRequestController.php` | `phases/faz-14/f14/backend/14.5/app/Http/Controllers/Api/V1/RefundRequestController.php` |
| `Claude outputs/f14/backend/14.5/app/Http/Requests/Refund/StoreRefundRequestRequest.php` | `phases/faz-14/f14/backend/14.5/app/Http/Requests/Refund/StoreRefundRequestRequest.php` |
| `Claude outputs/f14/backend/14.5/app/Http/Resources/RefundRequestResource.php` | `phases/faz-14/f14/backend/14.5/app/Http/Resources/RefundRequestResource.php` |
| `Claude outputs/f14/backend/14.5/contracts/error-codes.json` | `phases/faz-14/f14/backend/14.5/contracts/error-codes.json` |
| `Claude outputs/f14/backend/14.5/docs/08-HATA-SOZLESMESI.md` | `phases/faz-14/f14/backend/14.5/docs/08-HATA-SOZLESMESI.md` |
| `Claude outputs/f14/backend/14.5/docs/rehber/app/Actions/Payment/ClaimReleasedOrderAction.md` | `phases/faz-14/f14/backend/14.5/docs/rehber/app/Actions/Payment/ClaimReleasedOrderAction.md` |
| `Claude outputs/f14/backend/14.5/docs/rehber/app/Actions/Refund/RequestRefundAction.md` | `phases/faz-14/f14/backend/14.5/docs/rehber/app/Actions/Refund/RequestRefundAction.md` |
| `Claude outputs/f14/backend/14.5/docs/rehber/app/Enums/ErrorCode.md` | `phases/faz-14/f14/backend/14.5/docs/rehber/app/Enums/ErrorCode.md` |
| `Claude outputs/f14/backend/14.5/docs/rehber/routes/api.md` | `phases/faz-14/f14/backend/14.5/docs/rehber/routes/api.md` |
| `Claude outputs/f14/backend/14.5/docs/rehber/tests/Feature/RefundRequestTest.md` | `phases/faz-14/f14/backend/14.5/docs/rehber/tests/Feature/RefundRequestTest.md` |
| `Claude outputs/f14/backend/14.5/routes/api.php` | `phases/faz-14/f14/backend/14.5/routes/api.php` |
| `Claude outputs/f14/backend/14.5/tests/Feature/RefundRequestTest.php` | `phases/faz-14/f14/backend/14.5/tests/Feature/RefundRequestTest.php` |
| `Claude outputs/f14/backend/14.6/app/Actions/Refund/ResolveRefundRequestAction.php` | `phases/faz-14/f14/backend/14.6/app/Actions/Refund/ResolveRefundRequestAction.php` |
| `Claude outputs/f14/backend/14.6/app/Console/Commands/ApproveRefundRequest.php` | `phases/faz-14/f14/backend/14.6/app/Console/Commands/ApproveRefundRequest.php` |
| `Claude outputs/f14/backend/14.6/app/Console/Commands/Concerns/ResolvesRefundRequests.php` | `phases/faz-14/f14/backend/14.6/app/Console/Commands/Concerns/ResolvesRefundRequests.php` |
| `Claude outputs/f14/backend/14.6/app/Console/Commands/ListRefundRequests.php` | `phases/faz-14/f14/backend/14.6/app/Console/Commands/ListRefundRequests.php` |
| `Claude outputs/f14/backend/14.6/app/Console/Commands/RejectRefundRequest.php` | `phases/faz-14/f14/backend/14.6/app/Console/Commands/RejectRefundRequest.php` |
| `Claude outputs/f14/backend/14.6/app/Notifications/RefundRequestResolvedNotification.php` | `phases/faz-14/f14/backend/14.6/app/Notifications/RefundRequestResolvedNotification.php` |
| `Claude outputs/f14/backend/14.6/docs/rehber/PROJE-KOMUTLARI.md` | `phases/faz-14/f14/backend/14.6/docs/rehber/PROJE-KOMUTLARI.md` |
| `Claude outputs/f14/backend/14.6/docs/rehber/app/Actions/Refund/ResolveRefundRequestAction.md` | `phases/faz-14/f14/backend/14.6/docs/rehber/app/Actions/Refund/ResolveRefundRequestAction.md` |
| `Claude outputs/f14/backend/14.6/docs/rehber/app/Console/Commands/RefundCommands.md` | `phases/faz-14/f14/backend/14.6/docs/rehber/app/Console/Commands/RefundCommands.md` |
| `Claude outputs/f14/backend/14.6/docs/rehber/tests/Feature/RefundCommandsTest.md` | `phases/faz-14/f14/backend/14.6/docs/rehber/tests/Feature/RefundCommandsTest.md` |
| `Claude outputs/f14/backend/14.6/tests/Feature/RefundCommandsTest.php` | `phases/faz-14/f14/backend/14.6/tests/Feature/RefundCommandsTest.php` |
| `Claude outputs/f14/backend/14.7/app/Actions/Account/UpdateProfileAction.php` | `phases/faz-14/f14/backend/14.7/app/Actions/Account/UpdateProfileAction.php` |
| `Claude outputs/f14/backend/14.7/app/Http/Controllers/Api/V1/ProfileController.php` | `phases/faz-14/f14/backend/14.7/app/Http/Controllers/Api/V1/ProfileController.php` |
| `Claude outputs/f14/backend/14.7/app/Http/Requests/Account/UpdateProfileRequest.php` | `phases/faz-14/f14/backend/14.7/app/Http/Requests/Account/UpdateProfileRequest.php` |
| `Claude outputs/f14/backend/14.7/docs/rehber/app/Actions/Account/UpdateProfileAction.md` | `phases/faz-14/f14/backend/14.7/docs/rehber/app/Actions/Account/UpdateProfileAction.md` |
| `Claude outputs/f14/backend/14.7/docs/rehber/routes/api.md` | `phases/faz-14/f14/backend/14.7/docs/rehber/routes/api.md` |
| `Claude outputs/f14/backend/14.7/routes/api.php` | `phases/faz-14/f14/backend/14.7/routes/api.php` |
| `Claude outputs/f14/backend/14.7/tests/Feature/ProfileUpdateTest.php` | `phases/faz-14/f14/backend/14.7/tests/Feature/ProfileUpdateTest.php` |
| `Claude outputs/f14/backend/14.8/app/Actions/Account/ChangePasswordAction.php` | `phases/faz-14/f14/backend/14.8/app/Actions/Account/ChangePasswordAction.php` |
| `Claude outputs/f14/backend/14.8/app/Http/Controllers/Api/V1/PasswordController.php` | `phases/faz-14/f14/backend/14.8/app/Http/Controllers/Api/V1/PasswordController.php` |
| `Claude outputs/f14/backend/14.8/app/Http/Requests/Account/ChangePasswordRequest.php` | `phases/faz-14/f14/backend/14.8/app/Http/Requests/Account/ChangePasswordRequest.php` |
| `Claude outputs/f14/backend/14.8/app/Notifications/PasswordChangedNotification.php` | `phases/faz-14/f14/backend/14.8/app/Notifications/PasswordChangedNotification.php` |
| `Claude outputs/f14/backend/14.8/docs/rehber/app/Actions/Account/ChangePasswordAction.md` | `phases/faz-14/f14/backend/14.8/docs/rehber/app/Actions/Account/ChangePasswordAction.md` |
| `Claude outputs/f14/backend/14.8/docs/rehber/routes/api.md` | `phases/faz-14/f14/backend/14.8/docs/rehber/routes/api.md` |
| `Claude outputs/f14/backend/14.8/routes/api.php` | `phases/faz-14/f14/backend/14.8/routes/api.php` |
| `Claude outputs/f14/backend/14.8/tests/Feature/PasswordChangeTest.php` | `phases/faz-14/f14/backend/14.8/tests/Feature/PasswordChangeTest.php` |
| `Claude outputs/f14/backend/14.9/app/Actions/Auth/IssueApiTokenAction.php` | `phases/faz-14/f14/backend/14.9/app/Actions/Auth/IssueApiTokenAction.php` |
| `Claude outputs/f14/backend/14.9/app/Actions/Auth/LoginUserAction.php` | `phases/faz-14/f14/backend/14.9/app/Actions/Auth/LoginUserAction.php` |
| `Claude outputs/f14/backend/14.9/app/Actions/Auth/RegisterUserAction.php` | `phases/faz-14/f14/backend/14.9/app/Actions/Auth/RegisterUserAction.php` |
| `Claude outputs/f14/backend/14.9/app/Actions/Auth/RevokeOtherSessionsAction.php` | `phases/faz-14/f14/backend/14.9/app/Actions/Auth/RevokeOtherSessionsAction.php` |
| `Claude outputs/f14/backend/14.9/app/Actions/Auth/RevokeSessionAction.php` | `phases/faz-14/f14/backend/14.9/app/Actions/Auth/RevokeSessionAction.php` |
| `Claude outputs/f14/backend/14.9/app/Http/Controllers/Api/V1/AuthController.php` | `phases/faz-14/f14/backend/14.9/app/Http/Controllers/Api/V1/AuthController.php` |
| `Claude outputs/f14/backend/14.9/app/Http/Controllers/Api/V1/SessionController.php` | `phases/faz-14/f14/backend/14.9/app/Http/Controllers/Api/V1/SessionController.php` |
| `Claude outputs/f14/backend/14.9/app/Http/Resources/SessionResource.php` | `phases/faz-14/f14/backend/14.9/app/Http/Resources/SessionResource.php` |
| `Claude outputs/f14/backend/14.9/app/Support/DeviceLabel.php` | `phases/faz-14/f14/backend/14.9/app/Support/DeviceLabel.php` |
| `Claude outputs/f14/backend/14.9/database/migrations/2026_10_26_120000_add_user_agent_to_personal_access_tokens_table.php` | `phases/faz-14/f14/backend/14.9/database/migrations/2026_10_26_120000_add_user_agent_to_personal_access_tokens_table.php` |
| `Claude outputs/f14/backend/14.9/docs/rehber/app/Actions/Auth/IssueApiTokenAction.md` | `phases/faz-14/f14/backend/14.9/docs/rehber/app/Actions/Auth/IssueApiTokenAction.md` |
| `Claude outputs/f14/backend/14.9/docs/rehber/app/Actions/Auth/LoginUserAction.md` | `phases/faz-14/f14/backend/14.9/docs/rehber/app/Actions/Auth/LoginUserAction.md` |
| `Claude outputs/f14/backend/14.9/docs/rehber/app/Actions/Auth/RegisterUserAction.md` | `phases/faz-14/f14/backend/14.9/docs/rehber/app/Actions/Auth/RegisterUserAction.md` |
| `Claude outputs/f14/backend/14.9/docs/rehber/database/migrations/2026_10_26_120000_add_user_agent_to_personal_access_tokens_table.md` | `phases/faz-14/f14/backend/14.9/docs/rehber/database/migrations/2026_10_26_120000_add_user_agent_to_personal_access_tokens_table.md` |
| `Claude outputs/f14/backend/14.9/docs/rehber/routes/api.md` | `phases/faz-14/f14/backend/14.9/docs/rehber/routes/api.md` |
| `Claude outputs/f14/backend/14.9/routes/api.php` | `phases/faz-14/f14/backend/14.9/routes/api.php` |
| `Claude outputs/f14/backend/14.9/tests/Feature/SessionTest.php` | `phases/faz-14/f14/backend/14.9/tests/Feature/SessionTest.php` |
| `Claude outputs/f14/backend/14.9/tests/Unit/DeviceLabelTest.php` | `phases/faz-14/f14/backend/14.9/tests/Unit/DeviceLabelTest.php` |
| `Claude outputs/f14/frontend/14.12/docs/rehber/src/services/account.md` | `phases/faz-14/f14/frontend/14.12/docs/rehber/src/services/account.md` |
| `Claude outputs/f14/frontend/14.12/docs/rehber/src/stores/useAccountStore.md` | `phases/faz-14/f14/frontend/14.12/docs/rehber/src/stores/useAccountStore.md` |
| `Claude outputs/f14/frontend/14.12/scripts/verify-endpoints.ts` | `phases/faz-14/f14/frontend/14.12/scripts/verify-endpoints.ts` |
| `Claude outputs/f14/frontend/14.12/src/contracts/error-codes.json` | `phases/faz-14/f14/frontend/14.12/src/contracts/error-codes.json` |
| `Claude outputs/f14/frontend/14.12/src/locales/en/errors.json` | `phases/faz-14/f14/frontend/14.12/src/locales/en/errors.json` |
| `Claude outputs/f14/frontend/14.12/src/locales/tr/errors.json` | `phases/faz-14/f14/frontend/14.12/src/locales/tr/errors.json` |
| `Claude outputs/f14/frontend/14.12/src/services/account.ts` | `phases/faz-14/f14/frontend/14.12/src/services/account.ts` |
| `Claude outputs/f14/frontend/14.12/src/stores/sessionActions.ts` | `phases/faz-14/f14/frontend/14.12/src/stores/sessionActions.ts` |
| `Claude outputs/f14/frontend/14.12/src/stores/useAccountStore.ts` | `phases/faz-14/f14/frontend/14.12/src/stores/useAccountStore.ts` |
| `Claude outputs/f14/frontend/14.12/src/stores/useAuthStore.ts` | `phases/faz-14/f14/frontend/14.12/src/stores/useAuthStore.ts` |
| `Claude outputs/f14/frontend/14.12/src/types.ts` | `phases/faz-14/f14/frontend/14.12/src/types.ts` |
| `Claude outputs/f14/frontend/14.12/src/utils/toDisplayError.ts` | `phases/faz-14/f14/frontend/14.12/src/utils/toDisplayError.ts` |
| `Claude outputs/f14/frontend/14.13/src/components/account/AccountCard.tsx` | `phases/faz-14/f14/frontend/14.13/src/components/account/AccountCard.tsx` |
| `Claude outputs/f14/frontend/14.13/src/components/account/AccountNav.tsx` | `phases/faz-14/f14/frontend/14.13/src/components/account/AccountNav.tsx` |
| `Claude outputs/f14/frontend/14.13/src/components/account/DeleteAccountCard.tsx` | `phases/faz-14/f14/frontend/14.13/src/components/account/DeleteAccountCard.tsx` |
| `Claude outputs/f14/frontend/14.13/src/components/account/EmailChangeForm.tsx` | `phases/faz-14/f14/frontend/14.13/src/components/account/EmailChangeForm.tsx` |
| `Claude outputs/f14/frontend/14.13/src/components/account/FormField.tsx` | `phases/faz-14/f14/frontend/14.13/src/components/account/FormField.tsx` |
| `Claude outputs/f14/frontend/14.13/src/components/account/OrdersList.tsx` | `phases/faz-14/f14/frontend/14.13/src/components/account/OrdersList.tsx` |
| `Claude outputs/f14/frontend/14.13/src/components/account/PasswordForm.tsx` | `phases/faz-14/f14/frontend/14.13/src/components/account/PasswordForm.tsx` |
| `Claude outputs/f14/frontend/14.13/src/components/account/ProfileForm.tsx` | `phases/faz-14/f14/frontend/14.13/src/components/account/ProfileForm.tsx` |
| `Claude outputs/f14/frontend/14.13/src/components/account/RightRow.tsx` | `phases/faz-14/f14/frontend/14.13/src/components/account/RightRow.tsx` |
| `Claude outputs/f14/frontend/14.13/src/components/account/SessionList.tsx` | `phases/faz-14/f14/frontend/14.13/src/components/account/SessionList.tsx` |
| `Claude outputs/f14/frontend/14.13/src/components/account/TierRightsGrid.tsx` | `phases/faz-14/f14/frontend/14.13/src/components/account/TierRightsGrid.tsx` |
| `Claude outputs/f14/frontend/14.13/src/hooks/useAccountEntitlements.ts` | `phases/faz-14/f14/frontend/14.13/src/hooks/useAccountEntitlements.ts` |
| `Claude outputs/f14/frontend/14.13/src/utils/accountLabels.ts` | `phases/faz-14/f14/frontend/14.13/src/utils/accountLabels.ts` |
| `Claude outputs/f14/frontend/14.14/docs/rehber/src/pages/AccountPage.md` | `phases/faz-14/f14/frontend/14.14/docs/rehber/src/pages/AccountPage.md` |
| `Claude outputs/f14/frontend/14.14/docs/rehber/src/pages/account/README.md` | `phases/faz-14/f14/frontend/14.14/docs/rehber/src/pages/account/README.md` |
| `Claude outputs/f14/frontend/14.14/src/App.tsx` | `phases/faz-14/f14/frontend/14.14/src/App.tsx` |
| `Claude outputs/f14/frontend/14.14/src/pages/AccountPage.tsx` | `phases/faz-14/f14/frontend/14.14/src/pages/AccountPage.tsx` |
| `Claude outputs/f14/frontend/14.14/src/pages/DashboardPage.tsx` | `phases/faz-14/f14/frontend/14.14/src/pages/DashboardPage.tsx` |
| `Claude outputs/f14/frontend/14.14/src/pages/EmailChangeConfirmPage.tsx` | `phases/faz-14/f14/frontend/14.14/src/pages/EmailChangeConfirmPage.tsx` |
| `Claude outputs/f14/frontend/14.14/src/pages/PricingPage.tsx` | `phases/faz-14/f14/frontend/14.14/src/pages/PricingPage.tsx` |
| `Claude outputs/f14/frontend/14.14/src/pages/account/AccountOrdersSection.tsx` | `phases/faz-14/f14/frontend/14.14/src/pages/account/AccountOrdersSection.tsx` |
| `Claude outputs/f14/frontend/14.14/src/pages/account/AccountOverviewSection.tsx` | `phases/faz-14/f14/frontend/14.14/src/pages/account/AccountOverviewSection.tsx` |
| `Claude outputs/f14/frontend/14.14/src/pages/account/AccountPlansSection.tsx` | `phases/faz-14/f14/frontend/14.14/src/pages/account/AccountPlansSection.tsx` |
| `Claude outputs/f14/frontend/14.14/src/pages/account/AccountPrivacySection.tsx` | `phases/faz-14/f14/frontend/14.14/src/pages/account/AccountPrivacySection.tsx` |
| `Claude outputs/f14/frontend/14.14/src/pages/account/AccountSecuritySection.tsx` | `phases/faz-14/f14/frontend/14.14/src/pages/account/AccountSecuritySection.tsx` |
| `Claude outputs/FRONTEND-YAKALAMA-PLANI.md` | `phases/frontend-catch-up/FRONTEND-YAKALAMA-PLANI.md` |
| `claude/hero-video-onay/generate_hero_video.py` | `product/hero-video-onay/generate_hero_video.py` |
| `claude/hero-video-onay/hero-bg-poster.jpg` | `product/hero-video-onay/hero-bg-poster.jpg` |
| `claude/hero-video-onay/hero-bg.mp4` | `product/hero-video-onay/hero-bg.mp4` |
| `claude/hero-video-onay/hero-bg.webm` | `product/hero-video-onay/hero-bg.webm` |
| `claude/hero-video-onay/onizleme.html` | `product/hero-video-onay/onizleme.html` |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-desktop-poster.jpg` | `product/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-desktop-poster.jpg` |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-desktop.mp4` | `product/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-desktop.mp4` |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-desktop.webm` | `product/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-desktop.webm` |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-mobile-poster.jpg` | `product/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-mobile-poster.jpg` |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-mobile.mp4` | `product/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-mobile.mp4` |
| `claude/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-mobile.webm` | `product/video-onay/baby-shower-kabarcik/baby-shower-kabarcik-mobile.webm` |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-desktop-poster.jpg` | `product/video-onay/deniz-isiltisi/deniz-isiltisi-desktop-poster.jpg` |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-desktop.mp4` | `product/video-onay/deniz-isiltisi/deniz-isiltisi-desktop.mp4` |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-desktop.webm` | `product/video-onay/deniz-isiltisi/deniz-isiltisi-desktop.webm` |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-mobile-poster.jpg` | `product/video-onay/deniz-isiltisi/deniz-isiltisi-mobile-poster.jpg` |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-mobile.mp4` | `product/video-onay/deniz-isiltisi/deniz-isiltisi-mobile.mp4` |
| `claude/video-onay/deniz-isiltisi/deniz-isiltisi-mobile.webm` | `product/video-onay/deniz-isiltisi/deniz-isiltisi-mobile.webm` |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-desktop-poster.jpg` | `product/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-desktop-poster.jpg` |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-desktop.mp4` | `product/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-desktop.mp4` |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-desktop.webm` | `product/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-desktop.webm` |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-mobile-poster.jpg` | `product/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-mobile-poster.jpg` |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-mobile.mp4` | `product/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-mobile.mp4` |
| `claude/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-mobile.webm` | `product/video-onay/dogum-gunu-konfeti/dogum-gunu-konfeti-mobile.webm` |
| `claude/video-onay/generate_category_videos.py` | `product/video-onay/generate_category_videos.py` |
| `claude/video-onay/generate_premium_videos.py` | `product/video-onay/generate_premium_videos.py` |
| `claude/video-onay/generate_wedding_videos.py` | `product/video-onay/generate_wedding_videos.py` |
| `claude/video-onay/gokyuzu-ruyasi/generate_sky_video.py` | `product/video-onay/gokyuzu-ruyasi/generate_sky_video.py` |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-desktop-poster.jpg` | `product/video-onay/gokyuzu-ruyasi/gokyuzu-desktop-poster.jpg` |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-desktop.mp4` | `product/video-onay/gokyuzu-ruyasi/gokyuzu-desktop.mp4` |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-desktop.webm` | `product/video-onay/gokyuzu-ruyasi/gokyuzu-desktop.webm` |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-mobile-poster.jpg` | `product/video-onay/gokyuzu-ruyasi/gokyuzu-mobile-poster.jpg` |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-mobile.mp4` | `product/video-onay/gokyuzu-ruyasi/gokyuzu-mobile.mp4` |
| `claude/video-onay/gokyuzu-ruyasi/gokyuzu-mobile.webm` | `product/video-onay/gokyuzu-ruyasi/gokyuzu-mobile.webm` |
| `claude/video-onay/gokyuzu-ruyasi/onizleme.html` | `product/video-onay/gokyuzu-ruyasi/onizleme.html` |
| `claude/video-onay/gokyuzu-ruyasi/render.log` | `product/video-onay/gokyuzu-ruyasi/render.log` |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-desktop-poster.jpg` | `product/video-onay/gul-yapraklari/gul-yapraklari-desktop-poster.jpg` |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-desktop.mp4` | `product/video-onay/gul-yapraklari/gul-yapraklari-desktop.mp4` |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-desktop.webm` | `product/video-onay/gul-yapraklari/gul-yapraklari-desktop.webm` |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-mobile-poster.jpg` | `product/video-onay/gul-yapraklari/gul-yapraklari-mobile-poster.jpg` |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-mobile.mp4` | `product/video-onay/gul-yapraklari/gul-yapraklari-mobile.mp4` |
| `claude/video-onay/gul-yapraklari/gul-yapraklari-mobile.webm` | `product/video-onay/gul-yapraklari/gul-yapraklari-mobile.webm` |
| `claude/video-onay/kina-bordo/kina-bordo-desktop-poster.jpg` | `product/video-onay/kina-bordo/kina-bordo-desktop-poster.jpg` |
| `claude/video-onay/kina-bordo/kina-bordo-desktop.mp4` | `product/video-onay/kina-bordo/kina-bordo-desktop.mp4` |
| `claude/video-onay/kina-bordo/kina-bordo-desktop.webm` | `product/video-onay/kina-bordo/kina-bordo-desktop.webm` |
| `claude/video-onay/kina-bordo/kina-bordo-mobile-poster.jpg` | `product/video-onay/kina-bordo/kina-bordo-mobile-poster.jpg` |
| `claude/video-onay/kina-bordo/kina-bordo-mobile.mp4` | `product/video-onay/kina-bordo/kina-bordo-mobile.mp4` |
| `claude/video-onay/kina-bordo/kina-bordo-mobile.webm` | `product/video-onay/kina-bordo/kina-bordo-mobile.webm` |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-desktop-poster.jpg` | `product/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-desktop-poster.jpg` |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-desktop.mp4` | `product/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-desktop.mp4` |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-desktop.webm` | `product/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-desktop.webm` |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-mobile-poster.jpg` | `product/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-mobile-poster.jpg` |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-mobile.mp4` | `product/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-mobile.mp4` |
| `claude/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-mobile.webm` | `product/video-onay/mezuniyet-lacivert/mezuniyet-lacivert-mobile.webm` |
| `claude/video-onay/mum-isigi/mum-isigi-desktop-poster.jpg` | `product/video-onay/mum-isigi/mum-isigi-desktop-poster.jpg` |
| `claude/video-onay/mum-isigi/mum-isigi-desktop.mp4` | `product/video-onay/mum-isigi/mum-isigi-desktop.mp4` |
| `claude/video-onay/mum-isigi/mum-isigi-desktop.webm` | `product/video-onay/mum-isigi/mum-isigi-desktop.webm` |
| `claude/video-onay/mum-isigi/mum-isigi-mobile-poster.jpg` | `product/video-onay/mum-isigi/mum-isigi-mobile-poster.jpg` |
| `claude/video-onay/mum-isigi/mum-isigi-mobile.mp4` | `product/video-onay/mum-isigi/mum-isigi-mobile.mp4` |
| `claude/video-onay/mum-isigi/mum-isigi-mobile.webm` | `product/video-onay/mum-isigi/mum-isigi-mobile.webm` |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-desktop-poster.jpg` | `product/video-onay/nisan-sampanya/nisan-sampanya-desktop-poster.jpg` |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-desktop.mp4` | `product/video-onay/nisan-sampanya/nisan-sampanya-desktop.mp4` |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-desktop.webm` | `product/video-onay/nisan-sampanya/nisan-sampanya-desktop.webm` |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-mobile-poster.jpg` | `product/video-onay/nisan-sampanya/nisan-sampanya-mobile-poster.jpg` |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-mobile.mp4` | `product/video-onay/nisan-sampanya/nisan-sampanya-mobile.mp4` |
| `claude/video-onay/nisan-sampanya/nisan-sampanya-mobile.webm` | `product/video-onay/nisan-sampanya/nisan-sampanya-mobile.webm` |
| `claude/video-onay/onizleme-tumu.html` | `product/video-onay/onizleme-tumu.html` |
| `claude/video-onay/parti-aurora/parti-aurora-desktop-poster.jpg` | `product/video-onay/parti-aurora/parti-aurora-desktop-poster.jpg` |
| `claude/video-onay/parti-aurora/parti-aurora-desktop.mp4` | `product/video-onay/parti-aurora/parti-aurora-desktop.mp4` |
| `claude/video-onay/parti-aurora/parti-aurora-desktop.webm` | `product/video-onay/parti-aurora/parti-aurora-desktop.webm` |
| `claude/video-onay/parti-aurora/parti-aurora-mobile-poster.jpg` | `product/video-onay/parti-aurora/parti-aurora-mobile-poster.jpg` |
| `claude/video-onay/parti-aurora/parti-aurora-mobile.mp4` | `product/video-onay/parti-aurora/parti-aurora-mobile.mp4` |
| `claude/video-onay/parti-aurora/parti-aurora-mobile.webm` | `product/video-onay/parti-aurora/parti-aurora-mobile.webm` |
| `claude/video-onay/premium-lab/dugun-onyx.html` | `product/video-onay/premium-lab/dugun-onyx.html` |
| `claude/video-onay/premium-lab/dugun-sahil.html` | `product/video-onay/premium-lab/dugun-sahil.html` |
| `claude/video-onay/premium-lab/index.html` | `product/video-onay/premium-lab/index.html` |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-desktop-poster.jpg` | `product/video-onay/sunnet-yildiz/sunnet-yildiz-desktop-poster.jpg` |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-desktop.mp4` | `product/video-onay/sunnet-yildiz/sunnet-yildiz-desktop.mp4` |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-desktop.webm` | `product/video-onay/sunnet-yildiz/sunnet-yildiz-desktop.webm` |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-mobile-poster.jpg` | `product/video-onay/sunnet-yildiz/sunnet-yildiz-mobile-poster.jpg` |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-mobile.mp4` | `product/video-onay/sunnet-yildiz/sunnet-yildiz-mobile.mp4` |
| `claude/video-onay/sunnet-yildiz/sunnet-yildiz-mobile.webm` | `product/video-onay/sunnet-yildiz/sunnet-yildiz-mobile.webm` |
| `claude/video-onay/video_engine.py` | `product/video-onay/video_engine.py` |
| `PROMPT-FAZ-11.md` | `prompts/PROMPT-FAZ-11.md` |
| `PROMPT-FAZ-12.md` | `prompts/PROMPT-FAZ-12.md` |
| `PROMPT-YAYIN.md` | `prompts/PROMPT-YAYIN.md` |

## 7. `CLAUDE.md` tam metni

````markdown
# CLAUDE.md — davetkart-docs kuralları

Bu dosya bu depoda çalışan **her** yapay zekâ asistanı için bağlayıcıdır. Başka bir dokümanla
çelişirse bu dosya kazanır. Uzun açıklama için bağlantılara bak.

## 1. Bu depo nedir

- DavetKart'ın (dijital davetiye SaaS'ı) **kod dışı** dokümanları. Eski adı `claude/`.
- Kod depoları burada **değil**: `../davetkart-backend-php-laravel`, `../davetkart-frontent`.
  Onların kod kılavuzları (`docs/rehber/`) da kendi depolarında kalır.
- Yığın: backend PHP 8.5 + Laravel 13 (modüler monolit, Action katmanı) · frontend React 19 + TypeScript.

## 2. Oturum başında oku (sırayla)

1. [`README.md`](README.md): harita.
2. [`context/PHP-LARAVEL-SETUP.md`](context/PHP-LARAVEL-SETUP.md): §9 şu anki durum, §10 yol
   haritası, §11 ihlal edilemez kurallar, §2 çalışma kuralları.
3. [`decisions/DECISION-INDEX.md`](decisions/DECISION-INDEX.md): K numaraları, sıradaki boş numara.
4. İşle ilgili `phases/faz-NN/` klasörü (yayın işi için `operations/deployment/`).

## 3. Klasör haritası

| Klasör | Girer | Girmez |
|---|---|---|
| `context/` | Projenin güncel bağlamı ve çalışma kuralları | Faz raporu, prompt |
| `decisions/` | `DECISION-INDEX.md`, `addenda/PHP-LARAVEL-SETUP-EK-FAZ-NN.md` | Kararın tartışması (faz raporuna) |
| `phases/faz-NN/` | O fazın planı, raporu, devir notu, commit komutları, ara çıktıları | Kod kılavuzu (`docs/rehber/` kod deposunda) |
| `prompts/` | Ajanlara verilen `PROMPT-*.md` | Ajanın ürettiği rapor (`phases/` ya da `audits/`) |
| `audits/YYYY-MM-DD-<konu>/` | Denetim ve gözden geçirme raporları | Düzeltme kodu |
| `operations/` | Yayın, AWS, sunucu, DNS (`deployment/` altında) | Sırlar |
| `product/` | Fiyat, plan, tasarım/video onayları | Kod |
| `notes/` | Serbest notlar, araştırmalar, dış kaynak özetleri | Karar (karar `decisions/`'a) |
| `archive/` | Geçersiz kılınmış ya da mükerrer dosyalar (bantlı) | Güncel bir dosyanın kopyası |
| `_restructure/` | 2026-11-12 düzenlemesinin kayıtları ve betikleri | Yeni iş |

**Yeni dosya nereye?**

| Dosya | Yer |
|---|---|
| Ajan prompt'u | `prompts/PROMPT-<konu>.md` |
| Faz planı / raporu / devir notu / commit komutları | `phases/faz-NN/` |
| Tarihli inceleme, denetim | `audits/YYYY-MM-DD-<konu>/` |
| Yeni karar | Fazın `decisions/addenda/` dosyası **ve** `decisions/DECISION-INDEX.md` |
| Yayın / sunucu notu | `operations/deployment/` |
| Eskiyen dosya | `archive/` + en üste bant + `archive/README.md` satırı |
| Hiçbirine uymuyor | `_triage/` + İsmail'e sor |

Arşiv bandı (tek satır, dosyanın en üstü):
`> 🗄️ ARŞİV (YYYY-MM-DD) — Yerine geçen: <yol>. Neden: <tek cümle>.`

## 4. Adlandırma

- Klasörler İngilizce, küçük harf, `kebab-case`. Faz klasörleri `faz-NN` (`faz-07`, `faz-15`).
- Tarihli dosya ve klasörler `YYYY-MM-DD-<konu>`.
- Mevcut dosya adları **korunur**. `context/PHP-LARAVEL-SETUP.md` adı **asla değişmez**.
- Dallar: bu depoda `docs/<YYYY-MM-DD>-<konu>`, `audit/<YYYY-MM-DD>-<konu>`; kod depolarındaki
  düzeltme dalları `fix/<YYYY-MM-DD>-<bulgu-id>-<kısa-ad>`.
- Bulgu kimlikleri `ARC-NN`, `SEC-NN`, `TST-NN`, `FE-NN`, `OPS-NN`; denetim kimliği `AUD-YYYY-MM-DD`.

## 5. Karar kaydı

- Yeni karar = `DECISION-INDEX.md`'deki **sıradaki boş K numarası**.
- Numara asla yeniden kullanılmaz, değiştirilmez. Çakışma görürsen ⚠️ ile işaretle, numarayı İsmail'e bırak.
- Geçersiz kılınan karar silinmez; durumuna `geçersiz kılındı → K…` yazılır.
- Karar hem fazın `addenda/` dosyasına hem `DECISION-INDEX.md`'ye işlenir.
- Çelişkide daha yeni olan kazanır: ek dosyaları > `PHP-LARAVEL-SETUP.md`
  ([`context/PHP-LARAVEL-SETUP.md`](context/PHP-LARAVEL-SETUP.md), başlık notu).

## 6. Yazım

- Dokümanlar Türkçe, kısa ve doğrudan (`PHP-LARAVEL-SETUP.md` §2, kural 6).
- Commit mesajları İngilizce. Bu depoda: `docs(<alan>): <Fiil> ...`
  (ör. `docs(decisions): Add K128 for ...`).
- Bir bilginin tek bir güncel evi olur; diğer yerler ona bağlantı verir, kopyalamaz.
- Klasöre dosya ekleyen ya da çıkaran, o klasörün `README.md`'sini aynı değişiklikte günceller.
- Bu deponun her değişikliği [`CHANGELOG.md`](CHANGELOG.md)'ye bir satır olarak işlenir.

## 7. Çalışma biçimi (mevcut dokümanlardan)

- **Git yazma işlemlerini İsmail yapar.** `add`, `commit`, `push`, `stash`, `reset` çalıştırma;
  commit komutlarını ver ([`prompts/PROMPT-FAZ-11.md`](prompts/PROMPT-FAZ-11.md) §0 madde 2;
  `PHP-LARAVEL-SETUP.md` §2 kural 4: *"Komutları o çalıştırıyor."*).
- Commit komutu: her adım ayrı PowerShell bloğu, dosyalar **tek tek, açık yolla**; joker ve `-A`
  yok; blok `git status --short` ile biter ([`prompts/PROMPT-FAZ-12.md`](prompts/PROMPT-FAZ-12.md) §10 madde 3).
- **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma; koşmadıysa "koşmadı" yaz
  ([`prompts/PROMPT-FAZ-11.md`](prompts/PROMPT-FAZ-11.md) §0 madde 5).
- **K18:** kod yorumu kısa (1–3 satır); ayrıntı kod deposunda `docs/rehber/<aynı-yol>.md`
  (`PHP-LARAVEL-SETUP.md` §2 "Açıklama nereye yazılır?").
- **Frontend deposunda CRLF tuzağı:** `git add -A` alakasız yüzlerce dosyayı sürükler; dosyalar tek tek
  eklenir ([`notes/03-FRONTEND-YAPILACAKLAR.md`](notes/03-FRONTEND-YAPILACAKLAR.md);
  [`phases/faz-14/FAZ-14-FRONTEND-COMMIT-KOMUTLARI.md`](phases/faz-14/FAZ-14-FRONTEND-COMMIT-KOMUTLARI.md)).
- **Sırlar bu depoya asla yazılmaz:** `.env`, API anahtarları, parolalar, hesap numaraları.
  Para değerindeki sır düz yazılmaz (H14, [`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md) §B).
  Kod arşivleri (`.tgz`, `.tar`, `.bundle`) `.gitignore`'dadır; içlerinde `.env` olabilir.
- Plandan kendi kararınla sapma; yanlış bulduğun kararı önce söyle ve tartış
  (`PHP-LARAVEL-SETUP.md` §2 kural 5).

## 8. Yapma

- Dosya silme: arşivle (`archive/` + bant).
- Geçmiş raporları, prompt'ları ya da kararları yeniden yazma, özetleme, "düzeltme". Taşıma yüzünden
  kırılan bağlantıyı düzeltmek serbest.
- Yeni plan, rapor ya da prompt dosyasını kök dizine bırakma.
- Bu depodan çalışırken kod depolarında değişiklik yapma; onlar salt okunurdur.
- K numarasını yeniden kullanma ya da değiştirme.
````
