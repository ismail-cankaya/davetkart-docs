# Faz 26 — v2.0 kalan metinler

Faz 24 ortak bölümleri, kategori ve şablon başlıklarını taşıdı; hero bileşenlerinde ve şablona özel parçalarda koda
gömülü metinler kaldı (`verify:text-slots` tavanı: **511**, 138 dosya). Bu faz onları anahtara taşır; tavan yalnızca iner.

| | |
|---|---|
| Durum | ⏳ Sürüyor (28 Kasım 2026) |
| Kod dalı | frontend `faz-26-v2.0-texts` (`faz-25-v2.0-editor-ui`'dan) · backend değişikliği yok (yeni anahtarlar sözleşmeyle kopyalanır) |
| Kararlar | K301, K302, K304 (aynı kurallar) |

## Takip

| Sıra | Konu | Depo | Tavan | Commit | Durum |
|---|---|---|---|---|---|
| 26.0 | Başlangıç tavanı | fe | 511 | `346351f` | commit'lendi |

## Kural

- Görünen metin → `<InvText k>` (editörde tıklanabilir) ya da öznitelik/dize için `useInvText()`.
- Erişilebilirlik etiketleri ve kullanıcı içeriği yer tutucuları ("Davetlisiniz") → `fixed` (düzenlenemez).
- Her adımdan sonra `npm run text-slots:baseline` (tavan iner), `npm run text-slots:export` (yeni anahtarlar),
  backend `contracts/text-slots.json`'a aynen kopya, 762 çizimlik anlık görüntü karşılaştırması.
