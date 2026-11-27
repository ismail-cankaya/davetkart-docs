# İzleme ve alarm — çalıştırma kitabı

> **Tarih:** 22 Kasım 2026 (Faz 19.7, `OPS-03`) · Plan adımları: [`YAYIN-PLANI.md`](YAYIN-PLANI.md) Y11.3 (Sentry), Y11.7 (dış izleme)
> Kod: backend `GET /api/health` (kılavuz `docs/rehber/app/Support/Health/ReadinessProbe.md`) · bitiş tarihleri: [`SURE-TAKVIMI.md`](SURE-TAKVIMI.md)
> ⚠️ Bu dosyadaki hiçbir adım henüz çalıştırılmadı (hesap açma, DSN, sunucu: İsmail'in elle işi).

## 1. Ne izleniyor

| Duyarga | Nerede | Ne zaman alarm | Kim fark eder |
|---|---|---|---|
| `GET /api/health` | backend | 503: `database` · `schema` (bekleyen göç, Faz 20.1 K263) · `queue` (en eski iş >10 dk) · `scheduler` (kalp atışı >5 dk) · `disk` (≥%90) | Dış izleyici (§3) |
| `GET /api/ping` | backend | Dağıtım betiği (`deploy/deploy.sh`); canlılık, alarm değil | Dağıtım |
| Başarısız kuyruk işi | `ReportFailedJob` → `Log::critical` | Her iş vazgeçildiğinde | Sentry (§2) |
| Zamanlanmış işler (4) | `sentryMonitor` (K103) | İş koşmazsa / hata verirse | Sentry Crons (§2) |
| Gece yedeği | `pg-dump.sh` kalp atışları (K156) | Başarı gelmezse / başarısızlık gelirse | Dış izleyici (§4) |
| SSL bitişi | Let's Encrypt (otomatik yenileme) | Bitime 14 gün kala | Dış izleyici (§3) — Let's Encrypt artık e-posta atmıyor |

Yanıt gövdesi yalnızca başarısız kontrolün **adını** taşır; ayrıntı sunucuda: `php artisan tinker` →
`app(App\Support\Health\ReadinessProbe::class)->failures()`, kuyruk için `php artisan queue:monitor database:default`,
`schema` için `php artisan migrate:status --pending` (deploy'da `migrate --force` yarıda kalmış olabilir; `OPS-06`, `AUD-2026-11-26`'da 🟠).

## 2. Sentry (Y11.3)

1. Sentry'de proje (Laravel) → DSN'i kopyala. DSN bir sırdır: bu depoya ve sohbete yazılmaz.
2. Sunucuda `.env`: `SENTRY_LARAVEL_DSN=<DSN>` · `LOG_STACK=daily,sentry` · `SENTRY_SEND_DEFAULT_PII=false` (zaten şablonda).
3. `php artisan config:cache` → `php artisan sentry:test` → Sentry'de test olayı görünür.
4. Crons: dört iş (`orders-expire`, `media-prune-orphans`, `sanctum-prune-expired`, `data-purge`) ilk koşularında
   Sentry → Crons'ta kendiliğinden belirir. Alarm kuralı: "missed" ve "failed" → e-posta.
5. Uyarı kuralı: `level:fatal OR level:critical` → e-posta (başarısız iş satırı `critical`).

## 3. Dış izleyici (Y11.7)

§A-1 cevaplanmadı; araç seçilmedi. Karşılaştırma (ücretsiz katman koşulları değişebilir; kayıttan önce sitesinde doğrula):

| | UptimeRobot | Better Stack (Uptime) | Sentry Uptime |
|---|---|---|---|
| Plan kaydında | ✅ Y11.7 bunu anıyor | — | Sentry zaten kurulacak |
| HTTP 200 dışını alarm | ✅ | ✅ | ✅ |
| SSL bitiş uyarısı | ✅ | ✅ | ⚠️ doğrula |
| Kalp atışı (cron/heartbeat) adresi — yedek için | ✅ | ✅ | ⚠️ Crons ile ayrı |
| Bildirim | e-posta, uygulama | e-posta, uygulama, telefon | e-posta |

Hangisi seçilirse:

- Monitör 1: `GET https://davetkart.com/api/health`, **1 dakikada bir**, beklenen 200, **2 ardışık hata** sonrası
  alarm (dağıtımda `cache:clear` kalp atışını siler; ilk `schedule:run`'a kadar ≤1 dk `scheduler` düşer).
  Faz 20.4'ten beri (K264) deploy bakım kipinde: 30–60 sn boyunca her istek 503. Deploy bir dakikayı aşarsa
  alarm gelir; beklenen bir alarmdır. Deploy'dan önce izleyicide bakım penceresi aç ya da eşiği 3 ardışık hataya çek.
  Deploy bitip 503 sürüyorsa: `Site BAKIM KIPINDE kaliyor` (yarıda kalan deploy, `YAYIN-SIRASI.md` §4.1).
- Monitör 2: SSL bitişi `davetkart.com` (14 gün) — `SURE-TAKVIMI.md` satırını ✅ yap.
- Alarm kime: İsmail'in e-postası (+ telefon uygulaması). Kanal tek kişi; yayın sonrası ikinci kişi eklenecekse buraya yaz.

## 4. Yedek kalp atışları (K156)

Dış izleyicide iki **heartbeat/cron** monitörü aç: "yedek başarılı" (beklenen aralık 24 saat + 1 saat tolerans)
ve "yedek başarısız" (her vuruş alarm). Adresleri sunucuda `/etc/davetkart/backup.env` içine:
`BACKUP_HEARTBEAT_URL=` ve `BACKUP_HEARTBEAT_FAIL_URL=` (bkz. backend `deploy/backup/backup.env.example`).
Adresler sırdır; günlüğe yazılmaz (K156). Doğrulama: [`YEDEK-VE-GERI-YUKLEME.md`](YEDEK-VE-GERI-YUKLEME.md) prova adımı.

## 5. Elle doğrulama (kurulumdan sonra bir kez)

| # | Adım | Beklenen |
|---|---|---|
| 1 | `curl -i https://davetkart.com/api/health` | 200 `{"status":"ok"}` |
| 2 | Sunucuda cron'u 6 dk durdur (`sudo systemctl stop cron`), tekrar 1 | 503 `["scheduler"]` + dış izleyici alarmı; sonra `start` |
| 3 | `sudo systemctl stop davetkart-queue` + bir parola sıfırlama iste, 11 dk bekle | 503 `["queue"]`; sonra `start` |
| 4 | Sentry'de `sentry:test` olayı ve alarm e-postası | görüldü |
| 5 | Yedek betiğini elle koş | "başarılı" kalp atışı monitörde |

## 6. Kapasite metrikleri (Faz 21.14, `OPS-09`)

Eşikler ve eylemler: [`YAYIN-PLANI.md`](YAYIN-PLANI.md) §6.1. Bu tablo hangi değerin **nereden** okunacağını söyler. Hepsi
sunucuda, elle (alarm değil; dış izleyici yalnızca §1'deki sağlık ucunu izler). Haftada bir bakılır.

| Metrik | Komut / yer | Not |
|---|---|---|
| FPM havuzu: `max children reached`, `listen queue`, `active processes` | `cgi-fcgi` ile `/fpm-status` (backend `docs/rehber/deploy/php-fpm/davetkart.md` §4) | 21.5 kurulumundan sonra (K269); sayaç FPM yeniden başlayınca sıfırlanır |
| FPM yavaş istekler | `/var/log/php8.5-fpm-davetkart.slow.log` (satır sayısı/gün: `grep -c '^\[' …`) | > 5 sn istekler, yığınıyla |
| Kullanılabilir bellek | `free -m` ("available"); OOM: `journalctl -k --since -7d \| grep -i -E 'oom\|killed process'` | |
| p95 yanıt süresi | Nginx erişim günlüğü `$request_time` (21.4 önerisi `log_format davetkart`): `awk '$0 ~ /"(GET\|POST\|PUT\|DELETE) \/api\// {print $(NF-1)}' davetkart.access.log \| sort -n \| awk '{a[NR]=$1} END {print a[int(NR*0.95)]}'` | yükleme ve asistan uçlarını ayrı değerlendir |
| PostgreSQL bağlantıları | `sudo -u postgres psql -c "select count(*), (select setting from pg_settings where name='max_connections') from pg_stat_activity;"` | |
| PostgreSQL önbellek isabeti | `sudo -u postgres psql -d davetkart -c "select round(sum(blks_hit)*100.0/nullif(sum(blks_hit+blks_read),0),2) from pg_stat_database;"` | |
| Disk | `df -h /`; sağlık ucu `disk` %90'da 503 | |
| Kuyruk gecikmesi | `php artisan queue:monitor database:default`; sağlık ucu `queue` (>10 dk) | |
| CPU patlama kapasitesi | Lightsail konsolu → örnek → Metrics → "Burst capacity" | 2 GB plan patlamalı CPU kullanır |

Hiçbiri koşulmadı (sunucuya istek yok); komutlar sunucu kurulumuna göre yazıldı.
