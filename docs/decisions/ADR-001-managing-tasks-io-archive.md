# ADR-001 — managing-tasks I/O: archive done entries (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-03-31 |
| Status | Decided |
| Task | TASK-048 |

---

## Context

managing-tasks read/write operations were slow and token-heavy. Every workflow
loaded TASKS.md in full — including the ✅ Done section, which had grown to 30
entries (~70% of file size) and would grow unboundedly. The original task scope
framed this as a caching/batching problem, but challenge rounds reframed it as
two distinct bottlenecks:

1. **Token volume** — Done section loaded on every operation regardless of relevance
2. **Round-trip overhead** — 3 MCP reads before every write (schema + TASKS.md + qa-checklist)

Only bottleneck 1 was addressed in this session. Bottleneck 2 remains open.

---

## Options evaluated

**Option A — Archive done entries**
Move ✅ Done entries to an append-only `archive.md` co-located with TASKS.md.
TASKS.md Done section remains present but always empty. Archive read on explicit
`show archive` trigger only.

**Option B — SQLite MCP**
Replace Filesystem read/write with targeted SQL queries against a SQLite database.
`SELECT WHERE status=backlog`, `UPDATE SET status=done` — only query results enter
context. No unbounded file growth. Proper relational storage.

**Options not pursued**
- Read-once-per-session caching: architecturally unsound — TASKS.md content is
  already in context once read; the real cost is the initial read, not repetition.
  Stale-read risk if user edits file externally mid-session.
- Batched writes: misnomer — each workflow already produces exactly one write.
  Multi-write scenario (two sequential operations) still requires two reads of
  reference files (schema + qa-checklist); this is bottleneck 2, not a batching problem.
- Split section files (backlog.md / in-progress.md): adds routing complexity
  to every workflow with marginal token saving over Option A.

---

## Decision

**Option A chosen as immediate fix. Option B deferred as TASK-051.**

### Rationale

| Criterion | Option A | Option B |
|:----------|:---------|:---------|
| Implementable today | Yes — no new dependencies | No — SQLite MCP install unconfirmed |
| Token reduction | ~70% on TASKS.md reads immediately | Near-zero (query results only) |
| Latency reduction | None — same MCP call count | Yes — targeted queries replace full reads |
| New MCP required | No | Yes |
| Friction to other skills | None | None (storage is internal to managing-tasks) |
| Addresses bottleneck 1 (token volume) | Yes | Yes |
| Addresses bottleneck 2 (round-trips) | No | Yes |

Option A is the correct immediate action: zero risk, zero new dependencies,
solves the dominant cost driver today. Option B is the correct long-term target
but has an unverified prerequisite (SQLite MCP installable in WSL2).

---

## Consequences

- TASKS.md Done section is always empty post-migration — canonical done record is archive.md
- `done task` workflow appends to archive.md; TASKS.md is never written with done entries again
- `show archive` is the explicit trigger for done history retrieval
- Bottleneck 2 (reference file reads per operation) remains unaddressed — still 3 reads per write workflow
- TASK-051 tracks Option B implementation when SQLite MCP prerequisite is confirmed

---

| Field | Value |
|:------|:------|
| Version | 1.0 |
| Last Updated | 2026-03-31 |
| Status | Final |
