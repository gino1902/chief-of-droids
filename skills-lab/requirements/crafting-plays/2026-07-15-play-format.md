# Play format

> Specification for authoring plays. A play is a reusable recipe reconstructed
> from a session, so it can be replayed when a similar situation recurs.
>
> ⚠️ Unverified. Treat as provisional until validated against a second instance.

## What a play is

A play is a recipe you want to reproduce when you face a similar situation again. A session usually spans several moves; a play captures one. It is reconstructed from the move within a Claude-user session that is worth capitalising on, then turned into a repeatable procedure pitched at the narrowest scope that will recur.

A play is not a narrative retrospective (which recounts what happened) and not a generic how-to (which prescribes steps from scratch). It is the idealised path through a situation, recovered after the fact, with the dead ends removed and the load-bearing decisions named.

The play is the output of this format. The deliverable is the recipe itself (optimal workflow, critical moves, pits to avoid), the conditions that tell a future reader when to reach for it and what they should get back, and the tradeoffs taken to make it work.

## Section structure

| Section | Purpose | Shape |
| :--- | :--- | :--- |
| **When to trigger** | The situation that calls for the play, in its technical or business context, illustrated with concrete examples. This is the recognition signal. | Prose plus examples |
| **Premises** | The dated, time-sensitive claims the play relies on, each with a revalidation check. Replay begins by re-testing every premise. | Table (see "Execution fidelity") |
| **Why it matters** | The problem the play solves and the deliverable(s) it produces. Which of the two dominates depends on the play. | Prose, one tight paragraph |
| **Inputs** | The artefacts the play consumes, each anchored to an on-disk path with a content contract and an on-missing behaviour. Workflow gates may only reference inputs declared here. | Table (see "Execution fidelity") |
| **The play** | The recipe itself, the moves. Three parts: optimal workflow, critical moves, pits to avoid. | See "The play in detail" |
| **When to use it** | Go conditions. The preconditions under which applying the play is the right call once the situation is recognised. | Bullet list |
| **When not to use it** | No-go conditions and counter-cases that look similar but break the recipe. | Bullet list |
| **Expected outcome** | The value a future reuse should return, for the user and/or the system, stated in checkable terms. Names the deliverable artefact and its landing destination (chat output, or file path following the repo convention). | Prose or short table |
| **Tradeoffs** | The decisions where one pole was chosen against another, with the position taken and what it gave up. The reasoning behind the recipe. | One or more decision tables |
| **Version block** | The play's single version block. Carries Version, Last Updated, Status, and a Pairs with: line linking both the input artefact(s) the play gates on and the deliverable doc(s) the originating session produced. N/A only when the play neither consumes nor produces on-disk documents. | HTML comment at file end |

"When to trigger" describes the situation so a reader can pattern-match it. "When to use it" and "When not to use it" are the go and no-go gates applied once the match is made. Keep the three distinct. Premises are neither: they are facts assumed true at authoring time that may have decayed by replay time.

## The play in detail

| Part | Purpose | Shape |
| :--- | :--- | :--- |
| **Optimal workflow** | The reconstructed sequence of steps that worked, idealised from the session with detours removed. | Numbered list |
| **Critical moves** | The few decisions the outcome depends on. Remove one and the result collapses. | Bullet list or table |
| **Pits to avoid** | The missteps, dead ends, and frictions the session hit, stated as warnings. | Bullet list |

## Execution fidelity

A play that cannot be replayed deterministically from what is on disk is a retrospective with numbered steps. The rules below make every gate, method, and boundary in the play checkable at execution start.

### Inputs table

| Column | Content |
| :--- | :--- |
| Artefact | Name of the required input document or resource |
| Anchor | Absolute or repo-relative on-disk path. "Produced in a prior session" is not an anchor |
| Content contract | What the artefact must contain to be fit for purpose, stated so a rebuilt replacement can be validated against it, not just matched by filename |
| On missing | Produce-first (with the producing procedure or play named) or abort |

