# Frontend Yapılacaklar — Hata Sözleşmesi Uyarlaması

> **Oluşturma:** 31 Temmuz 2026
> **Kaynak karar:** K20 (hata sözleşmesi) · K21 (backend tek dil)
> **Sözleşmenin tamamı:** `davetkart-backend-php-laravel/docs/08-HATA-SOZLESMESI.md`
> **Durum:** Backend Faz 1'de uygulayacak. Frontend bu maddeleri **paralel**
> ilerletebilir — mock veriyle test edilebilir, backend'i beklemeye gerek yok.

---

## 1. Neden bu iş çıktı?

Backend artık **kullanıcıya gösterilecek metin döndürmüyor**. Yerine makine
tarafından okunabilir bir **hata kodu** dönüyor.

```
Önce:  Backend →  "E-posta alanı zaten kullanılıyor."  →  ekrana bas
Sonra: Backend →  { code: "VALIDATION_FAILED",
                    fields: { email: [{ rule: "unique" }] } }
                                    ↓
                  Frontend çevirir  →  ekrana bas
```

**Gerekçe:** Dil kararı sunum katmanının işidir. Frontend zaten 10 dil taşıyor;
backend'in aynı yükü tekrar taşıması gereksiz. Ayrıca metin backend'den
geldiğinde frontend onu bağlama göre değiştiremiyor.

**Yan kazanç:** `SetLocaleFromHeader` middleware'i iptal edildi — backend
`Accept-Language` başlığını okumayacak.

---

## 2. Sözleşme özeti

### 2.1 Doğrulama hatası — HTTP 422

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "fields": {
      "fullName":   [{ "rule": "required" }],
      "guestCount": [{ "rule": "max", "params": { "max": 10 } }]
    }
  }
}
```

### 2.2 İş kuralı hatası

```json
{
  "error": {
    "code": "PAYWALL_TIER_INSUFFICIENT",
    "params": { "requiredTier": "elit" }
  }
}
```

### 2.3 Yerel geliştirmede ek alan

`APP_DEBUG=true` iken yanıta bir `error.debug` bloğu eklenir (mesaj, exception
sınıfı, dosya, satır). **Üretimde hiç üretilmez.**

🔴 `debug` bloğunu **asla ekrana basma** — sadece `console.error` ile
geliştirici konsoluna yaz.

### 2.4 Değişmeyen kurallar

| Kural | Not |
|---|---|
| Başarılı yanıt zarfı `{ data: ... }` | Değişmedi |
| Auth başarı yanıtı **zarfsız** `{ user, token }` | Değişmedi |
| **401 → oturumu düşür** | `api.ts` interceptor'ı aynen kalıyor |
| Alan adları camelCase | `fields` anahtarları da camelCase |

### 2.5 Beklenecek durum kodları

| Durum | Anlam | Frontend davranışı |
|---|---|---|
| 401 | Kimlik yok/geçersiz | Oturumu düşür (mevcut interceptor) |
| 402 | Ödeme gerekli | Plan yükseltme akışına yönlendir |
| 403 | Yetki yok | Uyarı göster |
| **404** | Kaynak yok **veya senin değil** | "Bulunamadı" — 403 bekleme |
| 409 | Durum çakışması | Uyarı + sayfayı tazele |
| 422 | Doğrulama | Alan altı hatalar |
| 429 | Hız sınırı | "Çok hızlısınız" + `retryAfter` |

> ⚠️ **404 sürprizi:** Başkasının davetiyesine erişimde backend bilinçli olarak
> 404 döner (403 değil). Sebep: 403 kaynağın **var olduğunu** doğrular ve ULID
> uzayının taranmasına imkân verir.

---

## 3. Yapılacaklar

### ☐ 3.1 `types.ts` — hata tipleri

```ts
export interface ApiFieldError {
  /** Doğrulama kuralının adı: 'required' | 'email' | 'max' … */
  rule: string;
  /** Çeviride kullanılacak değerler: { max: 10 } */
  params?: Record<string, string | number>;
}

