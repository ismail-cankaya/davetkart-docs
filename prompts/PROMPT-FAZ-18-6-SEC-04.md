# PROMPT — FAZ 18.6: `SEC-04` Frontend sayfalarında güvenlik başlığı yok; token `localStorage`'da

> **Hazırlanma:** 16 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §4) · **Sıra:** 6/6
> **Önkoşul:** 18.5 (`SEC-03`) düzeltme dalı backend'de `faz-18-audit-fixes`'e birleşmiş olmalı. Bu prompt Faz 18'i de kapatır (§11).
> **Dokunulan depolar:** backend (`deploy/nginx`) · frontend (yalnızca yerel deneme ve gerekirse) · docs
> **Kullanım:** `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır. §A varsa önce onu sen yap.


---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 18: denetim düzeltmeleri** yapıyoruz. 12–15 Kasım 2026 genel sistem denetimi (`AUD-2026-11-12`) altı yüksek (🟠) bulgu çıkardı; her biri ayrı bir dalda, ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `SEC-04`** bulgusunu kapatır: *Frontend sayfalarında güvenlik başlığı yok; token `localStorage`'da*. Bu, altı bulgunun 6. sırası.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (18.6.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `restore`, `checkout -- <dosya>`. İzinli olanlar: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `SEC-04` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler. En sonda tam `composer check`. Frontend'e dokunduysan en sonda `npm run check`.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `18.6.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md`
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\REPORT.md` §1 ve §4'teki **`SEC-04`** tam metni · `davetkart-docs\audits\2026-11-12-full-system-audit\findings\02-security.md` · ilgili bulgular: `SEC-12` (Google yazı tipleri), `SEC-18` · kanıt: Nginx dosyasının okunması; API başlıkları sondada P57
4. `davetkart-docs\phases\faz-18\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-18.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Backend: `deploy/nginx/davetkart.conf` ve `docs/rehber/deploy/nginx/davetkart.md` · `deploy/deploy.sh` / `deploy-frontend.sh` (Nginx yapılandırması sunucuya nasıl kuruluyor, `nginx -t` + reload var mı) · `app/Http/Middleware/SecurityHeaders.php` (K85).
2. Frontend: `index.html` (satır içi betik var mı) · `vite.config.ts` · `src/services/auth.ts` (token saklama) · **dış kaynak envanteri:** `src/` ve `index.html`'de `https?://` geçen her yer (yazı tipleri, medya alan adı, harita karoları, video gömmeleri, Sentry/analitik, Shopier form gönderimi) · `iframe` kullanımı (editör önizlemesi aynı kökenden çerçeve kullanıyorsa `frame-ancestors 'none'` onu kırar) · WebGL/jiroskop/ivmeölçer/konum kullanan şablonlar (`Permissions-Policy`) · `blob:`/`data:` ve Web Worker kullanımı.
3. Docs: `operations/deployment/YAYIN-PLANI.md` (alan adları ve alt alan adları; hepsi HTTPS mi → HSTS `includeSubDomains` kararı; medya alan adı) · `operations/deployment/YAYIN-SIRASI.md`.
4. Denetimin tarayıcı betikleri: `davetkart-docs\audits\2026-11-12-full-system-audit\evidence\scripts\e2e\` (Playwright; yerel denemede yeniden kullanabilirsin).

**Sıradaki boş K numarası:** `DECISION-INDEX.md` "K128" diyor ama `ARC-01`'e göre K128–K145 backend `docs/rehber/fazlar/FAZ-13.md` ve `FAZ-14.md`'de kullanılmış. Gerçek son numarayı bu kaynaklardan ve `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`'den (varsa) bul. Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (rapordaki satırlar hâlâ geçerli mi), §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-18-audit-fixes                        # yoksa DUR (18.1 / OPS-01 yapılmamış)
git branch --merged faz-18-audit-fixes | Select-String "sec-03-"   # boşsa DUR: SEC-03 birleşmemiş
git switch -c fix/<YYYY-MM-DD>-sec-04-security-headers

cd D:\Projects\davetkart\davetkart-frontent
git fetch origin
git status --short                                   # yalnızca '?? .claude/' olabilir; başka satır varsa DUR
git switch faz-18-audit-fixes                        # yoksa DUR
git log --oneline -5                                 # önceki bulgular frontend'e dokunduysa birleştirmeleri burada görünür
git switch -c fix/<YYYY-MM-DD>-sec-04-security-headers

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-16-faz-18-audit-fixes                             # yoksa DUR
```

## 3. Bulgu (özet)

