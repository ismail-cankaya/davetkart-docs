# Yayına hazırlık ve işletim — AUD-2026-11-12

> Yürüten: ana oturum (Fable 5.2) · Kopya: `_audit-snap\backend` (okuma) · Commit: backend `d810410`, frontend `44caa49` · Tarih: 15 Kasım 2026
> Kaynaklar: `davetkart-docs/operations/deployment/YAYIN-PLANI.md` (§8 ilerleme kaydı, son satır 26 Ekim), `YAYIN-DEVIR.md`, `backend:deploy/`, `backend:docs/10-URETIM-ENV-SABLONU.md`, `backend:docs/rehber/deploy/`, diğer dört bulgu dosyası.
> **Canlı sisteme hiçbir istek atılmadı.** Sunucunun bugünkü durumu yalnızca yayın planının kaydından okundu; "plan kaydına göre" yazan her satır bu denetimde doğrulanmamıştır (B7).

## Özet

Altyapının yazılı kısmı özenli: dağıtım betiği temiz çalışma ağacı ister, yalnızca ileri sarar, sağlık
kontrolüyle biter; frontend dağıtımı `dist/` klasörünü atomik değiştirir ve eski parçaları 14 gün tutar; kuyruk
işçisi bellek sınırıyla ve yeniden doğumla tanımlı; zamanlanmış dört işin dördü de çakışma kilidi ve Sentry
izleyicisi taşıyor; yükleme sınırları uygulama → PHP → Nginx zincirinde tutarlı.

Yayın öncesi kapatılması gereken iki konu var. **Hangi commit'in yayına çıkacağı belli değil:** üretimdeki
backend (`main`) denetlenen daldan 4, frontend `main`'i 71 commit geride ve iki depo birlikte yükseltilmezse
19 premium şablon sunucuda Gold'a bağlı olmadan yayına girer (`OPS-01`). **Veritabanı yedeği ve geri yükleme
provası henüz yok** (`OPS-02`). İzleme ve alarm da kurulmamış (`OPS-03`).

