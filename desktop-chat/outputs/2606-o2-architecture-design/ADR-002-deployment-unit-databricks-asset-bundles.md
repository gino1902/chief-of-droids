# ADR-002 — Deployment unit: Databricks Asset Bundles, not Terraform (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | Platform / DevOps engineering |
| Informed | Wider data team |
| Revised | 2026-08-06, see Revision note |

---

## Revision note, 2026-08-06

The decision named Azure DevOps as the CI platform. The toolchain moved to GitLab, so that
clause is corrected here. This record is the only home for the CI platform choice: ADR-003
carried a duplicate mention in its layout consequences, which caused that whole record to be
treated as deprecated when the platform changed. That mention has been removed and ADR-003
now points here.

Two things were separated in the process. The deployment unit, bundles rather than Terraform,
is vendor-recommended and unaffected by the CI platform. The CI platform is our choice and
carries a cost recorded below, because GitLab is not among the integrations Databricks
documents.

Editing rather than superseding is legitimate only because the status is Draft.

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

**Option A chosen. All deployable workloads are Databricks Asset Bundles, deployed through
the Databricks CLI. The CI platform driving that CLI is GitLab.**

The two halves have different standing and should not be conflated. Bundles as the
deployment unit is the vendor's recommendation. GitLab as the CI platform is an
organisational choice that Databricks does not document, so it carries the cost recorded
under Consequences.

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

Decision basis for the deployment unit. The CI/CD overview page states verbatim:

> Declarative Automation Bundles are the recommended approach to CI/CD on Databricks.

It positions the Terraform provider for provisioning workspaces and infrastructure rather
than for resources, which is exactly the split behind the deferred hybrid option above. The
Lakeflow best-practices section "Manage pipelines with CI/CD and Declarative Automation
Bundles" recommends bundles for pipeline deployment.

Decision basis for the CI platform, stated honestly. There is none from the vendor. Verified
2026-08-06, the CI/CD overview names only three deployment integrations:

> Deploy changes to the Azure Databricks workspace using Declarative Automation Bundles with
> tools like Azure DevOps, GitHub Actions, or Jenkins.

GitLab appears nowhere on that page, and no Databricks walkthrough for GitLab CI exists
alongside the Azure DevOps, GitHub Actions and Jenkins ones. The list reads as illustrative
rather than exhaustive, and the underlying mechanism is the Databricks CLI, which any runner
can invoke. So GitLab is workable but unpaved.

---

## Validation

Every job and pipeline is defined inside a bundle. `databricks bundle validate` runs on every
merge request and must pass. No job or pipeline is created in a workspace outside a bundle.
CI authenticates without a long-lived secret. Any exception (for example a workload that
genuinely needs Terraform) is recorded as a follow-up ADR.

---

## Consequences

- All workloads live in bundles under the monorepo (see ADR-003).
- The team learns the Databricks CLI and bundle configuration.
- CI/CD is built around `bundle validate` and `bundle deploy`.
- If platform-level infrastructure need grows, revisit the deferred DAB plus Terraform
  hybrid in a new ADR rather than reworking this one.
- The GitLab CI configuration is written from the CLI upward, without a vendor walkthrough to
  follow. Budget for that, and treat the Azure DevOps and Jenkins guides as the reference
  shape to translate rather than as instructions.
- Authentication is the first thing to get right, and the documentation names the preferred
  answer: OAuth token federation, described as workload identity federation that "eliminates
  the need for Databricks secrets, making it the most secure way to authenticate to
  Databricks". Service principals for CI/CD are the alternative. A long-lived personal access
  token in a GitLab variable is the pattern to avoid.
- Lint tooling diverges from the bootstrap conventions and should be reconciled deliberately.
  This page names Pylint with the Databricks Labs pylint plugin for enforcing coding standards
  on Databricks code, while `bootstrapping-project` sets ruff for a data goal and flags its own
  ruff claim as unverified. Either is defensible; the point is that the vendor names Pylint, so
  choosing ruff is a deviation to make on purpose rather than by omission.

---

## Sources

| Source | Bears on | Verified |
|:-------|:---------|:---------|
| [CI/CD on Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/) | Bundles as the recommended CI/CD approach; the three named deployment integrations, which exclude GitLab; OAuth token federation as the most secure authentication; Terraform positioned for infrastructure rather than resources; Pylint named for code standards | 2026-08-06 |
| [Best practices and recommended CI/CD workflows on Databricks](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/best-practices) | CI/CD workflow recommendations | 2026-07-09 |
| [Best practices for Lakeflow Spark Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices), section "Manage pipelines with CI/CD and Declarative Automation Bundles" | Bundles for pipeline deployment | 2026-07-09 |

> ⚠️ Absence of evidence, recorded deliberately. GitLab is not named on the CI/CD overview and
> has no Databricks walkthrough. That is a verified absence as of 2026-08-06, not an inference,
> and it may change. Re-check before treating the GitLab wiring as unsupported.

Version history is git. This record carries no version field.
