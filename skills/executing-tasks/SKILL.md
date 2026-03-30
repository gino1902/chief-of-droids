---
name: executing-tasks
description: >
  Meta-skill that governs the end-to-end execution of a workspace task with
  enforced quality and determinism — from intent extraction through challenge,
  plan, QA suite, sub-task execution, verification, and refinement. Load this
  skill after `start TASK-XXX` transitions a task to In Progress and the user
  confirms execution, or when the user says "execute TASK-XXX". Does NOT manage
  task state (that is managing-tasks), does NOT implement domain logic (that is
  the composing skill for the task type). Orchestrates other skills; always
  declares which skill handles each sub-task. Triggers on: "execute TASK-XXX",
  or opt-in confirmation after "start TASK-XXX".
---
<!-- version: 1.2 | author: chief-of-droids workspace | last_updated: 2026-03-30 -->

# Executing Tasks Skill

Meta-skill that enforces a repeatable, quality-gated workflow for executing any
workspace task. Orchestrates domain skills — does not implement domain logic itself.

**Scope:** Execution discipline only. State transitions belong to `managing-tasks`.
Domain work belongs to the composing skill matched by the task-type classifier.

---

## Reference Files

- `references/challenge-protocol.md` — read at Step 3; defines confidence gate,
  self-assessment question, minimum recommendation, user approval prompt, exit conditions
- `references/subtask-patterns.md` — read at Steps 4 and 7; defines inner loop per task type
  (code / research / doc / file-write), each with steps and verify checklist used as
  input to the verification scenario definition at Step 4; contains Inner Loop QA Report
  format, severity definitions, and behaviour rule
- `references/task-type-classifier.md` — read at Step 2; decision table mapping
  task scope/target/origin signals to primary type + composing skills

---

## Meta-Skill Declaration

`executing-tasks` does not implement domain logic. It is an orchestration layer.
When a task's type or scope matches another skill's trigger, `executing-tasks`
loads that skill and defers to it for the relevant sub-tasks.

Consequence: the `Composes With` table is the primary execution mechanism,
not a secondary reference. Always load the matched composing skill before
entering the sub-task loop.

---

## Trigger Surface

**Primary (opt-in after managing-tasks):**
After `start TASK-XXX` transitions a task to 🟡 In Progress, ask exactly once:
> "Run executing-tasks workflow for TASK-XXX?"

If yes → load this skill and begin at Step 1.
If no → stop; user executes ad hoc.

**Standalone:**
- `execute TASK-XXX` — load directly, begin at Step 1
- `run TASK-XXX` — alias

Do NOT trigger on "my intent is [...]" — too ambiguous; conflicts with other skills.
Do NOT trigger on "start TASK-XXX" alone — that belongs to managing-tasks.

---

## Outer Loop Workflow

### Step 1 — Extract task context from TASKS.md

Read target TASKS.md via Filesystem tool. Extract the TASK-XXX entry.
Fields required: description, scope, target, origin.

Do NOT ask the user to re-describe the task. All context comes from TASKS.md.

If TASK-XXX not found:
> ⚠️ TASK-XXX not found in TASKS.md — verify task ID and status via managing-tasks before proceeding.
Stop.

If task status is not 🟡 In Progress:
> ⚠️ TASK-XXX is not In Progress (current: [status]) — run "start TASK-XXX" first.
Stop.

### Step 2 — Classify task type

Read `references/task-type-classifier.md`.
Apply decision table to scope and target fields.

State classification explicitly before proceeding:
> "Task type: [type]. Composing skills: [list]. Sub-task pattern: [pattern]."

If two types match equally: surface both, ask user to confirm primary.
One question only. Resolution stops further prompting.

### Step 3 — Challenge intent and scope

Read `references/challenge-protocol.md` before this step.
Apply the confidence gate exactly as defined there.

Do NOT enter Step 4 until the gate exits cleanly:
condition = no new blocking issues in the last round AND user explicitly approves.

### Step 4 — Propose and approve plan

Produce a stepped plan: phases, actions, outputs per phase.

**Final subset of the plan — Verification scenario (mandatory):**

Read `references/subtask-patterns.md`. Use the verify checklist for the classified
task type as input. Propose a verification scenario: what will be checked after all
sub-tasks complete, how it will be checked, and what constitutes a high-confidence pass.

Always include a confidence level % for the proposed scenario:
> "Verification scenario confidence: [N]% — [one-line rationale for the score]"

Challenge the scenario before presenting the full plan:
- Is the scenario testing outcomes or process steps? (Outcomes only — process steps are not valid scenario items)
- Does each item have a concrete, observable pass condition?
- Is the confidence level justified? Surface any factors that reduce it below 90%

