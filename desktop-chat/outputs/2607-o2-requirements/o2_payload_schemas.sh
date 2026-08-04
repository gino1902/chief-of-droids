#!/usr/bin/env bash
# Build a per-feed payload field inventory (TASK-092) via `claude -p` + the
# Microsoft 365 MCP connector. Sibling of o2_data_sources.sh, which lists the
# files and is forbidden from reading their contents. This one reads contents
# but is forbidden from emitting any value.
#
# Why keys only: the payloads carry personal data (workers, leave, CRA). The
# four things TASK-092 needs are answerable from field names plus two counts,
# so no row value ever has to leave the subprocess. The strict output grammar
# below is a whitelist, not a value blacklist: anything that is not a header,
# a count or a typed field path is rejected and nothing is written.
#
# This does NOT make the read safe in an absolute sense. Payload values still
# pass through the subprocess model context. It keeps them out of the parent
# session and off disk. The only route that removes the exposure entirely is
# doing this inside Databricks, which needs a dev workspace with the SharePoint
# UC connection (see ADR-009).
#
# Usage:
#   ./o2_payload_schemas.sh --probe            # ONE feed, verify the mechanism
#   ./o2_payload_schemas.sh                    # all feeds (refuses until probe passed)
#   ./o2_payload_schemas.sh --output PATH
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INVENTORY="$SCRIPT_DIR/o2-data-sources.md"
OUTPUT="$SCRIPT_DIR/o2-payload-schemas.md"
PROBE_STAMP="$SCRIPT_DIR/.probe-passed"
MODE=full

while [ $# -gt 0 ]; do
  case "$1" in
    --probe) MODE=probe ;;
    --output) OUTPUT="${2:?--output needs a path}"; shift ;;
    -h|--help) sed -n '2,25p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

DRIVE_ID="b!oqXdq5uZz0u1pcNG3wEqq6Nze9mlS-5Mmb1iNupWM9oFC9hXcZJpTaYx41QEcHIg"
ROOT_URI="file:///${DRIVE_ID}/root:/SQLI-INTERNAL/app-reports:"

# --- feed list: branch + leaf, derived from the committed inventory ---------
# Filenames in the inventory are stale (dated snapshots), so only the folder
# path is taken from it. The newest file is re-resolved at run time.
[ -r "$INVENTORY" ] || { echo "ERROR: $INVENTORY not readable. Run o2_data_sources.sh first." >&2; exit 1; }

FEEDS="$(awk -F'|' '
  /^\| *(analytic|cra|others|perso|project) *\|/ {
    url = $6
    gsub(/^ +| +$/, "", url)
    n = split(url, parts, "/")
    branch = parts[n-2]; leaf = parts[n-1]
    if (branch != "" && leaf != "") print branch "\t" leaf
  }' "$INVENTORY" | sort -u)"

FEED_COUNT="$(printf '%s\n' "$FEEDS" | grep -c . || true)"
[ "$FEED_COUNT" -ge 15 ] || { echo "ERROR: parsed only $FEED_COUNT feeds from the inventory, expected ~21." >&2; exit 1; }
echo "Parsed $FEED_COUNT feeds from the inventory." >&2

if [ "$MODE" = probe ]; then
  FEEDS="$(printf '%s\n' "$FEEDS" | head -1)"
  echo "Probe mode: $FEEDS" >&2
elif [ ! -e "$PROBE_STAMP" ]; then
  echo "ERROR: run --probe first. read_resource on a FILE uri is unverified;" >&2
  echo "       o2_data_sources.sh only ever descends folders. Do not attempt" >&2
  echo "       $FEED_COUNT reads before one is known to work." >&2
  exit 1
fi

