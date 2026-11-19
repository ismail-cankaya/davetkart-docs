# Faz 18 — denetim düzeltmeleri (`AUD-2026-11-12`)

Altı yüksek (🟠) bulgu, yayından önce. Her bulgu ayrı bir düzeltme dalında, ayrı bir prompt'la ve tek oturumda kapanır; commit'leri İsmail atar.

- **Kaynak:** [`audits/2026-11-12-full-system-audit/REPORT.md`](../../audits/2026-11-12-full-system-audit/REPORT.md) §1 ve §4
- **Entegrasyon dalı (backend ve frontend):** `faz-18-audit-fixes` (`origin/ccr-9a346997-bu6gve` üstüne; frontend'e `main`'deki `47aedc8` birleştirilir). Düzeltme dalları bundan açılır ve buna birleşir; faz sonunda `main` + `v1.1.0` (18.6 §11).
- **Düzeltme dalları:** `fix/<YYYY-MM-DD>-<bulgu-id>-<kısa-ad>` (`CLAUDE.md` §4)
- **Docs dalı:** `docs/2026-11-16-faz-18-audit-fixes`
- **Resmî faz kaydı:** backend `docs/rehber/fazlar/FAZ-18.md`
- **Sıra:** aşağıdaki tablo; her prompt bir öncekinin birleşmiş olmasını önkoşul olarak denetler.

| Sıra | Bulgu | Konu | Efor | Prompt | Depolar | Dal | K | Durum |
|---|---|---|---|---|---|---|---|---|
| 18.1 | `OPS-01` | Yayına çıkacak commit ve dağıtım sırası; plan kuralları sözleşmesi (+ `TST-01`) | S | [`PROMPT-FAZ-18-1-OPS-01.md`](../../prompts/PROMPT-FAZ-18-1-OPS-01.md) | backend · frontend · docs | `fix/2026-11-16-ops-01-release-alignment` (backend · frontend) | K146–K150 | kod ✅ · commit bekliyor (backend 18.1.1–18.1.4 birleşti `162c985`; kalan: frontend 18.1.5 + birleştirme, backend 18.1.7 + birleştirme, docs) |
| 18.2 | `OPS-02` | Veritabanı yedeği ve geri yükleme provası | M | [`PROMPT-FAZ-18-2-OPS-02.md`](../../prompts/PROMPT-FAZ-18-2-OPS-02.md) | backend · docs | `fix/2026-11-16-ops-02-db-backup` (backend) | K151–K157 | kod ✅ · commit bekliyor (yerel kuru koşu, prova ve mutantlar ✅ · `composer check` ✅ 1074 test · AWS/sunucu kurulumu ve ilk üretim provası İsmail'in elle işi: [`YEDEK-VE-GERI-YUKLEME.md`](../../operations/deployment/YEDEK-VE-GERI-YUKLEME.md)) |
| 18.3 | `SEC-01` | İlk yayın indirimi tek açık siparişe | M | [`PROMPT-FAZ-18-3-SEC-01.md`](../../prompts/PROMPT-FAZ-18-3-SEC-01.md) | backend · frontend · docs | `fix/2026-11-16-sec-01-first-publish-once` (backend · frontend) | K158–K163 | kod ✅ · commit bekliyor (backend 18.3.1–18.3.5, frontend 18.3.6, docs 18.3.7 · doğrulama sonuçları: backend `FAZ-18.md` §18.3 · ⚠️ plandan sapma: fiyat uçları isteğe bağlı hedef alıyor ve frontend ödeme sayfası değişti, K163 · göç yerelde henüz koşmadı: `php artisan migrate`) |
| 18.4 | `SEC-02` | Yayınlanmış hakkın iadesi | M | [`PROMPT-FAZ-18-4-SEC-02.md`](../../prompts/PROMPT-FAZ-18-4-SEC-02.md) | backend · frontend · docs | `fix/2026-11-17-sec-02-refund-after-publish` (backend · frontend) | K164–K169 | kod ✅ · commit bekliyor (backend 18.4.1–18.4.6, frontend 18.4.7, docs 18.4.8 · doğrulama sonuçları: backend `FAZ-18.md` §18.4 · ⚠️ plandan sapma: silme akışı da damga basıyor (K165), frontend SSS cevabı değişti · göç yerelde henüz koşmadı: `php artisan migrate`) |
| 18.5 | `SEC-03` | Shopier `callback` kipi üretimde reddedilir | S | [`PROMPT-FAZ-18-5-SEC-03.md`](../../prompts/PROMPT-FAZ-18-5-SEC-03.md) | backend · docs | — | — | bekliyor |
| 18.6 | `SEC-04` | Frontend güvenlik başlıkları + Faz 18 kapanışı | S | [`PROMPT-FAZ-18-6-SEC-04.md`](../../prompts/PROMPT-FAZ-18-6-SEC-04.md) | backend · (frontend) · docs | — | — | bekliyor |

Durum değerleri: `bekliyor` → `kod ✅ · commit bekliyor` → `birleşti` (İsmail işaretler).

**Etiketten önce kapanmalı (🟡, Faz 18 dışında):** `SEC-07` (`composer audit` kırmızı).

## Bu klasördeki dosyalar

| Dosya | Ne |
|---|---|
| [`FAZ-18-OPS-01-COMMIT-KOMUTLARI.md`](FAZ-18-OPS-01-COMMIT-KOMUTLARI.md) | 18.1 (`OPS-01`) commit ve birleştirme komutları: üstte kalan bloklar (frontend 18.1.5, backend 18.1.7, docs), altta çalıştırılmışların kaydı |

| [`FAZ-18-OPS-02-COMMIT-KOMUTLARI.md`](FAZ-18-OPS-02-COMMIT-KOMUTLARI.md) | 18.2 (`OPS-02`) commit ve birleştirme komutları: backend 18.2.1–18.2.4, docs 18.2.5 |

| [`FAZ-18-SEC-01-COMMIT-KOMUTLARI.md`](FAZ-18-SEC-01-COMMIT-KOMUTLARI.md) | 18.3 (`SEC-01`) commit ve birleştirme komutları: backend 18.3.1–18.3.5, frontend 18.3.6, docs 18.3.7 |

| [`FAZ-18-SEC-02-COMMIT-KOMUTLARI.md`](FAZ-18-SEC-02-COMMIT-KOMUTLARI.md) | 18.4 (`SEC-02`) commit ve birleştirme komutları: backend 18.4.1–18.4.6, frontend 18.4.7, docs 18.4.8 |

Kararlar: [`../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md) ·
çalıştırma kitapları: [`../../operations/deployment/YAYIN-SIRASI.md`](../../operations/deployment/YAYIN-SIRASI.md) (18.1) ·
[`../../operations/deployment/YEDEK-VE-GERI-YUKLEME.md`](../../operations/deployment/YEDEK-VE-GERI-YUKLEME.md) (18.2).
