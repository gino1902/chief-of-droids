# writing-requirements predictability report

Generated: 2026-05-15 (test run)
Runs analyzed: 5 — v01..v05 (`chief-of-droids-3-tiers-upgrade-v01` through `v05`)
Substrate: `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/requirements/substrates/two-tier-architecture-design-notes.md`
Analyzed skill: `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/.claude/skills/writing-requirements`

## Top-line scores

| Dimension | Score | Reading |
|:--|:--|:--|
| Section structure fidelity | **~95%** | 13/14 top-level sections appear in the same order in every run; v02 demotes "Actors & Consumers" from H2 to H3 inside `## Scope` (single demotion, content preserved). |
| Identifier alignment | **~25%** | FR-001 is stable (sentinel-read) in 4/5 runs but v02 reassigns it to a path-scoped-rule-load FR; the "could this be workspace?" prompt FR floats across IDs FR-016 (v01), FR-014 (v02), FR-015 (v03), FR-013 (v04), and is no longer a discrete FR in v05. |
| Substrate fidelity — domain concepts | **~85%** | Layer 1 / Layer 2 / Layer 3 are present in all 5 runs; the substrate's Registration / Routing / Usage triad (substrate lines 49–55) is carried by v02, v03, v04, v05 glossaries but not by v01; the "six capabilities" enumeration is explicit in v01, v04, v05 and partial in v02, v03. |
| Substrate fidelity — schemas | **~95%** | The sentinel 7-field schema (`uri`, `project`, `loaded_at`, `workspace_md_sha`, `project_md_sha`, `brief_sha`, `resolved_skills`) is preserved field-for-field in all 5 runs; v04 and v05 extract `resolved_skill` into a separate DR-002 — a semantic-equivalent expansion, not a loss. |
| Substrate fidelity — paths | **~90%** | `chief-of-droids/.sessions/<urlencoded-uri>.json`, `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, and `chief-of-droids/<project>/brief.md` appear byte-identical in all 5 runs; `docs/session-identity-recommendation.md` appears verbatim in v01, v04, v05 and is paraphrased/dropped from out-of-scope in v02, v03. |
| Substrate fidelity — verbatim strings | **~40%** | `"Which project?"` is preserved in all 5 runs (FR-002 / IR-OUT-001); `"could this be workspace?"` is preserved verbatim only in v01 and v02 — v03 drifts to `"could this be a workspace skill?"`, v04 drifts to `"Could this be a workspace skill?"`, and v05 omits a quoted form altogether. |
| Substrate fidelity — policies / constraints | **~85%** | Workspace-tier-wins precedence, Layer 1 minimality, trigger-disjointness, one-way composition, and no-runtime-override are all present in 5/5 runs; the reliability-budget priority list is encoded as a CON only in 3/5 runs (v01 CON-014, v04 CON-010, v05 CON-011) — absent from v02 and v03. |
| Modality and surface drift | **~70%** | NFR-001 (skills-routing reliability ≥ 92%) modality splits 3:2 across runs — MUST in v01, v02, v05; SHOULD in v03, v04 — for the same enforceable statement; NFR-003 is stable at SHOULD across all 5. |
| Naming framing | **~100%** | All 5 runs use the substrate H1 verbatim: `Two-Tier CLAUDE.md Architecture — Design Notes`. None reach for the slug `chief-of-droids-3-tiers-upgrade`. |

**Overall predictability — current (measured):**   Substance ≈ **0.70** · Structure ≈ **0.95** · Naming ≈ **1.00**.
**Overall predictability — projected (after R-001..R-005, analytical):** Substance ≈ **0.85** · Structure ≈ **0.95** · Naming ≈ **1.00**.

## Section structure fidelity

| File role | Run | Heading sequence delta |
|:--|:--|:--|
| requirements | v01 | — |
| requirements | v02 | "Actors & Consumers" demoted from H2 to H3, placed inside `## Scope`; all other sections in canonical order |
| requirements | v03 | — (adds `---` horizontal rule separators between sections; no heading delta) |
| requirements | v04 | — |
| requirements | v05 | — |

