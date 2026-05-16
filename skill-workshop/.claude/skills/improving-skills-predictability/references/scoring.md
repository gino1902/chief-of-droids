# Scoring rubric

Convert raw findings into per-dimension percentages, rounded to multiples of 5. Avoid false precision — the analytical projection is itself approximate.

## General formula

For each dimension, score = `100 * (preserved_items / total_items)`, rounded to the nearest 5%, with the following adjustments:

- `preserved_items` = full matches.
- Partial matches (semantic but not verbatim where verbatim was required) count as 0.5.
- An item present in fewer than 60% of runs counts as 0 for that dimension.

## Per-dimension rules

### Section structure fidelity

- `total_items` = max heading count across runs.
- `preserved_items` = headings that appear in the same position in every run.
- A demoted or promoted heading (level changed but text stable) counts as 0.5.
- A reordered heading counts as 0.

### Identifier alignment

- `total_items` = union of identifiers across runs.
- `preserved_items` = identifiers present in every run AND anchoring the same statement (semantic match) in every run.
- Split/fold events count as 0.5 (the meaning is preserved but the IDs are not).

### Substrate fidelity — domain concepts

- `total_items` = number of distinct concepts extracted in Phase 2.
- Concepts must be present in every run; semantic paraphrase is allowed.

### Substrate fidelity — schemas

- `total_items` = number of schema blocks in the substrate.
- A schema preserves credit only if all fields are present in the same role; renamed fields count as 0.5 if the renamed name is consistent across runs, 0 if not.

### Substrate fidelity — paths and verbatim strings

- Byte-level equality required. No partial credit.

### Substrate fidelity — policies / constraints

- `total_items` = number of modal statements in the substrate.
- Full match = present + same modality keyword.
- Same statement, different modality = 0.5.
- Missing = 0.

### Modality and surface drift

- `total_items` = number of aligned identifiers from Identifier alignment.
- `preserved_items` = identifiers whose modality keyword is identical across all runs.
- Surface drift (semantic-equivalent rewordings) does not subtract score but is noted in the report.

### Naming framing

- Binary by run: each run is either "reads substrate" (1) or "reads slug literally" (0). Hybrid = 0.5.
- Score = average across runs, rounded to nearest 5%.

## Predictability verdict aggregates

Two states are reported. The first is measured from the corpus; the second is projected from the stress test. Both are required.

### Current (measured)

- **Substance** = mean of all substrate-fidelity rows + identifier alignment.
- **Structure** = section structure fidelity score (single dimension).
- **Naming** = naming framing score (single dimension).

All three are reported on a 0.00–1.00 scale rounded to two decimals.

### Projected (after recommendations)

Computed by walking the ranked recommendations from Phase 6 and applying their per-dimension lifts to the current scores. For each dimension:

1. Start from the current per-dimension percentage (the row in the Top-line scores table).
2. For every recommendation whose `Targets` field names that dimension, add its projected-lift contribution to that dimension. A recommendation that targets multiple dimensions distributes its total lift proportionally to the number of dimensions it targets unless the recommendation states an explicit per-dimension breakdown.
3. Clamp the resulting per-dimension percentage to at most 100%. Never project above the ceiling — a recommendation cannot improve a dimension that is already at 100%.
4. Compute the projected Substance / Structure / Naming aggregates from the updated per-dimension percentages using the same formulas as the current-state aggregates.

A dimension that no recommendation targets keeps its current score unchanged in the projection.

The projection is analytical, not measured. The report must label it as such.

## Hard-fail check before writing

Every row in the top-line table must cite at least one piece of concrete evidence (a heading, an ID, a path, a quoted string, a run identifier). If any row has no evidence, the report is not allowed to be written — return to Phase 3 and gather the missing evidence.
