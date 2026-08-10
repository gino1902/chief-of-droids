# Agent teams with iTerm2 split panes

Setup note for running Claude Code agent teams with each teammate in its own iTerm2 pane, on this machine (macOS, iTerm2, Claude Code 2.1.226).

Split panes are not a Claude Code feature you switch on by itself. Three separate things have to be true: agent teams must be enabled, the display mode must be set to iTerm2, and iTerm2 must expose its Python API to the `it2` CLI. Miss any one and you get a single-terminal session with no visible error.

## Machine state at setup time

| Component | State before | Action |
|-----------|--------------|--------|
| iTerm2 | installed, `TERM_PROGRAM=iTerm.app` | none |
| `it2` CLI | absent | installed, 0.2.3 |
| tmux | absent | none, see fallback |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | unset | set to `1` in user settings |
| `teammateMode` | unset, so default `in-process` | set to `iterm2` |
| iTerm2 Python API | off | enabled by hand in Settings |

## What was changed

`it2` installed with uv, which pulls its own Python 3.10+ and so avoids the system Python 3.9.6:

```bash
uv tool install it2
```

Two keys added to `~/.claude/settings.json`:

```json
{
  "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" },
  "teammateMode": "iterm2"
}
```

Agent teams are experimental and disabled by default. Without the env var no team forms at all, so no panes open regardless of `teammateMode`. Since v2.1.179 the default mode is `in-process`, so the mode has to be named explicitly. The `iterm2` value has existed since v2.1.186 and selects native iTerm2 panes rather than auto-detecting.

## Manual step: Python API

iTerm2 → Settings → General → Magic → Enable Python API. `it2` drives iTerm2 through that API and nothing works until it is on.

Enabling it offers two sub-options. Choose "Require automation permission". A connecting process then needs macOS Automation permission for iTerm2, which is visible and revocable in System Settings → Privacy & Security → Automation. The other option, "Allow all apps to connect", lets any local process attach with no check, which means reading pane contents and typing into sessions that may hold client work. Do not start there.

Expect a one-time iTerm2 prompt naming the script the first time `it2` connects. Allow it permanently so teammate spawning does not stall on a dialog.

Do not write these preferences with `defaults write` while iTerm2 is running. It rewrites its own plist on quit and the change is lost.

## Verification

Quit and reopen iTerm2, then start a fresh `claude`. Settings are read at startup, so an already-running session will not pick up either key.

```bash
it2 ls          # lists iTerm2 sessions; a connection error means the Python API is still off
```

Then ask the lead for teammates, for example "spawn three teammates to review the o2 criteria docs from different angles". Each should land in its own pane.

> ⚠️ Unverified: how macOS attributes Automation permission to `it2` specifically. It is a Python tool launched from a shell inside iTerm2, not a separate app bundle, so the responsible process may be iTerm2 itself. If `it2 ls` cannot connect after a restart, look for an iTerm2 entry under Privacy & Security → Automation before considering the looser API setting.

## Fallback

There is no tmux on this machine, so `iterm2` mode is the only split-pane path. `brew install tmux` adds the alternative, with `tmux -CC` inside iTerm2 as the suggested entry point. To get back to a working session without touching settings:

```bash
claude --teammate-mode in-process   # or: auto
```

The flag is experimental and does not appear in `claude --help`. Split panes are not supported in the VS Code integrated terminal, Windows Terminal, or Ghostty.

## Caveats worth knowing before relying on this

`it2` is third-party software (mkusaka/it2), not an Anthropic tool, and the Anthropic docs point to it without vendoring it. Combined with the Python API it forms a local automation surface over terminals that may hold client data, which is a deliberate choice to make rather than a default to accept. `uv tool uninstall it2` reverses the install.

Teams cost far more tokens than one session, roughly linear in teammate count, because each teammate is a full Claude Code instance with its own context window. The docs suggest starting at three to five.

Two experimental limitations will show up in practice. `/resume` and `/rewind` do not restore in-process teammates, and the lead may then try to message teammates that no longer exist. Teammates also sometimes fail to mark tasks complete, which blocks anything depending on them, so a stuck task usually needs a manual status change or a nudge to the teammate.

If a tmux session ever outlives a Claude Code session, list and kill it:

```bash
tmux ls
tmux kill-session -t <session-name>
```

## Sources

- https://code.claude.com/docs/en/agent-teams
- https://github.com/mkusaka/it2

<!--
Version: 1.0 | Last Updated: 2026-08-10 | Status: Review
-->
