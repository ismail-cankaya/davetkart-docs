# Yedek ve geri yükleme — çalıştırma kitabı

> **Tarih:** 16 Kasım 2026 · **Kaynak:** `AUD-2026-11-12` → `OPS-02` (Faz 18.2) · **Kararlar:** K151–K157
> ([`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md))
> **Ne bu:** Gece veritabanı yedeğinin kurulumu, doğrulaması, aylık provası ve gerçek kurtarma adımları.
> [`YAYIN-PLANI.md`](YAYIN-PLANI.md) Y11.5 ve Y11.6'nın uygulaması. Betiklerin ayrıntısı backend deposunda:
> `docs/rehber/deploy/backup/pg-dump.md`, `docs/rehber/deploy/backup/restore-drill.md`,
> `docs/rehber/deploy/cron/davetkart-backup.md`.
> ⚠️ **B7:** §2–§5 ve §7'deki AWS ve sunucu adımları **yazıldı, çalıştırılmadı.** Betikler yerelde denendi
> (sonuçlar: backend `docs/rehber/fazlar/FAZ-18.md` §18.2). Gerçek S3 yüklemesi ve üretim provası İsmail'in elle işi.
> **Yer tutucu:** `<YEDEK-BUCKET>` = senin seçeceğin bucket adı (plan kaydı `davetkart-backup-…` diyor). Bu dosyaya
> anahtar, parola ya da hesap numarası yazılmaz.
> **Konsol adları** `English (Türkçe)` biçiminde. Türkçe karşılıklar konsolda birebir böyle olmayabilir; İngilizce ad esastır.

## 1. Özet

| Katman | Sıklık | Saklama | Çözdüğü felaket |
|---|---|---|---|
| Lightsail disk görüntüsü (Y4.4) | Her gün 01:00 UTC | 7 gün | Sunucu yandı: bütün makine dünkü hâline döner |
| `pg_dump` dökümü → S3 (bu kitap) | Her gün 02:00 UTC | 30 gün (+7 gün eski sürüm) | Veri bozuldu: tek tablo ya da dünkü veri geri gelir |

| Ölçü | Değer |
|---|---|
| **RPO** (en çok ne kadar veri kaybı) | 24 saat. Bilinçli kabul (K157). Riskli göçten önce elle bir koşu bunu o an için sıfırlar (§4.5) |
| **RTO** (ne kadar sürede dönüş) | **Henüz ölçülmedi.** İlk üretim provasında ölçülür ve §6'daki kayda yazılır |

Kim neye erişir (en az yetki, K153):

| Kimlik | Nerede durur | Medya bucket'ı | Yedek bucket'ı |
|---|---|---|---|
| `davetkart-app` | Sunucuda `.env` (`www-data` okur) | Oku, yaz, sil | **Erişim yok** |
| `davetkart-backup` | Sunucuda `/etc/davetkart/backup.env` (yalnızca root okur) | Erişim yok | **Yalnızca yaz** (`daily/*`); okuyamaz, listeleyemez, silemez |
| `ismail-admin` (MFA) | Senin konsol oturumun | Tam | Tam: geri yükleme ve silme yalnızca buradan |

Web uygulaması ele geçirilirse yedeklere ulaşılamaz. Sunucunun tamamı (root) ele geçirilirse saldırgan
yedekleri **okuyamaz ve silemez**; yalnızca yeni nesne yazabilir (sınırı: §10).

## 2. Yedek bucket'ı ☁️

`ismail-admin` ile, bölge **eu-central-1 (Frankfurt)**.

1. **S3** → **Buckets (Kovalar)** → **Create bucket (Kova oluştur)**
   - **Bucket type (Kova türü):** General purpose (Genel amaçlı)
   - **Bucket name (Kova adı):** `<YEDEK-BUCKET>` (küçük harf; medya bucket'ındaki gibi `davetkart-backup-` + kısa son ek)
   - **Object Ownership (Nesne sahipliği):** ACLs disabled (ACL'ler devre dışı)
   - **Block Public Access settings for this bucket (Bu kova için genel erişimi engelleme ayarları):**
     **Block all public access (Tüm genel erişimi engelle)** işaretli, dört alt kutu da işaretli. **Hiç açılmaz.**
   - **Bucket Versioning (Kova sürümleme):** Enable (Etkinleştir)
   - **Default encryption (Varsayılan şifreleme):** Server-side encryption with Amazon S3 managed keys (SSE-S3)
   - **Create bucket (Kova oluştur)**
2. Bucket → **Management (Yönetim)** → **Lifecycle rules (Yaşam döngüsü kuralları)** →
   **Create lifecycle rule (Yaşam döngüsü kuralı oluştur)**
   - **Lifecycle rule name (Kural adı):** `yedekleri-30-gunde-sil`
   - **Rule scope (Kural kapsamı):** Apply to all objects in the bucket (Kovadaki tüm nesnelere uygula) + onay kutusu
   - **Lifecycle rule actions (Kural eylemleri):**
     - ☑ **Expire current versions of objects (Nesnelerin geçerli sürümlerinin süresini doldur):** 30 gün
     - ☑ **Permanently delete noncurrent versions of objects (Geçerli olmayan sürümleri kalıcı olarak sil):** 7 gün
     - ☑ **Delete expired object delete markers or incomplete multipart uploads (Süresi dolmuş silme
       işaretçilerini veya tamamlanmamış çok parçalı yüklemeleri sil)** → **Delete incomplete multipart
       uploads (Tamamlanmamış çok parçalı yüklemeleri sil):** 7 gün
   - **Create rule (Kural oluştur)**
3. Doğrula: **Properties (Özellikler)** → Bucket Versioning **Enabled**, Default encryption **SSE-S3** ·
   **Permissions (İzinler)** → Block all public access **On** · **Management (Yönetim)** → kural **Enabled**.

**Sürümleme açıkken "silme" iki adımdır.** 30. günde nesne silinmez; üstüne bir *silme işaretçisi* konur ve
nesne "eski sürüm" olur. Eski sürüm 7 gün sonra kalıcı silinir. Yani bir döküm en çok **~37 gün** yaşar
(S3 kuralları günde bir kez işlediği için bir gün daha gecikebilir). Bu sayı gizlilik metnine girecek
sayıdır (§9, `SEC-11`).

Silme işaretçileri yer tutmaz; birikmeleri maliyet değil kalabalık sorunudur. Konsol aynı kuralda izin
vermezse "Delete expired object delete markers" için ikinci bir kural açılabilir (isteğe bağlı).

## 3. Yedek kimliği ☁️

1. **IAM** → **Users (Kullanıcılar)** → **Create user (Kullanıcı oluştur)**
   - **User name (Kullanıcı adı):** `davetkart-backup`
   - **Provide user access to the AWS Management Console (Kullanıcıya AWS Yönetim Konsolu erişimi ver):** işaretsiz
   - İzin ekleme adımını boş geç → **Create user (Kullanıcı oluştur)**
2. Kullanıcı → **Permissions (İzinler)** → **Add permissions (İzin ekle)** →
   **Create inline policy (Satır içi politika oluştur)** → **JSON**. `<YEDEK-BUCKET>`'ı değiştir:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "YalnizcaGunlukYedekYaz",
         "Effect": "Allow",
         "Action": "s3:PutObject",
         "Resource": "arn:aws:s3:::<YEDEK-BUCKET>/daily/*"
       }
     ]
   }
   ```

   **Policy name (Politika adı):** `davetkart-backup-yalnizca-yaz`
3. Kullanıcı → **Security credentials (Güvenlik kimlik bilgileri)** → **Access keys (Erişim anahtarları)** →
   **Create access key (Erişim anahtarı oluştur)** → kullanım amacı: **Application running outside AWS
   (AWS dışında çalışan uygulama)** → açıklama `lightsail-prod-yedek`.
   Gizli anahtar **yalnızca bir kez** gösterilir: parola yöneticisine kaydet. Sohbete, bu depoya ve
   `.env`'e yazma; tek evi sunucudaki `/etc/davetkart/backup.env`.

Politikada bilerek **olmayanlar**:

| Yok | Neden |
|---|---|
| `s3:GetObject` | Sunucu ele geçirilirse eski yedekler (misafir adları, e-postalar) indirilemesin |
| `s3:ListBucket` | Hangi yedeklerin olduğu bile görülemesin |
| `s3:DeleteObject`, `s3:DeleteObjectVersion` | Saldırgan izini silmek için yedekleri yok edemesin |
| `s3:AbortMultipartUpload` | Gerek yok: yarım kalan yüklemeyi §2'deki ömür kuralı 7 günde temizler. `aws` hata anında bunu dener ve reddedilir; günlükte ek bir `AccessDenied` satırı görürsen sebebi budur |

Büyük dosyada `aws s3 cp` çok parçalı yükleme yapar; onun da gerektirdiği izin `s3:PutObject`'tir.

## 4. Sunucuya kurulum 🐧

`ubuntu` kullanıcısıyla (root yetkisi gerekir; `deploy` yapamaz ve yapmamalı).

### 4.1 AWS CLI — 🔶 karar senin

Plan kaydında sunucuda `aws` komutu yok. Betik yalnızca `aws` adında çalışan bir komut ister; nasıl
kurulduğuna bakmaz. Ubuntu 24.04'ün deposunda `awscli` paketi bulunmuyor (doğrula: `apt-cache policy awscli`).

| Seçenek | Komut | Artı | Eksi |
|---|---|---|---|
| **(a) Resmî kurucu, v2** (öneri) | aşağıda | İmzası doğrulanır; snap'e bağımlılık yok (Composer ve Node kurulumlarıyla aynı tutum) | Güncelleme elle: aylık provada `--update` |
| (b) snap | `sudo snap install aws-cli --classic` | Tek komut, kendiliğinden güncellenir | Plan snap'ten kaçındı (certbot, Y7.2b); güncelleme anını sen seçmezsin |

```bash
# (a) resmî kurucu
cd /tmp
curl -fsSLo awscliv2.zip https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip
curl -fsSLo awscliv2.sig https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip.sig
# İmza: AWS CLI ekibinin açık anahtarını ve parmak izini RESMÎ kurulum sayfasından al
# ("Verifying the integrity of your downloaded zip file"), gpg --import ile ekle, sonra:
gpg --verify awscliv2.sig awscliv2.zip        # "Good signature" ve parmak izi sayfadakiyle aynı olmalı
unzip -q awscliv2.zip                          # unzip yoksa: sudo apt install -y unzip
sudo ./aws/install                             # /usr/local/bin/aws
aws --version
rm -rf aws awscliv2.zip awscliv2.sig
```

Parmak izini bu dosyaya yazmadım: doğrulayamadığım bir değeri kaynak göstermek istemem.

### 4.2 Betikleri sunucuya getir

**Yol A (Faz 18 yayınından sonra):** dosyalar `git pull` ile zaten `/var/www/davetkart/backend/deploy/` altında.

**Yol B (yayını beklemeden):** kurulu kopyalar depo klasöründen bağımsızdır; üç dosyayı kendi makinenden gönder.

```powershell
# yerelde, backend deposunda (dal: fix/2026-11-16-ops-02-db-backup ya da faz-18-audit-fixes)
scp -i $env:USERPROFILE\.ssh\davetkart_lightsail deploy\backup\pg-dump.sh deploy\backup\backup.env.example deploy\cron\davetkart-backup ubuntu@<SUNUCU-IP>:/tmp/
```

```bash
# sunucuda: Windows satır sonu gelmediğini doğrula (hepsi 0 olmalı)
grep -c $'\r' /tmp/pg-dump.sh /tmp/backup.env.example /tmp/davetkart-backup
```

Aşağıdaki komutlarda `KAYNAK` bu iki yoldan biridir:

```bash
KAYNAK=/var/www/davetkart/backend/deploy     # Yol A   (dosyalar: $KAYNAK/backup/…, $KAYNAK/cron/…)
```

Yol B'de dosyalar `/tmp` altında düzdür; komutlardaki `$KAYNAK/backup/` ve `$KAYNAK/cron/` yerine `/tmp/` yaz.

### 4.3 Ayar dosyası

```bash
sudo install -d -m 700 -o root -g root /etc/davetkart
sudo install -m 600 -o root -g root "$KAYNAK/backup/backup.env.example" /etc/davetkart/backup.env
sudo nano /etc/davetkart/backup.env       # BACKUP_S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
sudo stat -c '%U:%a' /etc/davetkart/backup.env      # root:600
```

Betik bu dosyanın sahibi root ve izni `600` değilse çalışmayı reddeder.

### 4.4 Betiğin kurulu kopyası ve S3'süz deneme

```bash
sudo install -m 755 -o root -g root "$KAYNAK/backup/pg-dump.sh" /usr/local/sbin/davetkart-pg-dump
sudo bash -n /usr/local/sbin/davetkart-pg-dump && echo "sozdizimi temiz"

# Önce S3'e gitmeden: root + postgres (peer) + anlık görüntü + doğrulama zinciri çalışıyor mu?
sudo /usr/local/sbin/davetkart-pg-dump --local /root/yedek-deneme
sudo ls -l /root/yedek-deneme
sudo cat /root/yedek-deneme/*.manifest.json
sudo rm -r /root/yedek-deneme
```

Beklenen son satır: `TAMAM: /root/yedek-deneme/davetkart-<damga>.dump (… bayt, 21 tablo, … satir, … sn)`.

Neden kopya: root, `deploy` kullanıcısının yazabildiği bir dosyayı çalıştırırsa `deploy` fiilen root olur.
Depodaki betik değişince bu `install` satırı **yeniden** çalıştırılır.

### 4.5 İlk gerçek koşu

```bash
sudo /usr/local/sbin/davetkart-pg-dump
```

Beklenen: `==> S3'e yukleniyor: s3://<YEDEK-BUCKET>/daily/YYYY/MM/DD` ve `TAMAM: …`. Sonra §5.

Bu komut her zaman elle de çalıştırılabilir: **riskli bir göçten hemen önce** çalıştır, o anın yedeği olsun.

### 4.6 Cron (en son)

```bash
sudo install -m 644 -o root -g root "$KAYNAK/cron/davetkart-backup" /etc/cron.d/davetkart-backup
ls -l /etc/cron.d/davetkart-backup        # -rw-r--r-- root root
timedatectl | grep "Time zone"            # Etc/UTC olmalı; cron sistem saatini kullanır
```

## 5. Doğrulama

**Konsolda:** S3 → `<YEDEK-BUCKET>` → `daily/YYYY/MM/DD/` → iki dosya: `davetkart-<damga>.dump` ve
`davetkart-<damga>.manifest.json`. Manifest varsa o koşu tamdır (betik önce dökümü, sonra manifesti yükler).
Dosyanın **Properties (Özellikler)** sekmesinde şifreleme **SSE-S3** görünmeli.

**Olumsuz deneme (en az yetkinin kanıtı), sunucuda:** dördü de `AccessDenied` ile **reddedilmeli**.

```bash
sudo bash -c 'set -a; . /etc/davetkart/backup.env; set +a
  aws s3 ls "s3://$BACKUP_S3_BUCKET/daily/"                                   # listeleme
  aws s3 cp "s3://$BACKUP_S3_BUCKET/daily/<YYYY/MM/DD>/<ad>.dump" /tmp/x      # okuma
  aws s3 rm "s3://$BACKUP_S3_BUCKET/daily/<YYYY/MM/DD>/<ad>.dump"             # silme
  aws s3 cp /etc/hostname "s3://$BACKUP_S3_BUCKET/baska-onek/deneme"          # önek dışına yazma'
```

Biri başarılı olursa politika fazla geniş: §3'teki JSON'la karşılaştır.

**Ertesi sabah:**

```bash
journalctl -t davetkart-backup --since today        # 02:00 koşusu; son satır TAMAM
```

**Yayın öncesi kontrol** ([`YAYIN-SIRASI.md`](YAYIN-SIRASI.md) §2, 6. madde): konsolda **dünün** klasöründe iki dosya var mı?

## 6. Geri yükleme provası 🖥️

**Denenmemiş yedek bir umuttur.** Prova, yedeğin testidir (K157).

| Ne zaman | |
|---|---|
| **İlk prova** | Kayıt açılmadan **önce**, ilk üretim dökümüyle. Yayın kapısı koşulu |
| Sonra | Ayda bir (takvime yinelenen hatırlatıcı: her ayın ilk haftası) |
| Ayrıca | Yedek betiği değiştiğinde · PostgreSQL ana sürümü yükseldiğinde · büyük bir göçten sonra |

Adımlar:

1. Konsoldan **dünün** iki dosyasını indir (S3 → klasör → iki dosyayı seç → **Download (İndir)**), aynı
   klasöre koy (ör. `C:\Yedek\`).
2. Provayı çalıştır:

   ```powershell
   cd D:\Projects\davetkart\davetkart-backend-php-laravel
   $env:PGPASSWORD = Read-Host 'Yerel postgres parolasi'
   powershell -ExecutionPolicy Bypass -File deploy\backup\restore-drill.ps1 -Dump C:\Yedek\davetkart-<damga>.dump
   $LASTEXITCODE        # 0 = bütün tablolar manifestle aynı
   ```

3. Çıktıdaki `Geri yukleme : … sn` değerini aşağıdaki kayda yaz.
4. Birkaç satıra gözle bak (`davetkart_restore_drill` içinde son siparişler, son LCV'ler).
5. Prova veritabanını ve indirdiğin iki dosyayı **sil**: ikisi de gerçek müşteri verisi.

Aylık provada ayrıca bak:

- [ ] Son 30 günün her günü için bir klasör var mı (eksik gece yok)?
- [ ] Kurulu kopya depodakiyle aynı mı: `cmp /var/www/davetkart/backend/deploy/backup/pg-dump.sh /usr/local/sbin/davetkart-pg-dump`
- [ ] Ömür kuralı hâlâ **Enabled** mı; 37 günden eski nesne kalmış mı?
- [ ] `aws --version` (resmî kurucuysa güncelle: kurucuyu `sudo ./aws/install --update` ile yeniden çalıştır)

### Prova kaydı

| Tarih | Döküm | Boyut | Geri yükleme süresi | Sonuç | Not |
|---|---|---|---|---|---|
| 16 Kas 2026 | **Yerel geliştirme verisi** (üretim değil) | 66 KB | 0,3 sn | ✅ 21 tablo aynı | Betik denemesi. RTO sayılmaz |
| — | İlk üretim dökümü | | | ⬜ | Kayıt açılmadan önce (K157) |

## 7. Gerçek kurtarma

Hangi felakette hangi katman:

| Olay | Katman | Yol |
|---|---|---|
| Birkaç satır ya da tek tablo bozuldu (hatalı göç, elle `DELETE`) | Döküm | §7.1 |
| Veritabanı bütünüyle bozuldu, sunucu sağlam | Döküm | §7.2 |
| Sunucu gitti (disk, yanlış silme) | Önce disk görüntüsü; aradaki fark gerekiyorsa üstüne döküm | Lightsail → Snapshots → yeni örnek, sonra §7.2 |

### 7.1 Tek tablo (senaryo A)

```powershell
powershell -ExecutionPolicy Bypass -File deploy\backup\restore-drill.ps1 -Dump C:\Yedek\davetkart-<damga>.dump -OnlyTable orders
```

Tablo canlıya değil, **yan veritabanına** (`davetkart_restore_side`) açılır. Satırları karşılaştırıp neyi
geri yazacağına sen karar verirsin; yollar ve ilkeler backend `docs/rehber/deploy/backup/restore-drill.md` §5'te.
🔴 Canlıya dokunmadan **önce** bozuk hâlin de dökümünü al (§4.5).

### 7.2 Bütün veritabanı (taslak — ⚠️ hiç denenmedi)

Sunucudaki kimlik yedekleri okuyamaz; döküm senin makinenden gelir.

```powershell
scp -i $env:USERPROFILE\.ssh\davetkart_lightsail C:\Yedek\davetkart-<damga>.dump ubuntu@<SUNUCU-IP>:/tmp/
```

```bash
# sunucuda
sudo -n -u www-data /usr/bin/php /var/www/davetkart/backend/artisan down       # yazmaları durdur
sudo install -m 600 -o postgres -g postgres /tmp/davetkart-<damga>.dump /var/lib/postgresql/geri.dump
sudo -u postgres createdb -O davetkart davetkart_geri
sudo -u postgres pg_restore --no-owner --no-acl --role=davetkart -d davetkart_geri /var/lib/postgresql/geri.dump
# sayıları manifestle karşılaştır, sonra veritabanlarının adını değiştir:
sudo -u postgres psql -c 'ALTER DATABASE davetkart RENAME TO davetkart_bozuk'
sudo -u postgres psql -c 'ALTER DATABASE davetkart_geri RENAME TO davetkart'
sudo -n -u www-data /usr/bin/php /var/www/davetkart/backend/artisan migrate --force   # döküm eski şemadaysa
# K233: dökümün alındığı andan beri yapılan silmeleri yeniden uygula (önce say, sonra uygula; sonunda data:purge koşar)
sudo -n -u www-data /usr/bin/php /var/www/davetkart/backend/artisan data:reapply-deletions --since=<dökümün-anı> --dry-run
sudo -n -u www-data /usr/bin/php /var/www/davetkart/backend/artisan data:reapply-deletions --since=<dökümün-anı>
sudo -n -u www-data /usr/bin/php /var/www/davetkart/backend/artisan up
sudo rm /var/lib/postgresql/geri.dump /tmp/davetkart-<damga>.dump
```

Bilmen gerekenler:

- `ALTER DATABASE … RENAME` açık bağlantı varken çalışmaz: önce PHP-FPM ve kuyruk işçisi durdurulur
  (`artisan down` bağlantıları kapatmaz).
- Manifestteki `lastMigration` dökümün hangi şemada olduğunu söyler; kod daha yeniyse `migrate` ileri taşır.
- Dökümden **sonra** gelen ödemeler geri gelmez: Shopier panelinden ve günlüklerden elle tamamlanır.
- `davetkart_bozuk` hemen silinmez; neyin bozulduğunu anlamak için durur.
- Bu adımlar ilk kez gerçek bir olayda denenmesin: bir provada, boş bir Lightsail örneğinde denenmeli.

## 8. Sürüm uyumu

Kural: **geri yükleyen taraf** (`pg_restore` ve hedef sunucu), dökümü alan `pg_dump`'ın **ana sürümünden**
eski olamaz. Tersi sorun değildir.

| | Sürüm | Kaynak |
|---|---|---|
| Sunucu (dökümü alan) | PostgreSQL 18.6 | Plan kaydı Y6.4 (25 Ekim); `unattended-upgrades` küçük sürümü ilerletebilir |
| Senin makinen (geri yükleyen) | PostgreSQL 18.4 | 16 Kasım'da ölçüldü: `pg_restore (PostgreSQL) 18.4` |

İkisi de 18: ana sürüm aynı. Küçük sürüm farkının `-Fc` dökümünde sorun çıkarmasını beklemiyorum, ama bunu
**gerçek dosyayla ilk üretim provası gösterecek**; prova betiği yerel küçük sürüm eskiyse uyarı yazar. Temiz
olan, yereli sunucunun sürümüne ya da üstüne güncellemek.

Sunucu bir gün PostgreSQL 19'a yükselirse **önce** kendi makinene 19 araçlarını kur; yoksa prova
`unsupported version … in file header` ile durur (betik bunu daha baştan söyler).

## 9. Saklama süresi ve kişisel veri

Dökümde kullanıcılar, davetiyeler ve misafir yanıtları var. "Silme" bir an değil bir süreçtir:

| Kopya | Silinen veri en geç ne zaman yok olur |
|---|---|
| Canlı veritabanı | Hemen (hesap silme, K97) ya da `data:purge` süresi (K98) |
| Lightsail disk görüntüsü | 7 gün |
| S3 dökümü | **~37 gün** (30 gün geçerli + 7 gün eski sürüm, §2) |

- Gizlilik metni bu süreyi söylemeli (`SEC-11`, Faz 18'in dışında). "30 gün" yazılacaksa kural 23 + 7
  yapılmalı; karar senin.
- **Yedekten dönüldüğünde silinmiş veri geri gelir.** Geri yüklemeden sonra, `artisan up`'tan önce
  `data:reapply-deletions --since=<dökümün anı>` (K233, §7.2): silme günlüğü veritabanının dışında
  (`DAVETKART_DELETION_LOG_DISK=s3`) durur, yedekten sonraki hesap/davetiye/LCV/medya silmelerini aynı
  Action'larla yeniden uygular ve sonunda `data:purge`'ü çalıştırır. `--since` dökümün manifestindeki an.
  Ayrıca uygulama günlüğünde `Deletion log write failed` satırı varsa o kimlikler elle silinir.
  Ayrıntı: backend `docs/rehber/app/Console/Commands/ReapplyDeletions.md`.
- Provada indirdiğin dosyalar ve prova veritabanı da birer kopyadır: iş bitince sil.

## 10. Bu düzen neyi korumaz

- **AWS hesabının ya da bölgesinin kaybı.** Yedek bucket'ı disk görüntüleriyle **aynı hesapta ve aynı
  bölgede**. Denetimin B senaryosu (hesap ya da bölge erişilemez) bu yüzden yalnızca kısmen kapanıyor:
  S3 bölge içinde dayanıklıdır, hesap ele geçirilirse ya da kapanırsa yedekler de gider. Çözümü (başka
  hesaba ya da bölgeye çoğaltma, ya da şifreli bir dış kopya) ayrı bir karar.
- **`ismail-admin`'in ele geçirilmesi.** Bu kimlik yedekleri silebilir. MFA şart; Object Lock ileride.
- **Üstüne yazma.** `PutObject` var olan bir anahtarın üstüne yazabilir. Eski içerik 7 gün "eski sürüm"
  olarak durur; yani fark etmek için 7 günün var.
- **Son 24 saat.** RPO bilinçli olarak 24 saat. Daha küçüğü WAL arşivi / PITR ister (K157, ileride).
- **Medya.** Fotoğraf ve videolar veritabanında değil; medya bucket'ında sürümlemeyle korunur (Y3.3).
- **Sessiz durma, izleme kurulana kadar.** Cron ya da sunucu durursa betik haber veremez. Kalp atışı
  adresleri (`BACKUP_HEARTBEAT_URL`, `BACKUP_HEARTBEAT_FAIL_URL`) `OPS-03` ile doldurulacak; o güne kadar
  tek denetim senin baktığın günlük ve konsol.

## 11. Sorun giderme

Betiklerin hata mesajları ve sebepleri: backend `docs/rehber/deploy/backup/pg-dump.md` §8,
`restore-drill.md` §7, `docs/rehber/deploy/cron/davetkart-backup.md` §5.
