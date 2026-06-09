# Doc-grounded design convergence

> A play for hardening a draft cloud-system design by challenging it against official documentation, pass after pass, until the mechanisms, the abstraction level, and the sourcing all hold. Worked instance: an event-driven ADLS Gen2 to bronze ingestion design.

## When to trigger

You hold a draft technical design for a system built on managed cloud services whose mechanics change between releases and whose component boundaries are easy to mis-state, and you want to harden it before a review or a build commitment. The recognition signal is a design that reads plausibly but rests on asserted mechanisms that were never checked against the platform's own documentation, or a diagram whose boxes quietly mix abstraction levels.

Concrete examples, all from the originating session:

- A C4 diagram labelled "ADLS sends event to Unity Catalog" and "Unity Catalog triggers job". Both are wrong. ADLS emits to Event Grid, and the Workflows file-arrival trigger, not Unity Catalog, starts the job.
- A flow describing a "listening job" that catches the notification. In the trigger design there is no listening job. There is a Databricks-managed control-plane service plus an ephemeral job run.
- A single "Auto Loader stream" box that actually hides two implementations, legacy file notification with a per-stream queue and managed file events with a shared cache, which differ in flag, topology, and ownership.
- A caveat stating "full listing every 7 days" when there are two distinct cadences, a 24-hour service reconciliation scan and a 7-day stream read-position expiry.

## Why it matters

Draft cloud designs drift from how the platform actually behaves, and the cost surfaces late, at architecture review or in production, where it is most expensive. The play converts a plausible draft into a design where every present-state claim is traceable to official documentation, the options are separated by real mechanism rather than by surface resemblance, and forward-looking community signals stay visible but quarantined. The deliverable is a hardened design artifact, a diagram with a per-step and per-option decision table, sourced citations, and a separated signals section, that a reviewer can audit line by line.

## The play

### Optimal workflow

1. State the design as an explicit flow or diagram, naming every step and every component.
2. Challenge each step against official documentation. Fetch the page, replace every asserted mechanism with a sourced one, and cite it.
3. Fix the abstraction level before drawing. Decide the C4 level, collapse internals into their container, and keep separately deployable units as separate boxes.
4. Distinguish mechanisms precisely. Where one box hides two implementations that differ in flag, topology, or ownership, split it into sub-options.
5. Re-run verification as a fresh pass on the revised design, and on each pass actively hunt drift across preview versus GA status, limits, cadences, and product naming, correcting what moved.
6. Separate official documentation from community or MVP signals. Tag the signals, state what each would change, and attach a verification step.
7. Package the result as a diagram plus a per-step and per-option decision table, with a sources list and a quarantined signals section.

### Critical moves

- Ground every present-state claim in a documentation fetch rather than memory. Remove this and drift returns within a single pass.
- Set the C4 level explicitly before drawing. Remove this and containers and components blur, and the diagram fails review.
- Split options by mechanism, not by resemblance. Remove this and the legacy and managed paths collapse into one box carrying the wrong shared tradeoffs.
- Quarantine community signals from sourced facts. Remove this and one unverified claim contaminates the documented baseline.
- Treat each verification request as a new drift hunt, not a re-read. Remove this and stale caveats survive into the deliverable.

### Pits to avoid

- Naming a managed service loosely, such as calling the file events service "a managed thing". Name it as a Databricks-managed control-plane service.
- Routing the event to the wrong component, such as "ADLS notifies Unity Catalog" or "Unity Catalog triggers the job". Unity Catalog governs the location, it is not the event bus or the scheduler.
- Treating a "listening job" as a running user job when the trigger design uses a managed service plus an ephemeral run.
- Merging the Workflows file-arrival trigger path and a continuous stream into one chain. They are alternative designs, not one sequence.
- Asserting a single listing cadence when there are two, owned by different parties.
- Assuming the platform default without checking the runtime, since a community signal suggested the Auto Loader default may have flipped from directory listing to file notification.

## When to use it

- The design rests on managed cloud services whose mechanics change between releases.
- The output faces an audience that needs claims to be sourced, such as an architecture review, an executive sign-off, or a regulated context.
- Precise component boundaries and mechanism naming materially affect the decision.
- Official documentation exists and is fetchable for the services in scope.
- The cost of shipping a wrong mechanism is high relative to the time spent verifying.

## When not to use it

- The work is routine execution against a stable, well-understood stack.
- The design is trivial, or the mechanism is settled and unlikely to drift.
- No authoritative documentation exists to ground the claims, so verification has nothing to anchor against.
- Speed dominates and the cost of being wrong is low, where a fast single answer is the better trade.
- The question is about content output rather than a transferable design pattern.

## Expected outcome

A future reuse returns a design artifact that passes the checks below. If any check fails, the play was not fully applied.

| Check | Pass condition |
| :--- | :--- |
| Sourcing | Every present-state claim carries an official documentation source. |
| Option distinctness | Every option differs from its siblings by a named mechanism, not by tone. |
| Signal hygiene | Every community or forward-looking claim is tagged and carries a verification step. |
| Auditability | A reviewer can trace each decision to its source without asking the author. |

## Tradeoffs

### Rigour and pace

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Verification depth | One fast sourced answer | Exhaustive multi-pass challenge | Iterate passes until claims stop moving, accepting many turns and searches |
| Response to a repeat verify request | Re-read and reassure | Treat as a fresh drift hunt | Fresh pass each time, surfacing new drift even when little changes |

### Design surface

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Option set | Recommend a single path | Keep every viable path | Keep four options with the choice deferred to context, accepting more to maintain |
| Mechanism granularity | One stream box | Split by implementation | Split legacy and managed, accepting more boxes for correct tradeoffs |
| Diagram medium | Rich rendered diagram | Portable ASCII | ASCII for speed and portability, accepting less visual polish |

### Sourcing and signals

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Community signals | Exclude entirely | Merge with the docs | Include but quarantine and tag, accepting an extra section |
| Claim basis | Trust model knowledge | Fetch and cite | Fetch and cite for present-state claims, accepting slower turns |

### Bronze modelling

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Bronze schema | Typed relational columns | Raw JSON string | parse_json to VARIANT plus a few promoted columns, accepting that VARIANT cannot be a partition or clustering key |

---

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-06-09 |
| Status | Draft |
| Pairs with | adls-bronze-ingestion-design.md |

