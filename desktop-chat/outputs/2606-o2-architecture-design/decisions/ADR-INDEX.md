# ADR index — Azure Databricks platform architecture

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Revised | 2026-08-06, consistency sweep |
| Scope | Data engineering platform on Azure Databricks with GitLab CI/CD |

This is a standalone decision log for the Databricks platform, numbered from ADR-001.
It is independent of the unrelated ADR-001 in the repository's `docs/decisions/`.

> ⚠️ Nothing here is locked. Nine of the eleven records are Draft, so none of them may be
> treated as a constraint that cannot move. `writing-technical-design` requires a locked
> set, which is why the tree has not been generated. See
> [the carry-over note](../2026-08-06-carry-over-technical-design.md).
>
> Two records are Accepted: ADR-008 and ADR-009. Note that status and lifecycle are
> different axes and this table carries only status. ADR-008 is agreed but not yet running,
> ADR-009 is running but blocked on one unverified read composition. Reading the table for
> what is live will mislead.

This directory is the **substrate**: decision records and this index, nothing else. Design
documents, the artefact skeleton and the task tracker sit one level up on purpose, so a
conformance derivation reading this directory reads only decisions. See
[`../adr-conformance/`](../adr-conformance/) for the suite that tests this set.

---

## Records

| ADR | Decision | Status | Revised |
|:----|:---------|:-------|:--------|
| [ADR-001](ADR-001-medallion-layer-ownership.md) | Medallion layer roles and ownership: bronze source-aligned, silver cross-source conforming, gold per business domain | Draft | 2026-08-06, 2026-08-07 |
| [ADR-002](ADR-002-deployment-unit-databricks-asset-bundles.md) | Databricks Asset Bundles as the deployment unit, over Terraform, with GitLab as the CI platform | Draft | 2026-08-06 |
| [ADR-003](ADR-003-repository-strategy-monorepo.md) | Single repository with independently deployable bundles and a shared folder | Draft | 2026-08-06 |
| [ADR-004](ADR-004-compute-serverless.md) | Serverless compute for all pipelines and jobs | Draft | |
| [ADR-005](ADR-005-orchestration-declarative-pipelines-jobs.md) | Declarative pipelines for logic, jobs to orchestrate, bronze split from transform | Draft | |
| [ADR-006](ADR-006-environments-dev-staging-prod.md) | Dev, staging and prod on three workspaces, with per-user dev isolation | Draft | 2026-08-06 |
| [ADR-007](ADR-007-pipeline-code-python-wheel-dataset-types.md) | Python pipelines over a tested package, dataset types fixed per layer | Draft | 2026-08-06 |
| [ADR-008](ADR-008-adls-bronze-ingestion.md) | ADLS Gen2 to bronze via Auto Loader with managed file events, file-arrival trigger plus availableNow drain | Accepted | |
| [ADR-009](ADR-009-sharepoint-bronze-ingestion.md) | SharePoint to bronze via the standard connector, scheduled drain, as a temporary bridge to ADR-008 | Accepted, blocked | 2026-08-07 |
| [ADR-010](ADR-010-middleware-o2-boundary.md) | Middleware and O2 boundary: SQLI data contracts, one-way inbound | Draft, amended | 2026-08-04 |
| [ADR-011](ADR-011-ingestion-baseline-entity-contract.md) | Ingestion baseline: contract on entities, producing system as configuration | Draft | |
| [ADR-012](ADR-012-repository-tree-strategy.md) | Repository tree strategy: the tree's shape follows the work, not the data | Draft | |

> ⚠️ Numbering is not reconciled. ADR-011 is the highest number known to this session, but records
> are being written in parallel sessions, so 012 onward may already be claimed elsewhere. Reconcile
> against every in-flight session before assigning a number, and do not reserve numbers in advance.

Two records are scoped and unwritten, deliberately unnumbered until the reconciliation above:
**data ownership model** and **Unity Catalog isolation and domain boundary**. Both were split out of
an earlier single-record scope that bundled ownership, Unity Catalog mechanics and the application
role vocabulary. The role vocabulary is a convention rather than a decision and folds into ADR-011's
terminology.

