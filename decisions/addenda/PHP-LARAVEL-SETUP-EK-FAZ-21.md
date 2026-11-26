# `PHP-LARAVEL-SETUP.md` — Faz 21 Yaması

> **Tarih:** 27 Kasım 2026 · **Kaynak:** `AUD-2026-11-12` düşük/öneri bulguları + `AUD-2026-11-26` §4b ·
> takip tablosu [`phases/faz-21/README.md`](../../phases/faz-21/README.md)
> **Ne bu:** Ana devir dosyasına (`context/PHP-LARAVEL-SETUP.md`) **işlenmeyi bekleyen** Faz 21 kayıtları. `-EK-FAZ-20` ile aynı biçim.
> **Tam kayıt:** `davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-21.md` · Numaralar K265'ten başlar.
> **Karar yolu:** Faz 21 tek oturumda, onaysız koştu. §A "Cevabın" sütunu boş kalan maddelerde plandaki varsayılan
> uygulandı; bu kararların durumunda "varsayılan (İsmail cevaplamadı)" yazar.

---

## A. Karar Kaydı'na eklenecek (§7)

### 21.1 — `SEC-16` (hesap bazlı, IP'den bağımsız giriş freni)

Dal: backend `faz-21-backlog`. Bulgu: `AUD-2026-11-12` [`findings/02-security.md`](../../audits/2026-11-12-full-system-audit/findings/02-security.md) "SEC-16".

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K265** | Girişte üçüncü kova: hesap başına, IP'den bağımsız **saatte 30 başarısız** deneme (anahtar `login-fail\|HMAC(normalize(e-posta))`, APP_KEY'li). Yalnızca başarısız giriş sayılır; kayıtsız adres de sayılır. Dolunca `429 RATE_LIMITED` + `retryAfter`, parola hiç denenmez (doğru parola da 429). Kalıcı kilit yok: pencere en geç bir saatte kapanır, başarılı parola sıfırlama kovayı boşaltır, açık oturumlar etkilenmez. Kova ilk dolduğunda var olan hesabın sahibine kuyruklu, Türkçe, IP'siz uyarı postası (ayrı kovayla saatte en çok bir). Mevcut iki kova (e-posta + IP 5/dk, IP 20/dk) ve sırası aynı | İki kovanın anahtarında da IP vardı; çok IP'den tek hesaba yapılan denemeler birikmiyordu. Başarılı girişi saymamak için kova rota ara katmanında değil Action'da (`Limit::by` her isteği sayar). Dolu kovada doğru parola geçseydi 429/200 farkı tahmini ele verirdi. Kayıtsız adres sayılmasaydı 429 sayım açığı olurdu. Kalıcı kilit saldırgana sahibi dışarıda tutma aracı verirdi; sıfırlama sahibin yolu | geçerli · **varsayılan (İsmail cevaplamadı)** · Faz 21.1 (27 Kas) |

- Sayılar `app/Support/AccountLoginThrottle.php` sabitlerinde (`MAX_FAILURES = 30`, `DECAY_SECONDS = 3600`); test bilerek
  sabit sayıyla yazıldı.
- Hata sözleşmesi değişmedi (yeni kod yok); backend `docs/08-HATA-SOZLESMESI.md` §4.1'e girişte `RATE_LIMITED`'ın üç
  kaynağı notu eklendi.
- Neyi kapatmaz (B6): saldırgan saatte 30 başarısız denemeyle sahibi o saat için girişten alıkoyabilir (sıfırlama yolu
  açık); kayıtlı hesabın 30. denemesinde posta kuyruğa yazılırken birkaç ms fark olabilir.

### 21.2 — `SEC-15` (kayıt ucu adresin kayıtlı olduğunu söylüyor)

Dal: backend `faz-21-backlog`. Bulgu: `AUD-2026-11-12` [`findings/02-security.md`](../../audits/2026-11-12-full-system-audit/findings/02-security.md) "SEC-15". §A-1: B.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K266** | `SEC-15` kabul edilen risk: kayıt ucu kayıtlı adresi `422 REGISTRATION_FAILED` ile söyler (yeni adreste `201`); sözleşme (K11 `{user, token}`, oturum açar) aynı kalır. Frenler: kayıt `throttle:auth` kovalarında (adres + IP 5/dk, IP 20/dk; kayıtlı adresle deneme de sayılır, giriş ile ortak kova), iki yolda da Argon2id hash (`hashed` cast'i INSERT'ten önce), `fields` yok. Frenler testle kilitlendi; yanıt süresi test edilmedi. Tam kapatma = kayıt her zaman `202 {status:"check_email"}`, oturum doğrulamadan sonra, kayıtlı adrese "siz miydiniz?" postası; K11'i ve frontend kayıt akışını değiştirir, ayrı faz | Giriş ve sıfırlama uçları sayım açığını kapattı; kayıtta durum kodu farkı kalıyor. Tam kapatma kullanıcıya bir adım (posta) ekler ve onaysız tek oturumda kimlik akışı değiştirilmez. Kovalar zaten vardı (`throttle:auth`), kod eklenmedi | geçerli · **varsayılan (İsmail cevaplamadı)** · Faz 21.2 (27 Kas) |

