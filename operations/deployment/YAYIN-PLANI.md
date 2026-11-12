# YAYIN PLANI — DavetKart'ı AWS Lightsail'e Almak

> **Tarih:** 3 Ekim 2026
> **Mimari:** Yol A — Lightsail (İsmail onayladı, 3 Ekim 2026)
> **Bütçe kısıtı:** ~200 $ AWS kredisi, ~10 ay geçerli → hedef **ayda ≤ 15 $**
> **Başlangıç noktası:** backend `faz-10` dalı (`2e5b0e6`) · frontend `main`
> **Durum:** 🟡 YD-1…YD-4 kararlaştırıldı (3 Ekim 2026). YD-5 açık (deploy'u bloke etmiyor). **Sıradaki: Y3.2 son testi (`media.davetkart.com`, DNS yayılması bekleniyor) → Y3.3** · Devir: `YAYIN-DEVIR.md` · Y2.3 Y7'den sonraya taşındı · ⏰ Y1.4 (bütçe alarmları) Y4'ten sonraya ertelendi

---

## 0. Bu plan ne yapar, ne yapmaz

Faz 0-10 uygulamayı **yazdı**. Bu plan onu **çalıştırır**: bir sunucu, bir alan adı, bir
veritabanı, bir mail kanalı ve bir medya deposu. Yeni özellik yok.

**Yayına almak ≠ lansman.** Bu planın sonunda site `https://davetkart.com`'da çalışır.
Ancak gerçek müşteriye açılması için FAZ-10'un **Dilim G**'sinin (Shopier) bitmesi gerekir
(§7, lansman kapısı). Sıralama bilinçli: Shopier'in bildirim (callback) gönderebilmesi için
zaten **herkese açık bir HTTPS adresi** lazım. Deploy, Dilim G'yi beklemiyor; tersine
onun önünü açıyor.

> ⚠️ `claude.ai` üzerindeki eski **"DavetKart AWS Rehberi"** artifact'ında Yol B için
> *"Free Tier'ın ilk 12 ayı neredeyse ücretsiz"* yazıyor. **Bu, bu hesap için yanlış.**
> 15 Temmuz 2025'ten sonra açılan hesaplarda 12 aylık ücretsiz EC2/RDS yok, her hizmet
> krediden düşüyor. Bu plan, o rehberin Yol A bölümlerinin **yerine geçer**.

---

## 1. Hedef mimari

```
Kullanıcı ──► davetkart.com  (DNS: Natro · A → Lightsail statik IP · www → 301 apex)
                  │
   ┌──────────────▼───────────── Lightsail · Ubuntu 24.04 · 2 GB · Frankfurt ─────────────┐
   │ Nginx + Let's Encrypt                                                               │
   │   /            → frontend/dist  (SPA, try_files → index.html)                       │
   │   /api/*       → PHP 8.5-FPM → Laravel 13                                           │
   │ PostgreSQL 18  (yalnızca 127.0.0.1)                                                 │
   │ queue:work     (systemd servisi, Restart=always)                                    │
   │ schedule:run   (cron, dakikada bir)                                                 │
   └───────────┬───────────────────────────────┬─────────────────────────────┬───────────┘
               ▼                               ▼                             ▼
        S3: medya (galeri, LCV)        SES: parola sıfırlama         S3: gece pg_dump
                                        (Türkçe, K96)                (ayrı önek, ömür kuralı)
```

| İlke | Gerekçe |
|---|---|
| **Same-origin** (`/api` aynı alan adında) | CORS ve preflight yok. Frontend'in `VITE_API_BASE_URL=/api` varsayılanı zaten bunu bekliyor |
| **Sunucu yok edilebilir, veri değil** | Medya ve yedek S3'te. Sunucu bozulursa yeniden kurulur; misafirin fotoğrafı onunla gitmez |
| **Altyapı da kod** | Nginx, systemd ve deploy betiği `deploy/` klasöründe, git'te durur. Sunucuda elle yazılan config kaybolur ve bir dahaki kurulumda hatırlanmaz (B10) |
| **En az yetki** | Uygulamanın AWS anahtarı yalnızca bir bucket'a ve SES'e yetkili. Sunucunun GitHub anahtarı yalnızca okuma yetkili ve yalnızca kendi deposuna bağlı |
| **Önce en düşük ortak payda** (K80) | Redis yok, `database` kuyruğu + `file` cache. Yükseltme ölçüm gelince yapılır |

### Maliyet tahmini

| Kalem | Aylık |
|---|---|
| Lightsail 2 GB (2 vCPU, 60 GB SSD, 3 TB trafik, statik IP dahil) | 12 $ |
| Otomatik snapshot (7 gün) | ~1–3 $ |
| S3 (medya + yedek, ilk aylarda birkaç GB) | < 1 $ |
| SES (1.000 mail başına 0,10 $) | ~0 $ |
| **Toplam** | **~14–16 $ → 10 ayda ~150 $** |

---

## 2. Kararlar

### 2.1 Alındı (3 Ekim 2026, İsmail)

| # | Karar |
|---|---|
| **YD-1** ✅ | Sunucuda `git pull` + `deploy.sh`. GitHub Actions sonraya |
| **YD-2** ✅ (14 Ekim'de değişti) | Medya bucket'ı **tamamen kapalı**; dışarıya yalnızca **CloudFront (OAC)** üzerinden `https://media.davetkart.com` olarak açılır. CloudFront **Free** flat-rate planı (0 $, 1M istek, 100 GB/ay). Yedekler ayrı bucket'ta (Y11) |
| **YD-3** ✅ | Redis yok; `database` kuyruk + `file` cache (K80) |
| **YD-4** ✅ | SSH 22 herkese açık, yalnızca anahtarla; parola ve root girişi kapalı |

### 2.2 Önerilerle ilk tablo (kayıt için)

| # | Soru | Öneri | Bloke ettiği aşama |
|---|---|---|---|
| **YD-1** | Kod sunucuya nasıl gider? (a) sunucuda `git pull` + `deploy.sh` (b) GitHub Actions ile otomatik | **(a)**. Önce elle tekrarlanabilir bir betik, otomasyon sonra. Otomatikleştirilen şey önce anlaşılmış olmalı | Y0, Y8 |
| **YD-2** | Medya S3'te nasıl görünür? (a) nesneler herkese açık okunur (bucket policy, yalnızca `media/` öneki) (b) bucket kapalı + süreli imzalı URL | **(a)**. Mevcut kod (`->url()`) ve frontend'in ETag/koşullu GET önbelleği kalıcı URL varsayıyor. Yollar ULID, yani tahmin edilemez. (b) kodu ve önbelleği değiştirir, ayrı bir iş. KVKK metnine *"bağlantıya sahip olan görebilir"* notu düşülür | Y3 |
| **YD-3** | Redis kurulsun mu? | **Hayır**. 2 GB RAM'de PHP-FPM + PostgreSQL + Argon2id (girişte 64 MB) zaten paylaşılıyor. K80'in `database`/`file` varsayılanları yeterli. Ölçüm gelince yükseltilir | Y6 |
| **YD-4** | SSH (22) herkese mi açık, yalnızca senin IP'ne mi? | **Herkese açık + yalnızca anahtar, parola ve root girişi kapalı**. Ev IP'n değişken; IP kısıtlaması seni dışarıda bırakır. Lightsail tarayıcı konsolu yedek kapı | Y4 |
| **YD-5** | Shopier bitene kadar sitede ödeme nasıl görünür? (a) kapalı beta: kayıt açık, yayınlama yok (b) yalnızca Havale/EFT (elle onay) (c) site hiç duyurulmaz | Senin ticari kararın. **Deploy'u bloke etmez**, yalnızca §7'yi bloke eder | Lansman |

---

## 3. Aşamalar

Ritim değişmedi: **1 cevap = 1 adım**. Komutları sen çalıştırırsın, ben gerekçeyi anlatırım,
sonucu görünce sıradakine geçeriz. 🖥️ = senin makinen · ☁️ = AWS konsolu · 🐧 = sunucu (SSH) · 🌐 = Natro

### Y0 — Kod tarafı hazırlık 🖥️ (sunucuya dokunmadan önce)

| # | İş | Neden |
|---|---|---|
| **Y0.1** | `composer require league/flysystem-aws-s3-v3` (backend) | Laravel'in `s3` diski bu paket olmadan çalışmaz; `DAVETKART_MEDIA_DISK=s3` ilk yüklemede patlar. Paket `aws/aws-sdk-php`'yi de getirir, böylece `MAIL_MAILER=ses` ek paket istemez (K95) |
| **Y0.2** | Frontend çalışma ağacı: 617 değişikliğin gerçeği (CRLF mi, gerçek iş mi?) + `.gitattributes` (10.81) | Sunucu **git'ten** çeker. Commit'lenmemiş hiçbir şey canlıya çıkmaz; yalnızca sende çalışan bir site en kötü sürpriz |
| **Y0.3** | `deploy/nginx/davetkart.conf` | Same-origin yönlendirme, `client_max_body_size 30m` (docs/10 Faz 9 §2), SPA geri dönüşü, hash'li dosyalar için `immutable` önbellek, `.env` ve gizli dosyalara erişim yasağı |
| **Y0.4** | `deploy/systemd/davetkart-queue.service` | Kuyruk işçisi: `Restart=always`, `--max-time=3600` (bellek sızıntısına karşı periyodik yeniden doğum) |
| **Y0.5** | `deploy/deploy.sh` | Tekrarlanabilir sıra: `git pull` → `composer install --no-dev -o` → `migrate --force` → `config:cache` + `route:cache` → `chmod 640` → `php-fpm reload` → `queue:restart`. Her adım hata verirse durur (`set -euo pipefail`) |
| **Y0.6** | `composer check` + `npm run check` yeşil, iki depoda da commit + push | Canlıya çıkan şey doğrulanmış bir commit olmalı (B7) |

### Y1 — AWS hesabının güvenliği ☁️

| # | İş | Neden |
|---|---|---|
| **Y1.1** | Root hesapta MFA | Root anahtarı çalınırsa hesap ve kredi gider. Root bundan sonra **kullanılmaz** |
| **Y1.2** | IAM Identity Center (ya da IAM) yönetici kullanıcısı + MFA | Günlük iş için. Root ile çalışmak, her gün kasanın anahtarını cepte taşımaktır |
| **Y1.3** | Billing → Credits: bitiş tarihi + **kapsadığı hizmetler** (Lightsail, S3, SES) | Kredinin Lightsail'i kapsamadığını ilk faturada öğrenmek istemeyiz |
| **Y1.4** | AWS Budgets: aylık 15 $ bütçe, %80 ve %100 e-posta uyarısı + **kredi bitiş** hatırlatması | Kredi bitince kart sessizce çekilmeye başlar. Uyarı, sürprizi faturadan önceye çeker |
| **Y1.5** | Varsayılan bölge: `eu-central-1` (Frankfurt) | Türkiye'ye en yakın büyük bölge, SES burada var. KVKK: veri yurt dışında, aydınlatma metnine girer (K14) |

### Y2 — SES (en erken başlat, onay beklemesi var) ☁️ 🌐

| # | İş | Neden |
|---|---|---|
| **Y2.1** | SES → domain identity `davetkart.com`, Easy DKIM (2048 bit) | Alan adını doğrulamak, `bilgi@davetkart.com` gibi her adresten gönderebilmek demek |
| **Y2.2** | Natro DNS: 3 DKIM CNAME + DMARC TXT (`p=none` ile başla). SPF'e **dokunulmaz** (özel MAIL FROM yok) | DKIM yoksa mail spam'e düşer; DMARC `none` önce izle, sonra sıkılaştır |
| **Y2.3** → **Y7.5'e taşındı** | Production access talebi | Bkz. Y7.5 |

### Y3 — S3 ve uygulama kimliği ☁️

| # | İş | Neden |
|---|---|---|
| **Y3.1** | Bucket `davetkart-prod-…` (eu-central-1), sürümleme **açık**, şifreleme varsayılan (SSE-S3) | Sürümleme: yanlışlıkla silinen dosya geri alınabilir |
| **Y3.2** | CloudFront dağıtımı (Free plan) + OAC + ACM sertifikası (`media.davetkart.com`, us-east-1) + Natro CNAME'leri. Bucket'ın Block Public Access'i 4/4 **hiç açılmaz** | Bucket'a yalnızca CloudFront erişir; yanlış bucket politikasıyla veri sızma riski yok. Ayrıntı §8 |
| **Y3.3** | Ömür (lifecycle) kuralları: `backups/` 30 gün · eski sürümler 30 gün | Yedekler ve eski sürümler sonsuza kadar birikip fatura büyütmesin |
| **Y3.4** | IAM kullanıcısı `davetkart-app`: yalnızca bu bucket'ta `Get/Put/DeleteObject` + `ses:SendRawEmail`; erişim anahtarı | Lightsail'de EC2 gibi "instance rolü" yok, bu yüzden anahtar zorunlu. Sızarsa zarar bu iki yetkiyle sınırlı kalır |

### Y4 — Lightsail sunucusu ☁️

| # | İş | Neden |
|---|---|---|
| **Y4.1** | Instance: Ubuntu 24.04 LTS, 2 GB plan, Frankfurt, **kendi SSH anahtarın** | LTS = 2029'a kadar güvenlik güncellemesi. 1 GB plan Argon2id + Postgres + Vite build'e dar gelir |
| **Y4.2** | Statik IP ata | Instance yeniden başlarsa IP değişmesin, DNS kırılmasın. Bağlıyken ücretsiz |
| **Y4.3** | Firewall: 22, 80, 443 (YD-4) · IPv6 için aynısı | Postgres (5432) **asla** dışarı açılmaz |
| **Y4.4** | Otomatik günlük snapshot (7 gün saklama) | Felaket kurtarmanın ilk katmanı (ikincisi Y11'de) |
| **Y4.5** ⏰ | **Ertelenen Y1.4: iki bütçe alarmı** (aşağıdaki §8 notuna bak) | İsmail'in isteğiyle sunucu kurulduktan sonraya alındı (4 Ekim 2026) |

### Y5 — Sunucu temeli 🐧

| # | İş | Neden |
|---|---|---|
| **Y5.1** | `apt update && upgrade`, `unattended-upgrades` | Güvenlik yamaları sen uyurken de gelsin |
| **Y5.2** | 2 GB swap dosyası | 2 GB RAM'de `npm run build` ya da büyük görsel küçültme (512M, Faz 9) anlık taşabilir; swap yoksa OOM killer Postgres'i öldürebilir |
| **Y5.3** | `deploy` kullanıcısı, SSH: parola ve root girişi kapalı | Saldırgan önce `root`'u dener; yoksa ilk kapı kapanır |
| **Y5.4** | Sunucu saat dilimi UTC + **saat eşitleme açık** (`timedatectl` → `System clock synchronized: yes`, `NTP service: active`) | Uygulama saat dilimini kendisi yönetiyor (K71). Saat kayarsa AWS imzaları (SigV4, ±5 dk) reddedilir: SES/S3 çağrıları düşer; Sanctum süreleri ve zamanlanmış işler kayar. 14 Ekim'de İsmail'in PC'sindeki 3 saatlik kayma S3 yüklemesini 'Signature expired' ile bozdu |

### Y6 — Yazılım yığını 🐧

| # | İş | Neden |
|---|---|---|
| **Y6.1** | PHP 8.5 (`ppa:ondrej/php`): `fpm cli pgsql gd exif mbstring xml curl zip intl bcmath` | K87 `^8.5`; Ubuntu'nun kendi deposunda yok. `pdo_pgsql` composer.json'da yazmıyor ama zorunlu (10.79) |
| **Y6.2** | `php.ini` (fpm + cli): `upload_max_filesize=25M`, `post_max_size=30M`, `memory_limit`, OPcache açık | Faz 9: aşılırsa sebepsiz 422 |
| **Y6.3** | Argon2id ölçümü (docs/10 komutu) → `ARGON_*` | Hedef ~250 ms. Bu donanımda ilk kez ölçülüyor (K32) |
| **Y6.4** | PostgreSQL 18 (PGDG apt), `davetkart` rolü + veritabanı, güçlü parola, yalnızca localhost | K19: geliştirmeyle aynı ana sürüm |
| **Y6.5** | Nginx, Composer, Node **24 LTS** (yalnızca build için; plandan sapma, bkz. Y6.5c) | — |

### Y7 — Alan adı ve SSL 🌐 🐧

| # | İş | Neden |
|---|---|---|
| **Y7.1** | Natro: `@` A → statik IP · `www` A (ya da CNAME) → aynı · varsa eski AAAA/A kayıtlarını temizle | Natro'nun park sayfası kaydı kalırsa trafiğin yarısı oraya gider |
| **Y7.2** | Yayılmayı doğrula (`nslookup`), sonra `certbot --nginx -d davetkart.com -d www.davetkart.com` | Let's Encrypt, DNS doğru yeri göstermeden sertifika vermez |
| **Y7.3** | `www` → `https://davetkart.com` 301 · `http` → `https` 301 | Tek kanonik adres: SEO, çerez ve `CORS_ALLOWED_ORIGINS` tek değer |
| **Y7.5** 🆕 ↪️ **Y10 sonrasına taşındı (26 Ekim)** | **SES production access talebi** (eski Y2.3). Form metni birlikte yazılır: transactional, parola sıfırlama, bounce/şikâyet yönetimi | 4 Ekim kararı: park edilmiş alan adından gelen talep reddedilme riski taşır; site canlıyken gönderilir. Sandbox (doğrulanmış Gmail'e 200/gün) deploy testleri için yeterli |
| **Y7.4** | HSTS'yi **Laravel mi Nginx mi** basıyor? İkisi birden değil (HardeningTest) | Çift başlık zararsız görünür ama farklı `max-age` çakışır |

### Y8 — Backend'in ilk kurulumu 🐧

| # | İş | Neden |
|---|---|---|
| **Y8.1** | GitHub **deploy key** (yalnızca okuma, yalnızca bu depo) → `git clone` | Kişisel token sunucuda durursa tüm depolarına erişim sızar |
| **Y8.2** | `.env` ← `docs/10` şablonu. Sırlar doldurulur, `chmod 600` | Şablonun her satırı bir gerekçe taşıyor; bu adımda tek tek üzerinden geçeriz |
| **Y8.3** | `key:generate` → `migrate --force` → `config:cache` → `route:cache` → `chmod 640 bootstrap/cache/config.php` | Sıra önemli: `config:cache`'ten sonra `.env` okunmaz (docs/10) |
| **Y8.4** | İzinler: `storage/` ve `bootstrap/cache/` yalnızca `www-data` grubu yazabilir | Kodun geri kalanı web sunucusu tarafından **değiştirilemez** olmalı |

### Y9 — Arka plan işleri 🐧

| # | İş | Neden |
|---|---|---|
| **Y9.1** | `davetkart-queue.service` (Y0.4) → `systemctl enable --now` | Parola sıfırlama maili ve görsel küçültme kuyruktan gider. İşçi yoksa **mail hiç gitmez**, hata da vermez |
| **Y9.2** | Cron: `* * * * * php artisan schedule:run` | `orders:expire`, `media:prune-orphans`, `sanctum:prune-expired`, `data:purge` (KVKK, K98) |
| **Y9.3** | `schedule:list` + `systemctl status` ile doğrula | — |

### Y10 — Frontend 🐧

| # | İş | Neden |
|---|---|---|
| **Y10.1** | Deploy key ile clone, `.env.production` (`VITE_API_BASE_URL=/api`, Havale/EFT değerleri YD-5'e göre) | `VITE_` değerleri derlemeye gömülür; değişirse **yeniden build** gerekir |
| **Y10.2** | `npm ci && npm run build` → Nginx kökü `dist/` | `npm ci`: kilit dosyasına birebir uyar, `install` gibi sürüm kaydırmaz |
| **Y10.3** | `deploy.sh`'a frontend adımı | Tek komutla iki taraf birlikte güncellenir |

### Y11 — Entegrasyonlar ve yedekleme 🐧 ☁️

| # | İş | Neden |
|---|---|---|
| **Y11.1** | SES: canlıda parola sıfırlama uçtan uca + `mail-tester.com` puanı | Spam klasörüne düşen sıfırlama maili, gelmeyen mailden farksızdır |
| **Y11.2** | S3: galeriye foto yükle → URL S3'ten geliyor, küçültme işi koştu | — |
| **Y11.3** | Sentry DSN + `LOG_STACK=daily,sentry` (10.55b) + Crons izleyicileri | Zamanlanmış iş sessizce durursa haberimiz olsun |
| **Y11.4** | Gemini üretim anahtarı + ilk gün gerçek soru (10.56) | Google 2.5 erişimini kısıtlayabiliyor |
| **Y11.5** | Gece `pg_dump` → `s3://…/backups/` (cron) | Snapshot tüm diski geri alır; `pg_dump` **tek bir tabloyu** ya da dünkü veriyi geri getirebilir. İki katman, iki farklı felaket |
| **Y11.6** | **Geri yükleme provası**: dünkü dump'ı yerelde aç | Denenmemiş yedek, yedek değildir |
| **Y11.7** | Dışarıdan çalışma izleme (UptimeRobot, ücretsiz) + Lightsail CPU/durum alarmı | Site düştüğünde bunu müşteriden önce öğrenmek |

### Y12 — Canlı doğrulama

| # | Kontrol |
|---|---|
| **Y12.1** | `APP_DEBUG=false` · `https://davetkart.com/.env` → 404 · hata yanıtında `debug` bloğu yok |
| **Y12.2** | SSL Labs notu A · güvenlik başlıkları |
| **Y12.3** | Hız sınırı **gerçek istemci IP'siyle** çalışıyor (`TRUSTED_PROXIES` boş, araya proxy yok) |
| **Y12.4** | FAZ-10 elle doğrulama betikleri (10.83) canlıda: kayıt → davetiye → yayınla → misafir LCV + foto |
| **Y12.5** | Büyük dosya: 14 MB foto 201, 16 MB foto 422 (Nginx değil Laravel cevaplıyor) |

---

## 4. Sıra ve bağımlılıklar

```
Y0 (kod hazırlığı) ─────────────────────────────────────────┐
Y1 (hesap) ──► Y2 (SES, beklemeye başlar) ──────────────┐   │
          └──► Y3 (S3 + IAM) ──────────────────────┐    │   │
          └──► Y4 (Lightsail) ──► Y5 ──► Y6 ──► Y7 ┴─► Y8 ┴─► Y9 ──► Y10 ──► Y11 ──► Y12
```

Y0 ile Y1–Y2 paralel yürüyebilir: SES onayını beklerken sunucuyu kurarız.

---

## 5. Bu planın tuzakları (baştan bil)

| # | Tuzak | Nerede |
|---|---|---|
| 1 | `.env` değiştirip `config:cache`'i unutmak: değişiklik **sessizce** uygulanmaz | Y8, her deploy |
| 2 | Kuyruk işçisi eski kodu bellekte tutar: deploy sonrası `queue:restart` yoksa yeni kod **yarım** çalışır | Y0.5 |
| 3 | Nginx'in 1 MB gövde sınırı: Laravel log'unda iz bırakmadan 413 | Y0.3 |
| 4 | SES sandbox: kendi adresine giden test maili çalışır, gerçek kullanıcıya gitmez. *"Bende çalışıyor"* yanılgısı | Y2.3 |
| 5 | Lightsail firewall IPv4 ve IPv6 için **ayrı**: biri açık unutulur | Y4.3 |
| 6 | Natro'da eski A kaydı kalırsa sertifika alınamaz ya da trafik bölünür | Y7.1 |
| 7 | Kredi bitiş tarihi geçince fatura karta düşer; Budgets kurulmadıysa ilk haber ekstreden gelir | Y1.4 |
| 8 | `PAYMENT_PROVIDER=fake` canlıda para almaz ama webhook sırrı zayıfsa sahte `paid` üretilebilir: sırrı **uzun ve rastgele** üret | Y8.2 |

---

## 6. Ne zaman Lightsail'den çıkılır?

Bugün değil, ama işaretleri bilmek mimari vizyonun parçası:

- CPU sürekli %50 üstü ya da RAM swap'a sürekli düşüyor → önce **4 GB plana yükselt** (snapshot'tan yeni instance, 5 dakika)
- Veritabanı uygulamayla RAM için kavga ediyor → Postgres'i **Lightsail Managed DB** ya da RDS'e taşı (`pg_dump` + `DB_HOST`)
- İki sunucu gerekiyor → Load balancer + Redis (cache/kuyruk/oturum paylaşılmalı) + `onOneServer` zaten hazır (10.44)

Medya S3'te ve config `.env`'de olduğu için bu geçişlerin hiçbiri kod değişikliği istemiyor.

---

## 7. Lansman kapısı (bu planın dışında, ama bağlı)

Site Y12'den sonra çalışır; **müşteriye açılması** için:

- [ ] FAZ-10 Dilim G (Shopier) ya da YD-5 kararı
- [ ] KVKK aydınlatma metni: veri Frankfurt'ta (yurt dışı aktarım), medya bağlantısı paylaşılabilir (YD-2)
- [ ] FAZ-10 Dilim Z kapanışı

---

## 8. İlerleme kaydı

*(Her adım bittikçe buraya işlenir.)*

| Adım | Tarih | Durum | Not |
|---|---|---|---|
| Y1.1 | 3 Ekim | ✅ | Root MFA |
| Y1.2 | 3–4 Ekim | ✅ | Fatura erişimi açık · `Admins` grubu (`AdministratorAccess`, ilk denemede politika eksikti, düzeltildi) · `ismail-admin` + MFA · hesap takma adı `davetkart` |
| Y1.3 | 4 Ekim | 🟡 | Hesap **ücretli planda** (ücretsiz planın 6 ayda hesabı kapatma riski yok). Kredi tutarı ve bitiş tarihi henüz yazılmadı |
| Y1.4 | — | ⏰ **Ertelendi → Y4.5** | Sunucu kurulduktan sonra yapılacak |
| Y1.5 | 4 Ekim | ✅ | Konsol varsayılan bölgesi Frankfurt (Unified Settings). Ek bölge açılmadı |
| Y2.1 | 4 Ekim | ✅ | SES Frankfurt: Gmail kimliği doğrulandı · `davetkart.com` kimliği (Easy DKIM, RSA 2048) · Essentials planı iptal → **à la carte** (0,10 $/1.000) · VDM/dedicated IP/kiracı yok · sandbox: 200 mail/gün, 1/sn |
| Y2.2 | 4 Ekim | ✅ Doğrulandı | Natro'ya 3 DKIM CNAME + `_dmarc` TXT (`p=none`). Mevcut kayıtlara dokunulmadı. **SPF değişmedi**: özel MAIL FROM yok → SPF `amazonses.com` için kontrol edilir, DMARC uyumu DKIM'den gelir |

### 📅 Süre takvimi (tek hata noktaları)

| Ne | Bitiş | Not |
|---|---|---|
| **Alan adı** `davetkart.com` (Natro) | 11 Eylül 2027 | 🔴 Otomatik yenileme KAPALI (4 Ekim). Biterse site + mail + SSL aynı gün düşer |
| **Natro mail hosting** (Standart, 250 MB, 1 hesap) | **11 Ocak 2027** | Alan adından AYRI bir hizmet, 4 aylık dönemle başlamış. Yenileme 5,88 $/yıl. Karar: yenile ya da Zoho'ya taşı — 11 Aralık'a kadar |
| AWS kredisi | ~10 ay (tarih Y4.5'te yazılacak) | Bitince aylık ~15 $ karta |

| Y2.3 | 4 Ekim | ↪️ **Y7.5'e taşındı** | Plan sapması (İsmail onayladı) |
| Y2.x | 4 Ekim | ✅ | SES test maili `bilgi@davetkart.com` → Gmail gelen kutusu (spam değil). Natro'da `bilgi@` kutusu |
| Y3.1 | 4 Ekim | ✅ | `davetkart-media-438641` (Frankfurt, ACL kapalı, Block Public Access 4/4 açık, sürümleme açık, SSE-S3 + Bucket Key). **İki bucket kararı**: yedekler Y11'de ayrı `davetkart-backup-…` bucket'ında (kusur yalıtımı) |

| Y3.2a | 14 Ekim | ✅ | CloudFront `davetkart-media` (`E3OV6EN5B6X9YB`, `d252jqf124chfh.cloudfront.net`), **Free plan**, origin REST uç noktası, OAC. Bucket politikası CloudFront'un kendisi tarafından yazıldı (`cloudfront.amazonaws.com`, `s3:GetObject`, `ArnLike AWS:SourceArn` = bu dağıtım). Block Public Access 4/4 açık kaldı. Test yüklemesi önce PC saati 3 saat kayık olduğu için `Signature expired` verdi; saat düzeltilince geçti |

| Y3.2b | 14–15 Ekim | ✅ | ACM sertifikası `media.davetkart.com` (us-east-1, `50b28409-841a-4919-8d97-2d3479b754d7`, Amazon, joker yok) DNS ile doğrulandı · CloudFront'a alternate domain + sertifika eklendi, güvenlik politikası `TLSv1.2_2021` · Natro'ya `media` CNAME → `d252jqf124chfh.cloudfront.net` eklendi. **15 Ekim 00:13:** `https://media.davetkart.com/test.jpg` açıldı ✅. **Kalan:** S3'ten `test.jpg` silinir |

### ▶️ Y3.2: `media.davetkart.com` (CloudFront + OAC) — 14 Ekim'de öne alındı

4 Ekim'de yayın sonrasına bırakılmıştı; 14 Ekim'de İsmail şimdi yapmaya karar verdi. Böylece geçici 'herkese açık bucket' aşaması hiç yaşanmıyor. Hedef: medya `https://media.davetkart.com/…` adresinden, bucket **tamamen kapalı**, yalnızca CloudFront (OAC) okur. Adımlar: ACM sertifikası (**us-east-1**, CloudFront için zorunlu) + Natro'da doğrulama CNAME'i → CloudFront dağıtımı + OAC → bucket politikasını OAC'ye çevir, herkese açık okuma iznini kaldır, Block Public Access'i 4/4 geri kilitle → Natro'da `media` CNAME → `.env` `AWS_URL=https://media.davetkart.com` + `config:cache`. **Kod ve veri göçü yok**: `media` satırları URL değil `disk`+`path` saklıyor (K54), URL okuma anında `AWS_URL`'den üretiliyor. HSTS `includeSubDomains` gönderildiği için alt alan adı HTTPS'siz çalışamaz.

### 🌐 Natro DNS'in durumu (4 Ekim 2026)

| Kayıt | Sahibi | Y7'de |
|---|---|---|
| A `@` → 85.159.66.93 · CNAME `www` → redirect.natrocdn.com | Natro park/yönlendirme | **Değişecek** (Lightsail IP) |
| MX ×2 `mx-0{1,2}.kurumsaleposta.com` · CNAME `autodiscover` · SRV `_autodiscover._tcp` · TXT `ntr._domainkey` · TXT SPF | Natro mail hosting | 🔒 Dokunulmaz |
| 3× CNAME `…._domainkey` → `….dkim.amazonses.com` · TXT `_dmarc` | SES (Y2.2) | 🔒 Dokunulmaz |
| CNAME `_db41d753218f08f2eb5dde52ca1afac5.media` → `…acm-validations.aws` | ACM sertifika doğrulaması (Y3.2, 14 Ekim) | 🔒 **Asla silinmez**: ACM her otomatik yenilemede bu kayda bakar |
| CNAME `media` → `d252jqf124chfh.cloudfront.net` | CloudFront medya dağıtımı (Y3.2, 15 Ekim) | 🔒 Dokunulmaz |

### ⏰ Y1.4 hatırlatması (Y4.5'te yapılacak)

**Tuzak:** AWS Budgets varsayılan olarak kredileri maliyetten düşer (`IncludeCredit=true`). Kredi bitene kadar harcama 0 $ görünür ve alarm hiç çalmaz.

1. **`davetkart-aylik-harcama`**: Maliyet bütçesi · Aylık · Yinelenen · Sabit 15 $ · Tüm hizmetler · **Gelişmiş seçenekler → Krediler işaretini KALDIR** · eşikler: %80 Gerçekleşen, %100 Gerçekleşen, %100 Tahmini
2. **`davetkart-kart-cekimi`**: aynı ama 1 $, krediler **dahil** (dokunma) · tek eşik: %100 Gerçekleşen → kart çekildiği anda mail
3. Krediler sayfasından **kalan tutar + bitiş tarihi** → plana yaz · telefon takvimine bitişten 1 ay önceye hatırlatıcı

| Y3.2c | 15 Ekim | ✅ | `media.davetkart.com/test.jpg` açıldı; `test.jpg` S3'ten silindi (delete marker; eski sürümü Y3.3 kuralı temizler) |
| Y3.3 | 15 Ekim | ✅ | Ömür kuralı `eski-surumleri-sil`, tüm bucket: noncurrent sürümler 7 gün sonra kalıcı silinir (plandaki 30 gün yerine 7, KVKK/`data:purge` gerekçesiyle) · süresi dolmuş delete marker'lar silinir · tamamlanmamış multipart 7 gün |
| Y3.4 | 15 Ekim | ✅ | IAM `davetkart-app` (konsol erişimi yok) · satır içi politika `davetkart-app-medya-ve-mail` (Get/Put/DeleteObject + ListBucket + ses:SendEmail/SendRawEmail; `DeleteObjectVersion` bilerek yok) · erişim anahtarı `lightsail-prod-davetkart` parola yöneticisinde. Y7.5'te SES kaynağı `davetkart.com` kimliğine daraltılacak |
| Y0.1 | 19–20 Ekim | ✅ | `league/flysystem-aws-s3-v3` `3.*` → 3.35.3 (aws-sdk-php 3.401.3 ile gelir). 🪤 Windows tuzağı: `composer.bat` `^` karakterini siler, `^3.0` → `3.0` (3.0.0'a sabitlenir). Kısıtta `^` yerine `3.*` kullan. Commit henüz atılmadı (Y0.6) |
| Y0.2 | 20 Ekim | ✅ | `composer audit` uyarısı (symfony/http-foundation, CVE-2026-108082 ReDoS) → `composer update symfony/http-foundation` v8.1.1 → v8.1.9, audit temiz. Önce `--dry-run` ile yalnızca 1 paket etkilendiği doğrulandı |
| Y0.3 | 20 Ekim | ✅ | `deploy/nginx/davetkart.conf` + `docs/rehber/deploy/nginx/davetkart.md` yazıldı (backend deposu). `nginx -t` ile test edilmedi, Y7'de denenecek. Varsayımlar: `/var/www/davetkart/{backend,frontend/dist}`, `/run/php/php8.5-fpm.sock` |
| Y0.4 | 20 Ekim | ✅ | `deploy/systemd/davetkart-queue.service` + rehber. `User=www-data`, `Restart=always`, `--tries=3 --timeout=60 --max-time=3600` (timeout < `retry_after` 90), `MemoryMax=768M`. Sunucuda denenmedi (Y9.1) |
| Y0.5 | 20 Ekim | ✅ | `deploy/deploy.sh` + rehber. **Sapma (onaylandı):** `config:cache`/`route:cache` artık `migrate`'ten ÖNCE. `artisan` hep `sudo -u www-data`. Y8.2'de `.env` izni `600` değil `deploy:www-data 640` olacak. Sunucuda denenmedi |
| Y0.6 (backend) | 20 Ekim | ✅ | Backend commit'lendi ve push'landı, çalışma ağacı temiz. Dal: `release-2026-10-20` (Y8'de clone edilecek dal bu ya da main'e birleşmiş hâli). **Frontend Y0.6 bekliyor:** 617 commit'lenmemiş değişiklik, `.gitattributes` kararı (10.81) |
| Y4.1 | 25 Ekim | ✅ | Lightsail `davetkart-prod`: Ubuntu 24.04 LTS (OS Only), 2 GB RAM / 2 vCPU / 60 GB SSD, Frankfurt Zone A (`eu-central-1a`), Dual-stack. Kendi SSH anahtarı: yerelde üretilen ed25519, Lightsail'e **yalnızca `.pub`** yüklendi, anahtar adı `davetkart_lightsail` (özel anahtar `%USERPROFILE%\.ssh\davetkart_lightsail`, parolalı, yedek parola yöneticisinde). Kullanıcı adı `ubuntu`. Lightsail "PHP update recommended" (CVE-2026-109618/109619) uyarısı genel bildirim, instance'ta PHP yok → **Y6'da kurulan PHP sürümünün yamalı olduğu kontrol edilecek** |
| Y4.2 | 25 Ekim | ✅ | Statik IP `StaticIp-1` = **3.74.92.172**, `davetkart-prod`'a bağlı (Lightsail kaynakları yeniden adlandırılamıyor). Y7'de Natro A kaydı bu IP olacak |
| Y4.3 | 25 Ekim | ✅ | Firewall: HTTP 80, SSH 22, HTTPS 443 (üçü de IPv4+IPv6). 🪤 Bu konsolda IPv4/IPv6 ayrı liste değil; **kuralın içinde iki kaynak satırı** var (`0.0.0.0/0` ve `::/0`); HTTPS eklenirken ikinci satır elle eklendi. Postgres (5432) açık değil |
| Y4.4 | 25 Ekim | ✅ | Otomatik günlük snapshot açık, saat **04:00 (GMT+3)** = 01:00 UTC; Lightsail son 7'yi tutar. `pg_dump` (Y11) 02:00'de çalışacak, çakışmasın |
| Y4.5 | 25 Ekim | ✅ | Bütçe 1: `davetkart-aylik-harcama` · 15 $ aylık · **Credit/Refund dahil DEĞİL** (ham harcama) · uyarılar: %85 gerçek, %100 tahmini, %100 gerçek. Bütçe 2: `davetkart-kart-cekimi` · 1 $ aylık · krediler dahil (net maliyet) · %100 gerçek. 📌 30 Eylül 2026 sonrası eklenen alıcılar e-postayı **doğrulamalı**, yoksa bildirim gitmez. Kalan: Billing → Credits (Y1.3) kalan tutar/bitiş/kapsam |
| Y1.3 | 25 Ekim | 🟡 | **Kredi:** 140 $ kazanılmış (100 $ Free Tier + 20 $ Explore AWS EC2 + 20 $ Explore AWS Budgets), kalan **136,51 $**, hepsi **25.07.2027**'de bitiyor (önceki "200 $" ulaşılabilir toplam: 3 Explore AWS etkinliği daha = +60 $, büyük olasılıkla aynı tarihte biter → güvenlik payı, runway uzatmaz). ~15 $/ay × 9 ay ≈ kalan kredi. **Açık:** Lightsail'in kredi kapsamında olduğu henüz doğrulanmadı (kullanım gecikmeli yansır) → **26 Ekim'de Credits → kullanım geçmişinde Lightsail ara**; yoksa `davetkart-kart-cekimi` alarmı ele verir. 📅 Takvim: **25 Haziran 2027** "kredi 25 Temmuz'da bitiyor" |
| Y1.3c | 25 Ekim | ✅ | Kullanım geçmişinde Temmuz'dan beri yalnızca AmazonEC2 (~1,60 $/ay): Temmuz'daki deneme `web-server` (t3.micro, us-east-1d). İsmail sonlandırdı. us-east-1 EC2 panosu: çalışan 0, birim 0, anlık görüntü 0, esnek IP 0, yük dengeleyici 0 (kalan: 1 anahtar çifti, 2 güvenlik grubu, ücretsiz). ⚠️ us-east-1'de **ACM sertifikası `media.davetkart.com` yaşıyor, silinmez**. **2 Kasım'da** EC2 kullanımının durduğu Credits geçmişinden doğrulanacak |
| Y4.2b / Y5.0 | 25 Ekim | ✅ | ⚠️ **Statik IP değişti:** İsmail yeni bir statik IP oluşturup bağladı → güncel adres **63.182.93.247** (eski `StaticIp-1` = 3.74.92.172 artık geçersiz; hesapta tek statik IP olduğu İsmail tarafından bildirildi). **Y7'de Natro A kaydı 63.182.93.247 olacak.** İlk SSH başarılı: `ssh -i %USERPROFILE%\.ssh\davetkart_lightsail ubuntu@63.182.93.247` · Ubuntu 24.04.4 LTS, 1,9 GiB RAM, 58 GB disk, swap 0 (Y5.2), özel IP 172.26.3.131 · ED25519 host parmak izi `SHA256:8EedTE2LQLfqkBnHQEPc2gzj/DtibmAiFx7tJ/fNfdE` |
| Y5.1 | 25 Ekim | ✅ | `apt update && upgrade`; `unattended-upgrades` zaten açık (`20auto-upgrades` iki satır "1", servis `enabled`); kernel güncellemesi için kontrollü `reboot` yapıldı, sonra `reboot-required` yok |
| Y5.2 | 25 Ekim | ✅ | 2 GB `/swapfile` (chmod 600, `/etc/fstab`'a kalıcı), `vm.swappiness=10` (`/etc/sysctl.d/99-swappiness.conf`). 📝 **Düzeltme (Y9'da uygula):** swap varken `MemoryMax` tek başına katı değil (cgroup önce swap'e iter); `davetkart-queue.service`'e **`MemorySwapMax=0`** eklenecek |
| Y5.3 | 25 Ekim | ✅ | `deploy` kullanıcısı (parolasız, `www-data` grubunda, **sudo yok**, aynı `.pub` anahtarı). `/etc/ssh/sshd_config.d/01-davetkart.conf` (60-cloudimg-settings.conf'tan ÖNCE okunsun diye `01-`; sshd'de ilk değer kazanır): PermitRootLogin no, PasswordAuthentication no, KbdInteractiveAuthentication no, MaxAuthTries 3, AllowUsers ubuntu deploy. Yeni oturumlarda ubuntu+deploy girişi doğrulandı, root reddedildi. `ubuntu` = parolasız sudo = fiilen root: anahtarı en kıymetli sır; günlük iş `deploy` ile. **Y8'de `deploy` için sınırlı sudoers yazılacak**, `deploy.sh`'taki `sudo -v` bu yüzden kaldırılacak |
| Y5.4 | 25 Ekim | ✅ | `timedatectl`: Etc/UTC, System clock synchronized: yes, NTP service: active. Sunucu saati İsmail'in saatiyle uyumlu (19:56 UTC = 22:56 İstanbul) |
| Y6.1a | 25 Ekim | ✅ | `ppa:ondrej/php` eklendi; `php8.5-fpm` Candidate = **8.5.12-1+ubuntu24.04.1+deb.sury.org+1**. 🔴 **PHP CVE-2026-109618 / CVE-2026-109619** (uzaktan kod çalıştırma, kimlik doğrulamasız, FPM dahil; 8.5.0–8.5.11 etkilenir, düzeltme **8.5.12**; kaynak: AWS bülteni 2026-143-aws). **Kural: sunucuya yalnızca ≥ 8.5.12 kurulur.** Lightsail'in "yeni blueprint'ten yeni instance aç" önerisi bizim için geçersiz (instance'ta PHP yoktu). **Y6.2'ye ekle:** `session.upload_progress.enabled=Off` (savunma derinliği). 📝 PPA açıklaması: depo `https://packages.sury.org/php/` içine taşınıyor; Noble için PPA şimdilik kullanılabilir, "önümüzdeki haftalarda" geçiş yolu verilecek → **izle** (apt update uyarısı çıkarsa kaynak değiştirilecek) |
| Y6.1b | 25 Ekim | ✅ | `php8.5-fpm` ve eklentiler kuruldu; `php -v` ≥ 8.5.12 doğrulandı. Kural sürüyor: sunucuda PHP < 8.5.12 olmayacak (unattended-upgrades PPA'dan güncelleme getirirse sürüm yine kontrol edilecek) |
| Y6.2 | 25 Ekim | ✅ | `/etc/php/8.5/mods-available/davetkart.ini` (+ `phpenmod -v 8.5 davetkart`): upload_max_filesize 25M, post_max_size 30M, memory_limit 256M, display_errors Off, log_errors On, expose_php Off, `session.upload_progress.enabled=Off`. Repo kopyası `deploy/php/davetkart.ini` (**kullanıcı henüz commit etmedi**) → Y8'de sunucudaki dosyayla karşılaştır |
| Y6.3 | 25 Ekim | ✅ | Argon2id ölçümü sunucuda ortalama **260 ms** → `ARGON_MEMORY=65536`, `ARGON_TIME=4`, `ARGON_THREADS=1` aynen kalır |
| Y6.4a-c | 25 Ekim | ✅ | PostgreSQL 18.6 (PGDG), küme `18/main`, yalnızca 127.0.0.1'de dinliyor. Rol `davetkart` (süper kullanıcı değil, parola var, parola yöneticisinde), veritabanı `davetkart` (sahibi `davetkart`) |
| Y6.4d | 25 Ekim | ✅ | Doğrulama: `postgres` = süper kullanıcı, **parolasız** (yalnızca yerel `peer` ile `sudo -u postgres psql`; TCP ile giriş imkânsız → bilinçli, parola eklenmez). `pg_hba.conf`: `local` → peer, `host 127.0.0.1/32` ve `::1/128` → scram-sha-256, başka kural yok. `psql -h 127.0.0.1 -U davetkart -d davetkart` → `current_user=davetkart`, `current_database=davetkart` ✅ |
| Y6.5a | 25 Ekim | ✅ | `nginx/1.24.0 (Ubuntu)` (Ubuntu deposu, güvenlik yamaları unattended-upgrades ile), `enabled` + `active`. Dinleyen portlar: `0.0.0.0:80` + `[::]:80` (nginx), `127.0.0.1:5432` (postgres, yalnızca yerel). Varsayılan sayfa `200 OK`. 📝 Yanıtta `Server: nginx/1.24.0 (Ubuntu)` sürüm sızdırıyor → bizim `davetkart.conf` içinde `server_tokens off;` zaten var (satır 33), Y7'de devreye girince başlık `Server: nginx` olur. Yan not: `~/.ssh/config` (Windows) `ServerAliveInterval 60` ile boşta kopma çözümü; `deploy` ile `sudo` reddi = beklenen davranış |
| Y6.5b | 25 Ekim | ✅ | Composer **2.10.3**, resmî kurulum betiği SHA-384 imzası doğrulanarak (`IMZA OK`) `/usr/local/bin/composer`'a kuruldu. `apt install composer` bilerek kullanılmadı (eski 2.7 + Ubuntu'nun `php8.3-*` paketlerini çeker → ikinci PHP). `which -a php` → `/usr/bin/php` ve `/bin/php` (Ubuntu 24.04'te `/bin` → `/usr/bin` sembolik bağı, aynı dosya), `php -v` = 8.5.12. Tarayıcıdan `http://63.182.93.247` varsayılan sayfa ✅ (firewall 80 doğrulandı). Kural: `composer install` root ile değil, Y8'de `deploy` ile |
| Y6.5c (karar) | 25 Ekim | ✅ | **Sapma:** Node 22 yerine **Node 24 LTS** (22'nin desteği 30 Nisan 2027'de bitiyor, 24 Nisan 2028'e kadar yama alıyor; Vite 6 + TS 5.8 uyumlu). İsmail yereldeki Node'u da 24'e yükseltecek (yerel ve sunucu aynı ana sürüm). Kaynak: NodeSource deposu, anahtar `/etc/apt/keyrings/nodesource.gpg` + `signed-by` (yalnızca bu depo için güvenilir), parmak izi **6F71F525282841EEDAF851B42F59B5F99B1BE0B4** kurulumda doğrulanacak. 📝 `@types/node` ^22 → frontend tarafında 24'e çekilmesi ayrı iş (build'i bozmaz) |
| Y6.5c | 25 Ekim | ✅ | Node **v24.22.1** + npm **11.19.1** (NodeSource resmî `setup_24.x`; boru yerine indir → `grep` ile incele → çalıştır). Anahtar `/usr/share/keyrings/nodesource.gpg` (betiğin tercihi; `Signed-By` ile yalnızca bu depoya bağlı), `nodesource.sources`: `node_24.x`, `nodistro`, `amd64`. Öncelik **600** (betiğin pin'i, Ubuntu'nun Node 18'ini ezer). `deploy` kullanıcısı da `v24.22.1` görüyor (sistem geneli kurulum → Y8 `deploy.sh` bulur). nvm bilerek kullanılmadı (kullanıcıya özel + apt dışı yama). Parmak izi **6F71 F525 2828 41EE DAF8 51B4 2F59 B5F9 9B1B E0B4** (NSolid, rsa2048, 2016) ✅ beklenenle aynı; kurulum betiği silindi |
| Y7.1 | 25 Ekim | ✅ | Natro: A `@` 85.159.66.93 → **63.182.93.247**; CNAME `www` → redirect.natrocdn.com silindi, yerine CNAME `www` → `davetkart.com` eklendi (ilk listede eksikti, sonra eklendi). AAAA yok (Lightsail statik IP yalnızca IPv4). Mail/SES/ACM/media kayıtlarının hepsi yerinde. NS: `ns1/ns2.natrohost.com`. Google DNS (8.8.8.8) `davetkart.com` → 63.182.93.247 ✅. `www.davetkart.com` → CNAME → 63.182.93.247: Natro yetkili sunucusunda (ns1, 83.217.77.15) ve Google DNS'te ✅ |
| Y7.2a | 25 Ekim | ✅ | 📝 Kurulumdan önce düzeltme: `server_tokens off;` yalnızca apex bloğundaydı → dosyanın en üstüne (http bağlamı) taşındı, `www` 301'i de sürümü gizliyor (rehbere bölüm eklendi; **commit bekliyor**: `deploy/nginx/davetkart.conf` + rehber). `scp` ile `/etc/nginx/sites-available/davetkart.conf` (root:root 644), `sites-enabled` bağlantısı, `default` kaldırıldı, `nginx -t` ✅, reload. Testler (İsmail'in PC'sinden): apex → `404` + `Server: nginx` (sürümsüz, dist henüz yok), `www` → `301 https://davetkart.com/`, IP → boş yanıt (444) |
| Y7.2b | 26 Ekim | ✅ | `apt install certbot python3-certbot-nginx` (snap yerine apt: yamalar unattended-upgrades ile). `certbot --nginx -d davetkart.com -d www.davetkart.com --redirect` → tek sertifika iki ad, `/etc/letsencrypt/live/davetkart.com/`. `certbot.timer` aktif (günde 2 kontrol), `renew --dry-run` ✅. Testler: `https://davetkart.com` → 404 (dist yok), `http://` → 301 https apex, `https://www` → 301 apex. 📅 **Let's Encrypt ömür kısalıyor:** 10 Şubat 2027'den itibaren 64 gün, 2028'de 45 gün (kaynak: letsencrypt.org/2026/10/07/64-day-certs). Certbot'un "bitime 30 gün kala yenile" varsayılanı ikisine de yeter; elle sabit gün yazılmayacak. ⚠️ Let's Encrypt artık bitiş uyarı e-postası göndermiyor → Y11 UptimeRobot'ta **SSL bitiş izlemesi** açılacak |
| Y7.3 | 26 Ekim | ✅ | certbot'un çıktısı okundu, **temiz hâli depoya yazıldı** (`# managed by Certbot` yok): 80 default → 444 · **443 default → `ssl_reject_handshake on`** (IP ile https'te sertifika/alan adı sızmıyor; test: schannel `SEC_E_ILLEGAL_MESSAGE` ✅) · **tek 80 bloğu** (`davetkart.com` + `www`) → doğrudan `https://davetkart.com` (çift yönlendirme kalktı; test: tek 301 ✅) · 443 `www` → apex · 443 apex = asıl site · **`http2`** (test: `HTTP/2 404` ✅). 🪤 `protocol options redefined for 0.0.0.0:443` uyarısı: `ssl`/`http2` adres:kapı özelliği, dört `listen 443` satırı birebir aynı yapıldı → uyarı gitti. `renew --dry-run` yeni dosyayla ✅. Rehber: 443 default, tek yönlendirme, http2, sıfırdan kurulum (`certonly --nginx --deploy-hook`). Certbot sürümünün yedeği `/root/davetkart.conf.certbot-yedek` (Y7 sonunda silinecek). **Commit bekliyor:** `deploy/nginx/davetkart.conf` + rehber |
| Y7.4 (Nginx) | 26 Ekim | ✅ | `grep -rin strict-transport /etc/nginx/ /etc/letsencrypt/options-ssl-nginx.conf` → yok: **Nginx HSTS basmıyor** (karar: yalnızca Laravel `SecurityHeaders`). Laravel tarafı (yanıtta başlık **tam 1 kez**) Y8'de `/api/ping` ile doğrulanacak |
| Y7.5 | 26 Ekim | ↪️ **Y10 sonrasına taşındı** | Plan sapması (İsmail onayladı): site şu an HTTPS ile açılıyor ama 404 (dist yok); AWS incelemesi boş sayfa görürse red riski. Frontend yayındayken gönderilecek. Sandbox (doğrulanmış adreslere 200/gün) Y8–Y10 testleri için yeterli |
| Y8.1 | 26 Ekim | 🟡 | `deploy` kullanıcısında ED25519 deploy anahtarı `~/.ssh/github_backend` (parolasız: `git pull` etkileşimsiz; risk = salt okunur + tek depo + 600 izin), `~/.ssh/config` takma adı `github-backend`. GitHub → backend deposu → Deploy keys: `davetkart-prod (Lightsail)`. `ssh -T github-backend` → `Hi ismail-cankaya/davetkart-backend-php-laravel!` ✅ (hesap değil **depo** adı = depoya bağlı anahtar). Frontend (`ismail-cankaya/davetkart`) için Y10'da ayrı `github_frontend`. GitHub host parmak izi `SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU` ✅, `github_backend` 600 ✅. **Açık:** Deploy keys ekranında "Read-only" görüntüsü. Dal durumu (26 Ekim): `release-v1.0` = `origin/release-v1.0`, `origin/main`'in 127 commit önünde, `main`'de olup onda olmayan 0 → **hızlı ileri sarma (fast-forward) mümkün**; `release-2026-10-20` `release-v1.0`'ın atası (47 geride). nginx/php dosyaları commit+push edilmiş |
| Y8.2a | 26 Ekim | ✅ | **Karar:** sunucu her zaman `main`'i çeker. `main` → `release-v1.0`'a fast-forward (127 commit, çakışma yok), `origin/main` = `78401f9`. Akış: dalda çalış → CI → `main`'e merge → push → sunucuda elle `deploy.sh` (push otomatik deploy ETMEZ; bilinçli). 📝 **Y12'ye eklendi:** GitHub `main` için branch protection (doğrudan push yok, CI geçmiş PR şart) |
| Y8.2b | 26 Ekim | ✅ | `/var/www/davetkart` = `deploy:www-data` **2750** (setgid: içindeki her şey grubu `www-data` miras alır). `deploy` umask **027** (`~/.profile` + `~/.bashrc`) → yeni dosya 640, klasör 750; `www-data` kodu okur ama YAZAMAZ (PHP açığı → kalıcı arka kapı engellenir). `git clone --branch main github-backend:…` → `/var/www/davetkart/backend`, HEAD `78401f9` ✅, `artisan` `-rw-r----- deploy:www-data`, `app`/`public` `drwxr-s--- deploy:www-data` ✅. Not: depodaki `CLAUDE.md`/`claude/` sunucuya geldi; Nginx yalnızca `public/` sunduğu için erişilemez |
| Y8.3a | 26 Ekim | ✅ | `chmod -R g+w storage bootstrap/cache` → `drwxrws--- deploy:www-data` (yalnızca bu ikisine grup yazma). `composer check-platform-reqs --no-dev` hepsi `success` (php 8.5.12, ext-gd, ext-exif…). `composer install --no-dev --optimize-autoloader --no-interaction --no-scripts` (deploy kullanıcısı): 88 paket, laravel/framework v13.35.0, `vendor` 125 MB. `composer audit --no-dev` → açık yok. `git status` temiz. 📝 `unzip` yok uyarısı (PHP zip ile açıyor, çalıştırma bitleri kaybolur) → `sudo apt install -y unzip` önerildi. 📝 `docs/10` şablonu eskimiş: `APP_URL=https://api.davetkart.com` (same-origin kararından önce), `AWS_URL` satırı yok, Shopier callback/OSB adresleri `api.` alt alan adında → düzeltilecek |
| Y8.3b | 26 Ekim | ✅ | Üretim `.env` (`docs/10` şablonundan, düzeltmelerle: `APP_URL=https://davetkart.com`, `AWS_BUCKET=davetkart-media-438641`, **`AWS_URL=https://media.davetkart.com`** (şablonda yoktu), `MAIL_MAILER=ses`, `AI_PROVIDER=null` (Gemini Y11), `PAYMENT_PROVIDER=shopier` + `PAYMENT_METHODS=gift_code` (fake bilerek değil: kart yanlışlıkla açılırsa 503)). Sırlar nano ile sunucuda dolduruldu, sohbete gelmedi. Yerel `.env`'den kopyalanmadı (APP_KEY/DB/Gemini ortam başına ayrı); yereldeki fazladan satırlar Laravel varsayılanları, üretimde gereksiz. `key:generate --force` ✅. `.env` = `-rw-r----- deploy:www-data` ✅, APP_KEY/DB_PASSWORD/AWS_* hepsi DOLU, `git status` temiz |
| Y8.4 | 26 Ekim | ✅ | `deploy` için **sınırlı sudoers** yazıldı: `deploy/sudoers/davetkart-deploy` → `(www-data) NOPASSWD: /usr/bin/php, /usr/bin/chmod` + `(root) NOPASSWD: /usr/bin/systemctl reload php8.5-fpm` (birebir). `deploy.sh`: `sudo -v` **kaldırıldı** (parolasız kullanıcıda hiç çalışmazdı), tüm sudo çağrıları `sudo -n` + tam yol, başta yetki ön kontrolü. Rehber: yeni `docs/rehber/deploy/sudoers/davetkart-deploy.md`, `deploy.md` güncellendi. Commit → main → push, sunucuda `git pull`; `visudo -cf` parsed OK → `/etc/sudoers.d/davetkart-deploy` (root:root 440), `visudo -c` hepsi OK. `sudo -l -U deploy` yalnızca iki kural. Test: `deploy` → `www-data` olarak `php -v` ✅ (8.5.12), `systemctl stop nginx` → `a password is required` ✅ (reddedildi) |
| Y8.5 | 26 Ekim | ✅ | **İlk deploy** (`bash deploy/deploy.sh`, `deploy` kullanıcısı): 29 göç `Ran`, `config.php` `www-data` 640, `packages.php`/`routes-v7.php` `www-data`. `https://davetkart.com/api/ping` → **200 `{"status":"ok"}`** (İsmail'in PC'sinden). `storage/logs` boş (warning altı log yok). 🪤 `bootstrap/cache/services.php` `deploy:www-data 750` kaldı: Y8.3b'deki `key:generate` **deploy** ile çalıştığı için üretmişti → `www-data` yeniden yazamaz; silinip `www-data` ile yeniden üretilecek. Kural: artisan yalnızca `sudo -n -u www-data` ile (key:generate tek istisnaydı, .env'e yazdığı için) |
| Y7.4 (Laravel) | 26 Ekim | ✅ | `/api/ping` yanıtında `Strict-Transport-Security: max-age=31536000; includeSubDomains` **tam 1 kez** (Laravel `SecurityHeaders`; Nginx basmıyor). Ayrıca `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, API CSP `default-src 'none'` ✅ |
| Y8.6 | 26 Ekim | ✅ | `services.php` silindi, `www-data` ile `artisan about` → yeniden üretildi, sahibi artık `www-data` ✅. `about`: production, **Debug OFF**, Laravel 13.35.0, PHP 8.5.12, URL davetkart.com, Timezone UTC. Not: önbellek dosyaları `775/664` (Laravel `replace()` + umask); "diğerleri" biti etkisiz çünkü `/var/www/davetkart` 2750 (diğerleri klasöre giremez). **Y8 tamam** |
| Y9.1 (hazırlık) | 26 Ekim | 🟡 | `davetkart-queue.service`'e **`MemorySwapMax=0`** eklendi (Y5.2 düzeltmesi: swap varken MemoryMax katı değil). Rehber güncellendi (MemorySwapMax paragrafı, kurulumda `systemd-analyze verify` + `install -m 644`). **Bekliyor:** commit → main → push, sunucuda `git pull`, kurulum ve `systemctl status` |
| Y9.1 | 26 Ekim | ✅ | İkinci deploy (`deploy.sh`): `481871a → 581da16`, ping ✅ (kod değişince deploy akışı denendi). `systemd-analyze verify` temiz, `/etc/systemd/system/davetkart-queue.service` (root 644), `enable --now` → **active (running)**, enabled. `systemctl show`: User=www-data, MemoryMax=805306368 (768M), **MemorySwapMax=0**, Restart=always. Status satırı: `max: 768.0M swap max: 0B` |
| Y9.2 | 26 Ekim | ✅ | `deploy/cron/davetkart` → `/etc/cron.d/davetkart` (root 644): her dakika `www-data` ile `schedule:run`; stdout atılır, stderr `logger -t davetkart-schedule` ile journal'a. `schedule:list`: orders:expire (saatlik), sanctum:prune-expired (00:00 UTC), media:prune-orphans (03:15 UTC), data:purge (03:45 UTC). Cron günlüğünde `(www-data) CMD (...)` ✅, `journalctl -t davetkart-schedule` boş ✅. Not: `ubuntu` `/var/www/davetkart`'a giremez (2750, tasarım gereği) → artisan tam yolla çağrılır |
| Y9.3 | 26 Ekim | ✅ | Kuyruk işçisi 22:09:16'dan beri `active (running)`: deploy'daki `queue:restart` işçiyi temiz kapattı, `Restart=always` 5 sn'de yeniden başlattı (beklenen döngü kanıtlandı). **Y9 tamam** |
| Y10.1 | 26 Ekim | ✅ | Frontend `main` → `faz-14-account-settings`'e fast-forward, `origin/main` = `ae5937b`. Çalışma ağacında yalnızca `.claude/` izlenmiyor (commit'e girmez, `git add -A` yok). `deploy` kullanıcısında ikinci deploy anahtarı `~/.ssh/github_frontend`, takma ad `github-frontend`, GitHub `ismail-cankaya/davetkart` → Deploy keys (salt okunur). İsmail iki `ssh -T` testinin de geçtiğini bildirdi. Üretim build değişkenleri: `VITE_API_BASE_URL=/api`, `VITE_PLACES_SEARCH_ENABLED=false` (sır değil; VITE_ değerleri tarayıcıya gömülür) |
| Y10.2 | 26 Ekim | ✅ | Frontend klonu `/var/www/davetkart/frontend` (`github-frontend:`, HEAD `ae5937b`). `npm ci --ignore-scripts` ✅ (210 paket, 6 sn; bağımlılık betikleri kapalıyken de build çalışıyor → kalıcı tercih). `VITE_API_BASE_URL=/api VITE_PLACES_SEARCH_ENABLED=false npm run build` → `✓ built in 12.57s`, RAM rahat (available 1.2 Gi, swap ~0). `dist` 26 MB, `node_modules` 187 MB, `dist/index.html` `deploy:www-data 640` ✅. **Site tarayıcıda çalışıyor** (İsmail). 🔴 `npm audit --omit=dev`: 14 açık (1 kritik, 10 yüksek). Sebep çoğunlukla **sınıflandırma**: AI Studio şablonundan kalma `express`, `dotenv` (hiç kullanılmıyor), `vite`, `@vitejs/plugin-react`, `@tailwindcss/vite` `dependencies`'te. Tarayıcıya gerçekten giden: **axios** (<1.19.1) ve **react-router** (<7.18.2) → Y10.2b'de düzeltilecek. 📝 Y12 performans: ana JS 1,59 MB (gzip 428 kB), `bg.png` 1,17 MB, CSS 921 kB (gzip 95 kB) |
| Y10.2b | 26 Ekim | ✅ | Frontend bağımlılık temizliği (`fix/deps-audit` → `main` = `47aedc8`): kullanılmayan `express`, `dotenv`, `@types/express` kaldırıldı; `vite@6`, `@vitejs/plugin-react@5`, `@tailwindcss/vite@4` → `devDependencies`; `npm audit fix` (axios, react-router, vite 6.4.5…). **`npm audit --omit=dev` ve tam `npm audit`: 0 açık.** `npm run check` (tsc + build + 11 verify betiği) ✅. npm `allow-scripts` uyarısı: esbuild kurulum betikleri onaysız = zaten çalışmıyor (sunucuda `--ignore-scripts` ile aynı tutum). ⚠️ GitHub: **depo adı değişmiş** → `ismail-cankaya/davetkart-frontent` (eski ad yönlendiriyor); yerel ve sunucu `origin` adresleri güncellenecek |
| Y10.3 (hazırlık) | 26 Ekim | 🟡 | `deploy/deploy-frontend.sh` yazıldı: temizlik kontrolü → `git pull --ff-only` → `npm ci --ignore-scripts` → `vite build --outDir dist.new` (yayındaki `dist/` dokunulmaz) → önceki `assets/` üzerine yazmadan kopyalanır, 14 günden eski kopyalar silinir (ChunkLoadError önlemi) → `dist→dist.old`, `dist.new→dist` → sağlık kontrolü (`<div id="root">`). Derleme ayarları (`VITE_API_BASE_URL=/api`, `VITE_PLACES_SEARCH_ENABLED=false`) betikte, sunucuda `.env.production` yok. `deploy.sh` sonunda çağırıyor (önce backend, `trap - ERR`). Rehber: `docs/rehber/deploy/deploy-frontend.md`, `deploy.md` §5 |
| Y10.3 (1. deneme) | 26 Ekim | 🪤 | Backend `7c47e13 → 443c5a5` ✅ ama **frontend adımı çalışmadı**: `git pull` `deploy.sh`'ı değiştirdi, çalışan bash süreci eski dosyayı okumaya devam etti (eski "Bitti" satırı). Düzeltme: `deploy.sh` `git pull` sonrası `deploy/` değiştiyse kendini `exec` ile yeni hâliyle baştan başlatıyor (`DAVETKART_DEPLOY_PREV`: tek sefer + doğru "önceki sürüm"). Rehber §Adım 1b. Sunucu frontend `origin` → `github-frontend:ismail-cankaya/davetkart-frontent.git` |
| Y10.3 | 26 Ekim | ✅ | Tek komutla tam site deploy'u (`deploy.sh` → backend, ardından `deploy-frontend.sh`): `[frontend] Bitti: ae5937b -> 47aedc8`, derleme `dist.new/` içine 11,3 sn, yer değiştirme + sağlık kontrolü ✅, site çalışıyor. 📝 `cp -an` coreutils 9.x'te "non-portable" uyarısı → `cp -a --update=none` (aynı anlam: var olanı ezme) |
| Y10.3b | 26 Ekim | ✅ | `cp --update=none` düzeltmesi deploy edildi ve **yeniden başlatma ilk kez canlı denendi**: `Kod cekiliyor (3bc56a8)` → `deploy/ betikleri degisti: yeni surumle yeniden baslatiliyor` → ikinci tur (tekrar başlatma YOK, "önceki sürüm" yine 3bc56a8) → `Backend bitti: 3bc56a8 -> 03d3940` → frontend `47aedc8 -> 47aedc8`, `cp` uyarısı yok. `dist` + `dist.old`, `git status` temiz, `dist/assets` 182 dosya (önceki derlemenin parçaları korunuyor). **Y10 tamam** |
| Y10.4 | 26 Ekim | ✅ | **Uçtan uca kullanıcı testi** (İsmail, tarayıcıdan): kayıt + giriş, davetiye oluşturma, fotoğraf yükleme (S3 + kuyruk + `media.davetkart.com`) çalışıyor; parola sıfırlama maili SES sandbox'tan doğrulanmış Gmail'e **gelen kutusuna** düştü (spam değil → DKIM/DMARC çalışıyor) |
