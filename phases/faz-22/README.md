# Faz 22 — Ertelenmiş düşük bulgular ve açık kararlar (tek sayfa)

> **Hazırlanma:** 26 Kasım 2026 · **Kaynak:** `AUD-2026-11-12` ([`REPORT.md`](../../audits/2026-11-12-full-system-audit/REPORT.md),
> [`findings/`](../../audits/2026-11-12-full-system-audit/findings/)) düşük (🟢) ve öneri (💡) bulguları + `AUD-2026-11-26`
> ([`REPORT.md`](../../audits/2026-11-26-post-faz-19-scan/REPORT.md) §4b) ikinci taramanın karar soruları.
> **Biçim:** paralel hat yok; maddeler §1'deki sırayla, **tek oturumda bir madde** koşulur. Her maddenin prompt'u bu sayfada (§4).
> **Önceki faz:** [`faz-20/`](../faz-20/README.md) (Faz 21 tanımlı değil).

## 0. Kapsam

17 madde. `AUD-2026-11-12`'nin 27 düşük/öneri bulgusundan 26 Kasım'da koda bakılarak **kapanmış** bulunanlar Faz 22'ye girmedi:
`ARC-09` (Faz 18.3), `SEC-14` (`express`/`dotenv` yok, derleme araçları `devDependencies`'te), `FE-05` (`contracts/plan-rules.json`
+ `verify:plans`, Faz 18.1), `FE-09` (en büyük video 2,3 MB), `FE-56` (`ThreeStage` `still`). Faz 20'de kapananlar: `OPS-06`,
`FE-06`, `FE-55`, `FE-57`.

## 1. Takip

Sıra: önce güvenlik ve ürün kararları, sonra işletim, temizlik ve test altyapısı; **depoların tamamına dokunan `ARC-07` en sonda.**
"§A" sütununda ✅ olan maddede önce senin cevapların gerekir (§4'te o maddenin tablosu); boş satırda ajan varsayılanı uygular ve
K kaydında "varsayılan (İsmail cevaplamadı)" yazar.

| Sıra | Bulgu | Önem | Konu | Efor | §A | Depolar | Dal (kod) | K | Durum |
|---|---|---|---|---|---|---|---|---|---|
| 22.1 | `SEC-16` | 🟢 | Hesap bazlı (IP'den bağımsız) giriş freni | S | ✅ | backend · docs | `fix/<tarih>-sec-16-account-login-bucket` | | bekliyor |
| 22.2 | `SEC-15` | 🟢 | Kayıt ucu adresin kayıtlı olduğunu söylüyor | S/M | ✅ | backend · frontend · docs | `fix/<tarih>-sec-15-register-enumeration` | | bekliyor |
| 22.3 | `FE-58` | 🟢 | Ödeme dönüşünde davetiye kullanıcıya sorulmadan yayınlanıyor (K67) | S | ✅ | frontend · docs | `fix/<tarih>-fe-58-publish-after-payment` | | bekliyor |
| 22.4 | `OPS-08` | 🟢 | Günlüklerde istek kimliği yok | S | ✅ | backend · (frontend) · docs | `fix/<tarih>-ops-08-request-id` | | bekliyor |
| 22.5 | `OPS-07` | 🟢 | PHP-FPM havuzu ve OPcache ayarı depoda yok | S | ✅ | backend (`deploy/`) · docs | `fix/<tarih>-ops-07-fpm-opcache` | | bekliyor |
| 22.6 | `ARC-06` | 🟢 | Hiç fırlatılmayan 3 hata kodu | S | ✅ | backend · frontend · docs | `fix/<tarih>-arc-06-unused-error-codes` | | bekliyor |
| 22.7 | `FE-08` | 🟢 | Konum araması: backend ucu yok, bayrakla kapalı kod | S | ✅ | frontend · docs | `fix/<tarih>-fe-08-places-search` | | bekliyor |
| 22.8 | `FE-03` | 🟢 | TypeScript `strict` kapalı (bugün 20 hata) | S | — | frontend · docs | `fix/<tarih>-fe-03-strict` | | bekliyor |
| 22.9 | `TST-05` | 🟢 | Node sürümü sabit değil (CI 22, yerel 24) | S | ✅ | frontend · docs | `fix/<tarih>-tst-05-node-version` | | bekliyor |
| 22.10 | `TST-06` | 💡 | Backend testleri paralel koşmuyor | M | — | backend · docs | `fix/<tarih>-tst-06-parallel-tests` | | bekliyor |
| 22.11 | `TST-03` | 🟢 | Satır kapsamı ölçülmüyor; eşik yok | S | ✅ | backend · docs | `fix/<tarih>-tst-03-coverage` | | bekliyor |
| 22.12 | `ARC-10` | 💡 | `OptimizeUploadedImage` 664 satır, dört sorumluluk | M | — | backend · docs | `fix/<tarih>-arc-10-image-pipeline` | | bekliyor |
| 22.13 | `SEC-18` | 💡 | Token `localStorage`'da; `httpOnly` çerez | L | ✅ | docs (plan) · (backend · frontend) | `docs/<tarih>-sec-18-cookie-auth-plan` | | bekliyor |
| 22.14 | `OPS-09` | 💡 | Yatay ölçek eşikleri yazılı değil | S | — | docs | `docs/<tarih>-ops-09-scale-thresholds` | — | bekliyor |
| 22.15 | `SEC-17` | 🟢 | Docs klasöründe git dışı 148 MB eski kod arşivi (`.env` içerenler) | S | ✅ | yerel disk · docs | `docs/<tarih>-sec-17-local-archives` | — | bekliyor |
| 22.16 | `ARC-08` | 🟢 | Dal hijyeni, sürüm etiketi yok, eski worktree'ler | M | ✅ | üç depo | — (dal/etiket işi) | | bekliyor |
| 22.17 | `ARC-07` | 🟢 | Frontend'de `.gitattributes` yok (CRLF/LF) | S | ✅ | frontend · docs | `fix/<tarih>-arc-07-gitattributes` | | bekliyor |

Durum değerleri: `bekliyor` → `kod ✅` → `birleşti`. Docs kaydı her maddede bu tabloya, [`CHANGELOG.md`](../../CHANGELOG.md)'ye ve K varsa
[`DECISION-INDEX.md`](../../decisions/DECISION-INDEX.md) + `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-22.md`'ye işlenir (ilk K'yı veren
madde ek dosyayı açar). Resmî faz kaydı backend `docs/rehber/fazlar/FAZ-22.md` (ilk backend maddesi açar).

## 2. Genel §A (bir kez, ilk prompt'tan önce)

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| G1 | Commit'leri kim atar? | **Ajan** atar, Claude etiketi/trailer yok, push yok (Faz 20'deki uygulama). "Ben" yazarsan ajan `phases/faz-22/FAZ-22-<sıra>-COMMIT-KOMUTLARI.md` hazırlar ve git'e yazmaz | |
| G2 | Entegrasyon dallarının tabanı? | Backend ve frontend'de en yeni birleşik dal (bugün `faz-20-critical-fixes`). Ajan `git branch --sort=-committerdate` ile bulur; birden fazla aday varsa **sorar** | |
| G3 | Entegrasyon dalı adı | Backend ve frontend `faz-22-backlog`; docs `docs/<ilk maddenin tarihi>-faz-22-backlog` | |