export interface ApiError {
  /** SCREAMING_SNAKE_CASE hata kodu — çeviri anahtarı olarak kullanılır. */
  code: string;
  /** Yalnızca VALIDATION_FAILED yanıtlarında bulunur. */
  fields?: Record<string, ApiFieldError[]>;
  /** İş kuralı hatalarında çeviride kullanılacak değerler. */
  params?: Record<string, string | number>;
  /** Yalnızca APP_DEBUG=true iken. Ekrana basılmaz. */
  debug?: { message?: string; exception?: string; file?: string; line?: number };
}

export interface ApiErrorResponse {
  error: ApiError;
}

/** toDisplayError() çıktısı — doğrudan render edilebilir. */
export interface DisplayError {
  code: string;
  status?: number;
  /** Form üstünde gösterilecek genel mesaj. */
  message: string;
  /** Alan adı → alan altında gösterilecek mesaj. */
  fieldMessages: Record<string, string>;
}
```

---

### ☐ 3.2 Çeviri anahtarları — `locales/<dil>/translation.json`

Mevcut dosyaya **üç yeni üst seviye bölüm** eklenecek. `i18n.ts`'e dokunmaya
gerek yok — tek `translation` ad alanı yeterli.

```json
{
  "nav": { "...": "mevcut" },

  "errors": {
    "UNKNOWN": "Beklenmeyen bir hata oluştu. Lütfen tekrar deneyin.",
    "NETWORK_ERROR": "Sunucuya ulaşılamıyor. İnternet bağlantınızı kontrol edin.",
    "TIMEOUT": "İşlem zaman aşımına uğradı. Lütfen tekrar deneyin.",
    "VALIDATION_FAILED": "Lütfen formdaki hataları düzeltin.",
    "INVALID_CREDENTIALS": "E-posta veya parola hatalı.",
    "REGISTRATION_FAILED": "Kayıt tamamlanamadı. Bilgilerinizi kontrol edin.",
    "RESOURCE_NOT_FOUND": "Aradığınız içerik bulunamadı.",
    "RATE_LIMITED": "Çok fazla deneme yaptınız. {{retryAfter}} saniye sonra tekrar deneyin.",
    "PAYWALL_TIER_INSUFFICIENT": "Bu özellik {{requiredTier}} planında açılıyor.",
    "RSVP_QUOTA_EXCEEDED": "Katılım kontenjanı doldu.",
    "RSVP_DEADLINE_PASSED": "Katılım bildirimi için son tarih geçti.",
    "INVITATION_ALREADY_PUBLISHED": "Bu davetiye zaten yayında.",
    "FILE_TOO_LARGE": "Dosya çok büyük.",
    "SERVER_ERROR": "Sunucuda bir sorun oluştu. Kısa süre sonra tekrar deneyin."
  },

  "validation": {
    "invalid": "{{field}} geçersiz.",
    "required": "{{field}} zorunludur.",
    "email": "{{field}} geçerli bir e-posta adresi olmalıdır.",
    "unique": "{{field}} zaten kullanılıyor.",
    "confirmed": "{{field}} doğrulaması eşleşmiyor.",
    "min": "{{field}} en az {{min}} karakter olmalıdır.",
    "max": "{{field}} en fazla {{max}} olabilir.",
    "numeric": "{{field}} sayı olmalıdır.",
    "date": "{{field}} geçerli bir tarih olmalıdır.",
    "url": "{{field}} geçerli bir bağlantı olmalıdır.",
    "image": "{{field}} bir görsel olmalıdır."
  },

  "fields": {
    "fullName": "Ad soyad",
    "email": "E-posta",
    "password": "Parola",
    "title": "Başlık",
    "eventDate": "Etkinlik tarihi",
    "venueName": "Mekân adı",
    "mapUrl": "Harita bağlantısı",
    "guestName": "Misafir adı",
    "guestCount": "Kişi sayısı",
    "file": "Dosya"
  }
}
```

**Değişken sözdizimi `{{ }}`** — i18next standardı, backend'in `:param`
sözdiziminden farklı.

> 🔴 **Önce `en`'i doldur.** `i18n.ts` içinde `fallbackLng: 'en'` var. Bir
> anahtar `tr`'de eksik ama `en`'de varsa i18next otomatik İngilizceye düşer —
> kullanıcı ham kod yerine anlamlı metin görür. Bu bedava güvenlik ağını
> kaybetmemek için **her yeni anahtar önce `en`'e** yazılmalı.

---

### ☐ 3.3 `services/api.ts` — `toDisplayError()`

Tek dönüşüm noktası. Hiçbir bileşen `error.response.data`'ya doğrudan
bakmamalı.

```ts
import axios from 'axios';
import i18n from '../i18n';
import type { ApiErrorResponse, DisplayError } from '../types';

