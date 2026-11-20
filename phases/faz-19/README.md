# Faz 19 — denetimin orta öncelikli bulguları (`AUD-2026-11-12`)

29 orta (🟡) bulgudan `TST-01` Faz 18.1'de kapandı (K150); kalan **28** bulgu burada. Her bulgu ayrı bir dalda, ayrı bir prompt'la ve tek oturumda kapanır; commit'leri İsmail atar.

- **Kaynak:** [`audits/2026-11-12-full-system-audit/REPORT.md`](../../audits/2026-11-12-full-system-audit/REPORT.md) §5.1 ve [`findings/`](../../audits/2026-11-12-full-system-audit/findings/)
- **Entegrasyon dalı (backend ve frontend):** `faz-19-audit-fixes` — `faz-18-audit-fixes`'in ucundan (19.1 §A). Düzeltme dalları bundan açılır ve buna birleşir.
- **Düzeltme dalları:** kod `fix/<YYYY-MM-DD>-<bulgu-id>-<kısa-ad>`; yalnızca docs'a dokunan bulgular (`ARC-01`, `OPS-05`) `docs/<YYYY-MM-DD>-<bulgu-id>-<kısa-ad>` (`CLAUDE.md` §4)
- **Docs dalı:** `docs/2026-11-20-faz-19-audit-fixes` (Faz 18 docs dalının ucundan)
- **Resmî faz kaydı:** backend `docs/rehber/fazlar/FAZ-19.md`. Backend'e dokunmayan bulgular bölümlerini önce `phases/faz-19/FAZ-19-<ID>-KAYIT.md`'ye yazar; sonraki backend bulgusu taşır.
- **Sürümler:** 19.1 (`SEC-07`) sonunda **`v1.1.0`** (= Faz 18 + `SEC-07`; Faz 18'in bekleyen etiketi). 19.28 sonunda **`v1.2.0`** (Faz 19 kapanışı).
- **§A:** "Karar" sütununda **§A** yazan prompt'larda önce senin cevapların gerekir; boş bırakılan satır için ajan prompt'taki varsayılanı uygular ve K kaydında işaretler.

## Sıra ve gerekçe

1. **Yayın engeli önce:** `SEC-07` (`v1.1.0` bunu bekliyor).
2. **Kayıt ve işletim:** `ARC-01` (K numaraları sağlam olsun ki sonraki 27 prompt güvenle K versin) → `ARC-02` → `ARC-05` → `ARC-04` → `OPS-04` → `OPS-03` → `OPS-05`.
3. **Güvenlik:** `SEC-05` → `SEC-06` → `TST-02` (kilit testleri; sonraki bulgular yeni kilitlerini bu desenle sınar) → `FE-51` (ürün kararı) → `SEC-08` (o karara göre kota) → `SEC-09` → `SEC-10` → `SEC-13` → `SEC-12` → `SEC-11` (gizlilik metni; önceki dört bulgunun sonucunu anlatır).
4. **Frontend:** `FE-52` → `FE-01` → `FE-02` → `TST-04` (E2E; sonraki frontend değişiklikleri onunla korunur) → `FE-04` → `FE-10` → `FE-53` (paket ve font işinden sonra ölçüm) → `FE-50` → `FE-54`.
5. **En son:** `ARC-03` (çok dosyaya dokunur; çakışma riski en az olsun diye) + Faz 19 kapanışı.

| Sıra | Bulgu | Konu | Efor | Karar | Prompt | Depolar | Dal | K | Durum |
|---|---|---|---|---|---|---|---|---|---|
| 19.1 | `SEC-07` | Composer bağımlılıklarında bilinen açıklar; `composer audit` kırmızı | S | **§A** | [`PROMPT-FAZ-19-01-SEC-07.md`](../../prompts/PROMPT-FAZ-19-01-SEC-07.md) | backend · docs | `fix/<tarih>-sec-07-composer-audit` | — | bekliyor |
| 19.2 | `ARC-01` | Karar indeksi K128–K145'i bilmiyor | S | — | [`PROMPT-FAZ-19-02-ARC-01.md`](../../prompts/PROMPT-FAZ-19-02-ARC-01.md) | docs | `docs/<tarih>-arc-01-decision-index` | — | bekliyor |
| 19.3 | `ARC-02` | Faz 16 ve 17'nin faz kaydı yok | S | **§A** | [`PROMPT-FAZ-19-03-ARC-02.md`](../../prompts/PROMPT-FAZ-19-03-ARC-02.md) | backend (yalnızca `docs/`) · docs | `fix/<tarih>-arc-02-phase-16-17-records` | — | bekliyor |
| 19.4 | `ARC-05` | Eski `claude/…` yolları; backend'in `claude/` klasörü ikinci ev | M | **§A** | [`PROMPT-FAZ-19-04-ARC-05.md`](../../prompts/PROMPT-FAZ-19-04-ARC-05.md) | backend (`claude/`, `docs/`) · docs | `fix/<tarih>-arc-05-claude-folder` | — | bekliyor |
| 19.5 | `ARC-04` | K55 "yerel disk kalır" geçerli görünüyor ama yayın planı S3 kuruyor | S | **§A** | [`PROMPT-FAZ-19-05-ARC-04.md`](../../prompts/PROMPT-FAZ-19-05-ARC-04.md) | backend · docs | `fix/<tarih>-arc-04-media-disk` | — | bekliyor |
| 19.6 | `OPS-04` | Üretim `.env` şablonu sunucudaki gerçek dosyadan sapmış | S | **§A** | [`PROMPT-FAZ-19-06-OPS-04.md`](../../prompts/PROMPT-FAZ-19-06-OPS-04.md) | backend · docs | `fix/<tarih>-ops-04-env-template` | — | bekliyor |
| 19.7 | `OPS-03` | İzleme ve alarm yok; sağlık ucu yalnızca PHP'nin ayakta olduğunu söylüyor | S | **§A** | [`PROMPT-FAZ-19-07-OPS-03.md`](../../prompts/PROMPT-FAZ-19-07-OPS-03.md) | backend · docs | `fix/<tarih>-ops-03-health-monitoring` | — | bekliyor |
| 19.8 | `OPS-05` | Tek hata noktaları: alan adı yenilemesi, posta ve kredi bitiş tarihleri | S | **§A** | [`PROMPT-FAZ-19-08-OPS-05.md`](../../prompts/PROMPT-FAZ-19-08-OPS-05.md) | docs | `docs/<tarih>-ops-05-expiry-calendar` | — | bekliyor |
| 19.9 | `SEC-05` | Zayıf parolalar kabul ediliyor | S | **§A** | [`PROMPT-FAZ-19-09-SEC-05.md`](../../prompts/PROMPT-FAZ-19-09-SEC-05.md) | backend · frontend · docs | `fix/<tarih>-sec-05-password-policy` | — | bekliyor |
| 19.10 | `SEC-06` | Genel hız sınırı IP anahtarlı: misafir trafiği davetiye sahibini de kilitliyor | M | **§A** | [`PROMPT-FAZ-19-10-SEC-06.md`](../../prompts/PROMPT-FAZ-19-10-SEC-06.md) | backend · docs | `fix/<tarih>-sec-06-rate-limit-keys` | — | bekliyor |
| 19.11 | `TST-02` | Kilitlerin hiçbiri testle korunmuyor | M | — | [`PROMPT-FAZ-19-11-TST-02.md`](../../prompts/PROMPT-FAZ-19-11-TST-02.md) | backend · docs | `fix/<tarih>-tst-02-lock-tests` | — | bekliyor |
| 19.12 | `FE-51` | Misafir fotoğraf/video yüklemesine arayüzden ulaşılamıyor | M | **§A** | [`PROMPT-FAZ-19-12-FE-51.md`](../../prompts/PROMPT-FAZ-19-12-FE-51.md) | frontend · backend · docs | `fix/<tarih>-fe-51-guest-media-upload` | — | bekliyor |
| 19.13 | `SEC-08` | Kimliksiz misafir davetiye başına 5 GB yükleyebilir; yetim dosya kotayı 24 saat tutar | M | **§A** | [`PROMPT-FAZ-19-13-SEC-08.md`](../../prompts/PROMPT-FAZ-19-13-SEC-08.md) | backend · docs | `fix/<tarih>-sec-08-guest-upload-budget` | — | bekliyor |
| 19.14 | `SEC-09` | E-posta doğrulaması yok | L | **§A** | [`PROMPT-FAZ-19-14-SEC-09.md`](../../prompts/PROMPT-FAZ-19-14-SEC-09.md) | backend · frontend · docs | `fix/<tarih>-sec-09-email-verification` | — | bekliyor |
| 19.15 | `SEC-10` | Shopier'e uydurma TCKN ve telefon gönderiliyor | S | **§A** | [`PROMPT-FAZ-19-15-SEC-10.md`](../../prompts/PROMPT-FAZ-19-15-SEC-10.md) | backend · docs (frontend yalnızca §A-1 "zorunlu" ise) | `fix/<tarih>-sec-10-shopier-buyer-fields` | — | bekliyor |
| 19.16 | `SEC-13` | `data:purge` tarihi olmayan davetiyelerin misafir verisini hiç silmiyor | S | **§A** | [`PROMPT-FAZ-19-16-SEC-13.md`](../../prompts/PROMPT-FAZ-19-16-SEC-13.md) | backend · docs | `fix/<tarih>-sec-13-purge-undated` | — | bekliyor |
| 19.17 | `SEC-12` | Her sayfa Google Fonts'u Google'dan yüklüyor | S | **§A** | [`PROMPT-FAZ-19-17-SEC-12.md`](../../prompts/PROMPT-FAZ-19-17-SEC-12.md) | frontend · backend (`deploy/nginx` CSP) · docs | `fix/<tarih>-sec-12-self-hosted-fonts` | — | bekliyor |
| 19.18 | `SEC-11` | Gizlilik metni "hemen silinir" diyor; yedekler tutuyor; üçüncü taraflar adıyla yok | S | **§A** | [`PROMPT-FAZ-19-18-SEC-11.md`](../../prompts/PROMPT-FAZ-19-18-SEC-11.md) | frontend · docs | `fix/<tarih>-sec-11-privacy-text` | — | bekliyor |
| 19.19 | `FE-52` | Fiyat sayfası SSS'si backend'de olmayan "yayın süresi" ve ücretli uzatmayı anlatıyor | S | **§A** | [`PROMPT-FAZ-19-19-FE-52.md`](../../prompts/PROMPT-FAZ-19-19-FE-52.md) | frontend · docs | `fix/<tarih>-fe-52-pricing-faq` | — | bekliyor |
| 19.20 | `FE-01` | Dil seçici on dil sunuyor, arayüzün büyük kısmı yalnızca Türkçe | S (sınırlama) / L (tam çeviri) | **§A** | [`PROMPT-FAZ-19-20-FE-01.md`](../../prompts/PROMPT-FAZ-19-20-FE-01.md) | frontend · docs | `fix/<tarih>-fe-01-language-scope` | — | bekliyor |
| 19.21 | `FE-02` | Hata sınırı yok: render hatası ve yüklenemeyen chunk ham hata ekranı veriyor | S | — | [`PROMPT-FAZ-19-21-FE-02.md`](../../prompts/PROMPT-FAZ-19-21-FE-02.md) | frontend · docs | `fix/<tarih>-fe-02-error-boundary` | — | bekliyor |
| 19.22 | `TST-04` | Gerçek frontend + gerçek backend'i koşturan otomatik test yok | L | **§A** | [`PROMPT-FAZ-19-22-TST-04.md`](../../prompts/PROMPT-FAZ-19-22-TST-04.md) | frontend (gerekirse backend: test verisi komutu) · docs | `fix/<tarih>-tst-04-e2e` | — | bekliyor |
| 19.23 | `FE-04` | Davetiye bağlantısının paylaşım önizlemesi yok (Open Graph) | M | **§A** | [`PROMPT-FAZ-19-23-FE-04.md`](../../prompts/PROMPT-FAZ-19-23-FE-04.md) | frontend · backend (Blade + `deploy/nginx`) · docs | `fix/<tarih>-fe-04-share-preview` | — | bekliyor |
| 19.24 | `FE-10` | Ana giriş paketi 1,64 MB: 299 şablon her sayfaya, misafir sayfasına bile yükleniyor | M | **§A** | [`PROMPT-FAZ-19-24-FE-10.md`](../../prompts/PROMPT-FAZ-19-24-FE-10.md) | frontend · docs | `fix/<tarih>-fe-10-bundle-split` | — | bekliyor |
| 19.25 | `FE-53` | Kısıtlı mobil koşulda LCP 3,9–5,7 sn; giriş ve fiyat sayfalarında CLS 0,33–0,63 | M | **§A** | [`PROMPT-FAZ-19-25-FE-53.md`](../../prompts/PROMPT-FAZ-19-25-FE-53.md) | frontend · docs | `fix/<tarih>-fe-53-mobile-vitals` | — | bekliyor |
| 19.26 | `FE-50` | Sihirbaz her ziyarette sunucuda boş taslak açıyor; yenilemede editör kayboluyor | M | **§A** | [`PROMPT-FAZ-19-26-FE-50.md`](../../prompts/PROMPT-FAZ-19-26-FE-50.md) | frontend · backend · docs | `fix/<tarih>-fe-50-draft-lifecycle` | — | bekliyor |
| 19.27 | `FE-54` | Hata ve başarı mesajları ekran okuyucuya duyurulmuyor; kontrast yetersiz | S | **§A** | [`PROMPT-FAZ-19-27-FE-54.md`](../../prompts/PROMPT-FAZ-19-27-FE-54.md) | frontend · docs | `fix/<tarih>-fe-54-accessibility` | — | bekliyor |
| 19.28 | `ARC-03` | K18 dosyaların %92'sinde çiğneniyor; 79 dosyanın kılavuzu yok | L | **§A** | [`PROMPT-FAZ-19-28-ARC-03.md`](../../prompts/PROMPT-FAZ-19-28-ARC-03.md) | backend · docs (frontend için yalnızca öneri) | `fix/<tarih>-arc-03-k18-ratchet` | — | bekliyor |

Durum değerleri: `bekliyor` → `kod ✅ · commit bekliyor` → `birleşti` (İsmail işaretler).
