# `PHP-LARAVEL-SETUP.md` — Faz 18 Yaması

> **Tarih:** 16 Kasım 2026'da açıldı; Faz 18'in altı bulgusu kapandıkça bölüm eklenir.
> **Ne bu:** Ana devir dosyasına (`context/PHP-LARAVEL-SETUP.md`) **işlenmeyi bekleyen** Faz 18 kayıtları.
> `-EK-FAZ-11` ve `-EK-FAZ-12` ile aynı biçim.
> **Tam kayıt:** `davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-18.md`
> **Kaynak:** `AUD-2026-11-12` ([`REPORT.md`](../../audits/2026-11-12-full-system-audit/REPORT.md) §4)
> ⚠️ **Numaralar K146'dan başlar.** [`DECISION-INDEX.md`](../DECISION-INDEX.md) "sıradaki boş numara K128"
> diyordu; K128–K145 backend `docs/rehber/fazlar/FAZ-13.md` ve `FAZ-14.md`'de kullanılmış (`ARC-01`).
> Denetimin `ARC-04` önerisi K55'in yerine geçecek karar için "K146" diyordu; o karar yazılmadı,
> yazıldığında o günün boş numarasını alır.

---

## A. Karar Kaydı'na eklenecek (§7)

### 18.1 — `OPS-01` (yayına çıkacak commit ve dağıtım sırası)

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K146** | **Plan kuralları sözleşmesi:** tek kaynak backend `config/davetkart.php`. `php artisan plans:export` → `contracts/plan-rules.json` (`tierOrder`, `rsvpLimits`, `moduleTiers`, `presetTiers`, `whiteLabelTier`). Fiyat ve zaman damgası yok; anahtarlar sıralı, çıktı deterministik. `--check` dosya bayatsa çıkış 1; `composer check` zincirinde `errors:export --check`'ten hemen sonra | "Hangi şablon hangi planda" iki depoda elle duruyordu ve farkı söyleyen araç yoktu (`OPS-01`, `FE-05`). Hata kataloğunun deseni (K31) fiyatın anlamını veren kurallara uzatıldı. Fiyat API'den gelir (K128); sözleşmeye yazılsaydı üçüncü kopya olurdu | ✅ Faz 18.1 |
| **K147** | **Frontend denetimi:** `npm run verify:plans` (`verify` zincirinde). Sözleşmenin kopyası `src/contracts/plan-rules.json`; betik (a) `minimumTier` ↔ `presetTiers` (iki yönde), (b) fiyat kartı ↔ `moduleTiers` + `rsvpLimits` + `whiteLabelTier`, (c) `getRequiredTier` ve `TIER_RANK` ↔ sözleşmeden hesaplanan planı karşılaştırır. Taşıma biçimi hata kataloğuyla aynı: **kopya**, kardeş depodan okuma yok | Mevcut desene uyuldu: betik başka depoya bakmaz, CI'da ve tek depoyla da aynı sonucu verir. Bedeli: kopyanın güncelliği ayrı denetlenir ([`YAYIN-SIRASI.md`](../../operations/deployment/YAYIN-SIRASI.md) §2 ve §4.3). Arayüz kuralları sözleşmeden *türetmez*; o iş `FE-05`'in kalanı | ✅ Faz 18.1 |
| **K148** | **Dağıtım sırası:** önce backend (`main` → `deploy.sh`), sunucuda `plans:export --check` yeşilken frontend (`main` → `deploy-frontend.sh`). Tersine sıra yasak. Geri almada sıra tersine döner | Kuralı uygulayan sunucu önce, kuralı gösteren arayüz sonra. Arayüz önce çıkarsa "Gold+" dediği şablonu sunucu korumaz (şablon başına 150 ₺). Dağıtım sırası bir doğruluk koşuludur | ✅ Faz 18.1 (çalıştırma kitabı; sunucuda denenmedi) |
| **K149** | **Sürüm etiketle izlenir, dalla değil.** İki depo aynı etiketi taşır (`vMAJOR.MINOR.PATCH`; Faz 18 sonu `v1.1.0`). `deploy.sh` ve `deploy-frontend.sh` yayınlanan commit'in yanına `git describe --tags --exact-match` çıktısını ya da `etiketsiz` yazar; frontend betiği backend'in etiketini de yazar. Etiketsiz ya da farklı etiket **uyarı** verir, dağıtımı durdurmaz | "Hangi iki commit birlikte doğrulandı" sorusunun cevabı dal olamaz. İlk sürümde katı kural fazla: acil düzeltme etiket beklemeden çıkabilmeli. Karar sonra sıkılaştırılabilir | ✅ Faz 18.1 (betik yerelde sahte `git` ile denendi) |
| **K150** | **Kalite kapısı kırmızı olan dal yayın adayı değildir.** `TST-01` (Pint, `TemplateCatalogueTest.php`) `OPS-01`'in önkoşulu olarak aynı dalda kapandı | Kapı ilk adımda kırılınca sonraki adımlar (`plans:export --check` dahil) hiç koşmaz; "doğrulanmış commit" hiçbir dalda yoktu | ✅ Faz 18.1 |

