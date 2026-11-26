# Faz 21 — Ertelenmiş düşük bulgular ve açık kararlar (tek oturum)

> **Hazırlanma:** 26 Kasım 2026 · **Kaynak:** `AUD-2026-11-12` ([`REPORT.md`](../../audits/2026-11-12-full-system-audit/REPORT.md) §5.2,
> [`findings/`](../../audits/2026-11-12-full-system-audit/findings/)) düşük (🟢) ve öneri (💡) bulguları + `AUD-2026-11-26`
> ([`REPORT.md`](../../audits/2026-11-26-post-faz-19-scan/REPORT.md) §4b) ikinci taramanın karar soruları.
> **Biçim (İsmail, 26 Kasım 2026):** **tek ajan, tek oturum**. Bütün maddeler §1'deki sırayla, onay beklemeden koşulur. Her madde
> bitince `faz-21-backlog` dalına commit atılır ve sonraki maddeye geçilir. Commit'leri ajan atar, Claude izi yoktur. Ajana
> yapıştırılacak metin §4'te.
> **Geçmiş:** bu plan aynı gün `phases/faz-22/` olarak yazıldı. İsmail'in kararıyla Faz 21'e çevrildi (22.n → 21.n) ve tek oturumda
> koşacak biçime getirildi. `FE-07` eklendi: Faz 22 listesinde yoktu, 26 Kasım'da hâlâ açıktı. Önceki faz:
> [`faz-20/`](../faz-20/README.md).

## 0. Kapsam

