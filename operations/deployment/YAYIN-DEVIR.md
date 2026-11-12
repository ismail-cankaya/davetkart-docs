# YAYIN DEVİR NOTU — DavetKart'ı AWS'e Alma

> **Yazıldığı an:** 15 Ekim 2026, 00:10 (İstanbul)
> **Kimin için:** Bu işe yeni bir oturumda devam edecek yapay zekâ asistanı
> **Ayrıntılı plan:** `YAYIN-PLANI.md` (aynı klasörde; ayrıca claude.ai projesinde `claude/YAYIN-PLANI.md`)
> **Bu dosya ile plan çelişirse:** bu dosya daha yenidir, ama ikisini de oku.

---

## 1. Kiminle çalışıyorsun, nasıl çalışıyorsun

**İsmail**, bilgisayar mühendisliği 3. sınıf öğrencisi. DavetKart'ı (dijital davetiye SaaS'ı) kendisi geliştirdi:
backend PHP 8.5 + Laravel 13 (`davetkart-backend-php-laravel/`), frontend React 19 + TypeScript (`davetkart-frontent/`).
Backend ve frontend **bitti**; şu an **canlıya alma (deploy)** aşamasındayız.

**Çalışma kuralları — ihlal edilemez:**

1. **Her cevapta tek bir adım.** Adımı ver, gerekçesini anlat, **DUR ve onay bekle.** İsmail "tamam" demeden sonrakine geçme.
2. **Kıdemli mimar gibi anlat.** Amaç komut kopyalatmak değil, **neden** öyle yapıldığını öğretmek: güvenlik, maliyet, tasarım ilkesi.
3. **AWS menü adlarını hep iki dilde ver:** `İngilizce (Türkçe)` — ör. **Security credentials** (**Güvenlik kimlik bilgileri**). İsmail'in konsolu bazen TR bazen EN.
4. **Komutları ve tıklamaları İsmail yapar.** Sen onun yerine çalıştırmazsın; ne yapacağını söyler, ekran görüntüsünü/çıktıyı beklersin.
5. **Her adımın sonunda bir doğrulama** iste (ekran görüntüsü, komut çıktısı, tarayıcı testi). "Yaptığını varsayma, doğrula."
6. **Plandan sapma önce tartışılır.** Daha iyi bir yol görürsen gerekçesiyle öner, onay al, sonra `YAYIN-PLANI.md`'ye işle.
7. Türkçe yaz, öğrenciye anlatır gibi, ama teknik ayrıntıyı atlamadan.

---

## 2. Varılan mimari (karar verildi)

```
Kullanıcı ──► davetkart.com  (DNS Natro'da · A → Lightsail statik IP — HENÜZ YOK, Y7'de)
                  │
   Lightsail · Ubuntu 24.04 · 2 GB · Frankfurt  (HENÜZ KURULMADI, Y4)
     Nginx + Let's Encrypt → /  React dist  ·  /api → PHP 8.5-FPM → Laravel 13
     PostgreSQL 18 (yalnızca 127.0.0.1) · queue:work (systemd) · schedule:run (cron)
                  │
   ┌──────────────┼────────────────────────────┐
   ▼              ▼                            ▼
 S3 medya      SES (mail gönderme)       S3 yedek (Y11, ayrı bucket)
 (kapalı) ◄── CloudFront ◄── https://media.davetkart.com   ✅ KURULDU
```

