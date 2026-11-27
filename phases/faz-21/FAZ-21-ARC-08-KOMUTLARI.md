# Faz 21.17 — `ARC-08`: dal hijyeni, worktree'ler ve sürüm etiketleri (yalnızca liste ve komut)

> 27 Kasım 2026 · ajan **hiçbir komutu koşmadı**: dal silme, `worktree remove` ve `tag` yok. Tablolar yalnızca salt okunur
> komutlardan (`for-each-ref`, `branch --merged`, `worktree list`, `log`, `status`) üretildi. Komut blokları İsmail içindir.
> Bulgu: `AUD-2026-11-12` `findings/01-architecture.md` "ARC-08". Kayıtlar: `HAT-C-ACIK-HATALAR.md` #21, #29.
> Depo adının kendisi de yazım hatası taşıyor (`davetkart-frontent` → frontend); yeniden adlandırma GitHub'da ve bütün
> belgelerde yol değiştirir, bu listenin kapsamı dışında.

## 1. Dallar

"Birleşmiş" = `git branch --merged <entegrasyon>` listesinde (entegrasyon: kod depolarında `faz-21-backlog`, docs'ta
`docs/2026-11-27-faz-21-backlog`). Birleşmiş dal silinince commit'ler kaybolmaz (entegrasyon dalında duruyor). Uzak dallara
dokunulmaz.

### 1.1 backend (`davetkart-backend-php-laravel`, 34 dal, etiket: yok)

| Dal | Son commit | Birleşmiş mi | Uzak | Worktree | Not |
|---|---|---|---|---|---|
| `faz-21-backlog` | 2026-11-27 | evet | — | ana çalışma ağacı | kalır |
| `faz-20-critical-fixes` | 2026-11-26 | evet | — | — |  |
| `fix/2026-11-26-ops-06-deploy-maintenance` | 2026-11-26 | evet | — | — |  |
| `fix/2026-11-26-ops-13-setup-app-key` | 2026-11-26 | evet | — | — |  |
| `fix/2026-11-26-ops-11-local-sync` | 2026-11-26 | evet | — | — |  |
| `fix/2026-11-26-sec-51-symfony-patch` | 2026-11-26 | evet | — | — |  |
| `fix/2026-11-26-ops-10-schema-readiness` | 2026-11-26 | evet | — | — |  |
| `faz-19-fix` | 2026-11-26 | evet | origin/faz-19-fix | — |  |
| `faz-19-audit-fixes` | 2026-11-25 | evet | origin/faz-19-audit-fixes | — |  |
| `faz-18-audit-fixes` | 2026-11-20 | evet | origin/ccr-9a346997-bu6gve | — |  |
| `faz15-desing/claude-davetiye` | 2026-11-04 | evet | origin/faz15-desing/claude-davetiye | — | yazım: design |
| `test` | 2026-11-04 | evet | origin/test | — |  |
| `main` | 2026-10-26 | evet | origin/main | — | kalır |
| `release-v1.0` | 2026-10-26 | evet | origin/release-v1.0 | — |  |
| `faz-14-account-settings` | 2026-10-25 | evet | origin/faz-14-account-settings | — |  |
| `faz-13-payment-settings` | 2026-10-25 | evet | origin/faz-13-payment-settings | — |  |
| `faz-12-shopier-not-right` | 2026-10-25 | evet | origin/faz-12-shopier | — |  |
| `faz-11-hediye-kodu` | 2026-10-24 | evet | origin/faz-11-hediye-kodu | — |  |
| `faz-10` | 2026-10-23 | evet | origin/faz-10 | — |  |
| `release-2026-10-20` | 2026-10-20 | evet | origin/release-2026-10-20 | — |  |
| `copilot/fix-composer-check-job` | 2026-10-14 | evet | origin/copilot/fix-composer-check-job | — |  |
| `edit-test` | 2026-09-25 | evet | origin/edit-test | — |  |
| `payment-servide` | 2026-09-21 | evet | origin/payment-servide | — | yazım: service |
| `production-steps` | 2026-09-21 | evet | origin/production-steps | — |  |
| `media-confugration` | 2026-09-20 | evet | origin/media-confugration | — | yazım: configuration |
| `faz-9` | 2026-09-17 | evet | origin/faz-9 | — |  |
| `faz-8` | 2026-09-07 | evet | origin/faz-8 | — |  |
| `faz-5-6-and-7` | 2026-09-04 | evet | origin/faz-5 | — |  |
| `faz-4` | 2026-08-28 | evet | origin/faz-4 | — |  |
| `Enums` | 2026-07-29 | evet | origin/Enums | — | yazım: büyük harfli, konu belirsiz |
| `agents/faz-5-6-7-branch-renaming-testing` | 2026-07-29 | evet | — | davetkart/davetkart-backend-php-laravel.worktrees/faz-5-6-7-branch-renaming-testing |  |
| `agents/fix-git-error-fetch-phase5-files` | 2026-07-29 | evet | — | davetkart/davetkart-backend-php-laravel.worktrees/agents-fix-git-error-fetch-phase5-files |  |
| `agents/fix-git-error-phase-5-update` | 2026-07-29 | evet | — | davetkart/davetkart-backend-php-laravel.worktrees/fix-git-error-phase-5-update |  |
| `agents/git-hatasi-cozme-faz5-guncelleme` | 2026-07-29 | evet | — | davetkart/davetkart-backend-php-laravel.worktrees/agents-git-hatasi-cozme-faz5-guncelleme |  |

