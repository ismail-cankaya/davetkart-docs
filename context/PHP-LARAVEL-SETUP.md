# DavetKart — Proje Devir Dosyası

> **Bu dosya kimin için:** Bu projeye yeni katılan bir yapay zekâ asistanı veya
> geliştirici için. Amaç: geçmiş süreci, alınan kararları ve gerekçelerini
> sıfırdan anlatmadan aktarmak.
>
> **İlk yapılacak:** Bu dosyayı baştan sona okuyun. Bölüm 2 çalışma kurallarını,
> Bölüm 9 "şu an neredeyiz", Bölüm 10 "sırada ne var" sorusunu cevaplar.
>
> **Son güncelleme:** 23 Eylül 2026 (backend "bitti" gözden geçirmesi)
> **Durum:** **Faz 0-4 ✅ doğrulandı** · **Faz 5-8 kod ✅ / elle doğrulama ⬜** ·
> **Faz 9 kod ✅ · `composer check` YEŞİL (238 test, 11 Eylül) / elle doğrulama ⬜** ·
> **Faz 9 sonrası eklemeler (17–21 Eylül) kod ✅ / `composer check` kayıt yok** ·
> **Frontend yakalama F1–F7 ✅ (13–16 Eylül)**
> **Sıradaki:** 🔴 `davetkart-backend-php-laravel/claude/GOZDEN-GECIRME-RAPORU.md`
> §1'deki iki kritik bulgu → `composer check` → Faz 5-9 + frontend F8 elle
> doğrulama → ödeme sağlayıcısı (**Shopier**).
>
> ---
>
> ### 🔴 YENİ ASİSTAN — bu dosya bir yerde eskiyor, oku
>
> Bu dosya **Faz 4 sonunda** yazıldı. Faz 5, 6 ve 7'nin kararları/dersleri
> **ayrı yama dosyalarında** birikti ve buraya **kısmen** işlendi:
>
> | Bölüm | Durum |
> |---|---|
> | §7 Karar Kaydı | ✅ **K64–K71 (Faz 7) işlendi**; K49–K63 ve K72–K86 hâlâ EK dosyalarında |
> | §9 Teknik Durum · §10 Yol Haritası · §15 Açık Sorular | ✅ **Faz 9'a göre güncellendi** |
> | Faz 5, 6, 8 ve 9'un kararları, kuralları ve dersleri | 🔴 **hâlâ işlenmedi** — EK dosyalarında |
>
> **Bu yüzden okuma sırası şudur:**
>
> ```
> 0. davetkart-backend-php-laravel/claude/GOZDEN-GECIRME-RAPORU.md ← 🔴 23 Eylül: açık bulgular
> 1. Bu dosya (bağlam, kararlar, çalışma kuralları)
> 2. davetkart-backend-php-laravel/claude/FAZ-9-DEVIR.md   ← EN GÜNCEL DEVİR (23 Eylül'de güncellendi)
> 3. .../claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md   (K49-K53, L1-L4, dersler 42-47)
> 4. .../claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md   (K54-K63, F1-F5, dersler 48-49)
> 5. .../claude/PHP-LARAVEL-SETUP-EK-FAZ-7.md   (K64-K71, M5-M8, W1-W3, dersler 50-55)
> 6. .../claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md   (K72-K79, Q1-Q4/X1-X3/L8/C8/B9, dersler 56-59)
> 7. .../claude/PHP-LARAVEL-SETUP-EK-FAZ-9.md   (K80-K86, B10/E12, dersler 60-64)
> ```
>
> Bir çelişki görürsen **daha yeni olan kazanır**: EK dosyaları > bu dosya.

---

## 1. Proje Nedir?

**DavetKart** — dijital davetiye (e-davetiye) SaaS platformu. Kullanıcılar düğün,
kına, nişan, sünnet, doğum günü, mezuniyet, baby shower ve parti için davetiye
tasarlar, ödeme yapıp yayınlar; misafirler paylaşılan linkten davetiyeyi görüp
LCV (katılım yanıtı) gönderir.

**Ticari model:** Ücretsiz katman **yok**. Yayınlamak için tek seferlik plan
satın alınır:

| Plan | Fiyat | Açtığı modüller |
|---|---|---|
| Standart | 249 ₺ | Temel + harita + sayaç + **max 100 kişi LCV** |
| Gold | 399 ₺ | + zarf animasyonu, zaman çizelgesi, sınırsız LCV |
| Elit | 549 ₺ | + galeri, hediye/IBAN modülü, logosuz yayın |

**Frontend:** React 19 + TypeScript. Çalışır durumda, **aktif olarak
geliştirilmeye devam ediyor**. Backend **sıfırdan yazılıyor**.

---

## 2. Kullanıcı Profili ve Çalışma Kuralları 🔴

- **Bilgisayar mühendisliği 3. sınıf öğrencisi**, adı **İsmail**
- Frontend'i **kendisi yazmadı** — devraldı, ama artık üzerinde çalışıyor
- **Amacı sadece çalışan kod değil, mimari vizyonu öğrenmek**
- PHP/Laravel'e **yeni**; React/TypeScript'e aşina
- Windows + **Laravel Herd**, komutları kendi makinesinde kendisi çalıştırıyor

### İhlal edilmemesi gereken kurallar

1. **TEK DOSYA KURALI.** Bir cevapta asla birden fazla dosya yazma. Sadece
   anlaşılan sıradaki tek dosyayı veya küçük bir mantıksal modülü yaz.
2. **GEREKÇE ANLAT.** Her kod için: neden bu yaklaşım, hangi tasarım deseni,
   güvenlik/performans açısından ne kazandırıyor.
3. **ONAY BEKLE.** Dosyayı yazıp anlattıktan sonra **DUR**.
4. **KULLANICININ YERİNE GEÇME.** Komutları o çalıştırıyor. Komutu ver,
   ne yapacağını açıkla, sonucu bekle.
5. **PLANDAN SAPMA.** Bir kararın yanlış olduğunu düşünüyorsan önce söyle ve
   tartış; kendi kararınla plandan sapma.
6. Türkçe, kısa ve doğrudan yaz.
7. SOLID, Clean Code ve Laravel standartlarına katı bağlı kal.

### 🔴 Açıklama nereye yazılır? (K18)

Uzun blok yorumlar kod dosyalarında **istenmiyor**.

| Nerede | Ne kadar |
|---|---|
| Kod dosyası | **Kısa** yorum — bir-iki satır |
| `docs/rehber/...` | **Detaylı eğitim dokümanı** — her kod dosyası için bir `.md` |
| `docs/rehber/fazlar/` | **Faz özeti** — hedefler, kurallar, devir |

Kılavuz yolu, kod yolunu **birebir** yansıtır:

```
config/davetkart.php                     → docs/rehber/config/davetkart.md
app/Enums/SubscriptionTier.php           → docs/rehber/app/Enums/SubscriptionTier.md
app/Providers/AppServiceProvider.php     → docs/rehber/app/Providers/AppServiceProvider.md
pint.json                                → docs/rehber/pint.md
```

Kılavuz **PHP'yi ilk kez gören biri** için yazılır: dil temelleri, Laravel'in o
dosyayı nasıl kullandığı, her kararın hangi iş kuralını veya saldırıyı çözdüğü,
**sık yapılan hatalar** tablosu, deneme adımları, **terim sözlüğü**.

---

## 3. Teknoloji Yığını

### Çekirdek

| Katman | Teknoloji | Sürüm |
|---|---|---|
| Dil | PHP | **^8.5** (20 Eylül 2026; önceden 8.3+) |
| Hata izleme | Sentry (`sentry/sentry-laravel`) | ^4.27 (21 Eylül 2026) |
| Framework | Laravel | 13.x |
| ORM | Eloquent (Active Record) | — |
| Kimlik doğrulama | Laravel Sanctum | 4.x |
| Yerel ortam | Laravel Herd (ücretsiz) | — |

### Veri

| Konu | Geliştirme | Test | Üretim |
|---|---|---|---|
| Veritabanı | **PostgreSQL 18** (`davetkart`) | **PostgreSQL 18** (`davetkart_test`) | **PostgreSQL 18** |
| Cache | file | array | Redis 7 |
| Kuyruk | database | sync | Redis 7 |
| Dosya | local disk | fake | S3 uyumlu |

> PostgreSQL pgAdmin 4 ile yönetiliyor; `psql` PATH'te değil, gerekmiyor.

### Kalite araçları — Faz 0'da kuruldu

| Araç | Sürüm | Komut |
|---|---|---|
| **Laravel Pint** | 1.27 | `composer lint` |
| **Larastan / PHPStan** | 3.10 / 2.2 | `composer analyse` |
| **PHPUnit** | 12.5 | `php artisan test` |
| **Hepsi** | — | **`composer check`** ← faz bitiş kapısı |

> 🔴 **Test framework'ü PHPUnit'tir, Pest DEĞİL.** Eski planda Pest yazıyordu;
> PHPUnit Laravel 13 ile zaten geliyor ve xUnit deseni evrensel olduğu için
> öğrenme değeri yüksek. Pest sonradan eklenebilir, ikisi yan yana çalışır.

### Kullanılmayacaklar

| Teknoloji | Neden hayır |
|---|---|
| Repository Pattern | Eloquent zaten Active Record; anlamsız aracı üretir (K4) |
| Clean Architecture / DDD | Soyutlama bütçesi; en karmaşık iş kuralı 3 satır (K15) |
| Mikroservis | Tek geliştirici, tek sunucu (K2) |
| Laravel Reverb / WebSocket | Ayrı daemon + RAM; Polling + ETag yeterli (K7) |
| Inertia / Blade / Livewire | Frontend ayrı çalışıyor; backend saf API |
| `app/Modules/` klasör yapısı | Aşırı mühendislik; katman-bazlı klasörleme yeterli |
| Backend i18n (çoklu dil) | Backend tek dil konuşur (K21) |

---

## 4. Dizin Haritası

```
D:\Projects\davetkart\
│
├── claude\                                   📓 BAĞLAM REPO'SU (ayrı git deposu)
│   ├── PHP-LARAVEL-SETUP.md                  ⭐ BU DOSYA — önce beni oku
│   ├── PROMPT.md                             yeni sohbet başlangıç prompt'u
│   └── Notlar\
│       ├── 01-FRONTEND-ANALIZI.md
│       ├── 02-FRONTEND-BACKEND-TEMAS-NOKTALARI.md
│       └── 03-FRONTEND-YAPILACAKLAR.md       🔴 K20 sonrası frontend işi
│
├── davetkart-frontent\                       ✅ Yakalama fazı F1–F7 tamamlandı (13–16 Eylül 2026)
│   ├── src\
│   │   ├── types.ts                          ⭐ API sözleşmesinin kaynağı
│   │   ├── data.ts                           plan fiyatları
│   │   ├── i18n.ts                           i18next, 10 dil, fallbackLng: 'en'
│   │   ├── services\                         ⭐ backend sınırları (7 dosya)
│   │   │   └── api.ts                        axios, baseURL '/api', 15 sn timeout
│   │   ├── stores\useSubscriptionStore.ts    getRequiredTier() — paywall ikizi
│   │   └── locales\                          10 dil (tr,en,ar,de,es,fr,hi,pt,ru,zh)
│   ├── vite.config.ts                        ⭐ /api → localhost:8000 proxy
│   ├── docs\rehber\src\                       Faz 3 — 8 frontend kılavuzu
│   └── CLAUDE.md                             frontend kod standartları
│
├── davetkart-backend-php-laravel\            🔨 AKTİF BACKEND
│   ├── CLAUDE.md                             ⭐ bağlayıcı kod standartları
│   ├── claude\                               🔴 FAZ DEVİR DOSYALARI (bu depoda!)
│   │   ├── GOZDEN-GECIRME-RAPORU.md          🔴 23 Eylül — tam gözden geçirme, açık bulgular
│   │   ├── FAZ-9-DEVIR.md                    ⭐ EN GÜNCEL DEVİR
│   │   ├── FAZ-7/6/5-DEVIR.md                tarihsel
│   │   ├── PHP-LARAVEL-SETUP-EK-FAZ-5…9.md   🔴 master'a işlenmeyi bekleyen yamalar
│   │   └── PROMPT-FAZ-*.md                   tarihsel başlangıç prompt'ları
│   ├── pint.json · phpstan.neon · phpunit.xml
│   ├── composer.json                         lint / analyse / check scriptleri
│   ├── .env · .env.example
│   │
│   ├── app\
│   │   ├── Actions\Auth\                            Faz 2 — 3 action
│   │   ├── Actions\Invitation\                      Faz 3 + Faz 4 + 🆕 Faz 7 (Publish…)
│   │   ├── Actions\Rsvp\                            Faz 5 + Faz 6 (ResolveOpen…)
│   │   ├── Actions\Media\                           Faz 6 — 2 action
│   │   ├── Actions\Payment\                         🆕 Faz 7 — StartCheckout · HandleCallback · CheckoutResult
│   │   ├── Contracts\                               🆕 Faz 5 + 7 — RsvpQuotaResolver · PublishEntitlementResolver
│   │   ├── Services\Payment\                        🆕 Faz 7 — PaymentGateway · FakeGateway · 2 DTO
│   │   ├── Services\Pricing\                        🆕 Faz 7 — TierResolver · OrderEntitlementResolver
│   │   ├── Services\Rsvp\                           Faz 5 → 🆕 Faz 7 (SubscriptionRsvpQuotaResolver)
│   │   ├── Console\Commands\ExportErrorCodes.php    Faz 1
│   │   ├── Enums\ErrorCode.php                      Faz 1 — 19 kod
│   │   ├── Enums\InvitationStatus.php               Faz 3 — saved | published
│   │   ├── Enums\SubscriptionTier.php               Faz 0 — ✅ Faz 7'de NİHAYET kullanıldı
│   │   ├── Enums\OrderStatus.php                    🆕 Faz 7 — durum makinesi
│   │   ├── Exceptions\ApiExceptionRenderer.php      Faz 1 — K20 zarfı
│   │   ├── Http\Controllers\Api\V1\                 Health · Auth · Invitation
│   │   ├── Events\InvitationChanged.php             🔴 Faz 4 — K48
│   │   ├── Listeners\ClearInvitationCache.php       🔴 Faz 4 — O4, O5
│   │   ├── Http\Middleware\ForceJsonResponse.php    Faz 1
│   │   ├── Http\Middleware\SetEtag.php              Faz 4 — RFC 7232
│   │   ├── Http\Requests\{Auth,Invitation}\         Faz 2 · Faz 3
│   │   ├── Http\Resources\                          User · Invitation · Public* ailesi
│   │   ├── Models\{User,Invitation,TimelineEvent,Rsvp,Media,Order}.php
│   │   ├── Policies\{InvitationPolicy,RsvpPolicy}.php  🔴 Faz 3/5 — IDOR · publish() Faz 7
│   │   └── Providers\AppServiceProvider.php
│   │
│   ├── bootstrap\app.php                     middleware kaydı + exception handler
│   ├── routes\api.php                        ping · auth · invitations · public
│   ├── tests\TestCase.php                    🔴 forgetAuthState() — T13
│   ├── tests\Feature\ + tests\Unit\          23 Eylül: 274 test metodu (Paywall 51 · Media 41 · Rsvp 29 ·
│   │                                          PublicInvitation 27 · Assistant 21 · OptimizeUploadedImage 19 · …)
│   │
│   ├── config\  (15 dosya)                   davetkart · payment · ai · hashing…
│   ├── contracts\error-codes.json            🔴 K33 — errors:export çıktısı, REPODA
│   │
│   ├── docs\
│   │   ├── 03-MIMARI-PLAN.md                 veri modeli + endpoint tablosu
│   │   ├── 05-KLASOR-VE-DOSYA-REFERANSI.md   dosya yazarken referans
│   │   ├── 07-GELISTIRME-YOL-HARITASI.md     ⭐⭐ GÜNCEL PLAN — 9 faz
│   │   ├── 08-HATA-SOZLESMESI.md             🔴 K20 — hata kodu sözleşmesi
│   │   ├── 09-TUM-FAZLAR-PLANI.md            ⭐ 9 fazın özeti + detayı
│   │   └── rehber\                           her kod dosyasının eğitim md'si
│   │       ├── fazlar\FAZ-0.md               ⭐ 31 kural
│   │       ├── fazlar\FAZ-1.md               ⭐ 19 yeni kural + K25-K34
│   │       ├── env.md · pint.md · phpstan.md · phpunit.md
│   │       ├── bootstrap\app.md · routes\api.md
│   │       ├── config\  (14 dosya)
│   │       └── app\  (Enums, Exceptions, Http, Console, Providers)
│   │
│   └── database\ lang\en\ storage\ vendor\
│
└── scaffold-structure.ps1                    işlevsiz (make:* yeterli)
```

