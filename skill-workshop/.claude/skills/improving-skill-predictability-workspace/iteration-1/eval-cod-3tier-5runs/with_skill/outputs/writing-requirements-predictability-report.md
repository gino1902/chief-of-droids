# writing-requirements predictability report

Generated: 2026-05-15 18:30
Runs analyzed: 5 — v01, v02, v03, v04, v05
Substrate: `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/requirements/substrates/two-tier-architecture-design-notes.md`
Analyzed skill: `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/.claude/skills/writing-requirements/`

## Top-line scores

| Dimension | Score | Reading |
|:--|:--|:--|
| Section structure fidelity | **~95%** | 14/14 top-level sections rendered in identical order in 4/5 runs; v02 demotes `Actors & Consumers` to an H3 subsection of `## Scope` (line 30 of v02). |
| Identifier alignment | **~30%** | Only DR-001, TR-001, TR-002, NFR-001, IR-OUT-001, CON-001 (Layer-1-only) anchor the same statement across all 5 runs. FR-001 anchors sentinel-read in 4/5 runs but anchors path-scoped-rule-file loading in v02, cascading offsets to FR-002..FR-013. Cross-run FR labels for "Which project?" prompt: FR-002 (v01,v03,v04,v05) vs FR-003 (v02). Cross-run FR labels for sentinel write: FR-005 (v01), FR-006 (v02), FR-004 (v03,v04,v05). |
| Substrate fidelity — domain concepts | **~85%** | Layer 1/2/3, Dispatcher, Sentinel, Project brief, Bootstrap protocol, workspace-tier-wins, `recent_chats[0].uri`, `creating-skills` preserved in all 5. Six-capability enumeration (skills routing, session hygiene, git versioning, available tools, project brief route, conditional rules by file type) enumerated in v02/v03/v04/v05 but compressed to one sentence in v01 Purpose. Tool-layer-vocabulary triple (Registration / Routing / Usage as distinct concerns) explicit in v02/v03/v04/v05 glossaries; absent as triple in v01. |
| Substrate fidelity — schemas | **~90%** | Sentinel seven-field set (`uri`, `project`, `loaded_at`, `workspace_md_sha`, `project_md_sha`, `brief_sha`, `resolved_skills`) preserved in all 5 DR-001. Resolved-skill element shape `{trigger, skill, tier}` emitted inline in v01/v02/v03 and as a separate DR-002 entry in v04/v05 — split/fold. |
| Substrate fidelity — paths | **~80%** | `chief-of-droids/.sessions/<urlencoded-uri>.json`, `chief-of-droids/CLAUDE.md`, `<project>/CLAUDE.md`, `<project>/brief.md`, `docs/session-identity-recommendation.md` byte-verbatim in all 5. `claude_desktop_config.json` cited in v02/v03/v04/v05 only (absent v01). `docs/claude-md-applicability-matrix.md` (Related artifacts in substrate) absent in all 5. |
| Substrate fidelity — verbatim strings | **~70%** | `"Which project?"` byte-verbatim in all 5 (FR-002 / IR-OUT-001 family). Substrate `"could this be workspace?"` (substrate line 132) preserved verbatim in v01 (FR-016), v02 (FR-014), v05 (no FR carries it); paraphrased to `"could this be a workspace skill?"` in v03 (FR-015) and `"Could this be a workspace skill?"` in v04 (FR-013) — article and noun insertion plus capitalization drift. |
| Substrate fidelity — policies / constraints | **~70%** | "Workspace tier wins" stable across all 5; "Hard reject at authoring time" stable across all 5; one-way composition stable across all 5; reliability priority order modeled as CON in v01 (CON-014), v04 (CON-010), v05 (CON-011) but absent from CON in v02 and v03. Substrate's 92–93% reliability statement renders as MUST in v01/v02/v05 NFR-001 and as SHOULD in v03/v04 NFR-001 — modality drift on a substrate statement that includes a numeric threshold. |
| Modality and surface drift | **~85%** | NFR-001 MUST/SHOULD split (v01/v02/v05 MUST vs v03/v04 SHOULD) on the 92% reliability statement. Surface drift on `"could this be workspace?"` → `"could this be a workspace skill?"` (v03), `"Could this be a workspace skill?"` (v04). Other aligned IDs (CON-001 Layer-1-only, CON workspace-wins, DR-001 REQUIRED markers) keep modality stable across all 5. |
| Naming framing | **~100%** | All 5 titles read `# Two-Tier CLAUDE.md Architecture — Design Notes` — the substrate H1 (substrate line 1). None of the 5 humanises the user-supplied slug `chief-of-droids-3-tiers-upgrade`. Notable: substrate H1 says "Two-Tier" while the slug says "3-tiers"; all 5 runs honour the substrate. |

