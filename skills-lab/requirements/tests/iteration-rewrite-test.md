# Iteration re-pass test — MD-1, writing-requirements second pass

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this after `chain-test-medium.md`, in a session where the Medium+ outputs already exist.

## Purpose

Exercise the stateless iteration contract of `writing-requirements`: feed a prior requirements artifact back as substrate, with one requirement added, and confirm three things. Existing FR IDs stay pinned (ID stability), the new requirement takes the next available ID, and the version increments 0.1 to 0.2. The straight Medium+ run only produced a first pass, so none of this was tested.

## Directory and precedence

Directory: `outputs/test-medium`, created by `chain-test-medium.md`, not by this test.

Precedence: run against a fresh Medium base. Empty `outputs/test-medium`, run `chain-test-medium.md` into it, then run this test. The MD-* tests share this base, so each runs from a fresh chain-test-medium result rather than accumulating in one dir.

## Preconditions

- The base is present from a fresh `chain-test-medium.md` run: `outputs/test-medium` holds `requirements/ingestion-pipeline/ingestion-pipeline-requirements.md` at Version 0.1 (FR-001 to FR-005) and `CONCEPTS.md`.
- Session cwd is `skills-lab/outputs/test-medium`.

## Run steps

### 1. Prepare the iterated substrate

Copy `requirements/ingestion-pipeline/ingestion-pipeline-requirements.md` to `outputs/ingestion-pipeline/ingestion-pipeline-v2.md`. In the copy, under §Functional Requirements, leave FR-001 to FR-005 exactly as they are and append one new, un-IDed requirement:

```markdown
**FR** — WHEN a `source delivery` has been read into `bronze`, the system SHALL retain it in its delivered form, so that ingestion is auditable.
```

The existing declared IDs FR-001 to FR-005 are what Phase 2 must preserve; the appended requirement carries no ID, so it must be assigned the next available one.

### 2. Re-run the formaliser

Invoke `writing-requirements ingestion-pipeline from outputs/ingestion-pipeline/ingestion-pipeline-v2.md --type generic`.

Phase 0.7 reads the prior `ingestion-pipeline-requirements.md` (still 0.1) for ID stability and the version increment. Phase 2 scans the substrate for declared IDs.

## Expected outputs (under `outputs/test-medium`)

- `requirements/ingestion-pipeline/ingestion-pipeline-requirements.md` overwritten to Version 0.2, containing FR-001 to FR-006. FR-001 to FR-005 unchanged in ID and statement; FR-006 is the retention requirement.
- `requirements/ingestion-pipeline/ingestion-pipeline-report.md` at Version 0.2.

## Acceptance criteria

- FR-001 to FR-005 keep both their IDs and their statements. No renumbering, no reordering.
- The appended requirement is assigned FR-006, the next available ID in the FR sequence.
- The version increments 0.1 to 0.2 in both files.
- No undefined-term warnings. The new requirement reuses `source delivery` and `bronze`, both already in the glossary and `CONCEPTS.md`, so no new term is introduced.

## Fail conditions

- Any of FR-001 to FR-004 is renumbered, reordered, or has its statement altered.
- The appended requirement is dropped, or given a duplicate ID, or given an out-of-sequence ID (a gap).
- The version stays at 0.1, or resets.

## Record

Note the version chain (0.1 to 0.2) and the ID-to-content map after the re-pass. Confirm FR-006 is the only ID added and that the first five are byte-for-byte stable in their statements.

## Note

This is a single-skill iteration test. It is the foundation the loop tests (MD-3, MD-4) rest on: if the re-pass does not preserve IDs and bump the version, a loop failure downstream cannot be localised.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
