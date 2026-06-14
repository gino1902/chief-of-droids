# CLAUDE.md — desktop-chat

---

## Scope

Applies to Claude Desktop sessions for the chief-of-droids project.
Primary working directory for all Desktop sessions: `/Users/gilllesmourgues/Workspace/chief-of-droids/desktop-chat/`
All temp files, output files, and session artefacts default to this directory.

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
- Session summaries in chat: omit git commit hashes — not actionable in chat context

---

## Version Block

Every `.md` file written to disk via a workflow must include a version block at the bottom (excludes chat-only outputs and user-owned files such as FRAMING.md).

The block is a hidden HTML comment — present in the source, not rendered:

```markdown
<!--
Version: 1.x | Last Updated: YYYY-MM-DD | Status: Draft / Review / Final
-->
```

Rationale: the metadata stays in the source (grep-able, diffable) but does not render, keeping the document clean for the reader. HTML comments are hidden by every renderer; do not use a visible table or YAML frontmatter for this purpose.

Version numbers must increment on each material revision.
Format: `1.0` for initial release, `1.1`, `1.2` etc. for incremental updates, `2.0` for structural rewrites.

---

## MCP Tools

This workspace uses two MCP servers for content retrieval. They have similar verb semantics but distinct scopes — do not conflate them.

| Tool | Server | Use for |
| :--- | :--- | :--- |
| `filesystem:read_text_file` | Filesystem MCP | Local file paths under `/Users/gilllesmourgues/Workspace/chief-of-droids/` |
| `fetch` | mcp-server-fetch | External URLs (HTTP/HTTPS) |

**Routing rule:** if the target is a URL → use `fetch`. If the target is a filesystem path → use `filesystem:read_text_file`. Never attempt a URL via Filesystem MCP or a local path via `fetch`.

**`fetch` tool behaviour:**
- Returns page content converted to markdown
- Truncates by default; use `start_index` to read in chunks
- Respects `robots.txt` when the call originates from a tool (model-initiated); ignores it when user-initiated via prompt
- Can access local/internal IP addresses — do not use `fetch` against localhost or internal network addresses in this workspace

**Enforcement:** the system prompt rule `never cite an external source unless its full content has been fetched and verified via web_fetch` is satisfied in Claude Desktop sessions by calling `fetch` via mcp-server-fetch. This tool is the Desktop-session equivalent of the `web_fetch` runtime tool available in claude.ai sessions.

---

## File Edits

- Pattern: `filesystem:read_text_file` → `filesystem:write_file` (full rewrite)
- `str_replace` has known silent failure behaviour in this workspace — do not use
- Always read the full current file before writing — never rewrite from memory or prior context

---

## Skills Architecture

This workspace loads skills via Claude Desktop + Filesystem MCP — not the official Claude Code Agent Skills mechanism. This distinction matters when applying official Anthropic guidance to skill design or assessment.

**How skills load in this workspace:**
- Claude reads `skills/HOW-TO-TRIGGER.md` explicitly via Filesystem tool at session bootstrap to determine routing
- The matched `SKILL.md` is then read in full via Filesystem tool
- No frontmatter scanning occurs — the full file content is always available once loaded

**Official Claude Code behaviors that do NOT apply here:**

| Claude Code behavior | Status in this workspace |
| :--- | :--- |
| Frontmatter description scanning — routes skills by reading descriptions | Not applicable — routing is via HOW-TO-TRIGGER.md, read explicitly |
| 250-char description cap — descriptions truncated in routing index | Not applicable — full SKILL.md content is loaded; length has no routing effect |
| `disable-model-invocation: true` — removes skill from auto-loading | Not applicable — no automatic loading mechanism exists |
| `context: fork` / `agent` fields — runs skill in a forked subagent | Not applicable — no subagent spawning in Claude Desktop |

**Example — 250-char cap:**
In Claude Code, a frontmatter description longer than 250 chars gets truncated in the routing index. The trigger keywords after the cutpoint become invisible to Claude's routing engine. In this workspace, Claude reads `HOW-TO-TRIGGER.md` for routing (full file, no truncation) and then loads the full SKILL.md. A 500-char description is entirely visible. Front-loading key triggers remains good practice for readability, but the 250-char limit is not a technical constraint here.

**Example — `disable-model-invocation: true`:**
In Claude Code, setting this field prevents the skill from auto-loading when a user's prompt matches the description. In this workspace, no auto-loading from description matching occurs — every skill load is explicit. The field is simply ignored.

When applying official Anthropic documentation (via `reviewing-tech-claims` or any source fetch) to skill design, always confirm whether the guidance is Claude Code-specific or general. Guidance about prompt engineering, description specificity, and negative examples applies to both environments. Guidance about frontmatter fields, forking, and routing mechanisms applies to Claude Code only.

---

## Task Management

Default TASKS.md for this desktop-chat context: `/Users/gilllesmourgues/Workspace/chief-of-droids/.tasks/TASKS.md`

Override precedence (highest to lowest):
1. Explicit path in the user's prompt — e.g. "add task to slide-gen" → `workspace/slide-gen/TASKS.md`
2. This CLAUDE.md default — `/Users/gilllesmourgues/Workspace/chief-of-droids/.tasks/TASKS.md`
3. Schema fallback — `<repo-root>/TASKS.md` relative to the active default repo

Repo-level CLAUDE.md files may declare their own default. That declaration takes
precedence over this default for sessions routed to that repo.

---

## Git

- Default repo: `/Users/gilllesmourgues/Workspace/chief-of-droids`; "all repos" → run across all repos
- Stage by explicit file path array — never by directory (risk of sweeping untracked files from subdirectories)
- **Mandatory commit gate — applies after every `filesystem:write_file` call without exception:**
  - Ask: "Do you want to commit?" — do not skip or pre-answer this question from context
  - A user message containing "commit" or any prior commit instruction does not bypass the gate — ask regardless
  - In a multi-write sequence, ask the gate after each individual write, not once at the end
  - Await explicit yes or no in the next user message before proceeding
  - Yes → ask "Display diffs? (yes/no)"; if yes → run `git_diff_staged` per uncommitted file, display each diff, then commit; if no → commit directly
  - No → wait for next prompt
- Commit message: propose and commit directly — no approval required
- Commit message format: `type(scope): description`
- Push: `git_push` unavailable via MCP — always push manually from Terminal

---

## Maintenance

Run a token audit whenever a rule, workflow, or routing path is added to the system prompt. Methodology to be re-established — TASK-083.

---

## Session Hygiene

Run once, as the final step of reading this file. Do not repeat within the session.

1. Call `recent_chats n=1` to get the most recent session's `updated_at`
2. Read `/Users/gilllesmourgues/Workspace/chief-of-droids/.tasks/sessions-findings/sentinel.md`
3. Evaluate:
   - If sentinel file is absent → surface: `⚠️ Session hygiene: sentinel not found (first run)`
   - If `recent_chats[0].updated_at - sentinel.last_run_date > 10 days` → surface:
     `⚠️ Session hygiene: last run was [sentinel.last_run_date], last session was [updated_at]`
   - If neither condition is met → proceed silently, no output
4. If a condition was surfaced: ask once — "Run managing-sessions skill now?"
   - Yes → invoke managing-sessions skill
   - Any other response → proceed without running the skill

---

<!--
Version: 1.2 | Last Updated: 2026-06-14 | Status: Draft
-->