Güvenlik başlıkları Laravel ara katmanında (K85) ve yalnızca `/api/*` yanıtlarında. `index.html`, JS, CSS ve videolar Nginx'ten doğrudan çıkıyor: CSP yok, `X-Frame-Options`/`frame-ancestors` yok, `X-Content-Type-Options` yok, HSTS yok. Oturum token'ı `localStorage`'da. Sonuç: arayüz çerçevelenebiliyor (clickjacking: "hesabı sil"e tıklatma) ve ileride çıkacak tek bir XSS token'ı okuyup dışarı gönderebilir; ikinci bir kilit yok.

**Dersin özü:** **derinlemesine savunma.** `localStorage`'daki token XSS'e karşı korumasızdır; onu orada tutmayı seçtiysen CSP ikinci kilittir. K85 "başlıklar middleware'de" derken API'yi düşündü; SPA'yı sunan katman Nginx olduğu için karar frontend'i kapsamadı. Ve bir Nginx tuzağı: `add_header` üst bloktan **miras alınmaz**, bir `location` kendi `add_header`'ını tanımladığı anda üsttekilerin hepsi düşer.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | **Tek kaynak:** başlıklar `deploy/nginx/snippets/security-headers.conf` (ya da deseninle uyumlu bir ad) dosyasında; `davetkart.com` sunucu bloğuna **ve** kendi `add_header`'ı olan her `location` bloğuna `include` edilir. Hepsi `always`. Snippet'in sunucuya kurulumu dağıtım betiğinin/çalıştırma kitabının parçası olur. |
| D2 | **Hemen zorlanan başlıklar:** `X-Content-Type-Options: nosniff` · `Referrer-Policy: strict-origin-when-cross-origin` · `Strict-Transport-Security: max-age=31536000` (`includeSubDomains` yalnızca plandaki bütün alt alan adları HTTPS ise; `preload` yok) · `X-Frame-Options` + **zorlanan küçük bir CSP**: `frame-ancestors 'self'` (aynı kökenden çerçeve yoksa `'none'`) `; base-uri 'self'; object-src 'none'`. Bu küçük CSP clickjacking'i bugün kapatır ve neredeyse hiçbir şeyi kırmaz. |
| D3 | **Tam CSP önce rapor kipinde:** `Content-Security-Policy-Report-Only` ile envantere dayalı tam politika (`default-src 'self'`; `script-src 'self'`; `style-src 'self' 'unsafe-inline'` + yazı tipi kaynağı; `img-src`/`media-src` medya alan adı + `data:` `blob:`; `connect-src 'self'` + gerçekten gereken uçlar; `form-action 'self' https://www.shopier.com`; …). Rapordaki örnek bir başlangıç, envanter kazanır. Rapor toplayıcı uç **eklenmez** (ihlaller tarayıcı konsolunda görülür; toplayıcı ayrı karar). Zorlamaya geçiş: bir haftalık gözlemden sonra ayrı bir değişiklikle. |
| D4 | `Permissions-Policy`: kullanılmayanlar kapalı (`camera=()`, `microphone=()`, `payment=()` …); şablonların kullandıkları (`gyroscope`, `accelerometer`, gerekirse `geolocation`) `(self)`. Envanterden çıkar. |
| D5 | **Token'ı httpOnly çereze taşımak bu bulgunun kapsamında değil** (Sanctum SPA çerez kimliği + CSRF; büyük iş). Açık karar olarak K'ya ve rapora yaz. |
| D6 | **Duman testi:** `deploy/smoke/check-security-headers.sh <url>` (`curl -sI`; beklenen başlıkların her biri yoksa sıfır dışı). Dağıtım sonrası çalıştırma kitabında; `deploy.sh`'ten uyarı olarak çağırmak istersen K'ya yaz. |

## 5. Adımlar ve dosya sahipliği

