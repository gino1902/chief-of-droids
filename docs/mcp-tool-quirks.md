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
Workaround: stage files explicitly by path rather than relying on status output
to confirm the change is tracked.

---

## `git_status` — false positive modified files

`git_status` can report files as modified when `git_diff_unstaged` and
`git_diff` against HEAD both return empty. On macOS the typical cause is file
mode bit changes (executable bit), not a content change. Confirmed by empty
diff; safe to ignore. Run `git config core.fileMode false` in the repo if the
issue is persistent.

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

## `git-workspace` MCP — unavailable in claude.ai sessions

The `git-workspace` MCP server is a **local process** configured in
`claude_desktop_config.json`. It spawns via `uvx` on the local machine as a
child process of Claude Desktop. It is never available in claude.ai browser or
app sessions — claude.ai cannot spawn local processes.

Consequence: `git_add`, `git_diff_staged`, `git_commit`, and all other
`git-workspace` tools return nothing from `tool_search` in a claude.ai session,
even when the server is correctly configured and working in Claude Desktop.

Workaround: run git operations from Claude Desktop, or directly from Terminal.
Confirmed 2026-04-12.

---

## `bash_tool` — cannot access local filesystem paths

`bash_tool` runs in a remote container, not on the local machine. It has no
access to local paths (`/Users/gilllesmourgues/Workspace/...`) regardless of
OS. Commands like `grep`, `cat`, or `ls` against local paths will silently
return empty or fail.

Use `filesystem:search_files` (with a `pattern` argument) for post-write
verification and file searches against local paths. This is the correct tool
for any operation that needs to inspect the local filesystem from within a
claude.ai session.

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

Absence of `[server-name]` entries in the MCP log means Claude Desktop never
attempted to spawn that server — not that it crashed after starting. Root
causes: JSON parse error in `claude_desktop_config.json`, or spawn blocked by
a system-level constraint.

Log location by platform:
- macOS: `~/Library/Logs/Claude/mcp-server-<key-name>.log`
- Windows: `%APPDATA%\Claude\logs\mcp-server-<key-name>.log`

Check the log file first; if no entries exist, the issue is pre-spawn.

---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.4        |
| Last Updated | 2026-04-12 |
| Status       | Draft      |
