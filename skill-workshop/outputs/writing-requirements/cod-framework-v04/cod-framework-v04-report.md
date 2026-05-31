# Report — cod-framework-v04

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |    8     |     1      |
| Info     |    6     |    N/A     |

## Phase 0 — Pre-flight

- [INFO] Slug `cod-framework-v04` validated against `^[a-z0-9-]+$`; no banned tokens (`requirement`, `req`, `reqs`).
- [INFO] Type `generic` resolved → loaded `references/template-s1.md`.
- [INFO] Substrate `./requirements/substrates/framework-requirements.md` resolved and read; `.md` extension confirmed.
- [INFO] Repo root resolved at `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/` (CLAUDE.md present in cwd).
- [INFO] Output directory `requirements/cod-framework-v04/` created.
- [INFO] No prior `cod-framework-v04-requirements.md` found → fresh pass; initial version `0.1`.

Outstanding: 0 blocking, 0 warnings, 6 info

## Phase 1 — Framing

- [INFO] Title resolved from substrate H1 (`Chief of Droids — Framework Requirements`).
- [INFO] Purpose synthesized from explicit "evolution purpose" paragraph plus framing prose; no ambiguity.
- [WARNING] §Scope — In Scope: substrate carries no explicit "in scope / covers / handles" wording. Items derived from the categories of declared requirements (functional, access, governance, observability, non-functional). Operator review required to confirm coverage. → Replace inferred bullets or confirm in next substrate revision.
- [WARNING] §Scope — Out of Scope: substrate has explicit "Explicitly out of scope" table; rendered as bullets verbatim. Only the inline parenthetical references were rewritten to point at v04 IDs. Operator review of cross-references required. → Verify each FR cross-reference in §Out of Scope.
- [INFO] §Actors derived from substrate Glossary entries `operator`, `drafting agent`, `executing agent`. Direction values follow input/output flow described in `input artifact` and `output artifact` definitions.

Outstanding: 0 blocking, 2 warnings, 2 info

## Phase 2 — Drafting

**ID stability scan:** substrate IDs use two-digit suffix (`FR-01`, `AR-01`, `GR-01`, `OR-01`, `NFR-01`). Regex `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b` requires three digits and does not include `AR`, `GR`, `OR` prefixes. No substrate IDs matched the regex; all output IDs are fresh per S1 numbering rules.

- [WARNING] Substrate IDs renumbered. Mapping below. Cross-document references to substrate IDs (`FR-01`, `AR-03`, etc.) elsewhere in the workspace will not resolve to v04 IDs without manual update. → Decide whether to align substrate IDs with the three-digit `<CAT>-NNN` convention going forward.

| Substrate ID | v04 ID  | Note |
|:-------------|:--------|:-----|
| FR-01        | FR-001  | — |
| FR-02        | FR-002  | — |
| FR-03        | FR-003  | — |
| FR-04        | FR-004  | — |
| FR-05        | FR-005  | — |
| FR-06        | FR-006  | — |
| FR-07        | FR-007  | — |
| FR-08        | FR-008  | — |
| FR-09        | FR-009 + FR-010 | Split for atomicity (preserve / render-ineligible) |
| FR-10        | FR-011  | Recast as Unwanted Behavior EARS |
| OR-01        | FR-012  | Folded into FR (S1 has no OBS section) |
| OR-02        | FR-013  | Folded |
| OR-03        | FR-014  | Folded |
| OR-04        | FR-015  | Folded |
| OR-05        | FR-016  | Folded |
| OR-06        | FR-017  | Folded |
| OR-07        | FR-018  | Folded |
| OR-08        | FR-019  | Folded |
| AR-01        | FR-020  | Folded into Constraints |
| AR-02        | FR-021  | — |
| AR-03        | FR-022  | — |
| AR-04        | FR-023  | — |
| AR-05        | FR-024  | — |
| AR-06        | FR-025 + FR-026 | Split for atomicity (positive grant / negative denial) |
| GR-01        | FR-027  | — |
| GR-02        | FR-028  | — |
| GR-03        | FR-029  | — |
| GR-04        | FR-030  | — |
| GR-05        | FR-031  | — |
| GR-06        | FR-032  | — |
| GR-07        | FR-033  | — |
| GR-08        | FR-034  | — |
| GR-09        | FR-035  | — |
| NFR-01       | FR-036  | — |
| NFR-02       | FR-037  | Recast as Unwanted Behavior EARS |
| NFR-03       | FR-038  | — |
| NFR-04       | FR-039  | — |
| NFR-05       | FR-040  | — |
| NFR-06       | FR-041  | — |
| NFR-07       | FR-042 + FR-043 | Split for atomicity (atomic-write property / no partial-state visibility) |

