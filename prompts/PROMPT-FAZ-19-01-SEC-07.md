# PROMPT — FAZ 19.1: `SEC-07` Composer bağımlılıklarında bilinen açıklar; `composer audit` kırmızı

> **Hazırlanma:** 20 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §5.1 · tam metin [`findings/02-security.md`](../audits/2026-11-12-full-system-audit/findings/02-security.md)) · **Sıra:** 1/28 · **Efor:** S
> **Önkoşul:** Faz 18'in bütün commit komutları çalıştırılmış olmalı; §A'daki dalları sen açarsın.
> **Dokunulan depolar:** backend · docs
> **Kullanım:** önce §A'yı sen doldur/yap; sonra `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır.

## §A — Senin kararın (prompt'u yapıştırmadan önce doldur)

Bu prompt Faz 19'u da başlatır. **Önce Faz 18'in commit komutlarının hepsini çalıştırmış ol** (`davetkart-docs\phases\faz-18\FAZ-18-*-COMMIT-KOMUTLARI.md`, en az §1–§3; altı `fix/…` dalı `faz-18-audit-fixes`'e birleşmiş olmalı). Sonra entegrasyon dalını aç:

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-18-audit-fixes
git branch --no-merged faz-18-audit-fixes --list "fix/*"   # boş olmalı
git status --short                                         # boş olmalı
git switch -c faz-19-audit-fixes

cd D:\Projects\davetkart\davetkart-frontent
git switch faz-18-audit-fixes
git branch --no-merged faz-18-audit-fixes --list "fix/*"   # boş olmalı
git status --short                                         # yalnızca '?? .claude/' olabilir
git switch -c faz-19-audit-fixes
```

Faz 18'i `main`'e henüz birleştirmediysen sorun değil: 19.1 sonunda `faz-19-audit-fixes` (= Faz 18 + `SEC-07`) `main`'e gider ve **`v1.1.0`** etiketi o zaman atılır (§11).

| # | Soru | Boş bırakırsan ajanın uygulayacağı varsayılan | Cevabın |
|---|---|---|---|
| 1 | Güncellemeyi yalnızca açık taşıyan paketlerle mi sınırlayalım, yoksa `laravel/framework` + bütün `symfony/*` küçük sürüm güncellemesi mi? | `composer update "symfony/*" laravel/framework --with-all-dependencies` (raporun önerisi; hepsi semver uyumlu) | |
| 2 | Callback adresi `config('app.url')`'den mi üretilsin? (Denetim: `url(CALLBACK_PATH)` istek host'una güveniyor) | Evet | |

**Boş satır için ajan varsayılanı uygular ve bunu K kaydında "varsayılan (İsmail cevaplamadı)" diye işaretler.**

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 19: denetimin orta öncelikli bulguları** üzerinde çalışıyoruz. `AUD-2026-11-12` 29 orta (🟡) bulgu çıkardı; `TST-01` Faz 18'de kapandı, kalan 28'i Faz 19'da her biri ayrı bir dalda ve ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `SEC-07`** bulgusunu kapatır: *Composer bağımlılıklarında bilinen açıklar; `composer audit` kırmızı*. Bu, 28 bulgunun 1. sırası. Yukarıdaki §A tablosu benim kararlarım.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (19.1.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `rm`, `mv`, `restore`, `checkout -- <dosya>`. İzinli: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `SEC-07` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz. Faz 19'da sırası gelecek bulgular için bkz. `davetkart-docs\phases\faz-19\README.md`.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler; en sonda tam `composer check` **ve** `composer audit`. Frontend'e dokunduysan en sonda `npm ci` + `npm run check`. Önceki bulguların eklediği denetimler (ör. `verify:plans`, varsa E2E) yeşil kalmalı.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kendi kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut/tarayıcı). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi, `contracts/*.json` + `--check`). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend sözleşme kopyası ve tr/en çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `19.1.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula, K kaydına "plandan sapma" diye yaz ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md` (sıradaki boş K numarası başlıkta)
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\findings\02-security.md` içindeki **`SEC-07`** tam metni · ilgili bulgular: `TST-01` (kapandı), `OPS-01` (yayın kontrol listesi), `SEC-03` (callback adresi) · kanıt: `evidence\commands\B2-composer-audit.txt`; Faz 18 kapanışında yeniden koşuldu: 6 pakette 9 açık (`FAZ-18.md` "Faz 18 kapanış özeti")
4. Faz 18'in kaydı: backend `docs\rehber\fazlar\FAZ-18.md` (özellikle "gördüm, dokunmadım" tabloları ve kapanış özeti; bu bulguya değinen satırlar) · `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`
5. `davetkart-docs\phases\faz-19\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-19.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Backend: `composer.json`, `composer.lock` (güncellenecek paketlerin bugünkü sürümleri) · `.github/workflows/ci.yml` (`composer audit` adımı) · `app/Services/Payment/ShopierGateway.php` (`url(CALLBACK_PATH)` ve diğer `url()`/`route()` ile üretilen dış adresler) · `config/app.php` (`url`) · `TrustProxies`/`trustedproxies` ayarı (bootstrap/app.php).
2. Docs: `operations/deployment/YAYIN-SIRASI.md` (yayın öncesi kontrol listesi, etiket komutları) · `phases/faz-18/FAZ-18-SEC-04-COMMIT-KOMUTLARI.md` §4–§7 (Faz 18 kapanış komutları).

**K numarası:** yeni karar = `DECISION-INDEX.md`'deki "Sıradaki boş numara". Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (denetim 12 Kasım'daydı; Faz 18 bazı satırları değiştirdi, rapordaki satırlar hâlâ geçerli mi), §A'da hangi satırlar dolu, §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
git switch -c fix/<YYYY-MM-DD>-sec-07-composer-audit

cd D:\Projects\davetkart\davetkart-frontent
git fetch origin
git status --short                                   # yalnızca '?? .claude/' olabilir; başka satır varsa DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
# frontend: bu bulguda değişmesi beklenmiyor; dal açma. Değiştirmen gerekirse burada aynı adla dal aç ve raporda söyle.

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-20-faz-19-audit-fixes                             # yoksa DUR
```

## 3. Bulgu (özet; tam metin bulgu dosyasında)

`composer audit` Symfony ve Laravel paketlerinde 6 pakette 9 bilinen açık gösteriyor (denetim günü 8; Faz 18 kapanışında 9). CI bu adımda kırmızı ve `v1.1.0` etiketi bunun yüzünden bekliyor (`OPS-01`, K150). Doğrudan bir sömürü yolu görülmedi ama "üretilen URL'ler istemcinin seçtiği host'u gösterebilir" maddesi `ShopierGateway`'deki `url(CALLBACK_PATH)` çağrısına dokunuyor.

**Dersin özü:** bağımlılık açığı senin yazmadığın ama senin sorumluluğunda olan koddur. Kırmızıya alışılmış bir kapı okunmaz hâle gelir; gerçek bir kritik açık aynı gürültüde kaybolur. Dış adres üretirken isteğin `Host` başlığına değil yapılandırmaya güvenmek (host header injection) aynı dersin kod tarafıdır.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | Güncelleme §A-1'e göre. `composer.lock` dışında `composer.json` kısıtı değişmez; değişmesi gerekirse DUR. |
| D2 | Dışarıya verilen her mutlak adres (Shopier callback/OSB dönüşü, e-posta bağlantıları, ödeme dönüş sayfası) `config('app.url')` ya da `config('davetkart.frontend.url')`'den üretilir; istek host'undan değil. `URL::forceRootUrl` gibi küresel bir çözüm yerine ilgili yerde açık üretim (ya da tek bir yardımcı). §A-2 "hayır" ise yalnızca D1. |
| D3 | Kalite kapısı tanımı genişler: "yayın adayı" = `composer check` ✅ **ve** `composer audit` ✅ (K150'nin tamamlayıcısı). `composer audit`'in `composer check` zincirine girip girmeyeceğini değerlendir: ağ isteği gerektirdiği için girmemesi ve CI'da ayrı adım kalması daha doğru olabilir; seçimini K'ya yaz. |

## 5. Adımlar ve dosya sahipliği

### Backend (`fix/<YYYY-MM-DD>-sec-07-composer-audit`)
| Adım | İş |
|---|---|
| 19.1.1 | D1: `composer update …` → `composer audit` (çıkış 0) → tam `composer check`. Değişen sürümleri tablo hâlinde kılavuza yaz (`docs/rehber/composer-guncelleme.md` ya da deseninle uyumlu bir yer). Dosyalar: `composer.lock` (+ gerekirse `composer.json`). |
| 19.1.2 | D2: callback adresinin üretimi + test + kılavuz. |
| 19.1.3 | `docs/rehber/fazlar/FAZ-19.md` oluştur + `## 19.1 — SEC-07`. |

### Docs
| Adım | İş |
|---|---|
| 19.1.4 | §7'deki ortak kayıtlar. `YAYIN-SIRASI.md` kontrol listesindeki `composer audit` maddesini Faz 19.1'e bağla. |

## 6. Testler ve kalite kapısı

- `composer audit` çıkış 0 (çıktıyı göster).
- D2 testi: `the_shopier_callback_url_ignores_the_request_host`: `Host: evil.example` başlıklı checkout isteğinde forma giden callback adresi `config('app.url')` ile başlar. **Mutant:** `url(...)`'e geri dön → kırmızı.
- Tam `composer check` (test sayısını yaz; Faz 18 sonunda 1166 idi).

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-19.md`: yoksa oluştur (başlık: "Faz 19 — denetimin orta öncelikli bulguları (`AUD-2026-11-12`)", 28 bulgunun tablosu). `## 19.1 — SEC-07` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar (frontend dahil), eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım işler. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).
- Docs deposunda `phases/faz-19/FAZ-19-*-KAYIT.md` dosyaları varsa (backend'e dokunmayan önceki bulguların bölümleri) ve `FAZ-19.md`'de karşılıkları yoksa, onları sıra numarasına göre `FAZ-19.md`'ye taşı; docs'taki dosyayı silme, başına "Taşındı → backend `FAZ-19.md` §19.x" notu ekle.

**Docs deposu (`docs/2026-11-20-faz-19-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı/daralttığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". Değişen eski kararların durum sütununa "→ K…" notu (eski satırı silme).
- `phases/faz-19/README.md`: `SEC-07` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-19/FAZ-19-SEC-07-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**. Geçmiş faz kayıtlarının metnini yeniden yazma; yalnızca tarihli bir **durum notu** eklemek ("→ Faz 19.x") ve taşıma yüzünden kırılan bağlantıyı düzeltmek serbest.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor). Bulgu zaten kapanmışsa kanıtını göster, kod yazma, yalnızca kayıt adımlarını yap.
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi, hukuki metin ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.
- Güncelleme bir majör sürüm atlatıyor ya da `composer check`'te davranış değişikliği kaynaklı kırmızı test çıkıyor: testi "düzeltme", farkı göster ve sor.

**Kapsam dışı (dokunma, raporda an):** Frontend `npm audit` (Faz 18'de temizdi; yine de `npm audit --omit=dev` sonucunu rapora yaz), `ARC-08` (dal temizliği).

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` (silinecek dosya varsa `git rm <yol>`, taşınacak dosya varsa `git mv <eski> <yeni>`) → `git commit -m "19.1.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Bloğun başında "Başlamadan" kısmı: her depoda `git status --short --untracked-files=all` ve **beklenen satırların tam listesi** (Faz 18'deki gibi), ki fazladan dosya varsa commit'ten önce göreyim.
- Sıra: backend blokları → frontend blokları → docs bloğu → birleştirme.
- **Birleştirme bloğu:** dokunduğun her kod deposu için ayrı ayrı: `git switch faz-19-audit-fixes` → `git merge --no-ff fix/<YYYY-MM-DD>-sec-07-composer-audit -m "Merge SEC-07 fix into faz-19-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-19\FAZ-19-SEC-07-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (19.1.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle; §A'nın hangi satırı cevaplıydı, hangisinde varsayılan uygulandı.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili test/denetimin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, Shopier, deneme) varsa numaralı liste.

## 11. `v1.1.0` (Faz 18 + `SEC-07`) — yalnızca komut ver, çalıştırma

`SEC-07` kapanınca Faz 18'in bekleyen etiketi atılabilir. Bu dalda `composer check` ✅ **ve** `composer audit` ✅ **ve** frontend `npm ci` + `npm run check` ✅ ise (üçünün çıktısını gör), §9'daki birleştirme bloğundan sonra şu blokları hazırla (`YAYIN-SIRASI.md`'deki sıra: önce backend, sonra frontend):

1. `faz-19-audit-fixes` → `main` (backend; sonra frontend). Faz 18 `main`'e zaten birleştiyse yalnızca `SEC-07` gelir.
2. İki depoda `git tag -a v1.1.0 -m "Release v1.1.0: Phase 18 audit fixes + SEC-07"` ve `git push origin v1.1.0`.
3. Docs deposunda Faz 18 docs dalının ve bu dalın `main`'e birleştirilmesi.
4. Dağıtım sırası ve dağıtım sonrası duman testi (`YAYIN-SIRASI.md` ve `FAZ-18-SEC-04-COMMIT-KOMUTLARI.md` §7'ye bağlantı ver, kopyalama).

Üçünden biri kırmızıysa etiket komutunu **verme**; engeli yaz.
