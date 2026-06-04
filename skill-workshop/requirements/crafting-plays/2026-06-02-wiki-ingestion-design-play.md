# Layering ingestion for a source-grounded knowledge base

> A play reconstructed from the 2026-05-31 to 06-02 session on the Databricks-on-Azure style curated wiki, covering how to store curated claims alongside structured data without breaking grounding. Provisional until validated against a second instance.

## When to trigger

You are designing an ingestion pipeline for a curated knowledge base built from immutable raw sources, and you must decide what to store, in what form, and how to keep it traceable back to source. The signal is a tension between keeping pages light and preserving data that some queries will need exactly.

Concrete instances:
- "Complex tables and chart series will not fit in markdown. Do we add JSON sidecars, and where do they live?"
- "How do we keep wiki claims lean but still answer a query like Tesla fiscal results over the last three years from the base alone?"
- "At what point in the pipeline do we decide to persist structured data rather than just a claim?"
- "A chart has no data labels. Do we digitise it into the base or not?"

## Why it matters

A curated knowledge base earns its value from grounded claims, not from copies of sources. Over-capturing turns it into a photocopier and breaks hierarchical navigation. Under-capturing loses data a future query needs. This play produces a layered design, lean claim pages plus on-demand structured artefacts, with a decision gate that keeps the operator's choices few and an unbroken provenance chain. The deliverable is the set of ingestion principles.

## The play

### Optimal workflow

1. Fix the atom. The base's unit is a cited claim, not a reproduction. Most of a source is discarded on purpose.
2. Layer the output. Lean claim pages in markdown, plus structured data artefacts in JSON for selected tables and charts, cross-referenced from the claims.
3. Make each structured artefact self-sufficient and discoverable. It carries subject, metric, period, and unit plus provenance, and it is indexed so a query can find it. Self-describing solves reading, an index solves retrieval.
4. Place the decision node behind the existing relevance and freshness filter, so only data attached to accepted claims is ever proposed for structured capture. Fold the choice into the row-level approval already in the pipeline rather than adding a new step.
5. Add a label-presence sub-gate. Digitise only charts with printed values. A label-free chart routes to a claim, never to a fabricated series.
6. Keep the JSON a projection, not a source of truth. It is re-ingest-only, rebuilt rather than patched, and it cites raw. Raw stays the only truth.
7. Mark estimated values explicitly with method and confidence.

### Critical moves

| Move | Why it is load-bearing |
| :--- | :--- |
| Define the atom as the cited claim | Without it the base over-captures and stops being a curated projection. |
| Gate the structured-data decision behind relevance and freshness | Stale or irrelevant visuals never reach the operator, so the decisions stay few. |
| Apply the label-presence sub-gate | Without it the base stores pixel-estimated values as if they were published facts. |
| Keep an unbroken provenance chain claim to JSON to raw, re-ingest only | Without it the derived data drifts from source and grounding breaks. |

### Pits to avoid

- Sidecar JSON with no index. A self-describing artefact still cannot be found by a query without retrieval metadata.
- A free-standing decision step bolted onto the pipeline instead of folded into the existing approval.
- Treating the JSON as authoritative. It is a projection. Raw is the source of truth.
- Storing infographics as structured data. They have no canonical schema, so keep them as vision-read claims.
- In-page JSON blobs. They defeat the lean-claim navigation that the layering exists to protect.

## When to use it

- A curated, source-grounded knowledge base with immutable raw sources.
- Sources contain data in tables or charts that some queries will need exactly.
- Traceability and grounding are hard requirements.

## When not to use it

- A document store whose goal is faithful full copies rather than curation.
- Sources with no structured data worth preserving beyond prose claims.
- One-shot summarisation with no re-ingest or audit lifecycle, where the projection discipline buys nothing.

## Expected outcome

- Claim pages stay lean and navigable.
- Structured artefacts are retrievable and answerable on their own.
- Every stored value traces to a raw source, and estimated values are flagged.

Falsifiable check: pick a target query and confirm it is answerable from the artefact alone, and confirm every datum in the artefact cites a raw source.

## Tradeoffs

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Base content | Faithful copy of the source | Curated claims projection | Curated projection. Gave up completeness. |
| Complex data home | Markdown only, which is lossy | JSON sidecar artefacts | Sidecar JSON. Added an index and provenance burden. |
| Artefact placement | In-page JSON block | Sidecar file cross-referenced from the claim | Sidecar. Gave up single-file simplicity. |
| Decision timing | Always extract structured data | Gated behind relevance and freshness | Gated. Fewer artefacts, operator effort folded into approval. |
| Chart data | Digitise everything | Only labelled charts, else a claim | Labelled only. Gave up label-free series. |

## Version block

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-06-02 |
| Status | Draft |
| Pairs with | `2026-06-02-extraction-stack-selection-play.md`, the wiki `CLAUDE.md` and `.claude/rules/page-schema.md`, and the companion `2026-06-02-tech-design-open-points.md` |