> Frontend ile backend arasında **tip paylaşımı yapılmıyor**. Sözleşme,
> `davetkart-frontent\src\types.ts` referans alınarak elle korunuyor.

---

## 5. Doküman Haritası

| # | Dosya | İçerik | Ne zaman aç |
|---|---|---|---|
| **07** | `docs\07-GELISTIRME-YOL-HARITASI.md` | ⭐⭐ **GÜNCEL PLAN.** 9 faz, faz başına dosya listesi ve "bitti" ölçütü | **Her oturum başında** |
| **08** | `docs\08-HATA-SOZLESMESI.md` | 🔴 Hata zarfı, kod kataloğu, güvenlik kuralları | **Her hata yolu yazımında** |
| **F0** | `docs\rehber\fazlar\FAZ-0.md` | ⭐ Faz 0 özeti + **31 kural** (Y/V/K/T/S/H/B serileri) | Kural aramak için |
| **F1** | `docs\rehber\fazlar\FAZ-1.md` | ⭐ Faz 1 özeti + **19 yeni kural** (H10-13, R1-5, M1-4, T6-9, G1-3) + K25-K31 | Kural aramak için |
| **F2** | `docs\rehber\fazlar\FAZ-2.md` | ⭐ Faz 2 özeti + **20 yeni kural** (A1-7, D1-5, E1-5, C1-3, T10-12, B4) + K35-K36 | Kural aramak için |
| **F2E** | `docs\rehber\fazlar\FAZ-2-ELLE-DOGRULAMA.md` | 13 adımlık elle doğrulama betiği | Uç noktaları elle sınarken |
| **F3** | `docs\rehber\fazlar\FAZ-3.md` | ⭐ Faz 3 özeti + **kronoloji** + **15 yeni kural** (P1-4, N1-4, D6, E6, C4-5, T13-14, B5) + K37-K44 | Kural aramak için |
| **F3E** | `docs\rehber\fazlar\FAZ-3-ELLE-DOGRULAMA.md` | 14 adımlık elle doğrulama + uçtan uca tarayıcı senaryosu | Faz 3'ü elle sınarken |
| **F4** | `docs\rehber\fazlar\FAZ-4.md` | ⭐ Faz 4 özeti + **kronoloji** + **11 yeni kural** (O1-O6, R6, E7, C6, T15, B6) + K45-K48 + dersler 34-41 | Kural aramak için |
| **F4E** | `docs\rehber\fazlar\FAZ-4-ELLE-DOGRULAMA.md` | 🔴 15 adım. **Adım 12** testin kapatamadığı boşluğu kapatır | Faz 4'ü elle sınarken |
| **F5** | `docs\rehber\fazlar\FAZ-5.md` | Faz 5 özeti + **10 yeni kural** (L1-4/E8-9/C7/P5/T16/B7) + K49-K53 + dersler 42-47 | Kural aramak için |
| **F6** | `docs\rehber\fazlar\FAZ-6.md` | Faz 6 özeti + **11 yeni kural** (F1-5/L5-6/A8/T17/E10/B8) + K54-K63 + dersler 48-49 | Kural aramak için |
| **F7** | `docs\rehber\fazlar\FAZ-7.md` | ⭐ Faz 7 özeti + **10 yeni kural** (M5-8/W1-3/L7/P6/E11) + K64-K71 + dersler 50-55 + 🔴 **§9 açık kararlar** | Kural aramak için |
| **F7E** | `docs\rehber\fazlar\FAZ-7-ELLE-DOGRULAMA.md` | 🔴 20 adım. **Adım 0** Faz 6'nın kapanış listesi | Faz 7'yi kapatırken |
| **GR** | `davetkart-backend-php-laravel\claude\GOZDEN-GECIRME-RAPORU.md` | 🔴 **23 Eylül 2026** — backend bitti gözden geçirmesi, bulgular + frontend sözleşme tablosu | **Her oturum başında** |
| **D9** | `davetkart-backend-php-laravel\claude\FAZ-9-DEVIR.md` | ⭐⭐ **EN GÜNCEL DEVİR** (23 Eylül'de güncellendi) — yeni asistan buradan başlar | **Her oturum başında** |
| **F8/F9** | `docs\rehber\fazlar\FAZ-8.md` · `FAZ-9.md` (+ `-ELLE-DOGRULAMA`) | Faz 8/9 özetleri, K72-K86 | Kural aramak için |
| **10** | `docs\10-URETIM-ENV-SABLONU.md` | Üretim `.env` şablonu + kurulum sırası | Sunucu kurarken |
| **11** | `docs\11-PROJE-TARIHCESI-VE-IS-AKISLARI.md` | Uçtan uca giriş; Ek A = 22 uçluk harita | İlk okuma |
| ~~D7~~ | `…\FAZ-7-DEVIR.md` | Tarihsel | — |
| **FE** | `davetkart-frontent\docs\rehber\src\` | Frontend kılavuzları (8 dosya) — K18 aynı kuralla | Frontend kodunu anlamak |
| **KV** | `docs\rehber\kavramlar\` | ⭐ `php-dili.md` · `komutlar.md` · `veritabani-ve-migration.md` · `istek-yasam-dongusu.md` | Dil/araç/kavram öğrenirken |
| **09** | `docs\09-TUM-FAZLAR-PLANI.md` | 9 fazın tek dokümanda özeti ve detayı | "Toplamda ne geliştireceğiz?" |
| **03** | `docs\03-MIMARI-PLAN.md` | Tablo şemaları, endpoint tablosu. ⚠️ §8'deki 12 adım **geçersiz** | Veri modeli tasarımı |
| **05** | `docs\05-KLASOR-VE-DOSYA-REFERANSI.md` | "Bu kodu nereye koymalıyım" karar ağacı | Yeni dosya yazarken |
| — | `docs\rehber\` | Yazılmış her kod dosyasının eğitim dokümanı | Bir dosyanın *neden* öyle olduğunu anlamak |
| **01** | `claude\Notlar\01-FRONTEND-ANALIZI.md` | Frontend'den türetilen API sözleşmesi | Sözleşme detayı |
| **02** | `claude\Notlar\02-FRONTEND-BACKEND-TEMAS-NOKTALARI.md` | Backend'e dokunan 24 frontend dosyası | "Frontend burada ne bekliyor?" |
| **03N** | `claude\Notlar\03-FRONTEND-YAPILACAKLAR.md` | 🔴 K20 sonrası frontend'e düşen iş | Frontend tarafına geçince |
| **04** | `docs\04-KURULUM-VE-KLASOR-YAPISI.md` | ⚠️ MySQL/SQLite atıfları **eskimiş** | Ortam sorunları |
| **06** | `docs\06-PHP-LARAVEL-HERD-NASIL-CALISIR.md` | PHP/Composer/Laravel/Herd kavram ayrımı | Ortam kavramları |
| — | `davetkart-backend-php-laravel\CLAUDE.md` | ⭐ Bağlayıcı kod standartları | **Her kod yazımında** |

---

## 6. 🔴 Terim Uyarısı — iki ayrı eksen

"Yatay / dikey mimari" terimleri literatürde **iki farklı anlamda** kullanılır.

**Eksen A — Klasörleme:** Dosyalar neye göre gruplanır?

| Katman-bazlı | Özellik-bazlı |
|---|---|
| `app/Http/Controllers/`, `app/Models/`, `app/Actions/` | `app/Modules/Auth/`, `app/Modules/Payment/` |

→ **Seçimimiz: katman-bazlı.** Modül sınırları alt klasör disipliniyle korunur:
`app/Actions/Auth/`, `app/Actions/Invitation/`…

**Eksen B — İnşa sırası:** Dosyalar hangi sırayla yazılır?

| Katman-katman | Özellik-özellik |
|---|---|
| Tüm migration'lar → tüm modeller → tüm controller'lar | Auth'un tüm katmanları → Invitation'ın tüm katmanları |

→ **Seçimimiz: özellik-özellik** (walking skeleton).

> **"Modüler Monolit"** bizde bir **dağıtım** kararıdır ("mikroservis değil"),
> klasörleme kararı değil. Literatürdeki *"Vertical Slice Architecture"*
> Eksen A'nın sağ sütunudur — biz onu **yapmıyoruz**.

---

## 7. Karar Kaydı

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K1** | PHP 8.3+ / Laravel 13 | Hızlı geliştirme; frontend zaten Laravel'e göre yapılandırılmış | ✅ Uygulandı · ⚠️ 20 Eylül 2026'da `composer.json` `^8.5`'e çıktı — gerekçesi kayda geçmedi, `phpstan.neon` `80300` kaldı (rapor) |
| **K2** | **Modüler Monolit** (mikroservis değil) | Tek geliştirici + tek sunucu. Conway Yasası | ✅ Kabul |
| **K3** | Katmanlı + **Action tabanlı** uygulama katmanı | Controller şişmesini önler, iş kuralı HTTP'siz test edilebilir (SRP) | ✅ Kabul |
| **K4** | **Repository Pattern KULLANILMAYACAK** | Eloquent zaten Active Record; üstüne konan repository anlamsız aracı üretir (YAGNI) | ✅ Kabul |
| **K5** | **Laravel Sanctum** (JWT değil) | `useAuthStore.logout()` **sunucu tarafında token iptali** bekliyor | ✅ Uygulandı |
| **K6** | **Hibrit veri modeli** | `show_*` bayrakları ayrı kolon (paywall'ı SQL ile doğrulamak için), `gift_options` JSON | ✅ Faz 3 |
| **K7** | Canlı LCV için **Polling + ETag** | Reverb/WebSocket ayrı daemon + RAM demek | ✅ ETag Faz 4'te; polling Faz 5 |
| **K8** | **`PaymentGateway` arayüzü + `FakeGateway`** | Sağlayıcı anlaşması beklenmeden doğru akış kurulur. Strategy Pattern | ✅ **Faz 7** |
| **K9'** | Üretimde **PostgreSQL 18** | MySQL 8'in yüksek RAM tabanı; PostgreSQL'de `jsonb` + güçlü kısıt desteği | ✅ Uygulandı |
| **K10** | API versiyonu **URL'de değil, namespace'te** | Frontend `baseURL = '/api'`; `/api/v1/...` yazarsak frontend **anında kırılır** | ✅ Faz 1 (`Api\V1\HealthController`) |
| **K11** | Başarı zarfı **ikili kural** | Auth endpoint'leri **zarfsız** `{user, token}`; diğerleri `{data: ...}` | 📋 Faz 2'de uygulanacak |
| **K12** | Auth'suz rotalar **`/api/public/`** öneki altında | `auth:sanctum` unutma riskini yapısal olarak kaldırır — fail-safe | ✅ Faz 4 |
| **K13** | Public ID olarak **ULID** | Ardışık integer'da misafir `/invite/1,2,3` gezer. ULID tahmin edilemez ama zaman sıralı | ✅ Faz 3 (K40 ile netleşti) |
| **K14** | IP adresleri **hash'lenerek** saklanır | KVKK/GDPR veri minimizasyonu. `hash(ip + app_key)` | ✅ Faz 5 · ✅ **Faz 8'de birleşti**: tek kaynak `App\Support\IpHasher::hash()` = `hash_hmac('sha256', ip, app.key)` (LCV + iletişim) |
| **K15** | **Tam Clean Architecture / DDD YAPILMAYACAK** | Soyutlama bütçesi. Bütçe gerçekten değişecek yerlere harcanır | ✅ Kabul |
| **K16** | Klasörler **`php artisan make:*`** ile üretilir | Klasörü açar + namespace'i doğru yazar | ✅ Uygulanıyor |
| **K17** | **Özellik-özellik inşa** (9 faz) | Öğrenme hedefi: katmanların birlikte çalıştığını erken görmek | ✅ Kabul |
| **K18** | Kodda **kısa yorum**, detay `docs/rehber/` altında | Kodun okunur kalması + öğrenme içeriğinin aranabilir olması | ✅ Uygulanıyor |
| **K19** | **Geliştirme ve testte de PostgreSQL 18** | Dev/prod parity (12-Factor X) | ✅ Uygulandı |
| **K20** | 🔴 **Hata sözleşmesi** — API metin değil **kod** döner | Sunum kararı frontend'in işi. Metin dönerse dil backend'e sızar, test metne bağlanır, bilgi ifşası artar | ✅ **Faz 1'de uygulandı** |
| **K21** | **Backend tek dil konuşur** (`APP_LOCALE=en`) | Frontend 10 dili i18next ile zaten taşıyor. K20'nin doğal sonucu | ✅ Uygulandı |
| **K22** | PHPStan seviyesi **kademeli**: 5 → Faz 2'de 6 → Faz 5'te 8 | Seviye 9'dan başlamak yüzlerce hata döker, geliştirici aracı kapatır | ✅ Takvim belirlendi |
| **K23** | Tarihler **`CarbonImmutable`** | Mutable Carbon'da `$d->subDays(3)` orijinali bozar. LCV son tarihinde bu, yanlış kişiye "süre doldu" demektir | ✅ Uygulandı |
| **K24** | Test framework'ü **PHPUnit** (Pest değil) | Laravel 13 ile zaten geliyor; xUnit deseni evrensel, öğrenme değeri yüksek | ✅ Uygulandı |
| **K25** | JSON zorlaması **middleware ile**, `shouldRenderJsonWhen` ile değil | Alternatif `api/*` **URL desenine** dayanır; kök seviyede rota açılınca tahmin sessizce yanlışlanır. Middleware **grup üyeliğine** bağlıdır | ✅ Faz 1 |
| **K26** | Hata zarfı mantığı **ayrı sınıfta** (`ApiExceptionRenderer`) | `bootstrap/app.php` kablolamadır. Ayrı sınıf birim testi + PHPStan kazandırır; yeni exception eklemek bootstrap'a dokunmaz | ✅ Faz 1 |
| **K27** | `PAYMENT_PROVIDER_ERROR` → **502**, `PROVIDER_UNAVAILABLE` → **503** | RFC 9110: yukarı akış hatalı yanıt döndüyse 502. 503 "bu sunucu çöktü" der, izleme alarmını yanlış yönlendirir | ✅ Faz 1 |
| **K28** | `RSVP_QUOTA_EXCEEDED` → **403** (429 değil) | 429 bir **hız** sınırıdır; kotamız **kapasite** sınırıdır. Misafir yavaşlayarak aşamaz | ✅ Faz 1 |
| **K29** | **RFC 9457 (Problem Details) kullanılmaz** | `title`/`detail` insan-okunur metin zorunlu kılar — K20'nin yasakladığı şey | ✅ Faz 1 |
| **K30** | Rota dosyasında **closure yok**, controller referansı | `route:cache` (Faz 9) closure'ları serileştiremez. Maliyet aynıyken erken ödemek ucuz | ✅ Faz 1 |
| **K31** | Katalog senkronizasyonu **tek yönlü üretim + `--check`** | Paylaşılan tip paketi iki repoyu bağımlı kılar. Kopya + doğrulama bağımlılık üretmez | ✅ Faz 1 |
| **K32** | Parola hash'i **Argon2id** (bcrypt değil) | Sadece CPU değil **bellek** de tüketir; GPU/ASIC ile paralel deneme kapasitesini düşürür. Laravel girişte otomatik rehash yapabilir | ✅ Faz 2 girişi |
| **K33** | Katalog **`contracts/error-codes.json`**, repoya işlenir | `--check` zincire girdiği için dosya git'te olmalı. `storage/app/` gitignore'lu, `docs/` eğitim klasörü | ✅ Faz 2 girişi |
| **K34** | `errors:export --check` **`composer check` zincirinde**, testlerden önce | Katalog sessizce eskimez; saniyelik kontrol dakikalık testlerden önce (fail fast) | ✅ Uygulandı |
| **K35** | `users` → **`first_name` + `last_name`**; API'de de **ayrı döner** | Birleştirmek kolay, birleşmiş veriyi ayırmak imkânsız ("Ayşe Nur Kaya" bölünemez). Fatura soyadı tek başına ister (Faz 7). Birleştirme bir **sunum kararıdır** → frontend'e ait | ✅ Faz 2 |
| **K36** | Auth uçlarına **hız sınırı** — Faz 5'ten öne çekildi | Brute-force **ve** K32'nin doğurduğu bellek tüketimi saldırısı (Argon2id = 64 MB × istek). İki limit: 5/dk (e-posta+IP) · 20/dk (IP) | ✅ Faz 2 |
| **K37** | `/api/invitations` **REST koleksiyonu** (upsert değil) | Ticari model çoklu davetiye; `orders.invitation_id` zaten bunu varsayıyor. Frontend'in "hesap başına tek davetiye" varsayımı devralınmış bir hataydı | ✅ Faz 3 |
| **K38** | `InvitationStatus` = **`saved \| published`** | `draft`'ı doğuran olay yok: frontend'de Kaydet düğmesi yok, autosave var. Durum makinesine ancak onu doğuran bir olay varsa durum eklenir | ✅ Faz 3 |
| **K39** | Durum kolonu **`VARCHAR + CHECK`**, native `ENUM` değil | PostgreSQL `ENUM`'da değer eklemek raw `ALTER TYPE` ister, silmek imkânsız. CHECK değerleri `InvitationStatus::values()`'tan beslenir | ✅ Faz 3 |
| **K40** | `invitations.id` = **ULID birincil anahtar**, ayrı slug yok | Frontend `/invite/{record.id}` kullanıyor. ULID tahmin edilemez **ve** zaman sıralı. `timeline_events.id` bigint kalır — URL'de geçmez | ✅ Faz 3 |
| **K41** | `phone_background` **kolon değil**, türetilir | Frontend'de hiçbir yerde okunmuyor, hep `imageTheme` ile aynı. Türetilebilen veri saklanmaz (E1) | ✅ Faz 3 |
| **K42** | Yayın hakkı **iki kaynaktan**, **tek arayüzden** sorulur | Tekil (davetiye başına) **ve** paket satın alma birlikte var. Dağılmış `if` yerine bir arayüz. `orders.invitation_id NULL` = paket alımı | ✅ **Faz 7** — `PublishEntitlementResolver` |
| **K43** | Plan kotası **yayınlananı** sayar, taslağı değil | Kullanıcı 5 tasarım deneyip birini yayınlayabilmeli; kotayı taslağa bağlamak denemenin bedeli olur | ⚠️ **Faz 7'de UYGULANMADI** — paket alımın kaç yayın açtığı sınırsız; açık ticari karar (`FAZ-7.md` §9) |
| **K44** | Kimliği **backend üretir** | Tarayıcı `tl-${Date.now()}` uyduruyordu ve varsayılan `tl-1` **her davetiyede aynıydı**. Sözleşme: `id: null` = yeni satır, `id: "7"` = güncelle. React'in `key` ihtiyacı ayrı `localKey` ile karşılanır | ✅ Faz 3 |
| **K45** | Cache **Action'ın dışında**, Resource çıktısı olan **diziyi** saklar | Action saf ve cache'siz test edilebilir kalır; cache'te bayat Eloquent nesnesi canlanmaz; ETag aynı diziden hesaplanır | ✅ Faz 4 |
| **K46** | ETag **ayrı middleware**, controller içi değil | Faz 5'in LCV polling ucu aynı katmanı yeniden kullanacak (C3); controller HTTP başlık mantığı taşımaz | ✅ Faz 4 |
| **K47** | Faz 4 **salt okuma** kalır; yayın ucu Faz 7'de | Şimdi yazılırsa paywall'sız bir "bedava yayın" yolu açılır ve K42/K43 bozulur. Doğrulama seeder/tinker ile | ✅ Faz 4 |
| **K48** | Olay **`InvitationChanged`**, modelden **yapısal** fırlar | Plandaki `InvitationPublished`'ı bugün fırlatan kod yok (ölü kod); yazma yolu sayısı artıyor ve unutmanın bedeli sessiz | ✅ Faz 4 |

### 🔴 Faz 7'de alınan kararlar (K64–K71)

> K49–K63 (Faz 5 ve 6) bu tabloya **henüz işlenmedi** — bkz.
> `PHP-LARAVEL-SETUP-EK-FAZ-5.md` ve `-EK-FAZ-6.md`.

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K64** | Checkout **iki uç**: `/invitations/{id}/checkout` (tekil) · `/payments/checkout` (paket) | `docs/09` tek uç öngörmüştü; **N1** gereği aidiyet URL'nin **yapısında** durur. Kimlik gövdede olsaydı `exists` kuralı cazip olur ve kimlik uzayı taranabilir hâle gelirdi (A1) | ✅ Faz 7 |
| **K65** | Webhook ucu **`/api/public/`** altında | **K12** fail-safe grubu; `docs/09`'un `/api/payments/webhook` planı ezildi. Auth'suz yüzeyin tamamı tek yerde görünür | ✅ Faz 7 |
| **K66** | `public_slug` **üretilmiyor** | **K40** onu geçersiz kıldı: `invitations.id` zaten ULID ve paylaşılan linkin kendisi. Sonuç: `SLUG_TAKEN` kodu kullanılmıyor ama **silinmiyor** (yayınlanmış kod adı sözleşmedir) | ✅ Faz 7 |
| **K67** | Ödeme **yayınlamaz**; yayın ayrı bir kullanıcı eylemidir | Paket alımda hangi davetiye belirsiz (K42); kullanıcı ödeme ile yayın arasında son düzenleme isteyebilir; webhook bir **makine** bildirimi, yayın bir **insan** kararıdır | ✅ Faz 7 |
| **K68** | "Zaten yayında" → **409**, sessiz başarı değil | Yayın ücretli ve yan etkili; 200 dönmek kullanıcıya iki kez ödediğini düşündürür. (Webhook'ta idempotans **isteniyor** — orada tekrar eden taraf bir makine) | ✅ Faz 7 |
| **K69** | İmza hatası → **404** (401/403/400 değil) | 401 frontend interceptor'ını tetikler + saldırgana sinyal; 403 ucun **varlığını** doğrular; 400 bozuk gövde ile sahte imzayı **ayırt ettirir**. 404 hiçbir ayrım vermez | ✅ Faz 7 |
| **K70** | Sürücü seçimi **çözüm anında**, sessiz varsayılan **yok** | Hatalı config yalnızca ödeme uçlarını kırmalı (blast radius). `default => fake` olsaydı eksik `IYZICO_API_KEY` her ödemeyi **bedava** yapardı | ✅ Faz 7 |
| **K71** | `invitations.timezone` = **duvar saati + IANA kimliği**, `timestamptz` değil | Sorun depolama değil **niyet**: "19:00" düğünün olduğu yerin saatidir. Yaz saati kuralı değişirse `timestamptz` saati **kaydırır**, duvar saati kaydırmaz (iCal `TZID` modeli). K63'ün üç fazlık borcu kapandı | ✅ Faz 7 |

---

## 8. Geçersiz Kılınan Kararlar ⚠️

| Ne | Yerine | Neden |
|---|---|---|
| NestJS + Fastify + Prisma önerisi | **Laravel** | Hız önceliği. `BACKEND-KARAR-RAPORU.md` silindi |
| ~~K9: Üretimde MySQL 8~~ | **PostgreSQL 18** | Düşük RAM tabanı, `jsonb`, güçlü kısıt desteği |
| ~~Geliştirmede SQLite~~ | **PostgreSQL 18** | Dev/prod parity. SQLite'ın gerekçesi "kurulum zahmeti"ydi |
| ~~"SQLite'ta ENUM yok, `string` kolon"~~ | Gerçek `ENUM` veya `CHECK` | PostgreSQL'e geçişle taviz gereksizleşti. Karar **Faz 3'te** |
| ~~`03-MIMARI-PLAN.md` §8 — 12 adımlık sıra~~ | **9 faz** (07) | K17. Aynı dokümanın diğer bölümleri geçerli |
| ~~Pest test framework'ü~~ | **PHPUnit** | K24 |
| ~~`APP_LOCALE=tr`~~ | **`en`** | K21 |
| ~~`lang/tr/validation.php`~~ | Silindi | API metin döndürmüyor (K20) |
| ~~Faz 8 `SetLocaleFromHeader`~~ | İptal | Backend tek dil (K21) |
| ~~Testte SQLite `:memory:`~~ | `davetkart_test` (PostgreSQL) | K19 |
| ~~`davetkart-contracts` TS paketi~~ | `artisan errors:export` JSON'u | Hiç doldurulmadı, kaldırıldı |
| ~~`davetkart-backend\` klasörü~~ | `davetkart-backend-php-laravel\` | Boş klasördü, silindi |

### Frontend `CLAUDE.md` — "Microservices" maddesi

Frontend standartları *"It will communicate with a Microservices backend"* diyor.
**Harfiyen uygulanmıyor.** Doğru okuma: modüller mikroservise *ayrılabilecek
şekilde* sınırlandırılır, ama **tek uygulama olarak deploy edilir** (K2).

---

## 9. Şu Anki Teknik Durum

### ✅ Yazılan kod

| Dosya | Ne yapar | Kılavuzu |
|---|---|---|
| `config/davetkart.php` | Plan fiyatları, kotalar, modül→tier haritası, limitler | `rehber/config/davetkart.md` |
| `config/payment.php` | Ödeme sağlayıcı seçimi, sırlar, webhook imza ayarları | `rehber/config/payment.md` |
| `config/ai.php` | AI sağlayıcı, Gemini anahtarı, timeout, system prompt | `rehber/config/ai.md` |
| `app/Enums/SubscriptionTier.php` | `rank()`, `price()`, `rsvpLimit()`, `covers()` | `rehber/app/Enums/SubscriptionTier.md` |
| `.env` · `.env.example` | PostgreSQL 18, `APP_LOCALE=en`, `CACHE_STORE=file` | `rehber/env.md` |
| `pint.json` | `declare_strict_types` açık, riskli kurallar kapalı | `rehber/pint.md` |
| `phpstan.neon` | Larastan + level 5, `checkModelProperties` | `rehber/phpstan.md` |
| `phpunit.xml` | `davetkart_test`, `array`/`sync`, katılık bayrakları | `rehber/phpunit.md` |
| `app/Providers/AppServiceProvider.php` | Katı model kipi, `CarbonImmutable`, yıkıcı komut engeli | `rehber/app/Providers/AppServiceProvider.md` |
| `composer.json` | `lint` / `analyse` / `check` scriptleri | — |

**Faz 1 (31 Temmuz 2026):**

| Dosya | Ne yapar | Kılavuzu |
|---|---|---|
| `app/Enums/ErrorCode.php` | 19 hata kodu, `status()`, `allowedParams()`, `filterParams()`, `isRetryable()` | `rehber/app/Enums/ErrorCode.md` |
| `app/Http/Middleware/ForceJsonResponse.php` | API her zaman JSON döner (K25) | `rehber/app/Http/Middleware/ForceJsonResponse.md` |
| `app/Exceptions/ApiExceptionRenderer.php` | Exception → K20 zarfı (K26) | `rehber/app/Exceptions/ApiExceptionRenderer.md` |
| `bootstrap/app.php` | Middleware kaydı + handler delegasyonu | `rehber/bootstrap/app.md` |
| `routes/api.php` | `GET /api/ping` | `rehber/routes/api.md` |
| `app/Http/Controllers/Api/V1/HealthController.php` | Sağlık sondası (K30) | `rehber/app/Http/Controllers/Api/V1/HealthController.md` |
| `tests/Feature/HealthTest.php` | 7 test, 3'ü sızıntı testi | `rehber/tests/Feature/HealthTest.md` |
| `app/Console/Commands/ExportErrorCodes.php` | `php artisan errors:export` (K31) | `rehber/app/Console/Commands/ExportErrorCodes.md` |

> `SubscriptionTier` **Faz 7'de** kullanılacak. Erken yazıldı ama doğru duruyor.

**Faz 2 (6 Ağustos 2026) — Auth dilimi:**

| Dosya | Ne yapar | Kılavuzu |
|---|---|---|
| `..._create_users_table.php` | `first_name` + `last_name`, `VARCHAR(60)` (K35) | `rehber/database/migrations/…create_users_table.md` |
| `app/Models/User.php` | `$fillable`, `hashed` cast, `HasApiTokens`, e-posta mutator | `rehber/app/Models/User.md` |
| `database/factories/UserFactory.php` | Test verisi, hash memoization, `PASSWORD` sabiti | `rehber/database/factories/UserFactory.md` |
| `app/Http/Resources/UserResource.php` | `id`→string, `firstName`/`lastName` ayrı, beyaz liste | `rehber/app/Http/Resources/UserResource.md` |
| `Requests/Auth/RegisterRequest.php` | 🔴 `unique` **bilerek yok** (A1) | `rehber/…/RegisterRequest.md` |
| `Requests/Auth/LoginRequest.php` | 🔴 `Password::min` **bilerek yok** (D3) | `rehber/…/LoginRequest.md` |
| `Exceptions/RegistrationFailedException.php` | Sebep kodda açık, yanıtta gizli | `rehber/app/Exceptions/RegistrationFailedException.md` |
| `Exceptions/InvalidCredentialsException.php` | 🔴 **Parametresiz kurucu** — ayrım imkânsız | `rehber/app/Exceptions/InvalidCredentialsException.md` |
| `Actions/Auth/RegisterUserAction.php` | Transaction + UNIQUE kısıtı yakalama (E2, E4) | `rehber/app/Actions/Auth/RegisterUserAction.md` |
| `Actions/Auth/LoginUserAction.php` | 🔴 **Zamanlama savunması** + rehash | `rehber/app/Actions/Auth/LoginUserAction.md` |
| `Actions/Auth/RevokeTokenAction.php` | Yalnızca mevcut token'ı iptal (A6) | `rehber/app/Actions/Auth/RevokeTokenAction.md` |
| `Controllers/Api/V1/AuthController.php` | 4 uç nokta, `session()` yardımcısı (C3) | `rehber/…/AuthController.md` |
| `routes/api.php` | Auth grubu — throttle ve sanctum **ayrı** alt gruplar | `rehber/routes/api.md` |
| `tests/Feature/AuthTest.php` | 14 test, 4'ü güvenlik regresyonu | `rehber/tests/Feature/AuthTest.md` |

**Faz 2'de düzenlenenler:**

| Dosya | Değişiklik |
|---|---|
| `.env` · `.env.example` | `HASH_DRIVER=argon2id` + `ARGON_*` — **K32 nihayet uygulandı** |
| `phpunit.xml` | `ARGON_MEMORY=1024` (test hızı; `BCRYPT_ROUNDS` argon'a etkisiz) |
| `AppServiceProvider.php` | `configureRateLimiting()` (K36) |
| `ApiExceptionRenderer.php` | 2 yeni `match` kolu (H11) |
| `bootstrap/app.php` | `is('api/*') \|\|` düzeltmesi · `use Throwable;` silindi |
| `phpstan.neon` | level 5 → **6** (K22) |
| `docs/03-MIMARI-PLAN.md` | §3.2, §3.3, §4.3 → K35 |

**Faz 3 (19 Ağustos 2026) — Invitation dilimi:**

| Dosya | Ne yapar | Kılavuzu |
|---|---|---|
| `app/Enums/InvitationStatus.php` | `saved \| published`, `default()`, `values()` | `rehber/app/Enums/InvitationStatus.md` |
| `..._create_invitations_table.php` | ULID PK, CHECK, 6 `show_*`, `(user_id,status)` | `rehber/database/migrations/…invitations…md` |
| `..._create_timeline_events_table.php` | `foreignUlid`, `sort_order`, CASCADE | `rehber/database/migrations/…timeline_events…md` |
| `app/Models/Invitation.php` | `HasUlids`, `#[Fillable]`, `immutable_*`, iki ilişki | `rehber/app/Models/Invitation.md` |
| `app/Models/TimelineEvent.php` | `belongsTo`, `sort_order` cast | `rehber/app/Models/TimelineEvent.md` |
| `InvitationFactory` · `TimelineEventFactory` | Deterministik test verisi | `rehber/database/factories/…` |
| `app/Policies/InvitationPolicy.php` | 🔴 IDOR savunması; reddi **404** (H7) | `rehber/app/Policies/InvitationPolicy.md` |
| `Requests/Invitation/{InvitationRequest,Store…,Update…}` | 21 alanlık eşleme, iç içe doğrulama | `rehber/app/Http/Requests/Invitation/…` |
| `Resources/{InvitationResource,InvitationPayloadResource,TimelineEventResource}` | Beyaz liste, iki tarih biçimi | `rehber/app/Http/Resources/…` |
| `Actions/Invitation/{Create…,Update…,SyncTimelineEvents…}` | Transaction + senkronizasyon | `rehber/app/Actions/Invitation/…` |
| `Controllers/Api/V1/InvitationController.php` | 5 uç nokta, `Gate::authorize()` | `rehber/…/InvitationController.md` |
| `routes/api.php` | `apiResource` + ULID rota kısıtı | `rehber/routes/api.md` |
| `tests/Feature/InvitationTest.php` | **18 test**, 5'i sahiplik | `rehber/tests/Feature/InvitationTest.md` |
| `tests/TestCase.php` | 🔴 **yeni** — `forgetAuthState()` (T13) | `rehber/tests/TestCase.md` |

**Faz 3'te düzenlenenler:**

| Dosya | Değişiklik |
|---|---|
| `app/Models/User.php` | `invitations()` ilişkisi |
| `app/Actions/Auth/LoginUserAction.php` | Gereksiz `?->` kaldırıldı (PHPStan) |
| `app/Http/Requests/Auth/RegisterRequest.php` | `Password::min(8)` → `'min:8'` (**D6**) |
| `tests/Feature/AuthTest.php` | `forgetAuthState()` (**T13**) |
| `database/seeders/DatabaseSeeder.php` | 🔴 Faz 2'den beri bozuktu (`name` kolonu yok) — yeniden yazıldı |
| `docs/rehber/…/LoginUserAction.md` · `RegisterRequest.md` · `AuthTest.md` | Yanlış açıklamalar düzeltildi (**B4**) |

**Faz 3 — frontend uyarlaması** (`davetkart-frontent/src/`, 8 dosya):

| Dosya | Değişiklik |
|---|---|
| `types.ts` | `TimelineEvent.id: string \| null` + `localKey` |
| `services/invitations.ts` | REST istemcisi, `Wire*` tipleri, hidrasyon |
| `services/persistence.ts` | Kimlik taşıyan arayüz; sınır düzeltildi |
| `stores/useInvitationStore.ts` | 🔴 `recordId`, kaydetme kuyruğu, `adoptServerIds` |
| `hooks/useDashboardData.ts` | Gerçek dizi + iyimser silme |
| `pages/DashboardPage.tsx` | Kart kaydın tamamını taşır; silme düğmesi |
| `components/create/TimelineEditor.tsx` | `id: null`, `localKey` ile eşleştirme |
| `data.ts` | Varsayılan programın kimlikleri |

**Faz 4 (27 Ağustos 2026) — Public okuma yolu:**

| Dosya | Ne yapar | Kılavuzu |
|---|---|---|
| `Actions/Invitation/ResolvePublicInvitationAction.php` | Görünürlük **sorgunun kapsamında**; `firstOrFail()` → 404 | `rehber/app/Actions/Invitation/ResolvePublicInvitationAction.md` |
| `Resources/PublicTimelineEventResource.php` | Misafir sürümü — `id` **yok** (C5) | `rehber/app/Http/Resources/PublicTimelineEventResource.md` |
| `Resources/PublicInvitationResource.php` | 🔴 **C6**: kapalı modülün verisi gövdeye hiç girmez | `rehber/app/Http/Resources/PublicInvitationResource.md` |
| `Controllers/Api/V1/PublicInvitationController.php` | `string $id` + `Cache::remember` (K45) | `rehber/…/PublicInvitationController.md` |
| `routes/api.php` → `/api/public/` | K12 fail-safe grubu + `whereUlid` | `rehber/routes/api.md` §0.3 |
| `Http/Middleware/SetEtag.php` | ETag + `304`, `isNotModified()` ile (R6) | `rehber/app/Http/Middleware/SetEtag.md` |
| `Events/InvitationChanged.php` | Alan olayı, `readonly` veri kabı | `rehber/app/Events/InvitationChanged.md` |
| `Listeners/ClearInvitationCache.php` | Cache invalidation; kuyruksuz + after-commit | `rehber/app/Listeners/ClearInvitationCache.md` |
| `tests/Feature/PublicInvitationTest.php` | **25 test** + mutasyon tablosu | `rehber/tests/Feature/PublicInvitationTest.md` |

**Faz 4'te düzenlenenler:**

| Dosya | Değişiklik |
|---|---|
| `phpstan.neon` | 🔴 `parseModelCastsMethod: true` — `casts()` metodu Faz 0'dan beri **hiç okunmuyordu** |
| `routes/api.php` | 🔴 Elle yazılmış büyük-harf ULID regex'i → `whereUlid()` (**R6**). Faz 3'te **hiçbir istek eşleşmemişti** |
| `Actions/Invitation/CreateInvitationAction.php` | 🔴 `make()` + açık `status` ataması (**E7**) — `store` uçları 500 veriyordu |
| `app/Models/Invitation.php` | `publicCacheKey()` (C3) + `$dispatchesEvents` (K48) |
| `docs/rehber/phpstan.md` · `routes/api.md` · `CreateInvitationAction.md` · `Invitation.md` | Gerekçeler işlendi |

**Faz 4 — frontend uyarlaması** (`davetkart-frontent/src/`, 2 dosya):

| Dosya | Değişiklik |
|---|---|
| `services/publicInvitation.ts` | **yeni** — public sözleşme `Omit`+`Pick` ile tipte |
| `pages/InvitePage.tsx` | `TODO(backend)` kapandı; 4 durumlu yükleme (loading/ready/missing/error) |

**Faz 2'de yazılan kavram dokümanları** (`docs/rehber/kavramlar/`):

| Doküman | Kapsam |
|---|---|
| `veritabani-ve-migration.md` | Veritabanı mantığı, migration'ın çözdüğü problem |
| `php-dili.md` | ⭐ TS bilenler için PHP referansı — 20 bölüm, tüm örnekler bu projeden |
| `komutlar.md` | Terminal komut referansı |
| `istek-yasam-dongusu.md` | Framework kaynağı üzerinden istek izleme (Bölüm 1/4 yazıldı) |

### ✅ Ortam

```
PostgreSQL 18       davetkart · davetkart_test   (pgAdmin 4 ile yönetiliyor)
Laravel 13.8        Sanctum 4.0, Tinker 3.0
PHP 8.5             Laravel Herd (Windows)   ← composer.json ^8.5 (20 Eylül 2026)
Pint 1.27           composer lint      ← DÜZELTİR
Larastan 3.10       composer analyse   (--memory-limit=1G script içinde)
PHPUnit 12.5        php artisan test
```

**`composer check` zinciri (K34) — sırayla, ilki kırılırsa gerisi koşmaz:**

```
pint --test  →  phpstan  →  errors:export --check  →  php artisan test
   (bakar,          (statik      (katalog güncel      (davranış)
    düzeltmez)       analiz)      mi?)
```

🔴 `pint --test` **düzeltmez**, sadece bakar. Kırıldığında `composer lint`
çalıştırılır, sonra `composer check` tekrarlanır.

`php artisan serve` → `http://127.0.0.1:8000`
Migration'lar koştu: `users`, `sessions`, `cache`, `jobs`, `personal_access_tokens`…

**Çalışan endpoint:** `GET /api/ping` → `{"status":"ok"}`
**Çalışan hata yolu:** bilinmeyen rota → `{"error":{"code":"RESOURCE_NOT_FOUND"}}`

**Faz 7 (3-4 Eylül 2026) — Ödeme ve paywall (ticari çekirdek):**

> Tam kayıt: `docs/rehber/fazlar/FAZ-7.md` · devir:
> `davetkart-backend-php-laravel/claude/FAZ-7-DEVIR.md`

| Dosya | Ne yapar | Kılavuzu |
|---|---|---|
| `app/Enums/OrderStatus.php` | `pending\|paid\|failed\|refunded` + **durum makinesi** (`canTransitionTo`) | `rehber/app/Enums/OrderStatus.md` |
| `..._create_orders_table.php` | 🔴 `provider_ref` UNIQUE + 4 CHECK · `invitation_id` nullable (K42) | `rehber/database/migrations/…create_orders_table.md` |
| `app/Models/Order.php` | Boş `#[Fillable]` · `scopeGrantingPublishRight` | `rehber/app/Models/Order.md` |
| `database/factories/OrderFactory.php` | Tutar **plandan** türetilir | `rehber/database/factories/OrderFactory.md` |
| `Exceptions/PaywallViolationException.php` + 3 kardeşi | 402×2 · 409 · 404 · 502/503 — hepsi `HasErrorCode` | `rehber/app/Exceptions/PaywallViolationException.md` |
| `Services/Payment/PaymentGateway.php` + 2 DTO | 🔴 Strategy Pattern (**K8**) | `rehber/app/Services/Payment/PaymentGateway.md` |
| `Services/Payment/FakeGateway.php` | **Gerçek HMAC**, `hash_equals`, sahte para | `rehber/app/Services/Payment/FakeGateway.md` |
| `Services/Pricing/TierResolver.php` | `getRequiredTier()`'ın **sunucu ikizi** | `rehber/app/Services/Pricing/TierResolver.md` |
| `Contracts/PublishEntitlementResolver.php` + `OrderEntitlementResolver` | 🔴 **K42** — iki kaynak, tek arayüz | `rehber/app/Contracts/PublishEntitlementResolver.md` |
| `Actions/Payment/StartCheckoutAction.php` | Sunucu fiyatı + telafi (**L7**) | `rehber/app/Actions/Payment/StartCheckoutAction.md` |
| `Actions/Payment/HandlePaymentCallbackAction.php` | 🔴 İdempotans: kilit + durum makinesi | `rehber/app/Actions/Payment/HandlePaymentCallbackAction.md` |
| `Actions/Invitation/PublishInvitationAction.php` | 🔴 **Paywall kapısı** — Faz 3'ten beri boştu (K47) | `rehber/app/Actions/Invitation/PublishInvitationAction.md` |
| `Requests/Payment/StoreCheckoutRequest.php` | Tek alan (`tier`); fiyat **yok** | `rehber/app/Http/Requests/Payment/StoreCheckoutRequest.md` |
| `Resources/OrderResource.php` | Üç alan; `providerRef` **sızmaz** | `rehber/app/Http/Resources/OrderResource.md` |
| `Controllers/…/PaymentController.php` | K42'nin iki kolu, iki metot | `rehber/…/PaymentController.md` |
| `Controllers/…/PublicPaymentWebhookController.php` | Üçüncü auth'suz yazma yolu | `rehber/…/PublicPaymentWebhookController.md` |
| `Services/Rsvp/SubscriptionRsvpQuotaResolver.php` | K51 dikiş yeri kapandı | `rehber/app/Services/Rsvp/SubscriptionRsvpQuotaResolver.md` |
| `..._add_timezone_to_invitations_table.php` | 🔴 **K63/K71** | `rehber/database/migrations/…add_timezone…md` |
| `tests/Feature/PaywallTest.php` | **33 test** + 33 satırlık mutasyon tablosu | `rehber/tests/Feature/PaywallTest.md` |

**Faz 7'de düzenlenenler:** `SubscriptionTier` (`values()`) · `ErrorCode`
(`PAYMENT_REQUIRED` artık `requiredTier` taşıyor) · `contracts/error-codes.json` ·
`User`/`Invitation` (`orders()`) · `Invitation` (`timezone`) ·
`InvitationPolicy` (`publish()`) · `AppServiceProvider` (3 bağlama + sürücü
seçimi) · `InvitationController` (`publish()`) · `InvitationRequest` ·
iki `InvitationPayload`/`PublicInvitation` Resource'u ·
`ResolveOpenRsvpInvitationAction` (son tarih artık davetiyenin diliminde) ·
`InvitationFactory` · `config/davetkart.php` (`default_timezone`) ·
`CLAUDE.md` (`if` kuralı gevşetildi — Faz 6'nın B4 borcu; `app/Contracts/`
tanımlandı; ödeme standartları eklendi)

**Faz 7'de SİLİNEN:** `app/Services/Rsvp/TierRsvpQuotaResolver.php` + kılavuzu
(**B8** — dikiş yeri kapandı, `FALLBACK_TIER` gitti)

---

**Faz 8 (7 Eylül 2026) — AI asistan ve iletişim:** `AiProvider` +
`GeminiProvider` + `NullProvider` · `AssistantController` (kotalı proxy,
`assistant_usages` tablosu) · `ContactSubject` + `contact_messages` ·
`IpHasher` + `HasHoneypot`. Tam kayıt: `docs/rehber/fazlar/FAZ-8.md`,
kararlar `claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md`.

**Faz 9 (11 Eylül 2026) — Üretim hazırlığı:**

| Dosya | Ne yapar |
|---|---|
| `app/Enums/OrderScope.php` | 🔴 Siparişin **ne satın aldığı** — `invitation_id`'nin yokluğundan türetilmiyor (**E12**) |
| `..._add_scope_to_orders_table` · `..._make_orders_scope_not_null` | Genişlet/daralt deseni, 2 CHECK |
| `Actions/Invitation/DeleteInvitationAction.php` | 3 günlük hak serbest bırakma penceresi (**K82**) |
| `Actions/Payment/ClaimReleasedOrderAction.php` | Serbest hakkı bağlar — **yeten en düşük** (**K83**) |
| `Console/Commands/ExpireStaleOrders.php` | `orders:expire` — `expires_at` ilk kez okunuyor |
| `Console/Commands/PruneOrphanMedia.php` | `media:prune-orphans` — LCV'ye bağlanmamış yüklemeler |
| `routes/console.php` | Projenin ilk **kendiliğinden çalışan** kodu |
| `config/cors.php` | 🔴 `exposed_headers: ['ETag']` — Faz 4/5 buna bağlı (**K86**) |
| `Http/Middleware/SecurityHeaders.php` | 6 sertleştirme başlığı, **global** yığında (**K85**) |
| `tests/Unit/OrderScopeTest.php` | Projenin **ilk birim testi** |
| `docs/10-URETIM-ENV-SABLONU.md` | Üretim `.env` şablonu, her satırın gerekçesiyle |

**Faz 9'da SİLİNEN:** `routes/web.php` · `resources/views/welcome.blade.php`
(ölü `welcome` rotası — ders 26). Tam kayıt: `docs/rehber/fazlar/FAZ-9.md`.
⚠️ **23 Eylül düzeltmesi:** iki dosya da depoda **duruyor** — 9.1 yalnızca
`bootstrap/app.php`'deki `web:` satırını kaldırdı. Rota yüklenmiyor, zararsız;
ama *"silindi"* iddiası doğru değil (B4). `git rm` bekliyor.

**Faz 9 sonrası — plan dışı eklemeler (17–21 Eylül 2026):**

| Dosya | Ne yapar |
|---|---|
| `Actions/Media/DeleteGalleryMediaAction.php` + `DELETE /invitations/{id}/media/{media}` | Galeriden silme — kilit altında, önce DB sonra dosya (F3) |
| `Resources/PublicGalleryImageResource.php` | Misafire galeri **kimliksiz** (`{url}`) |
| `..._add_gallery_media_ids_to_invitations_table.php` | Galeri **sırası** `jsonb` dizide; `#[Fillable]`'da değil |
| `Jobs/OptimizeUploadedImage.php` (yeniden yazıldı) + `Jobs/OptimizedImage.php` | EXIF yönü, piksel tavanı, bellek bütçesi, yeni yola yazma |
| `Jobs/DeleteReplacedMediaFile.php` | Eski dosyayı 24 saat sonra, sahipsizse siler |
| `AppServiceProvider::configureLocalServer()` | Windows'ta `php artisan serve` altında yükleme düşmesi (TEMP/TMP) |
| `.github/workflows/ci.yml` | PostgreSQL 18 servisiyle `composer check` + `composer audit` |
| `composer.json` | PHP `^8.5` · `ext-gd` · `ext-exif` · `sentry/sentry-laravel` |
| `config/sentry.php` + `bootstrap/app.php` | Sentry — `Integration::handles()` |
| `config/ai.php` + `GeminiProvider` | `gemini-2.5-flash` + `thinking_budget: 0` |

> Bunların hiçbiri için `composer check` sonucu kayda geçmedi. Sentry ve Gemini
> değişiklikleri **kılavuzsuz** eklenmişti (K18); 23 Eylül'de yazıldı/güncellendi.

### ❌ Henüz yok

- 🔴 Gerçek ödeme sağlayıcısı — **Shopier** (Eylül 2026'da hesap açıldı; eskiden
  `IyzicoGateway` planlanıyordu). `PaymentGateway` arayüzü (K8) hazır ama Shopier'in
  imza/geri dönüş modeline göre uyarlanmalı — rapor §4
- 🔴 **Parola sıfırlama**, e-posta doğrulama, hesap silme (KVKK) — hiçbir fazda yoktu
- Sipariş durumu / *"siparişlerim"* ucu · `InvitationResource.publishedAt`
  (frontend F7.2 istiyor)
- 🔴 Redis (cache + queue) · S3 uyumlu disk · `queue:work` süpervizörü —
  **K80 gereği birer YÜKSELTME**, varsayım değil
- `Jobs/SendRsvpNotification` (K79) — kanal/dil/politika/şablon dört ayrı karar
- 🔴 **Paket alımın kaç yayın açtığı sınırı** — açık ticari karar (K43)
- `contact_messages` için okuma ucu
- ~~Frontend'de `toDisplayError()` çeviri katmanı~~ ✅ F1 (13 Eylül)
- ~~Frontend Faz 4/5/6/7/8/9 uyarlamaları~~ ✅ F1–F7 (13–16 Eylül) — F8 doğrulaması açık

---

## 10. Yol Haritası — 9 Faz

Detayı `docs/07-GELISTIRME-YOL-HARITASI.md`'de. Her faz **çalışan bir çıktı**
ile biter; "dosya yazıldı" bitti sayılmaz.

| Faz | Konu | Frontend'de ne çalışır | Durum |
|---|---|---|---|
| **0** | Zemin: PostgreSQL + kalite araçları + hata sözleşmesi | — | ✅ **BİTTİ** |
| **1** | İlk endpoint + `ForceJsonResponse` + **hata zarfı (K20)** | — | ✅ **BİTTİ** |
| **2** | **Auth özellik dilimi** (17 backend + 7 frontend dosyası) | **Giriş / kayıt** ✅ | ✅ **BİTTİ** |
| **3** | **Invitation CRUD + Policy + Resource ailesi** (12 backend + 8 frontend) | **Dashboard + editör autosave** ✅ | ✅ **BİTTİ** |
| **4** | **Public davetiye + cache + ETag** (8 backend + 2 frontend) | **`/invite/{id}` sayfası** ✅ | ✅ **BİTTİ** |
| **5** | **RSVP** (public submit + owner list) | LCV gönderimi + canlı panel ✅ (FE F2/F5) | ⚠️ **KOD BİTTİ** · elle doğrulama açık |
| **6** | **Media + Job** (24 adım) | Galeri + LCV medyası ✅ (FE F2) | ⚠️ **KOD BİTTİ** · kapanış listesi açık |
| **7** | **`TierResolver` + `PublishInvitationAction` + Payment** (25 adım) | Yayınlama + paywall ✅ (FE F3) | ⚠️ **KOD BİTTİ** · `composer check` ✅ (Faz 9'da) · elle doğrulama açık |
| **8** | **AI proxy + Contact** (21 adım) | Asistan, iletişim formu ✅ (FE F2/F4) | ⚠️ **KOD BİTTİ** · elle doğrulama açık |
| **9** | **Üretim hazırlığı** (16 adım) | — | ⚠️ **KOD BİTTİ · `composer check` YEŞİL** · elle doğrulama açık |

> 🔴 **Faz 9 planlanandan farklı bitti.** `docs/07`/`docs/09`'daki 7 satırlık
> liste Faz 3'ten önce yazılmıştı ve birikmiş borçları içermiyordu. Gerçek
> kayıt: `docs/rehber/fazlar/FAZ-9.md`. **Redis, S3 ve `IyzicoGateway`
> ertelendi** (K80 + sandbox anahtarı yok); yerine `orders.scope` bulgusu,
> iki bakım komutu, zamanlayıcı, CORS ve güvenlik başlıkları yazıldı.

> 🔴 **Faz 5, 6 ve 7 "bitti" DEĞİL.** Üçünün de kodu yazıldı ve commit'lendi ama
> kapanış ölçütleri işaretlenmedi. Bir faz **çalışan bir çıktı** ile biter;
> "dosya yazıldı" bitti sayılmaz. Kapanış betikleri:
> `docs/rehber/fazlar/FAZ-5-ELLE-DOGRULAMA.md` (16 adım) ·
> `FAZ-6-ELLE-DOGRULAMA.md` (18 adım) · `FAZ-7-ELLE-DOGRULAMA.md` (20 adım).

### Faz 2 — çalışan uç noktalar ✅

| Method | Path | Auth | Yanıt |
|---|---|:---:|---|
| POST | `/api/auth/register` | — | `201` · **zarfsız** `{user, token}` |
| POST | `/api/auth/login` | — | `200` · **zarfsız** `{user, token}` |
| POST | `/api/auth/logout` | ✅ | `204` · gövde yok |
| GET | `/api/auth/me` | ✅ | `200` · **zarflı** `{data: {...}}` |

Elle doğrulama: `docs/rehber/fazlar/FAZ-2-ELLE-DOGRULAMA.md` (13 adım).
Faz özeti ve **kurulan 20 kural**: `docs/rehber/fazlar/FAZ-2.md`.

### Faz 3 — çalışan uç noktalar ✅

| Method | Path | Auth | Yanıt |
|---|---|:---:|---|
| GET | `/api/invitations` | ✅ | `200` · `{data: [...]}` — yalnızca kendi kayıtları |
| POST | `/api/invitations` | ✅ | `201` · `{data: {...}}` |
| GET | `/api/invitations/{id}` | ✅ | `200` · başkasınınkinde **404** (H7) |
| PUT | `/api/invitations/{id}` | ✅ | `200` · program senkronize edilir |
| DELETE | `/api/invitations/{id}` | ✅ | `204` · soft delete |

Elle doğrulama: `docs/rehber/fazlar/FAZ-3-ELLE-DOGRULAMA.md` (14 adım + uçtan uca).
Faz özeti, **kronoloji** ve **kurulan 15 kural**: `docs/rehber/fazlar/FAZ-3.md`.

### Faz 4 — çalışan uç noktalar ✅

| Method | Path | Auth | Yanıt |
|---|---|:---:|---|
| GET | `/api/public/invitations/{id}` | — | `200` · `{data: {id, invitation}}` · **ETag** |
| GET | (aynı, `If-None-Match` ile) | — | `304` · **gövde yok** |
| GET | (yayınlanmamış / silinmiş / yok) | — | `404` · üçü **ayırt edilemez** |

Elle doğrulama: `docs/rehber/fazlar/FAZ-4-ELLE-DOGRULAMA.md` (15 adım).
Faz özeti, **kronoloji** ve **kurulan 11 kural**: `docs/rehber/fazlar/FAZ-4.md`.

🔴 **Faz 4, Faz 3'ün yeşil kapanmadığını ortaya çıkardı** — üç fazda üçüncü kez
aynı desen. Ayrıntı: `FAZ-4.md` §8.

### Faz 5 · 6 · 7 — çalışan uç noktalar (⚠️ doğrulanmadı)

| Method | Path | Auth | Faz |
|---|---|:---:|:---:|
| POST | `/api/public/invitations/{id}/rsvps` | — | 5 |
| GET | `/api/invitations/{id}/rsvps` (ETag) · DELETE `/api/rsvps/{id}` | ✅ | 5 |
| POST | `/api/invitations/{id}/media` · `/api/public/invitations/{id}/media` | ✅ / — | 6 |
| **POST** | **`/api/invitations/{id}/publish`** | ✅ | **7** |
| **POST** | **`/api/invitations/{id}/checkout`** (tekil) | ✅ | **7** |
| **POST** | **`/api/payments/checkout`** (paket) | ✅ | **7** |
| **POST** | **`/api/public/payments/webhook`** | — | **7** |

**Toplam uç sayısı: 19** (Faz 7 sonu) → Faz 8'de **21** (asistan + iletişim) →
23 Eylül'de **22** (`DELETE /api/invitations/{id}/media/{media}`). Tam liste:
`docs/11` Ek A.

---

### 🔴 Sıradaki iş (25 Eylül 2026): FAZ 10

Plan: `davetkart-backend-php-laravel/claude/FAZ-10-PLANI.md` — 85 adım (10.0–10.84), 9 dilim
(0 · A kritik · B-D yüksek · E-F orta · G Shopier · H temizlik · Z kapanış).
Alınan kararlar: **K87** PHP ^8.5 kalır · **K88** yayındaki davetiyede plan kontrolü
kayıt anında (402) · **K89** `OrderStatus::Expired` · **K90** token ömrü 30 gün.
`ef7c692`'de (25 Eylül) uygulandı, 10.0'da kayda geçecek: **K91** bozuk girdi → 400 ·
**K92** `integer:strict` · **K93** `Retry-After` başlığı.

### Sıradaki iş (23 Eylül 2026) — Faz 10 planıyla yer değiştirdi

1. `claude/GOZDEN-GECIRME-RAPORU.md` §1 — **yayın sonrası paywall aşımı** ve
   **geç gelen ödemenin kaybolması** (ikisi de gerçek ödeme açılmadan kapanmalı)
2. `composer check` — Faz 9 sonrası eklemelerle ilk kayıtlı koşu (PHP 8.5 + Sentry)
3. Faz 5-9 elle doğrulama betikleri + frontend F8 (17 senaryo)
4. Shopier entegrasyonu (rapor §4) · parola sıfırlama · sipariş durumu ucu

### ~~🔴 Sıradaki iş: Faz 7'yi kapat~~ (tarihsel — 4 Eylül 2026)

Faz 7'nin kodu 30 commit hâlinde yazıldı. `composer check` **bir kez koştu**
(4 Eylül 2026) ve 7 hata buldu; hepsi düzeltildi (commit `7.30`) ama **zincir
henüz sonuna kadar gitmedi** — testler hiç çalışmadı.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel

# Faz 6'nın borcu (bir kez yapıldı, tekrar gerekmiyor)
php artisan storage:link

php artisan migrate
php artisan errors:export ; git diff contracts/error-codes.json
composer lint
composer check                      # 🔴 SON satıra bak
php artisan test --filter=PaywallTest
```

Sonra `docs/rehber/fazlar/FAZ-7-ELLE-DOGRULAMA.md` (20 adım; **Adım 0** Faz
6'nın kapanış listesi).

**Faz 7'nin bitti ölçütü:** Standart planla galeri açık davetiye
yayınlanamıyor (**402**); sahte ödeme sonrası yayınlanabiliyor. Aynı webhook
iki kez gelince **tek** order ve `paid_at` **değişmiyor**.

**Faz 7'de öğrenilenler:** Strategy Pattern · Dependency Inversion · idempotans
· veritabanı kısıtıyla race condition önleme · HMAC imza doğrulaması · para
aritmetiği (minor unit) · duvar saati vs `timestamptz`.

---

### ~~Faz 8 — bundan sonra (Faz 7 kapanınca)~~ ✅ Faz 8 7 Eylül'de yazıldı (tarihsel plan)

| # | Dosya |
|---|---|
| 8.1 | `app/Services/Ai/AiProvider.php` (interface) + `GeminiProvider` + `NullProvider` |
| 8.2 | `AssistantController` — kotalı proxy |
| 8.3 | `app/Enums/ContactSubject.php` |
| 8.4 | `..._create_contact_messages_table.php` + model |
| 8.5 | `ContactRequest` + `ContactController` |

`PaymentGateway` deseni (K8) burada **birebir tekrarlanacak**: sağlayıcı bir
arayüzün arkasında, `NullProvider` testte gerçek çağrıyı engeller. Ayrıntı
`docs/09` §Faz 8.

---

## 11. 🔴 İhlal Edilemez Kurallar

### Sözleşme kuralları (ihlal edilirse frontend kırılır)

| Kural | Sebep |
|---|---|
| Rotalar `/api/...` — **`/api/v1/...` DEĞİL** | `baseURL = '/api'`; versiyon namespace'te |
| Auth **başarı** yanıtı zarfsız `{user, token}` | `services/auth.ts` doğrudan `data.user` okuyor |
| Diğer başarı yanıtları `{data: ...}` zarfıyla | Laravel Resource varsayılanı |
| **Hata yanıtı `{error: {code, fields?, params?}}`** | K20 — `docs/08-HATA-SOZLESMESI.md` |
| Alan adları **camelCase** | Dönüşüm **sadece** API Resource katmanında |
| Kimlik hatası **401** | `api.ts` interceptor'ı `401`'de oturumu düşürür |
| Backend **8000** portunda | `vite.config.ts` proxy'si oraya bakıyor |
| Uzun işler kuyruğa | `api.ts` timeout **15 sn** |
| `id` alanları **string** | Frontend `id: string` bekliyor → ULID |

### Güvenlik kuralları

| Kural | Sebep |
|---|---|
| **Paywall sunucuda yeniden hesaplanır** | `getRequiredTier()` sadece tarayıcıda; DevTools'tan aşılabilir |
| LCV kotası **`SUM(guest_count)`** ile | `COUNT(*)` kullanılırsa 100 kayıt × 4 kişi = 400 misafir sızar |
| Modellerde **`$guarded = []` YASAK** | Sadece `$fillable` beyaz listesi |
| Action'da `$request->all()` değil **`validated()`** | Enjekte edilmiş alanlara karşı ikinci savunma |
| Sırlar sadece `.env` → `config/` → Service | Gemini/ödeme anahtarları frontend'e **asla** |
| Kod içinde **`env()` çağrılmaz** | `config:cache` sonrası `null` döner |
| Repoya giren dosyaya **sır yazılmaz** | `phpunit.xml`, `config/*.php` repodadır |
| IP'ler hash'lenerek saklanır | KVKK |
| Ödeme `provider_ref` **UNIQUE** | Webhook tekrarına karşı idempotans — 🔴 ama **yalnızca ikinci satırı** engeller (**M8**) |
| Durum makinesi + `lockForUpdate()` | Bir satırın **iki kez ilerlemesini** engeller (**M8**) |
| Fiyat **asla** istek gövdesinden okunmaz | `{"price":1}` biçimsel olarak geçerlidir; savunma kural değil **mimaridir** (**M6**) |
| Para **kuruşta tam sayı** (`amount_minor`) | Kayan noktada toplamlar kuruş kaçırır (**M5**) |
| Webhook imzası **ham gövde** + `hash_equals()` | Yeniden serileştirme imzayı bozar (**W1**); `===` zamanlama saldırısına açık (**W2**) |
| Webhook ucu **her zaman 2xx** | 404 sonsuz retry + bilgi sızıntısı (**W3**) |
| Exception'da `$code`/`$message`/`$file`/`$line` **yasaklı ad** | `Exception`'ın kendi özelliklerini gölgeler → LSP ihlali (ders 55) |
| **Auth hatalarında `fields` dönmez** | Kullanıcı sayımı (enumeration) açığı — K20 §3.1 |
| **Sahiplik yoksa 404**, 403 değil | 403 kaynağın varlığını doğrular — K20 §3.2 |
| `error.debug` **yalnızca `APP_DEBUG=true`** | Üretimde kod hiç çalışmaz |
| Yığın izi / SQL / sağlayıcı hatası **yanıta girmez** | Yalnızca log |

### Faz 1'de eklenen kurallar (özet)

| Seri | Konu | En kritik maddesi |
|---|---|---|
| **H10-H13** | Hata yolu | Action/Controller hata **yanıtı üretmez**, exception fırlatır (H10) |
| **R1-R5** | Rotalar | Rota dosyasına **closure yazılmaz** — `route:cache` kırılır (R1) |
| **M1-M4** | Middleware | Yalnızca `Accept` ezilir, **`Content-Type` asla** (M1) |
| **T6-T9** | Test | Bir davranışın hem **varlığı** hem **yokluğu** test edilir (T6) |
| **G1-G3** | Üretilen dosyalar | Çıktı **deterministik** olur, zaman damgası karşılaştırmadan çıkarılır |

### Faz 2'de eklenen kurallar (özet)

| Seri | Konu | En kritik maddesi |
|---|---|---|
| **A1-A7** | Kimlik ve güvenlik | Auth uçlarında `unique`/`exists` **kullanılmaz** (A1) · Kullanıcı yoksa bile hash doğrulanır (A3) · Güvenlik kodunda **kısa devre yasak** (A4) |
| **D1-D5** | Doğrulama | Kalite kuralı yalnızca **üretim anında** uygulanır, okuma anında değil (D3) |
| **E1-E5** | Veri katmanı | Benzersizlik **veritabanı kısıtıyla**, `if` ile değil (E2) · Türetilebilen veri saklanmaz (E1) |
| **C1-C3** | Sözleşme | Resource bir **beyaz listedir** (C1) · Zarf istisnası ad ad tanımlıdır (C2) |
| **T10-T12** | Test | Token testleri `withToken()` ile — `actingAs()` **boş yeşil** test üretir (T10) |
| **B4** | Belgeleme | Dokümanda verilen söz, kodda karşılığı yoksa **yalandır** |

### Faz 3'te eklenen kurallar (özet)

| Seri | Konu | En kritik maddesi |
|---|---|---|
| **P1-P4** | Yetkilendirme | Koleksiyon uçlarında sahiplik Policy ile değil **sorgu ile** korunur (P3) · Güvenlik karşılaştırmasında iki tarafın **tipi garanti** olmalı (P4) |
| **N1-N4** | İç içe koleksiyon | Alt kayıt **her zaman üst kaydın ilişkisinden** oluşturulur (N1) · **`null` ile `[]` farklı bilgilerdir** (N4) |
| **D6** | Doğrulama | Kural **adı** sözleşmenin parçasıdır; kural nesnesi değil string kural |
| **E6** | Veri katmanı | Kısıt yalnızca **backend'in sahibi olduğu** kurala konur |
| **C4-C5** | Sözleşme | Aynı veri, farklı okuyucular için **farklı Resource** (C4) · **Giden** alanlar da beyaz listedir (C5) |
| **T13-T14** | Test | İkinci kimlikli istekten önce **guard sıfırlanır** (T13) · Yapılmadığını test ediyorsan **etkiyi** doğrula (T14) |
| **B5** | Belgeleme | Otomatik kontrolün yolunda olmayan dosyayı **elle çalıştırmak** senin sorumluluğun |

### Faz 4'te eklenen kurallar (özet)

| Seri | Konu | En kritik maddesi |
|---|---|---|
| **O1-O6** | Önbellek | Cache'e konan şey **son adımın çıktısıdır** (O1) · TTL tazelik değil **üst sınır** (O3) · Geçersizleştirme **kuyruğa alınmaz** (O4) · Temizleme **commit'ten sonra** (O5) |
| **R6** | Rotalar | Framework'ün hazır kısıtı varsa desen **elle yazılmaz** — elle yazılan sessizce yanlış olabilir |
| **E7** | Veri katmanı | Sunucunun sahip olduğu alanın değerini **sunucu kodu** söyler; ORM DB varsayılanını geri okumaz |
| **C6** | Sözleşme | Kapalı modülün verisi gövdeye **hiç girmez** — boş değerle maskelenmez |
| **T15** | Test | Uçtan uca doğrulanamayan zincir **halkalara ayrılır**; testi uyarla, üretimi değil |
| **B6** | Belgeleme | Bir savunmanın **neyi kapatmadığı** da yazılır |

### Faz 5 · 6 · 7'de eklenen kurallar (özet)

> Tam metinleri **EK dosyalarında**; bu bölüme henüz işlenmedi.

| Faz | Seri | En kritik maddesi |
|---|---|---|
| **5** | **L1-L4** · E8-E9 · C7 · P5 · T16 · B7 | Savunma katmanları **ucuzdan pahalıya** (L1) · Bot tespiti **sessizdir** (L2) · Hız sınırı ile kota **birbirinin yerine geçmez** (L3) · **Mutasyon tablosu** faz kapanış ölçütüdür (T16) |
| **6** | **F1-F5** · L5-L6 · A8 · T17 · E10 · B8 | Dosya tipi **içerikten** doğrulanır (F1) · Depolanan adı **sunucu üretir** (F2) · **Dosya sistemi transaction'a dâhil değildir** (F3) · Bir sınıfın **değişmezi** doğrulama katmanına bırakılmaz (A8) |
| **7** | **M5-M8** · **W1-W3** · L7 · P6 · E11 | Para **kuruşta tam sayı** (M5) · Fiyat **asla gövdeden** okunmaz (M6) · İdempotans **iki katmandır** (M8) · İmza **ham gövde** + `hash_equals()` (W1/W2) · **Dış servis transaction'a dâhil değildir** (L7) · Policy'nin cevabı `bool`dur, **bilgi taşıyan red** oraya konmaz (P6) · Çok kolonlu değişmez **CHECK kısıtına** yazılır (E11) |

> **Toplam kural sayısı: 127** (FAZ-0 31 · FAZ-1 19 · FAZ-2 20 · FAZ-3 15 ·
> FAZ-4 11 · FAZ-5 10 · FAZ-6 11 · **FAZ-7 10**)

> **Kuralların tam listesi:**
> `docs/rehber/fazlar/FAZ-0.md` §4 (31 madde — Y/V/K/T/S/H/B)
> `docs/rehber/fazlar/FAZ-1.md` §4 (19 madde — H10-13/R/M/T6-9/G)
> `docs/rehber/fazlar/FAZ-2.md` §4 (20 madde — A/D/E/C/T10-12/B4)
> `docs/rehber/fazlar/FAZ-3.md` §5 (15 madde — P/N/D6/E6/C4-5/T13-14/B5)
> `docs/rehber/fazlar/FAZ-4.md` §5 (11 madde — O1-6/R6/E7/C6/T15/B6)
> `docs/rehber/fazlar/FAZ-5.md` · `FAZ-6.md` · **`FAZ-7.md` §5 (10 madde — M5-8/W1-3/L7/P6/E11)**

---

## 12. Bilinen Frontend Uyuşmazlıkları ⚠️

> ✅ **23 Eylül 2026:** Aşağıdaki tablonun 🔴 satırlarının **tamamı** frontend
> yakalama fazında (F1–F7, 13–16 Eylül) kapandı: medya/LCV/iletişim uçları,
> hata çeviri katmanı (`errors.json` + `toDisplayError()`), yayınlama, gerçek
> checkout, `activeTier` mock'unun silinmesi, ETag/polling, `timezone`, silme
> uyarısı (tarihsiz). Tablo tarihsel kayıt olarak duruyor.
>
> **Hâlâ açık olanlar** (ayrıntı: `GOZDEN-GECIRME-RAPORU.md` §3):
>
> | Konu | Backend | Frontend |
> |---|---|---|
> | Ödeme dönüş sayfası | `PAYMENT_SUCCESS_URL=/odeme/basarili` | 🔴 Rota **yok** — `*` ana sayfaya atıyor |
> | Sipariş durumu | Sorgulayan uç **yok** | Ödeme sonrası kullanıcıya bir şey söylenemiyor |
> | `publishedAt` | Hiçbir Resource'ta yok | Silme uyarısı tarihsiz (F7.2) |
> | Konum arama | `/public/places/search` **yok** | `VITE_PLACES_SEARCH_ENABLED=false` ile kapalı |
> | Galeri kotası | 30 dosya | Arayüz 8 fotoğrafta kesiyor |
> | "Logosuz özel yayın" (Elit) | Sinyal yok | Alt bilgi her zaman *"DavetKart ile hazırlandı"* |
> | Yayınlanmış davetiyeyi düzenleme | Modül açmayı **kontrol etmiyor** | "Düzenle" düğmesi serbest — rapor §1.1 |

| Konu | Backend | Frontend | Karar |
|---|---|---|---|
| ~~Kayıt gövdesi / `user` yanıtı~~ | `{firstName, lastName, ...}` | ✅ uyumlu · `utils/user.ts` birleştiriyor | ✅ **K35 — Faz 2'de çözüldü** |
| ~~401 yorumu~~ | `UNAUTHENTICATED` vs `INVALID_CREDENTIALS` | ✅ `apiErrorCode()` ile ayırt ediliyor | ✅ **Faz 2'de çözüldü** |
| Medya yükleme rotası | `POST /api/media` planlanmıştı | `POST /media/upload`, yanıt `{url}` | **Frontend kazanır** — Faz 6 |
| ~~`InvitationStatus`~~ | ~~`draft \| saved \| published`~~ | `'published' \| 'saved'` | ✅ **K38 — Faz 3'te çözüldü** |
| ~~Tekil davetiye varsayımı~~ | REST koleksiyonu | ✅ uyarlandı (F2-F6) | ✅ **K37 — Faz 3'te çözüldü** |
| ~~Program adımı kimliği~~ | Backend üretir | ✅ `id: null` + `localKey` | ✅ **K44 — Faz 3'te çözüldü** |
| `RsvpStatus` değerleri | `attending \| pending \| declined` | `'Katılıyor' \| 'Bekleniyor' \| 'Katılamıyor'` | DB İngilizce, çeviri frontend'de (K21) |
| Hata gösterimi | Kod döner | `errors.*` çeviri anahtarları **henüz yok** | `Notlar/03` — frontend yapacak |
| 404 sayfası | — | `path: '*'` → ana sayfaya yönlendiriyor | Faz 5 — `/invite/:id` kendi "bulunamadı" ekranını çiziyor (4.8), genel 404 hâlâ açık |
| CORS | `config/cors.php` daraltıldı | Vite proxy sayesinde same-origin | ✅ **K86 (Faz 9)**. 🔴 Üretimde proxy YOK: frontend'in gerçek origin'i `CORS_ALLOWED_ORIGINS`'e yazılmalı |
| **ETag okunabilirliği** | `exposed_headers: ['ETag']` (Faz 9) | `If-None-Match` **hiç gönderilmiyor** | 🔴 Backend hazır; polling'i frontend kuracak |
| **Silme + 3 günlük pencere** | K82 (Faz 9) | Uyarı yok | 🔴 Yayınlanmış davetiye silinirken kullanıcı uyarılmalı — sunum kararı (K20) |
| **Checkout ucu** | `POST /invitations/{id}/checkout` **veya** `/payments/checkout`, gövde `{tier}` | `paymentService.checkout({tier})` — **mock** | 🔴 Frontend uyarlanacak (**K64**) |
| **Checkout yanıtı** | **Zarflı** `{data:{orderId,tier,status,redirectUrl}}`, `status='pending'` | Zarfsız bekliyor, `status:'paid'` **sabit** | 🔴 Ödeme **anında** tamamlanmıyor; `paid`'e geçişi **webhook** yapar |
| **Yayınlama** | `POST /invitations/{id}/publish` → 200/402/409 | **Uç yok** | 🔴 `services/invitations.ts`'e eklenecek |
| **`activeTier`** | Sunucu tek doğruluk kaynağı (`orders`) | Oturum içi **mock** | 🔴 **En kritik madde**: mock kalırsa yayın 402 dönünce kullanıcı şaşırır |
| **`invitation.timezone`** | Her iki Resource'ta da gönderiliyor (misafirde **her zaman dolu**) | `types.ts`'te **alan yok** | 🔴 Eklenecek; geri sayım bu dilimde hesaplanmalı (**K63/K71**) |
| Yeni hata kodları | `PAYMENT_REQUIRED` · `PAYWALL_TIER_INSUFFICIENT` · `INVITATION_ALREADY_PUBLISHED` · `PAYMENT_PROVIDER_ERROR` · `PROVIDER_UNAVAILABLE` | `errors.json`'da karşılığı yok | `Notlar/03` — frontend yapacak |

---

## 13. Öğrenilen Dersler / Bilinen Tuzaklar

**1. Laravel klasör yapısı elle oluşturulamaz.** `vendor/autoload.php` (PSR-4
haritası) olmadan hiçbir sınıf bulunamaz. Klasör yapısı kurulumun **çıktısıdır**.

**2. Laravel 11+ iskeleti çok ince.** `app/` içinde sadece `Http/Controllers/`,
`Models/`, `Providers/` var. Diğerlerini `make:*` oluşturur.

**3. Laravel 11+ ile `Kernel.php` kaldırıldı.** Middleware, exception ve rota
kaydı `bootstrap/app.php` içinde. İnternetteki eğitimlerin çoğu eski yapıyı
anlatıyor.

**4. Herd ücretsiz sürümünde veritabanı yönetimi yok.** PHP, Composer, nginx,
node/npm var. PostgreSQL ayrı kuruldu, pgAdmin 4 ile yönetiliyor.

**5. `make:class` Action ve Service için de çalışıyor.** Laravel'in `Action`
kavramı yok ama `php artisan make:class Actions/X/YAction` klasörü açar ve
namespace'i doğru yazar.

**6. Klasör adları PascalCase olmalı.** Windows harf duyarsız, canlı sunucu
(Linux) duyarlı — `app/actions/` yerelde çalışır, sunucuda "class not found".

**7. Aşağıdan yukarı inşa öğrenmeyi zorlaştırır.** Config + enum ile başlandı;
"kitabın ortasından açmış gibi" hissedildi. K17 bu yüzden alındı.

**8. Terimler kontrol edilmeden kullanılmamalı.** "Yatay/dikey" kelimesi iki
farklı eksende kullanılınca karışıklık doğdu (bkz. Bölüm 6).

**9. PHPStan 128 MB'a sığmaz.** Larastan tüm modelleri çözümler.
`--memory-limit=1G` gerekir ve bu bayrak **`composer.json`'a** yazılır — kişinin
hafızasına değil. Aksi halde "bende çalışıyor" hataları doğar.

**10. Windows'ta `PATH` değişikliği çalışan süreçlere yansımaz.** Ortam
değişkenleri süreç doğarken kopyalanır; VS Code'un yeniden başlatılması gerekir.

**11. `shouldBeStrict()` zaten `preventLazyLoading()`'i içerir.** İkisini birden
yazmak gereksiz tekrardır.

### Faz 1'de öğrenilenler

**12. `pint` ile `pint --test` farklı komutlardır.** `composer check` içindeki
`--test` **düzeltmez**, sadece bakar ve bozuksa çıkış kodu `1` döner — zincirin
geri kalanı hiç çalışmaz. Çözüm: `composer lint` (düzeltir) → `composer check`
(doğrular). Bu, kalite kapısının işinin *değiştirmek* değil *doğrulamak* olduğu
tasarımının sonucudur.

**13. `config:publish` ile gelen dosyalar Pint'e takılır.** Laravel'in `vendor/`
içindeki config dosyaları `declare(strict_types=1)` kullanmıyor; bizim `pint.json`
zorunlu tutuyor (K1). Her `config:publish` sonrası `composer lint` çalıştırılmalı.

**14. Closure rotalar `route:cache`'i kırar.** `LogicException: Unable to prepare
route ... Uses Closure.` Faz 9'da patlayacak bir borç; Faz 1'de peşin ödendi (K30).

**15. `storage/app/` git'e girmez.** `storage/app/.gitignore` içinde `*` var.
Üretilen bir dosyayı `composer check`'in beklediği yere koyarken bu tuzağa
düşülür — dosya yerelde çalışır, temiz klonda "dosya yok" hatası verir (K33).

**16. `$e->errors()` değil `$e->validator->failed()`.** İlki çevrilmiş **metin**
döndürür (K20 ihlali); ikincisi ihlal edilen **kural adını** ve parametrelerini
verir. K20'yi teknik olarak mümkün kılan API budur.

**17. `match (true)`'da sıra anlamlıdır.** Normal `match`'ten farklı olarak kollar
yukarıdan aşağı denenir. `ThrottleRequestsException` bir `HttpException` olduğu
için, genel kol yukarıda kalırsa özel kol hiç çalışmaz. **Özelden genele** sırala.

### Faz 7'de öğrenilenler (50–55)

**50. 🔴 Bir alanın "doğrulanabilir" olması, kabul edilebilir olduğu anlamına
gelmez.** `{"price": 1}` gövdesi `integer|min:1` kurallarının hepsini geçer.
Fiyat için doğru savunma bir **kural** değil, alanı **hiç kabul etmemektir**.
Doğrulama katmanı **biçimi** doğrular; değeri kimin ürettiği bir **mimari
karardır**.

**51. Aynı teknik soru, farklı çağıranda farklı cevap ister.** İdempotans
webhook'ta **isteniyor** (tekrar eden bir makine, niyeti teyit), yayında
**istenmiyor** (tekrar eden bir insan, niyeti yeni bir şey yapmak). Ders 42'nin
üçüncü örneği: kural değişmedi, **çağıran** değişti.

**52. Bir arayüzün değerini, yazdığın gün değil kaldırdığın uygulamanın
maliyetiyle ölçersin.** `RsvpQuotaResolver` Faz 5'te "gereksiz dolaylılık" gibi
görünüyordu; Faz 7'de gerçek kaynağa geçiş **tek satır** oldu ve
`SubmitRsvpAction` ile testlerine hiç dokunulmadı. `PaymentGateway` aynı
kazancı ikinci kez verdi: 502 yolu, gerçek bir sağlayıcı olmadan test edildi.

**53. Bir `bool` bilgi taşıyamaz — ve yetki katmanı bunu bilmeli.** Paywall
kontrolünü Policy'ye koymak doğal görünüyordu; ama Policy reddi H7 gereği
**404**'e çevriliyor ve kullanıcı "davetiyem kayboldu" derdi. Kuralı iki
katmana bölerken ayırt edici soru: *"bu red bir bilgi taşımak zorunda mı?"*

**54. Framework'ün "modern" yolu, projenin sözleşmesini bozabilir.**
`Rule::enum(SubscriptionTier::class)` daha temiz görünüyordu ama
`$validator->failed()` anahtarı **sınıf adı** olurdu ve hata zarfına
`illuminate\validation\rules\enum` diye sızardı — **D6**'nın (Faz 3,
`Password::min(8)` → `'min:8'`) tam olarak yasakladığı şey. Aynı tuzak, yeni
kılıkta; bu kez kod yazılmadan önce yakalandı.

**55. 🔴 Bir sınıftan türerken üst sınıfın ÖZELLİKLERİNİ de miras alırsın — ve
alan dilinin doğru kelimesi, framework'ün ayırdığı bir ad olabilir.**
`private readonly ErrorCode $code` iki exception'da da yazıldı; `Exception`'ın
zaten `protected $code`'u var. İlk `composer check` koşusu **altı hata** verdi
ve üçü de aynı ilkenin görüntüsüydü: **LSP** — alt sınıf, üst sınıfın verdiği
sözü (görünürlük, tip, yazılabilirlik) daraltamaz. Metot çakışması
gürültülüdür; **özellik çakışması sessizdir** — kod çalışır, yalnızca statik
analiz yakalar. Yeni exception yazarken `$code`, `$message`, `$file`, `$line`
**yasaklı adlardır**.

> Faz 5 ve 6'nın dersleri (42–49) bu bölüme henüz işlenmedi — bkz.
> `PHP-LARAVEL-SETUP-EK-FAZ-5.md` §C ve `-EK-FAZ-6.md` §C.

### Faz 4'te öğrenilenler

**34. 🔴 "Beklediğim yanıtı aldım" ile "beklediğim sebeple aldım" farklı
şeylerdir.** Faz 3'ün üç IDOR testi 404 bekliyor ve 404 alıyordu — ama
Policy'den değil, **eşleşmeyen rotadan**. `InvitationPolicy.php` silinseydi de
geçerlerdi. Ders 24'ün (`actingAs` guard'ı atlar) rota katmanındaki ikizi.

**35. Bir aracı kurmak ile aracın işini yapması ayrı şeylerdir.**
`checkModelProperties: true` Faz 0'dan beri açıktı; ama `parseModelCastsMethod`
kapalı olduğu için **model cast'lerinin tamamı hiç değerlendirilmiyordu.** Bir
ayarın çalıştığı, ancak bir şeyi **yakaladığını gördüğünde** bilinir.

**36. Elle yazılan desen sessizce yanlış olabilir.** ULID regex'i kâğıt üzerinde
kusursuzdu; yalnızca harf durumu yanlıştı (`HasUlids` `strtolower()` uyguluyor)
ve hiçbir araç bunu söylemedi. Framework'ün kısıtı, değeri üreten kodla aynı
depoda durduğu için onunla birlikte değişir.

**37. ORM veritabanı varsayılanını geri okumaz.** `create()` sonrası bellekteki
model DB'nin doldurduğu kolonu taşımaz — ve katı kipin eksik-alan koruması yeni
oluşturulmuş modellerde **bilerek** devre dışıdır (`HasAttributes.php:518`).
Güvenlik ağının deliği tam olarak hatanın durduğu yerdeydi.

**38. Bir optimizasyon altındaki hatayı düzeltmez, hızlandırır.** Bayat cache
bayat bir ETag üretir, tarayıcı onu doğrular ve 304 alır: yanlış veri artık daha
verimli servis edilir.

**39. Bir savunmanın neyi kapatmadığını yazmak, kapattığını yazmak kadar
önemlidir.** ETag ağı kurtarır, CPU'yu değil. `ShouldHandleEventsAfterCommit`
yarışı daraltır, kapatmaz.

**40. Test edilebilirlik ile doğruluk çatışırsa testi uyarla, üretimi değil.**
After-commit dinleyicisi `RefreshDatabase` altında koşmuyor; arayüzü kaldırmak
testi yeşile döndürür ve gerçek bir yarış koşulunu geri getirirdi.

**41. Doğru katmanda alınmış bir karar umulmadık bir yerde ikinci kez işe
yarar.** `localKey` (K44 için yazılmıştı) misafirin `id`'siz adımlarında;
`$invitation->touch()` (frontend'in "son kaydetme" göstergesi için yazılmıştı)
program değişiminde cache'in düşmesinde.

### Faz 3'te öğrenilenler

**26. 🔴 Çalıştırılmayan kod, doğru olduğu varsayılan koddur.** Faz 3'te **üç**
örneği bulundu: iki AuthTest (7 Ağustos'tan beri kırmızı) ve `DatabaseSeeder`
(hiç çalıştırılmamış, var olmayan `name` kolonuna yazıyordu). "Yazıldı" ile
"çalışıyor" farklı durumlardır.

**27. Aynı dil özelliği bir yerde tuzak, başka yerde araçtır.** Kısa devre
`LoginUserAction`'da savunmayı çökertiyordu (A4), `SyncTimelineEventsAction`'da
güncellemeyi çökertecekti, ama `UpdateInvitationAction`'da tam istenen
davranıştı. Ayırt edici soru: *"sağ taraf her durumda çalışmalı mı?"* Aynısı
`?->` için de geçerli: `??` ile gereksiz, doğrudan metot çağrısında zorunlu.

**28. Laravel 11+ taban controller'ı boştur.** `authorizeResource`
`$this->middleware()` çağırıyor; taban sınıf artık `Illuminate\Routing\Controller`'dan
türemediği için o metot yok. Yerine `Gate::authorize()`. Ders 3'ün ailesi.

**29. Tip belirsizliğini sınırda çöz.** `user_id`, `show_*`, `sort_order`
cast'leri ve Resource'taki `(string)` dönüşümleri aynı ilkeden. Güvenlik
karşılaştırmasında patlarsa **herkesi kilitler**: `Model::getCasts()` yalnızca
artan anahtarlı modellerde birincil anahtarı cast ediyor, `HasUlids` kullanan
model **almıyor**.

**30. Savunma kodu her yere değil, güven sınırına yazılır.** Backend'de Action'a
gelen veri güvenilirdi (FormRequest doğrulamıştı); frontend'de servise gelen veri
**değildi** (ağdan geliyordu). İçeride tekrarlamak iki doğruluk kaynağı üretir,
sınırda yazmamak çökme üretir.

**31. Kısıt, sahibi olduğun kurala konur.** `status` backend'in malı ve güvenlik
sınırı — CHECK aldı. `palette`, `category_id`, `preset_id` frontend kataloğunun
anahtarları — almadı. Aksi hâlde her yeni tema backend deploy'u isterdi.

**32. Sözleşme değişince adı da değiştir.** `loadInvitation` → `loadRecord`.
Aynı adla kalsaydı kimliği geçirmeyi unutmak sessizce geçerdi; ad değişince
TypeScript her çağrıyı derleme hatasıyla gösterdi.

**33. Bir aracın kırılması, kırılan yerin hatalı olduğu anlamına gelmez.**
`logout revokes only the current token` kırmızıydı ama `RevokeTokenAction`
doğruydu — kusur **testin kendisindeydi** (guard önbelleği). Ders 18 bu kez ters
yönde işledi.

### Faz 2'de öğrenilenler

**18. 🔴 Bir aracın hata mesajı BELİRTİYİ söyler, SEBEBİ değil.** PHPStan üç kez
kırıldı; ikisi hata mesajındaki tipi körü körüne kopyalamaktan kaynaklandı
(`model property of User` **yazılabilir bir tip değildir** — Larastan onu içeride
üretir). Üçüncüsünde `vendor/larastan/` kaynağı okundu ve mesele tek okumada
çözüldü. **`vendor/` senin emrinde ve okunabilir.**

**19. Docblock, üst sınıftakinden daha iyi bilgi taşımıyorsa yazılmamalıdır.**
`Factory::definition()`'ın dönüş tipini kopyalamaya çalışmak kovaryansı bozdu.
`@return` hiç yazmayınca PHPStan üst sınıftan devraldı ve tip **daha iyi** oldu.

**20. Savunma kodu yazmadan önce framework'ün ne yaptığını oku.**
`prepareForValidation()`'daki `trim()` gereksizdi: `TrimStrings` **global
middleware'i** (Laravel 11+ varsayılan 9 middleware'den biri) zaten kırpıyor.
`ConvertEmptyStringsToNull` da boş string'i `null`'a çevirip `required`'ın
yakalamasını sağlıyor.

**21. 🔴 Rota eşleşmezse grup middleware'i HİÇ çalışmaz.**
`Router::dispatchToRoute()` önce `findRoute()` çağırır; eşleşme yoksa
`NotFoundHttpException` orada fırlar ve `runRouteWithinStack()`'e sıra gelmez.
Faz 1'in `html_request_to_api_still_receives_json` testi bu yüzden **hiç
geçmemişti** — ve faz özetine "doğrulandı" yazılmıştı.

**22. Bir güvenlik kararı başka bir açığı büyütebilir.** K32 (Argon2id) parola
kırmayı zorlaştırdı ama **iki yeni sorun doğurdu**: (a) her istek 64 MB'lık bir
kaynak talebine dönüştü → DoS yüzeyi, (b) doğrulama süresi 200 ms'e çıktı →
zamanlama sinyali güçlendi. K36 (rate limit) birincisini, sahte hash ikincisini
kapatıyor. **Sistemler bir yerden sertleşince başka bir yerden esner.**

**23. Laravel'in `rehash_on_login` ayarı yalnızca `Auth::attempt()` ile çalışır.**
Manuel `Hash::check()` kullanan kodda **etkisizdir**. `hashing.md`'de verilen
"parametreler değişirse hash'ler sessizce güncellenir" sözü, `LoginUserAction`'a
elle `rehashIfNeeded()` eklenene kadar **tutulmuyordu**. Bu, **B4** kuralını
doğuran olay.

**24. `actingAs()` guard'ı atlar.** Token iptalini `actingAs` ile test etmek
**yeşil yanan boş bir test** üretir — `currentAccessToken()` `null` döner ve
hiçbir şey doğrulanmaz. Token yolu test edilecekse `withToken()` kullanılmalı.

**25. Rate limiter anahtarı, kapsadığı rotalara göre seçilmelidir.** `email + IP`
anahtarı, gövdesinde `email` **olmayan** uçlarda (`logout`, `me`) herkes için
`'anonim|IP'` olur ve aynı ağdaki kullanıcılar birbirinin kovasını tüketir.
Farklı tehdit modeli = farklı rota grubu.

---

## 14. Yeni Asistan İçin Hızlı Başlangıç

### Okuma sırası

```
 1. Bu dosyayı oku (bitirdin)              → bağlam, K1–K48 + K64–K71 (K49–K63 ve K72–K86 EK dosyalarında), çalışma kuralları
 2. backend\claude\GOZDEN-GECIRME-RAPORU.md 🔴 23 Eylül — açık bulgular
    backend\claude\FAZ-9-DEVIR.md         ⭐ EN GÜNCEL DEVİR — 15 dakika
 3. backend\CLAUDE.md                     → bağlayıcı kod standartları
 4. docs\08-HATA-SOZLESMESI.md             → hata zarfı — HER hata yolunda geçerli
 5. docs\rehber\fazlar\FAZ-0.md            → 31 kural (Y/V/K/T/S/H/B)
 6. docs\rehber\fazlar\FAZ-1.md            → 19 kural (H10-13/R/M/T6-9/G) + K25-K34
 7. docs\rehber\fazlar\FAZ-2.md            → 20 kural (A/D/E/C/T10-12/B4) + K35-K36
 8. docs\rehber\fazlar\FAZ-3.md            → 15 kural (P/N/D6/E6/C4-5/T13-14/B5) + K37-K44
 9. docs\rehber\fazlar\FAZ-4.md            → 11 kural (O1-6/R6/E7/C6/T15/B6) + K45-K48 + dersler 34-41
10. docs\rehber\fazlar\FAZ-5.md            → 10 kural (L1-4/E8-9/C7/P5/T16/B7) + K49-K53
11. docs\rehber\fazlar\FAZ-6.md            → 11 kural (F1-5/L5-6/A8/T17/E10/B8) + K54-K63
12. docs\rehber\fazlar\FAZ-7.md            ⭐ 10 kural (M5-8/W1-3/L7/P6/E11) + K64-K71 + dersler 50-55
13. docs\07-GELISTIRME-YOL-HARITASI.md     → güncel plan, faz durumları
14. docs\09-TUM-FAZLAR-PLANI.md            → 9 fazın tamamı, ne inşa edeceğiz
15. docs\03-MIMARI-PLAN.md                 → veri modeli (⚠️ §8 GEÇERSİZ)
16. Bölüm 10 → 🔴 "Sıradaki iş (23 Eylül 2026)"
```

> 🔴 **Faz 5, 6 ve 7 özetlerini (10-12) atlama.** Bu dosyanın §7/§11/§13
> bölümlerine yalnızca **Faz 7** işlendi; Faz 5 ve 6'nın kararları/kuralları
> **sadece** kendi faz özetlerinde ve EK dosyalarında duruyor.

> 💡 PHP'ye yeniyseniz `docs\rehber\kavramlar\php-dili.md` ve
> `komutlar.md` başvuru kaynağıdır — baştan sona okunmaz, gerektiğinde bakılır.

### Yazılmış kodu anlamak için

Her kod dosyasının `docs/rehber/` altında birebir yol karşılığı bir eğitim
dokümanı var. Bir dosyanın **neden** öyle yazıldığını anlamak için oraya bak —
kod dosyasında yalnızca kısa yorum vardır (K18).

```
app/Enums/ErrorCode.php  →  docs/rehber/app/Enums/ErrorCode.md
bootstrap/app.php        →  docs/rehber/bootstrap/app.md
```

### Faz 1'in ürettiği zincir (Faz 2 buna eklenecek)

```
1. public/index.php              tek giriş noktası
2. bootstrap/app.php             uygulamayı kurar
3. [ForceJsonResponse]           Accept: application/json   ← M3: grubun BAŞINDA
4. [api grubunun geri kalanı]    throttle vb.
5. routes/api.php                rota eşleşmesi
6. Controller
   ├─ başarılı ────────────────→ JSON
   └─ exception fırladı
        ↓
7. bootstrap/app.php render()    expectsJson() ? devret : null
8. ApiExceptionRenderer          { error: { code, fields?, params?, debug? } }
9. ErrorCode                     status() + filterParams()
```

**Faz 2 bu zincire üç halka ekledi:** FormRequest (4.5 ile 5 arası), Action ve
Resource (6'nın içinde). Faz 4 `SetEtag`'i, Faz 5 `throttle` kovalarını, Faz 7
ise `Gate::authorize` + Action içinde **satır kilidi**ni ekledi. Bir yayın
isteğinin geçtiği dokuz katmanın tamamı: `docs/rehber/fazlar/FAZ-7.md` §4.

### Her dosya için çalışma ritmi

```
1. Komut     → php artisan make:*   (kullanıcı çalıştırır)
2. Kod       → kısa yorumlarla
3. Kılavuz   → docs/rehber/<mimari-yol>/<dosya>.md  (detaylı, PHP'ye sıfırdan)
4. Doğrulama → composer check
5. DUR       → onay bekle
```

### Her faz sonunda

```
docs/rehber/fazlar/FAZ-N.md yazılır:
  amaç · öğrenme hedefleri · hedef/sonuç tablosu · yazılan dosyalar
  · KURULAN KURALLAR · alınan kararlar · bir sonraki faza devir

Not: özetler kuralları kaydeder, süreç anlatmaz.
```

### Yanıt tarzı hatırlatması

- Türkçe, kısa ve doğrudan
- Her kod için: **neden bu yaklaşım / hangi desen / hangi güvenlik-performans
  gerekçesi**
- Kullanıcı öğrenci — kavramı açıkla, ama gereksiz uzatma
- Komutları kullanıcı kendi makinesinde çalıştırıyor; onun yerine geçme
- Bir dosya bitince **onay bekle**
- Bir kararın yanlış olduğunu düşünüyorsan **söyle ve tartış**, tek başına sapma

---

## 15. Açık Sorular

### Frontend — kalan iş (üçü F1'de kapandı, 13 Eylül 2026)

| Konu | Not |
|---|---|
| ~~`errors`/`validation`/`fields` çeviri bölümleri~~ | ✅ F1 |
| ~~`toDisplayError()` çeviri katmanı~~ | ✅ F1 |
| ~~`contracts/error-codes.json` kopyalanması~~ | ✅ F1 — 23 Eylül'de iki kopya karşılaştırıldı, **aynı** |
| `restoreSession()` → açılışta `GET /auth/me` | ⬜ **Hâlâ açık** — `services/auth.ts` oturumu yalnızca `localStorage`'dan okuyor; `/auth/me` hiç çağrılmıyor. İptal edilmiş token ilk API çağrısındaki 401'de yakalanıyor (zararsız), ama kullanıcı bilgisi hiç tazelenmiyor |

### Sonraki fazlarda

| Konu | Ne zaman |
|---|---|
| `routes/web.php` closure'ı (R1/R4 ihlali) | **Faz 9** — `route:cache` orada kırılır |
| 🔴 `event_at` saat dilimi — geri sayım sayacı | **Faz 5'e taşındı** — duvar saati saklanıyor; Berlin'deki misafirde sayaç kayıyor. Doğru çözüm `invitations.timezone` kolonu + iki alan. Faz 4'te bilinçli ertelendi |
| `DeleteInvitationAction` gerekli mi? | **Faz 6** — medya temizliği iş kuralı doğurunca |
| `window.confirm` yerine tasarım sistemine uygun modal | Frontend borcu |
| Genel API hız sınırı (`throttleApi`) | **Faz 5** — `logout`/`me` sınırsız **ve** public uçta 404'ler cache'lenmiyor |
| ~~`HasErrorCode` arayüzü~~ | ✅ **Faz 5'te yazıldı**; Faz 7'nin dört exception'ı da onu uyguluyor |
| ~~PHPStan level 6 → 8~~ | ✅ **Faz 5'te yükseltildi**, Faz 6'da ilk kez gerçekten koştu |
| ~~Ödeme sağlayıcısı arayüzü~~ | ✅ **Faz 7** — `PaymentGateway` + `FakeGateway` (K8). Gerçek `IyzicoGateway` **Faz 9** |
| **Argon2id parametre ayarı** | **Faz 9** — ölçmeden ayarlanmaz; üretim donanımı bilinmiyor |
| `sanctum:prune-expired` zamanlanmış görevi | **Faz 9** — token tablosu sınırsız büyüyor |
| Üretim barındırma + PostgreSQL sürüm eşitlemesi | **Faz 9** |

### 🔴 Faz 7'nin bıraktığı açık kararlar (İsmail'in cevabı bekleniyor)

| # | Konu | Öneri |
|---|---|---|
| 1 | 🔴 **Paket alım kaç yayın açar?** | Bugün **sınırsız** — tek bir 399 ₺'lik paket 100 davetiye yayınlatır. `orders.publish_quota` (int) + `PublishInvitationAction`'da sayaç önerilir. **K43 ancak o zaman tam uygulanmış olur** |
| ~~2~~ | ~~`SubmitRsvpAction::hashIp()` `hash()`, webhook `hash_hmac()` kullanıyor~~ | ✅ **Kapandı (Faz 8):** `App\Support\IpHasher::hash()` = `hash_hmac('sha256', ip, app.key)`; LCV ve iletişim aynı yerden hash'liyor |
| 3 | `app/Contracts/` klasörü | ✅ Faz 7'de ikinci kez kullanıldı (`PublishEntitlementResolver`) ve `CLAUDE.md`'ye işlendi — onay bekliyor |
| 4 | `SubscriptionTier::label()` hâlâ hiçbir yerden çağrılmıyor | Faz 8'de bir fatura/e-posta metni doğmazsa **silinmeli** (ders 26) |
| 5 | `rsvps.id` ULID (K52) | Faz 5'ten beri onay bekliyor |
| 6 | İade var olan yayını geri çekmiyor | `refunded` yeni yayın açmaz ama `invitations.status` bağımsız. İade akışı doğduğunda karar verilmeli |

### 🔴 23 Eylül 2026 gözden geçirmesinin eklediği açık kararlar

> Ayrıntı, senaryo ve öneri: `davetkart-backend-php-laravel/claude/GOZDEN-GECIRME-RAPORU.md`

| # | Konu | Öneri |
|---|---|---|
| 1 | 🔴 **Yayın sonrası paywall aşımı** — `UpdateInvitationAction` modül açmayı kontrol etmiyor | Güncellemede `TierResolver` + `PublishEntitlementResolver`; yetmezse 402 |
| 2 | 🔴 **Geç gelen ödeme** — `failed → paid` reddediliyor, iz bırakmıyor | Geçişe izin ver ya da en azından `critical` log + alarm |
| 3 | Sanctum token'ları **hiç sona ermiyor**; `sanctum:prune-expired` etkisiz | `sanctum.expiration` kararı |
| 4 | Sentry'ye 4xx iş istisnaları gidiyor | `dontReportWhen(status < 500)` |
| 5 | PHP ^8.5 kararı kayıtsız · `phpstan.neon` 80300 | Ya 80500 ya `^8.3` |
| 6 | `TrustProxies` yok — yük dengeleyici arkasında tüm IP kovaları tekleşir | Barındırma yolu seçilince (`docs/10`) |
| 7 | Parola sıfırlama · hesap silme · veri saklama süresi (KVKK) | Lansman öncesi |
| 8 | Fiyat sayfasında satılan ama olmayan özellikler (logosuz yayın, premium tema, video galerisi) | Ya uygula ya fiyat sayfasından kaldır |
| 9 | Ödeme sağlayıcısı Shopier — arayüz uyumu | Rapor §4 |

### ✅ Faz 9'da kapananlar

| Konu | Karar |
|---|---|
| ~~Süresi dolmuş `pending` siparişler~~ | `orders:expire` (9.9) |
| ~~Yetim medya temizliği~~ | `media:prune-orphans` (9.10) |
| ~~`sanctum:prune-expired` zamanlanmış görevi~~ | `routes/console.php` (9.11) |
| ~~`routes/web.php` closure'ı~~ | **Silindi** (9.1). K30'un gerekçesi geçersizleşti: Laravel 13 closure'ları serileştiriyor |
| ~~`DeleteInvitationAction` gerekli mi?~~ | Evet — bir **iş kuralı doğduğu için** (K82) |
| ~~CORS~~ | **K86** — `allowed_origins` daraltıldı, `exposed_headers: ['ETag']` |
| ~~Yüklenenler web kökü altında (K55)~~ | Yol açıldı: `.env` şablonunda `DAVETKART_MEDIA_DISK=s3`; göç **F4** sayesinde eski satırları kırmaz |

### 🔴 Faz 9'un eklediği yeni açık kararlar

| Konu | Not |
|---|---|
| **Zamanlanmış iş koşmazsa kimse bilmez** | `schedule:run` cron'a kurulmazsa hiçbir şey hata vermez. İzleme kararı gerekiyor |
| **Silme sonucu kullanıcıya söylenmiyor** | `DELETE /api/invitations/{id}` → 204. Hak serbest mi bırakıldı, yandı mı — bilinmiyor. Doğru çözüm bir *"siparişlerim"* ucu |
| **Ters yön yetim** (diskte var, satırı yok) | S3 göçünden sonra bir kez elle sayım |
| **Redis'e geçince `throttle` sınıfı değişir** | `ThrottleRequestsWithRedis` — kovalar aynı, davranış birebir değil |
| **Argon2id ölçülmedi** | Hedef ~250 ms/hash; paylaşımlı hostingde `memory_limit` zorlayabilir |

### ⬜ Sonraki fazlara

| Konu | Neden ertelendi |
|---|---|
| Sağlayıcı IP'lerini `throttleApi`'den muaf tutma | IP listesi sağlayıcı dokümanından gelir; anahtar yok |
| Gerçek ödeme sürücüsü + imza sırrı | 🔴 23 Eylül: sağlayıcı **Shopier** (hesap açıldı), `IyzicoGateway` değil. **W2** (`hash_equals`) korunur; **W1** (ham gövde) Shopier'in klasik akışında *form alanlarının* birleşimi olur — rapor §4 |
| `payment.webhook.tolerance_seconds` (replay penceresi) | Faz 0'dan beri config'te, hâlâ okunmuyor — **ya uygula ya sil** (ders 26) |
| Redis · S3 · süpervizör | **K80**: yükseltme; barındırma netleşince |

### Backend dışı

| Konu | Kim |
|---|---|
| Backend hata kodlarının 10 dile çevrilmesi | Frontend — `Notlar/03` |
| Frontend mock katmanlarının HTTP adapter'a çevrilmesi | Frontend — backend endpoint'leri hazır olunca (Faz 2'den itibaren) |
| `contracts/error-codes.json`'un frontend'e kopyalanması | Frontend — Faz 2'de ilk kez gerekecek |
| `scaffold-structure.ps1` silinsin mi? | `make:*` yeterli olduğu için işlevsiz kaldı |

### ✅ Kapananlar

| Konu | Karar |
|---|---|
| ~~`errors:export` çıktısı repoya mı işlenecek?~~ | **K33** — `contracts/error-codes.json`, repoya işlenir |
| ~~Argon2id'ye geçilecek mi?~~ | **K32** — evet, **Faz 2'de fiilen uygulandı** |
| ~~`--check` `composer check`'e eklensin mi?~~ | **K34** — evet, testlerden önce |
| ~~PHPStan level 5 → 6~~ | **K22** — ✅ Faz 2 sonunda yapıldı |
| ~~`rehash_on_login` açık kalsın mı?~~ | Evet — ama manuel `Hash::check` ile **etkisiz** olduğu için `LoginUserAction`'a elle eklendi (ders 23) |
| ~~Ad/soyad tek kolon mu ayrı mı?~~ | **K35** — ayrı, hem veritabanında hem API'de |
| ~~Auth rate limit ne zaman?~~ | **K36** — Faz 5 değil, **Faz 2** |
| ~~Migration'da `ENUM` mü `CHECK` mi?~~ | **K39** — `VARCHAR + CHECK` |
| ~~`InvitationStatus`'te `draft` kalacak mı?~~ | **K38** — hayır, iki değer |
| ~~`prepareForValidation`'daki `trim` ölü kod mu?~~ | Evet — `TrimStrings` zaten yapıyor; Faz 3'te dokunulmadı, Faz 5'te temizlenecek |
| ~~Davetiye kimliği nasıl üretilecek?~~ | **K40 + K44** — ULID, ve program adımlarını da **backend** üretir |
| ~~Plan hesaba mı davetiyeye mi bağlı?~~ | **K42** — ikisi de; tek arayüzden sorulur |
| ~~Cache Action'ın içinde mi dışında mı?~~ | **K45** — dışında; Resource çıktısı olan dizi cache'lenir |
| ~~ETag middleware mi controller içi mi?~~ | **K46** — ayrı middleware (Faz 5 yeniden kullanacak) |
| ~~Faz 4'te yayın ucu yazılsın mı?~~ | **K47** — hayır; salt okuma, doğrulama tinker ile |
| ~~`InvitationPublished` mı `InvitationChanged` mi?~~ | **K48** — `InvitationChanged`, modelden yapısal |
| ~~`PublishInvitationAction` iskeleti silinip yeniden mi üretilsin?~~ | Hayır — **Faz 7'de dolduruldu** (K47'nin sözü tutuldu) |
| ~~`invitations.timezone` nasıl modellensin?~~ | **K71** — duvar saati + IANA kimliği; `timestamptz` **değil** |
| ~~Checkout ucu tek mi iki mi?~~ | **K64** — iki uç; aidiyet URL'nin yapısında (N1) |
| ~~Webhook hangi yolda?~~ | **K65** — `/api/public/` altında (K12 fail-safe) |
| ~~Ödeme gelince davetiye otomatik yayınlansın mı?~~ | **K67** — hayır; yayın ayrı bir kullanıcı eylemi |
| ~~`RsvpQuotaResolver` gerçek kaynağa nasıl bağlanacak?~~ | **K51 kapandı** — bağlama tek satır değişti, `TierRsvpQuotaResolver` silindi |
