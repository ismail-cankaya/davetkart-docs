# AUD-2026-11-12 — Denetim Planı

> **Yürütenler için:** bu plan `superpowers:writing-plans` ile yazıldı ve
> `superpowers:dispatching-parallel-agents` ile yürütülür. Her dilim ajanı kendi görevini (§4) ve
> herkes için geçerli bölümleri (§1, §2, §3, §5, §6, Ek A) okur. Adımlar `- [ ]` ile işaretlenir.
> Bu bir **denetim** planıdır: "test" yerine **kanıt**, "commit" yerine **bulgu dosyası** vardır.

**Amaç:** DavetKart'ın (backend + frontend) yayın öncesi bağımsız denetimi; çıktı beş bulgu dosyası,
kanıt klasörü ve `REPORT.md`.

**Yaklaşım:** En yeni uzak dalların anlık görüntüsü depo dışına çıkarıldı; her dilim kendi yalıtılmış
kopyasında okur ve koşturur. A, B1, B2, C, D1, D2 paralel; E onlar bitince; rapor en sonda.

**Yığın:** PHP 8.5.12 · Laravel 13.35.0 · PostgreSQL 18.4 · Node 24.18 · npm 11.16 · React 19 · Vite 6 · TypeScript 5.8.

**Şartname:** İsmail'in 12 Kasım 2026 tarihli denetim prompt'u (sohbette verildi; `prompts/` altında
dosyası yok). Ajanların ihtiyaç duyduğu her bölüm bu dosyaya **aynen** alındı (§3, §4, §5, Ek A).

## 1. Genel kısıtlar

- **Ek A (§0) her ajan için bağlayıcıdır.** Özeti: kod depoları ve `davetkart-docs` salt okunur · git
  yazma işlemi yok · B7 (görmediğine "doğrulandı" yazma; kanıt türü `KOŞTURULDU` / `KOD OKUMASI` /
  `VARSAYIM`) · canlı sisteme istek yok · sır değeri hiçbir yere yazılmaz · Türkçe ve öğretici.
- **Yazılabilen yerler:** yalnızca `davetkart-docs/audits/2026-11-12-full-system-audit/` ve ajanın
  **kendi** anlık görüntü kopyası (§2). Başka ajanın kopyasına ve gerçek depolara yazılmaz.
- **Gerçek depolarda** (`D:\Projects\davetkart\davetkart-backend-php-laravel`, `…\davetkart-frontent`)
  yalnızca git **okuma** komutları koşar (`log`, `show`, `diff`, `grep`, `ls-tree`, `blame`).
  Denetlenen ref: `origin/ccr-9a346997-bu6gve`. Yerel çalışma ağacı **eskidir**; kod okuması için
  kullanılmaz.
