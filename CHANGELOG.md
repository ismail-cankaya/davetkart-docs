# Değişiklik Günlüğü

Bu deponun kendi değişiklikleri. En yeni üstte.

## 2026-11-27 — Faz 21 (`docs/2026-11-27-faz-21-backlog`)

- 21.0 hazırlık: dallar (`faz-21-backlog`, docs `docs/2026-11-27-faz-21-backlog`), ortam eşitlendi, taban kapıları yeşil (`composer check` 1306/1306, `composer audit` temiz, `npm run check` çıkış 0, e2e 6/6); backend `docs/rehber/fazlar/FAZ-21.md` açıldı. [`phases/faz-21/README.md`](phases/faz-21/README.md) §1.
- 21.1 `SEC-16`: girişte hesap başına, IP'den bağımsız kova (saatte 30 başarısız deneme, dolunca 429, sıfırlama boşaltır, sahibe IP'siz uyarı postası) — **K265** (varsayılan), [`EK-FAZ-21`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-21.md) açıldı, [`DECISION-INDEX.md`](decisions/DECISION-INDEX.md) (sıradaki K266), `decisions/README.md` satırı. `composer check` 1318/1318, e2e 6/6, 11 mutant öldü.
- 21.2 `SEC-15`: kayıt ucunun 422/201 farkı kabul edilen risk (sözleşme aynı); frenler (`throttle:auth` kovaları, iki yolda hash, `fields` yok) testle kilitlendi, kod eklenmedi — **K266** (varsayılan, B). `composer check` 1321/1321, e2e 6/6, 4 mutant öldü.

## 2026-11-27 — Faz 22 planı Faz 21 oldu, tek oturumda koşacak (`docs/2026-11-26-faz-21-plan`)

- [`phases/faz-21/README.md`](phases/faz-21/README.md) (eski `phases/faz-22/`): İsmail'in kararıyla 22.n → 21.n. Tek ajan bütün maddeleri tek oturumda, onay beklemeden koşar ve her maddeyi `faz-21-backlog` dalına commit'ler; commit'lerde ajan izi yok, push yok. Durma noktaları wip dalı + "bloke" kaçışına çevrildi; `SEC-18` yalnızca plan, `ARC-08` ve `SEC-17` yalnızca liste ve komut. Eksik kalan `FE-07` eklendi (21.16); `ARC-07` 21.18'e kaydı. Hazırlık (21.0) ve kapanış (21.90) maddeleri, ajana yapıştırılacak metin (§4). `phases/README.md`, `prompts/README.md`, Faz 20 takip tablosu ve `AUD-2026-11-26` raporundaki bağlantılar yeni yola çevrildi.

## 2026-11-26 — Faz 22 planı (`docs/2026-11-26-faz-22-plan`)

- [`phases/faz-21/README.md`](phases/faz-21/README.md) (yazıldığında `phases/faz-22/`): `AUD-2026-11-12`'nin hâlâ açık düşük/öneri bulguları ve Faz 20 ikinci taramasının karar soruları; 17 madde tek hatta, ortak çalışma biçimi ve her maddenin §A tablosu + prompt'u aynı sayfada. Kapanmış bulunanlar (`SEC-14`, `FE-05`, `ARC-09`, `FE-09`, `FE-56`) dışarıda. `phases/README.md`, `prompts/README.md`, Faz 20 takip tablosu ve `AUD-2026-11-26` raporu bağlantı aldı.

## 2026-11-26 — Faz 20 ikinci tarama: hesap yazma akışları ve frontend pürüzleri (`docs/2026-11-26-faz-20-critical-fixes`)

- Faz 14 elle doğrulaması ilk kez otomatik koşuldu (16/16); 20.7–20.10 frontend düzeltmeleri; `AUD-2026-11-12` düşük bulguları yeniden tarandı, beş karar sorusu [`phases/faz-20/README.md`](phases/faz-20/README.md) §İkinci tarama, rapor §4b.

## 2026-11-26 — Faz 20.4: deploy bakım kipinde (`docs/2026-11-26-faz-20-critical-fixes`)

