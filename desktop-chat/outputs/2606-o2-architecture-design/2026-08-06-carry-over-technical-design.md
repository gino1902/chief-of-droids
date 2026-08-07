# Carry-over: remaining ADRs, then technical design and project tree

> Handover in two stages. First finish the two scoped records, unnumbered pending reconciliation, using
> `making-architecture-decision`. Then run `writing-technical-design` against the set to
> produce the platform skeleton and living design document.
>
> ⚠️ The design run's preconditions are not met. Read the blocking section before invoking it.

| Field | Value |
|:------|:------|
| Written | 2026-08-06 |
| Revised | 2026-08-06, after ADR-011 landed and the record scope was split |
| From session | `o2-sources` |
| Target | A new repository for the O2 platform, on GitLab |
| Governing skills | `making-architecture-decision` for stage one, `writing-technical-design` for stage two. Both in `skills-lab` and neither deployed here |
| No version field | Git history is the version record for this folder |

---

## Stage one, finish the ADR sequence

An earlier scope bundled three decisions into one record. It was split, and ADR-011 is written.

| Record | State | What it decides |
|:-------|:------|:----------------|
| ADR-011 | Written, Draft | Ingestion baseline: contract on entities, producing system as configuration. Translation mappings where semantics are incompatible, lifespan secondary |
| Data ownership model | Not written, unnumbered | Who is accountable for a data definition and at what grain. Sections 1 and 2 are captured: the open question is whether a subdomain has one owning application or several, resolved to human ownership at subdomain grain; the forcing function is the transformation programme; options are federated flow-down (chosen), hybrid with a corporate polyseme tier, entity-grain, and centralised. Sections 3 to 8 remain |
| Unity Catalog isolation and domain boundary | Not written, unnumbered | Which axis each Unity Catalog level carries, environment or domain. Nothing captured beyond the analysis below |

The application role vocabulary, producer as system of origin and source as system extracted from
plus relay and consumer, is a convention rather than a decision. It fails the options test the same
way the slug rule did, and it folds into ADR-011's terminology. It also closes discovery-note F13.

**What the ownership record must carry, and it is the hard part.** One physical person appears as three
contractual roles owned by three different domains: Employee in `hr-administration`, Subcontractor
in `finance-suppliers`, Candidate in `hr-recruitment`, described by Talent Profile in `hr-talents`
and accounted for by User in `it-users`. The physical person is not modelled at all. Under the
chosen federated model that is five owners and no arbiter, which practitioner guidance says a
polyseme cannot have. It is an accepted limit rather than a solved problem, and it needs its
reopening condition written down.

**What the Unity Catalog record must carry.** Environment and domain can coexist because Unity Catalog separates the
processing environment (workspace) from the data domain (catalog), joined by workspace-catalog
binding. Proposed boundary: workspace is the environment, catalog is domain crossed with
environment, schema is layer and scope, and bronze sits in a platform catalog rather than a domain
one because a producer's feeds span domains. It amends ADR-006, whose catalog-per-environment
consequence it replaces while the `common/variables.yml` consequence survives.

---

## Stage two, what the design run does

Turn the ADRs plus the feed configuration into two outputs: the artefact skeleton
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

**2. The consistency sweep is complete.** Closed 2026-08-06, after this note was first written.
Five records were corrected, and the corrections changed two things that affect the tree:

| Record | Outcome |
|:-------|:--------|
| ADR-003 | Retained rather than deprecated. CI clause removed, vendor recommendation quoted, sharing mechanism stated, directory set grounded in active feeds |
| ADR-002 | Sole owner of the CI platform choice, now GitLab. Records that GitLab is not among the integrations Databricks documents, so the wiring is unpaved, and that authentication should use OAuth token federation rather than a stored token |
| ADR-007 | Delivery mechanism corrected to an editable install declared in `environment.dependencies`. **No wheel is built**, since jobs only orchestrate. Aggregate quality constraints route to a validation dataset plus a job dependency |
| ADR-006 | Approval gate in GitLab terms, `common/variables.yml` and the permissions block confirmed against the documented patterns, `/Shared` production path downgraded to unverified |
| ADR-INDEX | Sweep recorded, statuses and revision dates tabulated, the grounding rule for the tree stated |

Two consequences for the skeleton this note hands over. There is no wheel build to scaffold, so
`artifacts` stays out of the bundle configuration until a job gains a Python task. And any gating
quality check needs a second pipeline plus a job dependency rather than an expectation, which
changes the resource count per bundle.

Still true: every record remains Draft except ADR-008, so the skill's locked-ADR precondition is
still unmet. The sweep made them consistent, not locked. Locking is a deliberate non-goal for now,
because freezing decisions that rest on unread payloads and an unresolved identity question would
be worse than carrying them as Draft.

**3. Two records are still unwritten.** Per stage one above. The design run should
not start before them, since the Unity Catalog record decides the catalog and schema layout the
skeleton generates into and the ownership record decides who owns it.

