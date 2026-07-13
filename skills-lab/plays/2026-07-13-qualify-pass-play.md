# Qualify pass

> A multi-anchor review cycle that eliminates drift from a decision-bearing artefact and drives it to a verifiable converged state.

## When to trigger

A session has produced or revised a decision-bearing artefact (requirements document, design note, proposal, SAD section) across multiple turns, and one of these signals appears:

- The user asks to review, challenge, or qualify the artefact ("make a qualify pass", "challenge your answer", "review against quality").
- The artefact is about to be locked: version bump toward Final, commit, or handoff to planning.
- The author suspects the artefact records things the user never decided.

Concrete example (originating session): a refinement-harness requirements draft was audited on the decision-fidelity anchor. Five genuine drifts surfaced, including a user deferral silently converted into a design constraint, an unconfirmed number recorded as decided, and review rhetoric written up as a decision.

## Why it matters

Drift between what was decided in conversation and what the artefact says persists silently into planning, where it becomes a false constraint. Unanchored review passes make it worse: pass N+1 re-audits pass N's ground and manufactures churn, cosmetic findings dressed as drifts. The play produces a converged artefact where every claim traces to a decision, satisfies its governing contract, is internally consistent, and respects workspace conventions, with the drift tables as an audit trail.

## The play

The locked prompt:

```markdown
Qualify pass on [artefact].
Anchor: [decision fidelity | governing contract | internal consistency | conventions]
— one per pass, not yet used this cycle. Trivial artefact → single combined pass.

- Audit against the anchor only.
- Drift table: # | location | says | ground truth | Genuine/Churn | fix
- Apply nothing; await accept/reject per drift.
- Zero Genuine drifts → anchor clean. All four clean → converged, stop.
```

### Optimal workflow

1. Name the artefact and identify its governing contract (owning skill, template, checklist). If none exists, declare anchor 2 degraded rather than inventing one.
2. Run one qualify pass per anchor, in order: decision fidelity, governing contract, internal consistency, conventions.
3. In each pass, audit against that anchor only and lay drifts in the table. Apply nothing.
4. The user accepts or rejects per drift. Apply accepted fixes as a full-artefact revision.
5. Re-run any anchor plausibly dirtied by the fixes.
6. Stop at convergence: all four anchors clean on the current artefact version. Further passes are churn by definition.

### Critical moves

- Anchor rotation. One anchor per pass. Without it, the next pass re-audits the previous one and generates churn instead of signal.
- Genuine/Churn classification. Genuine changes meaning, scope, or a decision. Churn is cosmetic with near-zero risk either way. The split keeps accept/reject decisions cheap.
- Apply-nothing gate. Findings are proposals. User arbitration per drift prevents the reviewer silently re-resolving tensions the user should own.
- Convergence stop. A verifiable termination criterion. Without it, review loops indefinitely on diminishing findings.

### Pits to avoid

- Rerunning the same anchor "for quality". The second pass finds cosmetics and dresses them as drifts to satisfy the request.
- Recording review rhetoric as decisions. Phrases from a recommendation ("highest-value 20% first") are not decisions and do not belong in a Key decisions section.
- Converting user deferrals into constraints. "Decision not required at this stage" is a deferral, not permission to fix the answer.
- Silently resolving tensions between user answers. When two answers conflict (enforce vs guidance), record the resolution as a visible decision, not a quiet edit.
- Inventing a governing contract for free-form artefacts. Declare the anchor degraded and run the remaining three.

## When to use it

- The artefact carries decisions accumulated across multiple turns or sessions.
- A lock-in event is near: Final status, commit, or handoff.
- The governing contract exists, or its absence can be declared explicitly.

## When not to use it

- Trivial artefact. Use the single combined pass instead of four.
- The artefact is a record of a meeting or session. Fidelity to what happened governs, not fidelity to decisions.
- No decisions exist yet (mid-brainstorm). Qualifying an exploration freezes it prematurely.
- The pattern is already enforced by a stricter mechanism (a QA suite from executing-tasks, a skill checklist run in full).

## Expected outcome

| Value | Checkable form |
| :--- | :--- |
| Converged artefact | All four anchors declared clean on the same artefact version |
| Audit trail | One drift table per pass, with accept/reject recorded per drift |
| Bounded cost | Typical cycle 4 to 6 passes; a cycle that keeps finding Genuine drifts past 6 passes signals an upstream problem, not a review problem |

## Tradeoffs

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Pass granularity | One holistic pass: fast, but anchors blur and findings repeat | One pass per anchor: more passes, clean scoping | Per anchor, with a triviality valve for small artefacts |
| Fix application | Auto-apply: fast, but silently re-resolves user-owned tensions | Apply nothing: slower, every fix arbitrated | Apply nothing; the drift table is a proposal, never an action |
| Cycle state | Formal dirty-flag bookkeeping per fix | Conversational memory only | Conversational. One cheap re-pass over plausibly dirtied anchors costs less than tracking which fix dirties which anchor |
| Prompt weight | Rich rules covering every edge | Lean six lines | Lean. Instruction compliance degrades with length; the anchors and the table are the load-bearing parts |

---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.0        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
| Pairs with   | docs/brainstorms/2026-07-13-refinement-harness-requirements.md (pending write, editor gate open) |

<!--
Version: 1.0 | Last Updated: 2026-07-13 | Status: Draft
-->
