# Report — cod-framework-v01

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |    1     |     6      |
| Info     |    9     |    N/A     |

## Phase 0 — Pre-flight

- [INFO] Substrate located: `requirements/substrates/framework-requirements.md` (13.2 KB).
- [INFO] Repo root resolved: `/Users/gilllesmourgues/Workspace/chief-of-droids/skills-lab` (CLAUDE.md found in cwd).
- [INFO] Output directory `requirements/cod-framework-v01/` did not exist; created.
- [INFO] No prior `cod-framework-v01-requirements.md`; initial version `0.1`.

Outstanding: 0 blocking, 0 warnings, 4 info

## Phase 1 — Framing

- [INFO] Title derived from substrate H1 ("Chief of Droids — Framework Requirements"); rendered as `Chief of Droids Framework` (component name).
- [INFO] Purpose extracted from substrate's leading three paragraphs; tooling-specific phrasing (Claude Desktop, Claude Code, MCP, routing layer) trimmed to keep the artifact design-independent.
- [WARNING] §Scope — In Scope signal absent. Substrate contains no positive trigger ("in scope", "covers", "handles", "responsible for") at the framing level; per skill convention, In Scope rendered as `N/A`. Substrate's framing prose and FR list implicitly describe scope — consider adding an explicit "In scope" subsection to the substrate. → User adds an explicit In Scope subsection to substrate, then re-runs.
- [INFO] §Scope — Out of Scope extracted directly from substrate's "Explicitly out of scope" table (six entries).
- [INFO] §Actors derived from substrate Glossary (operator, drafting agent, executing agent). Direction values: `user`, `upstream`, `downstream`.

Outstanding: 0 blocking, 1 warning, 3 info

## Phase 2 — Drafting

- [WARNING] Substrate ID format mismatch. Substrate uses two-digit IDs (`FR-01`, `AR-01`, `GR-01`, `OR-01`, `NFR-01`); the ID-stability regex requires three-digit zero-padded IDs (`FR-\d{3}`). No substrate ID was preserved verbatim; output IDs assigned fresh from `FR-001`. Substrate-to-output ID mapping:
  | Substrate | Output    |
  |:----------|:----------|
  | FR-01..08 | FR-001..008 |
  | FR-09     | FR-009 + FR-010 (split) |
  | FR-10     | FR-011 |
  | AR-01..05 | FR-012..016 |
  | AR-06     | FR-017 + FR-018 (split) |
  | GR-01..08 | FR-019..026 |
  | GR-09     | FR-027 + FR-028 (split) |
  | OR-01..08 | FR-029..036 |
  | NFR-01..06 | FR-037..042 |
  | NFR-07    | FR-043 + FR-044 (split) |
  → User adopts three-digit IDs in substrate to enable ID stability across iterations.
- [WARNING] Substrate categories `AR` (Access), `GR` (Governance), `OR` (Observability), `NFR` (Non-functional) collapsed into the S1 `Constraints` section under the shared `FR-NNN` namespace. The S1 generic template provides only Functional + Constraints; categorical structure is preserved as sub-headings within Constraints (Access controls, Governance, Observability, Operational properties) but the ID prefix no longer carries category. → If category-stable IDs (`SEC-NNN`, `OBS-NNN`, `NFR-NNN`) are required, re-run with `--type technical`.
- [INFO] Four substrate entries were compound (multiple SHALLs or multiple distinct properties) and were split on output for atomicity:
  | Substrate | Reason | Output |
  |:--|:--|:--|
  | FR-09 | Two SHALLs (preserve + render-ineligible) | FR-009, FR-010 |
  | AR-06 | "SHALL have read … SHALL NOT have read" | FR-017, FR-018 |
  | GR-09 | Two trigger events (sealed, delivered) | FR-027, FR-028 |
  | NFR-07 | Two SHALLs (atomicity + no-partial-read) | FR-043, FR-044 |
