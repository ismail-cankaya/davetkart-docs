# Taşıma Planı — davetkart-docs (2026-11-12)

> Kural tablosu betikten gelir (`_restructure/restructure.py`, `RULES`). Dosya dosya tam liste:
> `INVENTORY.md` §2. Taşımalar sınıf sırasıyla yapılır; her sınıf ayrı commit.

## 1. Eski yol → yeni yol

| # | Eski yol | Yeni yol | Sınıf | Durum | Gerekçe |
|---|---|---|---|---|---|
| 1 | `claude/PHP-LARAVEL-SETUP.md` | `context/PHP-LARAVEL-SETUP.md` | context | güncel (EK-11/12 işlenmeyi bekliyor) | Ana bağlam ve karar kaydı; adı korunur |
| 2 | `claude/PHP-LARAVEL-SETUP-EK-FAZ-11.md`, `-12.md` | `decisions/addenda/` (aynı ad) | decisions | güncel (ana dosyaya işlenmedi) | Karar kaydı ekleri |
| 3 | `PROMPT-FAZ-11.md` | `prompts/PROMPT-FAZ-11.md` | prompts | tamamlandı | Faz 11 ajan prompt'u |
| 4 | `PROMPT-FAZ-12.md` | `prompts/PROMPT-FAZ-12.md` | prompts | tamamlandı | Faz 12 ajan prompt'u |
| 5 | `PROMPT-YAYIN.md` | `prompts/PROMPT-YAYIN.md` | prompts | güncel | Yayın oturumu başlangıç prompt'u |
| 6 | `YAYIN-PLANI.md` | `operations/deployment/YAYIN-PLANI.md` | operations | güncel | AWS Lightsail yayın planı (26 Eki) |
| 7 | `YAYIN-DEVIR.md` | `operations/deployment/YAYIN-DEVIR.md` | operations | güncel | Yayın devir notu (15 Eki) |
| 8 | `Claude outputs/FAZ-11-*.md` | `phases/faz-11/` | phases | tamamlandı | Faz 11 commit komutları |
| 9 | `Claude outputs/FAZ-12-RAPOR.md` | `phases/faz-12/` | phases | tamamlandı | Faz 12 raporu |
| 10 | `Claude outputs/FAZ-13-*.md`, `f13-ara/`, `teshis.php`, `php-herdsiz.ini` | `phases/faz-13/` | phases | tamamlandı | Faz 13 commit komutları, ara kod çıktısı, PHPStan teşhisi |
| 11 | `Claude outputs/FAZ-14-*.md`, `f14/` | `phases/faz-14/` | phases | tamamlandı | Faz 14 commit komutları ve kod çıktısı |
| 12 | `Claude outputs/FRONTEND-YAKALAMA-PLANI.md` | `phases/frontend-catch-up/` | phases | tamamlandı | F1–F7 planı (SETUP: ✅ 13–16 Eylül) |
| 13 | `claude/hero-video-onay/` | `product/hero-video-onay/` | product | tamamlandı | Hero video onay çalışması |
| 14 | `claude/video-onay/` | `product/video-onay/` | product | tamamlandı | Kategori videoları onay çalışması |
| 15 | `claude/Notlar/*` | `notes/` | notes | tarihsel not | Frontend analizi ve yapılacaklar |
| 16 | `claude/PROMPT.md` | `archive/PROMPT.md` | archive | geçersiz kılındı | 4 Eylül başlangıç prompt'u; "Faz 7'yi kapat" diyor |
| 17 | `claude/PROMPT-ARSIV-FAZ-4.md` | `archive/PROMPT-ARSIV-FAZ-4.md` | archive | geçersiz kılındı | PROMPT.md'nin eski sürümü |
| 18 | `claude/README.md` | `archive/davetkart-claude/README.md` | archive | geçersiz kılındı | Eski deponun tek satırlık README'si |
| 19 | `scaffold-structure.ps1` | `archive/scaffold-structure.ps1` | archive | geçersiz kılındı | Faz 0 backend iskelet betiği; silinmiş `davetkart-backend\` yolunu hedefliyor |
| 20 | `Claude outputs/_snap/`, `_to_delete/` | `archive/local-snapshots/` | archive (git dışı) | yerel | `.env` içeren kod arşivleri; `.gitignore`'da |

## 2. Önerilen yapıdan sapmalar

1. **`phases/faz-07`, `faz-09`, `faz-10` açılmadı.** O fazların belgeleri (devirler, Faz 10 planı)
   backend deposunun `claude/` klasöründe; bu depoda içerikleri yok. Boş klasör açılmadı.
2. **`audits/` boş başlıyor** (yalnızca `README.md`). `2026-09-23-code-review` ve `2026-09-24-test-audit`
   raporları backend `claude/` klasöründe (`GOZDEN-GECIRME-RAPORU.md`, `TEST-DENETIMI-2026-09-24.md`).
   Kapsam dışı olduğu için taşınmadı; `audits/README.md` onları listeler.
3. **`context/working-agreement.md`, `glossary.md` yok:** mevcut bir dosya yok, yeni metin yazılmadı.
4. **`phases/frontend-catch-up/` eklendi:** numaralı bir faz değil (Faz 9 ile 10 arası F1–F7).
5. **Kod çıktıları (`f13-ara/`, `f14/`) arşive değil `phases/`'a gitti:** o fazın commit komutları bu
   klasörlere atıf veriyor; birlikte dururlar.
6. **`_triage/` boş:** her dosyanın yeri içeriğinden ve tarihinden belirlenebildi.
7. **Düz metin yollar değiştirilmedi** (bkz. `INVENTORY.md` §6): tarihsel anlatımın parçası.
   Eski → yeni karşılığı kök `README.md`'de.
8. **Başlangıç altyapısı:** `.gitignore` (kod arşivleri) ve `.gitattributes` (`eol=lf`) başlangıç
   commit'ine eklendi; prompt'un listesinde yoktu ama sırları depo dışında tutmak için gerekliydi.

## 3. Sıra

`context` → `decisions` → `phases` → `prompts` → `operations` → `product` → `notes` → `archive`
(+ `archive-local`, git dışı). `audits` ve `_triage` taşınacak dosya içermiyor.
