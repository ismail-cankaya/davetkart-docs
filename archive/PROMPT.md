> 🗄️ ARŞİV (2026-11-12) — Yerine geçen: `context/PHP-LARAVEL-SETUP.md` ve `prompts/`. Neden: 4 Eylül 2026 durumunu (Faz 7) anlatıyor; sonrasında Faz 8–14 yazıldı.

# Yeni AI Asistanı İçin Başlangıç Prompt'u

> **Son güncelleme:** 4 Eylül 2026
> **Durum:** Faz 0-4 ✅ doğrulandı · Faz 5 kod ✅ · Faz 6 kod ✅ ·
> **Faz 7 kod ✅ (30 commit)** — üçünün de **kapanış ölçütü açık**
> **Sıradaki iş:** 🔴 **Faz 7'yi kapat**, sonra Faz 8
>
> Bu dosya bir **yönlendiricidir**. Kopyalanacak asıl prompt aşağıda §2'de.
> Faz 4'e kadarki eski sürüm: [`PROMPT-ARSIV-FAZ-4.md`](PROMPT-ARSIV-FAZ-4.md)

---

## 1. Hangi prompt'u kullanmalıyım?

| Durum | Kullanılacak dosya |
|---|---|
| 🔴 **Şu an** — Faz 7'nin kodu yazıldı, kapanmadı | `davetkart-backend-php-laravel\claude\PROMPT-FAZ-7-KAPANIS.md` |
| Faz 7 kapandıktan sonra | Faz 8 için yeni bir prompt yazılacak (`PROMPT-FAZ-8.md`) |
| Yalnızca bağlam yüklemek istiyorum | `claude\PHP-LARAVEL-SETUP.md` + `backend\claude\FAZ-7-DEVIR.md` |

> 🔴 **Neden ayrı bir "kapanış" prompt'u var?** Bu projede bir faz *"dosya
> yazıldı"* ile bitmez, **çalışan bir çıktıyla** biter (**B7**). Faz 1, 3 ve
> 4'te üç kez "yeşil" yazıldı ve değildi. Faz 5'ten beri durum alanına
> **gerçekten koşan bir komuta** dayanarak yazılıyor.

---

## 2. Kopyalanacak prompt (Faz 7'yi kapatmak için)

Tam metin şurada — **olduğu gibi kopyala-yapıştır**:

```
D:\Projects\davetkart\davetkart-backend-php-laravel\claude\PROMPT-FAZ-7-KAPANIS.md
```

O dosyanın `---` çizgileri arasındaki bölüm prompt'un kendisidir. İçinde:

- Faz 0-7 durum tablosu
- 7 dosyalık okuma sırası (`FAZ-7-DEVIR.md` ilk sırada)
- Faz 7'nin mimari çekirdeği (K42, K8, M8, M6, P6, W1-W3, K63/K71, K51)
- Plandan üç sapma ve gerekçeleri (K64/K65/K66)
- 10 çalışma kuralı
- İlk oturumda çalıştırılacak komutlar
- 🔴 En riskli iki nokta
- Faz 7 kapandıktan sonra sorulacak **altı açık karar**

---

## 3. Durum özeti (prompt'a gerek kalmadan hızlı bakış)

| Faz | Konu | Kod | `composer check` | Elle doğrulama |
|---|---|:---:|:---:|:---:|
| 0 | Zemin + kalite kapıları | ✅ | ✅ | ✅ |
| 1 | İlk uç + hata zarfı (K20) | ✅ | ✅ | ✅ |
| 2 | Auth dilimi | ✅ | ✅ | ✅ |
| 3 | Invitation CRUD | ✅ | ✅ | ✅ |
| 4 | Public davetiye + cache + ETag | ✅ | ✅ | ✅ |
| 5 | RSVP (auth'suz yazma) | ✅ 17 adım | ✅ (Faz 6'da) | ⬜ 16 adım |
| 6 | Media (dosya kabul eden yol) | ✅ 24 adım | ✅ (3 hata buldu) | ⬜ 18 adım |
| **7** | **Ödeme ve paywall** | ✅ **25 adım / 30 commit** | ⚠️ **1 kez koştu, 7 hata düzeltildi — testler koşmadı** | ⬜ 20 adım |
| 8 | AI asistan + iletişim | ⬜ | — | — |
| 9 | Üretim hazırlığı | ⬜ | — | — |

**Sayılar:** 19 uç nokta · 156 test · PHPStan level 8 · 127 kural · 71 karar ·
55 ders.

