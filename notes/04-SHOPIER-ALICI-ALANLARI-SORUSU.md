# Shopier'e soru: dijital üründe alıcı kimlik/iletişim alanları

> **Bulgu:** `SEC-10` (denetim 2026-11-12) · **Karar:** K125 (⚠️ elle doğrulama bekliyor) · **Hazırlayan:** Faz 19.15 (D4, 2026-11-22)
> **25 Kasım 2026 (K262):** telefon artık gerçek (kartla ödemede sorulur, yalnızca siparişte saklanır); soru TCKN ve adres için hâlâ geçerli, 2. ve 3. maddede `buyer_phone` artık sorulmuyor.
> **Durum:** gönderilmeyi bekliyor. Cevap gelince tarihi, kanalı ve metni `prompts/faz-19-agent/19-15-SEC-10.md` §A-1'e yaz ve 19.15'i yeniden çalıştır.

## Gönderilecek metin (destek formu ya da e-posta)

> Konu: Dijital ürün ödemesinde buyer_id_nr, buyer_phone ve adres alanları
>
> Merhaba,
>
> DavetKart (davetkart.com) olarak Shopier API (`api_pay4.php`, form ile yönlendirme) üzerinden
> **dijital ürün** satıyoruz (`product_type=1`; fiziksel teslimat yok). Kullanıcılarımızdan yalnızca
> ad, soyad ve e-posta alıyoruz.
>
> Aşağıdaki alanlar için yazılı bilgi rica ediyoruz:
>
> 1. `buyer_id_nr` (T.C. kimlik no), `buyer_phone`, `billing_*` ve `shipping_*` (adres, şehir, ülke,
>    posta kodu) dijital üründe **zorunlu mu**?
> 2. Zorunlu değilse: bu alanları **hiç göndermemeli** miyiz, yoksa **boş** mu göndermeliyiz?
> 3. Zorunluysa: tüm alıcılar için aynı **sabit bir yer tutucu** değer (ör. TCKN yerine sabit bir değer,
>    adres yerine "Dijital ürün") göndermek sözleşme ve risk kurallarınıza uygun mu? Uygun değilse
>    hangi alanları alıcıdan gerçek olarak almamız gerekiyor?
> 4. Bu alanlar itiraz (chargeback) ve risk değerlendirmesinde nasıl kullanılıyor?
>
> Teşekkürler.

## Neden soruyoruz

Bugün `config/payment.php` → `buyer_placeholders` herkes için aynı değerleri gönderiyor (`buyer_id_nr=11111111110`,
`buyer_phone=05000000000`, sabit adres). Kişisel veri alanlarının ya gerçek olması ya da sağlayıcının **yazılı**
kabul ettiği bir muafiyete dayanması gerekir; "çalışıyor" ile "izin verilmiş" aynı şey değil (denetim öğretici notu).

## Cevaba göre ne olacak (19.15 prompt'u §3)

| Cevap | Kol | Özet |
|---|---|---|
| Zorunlu değil | D1 | Alanlar kaldırılır ya da boş gider (cevabın dediği gibi); K125 "çözüldü → K…" |
| Zorunlu, telefon yeter | D2 | Checkout'ta telefon (TR mobil biçimi), yalnızca siparişte saklanır; frontend ödeme sayfasına alan |
| Zorunlu, TCKN de | DUR | KVKK kapsamı değişir, aydınlatma metni (`SEC-11`) etkilenir; ayrı karar |
| Her kolda | D3 | Yer tutucular config'ten kalkar; üretimde yer tutucuyla form üretmek imkânsız olur (SEC-03 fail-closed deseni) |

İmza etkilenmez: `ShopierSignature::forPayment` yalnızca `random_nr`, `platform_order_id`, tutar ve para birimini kapsıyor.