---

## The 2026-08-06 consistency sweep

Five records were corrected after the CI toolchain moved to GitLab and after the bundle
sharing mechanism was verified against the documentation. What changed:

| Record | Correction |
|:-------|:-----------|
| ADR-001 | Two corrections on 2026-08-06 and a third on 2026-08-07. Gold contradicted its own source, which says gold "models a business domain": use cases are the increment of delivery, not the unit of partition. Deployment units were asserted without ever being argued and were removed. Then, following ADR-011, bronze's source alignment was reclassified from a semantic boundary to a structural fact, since the contract now sits on entities with the producing system as a mapping |
| ADR-003 | Was briefly treated as deprecated because it named Azure DevOps pipeline files in its layout consequences. That was wrong in scope and discarded a decision Databricks explicitly recommends. The record is retained, the CI clause is removed, and the mechanism by which shared code reaches a bundle is now stated |
| ADR-002 | Takes sole ownership of the CI platform choice, now GitLab. The deployment-unit half is vendor-recommended; the CI-platform half is unpaved, because Databricks documents Azure DevOps, GitHub Actions and Jenkins but not GitLab |
| ADR-007 | The delivery mechanism was wrong. A built wheel under `libraries` is the job pattern; pipelines take an editable install declared in `environment.dependencies`. Since jobs only orchestrate, no wheel is consumed at all. Aggregate quality constraints were also impossible as written and now route to a validation dataset plus a job dependency |
| ADR-006 | Approval gate expressed in GitLab terms, branching language aligned, `common/variables.yml` and the permissions block confirmed against the documented patterns, and the `/Shared` production path downgraded to unverified |

Two lessons from the sweep worth keeping:

A record that mentions a neighbouring concern in passing will be treated as owning it. ADR-003's
incidental CI mention nearly cost a vendor-recommended decision. One concern per record, and
cross-reference rather than restate.

Records can agree in prose and disagree in mechanism. ADR-003 and ADR-007 both described shared
code reaching a bundle and read as compatible while specifying different things. Naming the
mechanism explicitly is what surfaced it.

---

## How the records relate

ADR-001 sets the three-layer ownership model (bronze source-aligned along the supply path,
silver as the shared cross-source conforming layer, gold per business domain delivered use case
by use case), and ADR-007 makes the silver layer real by
giving its conforming logic a tested package to live in. ADR-002 and ADR-003 set the tooling and
repository shape that every other record assumes, and both were corrected in the sweep above, so
read their revision notes before relying on them. ADR-004, ADR-005 and ADR-007 together define
how workloads are built and run. ADR-006 defines where they run and how they are promoted.

Two layout conventions are embedded rather than given their own records: resource file naming
(`<name>.pipeline.yml`, `<name>.job.yml`) sits in ADR-003, and the per-bundle permissions model
with production hardening sits in ADR-006. Both would be easier to find as their own records;
that is a tidy-up, not a decision.

ADR-008 and ADR-009 are source-specific ingestion decisions. Each is a concise record that
references its full locked design document in this folder rather than duplicating it. ADR-009 is
a temporary bridge that retires into ADR-008 when the source repoints to ADLS Gen2.

ADR-011 sets what O2 treats as its ingestion baseline, and it grounds on three of the records
above: ADR-001 for the bronze-source-aligned and silver-conformed split that lets an entity
contract sit above a per-producer bronze, ADR-010 principle 5 for admitting entities as supply
paths appear, and ADR-009 for the disposable-bridge precedent. It is the first record whose
companion document is a locked C4 System Landscape describing what exists, rather than a locked
design proposing how to build.

ADR-010 consolidates the middleware and O2 boundary. It grounds on ADR-001 (medallion ownership)
and ADR-009 (the implemented SharePoint-to-bronze pattern). Its 2026-08-04 amendment records that
the contracts are not canonical, that canonicalisation is deferred with no owner, and three open
questions including whether middleware anonymisation destroys the only cross-producer join key.
The amendment is proposed and not agreed by the record's five decision-makers.

