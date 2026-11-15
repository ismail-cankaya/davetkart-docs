# PROMPT — FAZ 18.1: `OPS-01` Yayına çıkacak commit belirsiz; iki depo ayrı yükseltilirse 19 premium şablon korumasız

> **Hazırlanma:** 16 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §4) · **Sıra:** 1/6
> **Önkoşul:** Bu prompt'lar `davetkart-docs` deposunda `docs/2026-11-16-faz-18-audit-fixes` dalına commit'lenmiş olmalı. §A'yı sen yap.
> **Dokunulan depolar:** backend · frontend · docs
> **Kullanım:** `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır. §A varsa önce onu sen yap.

## §A — Senin önceden yapacakların (prompt'u yapıştırmadan önce)

Faz 18'in **entegrasyon dalı** `faz-18-audit-fixes`. Denetlenen en yeni kod (`origin/ccr-9a346997-bu6gve`) üstüne kurulur; frontend'de `main`'deki `47aedc8` (bağımlılık temizliği, `SEC-14`) içine alınır. Altı düzeltme dalı bu daldan açılıp buna birleşir; faz sonunda bu dal `main`'e gider (18.6 §11).

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş olmalı
git switch -c faz-18-audit-fixes origin/ccr-9a346997-bu6gve
git log --oneline -1                                 # d810410 17.1 - feat(paywall) ... beklenir

cd D:\Projects\davetkart\davetkart-frontent
git fetch origin
git status --short                                   # yalnızca '?? .claude/' olmalı
git switch -c faz-18-audit-fixes origin/ccr-9a346997-bu6gve
git merge --no-ff origin/main -m "Merge main (47aedc8 dependency cleanup) into faz-18-audit-fixes"
# Çakışma çıkarsa birleştirmeyi YARIDA BIRAK (abort etme) ve prompt'u yapıştır; ajan çözer (§2).
git status --short
```

