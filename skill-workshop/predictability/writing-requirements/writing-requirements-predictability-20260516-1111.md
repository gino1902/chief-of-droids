# writing-requirements predictability report

Generated: 2026-05-16 11:11
Runs analyzed: 5 — v01, v02, v03, v04, v05
Substrate: `requirements/substrates/two-tier-architecture-design-notes.md`
Analyzed skill: `.claude/skills/writing-requirements/`
Comparable artifacts: `chief-of-droids-3-tiers-upgrade-requirements.md`
Non-comparable artifacts excluded: none

> Single comparable artifact — every "worst artifact" cell collapses to the requirements artifact. The artifact column is retained in tables for template fidelity.

> v03 and v05 are byte-identical files (confirmed via `cmp`). Treating them as independent runs inflates apparent stability; the analysis flags this in the deviation summary and discounts duplicate evidence where it would mask drift.

## Summary - Outputs Variance per Dimension

| Category | Actual | Projected | Comments |
|:--|:--|:--|:--|
| Structure | 0% | 0% | All 5 runs render the 15-section S2 template in identical order; no recommendation targets this dimension. |
| Substrate fidelity | 15% | 5% | Verbatim casing of `Could this be a workspace skill?` drifts to lowercase in v03/v05; DR-002 schema folded in v03/v04/v05. R-001, R-002, R-003, R-004 narrow this band. |
| Modality | 15% | 15% | NFR-001 SHOULD stable in 5/5; v04 introduces a SHALL NOT pair on CON-010 absent elsewhere. No recommendation targets this dimension. |
| Naming | 0% | 0% | All 5 runs read H1 verbatim from substrate (`Two-Tier CLAUDE.md Architecture — Design Notes`); no recommendation targets this dimension. |
| Identifier | 45% | 5% | CON-001 anchors three different statements across v01/v02/v04; FR-010..FR-016 cyclic ID shift in v02 and v04. R-001 + R-004 + R-005 collapse the drift. |

Analysis produced by `claude-opus-4-7[1m]`. Variance is the inverse of the predictability score: `variance = 100% − stability_score`, computed per dimension per artifact, then aggregated with the same worst-of-artifact rule used everywhere else in this report. For multi-sub-dimension categories (Substrate fidelity), the stability score is the mean across sub-dimensions before inversion. Numbers are rounded to multiples of 5 to avoid false precision. Projected values apply the recommendations from §Recommendations analytically — no re-runs were performed.

## Top-line scores

Score is the worst-of across comparable artifacts. `Worst artifact` names the artifact producing it (`all` if tied at the same value across all comparable artifacts).

