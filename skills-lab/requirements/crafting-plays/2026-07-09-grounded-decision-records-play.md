# Play: steering an open design question to a locked, source-grounded decision set

> A play reconstructed from a session. Replay it when you want to drive Claude from an open design question to a frozen, defensible set of decision records, not just an answer.
> ⚠️ Unverified. Provisional until validated against a second instance.

## When to trigger

You are facing an open design or architecture question that has no single right answer, and you want the reasoning captured in a durable, defensible form that outlives the chat. The value is in the decisions and why they were made, not in a one-off answer.

Examples:

- Choosing a platform architecture and its CI/CD approach from a blank page, where several patterns are viable and you will have to justify the choice later.
- Selecting between competing technical patterns (build tooling, environment model, layering) that other people will inherit.
- Turning a research question into a standard or a decision-record set that a team can review and adopt.

## Why it matters

An open design question usually gets a plausible first answer that nobody can later verify or defend. This play turns the question into a frozen set of one-decision records, each traceable to the source behind it, internally consistent after late changes, and paired with a living design doc for the build detail. It does that by steering the model through conversational clarification, repeated challenge against authoritative sources, and controlled freezing, rather than accepting the first pass.

## The play

### Optimal workflow

1. State the open question and ask for research against authoritative sources plus a proposed approach. Do not accept an answer from memory.
2. Clarify in conversation before committing. When the model offers premature multiple-choice, redirect to open discussion, and disclose your domain constraints one at a time as the shape emerges.
3. Ask the model to validate and expand your own framing, so it surfaces the hidden seams and the decisions you have not named yet, rather than just agreeing.
4. Run a challenge loop. Ask it to test the current proposal against your spec and the official docs, and to show what holds, what to add, and the remaining drifts. Repeat until it stabilises, and expect it to tell you when further rounds stop converging.
5. Freeze once the remaining drift is undecided choices, not errors. Say so explicitly, and have the full set of decisions restated in one place.
6. Pick the record format from existing house conventions, then validate that format against external standards and close the gaps before using it.
7. Generate the records, one decision each, with gated writes. Propose the name and destination, confirm, then write.
8. Enforce traceability. Number consistently, cite the specific source and section behind each decision, and forbid citing sources that were not actually used.
9. Fold in adjacent existing artifacts as records that reference their detail rather than duplicating it.
10. Propagate late changes. When a guiding principle shifts, revise the anchor record and every dependent, and update the index.
11. Commit by explicit path, keeping the set separate from unrelated working-tree changes.

### Critical moves

| Move | Why it is load-bearing |
|:-----|:-----------------------|
| Redirect premature multiple-choice into open clarification | Without it the model locks a wrong interpretation early and the whole set is built on it |
| Repeat the doc-grounded challenge loop to convergence | Without it the design is plausible but unverified and full of quiet drift |
| Freeze only when drift is choices, not errors | Freeze too early and you lock mistakes, too late and you never stop |
| Enforce source-per-decision and ban unused citations | Without it the records cannot be validated and carry false authority |
| Keep one decision per record, and split frozen decisions from the living design | Without it the records swell into a design doc that goes stale |
| Propagate a late principle change through the whole set | Without it the set contradicts itself |

### Pits to avoid

- Firing structured questions before the problem is understood. Open with conversation, not a form.
- Treating the first proposal as done. It usually takes several challenge rounds to settle.
- Not noticing non-convergence. If each round keeps surfacing new drifts that turn out to be optional features or your own additions rather than defects, name the two different yardsticks and stop.
- Citing sources that did not actually drive the decision. It manufactures confidence.
- Letting a summary artifact, such as the record template itself, go unchallenged against external standards.
- Stretching decision records into full build detail. Keep the how in a companion living doc.
- Agreeing to a late principle without checking it. Validate it against the sources first, because it may overturn earlier decisions.
- Committing unrelated changes with the set. Stage by explicit path.

## When to use it

- The question is genuinely open and consequential, and you will have to defend the choice.
- Authoritative external sources exist to ground the decisions.
- The output has to outlive the conversation and stand up to review by others.
- You hold domain constraints that will come out incrementally, not all at once.

## When not to use it

- The task is routine execution with a known answer.
- No authoritative source exists to ground the decisions, in which case it is opinion, and a discussion or an RFC fits better.
- The value is in a content deliverable, not a reusable decision record.
- You need a fast answer and the rigor is not warranted.

## Expected outcome

A numbered, frozen set of decision records, one decision each, every one traceable to the specific source behind it, with no record citing a source it did not use. The set is internally consistent after any late change, indexed with the relationships between records made explicit, and paired with a companion design doc that carries the build detail. Checkable: a reader can open any record and see why the choice was made, confirm each cited source was actually used, and find every record and its dependants from the index.

## Tradeoffs

Steering the collaboration:

| Decision | Pole A | Pole B | Chosen position |
|:---------|:-------|:-------|:----------------|
| Clarification mode | Structured multiple-choice up front | Open conversation throughout | Converse first, structure only once the shape is clear |
| Iteration depth | Accept the first proposal | Iterate without end | Challenge-loop until drift is choices not errors, then stop |
| Grounding | Trust the model's judgement | Demand a citation for everything | Cite the specific source per decision, and flag plainly where no source mandates the choice |

Shaping the artifact:

| Decision | Pole A | Pole B | Chosen position |
|:---------|:-------|:-------|:----------------|
| Record scope | One large design doc | One record per decision | One frozen record per decision, plus a living companion design doc |
| Template origin | Invent a format | Reuse the house convention as-is | Reuse the house template, validated against external standards, gaps closed |
| Late change | Append new records | Rewrite quietly in place | Rewrite the anchor, propagate to dependants, update the index |

---

| Field | Value |
|:------|:------|
| Version | 1.0 |
| Last Updated | 2026-07-09 |
| Status | Draft |
| Pairs with | ../../../desktop-chat/outputs/2606-o2-architecture-design/ADR-INDEX.md |
