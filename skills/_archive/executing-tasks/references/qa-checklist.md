<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-04-06 -->

# QA Checklist — executing-tasks

Governs: `executing-tasks` skill
Format: table (Severity / Maps to / Item / Pass / Fail signal)
Placement: Unified — single file; path-exclusive items carry inline path labels
Branch-exclusive ratio: 6 of 42 items are path-specific (14%) — below 50% threshold; unified placement correct

Usage: consulted during mock-request validation or skill assessment — not read during task execution

---

| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Blocking | Path detection | Path detected at Step 1: TASKS.md lookup for Path 1; "No existing task" surfaced for Path 2 | Correct path stated before Step 2 begins | Path not declared or wrong path followed — halt, re-detect from trigger |
| Blocking | Reference file read | Task context read from TASKS.md (Path 1) — user not asked to re-describe | TASKS.md entry fields extracted via filesystem read; no question posed to user for task description | User asked to re-describe task — halt, read TASKS.md instead |
| Blocking | Hard gate | Task status confirmed 🟡 In Progress before proceeding (Path 1 only) | Status field in TASKS.md entry is 🟡 In Progress at Step 1 | Status not In Progress — surface warning and halt; direct user to run `start TASK-XXX` first |
| Major | Output quality | Intent proposed by Claude from correct input source: description + scope for Path 1; trigger prompt for Path 2 | Path 1: intent derived from description and scope fields; Path 2: intent derived from trigger text | Wrong input source used — flag and re-derive intent from correct source |
| Major | Output quality | Path 2 value clause flagged inline if inferred — not silently assumed | Inferred value clause marked explicitly in proposed intent sentence | Value clause silently assumed — re-propose with inline flag |
| Major | Reference file read | Intent validated against intent-schema.md before presenting | intent-schema.md filesystem read occurs before intent proposal is shown | Intent proposed without reading schema — read schema and re-validate |
| Blocking | Hard gate | Intent confirmed by user (hard gate) before Step 2B | User has explicitly confirmed or modified the proposed intent sentence | Step 2B entered without explicit confirmation — return to gate, await response |
| Major | Output quality | Scope not referenced beyond Step 2A | No reference to `scope` field in Steps 3–11 | Scope referenced after Step 2A — remove reference, flag retirement violation |
| Blocking | Hard gate | Target confirmed (Path 1) or defined (Path 2) by user (hard gate) before Step 3 | User has explicitly confirmed (Path 1) or stated (Path 2) the target | Step 3 entered without target confirmation — return to gate, await response |
| Major | Path detection | Task type classified explicitly from confirmed intent + target — stated before Step 4a | Classification statement present in output before Step 4a begins | Classification absent or stated after Step 4a — re-state before proceeding |
| Major | Output quality | Composing skill(s) declared before sub-task loop enters | Each composing skill named in output before Step 9 loop begins | Loop entered without skill declaration — declare before re-entering |
| Major | Output quality | Verification scenario schema presented to user — user authored the scenarios | Schema block presented to user; scenarios come from user response, not Claude | Claude authored scenarios — discard, present schema and await user input |
| Blocking | Hard gate | Verification scenario: each user-provided scenario validated against blocking criteria before acceptance | All four blocking criteria checked per scenario; no scenario accepted with a failing criterion | Scenario accepted with unresolved blocking criterion — return to user with specific failure identified |
| Blocking | Hard gate | Verification scenario: `Then` clause validated for observability before acceptance — not an internal quality judgment | `Then` clause describes system state, data change, or user-visible impact | `Then` contains internal quality judgment — return specific clause to user for rewrite |
| Blocking | Failure handling | Verification scenario: blocking failures returned to user with specific issue identified | User receives the specific field and criterion that failed — not a generic rejection | Generic rejection issued — re-surface with specific field and criterion |
| Blocking | Hard gate | Verification scenario confirmed complete by user (hard gate) before Step 4b | User has explicitly stated the scenario set is complete | Step 4b entered on silence or partial response — return to gate, await explicit confirmation |
| Major | Output quality | Acceptance criteria: one or more criteria per scenario derived by Claude — Scenario ID / Acceptance criterion format | Table with Scenario ID and Acceptance criterion columns present; every scenario has ≥1 row | Scenario without a criterion row — derive and add before proceeding |
| Blocking | Hard gate | Acceptance criteria: observable, unambiguous, traceable criteria applied — Blocking items resolved before presenting | Each criterion is checkable with a tool call or read; only one pass/fail interpretation exists; traces to its scenario | Blocking validation failure present — rework criterion before presenting |
| Blocking | Hard gate | Acceptance criteria confirmed by user (hard gate) before Step 5 | User has explicitly confirmed or modified the acceptance criteria table | Step 5 entered without explicit confirmation — return to gate, await response |
| Blocking | Hard gate | Challenge gate anchored to Step 4b acceptance criteria | Challenge evaluation uses Step 4b criteria as the evaluation anchor — not task description or intent sentence | Challenge anchored to wrong artifact — re-anchor to Step 4b criteria |
| Blocking | Hard gate | Challenge gate exited cleanly — no new blocking issues, user approved | Last challenge round raised zero new blocking issues AND user explicitly approved | New blocking issue raised in last round OR approval absent — do not enter Step 6 |
| Minor | Output quality | Challenge summary emitted before Step 6: N rounds, blocking issues resolved, advisory items open | Summary line present showing round count, resolved blocking issues, and open advisory items | Summary absent — emit before proceeding to Step 6 |
| Major | Output quality | Plan constrained by Step 4b acceptance criteria — every sub-task output traceable to a criterion | Each sub-task in plan maps to ≥1 Step 4b criterion | Sub-task with no criterion mapping — remove or add criterion before approval |
| Major | Hard gate | Plan closed with "Does this plan meet the acceptance criteria agreed in Step 4b?" | Closing question appears verbatim at end of plan proposal | Closing question absent or paraphrased — re-close with exact wording |
| Blocking | Hard gate | Plan approved explicitly before Step 7 | User has responded with explicit approval or requested changes | Step 7 entered on silence or partial response — return to gate, await explicit approval |
| Blocking | Hard gate | Step 7 plan coverage validated: each sub-task maps to at least one Step 4b criterion and has a defined output before QA authoring begins | Coverage validation output present; every sub-task has criterion mapping and defined output | Sub-task missing criterion mapping or output definition — return to Step 6 to revise plan |
| Major | Output quality | QA suite: each test traceable to a Step 4b acceptance criterion — no untethered tests | Every QA test row references a Step 4b criterion ID | Test row with no criterion reference — add traceability or remove test |
| Minor | Output quality | QA suite confidence % stated with one-line rationale before user confirmation | Confidence percentage and rationale appear before approval prompt | Confidence absent — add before requesting confirmation |
| Blocking | Hard gate | QA suite designed before any sub-task executes | QA suite appears in output and is confirmed before Step 9 loop begins | Sub-task executed before QA suite confirmed — halt, complete QA design first |
| Major | Output quality | QA suite used as direct input to Step 10 — no separate checklist authored at Step 10 | Step 10 runs the QA suite from Step 7 verbatim — no new tests authored | New tests authored at Step 10 — remove; use Step 7 suite only |
| Major | Output quality | Each sub-task's governing skill declared before execution | Governing skill named in output immediately before each sub-task begins | Sub-task begins without skill declaration — declare before re-entering sub-task |
| Blocking | Reference file read | Step 9 Test step uses Inner-loop checklist from subtask-patterns.md — not prose description | Inner-loop checklist rows from subtask-patterns.md applied as test gate | Prose description used as test gate — read subtask-patterns.md and apply checklist |
| Blocking | Hard gate | No sub-task advanced with open Inner-loop checklist failures | All Inner-loop checklist items pass before next sub-task begins | Sub-task advanced with open failure — halt, resolve failure before advancing |
| Major | Output quality | Inner Loop QA Report surfaced after all sub-tasks complete — before Step 10 | Report present in output after last sub-task and before Step 10 begins | Report absent — emit before entering Step 10 |
| Blocking | Path detection | Step 10 proceeds automatically on all-pass; waits for user input on any failure | All-pass: Step 11 entered without prompt; any failure: explicit user input awaited | All-pass triggers user prompt, or failure proceeds without input — correct branching |
| Major | Output quality | Step 10 QA report surfaced before Step 11 | Full QA report with pass/partial/fail per test appears before Step 11 begins | Report absent — emit before entering Step 11 |
| Blocking | Completion condition | Completion declared only when all tests ✅ | "Execution complete" statement appears only after every QA test shows ✅ | Completion declared with open ⚠️ or ❌ — retract completion, return to Step 9 |
| Major | Output quality | Path 1: user prompted to run 'done TASK-XXX' via managing-tasks | Prompt to run `done TASK-XXX` appears in output at Step 11 (Path 1 only) | Prompt absent — add before session close |
| Minor | Output quality | Path 2: origin derived from confirmed intent action clause — title-cased noun-phrase (Path 2 only) | Origin value is a title-cased noun-phrase derived from the confirmed intent action clause | Origin absent or not title-cased — derive and correct |
| Blocking | Hard gate | Path 2: TASK-ID returned by `add task` retained before calling `done task` (Path 2 only) | TASK-ID from managing-tasks `add task` response is captured before `done task` is triggered | `done task` triggered without retaining TASK-ID — halt, retrieve TASK-ID first |
| Blocking | Hard gate | Path 2: managing-tasks `add task` confirmed before `done task` triggered (Path 2 only) | `add task` confirmation present in output before `done task` is called | `done task` called before `add task` confirmed — halt, await `add task` confirmation |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-04-06 |
| Status       | Active     |
