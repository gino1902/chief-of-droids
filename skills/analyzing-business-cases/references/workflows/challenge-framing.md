<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-03-23 -->

# Workflow: challenge framing

Trigger: `challenge framing <use-case-id>` | "challenge this proposal"
| "is the framing solid" | "does this make business sense"

## Steps

1. Use filesystem tool to read `use-case-<id>/FRAMING.md`
2. Use filesystem tool to read `references/challenge-checklist.md`
3. Run checklist against every section
4. Output a structured critique — section by section, issue by issue
5. Surface findings only — do not rewrite FRAMING.md unless user requests (see step 6)
6. If user confirms findings and requests a fix: propose edits, await approval, then write

## Failure handling

- `use-case-<id>/FRAMING.md` absent: halt — `⚠️ FRAMING.md not found for use-case-<id> — nothing to challenge.`
- `references/challenge-checklist.md` unreadable: proceed but flag — `⚠️ challenge-checklist.md unreadable — critique run from skill memory only.`

## Output

Structured critique in chat (no file write unless user requests)

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-03-23 |
| Status       | Final      |
