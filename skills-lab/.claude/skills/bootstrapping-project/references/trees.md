<!-- pass 3 reference for bootstrapping-project -->

# Pass 3 — project tree

Turns the intent in FRAMING.md into a source layout. Three rules govern this pass.

First, only scaffold on an empty repo. If source files already exist, do not propose a
reorganisation — document the existing structure so pass 4 can describe it accurately, and
skip creation. Reorganising someone's repo is rarely wanted and never safe by default.

Second, every directory must be justified now, not speculatively. Create only what the
project needs today. The deferred directories listed under each tree are created later,
when the trigger for them actually occurs — this keeps the tree honest and readable.

Third, write the conventions down. Each goal below carries a Conventions block: dependency,
import, and promotion rules, plus an Enforcement line naming the real mechanism. That block is
not just reference for the model — it is the source text for a `CONVENTIONS.md` written at the
repo root in this pass, the durable contract for the tree. Fill `CONVENTIONS.md` verbatim from
the locked goal's block, do not reword or re-synthesise. If it already exists, reconcile with a
minimal approval-gated diff, never regenerate. The lint config and project gate that enforce the
contract are generated at the pass 4 tail, once the stack is confirmed; `CONVENTIONS.md` names
the config file and runner so the two cannot silently drift.

`CONVENTIONS.md` ends with a machine-readable enforcement stanza, an HTML comment the lifecycle
drift-check (`check-conventions-drift.sh`) parses. Write it exactly in this shape, one stanza per
file:

```
<!-- enforcement:
config: <relative-path to the lint config, or none>
runner: <the lint command, or review>
zoned: <space-separated prefix/* globs whose child folders must each be zoned, or none>
-->
```

Per goal: app sets `config` to the ESLint config, `runner` to the lint command, and `zoned` to
`apps/* src/features/*`. Data sets the ruff config, its runner, and `zoned: none` (ruff is
file-level, not zone-level). Infra sets the TFLint config, its runner, and `zoned: none`. Thinking
sets `config: none`, `runner: review`, `zoned: none` — review is its only gate. At bootstrap
`config` and `runner` may be pending until the pass 4 tail confirms the stack; write the stanza
with the values the tail will produce, and the tail reconciles them into place when it generates
the config.

Create approved directories via `.gitkeep` files so they are tracked by git.

Resolve `<placeholders>` from the project name, or ask.

## thinking

```
decisions/    BDRs, ADRs (<type>-NNNN-title.md), superseded, never edited
notes/        living working and meeting notes
diagrams/     Mermaid / C4 sources
references/   documents that ground the decisions
```

Rationale — strengths:

- Small, one-decision records are the only documentation format that stays
  maintained — the origin text's argument: large documents are never kept up
  to date, bite-sized ones have a chance.
- The superseded chain preserves rationale: a reader can trust that an
  accepted record states what was true when written, and the current position
  is the chain's end, not an edited file.
- The record pattern extends beyond architecture — "any decision record" —
  which is what admits BDRs (Business Decision Records) alongside ADRs.

Rationale — watch-outs:

- Editing an accepted record destroys the log's trustworthiness — the whole
  value rests on immutability.
- `notes/` is the entropy sink: living notes that never promote into decisions
  or get pruned bury the records that matter.
- Decision theater — records written but never reviewed or referenced. One to
  two pages, reviewed like code, or not written at all.

Conventions — initiated with the tree, they are the structure's other half:

- Record rule: one decision per record, immutable once accepted. A reversal is
  a new record; the old one gets status superseded with a reference to its
  replacement. Lifecycle: proposed → accepted → deprecated or superseded.
- Naming rule: `<type>-NNNN-title.md`, type is `adr` or `bdr`; NNNN is
  sequential and monotonic per type, numbers never reused.
- Type rule: ADR records an architecturally significant decision; BDR records
  a business decision (house extension of the any-decision-record principle;
  substance authored via `analyzing-business-cases`).
- Promotion rule: thinking is born in `notes/`; it becomes a record in
  `decisions/` the moment a decision is taken. `references/` holds the
  documents the record's context cites — facts, not opinions.
- Diagram rule: `diagrams/` holds sources, not exports — Mermaid on the C4
  abstractions, so diagrams diff and review like code.
