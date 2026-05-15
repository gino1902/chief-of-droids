# writing-requirements predictability report

Generated: 2026-05-15 (test run)
Runs analyzed: 5 — v01, v02, v03, v04, v05
Substrate: `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/requirements/substrates/two-tier-architecture-design-notes.md`
Analyzed skill: `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/.claude/skills/writing-requirements/`

## Top-line scores

| Dimension | Score | Reading |
|:--|:--|:--|
| Section structure fidelity | **~95%** | 21 of 22 top-level sections rendered identically and in order in 5/5 runs; one demotion in v02 (Actors & Consumers nested as `### Actors & Consumers` under `## Scope` instead of as a sibling `##`). |
| Identifier alignment | **~35%** | Only FR-011 (corpus collision scan) lands at the same ID anchoring the same statement in all 5 runs. Sentinel read drifts FR-001 (v01/v03/v04/v05) → FR-002 (v02). Sentinel write drifts across FR-005 / FR-006 / FR-004 / FR-004 / FR-007 in v01/v02/v03/v04/v05. Anchor emission drifts across FR-006 / FR-007 / FR-005 / FR-005 / FR-008. v04 introduces DR-002 and TR-003 absent from v01/v03/v05. v05 splits one substrate read action into FR-003/FR-004/FR-005 where v01/v03/v04 fold them. |
| Substrate fidelity — domain concepts | **~90%** | 13 substrate concepts (two-tier, three-layer, Bootstrap protocol, Sentinel, Project brief, Reliability principle, Workspace tier wins, Single-predicate-per-turn, Tool layer vocabulary, Always-on tools, six native capabilities, etc.) — 12 surface in 5/5; "conditional rules by file type" only surfaces as FR in v02 and as scope in v04, dropped from v01/v03/v05. |
| Substrate fidelity — schemas | **~60%** | S1 sentinel 7-field schema preserved in 5/5 (DR-001 in every run). S2 `{trigger, skill, tier}` element preserved in 5/5 (DR-002 in v04, v05; inline in v01, v02, v03). S3 (Architecture layer/slot/carries table at substrate L36-39) reproduced verbatim in 0/5 — every run paraphrases into prose or bullets. S4 (six-capability table at L24-31) reproduced verbatim in 0/5 — every run paraphrases. |
| Substrate fidelity — paths | **~85%** | `chief-of-droids/.sessions/<urlencoded-uri>.json`, `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, `chief-of-droids/<project>/brief.md`, `recent_chats[0].uri`, `docs/session-identity-recommendation.md` preserved in 5/5 byte-for-byte. `claude_desktop_config.json` mentioned in v02, v04, v05 only — dropped from v01 and v03. |
| Substrate fidelity — verbatim strings | **~55%** | `"Which project?"` preserved verbatim in 5/5. SHA field names `workspace_md_sha` / `project_md_sha` / `brief_sha` and `resolved_skills` preserved in 5/5. "Option 2, hardened" — 0/5. "Option 1" — 4/5 (absent in v01). `"could this be workspace?"` — preserved verbatim only in v01; v03 says `"could this be a workspace skill?"`, v04 says `"Could this be a workspace skill?"`, v02 and v05 omit the FR entirely. "92–93%" range — v01 says "≥ 92%", v04 says "approximately 92–93%", v02/v03/v05 collapse to "92%". |
| Substrate fidelity — policies / constraints | **~85%** | 9 modal statements (Layer 1 minimality, disjoint triggers, explicit project selection, one-way composition, negative-trigger precedence, reliability priority order, hard-reject on collision, removal block, major version bump). 7 preserved with consistent modality in 5/5; Layer 1 minimality appears as both SHALL (CON-001) and SHOULD (NFR-003) in every run — dual-shape coverage but inconsistent across categories. Reliability priority order surfaces as CON in v01, v04, v05 and as prose-only in v02, v03. |
| Modality and surface drift | **~70%** | NFR-001 routing-reliability statement is MUST in v01, v02, v05 and SHOULD in v03, v04 for the same 92% target. "could this be workspace?" prompt is FR-SHALL in v01, v03, v04 and absent in v02, v05. Spelling drift: v01 uses "behavioural"; v03, v04, v05 use "behavioral". v04 introduces TR-003 (resolution-map derivation) absent in v01/v03/v05. |
| Naming framing | **~100%** | Title in every run is exactly `# Two-Tier CLAUDE.md Architecture — Design Notes` — substrate H1 at L1. No run falls back to a slug-derived title; no run humanises the slug `chief-of-droids-3-tiers-upgrade-v0X`. |

