# `PHP-LARAVEL-SETUP.md` — Faz 11 Yaması

> **Tarih:** 23 Ekim 2026
> **Ne bu:** Ana devir dosyasına (`claude/PHP-LARAVEL-SETUP.md`) **işlenmeyi bekleyen** Faz 11
> kayıtları. `-EK-FAZ-5…9` dosyalarıyla aynı biçim.
> **Tam kayıt:** `davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-11.md`
> 🔴 **Ana dosyaya henüz işlenmedi:** `PHP-LARAVEL-SETUP.md`'de commit'lenmemiş bir değişiklik
> var ve İsmail'in kararı "önce o commit'lensin". O commit'ten sonra bu dosyanın A–F
> bölümleri ana dosyaya taşınır.

---

## A. Karar Kaydı'na eklenecek (§7)

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K107** | **Hediye = sipariş.** Kod planı tamamen karşılıyorsa `provider='gift'`, `status='paid'`, `amount_minor=0` sipariş yazılır; sağlayıcıya gidilmez | Yayın hakkı, bağsız siparişin bağlanması, 402 kontrolü ve iade sonrası yayından kaldırma değişmeden tanıyor. Ayrı bir hak kaynağı beş yere ikinci sorgu eklerdi | ✅ Faz 11 |
| **K108** | Kısmi indirimde normal akış: `amount_minor = fiyat − indirim`, `discount_minor` ayrı kolon | Shopier (Faz 12) imzalı tutarı `amount_minor`'dan alacak; indirim sağlayıcıya şeffaf | ✅ Faz 11 |
| **K109** | Kod değil `sha256(normalize(kod))` saklanır + son 4 karakter ipucu | Kod para değerinde; tek kullanımlık kodlar ~59 bit, özetten geri bulunamaz (**H14**) | ✅ Faz 11 |
| **K110** | Kullanım sayısı **saklanmaz**: aktif = bağlı sipariş `pending`/`paid`/`refunded`; `failed`/`expired` kodu geri verir | Sayaç her başarısızlık yolunda (sağlayıcı hatası, `orders:expire`, red) elle düşürülmek zorunda kalırdı (**E13**) | ✅ Faz 11 |
| **K111** | Kişi başı 1 aktif kullanım; kontrol kod satırı `lockForUpdate` ile kilitliyken | Kilit aynı kodun bütün kullanımlarını sıraya koyuyor. Partial unique index kurulamazdı: aktiflik başka tabloda | ✅ Faz 11 |
| **K112** | Yüzde `intdiv` (aşağı), sabit `min(tutar, fiyat)`, `free` yalnızca kendi planında, indirim kodunda `tier=null` = bütün planlar | Float yok; kuruş farkı işletmenin lehine | ✅ Faz 11 |
| **K113** | Yok/kapalı/süresi dolmuş/tükenmiş → tek kod `GIFT_CODE_INVALID`; ayrıca `GIFT_CODE_ALREADY_USED`, `GIFT_CODE_NOT_APPLICABLE` (`params.tier`); hepsi 422 | Kod tahmin edene hangi kodların var olduğu sızmaz. Dört yanıt bayt bayt aynı (testli) | ✅ Faz 11 |
| **K114** | İade edilen sipariş kullanımı geri **vermez** | Öde → iade et → tekrar kullan döngüsü olmasın | ✅ Faz 11 |
| **K115** | Tek kullanımlık kodlar bir kez gösterilir: `storage/app/private/gift-codes/<batch>.csv`; konsola basılmaz | K109'un sonucu | ✅ Faz 11 |
| **K116** | Süresi dolup kullanımı iade olmuş siparişe geç ödeme gelirse kod `max_redemptions`'ı 1 aşabilir: **bilinen ve kabul edilen sınır** | Engellemek parası alınmış siparişi reddetmek olurdu | ✅ Faz 11 (kod yazılmadı) |

---

## B. Kurallar'a eklenecek (§11)

| # | Kural | En kısa hâli |
|---|---|---|
| **E13** | Geri alınması gereken bir sayaç saklanmaz; sayılan olayların **durumundan türetilir** | *Sayacı düşürmeyi her başarısızlık yolu hatırlamak zorundaysa, sayaç yalan söyleyecektir* |
| **H14** | Para değerindeki bir sır veritabanına, log'a ve konsola **düz yazılmaz** | *Özet saklanır, ipucu gösterilir, sır bir kez verilir* |

