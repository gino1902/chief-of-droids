# bootstrapping-project predictability report

Generated: 2026-07-08 13:35
Runs analyzed: 6 — v01, v02, v03, v04, v05, v06
Substrate: scratchpad/substrate.md (taskflow brief, goal=code / sub-type=app fullstack) — **provenance note: this substrate file was removed after the audit; the path no longer resolves.** It was the taskflow project brief: a fullstack team task-tracking app (React frontend, Node/TypeScript backend, pnpm), organising work on boards that hold work items with a state (todo/doing/done), owner, and due date, with four constraints (no cross-feature imports, dependencies point inward, UTC timestamps, no secrets in the repo). Regenerate from that description to reproduce this audit.
Analyzed skill: .claude/skills/bootstrapping-project/ (renamed from project-bootstrapping; SKILL.md v1.4; claude-md.md v1.3, post-R-001)
Comparable artifacts: FRAMING.md, CLAUDE.md, settings.json, tree.md (captured project tree)
Non-comparable artifacts excluded: none

This is a re-audit after applying R-001 from the 2026-07-08 13:17 baseline report (pin the CLAUDE.md conventions to one bullet per FRAMING constraint, no tree-derived extras). Fresh runs were generated against the patched skill; the tree-capture step was also made deterministic (`git ls-files` after commit) so the prior capture-format artifact does not recur.

## Summary - Outputs Variance per Dimension

| Category | Actual | Projected | Comments |
|:--|:--|:--|:--|
| Structure | 0% | = | FRAMING (5 sections) and CLAUDE (5 sections) hold identical heading order in all 6; settings.json and tree.md are now byte-identical across all 6 (single md5 each). |
| Substrate fidelity | 0% | = | FRAMING Constraints block is byte-identical across all 6 (single md5), the five pnpm commands render byte-identical in every CLAUDE.md, and the three backend tier paths are verbatim everywhere. |
| Modality | 0% | = | CLAUDE.md conventions are now count-locked at 4 in every run; bullets 1/2/4 are byte-identical across all 6, bullet 3 verbatim in 5/6. R-001 eliminated the prior reword and count drift; no recommendation targets this dimension. |
| Naming | 0% | = | Every run titles FRAMING `FRAMING — taskflow`, titles CLAUDE `CLAUDE.md`, and renders domain folders kebab-case (`work-items`); no slug-literal framing. |
| Identifier | n/a | n/a | No `[A-Z]{1,5}-\d{2,4}` identifier scheme is emitted by this skill in any artifact across any run. |

Analysis produced by `claude-opus-4-8[1m]`. Variance is the inverse of the predictability score: `variance = 100% − stability_score`, computed per dimension per artifact, then aggregated with the same worst-of-artifact rule used everywhere else in this report. For multi-sub-dimension categories (Substrate fidelity), the stability score is the mean across sub-dimensions before inversion. Numbers are rounded to multiples of 5 to avoid false precision. Projected values apply the recommendations from §Recommendations analytically — no re-runs were performed.

## Top-line scores

Score is the worst-of across comparable artifacts. `Worst artifact` names the artifact producing it (`all` if tied at the same value across all comparable artifacts).

| Dimension | Worst artifact | Score | Reading |
|:--|:--|:--|:--|
| Section structure fidelity | all | **~100%** | FRAMING (Why, For whom, Success, Delivered, Constraints) and CLAUDE (Purpose, Stack, Structure, Commands, Conventions) keep identical heading order in all 6; settings.json and tree.md share a single md5 each. |
| Identifier alignment | n/a | **n/a** | No `[A-Z]{1,5}-\d{2,4}` identifiers appear in any artifact across any run. |
| Substrate fidelity — domain concepts | all | **~100%** | taskflow, board, work item, state/owner/due date, and the three backend tiers are present in every run (FRAMING + CLAUDE prose, tree folders). |
| Substrate fidelity — schemas | n/a | **n/a** | The substrate defines no schema block (json/yaml/table/field-list). |
| Substrate fidelity — paths | all | **~100%** | `entry-points/api/`, `domain/`, `data-access/` and the eight `src/` dirs render verbatim in CLAUDE.md and the (now byte-identical) tree across all six. |
| Substrate fidelity — verbatim strings | all | **~100%** | The five pnpm commands and the `.env` token render byte-identical in every CLAUDE.md and FRAMING.md. |
| Substrate fidelity — policies / constraints | all | **~100%** | All four Constraints are byte-identical in every FRAMING.md (single md5) and present as conventions with modality intact in every CLAUDE.md. |
| Modality and surface drift | CLAUDE.md | **~100%** | Conventions locked to 4 bullets in every run; bullets 1/2/4 byte-identical across all 6, bullet 3 verbatim in v02–v06. No modality inversion. The lone residual is v01 rendering constraint 3 imperative ("Store and transmit…") — a single-run surface variant that does not subtract per the rubric. |
| Naming framing | all | **~100%** | Every run reads "taskflow" from the substrate title and derives `boards`/`work-items` as kebab-case folders; no run interpreted a slug literally. |

