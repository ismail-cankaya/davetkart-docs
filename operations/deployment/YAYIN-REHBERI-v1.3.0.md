# Yayın rehberi — `v1.0.0` → `v1.3.0` (Faz 18–21), sunucuda yapılacaklar

> **Tarih:** 27 Kasım 2026 · **Durum gözden geçirmesi:** [`../../audits/2026-11-27-main-gap-review/REPORT.md`](../../audits/2026-11-27-main-gap-review/REPORT.md)
> **Genel kurallar:** [`YAYIN-SIRASI.md`](YAYIN-SIRASI.md) (K148 önce backend, K149 etiket) · betik ayrıntıları backend
> `docs/rehber/deploy/` · yedek [`YEDEK-VE-GERI-YUKLEME.md`](YEDEK-VE-GERI-YUKLEME.md) · izleme [`IZLEME.md`](IZLEME.md)
> ⚠️ **B7:** Bu dosyadaki sunucu komutlarının hiçbiri koşmadı. Beklenen çıktılar kılavuzlardan ve betiklerin kaynağından.
> Sır yok: `.env` değerleri buraya, sohbete ya da günlüğe yazılmaz.

**Kim, nerede:** 🖥️ yerel PowerShell · 🐧 sunucu, `deploy` kullanıcısı · 🔑 sunucu, `ubuntu` (sudo) · ☁️ AWS konsolu.
`ubuntu` `/var/www/davetkart`'a giremez (2750): o kullanıcıyla dosyaları hep **tam yolla** ve `sudo` ile oku.

## 0. Bu yayında sunucuda ne değişiyor

| Alan | Değişiklik | Kaynak | Nasıl gelir |
|---|---|---|---|
| Veritabanı | 4 göç: kısmi UNIQUE index (`orders`), `orders.first_published_at` + geriye dönük doldurma, mevcut hesaplar doğrulanmış, `orders.buyer_phone` | K158, K164, K260, K262 | `deploy.sh` → `migrate --force` |
| Dağıtım | `deploy.sh` bakım kipinde çalışır (`down` → … → `up`); etiket ve Node uyarıları | K264, K149, K272 | Kendini yeniler (adım 1b) |
| Zamanlayıcı | `media:prune-orphans` günlük → **saatlik** (:15); yeni `health-heartbeat` her dakika | K190, K255 | Kod; cron dosyası değişmedi |
| Sağlık | Yeni `GET /api/health` (veritabanı, şema, kuyruk, zamanlayıcı, disk) | K255, K263 | Kod |
| `.env` | Yeni: `DAVETKART_DELETION_LOG_DISK`, `DAVETKART_GUEST_UPLOADS`. Üretimde sıkılaşan: `DAVETKART_MEDIA_DISK` (≠ `s3` → yükleme 503), `SHOPIER_CONFIRMATION` (`callback` → ödeme uçları 503), `MAIL_MAILER` (`log` → CRITICAL) | K233, K189, K183, K170, K185 | Elle (§3.3) |
| Nginx | Güvenlik başlıkları snippet'i (SPA), bot → OG önizleme sayfası (`/invite/`), `/fonts/` önbelleği | K173, K230, K226 | Elle: `deploy/nginx/install.sh` (§4.6) |
| PHP | OPcache `validate_timestamps=0`; ayrı FPM havuzu (`[davetkart]`, 4 süreç, slowlog, durum sayfası) | K269 | Elle (§5.1) |
| Yedek | Gece `pg_dump` → ayrı S3 bucket, kalp atışı, aylık prova | K151–K157 | Elle, ayrı oturum (§6) |
| Frontend | Node 24 (`.nvmrc`), kendi fontları, paylaşım kapakları (`dist/covers/`), 404 sayfası, e-posta doğrulama ekranı | K272, K226, K235 | `deploy-frontend.sh` |

## 1. Kısa kontrol listesi