| Dimension | Worst artifact | Score | Reading |
|:--|:--|:--|:--|
| Section structure fidelity | all | **100%** | All 5 runs render the 15-section S2 template in identical order: Purpose → Scope → Actors → Glossary → FR → IR → DR → NFR → Security → Constraints → ERR → OBS → AC → QC scorecard → Version block. Zero reorderings, zero demotions. |
| Identifier alignment | requirements | **~55%** | Workspace-first-resolution statement anchored to FR-013 in v01, FR-010 in v02, FR-012 in v03/v04/v05; trigger-collision-scan anchored to FR-010 in v01/v03/v05, FR-011 in v02, FR-009 in v04. CON-001 anchors three different statements: Layer 1 minimality (v01, v02), workspace-tier-wins (v03, v05), Layer 2 composition (v04). |
| Substrate fidelity — domain concepts | requirements | **~85%** | Two-Tier, three-layer model, Bootstrap protocol, Sentinel, `resolved_skills`, workspace/project tier — all preserved semantically in every run. Glossary entry count varies 17–27 (v04 trims the most; v01 most exhaustive). "Reliability principle" not surfaced as a discrete glossary entry in v03/v04/v05 — folded into CON. |
| Substrate fidelity — schemas | requirements | **~90%** | Seven-field sentinel schema (DR-001) preserved verbatim in all 5 runs. `resolved_skills` row schema (`{trigger, skill, tier}`) present as DR-002 in v01, v02; folded into DR-001 Notes in v03, v04, v05 — 0.5 credit per scoring rubric (renamed/folded consistently across the three). |
| Substrate fidelity — paths | requirements | **~95%** | `chief-of-droids/.sessions/<urlencoded-uri>.json`, `chief-of-droids/CLAUDE.md`, `<project>/CLAUDE.md`, `<project>/brief.md` — byte-level identical in every run. v01 omits the `.sessions` path from CON-007; v02–v05 carry it explicitly. |
| Substrate fidelity — verbatim strings | requirements | **~75%** | `Which project?` preserved verbatim (with `?`) in all 5 runs. `Could this be a workspace skill?` rendered case-stable in v01/v02/v04 ("Could…"); v03/v05 render lowercase ("could this be a workspace skill?"). One-character casing drift on a substrate-quoted prompt. |
| Substrate fidelity — policies / constraints | requirements | **~80%** | Workspace-tier-wins, disjoint triggers, one-way composition, negative-trigger precedence, Layer 1 minimality, brief/CLAUDE.md separation, project-once-per-session, PR-only governance — all carried as CONs with modality `SHALL`. Reliability-budget-priority (CON-009 in v01/v02; CON-011 in v05; absent as own CON in v04). |
| Modality and surface drift | requirements | **~85%** | NFR-001 (~92% reliability) consistently `SHOULD` in 5/5 runs. NFR-003 (Layer 1 minimal footprint) consistently `SHOULD`. CON modalities stable at `SHALL`. v04 introduces `SHALL NOT` on CON-010 ("no runtime override SHALL bypass…") absent in others (workspace-tier-wins is `SHALL` only elsewhere). |
| Naming framing | all | **100%** | All 5 runs use H1 `# Two-Tier CLAUDE.md Architecture — Design Notes` — verbatim substrate title. No run substitutes the user-supplied slug `chief-of-droids-3-tiers-upgrade`. Substrate framing wins in 5/5. |

**Overall predictability — current (measured, worst-of artifact):**   Substance ≈ **0.81** · Structure ≈ **1.00** · Naming ≈ **1.00** [worst artifact(s): requirements].
**Overall predictability — projected (after R-001..R-006, analytical, worst-of artifact):** Substance ≈ **0.93** · Structure ≈ **1.00** · Naming ≈ **1.00**.

Per-artifact aggregate breakdown:

| Artifact | Substance | Structure | Naming |
|:--|:--|:--|:--|
| chief-of-droids-3-tiers-upgrade-requirements.md | 0.81 | 1.00 | 1.00 |

## Section structure fidelity

| Artifact | Run | Heading sequence delta |
|:--|:--|:--|
| requirements | v01 | — |
| requirements | v02 | — |
| requirements | v03 | — |
| requirements | v04 | — |
| requirements | v05 | — |

Canonical sequence per artifact:

- **requirements:** Purpose · Scope (In/Out) · Actors & Consumers · Glossary · Functional Requirements · Interface Requirements (IR-IN, IR-OUT) · Data Requirements (DR, TR) · Non-Functional Requirements · Security · Constraints · Error Handling · Observability · Acceptance Criteria · Quality Criteria scorecard · Version block

Notes: Structure is the single fully-locked dimension. The S2 template's 15-section ordering binds every run. No structural drift to score against.

## Identifier alignment

