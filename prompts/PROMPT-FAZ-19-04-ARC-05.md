# PROMPT — FAZ 19.4: `ARC-05` Eski `claude/…` yolları; backend'in `claude/` klasörü ikinci ev

> **Hazırlanma:** 20 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §5.1 · tam metin [`findings/01-architecture.md`](../audits/2026-11-12-full-system-audit/findings/01-architecture.md)) · **Sıra:** 4/28 · **Efor:** M
> **Önkoşul:** 19.3 (`ARC-02`) düzeltme dalı `faz-19-audit-fixes`'e birleşmiş olmalı (§2 denetler).
> **Dokunulan depolar:** backend (`claude/`, `docs/`) · docs
> **Kullanım:** önce §A'yı sen doldur/yap; sonra `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır.

## §A — Senin kararın (prompt'u yapıştırmadan önce doldur)

| # | Soru | Boş bırakırsan ajanın uygulayacağı varsayılan | Cevabın |
|---|---|---|---|
| 1 | Backend `claude/` klasörü taşındıktan sonra backend'de ne kalsın? | Yalnızca `claude/README.md`: "Bu klasör `davetkart-docs`'a taşındı (tarih, eşleme tablosuna bağlantı)" | |
| 2 | Taşınan dosyaların geçmişi: docs deposunda `git log` ile izlenebilsin diye ayrı bir "verbatim taşıma" commit'i mi (içerik değişmeden), sonra bağlantı düzeltmeleri mi? | Evet: önce birebir kopya commit'i, sonra bağlantı düzeltmesi commit'i | |

**Boş satır için ajan varsayılanı uygular ve bunu K kaydında "varsayılan (İsmail cevaplamadı)" diye işaretler.**

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 19: denetimin orta öncelikli bulguları** üzerinde çalışıyoruz. `AUD-2026-11-12` 29 orta (🟡) bulgu çıkardı; `TST-01` Faz 18'de kapandı, kalan 28'i Faz 19'da her biri ayrı bir dalda ve ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `ARC-05`** bulgusunu kapatır: *Eski `claude/…` yolları; backend'in `claude/` klasörü ikinci ev*. Bu, 28 bulgunun 4. sırası. Yukarıdaki §A tablosu benim kararlarım.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (19.4.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `rm`, `mv`, `restore`, `checkout -- <dosya>`. İzinli: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `ARC-05` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz. Faz 19'da sırası gelecek bulgular için bkz. `davetkart-docs\phases\faz-19\README.md`.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler; en sonda tam `composer check` **ve** `composer audit`. Frontend'e dokunduysan en sonda `npm ci` + `npm run check`. Önceki bulguların eklediği denetimler (ör. `verify:plans`, varsa E2E) yeşil kalmalı.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kendi kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut/tarayıcı). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi, `contracts/*.json` + `--check`). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend sözleşme kopyası ve tr/en çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `19.4.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula, K kaydına "plandan sapma" diye yaz ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md` (sıradaki boş K numarası başlıkta)
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\findings\01-architecture.md` içindeki **`ARC-05`** tam metni · ilgili bulgular: `ARC-01` (indeks artık iki depoyu tarıyor), `_restructure/REPORT.md` §4 · kanıt: REPORT.md'deki `grep -rlE "claude[/\\](PHP-LARAVEL-SETUP|Notlar|FAZ-|GOZDEN|TEST-DENETIMI|PROMPT)"` → 25 dosya
4. Faz 18'in kaydı: backend `docs\rehber\fazlar\FAZ-18.md` (özellikle "gördüm, dokunmadım" tabloları ve kapanış özeti; bu bulguya değinen satırlar) · `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`
5. `davetkart-docs\phases\faz-19\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-19.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Backend: `claude/` klasörünün tam listesi (22 dosya) · denetimdeki `grep` komutunu bugün yeniden koş ve 25 atfın güncel listesini çıkar · backend `CLAUDE.md` (`claude/`'a atıf var mı).
2. Docs: `_restructure/REPORT.md` §4 ve taşıma betikleri (eşleme deseni) · `decisions/addenda/`, `phases/`, `audits/`, `prompts/`, `archive/` klasörlerinin README'leri · `CLAUDE.md` §3 ("Yeni dosya nereye?") ve §8 (silme yok, arşivle).

**K numarası:** yeni karar = `DECISION-INDEX.md`'deki "Sıradaki boş numara". Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (denetim 12 Kasım'daydı; Faz 18 bazı satırları değiştirdi, rapordaki satırlar hâlâ geçerli mi), §A'da hangi satırlar dolu, §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
git branch --merged faz-19-audit-fixes | Select-String "arc-02-phase-16-17-records"   # boşsa DUR: ARC-02 birleşmemiş
git switch -c fix/<YYYY-MM-DD>-arc-05-claude-folder

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

Docs deposu 12 Kasım'da yeniden düzenlendi; backend'deki 25 dosya hâlâ eski `claude/…` yollarını gösteriyor. Ayrıca backend'in kendi `claude/` klasörü (EK-FAZ-5…9, `FAZ-10-PLANI.md`, üç gözden geçirme, test denetimi, Faz 6–9 prompt'ları) taşınmadı: K49–K63 ve K72–K106'nın tek kaynağı orada.

