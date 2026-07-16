# Design output specification

The deliverables are two aligned outputs: a tree of artefacts (the per-file how) and, where the existence gate warrants it, a living design doc (the system-level how). This file gives the artefact tree shape, the rule for every artefact, the README convention, and the living design doc template. The worked example is a Databricks Asset Bundle medallion platform, but the rules are general: they hold for any design that renders a set of ADRs.

## The tree

One illustrative artefact of each kind, in a shape a team can clone. The example below is the medallion data-platform shape. For a different domain, keep the intent (one-of-each, independently deployable units, shared common code, a CI file, a README) and change the layout to fit.

The deployable unit is the bundle, one per role: a producer, a subject area, a use case. Two decisions that shape the same role belong in one bundle, not two, unless they are genuinely separate deployable units. That judgment is a friction the gate surfaces rather than the scaffold silently splitting, see Part A of the interview.

Shared code is a buildable package. If the bundles import from `common/`, then `common/` carries its own `pyproject.toml` and `src/` layout so the wheel it exposes actually builds. Loose modules under `common/` that no bundle can import are a defect, not a shared library.

```
artefacts/
├─ azure-pipelines.yml            # CI/CD: validate on PR, deploy on merge, prod on approval
├─ .gitignore
├─ common/                        # shared code and variables, synced into units
│  ├─ variables.yml               # shared variable defaults
│  └─ utils/shared_transforms.py  # shared pure functions
├─ <unit-a>/                      # one independently deployable unit
│  ├─ databricks.yml              # bundle definition
│  ├─ pyproject.toml
│  ├─ resources/*.pipeline.yml    # declarative pipeline
│  ├─ resources/*.job.yml         # schedule and orchestration
│  ├─ src/<unit-a>/*.py           # thin code stubs
│  └─ tests/test_*.py
└─ README.md                      # what is here, names to replace, open decisions, before use
```

## The rule for every artefact

Each artefact, whatever its type, obeys the same five rules.

Cite the ADR inline. Put the governing ADR on the line it justifies, or in the module docstring for a code file. A YAML line reads `serverless: true          # (ADR-004)`. A Python module opens `"""Bronze ingestion for one producer (ADR-008)."""`. This is the traceability, and it is non-optional: an element with no ADR either rests on a missing decision or does not belong here.

Render in the decision's own vocabulary. Use the exact terms the ADRs and framing use, and never substitute a more familiar or more general equivalent, because predictable artefacts come from borrowed vocabulary, not invented synonyms. For a technical artefact that is the exact API name, module path, config key, and field shape the decision cites, not a better-known alias. For a functional artefact that is the exact domain entity, role, and process-step name the decision uses, not a paraphrase.

Where the decision does not write a literal identifier, tell two cases apart. If it names a product, paradigm, or standard, derive the concrete identifier from that named thing and cite it, and never fall back to a more familiar or more widely used alias even when the alias is the better-known name. A derived, load-bearing identifier that the decision does not write literally is rendered concretely and marked as a confirm-this open decision, because the derivation is version-sensitive and easy to get subtly wrong. A derivation that is trivial or unambiguous renders silently with the product cited, so the flag stays for what genuinely needs a human eye. If nothing is named at all, no product and no standard, then it is a Decide element, not a licence to coin a term. Worked example: ADR-005 names "Lakeflow Spark Declarative Pipelines", so the pipeline file imports `from pyspark import pipelines`, not the legacy `dlt`, and flags the import surface as confirm-this.

Render Execute, resolve or placeholder Decide. For an Execute element, write the value the ADR locked. For a Decide element, write the value resolved in the interview, or, if it could not be closed, write a safe placeholder and log the open decision in the README. Never write a Decide value as if it were locked.

Tell two kinds of not-yet-real apart. A name that gets cloned once, like a producer, subject area, entity, or role, is a static placeholder: write a clear token (`source_system`, `subject_area`) and list it under names to replace. Use bare tokens in file and directory names (`source_system`), never angle-bracket forms (`<producer>`), because brackets break shells and make the tree awkward to clone. A value that varies by environment or instance and whose parameterisation a decision locks is not a placeholder at all, it is an Execute element: render the parameterisation mechanism the decision specifies (a variable, a per-target override, a config key), not a hardcoded value with a REPLACE marker. Hardcoding a value the decision said to parameterise under-renders the decision.

