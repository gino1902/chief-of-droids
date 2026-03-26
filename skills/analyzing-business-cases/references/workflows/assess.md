<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-03-25 -->

# Workflow: assess

Trigger: `assess <project-name>`

## Steps

1. Use filesystem tool to read `references/consistency-check.md`
2. Use filesystem tool to list `[REPO_NAME]/` directory — enumerate artifacts present
3. Read all available artifacts in order: FRAMING.md → CONSTITUTION.md → any additional
   project artifacts present — note which are absent; skip missing artifacts, do not block
4. For each artifact transition present, run the corresponding check from consistency-check.md
5. Output a gap table: artifact pair | issue | severity | recommendation
6. Do not rewrite any artifact — surface findings only
7. If user requests fixes: delegate to the appropriate workflow for that artifact type

## Failure handling

- `references/consistency-check.md` unreadable: halt — `⚠️ consistency-check.md unreadable — cannot run assessment. Resolve before continuing.`
- Missing artifacts are not failures — skip the transition and note in output.

## Output

Gap table in chat (no file write)

| Field        | Value      |
|--------------|------------|
| Version      | 1.1        |
| Last Updated | 2026-03-25 |
| Status       | Final      |
