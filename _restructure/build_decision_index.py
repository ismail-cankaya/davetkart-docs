"""decisions/DECISION-INDEX.md denetler (--check) ya da ilk sürümünü üretir (--generate).

Kullanım (docs deposunun kökünden):
  python -I _restructure/build_decision_index.py --check
      0 = indeks ve tanımlar aynı · 1 = fark var (numaralar yazılır) · 2 = kardeş backend deposu yok.
  python -I _restructure/build_decision_index.py --generate
      2026-11-12 üretimi: yalnızca K1–K127 kaynaklarını bilir ve DOSYAYI EZER. K128+ satırları elle
      eklendiği için bugün kullanılmaz; tarihçe için duruyor.

TANIM / ATIF KURALI (--check):
  Tanım = markdown tablo satırının İLK hücresi yalnızca K numarasıdır: `| K128 |`, `| **K128** |`,
  `| **K9'** |` ya da §8'deki üstü çizili biçim `| ~~K9: …~~ |`. Başka her geçiş (cümle içinde,
  başlıkta, ikinci ve sonraki hücrelerde, `K2xx` gibi yer tutucular) atıftır ve sayılmaz.
  Taranan: docs deposu + ../davetkart-backend-php-laravel içindeki bütün *.md dosyaları.
  Hariç: indeksin kendisi, SKIP_DIRS ve docs'ta SKIP_DOCS (bekleyen hat kayıtları 19.90'da işlenir;
  denetim raporları ve prompt'lar karar tanımlamaz, alıntılar).
"""
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BE = ROOT.parent / "davetkart-backend-php-laravel"

MAIN = "context/PHP-LARAVEL-SETUP.md"
SOURCES = [  # (dosya, gösterilen kaynak, bağlantı mı)
    (ROOT / MAIN, f"[`{MAIN}` §7](../{MAIN}#7-karar-kaydı)"),
    (BE / "claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md", "backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md` §A"),
    (BE / "claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md", "backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` §A"),
    (BE / "claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md", "backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md` §A"),
    (BE / "claude/PHP-LARAVEL-SETUP-EK-FAZ-9.md", "backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-9.md` §A"),
    (BE / "claude/FAZ-10-PLANI.md", "backend `claude/FAZ-10-PLANI.md` §2"),
    (ROOT / "decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md",
     "[`addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md#a-karar-kaydına-eklenecek-7)"),
    (ROOT / "decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md",
     "[`addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md` §A](addenda/PHP-LARAVEL-SETUP-EK-FAZ-12.md#a-karar-kaydına-eklenecek-7)"),
]

PHASES = [(1, 24, "Faz 0"), (25, 34, "Faz 1"), (35, 36, "Faz 2"), (37, 44, "Faz 3"), (45, 48, "Faz 4"),
          (49, 53, "Faz 5"), (54, 63, "Faz 6"), (64, 71, "Faz 7"), (72, 79, "Faz 8"), (80, 86, "Faz 9"),
          (87, 93, "Faz 10 (25 Eyl)"), (95, 106, "Faz 10 (25 Eyl–1 Eki)"), (94, 94, "Faz 12 (24 Eki)"),
          (107, 116, "Faz 11 (23 Eki)"), (117, 127, "Faz 12 (24 Eki)")]

# Durum notları: kaynak dosyalardaki ifadelerden; yeni yorum yok.
STATUS = {
    "K1": "geçerli · PHP sürümü K87 ile `^8.5`",
    "K9": "geçersiz kılındı → K9'",
    "K11": "geçerli · ana dosyada durum hâlâ \"📋 Faz 2'de uygulanacak\"",
    "K14": "geçerli · K77 ile `hash_hmac`'e birleşti",
    "K21": "geçerli · K96 istisnası (mailler Türkçe)",
    "K43": "⚠️ Faz 7'de uygulanmadı (açık ticari karar; bkz. K99)",
    "K53": "geçersiz kılındı → K62",
    "K55": "geçerli · ⚠️ yayın planı S3 diski kuruyor (`operations/deployment/YAYIN-DEVIR.md` Y0); yerine geçen K yok",
    "K62": "geçersiz kılındı → K79",
    "K63": "geçersiz kılındı → K71",
    "K67": "geçerli · ⚠️ frontend 11.6 ile çelişki sorusu açık (EK-FAZ-12 §F-7)",
    "K69": "geçerli · K122 tarayıcı callback'i için bilinçli sapma",
    "K94": "⚠️ geçici: elle doğrulamadan sonra güncellenecek",
    "K125": "⚠️ elle doğrulama bekliyor",
}

SPLIT = re.compile(r"(?<!\\)\|")


def phase(n):
    for a, b, name in PHASES:
        if a <= n <= b:
            return name
    return "?"


def clean(cell, limit=110):
    s = cell.replace("**", "").strip()
    s = re.sub(r"\s+", " ", s)
    if len(s) <= limit:
        return s
    s = s[: limit - 1].rstrip()
    return s + ("`…" if s.count("`") % 2 else "…")