**Overall predictability — current (measured):**   Substance ≈ **0.70** · Structure ≈ **0.95** · Naming ≈ **1.00**.
**Overall predictability — projected (after R-001..R-007, analytical):** Substance ≈ **0.80** · Structure ≈ **1.00** · Naming ≈ **1.00**.

## Section structure fidelity

| File role | Run | Heading sequence delta |
|:--|:--|:--|
| requirements.md | v01 | — |
| requirements.md | v02 | Actors & Consumers demoted from `##` to `### Actors & Consumers` and nested under `## Scope` |
| requirements.md | v03 | — |
| requirements.md | v04 | — |
| requirements.md | v05 | — |

Canonical sequence (longest common): `# title` · `## Purpose` · `## Scope` → `### In Scope` · `### Out of Scope` · `## Actors & Consumers` · `## Glossary` · `## Functional Requirements` · `## Interface Requirements` → `### Inbound (IR-IN)` · `### Outbound (IR-OUT)` · `## Data Requirements` → `### Data Requirements (DR)` · `### Transformation Requirements (TR)` · `## Non-Functional Requirements` · `## Security` · `## Constraints` · `## Error Handling` · `## Observability` · `## Acceptance Criteria` · `## Quality Criteria scorecard` · Version block.

Notes: 21 of 22 top-level sections appear at the same level and same position in 5/5 runs. The single deviation is v02 reframing Actors & Consumers as a sub-section of Scope. All other sections — including the always-on `## Security`, `## Observability`, and `## Quality Criteria scorecard` — are stable.

## Identifier alignment

| Identifier | Coverage (n/N) | Anchor stability | Notes |
|:--|:--|:--|:--|
| FR-001 | 5/5 | drift | "sentinel read" in v01/v03/v04/v05; "path-scoped rule load" in v02. |
| FR-002 | 5/5 | drift | "Which project? prompt" in v01/v03/v04/v05; "sentinel read" in v02. |
| FR-003 | 5/5 | drift | "load 3 bind files" in v01/v02/v03/v04; "load workspace CLAUDE.md only" in v05 (split). |
| FR-005 | 5/5 | drift | "write sentinel" v01; "verify three loaded" v02; "anchor emit" v03/v04; "load brief.md only" v05. |
| FR-006 | 5/5 | drift | "anchor emit" v01; "write sentinel" v02; "compare SHAs" v03/v04; "verify all three loaded" v05. |
| FR-011 | 5/5 | stable | "corpus collision scan executed" in all 5 runs. |
| FR-013 | 4/5 | drift | "workspace-first dispatch" in v01, v05; "block removal" in v04; "prompt could-this-be-workspace" in v04; absent as FR-013 in v02 (encoded only as CON-010). |
| FR-016 | 1/5 | (v01 only) | v01 carries FR-016 ("could this be workspace?" prompt). v03 places same content at FR-015; v04 places it at FR-013; v02 and v05 omit entirely. |
| DR-002 | 2/5 | split/fold | v04, v05 emit DR-002 (`resolved_skill` element). v01, v02, v03 fold into DR-001 notes. |
| TR-003 | 2/5 | split/fold | v02, v04 emit TR-003 (resolution-map derivation). v01, v03, v05 omit. |
| IR-IN-005, IR-IN-006, IR-IN-007 | 1–3/5 | split/fold | The "read three bind files" action is one IR in v01/v03, three in v02/v04/v05 with further IR-IN-006/007 for sentinel read and read-event metadata. |
| ERR-012, ERR-013, ERR-016 | 1–2/5 | split/fold | v04 emits ERR-012/013 (referenced-skill enumeration, no-response default). v01 emits ERR-016. v05 stops at ERR-011. |

Split/fold events: DR-002, TR-003, IR-IN read-list, ERR enumeration of optional handlers, FR pairing of "Which project?" with bind-action. Five distinct fold/split families across the corpus.

## Substrate fidelity — invariants probed

