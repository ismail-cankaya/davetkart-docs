# Faz 19.28 — `ARC-03` (K18 cırcırı) commit komutları + Faz 19 kapanışı

> **Tarih:** 25 Kasım 2026 · **Hat:** C · **Karar:** K259 · **Dallar:** backend `fix/2026-11-24-arc-03-k18-ratchet` ·
> docs `docs/2026-11-24-arc-03-k18-ratchet` (entegrasyon dallarından). Frontend değişmedi.
> §1–§4'ü İsmail'in 23 Kasım izniyle ajan çalıştırdı (kayıt için). **§5 ve sonrası İsmail'in.**

## 1. Backend — 19.28.1–19.28.5 (çalıştırıldı)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
# 19.28.1 komut + test + composer.json + CI + kılavuzlar
git add app/Support/K18Inspector.php
git add app/Console/Commands/CheckK18.php
git add tests/Feature/K18CheckTest.php
git add composer.json
git add .github/workflows/ci.yml
git add docs/rehber/app/Support/K18Inspector.md
git add docs/rehber/app/Console/Commands/CheckK18.md
git add docs/rehber/tests/Feature/K18CheckTest.md
git add docs/rehber/PROJE-KOMUTLARI.md
git commit -m "19.28.1 - feat(quality): Add the k18:check ratchet for short comments and guides to composer check (K259)"
# 19.28.2
git add routes/api.php
git add docs/rehber/routes/api.md
git commit -m "19.28.2 - docs(routes): Move the long route comments into the routes guide (K259)"
# 19.28.3
git add app/Providers/AppServiceProvider.php
git add docs/rehber/app/Providers/AppServiceProvider.md
git commit -m "19.28.3 - docs(providers): Move the long AppServiceProvider comments into its guide (K259)"
# 19.28.4 — klasör başına bir commit (pricing, account actions, account requests, notifications, payment, providers);
# dosyalar tek tek, mesajlar: "19.28.4 - docs(<alan>): Add the missing guides for ... (K259)"
# 19.28.5
git add docs/rehber/fazlar/FAZ-19.md
git add docs/rehber/fazlar/README.md
git commit -m "19.28.5 - docs(faz-19): Record ARC-03 and the Faz 19 closure summary (K259)"
git status --short
```

## 2. Docs — 19.28.6 (çalıştırıldı)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md
git add decisions/DECISION-INDEX.md
git add CHANGELOG.md
git add phases/faz-19/README.md
git add phases/README.md
git add phases/faz-19/FAZ-19-ARC-03-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Record ARC-03 (K259) and close Faz 19"
git status --short
```

## 3. Birleştirme: entegrasyon dalları (ana klasör, çalıştırıldı)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-24-arc-03-k18-ratchet -m "Merge ARC-03 into faz-19-audit-fixes"
git status --short
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-24-arc-03-k18-ratchet -m "Merge ARC-03 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

## 4. Kapılar (25 Kasım, bu dalda)

| Kapı | Sonuç |
|---|---|
| `composer check` | ❌ PHPStan iç hatası (#11) zinciri durdurdu; geri kalanı tek tek ✅ (Pint, üç `--check`, `k18:check`, 1271/1271 test) |
| `composer audit` | ✅ |
| Frontend `npm ci` + `npm run check` · `npm run e2e` · `npm run perf` | ✅ · ✅ 4/4 · ✅ bütçe içinde |

## 5. İsmail: `main`'e birleştirme (`operations/deployment/YAYIN-SIRASI.md` sırası: önce backend, sonra frontend)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch main
git merge --no-ff faz-19-audit-fixes -m "Merge Faz 19 audit fixes into main"
git status --short
cd D:\Projects\davetkart\davetkart-frontent
git switch main
git merge --no-ff faz-19-audit-fixes -m "Merge Faz 19 audit fixes into main"
git status --short
```

## 6. 🔴 `v1.2.0` etiketi: **VERİLMEDİ**

Prompt §11.5: kapılardan biri kırmızıysa etiket yok. Engel: `composer check` PHPStan iç hatası
(`Class mixed was not found`, `HAT-C-ACIK-HATALAR.md` #11). PHPStan yeşil olunca: `composer check` ✅ + `composer audit` ✅
(K181) görüldükten sonra iki depoda `git tag -a v1.2.0 -m "Faz 19"` ve `git push origin v1.2.0`.

## 7. İsmail: docs dalı `main`'e

```powershell
cd D:\Projects\davetkart\davetkart-docs
git switch main
git merge --no-ff docs/2026-11-20-faz-19-audit-fixes -m "Merge Faz 19 docs into main"
git status --short
```

## 8. Dağıtım ve duman testleri (etiketten sonra, sunucuda)

1. `deploy/deploy.sh` (backend), ardından frontend derlemesi (`YAYIN-SIRASI.md`). Yeni Nginx parçaları: önizleme botu
   eşlemesi (`FE-04`), self-host fontlar (`SEC-12`) → `install.sh` ile.
2. `deploy/smoke/check-security-headers.sh https://davetkart.com` → bütün satırlar OK (K178).
3. `curl -s -o /dev/null -w '%{http_code}' https://davetkart.com/api/health` → `200` (K255).
4. `curl -s -A 'WhatsApp/2.23' https://davetkart.com/invite/<yayındaki-davetiye> | grep og:title` → davetiye başlığı (K230).
5. `php artisan about` → medya diski `s3` (K183), posta sürücüsü `log` değil (K185).
