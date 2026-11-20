# PROMPT — FAZ 19.23: `FE-04` Davetiye bağlantısının paylaşım önizlemesi yok (Open Graph)

> **Hazırlanma:** 20 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §5.1 · tam metin [`findings/04-frontend-e2e.md`](../audits/2026-11-12-full-system-audit/findings/04-frontend-e2e.md)) · **Sıra:** 23/28 · **Efor:** M
> **Önkoşul:** 19.22 (`TST-04`) düzeltme dalı `faz-19-audit-fixes`'e birleşmiş olmalı (§2 denetler).
> **Dokunulan depolar:** frontend · backend (Blade + `deploy/nginx`) · docs
> **Kullanım:** önce §A'yı sen doldur/yap; sonra `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır.

## §A — Senin kararın (prompt'u yapıştırmadan önce doldur)

| # | Soru | Boş bırakırsan ajanın uygulayacağı varsayılan | Cevabın |
|---|---|---|---|
| 1 | Hangi kol? | **Sağlam:** bilinen önizleme botları (WhatsApp, Telegram, facebookexternalhit, Twitterbot, Slackbot, LinkedInBot, Discordbot …) için Nginx `/invite/{id}`'yi Laravel'e yönlendirir; Laravel OG etiketli küçük bir Blade sayfası döner. Site geneli OG etiketleri de `index.html`'e | |
| 2 | Önizleme görseli? | Davetiyenin kapak görseli (yoksa şablonun kapağı, o da yoksa site geneli görsel) | |
| 3 | Elit (logosuz) davetiyede `og:site_name`? | Boş | |

**Boş satır için ajan varsayılanı uygular ve bunu K kaydında "varsayılan (İsmail cevaplamadı)" diye işaretler.**

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 19: denetimin orta öncelikli bulguları** üzerinde çalışıyoruz. `AUD-2026-11-12` 29 orta (🟡) bulgu çıkardı; `TST-01` Faz 18'de kapandı, kalan 28'i Faz 19'da her biri ayrı bir dalda ve ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `FE-04`** bulgusunu kapatır: *Davetiye bağlantısının paylaşım önizlemesi yok (Open Graph)*. Bu, 28 bulgunun 23. sırası. Yukarıdaki §A tablosu benim kararlarım.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (19.23.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `rm`, `mv`, `restore`, `checkout -- <dosya>`. İzinli: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `FE-04` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz. Faz 19'da sırası gelecek bulgular için bkz. `davetkart-docs\phases\faz-19\README.md`.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler; en sonda tam `composer check` **ve** `composer audit`. Frontend'e dokunduysan en sonda `npm ci` + `npm run check`. Önceki bulguların eklediği denetimler (ör. `verify:plans`, varsa E2E) yeşil kalmalı.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kendi kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut/tarayıcı). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi, `contracts/*.json` + `--check`). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend sözleşme kopyası ve tr/en çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `19.23.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula, K kaydına "plandan sapma" diye yaz ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md` (sıradaki boş K numarası başlıkta)
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\findings\04-frontend-e2e.md` içindeki **`FE-04`** tam metni · ilgili bulgular: K102 (logosuz yayın, Elit) · `SEC-04` (Nginx snippet'leri, K173) · `SEC-12` (fontlar) · kanıt: `index.html` (12 satır; OG etiketi yok) · gerçek botla koşmadı
4. Faz 18'in kaydı: backend `docs\rehber\fazlar\FAZ-18.md` (özellikle "gördüm, dokunmadım" tabloları ve kapanış özeti; bu bulguya değinen satırlar) · `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`
5. `davetkart-docs\phases\faz-19\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-19.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Frontend: `index.html` · misafir sayfası rotası (`/invite/:id`) · şablon kapak görselleri (`data.ts`) · site geneli marka görseli (`public/`).
2. Backend: `GET /api/public/invitations/{id}` (yayın durumu, adlar, tarih, kapak) ve Resource'u · K102 (logosuz yayın) · `deploy/nginx/davetkart.conf` + snippet'ler (K173: `location` bazında `include`) · `resources/views` (Blade kullanılıyor mu) · misafir okuma cache'i/ETag (K7).
3. Bot `User-Agent` listesi için birincil kaynaklar (her platformun belgesi); kılavuzda kaynak bağlantıları.

**K numarası:** yeni karar = `DECISION-INDEX.md`'deki "Sıradaki boş numara". Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (denetim 12 Kasım'daydı; Faz 18 bazı satırları değiştirdi, rapordaki satırlar hâlâ geçerli mi), §A'da hangi satırlar dolu, §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
git switch -c fix/<YYYY-MM-DD>-fe-04-share-preview

