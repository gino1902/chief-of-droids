<!-- version: 1.2 | author: chief-of-droids workspace | last_updated: 2026-03-19 -->

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
| Workspace-level | `workspace/TASKS.md` |
| Repo-level | `<repo-root>/TASKS.md` |
| Use-case-level | `<repo-root>/use-case-<id>/TASKS.md` |

---

## Section Structure

Every TASKS.md contains exactly these three sections, in this order:

```markdown
## 🔴 Backlog

## 🟡 In Progress

## ✅ Done
```

Empty sections are retained — do not remove them.

---

## Entry Format

```
- TASK-XXX: [description] | target: [file-or-component] | scope: [note]
```

Done entries append a done date:

```
- TASK-XXX: [description] | target: [file-or-component] | scope: [note] | done: YYYY-MM-DD
```

---

## ID Format

- Format: `TASK-` followed by zero-padded three-digit number: `TASK-001`, `TASK-042`
- IDs are unique per TASKS.md file — not globally unique across the workspace
- Increment from the highest existing ID in the file (including Done section)

---

## Status Markers

| Marker | Meaning |
| :--- | :--- |
| 🔴 Backlog | Not started |
| 🟡 In Progress | Active — only one per file |
| ✅ Done | Complete |

Active is defined as 🟡 In Progress only. Any other state is not active.

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
- One active task (🟡 In Progress) per TASKS.md file — starting a second requires
  closing or moving the current one first
- Write authority is set per project in the system prompt — not per repo or use-case
- `update task` edits `target` and `scope` fields only — use `start task` or
  `done task` for status transitions

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
- TASK-002: Author tasks-schema.md reference file | target: skills/managing-tasks/references/ | scope: managing-tasks skill

## 🟡 In Progress
- TASK-001: Author managing-tasks SKILL.md | target: skills/managing-tasks/ | scope: managing-tasks skill

## ✅ Done
- TASK-000: Update system prompt skills block | target: Custom Instructions | scope: chief-of-droids | done: 2026-03-19
```
