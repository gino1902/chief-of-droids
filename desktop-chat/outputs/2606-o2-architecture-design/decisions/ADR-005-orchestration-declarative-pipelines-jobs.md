# ADR-005 — Orchestration: declarative pipelines for logic, jobs to orchestrate (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | DE team |
| Informed | Business use-case owners |

---

## Context

We need to decide how transformation logic is expressed and how work is scheduled.
The medallion layers (bronze, silver, gold) can be built imperatively in notebooks or
declaratively in pipelines, and scheduling can be coupled to the logic or separated
from it. This shapes every bundle's resources.

---

## Options evaluated

**Option A — Declarative pipelines for logic, jobs only to orchestrate, one pipeline per medallion layer**
All transformation runs as Lakeflow Spark Declarative Pipelines. Lakeflow Jobs only
schedule and orchestrate them. Bronze ingestion, silver conforming and gold aggregation
are separate pipelines in separate bundles (see ADR-001, ADR-003), which the docs
recommend so a transformation failure does not block new data landing in bronze.

**Option B — Imperative notebook jobs**
Transformations written directly in notebook tasks. Faster to start, but loses
declarative CDC, expectations, incremental refresh and built-in lineage, and is harder
to test and maintain.

**Option C — One pipeline covering bronze to gold**
Simpler to wire up, but couples the layers, so a transform failure blocks ingestion
and each layer cannot be scheduled or monitored independently.

**Options not pursued**
- An external orchestrator (Airflow, Azure Data Factory) as the primary scheduler:
  Lakeflow Jobs is native and sufficient. Consider only if an enterprise scheduler is
  mandated.

---

## Decision

**Option A chosen. Transformation logic lives only in declarative pipelines. Jobs hold
only orchestration. Bronze ingestion, silver conforming and gold aggregation are
separate pipelines in their respective layer bundles. Pipelines run in triggered mode
by default, with continuous reserved for seconds-range latency needs. Change data
capture uses declarative `APPLY CHANGES INTO` rather than imperative `MERGE`.**

### Rationale

| Criterion | Option A | Option B | Option C |
|:----------|:---------|:---------|:---------|
| Declarative CDC, expectations, lineage | Yes | No | Yes |
| Independent scheduling per layer | Yes | Partly | No |
| Ingestion isolated from transform failure | Yes | Partly | No |
| Testability of logic | High | Low | Medium |
| Wiring simplicity | Medium | High | High |

Declarative pipelines give data quality, CDC and lineage for free, and splitting
ingestion from transformation keeps each layer independently operable. The extra
wiring is a worthwhile cost.

Decision basis: the Lakeflow best-practices "Organize pipelines with the medallion
architecture" section directs separating ingestion from transformation; the "Choose
between triggered and continuous pipeline mode" section sets triggered as the default;
the "Use declarative CDC instead of imperative MERGE" section directs `APPLY CHANGES`.

---

## Validation

Transformation code appears only in pipeline resources, and jobs contain only
orchestration tasks. Each producer bundle has a distinct ingestion pipeline and
transformation pipeline. `databricks bundle validate` passes. Pipeline mode is
triggered unless a documented latency need justifies continuous.

---

## Consequences

- Each producer bundle carries a bronze ingest pipeline and a job. Each silver bundle
  carries a conforming pipeline and a job. Each use-case bundle carries a gold pipeline
  and a job.
- Layers are scheduled, monitored and troubleshot independently.
- CDC sources use `APPLY CHANGES INTO`, avoiding hand-written merge logic.
- Continuous mode is an explicit, justified exception, not a default.

---

## Sources

- Best practices for Lakeflow Spark Declarative Pipelines, section "Organize pipelines with the medallion architecture" — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices
- Best practices for Lakeflow Spark Declarative Pipelines, section "Choose between triggered and continuous pipeline mode" — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices
- Best practices for Lakeflow Spark Declarative Pipelines, section "Use declarative CDC instead of imperative MERGE" — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices

---

| Field | Value |
|:------|:------|
| Version | 0.1 (draft) |
| Last Updated | 2026-07-09 |
