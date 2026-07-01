# Play: steering a business-process decomposition to a reusable artefact

> A play is a reusable recipe reconstructed from one session, generalised so it
> can be replayed when a similar situation recurs.
>
> ⚠️ Unverified. Treat as provisional until validated against a second instance.

## Advices

- Spend the first turn on gaps, not output. A loose decomposition prompt almost always hides the model choice, the scope boundary, the granularity, and the tie-break rule. Surface them before designing.
- Make the model restate the contract back to you before it executes. The reformulation is where boundary tensions show up cheaply, while they still cost one sentence to fix.
- Define the ambiguous term semantically rather than structurally. A one-line definition can close an open scoping question without touching the design.
- Decide reuse format before writing. If a downstream agent will consume the artefact, human-readable prose loses the decision provenance the agent needs.
- Keep the write and commit gates explicit. Approval per write, diffs on request, staging by named file.

---

## When to trigger

You have a coarse list of top-level items and you need each one broken into a single level of parts, with a hard constraint that the parts do not overlap and together cover the whole. The originating session decomposed seven mega-processes into sub-processes for a professional-services company, under a MECE constraint applied between the top-level items.

Concrete signals:

- "Decompose these mega-processes into sub-processes, output must be MECE."
- "Break this capability map into level-two capabilities, no overlaps."
- "Split these value streams into stages that collectively cover the whole."
- "Take this domain list and produce non-overlapping subdomains for each."

The shape is always the same: a given set at level N, a required decomposition to level N+1, and an exclusivity-plus-exhaustiveness constraint that has to hold at a named boundary.

## Why it matters

A decomposition prompt looks complete but rarely is. Left unchallenged it produces a plausible list that fails the MECE test at the seams, where one part could sit under two parents. The play front-loads the disambiguation, fixes the boundary at which MECE must hold, and names a tie-break rule so contested parts land in one place with a recorded reason. The deliverable is a decomposition that survives the exclusivity test and an artefact a downstream agent can extend without re-deriving the rules.

## The play

### Optimal workflow

1. Challenge the prompt for gaps before designing anything. Target the four that decide the shape: the model or archetype behind the set, the boundary at which MECE must hold, the depth of decomposition, and the arbitration rule for contested parts.
2. Take the answers, default the low-stakes gaps yourself, and reformulate the whole prompt back as an explicit contract. State the MECE boundary and the tie-break rule in that reformulation.
3. Execute the decomposition once the contract is confirmed. Flag each contested part inline where the arbitration rule was applied.
4. Resolve any residual scoping question by defining the ambiguous term rather than restructuring. Confirm whether the definition changes the design or only confirms it.
5. Choose the on-disk format for the consumer. If a downstream agent will read it, encode the rules and the arbitrations as data, not prose.
6. Write to the confirmed path, then run the write and commit gates: approve the write, show the staged diff on request, stage by named file, commit.

### Critical moves

| Move | Why it is load-bearing |
| :--- | :--- |
| Challenge gaps before designing | Without it the model designs against its own assumptions and the MECE boundary is set by accident. |
| Fix the MECE boundary explicitly | "MECE" is ambiguous between within-parent and between-parent. The whole test depends on which one holds. |
| Name an arbitration rule and flag its every use | A tie-break rule is what makes contested parts land in exactly one place, with the reason recoverable later. |
| Reformulate before executing | The restated contract is where boundary tensions surface while they are still cheap to correct. |
| Encode rules and arbitrations as data for reuse | Prose loses the provenance a downstream agent needs to extend the artefact without re-deriving the rules. |

### Pits to avoid

- Answering the prompt as written. The first version omitted the business model, the MECE boundary, the depth, and the tie-break rule, all of which change the output.
- Treating MECE as one thing. Within-parent and between-parent exclusivity are different constraints and pick different designs.
- Leaving a contested part unarbitrated. Time capture, cash handling, and contracting each had two plausible parents. Without a rule they end up in both or neither.
- Shipping the decomposition as prose when an agent is the reader. The arbitration flags degrade to text the consumer has to parse again.
- Writing before the path and the format are confirmed, or committing without the gate.

## When to use it

- The set to decompose is given and stable, and the task is one level down.
- Non-overlap and full coverage are a stated requirement, not a nice-to-have.
- The decomposition will be reused, extended, or consumed by another agent.
- Contested parts are foreseeable, so a tie-break rule earns its place.

## When not to use it

- The decomposition is a one-off thinking aid with no reuse and no hard MECE bar.
- The set itself is still in flux. Settle the level-N list first, then decompose.
- The domain has a standard reference taxonomy to adopt wholesale, where authoring a bespoke one adds nothing.
- Depth beyond one level is needed. This play stops at level N+1. Deeper trees need repeated application, not one pass.

## Expected outcome

| Check | Pass condition |
| :--- | :--- |
| Exclusivity | No part appears under two parents at the stated boundary. |
| Exhaustiveness | The parts of each parent cover it with no acknowledged gap. |
| Arbitration recorded | Every contested part carries the parent chosen, the parent rejected, and the reason. |
| Machine-reusable | A downstream agent can add a part and check it against the recorded invariants without re-deriving them. |
| Provenance intact | The model, the boundary, the depth, and the tie-break rule are stated in the artefact. |

## Tradeoffs

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| MECE boundary | Within each parent | Between parents | Between parents, because that is where the decomposition fails first. |
| Elicitation depth | Ask every open question | Assume and proceed | Ask the four that change the shape, default the rest back to the model. |
| Ambiguity resolution | Restructure the design | Define the term | Define the term. A one-line semantic fix beat a structural change. |
| On-disk format | Human-readable prose | Machine-parseable data | Data, because the stated consumer was a downstream agent. |
| Arbitration visibility | Silent tie-break | Flagged on every use | Flagged, so the reason is recoverable at reuse. |
| Write control | Autonomous write | Gate per write | Gate per write, with diffs on request and staging by named file. |

---

| Field        | Value                                   |
| :----------- | :-------------------------------------- |
| Version      | 1.0                                     |
| Last Updated | 2026-07-01                              |
| Status       | Draft                                   |
| Pairs with   | desktop-chat/outputs/2607-o2-requirements/process-taxonomy.yaml |

<!--
Version: 1.0 | Last Updated: 2026-07-01 | Status: Draft
-->
