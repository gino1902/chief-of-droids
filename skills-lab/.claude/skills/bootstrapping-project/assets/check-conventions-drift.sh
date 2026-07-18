#!/usr/bin/env bash
# check-conventions-drift.sh <repo-dir> [<base-ref>]
#
# Verifies that a bootstrapped project's structural contract stays faithful:
# the CONVENTIONS.md contract, the lint config it names, and the tree agree,
# and any change to the contract since <base-ref> is traceable to a decision
# record. This is the lifecycle fidelity check for bootstrapping-project's
# CONVENTIONS.md output (Pass 3) and its generated enforcement (Pass 4 tail).
#
# CONVENTIONS.md must carry a machine-readable enforcement stanza, an HTML
# comment block the skill writes:
#
#   <!-- enforcement:
#   config: <relative-path> | none
#   runner: <command> | review
#   zoned: <space-separated prefix/* globs> | none
#   -->
#
# Three checks:
#   existence     config file named exists; the tool the runner names is wired into a gate
#   coverage      every folder under a zoned prefix has its path in the config,
#                 and no config-side drift leaves a zoned folder unenforced
#   traceability  if CONVENTIONS.md or the config changed since <base-ref> but no
#                 decision record was added in the same range, the change is untraceable
#
# The thinking goal sets config=none, runner=review, zoned=none: existence and
# coverage are skipped, traceability still runs.
#
# Deterministic, disk-only, no skill run. Exit 0 = pass, 1 = drift, 2 = usage
# or lookup error. Built from git, grep, sed, sort — no awk, no interpreter.

set -u
set -f  # no pathname expansion: zoned globs and git pathspecs are matched by us and by git, never by the shell
repo="${1:?usage: check-conventions-drift.sh <repo-dir> [<base-ref>]}"
base="${2:-}"

conv="$repo/CONVENTIONS.md"
[ -f "$conv" ] || { echo "FAIL: no CONVENTIONS.md in $repo"; exit 2; }

# --- parse the enforcement stanza -------------------------------------------
stanza=$(sed -n '/<!-- *enforcement:/,/-->/p' "$conv")
[ -n "$stanza" ] || { echo "FAIL: no enforcement stanza in $conv"; exit 2; }

field() { printf '%s\n' "$stanza" | grep -iE "^[[:space:]]*$1:" | head -1 | sed -E "s/^[[:space:]]*$1:[[:space:]]*//I; s/[[:space:]]*$//"; }
config=$(field config)
runner=$(field runner)
zoned=$(field zoned)

echo "conventions-drift: $repo"
echo "  stanza  config=${config:-<unset>}  runner=${runner:-<unset>}  zoned=${zoned:-<unset>}"

fail=0

# --- existence ---------------------------------------------------------------
if [ -n "$config" ] && [ "$config" != "none" ]; then
  if [ -f "$repo/$config" ]; then echo "  ok    config present   $config"
  else echo "  FAIL  config missing   $config"; fail=1; fi
fi

if [ -n "$runner" ] && [ "$runner" != "review" ]; then
  # A project gate may invoke the tool by full command (husky: `npx eslint .`) or by a
  # framework hook id (pre-commit: `id: ruff`). Match on the tool token, not the whole
  # runner string, so both styles register. The token is the first runner word that is not
  # a launcher, a flag, or a bare path.
  tool=""
  for t in $runner; do
    case "$t" in
      npx|npm|pnpm|yarn|bunx|uv|poetry|run|exec) continue ;;
      .|-*) continue ;;
      *) tool="$t"; break ;;
    esac
  done
  [ -z "$tool" ] && tool="$runner"
  gate_hits=$(grep -RIlF "$tool" \
    "$repo/.pre-commit-config.yaml" "$repo/package.json" "$repo/.husky" \
    "$repo/.github/workflows" "$repo/.gitlab-ci.yml" 2>/dev/null)
  if [ -n "$gate_hits" ]; then echo "  ok    runner wired     $tool (from: $runner)"
  else echo "  FAIL  runner not wired into any gate   $runner (tool: $tool)"; fail=1; fi
fi

# --- coverage ----------------------------------------------------------------
if [ -n "$zoned" ] && [ "$zoned" != "none" ]; then
  if [ -z "$config" ] || [ "$config" = "none" ]; then
    echo "  FAIL  zoned set but no config to hold the zones"; fail=1
  else
    tracked=$(git -C "$repo" ls-files 2>/dev/null) \
      || { echo "  FAIL  $repo is not a git repo (coverage needs git ls-files)"; exit 2; }
    for glob in $zoned; do
      case "$glob" in
        */\*) prefix="${glob%/\*}" ;;
        *) echo "  FAIL  unsupported zoned glob (expected prefix/*): $glob"; fail=1; continue ;;
      esac
      # immediate child dirs under the prefix, from tracked files. The trailing
      # slash in the grep keeps a file sitting directly in the prefix
      # (apps/.gitkeep) from being mistaken for a child folder.
      dirs=$(printf '%s\n' "$tracked" | grep -E "^$prefix/[^/]+/" | sed -E "s#^($prefix/[^/]+)/.*#\1#" | sort -u)
      if [ -z "$dirs" ]; then
        echo "  ok    zoned prefix has no folders yet   $prefix/*"
        continue
      fi
      while IFS= read -r d; do
        [ -z "$d" ] && continue
        if grep -qF "$d" "$repo/$config"; then printf '  ok    zoned            %s\n' "$d"
        else printf '  FAIL  folder unenforced (no zone in %s)   %s\n' "$config" "$d"; fail=1; fi
      done <<EOF
$dirs
EOF
    done
  fi
fi

# --- traceability ------------------------------------------------------------
if [ -n "$base" ]; then
  git -C "$repo" rev-parse --verify --quiet "$base" >/dev/null 2>&1 \
    || { echo "  FAIL  base ref not found: $base"; exit 2; }
  contract_paths="CONVENTIONS.md"
  [ -n "$config" ] && [ "$config" != "none" ] && contract_paths="$contract_paths $config"
  changed=$(git -C "$repo" diff --name-only "$base" -- $contract_paths)
  if [ -n "$changed" ]; then
    records=$(git -C "$repo" diff --name-only "$base" -- 'decisions/*' 'docs/adr/*' 'docs/**/adr/*')
    if [ -n "$records" ]; then
      echo "  ok    contract change traced to a decision record"
    else
      echo "  FAIL  contract changed since $base with no decision record:"
      printf '%s\n' "$changed" | sed 's/^/            /'
      fail=1
    fi
  else
    echo "  ok    contract unchanged since $base"
  fi
fi

if [ "$fail" -eq 0 ]; then echo "PASS"; exit 0; else echo "FAILED"; exit 1; fi
