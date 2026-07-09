# ADR-002 — Deployment unit: Databricks Asset Bundles, not Terraform (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | Platform / DevOps engineering |
| Informed | Wider data team |

---

## Context

We need a way to define, version and deploy jobs, pipelines and their configuration
as code, and to promote them consistently across environments. The choice of tooling
sets the shape of every bundle, the CI/CD pipeline and the team's learning curve, so
it is a foundational decision made once.

---

## Options evaluated

**Option A — Databricks Asset Bundles**
Bundles (Declarative Automation Bundles) package source and YAML configuration into a
single deployable unit, validated and deployed with the `databricks bundle` CLI.
Native to Databricks and its current recommended default.

**Option B — Terraform (databricks provider)**
A general infrastructure-as-code tool with a Databricks provider. Strong if the
organisation already standardises all infrastructure on Terraform, but heavier for
day-to-day data workloads and requires separate state management.

**Option C — Notebooks and manual jobs via Git folders**
Lowest ceremony, but no reproducible infrastructure definition and no clean promotion
path between environments.

**Options not pursued**
- DAB plus Terraform hybrid (Terraform for workspace and platform infrastructure, DAB
  for data workloads): sensible at larger scale, deferred until platform infrastructure
  grows beyond workspace basics. Revisit in a follow-up ADR if that happens.

---

## Decision

**Option A chosen. All deployable workloads are Databricks Asset Bundles, deployed
through the Databricks CLI in Azure DevOps.**

### Rationale

| Criterion | Option A | Option B | Option C |
|:----------|:---------|:---------|:---------|
| Databricks-recommended default | Yes | No | No |
| Code and config in one unit | Yes | Partly | No |
| CLI-driven CI/CD | Yes | Yes | Manual |
| Reproducible promotion | Yes | Yes | No |
| Breadth of infrastructure covered | Databricks resources | Broad | None |
| Learning curve for the team | Low | Medium | Lowest |

For a team whose work is entirely Databricks jobs and pipelines, bundles give the
tightest fit and the shortest path from source to a validated deployment. Terraform's
breadth is not needed while the scope is workspace-internal workloads.

Decision basis: the CI/CD best-practices page recommends Declarative Automation Bundles
(or Terraform) on Azure, and the Lakeflow best-practices "Manage pipelines with CI/CD
and Declarative Automation Bundles" section recommends bundles for pipeline deployment.

---

## Validation

Every job and pipeline is defined inside a bundle. `databricks bundle validate` runs
on every pull request and must pass. No job or pipeline is created in a workspace
outside a bundle. Any exception (for example a workload that genuinely needs Terraform)
is recorded as a follow-up ADR.

---

## Consequences

- All workloads live in bundles under the monorepo (see ADR-003).
- The team learns the Databricks CLI and bundle configuration.
- CI/CD is built around `bundle validate` and `bundle deploy`.
- If platform-level infrastructure need grows, revisit the deferred DAB plus Terraform
  hybrid in a new ADR rather than reworking this one.

---

## Sources

- Best practices and recommended CI/CD workflows on Databricks — https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/best-practices
- Best practices for Lakeflow Spark Declarative Pipelines, section "Manage pipelines with CI/CD and Declarative Automation Bundles" — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices

---

| Field | Value |
|:------|:------|
| Version | 0.1 (draft) |
| Last Updated | 2026-07-09 |