- **K264** (İsmail: seçenek A): `deploy.sh` `git pull`'dan önce `artisan down`, göçten sonra `up`; hata olursa bakımda kalır. [`EK-FAZ-20`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-20.md), [`DECISION-INDEX.md`](decisions/DECISION-INDEX.md) (sıradaki K265), [`phases/faz-20/README.md`](phases/faz-20/README.md), [`YAYIN-SIRASI.md`](operations/deployment/YAYIN-SIRASI.md) §4.1 ve [`IZLEME.md`](operations/deployment/IZLEME.md) (deploy sırasında beklenen 503).

## 2026-11-26 — Faz 20: Faz 19 sonrası kritik hatalar (`docs/2026-11-26-faz-20-critical-fixes`)

- [`audits/2026-11-26-post-faz-19-scan/REPORT.md`](audits/2026-11-26-post-faz-19-scan/REPORT.md) (`AUD-2026-11-26`): Hesap Ayarları'nın üç sayfasındaki 500'ün kökü yerel veritabanının 4 göç geride olması (`OPS-10`); tarama 🔴 1 · 🟠 2 (`OPS-06` ↑, `SEC-51`) · 🟡 2 · 🟢 2.
- [`phases/faz-20/README.md`](phases/faz-20/README.md): 20.1 `schema` hazır olma kontrolü (**K263**), 20.2 Symfony 8.1.12, 20.3 `composer sync`, 20.6 `composer setup` anahtarı ezmez; 20.4 (deploy penceresi) karar bekliyor. `composer check` 1304/1304, `composer audit` temiz, e2e 6/6. Sıradaki K264.
- [`EK-FAZ-20`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-20.md), [`DECISION-INDEX.md`](decisions/DECISION-INDEX.md) (K263; K255 notu), [`IZLEME.md`](operations/deployment/IZLEME.md) (`schema`), `phases/README.md` ve `audits/README.md` satırları; Faz 19 satırındaki eski "PHPStan #11" engeli düzeltildi.

## 2026-11-26 — Hat B: B-D10 ve B-D14 kapandı (`docs/2026-11-26-hat-b-final`)

- [`phases/faz-19/HAT-B-ACIK-KALANLAR.md`](phases/faz-19/HAT-B-ACIK-KALANLAR.md) §9: editörden hemen çıkınca son düzenlemenin kaybolması (B-D10) ve 16 şablonda zarf ipucu kontrastı (B-D14) bulunup düzeltildi; birleşik uçta bütün kapılar yeşil; ajana kalan iş yok.

## 2026-11-26 — Hat A birleşik uçta e2e (`docs/2026-11-26-hat-a-e2e`)

- [`phases/faz-19/HAT-A-ACIK-KALANLAR.md`](phases/faz-19/HAT-A-ACIK-KALANLAR.md) §10: `npm run e2e` `faz-19-fix` ucunda (Hat A + Hat B birleşmeleri) ayrı veritabanı ve portlarla 5/5; ilk koşu soğuk başlangıçta kayıt zaman aşımıyla kırıldı, nedeni kayda geçti. D7 ve İ7 kapandı; kod değişmedi.

## 2026-11-26 — Hat B ikinci tur kayıtları (`docs/2026-11-26-hat-b-records`)

