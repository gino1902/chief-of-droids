# Domain-language reuse test — MD-3, CONCEPTS write-back and reuse

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this after `chain-test-medium.md`, in a session where the Medium+ outputs already exist.

## Purpose

Exercise the ubiquitous-language loop. A second component, from a different Track, drawn on the same `CONCEPTS.md`, must reuse existing terms verbatim rather than mint synonyms, and record genuinely new terms back under the owning context. This guards the domain-driven-design no-drift property, where two components would otherwise name the same thing differently. It is also the closest safe probe of multi-component behaviour without the fan-out the chain design defers.

Scope: this row proves the loop at the brainstorm and `CONCEPTS.md` layer only and does not run `writing-requirements`. The CONCEPTS-to-spec leg, that a governed term reaches the formalised spec, is covered by `chain-test-medium.md` and `technical-formalisation-test.md`, which assert no undefined-term warnings with terms tracing to `CONCEPTS.md`.

## Directory and precedence

Directory: `outputs/test-medium`, created by `chain-test-medium.md`, not by this test.

Precedence: run against a fresh Medium base. Empty `outputs/test-medium`, run `chain-test-medium.md` into it, then run this test.

## Preconditions

- The base is present from a fresh `chain-test-medium.md` run: `outputs/test-medium` holds `FRAMING.md` (three Tracks), a context-structured `CONCEPTS.md` (the Ingestion and transformation context carries `landing zone` and `quality rules`; the Exposition and reporting context carries `cross-team report`), and the ingestion-pipeline slice.
- Session cwd is `skills-lab/outputs/test-medium`.

## Reset to the committed base (before acting)

The write-back edits `CONCEPTS.md` in place, and the no-drift claim is that existing terms are preserved while only the new one is added. That is provable only against the pristine base. `chain-test-medium` commits the base in `test-medium`'s own repo (see its Record step); that commit, `<base-commit>`, is the diff reference. From inside `outputs/test-medium`, reset to it before brainstorming:

```
git reset --hard <base-commit>
git clean -fd
```

`<base-commit>` is the base repo's HEAD after a fresh `chain-test-medium` run. This restores a deterministic base with no rebuild and no elicitation variance; the Record step diffs the working tree against it.

## Run steps

### 1. Brainstorm a second component (different Track)

Invoke `brainstorming-requirements from FRAMING.md --target "report builder"`, a component of the Exposition and reporting track. Phase 0 should read `CONCEPTS.md` and draw terms from it.

Answer the interview as scripted:

- Purpose: the report builder assembles `cross-team report` outputs for analysts from `gold`, so an analyst pulls a report without hand-reconciliation.
- Scope: covers selecting `gold` datasets and assembling them into a `cross-team report` on request, and holding a report definition that names which datasets a report pulls. Out of scope: producing `gold` (owned by the Ingestion and transformation track); governing what may be exposed (owned by the Governance and platform track).
- Actors and consumers: upstream, `gold` produced by the ingestion pipeline. Downstream, the analyst who reads the report.
- Requirements: elicit three to four, reusing `gold` and `cross-team report` verbatim from `CONCEPTS.md`. Introduce exactly one genuinely new term, `report definition`, and record it back to `CONCEPTS.md` under the Exposition and reporting context.

Let it emit the slice and update `CONCEPTS.md`.

## Expected outputs (under `outputs/test-medium`)

- a slice at `outputs/report-builder/report-builder.md`, using `gold` and `cross-team report` verbatim (backticked), with no synonyms.
- `CONCEPTS.md` updated in place: `report definition` added under the Exposition and reporting context block; every existing term preserved; no duplicated or forked context blocks.

## Acceptance criteria

- The slice reuses `gold` and `cross-team report` exactly as named in `CONCEPTS.md`, not paraphrased (no "consolidated report", no "trusted dataset", and so on).
- The one new term, `report definition`, is written back to `CONCEPTS.md` under the correct context, not left defined only inside the slice.
- `CONCEPTS.md` stays context-structured: a shared core, one block per Track, and a context map. It is not flattened or duplicated.

## Fail conditions

- A synonym is minted for a term that `CONCEPTS.md` already names (vocabulary drift).
- The new term is defined only in the slice and never recorded back to `CONCEPTS.md`.
- brainstorming ignores `CONCEPTS.md` and re-invents terms it should have drawn.

## Record

List the terms reused verbatim and the term(s) written back, with the context each landed in. Then emit the diff against the committed base as evidence, from inside `outputs/test-medium`:

```
git diff <base-commit> > ../test-medium.md-3.diff
```

Read the diff as the pass check. The only changes allowed are additive: the new `report-builder/` slice, and a `CONCEPTS.md` addition of `report definition` under the Exposition and reporting context. Every existing `CONCEPTS.md` term must be unchanged in the diff (no rename, no re-definition), no requirements file may appear, and `FRAMING.md` must be absent. Keep `outputs/test-medium.md-3.diff` as the evidence artifact.

## Note

brainstorming handles one component per run, so this is a manual second run against a shared `CONCEPTS.md`, not the auto-fan-out the design defers. It tests the write-back and reuse loop, not multi-component orchestration.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.3        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