**Dal:** `faz-5-and-6` (Faz 7'nin 30 commit'i de burada) · push edilmemiş olabilir.

---

## 4. Faz 7'de ne inşa edildi? (60 saniyelik özet)

**Projenin ticari çekirdeği.** Yayınlamak artık bir ödemeye bağlı ve karar
**tamamen sunucuda** veriliyor — istemciden gelen `tier` bilgisi hiçbir adımda
kullanılmıyor.

Bir yayın isteğinin geçtiği dokuz katman:

```
throttle:api → auth:sanctum → whereUlid → rota bağlaması
  → Gate::authorize('publish')       → değilse 404 (H7, 403 değil)
  → satır kilidi + yeniden oku       → eşzamanlı iki yayın (E9)
  → zaten yayında mı?                → 409 (K68)
  → TierResolver                     → gereken planı SUNUCUDA hesapla (K6)
  → PublishEntitlementResolver       → K42: tekil + paket, TEK arayüz
       ├─ ödeme yok    → 402 PAYMENT_REQUIRED
       └─ plan yetmez  → 402 PAYWALL_TIER_INSUFFICIENT
  → published + published_at
       → InvitationChanged → cache temizlendi (K48 — Action hatırlamıyor)
```

**Üç fazlık üç borç kapandı:**

| Borç | Kaynağı | Nasıl |
|---|---|---|
| `PublishInvitationAction` boş iskeleti | Faz 3 (**K47**) | Dolduruldu |
| `RsvpQuotaResolver`'ın gerçek kaynağı | Faz 5 (**K51**) | Bağlama **tek satır**; `TierRsvpQuotaResolver` silindi |
| `invitations.timezone` | Faz 4→5→6 (**K63**) | Kolon + 6 dosya |

Ve `SubscriptionTier` — **Faz 0'da yazılıp yedi faz boyunca hiç çağrılmayan**
enum — nihayet kullanıldı.

---

## 5. 🔴 Faz 7'de plandan üç sapma — geri alma

`docs/09` Faz 3'ten **önce** yazıldı, sonraki kararları bilmiyor:

| Plan | Gerçek | Neden |
|---|---|---|
| Tek `POST /api/payments/checkout`, gövdede `invitationId` | **İki uç**, kimlik URL'de | **N1** — aidiyet gövdeden gelseydi istemcinin sözüne kalırdı (**K64**) |
| `POST /api/payments/webhook` | `/api/public/payments/webhook` | **K12** fail-safe: auth'suz her rota tek yerde (**K65**) |
| Akışta "`public_slug` üret" | Üretilmiyor | **K40** — `id` zaten ULID ve linkin kendisi (**K66**) |

---

## 6. 🔴 Faz 7'nin devrettiği riskler ve açık kararlar

### Riskler (kapanış sırasında bakılacak)

| Risk | Nerede |
|---|---|
| `orders_paid_at_check` kısıtı `OrderFactory` ile **ilk kez** sınanacak | `FAZ-7.md` §7 |
| Larastan + yeni `Order` modeli (`Builder<Order>` jeneriği) | Aynı |
| `lockForUpdate` ve `hash_equals` **testle doğrulanamıyor** (T15) | `PaywallTest.md` §7.1 |

### Açık kararlar (İsmail'in cevabı bekleniyor)

| # | Konu |
|---|---|
| 1 | 🔴 **Paket alım kaç yayın açar?** Bugün **sınırsız** — K43 tam uygulanmadı |
| 2 | `hashIp()` `hash()`, webhook `hash_hmac()` kullanıyor — ikisi ayrıştı |
| 3 | `app/Contracts/` klasörü onayı |
| 4 | `SubscriptionTier::label()` hâlâ çağrılmıyor — Faz 8'de kullanılmazsa silinmeli |
| 5 | `rsvps.id` ULID (K52) onayı |
| 6 | İade var olan yayını geri çekmiyor |

Tam metin: `docs/rehber/fazlar/FAZ-7.md` §9.

---

## 7. Frontend borcu (dört faz birikti)

`davetkart-frontent` deposu **Faz 4, 5, 6 ve 7'nin hiçbirine uyarlanmadı.**
En kritik madde:

🔴 **`useSubscriptionStore.activeTier` bir oturum içi mock.** Sunucu artık tek
doğruluk kaynağı; frontend'in kendi "satın aldım" hafızası, yayın **402**
dönünce kullanıcıyı şaşırtır.

Tam liste: `docs/rehber/fazlar/FAZ-7.md` §8 (8 madde).
