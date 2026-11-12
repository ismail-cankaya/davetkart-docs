"""davetkart-docs düzenleme aracı (2026-11-12).

Kullanım (depo kökünden):
  python -I _restructure/restructure.py inventory   # INVENTORY.md + MIGRATION-PLAN.md üretir
  python -I _restructure/restructure.py move <sınıf> # o sınıfın dosyalarını taşır
  python -I _restructure/restructure.py links        # kırık Markdown bağlantılarını listeler

Kural: hiçbir dosya silinmez, içerik değiştirilmez; yalnızca taşınır.
"""
import os
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git"}
OWN = {"_restructure"}

# (eski önek, yeni önek, sınıf, durum, gerekçe) — ilk eşleşen kazanır.
RULES = [
    ("claude/PHP-LARAVEL-SETUP.md", "context/PHP-LARAVEL-SETUP.md", "context",
     "güncel (EK-11/12 işlenmeyi bekliyor)", "Ana bağlam ve karar kaydı; adı korunur"),
    ("claude/PHP-LARAVEL-SETUP-EK-FAZ-", "decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-", "decisions",
     "güncel (ana dosyaya işlenmedi)", "Karar kaydı eki"),
    ("PROMPT-FAZ-11.md", "prompts/PROMPT-FAZ-11.md", "prompts", "tamamlandı (tarihsel)", "Faz 11 ajan prompt'u"),
    ("PROMPT-FAZ-12.md", "prompts/PROMPT-FAZ-12.md", "prompts", "tamamlandı (tarihsel)", "Faz 12 ajan prompt'u"),
    ("PROMPT-YAYIN.md", "prompts/PROMPT-YAYIN.md", "prompts", "güncel", "Yayın oturumu başlangıç prompt'u"),
    ("YAYIN-PLANI.md", "operations/deployment/YAYIN-PLANI.md", "operations", "güncel", "AWS Lightsail yayın planı"),
    ("YAYIN-DEVIR.md", "operations/deployment/YAYIN-DEVIR.md", "operations", "güncel",
     "Yayın devir notu (15 Eki; plan 26 Eki'de güncellendi)"),
    ("Claude outputs/FAZ-11-", "phases/faz-11/FAZ-11-", "phases", "tamamlandı (tarihsel)", "Faz 11 commit komutları"),
    ("Claude outputs/FAZ-12-", "phases/faz-12/FAZ-12-", "phases", "tamamlandı (tarihsel)", "Faz 12 raporu"),
    ("Claude outputs/FAZ-13-", "phases/faz-13/FAZ-13-", "phases", "tamamlandı (tarihsel)", "Faz 13 commit komutları"),
    ("Claude outputs/f13-ara/", "phases/faz-13/f13-ara/", "phases", "tamamlandı (tarihsel)",
     "Faz 13 ara kod çıktısı (komut dosyaları bu klasöre atıf veriyor)"),
    ("Claude outputs/teshis.php", "phases/faz-13/teshis.php", "phases", "tamamlandı (tarihsel)",
     "Faz 13 PHPStan teşhis betiği (dosyanın ilk satırı)"),
    ("Claude outputs/php-herdsiz.ini", "phases/faz-13/php-herdsiz.ini", "phases", "tamamlandı (tarihsel)",
     "teshis.php ile aynı gün üretilmiş php.ini (Faz 13 teşhisi)"),
    ("Claude outputs/FAZ-14-", "phases/faz-14/FAZ-14-", "phases", "tamamlandı (tarihsel)", "Faz 14 commit komutları"),
    ("Claude outputs/f14/", "phases/faz-14/f14/", "phases", "tamamlandı (tarihsel)",
     "Faz 14 kod çıktısı; kod depolarına aktarıldı (ör. 14.3 backend'de 2026-10-25 commit'li)"),
    ("Claude outputs/FRONTEND-YAKALAMA-PLANI.md", "phases/frontend-catch-up/FRONTEND-YAKALAMA-PLANI.md", "phases",
     "tamamlandı (tarihsel)", "F1–F7 planı; SETUP: F1–F7 ✅ 13–16 Eylül"),
    ("claude/hero-video-onay/", "product/hero-video-onay/", "product", "tamamlandı (tarihsel)",
     "Hero video onay çalışması (tasarım)"),
    ("claude/video-onay/", "product/video-onay/", "product", "tamamlandı (tarihsel)",
     "Kategori videoları onay çalışması (tasarım)"),
    ("claude/Notlar/", "notes/", "notes", "tarihsel not", "Serbest notlar / analizler"),
    ("claude/PROMPT-ARSIV-FAZ-4.md", "archive/PROMPT-ARSIV-FAZ-4.md", "archive",
     "geçersiz kılındı → claude/PROMPT.md (o da arşivde)", "Faz 4'e kadarki başlangıç prompt'u"),
    ("claude/PROMPT.md", "archive/PROMPT.md", "archive",
     "geçersiz kılındı → context/PHP-LARAVEL-SETUP.md + prompts/", "4 Eylül başlangıç prompt'u; 'Faz 7'yi kapat' diyor"),
    ("claude/README.md", "archive/davetkart-claude/README.md", "archive",
     "geçersiz kılındı → README.md", "Eski davetkart-claude deposunun tek satırlık README'si (UTF-16)"),
    ("scaffold-structure.ps1", "archive/scaffold-structure.ps1", "archive",
     "geçersiz kılındı (Faz 0'da çalıştı)", "Backend klasör iskeleti betiği; silinmiş davetkart-backend\\ yolunu hedefliyor"),
    ("Claude outputs/_snap/", "archive/local-snapshots/_snap/", "archive-local", "yerel, git dışı",
     "Kod anlık görüntüleri; 3'ünde .env var → .gitignore"),
    ("Claude outputs/_to_delete/", "archive/local-snapshots/_to_delete/", "archive-local", "yerel, git dışı",
     "Önceki oturumun 'silinecek' dediği arşivler; silinmez, git dışı"),
]

