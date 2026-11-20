# PROMPT — FAZ 19.11: `TST-02` Kilitlerin hiçbiri testle korunmuyor

> **Hazırlanma:** 20 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §5.1 · tam metin [`findings/03-testing.md`](../audits/2026-11-12-full-system-audit/findings/03-testing.md)) · **Sıra:** 11/28 · **Efor:** M
> **Önkoşul:** 19.10 (`SEC-06`) düzeltme dalı `faz-19-audit-fixes`'e birleşmiş olmalı (§2 denetler).
> **Dokunulan depolar:** backend · docs
> **Kullanım:** `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır.

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 19: denetimin orta öncelikli bulguları** üzerinde çalışıyoruz. `AUD-2026-11-12` 29 orta (🟡) bulgu çıkardı; `TST-01` Faz 18'de kapandı, kalan 28'i Faz 19'da her biri ayrı bir dalda ve ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `TST-02`** bulgusunu kapatır: *Kilitlerin hiçbiri testle korunmuyor*. Bu, 28 bulgunun 11. sırası.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (19.11.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `rm`, `mv`, `restore`, `checkout -- <dosya>`. İzinli: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `TST-02` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz. Faz 19'da sırası gelecek bulgular için bkz. `davetkart-docs\phases\faz-19\README.md`.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler; en sonda tam `composer check` **ve** `composer audit`. Frontend'e dokunduysan en sonda `npm ci` + `npm run check`. Önceki bulguların eklediği denetimler (ör. `verify:plans`, varsa E2E) yeşil kalmalı.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kendi kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut/tarayıcı). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi, `contracts/*.json` + `--check`). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend sözleşme kopyası ve tr/en çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `19.11.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula, K kaydına "plandan sapma" diye yaz ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md` (sıradaki boş K numarası başlıkta)
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\findings\03-testing.md` içindeki **`TST-02`** tam metni · ilgili bulgular: K111 · backend `CLAUDE.md` §3 ("İki katman, iki farklı yarış") · Faz 18.3 (yeni kilit SQL düzeyinde sınandı) · Faz 18.4 "gördüm, dokunmadım": **donmuş hak eşzamanlı yayında bağlanabiliyor** (`ClaimReleasedOrderAction`, `withoutOpenRefundRequest()`) · kanıt: `evidence\mutation\M14.txt`, `M47.txt`, `M48.txt`, `M49.txt` (dördü de HAYATTA) · `TST-test-quality-metrics.txt` §4
4. Faz 18'in kaydı: backend `docs\rehber\fazlar\FAZ-18.md` (özellikle "gördüm, dokunmadım" tabloları ve kapanış özeti; bu bulguya değinen satırlar) · `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`
5. `davetkart-docs\phases\faz-19\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-19.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Backend: bütün `lockForUpdate()` çağrıları (`git grep -n lockForUpdate app`; denetimde 17, Faz 18 sonrası daha fazla) ve her birinin Action testi · Faz 18.3'ün `DB::listen` kilit testi (desen) · `ClaimReleasedOrderAction` ve iade talebi akışı (`FAZ-18.md` §18.4 "gördüm, dokunmadım" satırı tam metniyle) · `phpunit.xml` ve test veritabanı yapılandırması (`TestSuiteIsolationTest`) · `config/database.php` (ikinci bağlantı tanımlanabilir mi).
2. Denetim mutant kayıtları M14, M47, M48, M49 (hangi satır silindi).

**K numarası:** yeni karar = `DECISION-INDEX.md`'deki "Sıradaki boş numara". Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (denetim 12 Kasım'daydı; Faz 18 bazı satırları değiştirdi, rapordaki satırlar hâlâ geçerli mi), §A'da hangi satırlar dolu, §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
git branch --merged faz-19-audit-fixes | Select-String "sec-06-rate-limit-keys"   # boşsa DUR: SEC-06 birleşmemiş
git switch -c fix/<YYYY-MM-DD>-tst-02-lock-tests

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

Para ve kota değişmezlerini koruyan kilit satırlarından biri silinse `composer check` yeşil kalıyor: hiçbir test iki işlemi aynı anda koşturmuyor. Denetimde denenen dört kilit mutantının dördü hayatta kaldı. Faz 18.3 yeni kilidi SQL düzeyinde sınadı ama kalan kilitler testsiz; Faz 18.4 ayrıca gerçek bir yarış buldu (donmuş hak, eşzamanlı yayında bağlanabiliyor).

**Dersin özü:** tek süreçli test paketi **sıralı** doğruluğu kanıtlar; yarış durumu iki işlemin araya girmesiyle ortaya çıkar. Kilit, sıralı koşuda görünmez bir satırdır: silinince hiçbir test bozulmaz, çünkü hiçbir test onun engellediği durumu üretmez. Çözüm iki katmanlı: ucuz ve kesin (SQL'de `FOR UPDATE` var mı) + gerçekçi (iki bağlantı, `lock_timeout`).

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | Ortak test yardımcısı (trait ya da `tests/Support/…`): bir kapanışı çalıştırırken yürüyen SQL'i yakalar ve belirli tabloda `for update` geçtiğini doğrular. Her `lockForUpdate()` çağrısı için bir test (envanter tablosu kılavuzda: dosya · satır · koruduğu değişmez · test adı). |
| D2 | İki bağlantılı gerçek yarış testi en az dört kritik kilit için (M14 hediye kodu, M47 ödeme bildirimi, M48 LCV kotası, M49 serbest hak): A bağlantısı transaction açıp satırı kilitler, B bağlantısı `SET LOCAL lock_timeout = '200ms'` ile aynı Action'ı çağırır ve `55P03` bekler. İkinci bağlantı test veritabanına işaret eder (asla geliştirme veritabanına). `RefreshDatabase` transaction'ı bu testlerde nasıl ele alınıyor: kılavuzda açıkla (gerekirse `DatabaseMigrations`/ayrı grup). |
| D3 | Faz 18.4'ün bulduğu yarış: önce bir yarış testiyle **kırmızı** olduğunu göster. Düzeltme `ClaimReleasedOrderAction` içinde yerel kalıyorsa (ör. kilit sırası ya da kilitli satırda yeniden sınama) bu dalda yap ve K yaz; iade akışının durum makinesini değiştirmeyi gerektiriyorsa DUR. |
| D4 | Yarış testleri ayrı bir PHPUnit grubu (`@group concurrency`); `composer check`'te koşar. Süre artışını ölç ve yaz. |

## 5. Adımlar ve dosya sahipliği

### Backend (`fix/<YYYY-MM-DD>-tst-02-lock-tests`)
| Adım | İş |
|---|---|
| 19.11.1 | D1: yardımcı + kılavuz + envanter. |
| 19.11.2 | D1: her kilit için SQL düzeyi test (Action başına mevcut test dosyalarına). |
| 19.11.3 | D2 + D4: iki bağlantılı yarış testleri (+ gerekirse `config/database.php` test bağlantısı, `phpunit.xml`). |
| 19.11.4 | D3: yarış testi + (yerelse) düzeltme + kılavuz. |
| 19.11.5 | `FAZ-19.md` `## 19.11 — TST-02`. |

### Docs
| Adım | İş |
|---|---|
| 19.11.6 | §7'deki ortak kayıtlar; backend `CLAUDE.md` §3'e atıf (değiştirmek gerekiyorsa backend commit'ine). |

## 6. Testler ve kalite kapısı

- **Denetimin dört mutantını yeniden uygula** (M14, M47, M48, M49: kilidi sil) → bu kez her biri en az bir testte kırmızı. Sonucu tablo olarak yaz; geri al.
- Envanterdeki her `lockForUpdate()` için: sil → kırmızı (en az örnekleme olarak beş tanesini dene, hepsini denediysen söyle).
- D3: düzeltmeden önce kırmızı, sonra yeşil.
- Tam `composer check` ve süre farkı.

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-19.md`: yoksa oluştur (başlık: "Faz 19 — denetimin orta öncelikli bulguları (`AUD-2026-11-12`)", 28 bulgunun tablosu). `## 19.11 — TST-02` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar (frontend dahil), eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım işler. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).
- Docs deposunda `phases/faz-19/FAZ-19-*-KAYIT.md` dosyaları varsa (backend'e dokunmayan önceki bulguların bölümleri) ve `FAZ-19.md`'de karşılıkları yoksa, onları sıra numarasına göre `FAZ-19.md`'ye taşı; docs'taki dosyayı silme, başına "Taşındı → backend `FAZ-19.md` §19.x" notu ekle.

**Docs deposu (`docs/2026-11-20-faz-19-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı/daralttığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". Değişen eski kararların durum sütununa "→ K…" notu (eski satırı silme).
- `phases/faz-19/README.md`: `TST-02` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-19/FAZ-19-TST-02-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**. Geçmiş faz kayıtlarının metnini yeniden yazma; yalnızca tarihli bir **durum notu** eklemek ("→ Faz 19.x") ve taşıma yüzünden kırılan bağlantıyı düzeltmek serbest.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor). Bulgu zaten kapanmışsa kanıtını göster, kod yazma, yalnızca kayıt adımlarını yap.
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi, hukuki metin ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.
- İkinci bir veritabanı bağlantısı test ortamında kurulamıyor ya da geliştirme veritabanına dokunma riski var.
- D3'ün düzeltmesi iade akışının durumlarını değiştirmeyi gerektiriyor.

**Kapsam dışı (dokunma, raporda an):** HTTP düzeyinde eşzamanlı istek testleri (`TST-04`), `ARC-09`.

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` (silinecek dosya varsa `git rm <yol>`, taşınacak dosya varsa `git mv <eski> <yeni>`) → `git commit -m "19.11.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Bloğun başında "Başlamadan" kısmı: her depoda `git status --short --untracked-files=all` ve **beklenen satırların tam listesi** (Faz 18'deki gibi), ki fazladan dosya varsa commit'ten önce göreyim.
- Sıra: backend blokları → frontend blokları → docs bloğu → birleştirme.
- **Birleştirme bloğu:** dokunduğun her kod deposu için ayrı ayrı: `git switch faz-19-audit-fixes` → `git merge --no-ff fix/<YYYY-MM-DD>-tst-02-lock-tests -m "Merge TST-02 fix into faz-19-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-19\FAZ-19-TST-02-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (19.11.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle; §A'nın hangi satırı cevaplıydı, hangisinde varsayılan uygulandı.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili test/denetimin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, Shopier, deneme) varsa numaralı liste.
