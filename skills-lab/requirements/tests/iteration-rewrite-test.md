# Iteration re-pass test — MD-1, writing-requirements second pass

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this after `chain-test-medium.md`, in a session where the Medium+ outputs already exist.

## Purpose

Exercise the stateless iteration contract of `writing-requirements`: feed a prior requirements artifact back as substrate, with one requirement added, and confirm three things. Existing FR IDs stay pinned (ID stability), the new requirement takes the next available ID, and the version increments 0.1 to 0.2. The straight Medium+ run only produced a first pass, so none of this was tested.

## Directory and precedence

Directory: `testing/test-medium`, created by `chain-test-medium.md`, not by this test.

Precedence: run against a fresh Medium base. Empty `testing/test-medium`, run `chain-test-medium.md` into it, then run this test. The MD-* tests share this base, so each runs from a fresh chain-test-medium result rather than accumulating in one dir.

## Preconditions

- The base is present from a fresh `chain-test-medium.md` run: `testing/test-medium` holds `requirements/ingestion-pipeline/ingestion-pipeline-requirements.md` at Version 0.1, carrying the canonical base FR set, and `CONCEPTS.md`. Read the base for the actual FR list, do not assume a count. The current base is FR-001 to FR-005; every "FR-005 / FR-006" below is that instance, not a fixed number.
- Session cwd is `skills-lab/testing/test-medium`.

## Reset to the committed base (before acting)

MD-1 asserts ID and statement byte-stability across the re-pass, provable only against the pristine base. `chain-test-medium` commits the base in `test-medium`'s own repo (see its Record step); that commit, `<base-commit>`, is the diff reference. From inside `testing/test-medium`, reset to it before preparing the substrate:

```
git reset --hard <base-commit>
git clean -fd
```

`<base-commit>` is the base repo's HEAD after a fresh `chain-test-medium` run. This restores a deterministic base with no rebuild and no elicitation variance; the Record step diffs the re-pass output against it.

## Run steps

### 1. Prepare the iterated substrate

Copy `requirements/ingestion-pipeline/ingestion-pipeline-requirements.md` to `outputs/ingestion-pipeline/ingestion-pipeline-v2.md`. In the copy, under §Functional Requirements, leave every base FR exactly as it is and append one new, un-IDed requirement:

```markdown
**FR** — WHEN a `source delivery` has been read into `bronze`, the system SHALL retain it in its delivered form, so that ingestion is auditable.
```

The base's existing declared IDs are what Phase 2 must preserve; the appended requirement carries no ID, so it must be assigned the next available one after the base's highest.

### 2. Re-run the formaliser

Invoke `writing-requirements ingestion-pipeline from outputs/ingestion-pipeline/ingestion-pipeline-v2.md --type generic`.

Phase 0.7 reads the prior `ingestion-pipeline-requirements.md` (still 0.1) for ID stability and the version increment. Phase 2 scans the substrate for declared IDs.

## Expected outputs (under `testing/test-medium`)

- `requirements/ingestion-pipeline/ingestion-pipeline-requirements.md` overwritten to Version 0.2. Every base FR is unchanged in ID and statement; the appended requirement takes the next sequential ID after the base's highest (FR-006 for the current base) and is the retention requirement.
- `requirements/ingestion-pipeline/ingestion-pipeline-report.md` at Version 0.2.

## Acceptance criteria

- Every base FR keeps both its ID and its statement. No renumbering, no reordering.
- The appended requirement is assigned the next available ID after the base's highest (FR-006 for the current base), with no gap.
- The version increments 0.1 to 0.2 in both files.
- No undefined-term warnings. The new requirement reuses `source delivery` and `bronze`, both already in the glossary and `CONCEPTS.md`, so no new term is introduced.

## Fail conditions

- Any base FR (FR-001 to FR-005 for the current base) is renumbered, reordered, or has its statement altered.
- The appended requirement is dropped, or given a duplicate ID, or given an out-of-sequence ID (a gap).
- The version stays at 0.1, or resets.

## Record

Note the version chain (0.1 to 0.2) and the ID-to-content map after the re-pass. Then diff the re-pass output against the committed base, from inside `testing/test-medium`:

```
git diff <base-commit> -- requirements/ingestion-pipeline/ingestion-pipeline-requirements.md > ../test-medium.md-1.diff
```

Every base FR must appear in the diff as unchanged context; the only additions are the next-ID requirement (FR-006 for the current base) and the version bump. Confirm no base FR statement is on a changed line. Keep `testing/test-medium.md-1.diff` as the evidence artifact.

## Note

This is a single-skill iteration test. It is the foundation the loop tests (MD-3, MD-4) rest on: if the re-pass does not preserve IDs and bump the version, a loop failure downstream cannot be localised.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.3        |
| Last Updated | 2026-07-15 |
| Status       | Draft      |
