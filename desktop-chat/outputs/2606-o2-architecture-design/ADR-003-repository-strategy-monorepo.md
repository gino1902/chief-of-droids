# ADR-003 — Repository strategy: single monorepo with independently deployable bundles (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | DE team |
| Informed | Platform / DevOps engineering |

---

## Context

One data engineering team owns the three medallion layers (see ADR-001): bronze
ingestion per data producer, silver conforming per subject area, and gold per use case.
We need a repository layout that keeps these many bundles manageable, lets them share
common code, and still deploys each independently.

---

## Options evaluated

**Option A — Single monorepo, many bundles, shared folder**
All bundles live in one repository under grouping folders, alongside a shared
`common/` folder synced into bundles with `sync.paths`. This is the Databricks
recommended layout for storing many bundles.

**Option B — One repository per bundle or data product**
Strong isolation and independent cadence per repository. Justified when separate teams
own separate products, which is not our case; here it adds cross-repo coordination
cost with no offsetting benefit.

**Option C — Hybrid, a platform repo plus product repos**
A shared platform repo plus per-product repos. More moving parts, warranted only when
consuming teams are independent, which they are not.

**Options not pursued**
- A single large bundle covering everything: Databricks explicitly recommends small,
  focused bundles over one monolith.

---

## Decision

**Option A chosen. One monorepo, one bundle per producer and per use case, each
independently deployable, sharing a `common/` library via `sync.paths`.**

### Rationale

| Criterion | Option A | Option B | Option C |
|:----------|:---------|:---------|:---------|
| Fits single-team ownership | Yes | Overhead | Overhead |
| Shared code reuse | Native (sync.paths) | Duplicated or packaged | Packaged |
| Independent deployment per bundle | Yes | Yes | Yes |
| One place to version and review | Yes | No | Partly |
| Coordination cost | Low | High | High |

The whole estate is owned by one team and changes together, so one repository keeps
review and versioning in one place while `sync.paths` still gives per-bundle
deployment identities and shared code.

Decision basis: the "Sharing bundles and bundle files" page, section "Repository
structure", states the recommendation to store many bundles in one repository with a
shared folder, and the "Developer best practices" page recommends small, focused
bundles owned per team.

---

## Validation

Each bundle deploys on its own with `databricks bundle deploy`, and a change to one
bundle does not redeploy others. `sync.paths` references to `common/` resolve, and
`databricks bundle validate` passes for every bundle in CI.

---

## Consequences

- Top-level layout carries the three layers: `common/`, `ingestion/<producer>/`,
  `silver/<subject_area>/`, `use_cases/<use_case>/`, plus `docs/` and the Azure DevOps
  pipeline files. Producer bundles own bronze only, silver bundles own the conformed
  enterprise view, use-case bundles own gold (see ADR-001).
- The two-level grouping means shared references resolve as `../../common`, an accepted
  trade for clearer top-level intent.
- Bundles are independently deployable despite sharing a repository.
- Resource files follow the `<name>.pipeline.yml` and `<name>.job.yml` naming
  convention.

---

## Sources

- Sharing bundles and bundle files, section "Repository structure" — https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing
- Sharing bundles and bundle files, section "Configuration for file sharing" — https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing
- Developer best practices on Databricks — https://docs.databricks.com/aws/en/developers/best-practices

---

| Field | Value |
|:------|:------|
| Version | 0.1 (draft) |
| Last Updated | 2026-07-09 |
