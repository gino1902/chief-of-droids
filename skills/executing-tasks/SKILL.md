---
name: executing-tasks
description: >
  Executes workspace tasks with quality-gated workflow: intent, plan, QA,
  sub-tasks, verify. Triggers: 'execute TASK-XXX' (existing task), 'execute
  new task' (no prior entry), or opt-in after 'start TASK-XXX'. Not on
  'start TASK-XXX' alone.
---
<!-- version: 1.22 | author: chief-of-droids workspace | last_updated: 2026-04-03 -->

# Executing Tasks Skill

Meta-skill that enforces a repeatable, quality-gated workflow for executing any
workspace task. Orchestrates domain skills — does not implement domain logic itself.

**Scope:** Execution discipline only. State transitions belong to `managing-tasks`.
Domain work belongs to the composing skill matched by the task-type classifier.

---

## Reference Files

- `references/intent-schema.md` — read at Step 2; defines intent sentence structure,
  actor taxonomy, per-path authoring rules, and validation criteria
- `references/challenge-protocol.md` — read at Step 5; defines confidence gate,
  self-assessment question, minimum recommendation, user approval prompt, exit conditions
- `references/subtask-patterns.md` — read at Step 9; defines inner loop per task type
  (code / research / doc / file-write / skill-authoring / framing), each with an inner loop
  and Inner-loop checklist as the formal Test step gate; contains Inner Loop QA Report format,
  severity definitions, and behaviour rule
- `references/composing-skills.md` — read at Step 3; decision table mapping
  confirmed intent and target signals to primary type + composing skills

---

## Meta-Skill Declaration

`executing-tasks` does not implement domain logic. It is an orchestration layer.
When a task's type or confirmed intent matches another skill's trigger, `executing-tasks`
loads that skill and defers to it for the relevant sub-tasks.

Consequence: the `Composes With` table is the primary execution mechanism,
not a secondary reference. Always load the matched composing skill before
entering the sub-task loop.

---

## Trigger Surface

**Primary (opt-in after managing-tasks) — Path 1:**
After `start TASK-XXX` transitions a task to 🟡 In Progress, ask exactly once:
> "Run executing-tasks workflow for TASK-XXX?"

If yes → load this skill and begin at Step 1.
If no → stop; user executes ad hoc.

**Standalone — Path 1:**
- `execute TASK-XXX` — load directly, begin at Step 1
- `run TASK-XXX` — alias

**Standalone — Path 2 (no prior TASKS.md entry):**
- `execute new task` — load directly, begin at Step 1; no TASKS.md lookup
- `run new task` — alias

Path 2 intent, target, and task entry are defined during the workflow.
The task entry is created and closed via managing-tasks at Step 11.

Do NOT trigger on "my intent is [...]" — too ambiguous; conflicts with other skills.
Do NOT trigger on "start TASK-XXX" alone — that belongs to managing-tasks.

---

## Outer Loop Workflow

### Step 1 — Extract task context

**Detect path from trigger:**

If triggered by `execute TASK-XXX`, `run TASK-XXX`, or opt-in after `start TASK-XXX` → **Path 1:**
Read target TASKS.md via Filesystem tool. Extract the TASK-XXX entry.
Fields required: description, scope, target, origin.
Scope is extracted here for Step 2 intent proposal only — it is retired as a
working field after Step 2A confirmation. Do not reference it beyond Step 2A.
Do NOT ask the user to re-describe the task. All context comes from TASKS.md.

If TASK-XXX not found:
> ⚠️ TASK-XXX not found in TASKS.md — verify task ID and status via managing-tasks before proceeding.
Stop.

If task status is not 🟡 In Progress:
> ⚠️ TASK-XXX is not In Progress (current: [status]) — run "start TASK-XXX" first.
Stop.

If triggered by `execute new task` or `run new task` → **Path 2:**
> "No existing task — proceeding to Step 2 for intent formulation."
Proceed directly to Step 2. No TASKS.md lookup.

### Step 2 — Intent Formulation

Read `references/intent-schema.md` before this step.
If read fails: `⚠️ intent-schema.md could not be read — surface to user and stop before proceeding.`

#### Step 2A — Propose intent (hard gate)

Using the authoring rules in `references/intent-schema.md`, propose an intent sentence:

> "As [actor] I need to [action] so that [value]"