**Dersin özü:** "bir bilginin tek bir güncel evi olur". Taşıma yarım kaldığında iki ev de eksik olur. Taşımayı **eşleme tablosuyla** (eski yol → yeni yol) yapmak, hem bağlantı düzeltmesini mekanik hâle getirir hem de geçmişi okunur bırakır.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | Eşleme tablosu önce yazılır: backend `claude/<dosya>` → docs'taki yeni yol (`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-05…09.md`, `phases/faz-10/FAZ-10-PLANI.md`, `audits/2026-09-23-…/`, `audits/2026-09-24-test-audit/`, `audits/2026-10-09-…/`, `prompts/PROMPT-FAZ-6…9.md`). Yer kuralları docs `CLAUDE.md` §3. Tablo `_restructure/` deseniyle docs deposunda saklanır (ör. `_restructure/2026-11-backend-claude-map.md`). |
| D2 | Taşıma §A-2'ye göre. İçerik değişmez; yalnızca bağlantılar düzeltilir. Ajan dosyaları **kopyalar**, backend'deki silme `git rm` olarak §9'daki komutlarda bana kalır. |
| D3 | Backend `docs/` ve diğer dosyalardaki eski atıflar yeni yollara güncellenir. Docs deposundaki yolu backend'den göstermek için tek bir yazım biçimi seç (ör. `davetkart-docs: decisions/addenda/…`) ve kılavuza yaz. |
| D4 | `ARC-01`'in `build_decision_index.py --check`'i taşımadan sonra yeşil kalmalı (K49–K63, K72–K106'nın kaynak sütunları yeni yolları göstermeli). |

## 5. Adımlar ve dosya sahipliği

### Docs (`docs/2026-11-20-faz-19-audit-fixes` üzerinde, kod dalıyla birlikte)
| Adım | İş |
|---|---|
| 19.4.1 | D1: eşleme tablosu. |
| 19.4.2 | D2: birebir kopyalar (yeni yollarında) + klasör README'leri. |
| 19.4.3 | D2/D4: kopyaların iç bağlantıları ve `DECISION-INDEX.md` kaynak sütunları; `build_decision_index.py --check` 0. |

### Backend (`fix/<YYYY-MM-DD>-arc-05-claude-folder`)
| Adım | İş |
|---|---|
| 19.4.4 | D3: 25 (güncel sayı) dosyadaki atıfların düzeltilmesi. |
| 19.4.5 | §A-1: `claude/README.md` yönlendirme notu; diğer `claude/` dosyaları için `git rm` satırları (komutlarda). `FAZ-19.md` `## 19.4 — ARC-05`. |

### Docs
| Adım | İş |
|---|---|
| 19.4.6 | §7'deki ortak kayıtlar. |

## 6. Testler ve kalite kapısı

- Denetimin `grep` komutu backend'de (`claude/README.md` hariç) **0** döner; çıktıyı göster.
- Docs deposunda kırık göreli bağlantı taraması: taşınan dosyalardaki `](…)` bağlantılarının hedefi var mı (küçük bir Python betiği; `python -I`). **Mutant:** bir bağlantıyı boz → betik yakalar.
- `build_decision_index.py --check` → 0.

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-19.md`: yoksa oluştur (başlık: "Faz 19 — denetimin orta öncelikli bulguları (`AUD-2026-11-12`)", 28 bulgunun tablosu). `## 19.4 — ARC-05` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar (frontend dahil), eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım işler. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).
- Docs deposunda `phases/faz-19/FAZ-19-*-KAYIT.md` dosyaları varsa (backend'e dokunmayan önceki bulguların bölümleri) ve `FAZ-19.md`'de karşılıkları yoksa, onları sıra numarasına göre `FAZ-19.md`'ye taşı; docs'taki dosyayı silme, başına "Taşındı → backend `FAZ-19.md` §19.x" notu ekle.

**Docs deposu (`docs/2026-11-20-faz-19-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı/daralttığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". Değişen eski kararların durum sütununa "→ K…" notu (eski satırı silme).
- `phases/faz-19/README.md`: `ARC-05` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-19/FAZ-19-ARC-05-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**. Geçmiş faz kayıtlarının metnini yeniden yazma; yalnızca tarihli bir **durum notu** eklemek ("→ Faz 19.x") ve taşıma yüzünden kırılan bağlantıyı düzeltmek serbest.
- Backend `claude/` taşındığı için bu prompt'un ve önceki prompt'ların içinde geçen `claude\…` yollarına dokunma; bunlar geçmiş kayıt.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor). Bulgu zaten kapanmışsa kanıtını göster, kod yazma, yalnızca kayıt adımlarını yap.
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi, hukuki metin ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.
- Bir `claude/` dosyasının docs'ta zaten (farklı içerikle) bir karşılığı var: hangisinin güncel olduğuna karar verme; ikisini yan yana göster, sor.

**Kapsam dışı (dokunma, raporda an):** Dosyaların içeriğini güncelleme ya da özetleme (docs `CLAUDE.md` §8), `ARC-08`.

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` (silinecek dosya varsa `git rm <yol>`, taşınacak dosya varsa `git mv <eski> <yeni>`) → `git commit -m "19.4.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Bloğun başında "Başlamadan" kısmı: her depoda `git status --short --untracked-files=all` ve **beklenen satırların tam listesi** (Faz 18'deki gibi), ki fazladan dosya varsa commit'ten önce göreyim.
- Sıra: backend blokları → frontend blokları → docs bloğu → birleştirme.
- **Birleştirme bloğu:** dokunduğun her kod deposu için ayrı ayrı: `git switch faz-19-audit-fixes` → `git merge --no-ff fix/<YYYY-MM-DD>-arc-05-claude-folder -m "Merge ARC-05 fix into faz-19-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-19\FAZ-19-ARC-05-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (19.4.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle; §A'nın hangi satırı cevaplıydı, hangisinde varsayılan uygulandı.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili test/denetimin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, Shopier, deneme) varsa numaralı liste.