Canonical sequence (longest common): Purpose · Scope · Actors & Consumers · Glossary · Functional Requirements · Interface Requirements · Data Requirements · Non-Functional Requirements · Security · Constraints · Error Handling · Observability · Acceptance Criteria · Quality Criteria scorecard.

Notes: structure is the strongest dimension. The only material drift is v02's heading-level demotion of "Actors & Consumers"; content is preserved but the section is no longer addressable by its own anchor. v03 inserts decorative `---` separators that are not structural deviations.

## Identifier alignment

| Identifier (anchor statement) | Coverage (n/N) | Anchor stability | Notes |
|:--|:--|:--|:--|
| FR-001 ("read sentinel for current session") | 5/5 | drift | Stable anchor in v01, v03, v04, v05; in v02, FR-001 is reassigned to "WHEN a filesystem read of a project file occurs the dispatcher SHALL load applicable path-scoped rule files" and sentinel-read moves to FR-002. |
| FR-002 ("prompt 'Which project?'") | 4/5 | drift | Same statement in v01, v03, v04, v05; in v02, FR-002 is "read sentinel" (everything shifts +1). |
| FR (workspace-promotion prompt) | 5/5 | drift | FR-016 in v01, FR-014 in v02, FR-015 in v03, FR-013 in v04; in v05 the prompt is referenced semantically but not as a discrete FR. |
| FR (sentinel write) | 5/5 | drift | FR-005 in v01, FR-006 in v02, FR-004 in v03, FR-004 in v04, FR-007 in v05. |
| FR (anchor emission) | 5/5 | drift | FR-006 in v01, FR-007 in v02, FR-005 in v03, FR-005 in v04, FR-008 in v05. |
| DR-001 (sentinel schema) | 5/5 | stable | Same anchor (sentinel record) in all 5; v04 and v05 add DR-002 (resolved_skill element). |
| TR-001 (sentinel path derivation) | 5/5 | stable | Identical anchor across all 5. |
| TR-002 (SHA computation) | 5/5 | stable | Identical anchor across all 5. |
| NFR-001 (skills-routing ≥ 92%) | 5/5 | stable | Identical anchor across all 5 (modality drifts — see Modality table). |
| CON-001 (Layer 1 minimality content) | 5/5 | stable | Identical anchor in all 5. |
| CON (workspace-tier precedence) | 5/5 | drift | CON-008 (v01), CON-010 (v02), CON-007 (v03), CON-011 in substrate framing in v04 collides — covered as CON-005 in v05. |

Split/fold events:
- "Load workspace CLAUDE.md, project CLAUDE.md, project brief" is one FR (FR-003) in v01, v03, v04 and splits into three FRs (FR-003, FR-004, FR-005) in v05. v02 keeps a single FR-004 but adds dedicated IR-IN entries (IR-IN-003, IR-IN-004, IR-IN-005) for the same three paths.
- "Verify all three loaded + halt on failure" is fused with the load FR in v01, v03, v04 and split into a discrete FR-005 (v02) / FR-006 (v05).

## Substrate fidelity — invariants probed

