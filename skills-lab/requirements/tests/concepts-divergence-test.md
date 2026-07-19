# Domain-language divergence test — MD-7

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this after a fresh `chain-test-medium.md`, in a session at the Medium base.

## Purpose

Exercise the untested half of the domain-language design: a single word that legitimately means different things in two contexts. The chain design structures `CONCEPTS.md` by context precisely because "the same word can mean different things in two contexts", and the context map exists to record "where the same word diverges". MD-3 tests only the same-meaning case (reuse a term verbatim, no drift). This tests divergence: the word is recorded under both owning contexts with distinct definitions, and the context map carries a divergence row, rather than one meaning overwriting the other, a synonym being minted to dodge the clash, or the term being flattened into the shared core.

Scope: this row proves divergence at the `CONCEPTS.md` layer only and does not run `writing-requirements`. Because the formaliser reads a single slice and never sees the context map, it cannot exercise divergence at all. The divergence-to-spec leg, distinct senses enforced across components in the formalised output, is the deferred recomposition check (the context map as a runtime check), not this row.

## Directory and precedence

Directory: `testing/test-medium`, created by `chain-test-medium.md`, not by this test.

Precedence: run against a fresh Medium base. Empty `testing/test-medium`, run `chain-test-medium.md` into it, then run this test.

## Preconditions

- The base is present from a fresh `chain-test-medium.md` run: `testing/test-medium` holds `FRAMING.md` (three Tracks: Ingestion and transformation, Governance and platform, Exposition and reporting) and a context-structured `CONCEPTS.md`.
- Session cwd is `skills-lab/testing/test-medium`.

## Reset to the committed base (before acting)

The critical claim is that run 2 adds the Exposition meaning of `owner` without overwriting run 1's Governance meaning, a preservation property provable only against the pristine base. `chain-test-medium` commits the base in `test-medium`'s own repo (see its Record step); that commit, `<base-commit>`, is the diff reference. From inside `testing/test-medium`, reset to it before the first brainstorm:

```
git reset --hard <base-commit>
git clean -fd
```

`<base-commit>` is the base repo's HEAD after a fresh `chain-test-medium` run. This restores a deterministic base with no rebuild and no elicitation variance; the Record step diffs the working tree against it.

## Run steps

The divergent term is `owner`. In the Governance context it means the data steward accountable for a dataset. In the Exposition context it means the analyst accountable for a report. Same word, two meanings, two contexts.

### 1. Brainstorm a Governance component that introduces `owner`

Invoke `brainstorming-requirements from FRAMING.md --target "steward assignment"`, a component of the Governance and platform track. Draw terms from `CONCEPTS.md`.

- Purpose: steward assignment records who is accountable for each `catalog` dataset.
- Scope: covers assigning an `owner` (the accountable data steward) to a `catalog` dataset. Out of scope: producing the data (Ingestion track); exposing it (Exposition track).
- Requirements: at least one using `owner` meaning the data steward accountable for a `catalog` dataset.

Record `owner` back to `CONCEPTS.md` under the Governance and platform context.

### 2. Brainstorm an Exposition component that reuses the word with a different meaning

Invoke `brainstorming-requirements from FRAMING.md --target "report ownership"`, a component of the Exposition and reporting track.

- Purpose: report ownership records which analyst is accountable for each `cross-team report`.
- Scope: covers assigning an `owner` (the accountable analyst) to a `cross-team report`. Out of scope: producing `gold` (Ingestion track); stewarding datasets (Governance track).
- Requirements: at least one using `owner` meaning the analyst accountable for a `cross-team report`.

Here the skill must recognise that `owner` already exists in another context with a different meaning, and handle the divergence rather than collide.

## Expected outputs (under `testing/test-medium`)

- two slices: `outputs/steward-assignment/steward-assignment.md` and `outputs/report-ownership/report-ownership.md`.
- `CONCEPTS.md` updated so `owner` appears under both the Governance and platform context (data steward) and the Exposition and reporting context (report analyst), each with its own definition, and the context map carries a row recording that `owner` diverges between the two.

## Acceptance criteria

- `owner` is defined under both context blocks, with two distinct definitions that match the two meanings.
- The context map has a divergence row for `owner` (Governance meaning versus Exposition meaning).
- The Governance meaning from run 1 is preserved intact when run 2 adds the Exposition meaning. Neither overwrites the other.
- No synonym is minted to avoid the clash (no `report-owner` or `steward` substituted where `owner` was the elicited word).
- `owner` is not placed in the shared core, since it does not mean one thing everywhere.
- No extra artifacts: each brainstorm run writes only its slice and the `CONCEPTS.md` update. Neither run writes a requirements file, and neither modifies `FRAMING.md`.

## Fail conditions

- Run 2 overwrites the Governance meaning of `owner`, or run 1's entry disappears.
- A synonym is minted to dodge the divergence instead of recording two meanings.
- `owner` is flattened into the shared core.
- The context map has no divergence row for `owner`.
- Either run emits a stray artifact (a requirements file, or an edit to `FRAMING.md`).

## Record

Show the two `owner` definitions and the context-map divergence row. Then emit the diff against the committed base as evidence, from inside `testing/test-medium`:

```
git diff <base-commit> > ../test-medium.md-7.diff
```

Read the diff as the pass check. The only changes allowed are additive: the two new slices (`steward-assignment/`, `report-ownership/`), and `CONCEPTS.md` gaining `owner` under both the Governance and Exposition contexts plus a context-map divergence row. The Governance `owner` entry added by run 1 must still be present after run 2 (no deletion or overwrite in the final `CONCEPTS.md`), no synonym may appear, no requirements file may appear, and `FRAMING.md` must be absent from the diff. Keep `testing/test-medium.md-7.diff` as the evidence artifact.

## Note

This validates the central reason `CONCEPTS.md` is context-structured rather than a flat glossary. It is also groundwork for the deferred recomposition and consistency checks, which run against exactly these context-map divergence rows.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.3        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
