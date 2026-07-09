# Technical design topic map

> Scope map for the companion technical design doc that follows ADR-001 to 009.
> Groups the design topics by cluster, references the governing ADR, and marks each
> topic as a decision still to make or an ADR decision to execute.
> Pairs with ADR-INDEX.md.

Legend:

- **Execute** - apply a decision already locked in an ADR. No new choice, only design detail that renders the decision.
- **Decide** - an open design decision this doc must make. The ADR sets the frame; the specific is still open.
- **Mixed** - part execution, part an open decision, split in the task text.

## Foundation

| Topic | ADR | Design task |
|:------|:----|:------------|
| Logical medallion model and layer ownership, end-to-end flow | ADR-001 | Execute: render the bronze to silver to gold flow and the producer/subject-area/use-case boundaries |
| Repository and bundle topology | ADR-002, ADR-003 | Mixed. Execute: the monorepo layout, `sync.paths` common, resource naming. Decide: how silver decomposes into subject-area bundles |
| Unity Catalog organisation | ADR-006 | Decide: schema naming per producer, subject area and use case; volume scoping; external-location layout |

## Layer designs

| Topic | ADR | Design task |
|:------|:----|:------------|
| Bronze ingestion, ADLS Gen2 | ADR-008 | Execute: apply the locked Auto Loader managed-file-events design. Decide: final trigger config from pull cadence and freshness target |
| Bronze ingestion, SharePoint bridge | ADR-009 | Execute: apply the locked standard-connector design and the ADLS migration path. Decide: resolve the residual `singleVariantColumn` + `databricks.connection` test |
| Silver conforming layer | ADR-001, ADR-005, ADR-007 | Decide: conformed entity and subject-area model, keys, CDC targets, expectation policy per table, modelling approach (3NF / Data Vault / normalised) |
| Gold layer | ADR-001, ADR-007 | Decide: per-use-case dimensional models, aggregates and serving surfaces |

## Build and run

| Topic | ADR | Design task |
|:------|:----|:------------|
| Compute model | ADR-004, ADR-005 | Mixed. Execute: serverless everywhere. Decide: triggered cadence per pipeline and ingestion-frequency cost controls |
| Pipeline and code structure | ADR-005, ADR-007 | Decide: package and module boundaries, the thin-pipeline-over-wheel pattern, `src`/`tests`/`fixtures` layout |
| Orchestration | ADR-005, ADR-008, ADR-009 | Decide: inter-layer trigger and dependency wiring (how silver runs off bronze, gold off silver), trigger choice per pipeline |
| Data layout and performance | ADR-007, ADR-008 | Mixed. Execute: `CLUSTER BY AUTO`. Decide: explicit clustering keys where AUTO is not used, and the promoted-column set per table |

## Configuration, delivery, governance

| Topic | ADR | Design task |
|:------|:----|:------------|
| Parameterisation and config | ADR-006, ADR-007 | Decide: the variable schema (`variables.yml`), per-target override set, personal dev-schema mechanism |
| CI/CD | ADR-002, ADR-006 | Mixed. Execute: the dev to staging to prod promotion model and approval gate. Decide: the Azure DevOps pipeline design, service-principal auth, secrets store |
| Security, network and compliance | ADR-006, ADR-008, ADR-009 | Decide: network topology (private endpoints), encryption keys (platform vs CMK), grant model detail, secrets management. Standing checks are the input |
| Observability | ADR-005 | Decide: monitoring and alerting design (event-log queries, quality dashboards, event hooks, rollback). Largely greenfield |

## Cross-cutting

| Topic | ADR | Design task |
|:------|:----|:------------|
| Data contracts between layers and with producers | ADR-001, ADR-008, ADR-009 | Decide: the contract spec (schema, keys, casing, VARIANT promotion rules, provenance) |
| Naming conventions | ADR-003, ADR-006 | Decide: the full naming standard for bundles, resources, catalogs, schemas and tables |
| Testing strategy | ADR-007, ADR-009 | Decide: unit and integration approach on the wheel, plus the SharePoint empirical test |
| Lifecycle and open risks | ADR-008, ADR-009 | Execute: capture the risk register (SharePoint bridge retirement, Beta review dates, VARIANT Public Preview, DBR floors, standing checks, supersession triggers) |

---

| Field | Value |
|:------|:------|
| Version | 1.0 |
| Last Updated | 2026-07-09 |
| Status | Draft |
