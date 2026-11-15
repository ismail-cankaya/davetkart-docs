#!/usr/bin/env bash
# AUD-2026-11-12 · Dilim A · en cok degisen 15 dosya (git gecmisi).
# Salt okunur: yalnizca `git log` / `git rev-parse` (gercek depoda; calisma agacina dokunmaz).
# Kullanim: bash arc-churn.sh > ../commands/ARC-churn.txt
set -euo pipefail
REPO="/d/Projects/davetkart/davetkart-backend-php-laravel"
REF="origin/ccr-9a346997-bu6gve"
cd "$REPO"

echo "# komut: bash evidence/scripts/arc-churn.sh"
echo "# depo: $REPO · ref: $REF = $(git rev-parse --short "$REF") · commit sayisi: $(git log "$REF" --oneline | wc -l)"
echo "# ilk commit: $(git log "$REF" --reverse --format='%ad %h' --date=short | head -1) · son commit: $(git log "$REF" -1 --format='%ad %h' --date=short)"
echo

echo "## 1. En cok degisen 15 dosya (tum yollar)"
git log "$REF" --format= --name-only | grep -v '^$' | sort | uniq -c | sort -rn | head -15
echo

echo "## 2. En cok degisen 15 URETIM KODU dosyasi (app/ routes/ config/ bootstrap/ database/)"
git log "$REF" --format= --name-only | grep -E '^(app|routes|config|bootstrap|database)/' | sort | uniq -c | sort -rn | head -15
echo

echo "## 3. En cok degisen 15 test dosyasi"
git log "$REF" --format= --name-only | grep -E '^tests/' | sort | uniq -c | sort -rn | head -15
echo

echo "## 4. En cok degisen 15 dokuman (docs/ claude/ *.md)"
git log "$REF" --format= --name-only | grep -E '(^docs/|^claude/|\.md$)' | sort | uniq -c | sort -rn | head -15
echo

echo "## 5. Son 60 gunde en cok degisen 15 uretim kodu dosyasi"
git log "$REF" --since='60 days ago' --format= --name-only | grep -E '^(app|routes|config|bootstrap|database)/' | sort | uniq -c | sort -rn | head -15
echo

echo "## 6. Dal hijyeni: yerel ve uzak dallar"
echo "yerel dal sayisi: $(git branch | wc -l) · uzak dal sayisi: $(git branch -r | grep -vc 'HEAD')"
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short) %(objectname:short)' refs/heads refs/remotes | head -60
echo

echo "## 7. worktree listesi"
git worktree list
echo

echo "## 8. Denetlenen ref ile main / release-v1.0 farki (commit sayisi)"
for b in origin/main main release-v1.0 release-2026-10-20; do
  if git rev-parse -q --verify "$b" >/dev/null; then
    echo "$b..$REF ileride: $(git rev-list --count "$b..$REF") · geride: $(git rev-list --count "$REF..$b")"
  fi
done