| Invariant | Class | Source span | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:-:|:-:|:-:|:-:|:-:|
| Layer 1 / Layer 2 / Layer 3 slot mapping | concept | lines 36–39 | ✓ | ✓ | ✓ | ✓ | ✓ |
| "Registration / Routing / Usage" triad | concept | lines 49–55 | ✗ | ✓ | ✓ | ✓ | ✓ |
| Six capabilities (skills routing, session hygiene, …) | concept | lines 24–31 | ✓ | ≈ | ≈ | ✓ | ✓ |
| Sentinel 7-field schema | schema | lines 82–90 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/.sessions/<urlencoded-uri>.json` | path | line 80 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/CLAUDE.md` | path | line 66 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/<project>/CLAUDE.md` | path | line 67 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/<project>/brief.md` | path | line 68 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `docs/session-identity-recommendation.md` | path | lines 10, 137, 146 | ✓ | ≈ | ≈ | ✓ | ✓ |
| `claude_desktop_config.json` | path | line 50 | ≈ | ✓ | ✓ | ✓ | ✓ |
| `recent_chats[0].uri` | path | line 61 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `"Which project?"` | verbatim | line 63 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `"could this be workspace?"` | verbatim | line 133 | ✓ | ✓ | ✗ | ✗ | ✗ |
| Workspace tier wins (precedence) | policy | line 112 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Layer 1 minimality (MUST be minimal but sufficient) | policy | line 43 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Hard reject at authoring time on trigger collision | policy | line 117 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Composition strictly one-way | policy | line 131 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Negative triggers respected with same precedence | policy | line 132 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Explicit project selection required, no default | policy | line 76 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Workspace skill major bump on trigger edit | policy | line 129 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Workspace skill removal blocked when referenced | policy | line 130 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Reliability budget priority order (mechanical > once-per-session > behavioral) | policy | lines 102–104 | ✓ | ✗ | ✗ | ✓ | ✓ |

Legend: ✓ verbatim · ≈ semantic match · ✗ missing or distorted.

## Modality and surface drift

| Identifier | Statement (anchor) | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:-:|:-:|:-:|:-:|:-:|
| NFR-001 | Skills-routing reliability ≥ 92% | MUST | MUST | SHOULD | SHOULD | MUST |
| NFR-003 | Layer 1 token footprint minimal | SHOULD | SHOULD | SHOULD | SHOULD | SHOULD |
| FR (workspace-promotion prompt) | `"could this be workspace?"` | SHALL | SHALL | SHALL | SHALL | (none) |
| IR-IN-001 | Accept `recent_chats[0].uri` | MUST | MUST | MUST | MUST | MUST |
| CON-001 | Layer 1 content scope | SHALL | SHALL | SHALL | SHALL | SHALL |

Surface drift (semantic-equivalent rewordings worth flagging):
- "WHEN a turn begins THEN the framework SHALL read the sentinel" (v01, v02, v04, v05) vs. "WHEN a user turn begins, the framework SHALL read the sentinel" (v03).
- "the framework SHALL prompt the user with `"Which project?"`" (v01, v03, v05) vs. "with the question `"Which project?"`" (v04) vs. plain quotes vs. backticked across runs.
- "anchor" vs. "anchor message" vs. "anchor confirmation" vs. "load-confirmation anchor" — five runs, four distinct phrasings.

## Statement counts per category

| Category | v01 | v02 | v03 | v04 | v05 | min | max | mean |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| FR | 16 | 14 | 15 | 13 | 15 | 13 | 16 | 14.6 |
| IR-IN | 4 | 7 | 3 | 5 | 6 | 3 | 7 | 5.0 |
| IR-OUT | 4 | 5 | 3 | 4 | 4 | 3 | 5 | 4.0 |
| DR | 1 | 1 | 1 | 2 | 2 | 1 | 2 | 1.4 |
| TR | 2 | 3 | 2 | 3 | 2 | 2 | 3 | 2.4 |
| NFR | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.0 |
| CON | 14 | 16 | 13 | 14 | 12 | 12 | 16 | 13.8 |
| ERR | 11 | 11 | 8 | 11 | 11 | 8 | 11 | 10.4 |
| Glossary entries | 24 | 25 | 21 | 22 | 21 | 21 | 25 | 22.6 |

The widest spread is IR-IN (3 to 7 — more than 2× difference). v02 breaks IR-IN into one entry per bound artifact; v03 collapses bind reads into one entry. CON spread (12–16) is driven by whether the reliability-budget priority order is encoded as a CON (v01, v04, v05) or omitted (v02, v03) and by whether the "no runtime override" clause is folded into governance CON or split out.

## Naming framing finding

Substrate names this work: **"Two-Tier CLAUDE.md Architecture — Design Notes"** (substrate H1, line 1).

| Run | Title used | Framing |
|:--|:--|:--|
| v01 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v02 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v03 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v04 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v05 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |

