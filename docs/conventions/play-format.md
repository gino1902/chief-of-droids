# Play Format — Structure and Principles

> Specification for authoring *plays* — retrospective documents that capture
> a non-generic session pattern in reusable form. Derived from one source
> instance: `docs/brainstorms/2026-05-22-wiki-framework-play.md`.
>
> ⚠️ N=1 — principles below are inductive from a single play. Treat as
> provisional until validated against a second instance.

## What a play is

A play is a meta-retrospective on a Claude-user session that produced a non-generic move. It captures the signature move (the inversion or unexpected pattern), the conditions under which the move is reproducible, the tradeoffs encountered grouped into categories, and a single overarching posture that subsumes those tradeoffs.

A play is not a brainstorm (that captures content decisions), nor a how-to (that prescribes steps from scratch). It documents a *pattern observed in flight*.

## When to author a play

- Session produced a notable inversion, decomposition, or structural move
- The move is not obvious from the originating prompt
- The same move would plausibly help in future sessions of similar shape
- Session yield is high enough to quantify (decisions / artifacts / simplifications)

**Don't author a play when:**

- Session was routine execution (read → write → commit)
- The session's value lives in its content output, not its meta-pattern
- The pattern is already documented by a skill or convention
- Session yield is too thin for the Outcomes count to be meaningful

## Section structure

| Section | Purpose | Shape |
| :--- | :--- | :--- |
| **Originating prompt** | Verbatim trigger — preserves provenance and the format policy the play must honour | Blockquote |
| **Hook** | One-paragraph narrative of the *signature move* — the inversion or unexpected twist that made this session non-generic | Prose |
| **When to trigger** | Pattern-match conditions + explicit *don't trigger* counter-cases | Bullet list + "Don't trigger when…" sentence |
| **Why it matters** | Value proposition — what the play catches / produces that a naive flow would miss | Prose, one tight paragraph |
| **Outcomes** | Quantified inventory of what the session produced — makes the play falsifiable | Count table + output path |
| **How we conducted the play** | Three sub-sections: friction patterns / state-gap delta / numbered best-practices | Table + Table + Numbered list |
| **Tradeoffs — the categorization** | The thesis of the play. Step back from the individual decisions and group them into Tn categories | One subsection per Tn category, each with: decision table (pole/pole/chosen) + meta-observation |
| **Meta-meta-observation** | Single overarching posture detected across all Tn categories | One-line aphorism + prose justification |
| **Version block** | Standard. Plus `Pairs with:` line linking the deliverable doc(s) | Table |

## Principles

| # | Principle | Why it matters |
| :--- | :--- | :--- |
| P1 | **Tradeoffs are the deliverable, not the decisions.** The play's centre of gravity is the Tn categorization; individual decisions are inputs to it. | A play that only lists decisions is a changelog. The categorization is what makes it transferable. |
| P2 | **Each tradeoff stated as poles + a chosen position.** Both poles are named honestly; the chosen point is rarely either extreme. | Forces the author to articulate what was given up — single-pole framing hides the cost. |
| P3 | **Meta-observation per category is mandatory.** A decision table alone is descriptive; the meta-observation is what makes it a *pattern*. | Without it the table is data, not insight. |
| P4 | **Quantify outcomes.** Count decisions, open items, residual risks, simplifications, canonical text fragments produced. | Quantification forces honesty about session yield and gates publication (thin counts ⇒ no play). |
| P5 | **Friction is data, not noise.** Mid-session breakdowns (user lost, pushback, redirects) are catalogued as patterns that *produced* the best outputs. | Friction marks the seams where the move actually mattered. Hiding it lies about the session's shape. |
| P6 | **State-gap delta makes value legible.** Two-column begin/end table converts a meandering thread into a measurable change-in-the-world. | Same role as exit criteria in a plan — the delta is the outcome. |
| P7 | **Best practices are numbered and concrete.** No vague advice — each item names a move and where it was applied. | Anchors generic-sounding practices ("multi-pass refinement") to specific session moments. |
| P8 | **Counter-cases gate adoption.** "Don't trigger when…" sentence prevents the play from being mis-applied to wrong situations. | Without counter-cases, the play becomes universal advice and stops being a pattern. |
| P9 | **Single overarching posture closes the play.** The meta-meta-observation is a one-line aphorism that subsumes the Tn categories. | If no posture emerges, the categorization is wrong or the session was too noisy to yield a pattern. |
| P10 | **Limits of the posture are flagged.** The aphorism is not universal — state the conditions under which it would need to be revisited. | Prevents the play from being applied past its zone of validity. |

## Authoring procedure

1. Read the session end-to-end before drafting any section.
2. Identify the signature move — write the **Hook** first (one paragraph). If you cannot, the session likely does not warrant a play.
3. Reverse-engineer **When to trigger** from the conditions that made the move possible. Include explicit don't-trigger cases (P8).
4. Quantify **Outcomes** before writing prose. Thin counts ⇒ stop authoring (P4).
5. Catalogue conversation friction patterns — including ones that felt like failures (P5). Each row: pattern, where, what it produced.
6. Build the begin/end state-gap table — two columns, no commentary (P6).
7. Number the best practices — each item names a move + where it was applied (P7).
8. List individual decisions on a scratchpad. Cluster them into Tn tradeoff categories. Each category gets a decision table with `<pole A> / <pole B> / chosen` (P2).
9. Write a one-line meta-observation per Tn category — descriptive of the *pattern*, not the decisions (P3).
10. Surface the meta-meta-observation — the one-line posture that subsumes the Tn categories (P9). If no such posture emerges, the categorization is probably wrong.
11. Flag the limits of the posture — under what conditions would it need to be revisited? (P10)

## Format conventions

- Tables over bullet lists for structured comparisons (poles, friction patterns, state delta).
- One section per heading; avoid nested sub-sub-sections.
- All quantification in the Outcomes table; do not scatter counts through prose.
- Meta-observations rendered with `**Meta-observation:** …` on a single line at the end of each Tn subsection.
- Version block carries a `Pairs with:` row linking the deliverable doc(s) the session produced.

## Naming and location

- Filename: `YYYY-MM-DD-<topic>-play.md`
- Default location: `docs/brainstorms/` (alongside the brainstorm or deliverable it pairs with). Move to a dedicated `docs/plays/` only once N ≥ 3.

## Open questions (N=1 caveats)

| # | Question | Trigger to revisit |
| :--- | :--- | :--- |
| Q1 | Is 6 Tn categories the right ceiling? | Second play produces 4 or 8 categories naturally |
| Q2 | Does the Originating-prompt section stay verbatim, or get distilled? | Second play has a long or noisy originating prompt |
| Q3 | Should Outcomes count format be standardized (table columns fixed)? | Second play's outcome counts don't map cleanly to the same columns |
| Q4 | Is the Pairs-with line sufficient, or should plays embed the deliverable's exit criteria? | Second play's deliverable evolves independently of the play |

---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.0        |
| Last Updated | 2026-05-25 |
| Status       | Draft      |