```
T-1  [ ] §2 yerelde kapılar yeşil, üç depoda main'e birleştirildi (push YOK)
     [ ] §3 sunucuda ön kontrol: sürümler, canlı commit'ler, .env, göç çakışma sorgusu = 0 satır
Gün  [ ] §4.1 Lightsail anlık görüntüsü + elle pg_dump
     [ ] §4.2 v1.0.0 ve v1.3.0 etiketleri, backend push
     [ ] §4.3 bakım kipi ELLE açık → §4.4 deploy.sh → §4.5 ara kontrol
     [ ] §4.6 frontend push + cmp + deploy-frontend.sh
     [ ] §4.7 Nginx install.sh → §4.8 duman testleri → §4.9 tarayıcı
     [ ] §5 OPcache + FPM havuzu (aynı gün, sakin saatte)
Hafta[ ] §6 yedek sistemi + ilk prova   [ ] §7 SES production + Sentry + dış izleyici
     [ ] §8 CSP gözlem haftası          [ ] §10 kayıtlar, dal temizliği
```

## 2. Yerelde hazırlık (T-1) 🖥️

### 2.1 Kapılar (yayın adayı uçlarında)

```powershell
# backend
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-21-backlog
composer sync
composer check
composer audit
git status --short
```

```powershell
# frontend (Vite KAPALI; açıksa npm ci EPERM ile yarıda kalır)
cd D:\Projects\davetkart\davetkart-frontent
git switch faz-21-backlog
npm ci
npm run check
npm run e2e
git status --short
```

Beklenen (Faz 21 §7 kaydı): `composer check` 1354/1354, `composer audit` "No security vulnerability advisories found.",
`npm run check` çıkış 0, e2e 6/6. Biri kırmızıysa **dur**.

Sözleşme kopyası (`YAYIN-SIRASI.md` §2 madde 4): `AYNI` çıkmalı.

```powershell
cd D:\Projects\davetkart
$fark = Compare-Object (Get-Content davetkart-backend-php-laravel\contracts\plan-rules.json) `
                       (Get-Content davetkart-frontent\src\contracts\plan-rules.json)
if ($fark) { 'FARKLI'; $fark } else { 'AYNI' }
```

### 2.2 İsteğe bağlı: iki commit konusunu yeniden adlandır

fe `2cc799f` ve docs `56a65ca` konusunda proje kural dosyasının adı geçiyor (Faz 21 §6 21.90). Değiştireceksen **push'tan önce**
yap; push'tan sonra geçmiş yeniden yazılmaz. Yöntem Faz 21 §6 21.90'da.

### 2.3 `main`'e birleştir (push yok)

`main` üç depoda da aday dalın atası; birleştirme çakışmasız.

```powershell
# backend
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch main
git pull --ff-only
git merge --no-ff faz-21-backlog -m "Merge faz-21-backlog into main (Faz 18-21, AUD-2026-11-12, AUD-2026-11-26)"
git log --oneline -1
git status --short
```

```powershell
# frontend
cd D:\Projects\davetkart\davetkart-frontent
git switch main
git pull --ff-only
git merge --no-ff faz-21-backlog -m "Merge faz-21-backlog into main (Faz 18-21, AUD-2026-11-12, AUD-2026-11-26)"
git log --oneline -1
git status --short
```

```powershell
# docs (bu rehberi içeren dal önce docs/2026-11-27-faz-21-backlog'a alınmış olmalı)
cd D:\Projects\davetkart\davetkart-docs
git switch main
git pull --ff-only
git merge --no-ff docs/2026-11-27-faz-21-backlog -m "Merge docs/2026-11-27-faz-21-backlog into main (Faz 18-21 records)"
git log --oneline -1
git status --short
```

Birleşik `main`'de §2.1 kapılarını bir kez daha koş (ağaç aynı olmalı; `git diff faz-21-backlog main --stat` boş).

## 3. Sunucuda ön kontrol (T-1, kesintisiz)

### 3.1 Sürümler ve servisler 🐧

```bash
php -v | head -1                         # PHP 8.5.12 ya da üstü (CVE kuralı, Y6.1a)
node --version                           # v24.x (frontend .nvmrc = 24)
git -C /var/www/davetkart/backend status --short     # boş
git -C /var/www/davetkart/frontend status --short    # boş
df -h /                                  # %90 altında (sağlık ucu %90'da 503)
free -m
systemctl is-active php8.5-fpm nginx postgresql cron davetkart-queue   # hepsi active
```

### 3.2 Canlıdaki commit'ler → `v1.0.0` 🐧

```bash
git -C /var/www/davetkart/backend rev-parse --short HEAD    # beklenen 03d3940
git -C /var/www/davetkart/frontend rev-parse --short HEAD   # beklenen 47aedc8
```

Farklıysa `v1.0.0`'ı **sunucudaki** commit'lere at (§4.2), `main`'den tahmin etme.

### 3.3 `.env` 🐧

Yalnızca sır olmayan anahtarları göster:

```bash
cd /var/www/davetkart/backend
grep -E '^(APP_ENV|APP_DEBUG|APP_URL|AWS_URL|DAVETKART_MEDIA_DISK|MAIL_MAILER|PAYMENT_PROVIDER|PAYMENT_METHODS|SHOPIER_CONFIRMATION|LOG_STACK|DAVETKART_GUEST_UPLOADS|DAVETKART_DELETION_LOG_DISK)=' .env
```

| Anahtar | Olmalı | Değilse |
|---|---|---|
| `APP_ENV` / `APP_DEBUG` | `production` / `false` | — |
| `APP_URL` | `https://davetkart.com` | K184 |
| `AWS_URL` | `https://media.davetkart.com` | Görseller 403 (K184) |
| `DAVETKART_MEDIA_DISK` | `s3` | 🔴 Yeni sürümde yükleme 503 (K183) |
| `MAIL_MAILER` | `ses` | Her postada CRITICAL (K185) |
| `SHOPIER_CONFIRMATION` | `osb` ya da satır yok (varsayılan `osb`) | 🔴 `callback` → ödeme uçları 503 (K170) |
| `DAVETKART_GUEST_UPLOADS` | **ekle:** `false` | Varsayılan zaten `false`; açık yazmak niyeti belgeler (K189) |
| `DAVETKART_DELETION_LOG_DISK` | **ekle:** `s3` | Yoksa `local`: Lightsail görüntüsüne dönülünce günlük kaybolur (K233) |

