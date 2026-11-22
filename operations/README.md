# `operations/`

Yayın, AWS, sunucu, DNS. Sırlar (`.env`, anahtarlar, parolalar) **buraya yazılmaz**.

| Dosya | Ne | Durum |
|---|---|---|
| [`deployment/YAYIN-PLANI.md`](deployment/YAYIN-PLANI.md) | AWS Lightsail yayın planı (Y0–Y12) ve ilerleme kaydı; 3 Ekim 2026'da başladı | Güncel (dosya 26 Ekim 2026'da değişti) |
| [`deployment/YAYIN-DEVIR.md`](deployment/YAYIN-DEVIR.md) | Yayın devir notu: yapılanlar, kararlar, kalan adımlar, tuzaklar (15 Ekim 2026) | Güncel. ⚠️ Kendisi "plan ile çelişirse bu dosya daha yeni" diyor, ama plan bundan sonra (26 Ekim) güncellendi |
| [`deployment/YAYIN-SIRASI.md`](deployment/YAYIN-SIRASI.md) | Yayın sırası ve sürüm etiketi çalıştırma kitabı: kontrol listesi, etiket komutları, önce backend sonra frontend, geri alma (Faz 18.1, K146–K150) | Güncel (16 Kasım 2026). ⚠️ Sunucu komutları henüz çalıştırılmadı |
| [`deployment/YEDEK-VE-GERI-YUKLEME.md`](deployment/YEDEK-VE-GERI-YUKLEME.md) | Yedek ve geri yükleme çalıştırma kitabı: yedek bucket'ı, yalnızca yazabilen kimlik (IAM politikası), sunucu kurulumu, doğrulama, aylık prova ve prova kaydı, gerçek kurtarma (Faz 18.2, K151–K157) | Güncel (16 Kasım 2026). ⚠️ AWS ve sunucu adımları henüz çalıştırılmadı; ilk üretim provası bekliyor |
| [`deployment/SURE-TAKVIMI.md`](deployment/SURE-TAKVIMI.md) | Bitiş tarihi olan her şeyin tek evi: alan adı, posta barındırma, AWS kredisi, SSL; ne durur, sahibi, yenileme yolu, 30/7 gün hatırlatıcıları, posta karar tablosu (Faz 19.8, `OPS-05`) | Güncel (22 Kasım 2026). ⚠️ Alan adı otomatik yenilemesi ve posta kararı İsmail'de |
| [`deployment/davetkart-sure-takvimi.ics`](deployment/davetkart-sure-takvimi.ics) | Takvimin hatırlatıcıları (7 etkinlik); Google/Outlook'a içe aktarılır | Güncel (22 Kasım 2026) |

Bu işin başlangıç prompt'u: [`../prompts/PROMPT-YAYIN.md`](../prompts/PROMPT-YAYIN.md).
