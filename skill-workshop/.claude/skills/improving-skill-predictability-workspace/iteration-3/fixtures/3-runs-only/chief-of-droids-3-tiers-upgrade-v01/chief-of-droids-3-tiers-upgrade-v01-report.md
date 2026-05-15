# Report — chief-of-droids-3-tiers-upgrade-v01

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |    37    |     5      |
| Info     |    8     |    N/A     |

## Phase 0 — Pre-flight

- [INFO] Slug `chief-of-droids-3-tiers-upgrade-v01` validated against `^[a-z0-9-]+$` and confirmed not to contain `requirement`, `req`, or `reqs`.
- [INFO] `--type technical` accepted; loading `template-s2.md`, `ears.md`, `rfc2119.md`, `tables.md`, `verification.md`.
- [INFO] Repo root resolved by walking from cwd; first `CLAUDE.md` found at `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/CLAUDE.md`. Repo root = `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop`.
- [INFO] Output dir `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/requirements/chief-of-droids-3-tiers-upgrade-v01/` did not exist; created.
- [INFO] No prior `chief-of-droids-3-tiers-upgrade-v01-requirements.md` found; initial version `0.1` assigned; no ID-stability scan needed.
- [INFO] Substrate `./requirements/substrates/two-tier-architecture-design-notes.md` read; `.md` extension confirmed.

Outstanding: 0 blocking, 0 warnings, 6 info

## Phase 1 — Framing

- [INFO] Title resolved to first H1 of substrate: `Two-Tier CLAUDE.md Architecture — Design Notes`. Note: H1 says "Two-Tier" while slug says "3-tiers"; substrate body resolves this — design uses two tiers (workspace + project, with Layer 1 as a dispatcher carried by Project Instructions) realised across three layers. Title kept verbatim per skill rule. The slug carries the user-chosen iteration name and is not derived from the title.
- [WARNING] Substrate H1 contains `— Design Notes`, indicating the source is design notes rather than committed spec (substrate line 9 confirms: "Status: design notes, not committed spec"). Requirements derived under this status are inherently provisional. → User verification: confirm scope of derivation matches intended use.
- [INFO] Purpose extracted from substrate sentence "This document proposes a two-tier architecture that resolves both" (line 7); expanded with surrounding context to produce a single-paragraph purpose statement.
- [WARNING] §Scope In Scope items derived from positive signals across substrate sections (Architecture, Bootstrap protocol, Sentinel schema, Skills routing, Preconditions, Reliability principle). User verification required: confirm in-scope list matches intended deployable component boundary.
- [WARNING] §Scope Out of Scope items derived from the "Open items" section and explicit deferrals ("parked", "deferred", "undecided"). User verification required: confirm out-of-scope list is exhaustive.
- [WARNING] §Actors & Consumers entries derived from substrate references; no explicit actors block exists in substrate. User verification required.

Outstanding: 0 blocking, 4 warnings, 2 info

## Phase 2 — Drafting

- [INFO] No substrate-declared `<CAT>-NNN` IDs found in scan; canonical-ordering walk applied per `conventions.md` § "Canonical ordering for un-IDed substrate". All IDs assigned fresh.
- [INFO] FR sequence ordered by substrate-byte position of the SHALL-action sentence (translated from substrate imperative form). CON sequence likewise.
- [INFO] ERR coverage drafted in Phase 2 (not deferred to Phase 4). Mandatory-coverage shapes paired with ERR-NNN entries; opt-out rationales attached inline for Emit/Select/rejection-shape FRs.

### Functional Requirements

- [WARNING] FR-004 contains the compound "verify ... and halt with a clear error" — two SHALL-actions in one statement. Flagged as compound; suggested split: separate verify FR and separate halt-on-failure ERR. Retained as single statement for substrate fidelity (substrate also collapses both in one sentence at line 68).
- [WARNING] FR-006 Emit-shape SHALL action; opted out of ERR pairing with inline rationale.
- [WARNING] FR-009 pass-through; opted out of ERR pairing with inline rationale.
- [WARNING] FR-012 rejection-shape; FR is itself the error path; opted out of ERR pairing with inline rationale.
- [WARNING] FR-013 Select-shape; opted out of ERR pairing with inline rationale.
- [WARNING] FR-015 rejection-shape; opted out of ERR pairing with inline rationale.

### Interface Requirements

- [INFO] IR-IN-001..004 and IR-OUT-001..004 derived from substrate bootstrap protocol, sentinel schema, and anchor-emission signals.
- [WARNING] IR-IN-002 specifies "free-form" project-name response — substrate does not define a project-name format. User verification: define valid project-selector vocabulary.

### Data Requirements

- [INFO] DR-001 entity "Sentinel record" derived from substrate § "Sentinel schema" (lines 78–90); all seven fields preserved with substrate-named types and constraints.

### Transformation Requirements

