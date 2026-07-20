<!-- version: 1.4 | author: chief-of-droids workspace | last_updated: 2026-04-03 -->

# Workflow: challenge framing

Trigger: `challenge framing <project-name>` | `challenge framing` | "challenge this proposal"
| "is the framing solid" | "does this make business sense"

## Path Resolution

Resolve the FRAMING.md path in this order — stop at the first match:

1. **Explicit path in prompt** — user provides a full or relative path
   → use that path directly
2. **Active repo root** — no explicit path given
   → resolve to `[REPO_NAME]/FRAMING.md`

Never hardcode a path. Always confirm resolved path to the user before reading:
`Reading FRAMING.md from: <resolved-path>`

## Steps

1. Resolve FRAMING.md path (see Path Resolution above); read via Filesystem tool
2. Use filesystem tool to read `references/qa-checklist.md` — `challenge framing` section only
3. Run each item in the `challenge framing` checklist section against FRAMING.md
4. Output a structured critique — one finding per checklist item that fails, grouped by FRAMING.md section
5. Surface findings only — do not rewrite FRAMING.md unless user requests (see step 6)
6. If user confirms findings and requests a fix: propose edits, await approval, then write

## Failure handling

- FRAMING.md absent at resolved path: halt — `⚠️ FRAMING.md not found at <resolved-path> — nothing to challenge.`
- `references/qa-checklist.md` unreadable: proceed but flag — `⚠️ qa-checklist.md unreadable — critique run from skill memory only.`

## Output

Structured critique in chat (no file write unless user requests)

| Field        | Value      |
|--------------|------------|
| Version      | 1.4        |
| Last Updated | 2026-04-03 |
| Status       | Final      |
