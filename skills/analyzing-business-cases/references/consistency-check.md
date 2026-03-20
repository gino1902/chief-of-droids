<!-- version: 1.1 | author: slide-gen workspace | last_updated: 2026-03-11 -->

# Consistency Check

Run at each artifact transition during `assess <use-case-id>`.
Apply only transitions where both artifacts are present.

---

## Confidence Rule

Document maturity affects assessment confidence.
Apply this rule before running any content check:

| Artifact state | Confidence rating |
| :--- | :--- |
| Versioned, dated, no gaps | Complete - use as evidence |
| Present but unversioned or undated | Partial - flag before citing as evidence |
| Present but structurally incomplete (missing sections) | Blocking - content checks suspended until resolved |
| Absent | Missing - skip transition, note in gap table |

A Partial artifact can pass content checks — but the transition result is capped
at Partial regardless of content check outcomes. Never promote to Complete
on unversioned evidence.

---

## FRAMING -> CONSTITUTION

**Maturity check:** apply Confidence Rule to both artifacts before content checks.

Content checks:
- [ ] Use case objective in CONSTITUTION matches FRAMING problem statement
- [ ] Target audience in CONSTITUTION matches FRAMING stakeholder map
- [ ] Architecture Selection Criteria (if present) are traceable to FRAMING constraints
- [ ] No new scope introduced in CONSTITUTION not present in FRAMING

---

## CONSTITUTION -> SlideMap

**Maturity check:** apply Confidence Rule to both artifacts before content checks.

Content checks:
- [ ] Every slide maps to a CONSTITUTION research coverage area or a FRAMING objective
- [ ] No slide introduces a topic excluded by CONSTITUTION
- [ ] Slide density and content type respect CONSTITUTION tone and audience rules

---

## SlideMap -> DeckReady

**Maturity check:** apply Confidence Rule to both artifacts before content checks.

Content checks:
- [ ] Every DeckReady slide matches its SlideMap content brief
- [ ] No content authored beyond what SlideMap specifies
- [ ] Claims flagged [Assumption] in SlideMap remain flagged in DeckReady

---

## Assessment Output Format

For each transition assessed, produce one row:

| Transition | Maturity | Content | Blocking issues |
| :--- | :--- | :--- | :--- |
| FRAMING -> CONSTITUTION | Partial | Pass | CONSTITUTION unversioned |
| CONSTITUTION -> SlideMap | Complete | Fail | Slide 4 not traceable to any coverage area |

Overall rating = lowest rating across all transitions.
Do not proceed to next pipeline stage if any transition is Blocking.
