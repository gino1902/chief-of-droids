# json-artefact-extraction predictability report

Generated: 2026-06-01 13:48
Runs analyzed: 3 per artefact — r01..r03
Substrate: raw source images (binary), accuracy oracle = Claude vision read (validated layer)
Analyzed target: PaddleOCR structured-JSON layer (TableRecognitionPipelineV2 + PP-Chart2Table), paddleocr 3.6.0
Comparable artefacts: trims-tables, bar-automotive-revenues, line-1yr-performance
Non-comparable artefacts excluded: none

> Note on method. This report extrapolates the criteria of `improving-skills-predictability` to a non-text target the skill itself cannot ingest (it hard-fails on binary substrate and on N<5). The consistency dimensions are carried over verbatim in spirit. One axis is added that the source skill does not have: **Accuracy vs the vision oracle**. The addition is the point of the exercise, see the verdict.

## Summary - Outputs Variance per Dimension

| Category | Actual | Projected | Comments |
|:--|:--|:--|:--|
| Structure (schema shape) | 0% | = | Schema/table shape byte-identical across r01-r03 in every artefact; no recommendation targets this dimension |
| Substrate fidelity (value capture) | 0% | = | Values byte-identical run-to-run; line-1yr is identically wrong each run, which is exactly why variance is 0 |
| Modality | n/a | n/a | n/a — no modal statements in a data artefact |
| Naming | 0% | = | Entity/column naming stable across runs in all three artefacts |
| Identifier (record identity) | 0% | = | Rows/series anchor the same records across runs; no drift |

Analysis produced by `claude-opus-4-8[1m]`. Variance is the inverse of the predictability score: `variance = 100% − stability_score`, computed per dimension per artefact, then aggregated worst-of-artefact. Numbers are rounded to multiples of 5. Predictability is uniformly 0% variance because the extractor is deterministic (greedy decode, no sampling in generation_config). This is a measurement, not a projection.

## Top-line scores

Two axes. Predictability is run-to-run consistency (what the source skill measures). Accuracy is match to the vision oracle (the added axis). Score is worst-of across comparable artefacts.

| Dimension | Worst artefact | Predictability | Accuracy | Reading |
|:--|:--|:--|:--|:--|
| Schema-shape fidelity | all | **100%** | n/a | Same keys/columns/array shape in r01-r03 for all three artefacts |
| Record identity | line-1yr-performance | **100%** | ~25% | Same series labels each run, but BYDDY is dropped after 4 of 12 points identically every run |
| Field-set fidelity (challenge-1 schema) | all | **100%** | n/a | Stable field set run-to-run; semantic enrichment (entity/metric/unit/period) is a separate LLM step |
| Value verbatim stability | bar-automotive-revenues | **100%** | ~50% | Automotive series byte-identical and ~accurate; Consensus series byte-identical and 100% wrong ($0,000 ×10) |
| Provenance path stability | all | **100%** | n/a | Source path byte-stable |
| Record counts | all | **100%** | varies | Counts stable run-to-run; line-1yr emits a stable-but-incomplete count |
| Entity naming | all | **100%** | ~95% | Stable; minor footnote OCR ("Teslg ModelComngrison") on trims |

**Overall predictability — current (measured, worst-of artefact):**   Consistency ≈ **1.00** across all dimensions and artefacts.
**Overall accuracy — current (measured vs vision oracle, worst-of artefact):** ≈ **0.25** (line-1yr-performance).

Per-artefact aggregate breakdown:

| Artefact | Type | Extractor | Predictability | Accuracy |
|:--|:--|:--|:--|:--|
| trims-tables | labelled table | TableRecognitionPipelineV2 | 1.00 | ~0.95 |
| bar-automotive-revenues | estimated chart | PP-Chart2Table | 1.00 | ~0.50 |
| line-1yr-performance | estimated chart | PP-Chart2Table | 1.00 | ~0.25 |

## Section structure fidelity (schema shape)

