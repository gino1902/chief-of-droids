<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-04-02 -->

# Managing Tasks QA Checklist

Run before any write operation in the managing-tasks skill.

## Pre-write gates (all callers)

- [ ] `references/tasks-schema.md` read before any write operation
- [ ] Target file determined by inference rule — not assumed
- [ ] Write Authority rule checked before any write — see `references/tasks-schema.md`
- [ ] Bootstrap announced as proposal (not statement) when TASKS.md is missing
- [ ] Conflict check run before every `start task` — one active task per file
- [ ] TASK-ID incremented from highest ID across all sections including Done
- [ ] Done date appended in `YYYY-MM-DD` format
- [ ] `update task` modifies `target` and `scope` only — no other fields touched

## Caller context gates

- [ ] Caller type identified before field resolution — user (direct prompt) or skill (in-session payload)
- [ ] Skill call: origin, description, target taken from call payload directly — not prompted or derived
- [ ] Skill call: `add task` Step 8 writes directly — no proposal step presented to user
- [ ] Skill call: if a required field is absent, gap surfaced to orchestrating skill — not to user
- [ ] `add task`: TASK-ID returned explicitly after write — "Task created: TASK-XXX" — skill callers must retain it


| Field        | Value       |
|--------------|-------------|
| Version      | 1.1         |
| Last Updated | 2026-04-02  |
| Status       | Draft       |