Finding: every run reads the title from the substrate H1 verbatim and none humanises the slug `chief-of-droids-3-tiers-upgrade`. This dimension is at ceiling; the skill's Phase 1 framing rule is robust against slug-driven framing for this substrate.

## Per-file deviation summary

### v01
- Highest FR count of the corpus (16) — pairs every action with a discrete ERR including ERR-001 for sentinel-read and ERR-016 for prompt non-response.
- Only run whose glossary omits the substrate's Registration / Routing / Usage triad — the strongest substrate-fidelity miss in this run.
- Preserves `"could this be workspace?"` verbatim under FR-016.
- NFR-001 modality = MUST.

### v02
- Introduces FR-001 for path-scoped rule loading (no other run treats this as a top-level FR), shifting every downstream FR's ID by one.
- Demotes "Actors & Consumers" from H2 to H3 inside `## Scope` — only structural deviation in the corpus.
- Highest IR-IN count (7) — splits bind reads into one IR-IN entry per artifact.
- Highest CON count (16); omits the reliability-budget priority CON.
- Preserves `"could this be workspace?"` verbatim under FR-014.

### v03
- Thinnest ERR coverage (8) — fuses some load-failure paths into a single ERR.
- Fewest IR-IN entries (3); collapses bind reads into one IR-IN-002.
- Paraphrases the workspace-promotion prompt to `"could this be a workspace skill?"` — first verbatim drift.
- Omits the reliability-budget priority CON.
- NFR-001 modality = SHOULD.
- Adds decorative `---` separators between sections (cosmetic, not structural).

### v04
- Splits the sentinel schema into DR-001 + DR-002 (adds a discrete `resolved_skill` record type with `enum(workspace, project)`).
- Paraphrases the workspace-promotion prompt to `"Could this be a workspace skill?"` (capitalisation + wording drift on the verbatim invariant).
- NFR-001 modality = SHOULD.

### v05
- Splits "load three bind files" into three discrete FRs (FR-003, FR-004, FR-005) and pairs each with its own ERR (ERR-003, ERR-004, ERR-005).
- DR split like v04 (DR-001 + DR-002).
- Fewest CON entries (12); folds several governance CONs together.
- Workspace-promotion prompt is not a discrete FR in this run — the strongest verbatim-string miss of the corpus.
- NFR-001 modality = MUST.

## Predictability verdict

Structure and naming are at or near ceiling — the skill's section-ordering rule and substrate-first framing rule are working. The dominant source of variance is **identifier drift**: the same substrate statement (sentinel-read, workspace-promotion prompt, sentinel-write) lands on different FR numbers across runs because IDs are assigned in narrative order rather than in substrate order. The second-largest source of variance is the **verbatim-string drift** on `"could this be workspace?"` — 3 of 5 runs paraphrase or omit the literal. Pinning the verbatim and locking ID assignment to substrate-walk order would deliver most of the available predictability lift.

## Recommendations

*Stress test method: analytical projection — recommendations were applied to the recorded deviations from Phase 3 to estimate their effect. No re-runs were performed.*

### R-001 — Pin verbatim user-facing strings from the substrate     [projected lift: +50 pts]
- Targets: Substrate fidelity — verbatim strings.
- Statement: When the substrate quotes a string that the framework will emit to a user channel, the skill must carry that string into the output byte-for-byte, including casing and punctuation, and must wrap it in backticks. Do not paraphrase, recase, or rephrase such strings even when reformatting surrounding prose.
- Rationale: v03 paraphrased `"could this be workspace?"` to `"could this be a workspace skill?"`; v04 changed casing and wording to `"Could this be a workspace skill?"`; v05 dropped the verbatim altogether in favour of a semantic restatement. Pinning the rule would have prevented all three drifts.
- Projected effect: prevented 3 (v03, v04, v05), partial 0, unaffected 2 (v01, v02 already verbatim), regressed 0.
- Risk: a pinned wording can age poorly if the substrate intent shifts; tolerable because the rule is "carry whatever the substrate carries", not "carry this specific phrase".

