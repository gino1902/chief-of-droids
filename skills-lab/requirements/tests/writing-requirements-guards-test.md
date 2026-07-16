# Writing-requirements guards test — XC-1

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this in a fresh session. Negative-path sweep for `writing-requirements` Phase 0.

## Purpose

Confirm the Phase 0 hard-fail guards fire and write nothing. The straight tests only hit the happy path, so the argument and substrate validation was never exercised. Each sub-case below must halt with the hard-fail block (correct phase and reason) and leave no output files.

## Directory and precedence

Directory: `outputs/test-wr-guards`, created by this test.

Precedence: none. Independent of every other scenario.

## Preconditions

- A fresh session.
- The directory `skills-lab/outputs/test-wr-guards` exists and is empty. Session cwd is that directory.
- Create two fixtures in it: a valid `spec.md` (any small requirement-shaped markdown, one backticked term and one `The system shall …` line is enough) and a `spec.txt` with the same content but the wrong extension.

## Run steps

Run each invocation and record the outcome. Each must hard-fail at the stated Phase 0 step.

1. Reserved token in slug: `writing-requirements payment-requirements from spec.md --type generic` → hard-fail, slug contains the reserved token `requirements`.
2. Invalid slug characters: `writing-requirements user_auth from spec.md --type generic` → hard-fail, slug does not match `^[a-z0-9-]+$` (underscore).
3. Missing `--type`: `writing-requirements user-auth from spec.md` → hard-fail, `--type` absent.
4. Unrecognised `--type`: `writing-requirements user-auth from spec.md --type full` → hard-fail, `--type` not `generic` or `technical`.
5. Substrate not found: `writing-requirements user-auth from missing.md --type generic` → hard-fail, path not found.
6. Non-markdown substrate: `writing-requirements user-auth from spec.txt --type generic` → hard-fail, substrate is not `.md`.

## Expected outputs (under `outputs/test-wr-guards`)

- The two fixtures only. No directory is created by any sub-case. Sub-cases 1 to 5 halt at Phase 0.2 to 0.4, before the output dir is resolved. Sub-case 6 passes the path check, resolves the root at Phase 0.5, and reaches the Phase 0.8 substrate check, where it hard-fails. Phase 0.6 does not itself `mkdir` (the skill uses Read and Write tools only, so the output dir is created implicitly only when Phase 6 writes a file), and Phase 6 is never reached. So no `requirements/user-auth/` dir, and no `*-requirements.md` or `*-report.md`, is written by any sub-case.

## Acceptance criteria

- Every sub-case halts with the hard-fail block, citing the correct phase step and a matching reason and remediation.
- No output file is written by any sub-case (validation halts before Phase 6).
- Sub-cases 1 to 5 halt before repo-root resolution. Sub-case 6 halts at the Phase 0.8 substrate check after root resolution, which now always succeeds by anchoring at cwd. Phase 0.5 no longer walks upward, and since `test-wr-guards` carries no `CLAUDE.md` a no-`CLAUDE.md` warning is streamed, but nothing is written because the run hard-fails at 0.8.

## Fail conditions

- Any invocation proceeds past Phase 0 and writes a file.
- A hard-fail cites the wrong phase or reason.
- The reserved-token or invalid-slug case is silently accepted.

## Record

For each sub-case, note the phase cited and confirm nothing was written. One line per sub-case is enough.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
