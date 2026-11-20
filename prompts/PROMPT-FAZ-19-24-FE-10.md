# PROMPT — FAZ 19.24: `FE-10` Ana giriş paketi 1,64 MB: 299 şablon her sayfaya, misafir sayfasına bile yükleniyor

> **Hazırlanma:** 20 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §5.1 · tam metin [`findings/04-frontend-e2e.md`](../audits/2026-11-12-full-system-audit/findings/04-frontend-e2e.md)) · **Sıra:** 24/28 · **Efor:** M
> **Önkoşul:** 19.23 (`FE-04`) düzeltme dalı `faz-19-audit-fixes`'e birleşmiş olmalı (§2 denetler).
> **Dokunulan depolar:** frontend · docs
> **Kullanım:** önce §A'yı sen doldur/yap; sonra `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır.

## §A — Senin kararın (prompt'u yapıştırmadan önce doldur)

| # | Soru | Boş bırakırsan ajanın uygulayacağı varsayılan | Cevabın |
|---|---|---|---|
| 1 | Ana giriş paketi için bütçe (ham, sıkıştırılmamış)? | 400 kB; aşarsa `npm run check` kırmızı | |

**Boş satır için ajan varsayılanı uygular ve bunu K kaydında "varsayılan (İsmail cevaplamadı)" diye işaretler.**

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 19: denetimin orta öncelikli bulguları** üzerinde çalışıyoruz. `AUD-2026-11-12` 29 orta (🟡) bulgu çıkardı; `TST-01` Faz 18'de kapandı, kalan 28'i Faz 19'da her biri ayrı bir dalda ve ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `FE-10`** bulgusunu kapatır: *Ana giriş paketi 1,64 MB: 299 şablon her sayfaya, misafir sayfasına bile yükleniyor*. Bu, 28 bulgunun 24. sırası. Yukarıdaki §A tablosu benim kararlarım.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (19.24.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `rm`, `mv`, `restore`, `checkout -- <dosya>`. İzinli: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `FE-10` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz. Faz 19'da sırası gelecek bulgular için bkz. `davetkart-docs\phases\faz-19\README.md`.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler; en sonda tam `composer check` **ve** `composer audit`. Frontend'e dokunduysan en sonda `npm ci` + `npm run check`. Önceki bulguların eklediği denetimler (ör. `verify:plans`, varsa E2E) yeşil kalmalı.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kendi kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut/tarayıcı). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi, `contracts/*.json` + `--check`). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend sözleşme kopyası ve tr/en çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `19.24.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula, K kaydına "plandan sapma" diye yaz ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md` (sıradaki boş K numarası başlıkta)
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\findings\04-frontend-e2e.md` içindeki **`FE-10`** tam metni · ilgili bulgular: `FE-53` (sıradaki; performans ölçümü), `FE-09`, Faz 15–17 `lazyPresets.ts` deseni, `TST-04` (19.22: E2E yeşil kalmalı) · kanıt: `evidence\commands\TST-npm-run-check.txt` (paket boyutları)
4. Faz 18'in kaydı: backend `docs\rehber\fazlar\FAZ-18.md` (özellikle "gördüm, dokunmadım" tabloları ve kapanış özeti; bu bulguya değinen satırlar) · `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`
5. `davetkart-docs\phases\faz-19\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-19.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Frontend: `src/components/templates/TemplateRenderer.tsx` (dokuz barrel içe aktarımı) · `lazyPresets.ts` (doğru desen) · `src/components/preview/DeviceSimulator.tsx` ve `HomePage` → `PreviewSection` · `src/pages/InvitePage.tsx` · `src/data.ts` (4188 satır: katalog + kapak içe aktarımları) · `DeferredSection` · `vite.config.ts` (`manualChunks` var mı) · `verify:render` (şablonları nasıl çiziyor; tembelleşince değişmesi gerekebilir).
2. Build çıktısı: `npm run build` sonrası `dist/assets` boyutları (başlangıç ölçümünü kaydet).

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
git branch --merged faz-19-audit-fixes | Select-String "fe-04-share-preview"   # boşsa DUR: FE-04 birleşmemiş
git switch -c fix/<YYYY-MM-DD>-fe-10-bundle-split

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-20-faz-19-audit-fixes                             # yoksa DUR
```

## 3. Bulgu (özet; tam metin bulgu dosyasında)

Misafir tek bir davetiyeyi görmek için ana paketi (1 637 kB, gzip 442 kB) ve tek stil dosyasını (1 171 kB) indiriyor; paketin içinde tembel olmayan 299 şablonun hepsi var. Faz 15–17'nin 74 şablonu doğru desenle (tembel) eklendi; eski 299'u barrel dosyaları üzerinden statik. Ürünün en çok açılan sayfası en ağır sayfası.

**Dersin özü:** kod bölme **içe aktarım grafiğini** izler. `React.lazy` ile ayrılmış bir sayfa, statik yüklenen başka bir sayfanın da içe aktardığı bir modüle bağlıysa o modül ana pakete düşer; tembellik kâğıt üstünde kalır. Ölçmeden optimize etme; ölçtüğünü de bir bütçeyle kilitle.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | `TemplateRenderer`: şablon kimliği → `lazy(() => import(...))` haritası (`lazyPresets.ts` deseni); barrel içe aktarımları kalkar. Harita elle değil, mümkünse mevcut kayıttan türetilir (yeni şablon eklenince unutulmasın). Misafir yalnızca kendi şablonunu indirir. |
| D2 | Ana sayfadaki `DeviceSimulator` önizlemesi `DeferredSection` içinde tembel. |
| D3 | `data.ts` ikiye bölünür: katalog verisi (metin; küçük) ve kapak görseli içe aktarımları (yalnızca kataloğu çizen sayfalar). Mevcut içe aktaranlar güncellenir. |
| D4 | Paket bütçesi: `verify:bundle` (ya da build sonrası betik) §A-1; `npm run check` zincirinde. CSS'in bölünmesi bu bulguda **yok** (ikinci adım; raporda öner). |
| D5 | Tembelleşen şablon için yükleme sırasında iskelet (CLS olmasın) ve 19.21'in hata sınırı. |

## 5. Adımlar ve dosya sahipliği

### Frontend (`fix/<YYYY-MM-DD>-fe-10-bundle-split`) — 🔴 `git add -A` yasak
| Adım | İş |
|---|---|
| 19.24.1 | D1 + D5: `TemplateRenderer` + harita + kılavuzlar. |
| 19.24.2 | D2: ana sayfa önizlemesi. |
| 19.24.3 | D3: `data.ts` bölünmesi + içe aktaranlar. |
| 19.24.4 | D4: bütçe betiği + `package.json` + kılavuz; `npm run check` + `npm run e2e`. |

### Docs
| Adım | İş |
|---|---|
| 19.24.5 | §7'deki ortak kayıtlar (faz bölümü `phases/faz-19/FAZ-19-FE-10-KAYIT.md`): önce/sonra boyut tablosu. |

## 6. Testler ve kalite kapısı

- Önce/sonra tablo: ana giriş ham/gzip, misafir sayfasının indirdiği toplam (Playwright ağ kaydı ya da build manifest'i).
- `verify:bundle` yeşil. **Mutant:** `TemplateRenderer`'a bir barrel'ın statik içe aktarımını geri ekle → kırmızı.
- `verify:render` (373 şablon hâlâ çiziliyor) ve `npm run e2e` (19.22) yeşil.
- `npm run check`.

## 7. Kayıt (dokümantasyon)

**Faz kaydı:** bu bulgu backend'e dokunmuyor. `## 19.24 — FE-10` bölümünü backend `FAZ-19.md`'ye **yazma** (backend dalı açılmadı); aynı içeriği docs deposundaki `phases/faz-19/FAZ-19-FE-10-KAYIT.md` dosyasına yaz. Bir sonraki backend'e dokunan bulgu bu bölümü `FAZ-19.md`'ye taşır (raporunda hatırlat).
- Frontend'de değişen her dosyanın `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).

