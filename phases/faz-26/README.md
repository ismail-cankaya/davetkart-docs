# Faz 26 — v2.0 kalan metinler

Faz 24 ortak bölümleri, kategori ve şablon başlıklarını taşıdı; hero bileşenlerinde ve şablona özel parçalarda koda
gömülü metinler kaldı. Bu faz onları anahtara taşır; `verify:text-slots` tavanı yalnızca iner.

| | |
|---|---|
| Durum | ⏳ Sürüyor · tavan **511 → 243** (28 Kasım 2026) · kalan iş aşağıda |
| Kod dalı | frontend ve backend `faz-26-v2.0-texts` (`faz-25-v2.0-editor-ui`'dan) |
| Kararlar | K301, K302, K304 (aynı kurallar); `staticFixedText` v2.0 tek dil, v2.1'de `useFixedText` (K317) |

## Takip

| Sıra | Konu | Depo | Tavan | Commit | Durum |
|---|---|---|---|---|---|
| 26.0 | Başlangıç tavanı (Faz 24.3) | fe | 511 | `346351f` | commit'lendi |
| 26.1 | 27 ortak hero: geri sayım birimleri, tarih/mekân/saat/kalan etiketleri ortak anahtarlarla (`countdown.*`, `label.*`), hero'ya özgü sözler `hero.<ad>.*`, isim yer tutucusu `fixed`; sözleşme 77 anahtar; panelde "Etiketler" grubu ve yalnızca bu tasarımın metinleri | fe · be | 402 | fe `d5584a5` · be `51d6826`, `0013fc4` (sözleşme şekil testi: anahtarda rakam) | commit'lendi |
| 26.2 | Şablona özel parçalar: `design.<şablon>.*` (90 düzenlenebilir), 27 erişilebilirlik etiketi `fixed`; sözleşme 167 anahtar; panelde "Tasarıma özel" grubu; `verify:text-slots` rakam/tire içeren anahtarları da denetler | fe · be | **243** | fe `fc8cc5c` · be `70c627a` | commit'lendi |

Her adımda: `npm run check` çıkış 0, 762 çizimlik anlık görüntü taşımadan önceyle **birebir aynı**, e2e `text-editor` 3/3,
backend `composer check` 1398/1398. Paket bütçesi değişmedi (714,2 / 799,2 kB).

⚠️ `0013fc4`: `51d6826` (sözleşme kopyası) test koşusu bitmeden itildi ve şekil testi rakamlı anahtarda kırmızıydı;
bir sonraki commit düzeltti. Dal ucunda kapı yeşil.

## Kalan iş (243 metin, 69 dosya)

Dönüştürücünün bilerek bıraktığı metinler: değeri **dize olarak** kullanılan prop'lar ve diziler (bileşen `label: string`
bekliyor, metin `.length`/`.split()` ile işleniyor ya da React `key` oluyor). Her biri bileşende `const t = useInvText()`
ile `t('…')`'ye çevrilmeli (elle; hook'un yeri bileşene göre değişir). Ayrıca `TakvimHero`'nun ay ve gün adları anahtar
değil **`Intl.DateTimeFormat(locale)`** ile üretilmeli (dile göre doğru biçim).

En çok kalan dosyalar (`scripts/text-slots/baseline.json`):

| Dosya | Metin |
|---|---|
| `konsept/harita/veri.ts` | 21 |
| `shared/heroes/TakvimHero.tsx` | 20 |
| `konsept/sergi/soyutEserler.tsx` | 14 |
| `dogum-gunu/DogumGunuSurprizMakinesi/index.tsx` | 13 |
| `dugun/DugunKitapSayfa/index.tsx` | 10 |
| `mezuniyet/MezuniyetYillik/index.tsx` | 9 |
| `baby-shower/BabyKaziKazan/index.tsx` | 8 |
| `mezuniyet/MezuniyetKaraTahta/index.tsx` | 8 |
| `kurumsal/KurumsalIzometrik/index.tsx` | 7 |
| `dogum-gunu/kitap/ortak.tsx` | 6 |
| `mezuniyet/MezuniyetKaraTahta/tebesirMotoru.ts` | 5 |
| `shared/heroes/UfukHero.tsx` | 5 |

Yöntem (adım başına): dosyada `useInvText()`/`staticFixedText` ile taşı → `npm run text-slots:baseline` →
`npm run text-slots:export` → backend `contracts/text-slots.json`'a aynen kopya → anlık görüntü karşılaştırması
(`scripts/text-slots/snapshot.tsx`, `docs/rehber/scripts/text-slots.md`) → `npm run check`, `composer check`.
