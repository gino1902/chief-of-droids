#!/usr/bin/env bash
# check-pinned-contract.sh <dir> <stack>     stack = app | data | infra
#
# BC-3: one-run invariants against the determinism pins, from disk. No second
# bootstrap, no cross-run comparison.
#   - the CONVENTIONS.md runner equals the canonical pinned value for the stack
#   - app: the husky hook is the pinned shape (runs the runner, wires the
#     drift-check, nothing else)
#   - data: the local drift-check hook block is present and wired
#   - data/infra: the pre-commit rev is a real-tag form or the TODO marker,
#     never a guessed or empty value
#
# Deterministic, disk-only. Exit 0 pass, 1 fail, 2 usage.

set -u
dir="${1:?usage: check-pinned-contract.sh <dir> <stack:app|data|infra>}"
stack="${2:?missing stack: app|data|infra}"
conv="$dir/CONVENTIONS.md"
[ -f "$conv" ] || { echo "FAIL: no CONVENTIONS.md at $dir"; exit 1; }

case "$stack" in
  app)   want="npx eslint ." ;;
  data)  want="uv run ruff check ." ;;
  infra) want="tflint" ;;
  *) echo "FAIL: unknown stack $stack (app|data|infra)"; exit 2 ;;
esac

runner=$(grep -E "^runner:" "$conv" | head -1 | sed 's/^runner:[[:space:]]*//')
echo "pinned-contract: $dir ($stack)   runner=[$runner]"
fail=0
chk() { if [ "$2" -eq 0 ]; then printf '  ok    %s\n' "$1"; else printf '  FAIL  %s\n' "$1"; fail=1; fi; }

[ "$runner" = "$want" ]; chk "runner == canonical ($want)" $?

if [ "$stack" = app ]; then
  h="$dir/.husky/pre-commit"
  if [ -f "$h" ]; then
    grep -qF "npx eslint ." "$h"; chk "husky runs npx eslint ." $?
    grep -qF "bash scripts/check-conventions-drift.sh ." "$h"; chk "husky wires the drift-check" $?
    extra=$(grep -vE '^#!|^npx eslint \.$|^bash scripts/check-conventions-drift\.sh \.$|^[[:space:]]*$' "$h" | wc -l | tr -d ' ')
    [ "$extra" -eq 0 ]; chk "husky has no stray command (pinned shape)" $?
  else
    echo "  FAIL  no .husky/pre-commit"; fail=1
  fi
fi

if [ "$stack" = data ]; then
  pc="$dir/.pre-commit-config.yaml"
  if [ -f "$pc" ]; then
    grep -qE "id:[[:space:]]*conventions-drift" "$pc"; chk "data local drift-check hook block present" $?
    grep -qF "bash scripts/check-conventions-drift.sh ." "$pc"; chk "drift-check entry wired" $?
    rev=$(grep -E "^[[:space:]]*rev:" "$pc" | head -1 | sed 's/.*rev:[[:space:]]*//')
    echo "  rev=[$rev]"
    { printf '%s' "$rev" | grep -qE "^v[0-9]" || printf '%s' "$rev" | grep -qi "TODO"; }; chk "rev is a real-tag form or TODO (not guessed/empty)" $?
  else
    echo "  FAIL  no .pre-commit-config.yaml"; fail=1
  fi
fi

if [ "$stack" = infra ]; then
  pc="$dir/.pre-commit-config.yaml"
  if [ -f "$pc" ]; then
    rev=$(grep -E "^[[:space:]]*rev:" "$pc" | head -1 | sed 's/.*rev:[[:space:]]*//')
    echo "  rev=[$rev]"
    { printf '%s' "$rev" | grep -qE "^v[0-9]" || printf '%s' "$rev" | grep -qi "TODO"; }; chk "rev is a real-tag form or TODO (not guessed/empty)" $?
  fi
fi

if [ "$fail" -eq 0 ]; then echo "PASS"; exit 0; else echo "FAILED"; exit 1; fi
