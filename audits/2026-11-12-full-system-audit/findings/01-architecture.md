# Mimari ve kod kalitesi (backend) — AUD-2026-11-12

> Yürüten: ana oturum (Fable 5.2) · Kopya: `_audit-snap\backend` · Commit: `d810410` (`origin/ccr-9a346997-bu6gve`) · Tarih: 13 Kasım 2026
> Dilim ajanı kullanım sınırına takıldığı için bu dilimi ana oturum tek başına yürüttü.

## Özet

Backend'in iskeleti sağlam: Controller → FormRequest → Action → Model zinciri okuduğum her uçta tutuluyor,
para kuruş cinsinden tam sayı, durum makineleri enum'da, yarışa açık her yazma `lockForUpdate()` altında ve
veritabanı 30 CHECK kısıtıyla kendi değişmezlerini koruyor. Bulduğum sorunların çoğu kodda değil **kayıtta**:
karar indeksi kodun 18 karar gerisinde, Faz 16–17'nin faz kaydı yok, K18 (kısa yorum) kuralı dosyaların
%92'sinde çiğneniyor. Kodla ilgili iki tasarım boşluğu (ilk yayın indirimi, kullanılmış hakkın iadesi) para
etkisi taşıdığı için güvenlik dosyasında (`SEC-01`, `SEC-02`) anlatıldı; burada yalnızca atıf var.

**Kapsam dürüstlüğü:** `app/` altındaki 235 dosyanın ~75'i yorumlar ayıklanarak satır satır okundu (ödeme,
fiyat, hediye kodu, iade, davetiye yaşam döngüsü, kimlik/hesap, LCV, medya yükleme, ara katmanlar, sağlayıcı,
rotalar, zamanlayıcı). Geri kalanı (Resource'ların çoğu, `OptimizeUploadedImage`'ın gövdesi, konsol
komutlarının çoğu, asistan, iletişim, bildirim sınıfları) yalnızca kalıp taramasıyla (`grep`) geçildi. 29
migration'ın kısıt ve index satırları tarandı, dosyalar tek tek okunmadı.

Seviye sayıları: 🔴 0 · 🟠 0 · 🟡 5 · 🟢 4 · 💡 1 — Kanıt: KOŞTURULDU 7 · KOD OKUMASI 3

## Özet tablosu

| ID | Seviye | Kanıt türü | Başlık | Nerede | Efor | Tek satır öneri |
|---|---|---|---|---|---|---|
| ARC-01 | 🟡 | KOŞTURULDU | Karar indeksi K128–K145'i bilmiyor; "sıradaki boş numara" yanlış | `davetkart-docs/decisions/DECISION-INDEX.md:8` | S | İndekse 18 satır ekle, sıradaki numarayı K146 yap |
| ARC-02 | 🟡 | KOŞTURULDU | Faz 16 ve 17'nin faz kaydı yok; Faz 15 kaydı "kalite kapısı koşmadı" diyor | `backend:docs/rehber/fazlar/` | S | `FAZ-16.md`, `FAZ-17.md` yaz; kapıyı koşup sonucu işle |
| ARC-03 | 🟡 | KOŞTURULDU | K18 dosyaların %92'sinde çiğneniyor; 79 dosyanın kılavuzu yok | `backend:app/**`, `routes/api.php` | L | Uzun blokları `docs/rehber/`'e taşı; kuralı CI'da ölç |
| ARC-04 | 🟡 | KOD OKUMASI | K55 "yerel disk kalır" geçerli görünüyor ama yayın planı S3 kuruyor | `DECISION-INDEX.md:67`, `backend:config/davetkart.php:121` | S | K55'i geçersiz kılan yeni kararı yaz |
| ARC-05 | 🟡 | KOŞTURULDU | Eski `claude/…` yolları: backend'de 25 dosya; backend'in kendi `claude/` klasörü hâlâ ikinci ev | `backend:docs/*.md`, `backend:claude/` | M | `claude/`'u doküman deposuna taşı, atıfları güncelle |
| ARC-06 | 🟢 | KOŞTURULDU | Üç hata kodu hiçbir yerde fırlatılmıyor | `backend:app/Enums/ErrorCode.php:22,29,49` | S | Sil ya da "ayrılmış" diye işaretle |
| ARC-07 | 🟢 | KOŞTURULDU | Frontend'de `.gitattributes` yok; sözleşme dosyası CRLF, backend'deki LF | `frontend:src/contracts/error-codes.json` | S | `* text=auto eol=lf` + yeniden normalize |
| ARC-08 | 🟢 | KOŞTURULDU | Dal hijyeni: 30+ dal, yazım hatalı adlar, etiket yok, `main` 4 commit geride | iki kod deposu | M | Birleşmiş dalları sil, sürümleri etiketle |
| ARC-09 | 🟢 | KOD OKUMASI | Checkout idempotent değil: her çağrı yeni `pending` sipariş açar | `backend:app/Actions/Payment/StartCheckoutAction.php:111-142` | M | Aynı (kullanıcı, davetiye, plan) için açık siparişi yeniden kullan |
| ARC-10 | 💡 | KOD OKUMASI | `OptimizeUploadedImage` 664 satır, tek sınıfta dört sorumluluk | `backend:app/Jobs/OptimizeUploadedImage.php` | M | Kod çözme / EXIF / yeniden kodlama / dosya takası ayrı sınıflar |

## Neler iyi

Bunlar bozulmaması gereken tasarımlar; her biri kodda ya da canlı sondada görüldü.

