# Report — ticket-api

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |    0     |     8      |
| Info     |    23    |    N/A     |

## Phase 0 — Pre-flight
- [INFO] Parsed args: slug=ticket-api, path=ticket-api.md, type=technical.
- [INFO] Repo root = cwd (CLAUDE.md present); output dir requirements/ticket-api/ resolved.
- [INFO] No prior ticket-api-requirements.md found; version initialized to 0.1.
- [INFO] Substrate read: `.md`, non-empty, non-whitespace.

Outstanding: 0 blocking, 0 warnings, 4 info

## Phase 1 — Framing
- [INFO] Title taken from H1: "ticket-api".
- [INFO] Explicit purpose statement detected; no inference required.
- [INFO] Scope: positive signal ("Covers") and negation signals ("Out of scope", "owned by") both detected.
- [INFO] Actors: upstream (agent over HTTP) and downstream (ticket store) both detected.

Outstanding: 0 blocking, 0 warnings, 4 info

## Phase 2 — Drafting
- [INFO] FR-001 classified Mutate-shape (create); ERR-001 paired in the same pass.
- [INFO] FR-002 classified Acquire-shape (return by id); ERR-002 paired in the same pass.
- [INFO] CON-001 classified via FR-vs-CON tie-breaker row 3 (invariant "never changes").
- [INFO] NFR-002 mapped to Performance slot from latency signal ("300 ms", "95th percentile").
- [INFO] SEC-001 derived from Authorization category (b).
- [INFO] OBS-001 derived from Metric-exposure category (a); metric `ticket.created`.
- [INFO] IR-IN and IR-OUT rendered from the inbound HTTP interface signal.
- [WARNING-UNRESOLVED] NFR-001 (Reliability/correctness) universal slot — substrate silent; rendered N/A. → user supplies a reliability signal or accepts N/A.
- [WARNING-UNRESOLVED] NFR-002 modality set to SHOULD — substrate names no failure consequence for the 300 ms target (consequence unstated). → user confirms an enforcement path or accepts SHOULD.
- [WARNING-UNRESOLVED] DR sub-section rendered N/A — no typed data-model signal in substrate. → user supplies a data model or accepts N/A.
- [WARNING-UNRESOLVED] TR sub-section rendered N/A — no transformation signal in substrate. → user supplies a transformation rule or accepts N/A.

Outstanding: 0 blocking, 4 warnings, 7 info

## Phase 3 — Vocabulary
- [INFO] Glossary candidates via rule 2 (backtick): ticket, agent, ticket.created.
- [INFO] Stop-word filter applied; 0 candidates dropped.
- [WARNING-UNRESOLVED] Glossary entry "ticket" auto-derived — verify definition. → user confirms or corrects the definition.
- [WARNING-UNRESOLVED] Glossary entry "agent" auto-derived — verify definition. → user confirms or corrects the definition.
- [WARNING-UNRESOLVED] Glossary entry "ticket.created" auto-derived — verify definition. → user confirms or corrects the definition.

Outstanding: 0 blocking, 3 warnings, 2 info

## Phase 4 — Taxonomy hygiene
- [INFO] ID hygiene: all categories dense, no duplicates, all formats valid.
- [INFO] ERR coverage complete: FR-001→ERR-001, FR-002→ERR-002.
- [WARNING-UNRESOLVED] term "payload" used in FR-001 is absent from §Glossary. → user defines "payload" in the glossary or substrate.

Outstanding: 0 blocking, 1 warnings, 2 info

## Phase 5 — Verification
- [INFO] AC derived for all 11 active requirements; NFR-001 silent slot carries no AC.
- [INFO] Scorecard complete; FR-001 Unambiguous ✗ references the Phase 4 "payload" term-absence Warning.

Outstanding: 0 blocking, 0 warnings, 2 info

## Phase 6 — Format
- [INFO] Version 0.1 (initial); Status Draft; Last Updated 2026-07-16.
- [INFO] Write order: ticket-api-requirements.md then ticket-api-report.md.

Outstanding: 0 blocking, 0 warnings, 2 info

Outstanding: 0 blocking, 8 warnings, 23 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
