# Faz 27–29 — v2.1: Önizleme ve Tasarım Stüdyosu (Plan)

> **Durum:** ✅ Plan onaylandı (İsmail, 28 Kasım 2026) · kod sürüyor, takip [`README.md`](README.md).
> **Sürüm:** v2.1 (İsmail: *"Bu işlemimiz v 2.1 olacak"*). Faz 24–26 = v2.0.
> **Bölünme:** İsmail: *"işler çok uzarsa fazları bölebilirsin, 3 faza kadar"* → Faz 27 altyapı, Faz 28 stüdyo, Faz 29
> önizleme ve paylaşım (K329).
> **Taban:** frontend ve backend `faz-26-v2.0-texts`. Önce Faz 26'nın kalan 243 metni kendi dalında biter (26.3).
> **Kararlar:** K318–K329 ([`EK-FAZ-27`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-27.md)), Faz 24'e ayrılan
> K300–K329 aralığının kalanı.

## 0. Özet

Panelde her davetiyenin iki düzenleme kapısı olur:

- **Önizleme** (hızlı düzenleme, `/dashboard/preview/:id`): solda temel bilgiler (isimler, başlık, tarih, mekân, konum),
  sağda telefon önizlemesi. Teknik ayrıntı yok, paket istemez.
- **Düzenle** (Tasarım Stüdyosu, `/studio/:id`): Canva / WordPress gibi ayrı, tam ekran editör. Solda menü, orta-sağda
  davetiye (varsayılan telefon, ekrana sığar; tablet, bilgisayar, tam ekranda düzenle), sağda gerektiğinde açılan
  ayrıntı paneli. Başlıklar dahil bütün metinler tıklanarak düzenlenir.

Yayındaki davetiyede stüdyo değişiklikleri önce taslağa yazılır, **"Değişiklikleri yayınla"** ile misafire geçer.

## 1. İstek (İsmail, 28 Kasım 2026)

> Davetiye düzenle kısmında güncelleme yapacağız. Profil kısmında davetiyelerde Görüntüle yeşil renk ile, Kopyala
> Paylaş diye güncellenecek (en son adım), Önizleme ve Düzenle. Önizlemeye basıldığında kullanıcı davetiyenin temel
> bilgilerini değiştirebilecek, diğer yanda cep telefonundan önizleme yapabilecek; kullanıcı teknik detaya boğulmadan
> isim soyisim vs. düzenlesin. Düzenle kısmında Canva, WordPress gibi ayrı sayfada bir düzenleme editörü (Tasarım
> stüdyosu): PC'de bir yanda menü (önceki düzenledeki kısımlar: isimler, konum, bölümler…), diğer yanda davetiye
> varsayılan olarak cep telefonunda, ekrana sığacak şekilde; altta tablet, bilgisayar, tam ekranda düzenle. Davetiyede
> bazı metinler düzeltilmiyor; başlıklar dahil tüm metinler düzeltilsin. Metinlerin üzerine basarak düzenleme olsun;
> ayrıntılı düzenleme sayfası açılacaksa davetiyenin yanında açılsın.

Oturumdaki kararlar:

| Konu | İsmail |
|---|---|
| Sağ / sol | *"Sağ ile soldaki menüler yer değiştirsin"* → menü **solda**, davetiye orta-sağda, ayrıntı paneli **sağda**; Önizleme'de form solda, telefon sağda |
| Ek fikirler (taslak katmanı, misafir gözüyle, kontrol listesi, taşma uyarısı, telefonda aç) | *"5'i de olsun"*; telefonda aç (QR) *"zor iş gibi, en sona kalabilir"* |
| Adres | `/dashboard/onizle/:id` değil, İngilizce: `/dashboard/preview/:id` |
| Sürüm ve bölünme | v2.1; en çok 3 faz |
| Git | Bu oturum boyunca üç depoda dal, commit, push serbest; `main`'e dokunulmaz (K316 ilkesi) |
| Varsayılanlar (plan onayıyla) | Kart düğmeleri "Önizleme" ve "Düzenle"; sihirbaz stüdyoya geçer (tek editör); Faz 26 önce biter; Paylaş'ta QR var |

## 2. Mevcut durum (ölçüm, `faz-26-v2.0-texts` @ `fc8cc5c`)