### 1.2 frontend (`davetkart-frontent`, 49 dal, etiket: yok)

| Dal | Son commit | Birleşmiş mi | Uzak | Worktree | Not |
|---|---|---|---|---|---|
| `faz-21-backlog` | 2026-11-27 | evet | — | ana çalışma ağacı | kalır |
| `faz-20-critical-fixes` | 2026-11-26 | evet | origin/faz-20-critical-fixes | — |  |
| `fix/2026-11-26-fe-06-not-found-page` | 2026-11-26 | evet | — | — |  |
| `fix/2026-11-26-fe-57-toast-stacking` | 2026-11-26 | evet | — | — |  |
| `fix/2026-11-26-fe-55-misleading-copy` | 2026-11-26 | evet | — | — |  |
| `fix/2026-11-26-fe-57-expired-session` | 2026-11-26 | evet | — | — |  |
| `fix/2026-11-26-ops-06-neutral-unavailable-message` | 2026-11-26 | evet | — | — |  |
| `faz-19-fix` | 2026-11-26 | evet | origin/faz-19-fix | — |  |
| `faz-19-audit-fixes` | 2026-11-24 | evet | origin/faz-19-audit-fixes | — |  |
| `fix/2026-11-23-fe-50-draft-lifecycle` | 2026-11-23 | evet | origin/fix/2026-11-23-fe-50-draft-lifecycle | — |  |
| `fix/2026-11-23-sec-09-email-verification` | 2026-11-23 | evet | — | — |  |
| `fix/2026-11-23-sec-05-password-policy` | 2026-11-23 | evet | origin/fix/2026-11-23-sec-05-password-policy | — |  |
| `fix/2026-11-23-fe-51-guest-media-upload` | 2026-11-23 | evet | origin/fix/2026-11-23-fe-51-guest-media-upload | — |  |
| `faz-18-audit-fixes` | 2026-11-20 | evet | origin/ccr-9a346997-bu6gve | — |  |
| `fix/2026-11-17-sec-02-refund-after-publish` | 2026-11-20 | evet | — | — |  |
| `fix/2026-11-16-sec-01-first-publish-once` | 2026-11-17 | evet | origin/fix/2026-11-16-sec-01-first-publish-once | — |  |
| `fix/2026-11-16-ops-01-release-alignment` | 2026-11-16 | evet | origin/fix/2026-11-16-ops-01-release-alignment | — |  |
| `design/claude-davetiye` | 2026-11-04 | evet | origin/design/yedi-davetiye | — |  |
| `fix/deps-audit` | 2026-10-26 | evet | origin/fix/deps-audit | — |  |
| `main` | 2026-10-26 | evet | origin/main | — | kalır |
| `faz-14-account-settings` | 2026-10-25 | evet | origin/faz-14-account-settings | — |  |
| `faz-13-payment-settings` | 2026-10-25 | evet | origin/faz-13-payment-settings | — |  |
| `faz-12-shopier` | 2026-10-24 | evet | origin/faz-12-shopier | — |  |
| `faz-11-hediye-kodu` | 2026-10-24 | evet | origin/faz-11-hediye-kodu | — |  |
| `design/konseptler` | 2026-10-23 | evet | origin/design/konseptler | — |  |
| `design/harita` | 2026-10-23 | evet | origin/design/harita | — |  |
| `design/kitap` | 2026-10-23 | evet | origin/design/kitap | — |  |
| `design/sergi` | 2026-10-23 | evet | origin/design/sergi | — |  |
| `design/konsept-ortak` | 2026-10-22 | evet | origin/design/konsept-ortak | — |  |
| `design/kagit` | 2026-10-16 | evet | origin/design/kagit | — |  |
| `new-desing` | 2026-10-15 | evet | origin/new-desing | — | yazım: design |
| `invitation-design` | 2026-10-03 | evet | origin/invitation-design | — |  |
| `faz10-backend` | 2026-10-02 | evet | origin/faz10-backend | — |  |
| `payment-desing` | 2026-10-01 | evet | origin/payment-desing | — | yazım: design |
| `new-page-desing` | 2026-09-25 | **hayır** | origin/new-page-desing | — | yazım: design |
| `edit-design-motion-principles` | 2026-09-25 | evet | origin/edit-design-motion-principles | — |  |
| `edit-desing` | 2026-09-20 | evet | origin/edit-desing | — | yazım: design |
| `fix-error` | 2026-09-16 | evet | origin/fix-error | — |  |
| `backend-compatibility` | 2026-09-16 | evet | origin/backend-compatibility | — |  |
| `edit-video` | 2026-08-19 | evet | origin/edit-video | — |  |
| `feature/subscription` | 2026-07-29 | evet | origin/feature/subscription | — |  |
| `edit/dashboard` | 2026-07-08 | evet | origin/edit/dashboard | — |  |
| `new/backend-connect` | 2026-07-07 | evet | origin/new/backend-connect | — |  |
| `new/translate` | 2026-07-07 | evet | origin/new/translate | — |  |
| `feature/new-desing-create` | 2026-07-07 | evet | origin/feature/new-desing-create | — | yazım: design |
| `feature/new-invitation` | 2026-07-06 | evet | origin/feature/new-invitation | — |  |
| `feature/auth-and-dom` | 2026-07-05 | evet | origin/feature/auth-and-dom | — |  |
| `fix/desing` | 2026-07-05 | evet | origin/fix/desing | — | yazım: design |
| `edit/architecture` | 2026-07-05 | evet | origin/edit/architecture | — |  |

