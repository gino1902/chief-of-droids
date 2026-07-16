#!/usr/bin/env bash
# check-diff-confined.sh [--no-deletions] <repo-dir> <base-ref> <allowed-glob>...
#
# Asserts that `git diff <base-ref>` inside <repo-dir> touches only paths
# matching an allowed glob. An empty diff passes. With --no-deletions it also
# fails if any path was deleted (for additive rows).
#
# This is the diff-confinement check for the committed-base rows:
#   MD-5  check-diff-confined.sh <test-medium> <base> CLAUDE.md
#   MD-2  check-diff-confined.sh <test-medium> <base> FRAMING.md
#   MD-3  check-diff-confined.sh --no-deletions <test-medium> <base> CONCEPTS.md 'report-builder/*'
#   MD-7  check-diff-confined.sh --no-deletions <test-medium> <base> CONCEPTS.md 'steward-assignment/*' 'report-ownership/*'
#
# Deterministic, disk-only, no skill run. Exit 0 = pass, 1 = confinement
# failure, 2 = usage/lookup error. Built from git plus sed.

set -u
no_del=0
if [ "${1:-}" = "--no-deletions" ]; then no_del=1; shift; fi
repo="${1:?usage: check-diff-confined.sh [--no-deletions] <repo-dir> <base-ref> <allowed-glob>...}"
base="${2:?missing base ref}"
shift 2

git -C "$repo" rev-parse --verify --quiet "$base" >/dev/null 2>&1 \
  || { echo "FAIL: base ref not found in $repo: $base"; exit 2; }

echo "diff-confined: $repo @ $base   allowed: ${*:-<none>}"
changed=$(git -C "$repo" diff --name-only "$base")

fail=0
if [ -z "$changed" ]; then
  echo "  ok    no changes (empty diff)"
else
  while IFS= read -r p; do
    [ -z "$p" ] && continue
    ok=0
    for a in "$@"; do
      case "$p" in $a) ok=1; break;; esac
    done
    if [ "$ok" -eq 1 ]; then printf '  ok    allowed    %s\n' "$p"
    else printf '  FAIL  forbidden  %s\n' "$p"; fail=1; fi
  done <<EOF
$changed
EOF
fi

if [ "$no_del" -eq 1 ]; then
  dels=$(git -C "$repo" diff --name-only --diff-filter=D "$base")
  if [ -n "$dels" ]; then
    echo "  FAIL  deletions present:"; printf '%s\n' "$dels" | sed 's/^/            /'
    fail=1
  else
    echo "  ok    no deletions"
  fi
fi

if [ "$fail" -eq 0 ]; then echo "PASS"; exit 0; else echo "FAILED"; exit 1; fi
