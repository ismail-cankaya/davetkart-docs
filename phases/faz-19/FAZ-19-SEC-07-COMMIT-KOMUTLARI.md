# Faz 19.1 — `SEC-07` commit komutları (+ `v1.1.0`)

> **Tarih:** 20 Kasım 2026 · **Bulgu:** `SEC-07` (Composer bağımlılıklarında bilinen açıklar; `composer audit` kırmızı)
> **Dallar:** backend `fix/2026-11-20-sec-07-composer-audit` (← `faz-19-audit-fixes`) · docs `docs/2026-11-20-faz-19-audit-fixes`
> **Frontend:** değişmedi, commit yok. **Kararlar:** K179–K181 ([`EK-FAZ-19`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md))
> **Kayıt:** backend `docs/rehber/fazlar/FAZ-19.md` §19.1
> Komutları İsmail çalıştırır. Her blok kendi dalına geçer, dosyaları tek tek ekler, `git status --short` ile biter.

## Başlamadan: çalışma ağaçlarında ne olmalı

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git branch --show-current                     # fix/2026-11-20-sec-07-composer-audit
git status --short --untracked-files=all
```

Beklenen satırlar (tam liste; fazlası varsa commit'ten önce bak):

```
 M app/Services/Payment/ShopierGateway.php
 M composer.lock
 M docs/rehber/app/Services/Payment/ShopierGateway.md
 M docs/rehber/config/trustedproxy.md
 M docs/rehber/fazlar/FAZ-18.md
 M docs/rehber/fazlar/README.md
 M docs/rehber/tests/Feature/PaymentDriverResolutionTest.md
 M tests/Feature/PaymentDriverResolutionTest.php
 M tests/Feature/ShopierGatewayTest.php
?? docs/rehber/composer.md
?? docs/rehber/fazlar/FAZ-19.md
```

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git branch --show-current                     # faz-19-audit-fixes
git status --short --untracked-files=all      # boş (yalnızca '?? .claude/...' olabilir)
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git branch --show-current                     # docs/2026-11-20-faz-19-audit-fixes
git status --short --untracked-files=all
```

Beklenen satırlar:

```
 M CHANGELOG.md
 M decisions/DECISION-INDEX.md
 M decisions/README.md
 M operations/deployment/YAYIN-SIRASI.md
 M phases/README.md
 M phases/faz-18/FAZ-18-SEC-04-COMMIT-KOMUTLARI.md
 M phases/faz-19/README.md
?? decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md
?? phases/faz-19/FAZ-19-SEC-07-COMMIT-KOMUTLARI.md
?? prompts/faz-19-agent/19-02-ARC-01.md      ← senin dosyaların (20 Kasım 12:44); bu commit'e GİRMEZ
?? prompts/faz-19-agent/…                     ← aynı klasörün diğer dosyaları
```

## 0. 🔴 Önce: `vendor`'u kur ve kapıları gör (bu oturumda koşmadı)

