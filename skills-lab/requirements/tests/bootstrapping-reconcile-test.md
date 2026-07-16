# Bootstrapping reconcile test — MD-5

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this after a fresh `chain-test-medium.md`, in a session at the Medium base.

## Purpose

Exercise `bootstrapping-project` re-invoked on a repo where all four passes have already run. It must reconcile, not regenerate: detect each pass as done, route the FRAMING rework by creation branch, document the existing tree rather than reorganise it, and reconcile `CLAUDE.md` by filling gaps and dropping ungrounded lines while preserving wording. The goal stays locked by the stamp and `settings.json` is not touched.

## Directory and precedence

Directory: `outputs/test-medium`, created by `chain-test-medium.md`, not by this test.

Precedence: run against a fresh Medium base. Empty `outputs/test-medium`, run `chain-test-medium.md` into it, then run this test.

## Preconditions

- The base is present from a fresh `chain-test-medium.md` run: `outputs/test-medium` holds `.claude/settings.json`, `FRAMING.md` (framing-project shape with `last_updated` and the `<!-- goal: code -->` stamp), `CONCEPTS.md`, `CONVENTIONS.md`, a data-bundle tree anchor, and `CLAUDE.md`.
- Session cwd is `skills-lab/outputs/test-medium`.

## Reset to the committed base (before acting)

Reconcile-not-regenerate is a no-change claim across the whole tree, so it is only provable against the pristine base. `chain-test-medium` commits the base in `test-medium`'s own repo (see its Record step); that commit, `<base-commit>`, is the diff reference. From inside `outputs/test-medium`, reset to it before re-invoking bootstrapping:

```
git reset --hard <base-commit>
git clean -fd
```

`<base-commit>` is the base repo's HEAD after a fresh `chain-test-medium` run. Note this row re-runs bootstrapping, whose Pass 1 keys on `.git/` plus `.claude/settings.json`. The base repo, created during the base build, is exactly the existing-repo state reconcile must detect, so resetting to `<base-commit>` sets up that precondition directly. The Record step diffs the working tree against it.

## Run steps

### 1. Re-invoke bootstrapping

Invoke `bootstrapping-project`. Let it run the Preamble, report per-pass status, and resume in reconcile mode.

Expected routing:

- Pass 1: detects `.git`/`.claude/settings.json` present, reports done, does not rewrite `settings.json`.
- Pass 2: reads the goal from the stamp (code). Because `FRAMING.md` carries a `last_updated` key, it routes the rework to `framing-project` (the update branch), and does not ask the size question or run an inline five-question reconcile. If no gap needs filling, it leaves `FRAMING.md` as is.
- Pass 3: sees the existing tree, documents it, proposes no reorganisation. `CONVENTIONS.md` already exists, so it reconciles against the goal's conventions block with a minimal diff at most, never regenerates.
- Pass 4: reconciles `CLAUDE.md` against the code skeleton, filling any gap and dropping any ungrounded line, preserving wording, applied only on approval. The enforcement tail leaves the already-generated lint config in place rather than regenerating it.

Approve nothing that regenerates. Accept only gap-filling reconciliation.

## Expected outputs (under `outputs/test-medium`)

- No new artifacts. `settings.json`, `FRAMING.md`, `CONCEPTS.md`, `CONVENTIONS.md` and its lint config, and the tree are unchanged unless a genuine gap was filled.
- `CLAUDE.md` either unchanged or minimally reconciled, with its goal stamp and wording intact.

## Acceptance criteria

- The goal stays `code`, read from the stamp, never re-asked.
- Pass 2 routes to the `framing-project` update branch (not inline reconcile) and does not ask the Small/Medium+ size question.
- The tree is documented, not reorganised.
- `CONVENTIONS.md` is reconciled, not regenerated: its wording and enforcement stanza survive unchanged unless a genuine gap was filled.
- `CLAUDE.md` is reconciled, not regenerated wholesale, and stays under 60 lines.
- `settings.json` is not mutated (it is written once, in Pass 1 of the original run).

## Fail conditions

- Any artifact is regenerated wholesale.
- The size question is asked again, or an inline five-question reconcile runs on a framing-project doc.
- `settings.json` is rewritten.
- The tree is reorganised, or the goal stamp is changed.

## Record

Note which passes reported done versus reconciled, and confirm the FRAMING rework went to the framing-project branch. Then emit the whole-tree diff against the committed base as evidence, from inside `outputs/test-medium`:

```
git diff <base-commit> > ../test-medium.md-5.diff
```

The diff must be either empty or confined to gap-filling `CLAUDE.md` lines. `settings.json`, `FRAMING.md`, `CONCEPTS.md`, `CONVENTIONS.md` (and its lint config), and the tree must be absent from it. Any of those appearing is a regeneration, not a reconcile. Keep `outputs/test-medium.md-5.diff` as the evidence artifact.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.3        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
