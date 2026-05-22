# Session Identity Recommendation (parked)

Status: parked recommendation. Captures the proposed mechanism for deriving a per-session identifier in Claude Desktop chat, supporting the project-bind sentinel design discussed on 2026-05-14. Not yet committed as the framework approach.

## Problem

The chief-of-droids dispatcher design (Project Instructions reads `<project>/CLAUDE.md` once per session and verifies on every subsequent turn) requires a sentinel keyed to "this Claude Desktop chat session." Without a stable session identifier, the sentinel cannot distinguish a current-session bind from a stale prior-session bind — the silent-failure case the design is meant to prevent.

Claude Desktop does not expose a session ID to the model directly. The mechanism must be derived.

## Mechanisms considered

| Mechanism | How it works | Robustness | Cost |
|---|---|---|---|
| `recent_chats[0].uri` | Call `recent_chats n=1`; the most recently updated session is the current one. The returned uri is the Claude-assigned session identifier and is stable for the session's lifetime. | High | One `recent_chats` call per turn |
| First-user-message SHA + start-timestamp window | Hash first user message + session-start timestamp rounded to the minute | Medium — collisions possible if phrasing recurs in the same window | Cheap; deterministic from transcript |
| Composite (uri + first-message hash) | Both must match | Highest | Both prior costs |
| Time-window only, no session key | Sentinel valid if written within N minutes | Low — concurrent sessions corrupt; long pauses produce false reload | Cheapest; wrong on concurrent use |

## Recommendation

Use `recent_chats[0].uri` as the session identifier.

Rationale: it is the actual Claude-assigned session URI, stable across turns of the same session, distinct across sessions, and requires no attention to transcript content. The "reliable first-turn detection" problem typically associated with bootstrap-once mechanisms dissolves by inversion — every turn calls `recent_chats n=1` and compares against the sentinel's stored uri. The two-phase bootstrap (reset, then bind) collapses into a single per-turn predicate.

This also resolves two structural risks: no first-turn recursion (every turn behaves identically), and no sentinel concurrency collision (two concurrent sessions have two different uris and write to separate sentinel files).

## Downstream implications

- Sentinel path: `chief-of-droids/.sessions/<urlencoded-uri>.json`
- Reset semantics: nothing to reset. New sessions find no sentinel and run bootstrap. Old sentinels sit inert; cleanup is a periodic task.
- Per-turn verify rule: read sentinel for current uri → absent or `project` empty → ask for project; present but `claude_md_sha` mismatches disk → reload; otherwise proceed silently.
- Cost: one `recent_chats` call per turn. Consolidate with the existing Session Hygiene call in workspace `CLAUDE.md` to avoid duplication.

## Open questions blocking finalization

These do not depend on the session-ID choice but block the overall dispatcher spec:

- Is `chief-of-droids/skills/` retained as a shared tier alongside `<project>/skills/`, or do projects own their full skill set?
- Does the current workspace-level `CLAUDE.md` dissolve into Project Instructions, duplicate per project, or persist as a layer below project CLAUDE.md (hierarchical load)?

---

| Field        | Value       |
|--------------|-------------|
| Version      | 1.0         |
| Last Updated | 2026-05-14  |
| Status       | Draft       |