| Invariant | Class | Source span | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:--|:--|:--|:--|:--|
| `chief-of-droids/.sessions/<urlencoded-uri>.json` | path | L80 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/CLAUDE.md` | path | L66 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/<project>/CLAUDE.md` | path | L67 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `chief-of-droids/<project>/brief.md` | path | L68 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `recent_chats[0].uri` | path | L61, L82 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `docs/session-identity-recommendation.md` | path | L10, L137 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `claude_desktop_config.json` | path | L51 | ✗ | ✓ | ✗ | ✓ | ✓ |
| `"Which project?"` | verbatim | L63 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `"could this be workspace?"` | verbatim | L132 | ✓ | ✗ | ≈ "could this be a workspace skill?" | ≈ "Could this be a workspace skill?" | ✗ |
| "Option 2, hardened" | verbatim | L113 | ✗ | ✗ | ✗ | ✗ | ✗ |
| "Option 1" deferred-work mention | verbatim | L121 | ✗ | ✓ | ✓ | ✓ | ✓ |
| "~92–93%" reliability estimate | verbatim | L120 | ≈ "≥ 92%" | ≈ "≥ 92%" | ≈ "≥ 92%" | ≈ "92–93%" | ≈ "92%" |
| Sentinel 7-field schema | schema | L82-90 | ✓ | ✓ | ✓ | ✓ | ✓ |
| `{trigger, skill, tier}` element | schema | L90 | ≈ (inline) | ≈ (inline) | ≈ (inline) | ✓ DR-002 | ✓ DR-002 |
| Architecture layer/slot/carries table | schema | L36-39 | ✗ (paraphrased) | ✗ (paraphrased) | ✗ (paraphrased) | ✗ (paraphrased) | ✗ (paraphrased) |
| Six-capability native/loci table | schema | L24-31 | ✗ | ✗ | ✗ | ✗ | ✗ |
| "two-tier / three-layer" framing | concept | L34 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Bootstrap protocol concept | concept | L57 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Sentinel concept | concept | L78-90 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Project brief concept | concept | L92-96 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Reliability principle | concept | L98-108 | ✓ | ≈ (prose only) | ≈ (prose only) | ✓ | ✓ |
| Workspace-tier-wins | concept | L112-121 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Conditional rules by file type | concept | L31 | ✗ | ✓ FR-001 | ✗ | ≈ scope only | ✗ |
| Layer 1 minimality | policy | L43 | ✓ (CON+NFR dual) | ✓ (CON+NFR dual) | ✓ (CON+NFR dual) | ✓ (CON+NFR dual) | ✓ (CON+NFR dual) |
| Disjoint trigger phrases | policy | L119 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Explicit project selection (no default) | policy | L76 | ✓ | ✓ | ✓ | ✓ | ✓ |
| One-way composition | policy | L131 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Negative-trigger precedence | policy | L132 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Reliability priority order | policy | L100-104 | ✓ CON-014 | ≈ (prose) | ≈ (prose) | ✓ CON-010 | ✓ CON-011 |
| Hard-reject on collision | policy | L117 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Removal block | policy | L130 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Major version bump | policy | L129 | ✓ | ✓ | ✓ | ✓ | ✓ |

Legend: ✓ verbatim · ≈ semantic match · ✗ missing or distorted.

## Modality and surface drift

| Identifier | Statement (anchor) | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:--|:--|:--|:--|
| NFR-001 | skills-routing reliability ≥ 92% | MUST | MUST | SHOULD | SHOULD | MUST |
| NFR-003 | Layer 1 token footprint minimal | SHOULD | SHOULD | SHOULD | SHOULD | SHOULD |
| FR (sentinel read) | read sentinel keyed on uri | SHALL | SHALL | SHALL | SHALL | SHALL |
| FR (corpus collision scan) | execute corpus-wide scan | SHALL | SHALL | SHALL | SHALL | SHALL |
| FR (workspace removal block) | block removal while referenced | SHALL | SHALL | SHALL | SHALL | SHALL |
| FR (could-this-be-workspace prompt) | author prompt | SHALL | (absent) | SHALL | SHALL | (absent) |
| CON-005-ish (always-on tools L1) | filesystem/git/fetch at Layer 1 | SHALL | SHALL | SHALL | SHALL | SHALL |
| CON (Layer 1 only-bootstrap content) | dispatcher payload | SHALL | SHALL | SHALL | SHALL | SHALL |

