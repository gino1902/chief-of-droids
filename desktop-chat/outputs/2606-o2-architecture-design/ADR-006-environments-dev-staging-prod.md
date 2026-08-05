# ADR-006 — Environments: dev, staging and prod on three workspaces (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | Platform / Cloud team, Security |
| Informed | Wider data team |
| Revised | 2026-08-06, see Revision note |

---

## Revision note, 2026-08-06

Two corrections, one confirmation, one claim downgraded.

The validation named an Azure DevOps stage for the production approval gate. The toolchain moved
to GitLab, so the gate is expressed in GitLab terms. Which CI platform is used belongs to
ADR-002.

Branching language is aligned to GitLab: merge request rather than pull request. The trunk-based
flow itself is unchanged.

Confirmed rather than changed: the `common/variables.yml` consequence and the per-bundle
permissions block both match the documented patterns almost verbatim. Sources below.

Downgraded: the production `root_path` off `/Shared` is no longer stated as documented fact. See
the note under Validation.

Editing rather than superseding is legitimate only because the status is Draft.

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
development mode with personal schemas. Trunk-based branching: a feature branch deploys to a
personal dev pipeline in the dev catalog, merge of a merge request to main validates and
deploys to staging, and a tag or manual approval deploys to prod. The prod target uses a
restricted `root_path` and runs as a service principal.**

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

Each `databricks.yml` defines dev, staging and prod targets, with the catalog overridden per
target. Dev sets development mode and personal schemas. The prod target sets a restricted
`root_path` and a service principal `run_as`. The production deployment is gated by a manual
approval in GitLab, and CI authenticates without a long-lived secret (see ADR-002).
`databricks bundle validate` passes for each target.

> ⚠️ Unverified. The specific choice of `/Shared` as the production `root_path` prefix is not
> established by the sources below. The documented example places it under
> `/Workspace/Users/<user>/.bundle/${bundle.name}/${bundle.target}`, and the workspace convention
> in `bootstrapping-project` describes `/Shared` as the place for cross-team artefacts with a
> separate read-only production folder for automation. Settle the prefix deliberately before the
> first production deploy; the requirement this record actually imposes is that the path is
> restricted and not a developer's home.

---

## Consequences

- Three workspaces to provision and govern.
- Per-target catalog values live in `common/variables.yml`, reached from each bundle with
  `include: - ../common/*.yml`. This matches the documented shared-folder pattern, where the
  example places `variables.yml` in a sibling folder alongside shared code. The documentation
  names that folder `shared`; this project calls it `common` (see ADR-003).
- Developers are isolated by personal schemas in the shared dev catalog.
- Promotion follows dev to staging to prod, gated by a manual approval before production.
- Each bundle carries a top-level permissions block (CAN_VIEW all, CAN_MANAGE the DE group,
  CAN_RUN the deployment service principal). The documented example for shared bundles uses
  exactly this shape, with `CAN_VIEW` to a group of all users, `CAN_MANAGE` to a data
  engineering group and `CAN_RUN` to a service principal.
- Test data never comes from production. Combined with the `bootstrapping-project` test-data
  rule, that means small representative datasets including error records, a personal schema per
  developer, and local samples or anything carrying personal data kept out of git.

---

## Sources

| Source | Bears on | Verified |
|:-------|:---------|:---------|
| [Sharing bundles and bundle files](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing), sections "Configuration for file sharing" and "Permissions for shared bundles" | `common/variables.yml` reached via `include`, and the three-level permissions block confirmed almost verbatim | 2026-08-06 |
| [CI/CD on Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/) | Authentication without long-lived secrets, via ADR-002 | 2026-08-06 |
| [Best practices for Lakeflow Spark Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices), section "Use bundle targets for environment isolation" | The dev, staging, prod promotion workflow | 2026-07-09 |
| [Best practices and recommended CI/CD workflows on Databricks](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/best-practices) | Separate dev, staging and production workspaces | 2026-07-09 |
| [Declarative Automation Bundles project templates](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/templates) | Development mode, personal schemas, default catalog | 2026-07-09 |
| `.claude/skills/bootstrapping-project/references/trees.md`, `code — data` | The test-data rule and the workspace folder convention | 2026-08-06 |

Version history is git. This record carries no version field.
