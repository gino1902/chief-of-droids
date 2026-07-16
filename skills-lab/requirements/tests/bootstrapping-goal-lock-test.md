# Bootstrapping goal-lock test — XC-2

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this in a fresh session. It diversifies project type: this is the only thinking-goal scenario, so it exercises the thinking tree and CLAUDE.md skeleton.

## Purpose

Confirm the goal-lock invariant of `bootstrapping-project`. Once a goal is stamped in `FRAMING.md`, re-invoking with a conflicting goal argument must stop and report the conflict, making no changes. The goal is decided once and read from the stamp by every later pass.

## Directory and precedence

Directory: `outputs/test-goal-lock`, created by this test.

Precedence: self-contained. Bootstrap a thinking project, then re-invoke with a conflicting goal argument.

## Preconditions

- A fresh session.
- The directory `skills-lab/outputs/test-goal-lock` exists and is empty. Session cwd is that directory.

## Scripted subject — "arch-notes"

A Small thinking project: a personal decision log for architecture choices. Solo, no sponsor. Goal `thinking`.

## Run steps

### 1. Bootstrap a thinking project

Invoke `bootstrapping-project`. Goal `thinking`. Pass 2 size: Small (inline five-question framing).

- Why: I make architecture calls in chat and lose the reasoning, so I re-litigate the same decisions.
- For whom: me, and whoever inherits the system later.
- Success: every non-trivial decision has an ADR, for a quarter, and none is silently reversed.
- Delivered: a set of ADRs and working notes.
- Constraints: decisions are append-only; accepted ADRs are superseded, never edited.

Let it write `FRAMING.md` with `<!-- goal: thinking -->` on line one, scaffold the thinking tree (`decisions/`, `notes/`, `diagrams/`, `references/`), write `CONVENTIONS.md` (the thinking contract: record, naming, promotion rules, with a stanza of `config: none`, `runner: review`, `zoned: none` — review is the gate, no lint config generated), and write the thinking `CLAUDE.md` pointing at `CONVENTIONS.md`.

### 2. Re-invoke with a conflicting goal

Re-invoke `bootstrapping-project code` (the argument asserts `code`, the stamp says `thinking`).

Expected: the Preamble reads the goal from the stamp, sees the argument conflicts, stops, and reports the conflict. It makes no changes.

## Expected outputs (under `outputs/test-goal-lock`)

- The thinking project from step 1: `FRAMING.md` (five-question, `<!-- goal: thinking -->`), the thinking tree anchor, `CONVENTIONS.md` (thinking contract, no lint config since review is the gate), `CLAUDE.md` on the thinking skeleton, `.claude/settings.json`.
- Nothing new or changed from step 2.

## Acceptance criteria

- Step 1 produces a thinking project: the thinking tree (`decisions/`, `notes/`, `diagrams/`, `references/`), a `CONVENTIONS.md` carrying the thinking contract with `config: none`/`runner: review`/`zoned: none` (no lint config generated), and a thinking `CLAUDE.md` (challenge ideas, minimal-intervention edits, ADR discipline) pointing at `CONVENTIONS.md`.
- Step 2 stops and reports the goal conflict (stamp `thinking` versus argument `code`) and mutates nothing — `CONVENTIONS.md` included.

## Fail conditions

- Step 2 proceeds, adopts the argument goal, or mutates any artifact.
- Step 1 scaffolds a code or infra tree instead of the thinking tree.
- `CONVENTIONS.md` is missing from step 1, or a lint config was generated for the thinking goal (review is its only gate).
- The goal stamp is absent or altered.

## Record

Confirm step 2 halted with a conflict report, and that no file changed between step 1's end state and step 2's end state.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
