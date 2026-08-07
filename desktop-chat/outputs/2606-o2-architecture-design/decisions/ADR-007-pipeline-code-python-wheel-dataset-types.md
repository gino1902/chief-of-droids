# ADR-007 — Pipeline code: Python declarative pipelines over a tested wheel, dataset types per layer (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | DE team |
| Informed | Wider data team |
| Revised | 2026-08-06, see Revision note |

---

## Revision note, 2026-08-06

The intent of this record is unchanged and correct: thin pipeline files over pure functions in
an importable, tested package. The delivery mechanism was wrong.

This record specified a built wheel installed through the `libraries` mapping. Verified against
the documentation, that is the pattern for job tasks. For pipelines the documentation states
that dependencies are cached during development and must instead be declared in the
`environment` section of the pipeline configuration, as an editable install of the deployed
project. Since ADR-005 puts all transformation logic in declarative pipelines and leaves jobs
as orchestration only, the pipeline mechanism governs.

That has a consequence nobody intended: **the wheel may have no consumer at all.** Jobs here
run `pipeline_task` orchestration, not `python_wheel_task`, so no job installs a library, and
the pipelines take the package as an editable install rather than as a built artifact. The
package remains essential. Building and shipping a wheel does not, until something needs one.

Editing rather than superseding is legitimate only because the status is Draft.

---

## Context

We need to decide the language and packaging for pipeline logic, how it is unit-tested,
where reusable logic lives, and which pipeline dataset type each medallion layer uses.
The conformed enterprise view lives in the silver layer (ADR-001); this record decides
how the shared transformation and metric functions behind it are packaged and tested.

---

## Options evaluated

**Option A — Thin Python pipelines over a tested package, dataset types fixed per layer**
Pipeline definitions are thin Python files using the declarative API, calling pure
functions in an importable package. The package is delivered to pipelines as an editable
install of the deployed project, not as a built wheel (corrected 2026-08-06, see the
Revision note and the delivery section below). SQL is allowed for simple pipelines. Dataset
types are fixed: bronze streaming tables, silver streaming tables plus materialized views for
enrichment or aggregation, gold materialized views.

**Option B — All logic inline in pipeline notebooks**
Fast to start, but hard to unit-test, encourages copy-paste, and gives conformed
entities nowhere reusable to live.

**Option C — Pure SQL pipelines throughout**
Clear and analyst-friendly for simple transforms, but weaker for reusable logic and
conformed-entity functions, and harder to unit-test.

**Options not pursued**
- Compiling the pipeline definitions themselves into the package: pipeline files are source
  files referenced by the pipeline resource. The package holds shared logic, not the pipeline
  entry point.

---

## Decision

**Option A chosen. Pipeline files are thin and import pure functions from an importable,
tested package, delivered to pipelines as an editable install of the deployed project.
Reusable conformed logic and metric definitions live in the package and in `common/entities`,
exercised by `tests/`. Table layout uses liquid clustering with `CLUSTER BY AUTO`. Data quality
expectations are enforced: warn at bronze, drop or quarantine at silver, fail for critical gold
constraints, with aggregate constraints handled as described below because expectations cannot
express them.**

### How pipeline code and dependencies are delivered

Corrected 2026-08-06 against the documentation. Three mechanisms exist and only the third fits
this architecture:

| Mechanism | Documented for | Applies here |
|:----------|:---------------|:-------------|
| `sync.paths` plus a `sys.path` append | Sharing raw source across bundles in one repository | Available, but unversioned and not a package install |
| `artifacts: type: whl` plus `libraries: whl:` | Job tasks | No. Jobs here only orchestrate pipelines |
| `uv` and `pyproject.toml`, with `environment.dependencies` | Pipelines | Yes, this governs |

The documentation states the constraint plainly inside its own `pyproject.toml` example: for
pipelines, dependencies are cached during development, so they belong in the `environment`
section of the pipeline configuration instead. The pipeline therefore declares its transformation
sources with a glob and takes the project as an editable install:

```yaml
resources:
  pipelines:
    <layer>_<scope>:
      catalog: ${var.catalog}
      schema: ${var.schema}
      serverless: true
      libraries:
        - glob:
            include: <path to the layer's transformation files>/**
      environment:
        dependencies:
          - --editable ${workspace.file_path}
```

> ⚠️ Unverified. The exact relative paths for `root_path`, the glob and `${workspace.file_path}`
> under the monorepo layout of ADR-003 have not been exercised. Confirm with
> `databricks bundle validate` on the first bundle before replicating the shape.

### Aggregate data quality, which expectations cannot express

