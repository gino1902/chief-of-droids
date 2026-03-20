# Gate Assessment — Phase {N} — {YYYY-MM-DD}

> Use case: {use-case-id} — {use-case-name}
> Triggered by: {phase completion signal / user statement}
> Assessed by: Claude (data-platform-architect skill)
> Version: 1.0

---

## Phase Status Table

| Phase | Status | Evidence | Version | Gap |
| :--- | :--- | :--- | :--- | :--- |
| 1 — Requirements | | | | |
| 2 — Current State | | | | |
| 3 — Architecture Selection | | | | |
| 4 — Data Modelling | | | | |
| 5 — Security | | | | |
| 6 — Cost Modelling | | | | |
| 7 — Implementation | | | | |
| 8 — Observability | | | | |
| 9 — Final Review | | | | |

Status values: ✅ Complete · 🟡 Partial · 🔴 Missing · ⏭ Not yet applicable
Version values: vX.X · draft · YYYY-MM · none (no version = 🟡 Partial regardless of content) · stale (predates upstream change)

---

## Gate Condition — Phase {N}

| Condition | Met? | Evidence | Notes |
| :--- | :--- | :--- | :--- |
| Deliverable exists | | | |
| Deliverable is versioned | | | |
| Gate sign-off obtained | | | |
| Upstream inputs traceable | | | |

**Gate result:** ✅ Pass / 🔴 Fail / 🟡 Conditional pass (conditions listed below)

Conditions for conditional pass:
- {condition 1}
- {condition 2}

---

## Gap Analysis

### Sequencing Violations

{List any downstream phases started before upstream gate was met. Each is a risk, not just a gap.}

| Violation | Risk | Action required |
| :--- | :--- | :--- |
| Phase {X} started before Phase {Y} gate met | {consequence} | {what must be resolved} |

### Missing Elements

{For each 🟡 or 🔴 phase, state the missing element and risk of proceeding.}

| Phase | Missing element | Risk of proceeding |
| :--- | :--- | :--- |
| | | |

---

## Alignment Check Results

Confidence levels: ✅ Aligned · ⚠️ Misaligned · ❓ Cannot assess

| Check | Result | Confidence basis | Finding |
| :--- | :--- | :--- | :--- |
| Requirements → Architecture | | | |
| Requirements → Cost Model | | | |
| Requirements → Security | | | |
| Architecture → Data Model | | | |
| Architecture → Security | | | |
| Architecture → Cost Model | | | |
| Data Model → Security | | | |
| Data Model → Implementation Roadmap | | | |
| Cost Model → Implementation Roadmap | | | |
| Security → Implementation Roadmap | | | |
| Operations Runbook → Architecture | | | |
| Final Review → All phases | | | |
| Document consistency (all phases) | | | |

### Misalignment Details

{One block per ⚠️ finding. Remove section if none.}

```
⚠️ MISALIGNMENT — <Phase A> vs <Phase B>
Found in:   <deliverable or decision>
Conflict:   <what Phase A says> vs <what Phase B says>
Risk:       <consequence if not resolved>
Suggestion: <what needs to change and in which deliverable>
```

### Cannot Assess (❓) — Actions Required

{One entry per ❓ finding. Each becomes a HIGH action in recommendations.}

| Check | Missing artefact or evidence | Action |
| :--- | :--- | :--- |
| | | |

---

## Prioritised Recommendations

| Priority | Action | Why | Deliverable | Owner |
| :--- | :--- | :--- | :--- | :--- |
| BLOCKING | | | | |
| HIGH | | | | |
| MEDIUM | | | | |

Maximum 5 actions. BLOCKING items must be resolved before next phase proceeds.

---

## Sign-Off

| Field | Value |
| :--- | :--- |
| Assessment date | {YYYY-MM-DD} |
| Phase assessed | {N} |
| Gate result | ✅ Pass / 🔴 Fail / 🟡 Conditional |
| Signed off by | {name / role} |
| Next review trigger | {next phase completion / specific event} |
| Open items owner | {name / role} |

---

*This document is a project artefact. Store in `use-case-{id}/test/`. Do not store in the skill repository.*
*Future alignment checks may reference this document as version evidence for Phase {N} deliverables.*