/** Alan adını okunur etikete çevirir; karşılığı yoksa ham adı döner. */
function fieldLabel(name: string): string {
  return i18n.t(`fields.${name}`, { defaultValue: name });
}

/**
 * Her HTTP hatasını render edilebilir tek bir şekle indirger.
 * Bilinmeyen kod, ağ hatası ve bozuk gövde dahil HER durumda
 * dolu bir `message` döndürür — boş ekran gösterilmez.
 */
export function toDisplayError(error: unknown): DisplayError {
  const unknown = (): DisplayError => ({
    code: 'UNKNOWN',
    message: i18n.t('errors.UNKNOWN'),
    fieldMessages: {},
  });

  if (!axios.isAxiosError(error)) return unknown();

  // Yanıt hiç gelmedi: ağ kopuk veya 15 sn timeout doldu.
  if (!error.response) {
    const code = error.code === 'ECONNABORTED' ? 'TIMEOUT' : 'NETWORK_ERROR';
    return { code, message: i18n.t(`errors.${code}`), fieldMessages: {} };
  }

  const status = error.response.status;
  const apiError = (error.response.data as Partial<ApiErrorResponse>)?.error;

  if (!apiError?.code) return { ...unknown(), status };

  // Yerel geliştirme yardımı — asla ekrana basma.
  if (apiError.debug) console.error('[API]', apiError.code, apiError.debug);

  const fieldMessages: Record<string, string> = {};
  for (const [name, errors] of Object.entries(apiError.fields ?? {})) {
    const first = errors?.[0];
    if (!first) continue;
    fieldMessages[name] = i18n.t(`validation.${first.rule}`, {
      field: fieldLabel(name),
      ...first.params,
      // Kural çevirisi yoksa genel "geçersiz" mesajına düş.
      defaultValue: i18n.t('validation.invalid', { field: fieldLabel(name) }),
    });
  }

  return {
    code: apiError.code,
    status,
    message: i18n.t(`errors.${apiError.code}`, {
      ...apiError.params,
      // 🔴 Bilinmeyen kod: backend yeni kod eklediğinde boş ekran olmasın.
      defaultValue: i18n.t('errors.UNKNOWN'),
    }),
    fieldMessages,
  };
}
```

**İki katmanlı yedek (fallback) var:**

1. `defaultValue` — anahtar hiçbir dilde yoksa genel metne düşer
2. `fallbackLng: 'en'` — anahtar `tr`'de yok ama `en`'de varsa İngilizce görünür

---

### ☐ 3.4 Formlarda kullanım

```tsx
const [error, setError] = useState<DisplayError | null>(null);

async function handleSubmit(values: RegisterPayload) {
  try {
    await authService.register(values);
  } catch (e) {
    setError(toDisplayError(e));
  }
}

// Form üstü genel mesaj
{error && <Alert>{error.message}</Alert>}

