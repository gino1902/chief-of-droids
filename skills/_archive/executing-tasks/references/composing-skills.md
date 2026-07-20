<!-- version: 1.5 | author: chief-of-droids workspace | last_updated: 2026-04-13 -->

<classification-rule>

# Composing Skills

Read at Step 3 of the executing-tasks outer loop.
Maps confirmed intent to a primary task type and composing skills.

## Classification Rule

Apply the decision table below to the confirmed intent.
Evaluate all rows before resolving. Select the row whose signal set most completely
matches the confirmed intent.

If one row matches on more signals than all others: resolve to that row directly.
Do not surface ambiguity to the user.

If one signal is present but weak — appearing as part of a compound phrase where
the primary verb is not a table signal — treat as no match for that row. Apply the
unclassified fallback if no row produces a clean match.

Resolve to ONE primary type. If secondary patterns apply, declare them as sub-task
variants within the primary type.

If signals are ambiguous (two types match equally): surface both to the user,
ask to confirm primary. One question only.
Reason: a single disambiguating question keeps the classification step atomic —
splitting into two questions (primary then secondary) would imply secondary
classification is in scope here, which it is not.

If the user does not select either type or responds ambiguously: ask once more
with the same question. If still unresolved: halt —
"Classification unresolved. Clarify intent before proceeding."

Reason internally before classifying. Do not surface reasoning steps in output —
state the classification result only.

</classification-rule>

<decision-table>

## Decision Table

| Signal in confirmed intent | Primary type | Composing skills |
|:---------------------------|:-------------|:----------------|
| "author skill", "build skill", "new skill", origin prefix `skill:*` | skill-authoring | `creating-skills`, `writing-docs` |
| "write", "draft", "document", "guide", "runbook", "ADR" | doc | `writing-docs` |
| "fetch", "scan", "evaluate", "score", "assess", "research", "survey" | research | domain skill if confirmed target or intent signals a known domain (data platform → `architecting-data-platforms`; use case framing → `analyzing-business-cases`). Reason: domain skill inclusion is signal-driven, not discretionary — include only when the confirmed intent or target contains an explicit domain marker. |
| target is `.md` file AND confirmed intent involves writing content to it after research | research+file-write | domain skill + `writing-docs` |
| "build", "implement", "refactor", "fix", "code", target is a code file or repo | code | none by default; add `reviewing-tech-claims` if "verified" in confirmed intent |
| "frame", "challenge framing", "FRAMING.md", "assess-artifacts" | framing | `analyzing-business-cases` |

**research+file-write** is the only recognised compound type. It resolves to:
- primary pattern: research
- secondary pattern: file-write (applied after research phase completes)
- composing skills: both domain research skill + `writing-docs`

</decision-table>

<output-format>

## Classification Output Format

State before proceeding to Step 4a:

Example:
> "Task type: [type].
> Composing skills: [comma-separated list, or 'none beyond managing-tasks'].
> Sub-task pattern: [pattern name from subtask-patterns.md]."

Example (doc type — writing a runbook):
> "Task type: doc.
> Composing skills: writing-docs.
> Sub-task pattern: doc."

Example (research type — evaluating MCP server options, data platform target):
> "Task type: research.
> Composing skills: architecting-data-platforms.
> Sub-task pattern: research."

Example (skill-authoring type — authoring a new skill):
> "Task type: skill-authoring.
> Composing skills: creating-skills, writing-docs.
> Sub-task pattern: skill-authoring."

Example (ambiguity — "write" and "assess" signals both present equally):
> "Ambiguous classification — two types match equally: doc ('write') and
> research ('assess'). Which is the primary type for this task?"
> Await user confirmation before proceeding. If unresolved after one follow-up:
> halt — "Classification unresolved. Clarify intent before proceeding."

</output-format>

<unclassified-tasks>

## Unclassified Tasks

If no signal matches: default to `doc` type (least destructive, most general).
(doc type maps to the doc sub-task pattern in `subtask-patterns.md`)
State explicitly:

> "No clear type signal found — defaulting to doc type.
> If this is incorrect, confirm the correct type before proceeding."

</unclassified-tasks>

| Field        | Value       |
|--------------|-------------|
| Version      | 1.5         |
| Last Updated | 2026-04-13  |
| Status       | Draft       |
