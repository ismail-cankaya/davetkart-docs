# PROMPT — FAZ 18.5: `SEC-03` Shopier `callback` kipinde `status` ve tutar imzasız

> **Hazırlanma:** 16 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §4) · **Sıra:** 5/6
> **Önkoşul:** 18.4 (`SEC-02`) düzeltme dalı backend'de (frontend'e dokunduysa orada da) `faz-18-audit-fixes`'e birleşmiş olmalı.
> **Dokunulan depolar:** backend · docs
> **Kullanım:** `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır. §A varsa önce onu sen yap.


---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 18: denetim düzeltmeleri** yapıyoruz. 12–15 Kasım 2026 genel sistem denetimi (`AUD-2026-11-12`) altı yüksek (🟠) bulgu çıkardı; her biri ayrı bir dalda, ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `SEC-03`** bulgusunu kapatır: *Shopier `callback` kipinde `status` ve tutar imzasız*. Bu, altı bulgunun 5. sırası.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (18.5.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `restore`, `checkout -- <dosya>`. İzinli olanlar: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `SEC-03` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler. En sonda tam `composer check`. Frontend'e dokunduysan en sonda `npm run check`.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `18.5.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md`
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\REPORT.md` §1 ve §4'teki **`SEC-03`** tam metni · `davetkart-docs\audits\2026-11-12-full-system-audit\findings\02-security.md` · ilgili bulgular: `SEC-07` (üretilen URL'ler; `url(CALLBACK_PATH)`) · kanıt: kod okuması (Shopier'e istek atılmadı)
4. `davetkart-docs\phases\faz-18\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-18.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Backend: `app/Services/Payment/ShopierGateway.php` · `app/Services/Payment/Shopier/ShopierSignature.php` · `config/payment.php` · onay kipi enum'u · `HandlePaymentCallbackAction` (`amountMatches()`) · `AppServiceProvider::resolvePaymentGateway` · `PaymentProviderException::unavailable` (K123: sır eksikse fail-closed) · callback ve OSB denetleyicileri, rotaları · Shopier testleri · `docs/10-URETIM-ENV-SABLONU.md` · `docs/rehber/fazlar/FAZ-12.md` (K94 ⚠️ geçici, K117, K127).
2. Docs: `phases/faz-12/FAZ-12-RAPOR.md` (§A cevapları: OSB API ödemelerinde geliyor mu, başarısız ödemede callback geliyor mu) · `operations/deployment/YAYIN-DEVIR.md` ve `YAYIN-PLANI.md` (sunucuda hangi `SHOPIER_CONFIRMATION` değerinin planlandığı).

**Sıradaki boş K numarası:** `DECISION-INDEX.md` "K128" diyor ama `ARC-01`'e göre K128–K145 backend `docs/rehber/fazlar/FAZ-13.md` ve `FAZ-14.md`'de kullanılmış. Gerçek son numarayı bu kaynaklardan ve `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`'den (varsa) bul. Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (rapordaki satırlar hâlâ geçerli mi), §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-18-audit-fixes                        # yoksa DUR (18.1 / OPS-01 yapılmamış)
git branch --merged faz-18-audit-fixes | Select-String "sec-02-"   # boşsa DUR: SEC-02 birleşmemiş
git switch -c fix/<YYYY-MM-DD>-sec-03-shopier-callback-mode

# Frontend: bu bulguda değişmez. §1'deki okuma için `git show faz-18-audit-fixes:<yol>` kullan; dal açma.

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-16-faz-18-audit-fixes                             # yoksa DUR
```

## 3. Bulgu (özet)

`SHOPIER_CONFIRMATION=callback` seçilirse siparişi `paid` yapan şey tarayıcının getirdiği formdur. İmza yalnızca `random_nr + platform_order_id`'yi kapsar; `status` ve tutar imzanın dışında. Kullanıcı başarısız ödemenin formunda `status=failed`'ı `success` yaparsa imza yine geçerli; bu kipte bildirim tutar taşımadığı için `amountMatches()` `true` döner. Varsayılan kip `osb` ve orada callback siparişi değiştirmiyor (K117); risk, kipin tek bir `.env` satırı olması ve `docs/10`'un onu geçerli bir seçenek diye anlatması. (Shopier'in başarısız ödemede imzalı callback üretip üretmediği **varsayım**, doğrulanmadı.)

