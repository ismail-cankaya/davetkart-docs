# `prompts/faz-19-agent/` — Faz 19: 3 paralel hat, az token

Eski prompt'lar (`prompts/PROMPT-FAZ-19-*.md`) yerinde duruyor; işler, kararlar ve §A soruları aynı. Burada iş **üç hatta** bölündü: **aynı anda en fazla 3 ajan**, her hatta bir ajan, her ajan tek bulgu.

## Neden bir ajan 200–300 bin token harcıyor?

Claude Code'un gösterdiği token sayısı **toplamdır**: her araç çağrısında bütün bağlam (sistem istemi + araç tanımları + MCP araçları + `CLAUDE.md` + o ana kadar okunan her şey) yeniden işlenir. 30 bin tokenlık bağlamla 10 çağrı ≈ 300 bin. Bu yüzden düşürmenin iki kolu var: **bağlamı küçültmek** ve **çağrı sayısını azaltmak**.

| Kaynak | Önlem |
|---|---|
| Eski prompt'un okuma listesi (~300–400 KB) | `BAGLAM.md` (~9 KB) + prompt (~3–5 KB) + hedefli arama; büyük dosyaları bütün okumak yasak |
| Çok sayıda küçük araç çağrısı | Çağrı bütçesi (S 30 · M 50 · L 80), bağımsız komutları tek çağrıda birleştirme |
| Uzun test çıktıları | Son 40 satır + çıkış kodu; ara adımda `--filter`; tam kapı en sonda bir kez |
| Alt ajanlar / "fork" | Yasak. **Fork** edilen ajan ana oturumun bütün bağlamını devralır; 200–300 bin token'ın en olası kaynağı budur |
| Uzun ana oturumdan ajan başlatmak | Her hattı ayrı, **temiz** bir Claude Code oturumunda başlat (hat klasöründe, `/clear`) |
| Kullanılmayan MCP sunucuları (ör. Playwright) | Hat A ve C'de Claude Code'un `/mcp` menüsünden kapat; yalnızca tarayıcı gereken Hat B'de açık kalsın |
| Paylaşılan kayıt dosyalarını her ajanın okuyup düzenlemesi | Her bulgu tek bir kayıt dosyası yazar; paylaşılan dosyalar 19.90'da bir kez birleştirilir |

## Hatlar

