---
name: executing-tasks
description: >
  Use this skill whenever a workspace task needs executing. Enforces a
  quality-gated workflow — intent, plan, QA, sub-tasks, verify — so no task
  runs without confirmed scope and traceable tests. Triggers: any prompt
  matching '% execute % task %', 'run % task', or '% run % task %' patterns.
  Examples: 'Claude execute the following task: ...', 'run TASK-025',
  'execute the complex task TASK-XXX'. Does NOT trigger on 'start TASK-XXX'
  alone — that belongs to managing-tasks.
---
<!-- version: 1.33 | author: chief-of-droids workspace | last_updated: 2026-04-08 -->

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

**Pattern-based triggers (primary):**

Load this skill when the prompt matches any of:
- `% execute % task %` — e.g. "Claude execute the following task: ..."
- `run % task %` — e.g. "run TASK-025", "run the complex task"
- `% run % task %` — e.g. "Claude run task TASK-XXX"

where `%` matches any text including empty string.

**Opt-in trigger (secondary — after managing-tasks):**

After `start TASK-XXX` transitions a task to 🟡 In Progress, ask exactly once:
> "TASK-XXX is now In Progress. Run executing-tasks workflow, or proceed directly?"

- "workflow" → load this skill, begin at Step 1
- "directly" → stop; user executes ad hoc
- No response or ambiguous → ask once more, then wait

This question fires unconditionally after every `start TASK-XXX` transition.
Task scope appearing self-evident, narrow, or verbatim is not a reason to skip it.

**Does NOT trigger on:**
- `start TASK-XXX` alone — that belongs to managing-tasks
- `my intent is [...]` — too ambiguous

---

## Outer Loop Workflow

**ATDD double-loop structure:**
This workflow enforces two nested loops. Understanding which loop you are in at any
point prevents treating inner-loop success as acceptance.

- **Outer loop (acceptance):** Steps 4a → 4b → 7 → 10. Constitutes the acceptance
  gate. Opened at Step 4a when the user authors verification scenarios; remains open
  until Step 10 closes it via the traceability matrix. A sub-task passing its inner
  loop does not constitute outer-loop acceptance.
- **Inner loop (implementation):** Step 9 per sub-task. Governs implementation
  correctness for each unit of work. Inner-loop green is necessary but not sufficient —
  the outer loop closes only when all scenarios from Step 4a are exercised and pass
  in Step 10.

**TDD inner-loop discipline (Red → Green → Refactor):**
Step 9 enforces the TDD cycle at sub-task granularity, per owned QA row:
- **Red:** State-0 check confirms each owned QA row fails before any change is made.
- **Green:** Write phase is constrained to the minimum change required to pass the current row.
- **Refactor:** Immediately after the sub-task confidence gate passes, a scoped Refactor
  pass cleans the sub-task's output before advancing. Refactor does not touch other sub-tasks.

This cycle is owned by SKILL.md Step 9. The per-pattern inner loop in
`references/subtask-patterns.md` encodes Green and State-0 annotations per task type.

**Workflow state:** The artifacts produced at Steps 2A (confirmed intent), 2B (confirmed
target), 4a (verification scenarios), 4b (acceptance criteria), 6 (approved plan), and 7
(QA suite) are held in context for the remainder of the workflow. They are not written to
disk. If any downstream step references an artifact that appears missing (e.g. after a
session interruption): re-run from the step that produced it. Do not proceed with an
unconfirmed artifact.

**Confidence Derivation Rule (applies at Steps 9 and 10):**
After applying any checklist or test suite, compute confidence from the severity profile of failures:
- Start: 100%
- Any Blocking failure: Confidence = 0% (hard floor — cannot recover in the current run)
- Per Major failure: −20%
- Per Minor failure: −3%
- Report format: `Confidence: [N]% — [B] Blocking / [M] Major / [m] Minor failures`
- Gate: Confidence ≥ 95% is required to advance at Steps 9 and 10; below 95% blocks the current step

