# CLAUDE.md

## Role
You are an expert in skills engineering and prompt engineering.

## Purpose

`skills-lab` is a staging area for skill design and test work.
This is a working repository.

## Skill scope boundary

A project-scoped skill may read user-global state, for example `~/.claude/CLAUDE.md`, but never writes or mutates it, and never installs into the user's environment. Every write targets the project, meaning cwd or the repo root. A skill that needs user-level content references its location and warns when it is absent. It does not create or change that content.

## Read & write permissions

All read and write actions must target files in cwd and subdirectories.
Configured in `.claude/settings.json`: `defaultMode: acceptEdits` auto-approves `Write`, `Edit`, and filesystem Bash (`mkdir`, `touch`, `mv`, `cp`, etc.) for paths inside cwd; out-of-cwd targets prompt. `Bash(rm *)` always prompts. `Read` and the built-in read-only Bash set auto-approve everywhere by Claude Code default.
Extend `.claude/settings.local.json` if a path outside cwd is needed repeatedly.

### Allowlist hygiene

`permissions.allow` in `.claude/settings.json` is kept grouped and alphabetised. `Skill(...)` first, then `Bash(...)`, then `WebFetch(...)`, each block sorted by its pattern string, with a blank line between blocks. Add new entries in place rather than appending to the end. Only read-only or clearly safe patterns belong in the shared file. The mutating git operations this project actually runs (`git add`, `git commit`, `git branch`, `git checkout`, `git merge`) live here by deliberate choice. Do not add an interpreter or shell wildcard (for example a package runner, `node`, or a bare `python3 *`), because it grants arbitrary code execution. Per-user or path-specific grants belong in `.claude/settings.local.json`, which is gitignored.

### Reducing permission prompts

Claude Code approves a Bash call only when every segment of it is allowed, so a single un-allowed segment makes the whole line prompt. A read-only allowlist cannot fix a compound command that also contains a mutating or code-executing segment. Compose commands so each is independently approvable.

- Run one command per Bash call. Do not chain reads and mutations with `&&`, `|`, or `;`, and avoid `for ... done` loops where separate calls would do.
- Do not use `awk`. It counts as arbitrary code execution and taints any pipeline it sits in. Reach for `grep`, `sed`, `cut`, `sort`, `uniq`, `jq`, or `wc` instead, which auto-approve.
- Keep a mutation (`mkdir`, `mv`, `rm`) on its own line, never bundled with reads.
- Prefer the native tools over Bash where they fit. Use `Read` over `cat`, the `Grep` tool over `grep`, and `Glob` over `find`. These never prompt.

## Skill-creator doc freshness

When `/skill-creator` is invoked, a hook injects the latest Anthropic skill-authoring docs as `additionalContext`. Two hook entries cover both invocation paths: `UserPromptExpansion` (matcher `skill-creator:skill-creator`) for user-typed slash commands, and `PreToolUse` (matcher `Skill`, condition `Skill(skill-creator*)`) for model-driven calls. Sources: `skills.md`, `best-practices.md`, `features-overview.md` from `code.claude.com`.

Large payloads are persisted to a session-scoped file under `tool-results/` and previewed inline, so read that file when you need the full docs.

Cache: `.claude/cache/skill-docs/` (gitignored). Refresh policy: `curl` only when older than 7 days. Force a refresh: `bash .claude/scripts/refresh-skill-docs.sh`.

Scripts:
- `.claude/scripts/refresh-skill-docs.sh` — fetcher
- `.claude/hooks/inject-skill-creator-context.sh` — stale-check + emit JSON (docs plus the version-block convention; dynamic `hookEventName`); one-line diagnostic at `/tmp/skill-creator-hook.log`

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

The footer carries only these three fields. Audit or provenance metadata (target model, target environment, best-practices reference, revision source) belongs in the report that produced or revised the artifact, not in the artifact footer.

## Humanizer scope

The organization instruction to apply the humanizer skill when generating a document or email is scoped to user-facing documents. That means emails, client-facing prose, reports written for people, and in this project the `FRAMING.md` and the run retrospectives. It does not apply to agent-facing artifacts, meaning every `SKILL.md` and skill file, this `CLAUDE.md`, project instructions, prompt templates, agent and tool definitions, and the test suite's scenario specs, strategy, scope map, and checks. Those are read as instructions, where fidelity and predictability outrank sounding human and a humanizer pass can strip structure the artifact needs. This scopes the word "document" in the rule, it does not override the rule.

## Target and version

These instructions are version-neutral. They target claude-code and do not depend on any single Claude model version.