# Report — cod-framework-v03

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |    3     |     0      |
| Info     |   23     |    N/A     |

## Phase 0 — Pre-flight

- [INFO] Args parsed: slug=`cod-framework-v03`, type=`generic`, substrate=`./requirements/substrates/framework-requirements.md`
- [INFO] Repo root resolved at `/Users/gilllesmourgues/Workspace/chief-of-droids/skills-lab` (CLAUDE.md present at cwd)
- [INFO] Output directory created: `requirements/cod-framework-v03/`
- [INFO] No prior `cod-framework-v03-requirements.md` — initial pass (Version 0.1)
- [INFO] References loaded: `conventions.md`, `template-s1.md`, `ears.md`, `verification.md`

Outstanding: 0 blocking, 0 warnings, 5 info

## Phase 1 — Framing

- [INFO] Title extracted from substrate H1: "Chief of Droids — Framework Requirements"
- [INFO] Purpose extracted from explicit purpose statement in substrate paragraph 4 ("The framework's evolution purpose is to make the execution contract…")
- [WARNING] In Scope list inferred from substrate's requirement categories — substrate carries no explicit "In Scope" subsection. Treated by enumerating the topics covered by FR/AR/GR/OR/NFR sections. → user verification required.
- [INFO] Out of Scope list extracted verbatim from substrate's "Explicitly out of scope" section. Removed substrate's NFR-06 topic ("runtime dependencies on third-party services") from the out-of-scope list because it is itself a stated requirement (mapped to FR-041) — including it as out of scope would contradict the requirement.
- [INFO] Actors table assembled from substrate Glossary entries for *operator*, *drafting agent*, *executing agent*. Direction values: operator → user; drafting agent → upstream; executing agent → downstream.

Outstanding: 0 blocking, 1 warning, 3 info

## Phase 2 — Drafting

- [INFO] Substrate ID stability scan: substrate IDs use 2-digit format (`FR-01`, `AR-01`, `GR-01`, `OR-01`, `NFR-01`) and prefixes `AR`/`GR`/`OR` are not in the conventions ID-stability regex `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b`. No matches found. All output IDs renumbered fresh per S1 typology starting at `FR-001`.
- [INFO] Substrate categories `AR`, `GR`, `OR`, `NFR` are not S1 sections. Mapped to §6 Constraints (FR-NNN sequence shared with §5) with sub-headings preserving substrate domain grouping (Access / Governance / Observability / Non-functional).
- [INFO] Substrate FR-09 was compound (two SHALLs: preservation + ineligibility). Split into FR-009 (preservation) and FR-010 (ineligibility), both Event-driven EARS keyed off the abort trigger.
- [INFO] Substrate AR-06 was compound (positive read access + negative read access). Split into FR-017 (Ubiquitous, positive) and FR-018 (Unwanted Behavior, negative).
- [INFO] Substrate NFR-07 was compound (atomic-write SHALL + no-partial-state SHALL). Split into FR-042 (Ubiquitous, atomic) and FR-043 (Unwanted Behavior, no-partial-state).
- [INFO] RFC 2119 keyword `MAY` present in substrate AR-01 ("Only the operator MAY initiate…") translated to EARS Ubiquitous with permission framing: "The framework SHALL permit only the operator to…" (FR-012). No other RFC 2119 keywords (`MUST`, `SHOULD`, `MUST NOT`) appeared in substrate requirement statements; substrate already favours `SHALL` and `SHALL NOT`, which are EARS-compliant.
- [INFO] EARS pattern distribution: 35 Ubiquitous; 4 Event-driven (FR-009, FR-010); 4 Unwanted Behavior (FR-011, FR-018, FR-037, FR-043). Tally: 43 entries, all using legal EARS patterns.
- [INFO] Total entries written: 43 (§5 Functional: 11; §6 Constraints — Access: 7; Governance: 9; Observability: 8; Non-functional: 8).

Outstanding: 0 blocking, 0 warnings, 8 info

## Phase 3 — Vocabulary

- [INFO] 21 substrate-defined glossary entries preserved verbatim, status `substrate`. One internal cross-reference updated: substrate glossary entries referenced `GR-05` and `NFR-06`; renumbered to `FR-023` and `FR-041` respectively to track the artifact's own ID space.
- [WARNING] Auto-derived glossary entry: `execution outputs`. Term used in FR-014 (translated from substrate AR-03) and not separately defined in substrate glossary; closest substrate signal is the *artifact* definition's mention of "implementation files". → user verification required.
- [WARNING] Auto-derived glossary entry: `LLM`. Acronym used in FR-035 (substrate OR-08, "LLM token usage") and not defined in substrate glossary. → user verification required.

Outstanding: 0 blocking, 2 warnings, 1 info

## Phase 4 — Taxonomy hygiene

- [INFO] ID format check: all 43 entries match `FR-NNN` (three-digit) ✓
- [INFO] ID sequence dense: `FR-001` through `FR-043` with no gaps ✓
- [INFO] No duplicate IDs within FR category ✓
- [INFO] Glossary coverage: every domain term used in requirements is defined in §Glossary (after auto-derivation of `execution outputs` and `LLM`) ✓
- [INFO] EARS pattern legality: each FR entry uses Ubiquitous, Event-driven, or Unwanted Behavior — all legal patterns from `references/ears.md` ✓
- [INFO] One-`SHALL`-per-entry: each of the 43 entries contains exactly one modal verb (`SHALL` or `SHALL NOT`) ✓
- [INFO] No leakage of RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) into EARS statements ✓
- [INFO] Note on Bounded scoring (Phase 5 pre-signal): S1 collapses NFR-class substrate signals into the FR sequence, so the Bounded criterion (which is keyed by category prefix `NFR`/`OBS`/`SEC`) evaluates to `N/A` for every entry. The substrate's stated quality criterion "Quantified latency, throughput, or cost targets — out of scope" aligns with this outcome.

Outstanding: 0 blocking, 0 warnings, 8 info

## Phase 5 — Verification

- [INFO] Acceptance Criteria derived for all 43 requirements. Per-requirement counts: 22 entries with one AC; 21 entries with two or more ACs. No entry rendered with `N/A` AC.
- [INFO] Quality Criteria scorecard rendered for all 43 entries with the verbatim definitions block from `references/verification.md` followed by the scorecard table.
- [INFO] Scorecard outcome: Atomic ✓ × 43; Unambiguous ✓ × 43; Verifiable ✓ × 43; Traceable ✓ × 43; Bounded N/A × 43. No ✗ scores.

Outstanding: 0 blocking, 0 warnings, 3 info

## Phase 6 — Format

- [INFO] Format pass: §Title + Purpose, §Scope (In/Out), §Actors & Consumers, §Glossary, §Functional Requirements, §Constraints, §Acceptance Criteria, §Quality Criteria scorecard, §Version block — all present and ordered per `template-s1.md`. Files written in order: `cod-framework-v03-requirements.md`, then `cod-framework-v03-report.md`.

Outstanding: 0 blocking, 0 warnings, 1 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-06 |
| Status       | Draft      |
