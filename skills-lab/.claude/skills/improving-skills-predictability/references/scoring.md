# Scoring rubric

Convert raw findings into per-dimension percentages, rounded to multiples of 5. Avoid false precision — the analytical projection is itself approximate.

## Artifact scoping

Every per-dimension formula below is applied **per comparable artifact independently** (comparable artifacts are defined in SKILL.md Phase 0; non-comparable artifacts are excluded entirely). The top-line score for each dimension is the **minimum across comparable artifacts** (worst-of). The detail sections report the full per-artifact breakdown.

For a skill whose runs produce exactly one artifact, every dimension's "worst-of" collapses to that single artifact's score; the contract is identical to the single-axis case.

## General formula

For each (dimension, artifact) cell, score = `100 * (preserved_items / total_items)`, rounded to the nearest 5%, with the following adjustments:

- `preserved_items` = full matches.
- Partial matches (semantic but not verbatim where verbatim was required) count as 0.5.
- An item present in fewer than 60% of the runs that carry this artifact counts as 0 for that (dimension, artifact).

## Per-dimension rules

### Section structure fidelity

Per artifact:

- `total_items` = max heading count across the runs that carry this artifact.
- `preserved_items` = headings that appear in the same position in every run carrying this artifact.
- A demoted or promoted heading (level changed but text stable) counts as 0.5.
- A reordered heading counts as 0.

### Identifier alignment

Per artifact:

- `total_items` = union of identifiers found in this artifact across runs.
- `preserved_items` = identifiers present in every run for this artifact AND anchoring the same statement (semantic match) in every run.
- Split/fold events count as 0.5 (the meaning is preserved but the IDs are not).

### Substrate fidelity — domain concepts

Per artifact:

- `total_items` = number of distinct concepts extracted in Phase 2 that the analyzed skill is expected to surface in this artifact. A concept never expected in an artifact is excluded from that artifact's denominator (annotated `n/a` in the report) rather than counted as a miss.
- Concepts must be present in every run carrying this artifact; semantic paraphrase is allowed.

### Substrate fidelity — schemas

Per artifact:

- `total_items` = number of schema blocks in the substrate that the analyzed skill is expected to surface in this artifact.
- A schema preserves credit only if all fields are present in the same artifact; renamed fields count as 0.5 if the renamed name is consistent across runs, 0 if not.

### Substrate fidelity — paths and verbatim strings

Per artifact. Byte-level equality required. No partial credit.

### Substrate fidelity — policies / constraints

Per artifact:

- `total_items` = number of modal statements in the substrate expected in this artifact.
- Full match = present + same modality keyword.
- Same statement, different modality = 0.5.
- Missing = 0.

### Modality and surface drift

Per artifact:

- `total_items` = number of aligned identifiers in this artifact from Identifier alignment.
- `preserved_items` = identifiers in this artifact whose modality keyword is identical across all runs carrying the artifact.
- Surface drift (semantic-equivalent rewordings) does not subtract score but is noted in the report.

### Naming framing

Per artifact:

- Binary by run: each run's file in this artifact is either "reads substrate" (1) or "reads slug literally" (0). Hybrid = 0.5.
- Per-artifact score = average across runs that carry this artifact, rounded to nearest 5%.

Top-line score = minimum across comparable artifacts.

## Combine across artifacts

For every dimension above, the top-line value reported in the Phase 4 score table is `min over comparable artifacts` of the per-artifact score. The artifact producing that minimum is named in the `Worst artifact` column. Ties at the top score (typically 100%) collapse to `all` in the `Worst artifact` cell.

## Predictability verdict aggregates

Two states are reported. The first is measured from the corpus; the second is projected from the stress test. Both are required. Aggregates are computed per artifact first, then the verdict reports the worst-of-artifact value (the per-artifact breakdown is retained in the detail sections).

### Current (measured)

For each comparable artifact R, compute:

- **Substance(R)** = mean of all substrate-fidelity sub-dimension scores for R plus identifier alignment for R.
- **Structure(R)** = section structure fidelity score for R.
- **Naming(R)** = naming framing score for R.

The verdict reports `min over R` for each of Substance, Structure, Naming, on a 0.00–1.00 scale rounded to two decimals. If the worst artifact differs across Substance / Structure / Naming, name each worst artifact inline in the verdict text.

### Projected (after recommendations)

Computed by walking the ranked recommendations from Phase 6 and applying their per-(dimension, artifact) lifts to the current per-(dimension, artifact) scores. For each (dimension, artifact) cell:

1. Start from the current per-(dimension, artifact) percentage.
2. For every recommendation whose `Targets` field names this (dimension, artifact) — or names that dimension without scoping an artifact, in which case it applies to every comparable artifact for that dimension — add its projected-lift contribution. A recommendation targeting multiple cells distributes its total lift proportionally to the number of cells it targets unless the recommendation states an explicit per-cell breakdown.
3. Clamp each resulting per-(dimension, artifact) percentage to at most 100%. Never project above the ceiling.
4. Recompute Substance(R), Structure(R), Naming(R) per artifact, then take the worst-of-artifact for the projected verdict.

A (dimension, artifact) cell that no recommendation targets keeps its current score unchanged in the projection.

The projection is analytical, not measured. The report must label it as such.

## Hard-fail check before writing

Every row in the top-line table must cite at least one piece of concrete evidence (a heading, an ID, a path, a quoted string, a run identifier) **from the worst-of artifact named in that row**. Every per-artifact cell shown in the detail sections must likewise cite its own evidence. If any row or cell has no evidence, the report is not allowed to be written — return to Phase 3 and gather the missing evidence.