Per-path input source:

**Path 1:** derive action from the `description` field; derive value from the `scope` field.
Scope is used here as the value basis and retired after this confirmation.
Do not reference scope beyond this step.

**Path 2:** derive action and value from the trigger prompt text.
If the value clause cannot be inferred, flag it inline:
> "[…so that [inferred value — confirm or revise if incorrect]]"

Validate the proposed intent against `references/intent-schema.md` before presenting.

**Scope retirement:** scope is retired as a working field after this confirmation.
Do not reference it in any downstream step.

**Hard gate:** do not proceed to Step 2B until the user explicitly confirms or
modifies the intent.

#### Step 2B — Confirm or define target (hard gate)

**Path 1:** present the target extracted at Step 1.
> "Confirm this target: [target from TASKS.md]"

**Path 2:** ask the user to define it.
> "Define the target: [file or component this task will modify or produce]"

**Hard gate:** do not proceed to Step 3 until the user explicitly confirms or
defines the target.

### Step 3 — Classify task type

Read `references/composing-skills.md`.
If read fails: `⚠️ composing-skills.md could not be read — surface to user and stop before proceeding.`

Apply decision table to confirmed intent and target.

State classification explicitly before proceeding:
> "Task type: [type]. Composing skills: [list]. Sub-task pattern: [pattern]."

If two types match equally: surface both, ask user to confirm primary.
One question only. Resolution stops further prompting.

### Step 4a — Verification scenario (hard gate)

A verification scenario describes how the task's output will be exercised and what
behaviour is expected — from the actor's perspective. It operates at the functional
level: what triggers, what the actor observes. It does not name files, assertions,
or tool calls — those belong in Step 4b and Step 7.

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
| `Then` describes an observable outcome — system state, data change, or user-visible impact — not an internal quality judgment | Blocking | Return to user with specific gap identified |
| Traceable to task description or confirmed intent | Advisory | Surface to user; does not block acceptance |

If any Blocking criterion fails: surface the specific issue, return the scenario
to the user for correction. Do not accept partial scenarios.

**Hard gate:** do not proceed to Step 4b until all scenarios pass validation and
the user explicitly confirms the set is complete. Silence or partial response is
not confirmation.

### Step 4b — Acceptance criteria (hard gate)

For each confirmed scenario from Step 4a, Claude derives the conditions that must
hold for that scenario to be considered passing. This is where the abstraction
level drops from behaviour to observable state.

Propose to the user:

| Scenario ID | Acceptance criterion |
| :--- | :--- |
| Scenario ID from Step 4a | Exact, observable condition that must hold — file, section, field, or system state |

One or more criteria per scenario. A scenario may generate multiple criteria
if its `Then` clause depends on several independent conditions.

Before presenting, validate each criterion:

| Criterion | Severity | Consequence |
| :--- | :--- | :--- |
| Observable — checkable with a tool call or a read | Blocking | Rework before presenting |
| Unambiguous — only one interpretation of pass/fail | Blocking | Rework before presenting |
| Traceable to its scenario | Blocking | Remove or reassign |

**Hard gate:** do not proceed to Step 5 until the user explicitly confirms or
modifies the acceptance criteria. Acceptance criteria are the evaluation anchor
for Step 5 (challenge) and the constraint frame for Step 6 (plan). They must
be agreed before either step runs.

### Step 5 — Challenge acceptance criteria

Read `references/challenge-protocol.md` before this step.
If read fails: `⚠️ challenge-protocol.md could not be read — surface to user and stop before proceeding.`

Apply the confidence gate exactly as defined there.

**Evaluation anchor:** use the acceptance criteria from Step 4b. A blocking issue
is any gap, contradiction, missing input, or assumption in the acceptance criteria
that would prevent a viable plan from being authored or one or more criteria from
being met.

Do NOT enter Step 6 until the gate exits cleanly:
condition = no new blocking issues in the last round AND user explicitly approves.

### Step 6 — Propose and approve plan

Produce a stepped plan: sub-tasks, actions, outputs per sub-task.
The plan is constrained by the acceptance criteria agreed in Step 4b —
every output of every sub-task must be traceable to at least one criterion.

Close with exactly:
> "Does this plan meet the acceptance criteria agreed in Step 4b?"

Await explicit approval. If user requests changes: revise, re-present, re-close
with the same question. Do not proceed to Step 7 on partial approval.

