<!-- version: 1.7 | author: chief-of-droids workspace | last_updated: 2026-04-13 -->

<purpose>

# Challenge Protocol

Read at Step 5 of the executing-tasks outer loop.
Defines the confidence gate for challenging the acceptance criteria before plan authoring.

The challenge gate prevents premature plan authoring by requiring Claude to
surface blocking issues in the acceptance criteria before committing to an
execution path. It is confidence-based, not count-based: the gate exits when
no new blocking issues surface AND the user explicitly approves.

Note: plan-coverage checks (does each sub-task map to a criterion? does each
sub-task have a defined output?) run at Step 7 — after the plan exists. Step 5
operates on acceptance criteria only.

Reason internally before each challenge round. Do not surface internal reasoning
steps in output — present findings only.

</purpose>

<self-assessment>

## Self-Assessment Question

After each challenge round, Claude asks internally:

> "Did this round surface at least one new blocking issue — a gap, contradiction,
> underspecified decision, or incorrect assumption that would prevent one or more
> acceptance criteria from being met?"

If YES → mandatory further round. Do not ask user; run the next round immediately.
Reason: surfacing a mid-challenge blocking issue to the user before resolving it
interrupts the challenge arc and invites premature approval — the gate must close
internally before the user is consulted.

If NO → surface the finding and ask the user once:

> "No new blocking issues found in this round. Approve plan, or request another challenge round?"

If the user responds with a criteria change or clarification: apply the change,
re-run the last round against the updated criteria, then re-surface the approval
prompt. If the user goes silent: wait — do not auto-proceed.

If UNCERTAIN → treat as YES. Run a further round targeting the uncertain item
specifically. Reason: an unresolved uncertainty about a blocking issue is itself
a blocking issue — resolving ambiguity requires another pass, not premature closure.

</self-assessment>

<minimum-recommendation>

## Minimum Recommendation

Two challenge rounds are recommended before seeking approval.
Reason: two rounds cover criteria viability and completeness separately — a single
round conflates both layers and misses the completeness surface.

This is a recommendation, not a hard gate. If the first round surfaces no
blocking issues and the confirmed intent is narrow and well-specified, one round
is acceptable — but Claude must state explicitly that it is recommending approval
after fewer than the minimum.
Reason: a narrow, well-specified intent has a shallow acceptance criteria surface
— a second round on an already-exhausted surface adds no signal.

> "Only one challenge round run — intent appears well-specified. Recommend approval,
> but an additional round is available if you want it."

</minimum-recommendation>

<challenge-rounds>

## What to Challenge

Each round targets a different layer. Run in this order:

| Round | Focus | Questions to ask |
| :--- | :--- | :--- |
| 1 | Criteria viability | Are all acceptance criteria specific enough to be achieved by a bounded sub-task? Are any criteria contradictory or mutually exclusive? Are any criteria dependent on inputs, tools, or states not yet confirmed available? Could a result satisfy all criteria yet still fail the confirmed intent? |
| 2 | Criteria completeness | Does the set of acceptance criteria cover the full scope of the confirmed intent? Is there any behaviour implied by the intent that no criterion captures? Are there edge conditions not addressed by any criterion? |
| 3+ | Edge cases and failure modes | What happens if a tool fails? What if the output does not match a QA test? Is there a rollback path? |

Complete all questions in the current round before evaluating whether a new
blocking issue was found. Do not stop mid-round on the first identified issue —
surface all findings from the round together.

Example (blocking issue found — Round 1):

> "Round 1 — Criteria viability:
> Blocking issue found: criterion AC-2 ('file written to target path') depends on
> filesystem write access, which has not been confirmed available for this target.
> Running Round 2 before surfacing."

Example (no blocking issues found — Round 2):

> "Round 2 — Criteria completeness:
> No new blocking issues found. All acceptance criteria map to the confirmed intent
> scope. Advisory: criterion AC-1 could be split for clarity, but is unambiguous as
> written.
> No new blocking issues found in this round. Approve plan, or request another challenge round?"

</challenge-rounds>

<round-limit>

## Round Limit and Residual Risk

If blocking issues persist after three challenge rounds, continuing is not
guaranteed to resolve them — they may indicate an underspecified intent or
acceptance criteria that cannot be resolved without external input.

After Round 3, if blocking issues remain:

Example:
> "Three challenge rounds complete. The following blocking issues remain unresolved:
> [list]. Options: (1) revise the intent or acceptance criteria to address them;
> (2) accept residual risk and proceed. Which do you prefer?"

Await explicit user choice before proceeding. Do not auto-proceed.

</round-limit>

<blocking-vs-advisory>

## Blocking vs Advisory Issues

**Blocking** — must be resolved before plan authoring proceeds:
- Acceptance criterion with no achievable implementation path given confirmed tools
  and target. If achievability is unknown due to unconfirmed tool availability or
  access: treat as a blocking issue. Surface: "AC-[N] achievability unconfirmed —
  [dependency] not yet verified. Resolve before plan authoring."
- Acceptance criterion that is not observable or not unambiguous (should have been
  caught at Step 4b — surface if found here)
- Missing required input — Path 1: file not found, task ID wrong; Path 2:
  unparseable trigger prompt
- Tool dependency with no failure handling

**Advisory** — surface but do not block:
- Style or naming inconsistency
- Optimisation opportunity
- Non-critical ambiguity the user can resolve during execution
Reason: advisory items are quality signals the user may intentionally defer —
blocking on them would gate plan authoring on presentational concerns rather
than correctness gaps.

</blocking-vs-advisory>

<exit-conditions>

## Exit Conditions

##### Gate closes when:

1. At least one challenge round has been completed
2. The last round surfaced no new blocking issues
3. The user has explicitly approved the plan (not implied, not assumed)

##### Gate does not close on:

- User impatience ("just proceed") without explicit approval — ask once more.
  Reason: "just proceed" is not an explicit approval signal — the gate requires
  a deliberate affirmative; re-asking once confirms the user understood the gate
  before it closes.
- A fixed round count being reached
- Advisory-only issues remaining open

</exit-conditions>

<after-gate-exit>

## After Gate Exit

Record which rounds were run and what was resolved.
Surface a one-line summary before Step 6:

Example:
> "Challenge complete: [N] rounds. Blocking issues resolved: [list or 'none'].
> Advisory items open: [list or 'none']. Plan approved."

Example (two rounds, one advisory item open):
> "Challenge complete: 2 rounds. Blocking issues resolved: AC-2 filesystem access
> confirmed available. Advisory items open: AC-1 could be split for clarity — user
> may address during execution. Plan approved."

</after-gate-exit>

| Field        | Value       |
|--------------|-------------|
| Version      | 1.7         |
| Last Updated | 2026-04-13  |
| Status       | Draft       |
