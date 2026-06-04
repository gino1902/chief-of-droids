# Choosing and validating a document-extraction stack

> A play reconstructed from the 2026-05-31 to 06-02 session that converged on a vision-first extraction stack for Tesla source documents. Provisional until validated against a second instance.

## When to trigger

You must choose and commit to a toolchain that turns images and PDFs into markdown plus structured data, and the candidates span both deterministic OCR or layout models and frontier vision models. The signal is a stack decision you will depend on, not a one-off read.

Concrete instances:
- "Should we ingest these vendor decks with PaddleOCR-VL, Docling, or Claude vision?"
- "We need structured JSON out of charts and financial tables. Which extractor, and what guarantees on the numbers?"
- A teammate argues for adding a specialist OCR model because markdown cannot hold complex tables, and proposes JSON sidecars.
- "The benchmark leader is a small deterministic model. Should we just use the highest-scoring tool?"

## Why it matters

The obvious defaults are traps. Picking the benchmark leader, or the most deterministic tool, silently injects fabricated or run-to-run-inconsistent data into something downstream work trusts. This play produces a defensible stack choice backed by measured evidence on two axes, plus a pinned output schema that makes the choice safe to repeat. The deliverable is the decision and the test harness that justifies it.

## The play

### Optimal workflow

1. Frame the decision by source profile (chart and infographic heavy versus text and table heavy) and by the consuming unit (a cited claim versus a faithful full reproduction). Weight everything that follows by that frame.
2. Run an evidence-based comparison of candidates against the profile from published benchmarks and architecture, before installing anything.
3. Install the leading specialist candidate and run it on representative fixtures, not just on benchmarks.
4. Score on two independent axes. Predictability is run-to-run variance, measured by byte-diffing N runs. Accuracy is correctness against the source as ground truth.
5. Read the determinism result correctly. A deterministic tool that is wrong is consistently wrong, so a high predictability score is not evidence of quality.
6. Find the real accuracy predictor for your sources. Here it was the presence of printed labels. Label-free visuals force estimation, and estimation fabricates.
7. Validate the chosen reader on the hardest case (dense multi-section tables) before committing.
8. Close the predictability gap by pinning a typed-block schema, then re-run the variance test with independent isolated runs and confirm the structural variance collapses.
9. Confirm content fidelity with a round-trip on content, not layout.

### Critical moves

| Move | Why it is load-bearing |
| :--- | :--- |
| Weight the comparison by source profile | Without it the benchmark-leading or deterministic tool wins on paper and fails on the actual content mix. |
| Split predictability from accuracy into two axes | This is the move that exposes a deterministic tool that fabricates the same wrong answer every run. Collapse the axes and you mistake it for reliable. |
| Apply the label-presence gate | Printed values are faithful, label-free values are estimated. Without the gate you store estimates as fact. |
| Measure variance with independent isolated runs | In-context repeats anchor to the first output and fake a low variance. Isolated runs give the true number. |
| Pin a typed-block schema | Free-form output diverges in structure every run. Pinning collapses that variance to near zero. |

### Pits to avoid

- Treating determinism as reliability. In this session the specialist OCR scored near 100% predictability while returning roughly 25% accurate chart data, wrong identically on every run.
- Choosing a tool for a headline feature you then gate off. Chart-to-table was the reason to add the specialist, and the label gate then said not to use it on exactly the cases it was added for.
- Free-form JSON. Independent runs invented different top-level keys and nesting, with leaf counts spreading from 209 to 268 on one source.
- Estimating variance from in-context repeats. Anchoring makes the result look more stable than it is.
- Using full-document reconstruction as the fidelity test. It entangles extraction error, intended curation loss, and rendering or photo fabrication, so a mismatch is undiagnosable. Use a content round-trip plus a forward query test.
- Storing pixel-estimated chart series as exact numbers. That manufactures precision the source never published.
- Trusting a single accurate read as proof. Accuracy on one read is not predictability across reads.

## When to use it

- You are committing to a stack you will depend on, not running a one-off extraction.
- Sources are mixed or visually dense, with charts, infographics, or complex tables.
- The output feeds something that trusts the data, like a knowledge base, an index, or a downstream pipeline.
- You can produce representative sample sources to test against.

## When not to use it

- One-off extraction where a quick read is enough.
- Pure plain-text or markdown sources with no tables or charts, so there is no contest to resolve.
- You need guaranteed cell-aligned reproduction of dense grids as the actual artefact. That is the counter-case where a deterministic structural model can genuinely win, and this play would point you there rather than to vision.
- Throwaway or low-stakes output where variance and accuracy do not matter.

## Expected outcome

A future reuse should return a named stack with measured numbers, not an opinion.

- Printed-value accuracy and source fidelity at or near 100%.
- Inter-iteration structural variance near zero after schema pinning.
- Estimated values flagged with method and confidence, never stored as exact.

Falsifiable check: re-run the chosen stack three times on a sample. The structure and every printed value should be identical across runs, and any wrong value should be wrong-and-flagged, not wrong-and-confident.

## Tradeoffs

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| The reader | Specialist OCR, deterministic and structural | Frontier vision, sampled and semantic | Vision as the single reader. Gave up guaranteed grid alignment on dense tables. |
| Tolerated failure mode | Deterministic but confidently wrong | Sampled but honestly uncertain | Honest failure. Gave up byte-reproducibility of the read. |
| Chart data | Digitise the series (chart-to-table) | Capture the claim and flag estimated | Claim plus flag. Gave up exact series even on labelled charts. |
| JSON structure | Free-form, the model's choice | Pinned typed-block schema | Pinned. Gave up some expressivity. |
| Fidelity test | Full-document reconstruction | Content round-trip plus query | Content round-trip. Gave up any layout check. |
| Variance method | In-context repeats, cheap | Independent isolated runs | Isolated runs. Paid more compute for a valid measurement. |

## Version block

| Field | Value |
| :--- | :--- |
| Version | 1.1 |
| Last Updated | 2026-06-03 |
| Status | Draft |
| Pairs with | `outputs/predictability/json-artefact-extraction/json-artefact-extraction-predictability-20260601-1348.md`, `outputs/predictability/transpile-fidelity/`, `outputs/predictability/transpile-fidelity-pinned/schema.json`, and the companion `2026-06-02-tech-design-open-points.md` |
