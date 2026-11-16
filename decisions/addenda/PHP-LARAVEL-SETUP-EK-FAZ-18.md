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
