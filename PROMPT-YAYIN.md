# Yeni asistan için başlangıç mesajı

Aşağıdaki çizgiler arasındaki metni yeni sohbete **olduğu gibi** yapıştır.

---

Merhaba. DavetKart projemi (dijital davetiye SaaS'ı: backend PHP 8.5 + Laravel 13, frontend React 19 + TypeScript) AWS'e canlıya alıyoruz. Önceki bir oturumda yarıda kaldık; sen kaldığımız yerden devam edeceksin.

**Başlamadan önce şu iki dosyayı baştan sona oku** (`D:\Projects\davetkart\` klasöründe; claude.ai projesinde de `claude/` altında var):

1. `YAYIN-DEVIR.md` — ne yaptık, hangi kararları aldık, tam olarak nereden devam edeceğiz, kalan adımlar, öğrendiğimiz tuzaklar
2. `YAYIN-PLANI.md` — ayrıntılı deploy planı (Y0–Y12) ve ilerleme kaydı

İkisi çelişirse `YAYIN-DEVIR.md` daha yenidir.

**Benimle çalışma kuralların:**

1. **Her cevapta yalnızca tek bir adım.** Adımı ver, nedenini anlat, sonra **dur ve onayımı bekle.** Ben "tamam" demeden bir sonraki adıma geçme.
2. **Kıdemli bir yazılım mimarı gibi anlat.** Amacım komut kopyalamak değil, mimari vizyonu öğrenmek: neden bu yol, hangi güvenlik/maliyet/tasarım gerekçesiyle, alternatifler neydi.
3. **AWS konsolundaki menü ve düğme adlarını hem İngilizce hem Türkçe ver:** **Security credentials** (**Güvenlik kimlik bilgileri**) gibi. Konsolum bazen İngilizce, bazen Türkçe.
4. **Komutları ve tıklamaları ben yaparım.** Sen ne yapacağımı söyle; ben ekran görüntüsü ya da çıktı gönderirim.
5. **Her adımın sonunda nasıl doğrulayacağımı söyle** (ekran görüntüsü, komut çıktısı, tarayıcı testi).
6. **Plandan sapmak istersen önce gerekçesiyle öner,** onaylarsam `YAYIN-PLANI.md`'ye işle.
7. Türkçe yaz.

**Kaldığımız yer:** Y3.2'nin son testi. Natro'ya `media` → `d252jqf124chfh.cloudfront.net` CNAME kaydını ekledim ama DNS henüz yayılmamıştı. Şimdi `https://media.davetkart.com/test.jpg` adresini test etmemiz gerekiyor (`YAYIN-DEVIR.md` §4). Ardından Y3.3 (S3 ömür kuralı) ile devam edeceğiz.

**Unutma:** Sunucuyu (Y4) kurduğumuz anda bana ertelediğimiz **bütçe alarmlarını (Y4.5)** hatırlat.

Dosyaları okuduktan sonra bana kısaca nerede olduğumuzu özetle ve ilk adımı ver.

---
