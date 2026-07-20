<!-- version: 1.5 | author: chief-of-droids workspace | last_updated: 2026-04-13 -->

<purpose>

# Intent Schema

Read at Step 2 of the executing-tasks outer loop.
Defines the intent sentence structure, actor taxonomy, per-path authoring rules,
and validation criteria used in the Intent Formulation step.

**Definition:** Intent is the working frame for task execution.

**Scope boundary:** Intent supersedes the scope field value as the active reference
once confirmed by the user at Step 2A. It is session-local — not written to TASKS.md.

**Persistence:** The git commit is the persistence mechanism for intent in both paths.
Reason: intent is session-local and not written to TASKS.md — the commit message is
the only durable record of what was executed and why, making it the canonical audit
trail for intent across sessions.

Reason internally before proposing an intent sentence. Do not surface derivation
steps in output — present the proposed intent sentence and any inline flags only.

</purpose>

<sentence-structure>

## Sentence Structure

```
As [actor] I need to [action] so that [value]
```

| Field | Definition |
| :--- | :--- |
| actor | Who is requesting the action — see Actor Taxonomy below |
| action | Verb + object describing what must be done — specific, bounded |
| value | Observable benefit or outcome that defines success for the actor |

</sentence-structure>

<actor-taxonomy>

## Actor Taxonomy

Canonical values — use exactly as written:

| Actor | When to use |
| :--- | :--- |
| `user` | Action triggered directly by a user prompt |
| `System` | Action triggered by a rule, workflow, or skill — not a direct user prompt |
| `API <n>` | Action triggered by an external API push — reserved/future; not active in this workspace |

In this workspace, actor is `user` for all direct-prompt executions.
`System` applies when executing-tasks is invoked by an automated rule or workflow.
`API <n>` is reserved — include in validation taxonomy but do not expect it in practice.

</actor-taxonomy>

<per-path-authoring>

## Per-Path Authoring Rules

### Path 1 — Task from TASKS.md

Input sources:
- `description` field → action basis. If the `description` field is absent from the
  TASKS.md entry: halt — "⚠️ TASK-XXX description field missing — cannot derive
  action clause. Update the task entry before proceeding."
- `scope` field → value basis (one-time use; retired as the working reference after
  the user confirms the intent sentence — do not reference scope in any step after
  Step 2A. The scope field itself remains in the TASKS.md entry unchanged.
  Reason: scope is a TASKS.md authoring field, not an executing-tasks working field
  — executing-tasks does not own TASKS.md entries and must not modify them;
  retirement is a session-local designation only.)
  If the `scope` field is absent: proceed to Path 2 step 2 to infer the value clause
  from the description field content.

Authoring steps:
1. Extract the primary verb and object from `description` → compose action clause
2. Extract the purpose or benefit signal from `scope` → compose value clause
3. Determine actor from trigger type (direct prompt = `user`)
4. Validate the intent sentence against Validation Rules before presenting

Correct:
- description: "Design enforcement mechanism for managing-tasks read display spec"
- scope: "display column spec is unenforced — design options evaluated, approach chosen with rationale"
- Proposed intent sentence: "As user I need to design an enforcement mechanism for
  the managing-tasks read display spec so that the display column spec has a defined
  gate and cannot be silently violated"

### Path 2 — No prior TASKS.md entry

Input source:
- Free-form trigger prompt text (everything after `execute new task:` or `run new task:`)

If the trigger is bare — `execute new task` with no description following — ask once:
> "What should this task do? Provide a brief description and I will propose an intent."
Await the user's response before proceeding with authoring steps.
If the user's response still contains no action clause: flag and halt —
"No action clause present. Provide a verb + object description before proceeding."
Do not attempt to infer an action from an empty or undescriptive response.

Authoring steps:
1. Extract action verb and object from the prompt → compose action clause
2. Infer value clause from the prompt context and implied goal.
   Reason: the value clause must reflect the actor's observable benefit — infer from
   the most proximate goal signal in the prompt (outcome noun, purpose phrase, or
   implied state change); when no such signal is present, flag rather than fabricate.
3. If the value clause cannot be inferred from the trigger prompt text alone (no
   stated goal, benefit, or outcome present), flag it inline before presenting:
   > "[…so that [inferred value — confirm or revise if incorrect]]"
   Do not block on this — surface the inference and let the hard gate resolve it
4. Determine actor from trigger type (direct prompt = `user`)
5. Validate the intent sentence against Validation Rules before presenting

Correct:
- trigger prompt: "execute new task: refactor challenge-protocol.md to remove scope references"
- action: "refactor challenge-protocol.md to remove scope references"
- inferred value: "the challenge step is anchored to confirmed intent, not retired scope"
- Proposed intent sentence: "As user I need to refactor challenge-protocol.md to
  remove scope references so that the challenge step is anchored to confirmed intent,
  not retired scope"

Edge case (no goal signal in trigger — value clause flagged):
- trigger prompt: "execute new task: delete temp files in .cache/"
- action: "delete temp files in .cache/"
- no goal, benefit, or outcome stated in prompt
- Proposed intent sentence: "As user I need to delete temp files in .cache/ so that
  [inferred value — confirm or revise if incorrect]"

</per-path-authoring>

<validation-rules>

## Validation Rules

Apply to the proposed intent sentence before presenting it to the user.

| Rule | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- |
| Action clause contains verb + object | Blocking | Verb and object both present | Bare verb without object |
| Value clause is non-empty | Blocking | Value present — inferred and flagged is acceptable; absent is not | Value clause missing entirely |
| Value clause states actor-observable benefit — not an implementation state | Blocking | "so that executions start from a shared confirmed purpose" ✅ | "so that the file is updated" ❌ |
| No file paths or tool calls in any field | Blocking | No paths or tool references present | Path or tool name appears in any field |
| Actor is from the defined taxonomy | Blocking | user / System / API \<n\> | Any free-form actor value |

If a rule outcome is ambiguous — the clause is borderline rather than clearly pass
or fail — treat as fail. Surface the specific clause and the rule it borderlines.
Ask the user to clarify before presenting the intent sentence.

**Worked examples by rule:**

Rule 1 — Action clause contains verb + object:
- Correct: `I need to refactor challenge-protocol.md to remove scope references`
- Incorrect: `I need to refactor` (bare verb, no object)

Rule 2 — Value clause is non-empty:
- Correct: `so that [inferred value — confirm or revise if incorrect]` (flagged inference is acceptable)
- Incorrect: `As user I need to delete temp files` (value clause absent entirely)

Rule 4 — No file paths or tool calls in any field:
- Correct: `I need to update the challenge step documentation`
- Incorrect: `I need to run filesystem:write_file on skills/executing-tasks/references/challenge-protocol.md`

Rule 5 — Actor is from the defined taxonomy:
- Correct: `As user I need to…` / `As System I need to…`
- Incorrect: `As the developer I need to…` (free-form actor value)

</validation-rules>

<advisory-note>

## Advisory Note

`System` and `API <n>` are valid taxonomy entries but have no active trigger
path in this workspace today. If either appears in a proposed intent sentence,
surface it to the user for explicit confirmation before proceeding — these actors
are unusual and may indicate a misclassification of the trigger source.
Reason: System and API <n> actors have no active trigger path in this workspace
— an intent sentence proposing either is almost certainly a misclassification of
a direct user prompt, and proceeding without confirmation would execute the wrong path.

</advisory-note>

| Field        | Value       |
|--------------|-------------|
| Version      | 1.5         |
| Last Updated | 2026-04-13  |
| Status       | Draft       |