| Konu | Bulgu |
|---|---|
| Panel kartı | Yayında `Görüntüle` · `Kopyala` · `Düzenle`; kayıtlıda `Düzenlemeye Devam Et`. İkisi de `/create/:id` (`DashboardPage.tsx:140-175`) |
| Editör | Sihirbazın 3. adımı `EditorWorkspace`: solda `DesignerPanel`, sağda `DeviceSimulator`, altta Yayınla. Site çerçevesi içinde, ayrı sayfa değil |
| Düzenlenemeyen metin (1) | Faz 26 bitmedi: 69 dosyada **243** gömülü metin (`scripts/text-slots/baseline.json`) |
| Düzenlenemeyen metin (2) | Kullanıcı içeriği (isimler, başlık, alt başlık, mekân, tarih) önizlemede tıklanmıyor: `EditableTextMark` yalnızca şablon anahtarlarında. `invitation.names`/`displayNames(` 74, `invitation.title` 48 dosyada doğrudan çiziliyor |
| Cihaz önizlemesi | Şablon sayfadaki bir kutuya çiziliyor (`DeviceSimulator.tsx:230`); 116 şablon dosyası `sm:/md:/lg:` kullanıyor ve bunlar **tarayıcı penceresine** bakar. Tablet/bilgisayar önizlemesi cihazı taklit etmiyor |
| Yayındaki davetiye | Her değişiklik anında canlı (K306); `UpdateInvitationAction` yayında paket farkını sorar (402) |

## 3. Tasarım

### 3.1 Panel kartı (K326)

| Kart | Düğmeler |
|---|---|
| Yayında | `[Görüntüle 🟢] [Paylaş]` / `[Önizleme] [Düzenle]` · Sil altta |
| Taslak | `[Önizleme] [Düzenle]` · Sil altta |
| Bekleyen değişiklik | Rozet: "Yayınlanmamış değişiklik var" |

### 3.2 Önizleme — hızlı düzenleme (K318, K324)

- Tam ekran katman, adres `/dashboard/preview/:id`; geri tuşu kapatır.
- **Solda** form: isimler, başlık, alt başlık, tarih-saat, mekân ve konum. **Sağda** ekrana sığan telefon önizlemesi.
- Paket istemez (K305). Açık **Kaydet**; yayındaki davetiyede düğme **"Kaydet ve yayınla"**, misafire hemen yansır; aynı
  alanlar stüdyonun taslağından düşer (alan bazında son kaydeden kazanır).
- Kaydedilmemiş değişiklikle kapatmada sorar. "Stüdyoda aç" bağlantısı.
- Telefonda: önizleme üstte, "Bilgileri düzenle" alttan panel.