| Karar | Gerekçe |
|---|---|
| **Lightsail (Yol A)**, EC2+RDS ya da Elastic Beanstalk değil | ~200 $ AWS kredisi, ~10 ay geçerli → ayda ≤15 $. Lightsail ~14–16 $/ay; EC2+RDS ~28 $; EB ~50 $. 2025 sonrası hesaplarda 12 aylık ücretsiz EC2/RDS **yok** |
| Same-origin (`/api` aynı alan adında) | CORS yok; frontend `VITE_API_BASE_URL=/api` zaten bunu bekliyor |
| **YD-1:** deploy = sunucuda `git pull` + `deploy.sh` | Önce elle anlaşılır betik, GitHub Actions sonra |
| **YD-2 (14 Ekim'de güncellendi):** medya bucket'ı **tamamen kapalı**, yalnızca **CloudFront + OAC** okur, `https://media.davetkart.com` | Misafir fotoğrafları kişisel veri; yanlış bir bucket politikası satırıyla sızma riski yok |
| **İki ayrı bucket** (medya / yedek) | Kusur yalıtımı: yedek bucket'ının Block Public Access'i hiç açılmaz |
| **YD-3:** Redis yok | 2 GB RAM; `database` kuyruk + `file` cache (K80) yeterli |
| **YD-4:** SSH 22 herkese açık ama yalnızca anahtar; parola ve root girişi kapalı | İsmail'in ev IP'si değişken |
| Mail: **gönderme = Amazon SES**, **alma = Natro mail hosting** | Ayrı sorumluluklar; DNS'te barış içinde |

---

## 3. Yapılanlar (3–15 Ekim 2026)

### Y1 — AWS hesabı ✅
- Hesap: **ücretli planda** (ücretsiz plan 6 ayda hesabı kapatırdı — risk yok). Hesap no: `438641189207`.
- Root: MFA (2 cihaz), erişim anahtarı yok. **Root ile bir daha girilmiyor.**
- Fatura bilgisine IAM erişimi açıldı (root ile).
- IAM grubu `Admins` (`AdministratorAccess`) · kullanıcı **`ismail-admin`** (+MFA). Giriş: `https://davetkart.signin.aws.amazon.com/console` (hesap takma adı `davetkart`).
- Konsol varsayılan bölgesi: **eu-central-1 (Frankfurt)** (Unified Settings).
- ⏰ **Y1.4 (bütçe alarmları) ERTELENDİ → Y4.5** (İsmail'in isteği). Ayrıntı §5.

### Y2 — SES (mail gönderme) ✅
- Frankfurt'ta kimlikler: `ismayilcankaya2017@gmail.com` ✅ ve **`davetkart.com`** ✅ (Easy DKIM, RSA 2048).
- Fiyatlandırma: otomatik verilen **Essentials planı iptal edildi → à la carte** (0,10 $/1.000 mail). VDM, dedicated IP, kiracı yönetimi **yok**.
- Natro'ya: 3 DKIM CNAME + `_dmarc` TXT (`v=DMARC1; p=none;`). **SPF'e dokunulmadı** (özel MAIL FROM yok → SPF `amazonses.com` için kontrol edilir; DMARC uyumu DKIM'den gelir).
- Test: SES'ten `bilgi@davetkart.com` → Gmail **gelen kutusuna** düştü (spam değil).
- Natro'da **`bilgi@davetkart.com`** mail kutusu oluşturuldu (Gmail'e yönlendirme önerildi).
- **Sandbox'tayız:** günde 200 mail, yalnızca doğrulanmış adreslere. **Production erişimi talebi Y7.5'e taşındı** (park edilmiş alan adından talep reddedilme riski taşır; site canlıyken gönderilecek).

### Y3 — S3 + CloudFront 🟡 (son test bekliyor)
- Bucket **`davetkart-media-438641`** (Frankfurt, ACL kapalı, Block Public Access **4/4 açık**, sürümleme açık, SSE-S3 + Bucket Key).
- CloudFront dağıtımı **`davetkart-media`**: ID `E3OV6EN5B6X9YB`, adres `d252jqf124chfh.cloudfront.net`, **Free plan** (0 $/ay, 1M istek, 100 GB), origin = REST uç noktası, **OAC**. Bucket politikasını CloudFront kendisi yazdı (`cloudfront.amazonaws.com`, `s3:GetObject`, `ArnLike AWS:SourceArn` = bu dağıtım).
- Katman 1 testi ✅: `d252jqf124chfh.cloudfront.net/test.jpg` resmi açıyor · S3'e doğrudan erişim `AccessDenied` (negatif test ✅).
- ACM sertifikası **`media.davetkart.com`** (us-east-1, `50b28409-841a-4919-8d97-2d3479b754d7`) DNS ile doğrulandı · CloudFront'a alternate domain olarak eklendi · `TLSv1.2_2021`.
- Natro'ya `media` CNAME → `d252jqf124chfh.cloudfront.net` **eklendi**; 15 Ekim 00:08'de DNS henüz yayılmamıştı.

### Natro DNS'in tam durumu
| Kayıt | Sahibi | Ne yapılacak |
|---|---|---|
| A `@` → `85.159.66.93` · CNAME `www` → `redirect.natrocdn.com` | Natro park/yönlendirme | **Y7'de değişecek** (Lightsail statik IP) |
| MX ×2 `mx-0{1,2}.kurumsaleposta.com` · CNAME `autodiscover` · SRV `_autodiscover._tcp` · TXT `ntr._domainkey` · TXT SPF (`v=spf1 include:_spfcls.natrohost.com …`) | Natro mail hosting | 🔒 Dokunulmaz |
| 3× CNAME `…._domainkey` → `….dkim.amazonses.com` · TXT `_dmarc` | SES | 🔒 Dokunulmaz |
| CNAME `_db41d753218f08f2eb5dde52ca1afac5.media` → `…acm-validations.aws` | ACM | 🔒 **Asla silinmez** (otomatik yenileme buna bakar) |
| CNAME `media` → `d252jqf124chfh.cloudfront.net` | CloudFront | 🔒 Dokunulmaz |

---

## 4. ▶️ TAM OLARAK BURADAN DEVAM ET

**Y3.2'nin son testi:**
1. CloudFront'ta `davetkart-media` → **Last modified** "Deploying" değil, tarih görünüyor mu?
2. Tarayıcıda **`https://media.davetkart.com/test.jpg`** → resim açılmalı.
3. Adres çubuğundaki kilit → sertifika **`media.davetkart.com`** için, Amazon tarafından verilmiş olmalı.
4. Açılmıyorsa: `nslookup media.davetkart.com` (Windows cmd) → `d252jqf124chfh.cloudfront.net`'e çözülüyor mu? Çözülmüyorsa Natro kaydını kontrol et (Adı yalnızca `media`, İçerik sonda noktasız).
5. Geçince: S3'ten **`test.jpg`'yi sil**, `YAYIN-PLANI.md` §8'e Y3.2 ✅ işle.

---

## 5. Kalan adımlar (sırayla)

| # | Adım | Notlar |
|---|---|---|
| **Y3.3** | **Ömür kuralı (lifecycle)** `davetkart-media-438641` için: **eski (noncurrent) sürümler 7 gün sonra kalıcı silinsin** + tamamlanmamış çok parçalı yüklemeler 7 gün | 🔴 **KVKK bağı:** Faz 10'daki `data:purge` (K98) misafir verisini 6 ay sonra siler. Sürümleme açıkken "silme" yalnızca gizler; bu kural olmazsa fotoğraflar eski sürüm olarak sonsuza kadar kalır |
| **Y3.4** | IAM kullanıcısı **`davetkart-app`** (konsol erişimi **YOK**, yalnızca erişim anahtarı). Satır içi politika: `davetkart-media-438641` için `s3:GetObject/PutObject/DeleteObject` (`arn:…:davetkart-media-438641/*`) + `s3:ListBucket` (bucket ARN'i) + `ses:SendEmail`/`ses:SendRawEmail` | Lightsail'de EC2 gibi instance rolü yok → anahtar şart. Sızarsa zarar bu yetkilerle sınırlı (en az yetki). Anahtar yalnızca sunucudaki `.env`'e girer |
| **Y0** | Kod tarafı hazırlık (İsmail'in makinesinde) | `composer require league/flysystem-aws-s3-v3` (**yüklü değil** — S3 diski onsuz çalışmaz; aws-sdk-php'yi de getirir, SES için ek paket gerekmez) · `deploy/` klasörü: nginx conf, systemd kuyruk servisi, `deploy.sh` · 🔴 **Frontend deposunda ~617 commit'lenmemiş değişiklik** (büyük kısmı CRLF; `.gitattributes` kararı 10.81) — sunucu git'ten çekecek · `composer check` + `npm run check` yeşil, commit + push |
| **Y4** | Lightsail: Ubuntu 24.04 LTS, 2 GB (12 $/ay), Frankfurt, kendi SSH anahtarı · statik IP · firewall 22/80/443 (**IPv4 ve IPv6 ayrı**) · otomatik günlük snapshot (7 gün) | |
| **Y4.5** ⏰ | **Ertelenen bütçe alarmları** — sunucu kurulur kurulmaz HATIRLAT | 🔴 Tuzak: AWS Budgets varsayılan olarak **kredileri düşer** (`IncludeCredit=true`) → alarm hiç çalmaz. (1) `davetkart-aylik-harcama`: Maliyet, Aylık, Yinelenen, Sabit **15 $**, tüm hizmetler, **Gelişmiş seçenekler → Krediler işaretini KALDIR**, eşikler %80 Gerçekleşen / %100 Gerçekleşen / %100 Tahmini. (2) `davetkart-kart-cekimi`: **1 $**, krediler **dahil**, %100 Gerçekleşen. (3) Billing → Credits: kalan tutar + bitiş tarihi plana yazılsın, takvime 1 ay önceye hatırlatıcı |
| **Y5** | Sunucu temeli: güncellemeler + `unattended-upgrades` · 2 GB swap · `deploy` kullanıcısı, SSH parola/root kapalı · saat dilimi UTC **ve `timedatectl` ile saat eşitlemesi açık** | 14 Ekim'de İsmail'in PC saati 3 saat kaydı → S3 yüklemesi `Signature expired` verdi (SigV4 ±5 dk). Sunucuda olursa SES/S3 çağrıları ve zamanlanmış işler bozulur |
| **Y6** | PHP **8.5** (`ppa:ondrej/php`, K87): fpm cli pgsql gd exif mbstring xml curl zip intl bcmath · php.ini `upload_max_filesize=25M`, `post_max_size=30M`, OPcache · Argon2id ölçümü (hedef ~250 ms) · PostgreSQL 18 (PGDG), yalnızca localhost · Nginx, Composer, Node 22 | Ayrıntı: backend `docs/10-URETIM-ENV-SABLONU.md` |
| **Y7** | Natro: `@` A → Lightsail statik IP, `www` → aynı (eski `redirect.natrocdn.com` kaldırılır) · `certbot --nginx` · `www`→apex ve http→https 301 · HSTS'yi **Laravel mi Nginx mi** basıyor, ikisi birden değil | Laravel `SecurityHeaders` HSTS'yi **`includeSubDomains`** ile gönderiyor → her alt alan adı HTTPS olmalı |
| **Y7.5** | **SES production erişimi talebi** (eski Y2.3) | Site canlıyken. Form metni birlikte yazılacak: işlemsel mail (parola sıfırlama), bounce/şikâyet yönetimi |
| **Y8** | Backend: GitHub **deploy key** (salt okunur, tek depo) → clone · `.env` ← `docs/10` şablonu · `key:generate` → `migrate --force` → `config:cache` → `route:cache` → `chmod 640 bootstrap/cache/config.php` · izinler | `.env`'de: `DAVETKART_MEDIA_DISK=s3`, `AWS_BUCKET=davetkart-media-438641`, `AWS_DEFAULT_REGION=eu-central-1`, **`AWS_URL=https://media.davetkart.com`**, `MAIL_MAILER=ses`, `MAIL_FROM_ADDRESS=bilgi@davetkart.com`, `FRONTEND_URL=https://davetkart.com`, `CORS_ALLOWED_ORIGINS=https://davetkart.com`, `TRUSTED_PROXIES=` (boş), `LOG_STACK=daily,sentry`, `PAYMENT_PROVIDER=fake` + **uzun rastgele webhook sırrı** |
| **Y9** | `queue:work` systemd servisi · cron `schedule:run` · `schedule:list` ile doğrula | Kuyruk yoksa parola sıfırlama maili **hiç gitmez** |
| **Y10** | Frontend: deploy key ile clone · `.env.production` (`VITE_API_BASE_URL=/api`) · `npm ci && npm run build` → Nginx kökü `dist/` | |
| **Y11** | Entegrasyon testleri (canlıda parola sıfırlama, galeri yükleme → URL `media.davetkart.com`) · Sentry DSN · Gemini anahtarı · **yedek bucket'ı `davetkart-backup-…`** (Block Public Access hiç açılmaz) + gece `pg_dump` + ömür kuralı · **geri yükleme provası** · UptimeRobot | |
| **Y12** | Canlı doğrulama: `APP_DEBUG=false`, `/.env` 404, SSL Labs A, hız sınırı gerçek IP ile, 14 MB foto 201 / 16 MB 422 | |

---

## 6. Açık kararlar (İsmail'e sor)

- **YD-5 — lansman yaklaşımı (önerildi, onay bekliyor):** Site yayına girsin; ödeme **"yakında"**; **kayıt** şu üç koşul sağlanınca açılsın: (1) KVKK aydınlatma metni + gizlilik politikası sitede, (2) SES production onayı (Y7.5), (3) ödeme ekranı sahte akış yerine "yakında" gösteriyor. İsmail "yayınlayalım, ödeme yakında, sonra tam açarım, SEO için de iyi" dedi; SEO katkısının küçük olduğu (React SPA, içerik/teknik SEO daha önemli) anlatıldı. Kesin onay alınmadı.
- **AWS kredisinin kalan tutarı ve bitiş tarihi** henüz yazılmadı (Y4.5'te).
- **SEO** (yayın sonrası ayrı iş): başlık/açıklama etiketleri, `sitemap.xml`, `robots.txt`, gerekirse prerender.

---

## 7. Süre takvimi — tek hata noktaları

| Ne | Bitiş | Durum |
|---|---|---|
| Alan adı `davetkart.com` (Natro) | **11 Eylül 2027** | 🔴 Otomatik yenileme KAPALI. Biterse site + mail + SSL aynı gün düşer |
| Natro mail hosting (Standart, 250 MB, 1 hesap) | **11 Ocak 2027** | 4 aylık ilk dönem. Yenileme **5,88 $/yıl** — önerilen: yenile. Karar Aralık ortasına kadar |
| AWS kredisi | ~Ağustos 2027 (tahmini, teyit edilmedi) | Bitince ayda ~15 $ karta |

---

## 8. Bu süreçte öğrenilen tuzaklar (tekrarlanmasın)

| Tuzak | Ders |
|---|---|
| Natro DNS "Adı" alanı alan adını **kendisi ekler** | AWS'nin verdiği adın sonundaki `.davetkart.com.` silinir; İçerik'in sonundaki **nokta** silinir |
| Natro mail sayfasındaki **yeşil ▶ düğmesi** | Liste açmaz, **mail hizmetini durdurur**. Basılmadı; basılmamalı |
| SES yeni hesabı **otomatik Essentials** planına koyuyor | à la carte'a düşürüldü. Varsayılanlar satıcının çıkarına seçilir |
| AWS Budgets **kredileri varsayılan düşüyor** | Harcama bütçesinde "Krediler" işareti kaldırılmalı |
| PC saati 3 saat kayıktı | `Signature expired` → saat ve saat dilimi düzeltildi. Sunucuda `timedatectl` kontrolü şart |
| IAM grubu ilk oluşturulurken politika eklenmemişti | Her yapılandırmadan sonra doğrula |
| Hesap/IAM/Billing sayfalarında bölge seçici **"Global"** ve kilitli | Normal; global hizmetler |
| Ücretsiz AWS planı 6 ayda **hesabı kapatır** | Bu hesap ücretli planda, sorun yok |
| Amazon WorkMail | 30 Nisan 2026'dan beri yeni müşteri almıyor, 31 Mart 2027'de kapanıyor — seçenek değil |

---

## 9. Kod tabanından deploy'u etkileyen bilgiler

- `config/filesystems.php` → s3 diskinin `'url' => env('AWS_URL')` alanı var. `media` tablosu URL değil **`disk` + `path`** saklıyor (K54) → `AWS_URL` değişince bütün eski/yeni medya adresleri kendiliğinden değişir. Göç gerekmez.
- `OptimizeUploadedImage` küçültülmüş dosyayı **yeni bir path'e** yazar, eskisini 24 saat sonra siler → URL'ler değişmez (immutable), CloudFront önbelleği hiç bayatlamaz, invalidation gerekmez.
- `SecurityHeaders` (API yanıtları): `default-src 'none'` CSP + HSTS `includeSubDomains` (yalnızca HTTPS isteklerde).
- Frontend `compressImage.ts` yalnızca yükleme öncesi yerel dosyada çalışır → medya alan adı için CORS gerekmez.
- Backend dalı `faz-10`, frontend `main`. FAZ-10 planında Dilim G (Shopier) ve Z (kapanış) açık; gerçek ödeme için G gerekiyor.
- Bu bağlantılı oturumda `device_bash` çalışıyordu (15 Ekim). PHP/Composer o ortamda yok; `composer check`'i İsmail kendi makinesinde koşturur.
