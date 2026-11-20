# PROMPT — FAZ 19.25: `FE-53` Kısıtlı mobil koşulda LCP 3,9–5,7 sn; giriş ve fiyat sayfalarında CLS 0,33–0,63

> **Hazırlanma:** 20 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §5.1 · tam metin [`findings/04-frontend-e2e.md`](../audits/2026-11-12-full-system-audit/findings/04-frontend-e2e.md)) · **Sıra:** 25/28 · **Efor:** M
> **Önkoşul:** 19.24 (`FE-10`) düzeltme dalı `faz-19-audit-fixes`'e birleşmiş olmalı (§2 denetler).
> **Dokunulan depolar:** frontend · docs
> **Kullanım:** önce §A'yı sen doldur/yap; sonra `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır.

## §A — Senin kararın (prompt'u yapıştırmadan önce doldur)

| # | Soru | Boş bırakırsan ajanın uygulayacağı varsayılan | Cevabın |
|---|---|---|---|
| 1 | Bütçeler (kısıtlı mobil: CPU 4×, 1,6 Mbps, 150 ms)? | Misafir sayfası LCP < 3 sn · dört sayfada CLS < 0,1 | |
| 2 | Bütçe `npm run check`'e mi girsin, ayrı `npm run perf` mi? | Ayrı `npm run perf` (yavaş ve ortama duyarlı); sonuçlar faz kaydına | |

**Boş satır için ajan varsayılanı uygular ve bunu K kaydında "varsayılan (İsmail cevaplamadı)" diye işaretler.**

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 19: denetimin orta öncelikli bulguları** üzerinde çalışıyoruz. `AUD-2026-11-12` 29 orta (🟡) bulgu çıkardı; `TST-01` Faz 18'de kapandı, kalan 28'i Faz 19'da her biri ayrı bir dalda ve ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `FE-53`** bulgusunu kapatır: *Kısıtlı mobil koşulda LCP 3,9–5,7 sn; giriş ve fiyat sayfalarında CLS 0,33–0,63*. Bu, 28 bulgunun 25. sırası. Yukarıdaki §A tablosu benim kararlarım.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (19.25.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `rm`, `mv`, `restore`, `checkout -- <dosya>`. İzinli: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `FE-53` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz. Faz 19'da sırası gelecek bulgular için bkz. `davetkart-docs\phases\faz-19\README.md`.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler; en sonda tam `composer check` **ve** `composer audit`. Frontend'e dokunduysan en sonda `npm ci` + `npm run check`. Önceki bulguların eklediği denetimler (ör. `verify:plans`, varsa E2E) yeşil kalmalı.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kendi kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut/tarayıcı). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi, `contracts/*.json` + `--check`). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend sözleşme kopyası ve tr/en çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `19.25.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula, K kaydına "plandan sapma" diye yaz ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md` (sıradaki boş K numarası başlıkta)
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\findings\04-frontend-e2e.md` içindeki **`FE-53`** tam metni · ilgili bulgular: `FE-10` (19.24: paket bölündü), `SEC-12` (19.17: fontlar kendi alan adında), `TST-04` (19.22: Playwright kurulu) · kanıt: `evidence\commands\E2E-perf.json` · `evidence\scripts\e2e\perf-measure.mjs`
4. Faz 18'in kaydı: backend `docs\rehber\fazlar\FAZ-18.md` (özellikle "gördüm, dokunmadım" tabloları ve kapanış özeti; bu bulguya değinen satırlar) · `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`
5. `davetkart-docs\phases\faz-19\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-19.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Denetim: `evidence\scripts\e2e\perf-measure.mjs` (CDP ile ölçüm; taşınabilir) ve `E2E-perf.json` (başlangıç değerleri).
2. Frontend: 19.24 ve 19.17 sonrası durum · `index.html` · `src/index.css` ve 19.17'nin `@font-face` dosyası · fiyat sayfası kartları (API yanıtından sonra çiziliyor) · giriş sayfası kartı · ana sayfa videosu (`hero-bg.mp4`) · 19.22'nin Playwright kurulumu.

**K numarası:** yeni karar = `DECISION-INDEX.md`'deki "Sıradaki boş numara". Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (denetim 12 Kasım'daydı; Faz 18 bazı satırları değiştirdi, rapordaki satırlar hâlâ geçerli mi), §A'da hangi satırlar dolu, §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
# backend: bu bulguda değişmesi beklenmiyor; dal açma. Değiştirmen gerekirse burada aynı adla dal aç ve raporda söyle.

