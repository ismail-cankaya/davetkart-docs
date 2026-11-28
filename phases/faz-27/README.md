# Faz 27 — v2.1 altyapı: cihaz tuvali, kullanıcı içeriğinde tıkla-düzenle, taslak katmanı

Faz 27–29'un (v2.1, Önizleme ve Tasarım Stüdyosu) ilk fazı. Plan: [`FAZ-27-PLAN.md`](FAZ-27-PLAN.md) (üç fazın ortak
planı). Stüdyo arayüzü Faz 28, önizleme ve paylaşım Faz 29.

| | |
|---|---|
| Durum | ⏳ Sürüyor (28 Kasım 2026) |
| Sürüm | v2.1 (Faz 24–26 = v2.0) |
| Kod dalı | frontend ve backend `faz-27-v2.1-studio` (`faz-26-v2.0-texts` ucundan, 26.3 bittikten sonra) |
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
| 27.0 | Plan ve kararlar | docs | K318–K329 | — | bekliyor |
| 26.3 | Kalan 243 gömülü metin (Faz 26 dalında; kayıt [`faz-26`](../faz-26/README.md)) | fe · be | — | — | bekliyor |
| 27.1 | `iframe` cihaz tuvali | fe | K320 | — | bekliyor |
| 27.2 | `InvField`: kullanıcı içeriğinde tıkla-düzenle | fe | K321 | — | bekliyor |
| 27.3 | Taslak katmanı (backend) | be | K323, K324 | — | bekliyor |
| 27.4 | Taslak servisi ve store (frontend) | fe | K323 | — | bekliyor |

Durum değerleri: `bekliyor` · `commit'lendi` · `birleşti` (İsmail, `main`'e aldıktan sonra).