### Step 7 — Design QA suite

Immediately after plan approval — before any sub-task executes.

**Plan coverage validation (gate before QA authoring):**
For each sub-task from the Step 6 plan, verify:
- Sub-task maps to at least one acceptance criterion from Step 4b
- Sub-task has a defined output

If either check fails for any sub-task: return to Step 6 to revise the plan.
Do not proceed to QA authoring with uncovered or output-less sub-tasks.

**Handoff rule:** expand each acceptance criterion from Step 4b into one or more
full QA test rows. Do not author tests not traceable to a Step 4b criterion.

Format: ID | Assertion | Pass condition | Fail condition | Artifact.
Minimum: one test per acceptance criterion.

After presenting the suite, state confidence before awaiting user confirmation:
> "QA suite confidence: [N]% — [one-line rationale for the score]"

Await user confirmation before proceeding.

The QA suite produced here is the direct input to Step 10 (Verify).
Do not author a separate verification checklist at Step 10.

### Step 8 — Load composing skill(s)

Load each skill from the Composes With table matched in Step 3.
State which skill governs each sub-task before entering the loop:
> "Sub-task [N] governed by: [skill name]."

### Step 9 — Execute sub-task loop

Read `references/subtask-patterns.md`. Apply the inner loop for the classified type.
If read fails: `⚠️ subtask-patterns.md could not be read — surface to user and stop before proceeding.`

For each sub-task from the Step 6 plan:
- Run the inner loop within that sub-task: Create tests → Write → Run → Test → Debug → back to Write if failing
- For the **Test step**: apply the **Inner-loop checklist** for the classified pattern
  from `references/subtask-patterns.md` as the formal test gate — not the prose description
- Flag blockers immediately; do not silently skip or work around
- Do not advance to the next sub-task until all Inner-loop checklist items pass

After all sub-tasks complete, surface the Inner Loop QA Report (format defined in
`references/subtask-patterns.md`) covering all sub-tasks:
- All passed → proceed to Step 10 automatically
- Any failure → state adjusted confidence %, wait for explicit user input before proceeding

### Step 10 — Verify

Run every test from the QA suite (Step 7) against all outputs.
Report each: ✅ Pass | ⚠️ Partial | ❌ Fail.

If any ❌: return to Step 9 for the relevant sub-task. Do not proceed with open failures.
If all ✅ or ⚠️ only: surface the full QA report before Step 11.

### Step 11 — Refine

For any remaining ⚠️: propose targeted fixes, apply, re-run affected tests only.

When all tests ✅:
> "Execution complete. All QA tests pass. Ready for commit."

Prompt user — path-dependent:

**Path 1:**
> "Run 'done TASK-XXX' to close the task in managing-tasks."

**Path 2:**
Hand off to managing-tasks in sequence:

1. `add task` — pass the confirmed intent sentence as the task input.
   managing-tasks derives all fields from it.
   Also pass explicitly:
   - description: confirmed intent sentence.
   - target: confirmed at Step 2B
   - origin: `session:YYYY-MM-DD "[noun-phrase derived from confirmed intent, title-cased]"`
   Retain the TASK-ID assigned by managing-tasks before proceeding.

2. `done task TASK-XXX` — trigger immediately after `add task` confirms,
   using the TASK-ID retained from step 1.

---

## Composes With

| Skill | When | Sub-tasks governed |
| :--- | :--- | :--- |
| `managing-tasks` | Always — task context source (Path 1) and state close (both paths) | Step 1 read (Path 1), Step 11 done (Path 1) / add+done (Path 2) |
| `writing-docs` | Task type = doc | Step 9 inner loop: doc pattern |
| `creating-skills` | Task type = skill-authoring | Step 9 inner loop: skill pattern |
| `reviewing-tech-claims` | Any type where confirmed intent contains "verified" or "tech-checked" | Step 9: verification sub-tasks |
| `architecting-data-platforms` | Task type = research, target involves data platform | Step 9 inner loop: research pattern |
| `analyzing-business-cases` | Task type = framing | Step 9 inner loop: framing pattern — delegates domain work to analyzing-business-cases |

---

## QA Checklist

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


| Field        | Value       |
|--------------|-------------|
| Version      | 1.22        |
| Last Updated | 2026-04-03  |
| Status       | Draft       |