### 1.3 docs (`davetkart-docs`, 9 dal, etiket: yok)

| Dal | Son commit | Birleşmiş mi | Uzak | Worktree | Not |
|---|---|---|---|---|---|
| `docs/2026-11-27-faz-21-backlog` | 2026-11-27 | evet | — | ana çalışma ağacı | kalır |
| `docs/2026-11-26-faz-21-plan` | 2026-11-27 | evet | — | — |  |
| `docs/2026-11-26-faz-20-critical-fixes` | 2026-11-26 | evet | origin/docs/2026-11-26-faz-20-critical-fixes | — |  |
| `docs/2026-11-20-faz-19-audit-fixes` | 2026-11-26 | evet | origin/docs/2026-11-20-faz-19-audit-fixes | — |  |
| `docs/2026-11-26-hat-a-e2e` | 2026-11-26 | evet | — | davetkart-hat-a/davetkart-docs |  |
| `docs/2026-11-25-hat-c-fixes` | 2026-11-25 | evet | — | davetkart-hat-c/davetkart-docs |  |
| `docs/2026-11-16-faz-18-audit-fixes` | 2026-11-20 | evet | origin/docs/2026-11-16-faz-18-audit-fixes | — |  |
| `audit/2026-11-12-full-system-audit` | 2026-11-16 | evet | origin/audit/2026-11-12-full-system-audit | — |  |
| `main` | 2026-11-16 | evet | origin/main | — | kalır |

## 2. Worktree'ler

