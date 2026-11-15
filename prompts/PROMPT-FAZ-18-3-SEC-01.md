# PROMPT — FAZ 18.3: `SEC-01` "İlk yayın" indirimi aynı anda açılan her siparişe uygulanıyor

> **Hazırlanma:** 16 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §4) · **Sıra:** 3/6
> **Önkoşul:** 18.2 (`OPS-02`) düzeltme dalı backend'de `faz-18-audit-fixes`'e birleşmiş olmalı.
> **Dokunulan depolar:** backend · frontend (gerekirse) · docs
> **Kullanım:** `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır. §A varsa önce onu sen yap.


---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 18: denetim düzeltmeleri** yapıyoruz. 12–15 Kasım 2026 genel sistem denetimi (`AUD-2026-11-12`) altı yüksek (🟠) bulgu çıkardı; her biri ayrı bir dalda, ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `SEC-01`** bulgusunu kapatır: *"İlk yayın" indirimi aynı anda açılan her siparişe uygulanıyor*. Bu, altı bulgunun 3. sırası.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (18.3.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `restore`, `checkout -- <dosya>`. İzinli olanlar: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `SEC-01` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler. En sonda tam `composer check`. Frontend'e dokunduysan en sonda `npm run check`.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `18.3.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md`
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\REPORT.md` §1 ve §4'teki **`SEC-01`** tam metni · `davetkart-docs\audits\2026-11-12-full-system-audit\findings\02-security.md` · ilgili bulgular: `ARC-09` (`01-architecture.md`, checkout idempotent değil), `TST-02` (`03-testing.md`, kilitler testsiz) · kanıt: `evidence\commands\SEC-api-probe.txt` P12, P13, P13b · `evidence\mutation\` M06, M12, M13, M36
4. `davetkart-docs\phases\faz-18\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-18.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Backend: `app/Actions/Pricing/QuotePriceAction.php` · `app/Actions/Payment/StartCheckoutAction.php` · `app/Actions/Payment/HandlePaymentCallbackAction.php` (özellikle geç gelen ödeme ve süresi dolmuş sipariş davranışı, K102) · hediye kodu kullanımı (K111: satır kilidi + kullanım kaydı aynı transaction'da; **örnek alacağın desen**) · `Order` modeli, durum ve promosyon enum'ları, `orders` göçleri · `orders:expire` komutu · fiyat ve checkout testleri · `docs/rehber/fazlar/FAZ-13.md` (K130, K131).
2. Frontend: ödeme sayfası, `src/services/payments.ts`, fiyat önizlemesi; `scripts/verify-pricing.ts`.

**Sıradaki boş K numarası:** `DECISION-INDEX.md` "K128" diyor ama `ARC-01`'e göre K128–K145 backend `docs/rehber/fazlar/FAZ-13.md` ve `FAZ-14.md`'de kullanılmış. Gerçek son numarayı bu kaynaklardan ve `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`'den (varsa) bul. Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (rapordaki satırlar hâlâ geçerli mi), §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-18-audit-fixes                        # yoksa DUR (18.1 / OPS-01 yapılmamış)
git branch --merged faz-18-audit-fixes | Select-String "ops-02-"   # boşsa DUR: OPS-02 birleşmemiş
git switch -c fix/<YYYY-MM-DD>-sec-01-first-publish-once

cd D:\Projects\davetkart\davetkart-frontent
git fetch origin
git status --short                                   # yalnızca '?? .claude/' olabilir; başka satır varsa DUR
git switch faz-18-audit-fixes                        # yoksa DUR
git log --oneline -5                                 # önceki bulgular frontend'e dokunduysa birleştirmeleri burada görünür
git switch -c fix/<YYYY-MM-DD>-sec-01-first-publish-once

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-16-faz-18-audit-fixes                             # yoksa DUR
```

## 3. Bulgu (özet)

