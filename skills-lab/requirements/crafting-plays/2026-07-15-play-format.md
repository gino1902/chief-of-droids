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
| **Why it matters** | The problem the play solves and the deliverable(s) it produces. Which of the two dominates depends on the play. | Prose, one tight paragraph |
| **The play** | The recipe itself, the moves. Three parts: optimal workflow, critical moves, pits to avoid. | See "The play in detail" |
| **When to use it** | Go conditions. The preconditions under which applying the play is the right call once the situation is recognised. | Bullet list |
| **When not to use it** | No-go conditions and counter-cases that look similar but break the recipe. | Bullet list |
| **Expected outcome** | The value a future reuse should return, for the user and/or the system. Stated in checkable terms. | Prose or short table |
| **Tradeoffs** | The decisions where one pole was chosen against another, with the position taken and what it gave up. The reasoning behind the recipe. | One or more decision tables |
| **Version block** | The play's single version block. Carries Version, Last Updated, Status, and a Pairs with: line linking the deliverable doc(s) the session produced, or N/A when the session produced chat output only. | HTML comment at file end |

"When to trigger" describes the situation so a reader can pattern-match it. "When to use it" and "When not to use it" are the go and no-go gates applied once the match is made. Keep the three distinct.

## The play in detail

| Part | Purpose | Shape |
| :--- | :--- | :--- |
| **Optimal workflow** | The reconstructed sequence of steps that worked, idealised from the session with detours removed. | Numbered list |
| **Critical moves** | The few decisions the outcome depends on. Remove one and the result collapses. | Bullet list or table |
| **Pits to avoid** | The missteps, dead ends, and frictions the session hit, stated as warnings. | Bullet list |

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

## Authoring procedure

1. Read the session end to end before drafting any section.
2. Bound the play. A session usually spans several moves; the play captures one. Identify the single situation the play covers, from the user's instruction or the single most capitalisable move, and state what falls out of scope. Confirm the target with the user when the session is multi-scope or the instruction is ambiguous about which move.
3. Identify the situation and the move that resolved it. Draft When to trigger first, with at least one concrete example. If you cannot, the session probably does not warrant a play.
4. State why it matters. Name the problem solved and the deliverable(s) produced.
5. Reconstruct the optimal workflow. Walk the session, keep the steps that worked, drop the detours, renumber into a clean sequence (P2).
6. Extract the critical moves. For each, apply the collapse test: would the outcome still hold if this move were removed? If yes, it is not critical (P3).
7. Mine the session's friction and dead ends for pits to avoid (P4).
8. Write the when-to-use and when-not-to-use gates (P6).
9. State the expected outcome as value for the user and/or the system, in checkable terms (P7).
10. Catalogue the tradeoffs. For each load-bearing decision, name both poles and the position taken. Cluster into categories if there are many (P8).
11. Add the version block with a Pairs with: row linking the deliverable doc(s), or N/A when the session produced chat output only.

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
- All concrete examples sit under When to trigger, not scattered through other sections.
- The play's version block is a single HTML comment at file end, not a visible table. It carries a Pairs with: row linking the deliverable doc(s) the session produced, or N/A when the session produced chat output only. Plays are interactively authored rather than workflow-written, so they use the HTML-comment form.

## Naming and location

- Filename: `YYYY-MM-DD-<topic>-play.md`
- Location follows the repository's established convention for plays, and falls back to the project root only when the repo has none. The spec does not override a repo convention.

---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 2.1        |
| Last Updated | 2026-07-15 |
| Status       | Draft      |
