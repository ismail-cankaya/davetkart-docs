# `PHP-LARAVEL-SETUP.md` — Faz 24 Yaması

> **Tarih:** 27 Kasım 2026 · plan [`phases/faz-24/FAZ-24-PLAN.md`](../../phases/faz-24/FAZ-24-PLAN.md) · takip [`phases/faz-24/README.md`](../../phases/faz-24/README.md)
> **Ne bu:** Faz 24'ün (v2.0, davetiye metin editörü) karar **taslakları**. `-EK-FAZ-22` ile aynı biçim.
> ⚠️ **Numara bekliyor:** Faz 22 ve 23 açıkken sıradan numara çakışır (Faz 23 dalı "sıradaki K276" diyor, K276'yı Faz 22
> aldı). Öneri: Faz 24'e **K300–K329** ayrılsın (plan §9 S1). İsmail onaylayınca T1–T15 numaralanır ve
> [`DECISION-INDEX.md`](../DECISION-INDEX.md)'ye işlenir. O zamana kadar bu satırlar indekste **yok**.

---

## A. Karar Kaydı'na eklenecek (§7)

Kaynak: İsmail ile oturum, 27 Kasım 2026. "İsmail'in kararı" yazanlar oturumda açıkça cevaplandı; "öneri" yazanlar plan
§9'da soru olarak duruyor.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **T1** | **Tasarım kilitli, metin serbest.** Editör metinleri (sabit şablon metinleri dahil) ve özellikleri düzenler; font, renk, boyut ve yerleşim düzenlenmez. Serbest blok/sayfa kurucu yok | 366 tasarımın kalitesi korunur, destek yükü sınırlı kalır | taslak · **İsmail'in kararı** |
| **T2** | Her sabit metin kalıcı bir **anahtarla** okunur (`<bölüm>.<öğe>`, şablona özel `hero.<ad>.<öğe>`). Anahtar listesi paylaşılan sözleşme `contracts/text-slots.json` (backend kaynak, frontend kopya; `verify:text-slots` eşitliği ve şablonlarda gömülü metin kalmadığını denetler). Her anahtar `scope` (`shared`/`category`/`hero:<ad>`), `maxLength`, `multiline` taşır | Tek liste hem doğrulamayı (backend) hem editörü (frontend) besler; `plan-rules.json` deseni | taslak · öneri |
| **T3** | **Çok dilli altyapı v2.0'da, yalnızca `tr`.** Varsayılan metinler `src/locales/tr/invitation.json`'a; `invitations.locale` (varsayılan `tr`, v2.0'da yalnızca `tr` geçer); tarih ve çoğullar `Intl` ile. Diğer diller ve dil seçici **v2.1**. Davetiyenin dili arayüz dilinden bağımsız (`getFixedT(invitation.locale)`) | Metinlere zaten tek tek dokunuluyor; ikinci dilde aynı dosyalara yeniden girmek pahalı | taslak · **İsmail'in kararı** (dil kapsamı) |
| **T4** | `invitations.text_overrides` (`jsonb`): **yalnızca değişen** metinler, dile göre gruplu `{ "tr": { "<anahtar>": "<metin>" } }`. Düz metin; satır sonu yalnızca `multiline` anahtarda; kontrol karakteri yok; boş metin yok ("varsayılana dön" anahtarı siler); en fazla 120 anahtar | Varsayılan düzeltmesi dokunulmamış herkese yansır; yeni dil migration istemez; K6'nın `show_*` kolonlarına dokunulmaz | taslak · öneri |
| **T5** | Sabit metin özelleştirmesi **Elit** pakette. `has_custom_texts` boolean kolonu `text_overrides` ile birlikte **model mutator'ında** yazılır; `module_tiers`'a `'has_custom_texts' => 'elit'` (+ `plan-rules.json`). `TierResolver`, `PublishInvitationAction`, `UpdateInvitationAction` değişmez; iki kapı (yayın ve yayındaki güncelleme) kendiliğinden çalışır. Kullanıcının kendi içeriği (`title`, `names`, `venue`…) Elit istemez | K6: paket kuralı SQL ile doğrulanabilir kalır. Generated column olamaz: güncelleme kontrolü `save()`'den önce bellekte yapılır, generated column orada bayat kalır | taslak · **İsmail'in kararı** (Elit) · uygulama biçimi öneri |
| **T6** | Elit hakkı olmayan kullanıcı taslakta metin değiştirip önizleyebilir; kilit **yayında** (bugünkü 402 akışı). Paywall'da iki seçenek: Elit'e yükselt / özel metinleri sıfırla ve mevcut paketle yayınla (onaylı) | Bugünkü özellik kilidiyle aynı kalıp; kullanıcı değişikliği görüp yükseltir | taslak · öneri |
| **T7** | **Bölüme tıklayınca ayarları açılır; editörde ➕ ile kapalı özellik eklenir** (Zarf, Geri sayım, Program, Galeri, Hediye/IBAN, LCV). Özellik şablondaki sabit yerinde açılır. Paket dışı özellik kilit simgesiyle görünür, taslakta eklenebilir. **Gizle** `show_* = false` yapar, **veri silmez** | İsmail: "+ işaretine basınca IBAN kısmı eklensin"; gizleme geri alınabilir olsun diye veri korunur | taslak · **İsmail'in kararı** (➕) · gizleme davranışı öneri |
| **T8** | **Varsayılana dön** metin başına ve toplu; **ikisi de onay ister**, toplu onayda kaç metin sıfırlanacağı yazar | İsmail: "onay sorsun, direkt sıfırlamasın" | taslak · **İsmail'in kararı** |
| **T9** | **Asistanla metin önerisi:** `POST /api/assistant/text-suggestions`, istem sunucuda kurulur (serbest istem yok), 3 öneri, `maxLength`'e uymayan öneri atılır, mevcut günlük kotadan düşer. Öneri yalnızca kullanıcı "Uygula" derse yazılır | Maliyet ve kötüye kullanım sınırlı; kullanıcı kontrolü | taslak · **İsmail'in kararı** (kapsam) · ayrıntı öneri |
| **T10** | **Şablon/kategori değişimi:** `shared` ve `category` anahtarlar aynı kategoride taşınır; `hero:<ad>` anahtarlar yeni şablonda yoksa kullanılmaz ama silinmez. Kategori değişince kategoriye özel metinler için "koru / varsayılana dön" sorulur. Görünmeyen özel metinler de `has_custom_texts`'i `true` tutar | Kullanıcı emeği kaybolmaz; şablon değiştirip geri dönerek Elit kapısı atlanamaz | taslak · öneri |
| **T11** | **LCV metinleri** (başlık, etiketler, buton, teşekkür) v2.0'da anahtar sistemine girer. LCV'ye **özel soru** alanı v2.1 | Anahtar sisteminin doğal parçası; özel soru veri modelini değiştirir | taslak · **İsmail'in kararı** |
| **T12** | **Geri al / yinele** oturum içi (en fazla 50 adım); sayfa yenilenince geçmiş silinir | Editör hissi; kalıcı sürüm geçmişi ayrı iş | taslak · **İsmail'in kararı** |
| **T13** | v2.1+'a kalanlar: diğer diller ve misafirin dil seçmesi, asistanla çeviri, ton setleri, LCV özel soru, **bölüm sırası**, sağdan sola şablon düzeni, yayındaki davetiye için taslak katmanı | Kapsamı v2.0'da sınırlı tutmak | taslak · **İsmail'in kararı** (ton setleri, bölüm sırası, diller) |
| **T14** | **Kötüye kullanım:** metindeki URL'ler tıklanabilir yapılmaz; misafir sayfasında "bildir" (`POST /api/public/invitations/{id}/report`, throttle, IP hash'li, yöneticiye posta kuyrukta). Yerinde düzenleme `contentEditable` değil kontrollü alan; şablonlarda `dangerouslySetInnerHTML` yok | Davetkart alan adında oltalama sayfası riski; XSS yüzeyi sıfır kalsın | taslak · **İsmail'in kararı** (riskler ve önlemler) |
| **T15** | Kod dalları (frontend, backend) **Faz 23 bittikten sonra** açılır; Faz 24 içerik olarak Faz 23'e bağlı değil. Docs işi şimdi başlar; docs için commit/dal/push asistana serbest (bu oturum) | İsmail'in sırası | taslak · **İsmail'in kararı** |

**Eski kararlarla ilişki:**

- K6 (hibrit veri modeli) → değişmez; `has_custom_texts` aynı ilkeyle ayrı boolean kolon. `text_overrides` paket kuralının
  girdisi değil, içerik (K6'nın "sorgulanmayacak küçük veri jsonb" ilkesi).