**Overall predictability — current (measured, worst-of artifact):**   Substance ≈ **1.00** · Structure ≈ **1.00** · Naming ≈ **1.00** [all three tie at the top across every comparable artifact].
**Overall predictability — projected (after recommendations, analytical, worst-of artifact):** Substance ≈ **1.00** · Structure ≈ **1.00** · Naming ≈ **1.00** [no recommendation is warranted; all dimensions are at ceiling].

Per-artifact aggregate breakdown:

| Artifact | Substance | Structure | Naming |
|:--|:--|:--|:--|
| FRAMING.md | 1.00 | 1.00 | 1.00 |
| CLAUDE.md | 1.00 | 1.00 | 1.00 |
| settings.json | n/a | 1.00 | n/a |
| tree.md | 1.00 | 1.00 | 1.00 |

## Section structure fidelity

| Artifact | Run | Heading sequence delta |
|:--|:--|:--|
| FRAMING.md | v01–v06 | — (all six identical: goal stamp, H1 `FRAMING — taskflow`, user-owned blockquote, Why, For whom, Success, Delivered, Constraints) |
| CLAUDE.md | v01–v06 | — (all six identical: goal stamp, H1, Purpose, Stack, Structure, Commands, Conventions) |
| settings.json | v01–v06 | — (byte-identical, single md5) |
| tree.md | v01–v06 | — (byte-identical, single md5; deterministic `git ls-files` capture) |

Canonical sequence per artifact:

- **FRAMING.md:** goal stamp · H1 · user-owned blockquote · Why · For whom · Success · Delivered · Constraints
- **CLAUDE.md:** goal stamp · H1 · Purpose · Stack · Structure · Commands · Conventions
- **settings.json:** `permissions` → `defaultMode` → `ask`
- **tree.md:** `.claude/settings.json` · `.gitignore` · `apps/{boards,work-items}/{entry-points/api,domain,data-access}/.gitkeep` · `CLAUDE.md` · `FRAMING.md` · `src/{app,assets,components,config,features,testing,types,utils}/.gitkeep`

Notes: structure is fully locked. Unlike the 13:17 baseline, tree.md is now byte-identical across all six runs — the earlier flat-vs-nested difference was a capture-command artifact and was removed by committing before listing. The scaffolded set is unchanged from baseline (8 `src/` dirs incl. empty `features/`, `apps/{boards,work-items}` × three tiers).

## Identifier alignment

| Artifact | Identifier | Coverage (n/N) | Anchor stability | Notes |
|:--|:--|:--|:--|:--|
| — | — | — | — | No identifier scheme emitted by this skill in any artifact. |

Split/fold events: none.

## Substrate fidelity — invariants probed

