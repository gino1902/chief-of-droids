# MCP Tool Quirks

Known failure modes and workarounds for MCP tools used in this workspace.
Promoted from session findings (2026-03-28, 2026-04-11). Read at session start when tool
behaviour is uncertain, or when a tool returns unexpected results.

---

## `str_replace` / `filesystem:edit_file` — silent failure

Both tools fail silently in this workspace — no error returned, file unchanged.
The reliable pattern for all edits is: read the full file via
`filesystem:read_text_file`, then rewrite entirely via `filesystem:write_file`.
Never attempt targeted string replacement.

---

## `filesystem:write_file` — silent connectivity failure

When `filesystem:write_file` returns nothing (no result, no error) across
multiple attempts and paths, this is a session-level MCP connectivity issue —
not a path or content problem. Restart Claude Desktop to restore MCP
connectivity. Do not attempt to debug path format or content when the tool
returns silently.

---

## `filesystem:read_multiple_files` — silent empty result on bootstrap

On session bootstrap, `filesystem:read_multiple_files` can return an empty
result for known files even when those files have content. A follow-up
`filesystem:read_text_file` on the same path retrieves the content correctly.
Prefer `read_text_file` for individual file reads; use `read_multiple_files`
only for batch reads of 3+ files after bootstrap is confirmed stable.

---

## `filesystem:create_directory` — deep path single call

Calling `create_directory` with a path that includes multiple levels
(e.g. `skills/standardizing-artefacts/references/schemas`) creates the full
path including all intermediate directories in one call. No need to call
`create_directory` separately for parent and child levels. Confirmed
2026-04-11.

---

## `git_diff_unstaged` — empty result for Filesystem MCP writes

`git_diff_unstaged` (and `git_status`) do not surface files written by
`filesystem:write_file` even when the content on disk is confirmed correct.
This is a WSL2-specific issue: Filesystem MCP writes to the Linux path
directly, bypassing the git index that `git-workspace` tracks. Workaround:
stage files explicitly by path rather than relying on status output to confirm
the change is tracked.

---

## `git_status` — false positive modified files

`git_status` can report files as modified when `git_diff_unstaged` and
`git_diff` against HEAD both return empty. This is a CRLF/LF artefact, not a
real change. Confirmed by empty diff; safe to ignore.

---

## `git_log` — tool unavailable at session start

`git_log` is occasionally unavailable at session start due to tool load order.
Retry via `tool_search("git log")` resolves it reliably.

---

## `git_reset` — correction workflow for bad staged diffs

When `git_diff_staged` reveals an error after staging, use this correction
sequence: `git_reset` (unstages all staged files without altering the working
tree) → fix the issue on disk → `git_add` with explicit file path array →
`git_diff_staged` to verify → `git_commit`. Confirmed 2026-04-08.

---

## `bash_tool` — grep empty for WSL2 paths

`bash_tool` grep commands return empty output when targeting files at WSL2
paths (e.g. `/home/gino/workspace/...`) even when files exist and contain the
pattern. Use `filesystem:search_files` with a `pattern` argument as the
reliable fallback for post-write verification. Confirmed 2026-04-03.

---

## `docs.anthropic.com` skills best-practices URL — permissions error

`https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices`
consistently returns a permissions error in this workspace. Use `web_search`
for Anthropic engineering content instead. The agentskills.io specification is
accessible via web search as a substitute source. Confirmed 2026-04-06.

---

## `agentskills.io` — fetch blocked via MCP tool

`agentskills.io` fetch is blocked via the `fetch` MCP tool in this workspace
environment. Content is accessible via `web_search` querying
`agentskills.io specification`. Confirmed 2026-04-11.

---

## MCP log — spawn-level failure diagnosis

Absence of `[server-name]` entries in the MCP log
(`%APPDATA%\Claude\logs\mcp-server-<key-name>.log`) means Claude Desktop never
attempted to spawn that server — not that it crashed after starting. Root
causes: JSON parse error in `claude_desktop_config.json`, or spawn blocked by
AppContainer sandbox (MSIX install). Check the log file first; if no entries
exist, the issue is pre-spawn. Fix: uninstall MSIX Store version, install Win32
direct installer.

---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.1        |
| Last Updated | 2026-04-11 |
| Status       | Draft      |
