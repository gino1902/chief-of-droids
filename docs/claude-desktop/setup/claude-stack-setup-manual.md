# Claude Power Stack — Setup Manual

> Windows 11 | Claude Desktop + MCP + Claude Code
> Version 2.2

---

## Prerequisites

- Windows 11
- A Claude account (claude.ai) on a paid plan (Pro, Max, Team, or Enterprise)
- Accounts on each service you want to integrate (Gamma, Slack, Notion, etc.)

---

## Step 1 — Install Claude Desktop

1. Go to [claude.ai/download](https://claude.ai/download)
2. Click **Windows** to download `ClaudeSetup.exe`
3. Run the installer — accept all defaults
4. Launch Claude Desktop from the Start menu
5. Sign in with your Anthropic account

**Verify:** The app opens with Chat / Cowork / Code tabs at the top.

---

## Step 2 — Connect Remote MCP Services (Connectors)

This is the correct path for all hosted SaaS integrations (Gamma, Slack, Google Drive, Notion, GitHub, etc.).

### 2.1 Browse and connect

**Current canonical path: Customize > Connectors** (Connectors have moved out of Settings as of early 2026). The old `Settings > Connectors` path may still be present in some versions.

**A) Service is in the built-in directory** (Google Drive, GitHub, Gmail, Google Calendar):

1. Navigate to **Customize > Connectors** (or **Settings > Connectors** if you see that instead)
2. Click **Browse Connectors**
3. Find the service and click **Connect**
4. Complete the **OAuth flow** in your browser — log in and click Allow

**B) Service is not in the directory** (Gamma, Notion, Slack, and most others):

1. Navigate to **Customize > Connectors**
2. Click the **"+"** button next to Connectors
3. Enter the connector name and remote MCP server URL
4. Click Add → complete the **OAuth flow** in your browser

> ✅ **v2.1 correction:** Previous version referenced `Settings > Connectors > Add custom connector`. Canonical current path is `Customize > Connectors > "+"` per support.claude.com (verified 2026-03-13).

### 2.2 Use the connector

In any conversation, click the **`+`** button next to the chat input → **Connectors** — enable the connector for that conversation.

Or simply ask Claude to use it: *"Create a 5-slide presentation about AI trends in Gamma."*

### 2.3 Repeat for each service

Repeat Step 2.1 for every service you want to connect. No Node.js, no API keys, no JSON config needed.

---

## Step 3 — Connect Local MCP Extensions (.mcpb)

Use this path for tools that run on your machine (filesystem access, custom internal tools, etc.).

### 3.1 From the official directory

1. `Settings > Extensions > Browse Extensions`
2. Find the extension (e.g. Filesystem)
3. Click **Install**
4. Configure required settings (e.g. allowed directories) via the settings UI

### 3.2 From a custom .mcpb file

1. `Settings > Extensions > Advanced Settings`
2. Click **Install Extension…**
3. Select your `.mcpb` file
4. Follow the prompts to configure

**Note:** Claude Desktop includes a built-in Node.js runtime. No Node.js installation required for .mcpb extensions.

---

## Step 4 — Verify Connections

After connecting any service, test it in Claude Desktop:

```
List my Gamma themes
```

```
Show my Google Drive recent files
```

If the connector is active, Claude will return real data from the service. If not, go back to `Settings > Connectors` and verify the connection status.

To see all connected tools in a conversation, click the **`+`** button → **Connectors**.

---

## Step 5 — Install WSL2

WSL2 is required for Claude Code and for the Git workflow used in the content-as-code setup (Doc 3).

### 5.1 Install WSL2

Open PowerShell as Administrator:

```powershell
wsl --install
```

Restart your machine. Ubuntu is installed by default.

### 5.2 Complete Ubuntu setup

On first launch, Ubuntu will prompt you to create a Linux username and password. These are separate from your Windows credentials.

### 5.3 Update Ubuntu packages

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Step 6 — Set Up Git in WSL2

### 6.1 Install Git

```bash
sudo apt-get install git -y
```

### 6.2 Verify installation

```bash
git --version
```

### 6.3 Configure your identity

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### 6.4 Authenticate with GitHub

The recommended method is SSH keys — no password required on every push.

**Generate an SSH key:**

