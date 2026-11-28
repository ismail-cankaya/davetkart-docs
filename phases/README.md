# `phases/`

Faz bazında plan, rapor, commit komutları ve fazın ürettiği ara çıktılar. Her faz kendi klasöründe
(`faz-NN`). Fazın **resmî özeti ve elle doğrulama betiği** kod deposunda kalır
(`davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-NN.md`); burada o özetin dışındaki kayıtlar durur.

## Faz tablosu

Durum sütunu backend `docs/rehber/fazlar/README.md`'den alındı (orada yazan test sayıları **bulut
çalışma alanında** koştu, İsmail'in makinesinde değil).

| Faz | Konu | Durum | Dal | Bu depoda | Ana dosya (backend) |
|---|---|---|---|---|---|
| 0–9 | Temel, kimlik, davetiye, yayın, LCV, medya, ödeme, asistan, bakım | Kod ✅; ayrıntı `context/PHP-LARAVEL-SETUP.md` §10 | — | — | `docs/rehber/fazlar/FAZ-0.md` … `FAZ-9.md` |
| F1–F7 | Frontend yakalama (Faz 9 ile 10 arası) | ✅ 13–16 Eylül 2026 (`PHP-LARAVEL-SETUP.md` başlığı) | — | [`frontend-catch-up/`](frontend-catch-up/FRONTEND-YAKALAMA-PLANI.md) | — |
| 10 | Sertleştirme ve lansman eksikleri | Plan: [`faz-10/FAZ-10-PLANI.md`](faz-10/FAZ-10-PLANI.md); `FAZ-10.md` yazılmadı | `faz-10` | [`faz-10/`](faz-10/) | — |
| 11 | Hediye kodu | ⚠️ kod ✅ · elle doğrulama bekliyor | `faz-11-hediye-kodu` | [`faz-11/`](faz-11/) | `FAZ-11.md` |
| 12 | Shopier ile kartla ödeme | ⚠️ kod ✅ · §A boş, gerçek Shopier'e karşı sınanmadı | `faz-12-shopier` | [`faz-12/`](faz-12/FAZ-12-RAPOR.md) | `FAZ-12.md` |
| 13 | Fiyat API'si, indirimler, ödeme yöntemi anahtarı | ⚠️ kod ✅ · elle doğrulama bekliyor | `faz-13-payment-settings` | [`faz-13/`](faz-13/) | `FAZ-13.md` |
| 14 | Hesap ayarları: Planlarım, iptal/iade, profil, parola, oturumlar, e-posta | ⚠️ kod ✅ (bkz. backend README) | `faz-14-account-settings` | [`faz-14/`](faz-14/) | `FAZ-14.md` |
| 18 | Denetim düzeltmeleri (`AUD-2026-11-12`, altı 🟠 bulgu) | ⚠️ kod ✅ 6/6 (20 Kasım 2026) · `v1.1.0` etiketi bekliyor: `composer audit` kırmızı (`SEC-07`) · sunucu adımları koşmadı · → 20 Kasım: `SEC-07` Faz 19.1'de ele alındı (lock temiz); `vendor` + kapılar ve `v1.1.0` [`faz-19/FAZ-19-SEC-07-COMMIT-KOMUTLARI.md`](faz-19/FAZ-19-SEC-07-COMMIT-KOMUTLARI.md) §0, §5 | `faz-18-audit-fixes` + `fix/…` dalları | [`faz-18/`](faz-18/README.md) | `FAZ-18.md` (backend) |
| 19 | Denetimin orta öncelikli bulguları (`AUD-2026-11-12`, 28 🟡) | ⚠️ kod ✅ 28/28, birleşti (25 Kasım 2026) · `v1.2.0` etiketi bekliyor · ~~PHPStan iç hatası (#11)~~ 25 Kasım'da kapandı; 26 Kasım'da engel `composer audit` (`SEC-51`) → Faz 20.2 | `faz-19-audit-fixes` + `fix/…` / `docs/…` dalları | [`faz-19/`](faz-19/README.md) | `FAZ-19.md` (backend; başta kapanış özeti) |
| 20 | Faz 19 sonrası kritik hatalar (`AUD-2026-11-26`): yerel şema geride → Hesap Ayarları 500; `schema` hazır olma kontrolü, Symfony güvenlik yaması, yerel eşitleme | ⏳ 26 Kasım 2026 · ayrıntı takip tablosunda | `faz-20-critical-fixes` + `fix/2026-11-26-…` · docs `docs/2026-11-26-faz-20-critical-fixes` | [`faz-20/`](faz-20/README.md) | `FAZ-20.md` (backend) |
| 21 | Ertelenmiş düşük bulgular ve açık kararlar (`AUD-2026-11-12` 🟢/💡 + `AUD-2026-11-26` §4b): 18 madde, **tek ajan tek oturumda**, madde başına commit (ilk adı Faz 22'ydi, 26 Kasım'da Faz 21'e çevrildi). K265–K275 | ✅ 27 Kasım 2026 · 18/18 (bloke yok; 21.13, 21.14 plan · 21.15, 21.17 liste) · `composer check` 1354/1354, `audit` temiz, frontend check/e2e 6/6 · `main`'e birleştirme, sunucu adımları ve CI İsmail'in | backend/frontend `faz-21-backlog` · docs `docs/2026-11-27-faz-21-backlog` | [`faz-21/`](faz-21/README.md) | backend `docs/rehber/fazlar/FAZ-21.md` |
| 22 | Yayın öncesi son faz: eksikler ve düzenlemeler (madde listesi açık). 22.1 e-posta doğrulaması satın almayı engellemez, panelde hatırlatma (K276) | ⏳ 27 Kasım 2026 · ayrıntı takip tablosunda | backend/frontend `faz-22-release-prep` · docs `docs/2026-11-27-faz-22-release-prep` | [`faz-22/`](faz-22/README.md) | backend `docs/rehber/fazlar/FAZ-22.md` |
| 23 | v1.4 frontend: ana sayfa vitrin sahnesi (hero ile önizleme arasında, kaydırmaya bağlı telefon sahnesi) | 🔧 Yön A kodlandı (27 Kasım 2026, 23.1–23.4) · birleştirme bekliyor | frontend `faz-23-v1.4-frontend` (`faz-22-release-prep`'ten) · docs `docs/2026-11-27-faz-23-v1.3-frontend-plan` | [`faz-23/`](faz-23/README.md) | — |
| 24 | v2.0 altyapı: şablon metinleri koddan çıktı (anahtar + `tr.json`, çok dilli altyapı yalnızca `tr`), sözleşme `text-slots.json` + `verify:text-slots`, backend `locale` / `text_overrides` / `has_custom_texts`, özel metin Elit. K300–K305 | ✅ kod 28 Kasım 2026 · `composer check` 1385/1385, `npm run check` 0, 762 şablon çizimi taşımadan önceyle aynı · birleştirme bekliyor | backend/frontend `faz-24-v2.0-editor` (frontend `faz-23-v1.4-frontend`'ten, backend `faz-22-release-prep`'ten) · docs `claude/brave-edison-dbg3l1` | [`faz-24/`](faz-24/README.md) | backend `docs/rehber/fazlar/FAZ-24.md` |
| 25 | v2.0 editör: tıkla-düzenle, Metinler paneli, ➕ bölüm ekle / gizle, varsayılana dön (onaylı), geri al/yinele, kategori sorusu, paywall'da "metinleri sıfırla ve yayınla", asistan önerisi altyapısı, "bu davetiyeyi bildir". K306–K313, K315 | ✅ kod 28 Kasım 2026 · `composer check` 1398/1398, `npm run check` 0, e2e `text-editor` 3/3 (geliştirme sunucusu) · birleştirme bekliyor | backend/frontend `faz-25-v2.0-editor-ui` (`faz-24-v2.0-editor`'dan) | [`faz-25/`](faz-25/README.md) | backend `docs/rehber/fazlar/FAZ-25.md` |
| 26 | v2.0 kalan metinler: hero'larda ve şablona özel parçalarda koda gömülü metinler (`verify:text-slots` tavanı) | ✅ kod 28 Kasım 2026 · tavan 511 → **0** (26.1 hero'lar, 26.2 şablona özel parçalar, 26.3 kalanlar) · sözleşme 307 anahtar · `npm run check` 0, `composer check` 1398/1398 · birleştirme bekliyor | frontend/backend `faz-26-v2.0-texts` (`faz-25-v2.0-editor-ui`'dan) | [`faz-26/`](faz-26/README.md) | — |
| 27 | v2.1 altyapı (Faz 27–29: Önizleme ve Tasarım Stüdyosu): `iframe` cihaz tuvali, kullanıcı içeriğinde tıkla-düzenle (`InvField`), yayındaki davetiye için taslak katmanı. K318–K329 | ⏳ plan onaylandı (28 Kasım 2026) · önce 26.3 | frontend/backend `faz-27-v2.1-studio` (`faz-26-v2.0-texts`'ten) · docs `claude/cool-hamilton-q2dnft` | [`faz-27/`](faz-27/README.md) | backend `docs/rehber/fazlar/FAZ-27.md` |

## Klasörler

| Klasör | İçerik | Durum |
|---|---|---|
| [`faz-05/`](faz-05/) | `FAZ-5-DEVIR.md`, `OKUBENI-FAZ-5.md` (backend `claude/`'dan, 2026-11-22) | Tarihsel |
| [`faz-06/`](faz-06/) · [`faz-07/`](faz-07/) · [`faz-09/`](faz-09/) | `FAZ-6/7/9-DEVIR.md` (backend `claude/`'dan, 2026-11-22; Faz 8'in devri yok) | Tarihsel |
| [`faz-10/`](faz-10/) | `FAZ-10-PLANI.md`: 85 adım, K87–K106 (backend `claude/`'dan, 2026-11-22) | Tarihsel |
| [`faz-11/`](faz-11/) | `FAZ-11-COMMIT-KOMUTLARI.md` (backend + claude), `FAZ-11-FRONTEND-COMMIT-KOMUTLARI.md` | Tamamlandı (tarihsel) |
| [`faz-12/`](faz-12/) | `FAZ-12-RAPOR.md` (24 Ekim 2026) | Tamamlandı (tarihsel) |
| [`faz-13/`](faz-13/) | Commit komutları (backend, frontend) · `f13-ara/` ara kod çıktısı · `teshis.php` + `php-herdsiz.ini` (PHPStan teşhisi) | Tamamlandı (tarihsel) |
| [`faz-14/`](faz-14/) | Commit komutları (backend, frontend) · `f14/` adım adım kod çıktısı (14.1–14.14) | Tamamlandı (tarihsel) |
| [`faz-18/`](faz-18/) | Takip tablosu; bulgu başına commit komutları (altı bulgu) | Kod tamam · etiket bekliyor (`SEC-07`) · → `SEC-07` Faz 19.1'de ele alındı (20 Kasım; kapılar bekliyor) |
| [`faz-19/`](faz-19/) | Takip tablosu; bulgu başına commit komutları; `kayit/` (paralel hat kayıtları, 19.90'da birleşti) | Kod tamam (28/28) · `v1.2.0` bekliyor |
| [`faz-20/`](faz-20/) | Takip tablosu (`AUD-2026-11-26` düzeltmeleri, 20.4 karar sorusu) | Sürüyor |
| [`faz-21/`](faz-21/) | Takip tablosu ve çalışma notları (`README.md`, Ek A SEC-18 planı, Ek B SEC-17 arşiv listesi) · `FAZ-21-ARC-08-KOMUTLARI.md` (dal/worktree/etiket komutları) | Tamamlandı · birleştirme bekliyor |
| [`faz-22/`](faz-22/) | Takip tablosu (`README.md`) | Sürüyor |
| [`faz-23/`](faz-23/) | `FAZ-23-PLAN.md`: vitrin sahnesi planı, üç tasarım yönü, adımlar 23.0–23.9, uygulama kaydı (§0.2) | Yön A kodlandı |
| [`faz-24/`](faz-24/) | `FAZ-24-PLAN.md` (v2.0 metin editörü planı; Faz 24–26'nın ortak planı), takip tablosu (`README.md`) | Kod tamam · birleştirme bekliyor |
| [`faz-25/`](faz-25/) | Takip tablosu (`README.md`): editör | Kod tamam · birleştirme bekliyor |
| [`faz-26/`](faz-26/) | Takip tablosu (`README.md`): kalan gömülü metinler | Kod tamam · birleştirme bekliyor |
| [`faz-27/`](faz-27/) | `FAZ-27-PLAN.md` (v2.1 Önizleme ve Tasarım Stüdyosu; Faz 27–29'un ortak planı), takip tablosu (`README.md`) | Sürüyor |
| [`frontend-catch-up/`](frontend-catch-up/) | `FRONTEND-YAKALAMA-PLANI.md` (11 Eylül 2026) | Tamamlandı (tarihsel) |

Commit komutu dosyalarındaki `Claude outputs\f13-ara`, `Claude outputs\f14` yolları eski yerdir;
bugün `phases/faz-13/f13-ara/`, `phases/faz-14/f14/`.
