# PROMPT — FAZ 18.2: `OPS-02` Veritabanı yedeği ve geri yükleme provası yok

> **Hazırlanma:** 16 Kasım 2026 · **Denetim:** `AUD-2026-11-12` ([`REPORT.md`](../audits/2026-11-12-full-system-audit/REPORT.md) §4) · **Sıra:** 2/6
> **Önkoşul:** 18.1 (`OPS-01`) düzeltme dalı backend'de `faz-18-audit-fixes`'e birleşmiş olmalı.
> **Dokunulan depolar:** backend (`deploy/`) · docs
> **Kullanım:** `---` çizgisinden sonrasının tamamını Claude Code'a (Windows, `D:\Projects\davetkart`) yapıştır. §A varsa önce onu sen yap.


---

Merhaba. DavetKart projemde (backend PHP 8.5 + Laravel 13, modüler monolit + Action katmanı; frontend React 19 + TypeScript) **Faz 18: denetim düzeltmeleri** yapıyoruz. 12–15 Kasım 2026 genel sistem denetimi (`AUD-2026-11-12`) altı yüksek (🟠) bulgu çıkardı; her biri ayrı bir dalda, ayrı bir prompt'la kapanıyor. Bu prompt **yalnızca `OPS-02`** bulgusunu kapatır: *Veritabanı yedeği ve geri yükleme provası yok*. Bu, altı bulgunun 2. sırası.

## 0. Çalışma biçimi (bağlayıcı)