- [INFO] Substrate uses RFC 2119 verbs throughout; translated to EARS per drafting rules. Patterns selected: Ubiquitous (most), Event-driven (FR-009, FR-010), Unwanted Behavior (FR-011, FR-026, FR-037, FR-043).
- [INFO] Functional Requirements grouped into four logical areas (Declaration / Concurrency / Termination / Observability) for readability. Constraints grouped into three areas (Access / Governance / Durability and Isolation). Grouping does not break ID continuity.

Outstanding: 0 blocking, 1 warning, 2 info

## Phase 3 — Vocabulary

- [INFO] Substrate carries an explicit Glossary table with 18 entries; copied verbatim with status `substrate`.
- [WARNING] Auto-derived term: `execution outputs` — used in FR-022 (and substrate AR-03) but not defined in the substrate Glossary. Definition synthesized from context. → Operator review required.
- [WARNING] Auto-derived term: `LLM` — referenced in FR-019 (and substrate OR-08) without definition. Standard meaning supplied. → Operator review required.

Outstanding: 0 blocking, 2 warnings, 1 info

## Phase 4 — Taxonomy hygiene

Common checks:

- [INFO] All output IDs use `FR-NNN` format with three-digit zero-padded sequence per `references/conventions.md`.
- [INFO] Sequence is dense FR-001..FR-043 with no gaps; no duplicates within the FR category.
- [INFO] Glossary terms used in requirement text resolve against §Glossary (verified for: operator, agent, unit of work, artifact, input artifact, output artifact, sealed input artifact, lifecycle state, terminal state, in-flight, drafting agent, executing agent, designated audience, governance configuration, machine-verifiable, closure criterion, boundary, role, third-party service, execution outputs, LLM, canonical location).

EARS hygiene checks (T1):

- [INFO] Each FR entry uses a legal EARS pattern (Ubiquitous / Event-driven / Unwanted Behavior).
- [INFO] Each FR entry contains exactly one `SHALL` (or one `SHALL NOT`).
- [INFO] No RFC 2119 modal verbs (`MUST`, `SHOULD`, `MAY`) appear in FR statements.
- [WARNING] FR-022 contains a single `SHALL` but covers two distinct write authorities (`output artifact` and `execution outputs`). Atomicity is borderline — both authorities apply to the same role over assets of the same role's responsibility, so they are treated as a single property. → Consider splitting if downstream design distinguishes these two write paths.

Outstanding: 0 blocking, 1 warning, 5 info

## Phase 5 — Verification

- [INFO] Acceptance criteria derived for all 43 requirements from the `SHALL` action of each EARS statement; no `N/A` entries.
- [INFO] Quality scorecard: all 43 requirements score `✓` on Atomic, Unambiguous, Verifiable, and Traceable. Bounded is `N/A` across the board: S1 has no NFR/OBS/SEC categories, and quantitative thresholds are explicitly excluded by the substrate's "Out of Scope" table. The substrate's non-functional requirements are folded into FR Constraints by S1 design and inherit the `N/A` Bounded score by category rule.
- [WARNING] FR-022 marked `✓` Atomic on the table per rule "exactly one `SHALL` → ✓"; see Phase 4 warning re: borderline atomicity.

Outstanding: 0 blocking, 1 warning, 2 info

## Phase 6 — Format

- [INFO] Format pass applied across all sections per `references/template-s1.md`. Section ordering: Title+Purpose / Scope / Actors / Glossary / Functional Requirements / Constraints / Acceptance Criteria / Quality Criteria scorecard / Version block.
- [INFO] Version block written at bottom of both files. No prior `cod-framework-v04-requirements.md` → initial version `0.1`. Status: `Draft`. Last Updated: `2026-05-06`.

Outstanding: 0 blocking, 0 warnings, 2 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-06 |
| Status       | Draft      |
