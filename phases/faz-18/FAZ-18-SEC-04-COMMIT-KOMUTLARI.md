# Faz 18.6 — `SEC-04` commit komutları ve Faz 18 kapanışı

> **Tarih:** 20 Kasım 2026 · **Kararlar:** K173–K178 · **Faz kaydı:** backend `docs/rehber/fazlar/FAZ-18.md` §18.6
> ve "Faz 18 kapanış özeti"
> Her blok bir commit. Dosyalar tek tek, açık yolla eklenir; joker, klasör yolu ve `-A` yok.
> Her blok `git status --short` ile biter. Sıra: backend → docs → birleştirme → Faz 18 kapanışı.
> **Frontend değişmedi:** commit yok, birleştirme yok. Backend dalı: `fix/2026-11-20-sec-04-security-headers`.

## Başlamadan: çalışma ağaçlarında ne olmalı

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-04-security-headers
git status --short --untracked-files=all
```

Beklenen (12 satır, başka bir şey yok):

```
 M deploy/nginx/davetkart.conf
 M docs/rehber/app/Http/Middleware/SecurityHeaders.md
 M docs/rehber/deploy/nginx/davetkart.md
 M docs/rehber/fazlar/FAZ-18.md
 M docs/rehber/fazlar/FAZ-9.md
 M docs/rehber/fazlar/README.md
?? deploy/nginx/install.sh
?? deploy/nginx/snippets/davetkart-security-headers.conf
?? deploy/smoke/check-security-headers.sh
?? docs/rehber/deploy/nginx/install.md
?? docs/rehber/deploy/nginx/snippets/davetkart-security-headers.md
?? docs/rehber/deploy/smoke/check-security-headers.md
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-16-faz-18-audit-fixes
git status --short --untracked-files=all
```

Beklenen (7 satır):

```
 M CHANGELOG.md
 M decisions/DECISION-INDEX.md
 M decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md
 M operations/deployment/YAYIN-SIRASI.md
 M phases/README.md
 M phases/faz-18/README.md
?? phases/faz-18/FAZ-18-SEC-04-COMMIT-KOMUTLARI.md
```

Frontend ağacı boş ve `faz-18-audit-fixes`'te olmalı. `fix/2026-11-20-sec-04-security-headers` dalı
açıldı ama commit almadı (`fefa647`'de, entegrasyon dalıyla aynı). İstersen sil:

```powershell
cd D:\Projects\davetkart\davetkart-frontent
git switch faz-18-audit-fixes
git branch -d fix/2026-11-20-sec-04-security-headers
git status --short
```

## 1. Backend

Ara commit'ler ayrı ayrı koşulmadı (stash/checkout yasaktı); yalnızca son ağaç koştu
(`composer check` 1166 test, Nginx denemesi, mutantlar). 18.6.1'in kılavuzu 18.6.2'deki
`install.sh`'a ve 18.6.3'teki duman testine ileri bağlantı veriyor; üçü aynı birleştirmeyle gider.

```powershell
# 18.6.1 — SPA güvenlik başlıkları snippet'i + API dışındaki her location'a include (K173–K176)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-04-security-headers
git add deploy/nginx/snippets/davetkart-security-headers.conf
git add docs/rehber/deploy/nginx/snippets/davetkart-security-headers.md
git add deploy/nginx/davetkart.conf
git add docs/rehber/deploy/nginx/davetkart.md
git commit -m "18.6.1 - feat(nginx): Add security headers for the SPA in every non-API location"
git status --short
```

```powershell
# 18.6.2 — Nginx kurulum betiği: nginx -t yeşilse reload, kırmızıysa eskileri geri koy (K173)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-04-security-headers
git add deploy/nginx/install.sh
git add docs/rehber/deploy/nginx/install.md
git commit -m "18.6.2 - feat(deploy): Add an Nginx install script that tests before reloading and rolls back"
git status --short
```

```powershell
# 18.6.3 — duman testi: her location türü + API'de tek kaynak (K178)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-04-security-headers
git add deploy/smoke/check-security-headers.sh
git add docs/rehber/deploy/smoke/check-security-headers.md
git commit -m "18.6.3 - feat(deploy): Add a smoke test for the security headers of every location"
git status --short
```

```powershell
# 18.6.4 — faz kaydı + Faz 18 kapanışı; K85 durum notu; ara katman kılavuzuna "yalnızca API" notu
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-20-sec-04-security-headers
git add docs/rehber/fazlar/FAZ-18.md
git add docs/rehber/fazlar/README.md
git add docs/rehber/fazlar/FAZ-9.md
git add docs/rehber/app/Http/Middleware/SecurityHeaders.md
git commit -m "18.6.4 - docs(phases): Record Phase 18.6 (SEC-04 security headers) and close Phase 18"
git status --short                                   # boş olmalı
```

## 2. Docs

```powershell
# 18.6.6 — kararlar (K173–K178), indeks (K85 notu, sıradaki K179), çalıştırma kitabı §4.4 + §6, takip tabloları, bu dosya
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-16-faz-18-audit-fixes
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md
git add decisions/DECISION-INDEX.md
git add operations/deployment/YAYIN-SIRASI.md
git add phases/faz-18/README.md
git add phases/faz-18/FAZ-18-SEC-04-COMMIT-KOMUTLARI.md
git add phases/README.md
git add CHANGELOG.md
git commit -m "docs(decisions): Add K173-K178, the Nginx runbook steps and the Phase 18 closure for SEC-04"
git status --short                                   # boş olmalı
# git push -u origin docs/2026-11-16-faz-18-audit-fixes
```

## 3. Birleştirme (yalnızca backend)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-20-sec-04-security-headers -m "Merge SEC-04 fix into faz-18-audit-fixes"
git status --short
# git push -u origin faz-18-audit-fixes
# git push -u origin fix/2026-11-20-sec-04-security-headers
```