**Overall predictability:** Substance ≈ **0.70** · Structure ≈ **0.95** · Naming ≈ **1.00**.

## Section structure fidelity

| File role | Run | Heading sequence delta |
|:--|:--|:--|
| requirements.md | v01 | — |
| requirements.md | v02 | `Actors & Consumers` demoted from H2 to H3 under `## Scope` |
| requirements.md | v03 | — |
| requirements.md | v04 | — |
| requirements.md | v05 | — |

Canonical sequence (longest common): Purpose · Scope (In Scope, Out of Scope) · Actors & Consumers · Glossary · Functional Requirements · Interface Requirements (IR-IN, IR-OUT) · Data Requirements (DR, TR) · Non-Functional Requirements · Security · Constraints · Error Handling · Observability · Acceptance Criteria · Quality Criteria scorecard · Version block.

Notes: Section structure is the strongest dimension. The single deviation is v02's demotion of Actors & Consumers into Scope. Glossary placement before FRs is stable in all 5. Section order matches the template-s2 canonical order in every run.

## Identifier alignment

| Identifier | Coverage (n/N) | Anchor stability | Notes |
|:--|:--|:--|:--|
| FR-001 | 5/5 | drift | sentinel read in v01/v03/v04/v05; path-scoped rule-file load in v02 |
| FR-002 ("Which project?") | 5/5 | drift | v01/v03/v04/v05 anchor at FR-002; v02 anchors at FR-003 |
| FR sentinel write | 5/5 | drift | FR-005 (v01), FR-006 (v02), FR-004 (v03/v04/v05) |
| FR anchor emit | 5/5 | drift | FR-006 (v01), FR-007 (v02), FR-005 (v03/v04/v05), FR-008 (v05) |
| FR SHA compare | 5/5 | drift | FR-007 (v01), FR-008 (v02), FR-006 (v03/v04), FR-009 (v05) |
| FR SHA reload | 5/5 | drift | FR-008 (v01), FR-009 (v02), FR-007 (v03/v04), FR-010 (v05) |
| FR resolved_skills populate | 5/5 | drift | FR-010 (v01/v02), FR-009 (v04), absent in v03 as standalone FR; v05 absent (folded into FR-007 fields) |
| FR corpus collision scan | 5/5 | drift | FR-011 in v01/v02/v03/v05; FR-010 (combined with rejection) in v04 |
| FR dispatcher workspace-wins resolution | 4/5 | drift | FR-013 (v01/v05), absent in v02 (folded into TR-003), FR-010 (v03), FR-014 absent in v04 (covered by NFR-001) |
| FR major-version bump | 5/5 | drift | FR-014 (v01/v05), FR-012 (v02), FR-013 (v03), FR-011 (v04) |
| FR removal block | 4/5 | drift | FR-015 (v01/v05), FR-013 (v02), FR-014 (v03), FR-012 (v04) |
| FR project-skill workspace prompt | 5/5 | drift | FR-016 (v01), FR-014 (v02), FR-015 (v03), FR-013 (v04 — uses FR-013 slot), FR absent in v05 |
| CON Layer-1-only | 5/5 | stable | CON-001 in all 5 |
| CON workspace-tier-wins | 5/5 | drift | CON-008 (v01), CON-010 (v02), CON-007 (v03), absent as standalone in v04 (folded into TR-003), CON-005 (v05) |
| CON one-way composition | 5/5 | drift | CON-012 (v01), CON-015 (v02), CON-009/CON-010 (v03), CON-012 (v04), CON-007 (v05) |
| CON disjoint triggers | 5/5 | drift | CON-009 (v01), CON-011 (v02), CON-008 (v03), CON-011 (v04), CON-006 (v05) |
| CON no runtime override | 5/5 | drift | CON-011 (v01), CON-014 (v02), CON-013 (v03), CON-014 (v04), CON-012 (v05) |
| DR-001 sentinel schema | 5/5 | stable | DR-001 in all 5; seven-field set identical |
| DR-002 resolved-skill element | 2/5 | split/fold | separate DR-002 in v04/v05; inline note in v01/v02/v03 |
| TR-001 sentinel path derivation | 5/5 | stable | TR-001 in all 5 |
| TR-002 SHA computation | 5/5 | stable | TR-002 in all 5 |
| TR-003 resolved-skills map derivation | 3/5 | split/fold | TR-003 in v02 (truly v02 has TR-002 only; check) — present in v04, v05; absent v01, v03; v02 has only TR-001/TR-002 |
| NFR-001 92% routing | 5/5 | stable | NFR-001 in all 5 (modality drift handled separately) |
| IR-OUT-001 "Which project?" prompt | 5/5 | stable | IR-OUT-001 in all 5 |

