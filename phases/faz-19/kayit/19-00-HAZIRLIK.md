# Faz 19.0 — Paralel çalışma hazırlığı (hat başına test veritabanı)

> **Tarih:** 20 Kasım 2026 · **Karar:** K182 · **Dallar:** backend `fix/2026-11-20-faz19-parallel-test-db`
> (← `faz-19-audit-fixes`) · docs `docs/2026-11-20-faz19-parallel-test-db` (← `docs/2026-11-20-faz-19-audit-fixes`)
> **Commit komutları:** [`../FAZ-19-HAZIRLIK-COMMIT-KOMUTLARI.md`](../FAZ-19-HAZIRLIK-COMMIT-KOMUTLARI.md)

## Faz bölümü

**Sorun.** Üç hat aynı anda `composer check` koşarsa hepsi `davetkart_test`'i kullanır; bir hattın
`RefreshDatabase`'i diğerinin tablolarını siler, testler rastgele kırmızı olur. `phpunit.xml` adı
`<server>` ile bilinçli olarak sabitliyor (10.79b), kabuktan ezilemiyor.

**Karar (K182).** `config/database.php`: yalnızca `APP_ENV=testing` **ve** `DAVETKART_TEST_DB_SUFFIX`
doluyken `pgsql.database = davetkart_test_<son ek>`. Ad sabit `davetkart_test_` ön ekiyle kurulur
(`DB_DATABASE`'ten türetilmez). Son ek `[a-z0-9_]` dışındaysa `InvalidArgumentException` (fail-closed,
K70/K123): sessizce ortak veritabanına düşmek yarışı geri getirirdi. Başka ortamda etkisi yok.
`TestSuiteIsolationTest::the_test_suite_runs_on_its_own_database` genişledi: `assertSame` →
`\Adavetkart_test(_[a-z0-9_]+)?\z`; `davetkart`, `davetkart_hat_x`, boş ad yine kırmızı.

**Değişen dosyalar (backend).** `config/database.php` · `tests/Feature/TestSuiteIsolationTest.php` ·
`docs/rehber/config/database.md` (yeni bölüm "Faz 19.0 (K182)") · `docs/rehber/tests/Feature/TestSuiteIsolationTest.md` §5.

**Testler + mutant.**

| # | Koşu | Sonuç |
|---|---|---|
| 1 | `--filter=TestSuiteIsolationTest` (son ek yok) | ✅ 4/4 |
| 2 | `.env`'e geçici `DAVETKART_TEST_DB_SUFFIX=hat_x`, aynı test | ✅ 4/4 |
| 3 | Aynı `.env` + `APP_ENV=testing`, `tinker` ile `config(...)` | `davetkart_test_hat_x / testing` |
| 4 | Aynı `.env`, `APP_ENV=local` | `davetkart / local` (etkisiz) |
| 5 | Son ek `Hat-X` | 🔴 4 hata: `DAVETKART_TEST_DB_SUFFIX may only contain [a-z0-9_].` |
| M1 | Mutant: config'te ön ek `'davetkart_'.` (yani `davetkart_hat_x` kabul) | 🔴 test kırmızı, mesajda `davetkart_hat_x` |
| 6 | Tam `composer check` (pint, phpstan, errors/plans export, test) | ✅ 1168/1168 |

`.env` ve `config/database.php` her denemeden sonra yedekten geri kondu (hash eşit).

**B7.**

| İddia | Durum |
|---|---|
| Son ekli ad yalnızca `testing`'de | ✅ görüldü (3, 4) |
| Test son ekli adı görüyor ve kabul ediyor | ✅ görüldü (2, M1) |
| `composer check` | ✅ görüldü (6) |
| `composer audit` | koşmadı (bağımlılık değişmedi; prompt yalnızca `check` istedi) |
| `davetkart_test_hat_a/b/c` üzerinde gerçek koşu | koşmadı (veritabanları yok) |

**İsmail'e kalan elle işler.** (1) Üç veritabanını yarat:
`& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" -U postgres davetkart_test_hat_a` (`hat_b`, `hat_c` aynı).
(2) Her hattın backend worktree'sinin `.env`'ine `DAVETKART_TEST_DB_SUFFIX=hat_a|b|c` ekle (dosya
newline ile bitmiyorsa önce satır sonu). (3) Her hatta bir kez `php artisan test --compact --filter=TestSuiteIsolationTest`.

## Kararlar

| **K182** | Paralel hatlarda test veritabanı `davetkart_test_<DAVETKART_TEST_DB_SUFFIX>`; yalnızca `APP_ENV=testing`, son ek `[a-z0-9_]`, geçersizse fail-closed | Faz 19.0 (20 Kas) | geçerli | Üç hattın `RefreshDatabase`'i aynı veritabanında birbirinin tablolarını siliyordu; `<server>` sabitlemesi korunarak hat başına ayrıldı. |

## Eski kararların durum notları

yok (10.79b'nin `<server>` sabitlemesi korunur; K182 onun üstüne yalnızca `testing` ortamında son ek ekler).

## CHANGELOG satırı

- 2026-11-20 — Faz 19.0 (K182): paralel hatlar için hat başına test veritabanı (`DAVETKART_TEST_DB_SUFFIX` → `davetkart_test_<son ek>`); `TestSuiteIsolationTest` genişletildi.
