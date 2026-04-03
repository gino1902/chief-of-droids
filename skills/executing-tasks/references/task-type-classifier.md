<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-04-03 -->

# Task Type Classifier

Read at Step 3 of the executing-tasks outer loop.
Maps confirmed intent to a primary task type and composing skills.

---

## Classification Rule

Apply the decision table below to the confirmed intent.
Resolve to ONE primary type. If secondary patterns apply, declare them as sub-task
variants within the primary type — do not split into multiple primary types.

If signals are ambiguous (two types match equally): surface both to the user,
ask to confirm primary. One question only.

---

## Decision Table

| Signal in confirmed intent | Primary type | Composing skills |
|:---------------------------|:-------------|:----------------|
| "author skill", "build skill", "new skill", origin prefix `skill:*` | skill-authoring | `creating-skills`, `writing-docs` |
| "write", "draft", "document", "guide", "runbook", "ADR" | doc | `writing-docs` |
| "fetch", "scan", "evaluate", "score", "assess", "research", "survey" | research | domain skill if applicable (e.g. `architecting-data-platforms`, `analyzing-business-cases`) |
| target is `.md` file AND confirmed intent involves writing content to it after research | research+file-write | domain skill + `writing-docs` |
| "build", "implement", "refactor", "fix", "code", target is a code file or repo | code | none by default; add `reviewing-tech-claims` if "verified" in confirmed intent |
| "frame", "challenge framing", "FRAMING.md", "assess-artifacts" | framing | `analyzing-business-cases` |

**research+file-write** is the only recognised compound type. It resolves to:
- primary pattern: research
- secondary pattern: file-write (applied after research phase completes)
- composing skills: both domain research skill + `writing-docs`

---

## Classification Output Format

State before proceeding to Step 4a:

> "Task type: [type].
> Composing skills: [comma-separated list, or 'none beyond managing-tasks'].
> Sub-task pattern: [pattern name from subtask-patterns.md]."

---

## Unclassified Tasks

If no signal matches: default to `doc` pattern (least destructive, most general).
State explicitly:

> "No clear type signal found — defaulting to doc pattern.
> If this is incorrect, confirm the correct type before proceeding."
