<!-- version: 1.2 | author: chief-of-droids workspace | last_updated: 2026-04-02 -->

# Intent Schema

Read at Step 2 of the executing-tasks outer loop.
Defines the intent sentence structure, actor taxonomy, per-path authoring rules,
and validation criteria used in the Intent Formulation step.

---

## Purpose

Intent is the working frame for task execution. It supersedes the scope field
value as the active reference once confirmed by the user at Step 2A. It is
session-local — not written to TASKS.md. The git commit is the persistence
mechanism for intent in both paths.

---

## Sentence Structure

```
As [actor] I need to [action] so that [value]
```

| Field | Definition |
| :--- | :--- |
| actor | Who is requesting the action — see Actor Taxonomy below |
| action | Verb + object describing what must be done — specific, bounded |
| value | Observable benefit or outcome that defines success for the actor |

---

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

---

## Per-Path Authoring Rules

### Path 1 — Task from TASKS.md

Input sources:
- `description` field → action basis
- `scope` field → value basis (one-time use; retired as the working reference after
  Step 2A confirmation — see SKILL.md Step 2A for the retirement rule.
  The scope field itself remains in the TASKS.md entry unchanged.)

Authoring steps:
1. Extract the primary verb and object from `description` → compose action clause
2. Extract the purpose or benefit signal from `scope` → compose value clause
3. Determine actor from trigger type (direct prompt = `user`)
4. Validate the full sentence against Validation Rules before presenting

Example:
- description: "Design enforcement mechanism for managing-tasks read display spec"
- scope: "display column spec is unenforced — design options evaluated, approach chosen with rationale"
- Proposed: "As user I need to design an enforcement mechanism for the managing-tasks
  read display spec so that the display column spec has a defined gate and cannot be
  silently violated"

### Path 2 — No prior TASKS.md entry

Input source:
- Free-form trigger prompt text (everything after `execute new task:` or `run new task:`)

If the trigger is bare — `execute new task` with no description following — ask once:
> "What should this task do? Provide a brief description and I will propose an intent."
Await the user's response before proceeding with authoring steps.

Authoring steps:
1. Extract action verb and object from the prompt → compose action clause
2. Infer value clause from the prompt context and implied goal
3. If the value clause cannot be confidently inferred, flag it inline before presenting:
   > "[…so that [inferred value — confirm or revise if incorrect]]"
   Do not block on this — surface the inference and let the hard gate resolve it
4. Determine actor from trigger type (direct prompt = `user`)
5. Validate the full sentence against Validation Rules before presenting

Example:
- trigger prompt: "execute new task: refactor challenge-protocol.md to remove scope references"
- action: "refactor challenge-protocol.md to remove scope references"
- inferred value: "the challenge step is anchored to confirmed intent, not retired scope"
- Proposed: "As user I need to refactor challenge-protocol.md to remove scope references
  so that the challenge step is anchored to confirmed intent, not retired scope"

---

## Validation Rules

Apply to the proposed intent before presenting it to the user.

| Rule | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- |
| Action clause contains verb + object | Blocking | Verb and object both present | Bare verb without object |
| Value clause is non-empty | Blocking | Value present — inferred and flagged is acceptable; absent is not | Value clause missing entirely |
| Value clause states actor-observable benefit — not an implementation state | Blocking | "so that executions start from a shared confirmed purpose" ✅ | "so that the file is updated" ❌ |
| No file paths or tool calls in any field | Blocking | No paths or tool references present | Path or tool name appears in any field |
| Actor is from the defined taxonomy | Blocking | user / System / API \<n\> | Any free-form actor value |

---

## Advisory Note

`System` and `API <n>` are valid taxonomy entries but have no active trigger
path in this workspace today. If either appears in a proposed intent, surface it
to the user for explicit confirmation before proceeding — these actors are unusual
and may indicate a misclassification of the trigger source.


| Field        | Value       |
|--------------|-------------|
| Version      | 1.2         |
| Last Updated | 2026-04-02  |
| Status       | Draft       |