---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 18: denetim düzeltmeleri** yapıyoruz. 12–15 Kasım 2026 genel sistem denetimi (`AUD-2026-11-12`) altı yüksek (🟠) bulgu çıkardı; her biri ayrı bir dalda, ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `OPS-01`** bulgusunu kapatır: *Yayına çıkacak commit belirsiz; iki depo ayrı yükseltilirse 19 premium şablon korumasız*. Bu, altı bulgunun 1. sırası.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (18.1.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `restore`, `checkout -- <dosya>`. İzinli olanlar: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `OPS-01` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler. En sonda tam `composer check`. Frontend'e dokunduysan en sonda `npm run check`.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `18.1.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula ve §10'da gerekçelendir.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md`
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\REPORT.md` §1 ve §4'teki **`OPS-01`** tam metni · `davetkart-docs\audits\2026-11-12-full-system-audit\findings\05-operations.md` · ilgili bulgular: `TST-01` (`03-testing.md`), `FE-05` (`04-frontend-e2e.md`), `SEC-14`, `SEC-07` (`02-security.md`), `ARC-02`, `ARC-08` (`01-architecture.md`) · kanıt: `evidence\commands\OPS-branch-state.txt`, `TST-composer-check.txt`, `FE-d1-metrics.txt` §5
4. `davetkart-docs\phases\faz-18\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-18.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Backend: `config/davetkart.php` (`tiers`, `module_tiers`, `preset_tiers`, `branding.white_label_tier`) · `errors:export` komutunun kendisi ve `contracts/error-codes.json` (kopyalayacağın desen) · `composer.json` `check` betiği · `deploy/deploy.sh`, `deploy/deploy-frontend.sh` ve kılavuzları · `tests/Feature/TemplateCatalogueTest.php` · `docs/rehber/fazlar/FAZ-15.md` §3.
2. Frontend: `src/data.ts` (`minimumTier`, fiyat kartı özellik matrisi) · `src/stores/useSubscriptionStore.ts` (`getRequiredTier`) · `src/contracts/errorCodes*` ve `scripts/verify-error-contract.ts` (backend sözleşmesinin frontend'e nasıl taşındığı) · `scripts/run-check.mjs` · `package.json` `verify` zinciri.
3. Docs: `operations/deployment/YAYIN-PLANI.md` (Y8.2a, Y10) ve `YAYIN-DEVIR.md`.

**Sıradaki boş K numarası:** `DECISION-INDEX.md` "K128" diyor ama `ARC-01`'e göre K128–K145 backend `docs/rehber/fazlar/FAZ-13.md` ve `FAZ-14.md`'de kullanılmış. Gerçek son numarayı bu kaynaklardan ve `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`'den (varsa) bul. Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (rapordaki satırlar hâlâ geçerli mi), §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-18-audit-fixes                        # yoksa DUR (§A yapılmamış)
git rev-parse --short HEAD                           # d810410 değilse DUR
git switch -c fix/<YYYY-MM-DD>-ops-01-release-alignment

cd D:\Projects\davetkart\davetkart-frontent
git fetch origin
git status --short                                   # yalnızca '?? .claude/' olabilir; başka satır varsa DUR
git switch faz-18-audit-fixes                        # yoksa DUR
git log --oneline -5                                 # önceki bulgular frontend'e dokunduysa birleştirmeleri burada görünür
git switch -c fix/<YYYY-MM-DD>-ops-01-release-alignment

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-16-faz-18-audit-fixes                             # yoksa DUR
```

**18.1.0 — yalnızca §A'daki birleştirme çakışmayla yarıda kaldıysa:** `package.json` ve `package-lock.json` çakışmasını çöz: `47aedc8`'in değişikliği (kullanılmayan `express`, `dotenv`, `@types/express` gider; `vite`, `@vitejs/plugin-react`, `@tailwindcss/vite` `devDependencies`'e taşınır) **ve** dalın kendi değişiklikleri birlikte kalsın. Kilit dosyasını elle birleştirme; `package.json` çözülünce `npm install` ile yeniden üret. `npm ci` → `npm run check` koş. Birleştirme commit'inin komutunu ver (dosyalar tek tek) ve **DUR**: düzeltme dalı ancak bu commit'ten sonra açılabilir.

## 3. Bulgu (özet; tam metin REPORT.md §4)

Backend `main` = `03d3940`, denetlenen dal 4 commit ileride (Faz 16–17 `preset_tiers`: 13 → 32 Gold şablon). Frontend denetlenen dal `main`'den 71 commit ileride, 1 geride (`47aedc8`). İki depoda etiket yok. Frontend'in yeni şablonları backend'in dört commit'inden önce yayına çıkarsa arayüz 32 şablonu "Gold+" gösterir, sunucu yalnızca 13'ünü tanır ve Standart planla premium şablon yayınlanır (şablon başına 150 ₺). Ayrıca kalite kapısı bu dalda kırmızı (`TST-01`, Pint), yani bugün "doğrulanmış commit" hiçbir dalda yok.

**Dersin özü:** iki depo tek ürünün iki yarısıysa aralarındaki sözleşme (hangi şablon hangi planda) **tek kaynaktan** üretilmeli ve **dağıtım sırası** bir doğruluk koşuludur: kuralı uygulayan sunucu önce, kuralı gösteren arayüz sonra. "Hangi iki commit birlikte doğrulandı" sorusunun tek dürüst cevabı **etiket**tir.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | **Plan kuralları sözleşmesi:** tek kaynak backend `config/davetkart.php`. `php artisan plans:export` → `contracts/plan-rules.json` (plan sırası, plan başına LCV sınırı, `module_tiers`, `preset_tiers`, `white_label_tier`; **fiyat yok**, fiyat K128'le API'den gelir). Anahtarlar sıralı, çıktı deterministik. `--check` kipi dosya bayatsa çıkış 1. `composer check` zincirine `errors:export --check`'ten hemen sonra girer. Desen birebir `errors:export` (hata sözleşmesi) ile aynı. |
| D2 | **Frontend denetimi:** `npm run verify:plans` → backend sözleşmesini frontend'in kullandığı kurallarla karşılaştırır: (a) `src/data.ts`'teki `minimumTier` kimlikleri ↔ `preset_tiers` (iki yönde), (b) fiyat kartı özellik matrisi ↔ `module_tiers` ve LCV sınırı, (c) `getRequiredTier` ↔ sözleşme. Sözleşmenin frontend'e taşınma biçimi `errorCodes` ile **aynı** olsun (kopya mı, kardeş depodan okuma mı: mevcut deseni oku, ona uy). `verify` zincirine eklenir. |
| D3 | **Dağıtım sırası:** önce backend (`main` → `deploy.sh`), sunucuda `plans:export --check` yeşil ve yeni kural etkinken frontend (`main` → Y10). Tersine sıra yasak. |
| D4 | **Sürüm etiketle izlenir, dalla değil.** İki depo aynı etiketi taşır (`vMAJOR.MINOR.PATCH`; Faz 18 sonu `v1.1.0`). `deploy.sh` (ve frontend dağıtımı ayrı günlük tutuyorsa `deploy-frontend.sh`) yayınlanan commit'in yanına `git describe --tags --exact-match` çıktısını ya da `etiketsiz` yazar. Etiketsiz commit **uyarı** verir, dağıtımı durdurmaz (ilk sürümde katı kural fazla; kararı sonra sıkılaştırırız). |
| D5 | `TST-01` (🟡) bu bulgunun önkoşulu olarak burada kapanır: kalite kapısı kırmızıyken D1'in `--check` adımı hiç koşmaz. |

## 5. Adımlar ve dosya sahipliği

### Backend (`fix/<YYYY-MM-DD>-ops-01-release-alignment`)
| Adım | İş | Dosyalar |
|---|---|---|
| 18.1.1 | `TST-01`: `vendor/bin/pint tests/Feature/TemplateCatalogueTest.php` (sabit metotlardan önceye taşınır). Sonra **tam** `composer check`. 1056 testin yeşil olduğunu görmeden 18.1.2'ye geçme. | `tests/Feature/TemplateCatalogueTest.php` |
| 18.1.2 | D1: `plans:export` komutu + `contracts/plan-rules.json` + test (`--check` bayat dosyada 1, güncel dosyada 0; çıktı deterministik; bir `preset_tiers` satırı değişince `--check` kırmızı) + `composer.json` `check` zinciri + kılavuzlar. | komut sınıfı, `contracts/plan-rules.json`, test, `composer.json`, `docs/rehber/...` |
| 18.1.3 | D4: `deploy/deploy.sh` (gerekirse `deploy-frontend.sh`) etiket günlüğü + kılavuzları. Sözdizimi: `bash -n` (Git Bash varsa; yoksa "koşmadı"), `shellcheck` varsa. | `deploy/deploy.sh`, `docs/rehber/deploy/deploy.md` (+ frontend betiği) |
| 18.1.4 | `docs/rehber/fazlar/FAZ-18.md` oluştur + `## 18.1 — OPS-01` bölümü. | `docs/rehber/fazlar/FAZ-18.md` |

### Frontend (`fix/<YYYY-MM-DD>-ops-01-release-alignment`) — 🔴 `git add -A` yasak
| Adım | İş | Dosyalar |
|---|---|---|
| 18.1.5 | D2: sözleşmenin frontend kopyası/okuyucusu + `scripts/verify-plan-rules.ts` + `package.json` (`verify:plans`, `verify` zinciri) + `docs/rehber/scripts/verify-plan-rules.md`. | listede |

### Docs (`docs/2026-11-16-faz-18-audit-fixes`)
| Adım | İş |
|---|---|
| 18.1.6 | `operations/deployment/YAYIN-SIRASI.md` (yeni): D3 ve D4 için çalıştırma kitabı. Yayın öncesi kontrol listesi: backend `composer check` yeşil · `composer audit` yeşil (`SEC-07`) · frontend `npm run check` yeşil (içinde `verify:plans`) · iki depoda aynı etiket · yedek alınıyor (`OPS-02`). Etiket komutları (Faz 18 sonunda **ben** çalıştıracağım, sen değil). Geri alma: önceki etikete dönüş. `operations/deployment/README.md`'ye satır. §7'deki ortak kayıtlar. |

## 6. Testler ve kalite kapısı

- 18.1.2 testi: `the_plan_rules_contract_is_up_to_date` (ya da deseninle uyumlu bir ad). **Öldürmesi gereken mutant:** `config/davetkart.php`'den bir `preset_tiers` satırını sil → `plans:export --check` ve test kırmızı.
- 18.1.5: **mutant:** frontend sözleşme kopyasından (ya da `data.ts`'ten) bir premium kimliğini sil → `npm run verify:plans` kırmızı. İkinci mutant: fiyat kartında Gold'un galeri satırını `included: true` yap → kırmızı.
- Sonda: backend tam `composer check`; frontend `npm ci` + `npm run check`.

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-18.md`: yoksa oluştur (başlık: "Faz 18 — denetim düzeltmeleri (`AUD-2026-11-12`)", altı bulgunun tablosu). `## 18.1 — OPS-01` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar, eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım doğrulama adımları. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).

**Docs deposu (`davetkart-docs`, dal `docs/2026-11-16-faz-18-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". K128–K145 boşluğuna dokunma (`ARC-01` ayrı bir iş); tablonun üstüne ⚠️ notu yoksa ekle.
- `phases/faz-18/README.md`: `OPS-01` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-18/FAZ-18-OPS-01-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**; geçmiş rapordur.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor).
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.
- §2'de backend `faz-18-audit-fixes` `d810410`'da değil (uzak dal ilerlemiş olabilir).
- `verify:plans` **bugün** iki taraf arasında bir fark buluyor (denetim fark bulmamıştı). Farkı bir tarafa "düzeltme": hangi şablonun hangi planda olduğu bir fiyat kararıdır; tabloyu göster ve sor.


**Kapsam dışı (dokunma, raporda an):** `SEC-07` (`composer audit`; etiketten önce kapanmalı), `ARC-02` (Faz 16–17 kaydı), `ARC-08` (dal temizliği), `FE-05`'in API'ye dayalı tam çözümü.

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` → `git commit -m "18.1.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Sıra: backend blokları → frontend blokları → docs bloğu.
- En sona **birleştirme bloğu**: backend ve frontend için ayrı ayrı: `git switch faz-18-audit-fixes` → `git merge --no-ff <fix-dalı> -m "Merge OPS-01 fix into faz-18-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-18\FAZ-18-OPS-01-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (18.1.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili testin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, deneme) varsa numaralı liste.