- Neyi kapatmaz (B6): çok IP'li saldırgan IP başına dakikada 20 adres tarayabilir; hesap başına kova (K265) taramayı
  durdurmaz, çünkü her adres bir kez denenir.

### 21.3 — `FE-58` (ödeme dönüşünde davetiye kullanıcıya sorulmadan yayınlanıyor; K67 ile çelişki)

Dal: frontend `faz-21-backlog`. Bulgu: `AUD-2026-11-12` [`findings/04-frontend-e2e.md`](../../audits/2026-11-12-full-system-audit/findings/04-frontend-e2e.md) "FE-58". §A-1: otomatik yayın kalır.
Açık soru: [`EK-FAZ-12`](PHP-LARAVEL-SETUP-EK-FAZ-12.md) §F-7.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K267** | K67 daraltıldı: ödeme **sunucuda** yayınlamaz (webhook yalnızca siparişi `paid` yapar). Frontend, yayın niyetiyle başlayan ödemenin (davetiyeye bağlı sipariş) dönüşünde **bir kez** `POST /invitations/{id}/publish` ister; plan kontrolü (402) sunucuda. Sekme başına sipariş başına tek istek (`sessionStorage` `davetkart-auto-published`, en çok 20 kimlik); aynı sekmede yenileme ya da geri gelme yeni istek üretmez, kart "Ödemeniz onaylandı" der. Paket siparişi (`invitationId: null`) yayınlamaz | Kullanıcı ödemeye editörde "Yayınla"dan gelir; dönüşte ikinci bir onay aynı soruyu iki kez sorar. K67'nin gerekçesi (paket alımda davetiye belirsiz, webhook makine bildirimi) sunucu için doğru kalır. Yenilemede istek tekrar giderse kullanıcının panelden kaldırdığı davetiye sorulmadan yeniden yayınlanırdı | geçerli · **varsayılan (İsmail cevaplamadı)** · Faz 21.3 (27 Kas) |

- K67 → "daraltıldı → K267" (silinmedi).
- Neyi kapatmaz (B6): başka sekmede ya da yeni oturumda aynı dönüş adresi yine istek atar (yayındaysa 409 = başarı;
  kaldırılmışsa yeniden yayınlanır). Tam kapatma için siparişin "hakkı yayınlandı mı?" bilgisi (`orders.first_published_at`,
  Faz 18.4) `GET /orders/{id}` yanıtına girmeli (ayrı iş).
- Kod: `src/utils/autoPublish.ts` (`claimAutoPublish`, `returnCardView`), `verify:payment` 19 yeni denetim.

### 21.4 — `OPS-08` (günlüklerde istek kimliği yok)

Dal: backend `faz-21-backlog`. Bulgu: `AUD-2026-11-12` [`findings/05-operations.md`](../../audits/2026-11-12-full-system-audit/findings/05-operations.md) "OPS-08".

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K268** | Her yanıt `X-Request-Id` başlığı taşır (ULID). Gelen `X-Request-Id` yalnızca biçimi ULID ya da UUID ise kullanılır (biçim uzunluğu da sınırlar: 26/36), değilse yenisi üretilir. Kimlik Laravel `Context`'ine `request_id` olarak yazılır: günlük satırının `extra`'sına ve kuyruk işinin yüküne kendiliğinden gider. Hata zarfına **girmez** (K20 aynı). Ara katman (`AssignRequestId`) global zincirin en başında. Nginx'e öneri: erişim günlüğüne `$upstream_http_x_request_id` (nginx `$request_id` 32 hex, kabul edilmez) | Tanı: bir kullanıcı eylemi birden çok günlük satırı ve kuyruk işi üretir. Zarfa alan eklemek sözleşmeyi ve frontend tiplerini değiştirirdi; başlık yeter. Serbest metne güvenmek günlüğe istemcinin metnini sokardı. En başta durmazsa bakım kipi (503) ve 413 gibi erken yanıtlar kimliksiz kalırdı | geçerli · **varsayılan (İsmail cevaplamadı)** · Faz 21.4 (27 Kas) |

- Neyi kapatmaz (B6): Sentry olayına kimlik etiketi yok; zamanlayıcı/komut satırlarında `request_id` yok. Frontend'in
  hata bildiriminde kimliği göstermesi ayrı iş.
