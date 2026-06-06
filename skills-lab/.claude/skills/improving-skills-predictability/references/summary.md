# Summary block

Single block rendered in two places:

1. At the **top** of the report file (`<skill-name>-predictability-<timestamp>.md`), immediately under the `# <skill-name> predictability report` H1 and the standard generated-metadata lines (`Generated:`, `Runs analyzed:`, `Substrate:`, `Analyzed skill:`, `Comparable artifacts:`, `Non-comparable artifacts excluded:`).
2. At the **end of the run**, streamed to chat after the `✓ Wrote …` line.

Both renderings are byte-identical.

## Layout

```markdown
## Summary - Outputs Variance per Dimension

| Category | Actual | Projected | Comments |
|:--|:--|:--|:--|
| Structure | N% | N% | <one sentence citing the dominant evidence from the worst artifact> |
| Substrate fidelity | N% | N% | <one sentence> |
| Modality | N% | N% | <one sentence> |
| Naming | N% | N% | <one sentence> |
| Identifier | N% | N% | <one sentence> |

Analysis produced by `<model-id>`. Variance is the inverse of the predictability score: `variance = 100% − stability_score`, computed per dimension per artifact, then aggregated with the same worst-of-artifact rule used everywhere else in this report. For multi-sub-dimension categories (Substrate fidelity), the stability score is the **mean across sub-dimensions** before inversion. Numbers are rounded to multiples of 5 to avoid false precision. Projected values apply the recommendations from §Recommendations analytically — no re-runs were performed.
```

## Row → dimension mapping

| Row | Source dimensions (from §Top-line scores) | Aggregation |
|:--|:--|:--|
| Structure | Section structure fidelity | direct |
| Substrate fidelity | Domain concepts · Schemas · Paths · Verbatim strings · Policies / constraints | mean of the five sub-dimension scores, then `100% − mean` |
| Modality | Modality and surface drift | direct |
| Naming | Naming framing | direct |
| Identifier | Identifier alignment | direct |

The row order is fixed: Structure, Substrate fidelity, Modality, Naming, Identifier. Do not re-order.

## Actual column

For each row R:

1. Look up the per-(dimension, artifact) percentage(s) feeding R from §Top-line scores.
2. If R aggregates multiple sub-dimensions, take the mean per artifact first, then take the worst-of across comparable artifacts.
3. `actual = 100 − value`, rounded to the nearest 5.

A row with no comparable artifact data (e.g., the skill produces no identifiers at all) renders `Actual: n/a` and `Projected: n/a`. The Comments cell must still cite evidence — "n/a — no identifiers emitted by this skill across any run" or equivalent.

## Projected column

For each row R:

1. Start from the per-(dimension, artifact) percentages used to compute Actual.
2. For each ranked recommendation in §Recommendations, apply its projected lift to the (dimension, artifact) cells it targets (per `scoring.md` § "Projected aggregates"). Clamp each cell at 100%.
3. Recompute the row's value with the same aggregation used in Actual.
4. `projected = 100 − value`, rounded to the nearest 5.

If `projected == actual` and no recommendation targets the row, render `Projected: =` (literal equals sign) and add `no recommendation targets this dimension` to the Comments cell.

## Comments column

One sentence per row. Format:

- For rows with measurable drift (Actual > 0%): cite the worst-artifact evidence — name the worst artifact, the most-discriminating run, and either an identifier, a verbatim string, or a section name. Example: `Identifier · requirements · CON-001 anchors three statements across v01/v02/v04`.
- For rows at Actual 0%: cite the locking factor. Example: `Structure · all · 15-section S2 template binds completely; no deviations`.
- For rows where `projected < actual`: name the recommendation(s) responsible by ID. Example: `R-001 anchors IDs to substrate byte position`.

Do not exceed one line per row. If the evidence does not fit, shorten the wording — never wrap or split into two cells.

## Model attribution line

The line directly below the table starts with the literal string `Analysis produced by ` followed by the model ID in backticks (e.g., `claude-opus-4-7[1m]`). Resolve the model ID from the runtime — never hard-code it. If the runtime does not expose a model ID, emit `Analysis produced by <unknown-model>` and add `model-id unresolved at runtime` to the §Operational notes section of the report.

## Variance formula — verbatim text to render below the table

```
Analysis produced by `<model-id>`. Variance is the inverse of the predictability score: `variance = 100% − stability_score`, computed per dimension per artifact, then aggregated with the same worst-of-artifact rule used everywhere else in this report. For multi-sub-dimension categories (Substrate fidelity), the stability score is the mean across sub-dimensions before inversion. Numbers are rounded to multiples of 5 to avoid false precision. Projected values apply the recommendations from §Recommendations analytically — no re-runs were performed.
```

Render this paragraph verbatim. Do not rephrase per-run. Substitute only the model ID.

## Position in the file

In the report file:

```
# <skill-name> predictability report

Generated: <ts>
Runs analyzed: <N> — <list>
Substrate: <path>
Analyzed skill: <path>
Comparable artifacts: <list>
Non-comparable artifacts excluded: <list or "none">

## Summary - Outputs Variance per Dimension

<table + attribution paragraph from this spec>

## Top-line scores

<existing table>
```

In chat at end-of-run:

```
→ Phase 7 — Write
✓ Wrote <path>

## Summary - Outputs Variance per Dimension

<table + attribution paragraph>
```

Render no other commentary between `✓ Wrote …` and the Summary block. The Summary is the last token stream of the run.

| Field        | Value       |
|--------------|-------------|
| Version      | 1.1         |
| Last Updated | 2026-05-16  |
| Status       | Draft       |
