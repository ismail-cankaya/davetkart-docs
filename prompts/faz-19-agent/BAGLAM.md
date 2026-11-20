# Faz 19 — ajan bağlamı (ortak kurallar; her prompt'la birlikte bağlayıcı)

Özet kaynak: `PHP-LARAVEL-SETUP.md`, üç `CLAUDE.md`, Faz 18 kayıtları. Çelişki görürsen dur ve sor.

## 1. Token disiplini

**Neden:** her araç çağrısında bütün bağlam (sistem + araçlar + okuduğun her şey) yeniden işlenir. Harcama ≈ bağlam boyutu × çağrı sayısı. İkisini birden küçült.

1. **Alt ajan yok** (`Agent`/`Task`/Explore). Tek oturum, tek bulgu.
2. **Çağrı bütçesi:** prompt'un başındaki sayı (S 30 · M 50 · L 80). Yarısını geçtiysen ve iş yarıdan azsa dur, durumu yaz.
3. **Birleştir:** birbirinden bağımsız okumaları ve komutları **tek çağrıda** yap (aynı mesajda paralel araç çağrıları ya da `;` ile birleşik komut). Örn. başlangıç kontrollerinin hepsi tek komut.
4. **Okuma:** 300 satırdan uzun dosyayı bütün okuma; önce `git grep -n` / Grep, sonra Read (offset+limit). `PHP-LARAVEL-SETUP.md`, `REPORT.md`, `findings/*.md`, `FAZ-18.md`, `EK-FAZ-18.md` bütün olarak **yasak**. Bulgu metni: Grep `^### <ID> ` + 15 satır. `DECISION-INDEX.md`: ilk 25 satır. `vendor/`, `node_modules/`, `dist/`, `storage/` içinde arama yok.
5. **Yazma:** yeni dosyayı tek `Write` ile yaz; az sayıda büyük `Edit` tercih et. Yazdığın dosyayı doğrulamak için yeniden okuma.
6. **Çıktı kırp:** bash `cmd 2>&1 | tail -n 40; echo "exit=${PIPESTATUS[0]}"` · PowerShell `cmd 2>&1 | Select-Object -Last 40; "exit=$LASTEXITCODE"`. Kırmızıda yalnızca başarısız testi `--filter` ile yeniden koş.
7. **Testler:** ara adımlarda `php artisan test --compact --filter=…` ve `vendor/bin/pint --dirty`; tam kapı (`composer check` + `composer audit`, frontend `npm run check`, varsa `npm run e2e`) **en sonda bir kez**. Mutant en fazla 2, `--filter` ile.
8. **Ara mesaj yok.** Rapor en sonda, kısa (§6).

## 2. Paralel çalışma (3 hat)

