# PROMPT — FAZ 18.4: `SEC-02` Kullanılıp silinen davetiyenin hakkı iade edilebiliyor; yönetici göremiyor

> **Hazırlanma:** 16 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §4) · **Sıra:** 4/6
> **Önkoşul:** 18.3 (`SEC-01`) düzeltme dalı backend'de (frontend'e dokunduysa orada da) `faz-18-audit-fixes`'e birleşmiş olmalı.
> **Dokunulan depolar:** backend · frontend (gerekirse) · docs
> **Kullanım:** `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır. §A varsa önce onu sen yap.


---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 18: denetim düzeltmeleri** yapıyoruz. 12–15 Kasım 2026 genel sistem denetimi (`AUD-2026-11-12`) altı yüksek (🟠) bulgu çıkardı; her biri ayrı bir dalda, ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `SEC-02`** bulgusunu kapatır: *Kullanılıp silinen davetiyenin hakkı iade edilebiliyor; yönetici göremiyor*. Bu, altı bulgunun 4. sırası.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (18.4.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `restore`, `checkout -- <dosya>`. İzinli olanlar: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `SEC-02` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler. En sonda tam `composer check`. Frontend'e dokunduysan en sonda `npm run check`.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `18.4.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md`
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\REPORT.md` §1 ve §4'teki **`SEC-02`** tam metni · `davetkart-docs\audits\2026-11-12-full-system-audit\findings\02-security.md` · ilgili bulgular: `SEC-01` (aynı fazda kapandı, sipariş alanları değişmiş olabilir) · kanıt: `evidence\commands\SEC-api-probe.txt` P47, P49 · `evidence\mutation\` M30–M32
4. `davetkart-docs\phases\faz-18\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-18.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Backend: `app/Services/Refund/RefundEligibility.php` ve `RefundBlocker` enum'u · iade talebi oluşturma ve **onaylama** akışı (Action'lar, komutlar) · `app/Console/Commands/ListRefundRequests.php` · `app/Actions/Invitation/DeleteInvitationAction.php` (K82 üç günlük serbest bırakma) · `PublishInvitationAction` · `Order` modeli, `consumed_at` damgası (K137) ve onu basan iş · ilgili göçler ve testler · `docs/rehber/fazlar/FAZ-14.md` (K137, K139) · K82'nin kaydı.
2. Frontend: Hesap → Planlarım (iade düğmesinin görünürlüğü ve engel metinleri) · iade engeli çevirileri · `src/contracts/errorCodes*`.

**Sıradaki boş K numarası:** `DECISION-INDEX.md` "K128" diyor ama `ARC-01`'e göre K128–K145 backend `docs/rehber/fazlar/FAZ-13.md` ve `FAZ-14.md`'de kullanılmış. Gerçek son numarayı bu kaynaklardan ve `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`'den (varsa) bul. Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (rapordaki satırlar hâlâ geçerli mi), §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-18-audit-fixes                        # yoksa DUR (18.1 / OPS-01 yapılmamış)
git branch --merged faz-18-audit-fixes | Select-String "sec-01-"   # boşsa DUR: SEC-01 birleşmemiş
git switch -c fix/<YYYY-MM-DD>-sec-02-refund-after-publish

cd D:\Projects\davetkart\davetkart-frontent
git fetch origin
git status --short                                   # yalnızca '?? .claude/' olabilir; başka satır varsa DUR
git switch faz-18-audit-fixes                        # yoksa DUR
git log --oneline -5                                 # önceki bulgular frontend'e dokunduysa birleştirmeleri burada görünür
git switch -c fix/<YYYY-MM-DD>-sec-02-refund-after-publish

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-16-faz-18-audit-fixes                             # yoksa DUR
```

## 3. Bulgu (özet)

Kullanıcı Standart alır, yayınlar, misafirler LCV bırakır; üç günlük pencere (K82) açıkken davetiyeyi siler. Sipariş serbest kalır (`invitation_id = NULL`, `consumed_at = NULL`). İade uygunluğu yalnızca "bağlı mı, yanmış mı" diye bakar; ikisi de değil → talep 201. Yönetici `refunds:list`'te bu hakkın bir davetiyeyi yayınladığını gösteren hiçbir şey görmez ve onaylar. Sonda (P47, P49) kanıtlandı.

