# ADR-003 — Repository strategy: single monorepo with independently deployable bundles (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | DE team |
| Informed | Platform / DevOps engineering |
| Revised | 2026-08-06, see Revision note |

---

## Revision note, 2026-08-06

This record was treated as deprecated on 2026-08-06 when the toolchain moved to GitLab. That
was wrong in scope. The deprecation was aimed at one clause naming Azure DevOps pipeline
files, and it discarded a decision the vendor explicitly recommends. The record is therefore
retained, with three corrections:

- The CI clause is removed. Which CI platform is used belongs to ADR-002.
- The decision basis is upgraded from inference to a verbatim vendor recommendation.
- The mechanism by which shared code reaches a bundle is stated, because this record and
  ADR-007 previously described different mechanisms while reading as compatible.

Editing rather than superseding is legitimate here only because the status is Draft. Once a
record is Accepted it becomes immutable and a change requires a successor.

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
cost with no offsetting benefit. Rejected more firmly on 2026-08-06 once the sharing
mechanism was checked: splitting into repositories does not remove the local-file step
for shared code, it adds a publish step, an index token and a vendoring step in front of
it. There is no documented way for a bundle to consume a private wheel directly from a
registry at deploy time; the documented path downloads it first with
`pip download -d dist ... --index-url` and then references the local file or a Unity
Catalog volume.

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

Decision basis: this is the vendor's stated recommendation, not an inference. The
"Sharing bundles and bundle files" page, section "Repository structure", states verbatim:

> A common practice and Databricks' recommendation is to store source for many bundles in
> one repository with a shared folder.

Its worked example places `variables.yml` and shared code in a sibling folder, pulled into
each bundle with `sync.paths` and `include: - ../shared/*.yml`. The "Developer best
practices" page separately recommends small, focused bundles owned per team.

Naming note: the documentation example calls the sibling folder `shared`. This record and
ADR-006 and ADR-007 call it `common`. The name carries no behaviour; `common` is kept for
continuity across the three records.

### How shared code actually reaches a bundle

Recorded 2026-08-06 because this record and ADR-007 previously described different
mechanisms while reading as compatible. Three distinct mechanisms exist:

| Mechanism | Shares | Versioning | Fit |
|:----------|:-------|:-----------|:----|
| `sync.paths` plus a `sys.path` append | Raw source files | None | Requires DBR 14+ or serverless |
| `artifacts: type: whl` plus `libraries: whl:` | A built wheel | By build | Documented for job tasks |
| `uv` and `pyproject.toml` plus `environment.dependencies` | The project as an editable install | By repository state | The documented path for pipelines |

Because ADR-005 puts all transformation logic in declarative pipelines, the third
mechanism governs, not the second. The documentation states the limitation directly: for
pipelines, dependencies are cached during development, so they belong in the `environment`
section of the pipeline configuration rather than being installed as a built wheel. See
ADR-007, which needs correcting on this point.

---

## Validation

Each bundle deploys on its own with `databricks bundle deploy`, and a change to one
bundle does not redeploy others. `sync.paths` references to `common/` resolve, and
`databricks bundle validate` passes for every bundle in CI.

---

## Consequences

- Top-level layout carries the three layers: `common/`, `ingestion/<producer>/`,
  `silver/<subject_area>/`, `use_cases/<use_case>/`, plus `docs/`. Producer bundles own
  bronze only, silver bundles own the conformed enterprise view, use-case bundles own gold
  (see ADR-001). CI configuration lives wherever the chosen platform requires it, and which
  platform that is belongs to ADR-002, not here. This record is deliberately CI-agnostic:
  an earlier version named Azure DevOps pipeline files, which caused the whole record to be
  treated as deprecated on 2026-08-06 when the toolchain moved to GitLab. Only the CI clause
  was stale.
- Which directories exist at any time is grounded in the feed configuration, not in the
  taxonomy. A bronze bundle exists per producer having at least one active feed, a silver
  bundle per subject area having at least one active feed, and a gold bundle per use case
  with a go decision. On the 2026-08-06 configuration that is two bronze (APP, Whoz), five
  silver and zero gold, against a taxonomy of 17 subdomains. Directories for planned feeds
  are created when the feed goes active, not in advance.
- The two-level grouping means shared references resolve as `../../common`, an accepted
  trade for clearer top-level intent.
- Bundles are independently deployable despite sharing a repository.
- Resource files follow the `<name>.pipeline.yml` and `<name>.job.yml` naming
  convention.

---

## Sources

Fetched and verified on the dates shown. Each page carried a last-updated date within
twelve months at the time of verification.

| Source | Bears on | Verified |
|:-------|:---------|:---------|
| [Sharing bundles and bundle files](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing), sections "Repository structure" and "Configuration for file sharing" | The one-repository recommendation, the `shared` folder example, `sync.paths` and the `sys.path` append pattern | 2026-08-06 |
| [Bundle library dependencies](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/library-dependencies) | The three sharing mechanisms, the `uv` and `pyproject.toml` editable-environment pattern, and the pipeline dependency-caching limitation | 2026-08-06 |
| [Use a private artifact in a bundle](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/artifact-private) | Why Option B costs more: a private wheel must be downloaded locally before a bundle can reference it | 2026-08-06 |
| [Developer best practices on Databricks](https://docs.databricks.com/aws/en/developers/best-practices) | Small, focused bundles owned per team | 2026-07-09 |
| [O2 data sources](../2607-o2-requirements/o2-data-sources.md) and [domain taxonomy](../2607-o2-requirements/domain-taxonomy.md) | The feed configuration that grounds which directories exist | 2026-08-06 |

Version history is git. This record carries no version field.