Surface drift (semantic-equivalent rewordings worth flagging):
- "behavioural" (British) in v01 vs "behavioral" (American) in v03, v04, v05; v02 mixed.
- "Could this be a workspace skill?" (v04 capitalised) vs "could this be a workspace skill?" (v03 lowercase) vs `"could this be workspace?"` (v01 verbatim).
- "anchor message" (v02, v03, v05) vs "anchor confirmation" (v01) vs "load-confirmation anchor" (v04) — same role.
- "artefact" (v04, v05) vs "artifact" (v01, v02, v03).

## Statement counts per category

| Category | v01 | v02 | v03 | v04 | v05 | min | max | mean |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| FR | 16 | 14 | 15 | 13 | 15 | 13 | 16 | 14.6 |
| IR-IN | 4 | 7 | 3 | 5 | 6 | 3 | 7 | 5.0 |
| IR-OUT | 4 | 5 | 3 | 4 | 4 | 3 | 5 | 4.0 |
| DR | 1 | 1 | 1 | 2 | 2 | 1 | 2 | 1.4 |
| TR | 2 | 2 | 2 | 3 | 2 | 2 | 3 | 2.2 |
| NFR | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.0 |
| CON | 14 | 16 | 13 | 14 | 12 | 12 | 16 | 13.8 |
| ERR | 11 | 11 | 8 | 11 | 11 | 8 | 11 | 10.4 |
| Glossary entries | 26 | 25 | 21 | 24 | 22 | 21 | 26 | 23.6 |

## Naming framing finding

Substrate names this work: **"Two-Tier CLAUDE.md Architecture — Design Notes"** (source: substrate L1, H1).

| Run | Title used | Framing |
|:--|:--|:--|
| v01 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v02 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v03 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v04 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |
| v05 | Two-Tier CLAUDE.md Architecture — Design Notes | substrate |

Finding: every run reads its title verbatim from the substrate's H1. No run derives the title from the slug `chief-of-droids-3-tiers-upgrade-v0X` and no run humanises the slug. The `writing-requirements` skill's Phase 1 fallback ladder is operating correctly on this substrate; this dimension is at ceiling for the corpus and should not be a focus of further hardening.

## Per-file deviation summary

### v01
- Highest FR count (16) including FR-016 for the "could this be workspace?" prompt — the only run that carries the substrate's literal phrasing verbatim.
- Omits the "Option 1" deferred-work mention from §Out of Scope.
- Drops `claude_desktop_config.json` path reference (present in v02, v04, v05).
- Uses British spelling "behavioural" — outlier vs v03/v04/v05.

### v02
- Sole structural outlier: demotes `## Actors & Consumers` to `### Actors & Consumers` nested under `## Scope`.
- Reorders FR-001 to "path-scoped rule load" — only run that uplifts conditional-rules-by-file-type to FR-001.
- Splits IR-IN into 7 entries (the highest count); introduces IR-OUT-005 (collision rejection message) unique to this run.
- Drops the "could this be workspace?" prompt as a separate FR.

### v03
- Smallest output along most dimensions: 3 IR-IN, 3 IR-OUT, 8 ERR, 21 Glossary entries.
- Strictest with `<project>/rules/` directory enumeration in CON-004.
- Uses SHOULD modality on NFR-001 (vs MUST in v01/v02/v05).
- Does not surface the "conditional rules by file type" capability anywhere.

### v04
- Introduces DR-002 (resolved_skill element schema) and TR-003 (resolution-map derivation) explicitly — only one of two runs to do both.
- Largest §Glossary disambiguation effort.
- Uses SHOULD on NFR-001; introduces ERR-012, ERR-013 (longer ERR enumeration).
- Uses British "artefact" alongside American "behavioral".

### v05
- Splits the three bind-file reads into three separate FRs (FR-003, FR-004, FR-005) where v01/v02/v03/v04 fold them into one.
- Omits the "could this be workspace?" FR entirely.
- Drops the "Option 1" mention to §Out of Scope but lifts it to an explicit deferred-work bullet.
- Sentinel write lands at FR-007 (latest position in any run) due to the bind-read split.

## Predictability verdict

Identifier alignment is the dominant source of variance — only ~35% of FR/IR/DR/TR/ERR identifiers map cleanly across all 5 runs, because the skill assigns sequence numbers by emit-time order, not by substrate-statement order. The single highest-leverage fix is R-001 (lock ID assignment to substrate ordering), projected to lift identifier alignment from 35% to 60% and modality drift from 70% to 75% in one rule. Structure fidelity (95%) and Naming framing (100%) are already at or near ceiling and do not warrant further hardening. The combination of R-001 (IDs) + R-003 (verbatim tables) + R-004 (verbatim user strings) carries roughly two-thirds of the projected Substance lift; the rest are smaller polish moves.