// Alan altı mesaj
<Input name="email" />
{error?.fieldMessages.email && <FieldError>{error.fieldMessages.email}</FieldError>}
```

---

### ☐ 3.5 🔴 Auth formlarında özel durum

Backend **kullanıcı sayımı (user enumeration) açığını kapatmak için** auth
hatalarında `fields` **döndürmez**:

| Endpoint | Yanıt | Frontend |
|---|---|---|
| `/auth/login` | `INVALID_CREDENTIALS`, `fields` **yok** | Form **üstünde** tek mesaj göster |
| `/auth/register` | `REGISTRATION_FAILED`, `fields` **yok** | Aynı |

**Neden?** "Parola hatalı" ile "kullanıcı yok" ayrımı yapılırsa, saldırgan
elindeki e-posta listesini forma girip hangilerinin kayıtlı olduğunu öğrenir.

**Frontend'e düşen:** Bu iki formda alan altı hata gösterme mantığı
kurgulanmamalı — hata **form seviyesinde** gösterilecek. İstemci tarafı
doğrulama (boş alan, e-posta biçimi) elbette alan altında kalabilir; sunucudan
gelen auth hatası kalmayacak.

---

## 4. Backend'den gelecek katalog dosyası

Backend `php artisan errors:export` komutuyla şunu üretecek:

```json
{
  "generatedAt": "2026-07-31T12:00:00Z",
  "codes": {
    "VALIDATION_FAILED":         { "status": 422, "params": [] },
    "PAYWALL_TIER_INSUFFICIENT": { "status": 402, "params": ["requiredTier"] },
    "RATE_LIMITED":              { "status": 429, "params": ["retryAfter"] }
  }
}
```

**Kullanımı:** Dosya frontend'e kopyalanır; küçük bir script `errors` bölümünde
eksik anahtarları listeler.

> Bu tek yönlü bir üretimdir — iki repo arasında **bağımlılık kurulmaz**.
> (Daha önce denenen `davetkart-contracts` paylaşılan tip paketi hiç
> doldurulmadığı için kaldırılmıştı.)

---

## 5. Test önerisi

Backend'i beklemeden mock'la test edilebilir:

```ts
it('bilinmeyen kod için genel mesaj döner', () => {
  const err = mockAxiosError(500, { error: { code: 'HENUZ_OLMAYAN_KOD' } });
  expect(toDisplayError(err).message).toBe(i18n.t('errors.UNKNOWN'));
});

it('alan hatasını çevirir ve parametreyi yerleştirir', () => {
  const err = mockAxiosError(422, {
    error: { code: 'VALIDATION_FAILED',
             fields: { guestCount: [{ rule: 'max', params: { max: 10 } }] } },
  });
  expect(toDisplayError(err).fieldMessages.guestCount)
    .toBe('Kişi sayısı en fazla 10 olabilir.');
});