| Artifact | Identifier | Coverage (n/N) | Anchor stability | Notes |
|:--|:--|:--|:--|:--|
| requirements | FR-001 (sentinel read) | 5/5 | stable | Same statement anchored to FR-001 in every run. |
| requirements | FR-002 (`Which project?` prompt) | 5/5 | stable | Verbatim string preserved. |
| requirements | FR-003 (three-file load) | 5/5 | stable | All five runs anchor the three-artifact load to FR-003. |
| requirements | FR-004 (load verification) | 5/5 | stable | — |
| requirements | FR-005 (sentinel write) | 5/5 | **fold/split** | v04 folds anchor emission into FR-005; v01/v02/v03/v05 keep FR-006 separate. |
| requirements | FR-006 (bind anchor emit) | 4/5 | **fold/split** | Absent in v04 (folded into FR-005). |
| requirements | FR-009 (proceed silently) | 5/5 | stable | Anchors the negative-outcome G-1a contract in every run. |
| requirements | FR-010 (collision scan) | 5/5 | **drift** | Anchored to FR-010 in v01/v03/v05; FR-011 in v02; FR-009 in v04. |
| requirements | FR-011 (hard-reject on collision) | 5/5 | **drift** | Anchored to FR-011 in v01/v03/v04/v05; FR-012 in v02. |
| requirements | FR-012 (workspace-first dispatch) | 5/5 | **drift** | Anchored to FR-013 in v01, FR-010 in v02, FR-012 in v03/v04/v05. |
| requirements | FR-013 (`resolved_skills` populate) | 5/5 | **drift** | Anchored to FR-012 in v01, FR-013 in v02/v03/v05, FR-011 in v04. |
| requirements | FR-014 (major-version bump on trigger edit) | 5/5 | **drift** | FR-014 in v01/v02/v03/v05, FR-013 in v04. |
| requirements | FR-015 (removal block while referenced) | 5/5 | **drift** | FR-015 in v01/v02/v03/v05, FR-014 in v04. |
| requirements | FR-016 (author promotion prompt) | 5/5 | **drift** | FR-016 in v01/v02/v03/v05, FR-015 in v04. |
| requirements | CON-001 | 5/5 | **drift (split anchor)** | Layer 1 minimality (v01, v02); workspace-tier-wins (v03, v05); Layer 2 composition (v04). Three different statements share the same ID. |
| requirements | CON-005 (always-on tools at Layer 1) | 5/5 | stable | Identical statement under CON-005 in every run. |
| requirements | CON-006 (project-specific tools at Layer 3) | 5/5 | stable | — |
| requirements | DR-001 (sentinel schema) | 5/5 | stable | Seven-field schema preserved verbatim under DR-001 across runs. |
| requirements | DR-002 (`resolved_skills` row) | 2/5 | **fold** | Standalone DR-002 in v01, v02; folded into DR-001 Notes column in v03, v04, v05. |
| requirements | TR-001 (sentinel path derivation) | 5/5 | stable | URL-encode + prepend + append rule preserved. |
| requirements | TR-002 (file SHA computation) | 4/5 | partial | TR-002 present in v01, v03, v04, v05; absent in v02 (only TR-001 is rendered). |
| requirements | NFR-001 (routing reliability) | 5/5 | stable | All five anchor the ≥92% target under NFR-001 with modality `SHOULD`. |
| requirements | NFR-002 (Performance N/A) | 5/5 | stable | — |
| requirements | NFR-003 (Layer 1 footprint) | 5/5 | stable | — |

Split/fold events: 
- FR-005/FR-006 fold in v04 (sentinel write + anchor merged).
- DR-002 fold in v03/v04/v05 (`resolved_skills` row absorbed into DR-001 Notes).
- TR-002 omission in v02.
- FR-010..FR-016 cyclic ID shift in v02 and v04: same seven statements, three different ID alignments across the five runs.
- CON-001 anchors three semantically distinct statements across runs (Layer 1 minimality / workspace-tier precedence / Layer 2 composition).

## Substrate fidelity — invariants probed

One row per (invariant, artifact) cell. An invariant the analyzed skill never surfaces in a given artifact across any run is annotated `n/a` rather than `✗`.