- **Dosya atıfı:** `backend:app/Actions/…php:42` ya da `frontend:src/…tsx:10` (depo köküne göre,
  denetlenen commit'te).
- **Gerçek `.env` okunmaz.** Dolu/boş durumu gerekiyorsa değerleri maskeleyen bir komutla alınır.
  Kopyalardaki `.env` dosyaları `.env.example`'dan üretildi; içlerinde yalnızca yerel PostgreSQL
  parolası vardır, o da yazılmaz.
- **Dış ağ:** paket kayıtları (Packagist, npm) ve resmî dokümanlar serbest. `davetkart.com`,
  `media.davetkart.com`, AWS, SES, Shopier, Gemini, Sentry: **yasak**.
- **Alt ajan açılmaz.** Her dilim tek ajandır.
- Depoda commit'lenmiş **gerçek bir sır** bulan ajan değeri yazmadan yerini bildirir ve **hemen durur**.

## 2. Ortam: anlık görüntü ve kopyalar

Kurulum kaydı: `evidence/scripts/00-snapshot-setup.sh`, `evidence/scripts/01-env-and-db-setup.php`,
`evidence/commands/00…02-*.txt`. Kök: `D:\Projects\davetkart\_audit-snap\` (depo değil).

| Kopya | Commit | Kim yazar | Uygulama DB | Test DB (`phpunit.xml`) | Port |
|---|---|---|---|---|---|
| `backend` | `d810410` | **kimse** (referans; A okur, artisan okuma komutları) | `davetkart_aud_arc` | `davetkart_aud_arc_test` | 8300 |
| `backend-sec` | `d810410` | B1 | `davetkart_aud_sec` | `davetkart_aud_sec_test` | 8200 |
| `backend-tst` | `d810410` | C (mutasyon burada) | `davetkart_aud_tst` | `davetkart_aud_tst_test` | 8400 |
| `backend-e2e` | `d810410` | D2 | `davetkart_aud_e2e` | `davetkart_aud_e2e_test` | **8000** |
| `frontend` | `44caa49` | D2 (dev sunucu **3000**); D1 ve B2 yalnızca okur | — | — | 3000 |
| `frontend-tst` | `44caa49` | C (`npm run check`, build); B2 `npm audit` | — | — | — |

- Kopyalarda kaynak koda yapılan **tek** fark: `phpunit.xml` → `DB_DATABASE` (İsmail'in
  `davetkart_test` veritabanı silinmesin diye). `vendor/` gerçek depodan kopyalandı (`composer.lock`
  aynı); `node_modules/` `npm ci` ile kuruldu.
- `.env`: `AI_PROVIDER=null`, `MAIL_MAILER=log`, `PAYMENT_PROVIDER=fake`, Sentry ve AWS boş.
  `backend-sec` ve `backend-e2e`'de ayrıca `PAYMENT_METHODS=card,gift_code`, `QUEUE_CONNECTION=sync`.
  Ajan kendi kopyasının `.env`'ini değiştirebilir; değişikliği bulgu dosyasına yazar.
- **PHP:** PowerShell'de `php` / `composer` (Herd `.bat`). Git Bash'te `php` yok; orada
  `/c/Users/ismail/.config/herd/bin/php85/php.exe` kullanılır.
- Vite proxy'si `http://localhost:8000`'e sabit (`frontend:vite.config.ts:25`); bu yüzden yalnızca
  D2 8000'i kullanır.
- Playwright MCP tek tarayıcıdır: **yalnızca D2** kullanır.

## 3. Regresyon listesi ve sahipleri

Durum: ✅ kapandı · 🟡 kısmen · ❌ açık · ❓ doğrulanamadı. Her sahip kendi satırlarını bulgu
dosyasının sonundaki **"Regresyon"** tablosuna yazar (kaynak · bulgu · durum · kanıt türü · kanıt).

| # | Kaynak | Bulgu | Sahip |
|---|---|---|---|
| R1 | Review §1.1 / K-1 | Yayından sonra `PUT` ile üst plan modülleri açılıyor (paywall bypass) | B1 (API) · C (mutasyon) · D2 (arayüz) |
| R2 | Review §1.2 / K-4 | Süresi dolan siparişe geç gelen `paid` bildirimi sessizce yutuluyor | B1 · C (mutasyon) |
| R3 | Review §2.1 | Ödeme dönüş sayfası + `GET /orders/{id}` + `publishedAt` | D1 (sözleşme) · D2 (yolculuk 3) |
| R4 | Review §2.2 | Sanctum token ömrü (`expiration => null`), `sanctum:prune-expired` etkisiz | B1 |
| R5 | Review §2.3 | `TrustProxies` / gerçek istemci IP'si | B1 · E (Nginx tarafı) |
| R6 | Review §2.4 | Parola sıfırlama, e-posta doğrulama, hesap silme, KVKK saklama süresi (`data:purge`) | B1 (akışlar) · B2 (KVKK) |
| R7 | Review §5.1 | 4xx iş istisnalarının Sentry'ye gitmesi | A |
| R8 | Review §5.2 | Fiyat sayfası vaatleri ↔ sunucu kuralları (logosuz yayın, premium tema, video galerisi) | D1 · A |
| R9 | Review §5.4–5.5 | Hız sınırları (CGNAT), video boyutu, mükerrer LCV | B1 |
| R10 | Review §6.1–6.10 | Ölü dosya/config, `mapUrl` şeması, `preventStrayRequests`, `SENTRY_LARAVEL_DSN` testte, git hijyeni, CRLF / `.gitattributes` | A (ölü kod, git hijyeni, CRLF) · C (`preventStrayRequests`, Sentry) |
| R11 | Test denetimi K-2…K-8 | NUL baytı, Türkçe `İ` e-posta normalizasyonu, `Retry-After` başlığı, yarım JSON → 400, `integer:strict`, `mapUrl` şemaları | C (testle) · B1 (canlı istekle) |
| R12 | Test denetimi §2 | Mutasyonda hayatta kalan testler (InvitationTest, PublicInvitationTest cache anahtarı, PaywallTest fiyat/para birimi, AuthTest, HardeningTest HSTS) | C |
| R13 | Faz 7 açık soru | Paket alımın kaç yayın açtığı (`publish_quota`, K43) | A |
| R14 | Faz 11–12 | Hediye kodu kötüye kullanımı (yarış durumu, tekrar kullanım, tutarın sunucuda hesaplanması) · Shopier imza/OSB/`status` imzasızlığı · open redirect · tutar doğrulaması | B1 |
| R15 | Faz 14 | Plan hakkı sayısı, hak iptali/iade talebi, güvenli e-posta değişikliği | B1 (güvenlik) · A (tasarım) · D2 (yolculuk 6) |
| R16 | Fiyat kararı | Fiyatların yalnızca backend'den gelmesi, indirim/ilk yayın indirimi, ödeme yöntemlerinin tek ayarla açılıp kapanması | D1 (frontend) · A (backend) |
| R17 | `DECISION-INDEX.md` | "Geçerli" işaretli kararların kodda gerçekten uygulandığı (en az: ödeme/paywall, medya, hata sözleşmesi, güvenlik kararları; örneklem yöntemini yaz) · ⚠️ işaretli numara çakışmalarının kodu etkileyip etkilemediği | A |

Önceki raporlar (hepsi `_audit-snap\backend\claude\` altında): `GOZDEN-GECIRME-RAPORU.md` (23 Eylül,
"Review §…" atıfları buna), `TEST-DENETIMI-2026-09-24.md` (K-1…K-8), `GOZDEN-GECIRME-2026-10-09-BACKEND.md`,
`GOZDEN-GECIRME-2026-10-09-FRONTEND.md`, `FAZ-10-PLANI.md` (K87–K106).

## 4. Dilimler

Her dilim için ortak adımlar:

- [ ] `davetkart-docs/CLAUDE.md` ve bu planı oku; dilimin "Önce oku" listesini oku.
- [ ] Kapsam maddelerini sırayla denetle; her bulguyu §5 biçiminde, kanıtıyla yaz.
- [ ] Sahibi olduğun regresyon satırlarını (§3) kapat.
- [ ] `superpowers:verification-before-completion`: her `KOŞTURULDU` bulgusunun kanıt dosyası var mı,
  dosyadaki çıktı iddiayı gerçekten gösteriyor mu, atıf verilen `dosya:satır` doğru mu?
- [ ] Bulgu dosyasını §6'daki iskeletle bitir; ana oturuma kısa özet dön.

### A — Mimari ve kod kalitesi (backend) · `ARC-01…` → `findings/01-architecture.md`

**Kopya:** `backend` (yalnızca okuma + `php artisan route:list`, `about`, `migrate:status`, `schedule:list`,
`db:table` gibi okuma komutları; **test koşturma**).
**Önce oku:** `backend/CLAUDE.md` · `backend/docs/03-MIMARI-PLAN.md` · `docs/08-HATA-SOZLESMESI.md` ·
`docs/09-TUM-FAZLAR-PLANI.md` · `docs/rehber/fazlar/FAZ-13.md`, `FAZ-14.md`, `FAZ-15.md` ·
`claude/GOZDEN-GECIRME-RAPORU.md` · `claude/GOZDEN-GECIRME-2026-10-09-BACKEND.md` ·
`claude/FAZ-10-PLANI.md` §2 · `davetkart-docs/decisions/DECISION-INDEX.md` ve `decisions/addenda/`.

- Katman kuralları: Controller → Request → Action → Model/Service; iş kuralı Controller'da veya Model'de sızmış mı? Action'lar tek sorumluluklu mu?
- SOLID, bağımlılık yönü, Strategy (ödeme/AI sürücüleri), DTO/değer nesneleri, enum kullanımı, transaction ve kilit sınırları, idempotans.
- Hata sözleşmesi (`docs/08`): zarf, hata kodları, HTTP durumları tutarlı mı; `contracts/error-codes.json` iki depoda aynı mı? (`backend/contracts/…` ↔ `frontend/src/contracts/…`)
- Veritabanı: migration'lar, index'ler, CHECK/UNIQUE kısıtları, N+1 (eager loading), soft delete ve veri saklama, para birimi (minor units, float yok).
- Kuyruk, zamanlayıcı, cache (anahtar tasarımı, temizleme), dosya depolama (`disk + path`).
- Ölü kod, kopya mantık, karmaşıklığı yüksek dosyalar (en büyük 15 dosya + en çok değişen 15 dosya; gerçek depoda `git log origin/ccr-9a346997-bu6gve --format= --name-only | sort | uniq -c | sort -rn`).
- `docs/rehber/` kılavuzu olmayan kod dosyaları (K18).
- **Dokümantasyon ↔ kod kayması:** backend `docs/` ve `davetkart-docs` içindeki "güncel" belgelerin kodla çeliştiği yerler; kod depolarında hâlâ eski `claude\...` yoluna atıf veren dosyalar (`CLAUDE.md`, `README.md`, `docs/`). Faz 16 ve 17'nin faz kaydı yok; bunu da değerlendir. Yalnızca raporla.
- Laravel 13 / Sanctum / kuyruk / zamanlayıcı API'lerinin güncel dokümana göre doğru ve deprecated olmadığı (Context7 bağlı değil → resmî doküman; bakamadığını "doğrulanamadı" yaz).
- Regresyon: R7, R8 (sunucu tarafı), R10 (ölü kod, git hijyeni, CRLF), R13, R15 (tasarım), R16 (backend), R17.

### B1 — Güvenlik: backend · `SEC-01…SEC-49` → `findings/02-security-b1.md`

**Kopya:** `backend-sec` (sunucu 8200, PHPUnit, `curl`, geçici test dosyaları burada serbest).
**Önce oku:** `claude/FAZ-10-PLANI.md` · `davetkart-docs/decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md`, `-12.md` ·
`davetkart-docs/phases/faz-12/FAZ-12-RAPOR.md` · `docs/rehber/fazlar/FAZ-11…14.md` ve `…-ELLE-DOGRULAMA.md` ·
`docs/08-HATA-SOZLESMESI.md` · iki gözden geçirme raporu.
Referans: **OWASP ASVS 4.0.3 Seviye 2** ve **OWASP API Security Top 10 (2023)**. Her başlık için ✅/❌/N-A tablosu.

- Kimlik doğrulama ve oturum: Sanctum token ömrü/iptali, parola politikası ve hash (Argon2id), parola sıfırlama, e-posta doğrulama, kullanıcı numaralandırma, kaba kuvvet koruması.
- Yetkilendirme: her uçta nesne düzeyinde sahiplik (BOLA/IDOR), toplu atama (`fillable`/`guarded`), fonksiyon düzeyinde yetki. **Her rota** için (`route:list`) sahiplik kanıtı tablosu.
- Girdi: doğrulama kuralları, NUL baytı, Unicode normalizasyonu, `url` şemaları, dosya yükleme (içerikten MIME, boyut, polyglot, SVG, EXIF temizleme), yol geçişi.
- Ödeme: fiyatın sunucuda hesaplanması, imza karşılaştırması (`hash_equals`), tekrar oynatma, idempotans, tutar/para birimi doğrulaması, open redirect, sır eksikliğinde fail-safe.
- Hediye kodu: tahmin edilebilirlik, eşzamanlı kullanım yarışı, kullanım sayacının kilitlenmesi.
- Hız sınırları ve IP tespiti (TrustProxies, IPv6 /64).
- Başlıklar (API tarafı): CSP, HSTS, CORS, `X-Content-Type-Options`, frame koruması.
- Loglara/Sentry'ye kişisel veri ya da sır gidiyor mu (kod okuması; Sentry'ye istek yok).
- Regresyon: R1, R2, R4, R5, R6 (akışlar), R9, R11 (canlı istekle), R14, R15 (güvenlik).
- Shopier sürücüsü **yalnızca** kod okuması ve sahte imzalı yerel isteklerle denetlenir; Shopier'e istek atılmaz.

### B2 — Güvenlik: frontend, sırlar, bağımlılıklar, KVKK · `SEC-50…SEC-99` → `findings/02-security-b2.md`

**Kopya:** `frontend` (okuma), `frontend-tst` (`npm audit`, C ile paylaşılır: build çıktısına dokunma), `backend` (okuma; `composer audit` için `backend-sec` değil `backend` kullan, yazmaz).
**Önce oku:** `claude/GOZDEN-GECIRME-2026-10-09-FRONTEND.md` · `backend/docs/10-URETIM-ENV-SABLONU.md` ·
`backend/deploy/nginx/davetkart.conf` · `claude/FAZ-10-PLANI.md` (K97, K98) · `davetkart-docs/operations/deployment/YAYIN-PLANI.md`.

- Frontend: token'ın `localStorage`'da saklanmasının riski (XSS ile çalınma), `dangerouslySetInnerHTML`, kullanıcı içeriğinin render'ı, harici script/CDN, kaynak haritalarının build'e girip girmediği.
- Başlıklar (frontend tarafı): Nginx / Vite build için CSP, HSTS, `X-Content-Type-Options`, frame koruması.
- Sırlar: depoda sızmış sır var mı (üç gerçek depoda `git log -p --all` içinde anahtar kalıpları: `AIza`, `AKIA`, `sk-`, `-----BEGIN`, Sentry DSN, `SHOPIER`, parola atamaları; `.env.example`). **Eşleşen değeri yazdırma**: yalnızca commit + dosya + satır + maskeli hâl. Gerçek sır bulursan dur.
- Bağımlılıklar: `composer audit`, `npm audit --omit=dev` ve tüm ağaç; kritik/yüksek olanları GitHub Advisory ile doğrula.
- **Bağımlılık tablosu** (rapor §10): `composer.json` ve `package.json`'daki her doğrudan bağımlılık için kurulu sürüm ↔ güncel kararlı sürüm (`composer outdated --direct`, `npm outdated`), güvenlik notu, aksiyon. Context7 bağlı değil; kaynağı "Packagist/npm kaydı" diye yaz. Frontend `main`'deki `47aedc8` (bağımlılık düzeltmesi) denetlenen dalda yok: farkı `git show 47aedc8` ile oku ve değerlendir.
- **KVKK:** misafir kişisel verisi (ad, mesaj, fotoğraf/video), saklama ve silme, S3 sürümleme ile silmenin gerçekten silme olup olmadığı, aydınlatma metni ve gizlilik politikasının sitede varlığı.
- Regresyon: R6 (KVKK kısmı).

### C — Testler ve kalite kapısı · `TST-01…` → `findings/03-testing.md`

**Kopya:** `backend-tst`, `frontend-tst`.
**Önce oku:** `claude/TEST-DENETIMI-2026-09-24.md` · `docs/rehber/fazlar/FAZ-15.md` (§3: bu dalda `composer check` **hiç koşmadı**) · `docs/rehber/phpunit.md` · `backend/.github/workflows/ci.yml`, `frontend/.github/workflows/ci.yml`.

- Backend: `composer check` (pint + phpstan + testler). Son satırı ve süreyi kaydet. Kırmızı varsa nedenini sınıflandır (ortam mı — ör. anlık görüntüde satır sonu —, gerçek hata mı).
- Frontend: `npm run check` (tip kontrolü, build, verify). Build çıktısının boyutu, en büyük 10 parça.
- Kapsam: hangi uçların/Action'ların hiç testi yok? Test piramidi (Unit/Feature/E2E) dengesi.
- **Örnek mutasyon:** §3'teki kritik kuralların her biri için üretim kodunda tek satırı boz, ilgili testi koştur, kodu geri al. Sonuç tablosu: mutant öldü mü, hayatta mı? Her denemeden sonra `backend-tst` ↔ `backend` karşılaştırması (`diff -rq`, `vendor`/`storage`/`bootstrap/cache`/`.env`/`.phpunit.cache` hariç) **boş** olmalı. Kayıt: `evidence/mutation/M<NN>-<ad>.txt` (mutasyon diff'i + test çıktısı + geri alma kanıtı). Koşan test sayısı 0 ise sonucu reddet.
- Test kalitesi: gerçekçi Türkçe veri mi, oyuncak veri mi; yanıtı mı yoksa etkiyi (DB durumu) mu doğruluyor (T14); `actingAs` kullanımı (T10); `Http::preventStrayRequests()`.
- Regresyon: R1 ve R2 (mutasyon), R10 (`preventStrayRequests`, `SENTRY_LARAVEL_DSN`), R11, R12.

### D1 — Frontend mimarisi ve sözleşme · `FE-01…FE-49` → `findings/04-frontend-d1.md`

**Kopya:** `frontend` (yalnızca okuma; sunucu D2'nin), `backend` (okuma).
**Önce oku:** `frontend/CLAUDE.md` · `frontend/docs/` · `davetkart-docs/notes/02-FRONTEND-BACKEND-TEMAS-NOKTALARI.md`, `03-FRONTEND-YAPILACAKLAR.md` · `claude/GOZDEN-GECIRME-2026-10-09-FRONTEND.md` · `backend/docs/rehber/FIYAT-VE-INDIRIM-YONETIMI.md`.

- Mimari: klasör yapısı, bileşen sorumlulukları, state yönetimi, servis katmanı, tip güvenliği (`any`, `as` zorlamaları, `unknown` daraltması), hata/yükleme durumları, i18n (10 dil, eksik anahtarlar: anahtar kümelerini betikle karşılaştır).
- Backend sözleşmesiyle uyum: frontend'in çağırdığı her uç ↔ `routes/api.php`; tipler ↔ Resource alanları; frontend'de kalmış **sabit fiyat** var mı (karar: fiyatlar yalnızca backend'den). **Sözleşme tablosu** (rapor §9): uç, frontend çağrısı, durum.
- React 19 / router / Zustand / i18next / Vite API'lerinin güncel dokümana göre doğruluğu (Context7 yok → resmî doküman).
- Faz 15–17 şablonları (`src/components/templates`, `src/data.ts`): kayıt düzeni, lazy yükleme, `minimumTier` ↔ backend `config/davetkart.php` `preset_tiers` eşleşmesi.
- Matt Pocock skill'lerinden uygun olanları kullan (`mattpocock-skills:codebase-design`, `…:diagnosing-bugs`, `…:tdd`); kullandıklarını listele, olmayan skill adı uydurma.
- Regresyon: R3 (sözleşme), R8, R16 (frontend).

### D2 — Uçtan uca tarayıcı testi · `FE-50…FE-99` → `findings/04-frontend-d2.md`

**Kopya:** `backend-e2e` (`php artisan serve --port=8000`), `frontend` (`npm run dev`, port 3000).
**Önce oku:** `docs/rehber/fazlar/FAZ-11…14-ELLE-DOGRULAMA.md` · `docs/rehber/PROJE-KOMUTLARI.md` (hediye kodu, iade komutları).
Playwright yalnızca `http://localhost:3000` üzerinde. Görünümler: masaüstü 1440px, mobil 390px.

1. Kayıt → giriş → çıkış → hatalı parola → hız sınırı mesajı
2. Davetiye oluştur → editör → otomatik kaydetme → önizleme
3. Plan seç → ödeme ekranı (sahte sürücü / hediye kodu) → dönüş sayfası → yayınla
4. Yayındaki davetiyeyi düzenleyip üst plan modülü açmaya çalış (K-1 regresyonu)
5. Misafir sayfası → LCV gönder → fotoğraf yükle → sahibin panelinde görünmesi
6. Hesap ayarları (Faz 14): plan hakları, hak iptali, e-posta değişikliği
7. Yeni davetiye tasarımları (Faz 15–17): animasyonların mobilde akıcılığı, düşük güçlü cihaz için `prefers-reduced-motion`
8. Dil değiştirme, 404 sayfası, oturumu düşmüş kullanıcı (401) davranışı

- Her yolculukta: ekran görüntüsü (`evidence/screenshots/J<N>-<adım>-<1440|390>.png`), konsol hataları, başarısız ağ istekleri, beklenmeyen 4xx/5xx.
- Erişilebilirlik (axe-core sayfaya enjekte edilebiliyorsa; CDN yerine `node_modules` ya da yerel dosya): kontrast, etiketler, klavye ile gezinme, odak yönetimi.
- Performans: Lighthouse benzeri ölçüm yapılabiliyorsa LCP/CLS/TBT; yoksa build boyutu ve ağ şelalesi üzerinden yorum.
- Regresyon: R1 (arayüz), R3 (yolculuk 3), R15 (yolculuk 6).

### E — Yayına hazırlık ve işletim · `OPS-01…` → `findings/05-operations.md`  *(A–D bittikten sonra)*

**Kopya:** `backend` (okuma). **Önce oku:** `davetkart-docs/operations/deployment/YAYIN-PLANI.md`, `YAYIN-DEVIR.md` · `davetkart-docs/prompts/PROMPT-YAYIN.md` · `backend/docs/10-URETIM-ENV-SABLONU.md` · `backend/deploy/` · `docs/rehber/deploy/` · diğer dört dilimin bulgu dosyaları.

- `YAYIN-PLANI.md` / `YAYIN-DEVIR.md`'deki Y0–Y12 adımlarının koddaki karşılıkları: S3 diski paketi (`league/flysystem-aws-s3-v3`), `deploy/` klasörü, Nginx/systemd dosyaları, `.env` şablonunun eksiksizliği, `APP_DEBUG`, log/Sentry yapılandırması, kuyruk ve zamanlayıcı.
- Yedekleme ve geri yükleme planı, izleme (uptime, hata), alarm.
- Gözlemlenebilirlik: yapılandırılmış log, korelasyon kimliği, kişisel verinin loglanmaması.
- Ölçeklenebilirlik: tek sunucu (Lightsail 2 GB) varsayımında darboğazlar; ileride yatay ölçek için engel olan tasarımlar (yerel dosya, `file` cache, oturum).
- Dal durumu: denetlenen dal, `main` ve `release-v1.0` arasındaki fark; yayına hangi commit'in çıkacağı.
- Regresyon: R5 (Nginx / vekil tarafı).

### R — Rapor *(ana oturum)*

- [ ] `02-security-b1.md` + `02-security-b2.md` → `findings/02-security.md`; `04-frontend-d1.md` + `04-frontend-d2.md` → `findings/04-frontend-e2e.md` (parça dosyaları birleştirildikten sonra kaldırılır).
- [ ] Tekrarları ayıkla; `REPORT.md`'yi yaz (kapak, yönetici özeti, puan kartı, tam / eksik, bulgular, regresyon, sözleşme ve bağımlılık tabloları, yol haritası, kararlar, dersler, ekler).
- [ ] `audits/README.md` ve `CHANGELOG.md`'ye birer satır; `git status --short` başlangıçla karşılaştır.

## 5. Bulgu biçimi (her dilimde aynı, makinece ayrıştırılır)

```
### <ÖNEK>-<NN> <Başlık>        ← ör. SEC-03 Sanctum token'ları hiç sona ermiyor
- Seviye: 🔴 Kritik · 🟠 Yüksek · 🟡 Orta · 🟢 Düşük · 💡 Öneri      (yalnızca BİRİ yazılır)
- Kanıt türü: KOŞTURULDU | KOD OKUMASI | VARSAYIM
- Nerede: dosya:satır (birden fazlaysa liste)
- Senaryo: adım adım nasıl ortaya çıkıyor
- Kanıt: komut + çıktının ilgili satırları / ekran görüntüsü yolu
- Etki: kullanıcıya, paraya, veriye, itibara etkisi
- Neden önemli (öğretici not): hangi ilke/desen/standart (ör. ASVS V4.2.1, OWASP API1)
- Öneri: en ucuzdan en sağlama, kod parçasıyla (uygulanmadan)
- Test önerisi: test adı + neyi doğrulayacağı + öldürmesi gereken mutant
- Efor: S (≤1 saat) · M (yarım gün) · L (1–2 gün) · XL
- İlgili: önceki rapor maddesi / K numarası
```

Seviye ölçütü: 🔴 = para kaybı, yetkisiz erişim, kişisel veri sızıntısı ya da veri kaybı, normal arayüzle
tetiklenebilir. 🟠 = aynı etkiler ama özel koşul gerektirir, ya da yayını engelleyen eksik. 🟡 =
doğruluk/dayanıklılık sorunu. 🟢 = temizlik. 💡 = iyileştirme fikri.

Kurallar: başlık satırı tam olarak `### <ID> <Başlık>` · `- Seviye:` satırında tek seviye · bulgu olmayan
iyi tasarımlar "Neler iyi" bölümüne (kanıtıyla) · tahmin `VARSAYIM` diye işaretlenir · koşmadıysa "koşmadı".

## 6. Bulgu dosyası iskeleti ve kanıt adları

```
# <Dilim adı> — AUD-2026-11-12
> Ajan: … · Kopya: … · Commit: … · Tarih: …
## Özet                 ← 5–10 satır + seviye sayıları
## Özet tablosu         ← | ID | Seviye | Kanıt türü | Başlık | Nerede | Efor | Tek satır öneri |
## Neler iyi            ← korunması gereken tasarımlar, kanıtıyla
## Bulgular             ← §5 biçiminde, ID sırasıyla
## Tablolar             ← dilime özgü (ASVS, rota sahipliği, mutasyon, sözleşme, bağımlılık, yolculuk)
## Regresyon            ← §3'teki satırların
## Kullanılan araçlar ve skill'ler / kullanılamayanlar
## Koşturulan komutlar  ← kanıt dosyalarının listesi
## İsmail'e sorular
```

| Tür | Yol |
|---|---|
| Komut çıktısı | `evidence/commands/<ID ya da dilim>-<kısa-ad>.txt` (ilk satırlarda komutun kendisi) |
| Betik | `evidence/scripts/<dilim>-<kısa-ad>.<uzantı>` |
| Ekran görüntüsü | `evidence/screenshots/J<N>-<adım>-<1440\|390>.png` |
| Mutasyon | `evidence/mutation/M<NN>-<ad>.txt` |

## 7. Bu denetimin kendi riskleri (inceleme odağı)

1. **Yanlış ağacı denetlemek:** yerel çalışma ağacı 60 commit geride. Her kanıt anlık görüntüden gelmeli.
2. **Boş yeşil mutasyon:** filtre 0 test koşarsa "mutant öldü" sanılır. Koşan test sayısı kaydedilir.
3. **Ortam farkını hata sanmak:** anlık görüntüde satır sonları, `.env.example` varsayılanları, `QUEUE_CONNECTION=sync` gerçek dağıtımdan farklı. Kırmızı sonuçlar sınıflandırılır.
4. **Okunan kodu koşmuş gibi sunmak (B7):** Shopier, S3, SES, Gemini yolları koşturulamaz; hepsi `KOD OKUMASI`.
5. **Dilimler arası tekrar ve çelişki:** aynı kök neden iki dilimde farklı seviyeyle çıkabilir; raporda tek bulguya indirilir.

---

## Ek A — Çalışma kuralları (şartname §0, aynen)

0. 🔴 **Önce `davetkart-docs/CLAUDE.md`'yi oku ve uy.** Adlandırma, klasör yerleşimi, karar kaydı, yazım ve commit biçimi oradaki kurallara göre yapılır. Bu prompt ile çelişirse **daha kısıtlayıcı olan** uygulanır (bu denetimde §0'daki salt okunurluk ve git yasağı her zaman geçerlidir). Çelişkiyi raporun eklerine yaz.
1. 🔴 **Salt okunur denetim.** `davetkart-backend-php-laravel/`, `davetkart-frontent/` ve `davetkart-docs/` (eski adıyla `claude/`) altındaki **hiçbir mevcut dosyayı değiştirme**. Yazabileceğin yerler: `davetkart-docs/audits/2026-11-12-full-system-audit/` (yeni klasör, §0-8'deki yapıyla) ve `CLAUDE.md` gereği bu denetimin kaydı için **tek satırlık** ekler: `audits/README.md` (listeye bu denetim) ve `CHANGELOG.md`. Başka hiçbir doküman değişmez; eskimiş bulduğun dokümanı rapora yaz. Düzeltme önerilerini rapora yaz, koda uygulama.
2. 🔴 **Git yazma işlemi yok:** `add`, `commit`, `push`, `stash`, `reset`, `checkout`, `switch`, `branch -d`, `clean` çalıştırma. Okuma serbest: `status`, `log`, `diff`, `show`, `branch -a`, `grep`.
3. 🔴 **B7:** çıktısını kendin görmediğin hiçbir şeye "doğrulandı" yazma. Her bulguda kanıt türünü belirt: `KOŞTURULDU` (komut/test/tarayıcı çıktısı var) · `KOD OKUMASI` (yalnızca okuyarak) · `VARSAYIM`. Tahmini gerçek gibi sunma.
4. 🔴 **Canlı sisteme dokunma.** `davetkart.com`, `media.davetkart.com`, AWS, SES, Shopier, Gemini: hiçbirine istek atma, form doldurma, yük testi yapma. Playwright yalnızca `localhost` / `*.test` üzerinde çalışır. Gerçek sırlar (`.env`) okunabilir ama **değerleri rapora, loga ya da sohbete asla yazılmaz**; yalnızca "dolu/boş/eksik" durumu yazılır.
5. Kanıt üretmek için deneme betiği, `curl` komutu, Playwright betiği ya da geçici PHPUnit testi gerekiyorsa bunları `davetkart-docs/audits/2026-11-12-full-system-audit/evidence/` altına yaz ve oradan koştur. Geçici testi depoya kopyalaman gerekirse koştur, çıktıyı kaydet, dosyayı **hemen geri taşı** ve raporda belirt; `git status` denetim öncesi hâline dönmüş olmalı.
6. Türkçe yaz. Ben bilgisayar mühendisliği öğrencisiyim ve mimariyi öğrenmek istiyorum: her önemli bulguda **neden** sorun olduğunu, hangi ilkeyi/deseni ihlal ettiğini ve doğru deseni kısaca anlat.
7. Bu oturumdaki her alt ajan da **Fable 5.2** ile çalışır ve bu kuralların aynısına uyar. Alt ajana verdiğin her görev tanımına §0'ı aynen ekle.
8. **Denetim klasörünün yapısı:** `README.md`, `REPORT.md`, `PLAN.md`, `findings/01…05-*.md`, `evidence/{commands,scripts,screenshots,mutation}/`. Bulgu kimlikleri dilim önekiyle: `ARC-01` (mimari), `SEC-01` (güvenlik), `TST-01` (test), `FE-01` (frontend/E2E), `OPS-01` (işletim).

**Anlık görüntü kararının (İsmail, 13 Kasım 2026) kurallara etkisi:** madde 5'teki "geçici testi depoya
kopyala, hemen geri taşı" yolu **kullanılmaz**; geçici test ve mutasyon ajanın kendi kopyasında yapılır,
gerçek depolara hiçbir şey kopyalanmaz. Madde 1 ve 2 gerçek depolar için aynen geçerlidir.