def main():
    seen = {}
    for path, label in SOURCES:
        if not path.exists():
            raise SystemExit(f"kaynak yok: {path}")
        in_rules = False
        for line in path.read_text("utf-8").splitlines():
            if line.startswith("## "):
                in_rules = "Kural" in line  # EK dosyalarında §B kuralları K80'i tekrar ediyor
            m = re.match(r"^\| \*\*(K\d+'?)\*\* \|", line)
            if not m or in_rules:
                continue
            k = m.group(1)
            if k in seen:
                continue
            cells = SPLIT.split(line)
            seen[k] = (clean(cells[2]), label)
    # K9 asıl kararı (MySQL) yalnızca §8'de üstü çizili; satırı elle ekle
    seen.setdefault("K9", ("Üretimde MySQL 8", f"[`{MAIN}` §8](../{MAIN}#8-geçersiz-kılınan-kararlar-️)"))

    def key(k):
        return (int(re.sub(r"\D", "", k)), k.endswith("'"))

    out = ["# Karar İndeksi (K numaraları)", "",
           "> **Tek tablo.** Kararın kendisi ve gerekçesi kaynak dosyada; burada tek satırlık başlık.",
           "> Üretim: `python -I _restructure/build_decision_index.py` (2026-11-12). Yeni karar eklerken",
           "> bu dosyaya da elle satır eklenir (bkz. `../CLAUDE.md` §5).",
           "> ⚠️ işaretli satırlar açık soru ya da çelişki taşır; **numaralar değiştirilmedi.**", "",
           "**Sıradaki boş numara: K128**", "",
           "| K# | Başlık | Faz | Durum | Kaynak |", "|---|---|---|---|---|"]
    nums = sorted(seen, key=key)
    for k in nums:
        title, src = seen[k]
        n = int(re.sub(r"\D", "", k))
        out.append(f"| **{k}** | {title} | {phase(n)} | {STATUS.get(k, 'geçerli')} | {src} |")
    present = {int(re.sub(r"\D", "", k)) for k in nums}
    missing = [n for n in range(1, max(present) + 1) if n not in present]
    out += ["", "## Notlar", "",
            f"- Eksik numara: {', '.join(f'K{n}' for n in missing) if missing else 'yok'} (K1–K{max(present)}).",
            "- Çakışma: backend `docs/07` §8'deki ikinci **K18** (Pest/PHPUnit) orada **K24** olarak düzeltilmiş"
            " (`docs/07:958`). Bu depoda çakışma yok.",
            "- K94, Faz 10 planında Shopier için ayrıldı, Faz 12'de tanımlandı; bu yüzden sıra dışı görünür.",
            "- Ana dosyaya (`context/PHP-LARAVEL-SETUP.md` §7) işlenmiş olanlar yalnızca K1–K48 ve K64–K71."
            " Geri kalanı kaynak sütunundaki ek dosyalarda bekliyor.",
            "- Backend kaynakları (`davetkart-backend-php-laravel/claude/…`) bu depoda değil; yol düz metindir."]
    (ROOT / "decisions" / "DECISION-INDEX.md").write_text("\n".join(out) + "\n", "utf-8")
    print(f"{len(nums)} satır; eksik: {missing}")


INDEX = ROOT / "decisions" / "DECISION-INDEX.md"
SKIP_DIRS = {".git", "vendor", "node_modules", "storage", "dist", "bootstrap", "public"}
SKIP_DOCS = ("phases/faz-19/kayit/", "audits/", "prompts/", "_restructure/")
DEF = re.compile(r"^\|\s*(?:(?:\*\*|~~)*(K\d+'?)(?:\*\*|~~)*|~~(K\d+'?):[^|]*~~)\s*\|")


def definitions(base, skip=()):
    """{K: [göreli yol:satır, ...]} — yalnızca tanım satırları (bkz. kural)."""
    found = {}
    for d, dirs, files in os.walk(base):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            path = Path(d) / f
            rel = path.relative_to(base).as_posix()
            if not f.endswith(".md") or path == INDEX or rel.startswith(skip):
                continue
            for i, line in enumerate(path.read_text("utf-8", errors="replace").splitlines(), 1):
                m = DEF.match(line)
                if m:
                    found.setdefault(m.group(1) or m.group(2), []).append(f"{rel}:{i}")
    return found


def check():
    if not BE.is_dir():
        print(f"UYARI: kardeş backend deposu yok: {BE} — denetim yapılmadı.")
        return 2
    defined = definitions(ROOT, SKIP_DOCS)
    for k, where in definitions(BE).items():
        defined.setdefault(k, []).extend(f"backend {w}" for w in where)
    indexed = set()
    for line in INDEX.read_text("utf-8").splitlines():
        m = DEF.match(line)
        if m:
            indexed.add(m.group(1) or m.group(2))
    num = lambda k: (int(re.sub(r"\D", "", k)), k.endswith("'"))  # noqa: E731
    missing = sorted(set(defined) - indexed, key=num)
    orphan = sorted(indexed - set(defined), key=num)
    for k in missing:
        print(f"indekste yok: {k} ({', '.join(defined[k][:3])})")
    for k in orphan:
        print(f"tanımı yok: {k} (indekste var, docs ve backend'de tanım satırı yok)")
    print(f"indeks {len(indexed)} · tanım {len(defined)} · eksik {len(missing)} · tanımsız {len(orphan)}")
    return 1 if missing or orphan else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--check"]:
        sys.exit(check())
    if sys.argv[1:] == ["--generate"]:
        main()
        sys.exit(0)
    print(__doc__)
    sys.exit(2)
