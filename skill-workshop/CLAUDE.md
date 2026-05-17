# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Role
You are an anthrophic engineer, expert in skills engineering and in prompt engineering.

## Purpose

`skill-workshop` is a staging area for skill design and test work.
This is a working repository.

## Read & write permissions

All read and write actions must target files in cwd and subdirectories.
Configured in `.claude/settings.json`: `defaultMode: acceptEdits` auto-approves `Write`, `Edit`, and filesystem Bash (`mkdir`, `touch`, `mv`, `cp`, etc.) for paths inside cwd; out-of-cwd targets prompt. `Bash(rm *)` always prompts. `Read` and the built-in read-only Bash set auto-approve everywhere by Claude Code default.
Extend `.claude/settings.local.json` if a path outside cwd is needed repeatedly.

## Skill-creator doc freshness

When `/skill-creator` is invoked, a hook injects the latest Anthropic skill-authoring docs as `additionalContext`. Two hook entries cover both invocation paths: `UserPromptExpansion` (matcher `skill-creator:skill-creator`) for user-typed slash commands, and `PreToolUse` (matcher `Skill`, condition `Skill(skill-creator*)`) for model-driven calls. Sources: `skills.md`, `best-practices.md`, `features-overview.md` from `code.claude.com`.

The payload is ~108 KB. Claude Code persists large `additionalContext` to a session-scoped file under `tool-results/` and inlines a 2 KB preview + the file path — the model `Read`s the file when it needs the full docs, so ~28K tokens don't hit every turn.

Cache: `.claude/cache/skill-docs/` (gitignored). Refresh policy: `curl` only when older than 7 days. Force a refresh: `bash .claude/scripts/refresh-skill-docs.sh`.

Scripts:
- `.claude/scripts/refresh-skill-docs.sh` — fetcher
- `.claude/hooks/inject-skill-docs.sh` — stale-check + emit JSON (dynamic `hookEventName`); one-line diagnostic at `/tmp/skill-creator-hook.log`

## Auto-memory

Disabled for this project via `autoMemoryEnabled: false` in `.claude/settings.json`. Do not write to or read from any auto-memory directory; do not propose memory entries.

## Version Block

Every `.md` file written to disk via a workflow must include a version block at the bottom (excludes chat-only outputs and user-owned files such as FRAMING.md):

| Field        | Value                  |
|--------------|------------------------|
| Version      | 1.x                    |
| Last Updated | YYYY-MM-DD             |
| Status       | Draft / Review / Final |

Version numbers must increment on each material revision.
Format: `1.0` for initial release, `1.1`, `1.2` etc. for incremental updates, `2.0` for structural rewrites.