- K233–K237 (silme günlüğü, sipariş 10 yıl, paylaşım kapağı, e2e CI, paket bütçesi) [`decisions/DECISION-INDEX.md`](decisions/DECISION-INDEX.md) ve [`EK-FAZ-19.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md) "Hat B" bölümünde; [`YEDEK-VE-GERI-YUKLEME.md`](operations/deployment/YEDEK-VE-GERI-YUKLEME.md) §7.2/§9'a `data:reapply-deletions` adımı; [`HAT-B-ACIK-KALANLAR.md`](phases/faz-19/HAT-B-ACIK-KALANLAR.md) §9 güncellendi.

## 2026-11-25 — Hat A kalan eksikleri, ikinci tur (`docs/2026-11-25-hat-a-fixes-2`)

- [`phases/faz-19/HAT-A-ACIK-KALANLAR.md`](phases/faz-19/HAT-A-ACIK-KALANLAR.md) §9: E4 (iliştirmede bütçe), E6 (`media:move-disk`), E7 (`env:template --env`) kapandı; E5 kısmen: **K262** kartla ödemede gerçek telefon (yalnızca siparişte), TCKN/adres Shopier cevabını bekliyor (`notes/04` durumu, K125 kısmen geçersiz). `composer check` 1292/1292, `npm run check` yeşil; e2e koşmadı. Sıradaki K263. Komutlar: [`phases/faz-19/FAZ-19-HAT-A-FIX-COMMIT-KOMUTLARI.md`](phases/faz-19/FAZ-19-HAT-A-FIX-COMMIT-KOMUTLARI.md) §5–§6.

## 2026-11-25 — Hat A açık kalanları kapandı (`docs/2026-11-25-hat-a-fixes`)

- [`phases/faz-19/HAT-A-ACIK-KALANLAR.md`](phases/faz-19/HAT-A-ACIK-KALANLAR.md): §1'in 4 hatası kapandı (H2 taslak tavanı mesajı `faz-19-fix`'te), §2'den E1 (K260 hesap doğrulama göçü), E2 (K261 boş taslak temizlik komutu), E3, E8, E9; `composer check` 1279/1279 ve `npm run check` yeşil, e2e koşulmadı (§8). K260–K261 `DECISION-INDEX.md` ve EK-FAZ-19'a işlendi (sıradaki K262). Komutlar: [`phases/faz-19/FAZ-19-HAT-A-FIX-COMMIT-KOMUTLARI.md`](phases/faz-19/FAZ-19-HAT-A-FIX-COMMIT-KOMUTLARI.md).

## 2026-11-25 — Hat B bilinen hataları kapandı (`docs/2026-11-25-hat-b-fixes`)

- [`phases/faz-19/HAT-B-ACIK-KALANLAR.md`](phases/faz-19/HAT-B-ACIK-KALANLAR.md) §1'in 7 hatası (B-H1–B-H7) `faz-19-fix`'te kapandı; B-H2'nin kökü form yeniden bağlanması değil zarf animasyonundaki `inert`'ti; `composer check`, `npm run check` ve e2e (4/4) yeşil (§8). Komutlar: [`phases/faz-19/FAZ-19-HAT-B-FIX-COMMIT-KOMUTLARI.md`](phases/faz-19/FAZ-19-HAT-B-FIX-COMMIT-KOMUTLARI.md).

## 2026-11-25 — Hat C açık hataları kapandı (`docs/2026-11-25-hat-c-fixes`)

- [`phases/faz-19/HAT-C-ACIK-HATALAR.md`](phases/faz-19/HAT-C-ACIK-HATALAR.md): kod ve doküman maddeleri (#1, #2, #11–#20, #27, #30) kapandı; PHPStan'in iç hatası ortak sonuç önbelleğiydi (`tmpDir`), `composer check` uçtan uca yeşil (§E). Komutlar: [`phases/faz-19/FAZ-19-HAT-C-FIX-COMMIT-KOMUTLARI.md`](phases/faz-19/FAZ-19-HAT-C-FIX-COMMIT-KOMUTLARI.md); `phases/faz-19/README.md` üç hat raporunu listeliyor.

## 2026-11-25 — Hat C açık hatalar listesi (`docs/2026-11-25-hat-c-open-items`)

- [`phases/faz-19/HAT-C-ACIK-HATALAR.md`](phases/faz-19/HAT-C-ACIK-HATALAR.md) güncellendi: Faz 19 ortak düzeltme dalı için öncelik sırası; PHPStan (#11, #12, #1, #18, #19), `OPS-03` kılavuzları (#13), 19.28 artıkları (#14–#17, #20), sürüm etiketleri (#21), dal düzeni; #3, #4, #7 kapandı.

## 2026-11-25 — Faz 19.28 `ARC-03` ve Faz 19 kapanışı (`docs/2026-11-24-arc-03-k18-ratchet`)

- 19.28 `ARC-03`: K18 cırcırı `php artisan k18:check` `composer check`'te; `routes/api.php` ve `AppServiceProvider.php` uzun yorumları kılavuzlarına taşındı; 29 eksik kılavuz (K259; `DECISION-INDEX.md` sıradaki K260, K18 durum notu).
- Faz 19 kapanışı: 28/28 birleşti; tam takım, `composer audit`, frontend check/e2e/perf ✅; `composer check` PHPStan iç hatasıyla kırmızı → `v1.2.0` bekliyor ([`phases/faz-19/FAZ-19-ARC-03-COMMIT-KOMUTLARI.md`](phases/faz-19/FAZ-19-ARC-03-COMMIT-KOMUTLARI.md)); `phases/README.md` Faz 19 satırı.

## 2026-11-24 — Faz 19.90: hat kayıtları birleştirildi (`docs/2026-11-24-faz19-records`)

- 19.0 ve 19.2–19.27'nin kararları K182, K183–K192, K220–K232, K250–K258 ([`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md); `DECISION-INDEX.md`: sıradaki boş numara K259, eski karar durum notları, bekleyen aralık kaldırıldı); takip tablosu [`phases/faz-19/README.md`](phases/faz-19/README.md) `birleşti`; `prompts/README.md`: `faz-19-agent/`.
- 19.0 hazırlık: paralel hatlar için hat başına test veritabanı (`DAVETKART_TEST_DB_SUFFIX` → `davetkart_test_<son ek>`); `TestSuiteIsolationTest` genişletildi.
- 19.2 `ARC-01`: Karar indeksine K128–K145 eklendi; `build_decision_index.py --check` docs + backend tanımlarını indeksle karşılaştırıyor (K250, K251).
- 19.3 `ARC-02`: Backend `FAZ-16.md`, `FAZ-17.md` ve kısa elle doğrulama dosyaları; Faz 16–17'nin 19 Gold şablonu K252 ile kayda geçti; `FAZ-15.md`'ye kapı durum notu.
- 19.4 `ARC-05`: Backend `claude/` (22 dosya) docs'a birebir taşındı, 25 dosyadaki eski yollar `davetkart-docs: …` biçimine çevrildi, K49–K106 kaynakları docs'ta (K253, K254).
- 19.5 `ARC-04`: Üretimde medya diski `s3` değilse sahip ve misafir yüklemeleri 503 ile reddediliyor, `php artisan about` diski gösteriyor; K55 → K183.
- 19.6 `OPS-04`: Üretim `.env` şablonu Y8.3b düzeltmeleriyle güncellendi, `env:template --check` `composer check`'e girdi, üretimde `log` posta sürücüsü CRITICAL log ve `about` uyarısı veriyor; K184–K185.
- 19.7 `OPS-03`: `GET /api/health` (veritabanı, kuyruk, zamanlayıcı, disk; ayrıntısız 503), zamanlayıcı kalp atışı, başarısız iş bildirimi (K255, K256); `operations/deployment/IZLEME.md`.
- 19.8 `OPS-05`: `operations/deployment/SURE-TAKVIMI.md` (alan adı, posta, AWS kredisi, SSL; 30/7 gün hatırlatıcı, posta karar tablosu) ve `davetkart-sure-takvimi.ics`; `.ics` için CRLF kuralı.
- 19.9 `SEC-05`: Kayıt, sıfırlama ve parola değiştirme yaygın parolaları ve tek karakter tekrarını reddeder; tek kural kaynağı `PasswordPolicy` (K258).
- 19.10 `SEC-06`: Genel API hız sınırı girişli kullanıcıda kullanıcı anahtarlı (120/dk), misafir davetiye okuması ayrı kovada (300/dk), misafir medya IP kovası 60/dk; K186.
- 19.11 `TST-02`: 17 kilidin her biri SQL düzeyinde, para/kota kilitleri iki bağlantılı testle korunuyor (17/17 mutant öldü); serbest hakkın iade talebiyle yarışı düzeltildi; K187–K188.
- 19.12 `FE-51`: Misafir foto/video yükleme ucu `DAVETKART_GUEST_UPLOADS` bayrağıyla kapatıldı (varsayılan kapalı, 404). Yanıtta `guestUploads` alanı yayınlanıyor. Arayüzdeki ölü `RsvpModal`, `uploadAsGuest` ve `onRsvpClick` kaldırıldı (K189).
- 19.13 `SEC-08`: Misafir yüklemesine davetiye başına 1 GB iliştirilmiş bayt bütçesi ve iliştirilmemişler için ayrı kota (50 dosya / 200 MB) geldi. Yetim süresi 24 saatten 1 saate indi, temizlik saatlik koşuyor (K190).
- 19.14 `SEC-09`: Kayıtta doğrulama postası (imzalı, 24 saat). Doğrulanmamış hesap ödeme başlatamaz ve yayınlayamaz (`EMAIL_NOT_VERIFIED`), ilk yayın indirimi alamaz. Yeniden gönderme saatte 3. Arayüzde doğrulama bandı ve `/eposta-dogrula` sayfası var (K191).
- 19.15 `SEC-10`: Shopier'e dijital üründe TCKN/telefon/adres alanları için gönderilecek soru hazırlandı (`notes/04`); cevap gelene kadar kod değişmedi (K125 bekliyor).
- 19.16 `SEC-13`: `data:purge` tarihsiz davetiyenin misafir verisini yayın/oluşturma + 12 ay sonra siler, `--dry-run` ayrı sayar (K257).
- 19.17 `SEC-12`: Fontlar kendi alan adımızdan sunuluyor; CSP'den Google Fonts çıktı, `verify:fonts` geri dönüşü yakalar (K226).
- 19.18 `SEC-11`: Gizlilik metni yedeklerden silinme süresini (en geç 40 gün) ve veri işleyenleri adıyla söylüyor; `verify-render` sabiti ve adları kilitliyor (K231).
- 19.19 `FE-52`: Fiyat sayfası SSS'si yayın süresi ve ücretli uzatma vaat etmiyor; davetiye siz silene kadar yayında, misafir verisi etkinlikten 6 ay sonra silinir (K232).
- 19.20 `FE-01`: Dil seçici yalnızca tr/en sunuyor, eski kayıtlı dil tr'ye düşüyor (K220); `verify:i18n` gömülü Türkçe metin mandalı (K221).
- 19.21 `FE-02`: Rotalarda markalı hata sınırı (editörde kaydetme notu, misafir kapsamı) (K222); yüklenemeyen chunk'ta tek seferlik yenileme (K223).
- 19.22 `TST-04`: Playwright ile üç uçtan uca yolculuk ve tek komutluk e2e ortamı (`npm run e2e`) (K224, K225).
- 19.23 `FE-04`: Davetiye bağlantısı WhatsApp/Telegram'da adlar, tarih ve mekânla önizleniyor (yalnızca yayındaki davetiye); site geneli OG etiketleri (K230).
- 19.24 `FE-10`: Ana paket 1.58 MB → 699 kB: şablonlar tembel parçalarda, katalog ayrı, `verify:bundle` bütçesi (K227).
- 19.25 `FE-53`: Kısıtlı mobilde CLS dört sayfada 0–0,014 (önce 0,18–0,63), `npm run perf` bütçesi (K228).
- 19.26 `FE-50`: Sihirbaz artık yalnızca gerçek içerikte ya da "Davetiyeni Oluştur"da taslak açıyor. Adres `/create/<id>` olduğu için yenileme aynı taslağa dönüyor. Kullanıcı başına 50 taslak tavanı var (`DRAFT_LIMIT_REACHED`, K192).
- 19.27 `FE-54`: Bildirimler ekran okuyucuya duyuruluyor, 14 sayfada kontrast/yer işareti ihlali sıfır ve `npm run e2e`'de axe taraması (K229).