# --- per-feed prompt --------------------------------------------------------
# Folder descent uses only returned URIs, the method already proven by
# o2_data_sources.sh. Reading the selected file is the one unproven step.
build_prompt() {
  local branch="$1" leaf="$2"
  cat <<EOF
You have the Microsoft 365 connector. Use ONLY the read_resource tool.

Root folder URI: ${ROOT_URI}
Target: branch "${branch}", leaf folder "${leaf}"

Method, follow exactly:
1. read_resource the root URI. Find the child entry named "${branch}". Use the
   file:/// URI it returns. Never construct a URI yourself.
2. read_resource that URI. Find the child entry named "${leaf}". Use its
   returned URI.
3. read_resource that URI to list files, named YYYY-MM-DD__<type>.json.
   Select the one whose date is newest.
4. read_resource the selected file to obtain its JSON content.
5. If step 4 does not return the file's content, output exactly:
   ERROR_NO_CONTENT
   and stop. Do not guess, infer or reconstruct a schema from the filename.

Then emit a field inventory. ABSOLUTE RULE: never output a value from the
file. Not as an example, not in a comment, not to illustrate a type. Values
are the one thing that must not leave this process. Emit only field paths,
inferred types and counts.

Output format, exactly these four line kinds and nothing else:

FEED\t${branch}\t${leaf}
FILE\t<selected filename>
RECORDS\t<integer count of records in the file>
FIELD\t<path>\t<type>\t<non-null count>

Rules for the FIELD lines:
- path uses dots for nesting and [] for arrays, for example worker.contract[].id
- if an object is keyed by a dynamic identifier rather than a fixed name,
  replace that segment with the literal <key> and do not reproduce the
  identifier. Example: records.<key>.status
- type is one of: string number boolean null object array mixed
- non-null count is how many records have that path populated
- one line per distinct path, sorted alphabetically
- no blank lines, no prose, no markdown, no code fences

Output nothing but those lines.
EOF
}

# --- strict grammar gate ----------------------------------------------------
# Whitelist. Any line that is not one of the four kinds fails the whole feed.
# Path segments are bounded and may not be all digits, which is what stops a
# dynamic identifier key leaking through as a field name.
PATH_RE='[A-Za-z_][A-Za-z0-9_]{0,63}(\[\])?(\.(<key>|[A-Za-z_][A-Za-z0-9_]{0,63})(\[\])?)*'
validate() {
  local body="$1" feed="$2" bad
  bad="$(printf '%s\n' "$body" | grep -vE "^(FEED\t[a-z_]+\t[a-z_0-9]+|FILE\t[0-9]{4}-[0-9]{2}-[0-9]{2}__[A-Za-z0-9_]+\.json|RECORDS\t[0-9]+|FIELD\t${PATH_RE}\t(string|number|boolean|null|object|array|mixed)\t[0-9]+)$" || true)"
  if [ -n "$bad" ]; then
    echo "REJECTED $feed: output does not match the grammar. Offending lines:" >&2
    printf '%s\n' "$bad" | head -10 >&2
    return 1
  fi
  printf '%s\n' "$body" | grep -q '^FIELD	' || { echo "REJECTED $feed: no FIELD lines." >&2; return 1; }
  return 0
}

# --- run --------------------------------------------------------------------
TMP="$(mktemp)"; trap 'rm -f "$TMP"' EXIT
OK=0; FAILED=0

while IFS=$'\t' read -r branch leaf; do
  [ -n "$branch" ] || continue
  echo "Reading ${branch}/${leaf}..." >&2
  body="$(claude -p "$(build_prompt "$branch" "$leaf")" \
    --allowedTools "mcp__claude_ai_Microsoft_365__read_resource" || true)"

  if printf '%s' "$body" | grep -q 'ERROR_NO_CONTENT'; then
    echo "STOP: read_resource did not return file content for ${branch}/${leaf}." >&2
    echo "      The connector cannot read payloads this way. Do not retry the" >&2
    echo "      other feeds. Escalate: this task needs the Databricks route." >&2
    exit 3
  fi

  if validate "$body" "${branch}/${leaf}"; then
    printf '%s\n' "$body" >> "$TMP"; OK=$((OK+1))
  else
    FAILED=$((FAILED+1))
  fi
done <<< "$FEEDS"

echo "Feeds accepted: $OK. Rejected: $FAILED." >&2
[ "$OK" -gt 0 ] || { echo "ERROR: nothing accepted, writing nothing." >&2; exit 1; }

if [ "$MODE" = probe ]; then
  echo "--- probe output ---" >&2
  cat "$TMP"
  touch "$PROBE_STAMP"
  echo "--- probe passed. Grammar held and content was returned. Re-run without --probe. ---" >&2
  exit 0
fi

{
  echo "# O2 payload field inventory"
  echo
  echo "Generated by \`o2_payload_schemas.sh\` on $(date +%Y-%m-%d). Field paths, types"
  echo "and non-null counts only. No payload values pass through this file by construction:"
  echo "the generator rejects any output that does not match its field-path grammar."
  echo
  echo "Feeds accepted: $OK. Rejected: $FAILED."
  echo
  echo '```'
  cat "$TMP"
  echo '```'
  echo
  echo "<!--"
  echo "Version: 1.0 | Last Updated: $(date +%Y-%m-%d) | Status: Draft"
  echo "-->"
} > "$OUTPUT"

echo "Wrote $OUTPUT" >&2
