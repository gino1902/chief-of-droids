# MCP Filesystem Setup — WSL2 + Claude Desktop

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

### 2. Configure WSL2 Path
When prompted for the directory path, enter the WSL2 UNC format:
```
\\wsl.localhost\Ubuntu\home\gino\workspace
```

Scope to the workspace root — not a sub-directory. This gives the Filesystem MCP access to
`CLAUDE.md`, `TASKS.md`, `skills/`, and `docs/` across all projects.

### 3. Restart Claude Desktop
Fully quit (system tray icon → right-click → **Quit**, not just close the window), then relaunch.

---

## Path behaviour — UNC vs POSIX

The Filesystem MCP accepts UNC paths (`\\wsl.localhost\Ubuntu\...`) in its configuration UI.
However, inside a session the MCP server runs in WSL2 and resolves paths as POSIX
(`/home/gino/workspace/...`). Both forms work for reads and writes, but the MCP server
rejects UNC paths that start outside its configured root.

Rule: use POSIX paths in prompts and tool calls. Use UNC format only in the Extensions
configuration UI.

---

## Verify Connection
In a new chat, ask Claude to list files in the workspace root. If it returns the file tree → ✅ connected.

---

## Notes
- No manual `claude_desktop_config.json` editing required for the Filesystem extension
- No Node.js/npm installation required — Claude Desktop includes a built-in Node.js runtime
- The built-in runtime is what allows the Filesystem MCP to work without external dependencies;
  other MCP servers (e.g. `mcp-server-git`) that run via `wsl.exe` require the Win32 installer

---

## Troubleshooting

**Extension connects but tools not available in session**
- MCP servers initialise at session start — open a new conversation after connecting
- Check logs: hamburger menu → **Open MCP Log File**
- If no log file exists for the server, it failed to spawn — verify Win32 installer (not Store)

**UNC path rejected / access denied**
- Confirm the path in Extensions settings matches `\\wsl.localhost\Ubuntu\home\gino\workspace`
- Do not scope to a sub-directory unless intentional

**MCP server not appearing after restart**
- System tray close leaves a background process alive — always use tray → **Quit**
- If still not appearing, check `hamburger → Open MCP Log File` for startup errors

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-03-20 |
| Status       | Final      |
