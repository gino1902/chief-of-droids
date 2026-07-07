# Project Layout Standards — Reference Session

## 1. Frontend (React) — bulletproof-react

`alan2207/bulletproof-react` — closest equivalent for React apps.

```
src/
├── app/              # app entry: routes, provider, router
├── assets/
├── components/       # shared, cross-app components
├── config/           # env vars, global config
├── features/         # feature-based modules ← the core idea
│   └── awesome-feature/
│       ├── api/
│       ├── components/
│       ├── hooks/
│       ├── stores/
│       ├── types/
│       └── index.ts  # public API of the feature
├── hooks/            # shared hooks
├── lib/              # preconfigured third-party libs
├── stores/           # global state
├── testing/          # shared test utils/mocks only
├── types/
└── utils/
```

**Core rule:** features are self-contained; don't import across features — compose at the `app/` layer.

**Tests:** co-located next to source (`Button.tsx` + `Button.test.tsx`). `src/testing/` holds only shared setup (test-utils wrapper, MSW server), not the tests themselves. E2E tests (Cypress/Playwright) usually live in their own root-level folder outside `src/`.

---

## 2. Backend (Node.js) — nodebestpractices

`goldbergyoni/nodebestpractices` — de facto Node.js backend standard (~104k stars).

```
my-system/
├── apps/                  # components, one per business domain
│   ├── orders/
│   │   ├── entry-points/
│   │   │   ├── api/       # controllers
│   │   │   └── message-queue/
│   │   ├── domain/        # DTOs, services, business logic
│   │   └── data-access/   # DB calls
│   ├── users/
│   └── payments/
└── libraries/              # cross-cutting, reusable across apps
    ├── logger/
    └── authenticator/
```

**Core rule:** 3-tier split per component (entry-points → domain → data-access); top-level folder names should "scream" the business domain, not the framework (not "Rails-like" or "Spring-like").

**Tests:** prioritizes API/component-level testing over pure unit tests — hit the component's actual entry-point (`api/` controller) via HTTP. Tests typically live in a parallel `test/` directory per component, following the AAA pattern (Arrange-Act-Assert).

---

## 3. Databricks — Asset Bundles `default-python` template

`databricks bundle init` — Databricks' own official reference scaffold (formerly "Databricks Asset Bundles," now "Declarative Automation Bundles"). Companion reference repo: `databricks/notebook-best-practices`.

```
my_project/
├── databricks.yml         # bundle definition, targets (dev/prod)
├── README.md
├── pyproject.toml         # deps, managed via uv
├── src/
│   └── my_project/
│       ├── main.py        # importable, testable package code
│       └── notebook.ipynb # thin orchestration notebook, imports the package
├── resources/
│   └── my_project_job.yml # job/workflow definitions
├── tests/
│   └── main_test.py       # unit tests against the package, via databricks-connect
└── scratch/
    └── exploration.ipynb  # throwaway/ad-hoc notebooks, not deployed
```

**Core rule:** keep notebooks thin (orchestration only); push real logic into an importable `src/` package so it's unit-testable. `resources/` + `databricks.yml` handle deployment/orchestration separately from code.

**Tests:** dedicated top-level `tests/` folder, parallel to `src/`, testing the importable package directly via `databricks-connect` — not the notebook itself.

Workspace-level convention (separate from repo layout): Git folders cloned per-developer under `/Workspace/Users/<email>/<project>`, a shared read-only production Git folder for automation, `/Shared` for cross-team artifacts, dev/staging/prod separated by workspace or folder+branch.

---

## Cross-cutting pattern

All four converge on the same underlying principle:

> **Separate orchestration/entry-point code from business logic, and keep logic in importable, testable units rather than scripts or monolithic files.**

| Ecosystem | Entry-point layer | Logic layer | Test location |
|---|---|---|---|
| Go | `cmd/` | `internal/`, `pkg/` | co-located `_test.go` |
| Frontend | `app/` (routes/router) | `features/*` | co-located `*.test.tsx` |
| Backend (Node) | `entry-points/api` | `domain/` | parallel `test/` per component |
| Databricks | `notebook.ipynb` | `src/<package>/` | top-level `tests/` |
