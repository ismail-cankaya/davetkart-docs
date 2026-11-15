# AUD-2026-11-12 — Genel sistem denetimi

| | |
|---|---|
| **Kimlik** | `AUD-2026-11-12` |
| **Tür** | Salt okunur denetim (mimari, güvenlik, test, frontend/E2E, işletim). Kod değişmedi. |
| **Yürüten** | Claude Code, Fable 5.2 (ana oturum; dilim ajanları kullanım sınırına takıldı) |
| **Tarih** | 12–15 Kasım 2026 |
| **Durum** | ✅ tamamlandı (15 Kasım 2026) |
| **Sonuç** | 62 bulgu: 🔴 0 · 🟠 6 · 🟡 29 · 🟢 22 · 💡 5. Karar: yayına koşullu hazır (altı 🟠 kapanınca) |
| **Rapor** | [`REPORT.md`](REPORT.md) · plan: [`PLAN.md`](PLAN.md) |

## Kapsam ve dallar

| Depo | Denetlenen ref | Commit | Yerel çalışma ağacı (denetim başında) |
|---|---|---|---|
| `davetkart-backend-php-laravel` | `origin/ccr-9a346997-bu6gve` | `d810410af48181753b72c0c89a3128b4f4a97bb7` | `faz15-desing/claude-davetiye@82c7312` (1 commit geride), temiz |
| `davetkart-frontent` | `origin/ccr-9a346997-bu6gve` | `44caa4909557ae2db48b15b67ab12918d5212b02` | `design/claude-davetiye@15889ba` (60 commit geride), temiz |
| `davetkart-docs` | `audit/2026-11-12-full-system-audit` | başlangıç `9e2aba6` | temiz |

**Neden çalışma ağacı değil:** yerel ağaçlar uzaktaki en yeni işin gerisindeydi ve `git switch`/`pull`
bu denetimde yasak. İsmail'in kararıyla (13 Kasım 2026) en yeni uzak dallar `git archive` ile depo
dışına, `D:\Projects\davetkart\_audit-snap\` altına çıkarıldı. Bütün okuma, test, build ve tarayıcı
kanıtı o anlık görüntüden gelir. Kopyaların tablosu: [`PLAN.md`](PLAN.md) §2.

Frontend `main`'deki `47aedc8` (bağımlılık düzeltmesi) denetlenen dalda **yok**; raporda `SEC-14` ve `OPS-01`.

## Ortam

PHP 8.5.12 · Composer 2.10.3 · Laravel 13.35.0 · PostgreSQL 18.4 · Node 24.18.0 · npm 11.16.0 ·
Windows 11 (Herd) · Playwright 1.61.1 + Chromium (başsız) · axe-core 4.10.3. Denetim veritabanları:
`davetkart_aud_{arc,sec,tst,e2e}` ve `…_test` eşleri (yerel PostgreSQL'de, bu denetim için oluşturuldu).

## Şartnameden sapmalar

Tam liste ve gerekçeler: [`REPORT.md`](REPORT.md) Ek A. Özet:

| Sapma | Neden |
|---|---|
| Çalışma ağacı yerine anlık görüntü denetlendi | Yukarıda. |
| Kopyalarda `phpunit.xml` → `DB_DATABASE` değişti | `RefreshDatabase` İsmail'in `davetkart_test` veritabanını silmesin diye. Başka kaynak farkı yok. |
| Kopyaların `.env`'i `.env.example`'dan üretildi | Gerçek `.env`'deki sırlar kopyalara taşınmadı; dış servislerin hepsi kapalı. |
| Dilimleri ajanlar değil ana oturum yürüttü; denetim dört güne yayıldı | Ajanlar ve oturum kullanım sınırına takıldı; iş bulgu dosyalarından sürdürüldü. |
| Tarayıcı yolculukları bağımsız Playwright betikleriyle koştu | Playwright MCP her çağrıda betiği geri yazıyordu (`evidence/scripts/e2e/`). |
| Performans `localhost:4173`'te (üretim build'i), Lighthouse yerine CDP ile ölçüldü | Geliştirme sunucusu paketlenmemiş modül sunar; Lighthouse kurulu değil. |
| Context7 kullanılamadı | Bağlı değil. Sürümler Packagist/npm kaydından. |
| Dört boş parça dosyası silindi | Plan gereği (`02-security-b1/b2.md`, `04-frontend-d1/d2.md`); içerikleri yoktu. |
| Şartname (`PROMPT-…`) depoda yok | Sohbette verildi; gereken bölümleri `PLAN.md`'ye aynen alındı. |

## İçerik

- [`REPORT.md`](REPORT.md): nihai teknik rapor (yönetici özeti, puan kartı, bulgular, regresyon, sözleşme ve
  bağımlılık tabloları, yol haritası, kararlar, dersler, ekler).
- [`PLAN.md`](PLAN.md): dilimler, ortam, regresyon sahipleri, bulgu biçimi.
- [`findings/`](findings/): [`01-architecture.md`](findings/01-architecture.md) (10 bulgu) ·
  [`02-security.md`](findings/02-security.md) (18) · [`03-testing.md`](findings/03-testing.md) (6) ·
  [`04-frontend-e2e.md`](findings/04-frontend-e2e.md) (19) · [`05-operations.md`](findings/05-operations.md) (9).
- [`evidence/`](evidence/): `commands/` (50 komut çıktısı) · `scripts/` (27 betik; `e2e/` altında tarayıcı
  betikleri) · `mutation/` (51 mutant kaydı) · `screenshots/` (80 ekran görüntüsü).

Bulgu sayıları ve tabloları yeniden üretmek için: `node evidence/scripts/90-report-tools.mjs stats`.

## Temizlik (denetim bitince, İsmail)

`D:\Projects\davetkart\_audit-snap\` klasörü ve sekiz `davetkart_aud_*` veritabanı silinebilir; kanıt
dosyaları bu klasördedir, anlık görüntüye bağımlı değildir. `davetkart_aud_e2e` içinde denetimin sahte test
verisi var (bir hesap, dört davetiye, iki sipariş, iki LCV, bir hediye kodu). Ayrıntı: `REPORT.md` Ek E.
