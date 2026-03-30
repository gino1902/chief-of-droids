<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-03-30 -->

# Challenge Protocol

Read at Step 3 of the executing-tasks outer loop.
Defines the confidence gate for challenging task intent and plan.

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
blocking issues and the task scope is narrow and well-specified, one round
may suffice — but Claude must state explicitly that it is recommending
approval after fewer than the minimum.

> "Only one challenge round run — scope appears well-specified. Recommend approval,
> but an additional round is available if you want it."

---

## What to Challenge

Each round targets a different layer. Run in this order:

| Round | Focus | Questions to ask |
|:------|:------|:----------------|
| 1 | Scope and assumptions | Is the task boundary clear? Are there unstated dependencies? Does the scope match the target? |
| 2 | Plan feasibility | Can each phase be executed with available tools? Are outputs from one phase actually consumed by the next? Is "done" defined? |
| 3+ | Edge cases and failure modes | What happens if a tool fails? What if the output does not match the QA test? Is there a rollback path? |

---

## Blocking vs Advisory Issues

**Blocking** — must be resolved before plan is approved:
- Undefined scope boundary
- Missing required input (file not found, task ID wrong)
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
Surface a one-line summary before Step 4:

> "Challenge complete: [N] rounds. Blocking issues resolved: [list or 'none'].
> Advisory items open: [list or 'none']. Plan approved."