Expectations are row-level SQL predicates evaluated per record, and they may not contain
subqueries against other tables. So "fail for critical gold constraints" holds only for
row-level constraints. Anything aggregate, row-count parity between layers, primary-key
uniqueness, or a coverage threshold, needs the validation-table pattern: a materialized view
computing the aggregate with `expect_or_fail` on its result.

One further limit shapes the topology. A validation table does not gate its downstream tables:
reading it from another dataset does not make that dataset wait. To stop downstream work on a
failed check, validation and downstream must be separate pipelines with the downstream task
depending on the validation task in a job. That is consistent with ADR-005's separation of
ingestion from transformation, and it means a gating check is a job-level dependency rather
than a clever expectation.

### Rationale

| Criterion | Option A | Option B | Option C |
|:----------|:---------|:---------|:---------|
| Unit-testable logic | Yes | No | Weak |
| Reuse of conformed entities | Yes | No | Weak |
| Supports the silver conforming layer (ADR-001) | Yes | No | Partly |
| Ease for simple transforms | Medium | High | High |
| Analyst accessibility | Medium | Medium | High |

Factoring pure functions into a tested package is what makes the silver conforming
layer from ADR-001 real rather than aspirational: the enterprise-view logic is written
once, tested, and imported by the silver pipelines that gold then builds on. SQL remains
available where a pipeline is simple enough not to need it.

Decision basis: the Lakeflow best-practices "Choose the right dataset type" and
"Organize pipelines with the medallion architecture" sections fix streaming tables and
materialized views per layer; the templates page provides the Python package option; the
"Use liquid clustering for data layout" and "Enforce data quality with expectations" sections
set those defaults. The delivery mechanism for that package is corrected above and is not the
wheel route the templates page describes for job tasks.

---

## Validation

Pipeline files are thin and import from the package. `tests/` cover the package and run in CI.
Each pipeline declares its dependencies in the `environment` section and its transformation
sources by glob, and `databricks bundle validate` passes for every bundle and target. Dataset
types match the per-layer rule in review, and expectations are present on each pipeline. Any
aggregate constraint appears as a validation dataset, and any gating check appears as a job task
dependency rather than as an expectation.

---

## Consequences

- `src/<package>/` is the tested, importable package; pipeline files import it; medallion
  subfolders become modules within the package. Module names must be valid Python identifiers,
  so subject-area names carrying hyphens or other characters need a slug rule. That rule does
  not exist yet and blocks generation of the silver layer.
- No wheel is built or installed while jobs only orchestrate pipelines. The `artifacts` mapping
  becomes necessary the moment a job gains a Python task, and not before. Do not carry wheel
  machinery that nothing consumes.
- Unit tests run in CI against the package, locally via `uv run pytest`, independent of the
  deployment mechanism.
- SQL is used only for pipelines simple enough to not need shared logic. Note that loading
  expectations from an external table or module is a Python-only capability, so a pipeline that
  needs shared rules cannot be pure SQL.
- Table layout is self-tuning via `CLUSTER BY AUTO`, with no manual partitioning.
- Gating on a failed quality check costs a second pipeline and a job dependency, not a
  configuration flag.

---

## Sources

| Source | Bears on | Verified |
|:-------|:---------|:---------|
| [Bundle library dependencies](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/library-dependencies) | The corrected delivery mechanism: `uv` and `pyproject.toml`, the pipeline dependency-caching limitation, `environment.dependencies` with an editable install, the glob for transformation sources, and the wheel-under-`libraries` pattern being for job tasks | 2026-08-06 |
| [Manage data quality with pipeline expectations](https://learn.microsoft.com/en-us/azure/databricks/ldp/expectations) | Expectations are row-level predicates with warn, drop and fail actions, and may not contain subqueries against other tables | 2026-08-04 |
| [Expectation recommendations and advanced patterns](https://learn.microsoft.com/en-us/azure/databricks/ldp/expectation-patterns) | The validation-table pattern for aggregate constraints; that a validation table does not gate its downstream tables; loading rules from a table or module is Python-only | 2026-08-04 |
| [Best practices for Lakeflow Spark Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/best-practices), sections "Choose the right dataset type", "Organize pipelines with the medallion architecture", "Use liquid clustering for data layout", "Enforce data quality with expectations" | Dataset types per layer, layer separation, `CLUSTER BY AUTO`, expectations | 2026-07-09 |
| [Declarative Automation Bundles project templates](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/templates) | The Python package option. Cited for the package, no longer for the wheel | 2026-07-09 |

Version history is git. This record carries no version field.
