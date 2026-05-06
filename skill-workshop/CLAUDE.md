# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Scope of this CLAUDE.md

This file is the only CLAUDE.md in scope for Claude Code sessions running in `skill-workshop/`. Do not load or apply the workspace-level CLAUDE.md at `../CLAUDE.md` — it targets Claude Desktop sessions (Filesystem MCP routing, `str_replace` warnings, commit gate, `recent_chats` sentinel, etc.) and its rules do not apply here.

## Read permissions

Skills iterated here may read substrate files outside cwd (e.g. `../docs/`). Output is always written under cwd, and cwd only. Claude Code auto-allows `Read` only for paths inside cwd, so reads outside `skill-workshop/` prompt for approval. Approve per file, or extend `.claude/settings.local.json` if a path is needed repeatedly.

## Auto-memory

Disabled for this project via `autoMemoryEnabled: false` in `.claude/settings.local.json`. Do not write to or read from any auto-memory directory; do not propose memory entries.

## Purpose

`skill-workshop` is a staging area for skill design work — design handoff documents, decision records, and pre-draft material for skills that will eventually live under `../skills/<skill-name>/`. Files here are working documents, not final deliverables.

## File naming convention

`YYYY-MM-DD-<skill-name>-<purpose>.md`

Example: `2026-05-05-writing-requirements-skill-design.md`

## Relationship to the skills directory

Design documents here feed into a skill folder. The install pattern depends on scope:

- **Project scope** — skill lives at `skill-workshop/.claude/skills/<skill-name>/` and is only available when Claude Code runs inside `skill-workshop/`. No symlink needed. This is the default for skills under active iteration.
- **User scope** — skill lives at `../skills/<skill-name>/` (workspace root) and is symlinked into `~/.claude/skills/<skill-name>` to make it available to all projects:
   ```bash
   ln -s ~/Workspace/chief-of-droids/skills/<skill-name> ~/.claude/skills/<skill-name>
   ```

Once a skill ships, its design doc in `skill-workshop/` is retired (kept for history, not actively used).

## Active work

Current design in progress: `writing-requirements` skill — see `2026-05-05-writing-requirements-skill-design.md` for locked decisions, parked items, and next-session instructions.
