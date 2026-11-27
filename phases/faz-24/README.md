# Faz 24 — v2.0: Davetiye Metin Editörü

Kullanıcı "Düzenle" ile editörü açar; önizlemede metne (sabit şablon metinleri dahil) ya da bölüme tıklayıp değiştirir,
➕ ile yeni özellik ekler. Metinler koddan çıkarken çok dilli altyapı kurulur (v2.0'da yalnızca Türkçe). Sabit metin
özelleştirmesi Elit pakette.

| | |
|---|---|
| Durum | 📝 Plan · kod yok · karar numaraları bekliyor |
| Sürüm | v2.0 (Faz 22 → `v1.3`, Faz 23 → `v1.4`) |
| Kod dalı | frontend/backend `faz-24-v2.0-editor` (öneri) — **Faz 23 bittikten sonra** açılır |
| Docs dalı | `claude/brave-edison-dbg3l1` |
| Kararlar | [`EK-FAZ-24`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-24.md): taslak T1–T15, ⚠️ numara bekliyor (öneri K300–K329) |

## Dosyalar

| Dosya | İçerik |
|---|---|
| [`FAZ-24-PLAN.md`](FAZ-24-PLAN.md) | İstek ve oturum kararları, mevcut durum (kod ölçümü), kapsam (v2.0 / v2.1+), tasarım (anahtarlar, çok dillilik, veri modeli, editör, ➕, şablon değişimi, asistan, kötüye kullanım), adımlar 24.0–24.13, riskler, test planı, açık sorular S1–S6 |

## Takip

**Bu tablo ilerlemenin tek kaydıdır.**

| Sıra | Konu | Depolar | Commit'ler | Durum |
|---|---|---|---|---|
| 24.P | Plan ve karar taslakları | docs | — | yazıldı |
| 24.0–24.13 | Bkz. plan §5 | fe · be · docs | — | bekliyor (Faz 23 bitince) |

Durum değerleri: `bekliyor` · `commit'lendi` · `birleşti` (İsmail, `main`'e aldıktan sonra).
