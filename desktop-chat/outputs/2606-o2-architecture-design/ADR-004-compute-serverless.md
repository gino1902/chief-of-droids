# ADR-004 — Compute: serverless for all pipelines and jobs (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | Platform / FinOps |
| Informed | Wider data team |

---

## Context

Every pipeline and job needs compute. The choice between serverless and self-managed
clusters affects cost, configuration burden, and which governance features are
available by default.

---

## Options evaluated

**Option A — Serverless compute**
Databricks manages the infrastructure, with no cluster sizing to configure. Databricks
recommends serverless for new pipelines, cites roughly 20% lower cost than comparable
classic clusters, and serverless always runs on Unity Catalog, so governance and
lineage are built in.

**Option B — Classic job clusters**
Full control over instance types and runtime. Needed only for specific libraries or
runtimes not supported on serverless, at the cost of ongoing sizing and tuning.

**Option C — All-purpose interactive clusters for jobs**
An anti-pattern for scheduled work, expensive and discouraged.

---

## Decision

**Option A chosen. Serverless for every pipeline and job. No `new_cluster` or
`job_clusters` blocks. Classic compute is used only as a documented exception when a
specific requirement is unsupported on serverless.**

### Rationale

| Criterion | Option A | Option B | Option C |
|:----------|:---------|:---------|:---------|
| Databricks-recommended | Yes | No | No |
| Configuration burden | None | High | High |
| Relative cost | Lower | Higher | Highest |
| Unity Catalog by default | Yes | Optional | Optional |
| Control over runtime | Limited | Full | Full |

Serverless removes cluster management entirely, lands lower cost, and forces Unity
Catalog, which we want anyway. The limited runtime control is acceptable given our
workloads are standard batch pipelines.

Decision basis: the Lakeflow best-practices "Use serverless compute" section states
Databricks recommends serverless for new pipelines and that serverless always uses
Unity Catalog.

---

## Validation

No resource YAML contains `new_cluster` or `job_clusters` in review. Pipelines are
configured serverless. Any classic-compute exception carries a note in the bundle and
a reference back to this ADR.

---

## Consequences

- Resource configuration is simpler, with no cluster definitions to maintain.
- Unity Catalog is mandatory, which aligns with the per-environment catalog model
  (see ADR-006).
- A genuine need for classic compute is handled as a recorded exception, not a silent
  deviation.

---

## Sources

- Best practices for Lakeflow Spark Declarative Pipelines, section "Use serverless compute" — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices

---

| Field | Value |
|:------|:------|
| Version | 0.1 (draft) |
| Last Updated | 2026-07-09 |
