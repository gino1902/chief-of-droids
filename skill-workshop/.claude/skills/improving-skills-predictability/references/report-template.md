# Report template

Render exactly this structure. Replace bracketed tokens. Keep tables intact even if a row's value is `N/A`.

---

# [skill-name] predictability report

Generated: [YYYY-MM-DD HH:MM]
Runs analyzed: [N] — [list run identifiers, e.g., v01..v05]
Substrate: [substrate path]
Analyzed skill: [skill path]
Comparable artifacts: [list artifact keys]
Non-comparable artifacts excluded: [list or "none"]

## Summary - Outputs Variance per Dimension

| Category | Actual | Projected | Comments |
|:--|:--|:--|:--|
| Structure | [N]% | [N]% | [one sentence — worst-artifact evidence or locking factor; or recommendation IDs if Projected < Actual] |
| Substrate fidelity | [N]% | [N]% | [one sentence] |
| Modality | [N]% | [N]% | [one sentence] |
| Naming | [N]% | [N]% | [one sentence] |
| Identifier | [N]% | [N]% | [one sentence] |

Analysis produced by `[model-id]`. Variance is the inverse of the predictability score: `variance = 100% − stability_score`, computed per dimension per artifact, then aggregated with the same worst-of-artifact rule used everywhere else in this report. For multi-sub-dimension categories (Substrate fidelity), the stability score is the mean across sub-dimensions before inversion. Numbers are rounded to multiples of 5 to avoid false precision. Projected values apply the recommendations from §Recommendations analytically — no re-runs were performed.

## Top-line scores

Score is the worst-of across comparable artifacts. `Worst artifact` names the artifact producing it (`all` if tied at the same value across all comparable artifacts).

| Dimension | Worst artifact | Score | Reading |
|:--|:--|:--|:--|
| Section structure fidelity | [artifact] | **~X%** | [one-sentence evidence from the worst artifact — e.g., "M/M sections rendered identically in K/N runs of the requirements artifact; one demotion in vXX"] |
| Identifier alignment | [artifact] | **~X%** | [evidence citing IDs and runs in the worst artifact] |
| Substrate fidelity — domain concepts | [artifact] | **~X%** | [evidence — concepts and which runs preserve them in the worst artifact] |
| Substrate fidelity — schemas | [artifact] | **~X%** | [evidence — schema name and per-run preservation in the worst artifact] |
| Substrate fidelity — paths | [artifact] | **~X%** | [evidence — paths and verbatim status in the worst artifact] |
| Substrate fidelity — verbatim strings | [artifact] | **~X%** | [evidence — quoted strings and per-run preservation in the worst artifact] |
| Substrate fidelity — policies / constraints | [artifact] | **~X%** | [evidence — modality bundle in the worst artifact] |
| Modality and surface drift | [artifact] | **~X%** | [evidence — IDs whose modality changed across runs in the worst artifact] |
| Naming framing | [artifact] | **~X%** | [evidence — does the title read from substrate or from slug in the worst artifact?] |

**Overall predictability — current (measured, worst-of artifact):**   Substance ≈ **0.XX** · Structure ≈ **0.XX** · Naming ≈ **0.XX** [worst artifact(s): <list>].
**Overall predictability — projected (after R-001..R-NNN, analytical, worst-of artifact):** Substance ≈ **0.XX** · Structure ≈ **0.XX** · Naming ≈ **0.XX**.

Per-artifact aggregate breakdown:

| Artifact | Substance | Structure | Naming |
|:--|:--|:--|:--|
| [artifact-1] | 0.XX | 0.XX | 0.XX |
| [artifact-2] | 0.XX | 0.XX | 0.XX |
| … | … | … | … |

## Section structure fidelity

| Artifact | Run | Heading sequence delta |
|:--|:--|:--|
| [artifact-1] | v01 | [list of insertions / deletions / reorderings vs. canonical, or "—"] |
| [artifact-1] | v02 | … |
| [artifact-2] | v01 | … |
| … | … | … |

Canonical sequence per artifact:

- **[artifact-1]:** [ordered list]
- **[artifact-2]:** [ordered list]