**4. Neither skill is reachable from this repository.** Only `bootstrapping-project` is
deployed to `chief-of-droids/.claude/skills/`. Both `making-architecture-decision` and
`writing-technical-design` live in `skills-lab/.claude/skills/`, and both carry
`disable-model-invocation: true`, so neither fires on its own and each must be invoked explicitly.

**5. `2026-07-10-technical-design.md` in this folder predates the ADR-003 revision** and is
partly stale. Decide whether the next run updates it or supersedes it.

---

## Invocation

**Step zero, before writing either record: reconcile the numbering.** ADR-011 is the highest number
this session knows about, but records are being written in parallel sessions and 012 onward may
already be claimed. Check every in-flight session first, then assign. Numbers are deliberately not
reserved here, because a reservation made in one session is invisible to another and produces two
records with the same number.

Stage one, twice, once per record:

```
making-architecture-decision
```

It runs as an interview, one question at a time across eight sections, and it pushes back on weak
answers rather than transcribing them. The ownership record starts at section 3, since 1 and 2 are captured.

Stage two, once the two records exist:

```
writing-technical-design from desktop-chat/outputs/2606-o2-architecture-design/decisions
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

## Identifier convention, settled 2026-08-06

This is a convention, not a decision. It has no competing options: hyphens break Python imports
and force backtick-quoting in Unity Catalog, so underscores is the only workable form. It is
enforced by the generator, or by a validator that rejects a slug failing the identifier test.

Carry it verbatim into `CONVENTIONS.md` at the platform repo root when that repo is created. This
note is its interim home only because the repo does not exist yet.

**Slug rule.** One identifier per subject area, used unchanged as the directory name, the bundle
name, the Python module and the Unity Catalog schema. Lowercase, words separated by underscores,
valid as a Python identifier and legal in Unity Catalog without quoting. Display names may keep
characters the slug cannot, so `finance-fa&c` remains the display name.

Underscores rather than hyphens because the slug has three consumers and only underscores satisfy
all of them:

| Consumer | Hyphen | Underscore |
|:---------|:-------|:-----------|
| Directory and bundle name | Works | Works |
| Python module under `src/o2/silver/` | Invalid, cannot be imported | Works |
| Unity Catalog schema | Legal but needs backtick-quoting forever | Works |

The documented bundle example uses underscores for both folder and bundle name (`job_bundle`,
`pipeline_bundle`), so this also matches the vendor shape.

**The slug is produced by a transform and stored in a column.** Decided 2026-08-06. The transform
is the authority, so one generator computes every slug and no two consumers can disagree. The
column is its materialised result, so consumers read a value rather than re-implementing the rule.

The transform is a single substitution, which is the whole rule:

1. Trim and lowercase.
2. Replace every run of characters outside `a-z0-9` with one underscore.
3. Strip leading and trailing underscores.

In one expression: `re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")`.

Replacing rather than deleting is deliberate. A disallowed character is a token boundary, so it
should become a separator rather than vanish. `fa&c` is three tokens, and `finance_fa_c` keeps
that structure where `finance_fac` would collapse it into a word that does not exist.

Verified 2026-08-06 against all 17 subdomains: every result is a valid Python identifier and none
collides with a Python keyword. Edge cases behave: repeated separators collapse (`a&&b` gives
`a_b`), leading and trailing separators are stripped, and uppercase and spaces are handled.

| Display name | Slug |
|:-------------|:-----|
| hr-administration | `hr_administration` |
| hr-talents | `hr_talents` |
| project-master | `project_master` |
| project-resources | `project_resources` |
| finance-fa&c | `finance_fa_c` |

Because the rule is mechanical and total, there is no exception list and no hand-picked slug. The
twelve planned subdomains slug cleanly too, so nothing needs revisiting when a feed goes active.

**Where the column lives is still open, and it matters.** The taxonomy workbook is hand-edited,
so a typed slug column would be overwritten or left stale by the next human save. Three shapes:

| Shape | Drift risk | Visible in Excel |
|:------|:-----------|:-----------------|
| Column exists only in the generated YAML and markdown views | None, the workbook stays purely human-authored | No |
| Column in the workbook as an Excel formula | None, it recomputes itself | Yes |
| Column in the workbook as typed values rewritten by CI | Real, between edits | Yes |

Prefer the first, or the second if an editor needs to see the slug while working. Avoid the third.
Note that choosing the formula shape requires `xlsx_to_md.py` to read a formula cell's cached
value rather than its formula text.

**Renames are breaking.** Unity Catalog lineage is not preserved across renames of catalogs,
schemas, tables, views or columns, so changing a slug destroys lineage history rather than
refactoring it. Treat a slug as append-only once a schema exists under it.

**Open, and it belongs to AD-1 rather than here:** whether the slug is authoritative data held as
a column in the taxonomy, or derived by transforming the display name. See the discovery note.

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
| Whether the slug is data in the taxonomy or derived from the display name, AD-1 | Whether the generator reads a column or implements a transform every consumer must match. The slug values themselves are settled |
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