Threshold interpretation: ≥ 95% = 0 Blocking + 0 Major + at most 1 Minor failure.

### Step 1 — Extract task context

**Detect TASK-XXX in trigger prompt:**

Scan the triggering prompt for a pattern matching `TASK-` followed by digits (e.g. `TASK-025`).

```
if TASK-XXX found in prompt:
    attempt filesystem:read_text_file on target TASKS.md
    if tool error (not a parsed result):
        ⚠️ TASKS.md could not be read — tool error. Verify file path and MCP server status.
        Stop.
    if TASK-XXX found in TASKS.md:
        extract description, scope, target, origin fields
        scope used for Step 2 intent pre-fill only — retired after Step 2A confirmation
        proceed to Step 2 (Path 1 — TASKS.md context available)
    else:
        ⚠️ TASK-XXX not found in TASKS.md — verify task ID before proceeding.
        Stop.
else:
    proceed to Step 2 (Path 2 — prompt as intent source)
```

No status check on task state. Hard stop only on tool read error or TASK-XXX not found.

### Step 2 — Intent Formulation

Read `references/intent-schema.md` before this step.
If read fails: `⚠️ intent-schema.md could not be read — surface to user and stop before proceeding.`

#### Step 2A — Collect and propose intent (hard gate)

Render **Artifact 1** — the intent input form. Per-path pre-fill behaviour:

**Path 1 (TASKS.md entry found):** before rendering, derive pre-fill values from the extracted entry:
- `action` field: extract primary verb + object from `description`
- `value` field: extract purpose or benefit signal from `scope`
- `actor` pill: pre-select `user` (direct prompt trigger)

Inject derived text as default textarea content. The user may edit any field before submitting.

**Path 2 (no TASKS.md entry):** render with empty `action` and `value` fields. Pre-select `user` on the `actor` pill.
If the trigger prompt contains sufficient description text, pre-fill `action` from it; leave
`value` empty.

**Artifact 1 structure** (render as elicit form):
- Actor pill group: `user` | `System` | `Other` (single-select; `Other` reveals free-text input)
- Action textarea: "What must be done? (verb + object — no file paths or tool names)"
- Value textarea: "What is the observable benefit when this is done? (actor perspective, not implementation state)"
- Submit button: "Propose intent"
- Rendering note: Artifact 1 contains form elements — read `shared/elevate-theme/elevate-artifact.md`
  before building and apply the `applyAll()` inline style pattern. CSS custom properties on
  inputs, textareas, and buttons are prohibited.

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

**Path 1:** use the `target` field from the extracted TASKS.md entry.

**Path 2 (or Path 1 with no target field):** infer from the confirmed action clause —
identify the primary noun object and map it to the most specific matching path in the
workspace (skill file, reference file, repo-level doc, or component). Pre-fill with the
inferred path. If confidence is low, append inline: `*(inferred — verify before confirming)*`

Render **Artifact 2** — the confirm + target form:

**Artifact 2 structure** (render as elicit form):
- Intent sentence textarea: pre-filled with the assembled sentence from Step 2A; user may edit
- Target textarea: pre-filled per derivation rule above; user may edit
- Submit button: "Confirm intent"
- Rendering note: Artifact 2 contains form elements — read `shared/elevate-theme/elevate-artifact.md`
  before building and apply the `applyAll()` inline style pattern. CSS custom properties on
  inputs, textareas, and buttons are prohibited.

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

**Role in the outer loop:** scenarios authored here constitute the acceptance specification.
They open the outer loop and remain the reference point through Steps 4b, 7, and 10.
No scenario may be dropped, merged, or reinterpreted in any downstream step without
returning to this step for explicit user confirmation.

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