- [INFO] TR-001 (sentinel path derivation) derived from substrate filename pattern `chief-of-droids/.sessions/<urlencoded-uri>.json` (line 80); URL-encoding rule inferred from the `<urlencoded-uri>` placeholder.
- [WARNING] TR-002 (SHA computation) does not specify the digest algorithm (SHA-1, SHA-256, etc.) — substrate uses bare "SHA". User verification: pin the digest algorithm.

### Non-Functional Requirements

- [INFO] NFR-001 (Reliability) mapped to substrate signal "Reliability estimate: ~92–93%" per canonical mapping table.
- [WARNING] NFR-002 (Performance) rendered as `N/A` — substrate silent on performance threshold. Universal slot per template-s2; cannot be omitted.
- [WARNING] NFR-003 (Resource/footprint) Measurement is `TBD` — substrate uses adjective "minimal" without numeric threshold. Phase 4 unbounded-NFR check applies.
- [WARNING] NFR-001 uses ≥ 92% from the lower bound of substrate range 92–93%; lower bound chosen to be the most permissive interpretation. User verification: confirm threshold.

### Security

- [WARNING] §Security rendered as `N/A` — substrate addresses none of the six derivability categories (authentication, authorization, encryption, audit logging, rate limiting, input validation) explicitly. Governance signals ("PR-to-workspace", "hard reject", "blocked while referenced") classified as CON per the SEC exclusion list. No `SEC-NNN` IDs allocated per the empty-section rule. User verification: confirm no security obligations are intended.

### Constraints

- [WARNING] CON-007 contains two SHALL clauses (`<project>/CLAUDE.md` SHALL carry ... ; `<project>/brief.md` SHALL carry ...) for substrate fidelity. Atomic check ✗. Suggested split: CON-007a and CON-007b.
- [WARNING] CON-008 contains two SHALL clauses (workspace tier SHALL win ... and project-tier change SHALL be rejected). Atomic check ✗. Suggested split.
- [WARNING] CON-012 contains a SHALL + SHALL NOT clause pair (one-way composition + workspace SHALL NOT reference project). Atomic check ✗. Suggested split.
- [INFO] CON-014 (reliability principle) derived from substrate § "Reliability principle" lines 100–104; rendered as CON because it constrains framework-level resource allocation rather than describing a runtime event.

### Error Handling

- [INFO] ERR-001, ERR-002, ERR-003, ERR-004, ERR-005, ERR-007, ERR-008, ERR-010, ERR-011, ERR-014, ERR-016 drafted in Phase 2 paired with their mandatory-coverage FRs (Acquire / Mutate / Validate / Solicit / Transform-with-external-inputs shapes).
- [INFO] ERR sequence contains gaps at 006, 009, 012, 013, 015 — paired FRs opt out of ERR coverage. Gaps are permitted per `conventions.md` § "ID convention".

### Observability

- [WARNING] §Observability rendered as `N/A` — substrate addresses none of the five derivability categories (metrics, structured logs, traces, health endpoint, alert threshold) explicitly. The anchor confirmation is scoped to §IR-OUT; SHA fingerprints in the sentinel are scoped to §DR; user-channel error messages are scoped to §ERR per the OBS exclusion list. No `OBS-NNN` IDs allocated. User verification: confirm no observability obligations are intended.

Outstanding: 0 blocking, 16 warnings, 6 info

## Phase 3 — Vocabulary