Frontend için birleştirme yok (commit yok). Bitince `phases/faz-18/README.md`'de `SEC-04` satırını
`birleşti` yap; 18.1–18.5 satırları da git'te birleşmiş görünüyor (backend `96664dd`, frontend `fefa647`).

## 4. Faz 18 kapanışı: `faz-18-audit-fixes` → `main` (önce backend, sonra frontend)

🔴 **`main`'e birleştirme yayın değildir, ama sunucu `main`'i çeker (Y8.2a).** `SEC-07` kapanıp `v1.1.0`
atılana kadar sunucuda `deploy.sh` / `deploy-frontend.sh` **çalıştırma** ve `main`'i itmeyi bekletmek
en güvenlisi (itme satırları yorumda). Üç depoda da `main` entegrasyon dalının atası (20 Kasım:
`faz-18-audit-fixes..main` = 0), birleştirme çakışmasız.

```powershell
# 4a — backend
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch main
git merge --no-ff faz-18-audit-fixes -m "Merge faz-18-audit-fixes into main (Faz 18 audit fixes, AUD-2026-11-12)"
git log --oneline -1
git status --short
# git push origin main          # SEC-07 kapanıp etiket atılana kadar bekletmen önerilir
```

```powershell
# 4b — frontend (backend'den SONRA)
cd D:\Projects\davetkart\davetkart-frontent
git switch main
git merge --no-ff faz-18-audit-fixes -m "Merge faz-18-audit-fixes into main (Faz 18 audit fixes, AUD-2026-11-12)"
git log --oneline -1
git status --short
# git push origin main          # backend main'i itildikten sonra
```

## 5. Etiket: **BEKLİYOR** (`v1.1.0` komutu verilmedi)

Prompt 18.6 §11.5: `composer audit` kırmızıyken etiket komutu verilmez. 20 Kasım'da son ağaçta:

| Kapı | Sonuç |
|---|---|
| backend `composer check` | ✅ 1166 test |
| backend `composer audit` | ❌ çıkış 1 · 6 pakette 9 açık |
| frontend `npm ci` | ✅ `found 0 vulnerabilities` |
| frontend `npm run check` | ✅ çıkış 0 |

Engeller (`SEC-07`, ayrı bulgu; bu dalda düzeltilmedi):

| Paket | Kurulu | Açık |
|---|---|---|
| `laravel/framework` | v13.35.0 | 1 (düşük: Concurrency süreç çıktısı enjeksiyonu) |
| `symfony/http-foundation` | v8.1.9 | 4 (güvenilir vekil kısayolu, HEAD ile erişim kuralı atlatma, yol kuralı atlatma, istemcinin seçtiği host) |
| `symfony/http-kernel` | v8.1.1 | 1 (iletilen başlıklarla host/şema) |
| `symfony/routing` | v8.1.0 | 1 (host yer tutucusu) |
| `symfony/mime` | v8.1.0 | 1 (orta: e-posta başlık enjeksiyonu) |
| `symfony/filesystem` | v8.1.9 | 1 (`://` öneki kök sayılıyor) |

`SEC-07` kapandığında (ayrı dal, `composer update` + `composer check` + `composer audit` yeşil) etiket
komutları docs `operations/deployment/YAYIN-SIRASI.md` §3'te. Yayın kontrol listesi aynı dosyanın §2'si.

## 6. Docs dalı → `main`

```powershell
cd D:\Projects\davetkart\davetkart-docs
git switch main
git merge --no-ff docs/2026-11-16-faz-18-audit-fixes -m "Merge Faz 18 audit fix records into main"
git log --oneline -1
git status --short
# git push origin main
```

## 7. Dağıtım (etiketten sonra) ve duman testi

Sıra `operations/deployment/YAYIN-SIRASI.md`'de; burada yalnızca başlıklar:

1. §4.1 backend: `main` + `v1.1.0` it → sunucuda `bash deploy/deploy.sh` (`deploy` kullanıcısı).
2. §4.2 ara kontrol: `plans:export --check` yeşil.
3. §4.3 frontend: `main` + `v1.1.0` it → sözleşme `cmp` → `bash …/deploy-frontend.sh`.
4. **§4.4 Nginx (yeni, `v1.1.0`'da gerekli):** sudo yetkili kullanıcıyla
   `cd /var/www/davetkart/backend && sudo bash deploy/nginx/install.sh`.
5. **§6 duman testi:** `bash deploy/smoke/check-security-headers.sh https://davetkart.com` → altı `OK`,
   `SONUC: tamam`. Sonra bir hafta CSP gözlemi (K175).

## 8. Commit'ten sonra: elle işler

1. **Sunucuda (yayın günü):** §7'deki 4. ve 5. adım. `install.sh` kırmızı biterse site etkilenmez
   (eskiler geri konur); `nginx: [emerg]` satırını oku.
2. **Tarayıcıda (yayın günü):** DevTools → Network → belge yanıtında yedi başlık; Console'da
   `report-only` satırı olmamalı. Clickjacking denemesi: backend `FAZ-18.md` §18.6 "Elle doğrulama" 5.
3. **Bir hafta:** ödeme (kart açıksa Shopier'e gidiş-dönüş), galeriye fotoğraf, telefonda 3D şablon;
   Console'daki `report-only` satırlarını not et → zorlama kararı (yeni K).
4. **Yerel geliştirme veritabanı:** 20 Kasım'daki deneme sırasında yanlışlıkla bir kullanıcı (id 6) ve
   üç taslak yazıldı, aynı oturumda kimlikleriyle silindi. Tek iz: bir sonraki kullanıcı id'si 7.
   İstersen kendin bak: `select max(id) from users;` → 5.
