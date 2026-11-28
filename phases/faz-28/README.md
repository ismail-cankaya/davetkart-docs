# Faz 28 — v2.1 Tasarım Stüdyosu arayüzü

Faz 27–29'un (v2.1) ikinci fazı. Plan: [`../faz-27/FAZ-27-PLAN.md`](../faz-27/FAZ-27-PLAN.md) (ortak plan). Altyapı
[Faz 27](../faz-27/README.md), önizleme ve paylaşım [Faz 29](../faz-29/README.md).

| | |
|---|---|
| Durum | ✅ Kod tamam (28 Kasım 2026) · birleştirme bekliyor |
| Sürüm | v2.1 |
| Kod dalı | frontend `faz-28-v2.1-studio-ui` (`faz-27-v2.1-studio`'dan). Backend değişmedi |
| Kararlar | [`EK-FAZ-27`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-27.md): K319, K320, K322, K325, K326 |

## Takip

| Sıra | Konu | Depo | K | Commit | Durum |
|---|---|---|---|---|---|
| 28.0 | Seçici, öğenin kendi metin düğümlerini de eşler (ayraçlı hero'lar). Tarama: 103 tasarım (307'nin 1/3'ü), isim 103/103, mekân 103/103, başlık çizildiği 91/91 | fe | K321 | `8583ef1` | commit'lendi |
| 28.1 | Stüdyo: solda menü (Bilgiler, Bölümler, Tema, Hazırlık), ortada cihaz tuvali (telefon / tablet / bilgisayar, tam ekranda düzenle), sağda ayrıntı paneli (≥1440 px yanaşık), misafir gözüyle, hazırlık listesi, taşma uyarısı | fe | K319, K322, K325, K326 | `8e8c96f` | commit'lendi |
| 28.6 | `/studio/:id?` rotası; sihirbaz ve panel "Düzenle" stüdyoya açar; eski `EditorWorkspace` ve `DesignerPanel` kalktı; misafir paketi bütçede | fe | K319 | `ff5ad8d` | commit'lendi |

28.2–28.5 (planda ayrı adımlar) 28.1 içinde tek commit'te yapıldı.

## Kapılar

| Adım | Sonuç |
|---|---|
| 28.6 | `npm run check` çıkış 0 · e2e `text-editor.spec.ts` 6/6 (geliştirme sunucusu, yerel backend) |

Koşmadı: `flows.ts`, `editor-flush`, `paywall-after-publish` güncellendi ama koşulmadı (backend + PowerShell ister).

## Not

- Misafir paketi (K237, 800 000 bayt) iki kez aşıldı ve geri alındı: ince rota kabukları (`StudioPage`, `CreatePage`,
  `DashboardPage` → tembel iç bileşen), isteğe bağlı rota parçaları (`/studio/:id?`, `/create/:id?`) ve
  `useEditorStore`'dan `resolve` içe aktarımının kalkması. Ayrıntı: frontend `docs/rehber/src/routes.md`.