## Recommendations

*Stress test method: analytical projection — recommendations were applied to the recorded deviations from Phase 3 to estimate their effect. No re-runs were performed.*

### R-001 — Lock FR/CON/ERR ID assignment to substrate top-to-bottom ordering     [projected lift: +25 pts]
- Targets: Identifier alignment, Modality and surface drift
- Statement: When assigning identifiers in Phase 2, walk the substrate body top-to-bottom and assign sequence numbers in the order each requirement-shaped statement first appears. Do not reorder identifiers for narrative flow or thematic grouping in the output. Document the substrate-order precedence rule in the skill prompt as the canonical assignment policy.
- Rationale: ID positional drift is the largest single deviation pattern — "sentinel read" sits at FR-001 in v01/v03/v04/v05 but FR-002 in v02; "write sentinel" sits at FR-004/005/006/007 across the corpus; "anchor emit" sits at FR-005/006/007/008. Anchoring to substrate order eliminates the positional coin flip.
- Projected effect: prevented (the ~8 FR/ERR ID drift events across v01–v05), partial (3–4 CON/IR alignment fold-or-split events), unaffected (Glossary count drift, Naming framing), regressed (none — substrate ordering is unambiguous in this corpus).
- Risk: when substrate is later restructured between iterations, all IDs shift in lockstep. Document the precedence and pair with a major-version bump policy for the requirements artefact when substrate ordering changes.

### R-003 — Mandatory verbatim reproduction of substrate tables     [projected lift: +25 pts]
- Targets: Substrate fidelity — schemas
- Statement: When the substrate carries a multi-row table that frames the architecture, the capability matrix, or another tabular invariant, the skill MUST reproduce the table verbatim (header row and all data rows) inside the §Constraints, §Data Requirements, or §Purpose section. Paraphrasing a substrate table into prose or bullets is a hard Warning. The reproduced table need not be the only treatment, but it must be present.
- Rationale: substrate's "Architecture — two tiers, three layers" 3-row table (L36-39) and "Capabilities Claude Code provides natively that chief-of-droids must implement via instruction" 6-row table (L24-31) are reproduced verbatim in 0/5 runs. Both tables carry the substrate's primary information axes; paraphrasing them loses the layer/slot/carries and capability/mechanism/locus pairings.
- Projected effect: prevented (S3, S4 schema fidelity across all 5 runs), partial (S2 `{trigger, skill, tier}` element representation), unaffected (S1 sentinel schema — already present in 5/5), regressed (none).
- Risk: increases output length; some readers may prefer prose summaries. Mitigated by allowing the prose paraphrase as an addition, not a replacement.

### R-004 — Pin verbatim user-channel strings with byte-identical casing     [projected lift: +15 pts]
- Targets: Substrate fidelity — verbatim strings
- Statement: Any string the substrate emits to a user channel (prompts, anchors, error messages, button labels, log lines) MUST be carried into FR statements and AC entries with byte-identical casing and punctuation, wrapped in backticks. Paraphrase, recasing, or addition/removal of surrounding words is a hard Warning. The skill MUST list these strings in a verbatim-strings table at the end of Phase 1 and reference them by anchor in subsequent phases.
- Rationale: `"could this be workspace?"` from substrate L132 is preserved verbatim only in v01; v03 emits `"could this be a workspace skill?"`, v04 emits `"Could this be a workspace skill?"`, and v02/v05 omit the prompt as an FR entirely. `"Which project?"` is preserved 5/5 by virtue of being a single-token prompt; longer prompts drift.
- Projected effect: prevented (V6 drift in 4 runs), partial (V7 percentage range vs scalar), unaffected (V1, V2, V3 — already stable in 5/5), regressed (none).
- Risk: aging — if the substrate's prompt wording is later relaxed, the skill's pin must update with it. Mitigated by re-extracting the verbatim set on every run rather than caching it.

