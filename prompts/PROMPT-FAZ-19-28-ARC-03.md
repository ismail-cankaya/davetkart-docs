# PROMPT — FAZ 19.28: `ARC-03` K18 dosyaların %92'sinde çiğneniyor; 79 dosyanın kılavuzu yok

> **Hazırlanma:** 20 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §5.1 · tam metin [`findings/01-architecture.md`](../audits/2026-11-12-full-system-audit/findings/01-architecture.md)) · **Sıra:** 28/28 · **Efor:** L
> **Önkoşul:** 19.27 (`FE-54`) düzeltme dalı `faz-19-audit-fixes`'e birleşmiş olmalı (§2 denetler).
> **Dokunulan depolar:** backend · docs (frontend için yalnızca öneri)
> **Kullanım:** önce §A'yı sen doldur/yap; sonra `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır.

## §A — Senin kararın (prompt'u yapıştırmadan önce doldur)

Bu prompt Faz 19'u da kapatır (§11).

| # | Soru | Boş bırakırsan ajanın uygulayacağı varsayılan | Cevabın |
|---|---|---|---|
| 1 | Hangi kol? | **Cırcır (ratchet):** kural aynen kalır (1–3 satır); `composer check`'e `k18:check` girer ve yalnızca **bu daldan sonra değişen** dosyalarda uzun blok ya da eksik kılavuz varsa kırmızı. Mevcut ihlaller dokunuldukça temizlenir | |
| 2 | Bu bulguda en kötü iki dosya (`routes/api.php`, `AppServiceProvider.php`) taşınsın mı? | Evet: uzun açıklama blokları kılavuzlarına taşınır, kod davranışı değişmez | |
| 3 | Faz 13–14'ün kılavuzsuz dosyaları (`Actions/Pricing`, `Actions/Account`, `Requests/Account`, `Notifications`, `Services/Payment`; ~22 dosya) bu bulguda yazılsın mı? | Evet | |

**Boş satır için ajan varsayılanı uygular ve bunu K kaydında "varsayılan (İsmail cevaplamadı)" diye işaretler.**

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 19: denetimin orta öncelikli bulguları** üzerinde çalışıyoruz. `AUD-2026-11-12` 29 orta (🟡) bulgu çıkardı; `TST-01` Faz 18'de kapandı, kalan 28'i Faz 19'da her biri ayrı bir dalda ve ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `ARC-03`** bulgusunu kapatır: *K18 dosyaların %92'sinde çiğneniyor; 79 dosyanın kılavuzu yok*. Bu, 28 bulgunun 28. sırası. Yukarıdaki §A tablosu benim kararlarım.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (19.28.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `rm`, `mv`, `restore`, `checkout -- <dosya>`. İzinli: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `ARC-03` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz. Faz 19'da sırası gelecek bulgular için bkz. `davetkart-docs\phases\faz-19\README.md`.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler; en sonda tam `composer check` **ve** `composer audit`. Frontend'e dokunduysan en sonda `npm ci` + `npm run check`. Önceki bulguların eklediği denetimler (ör. `verify:plans`, varsa E2E) yeşil kalmalı.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kendi kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut/tarayıcı). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi, `contracts/*.json` + `--check`). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend sözleşme kopyası ve tr/en çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `19.28.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula, K kaydına "plandan sapma" diye yaz ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md` (sıradaki boş K numarası başlıkta)
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\findings\01-architecture.md` içindeki **`ARC-03`** tam metni · ilgili bulgular: K18 · `evidence\commands\ARC-k18-guide-gaps.txt` · `evidence\scripts\arc-k18-guide-gaps.sh` · kanıt: `bash evidence/scripts/arc-k18-guide-gaps.sh` (362 dosya, 79 kılavuzsuz; 287 üretim dosyasının 265'inde 3 satırdan uzun yorum)
4. Faz 18'in kaydı: backend `docs\rehber\fazlar\FAZ-18.md` (özellikle "gördüm, dokunmadım" tabloları ve kapanış özeti; bu bulguya değinen satırlar) · `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`
5. `davetkart-docs\phases\faz-19\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-19.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Backend: K18'in metni (`davetkart-docs/context/PHP-LARAVEL-SETUP.md` §2 "Açıklama nereye yazılır?") · `routes/api.php` · `app/Providers/AppServiceProvider.php` · `docs/rehber/` yapısı · `composer.json` `check` zinciri ve mevcut `--check` komutları (desen) · denetimin `arc-k18-guide-gaps.sh` betiği (Windows'ta bash yoksa PHP komutu olarak yeniden yaz).
2. Faz 18–19 boyunca eklenen dosyalar (kılavuzları var mı): `git diff --name-only main...faz-19-audit-fixes -- app`.