### R-002 — Anchor identifiers to substrate walk order, not narrative order     [projected lift: +35 pts]
- Targets: Identifier alignment.
- Statement: When assigning identifiers in Phase 2, walk the substrate body top-to-bottom and assign the next identifier in the matching category to each requirement-shaped statement at its first appearance. Do not renumber identifiers for narrative flow within the output. Do not reserve early IDs for statements that appear later in the substrate.
- Rationale: FR-001 currently lands on whichever action the run chose to render first — sentinel-read in v01/v03/v04/v05, path-scoped-rule-load in v02. The workspace-promotion FR drifts across IDs FR-013, FR-014, FR-015, FR-016 because runs disagree on its narrative position. Walk-order assignment would collapse this drift.
- Projected effect: prevented 4 (FR-001 swap in v02; sentinel-write ID drift; anchor-emission ID drift; workspace-promotion ID drift), partial 1 (load-three-files split/fold in v05 remains a legitimate substrate ambiguity), unaffected 0, regressed 0.
- Risk: substrate restructuring between iterations breaks ID stability across versions of the same output; document this precedence and use ID stability across runs of the same substrate, not across substrates.

### R-003 — Pin modality by enforceability, not by author preference     [projected lift: +20 pts]
- Targets: Modality and surface drift.
- Statement: Modality is determined by enforceability. A statement is MUST or SHALL when it has a verifiable acceptance test that gates a release; SHOULD when it can be observed but not gated; MAY when it is a discretionary optimisation. Record the enforceability decision in the report alongside the modality.
- Rationale: NFR-001 ("skills-routing reliability ≥ 92%") split 3:2 across MUST and SHOULD across runs for an identical anchor that carries a measurable threshold. Enforceability-based modality pins the answer.
- Projected effect: prevented 2 (v03 and v04 SHOULD on NFR-001), partial 0, unaffected 3 (NFR-003 already stable; other identifiers carry stable modality), regressed 0.
- Risk: forces the skill to evaluate enforceability before writing modality, slightly slowing Phase 2.

### R-004 — Re-read substrate vocabulary blocks before drafting the Glossary     [projected lift: +10 pts]
- Targets: Substrate fidelity — domain concepts.
- Statement: Before drafting the Glossary in Phase 3, re-read the substrate sections that introduce terminology triads, framings, or numbered enumerations (look for headings such as "Vocabulary", "Tool layer vocabulary", "Architecture", and any prose that defines distinct concerns in parallel). Carry every such triad into the Glossary using the substrate's literal phrasing.
- Rationale: v01's Glossary omitted the substrate's explicit Registration / Routing / Usage triad (substrate lines 49–55); v02 and v03 covered the "six capabilities" enumeration only partially. A re-read step locks these structural terminology blocks into the Glossary.
- Projected effect: prevented 1 (v01 triad omission), partial 2 (v02 and v03 partial six-capability coverage), unaffected 2 (v04, v05), regressed 0.
- Risk: increases Phase 3 prompt length and re-read cost.

### R-005 — Mandate substrate reliability/priority statements as Constraints     [projected lift: +10 pts]
- Targets: Substrate fidelity — policies / constraints.
- Statement: When the substrate carries a prioritised list framing how a quality budget is to be spent (e.g., "reliability budget", "performance budget", "trust budget"), encode the priority order as a CON in the output. Do not relocate it to NFR or to Purpose prose.
- Rationale: v02 and v03 dropped the substrate's reliability-budget priority list (mechanical > once-per-session > behavioural) from the CON section even though it is a normative claim the substrate makes explicitly (lines 102–104). v01, v04, v05 encoded it as CON-014 / CON-010 / CON-011 respectively.
- Projected effect: prevented 2 (v02, v03), partial 0, unaffected 3 (v01, v04, v05), regressed 0.
- Risk: a poorly-drafted CON of this shape can look like prose; the skill must hold the priority order as the testable surface, not the philosophical framing around it.

| Field        | Value       |
|--------------|-------------|
| Version      | 1.0         |
| Last Updated | 2026-05-15  |
| Status       | Draft       |
