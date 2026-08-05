# Carry-over: technical design and project tree

> Handover for the session that runs `writing-technical-design` against this ADR set to
> produce the O2 platform artefact skeleton and living design document.
>
> ⚠️ Preconditions are not met yet. Read the blocking section before invoking anything.

| Field | Value |
|:------|:------|
| Written | 2026-08-06 |
| From session | `o2-sources` |
| Target | A new repository for the O2 platform, on GitLab |
| Governing skill | `writing-technical-design`, currently in `skills-lab` and not deployed here |
| No version field | Git history is the version record for this folder |

---

## What the next session does

Turn the locked ADRs plus the feed configuration into two outputs: the artefact skeleton
that renders the decisions (tree, bundle configuration, pipeline and job resource files,
code stubs, CI file, README) and a living design document carrying the system-level how.

The skill writes an illustrative skeleton, not a runnable platform. That distinction is in
its own description and should be honoured, so nobody expects working pipelines out of it.

---

## Blocking preconditions

**1. The skill requires locked ADRs. Ours are Draft.**

Nine of the ten records are Draft. Only ADR-008 is Accepted. ADR-009 is Draft and blocked on
an unverified composition. ADR-010 carries an amendment marked proposed and not agreed by its
five decision-makers.

**2. Four records still disagree with each other.** State as of 2026-08-06:

| Record | Status | What is wrong |
|:-------|:-------|:--------------|
| ADR-003 | Draft, revised 2026-08-06 | Corrected. CI clause removed, vendor recommendation quoted, sharing mechanism stated, directory set grounded in active feeds |
| ADR-002 | Draft | Says workloads are "deployed through the Databricks CLI in Azure DevOps". This is now the only home of the stale CI clause and needs GitLab |
| ADR-007 | Draft | Specifies a built wheel under `libraries`. That is the job pattern. Pipelines use an editable environment install, and ADR-005 puts all logic in pipelines |
| ADR-006 | Draft | Validation says "The Azure DevOps prod stage has a manual approval gate". Its `common/variables.yml` consequence is confirmed correct by the documentation |
| ADR-INDEX | Draft | Asserts ADR-002 and ADR-003 set the shape every record assumes, does not record the ADR-003 revision, and parks the `<name>.pipeline.yml` and `<name>.job.yml` naming convention inside ADR-003 instead of giving it a record |

**3. The skill is not reachable from this repository.** Only `bootstrapping-project` is
deployed to `chief-of-droids/.claude/skills/`. `writing-technical-design` lives in
`skills-lab/.claude/skills/`. It also carries `disable-model-invocation: true`, so it never
fires on its own and must be invoked explicitly.

**4. `2026-07-10-technical-design.md` in this folder predates the ADR-003 revision** and is
partly stale. Decide whether the next run updates it or supersedes it.

---

## Invocation, once unblocked

```
writing-technical-design from desktop-chat/outputs/2606-o2-architecture-design
```

---

## Inputs the skill needs beyond the ADRs

| Input | Path | Role |
|:------|:-----|:-----|
| Feed configuration | [o2-data-sources.md](../2607-o2-requirements/o2-data-sources.md) | Which bundles exist. Generated view of `o2-data-sources.xlsx`, which is the source of truth and is not git-tracked |
| Domain taxonomy | [domain-taxonomy.md](../2607-o2-requirements/domain-taxonomy.md) | Subject areas for the silver layer, 5 domains and 17 subdomains |
| Discovery note | [2026-08-04-data-sources-discovery-note.md](../2607-o2-requirements/2026-08-04-data-sources-discovery-note.md) | 15 findings and 4 proposed decisions, none approved |
| Tree conventions | `.claude/skills/bootstrapping-project/references/trees.md`, the `code — data` section | The base layout and the conventions block that becomes `CONVENTIONS.md` |

---

## The generation rule

The tree is a projection of the configuration, not a hand-maintained structure. This is the
main design output of the originating session.

```
bronze bundle  ← one per producer having at least one active feed
silver bundle  ← one per subdomain having at least one active feed
gold bundle    ← one per use-case brief with a go decision
a feed row     ← the routing edge from its producer's bronze to its subdomain's silver
```

Adding an active feed for a new producer creates a bundle. Flipping the last active feed of a
subdomain makes its bundle removable. The taxonomy alone never justifies a directory.

---

## What the configuration justifies today

Applying the rule to the 19 active feeds of 33:

| Layer | Axis | Full taxonomy | Justified now |
|:------|:-----|--------------:|--------------:|
| Bronze | per producer | 9 producer values | **2**: APP with 13 feeds, Whoz with 6 |
| Silver | per subject area | 17 subdomains | **5**: hr-administration 7, hr-talents 6, finance-fa&c 2, project-master 2, project-resources 2 |
| Gold | per use case | not applicable | **0**, no brief has a go decision |

Seven bundles, not twenty-six. Domains touched are hr, project and finance. Sales and it have
no active feed. Twelve subdomains and six producer values exist only on `planned` rows.

The `bootstrapping-project` rule that every directory must be justified now rather than
speculatively applies directly: do not scaffold the twelve planned subdomains.

---

## Proposed tree

