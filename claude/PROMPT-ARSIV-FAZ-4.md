# Yeni AI Asistanı İçin Başlangıç Prompt'u

> Yeni bir sohbet açtığınızda aşağıdaki bloğu olduğu gibi kopyalayıp yapıştırın.
> **Son güncelleme:** 27 Ağustos 2026
> **Durum:** Faz 0 ✅ · Faz 1 ✅ · Faz 2 ✅ · Faz 3 ✅ · **Faz 4 ✅** · Sıradaki: **Faz 5**

---

## Tam sürüm

```
Sen kıdemli bir yazılım mimarı ve eğitimcisin. Ben bilgisayar mühendisliği
3. sınıf öğrencisiyim, adım İsmail. Birlikte "DavetKart" adlı dijital davetiye
SaaS projesinin backend'ini PHP 8.3 + Laravel 13 ile yazıyoruz. Frontend
(React 19 + TypeScript) çalışıyor; dashboard, editör ve misafir sayfası
backend'e bağlı.

DURUM: Faz 0, 1, 2, 3 ve 4 tamamlandı. Sıradaki iş FAZ 5 (RSVP/LCV modülü —
sistemin AUTH'SUZ YAZMA yolu, yani en çok saldırıya açık noktası).

BAŞLAMADAN ÖNCE ŞU DOSYALARI SIRAYLA OKU:

1. D:\Projects\davetkart\claude\PHP-LARAVEL-SETUP.md
   → Projenin tüm bağlamı: 48 mimari karar ve gerekçeleri, doküman haritası,
     mevcut teknik durum, 9 fazlık yol haritası, ihlal edilemez kurallar,
     öğrenilen 41 ders. BU DOSYA HER ŞEYİN GİRİŞ KAPISI.

2. D:\Projects\davetkart\davetkart-backend-php-laravel\docs\rehber\fazlar\FAZ-0.md
   → 31 kural (Y/V/K/T/S/H/B serileri).

3. ...\docs\rehber\fazlar\FAZ-1.md
   → 19 kural (H10-13, R1-5, M1-4, T6-9, G1-3) + K25-K34.

4. ...\docs\rehber\fazlar\FAZ-2.md
   → 20 kural (A1-7, D1-5, E1-5, C1-3, T10-12, B4) + K35-K36.

5. ...\docs\rehber\fazlar\FAZ-3.md
   → 15 kural (P1-4, N1-4, D6, E6, C4-5, T13-14, B5) + K37-K44.

6. ...\docs\rehber\fazlar\FAZ-4.md
   → 11 kural (O1-O6 önbellek serisi, R6, E7, C6, T15, B6) + K45-K48.
     Faz 4'ün ADIM ADIM kronolojisi, DÖRT plan sapması, dersler 34-41 ve
     Faz 3'te bulunup düzeltilen ÜÇ kusur burada. En son yazılan faz özeti
     bu — dikkatle oku, §8'i atlama.

7. ...\docs\08-HATA-SOZLESMESI.md
   → Hata sözleşmesi (K20). Faz 1'de uygulandı, HER hata yolunda geçerli.
     Faz 5'te RSVP_QUOTA_EXCEEDED ve RSVP_DEADLINE_PASSED kodları
     kullanılacak — §3.4'teki `params` beyaz listesi kritik.

8. ...\CLAUDE.md
   → Bağlayıcı backend kod standartları.

Okuduktan sonra bana tek paragrafta şunu özetle: hangi fazdayız, Faz 4'te ne
inşa ettik, Faz 5'in ilk dosyası ne ve neden o sırada. Ayrıca Faz 4'te alınan
DÖRT "plandan sapma" kararını da söyle — onları geri almamalısın.

GEREKTİĞİNDE ŞUNLARI DA AÇ:
- docs\07-GELISTIRME-YOL-HARITASI.md   (faz detayları)
- docs\09-TUM-FAZLAR-PLANI.md          (9 fazın tamamı)
- docs\03-MIMARI-PLAN.md               (veri modeli, endpoint tablosu — §8 GEÇERSİZ)
- docs\05-KLASOR-VE-DOSYA-REFERANSI.md (dosya yazarken referans)
- docs\rehber\<kod-yolu>.md            (yazılmış HER backend dosyasının eğitim md'si)
- docs\rehber\kavramlar\               (php-dili · komutlar · veritabani · istek-yasam-dongusu)
- docs\rehber\fazlar\FAZ-4-ELLE-DOGRULAMA.md (15 adım; adım 12 kritik)
- davetkart-frontent\docs\rehber\src\  (10 frontend kılavuzu)
- claude\Notlar\01, 02, 03             (frontend sözleşmesi ve yapılacaklar)

ÇALIŞMA KURALLARIM — bunlara kesinlikle uy:

1. TEK DOSYA KURALI: Bir cevapta asla birden fazla dosya yazma. Sadece
   anlaştığımız sıradaki tek dosyayı veya küçük bir mantıksal modülü yaz.
   (İstisna: açıkça "hepsini tek seferde yaz" dersem.)

2. GEREKÇE ANLAT: Yazdığın her kod için neden o yaklaşımı seçtiğini, hangi
   tasarım desenini kullandığını, güvenlik ve performans açısından ne
   kazandırdığını bir kıdemli mühendis gibi anlat. Amacım kodu kopyalamak
   değil, mimari vizyonu öğrenmek.

3. ONAY BEKLE: Bir dosyayı yazıp anlattıktan sonra DUR. Ben "anladım,
   sıradakine geçelim" veya "şurayı değiştirelim" demeden bir sonraki
   aşamaya geçme.

4. BENİM YERİME GEÇME: Komutları kendi makinemde (Windows + Laravel Herd)
   ben çalıştırıyorum. Bana komutu ver, ne yapacağını açıkla, sonucu bekle.

5. PLANDAN SAPMA: Bir kararın yanlış olduğunu düşünüyorsan önce bana söyle
   ve gerekçesini tartışalım; kendi kararınla plandan sapma.

6. SOLID, Clean Code ve Laravel standartlarına katı bağlı kal.

7. Türkçe, öğrenciye açıklar gibi mantığını açıklayarak yaz. Sıfırdan
   öğreniyormuş gibi anlat ancak mühendislikte kullanılan teknik detayları
   atlama.

8. AÇIKLAMA NEREYE YAZILIR: Kod dosyasına sadece kısa yorum (bir-iki satır).
   Detaylı anlatım docs/rehber/<kod-yolu>/<dosya>.md içine ayrı bir eğitim
   dokümanı olarak yazılır. Kılavuz yolu kod yolunu BİREBİR yansıtır.
   Frontend dosyaları için aynı kural, kendi deposunda:
   davetkart-frontent/docs/rehber/src/<yol>.md
   Kılavuz PHP'yi ilk kez gören biri için yazılır: dil temelleri, tasarım
   kararları, sık yapılan hatalar tablosu, "kendin dene" adımları,
   terim sözlüğü.

9. HER DOSYA İÇİN RİTİM:
   komut ver -> kodu yaz -> kılavuzu yaz -> composer check -> DUR, onay bekle

10. HER ADIM YEŞİL BİTMELİ: Henüz var olmayan bir sınıfa referans verme.
    Bağımlılık sırası dosya yazma sırasını belirler. "Sonra düzelir" diyerek
    kırık bırakma.

11. TAHMİN YÜRÜTME, KAYNAĞA BAK: vendor/ klasörü okunabilir ve senin emrinde.
    Bir aracın hata mesajı BELİRTİYİ söyler, SEBEBİ değil. Framework'ün ne
    yaptığından emin değilsen kaynağı aç — beş dakika sürer, yanlış tahmin
    saatler sürer.

12. HER FAZ SONUNDA: docs/rehber/fazlar/FAZ-N.md özetini ve
    FAZ-N-ELLE-DOGRULAMA.md betiğini yaz, PHP-LARAVEL-SETUP.md'yi ve
    claude/PROMPT.md'yi güncelle, docs/07 ile docs/09'daki faz planına
    "tamamlandı" ve varsa sapmaları işle.

13. 🔴 "YEŞİL GÖRDÜM" DEMEK İÇİN ZİNCİRİN TAMAMI KOŞMUŞ OLMALI.
    composer check fail-fast: pint kırılırsa phpstan, phpstan kırılırsa
    TESTLER HİÇ KOŞMAZ. Faz 2, Faz 3 ve Faz 4'te üç kez "kapandı" sanılan faz
    aslında kapanmamıştı. Bir fazı bitmiş saymadan önce çıktının SON satırına
    (test sayısı) bak, ilk satırına değil.

14. 🔴 BEKLEDİĞİN YANITI ALMAK, BEKLEDİĞİN SEBEPLE ALDIĞIN ANLAMINA GELMEZ.
    Bir test yeşilse "neden yeşil?" diye sor. Faz 3'ün IDOR testleri 404
    bekliyor ve 404 alıyordu — ama Policy'den değil, eşleşmeyen bir rotadan.
    Policy dosyası silinseydi de geçerlerdi. Güvenlik testi yazarken
    MUTASYON sor: "bu korumayı silsem hangi test kırılır?"

Şimdi dosyaları oku ve Faz 5'in ilk dosyasından devam edelim.
```

