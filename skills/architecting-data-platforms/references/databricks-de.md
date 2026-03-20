# Databricks — Data Engineering Reference

All version-sensitive claims in this file must be verified against official sources
before use. Do not treat this file as authoritative for API details, config syntax,
or feature availability.

Official sources:
- `docs.databricks.com`
- `docs.databricks.com/release-notes`
- `docs.delta.io`

---

## Compute Strategy

### Compute Type Selection

| Compute type | Use case | Cost profile |
| :--- | :--- | :--- |
| All-purpose cluster | Interactive dev, ad hoc analysis | High — long-lived, shared |
| Job cluster | Production scheduled jobs | Low — ephemeral, auto-terminated |
| DLT cluster | Delta Live Tables pipelines | Managed by runtime |
| SQL Warehouse (serverless) | SQL analytics, BI tool queries | Pay-per-query; preferred on Azure |

**Senior rule:** All-purpose clusters in production are a cost anti-pattern.
Every production workload should run on job clusters or SQL Warehouses.

### Cluster Auto-Termination

Stable principle — specific default values must be verified at `docs.databricks.com`:

- Auto-termination must be enabled on all all-purpose clusters and enforced via cluster policy
- Reduce termination timeout to match actual usage patterns — platform default is higher than most teams need
- Typical targets: 15–30 min for SQL/ad hoc; up to 60 min for interactive dev
- Never disable auto-termination on all-purpose clusters

---

## Delta Lake

⚠️ Fetch from `docs.delta.io` before advising on any of the following — all are
version-sensitive:

- Transaction log structure (`_delta_log/`), checkpoint behaviour, ACID guarantees
- `OPTIMIZE` and `ZORDER BY` syntax, scheduling recommendations
- `VACUUM` retention threshold defaults and time travel interaction
- Schema evolution options (`mergeSchema`, `ALTER TABLE`, `overwriteSchema`)
- Deletion vectors, liquid clustering (newer features — check runtime availability)

**Decision rules that do not require a fetch:**

- Schedule `OPTIMIZE` as a post-write job, not inline with ingestion
- Never drop and recreate a Delta table unless data loss is explicitly acceptable
- Coordinate `VACUUM` retention with any active time travel or streaming checkpoints

---

## Unity Catalog

⚠️ Fetch from `docs.databricks.com` before advising on hierarchy, privilege grants,
metastore constraints, or External Location configuration — these evolve with each
platform release.

**Decision rules that do not require a fetch:**

- Unity Catalog governs access at catalog/schema/table level via GRANT statements — grants to roles, not individuals
- External Locations replace mount points — always prefer for new workloads
- Row-level and column-level security requires Unity Catalog — not available in legacy Hive metastore
- Metastore root storage account is dedicated — do not co-locate application data
- 1 metastore per Azure region per account (verify current constraint at docs before advising)

---

## Ingestion Patterns

⚠️ Fetch from `docs.databricks.com` before advising on Auto Loader configuration,
COPY INTO syntax, or scale limits — capabilities change across runtime versions.

**Decision rules that do not require a fetch:**

- Auto Loader for continuous/streaming ingest where files arrive incrementally
- COPY INTO for periodic batch loads where idempotency is required
- For Event Hubs or Kafka integration, confirm connector version against active runtime at `docs.databricks.com/release-notes`

---

## DLT — Delta Live Tables

⚠️ Fetch from `docs.databricks.com` before advising on Expectations syntax, pipeline
modes (triggered vs continuous), or serverless DLT availability.

**Decision rules that do not require a fetch:**

- Use DLT when lineage, quality monitoring, and declarative pipeline management are required
- Use plain Notebooks + Workflows for exploratory or low-criticality pipelines
- Never mix DLT and plain notebook paradigms within the same pipeline
- DLT Expectations failures should be classified at design time: warn / drop / fail — not left as defaults
