#!/usr/bin/env bash
# AUD-2026-11-12 · Dilim A · K18: docs/rehber/<ayni-yol>.md kilavuzu olmayan kod dosyalari
# + kisa-yorum kurali (1-3 satir) ihlali: 3 satirdan uzun yorum bloklari.
# Salt okunur. Anlik goruntu: _audit-snap/backend (d810410).
# Kullanim: bash arc-k18-guide-gaps.sh > ../commands/ARC-k18-guide-gaps.txt
set -euo pipefail
SNAP="/d/Projects/davetkart/_audit-snap/backend"
cd "$SNAP"

echo "# komut: bash evidence/scripts/arc-k18-guide-gaps.sh"
echo "# kopya: $SNAP (backend d810410) · tarih: $(date -u +%Y-%m-%dT%H:%MZ)"
echo "# kural: <yol>/<Ad>.php -> docs/rehber/<yol>/<Ad>.md"
echo

total=0; missing=0
miss_list=$(mktemp)
for root in app routes config bootstrap database tests; do
  while IFS= read -r -d '' f; do
    total=$((total+1))
    guide="docs/rehber/${f%.php}.md"
    if [ ! -f "$guide" ]; then
      missing=$((missing+1))
      echo "$f" >> "$miss_list"
    fi
  done < <(find "$root" -name '*.php' -not -path 'bootstrap/cache/*' -print0)
done

echo "## 1. Ozet"
echo "taranan kod dosyasi: $total · kilavuzu OLMAYAN: $missing · kilavuzu olan: $((total-missing))"
echo

echo "## 2. Klasor bazinda eksik sayisi"
sed 's|/[^/]*$||' "$miss_list" | sort | uniq -c | sort -rn
echo

echo "## 3. Kilavuzu olmayan dosyalar (tam liste)"
sort "$miss_list"
echo

echo "## 4. Yetim kilavuzlar: docs/rehber altinda olup karsiligi kod dosyasi OLMAYAN .md (app/routes/config/bootstrap/database/tests altlari)"
for root in app routes config bootstrap database tests; do
  [ -d "docs/rehber/$root" ] || continue
  while IFS= read -r -d '' g; do
    rel="${g#docs/rehber/}"
    php="${rel%.md}.php"
    if [ ! -f "$php" ]; then echo "$g"; fi
  done < <(find "docs/rehber/$root" -name '*.md' -print0)
done | sort
echo

echo "## 5. K18 kisa yorum kurali: 3 satirdan uzun yorum bloklari (uretim kodu)"
echo "blok>3 | en uzun blok | yorum satiri | toplam satir | dosya"
find app routes config bootstrap database/migrations -name '*.php' -not -path 'bootstrap/cache/*' -print0 \
  | while IFS= read -r -d '' f; do
      awk -v F="$f" '
        function flush() { if (run > 3) long++; if (run > maxrun) maxrun = run; run = 0 }
        { total++ }
        /^[[:space:]]*(\/\/|\/\*|\*\/|\*)/ { run++; com++; next }
        /^[[:space:]]*#[^\[]/ { run++; com++; next }
        { flush() }
        END { flush(); printf "%d | %d | %d | %d | %s\n", long+0, maxrun+0, com+0, total, F }
      ' "$f"
    done | sort -t'|' -k1,1 -rn > "$miss_list.blocks"
head -25 "$miss_list.blocks"
echo
echo "uretim kodunda 3 satirdan uzun yorum blogu iceren dosya sayisi: $(awk -F'|' '$1+0 > 0' "$miss_list.blocks" | wc -l) / $(wc -l < "$miss_list.blocks")"
echo "toplam uzun blok: $(awk -F'|' '{s+=$1} END {print s}' "$miss_list.blocks")"
echo "en uzun tek yorum blogu (satir): $(awk -F'|' '{ if ($2+0 > m) m=$2+0 } END {print m}' "$miss_list.blocks")"
rm -f "$miss_list" "$miss_list.blocks"
