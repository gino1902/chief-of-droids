# Small-to-Medium upgrade test — SM-1

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this in a fresh Claude Code session, separate from the other tests.

## Purpose

Exercise the mitigation the chain design names for a Small project entering the requirements chain: run `framing-project` on it to seed `CONCEPTS.md` and Tracks, converting it to the Medium+ shape before elicitation continues. The test runs the Small chain to a first slice, then upgrades, then re-runs the chain, and checks that the upgrade governs the vocabulary. It is the integration capstone.

## Directory and precedence

Directory: `testing/test-upgrade`, created by this test (self-contained, it bootstraps its own Small base).

Precedence: run after MD-1, MD-3, and MD-4 are green, so a failure localises to the upgrade rather than to a mechanism underneath it. No shared base, this test builds and upgrades its own.

## Preconditions

- A fresh session.
- The directory `skills-lab/testing/test-upgrade` exists and is empty. Session cwd is that directory.

## Scripted subject — "sensordrop"

A solo utility that files incoming sensor CSV drops into a tidy local store. Genuinely Small: solo, one workflow, no sponsor.

## Run steps

### 1. bootstrapping-project (Small)

Invoke `bootstrapping-project`. Goal `code`. Pass 2 size: Small (inline five-question framing). Sub-type: data. Answer:

- Why: sensor CSV drops pile up unsorted in a downloads folder, so I lose which reading came from which sensor.
- For whom: me, solo.
- Success: every drop lands filed by sensor and date, for a month, with none misfiled.
- Delivered: a small Python CLI with a local file store.
- Constraints: local only; one machine.

Approve the tree and the CLAUDE.md.

Confirm the Small branch fired: `FRAMING.md` is the five-question shape (goal stamp on line one, no `last_updated` frontmatter), there is no `CONCEPTS.md`, and there are no Tracks.

### 2. brainstorming (Small base, first pass)

Invoke `brainstorming-requirements from FRAMING.md --target "filing"`. There is no `CONCEPTS.md`, so it proceeds and records the terms it settles. Elicit a "file a drop" component slice using the domain terms `drop`, `sensor`, `reading`, and `store`. Emit the slice.

### 3. writing-requirements (first pass) — record vocabulary noise

Run `writing-requirements filing from <slice-path> --type generic`. Record the report: the count of any undefined-term warnings and the Outstanding line. A no-`CONCEPTS.md` base is where the design expects vocabulary noise, but the actual count depends on how fully the slice governed its own terms, so record it rather than asserting it.

### 4. framing-project (the upgrade)

Invoke `framing-project`. It finds an existing `FRAMING.md` (the five-question Small doc) and runs its update path. Use it to add Tracks and seed a context-structured `CONCEPTS.md` capturing the terms already settled (`drop`, `sensor`, `reading`, `store`). Record whether it consumes the five-question doc cleanly or needs reconciliation, since the Small doc lacks the frontmatter framing-project normally writes. This is itself a finding about the upgrade path.

### 5. brainstorming (re-run on the Medium+ base)

Re-invoke `brainstorming-requirements from FRAMING.md --target "filing"`. The terms are now governed by the seeded `CONCEPTS.md`, so it should draw them from there.

### 6. writing-requirements (re-pass)

Re-run `writing-requirements filing from <slice-path> --type generic`. The undefined-term warnings from step 3 should be cleared, and the version should increment.

## Expected outputs (under `testing/test-upgrade`)

- Small bootstrap artifacts: five-question `FRAMING.md`, `CLAUDE.md`, a tree anchor, `CONVENTIONS.md` (data contract, `zoned: none`), and no `CONCEPTS.md` initially.
- After the upgrade: `FRAMING.md` in framing-project shape (frontmatter with `last_updated`, Tracks) and a context-structured `CONCEPTS.md`. `CONVENTIONS.md` is untouched by the upgrade — the framing shift adds domain language, it does not change the structural contract.
- the `filing` slice (pre- and post-upgrade) and `requirements/filing/filing-requirements.md` plus `-report.md` (0.1 then 0.2).

## Acceptance criteria

- The Small bootstrap produces no `CONCEPTS.md` and no Tracks, but does produce `CONVENTIONS.md` (the structural contract is written regardless of size). The Small branch fired.
- The upgrade produces a context-structured `CONCEPTS.md` and Tracks, converting the project to the Medium+ shape, and leaves `CONVENTIONS.md` unchanged.
- The post-upgrade `writing-requirements` re-pass carries no undefined-term warnings, or strictly fewer than the pre-upgrade pass, demonstrating the mitigation.
- The version increments across the re-write.

## Fail conditions

- `framing-project` cannot consume the five-question Small `FRAMING.md` at all (the upgrade path is broken).
- The post-upgrade requirements still carry undefined-term warnings for terms now defined in `CONCEPTS.md`.
- `CONCEPTS.md` after the upgrade is not context-structured.

## Record

The undefined-term warning count before versus after the upgrade. Note whether the framing-project conversion of a five-question FRAMING was clean or needed reconciliation, which is a chain-level finding worth carrying forward.

## Note

This is the integration capstone. Because it exercises bootstrapping, framing-project, brainstorming, and writing-requirements in sequence, it is only diagnostic once each of those is individually proven, hence its late position in the priority order.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
