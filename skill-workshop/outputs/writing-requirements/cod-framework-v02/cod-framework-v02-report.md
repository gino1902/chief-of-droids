# Report — cod-framework-v02

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |    8     |     5      |
| Info     |    7     |    N/A     |

## Phase 0 — Pre-flight

- [INFO] Args parsed: slug `cod-framework-v02`, substrate `./requirements/substrates/framework-requirements.md`, type `generic`.
- [INFO] Slug validated against `^[a-z0-9-]+$`; no forbidden tokens (`requirement`, `req`, `reqs`).
- [INFO] CLAUDE.md found at cwd `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/`; repo root resolved.
- [INFO] Output directory `requirements/cod-framework-v02/` created.
- [INFO] No prior `cod-framework-v02-requirements.md` found; initial version `0.1`.
- [INFO] Substrate read: 131 lines, valid `.md`.
- [INFO] Reference files loaded: `conventions.md`, `template-s1.md`, `ears.md`, `verification.md`.

Outstanding: 0 blocking, 0 warnings, 7 info

## Phase 1 — Framing

- [WARNING] Title derived from substrate H1 `Chief of Droids — Framework Requirements`; rendered as component name `Chief of Droids Framework` to match S1 `# <component name>` form. → Verify component-name choice.
- [WARNING] Substrate has no explicit `## Scope > ### In Scope` section. In-Scope items inferred from substrate categories (Functional, Access, Governance, Observability) and framing prose. → Confirm or replace inferred items.
- [INFO] Out-of-Scope items lifted verbatim from substrate's `## Explicitly out of scope` table; reason-for-exclusion column dropped per S1 list format.
- [INFO] Actors table populated from operator/agent roles defined in substrate Glossary; LLM API added as downstream actor based on substrate's mention of "agents invoking external services (such as LLM APIs)".

Outstanding: 0 blocking, 2 warnings, 2 info

## Phase 2 — Drafting

- [INFO] Substrate-declared IDs (`FR-01..FR-10`, `AR-01..AR-06`, `GR-01..GR-09`, `OR-01..OR-08`, `NFR-01..NFR-07`) use two-digit sequence; do not match the convention regex `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b`. ID stability did not preserve them; output IDs regenerated under the S1 single FR sequence.
- [INFO] Substrate categories AR / GR / OR mapped into §5 Functional Requirements (S1 has no separate Access / Governance / Observability sections). Logical grouping retained via subheadings.
- [INFO] Substrate category NFR mapped into §6 Constraints; FR sequence continues.
- [WARNING] Substrate `FR-09` is compound (two `SHALL` clauses: preserve artifacts AND render ineligible). Split into output `FR-009` (preserve) and `FR-010` (ineligibility). → Confirm split is intended.
- [WARNING] Substrate `AR-06` is compound (one `SHALL` grant + one `SHALL NOT` deny). Recombined into a single-`SHALL` form using "only … to which the agent is assigned". → Verify the deny clause remains correctly expressed.
- [WARNING] Substrate `NFR-07` is two sentences with two `SHALL` constructs. Combined into a single-`SHALL` requirement (`FR-041`) with a "such that" clause. → Verify atomicity intent preserved.
- [WARNING] RFC 2119 `MAY` (substrate `AR-01`) translated to EARS form ("The framework SHALL permit only …"). → Verify the operator-only restriction reads as intended.
- [INFO] All other requirements rendered as Ubiquitous EARS; no event/state/optional triggers other than `FR-009`, `FR-010` (Event-driven WHEN-aborted) and `FR-011` (Unwanted Behavior IF/THEN).

Outstanding: 0 blocking, 4 warnings, 4 info

## Phase 3 — Vocabulary

- [INFO] 20 substrate-defined terms preserved (status `substrate`).
- [WARNING] Auto-derived term `abort` added — used in `FR-009`/`FR-010`/`FR-012`; substrate defines only the noun `aborted` via `terminal state`. → Verify wording.
- [WARNING] Auto-derived term `execution outputs` added — used in `FR-014`; substrate references the phrase in `AR-03` without dedicated definition. → Verify wording.
- [WARNING] Auto-derived term `agent session` added — used in `FR-004`/`FR-021`/`FR-027`/`FR-028`; substrate uses the term throughout but does not define it explicitly. → Verify wording.

Outstanding: 0 blocking, 3 warnings, 1 info

## Phase 4 — Taxonomy hygiene

| Check | Result |
|:--|:--|
| ID format `<CAT>-NNN` valid per category | Pass — all 41 IDs match `FR-\d{3}` |
| ID sequence dense per category | Pass — `FR-001`..`FR-041`, no gaps |
| No duplicate IDs within a category | Pass |
| Terms used in requirements present in §Glossary | Pass after auto-derivation of `abort`, `execution outputs`, `agent session` |
| Each FR / CON entry uses a legal EARS pattern | Pass — Ubiquitous (38), Event-driven (2: `FR-009`, `FR-010`), Unwanted Behavior (1: `FR-011`) |
| Each FR / CON entry contains exactly one `SHALL` | Pass — verified including `SHALL NOT` (`FR-011`, `FR-036`) and `SHALL` with embedded "such that" (`FR-041`) |
| RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) absent from EARS statements | Pass |

Outstanding: 0 blocking, 0 warnings, 0 info

## Phase 5 — Verification

- [INFO] Acceptance Criteria derived for all 41 requirements; no `N/A` AC entries emitted.
- [INFO] Quality-Criteria scorecard rendered with `Bounded = N/A` for every row. All output IDs use the `FR-` prefix per S1 single-sequence rule; under verification.md the Bounded check applies only to NFR-class IDs (`NFR`, `OBS`, `SEC`). Substrate's NFR-prefixed quantitative-class concerns (e.g. `FR-035` machine restart, `FR-039` reproducibility, `FR-041` atomicity) cannot be checked for quantitative thresholds in the S1 scorecard.
- [WARNING] Substrate explicitly excludes quantified targets ("Quantified latency, throughput, or cost targets" — Out of Scope). Several output requirements (`FR-005`, `FR-035`, `FR-037`, `FR-039`, `FR-041`) carry quality attributes that would be `Bounded`-checked under S2; in S1 they pass the scorecard by N/A. → Reconsider running this requirement set under `--type technical` if quantitative thresholds matter.

Outstanding: 0 blocking, 1 warning, 2 info

## Phase 6 — Format

- [INFO] Requirements file written at `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/requirements/cod-framework-v02/cod-framework-v02-requirements.md`.
- [INFO] Report file written at `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/requirements/cod-framework-v02/cod-framework-v02-report.md`.

Outstanding: 0 blocking, 0 warnings, 2 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-06 |
| Status       | Draft      |
