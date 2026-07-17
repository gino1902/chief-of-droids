# ADR-001 — Medallion layer roles and ownership: bronze per producer, silver cross-source, gold per use case (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | Business use-case owners |
| Informed | Wider data team |

---

## Context

The platform organises data along the medallion architecture. Each layer needs a clear
role and a clear ownership boundary, because those boundaries drive the bundle layout,
the pipelines and the grants. A single data engineering team owns all three layers.
Business teams give requirements and consume gold read-only.

Data in the platform is classified on three axes:

- By layer: raw (bronze), conformed or enterprise (silver), curated and business-ready (gold).
- By authority: authoritative, a source of truth, versus derived.
- By purpose: analytical, the medallion layers, versus operational, a Lakebase OLTP table.

The decision with a known failure mode is where cross-source conforming happens. If
gold is built per use case straight from each producer's data, every use case re-does
the integration and the same business concept (active customer, revenue grain) drifts
apart across dashboards.

---

## Options evaluated

**Option A — Bronze per producer, silver as the shared cross-source conforming layer, gold per use case**
Bronze is raw and source-aligned, one boundary per producer. Silver reads one or more
bronze tables and produces the validated, conformed enterprise view of each entity,
organised by subject area rather than by producer. Gold aggregates from silver, one
boundary per business use case. Conforming happens once, in silver.

**Option B — Bronze and silver both per producer, integration deferred to gold**
Silver is source-scoped cleaning only, and cross-source joins happen in each use case's
gold. Rejected: it pushes conforming into every use case, duplicating logic and
reintroducing divergence, and it contradicts the medallion guidance that silver reads
from one or more bronze and provides the enterprise view.

**Option C — Central conformed gold layer owned by a curation team**
A dedicated function builds canonical gold for all use cases. Deferred: silver already
provides the conformed view without a separate team, and a central gold gate risks
becoming a bottleneck.

---

## Decision

**Option A chosen. Layer roles and ownership are:**

- **Bronze, per data producer.** Raw, minimal validation, appended incrementally, one
  bundle per producer. Consumed only by silver, not by analysts.
- **Silver, shared cross-source transformation layer.** Reads one or more bronze (or
  silver) tables and performs cleansing, deduplication, normalisation and joins to
  produce the enterprise view of each entity. Organised by subject area, not by
  producer. Never written directly from ingestion. This is the home of conformed
  definitions.
- **Gold, per business use case.** Aggregations and dimensional models built from
  silver, each serving one use case. Multiple golds by business need.

Divergence is now prevented structurally, not just by process: every gold builds on the
single silver enterprise view rather than re-conforming from bronze. A review of new
gold definitions remains as a backstop.

### Rationale

| Criterion | Option A | Option B | Option C |
|:----------|:---------|:---------|:---------|
| Home for cross-source conforming | Silver, once | Each use case | Central gold |
| Divergence risk | Low (structural) | High | Low |
| Per-use-case delivery speed | Fast | Fast | Slower (central gate) |
| Aligns with official medallion | Yes | No | Partly |
| Team / process overhead | Low | Low | High |

Option A matches the official medallion guidance exactly and removes divergence at the
structural level, because conforming lives in one shared layer that every use case
consumes.

Decision basis: the Azure Databricks medallion page states silver is built by reading
"one or more bronze or silver tables", brings "data from different sources into an
Enterprise view", and "does not recommend writing to silver tables directly from
ingestion"; and that gold "models a business domain", with "multiple gold layers to
meet different business needs".

---

## Validation

Gold pipelines read from silver, never directly from bronze. Cross-source conforming
logic exists once, in silver, and is not duplicated in gold. A new gold definition that
re-implements an existing silver concept requires explicit sign-off on the pull request.
`databricks bundle validate` passes.

---

## Consequences

- Bronze bundles are per producer and own raw data only (see ADR-003, ADR-008, ADR-009).
- Silver bundles are per subject area and own the conformed enterprise view; they are a
  distinct layer, not part of the producer bundle.
- Gold bundles are per use case and build only on silver.
- Repository layout carries three layers: `ingestion/`, `silver/`, `use_cases/`.
- Conformed entity tables live in silver; shared transformation and metric functions
  live in the `common/` package (see ADR-007).
- Business teams get read-only grants on the gold schemas relevant to their use case,
  and where needed on silver.

---

## Sources

- What is the medallion lakehouse architecture? (Azure Databricks) — https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion
- Best practices for Lakeflow Spark Declarative Pipelines, section "Organize pipelines with the medallion architecture" — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices

---

| Field | Value |
|:------|:------|
| Version | 0.3 (draft) |
| Last Updated | 2026-07-17 |
