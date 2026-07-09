# ADR-007 — Pipeline code: Python declarative pipelines over a tested wheel, dataset types per layer (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | DE team |
| Informed | Wider data team |

---

## Context

We need to decide the language and packaging for pipeline logic, how it is unit-tested,
where reusable logic lives, and which pipeline dataset type each medallion layer uses.
The conformed enterprise view lives in the silver layer (ADR-001); this record decides
how the shared transformation and metric functions behind it are packaged and tested.

---

## Options evaluated

**Option A — Thin Python pipelines over a tested wheel, dataset types fixed per layer**
Pipeline definitions are thin Python files using the declarative API, calling pure
functions in an importable package that builds to a wheel. SQL is allowed for simple
pipelines. Dataset types are fixed: bronze streaming tables, silver streaming tables
plus materialized views for enrichment or aggregation, gold materialized views.

**Option B — All logic inline in pipeline notebooks**
Fast to start, but hard to unit-test, encourages copy-paste, and gives conformed
entities nowhere reusable to live.

**Option C — Pure SQL pipelines throughout**
Clear and analyst-friendly for simple transforms, but weaker for reusable logic and
conformed-entity functions, and harder to unit-test.

**Options not pursued**
- Compiling the pipeline definitions themselves into the wheel: pipelines are source
  files referenced by the pipeline. The wheel holds shared logic, not the pipeline
  entry point.

---

## Decision

**Option A chosen. Pipeline files are thin and import pure functions from a
wheel-built package. Reusable conformed logic and metric definitions live in the
package and in `common/entities`, exercised by `tests/`. Table layout uses liquid
clustering with `CLUSTER BY AUTO`. Data quality expectations are enforced: warn at
bronze, drop or quarantine at silver, fail for critical gold constraints.**

### Rationale

| Criterion | Option A | Option B | Option C |
|:----------|:---------|:---------|:---------|
| Unit-testable logic | Yes | No | Weak |
| Reuse of conformed entities | Yes | No | Weak |
| Supports the silver conforming layer (ADR-001) | Yes | No | Partly |
| Ease for simple transforms | Medium | High | High |
| Analyst accessibility | Medium | Medium | High |

Factoring pure functions into a tested package is what makes the silver conforming
layer from ADR-001 real rather than aspirational: the enterprise-view logic is written
once, tested, and imported by the silver pipelines that gold then builds on. SQL remains
available where a pipeline is simple enough not to need it.

Decision basis: the Lakeflow best-practices "Choose the right dataset type" and
"Organize pipelines with the medallion architecture" sections fix streaming tables and
materialized views per layer; the templates page provides the Python-package-to-wheel
option; the "Use liquid clustering for data layout" and "Enforce data quality with
expectations" sections set those defaults.

---

## Validation

Pipeline files are thin and import from the package. `tests/` cover the package and run
in CI. The wheel builds via the bundle `artifacts` section. Dataset types match the
per-layer rule in review, and expectations are present on each pipeline.
`databricks bundle validate` passes.

---

## Consequences

- `src/<package>/` is the tested wheel; pipeline files import it; medallion subfolders
  become modules within the package.
- Unit tests run in CI against the package.
- SQL is used only for pipelines simple enough to not need shared logic.
- Table layout is self-tuning via `CLUSTER BY AUTO`, with no manual partitioning.

---

## Sources

- Best practices for Lakeflow Spark Declarative Pipelines, section "Choose the right dataset type" — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices
- Best practices for Lakeflow Spark Declarative Pipelines, section "Organize pipelines with the medallion architecture" — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices
- Best practices for Lakeflow Spark Declarative Pipelines, section "Use liquid clustering for data layout" — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices
- Best practices for Lakeflow Spark Declarative Pipelines, section "Enforce data quality with expectations" — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices
- Declarative Automation Bundles project templates (Python package to wheel option) — https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/templates

---

| Field | Value |
|:------|:------|
| Version | 0.1 (draft) |
| Last Updated | 2026-07-09 |
