# PROMPT — FAZ 19.21: `FE-02` Hata sınırı yok: render hatası ve yüklenemeyen chunk ham hata ekranı veriyor

> **Hazırlanma:** 20 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §5.1 · tam metin [`findings/04-frontend-e2e.md`](../audits/2026-11-12-full-system-audit/findings/04-frontend-e2e.md)) · **Sıra:** 21/28 · **Efor:** S
> **Önkoşul:** 19.20 (`FE-01`) düzeltme dalı `faz-19-audit-fixes`'e birleşmiş olmalı (§2 denetler).
> **Dokunulan depolar:** frontend · docs
> **Kullanım:** `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır.

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 19: denetimin orta öncelikli bulguları** üzerinde çalışıyoruz. `AUD-2026-11-12` 29 orta (🟡) bulgu çıkardı; `TST-01` Faz 18'de kapandı, kalan 28'i Faz 19'da her biri ayrı bir dalda ve ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `FE-02`** bulgusunu kapatır: *Hata sınırı yok: render hatası ve yüklenemeyen chunk ham hata ekranı veriyor*. Bu, 28 bulgunun 21. sırası.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (19.21.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `rm`, `mv`, `restore`, `checkout -- <dosya>`. İzinli: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `FE-02` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz. Faz 19'da sırası gelecek bulgular için bkz. `davetkart-docs\phases\faz-19\README.md`.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler; en sonda tam `composer check` **ve** `composer audit`. Frontend'e dokunduysan en sonda `npm ci` + `npm run check`. Önceki bulguların eklediği denetimler (ör. `verify:plans`, varsa E2E) yeşil kalmalı.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kendi kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut/tarayıcı). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi, `contracts/*.json` + `--check`). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend sözleşme kopyası ve tr/en çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `19.21.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula, K kaydına "plandan sapma" diye yaz ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md` (sıradaki boş K numarası başlıkta)
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\findings\04-frontend-e2e.md` içindeki **`FE-02`** tam metni · ilgili bulgular: `deploy-frontend.sh` (eski `assets/` 14 gün), `OPS-03` (Sentry; frontend'de Sentry var mı) · kanıt: `evidence\commands\FE-d1-metrics.txt` §4
4. Faz 18'in kaydı: backend `docs\rehber\fazlar\FAZ-18.md` (özellikle "gördüm, dokunmadım" tabloları ve kapanış özeti; bu bulguya değinen satırlar) · `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`
5. `davetkart-docs\phases\faz-19\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-19.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Frontend: `src/App.tsx` (rota tanımları; `createBrowserRouter` mı `<Routes>` mı — `errorElement` buna göre) · `src/components/layout/AppLayout.tsx` (`Suspense`) · `ThreeStage.tsx` (tek mevcut sınır; desen) · editörün kaydedilmemiş durum yönetimi (`useInvitationAutoSave`) · `main.tsx` · frontend'de hata raporlama (Sentry) var mı.
2. Backend (salt okunur): `deploy/deploy-frontend.sh` (`KEEP_OLD_ASSETS_DAYS`).

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
git branch --merged faz-19-audit-fixes | Select-String "fe-01-language-scope"   # boşsa DUR: FE-01 birleşmemiş
git switch -c fix/<YYYY-MM-DD>-fe-02-error-boundary

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-20-faz-19-audit-fixes                             # yoksa DUR
```

## 3. Bulgu (özet; tam metin bulgu dosyasında)

Hiçbir rotada `errorElement` yok; bir bileşen hatası ya da yüklenemeyen bir tembel chunk (zayıf mobil bağlantı, çok eski sekme) React Router'ın İngilizce, markasız "Unexpected Application Error!" ekranını veriyor; editördeki kaydedilmemiş değişiklik kaybolabiliyor.

**Dersin özü:** `Suspense` yüklemenin **beklemesini** yönetir, **başarısızlığını** değil. Tembel yüklenen her modül bir ağ isteğidir ve her ağ isteği başarısız olabilir. Hata sınırı, hatanın yayılacağı alanı **senin seçtiğin** yerdir; seçmezsen çerçeve en dışta seçer.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | Kök rotada `RouteError` (marka, Türkçe/İngilizce metin `t()` ile, "Sayfayı yenile" ve "Ana sayfa"); ayrıca editör ve misafir sayfası gibi kritik alt ağaçlara kendi sınırları (hata yalnızca o bölgeyi düşürür). |
| D2 | `vite:preloadError` dinleyicisi: chunk hatasında **tek seferlik** `location.reload()`; sonsuz döngüye karşı `sessionStorage` bayrağı (zaman damgalı). Yenileme de başarısızsa `RouteError`. |
| D3 | Editörde sınır tetiklenirse mevcut otomatik kaydetmenin son durumu korunur (kaydedilmemişse kullanıcıya söylenir); hata ayrıntısı kullanıcıya gösterilmez, yalnızca geliştirme modunda. |
| D4 | Frontend'de hata raporlama varsa sınır onu çağırır; yoksa yeni bağımlılık eklenmez (`OPS-03` backend tarafındaydı). |

## 5. Adımlar ve dosya sahipliği

### Frontend (`fix/<YYYY-MM-DD>-fe-02-error-boundary`) — 🔴 `git add -A` yasak
| Adım | İş |
|---|---|
| 19.21.1 | D1 + D3: `RouteError` bileşeni + rota bağlama + çeviri + kılavuzlar. |
| 19.21.2 | D2: preload hata yöneticisi + kılavuz. |
| 19.21.3 | `verify:render` vakaları; `npm run check`. |

### Docs
| Adım | İş |
|---|---|
| 19.21.4 | §7'deki ortak kayıtlar (faz bölümü `phases/faz-19/FAZ-19-FE-02-KAYIT.md`). |

## 6. Testler ve kalite kapısı

- `verify:render`: "çocuğu hata fırlatan rota `RouteError` çiziyor". **Mutant:** `errorElement` satırını sil → kırmızı.
- Preload yöneticisi birim denetimi: ilk hata → yeniden yükleme çağrılır; bayrak varken ikinci hata → çağrılmaz. **Mutant:** bayrak kontrolünü kaldır → kırmızı.
- Tarayıcı: `vite preview` + bir chunk dosyasını geçici olarak yeniden adlandır → tek yenileme, sonra `RouteError` (ekran görüntüsü; koşamadıysan "koşmadı").
- `npm run check`.

## 7. Kayıt (dokümantasyon)

**Faz kaydı:** bu bulgu backend'e dokunmuyor. `## 19.21 — FE-02` bölümünü backend `FAZ-19.md`'ye **yazma** (backend dalı açılmadı); aynı içeriği docs deposundaki `phases/faz-19/FAZ-19-FE-02-KAYIT.md` dosyasına yaz. Bir sonraki backend'e dokunan bulgu bu bölümü `FAZ-19.md`'ye taşır (raporunda hatırlat).
- Frontend'de değişen her dosyanın `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).

**Docs deposu (`docs/2026-11-20-faz-19-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı/daralttığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". Değişen eski kararların durum sütununa "→ K…" notu (eski satırı silme).
- `phases/faz-19/README.md`: `FE-02` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-19/FAZ-19-FE-02-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**. Geçmiş faz kayıtlarının metnini yeniden yazma; yalnızca tarihli bir **durum notu** eklemek ("→ Faz 19.x") ve taşıma yüzünden kırılan bağlantıyı düzeltmek serbest.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor). Bulgu zaten kapanmışsa kanıtını göster, kod yazma, yalnızca kayıt adımlarını yap.
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi, hukuki metin ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.


**Kapsam dışı (dokunma, raporda an):** 404 sayfası (`FE-06`, 🟢), frontend hata raporlama aracının seçimi.

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` (silinecek dosya varsa `git rm <yol>`, taşınacak dosya varsa `git mv <eski> <yeni>`) → `git commit -m "19.21.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Bloğun başında "Başlamadan" kısmı: her depoda `git status --short --untracked-files=all` ve **beklenen satırların tam listesi** (Faz 18'deki gibi), ki fazladan dosya varsa commit'ten önce göreyim.
- Sıra: backend blokları → frontend blokları → docs bloğu → birleştirme.
- **Birleştirme bloğu:** dokunduğun her kod deposu için ayrı ayrı: `git switch faz-19-audit-fixes` → `git merge --no-ff fix/<YYYY-MM-DD>-fe-02-error-boundary -m "Merge FE-02 fix into faz-19-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-19\FAZ-19-FE-02-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (19.21.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle; §A'nın hangi satırı cevaplıydı, hangisinde varsayılan uygulandı.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili test/denetimin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, Shopier, deneme) varsa numaralı liste.
