# Conventions workflow explained

For a junior dev who runs `bootstrapping-project`, or who opens a repo it created and needs to
understand the convention machinery. It assumes you know git and a terminal, and nothing about the
skill. It explains the idea first, then gives a short runbook.

## The idea in one paragraph

A project's folder structure implies rules about what may import what, where code lives, and how a
piece of code graduates from one layer to the next. Those rules usually live in someone's head and
slowly rot. This workflow writes them down once in a file called `CONVENTIONS.md`, has a linter
enforce them so they cannot quietly erode, and ships a small script that flags when a rule changes
without a recorded decision. The structure is one half of the picture and the rules that guard it
are the other. You can change a rule, but the change has to be a recorded decision rather than a
quiet edit.

## The four artifacts

Four files carry the workflow.

- `CONVENTIONS.md` is the contract. It states the dependency, import, and promotion rules in plain
  words, and ends with a small machine-readable block naming the linter config and the command
  that runs it.
- The lint config is the linter that actually encodes the rules. For an app that is an ESLint
  config with import-boundary zones. For data it is a ruff config.
- The gate is a pre-commit hook that runs the linter and blocks a commit that breaks the rules.
- `scripts/check-conventions-drift.sh` is the guard. It checks that the contract, the config, and
  the tree still agree, and that any change to the contract is tied to a decision record.

## The part that trips people up: two lifecycles

The workflow lives in two separate worlds. Mixing them up is the main source of confusion, so keep
them apart and the rest is easy.

### Creation, inside Claude Code

This is the Claude Code session. It runs once when you bootstrap the project, and again if you
re-run the skill later to reconcile.

You invoke `bootstrapping-project`. Claude Code loads the skill, then reads one reference file per
step as it needs it. The skill works in four passes, in order. It sets up the environment, writes
FRAMING.md, builds the tree and writes `CONVENTIONS.md`, then writes CLAUDE.md and generates the
enforcement. Every file it writes is checked against your permission settings. The project's
baseline turns on `acceptEdits`, so writes inside the project folder go through without asking. A
network call, such as the version lookup below, or a delete can still stop to ask. At the end it
writes the lint config and the gate, copies the guard script into `scripts/`, and looks up the
linter's real current version with `git ls-remote` instead of guessing one.

That is all Claude Code does. Once the session ends it is gone, and it does not watch your commits.

### Enforcement, outside Claude Code

This is git and your CI. It runs for the life of the project, for everyone who touches the repo,
whether or not they ever use Claude.

Every time someone runs `git commit`, the gate runs the linter and the guard's basic checks, that
the config still exists and that every folder needing a rule has one. A failure blocks the commit.
On a pull request, CI runs the guard's traceability check. If `CONVENTIONS.md` or the lint config
changed but no decision record was added, it flags the change.

Claude Code is not part of this, and that is on purpose. A rule that only bound Claude's sessions
would not bind the person who edits the repo in a plain editor. The gate is a normal project file,
so it binds everyone.

### "Hook" means two different things

This is the mix-up to watch for.

A harness hook lives in `.claude/settings.json`. It is Claude Code automation. This workflow never
writes one, and `settings.json` is written once at bootstrap and then left alone. A git hook lives
in `.husky/pre-commit`, or is declared in `.pre-commit-config.yaml`. It is the gate, and it runs on
`git commit` for anyone. When this doc says "the gate" it means the git one.

## What each project type gets

A repo has one goal, and the goal decides the stack, which decides the gate.

| Goal | Lint config | Gate | Guarded folders |
|:--|:--|:--|:--|
| code, app (Node or TS) | ESLint with import-boundary zones | husky pre-commit | `apps/*`, `src/features/*`, whichever sides exist |
| code, data (Python) | ruff config in `pyproject.toml` | `.pre-commit-config.yaml` (ruff) | none, ruff is file-level |
| infra (Terraform) | `.tflint.hcl` | `.pre-commit-config.yaml` (fmt, validate, tflint) | none |
| thinking | none, review is the gate | none | none |

The thinking goal has no linter. Its rules are held by review, and the guard still checks that a
change to `CONVENTIONS.md` traces back to a record in `decisions/`.

## The lifecycle in motion

Four things happen to a project over time. Each one belongs to a lifecycle above.

- A fresh bootstrap is creation. The skill writes all four artifacts against a new tree, and looks
  up the linter version live so it is real and current.
- Adding the contract to an older repo is creation, in reconcile mode. Re-run the skill. It sees
  the tree exists but `CONVENTIONS.md` does not, and backfills the contract, config, gate, and
  guard against the tree already there, without reorganising it. It adds only what is missing.
- A linter version bump is routine enforcement. Over months the pinned version ages. The project's
  own tooling, `pre-commit autoupdate` or a bot like Renovate, opens a pull request to bump it. The
  guard does not treat this as a contract change, because the version lives in the gate file, which
  the traceability check does not watch.
- A convention change is deliberate enforcement. Someone wants to change a rule. They edit
  `CONVENTIONS.md` and its lint config together, and add a decision record under `docs/adr/` or
  `decisions/`. Without that record the guard fails the pull request. That is the whole point.
  Rules can change, but only on purpose and on the record.

## Why it is built this way

- The rules are written down because rules in a head rot. `CONVENTIONS.md` is the one source of
  truth.
- A linter enforces them because a written rule is followed about 70 percent of the time and a gate
  is followed every time.
- The gate is a project file, not Claude Code config, so it binds every contributor.
- The guard ships inside the project, so the guarantee travels with the repo, not with whoever
  happens to have the skill installed.
- The linter version is looked up, not guessed, so day one is real, and the project's own tooling
  keeps it fresh after that.

## Runbook

The commands a dev actually runs.

Bootstrap a new project. In an empty project folder, from a Claude Code session, invoke the
`bootstrapping-project` skill and answer its questions. It writes `CONVENTIONS.md`, the lint config,
the gate, and `scripts/check-conventions-drift.sh`.

Add the contract to an older repo that does not have one. Re-run `bootstrapping-project` on the
repo. It backfills against the existing tree.

Check for drift locally. This runs the existence and coverage checks, and needs no history.

```sh
bash scripts/check-conventions-drift.sh .
```

Check traceability in CI, against the branch you are merging into.

```sh
bash scripts/check-conventions-drift.sh . "$MERGE_BASE"   # for example origin/main
```

Change a convention the right way.

```sh
# 1. edit CONVENTIONS.md and the lint config together
# 2. add a decision record, for example docs/adr/adr-0001-allow-shared-utils.md
# 3. commit. the guard passes because the change is recorded
```

Bump the linter version when it ages.

```sh
pre-commit autoupdate   # rewrites the version to the current release, then commit the result
```

If `check-conventions-drift.sh` fails, read the one line it prints. "folder unenforced" means a new
folder needs a lint rule. "contract changed with no decision record" means add the decision record.
"config missing" means the lint config the contract names is gone.

---

| Field        | Value      |
|--------------|------------|
| Version      | 1.2        |
| Last Updated | 2026-07-19 |
| Status       | Draft      |
