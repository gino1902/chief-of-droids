---
name: managing-tasks
description: >
  Manages TASKS.md files across repos and use-cases — reads, adds, starts,
  completes, and bootstraps task lists. Use when the user says "show tasks",
  "next task", "start task TASK-XXX", "done task TASK-XXX", "add task",
  "update task TASK-XXX", "bulk update tasks", or "show archive". Also use
  when the user asks what is pending, what to work on next, or wants to record
  or update a task.
---
<!-- version: 2.4 | author: chief-of-droids workspace | last_updated: 2026-04-02 -->

# Managing Tasks Skill

Manages TASKS.md files at workspace, repo, and use-case level. Maintains task state
across sessions as the primary continuity mechanism for the workspace.

**Scope:** Reading, writing, and bootstrapping TASKS.md files only. Does not
execute tasks — it records and transitions their state.

**Archive:** Done entries are appended to `archive.md` (co-located with TASKS.md).
The ✅ Done section of TASKS.md is always empty post-migration. Use `show archive`
to retrieve done history.

---

## Reference Files

- `references/tasks-schema.md` — read before any write operation; defines
  canonical TASKS.md structure, entry format, ID format, status markers,
  write authority rules, scope rules, origin field prefixes, and target resolution order
- `references/qa-checklist.md` — read and run before any write operation

---

## Caller Context

This skill is invoked by two caller types. Behaviour differs at steps that
would otherwise prompt the user:

| Caller | How to detect | Behaviour on ambiguous fields |
| :--- | :--- | :--- |
| User | Direct prompt in chat | Ask the user for missing fields |
| Skill | Structured field payload passed in-session by a composing skill (e.g. `executing-tasks`) | Use provided field values directly — do not ask the user |

If a field is absent in a skill call: surface the gap to the orchestrating skill,
not to the user. The orchestrating skill is responsible for resolving it.

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
Archive path is always `archive.md` co-located in the same directory as the target TASKS.md.

---

## Triggers

**Read triggers** (no file write):

| Phrase | Action |
| :--- | :--- |
| "show tasks" | Read and display Backlog and In Progress from the target TASKS.md |
| "next task" | Read TASKS.md, identify first entry in 🔴 Backlog, propose it |
| "show archive" | Read archive.md and display all done entries |

**Write triggers** (file write per Write Authority rule in `references/tasks-schema.md`):

| Phrase | Action |
| :--- | :--- |
| "start task TASK-XXX" | Move TASK-XXX from 🔴 Backlog → 🟡 In Progress |
| "done task TASK-XXX" | Remove TASK-XXX from current section, append to archive.md with `done: YYYY-MM-DD` |
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
3. Display tasks grouped by section (Backlog / In Progress only — Done section is always empty).
   For each section render a table with these columns — all mandatory, never omit:

   | ID | Description | Target | Origin |
   | :--- | :--- | :--- | :--- |

   The `scope` field is not displayed in the table — it is available via `update task` only.
   To view done history, use `show archive`.

---

## Workflow: show archive

Steps:
1. Determine archive path: same directory as target TASKS.md, filename `archive.md`
2. Read archive.md via Filesystem tool
   — if file not found, surface: `⚠️ No archive found at [path]`
3. Display all entries as a table:

   | ID | Description | Target | Origin | Done |
   | :--- | :--- | :--- | :--- | :--- |

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
5. Read `references/qa-checklist.md` and run it
6. Propose the state transition: move entry from 🔴 Backlog → 🟡 In Progress
7. Write per Write Authority rule in `references/tasks-schema.md`
8. Ask once: "Run executing-tasks workflow for TASK-XXX?"
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
6. Propose: remove entry from TASKS.md, append to archive.md with `done: YYYY-MM-DD`
7. Write TASKS.md (entry removed) per Write Authority rule
8. Append entry to archive.md — create archive.md with `# Archive` header if it does not exist

---

## Workflow: add task

Steps:
1. Read `references/tasks-schema.md`
2. Determine target TASKS.md (Target Resolution above)
3. Read target TASKS.md (run bootstrap if missing)
   — if Filesystem tool errors, flag and stop
4. Determine next available TASK-ID — increment from highest existing ID
   across all sections in TASKS.md and archive.md combined
5. Resolve `origin` field:
   - Skill call: use the `origin` value provided in the call payload directly —
     do not ask the user
   - User call: if `origin` not stated in the prompt, propose `session:YYYY-MM-DD`
     using today's date as default; user may override with any valid prefix
6. Resolve remaining fields (description, target) from the call payload or prompt.
   For skill calls: use provided values directly.
   For user calls: derive from the prompt; ask if ambiguous.
7. Read `references/qa-checklist.md` and run it
8. Propose and write entry:
   - User call: propose entry in correct section per schema format; await confirmation
     per Write Authority rule in `references/tasks-schema.md`
   - Skill call: write entry directly — no proposal step; field values are
     already confirmed by the orchestrating skill
9. Return the assigned TASK-ID to the caller — surface explicitly:
    > "Task created: TASK-XXX"
    Skill callers must retain this ID before proceeding.

---

## Workflow: update task

Steps:
1. Read `references/tasks-schema.md`
2. Determine target TASKS.md (Target Resolution above)
3. Read target TASKS.md — if Filesystem tool errors, flag and stop
4. Locate TASK-XXX in any section — if not found, check archive.md before flagging
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


| Field        | Value       |
|--------------|-------------|
| Version      | 2.4         |
| Last Updated | 2026-04-02  |
| Status       | Draft       |
