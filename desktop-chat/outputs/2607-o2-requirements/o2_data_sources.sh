#!/usr/bin/env bash
# Rebuild the O2 data-sources table via `claude -p` + the Microsoft 365 MCP
# connector (reuses the connector auth; no Azure app / sign-in needed).
#
# The model produces the markdown table on stdout. This script always prints
# it, then writes the file: silently if it does not exist yet, or after a y/N
# confirm if it would overwrite. --yes skips the confirm (for cron).
#
# Usage:
#   ./o2_data_sources.sh                 # print, then create or confirm-overwrite
#   ./o2_data_sources.sh --yes           # overwrite without confirming
#   ./o2_data_sources.sh --output PATH   # write somewhere else
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT="$SCRIPT_DIR/o2-data-sources.md"
ASSUME_YES=0

while [ $# -gt 0 ]; do
  case "$1" in
    --yes|-y) ASSUME_YES=1 ;;
    --output) OUTPUT="${2:?--output needs a path}"; shift ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

DRIVE_ID="b!oqXdq5uZz0u1pcNG3wEqq6Nze9mlS-5Mmb1iNupWM9oFC9hXcZJpTaYx41QEcHIg"

PROMPT=$(cat <<EOF
You have the Microsoft 365 connector. Build a data-source manifest from
SharePoint and output ONLY a GitHub markdown table, nothing else.

Drive id: ${DRIVE_ID}
Root folder URI: file:///${DRIVE_ID}/root:/SQLI-INTERNAL/app-reports:
URL base: https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports

Use ONLY the read_resource tool. Do not call search. Never read file contents.
read_resource on a folder returns child entries, each with a name and a
file:/// URI. Descend into folders using the returned URI; build url paths from
the returned names.

Method, follow exactly:
1. read_resource the root URI to list the branch folders.
2. read_resource each branch folder to list its leaf folders.
3. read_resource each leaf folder to list its files. Files are named
   YYYY-MM-DD__<type>.json. Select the one whose YYYY-MM-DD date is newest.
4. Build each row from the names you traversed:
   branch = branch folder name.
   name   = selected filename.
   url    = URL base + "/" + branch + "/" + leaf folder name + "/" + name.
5. Output ONLY this table, no prose before or after. Header exactly:

| branch | name | url |
|--------|------|-----|

One row per leaf folder, sorted by branch then name. Output nothing but the table.
EOF
)

echo "Running claude -p (this walks the folder tree; may take a minute)..." >&2
TABLE="$(claude -p "$PROMPT" \
  --allowedTools "mcp__claude_ai_Microsoft_365__read_resource")"

# --- sanity check (before the gate) ---------------------------------------
if ! printf '%s\n' "$TABLE" | grep -q '^| branch | name | url'; then
  echo "ERROR: output has no valid table header. Got:" >&2
  printf '%s\n' "$TABLE" >&2
  exit 1
fi
ROWS=$(printf '%s\n' "$TABLE" | grep -Ec '^\| (analytic|cra|others|perso|project) \|')
if [ "$ROWS" -lt 15 ]; then
  echo "ERROR: only $ROWS data rows, expected ~21. Refusing to continue." >&2
  printf '%s\n' "$TABLE" >&2
  exit 1
fi
echo "OK: $ROWS data rows." >&2

# --- show, then write gate -------------------------------------------------
printf '%s\n' "$TABLE"                          # always show the result

if [ -e "$OUTPUT" ] && [ "$ASSUME_YES" -eq 0 ]; then
  printf '\nOverwrite %s? [y/N] ' "$OUTPUT" >&2
  read -r answer || answer=""                   # EOF (no tty) -> No, nothing clobbered
  case "$answer" in
    y|Y|yes|YES) ;;
    *) echo "Kept existing file, nothing written." >&2; exit 0 ;;
  esac
fi

mkdir -p "$(dirname "$OUTPUT")"                  # create it anyway, no matter the dir
printf '%s\n' "$TABLE" > "$OUTPUT"
echo "Wrote $OUTPUT" >&2
