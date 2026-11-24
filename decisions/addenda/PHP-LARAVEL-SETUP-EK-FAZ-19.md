# `PHP-LARAVEL-SETUP.md` — Faz 19 Yaması

> **Tarih:** 20 Kasım 2026'da açıldı; 19.0 ve 19.2–19.27 hat kayıtlarından 24 Kasım'da (19.90) işlendi.
> Kullanılan: K182 (hazırlık) · K183–K192 (Hat A) · K220–K232 (Hat B) · K250–K258 (Hat C). 19.28 `ARC-03` bekliyor.
> **Ne bu:** Ana devir dosyasına (`context/PHP-LARAVEL-SETUP.md`) **işlenmeyi bekleyen** Faz 19 kayıtları.
> `-EK-FAZ-18` ile aynı biçim.
> **Tam kayıt:** `davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-19.md`
> **Kaynak:** `AUD-2026-11-12` ([`REPORT.md`](../../audits/2026-11-12-full-system-audit/REPORT.md) §5.1) ·
> takip tablosu [`phases/faz-19/README.md`](../../phases/faz-19/README.md)
> Numaralar K179'dan başlar ([`DECISION-INDEX.md`](../DECISION-INDEX.md), 20 Kasım).

---

## A. Karar Kaydı'na eklenecek (§7)

### 19.0 — Hazırlık: paralel hatlar için hat başına test veritabanı

Kayıt: [`phases/faz-19/kayit/19-00-HAZIRLIK.md`](../../phases/faz-19/kayit/19-00-HAZIRLIK.md) · dallar: backend `fix/2026-11-20-faz19-parallel-test-db` · docs `docs/2026-11-20-faz19-parallel-test-db`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K182** | Paralel hatlarda test veritabanı `davetkart_test_<DAVETKART_TEST_DB_SUFFIX>`; yalnızca `APP_ENV=testing`, son ek `[a-z0-9_]`, geçersizse fail-closed | Üç hattın `RefreshDatabase`'i aynı veritabanında birbirinin tablolarını siliyordu; `<server>` sabitlemesi korunarak hat başına ayrıldı. | geçerli · Faz 19.0 (20 Kas) |

### 19.1 — `SEC-07` (Composer bağımlılıklarında bilinen açıklar; `composer audit` kırmızı)

Kod kılavuzları (backend `docs/rehber/`): `composer.md` · `app/Services/Payment/ShopierGateway.md` §12 ·
`tests/Feature/PaymentDriverResolutionTest.md` · `config/trustedproxy.md` (durum notu). Frontend değişmedi.