18 madde. `AUD-2026-11-12`'nin 27 düşük/öneri bulgusundan bazıları 26 Kasım'da koda bakılarak **kapanmış** bulundu ve Faz 21'e girmedi:
- `ARC-09` (Faz 18.3)
- `SEC-14` (`express`/`dotenv` yok, derleme araçları `devDependencies`'te)
- `FE-05` (`contracts/plan-rules.json` + `verify:plans`, Faz 18.1)
- `FE-09` (en büyük video 2,3 MB)
- `FE-56` (`ThreeStage` `still`)

Faz 20'de kapananlar: `OPS-06`, `FE-06`, `FE-55`, `FE-57`.

`FE-07` 26 Kasım'da yeniden denetlendi: frontend `README.md` 0 satır, `CLAUDE.md:9` hâlâ "Google GenAI" diyor. Bu yüzden Faz 21'e alındı (21.16).

## 1. Takip

**Bu tablo ilerlemenin tek kaydıdır.** Ajan her madde bitince satırı günceller ve docs'a commit'ler. Oturum yarıda kesilirse ya da
bağlam özetlenirse, iş `bekliyor` olan ilk satırdan sürer.

Sıra:
1. Güvenlik ve ürün kararları
2. İşletim, temizlik ve test altyapısı
3. Kayıt işleri
4. **Frontend'in tamamına dokunan `ARC-07` en sonda**

"§A" sütununda ✅ olan maddenin karar tablosu §5'te. Ajan "Cevabın" sütunu doluysa onu uygular. Boşsa varsayılanı uygular ve K kaydına
"varsayılan (İsmail cevaplamadı)" yazar.

| Sıra | Bulgu | Önem | Konu | Efor | §A | Depolar | K | Commit'ler | Durum |
|---|---|---|---|---|---|---|---|---|---|
| 21.0 | — | — | Hazırlık: ortam eşitleme, dallar, taban kapıları, `FAZ-21.md` açılışı | S | — | backend · frontend · docs | — | be 6ffb824 | commit'lendi |
| 21.1 | `SEC-16` | 🟢 | Hesap bazlı (IP'den bağımsız) giriş freni | S | ✅ | backend · docs | K265 | be 245a71f | commit'lendi |
| 21.2 | `SEC-15` | 🟢 | Kayıt ucu adresin kayıtlı olduğunu söylüyor | S/M | ✅ | backend · frontend · docs | K266 | be ec850e0 | commit'lendi |
| 21.3 | `FE-58` | 🟢 | Ödeme dönüşünde davetiye kullanıcıya sorulmadan yayınlanıyor (K67) | S | ✅ | frontend · docs | K267 | fe ea9d8b1 | commit'lendi |
| 21.4 | `OPS-08` | 🟢 | Günlüklerde istek kimliği yok | S | ✅ | backend · (frontend) · docs | K268 | be 26943a9 | commit'lendi |
| 21.5 | `OPS-07` | 🟢 | PHP-FPM havuzu ve OPcache ayarı depoda yok | S | ✅ | backend (`deploy/`) · docs | | | bekliyor |
| 21.6 | `ARC-06` | 🟢 | Hiç fırlatılmayan 3 hata kodu | S | ✅ | backend · frontend · docs | | | bekliyor |
| 21.7 | `FE-08` | 🟢 | Konum araması: backend ucu yok, bayrakla kapalı kod | S | ✅ | frontend · docs | | | bekliyor |
| 21.8 | `FE-03` | 🟢 | TypeScript `strict` kapalı (bugün 20 hata) | S | — | frontend · docs | | | bekliyor |
| 21.9 | `TST-05` | 🟢 | Node sürümü sabit değil (CI 22, yerel 24) | S | ✅ | frontend · docs | | | bekliyor |
| 21.10 | `TST-06` | 💡 | Backend testleri paralel koşmuyor | M | — | backend · docs | | | bekliyor |
| 21.11 | `TST-03` | 🟢 | Satır kapsamı ölçülmüyor; eşik yok | S | ✅ | backend · docs | | | bekliyor |
| 21.12 | `ARC-10` | 💡 | `OptimizeUploadedImage` 664 satır, dört sorumluluk | M | — | backend · docs | | | bekliyor |
| 21.13 | `SEC-18` | 💡 | Token `localStorage`'da; `httpOnly` çerez (bu fazda yalnızca plan) | L | ✅ | docs | | | bekliyor |
| 21.14 | `OPS-09` | 💡 | Yatay ölçek eşikleri yazılı değil | S | — | docs | — | | bekliyor |
| 21.15 | `SEC-17` | 🟢 | Docs klasöründe git dışı 148 MB eski kod arşivi (`.env` içerenler) | S | ✅ | yerel disk (yalnızca liste) · docs | — | | bekliyor |
| 21.16 | `FE-07` | 🟢 | Frontend `README.md` boş; `CLAUDE.md` kodla çelişiyor | S | — | frontend · docs | — | | bekliyor |
| 21.17 | `ARC-08` | 🟢 | Dal hijyeni, sürüm etiketi yok, eski worktree'ler (yalnızca liste ve komut) | M | ✅ | üç depo (salt okuma) · docs | — | | bekliyor |
| 21.18 | `ARC-07` | 🟢 | Frontend'de `.gitattributes` yok (CRLF/LF) | S | ✅ | frontend · docs | | | bekliyor |
| 21.90 | — | — | Kapanış: tam kapılar, kayıtlar, rapor | S | — | backend · frontend · docs | — | | bekliyor |

Durum değerleri:
- `bekliyor`
- `commit'lendi` (ajan)
- `bloke → wip/<dal>` (ajan; nedeni §6'da)
- `plan` / `liste` (kod yazılmayan maddeler)
- `birleşti` (İsmail, `main`'e aldıktan sonra)

"Commit'ler" sütununa depo başına kısa hash yazılır (ör. `be 1a2b3c4 · fe 5d6e7f8`).

## 2. Genel kararlar (İsmail, 26 Kasım 2026)

| # | Konu | Karar |
|---|---|---|
| G1 | Commit'leri kim atar? | **Ajan** atar, her madde sonunda. Claude etiketi ya da trailer yok, push yok. Kimlik deponun mevcut `git config`'i (`ismail-cankaya`) |
| G2 | Entegrasyon dallarının tabanı | Backend ve frontend `faz-20-critical-fixes` ucu. Docs: Faz 21 plan dalının ucu |
| G3 | Dal adları | Backend ve frontend `faz-21-backlog`; docs `docs/<başlangıç tarihi>-faz-21-backlog`. **Madde dalı yok**: her madde doğrudan entegrasyon dalına commit'lenir |
| G4 | Onay | Yok. Ajan durmaz; dur gereken yerde §3 madde 5'teki kaçış yolunu uygular |

## 3. Ortak çalışma biçimi (bağlayıcı)

### Hazırlık ve ortam

1. **Önce oku:**
   - `davetkart-docs\CLAUDE.md`
   - `context\PHP-LARAVEL-SETUP.md` (§2, §11, §13). §9/§10 23 Eylül'de kaldı; güncel durum `phases\README.md`'de.
   - `decisions\DECISION-INDEX.md` (sıradaki boş K başlıkta; 26 Kasım'da K265)
   - Bu sayfa
   - Backend ve frontend `CLAUDE.md`
   - Her madde için: bulgunun tam metni (`findings/` ya da `AUD-2026-11-26` raporu) ve dokunacağın dosyaların
     `docs/rehber/<aynı-yol>.md` kılavuzları
2. **Ortamı eşitle (Faz 20 dersi):**
   - Backend: `composer sync` (bağımlılık + göç).
   - Frontend: Vite **kapalıyken** `npm ci`. Vite açıksa `npm install` kullan, çünkü `npm ci` `EPERM` ile `node_modules`'ü yarım bırakır.
   - `php artisan migrate:status --pending` boş, `composer install --dry-run` "Nothing to install" olmalı.

### Çalışma kuralları

3. **Bu fazda geçersiz olan proje kuralları (İsmail'in açık izni):**
   - "Git yazma işlemlerini İsmail yapar" (`CLAUDE.md` §7) → ajan `add` ve `commit` yapar, dal açar (`git switch -c`).
   - "Bu depodan çalışırken kod depolarında değişiklik yapma" (§8) → ajan üç depoda da çalışır.
   - "Her dosyadan sonra dur" → askıda. Açıklama yükümlülüğü (kılavuzlar, rapor) sürüyor.
4. **Hâlâ yasak:**
   - `push`, `merge` (`main`'e ya da başka dala), `rebase`, `reset`, `stash`, `tag`, `commit --amend`, `--no-verify`
   - `git branch -d/-D`, `worktree remove`, `git config` değişikliği, `--author`
   - Dosya silme dışında geri dönüşsüz yerel işler (arşiv silme, anahtar döndürme)
   - Canlı sisteme istek (sunucu, Shopier, AWS, Sentry, alan adı paneli, GitHub API)
   - Hiçbir dosyaya sır yazma
   - Sunucuda yapılacak adımlar komut olarak yazılır, koşulmaz.
5. **Durma yok, kaçış yolu var.** Bir madde §5'te "dur" gerektiriyorsa ya da kapılar 3 düzeltme denemesinden sonra hâlâ kırmızıysa:
   - (a) Maddenin değişikliklerini `wip/<YYYY-MM-DD>-21-<n>-<id>` dalına commit'le (`git switch -c wip/… && git add <dosyalar> && git commit`).
   - (b) `git switch faz-21-backlog`.
   - (c) §1 satırını `bloke → wip/…` yap, nedeni §6'ya bir paragraf olarak yaz, docs'u commit'le.
   - (d) Sonraki maddeye geç.

   Sonraki bir madde bloke maddeye bağlıysa o da aynı yolla bloke olur. Entegrasyon dalına **kırmızı kapıyla commit atılmaz**.
6. **Tek madde, tek kapsam.** Başka maddeye ait bir sorunu düzeltme; §6'da "gördüm, dokunmadım" altında yaz.
7. **Test önce (TDD):** davranış değişikliğinde önce kırmızı test, sonra kod. Her yeni test için en az bir mutantla testin gerçekten
   koruduğunu göster: kodu boz → kırmızı → geri al.

### Kapılar ve kayıt

8. **Kalite kapısı (madde sonunda, commit'ten önce):**
   - Backend'e dokunduysan `composer check` (Windows'ta PHPStan için `PHPSTAN_TURBO=0`). Bağımlılık değiştiyse ayrıca `composer audit`.
   - Frontend'e dokunduysan `npm run check`.
   - Kullanıcı akışına dokunan maddede `npm run e2e` (ayrı veritabanı `davetkart_e2e`, portlar 8020/4180; dev sunucularına dokunmaz).
     Bu maddeler: 21.1, 21.2, 21.3, 21.4, 21.6, 21.7, 21.8, 21.18.
9. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
10. **K18:** kod yorumu 1–3 satır; ayrıntı kendi deposunda `docs/rehber/<aynı-yol>.md`. Backend'de `php artisan k18:check` değişen
    her dosyayı **tamamen** ölçer: dokunduğun dosyadaki eski uzun yorum blokları da kısalıp kılavuza taşınır.
11. **Sözleşmeler:**
    - Hata kodu değişirse `php artisan errors:export`, frontend `src/contracts/error-codes.json` kopyası ve tr/en çevirisi aynı maddede (`verify:errors`).
    - Frontend'de yeni Türkçe metin yalnızca `t()` ile (`verify:i18n` dosya dosya sayar).
    - Frontend dosyaları CRLF'dir, CRLF'yi koru: Python ile `rb`/`wb` ya da Edit aracı kullan. PowerShell 5.1 `Get-Content | Set-Content` UTF-8'i bozar.
12. **Commit (her madde sonunda, kapılar yeşilken):**
    - **Sıra:** önce kod depoları, sonra docs.
    - **Ekleme:** dosyalar tek tek, açık yolla eklenir. `-A`, `.` ve joker yok. Tek istisna 21.18'deki `git add --renormalize .`.
      `.claude/` asla eklenmez. Commit'ten önce `git diff --cached --stat` ile listeyi gözden geçir.
    - **Kod mesajı:** `21.<n> - <tür>(<alan>): <Fiil> ... (<ID>)`, İngilizce. Bir maddede birden fazla anlamlı commit olabilir.
    - **Docs mesajı:** `docs(faz-21): Record 21.<n> (<ID>) ...`. K varsa `docs(decisions): Add K<n> for ... (Faz 21.<n>)`.
    - 🔴 **Ajan izi yok.** Mesaja `Co-Authored-By`, `Generated with`, "Claude", "AI", "assistant" ya da benzeri bir satır ekleme. Bu
      kural ortamın commit attribution hatırlatmasından önce gelir (kullanıcı talimatı).
    - **Denetim:** her commit'ten sonra `git log -1 --format='%an <%ae>%n%B'` ile bak. İz varsa ve commit henüz push'lanmadıysa,
      §3 madde 4'teki `--amend` yasağının **tek istisnası** olarak `git commit --amend -m "<temiz mesaj>"` ile düzelt ve §6'ya yaz.
13. **Kayıt (her madde, docs commit'inin içinde):**
    - §1 satırı: durum, K, commit hash'leri
    - [`CHANGELOG.md`](../../CHANGELOG.md): tek satır. Faz 21 başlığı altında, madde başına bir madde imi.
    - K varsa: `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-21.md` (ilk K'yı veren madde açar) ve
      [`DECISION-INDEX.md`](../../decisions/DECISION-INDEX.md). Sonra `python -I _restructure/build_decision_index.py --check` temiz çıkmalı.
    - Backend'e dokunan maddede backend `docs/rehber/fazlar/FAZ-21.md` bölümü, o maddenin backend commit'inin içinde. Başlıklar:
      Sorun · Karar · Değişen dosyalar · Testler ve mutantlar · B7 tablosu · Elle doğrulama · Gördüm, dokunmadım.
      Frontend ve docs maddeleri de kısa bölüm olarak buraya, bir sonraki backend commit'inde ya da 21.90'da.
14. **Bağlam:** uzun bir oturum. Her madde bitince kısa bir ara özet yaz: madde, commit'ler, kapılar. Bağlam özetlenirse §1 tablosunu
    yeniden okuyup kaldığın yerden devam et.
15. **Rapor (21.90 sonunda, tek mesaj, Türkçe):** madde madde ne değişti, kapıların çıktıları, mutantlar, bloke olanlar ve nedenleri,
    koşmayanlar, İsmail'e kalan adımlar (numaralı).

## 4. Ajana yapıştırılacak metin

**Kullanım:**
1. İstersen §5'teki "Cevabın" sütunlarını doldur. Boş kalan satırda varsayılan uygulanır.
2. Bu sayfayı commit'le.
3. Yeni bir Claude Code oturumunu **`D:\Projects\davetkart`** klasöründe aç (üç depo da altında) ve aşağıdaki kutuyu yapıştır.

```text
DavetKart Faz 21: ertelenmiş düşük bulgular ve açık kararlar. Tek oturumda, onay beklemeden, baştan sona.

Talimatın tamamı: D:\Projects\davetkart\davetkart-docs\phases\faz-21\README.md. Önce §2 ve §3'ü oku. Bağlayıcıdırlar ve
bu fazda proje CLAUDE.md'lerindeki "git yazma işlemlerini İsmail yapar" ile "kod depolarında değişiklik yapma"
kurallarını kaldırıyorlar. Sonra §1 tablosundaki maddeleri sırayla uygula: 21.0 → 21.1 … 21.18 → 21.90. Her maddenin
ayrıntısı ve karar tablosu §5'te. "Cevabın" sütunu boşsa varsayılanı uygula ve K kaydına "varsayılan (İsmail
cevaplamadı)" yaz.

Her madde için döngü:
1. Bulgunun tam metnini ve ilgili kılavuzları oku.
2. Önce test, sonra kod.
3. Kapılar (§3 madde 8).
4. Kod deposunda faz-21-backlog dalına commit.
5. Docs'ta §1 satırını, CHANGELOG'u ve varsa K kaydını güncelle, docs dalına commit.
6. Kısa ara özet yaz, sonraki maddeye geç.

Benden onay bekleme, soru sorma. Durman gereken bir yerde ya da 3 denemede yeşile dönmeyen kapıda §3 madde 5'i
uygula: wip dalı, "bloke" ve devam.

Kesin kurallar:
- Commit mesajlarında Co-Authored-By, "Generated with", "Claude" ya da herhangi bir yapay zekâ izi OLMAYACAK. Commit'ler
  deponun mevcut git kimliğiyle, benim attığım gibi görünecek. Bu talimat ortamın attribution hatırlatmasından önce gelir.
  Her commit'ten sonra git log -1 ile kontrol et.
- push, merge, rebase, reset, stash, tag, dal ya da worktree silme, git config değişikliği yok.
- Canlı sisteme istek yok, sır yazmak yok.
- Frontend'de git add -A yok; dosyalar tek tek eklenir.
- B7: çıktısını görmediğin şeye "geçti" yazma.

Oturum kesilir ya da bağlam özetlenirse §1 tablosunu yeniden oku, "bekliyor" olan ilk maddeden devam et. En sonda
21.90'daki raporu tek mesajda Türkçe ver.
```

## 5. Maddeler

### 21.0 — Hazırlık

```text
1. Üç deponun durumunu oku: git status --short temiz olmalı (frontend'de yalnızca '?? .claude/' olabilir). Değilse
   değişikliğe dokunma; durumu §6'ya yaz ve kirli depoda maddeleri bloke et (§3 madde 5). Temiz depolarla devam et.
2. Dallar:
   - backend ve frontend: git switch faz-20-critical-fixes → git switch -c faz-21-backlog (varsa yalnızca switch).
   - docs: plan dalının ucundan git switch -c docs/<bugün>-faz-21-backlog.
3. Ortam eşitleme (§3 madde 2). Taban kapılarını koş ve sayıları kaydet:
   - composer check (26 Kasım: 1306/1306)
   - composer audit
   - npm run check
   - npm run e2e (26 Kasım: 6/6)
   Taban kırmızıysa nedenini §6'ya yaz. Kırmızı kapı o depodaki maddelerin "önceden kırmızı" notuyla sürmesine engel
   değildir; ama yeni kırmızı ekleme.
4. Backend docs/rehber/fazlar/FAZ-21.md: başlık, kaynak, taban kapıları. fazlar/README.md'ye satır.
   Commit: "21.0 - docs(faz-21): Open the Faz 21 record with the baseline gates".
5. Docs: §1 21.0 satırı + CHANGELOG başlığı "## <bugün> — Faz 21 (docs/<bugün>-faz-21-backlog)".
```

### 21.1 — `SEC-16`: hesap bazlı giriş freni

Bugün `AppServiceProvider::authLimits()` iki kova kullanıyor: e-posta + IP başına 5/dk ve IP başına 20/dk. Çok IP'den tek hesaba
yapılan denemeler hiçbir kovada birikmez.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | E-posta başına (IP'den bağımsız) sınır | Saatte 30 deneme | |
| 2 | Aşılınca | 429 `RATE_LIMITED` (`retryAfter` ile); hesap kilitlenmez (kilit, saldırganın sahibi dışarıda bırakmasına araç olur) | |
| 3 | Hesap sahibine "şüpheli giriş denemeleri" postası | Evet, kova ilk dolduğunda, saatte en çok 1 (kuyrukta); postada IP yok | |
| 4 | Kovaya sayılan denemeler | Yalnızca **başarısız** girişler (doğru parolayla giren sahip kendi kovasını doldurmaz) | |

```text
Tam metin: findings\02-security.md "SEC-16".
1. Önce test (tests/Feature içinde, mevcut auth hız sınırı testlerinin yanına):
   - Aynı e-postaya farklı IP'lerden (REMOTE_ADDR değiştirerek) §A-1 sınırının bir fazlası kadar başarısız deneme →
     sonuncusu 429 RATE_LIMITED.
   - Başka e-postaya aynı IP'lerden deneme etkilenmez.
   - §A-4'e göre doğru parolayla giriş kovayı doldurmaz. Bunun için sayaç başarısız girişte elle artırılır;
     Limit::by tek başına başarılı isteği de sayar.
2. authLimits()'e üçüncü kova ya da LoginAction'da başarısızlıkta artan ayrı bir RateLimiter anahtarı:
   - E-posta EmailNormalizer ile normalize edilir; kişisel veri olduğu için anahtar hash'lenir (IpHasher deseni).
   - Mevcut iki kova ve sırası değişmez.
3. §A-3 "evet" ise kuyruklu bildirim: mevcut Notification desenleri, yerelde MAIL_MAILER=log, saatte en çok 1, şablon tr.
4. Kılavuzlar: AppServiceProvider.md (hız sınırı bölümü), yeni sınıfların .md'leri, gerekirse docs/08 hata sözleşmesi.
5. K kaydı: sınır, sayılan denemeler, bildirim (sıradaki boş K).
Kaçış: mevcut bir test kova sırasına ya da sayısına bağlıysa o testi değiştirme; yeni kovayı mevcut ikisinin ARKASINA ekle.
Yine de çakışıyorsa §3 madde 5.
```

### 21.2 — `SEC-15`: kayıt ucu adresin kayıtlı olduğunu söylüyor

Var olan adresle kayıt `422 REGISTRATION_FAILED`, yeni adresle 201 döner (`RegisterUserAction`, `UniqueConstraintViolationException`).
Bulguyu tamamen kapatmanın tek yolu kaydı "postanızı kontrol edin" akışına çevirmek. Bu K11'i değiştirir (kayıt `{user, token}` döner
ve oturum açar).

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Yol | **B:** sözleşme aynı kalır; riski kabul et, kayıt ucuna e-posta + IP kovası ekle, 201 ve 422 yanıt sürelerini eşitle, kararı K'ye yaz | |
| 2 | A seçilirse (tam kapatma) | Kayıt her zaman `202 {status: "check_email"}` döner, oturum açmaz; adres yeniyse doğrulama postası, kayıtlıysa "biri bu adresle kayıt denedi, siz miydiniz? Giriş / parola sıfırlama" postası; ilk giriş doğrulamadan sonra. Frontend kayıt sayfası "postanızı kontrol edin" ekranına geçer; e2e `register()` akışı güncellenir | |

```text
Tam metin: findings\02-security.md "SEC-15". İlgili kararlar:
- K11: auth yanıtı zarfsız {user, token}
- K191: e-posta doğrulama
- A1–A7: auth uçlarında unique/exists yok, kısa devre yok

§A-1 = B (varsayılan) ise:
1. Önce testler: kayıt ucuna e-posta+IP ve IP kovası (mevcut 'auth' limiter'ıyla aynı desen, sayılar K'de). Var olan
   adresle kayıt denemesi de kovaya sayılır.
2. Yanıt süresi: var olan adreste de parola hash'i hesaplanmalı (A3 ruhu). RegisterUserAction'ın çakışma yolunda
   Hash::make atlanıyor mu, kontrol et. Atlanıyorsa eşitle. Zaman testi kırılgan olduğu için bunu test etme; gerekçeyi
   kılavuza yaz.
3. K: "SEC-15 kabul edilen risk: kayıt ucu kayıtlı adresi 422 ile söyler; frenler: …; tam kapatma K11'i değiştirir".

§A-1 = A ise:
1. Kontrat değişikliği: backend RegisterController/Action → 202 {status:"check_email"}. Zarf istisnası C2'ye göre ad ad
   tanımlı: docs/08 ve contracts güncellenir. Oturum açılmaz. Kayıtlı adrese "kayıt denemesi" postası (kuyrukta, hız sınırlı).
2. Frontend: RegisterPage ve services/auth.ts register(). "Postanızı kontrol edin" ekranı t() ile.
   verify:endpoints/verify:state güncellenir. e2e/support/flows.ts register() doğrulama bağlantısından sonra giriş yapar.
   npm run e2e yeşil.
3. Eski davranışı kilitleyen testler bilinçli güncellenir; her değişiklik §6'da listelenir.
Kaçış (A): kayıttan hemen sonra oturum varsayan bir akış bulursan (ödeme dönüşü, sihirbaz) onu da bu maddede düzelt ve
e2e ile doğrula. Olmuyorsa §3 madde 5.
```

### 21.3 — `FE-58`: ödeme dönüşünde onaysız yayın

`useAutoPublish.ts` şöyle çalışıyor: sipariş `paid` ve davetiyeye bağlıysa dönüş sayfası düğmesiz `POST /invitations/{id}/publish` atar.
K67 ise "ödeme yayınlamaz; yayın ayrı bir kullanıcı eylemidir" diyor (⚠️ çelişki sorusu açık).

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Davranış | **Otomatik yayın kalır** (kullanıcı ödemeye zaten "Yayınla"dan geldi). K67 yeni K ile daraltılır: "ödeme **sunucuda** yayınlamaz; frontend, yayın niyetiyle başlayan ödemenin dönüşünde yayınlar" | |
| 2 | Otomatik değilse | Dönüş sayfasında "Şimdi yayınla" düğmesi; ödeme alındı, davetiye taslakta kalır | |

```text
Tam metin: findings\04-frontend-e2e.md "FE-58"; K67 ve EK-FAZ-12 §F-7.
1. Seçilen davranışı verify:payment'te kilitle (önce kırmızı):
   - §A-1 otomatik ise: davetiyeye bağlı ödenmiş sipariş dönüşte TEK yayın isteği üretir; paket (davetiyesiz) siparişi
     üretmez; tekrar ziyaret ikinci istek üretmez.
   - Düğme seçildiyse: istek yalnızca düğmeyle gider.
2. Otomatik kalıyorsa kod değişmeyebilir; yalnızca test + K. Düğme seçildiyse PaymentReturnPage + useAutoPublish, metinler t().
3. K: K67'nin durumuna "daraltıldı → K<yeni>" yaz (K67 silinmez). EK-FAZ-12 §F-7 sorusuna bağlantı ver.
4. npm run check ve npm run e2e (yayın yolculuğu ödeme dönüşünden geçiyor).
```

### 21.4 — `OPS-08`: istek kimliği

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Hata zarfına `requestId` | Hayır (sözleşme aynı kalır); yalnızca `X-Request-Id` yanıt başlığı. Destek için frontend hata bildiriminde göstermek ayrı iş | |
| 2 | Gelen `X-Request-Id` başlığına güvenilsin mi? | Yalnızca biçimi geçerliyse (ULID/UUID, ≤64 karakter); değilse yenisi üretilir | |

```text
Tam metin: findings\05-operations.md "OPS-08".
1. Önce test (HardeningTest ya da yeni RequestIdTest):
   - Her API yanıtında X-Request-Id var.
   - Geçerli gelen kimlik aynen döner; geçersiz ya da uzun gelen kimlik yenisiyle değişir.
   - Aynı istekte yazılan log satırları request_id taşır (Log::spy ya da Context::get).
   - Kuyruğa giden iş aynı kimliği taşır (Laravel Context işlerle taşınır, doğrula).
2. Ara katman: app/Http/Middleware içinde, bootstrap/app.php'de global ve EN BAŞTA (M1 kuralı: yalnızca Accept ezilir).
   Illuminate\Support\Facades\Context::add('request_id', …) ve yanıt başlığı. Log biçiminde context görünüyor mu, kontrol et.
3. deploy/nginx'te $request_id ile başlık geçirme önerisini kılavuza yaz (sunucu adımı, koşma).
4. Kılavuzlar + K (başlık adı, biçim, güven kuralı).
```

### 21.5 — `OPS-07`: PHP-FPM havuzu ve OPcache

Sunucu 2 GB. Kuyruk işçisi 768 MB'a, her FPM süreci 256 MB'a kadar çıkabilir. Havuz dosyası depoda yok. K264'ten beri deploy bakım
kipinde ve FPM'i `reload` ediyor; bu da `opcache.validate_timestamps=0`'ı güvenli kılar.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | `pm.max_children` | 4 (`pm = dynamic`, `start_servers 2`, `min_spare 1`, `max_spare 3`, `max_requests 500`) | |
| 2 | OPcache | `memory_consumption=128`, `max_accelerated_files=20000`, `validate_timestamps=0` (deploy'da reload şart; `deploy.md`'ye yaz) | |

```text
Tam metin: findings\05-operations.md "OPS-07". Sunucuya istek YOK.
1. Dosyalar:
   - deploy/php-fpm/davetkart.conf (havuz): kullanıcı www-data, socket deploy/nginx ile aynı, §A-1 sayıları, slowlog,
     request_terminate_timeout = nginx fastcgi_read_timeout ile uyumlu.
   - deploy/php/davetkart.ini'ye §A-2 OPcache satırları.
2. Kılavuz docs/rehber/deploy/php-fpm/davetkart.md:
   - Bellek tablosu: FPM 4×256, kuyruk 768, PostgreSQL shared_buffers önerisi, işletim sistemi payı; toplam 2048 MB içinde.
   - Kurulum komutları (cp → php-fpm8.5 -t → systemctl reload) ve geri alma.
   - deploy.md'ye not: "validate_timestamps=0: reload'suz kod değişmez".
3. Yerel doğrulama: Herd'in php-cgi/php-fpm'i ile `-t` sözdizimi denemesi mümkünse koş, değilse "koşmadı" yaz.
4. İsmail'e kalan sunucu adımları §6'da numaralı liste.
```

### 21.6 — `ARC-06`: kullanılmayan hata kodları

`TOKEN_EXPIRED`, `INVITATION_LOCKED` ve `SLUG_TAKEN` katalogda ve çevirilerde var, ama `app/` içinde bunları fırlatan yok. Faz 20.7'den
beri frontend 401'de "Oturumunuz sona erdi" diyor; `TOKEN_EXPIRED` ayrımına gerek kalmadı.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Üç kod | Üçü de silinir (`SLUG_TAKEN`, K66: slug üretilmiyor) | |

```text
Tam metin: findings\01-architecture.md "ARC-06".
1. Önce kanıt: grep ile üç kodun backend app/ ve frontend src/ kullanımını göster. Çeviri dosyaları hariç sonuç 0 olmalı.
2. Silinecek ve güncellenecek yerler:
   - app/Enums/ErrorCode.php: case'ler ve status()/params eşlemeleri
   - php artisan errors:export → contracts/error-codes.json
   - Frontend src/contracts kopyası ve tr/en errors.json anahtarları
   - docs/08 hata sözleşmesi tablosu
3. 🔴 K18 cırcırı: ErrorCode.php'yi değiştirince k18:check dosyanın TAMAMINI ölçer (26 Kasım'da 9 uzun blok). Blokları
   1–3 satıra indir, ayrıntıyı docs/rehber/app/Enums/ErrorCode.md'ye taşı (anlam kaybı olmasın).
4. Kapılar: composer check, npm run check (verify:errors kod sayısı 31 → 28), npm run e2e.
5. Commit'ler: backend ve frontend ayrı; mesajlarda aynı madde numarası.
```

### 21.7 — `FE-08`: konum araması

`src/services/places.ts`, `hooks/usePlaceSearch.ts` ve `components/create/location/LocationSearchField.tsx` duruyor. Backend'de `places`
rotası yok, bayrak (`VITE_PLACES_SEARCH_ENABLED`) kapalı.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Yol | **Kaldır:** üç dosya ve bayrak silinir, "haritadan seç" tek yol | |
| 2 | Uç yazılacaksa | Ayrı faz (Places anahtarı sunucuda, önbellek, `throttle`, KVKK gizlilik metni). Faz 21'de yalnızca plan | |

```text
Tam metin: findings\04-frontend-e2e.md "FE-08".
Kaldır seçildiyse:
1. Üç dosyayı ve kullanım yerlerini, .env örneklerindeki bayrağı ve docs/rehber kılavuzlarını kaldır. Bu silme bulgunun
   kendisidir ve git'te geri alınabilir.
2. Editörde konum alanı "haritadan seç" ve elle yazma ile çalışmaya devam etmeli (e2e createInvitation 'Davet Konumu'
   alanını dolduruyor).
3. verify:endpoints ve verify:i18n tabanı azalırsa `npm run verify:i18n -- --update` (yalnızca azalış).
4. npm run check + npm run e2e.
Uç seçildiyse: kod yazma. Planı bu sayfanın sonuna "Ek C — FE-08 konum araması planı" olarak yaz (uç sözleşmesi,
sağlayıcı, maliyet, KVKK) ve §1 satırını "plan" yap.
```

### 21.8 — `FE-03`: TypeScript `strict`

26 Kasım'da `npx tsc --noEmit --strict` 20 hata verdi:
- 15'i `templates/shared/effects/particleEngine.ts`
- 2'si `preview/PreviewSection.tsx`
- Birer tane `templates/lazyPresets.ts`, `templates/TemplateRenderer.tsx` ve `create/EditorWorkspace.tsx`

```text
Tam metin: findings\04-frontend-e2e.md "FE-03".
1. Ölç: npx tsc --noEmit --strict. Dosya başına sayıyı §6'ya yaz.
2. tsconfig.json'a "strict": true. Hataları davranış değiştirmeden kapat:
   - null için erken dönüş ya da daraltma
   - `as` ve `!` yalnızca bir satırlık gerekçe yorumuyla
   - particleEngine.ts'te canvas/context null'ı bir kez daraltılıp aşağı geçirilsin
3. noUncheckedIndexedAccess bu maddede AÇILMAZ. Deneme olarak açarsan kaç hata çıktığını §6'ya yaz (sonraki karar için)
   ve geri kapat.
4. npm run check + npm run e2e (şablonlar ve editör a11y taraması dahil) + npm run a11y:envelopes.
```

### 21.9 — `TST-05`: Node sürümü

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Sürüm | Node 24 (yerel 24.18; sunucudaki derleme sürümü Y6.5c'ye göre v24.22.1 → İsmail'e doğrulama komutu) | |

```text
Tam metin: findings\03-testing.md "TST-05".
1. Frontend:
   - Köke .nvmrc (§A-1).
   - package.json'a "engines": {"node": ">=24 <25"}.
   - .github/workflows/*.yml'de her iş için node-version yerine node-version-file: .nvmrc.
2. deploy-frontend.sh (backend deposunda, deploy/) başında `node --version` .nvmrc ile uyuşmuyorsa UYARI yazsın, durdurmasın.
   Backend commit'i aynı madde numarasıyla.
3. Kılavuz yaz. İsmail'e sunucuda çalıştıracağı `node --version` komutunu ver. CI push'u İsmail'in; CI koşusu "koşmadı".
```

### 21.10 — `TST-06`: paralel testler

```text
Tam metin: findings\03-testing.md "TST-06"; K182 (DAVETKART_TEST_DB_SUFFIX, TestSuiteIsolationTest).
1. Ölç: php artisan test, tam süre (26 Kasım: ~200–260 sn, 1306 test).
2. brianium/paratest (dev) + `php artisan test --parallel`:
   - PostgreSQL'de süreç başına veritabanı (davetkart_test_<token>), K182 son ekiyle birlikte çalışmalı.
   - TestSuiteIsolationTest buna göre güncellenir.
   - Kilit testleri (concurrency grubu, TST-02: alt süreç ve lock_timeout) paralelde kararsızsa ayrı grupta sıralı koşar.
3. composer check'teki test adımı DEĞİŞMEZ. Yalnızca ayrı betik eklenir (`composer test:parallel`). Üç ardışık yeşil koşu
   ve süre farkını §6'ya yaz. check'e alınması İsmail'e soru olarak rapora girer.
4. composer audit (yeni dev bağımlılığı).
```

### 21.11 — `TST-03`: satır kapsamı

Yerel Herd PHP'de `pcov`/`xdebug` yok (26 Kasım'da yeniden bakılmadı).

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Eşik | İlk ölçümün 3 puan altı; ölçüm yoksa eşik yok, yalnızca rapor | |

```text
Tam metin: findings\03-testing.md "TST-03".
1. Yerelde php -m ile pcov/xdebug var mı, bak. Yoksa kurulum yolunu (Herd) kılavuza yaz; kurma.
2. CI (.github/workflows/ci.yml): coverage: pcov ve ayrı adımda `php artisan test --coverage --min=<eşik>`. Eşik yoksa
   --min'siz çalışır ve özeti artefakt olarak saklar. composer check değişmez.
3. Ölçüm yerelde koşmadıysa eşik koyma. "İlk CI koşusundan sonra eşik koy" adımını İsmail'e kalanlara yaz.
```

### 21.12 — `ARC-10`: görsel işleme işi

```text
Tam metin: findings\01-architecture.md "ARC-10". Davranış DEĞİŞMEZ (saf yeniden düzenleme).
1. Önce mevcut OptimizeUploadedImageTest ve medya testlerini koş; yeşil tabanın sayısını §6'ya yaz.
2. app/Jobs/OptimizeUploadedImage.php (664 satır) küçük sınıflara bölünür:
   - Öneri: ImageDecoder, ExifOrientation, ImageEncoder, MediaFileSwap.
   - Adlar ve yerler CLAUDE.md'ye göre: dış servis değil → app/Support/Media/ ya da Action.
   - Job yalnızca sırayı yönetir.
3. Her yeni sınıfa birim testi + bir mutant. Uçtan uca test aynen yeşil kalır. Şu iki koruma testte var mı, bak
   (AUD P54–P55); yoksa ekle:
   - Saklanan dosyada EXIF yok.
   - Saklanan dosyada dosya sonuna eklenmiş PHP kuyruğu yok.
4. K18: job'un 264 satırlık yorumu sınıf kılavuzlarına dağılır; k18:check temiz.
```

### 21.13 — `SEC-18`: token `httpOnly` çerezde (bu fazda yalnızca plan)

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Kapsam | **Yalnızca plan** (karar kaydı + geçiş planı); uygulama CSP zorlamaya geçtikten (K175) sonra ayrı faz | |
| 2 | Plan neyi varsaysın | Sanctum SPA çerez kimliği (aynı site: `davetkart.com` + `/api`), CSRF çerezi, `{user, token}` zarfı yerine `{user}` (K11 değişir), geçiş süresince iki yol | |

```text
Tam metin: findings\02-security.md "SEC-18". İlgili: K5, K11, K174–K175 (CSP); frontend src/services/auth.ts ve api.ts.
Bu fazda kod YOK (onaysız tek oturumda kimlik doğrulama mimarisi değiştirilmez). §A-1'e "uygula" yazılmışsa bile yalnızca
plan yazılır ve planın sonuna "uygulama fazı önerisi" eklenir.

Planı bu sayfanın sonuna "Ek A — SEC-18 geçiş planı" olarak yaz. İçerik:
- Tehdit: XSS ile token okuma
- Seçenekler
- Sanctum SPA kurulumu: stateful domain, CSRF, CORS, Nginx
- K11/K20 etkisi
- Frontend değişiklikleri: interceptor, 401, sekme senkronu
- Mobil ve üçüncü taraf etkisi (yok)
- Geçiş ve geri alma
- Test planı (e2e)
- Ön koşul: K175 zorlama
- Sonunda İsmail'e karar soruları
K: "planlandı". §1 durumu: plan.
```

### 21.14 — `OPS-09`: yatay ölçek eşikleri

```text
Tam metin: findings\05-operations.md "OPS-09". Yalnızca docs; kod yok.
1. operations/deployment/YAYIN-PLANI.md §6'daki "Lightsail'den ne zaman çıkılır" eşiklerine ölçülebilir sayılar ekle:
   - FPM kuyruğu (slowlog/listen queue)
   - Bellek (21.5 tablosu)
   - p95 yanıt süresi
   - PostgreSQL bağlantı ve disk
2. İkinci sunucuya geçişte kırılacakların listesi:
   - file cache → hız sınırı sayaçları sunucu başına olur
   - onOneServer/withoutOverlapping kilitleri
   - database kuyruğu
3. Geçiş sırası: önce PostgreSQL'i ayır, sonra Redis (cache + kuyruk + kilit).
YAYIN-PLANI bir plan kaydı: eski satırları yeniden yazma, yeni alt bölüm ekle. IZLEME.md'ye hangi metriğin nereden
okunacağını yaz.
```

### 21.15 — `SEC-17`: diskteki eski kod arşivleri (yalnızca liste)

`davetkart-docs/archive/local-snapshots/` git dışında (`.gitignore:5`). 26 Kasım'da 16 dosya, 148 MB tutuyordu (`_snap/*.tgz|*.tar`,
`_to_delete/`). Denetimde üç arşivin dosya listesinde `.env` vardı. Silme ve anahtar döndürme **İsmail'in** işi.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Arşivler | Ajan yalnızca listeler; İsmail siler ya da şifreli kasaya taşır | |
| 2 | Anahtarlar | `.env` içeren arşivlerdeki anahtar **adlarını** (değerleri değil) ajan listeler; hâlâ geçerli olanları İsmail döndürür | |

```text
Tam metin: findings\02-security.md "SEC-17".
🔴 Arşivleri AÇMA, içerik okuma, değer yazdırma. Yalnızca `tar -tf`/`tar -tzf` ile dosya ADI listesi.
1. Her arşiv için: boyut, tarih, .env / *.pem / credentials içeren yol var mı (evet/hayır).
   .env içeren arşivlerde §A-2 için yalnızca anahtar ADLARI gerekiyor:
   `tar -xOf <arşiv> <yol> | grep -oE '^[A-Z0-9_]+='`
   Değer yazdırma YOK; çıktı yalnızca adlar.
2. Listeyi bu sayfanın sonuna "Ek B — SEC-17 arşiv listesi" olarak yaz (adlar, boyutlar, içerik türü; değer yok).
3. İsmail'e kalanlar:
   - Hangi arşivin silinebileceği
   - Hangi anahtarların döndürülmesi gerektiği (APP_KEY, DB parolası, AWS, Shopier) ve nasıl (her biri için tek satır yol)
Silme yok. §1 durumu: liste.
```

### 21.16 — `FE-07`: frontend `README.md` ve `CLAUDE.md`

26 Kasım'da frontend `README.md` 0 satırdı. `CLAUDE.md:9` hâlâ "AI Integration: Google GenAI (`@google/genai`)" diyor; oysa asistan
backend üzerinden çalışıyor.

```text
Tam metin: findings\04-frontend-e2e.md "FE-07" (satır 166).
1. README.md:
   - Kurulum: Node sürümü .nvmrc'den (21.9), Vite kapalıyken npm ci
   - npm run check / e2e / a11y:envelopes ne yapar
   - Ortam değişkenleri (.env.example'dan; değer yok)
   - Backend'le ilişki (aynı köken /api, VITE_API_BASE_URL)
   - verify:* betiklerinin kısa listesi
   - Kılavuzların yeri (docs/rehber)
2. CLAUDE.md:
   - Yalnızca kodla çelişen satırları düzelt: GenAI satırı → "asistan backend üzerinden (/api/assistant)".
     İlgili diğer çelişkiler için findings satır 43'e bak.
   - verify betikleri ve strict (21.8) gerçeğe göre.
   - Başka kural ekleme ya da çıkarma.
3. Önce `@google/genai` hâlâ package.json'da mı ve src/ içinde kullanılıyor mu, grep ile bak. Kullanılmıyorsa bağımlılığı
   kaldırmak bu maddenin işi DEĞİL; §6 "gördüm, dokunmadım".
4. npm run check.
```

### 21.17 — `ARC-08`: dal hijyeni ve sürüm etiketleri (yalnızca liste ve komut)

26 Kasım'daki durum:
- Yerel dallar: backend 33, frontend 48, docs 7.
- Üç depoda da etiket yok.
- `davetkart-backend-php-laravel.worktrees/` altında 4 eski worktree; `D:\Projects\davetkart-hat-{a,b,c}` Faz 19 worktree'leri (ayrık uçta).
- Bekleyen etiketler (Hat C #21): `v1.0.0`, `v1.1.0` (Faz 18 + `SEC-07`), `v1.2.0` (Faz 19).

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Silinecek dallar | Yalnızca `git branch --merged <entegrasyon>` listesindekiler önerilir; uzak dallara dokunulmaz | |
| 2 | Worktree'ler | Temiz olanlar (`git status` boş) için `git worktree remove` komutu önerilir; kirli olan listelenir | |
| 3 | Etiketler | Ajan hangi commit'in hangi etiket olacağını docs kayıtlarından çıkarır ve tablo hâlinde sunar | |

```text
Tam metin: findings\01-architecture.md "ARC-08". Etiket kayıtları:
- phases\faz-19\FAZ-19-SEC-07-COMMIT-KOMUTLARI.md §5
- FAZ-19-ARC-03-COMMIT-KOMUTLARI.md §5–§7
- operations\deployment\YAYIN-SIRASI.md §3
- phases\faz-19\HAT-C-ACIK-HATALAR.md #21, #29

Bu madde GERİ DÖNÜŞSÜZ adımlar içerir. Bu tek oturumda HİÇBİRİ koşulmaz: dal silme, worktree remove ve tag yok.
Yalnızca salt okunur git komutları (branch -vv, branch --merged, worktree list, log, status) kullanılır.
1. Yeni dosya phases\faz-21\FAZ-21-ARC-08-KOMUTLARI.md:
   - Üç depo için tablo: dal, son commit tarihi, entegrasyon dalına birleşmiş mi, hangi worktree'de açık.
     Yazım hatalı adları işaretle.
   - Worktree tablosu: yol, dal ya da uç, temiz mi.
   - Etiket önerisi: v1.0.0 / v1.1.0 / v1.2.0 için commit ve gerekçe (kayıttan alıntı).
   - İsmail'in koşacağı komutlar: her adım ayrı PowerShell bloğu; `git branch -d` (asla -D), tek tek; `git worktree
     remove`; `git tag -a`. Push yok. Her blok `git status --short` ile biter.
2. Bu klasörün dosya listesine (§7) satır ekle.
3. HAT-C-ACIK-HATALAR #21/#29'a bu dosyaya bağlantı ekle. Geçmiş metni yeniden yazma; yalnızca not ekle.
§1 durumu: liste.
```

### 21.18 — `ARC-07`: frontend `.gitattributes` (en son)

Frontend çalışma ağacı CRLF, indeks çoğunlukla LF (`autocrlf`). Sözleşme dosyası iki depoda bayt bayt farklı. Normalizasyon commit'i
yüzlerce dosyaya dokunabilir; açık işlerle çakışmasın diye **bütün frontend maddelerinden sonra** yapılır.

| # | Soru | Boş bırakırsan | Cevabın |
|---|---|---|---|
| 1 | Kural | `* text=auto eol=lf` + ikili kalıplar (`*.png *.jpg *.webp *.mp4 *.webm *.woff2 *.glb *.ico binary`) | |
| 2 | Çalışma ağacı | Dokunulmaz: mevcut CRLF dosyalar git'te LF'ye normalize edilir, `git status` temiz kalmalı. Dosyaları diskte de LF'ye çevirmek isteğe bağlı; ajan adımları yazar (yalnızca temiz ağaçta, Vite kapalıyken), İsmail koşar | |

```text
Tam metin: findings\01-architecture.md "ARC-07".
Ön koşul: frontend faz-21-backlog'da çalışma ağacı temiz ve 21.2–21.16'nın frontend işleri commit'li ya da bloke.
Değilse maddeyi bloke et (§3 madde 5).
1. Ölç: `git ls-files --eol` özeti (i/lf, i/crlf, i/mixed sayıları) ve contracts/error-codes.json'ın backend kopyasıyla
   bayt farkı.
2. İki ayrı commit:
   (a) Yalnızca .gitattributes.
   (b) `git add --renormalize .` sonucu. Bu, §3 madde 12'deki tek joker istisnasıdır. Değişiklik yalnızca satır sonu
       olmalı: `git diff --cached --ignore-all-space --stat` boş çıkmalı. Değilse `git restore --staged .` ile indeksi
       boşalt ve maddeyi bloke et.
3. Sonra npm run check + npm run e2e. contracts dosyası backend'le bayt bayt aynı olmalı (sha256).
4. docs CLAUDE.md §7 "CRLF tuzağı" maddesi için güncelleme önerisini §6'ya yaz. CLAUDE.md'yi değiştirme.
```

### 21.90 — Kapanış

```text
1. Tam kapılar, son uçta:
   - composer check + composer audit (backend)
   - npm ci + npm run check + npm run e2e (frontend)
   - python -I _restructure/build_decision_index.py --check (docs)
   Sayıları §7 "Doğrulama" tablosuna yaz.
2. Backend FAZ-21.md: "Faz 21 kapanış özeti" (madde tablosu, bloke olanlar, kapılar) + fazlar/README.md satırı. Commit.
3. Docs:
   - phases/README.md Faz 21 satırı ve klasör satırı
   - audits/2026-11-12-full-system-audit/README.md'ye "düşük bulguların durumu → phases/faz-21" notu
   - Bu sayfanın §6'sı ve §7'si
   - CHANGELOG
   Commit.
4. Üç depoda `git status --short` (temiz) ve `git log --oneline faz-20-critical-fixes..faz-21-backlog` çıktılarını rapora koy.
   Bütün commit'lerde ajan izi olmadığını göster:
   `git log faz-20-critical-fixes..faz-21-backlog --format=%B | grep -ciE "co-authored|claude|generated with"` → 0.
5. Raporu ver (§3 madde 15).
```

## 6. Çalışma notları (ajan doldurur)

*Bloke olanların nedeni, "gördüm, dokunmadım", plandan sapmalar, ölçümler.*

### 21.0

- Taban (27 Kasım, `faz-20-critical-fixes` ucu): `composer check` 1306/1306 (4765 assertion, 121,9 sn), `k18: 32 dosya, 0 ihlal`;
  `composer audit` temiz; `npm run check` çıkış 0 (31 hata kodu, i18n tabanı 781 parça / 65 dosya); `npm run e2e` 6/6.
- Vite (`npm run dev`) ve `php artisan serve` İsmail'in oturumunda açıktı. Bu yüzden `npm ci` yerine `npm install` koşuldu
  (§3 madde 2); dev sunucularına dokunulmadı.

### 21.1 (`SEC-16`)

- **Plandan sapma (küçük):** §A-2 "hesap kilitlenmez" sözünü gerçek kılmak için başarılı parola sıfırlama hesap kovasını
  boşaltıyor (`ResetPasswordAction`); planda yazmıyordu. Dolu kovada doğru parola da 429 alıyor; aksi hâlde kova hiçbir
  şeyi frenlemezdi (gerekçe K265).
- **Kapı sırasında çıkan:** tam takımda `OptimizeUploadedImageTest` 128 MB `memory_limit`'te düştü (iki dosya ayrı ayrı
  yeşil). Ölçüldü: süreç görsel testine ~93 MB kalıcı bellekle geliyordu. `phpunit.xml`'e test süreci için
  `memory_limit=256M` eklendi (backend `docs/rehber/phpunit.md` §5). Üç denemede yeşil: 1) PHPStan jenerik tipi,
  2) bellek, 3) yeşil (1318/1318).
- **Gördüm, dokunmadım:** `config/davetkart.php` `auth.login_rate_limit_per_minute` hiçbir yerde okunmuyor
  (`authLimits()` 5'i sabit yazıyor).

### 21.2 (`SEC-15`)

- **Plandan sapma yok, ama "ekle" adımı boş çıktı:** kayıt rotası zaten `throttle:auth` grubundaydı (adres + IP 5/dk,
  IP 20/dk; giriş ile ortak `auth` limiter'ı). Kod eklenmedi; kovalar üç testle kilitlendi (backend
  `RegistrationEnumerationBrakesTest`). Çakışma yolunda `Hash::make` atlanmıyor (`hashed` cast'i INSERT'ten önce).
- Frontend'e dokunulmadı (B yolu). `npm run check` koşulmadı: frontend değişmedi; `npm run e2e` 6/6.
- Gördüm, dokunmadım: `Hash::partialMock()` Laravel 13'te kurucusuz `HashManager` üretiyor ve gerçek hash'e geçemiyor
  (`Call to a member function get() on null`); testte `tests/Support/CountingHasher` kullanıldı.

### 21.3 (`FE-58`)

- **Plandan sapma:** plan "otomatik kalıyorsa kod değişmeyebilir" diyordu. "Tekrar ziyaret ikinci istek üretmez" testi
  bugünkü kodda kırmızı olurdu: bekçi yalnızca `useRef`'teydi, yenilemede sıfırlanıyordu. Panelde "Yayından kaldır"
  olduğu için yenileme, kullanıcının kaldırdığı davetiyeyi sorulmadan yeniden yayınlayabiliyordu. Karar saf fonksiyona
  (`src/utils/autoPublish.ts`) taşındı, sekme belleği (`sessionStorage`) eklendi; tekrar ziyarette kart "Ödemeniz
  onaylandı" diyor (eski hâliyle `idle` → sonsuz "yayına alınıyor" olurdu).
- `PaymentReturnPage::cardViewFor` → `utils/autoPublish.ts::returnCardView` (test edilebilsin diye), `skipped` kolu eklendi.
- Kapılar: `npm run check` çıkış 0 (31 kod, i18n 781/65 değişmedi), `npm run e2e` 6/6; `verify:payment` 19 yeni denetim,
  7 mutant öldü.
- Gördüm, dokunmadım: başka sekmede ya da yeni oturumda aynı dönüş adresi yine istek atar; tam kapatma için
  `GET /orders/{id}` yanıtına `orders.first_published_at` bilgisi gerekir (backend + sözleşme, ayrı iş).

### 21.4 (`OPS-08`)

- Frontend'e dokunulmadı (§A-1: zarf aynı; hata bildiriminde kimliği göstermek ayrı iş). `npm run e2e` 6/6.
- Plandaki "≤64 karakter" sınırı ayrı bir kontrol olarak yazıldı, mutant yaşadı (ULID/UUID biçimi uzunluğu zaten
  sınırlıyor); kontrol kaldırıldı, test vakası kaldı.
- İki denemede yeşil: 1) PHPStan (`Log::channel()` dönüş tipi), 2) yeşil (1335/1335).
- İsmail'e kalan sunucu adımı: nginx `log_format` içine `rid=$upstream_http_x_request_id` (backend
  `docs/rehber/app/Http/Middleware/AssignRequestId.md` §6). Koşulmadı.

## 7. Doğrulama ve kalanlar (21.90'da doldurulur)

| Kapı | Sonuç (görülen çıktı) |
|---|---|
| Backend `composer check` | |
| Backend `composer audit` | |
| Frontend `npm run check` | |
| Frontend `npm run e2e` | |
| Karar indeksi `--check` | |
| Ajan izi taraması (üç depo) | |

**Bu klasördeki dosyalar:** `README.md` (bu sayfa) · `FAZ-21-ARC-08-KOMUTLARI.md` (21.17'de açılır).

**İsmail'e kalan:** *(21.90'da numaralı liste)*
