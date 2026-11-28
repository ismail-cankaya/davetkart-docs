# Faz 29 — v2.1 Önizleme ve paylaşım

Faz 27–29'un (v2.1) son fazı. Plan: [`../faz-27/FAZ-27-PLAN.md`](../faz-27/FAZ-27-PLAN.md).

| | |
|---|---|
| Durum | ✅ Kod tamam (28 Kasım 2026) · birleştirme bekliyor |
| Sürüm | v2.1 |
| Kod dalı | frontend `faz-29-v2.1-share` (`faz-28-v2.1-studio-ui`'dan) · backend `faz-29-v2.1-share` (`faz-27-v2.1-studio`'dan) |
| Kararlar | [`EK-FAZ-27`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-27.md): K318, K324, K327, K328 |

## Takip

| Sıra | Konu | Depo | K | Commit | Durum |
|---|---|---|---|---|---|
| 29.1 | Panel kartları: yayında Görüntüle (yeşil) + Paylaş, Önizleme + Düzenle; taslakta Önizleme + Düzenlemeye devam et; taslak rozeti. Hızlı önizleme `/dashboard/preview/:id`: solda temel bilgiler, sağda telefon. Paylaş penceresi (bağlantı, WhatsApp, QR) | fe | K318, K324, K327 | `5751705` | commit'lendi |
| 29.4 | "Telefonda aç": 24 saatlik imzalı önizleme bağlantısı + QR (stüdyo üst çubuğu, hızlı önizleme). Sayfa `/preview/:id` | fe · be | K328 | fe `17781a3` · be `6e0b86f` | commit'lendi |
| 29.5 | Backend faz kaydı `docs/rehber/fazlar/FAZ-27.md` | be | — | `cafee53` | commit'lendi |

29.2–29.3 (planda ayrı adımlar) 29.1 içinde yapıldı.

## Kapılar

| Adım | Sonuç |
|---|---|
| 29.1, 29.4 frontend | `npm run check` çıkış 0 · misafir paketi 799 976 / 800 000 bayt |
| 29.4 backend | `composer check` 1415/1415 (6 yeni: `InvitationPreviewLinkTest`) |
| Elle (yerel backend + Vite) | Hızlı düzenleme yalnızca değişen alanları gönderdi, misafir ucu güncellendi; QR çizildi; telefon bağlantısı taslak başlığı gösterdi, misafir değişmedi, bozuk imza reddedildi (404) |

Koşmadı: tam e2e takımı, gerçek telefonda QR okutma, sunucu adımları (`FRONTEND_URL`, migration).

## Risk

- ⚠️ **Misafir paketi bütçenin 24 bayt altında.** Misafir sayfasına ya da ana giriş parçasına eklenecek ilk şey
  `verify:bundle`'ı kırar. Öneri: bütçeyi gözden geçirmek ya da misafir dışı bir şeyi daha giriş parçasından ayırmak
  (İsmail'in kararı).
