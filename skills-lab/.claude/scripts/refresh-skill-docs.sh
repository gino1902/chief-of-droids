#!/bin/bash
# Fetch latest Anthropic skill-authoring docs into local cache.
# Idempotent. Run manually to force-refresh, or let inject-skill-creator-context.sh
# call it when the cache is older than 7 days.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CACHE_DIR="$SCRIPT_DIR/../cache/skill-docs"
mkdir -p "$CACHE_DIR"

URLS=(
  "https://code.claude.com/docs/en/skills.md"
  "https://code.claude.com/docs/en/best-practices.md"
  "https://code.claude.com/docs/en/features-overview.md"
)

for url in "${URLS[@]}"; do
  curl -sLf "$url" -o "$CACHE_DIR/$(basename "$url")"
done

echo "Refreshed: $CACHE_DIR"