---

## What grounds the tree

The repository layout is a projection of the feed configuration, not of the taxonomy. Inputs are
[o2-data-sources](../../2607-o2-requirements/o2-data-sources.md) and
[domain-taxonomy](../../2607-o2-requirements/domain-taxonomy.md).

**ADR-012 decides what governs that projection**: a concept becomes structure only if it changes
when the organisation changes, and a directory becomes its own bundle only when it has its own
release gate. The count is an output of that rule, not a decision, and it moves as the
configuration moves. On the 2026-08-07 configuration it yields two bundles.

The paragraph below records why the count was unowned between 2026-08-06 and 2026-08-07, and is
kept so nobody reintroduces the removed rules.

**How many bundles that projection produces was not decided by any record here.** This
section previously stated a bundle per producer, a bundle per subject area and a bundle per use
case, giving two bronze, five silver and zero gold. All three rules came from ADR-001's
consequences, which asserted them without ever putting them to options, and they were removed from
that record on 2026-08-06 for exactly that reason. Restating them here would reintroduce through
the index what was removed from the record.

Two things are settled and worth keeping distinct from the count. Gold is organised by business
domain and delivered use case by use case, so a second use case in a domain adds tables rather
than a unit (ADR-001). And bronze alignment along the supply path is structural, not a semantic
contract, because the contract sits on entities with the producing system recorded as a mapping
(ADR-011).

Analysis exists that argues the count down sharply, on the vendor's own sizing criteria and on the
observation that all active feeds arrive through one connector from one site. It is not recorded
in any decision, so it is not cited here. Until a record carries it, the count is open.

---

## Open items before lock-in

- Status is Draft on nine of eleven records. Moving to Accepted is the lock-in step and the
  precondition for generating the tree. Locking is a deliberate non-goal for now, because
  freezing decisions that rest on unread payloads and an unresolved identity question would be
  worse than carrying them as Draft.
- ~~The bundle count is unowned.~~ Closed 2026-08-07 by ADR-012, which decides the rule rather
  than the number.
- The feed-to-entity mapping does not exist. ADR-011 admits an entity "when a supply path
  exists" and nothing records which feeds carry which entities, so that admission test cannot
  be evaluated. Two subdomains already have more entities than feeds.
- `Task` is TBD on every record, to be filled once ticketed.
- Decision-maker is a placeholder (Gino) on most records, and the consulted parties vary and need
  confirming. ADR-010 is the exception, carrying five named decision-makers, which is why its
  amendment needs their review rather than an edit.
- A slug rule for subject-area names to Python module names does not exist. `finance-fa&c` cannot
  become a module or bundle name as written. This blocks silver-layer generation.
- ADR-007's title still says "python wheel" while the record now says no wheel is built. Renaming
  a record is a bigger move than a sweep.
- ADR-009 remains blocked on one unverified read composition.
- Lint tooling is unsettled: Databricks names Pylint with their own plugin, `bootstrapping-project`
  sets ruff for a data goal and flags its own claim as unverified. Choose deliberately.

---

## Sources

Records list their own sources with verification dates. The documents used across the set:

| Source | Verified |
|:-------|:---------|
| [Sharing bundles and bundle files](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing) | 2026-08-06 |
| [Bundle library dependencies](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/library-dependencies) | 2026-08-06 |
| [Use a private artifact in a bundle](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/artifact-private) | 2026-08-06 |
| [CI/CD on Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/) | 2026-08-06 |
| [Best practices for Lakeflow Spark Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices) | 2026-07-09 |
| [Best practices and recommended CI/CD workflows on Databricks](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/best-practices) | 2026-07-09 |
| [Declarative Automation Bundles project templates](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/templates) | 2026-07-09 |
| [Developer best practices on Databricks](https://docs.databricks.com/aws/en/developers/best-practices) | 2026-07-09 |

Version history is git. This index carries no version field.
