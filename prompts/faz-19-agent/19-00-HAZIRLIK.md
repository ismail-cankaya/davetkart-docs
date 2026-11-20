# 19.0 — Paralel çalışma hazırlığı (hat başına test veritabanı)

> **Başlatma:** `D:\Projects\davetkart` (ana klasör) → `/clear` → `/model sonnet` → [`BASLA.md`](BASLA.md) §0 satırı.
> **Tek ajan, hatlar başlamadan önce.** **Model:** `/model sonnet` · **Çağrı bütçesi:** 30 · Kurallar: `BAGLAM.md` (yalnızca §1 ve §3; bu prompt ana klasörde çalışır, §2'nin "ana klasörde değişiklik yok" kuralı bu prompt için geçerli değil).

## Sorun

Üç hat aynı anda `composer check` koşarsa hepsi `davetkart_test` veritabanını kullanır; `RefreshDatabase` birbirinin tablolarını siler ve testler rastgele kırmızı olur. `phpunit.xml` adı `<server>` ile sabitliyor (kabuktan ezilemesin diye, bilinçli) ve `TestSuiteIsolationTest` adın tam `davetkart_test` olduğunu doğruluyor.

## Karar (K182)

- `config/database.php`: yalnızca `APP_ENV=testing` iken ve `.env`'de `DAVETKART_TEST_DB_SUFFIX` tanımlıysa (yalnızca `[a-z0-9_]`), veritabanı adı `davetkart_test_<suffix>` olur. Başka hiçbir ortamda etkisi yok.
- `TestSuiteIsolationTest::the_test_suite_runs_on_its_own_database`: ad `davetkart_test` **ya da** `davetkart_test_` ile başlıyor olmalı; geliştirme (`davetkart`) ve boş ad yine kırmızı. Testi zayıflatma, genişlet.
- Kılavuz: `docs/rehber/config/database.md` (ya da var olan) — neden, nasıl kullanılır, hangi hatayı önler.

## Adımlar (ana klasör, `D:\Projects\davetkart\davetkart-backend-php-laravel`)

1. `git status --short` temiz; `git switch -c fix/<YYYY-MM-DD>-faz19-parallel-test-db faz-19-audit-fixes`.
2. `19.0.1` config + test + kılavuz. Testler: `--filter=TestSuiteIsolationTest`; bir kez `.env`'e geçici `DAVETKART_TEST_DB_SUFFIX=hat_x` ekleyip aynı testin `davetkart_test_hat_x`'i gördüğünü göster, sonra satırı geri al. Tam `composer check` bir kez.
3. **Mutant:** ön ek kontrolünü kaldır (`davetkart` kabul edilsin) → test kırmızı.
4. Docs: ana docs klasöründe `git switch -c docs/<YYYY-MM-DD>-faz19-parallel-test-db docs/2026-11-20-faz-19-audit-fixes`; `phases/faz-19/kayit/19-00-HAZIRLIK.md` (`BAGLAM.md` §4 biçiminde, K182) ve `phases/faz-19/FAZ-19-HAZIRLIK-COMMIT-KOMUTLARI.md` (bu prompt için commit + birleştirme blokları **ana klasörde**).
5. Rapor (≤25 satır).
