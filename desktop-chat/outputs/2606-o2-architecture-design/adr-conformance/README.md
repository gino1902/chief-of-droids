# ADR conformance suite

Tests whether the decision records in [`../decisions/`](../decisions/) are complete, consistent
and unambiguous enough that the same situation yields the same design twice.

It tests the **records**, not the platform. A failing case is a defect in an ADR, not in code.

---

## Why the substrate is isolated

The derivation reads a directory. If that directory also held design documents, the artefact
skeleton and a task tracker, variance between runs would come from what each run happened to read
rather than from the records. `../decisions/` therefore contains decision records and the index,
nothing else.

This suite sits outside it for the same reason. Anything placed inside `../decisions/` becomes
part of the substrate and would be ingested as if it were a decision.

---

## The four verdicts

| Verdict | Meaning | Remedy |
|:--------|:--------|:-------|
| **Determined** | The records yield exactly one design, and every element traces to a named record and section | None, the case passes |
| **Underspecified** | A record answers, but loosely enough that two competent readers would design it differently | Tighten wording in place |
| **Conflict** | Two records answer, and differently | Reconcile, and record which one owns the question |
| **Gap** | No record answers | Write a record, name it a convention, or log it as accepted |

A case passes only on **Determined**. Anything else is a finding with an owner.

---

## Three instruments, because the verdicts are not detected the same way

**Gap** and **Conflict** are properties of the text. One careful derivation finds them, by
requiring a citation for every element of the design. An element with no citation is a gap; two
records cited for the same element with different values is a conflict.

**Determined** against **Underspecified** cannot be seen in one pass. A single reader always
produces one design and it always feels determined. Predictability is a property of the
distribution of readings, so it needs more than one sample: N independent derivations, compared.

Order matters and saves money. Grade gap, then conflict, then variance. Only cases clean on the
first two are worth spending N runs on.

---

## Running it repeatably

- **Pin the substrate.** Record the git SHA of `../decisions/` before any run. Without it, "same
  substrate, same output" is not a claim that can be checked.
- **Fixed prompt, stored not typed.** The runner reads it from the case. Hand-editing between runs
  invalidates the comparison.
- **Structured output.** The derivation returns a fixed field set, each field with its citation.
  Free prose cannot be compared mechanically.
- **Independent runs.** Fresh process per run, given only the substrate path and one case. No
  shared context and no sight of prior derivations, or runs converge for the wrong reason.
- **Record the model and date.** Output varies by model, so a result means nothing without one.
- **Compare per element, not per document.** Agreement is the fraction of design elements
  identical across runs. Two derivations can differ in wording and agree entirely in substance.
- **Store results in `runs/`**, which is git-ignored. A run is reproducible from the cases plus
  the SHA. What survives is the finding, not the transcript.
- **Freeze on pass.** Once a case is Determined and the derived design is confirmed as the one
  wanted, that design becomes expected output and the case converts from discovery to regression.
- **Re-run trigger is any change to a record.** A moved design is then either an intended
  consequence or a break.

---

## Two rules that make the results mean anything

**Attribution.** Every element of a design cites the record and section it came from. An element
with no citation is a gap wearing a design's clothes. That is precisely how a bundle-per-producer
assumption survived unexamined for a month.

**Coverage.** Every record is exercised by at least one case, and every case exercises at least
one record. A record with no case is untested. ADR-004 is expected to have none, and that is
recorded rather than hidden.

---

## Two limitations, stated so nobody over-reads a result

Agreement across N runs of the same model is **not correctness**. Models share biases and can
agree on the same misreading. High agreement means the records are unambiguous, not that they are
right.

So the loop stays human. The derivation is mechanical; whether the derived design is the one
actually wanted is a ruling. Where those two differ, the finding is a defect in the records, and
that divergence is the most valuable output this suite produces.

The runner never proposes a design and never edits a record. Otherwise the instrument grades its
own output.

---

## Layout

```
adr-conformance/
├── README.md     this file, the method
├── cases.md      the case set
└── runs/         results, git-ignored
```

### Why one file rather than one per case

The argument for one file per case is that a run writes results back, giving per-case history and
avoiding collisions. That argument mostly evaporates against the method above: run output goes to
`runs/`, which is git-ignored, so the tracked case changes only when a design is frozen on pass.
That happens roughly once per case, ever. A handful of rare edits to one file is not a collision
problem.

What one file buys is real. The shared vocabulary, producer, route and vehicle, union against
join, and the five design elements, is stated once rather than nine times. Cross-references read
as sentences instead of links. And the coverage table only means anything with the whole set in
view, which is where the sharpest finding already is: ADR-002 and ADR-003 have no case at all, and
that is visible only because they can be seen together.

Both reversals are cheap, which is what makes this low stakes. Splitting is mechanical, since the
cases are already delimited by headers.

**Split when a case starts accumulating its own history: repeated freezes, a superseded expected
design, or a run cadence frequent enough that per-case diffs matter. Also split if the set
outgrows a single readable pass, which nine does not and twenty-five would.**