## 2026-11-20 — Faz 19.1 `SEC-07` kayıtları (`docs/2026-11-20-faz-19-audit-fixes`)

- Yeni `composer.lock` temiz (`composer audit --locked`; `vendor` kurulumu ve yeni `vendor` ile kapılar İsmail'de, GitHub erişilemedi), Shopier callback adresi `APP_URL`'den: K179–K181 ([`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md) yeni; `DECISION-INDEX.md`: sıradaki boş numara K182, K150 için "tamamlandı → K181"; `decisions/README.md`); [`operations/deployment/YAYIN-SIRASI.md`](operations/deployment/YAYIN-SIRASI.md) §2 madde 2 ve §3 etiket mesajı; [`phases/faz-19/FAZ-19-SEC-07-COMMIT-KOMUTLARI.md`](phases/faz-19/FAZ-19-SEC-07-COMMIT-KOMUTLARI.md) (19.1 + `v1.1.0` blokları); `phases/faz-19/README.md`, `phases/README.md` satırları; `phases/faz-18/FAZ-18-SEC-04-COMMIT-KOMUTLARI.md` §5 durum notu.

## 2026-11-20 — Faz 19 prompt'ları (`docs/2026-11-20-faz-19-audit-fixes`)

- `AUD-2026-11-12`'nin 28 orta (🟡) bulgusu için 28 prompt (`TST-01` Faz 18.1'de kapandı): `prompts/PROMPT-FAZ-19-01-SEC-07.md` … `PROMPT-FAZ-19-28-ARC-03.md`; takip tablosu ve sıra gerekçesi [`phases/faz-19/README.md`](phases/faz-19/README.md); `prompts/README.md` ve `phases/README.md` satırları.

## 2026-11-20 — Faz 18.6 `SEC-04` kayıtları ve Faz 18 kapanışı (`docs/2026-11-16-faz-18-audit-fixes`)

- SPA güvenlik başlıkları Nginx'te: K173–K178 ([`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md) §18.6; `DECISION-INDEX.md`: sıradaki boş numara K179, K85 için "daraltıldı → K173"); [`operations/deployment/YAYIN-SIRASI.md`](operations/deployment/YAYIN-SIRASI.md) §4.4 (Nginx kurulumu) ve §6 (duman testi); [`phases/faz-18/FAZ-18-SEC-04-COMMIT-KOMUTLARI.md`](phases/faz-18/FAZ-18-SEC-04-COMMIT-KOMUTLARI.md) (SEC-04 + Faz 18 kapanış komutları; etiket komutları `SEC-07` yüzünden yok); `phases/faz-18/README.md` ve `phases/README.md` Faz 18 satırları.

## 2026-11-20 — Faz 18.5 `SEC-03` kayıtları (`docs/2026-11-16-faz-18-audit-fixes`)

- Shopier `callback` kipi üretimde reddedilir: K170–K172 ([`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md) §18.5; `DECISION-INDEX.md`: sıradaki boş numara K173, K117 için "daraltıldı → K170", K122/K126 için "genişletildi" ve K94 için kaldırma notu); [`phases/faz-18/FAZ-18-SEC-03-COMMIT-KOMUTLARI.md`](phases/faz-18/FAZ-18-SEC-03-COMMIT-KOMUTLARI.md); `phases/faz-18/README.md` satırları.

## 2026-11-20 — Faz 18.4 `SEC-02` kayıtları (`docs/2026-11-16-faz-18-audit-fixes`)

- Yayın yapmış hak iade edilmez: K164–K169 ([`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md) §18.4; `DECISION-INDEX.md`: sıradaki boş numara K170, K82 için "daraltıldı → K164", K139 için "daraltıldı → K166" notu); [`phases/faz-18/FAZ-18-SEC-02-COMMIT-KOMUTLARI.md`](phases/faz-18/FAZ-18-SEC-02-COMMIT-KOMUTLARI.md); `phases/faz-18/README.md` satırları.

## 2026-11-16 — Faz 18.3 `SEC-01` kayıtları (`docs/2026-11-16-faz-18-audit-fixes`)

- "İlk yayın" indirimi tek açık siparişe: K158–K163 ([`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md) §18.3; `DECISION-INDEX.md`: sıradaki boş numara K164, K131 için "daraltıldı → K159" notu); [`phases/faz-18/FAZ-18-SEC-01-COMMIT-KOMUTLARI.md`](phases/faz-18/FAZ-18-SEC-01-COMMIT-KOMUTLARI.md); `phases/faz-18/README.md` satırları.

## 2026-11-16 — Faz 18.2 `OPS-02` kayıtları (`docs/2026-11-16-faz-18-audit-fixes`)

- Yedek ve geri yükleme çalıştırma kitabı [`operations/deployment/YEDEK-VE-GERI-YUKLEME.md`](operations/deployment/YEDEK-VE-GERI-YUKLEME.md) (bucket, IAM politikası, sunucu kurulumu, prova kaydı); K151–K157 ([`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md), `DECISION-INDEX.md`: sıradaki boş numara K158); `YAYIN-PLANI.md` Y11.5–Y11.6 bağlantıları ve ilerleme satırı; `YAYIN-SIRASI.md` kontrol listesi 6. madde; [`phases/faz-18/FAZ-18-OPS-02-COMMIT-KOMUTLARI.md`](phases/faz-18/FAZ-18-OPS-02-COMMIT-KOMUTLARI.md); `phases/faz-18/README.md` ve `operations/README.md` satırları.

## 2026-11-16 — Faz 18.1 `OPS-01` kayıtları (`docs/2026-11-16-faz-18-audit-fixes`)

- Yayın sırası ve sürüm etiketi çalıştırma kitabı [`operations/deployment/YAYIN-SIRASI.md`](operations/deployment/YAYIN-SIRASI.md); K146–K150 ([`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md), `DECISION-INDEX.md`: sıradaki boş numara K151, K128–K145 için ⚠️ notu); [`phases/faz-18/FAZ-18-OPS-01-COMMIT-KOMUTLARI.md`](phases/faz-18/FAZ-18-OPS-01-COMMIT-KOMUTLARI.md); `phases/faz-18/README.md`, `operations/README.md`, `decisions/README.md` satırları.
- Aynı gün: `phases/faz-18/README.md` `OPS-01` satırı ve `FAZ-18-OPS-01-COMMIT-KOMUTLARI.md` gerçek duruma göre güncellendi (atılan commit'lerin kimlikleri, kalan üç blok).

## 2026-11-16 — Faz 18 prompt'ları (`docs/2026-11-16-faz-18-audit-fixes`)

- `AUD-2026-11-12`'nin altı yüksek (🟠) bulgusu için altı prompt: `prompts/PROMPT-FAZ-18-{1..6}-*.md`; takip tablosu [`phases/faz-18/README.md`](phases/faz-18/README.md); `prompts/README.md` ve `phases/README.md` satırları.

## 2026-11-15 — Genel sistem denetimi (`audit/2026-11-12-full-system-audit`)

- `AUD-2026-11-12`: [`audits/2026-11-12-full-system-audit/`](audits/2026-11-12-full-system-audit/README.md) eklendi (rapor, beş bulgu dosyası, kanıt klasörü); `audits/README.md` listesine işlendi. Başka doküman değişmedi.

## 2026-11-12 — Depo düzenlemesi (`docs/2026-11-12-restructure`)

- Başlangıç commit'i: depo o anki hâliyle git'e alındı. Eski `davetkart-claude` deposunun `.git`'i
  depo dışına (`D:\Projects\davetkart\_backup\davetkart-claude.git`) taşındı; eski geçmiş o uzak depoda.
- `.gitignore`: kod arşivleri (`.tgz`, `.tar`, `.bundle`) git dışı; üçünde `.env` var.
- Klasör yapısı: `context/`, `decisions/`, `phases/`, `prompts/`, `audits/`, `operations/`,
  `product/`, `notes/`, `archive/`. 277 dosya taşındı, içerikleri değişmedi.
- Arşive giden 3 dosyaya tek satırlık arşiv bandı eklendi; `archive/README.md`.
- Yeni: `decisions/DECISION-INDEX.md` (K1–K127), klasör `README.md`'leri, kök `README.md`,
  `CLAUDE.md`, `AGENTS.md`, bu dosya.
- Kayıtlar: [`_restructure/`](_restructure/REPORT.md) (envanter, taşıma planı, rapor, betikler).