| Artefact | Run | Shape delta vs r01 |
|:--|:--|:--|
| trims-tables | r01 | — (canonical) |
| trims-tables | r02 | — (byte-identical) |
| bar-automotive-revenues | r01-r03 | — (byte-identical, 3 cols × 10 rows each run) |
| line-1yr-performance | r01-r03 | — (byte-identical, 8 series rows each run) |

Notes: every artefact's structure is byte-stable across runs. Determinism was verified by diff: chart2table returned 683 identical bytes ×3 on line-1yr; table pipeline HTML identical ×2 on trims; bar chart identical ×3.

## Identifier alignment (record identity)

| Artefact | Identifier | Coverage | Anchor stability | Notes |
|:--|:--|:--|:--|:--|
| line-1yr | TSLA, SPX, F, GM, BYDDY, VWAGY, MBGAF, TM | 3/3 | stable label, wrong data | All 8 labels present each run; BYDDY truncated to 4 points identically |
| bar-automotive | Automotive, Consensus | 3/3 | stable | Both columns present each run; Consensus values dead each run |
| trims-tables | Model S/X AWD/Plaid | 3/3 | stable | Rows anchor correctly |

Split/fold events: none.

## Substrate fidelity — value capture vs oracle

| Invariant (from vision oracle) | Artefact | r01 | r02 | r03 | Accuracy |
|:--|:--|:--|:--|:--|:--|
| Model S AWD = $79,990 / 410 mi | trims | ✓ | ✓ | ✓ | exact |
| Model X Plaid = $99,990 / 314 mi | trims | ✓ | ✓ | ✓ | exact |
| Footnote "Tesla Model Comparison" | trims | ✗ | ✗ | ✗ | OCR'd "Teslg ModelComngrison" |
| Automotive 2020..2029e bars | bar | ≈ | ≈ | ≈ | within ~3k of gridline truth |
| Consensus series (red bars) | bar | ✗ | ✗ | ✗ | "$0,000" ×10, series lost |
| Y-axis negative values (-10%..-60%) | line | ✗ | ✗ | ✗ | no negative value emitted at all |
| TSLA trajectory | line | ✗ | ✗ | ✗ | fabricated monotonic rise; real series is volatile |
| BYDDY full series | line | ✗ | ✗ | ✗ | truncated to 4 of 12 points |

Legend: ✓ exact · ≈ accurate estimate · ✗ missing or distorted. Note the column pattern: every defect repeats identically across r01-r03. The extractor is consistently wrong, which a predictability-only metric reads as a perfect score.

## Statement counts per category

### Artefact: line-1yr-performance

| Category | r01 | r02 | r03 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|
| series labels | 8 | 8 | 8 | 8 | 8 | 8.0 |
| datapoints emitted | ~88 | ~88 | ~88 | 88 | 88 | 88.0 |
| negative values | 0 | 0 | 0 | 0 | 0 | 0.0 |
| malformed cells | 6 | 6 | 6 | 6 | 6 | 6.0 |

### Artefact: bar-automotive-revenues

| Category | r01 | r02 | r03 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|
| year rows | 10 | 10 | 10 | 10 | 10 | 10.0 |
| Automotive values | 10 | 10 | 10 | 10 | 10 | 10.0 |
| valid Consensus values | 0 | 0 | 0 | 0 | 0 | 0.0 |

## Naming framing finding

Source names the entities from the chart legends and table headers. All runs read naming from the source artefact, not from any slug. Only defect is OCR-level: the trims footnote stylised text degraded identically each run. Framing is stable and source-derived.

## Per-file deviation summary

### r01-r03 (identical)
- **trims-tables:** core values exact; footnote OCR garbled; composite-image detection merges the two sub-tables in one region.
- **bar-automotive-revenues:** Automotive series accurate to gridlines; Consensus series fully lost to "$0,000" sentinel.
- **line-1yr-performance:** all negatives absent; TSLA fabricated; BYDDY truncated; 6 malformed multi-guess cells.

No run is an outlier. Run-to-run deviation is zero by construction.

## Predictability verdict

