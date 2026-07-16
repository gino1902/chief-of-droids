#!/bin/bash
# Hook handler for /skill-creator: emit cached Anthropic skill-authoring docs as
# additionalContext. Wired to both PreToolUse(Skill) and UserPromptExpansion in
# settings.json. Echoes the event name back so Claude Code accepts the output for
# whichever event invoked it. Refreshes the cache inline if older than 7 days.

HOOK_INPUT=$(cat)
HOOK_EVENT=$(printf '%s' "$HOOK_INPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("hook_event_name","PreToolUse"))' 2>/dev/null)
[ -z "$HOOK_EVENT" ] && HOOK_EVENT="PreToolUse"

# Lightweight visibility: one line per fire. Truncate with `: > /tmp/skill-creator-hook.log`.
echo "$(date -Iseconds) fired (event=$HOOK_EVENT)" >> /tmp/skill-creator-hook.log

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

HOOK_EVENT="$HOOK_EVENT" printf '%s' "$CONTENT" | HOOK_EVENT="$HOOK_EVENT" python3 -c '
import json, sys, os
content = sys.stdin.read()
event = os.environ.get("HOOK_EVENT","PreToolUse")
convention = (
    "\n\n---\n\n"
    "## Project convention (skills-lab) — applies on top of the docs above\n\n"
    "Any SKILL.md or other .md file this run writes to disk must end with the "
    "canonical version block from CLAUDE.md, and only these three fields:\n\n"
    "| Field        | Value                  |\n"
    "|--------------|------------------------|\n"
    "| Version      | 1.x                    |\n"
    "| Last Updated | YYYY-MM-DD             |\n"
    "| Status       | Draft / Review / Final |\n\n"
    "Audit or provenance metadata (target model, target environment, "
    "best-practices reference, revision source) goes in the report that produced "
    "the artifact, not in the footer. This overrides the Anthropic template above "
    "where they differ."
)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": event,
        "additionalContext": "## Fresh Claude Code skill-authoring docs (cached locally, refreshed every 7 days)\n\n" + content + convention
    }
}))'