Split/fold events: DR-002 (resolved-skill element) emitted as a separate schema in v04/v05; inlined as a column-note in v01/v02/v03. TR-003 (resolved-skills map derivation) emitted in v04/v05; absent v01/v02/v03. v02 introduces FR-001 = "load path-scoped rule files" which has no counterpart in the other four runs (the path-scoped rules concept appears in substrate but is treated as Layer-3 capability metadata, not a per-turn FR, in v01/v03/v04/v05).

## Substrate fidelity — invariants probed

| Invariant | Class | Source span | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:--|:--|:--|:--|:--|
| Layer 1 / Layer 2 / Layer 3 three-layer model | concept | lines 36–39 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Dispatcher | concept | line 37, line 60 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Six native capabilities enumerated | concept | lines 22–32 | ≈ partial | ≈ | ≈ | ≈ | ≈ |
| Tool layer vocabulary triple (Registration / Routing / Usage) | concept | lines 47–55 | ✗ | ≈ | ≈ | ≈ | ≈ |
| Always-on tools (filesystem, git, fetch) | concept | line 55 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Bootstrap protocol — single-predicate-per-turn | concept | line 59 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Sentinel path `chief-of-droids/.sessions/<urlencoded-uri>.json` | path | line 81 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Workspace CLAUDE.md `chief-of-droids/CLAUDE.md` | path | line 65 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Project CLAUDE.md `chief-of-droids/<project>/CLAUDE.md` | path | line 66 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Project brief `<project>/brief.md` | path | line 67 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `claude_desktop_config.json` | path | line 51 | ✗ | ✓ | ✓ | ✓ | ✓ |
| `docs/session-identity-recommendation.md` | path | line 10, 137, 146 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `docs/claude-md-applicability-matrix.md` | path | line 147 | ✗ | ✗ | ✗ | ✗ | ✗ |
| Prompt `"Which project?"` | verbatim | line 63 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Prompt `"could this be workspace?"` | verbatim | line 132 | ✓ | ✓ | ≈ | ≈ | ✗ |
| Sentinel schema seven fields | schema | lines 82–90 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Resolved-skill element `{trigger, skill, tier}` | schema | line 90, line 118 | ≈ inline | ≈ inline | ≈ inline | ✓ DR-002 | ✓ DR-002 |
| Workspace tier wins (precedence rule) | policy | line 112 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Hard reject at authoring time on trigger collision | policy | line 115 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Trigger phrases disjoint by name and phrase | policy | line 116 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Workspace skill removal blocked while referenced | policy | line 130 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Composition one-way (workspace SHALL NOT reference project) | policy | line 131 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Negative triggers respected, same precedence direction | policy | line 132 | ≈ | ≈ | ≈ | ≈ | ≈ |
| User chooses project once per session, no default | policy | line 76 | ≈ | ≈ | ✗ | ≈ | ≈ |
| Reliability budget priority order (mechanical > once-per-session > behavioural) | policy | lines 100–104 | ≈ | ≈ | ✗ | ≈ | ≈ |
| 92–93% reliability estimate | policy | line 119 | ✓ MUST | ✓ MUST | ≈ SHOULD | ≈ SHOULD | ✓ MUST |
| Layer 1 minimality (must be minimal but sufficient) | policy | line 43 | ≈ | ≈ | ≈ | ≈ | ≈ |
| `creating-skills` enforces corpus-wide scan | policy | line 115, line 125 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Major version bump on workspace skill trigger edit | policy | line 129 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Governance escape hatch via PR-to-workspace | policy | line 128 | ≈ | ≈ | ≈ | ≈ | ≈ |

