# Birleştirme çakışması yardımcısı (her hat için)

> **Ne zaman:** ana klasörde (`D:\Projects\davetkart\<depo>`) `git merge --no-ff …` çakışmayla durduğunda. Birleştirmeyi **iptal etme**; yeni oturum (`/clear`) + `/model sonnet` + bu dosya. **Çağrı bütçesi:** 25. Kurallar: `BAGLAM.md` §1 ve §3 (bu prompt ana klasörde çalışır).

1. `git status --short` + `git diff --name-only --diff-filter=U` (tek komut). Yalnızca çakışan dosyaları, yalnızca çakışma bloklarını oku (`git grep -n "^<<<<<<<"` ile satırları bul).
2. **Kural:** iki tarafın değişikliği de korunur (iki hat farklı bulgular üzerinde çalıştı). Anlam çatışması varsa (aynı satırda iki farklı karar) **dur**, iki seçeneği göster.
3. **Üretilmiş dosyalar elle birleştirilmez, yeniden üretilir:** `contracts/error-codes.json` → kaynak enum/katalog birleştirildikten sonra `php artisan errors:export`; `contracts/plan-rules.json` → `php artisan plans:export`; `package-lock.json` → `package.json` birleştirildikten sonra `npm install`; frontend sözleşme kopyaları → depodaki eşitleme betiğiyle.
4. Çeviri JSON'ları: iki tarafın anahtarları birlikte; JSON geçerli mi (`node -e "JSON.parse(require('fs').readFileSync('<yol>','utf8'))"`).
5. Kapı: çakışan alana göre `--filter`'lı testler + son olarak tam `composer check` ya da `npm run check` (yalnızca etkilenen depo).
6. Bana: çözülen dosyaları tek tek `git add` eden ve birleştirmeyi `git commit --no-edit` ile bitiren PowerShell bloğu. Rapor ≤15 satır.
