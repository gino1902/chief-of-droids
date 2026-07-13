# Warnings-to-refinement loop test — MD-4

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this after `chain-test-medium.md`, in a session where the Medium+ outputs already exist.

## Purpose

Exercise the downstream-to-upstream feedback loop, the second dotted arrow in the chain design. A first slice deliberately leaves one requirement without a measurable predicate. `writing-requirements` flags it as having no derivable acceptance criterion. That warning drives a `brainstorming-requirements` refinement that adds a predicate, and the re-write clears the warning. This tests the elicit-then-write seam under correction rather than on a clean first pass.

## Directory and precedence

Directory: `outputs/test-medium`, created by `chain-test-medium.md`, not by this test.

Precedence: run against a fresh Medium base (empty `outputs/test-medium`, run `chain-test-medium.md` into it, then run this test), and only after MD-1 (`iteration-rewrite-test.md`) is green, so a failure here points at the loop, not at the re-pass underneath it.

## Preconditions

- The base is present from a fresh `chain-test-medium.md` run: `outputs/test-medium` holds `FRAMING.md` and a context-structured `CONCEPTS.md`.
- Session cwd is `skills-lab/outputs/test-medium`.

## Run steps

### 1. Brainstorm a deliberately weak first slice

Invoke `brainstorming-requirements from FRAMING.md --target "delivery intake"`, an Ingestion and transformation component. Draw terms from `CONCEPTS.md`.

Answer as scripted, with one measurable requirement and one deliberately vague one:

- Purpose: delivery intake reads `landing zone` deliveries into `bronze` on arrival.
- Scope: covers detecting a new `source delivery` in the `landing zone` and reading it into `bronze`, and processing it in good time. Out of scope: transformation to `silver` and `gold` (owned by the ingestion pipeline).
- Actors and consumers: upstream, the `landing zone`. Downstream, `bronze`.
- Requirements:
  - R-01: The system shall read a `source delivery` into `bronze`, when it lands in the `landing zone`. (measurable trigger)
  - R-02: The system shall process each `source delivery` promptly, when a delivery lands. (deliberately vague, "promptly" carries no measurable predicate)

Emit the slice at `outputs/delivery-intake/delivery-intake.md`.

### 2. Formalise, and let the gap surface

Run `writing-requirements delivery-intake from outputs/delivery-intake/delivery-intake.md --type generic`.

Expected: the FR derived from R-02 renders `AC: N/A — no verifiable condition derivable from substrate`, with a `[WARNING-UNRESOLVED]` no-derivable-AC finding. Record the §Summary and the phase Outstanding line.

### 3. Refine, closing the loop

Feed the warning back into elicitation. Re-run the `delivery-intake` brainstorm, tightening R-02's conditions clause to a measurable predicate, for example `within 30 minutes of the delivery landing`. Update the slice in place.

### 4. Re-formalise

Re-run `writing-requirements delivery-intake from outputs/delivery-intake/delivery-intake.md --type generic`.

Expected: the R-02 FR now yields a derivable AC (a 30-minute threshold), the no-derivable-AC warning is gone, and the version increments 0.1 to 0.2.

## Expected outputs (under `outputs/test-medium`)

- a slice at `outputs/delivery-intake/delivery-intake.md`, v1 then refined.
- `requirements/delivery-intake/delivery-intake-requirements.md` and `-report.md`, at 0.1 (pass one) then 0.2 (pass two).

## Acceptance criteria

- Pass one flags the vague requirement with a no-derivable-AC warning.
- After the refinement supplies a measurable predicate, pass two derives an acceptance criterion for it and the warning is cleared.
- The version increments across the re-pass, and R-01 keeps its ID.

## Fail conditions

- Pass one does not flag the vague requirement (the verification step missed a requirement with no measurable predicate).
- Pass two still warns despite a measurable predicate now being present (the loop did not close).
- The refinement silently rewrote other requirements rather than only tightening R-02.

## Record

Quote the Outstanding line before and after. Show R-02's conditions clause in v1 versus v2, and its acceptance criterion before (N/A) and after (the derived threshold). The count will also carry the auto-derived glossary entries as `WARNING-UNRESOLVED` (verification-pending) in both passes; those are normal after the `conventions.md` resolution-model fix. Track the no-derivable-AC warning specifically, which is the one that must clear between passes.

## Note

This is the correction loop the chain design draws as "warnings feed refinement". It depends on MD-1's re-pass working, which is why MD-1 is sequenced ahead of it.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