Kural "`paid_at` damgalı sipariş yoksa ilk yayındır" ve bekleyen siparişleri saymıyor (K131). Yeni kullanıcı iki sekmede (ya da bir davetiye + bir paket) checkout açarsa iki sipariş de %60 indirimli olur (249,00 → 99,60 TL); ödeme bildirimi indirimin hâlâ geçerli olup olmadığına bakmaz. Sınır yok: on sekme, on indirimli hak. Sonda (P13) kanıtlandı.

**Dersin özü:** bu bir **TOCTOU** (kontrol anı ≠ kullanım anı) hatası. Tek kullanımlık bir hak ya **ayrılır** (reserve) ya da kullanım anında yeniden doğrulanır. Hediye kodunda doğru yapılmış (K111); ilk yayın indiriminde aynı desen yok. Doğru çözüm katmanlıdır: uygulama kilidi + veritabanı değişmezi + son kapıda yeniden sınama.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | **Değişmez:** bir kullanıcının aynı anda en fazla **bir** `pending` + `first_publish` siparişi olur. Üç katman: (1) `StartCheckoutAction` transaction'ında kullanıcı satırı `lockForUpdate()`; (2) PostgreSQL **kısmi UNIQUE index** `(user_id) WHERE status = 'pending' AND promotion = 'first_publish'` (kolon ve enum değerlerini koddan al); (3) `HandlePaymentCallbackAction`'da `paid`'e geçerken kullanıcının başka `paid` `first_publish` siparişi varsa geçişi **yine yap** (para alındı, geri çevrilemez) ama `Log::critical` + mevcut yönetici bildirim mekanizması (yoksa yalnızca `Log::critical`, raporda an). |
| D2 | **Uygunluk tek yerde:** "bu kullanıcı şu an ilk yayın indirimine uygun mu" sorusunun cevabı tek bir sınıfta/metotta (ör. `FirstPublishEligibility`) ve hem `QuotePriceAction` hem `StartCheckoutAction` onu kullanır. Gösterilen fiyat = tahsil edilen fiyat (K128'in ruhu). Kural: `paid` `first_publish` yok **ve** başka bir hedef için açık indirimli sipariş yok. |
| D3 | **Aynı niyet tekrarlanırsa (ARC-09'un SEC-01'e gereken kısmı):** aynı kullanıcı + aynı hedef (davetiye ya da paket) + aynı plan + aynı hediye kodu için süresi dolmamış `pending` sipariş varsa **onu döndür** (yeni satır açma). Aksi hâlde düzeltme, sayfayı yenileyen kullanıcıyı cezalandırır. |
| D4 | **Aynı hedefte farklı plan / farklı kod:** önce geç gelen ödemenin süresi dolmuş/iptal siparişte ne yaptığını oku. Eski bekleyen siparişi kapatmak güvenliyse (geç ödeme yine de doğru tutarla hakka dönüşüyor ve kayıt düşüyor) eskisini kapat, yenisi indirimi alsın. Güvenli değilse yeni sipariş indirimsiz açılsın. Seçimini ve gerekçesini K'ya yaz. |
| D5 | **Göç veri değiştirmez:** index oluşturulmadan önce çakışan satır varsa göç anlaşılır bir mesajla durur; çözüm sorgusu kılavuzda yazar. (Canlıda müşteri verisi yok; yerel veritabanında deneme siparişlerin olabilir.) |
| D6 | API yanıt biçimi değişmez. Önizlemede indirimin neden düştüğünü anlatan yeni bir alan **eklenmez**; bu bir UX sorusu olarak raporda kalır. |

## 5. Adımlar ve dosya sahipliği

### Backend (`fix/<YYYY-MM-DD>-sec-01-first-publish-once`)
| Adım | İş |
|---|---|
| 18.3.1 | D5: kısmi UNIQUE index göçü + kılavuzu + index'i doğrudan iki satır ekleyerek sınayan test (`QueryException`). |
| 18.3.2 | D2: uygunluk sınıfı + `QuotePriceAction` onu kullanır + kılavuzlar + testler. |
| 18.3.3 | D1(1), D3, D4: `StartCheckoutAction` (kilit, yeniden kullanma, indirim kararı) + kılavuz + testler. |
| 18.3.4 | D1(3): `HandlePaymentCallbackAction` son kapı denetimi + kılavuz + test (`Log::spy` ile `critical`). |
| 18.3.5 | `FAZ-18.md` `## 18.3 — SEC-01`. |

### Frontend (yalnızca gerekirse; 🔴 `git add -A` yasak)
| Adım | İş |
|---|---|
| 18.3.6 | Yanıt biçimi değişmediyse frontend'e dokunma ve `verify:pricing`'i koşup sonucunu yaz. Değiştiyse tipler + `verify:pricing` + çeviri. |

### Docs
| Adım | İş |
|---|---|
| 18.3.7 | §7'deki ortak kayıtlar. K131'in durumunu "daraltıldı → K…" diye işaretle (silme). |

## 6. Testler ve kalite kapısı

- `the_first_publish_discount_is_granted_to_one_order_only`: aynı kullanıcı iki farklı hedef için checkout açar; ikincinin `promotion`'ı `null`, tutarı liste fiyatı. **Mutant:** "açık indirimli sipariş var mı" sorgusunu kaldır → kırmızı.
- `a_second_checkout_for_the_same_target_reuses_the_pending_order`: iki istek, tek satır. **Mutant:** yeniden kullanma sorgusunu kaldır → kırmızı.
- `the_quote_and_the_checkout_agree_on_the_first_publish_discount`: açık indirimli sipariş varken başka hedefin önizlemesi de indirimsiz.
- D4 testi (seçtiğin kola göre).
- `a_second_paid_first_publish_order_is_logged_as_critical`.
- **Kilit (`TST-02` deseni):** checkout sırasında yürüyen SQL'de kullanıcı satırı için `for update` geçtiğini `DB::listen` ile doğrula. **Mutant:** `lockForUpdate()`'i kaldır → bu test kırmızı. (Gerçek iki bağlantılı yarış testi `TST-02`'nin işi; kapsam dışı.)
- Sonda tam `composer check`; frontend'e dokunduysan `npm run check`, dokunmadıysan `npm run verify:pricing`.

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-18.md`: yoksa oluştur (başlık: "Faz 18 — denetim düzeltmeleri (`AUD-2026-11-12`)", altı bulgunun tablosu). `## 18.3 — SEC-01` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar, eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım doğrulama adımları. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).

**Docs deposu (`davetkart-docs`, dal `docs/2026-11-16-faz-18-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". K128–K145 boşluğuna dokunma (`ARC-01` ayrı bir iş); tablonun üstüne ⚠️ notu yoksa ekle.
- `phases/faz-18/README.md`: `SEC-01` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-18/FAZ-18-SEC-01-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**; geçmiş rapordur.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor).
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.
- Geç gelen ödemenin davranışı koddan net okunamıyor ve D4'ün iki kolu da para riski taşıyor.
- Promosyon bilgisi `orders` tablosunda ayrı bir kolonda değil (kısmi index kurulamıyor): şema önerini yaz, sor.


**Kapsam dışı:** `ARC-09`'un D3 dışındaki kısmı (`Idempotency-Key`), `TST-02`'nin yarış testleri, hediye kodu yarışı.

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` → `git commit -m "18.3.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Sıra: backend blokları → frontend blokları → docs bloğu.
- En sona **birleştirme bloğu**: backend için (frontend'e dokunduysan onun için de): `git switch faz-18-audit-fixes` → `git merge --no-ff <fix-dalı> -m "Merge SEC-01 fix into faz-18-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-18\FAZ-18-SEC-01-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (18.3.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili testin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, deneme) varsa numaralı liste.
