# PROMPT — FAZ 19.9: `SEC-05` Zayıf parolalar kabul ediliyor

> **Hazırlanma:** 20 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §5.1 · tam metin [`findings/02-security.md`](../audits/2026-11-12-full-system-audit/findings/02-security.md)) · **Sıra:** 9/28 · **Efor:** S
> **Önkoşul:** 19.8 (`OPS-05`) docs dalı `docs/2026-11-20-faz-19-audit-fixes`'e birleşmiş olmalı (§2 denetler).
> **Dokunulan depolar:** backend · frontend · docs
> **Kullanım:** önce §A'yı sen doldur/yap; sonra `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır.

## §A — Senin kararın (prompt'u yapıştırmadan önce doldur)

| # | Soru | Boş bırakırsan ajanın uygulayacağı varsayılan | Cevabın |
|---|---|---|---|
| 1 | En az uzunluk? | 12 (ASVS 2.1.1) | |
| 2 | Sızıntı denetimi: Laravel `Password::uncompromised()` (Have I Been Pwned'a k-anonimlikle istek; parola gitmez, SHA-1'in ilk 5 karakteri gider) mi, yoksa depoda en yaygın 10.000 parolalık liste mi? | Depoda liste (dış istek yok, KVKK ve kullanılabilirlik riski yok); kaynağı ve lisansı kılavuzda | |
| 3 | Mevcut hesaplar: zayıf parolası olanlar zorla değiştirilsin mi? | Hayır; kural yalnızca yeni parola belirlenirken | |

**Boş satır için ajan varsayılanı uygular ve bunu K kaydında "varsayılan (İsmail cevaplamadı)" diye işaretler.**

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 19: denetimin orta öncelikli bulguları** üzerinde çalışıyoruz. `AUD-2026-11-12` 29 orta (🟡) bulgu çıkardı; `TST-01` Faz 18'de kapandı, kalan 28'i Faz 19'da her biri ayrı bir dalda ve ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `SEC-05`** bulgusunu kapatır: *Zayıf parolalar kabul ediliyor*. Bu, 28 bulgunun 9. sırası. Yukarıdaki §A tablosu benim kararlarım.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (19.9.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `rm`, `mv`, `restore`, `checkout -- <dosya>`. İzinli: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `SEC-05` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz. Faz 19'da sırası gelecek bulgular için bkz. `davetkart-docs\phases\faz-19\README.md`.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler; en sonda tam `composer check` **ve** `composer audit`. Frontend'e dokunduysan en sonda `npm ci` + `npm run check`. Önceki bulguların eklediği denetimler (ör. `verify:plans`, varsa E2E) yeşil kalmalı.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kendi kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut/tarayıcı). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi, `contracts/*.json` + `--check`). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend sözleşme kopyası ve tr/en çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `19.9.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula, K kaydına "plandan sapma" diye yaz ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md` (sıradaki boş K numarası başlıkta)
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\findings\02-security.md` içindeki **`SEC-05`** tam metni · ilgili bulgular: `SEC-16` (hız sınırı yavaşlatır, durdurmaz) · kanıt: `evidence\commands\SEC-api-probe.txt` P67 (`12345678`, `password`, `aaaaaaaa` → 201)
4. Faz 18'in kaydı: backend `docs\rehber\fazlar\FAZ-18.md` (özellikle "gördüm, dokunmadım" tabloları ve kapanış özeti; bu bulguya değinen satırlar) · `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`
5. `davetkart-docs\phases\faz-19\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-19.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Backend: `app/Http/Requests/Auth/RegisterRequest.php`, `ResetPasswordRequest.php`, `Account/ChangePasswordRequest.php` · doğrulama hata kodlarının sözleşmeye nasıl çevrildiği (`docs/08-HATA-SOZLESMESI.md`, `contracts/error-codes.json`) · ilgili testler.
2. Frontend: kayıt, parola sıfırlama, parola değiştirme formları (istemci tarafı uzunluk ipuçları, `minLength`) · hata çevirileri (`src/locales/*`, `src/contracts/errorCodes*`) · `verify:errors`.

**K numarası:** yeni karar = `DECISION-INDEX.md`'deki "Sıradaki boş numara". Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (denetim 12 Kasım'daydı; Faz 18 bazı satırları değiştirdi, rapordaki satırlar hâlâ geçerli mi), §A'da hangi satırlar dolu, §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
git switch -c fix/<YYYY-MM-DD>-sec-05-password-policy

