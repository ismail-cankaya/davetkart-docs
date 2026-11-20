# PROMPT — FAZ 19.2: `ARC-01` Karar indeksi K128–K145'i bilmiyor

> **Hazırlanma:** 20 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §5.1 · tam metin [`findings/01-architecture.md`](../audits/2026-11-12-full-system-audit/findings/01-architecture.md)) · **Sıra:** 2/28 · **Efor:** S
> **Önkoşul:** 19.1 (`SEC-07`) düzeltme dalı `faz-19-audit-fixes`'e birleşmiş olmalı (§2 denetler).
> **Dokunulan depolar:** docs
> **Kullanım:** `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır.

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 19: denetimin orta öncelikli bulguları** üzerinde çalışıyoruz. `AUD-2026-11-12` 29 orta (🟡) bulgu çıkardı; `TST-01` Faz 18'de kapandı, kalan 28'i Faz 19'da her biri ayrı bir dalda ve ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `ARC-01`** bulgusunu kapatır: *Karar indeksi K128–K145'i bilmiyor*. Bu, 28 bulgunun 2. sırası.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (19.2.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `rm`, `mv`, `restore`, `checkout -- <dosya>`. İzinli: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `ARC-01` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz. Faz 19'da sırası gelecek bulgular için bkz. `davetkart-docs\phases\faz-19\README.md`.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler; en sonda tam `composer check` **ve** `composer audit`. Frontend'e dokunduysan en sonda `npm ci` + `npm run check`. Önceki bulguların eklediği denetimler (ör. `verify:plans`, varsa E2E) yeşil kalmalı.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kendi kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut/tarayıcı). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi, `contracts/*.json` + `--check`). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend sözleşme kopyası ve tr/en çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `19.2.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula, K kaydına "plandan sapma" diye yaz ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md` (sıradaki boş K numarası başlıkta)
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\findings\01-architecture.md` içindeki **`ARC-01`** tam metni · ilgili bulgular: `ARC-05` (karar kaydının yarısı backend `claude/` klasöründe) · kanıt: REPORT.md'deki `grep … uniq -c` çıktısı (K128–K145'in koddaki atıf sayıları)
4. Faz 18'in kaydı: backend `docs\rehber\fazlar\FAZ-18.md` (özellikle "gördüm, dokunmadım" tabloları ve kapanış özeti; bu bulguya değinen satırlar) · `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`
5. `davetkart-docs\phases\faz-19\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-19.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Docs: `decisions/DECISION-INDEX.md` (üstteki ⚠️ notu: K131 → K159, K139 → K166) · `_restructure/build_decision_index.py` ve `_restructure/REPORT.md` §3 · `decisions/addenda/*` ve `context/PHP-LARAVEL-SETUP.md` §7–§8 (indeksin bugünkü kaynakları).
2. Backend (salt okunur; `git show faz-19-audit-fixes:<yol>` ile): `docs/rehber/fazlar/FAZ-13.md` §4 (K128–K136) · `FAZ-14.md` (K137–K145) · `FAZ-18.md` ve `FAZ-19.md` (varsa).

**K numarası:** yeni karar = `DECISION-INDEX.md`'deki "Sıradaki boş numara". Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (denetim 12 Kasım'daydı; Faz 18 bazı satırları değiştirdi, rapordaki satırlar hâlâ geçerli mi), §A'da hangi satırlar dolu, §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
git branch --merged faz-19-audit-fixes | Select-String "sec-07-composer-audit"   # boşsa DUR: SEC-07 birleşmemiş
# backend: bu bulguda değişmesi beklenmiyor; dal açma. Değiştirmen gerekirse burada aynı adla dal aç ve raporda söyle.

cd D:\Projects\davetkart\davetkart-frontent
git fetch origin
git status --short                                   # yalnızca '?? .claude/' olabilir; başka satır varsa DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
# frontend: bu bulguda değişmesi beklenmiyor; dal açma. Değiştirmen gerekirse burada aynı adla dal aç ve raporda söyle.

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-20-faz-19-audit-fixes                             # yoksa DUR
git switch -c docs/<YYYY-MM-DD>-arc-01-decision-index            # bu bulgu yalnızca docs: kendi dalı
```

## 3. Bulgu (özet; tam metin bulgu dosyasında)

Faz 13 ve 14 backend deposunda K128–K145'i tanımladı; 12 Kasım'daki düzenleme indeksi yalnızca docs deposundan üretti. Faz 18 bunu bir ⚠️ notuyla geçici olarak yönetti (K146'dan başladı, K131 ve K139'un "daraltıldı" notlarını backend faz dosyalarına yazdı). Satırlar hâlâ indekste yok.

**Dersin özü:** karar kaydı (ADR) **tek doğruluk kaynağı** olmak zorunda. İki depoya bölünmüş kayıtta her taraf diğerini eksik görür. Düzeltme numarayı değiştirmek değil (numara asla yeniden kullanılmaz), indeksi kaynağa yetiştirmek ve bunun **bir daha kaymayacağını bir denetimle** garanti etmektir.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | K128–K145 indekse girer; kaynak sütunu backend faz dosyasına bağlantı (docs deposundan backend'e göreli bağlantı çalışmayacağı için desen: `backend: docs/rehber/fazlar/FAZ-13.md §4` metni). K131 ve K139'un durumu "daraltıldı → K159 / K166". |
| D2 | `build_decision_index.py --check`: docs deposundaki **ve** kardeş backend deposundaki (`../davetkart-backend-php-laravel`, yoksa uyarı + çıkış 2) bütün `K\d+` **tanımlarını** toplar; indekste olmayan ya da indekste olup hiçbir yerde tanımı olmayan numara varsa çıkış 1. Tanım ile atıfı ayırt etme kuralını betiğin başına yaz (ör. tablo satırı `| **K128** |` ya da başlık). |
| D3 | ⚠️ notu kaldırılır, yerine "Bu indeks `build_decision_index.py --check` ile denetlenir" satırı. Python dışında bağımlılık yok; `python -I` ile koşar. |

## 5. Adımlar ve dosya sahipliği

### Docs (`docs/<YYYY-MM-DD>-arc-01-decision-index`)
| Adım | İş |
|---|---|
| 19.2.1 | D2: `_restructure/build_decision_index.py` `--check` kipi (+ `_restructure/README.md` ya da betik başında kullanım notu). |
| 19.2.2 | D1 + D3: `decisions/DECISION-INDEX.md` K128–K145 satırları, ⚠️ notunun değişimi; `--check` çıkış 0. |
| 19.2.3 | §7'deki ortak kayıtlar (`ARC-01` backend'e dokunmadığı için faz bölümü `phases/faz-19/FAZ-19-ARC-01-KAYIT.md`'ye). |

## 6. Testler ve kalite kapısı

- `python -I _restructure/build_decision_index.py --check` → 0 (çıktıyı göster).
- **Mutant 1:** indeksten K140 satırını sil → çıkış 1 ve eksik numarayı yazıyor. **Mutant 2:** indekse tanımı olmayan K999 ekle → çıkış 1. Geri al.
- Kardeş depo yoksa davranış: klasör adını geçici olarak yanlış ver → uyarı + çıkış 2 (başarı sayılmamalı).

## 7. Kayıt (dokümantasyon)

**Faz kaydı:** bu bulgu backend'e dokunmuyor. `## 19.2 — ARC-01` bölümünü backend `FAZ-19.md`'ye **yazma** (backend dalı açılmadı); aynı içeriği docs deposundaki `phases/faz-19/FAZ-19-ARC-01-KAYIT.md` dosyasına yaz. Bir sonraki backend'e dokunan bulgu bu bölümü `FAZ-19.md`'ye taşır (raporunda hatırlat).


**Docs deposu (bu bulgunun kendi docs dalı (`docs/<YYYY-MM-DD>-arc-01-decision-index`); yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı/daralttığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". Değişen eski kararların durum sütununa "→ K…" notu (eski satırı silme).
- `phases/faz-19/README.md`: `ARC-01` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-19/FAZ-19-ARC-01-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**. Geçmiş faz kayıtlarının metnini yeniden yazma; yalnızca tarihli bir **durum notu** eklemek ("→ Faz 19.x") ve taşıma yüzünden kırılan bağlantıyı düzeltmek serbest.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor). Bulgu zaten kapanmışsa kanıtını göster, kod yazma, yalnızca kayıt adımlarını yap.
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi, hukuki metin ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.
- Bir numara iki farklı kararla tanımlanmış (gerçek çakışma): ⚠️ ile işaretle, numarayı değiştirme, sor.

**Kapsam dışı (dokunma, raporda an):** `ARC-05` (backend `claude/` klasörünün taşınması; bir sonraki sıralardan biri), kararların içeriği.

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` (silinecek dosya varsa `git rm <yol>`, taşınacak dosya varsa `git mv <eski> <yeni>`) → `git commit -m "19.2.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Bloğun başında "Başlamadan" kısmı: her depoda `git status --short --untracked-files=all` ve **beklenen satırların tam listesi** (Faz 18'deki gibi), ki fazladan dosya varsa commit'ten önce göreyim.
- Sıra: backend blokları → frontend blokları → docs bloğu → birleştirme.
- **Birleştirme bloğu:** docs deposunda: `git switch docs/2026-11-20-faz-19-audit-fixes` → `git merge --no-ff docs/<YYYY-MM-DD>-arc-01-decision-index -m "Merge ARC-01 into docs/2026-11-20-faz-19-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-19\FAZ-19-ARC-01-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (19.2.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle; §A'nın hangi satırı cevaplıydı, hangisinde varsayılan uygulandı.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili test/denetimin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, Shopier, deneme) varsa numaralı liste.
