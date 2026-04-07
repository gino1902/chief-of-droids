---
name: executing-tasks
description: >
  Use this skill whenever a workspace task needs executing. Enforces a
  quality-gated workflow — intent, plan, QA, sub-tasks, verify — so no task
  runs without confirmed scope and traceable tests. Triggers: 'execute
  TASK-XXX' (existing task), 'execute new task' (no prior entry), or opt-in
  after 'start TASK-XXX'. Do not wait to be asked — offer this workflow
  automatically after any task transitions to In Progress. Not on 'start
  TASK-XXX' alone.
---
<!-- version: 1.27 | author: chief-of-droids workspace | last_updated: 2026-04-07 -->

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
  confirmed intent and target signals to primary type + composing skills; owns the
  ambiguity-resolution rule for equal-match cases
- `references/qa-checklist.md` — consulted during mock-request validation or skill
  assessment; not read during task execution
- See workspace `CLAUDE.md` §`MCP Tools` and §`File Edits` for known tool behaviour
  and failure modes (POSIX path requirement, `str_replace` silent failure) — not re-stated here.

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

**Workflow state:** The artifacts produced at Steps 2A (confirmed intent), 2B (confirmed
target), 4a (verification scenarios), 4b (acceptance criteria), 6 (approved plan), and 7
(QA suite) are held in context for the remainder of the workflow. They are not written to
disk. If any downstream step references an artifact that appears missing (e.g. after a
session interruption): re-run from the step that produced it. Do not proceed with an
unconfirmed artifact.

### Step 1 — Extract task context

**Detect path from trigger:**

If triggered by `execute TASK-XXX`, `run TASK-XXX`, or opt-in after `start TASK-XXX` → **Path 1:**
Read target TASKS.md via Filesystem tool. Extract the TASK-XXX entry.
Fields required: description, scope, target, origin.
Scope is extracted here for Step 2 intent proposal only — it is retired as a
working field after Step 2A confirmation. Do not reference it beyond Step 2A.
Do NOT ask the user to re-describe the task. All context comes from TASKS.md.

If `filesystem:read_text_file` returns a tool error (not a parsed result):
> ⚠️ TASKS.md could not be read — tool error. Verify the file path and MCP server status before retrying.
Stop. Do not treat as "task not found."

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

#### Step 2A — Collect and propose intent (hard gate)

Render **Artifact 1** — the intent input form. Per-path pre-fill behaviour:

**Path 1:** before rendering, derive pre-fill values from the TASKS.md entry read at Step 1:
- `action` field: extract primary verb + object from `description`
- `value` field: extract purpose or benefit signal from `scope`
- `actor` pill: pre-select `user` (direct prompt trigger)

Inject derived text as default textarea content. The user may edit any field before submitting.

**Path 2:** render with empty `action` and `value` fields. Pre-select `user` on the `actor` pill.
If the trigger prompt contains sufficient description text, pre-fill `action` from it; leave
`value` empty.

**Artifact 1 structure** (render as elicit form):
- Actor pill group: `user` | `System` | `Other` (single-select; `Other` reveals free-text input)
- Action textarea: "What must be done? (verb + object — no file paths or tool names)"
- Value textarea: "What is the observable benefit when this is done? (actor perspective, not implementation state)"
- Submit button: "Propose intent"

On submit, `sendPrompt()` delivers raw field values to Claude. Apply all five blocking
validation rules from `references/intent-schema.md` before proceeding:

| Outcome | Action |
| :--- | :--- |
| Any blocking rule fails | Surface the specific field and violation in chat; ask user to correct and resubmit — do not render Artifact 2 |
| `actor` is `Other` and value resembles `API <n>` | Block: `⚠️ API <n> actor has no active trigger path in this workspace — likely a misclassification. Correct the actor or stop.` Do not render Artifact 2. |
| `actor` is `System` | Surface advisory from intent-schema.md; require explicit user confirmation before rendering Artifact 2 |
| All rules pass | Assemble intent sentence and proceed to Artifact 2 |

Assemble: `"As [actor] I need to [action] so that [value]"`

Validate the assembled sentence against `references/intent-schema.md` before rendering Artifact 2.

**Scope retirement (Path 1):** scope is retired as a working field after the user confirms
the intent sentence. Do not reference it in any downstream step.

#### Step 2B — Confirm intent and target (hard gate)

Before rendering Artifact 2, derive the target proposal:

**Path 1:** use the `target` field from TASKS.md directly.

**Path 2 (or Path 1 with no target field):** infer from the confirmed action clause —
identify the primary noun object and map it to the most specific matching path in the
workspace (skill file, reference file, repo-level doc, or component). Pre-fill with the
inferred path. If confidence is low, append inline: `*(inferred — verify before confirming)*`

Render **Artifact 2** — the confirm + target form:

**Artifact 2 structure** (render as elicit form):
- Intent sentence textarea: pre-filled with the assembled sentence from Step 2A; user may edit
- Target textarea: pre-filled per derivation rule above; user may edit
- Submit button: "Confirm intent"

On submit, `sendPrompt()` delivers both fields to Claude.

If the user edited the intent sentence: re-validate against the five blocking rules before
accepting. Surface any failure and ask to correct; do not proceed with an invalid sentence.

**Hard gate:** do not proceed to Step 3 until both `intent_sentence` and `target` are
non-empty and the user has submitted Artifact 2.

### Step 3 — Classify task type

Read `references/composing-skills.md`.
If read fails: `⚠️ composing-skills.md could not be read — surface to user and stop before proceeding.`

Apply the decision table to confirmed intent and target. Ambiguity resolution rule is
defined in `references/composing-skills.md` — follow it; do not restate here.

State classification explicitly before proceeding:
> "Task type: [type]. Composing skills: [list]. Sub-task pattern: [pattern]."

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

**Submission protocol — one scenario at a time:**
Scenarios are submitted and validated one at a time. After the user submits a scenario,
Claude validates it immediately against the criteria below. If validation passes, Claude
confirms acceptance and asks: "Add another scenario, or confirm the set is complete?"
If validation fails, Claude returns the scenario with the specific field and issue
identified — the user corrects and resubmits that scenario before any further scenarios
are accepted. Claude does not accept a new scenario while a correction is pending.

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
If user requests changes:
- If the objection is with the criteria themselves → return to Step 4b, revise criteria,
  re-derive the QA suite from the updated criteria, re-present.
- If the objection is with the test expansion (a Claude authoring error) → revise the
  affected test rows, re-present the full suite, re-confirm before proceeding.
Do not proceed on partial approval.

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

If any ❌: return to Step 9 for the relevant sub-task.
**Retry cap:** if a sub-task returns to Step 9 and fails Step 10 a second time, do not
loop again automatically. Surface:
> "Sub-task [N] has failed verification twice. Options: (1) revise the acceptance
> criterion; (2) revise the plan sub-task; (3) accept residual risk and proceed.
> Which do you prefer?"
Await explicit user choice before proceeding.

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

**Path 2 session-interruption recovery:** if the session ends after `add task` confirms
but before `done task` is called, the task will exist in TASKS.md as 🟡 In Progress with
no corresponding close. On resumption: use `execute TASK-XXX` (Path 1) with the TASK-ID
from the `add task` confirmation, skip to Step 11, and call `done task TASK-XXX`.

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

| Field        | Value       |
|:-------------|:------------|
| Version      | 1.27        |
| Last Updated | 2026-04-07  |
| Status       | Draft       |