```
o2-platform/                       new GitLab repo, not inside chief-of-droids
├── CONVENTIONS.md                 verbatim from the skill's data block + enforcement stanza
├── pyproject.toml                 uv, ruff config, wheel build
├── scripts/check-conventions-drift.sh
├── common/
│   ├── variables.yml              per-target catalogs                      ADR-006
│   └── entities/                  conformed entity logic                   ADR-007
├── src/o2/                        the tested package
│   ├── bronze/  silver/  common/  medallion subfolders as modules          ADR-007
├── tests/                         unit tests against the package
├── ingestion/                     bronze, one bundle per producer          ADR-001
│   ├── app/  whoz/
├── silver/                        one bundle per active subdomain
│   ├── hr_administration/  hr_talents/  project_master/
│   ├── project_resources/  finance_fa_c/
└── use_cases/                     .gitkeep only, no gold yet
```

Each bundle carries the same three things, from ADR-005 and ADR-007: `databricks.yml` with
three targets, `resources/<name>.pipeline.yml` plus `<name>.job.yml`, and thin `pipelines/*.py`
importing the package. Bronze ingest and transformation stay separate pipelines so a transform
failure cannot block landing.

Deferred with the trigger that creates each: the twelve subdomains and six producers at their
first active feed, `use_cases/<case>/` at the first go decision, `scratch/` at the first
exploration.

---

## Naming rule needed before generation

Not decided anywhere, and generation fails without it:

- Subdomain names use hyphens (`hr-administration`), which are invalid as Python module names,
  while ADR-007 requires medallion subfolders to be package modules. So a slug is required.
- `finance-fa&c` contains an ampersand, which is invalid in a module name and a bundle name.
  `finance_fa_c` above is a guess, not a decision.

---

## Verified mechanism facts, do not re-derive

Fetched and verified 2026-08-06. Full detail and quotes sit in ADR-003's revision note and in
the discovery note's verified-mechanics section.

| Fact | Consequence |
|:-----|:------------|
| One repository with a shared folder is Databricks' explicit recommendation, quoted verbatim in ADR-003 | The monorepo shape is vendor-backed, not preference |
| `sync.paths` shares raw source and the consumer appends to `sys.path`. Requires DBR 14+ or serverless | Not a wheel, and not versioned |
| A built wheel under `libraries` is documented for job tasks | Not the pipeline path |
| For pipelines, dependencies are cached during development, so they belong in the `environment` section, via `uv` and `pyproject.toml` with an editable install | This governs, because ADR-005 puts all logic in pipelines. ADR-007 needs correcting |
| A private wheel cannot be consumed straight from a registry. It must be downloaded locally first, then referenced as a file or from a Unity Catalog volume | Repo-per-bundle costs more machinery, not less |
| Expectations are row-level only, with no cross-table subqueries. A validation table does not gate its downstream tables | Aggregate checks need a separate validation pipeline with a job task dependency |
| Unity Catalog lineage is emitted at read and write time | It detects, it cannot prevent |

---

## Conventions that carry from `bootstrapping-project`

`CONVENTIONS.md` is written at the repo root, filled verbatim from the `code — data`
conventions block, dropping the author-facing unverified caveats. Its enforcement stanza for a
data goal:

```
<!-- enforcement:
config: pyproject.toml
runner: uv run ruff check .
zoned: none
-->
```

Rules that survive unchanged: notebooks import the package and never the reverse; transform
logic never lives in a notebook; code is born in `scratch/` and moves into the package with a
test at first production use; approved directories are created via `.gitkeep`; test against
small representative datasets including error records, never production data, with a personal
schema per developer and the production catalog bound to the production workspace only.

Two bootstrap answers are superseded now that the architecture stage has arrived. The skill
answers the ETL-pipeline prompt no and says why, that orchestration style is an architecture
decision. ADR-005 has made it, so pipelines are yes. The skill also defers the medallion
layering to this stage explicitly, so layering the tree executes that deferral rather than
overriding it.

---

## Open decisions that would change the tree

| Question | Effect if answered differently |
|:---------|:-------------------------------|
| The slug rule above | Every silver bundle and module name |
| What `inactive` means, discovery note F12. Both inactive feeds land daily | Whether two feeds belong in the tree at all, and whether the middleware is shipping unwanted data |
| Written definitions for `producer` and `source`, F13. `Sharepoint` appears as both | A planned feed would generate a bronze bundle named after a landing zone |
| Whether the source of truth moves from the workbooks to YAML, AD-4 | Whether the tree is generated by a script or by hand |
| Whether O2 owns identity mapping, AD-2 | Whether a mapping table and its stewardship enter the silver layer |

Resolved since the discovery note was written: ADP is not a producer. Its three feeds belong to
APP, which is why bronze is two bundles rather than three. The discovery note's F4 stands and
the workbook needs the same correction.

---

## Not in scope for the next session

Reading the 20 unread payloads in `2608-o2-data-sources`. Building the YAML generator and
validator for the workbook pair, which waits on AD-4. Writing the four ADRs proposed in the
discovery note. Anything that produces a runnable platform rather than a skeleton.

---

## Sources

| Source | Bears on |
|:-------|:---------|
| [Sharing bundles and bundle files](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing) | One-repository recommendation, `sync.paths` |
| [Bundle library dependencies](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/library-dependencies) | The three sharing mechanisms, pipeline dependency limitation |
| [Use a private artifact in a bundle](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/artifact-private) | Why a registry costs more |
| [Bundle configuration in Python](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/python) | Generating resources from metadata |
| ADR-001, ADR-002, ADR-003, ADR-005, ADR-006, ADR-007 in this folder | The decisions the skeleton must render |
| `.claude/skills/bootstrapping-project/references/trees.md` | Base layout and conventions |
| `skills-lab/.claude/skills/writing-technical-design/SKILL.md` | The skill's own contract and preconditions |

All Microsoft Learn pages fetched and verified 2026-08-06, each carrying a last-updated date
within twelve months.
