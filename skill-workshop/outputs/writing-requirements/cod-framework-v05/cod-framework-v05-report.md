# Report — cod-framework-v05

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |    4     |     2      |
| Info     |    5     |    N/A     |

## Phase 0 — Pre-flight

- [INFO] Slug `cod-framework-v05` validated against `^[a-z0-9-]+$`; no banned tokens.
- [INFO] Type resolved to `generic` → S1 template loaded.
- [INFO] Substrate resolved at `requirements/substrates/framework-requirements.md`; `.md` extension confirmed.
- [INFO] Repo root resolved at `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop` (cwd `CLAUDE.md` present).
- [INFO] No prior `cod-framework-v05-requirements.md` at output path; treated as initial pass (version `0.1`).

Outstanding: 0 blocking, 0 warnings, 5 info

## Phase 1 — Framing

- Title source: substrate H1 `Chief of Droids — Framework Requirements`; rendered as `Chief of Droids — Framework` (the `Requirements` tail is metadata of the substrate, not part of the component name).
- Purpose: synthesised from the substrate's three lead paragraphs and the explicit "evolution purpose" sentence; no inference outside substrate prose.
- Scope `In Scope`: extracted from substrate's substantive coverage across FR/AR/GR/OR/NFR sections.
- Scope `Out of Scope`: extracted verbatim-equivalent from substrate's "Explicitly out of scope" section; FR-042 cross-reference inserted in place of the original NFR-06 reference (renumbered per S1).
- Actors: extracted from glossary entries (operator, drafting agent, executing agent) and from substrate text (governance configuration, operator's host environment); abstract per substrate's design-independence quality criterion.

Outstanding: 0 blocking, 0 warnings, 0 info

## Phase 2 — Drafting

- ID stability: substrate uses two-digit IDs (`FR-01`, `AR-01`, `GR-01`, `OR-01`, `NFR-01`) which do not match the skill's three-digit declared-ID regex `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b`. No IDs preserved; full renumbering under the S1 `FR-NNN` sequence per `references/conventions.md`. Substrate-to-output mapping below.
- Template: S1 (generic). Sections §5 Functional Requirements and §6 Constraints both share the `FR-NNN` sequence per template rule.
- Partition rationale: substrate FR + OR (observability behaviours) + GR-09 (verify-on-seal/delivery) → §5 Functional Requirements; substrate AR (access policies) + GR-01..08 (governance/structural) + NFR (non-functional properties) → §6 Constraints.
- EARS conversion: substrate's RFC 2119 `SHALL` translated to EARS patterns: Ubiquitous (default), Event-driven (`WHEN`) for transition responses, State-driven (`WHILE`) for in-state invariants, Unwanted Behavior (`IF…THEN`) for guards and refusals.
- Compound-requirement splits:
  - Substrate FR-09 (preserve + render-ineligible on abort) → output FR-009 + FR-010.
  - Substrate NFR-07 (atomic write + no partial-state observation) → output FR-043 + FR-044.
- [INFO] Substrate FR-09 originally read as one `SHALL` statement coordinating two distinct properties; split per atomic-requirement rule.

**Substrate-to-output ID mapping:**

| Substrate | Output | Notes |
|:--|:--|:--|
| FR-01 | FR-001 | Ubiquitous |
| FR-02 | FR-002 | Ubiquitous |
| FR-03 | FR-003 | Ubiquitous |
| FR-04 | FR-004 | Ubiquitous |
| FR-05 | FR-005 | Ubiquitous |
| FR-06 | FR-006 | Refactored to Unwanted Behavior (`IF … THEN`) for clearer testability |
| FR-07 | FR-007 | Ubiquitous |
| FR-08 | FR-008 | Ubiquitous |
| FR-09 | FR-009 + FR-010 | Split: preserve / render ineligible |
| FR-10 | FR-011 | Refactored to Unwanted Behavior |
| OR-01 | FR-012 | |
| OR-02 | FR-013 | |
| OR-03 | FR-014 | |
| OR-04 | FR-015 | |
| OR-05 | FR-016 | |
| OR-06 | FR-017 | |
| OR-07 | FR-018 | |
| OR-08 | FR-019 | |
| GR-09 | FR-020 + FR-021 | Split: seal-time check / delivery-time check (substrate compound) |
| AR-01 | FR-022 | |
| AR-02 | FR-023 | |
| AR-03 | FR-024 | |
| AR-04 | FR-025 | |
| AR-05 | FR-026 | |
| AR-06 | FR-027 + FR-028 | Split: granted reads / denied reads (substrate compound) |
| GR-01 | FR-029 | |
| GR-02 | FR-030 | State-driven |
| GR-03 | FR-031 | |
| GR-04 | FR-032 | |
| GR-05 | FR-033 | Event-driven |
| GR-06 | FR-034 | |
| GR-07 | FR-035 | |
| GR-08 | FR-036 | |
| NFR-01 | FR-037 | |
| NFR-02 | FR-038 | Unwanted Behavior |
| NFR-03 | FR-039 | |
| NFR-04 | FR-040 | |
| NFR-05 | FR-041 | Event-driven |
| NFR-06 | FR-042 | |
| NFR-07 | FR-043 + FR-044 | Split: atomic write / no partial observation |

Outstanding: 0 blocking, 0 warnings, 1 info

## Phase 3 — Vocabulary

- Substrate provided a comprehensive glossary; 21 entries imported with status `substrate`.
- Cross-reference repaired: substrate glossary entry `closure criterion` referenced GR-05 and `third-party service` referenced NFR-06; rewritten to FR-033 and FR-042 respectively to match output IDs.
- One auto-derived addition: `session` — used in FR-004, FR-012, FR-013, FR-032 but not formally defined in the substrate (substrate's `agent` entry mentions "single session" without defining the term). Status `auto-derived — verify`.
- [WARNING] Glossary entry `session` is auto-derived; user verification required.

Outstanding: 0 blocking, 1 warning, 0 info

## Phase 4 — Taxonomy hygiene

- ID format: all 44 entries match `FR-NNN` with three-digit zero padding. ✓
- Sequence density: `FR-001` through `FR-044`, dense, no gaps. ✓
- Duplicates within `FR` category: none. ✓
- EARS pattern legality (per `references/ears.md`): every entry uses Ubiquitous, Event-driven, State-driven, or Unwanted Behavior. ✓
- One `SHALL` per entry: confirmed for every entry after the substrate splits noted in Phase 2. ✓
- RFC 2119 keyword leak into EARS statements: none. ✓
- Glossary coverage of requirement vocabulary:
  - [WARNING] Term `LLM token usage` (FR-019) is not in §Glossary; commonly understood, but consider defining for precision.
  - [WARNING] Term `wall-clock execution time` (FR-019) is not in §Glossary; same note.
  - [WARNING] Term `governance configuration` is in §Glossary; FR-031 paraphrases its components ("policies, skills, instructions, surface specifications") rather than using the defined term — preserved verbatim from substrate for traceability, but consider replacing with `governance configuration` in a future iteration for tighter cohesion.

Outstanding: 0 blocking, 3 warnings, 0 info

## Phase 5 — Verification

- AC derivation: every requirement received at least one acceptance criterion derived from its `SHALL` action per `references/verification.md` rules; no `N/A` entries.
- Quality scorecard: 44 rows; all five criteria evaluated per requirement.
  - Atomic: ✓ for all 44 (single `SHALL` confirmed).
  - Unambiguous: ✓ for all 44 (terms either in §Glossary or universally understood; the warnings in Phase 4 are flagged for tightening but do not invalidate the entries).
  - Verifiable: ✓ for all 44 (each has at least one non-`N/A` AC).
  - Traceable: ✓ for all 44 (`FR-NNN` format, valid prefix, unique).
  - Bounded: `N/A` for all 44 (S1 generic template treats all entries as FR/CON; Bounded applies only to NFR-class. The substrate's NFR entries, after consolidation under the S1 template, are rendered as FR-NNN constraints and therefore are scored `N/A` for Bounded per the verification reference. If quantitative thresholds are added later, retype to a technical pass.)
- [INFO] FR-019 (resource consumption: LLM tokens, wall-clock time) is the closest candidate for a Bounded threshold (e.g. minimum sampling resolution); none specified by substrate. Consider adding measurement granularity in a future technical pass.

Outstanding: 0 blocking, 0 warnings, 1 info

## Phase 6 — Format

- Both files formatted per template; version block appended.
- Write order: requirements file first (`cod-framework-v05-requirements.md`), then this report.
- No prior `cod-framework-v05-requirements.md` detected → initial version `0.1`.

Outstanding: 0 blocking, 0 warnings, 0 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-06 |
| Status       | Draft      |
