<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-04-06 -->

# QA Checklist — executing-tasks

Governs: `executing-tasks` skill
Format: executing-tasks severity model (Blocking / Major / Minor)
Placement: Unified — single file; path-exclusive items carry inline path labels
Branch-exclusive ratio: 6 of 42 items are path-specific (14%) — below 50% threshold; unified placement correct

Usage: consulted during mock-request validation or skill assessment — not read during task execution

---

- [ ] **Blocking** — Path detected at Step 1: TASKS.md lookup for Path 1; "No existing task" surfaced for Path 2
- [ ] **Blocking** — Task context read from TASKS.md (Path 1) — user not asked to re-describe
- [ ] **Blocking** — Task status confirmed 🟡 In Progress before proceeding (Path 1 only)
- [ ] **Major** — Intent proposed by Claude from correct input source: description + scope for Path 1; trigger prompt for Path 2
- [ ] **Major** — Path 2 value clause flagged inline if inferred — not silently assumed
- [ ] **Major** — Intent validated against intent-schema.md before presenting
- [ ] **Blocking** — Intent confirmed by user (hard gate) before Step 2B
- [ ] **Major** — Scope not referenced beyond Step 2A
- [ ] **Blocking** — Target confirmed (Path 1) or defined (Path 2) by user (hard gate) before Step 3
- [ ] **Major** — Task type classified explicitly from confirmed intent + target — stated before Step 4a
- [ ] **Major** — Composing skill(s) declared before sub-task loop enters
- [ ] **Major** — Verification scenario schema presented to user — user authored the scenarios
- [ ] **Blocking** — Verification scenario: each user-provided scenario validated against blocking criteria before acceptance
- [ ] **Blocking** — Verification scenario: `Then` clause validated for observability before acceptance — not an internal quality judgment
- [ ] **Blocking** — Verification scenario: blocking failures returned to user with specific issue identified
- [ ] **Blocking** — Verification scenario confirmed complete by user (hard gate) before Step 4b
- [ ] **Major** — Acceptance criteria: one or more criteria per scenario derived by Claude — Scenario ID / Acceptance criterion format
- [ ] **Blocking** — Acceptance criteria: observable, unambiguous, traceable criteria applied — Blocking items resolved before presenting
- [ ] **Blocking** — Acceptance criteria confirmed by user (hard gate) before Step 5
- [ ] **Blocking** — Challenge gate anchored to Step 4b acceptance criteria
- [ ] **Blocking** — Challenge gate exited cleanly — no new blocking issues, user approved
- [ ] **Minor** — Challenge summary emitted before Step 6: N rounds, blocking issues resolved, advisory items open
- [ ] **Major** — Plan constrained by Step 4b acceptance criteria — every sub-task output traceable to a criterion
- [ ] **Major** — Plan closed with "Does this plan meet the acceptance criteria agreed in Step 4b?"
- [ ] **Blocking** — Plan approved explicitly before Step 7
- [ ] **Blocking** — Step 7 plan coverage validated: each sub-task maps to at least one Step 4b criterion and has a defined output before QA authoring begins
- [ ] **Major** — QA suite: each test traceable to a Step 4b acceptance criterion — no untethered tests
- [ ] **Minor** — QA suite confidence % stated with one-line rationale before user confirmation
- [ ] **Blocking** — QA suite designed before any sub-task executes
- [ ] **Major** — QA suite used as direct input to Step 10 — no separate checklist authored at Step 10
- [ ] **Major** — Each sub-task's governing skill declared before execution
- [ ] **Blocking** — Step 9 Test step uses Inner-loop checklist from subtask-patterns.md — not prose description
- [ ] **Blocking** — No sub-task advanced with open Inner-loop checklist failures
- [ ] **Major** — Inner Loop QA Report surfaced after all sub-tasks complete — before Step 10
- [ ] **Blocking** — Step 10 proceeds automatically on all-pass; waits for user input on any failure
- [ ] **Major** — Step 10 QA report surfaced before Step 11
- [ ] **Blocking** — Completion declared only when all tests ✅
- [ ] **Major** — Path 1: user prompted to run 'done TASK-XXX' via managing-tasks
- [ ] **Minor** — Path 2: origin derived from confirmed intent action clause — title-cased noun-phrase
- [ ] **Blocking** — Path 2: TASK-ID returned by `add task` retained before calling `done task`
- [ ] **Blocking** — Path 2: managing-tasks `add task` confirmed before `done task` triggered

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-04-06 |
| Status       | Active     |
