#!/usr/bin/env bash
# AUD-2026-11-12 — git geçmişinde sır taraması (üç gerçek depo, yalnızca `git log -p --all` okuması).
# DEĞER YAZDIRMAZ: eşleşen değerin ilk 4 karakteri + uzunluğu çıkar. Çıktı: commit · dosya · anahtar/kalıp · maske.
set -uo pipefail
for repo in davetkart-backend-php-laravel davetkart-frontent davetkart-docs; do
  echo "## $repo ($(git -C "/d/Projects/davetkart/$repo" rev-list --all --count) commit, bütün dallar)"
  git -C "/d/Projects/davetkart/$repo" log -p --all --no-color --no-ext-diff 2>/dev/null | awk '
    function mask(v,   n) { n = length(v); return substr(v, 1, 4) "…(" n " kr)" }
    /^commit [0-9a-f]{40}/ { c = substr($2, 1, 7); next }
    /^\+\+\+ b\// { f = substr($0, 7); next }
    /^\+/ {
      line = substr($0, 2)
      if (match(line, /AIza[0-9A-Za-z_-]{30,}/))                    print c " | " f " | Google API anahtarı kalıbı | " mask(substr(line, RSTART, RLENGTH))
      if (match(line, /AKIA[0-9A-Z]{16}/))                          print c " | " f " | AWS erişim anahtarı kalıbı | " mask(substr(line, RSTART, RLENGTH))
      if (match(line, /sk-[A-Za-z0-9]{20,}/))                       print c " | " f " | sk- anahtar kalıbı | " mask(substr(line, RSTART, RLENGTH))
      if (match(line, /ghp_[A-Za-z0-9]{36}/))                       print c " | " f " | GitHub token kalıbı | " mask(substr(line, RSTART, RLENGTH))
      if (line ~ /-----BEGIN [A-Z ]*PRIVATE KEY-----/)              print c " | " f " | özel anahtar bloğu | (içerik yazılmadı)"
      if (match(line, /https:\/\/[0-9a-f]{32}@[a-z0-9.]*sentry\.io/)) print c " | " f " | Sentry DSN kalıbı | " mask(substr(line, RSTART + 8, 32))
      if (match(line, /(APP_KEY|[A-Z_]*API_KEY|[A-Z_]*SECRET[A-Z_]*|[A-Z_]*PASSWORD|[A-Z_]*OSB_KEY|[A-Z_]*TOKEN|[A-Z_]*DSN)[ \t]*=[ \t]*["\x27]?[^ \t"\x27#]{8,}/)) {
        kv = substr(line, RSTART, RLENGTH); k = kv; sub(/[ \t]*=.*/, "", k); v = kv; sub(/^[^=]*=[ \t]*["\x27]?/, "", v)
        if (v !~ /^(null|true|false|your|xxx|changeme|example|\$\{|<|env\(|config\()/) print c " | " f " | " k " ataması | " mask(v)
      }
    }' | sort -u
  echo
done