1. **Fiyat istekten okunmuyor, mimari olarak okunamıyor.** `StoreCheckoutRequest` yalnızca `tier` ve `giftCode`
   doğrular (`app/Http/Requests/Payment/StoreCheckoutRequest.php:50-56`); tutar `QuotePriceAction` → `PriceQuote`
   zincirinden gelir (`StartCheckoutAction.php:113,297-304`). Sonda P12: gövdeye `price:1, currency:USD,
   status:paid` konuldu, sipariş `9960 kuruş / TRY / pending` açıldı. Kural bir `if` değil, veri akışının şekli.
2. **İdempotans iki katmanlı.** `provider_ref` UNIQUE ikinci satırı, `OrderStatus::canTransitionTo()` +
   `lockForUpdate()` aynı satırın iki kez ilerlemesini engeller (`HandlePaymentCallbackAction.php:57-95`,
   `OrderStatus.php:114-122`). Sonda P21–P23: tekrar oynatılan `paid` hiçbir şeyi değiştirmedi, `paid → failed`
   reddedildi, `expired → paid` kabul edildi.
3. **Sahiplik yoksa 404.** `AuthorizationException` ve `ModelNotFoundException` aynı koda iner
   (`ApiExceptionRenderer.php:123-124`); sonda P02–P08, P27, P45, P46, P68: ikinci kullanıcının on bir denemesi
   de `404 RESOURCE_NOT_FOUND`.
4. **Veritabanı kendi kurallarını biliyor.** 30 CHECK kısıtı (durum, plan, tutar ≥ 0, indirim kaynakları,
   `consumed_at`), kısmi UNIQUE index (`refund_requests_one_open_per_order`), `float`/`decimal` kolon yok
   (`evidence/commands` yok; komut bu dosyanın "Koşturulan komutlar" bölümünde).
5. **Strateji arayüzleri sessiz varsayılana düşmüyor.** Ödeme ve AI sürücüsü `match` ile çözülür, bilinmeyen değer
   503 fırlatır (`AppServiceProvider.php:81-90,118-123`); Shopier sırrı eksikse sürücü kurulmaz
   (`ShopierGateway.php:85-100`).
6. **Dış servis transaction'ın dışında.** Sipariş ve hediye kodu kullanımı tek transaction'da yazılır, sağlayıcı
   çağrısı sonra yapılır, hata olursa sipariş `failed` olur ve kod serbest kalır (`StartCheckoutAction.php:111-172`).
7. **Dosya sistemi de transaction'ın dışında, ama telafi ediliyor.** Dosya önce yazılır, satır kilit altında
   eklenir, hata olursa dosya silinir (`StoreUploadedMediaAction.php:72-121`); hesap silmede dosyalar commit'ten
   sonra silinir (`DeleteAccountAction.php:44-84`).
8. **Auth'suz rotalar tek önekte.** `/api/public/` grubu (`routes/api.php:301-437`) "auth unutuldu mu" sorusunu bir
   hatırlama meselesi olmaktan çıkarıyor; sonda P01: sekiz korumalı uç kimliksiz 401.
9. **Hata sözleşmesi tek yerde.** `ApiExceptionRenderer` bütün istisnaları `{error:{code,fields?,params?}}`
   zarfına çevirir; `contracts/error-codes.json` iki depoda anlamsal olarak aynı (28 kod,
   `evidence/commands/FE-error-codes-compare.txt`).
10. **4xx iş istisnaları Sentry'ye gitmiyor** (`bootstrap/app.php:56-58`).

## Bulgular

### ARC-01 Karar indeksi K128–K145'i bilmiyor; "sıradaki boş numara" yanlış
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `davetkart-docs/decisions/DECISION-INDEX.md:8` ("Sıradaki boş numara: K128") · `backend:docs/rehber/fazlar/FAZ-13.md:48-60` (K128–K136) · `backend:docs/rehber/fazlar/FAZ-14.md:70-78` (K137–K145)
- Senaryo: 1) Faz 13 ve 14 backend deposunda K128–K145'i tanımladı. 2) 12 Kasım'daki depo düzenlemesi indeksi `davetkart-docs` içindeki dosyalardan üretti; backend'in `docs/rehber/fazlar/` klasörünü taramadı. 3) İndeks "K1–K127, sıradaki K128" diyor. 4) `CLAUDE.md` §5'e uyan bir sonraki asistan yeni karara K128 verir; bu numara kodda 19 yerde başka bir kararı (fiyatın tek kaynağı backend) gösteriyor.
- Kanıt: `grep -rhoE "\bK1(2[89]|[3-9][0-9])\b" app routes config tests docs database | sort | uniq -c` → `19 K128 · 12 K129 · 6 K130 · 7 K131 · 10 K132 · 28 K133 · 21 K134 · 12 K135 · 14 K136 · 21 K137 · 19 K138 · 15 K139 · 9 K140 · 6 K141 · 5 K142 · 14 K143 · 17 K144 · 2 K145`
- Etki: Numara çakışması. Karar numaraları kod yorumlarında, testlerde ve kılavuzlarda atıf olarak kullanıldığı için aynı numaranın iki anlam taşıması "bu kural neden var" sorusunun cevabını bozar.
- Neden önemli (öğretici not): Karar kaydı (ADR) bir **tek doğruluk kaynağı** olmak zorunda. İki depoya bölünmüş bir kayıtta her taraf diğerini eksik görür. Düzeltme numarayı değiştirmek değil (numara asla yeniden kullanılmaz), indeksi kaynağa yetiştirmektir.
- Öneri: İndekse K128–K145 satırlarını ekle (kaynak sütunu: backend `docs/rehber/fazlar/FAZ-13.md` §4 ve `FAZ-14.md`), başlığı "Sıradaki boş numara: **K146**" yap. `_restructure/build_decision_index.py`'ye backend faz dosyalarını da okut.
- Test önerisi: `build_decision_index.py --check`: backend ve doküman deposundaki bütün `K\d+` tanımlarını toplar, indekste olmayan numara varsa sıfır dışı çıkar. Öldürmesi gereken mutant: indeksten bir satırı silmek.
- Efor: S
- İlgili: R17 · `_restructure/REPORT.md` §3

