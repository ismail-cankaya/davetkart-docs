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
