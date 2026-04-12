# MCP Filesystem Setup — WSL2 + Claude Desktop

> ⚠️ This guide applies to the **WSL2/Windows environment** (pre-2026-04-12).
> The workspace has migrated to macOS (M5). For macOS setup, refer to the
> setup guide produced in the 2026-04-12 session ("MacBook Pro M5 workspace setup guide").
> Path references in this document have been updated to reflect the current workspace
> location but the connection procedure remains WSL2-specific.

**Environment:** Windows 11 + WSL2 + Claude Desktop (Win32 installer)

> ⚠️ Install Claude Desktop from **claude.ai/download** (Win32 direct installer), not from the Microsoft Store.
> The Store version runs in an MSIX sandbox that blocks `wsl.exe` process spawning — MCP servers requiring WSL2
> will silently fail to start with no log output.

---

## Steps

### 1. Install Filesystem Extension
- Go to **Settings → Extensions → Browse extensions**
- Find **Filesystem** in the Anthropic-reviewed directory
- Click **Install**

### 2. Configure Path
When prompted for the directory path, enter the workspace root:
```
/Users/gilllesmourgues/Workspace/chief-of-droids
```

Scope to the workspace root — not a sub-directory. This gives the Filesystem MCP access to
`CLAUDE.md`, `TASKS.md`, `skills/`, and `docs/` across all projects.

### 3. Restart Claude Desktop
Fully quit (system tray icon → right-click → **Quit**, not just close the window), then relaunch.

---

## Verify Connection
In a new chat, ask Claude to list files in the workspace root. If it returns the file tree → ✅ connected.

---

## Notes
- No manual `claude_desktop_config.json` editing required for the Filesystem extension
- No Node.js/npm installation required — Claude Desktop includes a built-in Node.js runtime

---

## Troubleshooting

**Extension connects but tools not available in session**
- MCP servers initialise at session start — open a new conversation after connecting
- Check logs: hamburger menu → **Open MCP Log File**
- macOS log location: `~/Library/Logs/Claude/mcp-server-<key-name>.log`

**Path rejected / access denied**
- Confirm the path in Extensions settings matches `/Users/gilllesmourgues/Workspace/chief-of-droids`
- Do not scope to a sub-directory unless intentional

**MCP server not appearing after restart**
- System tray close leaves a background process alive — always use tray → **Quit**
- If still not appearing, check hamburger → **Open MCP Log File** for startup errors

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.2        |
| Last Updated | 2026-04-12 |
| Status       | Final      |