cd D:\Projects\davetkart\davetkart-frontent
git fetch origin
git status --short                                   # yalnızca '?? .claude/' olabilir; başka satır varsa DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
git branch --merged faz-19-audit-fixes | Select-String "tst-04-e2e"   # boşsa DUR: TST-04 birleşmemiş
git switch -c fix/<YYYY-MM-DD>-fe-04-share-preview

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-20-faz-19-audit-fixes                             # yoksa DUR
```

## 3. Bulgu (özet; tam metin bulgu dosyasında)

Tek sayfa uygulaması her adres için aynı `index.html`'i dönüyor ve içinde OG etiketi yok. WhatsApp'ın önizleme botu JavaScript çalıştırmadığı için davetiye bağlantısı sohbette çıplak bir bağlantı olarak görünüyor; çiftin adı ve kapak görseli yok. Ürünün dağıtım kanalı mesajlaşma uygulamaları.

**Dersin özü:** SPA içeriğini tarayıcıda üretir; bağlantı önizleme botları tarayıcı değildir. "Sunucu ilk yanıtta ne dönüyor" sorusu SEO'dan önce **paylaşılabilirlik** sorusudur. Bot için ayrı yanıt üretirken en büyük risk sızıntıdır: yayınlanmamış davetiyenin adları asla dönmemeli.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | Site geneli OG + `description` + `twitter:card` etiketleri `index.html`'de. |
| D2 | §A-1 sağlam kol: `GET /invite/{id}` (bot) → Laravel önizleme denetleyicisi → Blade. **Yalnızca yayınlanmış** davetiye için ad/tarih/görsel; değilse genel önizleme (adlar sızmaz). Bütün değerler HTML-kaçışlı (XSS: davetiye adları kullanıcı girdisi). `og:url` ve görsel adresi `config('app.url')`/medya adresinden (SEC-07 dersi). |
| D3 | Nginx: bot eşlemesi `map $http_user_agent $is_preview_bot` ile; yalnızca `/invite/` konumunda; botsa Laravel'e (`fastcgi`), değilse mevcut SPA. Güvenlik başlıkları snippet'i bu konuma da `include` (K173). Kullanıcı ajanı sahtelenebilir: bu yüzden D2'deki "yalnızca yayınlanmış" kuralı tek savunmadır, Nginx eşlemesi değil. |
| D4 | Önbellek: Blade yanıtı kısa süreli cache'lenir; davetiye güncellenince geçersizleşir (misafir okuma cache'inin anahtarıyla aynı yaşam döngüsü). |

## 5. Adımlar ve dosya sahipliği

### Backend (`fix/<YYYY-MM-DD>-fe-04-share-preview`)
| Adım | İş |
|---|---|
| 19.23.1 | D2 + D4: denetleyici + Blade + rota + kılavuzlar + testler. |
| 19.23.2 | D3: Nginx `map` + `/invite/` konumu + duman testi + kılavuzlar. |
| 19.23.3 | `FAZ-19.md` `## 19.23 — FE-04`. |

### Frontend (`fix/<YYYY-MM-DD>-fe-04-share-preview`) — 🔴 `git add -A` yasak
| Adım | İş |
|---|---|
| 19.23.4 | D1: `index.html` + (gerekirse) görsel; `npm run check`. |

### Docs
| Adım | İş |
|---|---|
| 19.23.5 | §7'deki ortak kayıtlar; `YAYIN-SIRASI.md`'ye dağıtım sonrası önizleme kontrolü (`curl -A "WhatsApp/2" …`). |

## 6. Testler ve kalite kapısı

- `a_bot_gets_the_couples_names_in_og_title` · `an_unpublished_invitation_gets_the_generic_preview`. **Mutant:** yayın durumu koşulunu kaldır → kırmızı (taslak adları sızar).
- `preview_values_are_html_escaped` (adda `<script>`).
- `an_elite_invitation_has_no_site_name` (K102).
- Yerel Nginx (Herd) varsa: `curl -A "WhatsApp/2.23" http://…/invite/<id>` → Blade; normal ajan → SPA. Koşamadıysan "koşmadı".
- `composer check`, `npm run check`.

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-19.md`: yoksa oluştur (başlık: "Faz 19 — denetimin orta öncelikli bulguları (`AUD-2026-11-12`)", 28 bulgunun tablosu). `## 19.23 — FE-04` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar (frontend dahil), eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım işler. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).
- Docs deposunda `phases/faz-19/FAZ-19-*-KAYIT.md` dosyaları varsa (backend'e dokunmayan önceki bulguların bölümleri) ve `FAZ-19.md`'de karşılıkları yoksa, onları sıra numarasına göre `FAZ-19.md`'ye taşı; docs'taki dosyayı silme, başına "Taşındı → backend `FAZ-19.md` §19.x" notu ekle.

**Docs deposu (`docs/2026-11-20-faz-19-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı/daralttığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". Değişen eski kararların durum sütununa "→ K…" notu (eski satırı silme).
- `phases/faz-19/README.md`: `FE-04` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-19/FAZ-19-FE-04-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**. Geçmiş faz kayıtlarının metnini yeniden yazma; yalnızca tarihli bir **durum notu** eklemek ("→ Faz 19.x") ve taşıma yüzünden kırılan bağlantıyı düzeltmek serbest.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor). Bulgu zaten kapanmışsa kanıtını göster, kod yazma, yalnızca kayıt adımlarını yap.
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi, hukuki metin ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.


**Kapsam dışı (dokunma, raporda an):** SEO (site haritası, sunucu tarafı render), `og:image` için dinamik görsel üretimi.

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` (silinecek dosya varsa `git rm <yol>`, taşınacak dosya varsa `git mv <eski> <yeni>`) → `git commit -m "19.23.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Bloğun başında "Başlamadan" kısmı: her depoda `git status --short --untracked-files=all` ve **beklenen satırların tam listesi** (Faz 18'deki gibi), ki fazladan dosya varsa commit'ten önce göreyim.
- Sıra: backend blokları → frontend blokları → docs bloğu → birleştirme.
- **Birleştirme bloğu:** dokunduğun her kod deposu için ayrı ayrı: `git switch faz-19-audit-fixes` → `git merge --no-ff fix/<YYYY-MM-DD>-fe-04-share-preview -m "Merge FE-04 fix into faz-19-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-19\FAZ-19-FE-04-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (19.23.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle; §A'nın hangi satırı cevaplıydı, hangisinde varsayılan uygulandı.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili test/denetimin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, Shopier, deneme) varsa numaralı liste.
