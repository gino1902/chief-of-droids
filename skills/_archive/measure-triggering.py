#!/usr/bin/env python3
"""
Measure real triggering of the legacy skills/ collection from a claude.ai data export.

The Desktop router (skills/HOW-TO-TRIGGER.md) emits a routing line on line 2 of
every assistant turn:  🧭 skills: <name>@<version>[ (carried|failed)], ...  |  🧭 skills: none
This script counts those lines per skill. That is the authoritative usage signal
for the 10 legacy skills, which run only in Claude Desktop and never appear in
Claude Code transcripts.

Get the input: claude.ai -> Settings -> Privacy/Account -> Export data. You receive
a zip with conversations.json. Unzip it and point this script at the folder or the file.

Usage:
    python3 measure-triggering.py <path-to-export-dir-or-conversations.json>

It scans every assistant message, so it captures the desktop-chat project (the only
place the router runs) without needing conversation->project linkage from the export.
"""
import json, os, re, sys
from collections import defaultdict

# The 10 legacy skills. Any name outside this set is still reported, under "OTHER".
TARGETS = [
    "analyzing-business-cases", "architecting-data-platforms", "brainstorming-ideas",
    "creating-skills", "editing-docs", "executing-tasks", "managing-sessions",
    "managing-tasks", "project-bootstrapping", "reviewing-tech-claims",
]

ROUTING = re.compile(r"🧭\s*skills:\s*(.+)")
# one entry: name[@version][ (state)]  -> capture name + optional state
ENTRY = re.compile(r"([a-z][a-z0-9-]+)(?:@[^\s,()]+)?(?:\s*\(([a-z]+)\))?")


def find_conversations(path):
    """Return the conversations list from a dir or a json file."""
    if os.path.isdir(path):
        cand = os.path.join(path, "conversations.json")
        if not os.path.exists(cand):
            hits = [f for f in os.listdir(path) if f.endswith(".json") and "conversation" in f.lower()]
            cand = os.path.join(path, hits[0]) if hits else None
        path = cand
    if not path or not os.path.exists(path):
        sys.exit(f"conversations.json not found at {path!r}")
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return data if isinstance(data, list) else data.get("conversations", [])


def message_text(msg):
    """Pull text from both legacy `text` and newer `content[].text` shapes."""
    parts = []
    t = msg.get("text")
    if isinstance(t, str):
        parts.append(t)
    for block in msg.get("content", []) or []:
        if isinstance(block, dict) and isinstance(block.get("text"), str):
            parts.append(block["text"])
    return "\n".join(parts)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    convos = find_conversations(sys.argv[1])

    # per skill: fresh / carried / failed counts, distinct convos, date range
    stats = defaultdict(lambda: {"fresh": 0, "carried": 0, "failed": 0,
                                 "convos": set(), "first": None, "last": None})
    turns_total = turns_routed = turns_none = 0

    for conv in convos:
        cid = conv.get("uuid") or conv.get("name")
        for msg in conv.get("chat_messages", []) or []:
            if msg.get("sender") != "assistant":
                continue
            m = ROUTING.search(message_text(msg))
            if not m:
                continue
            turns_total += 1
            date = (msg.get("created_at") or conv.get("created_at") or "")[:10]
            body = m.group(1).strip()
            if body.lower().startswith("none"):
                turns_none += 1
                continue
            turns_routed += 1
            for name, state in ENTRY.findall(body):
                key = name if name in TARGETS else "OTHER:" + name
                s = stats[key]
                s[{"carried": "carried", "failed": "failed"}.get(state, "fresh")] += 1
                s["convos"].add(cid)
                if date:
                    s["first"] = min(s["first"] or date, date)
                    s["last"] = max(s["last"] or date, date)

    print(f"turns with a routing line : {turns_total}")
    print(f"  routed to >=1 skill     : {turns_routed}")
    print(f"  explicit 'none'         : {turns_none}\n")

    hdr = f'{"skill":30} {"fresh":>5} {"carr":>5} {"fail":>5} {"convo":>5}  {"first":10} {"last":10}'
    print(hdr); print("-" * len(hdr))
    def sort_key(k): return (-stats[k]["fresh"], k)
    for key in [k for k in TARGETS if k in stats] + sorted([k for k in stats if k.startswith("OTHER:")]):
        s = stats[key]
        print(f'{key:30} {s["fresh"]:>5} {s["carried"]:>5} {s["failed"]:>5} '
              f'{len(s["convos"]):>5}  {s["first"] or "-":10} {s["last"] or "-":10}')
    missing = [k for k in TARGETS if k not in stats]
    if missing:
        print("\nnever triggered:", ", ".join(missing))


if __name__ == "__main__":
    main()
