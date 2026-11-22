# Süre takvimi — bitiş tarihi olan her şey (tek ev)

> **Tarih:** 22 Kasım 2026 (Faz 19.8, `OPS-05`) · Önceki tablo: [`YAYIN-PLANI.md`](YAYIN-PLANI.md) §8 "📅 Süre takvimi"
> (tarihsel kayıt olarak orada kalır; güncel hâli burası). Hatırlatıcılar: [`davetkart-sure-takvimi.ics`](davetkart-sure-takvimi.ics).
> Kural: süresi dolan her şey (alan adı, sertifika, kredi, abonelik) bir izleme kalemidir. Hatırlatıcı
> bitişten **30 gün** ve **7 gün** önce. Durum değişince bu tabloyu ve `.ics`'i birlikte güncelle.

## 1. Önce yapılacak (İsmail doğrulayacak)

| # | Ne | Neden | Hatırlatıcı |
|---|---|---|---|
| 0 | 🔴 Natro panelinde `davetkart.com` **otomatik yenilemesini aç**, kayıtlı kartın geçerlilik tarihini kontrol et | 4 Ekim kaydı: "Otomatik yenileme KAPALI". Durum bugün bilinmiyor (§A-1 cevapsız) | 25 Kasım 2026 |

## 2. Takvim

| Kalem | Bitiş | Biterse ne durur | Sahibi | Yenileme yolu | Hatırlatıcı (30 / 7 gün) | Durum |
|---|---|---|---|---|---|---|
| **Alan adı** `davetkart.com` (Natro) | **11 Eylül 2027** | Site, API, `media.` alt alanı, SSL yenilemesi ve bütün postalar aynı gün; alan adı başkasına geçerse kalıcı | İsmail | Natro → Alan adlarım → otomatik yenileme + kart | 12 Ağustos 2027 · 4 Eylül 2027 | ⚠️ otomatik yenileme KAPALI (4 Ekim); §1 #0 |
| **Natro posta barındırma** (Standart, 250 MB, 1 hesap) | **11 Ocak 2027** | `bilgi@davetkart.com` kutusu: müşteri yanıtları ve SES'in gönderen adresine gelen yanıtlar geri döner. SES'in **gönderimi** durmaz (DKIM Natro DNS'inde, kutudan bağımsız) | İsmail | §3'teki karar; yenileme 5,88 $/yıl | **11 Aralık 2026 (karar)** · 4 Ocak 2027 | ⚠️ karar verilmedi (§A-2 cevapsız) |
| **AWS kredisi** (kalan 136,51 $, 25 Ekim) | **25 Temmuz 2027** | Hiçbir şey durmaz; harcama (~15 $/ay, Y4.5 bütçesi) karta yansır. Kart geçersizse hesap askıya alınabilir | İsmail | Billing → Payment methods: kart; Budgets: `davetkart-kart-cekimi` alarmı zaten net maliyeti izler | **25 Haziran 2027** · 18 Temmuz 2027 | ⚠️ kredi sonrası aylık tahmin ve kart hazır mı bilinmiyor (§A-3 cevapsız) |
| **SSL** `davetkart.com`, `www` (Let's Encrypt) | Otomatik (90 gün; 10 Şubat 2027'den sonra 64 gün) | Tarayıcı siteyi açmaz | Sunucu | `certbot.timer` günde 2 kez; bitime 30 gün kala yeniler. `renew --dry-run` ✅ (Y7.2b, 26 Ekim) | Sabit gün **yok** (plan kararı: ömür kısalıyor) | ✅ otomatik · ⚠️ dış izleme yok: Let's Encrypt artık uyarı e-postası atmıyor; SSL bitiş izlemesi Y11.7 / `OPS-03` ile kurulacak |
| **SSL** `media.davetkart.com` (ACM, us-east-1) | Otomatik (ACM yönetir) | Medya (görseller) açılmaz | AWS | ACM DNS doğrulamasıyla kendisi yeniler; şartı Natro'daki `_db41d7…media` CNAME'inin **silinmemesi** (YAYIN-PLANI §8) | yok | ✅ otomatik |

Tarihlerin kaynağı: alan adı ve posta YAYIN-PLANI §8 tablosu; kredi Y1.3 (25 Ekim) satırı; SSL Y7.2b.

## 3. Posta kararı (11 Aralık 2026'ya kadar)

§A-2 cevaplanmadı; karar verilmedi, K yazılmadı. Seçenekler:

| Seçenek | Maliyet | SES gönderen adresine etkisi | Taşıma adımları |
|---|---|---|---|
| **Natro'da yenile** | 5,88 $/yıl (plan kaydı) | Yok | Natro panelinde yenile; başka iş yok |
| **Zoho Mail** (plan kaydında anılan seçenek) | Ücretsiz plan var; koşulları kayıttan önce Zoho'nun sitesinden doğrula | Gönderim etkilenmez; SPF'e Zoho eklenir, Zoho'nun DKIM kaydı **ayrı seçiciyle** eklenir (SES'in 3 CNAME'i kalır) | Zoho'da alan adı doğrula (TXT) → `bilgi@` kutusu → MX'i Zoho'ya çevir → SPF'e `include` → Zoho DKIM → eski postaları dışa/içe aktar → MX yayıldıktan sonra Natro posta hizmetini bitir |
| **Google Workspace** | Kullanıcı başına aylık ücret (güncel fiyat sitesinde) | Zoho ile aynı (SPF + ayrı DKIM seçicisi) | Zoho ile aynı adımlar, Google yönergeleriyle |
| **SES gelen posta** | Çok düşük (kullanım başına) | Gönderen ile aynı hizmet | Kutu değildir: posta S3'e düşer, okumak/iletmek için ek iş (kural + Lambda). SES gelen posta yalnızca bazı bölgelerde var; Frankfurt'ta olup olmadığını konsolda doğrula. Tek kişilik destek için en zahmetlisi |

⚠️ Her taşımada: MX değişikliği yayılana kadar (TTL) iki kutu da açık kalmalı; DMARC (`p=none`) değişmez.
Natro'da **DNS** ile **posta barındırma** ayrı hizmetlerdir (plan kaydı); posta bitince DNS kayıtları kalır, bunu Natro panelinde doğrula.

## 4. AWS kredisi bitince (25 Haziran 2027'ye kadar)

- Billing → Bills: son üç ayın kredi öncesi ham tutarı (bütçe `davetkart-aylik-harcama` ham harcamayı izler).
- Kartın geçerlilik tarihi Temmuz 2027'den sonra mı.
- Tahmini aylık maliyeti buraya yaz: `… $/ay (… tarihinde ölçüldü)`.

## 5. Bakım

- Yeni bitiş tarihi (yeni hizmet, yeni sertifika, yeni abonelik) → bu tabloya satır + `.ics`'e iki VEVENT.
- `.ics`'i içe aktarma: Google Takvim → Ayarlar → İçe ve dışa aktar → dosyayı seç. Outlook → Takvim ekle →
  Dosyadan yükle. Aynı dosyayı yeniden içe aktarmak, aynı `UID`'li etkinliği çoğu uygulamada güncelleyebilir; çift
  görünürse eskisini sil.