Plan kaydına göre Y0–Y9 tamam (backend 26 Ekim'de canlıda, `/api/ping` yanıt veriyor), Y10 (frontend), Y11
(entegrasyon, yedek, izleme) ve Y12 (canlı doğrulama) açık.

Seviye sayıları: 🔴 0 · 🟠 2 · 🟡 3 · 🟢 3 · 💡 1 — Kanıt: KOŞTURULDU 1 · KOD OKUMASI 8

## Özet tablosu

| ID | Seviye | Kanıt türü | Başlık | Nerede | Efor | Tek satır öneri |
|---|---|---|---|---|---|---|
| OPS-01 | 🟠 | KOŞTURULDU | Yayına çıkacak commit belirsiz; iki depo ayrı yükseltilirse 19 premium şablon korumasız | iki kod deposu: `main` ↔ `ccr-9a346997-bu6gve` | S | Önce backend, sonra frontend; ikisini de `main`'e al ve etiketle |
| OPS-02 | 🟠 | KOD OKUMASI | Veritabanı yedeği ve geri yükleme provası yok | `YAYIN-PLANI.md` Y11.5–Y11.6 · `backend:deploy/` | M | `deploy/backup/pg-dump.sh` + cron + bir kez geri yükleme provası |
| OPS-03 | 🟡 | KOD OKUMASI | İzleme ve alarm kurulmamış; sağlık ucu yalnızca PHP'nin ayakta olduğunu söylüyor | `backend:app/Http/Controllers/Api/V1/HealthController.php:19-22` | S | Sentry DSN + dış izleme + veritabanına dokunan hazır olma ucu |
| OPS-04 | 🟡 | KOD OKUMASI | Üretim `.env` şablonu sunucudaki gerçek dosyadan sapmış | `backend:docs/10-URETIM-ENV-SABLONU.md:59,123,228` | S | Şablonu Y8.3b düzeltmeleriyle güncelle |
| OPS-05 | 🟡 | KOD OKUMASI | Tek hata noktaları: alan adı otomatik yenilemesi kapalı, posta ve kredi bitiş tarihleri | `YAYIN-PLANI.md` §8 "Süre takvimi" | S | Otomatik yenilemeyi aç; iki tarihi takvime yaz |
| OPS-06 | 🟢 | KOD OKUMASI | Dağıtım yerinde yapılıyor, bakım kipi yok | `backend:deploy/deploy.sh` | M | `artisan down`/`up` ya da sürüm klasörü + sembolik bağ |
| OPS-07 | 🟢 | KOD OKUMASI | PHP-FPM havuzu ve OPcache ayarı depoda yok; bellek bütçesi yazılı değil | `backend:deploy/php/davetkart.ini` | S | `deploy/php-fpm/` altına havuz dosyası + bellek tablosu |
| OPS-08 | 🟢 | KOD OKUMASI | Günlüklerde istek kimliği yok | `backend:config/logging.php`, `bootstrap/app.php` | S | `X-Request-Id` ara katmanı + `Log::shareContext` |
| OPS-09 | 💡 | KOD OKUMASI | Yatay ölçeğin önündeki tasarım kararları | `file` cache, `database` kuyruk, tek makinede PostgreSQL | L | Bugün dokunma; eşikleri ölç ve yaz |

## Neler iyi

1. **Dağıtım betiği hataya karşı yazılmış.** `set -euo pipefail`; kirli çalışma ağacında durur; `git pull
   --ff-only`; `deploy/` değiştiyse kendini yeni sürümle yeniden başlatır; `www-data` ile `artisan`; sonunda
   `https://davetkart.com/api/ping`'i yerelden çağırır (`deploy/deploy.sh`).
2. **Frontend değişimi atomik ve geri alınabilir.** `dist.new/`'e derlenir, eski `assets/` dosyaları kopyalanır
   (14 gün tutulur; açık sekmeler eski parçaları yükleyebilir), `dist → dist.old`, `dist.new → dist`, ana sayfa
   denetlenir; hata olursa tek satırla geri alınır (`deploy/deploy-frontend.sh`). Bu, `FE-02`'deki "yayın
   sonrası bulunamayan chunk" senaryosunu 14 gün için kapatıyor.
3. **En az yetki.** `deploy` kullanıcısının `sudo`'su üç komutla sınırlı (`deploy/sudoers/davetkart-deploy`);
   uygulamanın AWS kimliği tek bucket ve SES ile sınırlı, GitHub anahtarı salt okunur (plan kaydı Y3.4, Y8.1).
4. **Kuyruk işçisi sınırlı ve kendini yeniliyor.** `Restart=always`, `--max-time=3600`, `--timeout=60` <
   `retry_after` 90, `MemoryMax=768M` + `MemorySwapMax=0`, `NoNewPrivileges`, `PrivateTmp`
   (`deploy/systemd/davetkart-queue.service`).
5. **Zamanlanmış işler korumalı ve izlenmeye hazır.** Dört işin dördünde `withoutOverlapping()`,
   `onOneServer()` ve `sentryMonitor(...)` (`routes/console.php:44-98`). DSN girildiği gün "iş çalışmadı" alarmı
   hazır.
6. **Yükleme sınırları zincir boyunca tutarlı.** Uygulama 15 MB (fotoğraf) / 20 MB (video)
   (`config/davetkart.php:193-210`) ≤ PHP `upload_max_filesize=25M` ≤ `post_max_size=30M` ≤ Nginx
   `client_max_body_size 30m`. Büyük dosyayı Nginx değil Laravel reddeder; kullanıcı anlamlı hata görür.
7. **Nginx varsayılan sunucuları kapalı.** Bilinmeyen ad 80'de `444`, 443'te `ssl_reject_handshake on`;
   nokta ile başlayan dosyalar 404; `server_tokens off` (`deploy/nginx/davetkart.conf`).
8. **Aynı kaynak (same-origin).** `/api` aynı alan adında: CORS yok, vekil başlığı yok, istemci IP'si
   `REMOTE_ADDR`'den geliyor; `TRUSTED_PROXIES` boş (R5).
9. **Üretim günlük ayarı tutumlu.** `LOG_STACK=daily,sentry`, `LOG_LEVEL=warning`, 14 gün
   (`docs/10-URETIM-ENV-SABLONU.md:137-143`); `APP_DEBUG=false`, `SENTRY_SEND_DEFAULT_PII=false`.
10. **Plan kaydına göre sunucu temeli sağlam:** `unattended-upgrades`, 2 GB swap, parolasız ve `sudo`'suz
    `deploy` kullanıcısı, PostgreSQL yalnızca `127.0.0.1`, S3'te Block Public Access + sürümleme + 7 günlük
    eski sürüm temizliği, CloudFront OAC, bütçe alarmları, Argon2id ölçümü (260 ms).

## Bulgular

### OPS-01 Yayına çıkacak commit belirsiz; iki depo ayrı yükseltilirse 19 premium şablon korumasız
- Seviye: 🟠 Yüksek
- Kanıt türü: KOŞTURULDU
- Nerede: backend `origin/main` = `origin/release-v1.0` = `03d3940` (26 Ekim) ↔ denetlenen `d810410` (4 commit ileride) · frontend `origin/main` = `47aedc8` ↔ denetlenen `44caa49` (71 commit ileride, 1 geride) · frontend'de `release-v1.0` dalı yok · iki depoda etiket yok
- Senaryo: 1) Sunucu `main`'i çekiyor (plan kaydı Y8.2a). Backend `main`'inde 13 premium şablon Gold'a bağlı. 2) Frontend'in yeni şablonları (Faz 15–17, 71 commit) `main`'e alınıp Y10'da yayınlanır; backend'in dört commit'i (Faz 16–17 `preset_tiers`) unutulur ya da sonraya kalır. 3) Arayüz 32 şablonu "Premium · Gold+" diye gösterir; sunucu yalnızca 13'ünü tanır. 4) Kullanıcı Standart planla (249 ₺) premium bir şablon seçip yayınlar; sunucu 402 dönmez. Fark şablon başına 150 ₺.
- Kanıt: `evidence/commands/OPS-branch-state.txt`: `rev-list --count origin/main..origin/ccr-9a346997-bu6gve` → backend 4, frontend 71 (tersi 0 ve 1); `git show origin/main:config/davetkart.php | grep -c "=> 'gold',"` → 15 (13 şablon + 2 modül), denetlenen dalda 34 (32 + 2); frontend `minimumTier` sayısı `main`'de 13, denetlenen dalda 32.
- Etki: Para kaybı ve geri alınması zor bir durum: Standart'la yayınlanmış premium davetiyeler sonradan kapatılırsa müşteri şikâyeti, açık bırakılırsa fiyatlandırma delinmiş olur. Ayrıca denetlenen dalın kalite kapısı kırmızı (`TST-01`) ve Faz 16–17'nin kaydı yok (`ARC-02`); yani "yayına hazır commit" bugün hiçbir dalda işaretli değil.
- Neden önemli (öğretici not): İki depo tek bir ürünün iki yarısıdır ve aralarındaki sözleşme (hangi şablon hangi planda) iki tarafta ayrı ayrı durur (`FE-05`). Böyle bir sözleşmede **dağıtım sırası** bir doğruluk koşuludur: kuralı uygulayan taraf (sunucu) önce, kuralı gösteren taraf (arayüz) sonra yayınlanır. Etiket, "hangi iki commit birlikte doğrulandı" sorusunun tek dürüst cevabıdır.
- Öneri: 1) Sıra: backend'in dört commit'i → `main` (`composer check` yeşil olduktan sonra) → `deploy.sh`; ardından frontend → `main` → Y10. 2) İki depoda aynı adla etiket (`v1.1.0`); `deploy.sh` yayınlanan commit'i günlüğe yazıyor, etiketi de yazsın. 3) Frontend `npm run check`'e "premium şablon listesi backend sözleşmesiyle aynı" denetimi (`FE-05`'teki `verify:plans`). 4) Frontend `main`'deki `47aedc8` (bağımlılık temizliği) denetlenen dala alınmalı (`SEC-14`).
- Test önerisi: `verify:plans`: `src/data.ts`'teki `minimumTier` kimlikleri ↔ `contracts/plan-rules.json`. Öldürmesi gereken mutant: sözleşme dosyasından bir premium kimliği silmek.
- Efor: S
- İlgili: `ARC-08` (dal hijyeni) · `ARC-02` · `TST-01` · `FE-05` · `SEC-14`

### OPS-02 Veritabanı yedeği ve geri yükleme provası yok
- Seviye: 🟠 Yüksek
- Kanıt türü: KOD OKUMASI
- Nerede: `YAYIN-PLANI.md` Y11.5 (gece `pg_dump` → S3), Y11.6 (geri yükleme provası): ilerleme kaydında yok · `backend:deploy/` (yedek betiği yok; `deploy/cron/davetkart` yalnızca `schedule:run`) · tek yedek: Lightsail günlük disk görüntüsü, son 7 gün (plan kaydı Y4.4)
- Senaryo: A) Hatalı bir göç ya da elle çalıştırılan bir `DELETE` siparişleri bozar. Disk görüntüsü bütün sunucuyu dünkü hâline döndürür: aradaki ödemeler ve LCV'ler de gider; tek tabloyu geri getirmek mümkün değil. B) Lightsail hesabı ya da bölgesi erişilemez olur; görüntüler aynı hesapta. C) Yedek alınıyor sanılır, ilk ihtiyaçta dosyanın açılmadığı görülür.
- Kanıt: `grep -rl pg_dump backend/deploy backend/docs/rehber/deploy` → boş; `YAYIN-PLANI.md` §8'de Y11 satırı yok; `YAYIN-DEVIR.md:119` Y11'i "yapılacak" diye listeliyor.
- Etki: Sipariş, hak ve misafir yanıtı kaybı; kurtarma noktası 24 saat. Bugün canlıda müşteri verisi yok (frontend yayında değil), yani bu açığın kapatılması için en ucuz an şimdi.
- Neden önemli (öğretici not): Yedeğin iki ölçüsü vardır: ne kadar veri kaybedersin (RPO) ve ne kadar sürede dönersin (RTO). Disk görüntüsü "sunucu yandı"yı, mantıksal döküm (`pg_dump`) "veri bozuldu"yu çözer; ikisi farklı felaketlerdir. Ve denenmemiş yedek bir umuttur: geri yükleme provası yedeğin testidir.
- Öneri: `deploy/backup/pg-dump.sh` (`pg_dump -Fc` → `gzip` gerekmez → `aws s3 cp` ayrı bucket'a, başarısızlıkta sıfır dışı çıkış) + `/etc/cron.d` satırı 02:00 UTC + S3 ömür kuralı (30 gün) + Sentry Crons izleyicisi. Bir kez: dünkü dökümü yerelde `pg_restore` ile aç, `orders` ve `invitations` sayılarını karşılaştır, süreyi plana yaz. Kayıt açılmadan önce tamamlanmalı.
- Test önerisi: Aylık geri yükleme provası (takvim işi); betik için: boş veritabanında döküm → geri yükle → satır sayıları eşit.
- Efor: M
- İlgili: Y11.5, Y11.6 · `SEC-11` (yedeklerde saklama süresi ve gizlilik metni)

### OPS-03 İzleme ve alarm kurulmamış; sağlık ucu yalnızca PHP'nin ayakta olduğunu söylüyor
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:app/Http/Controllers/Api/V1/HealthController.php:19-22` (`return response()->json(['status' => 'ok'])`) · `YAYIN-PLANI.md` Y11.3 (Sentry DSN), Y11.7 (dış izleme): ilerleme kaydında yok · `docs/10-URETIM-ENV-SABLONU.md:195` (`SENTRY_LARAVEL_DSN=` boş)
- Senaryo: 1) PostgreSQL durur ya da disk dolar. 2) `/api/ping` veritabanına dokunmadığı için 200 dönmeye devam eder; dağıtım betiğinin sağlık kontrolü ve kurulacak dış izleme "çalışıyor" der. 3) Kuyruk işçisi takılırsa parola sıfırlama mailleri gitmez; hata da üretmez. 4) Sorunu ilk fark eden müşteri olur.
- Kanıt: `HealthController` gövdesi tek satır; `grep -rnE "Queue::failing|queue:monitor" app routes deploy` → boş.
- Etki: Arıza süresi, birinin şikâyet etmesine kadar uzar. Kod tarafı hazır: dört zamanlanmış işte `sentryMonitor` var, DSN girilince çalışır.
- Neden önemli (öğretici not): İki ayrı soru vardır: süreç **canlı mı** (liveness) ve iş **yapabiliyor mu** (readiness). Tek bir "ok" dönen uç yalnızca ilkini cevaplar. İzleme, sistemin sessizce bozulabildiği her yere (veritabanı, kuyruk, zamanlayıcı, disk) bir duyarga koymaktır.
- Öneri: 1) `GET /api/ping` aynen kalsın (ucuz, dağıtım için). 2) `GET /api/health`: `DB::select('select 1')`, `jobs` tablosundaki en eski işin yaşı, son `schedule:run` zamanı (cache'e yazılan damga), disk boşluğu; herhangi biri eşik dışıysa 503. Ayrıntı döndürmesin. 3) Sentry DSN + `Queue::failing` dinleyicisi. 4) Dış izleme `/api/health`'e, 1 dakikada bir.
- Test önerisi: `HealthTest::readiness_fails_when_the_database_is_unreachable` (bağlantı adı geçersiz yapılır → 503). Öldürmesi gereken mutant: veritabanı denetimini kaldırmak.
- Efor: S
- İlgili: Y11.3, Y11.7 · R7 (4xx Sentry'ye gitmez)

### OPS-04 Üretim `.env` şablonu sunucudaki gerçek dosyadan sapmış
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:docs/10-URETIM-ENV-SABLONU.md:59` (`APP_URL=https://api.davetkart.com`) · `:123` (`AWS_BUCKET=`; `AWS_URL` satırı yok) · `:228` (`MAIL_MAILER=log`) ↔ `YAYIN-PLANI.md` §8 Y8.3b ("şablondan, düzeltmelerle: `APP_URL=https://davetkart.com` … `AWS_URL=https://media.davetkart.com` (şablonda yoktu)")
- Senaryo: Sunucu yeniden kurulur (planın ilkesi: "sunucu yok edilebilir"). `.env` şablondan üretilir: `APP_URL` var olmayan `api.` alt alanını gösterir, medya adresleri CloudFront yerine S3'ün doğrudan adresine döner (bucket herkese kapalı → görseller 403), posta `log` sürücüsünde kalır (parola sıfırlama maili hiç gitmez, hata da vermez).
- Kanıt: Şablon dosyası okundu; gerçek sunucu `.env`'i okunmadı (canlı sisteme dokunulmadı), düzeltmelerin kaynağı plan kaydı. Şablon 65 anahtar taşıyor; uygulamaya özgü anahtarlardan eksik olan `AWS_URL`.
- Etki: Bir sonraki kurulumda aynı üç hata yeniden yapılır; bulunmaları ilk seferinde bir oturum sürmüştü. Posta sürücüsünün sessiz `log` varsayılanı en tehlikelisi: kullanıcı "mail gelmedi" der, sunucuda hata yoktur.
- Neden önemli (öğretici not): Şablon, altyapının kod hâlidir; sunucuda elle yapılan her düzeltme şablona geri işlenmezse "altyapı da kod" ilkesi tek yönlü çalışır. Belgeyle gerçek arasındaki fark, bir felaket kurtarma anında ortaya çıkan gizli borçtur.
- Öneri: Şablonu güncelle: `APP_URL=https://davetkart.com`, `AWS_URL=https://media.davetkart.com`, `AWS_BUCKET` örnek değeri; `MAIL_MAILER` için üretimde `log` kalırsa açılışta uyarı (`AppServiceProvider`: `production` + `log` → `Log::critical`). Şablonla config'in okuduğu anahtarları karşılaştıran küçük bir denetim `composer check`'e eklenebilir.
- Test önerisi: `ProductionConfigTest::the_log_mailer_is_refused_in_production` (ortam `production`, sürücü `log` → açılış hatası ya da kritik günlük).
- Efor: S
- İlgili: Y8.3b · Y7.5 (SES üretim erişimi) · `ARC-05` (doküman kayması)

### OPS-05 Tek hata noktaları: alan adı otomatik yenilemesi kapalı, posta ve kredi bitiş tarihleri
- Seviye: 🟡 Orta
- Kanıt türü: KOD OKUMASI
- Nerede: `YAYIN-PLANI.md` §8 "Süre takvimi": alan adı `davetkart.com` 11 Eylül 2027 ("Otomatik yenileme KAPALI") · Natro posta barındırma 11 Ocak 2027 · AWS kredisi 25 Temmuz 2027
- Senaryo: Alan adı yenilenmez: site, API, medya alt alanı, SSL yenilemesi ve bütün postalar aynı gün durur. Posta barındırma biterse `bilgi@davetkart.com` kutusu kapanır; SES'in gönderen adresi ve müşteri yanıtları buraya geliyor.
- Kanıt: Plan dosyasının kendi kaydı (4 ve 25 Ekim); alan adı sağlayıcısının paneli bu denetimde görülmedi.
- Etki: Tam kesinti; alan adı başkasına geçerse kalıcı. En yakın tarih iki ay sonra (posta, 11 Ocak 2027).
- Neden önemli (öğretici not): En güvenilir sistemler çoğu zaman bir faturanın ödenmemesiyle düşer. Süresi dolan her şey (alan adı, sertifika, kredi, anahtar) bir izleme kalemidir.
- Öneri: Alan adında otomatik yenilemeyi aç ve kartı doğrula; posta için karar ver (yenile ya da taşı) ve 11 Aralık'a hatırlatıcı; kredi bitişinden bir ay önceye hatırlatıcı. Dış izleme aracı alan adı ve sertifika bitişini de izleyebilir.
- Test önerisi: —
- Efor: S
- İlgili: Y1.3, Y11.7

### OPS-06 Dağıtım yerinde yapılıyor, bakım kipi yok
- Seviye: 🟢 Düşük
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:deploy/deploy.sh` (sıra: `git pull` → `composer install` → `config:cache`, `route:cache` → `migrate --force` → `php-fpm reload`)
- Senaryo: `git pull` ile `php-fpm reload` arasındaki saniyelerde PHP dosyaları yeni, OPcache ve veritabanı şeması eski olabilir. Sütun ekleyen bir göçte bu aralıkta gelen istek 500 alabilir; sütun silen bir göçte geri alma kod + şema birlikte yapılmak zorunda.
- Kanıt: Betik okundu; geri alma adımları `docs/rehber/deploy/deploy.md` §4'te elle tarif edilmiş.
- Etki: Bugünkü trafikte birkaç saniyelik, nadir bir pencere. Trafik arttıkça görünür olur.
- Neden önemli (öğretici not): Yerinde dağıtımda "eski sürüm" ile "yeni sürüm" arasında tanımsız bir ara hâl vardır. Sürüm klasörleri (her dağıtım yeni bir dizin, sonunda tek bir sembolik bağ değişir) bu ara hâli ortadan kaldırır; frontend betiği bunu zaten yapıyor (`dist.new` → `dist`).
- Öneri: Ucuz: göç içeren dağıtımlarda `artisan down --retry=15` … `artisan up`. Sağlam: backend için de `releases/<commit>` + `current` bağı; göçler geriye uyumlu yazılır (önce ekle, sonraki sürümde sil).
- Test önerisi: —
- Efor: M
- İlgili: Y0.5

### OPS-07 PHP-FPM havuzu ve OPcache ayarı depoda yok; bellek bütçesi yazılı değil
- Seviye: 🟢 Düşük
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:deploy/php/davetkart.ini` (yalnızca yükleme sınırları, `memory_limit=256M`, hata gösterimi) · `grep -rnE "pm\.max_children|opcache\." deploy docs/rehber/deploy docs/10-URETIM-ENV-SABLONU.md` → boş
- Senaryo: Sunucu 2 GB. Kuyruk işçisi 768 MB'a kadar, her FPM süreci 256 MB'a kadar, PostgreSQL kendi payını alır. `pm.max_children` Ubuntu varsayılanında (5) kalırsa en kötü durumda 5 × 256 + 768 = 2 048 MB: bellek tükenir, çekirdek bir süreci öldürür (çoğu zaman PostgreSQL).
- Kanıt: Depoda havuz dosyası yok; sunucudaki `/etc/php/8.5/fpm/pool.d/www.conf` bu denetimde görülmedi.
- Etki: Yük altında (aynı akşam gönderilen büyük bir davetiye, eşzamanlı fotoğraf yüklemeleri) bellek baskısı. Bugün düşük olasılık.
- Neden önemli (öğretici not): Sabit bellekli bir makinede her bileşenin tavanı toplandığında makineyi aşmamalıdır; aşarsa hangi sürecin öleceğine çekirdek karar verir. Bütçe tablosu bu kararı sana geri verir.
- Öneri: `deploy/php-fpm/davetkart.conf`: `pm = dynamic`, `pm.max_children = 4`, `pm.max_requests = 500`; `deploy/php/davetkart.ini`'ye `opcache.memory_consumption`, `opcache.validate_timestamps=0` (dağıtım zaten `reload` yapıyor). Rehbere bellek tablosu: FPM, kuyruk, PostgreSQL (`shared_buffers`), işletim sistemi.
- Test önerisi: —
- Efor: S
- İlgili: Y5.2, Y6.2 · `YAYIN-PLANI.md` §6

### OPS-08 Günlüklerde istek kimliği yok
- Seviye: 🟢 Düşük
- Kanıt türü: KOD OKUMASI
- Nerede: `backend:config/logging.php` (satır biçimi, JSON biçimlendirici yok) · `backend:bootstrap/app.php` (istek kimliği üreten ara katman yok)
- Senaryo: Kullanıcı "ödeme sırasında hata aldım" der. Günlükte aynı dakikaya düşen onlarca satırdan hangilerinin o isteğe ait olduğu bulunamaz; kuyruğa giden iş ile onu doğuran istek eşlenemez.
- Kanıt: `grep -rnEi "X-Request-Id|correlation|shareContext|Context::add" app bootstrap config` → boş.
- Etki: Tanı süresi uzar. Kişisel veri günlüğe yazılmıyor (`02-security.md`, "Neler iyi" 9); bu iyi ve korunmalı.
- Neden önemli (öğretici not): Tek sunucuda bile bir kullanıcı eylemi birden çok günlük satırı ve bir kuyruk işi üretir. İstek kimliği bu parçaları bağlayan iptir; hata yanıtında kullanıcıya da verilirse destek "şu kodu söyleyin" diyebilir.
- Öneri: Ara katman: gelen `X-Request-Id` yoksa ULID üret, `Log::shareContext(['request_id' => …])`, yanıta başlık olarak ekle; hata zarfına `requestId` alanı (sözleşmeye bir satır). Kuyruk işlerinde `Context` ile taşı.
- Test önerisi: `HardeningTest::every_response_carries_a_request_id`.
- Efor: S
- İlgili: `docs/08-HATA-SOZLESMESI.md`

### OPS-09 Yatay ölçeğin önündeki tasarım kararları
- Seviye: 💡 Öneri
- Kanıt türü: KOD OKUMASI
- Nerede: `docs/10-URETIM-ENV-SABLONU.md` (`CACHE_STORE=file`, `QUEUE_CONNECTION=database`, `SESSION_DRIVER=file`) · `routes/console.php` (`onOneServer()`) · PostgreSQL uygulamayla aynı makinede
- Senaryo: İkinci bir uygulama sunucusu eklenirse: hız sınırı sayaçları sunucu başına tutulur (sınır ikiye katlanır), `onOneServer()` kilidi dosya cache'inde olduğu için zamanlanmış işler iki sunucuda da koşar, `withoutOverlapping()` aynı nedenle işlemez.
- Kanıt: Kod ve şablon okuması. Medya S3'te, oturum token tabanlı: bu ikisi engel değil.
- Etki: Bugün yok; tek sunucu için doğru ve bilinçli seçim (K80: "önce en düşük ortak payda").
- Neden önemli (öğretici not): Paylaşılan durum (sayaç, kilit, kuyruk) tek sunucuda dosyada durabilir; ikinci sunucu geldiği gün ağ üzerinden erişilen bir depoya taşınmak zorundadır. Bunu bilmek, taşımayı ihtiyaçtan önce yapmak anlamına gelmez.
- Öneri: Dokunma. `YAYIN-PLANI.md` §6'daki "ne zaman Lightsail'den çıkılır" eşiklerine ölçülebilir sayılar ekle (FPM kuyruğu, bellek, p95 yanıt süresi). İlk adım büyük olasılıkla PostgreSQL'i ayırmak, ikinci adım Redis (cache + kuyruk + kilit).
- Test önerisi: —
- Efor: L
- İlgili: K80 · `SEC-06` (IP anahtarlı hız sınırı)

## Tablolar

### Yayın adımları ↔ koddaki karşılıkları

Durum sütunu `YAYIN-PLANI.md` §8 kaydından alındı (son satır 26 Ekim 2026); canlı sistemde doğrulanmadı.

| Adım | Koddaki / depodaki karşılığı | Kod tarafı (bu denetim) | Plan kaydına göre durum |
|---|---|---|---|
| Y0.1 S3 paketi | `composer.json`: `league/flysystem-aws-s3-v3: 3.*` | ✅ var | ✅ |
| Y0.3 Nginx | `deploy/nginx/davetkart.conf` (108 satır) | ✅; güvenlik başlıkları eksik (`SEC-04`), `/videos/` önbelleği yok (`FE-09`) | ✅ (26 Ekim'de kuruldu) |
| Y0.4 Kuyruk servisi | `deploy/systemd/davetkart-queue.service` | ✅ | ✅ |
| Y0.5 Dağıtım betiği | `deploy/deploy.sh`, `deploy/deploy-frontend.sh` | ✅; bakım kipi yok (`OPS-06`) | ✅ (iki dağıtım yapıldı) |
| Y0.6 Kapılar yeşil | `composer check`, `npm run check` | ❌ denetlenen dalda `composer check` kırmızı (`TST-01`); `main` için koşmadı | backend ✅ (20 Ekim, `main`), frontend bekliyor |
| Y1–Y4 AWS, SES, S3, Lightsail | — (konsol işleri) | kapsam dışı | ✅; SES üretim erişimi (Y7.5) bekliyor |
| Y5–Y7 Sunucu, yığın, SSL | `deploy/php/davetkart.ini`, `deploy/sudoers/` | ✅; FPM havuzu depoda yok (`OPS-07`) | ✅ |
| Y8 Backend kurulumu | `docs/10-URETIM-ENV-SABLONU.md` | 🟡 şablon sapmış (`OPS-04`) | ✅ (26 Ekim, `/api/ping` yanıt verdi) |
| Y9 Arka plan işleri | `deploy/cron/davetkart`, `routes/console.php` | ✅ | ✅ |
| Y10 Frontend | `deploy/deploy-frontend.sh` | ✅ betik hazır; yayınlanacak commit belirsiz (`OPS-01`) | ⬜ kayıt yok |
| Y11.1–11.2 SES ve S3 denemesi | — | — | ⬜ |
| Y11.3 Sentry | `config/logging.php:129-131`, `sentryMonitor` | ✅ kod hazır, DSN boş | ⬜ (`OPS-03`) |
| Y11.5–11.6 Yedek ve prova | — (betik yok) | ❌ | ⬜ (`OPS-02`) |
| Y11.7 Dış izleme | `/api/ping` | 🟡 sığ (`OPS-03`) | ⬜ |
| Y12 Canlı doğrulama | `FAZ-*-ELLE-DOGRULAMA.md` | — | ⬜ |

### Dal durumu (`evidence/commands/OPS-branch-state.txt`)

| Depo | `main` | `release-v1.0` | Denetlenen dal | Fark | Premium şablon |
|---|---|---|---|---|---|
| Backend | `03d3940` (26 Ekim) | `03d3940` | `d810410` (5 Kasım) | denetlenen 4 ileride, 0 geride | `main` 13 · denetlenen 32 |
| Frontend | `47aedc8` (26 Ekim) | yok | `44caa49` (5 Kasım) | denetlenen 71 ileride, 1 geride | `main` 13 · denetlenen 32 |

Tutarlı çiftler: (`main`, `main`) ve (denetlenen, denetlenen). Tutarsız çift: frontend denetlenen + backend
`main` (`OPS-01`). Uzak dal sayısı: backend 24, frontend 42; etiket yok (`ARC-08`).

### Yayın öncesi kapı (bu denetimin bulgularından)

| Koşul | Bulgu | Durum |
|---|---|---|
| Yayınlanacak iki commit belli ve etiketli; backend önce | `OPS-01` | ❌ |
| `composer check` yeşil, `composer audit` temiz | `TST-01`, `SEC-07` | ❌ |
| Veritabanı yedeği + bir geri yükleme provası | `OPS-02` | ❌ |
| Hata izleme ve dış izleme açık | `OPS-03` | ❌ |
| Shopier `callback` kipi üretimde kapalı | `SEC-03` | ❌ |
| Frontend güvenlik başlıkları (Nginx) | `SEC-04` | ❌ |
| İki para etkili iş kuralı kapalı | `SEC-01`, `SEC-02` | ❌ |
| Fiyat sayfası metni gerçek kuralla aynı | `FE-52` | ❌ |
| SES üretim erişimi ve posta sürücüsü | Y7.5, `OPS-04` | ⬜ (plan kaydında bekliyor) |

## Regresyon

| # | Kaynak | Bulgu | Durum | Kanıt türü | Kanıt |
|---|---|---|---|---|---|
| R5 (Nginx / vekil tarafı) | Review §2.3 | `TrustProxies` / gerçek istemci IP'si | ✅ kapandı | KOD OKUMASI | Nginx ve PHP-FPM aynı makinede; `location = /index.php` `include fastcgi_params` ile `REMOTE_ADDR` doğrudan istemci (`deploy/nginx/davetkart.conf`); araya vekil yok, `TRUSTED_PROXIES` boş (`docs/10-URETIM-ENV-SABLONU.md:55-61`); `X-Forwarded-For` güvenilmediği için sahte başlıkla IP değiştirilemez. Uygulama tarafı `02-security.md` R5. Canlıda doğrulama Y12.3'te (koşmadı). İleride CDN ya da yük dengeleyici eklenirse `TRUSTED_PROXIES` doldurulmak zorunda |

## Kullanılan araçlar ve skill'ler / kullanılamayanlar

- Kullanılan: `git` (yalnızca okuma: `log`, `rev-list`, `show`, `branch -r`, `tag`), `grep`, dosya okuma.
- Skill: `superpowers:executing-plans`.
- Kullanılamayan / yapılmayan: canlı sunucuya ve AWS'ye erişim (yasak). `nginx -t`, `systemd-analyze verify`,
  `shellcheck` koşturulmadı (araçlar bu makinede yok; betikler okundu). Sunucudaki gerçek `.env`, FPM havuzu
  ve cron durumu görülmedi.

## Koşturulan komutlar

| Kanıt | Komut |
|---|---|
| `evidence/commands/OPS-branch-state.txt` | gerçek depolarda `git log -1`, `git rev-list --count`, `git show <ref>:<dosya> \| grep -c`, `git branch -r`, `git tag` |
| (dosyasız) ortam anahtarları | `grep -rhoE "env\('[A-Z0-9_]+'" config` (207 anahtar) ↔ `.env.example` (77) ↔ `docs/10` (65); uygulamaya özgü eksik: `AWS_URL` |
| (dosyasız) yedek betiği | `grep -rl pg_dump deploy docs/rehber/deploy` → boş |
| (dosyasız) FPM / OPcache | `grep -rnE "pm\.max_children\|opcache\." deploy docs/rehber/deploy docs/10-URETIM-ENV-SABLONU.md` → boş |
| (dosyasız) istek kimliği | `grep -rnEi "X-Request-Id\|correlation\|shareContext\|Context::add" app bootstrap config` → boş |

## İsmail'e sorular

1. **Yayın dalı (`OPS-01`):** Faz 15–17 ilk yayında olacak mı? Olacaksa iki depoyu `main`'e hangi sırayla
   alacağız; olmayacaksa frontend `main` (13 premium şablon) ile mi çıkılacak?
2. **Sunucudaki `.env` (`OPS-04`):** `MAIL_MAILER` bugün ne (`log` mu `ses` mi)? Değeri değil, yalnızca sürücü adını
   bilmek yeterli.
3. **Yedek (`OPS-02`):** `davetkart-backup-…` bucket'ı açıldı mı? Geri yükleme provasını birlikte yapalım mı?
4. **FPM havuzu (`OPS-07`):** sunucuda `pm.max_children` kaç? (`grep -E "^pm" /etc/php/8.5/fpm/pool.d/www.conf`)
5. **Alan adı (`OPS-05`):** otomatik yenileme 4 Ekim'den sonra açıldı mı?