it('ağ hatasında boş mesaj dönmez', () => {
  expect(toDisplayError(mockNetworkError()).message).not.toBe('');
});
```

---

## 6. Kontrol listesi

- [ ] `types.ts` → `ApiError`, `ApiFieldError`, `ApiErrorResponse`, `DisplayError`
- [ ] `locales/en/translation.json` → `errors`, `validation`, `fields` (**önce bu**)
- [ ] `locales/tr/translation.json` → aynı üç bölüm
- [ ] Kalan 8 dil (es, fr, de, zh, hi, ar, ru, pt)
- [ ] `services/api.ts` → `toDisplayError()`
- [ ] Kayıt / giriş formları → form seviyesi hata
- [ ] Davetiye editörü → alan altı hata
- [ ] LCV formu → alan altı + kota hatası
- [ ] Bilinmeyen kod testi
- [ ] `error.debug` ekrana basılmıyor doğrulaması

---

## 7. Açık sorular

| Konu | Durum |
|---|---|
| Hata gösterimi: toast mı, alan altı mı, ikisi de mi? | Frontend kararı |
| 8 ek dilin çevirileri kim/nasıl yapacak? | Ticari karar |
| ~~`errors:export` çıktısı repoya mı işlenecek?~~ | ✅ **K33** — `contracts/error-codes.json`, repoda |
| 429 sonrası otomatik yeniden deneme olacak mı? | Karar yok |

---

# BÖLÜM II — Faz 2 ile gelen SÖZLEŞME DEĞİŞİKLİKLERİ

> **Eklendi:** 6 Ağustos 2026 · Faz 2 kapanışı
> **Durum:** ✅ **TAMAMLANDI** — backend ve frontend sözleşmesi uyumlu.
> Aşağıdaki bölümler **kayıt** olarak duruyor: ne değişti, neden değişti.

## 8. 🔴 K35 — ad ve soyad ayrıldı

Backend artık tek bir `fullName` alanı **kabul etmiyor** ve **döndürmüyor**.

### 8.1 Neden?

Birleştirmek kolay, birleşmiş veriyi ayırmak **imkânsızdır**. "Ayşe Nur Kaya"
için ad "Ayşe" mi "Ayşe Nur" mü olduğu hiçbir algoritmayla çıkarılamaz.

Ayrı tutmanın somut kazançları: fatura ve resmî belge soyadı tek başına ister
(Faz 7), soyada göre sıralama mümkün olur, "Sayın Kaya" hitabı kurulabilir.

Ve birleştirme bir **sunum kararıdır** — K20'nin ilkesi gereği frontend'e ait.
Backend `fullName` gönderirse "Merhaba Ayşe", "Sayın Kaya", "KAYA, Ayşe"
seçeneklerinin hiçbiri kurulamaz.

### 8.2 Değişen istek — `POST /api/auth/register`

```diff
- { "fullName": "Ayse Yildirim", "email": "...", "password": "..." }
+ { "firstName": "Ayse", "lastName": "Yildirim", "email": "...", "password": "..." }
```

| Alan | Kural |
|---|---|
| `firstName` | zorunlu, string, **en fazla 60** karakter |
| `lastName` | zorunlu, string, **en fazla 60** karakter |
| `email` | zorunlu, e-posta biçimi, en fazla 255 |
| `password` | zorunlu, **en az 8**, en fazla 255 |

### 8.3 Değişen yanıt — `user` nesnesi

```diff
  {
    "user": {
      "id": "1",
-     "fullName": "Ayse Yildirim",
+     "firstName": "Ayse",
+     "lastName": "Yildirim",
      "email": "ayse@ornek.test"
    },
    "token": "1|kJ8x..."
  }
```

### 8.4 ✅ Dokunulan dosyalar

| Dosya | Ne yapıldı | ✓ |
|---|---|:---:|
| `src/types.ts` | `AuthUser` ve `RegisterPayload` → `firstName` + `lastName` | ✅ |
| `src/utils/user.ts` | 🆕 `fullName(user)` yardımcısı — birleştirmenin **tek yeri** | ✅ |
| `src/pages/RegisterPage.tsx` | Tek input → **iki input** (`Ad` / `Soyad`), `maxLength={60}` | ✅ |
| `src/pages/LoginPage.tsx` | `fullName(user)` | ✅ |
| `src/pages/DashboardPage.tsx` | `fullName(user)` | ✅ |
| `src/components/layout/Header.tsx` | `fullName(user)` | ✅ |
| `src/services/auth.ts` | Yanıt şekli doğrulaması (`firstName`/`lastName` kontrolü) | ✅ |

**Birleştirme tek yerde toplandı** — `src/utils/user.ts`:

```ts
export function fullName(user: Pick<AuthUser, 'firstName' | 'lastName'>): string {
  return [user.firstName, user.lastName]
    .filter((part): part is string => typeof part === 'string' && part.trim() !== '')
    .map((part) => part.trim())
    .join(' ');
}
```

`filter` neden var? Yarım dolu bir çiftte (yalnızca ad girilmişse) araya sarkan
boşluk basılmaz. Backend `UserResource`'taki `trim()` ile aynı savunma
mantığı — iki uçta da.

> 💡 Şu an her yerde tam ad gösteriliyor. `Header` gibi dar alanlarda yalnızca
> `user.firstName` kullanmak daha iyi durabilir; artık **seçim mümkün** —
> `fullName` gönderilseydi olmazdı. K35'in kazandırdığı esneklik tam olarak bu.

---

## 9. 🔴 401'in iki anlamı var — interceptor düzeltilmeli

`services/api.ts` interceptor'ı şu an **her** 401'de oturumu düşürüyor. Faz 2
ile iki farklı 401 üretiliyor:

| Kod | Ne demek | Frontend ne yapmalı |
|---|---|---|
| `UNAUTHENTICATED` | Token yok / geçersiz / iptal edilmiş | ✅ Oturumu düşür, giriş sayfasına at |
| **`INVALID_CREDENTIALS`** | Girilen e-posta veya parola yanlış | 🔴 **Formda kal**, hatayı göster |

Şu anki davranışla, kullanıcı yanlış parola girdiğinde frontend onu "oturumun
düştü" sanıp yönlendiriyor — zaten giriş sayfasında olduğu için **form
sıfırlanıyor** ve yazdıkları uçuyor.

### ✅ 9.1 Yapıldı — `services/api.ts`

```ts
export function apiErrorCode(error: unknown): string | null { … }
export function apiErrorParams(error: unknown): Record<string, unknown> { … }

