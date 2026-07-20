# Handover: consolidate the requirements-chain test suite into tests/

A one-session migration to be run in a clean session, not during a deploy and not while other sessions are writing the repo. It removes the split that scattered the suite across `requirements/` and `testing/`, and aligns names with convention.

## Why

`requirements/` is the skill backlog (to-do and in-progress skill requirements). The test suite does not belong there. Today the durable suite artifacts sit in `requirements/tests/` and loose in `requirements/`, while `testing/` holds generated run instances. Convention: `tests/` is where a suite lives, `testing/` has no distinct role beside it and should be retired, and generated run outputs are gitignored scratch, not tracked. This move applies that.

## Preconditions

- The repo is quiet. `skills-lab` is a subdirectory of the `chief-of-droids` git repo, so the index is shared across sessions. Do this only when nothing else is staging or committing.
- On a branch, tree otherwise clean.
- After any pending deploy. `deploy.sh` blocks on a dirty tree, and this move dirties it. The move does not affect deploy, which ships `.claude/skills/` only.

## Target structure

```
tests/requirements-chain/
  test-strategy.md
  scope-map.md
  FRAMING.md
  <the 15 chain scenario .md files>
  bootstrapping-conventions-generation-test.md   # BC-1
  bootstrapping-drift-check-test.md              # BC-2
  bootstrapping-pinned-contract-test.md          # BC-3
  bootstrapping-backfill-test.md                 # BC-4
  verify-summary-info-tally.md
  design.md                        # from requirements-chain-design.md
  conventions-validation-run.md    # from requirements-chain-conventions-validation-run.md
  retrospectives/
    run1.md                        # from requirements-chain-test-retrospective-run1.md
    run2.md                        # from requirements-chain-test-retrospective-run2.md
  checks/
    check-summary-tally.sh
    check-diff-confined.sh
    check-conventions-drift.sh
    check-conventions-contract.sh
    check-pinned-contract.sh
requirements/          # skill backlog only, suite removed
tests/.runs/           # gitignored run scratch (replaces testing/ and the test-* dirs in outputs/)
```

## Moves, run from `skills-lab/`

```
git mv requirements/tests tests/requirements-chain
mkdir -p tests/requirements-chain/retrospectives
git mv requirements/requirements-chain-test-retrospective-run1.md tests/requirements-chain/retrospectives/run1.md
git mv requirements/requirements-chain-test-retrospective-run2.md tests/requirements-chain/retrospectives/run2.md
git mv requirements/requirements-chain-design.md tests/requirements-chain/design.md
git mv requirements/requirements-chain-conventions-validation-run.md tests/requirements-chain/conventions-validation-run.md
```

`git mv` of the directory carries `checks/` and every spec with it. The within-suite links that were same-directory stay valid, only the renamed docs and the retrospectives moving into `retrospectives/` need path fixes below.

## Reference updates

Find every reference, then fix:

```
grep -rl "requirements/tests"                              .   # exclude .git
grep -rl "requirements-chain-test-retrospective-run"       .
grep -rl "requirements-chain-design"                       .
grep -rl "requirements-chain-conventions-validation-run"   .
```

Expected edits, at least:

- `tests/requirements-chain/test-strategy.md`: its companion line points to `requirements-chain-design.md` (now `design.md`, same dir) and the run-through links point to the retrospectives (now `retrospectives/run1.md`, `retrospectives/run2.md`).
- `tests/requirements-chain/retrospectives/run1.md` and `run2.md`: links to `test-strategy.md` and the design doc, and to each other.
- `tests/requirements-chain/conventions-validation-run.md`: its plan pointer to `tests/test-strategy.md`.
- `tests/requirements-chain/FRAMING.md`: the provisional-location line, update to state the settled home.
- `CLAUDE.md`: confirm by grep whether it names any suite path; the humanizer-scope line references the suite by role, not path, so likely no change.
- Any skill or doc the greps surface.

## Scratch, handled separately and last

- Add the run-scratch dir to `.gitignore` and stop tracking generated runs. Create `tests/.runs/` for new runs and point scenarios there.
- `testing/` is heavy, each run instance carries its own nested `.git`, and parallel sessions write into it. Do not fight active writers. Safest sequence: gitignore first, then `git rm -r --cached` the tracked run dirs, then delete on disk only once the repo is quiet.
- The `test-*`, `verify-*` dirs under `outputs/` are older scratch of the same kind, treat them the same.

## Commit discipline

- The shared index means `git commit` sweeps whatever any session has staged. Commit with an explicit pathspec so only the intended paths land: `git commit -m "..." -- <paths>`.
- Commit the renames as one move, then the reference-fix edits, then the scratch gitignore, each scoped by pathspec.

## Settled decisions carried into this move

- `tests/` is the suite home, plural, per convention.
- `testing/` is retired, no distinct role beside `tests/`.
- Run outputs are gitignored scratch under `.runs/`, never committed.
- `requirements/` is skill backlog only.

## Do not

- Do not run during a deploy or with other sessions active.
- Do not commit run scratch.
- Do not `git add -A` then commit, it will sweep parallel work, use pathspecs.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-20 |
| Status       | Draft      |
