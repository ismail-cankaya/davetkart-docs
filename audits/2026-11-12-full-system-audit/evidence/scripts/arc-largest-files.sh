#!/usr/bin/env bash
# AUD-2026-11-12 · Dilim A · en buyuk 15 dosya (satir sayisi) + yorum orani.
# Salt okunur: yalnizca wc / grep / awk. Anlik goruntu: _audit-snap/backend (d810410).
# Kullanim: bash arc-largest-files.sh > ../commands/ARC-largest-files.txt
set -euo pipefail
SNAP="/d/Projects/davetkart/_audit-snap/backend"
cd "$SNAP"

echo "# komut: bash evidence/scripts/arc-largest-files.sh"
echo "# kopya: $SNAP (backend d810410) · tarih: $(date -u +%Y-%m-%dT%H:%MZ)"
echo

# Yorum satiri = bosluklardan sonra //, #, /*, * ya da */ ile baslayan satir (attribute #[ haric).
stats() {
  awk '
    { total++ }
    /^[[:space:]]*$/ { blank++; next }
    /^[[:space:]]*(\/\/|\/\*|\*\/|\*)/ { comment++; next }
    /^[[:space:]]*#[^\[]/ { comment++; next }
    { code++ }
    END { printf "%d %d %d %d", total, code+0, comment+0, blank+0 }
  ' "$1"
}

echo "## 1. Uretim kodu: en buyuk 15 PHP dosyasi (app/ routes/ config/ bootstrap/ database/)"
echo "satir | kod | yorum | bos | yorum% | dosya"
find app routes config bootstrap database -name '*.php' -not -path 'bootstrap/cache/*' -print0 \
  | while IFS= read -r -d '' f; do
      read -r t c m b <<<"$(stats "$f")"
      pct=$(( t > 0 ? (m * 100) / t : 0 ))
      echo "$t | $c | $m | $b | ${pct}% | $f"
    done | sort -t'|' -k1,1 -rn | head -15
echo

echo "## 2. Uretim kodu: KOD satirina gore en buyuk 15 (yorum ve bos satir haric)"
echo "kod | satir | yorum% | dosya"
find app routes config bootstrap database -name '*.php' -not -path 'bootstrap/cache/*' -print0 \
  | while IFS= read -r -d '' f; do
      read -r t c m b <<<"$(stats "$f")"
      pct=$(( t > 0 ? (m * 100) / t : 0 ))
      echo "$c | $t | ${pct}% | $f"
    done | sort -t'|' -k1,1 -rn | head -15
echo

echo "## 3. Testler: en buyuk 15 dosya"
echo "satir | dosya"
find tests -name '*.php' -print0 | xargs -0 wc -l | grep -v ' total$' | sort -rn | head -15 | awk '{print $1" | "$2}'
echo

echo "## 4. Toplamlar (klasor bazinda: dosya · satir · kod · yorum · yorum%)"
for d in app routes config bootstrap database/migrations database/factories database/seeders tests; do
  [ -d "$d" ] || continue
  n=0; T=0; C=0; M=0
  while IFS= read -r -d '' f; do
    read -r t c m b <<<"$(stats "$f")"
    n=$((n+1)); T=$((T+t)); C=$((C+c)); M=$((M+m))
  done < <(find "$d" -name '*.php' -not -path 'bootstrap/cache/*' -print0)
  pct=$(( T > 0 ? (M * 100) / T : 0 ))
  echo "$d | dosya=$n | satir=$T | kod=$C | yorum=$M | yorum%=${pct}%"
done
echo

echo "## 5. app/ alt klasorleri (dosya · satir · kod · yorum%)"
for d in $(find app -mindepth 1 -maxdepth 1 -type d | sort); do
  n=0; T=0; C=0; M=0
  while IFS= read -r -d '' f; do
    read -r t c m b <<<"$(stats "$f")"
    n=$((n+1)); T=$((T+t)); C=$((C+c)); M=$((M+m))
  done < <(find "$d" -name '*.php' -print0)
  pct=$(( T > 0 ? (M * 100) / T : 0 ))
  echo "$d | dosya=$n | satir=$T | kod=$C | yorum%=${pct}%"
done
