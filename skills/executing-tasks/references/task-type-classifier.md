<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-03-30 -->

# Task Type Classifier

Read at Step 2 of the executing-tasks outer loop.
Maps task scope and target signals to a primary task type and composing skills.

---

## Classification Rule

Apply the decision table below to the `scope` and `target` fields of the task entry.
Resolve to ONE primary type. If secondary patterns apply, declare them as sub-task
variants within the primary type — do not split into multiple primary types.

If signals are ambiguous (two types match equally): surface both to the user,
ask to confirm primary. One question only.

---

## Decision Table

| Signal in scope or target | Primary type | Composing skills |
|:--------------------------|:-------------|:----------------|
| "author skill", "build skill", "new skill", origin prefix `skill:*` | skill-authoring | `creating-skills`, `writing-docs` |
| "write", "draft", "document", "guide", "runbook", "ADR", target is `.md` doc | doc | `writing-docs` |
| "fetch", "scan", "evaluate", "score", "assess", "research", "survey" | research | domain skill if applicable (e.g. `architecting-data-platforms`) |
| target is `.md` file AND scope involves writing content to it after research | research+file-write | domain skill + `writing-docs` |
| "build", "implement", "refactor", "fix", "code", target is a code file or repo | code | none by default; add `reviewing-tech-claims` if "verified" in scope |
| "frame", "challenge framing", "FRAMING.md", origin prefix `session:*` + framing language | framing | `analyzing-business-cases` |

**research+file-write** is the only recognised compound type. It resolves to:
- primary pattern: research
- secondary pattern: file-write (applied after research phase completes)
- composing skills: both domain research skill + `writing-docs`

---

## Classification Output Format

State before proceeding to Step 3:

> "Task type: [type].
> Composing skills: [comma-separated list, or 'none beyond managing-tasks'].
> Sub-task pattern: [pattern name from subtask-patterns.md]."

---

## Unclassified Tasks

If no signal matches: default to `doc` pattern (least destructive, most general).
State explicitly:

> "No clear type signal found — defaulting to doc pattern.
> If this is incorrect, confirm the correct type before proceeding."