| Invariant | Class | Artifact | Source span | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| `chief-of-droids/.sessions/<urlencoded-uri>.json` | path | requirements | L80 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/CLAUDE.md` | path | requirements | L65, L87 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/<project>/CLAUDE.md` | path | requirements | L66, L88 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/<project>/brief.md` | path | requirements | L67, L89 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `recent_chats[0].uri` | path | requirements | L61, L86 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `claude_desktop_config.json` | path | requirements | L51 | ✓ | ✓ | ✓ | ≈ | ✓ |
| Sentinel schema (7 fields) | schema | requirements | L82–90 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `resolved_skills` row (`{trigger, skill, tier}`) | schema | requirements | L90 | ✓ | ✓ | ≈ | ≈ | ≈ |
| Two-Tier (three-layer) model | concept | requirements | L35–39 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Layer 1 / Layer 2 / Layer 3 | concept | requirements | L37–39 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Bootstrap protocol | concept | requirements | L57–76 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Sentinel | concept | requirements | L78–90 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Workspace tier / Project tier | concept | requirements | L112–119 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Reliability principle (mech > once-per-session > behavioral) | concept | requirements | L98–108 | ✓ | ≈ | ≈ | ✗ | ≈ |
| Always-on tools (filesystem, git, fetch) | concept | requirements | L52, L55 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Tool-layer vocabulary (Registration / Routing / Usage) | concept | requirements | L47–55 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Negative trigger precedence (workspace-first) | concept | requirements | L132 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `Which project?` | verbatim | requirements | L63 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `Could this be a workspace skill?` | verbatim | requirements | L133 | ✓ | ✓ | ≈ | ✓ | ≈ |
| "workspace tier wins" | verbatim | requirements | L112 | ≈ | ≈ | ≈ | ≈ | ≈ |
| "single-predicate-per-turn" | verbatim | requirements | L59 | ≈ | ≈ | ✓ | ✓ | ≈ |
| Workspace-tier-wins precedence | policy (SHALL) | requirements | L112 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Disjoint trigger phrases | policy (SHALL) | requirements | L116 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Sentinel records `{trigger → skill, tier}` map at bind | policy (SHALL) | requirements | L117 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Layer 1 minimality (bootstrap, sentinel verify, tool routing only) | policy (SHALL) | requirements | L43 | ✓ | ✓ | ≈ | ✓ | ≈ |
| Substantive content in Layer 2/3, not Layer 1 | policy (SHALL) | requirements | L45 | ✓ | ✓ | ✓ | ✗ | ✓ |
| Always-on tools at Layer 1 | policy (SHALL) | requirements | L55 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Project-specific tools at Layer 3 | policy (SHALL) | requirements | L55 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Project selected once per session, no default | policy (SHALL) | requirements | L76 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Workspace skill removal blocked while project skill references it | policy (SHALL) | requirements | L130 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Major-version bump on workspace trigger edit | policy (SHALL) | requirements | L129 | ✓ | ✓ | ✓ | ✓ | ✓ |
| One-way composition (workspace → project forbidden) | policy (SHALL) | requirements | L131 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Reliability budget: mechanical > once-per-session > behavioral | policy (SHALL/SHOULD) | requirements | L100–104 | ✓ | ✓ | ≈ | ✗ | ≈ |
| Routing reliability ≈ 92–93% | policy (SHOULD) | requirements | L119 | ✓ | ✓ | ✓ | ✓ | ✓ |
| PR-to-workspace governance escape hatch (no runtime override) | policy (SHALL) | requirements | L128 | ✓ | ✓ | ✓ | ✓ | ✓ |

Legend: ✓ verbatim · ≈ semantic match · ✗ missing or distorted · n/a invariant not expected in this artifact.

## Modality and surface drift

| Artifact | Identifier | Statement (anchor) | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:--|:--|:--|:--|:--|
| requirements | NFR-001 | Routing reliability ≥ 92% | SHOULD | SHOULD | SHOULD | SHOULD | SHOULD |
| requirements | NFR-003 | Layer 1 minimal token footprint | SHOULD | SHOULD | SHOULD | SHOULD | SHOULD |
| requirements | CON-005 (v01-v02) / CON-004 (v03-v05) / CON-004 (v04) | Always-on tools at Layer 1 | SHALL | SHALL | SHALL | SHALL | SHALL |
| requirements | CON workspace-tier-wins | Workspace-tier wins on collision | SHALL | SHALL | SHALL | SHALL (with SHALL NOT pair) | SHALL |
| requirements | FR-002 | Prompt `Which project?` | SHALL | SHALL | SHALL | SHALL | SHALL |
| requirements | FR-016 / FR-015 | Author promotion prompt | SHALL | SHALL | SHALL | SHALL | SHALL |

Surface drift (semantic-equivalent rewordings worth flagging):
- v04 splits CON-010 into a `SHALL` + `SHALL NOT` pair on runtime override; other runs render a single `SHALL` (PR-to-workspace) clause.
- v01 phrases sentinel read as "framework SHALL read"; v03/v05 phrase as "dispatcher SHALL read" (semantic equivalent but subject shifts from `framework` to `dispatcher`).
- v03 and v05 are byte-identical — zero drift between them; their agreement is not independent evidence.

## Statement counts per category

### Artifact: chief-of-droids-3-tiers-upgrade-requirements.md

| Category | v01 | v02 | v03 | v04 | v05 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| FR | 16 | 16 | 16 | 15 | 16 | 15 | 16 | 15.8 |
| IR-IN | 2 | 3 | 3 | 5 | 3 | 2 | 5 | 3.2 |
| IR-OUT | 3 | 4 | 3 | 3 | 3 | 3 | 4 | 3.2 |
| DR | 2 | 2 | 1 | 1 | 1 | 1 | 2 | 1.4 |
| TR | 2 | 1 | 2 | 2 | 2 | 1 | 2 | 1.8 |
| NFR | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.0 |
| SEC | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 | 0 | 0.0 |
| CON | 14 | 13 | 11 | 13 | 11 | 11 | 14 | 12.4 |
| ERR | 11 | 11 | 13 | 3 | 13 | 3 | 13 | 10.2 |
| OBS | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 (N/A) | 0 | 0 | 0.0 |
| Glossary entries | 27 | 25 | 22 | 17 | 22 | 17 | 27 | 22.6 |

ERR count is the loudest deviation: v04 emits 3 ERRs versus 11–13 in the other runs. The drop is structural (v04 attaches `(no ERR — rationale: …)` opt-outs to most FRs rather than drafting ERR entries) — not a bug, but a different reading of the ERR coverage protocol in `references/ears.md`. Five runs producing three distinct ERR counts (3, 11, 13) on a protocol whose Phase 2 directive is "MUST draft in the same pass" is the highest-leverage finding in this report.

## Naming framing finding

Substrate names this work: **"Two-Tier CLAUDE.md Architecture — Design Notes"** (source: substrate H1, line 1).

| Artifact | Run | Title used | Framing |
|:--|:--|:--|:--|
| requirements | v01 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| requirements | v02 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| requirements | v03 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| requirements | v04 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| requirements | v05 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |

Finding: 5/5 runs read the title verbatim from the substrate H1. No run substitutes the user-supplied slug `chief-of-droids-3-tiers-upgrade`. The Phase 1 fallback chain in `writing-requirements/SKILL.md` (H1 → H2 → frontmatter → slug) terminates cleanly at H1 in every run. Naming framing is the most stable dimension in this analysis.

## Per-file deviation summary

### v01

- **requirements:** Largest glossary (27 entries — every backtick-wrapped token and capitalized phrase emitted). Two-DR rendering (DR-001 for sentinel + DR-002 for `resolved_skills` row). 14 CONs — most explicit "Reliability budget" CON. Workspace-first dispatch anchored to FR-013 (unique among runs).

### v02

- **requirements:** IR-IN-003 added (on-disk SHA as input — only run to surface this as a distinct inbound interface). IR-OUT-004 added (author-prompt as outbound — verbatim string promoted to its own interface). Cyclic ID-shift on FR-010..FR-013 (collision-scan at FR-011, workspace-first at FR-010). TR-002 omitted. Outlier in IR-IN count (3) and IR-OUT count (4).

### v03

- **requirements:** CON-001 reassigned to "workspace-tier-wins" (vs Layer 1 minimality elsewhere). DR-002 folded into DR-001 Notes. `Could this be a workspace skill?` casing dropped to lowercase. Byte-identical to v05 — its independence is illusory.

### v04

- **requirements:** Strongest structural divergence: 15 FRs (vs 16 elsewhere), 3 ERRs (vs 11–13), 5 IR-IN entries (vs 2–3). Folds anchor emission into FR-005; uses `(no ERR — rationale: …)` opt-outs heavily. CON-001 reassigned to Layer 2 composition; "substantive content in Layer 2/3, not Layer 1" not surfaced as a CON. Glossary trimmed to 17 (smallest). The "outlier" run.

### v05

- **requirements:** Byte-identical to v03 (`cmp` returns 0 differences). Carries the same CON-001 reassignment, the same DR-002 fold, the same lowercase casing on the author prompt. Adds zero independent signal — every agreement-with-v03 in the tables above is one observation, not two.

### Non-comparable artifacts

None — the user-confirmed `--files` glob (`*-requirements.md`) yields one artifact, present in 5/5 runs.

## Predictability verdict

The dominant source of variance is **identifier alignment** (~55%) within the requirements artifact: the seven statements anchored to FR-010..FR-016 in v01/v03/v05 are cyclically remapped in v02 and folded in v04, and CON-001 carries three different statements across the five runs. The single highest-leverage fix is to bind identifier assignment to the substrate's byte-position walk (already specified in `conventions.md` § "Canonical ordering for un-IDed substrate") with explicit reference from Phase 2 of `SKILL.md`. **Section structure fidelity** (100%) and **Naming framing** (100%) are already locked — no recommendation targets them.

A secondary high-leverage drift is the **ERR coverage protocol**: v04 produces 3 ERRs while v01/v02/v03/v05 produce 11–13. The Phase 2 directive in `references/ears.md` ("Mandatory drafting (Phase 2): FRs whose contract shape is Acquire/Mutate/Validate/Solicit/Transform-with-external-inputs MUST have a paired ERR drafted") is not consistently applied — v04 reads it as opt-out-friendly, others as opt-out-rare.

The v03 ≡ v05 byte-identity is itself a signal: the skill's stateless re-run can produce two byte-identical outputs on the same substrate, suggesting that for some prompt/temperature configurations the answer space collapses. This is good (high reproducibility within a basin) but the basin is not unique (v01, v02, v04 occupy different basins on the same substrate). The N=5 sample undercounts true variance because v05 contributes zero novel evidence.

## Recommendations

*Stress test method: analytical projection — recommendations were applied to the recorded deviations from Phase 3 to estimate their effect. No re-runs were performed.*

### R-001 — Anchor IDs to substrate byte position with explicit Phase 2 reference     [projected lift: +25 pts]

- Targets: Identifier alignment (requirements), Substrate fidelity — policies (requirements)
- Statement: In Phase 2, before drafting any FR/CON/IR/DR/TR/NFR/ERR statement, walk the substrate body top-to-bottom and assign category IDs in the order each requirement-shaped sentence's first modal verb appears. Reference `conventions.md` § "Canonical ordering for un-IDed substrate" explicitly from `SKILL.md` Phase 2 — currently the canonical-ordering rule exists in conventions but is not invoked by name from Phase 2's drafting step.
- Rationale: The seven-statement cyclic ID shift in v02 and v04 (FR-010..FR-016) and the three-meaning CON-001 split would all collapse if every run walked the substrate body in the same order. The rule already exists; it's not bound to the drafting step.
- Projected effect: prevented 7 (the FR-010..FR-016 cyclic shifts in v02 and v04, CON-001 split), partial 2 (DR-002 fold across v03/v04/v05 — fold is a separate decision), unaffected 0, regressed 0.
- Risk: Forces the skill to compute a substrate-byte order before drafting begins; slightly slower Phase 2. Acceptable cost.

### R-002 — Pin verbatim user-channel prompts in the skill prompt     [projected lift: +15 pts]

- Targets: Substrate fidelity — verbatim strings (requirements)
- Statement: Verbatim user-channel prompts (the `Which project?` bind prompt; the `Could this be a workspace skill?` promotion prompt) MUST be carried into output with byte-level fidelity, including capitalization. Add an explicit substrate-prompt list to `SKILL.md` Phase 0 and require the drafter to copy from that list rather than paraphrase.
- Rationale: v03 and v05 lowercase `Could this be a workspace skill?` to `could this be a workspace skill?`. One-character casing drift on a user-channel prompt is the kind of invariant that should never degrade.
- Projected effect: prevented 2 (v03 + v05 casing drift), partial 0, unaffected 0, regressed 0.
- Risk: Pinning a prompt's wording resists substrate evolution; if the substrate intentionally rewords, the pin would need updating. Note this is a low-risk class of verbatim (user prompts are typically stable).

### R-003 — Make ERR coverage protocol opt-out explicit per FR     [projected lift: +15 pts]

- Targets: Statement counts per category (requirements), Substrate fidelity — policies (requirements)
- Statement: For every FR whose contract shape is Acquire/Mutate/Validate/Solicit/Transform-with-external-inputs (per `references/ears.md` § "Contract-shape coverage matrix"), the skill MUST either draft a paired ERR in the same Phase 2 pass OR attach an inline `(no ERR — rationale: <reason>)` opt-out to the FR. Phase 4 audits the pair; Phase 2 is required to make the choice explicit. Default behavior when shape mandates coverage and substrate provides no failure-path text: draft a generic "halt + surface error" ERR rather than opt-out.
- Rationale: v04 generates 3 ERRs vs 11–13 in others by interpreting "substrate silent on failure path" as opt-out. v01/v02/v03/v05 interpret it as draft-the-generic-halt. The default behavior is not specified.
- Projected effect: prevented 10 (the 10 missing ERR entries in v04 vs the median of 11), partial 0, unaffected 3 (the 3 ERRs v04 already drafts), regressed 0.
- Risk: Forces a draft-or-rationale choice on every Acquire/Mutate/Validate FR; slightly increases Phase 2 cost. The benefit is a deterministic ERR count per substrate.

### R-004 — Lock `resolved_skills` row schema rendering     [projected lift: +10 pts]

- Targets: Identifier alignment (requirements), Substrate fidelity — schemas (requirements)
- Statement: When the substrate names a sub-entity (here `{trigger, skill, tier}` row inside `resolved_skills`), the skill MUST render it as a distinct DR-NNN entry — never fold it into a parent DR's Notes column. The minimum threshold for a distinct DR is named-fields-with-types; the substrate's three named fields meet that threshold.
- Rationale: v01 and v02 render DR-002; v03/v04/v05 fold it into DR-001 Notes. The Notes-column fold loses the typed-field schema and breaks the cross-link target for `resolved_skills`-related ACs.
- Projected effect: prevented 3 (v03, v04, v05 fold events), partial 0, unaffected 0, regressed 0.
- Risk: One extra DR entry per nested entity. Negligible cost. Mild risk that the rule over-fires on shallow nested structures — `references/tables.md` already carries the "two typed-field rows minimum" filter, which catches that case.

### R-005 — Promote routing-precedence active behavior to fixed FR slot     [projected lift: +8 pts]

- Targets: Identifier alignment (requirements)
- Statement: The "workspace-tier-wins" dispatch behavior — active path resolved by the dispatcher at runtime — MUST be rendered as an FR (not a CON). When the substrate names both the active behavior and the invariant (G-1b in `references/ears.md`), the skill renders one FR for the dispatch and one CON for the invariant; never one alone, never the invariant masquerading as CON-001. The FR for workspace-first dispatch is assigned the next available FR-NNN after the resolved-skills-populate FR.
- Rationale: v01 anchors workspace-first to FR-013, v02 to FR-010, v03/v04/v05 to FR-012. CON-001 across runs swings between Layer-1-minimality, workspace-tier-wins, and Layer-2-composition. The active dispatch path and the precedence invariant are tangled.
- Projected effect: prevented 5 (the FR-010..FR-013 cyclic shifts on workspace-first), partial 2 (CON-001 split — the rule names where active behavior goes, not how to pick which CON gets the -001 slot), unaffected 0, regressed 0.
- Risk: Over-fires when substrate provides only the invariant flavor without the active behavior — the rule needs a "G-1b precondition: both flavors named" guard. `references/ears.md` § G-1b already carries that guard; the recommendation references it.

### R-006 — Suppress Phase 0 artifact-confirmation prompt when discovery is unambiguous     [projected lift: +5 pts]

- Targets: Predictability of the analysis skill (`improving-skills-predictability`), not the analyzed `writing-requirements`. Note this recommendation is meta — surfaced as a finding from running the present analysis.
- Statement: In `improving-skills-predictability/SKILL.md` Phase 0 step 3, the artifact-confirmation prompt fires only when at least one of these conditions holds: (a) ≥1 non-comparable artifact exists; (b) ≥1 comparable artifact has coverage gaps in some runs; (c) the `--files` glob was auto-proposed in this session rather than user-supplied; (d) ≥2 distinct slug groups co-exist under the resolved outputs directory. When none of (a)–(d) hold, skip the prompt and proceed directly to Phase 1.
- Rationale: When this analysis was run, the user-confirmed `--files` glob produced 1 comparable artifact × 5 runs with full coverage. The artifact-confirmation prompt added zero signal and was challenged by the user as dead weight. Gating the prompt on ambiguity restores its purpose.
- Projected effect: prevented 1 (the dead prompt this session), partial 0, unaffected 0, regressed 0 (the prompt still fires when it's useful).
- Risk: A subtle ambiguity that doesn't match (a)–(d) could slip through. Reviewers should keep an escape hatch — e.g., an `--always-confirm` flag — for users who want the prompt unconditionally.

| Field        | Value       |
|--------------|-------------|
| Version      | 1.0         |
| Last Updated | 2026-05-16  |
| Status       | Draft       |
