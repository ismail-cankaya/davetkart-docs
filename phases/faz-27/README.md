# Faz 27 — v2.1 altyapı: cihaz tuvali, kullanıcı içeriğinde tıkla-düzenle, taslak katmanı

Faz 27–29'un (v2.1, Önizleme ve Tasarım Stüdyosu) ilk fazı. Plan: [`FAZ-27-PLAN.md`](FAZ-27-PLAN.md) (üç fazın ortak
planı). Stüdyo arayüzü Faz 28, önizleme ve paylaşım Faz 29.

| | |
|---|---|
| Durum | ✅ Kod tamam (28 Kasım 2026) · birleştirme bekliyor |
| Sürüm | v2.1 (Faz 24–26 = v2.0) |
| Kod dalı | frontend ve backend `faz-27-v2.1-studio` (`faz-26-v2.0-texts` ucundan, 26.3 bittikten sonra); devamı [`faz-28`](../faz-28/README.md), [`faz-29`](../faz-29/README.md) |
| Docs dalı | `claude/cool-hamilton-q2dnft` (`claude/brave-edison-dbg3l1` ucuna ileri sarıldı) |
| Kararlar | [`EK-FAZ-27`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-27.md): K318–K329 |

## Dosyalar

| Dosya | İçerik |
|---|---|
| [`FAZ-27-PLAN.md`](FAZ-27-PLAN.md) | Faz 27–29 planı: istek, oturum kararları, ölçüm, tasarım, adımlar, riskler |

## Takip

**Bu tablo ilerlemenin tek kaydıdır** (Faz 28 ve 29 kendi klasörlerinde açılır).

| Sıra | Konu | Depo | K | Commit | Durum |
|---|---|---|---|---|---|
| 27.0 | Plan ve kararlar | docs | K318–K329 | `96739bc` | commit'lendi |
| 26.3 | Kalan 243 gömülü metin (Faz 26 dalında; kayıt [`faz-26`](../faz-26/README.md)) | fe · be | — | fe `b53ff20` · be `e948a3f` | commit'lendi |
| 27.1 | `iframe` cihaz tuvali (390 / 820 / 1280 px, ölçekli) | fe | K320 | `6b55d2f` | commit'lendi |
| 27.2 | Tıkla-düzenle: kullanıcı içeriği (isim, başlık, alt başlık, mekân) ve tüm şablon metinleri; `InvField` yerine DOM eşlemesi (EK-FAZ-27 §A sonu) | fe | K321 | `ab6de36` | commit'lendi |
| 27.3 | Taslak katmanı: `pending_changes`, kaydet / yayınla / at uçları | be | K323, K324 | `8ee40c0` | commit'lendi |
| 27.4 | Taslak servisi ve store: yayındaki davetiyede otomatik kayıt taslağa, "Değişiklikleri yayınla" / "Değişiklikleri at" | fe | K323 | `d0aab0e` | commit'lendi |

Durum değerleri: `bekliyor` · `commit'lendi` · `birleşti` (İsmail, `main`'e aldıktan sonra).

## Kapılar

| Adım | Sonuç |
|---|---|
| 27.1–27.4 frontend | `npm run check` çıkış 0 (lint, build, 15 `verify:*`, misafir paketi K237 bütçesinde) |
| 27.3 backend | `composer check` 1409/1409 |
| Elle (yerel backend + Vite) | Yayındaki davetiyede stüdyo kaydı misafiri değiştirmedi; "Değişiklikleri yayınla" uyguladı |

Koşmadı: tam e2e takımı (backend + PowerShell ister), sunucu adımları.