20 Kasım'da GitHub bu makineden 12:40–13:22 arası erişilemedi (`Connection was reset`); yeni
`composer.lock` yazıldı ama paketler indirilemedi, `vendor/` hâlâ eski (Laravel 13.35.0). Yeni lock
`composer audit --locked` ile temiz görüldü; **yeni `vendor` ile hiçbir test koşmadı.** GitHub
erişilebilirken, commit'ten önce:

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-07-composer-audit
composer install                              # 1 install, 54 updates, 0 removals
composer install --dry-run                    # Nothing to install, update or remove
composer audit                                # No security vulnerability advisories found.  (çıkış 0)
composer check                                # son satır "result":"passed", "tests":1168
git status --short --untracked-files=all      # aşağıdaki listeyle aynı; composer.lock yeniden değişmemiş olmalı
```

Biri kırmızıysa **commit etme**: çıktıyı bana getir (K150). `composer install` `composer.lock`'u
değiştirmez; değişmişse (`git diff --stat composer.lock` 875 satırdan farklıysa) yine dur.

## 1. Backend

```powershell
# 19.1.1 — composer.lock (55 paket, majör yok) + kılavuz
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-07-composer-audit
git add composer.lock
git add docs/rehber/composer.md
git commit -m "19.1.1 - fix(deps): Update Laravel and Symfony to clear the nine composer audit advisories"
git status --short
```

```powershell
# 19.1.2 — Shopier callback adresi APP_URL'den (K180) + test + kılavuzlar
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-07-composer-audit
git add app/Services/Payment/ShopierGateway.php
git add tests/Feature/PaymentDriverResolutionTest.php
git add tests/Feature/ShopierGatewayTest.php
git add docs/rehber/app/Services/Payment/ShopierGateway.md
git add docs/rehber/tests/Feature/PaymentDriverResolutionTest.md
git add docs/rehber/config/trustedproxy.md
git commit -m "19.1.2 - fix(payments): Build the Shopier callback URL from APP_URL instead of the request host"
git status --short
```

```powershell
# 19.1.3 — faz kaydı (FAZ-19.md yeni) + faz dizini + FAZ-18 durum notu
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-07-composer-audit
git add docs/rehber/fazlar/FAZ-19.md
git add docs/rehber/fazlar/README.md
git add docs/rehber/fazlar/FAZ-18.md
git commit -m "19.1.3 - docs(phases): Record Phase 19.1 (SEC-07 composer audit and Shopier callback host)"
git status --short                            # boş olmalı
```

## 2. Frontend

Değişiklik yok, commit yok.

## 3. Docs

```powershell
# 19.1.4 — K179–K181, takip tablosu, yayın listesi, bu dosya
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-20-faz-19-audit-fixes
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md
git add decisions/DECISION-INDEX.md
git add decisions/README.md
git add operations/deployment/YAYIN-SIRASI.md
git add phases/faz-19/README.md
git add phases/faz-19/FAZ-19-SEC-07-COMMIT-KOMUTLARI.md
git add phases/faz-18/FAZ-18-SEC-04-COMMIT-KOMUTLARI.md
git add phases/README.md
git add CHANGELOG.md
git commit -m "docs(decisions): Add K179-K181 and commit commands for SEC-07"
git status --short                            # yalnızca '?? prompts/faz-19-agent/…' (senin)
```

## 4. Birleştirme (yalnızca backend)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-19-audit-fixes
git merge --no-ff fix/2026-11-20-sec-07-composer-audit -m "Merge SEC-07 fix into faz-19-audit-fixes"
git status --short
# git push -u origin fix/2026-11-20-sec-07-composer-audit
# git push -u origin faz-19-audit-fixes
```

Frontend'de birleştirilecek dal yok (`faz-19-audit-fixes` = `faz-18-audit-fixes`, `fefa647`).

```powershell
# isteğe bağlı: frontend entegrasyon dalını uzak depoya gönder
# cd D:\Projects\davetkart\davetkart-frontent
# git push -u origin faz-19-audit-fixes
```

---

## 5. `v1.1.0` (Faz 18 + `SEC-07`) — prompt 19.1 §11

**Etiket: BEKLİYOR.** Prompt §11: üç kapının çıktısı görülmeden etiket komutu verilmez. 20 Kasım'da:

| Kapı | Sonuç |
|---|---|
| backend `composer check` | ⚠️ yalnızca **eski** `vendor` ile ✅ (1168 test); yeni `vendor` ile koşmadı |
| backend `composer audit` | ⚠️ yeni lock `--locked` ile ✅ (çıkış 0); kurulu paketlerle koşmadı |
| frontend `npm ci` + `npm run check` | ✅ çıkış 0 (frontend değişmedi) |

§0 yeşil olunca bana "devam" de: kapıları görüp §5.2'yi (etiket) eklerim. Etiketin biçimi ve sırası
zaten docs [`YAYIN-SIRASI.md`](../../operations/deployment/YAYIN-SIRASI.md) §3–§4'te (mesaj:
`Release v1.1.0: Phase 18 audit fixes + SEC-07`). Sıra: **önce backend, sonra frontend** (K148).
§5.1 ve §5.3 (birleştirmeler) §0 yeşil olduktan sonra çalıştırılabilir.

