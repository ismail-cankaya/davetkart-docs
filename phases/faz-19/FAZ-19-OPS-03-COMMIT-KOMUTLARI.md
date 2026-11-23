# Faz 19.7 — `OPS-03` (izleme ve hazır olma ucu) commit komutları

> **Tarih:** 22 Kasım 2026 · **Kararlar:** K255, K256 · **Kayıt:** [`kayit/19-07-OPS-03.md`](kayit/19-07-OPS-03.md)
> **Dallar:** backend `fix/2026-11-22-ops-03-health-monitoring` · docs `docs/2026-11-22-ops-03-health-monitoring` · frontend değişmedi.
> Komutları İsmail çalıştırır. ⚠️ Backend `composer check` bu daldan bağımsız nedenle kırmızı ([`HAT-C-ACIK-HATALAR.md`](HAT-C-ACIK-HATALAR.md) #1, #11).

## Başlamadan

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git branch --show-current                     # fix/2026-11-22-ops-03-health-monitoring
git status --short --untracked-files=all
```

```
 M bootstrap/providers.php
 M routes/api.php
 M routes/console.php
 M tests/Feature/MaintenanceTest.php
?? app/Contracts/DiskUsage.php
?? app/Contracts/HealthCheck.php
?? app/Http/Controllers/Api/V1/ReadinessController.php
?? app/Listeners/ReportFailedJob.php
?? app/Providers/MonitoringServiceProvider.php
?? app/Support/Health/DatabaseCheck.php
?? app/Support/Health/DiskSpaceCheck.php
?? app/Support/Health/LocalDiskUsage.php
?? app/Support/Health/QueueBacklogCheck.php
?? app/Support/Health/ReadinessProbe.php
?? app/Support/Health/RecordSchedulerHeartbeat.php
?? app/Support/Health/SchedulerHeartbeatCheck.php
?? config/health.php
?? docs/rehber/app/Listeners/ReportFailedJob.md
?? docs/rehber/app/Providers/MonitoringServiceProvider.md
?? docs/rehber/app/Support/Health/ReadinessProbe.md
?? docs/rehber/config/health.md
?? docs/rehber/tests/Feature/ReadinessTest.md
?? tests/Feature/ReadinessTest.php
```

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git branch --show-current                     # docs/2026-11-22-ops-03-health-monitoring
git status --short --untracked-files=all
```

```
 M operations/README.md
 M phases/faz-19/HAT-C-ACIK-HATALAR.md
?? operations/deployment/IZLEME.md
?? phases/faz-19/FAZ-19-OPS-03-COMMIT-KOMUTLARI.md
?? phases/faz-19/kayit/19-07-OPS-03.md
```

## 1. Backend — 19.7.1 (hazır olma ucu)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git add app/Contracts/HealthCheck.php
git add app/Contracts/DiskUsage.php
git add app/Support/Health/DatabaseCheck.php
git add app/Support/Health/QueueBacklogCheck.php
git add app/Support/Health/SchedulerHeartbeatCheck.php
git add app/Support/Health/DiskSpaceCheck.php
git add app/Support/Health/LocalDiskUsage.php
git add app/Support/Health/ReadinessProbe.php
git add app/Http/Controllers/Api/V1/ReadinessController.php
git add app/Providers/MonitoringServiceProvider.php
git add bootstrap/providers.php
git add config/health.php
git add routes/api.php
git add docs/rehber/app/Support/Health/ReadinessProbe.md
git add docs/rehber/app/Providers/MonitoringServiceProvider.md
git add docs/rehber/config/health.md
git add docs/rehber/tests/Feature/ReadinessTest.md
git add tests/Feature/ReadinessTest.php
git commit -m "19.7.1 - feat(health): Add a readiness endpoint that checks the database, queue, scheduler and disk (K255)"
git status --short
```

## 2. Backend — 19.7.2 (zamanlayıcı kalp atışı)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git add app/Support/Health/RecordSchedulerHeartbeat.php
git add routes/console.php
git add tests/Feature/MaintenanceTest.php
git commit -m "19.7.2 - feat(health): Record a scheduler heartbeat every minute for the readiness check (K255)"
git status --short
```

## 3. Backend — 19.7.3 (başarısız iş bildirimi)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git add app/Listeners/ReportFailedJob.php
git add docs/rehber/app/Listeners/ReportFailedJob.md
git commit -m "19.7.3 - feat(queue): Report failed jobs at critical level without payload or message (K256)"
git status --short
```

Not: `ReadinessTest` üç commit'in testlerini birlikte taşır; 19.7.1'de dosyanın tamamı eklenir, ara commit'lerde
kalp atışı ve dinleyici testleri 19.7.2/19.7.3 gelene kadar kırmızıdır. Ara commit'lerde yeşil istersen 1–3'ü tek commit yap.

## 4. Docs — 19.7.5 (çalıştırma kitabı + kayıt)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add operations/deployment/IZLEME.md
git add operations/README.md
git commit -m "docs(operations): Add the monitoring runbook for the readiness endpoint, Sentry and the uptime monitor"
git add phases/faz-19/kayit/19-07-OPS-03.md
git add phases/faz-19/HAT-C-ACIK-HATALAR.md
git add phases/faz-19/FAZ-19-OPS-03-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add the OPS-03 record, commit commands and new lane C open issues (K255, K256)"
git status --short
```

## 5. Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-22-ops-03-health-monitoring -m "Merge OPS-03 into faz-19-audit-fixes"
git status --short
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-22-ops-03-health-monitoring -m "Merge OPS-03 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md` (olası yerler: `routes/console.php`, `routes/api.php`, `tests/Feature/MaintenanceTest.php`).