`nano .env` ile iki satırı ekle (şablon: backend `docs/10-URETIM-ENV-SABLONU.md`). `config:cache` gerekmez: deploy yapar.
İzinler değişmemeli: `ls -l .env` → `-rw-r----- deploy www-data`.

### 3.4 Göç çakışma sorgusu 🔑

`2026_11_16` göçü çakışan veri varsa **bilerek durur** (K162) ve site bakım kipinde kalır. Önceden bak:

```bash
sudo -u postgres psql -d davetkart -c "SELECT user_id, COUNT(*) FROM orders WHERE status = 'pending' AND promotion = 'first_publish' AND user_id IS NOT NULL GROUP BY user_id HAVING COUNT(*) > 1;"
```

Beklenen `(0 rows)`. Satır varsa çözüm backend `docs/rehber/database/migrations/2026_11_16_100000_add_one_pending_first_publish_index_to_orders.md` §4;
deploy'dan önce kapat.

## 4. Yayın günü

Trafiğin en az olduğu saat. Toplam kesinti beklentisi: API için ~1–3 dk (bakım kipi), statik site açık.
Dış izleyici kuruluysa önce bakım penceresi aç (`IZLEME.md` §3).

### 4.1 Geri dönüş noktası ☁️ 🔑

1. ☁️ Lightsail → `davetkart-prod` → **Snapshots (Anlık görüntüler)** → **Create snapshot**: `davetkart-prod-pre-v1-3-0`.
   Bitmesini bekle. Gece yedeği henüz kurulu değil (§6); elindeki tek tam kopya bu ve otomatik görüntüler.
2. 🔑 Elle veritabanı dökümü (RPO'yu o an için sıfırlar):

```bash
F=/var/lib/postgresql/davetkart-pre-v1.3.0-$(date -u +%Y%m%dT%H%MZ).dump
sudo -u postgres pg_dump -Fc -d davetkart -f "$F"
sudo -u postgres pg_restore --list "$F" | head -3      # okunabiliyor mu
sudo ls -l "$F"
```

Dosya kişisel veri içerir: sunucudan çıkarma, bir hafta sonra sil.

3. 🔑 Nginx'in bugünkü dosyasını sakla (geri alma için; `v1.0.0`'da `install.sh` yok):

```bash
sudo cp -p /etc/nginx/sites-available/davetkart.conf /root/davetkart.conf.v1.0.0
```

### 4.2 Etiketler ve backend push 🖥️

