# CLAUDE.md — workspace

---

## Scope

Applies to all repos in this workspace unless a repo-level CLAUDE.md overrides these defaults.

---

## Tone

- Direct, technical, no filler
- Assume the reader is the repo author: business architect with strong technical background
- No preamble summarising what you're about to do — just do it
- Language: English
- Flag uncertainty explicitly: `> ⚠️ Unverified — check against official docs`
- Flag outdated content explicitly: `> ⚠️ Stale — verify before use`
- Flag scaffolded content awaiting user input: `> 🔲 To be defined — awaiting user input`

---

## Format

- Default output format: **Markdown (.md)**
- Use plain prose with tables and code blocks where appropriate
- No decorative formatting: no emoji, no horizontal rules as decoration
- Use headers sparingly — one level of nesting is usually enough
- Prefer tables over bullet lists for structured comparisons
- All code examples use fenced blocks with language tag (` ```xml `, ` ```bash `, ` ```markdown `)

---

## Version Block

Every `.md` file written to disk via a workflow must include a version block at the bottom (excludes chat-only outputs and user-owned files such as FRAMING.md):

| Field        | Value                  |
|--------------|------------------------|
| Version      | 1.x                    |
| Last Updated | YYYY-MM-DD             |
| Status       | Draft / Review / Final |

Version numbers must increment on each material revision.
Format: `1.0` for initial release, `1.1`, `1.2` etc. for incremental updates, `2.0` for structural rewrites.

---

## Task Management

Default TASKS.md for this workspace context: `workspace/TASKS.md`

This applies when the active Claude Desktop project operates at workspace scope —
i.e. its work spans multiple repos or the shared skills library rather than a
single named repo.

Override precedence (highest to lowest):
1. Explicit path in the user's prompt — e.g. "add task to slide-gen" → `workspace/slide-gen/TASKS.md`
2. This CLAUDE.md default — `workspace/TASKS.md`
3. Schema fallback — `<repo-root>/TASKS.md` relative to the active default repo

Repo-level CLAUDE.md files may declare their own default. That declaration takes
precedence over this workspace default for sessions routed to that repo.
