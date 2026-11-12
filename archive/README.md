# `archive/`

Geçersiz kılınmış ya da işi bitmiş dosyalar. **Silinmez, değiştirilmez.** Her dosyanın en üstünde
tek satırlık bir arşiv bandı vardır (bant konamayan dosyalar aşağıda belirtilmiştir).

| Dosya | Eski yol | Neden arşivde | Yerine geçen |
|---|---|---|---|
| [`PROMPT.md`](PROMPT.md) | `claude/PROMPT.md` | 4 Eylül 2026 başlangıç prompt'u; "sıradaki iş: Faz 7'yi kapat" diyor | [`../context/PHP-LARAVEL-SETUP.md`](../context/PHP-LARAVEL-SETUP.md) + [`../prompts/`](../prompts/README.md) |
| [`PROMPT-ARSIV-FAZ-4.md`](PROMPT-ARSIV-FAZ-4.md) | `claude/PROMPT-ARSIV-FAZ-4.md` | PROMPT.md'nin Faz 4'e kadarki sürümü | `PROMPT.md` (o da arşivde) |
| [`davetkart-claude/README.md`](davetkart-claude/README.md) | `claude/README.md` | Eski `davetkart-claude` deposunun tek satırlık README'si. UTF-16 kodlu; **bant eklenmedi** (kodlamayı bozmamak için) | [`../README.md`](../README.md) |
| [`scaffold-structure.ps1`](scaffold-structure.ps1) | `scaffold-structure.ps1` | Faz 0 backend klasör iskeleti betiği; işi bitti, hedef yol `davetkart-backend\` artık yok. Bant yorum satırı olarak eklendi | — |
| `local-snapshots/` (git dışı) | `Claude outputs/_snap/`, `Claude outputs/_to_delete/` | Oturumların aldığı kod arşivleri (`.tgz`, `.tar`, `.bundle`). 🔴 Üçünde `.env` var: `.gitignore` ile depo dışında, yalnızca diskte | — |

## Bu depoda olmayan arşiv kayıtları

- `BACKEND-KARAR-RAPORU.md` (NestJS önerisi): `context/PHP-LARAVEL-SETUP.md` §8'e göre **silinmiş**;
  bu depoda kopyası yok.
- Eski `davetkart-claude` deposunun git geçmişi (5 commit, son 2026-09-04): `davetkart-claude` uzak
  deposunda ve yerelde `D:\Projects\davetkart\_backup\davetkart-claude.git`. Commit listesi:
  [`../_restructure/claude-git-log.txt`](../_restructure/claude-git-log.txt).
