#!/usr/bin/env bash
# check-conventions-contract.sh <dir> [<trees.md>]
#
# BC-1: asserts the generated CONVENTIONS.md is a faithful contract, from disk:
#   - it exists at the repo root
#   - it carries no leaked authoring caveat (an "Unverified" / "⚠️" line)
#   - it has the enforcement stanza (config / runner / zoned)
#   - every rule bullet's opening line is present verbatim in the skill's
#     trees.md, so the rules were copied, not re-synthesised
#
# Deterministic, disk-only. Exit 0 pass, 1 fail, 2 usage/lookup.
# <trees.md> defaults to the bootstrapping-project reference. Pass the version
# that generated <dir> if it differs, since the verbatim check is version-matched.

set -u
dir="${1:?usage: check-conventions-contract.sh <dir> [<trees.md>]}"
trees="${2:-$(dirname "$0")/../../../.claude/skills/bootstrapping-project/references/trees.md}"
conv="$dir/CONVENTIONS.md"

[ -f "$conv" ]  || { echo "FAIL: no CONVENTIONS.md at $dir"; exit 1; }
[ -f "$trees" ] || { echo "FAIL: trees.md not found at $trees"; exit 2; }

echo "conventions-contract: $conv"
fail=0
chk() { if [ "$2" -eq 0 ]; then printf '  ok    %s\n' "$1"; else printf '  FAIL  %s\n' "$1"; fail=1; fi; }

# no leaked authoring caveat
grep -qE "Unverified|⚠️" "$conv"; [ $? -ne 0 ]; chk "no Unverified/caveat line" $?

# enforcement stanza present
{ grep -q "enforcement:" "$conv" && grep -qE "^config:" "$conv" \
  && grep -qE "^runner:" "$conv" && grep -qE "^zoned:" "$conv"; }; chk "enforcement stanza (config/runner/zoned)" $?

# rule bullets copied verbatim from trees.md
# extract the rule bullets, the "- " lines before the enforcement stanza, so
# this does not depend on the section heading text
bullets=$(sed -n '1,/enforcement:/p' "$conv" | grep -E '^- ')
n=$(printf '%s\n' "$bullets" | grep -cE '^- ')
missing=0
if [ "$n" -eq 0 ]; then
  echo "  FAIL  no rule bullets found (parse failed or empty contract)"; missing=1
else
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    grep -qF -- "$line" "$trees" || { printf '  FAIL  rule not verbatim in trees.md: %s...\n' "$(printf '%s' "$line" | cut -c1-56)"; missing=1; }
  done <<EOF
$bullets
EOF
fi
chk "rule bullets present and verbatim in trees.md ($n found)" "$missing"

if [ "$fail" -eq 0 ]; then echo "PASS"; exit 0; else echo "FAILED"; exit 1; fi