### R-007 — Force explicit decision on each substrate-listed capability     [projected lift: +15 pts]
- Targets: Substrate fidelity — domain concepts, Statement counts per category
- Statement: When the substrate enumerates a capability list, six-item framework, or similar fixed-cardinality structure, the skill MUST emit at least one FR, CON, or IR entry per enumerated item — or an explicit `N/A — out of scope per substrate` note for that item. Silent omission of an enumerated item is a hard Warning surfaced in the Phase 4 closure line.
- Rationale: substrate's six-capability matrix (L24-31) names skills routing, session hygiene, git versioning, available tools, project brief route, conditional rules by file type. Path-scoped rules (item 6) surfaces as FR in v02 (FR-001), as §Scope in v04, and is absent from v01, v03, v05. The substrate's organising frame is partially lost in 3/5 runs.
- Projected effect: prevented (capability-presence drift), partial (the per-capability FR count is still variable), unaffected (Glossary, NFR count), regressed (could over-constrain when one capability legitimately has no requirement-shaped statement; the explicit-out-of-scope opt-out absorbs this).
- Risk: over-fits to substrates that enumerate; degenerate substrates without a capability list are unaffected by the rule and the skill behaves as today.

### R-002 — Pin modality keyword for NFR statements to substrate's own modal keyword     [projected lift: +15 pts]
- Targets: Modality and surface drift, Substrate fidelity — policies / constraints
- Statement: Modality on NFR statements is determined by the substrate's own modal keyword. If the substrate uses MUST or SHALL or imperative "is required to", emit MUST. If the substrate uses SHOULD or qualified language ("approximately", "around", "estimate", "target", "approximately N%"), emit SHOULD. If the substrate uses MAY or "may", emit MAY. The skill MUST surface the substrate modality choice as a Phase 1 finding before drafting any NFR.
- Rationale: NFR-001 (routing reliability ≥ 92%) flips MUST (v01, v02, v05) vs SHOULD (v03, v04) for the same target. Substrate L120 says "Reliability estimate: ~92–93%." — qualitative phrasing with no MUST/SHALL — so SHOULD is the substrate-derived choice. Pinning by substrate modality removes the coin flip.
- Projected effect: prevented (NFR-001 modality flip), partial (Layer 1 minimality dual-shape CON-SHALL + NFR-SHOULD coverage), unaffected (FR/CON modality which is already 5/5 stable), regressed (none).
- Risk: slightly slower output — the skill must read the substrate's modal keyword before writing each NFR. Mitigated by reading the substrate once in Phase 1 and caching modal-keyword spans.

### R-006 — One IR-IN entry per distinct path read     [projected lift: +10 pts]
- Targets: Identifier alignment, Statement counts per category
- Statement: Each filesystem read of a distinct path is its own IR-IN-NNN requirement. When the substrate names N distinct paths to be read at the same lifecycle event, emit N separate IR-IN entries — do not fold them into a single multi-path IR-IN. Likewise: each filesystem write of a distinct path is its own IR-OUT entry.
- Rationale: IR-IN count varies from 3 (v03) to 7 (v02) — the variance is whether the three bind reads count as one IR-IN or three. The same indecision causes v05 to split the bind-read action into FR-003, FR-004, FR-005 where v01/v03/v04 fold them. Pinning "one IR per distinct path" makes the count and the FR mapping predictable.
- Projected effect: prevented (IR-IN count variance, v05 FR-split), partial (DR-001 vs DR-001+DR-002 — schema fields are not paths), unaffected (Glossary, NFR), regressed (verbosity — lengthens IR-IN sections, lower information density per line).
- Risk: produces visually verbose IR-IN sections. Acceptable trade-off given the variance reduction.

### R-005 — Pin §Actors & Consumers as a top-level section     [projected lift: +5 pts]
- Targets: Section structure fidelity
- Statement: §Actors & Consumers is a top-level `##` section positioned between §Scope and §Glossary. It is never nested under §Scope and never relocated after §Glossary. If the substrate carries no actor signal, render §Actors & Consumers with `N/A — substrate silent on actors. Warning emitted.` rather than omitting or demoting the section.
- Rationale: v02 demotes Actors & Consumers to `### Actors & Consumers` nested under §Scope — the only structural deviation observed across 22 sections × 5 runs. One-line section-ordering rule prevents recurrence.
- Projected effect: prevented (v02's structural anomaly), partial (none), unaffected (v01/v03/v04/v05 — already stable), regressed (none).
- Risk: minimal; trades the rare nested form for an explicit positional rule.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
