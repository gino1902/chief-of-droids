<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-04-18 -->

# Requirements Capture

This content is loaded when Phase 3 begins — after the collaborative dialogue (Phases 0–2) has produced durable decisions worth preserving.

---

<required-content>

This requirements document should behave like a lightweight PRD without PRD ceremony. Include what planning needs to execute well, and skip sections that add no value for the scope.

Restrict the requirements document to product definition and scope control. Do not include implementation details such as libraries, schemas, endpoints, file layouts, or code structure unless the brainstorm is inherently technical and those details are themselves the subject of the decision.
Reason: implementation details in requirements documents create false constraints that planning must either honor or explicitly override — both outcomes waste effort.

**Required content for non-trivial work:**
- Problem frame
- Concrete requirements or intended behavior with stable IDs
- Scope boundaries
- Success criteria

**Include when materially useful:**
- Key decisions and rationale
- Dependencies or assumptions
- Outstanding questions
- Alternatives considered
- High-level technical direction only when the work is inherently technical and the direction is part of the product/architecture decision

Reason: optional sections that add no planning value inflate document size and reduce signal-to-noise ratio.

</required-content>

<template>

**Document structure:** Use this template and omit clearly inapplicable optional sections:

Template (unfilled):

```markdown
---
date: YYYY-MM-DD
topic: <kebab-case-topic>
---

# <Topic Title>

## Problem Frame
[Who is affected, what is changing, and why it matters]

## Requirements

**[Group Header]**
- R1. [Concrete requirement in this group]
- R2. [Concrete requirement in this group]

**[Group Header]**
- R3. [Concrete requirement in this group]

## Success Criteria
- [How we will know this solved the right problem]

## Scope Boundaries
- [Deliberate non-goal or exclusion]

## Key Decisions
- [Decision]: [Rationale]

## Dependencies / Assumptions
- [Only include if material]

## Outstanding Questions

### Resolve Before Planning
- [Affects R1][User decision] [Question that must be answered before planning can proceed]

### Deferred to Planning
- [Affects R2][Technical] [Question that should be answered during planning or codebase exploration]
- [Affects R2][Needs research] [Question that likely requires research during planning]

## Next Steps
[If `Resolve Before Planning` is empty: Continue in this conversation to outline an implementation plan]
[If `Resolve Before Planning` is not empty: Continue in this conversation to resolve blocking questions before planning]
```

Example (Lightweight — filled):

```markdown
---
date: 2026-04-18
topic: add-csv-export
---

# CSV Export for Report View

## Problem Frame
Users need to share report data with stakeholders who do not have system access. Currently no export path exists.

## Requirements
- R1. Add an Export CSV button to the Report View toolbar.
- R2. Export includes all rows currently visible (respects active filters).
- R3. File is named `report-YYYY-MM-DD.csv` using the export date.

## Success Criteria
- A user can download filtered report data without developer assistance.

## Scope Boundaries
- No Excel (.xlsx) export in this iteration.
- No scheduled or automated exports.

## Next Steps
Continue in this conversation to outline an implementation plan.
```

Example (edge — all questions deferred):

```markdown
---
date: 2026-04-18
topic: notification-redesign
---

# Notification System Redesign

## Problem Frame
Users miss time-sensitive alerts because the current notification model does not distinguish urgency levels.

## Requirements

**Delivery**
- R1. Notifications must support at least two urgency levels: standard and critical.
- R2. Critical notifications must be surfaced immediately regardless of user notification preferences.

**Preferences**
- R3. Users can mute standard notifications per channel.

## Success Criteria
- Critical alerts reach users within 30 seconds of trigger.
- Zero critical notifications suppressed by user preference settings.

## Scope Boundaries
- No SMS or email delivery in this iteration.

## Outstanding Questions

### Resolve Before Planning
_(none)_

### Deferred to Planning
- [Affects R2][Technical] Does the current pub/sub infrastructure support priority queues, or does a new delivery path need to be introduced?
- [Affects R3][Needs research] What notification preference model does the existing user settings module expose?

## Next Steps
Continue in this conversation to outline an implementation plan.
```

