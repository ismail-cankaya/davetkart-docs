# Faz 24 — v2.0: Davetiye Metin Editörü (Plan)

> **Durum:** 📝 Plan · kod yok · karar numaraları bekliyor (§9 S1).
> **Tarih:** 27 Kasım 2026 · **Sürüm:** v2.0 · **Sıra:** Faz 22 → `v1.3` → Faz 23 (`v1.4`) → **Faz 24 (`v2.0`)**.
> **Bağımlılık:** Faz 23'e **bağlı değil** (İsmail, 27 Kasım). Ama kod dalları **Faz 23 bittikten sonra** açılır (İsmail, 27 Kasım).
> **Docs dalı:** `claude/brave-edison-dbg3l1` (`docs/2026-11-27-faz-22-release-prep` ucundan; `main` Faz 18'de kaldığı için).
> **Analiz tabanı:** frontend `faz-21-backlog` @ `e28b599` · backend `main` @ `03d3940`. Faz 22/23 kodu görülmedi; dal açılınca §2 yeniden ölçülür.
> **Kararlar:** [`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-24.md`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-24.md) (taslak T1–T15).

## 0. Özet

Kullanıcı davetiyesini oluşturduktan sonra **"Düzenle"** ile bir editör açar. Önizlemede bir metne tıklar ve değiştirir;
buna şablonun **sabit metinleri** de dahildir ("Evleniyoruz", "Özel Anlarımız", "Katılımımı Bildir"…). Bir bölüme
tıklayınca o bölümün ayarları açılır; **➕** ile henüz eklenmemiş bir özellik (IBAN, program, galeri…) eklenir.

İlke: **tasarım kilitli, metin serbest.** Font, renk ve yerleşim değiştirilmez (İsmail: "font değiştirme gibi kapsamlı
işleri düşünmüyorum").

Metinler koddan çıkarılırken **çok dilli altyapı** da kurulur, ama v2.0'da **yalnızca Türkçe** vardır; diğer diller
v2.1'de eklenir (İsmail, 27 Kasım).

Sabit metin özelleştirmesi **Elit** pakette (İsmail, 27 Kasım). Kullanıcının kendi içeriği (isimler, mekân, tarih…)
bugünkü gibi her pakette düzenlenir.

## 1. İstek (İsmail, 27 Kasım 2026)

> Planım kullanıcı davetiye oluşturduktan sonra davetiyesindeki değişmeyen metinler de dahil olmak üzere istediği gibi
> özelleştirmesini istiyorum. Wordpress gibi mantığı olacak. Davetiyeyi düzenleye basıldığında editör açılacak. Kullanıcı
> oradan bir metne veya özelliğe tıklayıp istediği gibi değiştirebilecek. Şimdilik font değiştirme gibi kapsamlı işleri
> düşünmüyorum pek mantıklı gelmedi. Metin vs. gibi kısımlar mantıklı geldi.

Oturumdaki kararlar (aynı gün):

| Konu | İsmail'in cevabı |
|---|---|
| Çok dillilik | Metinler koddan çıkarken **önce çok dillilik altyapısı** gelsin; şimdilik yalnızca Türkçe; diğer diller sonra (v2.1) |
| Riskler ve önlemler (§6) | "Gayet iyi" — hepsi kapsamda |
| Tıkla-düzenle + Metinler paneli | ✅ |
| Bölüme tıklayınca ayarlar | ✅ + **editörde ➕ ile yeni özellik ekleme** ("+ işaretine basınca IBAN kısmı eklensin") |
| Varsayılana dön | ✅ ama **onay sorsun**, doğrudan sıfırlamasın |
| Ton setleri (Resmi/Samimi/Esprili) | Sonraki adım (v2.1+) |
| Asistanla metin önerisi | ✅ v2.0 |
| LCV metinleri, geri al/yinele, bölüm sırası | Önerildiği gibi: LCV metinleri v2.0 (özel soru v2.1); geri al/yinele oturum içi v2.0; bölüm sırası v2.1 |
| Paket | Metin değiştirme ve özelleştirme **en üst pakette** (Elit) |

## 2. Mevcut durum (kod ölçümü)

### 2.1 Sabit metinler nerede

| Yer | Örnek | Ölçek |
|---|---|---|
| Kategori `flavors.tsx` (`TemplateFlavor`) | `envelopeLabel: 'Düğün Davetiyesi'`, `tagline: 'Evleniyoruz'`, `headings.*`, `eyebrows.*`, `giftNote` | Kategori başına bir nesne (11 kategori) |
| Ortak bölümlerdeki yedek metinler | `Gallery.tsx:80` `'Özel Anlarımız'`, `GiftRegistry.tsx:49` `'Hediye Takdiri'`, `RSVPForm.tsx:86` `'LCV — Katılım Bildirimi'`, `:246` `Katılım Durumu`, `:289` `Katılımımı Bildir` | `templates/shared/*.tsx` |
| Hero ve şablona özel parçalar | `BentoHero` "Davetliler/Tarih/Mekân/Kalan Süre", `TakvimHero` "gün kaldı", `GazeteHero` "Yıl 1 · Sayı 1", `UfukHero` "Mekân", `Details.tsx` "Tarih & Saat" | Kaba sayım: `templates/` altında ~118 JSX metin satırı |

- Şablon sayısı: katalogda 366 preset (`src/templateCatalog.ts`), `templates/` altında ~387 klasör.
- `InvitationComposition` kullanan dosya: 424. Kullanmayanlar az (`DugunKitapSayfa` ve `shared/` yardımcıları).
  **Sonuç:** kategori metinleri ve ortak bölümler taşınınca şablonların neredeyse hepsi kapsanır.
- Şablonlarda `react-i18next` kullanılmıyor (yalnızca `canvas`/`webgl` gibi teknik `t(` eşleşmeleri). Uygulama arayüzü
  11 dilde (`src/locales/*`), **davetiye metinleri yalnızca Türkçe ve koda gömülü**.

### 2.2 Veri ve paket

- `invitations` tablosu: kullanıcı içeriği ayrı kolonlar (`title`, `subtitle`, `names`, `venue`…), özellikler `show_*`
  boolean kolonları (K6: paket kuralı SQL ile doğrulanabilsin).
- `TierResolver::requiredFor()` gereken paketi `davetkart.module_tiers` (kolon → paket) ve `preset_tiers`'tan hesaplar.
  `module_tiers`: `show_rsvp`/`show_timer` standart, `show_envelope`/`show_timeline` gold, `show_gallery`/`show_gift` elit.
- **Yayın kapısı iki yerde:** `PublishInvitationAction` (yayın anı) ve `UpdateInvitationAction::ensureRaisedTierIsOwned()`
  (yayındaki davetiyede gereksinim yükselirse). İkisi de `402` + `PaywallViolationException` (`noPurchase` / `insufficientTier`).
- **Yayındaki davetiyede değişiklik bugün anında canlıya gider** (ayrı taslak katmanı yok). Önbellek `InvitationChanged`
  olayıyla (`updated`) kendiliğinden temizlenir.
- Paylaşılan sözleşmeler: `plan-rules.json`, `error-codes.json` (backend kaynak → frontend `src/contracts/` kopyası,
  `verify:plans` / `verify:errors` eşitliği denetler).

### 2.3 Editör ve asistan

- Bugünkü editör: `components/create/EditorWorkspace.tsx` — solda form paneli (`components/editor/DesignerPanel.tsx`),
  sağda telefon önizlemesi (`components/preview/DeviceSimulator.tsx`); otomatik kayıt `useInvitationAutoSave`.
- Asistan: `POST /api/assistant/chat` → `AskAssistantAction` → `AiProvider` (`GeminiProvider`); günlük 30 mesaj/kullanıcı
  (`davetkart.assistant.daily_message_limit_per_user`), `throttle:assistant`.

## 3. Kapsam

### 3.1 v2.0 (bu faz)

| # | Özellik |
|---|---|
| A | **Metin anahtarı altyapısı:** her sabit metne kalıcı bir anahtar; paylaşılan sözleşme `text-slots.json` |
| B | **Çok dilli altyapı, yalnızca `tr`:** varsayılan metinler dil dosyasında; `invitations.locale`; `Intl` ile tarih |
| C | **Metinleri koddan çıkarma:** önce kategori metinleri + ortak bölümler, sonra hero'lar ve özel şablonlar |
| D | **Backend:** `locale`, `text_overrides`, `has_custom_texts`; doğrulama; Resource; Elit kuralı |
| E | **Tıkla-düzenle** önizlemede + **Metinler paneli**; mobilde alttan açılan panel; karakter sayacı |
| F | **Bölüm ayarları + ➕ özellik ekle**; bölüm gizleme veri silmez |
| G | **Varsayılana dön** (metin başına ve toplu), **onaylı** |
| H | **Asistanla metin önerisi**; öneri onayla uygulanır |
| I | **LCV metinleri** (başlık, buton, teşekkür mesajı, etiketler) |
| J | **Geri al / yinele** (oturum içi) |
| K | **Şablon / kategori değişimi** davranışı |
| L | **Kötüye kullanım önlemleri:** tıklanamaz bağlantılar, misafir sayfasında "bildir" |
| M | **Paket arayüzü:** Elit rozeti, 402 akışında "özel metinler Elit gerektirir" |

### 3.2 Sonraya (v2.1+)

Diğer diller ve misafirin dil seçmesi · asistanla çeviri · ton setleri · LCV özel soru · bölüm sırası · sağdan sola
(Arapça) şablon düzeni · yayındaki davetiye için ayrı taslak katmanı (§9 S2).

### 3.3 Kapsam dışı

Font, renk, boyut, yerleşim düzenlemesi · serbest bölüm/blok ekleme (sayfa kurucu) · HTML/zengin metin.

## 4. Tasarım

### 4.1 Metin anahtarları (`text-slots.json`)

Her sabit metin bir anahtarla okunur. Adlandırma: `<bölüm>.<öğe>`; şablona özel olanlar `hero.<hero-adı>.<öğe>`.

```json
{
  "version": 1,
  "slots": {
    "hero.tagline":            { "scope": "category", "maxLength": 40,  "multiline": false },
    "envelope.label":          { "scope": "category", "maxLength": 40,  "multiline": false },
    "gallery.eyebrow":         { "scope": "shared",   "maxLength": 32,  "multiline": false },
    "gift.note":               { "scope": "category", "maxLength": 240, "multiline": true  },
    "rsvp.submit":             { "scope": "shared",   "maxLength": 28,  "multiline": false },
    "rsvp.thanks":             { "scope": "shared",   "maxLength": 240, "multiline": true  },
    "hero.gazete.issue":       { "scope": "hero:gazete", "maxLength": 24, "multiline": false }
  }
}
```

- `scope`: `shared` (bütün şablonlarda aynı), `category` (kategoriye göre varsayılanı değişir), `hero:<ad>` (tek hero).
  Şablon değişiminde neyin taşınacağını bu belirler (§4.7).
- Kaynak backend'de (`contracts/text-slots.json`), frontend `src/contracts/` kopyası; yeni `verify:text-slots` eşitliği
  denetler (`verify:plans` deseni).
- **Düzenlenmeyen metinler:** `aria-label`, ekran okuyucu metinleri, hata mesajları. Bunlar da dil dosyasına taşınır
  (çok dillilik için) ama sözleşmede yoktur, kullanıcı değiştiremez.

### 4.2 Çok dilli altyapı (yalnızca `tr`)

| Parça | v2.0 | v2.1 |
|---|---|---|
| Varsayılan metinler | `src/locales/tr/invitation.json` (anahtar → metin; kategoriye göre değişenler `category.<id>.<anahtar>`) | `en/invitation.json`… |
| Davetiyenin dili | `invitations.locale` (`varchar(8)`, varsayılan `tr`); arayüzde seçim yok | Dil seçici |
| Okuma | `useInvitationText(key)`: önce `text_overrides[locale][key]`, yoksa `invitation` ad alanında kategori varsayılanı, yoksa ortak varsayılan | Değişmez |
| Tarih, sayı, "gün kaldı" | `Intl.DateTimeFormat(locale)`, `Intl.PluralRules(locale)`; sabit `tr-TR` yazılmaz | Değişmez |

🔴 **Davetiyenin dili arayüz dilinden bağımsızdır.** İngilizce arayüzle Türkçe davetiye hazırlanabilir. Şablonlar
`i18n.getFixedT(invitation.locale, 'invitation')` ile okur, arayüzün `useTranslation()`'ı ile değil.

Sağdan sola: v2.0'da yeni yazılan kodda mantıksal CSS sınıfları (`ms-`/`me-`/`ps-`/`pe-`, `start`/`end`) kullanılır;
mevcut şablonlar sağdan sola için düzeltilmez.

### 4.3 Veri modeli (backend)

| Kolon | Tür | Not |
|---|---|---|
| `locale` | `varchar(8)` not null, varsayılan `'tr'` | v2.0'da yalnızca `tr` geçer (`Rule::in(config('davetkart.invitation_locales'))`) |
| `text_overrides` | `jsonb` null | `{ "tr": { "rsvp.submit": "Geliyorum!" } }` — **yalnızca değişen** metinler, dile göre gruplu |
| `has_custom_texts` | `boolean` not null, varsayılan `false` | K6'nın ruhu: paket kuralı SQL ile doğrulanabilsin |

- `has_custom_texts` **model mutator'ında** `text_overrides` ile birlikte yazılır (`fill()` anında).
  🔴 Veritabanında *generated column* olamaz: `UpdateInvitationAction` paket kontrolünü `save()`'den **önce**, bellekteki
  modelde yapar; generated column bellekte bayat kalır ve kontrol atlanırdı.
- `module_tiers`'a tek satır: `'has_custom_texts' => 'elit'`. `TierResolver`, `PublishInvitationAction` ve
  `UpdateInvitationAction` **değişmez**; iki kapı da kendiliğinden çalışır. `plan-rules.json` `moduleTiers`'a aynı satır.
- `#[Fillable]`'a `locale`, `text_overrides` eklenir; `has_custom_texts` **eklenmez** (yalnızca mutator yazar).
- Varsayılan metne eşit gelen değer saklanmaz (frontend göndermez; backend de varsayılanları bilmediği için bunu
  zorlamaz). Boş metin yok: "varsayılana dön" anahtarı **siler**.

### 4.4 Doğrulama (`InvitationRequest`)

- `text_overrides`: dizi; birinci düzey anahtarlar `invitation_locales` içinde; ikinci düzey anahtarlar `text-slots.json`'da.
- Her değer: `string`, `min:1`, `max:<slot.maxLength>`; `multiline: false` ise satır sonu yok; kontrol karakterleri yok
  (satır sonu hariç); toplam en fazla 120 anahtar.
- HTML **kaçışlanmaz, reddedilmez**: düz metin saklanır, React metni zaten kaçışlar. `dangerouslySetInnerHTML` yasak
  (yeni `verify:text-slots` şablon klasöründe arar).

### 4.5 Editör (frontend)

**Mimari:** `TemplateRenderer` yeni bir `mode: 'edit'` alır. Düzenlenebilir her metin `<EditableText slot="rsvp.submit" />`
ile çizilir: `preview`/`live` kipinde düz metin, `edit` kipinde tıklanabilir ve üzerine gelince kesikli çerçeve.
İş mantığı bileşende değil, `useTextOverridesStore`'da (Zustand; CLAUDE.md §1: alan başına store).

| Parça | Davranış |
|---|---|
| Tıkla-düzenle (masaüstü) | Metne tıklayınca yerinde düzenleme (kontrollü `textarea`/`input`, `contentEditable` değil — yapıştırılan HTML riski). Enter kaydeder (çok satırlıda Ctrl+Enter), Esc vazgeçer. Karakter sayacı `maxLength`'e göre |
| Mobil | Metne dokununca alttan açılan panel; önizlemede taşmayı aynı anda gösterir |
| Metinler paneli | Bütün anahtarlar bölüm bölüm listelenir; değişenler işaretli; klavye ve ekran okuyucu yolu. Panelden bir metne gidince önizleme oraya kayar |
| Varsayılana dön | Metin başına ↺ ve "Tüm metinleri sıfırla". **İkisi de onay ister** (`ui/ConfirmDialog`); toplu sıfırlamada kaç metnin sıfırlanacağı yazar |
| Geri al / yinele | Oturum içi geçmiş (en fazla 50 adım), Ctrl+Z / Ctrl+Shift+Z ve araç çubuğu düğmeleri. Sayfa yenilenince geçmiş silinir |
| Paket | Elit hakkı olmayan kullanıcı taslakta metin değiştirebilir; panelde "Özel metinler Elit pakette yayınlanır" notu. Yayında 402 gelirse paywall'da iki seçenek: **Elit'e yükselt** ya da **özel metinleri sıfırla ve mevcut paketle yayınla** (onaylı) |

Kullanıcının kendi içeriği (`title`, `names`, `venue`, tarih…) aynı tıkla-düzenle ile düzenlenir ama Elit **istemez**;
bunlar bugünkü kolonlara yazılır, `text_overrides`'a değil.

### 4.6 Bölüm ayarları ve ➕ özellik ekle

- Önizlemede bir bölüme tıklamak (başlığın dışında) o bölümün ayar panelini açar: Program → `TimelineEditor`, Hediye →
  banka/IBAN/hediye seçenekleri, LCV → son gün ve menü tercihi, Galeri → `GalleryUploader`. Bugünkü form parçaları yeniden
  kullanılır; `DesignerPanel` bu panellerin kabuğu olur.
- **➕ Özellik ekle:** editörde sabit bir düğme ve bölümler arası ince ➕ çizgileri. Açılan liste kapalı `show_*`
  özelliklerini gösterir (Zarf, Geri sayım, Program, Galeri, Hediye/IBAN, LCV). Seçilen özellik **şablondaki sabit
  yerinde** açılır (sıra değişmez, v2.1) ve ayar paneli hemen açılır.
- Paket dışı özellik listede kilit simgesi ve paket adıyla görünür; eklenebilir (taslakta), kilit yayında (bugünkü kural).
- **Bölümü kaldır:** bölüm menüsünde "Gizle"; `show_* = false` yapılır, **veri silinmez** (IBAN, program adımları kalır).
  Tekrar eklenince geri gelir. Gizleme onay istemez (geri alınabilir), çünkü veri kaybı yok.

### 4.7 Şablon ve kategori değişimi

| Değişim | `shared` | `category` | `hero:<ad>` |
|---|---|---|---|
| Aynı kategoride şablon | Taşınır | Taşınır | Yeni şablonda o hero yoksa **kullanılmaz ama silinmez**; geri dönülünce geri gelir. Kullanıcıya "N özel metin bu tasarımda görünmüyor" notu |
| Kategori | Taşınır | **Sorulur:** "Kategoriye özel N metni koru / varsayılana dön" (ör. düğün "Evleniyoruz" → kına) | Aynı kural |

Görünmeyen özel metinler `has_custom_texts`'i yine `true` tutar. Bu bilerek: aksi halde şablon değiştirip yayınlayıp geri
dönerek Elit kapısı atlanırdı. Paywall ekranında "görünmeyen özel metinleri temizle" seçeneği bulunur.

### 4.8 Asistanla metin önerisi

- Yeni uç: `POST /api/assistant/text-suggestions` `{ invitationId, slot, current }` → `{ data: { suggestions: string[3] } }`.
- `SuggestInvitationTextAction`: istem sunucuda kurulur (kategori, anahtarın anlamı, `maxLength`, dil); kullanıcı yalnızca
  mevcut metni gönderir, serbest istem yok. Yanıt `maxLength`'e göre kırpılmaz, **uymayan öneri atılır**.
- Kota: mevcut günlük 30 mesajdan düşer (`AssistantUsage`), `throttle:assistant`. Sahiplik `InvitationPolicy` ile.
- Frontend: metnin yanındaki ✨ → üç öneri; birine tıklamak **önizler**, "Uygula" ile `text_overrides`'a yazılır.
  Hiçbir öneri kendiliğinden uygulanmaz.

### 4.9 Kötüye kullanım

- Metindeki URL'ler **tıklanabilir yapılmaz** (otomatik bağlantılama yok).
- Misafir sayfasının altına küçük "Bu davetiyeyi bildir" bağlantısı → `POST /api/public/invitations/{id}/report`
  (`throttle`, IP hash'li — KVKK), kayıt + yöneticiye posta (kuyrukta, 15 saniye kuralı). Mevcut `ContactMessage` yapısı
  yeniden kullanılabilir mi, 24.11'de bakılır.
- Uzunluk sınırları (§4.4) zaten serbest uzun metni engeller.

## 5. Adımlar

Her adım ayrı commit; frontend ve backend dalları **Faz 23 bittikten sonra** açılır (24.0). 24.1–24.4 **görsel fark
sıfır** hedefler: davranış değişmez, yalnızca metnin geldiği yer değişir.

| Adım | İş | Depo | Kapı |
|---|---|---|---|
| 24.0 | Faz 23 bitti mi kontrol; dallar `faz-24-v2.0-editor` (frontend/backend, Faz 23'ün birleştiği uçtan); taban kapıları; §2 yeniden ölçülür | fe · be · docs | `npm run check`, `composer check` taban |
| 24.1 | **Envanter:** `templates/` altındaki sabit metinlerin listesi (betik + elle), anahtar adları, `text-slots.json` taslağı, `maxLength` değerleri (bugünkü metnin uzunluğu × tasarıma göre pay) | fe · docs | Liste docs'ta (`phases/faz-24/envanter/`) |
| 24.2 | **Çok dilli altyapı:** `invitation` ad alanı, `tr/invitation.json`, `useInvitationText`, `getFixedT(locale)`, `Intl` yardımcıları (`eventDate.ts`, `calendar.ts`, `useCountdown.ts`) | fe | `verify:i18n`, `verify:time` |
| 24.3 | **Taşıma A:** `flavors.tsx` (11 kategori) + `templates/shared/*.tsx` | fe | Ekran görüntüsü farkı 0 (`scripts/onizleme/cek.ts`, önce/sonra) |
| 24.4 | **Taşıma B:** `shared/heroes/*`, `*/parts/*`, özel şablonlar; yeni `verify:text-slots` kapısı: şablon klasöründe gömülü metin kalmadı, sözleşme iki depoda eşit, `dangerouslySetInnerHTML` yok | fe | Ekran görüntüsü farkı 0; `verify:text-slots` |
| 24.5 | **Backend veri:** migration (`locale`, `text_overrides`, `has_custom_texts`), mutator, `#[Fillable]`, `contracts/text-slots.json`, `InvitationRequest` kuralları, `InvitationResource`/`InvitationPayloadResource`/`PublicInvitationResource` (`locale`, `textOverrides`), `module_tiers` + `plan-rules.json` | be · fe | `composer check`; testler §7 |
| 24.6 | **Frontend durum:** `useTextOverridesStore`, `types.ts` (`TextOverrides`), otomatik kayıt, geri al/yinele | fe | `verify:state`, `verify:content` |
| 24.7 | **Editör:** `mode: 'edit'`, `EditableText`, yerinde düzenleme, mobil panel, Metinler paneli, varsayılana dön (onaylı) | fe | e2e: metin değiştir → kaydet → yenile → kalıcı |
| 24.8 | **Bölüm ayarları + ➕:** tıklanan bölümün paneli, özellik ekle listesi, gizle | fe | e2e: ➕ ile IBAN ekle, gizle, geri ekle → veri duruyor |
| 24.9 | **Şablon/kategori değişimi** (§4.7) | fe | Birim testi: anahtar taşıma kuralı |
| 24.10 | **Asistan önerisi** (§4.8) | be · fe | Backend testleri (kota, sahiplik, uymayan öneri atılır); `NullProvider` ile e2e |
| 24.11 | **Kötüye kullanım:** bildir ucu ve bağlantısı (§4.9) | be · fe | Backend testleri (throttle, IP hash) |
| 24.12 | **Paket arayüzü:** Elit rozeti, paywall'da iki seçenek, fiyat sayfası özellik satırı ve SSS | fe | `verify:pricing`, `verify:plans` |
| 24.13 | Kapanış: kapılar, e2e, erişilebilirlik (`a11y`), `perf` bütçesi, `docs/rehber`, backend `FAZ-24.md`, `v2.0` notları | fe · be · docs | Bütün kapılar |

## 6. Riskler ve önlemler

| Risk | Önlem |
|---|---|
| Uzun metin tasarımı bozar | Anahtar başına `maxLength`, backend'de zorunlu; editörde canlı sayaç; önizleme anında |
| XSS | Düz metin; React kaçışı; `contentEditable` ve `dangerouslySetInnerHTML` yok (`verify:text-slots`) |
| Oltalama / kötüye kullanım | Tıklanamaz bağlantılar, "bildir", uzunluk sınırı (§4.9) |
| Şablon değiştirerek Elit kapısını atlamak | Görünmeyen özel metinler de `has_custom_texts = true` tutar (§4.7) |
| Yayındaki davetiyede yarım yazılmış metin misafire görünür | Bugün de form alanları için geçerli (anında canlı). Yerinde düzenleme yalnızca Enter/"Kaydet" ile yazar, her tuşta değil. Ayrı taslak katmanı §9 S2 |
| Taşıma sırasında görsel bozulma (366 şablon) | 24.3/24.4 önce/sonra ekran görüntüsü karşılaştırması; adım başına commit |
| Taşımadan sonra yeni gömülü metin eklenmesi | `verify:text-slots` kapısı `npm run check`'e girer |
| Varsayılan metin değişince kullanıcınınki ezilir | Yalnızca değişenler saklanır; varsayılan değişikliği yalnızca dokunulmamış metinleri etkiler |
| Asistan maliyeti | Mevcut günlük kota; sunucuda kurulan dar istem; serbest istem yok |
| Davetiye dili ile arayüz dilinin karışması | `getFixedT(invitation.locale)`; e2e: İngilizce arayüzde Türkçe davetiye |

## 7. Test planı (özet)

- **Backend:** Elit hakkı olmayan davetiye özel metinle yayınlanamaz (402 `noPurchase`/`insufficientTier`); yayındaki
  standart davetiyeye özel metin eklemek 402 ve satır yazılmaz; `has_custom_texts` `fill()` anında güncellenir (mutator);
  bilinmeyen anahtar, `maxLength` aşımı, tek satırlıda satır sonu, desteklenmeyen dil → 422; varsayılana dön (anahtarı
  sil) → `has_custom_texts` false olur; `PublicInvitationResource` `textOverrides` taşır, önbellek güncellemede temizlenir;
  asistan önerisi kota ve sahiplik.
- **Frontend:** `useInvitationText` öncelik sırası; şablon/kategori değişim kuralı; geri al/yinele; `verify:text-slots`.
- **e2e:** metin değiştir → yenile → kalıcı; ➕ IBAN ekle/gizle/geri ekle; varsayılana dön onay iptal edilince değişmez;
  Elit'siz yayın → paywall iki seçenek.

## 8. Faz 23 ile ilişki

Faz 23 (ana sayfa vitrin sahnesi) `HomePage`, `PreviewSection`, `DeviceSimulator`'a dokunur. Faz 24 de `DeviceSimulator` ve
şablonlara dokunur. Kod dalları Faz 23 birleştikten sonra açılacağı için çakışma 24.0'da Faz 23'ün son hali üzerinden
çözülür. Faz 23'ün `ui/PhoneFrame` ayrıştırması (23.1) editörün telefon kabuğu için de kullanılır.

## 9. Açık sorular (İsmail)

| # | Soru | Öneri |
|---|---|---|
| S1 | **Karar numaraları.** Faz 22 dalı "sıradaki K277" diyor, Faz 23 dalı hâlâ "K276" diyor (K276'yı Faz 22 aldı). Faz 22 ve 23 açıkken Faz 24 sıradan numara alırsa çakışır | Faz 24'e **K300–K329 aralığı ayrılsın** (Faz 19 hatlarındaki aralık ayırma deseni). Onaylanınca T1–T15 numaralanır ve indekse işlenir |
| S2 | Yayındaki davetiyede değişiklik bugün **anında** canlıya gidiyor. Editörle bu daha sık olacak | v2.0'da bugünkü davranış korunsun (yerinde düzenleme yalnızca onayla yazar); "değişiklikleri yayınla" taslak katmanı v2.1 adayı |
| S3 | Asistan önerisi Elit'e mi bağlı, herkese mi açık? | Herkese açık, günlük kotadan düşsün: öneriyi uygulayan zaten yayında Elit'e takılır (satış akışı) |
| S4 | Kullanıcının kendi içeriği (isimler, mekân, başlık) tıkla-düzenle ile her pakette düzenlenebilsin mi? | Evet; Elit yalnızca **sabit şablon metinleri** için |
| S5 | Bir sabit metin tamamen **boş** bırakılabilsin mi (ör. "Özel Anlarımız" etiketini kaldırmak)? | Hayır (tasarım boşluğu bozulur); kaldırma bölüm düzeyinde "Gizle" ile |
| S6 | Kod dal adı | `faz-24-v2.0-editor` (frontend ve backend) |