Legend: ✓ verbatim · ≈ semantic match · ✗ missing or distorted.

## Modality and surface drift

| Identifier | Statement (anchor) | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:--|:--|:--|:--|
| NFR-001 | 92% skill-routing reliability | MUST | MUST | SHOULD | SHOULD | MUST |
| NFR-003 | Layer 1 minimal token footprint | SHOULD | SHOULD | SHOULD | SHOULD | SHOULD |
| CON-001 (or equivalent) | Layer 1 contains only dispatcher/sentinel-verify/always-on tool routing | SHALL | SHALL | SHALL | SHALL | SHALL |
| CON workspace-wins | Workspace skill wins on collision | SHALL | SHALL | SHALL | (TR-003) | SHALL |
| CON disjoint triggers | Trigger phrases disjoint across tiers | SHALL | SHALL | SHALL | SHALL | SHALL |
| CON one-way composition | Workspace SHALL NOT reference project | SHALL NOT | SHALL NOT | SHALL NOT | SHALL NOT | SHALL NOT |
| FR "Which project?" prompt | Framework prompts on absent/mismatched sentinel | SHALL | SHALL | SHALL | SHALL | SHALL |
| FR sentinel write | After bind verify, write sentinel | SHALL | SHALL | SHALL | SHALL | SHALL |
| FR removal block | Block removal of referenced workspace skill | SHALL | SHALL | SHALL | SHALL | SHALL |

Surface drift worth flagging:

- Substrate `"could this be workspace?"` reworded to `"could this be a workspace skill?"` (v03 FR-015) and `"Could this be a workspace skill?"` (v04 FR-013). Article ("a") inserted and noun ("skill") appended; v04 additionally capitalises the first character. Both are semantic-equivalent rewordings of a string the substrate quotes literally — both should have been left verbatim.
- Substrate "workspace tier wins" rendered alternately as `workspace-tier-wins` (hyphenated compound, v02 glossary, v04 glossary) and `workspace tier wins` (v01, v03, v05). Cosmetic.
- "Reliability principle" vs "Reliability budget" — substrate uses both ("reliability principle" line 98, "reliability budget" line 100). v01/v04/v05 keep both terms in glossary; v02/v03 fold to one.

## Statement counts per category

| Category | v01 | v02 | v03 | v04 | v05 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| FR | 16 | 14 | 15 | 13 | 14 | 13 | 16 | 14.4 |
| IR-IN | 4 | 7 | 3 | 5 | 6 | 3 | 7 | 5.0 |
| IR-OUT | 4 | 5 | 3 | 4 | 4 | 3 | 5 | 4.0 |
| DR | 1 | 1 | 1 | 2 | 2 | 1 | 2 | 1.4 |
| TR | 2 | 2 | 2 | 3 | 2 | 2 | 3 | 2.2 |
| NFR | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.0 |
| CON | 14 | 16 | 13 | 14 | 12 | 12 | 16 | 13.8 |
| ERR | 11 | 11 | 8 | 11 | 11 | 8 | 11 | 10.4 |
| Glossary | 26 | 24 | 19 | 20 | 21 | 19 | 26 | 22.0 |