Notes: [1–3 sentences on the most material structural deviations, noting per-artifact differences if they diverge].

## Identifier alignment

| Artifact | Identifier | Coverage (n/N) | Anchor stability | Notes |
|:--|:--|:--|:--|:--|
| [artifact] | [ID-001] | n/N | stable / drift / split | [evidence] |
| … | … | … | … | … |

Split/fold events: [list (artifact, IDs) where one run's ID maps to multiple in another, or "none"].

## Substrate fidelity — invariants probed

One row per (invariant, artifact) cell. An invariant that the analyzed skill never surfaces in a given artifact across any run is annotated `n/a` rather than `✗` and is excluded from that artifact's denominator.

| Invariant | Class | Artifact | Source span | v01 | v02 | v03 | v04 | v05 | … |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| [verbatim or paraphrased anchor] | path / schema / verbatim / concept / policy | [artifact] | [substrate line range or section] | ✓ / ≈ / ✗ / n/a | … | … | … | … | … |

Legend: ✓ verbatim · ≈ semantic match · ✗ missing or distorted · n/a invariant not expected in this artifact.

## Modality and surface drift

| Artifact | Identifier | Statement (anchor) | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:--|:--|:--|:--|:--|
| [artifact] | [ID] | [short anchor of the statement] | MUST | SHOULD | MUST | MUST | MAY |

Surface drift (semantic-equivalent rewordings worth flagging, scoped per artifact): [bullet list or "none"].

## Statement counts per category

One table per comparable artifact.

### Artifact: [artifact-1]

| Category | v01 | v02 | v03 | v04 | v05 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| [category] | n | n | n | n | n | n | n | n.n |
| … | … | … | … | … | … | … | … | … |

### Artifact: [artifact-2]

| Category | v01 | v02 | v03 | v04 | v05 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| [category] | n | n | n | n | n | n | n | n.n |
| … | … | … | … | … | … | … | … | … |

(Repeat per comparable artifact.)

## Naming framing finding

Substrate names this work: **"[canonical name from substrate]"** (source: [substrate location]).

| Artifact | Run | Title used | Framing |
|:--|:--|:--|:--|
| [artifact-1] | v01 | [title] | substrate / slug-literal / hybrid |
| [artifact-1] | v02 | … | … |
| [artifact-2] | v01 | … | … |
| … | … | … | … |

Finding: [one paragraph — whether runs read framing from substrate or from slug, with per-artifact notes if artifacts diverge; cite contrary evidence if the original premise was wrong].

## Per-file deviation summary

For each run, list 1–3 lines per artifact. At minimum, one line per (dimension, artifact) where this run is the outlier.

### v01

- **[artifact-1]:** [1–3 lines on what is distinctive about this run's file in this artifact]
- **[artifact-2]:** …

### v02

- **[artifact-1]:** …
- **[artifact-2]:** …

(Continue for every run.)

### Non-comparable artifacts

[List any artifacts present in < ⌈N/2⌉ runs, with the run identifiers where they appear, or "none". Excluded from scoring per SKILL.md Phase 0 comparability filter.]

## Predictability verdict

[Two to four sentences. State which (dimension, artifact) cell is the dominant source of variance, name the single highest-leverage fix, and note any (dimension, artifact) cell where runs are already at ≥95%. If the worst artifact differs across Substance / Structure / Naming, name each worst artifact explicitly.]

## Recommendations

*Stress test method: analytical projection — recommendations were applied to the recorded deviations from Phase 3 to estimate their effect. No re-runs were performed.*

### R-001 — [one-line title]     [projected lift: +N pts]
- Targets: [(dimension, artifact) cells, or "dimension X across all artifacts"]
- Statement: [imperative, one or two sentences]
- Rationale: [which observed deviations it would have prevented]
- Projected effect: prevented [A], partial [B], unaffected [C], regressed [D]
- Risk: [one sentence]

### R-002 — …

(Continue in ranked order. Highest projected lift first.)

| Field        | Value       |
|--------------|-------------|
| Version      | 1.2         |
| Last Updated | 2026-05-16  |
| Status       | Draft       |