```bash
ssh-keygen -t ed25519 -C "your@email.com"
```

Press Enter to accept all defaults.

**Copy your public key:**

```bash
cat ~/.ssh/id_ed25519.pub
```

**Add it to GitHub:**

1. Go to [github.com](https://github.com) → click your **profile avatar** (top right) → **Settings**
2. In the left sidebar, under **Access**, click **SSH and GPG keys**
3. Click **New SSH key** (or **Add SSH key** if you have existing keys)
4. Set **Key type** to **Authentication Key**
5. Add a **Title** (e.g. "WSL2 Ubuntu")
6. Paste your public key in the **Key** field
7. Click **Add SSH key**

**Test the connection:**

```bash
ssh -T git@github.com
```

Expected output: `Hi username! You've successfully authenticated.`

---

## Step 7 — Install Claude Code

Claude Code cannot run natively in PowerShell on Windows — it requires WSL2 (Steps 5–6 above).

### 7.1 Open Ubuntu terminal

From the Start menu, open **Ubuntu**. You are now in a Linux environment.

### 7.2 Install Node.js in WSL2

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 7.3 Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 7.4 Authenticate

```bash
claude
```

On first run, a browser window will open to authenticate with your Anthropic account.

### 7.5 Basic usage

Navigate to any project folder and start Claude Code:

```bash
cd /mnt/c/Users/<you>/your-project
claude
```

The `/mnt/c/` prefix maps to your Windows `C:\` drive from within WSL2.

---

## Step 8 — Adding a New Remote MCP Service (Repeatable Pattern)

When you want to connect a new SaaS tool:

1. Check if it has a connector: `Settings > Connectors > Browse Connectors`
2. If listed: click Connect → OAuth → done
3. If not listed: check if the service offers a custom remote MCP URL
4. If yes: `Settings > Connectors > Add Custom Connector` → enter the URL → OAuth

---

## Step 9 — Adding a New Local MCP Extension (Repeatable Pattern)

When you want to add a local tool:

1. Check the official directory: `Settings > Extensions > Browse Extensions`
2. If listed: click Install → configure → done
3. If not listed: obtain or build a `.mcpb` file
4. `Settings > Extensions > Advanced Settings > Install Extension` → select `.mcpb`

---

## Advanced — JSON Config (Developers Only)

The `claude_desktop_config.json` file is valid only for **custom local MCP servers during development**. It does not work for remote/hosted services.

Location:

```
%APPDATA%\Claude\claude_desktop_config.json
```

Template:

```json
{
  "mcpServers": {
    "my-custom-server": {
      "command": "node",
      "args": ["C:\\absolute\\path\\to\\server.js"],
      "env": { "MY_API_KEY": "YOUR_KEY_HERE" }
    }
  }
}
```

After editing: fully quit Claude Desktop (system tray → Quit) and relaunch.

Validate JSON before saving at [jsonlint.com](https://jsonlint.com).

---

## Troubleshooting

**Connector not appearing after OAuth**

- Disconnect and reconnect the connector in `Settings > Connectors`
- Make sure you completed the OAuth flow and clicked Allow

**Extension not installing**

- Ensure Claude Desktop is updated to the latest version
- Re-download the `.mcpb` file in case it is corrupted
- Check `Settings > Extensions` for error logs

**SSH authentication fails**

- Run `ssh-keygen -t ed25519 -C "your@email.com"` again
- Verify the public key is added to GitHub under Settings → SSH and GPG keys → Authentication Key

**Claude Code not found in WSL2**

- Run `npm install -g @anthropic-ai/claude-code` again
- Verify with `claude --version`

**Claude Code can't access Windows files**

- Use `/mnt/c/Users/<you>/...` path format inside WSL2

---

## File Reference

| File / Location | Purpose |
| :--- | :--- |
| `%APPDATA%\Claude\claude_desktop_config.json` | Local MCP server config (developers only) |
| `Settings > Connectors` | Manage remote MCP connections |
| `Settings > Extensions` | Manage local .mcpb extensions |
| `Settings > Developer` | Logs and advanced MCP debugging |

---

*Doc 2 of 2 — see 01-claude-stack-explainer.md for architecture and component details*
*MCP server setup guides: filesystem-mcp-wsl2-setup.md | mcp-server-git-setup.md*