**Docs deposu (`docs/2026-11-20-faz-19-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı/daralttığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". Değişen eski kararların durum sütununa "→ K…" notu (eski satırı silme).
- `phases/faz-19/README.md`: `FE-10` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-19/FAZ-19-FE-10-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**. Geçmiş faz kayıtlarının metnini yeniden yazma; yalnızca tarihli bir **durum notu** eklemek ("→ Faz 19.x") ve taşıma yüzünden kırılan bağlantıyı düzeltmek serbest.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor). Bulgu zaten kapanmışsa kanıtını göster, kod yazma, yalnızca kayıt adımlarını yap.
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi, hukuki metin ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.


**Kapsam dışı (dokunma, raporda an):** CSS bölme, three.js parçası, görsel optimizasyonu (`FE-09`), performans ölçümü (`FE-53`).

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` (silinecek dosya varsa `git rm <yol>`, taşınacak dosya varsa `git mv <eski> <yeni>`) → `git commit -m "19.24.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Bloğun başında "Başlamadan" kısmı: her depoda `git status --short --untracked-files=all` ve **beklenen satırların tam listesi** (Faz 18'deki gibi), ki fazladan dosya varsa commit'ten önce göreyim.
- Sıra: backend blokları → frontend blokları → docs bloğu → birleştirme.
- **Birleştirme bloğu:** dokunduğun her kod deposu için ayrı ayrı: `git switch faz-19-audit-fixes` → `git merge --no-ff fix/<YYYY-MM-DD>-fe-10-bundle-split -m "Merge FE-10 fix into faz-19-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-19\FAZ-19-FE-10-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (19.24.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle; §A'nın hangi satırı cevaplıydı, hangisinde varsayılan uygulandı.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili test/denetimin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, Shopier, deneme) varsa numaralı liste.