</template>

<formatting-rules>

For **Standard** and **Deep** brainstorms, write a requirements document.

For **Lightweight** brainstorms, keep the requirements document compact. Brief alignment means the conversation produced shared understanding with no decisions requiring durable capture — skip requirements document creation in that case.

For very small requirements documents with only 1–3 simple requirements, plain bullet requirements are acceptable. For **Standard** and **Deep** requirements documents, use stable IDs like `R1`, `R2`, `R3` so planning and later review can refer to them unambiguously.

When requirements span multiple distinct concerns, group them under bold topic headers within the Requirements section. The trigger for grouping is distinct logical areas, not item count — even four requirements benefit from headers if they cover three different topics. Group by logical theme (e.g., "Packaging", "Migration and Compatibility", "Contributor Workflow"), not by the order they were discussed. Requirements keep their original stable IDs — numbering does not restart per group. A requirement belongs to whichever group it fits best; do not duplicate it across groups. Skip grouping only when all requirements are about the same thing.

Correct (grouped):

```markdown
**Delivery**
- R1. Notifications support two urgency levels.
- R2. Critical notifications surface immediately.

**Preferences**
- R3. Users can mute standard notifications per channel.
```

Incorrect (ungrouped when topics differ):

```markdown
- R1. Notifications support two urgency levels.
- R2. Critical notifications surface immediately.
- R3. Users can mute standard notifications per channel.
```

Keep the requirements document as short as the scope warrants. Lightweight: 1–2 pages. Standard: 2–4 pages. Deep: no formal limit, but prefer concise.
Reason: short requirements documents are easier to scan during planning — padding creates noise without value.

Ensure `docs/brainstorms/` directory exists before writing.

</formatting-rules>

<completeness-check>

Reason internally before declaring a section complete. Do not surface reasoning in the requirements document.

Before finalising, check:
- What would planning still have to invent if this brainstorm ended now?
- Do any requirements depend on something claimed to be out of scope?
- Are any unresolved items actually product decisions rather than planning questions?
- Did implementation details leak in when they shouldn't have?
- Do any requirements claim that infrastructure is absent without that claim having been verified against the codebase? If so, verify now or label as an unverified assumption.
- Is there a low-cost change that would make this materially more useful?
- Would a visual aid (flow diagram, comparison table, relationship diagram) help a reader grasp the requirements faster than prose alone?

If planning would need to invent product behavior, scope boundaries, or success criteria, the brainstorm is not complete yet.

If the user declines a requirements document, capture key decisions as a brief inline summary in chat instead.

If the conversation produced no durable decisions, do not write a requirements document. Summarise shared understanding in chat instead.

If a required section cannot be filled from the brainstorm, mark it: `> 🔲 To be defined — awaiting further brainstorm.` Do not fabricate content.

</completeness-check>

<outstanding-questions-protocol>

If a requirements document contains outstanding questions:
- Use `Resolve Before Planning` only for questions that truly block planning
- If `Resolve Before Planning` is non-empty, keep working those questions during the brainstorm by default
- If the user explicitly wants to proceed anyway, convert each remaining item into an explicit decision, assumption, or `Deferred to Planning` question before proceeding
- Do not force resolution of technical questions during brainstorming just to remove uncertainty
- Put technical questions, or questions that require validation or research, under `Deferred to Planning` when they are better answered there
- Use tags like `[Needs research]` when the planner should likely investigate the question rather than answer it from repo context alone
- Carry deferred questions forward explicitly rather than treating them as a failure to finish the requirements document

If the user explicitly wants to proceed with `Resolve Before Planning` still populated, convert each remaining item into an explicit decision, assumption, or `Deferred to Planning` question before proceeding.

</outstanding-questions-protocol>

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-04-18 |
| Status       | Draft      |