- Üç hat aynı anda çalışır; **her hatta aynı anda tek ajan**. Hat klasörleri: `D:\Projects\davetkart-hat-a|b|c\` (içinde `davetkart-backend-php-laravel`, `davetkart-frontent`, `davetkart-docs` worktree'leri). Ana klasör `D:\Projects\davetkart\` yalnızca İsmail'in birleştirmeleri içindir; **ajan ana klasörde dosya değiştirmez**.
- Yeni dal **her zaman** entegrasyon dalından açılır: kod `git switch -c fix/<YYYY-MM-DD>-<slug> faz-19-audit-fixes`, docs `git switch -c docs/<YYYY-MM-DD>-<slug> docs/2026-11-20-faz-19-audit-fixes`. (Entegrasyon dalları ana klasörde açık olduğu için worktree'de `git switch faz-19-audit-fixes` **çalışmaz**; gerek de yok.)
- **Test veritabanı hatta özel:** worktree'nin `.env`'inde `DAVETKART_TEST_DB_SUFFIX=hat_a|b|c` (19.0 hazırlığı). Başka hattın veritabanına, geliştirme veritabanına ve canlıya dokunma.
- **Portlar:** Hat A backend `8010`; Hat B frontend `5173/4173`, E2E backend `8020` + preview `4180`; Hat C backend `8030`.
- **K numarası:** hattın aralığından (A K183–K219 · B K220–K249 · C K250–K279). Kullanılan en büyük numarayı `git grep -h -o "K2[0-9][0-9]\|K1[89][0-9]" -- phases/faz-19/kayit` (docs worktree'sinde, entegrasyon dalından) ile bul, sonrakini al. Aralık biterse dur.
- **Paylaşılan dosyalar:** `DECISION-INDEX.md`, `EK-FAZ-19.md`, `CHANGELOG.md`, `phases/faz-19/README.md`, `prompts/README.md`, backend `FAZ-19.md` ve `fazlar/README.md`'ye **dokunma** (19.90 birleştirir). İstisna: prompt'ta açıkça yazıyorsa.
- Başka bir bulgunun kararını ya da sonucunu arıyorsan (prompt'ta "19.x'in K'sı", "`FAZ-19.md` §19.x" geçiyorsa) 19.90'dan önce bu bilgi `phases/faz-19/kayit/19-xx-*.md`'dedir; oradan oku.
- Yeni çeviri anahtarlarını ve config anahtarlarını dosyanın sonuna değil ilgili bölümün içine ekle (birleştirme çakışmasını azaltır).

## 3. Çalışma biçimi ve proje kuralları

- Adımların hepsi **tek seferde, durmadan**; yalnızca §5 ve prompt'taki dur koşullarında dur.
- 🔴 **Git yazma yasak:** `add`, `commit`, `push`, `stash`, `reset`, `merge`, `rebase`, `tag`, `rm`, `mv`, `restore`, `checkout -- <dosya>`, `worktree`. İzinli: okuma komutları ve yukarıdaki `git switch -c`.
- Tek bulgu = tek dal; kapsam dışını düzeltme ("gördüm, dokunmadım"). Her dosya tek adıma ait. 🔴 **B7:** görmediğin çıktıya "geçti" yazma. Canlı sisteme istek ve sır yok. Frontend'de dosyalar tek tek (CRLF). Plandan sapma: gerekçe + K'da "plandan sapma". §A boş satır: varsayılan + K'da "varsayılan (İsmail cevaplamadı)".
- **Yığın ve desenler:** Laravel 13 / PHP 8.5, Action katmanı, Repository yok, Sanctum; para tam sayı kuruş; enum durumlar; `transaction` + `lockForUpdate`; fail-closed yapılandırma (K70/K123); dış adres `config('app.url')`'den. Frontend React 19 + TS + Vite.
- **Sözleşmeler:** hata kodu = `contracts/error-codes.json` + `php artisan errors:export` + frontend kopyası + tr/en çeviri (`verify:errors`); plan kuralları `plans:export --check` + `verify:plans`.
- **K18:** kod yorumu 1–3 satır; ayrıntı aynı depoda `docs/rehber/<aynı-yol>.md`, **en fazla ~50 satır** (neden · desen · hangi hataya karşı · sık hata · nasıl denenir), kod dosyasıyla aynı commit'te.
- **Commit mesajı** İngilizce: kod `19.<n>.<adım> - <tür>(<alan>): <Fiil> ...`, docs `docs(<alan>): <Fiil> ...`.

## 4. Kayıt (paylaşılan dosyalar yerine tek dosya)

Docs worktree'sinde bulgunun dalında **iki dosya** yaz:

1. `phases/faz-19/kayit/19-<NN>-<ID>.md` (en fazla ~60 satır):
   - `## Faz bölümü` — sorun (2–3 cümle), kararlar, değişen dosyalar, testler + mutantlar, B7 tablosu, İsmail'e kalan elle işler.
   - `## Kararlar` — her K için tek satır: `| **K2xx** | başlık | Faz 19.<n> (<tarih>) | geçerli | gerekçe (tek cümle) |`
   - `## Eski kararların durum notları` — ör. `K55 → geçersiz kılındı → K2xx` (yoksa "yok").
   - `## CHANGELOG satırı` — tek satır.
2. `phases/faz-19/FAZ-19-<ID>-COMMIT-KOMUTLARI.md` (§6).

Backend `FAZ-19.md`, `DECISION-INDEX.md`, `EK-FAZ-19.md`, `CHANGELOG.md` ve takip tablosu bu dosyalardan **19.90**'da üretilir.

## 5. Başlarken ve dur

- **Tek komutla başlangıç kontrolü:** hattın üç worktree'sinde `git status --short` (temiz olmalı; docs'ta yalnızca bu prompt dosyası §A yüzünden değişmiş olabilir), `git fetch` gerekmez (aynı depo), önceki bulgunun dalı birleşmiş mi: `git branch --merged faz-19-audit-fixes --list "fix/*-<önceki-slug>"` (docs bulgusunda `docs/2026-11-20-faz-19-audit-fixes` ve `docs/*-<önceki-slug>`).
- **Dur ve sor:** önkoşul tutmuyor · kod bulgunun anlattığından belirgin farklı (zaten kapanmışsa kanıt + yalnızca kayıt) · kapı senin dışındaki nedenle kırmızı · izin verilmeyen yeni bağımlılık · para/müşteri verisi/hukuki metin/canlı sistem için geri alınamaz karar · çağrı bütçesi sorunu (§1.2).

## 6. Commit komutları ve rapor

**Commit komutları dosyası:**
- Üstte her worktree için beklenen `git status --short --untracked-files=all` satırları.
- Her adım ayrı PowerShell bloğu, **hattın klasöründe**: `cd D:\Projects\davetkart-hat-<x>\<depo>` → `git add <yol>` tek tek (`git rm`, `git mv` gerekirse) → `git commit -m "..."` → `git status --short`. Joker, klasör yolu, `-A` yok. Sıra: backend → frontend → docs.
- Son blok **ana klasörde** birleştirme: `cd D:\Projects\davetkart\<depo>` → `git merge --no-ff <dal> -m "Merge <ID> into <entegrasyon>"` → `git status --short` (kod için `faz-19-audit-fixes`, docs için `docs/2026-11-20-faz-19-audit-fixes`). Çakışma çıkarsa: `19-CAKISMA.md`.

**Rapor (tek mesaj, ≤40 satır):** adımlar · K'lar · B7 tablosu · mutant sonucu · gördüm-dokunmadım · commit dosyasının yolu · öğretici özet (≤5 satır) · İsmail'in elle işleri · kullanılan araç çağrısı sayısı.
