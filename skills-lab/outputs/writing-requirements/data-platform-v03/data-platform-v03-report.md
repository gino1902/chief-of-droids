# Report — data-platform-v03

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |    18    |     7      |
| Info     |    5     |    N/A     |

## Phase 0 — Pre-flight

- [INFO] Slug `data-platform-v03` valid; banned tokens (`requirement`, `req`, `reqs`) absent.
- [INFO] Substrate `requirements/substrates/data-platform.md` resolved and readable (10.7 KB, `.md`).
- [INFO] CLAUDE.md located at `skills-lab/CLAUDE.md`; repo root resolved to `skills-lab/`.
- [INFO] No prior `data-platform-v03-requirements.md` found in `requirements/data-platform-v03/`; initial version `0.1`. Sibling iterations (`data-platform-v01/`, `data-platform-v02/`) exist under different slugs and do not anchor IDs for this run.
- [INFO] Substrate scanned for declared IDs matching `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b`: zero matches. Substrate uses `F#`, `G#`, `O#`, `NFR#` prefixes — fresh ID assignment applied.

Outstanding: 0 blocking, 0 warnings, 5 info

## Phase 1 — Framing

- [WARNING] Title taken verbatim from substrate H1 ("SQLI – Data Platform Creation"). → Verify the title reflects component scope; substrate also serves a wider system view.
- [WARNING] Purpose paragraph inferred from substrate prose; substrate contains no explicit "purpose" statement. → Verify or replace with author-supplied purpose.
- [WARNING] Out of Scope rendered as `N/A`: substrate provides no explicit out-of-scope signals. Items marked `TBD` (F8, F17, NFR1, NFR2, NFR6, NFR7) are deferred decisions, not exclusions. → Add explicit out-of-scope items if any, especially around adjacent systems (BI tooling, data science workbench, source-system data quality).
- [WARNING] Actors & Consumers describe abstract roles only — substrate does not enumerate specific subsystems, named operator roles, or named business-user roles. → Replace with named actors when known.
- [INFO] Title + Purpose + Scope + Actors rendered.

Outstanding: 0 blocking, 4 warnings, 1 info

## Phase 2 — Drafting

- [WARNING] FR-005 reformulated from substrate F5 (consumer-side phrasing) to a System-side capability obligation. Verify intent.
- [WARNING] FR-010 reformulated from substrate F10 (producer-side phrasing) to a System-side acceptance obligation. Verify intent.
- [WARNING] FR-008 / FR-014 — substrate marks "use cases to be defined in the future"; only the exposure obligation is captured.
- [WARNING] FR-011 / FR-012 split from substrate F11 (compound: retention period + automatic erasure).
- [WARNING] DR sub-section rendered as `N/A`: substrate provides no field-level data model.
- [WARNING] TR sub-section rendered as `N/A`: substrate references transformation existence (F7) but no input → rule → output mapping.
- [WARNING] IR statements describe obligation only; substrate provides no protocol, schema, or format specification.
- [WARNING] NFR-001..NFR-005 carry `Measurement: TBD` per substrate's explicit deferral.
- [WARNING] ERR coverage minimal: substrate defines explicit error paths only for NFR1 (retry) and NFR2 (dead-letter); the majority of FRs have no derived ERR entry. Coverage to be expanded in design phase.
- [WARNING] ERR-003 introduced to mirror SEC-004 (substrate O6) — captures the operational error path of the data-leakage prevention obligation. Verify whether SEC-004 alone is sufficient or whether ERR-003 should remain as an explicit error-handling entry.
- [INFO] All template sections rendered. Drafting categories used: FR×17, IR-IN×4, IR-OUT×4, DR×0 (N/A), TR×0 (N/A), NFR×8, SEC×4, CON×7, ERR×3, OBS×5.

Outstanding: 0 blocking, 10 warnings, 1 info

## Phase 3 — Vocabulary