**K numarası:** yeni karar = `DECISION-INDEX.md`'deki "Sıradaki boş numara". Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (denetim 12 Kasım'daydı; Faz 18 bazı satırları değiştirdi, rapordaki satırlar hâlâ geçerli mi), §A'da hangi satırlar dolu, §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
git switch -c fix/<YYYY-MM-DD>-arc-03-k18-ratchet

cd D:\Projects\davetkart\davetkart-frontent
git fetch origin
git status --short                                   # yalnızca '?? .claude/' olabilir; başka satır varsa DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
git branch --merged faz-19-audit-fixes | Select-String "fe-54-accessibility"   # boşsa DUR: FE-54 birleşmemiş
# frontend: bu bulguda değişmesi beklenmiyor; dal açma. Değiştirmen gerekirse burada aynı adla dal aç ve raporda söyle.

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-20-faz-19-audit-fixes                             # yoksa DUR
```

## 3. Bulgu (özet; tam metin bulgu dosyasında)

K18 "kod yorumu 1–3 satır, ayrıntı kılavuzda" diyor; üretim kodundaki 287 dosyanın 265'inde 3 satırdan uzun yorum bloğu var (675 blok, en uzunu 50 satır). Ters yönde 362 kod dosyasının 79'unun kılavuzu yok. `routes/api.php`'de 40 rota 300 satır açıklamanın arasında.

**Dersin özü:** yorum kodun **neden** öyle olduğunu söylemeli ve kodla birlikte eskir; uzun bir blok, yanındaki satır değiştiğinde güncellenmeyen ilk şeydir. Kuralın kendisi doğru, sorun ihlalin **ölçülmemesi**. Büyük bir borcu bir kerede kapatmak yerine "yeni borç yok" kapısı (cırcır) koyup eskiyi dokundukça ödemek, sürdürülebilir olandır.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | `php artisan k18:check` (ad deseninle uyumlu): verilen taban referansına (`--base=<ref>`, varsayılan `faz-19-audit-fixes`'in bu daldan önceki ucu ya da `main`) göre değişen `app/`, `routes/`, `config/`, `database/` dosyalarında (a) 3 satırdan uzun yorum bloğu, (b) eşi olmayan `docs/rehber/<aynı-yol>.md` varsa çıkış 1. Docblock'taki tip ek açıklamaları (`@param`, `@return`, PHPStan generic'leri) sayılmaz; kural betiğin başında açık. `composer check` zincirine girer; taban referansı CI'da nasıl verilecek, kılavuzda. |
| D2 | §A-2: `routes/api.php` ve `AppServiceProvider.php` blokları kılavuzlarına taşınır; kodda 1–3 satırlık "neden" + kılavuz bağlantısı kalır. Davranış değişmez (rota listesi önce/sonra aynı: `php artisan route:list --json` karşılaştırması). |
| D3 | §A-3: eksik kılavuzlar yazılır (envanter tablosu `FAZ-19.md`'ye). |
| D4 | Frontend için aynı denetim **önerilir** (raporda); bu bulguda frontend'e dokunulmaz. |

## 5. Adımlar ve dosya sahipliği

### Backend (`fix/<YYYY-MM-DD>-arc-03-k18-ratchet`)
| Adım | İş |
|---|---|
| 19.28.1 | D1: komut + test + `composer.json` + kılavuz. |
| 19.28.2 | D2: `routes/api.php` + kılavuzu. |
| 19.28.3 | D2: `AppServiceProvider.php` + kılavuzu. |
| 19.28.4 | D3: eksik kılavuzlar (klasör başına bir commit: `Actions/Pricing`, `Actions/Account`, `Requests/Account`, `Notifications`, `Services/Payment`, diğerleri). |
| 19.28.5 | `FAZ-19.md` `## 19.28 — ARC-03` + §11 kapanış özeti. |

### Docs
| Adım | İş |
|---|---|
| 19.28.6 | §7'deki ortak kayıtlar; K18 satırına "→ K… (denetimle)". |

## 6. Testler ve kalite kapısı

