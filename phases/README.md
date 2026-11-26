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
| [`frontend-catch-up/`](frontend-catch-up/) | `FRONTEND-YAKALAMA-PLANI.md` (11 Eylül 2026) | Tamamlandı (tarihsel) |

Commit komutu dosyalarındaki `Claude outputs\f13-ara`, `Claude outputs\f14` yolları eski yerdir;
bugün `phases/faz-13/f13-ara/`, `phases/faz-14/f14/`.