### Backend (`fix/<YYYY-MM-DD>-sec-04-security-headers`)
| Adım | İş |
|---|---|
| 18.6.1 | D1–D4: snippet + `davetkart.conf` include'ları + kılavuzlar. |
| 18.6.2 | D1: snippet'in kurulumu (dağıtım betiği ya da kılavuz) — betik değişiyorsa kılavuzuyla. |
| 18.6.3 | D6: duman testi betiği + kılavuzu. |
| 18.6.4 | `FAZ-18.md` `## 18.6 — SEC-04` (+ §11'deki kapanış bölümü). |

### Frontend (🔴 `git add -A` yasak)
| Adım | İş |
|---|---|
| 18.6.5 | **Yerel deneme:** `npm run build` → `vite preview`'u D2+D3 başlıklarıyla çalıştır (yalnızca `preview.headers`; `dev` sunucusuna dokunma) → Playwright ile ana sayfa, giriş, editör, bir WebGL/jiroskop şablonu, misafir sayfası ve ödeme sayfasını gez → konsoldaki CSP ihlallerini topla (rapor kipi + aynı politikayı bir kez **zorlayarak** da dene ki neyin kırılacağı görülsün) → politikayı düzelt. `preview.headers` yapılandırmasını kalıcı yapıp yapmamaya karar ver: kalıcıysa başlıkları Nginx snippet'inden **okuyan** tek kaynaklı bir çözüm olsun (iki kopya olmasın); değilse geçici değişikliği geri al ve frontend'de commit olmasın. |

### Docs
| Adım | İş |
|---|---|
| 18.6.6 | §7'deki ortak kayıtlar; K85'in satırına "SEC-04 ile SPA başlıkları Nginx'te → K…" notu. `YAYIN-SIRASI.md`'ye dağıtım sonrası duman testi adımı. |

## 6. Testler ve kalite kapısı

- `nginx -t`: Windows'ta Nginx ya da Docker varsa, sertifika yolları sahte dosyalarla karşılanmış bir kopyada dene. Yoksa "koşmadı" ve sunucuda benim çalıştıracağım komutu yaz.
- Duman testi betiği: yerel `vite preview` adresine karşı (D2+D3 başlıklarıyla) yeşil; başlıkları kaldırınca kırmızı (**mutant**).
- **Nginx miras mutantı:** snippet'i bir `location` bloğundan çıkar → o konumun yanıtında başlıklar yok (bunu ancak Nginx koşabiliyorsan gösterebilirsin; yoksa kod okumasıyla anlat ve B7'de "koşmadı" yaz).
- Playwright ihlal listesi: önce/sonra tablo.
- Sonda tam `composer check`; frontend'e dokunduysan `npm run check`.

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-18.md`: yoksa oluştur (başlık: "Faz 18 — denetim düzeltmeleri (`AUD-2026-11-12`)", altı bulgunun tablosu). `## 18.6 — SEC-04` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar, eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım doğrulama adımları. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).

**Docs deposu (`davetkart-docs`, dal `docs/2026-11-16-faz-18-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". K128–K145 boşluğuna dokunma (`ARC-01` ayrı bir iş); tablonun üstüne ⚠️ notu yoksa ekle.
- `phases/faz-18/README.md`: `SEC-04` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-18/FAZ-18-SEC-04-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**; geçmiş rapordur.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor).
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.
- Envanter, `script-src 'self'` ile çalışmayan bir şey gösteriyor (satır içi betik, `eval`, üçüncü taraf betik): seçenekleri (hash, nonce, betiği dosyaya taşımak) yaz, sor.
- Aynı kökenden çerçeve kullanımı var ve `X-Frame-Options`/`frame-ancestors` seçimi bir özelliği kırıyor.


## 11. Faz 18 kapanışı (SEC-04'ten sonra, aynı oturumda)

Bu dal, önceki beş düzeltmenin birleştiği `faz-18-audit-fixes`'ten açıldığı için Faz 18'in son hâlini temsil eder.

1. Bu dalda backend `composer check` **ve** `composer audit`; frontend `npm ci` + `npm run check`. Çıktıları B7 tablosuna yaz.
2. `docs/rehber/fazlar/FAZ-18.md` başına özet: altı bulgunun durumu, K numaraları, kalan elle işler (bu bölüm 18.6.4'ün commit'ine girer).
3. Docs: `phases/faz-18/README.md` tablosunu tamamla; `phases/README.md`'de Faz 18 satırı; `CHANGELOG.md`.
4. **Bana komutlar (çalıştırma):** a) SEC-04 dalını `faz-18-audit-fixes`'e birleştirme; b) `faz-18-audit-fixes` → `main` (önce backend, sonra frontend; `YAYIN-SIRASI.md` D3); c) **yalnızca** 1. maddedeki dört komut yeşilse iki depoda `v1.1.0` etiketi (`git tag -a v1.1.0 -m "..."`) ve `git push origin v1.1.0`; d) docs dalının `main`'e birleştirilmesi; e) dağıtım sırası ve dağıtım sonrası duman testi.
5. 🔴 `composer audit` kırmızıysa (`SEC-07`) etiket komutlarını **verme**; engelleri listele ve "etiket bekliyor" yaz. `SEC-07`'yi kendin düzeltme (ayrı bulgu).
6. Raporun sonuna "Faz 18'den sonra sıradaki işler" listesi: kalan 🟡 bulgular arasından yayından önce kapanması gerektiğini düşündüklerin, gerekçesiyle (öneri; karar benim).

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` → `git commit -m "18.6.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Sıra: backend blokları → frontend blokları → docs bloğu.
- En sona **birleştirme bloğu**: backend ve (commit gerekiyorsa) frontend için ayrı ayrı: `git switch faz-18-audit-fixes` → `git merge --no-ff <fix-dalı> -m "Merge SEC-04 fix into faz-18-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-18\FAZ-18-SEC-04-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (18.6.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili testin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, deneme) varsa numaralı liste.
