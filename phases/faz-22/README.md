# Faz 22 — Yayın öncesi son faz: eksikler ve düzenlemeler

> **Başlangıç:** 27 Kasım 2026 · **Dallar:** backend/frontend `faz-22-release-prep` (`faz-21-backlog` ucundan:
> backend `1191a95`, frontend `e28b599`), docs `docs/2026-11-27-faz-22-release-prep` (`docs/2026-11-27-faz-21-backlog` ucundan)
> **Ne bu:** İsmail'in tanımı (27 Kasım 2026): *"Faz 22 genel olarak eksiklerin ve düzenlemelerin yapılacağı, release'den
> önceki son faz."* Madde listesi açık; İsmail yeni madde verdikçe §1'e satır eklenir.
> **Kararlar:** [`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-22.md`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-22.md) · K276'dan başlar.
> **Backend kaydı:** `davetkart-backend-php-laravel/docs/rehber/fazlar/FAZ-22.md` · **Önceki:** [`faz-21/`](../faz-21/README.md)

## 1. Takip

**Bu tablo ilerlemenin tek kaydıdır.**

| Sıra | Konu | Depolar | K | Commit'ler | Durum |
|---|---|---|---|---|---|
| 22.1 | E-posta doğrulaması satın almayı ve yayını engellemez; panelde hatırlatma bandı | backend · frontend · docs | K276 | be 5d390e2 · fe 6c0ea84 | commit'lendi |

Durum değerleri: `bekliyor` · `commit'lendi` · `birleşti` (İsmail, `main`'e aldıktan sonra).

## 2. 22.1 — E-posta doğrulaması engel değil, hatırlatma

**İstek (İsmail, 27 Kasım 2026):** *"Doğrulama olmadan satın alma olmuyordu. Bu kural değişecek. Panelde e-posta doğrulaması
hatırlatması olsun ancak satın almaya engel olmasın. Uyarı: 'Hesap erişiminizi kaybetmemek için mail adresinizi doğrulayınız'."*

**Soru ve cevap (oturumda):** K191'in kapısı üç yerdeydi: checkout, yayın, ilk yayın indirimi. Checkout ve yayın birlikte
kalkar (yayın kalsaydı ödeyen kullanıcının otomatik yayını 403 alırdı). İlk yayın indirimi için İsmail **"doğrulama istemeye
devam"** seçti: satın almayı engellemez, doğrulanmamış hesap liste fiyatından öder; sahte adresle açılan hesapların indirimi
tekrar tekrar kullanması önlenir.

**Ne değişti:**

| Depo | Değişiklik |
|---|---|
| backend | `VerifiedEmailGuard` ve `EmailNotVerifiedException` silindi; `StartCheckoutAction` ve `PublishInvitationAction` kapıyı çağırmıyor. `ErrorCode::EmailNotVerified` ve `contracts/error-codes.json` satırı silindi (K270: fırlatılmayan kod katalogda kalmaz; 28 → 27). `FirstPublishEligibility` aynı. İki test ters çevrildi: `an_unverified_account_can_start_a_checkout_at_list_price`, `an_unverified_account_can_publish_a_paid_invitation` |
| frontend | Bant metni (tr/en): "Hesap erişiminizi kaybetmemek için e-posta adresinizi doğrulayın. Bağlantıyı {{email}} adresine gönderdik; doğrulanan hesaplarda ilk davetiye indirimi de geçerli olur." Doğrulama sayfası `doneBody`, fiyat sayfası indirim bandı ve SSS "doğrulanınca" diyor. `EMAIL_NOT_VERIFIED` sözleşme kopyasından ve tr/en `errors.json`'dan silindi |
| docs | K276; K191 ve K159 durum notları |

Bant yeri değişmedi: `AppLayout` (Header'ın altı), panel dahil oturum açık her sayfa; kapatılamaz.

Kapı sonuçları: backend `docs/rehber/fazlar/FAZ-22.md` §22.1 (`composer check` bu oturumda **koşmadı**, frontend `npm run check` çıkış 0).
