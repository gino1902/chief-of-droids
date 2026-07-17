# ADR index — Azure Databricks platform architecture

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Scope | Data engineering platform on Azure Databricks with Azure DevOps CI/CD |

This is a standalone decision log for the Databricks platform, numbered from ADR-001.
It is independent of the unrelated ADR-001 in the repository's `docs/decisions/`.

---

## Records

| ADR | Decision | Status |
|:----|:---------|:-------|
| [ADR-001](ADR-001-medallion-layer-ownership.md) | Medallion layer roles and ownership: bronze per producer, silver cross-source conforming, gold per use case | Draft |
| [ADR-002](ADR-002-deployment-unit-databricks-asset-bundles.md) | Databricks Asset Bundles as the deployment unit, over Terraform | Draft |
| [ADR-003](ADR-003-repository-strategy-monorepo.md) | Single monorepo with independently deployable bundles and a shared library | Draft |
| [ADR-004](ADR-004-compute-serverless.md) | Serverless compute for all pipelines and jobs | Draft |
| [ADR-005](ADR-005-orchestration-declarative-pipelines-jobs.md) | Declarative pipelines for logic, jobs to orchestrate, bronze split from transform | Draft |
| [ADR-006](ADR-006-environments-dev-staging-prod.md) | Dev, staging and prod on three workspaces, with per-user dev isolation | Draft |
| [ADR-007](ADR-007-pipeline-code-python-wheel-dataset-types.md) | Python pipelines over a tested wheel, dataset types fixed per layer | Draft |
| [ADR-008](ADR-008-adls-bronze-ingestion.md) | ADLS Gen2 to bronze via Auto Loader with managed file events, file-arrival trigger plus availableNow drain | Accepted |
| [ADR-009](ADR-009-sharepoint-bronze-ingestion.md) | SharePoint to bronze via the standard connector, scheduled drain, as a temporary bridge to ADR-008 | Draft |
| [ADR-010](ADR-010-middleware-o2-boundary.md) | Middleware and O2 boundary: canonical SQLI data contracts, one-way inbound | Draft |

---

## How the records relate

ADR-001 sets the three-layer ownership model (bronze per producer, silver as the shared
cross-source conforming layer, gold per use case), and ADR-007 makes the silver layer
real by giving its conforming logic a tested package to live in. ADR-002 and ADR-003 set
the tooling and repository shape that every other record assumes. ADR-004, ADR-005 and
ADR-007 together define how workloads are built and run. ADR-006 defines where they run
and how they are promoted.

Two layout conventions are embedded rather than given their own records: resource file
naming (`<name>.pipeline.yml`, `<name>.job.yml`) sits in ADR-003, and the per-bundle
permissions model with production hardening sits in ADR-006.

ADR-008 and ADR-009 are source-specific ingestion decisions. Each is a concise record
that references its full locked design document in this folder rather than duplicating
it. ADR-009 is a temporary bridge that retires into ADR-008 when the source repoints to
ADLS Gen2.

ADR-010 consolidates the middleware and O2 boundary. It grounds on ADR-001 (medallion
ownership) and ADR-009 (the implemented SharePoint-to-bronze pattern), and states the
boundary as canonical SQLI data contracts that O2 subscribes to.

---

## Sources

Each record lists, in its own Sources section, only the documents behind its options
and decision. The documents used across the set are:

- Best practices for Lakeflow Spark Declarative Pipelines — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices
- Best practices and recommended CI/CD workflows on Databricks — https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/best-practices
- Sharing bundles and bundle files — https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing
- Declarative Automation Bundles project templates — https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/templates
- Developer best practices on Databricks — https://docs.databricks.com/aws/en/developers/best-practices

---

## Open items before lock-in

- `Task` field is TBD on every record, to be filled once ticketed.
- Decision-maker is a placeholder (Gino), and the consulted parties vary by record and
  need confirming.
- Status is Draft throughout. Moving to Decided is the lock-in step.

---

| Field | Value |
|:------|:------|
| Version | 0.3 (draft) |
| Last Updated | 2026-07-17 |