Every prerequisite the workflow gates on must be a row in this table. A workflow step may not test for an artefact that has no row.

### Fidelity rules

| # | Rule |
| :--- | :--- |
| F1 | Anchored inputs. Every input exists at a declared path, checkable at replay start from disk, never from session memory. |
| F2 | Content contract. A rebuilt or replaced input satisfies the declared content contract before the workflow proceeds. |
| F3 | Method determinism. Any scale, threshold, scoring rule, classification scheme, or query template a workflow step depends on is embedded in the play or linked at an anchored path. A step that says "rank by X" without the scale is not replayable. |
| F4 | Terminology anchoring. When the play narrows, qualifies, or renames terms from a source taxonomy (official docs, standard vocabularies), it states the mapping: play term, source term, qualifier applied. |
| F5 | Resource accounting. When the play states a budget (queries, fetches, tool calls), it defines what counts against it and how discoveries made outside the budgeted phase (for example, sources surfaced while producing inputs) are treated: carried into the corpus, or discarded. |
| F6 | Premise revalidation. Time-sensitive claims are recorded as premises with an as-of date and a revalidation check. A failed premise is a revision trigger for the play, not a silent continuation. |
| F7 | Deliverable landing. The expected outcome names the deliverable artefact and its destination. A deliverable with no landing rule defaults to chat output, and that default is stated, not implied. |

### Premises table

| Column | Content |
| :--- | :--- |
| Premise | The time-sensitive claim (for example, "the integration is in beta") |
| As of | The date the claim was last verified |
| Revalidation check | The concrete test to re-run at replay (for example, "fetch the official status page and confirm the beta note") |

## Replay procedure

1. Premise check. Re-run every revalidation check in the Premises table. Any failure is surfaced and treated as a revision trigger; the user decides whether to revise the play or proceed with the premise struck out.
2. Input gate. Verify every Inputs row: the artefact exists at its anchor and satisfies its content contract. On missing or non-conforming, follow the row's on-missing behaviour before any workflow step runs.
3. Execute the optimal workflow. Methods, scales, and budgets come from the play per F3 and F5, not from reconstruction.
4. Land the deliverable per the expected outcome's destination rule.

## Tradeoffs

Each tradeoff names both poles honestly and states the position taken, which is rarely either extreme. The chosen point and what it cost are the reusable part, since a future reader inherits the same tension. When there are many, cluster them into categories and give each category its own table.

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| (one row per load-bearing decision) | | | |

## Principles

| # | Principle | Why it matters |
| :--- | :--- | :--- |
| P1 | The recipe is the deliverable. The play's centre of gravity is the reusable workflow, not the account of the session. | A play that only recounts the session is a retrospective. The reusable procedure is what makes it transferable. |
| P2 | Reconstruct, do not transcribe. The workflow is the idealised path, not the literal sequence. | The session wandered. A future reader needs the route that worked, not the wrong turns. |
| P3 | Critical moves are named explicitly and kept few. | If everything is critical, nothing is. Naming the load-bearing decisions is what lets a reader reproduce the result. |
| P4 | Pits come from real missteps. | Friction in the session is mined, not hidden. A pit the author actually fell into is worth more than a hypothetical one. |
| P5 | Triggers are shown with examples, not only described. | A trigger condition without a concrete instance cannot be matched against a new situation. |
| P6 | Use and don't-use gates are both stated. | Without the don't-use gate the play becomes universal advice and stops being a recipe. |
| P7 | Expected outcome is stated as value and made falsifiable. | If a reuse cannot be checked against the promised outcome, the play cannot be validated or retired. |
| P8 | Each tradeoff is stated as both poles plus the chosen position. | Single-pole framing hides the cost. Naming what was given up makes the choice reusable rather than dogmatic. |
| P9 | Pitch the recipe at the narrowest scope that will recur. Keep it specific to the concrete instance until a second instance is in hand. | Generalising on a single observation invents a recurrence that has not been seen. A later instance is what widens the scope. |
| P10 | Replayable means checkable from disk. Every gate the workflow imposes is decidable at execution start from anchored artefacts, embedded methods, and dated premises. | A gate that depends on session memory or the author's recall fails silently on replay, and the play executes against reconstructed rather than real prerequisites. |
| P11 | Premises decay. The situation description is written for pattern-matching; claims that can change are premises with revalidation checks, not standing facts. | A stale premise turns the play's own replay triggers invisible: the condition fires in the world while the play still asserts the old state. |

