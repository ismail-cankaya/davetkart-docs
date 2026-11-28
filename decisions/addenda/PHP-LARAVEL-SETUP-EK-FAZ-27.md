# `PHP-LARAVEL-SETUP.md` — Faz 27–29 Yaması (v2.1 Önizleme ve Tasarım Stüdyosu)

> **Tarih:** 28 Kasım 2026 · plan [`phases/faz-27/FAZ-27-PLAN.md`](../../phases/faz-27/FAZ-27-PLAN.md) · takip
> [`faz-27`](../../phases/faz-27/README.md)
> **Ne bu:** Faz 27, 28 ve 29'un kararları. `-EK-FAZ-24` ile aynı biçim.
> **Numara aralığı:** Faz 24–26'ya ayrılan K300–K329'un boş kalanı (K318–K329) Faz 27–29'a verildi; aralık doldu.
> Sıradan numaralama (K277…) değişmedi.

---

## A. Karar Kaydı'na eklenecek (§7)

| # | Karar | Gerekçe | Durum |
|---|---|---|---|
| **K318** | **İki düzenleme kapısı.** Panel kartında **Önizleme** (hızlı düzenleme: temel bilgiler + telefon önizlemesi, `/dashboard/preview/:id`, tam ekran katman) ve **Düzenle** (Tasarım Stüdyosu, `/studio/:id`, ayrı tam ekran sayfa) | Kullanıcı teknik ayrıntıya boğulmadan isim/tarih düzeltebilsin; ayrıntı isteyen editöre gitsin | geçerli · **İsmail'in kararı** (adres İngilizce) · Faz 27–29 |
| **K319** | **Stüdyo yerleşimi:** solda menü (Bilgiler · Bölümler · Metinler · Tema · Kontrol listesi), orta-sağda tuval, sağda gerektiğinde açılan ayrıntı paneli (1440 px altında tuvalin üstüne katman); telefonda tuval tam ekran + alt çubuk; site üst/alt çerçevesi yok. Önizleme'de form solda, telefon sağda | İsmail: *"sağ ile soldaki menüler yer değiştirsin"* | geçerli · **İsmail'in kararı** · Faz 28 |
| **K320** | **Tuval aynı uygulamada `iframe`:** şablon React portal ile iframe belgesine, gerçek cihaz genişliğinde (390 / 820 / 1280 px) çizilir ve `transform: scale()` ile alana sığar; ana belgenin stilleri kopyalanır. Misafir sayfası ve ana sayfa vitrini değişmez | 116 şablon dosyasındaki `sm:/md:/lg:` sınıfları tarayıcı penceresine bakıyor; kutu içinde çizim cihazı taklit etmiyor | geçerli · plan onayı · Faz 27.1 |
| **K321** | **Kullanıcı içeriğinde tıkla-düzenle (`InvField`):** isimler, başlık, alt başlık, mekân, tarih önizlemede tıklanır; değer `useInvitationStore`'a yazılır (paket yok, `text_overrides`'a değil). Köprü yokken (misafir) DOM aynı | İsmail: *"başlıklar dahil tüm metinler düzeltilsin"*; K305 (kendi içerik paket istemez) | geçerli · **İsmail'in kararı** · Faz 27.2 |
| **K322** | **Tek editör:** sihirbaz (kategori → tema → bilgiler → üretim) sonunda stüdyoya geçer; `EditorWorkspace` kalkar; `/create/:id` stüdyoya yönlendirir; giriş yapmamış kullanıcı `/studio` (yerel taslak) | İki editör bakım yükü ve tutarsızlık | geçerli · plan onayı · Faz 28.6 |
| **K323** | **Taslak katmanı (yayındaki davetiye):** stüdyo değişiklikleri `invitations.pending_changes` (`jsonb`, yalnızca canlıdan farklı alanlar) kolonuna yazılır; `PUT /invitations/{id}/pending` (paket kontrolü yok), `POST …/pending/publish` (`UpdateInvitationAction` üzerinden: kilit, paket farkı, 402), `DELETE …/pending`. Misafir yanıtı ve önbellek değişmez. Galeri yükleme/silme anında, yalnızca galeri sırası taslakta | Tam editörle yarım değişiklik misafire gitmesin. K306'nın "yayındaki değişiklik anında yansır" kısmını ve K317'nin "taslak katmanı" maddesini geçersiz kılar | geçerli · **İsmail'in kararı** (ek fikir 1) · Faz 27.3 |
| **K324** | **Hızlı düzenleme yayına anında:** Önizleme'de açık "Kaydet"; yayındaki davetiyede "Kaydet ve yayınla" doğrudan canlıya yazar ve yazılan alanlar `pending_changes`'tan düşer (alan bazında son kaydeden kazanır) | Temel bilgi düzeltmesi beklemesin; taslakla çakışma kuralı tek ve açık | geçerli · plan onayı · Faz 27.3, 29.1 |
| **K325** | **Misafir gözüyle, yayına hazır kontrol listesi, taşma uyarısı:** çerçevesiz tam ekran gösterim (zarf baştan); eksik bilgi maddeleri (örnek isim, tarih yok/geçmiş, mekân boş, LCV son günü yok) "Hazır n/m"; kutusundan taşan metin ⚠️ | Kullanıcı yayından önce sorunları görsün | geçerli · **İsmail'in kararı** (ek fikir 2–4) · Faz 28.5 |
| **K326** | **Panel kartı:** yayında `Görüntüle` (yeşil) · `Paylaş` · `Önizleme` · `Düzenle`; taslakta `Önizleme` · `Düzenle`; bekleyen taslakta rozet | İsmail'in isteği | geçerli · **İsmail'in kararı** · Faz 29.2 |
| **K327** | **Paylaş:** telefonda `navigator.share`; masaüstünde menü (bağlantıyı kopyala, WhatsApp, QR kod); QR kütüphanesi tembel parça | "Kopyala" yerine paylaşım | geçerli · **İsmail'in kararı** (en son adım) · Faz 29.3 |
| **K328** | **Telefonda aç:** `POST /invitations/{id}/preview-link` 24 saatlik imzalı bağlantı (`URL::temporarySignedRoute`); `GET /api/public/invitations/{id}/preview` canlı + taslak birleşik, önbelleksiz, `X-Robots-Tag: noindex`, taslak davetiyede de çalışır, LCV/yükleme göndermez; stüdyo ve Önizleme'de QR | Gerçek görünüm kullanıcının kendi telefonunda | geçerli · **İsmail'in kararı** (ek fikir 5, *"en sona kalabilir"*) · Faz 29.4 |
| **K329** | **Sürüm ve bölünme:** Faz 27–29 = **v2.1** (Faz 27 altyapı, 28 stüdyo, 29 önizleme ve paylaşım); dallar frontend/backend `faz-27-v2.1-studio` (`faz-26-v2.0-texts`'ten) → `faz-28-…` → `faz-29-…`; `main`'e dokunulmaz. K317'nin diğer maddeleri (diller, çeviri, ton, LCV özel soru, bölüm sırası, RTL) sonraki sürüme | İsmail: *"Bu işlemimiz v 2.1 olacak"*, *"3 faza kadar"* | geçerli · **İsmail'in kararı** |

**Eski kararlarla ilişki:**

- K306 → "yayındaki davetiyede değişiklik anında yansır" kısmı **geçersiz kılındı → K323**; tıkla-düzenle ve "Kaydet" ile
  yazma geçerli.
- K317 → "taslak katmanı" maddesi **geçersiz kılındı → K323**; sürüm etiketi K329 ile (v2.1 artık Faz 27–29).
- K305 (kendi içerik paket istemez) → K321 ve K324 aynı ilkeyle.
- K237 / K315 (paket bütçesi 720 / 800 kB) → korunur.

## B. Uygulama kaydı

Ayrıntı ve commit'ler: faz klasörleri ve backend `docs/rehber/fazlar/FAZ-27.md` (yazıldıkça).