- `k18:check` testi: uzun bloklu yeni dosya → 1; kılavuzu olan kısa yorumlu dosya → 0; docblock tip ek açıklamaları sayılmıyor. **Mutant:** eşik karşılaştırmasını `>` yerine `>=` yap ya da kılavuz kontrolünü kaldır → kırmızı.
- `php artisan route:list --json` önce/sonra aynı (D2).
- Denetim betiğinin güncel çıktısı: önce/sonra (79 → ?, 265 → ?).
- Tam `composer check`, `composer audit`.

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-19.md`: yoksa oluştur (başlık: "Faz 19 — denetimin orta öncelikli bulguları (`AUD-2026-11-12`)", 28 bulgunun tablosu). `## 19.28 — ARC-03` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar (frontend dahil), eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım işler. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).
- Docs deposunda `phases/faz-19/FAZ-19-*-KAYIT.md` dosyaları varsa (backend'e dokunmayan önceki bulguların bölümleri) ve `FAZ-19.md`'de karşılıkları yoksa, onları sıra numarasına göre `FAZ-19.md`'ye taşı; docs'taki dosyayı silme, başına "Taşındı → backend `FAZ-19.md` §19.x" notu ekle.

**Docs deposu (`docs/2026-11-20-faz-19-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı/daralttığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". Değişen eski kararların durum sütununa "→ K…" notu (eski satırı silme).
- `phases/faz-19/README.md`: `ARC-03` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-19/FAZ-19-ARC-03-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**. Geçmiş faz kayıtlarının metnini yeniden yazma; yalnızca tarihli bir **durum notu** eklemek ("→ Faz 19.x") ve taşıma yüzünden kırılan bağlantıyı düzeltmek serbest.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor). Bulgu zaten kapanmışsa kanıtını göster, kod yazma, yalnızca kayıt adımlarını yap.
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi, hukuki metin ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.


**Kapsam dışı (dokunma, raporda an):** Bütün uzun yorumların taşınması (cırcırla zamanla), frontend denetimi (öneri).

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` (silinecek dosya varsa `git rm <yol>`, taşınacak dosya varsa `git mv <eski> <yeni>`) → `git commit -m "19.28.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Bloğun başında "Başlamadan" kısmı: her depoda `git status --short --untracked-files=all` ve **beklenen satırların tam listesi** (Faz 18'deki gibi), ki fazladan dosya varsa commit'ten önce göreyim.
- Sıra: backend blokları → frontend blokları → docs bloğu → birleştirme.
- **Birleştirme bloğu:** dokunduğun her kod deposu için ayrı ayrı: `git switch faz-19-audit-fixes` → `git merge --no-ff fix/<YYYY-MM-DD>-arc-03-k18-ratchet -m "Merge ARC-03 fix into faz-19-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-19\FAZ-19-ARC-03-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (19.28.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle; §A'nın hangi satırı cevaplıydı, hangisinde varsayılan uygulandı.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili test/denetimin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, Shopier, deneme) varsa numaralı liste.

## 11. Faz 19 kapanışı (ARC-03'ten sonra, aynı oturumda)

Bu dal, önceki 27 düzeltmenin birleştiği `faz-19-audit-fixes`'ten açıldığı için Faz 19'un son hâlini temsil eder.

1. Bu dalda backend `composer check` **ve** `composer audit`; frontend `npm ci` + `npm run check` + `npm run e2e` (+ `npm run perf` bütçe raporu). Çıktıları B7 tablosuna yaz.
2. `docs/rehber/fazlar/FAZ-19.md` başına özet: 28 bulgunun durumu, K aralığı, kalan elle işler (Shopier cevabı, takvim, izleme hesabı, hukukçu …), docs'taki `FAZ-19-*-KAYIT.md` bölümlerinin hepsinin `FAZ-19.md`'ye taşındığının kontrolü (19.28.5 commit'ine girer).
3. Docs: `phases/faz-19/README.md` tablosunu tamamla; `phases/README.md`'de Faz 19 satırı; `CHANGELOG.md`.
4. **Bana komutlar (çalıştırma):** a) ARC-03 dalını `faz-19-audit-fixes`'e birleştirme; b) `faz-19-audit-fixes` → `main` (önce backend, sonra frontend; `YAYIN-SIRASI.md`); c) **yalnızca** 1. maddedeki kapılar yeşilse iki depoda `v1.2.0` etiketi ve `git push origin v1.2.0`; d) docs dalının `main`'e birleştirilmesi; e) dağıtım sırası ve dağıtım sonrası duman testleri (güvenlik başlıkları, `/api/health`, önizleme botu).
5. Kapılardan biri kırmızıysa etiket komutunu **verme**; engelleri listele.
6. Raporun sonuna "Faz 19'dan sonra sıradaki işler": 22 düşük (🟢) ve 5 öneri (💡) bulgu arasından yayından sonra ilk ele alınması gerekenler, gerekçesiyle (öneri; karar benim).