---

## Kısa sürüm (bağlam sınırlıysa)

```
D:\Projects\davetkart\claude\PHP-LARAVEL-SETUP.md ve
D:\Projects\davetkart\davetkart-backend-php-laravel\docs\rehber\fazlar\FAZ-4.md
dosyalarını oku, DavetKart backend projesine kaldığımız yerden devam et.
Faz 0-1-2-3-4 bitti, sıradaki Faz 5 (RSVP — auth'suz yazma yolu, katmanlı
savunma).

Sen kıdemli yazılım mimarısın, ben öğrenciyim. Kurallar: tek cevapta tek dosya
yaz, her kararın gerekçesini (tasarım deseni + güvenlik/performans) anlat, kod
dosyasına kısa yorum + docs/rehber altına detaylı kılavuz yaz, her adım
composer check yeşil bitsin (çıktının SON satırına bak), sonra DUR ve onayımı
bekle. Komutları ben çalıştırıyorum. Emin olmadığın framework davranışını
vendor/ kaynağından doğrula. Türkçe ve kısa yaz.
```

---

## Durum özeti (prompt'a gerek kalmadan hızlı bakış)

| Konu | Durum |
|---|---|
| **Tamamlanan** | Faz 0 (zemin) · Faz 1 (hata zarfı) · Faz 2 (auth) · Faz 3 (Invitation CRUD) · **Faz 4 (public okuma + cache + ETag)** |
| **Sıradaki** | **Faz 5** — RSVP: auth'suz yazma yolu, katmanlı savunma |
| **Çalışan uç noktalar** | `GET /api/ping` · 4 auth ucu · 5 invitations ucu · **1 public ucu (ETag'li)** |
| **Frontend durumu** | ✅ Dashboard + editör (Faz 3) **ve misafir sayfası** (Faz 4) gerçek backend'e bağlı |
| **Veritabanı** | PostgreSQL 18 · `davetkart` + `davetkart_test` · 2 iş tablosu |
| **Kalite kapısı** | `composer check` = pint --test → phpstan → errors:export --check → test |
| **Test sayısı** | **66** (7 Health + 15 Auth + 19 Invitation + **25 PublicInvitation**) |
| **Karar sayısı** | **48** (K1–K48) |
| **Kural sayısı** | **96** (FAZ-0: 31 · FAZ-1: 19 · FAZ-2: 20 · FAZ-3: 15 · **FAZ-4: 11**) |
| **Ders sayısı** | **41** |
| **Test framework** | PHPUnit (Pest **değil**) |
| **Backend dili** | Tek dil: `en`. Metin değil **hata kodu** döner |
| **Parola hash'i** | Argon2id (K32) |
| **PHPStan seviyesi** | 6 + `parseModelCastsMethod: true` (Faz 5'te level 8 — K22) |
| **Cache** | dev `file` · test `array` · prod Redis. Anahtar: `Invitation::publicCacheKey()` |

---

## Faz 4'te ne inşa edildi? (yeni asistan için 60 saniyelik özet)

**8 backend + 2 frontend dosyası.** Faz 3 *"buna dokunabilir misin?"* sorusunu
çözmüştü; Faz 4 *"kimliği bilinmeyen biri bunun **neyini** görebilir ve bunu
**kaç kere hesaplarız**?"* sorusunu çözdü.

| Dosya | İşi |
|---|---|
| `Actions/Invitation/ResolvePublicInvitationAction.php` | Görünürlük bir `if` değil **sorgunun kapsamı**; `firstOrFail()` → 404 |
| `Resources/PublicTimelineEventResource.php` | Misafir sürümü — `id` **yok** (artan bigint sayım sızıntısı) |
| `Resources/PublicInvitationResource.php` | 🔴 **C6**: kapalı modülün verisi gövdeye **hiç girmez** |
| `Controllers/Api/V1/PublicInvitationController.php` | `string $id` (binding cache'i baypas ederdi) + `Cache::remember` |
| `routes/api.php` → `/api/public/` | K12 fail-safe grubu + `whereUlid` |
| `Http/Middleware/SetEtag.php` | ETag + `304`; RFC 7232 mantığı `isNotModified()`'e bırakıldı |
| `Events/InvitationChanged.php` + `Listeners/ClearInvitationCache.php` | Cache invalidation; kuyruksuz + after-commit |
| `tests/Feature/PublicInvitationTest.php` | **25 test** + mutasyon tablosu |
| Frontend: `services/publicInvitation.ts` · `pages/InvitePage.tsx` | `TODO(backend)` kapandı |

**Çalışan uç noktalar:**

| Method | Path | Yanıt |
|---|---|---|
| GET | `/api/public/invitations/{id}` | `200` · `{data:{id, invitation}}` · **ETag** |
| GET | aynı + `If-None-Match` | `304` · gövde yok |
| GET | yayınlanmamış / silinmiş / hiç yok | `404` · üçü **ayırt edilemez** |

**Faz 4'ün dört kritik fikri:**

1. **İki katman üst üste biner.** Cache *veritabanına gitmeyi*, ETag *gövdeyi
   göndermeyi* önler. Biri diğerinin yerine geçmez.
2. **TTL bir tazelik garantisi değil, üst sınırdır (O3).** Tazeliği olay
   sağlar; TTL yalnızca olayın kaçırıldığı durumlar için emniyet kemeridir.
3. **Ekranda görünmemek ile gönderilmemek farklıdır (C6).** Kapalı modülün
   verisi boş string olarak değil, **anahtar olarak da** yoktur — aksi hâlde
   DevTools açan misafir IBAN'ı okur.
4. **Bir savunmanın neyi kapatmadığını yazmak, kapattığını yazmak kadar
   önemlidir (B6).** ETag ağı kurtarır, CPU'yu değil.

---

## 🔴 Faz 4'te yapılan DÖRT plan sapması — geri alma

Yeni asistan yol haritasında yazanı görüp "düzeltmeye" kalkabilir. Dördü de
tartışılarak, gerekçesiyle yapıldı ve `docs/07` ile `docs/09` bunlara göre
güncellendi.

| Yol haritasında yazan | Yapılan | Neden |
|---|---|---|
| Cache `ResolvePublicInvitationAction` içinde (`Cache::remember`) | Cache **controller'da**, Resource çıktısı olan **dizi** üzerinde (K45) | Action saf ve cache'siz test edilebilir kalır; cache'te serileşmiş Eloquent modeli şema değişince bayat nesne canlandırır; ETag aynı diziden hesaplanır |
| `Events/InvitationPublished` | `Events/InvitationChanged` (K48) | Yayın akışı Faz 7'de; `InvitationPublished`'ı bugün fırlatan kod yok → üç faz boyunca **ölü kod** olurdu. Cache'i bugün bayatlatan şey autosave güncellemesi ve silme |
| Tek `PublicInvitationResource` | + `PublicTimelineEventResource` (4.2a) | Misafire artan bigint kimlik gitmemeli — K40'ın ULID ile kapattığı sayım sızıntısı arka kapıdan geri gelirdi (C5) |
| Cache testleri uçtan uca | Zincir **üç halkaya** bölündü (T15) | `RefreshDatabase` her testi rollback ediyor; `ShouldHandleEventsAfterCommit` dinleyicisi hiçbir testte koşmuyor. Testi yeşile döndürmek için arayüzü kaldırmak = gerçek bir yarış koşulunu geri getirmek |

---

## 🔴 Faz 4'ün devrettiği riskler ve borçlar

Yeni asistan Faz 5'e başlamadan önce bunları bilmeli:

| Konu | Durum | Nerede kapanacak |
|---|---|---|
| **Genel API hız sınırı yok** | `/api/public/...` sınırsız; ayrıca **404'ler cache'lenmiyor**, rastgele ULID yağdıran biri her istekte bir sorgu açtırıyor | **Faz 5.8** — `throttleApi` + RSVP limitleri |
| **`event_at` saat dilimi** | Duvar saati saklanıyor (`Y-m-d\TH:i`). Berlin'deki misafirin geri sayımı kayıyor. Doğru çözüm `invitations.timezone` kolonu + iki alan | **Faz 5'te karara bağlanmalı** (Faz 4'te bilinçli ertelendi) |
| **Cache invalidation testte doğrulanamıyor** | `FAZ-4-ELLE-DOGRULAMA.md` **adım 12** tek kanıt. Faz 5'te aynı sorunu üreten kod yazılırsa aynı çözüm (halkalama) uygulanmalı | Faz 5 testleri |
| **`PublishInvitationAction` boş iskelet** | `make:class` çıktısı, `final` bile değil, kimse çağırmıyor | **Faz 7** — ya doldurulacak ya silinecek |
| **Frontend deposunda CRLF/LF karmaşası** | Çalışma ağacı CRLF, commit'lenmiş blob'lar LF. `git add -A` 473 alakasız dosyayı sürüklüyor — **dosyaları tek tek ekle** | `.gitattributes` kararı İsmail'e ait |

---

## Faz 5'te ne yapılacak?

**Amaç:** Sistemin **auth'suz yazma** yolu — en çok saldırıya açık noktası.
Faz 4 auth'suz *okuma*yı açmıştı; Faz 5 auth'suz *yazma*yı açıyor ve buradaki
tehdit modeli tamamen farklı.

| # | Dosya | Not |
|---|---|---|
| 5.1 | `app/Enums/RsvpStatus.php` | DB İngilizce (`attending\|pending\|declined`), çeviri frontend'de (K21) |
| 5.2 | `..._create_rsvps_table.php` | `ip_hash` (K14), `(invitation_id, status)` indeksi |
| 5.3 | `app/Models/Rsvp.php` | |
| 5.4 | `StoreRsvpRequest` | honeypot alanı |
| 5.5 | `app/Exceptions/RsvpQuotaExceededException.php` | + **`HasErrorCode` arayüzü** — üçüncü exception geldi (H11) |
| 5.6 | `SubmitRsvpAction` | 🔴 deadline + kota + IP hash |
| 5.7 | `RsvpResource` + `RsvpController` | public submit + owner list |
| 5.8 | Rate limit kaydı (`AppServiceProvider`) + **`throttleApi`** | Faz 4'ün borcu burada kapanır |
| 5.9 | `Jobs/SendRsvpNotification` | 15 saniye kuralı — ilk kuyruk işi |
| 5.10 | `tests/Feature/RsvpTest.php` | 🔴 kota `SUM(guest_count)` ile |

**Uç noktalar:**

| Method | Path | Auth |
|---|---|:---:|
| POST | `/api/public/invitations/{id}/rsvps` | — |
| GET | `/api/invitations/{id}/rsvps` | ✅ (ETag'li polling — `SetEtag` yeniden kullanılacak, K46) |
| DELETE | `/api/rsvps/{id}` | ✅ |

**Bitti ölçütü:** Misafir LCV gönderiyor; sahip panelde 15 sn'de bir güncellenen
listeyi görüyor.

### 🔴 Faz 5'in beş kritik noktası

1. **Kota `COUNT(*)` ile değil `SUM(guest_count)` ile.** 100 kayıt × 4 kişi =
   400 misafir demektir; `COUNT(*)` kullanılırsa Standart plan sessizce
   dörde katlanır.
2. **`RSVP_QUOTA_EXCEEDED` → 403, 429 değil (K28).** 429 bir *hız* sınırıdır;
   kotamız *kapasite* sınırıdır. Misafir yavaşlayarak aşamaz.
3. **`remaining`/`limit` parametreleri yalnızca davetiye SAHİBİNE** (08 §3.4).
   Anonim misafir kota durumunu bilmemeli — `ErrorCode::filterParams()` beyaz
   listesi bunu kodda zorluyor.
4. **IP ham saklanmaz (K14).** `hash(ip + app_key)` — KVKK veri
   minimizasyonu. Hash'i üreten yer tek olmalı (C3, tıpkı `publicCacheKey`
   gibi).
5. **Honeypot dolduysa sessizce `200` dön, KAYDETME.** Bota "yakalandın"
   dememek, savunmanın parçasıdır.

### Faz 5'te Faz 4'ten devralınan araçlar

- `/api/public/` grubu hazır — LCV gönderim ucu **oraya** eklenecek (K12)
- `SetEtag` middleware hazır — sahibin polling ucuna takılacak (K46)
- `InvitationChanged` + otomatik keşif hazır — LCV sayacı cache'lenirse ikinci
  bir dinleyici `UpdateInvitationAction`'a dokunmadan eklenebilir
- `Invitation::publicCacheKey()` — ikinci bir anahtar deseni gerekirse örnek
