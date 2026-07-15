# Framing update test — MD-2, framing-project update run

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this after a fresh `chain-test-medium.md`, in a session at the Medium base.

## Purpose

Exercise the canonical upstream-change event: `framing-project` run a second time on an existing `FRAMING.md`. It should take its update path, revisit only the section the user picks, preserve every other section verbatim, bump `last_updated`, and touch `CONCEPTS.md` only if a term or boundary actually moved. This proves the intent anchor can evolve without a wholesale rewrite, which is what every downstream re-run depends on.

## Directory and precedence

Directory: `outputs/test-medium`, created by `chain-test-medium.md`, not by this test.

Precedence: run against a fresh Medium base. Empty `outputs/test-medium`, run `chain-test-medium.md` into it, then run this test.

## Preconditions

- The base is present from a fresh `chain-test-medium.md` run: `outputs/test-medium` holds a framing-project-shaped `FRAMING.md` (YAML frontmatter with `last_updated`, three Tracks) and a context-structured `CONCEPTS.md`.
- Session cwd is `skills-lab/outputs/test-medium`.

## Base snapshot (before acting)

The scenario edits `FRAMING.md` in place, so the pristine base is destroyed the moment `framing-project` runs. Before invoking anything, snapshot the fresh base from the skills-lab repo root so the no-change criteria can be proven as a diff:

```
cp -R outputs/test-medium outputs/test-medium.base
```

Use a filesystem copy, not a nested `git init` inside the test dir. An added `.git/` would perturb the bootstrapping detection sibling rows exercise (see the git-init open item in `test-strategy.md`). The diff in Record compares the copy against the post-run dir with `git diff --no-index`, which needs no repo.

## Run steps

### 1. Invoke the update

Invoke `framing-project`. Phase 0 finds the existing `FRAMING.md` and announces the update path. When asked which section to revisit, pick "Our approach".

Answer the re-interview so the change is a wording sharpening, not a boundary move:

- Our approach: we reach trusted cross-team reporting by building one governed data platform on a medallion architecture, delivered one use case at a time, and we prove it on the finance-operations reconciliation case first before widening.

This refines the approach without introducing or moving any domain term or boundary.

### 2. Let it write

Let `framing-project` update `FRAMING.md` and decide whether `CONCEPTS.md` needs a change.

## Expected outputs (under `outputs/test-medium`)

- `FRAMING.md` updated in place: the "Our approach" section carries the refined wording; `last_updated` is bumped to today; every other section (Target problem, Who it's for, What success means, Tracks, Not working on) is byte-for-byte unchanged.
- `CONCEPTS.md` unchanged, because no term or boundary moved.

## Acceptance criteria

- Only the revisited section changed. All other sections are preserved verbatim.
- `last_updated` in the frontmatter advances.
- `CONCEPTS.md` is left untouched, since the revision moved no term or boundary.
- The document stays framing-project shape (frontmatter, locked section order), and the injected `<!-- goal: code -->` stamp is preserved.

## Fail conditions

- Any unrevisited section is reworded, reordered, or dropped (wholesale regeneration).
- `last_updated` is not advanced.
- `CONCEPTS.md` is churned despite no boundary moving.
- The goal stamp is lost, or the frontmatter shape is broken.

## Record

Emit the diff against the committed base as a named evidence artifact, from the repo root:

```
git diff --no-index outputs/test-medium.base outputs/test-medium > outputs/test-medium.md-2.diff
```

The diff must contain only `FRAMING.md` changes: the "Our approach" section and the `last_updated` line. `CONCEPTS.md` and every other section must be absent from the diff. If any other path appears, the no-churn rule failed. Keep `outputs/test-medium.md-2.diff` as the evidence artifact.

## Note

A companion variant worth running later moves a boundary on purpose (rename or re-scope a Track) and checks that `CONCEPTS.md` then updates in place, preserving existing terms. This test deliberately holds boundaries fixed to prove the no-churn half of the rule.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-07-15 |
| Status       | Draft      |