## 3. Ortak çalışma biçimi (her prompt bunu okutur)

Prompt'lar bu bölüme atıf yapar; ajan önce bunu okur. Bağlayıcıdır.

1. **Önce oku:** `davetkart-docs\CLAUDE.md` · `context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `decisions\DECISION-INDEX.md`
   (sıradaki boş K başlıkta; 26 Kasım'da K265) · bu sayfa (§1, §2 ve kendi maddesi) · bulgunun tam metni (`findings/` ya da
   `AUD-2026-11-26` raporu) · dokunacağın dosyaların `docs/rehber/<aynı-yol>.md` kılavuzları.
2. **Ortamı eşitle (Faz 20 dersi):** backend `composer sync` (bağımlılık + göç); frontend Vite **kapalıyken** `npm ci` (Vite açıksa
   `npm install`, `npm ci` `EPERM` ile `node_modules`'ü yarım bırakır). `php artisan migrate:status --pending` boş, `composer install
   --dry-run` "Nothing to install" olmalı.
3. **Dallar:** §2 G2/G3'e göre entegrasyon dalı yoksa açılır; madde dalı §1'deki addır (`<tarih>` = `YYYY-MM-DD`), entegrasyon dalından
   açılır ve `--no-ff` ile birleşir (`Merge 22.<n> (<ID>) into faz-22-backlog`). Tek madde = tek dal; başka maddeye ait sorunu
   düzeltme, raporda "gördüm, dokunmadım" altında yaz.
4. **Durmadan uygula;** yalnızca maddenin "Dur ve sor" koşullarında ya da veri silme/geri dönüşsüz adımda dur. Proje talimatındaki
   "her dosyadan sonra dur" kuralı bu fazda askıda; açıklama yükümlülüğü sürüyor (kılavuzlar + rapor).
5. **Test önce (TDD):** davranış değişikliğinde önce kırmızı test, sonra kod; her yeni test için en az bir mutantla testin gerçekten
   koruduğunu göster (kodu boz → kırmızı → geri al).
6. **Kalite kapısı:** backend'e dokunduysan en sonda `composer check` (Windows'ta PHPStan için `PHPSTAN_TURBO=0`) **ve**
   `composer audit`; frontend'e dokunduysan `npm run check`. Kullanıcı akışına dokunan maddede `npm run e2e` (ayrı veritabanı
   `davetkart_e2e`, portlar 8020/4180; dev sunucularına dokunmaz).
7. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma; koşmadıysa "koşmadı" ve nedeni.
8. **K18:** kod yorumu 1–3 satır; ayrıntı kendi deposunda `docs/rehber/<aynı-yol>.md`. Backend'de `php artisan k18:check`
   değişen her dosyayı **tamamen** ölçer: dokunduğun dosyadaki eski uzun yorum blokları da kısalıp kılavuza taşınır.
9. **Sözleşmeler:** hata kodu değişirse `php artisan errors:export` + frontend `src/contracts/error-codes.json` kopyası + tr/en
   çevirisi aynı dalda (`verify:errors`). Frontend'de yeni Türkçe metin yalnızca `t()` ile (`verify:i18n` dosya dosya sayar).
   Frontend dosyaları CRLF'dir: CRLF'yi koru (Python ile `rb`/`wb` ya da Edit aracı; PowerShell 5.1 `Get-Content | Set-Content`
   UTF-8'i bozar).
10. **Yasaklar:** canlı sisteme istek (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API) yok; hiçbir dosyaya sır yazma;
    frontend'de `git add -A` yok, dosyalar tek tek. Sunucuda yapılacak adımları komut olarak yaz, koşma.
11. **Commit:** §2 G1'e göre. Mesaj İngilizce: kod `22.<n> - <tür>(<alan>): <Fiil> ...`; docs `docs(<alan>): <Fiil> ...`.
12. **Kayıt:** §1 tablosu (durum, K, dal) · `CHANGELOG.md` satırı · K varsa EK-FAZ-22 + `DECISION-INDEX.md`
    (`python -I _restructure/build_decision_index.py --check` temiz) · backend `docs/rehber/fazlar/FAZ-22.md` bölümü
    (Sorun · Karar · Değişen dosyalar · Testler ve mutantlar · B7 tablosu · Elle doğrulama · Gördüm, dokunmadım).
13. **Rapor (en sonda, tek mesaj, Türkçe):** ne değişti, kapıların çıktıları, mutantlar, koşmayanlar, İsmail'e kalan adımlar.

## 4. Prompt'lar

Kullanım: maddenin §A tablosunu doldur (boş = varsayılan), sonra o maddenin kutusundaki metni yeni bir Claude Code oturumuna
(Windows, `D:\Projects\davetkart`) yapıştır.

### 22.1 — `SEC-16`: hesap bazlı giriş freni

Bugün `AppServiceProvider::authLimits()` iki kova: e-posta + IP başına 5/dk, IP başına 20/dk. Çok IP'den tek hesaba deneme hiçbir
kovada birikmez.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | E-posta başına (IP'den bağımsız) sınır | Saatte 30 deneme | |
| 2 | Aşılınca | 429 `RATE_LIMITED` (`retryAfter` ile); hesap kilitlenmez (kilit, saldırganın sahibi dışarıda bırakmasına araç olur) | |
| 3 | Hesap sahibine "şüpheli giriş denemeleri" postası | Evet, kova ilk dolduğunda, saatte en çok 1 (kuyrukta); postada IP yok | |
| 4 | Kovaya sayılan denemeler | Yalnızca **başarısız** girişler (doğru parolayla giren sahip kendi kovasını doldurmaz) | |

```text
DavetKart Faz 22.1 — SEC-16 (hesap bazlı giriş freni). Önce davetkart-docs\phases\faz-22\README.md §3'ü (ortak çalışma
biçimi) ve §2'yi oku ve uygula; §1 tablosundaki 22.1 satırı ve §4'teki 22.1 §A cevapları bu işin kararlarıdır. Bulgunun tam
metni: davetkart-docs\audits\2026-11-12-full-system-audit\findings\02-security.md "SEC-16".