## Authoring procedure

1. Read the session end to end before drafting any section.
2. Bound the play. A session usually spans several moves; the play captures one. Identify the single situation the play covers, from the user's instruction or the single most capitalisable move, and state what falls out of scope. Confirm the target with the user when the session is multi-scope or the instruction is ambiguous about which move.
3. Identify the situation and the move that resolved it. Draft When to trigger first, with at least one concrete example. If you cannot, the session probably does not warrant a play.
4. Extract the premises. Date every time-sensitive claim in the trigger and pair it with a revalidation check (P11, F6).
5. State why it matters. Name the problem solved and the deliverable(s) produced.
6. Declare the inputs. For every artefact the workflow will gate on, fill an Inputs row: anchor, content contract, on-missing behaviour (F1, F2). If an input only ever existed as chat output, either persist it now and anchor it, or redesign the gate.
7. Reconstruct the optimal workflow. Walk the session, keep the steps that worked, drop the detours, renumber into a clean sequence (P2). Embed or link every method, scale, and budget a step depends on (F3, F5), and state term mappings where the play narrows a source taxonomy (F4).
8. Extract the critical moves. For each, apply the collapse test: would the outcome still hold if this move were removed? If yes, it is not critical (P3).
9. Mine the session's friction and dead ends for pits to avoid (P4).
10. Write the when-to-use and when-not-to-use gates (P6).
11. State the expected outcome as value for the user and/or the system, in checkable terms, including the deliverable's landing destination (P7, F7).
12. Catalogue the tradeoffs. For each load-bearing decision, name both poles and the position taken. Cluster into categories if there are many (P8).
13. Add the version block with a Pairs with: row linking the input artefact(s) and the deliverable doc(s), or N/A when the play neither consumes nor produces on-disk documents.
14. QA pass. Verify: all concrete examples sit under When to trigger, every workflow gate maps to an Inputs row, every premise has a check, every stated budget has an accounting rule, and Pairs with is consistent with the Inputs table and expected outcome.

## When to author a play

- It is user triggered. Claude reads the session against this format and challenges it against "When not to author a play" below.
- If the analysis meets the criteria, Claude prompts the user to confirm the play construction, and displays any unmet criteria with the reason they are not met.

## When not to author a play

- The session was routine execution (read, write, commit).
- The session's value lives in its content output, not in a reusable pattern.
- The pattern is already covered by a skill or convention.
- The session yield is too thin for the recipe to be worth reconstructing.

## Format conventions

- Tables over bullet lists for structured comparisons.
- One section per heading. Avoid nested sub-sub-sections beyond the play's three parts.
- The optimal workflow is numbered. Critical moves and pits are listed.
- Tradeoffs are rendered as pole A / pole B / chosen position tables.
- All concrete examples sit under When to trigger, not scattered through other sections. Pits reference session friction as warnings without re-narrating the incident; the incident's concrete telling belongs under When to trigger.
- The play's version block is a single HTML comment at file end, not a visible table. It carries a Pairs with: row linking the input artefact(s) the play gates on and the deliverable doc(s) the originating session produced. N/A is reserved for plays that neither consume nor produce on-disk documents. Plays are interactively authored rather than workflow-written, so they use the HTML-comment form.

## Naming and location

- Filename: `YYYY-MM-DD-<topic>-play.md`
- Location follows the repository's established convention for plays, and falls back to the project root only when the repo has none. The spec does not override a repo convention.

---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 2.2        |
| Last Updated | 2026-07-15 |
| Status       | Draft      |
