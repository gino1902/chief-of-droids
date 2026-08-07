# ADR-001 — Medallion layer roles and ownership: bronze source-aligned, silver cross-source, gold per business domain (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | Business use-case owners |
| Informed | Wider data team |
| Revised | 2026-08-06, see Revision note |

---

## Revision note, 2026-08-06

Two corrections, both of the same kind: this record said more than it decided.

**Gold was written as per use case, and its own source says otherwise.** The decision basis
below quotes the medallion page as saying gold "models a business domain", with "multiple gold
layers to meet different business needs". Business domain, not use case. The record cited a
domain-shaped statement and wrote a use-case-shaped rule. Use cases are how gold is delivered,
one after another, not how it is partitioned. The rule is corrected; the basis quote is
unchanged because it was right all along.

**Deployment units were asserted, never argued.** The record stated one bundle per producer,
per subject area and per use case, inside a decision about what the layers mean and who owns
them. Those are two different questions, and the second was never put to options. Layer
semantics stay here. How many bundles they become moves to the tree contract, where it can be
argued against the vendor's own sizing criteria rather than inherited from a phrase.

Neither correction changes the decision this record actually made: conforming happens once, in
silver, and gold never re-conforms from bronze.

**Third correction, 2026-08-07, following ADR-011.** Bronze was described as being organised
"per data producer" with the producer as its *semantic* boundary. ADR-011 subsequently placed the
ingestion contract on entities and recorded the producing system as a mapping rather than as the
contract. Bronze remains source-aligned, which is a structural fact about how records arrive, but
that alignment is no longer a semantic claim. The wording is corrected and the cross-reference to
ADR-011 added, which this record previously lacked.

Editing rather than superseding is legitimate only because the status is Draft.

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

**Option A — Bronze source-aligned, silver as the shared cross-source conforming layer, gold per business domain**
Bronze is raw and source-aligned, organised along the supply path. Silver reads one or more
bronze tables and produces the validated, conformed enterprise view of each entity,
organised by subject area rather than by producer. Gold aggregates from silver, organised
by the business domain it serves and delivered one use case at a time. Conforming happens
once, in silver.

<!-- This option was originally written as "gold per use case". Corrected 2026-08-06 so
the option and the Decision agree, since the source cited in the basis says gold "models a
business domain". The substance of what was evaluated is unchanged: gold aggregates from
silver and never re-conforms from bronze. -->

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

- **Bronze, source-aligned.** Raw, minimal validation, appended incrementally, organised
  along the supply path it arrives on. Consumed only by silver, not by analysts. The
  alignment is *structural*, a fact about how records arrive, not a semantic contract:
  ADR-011 places the contract on entities and records the producing system as a mapping.
  How many bundles this maps to is not decided by this record, see the Revision
  note.
- **Silver, shared cross-source transformation layer.** Reads one or more bronze (or
  silver) tables and performs cleansing, deduplication, normalisation and joins to
  produce the enterprise view of each entity. Organised by subject area, not by
  producer. Never written directly from ingestion. This is the home of conformed
  definitions.
- **Gold, per business domain, delivered use case by use case.** Aggregations and
  dimensional models built from silver, organised by the business domain they serve.
  Multiple golds by business need. Use cases are the increment of *delivery*, not the
  unit of *partition*: the first use case in a domain creates that domain's gold, and
  later use cases in the same domain add to it. Corrected 2026-08-06, see the Revision
  note.

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

- Bronze owns raw data only and is source-aligned along the supply path (see ADR-008,
  ADR-009). What O2 commits to ingest is a set of entities, not a set of producers, and
  the producing system is configuration (see ADR-011).
- Silver owns the conformed enterprise view, organised by subject area; it is a distinct
  layer, never part of an ingestion boundary.
- Gold builds only on silver, never on bronze, and is organised by business domain.
- How many bundles these three layers become, and the repository layout that
  carries them, are not settled here. Layout belongs to ADR-003 and the count belongs to
  the tree contract. This record previously asserted both, which is how a layer-semantics
  decision came to own a question about bundles it never argued.
- Conformed entity tables live in silver; shared transformation and metric functions
  live in the `common/` package (see ADR-007).
- Business teams get read-only grants on the gold schemas relevant to their use case,
  and where needed on silver.

---

## Sources

| Source | Bears on | Verified |
|:-------|:---------|:---------|
| [What is the medallion lakehouse architecture?](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion) | Silver reads one or more bronze or silver tables and brings sources into an enterprise view; do not write to silver directly from ingestion; gold "models a business domain" with "multiple gold layers to meet different business needs" | 2026-07-09 |
| [Best practices for Lakeflow Spark Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices), section "Organize pipelines with the medallion architecture" | Separating ingestion from transformation | 2026-07-09 |

Version history is git. This record carries no version field.