```powershell
# backend: v1.0.0 = sunucudaki commit (§3.2), v1.3.0 = birleşik main
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git tag -a v1.0.0 03d3940 -m "Release v1.0.0: first production deploy (26 Oct 2026)"
git tag -a v1.3.0 main -m "Release v1.3.0: Faz 18-21 audit fixes (AUD-2026-11-12, AUD-2026-11-26)"
git describe --tags --exact-match main
git status --short
```

```powershell
# frontend: etiketler şimdi, push §4.6'da
cd D:\Projects\davetkart\davetkart-frontent
git tag -a v1.0.0 47aedc8 -m "Release v1.0.0: first production deploy (26 Oct 2026)"
git tag -a v1.3.0 main -m "Release v1.3.0: Faz 18-21 audit fixes (AUD-2026-11-12, AUD-2026-11-26)"
git describe --tags --exact-match main
git status --short
```

`v1.1.0` / `v1.2.0`: isteğe bağlı tarihî işaret (`phases/faz-21/FAZ-21-ARC-08-KOMUTLARI.md` §3). `v1.2.0` önerilen uçta `composer audit`
kırmızı (`SEC-51`); yayın etiketi olarak kullanılmaz.

```powershell
# backend push (yalnızca backend; frontend main'i HENÜZ itme)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git push origin main
git push origin v1.0.0
git push origin v1.3.0
git status --short
```

### 4.3 Bakım kipini elle aç 🐧

Canlıdaki `deploy.sh` eski sürüm: `git pull`'u bakım kipi olmadan yapar, yeni betiğe ancak ondan sonra geçer (backend
`docs/rehber/deploy/deploy.md` adım 0b ⚠️). O birkaç saniyede yeni kod eski `vendor/` ve eski şemayla cevap verebilir.
Bu yayına özel: kipi pull'dan **önce** elle aç.

```bash
cd /var/www/davetkart/backend
sudo -n -u www-data /usr/bin/php artisan down --retry=60
curl -s -o /dev/null -w '%{http_code}\n' https://davetkart.com/api/ping    # 503
```

Kipi yeni `deploy.sh` kapatır (`artisan up`). Sonraki yayınlarda bu adım yok.

### 4.4 Backend deploy 🐧

```bash
cd /var/www/davetkart/backend
bash deploy/deploy.sh
```

Günlükte sırayla görmen gerekenler:

```
==> Kod cekiliyor (onceki surum: 03d3940)
==> deploy/ betikleri degisti: yeni surumle yeniden baslatiliyor
==> Bakim kipi aciliyor (API 503)          # zaten açık: yalnızca seçenekleri yeniler
==> Surum: <kimlik> (v1.3.0)
==> Veritabani gocleri                      # 4 göç DONE
==> Bakim kipi kapaniyor
==> Backend bitti: 03d3940 -> <kimlik> (v1.3.0)
==> [frontend] ...                          # frontend main itilmediği için 47aedc8'i yeniden derler: zararsız
```

- `(etiketsiz)` görürsen `v1.3.0` itilmemiştir: deploy sürer, frontend'e geçmeden it.
- `Site BAKIM KIPINDE kaliyor (503)`: deploy yarıda kaldı. `artisan up` **yapma** (yarım şema). Sebebi düzelt, `bash deploy/deploy.sh`'ı
  yeniden çalıştır. Göç çakışma mesajıysa §3.4.
- `composer install` `ext-…` isterse PHP eklentisi eksik: `composer check-platform-reqs --no-dev`.

### 4.5 Ara kontrol 🐧

```bash
cd /var/www/davetkart/backend
A="sudo -n -u www-data /usr/bin/php artisan"
git describe --tags --exact-match HEAD          # v1.3.0
$A migrate:status --pending                     # bekleyen göç yok
$A plans:export --check                         # "Plan kurallari sozlesmesi guncel."
$A about --only=davetkart                       # Media disk: s3 · Mail mailer: ses
$A env:template --env=.env --check              # "missing in .env" satırı olmamalı (yalnızca anahtar adları basılır)
$A schedule:list                                # media:prune-orphans saatlik :15 · health-heartbeat her dakika
systemctl is-active davetkart-queue             # active
sleep 70; curl -s https://davetkart.com/api/health; echo     # {"status":"ok"}
```

`/api/health` ilk dakikada `scheduler` diye 503 verebilir (kalp atışı henüz yazılmadı); bir dakika sonra tekrar bak.
Kalıcı 503'te hangi kontrolün düştüğü: `IZLEME.md` §1. `plans:export --check` kırmızıysa **dur**, frontend'i yayınlama.