**Dersin özü:** iki kural ayrı ayrı doğru (K82: yanlış yayını geri alabilme; K139: kullanılmamış hak iade edilebilir), hata **birleşim yerinde**: birincisi "kullanıldı" bilgisini siliyor, ikincisi o bilgiye güveniyor. Bir durumu **bir bağın yokluğundan türetmek** kırılgandır; olay bir **damga** ile kaydedilir ve damga geri alınmaz (K137'nin dersi).

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | **Damga:** `orders.first_published_at` (`timestampTz`, nullable). `PublishInvitationAction` siparişi yayın için kullandığında, aynı transaction'da ve yalnızca boşsa basar. Serbest bırakma (K82), davetiye silme ya da başka hiçbir yol onu **silmez**. Toplu atamaya kapalı; yalnızca Action basar. |
| D2 | **Uygunluk:** `RefundEligibility`'de `first_published_at !== null` → engel. Mevcut `RefundBlocker::InUse` ve kullanıcıya görünen metni bu durumu doğru anlatıyorsa onu kullan; anlatmıyorsa yeni bir engel (ör. `Used`) + hata sözleşmesi + çeviri. Seçimini K'ya yaz. |
| D3 | **Onay anında yeniden sına (TOCTOU):** iade talebi açıkken yayın mümkünse, onay komutu/Action'ı uygunluğu **onay anında** yeniden değerlendirir; uygun değilse onaylamaz ve sebebini yazar. Bugün yeniden sınıyorsa dokunma, testle kilitle. |
| D4 | **Yöneticinin görüşü:** `refunds:list`'e "Yayın" sütunu: `first_published_at` ya da "hiç yayınlanmadı". |
| D5 | **Geriye dönük doldurma:** göç, bugün bir davetiyeye bağlı ve o davetiye yayınlanmış (ya da `consumed_at` dolu) siparişlerde damgayı en iyi bilinen zamanla doldurur. Daha önce serbest kalmış siparişler için iz varsa (çöp kutusundaki davetiye vb.) kullan; yoksa sınırlamayı kılavuza yaz. Canlıda müşteri verisi yok. |
| D6 | K82 aynen kalır: kullanıcı üç gün içinde yayını geri alıp hakkı başka davetiyede kullanabilir. Değişen yalnızca **iade**. |

## 5. Adımlar ve dosya sahipliği

### Backend (`fix/<YYYY-MM-DD>-sec-02-refund-after-publish`)
| Adım | İş |
|---|---|
| 18.4.1 | D1 + D5: göç (kolon + doldurma), `Order` modeli (cast, korunan alan) + kılavuzlar. |
| 18.4.2 | D1: `PublishInvitationAction` damgayı basar + kılavuz + testler (ilk yayında basılır; ikinci yayında değişmez; serbest bırakmada silinmez). |
| 18.4.3 | D2 (+ gerekirse hata sözleşmesi): `RefundEligibility` + kılavuz + test. |
| 18.4.4 | D3: onay akışı + test. |
| 18.4.5 | D4: `refunds:list` + kılavuz + test (çıktıda sütun). |
| 18.4.6 | `FAZ-18.md` `## 18.4 — SEC-02`. |

### Frontend (yalnızca D2'de yeni engel çıktıysa; 🔴 `git add -A` yasak)
| Adım | İş |
|---|---|
| 18.4.7 | Sözleşme kopyası, çeviri, Planlarım'daki engel metni; `npm run check`. |

### Docs
| Adım | İş |
|---|---|
| 18.4.8 | §7'deki ortak kayıtlar. K82 ve K139'un satırına "SEC-02 ile daraltıldı → K…" notu (silme). |

## 6. Testler ve kalite kapısı

- `a_right_that_published_an_invitation_cannot_be_refunded_after_release`: öde → yayınla → sil → iade talebi 409 (D2'deki kodla). **Mutant:** yeni koşulu `RefundEligibility`'den çıkar → kırmızı.
- `releasing_a_right_keeps_its_first_published_at`. **Mutant:** serbest bırakmada damgayı sıfırla → kırmızı.
- `an_unpublished_right_is_still_refundable` (regresyon: K139 bozulmadı).
- D3 testi: talep açıkken yayın (mümkünse) → onay reddedilir.
- `refunds:list` çıktısında "Yayın" sütunu.
- Sonda tam `composer check`; frontend'e dokunduysan `npm run check`.

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-18.md`: yoksa oluştur (başlık: "Faz 18 — denetim düzeltmeleri (`AUD-2026-11-12`)", altı bulgunun tablosu). `## 18.4 — SEC-02` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar, eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım doğrulama adımları. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).

**Docs deposu (`davetkart-docs`, dal `docs/2026-11-16-faz-18-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". K128–K145 boşluğuna dokunma (`ARC-01` ayrı bir iş); tablonun üstüne ⚠️ notu yoksa ekle.
- `phases/faz-18/README.md`: `SEC-02` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-18/FAZ-18-SEC-02-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**; geçmiş rapordur.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor).
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.
- İade talebi açıkken yayın yapılabiliyor ve onay akışı yeniden sınamıyor, ama düzeltmesi iade sürecinin durum makinesini değiştirmeyi gerektiriyor: önerini yaz, sor.


**Kapsam dışı:** iade sürecinin genel tasarımı, Shopier iade API'si.

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` → `git commit -m "18.4.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Sıra: backend blokları → frontend blokları → docs bloğu.
- En sona **birleştirme bloğu**: backend için (frontend'e dokunduysan onun için de): `git switch faz-18-audit-fixes` → `git merge --no-ff <fix-dalı> -m "Merge SEC-02 fix into faz-18-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-18\FAZ-18-SEC-02-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (18.4.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili testin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, deneme) varsa numaralı liste.
