#!/usr/bin/env python3
"""
claude-proxy.py — Claude Desktop token tracking proxy
Wraps /v1/messages, accumulates usage per turn, prints session summary on exit.

Usage:
    python3 claude-proxy.py

Requirements:
    pip install anthropic --break-system-packages

Environment:
    ANTHROPIC_API_KEY   — required
    CLAUDE_MODEL        — optional, default: claude-sonnet-4-6
"""

import os
import sys
import signal
import anthropic

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not API_KEY:
    print("⚠️  ANTHROPIC_API_KEY not set. Export it before running this script.")
    sys.exit(1)

client = anthropic.Anthropic(api_key=API_KEY)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
messages = []
tracking = False

session_totals = {
    "input_tokens": 0,
    "output_tokens": 0,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
}
turn_count = 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def fmt_tokens(n: int) -> str:
    return f"{n:,}"


def print_usage(usage, turn: int):
    inp = usage.input_tokens
    out = usage.output_tokens
    cache_cr = getattr(usage, "cache_creation_input_tokens", 0) or 0
    cache_rd = getattr(usage, "cache_read_input_tokens", 0) or 0
    print(
        f"\n  [turn {turn}] in={fmt_tokens(inp)} | out={fmt_tokens(out)}"
        + (f" | cache_write={fmt_tokens(cache_cr)}" if cache_cr else "")
        + (f" | cache_read={fmt_tokens(cache_rd)}" if cache_rd else "")
    )


def print_summary():
    if not tracking or turn_count == 0:
        return
    t = session_totals
    total = t["input_tokens"] + t["output_tokens"]
    print("\n" + "─" * 52)
    print("  Session summary")
    print("─" * 52)
    print(f"  Turns            : {turn_count}")
    print(f"  Input tokens     : {fmt_tokens(t['input_tokens'])}")
    print(f"  Output tokens    : {fmt_tokens(t['output_tokens'])}")
    if t["cache_creation_input_tokens"]:
        print(f"  Cache writes     : {fmt_tokens(t['cache_creation_input_tokens'])}")
    if t["cache_read_input_tokens"]:
        print(f"  Cache reads      : {fmt_tokens(t['cache_read_input_tokens'])}")
    print(f"  Total tokens     : {fmt_tokens(total)}")
    print("─" * 52 + "\n")


def handle_exit(sig=None, frame=None):
    print_summary()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


# ---------------------------------------------------------------------------
# Session start
# ---------------------------------------------------------------------------
print(f"\nClaude proxy — model: {MODEL}")
answer = input("Track token consumption for this session? (y/n): ").strip().lower()
tracking = answer == "y"
if tracking:
    print("  Tracking enabled — usage printed after each turn.\n")
else:
    print("  Tracking disabled — plain passthrough.\n")

print('Type your message and press Enter. Type "exit" to quit.\n')

# ---------------------------------------------------------------------------
# Conversation loop
# ---------------------------------------------------------------------------
while True:
    try:
        user_input = input("You: ").strip()
    except EOFError:
        handle_exit()

    if not user_input:
        continue

    if user_input.lower() in ("exit", "quit"):
        handle_exit()

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=8096,
            messages=messages,
        )
    except anthropic.APIError as e:
        print(f"\n⚠️  API error: {e}\n")
        messages.pop()
        continue

    assistant_text = response.content[0].text
    messages.append({"role": "assistant", "content": assistant_text})

    print(f"\nClaude: {assistant_text}\n")

    if tracking:
        turn_count += 1
        usage = response.usage
        session_totals["input_tokens"] += usage.input_tokens
        session_totals["output_tokens"] += usage.output_tokens
        session_totals["cache_creation_input_tokens"] += (
            getattr(usage, "cache_creation_input_tokens", 0) or 0
        )
        session_totals["cache_read_input_tokens"] += (
            getattr(usage, "cache_read_input_tokens", 0) or 0
        )
        print_usage(usage, turn_count)