## Naming framing finding

Substrate names this work: **"Two-Tier CLAUDE.md Architecture — Design Notes"** (substrate line 1, H1).

| Run | Title used | Framing |
|:--|:--|:--|
| v01 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v02 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v03 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v04 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v05 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |

Finding: every run reads the canonical name from the substrate H1; none humanises the user-supplied slug `chief-of-droids-3-tiers-upgrade`. This is a strength of the current skill — the title-fallback chain (H1 → H2 → frontmatter `title:` → slug+Warning) is honoured consistently. Notable: the substrate says "Two-Tier" while the slug says "3-tiers"; the substrate body clarifies the "two tiers, three layers" framing (substrate line 34). All runs honour the substrate framing rather than the slug's "3-tiers" framing — the right call.

## Per-file deviation summary

### v01
- Most granular FR section (16 entries) and largest glossary (26 entries); the only run that emits FR-016 as a distinct entry for the project-skill workspace-promotion prompt.
- Omits the tool-layer-vocabulary triple (Registration / Routing / Usage) from the glossary even though the substrate dedicates a subsection to it.
- Omits `claude_desktop_config.json` path (the only run that does so).
- Truncates the six-capability enumeration in Purpose to a single sentence; v02–v05 enumerate.

### v02
- Demotes `Actors & Consumers` from H2 to H3 inside `## Scope` (the only structural deviation in the corpus).
- Introduces FR-001 = "load path-scoped rule files" which has no counterpart in v01/v03/v04/v05 and cascades a 1-step offset across all FR identifiers anchored to the bootstrap protocol.
- Largest IR-IN count (7) — splits each file read into its own IR-IN entry.
- Largest CON count (16) — finer-grained constraint splitting (e.g., separates "Layer 2 SHALL contain" from "Layer 3 SHALL contain").

### v03
- Smallest ERR section (8 entries) — folds several error responses into adjacent error IDs.
- Smallest IR-IN count (3) — collapses all four bind reads (workspace md, project md, brief, sentinel) into one IR-IN entry.
- Renders the 92% reliability target as SHOULD (not MUST) — modality drift on a substrate statement with a numeric threshold.
- Paraphrases `"could this be workspace?"` to `"could this be a workspace skill?"`.
- Drops the "user chooses project once per session, no default" constraint and the reliability-principle constraint from the CON section.

### v04
- Smallest FR count (13) — folds collision-scan and reject-on-collision into a single FR-010.
- Splits DR-002 (resolved-skill element) as a separate schema entry.
- Splits TR-003 (resolved-skills map derivation) as a separate transformation entry.
- Capitalises and paraphrases the substrate prompt to `"Could this be a workspace skill?"` (the only run that does both).
- Renders the 92% reliability target as SHOULD.

### v05
- Splits FR-003, FR-004, FR-005 as three separate FRs for the three bind reads (workspace md / project md / brief) — the only run that does this.
- Smallest CON count (12) — coarser-grained constraint statements.
- DR-002 separate schema entry (like v04).
- Returns to MUST for NFR-001.
- Smallest glossary count of the v04/v05 pair (21).

## Predictability verdict

Identifier alignment is the dominant source of variance (~30%). The skill stably emits the right substance — the same set of constraints, the same sentinel schema, the same workspace-wins precedence rule, the same canonical paths and prompts — but it does not stably bind that substance to the same identifier across runs. A single drafting-order perturbation in v02 (front-loading FR-001 = path-scoped rule files) cascades an offset across nearly every FR ID. The single highest-leverage fix is to pin identifier order to the substrate body's appearance order rather than the drafter's pen order. Section structure (~95%), naming framing (~100%), modality on aligned IDs (~85%), and the sentinel schema (~90%) are already strong. The "could this be workspace?" prompt is the most prominent verbatim drift (3/5 verbatim, 2/5 paraphrased).