- Enforcement: there is no lint equivalent here — review is the gate. Records
  go through the same review as code; a pre-commit or CI check can at most
  verify naming and that accepted records are untouched.

Sources:

1. [Nygard — Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html)
2. [adr.github.io — Architectural Decision Records](https://adr.github.io/)
3. [C4 model](https://c4model.com/)

Ask the code sub-type question first: data or app.

## code — data

Declarative Automation Bundles (formerly Databricks Asset Bundles), `default-python`
template (`databricks bundle init default-python`; requires uv; companion reference
`databricks/notebook-best-practices`).

The init is interactive — it composes the tree from four prompts: notebook job (yes),
ETL pipeline (no), Python package stub (yes), serverless (project's call). Answering
this way yields the bootstrap tree; the pipeline prompt is answered no because that
choice is architecture-stage, not bootstrap-stage (see below).

```
databricks.yml            bundle definition, targets (dev/prod)
pyproject.toml            deps and build, managed via uv (required by the template)
src/<pkg>/
  main.py                 importable, testable package code
  notebook.ipynb          thin orchestration entry, imports the package
resources/
  <pkg>.job.yml           job / workflow definitions
tests/
  main_test.py            unit tests against the package — uv run pytest, via databricks-connect
```

`default-minimal` (empty bundle, required files only) is the leaner alternative when
even the sample job is unwanted; the package-and-tests skeleton above is why
`default-python` stays the default here.

Rationale — strengths:

- The importable `src/` package makes logic unit-testable locally (uv run pytest +
  databricks-connect) without deploying — the single biggest quality lever on
  Databricks projects.
- `resources/` and `databricks.yml` isolate deployment and orchestration from code —
  targets (dev/prod) are configuration, not branches.
- The bundle is the clonable unit: one bundle, one deployable, one blast radius.

Rationale — watch-outs:

- Notebook logic creep is the failure mode: code accumulates in `notebook.ipynb`
  instead of the package, and testability silently dies.
- `resources/` sprawl — many near-duplicate job YAMLs signal a missing pipeline or
  a topology decision being avoided.
- databricks-connect pins compatibility to the remote runtime — keep its version at
  or below the cluster runtime.

Conventions — initiated with the tree, they are the structure's other half:

- Dependency rule: notebooks import the package; the package never imports
  notebooks. Tests import the package only, never the notebook.
- Thin-notebook rule: `notebook.ipynb` orchestrates (parameters, calls, display);
  any transform logic belongs in `src/<pkg>/`.
- Promotion rule: code is born in `scratch/` exploration; it moves into
  `src/<pkg>/` with a test at first production use.
- Enforcement — three testing layers, matching how the bundle moves toward
  production: unit tests on `src/` via `uv run pytest` on every pull request
  (failures block merges); `bundle validate` locally and `bundle deploy` to a
  non-production workspace in CI; E2E jobs in staging after deploy. Lint with ruff.
  > ⚠️ Unverified — ruff is used in Databricks' own bundle-examples CI, but that
  > claim comes from a secondary source; confirm in the repo before citing.
- E2E assertion rule (deferred — activates at the first staging target): every
  E2E run pairs a completion check with data-quality assertions on the output
  tables — row counts and schema expectations at minimum. DataFrame-level
  assertions in integration tests use chispa. "All tests pass on main and in
  staging" is the gate for promoting to production.
- Test-data rule: test against small, representative datasets that include
  error records — never production data. Isolation makes this safe: a personal
  schema per developer (`dev_${user_name}`), separate dev/staging/prod catalogs,
  and the production catalog bound `ISOLATED` to the production workspace only.
  Local data samples and anything with PII stay out of git (`.gitignore`).

Tests: a dedicated top-level `tests/` parallel to `src/`, testing the importable package
directly via `databricks-connect`, not the notebook itself.

Deferred: `scratch/exploration.ipynb` for throwaway notebooks, added at the first ad-hoc
exploration (excluded from deployment). A second `resources/*.yml` at the second job.
`docs/adr/` at the first decision.

Topology is provisional. This is a single bundle, the clonable unit. Layering it into a
medallion monorepo (bronze / silver / gold as top-level directories, one bundle per producer,
subject area, and use case, sharing a `common/` via `sync.paths`) is an architecture-stage
decision, not a bootstrap-time one. Defer it to `making-architecture-decision` and
`writing-technical-design`; do not pre-scaffold layers here. The anchor stays one bundle so
the architecture stage can restructure without unwinding speculative directories.

Orchestration style is provisional too. The init prompt offers an ETL pipeline
(Lakeflow Spark Declarative Pipelines, a `resources/*.pipeline.yml` over pure `src/`
modules); it is answered no at bootstrap because which orchestration style fits is an
architecture-stage decision routed to `making-architecture-decision` and
`writing-technical-design`. Re-running the choice later costs one resource file, not a
restructure.

Workspace convention (separate from the repo layout, note it, do not scaffold it): git
folders are cloned per-developer under `/Workspace/Users/<email>/<project>`, with a shared
read-only production folder for automation and `/Shared` for cross-team artifacts.

Sources:

1. [Declarative Automation Bundles project templates](https://docs.databricks.com/aws/en/dev-tools/bundles/templates)
2. [Develop pipelines with Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/pipelines-tutorial)
3. [Build a Python wheel file using Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/python-wheel)
4. [Developer best practices on Databricks](https://docs.databricks.com/aws/en/developers/best-practices)
5. [Best practices and recommended CI/CD workflows on Databricks](https://docs.databricks.com/gcp/en/dev-tools/ci-cd/best-practices)
6. [databricks/notebook-best-practices](https://github.com/databricks/notebook-best-practices)

## code — app

Two standard layouts. Create only the side(s) the project actually has — a UI-only project
takes frontend, a service-only project takes backend, a fullstack project takes both.

Fixed layout rules — apply these the same way every run, they are not judgement calls:

- Place the frontend at top-level `src/` and the backend at top-level `apps/`. Do not add
  `frontend/` or `backend/` wrapper directories. Both reference standards are already
  top-level layouts, so wrapping them is an unforced divergence.
- Scaffold one `apps/<domain>/` for every business domain the brief names, each with its
  three tiers (`entry-points/api/`, `domain/`, `data-access/`). Never leave `apps/` empty.
  The brief names the domains, so scaffolding them is grounded, not speculative.
- Derive each domain folder name from the brief's business nouns in kebab-case. "Work items"
  becomes `work-items`, not `workitems`. Do not collapse or re-case the term — the import
  path depends on it.
- Scaffold the frontend `src/` set exactly: `app/`, `assets/`, `components/`, `config/`,
  `features/`, `testing/`, `types/`, `utils/` — these eight, and no others, at bootstrap.
  Include `assets/` even when it starts empty; do not drop it. The bulletproof-react layout
  below also shows `hooks/`, `lib/`, and `stores/` — those three are deferred to the first
  shared consumer, not scaffolded now.
- Leave `src/features/` empty at bootstrap. Do not pre-scaffold per-feature subfolders
  (`src/features/<feature>/`); create each one when its feature arrives. This is the same
  first-consumer rule applied to `apps/<domain>/` tiers, mirrored on the frontend so the two
  sides do not diverge.
- Defer the per-domain `test/` directory until the first test is written. Do not scaffold it
  at bootstrap, and apply this uniformly to every domain so runs do not diverge on it.
- Defer `libraries/` until a second component needs a shared concern. Do not create it at
  bootstrap.

### frontend (React) — bulletproof-react (`alan2207/bulletproof-react`)

```
e2e/                  E2E scenarios (Cypress / Playwright) — root level, outside src/
src/
├── app/              app entry: routes, providers, router
├── assets/
├── components/       shared, cross-app components — co-located *.test.tsx or __tests__/
├── config/           env vars, global config
├── features/         feature-based modules — the core idea
│   └── <feature>/
│       ├── api/
│       ├── components/   ui + co-located tests, like every source folder
│       ├── hooks/
│       ├── stores/
│       └── types/
├── hooks/            shared hooks
├── lib/              preconfigured third-party libs
├── stores/           global state
├── testing/          test infrastructure only (test-utils, MSW) — never test scenarios
├── types/
└── utils/
```

Rationale — strengths:

- Feature isolation is a lint-enforced contract, not a folder convention —
  the ESLint zones below are what make the boundary real.
- `lib/` concentrates vendor coupling (axios instance, query client) in one
  place — eases swaps and mocking.
- Feature-local `stores/` plus a near-empty global `stores/` keeps state where
  its consumers are.

Rationale — watch-outs:

- The shared/feature duality (`components`, `hooks`, `stores`, `types` at both
  levels) invites dumping grounds without a promotion rule.
- Cross-feature imports are the long-term failure mode; the structure does not
  prevent them by itself.
- Root `utils/` and `types/` are entropy magnets — a fat `utils/` signals
  feature logic leaking out.

Conventions — initiated with the tree, they are the structure's other half:

- Dependency rule: features never import each other. Composition happens in
  `app/`. Unidirectional flow: shared → features → app. Shared layers
  (`components/`, `hooks/`, `lib/`, `stores/`, `types/`, `utils/`, `config/`,
  `testing/`) never import from `features/` or `app/`.
- Import rule: import files directly — no barrel files (`index.ts`). The
  reference doc dropped barrels: they break Vite tree shaking and cost
  performance. The boundary is held by lint zones, not by an entry file.
- Promotion rule: code is born in its feature; it moves to a shared layer at
  the second consumer, not before.
- State rule: global `stores/` holds app-wide concerns only (auth, theme).
  Server state goes to the query cache; the rest stays feature-local.
- Enforcement: encode the dependency rule in ESLint via
  `import/no-restricted-paths` zones (the reference standard's mechanism:
  one zone per feature blocking the rest of `features/`, plus zones enforcing
  the unidirectional flow). `eslint-plugin-boundaries` is a viable alternative.
  Prose conventions erode; lint holds.

Tests: co-located next to source — sibling `*.test.tsx` or a `__tests__/` folder, both are
the reference idiom. `src/testing/` holds only shared infrastructure (test-utils wrapper,
MSW handlers and mock DB), never the tests. E2E tests live in root-level `e2e/`, outside
`src/`, created at the first E2E test.

Deferred: create `features/<feature>/` per feature as it arrives, and inside a feature only
the sub-folders it uses. `stores/`, `lib/`, `hooks/` at the first shared consumer. `e2e/` at
the first E2E test.

Sources:

1. [bulletproof-react — project structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md)
2. [bulletproof-react — testing](https://github.com/alan2207/bulletproof-react/blob/master/docs/testing.md)

### backend (Node.js) — nodebestpractices (`goldbergyoni/nodebestpractices`)

```
apps/                  components, one per business domain
├── orders/
│   ├── entry-points/
│   │   ├── api/       controllers — thin adapters, first validation only
│   │   └── message-queue/
│   ├── domain/        DTOs, services, business logic
│   └── data-access/   DB calls, wraps persistence — ORM/DB types stay here
├── users/
└── payments/
libraries/             cross-cutting, reusable across apps
├── logger/
└── authenticator/
```

Rationale — strengths:

- The 3-tier split separates technical concerns (HTTP, DB) from pure logic —
  the reference standard's stated reason for preferring it over MVC or clean
  architecture: real physical tiers, no extra abstractions.
- Top-level names scream the business domain, not the framework — the tree
  stays legible as the system grows and paves the way to service extraction.
- `libraries/` isolates generic concerns; each can later be wrapped and
  published as a private npm package without touching the components.

Rationale — watch-outs:

- Web objects leaking past `entry-points/` is the named failure mode: passing
  request/response into `domain/` couples logic to the transport and blocks
  reuse by other entry points.
- ORM and DB types leaking out of `data-access/` couple the domain to
  persistence — the layer exists to wrap them.
- `libraries/` invites premature extraction — a concern lands there at its
  second consumer, not on the guess that one will come.

Conventions — initiated with the tree, they are the structure's other half:

- Dependency rule: a component consumes another component only through its
  public interface or API — never by reaching into its folders. Generic
  concerns shared by components live in `libraries/`.
- Boundary rule: `entry-points/` adapts payloads and validates, then calls
  `domain/`; request/response objects never cross into `domain/`;
  ORM/DB types never leave `data-access/`.
- Promotion rule: a concern moves to `libraries/<lib>/` at its second
  consumer, wrapped behind the project's own interface.
- Test rules: API/component tests over the real entry-point first, unit tests
  where logic warrants; AAA structure; no global fixtures or seeds — each test
  adds its own data; E2E runs against a production-like environment.
- Enforcement: encode the component and layer boundaries in ESLint
  (`import/no-restricted-paths` zones or `eslint-plugin-boundaries`) so the
  dependency and boundary rules are lint-held, not prose-held.
  > ⚠️ Unverified — the reference standard endorses linting generically but
  > prescribes no boundary plugin; tool choice mirrors the frontend section.

Tests: prioritise API / component-level testing over pure unit tests — hit the component's
actual entry-point (`api/` controller) over HTTP. Tests live in a parallel `test/` directory
per component, following Arrange-Act-Assert. That `test/` directory is deferred until the
first test is written (see the fixed layout rules), not scaffolded at bootstrap.

Deferred: create one `apps/<domain>/` per domain that exists now, and inside it only the
tiers it uses. `libraries/<lib>/` at the second consumer of that concern. `docs/adr/` at the
first decision.

Sources:

1. [nodebestpractices — README, practices 1.1–1.3 and 4.x](https://github.com/goldbergyoni/nodebestpractices)
2. [nodebestpractices — structure by components](https://github.com/goldbergyoni/nodebestpractices/blob/master/sections/projectstructre/breakintcomponents.md)

## infra

Reference standard: HashiCorp Terraform Style Guide (`developer.hashicorp.com/terraform/language/style`).

```
modules/      reusable modules, no environment values — standard structure (main/variables/outputs.tf)
envs/<env>/   thin composition roots (dev, uat, prod) — own backend.tf, own state file
```

CI files live where the platform requires them (`.github/workflows/`, `azure-pipelines.yml`)
— no custom directory.

Rationale — strengths:

- One state file per environment is the point of the layout: a failed apply in
  dev cannot touch prod state, and blast radius is bounded from the first commit.
- Modules force parameterisation — everything env-specific arrives as a
  variable, so the same code path serves every environment.
- The layout matches the official standard, so Terraform tooling (registry,
  doc generation, `terraform test`) works without adaptation.

Rationale — watch-outs:

- Env-root drift: dev/uat/prod composition roots are near-copies, and they
  diverge silently. Keeping them thin is what keeps their diffs reviewable.
- Single-repo modules are the documented monorepo variant; its named cost is
  CI — every workflow must target the modified directories, not the repo.
- Version pins duplicated across env roots drift apart — align them
  deliberately at every upgrade.

Conventions — initiated with the tree, they are the structure's other half:

- Composition rule: `envs/<env>/` holds module calls, environment parameters,
  and its own backend config — nothing else. Resource logic never lives in an
  env root.
- Module rule: modules group logically related resources, follow the standard
  structure (`main.tf`, `variables.tf`, `outputs.tf`), and never configure
  a backend or hardcode environment values.
- Pinning rule: pin the Terraform binary (`required_version`), providers
  (`required_providers`), and module versions from the first commit.
- State and secrets rule: state holds secrets in plaintext — remote backend
  per environment; never commit `terraform.tfstate*`, `.terraform/`, saved
  plans, or sensitive `.tfvars`; always commit `.terraform.lock.hcl`. No
  long-lived static credentials — dynamic credentials or environment variables.
- Promotion rule: a module leaves `modules/` for its own repository (and
  registry versioning) at its first consumer outside this repo.
- Enforcement: `terraform fmt` and `terraform validate` as pre-commit hooks;
  TFLint in CI; `terraform test` on modules as a pre-merge check — deferred to
  the first module carrying logic worth testing.

Deferred: split `envs/<env>/` into per-component roots at the second component, to isolate
state blast-radius within an environment, not only across environments. `docs/adr/` at the
first decision. `terraform test` files at the first module with testable logic.

Databricks work is the `code — data` goal, not infra — see that section. One platform lives
in one place, under one goal, per the one-goal-per-repo principle.

Sources:

1. [Terraform Style Guide](https://developer.hashicorp.com/terraform/language/style)

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 2.1        |
| Last Updated | 2026-07-16 |
| Status       | Review     |
