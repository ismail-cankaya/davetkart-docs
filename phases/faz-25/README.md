# Faz 25 — v2.0 editör: tıkla-düzenle, bölümler, geri al

Tasarım stüdyosunda önizlemedeki metne tıklayıp değiştirme, "Metinler" paneli, ➕ ile bölüm ekleme ve gizleme, onaylı
varsayılana dönüş, geri al/yinele, kategori değişiminde soru, paywall'da "metinleri sıfırla ve yayınla", asistan önerisi
altyapısı ve misafir sayfasında "bu davetiyeyi bildir". Plan: [`../faz-24/FAZ-24-PLAN.md`](../faz-24/FAZ-24-PLAN.md).

| | |
|---|---|
| Durum | ✅ Kod tamam (28 Kasım 2026) · birleştirme İsmail'in |
| Kod dalı | frontend/backend `faz-25-v2.0-editor-ui` (`faz-24-v2.0-editor`'dan) |
| Kararlar | [`EK-FAZ-24`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-24.md): K306–K313, K315 |
| Backend kaydı | `davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-25.md` |

## Takip

| Sıra | Konu | Depo | K | Commit | Durum |
|---|---|---|---|---|---|
| 25.1 (be) | Metin önerisi ucu (`/invitations/{id}/text-suggestions`, sunucu istemi, paylaşılan kota `ChargeAssistantQuotaAction`) ve misafir bildirimi (`/public/invitations/{id}/report`, `invitation_reports`, kuyruk postası); 13 test | be | K310, K313 | `1b532f9` | commit'lendi |
| 25.1 (fe) | Editör: `useEditorStore`, yerinde düzenleyici, Metinler paneli, `EditableSection` + çip, ➕ menüsü ve Bölümler listesi, ayar çekmecesi (`ModuleFields`), kategori sorusu, paywall ikinci yolu (`usePublishFlow`), bildir bağlantısı ve penceresi; tembel metin paketi ve editör çevirileri; e2e `text-editor` | fe | K306–K309, K311–K313, K315 | `ce5a59b` | commit'lendi |

## Kapılar (bu oturum)

- Backend `composer check`: **1398/1398**.
- Frontend `npm run check`: **çıkış 0**; paket bütçesi: ilk yükleme **714,2 kB** (≤ 720), misafir **799,2 kB** (≤ 800).
- e2e `e2e/text-editor.spec.ts` (proje `editor`): **3/3**, geliştirme sunucusuna karşı geçici yapılandırmayla
  (backend gerekmez). Tüm e2e paketi **koşmadı** (backend + PowerShell ister).
- Anlık görüntü: 762 çizim taşımadan önceyle **aynı** (misafirde editör çerçevesi yok).

## Bilinen sınırlar

- Asistan istemi ilk sürüm (K310): ton, uzunluk ayarı, çok dil sonraki faz.
- Hero ve şablona özel parçalardaki metinler henüz anahtarsız: önizlemede tıklanmaz, panelde yok → [Faz 26](../faz-26/README.md).
- Yayındaki davetiyede "Kaydet" misafire anında yansır (taslak katmanı v2.1, K317).
