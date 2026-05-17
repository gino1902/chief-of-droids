#!/bin/bash
# PreToolUse hook: emit cached Anthropic skill-authoring docs as additionalContext
# when /skill-creator is about to run. Refreshes the cache inline if older than 7 days.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CACHE_DIR="$SCRIPT_DIR/../cache/skill-docs"
REFRESH_SCRIPT="$SCRIPT_DIR/../scripts/refresh-skill-docs.sh"
STALE_SECONDS=$((7 * 24 * 3600))
PRIMARY="$CACHE_DIR/skills.md"

# Cross-platform mtime (macOS: stat -f %m, Linux: stat -c %Y)
mtime() { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null; }

if [ ! -f "$PRIMARY" ] || [ $(($(date +%s) - $(mtime "$PRIMARY"))) -gt "$STALE_SECONDS" ]; then
  bash "$REFRESH_SCRIPT" >/dev/null 2>&1 || true
fi

[ -d "$CACHE_DIR" ] || exit 0
CONTENT=$(cat "$CACHE_DIR"/*.md 2>/dev/null)
[ -z "$CONTENT" ] && exit 0

printf '%s' "$CONTENT" | python3 -c '
import json, sys
content = sys.stdin.read()
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": "## Fresh Claude Code skill-authoring docs (cached locally, refreshed every 7 days)\n\n" + content
    }
}))'
