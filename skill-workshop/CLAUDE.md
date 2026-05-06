# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read & write permissions

All read and write actions must target file in cwd and subdirectories.
Claude Code auto-allows `Read` for paths inside cwd.
Extend `.claude/settings.local.json` if a path outside cwd is needed repeatedly.

## Auto-memory

Disabled for this project via `autoMemoryEnabled: false` in `.claude/settings.local.json`. Do not write to or read from any auto-memory directory; do not propose memory entries.

## Purpose

`skill-workshop` is a staging area for skill design and test work.
This is a working repository.