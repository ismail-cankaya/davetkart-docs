# Faz 26 — v2.0 kalan metinler

Faz 24 ortak bölümleri, kategori ve şablon başlıklarını taşıdı; hero bileşenlerinde ve şablona özel parçalarda koda
gömülü metinler kaldı. Bu faz onları anahtara taşır; `verify:text-slots` tavanı yalnızca iner.

| | |
|---|---|
| Durum | ✅ Kod tamam (28 Kasım 2026) · tavan **511 → 0** · birleştirme İsmail'in |
| Kod dalı | frontend ve backend `faz-26-v2.0-texts` (`faz-25-v2.0-editor-ui`'dan) |
| Kararlar | K301, K302, K304 (aynı kurallar); `staticFixedText` v2.0 tek dil, v2.1'de `useFixedText` (K317) |

## Takip

| Sıra | Konu | Depo | Tavan | Commit | Durum |
|---|---|---|---|---|---|
| 26.0 | Başlangıç tavanı (Faz 24.3) | fe | 511 | `346351f` | commit'lendi |
| 26.1 | 27 ortak hero: geri sayım birimleri, tarih/mekân/saat/kalan etiketleri ortak anahtarlarla (`countdown.*`, `label.*`), hero'ya özgü sözler `hero.<ad>.*`, isim yer tutucusu `fixed`; sözleşme 77 anahtar; panelde "Etiketler" grubu ve yalnızca bu tasarımın metinleri | fe · be | 402 | fe `d5584a5` · be `51d6826`, `0013fc4` (sözleşme şekil testi: anahtarda rakam) | commit'lendi |
| 26.2 | Şablona özel parçalar: `design.<şablon>.*` (90 düzenlenebilir), 27 erişilebilirlik etiketi `fixed`; sözleşme 167 anahtar; panelde "Tasarıma özel" grubu; `verify:text-slots` rakam/tire içeren anahtarları da denetler | fe · be | **243** | fe `fc8cc5c` · be `70c627a` | commit'lendi |
| 26.3 | Kalan 243 metin (dize prop'ları, diziler, modül sabitleri) `useInvText`/`useFixedText` ile; `TakvimHero` ay/gün adları `Intl`; tarayıcı genişledi (şapkalı harf, `?`/`:` cümle, diğer JSX prop'ları, şablon dizeleri, parametre varsayılanı) ve bulduğu 63 metin de taşındı; kod dizeleri `// text-slots: kod`; `KurumsalIzometrik`/`BrutalHero` görünen metne bakarak karar vermiyor; LCV menü seçenekleri düzenlenebilir; sözleşme **307** anahtar | fe | **0** | fe `b53ff20` | commit'lendi |
| 26.4 | Sözleşme kopyası (307 anahtar); sınır testinde yer tutucular dolduruluyor | be | — | be `e948a3f` | commit'lendi |

Her adımda: `npm run check` çıkış 0, 762 çizimlik anlık görüntü taşımadan önceyle **birebir aynı**, e2e `text-editor` 3/3,
backend `composer check` 1398/1398. Paket bütçesi: 714,2 / 799,2 kB (26.3'te misafir 799,3 kB; bütçe 800).

26.3 ortamı (bu oturum): Node 24.22.3, PHP 8.5.13 kaynaktan, PostgreSQL 16. e2e `text-editor` geliştirme sunucusuna
karşı geçici yapılandırmayla koştu (backend gerekmez); tüm e2e paketi **koşmadı**.

⚠️ `0013fc4`: `51d6826` (sözleşme kopyası) test koşusu bitmeden itildi ve şekil testi rakamlı anahtarda kırmızıydı;
bir sonraki commit düzeltti. Dal ucunda kapı yeşil.

## Kalan iş

Yok: tavan 0. 26.2 sonundaki 243 metnin listesi ve yöntem commit `c25746e`'deki bu dosyada; yöntemin güncel hâli
frontend `docs/rehber/scripts/text-slots.md` ("Tarayıcının kuralları", "Metni taşıma yolları").

Bilinen sınır: `staticFixedText` v2.0'da tek dil (`tr`); erişilebilirlik etiketlerinin bir kısmı onu kullanıyor (K317 → v2.2+).
