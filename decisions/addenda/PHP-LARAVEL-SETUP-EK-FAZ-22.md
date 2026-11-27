# `PHP-LARAVEL-SETUP.md` — Faz 22 Yaması

> **Tarih:** 27 Kasım 2026 · takip tablosu [`phases/faz-22/README.md`](../../phases/faz-22/README.md)
> **Ne bu:** Ana devir dosyasına (`context/PHP-LARAVEL-SETUP.md`) **işlenmeyi bekleyen** Faz 22 kayıtları. `-EK-FAZ-21` ile aynı biçim.
> **Tam kayıt:** `davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-22.md` · Numaralar K276'dan başlar.

---

## A. Karar Kaydı'na eklenecek (§7)

### 22.1 — E-posta doğrulaması satın almayı engellemez

Dal: backend/frontend `faz-22-release-prep`. İstek: İsmail, 27 Kasım 2026.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K276** | E-posta doğrulaması checkout'u ve yayını **beklemez**: `VerifiedEmailGuard`, `EmailNotVerifiedException` ve `403 EMAIL_NOT_VERIFIED` kaldırıldı (katalog 28 → 27, K270). İlk yayın indirimi doğrulama istemeye **devam eder** (`FirstPublishEligibility`; doğrulanmamış hesap liste fiyatından öder). Panelde kapatılamayan hatırlatma bandı: "Hesap erişiminizi kaybetmemek için e-posta adresinizi doğrulayın"; bant doğrulamanın indirimi açtığını da söyler. Kayıtta doğrulama postası, yeniden gönderme (saatte 3) ve bağlantı (24 saat) aynı. K191'in checkout ve yayın maddelerini geçersiz kılar | Doğrulama satın almanın önünde sürtünmeydi; ödeme sağlayıcısı alıcıyı ayrıca doğruluyor. Yayın kapısı da birlikte kalkmalı: kalsaydı ödeme dönüşündeki otomatik yayın (K267) 403 alırdı. İndirim hesaba bağlı bir hak; doğrulamasız uydurma adresle açılan her hesap bir indirim daha alırdı (K191 gerekçesi geçerli) | geçerli · **İsmail'in kararı** (indirim sorusu oturumda cevaplandı) · Faz 22.1 (27 Kas) |

**Eski kararların durum notları:**

- K191 → checkout ve yayın kapısı (`403 EMAIL_NOT_VERIFIED`) **geçersiz kılındı → K276**; doğrulama bağlantısı, yeniden gönderme ve "ilk yayın indirimi yalnızca doğrulanmışa" maddeleri geçerli.
- K159 → değişmedi (K191 daraltması sürüyor).
