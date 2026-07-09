# ADR-006 — Environments: dev, staging and prod on three workspaces (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | Platform / Cloud team, Security |
| Informed | Wider data team |

---

## Context

We need environment separation that isolates production from development work, gives a
place to integration-test before release, and lets developers work without colliding
with each other. This drives the bundle targets, the catalog model and the branching
strategy.

---

## Options evaluated

**Option A — Three environments on three workspaces**
Separate dev, staging and prod workspaces, expressed as bundle targets, with a Unity
Catalog catalog per environment. Dev uses development mode with per-user personal
schemas in a shared dev catalog. This matches the Databricks CI/CD workflow and
best-practice guidance.

**Option B — Two environments (dev and prod)**
The bundle template default. Lighter, but there is no staging gate before production,
which is risky for a platform serving business consumers.

**Option C — One workspace, separated only by catalog**
Cheapest, but no blast-radius isolation, so a production incident can affect
development.

**Options not pursued**
- A workspace per developer: costly and unnecessary, since personal schemas already
  isolate developers within the shared dev workspace.

---

## Decision

**Option A chosen. Three targets and three workspaces, catalog per environment, dev in
development mode with personal schemas. Trunk-based branching: a feature branch deploys
to a personal dev pipeline in the dev catalog, merge to main validates and deploys to
staging, and a tag or manual approval deploys to prod. The prod target uses a
restricted `root_path` off `/Shared` and runs as a service principal.**

### Rationale

| Criterion | Option A | Option B | Option C |
|:----------|:---------|:---------|:---------|
| Isolates prod from dev | Yes | Yes | No |
| Staging gate before prod | Yes | No | No |
| Developer isolation | Yes (personal schemas) | Yes | Weak |
| Cost | Higher | Medium | Lowest |
| Matches Databricks CI/CD workflow | Yes | Partly | No |

A platform serving business consumers needs a staging gate and hard prod isolation.
The added workspace cost buys exactly that, and personal schemas remove developer
collisions without per-developer workspaces.

Decision basis: the Lakeflow best-practices "Use bundle targets for environment
isolation" section describes the dev, staging, prod promotion workflow, and the CI/CD
best-practices page calls for separate dev, staging and production workspaces. The
templates page provides development mode and personal schemas; the sharing page,
section "Permissions for shared bundles", provides the production `root_path` and
`run_as` pattern.

---

## Validation

Each `databricks.yml` defines dev, staging and prod targets, with the catalog overridden
per target. Dev sets development mode and personal schemas. The prod target sets a
restricted `root_path` and a service principal `run_as`. The Azure DevOps prod stage
has a manual approval gate. `databricks bundle validate` passes for each target.

---

## Consequences

- Three workspaces to provision and govern.
- Per-target catalog values live in `common/variables.yml`.
- Developers are isolated by personal schemas in the shared dev catalog.
- Promotion follows dev to staging to prod, gated by an approval before production.
- Each bundle carries a top-level permissions block (CAN_VIEW all, CAN_MANAGE the DE
  group, CAN_RUN the deployment service principal).

---

## Sources

- Best practices for Lakeflow Spark Declarative Pipelines, section "Use bundle targets for environment isolation" — https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices
- Best practices and recommended CI/CD workflows on Databricks — https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/best-practices
- Declarative Automation Bundles project templates (development mode, personal schemas, default catalog) — https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/templates
- Sharing bundles and bundle files, section "Permissions for shared bundles" — https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing

---

| Field | Value |
|:------|:------|
| Version | 0.1 (draft) |
| Last Updated | 2026-07-09 |
