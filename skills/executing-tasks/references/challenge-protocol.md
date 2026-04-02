<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-04-01 -->

# Challenge Protocol

Read at Step 5 of the executing-tasks outer loop.
Defines the confidence gate for challenging the task plan against confirmed intent.

---

## Purpose

The challenge gate prevents premature plan approval by requiring Claude to
surface blocking issues before committing to an execution path. It is
confidence-based, not count-based: the gate exits when no new blocking
issues surface AND the user explicitly approves.

---

## Self-Assessment Question

After each challenge round, Claude asks internally:

> "Did this round surface at least one new blocking issue — a gap, contradiction,
> underspecified decision, or incorrect assumption that would cause the plan to fail
> or produce wrong output if left unresolved?"

If YES → mandatory further round. Do not ask user; run the next round immediately.
If NO → surface the finding and ask the user once:

> "No new blocking issues found in this round. Approve plan, or request another challenge round?"

---

## Minimum Recommendation

Two challenge rounds are recommended before seeking approval.

This is a recommendation, not a hard gate. If the first round surfaces no
blocking issues and the confirmed intent is narrow and well-specified, one round
may suffice — but Claude must state explicitly that it is recommending approval
after fewer than the minimum.

> "Only one challenge round run — intent appears well-specified. Recommend approval,
> but an additional round is available if you want it."

---

## What to Challenge

Each round targets a different layer. Run in this order:

| Round | Focus | Questions to ask |
| :--- | :--- | :--- |
| 1 | Intent precision | Is the action clause specific enough to produce a deterministic plan? Is the value clause testable — could a pass/fail verdict be reached against it? Does the confirmed target match the action implied by the intent? |
| 2 | Plan feasibility | Can each phase be executed with available tools? Are there unstated dependencies between phases? Are outputs from one phase actually consumed by the next? Is "done" defined? |
| 3+ | Edge cases and failure modes | What happens if a tool fails? What if the output does not match the QA test? Is there a rollback path? |

---

## Blocking vs Advisory Issues

**Blocking** — must be resolved before plan is approved:
- Intent action clause too vague to produce a deterministic plan
- Value clause not testable — no observable pass/fail condition
- Missing required input — Path 1: file not found, task ID wrong; Path 2: unparseable trigger prompt
- Plan phase with no defined output
- Tool dependency with no failure handling

**Advisory** — surface but do not block:
- Style or naming inconsistency
- Optimisation opportunity
- Non-critical ambiguity the user can resolve during execution

---

## Exit Conditions

The gate exits when ALL of the following are true:
1. At least one challenge round has been completed
2. The last round surfaced no new blocking issues
3. The user has explicitly approved the plan (not implied, not assumed)

The gate does NOT exit on:
- User impatience ("just proceed") without explicit approval — ask once more
- A fixed round count being reached
- Advisory-only issues remaining open

---

## After Gate Exit

Record which rounds were run and what was resolved.
Surface a one-line summary before Step 6:

> "Challenge complete: [N] rounds. Blocking issues resolved: [list or 'none'].
> Advisory items open: [list or 'none']. Plan approved."


| Field        | Value       |
|--------------|-------------|
| Version      | 1.1         |
| Last Updated | 2026-04-01  |
| Status       | Draft       |
