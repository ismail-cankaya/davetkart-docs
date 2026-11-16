# Faz 18.2 — `OPS-02` commit komutları

> **Tarih:** 16 Kasım 2026 · **Kararlar:** K151–K157 · **Faz kaydı:** backend `docs/rehber/fazlar/FAZ-18.md` §18.2
> Her blok bir commit. Dosyalar tek tek, açık yolla eklenir; joker, klasör yolu ve `-A` yok.
> Her blok `git status --short` ile biter. Frontend bu bulguda **değişmedi**; bloğu yok.

## Başlamadan: çalışma ağacında ne olmalı

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-ops-02-db-backup
git status --short --untracked-files=all
```

Beklenen (dokuz satır, başka bir şey yok):

```
 M docs/rehber/fazlar/FAZ-18.md
 M docs/rehber/fazlar/README.md
?? deploy/backup/backup.env.example
?? deploy/backup/pg-dump.sh
?? deploy/backup/restore-drill.ps1
?? deploy/cron/davetkart-backup
?? docs/rehber/deploy/backup/pg-dump.md
?? docs/rehber/deploy/backup/restore-drill.md
?? docs/rehber/deploy/cron/davetkart-backup.md
```

## 1. Backend

```powershell
# 18.2.1 — yedek betiği, ayar dosyası şablonu ve kılavuzu
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-ops-02-db-backup
git add deploy/backup/pg-dump.sh
git add deploy/backup/backup.env.example
git add docs/rehber/deploy/backup/pg-dump.md
git commit -m "18.2.1 - feat(deploy): Add nightly pg_dump backup script with verification and manifest"
git status --short
```

```powershell
# 18.2.2 — cron satırı ve kılavuzu
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-ops-02-db-backup
git add deploy/cron/davetkart-backup
git add docs/rehber/deploy/cron/davetkart-backup.md
git commit -m "18.2.2 - feat(deploy): Add cron entry for the nightly database backup"
git status --short
```

```powershell
# 18.2.3 — geri yükleme provası betiği ve kılavuzu
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-ops-02-db-backup
git add deploy/backup/restore-drill.ps1
git add docs/rehber/deploy/backup/restore-drill.md
git commit -m "18.2.3 - feat(deploy): Add restore drill script with single-table recovery mode"
git status --short
```

```powershell
# 18.2.4 — faz kaydı
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch fix/2026-11-16-ops-02-db-backup
git add docs/rehber/fazlar/FAZ-18.md
git add docs/rehber/fazlar/README.md
git commit -m "18.2.4 - docs(phases): Record Phase 18.2 (OPS-02 database backup and restore drill)"
git status --short                                   # boş olmalı
```

## 2. Docs

```powershell
# 18.2.5 — çalıştırma kitabı, kararlar, takip tablosu
cd D:\Projects\davetkart\davetkart-docs
git switch docs/2026-11-16-faz-18-audit-fixes
git add operations/deployment/YEDEK-VE-GERI-YUKLEME.md
git add operations/deployment/YAYIN-PLANI.md
git add operations/deployment/YAYIN-SIRASI.md
git add operations/README.md
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md
git add decisions/DECISION-INDEX.md
git add phases/faz-18/README.md
git add phases/faz-18/FAZ-18-OPS-02-COMMIT-KOMUTLARI.md
git add CHANGELOG.md
git commit -m "docs(operations): Add backup and restore runbook and K151-K157 for OPS-02"
git status --short                                   # boş olmalı
# git push -u origin docs/2026-11-16-faz-18-audit-fixes
```

## 3. Birleştirme (yalnızca backend)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch faz-18-audit-fixes
git merge --no-ff fix/2026-11-16-ops-02-db-backup -m "Merge OPS-02 fix into faz-18-audit-fixes"
git status --short
# git push -u origin faz-18-audit-fixes
# git push -u origin fix/2026-11-16-ops-02-db-backup
```

🔴 Birleştirmeyi atlama: sonraki prompt (18.3, `SEC-01`) backend'de
`git branch --merged faz-18-audit-fixes | Select-String "ops-02-"` ile bakar; boş dönerse durur.

Bitince `phases/faz-18/README.md`'de `OPS-02` satırını `birleşti` yap.

## 4. Commit'ten sonra: elle işler

Commit bulguyu **kodda** kapatır; yedek ancak aşağıdakilerle gerçek olur
([`operations/deployment/YEDEK-VE-GERI-YUKLEME.md`](../../operations/deployment/YEDEK-VE-GERI-YUKLEME.md)):

1. Yedek bucket'ı ve `davetkart-backup` kimliği (§2–§3).
2. Sunucu: AWS CLI (**karar**, §4.1), ayar dosyası, kurulu kopya, elle ilk koşu, cron (§4).
3. Doğrulama ve dört olumsuz deneme (§5).
4. İlk üretim provası, süre prova kaydına (§6). **Kayıt açılmadan önce.**

Yerelde kalan prova veritabanları (geliştirme verisinin kopyası; istediğinde sil):

```powershell
& 'C:\Program Files\PostgreSQL\18\bin\dropdb.exe' -h 127.0.0.1 -p 5432 -U postgres davetkart_restore_drill
& 'C:\Program Files\PostgreSQL\18\bin\dropdb.exe' -h 127.0.0.1 -p 5432 -U postgres davetkart_restore_side
```
