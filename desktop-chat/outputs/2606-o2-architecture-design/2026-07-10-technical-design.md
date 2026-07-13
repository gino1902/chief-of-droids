# Technical design

> Living companion to ADR-001 to 009. The ADRs are the frozen why; this is the how and
> how-it-fits-together, kept current as the platform evolves.
> Scope and cluster order follow 2026-07-09-technical-design-topic-map.md.
> Reference skeleton: artefacts/.

Status of clusters: Foundation is worked below. The rest are stubbed and pull from the
topic map as they are decided.

Proposals in this doc are marked where a sensible default is offered for confirmation.
Genuinely open items are marked 🔲 To be defined.

---

## 1. Foundation

### 1.1 Unity Catalog naming

One catalog per environment (ADR-006). A platform prefix avoids collisions if the
metastore is shared.

| Object | Convention | Example |
|:-------|:-----------|:--------|
| Catalog | `<platform>_<env>`, env in dev / staging / prod | `o2_dev`, `o2_prod` |
| Bronze schema | `<producer>_bronze` | `salesforce_bronze` |
| Silver schema | `<subject_area>_silver` | `customer_silver` |
| Gold schema | `<use_case>_gold` | `churn_gold` |
| Dev per-user schema | `${workspace.current_user.short_name}_<schema>` | `gino_salesforce_bronze` |
| Table | business entity in snake_case, no layer suffix (schema carries the layer) | `orders`, `order_enriched` |
| Provenance columns (convention) | `_ingested_at`, `_source_file` on bronze; sourced from the `_metadata` column the docs expose (e.g. `_metadata.file_name`) | |

Proposal: the layer lives in the schema name, not the table name, so the same entity
reads cleanly across layers (`salesforce_bronze.orders` to `customer_silver.order_enriched`).

External locations and volumes (ADR-008, UC best practices):

- One external location per storage container (a broad path). Enable file events on it,
  which the docs say improves Auto Loader and file-arrival triggers.
- The raw landing zone is an external volume registered at a per-producer prefix under
  the external location. External volumes are the doc-recommended registration for
  landing and ingestion areas. Never register a volume or table at the external-location
  root (it blocks any further registration under that location).
- Bronze, silver and gold tables are managed tables, the Databricks default for all new
  tables. Prefer catalog-level managed storage.
- Volume naming: `<producer>_landing` in the producer's bronze schema.

Environment isolation (resolved against UC best practices):

- One metastore per region (a Databricks constraint), shared by all workspaces in that
  region. The catalog is the isolation unit, so dev, staging and prod are separate
  catalogs in that one metastore, not separate metastores. Separate metastores are only
  for regional or data-sovereignty needs.
- Bind the prod catalog, and the prod external locations, to the prod workspace so
  production data is unreachable from dev or staging even if an identity is misconfigured.

🔲 To be defined: the platform prefix value.

### 1.2 Silver subject-area decomposition

Silver is organised by subject area, not by producer (ADR-001). A subject area is a
business-entity domain (customer, order, product, finance), and one silver bundle owns
one subject area. Each subject area reads one or more bronze producer schemas, so the
mapping is many-to-many.

Rules:

- Name subject areas after conformed business entities, never after a source system.
  A producer-shaped silver is the anti-pattern ADR-001 rejects.
- Start with a small set aligned to the core entities the use cases share. Split later
  if one becomes too broad.
- A conformed entity is defined once, in the silver subject area that owns it, and every
  gold use case consumes it. No re-conforming in gold.

Producer-to-subject-area matrix (illustrative, 🔲 to be defined with the business):

| Subject area | Reads from (bronze producers) |
|:-------------|:------------------------------|
| customer | salesforce, billing |
| order | salesforce, web_events |
| product | pim |

### 1.3 Bundle and resource naming

| Item | Convention | Example |
|:-----|:-----------|:--------|
| Bronze bundle | `ingest_<producer>` | `ingest_salesforce` |
| Silver bundle | `silver_<subject_area>` | `silver_customer` |
| Gold bundle | `gold_<use_case>` | `gold_churn` |
| Resource files | `<name>.pipeline.yml`, `<name>.job.yml` (ADR-003) | `salesforce.pipeline.yml` |
| Pipeline resource key | `<producer>_ingest`, `<subject_area>_conform`, `<use_case>_gold` | `salesforce_ingest` |
| Job resource key | `<pipeline_key>_job` | `salesforce_ingest_job` |
| Python package | matches the bundle's domain, one package per bundle under `src/` | `salesforce`, `customer` |

### 1.4 Ownership and grants (UC best practices)

Governs how the naming above is secured. Complements the per-bundle permissions in ADR-006.

- Assign ownership of production catalogs and schemas to groups, not individual users.
- Jobs run as service principals, and direct `MODIFY` on production tables is reserved
  for service principals, so a person cannot overwrite production by accident.
- Grant `USE CATALOG` and `USE SCHEMA` only to principals who should query the data.
  Grant `BROWSE` on catalogs to all account users for discoverability, and configure
  access-request destinations so users can request access to what they discover.
- Business teams get read-only grants on the gold schemas for their use case, and on
  silver where needed (ADR-001).

---

## 2. Layer designs

🔲 To be defined. Bronze is largely execution (ADR-008, ADR-009 and their locked design
docs). Silver conformed-entity models and gold dimensional models are Decide items in
the topic map, worked per subject area and per use case.

## 3. Build and run

🔲 To be defined. Compute (serverless, ADR-004) and packaging (thin pipelines over a
tested wheel, ADR-007) are executed in the skeleton. Inter-layer orchestration wiring
(how silver runs off bronze, gold off silver) is the open Decide item; the skeleton uses
a schedule as a placeholder.

## 4. Configuration, delivery, governance

🔲 To be defined. Variable schema, CI/CD pipeline detail (ADR-002, ADR-006, executed in
the skeleton), security and network topology, and observability.

## 5. Cross-cutting

🔲 To be defined. Data contracts between layers and with producers, the full naming
standard (started in 1.1 and 1.3), the testing strategy, and the lifecycle risk register.

---

## Sources

Sources for the sections written so far, following the ADR convention of citing only
what was used. This grows as clusters are filled. ADR-001 to 009 carry their own
sources and are not repeated here.

- What is the medallion lakehouse architecture (Azure Databricks) — https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion
- Unity Catalog best practices (Azure Databricks) — https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/best-practices
- Sharing bundles and bundle files, resource naming and sync.paths — https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing

---

| Field | Value |
|:------|:------|
| Version | 0.2 (draft) |
| Last Updated | 2026-07-10 |
| Status | Draft |