- [WARNING] 13 glossary entries auto-derived from substrate usage (terms used in requirements but not defined in the substrate glossary): Authorised operator, Authorised subsystem, Authorised external end-user, Producing subsystem, Consuming subsystem, Source subsystem, Business-ready data, Business workflow, Unit & Department, SQLI data retention policy, SQLI data security policy, SQLI data access policy, SQLI user access policy, SQLI data classification policy, SQLI audit policy. → All marked `auto-derived — verify`; user review required.
- [INFO] 39 substrate glossary entries carried through unchanged with status `substrate`.

Outstanding: 0 blocking, 1 warning (multi-entry), 1 info

## Phase 4 — Taxonomy hygiene

Common checks:

- [INFO] ID format `<CAT>-NNN` valid for all entries across categories: FR, CON, IR-IN, IR-OUT, NFR, SEC, ERR, OBS.
- [INFO] ID sequence dense per category (no gaps) — no prior pass deleted IDs, so no vacated slots expected.
- [INFO] No duplicate IDs within any category.
- [WARNING] Glossary coverage: all domain-specific terms used in requirements are present in §Glossary, but 13 entries are flagged `auto-derived — verify` (see Phase 3) and require author confirmation before they count as fully resolved.

T1 (EARS) checks — apply to FR, CON, ERR:

- [INFO] Each FR and CON entry uses a legal EARS pattern (Ubiquitous, Event-driven, or State-driven).
- [INFO] Each ERR entry uses Unwanted Behavior EARS exclusively.
- [INFO] Each ERR entry contains a cross-link to an existing FR (`→ FR-003` ×2, `→ FR-016` ×1).
- [INFO] Each FR and CON entry contains exactly one `SHALL`.
- [INFO] RFC 2119 keywords absent from EARS statements.

T2 (RFC 2119) checks — apply to IR, NFR, SEC, OBS:

- [INFO] Each IR, NFR, SEC, OBS entry contains at least one RFC 2119 keyword (`MUST`/`SHOULD`).
- [INFO] Each NFR entry contains a Measurement field.
- [WARNING] NFR-001..NFR-005 Measurement field is `TBD` (substrate-deferred). Bounded score is ✗ for those entries; see §Quality Criteria scorecard.
- [INFO] EARS `SHALL` does not appear in pure RFC 2119 IR/NFR/OBS statements. (Event-driven EARS forms appear in IR-IN-002 and IR-IN-004 — explicitly allowed by template.)
- [INFO] IR-IN and IR-OUT sub-sections both rendered (4 entries each).
- [INFO] SEC-004 uses Unwanted Behavior EARS form — explicitly allowed for threat-mitigation security entries.

T3/T4 (Table-form) checks — apply to DR, TR:

- [INFO] DR sub-section rendered as `N/A` (no substrate signal); column rules not applicable.
- [INFO] TR sub-section rendered as `N/A` (no substrate signal); column rules not applicable.

Outstanding: 0 blocking, 2 warnings, 13 info

## Phase 5 — Verification

- [INFO] Acceptance Criteria derived for all 48 non-N/A requirement entries (17 FR + 8 IR + 8 NFR + 4 SEC + 7 CON + 3 ERR + 5 OBS).
- [WARNING] FR-008 and FR-014 carry a secondary `AC: N/A` marker for downstream use-case completeness — substrate defers use-case enumeration.
- [WARNING] NFR-001..NFR-005 ACs note `Quantitative thresholds: TBD` mirroring the deferred Measurement.
- [INFO] Quality Criteria scorecard: Atomic, Unambiguous, Verifiable, Traceable scored ✓ for all 50 entries.
- [WARNING] Bounded ✗ on NFR-001, NFR-002, NFR-003, NFR-004, NFR-005 — unbounded NFR (no quantitative threshold). Bounded ✓ on NFR-006, NFR-007, NFR-008.

Outstanding: 0 blocking, 3 warnings, 2 info

## Phase 6 — Format

- [INFO] Format pass applied: section ordering matches template-s2 (Title+Purpose, Scope, Actors, Glossary, FR, IR, DR, NFR, SEC, CON, ERR, OBS, AC, QC, Version block).
- [INFO] Initial version block written: `0.1`, Status `Draft`, Last Updated `2026-05-07`.
- [INFO] Both files written under `requirements/data-platform-v03/`.

Outstanding: 0 blocking, 0 warnings, 3 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-07 |
| Status       | Draft      |