**§A:** iki satır da **boş** bırakıldı; varsayılanlar uygulandı. §A-1'in varsayılan komutu dolaylı
bağımlılıklarda majör sürüm atlattığı için iş durdu (prompt §8) ve İsmail oturumda majörsüz yolu seçti.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K179** | **Güvenlik güncellemesinin kapsamı:** `composer update "symfony/*" laravel/framework --with-all-dependencies` + üç geçici `--with` kısıtı (`guzzlehttp/psr7:^2.13`, `guzzlehttp/uri-template:^1.0.10`, `brick/math:^0.18`). Yalnızca `composer.lock` değişir: 55 paket (`laravel/framework` 13.35.0 → 13.43.0; açık taşıyan altı Symfony paketi 8.1.10/8.1.11); `composer.json` aynı (`content-hash` değişmedi); majör yok. Guzzle 8 / PSR-7 3 / `brick/math` 1.0 geçişi **ayrı karar** | Güvenlik yaması davranış değişikliği taşımamalı. `-W` tek başına beş dolaylı paketi majör atlatıyordu (`guzzle` 7 → 8 Laravel HTTP istemcisinin, AWS SDK'nın ve Sentry'nin altında). `-W` şart: Laravel 13.40+ `laravel/prompts ^0.3.25` istiyor, adı geçen paketlerle sınırlı güncelleme çözülmüyor. Alt sınır bugünkü sürüm: `^1.0` çözücüyü `uri-template`'i 1.0.0'a düşürmeye götürdü | ✅ Faz 19.1 (lock; `audit --locked` çıkış 0) · §A-1 varsayılanı (İsmail cevaplamadı) → §8 (majör) → İsmail "majörsüz"ü seçti · ⚠️ yeni `vendor` ile `composer check` koşmadı (GitHub erişilemedi; eski `vendor` ile 1168 test ✅) · ⚠️ sonraki düz `composer update` majörleri getirir |
| **K180** | **Dışarıya verilen mutlak adresler istekten değil yapılandırmadan üretilir.** Shopier callback = `rtrim(config('app.url'), '/')` + `ShopierGateway::CALLBACK_PATH`; açık üretim, küresel `URL::forceRootUrl` yok. Diğerleri zaten böyleydi: postalar `davetkart.frontend.url`, ödeme dönüşü `payment.return_urls` (K122), e-posta değişikliği göreli imza (K144), medya disk `url`'i | `url()` / `route()` kökü isteğin `Host`'undan (güvenilen vekil varsa `X-Forwarded-Host`'tan) alır; ikisi de istemcinin elinde (host header injection). Bugün sömürü yolu yok: Nginx tanımadığı host'u `444` ile keser, `TRUSTED_PROXIES` boş, saldırgan yalnızca kendi formunu bozabilir. Yani derinlemesine savunma. Küresel ayar her `url()`'yi etkiler ve etkisi çağrının yanında görünmez | ✅ Faz 19.1 · §A-2 varsayılanı (İsmail cevaplamadı) · ⚠️ `APP_URL` artık ödeme dönüşü için kritik; sunucudaki değer gözle doğrulanmadı · `docs/10` şablonu eski `api.davetkart.com`'u gösteriyor (`OPS-04`) |
| **K181** | **Yayın adayı = `composer check` ✅ ve `composer audit` ✅.** `composer audit` `composer check` zincirine **girmez**: CI'da ayrı adım ("Composer güvenlik taraması"), yayın kontrol listesinde ayrı madde ([`YAYIN-SIRASI.md`](../../operations/deployment/YAYIN-SIRASI.md) §2, madde 2). **K150'yi tamamlar** | `check` deterministik ve çevrimdışı: aynı commit, aynı sonuç. `audit` ağ ister ve zamana bağlı: aynı lock 13 Kasım sabahı 8, akşamı 9 açık verdi. Birleşirse ağ sorunu "kod bozuk" gibi görünür (19.1'de GitHub 40 dakikadan uzun erişilemedi) ve kapı zamana bağlanır. Ayrı adım olunca CI özetinde hangisinin patladığı tek bakışta görünür | ✅ Faz 19.1 |

**Tamamlanan karar:** K150 → **K181** (K150 geçerli; "kalite kapısı" yayın için iki parçalı oldu). Durum
notu [`DECISION-INDEX.md`](../DECISION-INDEX.md)'de. Geçersiz kılınan karar: yok.

Açık kalanlar (karar İsmail'in): Guzzle 8 / PSR-7 3 / `brick/math` 1.0 geçişi (ayrı dal; HTTP istemcisi,
S3 ve Sentry yolları sınanarak) · sunucudaki `APP_URL`'in yayından önce gözle doğrulanması
(`https://davetkart.com` olmalı) · `docs/10` üretim şablonunun düzeltilmesi (`OPS-04`, Faz 19.6).

### 19.2 — `ARC-01`: Karar indeksi K128–K145'i bilmiyor

Kayıt: [`phases/faz-19/kayit/19-02-ARC-01.md`](../../phases/faz-19/kayit/19-02-ARC-01.md) · dallar: docs `docs/2026-11-20-arc-01-decision-index-hat-c`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K250** | Karar indeksi `build_decision_index.py --check` ile denetlenir: tanım = tablo satırının ilk hücresi yalnızca K numarası; docs + kardeş backend; eksik/tanımsız → 1, backend yok → 2 | K128–K145 denetim olmadığı için indekse hiç girmedi; makine karşılaştırması bu tür boşluğu kapıda yakalar. | geçerli · Faz 19.2 (20 Kas) |
| **K251** | `build_decision_index.py` argümansız koşunca yazmaz (kullanım, çıkış 2); 2026-11-12 üretimi yalnızca `--generate` ile | Eski üretim K1–K127'yi bilir; yanlışlıkla koşmak elle eklenen K128+ satırlarını silerdi. | geçerli · Faz 19.2 (20 Kas) |

### 19.3 — `ARC-02`: Faz 16 ve 17'nin faz kaydı yok

Kayıt: [`phases/faz-19/kayit/19-03-ARC-02.md`](../../phases/faz-19/kayit/19-03-ARC-02.md) · dallar: backend `fix/2026-11-20-arc-02-phase-16-17-records` · docs `docs/2026-11-20-arc-02-phase-16-17-records`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K252** | Gold = videolu **ya da** premium etkileşimli (canlı WebGL / sensörlü) şablon; Faz 16'nın 10 ve Faz 17'nin 9 kimliği `preset_tiers`'te (kaynak `contracts/plan-rules.json` `presetTiers`). ⚠️ onay yalnızca kod yorumunda, kayıt onaylatılmadı | 19 şablonun fiyat kararı yalnızca commit mesajındaydı; K102'nin genişlemesi numarayla kayda geçti. | geçerli · ⚠️ İsmail onaylamadı · Faz 19.3 (20 Kas) |

**Eski kararların durum notları:**

- K102 → genişletildi → K252 (premium = video **ya da** premium etkileşim; Faz 17, 2026-11-05).

### 19.4 — `ARC-05`: Eski `claude/…` yolları; backend'in `claude/` klasörü ikinci ev

Kayıt: [`phases/faz-19/kayit/19-04-ARC-05.md`](../../phases/faz-19/kayit/19-04-ARC-05.md) · dallar: backend `fix/2026-11-22-arc-05-claude-folder` · docs `docs/2026-11-22-arc-05-claude-folder`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K253** | `build_decision_index.py --check` Faz 19 hat aralığındaki (K182–K279) indekste olmayan tanımları "bekleyen" yazar, hata saymaz; 19.90 indekse işleyince aralık kaldırılır | Faz özetleri K'yı 19.90'dan önce tanımlıyor (K252); aksi hâlde her hat kapıyı kırmızı görürdü. | geçerli · Faz 19.4 (22 Kas) |
| **K254** | Kod dışı doküman tek evde (`davetkart-docs`); backend'de yalnızca `claude/README.md` yönlendirmesi; backend'den atıf `` `davetkart-docs: <yol>` `` düz metin | Backend `claude/` ikinci ev olmuş, 25 dosya kırık yol gösteriyordu; depolar arası göreli bağlantı GitHub'da çalışmaz. | geçerli · Faz 19.4 (22 Kas) |

**Eski kararların durum notları:**

- K250 → genişletildi → K253 (bekleyen aralık).

### 19.5 — `ARC-04`: K55 "yerel disk kalır" geçerli görünüyor ama yayın planı S3 kuruyor

Kayıt: [`phases/faz-19/kayit/19-05-ARC-04.md`](../../phases/faz-19/kayit/19-05-ARC-04.md) · dallar: backend `fix/2026-11-20-arc-04-media-disk` · docs `docs/2026-11-20-arc-04-media-disk`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K183** | Üretimde medya yalnızca `s3` diskine yazılır; başka disk yüklemeyi 503 `PROVIDER_UNAVAILABLE` ile durdurur, okuma çalışır; yerel disk yalnızca yerel/test | Unutulmuş ortam değişkeni misafir fotoğraflarını sessizce sunucu diskine yazmasın (K70 fail-closed ilkesi depolamaya). | geçerli · Faz 19.5 (2026-11-20) |

**Eski kararların durum notları:**

- `K55 → geçersiz kılındı → K183`

### 19.6 — `OPS-04`: Üretim `.env` şablonu sunucudaki gerçek dosyadan sapmış

Kayıt: [`phases/faz-19/kayit/19-06-OPS-04.md`](../../phases/faz-19/kayit/19-06-OPS-04.md) · dallar: backend `fix/2026-11-22-ops-04-env-template` · docs `docs/2026-11-22-ops-04-env-template`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K184** | Üretim `.env` şablonu config'in okuduğu anahtarlarla `env:template --check` ile eşit tutulur; dışlamalar komutta açık liste; Y8.3b düzeltmeleri şablonda | Sunucuda elle yapılan düzeltme şablona dönmezse yeniden kurulum aynı hataları üretir. | geçerli · Faz 19.6 (2026-11-22) |
| **K185** | Üretimde `MAIL_MAILER=log` uygulamayı durdurmaz; her gönderim denemesi CRITICAL log, `about` satırı uyarı gösterir | Posta kaybı görünür olmalı ama giriş/LCV/davetiyeyi durdurmamalı. | geçerli · Faz 19.6 (2026-11-22) |

### 19.7 — `OPS-03`: İzleme ve alarm yok; sağlık ucu yalnızca PHP'nin ayakta olduğunu söylüyor

Kayıt: [`phases/faz-19/kayit/19-07-OPS-03.md`](../../phases/faz-19/kayit/19-07-OPS-03.md) · dallar: backend `fix/2026-11-22-ops-03-health-monitoring` · docs `docs/2026-11-22-ops-03-health-monitoring`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K255** | `GET /api/health` hazır olma ucu: veritabanı, kuyruk (en eski iş >10 dk), zamanlayıcı kalp atışı (>5 dk), disk (≥%90); herhangi biri → 503; gövde yalnızca durum + başarısız kontrolün adı; eşikler `config/health.php`; `/api/ping` canlılık olarak kalır | `/ping` veritabanı ölüyken de 200 dönüyordu; dış izleme sessiz bozulmaları görmüyordu. | geçerli · Faz 19.7 (22 Kas) |
| **K256** | Başarısız kuyruk işi `Log::critical` ile bildirilir; bağlam yalnızca iş sınıfı, kuyruk, bağlantı, deneme sayısı, istisna sınıfı (yük ve istisna metni yok) | Sentry kanalı `critical` eşikli; yük ve hata metni kişisel veri taşır. | geçerli · Faz 19.7 (22 Kas) |

**Eski kararların durum notları:**

- K103 (zamanlanmış işler Sentry Crons'a bağlı) → kapsam genişledi: beşinci iş `health-heartbeat` (K255).
- K156 (yedek kalp atışları, alarm `OPS-03`) → bağlanacağı yer yazıldı: `IZLEME.md` §4 (adresler hâlâ boş).

### 19.8 — `OPS-05`: Tek hata noktaları: alan adı yenilemesi, posta ve kredi bitiş tarihleri

Kayıt: [`phases/faz-19/kayit/19-08-OPS-05.md`](../../phases/faz-19/kayit/19-08-OPS-05.md) · dallar: docs `docs/2026-11-22-ops-05-expiry-calendar`.

Yeni K yok.

### 19.9 — `SEC-05`: Zayıf parolalar kabul ediliyor

Kayıt: [`phases/faz-19/kayit/19-09-SEC-05.md`](../../phases/faz-19/kayit/19-09-SEC-05.md) · dallar: backend ve frontend `fix/2026-11-23-sec-05-password-policy` · docs `docs/2026-11-23-sec-05-password-policy`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K258** | Parola kuralı tek kaynaktan (`App\Rules\PasswordPolicy`): en az 8, en çok 255 karakter, yaygın 10.000 parola listesinde olmayan (büyük/küçük harf duyarsız) ve tek karakter tekrarı olmayan; kayıt, sıfırlama, değiştirmede aynı; karmaşıklık kuralı yok; mevcut hesaplar zorlanmaz; hata `VALIDATION_FAILED` + `uncommon_password` | `SEC-05`: en yaygın parolalar kabul ediliyordu; uzunluk 8 İsmail'in kararı. | geçerli · Faz 19.9 (23 Kas) |

**Eski kararların durum notları:**

- `RegisterRequest` D6 (kural adı sözleşmenin parçası) → uygulandı: yeni kural dize adlı (`uncommon_password`).

### 19.10 — `SEC-06`: Genel hız sınırı IP anahtarlı: misafir trafiği davetiye sahibini de kilitliyor

Kayıt: [`phases/faz-19/kayit/19-10-SEC-06.md`](../../phases/faz-19/kayit/19-10-SEC-06.md) · dallar: backend `fix/2026-11-22-sec-06-rate-limit-keys` · docs `docs/2026-11-22-sec-06-rate-limit-keys`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K186** | Genel `api` kovası kimlikliyse kullanıcı (120/dk), değilse IP (60/dk); misafir davetiye okuması ayrı `public-read` kovası (IP 300/dk); misafir medya IP 60/dk; sayılar `davetkart.api.rate_limit`'te | Hız sınırının anahtarı kaynağı tüketen kimlik olmalı; tek IP'deki salon sahibini kilitlememeli. | geçerli · Faz 19.10 (2026-11-22) |

**Eski kararların durum notları:**

- `K104` → geçerli; misafir medya IP sayısı K186 ile 15 → 60 güncellendi (davetiye kovası aynen).

### 19.11 — `TST-02`: Kilitlerin hiçbiri testle korunmuyor

Kayıt: [`phases/faz-19/kayit/19-11-TST-02.md`](../../phases/faz-19/kayit/19-11-TST-02.md) · dallar: backend `fix/2026-11-22-tst-02-lock-tests` · docs `docs/2026-11-22-tst-02-lock-tests`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K187** | Her `lockForUpdate()` bir SQL düzeyi testle (`LockAssertions::assertLocksRowOf`) korunur ve kılavuz envanterine yazılır; para/kota kilitleri ayrıca ikinci bağlantıyla (`55P03`) sınanır; yarış testleri `concurrency` grubunda, `DatabaseTruncation` ile | Tek süreçli paket kilidin silinmesini göremez; envanter yeni kilidin testsiz kalmasını görünür kılar. | geçerli · Faz 19.11 (2026-11-22) |
| **K188** | `ClaimReleasedOrderAction` kilitli adayları aldıktan sonra koşulları yeni sorguyla yeniden sınar (başka tabloya bakan koşul kilitten sonra yeniden sorulur) | READ COMMITTED değişmeyen satırı yeniden sınamaz; iade talebi açılmış donmuş hak bağlanıyordu (testle kanıtlı). | geçerli · Faz 19.11 (2026-11-22) |

**Eski kararların durum notları:**

- `K138` → geçerli; K188 ile eşzamanlı durumda da uygulanır hâle geldi.
- `K111` → geçerli; kilidi artık M14 testleri koruyor.

### 19.12 — `FE-51`: Misafir fotoğraf/video yüklemesine arayüzden ulaşılamıyor

Kayıt: [`phases/faz-19/kayit/19-12-FE-51.md`](../../phases/faz-19/kayit/19-12-FE-51.md) · dallar: backend ve frontend `fix/2026-11-23-fe-51-guest-media-upload` · docs `docs/2026-11-23-fe-51-guest-media-upload`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K189** | Misafir medya yüklemesi bayrakla kapalı (varsayılan), kapalıyken 404; bayrak public davetiye yanıtında `guestUploads` | Arayüzü olmayan kimliksiz yazma ucu saldırı yüzeyiydi; 404, LCV kapalıyken dönen 404 ile aynı (C6); arayüz bayrağı sabit kodlamaz | geçerli · Faz 19.12 (2026-11-23) |

**Eski kararların durum notları:**

- Faz 6 (6.14–6.16) misafir medya ucu → **bayrağa bağlandı** (K189); davranış bayrak açıkken aynı.

### 19.13 — `SEC-08`: Kimliksiz misafir davetiye başına 5 GB yükleyebilir; yetim dosya kotayı 24 saat tutar

Kayıt: [`phases/faz-19/kayit/19-13-SEC-08.md`](../../phases/faz-19/kayit/19-13-SEC-08.md) · dallar: backend `fix/2026-11-23-sec-08-guest-upload-budget` · docs `docs/2026-11-23-sec-08-guest-upload-budget`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K190** | Misafir yükleme bütçesi: iliştirilmiş 1 GB + tür başına adet; iliştirilmemişler ayrı kota (50 dosya / 200 MB); yetim 1 saat, temizlik saatlik | Kimliksiz yazma ucunda adet yetmez, bayt ve zaman da sınırlanmalı; yetim kotayı tutamamalı (OWASP API4) | geçerli · Faz 19.13 (2026-11-23) |

**Eski kararların durum notları:**

- Faz 6 misafir medya kotası ("COUNT(*) doğru metrik") → **genişletildi** (K190): adet kaldı, iliştirilmiş bayt ve bekleyen kota eklendi.
- Faz 9 (9.10) `orphan_grace_hours = 24`, günlük 03:15 → **geçersiz kılındı → K190** (1 saat, saatlik).

### 19.14 — `SEC-09`: E-posta doğrulaması yok

Kayıt: [`phases/faz-19/kayit/19-14-SEC-09.md`](../../phases/faz-19/kayit/19-14-SEC-09.md) · dallar: backend ve frontend `fix/2026-11-23-sec-09-email-verification` · docs `docs/2026-11-23-sec-09-email-verification`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K191** | Kayıt sonrası e-posta doğrulaması: imzalı 24 saatlik bağlantı (EmailChangeLink deseni, sır saklanmaz), checkout ve yayın `403 EMAIL_NOT_VERIFIED`, ilk yayın indirimi yalnızca doğrulanmışa, yeniden gönderme saatte 3 | Doğrulanmamış adres bir iddiadır; para, yayın ve indirim kanıta bağlanmalı. Projede kurulu imzalı bağlantı deseni veritabanına sır yazmadan tek kullanım sağlıyor | geçerli · Faz 19.14 (2026-11-23) |

**Eski kararların durum notları:**

- `K159` (ilk yayın uygunluğu) → **daraltıldı** (K191): yalnızca doğrulanmış hesap.
- `K144` (e-posta değişikliği) → değişmedi; onaylanan değişiklik hesabı doğrulanmış sayar.

### 19.15 — `SEC-10`: Shopier'e uydurma TCKN ve telefon gönderiliyor

Kayıt: [`phases/faz-19/kayit/19-15-SEC-10.md`](../../phases/faz-19/kayit/19-15-SEC-10.md) · dallar: docs `docs/2026-11-22-sec-10-shopier-buyer-fields`.

Yeni K yok.

**Eski kararların durum notları:**

- `K125` → ⚠️ elle doğrulama bekliyor → **soru hazır, gönderilmeyi bekliyor** (`notes/04-SHOPIER-ALICI-ALANLARI-SORUSU.md`, 2026-11-22).

### 19.16 — `SEC-13`: `data:purge` tarihi olmayan davetiyelerin misafir verisini hiç silmiyor

Kayıt: [`phases/faz-19/kayit/19-16-SEC-13.md`](../../phases/faz-19/kayit/19-16-SEC-13.md) · dallar: backend `fix/2026-11-23-sec-13-purge-undated` · docs `docs/2026-11-23-sec-13-purge-undated`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K257** | Etkinlik tarihi olmayan davetiyede misafir verisi (LCV + misafir dosyaları) `published_at` + 12 ay, yayınlanmamışsa `created_at` + 12 ay sonra silinir; tarihli davetiyede K98 (`event_at` + 6 ay) aynen; sahibe bildirim yok | `NULL` tarih sorguda sessizce atlanıyor, saklama sözü bir alt kümede tutulmuyordu (`SEC-13`). | geçerli · Faz 19.16 (23 Kas) |

**Eski kararların durum notları:**

- K98 (saklama süreleri) → kapsam genişledi: tarihsiz davetiye için yedek kural (K257).
- N4 (tarihsiz davetiyeye dokunulmaz, Faz 10) → geçersiz kılındı → K257.

### 19.17 — `SEC-12`: Her sayfa Google Fonts'u Google'dan yüklüyor

Kayıt: [`phases/faz-19/kayit/19-17-SEC-12.md`](../../phases/faz-19/kayit/19-17-SEC-12.md) · dallar: backend ve frontend `fix/2026-11-23-sec-12-self-hosted-fonts` · docs `docs/2026-11-23-sec-12-self-hosted-fonts`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K226** | Fontlar kendi alan adımızdan: `public/fonts/` (latin + latin-ext, lisanslarıyla), site geneli `src/styles/fonts.css`, şablonlar `/fonts/templates.css` (`loadTemplateFonts`), `verify:fonts`, CSP'den Google çıktı | Ziyaretçi IP'si üçüncü tarafa gitmesin; CSP dış alan adı istemesin. | geçerli · Faz 19.17 (2026-11-23) |

### 19.18 — `SEC-11`: Gizlilik metni "hemen silinir" diyor; yedekler tutuyor; üçüncü taraflar adıyla yok

Kayıt: [`phases/faz-19/kayit/19-18-SEC-11.md`](../../phases/faz-19/kayit/19-18-SEC-11.md) · dallar: frontend `fix/2026-11-24-sec-11-privacy-text` · docs `docs/2026-11-24-sec-11-privacy-text`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K231** | Gizlilik metni silmeyi iki adımda söyler: canlıdan hemen, yedeklerden en geç `BACKUP_PURGE_DAYS` (40) gün içinde; veri işleyenler ad · amaç · yer · veriyle listelenir; `verify-render` sabiti ve adları kilitler | Dürüst saklama beyanı en uzun yaşayan kopyanın süresini söyler (K152 ~37 gün). | geçerli · Faz 19.18 (2026-11-24) |

**Eski kararların durum notları:**

- K97 (hesap silme: derhal) → kapsam daraltıldı: "derhal" canlı sistem için; yedekler K231.
- K98 (saklama süreleri) → metin K257 ile hizalandı (tarihsiz davetiye 12 ay).

### 19.19 — `FE-52`: Fiyat sayfası SSS'si backend'de olmayan "yayın süresi" ve ücretli uzatmayı anlatıyor

Kayıt: [`phases/faz-19/kayit/19-19-FE-52.md`](../../phases/faz-19/kayit/19-19-FE-52.md) · dallar: frontend `fix/2026-11-24-fe-52-pricing-faq` · docs `docs/2026-11-24-fe-52-pricing-faq`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K232** | Davetiyenin yayın süresi yok: siz silene kadar yayında kalır; fiyat sayfası SSS'si süre ya da ücretli uzatma vaat etmez, misafir verisi süresini `GUEST_DATA_MONTHS_AFTER_EVENT` sabitinden söyler; `verify-render` kilitler | Fiyat sayfası bir sözleşme taslağıdır (R8): backend'de karşılığı olmayan vaat yazılmaz. | geçerli · Faz 19.19 (2026-11-24) |

### 19.20 — `FE-01`: Dil seçici on dil sunuyor, arayüzün büyük kısmı yalnızca Türkçe

Kayıt: [`phases/faz-19/kayit/19-20-FE-01.md`](../../phases/faz-19/kayit/19-20-FE-01.md) · dallar: frontend `fix/2026-11-20-fe-01-language-scope` · docs `docs/2026-11-20-fe-01-language-scope`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K220** | Dil seçici yalnızca tr/en; eski kayıt ve desteklenmeyen dil tr'ye düşer | Arayüz çevrilmemiş dilleri sunarak veremediği bir söz veriyordu. | geçerli · Faz 19.20 (2026-11-20) |
| **K221** | `verify:i18n`: çekirdek .tsx gömülü Türkçe metin mandalı (dosya başına tam eşit taban) | Çeviri borcu her yeni ekranla sessizce büyümesin. | geçerli · Faz 19.20 (2026-11-20) |

### 19.21 — `FE-02`: Hata sınırı yok: render hatası ve yüklenemeyen chunk ham hata ekranı veriyor

Kayıt: [`phases/faz-19/kayit/19-21-FE-02.md`](../../phases/faz-19/kayit/19-21-FE-02.md) · dallar: frontend `fix/2026-11-20-fe-02-error-boundary` · docs `docs/2026-11-20-fe-02-error-boundary`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K222** | Rota hata sınırları: katmanlı `errorElement` + markalı `RouteError` (editör kaydetme notu, misafir kapsamı) | Hata yayılacağı alanı çerçeve değil biz seçelim; editörde taslak kaybolmasın. | geçerli · Faz 19.21 (2026-11-20) |
| **K223** | `vite:preloadError` → tek seferlik yenileme, `sessionStorage` zaman damgası 60 s | Chunk hatasının çoğu bir yenilemeyle geçer; döngü olmamalı. | geçerli · Faz 19.21 (2026-11-20) |

### 19.22 — `TST-04`: Gerçek frontend + gerçek backend'i koşturan otomatik test yok

Kayıt: [`phases/faz-19/kayit/19-22-TST-04.md`](../../phases/faz-19/kayit/19-22-TST-04.md) · dallar: backend ve frontend `fix/2026-11-22-tst-04-e2e` · docs `docs/2026-11-22-tst-04-e2e`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K224** | Playwright e2e: Chromium, üç yolculuk (yayın+hediye kodu, misafir LCV→panel, yayındaki davetiyede plan duvarı), `npm run e2e` yerel, `check`'e girmez | Backend ↔ frontend sözleşmesini gerçek sunucuyla tek kapı koşturur. | geçerli · Faz 19.22 (2026-11-23) |
| **K225** | `scripts/e2e/backend.ps1`: yalnızca `davetkart_e2e*` adlı veritabanını sıfırdan kurar, ortamı süreçte verir, `.env`'e dokunmaz | Veritabanı silen betik geliştirme/test verisine asla dokunmamalı. | geçerli · Faz 19.22 (2026-11-23) |

### 19.23 — `FE-04`: Davetiye bağlantısının paylaşım önizlemesi yok (Open Graph)

Kayıt: [`phases/faz-19/kayit/19-23-FE-04.md`](../../phases/faz-19/kayit/19-23-FE-04.md) · dallar: backend ve frontend `fix/2026-11-23-fe-04-share-preview` · docs `docs/2026-11-23-fe-04-share-preview`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K230** | Paylaşım önizlemesi: Nginx bot eşlemesi → Laravel `GET /invite/{id}` (grupsuz web rotası) OG Blade; yalnızca yayındaki davetiye, misafir önbelleğiyle aynı anahtar; site geneli OG `index.html`'de | Bağlantı paylaşılınca davetiye tanınsın; UA sahteciliği taslak sızdırmasın. | geçerli · Faz 19.23 (2026-11-23) |

### 19.24 — `FE-10`: Ana giriş paketi 1,64 MB: 299 şablon her sayfaya, misafir sayfasına bile yükleniyor

Kayıt: [`phases/faz-19/kayit/19-24-FE-10.md`](../../phases/faz-19/kayit/19-24-FE-10.md) · dallar: frontend `fix/2026-11-23-fe-10-bundle-split` · docs `docs/2026-11-23-fe-10-bundle-split`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K227** | Şablonlar şablon başına tembel parça (`THEME_PRESETS` → `lazyTemplate`), katalog `templateCatalog.ts`'e ayrı, ana sayfa önizlemesi tembel, `verify:bundle` cırcır bütçe (ilk 720 kB / misafir 900 kB) | Her sayfa ve misafir 300 şablonu indirmesin; büyüme `check`'te kırmızı olsun. | geçerli · Faz 19.24 (2026-11-23) |

### 19.25 — `FE-53`: Kısıtlı mobil koşulda LCP 3,9–5,7 sn; giriş ve fiyat sayfalarında CLS 0,33–0,63

Kayıt: [`phases/faz-19/kayit/19-25-FE-53.md`](../../phases/faz-19/kayit/19-25-FE-53.md) · dallar: frontend `fix/2026-11-23-fe-53-mobile-vitals` · docs `docs/2026-11-23-fe-53-mobile-vitals`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K228** | `npm run perf` (kısıtlı mobil, 3 koşu ortanca; misafir LCP < 3 sn, CLS < 0,1), metrik eşlemeli yedek fontlar, tembel sayfa yer tutucusu `100svh`, hero videosu `load` sonrası | Kayma kaynağı ölçümle bulunur ve geri dönüş elle koşulan bütçeyle yakalanır. | geçerli · Faz 19.25 (2026-11-23) |

### 19.26 — `FE-50`: Sihirbaz her ziyarette sunucuda boş taslak açıyor; yenilemede editör kayboluyor

Kayıt: [`phases/faz-19/kayit/19-26-FE-50.md`](../../phases/faz-19/kayit/19-26-FE-50.md) · dallar: backend ve frontend `fix/2026-11-23-fe-50-draft-lifecycle` · docs `docs/2026-11-23-fe-50-draft-lifecycle`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K192** | Taslak yaşam döngüsü: ilk kayıt gerçek içerikte ya da "Davetiyeni Oluştur"da; adres `/create/<id>`; kullanıcı başına 50 yayınlanmamış davetiye, kilitli sayım, `403 DRAFT_LIMIT_REACHED` | Kayıt kullanıcının "bir şey yaptım" dediği anda açılmalı ve kimliği adreste durmalı; sınırsız satır açılamamalı | geçerli · Faz 19.26 (2026-11-23) |

**Eski kararların durum notları:**

- `K37` (taslak kimliği editörde) → **genişletildi** (K192): kimlik adreste de duruyor.

### 19.27 — `FE-54`: Hata ve başarı mesajları ekran okuyucuya duyurulmuyor; kontrast yetersiz

Kayıt: [`phases/faz-19/kayit/19-27-FE-54.md`](../../phases/faz-19/kayit/19-27-FE-54.md) · dallar: frontend `fix/2026-11-23-fe-54-accessibility` · docs `docs/2026-11-23-fe-54-accessibility`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K229** | Toast iki kalıcı canlı bölge (status/alert), kontrast WCAG AA (`gold-ink` tonu, alt bilgi /70), misafir sayfası `<main>`, `npm run e2e`'de 14 sayfalık axe taraması | Mesajlar ekran okuyucuya ulaşsın; kontrast geri kayarsa e2e kırmızı. | geçerli · Faz 19.27 (2026-11-23) |