| Invariant | Class | Artifact | Source span | v01 | v02 | v03 | v04 | v05 | v06 |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| Never import across feature modules | policy | FRAMING.md | L41 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Never import across feature modules | policy | CLAUDE.md | L41 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| domain tier must not import from entry-points | policy | FRAMING.md | L42 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| domain tier must not import from entry-points | policy | CLAUDE.md | L42 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| All timestamps stored/transmitted in UTC | policy | FRAMING.md | L43 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| All timestamps stored/transmitted in UTC | policy | CLAUDE.md | L43 | ≈ | ✓ | ✓ | ✓ | ✓ | ✓ |
| No secrets in repo / git-ignored `.env` | policy | FRAMING.md | L44 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| No secrets in repo / git-ignored `.env` | policy | CLAUDE.md | L44 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `pnpm install/dev/build/test/lint` | verbatim | CLAUDE.md | L32 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `.env` | verbatim | FRAMING.md + CLAUDE.md | L44 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `entry-points/api/`, `domain/`, `data-access/` | path | CLAUDE.md | L36–37 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `entry-points/api`, `domain`, `data-access` | path | tree.md | L36–37 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `src/{assets,components,…}` layout | path | CLAUDE.md + tree.md | L33–35 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| taskflow / board / work item | concept | FRAMING.md + CLAUDE.md | L5–7 | ≈ | ≈ | ≈ | ≈ | ≈ | ≈ |
| state (todo/doing/done), owner, due date | concept | FRAMING.md | L6–7 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| three-tier backend / fullstack | concept | CLAUDE.md + tree.md | L36–37 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Legend: ✓ verbatim · ≈ semantic match · ✗ missing or distorted · n/a invariant not expected in this artifact.

Notes: substrate fidelity is perfect. The four constraints are byte-verbatim in every FRAMING.md and, after R-001, are now carried into CLAUDE.md conventions verbatim as well — the only exception is v01's constraint 3 (`≈`, imperative rephrase of the declarative "All timestamps are stored and transmitted in UTC"). Every other constraint cell is a full byte match in every run.

## Modality and surface drift

Modality is keyed on the four constraint statements (no identifier scheme exists).

| Artifact | Statement (anchor) | v01 | v02 | v03 | v04 | v05 | v06 |
|:--|:--|:--|:--|:--|:--|:--|:--|
| CLAUDE.md | feature-import boundary | never | never | never | never | never | never |
| CLAUDE.md | domain must not import entry-points | must not | must not | must not | must not | must not | must not |
| CLAUDE.md | timestamps in UTC | declarative | declarative | declarative | declarative | declarative | declarative |
| CLAUDE.md | no secrets in repo | prohibitive | prohibitive | prohibitive | prohibitive | prohibitive | prohibitive |

No modality inversion in any run. Surface drift (semantic-equivalent, scoped to CLAUDE.md):

- Conventions bullet 3: v01 renders "Store and transmit all timestamps in UTC" (imperative) where v02–v06 keep the FRAMING wording "All timestamps are stored and transmitted in UTC". This is the sole surviving convention-wording variant. It traces to a self-conflicting phrase in the applied fix ("carried in imperative form using that constraint's own wording"); the two clauses disagree only for a declarative constraint. See §Recommendations note.
- Conventions bullets 1, 2, 4: byte-identical across all six runs — the prior reword variants (v04 "Frontend features are self-contained…", v06 "Compose them at the `app/` layer…") and the v03 fifth convention are gone.
- Purpose / Stack / Structure prose still paraphrases run-to-run (e.g., Stack "React with TypeScript" vs "React single-page app" vs "React"; Structure names features in v03/v06, calls them "empty until a feature arrives" in v01/v05). This is grounded narrative the skill generates fresh from FRAMING; it is expected variation, not a scored defect.

## Statement counts per category

### Artifact: FRAMING.md

| Category | v01 | v02 | v03 | v04 | v05 | v06 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| Success bullets | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.0 |
| Delivered bullets | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.0 |
| Constraints bullets | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4.0 |

### Artifact: CLAUDE.md

| Category | v01 | v02 | v03 | v04 | v05 | v06 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| Stack bullets | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.0 |
| Structure bullets | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2.0 |
| Commands | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5.0 |
| Conventions bullets | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4.0 |

### Artifact: settings.json

| Category | v01 | v02 | v03 | v04 | v05 | v06 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| `ask` rules | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1.0 |
| `deny` rules | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 |

### Artifact: tree.md

| Category | v01 | v02 | v03 | v04 | v05 | v06 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| Scaffolded leaf dirs (.gitkeep) | 14 | 14 | 14 | 14 | 14 | 14 | 14 | 14 | 14.0 |

