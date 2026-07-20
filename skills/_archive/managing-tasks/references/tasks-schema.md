<!-- version: 1.7 | author: chief-of-droids workspace | last_updated: 2026-04-02 -->

# TASKS.md Schema

Canonical format for all TASKS.md files in the workspace.
Read this file before any write operation in the managing-tasks skill.

## Contents

- Target Resolution Order
- File Locations
- Section Structure
- Entry Format
- ID Format
- Status Markers
- Write Authority
- Scope Rules
- Empty File Template
- Example

---

## Target Resolution Order

When determining which TASKS.md to read or write, resolve in this order:

1. **Explicit prompt override** — user names a repo or path directly in the trigger
   (e.g. "add task to slide-gen", "show tasks in workspace/TASKS.md")
   → use the named path, no further resolution needed

2. **CLAUDE.md default** — read the active CLAUDE.md (workspace or repo level)
   and check for a `## Task Management` section declaring a default TASKS.md path
   → use that path if present

3. **Schema fallback** — no prompt override and no CLAUDE.md declaration
   → use `<repo-root>/TASKS.md` relative to the active default repo

Resolution stops at the first match. Never skip to a lower-priority source
if a higher-priority source is available and readable.

---

## File Locations

| Scope | Path |
| :--- | :--- |
| Workspace-level | `workspace/.tasks/TASKS.md` |
| Workspace archive | `workspace/.tasks/archive.md` — append-only; contains all done entries |
| Repo-level | `<repo-root>/TASKS.md` |
| Repo archive | `<repo-root>/archive.md` — append-only; co-located with repo TASKS.md |
| Use-case-level | `<repo-root>/use-case-<id>/TASKS.md` |

Archive path is always `archive.md` in the same directory as the target TASKS.md.
Archive is created automatically on first `done task` if it does not exist.

---

## Section Structure

Every TASKS.md contains exactly these three sections, in this order:

```markdown
## 🔴 Backlog

## 🟡 In Progress

## ✅ Done
```

Empty sections are retained — do not remove them.
The `## ✅ Done` section is always empty post-migration. Done entries live in `archive.md`.

---

## Entry Format

```
- TASK-XXX: [description] | target: [file-or-component] | scope: [note] | origin: [prefix:label] "[title]"
```

Done entries (in archive.md) append a done date:

```
- TASK-XXX: [description] | target: [file-or-component] | scope: [note] | origin: [prefix:label] "[title]" | done: YYYY-MM-DD
```

### Origin field

`origin` records where the task was first identified. Format: `prefix:label "Human-readable title"`.

| Prefix | Label | Title | Example |
| :--- | :--- | :--- | :--- |
| `session` | `YYYY-MM-DD` | Session name as it appears in chat history | `session:2026-03-19 "Setting up Claude framework context"` |
| `findings` | `YYYY-MM-DD` | Findings file descriptor | `findings:2026-03-28 "Workspace session analysis run 1"` |
| `skill` | `skill-name` | Workflow that produced the task | `skill:recommend-skills "Recommend skills workflow"` |

`origin` is set at task creation and is not modified thereafter.
`update task` may not change the `origin` field — it is immutable.

---

## ID Format

- Format: `TASK-` followed by zero-padded three-digit number: `TASK-001`, `TASK-042`
- IDs are unique per TASKS.md file — not globally unique across the workspace
- Increment from the highest existing ID across TASKS.md and archive.md combined

---

## Status Markers

| Marker | Meaning |
| :--- | :--- |
| 🔴 Backlog | Not started |
| 🟡 In Progress | Active |
| ✅ Done | Complete — entry lives in archive.md, not TASKS.md |

---

## Write Authority

Default: propose change, write on approval.

Override: if the active system prompt explicitly declares
`managing-tasks: writes pre-approved`, write immediately after proposing —
no confirmation step required.

Projects that do not declare this override retain the confirmation step.

---

## Scope Rules

- Workspace-level TASKS.md: cross-repo infrastructure, shared skills library work
- Repo-level TASKS.md: shared tasks and cross-use-case work within that repo
- Use-case TASKS.md: tasks scoped to that use-case only
- Write authority is set per project in the system prompt — not per repo or use-case
- `update task` edits `target` and `scope` fields only — `origin` is immutable;
  use `start task` or `done task` for status transitions

---

## Empty File Template

```markdown
# TASKS.md — [repo or use-case name]

## 🔴 Backlog

## 🟡 In Progress

## ✅ Done
```

---

## Example

```markdown
# TASKS.md — chief-of-droids

## 🔴 Backlog
- TASK-002: Author tasks-schema.md reference file | target: skills/managing-tasks/references/ | scope: managing-tasks skill | origin: session:2026-03-19 "Setting up Claude framework context"

## 🟡 In Progress
- TASK-001: Author managing-tasks SKILL.md | target: skills/managing-tasks/ | scope: managing-tasks skill | origin: session:2026-03-19 "Setting up Claude framework context"

## ✅ Done
```

```markdown
# archive.md — chief-of-droids

- TASK-000: Update system prompt skills block | target: Custom Instructions | scope: chief-of-droids | origin: session:2026-03-19 "Setting up Claude framework context" | done: 2026-03-19
```