CLASS_ORDER = ["context", "decisions", "phases", "prompts", "audits", "operations", "product", "notes",
               "archive", "archive-local", "_triage"]


def all_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = Path(dirpath).relative_to(ROOT)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not (rel_dir == Path(".") and d in OWN)]
        for f in filenames:
            yield (rel_dir / f).as_posix().lstrip("./") if str(rel_dir) != "." else f


def rule_for(path):
    for old, new, cls, status, why in RULES:
        if path == old or (old.endswith(("/", "-")) and path.startswith(old)):
            return new + path[len(old):], cls, status, why
    return None


def first_heading(p):
    if p.suffix.lower() not in {".md", ".ps1", ".php", ".py", ".html", ".ts", ".tsx", ".json", ".ini"}:
        return ""
    try:
        raw = p.read_bytes()[:4000]
        text = raw.decode("utf-16") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("utf-8", "replace")
    except Exception:
        return ""
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#") and len(s) > 2 and not s.startswith("#!"):
            return s.lstrip("# ").replace("|", "\\|")[:80]
    return ""


AYLAR = "Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık"
DATE_RE = re.compile(r"20\d\d-\d\d-\d\d|\d{1,2} (?:%s) 20\d\d" % AYLAR)


def in_file_date(p):
    if p.suffix.lower() != ".md":
        return ""
    m = DATE_RE.search(p.read_text("utf-8", "replace")[:3000])
    return m.group(0) if m else ""


def old_git_dates():
    d = {}
    f = ROOT / "_restructure" / "claude-git-dates.tsv"
    if f.exists():
        for line in f.read_text("utf-8").splitlines():
            k, v = line.split("\t")
            d[k] = v
    return d