The CLAUDE.md conventions count is now flat at 4 (was min 4 / max 5 at baseline, driven by v03's extra convention). No count swing remains anywhere.

## Naming framing finding

Substrate names this work: **"taskflow"** (source: substrate H1 `# taskflow — project brief`, L1, and bold `**taskflow**` at L5).

| Artifact | Run | Title used | Framing |
|:--|:--|:--|:--|
| FRAMING.md | v01–v06 | `FRAMING — taskflow` | substrate |
| CLAUDE.md | v01–v06 | `CLAUDE.md` (Purpose names "taskflow") | substrate |
| tree.md | v01–v06 | `# taskflow project tree` | substrate |

Finding: naming is fully stable, unchanged from baseline. Every run reads "taskflow" from the substrate, derives `boards`/`work-items` as kebab-case folders, and never treats a slug literally.

## Per-file deviation summary

### v01
- **CLAUDE.md:** only run to render conventions bullet 3 imperative ("Store and transmit all timestamps in UTC"); Stack "React (single-page)"; Structure notes features "empty until a feature arrives".
- **FRAMING.md:** Why keeps "state (todo / doing / done)" enumeration inline (longest FRAMING at 1308 bytes).
- **settings.json / tree.md:** byte-identical to all runs.

### v02
- **CLAUDE.md:** leanest FRAMING/CLAUDE pairing; Stack "React with TypeScript"; Structure reorders `components/`/`config/` before `assets/`.
- **FRAMING.md / settings.json / tree.md:** canonical.

### v03
- **CLAUDE.md:** Purpose "lightweight task tracker"; Stack qualifies frontend "feature-based under `src/features/`"; Structure names features `boards`, `work-items`. Conventions = 4 verbatim (prior 5th convention gone).
- **FRAMING.md / settings.json / tree.md:** canonical.

### v04
- **CLAUDE.md:** most-compressed Purpose (one clause); Stack "Node with TypeScript".
- **FRAMING.md / settings.json / tree.md:** canonical.

### v05
- **CLAUDE.md:** Purpose "light task tracker"; Stack "React + TypeScript … three-tier layout"; Structure "empty at bootstrap".
- **FRAMING.md:** Why "light task tracker where small teams…".
- **settings.json / tree.md:** canonical.

### v06
- **CLAUDE.md:** Stack drops per-tier TypeScript ("React" / "Node.js exposing a small REST API"); Structure names features `boards`, `work-items`.
- **FRAMING.md / settings.json / tree.md:** canonical.

### Non-comparable artifacts

none.

## Predictability verdict

After R-001 the corpus is at ceiling on every scored dimension: Substance 1.00, Structure 1.00, Naming 1.00, and Modality variance is 0% (down from 5%). The fix worked as projected — the CLAUDE.md conventions are now count-locked at 4 in every run with bullets 1/2/4 byte-identical and bullet 3 verbatim in five of six, so the prior reword variants and v03's fifth convention are eliminated. The deterministic tree capture also collapsed tree.md to a single md5. No recommendation is warranted. The only residual variance is sanctioned grounded prose (FRAMING "Why", CLAUDE "Purpose"/"Stack"/"Structure" narrative), which the skill is designed to generate fresh from FRAMING and which is not a predictability defect.

## Recommendations

*Stress test method: analytical projection — recommendations were applied to the recorded deviations from Phase 3 to estimate their effect. No re-runs were performed.*

No recommendation meets the inclusion bar (every scored dimension is at ceiling; the catalog refuses recommendations with combined projected lift below +5 points).

### Optional micro-refinement (not scored, below inclusion bar)

- **Resolve the imperative-vs-verbatim ambiguity in the applied fix.** The R-001 wording in `claude-md.md` reads "carried in imperative form using that constraint's own wording"; for a declarative constraint (constraint 3) these two clauses conflict, and v01 resolved it toward imperative while v02–v06 kept the verbatim wording. Tightening the instruction to "carry each Constraint verbatim; do not convert a declarative constraint to imperative" would remove the single surviving surface variant. Projected lift below +5 pts (the dimension is already ~100%), so it is logged here for transparency rather than ranked.

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-07-08 |
| Status       | Draft      |
