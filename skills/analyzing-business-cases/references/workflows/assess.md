<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-03-23 -->

# Workflow: assess

Trigger: `assess <use-case-id>`

## Steps

1. Use filesystem tool to read `references/consistency-check.md`
2. Use filesystem tool to list `use-case-<id>/` directory — enumerate artifacts present
3. Read all available artifacts in order: FRAMING.md → CONSTITUTION.md → any additional
   pipeline artifacts present (e.g. SlideMap.md, DeckReady.md, or project-specific equivalents)
   — note which are absent; skip missing artifacts, do not block
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
| Version      | 1.0        |
| Last Updated | 2026-03-23 |
| Status       | Final      |