1. **Bütün adımları (18.2.1 → sonuncusu) tek seferde, durmadan uygula.** Adımlar arasında onay bekleme; yalnızca §8'deki durumlarda dur. Proje talimatındaki "her dosyadan sonra dur" kuralı bu fazda askıda; **açıklama yükümlülüğü sürüyor** (§7 kılavuzları, §10 rapor).
2. 🔴 **Git yazma işlemi YASAK:** `git add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `restore`, `checkout -- <dosya>`. İzinli olanlar: `fetch`, `status`, `log`, `diff`, `show`, `branch` listesi, `merge-base`; §2'deki dalları `git switch -c` ile açmak ve var olan dala `git switch` ile geçmek. **Commit'leri ben atacağım;** sen §9'daki komutları hazırlarsın.
3. **Tek bulgu = tek dal.** Bu dalda yalnızca `OPS-02` kapsamındaki değişiklik olur. Başka bir bulguya ait sorun görürsen düzeltme; §10 raporunda "gördüm, dokunmadım" altında yaz.
4. **Dosya sahipliği:** her dosya tek bir adıma ait. Bir dosyaya ikinci kez dokunman gerekirse o değişikliği sonraki adımın commit'ine taşı ve raporda belirt.
5. **Kalite kapısı:** her backend adımından sonra `vendor/bin/pint --test`, `vendor/bin/phpstan analyse --memory-limit=1G` ve ilgili testler. En sonda tam `composer check`. Frontend'e dokunduysan en sonda `npm run check`.
6. 🔴 **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma. Koşmadıysa "koşmadı" ve nedenini yaz.
7. **K18 — açıklamanın yeri:** koddaki yorumlar 1–3 satır. Her yeni ya da anlamlı ölçüde değişen dosya için kod deposunda `docs/rehber/<aynı-yol>.md` kılavuzunu yaz/güncelle. Okuyucu öğrenen biri: neden bu yaklaşım, hangi tasarım deseni, hangi saldırı ya da hata türüne karşı, sık yapılan hatalar, nasıl denenir (tinker/komut). Kılavuz kendi kod dosyasının commit'ine girer.
8. **Mimariye uy:** SOLID, Clean Code, Laravel ve React standartları; mevcut desenler (Action katmanı, enum durumlar, para tam sayı kuruş, `lockForUpdate` + transaction, hata sözleşmesi). Yeni hata kodu gerekirse `contracts/error-codes.json` + `php artisan errors:export` + frontend çevirisi aynı bulgunun dalında.
9. **Dil:** Türkçe yaz. Commit mesajları İngilizce: kod depolarında `18.2.<adım> - <tür>(<alan>): <Fiil> ...`, docs deposunda `docs(<alan>): <Fiil> ...`.
10. **Canlı sisteme hiçbir istek atma** (sunucu, Shopier, AWS, Sentry, GitHub API). Hiçbir dosyaya sır yazma.
11. **Frontend'de `git add -A` yasak** (CRLF tuzağı); commit komutlarında dosyalar tek tek, açık yolla.
12. **Plandan sapma:** §4'teki bir kararı yanlış bulursan önce gerekçesini yaz. §8 dur koşulu değilse en güvenli seçeneği uygula ve §10'da gerekçelendir.
13. **AWS konsol adımlarında** menü ve düğme adlarını iki dilde yaz: `English (Türkçe)` (ör. `Create bucket (Kova oluştur)`). Konsolu iki dilde kullanıyorum.

## 1. Başlamadan önce oku

**Ortak:**
1. `davetkart-docs\CLAUDE.md` · `davetkart-docs\context\PHP-LARAVEL-SETUP.md` (§2, §9, §11, §13) · `davetkart-docs\decisions\DECISION-INDEX.md`
2. `davetkart-backend-php-laravel\CLAUDE.md` · `davetkart-frontent\CLAUDE.md`
3. Denetim: `davetkart-docs\audits\2026-11-12-full-system-audit\REPORT.md` §1 ve §4'teki **`OPS-02`** tam metni · `davetkart-docs\audits\2026-11-12-full-system-audit\findings\05-operations.md` · ilgili bulgular: `OPS-03` (izleme), `SEC-11` (`02-security.md`: saklama süresi ve gizlilik) · kanıt: REPORT.md §4 `OPS-02` kanıt satırı
4. `davetkart-docs\phases\faz-18\README.md` (takip tablosu) · backend `docs\rehber\fazlar\FAZ-18.md` (varsa; önceki bulguların bölümleri)

**Bu bulguya özel:**
1. Docs: `operations/deployment/YAYIN-PLANI.md` (Y4.4 Lightsail görüntüleri, Y11.5 gece `pg_dump` → S3, Y11.6 geri yükleme provası; sunucu işletim sistemi, PostgreSQL sürümü, saat dilimi, kullanıcılar, S3 medya erişiminin nasıl çözüldüğü) · `YAYIN-DEVIR.md` (Y11) · `operations/deployment/YAYIN-SIRASI.md` (18.1'de yazıldı).
2. Backend: `deploy/` klasörünün tamamı ve `docs/rehber/deploy/*` (cron dosyasının sunucuya nasıl kurulduğu, `deploy.sh`'in neyi kopyaladığı) · `docs/10-URETIM-ENV-SABLONU.md` · `config/database.php`.

**Sıradaki boş K numarası:** `DECISION-INDEX.md` "K128" diyor ama `ARC-01`'e göre K128–K145 backend `docs/rehber/fazlar/FAZ-13.md` ve `FAZ-14.md`'de kullanılmış. Gerçek son numarayı bu kaynaklardan ve `davetkart-docs\decisions\addenda\PHP-LARAVEL-SETUP-EK-FAZ-18.md`'den (varsa) bul. Çakışma görürsen ⚠️ ile işaretle, numarayı bana bırak.

Okuduktan sonra **5–10 satırlık bir özet** ver: bulgunun koddaki bugünkü hâli (rapordaki satırlar hâlâ geçerli mi), §4'te hangi kolu seçtiğin, kullanacağın K numaraları. Sonra durmadan devam et.

## 2. Dallar ve önkoşul kontrolü

`<YYYY-MM-DD>` = dalı açtığın günün tarihi. Dal adları `davetkart-docs\CLAUDE.md` §4'teki biçimde.

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git fetch origin
git status --short                                   # boş değilse DUR
git switch faz-18-audit-fixes                        # yoksa DUR (18.1 / OPS-01 yapılmamış)
git branch --merged faz-18-audit-fixes | Select-String "ops-01-"   # boşsa DUR: OPS-01 birleşmemiş
git switch -c fix/<YYYY-MM-DD>-ops-02-db-backup

# Frontend: bu bulguda değişmez. §1'deki okuma için `git show faz-18-audit-fixes:<yol>` kullan; dal açma.

cd D:\Projects\davetkart\davetkart-docs
git status --short                                   # boş değilse DUR
git switch docs/2026-11-16-faz-18-audit-fixes                             # yoksa DUR
```

## 3. Bulgu (özet)

Tek yedek Lightsail'in günlük disk görüntüsü (son 7 gün, aynı hesapta). Mantıksal döküm yok, geri yükleme hiç denenmedi. Hatalı bir göç ya da elle `DELETE` siparişleri bozarsa tek tablo geri getirilemez; disk görüntüsüne dönmek aradaki ödemeleri ve LCV'leri de siler. Canlıda henüz müşteri verisi yok: bu açığı kapatmanın en ucuz anı şimdi.

**Dersin özü:** yedeğin iki ölçüsü var: **RPO** (ne kadar veri kaybedersin) ve **RTO** (ne kadar sürede dönersin). Disk görüntüsü "sunucu yandı"yı, mantıksal döküm "veri bozuldu"yu çözer; farklı felaketlerdir. **Denenmemiş yedek bir umuttur:** geri yükleme provası yedeğin testidir.

## 4. Kararlar (sıradaki boş K numaralarını sen ver)

| # | Karar |
|---|---|
| D1 | **Biçim:** `pg_dump -Fc` (sıkıştırılmış, `pg_restore -t` ile tek tablo geri yüklenebilir). Her gece 02:00 UTC (sunucu saat dilimini plandan doğrula; cron.d sistem saatini kullanır). Çakışan koşu `flock` ile engellenir. |
| D2 | **Hedef:** uygulamanın medya bucket'ından **ayrı** bir S3 bucket'ı. Block Public Access açık, sürümleme açık, sunucu tarafı şifreleme (SSE-S3), ömür kuralı: 30 gün sonra sil (eski sürümler 7 gün). Bucket adını ben seçerim; dosyalara yer tutucu yaz. |
| D3 | **En az yetki:** sunucudaki yedek kimliği **yalnızca yazabilir** (`s3:PutObject` yedek önekine); okuyamaz, listeleyemez, silemez. Sunucu ele geçirilse bile saldırgan yedekleri silemez ya da okuyamaz. Geri yükleme benim kendi kimliğimle yapılır. IAM politikası JSON'u çalıştırma kitabına girer (sır değil). Lightsail örneği IAM rolü taşıyamıyorsa (plan kaydındaki medya erişimine bak) erişim anahtarı yalnızca root'un okuyabildiği bir dosyada durur (`600`); depoya ve günlüğe asla girmez. |
| D4 | **Veritabanı kimliği:** parola komut satırına ya da betiğe girmez. Plandaki kullanıcı yapısına göre `postgres` sistem kullanıcısıyla peer kimlik doğrulama **ya da** `.pgpass`; birini seç, gerekçesini K'ya yaz. |
| D5 | **Betik (`deploy/backup/pg-dump.sh`):** `set -euo pipefail`, `umask 077`, geçici dizin + `trap` ile temizlik; döküm → `pg_restore --list` ile dosyanın okunabildiğini doğrula → boyut > 0 → aynı anda önemli tabloların satır sayılarını (`users`, `invitations`, `orders`, LCV tablosu; gerçek adları koddan al) bir `manifest.json`'a yaz → ikisini `aws s3 cp --sse AES256` ile `daily/YYYY/MM/DD/` önekine yükle → her adımı günlüğe yaz → herhangi bir hatada sıfır dışı çıkış. `DRY_RUN=1` (ya da `--local <dizin>`) kipinde S3 yerine yerel dizine yazar. Yeni bağımlılık yok (`pg_dump`, `aws` CLI, `flock`, `curl`). |
| D6 | **İzleme (asgari):** betik bittiğinde, ortam dosyasında bir kalp atışı adresi tanımlıysa (`BACKUP_HEARTBEAT_URL`, ör. Sentry Crons) `curl` ile başarı/başarısızlık bildirir; tanımlı değilse yalnızca günlük. Tam izleme ve alarm `OPS-03`'ün işi. |
| D7 | **Kabul ölçütü:** kayıt açılmadan önce bir kez geri yükleme provası yapılmış ve süresi (RTO) plana yazılmış olmalı. RPO = 24 saat bilinçli olarak kabul edilir; daha küçük RPO (WAL arşivi / PITR) ileride ayrı karar. |

## 5. Adımlar ve dosya sahipliği

### Backend (`fix/<YYYY-MM-DD>-ops-02-db-backup`)
| Adım | İş | Dosyalar |
|---|---|---|
| 18.2.1 | D1–D6: yedek betiği + kılavuzu. | `deploy/backup/pg-dump.sh`, `docs/rehber/deploy/backup/pg-dump.md` |
| 18.2.2 | Cron satırı (yedek, ayrı dosya; mevcut `deploy/cron/davetkart`'ın kurulum yolunu izle) + kılavuzu. Kurulum adımı `deploy.sh`'in kapsamındaysa oraya, değilse çalıştırma kitabına. | `deploy/cron/davetkart-backup` (ya da desene uyan ad), `docs/rehber/deploy/cron/...md` |
| 18.2.3 | Geri yükleme provası betiği (Windows'ta benim çalıştıracağım; PowerShell ya da Git Bash, hangisi daha az bağımlılık gerektiriyorsa): S3'ten indir → `createdb davetkart_restore_drill` → `pg_restore --no-owner --no-acl` → `manifest.json`'daki sayılarla karşılaştır → süreyi yaz → çıkışta tabloları farklıysa sıfır dışı. Tek tablo kurtarma (senaryo A) için ayrı bölüm: yan veritabanına `pg_restore -t orders`, sonra elle karşılaştırma. | `deploy/backup/restore-drill.*`, kılavuzu |
| 18.2.4 | `FAZ-18.md` `## 18.2 — OPS-02`. | `docs/rehber/fazlar/FAZ-18.md` |

### Docs (`docs/2026-11-16-faz-18-audit-fixes`)
| Adım | İş |
|---|---|
| 18.2.5 | `operations/deployment/YEDEK-VE-GERI-YUKLEME.md` (yeni): bucket kurulumu (konsol adımları **English (Türkçe)**), IAM politikası JSON'u, sunucuya kurulum komutları, ilk elle koşu ve doğrulama, aylık prova takvimi, `pg_restore` sürüm uyumu notu (yereldeki PostgreSQL 18.4, sunucununki ≥ olmalı; plandan kontrol et). `YAYIN-PLANI.md`'de Y11.5 ve Y11.6'ya bu dosyaya bağlantı ver (geçmiş satırları yeniden yazma, yalnızca bağlantı/durum). `YAYIN-SIRASI.md` kontrol listesindeki yedek maddesine bağlantı. §7'deki ortak kayıtlar. |

## 6. Testler ve kalite kapısı

- `bash -n deploy/backup/pg-dump.sh` ve `shellcheck` (varsa). Yoksa "koşmadı".
- **Yerel kuru koşu:** `DRY_RUN=1` ile yerel geliştirme veritabanına karşı (Git Bash + PostgreSQL araçları PATH'teyse) döküm → `pg_restore --list` → manifest. Ardından 18.2.3'ün betiğiyle bu yerel dökümü `davetkart_restore_drill`'e geri yükle ve sayıları karşılaştır. Koşabildiğin kadarını koş; kalanını "koşmadı" diye yaz. Prova veritabanını sonda bırak, silme komutunu raporda ver.
- **Mutant:** betikte `pg_restore --list` doğrulamasını kaldır ve bozuk (boş) bir dosya ver → betik yine de başarı dönüyorsa doğrulama işe yarıyor demektir; kaldırınca sessizce geçtiğini, geri koyunca kırmızı olduğunu göster.
- PHP değişmiyorsa `composer check` gerekmez; yine de sonda bir kez koş ve sonucunu yaz (dalın sağlığı).

## 7. Kayıt (dokümantasyon)

**Kod deposu (backend, bu dalın içinde):**
- `docs/rehber/fazlar/FAZ-18.md`: yoksa oluştur (başlık: "Faz 18 — denetim düzeltmeleri (`AUD-2026-11-12`)", altı bulgunun tablosu). `## 18.2 — OPS-02` bölümünü ekle: sorun (bir paragraf), kararlar (K numaraları), değişen dosyalar, eklenen testler ve öldürdükleri mutantlar, doğrulama durumu (B7 tablosu), benim elle yapacağım doğrulama adımları. Bu dosya bu bulgunun **son** backend commit'ine girer.
- Değişen her kod dosyasının `docs/rehber/<aynı-yol>.md` kılavuzu (kural 7).

**Docs deposu (`davetkart-docs`, dal `docs/2026-11-16-faz-18-audit-fixes`; yoksa DUR):**
- `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`: yoksa oluştur; bu bulgunun kararlarını (K numarası, karar, gerekçe, geçersiz kıldığı karar) ekle.
- `decisions/DECISION-INDEX.md`: yeni K satırları + "Sıradaki boş numara". K128–K145 boşluğuna dokunma (`ARC-01` ayrı bir iş); tablonun üstüne ⚠️ notu yoksa ekle.
- `phases/faz-18/README.md`: `OPS-02` satırında durum `kod ✅ · commit bekliyor`, dal adı, K numaraları.
- `phases/faz-18/FAZ-18-OPS-02-COMMIT-KOMUTLARI.md`: §9'daki komutların tamamı.
- `CHANGELOG.md`: tarihli tek satır. Klasöre dosya eklediysen o klasörün `README.md`'si.
- 🔴 Denetim raporunu (`audits/…`) **değiştirme**; geçmiş rapordur.

## 8. Dur ve sor

Aşağıdakilerden biri olursa işi o noktada bırak, durumu ve seçenekleri yaz, cevabımı bekle:
- §2'deki önkoşul kontrolü başarısız (çalışma ağacı kirli, beklenen dal ya da birleştirme yok).
- Kod raporun anlattığından belirgin biçimde farklı (bulgu zaten kapanmış, dosyalar taşınmış, varsayım tutmuyor).
- Kalite kapısı senin değişikliğin dışındaki bir nedenle kırmızı ve bu bulgunun kapsamında düzeltilemiyor.
- Yeni bir Composer ya da npm bağımlılığı gerekiyor.
- Bir karar para, müşteri verisi ya da yayındaki sistem hakkında geri alınamaz bir sonuç doğuruyor.
- Plan kaydına göre veritabanı Lightsail örneğinde değil (yönetilen veritabanı, RDS vb.): tasarım değişir, sor.
- Sunucuda `aws` CLI ya da `pg_dump` kurulumu plan dışı bir paket gerektiriyor: kurulum komutunu yaz, kararı bana bırak.


**Kapsam dışı:** `OPS-03` (izleme ve alarmın tamamı), `SEC-11` (gizlilik metninde yedek saklama süresi; raporda an), WAL/PITR.

## 9. Commit komutları (sen hazırla, ben çalıştırırım)

- Her adım **ayrı bir PowerShell bloğu**: `cd <depo>` → `git switch <dal>` (doğru dalda olduğumu garantile) → dosyalar **tek tek, açık yolla** `git add` → `git commit -m "18.2.<adım> - ..."` → `git status --short`.
- Joker (`*`), klasör yolu ve `-A` yok. Kılavuz md'si kendi kod dosyasıyla aynı blokta.
- Sıra: backend blokları → frontend blokları → docs bloğu.
- En sona **birleştirme bloğu**: yalnızca backend için: `git switch faz-18-audit-fixes` → `git merge --no-ff <fix-dalı> -m "Merge OPS-02 fix into faz-18-audit-fixes"` → `git status --short`. Ardından isteğe bağlı `git push -u origin <dal>` satırları (yorum olarak, `#` ile).
- Aynı komutları `davetkart-docs\phases\faz-18\FAZ-18-OPS-02-COMMIT-KOMUTLARI.md`'ye yaz ve §10 raporunda da göster.

## 10. Rapor (en sonda, tek mesaj)

1. **Ne değişti:** adım adım (18.2.1 …), her adımın dosyaları.
2. **Kararlar:** K numaralarıyla, birer cümle.
3. **B7 tablosu:** komut · sonuç · çıktıdan kısa alıntı. Koşmayan her şey "koşmadı" + neden.
4. **Mutant denemesi:** §6'daki mutant(lar)ı elle uygula → ilgili testin kırmızıya döndüğünü gör → kodu geri al → `git diff --stat` ile geri alındığını göster. Sonucu yaz.
5. **Gördüm, dokunmadım:** kapsam dışı kalan sorunlar (bulgu kimliğiyle, varsa).
6. **Commit komutları:** §9'daki bloklar.
7. **Öğretici özet (5–10 satır):** bu bulgunun dersi; seçilen desen ve neden; benzer hatayı ileride nasıl tanırım.
8. **Bana kalan elle işler:** (sunucu, panel, AWS, deneme) varsa numaralı liste.