**Role in the outer loop:** these criteria are the outer-loop acceptance specification.
They must remain unmet by the current system state until all sub-tasks in Step 9
complete. Agreement here binds Steps 5, 6, 7, and 10 — criteria cannot be silently
revised in any downstream step without returning here for explicit user confirmation.

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
Every test row must cite at least one S[N] from Step 4a in the Scenario column.
A test row with no Scenario reference is invalid and must be removed or reassigned
before the suite is confirmed.

Format: ID | Scenario | Severity | Assertion | Pass condition | Fail condition | Artifact.
Minimum: one test per acceptance criterion.

Assign Severity per the acceptance criterion each test covers:
- Blocking: test covers a criterion whose failure makes the associated verification scenario untestable
- Major: test covers a criterion that partially validates the scenario
- Minor: test covers a style or advisory criterion

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

**QA Row Ownership Table (produce before entering Step 9):**

For each QA row from the Step 7 suite, assign it to the sub-task whose Step 6 plan
output will satisfy its assertion. Produce and surface:

| Sub-task | QA Row IDs | Acceptance criterion IDs |
| :--- | :--- | :--- |
| Sub-task N | QA-X, QA-Y | Criterion IDs from Step 4b |

Derivation rule: match each QA row's assertion target to the sub-task that produces
the output under test.

Constraints:
- Every QA row must map to exactly one sub-task.
- If a QA row's assertion spans multiple sub-tasks' outputs: flag as ambiguous; resolve
  by splitting the row or assigning to the sub-task that produces the primary artifact.
- If a QA row cannot be assigned to any sub-task: plan gap — return to Step 6 before proceeding.

This table is the ownership reference for the State-0 check (Red) and per-row Write
discipline (Green) throughout Step 9.

### Step 9 — Execute sub-task loop

Read `references/subtask-patterns.md`. Apply the inner loop for the classified type.
If read fails: `⚠️ subtask-patterns.md could not be read — surface to user and stop before proceeding.`

**Role in the double loop:** Step 9 is the inner loop. Each sub-task's inner-loop
checklist governs implementation correctness for that unit of work. Inner-loop green
is necessary but not sufficient — it confirms the sub-task is well-formed, not that
the outer acceptance gate has been met. The outer loop closes only at Step 10.

For each sub-task from the Step 6 plan:

**Red — State-0 check (before Write):**
Using the QA Row Ownership Table from Step 8, identify rows owned by this sub-task.
For each owned row:
- `code` or `file-write` type: run the assertion against the current system; confirm
  it returns fail. If any row already passes before changes begin, surface as a
  State-0 anomaly — the sub-task may be redundant or the criterion may need revision.
  Resolve with the user before proceeding.
- `doc`, `skill-authoring`, `framing`, or `research` type: record artifact-absent or
  section-absent as the fail state. One line per row. No execution required.

State before entering Write:
> `"State-0 confirmed for sub-task [N]: [M] rows fail as expected."`

If any row passes unexpectedly: block. State:
> `"State-0 anomaly — QA row [ID] already passes before changes. Resolve before proceeding."`

**Green — per-row Write discipline:**
Work through owned QA rows one at a time:
- Write only the minimum change required to advance the current row from fail to pass.
- Run the Test step; if the row passes, advance to the next owned row.
- Do not speculatively address rows not yet in the current Write cycle.

Follow the inner loop from `references/subtask-patterns.md` for the classified type:
Create tests → Write → Run → Test → Debug → back to Write if failing.
For the **Test step**: apply the **Inner-loop checklist** for the classified pattern
as the formal test gate — not the prose description.
Flag blockers immediately; do not silently skip or work around.
Do not advance to the next sub-task until all Inner-loop checklist items pass.

After the Inner-loop checklist is assessed, apply the Confidence Derivation Rule:
- Confidence ≥ 95%: state the score. Run the Refactor phase (below), then advance to the next sub-task.
- Confidence < 95%: block advancement. State:
  > "Sub-task [N] confidence: [N]% — below 95% gate. Failing items: [list]. Resolve before advancing."