**Dersin özü:** bir imza yalnızca **kapsadığı** alanları korur; karar veren alan imzanın dışındaysa imza kararı korumaz. Tarayıcıdan gelen her şey kullanıcının elindedir; para kararı sunucudan sunucuya giden kanalda (OSB) verilir. Güvensiz olduğu bilinen seçeneği "kapatılabilir" bırakmak yerine **üretimde imkânsız kılmak** fail-safe tasarımdır.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | **Üretimde ret:** `App::isProduction()` ve onay kipi `callback` ise ağ geçidi kurulamaz: sır eksikliğiyle **aynı** davranış (K123: `PaymentProviderException::unavailable` → checkout 503, mevcut hata kodu). Kurulumda bir kez `Log::critical` (yanlış yapılandırma görünür olsun). Callback ucu bu durumda hiçbir siparişi değiştirmez ve kullanıcıyı mevcut başarısızlık/bekleme sayfasına güvenli biçimde yönlendirir (500 ve iç ayrıntı sızmaz). |
| D2 | **Neden şimdi tamamen kaldırmıyoruz:** Faz 12 §A'nın OSB cevapları (API ile başlatılan ödemelerde OSB geliyor mu) raporda doğrulanmış değilse `callback` yerelde tek deneme yolu olabilir. Faz 12 raporunu oku: OSB doğrulanmışsa **kaldırma** önerisini K olarak yaz ve raporda sor; kendin kaldırma. |
| D3 | **`amountMatches()` fail-closed:** bildirimde tutar yoksa **üretimde** eşleşme sayılmaz. Bu değişiklik yerel/test akışını bozmamalı. Kodu okuyunca gereksiz ya da riskli bulursan uygulama, nedenini rapora yaz. |
| D4 | `docs/10-URETIM-ENV-SABLONU.md`: `callback` "yalnızca yerel/test; üretimde reddedilir (K…)" olarak işaretlenir. |

## 5. Adımlar ve dosya sahipliği

### Backend (`fix/<YYYY-MM-DD>-sec-03-shopier-callback-mode`)
| Adım | İş |
|---|---|
| 18.5.1 | D1: `ShopierGateway` (ve gerekiyorsa `resolvePaymentGateway`) + kılavuz + testler. |
| 18.5.2 | D1: callback ucunun bu durumdaki güvenli yanıtı (denetleyici/Action) + test. Ayrı dosya gerekmiyorsa bu adımı atla ve raporda söyle. |
| 18.5.3 | D3 (uygularsan): `HandlePaymentCallbackAction` + kılavuz + test. |
| 18.5.4 | D4: `docs/10-URETIM-ENV-SABLONU.md` + `FAZ-18.md` `## 18.5 — SEC-03`. |

### Docs
| Adım | İş |
|---|---|
| 18.5.5 | §7'deki ortak kayıtlar; K94/K117 satırlarına "SEC-03 ile üretimde callback reddedilir → K…" notu. |

## 6. Testler ve kalite kapısı

- `the_callback_confirmation_mode_is_refused_in_production`: üretim ortamı + `callback` → checkout 503 ve doğru hata kodu; sipariş açılmaz ya da `pending` kalır (mevcut sır eksikliği testinin deseni). **Mutant:** ortam kontrolünü kaldır → kırmızı.
- `the_callback_mode_still_works_outside_production` (regresyon).
- `osb_mode_works_in_production` (regresyon).
- Üretim + `callback` + sahte imzalı `status=success` callback → sipariş `paid` olmaz.
- D3 uygulandıysa: üretimde tutarsız bildirim → `paid` olmaz. **Mutant:** yeni koşulu kaldır → kırmızı.
- Testler sahte sır ve kendi hesapladığın imzayla; gerçek Shopier'e istek yok. Sonda tam `composer check`.

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-18.md`: yoksa oluştur (başlık: "Faz 18 — denetim düzeltmeleri (`AUD-2026-11-12`)", altı bulgunun tablosu). `## 18.5 — SEC-03` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar, eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım doğrulama adımları. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).

**Docs deposu (`davetkart-docs`, dal `docs/2026-11-16-faz-18-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". K128–K145 boşluğuna dokunma (`ARC-01` ayrı bir iş); tablonun üstüne ⚠️ notu yoksa ekle.
- `phases/faz-18/README.md`: `SEC-03` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-18/FAZ-18-SEC-03-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**; geçmiş rapordur.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor).
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.
- Yayın kaydına göre sunucu `SHOPIER_CONFIRMATION=callback` ile yapılandırılmış ya da öyle planlanmış: bu değişiklik yayına çıkınca ödemeler durur. Sor.


**Kapsam dışı:** `SEC-07` (callback adresini `config('app.url')`'den üretmek dahil), K94'ün canlı doğrulaması.

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` → `git commit -m "18.5.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Sıra: backend blokları → frontend blokları → docs bloğu.
- En sona **birleştirme bloğu**: yalnızca backend için: `git switch faz-18-audit-fixes` → `git merge --no-ff <fix-dalı> -m "Merge SEC-03 fix into faz-18-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-18\FAZ-18-SEC-03-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (18.5.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili testin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, deneme) varsa numaralı liste.
