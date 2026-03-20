<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-03-19 -->

# Managing Tasks QA Checklist

Run before any write operation in the managing-tasks skill.

- [ ] `references/tasks-schema.md` read before any write operation
- [ ] Target file determined by inference rule — not assumed
- [ ] Write Authority rule checked before any write — see `references/tasks-schema.md`
- [ ] Bootstrap announced as proposal (not statement) when TASKS.md is missing
- [ ] Conflict check run before every `start task` — one active task per file
- [ ] TASK-ID incremented from highest ID across all sections including Done
- [ ] Done date appended in `YYYY-MM-DD` format
- [ ] `update task` modifies `target` and `scope` only — no other fields touched