def inventory():
    dates = old_git_dates()
    rows, unmapped = [], []
    for path in sorted(all_files()):
        if path in {".gitignore", ".gitattributes"}:
            continue
        r = rule_for(path)
        if not r:
            unmapped.append(path)
            continue
        p = ROOT / path
        rows.append((path, p.stat().st_size, first_heading(p), in_file_date(p),
                     dates.get(path, "— (eski depoda commit'lenmemişti)" if path.startswith("claude/") else "— (git'e hiç girmemişti)"), *r))
    return rows, unmapped


def write_docs():
    rows, unmapped = inventory()
    counts = {}
    for row in rows:
        counts[row[6]] = counts.get(row[6], 0) + 1
    inv = ["# Envanter — davetkart-docs (2026-11-12)", "",
           "> Betikle üretildi: `python -I _restructure/restructure.py inventory`. Tarih sütunları:",
           "> **dosyada** = dosyanın ilk 3000 karakterinde geçen ilk tarih; **eski git** = eski",
           "> `davetkart-claude` deposundaki son commit (`claude/` dışındakiler hiç commit'lenmemişti).",
           "> Dosyalar başlangıç commit'i `9e428a8` anındaki yollarıyla listelenir.", "",
           "## 1. Sınıflara dağılım", "", "| Sınıf | Dosya |", "|---|---|"]
    for c in CLASS_ORDER:
        if c in counts:
            inv.append(f"| `{c}` | {counts[c]} |")
    inv += [f"| **Toplam** | **{len(rows)}** |", ""]
    if unmapped:
        inv += ["## ⚠️ Kurala uymayan dosyalar", ""] + [f"- `{u}`" for u in unmapped] + [""]
    inv += ["## 2. Dosyalar", "",
            "| Yol | Boyut | İlk başlık | Dosyada tarih | Eski git | Sınıf | Durum |",
            "|---|---:|---|---|---|---|---|"]
    for path, size, head, fdate, gdate, new, cls, status, why in rows:
        inv.append(f"| `{path}` | {size:,} | {head} | {fdate} | {gdate} | {cls} | {status} |")
    extra = ROOT / "_restructure" / "inventory-findings.md"
    if extra.exists():
        inv += ["", extra.read_text("utf-8")]
    (ROOT / "_restructure" / "INVENTORY.md").write_text("\n".join(inv) + "\n", "utf-8")

    print(f"{len(rows)} dosya, {len(unmapped)} eşleşmeyen")


def move(cls):
    rows, _ = inventory()
    n = 0
    for path, *_rest in rows:
        new, c = _rest[4], _rest[5]
        if c != cls:
            continue
        src, dst = ROOT / path, ROOT / new
        if dst.exists():
            sys.exit(f"HEDEF VAR, durdu: {new}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        n += 1
    # boşalan klasörleri kaldır (dosya silinmez)
    for d in ["claude/Notlar", "claude/hero-video-onay", "claude/video-onay", "claude",
              "Claude outputs/_snap", "Claude outputs/_to_delete", "Claude outputs"]:
        p = ROOT / d
        if p.exists():
            for sub in sorted(p.rglob("*"), key=lambda x: len(x.parts), reverse=True):
                if sub.is_dir() and not any(sub.iterdir()):
                    sub.rmdir()
            if not any(p.iterdir()):
                p.rmdir()
    print(f"{cls}: {n} dosya taşındı")


LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def links():
    broken = []
    for path in all_files():
        if not path.endswith(".md") or path.startswith("phases/faz-14/f14/") or path.startswith("phases/faz-13/f13-ara/"):
            continue
        text = (ROOT / path).read_text("utf-8", "replace")
        for target in LINK_RE.findall(text):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            t = target.split("#")[0]
            if t and not (ROOT / path).parent.joinpath(t).exists():
                broken.append(f"{path} → {target}")
    print("\n".join(broken) if broken else "Kırık bağlantı yok.")
    return broken


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "inventory"
    if cmd == "inventory":
        write_docs()
    elif cmd == "move":
        move(sys.argv[2])
    elif cmd == "links":
        sys.exit(1 if links() else 0)
