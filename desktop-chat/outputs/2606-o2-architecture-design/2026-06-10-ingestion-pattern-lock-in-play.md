# Play: ingestion pattern lock-in against deployment context

> A play is a reusable recipe reconstructed from a session. This one captures how
> a pre-enumerated, option-agnostic ingestion design was collapsed into a single
> context-specific verdict.

## When to trigger

You hold a design doc that lays out several candidate patterns option-agnostically (each with abstract benefit and tradeoff), and a concrete deployment context then arrives that should select among them. The trigger is the arrival of the context, not the writing of the catalogue. The catalogue is the input, the verdict is the output.

Concrete examples:

- "The extractor is already running, everything downstream is greenfield, we will stand up a new Databricks workspace on the latest runtime. Pick the ingestion option." (The originating session.)
- "Here is our medallion-options doc and our actual team size and cloud posture. Which layer model do we commit to?"
- "We enumerated three CDC approaches in the design. Given we are on SQL Server with Unity Catalog already in place, which one?"

## Why it matters

It converts an option-agnostic catalogue into a defensible, context-specific verdict without re-deriving the catalogue. The deliverable is a per-option table re-scored against the actual context, a single recommendation, and the one variable that would change it. The problem it solves is convergence: a generic comparison never selects on its own, because a tradeoff is only a cost when the context makes it bite.

## The play

### Optimal workflow

1. Take the option-agnostic comparison as the input. If one does not exist, this is design-from-scratch, not lock-in, so stop and run the design workflow instead.
2. Verify the comparison's version-sensitive claims against official sources before trusting it as the decision base. Fetch first-party docs, confirm each load-bearing claim, fold any deltas back into the doc.
3. Capture the deployment context as hard constraints: what already exists, what is greenfield, the runtime and governance posture, and the shape of the upstream.
4. Re-score each option against those constraints, not in the abstract. Drop any option whose sole rationale is nullified by the context.
5. Look for composition among the survivors, not only competition. Two options that read as rivals often stack.
6. Name the single deciding variable that splits the residual choice, and state the verdict conditionally on it.
7. Make the verdict architect-legible: separate the option identifier from the design pattern, and attach the concrete cloud and platform components to each scenario.

### Critical moves

| Move | Why it is load-bearing |
| :--- | :--- |
| Verify before deciding | The verdict rests on the doc's claims. In the session, two load-bearing facts (DBR 18.1 file-events default, file events default-on for new locations) were only confirmable in the FAQ, not the pages the doc itself cited. Decide on an unverified doc and the verdict can rest on a stale claim |
| Re-score against context, not in the abstract | The generic tradeoffs do not select. The context nullified whole branches: with Unity Catalog present, the two options whose only purpose was escaping UC lost their reason to exist. Remove this move and all options survive, so nothing converges |
| Challenge the upstream assumption | Recognising the extractor as a puller (periodic, bursty arrivals) flipped the default away from always-on streaming toward event-triggered ephemeral compute. Remove this and you default to a continuous stream and overspend on idle compute |
| Name the one deciding variable | Reducing the residual choice to a single checkable question (freshness SLA against pull cadence) replaces an open debate with a falsifiable fork. Remove this and the verdict stays mushy |

### Pits to avoid

- Trusting a doc's own "checked against current docs" line without re-fetching. The doc was accurate here, but the claims that decided the verdict were the ones easiest to get wrong.
- Treating options as mutually exclusive. The file-arrival trigger and managed file events compose: the trigger starts the job, the Auto Loader inside uses the managed file events mechanism. Either/or framing hides the real answer.
- Scoring tradeoffs abstractly. "Cache hop adds latency" only bites if latency matters here. "Needs UC" only bites if UC is absent. Let the context decide which generic tradeoff is real.
- Following a workspace tool contract past the point it serves its intent. The contract named a fetch tool that truncates long pages, which would have undermined full-content verification. The better tool for the domain was used and the deviation flagged.

## When to use it

- A pre-enumerated, option-agnostic comparison already exists or can be produced cheaply.
- The deployment context is concrete enough to nullify branches: known runtime, known governance, a clear split between what exists and what is greenfield.
- The options carry version-sensitive claims that can be checked against official sources.

## When not to use it

- The option set is not yet defined. That is design-from-scratch, so use the design workflow.
- The context is still open or hypothetical, so nothing collapses.
- Only one option is viable from the outset, so there is no convergence to perform.
- The decision is value-driven or political rather than constraint-driven.

## Expected outcome

| Check | Pass condition |
| :--- | :--- |
| Re-scored table | Each option has a benefit and tradeoff stated against the actual context, plus a keep, drop, or conditional verdict |
| Single deciding variable | Any residual choice hangs on exactly one named, checkable variable |
| Traceable claims | Every version-sensitive claim under the verdict is traced to an official source |
| Transferable | A future reader facing a similar lock-in reaches a verdict without re-enumerating options or re-verifying from scratch |

## Tradeoffs

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Verification depth | Trust the doc's self-attestation | Re-fetch every cited source | Re-fetch all sources, since the verdict rests on them, accepting the token cost |
| Tool routing | Follow the workspace contract tool | Use the better tool for the domain | Better tool, with the contract deviation flagged once |
| Verdict shape | One unconditional pick | A full conditional fork | A primary verdict plus one deciding variable, because the context left exactly one variable open |
| Recipe reconstruction | Transcribe the session as it ran | Reconstruct the idealised path | Reconstruct, detours removed |
| Scoring frame | Keep the generic tradeoffs | Re-score against context | Re-score, since generic tradeoffs do not select |

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-06-10 |
| Status | Draft |
| Pairs with | desktop-chat/outputs/2606-o2-architecture-design/2026-06-09-adls-bronze-ingestion-design.md |
