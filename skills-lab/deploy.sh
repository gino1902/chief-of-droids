#!/usr/bin/env bash
#
# deploy.sh — copy one or more skills from skills-lab into a target project.
#
# Usage:
#   bash deploy.sh <target-repo> <skill-or-package>... [--force]
#
# A <skill-or-package> is either a skill directory name under .claude/skills/,
# or a package name matching packages/<name>.txt (expanded to its skill list).
#
# Versioning: the version of every deployed skill is the skills-lab short commit
# SHA at deploy time. Run `git show <sha>:.claude/skills/<skill>/SKILL.md` in
# skills-lab to see exactly what shipped.
#
# Footer gate: a skill is refused if its SKILL.md footer Status is Draft or is
# missing. Deploying a draft skill into a real project could mislead, so it is
# blocked. Pass --force to override (loudly).
#
# Dirty-tree guard: if skills-lab has uncommitted changes the SHA cannot
# reconstruct what shipped, so deploy is blocked unless --force.
#
# Records written:
#   <target>/.claude/skills/DEPLOYED.md   install record (one row per skill)
#   <skills-lab>/DEPLOYMENTS.md           outbound ledger (one row per run)

set -euo pipefail

LAB_ROOT="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$LAB_ROOT/.claude/skills"
PKG_DIR="$LAB_ROOT/packages"

# Statuses that are allowed to deploy. Tighten to '^final$' when skills mature.
ALLOWED_STATUS_REGEX='^(review|final)$'

# --- parse args -------------------------------------------------------------
FORCE=0
POSITIONAL=()
for a in "$@"; do
  if [ "$a" = "--force" ]; then
    FORCE=1
  else
    POSITIONAL+=("$a")
  fi
done

if [ "${#POSITIONAL[@]}" -lt 2 ]; then
  echo "usage: bash deploy.sh <target-repo> <skill-or-package>... [--force]" >&2
  exit 2
fi

TARGET="${POSITIONAL[0]}"
REQUESTS=("${POSITIONAL[@]:1}")

if [ ! -d "$TARGET" ]; then
  echo "error: target repo not found: $TARGET" >&2
  exit 2
fi

# --- resolve requests to a (skill, origin-package) list ---------------------
SKILLS=()
ORIGINS=()

add_skill() {
  local skill="$1" origin="$2" existing
  for existing in "${SKILLS[@]:-}"; do
    [ "$existing" = "$skill" ] && return 0
  done
  SKILLS+=("$skill")
  ORIGINS+=("$origin")
}

for req in "${REQUESTS[@]}"; do
  if [ -f "$PKG_DIR/$req.txt" ]; then
    while IFS= read -r line; do
      line="$(printf '%s' "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
      [ -z "$line" ] && continue
      case "$line" in \#*) continue ;; esac
      add_skill "$line" "$req"
    done < "$PKG_DIR/$req.txt"
  else
    add_skill "$req" "-"
  fi
done

# --- footer gate ------------------------------------------------------------
skill_status() {
  grep -iE '^\|[[:space:]]*Status[[:space:]]*\|' "$SKILLS_DIR/$1/SKILL.md" 2>/dev/null \
    | head -1 | cut -d'|' -f3 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}

echo "Checking ${#SKILLS[@]} skill(s)..."
GATE_FAIL=0
for skill in "${SKILLS[@]}"; do
  dir="$SKILLS_DIR/$skill"
  if [ ! -d "$dir" ]; then
    echo "  ✗ $skill: not found in $SKILLS_DIR" >&2
    GATE_FAIL=1
    continue
  fi
  status="$(skill_status "$skill")" || true
  low="$(printf '%s' "$status" | tr '[:upper:]' '[:lower:]')"
  if [ -z "$status" ]; then
    echo "  ✗ $skill: no Status field in SKILL.md footer" >&2
    GATE_FAIL=1
  elif ! printf '%s' "$low" | grep -qE "$ALLOWED_STATUS_REGEX"; then
    echo "  ✗ $skill: Status is '$status' (must be Review or Final, not Draft)" >&2
    GATE_FAIL=1
  else
    echo "  ✓ $skill: Status '$status'"
  fi
done

if [ "$GATE_FAIL" -ne 0 ]; then
  if [ "$FORCE" -eq 1 ]; then
    echo "WARNING: footer gate failed but --force set; deploying anyway." >&2
  else
    echo "Aborted: footer gate failed. Fix status, or re-run with --force." >&2
    exit 1
  fi
fi

# --- dirty-tree guard -------------------------------------------------------
if [ -n "$(git -C "$LAB_ROOT" status --porcelain)" ]; then
  if [ "$FORCE" -eq 1 ]; then
    echo "WARNING: skills-lab has uncommitted changes; SHA will not reconstruct what ships." >&2
  else
    echo "Aborted: skills-lab has uncommitted changes. Commit first, or re-run with --force." >&2
    exit 1
  fi
fi

SHA="$(git -C "$LAB_ROOT" rev-parse --short HEAD)"
TODAY="$(date +%F)"

# --- copy + record ----------------------------------------------------------
TARGET_SKILLS="$TARGET/.claude/skills"
mkdir -p "$TARGET_SKILLS"

DEPLOYED="$TARGET_SKILLS/DEPLOYED.md"
if [ ! -f "$DEPLOYED" ]; then
  {
    echo "# Deployed skills"
    echo
    echo "Skills deployed into this project from skills-lab. Version is the skills-lab"
    echo "commit SHA at deploy time; run \`git show <sha>:.claude/skills/<skill>/\` in"
    echo "skills-lab to see exactly what shipped."
    echo
    echo "| Skill | Version | Package | Date | Source |"
    echo "|-------|---------|---------|------|--------|"
  } > "$DEPLOYED"
fi

LEDGER="$LAB_ROOT/DEPLOYMENTS.md"
if [ ! -f "$LEDGER" ]; then
  {
    echo "# Deployments ledger"
    echo
    echo "Outbound record of skills deployed from skills-lab. One row per deploy run."
    echo
    echo "| Date | Target | Skills | Version |"
    echo "|------|--------|--------|---------|"
  } > "$LEDGER"
fi

echo "Deploying at version $SHA ..."
i=0
for skill in "${SKILLS[@]}"; do
  origin="${ORIGINS[$i]}"
  i=$((i + 1))
  src="$SKILLS_DIR/$skill"
  dest="$TARGET_SKILLS/$skill"
  rm -rf "$dest"
  cp -R "$src" "$dest"
  printf '| %s | %s | %s | %s | %s |\n' "$skill" "$SHA" "$origin" "$TODAY" "skills-lab" >> "$DEPLOYED"
  echo "  → $skill"
done

SKILL_LIST="$(printf '%s, ' "${SKILLS[@]}" | sed 's/, $//')"
printf '| %s | %s | %s | %s |\n' "$TODAY" "$TARGET" "$SKILL_LIST" "$SHA" >> "$LEDGER"

echo "Done. ${#SKILLS[@]} skill(s) → $TARGET_SKILLS"
echo "Recorded in $DEPLOYED and $LEDGER"