**Refactor — per-sub-task (after confidence gate):**
Immediately after confidence ≥ 95% is confirmed, apply a scoped Refactor pass:
- Permitted: restructure for clarity, remove redundancy, improve naming — within this sub-task's output only.
- Prohibited: any change that touches outputs owned by another sub-task.

After Refactor: re-run this sub-task's owned QA rows. All must still pass before advancing.
If any row fails after Refactor: re-enter the Write phase for that row only; do not reset
the confidence gate unless a new Blocking failure is introduced.

After all sub-tasks complete, surface the Inner Loop QA Report (format defined in
`references/subtask-patterns.md`) covering all sub-tasks:
- All passed → proceed to Step 10 automatically
- Any failure → state adjusted confidence %, wait for explicit user input before proceeding

### Step 10 — Verify

Run every test from the QA suite (Step 7) against all outputs.
Report each: ✅ Pass | ⚠️ Partial | ❌ Fail.

**Traceability matrix (required before confidence computation):**
After all per-test results are reported, produce the following table:

| Scenario | Acceptance criteria | QA tests | Scenario status |
| :--- | :--- | :--- | :--- |
| S[N] from Step 4a | Criterion IDs from Step 4b | Test IDs from Step 7 | ✅ Pass / ❌ Fail |

Rules:
- Scenario status = ✅ only if all QA tests mapped to that scenario pass.
- If any scenario from Step 4a has no QA test mapped to it: block — return to Step 7
  to close the gap before computing confidence. Do not proceed with an unmapped scenario.
- If any scenario status = ❌: the outer loop is not closed. Treat as a Blocking failure
  regardless of the individual test's severity.

After the traceability matrix is confirmed complete and all scenarios are accounted for,
apply the Confidence Derivation Rule using each test's Severity from the Step 7 QA suite:
- Compute and state: `QA suite confidence: [N]%`
- Confidence ≥ 95%: proceed to Step 11.
- Confidence < 95%: treat as suite failure regardless of individual ✅/⚠️ counts —
  return to Step 9 for the failing sub-tasks.

If any ❌: return to Step 9 for the relevant sub-task.
**Retry cap:** if a sub-task returns to Step 9 and fails Step 10 a second time, do not
loop again automatically. Surface:
> "Sub-task [N] has failed verification twice. Options: (1) revise the acceptance
> criterion; (2) revise the plan sub-task; (3) accept residual risk and proceed.
> Which do you prefer?"
Await explicit user choice before proceeding.

If all ✅ or ⚠️ only: surface the full QA report before Step 11.

### Step 11 — Integration Refine

Address any remaining ⚠️ from Step 10. Permitted changes: cross-sub-task consistency
only — wiring, shared references, structural cohesion. No new content introduced here;
per-sub-task quality was addressed in the Step 9 Refactor phase.

Apply targeted fixes; re-run affected tests only.

When all tests ✅:
> "Execution complete. All QA tests pass. Ready for commit."

Prompt user — path-dependent:

**Path 1 (TASKS.md entry was found):**
> "Run 'done TASK-XXX' to close the task in managing-tasks."

**Path 2 (no TASKS.md entry):**
Hand off to managing-tasks in sequence:

1. `add task` — pass the confirmed intent sentence as the task input.
   managing-tasks derives all fields from it.
   Also pass explicitly:
   - description: confirmed intent sentence
   - target: confirmed at Step 2B
   - origin: `session:YYYY-MM-DD "[noun-phrase derived from confirmed intent, title-cased]"`
   Retain the TASK-ID assigned by managing-tasks before proceeding.

2. `done task TASK-XXX` — trigger immediately after `add task` confirms,
   using the TASK-ID retained from step 1.

**Path 2 session-interruption recovery:** if the session ends after `add task` confirms
but before `done task` is called, the task will exist in TASKS.md as 🟡 In Progress with
no corresponding close. On resumption: use the pattern-based trigger with the TASK-ID
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
| Version      | 1.33        |
| Last Updated | 2026-04-08  |
| Status       | Draft       |