api.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (
      axios.isAxiosError(error) &&
      error.response?.status === 401 &&
      apiErrorCode(error) !== 'INVALID_CREDENTIALS'      // ← ayrım
    ) {
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);
```

`apiErrorCode` / `apiErrorParams` **geçici yardımcılardır**: kalıcı olan
`toDisplayError()` çeviri katmanı (§3.3) henüz yazılmadı. O geldiğinde bu ikisi
onun içine taşınacak — şimdilik hata kodunu okumanın tek yeri burası.

---

## 10. Yeni uç noktalar

### 10.1 `POST /api/auth/logout` — davranış netleşti

| Konu | Sonuç |
|---|---|
| Başarılı | **`204 No Content`** — gövde yok |
| Etkisi | 🔴 **Yalnızca isteği taşıyan token** iptal edilir |
| Diğer cihazlar | Etkilenmez — telefondan çıkmak laptop'ı düşürmez |
| İkinci çağrı | `401` döner ve bu **doğrudur** — mevcut `.catch(() => {})` yeterli |

`services/auth.ts`'teki `revokeSession()` **olduğu gibi çalışıyor**, değişiklik
gerekmiyor.

### 10.2 `GET /api/auth/me` — yeni, henüz kullanılmıyor

```json
{ "data": { "id": "1", "firstName": "Ayse", "lastName": "Yildirim", "email": "..." } }
```

🔴 **Zarf `data` VAR.** `login`/`register`'daki zarfsız istisna yalnızca o iki uç
için geçerli.

**Önerilen kullanım:** `restoreSession()` şu an `localStorage`'daki token'a
körü körüne güveniyor. Uygulama açılışında `me` çağrılırsa iptal edilmiş bir
token yakalanır:

```
200 → oturum geçerli, devam
401 → token iptal edilmiş, clearSession() + giriş ekranı
```

---

## 11. 🔴 Hız sınırı (K36) — 429 artık gerçek

`/auth/register` ve `/auth/login` sınırlı:

| Limit | Anahtar | Amacı |
|---|---|---|
| **5/dakika** | e-posta + IP | Brute-force |
| **20/dakika** | IP | Password spraying |

Aşılırsa:

```json
{ "error": { "code": "RATE_LIMITED", "params": { "retryAfter": 47 } } }
```

`Retry-After` HTTP başlığı da gelir.

### ✅ 11.1 Yapıldı — kullanıcıya doğru sebep söyleniyor

`LoginPage` ve `RegisterPage` artık `429`'u ayırt ediyor:

```ts
if (apiErrorCode(e) === 'RATE_LIMITED') {
  const seconds = Number(apiErrorParams(e).retryAfter ?? 60);
  toast(`Çok fazla deneme yaptınız. ${seconds} saniye sonra tekrar deneyin.`, 'info');
} else {
  toast('Giriş yapılamadı. Bilgilerinizi kontrol edip tekrar deneyin.', 'info');
}
```

**Neden şart:** `429` durumunda *"bilgilerinizi kontrol edin"* demek
**yanıltıcıdır** — bilgiler doğru olsa da istek reddedilir. Kullanıcı doğru
parolasını tekrar tekrar dener, her deneme limiti uzatır.

### ☐ 11.2 Kalan (isteğe bağlı)

- Butonu `retryAfter` saniye boyunca **devre dışı bırakıp geri sayım göstermek**
- 🔴 Otomatik yeniden deneme **yapma**: limiti tüketir, süreyi uzatır

> ⚠️ Geliştirme sırasında formu art arda denerken `429` alabilirsin. Hata değil.

---

## 12. E-posta artık büyük/küçük harf duyarsız

Backend e-postayı hem yazarken hem okurken küçük harfe indiriyor.
`Ayse@Ornek.TEST` ile kaydolan kullanıcı `ayse@ornek.test` ile giriş yapabilir.

**✅ Yapıldı:** Giriş ve kayıt formlarındaki e-posta alanlarına
`autoCapitalize="none"`, `autoCorrect="off"`, `spellCheck={false}` eklendi.
Mobil klavyenin ilk harfi büyütmesi backend'in küçülttüğü değerle görsel
tutarsızlık yaratıyordu.

### ✅ 12.1 Bonus — giriş formundan `minLength` kaldırıldı

`LoginPage`'in parola alanında `minLength={6}` vardı. Kaldırıldı, çünkü
**giriş formu parola politikası uygulamaz** — backend'deki `LoginRequest` ile
aynı gerekçe (kural **D3**):

> Kural bir gün 12'ye çıkarsa, 9 karakterli parolayla kaydolmuş kullanıcı
> **doğru parolasıyla** giriş yapamaz hâle gelir. Kural veri **üretilirken**
> uygulanır, **okunurken** değil.

`RegisterPage`'de ise `minLength={8}` **duruyor** ve durmalı — orası üretim
anıdır, backend'in `Password::min(8)` kuralının aynası.

---

## 13. `contracts/error-codes.json` — kopyalanmayı bekliyor

Backend `php artisan errors:export` ile üretiyor ve dosya **repoda işli**
(K33). Faz 2'de ilk kez gerçekten lazım.

```
davetkart-backend-php-laravel/contracts/error-codes.json
                    ↓ kopyala
