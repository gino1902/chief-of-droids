<!-- pass D reference for project-bootstrapping -->

# Pass D — project tree

Turns the intent in FRAMING.md into a source layout. Two rules govern this pass.

First, only scaffold on an empty repo. If source files already exist, do not propose a
reorganisation — document the existing structure so pass B can describe it accurately, and
skip creation. Reorganising someone's repo is rarely wanted and never safe by default.

Second, every directory must be justified now, not speculatively. Create only what the
project needs today. The deferred directories listed under each tree are created later,
when the trigger for them actually occurs — this keeps the tree honest and readable.

Create approved directories via `.gitkeep` files so they are tracked by git.

Resolve `<placeholders>` from the project name, or ask.

## thinking

```
decisions/    ADRs (NNNN-title.md), superseded, never edited
notes/        living working and meeting notes
diagrams/     Mermaid / C4 sources
references/   documents that ground the decisions
```

Ask the code sub-type question first: data or app.

## code — data

Databricks Asset Bundles, `default-python` template (`databricks bundle init`; companion
reference `databricks/notebook-best-practices`).

```
databricks.yml            bundle definition, targets (dev/prod)
pyproject.toml            deps, managed via uv
src/<pkg>/
  main.py                 importable, testable package code
  notebook.ipynb          thin orchestration notebook, imports the package
resources/
  <pkg>_job.yml           job / workflow definitions
tests/
  main_test.py            unit tests against the package, via databricks-connect
```

Core rule: keep notebooks thin (orchestration only) and push real logic into the importable
`src/` package so it is unit-testable. `resources/` and `databricks.yml` handle deployment
and orchestration separately from code.

Tests: a dedicated top-level `tests/` parallel to `src/`, testing the importable package
directly via `databricks-connect`, not the notebook itself.

Deferred: `scratch/exploration.ipynb` for throwaway notebooks, added at the first ad-hoc
exploration (never deployed). A second `resources/*.yml` at the second job. `docs/adr/` at
the first decision.

Workspace convention (separate from the repo layout, note it, do not scaffold it): git
folders are cloned per-developer under `/Workspace/Users/<email>/<project>`, with a shared
read-only production folder for automation and `/Shared` for cross-team artifacts.

## code — app

Two standard layouts. Create only the side(s) the project actually has — a UI-only project
takes frontend, a service-only project takes backend, a fullstack project takes both.

### frontend (React) — bulletproof-react (`alan2207/bulletproof-react`)

```
src/
├── app/              app entry: routes, providers, router
├── assets/
├── components/       shared, cross-app components
├── config/           env vars, global config
├── features/         feature-based modules — the core idea
│   └── <feature>/
│       ├── api/
│       ├── components/
│       ├── hooks/
│       ├── stores/
│       ├── types/
│       └── index.ts  public API of the feature
├── hooks/            shared hooks
├── lib/              preconfigured third-party libs
├── stores/           global state
├── testing/          shared test utils / mocks only
├── types/
└── utils/
```

Core rule: features are self-contained. Do not import across features — compose them at the
`app/` layer.

Tests: co-located next to source (`Button.tsx` + `Button.test.tsx`). `src/testing/` holds
only shared setup (test-utils wrapper, MSW server), not the tests. E2E tests (Cypress /
Playwright) live in their own root-level folder outside `src/`.

Deferred: create `features/<feature>/` per feature as it arrives, and inside a feature only
the sub-folders it uses. `stores/`, `lib/`, `hooks/` at the first shared consumer.

### backend (Node.js) — nodebestpractices (`goldbergyoni/nodebestpractices`)

```
apps/                  components, one per business domain
├── orders/
│   ├── entry-points/
│   │   ├── api/       controllers
│   │   └── message-queue/
│   ├── domain/        DTOs, services, business logic
│   └── data-access/   DB calls
├── users/
└── payments/
libraries/             cross-cutting, reusable across apps
├── logger/
└── authenticator/
```

Core rule: a 3-tier split per component (entry-points then domain then data-access). Top-level
folder names should scream the business domain, not the framework.

Tests: prioritise API / component-level testing over pure unit tests — hit the component's
actual entry-point (`api/` controller) over HTTP. Tests live in a parallel `test/` directory
per component, following Arrange-Act-Assert.

Deferred: create one `apps/<domain>/` per domain that exists now, and inside it only the
tiers it uses. `libraries/<lib>/` at the second consumer of that concern. `docs/adr/` at the
first decision.

## infra

```
modules/      reusable modules, no environment values
envs/<env>/   thin composition roots (dev, uat, prod)
```

CI files live where the platform requires them (`.github/workflows/`, `azure-pipelines.yml`)
— no custom directory. Deferred: split `envs/<env>/` into per-component roots at the second
component, to isolate state blast-radius within an environment, not only across environments.
`docs/adr/` at the first decision.

Databricks work is the `code — data` goal, not infra — see that section. One platform lives
in one place, under one goal, per the one-goal-per-repo principle.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.3        |
| Last Updated | 2026-07-07 |
| Status       | Review     |
