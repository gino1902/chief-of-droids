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
<!-- version: 1.10 | author: chief-of-droids workspace | last_updated: 2026-03-31 -->

# Executing Tasks Skill

Meta-skill that enforces a repeatable, quality-gated workflow for executing any
workspace task. Orchestrates domain skills — does not implement domain logic itself.

**Scope:** Execution discipline only. State transitions belong to `managing-tasks`.
Domain work belongs to the composing skill matched by the task-type classifier.

---

## Reference Files

- `references/challenge-protocol.md` — read at Step 3; defines confidence gate,
  self-assessment question, minimum recommendation, user approval prompt, exit conditions
- `references/subtask-patterns.md` — read at Step 7; defines inner loop per task type
  (code / research / doc / file-write), each with steps and Inner-loop checklist as the
  formal Test step gate; contains Inner Loop QA Report format, severity definitions,
  and behaviour rule
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

### Step 2a — Verification scenario (hard gate)

A verification scenario describes how the task's output will be exercised and what
behaviour is expected — from the actor's perspective. It operates at the functional
level: what triggers, what the actor observes. It does not name files, assertions,
or tool calls — those belong in Step 2b and Step 5.

Present the schema to the user and ask them to author the scenarios:

> "Please provide one or more verification scenarios using this schema:
>
> ```
> S[N]
> Given: [what is true before the trigger fires]
> When:  [single trigger — one action or event only]
> Then:  [observable system result] and/or [data change] and/or [user-visible impact]
> ```
>
> One block per distinct functional behaviour introduced or changed by this task.
> A single When per scenario — if you have a compound trigger, split it into two scenarios."

On receipt, validate each user-provided scenario against these criteria before
accepting it:

| Criterion | Severity | Action on failure |
| :--- | :--- | :--- |
| No file paths, tool calls, or assertions in any field | Blocking | Return to user with specific field flagged |
| `When` contains exactly one trigger | Blocking | Return to user; ask to split |
| `Given` describes system or data state — not storage, tools, or implementation | Blocking | Return to user with specific gap identified |
| Traceable to task description or scope | Advisory | Surface to user; does not block acceptance |

If any Blocking criterion fails: surface the specific issue, return the scenario
to the user for correction. Do not accept partial scenarios.

**Hard gate:** do not proceed to Step 2b until all scenarios pass validation and
the user explicitly confirms the set is complete. Silence or partial response is
not confirmation.

### Step 2b — Acceptance criteria (hard gate)

For each confirmed scenario from Step 2a, Claude derives the conditions that must
hold for that scenario to be considered passing. This is where the abstraction
level drops from behaviour to observable state.

Propose to the user:

| Scenario ID | Acceptance criterion |
| :--- | :--- |
| Scenario ID from Step 2a | Exact, observable condition that must hold — file, section, field, or system state |

One or more criteria per scenario. A scenario may generate multiple criteria
if its `Then` clause depends on several independent conditions.

Before presenting, validate each criterion:

| Criterion | Severity | Consequence |
| :--- | :--- | :--- |
| Observable — checkable with a tool call or a read | Blocking | Rework before presenting |
| Unambiguous — only one interpretation of pass/fail | Blocking | Rework before presenting |
| Traceable to its scenario | Blocking | Remove or reassign |

**Hard gate:** do not proceed to Step 3 until the user explicitly confirms or
modifies the acceptance criteria. Acceptance criteria are the evaluation anchor
for Step 3 (challenge) and the constraint frame for Step 4 (plan). They must
be agreed before either step runs.

### Step 3 — Challenge intent and scope

Read `references/challenge-protocol.md` before this step.
Apply the confidence gate exactly as defined there.

**Evaluation anchor:** use the acceptance criteria from Step 2b. A blocking issue
is any gap, contradiction, missing input, or assumption that would prevent one or
more acceptance criteria from being met.

Do NOT enter Step 4 until the gate exits cleanly:
condition = no new blocking issues in the last round AND user explicitly approves.

### Step 4 — Propose and approve plan

Produce a stepped plan: phases, actions, outputs per phase.
The plan is constrained by the acceptance criteria agreed in Step 2b —
every output of every phase must be traceable to at least one criterion.

Close with exactly:
> "Does this plan meet the acceptance criteria agreed in Step 2b?"

Await explicit approval. If user requests changes: revise, re-present, re-close
with the same question. Do not proceed to Step 5 on partial approval.

### Step 5 — Design QA suite

Immediately after plan approval — before any sub-task executes.

**Handoff rule:** expand each acceptance criterion from Step 2b into one or more
full QA test rows. Do not author tests not traceable to a Step 2b criterion.

Format: ID | Assertion | Pass condition | Fail condition | Artifact.
Minimum: one test per acceptance criterion.

After presenting the suite, state confidence before awaiting user confirmation:
> "QA suite confidence: [N]% — [one-line rationale for the score]"

Await user confirmation before proceeding.

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
- For the **Test step**: apply the **Inner-loop checklist** for the classified pattern
  from `references/subtask-patterns.md` as the formal test gate — not the prose description
- Flag blockers immediately; do not silently skip or work around
- Do not advance to the next sub-task until all Inner-loop checklist items pass

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
- [ ] Task type classified explicitly and stated before Step 2a
- [ ] Composing skill(s) declared before sub-task loop enters
- [ ] Verification scenario schema presented to user — user authored the scenarios
- [ ] Verification scenario: each user-provided scenario validated against blocking criteria before acceptance
- [ ] Verification scenario: blocking failures returned to user with specific issue identified
- [ ] Verification scenario confirmed complete by user (hard gate) before Step 2b
- [ ] Acceptance criteria: one or more criteria per scenario derived by Claude — Scenario ID / Acceptance criterion format
- [ ] Acceptance criteria: observable, unambiguous, traceable criteria applied — Blocking items resolved before presenting
- [ ] Acceptance criteria confirmed by user (hard gate) before Step 3
- [ ] Challenge gate anchored to Step 2b acceptance criteria
- [ ] Challenge gate exited cleanly — no new blocking issues, user approved
- [ ] Plan constrained by Step 2b acceptance criteria — every phase output traceable to a criterion
- [ ] Plan closed with "Does this plan meet the acceptance criteria agreed in Step 2b?"
- [ ] Plan approved explicitly before QA suite design
- [ ] QA suite: each test traceable to a Step 2b acceptance criterion — no untethered tests
- [ ] QA suite confidence % stated with one-line rationale before user confirmation
- [ ] QA suite designed before any sub-task executes
- [ ] QA suite used as direct input to Step 8 — no separate checklist authored at Step 8
- [ ] Each sub-task's governing skill declared before execution
- [ ] Step 7 Test step uses Inner-loop checklist from subtask-patterns.md — not prose description
- [ ] No sub-task advanced with open Inner-loop checklist failures
- [ ] Inner Loop QA Report surfaced after all sub-tasks complete — before Step 8
- [ ] Step 8 proceeds automatically on all-pass; waits for user input on any failure
- [ ] Step 8 QA report surfaced before Step 9
- [ ] Completion declared only when all tests ✅
- [ ] User prompted to close task via managing-tasks
