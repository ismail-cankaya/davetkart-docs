# Backend `claude/` → `davetkart-docs` eşleme tablosu (2026-11-22, `ARC-05`)

> 12 Kasım düzenlemesi ([`REPORT.md`](REPORT.md) §4) backend deposunun kendi `claude/` klasörünü kapsam
> dışı bırakmıştı. Faz 19.4'te (`ARC-05`) 22 takipli dosya buraya **birebir** kopyalandı (blob kimlikleri
> backend'deki ile aynı), ardından yalnızca göreli bağlantılar düzeltildi. Backend'de yalnızca
> `claude/README.md` (yönlendirme) kalır. Yer kuralı: [`../CLAUDE.md`](../CLAUDE.md) §3; adlar korundu (§4).

## 1. Taşınan dosyalar

| Backend (eski) | Docs (yeni) |
|---|---|
| `claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md` … `-EK-FAZ-9.md` | [`decisions/addenda/`](../decisions/addenda/) (aynı adlar) |
| `claude/OKUBENI-FAZ-5.md` · `claude/FAZ-5-DEVIR.md` | [`phases/faz-05/`](../phases/faz-05/) |
| `claude/FAZ-6-DEVIR.md` | [`phases/faz-06/`](../phases/faz-06/) |
| `claude/FAZ-7-DEVIR.md` | [`phases/faz-07/`](../phases/faz-07/) |
| `claude/FAZ-9-DEVIR.md` | [`phases/faz-09/`](../phases/faz-09/) |
| `claude/FAZ-10-PLANI.md` | [`phases/faz-10/`](../phases/faz-10/) |
| `claude/GOZDEN-GECIRME-RAPORU.md` (23 Eylül) | [`audits/2026-09-23-backend-review/`](../audits/2026-09-23-backend-review/) |
| `claude/TEST-DENETIMI-2026-09-24.md` | [`audits/2026-09-24-test-audit/`](../audits/2026-09-24-test-audit/) |
| `claude/GOZDEN-GECIRME-2026-10-09-BACKEND.md` · `-FRONTEND.md` | [`audits/2026-10-09-code-review/`](../audits/2026-10-09-code-review/) |
| `claude/PROMPT-FAZ-6.md` · `-7.md` · `-7-KAPANIS.md` · `-7-TEK-SEFERDE.md` · `-8.md` · `-9.md` | [`prompts/`](../prompts/) (aynı adlar) |
| `claude/Notlar/04-FAZ-5-FRONTEND-YAPILACAKLAR.md` | [`notes/`](../notes/) |

Kopyalarda düzeltilen bağlantılar (13): `FAZ-5-DEVIR.md` (2), `OKUBENI-FAZ-5.md` (4), `FAZ-6-DEVIR.md` (1),
`EK-FAZ-5.md` (1), `PROMPT-FAZ-7.md` (1), `PROMPT-FAZ-7-TEK-SEFERDE.md` (1). Metindeki `claude/…` geçişleri
(bağlantı olmayan) tarihsel içerik olarak bırakıldı (`CLAUDE.md` §8).

## 2. Daha önce taşınmış olup backend'de eski yolla anılanlar

| Backend metnindeki eski yol | Docs |
|---|---|
| `claude/PHP-LARAVEL-SETUP.md` | `context/PHP-LARAVEL-SETUP.md` |
| `claude/PHP-LARAVEL-SETUP-EK-FAZ-11.md` | `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` |
| `claude/Notlar/03-FRONTEND-YAPILACAKLAR.md` | `notes/03-FRONTEND-YAPILACAKLAR.md` |
| `claude/PROMPT-FAZ-12.md` | `prompts/PROMPT-FAZ-12.md` |
| `claude/FAZ-13-PLANI.md` · `claude/FAZ-14-PLANI.md` | **hiçbir depoda yok** (iki deponun git geçmişinde de) |

## 3. Backend'den bu depoya atıf biçimi

Göreli bağlantı depolar arasında çalışmaz (GitHub'da ayrı depolar). Tek biçim, kod biçiminde düz metin:
`` `davetkart-docs: <bu depodaki yol>` `` (ör. `` `davetkart-docs: context/PHP-LARAVEL-SETUP.md` ``).
Kılavuz: backend `docs/rehber/kavramlar/davetkart-docs-yollari.md`.