> **Toplam:** 140 (FAZ-0…9) + FAZ-10 (bkz. `FAZ-10-PLANI.md`) + **FAZ-11: 2**

---

## C. Dersler'e eklenecek (§13)

**65. PostgreSQL'de bir hata bütün transaction'ı zehirler.** UNIQUE ihlalini yakalayıp devam
etmek isteyen kod `save()`'i iç bir `DB::transaction` (savepoint) ile sarmalı. Aksi halde dışta
bir transaction varsa (testlerde `RefreshDatabase`) sonraki her sorgu `25P02` alır.

**66. 🔴 PHPUnit yarış koşulu göremez.** Tek süreç, tek bağlantı, tek transaction:
`lockForUpdate` silinse bütün testler yeşil kalır. Kilidin kanıtı ancak birden çok süreçle
(`pcntl_fork`, ayrı bağlantılar, yapay bekleme penceresi) alınır. Faz 11'de kilitli 1/6,
kilitsiz 6/6.

**67. `expectsOutputToContain` sıralı ve tüketicidir.** Her beklenti bir çıktı satırını
tüketir; aynı tablo satırındaki iki hücre için iki beklenti yazılırsa ikincisi "yok" der.
Çözüm `Artisan::call()` + `Artisan::output()`.

**68. Bir "açık karar"ı kilitleyen test bir sözleşmedir.** `OrderTest` yanıtta `amount`
kelimesini arıyor. Yeni alan (`discountMinor`) C7 kalıbıyla, yalnızca varken eklendi; karar
değişecekse önce test bilinçli olarak güncellenir.

---

## D. §9 Teknik Durum: güncelleme

### Çalışan uç noktalar (yeni ve değişen)

| Uç | Ne |
|---|---|
| `POST /api/gift-codes/preview` `{code, tier}` | 200 `{benefit, tier, priceMinor, discountMinor, totalMinor, currency}` · 422 `GIFT_CODE_*` · `auth:sanctum` + `throttle:gift-code` |
| `POST /api/invitations/{id}/checkout` | + isteğe bağlı `giftCode`; tutar 0 ise 201 `status: paid` |
| `POST /api/payments/checkout` | Aynı |
| `GET /api/orders`, `/api/orders/{id}` | + isteğe bağlı `discountMinor` (yalnızca indirim varsa) |

### Komutlar

`gift-codes:create` · `gift-codes:generate` · `gift-codes:list` · `gift-codes:disable`

### Tablolar

`gift_codes` · `gift_code_redemptions` · `orders.discount_minor` + `orders_gift_amount_check`

### Kalite kapısı

`composer check` **684/684** (bulut çalışma alanında, PHP 8.5.12 + PostgreSQL 16; İsmail'in
makinesinde koşmadı). Her adım commit'i ayrı ayrı da yeşil: 551 → 569 → 593 → 616 → 628 → 673 → 684.

---

## E. §10 Yol Haritası: güncelleme

| Faz | Konu | Durum |
|---|---|---|
| **11** | Hediye kodu | ⚠️ backend ✅ (11.1–11.11) · frontend ✅ (11.12–11.16) · elle doğrulama bekliyor |
| **12** | Shopier ile kredi kartı ödemesi | ⬜ Faz 11 commit'lendikten sonra (`PROMPT-FAZ-12.md`) |

---

## F. §15 Açık Sorular: güncelleme

### ⬜ Faz 11'in eklediği

1. `OrderResource`'ta `amountMinor` açılsın mı? (Ödeme dönüş sayfası "ödenen tutar" göstermek isterse.)
2. Bekleyen sipariş kodu 30 dk tutar: aynı kişi kart sayfasını kapatıp tekrar denerse
   `ALREADY_USED`. Kabul mü, yoksa yeni checkout eski `pending` siparişi iptal mi etsin?
3. Toplu kapatma (`gift-codes:disable --batch=`) gerekli mi?
4. Kilit için otomatik bir eşzamanlılık testi grubu kurulsun mu? (Ders 66.)
5. `GiftCodeRedemption::releasingStatuses()` → `OrderStatus`'a taşınsın mı (K50 deseni)?
6. `docs/rehber/fazlar/README.md`'de Faz 10 satırı yok (`FAZ-10.md` yazılmamış).