- [WARNING] Glossary entries auto-derived; user review required.
- [INFO] Acronym rule extracted: `SHA`, `MCP`, `URI`. Acronyms `JSON`, `URL`, `ID` excluded via stop-word list.
- [INFO] Backtick rule extracted: `recent_chats[0].uri`, `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, `chief-of-droids/<project>/brief.md`, `chief-of-droids/.sessions/<urlencoded-uri>.json`, `workspace_md_sha`, `project_md_sha`, `brief_sha`, `resolved_skills`, `creating-skills`.
- [INFO] Capitalized-noun-phrase rule extracted: Project Instructions, Bootstrap Protocol, Sentinel, Layer 1, Layer 2, Layer 3, Workspace Tier, Project Tier, Resolution Map, Project Brief, Always-On Tool, Promotion, Trigger Collision, Negative Trigger, Composition, Anchor, Session Bind, Reliability Principle, Dispatcher.
- [INFO] Explicit-substrate-definition rule extracted: none in `"X is defined as"` form. The sentinel schema (substrate lines 78–90) is a typed schema, scoped to §DR rather than to §Glossary.
- [WARNING] Glossary contains 27 entries; all marked `auto-derived — verify`. No `substrate` status entries (no explicit definitions in source).

Outstanding: 0 blocking, 2 warnings, 4 info

## Phase 4 — Taxonomy hygiene

### Common checks

- [INFO] All requirement IDs match `<CAT>-NNN` format with valid category prefixes.
- [INFO] Sequences are dense within FR (001–016), IR-IN (001–004), IR-OUT (001–004), DR (001), TR (001–002), NFR (001–003), CON (001–014). ERR sequence contains intentional gaps (006, 009, 012, 013, 015) per opt-out rationale.
- [INFO] No duplicate IDs detected within any category.
- [WARNING] Glossary check: terms appearing in requirements that may not be universally understood — "fail-fast", "Acquire-shape", "Select-shape" — these appear only in `references/ears.md` and report prose, not in the artifact requirement statements. No artifact-text gap detected.

### T1 (EARS) checks

- [WARNING] FR-004 compound (two SHALL clauses); flagged.
- [WARNING] CON-007, CON-008, CON-012 compound; flagged.
- [INFO] All FR/CON entries use legal EARS patterns (Ubiquitous, Event-driven, Unwanted Behavior).
- [INFO] All ERR entries use Unwanted Behavior EARS exclusively.
- [INFO] All ERR entries contain a `→ FR-NNN` cross-link to an existing FR.
- [INFO] No RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) detected inside EARS statements.
- [INFO] FR vs CON binary-decision test applied; no misclassifications detected. Cases that triggered tie-breakers: CON-001 / CON-002 / CON-003 / CON-004 / CON-006 (tie-breaker row 2 — placement / routing); CON-009 / CON-011 / CON-012 / CON-013 (tie-breaker row 3 — invariant without event); CON-005 (tie-breaker row 3); CON-008 (tie-breaker row 3); CON-010 / CON-014 (tie-breaker row 3).
- [INFO] ERR coverage protocol applied during Phase 2. All Acquire/Mutate/Validate/Solicit/Transform-with-external-inputs FRs are either ERR-paired or carry an inline opt-out rationale.
- [INFO] ERR text contains no implementation-mechanism naming (file/network/MCP/database) at the contract level; mechanism names (filesystem, JSON, SHA) appear only in IR-IN, IR-OUT, and DR contexts where mechanism specification is part of the contract.

### T2 (RFC 2119) checks

- [INFO] IR-IN, IR-OUT, NFR, OBS entries contain RFC 2119 keywords (MUST/SHOULD); none mix EARS `SHALL` with RFC 2119 keywords.
- [WARNING] NFR-002 Measurement absent (rendered as N/A); flagged per universal-slot rule.
- [WARNING] NFR-003 Measurement is `TBD` (no numeric value); unbounded-NFR check fires.
- [INFO] NFR-001 (Reliability/correctness) and NFR-002 (Performance) both rendered, satisfying mandatory-slot rule for `--type technical`.
- [INFO] NFR slot assignment follows the canonical substrate-signal → NFR-slot mapping: reliability/92% → NFR-001, performance (silent) → NFR-002, "minimal" footprint → NFR-003.
- [INFO] §Security N/A — no `SEC-NNN` numeric IDs allocated; section heading carries the N/A statement.
- [INFO] §Observability N/A — no `OBS-NNN` numeric IDs allocated; section heading carries the N/A statement.

### T3/T4 (table-form) checks

- [INFO] DR-001 table includes all four columns: Field, Type, Constraints, Notes.
- [INFO] TR-001 and TR-002 tables include all three columns: Input, Rule, Output.
- [INFO] DR-001 entity has seven typed field rows with Constraints column entries — passes the "≥ 2 field rows with typed Constraints" qualification.
- [INFO] TR-001 matches "encoding/decoding rule" candidate; TR-002 matches "hash/digest/fingerprint computation declaration" candidate.

Outstanding: 0 blocking, 6 warnings, 13 info

## Phase 5 — Verification

- [INFO] Acceptance criteria derived per `verification.md` rules — one or more AC per requirement.
- [INFO] NFR-002 and NFR-003 ACs rendered as `N/A — no verifiable condition derivable from substrate` per `verification.md` Warning rule.
- [INFO] Quality scorecard contains a row per requirement; criteria scored per `verification.md` rules.
- [WARNING] Atomic ✗ on FR-004, CON-007, CON-008, CON-012 — compound statements (see Phase 4).
- [WARNING] Verifiable ✗ on NFR-002, NFR-003 — no derivable AC (substrate silent or Measurement TBD).
- [WARNING] Bounded ✗ on NFR-002, NFR-003 — no quantitative signal; NFR-002 silent, NFR-003 measurement TBD.

Outstanding: 0 blocking, 4 warnings, 3 info

## Phase 6 — Format

- [INFO] Format pass applied across all 15 sections per `template-s2.md`.
- [INFO] Version block appended; initial version `0.1`; status `Draft`; last updated `2026-05-15`.
- [INFO] Both files written to `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/requirements/chief-of-droids-3-tiers-upgrade-v01/`.

Outstanding: 0 blocking, 0 warnings, 3 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
