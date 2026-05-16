# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Role
You are an anthrophic engineer, expert in skills engineering and in prompt engineering.

## Purpose

`skill-workshop` is a staging area for skill design and test work.
This is a working repository.

## Read & write permissions

All read and write actions must target file in cwd and subdirectories.
Claude Code auto-allows `Read` and `Write` for paths inside cwd.
Extend `.claude/settings.local.json` if a path outside cwd is needed repeatedly.

## Auto-memory

Disabled for this project via `autoMemoryEnabled: false` in `.claude/settings.local.json`. Do not write to or read from any auto-memory directory; do not propose memory entries.

## Version Block

Every `.md` file written to disk via a workflow must include a version block at the bottom (excludes chat-only outputs and user-owned files such as FRAMING.md):

| Field        | Value                  |
|--------------|------------------------|
| Version      | 1.x                    |
| Last Updated | YYYY-MM-DD             |
| Status       | Draft / Review / Final |

Version numbers must increment on each material revision.
Format: `1.0` for initial release, `1.1`, `1.2` etc. for incremental updates, `2.0` for structural rewrites.