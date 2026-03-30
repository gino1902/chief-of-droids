---
name: managing-tasks
description: >
  Manages TASKS.md files across repos and use-cases — reads, adds, starts,
  completes, and bootstraps task lists. Use when the user says "show tasks",
  "next task", "start task TASK-XXX", "done task TASK-XXX", "add task",
  "update task TASK-XXX", or "bulk update tasks". Also use when the user asks
  what is pending, what to work on next, or wants to record or update a task.
---
<!-- version: 2.0 | author: chief-of-droids workspace | last_updated: 2026-03-30 -->

# Managing Tasks Skill

Manages TASKS.md files at workspace, repo, and use-case level. Maintains task state
across sessions as the primary continuity mechanism for the workspace.

**Scope:** Reading, writing, and bootstrapping TASKS.md files only. Does not
execute tasks — it records and transitions their state.

---

## Reference Files

- `references/tasks-schema.md` — read before any write operation; defines
  canonical TASKS.md structure, entry format, ID format, status markers,
  write authority rules, scope rules, origin field prefixes, and target resolution order
- `references/qa-checklist.md` — read and run before any write operation

---

## Target Resolution

Apply this resolution order at the start of every workflow to determine which
TASKS.md to operate on. Resolution stops at the first match.

**Step A — Explicit prompt override**
If the user names a repo, path, or context in the trigger
(e.g. "add task to slide-gen", "show tasks in workspace/TASKS.md", "tasks for use-case-1"),
use that path directly. No further resolution needed.

**Step B — CLAUDE.md default**
Read the active CLAUDE.md (workspace-level first, then repo-level if routed to a repo).
If a `## Task Management` section is present with a declared default path, use that path.

**Step C — Schema fallback**
No prompt override and no CLAUDE.md declaration:
use `<repo-root>/TASKS.md` relative to the active default repo.

All workflows below reference "determine target TASKS.md" — that means run Steps A → B → C.

---

## Triggers

**Read triggers** (no file write):

| Phrase | Action |
| :--- | :--- |
| "show tasks" | Read and display all tasks from the target TASKS.md |
| "next task" | Read TASKS.md, identify first entry in 🔴 Backlog, propose it |

**Write triggers** (file write per Write Authority rule in `references/tasks-schema.md`):

| Phrase | Action |
| :--- | :--- |
| "start task TASK-XXX" | Move TASK-XXX from 🔴 Backlog → 🟡 In Progress |
| "done task TASK-XXX" | Move TASK-XXX from current section → ✅ Done, append `done: YYYY-MM-DD` |
| "add task" | Propose new entry in correct section, write per authority rule |
| "update task TASK-XXX" | Update `target` and/or `scope` fields of TASK-XXX, write per authority rule |
| "bulk update tasks" | Apply user-provided change list as a diff across multiple tasks, write per authority rule |

---

## Workflow: read tasks

Steps:
1. Determine target TASKS.md (Target Resolution above)
2. Read target TASKS.md via Filesystem tool
   — if Filesystem tool errors, flag: `⚠️ Filesystem tool unavailable — cannot read TASKS.md`
   — if file not found: run **bootstrap workflow** before proceeding
3. Display tasks grouped by section (Backlog / In Progress / Done).
   For each section render a table with these columns — all mandatory, never omit:

   | ID | Description | Target | Origin |
   | :--- | :--- | :--- | :--- |

   Done tasks add a fifth column: **Done**.
   The `scope` field is not displayed in the table — it is available via `update task` only.

---

## Workflow: next task

Steps:
1. Determine target TASKS.md (Target Resolution above)
2. Read target TASKS.md via Filesystem tool
   — if Filesystem tool errors, flag: `⚠️ Filesystem tool unavailable — cannot read TASKS.md`
   — if file not found: run **bootstrap workflow** before proceeding
3. Identify the first entry in 🔴 Backlog — if Backlog is empty, say so and stop
4. Propose the task as a short prose card — intentionally lighter than the full
   `read tasks` table display; includes ID, description, target, and origin.
   Do not render as a table row.
5. Do not start it — wait for explicit "start task TASK-XXX"

---

## Workflow: start task

Steps:
1. Read `references/tasks-schema.md`
2. Determine target TASKS.md (Target Resolution above)
3. Read target TASKS.md (run bootstrap if missing)
   — if Filesystem tool errors, flag and stop
4. Locate TASK-XXX in 🔴 Backlog — if not found, flag and stop
5. Check 🟡 In Progress section: if any task is already present in this file,
   flag the conflict and stop — one active task per TASKS.md file
6. Read `references/qa-checklist.md` and run it
7. Propose the state transition: move entry from 🔴 Backlog → 🟡 In Progress
8. Write per Write Authority rule in `references/tasks-schema.md`
9. Ask once: "Run executing-tasks workflow for TASK-XXX?"
   If yes → load `executing-tasks` skill; it takes over from here.
   If no → stop; task is 🟡 In Progress, user executes ad hoc.

---

## Workflow: done task

Steps:
1. Read `references/tasks-schema.md`
2. Determine target TASKS.md (Target Resolution above)
3. Read target TASKS.md — if Filesystem tool errors, flag and stop
4. Locate TASK-XXX in any non-Done section — if not found, flag and stop
5. Read `references/qa-checklist.md` and run it
6. Propose: move entry to ✅ Done, append `done: YYYY-MM-DD`
7. Write per Write Authority rule in `references/tasks-schema.md`

---

## Workflow: add task

Steps:
1. Read `references/tasks-schema.md`
2. Determine target TASKS.md (Target Resolution above)
3. Read target TASKS.md (run bootstrap if missing)
   — if Filesystem tool errors, flag and stop
4. Determine next available TASK-ID (increment from highest existing ID
   across all sections, including Done)
5. Ask the user for `origin` if not stated in the prompt — propose `session:YYYY-MM-DD`
   using today's date as default; user may override with any valid prefix
6. Read `references/qa-checklist.md` and run it
7. Propose entry in correct section per schema format
8. Write per Write Authority rule in `references/tasks-schema.md`

---

## Workflow: update task

Steps:
1. Read `references/tasks-schema.md`
2. Determine target TASKS.md (Target Resolution above)
3. Read target TASKS.md — if Filesystem tool errors, flag and stop
4. Locate TASK-XXX in any section — if not found, flag and stop
5. Display current entry to the user
6. Ask: "What should change — target, scope, or both?"
7. Read `references/qa-checklist.md` and run it
8. Propose updated entry with only `target: [file-or-component]` and/or
   `scope: [note]` fields modified — description, status, and `origin` are
   not editable via this workflow
9. Write per Write Authority rule in `references/tasks-schema.md`

---

## Workflow: bulk update tasks

Steps:
1. Read `references/tasks-schema.md`
2. Determine target TASKS.md (Target Resolution above)
3. Read target TASKS.md — if Filesystem tool errors, flag and stop
4. Receive user-provided change list (additions, field edits, removals)
5. Read `references/qa-checklist.md` and run it
6. Propose full diff across all affected entries
7. Write per Write Authority rule in `references/tasks-schema.md`

---

## Workflow: bootstrap

Trigger: TASKS.md not found at expected path

Steps:
1. Read `references/tasks-schema.md`
2. Inform the user: "No TASKS.md found at [path] — proposing scaffold from schema"
3. Propose empty TASKS.md using canonical schema structure
4. Write per Write Authority rule in `references/tasks-schema.md`
5. Continue with the original trigger workflow

---

## Composes With

None. This skill manages task state only — it does not compose with doc-writer
or other skills. Task documentation beyond TASKS.md is out of scope.