Geçersiz kılınan karar: yok. K148, Y8.2a'yı ("sunucu her zaman `main`'i çeker") ve `deploy.sh`'ın
"önce backend" sırasını değiştirmez; ikisini kurala bağlar ve ara kontrol ekler.

### 18.2 — `OPS-02` (veritabanı yedeği ve geri yükleme provası)

Çalıştırma kitabı: [`operations/deployment/YEDEK-VE-GERI-YUKLEME.md`](../../operations/deployment/YEDEK-VE-GERI-YUKLEME.md).

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K151** | **Biçim ve zaman:** her gece 02:00 UTC'de `pg_dump -Fc`. Ayrı cron dosyası (`deploy/cron/davetkart-backup`), kullanıcı `root`, Laravel zamanlayıcısından bağımsız. Çakışan koşu `flock` ile, kilit betiğin içinde | `-Fc` sıkıştırılmıştır ve `pg_restore -t` ile tek tablo geri gelir. 02:00 UTC: disk görüntüsü 01:00 (Y4.4), `media:prune-orphans` 03:15. Yedek, korumaya çalıştığı uygulamaya bağımlı olmamalı: Laravel bozukken de çalışır ve anahtarı `www-data`'nın okuduğu `.env`'de durmaz. Kilit betikte olunca elle koşu ile cron koşusu da birbirini görür | ✅ Faz 18.2 (cron sunucuda denenmedi) |
| **K152** | **Hedef:** medya bucket'ından **ayrı** bir S3 bucket'ı (adını İsmail seçer). Block Public Access 4/4 açık, sürümleme açık, SSE-S3. Ömür kuralı: geçerli sürüm 30 gün sonra sona erer, eski sürüm 7 gün sonra kalıcı silinir, yarım çok parçalı yükleme 7 gün. Anahtar düzeni `daily/YYYY/MM/DD/<veritabanı>-<damga>.dump` + `.manifest.json` | Kusur yalıtımı (Y3.1'de alınan iki bucket kararının uygulaması): medya politikasındaki bir hata yedekleri açmaz. Sürümleme, üstüne yazılan ya da silinen yedeğin 7 gün geri alınabilmesi için. ⚠️ Etkili saklama en çok ~37 gündür (30 + 7); gizlilik metnine girecek sayı budur (`SEC-11`) | ✅ Faz 18.2 (bucket henüz açılmadı) |
| **K153** | **En az yetki:** sunucudaki kimlik `davetkart-backup` yalnızca `s3:PutObject` (`<bucket>/daily/*`); okuyamaz, listeleyemez, silemez. Geri yükleme `ismail-admin` ile. Lightsail örnek rolü taşıyamadığı için (Y3.4) erişim anahtarı `/etc/davetkart/backup.env`'de (root:600); betik izin yanlışsa çalışmaz, anahtarı ve kalp atışı adresini günlüğe yazmaz. Betik depodan değil root'a ait **kurulu kopyadan** çalışır (`/usr/local/sbin/davetkart-pg-dump`) | Sunucu ele geçirilse bile eski yedekler indirilemez ve silinemez; uygulamanın anahtarı (`davetkart-app`) bu bucket'a hiç erişemez. Kurulu kopya: root, `deploy` kullanıcısının yazabildiği bir dosyayı çalıştırırsa `deploy` fiilen root olur. Sınırı: `PutObject` üstüne yazabilir (eski sürüm 7 gün durur); Object Lock ileride | ✅ Faz 18.2 (kimlik henüz açılmadı) |
| **K154** | **Veritabanı kimliği:** `postgres` sistem kullanıcısı + peer kimlik doğrulama (`runuser -u postgres`). `.pgpass` kullanılmaz; parola betikte, komut satırında ve yedek ayar dosyasında yok. Bağlantılar `--no-password` ile | Y6.4d: `postgres` parolasız ve yalnızca yerel soketten girebiliyor. `.pgpass` veritabanı parolasının diskte ikinci kopyası olurdu ve parola değişince yedek sessizce bozulurdu. Süper kullanıcı her nesneyi döker; TCP ile girişi yok | ✅ Faz 18.2 (peer sunucuda denenmedi; yerelde libpq ortamıyla koştu) |
| **K155** | **Doğrulama zinciri ve manifest:** döküm yüklenmeden önce `pg_restore --list` ile okunur, boyutu > 0 olmalı, dört zorunlu tablonun (`users`, `invitations`, `orders`, `rsvps`) verisi içindekiler listesinde olmalı. `manifest.json` `public` şemasındaki **bütün** tabloların satır sayısını, dökümün SHA-256'sını, sürümleri ve son göçü taşır. Sayılar dökümle **aynı anlık görüntüden** alınır (`pg_export_snapshot()` + `pg_dump --snapshot`). Önce döküm, sonra manifest yüklenir. `--local <dizin>` / `DRY_RUN=1` kipi S3 yerine yerel dizine yazar. Herhangi bir hatada sıfır dışı çıkış | "Yedek alınıyor sanılır, ilk ihtiyaçta açılmadığı görülür" (`OPS-02` senaryo C). Anlık görüntü sayesinde prova tam eşitlik arar; yanlış alarm veren denetim okunmaz. Bütün tabloları saymak listeyi elle güncelleme ihtiyacını kaldırır. Yeni bağımlılık yok (`jq` yerine `printf`, değerler desenle denetlenir) | ✅ Faz 18.2 (yerelde mutantlarla denendi) |
| **K156** | **İzleme (asgari):** ayar dosyasında tanımlıysa betik başarıda `BACKUP_HEARTBEAT_URL`'yi, hatada `BACKUP_HEARTBEAT_FAIL_URL`'yi `curl` ile çağırır; tanımlı değilse yalnızca günlük (`journalctl -t davetkart-backup`). Kalp atışı gönderilemezse yedek başarısız sayılmaz | Asıl değer gelmeyen kalp atışıdır (ölü adam anahtarı): cron ya da sunucu durduğunda betik haber veremez. İki ayrı adres: tek adrese `?status=error` eklemek Sentry'de çalışır, başka araçlarda hatayı başarı diye bildirirdi. Alarmın tamamı `OPS-03` | ✅ Faz 18.2 (adresler boş; `OPS-03`'te dolacak) |
| **K157** | **Kabul ölçütü:** kayıt açılmadan önce ilk üretim dökümüyle bir geri yükleme provası (`deploy/backup/restore-drill.ps1`) yapılır ve ölçülen süre çalıştırma kitabının prova kaydına yazılır; sonra ayda bir. **RPO = 24 saat** bilinçli kabul; riskli göçten önce elle koşu. Daha küçük RPO (WAL arşivi / PITR) ileride ayrı karar | Denenmemiş yedek bir umuttur: prova yedeğin testidir. RTO ölçülmeden bilinemez. Bugünkü ölçekte 24 saatlik kayıp, sürekli arşivin karmaşıklığından ucuz | ⚠️ Betik hazır ve yerelde denendi; **üretim provası yapılmadı** |

Geçersiz kılınan karar: yok. K152, `YAYIN-PLANI.md` Y3.3'teki "`backups/` öneki 30 gün" satırının yerine
geçer (o satır tek bucket varsayımıyla yazılmıştı; Y3.1 kaydında iki bucket'a dönülmüştü). K151, K84'ü
("bakım komutları `--dry-run` taşır ve zamanlayıcıdan önce elle koşulur") yedek betiğine de uygular:
`--local` kipi ve cron'dan önce elle koşu.

Açık kalanlar (karar İsmail'in): sunucuya AWS CLI'nin nasıl kurulacağı (çalıştırma kitabı §4.1) ·
saklama süresi 30 + 7 mi kalacak, gizlilik metni için 23 + 7 mi olacak (`SEC-11`) · yedeklerin başka bir
hesaba ya da bölgeye çoğaltılması (denetimin B senaryosu yalnızca kısmen kapandı; kitap §10).
