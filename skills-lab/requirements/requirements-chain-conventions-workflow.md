# Conventions workflow explained

For a junior dev who runs `bootstrapping-project`, or who lands in a repo it created and has to
understand the convention machinery. It assumes git and a terminal. It assumes nothing about the
skill. Explainer first, a short runbook at the end.

## The one-paragraph model

A project's folder structure implies rules: what may import what, where code lives, how a concern
graduates from one layer to another. Those rules usually live in someone's head and rot. This
workflow writes them down once, in a file called `CONVENTIONS.md`, makes a linter enforce them so
they cannot quietly erode, and ships a small script that flags when the rules change without a
recorded decision. Structure on one side, the rules that guard it on the other. Changing a rule is
allowed, but it has to be a deliberate, recorded decision, not a silent edit.

Four artifacts carry it:

- `CONVENTIONS.md` — the contract. The dependency, import, and promotion rules in plain words,
  plus a small machine-readable block at the bottom naming the linter config and command.
- a lint config — for example an ESLint config with import-boundary zones, or a ruff config. This
  is the linter actually encoding the rules.
- a gate — a pre-commit hook (via husky or the pre-commit framework) that runs the linter, so a
  bad commit is blocked rather than merely frowned upon.
- `scripts/check-conventions-drift.sh` — the guard. It checks the contract, the config, and the
  tree still agree, and that any change to the contract is tied to a decision record.

## The part that trips people up: two lifecycles

The workflow lives in two different worlds, and they are easy to confuse. Keep them apart and
everything else falls into place.

### Lifecycle one: creation, inside Claude Code

This is the Claude Code harness. It runs once, when you bootstrap the project, or again when you
re-run the skill to reconcile.

- You invoke `bootstrapping-project`. The harness loads the skill, then reads one reference file
  per pass as it needs it.
- The skill runs four passes in order: environment, FRAMING.md, the tree plus `CONVENTIONS.md`,
  then CLAUDE.md and an enforcement tail. Each file it writes is a tool call the harness checks
  against your permission settings. The project's baseline sets `acceptEdits`, so writes inside the
  project folder are auto-approved and do not stop to ask. A network call like the version lookup
  below, or a delete, can still prompt.
- At the enforcement tail the skill writes the lint config and the gate, copies the drift-check
  script into `scripts/`, and looks up the real current linter version with `git ls-remote` rather
  than guessing one.

That is the whole involvement of Claude Code. Once the session ends, the harness is gone. It is
not watching your commits.

### Lifecycle two: enforcement, outside Claude Code

This is git and your CI, running for the life of the project, for every contributor, whether or not
they ever use Claude.

- On every `git commit`, the pre-commit gate runs the linter and the drift-check's base checks
  (does the config still exist, does every folder that should be guarded have a rule). A failure
  blocks the commit.
- On a pull request, CI runs the drift-check's traceability check against the branch's target: if
  `CONVENTIONS.md` or the lint config changed but no decision record was added, it flags an
  untraceable change.

Claude Code is not part of this. That is deliberate. A rule that only bound Claude's sessions would
not bind the human who edits the repo in a plain editor. The gate is a project file so it binds
everyone.

### The word "hook" means two different things

This is the single most common mix-up, so say it plainly.

- A harness hook lives in `.claude/settings.json`. It is Claude Code automation, and this workflow
  never writes one. `settings.json` is written once at bootstrap and then left alone.
- A git hook lives in `.husky/pre-commit` or is declared in `.pre-commit-config.yaml`. It is the
  gate. It runs on `git commit`, for anyone.

When this doc says "the gate" or "the pre-commit hook" it means the git one. The harness one is not
in play.

## What each project type gets

The skill locks one goal per repo, and the goal decides the stack and therefore the gate.

| Goal | Lint config | Gate | Guarded folders |
|:--|:--|:--|:--|
| code, app (Node/TS) | ESLint with import-boundary zones | husky pre-commit | `apps/*`, `src/features/*`, the sides that exist |
| code, data (Python) | ruff config in `pyproject.toml` | `.pre-commit-config.yaml` (ruff) | none, ruff is file-level |
| infra (Terraform) | `.tflint.hcl` | `.pre-commit-config.yaml` (fmt, validate, tflint) | none |
| thinking | none, review is the gate | none | none |

The thinking goal has no linter. Its rules (one decision per record, records are immutable once
accepted) are held by review, and the drift-check still guards traceability of `CONVENTIONS.md`
against its `decisions/` records.

## The lifecycle in motion

Four things happen to a project over time. Each maps to one of the two lifecycles above.

- Fresh bootstrap (creation). The skill writes all four artifacts against a new tree. The linter
  version is looked up live so it is real and current.
- An existing repo that predates the contract (creation, reconcile). Re-run the skill. It notices
  the tree exists but `CONVENTIONS.md` does not, and backfills the contract, config, gate, and
  script against the existing tree without reorganising it. Nothing is regenerated, only what is
  missing is added.
- A linter version bump (enforcement, routine). Over months the pinned linter version ages. The
  project's own tooling, `pre-commit autoupdate` or a bot like Renovate, opens a pull request to
  bump it. This is normal maintenance. The drift-check does not treat it as a contract change,
  because the version lives in the gate file, which is outside what the traceability check watches.
- A convention change (enforcement, deliberate). Someone wants to change a rule, say allow a new
  import path. They edit `CONVENTIONS.md` and its lint config together, and they add a decision
  record (an ADR under `docs/adr/` or `decisions/`). Without that record the drift-check fails the
  pull request. This is the whole point: rules can change, but only on purpose and on the record.

## Why it is built this way

- The rules are written down because rules in people's heads rot. `CONVENTIONS.md` is the single
  source of truth.
- A linter enforces them because prose is followed about 70 percent of the time and a gate is
  followed 100 percent. The rule that is only written is the rule that erodes.
- The gate is a project file, not Claude Code config, so it binds every contributor.
- The drift-check ships inside the project so the guarantee travels with the repo, not with whoever
  happens to have the skill installed.
- The linter version is looked up, not guessed, so day one is real and current, then handed to the
  project's own update tooling.

## Runbook

Commands a dev actually runs.

Bootstrap a new project:

```sh
# in an empty project directory, from a Claude Code session
# invoke the bootstrapping-project skill and answer its questions
# it writes CONVENTIONS.md, the lint config, the gate, and scripts/check-conventions-drift.sh
```

Add the contract to an existing repo that does not have one:

```sh
# re-run bootstrapping-project on the repo; it backfills against the existing tree
```

Check for drift locally (existence and coverage, no history needed):

```sh
bash scripts/check-conventions-drift.sh .
```

Check traceability in CI, against the branch you are merging into:

```sh
bash scripts/check-conventions-drift.sh . "$MERGE_BASE"   # e.g. origin/main
```

Change a convention the right way:

```sh
# 1. edit CONVENTIONS.md and the lint config together
# 2. add a decision record, e.g. docs/adr/adr-0001-allow-shared-utils.md
# 3. commit. the drift-check passes because the change is recorded
```

Bump the linter version when it ages:

```sh
pre-commit autoupdate   # rewrites the rev to the current release; commit the result
```

If `check-conventions-drift.sh` fails, read the one line it prints. "folder unenforced" means a new
folder needs a lint zone. "contract changed with no decision record" means add the ADR. "config
missing" means the lint config the contract names is gone.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-19 |
| Status       | Draft      |