| Hat | Konu | Bulgu | K aralığı | Klasör |
|---|---|---|---|---|
| **A** | backend | 9 | K183–K219 | `D:\Projects\davetkart-hat-a\` |
| **B** | frontend | 10 | K220–K249 | `D:\Projects\davetkart-hat-b\` |
| **C** | kayıt, işletim, küçük backend | 7 | K250–K279 | `D:\Projects\davetkart-hat-c\` |

Hatlar içindeki dosya sahipliği çakışmayı azaltacak biçimde seçildi: `AppServiceProvider`, `config/davetkart.php` ve hata katalogu ağırlıklı olarak Hat A'da; Nginx ve şablonlar Hat B'de; docs ve küçük backend işleri Hat C'de. Yine de çakışma olursa: `19-CAKISMA.md`.

## Sıra

1. **19.0 hazırlık (tek ajan, ana klasörde):** `19-00-HAZIRLIK.md` → commit + birleştir.
2. **Hat klasörlerini kur (bir kez, sen):**

   ```powershell
   cd D:\Projects\davetkart
   git -C davetkart-backend-php-laravel worktree prune
   git -C davetkart-docs worktree prune
   foreach ($h in 'a','b','c') {
     $r = "D:\Projects\davetkart-hat-$h"
     git -C davetkart-backend-php-laravel worktree add --detach "$r\davetkart-backend-php-laravel" faz-19-audit-fixes
     git -C davetkart-frontent worktree add --detach "$r\davetkart-frontent" faz-19-audit-fixes
     git -C davetkart-docs worktree add --detach "$r\davetkart-docs" docs/2026-11-20-faz-19-audit-fixes
     Copy-Item davetkart-backend-php-laravel\.env "$r\davetkart-backend-php-laravel\.env"
     Add-Content "$r\davetkart-backend-php-laravel\.env" "`nDAVETKART_TEST_DB_SUFFIX=hat_$h"
     Push-Location "$r\davetkart-backend-php-laravel"; composer install --no-interaction; Pop-Location
     Push-Location "$r\davetkart-frontent"; npm ci; Pop-Location
   }
   ```
   Sonra PostgreSQL'de üç veritabanını oluştur: `davetkart_test_hat_a`, `davetkart_test_hat_b`, `davetkart_test_hat_c` (Hat B ayrıca `davetkart_e2e`; `TST-04` kurar). Ana klasör `faz-19-audit-fixes`'te kalır; birleştirmeleri orada yaparsın.
3. **Üç hattı başlat:** her hat için ayrı bir Claude Code oturumu; **çalışma klasörü hat klasörü** (`D:\Projects\davetkart-hat-a` …). Yapıştıracağın satırlar **hazır**: [`BASLA.md`](BASLA.md) (şablon yok, her bulgunun gerçek dosya adı ve klasörü yazılı; aynı satır her prompt dosyasının başında da var). Her bulguda: §A'yı **hat klasöründeki** kopyada doldur → `/clear` → `/model` → satırı yapıştır. Bitince: commit komutları (hat klasöründe) → birleştirme (ana klasörde) → hattın sıradaki satırı.
4. **Hat B'nin `SEC-11`'i** Hat A'nın `SEC-10`, `SEC-09` ve Hat C'nin `SEC-13`'ünü bekler (dosyada yazıyor).
5. **Üç hat bitince (Hat C'de):** `19-90-KAYIT.md` → `19-28-ARC-03.md` (Faz 19 kapanışı, `v1.2.0`).
6. Kapanıştan sonra hat klasörlerini kaldır: `git -C <depo> worktree remove D:\Projects\davetkart-hat-x\<depo>` (her depo, her hat).

## Sıra tablosu

| Hat/sıra | Bulgu | Model | Çağrı | §A | Bekler | Dosya |
|---|---|---|---|---|---|---|
| A1 | 19.5 `ARC-04` | Sonnet | 30 | §A | — | [`19-05-ARC-04.md`](19-05-ARC-04.md) |
| A2 | 19.6 `OPS-04` | Sonnet | 30 | §A | — | [`19-06-OPS-04.md`](19-06-OPS-04.md) |
| A3 | 19.10 `SEC-06` | Sonnet | 50 | §A | — | [`19-10-SEC-06.md`](19-10-SEC-06.md) |
| A4 | 19.11 `TST-02` | Opus | 50 | — | — | [`19-11-TST-02.md`](19-11-TST-02.md) |
| A5 | 19.15 `SEC-10` | Sonnet | 30 | §A | — | [`19-15-SEC-10.md`](19-15-SEC-10.md) |
| A6 | 19.12 `FE-51` | Sonnet | 50 | §A | — | [`19-12-FE-51.md`](19-12-FE-51.md) |
| A7 | 19.13 `SEC-08` | Opus | 50 | §A | — | [`19-13-SEC-08.md`](19-13-SEC-08.md) |
| A8 | 19.14 `SEC-09` | Opus | 80 | §A | — | [`19-14-SEC-09.md`](19-14-SEC-09.md) |
| A9 | 19.26 `FE-50` | Opus | 50 | §A | — | [`19-26-FE-50.md`](19-26-FE-50.md) |
| B1 | 19.20 `FE-01` | Sonnet | 30 | §A | — | [`19-20-FE-01.md`](19-20-FE-01.md) |
| B2 | 19.21 `FE-02` | Sonnet | 30 | — | — | [`19-21-FE-02.md`](19-21-FE-02.md) |
| B3 | 19.22 `TST-04` | Opus | 80 | §A | — | [`19-22-TST-04.md`](19-22-TST-04.md) |
| B4 | 19.17 `SEC-12` | Sonnet | 30 | §A | — | [`19-17-SEC-12.md`](19-17-SEC-12.md) |
| B5 | 19.24 `FE-10` | Opus | 50 | §A | — | [`19-24-FE-10.md`](19-24-FE-10.md) |
| B6 | 19.25 `FE-53` | Opus | 50 | §A | — | [`19-25-FE-53.md`](19-25-FE-53.md) |
| B7 | 19.27 `FE-54` | Sonnet | 30 | §A | — | [`19-27-FE-54.md`](19-27-FE-54.md) |
| B8 | 19.23 `FE-04` | Opus | 50 | §A | — | [`19-23-FE-04.md`](19-23-FE-04.md) |
| B9 | 19.18 `SEC-11` | Sonnet | 30 | §A | `SEC-10`, `SEC-09`, `SEC-13` | [`19-18-SEC-11.md`](19-18-SEC-11.md) |
| B10 | 19.19 `FE-52` | Sonnet | 30 | §A | — | [`19-19-FE-52.md`](19-19-FE-52.md) |
| C1 | 19.2 `ARC-01` | Sonnet | 30 | — | — | [`19-02-ARC-01.md`](19-02-ARC-01.md) |
| C2 | 19.3 `ARC-02` | Sonnet | 30 | §A | — | [`19-03-ARC-02.md`](19-03-ARC-02.md) |
| C3 | 19.4 `ARC-05` | Sonnet | 50 | §A | — | [`19-04-ARC-05.md`](19-04-ARC-05.md) |
| C4 | 19.8 `OPS-05` | Sonnet | 30 | §A | — | [`19-08-OPS-05.md`](19-08-OPS-05.md) |
| C5 | 19.7 `OPS-03` | Sonnet | 30 | §A | — | [`19-07-OPS-03.md`](19-07-OPS-03.md) |
| C6 | 19.16 `SEC-13` | Sonnet | 30 | §A | — | [`19-16-SEC-13.md`](19-16-SEC-13.md) |
| C7 | 19.9 `SEC-05` | Sonnet | 30 | §A | — | [`19-09-SEC-05.md`](19-09-SEC-05.md) |
| C8 | 19.90 kayıt birleştirme | Sonnet | 40 | — | A, B, C bitmiş | [`19-90-KAYIT.md`](19-90-KAYIT.md) |
| C9 | 19.28 `ARC-03` + Faz 19 kapanışı | Sonnet | 80 | §A | 19.90 | [`19-28-ARC-03.md`](19-28-ARC-03.md) |

Yardımcılar: [`BASLA.md`](BASLA.md) (yapıştırılacak satırlar) · [`BAGLAM.md`](BAGLAM.md) (ortak kurallar) · [`19-00-HAZIRLIK.md`](19-00-HAZIRLIK.md) · [`19-CAKISMA.md`](19-CAKISMA.md)