### ARC-02 Faz 16 ve 17'nin faz kaydı yok; Faz 15 kaydı "kalite kapısı koşmadı" diyor
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:docs/rehber/fazlar/` (en yeni dosya `FAZ-15.md`) · `backend:docs/rehber/fazlar/FAZ-15.md:4,33-43` · commit'ler `82c7312` (16.1) ve `d810410` (17.1)
- Senaryo: 1) Faz 15–17 bulut çalışma alanında (PHP 8.3) yazıldı; proje PHP ^8.5 istediği için `composer check` orada koşamadı. 2) Faz 16 on, Faz 17 dokuz şablonu `config/davetkart.php` → `preset_tiers`'e Gold olarak ekledi (`config/davetkart.php:81-103`). 3) İki faz için ne faz özeti ne elle doğrulama dosyası yazıldı. 4) Bu denetimdeki koşu bu dal için ilk gerçek koşu oldu ve kapı kırmızı çıktı (`TST-01`).
- Kanıt: `ls backend/docs/rehber/fazlar | grep -E "FAZ-1[5-7]"` → yalnızca `FAZ-15.md`. `evidence/commands/TST-step1-pint.txt` → `"result":"fail"`.
- Etki: Gold'a bağlanan 19 şablon bir **fiyat kararı**; kaydı yalnızca commit mesajında duruyor. Kapı koşmadan birleştirilen kod, projenin kendi "faz kapanış ölçütü" kuralını (T16, B7) atlıyor.
- Neden önemli (öğretici not): Bir kuralın değeri, uygulanamadığı gün ne olduğuyla ölçülür. "Ortam uygun değildi" gerekçesi kapıyı geçici olarak açar; açık kaldığını kimse izlemezse kalıcı olur. Kapıyı koşturamayan ortamda yazılan iş, kapıyı koşturabilen ortamda kapanana kadar "bitmedi" sayılmalı.
- Öneri: `FAZ-16.md` ve `FAZ-17.md` (ne eklendi, hangi karar, doğrulama durumu) + hangi şablonun neden Gold olduğu kararını K numarasıyla kaydet. Bulut ortamına PHP 8.5 kurulamıyorsa GitHub Actions'taki `composer check` sonucunu faz kapanış kanıtı olarak kullan.
- Test önerisi: —
- Efor: S
- İlgili: `TST-01` · B7 · T16

### ARC-03 K18 dosyaların %92'sinde çiğneniyor; 79 dosyanın kılavuzu yok
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:routes/api.php` (437 satırın büyük kısmı açıklama bloğu) · `backend:app/Providers/AppServiceProvider.php` (%47 yorum) · tam liste `evidence/commands/ARC-k18-guide-gaps.txt`
- Senaryo: K18 "kod yorumu kısa (1–3 satır), ayrıntı `docs/rehber/<aynı-yol>.md`" diyor. Ölçüm: üretim kodundaki 287 dosyanın 265'inde 3 satırdan uzun yorum bloğu var (toplam 675 blok, en uzunu 50 satır). Ters yönde: 362 kod dosyasının 79'unun kılavuzu yok; eksikler Faz 13–14'te yoğunlaşıyor (`Actions/Pricing` 5, `Actions/Account` 4, `Requests/Account` 4, `Notifications` 4, `Services/Payment` 5).
- Kanıt: `bash evidence/scripts/arc-k18-guide-gaps.sh` → `taranan kod dosyasi: 362 · kilavuzu OLMAYAN: 79` ve `uretim kodunda 3 satirdan uzun yorum blogu iceren dosya sayisi: 265 / 287`.
- Etki: Kural ile uygulama ters yönde ilerliyor: açıklama koda yazılıyor, kılavuz geride kalıyor. Aynı bilginin iki evi oluşuyor ve hangisinin güncel olduğu belirsizleşiyor. Okunabilirlik de düşüyor: `routes/api.php`'de 40 rota tanımı 300 satır açıklamanın arasında.
- Neden önemli (öğretici not): Yorum kodun **neden** öyle olduğunu söylemeli ve kodla birlikte eskir. Uzun bir yorum bloğu, yanındaki satır değiştiğinde güncellenmeyen ilk şeydir. Kuralın kendisi doğru; sorun, ihlalin ölçülmemesi.
- Öneri: 1) En ucuz: kuralı gevşetip gerçeği kabul et (ör. "en fazla 8 satır") ve bunu karar olarak yaz. 2) Sağlam: uzun blokları kılavuza taşı, `composer check`'e yorum bloğu uzunluğunu ölçen küçük bir betik ekle (mevcut `arc-k18-guide-gaps.sh` temel olabilir), kılavuzu olmayan yeni dosyada kapıyı düşür.
- Test önerisi: `composer check` adımı `k18:check`: yeni/değişen dosyada 3 satırdan uzun blok ya da eksik kılavuz varsa kırmızı.
- Efor: L
- İlgili: K18