### 3.3 Tasarım Stüdyosu (K319–K322, K325)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ ← Panel  Ayşe & Mehmet · Kaydedildi ✓  Hazır 4/5  ↶ ↷  👁 Misafir gözüyle  [Değişiklikleri yayınla] │
├───────────────────┬───────────────────────────────────────────┬─────────────────────┤
│ SOL MENÜ          │                                           │ SAĞ DENETÇİ         │
│ ▸ Bilgiler        │              ┌─────────┐                  │ (gerekince açılır)  │
│ ▸ Bölümler (+)    │              │ davetiye│ ← metne tıkla,   │ Program, Galeri,    │
│ ▸ Metinler        │              │ ekrana  │   yerinde düzenle│ Hediye/IBAN, LCV,   │
│ ▸ Tema            │              │ sığar   │                  │ Konum               │
│ ▸ Kontrol listesi │              └─────────┘                  │                     │
│                   │   📱 Telefon · Tablet · Bilgisayar   Sığdır · %   ⛶ Tam ekranda düzenle │
└───────────────────┴───────────────────────────────────────────┴─────────────────────┘
```

- Ayrı sayfa, site üst/alt çerçevesi yok. `/studio/:id`; giriş yapmamış kullanıcı `/studio` (yerel taslak).
- **Sol menü:** bugünkü `DesignerPanel` sekmelere bölünür (Bilgiler · Bölümler · Metinler · Tema · Kontrol listesi).
  Bölüm adına tıklamak tuvali o bölüme kaydırır.
- **Tuval:** varsayılan telefon, kullanılabilir alana sığacak ölçek; alt çubukta cihaz, yakınlaştırma (Sığdır / %),
  **Tam ekranda düzenle** (paneller gizlenir, düzenleme açık, Esc çıkar).
- **Tıkla-düzenle:** şablon metinleri (K306) **ve** kullanıcı içeriği (K321).
- **Sağ denetçi:** Program, Galeri, Hediye/IBAN, LCV, Konum ayarları; bugünkü `SectionSettingsDrawer`'ın yerini alır.
  1440 px'ten dar ekranda tuvalin üstüne kayan katman.
- **Telefon:** tuval tam ekran; alt çubuk sekmeleri alttan panel olarak açar.
- **Misafir gözüyle:** editör çerçevesi olmadan tam ekran, zarf baştan.
- **Kontrol listesi:** isimler örnek metin, tarih yok/geçmiş, mekân boş, LCV açık ama son gün yok. Maddeye tıklamak
  ilgili alanı açar. Üst çubukta "Hazır n/m".
- **Taşma uyarısı:** metin kutusundan taşıyorsa (`scrollWidth > clientWidth` / `scrollHeight > clientHeight`) önizlemede
  ve Metinler panelinde ⚠️.

### 3.4 Tek editör (K322)

Sihirbaz (kategori → tema → bilgiler → üretim ekranı) aynı kalır, sonunda `/studio/:id`'ye (anonimse `/studio`) geçer.
`EditorWorkspace` ve `/create/:id`'nin editör aşaması kalkar; `/create/:id` stüdyoya yönlendirir (eski bağlantılar
kırılmaz).

### 3.5 Tuval: aynı uygulamada `iframe` (K320)

- Şablon, aynı kaynaktaki boş bir `iframe`'in belgesine React portal ile çizilir; ana belgenin stilleri (`<style>`,
  `<link rel=stylesheet>`, yazı tipleri) kopyalanır ve izlenir. `md:/lg:` sınıfları iframe genişliğine göre çalışır.
- Çizim gerçek genişlikte (telefon 390, tablet 820, bilgisayar 1280 px), `transform: scale()` ile alana sığdırılır.
- Store'lar, editör köprüsü ve olaylar aynı React ağacında kalır (portal); tıklanan metnin konumu iframe ofseti ve ölçekle
  ana belgeye çevrilir.
- Misafir sayfası (`/invite/:id`) değişmez. Ana sayfa vitrin önizlemesi bugünkü `DeviceSimulator` ile kalır.
- 27.1 deneme ve ölçümle başlar; çalışmazsa İsmail'e dönülür (geri dönüş: yalnızca telefon doğru).

### 3.6 Kullanıcı içeriğinde tıkla-düzenle (K321)

- `InvField` (`field="names" | "title" | "subtitle" | "venue" | "date"…`): editör köprüsü yoksa çocuklarını olduğu gibi
  çizer (misafir DOM'u aynı → 762 çizimlik anlık görüntü birebir), varsa `EditableTextMark` gibi tıklanır.
- Tıklayınca yerinde düzenleyici alanı `useInvitationStore`'a yazar (paket yok, `text_overrides`'a değil). Tarih için
  tarih-saat seçici, mekân için sağ denetçide Konum.
- Dönüşüm betikle (Faz 24 deseni) + elle; `verify:text-slots` benzeri bir kapı `invitation.title`/`names` çıplak
  çizimini sayar, tavan yalnızca iner.

### 3.7 Taslak katmanı (backend, K323)

| Parça | Ayrıntı |
|---|---|
| Kolon | `invitations.pending_changes` `jsonb` null: canlıdan **farklı** alanlar (`attributes`, `text_overrides`, `timeline_events`, `gallery_media_ids`) |
| `PUT /invitations/{id}/pending` | Yalnızca yayındaki davetiye; doğrulama `InvitationRequest` ile aynı; paket kontrolü **yok** (taslak serbest, K43 ruhu) |
| `POST /invitations/{id}/pending/publish` | Taslağı `UpdateInvitationAction`'dan geçirir (kilit, paket farkı, 402 aynı yerde); başarıda `pending_changes = null` |
| `DELETE /invitations/{id}/pending` | Taslağı atar |
| Yanıt | `InvitationResource` → `pendingChanges` (camelCase, açık dönüşüm) ve `hasPendingChanges`; `PublicInvitationResource` değişmez, önbellek değişmez (`pending_changes` yazımı `InvitationChanged` fırlatmaz) |
| Hızlı düzenleme | Yayında normal `PUT /invitations/{id}`; yazılan alanlar `pending_changes`'tan düşer (`UpdateInvitationAction` içinde) |
| Taslak olmayan davetiye | Bugünkü gibi doğrudan yazılır |
| Sınır | Galeriye yükleme/silme anında (medya Action'ları); yalnızca galeri **sırası** taslakta |
| Yetki | `InvitationPolicy::update` |

### 3.8 Telefonda aç (K328, en son adım)

`POST /invitations/{id}/preview-link` → `{ url, expiresAt }` (24 saat, `URL::temporarySignedRoute`). Bağlantı frontend
`/preview/:id?expires&signature` sayfasını açar; sayfa `GET /api/public/invitations/{id}/preview?expires&signature`'dan
canlı + taslak birleşik veriyi okur. Önbelleksiz, `X-Robots-Tag: noindex`, taslak (yayında olmayan) davetiyede de çalışır,
LCV ve misafir yüklemesi gönderim yapmaz. Stüdyo ve Önizleme'de QR kod olarak gösterilir.

### 3.9 Paylaş (K327)

Telefonda `navigator.share` (cihazın menüsü); masaüstünde menü: Bağlantıyı kopyala · WhatsApp · QR kod. QR kütüphanesi
tembel parça.

## 4. Fazlar ve adımlar

| Adım | İş | Depo |
|---|---|---|
| **26.3** | Kalan 243 gömülü metin anahtara (tavan → 0); `TakvimHero` ay/gün adları `Intl` | fe · be (sözleşme kopyası) |
| **Faz 27 — altyapı** | | |
| 27.0 | Plan ve kararlar | docs |
| 27.1 | `iframe` tuval (`DeviceCanvas`): gerçek genişlik, ölçek, stil eşleme, tıklama konumu | fe |
| 27.2 | `InvField`: kullanıcı içeriğinde tıkla-düzenle, şablon dönüşümü, kapı | fe |
| 27.3 | Taslak katmanı: migration, Action'lar, uçlar, Resource, testler | be |
| 27.4 | Frontend: taslak servisi ve store (yayındaysa otomatik kayıt taslağa) | fe |
| **Faz 28 — stüdyo** | | |
| 28.1 | `/studio/:id` iskeleti, üst çubuk, sol menü sekmeleri | fe |
| 28.2 | Tuval alanı, cihaz çubuğu, yakınlaştırma, tam ekranda düzenle | fe |
| 28.3 | Sağ denetçi, telefonda alt çubuk | fe |
| 28.4 | Taslak arayüzü: "Değişiklikleri yayınla" / "Vazgeç", rozetler | fe |
| 28.5 | Misafir gözüyle, kontrol listesi, taşma uyarısı | fe |
| 28.6 | Sihirbaz → stüdyo, `EditorWorkspace` kalkar, e2e | fe |
| **Faz 29 — önizleme ve paylaşım** | | |
| 29.1 | `/dashboard/preview/:id` hızlı düzenleme | fe |
| 29.2 | Panel kartı düğmeleri | fe |
| 29.3 | Paylaş menüsü | fe |
| 29.4 | Telefonda aç: imzalı önizleme bağlantısı (be) + QR (fe) | be · fe |
| 29.5 | Kapanış: kapılar, e2e, erişilebilirlik, paket bütçesi, `docs/rehber`, backend `FAZ-27/28/29.md` | hepsi |

Her adım ayrı commit ve push. Kapılar: `npm run check`, `composer check`, anlık görüntü (762 çizim, şablona dokunan
adımlarda), ilgili e2e.

## 5. Riskler

| Risk | Önlem |
|---|---|
| `iframe`: Lenis, motion, yazı tipleri, tam ekran, popover konumu | 27.1 en başta, ölçümle; olmazsa İsmail'e dönülür |
| Taslak ile hızlı düzenleme çakışması | Alan bazında son kaydeden kazanır (§3.7) |
| Taslağın misafire sızması | `PublicInvitationResource` `pending_changes` okumaz; test |
| Taslakla paket kapısını atlamak | Yayınlama `UpdateInvitationAction`'dan geçer; test (402, satır yazılmaz) |
| Paket bütçesi (720 / 800 kB) | Stüdyo, önizleme, QR tembel parça; `verify:bundle` |
| `InvField` dönüşümünde görsel bozulma | Anlık görüntü birebir; adım başına commit |
| e2e tüm paket backend + PowerShell ister | Bu ortamda editör projeleri koşar; koşmayan "koşmadı" yazılır (B7) |