| Yol | Dal / uç | Temiz mi (`git status --short`) | Not |
|---|---|---|---|
| `D:\Projects\davetkart\davetkart-backend-php-laravel.worktrees\agents-fix-git-error-fetch-phase5-files` | `agents/fix-git-error-fetch-phase5-files` (d4b9a6f 2026-07-29) | evet | Faz 5 dönemi ajan worktree'si |
| `D:\Projects\davetkart\davetkart-backend-php-laravel.worktrees\agents-git-hatasi-cozme-faz5-guncelleme` | `agents/git-hatasi-cozme-faz5-guncelleme` (d4b9a6f 2026-07-29) | evet | Faz 5 dönemi ajan worktree'si |
| `D:\Projects\davetkart\davetkart-backend-php-laravel.worktrees\faz-5-6-7-branch-renaming-testing` | `agents/faz-5-6-7-branch-renaming-testing` (d4b9a6f 2026-07-29) | evet | Faz 5 dönemi ajan worktree'si |
| `D:\Projects\davetkart\davetkart-backend-php-laravel.worktrees\fix-git-error-phase-5-update` | `agents/fix-git-error-phase-5-update` (d4b9a6f 2026-07-29) | evet | Faz 5 dönemi ajan worktree'si |
| `D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel` | ayrık uç (92ef1f2 2026-11-25) | evet | Faz 19 hattı |
| `D:\Projects\davetkart-hat-b\davetkart-backend-php-laravel` | ayrık uç (1605f38 2026-11-26) | evet | Faz 19 hattı |
| `D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel` | ayrık uç (70f3f7e 2026-11-25) | evet | Faz 19 hattı |
| `D:\Projects\davetkart-hat-a\davetkart-docs` | `docs/2026-11-26-hat-a-e2e` (0721a8b 2026-11-26) | evet | Faz 19 hattı |
| `D:\Projects\davetkart-hat-b\davetkart-docs` | ayrık uç (ee7f729 2026-11-26) | evet | Faz 19 hattı |
| `D:\Projects\davetkart-hat-c\davetkart-docs` | `docs/2026-11-25-hat-c-fixes` (6e57f1f 2026-11-25) | evet | Faz 19 hattı |
| `D:\Projects\davetkart-hat-b\davetkart-frontent` | — | git deposu **değil** (düz klasör) | elle bakılıp silinebilir |
| `D:\Projects\davetkart\davetkart-docs.worktrees\` | — | boş klasör, kayıtlı worktree yok | silinebilir |

## 3. Etiket önerisi

Kayıtlar: `phases/faz-19/FAZ-19-SEC-07-COMMIT-KOMUTLARI.md` §5 ("`v1.1.0` (Faz 18 + `SEC-07`)"), `FAZ-19-ARC-03-COMMIT-KOMUTLARI.md`
§6 ("`v1.2.0` etiketi: VERİLMEDİ … iki depoda `git tag -a v1.2.0 -m "Faz 19"`"), `operations/deployment/YAYIN-SIRASI.md` §3
("`v1.1.0`'dan önce, bugün sunucuda çalışan iki commit'i `v1.0.0` diye etiketle"), `HAT-C-ACIK-HATALAR.md` #21. Kural: yayın
adayı = `composer check` ✅ ve `composer audit` ✅ (K181); iki depo aynı etiketi taşır (K149).

| Etiket | backend | frontend | Gerekçe | Not |
|---|---|---|---|---|
| `v1.0.0` | sunucudaki commit (yerelde `main` = `03d3940`, 26 Eki) | sunucudaki commit (yerelde `main` = `47aedc8`, 26 Eki) | YAYIN-SIRASI §3: geri dönülecek ilk etiket | **Önce sunucuda doğrula** (`git -C /var/www/davetkart/backend rev-parse --short HEAD`); `main`'den tahmin etme |
| `v1.1.0` | `44f6022` ("Merge SEC-07 fix into faz-19-audit-fixes", 20 Kas) | `fefa647` (`faz-18-audit-fixes` ucu, 20 Kas) | Faz 18 + `SEC-07` (frontend'de `SEC-07` değişikliği yok) | O günkü `composer audit` yeşildi; 26 Kasım'da `SEC-51` yeni bir açık bildirdi, bu commit bugün `audit` kırmızı verir: yalnızca tarihî işaret |
| `v1.2.0` | `7f589e7` (`faz-19-fix` ucu, 26 Kas) | `5c68df3` (`faz-19-fix` ucu, 26 Kas) | Faz 19 sonu (HAT-C #21) | ⚠️ Bu uçta `composer audit` kırmızı (`SEC-51`, AUD-2026-11-26) → K181'e göre yayın adayı **değil**. Öneri: `v1.2.0` = `faz-20-critical-fixes` ucu (backend `70edfcf`, frontend `f774f1b`; Faz 19 + 20, audit yeşil). Karar İsmail'in |
| (sonra) `v1.3.0` | `faz-21-backlog` `main`'e birleşince | aynı | Faz 21 | kayıtta yok; öneri |

## 4. İsmail'in koşacağı komutlar

Sıra: önce §4.1 (worktree'ler; kendi dalını tutan worktree varken dal silinemez), sonra §4.2 (dallar), en son §4.3 (etiket,
`main` birleştirmesi ve kapılardan sonra). Her blok `git status --short` ile biter. **Push yok.** `git branch -d` (küçük `d`) birleşmemiş
dalı reddeder; `-D` kullanma. Birleşmemiş dallar (yukarıda "hayır") listelenmedi: önce içeriklerine bak.

### 4.1 Temiz worktree'ler

```powershell
# 4.1a — backend Faz 5 dönemi ajan worktree'leri (dördü de temiz)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git worktree remove "D:\Projects\davetkart\davetkart-backend-php-laravel.worktrees\agents-fix-git-error-fetch-phase5-files"
git worktree remove "D:\Projects\davetkart\davetkart-backend-php-laravel.worktrees\agents-git-hatasi-cozme-faz5-guncelleme"
git worktree remove "D:\Projects\davetkart\davetkart-backend-php-laravel.worktrees\faz-5-6-7-branch-renaming-testing"
git worktree remove "D:\Projects\davetkart\davetkart-backend-php-laravel.worktrees\fix-git-error-phase-5-update"
git worktree list
git status --short
```

```powershell
# 4.1b — Faz 19 hat worktree'leri (backend)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git worktree remove "D:\Projects\davetkart-hat-a\davetkart-backend-php-laravel"
git worktree remove "D:\Projects\davetkart-hat-b\davetkart-backend-php-laravel"
git worktree remove "D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel"
git worktree prune
git worktree list
git status --short
```

```powershell
# 4.1c — Faz 19 hat worktree'leri (docs)
cd D:\Projects\davetkart\davetkart-docs
git worktree remove "D:\Projects\davetkart-hat-a\davetkart-docs"
git worktree remove "D:\Projects\davetkart-hat-b\davetkart-docs"
git worktree remove "D:\Projects\davetkart-hat-c\davetkart-docs"
git worktree prune
git worktree list
git status --short
```

`D:\Projects\davetkart-hat-b\davetkart-frontent` git deposu değil, `davetkart-hat-b` altındaki `*.log` dosyaları da kayıt dışı:
içine bakıp elle silebilirsin. `D:\Projects\davetkart\davetkart-docs.worktrees\` boş.

### 4.2 Birleşmiş dallar (`git branch -d`, tek tek)

**a) Konu dalları: hemen.** **b) Entegrasyon ve sürüm dalları (`faz-*`, `release-*`, docs `…-faz-…`): yalnızca `faz-21-backlog`
(docs dalı) `main`'e birleşip itildikten sonra**; kayıtlar ve PR'lar bu adlara bağlantı veriyor. Uzak dalı olanlarda `-d`
yerel commit'ler uzağa itilmemişse reddeder (güvenli).

```powershell
# 4.2a — backend: konu dalları (16 dal)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-21-backlog
git branch -d fix/2026-11-26-ops-06-deploy-maintenance
git branch -d fix/2026-11-26-ops-13-setup-app-key
git branch -d fix/2026-11-26-ops-11-local-sync
git branch -d fix/2026-11-26-sec-51-symfony-patch
git branch -d fix/2026-11-26-ops-10-schema-readiness
git branch -d test
git branch -d copilot/fix-composer-check-job
git branch -d edit-test
git branch -d payment-servide
git branch -d production-steps
git branch -d media-confugration
git branch -d Enums
git branch -d agents/faz-5-6-7-branch-renaming-testing  # önce worktree kaldırılmalı (§2)
git branch -d agents/fix-git-error-fetch-phase5-files  # önce worktree kaldırılmalı (§2)
git branch -d agents/fix-git-error-phase-5-update  # önce worktree kaldırılmalı (§2)
git branch -d agents/git-hatasi-cozme-faz5-guncelleme  # önce worktree kaldırılmalı (§2)
git branch --list
git status --short
```

```powershell
# 4.2b — backend: entegrasyon dalları, main birleşmesinden SONRA (16 dal)
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-21-backlog
git branch -d faz-20-critical-fixes
git branch -d faz-19-fix
git branch -d faz-19-audit-fixes
git branch -d faz-18-audit-fixes
git branch -d faz15-desing/claude-davetiye
git branch -d release-v1.0
git branch -d faz-14-account-settings
git branch -d faz-13-payment-settings
git branch -d faz-12-shopier-not-right
git branch -d faz-11-hediye-kodu
git branch -d faz-10
git branch -d release-2026-10-20
git branch -d faz-9
git branch -d faz-8
git branch -d faz-5-6-and-7
git branch -d faz-4
git branch --list
git status --short
```

```powershell
# 4.2a — frontend: konu dalları (37 dal)
cd D:\Projects\davetkart\davetkart-frontent
git switch faz-21-backlog
git branch -d fix/2026-11-26-fe-06-not-found-page
git branch -d fix/2026-11-26-fe-57-toast-stacking
git branch -d fix/2026-11-26-fe-55-misleading-copy
git branch -d fix/2026-11-26-fe-57-expired-session
git branch -d fix/2026-11-26-ops-06-neutral-unavailable-message
git branch -d fix/2026-11-23-fe-50-draft-lifecycle
git branch -d fix/2026-11-23-sec-09-email-verification
git branch -d fix/2026-11-23-sec-05-password-policy
git branch -d fix/2026-11-23-fe-51-guest-media-upload
git branch -d fix/2026-11-17-sec-02-refund-after-publish
git branch -d fix/2026-11-16-sec-01-first-publish-once
git branch -d fix/2026-11-16-ops-01-release-alignment
git branch -d design/claude-davetiye
git branch -d fix/deps-audit
git branch -d design/konseptler
git branch -d design/harita
git branch -d design/kitap
git branch -d design/sergi
git branch -d design/konsept-ortak
git branch -d design/kagit
git branch -d new-desing
git branch -d invitation-design
git branch -d payment-desing
git branch -d edit-design-motion-principles
git branch -d edit-desing
git branch -d fix-error
git branch -d backend-compatibility
git branch -d edit-video
git branch -d feature/subscription
git branch -d edit/dashboard
git branch -d new/backend-connect
git branch -d new/translate
git branch -d feature/new-desing-create
git branch -d feature/new-invitation
git branch -d feature/auth-and-dom
git branch -d fix/desing
git branch -d edit/architecture
git branch --list
git status --short
```

```powershell
# 4.2b — frontend: entegrasyon dalları, main birleşmesinden SONRA (9 dal)
cd D:\Projects\davetkart\davetkart-frontent
git switch faz-21-backlog
git branch -d faz-20-critical-fixes
git branch -d faz-19-fix
git branch -d faz-19-audit-fixes
git branch -d faz-18-audit-fixes
git branch -d faz-14-account-settings
git branch -d faz-13-payment-settings
git branch -d faz-12-shopier
git branch -d faz-11-hediye-kodu
git branch -d faz10-backend
git branch --list
git status --short
```

```powershell
# 4.2a — docs: konu dalları (3 dal)
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-27-faz-21-backlog
git branch -d docs/2026-11-26-hat-a-e2e  # önce worktree kaldırılmalı (§2)
git branch -d docs/2026-11-25-hat-c-fixes  # önce worktree kaldırılmalı (§2)
git branch -d audit/2026-11-12-full-system-audit
git branch --list
git status --short
```

```powershell
# 4.2b — docs: entegrasyon dalları, main birleşmesinden SONRA (4 dal)
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-27-faz-21-backlog
git branch -d docs/2026-11-26-faz-21-plan
git branch -d docs/2026-11-26-faz-20-critical-fixes
git branch -d docs/2026-11-20-faz-19-audit-fixes
git branch -d docs/2026-11-16-faz-18-audit-fixes
git branch --list
git status --short
```

### 4.3 Etiketler (kapılar yeşil ve `main` birleştirmesinden sonra)

Önce `v1.0.0` için sunucudaki commit'leri öğren (YAYIN-SIRASI §3). Sonra her etiket için iki depoda aynı ad (K149), önce backend.

```powershell
# 4.3a — backend
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git tag -a v1.0.0 <sunucudaki-backend-commit> -m "Release v1.0.0: first production deploy (26 Oct)"
git tag -a v1.1.0 44f6022 -m "Release v1.1.0: Phase 18 audit fixes + SEC-07"
git tag -a v1.2.0 <seçilen-commit> -m "Release v1.2.0: Phase 19 (+ Phase 20 if faz-20-critical-fixes)"
git tag -l "v1*"
git status --short
```

```powershell
# 4.3b — frontend
cd D:\Projects\davetkart\davetkart-frontent
git tag -a v1.0.0 <sunucudaki-frontend-commit> -m "Release v1.0.0: first production deploy (26 Oct)"
git tag -a v1.1.0 fefa647 -m "Release v1.1.0: Phase 18 audit fixes"
git tag -a v1.2.0 <seçilen-commit> -m "Release v1.2.0: Phase 19 (+ Phase 20 if faz-20-critical-fixes)"
git tag -l "v1*"
git status --short
```

Etiketleri itmek (`git push origin v1.x.0`) dağıtım sırasının parçası: YAYIN-SIRASI §4.