### ARC-04 K55 "yerel disk kalır" geçerli görünüyor ama yayın planı S3 kuruyor
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `davetkart-docs/decisions/DECISION-INDEX.md:67` (K55, "geçerli · ⚠️") · `backend:config/davetkart.php:121` (`DAVETKART_MEDIA_DISK` varsayılanı `public`) · `backend:composer.json:15` (`league/flysystem-aws-s3-v3`)
- Senaryo: K55 medyanın yerel `public` diskinde kalacağını söylüyor; paket listesine S3 sürücüsü eklenmiş ve yayın planı S3 diskini kuruyor. Kararı geçersiz kılan bir K yok. Varsayılan hâlâ `public`: üretim `.env`'inde değişken unutulursa misafir fotoğrafları web kökünün altına, sunucunun kendi diskine yazılır.
- Kanıt: dosya okuması; S3 yolu koşturulmadı (AWS'ye istek yasak).
- Etki: Karar kaydına güvenen biri yanlış diski varsayar. Sessiz varsayılan, 5 GB/davetiye misafir kotasıyla (`SEC-08`) birleşince tek sunucunun diskini doldurabilir.
- Neden önemli (öğretici not): Proje başka yerde "bilinmeyen değer sessiz varsayılana düşmez" ilkesini uyguluyor (ödeme sürücüsü, K70). Aynı ilke depolama için de geçerli: üretimde hangi diskin kullanıldığı bir tercih değil bir **güvenlik ve maliyet** kararı.
- Öneri: K55'i "geçersiz kılındı → K146" yap ve yeni kararı yaz. `APP_ENV=production` iken `davetkart.media.disk === 'public'` ise açılışta uyarı logla (ya da `about` komutunda göster).
- Test önerisi: `production_refuses_the_public_media_disk`: üretim ortamı + `public` disk → yükleme 503 ya da açılış uyarısı.
- Efor: S
- İlgili: K55 · K80 · `OPS-04` (üretim şablonu: `DAVETKART_MEDIA_DISK=s3`)

### ARC-05 Eski `claude/…` yolları: backend'de 25 dosya; backend'in kendi `claude/` klasörü ikinci ev
- Seviye: 🟡 Orta
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:docs/03-MIMARI-PLAN.md:314` · `backend:docs/07-GELISTIRME-YOL-HARITASI.md:382,557` · `backend:docs/08-HATA-SOZLESMESI.md:300` · `backend:docs/09-TUM-FAZLAR-PLANI.md:888` · `backend:docs/11-PROJE-TARIHCESI-VE-IS-AKISLARI.md:17,2906,2918,2981` · `backend:claude/` (22 dosya)
- Senaryo: Doküman deposu 12 Kasım'da yeniden düzenlendi (`claude/PHP-LARAVEL-SETUP.md` → `context/…`, `claude/Notlar/` → `notes/`). Backend'deki 25 dosya hâlâ eski yolu gösteriyor. Ayrıca backend deposunun kendi `claude/` klasörü (EK-FAZ-5…9, `FAZ-10-PLANI.md`, üç gözden geçirme, test denetimi) taşınmadı: K49–K63 ve K72–K106'nın tek kaynağı orada.
- Kanıt: `grep -rlE "claude[/\\](PHP-LARAVEL-SETUP|Notlar|FAZ-|GOZDEN|TEST-DENETIMI|PROMPT)" backend --include=*.md --include=*.php | grep -v '^backend/claude/' | wc -l` → `25`.
- Etki: Yeni oturum açan bir asistan ya da insan, verilen yolda dosyayı bulamaz. Karar kaydının yarısı kod deposunda, yarısı doküman deposunda.
- Neden önemli (öğretici not): "Bir bilginin tek bir güncel evi olur" (`davetkart-docs/CLAUDE.md` §6). Taşıma yarım kaldığında iki ev de eksik olur.
- Öneri: `backend/claude/` içeriğini `davetkart-docs`'a taşı (`decisions/addenda/`, `phases/faz-05…10/`, `audits/2026-09-23-…`, `audits/2026-09-24-test-audit/`, `audits/2026-10-09-…`, `prompts/`); backend `docs/` içindeki 25 atfı yeni yollarla güncelle.
- Test önerisi: —
- Efor: M
- İlgili: `_restructure/REPORT.md` §4

### ARC-06 Üç hata kodu hiçbir yerde fırlatılmıyor
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `backend:app/Enums/ErrorCode.php:22` (`TOKEN_EXPIRED`) · `:29` (`INVITATION_LOCKED`) · `:49` (`SLUG_TAKEN`)
- Senaryo: Üç kod katalogda ve frontend çevirilerinde duruyor ama `app/` içinde kullanan yok. `TOKEN_EXPIRED` özellikle yanıltıcı: 31 günlük token `UNAUTHENTICATED` alıyor (sonda P70), yani frontend "oturumun süresi doldu" ile "hiç giriş yapmadın"ı ayıramıyor.
- Kanıt: `grep -rn "ErrorCode::InvitationLocked\|ErrorCode::SlugTaken\|ErrorCode::TokenExpired" app | grep -v Enums/ErrorCode.php | wc -l` → her biri `0`.
- Etki: Sözleşmede verilmiş ama tutulmayan söz (B4). Frontend'de ölü çeviri ve ölü dal.
- Neden önemli (öğretici not): Bir sözleşme, ne **olabileceğinin** listesidir; listede olup hiç olmayan şey, okuyanı var olmayan bir durumu ele almaya zorlar.
- Öneri: `SLUG_TAKEN` ve `INVITATION_LOCKED`'ı sil (K66: slug üretilmiyor). `TOKEN_EXPIRED` için karar ver: ya Sanctum'un süre kontrolünü bu koda bağla ya da sil.
- Test önerisi: `every_error_code_is_thrown_somewhere`: enum case'lerini `app/` içinde arayan mimari testi.
- Efor: S
- İlgili: R10 · B4

### ARC-07 Frontend'de `.gitattributes` yok; sözleşme dosyası CRLF
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: `frontend:` (kökte `.gitattributes` yok) · `frontend:src/contracts/error-codes.json` (170 CR + 170 LF) ↔ `backend:contracts/error-codes.json` (0 CR)
- Senaryo: Backend `* text=auto eol=lf` kullanıyor; frontend'de kural yok. İki depodaki sözleşme dosyası anlamsal olarak aynı ama bayt bayt farklı; "iki kopya aynı mı" kontrolü sha256 ile yapılırsa yanlış alarm verir. `davetkart-docs/CLAUDE.md` §7'deki "frontend'de `git add -A` yüzlerce dosyayı sürükler" tuzağının kökü de bu.
- Kanıt: `evidence/commands/FE-error-codes-compare.txt` → `bayt bayt aynı mı: false` · `normalize sonrası aynı mı: true`.
- Etki: Gürültülü diff'ler, yanlışlıkla commit'lenen satır sonu değişiklikleri.
- Neden önemli (öğretici not): Satır sonu bir **depo** ayarı olmalı, geliştiricinin makine ayarı değil. `.gitattributes` bunu depoya yazar.
- Öneri: Frontend köküne `* text=auto eol=lf` + ikili dosya kalıpları; ardından tek seferlik `git add --renormalize .` commit'i.
- Test önerisi: CI'da `git ls-files --eol | grep -c 'i/crlf'` → 0.
- Efor: S
- İlgili: R10 (Review §6.10)

### ARC-08 Dal hijyeni: 30+ dal, yazım hatalı adlar, etiket yok
- Seviye: 🟢 Düşük
- Kanıt türü: KOŞTURULDU
- Nerede: backend ve frontend depoları (`git branch -a`, `git tag`)
- Senaryo: Backend'de 20+, frontend'de 35+ dal var; birçoğu birleşmiş. Adlarda yazım hataları kalıcılaşmış (`faz15-desing`, `payment-servide`, `media-confugration`, `faz-12-shopier-not-right`). Hiç etiket yok; yayına çıkan commit `release-v1.0` dalıyla izleniyor. Backend `main` denetlenen dalın 4 commit gerisinde; frontend'de denetlenen dal `main`'deki `47aedc8` düzeltmesini içermiyor (`SEC-13`). `davetkart-backend-php-laravel.worktrees/` altında dört eski çalışma ağacı duruyor.
- Kanıt: `git -C <depo> branch -a -vv --sort=-committerdate` ve `git tag` (boş) çıktıları; `README.md` kapsam tablosu.
- Etki: "Hangi kod yayında, hangisi en yeni" sorusunun cevabı dal adlarından okunamıyor; bu denetimin başında yerel ağacın 60 commit geride olduğunun fark edilmemesi bunun sonucu.
- Neden önemli (öğretici not): Dal geçici bir çalışma alanıdır, etiket kalıcı bir işarettir. Sürümü dalla izlemek, dal ilerlediğinde "o gün ne yayınlandı" bilgisini kaybettirir.
- Öneri: Yayın commit'lerini etiketle (`v1.0.0`), birleşmiş dalları sil, tek bir entegrasyon dalı belirle ve yerel depoları ona göre güncel tut.
- Test önerisi: —
- Efor: M
- İlgili: R10 (git hijyeni)

### ARC-09 Checkout idempotent değil: her çağrı yeni `pending` sipariş açar
- Seviye: 🟢 Düşük
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:app/Actions/Payment/StartCheckoutAction.php:111-142,195-243`
- Senaryo: Aynı kullanıcı aynı davetiye ve plan için `POST /invitations/{id}/checkout`'u iki kez çağırırsa (çift tıklama, sekme yenileme) iki ayrı `pending` sipariş oluşur. Kodsuz checkout `throttle:gift-code` kovasına yazılmadığı için (`AppServiceProvider.php:326-328`) tek fren genel 60/dk tavanı.
- Kanıt: kod okuması; sonda P12 + P13a aynı kullanıcıya art arda iki `pending` sipariş açtı.
- Etki: Sipariş tablosunda gürültü; `orders:expire` temizliyor. Asıl önemi `SEC-01`'in zemini olması: açık siparişler birbirinden habersiz fiyatlanıyor.
- Neden önemli (öğretici not): Para başlatan bir uç **idempotent** olmalı: aynı niyet iki kez gönderildiğinde ikinci istek birincinin sonucunu döndürmeli. Bunun iki yaygın yolu var: istemcinin ürettiği `Idempotency-Key` başlığı ya da sunucunun "aynı (kullanıcı, kaynak, plan) için açık sipariş varsa onu döndür" kuralı.
- Öneri: Transaction içinde, kullanıcı satırı kilitliyken aynı (kullanıcı, davetiye, plan) için süresi dolmamış `pending` sipariş varsa onu döndür; yoksa aç.
- Test önerisi: `a_second_checkout_for_the_same_invitation_reuses_the_pending_order`: iki istek, tek satır. Öldürmesi gereken mutant: yeniden kullanma sorgusunu kaldırmak.
- Efor: M
- İlgili: `SEC-01` · M8

### ARC-10 `OptimizeUploadedImage` 664 satır, tek sınıfta dört sorumluluk
- Seviye: 💡 Öneri
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:app/Jobs/OptimizeUploadedImage.php` (664 satır; 301 kod, 264 yorum)
- Senaryo: Job; görüntüyü çözmeyi, EXIF yönünü okumayı, yeniden boyutlandırıp kodlamayı, bellek sınırını yönetmeyi ve eski dosyayı yenisiyle takas etmeyi tek sınıfta yapıyor. Gövdesi bu denetimde satır satır okunmadı; yalnızca ilgili satırlar tarandı. Davranışı canlı sondada doğrulandı (P54–P55: EXIF ve dosya sonuna eklenen PHP kuyruğu saklanan dosyada yok).
- Kanıt: `evidence/commands/ARC-largest-files.txt` (en büyük dosya) · `evidence/commands/SEC-api-probe.txt` P54–P55.
- Etki: Değiştirmesi en riskli dosya; mahremiyet (EXIF/GPS) ve disk (dosya takası) aynı yerde.
- Neden önemli (öğretici not): Tek Sorumluluk İlkesi "bir sınıfın değişmek için tek bir nedeni olsun" der. Burada dört neden var: görüntü kütüphanesi, mahremiyet kuralı, kalite hedefi, depolama.
- Öneri: `ImageDecoder`, `ExifOrientation`, `ImageEncoder`, `MediaFileSwap` gibi küçük sınıflara ayır; job yalnızca sırayı yönetsin.
- Test önerisi: Ayrılan her sınıf için birim testi; mevcut `OptimizeUploadedImageTest` uçtan uca kalır.
- Efor: M
- İlgili: —

## Tablolar

### En büyük 15 üretim dosyası (`evidence/commands/ARC-largest-files.txt`)

| Satır | Kod | Yorum % | Dosya |
|---|---|---|---|
| 664 | 301 | 39 | `app/Jobs/OptimizeUploadedImage.php` |
| 450 | 190 | 47 | `app/Providers/AppServiceProvider.php` |
| 437 | 332 | 15 | `routes/api.php` |
| 377 | 218 | 24 | `app/Services/Payment/ShopierGateway.php` |
| 333 | 169 | 35 | `app/Actions/Payment/StartCheckoutAction.php` |
| 327 | 148 | 43 | `config/davetkart.php` |
| 248 | 135 | 29 | `app/Exceptions/ApiExceptionRenderer.php` |
| 248 | 105 | 47 | `app/Models/Invitation.php` |
| 238 | 94 | 44 | `app/Enums/ErrorCode.php` |
| 238 | 102 | 44 | `app/Models/Order.php` |
| 235 | 166 | 13 | `config/session.php` |
| 212 | 92 | 41 | `app/Http/Requests/Media/MediaRequest.php` |
| 197 | 140 | 11 | `app/Actions/GiftCode/GiftCodeSpec.php` |
| 195 | 89 | 44 | `app/Services/Ai/GeminiProvider.php` |
| 186 | 153 | 5 | `config/database.php` |

Not: `routes/api.php` satırında "yorum %15" ölçümü `|` ile başlayan blok satırlarını kod sayıyor; gerçek oran çok daha yüksek.

### En çok değişen 15 dosya (`evidence/commands/ARC-churn.txt`, `git log origin/ccr-9a346997-bu6gve`)

| Commit | Dosya |
|---|---|
| 33 | `routes/api.php` |
| 22 | `docs/rehber/routes/api.md` |
| 20 | `config/davetkart.php` |
| 19 | `bootstrap/app.php` |
| 18 | `app/Providers/AppServiceProvider.php` |
| 15 | `docs/07-GELISTIRME-YOL-HARITASI.md` |
| 14 | `tests/Feature/PaywallTest.php` |
| 13 | `docs/09-TUM-FAZLAR-PLANI.md` |
| 12 | `docs/rehber/app/Providers/AppServiceProvider.md` |
| 12 | `docs/10-URETIM-ENV-SABLONU.md` |
| 12 | `app/Models/Order.php` |
| 12 | `.env.example` |
| 11 | `docs/rehber/tests/Feature/PaywallTest.md` |
| 11 | `docs/rehber/config/davetkart.md` |
| 11 | `contracts/error-codes.json` |

Yorum: `routes/api.php`, `config/davetkart.php` ve `AppServiceProvider` hem en büyük hem en çok değişen dosyalar. Bu üçü projenin "tanrı dosyaları" olma yolunda: her faz oraya bir şey ekliyor. Hız sınırlayıcıları ayrı bir sağlayıcıya (`RateLimitServiceProvider`), rotaları alan bazlı dosyalara bölmek bir sonraki fazdan önce yapılabilir.

### Karar örneklemi (R17)

Yöntem: ödeme/paywall, medya, hata sözleşmesi ve güvenlik kararlarının hepsi, geri kalanından örnekler. "K" = canlı sondada koşturuldu (`evidence/commands/SEC-api-probe*.txt`, P/Q numarasıyla), "O" = kod okuması.

| K# | Karar | Kodda nerede | Durum | Kanıt |
|---|---|---|---|---|
| K8 | `PaymentGateway` + `FakeGateway` | `app/Services/Payment/PaymentGateway.php`, `FakeGateway.php:31` | ✅ | O |
| K14/K77 | IP `hash_hmac` ile saklanır | `app/Actions/Rsvp/SubmitRsvpAction.php:83` | ✅ | K (P24) |
| K20 | Hata zarfı kod döner | `app/Exceptions/ApiExceptionRenderer.php:57-75` | ✅ | K (bütün sonda) |
| K28 | Kota aşımı 403 | `app/Actions/Rsvp/EnsureRsvpQuotaAction.php:61-63` | ✅ | K (P28) |
| K36 | Auth hız sınırı | `app/Providers/AppServiceProvider.php:380-389` | ✅ | K (P83) |
| K39 | `VARCHAR + CHECK` | migration'larda 30 CHECK | ✅ | K (grep) |
| K42/K99 | Tek sipariş tek davetiye yayınlar | `OrderEntitlementResolver.php:55-64`, `ClaimReleasedOrderAction.php:45` | ✅ | O |
| K43 | Kota yayınlananı sayar | K99 ile cevaplandı; indeksteki ⚠️ artık geçersiz | ✅ | O |
| K45 | Cache Resource çıktısını saklar | `PublicInvitationController.php:38-50` | ✅ | O |
| K54 | `media.disk` kolonda | `StoreUploadedMediaAction.php:91` | ✅ | K (P56) |
| K55 | Yerel `public` disk | `config/davetkart.php:121` | ⚠️ `ARC-04` | O |
| K58/K59 | Medya kimlikle iliştirilir, geçersizi düşer | `ResolveGuestMediaAction.php:49-66` | ✅ | O |
| K64/K65 | İki checkout ucu; webhook `public` altında | `routes/api.php:198,204,378` | ✅ | K (P12, P13a) |
| K67 | Ödeme yayınlamaz | `HandlePaymentCallbackAction.php:114-160` (yayın yok) | ✅ backend | K (P14) |
| K68 | "Zaten yayında" 409 | `PublishInvitationAction.php:68-70` | ✅ | K (P18) |
| K69 | İmza hatası 404 | `FakeGateway.php:139-141` | ✅ | K (P19) |
| K70 | Sürücü sessiz varsayılana düşmez | `AppServiceProvider.php:81-90` | ✅ | O |
| K82/K83 | 3 günlük serbest bırakma; en ucuz yeten sipariş | `DeleteInvitationAction.php:51-68`, `ClaimReleasedOrderAction.php:87-104` | ✅ (yan etkisi `SEC-02`) | K (P47) |
| K85/K86 | Güvenlik başlıkları, CORS | `SecurityHeaders.php:40-77`, `config/cors.php:45-84` | ✅ | K (P57–P61) |
| K88 | Yayındaki davetiyede modül açma 402 | `UpdateInvitationAction.php:62-64,91-110` | ✅ | K (P15) |
| K89 | `Expired → Paid` | `OrderStatus.php:118` | ✅ | K (P23) |
| K90 | Token 30 gün | `config/sanctum.php:66` | ✅ | K (P70) |
| K91/K92 | Bozuk girdi 400; `integer:strict` | `RejectMalformedInput.php:36-38` | ✅ | K (P31–P34) |
| K93 | `Retry-After` başlığı | `ApiExceptionRenderer.php:96` | ✅ | K (P43, P83) |
| K97 | Hesap silme anonimleştirir | `DeleteAccountAction.php:44-84` | ✅ | K (P81) |
| K98 | Saklama süreleri | `app/Console/Commands/PurgeExpiredData.php` | ❓ okunmadı | — |
| K100 | İade yayından kaldırır | `HandlePaymentCallbackAction.php:153-160` | ✅ | O |
| K101 | Misafir düzenleme kodu | `UpdateRsvpAction.php:56-60` | ✅ | K (P25, P26) |
| K102 | Elit'te imza yok; videolu temalar Gold | `ResolveBrandingAction.php:40-45`, `config/davetkart.php:65-103` | ✅ | K (P15, P16) |
| K103 | Zamanlanmış işler Sentry'ye bağlı | `routes/console.php:48,65,86,98` | ✅ | O |
| K104 | Hız sınırları, IPv6 /64 | `config/davetkart.php:114-132`, `IpBucket.php:39` | ✅ (yan etkisi `SEC-06`) | K (P85) |
| K105 | IBAN mod-97 | `AppServiceProvider.php:147-150` | ✅ | K (P36) |
| K107–K113 | Hediye = sipariş; hash'li kod; kişi başı tek kullanım | `StartCheckoutAction.php:125-139,251-285`, `GiftCodeFormat.php:42`, `QuoteGiftCodeAction.php:39-57` | ✅ | K (P38–P43) |
| K111 | Kod satırı kilitliyken kontrol | `ReserveGiftCodeAction.php:43-46` | ✅ kod; yarış koşturulmadı | O |
| K115 | Kod CSV'si özel diskte | `GenerateGiftCodeBatchAction.php:28,56` | ✅ | O |
| K117/K127 | OSB varsayılan; callback ayrı tip | `config/payment.php:44`, `ShopierGateway.php:156-192` | ✅ (yan etkisi `SEC-03`) | O |
| K121–K124 | `platform_order_id = orders.id`; 303; sır yoksa 503; tutar biçimi | `ShopierGateway.php:120,85-100`, `ShopierCallbackController.php:63-71`, `ShopierAmount.php:27` | ✅ | O |
| K126 | Bildirim tutarı siparişle eşleşmeli | `HandlePaymentCallbackAction.php:101-112,170-178` | ✅ | O |
| K128–K136 | Fiyat backend'de; ilk yayın %60; indirimler toplanmaz; ödeme yöntemleri | `QuotePriceAction.php:46-153`, `PaymentMethods.php:42-69` | ✅ (K131'in yan etkisi `SEC-01`) | K (P12, P13) |
| K137–K139 | Yanmış hak damgası; iade talebi hakkı dondurur | `Order.php:138-141`, `RefundEligibility.php:33-43` | ✅ (boşluk `SEC-02`) | K (P44, P47, P48) |
| K142–K144 | Parola değişince oturumlar kapanır; e-posta değişikliği sızdırmaz | `ChangePasswordAction.php:33-42`, `ConfirmEmailChangeAction.php:42-66` | ✅ | K (Q01–Q08) |

İndeksteki ⚠️ satırların kod etkisi: K11 (yalnızca durum metni eskimiş), K43 (K99 kapattı), K67 (backend uyuyor; frontend ödeme dönüşünde kendiliğinden yayınlıyor: `FE-58`), K94 ve K125 (Shopier elle doğrulaması bekliyor: kod var, canlı doğrulama yok; `SEC-03`, `SEC-10`), K55 (`ARC-04`). Numara çakışması kodu etkilemiyor; tek gerçek risk `ARC-01`.

## Regresyon

| # | Kaynak | Bulgu | Durum | Kanıt türü | Kanıt |
|---|---|---|---|---|---|
| R7 | Review §5.1 | 4xx iş istisnaları Sentry'ye gidiyor | ✅ kapandı | KOD OKUMASI | `bootstrap/app.php:56-58` (`dontReportWhen`, `status() < 500`). Sentry'ye istek atılmadı. |
| R8 | Review §5.2 (sunucu tarafı) | Fiyat sayfası vaatleri ↔ sunucu kuralları | ✅ kapandı (sunucu) | KOŞTURULDU | Elit'te imza yok: `ResolveBrandingAction.php:40-45`, P16 `showBranding=true` (Standart). Premium tema Gold: P15. Frontend tarafı `FE-05` (kopya kural) ve `FE-52` (SSS'deki "yayın süresi"). |
| R10 | Review §6.1–6.10 (ölü kod, git hijyeni, CRLF) | Ölü dosya/config, git hijyeni, `.gitattributes` | 🟡 kısmen | KOŞTURULDU | `payment.webhook.tolerance_seconds` silinmiş (grep boş); `SubscriptionTier::label()` artık kullanılıyor (`ShopierGateway.php:128`). Açık kalan: `ARC-06`, `ARC-07`, `ARC-08`. |
| R13 | Faz 7 açık soru | Paket kaç yayın açar (`publish_quota`, K43) | ✅ kapandı | KOD OKUMASI | K99: paket bağsız tekil sipariş, ilk yayında bağlanır (`ClaimReleasedOrderAction.php:45`); `publish_quota` kolonu yok ve gerekmiyor. |
| R15 | Faz 14 (tasarım) | Plan hakkı sayısı, hak iptali, e-posta değişikliği | 🟡 kısmen | KOŞTURULDU | Tasarım tutarlı (P44, P48, Q01–Q08). Boşluk: serbest kalan kullanılmış hak iade edilebiliyor (`SEC-02`, P47). |
| R16 | Fiyat kararı (backend) | Fiyat yalnızca backend'den; indirim; ödeme yöntemi anahtarı | 🟡 kısmen | KOŞTURULDU | Fiyat sunucuda (P12), indirimler toplanmıyor (`QuotePriceAction.php:146-153`), yöntem tek ayarla kapanıyor (`PaymentMethods.php:64-69`). Boşluk: ilk yayın indirimi birden çok siparişe uygulanıyor (`SEC-01`, P13). |
| R17 | `DECISION-INDEX.md` | "Geçerli" kararlar kodda mı; ⚠️ çakışmalar | 🟡 kısmen | KOŞTURULDU | Yukarıdaki tablo: örneklenen 60+ kararın hepsi kodda; K98 okunmadı; indeks K128–K145'i içermiyor (`ARC-01`). |

## Kullanılan araçlar ve skill'ler / kullanılamayanlar

- Kullanılan: `superpowers:writing-plans` (plan), `superpowers:dispatching-parallel-agents` (ilk dağıtım; ajanlar sınıra takıldı). Kod okuması `awk` ile yorum ayıklanarak, taramalar `grep` ile yapıldı.
- Kullanılamayan: **Context7** (bağlı değil). Laravel 13 / Sanctum API'lerinin güncel dokümanla karşılaştırması **yapılmadı**; kullanılan API'ler (`Application::configure`, `RateLimiter::for`, `Schedule::command(...)->onOneServer()`, `Model::shouldBeStrict`, `Config::integer/string/array`) çalışan test paketi (1055/1056) ve PHPStan (0 hata) ile dolaylı olarak doğrulandı; "deprecated değil" iddiası **doğrulanamadı**.
- `superpowers:systematic-debugging`, `verification-before-completion`, `mattpocock-skills:codebase-design`: token tasarrufu için ayrıca çağrılmadı; doğrulama adımı (her `KOŞTURULDU` satırının kanıt dosyası var mı) elle yapıldı.

## Koşturulan komutlar

| Dosya | İçerik |
|---|---|
| `evidence/commands/ARC-largest-files.txt` | `bash evidence/scripts/arc-largest-files.sh` |
| `evidence/commands/ARC-churn.txt` | `bash evidence/scripts/arc-churn.sh` |
| `evidence/commands/ARC-k18-guide-gaps.txt` | `bash evidence/scripts/arc-k18-guide-gaps.sh` |
| `evidence/commands/FE-error-codes-compare.txt` | `node evidence/scripts/fe-error-codes-compare.mjs` |
| `evidence/commands/SEC-api-probe.txt`, `SEC-api-probe-2.txt` | canlı sonda (P ve Q numaraları) |
| (satır içi) | K numarası sayımı, CHECK/UNIQUE/index taraması, `float\|decimal` taraması, ölü hata kodu sayımı: komutlar ilgili bulgunun "Kanıt" satırında |

## İsmail'e sorular

1. K55'in yerine geçecek kararı (üretimde medya S3'te) sen mi yazacaksın? Numara önerisi: K146.
2. K18'i gevşetmek mi (gerçeği kabul), yoksa uygulatmak mı (kapıya ölçüm) istiyorsun?
3. Faz 16–17'de hangi şablonun Gold olduğu kararı kimin ve hangi ölçütle verildi? (K102 "videolu temalar" diyordu; Faz 17'nin dokuz şablonunun hepsi videolu mu?)