The binding constraint is accuracy, not predictability, and the two are orthogonal here. Predictability is 1.00 on every dimension and artefact because the extractor is deterministic, so re-ingest of the same source reproduces the same JSON exactly. That is genuinely useful for the grounding and citation-stability rules. But it is silent on correctness: the line-1yr-performance artefact scores 1.00 predictability and ~0.25 accuracy, because it fabricates the same wrong table every run. Accuracy is fully predicted by two source properties the predictability metric cannot see: presence of printed values (labelled trims ≈ 0.95, label-free charts 0.25-0.50) and series count (single-series Automotive ≈ accurate, 8-series line ≈ fabricated). The highest-leverage fix is therefore not a predictability fix at all, it is a gate on which artefacts are allowed to become JSON in the first place.

## Recommendations

*Stress test method: analytical projection against the recorded per-artefact defects. No re-runs performed. Lift is measured on the accuracy axis, since predictability is already maxed and adding consistency constraints to a deterministic extractor yields nothing.*

### R-001 — Gate JSON-artefact creation on printed data labels     [projected accuracy lift: +45 pts worst-of]
- Targets: Value capture, all chart artefacts
- Statement: In the ingest decision node, a chart routes to a PP-Chart2Table JSON artefact only if it carries printed per-datum values. A chart whose values must be read off an axis (label-free) routes to a Claude vision claim instead, never to a digitised series.
- Rationale: would have stopped both failing artefacts (bar Consensus, entire line chart) from being persisted as false data. Trims (labelled) is unaffected and stays.
- Projected effect: prevented 2, partial 0, unaffected 1, regressed 0
- Risk: low — removes exactly the artefacts the oracle shows are untrustworthy.
- Dependencies / Overlap: supersedes R-003 — the label gate subsumes the single-series cap for the label-free cases.

### R-002 — Human value-verification before commit (the row-level approval)     [projected accuracy lift: +25 pts]
- Targets: Value capture, all artefacts
- Statement: No chart2table artefact is committed until its values are confirmed against the source in the ingest report. The approval row shows the extracted JSON beside the source crop.
- Rationale: catches the labelled-but-misread case (trims footnote OCR) and any label-gate false-negative. This is the only accuracy gate that works on label-free charts, since no machine oracle exists for them.
- Projected effect: prevented 1, partial 2, unaffected 0, regressed 0
- Risk: low — adds operator effort, already folded into the existing one-report approval flow.
- Dependencies / Overlap: additive with R-001 — R-001 reduces the volume reaching this gate so the operator judges fewer artefacts.

### R-003 — Cap chart2table to single dominant series     [projected accuracy lift: +20 pts]
- Targets: Value capture, multi-series charts
- Statement: chart2table is invoked only on single-series or two-series-with-labels charts. Multi-series label-free charts (>2 series) are rejected from the JSON layer.
- Rationale: the 8-series line chart is the worst artefact; the 2-series bar lost its second series. Series count predicts collapse.
- Projected effect: prevented 1, partial 1, unaffected 1, regressed 0
- Risk: medium — may exclude a legitimate labelled multi-series chart; R-001 already covers most cases.
- Dependencies / Overlap: overlaps R-001 — both filter the same failing artefacts by different criteria.

### R-004 — Schema honesty fields: method + per-series confidence + sentinel rejection     [projected accuracy lift: +10 pts]
- Targets: Field-set fidelity, all artefacts
- Statement: Every chart-derived artefact carries `method: labelled|estimated` and a per-series confidence. A series that resolves entirely to a sentinel ("$0,000") is dropped, not stored.
- Rationale: would have prevented the dead Consensus series from being persisted as zeros, and flags estimated artefacts so a query never mistakes an estimate for a published figure (challenge 4).
- Projected effect: prevented 1, partial 1, unaffected 1, regressed 0
- Risk: low.
- Dependencies / Overlap: additive with R-001 — honesty metadata plus the label gate together close the false-precision risk.

| Field        | Value       |
|--------------|-------------|
| Version      | 1.0         |
| Last Updated | 2026-06-01  |
| Status       | Draft       |