- [INFO] Four substrate statements rephrased to make the framework the grammatical subject (consistent with FR-drafting rule "behaviors of the subject component itself"): AR-02, AR-03, AR-04, AR-05, OR-04 ("attribute every write" rather than "every write SHALL be attributable").
- [INFO] Three statements translated from Ubiquitous to a more specific EARS pattern where a trigger or condition was implicit in substrate phrasing:
  | Output | Substrate phrase | Pattern |
  |:--|:--|:--|
  | FR-009, FR-010 | "On abort of a unit of work …" | Event-driven (WHEN) |
  | FR-011 | "SHALL NOT permit … before sealed" | Unwanted Behavior (IF/THEN) |
  | FR-018 | "SHALL NOT have read access …" | Unwanted Behavior (IF/THEN) |
  | FR-023 | "at the time the input artifact is sealed" | Event-driven (WHEN) |
  | FR-027, FR-028 | "at the time the artifact is sealed / delivered" | Event-driven (WHEN) |
  | FR-038 | "A failure during the execution …" | Unwanted Behavior (IF/THEN) |
  | FR-041 | "Re-execution … given the same sealed input artifact" | Event-driven (WHEN) |
  | FR-044 | "in the middle of being written" | Unwanted Behavior (IF/THEN) |
- [INFO] Substrate's parenthetical clarifications retained where they bound semantics (FR-036 LLM tokens + wall-clock; FR-040 additive-extension definition).

Outstanding: 0 blocking, 2 warnings, 3 info

## Phase 3 — Vocabulary

- [INFO] Substrate Glossary (19 entries) preserved verbatim with `Status: substrate`.
- [WARNING] One auto-derived term added: `execution outputs` (used in FR-014, distinct from `output artifact`; not formally defined in substrate). Rendered with `Status: auto-derived — verify`. → User confirms or refines the definition; if rejected, remove from glossary and rephrase FR-014.

Outstanding: 0 blocking, 1 warning, 1 info

## Phase 4 — Taxonomy hygiene

- [INFO] ID format check: all 44 output IDs match `FR-\d{3}`.
- [INFO] ID sequence dense across `FR-001` to `FR-044`; no gaps.
- [INFO] No duplicate IDs.
- [INFO] EARS pattern legality: all 44 statements use a legal EARS pattern (Ubiquitous: 33; Event-driven: 7; Unwanted Behavior: 4; State-driven: 0; Optional Feature: 0).
- [INFO] Single-modal check: every output statement contains exactly one `SHALL` (or `SHALL NOT`); no compound entries remain.
- [INFO] RFC 2119 keyword bleed: no `MUST`, `SHOULD`, or `MAY` in any output requirement statement.
- [INFO] Glossary coverage of requirement terms: all domain-specific terms used in requirement statements appear in §Glossary after the addition of `execution outputs`.

Outstanding: 0 blocking, 0 warnings, 7 info

## Phase 5 — Verification

- [INFO] Acceptance criteria derived for all 44 requirements (1–2 AC per entry); no `N/A` AC.
- [INFO] Quality scorecard: Atomic ✓ (44/44), Unambiguous ✓ (44/44), Verifiable ✓ (44/44), Traceable ✓ (44/44), Bounded `N/A` (44/44).
- [WARNING] Bounded check is `N/A` for every requirement because the S1 generic template uses the `FR-NNN` prefix uniformly. Substrate entries that are semantically NFR-class (`NFR-01..07`, `OR-01..08`) are not evaluated for quantitative thresholds in this skeleton. The substrate explicitly excludes "quantified latency, throughput, or cost targets" — so the gap is intentional at this stage. → If quantitative thresholds become in-scope, re-run with `--type technical` to obtain `NFR-NNN` / `OBS-NNN` IDs and a non-N/A Bounded check.
- [WARNING] Substrate's own quality criteria (Non-ambiguous, Complete, Design-independent, Atomic, C4-friendly) differ from the standardized scorecard (Atomic, Unambiguous, Verifiable, Traceable, Bounded). The substrate's `Complete`, `Design-independent`, and `C4-friendly` dimensions are not evaluated in §QC. → User reviews whether the standardized criteria are sufficient or whether additional dimensions need separate review.
- [WARNING] Substrate type signal vs invocation. The substrate carries 7 NFRs, 8 observability requirements, and 6 access requirements — characteristic of a technical-typology specification. Skill was invoked with `--type generic`, which collapses these into FR-NNN constraints and skips Bounded scoring. → If a richer requirements artifact is wanted (separate `NFR`, `OBS`, `SEC`, `IR-IN`, `IR-OUT`, `DR`, `TR` sections with category-stable IDs), re-run with `--type technical`.

Outstanding: 0 blocking, 3 warnings, 2 info

## Phase 6 — Format

- [INFO] Format pass applied across all sections per S1 template; sub-headings introduced under §Constraints because the section contains 33 entries (more than 5).
- [INFO] Version block: initial version `0.1`; status `Draft`; last updated `2026-05-06`.

Outstanding: 0 blocking, 0 warnings, 2 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-06 |
| Status       | Draft      |
