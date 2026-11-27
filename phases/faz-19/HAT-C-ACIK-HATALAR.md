# Hat C — açık hatalar ve eksikler (Faz 19 ortak düzeltme dalı için)

> İsmail'in isteği (22 Kasım 2026): Hat C'de görülen, bulgunun kapsamı dışında kalan hatalar burada toplanır.
> **25 Kasım 2026 güncellemesi:** Hat C'nin bütün işleri (19.2–19.4, 19.7–19.9, 19.16, 19.90, 19.28) bitti. Hatlar
> bundan sonra hataları **tek bir Faz 19 düzeltme dalında** birlikte kapatacak; bu dosya Hat C'nin girdisidir.
> Her madde: ne · kanıt · önerilen düzeltme · durum. Numaralar korunur (eski numaralara başka yerden atıf var).
> **25 Kasım 2026, ortak düzeltme:** kod ve doküman maddelerinin hepsi kapandı (19.91.1–19.91.9, `faz-19-fix`'e birleşti);
> `composer check` uçtan uca yeşil (§E). Açık kalanlar yalnızca İsmail'in kararı/eylemi (#21, #28, #29, #31, #5, #6, §D).
> Komutlar: [`FAZ-19-HAT-C-FIX-COMMIT-KOMUTLARI.md`](FAZ-19-HAT-C-FIX-COMMIT-KOMUTLARI.md).

## Öncelik sırası (önerilen)

1. **#11 + #1 + #12** (PHPStan): `composer check` bunlar yüzünden kırmızı → `v1.2.0` yok, CI'da `k18:check` hiç koşmuyor (#18).
2. **#13** (`OPS-03` kılavuzları): Hat C'nin kendi K18 borcu; ilk dokunuşta `k18:check` zaten isteyecek.
3. **#2, #21** (sürüm etiketleri), sonra geri kalan kod/doküman kalitesi (#14–#20).
4. İsmail'in elle işleri (#8, #9, #10, #22–#26).

## A. Kalite kapısı (🔴 yayını engelliyor)

| # | Ne | Kanıt | Önerilen düzeltme | Durum |
|---|---|---|---|---|
| 11 | 🔴 PHPStan iç hatası: `Internal error: Class mixed was not found … discovering symbols is probably not configured properly` | Analiz edilen dosya koşudan koşuya değişiyor: 19.7'de `MaintenanceTest.php`, 19.16'da `TemplateCatalogueTest.php` ve `PurgeExpiredData.php`'nin HEAD hâli, 19.9 ve 19.28'de (25 Kas) yine `TemplateCatalogueTest.php`. Belirli bir dosyaya bağlı değil. Yeni `vendor` (larastan 3.10.0, phpstan 2.2.7, Laravel 13.43). Çökünce aynı koşunun başka hataları da raporlanmıyor | `vendor/bin/phpstan analyse -v --error-format=table tests/Feature/TemplateCatalogueTest.php` ile yığın izi (ajan biçimlendiricisi gizliyor). Olası kaynaklar: bir PHPDoc'ta `mixed`'in sınıf adı gibi çözülmesi, larastan/phpstan sürüm uyumsuzluğu (`composer why-not`, bir alt/üst yama sürümü dene), sonuç önbelleği (`phpstan clear-result-cache`). Çözüm `ignoreErrors` olmasın | ✅ kapandı (19.91.1) · kök neden: `tmpDir` yoktu, sonuç önbelleği bütün worktree'lerde ortak `%TEMP%\phpstan`'daydı (Hat A H3, Hat B B-H7). `tmpDir: storage/phpstan` ile tam koşu çökmeden bitti; `ignoreErrors` yok. Hat B de aynı düzeltmeyi (B-H7) birleştirdi; birleşik dalda onunki geçerli |
| 12 | 🔴 PHPStan tek dosya kipinde PHPDoc'u okumuyor gibi: her dosyada `missingType.property` (`$signature`), `missingType.iterableValue` (dönüşü `@return list<string>` ile yazılmış metotlarda bile) | 25 Kas: `phpstan analyse app/Console/Commands/CheckEnvTemplate.php app/Rules/PasswordPolicy.php` → 9 hata; mevcut, daha önce yeşil geçmiş dosyalar. Yeni dosyalarda da aynısı (`CheckK18.php`, `K18Inspector.php`) | #11 ile aynı kök olabilir (sembol keşfi/yapılandırma). #11 düzelince tek dosya koşusunu tekrarla; hâlâ varsa `phpstan.neon` `paths` dışı dosyalar için davranışı incele | ✅ kapandı (19.91.1) · aynı kök; `CheckEnvTemplate`, `PasswordPolicy`, `CheckK18`, `K18Inspector`, `TemplateCatalogueTest` tek dosya kipinde 0 hata |
| 1 | `cast.string` ×2: `(string) $id` | `app/Console/Commands/Concerns/ResolvesRefundRequests.php:29` (14.6'dan beri). #11 tam koşuyu çökerttiği için **bugün görünüp görünmediği bilinmiyor** | `is_string($id) ? $id : throw …` ile daralt (cast değil). `composer check` + `--filter=RefundCommandsTest` | ✅ kapandı (19.91.2) · `is_string` daraltması; birleşik dalda Hat B'nin (B-H1) eşdeğer hâli ve kılavuzu geçerli |
| 18 | 🔴 `k18:check` (K259) CI'da fiilen koşmuyor | `composer.json` `check` zincirinde PHPStan, `k18:check`'ten önce; PHPStan kırmızıyken zincir orada duruyor. Yerelde tek tek koşuldu (✅ 0 ihlal) | #11 çözülünce kendiliğinden düzelir. İstenirse sıra değişmez; ayrı CI adımı da düşünülebilir | ✅ kapandı · PHPStan yeşil, zincir `k18:check`'e ulaşıyor (bkz. #2) |
| 19 | Hat C'nin yeni kodu PHPStan'den **hiç** geçmedi | 19.9 (`PasswordPolicy`, `ValidationServiceProvider`), 19.16 (`PurgeExpiredData` değişikliği), 19.28 (`K18Inspector`, `CheckK18`, `K18CheckTest`), 19.7'nin bir kısmı. Testler yeşil (1271/1271) ama tip denetimi yok | #11 sonrası `composer check`; çıkan hataları aynı dalda düzelt | ✅ kapandı (19.91.3, 19.91.4) · tam koşuda 8 gerçek hata çıktı: `ResolvesRefundRequests` ×2, `ReadinessTest:175`, `CheckK18:29/38`, `K18CheckTest:84/90/99`; hepsi tipiyle düzeltildi → 0 |

## B. Hat C'nin kendi eksikleri (kod ve doküman)

| # | Ne | Kanıt | Önerilen düzeltme | Durum |
|---|---|---|---|---|
| 13 | `OPS-03` (19.7) sınıflarının 9'unun kılavuzu yok (K18) | Kılavuz yok: `app/Support/Health/{DatabaseCheck, DiskSpaceCheck, LocalDiskUsage, QueueBacklogCheck, RecordSchedulerHeartbeat, SchedulerHeartbeatCheck}.php`, `app/Contracts/{HealthCheck, DiskUsage}.php`, `app/Http/Controllers/Api/V1/ReadinessController.php`. Yalnızca `ReadinessProbe` ve bir klasör notu (`docs/rehber/app/Support/Health/`) var | Her dosyaya `docs/rehber/<aynı-yol>.md` (eşik, hangi hatayı yakalar, test, deneme). `k18:check <dosyalar>` → 0 | ✅ kapandı (19.91.5) · 9 kılavuz; `k18:check <9 dosya>` → 0 ihlal |
| 14 | 19.28 taşıma betiğinin kod özetleri yer yer kesik (`…`) | `routes/api.php` T4, T19 · `AppServiceProvider.php` P8 (üç satırın ikisi yarım cümle). Bilgi kaybı yok (tam metin kılavuzda) | Bu üç özeti elle bir cümleye indir | ✅ kapandı (19.91.6) · T4, T19, P8 tek tam cümle; başka kesik özet yok (`git grep '…$'` yalnızca bilinçli örnek URL'ler) |
| 15 | Taşınan notlarda biçim kaybı | `docs/rehber/routes/api.md` "Koddan taşınan notlar" T20 (girintili numaralı liste düz metne döndü), bazı bloklarda satır sonları paragraf oldu | T20 ve listeli blokları markdown listesine çevir | ✅ kapandı (19.91.7) · T19, T20 markdown listesi; T4/T19/T20'de 🔴/⚠️ satırları ayrı paragraf |
| 16 | `K18CheckTest` depo içine geçici dosya yazıyor | `the_command_passes_for_a_clean_file_and_fails_for_a_long_block`: `database/k18-<rastgele>.php`, `finally` ile siliniyor. Test süreci öldürülürse dosya kalır ve `k18:check`'i kırmızı yapar | Komuta `--root` seçeneği (yalnızca test) ya da `base_path()`'i geçici kökle değiştiren bir kurulum | ✅ kapandı (19.91.4) · kirli dosya geçici köke yazılıyor (`$this->app->setBasePath()`, `finally` ile geri), komuta seçenek eklenmedi |
| 17 | `K18Inspector` sınırları | Sondaki (`$x = 1; // …`) yorumlar sonraki satırlarla aynı bloğa girebiliyor; docblock'un hemen altındaki `//` bloğu docblock'la birleşiyor. Yanlış pozitif, yanlış negatif değil | Kod satırıyla aynı satırdaki yorumu blok başlatıcı sayma; test ekle | ✅ kapandı (19.91.4) · sondaki yorum blok başlatmıyor; docblock ile `//` ayrı blok. 2 test + 2 mutant (ikisi de kırmızı) |
| 20 | Kod tabanı geneli K18 envanteri yeni tanımla ölçülmedi | 19.28'de ölçüm betiği hata verdi; yalnızca denetimin `awk` ölçüsü var (kılavuzsuz 110 → 81; uzun bloklu 298/327, ama bu ölçü `/**` ve `*/`'yi de sayıyor) | `K18Inspector` ile bütün `app/ routes/ config/ database/` taraması → `FAZ-19.md` 19.28 tablosuna gerçek sayı | ✅ kapandı (19.91.8) · 338 dosya, kılavuzsuz 45, uzun bloklu 271 (568 blok), temiz 44 → backend `FAZ-19.md` 19.28 tablosu satır 6 |
| 27 | Parola formunda "yaygın parolalar kabul edilmez" ipucu yok | 19.9 sapma 6: `PasswordForm.tsx` gömülü Türkçe metin tabanı (`verify:i18n`) 5 → 6 olacağı için geri alındı. Kullanıcı kuralı ancak hata alınca öğreniyor | İpucunu `t()` ile çevirili ekle (tr/en), tabanı düşür | ✅ kapandı (19.91.9) · `auth.passwordHint` (tr/en). `verify:i18n` tabanı değişmedi (781): eski `hint` dizesi zaten sayılmıyordu, düşecek parça yok |
| 28 | Mevcut zayıf parolalı hesaplar zorlanmıyor | K258 / §A-3 varsayılanı: yalnızca yeni parola denetleniyor | İsmail kararı: girişte uyarı ya da bir sonraki değişiklikte zorlama | Karar bekliyor · İsmail |

## C. Sürüm, dal ve depo düzeni

| # | Ne | Kanıt | Önerilen düzeltme | Durum |
|---|---|---|---|---|
| 2 | `SEC-07` kapısı: yeni `vendor` ile `composer check` | 25 Kas: yeni `vendor` ile `composer audit` ✅, `php artisan test` ✅ 1271/1271; `composer check` ❌ (#11) | #11 sonrası `composer check`; K181 satırına sonuç | ✅ kapandı · `composer check` exit 0 (ayrıntı aşağıda §E) |
| 21 | Depolarda **hiç** sürüm etiketi yok | `git tag -l 'v1*'` boş (backend). `v1.0.0` (YAYIN-SIRASI §3 önerisi), `v1.1.0` (Faz 18 + `SEC-07`) ve `v1.2.0` (Faz 19) bekliyor | #11 sonrası sırayla: `main` birleştirme → etiketler (`FAZ-19-SEC-07-COMMIT-KOMUTLARI.md` §5, `FAZ-19-ARC-03-COMMIT-KOMUTLARI.md` §5–§7) | Açık · İsmail · **engel kalktı**: `composer check` yeşil (§E) · → **Faz 21.17 (27 Kas):** dal/worktree/etiket listesi ve komutlar [`../faz-21/FAZ-21-ARC-08-KOMUTLARI.md`](../faz-21/FAZ-21-ARC-08-KOMUTLARI.md) |
| 29 | Birleşmiş Hat C dalları silinmedi | Backend'de 7 Hat C `fix/…` dalı birleşik; docs'ta 34 `docs/…` dalı (bütün hatlar). Denetim `ARC-08` (dal hijyeni) ile aynı konu | Ortak dal birleştikten sonra `git branch -d` (yalnızca `--merged` olanlar) | Açık · → **Faz 21.17 (27 Kas):** dal/worktree/etiket listesi ve komutlar [`../faz-21/FAZ-21-ARC-08-KOMUTLARI.md`](../faz-21/FAZ-21-ARC-08-KOMUTLARI.md) |
| 30 | Hat C çalışma klasörleri dallarda kaldı | `davetkart-hat-c`: backend `fix/2026-11-24-arc-03-k18-ratchet`, docs bu dal, frontend ayrık `fe70b62` | Ortak dala geçerken `git switch`; ya da worktree'leri kaldır | ✅ kapandı · Hat C worktree'leri `fix/2026-11-25-hat-c-open-issues` (backend, frontend) ve `docs/2026-11-25-hat-c-fixes` dallarında |
| 31 | CI'da `fetch-depth: 0` gerçek GitHub koşusunda denenmedi | 19.28'de `ci.yml` değişti, push yok | İlk push'ta CI özetinde `k18:` satırını gör (#18 çözülmüşse) | Açık · #18 çözüldü; push İsmail'in |
| 3 | Ana klasörde boş ARC-01 worktree'si | 25 Kas: `git worktree list`'te artık yok | — | ✅ kapandı |
| 4 | `DECISION-INDEX.md` "Sıradaki boş numara" eskidi | 19.90 ve 19.28 güncelledi: sıradaki **K260** | — | ✅ kapandı |
| 7 | ARC-01 `--check`'i hat aralığında kırmızı | K253 (19.4); aralık 19.90'da kaldırıldı | — | ✅ kapandı |
| 5 | `claude/FAZ-13-PLANI.md`, `FAZ-14-PLANI.md` hiçbir deponun geçmişinde yok | `git log --all` boş | İsmail'in makinesinde/claude.ai projesinde ara | Açık · bilgi |
| 6 | Docs'ta backend `FAZ-14.md` kopyası | `phases/faz-14/f14/backend/14.11/docs/rehber/fazlar/FAZ-14.md` | İstenirse `archive/` | Bilgi |

## D. İsmail'in elle işleri (Hat C bulgularından)

| # | Ne | Kaynak | Durum |
|---|---|---|---|
| 8 | 🔴 `davetkart.com` otomatik yenilemesi KAPALI (4 Ekim kaydı) | `SURE-TAKVIMI.md` §1 #0 (19.8) | Açık · hatırlatıcı 25 Kasım'dı |
| 9 | Natro posta 11 Ocak 2027'de bitiyor; karar yok | `SURE-TAKVIMI.md` §3 | Açık · 11 Aralık'a kadar |
| 10 | SSL bitiş izlemesi kurulmadı | `IZLEME.md` §3 Monitör 2 (19.7) | Açık |
| 22 | Hazır olma ucu ve kalp atışı adresleri boş | `IZLEME.md` §4 (K255, K156); UptimeRobot/Sentry Crons hesabı | Açık |
| 23 | `.ics` takviminin içe aktarılması, tarihlerin doldurulması | `operations/deployment/davetkart-sure-takvimi.ics` (19.8) | Açık |
| 24 | K252 (Gold = video ya da premium etkileşim) onayı yalnızca kod yorumunda | 19.3 kaydı ⚠️ | Açık · onay ve tarih |
| 25 | Sunucu tarafı duman testleri hiç koşmadı | `/api/health` 200 (K255), `php artisan about` (K183, K185); `FAZ-19-ARC-03-COMMIT-KOMUTLARI.md` §8 | Dağıtımdan sonra |
| 26 | Frontend K18 cırcırı (`verify:k18`) kararı | 19.28 D4 önerisi | Karar bekliyor |

## E. Ortak düzeltmenin kapıları (25 Kasım 2026, Hat C worktree'leri)

| Kontrol | Sonuç (görülen çıktı) |
|---|---|
| Backend `composer check` (`fix/2026-11-25-hat-c-open-issues` @ `d414c47`) | ✅ exit 0 — pint geçti · PHPStan 0 hata · `errors`/`plans`/`env` güncel · `k18: 5 dosya, 0 ihlal` · 1273/1273 test, 4620 doğrulama |
| PHPStan tek dosya kipi (#12) | ✅ 0 hata (5 dosya) |
| `K18CheckTest` mutantları (#17) | M1 sondaki yorum kuralı kaldırıldı → 🔴 · M2 docblock/`//` ayrımı kaldırıldı → 🔴 |
| Frontend `npm run check` (`fix/2026-11-25-hat-c-open-issues`) | ✅ exit 0 · `verify:i18n` 781 parça (değişmedi) |
| `composer audit` · `npm run e2e` | koşmadı (bağımlılık değişmedi; e2e Hat B'nin portu) |