Keep code stubs thin. A code artefact shows the shape and the seam, not the full logic. A bronze stub declares the table and delegates to a thin, testable reader. It does not implement the whole transform. The design is the structure, the seams, and the citations, not a finished implementation. Import the seam from the shared package rather than defining it locally as a stub, so the thin-pipeline-over-wheel structure is visible in the file. A seam defined locally hides the boundary the wheel is meant to own.

## Rendering forms by artefact type

The design takes whatever form renders the decision most precisely. Reach for the form, not prose.

- Project tree, as the folder layout itself and a tree block in the README.
- Config, as an annotated YAML skeleton (`variables.yml`, `databricks.yml`).
- Pipeline and bundle definition, as a `*.pipeline.yml` sketch of its real shape.
- Schedule and orchestration, as a `*.job.yml` with the trigger and dependency wiring, or a cron skeleton.
- CI/CD, as an `azure-pipelines.yml` sketch of the stages and gates.
- Code, as a thin `*.py` stub with the seam and the docstring citation.
- Tests, as a thin `test_*.py` stub that pins the seam, one per code artefact.
- Data model, as a schema stub or a table of entities, keys, and types. A conformed or dimensional model with no real entities yet is a placeholder plus an open decision.
- Contract, as a schema table or JSON schema (fields, keys, casing, promotion rules, provenance).
- Diagram, as a small C4 or flow sketch where structure or topology is the point.
- Tables, for per-item detail (per-target overrides, clustering keys, grants, risks).

## The README

The README is the only prose artefact, and it carries the reader from the tree to a usable scaffold. Follow this shape.

```markdown
# Platform skeleton

Illustrative, one-of-each scaffold for the <platform> defined in ADR-001 to NNN.
A starting shape to clone, not the populated repo.

## What is here
<the tree block, each line annotated with its purpose and governing ADR>

## Names to replace
<the placeholders: unit names, hosts, urls, groups, principal ids>

## Open decisions still to make
<the Decide elements not closed in the interview, each a one-liner with what is needed>

## Before use
> ⚠️ Unverified. The field shapes are grounded in the docs read during design, not run.
> <the validate command, e.g. `databricks bundle validate -t dev`>
<the toolchain and runtime prerequisites>

---
| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | YYYY-MM-DD |
| Status       | Draft      |
```

## The living design doc

Produced where the existence gate warrants it (Part C of the interview): ambiguity in the shared band (unit boundaries, seam contracts, data model) or in a cross-cutting concern. Otherwise a minimal stub. Short, one to three pages for an incremental design. It carries the system-level how and references the ADRs for the why. It never restates ADR rationale, per-file config (that is the artefacts), or operational steps (that is the README).

Sections follow the design-doc practice, adapted so the why stays in the ADRs. Interview only the sections the ADRs leave thin, and drop a section with nothing system-level to say.

~~~markdown
---
title: <system> technical design
status: Draft
reviewers: <named reviewer or role>
last_updated: YYYY-MM-DD
---

# <system> technical design

> Living companion to ADR-001 to NNN. The ADRs are the frozen why; this is the
> system-level how. Per-file detail lives in artefacts/, operational steps in its README.

## Context and scope
<the landscape this sits in and where its edges are>

## Goals and non-goals
- Goal: <...>
- Non-goal: <...>

## Design
<overview, then how the units fit and hand data across; cite the ADRs, do not re-argue them>

### System context
<a small C4 or flow diagram where topology is the point>

### Data flow across units
<how data moves end to end, at the system level>

### Contracts between units
<schema, keys, casing, promotion rules, provenance at each seam; a table>

## Cross-cutting concerns
<security, privacy, observability across units, not file by file>

## Open items
<system-level questions not yet closed, each one line with what is needed to close it>

## Sources
<only docs actually used; the ADRs carry their own sources and are not repeated>

---
| Field        | Value       |
|--------------|-------------|
| Version      | 0.1 (draft) |
| Last Updated | YYYY-MM-DD  |
| Status       | Draft       |
~~~

A shared decision (a seam contract, the data model, a unit boundary) is written here and in the artefact that renders it, from the one answer resolved in the interview. The two are never asked or answered separately.

## Scope of the scaffold

Match it to the decisions. A handful of ADRs on one layer scaffolds that layer. A full platform spanning every ADR scaffolds one of each unit. Either way it is one-of-each and illustrative. Populating it per real producer, subject area, or use case, and running it, is the team's next step, not this skill's.
