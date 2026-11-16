# Karar İndeksi (K numaraları)

> **Tek tablo.** Kararın kendisi ve gerekçesi kaynak dosyada; burada tek satırlık başlık.
> Üretim: `python -I _restructure/build_decision_index.py` (2026-11-12). Yeni karar eklerken
> bu dosyaya da elle satır eklenir (bkz. `../CLAUDE.md` §5).
> ⚠️ işaretli satırlar açık soru ya da çelişki taşır; **numaralar değiştirilmedi.**

> ⚠️ **K128–K145 bu tabloda yok** (`ARC-01`, ayrı bir iş): backend `docs/rehber/fazlar/FAZ-13.md`
> ve `FAZ-14.md`'de kullanılmışlar, satırları buraya işlenmedi. Bu numaralar **dolu**; yeni
> karar almaz. Faz 18 kararları bu yüzden K146'dan başlar (2026-11-16).

**Sıradaki boş numara: K158**

| K# | Başlık | Faz | Durum | Kaynak |
|---|---|---|---|---|
| **K1** | PHP 8.3+ / Laravel 13 | Faz 0 | geçerli · PHP sürümü K87 ile `^8.5` | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K2** | Modüler Monolit (mikroservis değil) | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K3** | Katmanlı + Action tabanlı uygulama katmanı | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K4** | Repository Pattern KULLANILMAYACAK | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K5** | Laravel Sanctum (JWT değil) | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K6** | Hibrit veri modeli | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K7** | Canlı LCV için Polling + ETag | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K8** | `PaymentGateway` arayüzü + `FakeGateway` | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K9** | Üretimde MySQL 8 | Faz 0 | geçersiz kılındı → K9' | [`context/PHP-LARAVEL-SETUP.md` §8](../context/PHP-LARAVEL-SETUP.md#8-geçersiz-kılınan-kararlar-️) |
| **K9'** | Üretimde PostgreSQL 18 | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K10** | API versiyonu URL'de değil, namespace'te | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K11** | Başarı zarfı ikili kural | Faz 0 | geçerli · ana dosyada durum hâlâ "📋 Faz 2'de uygulanacak" | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K12** | Auth'suz rotalar `/api/public/` öneki altında | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K13** | Public ID olarak ULID | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K14** | IP adresleri hash'lenerek saklanır | Faz 0 | geçerli · K77 ile `hash_hmac`'e birleşti | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K15** | Tam Clean Architecture / DDD YAPILMAYACAK | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K16** | Klasörler `php artisan make:*` ile üretilir | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K17** | Özellik-özellik inşa (9 faz) | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K18** | Kodda kısa yorum, detay `docs/rehber/` altında | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K19** | Geliştirme ve testte de PostgreSQL 18 | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K20** | 🔴 Hata sözleşmesi — API metin değil kod döner | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K21** | Backend tek dil konuşur (`APP_LOCALE=en`) | Faz 0 | geçerli · K96 istisnası (mailler Türkçe) | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K22** | PHPStan seviyesi kademeli: 5 → Faz 2'de 6 → Faz 5'te 8 | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K23** | Tarihler `CarbonImmutable` | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K24** | Test framework'ü PHPUnit (Pest değil) | Faz 0 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K25** | JSON zorlaması middleware ile, `shouldRenderJsonWhen` ile değil | Faz 1 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K26** | Hata zarfı mantığı ayrı sınıfta (`ApiExceptionRenderer`) | Faz 1 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K27** | `PAYMENT_PROVIDER_ERROR` → 502, `PROVIDER_UNAVAILABLE` → 503 | Faz 1 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K28** | `RSVP_QUOTA_EXCEEDED` → 403 (429 değil) | Faz 1 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K29** | RFC 9457 (Problem Details) kullanılmaz | Faz 1 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K30** | Rota dosyasında closure yok, controller referansı | Faz 1 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K31** | Katalog senkronizasyonu tek yönlü üretim + `--check` | Faz 1 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K32** | Parola hash'i Argon2id (bcrypt değil) | Faz 1 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K33** | Katalog `contracts/error-codes.json`, repoya işlenir | Faz 1 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K34** | `errors:export --check` `composer check` zincirinde, testlerden önce | Faz 1 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K35** | `users` → `first_name` + `last_name`; API'de de ayrı döner | Faz 2 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K36** | Auth uçlarına hız sınırı — Faz 5'ten öne çekildi | Faz 2 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K37** | `/api/invitations` REST koleksiyonu (upsert değil) | Faz 3 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K38** | `InvitationStatus` = `saved \| published` | Faz 3 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K39** | Durum kolonu `VARCHAR + CHECK`, native `ENUM` değil | Faz 3 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K40** | `invitations.id` = ULID birincil anahtar, ayrı slug yok | Faz 3 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K41** | `phone_background` kolon değil, türetilir | Faz 3 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K42** | Yayın hakkı iki kaynaktan, tek arayüzden sorulur | Faz 3 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K43** | Plan kotası yayınlananı sayar, taslağı değil | Faz 3 | ⚠️ Faz 7'de uygulanmadı (açık ticari karar; bkz. K99) | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K44** | Kimliği backend üretir | Faz 3 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K45** | Cache Action'ın dışında, Resource çıktısı olan diziyi saklar | Faz 4 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K46** | ETag ayrı middleware, controller içi değil | Faz 4 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K47** | Faz 4 salt okuma kalır; yayın ucu Faz 7'de | Faz 4 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K48** | Olay `InvitationChanged`, modelden yapısal fırlar | Faz 4 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K49** | `RsvpStatus` = `attending \| pending \| declined`; `label()` metodu yok | Faz 5 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md` §A |
| **K50** | LCV kotası `attending + pending` toplamını sayar; `declined` saymaz | Faz 5 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md` §A |
| **K51** | Kota limiti `RsvpQuotaResolver` arayüzü arkasından okunur | Faz 5 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md` §A |
| **K52** | `rsvps.id` = ULID | Faz 5 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md` §A |
| **K53** | `Jobs/SendRsvpNotification` Faz 5'te yazılmadı | Faz 5 | geçersiz kılındı → K62 | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md` §A |
| **K54** | `media.disk` kolonda saklanır, `config()`'ten okunmaz | Faz 6 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` §A |
| **K55** | Depolama yerel `public` diski kalır; S3/R2 ertelendi | Faz 6 | geçerli · ⚠️ yayın planı S3 diski kuruyor (`operations/deployment/YAYIN-DEVIR.md` Y0); yerine geçen K yok | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` §A |
| **K56** | `media.id` = ULID | Faz 6 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` §A |
| **K57** | Medya polimorfik değil; `invitation_id` + `kind` ile modellendi | Faz 6 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` §A |
| **K58** | LCV medyası kimlikle iliştirilir, URL ile değil | Faz 6 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` §A |
| **K59** | Geçersiz medya kimliği sessizce düşürülür, reddedilmez | Faz 6 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` §A |
| **K60** | `rsvps` medya FK'leri `nullOnDelete` | Faz 6 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` §A |
| **K61** | Misafirin medya ucu ayrı bir throttle kovası alır (`throttle:media`) | Faz 6 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` §A |
| **K62** | `Jobs/SendRsvpNotification` Faz 8'e kaldı | Faz 6 | geçersiz kılındı → K79 | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` §A |
| **K63** | `invitations.timezone` Faz 7'ye ertelendi | Faz 6 | geçersiz kılındı → K71 | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` §A |
| **K64** | Checkout iki uç: `/invitations/{id}/checkout` (tekil) · `/payments/checkout` (paket) | Faz 7 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K65** | Webhook ucu `/api/public/` altında | Faz 7 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K66** | `public_slug` üretilmiyor | Faz 7 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K67** | Ödeme yayınlamaz; yayın ayrı bir kullanıcı eylemidir | Faz 7 | geçerli · ⚠️ frontend 11.6 ile çelişki sorusu açık (EK-FAZ-12 §F-7) | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K68** | "Zaten yayında" → 409, sessiz başarı değil | Faz 7 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K69** | İmza hatası → 404 (401/403/400 değil) | Faz 7 | geçerli · K122 tarayıcı callback'i için bilinçli sapma | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K70** | Sürücü seçimi çözüm anında, sessiz varsayılan yok | Faz 7 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K71** | `invitations.timezone` = duvar saati + IANA kimliği, `timestamptz` değil | Faz 7 | geçerli | [`context/PHP-LARAVEL-SETUP.md` §7](../context/PHP-LARAVEL-SETUP.md#7-karar-kaydı) |
| **K72** | Asistan ucu auth'lu | Faz 8 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md` §A |
| **K73** | Kota veritabanında sayılır (`assistant_usages`); `throttle:assistant` ayrıca durur | Faz 8 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md` §A |
| **K74** | Kota aşımı 429 + yeni kod `ASSISTANT_QUOTA_EXCEEDED` | Faz 8 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md` §A |
| **K75** | AI sağlayıcı hatalarının tamamı → `PROVIDER_UNAVAILABLE` (503) | Faz 8 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md` §A |
| **K76** | İletişim ucu `/api/public/contact` (`/api/contact` değil) | Faz 8 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md` §A |
| **K77** | `ip_hash` `hash_hmac`'e birleşti; ortak yer `app/Support/IpHasher` | Faz 8 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md` §A |
| **K78** | `ai.request.timeout_seconds` 10 → 6; retry yalnızca bağlantı hatasında | Faz 8 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md` §A |
| **K79** | `Jobs/SendRsvpNotification` yazılmadı | Faz 8 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md` §A |
| **K80** | Altyapı en düşük ortak paydaya yazılır; Redis, S3 ve süpervizör birer yükseltmedir | Faz 9 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-9.md` §A |
| **K81** | `orders.scope` — kapsam satırda saklanır, okumada türetilmez | Faz 9 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-9.md` §A |
| **K82** | Yayınlanmış davetiye silinebilir; ödenen hak 3 gün içinde serbest kalır | Faz 9 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-9.md` §A |
| **K83** | Serbest hak, yayın anında yeten en düşük siparişten harcanır | Faz 9 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-9.md` §A |
| **K84** | Bakım komutları `--dry-run` taşır ve zamanlayıcıdan önce elle koşulur | Faz 9 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-9.md` §A |
| **K85** | Güvenlik başlıkları middleware'de, nginx'te değil | Faz 9 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-9.md` §A |
| **K86** | `config/cors.php` yayınlandı ve daraltıldı; `exposed_headers: ['ETag']` | Faz 9 | geçerli | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-9.md` §A |
| **K87** | PHP ^8.5 kalır | Faz 10 (25 Eyl) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K88** | Yayındaki davetiyede modül açma kayıt anında plan kontrolünden geçer → 402 `PAYWALL_TIER_INSUFFICIENT` | Faz 10 (25 Eyl) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K89** | `OrderStatus::Expired` eklenir. `orders:expire` onu yazar, `Expired → Paid` geçişine izin verilir. `Failed` f… | Faz 10 (25 Eyl) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K90** | Sanctum token ömrü 30 gün, mutlak (oluşturmadan itibaren) | Faz 10 (25 Eyl) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K91** | Bozuk girdi (yarım JSON, NUL) → 400, alan başına değil `api` grubunda tek middleware | Faz 10 (25 Eyl) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K92** | Sayı alanları `integer:strict` (`true` ve `"3"` reddedilir) | Faz 10 (25 Eyl) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K93** | 429 ve 503 yanıtları `Retry-After` başlığını da taşır | Faz 10 (25 Eyl) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K94** | §A girdisi: BOŞ. Varsayılanlar: klasik `api_pay4.php`; ödeme imzası `base64(HMAC(random_nr·order_id·tutar·par`… | Faz 12 (24 Eki) | ⚠️ geçici: elle doğrulamadan sonra güncellenecek | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K95** | Mail kanalı kodda sağlayıcıdan bağımsız; geliştirmede `MAIL_MAILER=log`. SES mi alan adının SMTP'si mi, deplo… | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K96** | Kullanıcıya giden mailler Türkçe (K21'in istisnası). Dil `config/davetkart.php` → `mail.locale` | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K97** | Hesap silinince anonimleştir: kullanıcı, davetiyeleri, LCV'leri, medyası (dosyalarıyla) silinir; `orders` sat… | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K98** | Saklama süreleri: çöp kutusundaki davetiye 30 gün · misafir verisi etkinlikten 6 ay · iletişim mesajı 12 ay.… | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K99** | Paket (davetiyesiz alınan sipariş) tek davetiye yayınlar: bağsız tekil sipariş olarak açılır, ilk yayında bağ… | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K100** | İade, davetiyeyi kapsayan başka ödenmiş sipariş bırakmıyorsa davetiye yayından kalkar ve taslağa döner | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K101** | Misafire düzenleme kodu: aynı tarayıcıdan ikinci gönderim yeni satır açmaz, eskisini günceller (`PUT /public/`… | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K102** | P-1 karışık: Elit'te *"DavetKart ile hazırlandı"* yok · premium = videolu 13 tema, en az Gold · *"video galer… | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K103** | Zamanlanmış işler Sentry Cron Monitors'a bağlı (sabit izleyici adları) | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K104** | Hız sınırları düğüne göre: LCV IP 20/dk, davetiye 300/saat · medya IP 15/dk, davetiye 150/saat · IPv6 kovası… | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K105** | IBAN her kayıtta biçim + mod-97 ile doğrulanır (TR 26 karakter); değer yazıldığı gibi saklanır | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K106** | Asistanın günlük kotası İstanbul gece yarısında yenilenir (`default_timezone`) | Faz 10 (25 Eyl–1 Eki) | geçerli | backend `claude/FAZ-10-PLANI.md` §2 |
| **K107** | Hediye = sipariş. Kod planı tamamen karşılıyorsa `provider='gift'`, `status='paid'`, `amount_minor=0` sipariş… | Faz 11 (23 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md#a-karar-kaydına-eklenecek-7) |
| **K108** | Kısmi indirimde normal akış: `amount_minor = fiyat − indirim`, `discount_minor` ayrı kolon | Faz 11 (23 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md#a-karar-kaydına-eklenecek-7) |
| **K109** | Kod değil `sha256(normalize(kod))` saklanır + son 4 karakter ipucu | Faz 11 (23 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md#a-karar-kaydına-eklenecek-7) |
| **K110** | Kullanım sayısı saklanmaz: aktif = bağlı sipariş `pending`/`paid`/`refunded`; `failed`/`expired` kodu geri ve… | Faz 11 (23 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md#a-karar-kaydına-eklenecek-7) |
| **K111** | Kişi başı 1 aktif kullanım; kontrol kod satırı `lockForUpdate` ile kilitliyken | Faz 11 (23 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md#a-karar-kaydına-eklenecek-7) |
| **K112** | Yüzde `intdiv` (aşağı), sabit `min(tutar, fiyat)`, `free` yalnızca kendi planında, indirim kodunda `tier=null`… | Faz 11 (23 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md#a-karar-kaydına-eklenecek-7) |
| **K113** | Yok/kapalı/süresi dolmuş/tükenmiş → tek kod `GIFT_CODE_INVALID`; ayrıca `GIFT_CODE_ALREADY_USED`, `GIFT_CODE_`… | Faz 11 (23 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md#a-karar-kaydına-eklenecek-7) |
| **K114** | İade edilen sipariş kullanımı geri vermez | Faz 11 (23 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md#a-karar-kaydına-eklenecek-7) |
| **K115** | Tek kullanımlık kodlar bir kez gösterilir: `storage/app/private/gift-codes/<batch>.csv`; konsola basılmaz | Faz 11 (23 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md#a-karar-kaydına-eklenecek-7) |
| **K116** | Süresi dolup kullanımı iade olmuş siparişe geç ödeme gelirse kod `max_redemptions`'ı 1 aşabilir: bilinen ve k… | Faz 11 (23 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md#a-karar-kaydına-eklenecek-7) |
| **K117** | Onay kanalı `SHOPIER_CONFIRMATION`, varsayılan `osb`: tarayıcı callback'i yalnızca yönlendirir, `paid`'i yaln… | Faz 12 (24 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K118** | `CheckoutSession` bir `CheckoutAction` taşır: `RedirectAction(url)` \| `FormPostAction(url, fields)`. `Paymen`… | Faz 12 (24 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K119** | `OrderResource.checkout = {type:'redirect',url} \| {type:'form',url,fields}`; `redirectUrl` `type=redirect` i… | Faz 12 (24 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K120** | Shopier paketi eklenmez, kendi sürücümüz | Faz 12 (24 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K121** | `platform_order_id = orders.id = provider_ref` (M8 korunur); Shopier'in kimliği `orders.provider_payment_id`… | Faz 12 (24 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K122** | Callback yanıtı 303, hedef `config('payment.return_urls')`'ten, `order` yalnızca ULID ise; geçersiz imza → `/`… | Faz 12 (24 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K123** | Sır, mod ya da (`osb` modunda) OSB kimliği eksikse `ShopierGateway` kurulmaz → 503 | Faz 12 (24 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K124** | Tutar metni `sprintf('%d.%02d', intdiv, %)`; imzaya giren ve forma yazılan aynı değişken | Faz 12 (24 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K125** | Ad/soyad/e-posta kullanıcıdan; TCKN, telefon, adres `config('payment.providers.shopier.buyer_placeholders')` | Faz 12 (24 Eki) | ⚠️ elle doğrulama bekliyor | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K126** | Bildirim tutar taşıyorsa (OSB) siparişin `amount_minor` + `currency`'siyle eşleşmeli; uymazsa geçiş yok + `Lo`… | Faz 12 (24 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K127** | Tarayıcı callback'i ayrı metot (`parseCallback`) ve ayrı tip (`ShopierCallback`); `osb` modunda bildirim nesn… | Faz 12 (24 Eki) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7) |
| **K146** | Plan kuralları sözleşmesi: `plans:export` → `contracts/plan-rules.json` (fiyat ve damga yok), `--check` `composer check` zincirinde | Faz 18.1 (16 Kas) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |
| **K147** | Frontend `verify:plans`: `minimumTier`, fiyat kartı ve `getRequiredTier` ↔ sözleşme kopyası (kopya, kardeş depodan okuma yok) | Faz 18.1 (16 Kas) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |
| **K148** | Dağıtım sırası: önce backend, `plans:export --check` yeşilken frontend; tersine sıra yasak | Faz 18.1 (16 Kas) | geçerli · ⚠️ sunucuda denenmedi | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |
| **K149** | Sürüm etiketle izlenir (`vMAJOR.MINOR.PATCH`, iki depoda aynı); deploy betikleri etiketi yazar, etiketsiz commit uyarı verir, durdurmaz | Faz 18.1 (16 Kas) | geçerli · ⚠️ sunucuda denenmedi | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |
| **K150** | Kalite kapısı kırmızı olan dal yayın adayı değildir; `TST-01` `OPS-01` dalında kapandı | Faz 18.1 (16 Kas) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |
| **K151** | Gece yedeği: 02:00 UTC'de `pg_dump -Fc`; ayrı cron dosyası, `root`, Laravel zamanlayıcısından bağımsız; kilit (`flock`) betiğin içinde | Faz 18.2 (16 Kas) | geçerli · ⚠️ sunucuda denenmedi | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |
| **K152** | Yedekler medyadan ayrı S3 bucket'ında: Block Public Access, sürümleme, SSE-S3; geçerli sürüm 30 gün + eski sürüm 7 gün (etkili saklama ~37 gün) | Faz 18.2 (16 Kas) | geçerli · ⚠️ bucket henüz açılmadı | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |
| **K153** | Sunucudaki yedek kimliği yalnızca yazabilir (`s3:PutObject`, `daily/*`); anahtar root:600 dosyada; betik root'a ait kurulu kopyadan çalışır | Faz 18.2 (16 Kas) | geçerli · ⚠️ kimlik henüz açılmadı | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |
| **K154** | Yedek veritabanına `postgres` sistem kullanıcısı + peer ile bağlanır; `.pgpass` yok, parola hiçbir yerde yok | Faz 18.2 (16 Kas) | geçerli · ⚠️ sunucuda denenmedi | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |
| **K155** | Döküm yüklenmeden doğrulanır (`pg_restore --list`, boyut, zorunlu tablolar) ve `manifest.json` ile gider; satır sayıları dökümle aynı anlık görüntüden | Faz 18.2 (16 Kas) | geçerli | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |
| **K156** | Yedek izlemesi asgari: isteğe bağlı iki kalp atışı adresi (başarı / başarısızlık); adres günlüğe yazılmaz; alarm `OPS-03` | Faz 18.2 (16 Kas) | geçerli · adresler boş | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |
| **K157** | Kayıt açılmadan önce üretim dökümüyle geri yükleme provası ve ölçülen süre plana; sonra ayda bir; RPO 24 saat kabul, WAL/PITR ayrı karar | Faz 18.2 (16 Kas) | geçerli · ⚠️ üretim provası yapılmadı | [`addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md#a-karar-kaydına-eklenecek-7) |

## Notlar

- Eksik numara: yok (K1–K127).
- Çakışma: backend `docs/07` §8'deki ikinci **K18** (Pest/PHPUnit) orada **K24** olarak düzeltilmiş (`docs/07:958`). Bu depoda çakışma yok.
- K94, Faz 10 planında Shopier için ayrıldı, Faz 12'de tanımlandı; bu yüzden sıra dışı görünür.
- Ana dosyaya (`context/PHP-LARAVEL-SETUP.md` §7) işlenmiş olanlar yalnızca K1–K48 ve K64–K71. Geri kalanı kaynak sütunundaki ek dosyalarda bekliyor.
- Backend kaynakları (`davetkart-backend-php-laravel/claude/…`) bu depoda değil; yol düz metindir.