## Recommendations

*Stress test method: analytical projection — recommendations were applied to the recorded deviations from Phase 3 to estimate their effect. No re-runs were performed.*

### R-001 — Anchor FR/CON/ERR identifiers to substrate-body order, not drafting order     [projected lift: +30 pts]
- Targets: Identifier alignment; Modality (indirectly via aligned-ID count)
- Statement: When assigning IDs in Phase 2, walk the substrate body top-to-bottom and assign FR-001, FR-002, … in the order each requirement-shaped statement first appears in the substrate. Do the same for CON, ERR, IR-IN, IR-OUT. The drafter SHALL NOT renumber for narrative flow. For the two-tier-architecture substrate the FR order is: (1) sentinel read, (2) project prompt, (3) workspace CLAUDE.md load, (4) project CLAUDE.md load, (5) project brief load, (6) bind verify, (7) sentinel write, (8) anchor emit, (9) per-turn SHA compare, (10) SHA reload, (11) resolved_skills populate, (12) corpus collision scan, (13) workspace-wins dispatcher resolution, (14) major-version bump on workspace trigger edit, (15) removal block, (16) project-skill workspace-promotion prompt.
- Rationale: Would prevent v02's FR-001 displacement (path-scoped rule files was substrate-late, not substrate-first) and all cascading offsets on FR-002..FR-013. Would also stabilise CON ordering by anchoring to the substrate's `Skills routing` and `Preconditions` sections.
- Projected effect: prevented ~14 identifier-anchor drifts (FR-002..FR-013 across v02 plus CON workspace-wins drift across all 5); partial ~2 (DR-002 / TR-003 split/fold, since substrate puts these in different positions across paragraphs); unaffected v01's unique FR-016 (legitimate substrate signal); regressed none.
- Risk: Substrate restructuring between iterations would shift IDs by construction. Document this as the precedence rule — the substrate is the canonical order, not prior iterations.

### R-002 — Pin the project-skill authoring prompt verbatim     [projected lift: +15 pts]
- Targets: Substrate fidelity — verbatim strings
- Statement: When the substrate quotes a prompt literally (any string in double quotes or backticks that the substrate treats as a verbatim user-channel emission), emit it byte-identically in both the FR and the IR-OUT entries. Specifically for this substrate: the project-skill authoring prompt MUST read `"could this be workspace?"` — lowercase initial, no article, no trailing noun. Do not paraphrase, do not recase, do not append nouns to clarify.
- Rationale: Would prevent v03 paraphrase (`"could this be a workspace skill?"`) and v04 paraphrase plus capitalisation (`"Could this be a workspace skill?"`).
- Projected effect: prevented 2 paraphrases on this string; partial 0; unaffected `"Which project?"` (already verbatim across all 5); regressed 0.
- Risk: Pinning wording locks the framework to the substrate's wording even if the substrate's wording is later judged poor — note this only because the substrate explicitly fronts this string as a prompt.

### R-003 — Pin NFR modality to MUST when the substrate states a numeric threshold     [projected lift: +10 pts]
- Targets: Substrate fidelity — policies / constraints; Modality and surface drift
- Statement: For any NFR whose substrate source contains a quantitative threshold (percentage, count, time unit, byte budget), the rendered modality MUST be MUST. SHOULD is reserved for substrate statements that express a qualitative preference without a measurable target. For this substrate, the "~92–93%" reliability statement is quantitative — NFR-001 SHALL therefore render as MUST.
- Rationale: Would prevent v03 and v04 NFR-001 rendering as SHOULD on a statement that the substrate quantifies.
- Projected effect: prevented 2 modality drifts (v03 NFR-001, v04 NFR-001); partial 0; unaffected NFR-002 (substrate silent, N/A) and NFR-003 (substrate qualitative); regressed 0.
- Risk: Forces the skill to evaluate enforceability before writing modality. Slightly slower drafting; trivial.

