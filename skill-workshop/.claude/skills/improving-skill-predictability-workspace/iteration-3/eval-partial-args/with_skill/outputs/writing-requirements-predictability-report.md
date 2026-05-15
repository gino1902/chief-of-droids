# writing-requirements predictability report

Generated: 2026-05-15 12:00
Runs analyzed: 5 — v01, v02, v03, v04, v05
Substrate: /Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/requirements/substrates/two-tier-architecture-design-notes.md
Analyzed skill: /Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/.claude/skills/writing-requirements

## Top-line scores

| Dimension | Score | Reading |
|:--|:--|:--|
| Section structure fidelity | **~95%** | 14/14 top-level sections present and ordered identically in 4/5 runs; v02 demotes "Actors & Consumers" from H2 to H3 under Scope. |
| Identifier alignment | **~55%** | Anchored IDs (FR-001 = sentinel read, DR-001 = sentinel record, TR-001 = sentinel-path derivation) stable in all 5 runs, but sentinel-write moves between FR-005 (v01), FR-006 (v02), FR-004 (v03/v04), FR-007 (v05); ERR counts span 8–11. |
| Substrate fidelity — domain concepts | **~100%** | All 13 substrate concepts (Layer 1/2/3, sentinel, bootstrap protocol, project brief, always-on tools, workspace-tier-wins precedence, resolved skills map, `creating-skills`, trigger collision, registration/routing/usage, one-way composition, negative triggers, reliability principle) present in every run. |
| Substrate fidelity — schemas | **~95%** | Sentinel-record 7-field schema preserved verbatim in all 5 runs; `resolved_skills` element shape preserved in all 5; v04/v05 promote it to a separate DR-002, v01/v02/v03 keep it inline — same field set either way. |
| Substrate fidelity — paths | **~100%** | All five substrate paths (`chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, `chief-of-droids/<project>/brief.md`, `chief-of-droids/.sessions/<urlencoded-uri>.json`, `claude_desktop_config.json`) appear byte-identical in every run. |
| Substrate fidelity — verbatim strings | **~70%** | `"Which project?"` preserved verbatim in all 5 runs; `recent_chats[0].uri` preserved verbatim in all 5; `"could this be workspace?"` (substrate L133) only verbatim in v01/v02 — v03 paraphrases to `"could this be a workspace skill?"`, v04 capitalizes to `"Could this be a workspace skill?"`, v05 omits the FR; "minimal but sufficient" verbatim only in v04. |
| Substrate fidelity — policies / constraints | **~90%** | Modal statements (workspace tier wins, disjoint triggers, no-default project, major-version-bump-on-trigger-edit, removal-block-while-referenced, one-way composition, negative-trigger precedence, PR-to-workspace governance, reliability budget order) all present in every run; only v03 omits the no-default-project CON. |
| Modality and surface drift | **~85%** | NFR-001 (skills-routing reliability ≥ 92%) flips between MUST (v01/v02/v05) and SHOULD (v03/v04); FR/CON modalities are stable at SHALL in all runs. |
| Naming framing | **~100%** | All 5 runs render the Title verbatim as substrate H1 `Two-Tier CLAUDE.md Architecture — Design Notes`; no run substitutes the slug `chief-of-droids-3-tiers-upgrade`. |

**Overall predictability — current (measured):**   Substance ≈ **0.85** · Structure ≈ **0.95** · Naming ≈ **1.00**.
**Overall predictability — projected (after R-001..R-007, analytical):** Substance ≈ **0.93** · Structure ≈ **1.00** · Naming ≈ **1.00**.

## Section structure fidelity

| File role | Run | Heading sequence delta |
|:--|:--|:--|
| `<slug>-requirements.md` | v01 | — |
| `<slug>-requirements.md` | v02 | `Actors & Consumers` demoted from H2 to H3 under `Scope` |
| `<slug>-requirements.md` | v03 | — (adds decorative `---` rules between H2 sections; no heading change) |
| `<slug>-requirements.md` | v04 | — |
| `<slug>-requirements.md` | v05 | — |

Canonical sequence (longest common): Purpose, Scope, Actors & Consumers, Glossary, Functional Requirements, Interface Requirements (IR-IN, IR-OUT), Data Requirements (DR, TR), Non-Functional Requirements, Security, Constraints, Error Handling, Observability, Acceptance Criteria, Quality Criteria scorecard.

Notes: structural drift is one heading-level demotion in one of five runs. No section was reordered, dropped, or relocated. Decorative horizontal rules in v03 do not affect the heading sequence.

## Identifier alignment

| Identifier | Coverage (n/N) | Anchor stability | Notes |
|:--|:--|:--|:--|
| FR-001 (sentinel read) | 5/5 | stable | All runs anchor FR-001 to "read sentinel keyed on `recent_chats[0].uri`". |
| FR-002 (`Which project?` prompt) | 5/5 | drift | v01/v04/v05 = FR-002; v02/v03 = FR-003. Same statement, different ID. |
| FR-003 (load three bind files) | 5/5 | drift | v01/v04 = FR-003 single statement; v02 = FR-004; v03 = FR-003; v05 splits to FR-003/004/005 (one FR per file). |
| FR-005/006/007 (sentinel write) | 5/5 | drift | v01 = FR-005; v02 = FR-006; v03 = FR-004; v04 = FR-004; v05 = FR-007. Same statement, four different IDs. |
| FR-008/007/005 (anchor emission) | 5/5 | drift | v01 FR-006; v02 FR-007; v03 FR-005; v04 FR-005; v05 FR-008. |
| FR-007/006/008/009 (SHA compare) | 5/5 | drift | v01 FR-007; v02 FR-008; v03 FR-006; v04 FR-006; v05 FR-009. |
| FR-008/009/007/010 (reload-on-mismatch) | 5/5 | drift | v01 FR-008; v02 FR-009; v03 FR-007; v04 FR-007; v05 FR-010. |
| FR-010 (populate `resolved_skills`) | 5/5 | drift | v01 FR-010; v02 FR-010; v03 implicit in FR-004; v04 FR-009; v05 embedded in FR-007. |
| FR-011 (corpus collision scan) | 5/5 | stable | All runs anchor to FR-011 with identical statement. |
| FR-013/010 (workspace-first resolution) | 4/5 | drift | v01 FR-013; v02 implicit in CON; v03 FR-010; v04 absent as FR (CON only); v05 FR-013. |
| FR-016/014/015/013 ("could this be workspace?" prompt) | 4/5 | drift | v01 FR-016; v02 FR-014; v03 FR-015; v04 FR-013; v05 absent. |
| DR-001 (Sentinel record) | 5/5 | stable | Identical 7-field shape in all runs. |
| DR-002 (resolved_skill element) | 2/5 | split | v04 and v05 split out as DR-002; v01/v02/v03 keep inline in DR-001 `resolved_skills` row. |
| TR-001 (sentinel path derivation) | 5/5 | stable | Identical anchor in all runs. |
| TR-002 (SHA computation) | 5/5 | stable | Identical anchor; v01/v04/v05 split into three rows by file, v02/v03 collapse. |
| TR-003 (resolved skills map derivation) | 2/5 | split | v02 and v04 add TR-003; v01/v03/v05 omit. |
| NFR-001 (routing reliability) | 5/5 | drift | Modality flips MUST↔SHOULD across runs (see Modality table). |
| CON-001 (Layer 1 minimality) | 5/5 | stable | Same anchor; all runs use SHALL. |

Split/fold events: DR-002 split (v04/v05 vs v01/v02/v03); TR-003 split (v02/v04 vs others); v05 fan-out of bind-load FR into three sibling FRs; v04 absorbs workspace-first-resolution into CON-only treatment.

## Substrate fidelity — invariants probed

| Invariant | Class | Source span | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:--|:--|:--|:--|:--|
| `Two-Tier CLAUDE.md Architecture — Design Notes` (H1) | verbatim | L1 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Layer 1 / Layer 2 / Layer 3 named tiers | concept | L33–43 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Bootstrap protocol (single-predicate-per-turn) | concept | L57–75 | ≈ | ≈ | ≈ | ≈ | ≈ |
| Sentinel 7-field schema | schema | L82–90 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `{trigger, skill, tier}` element shape | schema | L90 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/CLAUDE.md` | path | L37, L62 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/<project>/CLAUDE.md` | path | L39, L65 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/<project>/brief.md` | path | L66, L91 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/.sessions/<urlencoded-uri>.json` | path | L80 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `claude_desktop_config.json` | path | L52 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `docs/session-identity-recommendation.md` | path | L10, L137 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `"Which project?"` | verbatim | L64 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `recent_chats[0].uri` | verbatim | L62 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `"could this be workspace?"` (substrate L133) | verbatim | L133 | ✓ | ✓ | ✗ | ✗ | ✗ |
| "minimal but sufficient" | verbatim | L43 | ✗ | ✗ | ✗ | ✓ | ✗ |
| Workspace tier wins (precedence rule) | policy | L114 | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL |
| Trigger phrases disjoint by name and phrase | policy | L116 | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL |
| Hard reject at authoring time on collision | policy | L116 | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL |
| Major-version bump on trigger edit | policy | L128 | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL |
| Workspace skill removal blocked while referenced | policy | L129 | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL |
| One-way composition (workspace ⇏ project) | policy | L130 | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL |
| Negative triggers respected same direction | policy | L131 | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL | ✓ SHALL |
| User chooses project once / no default | policy | L76 | ✓ SHALL | ✓ SHALL | ✗ | ✓ SHALL | ✓ SHALL |
| Layer 1 must be minimal | policy | L43 | ✓ SHOULD | ✓ SHOULD | ✓ SHOULD | ✓ SHOULD | ✓ SHOULD |
| Reliability budget priority order | policy | L100–104 | ✓ SHALL | ≈ (not lifted to CON) | ✗ | ✓ SHALL | ✓ SHALL |
| Routing reliability ~92–93% | policy | L119 | ✓ MUST 92% | ✓ MUST 92% | ✓ SHOULD 92% | ✓ SHOULD 92% | ✓ MUST 92% |

Legend: ✓ verbatim · ≈ semantic match · ✗ missing or distorted.

## Modality and surface drift

| Identifier | Statement (anchor) | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:--|:--|:--|:--|
| NFR-001 | routing reliability ≥ 92% | MUST | MUST | SHOULD | SHOULD | MUST |
| NFR-003 | Layer 1 minimal token footprint | SHOULD | SHOULD | SHOULD | SHOULD | SHOULD |
| FR-001 | read sentinel | SHALL | SHALL | SHALL | SHALL | SHALL |
| FR (sentinel write) | write sentinel | SHALL | SHALL | SHALL | SHALL | SHALL |
| CON-001 / CON-002 | Layer 1 contents only | SHALL | SHALL | SHALL | SHALL | SHALL |
| CON (workspace tier wins) | precedence | SHALL | SHALL | SHALL | SHALL | SHALL |
| IR-IN-001 | accept `recent_chats[0].uri` | MUST | MUST | MUST | MUST | MUST |
| IR-OUT-001 | emit `"Which project?"` | SHALL | SHALL | MUST | SHALL | MUST |

Surface drift (semantic-equivalent rewordings worth flagging):
- IR-OUT prompt-emission modal flips between SHALL and MUST (v03/v05 use MUST; others SHALL) — same semantic, different RFC 2119 keyword.
- "anchor" rendered as "anchor message" (v02/v03/v04), "anchor confirmation" (v01/v05), and "anchor line" (v04). Same concept.
- "bind" rendered as both verb (all runs) and noun (v04, v05) — substrate uses both.
- v05 splits the load FR into three sibling FRs (one per file); other runs use a single FR with a three-path conjunction.

## Statement counts per category

| Category | v01 | v02 | v03 | v04 | v05 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| FR | 16 | 14 | 15 | 13 | 15 | 13 | 16 | 14.6 |
| IR-IN | 4 | 7 | 3 | 5 | 6 | 3 | 7 | 5.0 |
| IR-OUT | 4 | 5 | 3 | 4 | 4 | 3 | 5 | 4.0 |
| DR | 1 | 1 | 1 | 2 | 2 | 1 | 2 | 1.4 |
| TR | 2 | 3 | 2 | 3 | 2 | 2 | 3 | 2.4 |
| NFR | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.0 |
| CON | 14 | 16 | 13 | 14 | 12 | 12 | 16 | 13.8 |
| ERR | 11 | 11 | 8 | 11 | 11 | 8 | 11 | 10.4 |
| Glossary entries | 27 | 25 | 21 | 22 | 21 | 21 | 27 | 23.2 |

## Naming framing finding

Substrate names this work: **"Two-Tier CLAUDE.md Architecture — Design Notes"** (source: substrate H1, line 1).

| Run | Title used | Framing |
|:--|:--|:--|
| v01 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v02 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v03 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v04 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v05 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |

Finding: every run reads framing from substrate. None uses the user-supplied slug `chief-of-droids-3-tiers-upgrade-v0X` as the title. The H1 says "Two-Tier" while the slug says "3-tiers" — the substrate body explains the design uses two tiers across three layers, and v01 reports this explicitly in its Phase 1 report. The skill's Phase 1 framing rule (first H1 in substrate, then fallbacks) is operating correctly. Naming framing is the strongest dimension in this corpus.

## Per-file deviation summary

### v01
- Highest FR count (16) and largest Glossary (27 entries); most-detailed Phase 1–6 report with 37 warnings.
- Carries explicit Phase 1 note reconciling the "Two-Tier" H1 vs "3-tiers" slug; preserves substrate title verbatim.
- ERR sequence has intentional gaps at 006/009/012/013/015 with inline rationale per Emit/Select/rejection-shape opt-outs.

### v02
- Only structural deviation in the corpus: demotes `Actors & Consumers` from H2 to H3 under `Scope`.
- Largest IR-IN expansion (7 entries), pulling per-file reads (workspace CLAUDE.md, project CLAUDE.md, brief, sentinel) and the path-scoped-rules read-event into separate IRs.
- Adds TR-003 (resolved-skills-map derivation) and IR-OUT-005 (collision-rejection message); largest CON count (16).

### v03
- Lowest ERR count (8); lowest IR-IN/IR-OUT counts (3 each).
- Decorative horizontal rules `---` inserted between H2 sections — only run that does so.
- Paraphrases the substrate prompt as `"could this be a workspace skill?"` — only run with this drift; substrate text is `"could this be workspace?"`.
- Drops the explicit "no default project" CON.

### v04
- Most aggressive schema factoring: splits resolved-skill element into DR-002 and lifts skills-map derivation into TR-003.
- Capitalizes the substrate prompt as `"Could this be a workspace skill?"` — verbatim drift on a quoted string.
- Only run that quotes "minimal but sufficient" verbatim.
- Uses SHOULD on NFR-001 (routing reliability) — joins v03 in this modality flip.

### v05
- Splits bind-load into three sibling FRs (FR-003/004/005), one per file; all other runs use a single FR.
- Drops the "could this be workspace?" project-skill authoring prompt FR entirely — no equivalent FR present.
- Smallest Glossary (21 entries); lowest CON count (12); preserves DR-002 split from v04.
- Sentinel-write FR sits at FR-007 — the latest index across the corpus.

## Predictability verdict

The dominant source of variance is identifier alignment: even when every run carries the same statement set, the numbering drifts (sentinel-write FR ID, anchor-emission FR ID, and SHA-compare FR ID each shift across all 5 runs). Substrate-fidelity dimensions (concepts, paths, schemas, policies) are already near or at ceiling — the skill reliably preserves what the substrate says. Naming framing is at 100% — all 5 runs read title from substrate, not from slug. The single highest-leverage fix is to anchor IDs to substrate body order (R-001), which lifts identifier alignment from ~55% to ~80% and also tightens statement-count drift. Verbatim fidelity is the secondary leakage point — pinning the `"could this be workspace?"` prompt would close the largest remaining substrate-verbatim gap.

## Recommendations

*Stress test method: analytical projection — recommendations were applied to the recorded deviations from Phase 3 to estimate their effect. No re-runs were performed.*

### R-001 — Anchor identifiers to substrate body order     [projected lift: +25 pts]
- Targets: Identifier alignment, Statement counts per category
- Statement: When assigning IDs in Phase 2, walk the substrate body top-to-bottom and assign identifiers to requirement-shaped statements in the order they first appear in the substrate. Do not renumber for narrative flow or template layout. If a statement aggregates several substrate sentences, anchor the ID to the earliest sentence.
- Rationale: sentinel-write, anchor-emission, SHA-compare and reload-on-mismatch FR IDs drift across all 5 runs (FR-005 in v01, FR-006 in v02, FR-004 in v03, FR-004 in v04, FR-007 in v05 — for "sentinel write"). Anchoring by substrate body order would have collapsed this drift.
- Projected effect: prevented 12, partial 5, unaffected 8, regressed 0
- Risk: ordering rules may conflict when the substrate is restructured between iterations; document the precedence (substrate body order > template layout).

### R-002 — Pin "could this be workspace?" verbatim     [projected lift: +10 pts]
- Targets: Substrate fidelity — verbatim strings
- Statement: When the substrate quotes a prompt fragment in backticks or double quotes, the output must reproduce that fragment byte-for-byte. Do not recase, paraphrase, or wrap in additional words. If a substrate prompt has no corresponding FR in the active template, still surface the verbatim string in the rationale or glossary, never drop it.
- Rationale: substrate L133 reads `"could this be workspace?"`. v03 paraphrased to "could this be a workspace skill?", v04 capitalized to "Could this be a workspace skill?", v05 dropped the FR carrying this prompt entirely.
- Projected effect: prevented 3, partial 0, unaffected 0, regressed 0
- Risk: pinning wording may age poorly if substrate intent shifts; treat the verbatim as load-bearing only when the substrate itself quotes it.

### R-003 — Pin modality by enforceability     [projected lift: +10 pts]
- Targets: Modality and surface drift
- Statement: NFR / quantitative-measurement statements receive MUST if and only if a verifiable numeric threshold is declared in the substrate or derivable from it. SHOULD is reserved for qualitative thresholds (no numeric value). MAY is for explicit discretionary cases. The author does not select modality by preference.
- Rationale: NFR-001 (routing reliability ≥ 92%) carries a numeric substrate threshold yet is rendered MUST in v01/v02/v05 and SHOULD in v03/v04. Per the enforceability rule, the correct modality is MUST.
- Projected effect: prevented 2, partial 0, unaffected 0, regressed 0
- Risk: forces a modality-decision step before drafting NFR statements; small additional cost per NFR.

### R-004 — Lock DR/TR factoring     [projected lift: +5 pts]
- Targets: Substrate fidelity — schemas, Identifier alignment
- Statement: A schema element whose shape is explicitly named in the substrate (e.g., `{trigger, skill, tier}`) must be promoted to a sibling DR-NNN at the same level as its containing record. Likewise, a derivation rule that converts one schema to another receives its own TR-NNN. The decision is binary: substrate names the shape ⇒ promote; substrate does not name it ⇒ inline.
- Rationale: v04 and v05 split out DR-002 (resolved_skill element) and TR-003 (resolved-skills-map derivation), v01/v02/v03 inline both. The substrate explicitly names `{trigger, skill, tier}` and the derivation rule — per a clear factoring rule, both deserve dedicated IDs.
- Projected effect: prevented 4, partial 0, unaffected 0, regressed 0
- Risk: more IDs to maintain; a sparse schema may produce DR/TR entries that read as one-line restatements.

### R-005 — Fix bind-load FR factoring     [projected lift: +5 pts]
- Targets: Identifier alignment, Statement counts per category
- Statement: A single substrate sentence that lists multiple artefacts to be loaded in one operation produces one FR, not one FR per artefact. The artefacts are enumerated in the FR statement and in the matching IR-IN rows. Split into sibling FRs only when the substrate itself treats each load as a distinct operation with distinct preconditions.
- Rationale: v05 splits "load workspace CLAUDE.md, project CLAUDE.md, project brief" into FR-003, FR-004, FR-005 (one FR per file); v01/v02/v03/v04 use a single FR. Substrate L65-67 lists the three files as one bullet under "On user answer, load:" — a single load operation.
- Projected effect: prevented 1, partial 0, unaffected 0, regressed 0
- Risk: under-splitting may hide per-file failure modes; the ERR coverage protocol must still enumerate per-file load errors.

### R-006 — Require the project-skill promotion-prompt FR     [projected lift: +5 pts]
- Targets: Substrate fidelity — policies / constraints
- Statement: Every preconditional rule declared in the substrate (a numbered or bulleted list of conditions for the design to hold) must produce at least one requirement-shaped statement in the output. Conditions that prescribe a user-facing prompt produce an FR whose IR-OUT row carries the prompt verbatim.
- Rationale: substrate Precondition 9 ("Project-skill authoring asks 'could this be workspace?' — promotion > parallel") is rendered as an FR by v01/v02/v03/v04 and entirely dropped by v05.
- Projected effect: prevented 1, partial 0, unaffected 0, regressed 0
- Risk: forces complete coverage of the substrate's Preconditions section even when a precondition is governance-only; accept the small over-coverage cost.

### R-007 — Lock §Actors & Consumers at top-level H2     [projected lift: +5 pts]
- Targets: Section structure fidelity
- Statement: §Actors & Consumers is a top-level H2 in the output, never a child of §Scope. The framing produces three independent H2 sections: §Title+Purpose, §Scope, §Actors & Consumers — in that order.
- Rationale: v02 demoted Actors to H3 under Scope, the only structural deviation in the corpus. The skill's Phase 1 step "§Actors & Consumers" implies a separate section but does not pin the heading level.
- Projected effect: prevented 1, partial 0, unaffected 0, regressed 0
- Risk: rigid ordering may produce empty Actors sections when substrate is silent; accept this as the lesser cost (the template already prescribes `N/A` + Warning for absent signal).

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