cd D:\Projects\davetkart\davetkart-frontent
git fetch origin
git status --short                                   # yalnızca '?? .claude/' olabilir; başka satır varsa DUR
git switch faz-19-audit-fixes                        # yoksa DUR (19.1 §A yapılmamış)
git switch -c fix/<YYYY-MM-DD>-sec-05-password-policy

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-20-faz-19-audit-fixes                             # yoksa DUR
git branch --merged docs/2026-11-20-faz-19-audit-fixes | Select-String "ops-05-expiry-calendar"   # boşsa DUR: OPS-05 birleşmemiş
```

## 3. Bulgu (özet; tam metin bulgu dosyasında)

Üç istek sınıfı da `min:8, max:255` kullanıyor; kayıtta `12345678`, `password`, `aaaaaaaa` kabul ediliyor. Kimlik bilgisi doldurma saldırısında en çok denenen parolalar geçerli.

**Dersin özü:** ASVS uzunluk ve "yaygın değil" ister; karmaşıklık kuralı (büyük harf, rakam) **istemez**, çünkü kullanıcıyı `Parola1!` gibi tahmin edilebilir kalıplara iter. Aynı kural üç yerde yazılıyorsa bir gün biri unutulur: kural **tek bir nesnede** durmalı.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | Tek kural kaynağı: `App\Rules\…` ya da `Password::defaults()` (`AppServiceProvider`'da) — üç istek de onu kullanır. Uzunluk §A-1, üst sınır 255 kalır (bcrypt 72 bayt sınırına dikkat: kılavuzda açıkla). |
| D2 | §A-2: liste seçildiyse `resources/` altında sıkıştırılmamış düz metin, yükleme bellekte bir kez (cache), karşılaştırma küçük harfe çevrilmiş tam eşleşme. `uncompromised` seçildiyse zaman aşımı ve servis erişilemezken **açık başarısızlık** (kayıt engellenmez) — kılavuzda neden. |
| D3 | Yeni hata kodu gerekiyorsa (ör. `password_too_common`) sözleşme + tr/en çeviri; gerekmiyorsa mevcut doğrulama kodu ve alan mesajı. |
| D4 | Frontend formları aynı uzunluğu gösterir (ipucu metni + `minLength`); sunucu son sözü söyler. |

## 5. Adımlar ve dosya sahipliği

### Backend (`fix/<YYYY-MM-DD>-sec-05-password-policy`)
| Adım | İş |
|---|---|
| 19.9.1 | D1 + D2: kural nesnesi (+ liste dosyası) + kılavuz + testler. |
| 19.9.2 | D1: üç istek sınıfı + testler (+ D3 sözleşme). |
| 19.9.3 | `FAZ-19.md` `## 19.9 — SEC-05`. |

### Frontend (`fix/<YYYY-MM-DD>-sec-05-password-policy`) — 🔴 `git add -A` yasak
| Adım | İş |
|---|---|
| 19.9.4 | D4 (+ D3 çevirileri, sözleşme kopyası); `npm run check`. |

### Docs
| Adım | İş |
|---|---|
| 19.9.5 | §7'deki ortak kayıtlar. |

## 6. Testler ve kalite kapısı

- `registration_rejects_common_passwords` (veri sağlayıcılı: `12345678`, `password`, `qwerty123456`, `aaaaaaaaaaaa`). **Mutant:** kuralı `min:8`'e geri al → kırmızı.
- Aynı veri sağlayıcı parola sıfırlama ve parola değiştirme için de (üç uç, tek kural: biri unutulursa kırmızı).
- `a_long_uncommon_passphrase_is_accepted` (regresyon).
- Frontend: `npm run check` (`verify:errors` dahil).

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-19.md`: yoksa oluştur (başlık: "Faz 19 — denetimin orta öncelikli bulguları (`AUD-2026-11-12`)", 28 bulgunun tablosu). `## 19.9 — SEC-05` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar (frontend dahil), eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım işler. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).
- Docs deposunda `phases/faz-19/FAZ-19-*-KAYIT.md` dosyaları varsa (backend'e dokunmayan önceki bulguların bölümleri) ve `FAZ-19.md`'de karşılıkları yoksa, onları sıra numarasına göre `FAZ-19.md`'ye taşı; docs'taki dosyayı silme, başına "Taşındı → backend `FAZ-19.md` §19.x" notu ekle.

**Docs deposu (`docs/2026-11-20-faz-19-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı/daralttığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". Değişen eski kararların durum sütununa "→ K…" notu (eski satırı silme).
- `phases/faz-19/README.md`: `SEC-05` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-19/FAZ-19-SEC-05-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**. Geçmiş faz kayıtlarının metnini yeniden yazma; yalnızca tarihli bir **durum notu** eklemek ("→ Faz 19.x") ve taşıma yüzünden kırılan bağlantıyı düzeltmek serbest.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor). Bulgu zaten kapanmışsa kanıtını göster, kod yazma, yalnızca kayıt adımlarını yap.
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor (parola listesi bir **veri dosyası**dır, bağımlılık değil; lisansını kılavuza yaz).
- Bir karar para, müşteri verisi, hukuki metin ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.


**Kapsam dışı (dokunma, raporda an):** `SEC-16` (giriş hız sınırı), iki adımlı doğrulama.

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` (silinecek dosya varsa `git rm <yol>`, taşınacak dosya varsa `git mv <eski> <yeni>`) → `git commit -m "19.9.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Bloğun başında "Başlamadan" kısmı: her depoda `git status --short --untracked-files=all` ve **beklenen satırların tam listesi** (Faz 18'deki gibi), ki fazladan dosya varsa commit'ten önce göreyim.
- Sıra: backend blokları → frontend blokları → docs bloğu → birleştirme.
- **Birleştirme bloğu:** dokunduğun her kod deposu için ayrı ayrı: `git switch faz-19-audit-fixes` → `git merge --no-ff fix/<YYYY-MM-DD>-sec-05-password-policy -m "Merge SEC-05 fix into faz-19-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-19\FAZ-19-SEC-05-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (19.9.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle; §A'nın hangi satırı cevaplıydı, hangisinde varsayılan uygulandı.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili test/denetimin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, Shopier, deneme) varsa numaralı liste.