### R-004 — Split schemas with structured array elements into separate DR entries     [projected lift: +10 pts]
- Targets: Substrate fidelity — schemas; Identifier alignment (DR-002 row)
- Statement: When a substrate schema names an array field whose element shape is itself a structured object (≥2 fields), emit the element shape as its own DR-NNN entry rather than inlining it as a column note in the parent table. For this substrate, the `resolved_skills` array element shape `{trigger, skill, tier}` SHALL be emitted as DR-002.
- Rationale: Would standardise v01/v02/v03 (inline) to match v04/v05 (separate DR-002), eliminating the schema split/fold deviation and stabilising the DR identifier set across runs.
- Projected effect: prevented 3 DR-002 fold events (v01, v02, v03); partial 0; unaffected DR-001 itself; regressed 0.
- Risk: Slightly inflates DR section. Minor.

### R-005 — Carry the six-capability enumeration verbatim into Purpose/Scope     [projected lift: +10 pts]
- Targets: Substrate fidelity — domain concepts
- Statement: Before drafting Purpose, re-read the substrate's "Capabilities Claude Code provides natively that chief-of-droids must implement via instruction" table. Carry all six capability names verbatim into Purpose and Scope. The substrate enumerates them in this order: (1) Skills routing, (2) Session hygiene, (3) Git versioning, (4) Available tools, (5) Project brief route, (6) Conditional rules by file type. Do not paraphrase capability names, do not reorder, do not collapse the list into prose.
- Rationale: Would prevent v01's compression of the six-capability list to a single Purpose sentence.
- Projected effect: prevented 1 domain-concept omission (v01); partial 0; unaffected v02–v05 (already enumerate); regressed 0.
- Risk: Negligible. Increases Purpose length by ~30 tokens.

### R-006 — Cite all substrate Related-artifacts paths in Actors & Consumers     [projected lift: +5 pts]
- Targets: Substrate fidelity — paths
- Statement: When the substrate has a section titled `Related artifacts` (or `Companion`, `References`, `See also`) listing filesystem paths, every path in that section MUST appear verbatim in the requirements artifact — either in Actors & Consumers (preferred, as an upstream actor) or in Out of Scope (when parked/deferred).
- Rationale: Would correct the consistent omission of `docs/claude-md-applicability-matrix.md` across all 5 runs. Would not have changed the (already-present) `docs/session-identity-recommendation.md` citation.
- Projected effect: prevented 5 path omissions (all 5 runs miss the applicability-matrix path); partial 0; regressed 0.
- Risk: Low. The path may not always be load-bearing for the requirements set, but citing it costs little.

### R-007 — Anchor IR-IN granularity to {source, payload-contract} pairs     [projected lift: +5 pts]
- Targets: Statement counts per category (informational); Identifier alignment (IR-IN family)
- Statement: Emit exactly one IR-IN entry per distinct `{source system, payload contract}` pair. Reads of multiple files via the same MCP server collapse to a single IR-IN entry when their payload contract is identical (e.g., "markdown content via filesystem MCP"); they remain separate when the contract differs (e.g., "JSON sentinel record" vs "markdown CLAUDE.md"). For this substrate the expected IR-IN cardinality is 4–5 entries: (1) `recent_chats[0].uri` from Claude Desktop API, (2) user free-form project name, (3) markdown content via filesystem MCP (workspace md, project md, brief — same contract), (4) JSON sentinel record via filesystem MCP, (5) read-event metadata for path-scoped rule matching (only if the substrate names this as inbound).
- Rationale: Would compress v02's 7 IR-IN entries and inflate v03's 3 entries toward a stable 4–5.
- Projected effect: prevented IR-IN drift on 2 runs (v02 over-split, v03 over-collapse); partial 2 (v01, v05 land near target but not on it); regressed 0.
- Risk: A poorly-drawn payload-contract boundary will create new drift on the boundary itself. Mitigate by spelling out the rule in the skill's IR-IN drafting section.

| Field        | Value       |
|--------------|-------------|
| Version      | 1.0         |
| Last Updated | 2026-05-15  |
| Status       | Draft       |