davetkart-frontent/src/contracts/error-codes.json
```

Küçük bir script `errors` bölümünde eksik anahtarları listelesin. Backend
tarafında `errors:export --check` `composer check` zincirinde olduğu için
katalog **eskimiyor** (K34).

---

## 14. Faz 2 kontrol listesi

**Kırıcı — bunlar olmadan kayıt/giriş çalışmaz:**

- [x] `types.ts` → `AuthUser` ve `RegisterPayload`: `firstName` + `lastName`
- [x] `utils/user.ts` → `fullName()` yardımcısı
- [x] `RegisterPage.tsx` → iki ayrı input
- [x] `Header.tsx`, `DashboardPage.tsx`, `LoginPage.tsx` → `fullName(user)`
- [x] `services/auth.ts` → yanıt şekli doğrulaması

**Davranışsal:**

- [x] `api.ts` interceptor → `INVALID_CREDENTIALS`'ta oturumu **düşürmüyor**
- [x] `429` → kullanıcıya doğru sebep ve `retryAfter` söyleniyor
- [x] Auth formlarında hata **form seviyesinde** (toast) — `fields` gelmiyor
- [x] E-posta alanlarında `autoCapitalize="none"`
- [x] `LoginPage` → parola `minLength` kaldırıldı (D3)

**Kalan — Faz 2'yi bloke etmiyor:**

- [ ] `locales/*/translation.json` → `errors`, `validation`, `fields` bölümleri (§3.2)
- [ ] `services/api.ts` → `toDisplayError()` çeviri katmanı (§3.3)
- [ ] `restoreSession()` → açılışta `GET /auth/me` ile token doğrula
- [ ] `429` → butonu geri sayımla devre dışı bırak
- [ ] `contracts/error-codes.json` kopyala + eksik anahtar kontrolü

> ⚠️ Kalan maddeler **K20'nin (hata sözleşmesi) frontend tarafıdır**, K35'in
> değil. Şu an toast'larda sabit Türkçe metinler var; `toDisplayError()`
> geldiğinde 10 dile açılacaklar.

---

## 15. Uçtan uca doğrulama

İkisi birden çalışırken:

```powershell
# 1. terminal — backend
cd davetkart-backend-php-laravel
php artisan serve

# 2. terminal — frontend
cd davetkart-frontent
npm run dev
```

**Faz 2'nin bitiş ölçütü:** Tarayıcıdan **gerçek hesapla kayıt olup giriş
yapabilmek.** Token `localStorage`'a düşüyor, sayfa yenilenince oturum
korunuyor.

Backend uç noktalarının tek tek doğrulaması:
`davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-2-ELLE-DOGRULAMA.md`

---

## 16. Faz 4 sonrası frontend durumu (27 Ağustos 2026)

Faz 4'te frontend'de **iki** dosya değişti; bu bölüm hangi maddelerin kapandığını
ve hangilerinin hâlâ açık olduğunu söyler.

### ✅ Kapananlar

| Madde | Nerede |
|---|---|
| `InvitePage.tsx` yerel store'u çiziyordu (`TODO(backend)`) | ✅ `GET /api/public/invitations/:id` ucuna bağlandı |
| Misafir sayfasında şablon editörün store'undan geliyordu | ✅ Artık `invitation.imageTheme`'den çözülüyor |
| Public uç için hata gösterimi yok | ✅ `apiErrorCode()` ile `RESOURCE_NOT_FOUND` ↔ taşıma hatası ayrımı yapılıyor |

### 🔴 Yeni sözleşme: public gövde, sahibin gövdesinden FARKLI

`src/services/publicInvitation.ts` bunu tipte anlatıyor. Backend **kapalı
modülün verisini hiç göndermiyor** (C6):

| Modül kapalıysa | Gövdede olmayan anahtarlar |
|---|---|
| `showGift` | `bankName`, `accountHolder`, `iban`, `giftOptions` |
| `showTimeline` | `timelineEvents` |
| `showGallery` | `galleryImages` |
| `showRSVP` | `rsvpDeadline`, `askMenuPreference` |

Ayrıca `status`, `updatedAt` ve program adımlarının `id`'si de **gelmiyor**.

`types.ts` **değiştirilmedi** — eksik alanlar servis sınırında tamamlanıyor.
Bu, Faz 3'te `whenLoaded()` için reddettiğimiz davranış değil: orada eksiklik
"bilinmiyor" demekti ve doldurulan değer çiziliyordu; burada "sana ait değil"
demek ve `InvitationComposition` kapalı modülün bileşenini mount bile etmiyor,
yani doldurulan varsayılan hiçbir zaman çizilmiyor.

### Hâlâ açık — Faz 5 ve sonrası

| Madde | Ne zaman |
|---|---|
| `RsvpModal` yerel store'la çalışıyor, sunucuya göndermiyor | **Faz 5** — `POST /api/public/invitations/{id}/rsvps` |
| Sahibin LCV paneli (15 sn polling, ETag'li) | **Faz 5** |
| `toDisplayError()` çeviri katmanı (§3.3) | Açık — `apiErrorCode()` hâlâ geçici çözüm |
| `errors`/`validation`/`fields` çeviri bölümleri (§3.2) | Açık |
| `contracts/error-codes.json` kopyalanması (§13) | Açık |
| `restoreSession()` → açılışta `GET /auth/me` (§10.2) | Açık |
| `galleryImages` her zaman `[]` | Faz 6 |
| Geri sayım sayacı saat dilimi | Faz 5'te karara bağlanacak — `invitations.timezone` |
| 🔴 Depo CRLF/LF karmaşası: `git add -A` 473 dosyayı sürüklüyor | `.gitattributes` kararı bekliyor; şimdilik dosyaları **tek tek** ekle |

### Yeni kılavuzlar

`davetkart-frontent/docs/rehber/src/` altına iki dosya eklendi:
`services/publicInvitation.md` ve `pages/InvitePage.md`.
