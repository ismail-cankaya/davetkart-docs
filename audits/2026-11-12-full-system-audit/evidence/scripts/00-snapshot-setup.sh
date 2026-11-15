#!/usr/bin/env bash
# AUD-2026-11-12 — anlık görüntü kurulumu.
# Kod depolarına YAZMAZ: yalnızca `git archive` / `git show` / `git ls-tree` (salt okunur) kullanır.
# Çıktı: D:\Projects\davetkart\_audit-snap\{backend,frontend}  (depo dışı, kısa yol: LongPathsEnabled=0)
set -euo pipefail
ROOT=/d/Projects/davetkart
SNAP=$ROOT/_audit-snap
B=$ROOT/davetkart-backend-php-laravel
F=$ROOT/davetkart-frontent
REF=origin/ccr-9a346997-bu6gve
mkdir -p "$SNAP/backend" "$SNAP/frontend"
BH=$(git -C "$B" rev-parse "$REF"); FH=$(git -C "$F" rev-parse "$REF")
echo "backend  $REF = $BH"
echo "frontend $REF = $FH"
git -C "$B" archive "$BH" | tar -x -C "$SNAP/backend"
# .gitattributes'teki export-ignore yüzünden arşive girmeyen dosyalar (/.github vb.)
git -C "$B" ls-tree -r --name-only "$BH" | while IFS= read -r f; do
  if [ ! -e "$SNAP/backend/$f" ]; then mkdir -p "$SNAP/backend/$(dirname "$f")"; git -C "$B" show "$BH:$f" > "$SNAP/backend/$f"; echo "export-ignore tamamlandı: $f"; fi
done
git -C "$F" archive "$FH" | tar -x -C "$SNAP/frontend"
git -C "$F" ls-tree -r --name-only "$FH" | while IFS= read -r f; do
  if [ ! -e "$SNAP/frontend/$f" ]; then mkdir -p "$SNAP/frontend/$(dirname "$f")"; git -C "$F" show "$FH:$f" > "$SNAP/frontend/$f"; echo "eksik tamamlandı: $f"; fi
done
echo "$BH" > "$SNAP/backend.commit"; echo "$FH" > "$SNAP/frontend.commit"
echo "backend dosya: $(find "$SNAP/backend" -type f | wc -l) (ağaçta $(git -C "$B" ls-tree -r --name-only "$BH" | wc -l))"
echo "frontend dosya: $(find "$SNAP/frontend" -type f | wc -l) (ağaçta $(git -C "$F" ls-tree -r --name-only "$FH" | wc -l))"
