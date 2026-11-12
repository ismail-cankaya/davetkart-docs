# Değişiklik Günlüğü

Bu deponun kendi değişiklikleri. En yeni üstte.

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