Yapılacaklar:
1. Önce test (tests/Feature içinde mevcut auth hız sınırı testlerinin yanına): aynı e-postaya farklı IP'lerden (REMOTE_ADDR
   değiştirerek) §A-1 sınırının bir fazlası kadar başarısız deneme → sonuncusu 429 RATE_LIMITED; başka e-postaya aynı IP'lerden
   deneme etkilenmez; §A-4'e göre doğru parolayla giriş kovayı doldurmaz (bunun için sayaç başarısız girişte elle artırılır;
   Limit::by tek başına başarılı isteği de sayar).
2. authLimits()'e üçüncü kova ya da LoginAction'da başarısızlıkta artan ayrı RateLimiter anahtarı (EmailNormalizer ile normalize
   e-posta; kişisel veri anahtarı olarak hash'lenir — IpHasher deseni). Mevcut iki kova ve sırası değişmez.
3. §A-3 "evet" ise kuyruklu bildirim (mevcut Notification desenleri, MAIL_MAILER=log yerelde), saatte en çok 1; şablon tr.
4. Kılavuzlar: AppServiceProvider.md (hız sınırı bölümü), yeni sınıfların .md'leri, docs/08 hata sözleşmesi gerekirse.
5. K kaydı: sınır, sayılan denemeler, bildirim (sıradaki boş K).
Dur ve sor: mevcut bir test kova sırasına ya da sayısına bağlıysa ve değişmesi gerekiyorsa.
```

### 22.2 — `SEC-15`: kayıt ucu adresin kayıtlı olduğunu söylüyor

Var olan adresle kayıt `422 REGISTRATION_FAILED`, yeni adresle 201 (`RegisterUserAction`, `UniqueConstraintViolationException`).
Kapatmanın tek tam yolu kaydı "postanızı kontrol edin" akışına çevirmektir; bu K11'i (kayıt `{user, token}` döner ve oturum açar)
değiştirir.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Yol | **B:** sözleşme aynı kalır; riski kabul et, kayıt ucuna e-posta + IP kovası ekle, 201 ve 422 yanıt sürelerini eşitle, kararı K'ye yaz | |
| 2 | A seçilirse (tam kapatma) | Kayıt her zaman `202 {status: "check_email"}` döner, oturum açmaz; adres yeniyse doğrulama postası, kayıtlıysa "biri bu adresle kayıt denedi, siz miydiniz? Giriş / parola sıfırlama" postası; ilk giriş doğrulamadan sonra. Frontend kayıt sayfası "postanızı kontrol edin" ekranına geçer; e2e `register()` akışı güncellenir | |

```text
DavetKart Faz 22.2 — SEC-15 (kayıt ucu adres sayımı). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula;
22.2 §A cevapları kararlardır. Tam metin: findings\02-security.md "SEC-15"; ilgili kararlar K11 (auth yanıtı zarfsız {user, token}),
K191 (e-posta doğrulama), A1–A7 (auth uçlarında unique/exists yok, kısa devre yok).

§A-1 = B (varsayılan) ise:
1. Önce testler: kayıt ucuna e-posta+IP ve IP kovası (mevcut 'auth' limiter'ıyla aynı desen, sayılar K'de); var olan adresle
   kayıt denemesi kovaya sayılır.
2. Yanıt süresi: var olan adreste de parola hash'i hesaplanır (A3 ruhu) — RegisterUserAction'da çakışma yolunda Hash::make
   atlanmıyor mu kontrol et; atlanıyorsa eşitle ve bunu ölçen bir test yerine kılavuzda gerekçeyle yaz (zaman testi kırılgan).
3. K: "SEC-15 kabul edilen risk: kayıt ucu kayıtlı adresi 422 ile söyler; frenler: …; tam kapatma K11'i değiştirir".
§A-1 = A ise:
1. Kontrat değişikliği: backend RegisterController/Action → 202 {status:"check_email"} (zarf istisnası C2'ye göre ad ad tanımlı:
   docs/08 ve contracts güncellenir), oturum açılmaz; kayıtlı adrese "kayıt denemesi" postası (kuyrukta, hız sınırlı).
2. Frontend: RegisterPage ve services/auth.ts register(); "postanızı kontrol edin" ekranı t() ile; verify:endpoints/verify:state
   güncellenir; e2e/support/flows.ts register() doğrulama bağlantısından sonra giriş yapar; npm run e2e yeşil.
3. Eski davranışı kilitleyen testler bilinçli güncellenir; her değişiklik raporda listelenir.
Dur ve sor: A seçildiyse ve mevcut kullanıcı akışında (ödeme dönüşü, sihirbaz) kayıttan hemen sonra oturum varsayan bir yer
bulursan.
```

### 22.3 — `FE-58`: ödeme dönüşünde onaysız yayın

`useAutoPublish.ts`: sipariş `paid` ve davetiyeye bağlıysa dönüş sayfası düğmesiz `POST /invitations/{id}/publish` atar. K67 "ödeme
yayınlamaz; yayın ayrı bir kullanıcı eylemidir" der (⚠️ çelişki sorusu açık).

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Davranış | **Otomatik yayın kalır** (kullanıcı ödemeye zaten "Yayınla"dan geldi). K67 yeni K ile daraltılır: "ödeme **sunucuda** yayınlamaz; frontend, yayın niyetiyle başlayan ödemenin dönüşünde yayınlar" | |
| 2 | Otomatik değilse | Dönüş sayfasında "Şimdi yayınla" düğmesi; ödeme alındı, davetiye taslakta kalır | |

```text
DavetKart Faz 22.3 — FE-58 (ödeme dönüşünde yayın). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula;
22.3 §A cevapları kararlardır. Tam metin: findings\04-frontend-e2e.md "FE-58"; K67 ve EK-FAZ-12 §F-7.

1. Seçilen davranışı verify:payment'te kilitle (önce kırmızı): §A-1 otomatik → "davetiyeye bağlı ödenmiş sipariş dönüşte TEK
   yayın isteği üretir, paket (davetiyesiz) siparişi üretmez, tekrar ziyaret ikinci istek üretmez"; düğme seçildiyse → "istek
   yalnızca düğmeyle gider".
2. Otomatik kalıyorsa kod değişmeyebilir; yalnızca test + K. Düğme seçildiyse PaymentReturnPage + useAutoPublish, metinler t().
3. K: K67'nin durumuna "daraltıldı → K<yeni>" yaz (K67 silinmez); EK-FAZ-12 §F-7 sorusuna bağlantı.
4. npm run check ve npm run e2e (yayın yolculuğu ödeme dönüşünden geçiyor).
```

### 22.4 — `OPS-08`: istek kimliği

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Hata zarfına `requestId` | Hayır (sözleşme aynı kalır); yalnızca `X-Request-Id` yanıt başlığı. Destek için frontend hata bildiriminde göstermek ayrı iş | |
| 2 | Gelen `X-Request-Id` başlığına güvenilsin mi? | Yalnızca biçimi geçerliyse (ULID/UUID, ≤64 karakter); değilse yenisi üretilir | |

```text
DavetKart Faz 22.4 — OPS-08 (istek kimliği). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula; 22.4 §A
cevapları kararlardır. Tam metin: findings\05-operations.md "OPS-08".

1. Önce test (HardeningTest ya da yeni RequestIdTest): her API yanıtında X-Request-Id var; geçerli gelen kimlik aynen döner;
   geçersiz/uzun gelen kimlik yenisiyle değişir; aynı istekte yazılan log satırları request_id taşır (Log::spy ya da
   Context::get); kuyruğa giden iş aynı kimliği taşır (Laravel Context işlerle taşınır — doğrula).
2. Ara katman (app/Http/Middleware, bootstrap/app.php'de global ve EN BAŞTA, M1 kuralı: yalnızca Accept ezilir) →
   Illuminate\Support\Facades\Context::add('request_id', …); yanıt başlığı. Log biçiminde context görünür mü kontrol et.
3. deploy/nginx'te $request_id ile başlık geçirme önerisi kılavuza (sunucu adımı, koşma).
4. Kılavuzlar + K (başlık adı, biçim, güven kuralı).
```

### 22.5 — `OPS-07`: PHP-FPM havuzu ve OPcache

Sunucu 2 GB; kuyruk işçisi 768 MB'a, her FPM süreci 256 MB'a kadar. Havuz dosyası depoda yok. K264'ten beri deploy bakım kipinde ve
FPM'i `reload` ediyor; bu, `opcache.validate_timestamps=0`'ı güvenli kılar.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | `pm.max_children` | 4 (`pm = dynamic`, `start_servers 2`, `min_spare 1`, `max_spare 3`, `max_requests 500`) | |
| 2 | OPcache | `memory_consumption=128`, `max_accelerated_files=20000`, `validate_timestamps=0` (deploy'da reload şart; `deploy.md`'ye yaz) | |

```text
DavetKart Faz 22.5 — OPS-07 (FPM havuzu, OPcache, bellek bütçesi). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku
ve uygula; 22.5 §A cevapları kararlardır. Tam metin: findings\05-operations.md "OPS-07". Sunucuya istek YOK.

1. deploy/php-fpm/davetkart.conf (havuz: kullanıcı www-data, socket deploy/nginx ile aynı, §A-1 sayıları, slowlog, request_terminate_timeout
   = nginx fastcgi_read_timeout ile uyumlu) ve deploy/php/davetkart.ini'ye §A-2 OPcache satırları.
2. Kılavuz docs/rehber/deploy/php-fpm/davetkart.md: bellek tablosu (FPM 4×256, kuyruk 768, PostgreSQL shared_buffers önerisi,
   işletim sistemi payı = 2048 MB içinde), kurulum komutları (cp → php-fpm8.5 -t → systemctl reload) ve geri alma. deploy.md'ye
   "validate_timestamps=0: reload'suz kod değişmez" notu.
3. Yerel doğrulama: Herd'in php-cgi/php-fpm ile `-t` sözdizimi denemesi mümkünse koş, değilse "koşmadı".
4. İsmail'e kalan sunucu adımları raporda numaralı liste.
```

### 22.6 — `ARC-06`: kullanılmayan hata kodları

`TOKEN_EXPIRED`, `INVITATION_LOCKED`, `SLUG_TAKEN` katalogda ve çevirilerde var, `app/` içinde fırlatan yok. Faz 20.7'den beri
frontend 401'de "Oturumunuz sona erdi" diyor; `TOKEN_EXPIRED` ayrımına gerek kalmadı.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Üç kod | Üçü de silinir (`SLUG_TAKEN`, K66: slug üretilmiyor) | |

```text
DavetKart Faz 22.6 — ARC-06 (kullanılmayan hata kodları). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula;
22.6 §A cevabı karardır. Tam metin: findings\01-architecture.md "ARC-06".

1. Önce kanıt: grep ile üç kodun backend app/ ve frontend src/ kullanımını göster (çeviri dosyaları hariç 0 olmalı).
2. app/Enums/ErrorCode.php'den case'ler ve status()/params eşlemeleri; php artisan errors:export → contracts/error-codes.json;
   frontend src/contracts kopyası ve tr/en errors.json anahtarları; docs/08 hata sözleşmesi tablosu.
3. 🔴 K18 cırcırı: ErrorCode.php'yi değiştirince k18:check dosyanın TAMAMINI ölçer (26 Kasım'da 9 uzun blok). Blokları 1–3
   satıra indir, ayrıntıyı docs/rehber/app/Enums/ErrorCode.md'ye taşı (anlam kaybı olmasın).
4. Kapılar: composer check, npm run check (verify:errors kod sayısı 31 → 28).
```

### 22.7 — `FE-08`: konum araması

`src/services/places.ts`, `hooks/usePlaceSearch.ts`, `components/create/location/LocationSearchField.tsx` duruyor; backend'de
`places` rotası yok; bayrak (`VITE_PLACES_SEARCH_ENABLED`) kapalı.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Yol | **Kaldır:** üç dosya ve bayrak silinir, "haritadan seç" tek yol | |
| 2 | Uç yazılacaksa | Ayrı faz (Places anahtarı sunucuda, önbellek, `throttle`, KVKK gizlilik metni) — Faz 22'de yalnızca plan | |

```text
DavetKart Faz 22.7 — FE-08 (konum araması). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula; 22.7 §A
cevapları kararlardır. Tam metin: findings\04-frontend-e2e.md "FE-08".

Kaldır seçildiyse: üç dosyayı ve kullanım yerlerini, .env örneklerindeki bayrağı ve docs/rehber kılavuzlarını kaldır; editörde
konum alanı "haritadan seç"/elle yazma ile çalışmaya devam etmeli (e2e createInvitation 'Davet Konumu' alanını dolduruyor).
verify:endpoints ve verify:i18n tabanı azalırsa `npm run verify:i18n -- --update` (yalnızca azalış). npm run check + npm run e2e.
Uç seçildiyse: kod yazma; planı bu sayfanın sonuna "Ek C — FE-08 konum araması planı" olarak yaz (uç sözleşmesi, sağlayıcı,
maliyet, KVKK) ve §1 satırını "plan" olarak işaretle.
```

### 22.8 — `FE-03`: TypeScript `strict`

26 Kasım'da `npx tsc --noEmit --strict` → 20 hata: 15'i `templates/shared/effects/particleEngine.ts`, 2 `preview/PreviewSection.tsx`,
1'er `templates/lazyPresets.ts`, `templates/TemplateRenderer.tsx`, `create/EditorWorkspace.tsx`.

```text
DavetKart Faz 22.8 — FE-03 (TypeScript strict). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula. Tam
metin: findings\04-frontend-e2e.md "FE-03".

1. Ölç: npx tsc --noEmit --strict (dosya başına sayı raporda).
2. tsconfig.json'a "strict": true. Hataları davranış değiştirmeden kapat: null için erken dönüş/daraltma; `as` ve `!` yalnızca
   gerekçesi bir satır yorumla. particleEngine.ts'te canvas/context null'ı bir kez daraltılıp aşağı geçirilsin.
3. noUncheckedIndexedAccess bu maddede AÇILMAZ; açılırsa kaç hata çıktığını raporda yaz (sonraki karar için).
4. npm run check + npm run e2e (şablonlar ve editör a11y taraması dahil) + npm run a11y:envelopes.
```

### 22.9 — `TST-05`: Node sürümü

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Sürüm | Node 24 (yerel 24.18; sunucudaki derleme sürümü bilinmiyor → İsmail'e komut) | |

```text
DavetKart Faz 22.9 — TST-05 (Node sürümü). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula; 22.9 §A
cevabı karardır. Tam metin: findings\03-testing.md "TST-05".

1. Frontend köküne .nvmrc (§A-1) + package.json "engines": {"node": ">=24 <25"}; .github/workflows/*.yml'de node-version
   yerine node-version-file: .nvmrc (her iş).
2. deploy-frontend.sh başında `node --version` .nvmrc ile uyuşmuyorsa UYARI (durdurma) — backend deposundaki deploy/ betiğine
   dokunmak gerekiyorsa o depoda ayrı dal, aynı madde numarası.
3. Kılavuz + İsmail'e: sunucuda `node --version` komutu. CI push'u İsmail'in; CI koşusu "koşmadı".
```

### 22.10 — `TST-06`: paralel testler

```text
DavetKart Faz 22.10 — TST-06 (paralel backend testleri). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula.
Tam metin: findings\03-testing.md "TST-06"; K182 (DAVETKART_TEST_DB_SUFFIX, TestSuiteIsolationTest).

1. Ölç: php artisan test (tam süre, 26 Kasım: ~200–260 sn, 1306 test).
2. brianium/paratest (dev) + `php artisan test --parallel`: PostgreSQL'de süreç başına veritabanı (davetkart_test_<token>), K182
   son ekiyle birlikte çalışmalı; TestSuiteIsolationTest buna göre. Kilit testleri (concurrency grubu, TST-02: alt süreç ve
   lock_timeout) paralelde kararsızsa onları ayrı grupta sıralı koştur.
3. composer check'teki test adımını paralele çevirmek §A'sız değişiklik değildir: önce `composer test:parallel` gibi ayrı betik;
   üç ardışık yeşil koşu + süre farkı raporda; check'e alınması İsmail'in onayıyla (raporda sor).
4. composer audit (yeni dev bağımlılığı).
```

### 22.11 — `TST-03`: satır kapsamı

Yerel Herd PHP'de `pcov`/`xdebug` yok (26 Kasım'da yeniden bakılmadı).

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Eşik | İlk ölçümün 3 puan altı; ölçüm yoksa eşik yok, yalnızca rapor | |

```text
DavetKart Faz 22.11 — TST-03 (kapsam). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula; 22.11 §A cevabı
karardır. Tam metin: findings\03-testing.md "TST-03".

1. Yerelde php -m ile pcov/xdebug var mı bak; yoksa kurulum yolunu (Herd) kılavuza yaz, kurma.
2. CI (.github/workflows/ci.yml): coverage: pcov ve ayrı adımda `php artisan test --coverage --min=<eşik>` (eşik yoksa --min'siz,
   özet artefakt). composer check değişmez.
3. Ölçüm yerelde koşmadıysa eşik koyma; raporda "ilk CI koşusundan sonra eşik" adımını İsmail'e yaz.
```

### 22.12 — `ARC-10`: görsel işleme işi

```text
DavetKart Faz 22.12 — ARC-10 (OptimizeUploadedImage'ı ayır). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve
uygula. Tam metin: findings\01-architecture.md "ARC-10". Davranış DEĞİŞMEZ (saf yeniden düzenleme).

1. Önce mevcut OptimizeUploadedImageTest + medya testlerini koş, yeşil taban (sayı raporda).
2. app/Jobs/OptimizeUploadedImage.php (664 satır) → küçük sınıflar (öneri: ImageDecoder, ExifOrientation, ImageEncoder,
   MediaFileSwap; adlar ve yerleri CLAUDE.md'ye göre: dış servis değil → app/Support/Media/ ya da Action). Job yalnızca sırayı yönetir.
3. Her yeni sınıfa birim testi + bir mutant; uçtan uca test aynen yeşil. EXIF ve dosya sonuna eklenmiş PHP kuyruğunun saklanan
   dosyada olmadığı (AUD P54–P55) testle korunuyor mu bak; yoksa ekle.
4. K18: job'un 264 satırlık yorumu sınıf kılavuzlarına dağılır; k18:check temiz.
```

### 22.13 — `SEC-18`: token `httpOnly` çerezde

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Kapsam | **Yalnızca plan** (karar kaydı + geçiş planı); uygulama CSP zorlamaya geçtikten (K175) sonra ayrı faz | |
| 2 | Uygulama seçilirse | Sanctum SPA çerez kimliği (aynı site: `davetkart.com` + `/api`), CSRF çerezi, `{user, token}` zarfı yerine `{user}` (K11 değişir), geçiş süresince iki yol | |

```text
DavetKart Faz 22.13 — SEC-18 (çerez tabanlı oturum). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula;
22.13 §A cevapları kararlardır. Tam metin: findings\02-security.md "SEC-18"; K5, K11, K174–K175 (CSP), FE tarafı
src/services/auth.ts ve api.ts.

§A-1 = plan (varsayılan): kod yazma. Planı ayrı dosyaya değil bu sayfanın sonuna "Ek A — SEC-18 geçiş planı" olarak yaz
(Faz 22 tek sayfa): tehdit (XSS ile token okuma), seçenekler, Sanctum SPA kurulumu (stateful
domain, CSRF, CORS, Nginx), K11/K20 etkisi, frontend değişiklikleri (interceptor, 401, sekme senkronu), mobil/üçüncü taraf
etkisi (yok), geçiş ve geri alma, test planı (e2e), ön koşul K175 zorlama. Sonunda İsmail'e karar soruları. K: "planlandı".
§A-1 = uygula: önce planı yaz, İsmail'e göster ve DUR.
```

### 22.14 — `OPS-09`: yatay ölçek eşikleri

```text
DavetKart Faz 22.14 — OPS-09 (ölçek eşikleri). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula. Tam metin:
findings\05-operations.md "OPS-09". Yalnızca docs; kod yok.

operations/deployment/YAYIN-PLANI.md §6'daki "Lightsail'den ne zaman çıkılır" eşiklerine ölçülebilir sayılar ekle: FPM kuyruğu
(slowlog/listen queue), bellek (OPS-07 tablosu), p95 yanıt süresi, PostgreSQL bağlantı ve disk. İkinci sunucuya geçişte
kırılacaklar listesi (file cache → hız sınırı sayaçları sunucu başına, onOneServer/withoutOverlapping kilitleri, database kuyruğu)
ve sıra (önce PostgreSQL'i ayır, sonra Redis: cache + kuyruk + kilit). YAYIN-PLANI bir plan kaydı: eski satırları yeniden yazma,
yeni alt bölüm ekle. IZLEME.md'ye hangi metriğin nereden okunacağı.
```

### 22.15 — `SEC-17`: diskteki eski kod arşivleri

`davetkart-docs/archive/local-snapshots/` (git dışı, `.gitignore:5`): 26 Kasım'da 16 dosya, 148 MB (`_snap/*.tgz|*.tar`). Denetimde üçünün
dosya listesinde `.env` vardı. Silme ve anahtar döndürme **senin** işin.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Arşivler | Ajan yalnızca listeler; sen silersin ya da şifreli kasaya taşırsın | |
| 2 | Anahtarlar | `.env` içeren arşivlerdeki anahtar **adlarını** (değerleri değil) ajan listeler; hâlâ geçerli olanları sen döndürürsün | |

```text
DavetKart Faz 22.15 — SEC-17 (yerel arşivler). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve uygula; 22.15 §A
cevapları kararlardır. Tam metin: findings\02-security.md "SEC-17".

🔴 Arşivleri AÇMA, içerik okuma, değer yazdırma. Yalnızca `tar -tf`/`tar -tzf` ile dosya ADI listesi.
1. Her arşiv: boyut, tarih, .env / *.pem / credentials içeren yol var mı (evet/hayır). .env içeren arşivlerde yalnızca .env'in
   anahtar ADLARI gerekiyorsa §A-2 için: `tar -xOf <arşiv> <yol> | grep -oE '^[A-Z0-9_]+='` (değer yazdırma YOK, çıktı yalnızca adlar).
2. Bu sayfanın sonuna "Ek B — SEC-17 arşiv listesi" (adlar, boyutlar, içerik türü; değer yok).
3. İsmail'e: hangi arşivin silinebileceği, hangi anahtarların (APP_KEY, DB parolası, AWS, Shopier) döndürülmesi gerektiği
   ve nasıl (her biri için tek satır yol). Sen silme.
```

### 22.16 — `ARC-08`: dal hijyeni ve sürüm etiketleri

26 Kasım: backend 33, frontend 48, docs 7 yerel dal; üç depoda da etiket yok; `davetkart-backend-php-laravel.worktrees/` altında 4 eski
worktree; `D:\Projects\davetkart-hat-{a,b,c}` Faz 19 worktree'leri (ayrık uçta). Bekleyen etiketler: `v1.0.0`, `v1.1.0` (Faz 18 +
`SEC-07`), `v1.2.0` (Faz 19) — Hat C #21.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Silinecek dallar | Yalnızca `git branch --merged <entegrasyon>` listesindekiler, tek tek senin onayınla; uzak dallara dokunulmaz | |
| 2 | Worktree'ler | Temiz olanlar (`git status` boş) `git worktree remove`; kirli olan listelenir, dokunulmaz | |
| 3 | Etiketler | Ajan hangi commit'in hangi etiket olacağını docs kayıtlarından çıkarır ve tablo halinde sunar; etiketi sen onaylarsın, push senin | |

```text
DavetKart Faz 22.16 — ARC-08 (dal hijyeni, etiketler, worktree'ler). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi
oku ve uygula; 22.16 §A cevapları kararlardır. Tam metin: findings\01-architecture.md "ARC-08"; etiket kayıtları:
phases\faz-19\FAZ-19-SEC-07-COMMIT-KOMUTLARI.md §5, FAZ-19-ARC-03-COMMIT-KOMUTLARI.md §5–§7, operations\deployment\YAYIN-SIRASI.md §3,
phases\faz-19\HAT-C-ACIK-HATALAR.md #21, #29.

Bu madde GERİ DÖNÜŞSÜZ adımlar içerir: her silmeden önce tabloyu göster ve İsmail'in "evet"ini bekle (§3 madde 4).
1. Üç depo için tablo: dal, son commit tarihi, entegrasyon dalına birleşmiş mi, hangi worktree'de açık. Yazım hatalı adlar işaretli.
2. Worktree tablosu (yol, dal/uç, temiz mi).
3. Etiket önerisi: v1.0.0 / v1.1.0 / v1.2.0 için commit + gerekçe (kayıttan alıntı).
4. Onaydan sonra: yalnızca onaylanan dalları `git branch -d` (asla -D), worktree remove, etiketleri `git tag -a`. Push yok.
5. Kayıt: HAT-C-ACIK-HATALAR #21/#29 ve bu sayfa §1.
```

### 22.17 — `ARC-07`: frontend `.gitattributes` (en son)

Frontend çalışma ağacı CRLF, indeks çoğunlukla LF (`autocrlf`); sözleşme dosyası iki depoda bayt bayt farklı. Normalizasyon commit'i
yüzlerce dosyaya dokunabilir; açık dallarla çakışmasın diye **bütün frontend dalları birleştikten sonra**.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Kural | `* text=auto eol=lf` + ikili kalıplar (`*.png *.jpg *.webp *.mp4 *.webm *.woff2 *.glb *.ico binary`) | |
| 2 | Çalışma ağacı | Dokunulmaz: mevcut CRLF dosyalar git'te LF'ye normalize edilir, `git status` temiz kalmalı. Dosyaları diskte de LF'ye çevirmek isteğe bağlı; ajan adımları yazar (yalnızca temiz ağaçta, Vite kapalıyken), sen koşarsın | |

```text
DavetKart Faz 22.17 — ARC-07 (.gitattributes + satır sonu). Önce davetkart-docs\phases\faz-22\README.md §3 ve §2'yi oku ve
uygula; 22.17 §A cevapları kararlardır. Tam metin: findings\01-architecture.md "ARC-07".

Ön koşul: frontend'de birleşmemiş Faz 22 dalı yok (`git branch --no-merged faz-22-backlog` boş); değilse DUR.
1. Ölç: `git ls-files --eol` özeti (i/lf, i/crlf, i/mixed sayıları) ve contracts/error-codes.json'ın backend kopyasıyla bayt farkı.
2. İki ayrı commit: (a) yalnızca .gitattributes; (b) `git add --renormalize .` sonucu (yalnızca satır sonu; `git diff --cached
   --ignore-all-space --stat` boş olmalı — değilse DUR).
3. Sonrasında npm run check + npm run e2e; contracts dosyası backend'le bayt bayt aynı (sha256).
4. docs CLAUDE.md §7 "CRLF tuzağı" maddesine ve hafıza notlarına güncelleme önerisi (CLAUDE.md'yi İsmail onaylamadan değiştirme).
```