cd D:\Projects\davetkart\davetkart-frontent
git fetch origin
git status --short                                   # yalnızca '?? .claude/' olabilir; başka satır varsa DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
git branch --merged faz-19-audit-fixes | Select-String "fe-10-bundle-split"   # boşsa DUR: FE-10 birleşmemiş
git switch -c fix/<YYYY-MM-DD>-fe-53-mobile-vitals

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-20-faz-19-audit-fixes                             # yoksa DUR
```

## 3. Bulgu (özet; tam metin bulgu dosyasında)

Kısıtlı mobil koşulda LCP ana sayfada 5,7, misafir sayfasında 4,5 sn; CLS giriş sayfasında 0,33, fiyatlarda 0,63. Kök nedenler: ana paket (19.24'te bölündü), Google Fonts `@import` (19.17'de kalktı) ve fiyat kartlarının API yanıtından sonra yer ayrılmadan çizilmesi.

**Dersin özü:** kısıtsız ölçümde her şey iyi görünür; fark **yavaş koşulda** ortaya çıkar, çünkü darboğaz ağ ve ayrıştırma süresidir. CLS'in yalnızca yavaş koşulda çıkması tipik bir işarettir: geç gelen font ve geç gelen veri, önceden yer ayrılmamış alanı iter. Önce ölç, sonra düzelt, sonra bütçeyle kilitle.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | Önce **yeniden ölç** (19.17 ve 19.24 sonrası); kalan sorunları yalnızca ölçüme dayanarak sırala. |
| D2 | Fontlar: kritik bir-iki dosya için `<link rel="preload" as="font" crossorigin>`; yedek font `size-adjust`/`ascent-override` ile eşlenir (font değişiminde kayma olmasın). |
| D3 | Fiyat ve giriş kartlarına sabit en küçük yükseklik ya da iskelet (veri gelmeden yer ayrılır). |
| D4 | Ana sayfa videosu `preload="none"` + `poster`; LCP öğesi görselse `fetchpriority="high"`. |
| D5 | `npm run perf`: ölçüm betiği (`perf-measure.mjs`'ten uyarlanmış, Playwright ile) + §A-1 bütçeleri; üç koşunun ortancası. |

## 5. Adımlar ve dosya sahipliği

### Frontend (`fix/<YYYY-MM-DD>-fe-53-mobile-vitals`) — 🔴 `git add -A` yasak
| Adım | İş |
|---|---|
| 19.25.1 | D5: ölçüm betiği + `package.json` + kılavuz (önce bu: başlangıç ölçümü bununla). |
| 19.25.2 | D2: font ön yükleme ve yedek font eşleme. |
| 19.25.3 | D3: kart iskeletleri. |
| 19.25.4 | D4: video ve LCP öğesi; `npm run check` + `npm run e2e` + `npm run perf`. |

### Docs
| Adım | İş |
|---|---|
| 19.25.5 | §7'deki ortak kayıtlar (faz bölümü `phases/faz-19/FAZ-19-FE-53-KAYIT.md`): dört sayfa × (LCP, CLS, TBT, bayt) önce/sonra tablosu. |

## 6. Testler ve kalite kapısı

- `npm run perf` üç koşu ortancası, dört sayfa; bütçe içinde mi (dışındaysa dürüstçe yaz, bütçeyi gevşetme — sor).
- **Mutant:** fiyat kartı iskeletini kaldır → fiyat sayfası CLS bütçeyi aşar.
- `npm run check`, `npm run e2e`.

## 7. Kayıt (dokümantasyon)

**Faz kaydı:** bu bulgu backend'e dokunmuyor. `## 19.25 — FE-53` bölümünü backend `FAZ-19.md`'ye **yazma** (backend dalı açılmadı); aynı içeriği docs deposundaki `phases/faz-19/FAZ-19-FE-53-KAYIT.md` dosyasına yaz. Bir sonraki backend'e dokunan bulgu bu bölümü `FAZ-19.md`'ye taşır (raporunda hatırlat).
- Frontend'de değişen her dosyanın `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).

**Docs deposu (`docs/2026-11-20-faz-19-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı/daralttığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". Değişen eski kararların durum sütununa "→ K…" notu (eski satırı silme).
- `phases/faz-19/README.md`: `FE-53` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-19/FAZ-19-FE-53-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**. Geçmiş faz kayıtlarının metnini yeniden yazma; yalnızca tarihli bir **durum notu** eklemek ("→ Faz 19.x") ve taşıma yüzünden kırılan bağlantıyı düzeltmek serbest.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor). Bulgu zaten kapanmışsa kanıtını göster, kod yazma, yalnızca kayıt adımlarını yap.
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi, hukuki metin ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.
- Bütçeye ulaşmak için CSS bölme ya da sunucu tarafı render gibi kapsamı büyüten bir değişiklik gerekiyor: ölçümü göster, sor.

**Kapsam dışı (dokunma, raporda an):** CSS bölme, görüntü CDN'i, gerçek kullanıcı ölçümü (RUM).

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` (silinecek dosya varsa `git rm <yol>`, taşınacak dosya varsa `git mv <eski> <yeni>`) → `git commit -m "19.25.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Bloğun başında "Başlamadan" kısmı: her depoda `git status --short --untracked-files=all` ve **beklenen satırların tam listesi** (Faz 18'deki gibi), ki fazladan dosya varsa commit'ten önce göreyim.
- Sıra: backend blokları → frontend blokları → docs bloğu → birleştirme.
- **Birleştirme bloğu:** dokunduğun her kod deposu için ayrı ayrı: `git switch faz-19-audit-fixes` → `git merge --no-ff fix/<YYYY-MM-DD>-fe-53-mobile-vitals -m "Merge FE-53 fix into faz-19-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-19\FAZ-19-FE-53-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (19.25.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle; §A'nın hangi satırı cevaplıydı, hangisinde varsayılan uygulandı.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili test/denetimin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, Shopier, deneme) varsa numaralı liste.
