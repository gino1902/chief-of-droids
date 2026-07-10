# Platform skeleton

Illustrative, one-of-each scaffold for the Azure Databricks platform defined in ADR-001 to 009. It is a starting shape to clone, not the populated repo.

## What is here

```
artefacts/
├─ azure-pipelines.yml            # CI/CD: validate on PR, deploy staging on main, deploy prod on approval
├─ .gitignore
├─ common/                        # shared code and variables, synced into bundles via sync.paths
│  ├─ variables.yml               # shared variable defaults (group names, service principal)
│  └─ utils/shared_transforms.py  # shared pure functions (imported by pipelines)
├─ ingestion/source_system/       # one BRONZE bundle, per data producer (ADR-001, ADR-008)
├─ silver/subject_area/           # one SILVER bundle, per subject area, cross-source conforming (ADR-001)
└─ use_cases/use_case/            # one GOLD bundle, per business use case (ADR-001)
```

Each bundle is independently deployable and shares `common/` through `sync.paths`.

## Names to replace

`source_system`, `subject_area`, `use_case`, the workspace hosts, storage URLs, group names and service-principal ids are placeholders. Replace them, and clone one bundle per real producer, subject area and use case.

## Open decisions still to make

Marked in the topic map (`../2026-07-09-technical-design-topic-map.md`). Chiefly: concrete catalog and schema naming, the silver conformed-entity model, gold dimensional models, and inter-layer orchestration wiring. The skeleton uses a simple schedule for silver and gold; the real dependency wiring is a Decide item.

## Before use

> ⚠️ Unverified. Field shapes are grounded in the Databricks docs, not run against a workspace. A static conformance pass was done; three items could not be settled without the CLI and must be confirmed by `databricks bundle validate -t dev` and a dev deploy:
> 1. Loading a `.py` declarative-pipeline module. The pipeline `libraries: notebook` form may need to be a `glob`/`file` include, or the source package added as a pipeline library, so `reader` and the shared `utils` are importable at runtime.
> 2. The `dp.apply_changes(...)` signature (keys, sequence_by, stored_as_scd_type) under the `pyspark.pipelines` namespace.
> 3. How the shared `common/utils` package resolves on the pipeline path (sync.paths lands it, but the import root must be confirmed).

Requires the Databricks CLI, `uv`, and Databricks Runtime 18.1+ for the automatic managed-file-events default (ADR-008).

---

| Field | Value |
|:------|:------|
| Version | 1.0 |
| Last Updated | 2026-07-09 |
| Status | Draft |