### 4.6 Frontend 🖥️ 🐧

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git push origin main
git push origin v1.0.0
git push origin v1.3.0
git status --short
```

```bash
# sunucuda, deploy
cd /var/www/davetkart/frontend
git fetch origin
git show origin/main:src/contracts/plan-rules.json \
  | cmp - /var/www/davetkart/backend/contracts/plan-rules.json && echo "sozlesme ayni"
bash /var/www/davetkart/backend/deploy/deploy-frontend.sh
```

Beklenen: `sozlesme ayni`, ardından `==> [frontend] Surum: <kimlik> (v1.3.0) | backend: v1.3.0` ve Node uyarısı **yok**.
`cmp` fark bulursa yayınlama (`YAYIN-SIRASI.md` §4.3).

### 4.7 Nginx 🔑

Önce canlıdaki dosya depodaki eski sürümle aynı mı (sunucuda elle değişiklik var mı):

```bash
sudo -u deploy git -C /var/www/davetkart/backend show 03d3940:deploy/nginx/davetkart.conf \
  | sudo diff - /etc/nginx/sites-available/davetkart.conf && echo "canli dosya = v1.0.0"
```

Fark çıkarsa önce onu anla: `install.sh` siteyi depodakiyle değiştirir. Sonra:

```bash
sudo bash /var/www/davetkart/backend/deploy/nginx/install.sh
```

Beklenen son satır `Bitti. Simdi duman testi: …`. `nginx -t kirmizi: eski dosyalar geri kondu` görürsen site değişmemiştir;
hatayı oku (backend `docs/rehber/deploy/nginx/install.md`).

### 4.8 Duman testleri 🐧

```bash
cd /var/www/davetkart/backend
bash deploy/smoke/check-security-headers.sh --resolve davetkart.com:443:127.0.0.1 https://davetkart.com
bash deploy/smoke/check-share-preview.sh https://davetkart.com <yayindaki-bir-davetiye-id>
curl -sI https://davetkart.com/api/ping | grep -i x-request-id      # ULID (K268)
```

Beklenen: iki betikte de `SONUC: tamam`. Başlık betiği kırmızıysa yayın geri alınmaz (site çalışır); Nginx düzeltilip §4.7 tekrarlanır.

### 4.9 Tarayıcıda (gizli pencere) 🖥️

| # | Akış | Beklenen |
|---|---|---|
| 1 | Mevcut hesapla giriş → Hesap Ayarları'nın beş sayfası | Hepsi açılır ("Bir aksaklık oldu" yok; `AUD-2026-11-26` §1) |
| 2 | Davetiye oluştur → yenile (`/create/<id>`) | Editör kaybolmaz (FE-50) |
| 3 | Hediye koduyla yayınla | Yayında; panelde hak "kullanıldı" (SEC-02) |
| 4 | Misafir olarak LCV | Panelde görünür |
| 5 | Davetiye bağlantısını WhatsApp'ta paylaş | Önizleme kartı (FE-04; B-İ3) |
| 6 | `/olmayan-sayfa` | 404 sayfası (FE-06) |
| 7 | **Yeni** hesap aç | Doğrulama postası: SES sandbox'ta yalnızca doğrulanmış adrese gelir (§7) |
| 8 | DevTools → Network: font istekleri | Yalnızca `/fonts/…`, Google yok (SEC-12) |
| 9 | DevTools → Console | `report-only` CSP satırlarını not et (§8) |

## 5. Aynı gün, sakin saatte: OPcache ve FPM havuzu 🔑

### 5.1 Kurulum

İsteğe bağlı ama önerilen (K269). FPM yeniden başlarken ~1 sn 502 olabilir.

```bash
B=/var/www/davetkart/backend
sudo diff /etc/php/8.5/mods-available/davetkart.ini "$B/deploy/php/davetkart.ini"   # yalnızca OPcache satırları farklı olmalı
sudo cp "$B/deploy/php/davetkart.ini" /etc/php/8.5/mods-available/davetkart.ini
sudo cp "$B/deploy/php-fpm/davetkart.conf" /etc/php/8.5/fpm/pool.d/davetkart.conf
sudo mv /etc/php/8.5/fpm/pool.d/www.conf /etc/php/8.5/fpm/pool.d/www.conf.dist      # aynı soket; silinmez
sudo touch /var/log/php8.5-fpm-davetkart.slow.log
sudo chown www-data:www-data /var/log/php8.5-fpm-davetkart.slow.log
sudo php-fpm8.5 -t                                    # "test is successful"
sudo systemctl restart php8.5-fpm
curl -fsS https://davetkart.com/api/ping; echo
sudo php-fpm8.5 -i | grep -E '^opcache\.(validate_timestamps|memory_consumption)'   # 0 · 128
```

Geri alma: `sudo mv /etc/php/8.5/fpm/pool.d/www.conf.dist /etc/php/8.5/fpm/pool.d/www.conf`,
`sudo rm /etc/php/8.5/fpm/pool.d/davetkart.conf`, `sudo systemctl restart php8.5-fpm`.

**Bellek (21.5 sorusu):** 4 süreç × 256 MB + kuyruk 768 MB tavanları toplamı 2 GB'ı ~220 MB aşıyor. Sunucuda 2 GB takas zaten var
(Y5.2, `vm.swappiness=10`). Öneri: ayarı olduğu gibi bırak, ilk hafta `journalctl -k | grep -i oom` ve `free -m`'e bak (`IZLEME.md` §6).

### 5.2 Bundan sonra değişen alışkanlık

`validate_timestamps=0` ile PHP diskteki dosyayı **reload olmadan görmez**. `deploy.sh` bunu yapar. Elle bir şey değiştirirsen:

| Ne yaptın | Ardından |
|---|---|
| `.env` düzenledin | `artisan config:cache` **ve** `sudo systemctl reload php8.5-fpm` (`config.php` bir PHP dosyası) |
| Kod dosyasına elle dokundun (yapma) | `reload php8.5-fpm` |

### 5.3 İsteğe bağlı: Nginx günlüğünde istek kimliği (K268)

Site dosyası her `install.sh`'ta depodan yazılır; bu yüzden ayrı dosyaya koy (`conf.d` http bağlamında okunur):

```bash
sudo tee /etc/nginx/conf.d/davetkart-log.conf >/dev/null <<'EOF'
log_format davetkart '$remote_addr - [$time_local] "$request" $status $body_bytes_sent $request_time rid=$upstream_http_x_request_id';
access_log /var/log/nginx/davetkart.access.log davetkart;
EOF
sudo nginx -t && sudo systemctl reload nginx
```

Ayrıntı: backend `docs/rehber/app/Http/Middleware/AssignRequestId.md` §6.

### 5.4 Tek seferlik komutlar 🐧

```bash
A="sudo -n -u www-data /usr/bin/php /var/www/davetkart/backend/artisan"
$A media:move-disk --dry-run                    # 'public' diskte medya var mı (Hat A İ8); 0 ise iş yok
$A invitations:prune-empty-drafts --dry-run     # boş eski taslaklar (K261); sayıya bakıp istersen --dry-run'sız
```

`media:move-disk` dosya bulursa: `$A media:move-disk` → doğrula → `$A media:move-disk --delete-source` (Hat A §9 E6).

## 6. İlk hafta: gece yedeği (`OPS-02`) ☁️ 🔑

Canlıda bugün yalnızca Lightsail görüntüsü var. Kitap: [`YEDEK-VE-GERI-YUKLEME.md`](YEDEK-VE-GERI-YUKLEME.md), bu sırayla:

1. §2 yedek bucket'ı (Frankfurt, Block Public Access 4/4, sürümleme, 30 + 7 gün ömür kuralı).
2. §3 `davetkart-backup` kimliği (yalnızca yazma).
3. §4.1 AWS CLI kurulumu (karar senin), §4.2–§4.5 betik + `/etc/davetkart/backup.env` + S3'süz deneme + ilk gerçek koşu.
4. §4.6 cron: `deploy/cron/davetkart-backup` → `/etc/cron.d/davetkart-backup` (02:00 UTC).
5. §5 doğrulama, §6 **ilk üretim provası** ve RTO'yu kayda yaz.
6. Yedek bucket'ı açılınca gizlilik metnindeki süreyi panelle karşılaştır (Hat B B-İ4).

## 7. İlk hafta: posta ve izleme

| # | İş | Neden şimdi | Kaynak |
|---|---|---|---|
| 1 | ☁️ **SES production erişimi** talebi | 🔴 Yeni hesaplar doğrulama postası almadan ödeme/yayın yapamaz (`SEC-09`, K191). Sandbox'ta posta yalnızca doğrulanmış adreslere gider. Mevcut hesaplar K260 ile etkilenmez | `YAYIN-PLANI.md` Y7.5 |
| 2 | Sentry DSN + `LOG_STACK=daily,sentry` → `config:cache` + FPM reload (§5.2) → `sentry:test` | Başarısız iş ve 5 zamanlanmış işin takibi | `IZLEME.md` §2 |
| 3 | Dış izleyici: `/api/health` (1 dk, 2 ardışık hata), SSL bitişi (14 gün), yedek kalp atışları | Site ya da yedek düşerse haber | `IZLEME.md` §3–§4 |
| 4 | Elle doğrulama: cron'u 6 dk durdur → `scheduler` 503; kuyruğu durdur → `queue` 503 | Alarmın gerçekten çaldığını görmek | `IZLEME.md` §5 |
| 5 | Natro: alan adı otomatik yenileme; posta kararı **11 Aralık**'a kadar | Tek hata noktaları | `SURE-TAKVIMI.md` |

## 8. Yayından sonraki hafta: CSP gözlemi

Tam CSP **rapor kipinde** (K175). Ödeme dahil akışları gez, DevTools → Console'daki `report-only Content Security Policy`
satırlarını not et. Temizse zorlamaya geçiş ayrı değişiklik ve ayrı karar (backend
`docs/rehber/deploy/nginx/snippets/davetkart-security-headers.md` §5). `SEC-18` (çerezli oturum) bunun arkasında bekliyor.

## 9. Geri alma

🔴 Sıra tersine döner: **önce frontend, sonra backend.**

| Durum | Ne yap |
|---|---|
| Deploy bakımda kaldı | `artisan up` yapma; sebebi düzelt, `bash deploy/deploy.sh` (backend `deploy.md` §4) |
| Yalnızca yeni arayüz bozuk | 🐧 `cd /var/www/davetkart/frontend && mv dist dist.bad && mv dist.old dist` |
| Nginx bozuk | 🔑 `sudo cp -p /root/davetkart.conf.v1.0.0 /etc/nginx/sites-available/davetkart.conf && sudo nginx -t && sudo systemctl reload nginx`. Snippet dosyası kalabilir (eski site onu `include` etmez) |
| FPM havuzu bozuk | §5.1 geri alma |
| Sürümün tamamı geri | `YAYIN-SIRASI.md` §5.2: `main`'de `v1.0.0` ağacına dönen yeni commit + `v1.3.1` etiketi, önce frontend. ⚠️ `v1.0.0`'ın `deploy.sh`'ında bakım kipi yok: o deploy'dan önce §4.3'teki gibi elle `down` |
| Veri bozuldu | Son çare: §4.1'deki döküm (`YEDEK-VE-GERI-YUKLEME.md` §7). Dökümden sonraki bütün yazılar kaybolur |

Göçler geri alınmaz; dördü de geriye uyumlu: eski kod yeni sütunları okumaz, kısmi index yalnızca ikinci bekleyen indirimli siparişi
engeller, `email_verified_at` doldurması zararsız (`down()` yok).

## 10. Yayından sonra kayıt

- `YAYIN-PLANI.md` §8 ilerleme kaydına satırlar: tarih, `v1.3.0`, iki commit, kesinti süresi, göç çıktısı, §4.5 ve §4.8 sonuçları.
- `phases/faz-18…21` tablolarında durum `birleşti`; `phases/README.md`.
- `YAYIN-SIRASI.md` §3'teki "`v1.1.0`'da ilk kez" notları artık `v1.3.0` için geçerli (tarihî metin değiştirilmez, not düşülür).
- Dal ve worktree temizliği: `phases/faz-21/FAZ-21-ARC-08-KOMUTLARI.md` §4 (yalnızca `--merged`, `-d`).
- §4.1'deki dökümü bir hafta sonra sil; elle anlık görüntüyü otomatikler yeterince birikince sil.
- Eski kod arşivleri (`SEC-17`): içindeki AWS ve Gemini anahtarları doluysa döndür (Faz 21 Ek B.3).
