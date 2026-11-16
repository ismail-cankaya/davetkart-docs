# Değişiklik Günlüğü

Bu deponun kendi değişiklikleri. En yeni üstte.

## 2026-11-16 — Faz 18.1 `OPS-01` kayıtları (`docs/2026-11-16-faz-18-audit-fixes`)

- Yayın sırası ve sürüm etiketi çalıştırma kitabı [`operations/deployment/YAYIN-SIRASI.md`](operations/deployment/YAYIN-SIRASI.md); K146–K150 ([`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md), `DECISION-INDEX.md`: sıradaki boş numara K151, K128–K145 için ⚠️ notu); [`phases/faz-18/FAZ-18-OPS-01-COMMIT-KOMUTLARI.md`](phases/faz-18/FAZ-18-OPS-01-COMMIT-KOMUTLARI.md); `phases/faz-18/README.md`, `operations/README.md`, `decisions/README.md` satırları.
- Aynı gün: `phases/faz-18/README.md` `OPS-01` satırı ve `FAZ-18-OPS-01-COMMIT-KOMUTLARI.md` gerçek duruma göre güncellendi (atılan commit'lerin kimlikleri, kalan üç blok).

## 2026-11-16 — Faz 18 prompt'ları (`docs/2026-11-16-faz-18-audit-fixes`)

- `AUD-2026-11-12`'nin altı yüksek (🟠) bulgusu için altı prompt: `prompts/PROMPT-FAZ-18-{1..6}-*.md`; takip tablosu [`phases/faz-18/README.md`](phases/faz-18/README.md); `prompts/README.md` ve `phases/README.md` satırları.

## 2026-11-15 — Genel sistem denetimi (`audit/2026-11-12-full-system-audit`)

- `AUD-2026-11-12`: [`audits/2026-11-12-full-system-audit/`](audits/2026-11-12-full-system-audit/README.md) eklendi (rapor, beş bulgu dosyası, kanıt klasörü); `audits/README.md` listesine işlendi. Başka doküman değişmedi.

## 2026-11-12 — Depo düzenlemesi (`docs/2026-11-12-restructure`)

- Başlangıç commit'i: depo o anki hâliyle git'e alındı. Eski `davetkart-claude` deposunun `.git`'i
  depo dışına (`D:\Projects\davetkart\_backup\davetkart-claude.git`) taşındı; eski geçmiş o uzak depoda.
- `.gitignore`: kod arşivleri (`.tgz`, `.tar`, `.bundle`) git dışı; üçünde `.env` var.
- Klasör yapısı: `context/`, `decisions/`, `phases/`, `prompts/`, `audits/`, `operations/`,
  `product/`, `notes/`, `archive/`. 277 dosya taşındı, içerikleri değişmedi.
- Arşive giden 3 dosyaya tek satırlık arşiv bandı eklendi; `archive/README.md`.
- Yeni: `decisions/DECISION-INDEX.md` (K1–K127), klasör `README.md`'leri, kök `README.md`,
  `CLAUDE.md`, `AGENTS.md`, bu dosya.
- Kayıtlar: [`_restructure/`](_restructure/REPORT.md) (envanter, taşıma planı, rapor, betikler).
