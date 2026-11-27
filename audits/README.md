# `audits/`

Denetim ve gözden geçirme raporları. Her denetim kendi tarihli klasöründe:
`YYYY-MM-DD-<konu>/` (ör. `2026-11-12-full-system-audit/`). Denetim kimliği `AUD-YYYY-MM-DD`.

| Tarih | Denetim | Konu | Sonuç |
|---|---|---|---|
| 2026-11-12 | [`AUD-2026-11-12`](2026-11-12-full-system-audit/README.md) | Genel sistem denetimi (mimari, güvenlik, test, frontend/E2E, işletim) | 62 bulgu: 🟠 6 · 🟡 29 · 🟢 22 · 💡 5 · [rapor](2026-11-12-full-system-audit/REPORT.md) |
| 2026-11-26 | [`AUD-2026-11-26`](2026-11-26-post-faz-19-scan/REPORT.md) | Faz 19 sonrası hata taraması: Hesap Ayarları'nın üç sayfası 500 (yerel şema geride) + kapılar, duman ve tarayıcı taraması | 🔴 1 · 🟠 2 · 🟡 3 · 🟢 3 · düzeltme [`phases/faz-20/`](../phases/faz-20/README.md) |
| 2026-11-27 | [`2026-11-27-main-gap-review`](2026-11-27-main-gap-review/REPORT.md) | Canlıdaki `main` ile yayın adayı `faz-21-backlog` arasında: yapılan planlar, kalan sunucu/AWS işleri ve kararlar (salt okunur) | 62 denetim bulgusunun kodu tamam (4'ü bilinçli plan/liste, `SEC-10` kısmi); yayın, etiket ve sunucu adımları yapılmadı · rehber [`YAYIN-REHBERI-v1.3.0.md`](../operations/deployment/YAYIN-REHBERI-v1.3.0.md) |
| 2026-11-27 | [`2026-11-27-release-v1.1-check`](2026-11-27-release-v1.1-check/REPORT.md) | Yayın öncesi son kontrol: dört kapı aday uçta (PHP 8.5, Node 24), Hat A/B/C kapanışı, `release-2026-11-28-v1.1` dalı | Engelleyen hata yok · kapılar yeşil (1354/1354, kapsam %96,0, e2e 6/6) · 🟢 1 (R1 e2e `LOG_LEVEL`) · 💡 4 |

Önceki raporlar (backend `claude/` klasöründen 2026-11-22'de taşındı, `ARC-05`; eşleme: [`_restructure/2026-11-backend-claude-map.md`](../_restructure/2026-11-backend-claude-map.md)):

| Tarih | Rapor | Konu |
|---|---|---|
| 2026-09-23 | [`2026-09-23-backend-review/GOZDEN-GECIRME-RAPORU.md`](2026-09-23-backend-review/GOZDEN-GECIRME-RAPORU.md) | Backend "bitti" gözden geçirmesi |
| 2026-09-24 | [`2026-09-24-test-audit/TEST-DENETIMI-2026-09-24.md`](2026-09-24-test-audit/TEST-DENETIMI-2026-09-24.md) | Test denetimi |
| 2026-10-09 | [`2026-10-09-code-review/GOZDEN-GECIRME-2026-10-09-BACKEND.md`](2026-10-09-code-review/GOZDEN-GECIRME-2026-10-09-BACKEND.md) | Backend gözden geçirmesi |
| 2026-10-09 | [`2026-10-09-code-review/GOZDEN-GECIRME-2026-10-09-FRONTEND.md`](2026-10-09-code-review/GOZDEN-GECIRME-2026-10-09-FRONTEND.md) | Frontend gözden geçirmesi |
