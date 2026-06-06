# Tech design: open points and actions

> Companion to the two plays from the 2026-05-31 to 06-02 session. These are the decisions the session opened but did not close. Each names the question, why it is open, and the next action.

## Schema and enforcement

| # | Open point | Why it is open | Next action |
| :--- | :--- | :--- | :--- |
| S1 | Generation-time enforcement of the schema | The agents validated output with a full `jsonschema` library after the fact. That is not the same as the model being constrained at generation time. The API structured-output layer accepts only a subset and largely ignores `$schema`. | Verify the current Anthropic tool-use and structured-output subset. Confirm what it enforces. |
| S2 | Conditional blocks may not be enforced | The schema discriminates block types with `if/then` inside `allOf`, which a post-hoc validator honours but a constrained-decoding engine likely does not. | Convert the block-type discrimination to a `oneOf` tagged union, which is more widely enforced at generation time. |
| S3 | Draft 2020-12 versus draft-07 | 2020-12 was chosen for `prefixItems` (strict positional row typing) and for being current stable. The enforcement engine may not support 2020-12 keywords. | Confirm the engine supports 2020-12, or downgrade `prefixItems` to the draft-07 array-form `items` as the documented fallback. |
| S4 | Schema is provisional | Block types were exercised on two source kinds only. The `entities` block for infographics is the weakest, with no firm shape. | Exercise the schema on more source kinds and firm up or drop the `entities` block. |
| S5 | Tables without header rows | The verbatim-column rule binds column names to the source header. It has no defined fallback when a table has no header row. | Define a fallback naming rule for header-less tables. |

## Extraction stack

| # | Open point | Why it is open | Next action |
| :--- | :--- | :--- | :--- |
| E1 | Docling never tested empirically | It was held as the complex-table fallback on the strength of published benchmarks and architecture, not a run on these fixtures. | Either test Docling on a genuinely dense grid that vision might mishandle, or formally shelve it with that caveat stated. |
| E2 | Estimated-value confidence not calibrated | Chart values are flagged estimated with a confidence label, but the labels are not calibrated against any error measurement. | Calibrate confidence bands against measured read error on labelled-then-masked charts. |
| E3 | Production PDF renderer undecided | The regen PDFs used Chrome headless as a throwaway. No production renderer was chosen. | Decide whether regen is even needed in production, and if so pick a renderer. |

## Variance residuals

| # | Open point | Why it is open | Next action |
| :--- | :--- | :--- | :--- |
| V1 | Prose-block granularity varies | After schema pinning, structured blocks are byte-stable but prose paragraph count still moves by about two across runs. | Decide whether this is acceptable or whether prose chunking needs a rule. |
| V2 | Styling-only information is lost | The round-trip preserves stated content but drops information carried only by visual styling with no text label, like the colour-highlighted current-quarter column. | Decide whether any source styling carries meaning that must be captured as text. |

## Wiki design (deferred when the session decoupled)

| # | Open point | Why it is open | Next action |
| :--- | :--- | :--- | :--- |
| W1 | Decision-node placement | The node was specified conceptually but not wired into the actual `/ingesting-sources` pipeline, which is still unauthored. | Author the ingest skill with the decision node folded into row-level approval. |
| W2 | Artefact index and retrieval | The need for an index of structured artefacts was identified but no index format was defined. | Define where the artefact index lives (page front-matter or `index.md`) and its fields. |
| W3 | Re-ingest mechanics for artefacts | Re-ingest-only and rebuilt-not-patched were stated as principles but not specified as procedure. | Specify how a structured artefact is superseded on re-ingest. |

## Cross-cutting

| # | Open point | Next action |
| :--- | :--- | :--- |
| X1 | The two plays overlap on the schema and the label gate. | Decide whether to factor the shared pieces into one referenced spec or let each play restate them. |

## Version block

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-06-02 |
| Status | Draft |
| Pairs with | `2026-06-02-extraction-stack-selection-play.md`, `2026-06-02-wiki-ingestion-design-play.md` |
