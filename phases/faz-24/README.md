# Faz 24 — v2.0 altyapı: şablon metinleri koddan çıktı

Şablonların sabit metinleri anahtarla okunur (`src/invitationText/`), varsayılanlar `tr.json`'da, düzenlenebilir
anahtarlar sözleşmede (`text-slots.json`). Backend davetiyenin dilini ve kullanıcının değiştirdiği metinleri saklar,
özel metin Elit ister. Editör arayüzü [Faz 25](../faz-25/README.md), kalan gömülü metinler [Faz 26](../faz-26/README.md).

| | |
|---|---|
| Durum | ✅ Kod tamam (28 Kasım 2026) · birleştirme İsmail'in |
| Sürüm | v2.0 (Faz 22 → `v1.3`, Faz 23 → `v1.4`) |
| Kod dalı | frontend `faz-24-v2.0-editor` (`faz-23-v1.4-frontend` @ `105169f`'ten), backend `faz-24-v2.0-editor` (`faz-22-release-prep` @ `5d250b9`'dan) |
| Docs dalı | `claude/brave-edison-dbg3l1` |
| Kararlar | [`EK-FAZ-24`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-24.md): K300–K305, K314, K316, K317 (aralık K300–K329) |
| Backend kaydı | `davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-24.md` |

## Dosyalar

| Dosya | İçerik |
|---|---|
| [`FAZ-24-PLAN.md`](FAZ-24-PLAN.md) | Faz 24–26'nın ortak planı: istek ve oturum kararları, kod ölçümü, kapsam, tasarım, adımlar, riskler, test planı; §10 uygulama kaydı |

## Takip

**Bu tablo ilerlemenin tek kaydıdır.**

| Sıra | Konu | Depo | K | Commit | Durum |
|---|---|---|---|---|---|
| 24.P | Plan ve karar taslakları | docs | — | `51b3423` | commit'lendi |
| 24.0 | Faz 22 ucunun kırmızıları: `ErrorCodeUsageTest` 28 → 27, `error-codes.json` yeniden dışa aktarım, `k18:check` 10 ihlal (dört dosyada uzun yorum → kılavuz) | be | — | `8806d68` · `41f0d0d` · `1803729` | commit'lendi |
| 24.1 | Bütün şablonların belirlenimci HTML anlık görüntüsü (762 çizim, sabit saat/tohum) | fe | — | `55fa26c` | commit'lendi |
| 24.2 | Metinler koddan çıktı: ortak bölümler, 9 kategori flavor'ı, 63 şablon kapsamı (+ sergi, kitap); `InvText`, sağlayıcılar | fe | K300, K302 | `3f7d91a` | commit'lendi |
| 24.3 | `text-slots.json` (46 anahtar), `text-slots:export`/`baseline`, `verify:text-slots` | fe | K301, K304 | `346351f` | commit'lendi |
| 24.4 | `locale`, `text_overrides`, `has_custom_texts`, doğrulama, kaynaklar, `module_tiers` Elit; 26 + 6 test | be | K302–K305 | `7bca677` | commit'lendi |
| 24.5 | Plan sözleşmesi (`DERIVED_MODULES`), `getRequiredTier`, fiyat kartı satırı "Metinleri özelleştirme", başlangıç davetiyesi `tr` | fe | K305 | `c1245ab` | commit'lendi |

Durum değerleri: `bekliyor` · `commit'lendi` · `birleşti` (İsmail, `main`'e aldıktan sonra).

## Kapılar (bu oturum, bulut çalışma alanı)

- Backend `composer check` (pint, phpstan, `errors:export --check`, `plans:export --check`, `env:template --check`,
  `k18:check`, testler): **1385/1385** (24.4 sonunda). PHP 8.5.13 kaynaktan derlendi, PostgreSQL 16 (üretim 18; testler
  16'da koştu).
- Frontend `npm run check` (lint + build + 16 `verify:*`): **çıkış 0**.
- Anlık görüntü: taşımadan önce ve sonra 762 çizim, `<!-- -->` ayraçları dışında **birebir aynı**.
- e2e: bu fazda koşmadı (Faz 25'te editör senaryosu koştu).
