# Backfill on reconcile test: BC-4

_These are illustrative fixtures. The subject, scripted answers, and file names below are examples to make the run concrete, not fixed requirements. The acceptance criteria carry the test._

Bootstrapping-only. One reconcile run against a pre-feature fixture.

## Purpose

Confirm the contract reaches existing repos: re-running `bootstrapping-project` on a pre-feature repo (a scaffolded tree with no `CONVENTIONS.md`) detects Pass 3 as incomplete and backfills the contract, enforcement, and drift-check against the existing tree, without reorganising it. This is the lifecycle half of the feature, for projects that predate it.

## Directory and precedence

Directory: `testing/bc4`. Precedence: none, self-contained, it builds and commits its own pre-feature fixture. After BC-1 and BC-2 are green.

## Preconditions

- A fresh session or subagent.
- `testing/bc4` holds a constructed pre-feature fixture: an app-backend tree plus `CLAUDE.md`, with `CONVENTIONS.md`, the lint config, the gate, and the drift-check removed and the `CLAUDE.md` pointer stripped, committed as the base.
- Session cwd is that directory.

## Run steps

1. Re-invoke `bootstrapping-project`. Let the Preamble detect Pass 3 incomplete (tree present, `CONVENTIONS.md` absent) and resume to backfill. Approve gap-filling only, reject any regeneration.

## Expected outputs (under `testing/bc4`)

- Added: `CONVENTIONS.md`, the lint config, the gate, and `scripts/check-conventions-drift.sh`.
- `CLAUDE.md` reconciled: the `CONVENTIONS.md` pointer added, nothing removed.
- The existing tree (`apps/`), `FRAMING.md`, and `settings.json` absent from the diff.
- The backfilled husky hook byte-identical to the pinned template, and the delivered drift-check passes.

## Acceptance criteria

- The diff against the pre-feature base is additive: the backfill set only, with the tree, `FRAMING.md`, and `settings.json` absent.
- The `CLAUDE.md` change is the pointer added, zero lines removed.
- The backfilled husky hook equals the pinned template.
- The backfilled project's own `check-conventions-drift.sh` passes.

Check: `checks/check-diff-confined.sh --no-deletions <dir> <base> CONVENTIONS.md '<config>' '<gate>' 'scripts/check-conventions-drift.sh' CLAUDE.md`, then the delivered drift-check. One reconcile run, disk-only checks.

## Fail conditions

- The tree, `FRAMING.md`, or `settings.json` appears in the diff.
- `CLAUDE.md` is regenerated (any line removed) rather than reconciled.
- The husky hook differs from the pinned template, or the delivered drift-check fails.
- Pass 3 is reported done, so the backfill is skipped on the pre-feature repo.

## Record

The additive diff contents, the `CLAUDE.md` added-versus-removed counts, and the delivered drift-check result.

## Note

The reconcile counterpart is MD-5, a fully-bootstrapped repo where reconcile is a no-op. BC-4 is the pre-feature case, where reconcile must backfill rather than report done.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-20 |
| Status       | Draft      |
