<!-- version: 1.9 | author: chief-of-droids workspace | last_updated: 2026-04-03 -->

# Workflow: assess-artifacts

Trigger: `assess-artifacts <project-name>`

## Steps

1. Use filesystem tool to read `references/qa-checklist.md` (assess-artifacts section) and `references/workflows/challenge-framing.md`
2. Use filesystem tool to list `[REPO_NAME]/` directory — enumerate artifacts present
3. Read all available artifacts in order: FRAMING.md → [REPO_NAME]/CLAUDE.md → any additional
   project artifacts present — note which are absent; skip missing artifacts, do not block
4. Run challenge-framing workflow on the FRAMING.md read in step 3 — surface findings; don't rewrite
5. Run qa-checklist assess-artifacts section on the artifacts read in step 3
6. Output a gap table: artifact pair | issue | severity | recommendation
7. Do not rewrite any artifact — surface findings only
8. If user requests fixes: delegate to the appropriate workflow for that artifact type

## Failure handling

- `references/workflows/challenge-framing.md` unreadable: proceed but flag — `⚠️ challenge-framing.md unreadable — FRAMING challenge skipped; review manually.`
- `references/qa-checklist.md` unreadable: proceed but flag — `⚠️ qa-checklist.md unreadable — execution checks skipped; review manually.`
- Missing artifacts are not failures — skip the transition and note in output.

## Output

Gap table in chat (no file write)

| Field        | Value      |
|--------------|------------|
| Version      | 1.9        |
| Last Updated | 2026-04-03 |
| Status       | Final      |
