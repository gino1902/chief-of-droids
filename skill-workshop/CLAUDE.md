# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

`skill-workshop` is a staging area for skill design work — design handoff documents, decision records, and pre-draft material for skills that will eventually live under `../skills/<skill-name>/`. Files here are working documents, not final deliverables.

## File naming convention

`YYYY-MM-DD-<skill-name>-<purpose>.md`

Example: `2026-05-05-writing-requirements-skill-design.md`

## Relationship to the skills directory

Design documents here feed into `../skills/<skill-name>/SKILL.md`. Once a skill ships:

1. The corresponding design doc in `skill-workshop/` is retired (kept for history, not actively used).
2. The skill folder is created at `../skills/<skill-name>/`.
3. A symlink is created for Claude Code agent scope:
   ```bash
   ln -s ~/Workspace/chief-of-droids/skills/<skill-name> ~/.claude/skills/<skill-name>
   ```

## Active work

Current design in progress: `writing-requirements` skill — see `2026-05-05-writing-requirements-skill-design.md` for locked decisions, parked items, and next-session instructions.