Loop until both Claude and user are satisfied the scenario will provide high-confidence verification.
The plan is not presented for approval until the verification scenario is agreed.

Present the full plan including the agreed verification scenario.
Close with exactly:
> "Does this plan and verification scenario meet your confidence bar?"

Await explicit approval. If user requests changes: revise, re-present, re-close with the same question.
Do not proceed to Step 5 on partial approval.

### Step 5 — Design QA suite

Immediately after plan approval — before any sub-task executes.

The QA suite is scoped to the verification scenario agreed in Step 4 exclusively.
Outer loop procedural steps (Steps 1–4, 6) are excluded.
Inner loop procedural steps (Create tests, Run, Debug) are excluded.
Only the verification scenario items from Step 4 generate QA tests.

Format: ID | Assertion | Pass condition | Fail condition | Artifact.
Minimum: one test per verification scenario item.
Present suite to user. Await confirmation before proceeding.

The QA suite produced here is the direct input to Step 8 (Verify).
Do not author a separate verification checklist at Step 8.

### Step 6 — Load composing skill(s)

Load each skill from the Composes With table matched in Step 2.
State which skill governs each sub-task before entering the loop:
> "Sub-task [N] governed by: [skill name]."

### Step 7 — Execute sub-task loop

Read `references/subtask-patterns.md`. Apply the inner loop for the classified type.

For each sub-task:
- Apply inner loop: Create tests → Write → Run → Test → Debug → back to Write if failing
- Flag blockers immediately; do not silently skip or work around
- Do not advance to the next sub-task until the current one passes its inner test gate

After all sub-tasks complete, surface the Inner Loop QA Report (format defined in
`references/subtask-patterns.md`) covering all sub-tasks:
- All passed → proceed to Step 8 automatically
- Any failure → state adjusted confidence %, wait for explicit user input before proceeding

### Step 8 — Verify

Run every test from the QA suite (Step 5) against all outputs.
Report each: ✅ Pass | ⚠️ Partial | ❌ Fail.

If any ❌: return to Step 7 for the relevant sub-task. Do not proceed with open failures.
If all ✅ or ⚠️ only: surface the full QA report before Step 9.

### Step 9 — Refine

For any remaining ⚠️: propose targeted fixes, apply, re-run affected tests only.

When all tests ✅:
> "Execution complete. All QA tests pass. Ready for commit."

Prompt user:
> "Run 'done TASK-XXX' to close the task in managing-tasks."

---

## Composes With

| Skill | When | Sub-tasks governed |
| :--- | :--- | :--- |
| `managing-tasks` | Always — task context source and state close | Step 1 (read), Step 9 (done prompt) |
| `writing-docs` | Task type = doc | Step 7 inner loop: doc pattern |
| `creating-skills` | Task type = skill-authoring (origin prefix: skill:*) | Step 7 inner loop: skill pattern |
| `reviewing-tech-claims` | Any type where scope contains "verified" or "tech-checked" | Step 7: verification sub-tasks |
| `architecting-data-platforms` | Task type = research, target involves data platform | Step 7 inner loop: research pattern |
| `analyzing-business-cases` | Task type = framing | Step 7 inner loop: framing sub-tasks |

---

## QA Checklist

- [ ] Task context read from TASKS.md — user not asked to re-describe
- [ ] Task status confirmed 🟡 In Progress before proceeding
- [ ] Task type classified explicitly and stated before Step 3
- [ ] Composing skill(s) declared before sub-task loop enters
- [ ] Challenge gate exited cleanly — no new blocking issues, user approved
- [ ] Verification scenario proposed with confidence % and rationale before plan approval
- [ ] Verification scenario challenged for outcome-vs-process and observable pass conditions
- [ ] Plan closed with "Does this plan and verification scenario meet your confidence bar?"
- [ ] Plan approved explicitly before QA suite design
- [ ] QA suite scoped to verification scenario items only — outer and inner loop procedural steps excluded
- [ ] QA suite designed before any sub-task executes
- [ ] QA suite used as direct input to Step 8 — no separate checklist authored at Step 8
- [ ] Each sub-task's governing skill declared before execution
- [ ] No sub-task advanced with open inner test failures
- [ ] Inner Loop QA Report surfaced after all sub-tasks complete — before Step 8
- [ ] Step 8 proceeds automatically on all-pass; waits for user input on any failure
- [ ] Step 8 QA report surfaced before Step 9
- [ ] Completion declared only when all tests ✅
- [ ] User prompted to close task via managing-tasks