🔴 `main`'e birleştirme yayın değildir, ama sunucu `main`'i çeker (Y8.2a). İtmeyi dağıtıma hazır
olduğunda yap. Bugün sunucuda çalışan commit'leri önce `v1.0.0` diye etiketlemek önerisi:
`YAYIN-SIRASI.md` §3 sonu (geri dönülecek etiket, §5).

### 5.1 `faz-19-audit-fixes` → `main`

20 Kasım'da üç depoda `main` entegrasyon dalının atası (`faz-19-audit-fixes..main` = 0); Faz 18 henüz
`main`'de değil, bu birleştirme Faz 18'i ve `SEC-07`'yi birlikte getirir. Çakışma beklenmez.

```powershell
# 5.1a — backend
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch main
git merge --no-ff faz-19-audit-fixes -m "Merge faz-19-audit-fixes into main (v1.1.0: Phase 18 audit fixes + SEC-07)"
git log --oneline -1
git status --short
```

```powershell
# 5.1b — frontend (backend'den SONRA)
cd D:\Projects\davetkart\davetkart-frontent
git switch main
git merge --no-ff faz-19-audit-fixes -m "Merge faz-19-audit-fixes into main (v1.1.0: Phase 18 audit fixes)"
git log --oneline -1
git status --short
```

### 5.2 Etiket: **BEKLİYOR** (komut verilmedi)

Engel: yeni `vendor` ile `composer check` ve kurulu paketlerle `composer audit` görülmedi (§0, yukarıdaki
tablo). İtme de etiketten sonra gelir; `main`'i etiketten önce itme (sunucu `main`'i çeker, Y8.2a):

```powershell
# git push origin main      # backend: etiket atılıp YAYIN-SIRASI §4.1'e gelindiğinde
# git push origin main      # frontend: backend sunucuda yeşilken (§4.3)
```

### 5.3 Docs dalları → `main`

`docs/2026-11-16-faz-18-audit-fixes`, Faz 19 docs dalının atası; ikisi sırayla birleşir. Faz 19 docs
dalı sonraki bulgularla ilerlemeye devam eder ve Faz 19 sonunda yeniden birleşir.

```powershell
cd D:\Projects\davetkart\davetkart-docs
git switch main
git merge --no-ff docs/2026-11-16-faz-18-audit-fixes -m "Merge Faz 18 audit fix records into main"
git merge --no-ff docs/2026-11-20-faz-19-audit-fixes -m "Merge Faz 19.1 (SEC-07) records into main"
git log --oneline -3
git status --short                            # yalnızca '?? prompts/faz-19-agent/…' (senin)
# git push origin main
git switch docs/2026-11-20-faz-19-audit-fixes
```

### 5.4 Dağıtım ve duman testi

Kopyalanmadı; tek ev:

- Sıra, komutlar, ara kontrol: [`YAYIN-SIRASI.md`](../../operations/deployment/YAYIN-SIRASI.md) §4.1–§4.4
  (§4.4 Nginx kurulumu `v1.1.0`'da gerekli).
- Duman testi: aynı dosya §6.
- Faz 18'in yayın günü listesi: [`FAZ-18-SEC-04-COMMIT-KOMUTLARI.md`](../faz-18/FAZ-18-SEC-04-COMMIT-KOMUTLARI.md) §7–§8.
- **`SEC-07`'ye özgü, dağıtımdan önce:** sunucuda `grep '^APP_URL=' /var/www/davetkart/backend/.env`
  → `APP_URL=https://davetkart.com` (K180: Shopier callback adresi artık buradan). Dağıtımdan sonra
  sunucuda `cd /var/www/davetkart/backend && composer audit --no-dev` → `No security vulnerability advisories found.`

## 6. Commit'ten sonra: elle işler

Backend `docs/rehber/fazlar/FAZ-19.md` §19.1 "Elle doğrulama (İsmail)".
