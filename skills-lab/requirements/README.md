# smart-init

A Claude Code skill that creates or reconciles a project's CLAUDE.md, tailored to what the project is for.

## Why

A CLAUDE.md written for running code misgoverns a repo meant for thinking, and vice versa. The built-in `/init` produces one generic file regardless. This skill locks a project goal at creation (thinking, code, or infra) and generates a CLAUDE.md that carries only the rules that goal needs.

Three principles drive the design:

1. Less is more. Instruction-following degrades as instruction count grows, so every generated file stays under 60 lines and every line must be grounded in the repo. Behavioural rules that apply everywhere (the Karpathy guidelines) live once at user level, never per project.
2. Hard rules belong in enforcement. Prohibitions like "never deploy" go to settings.json deny rules and hooks, which enforce at 100%, not to CLAUDE.md prose, which is followed about 70% of the time.
3. Surgical by default. An existing CLAUDE.md is never regenerated. It is reconciled through a minimal, approval-gated diff that preserves the author's wording.

## What

One command, two modes, detected by whether CLAUDE.md exists:

- CREATE (no CLAUDE.md): asks the goal if not passed as argument, locks it via a stamp, scans the repo, writes the file from a goal-specific skeleton. On an empty repo it also proposes a minimal project tree (thinking, code-data, code-app, or infra) and scaffolds it after approval. Directories are deferred until needed, never speculative.
- RECONCILE (CLAUDE.md exists): reads the locked goal from the stamp, rejects a conflicting argument, and proposes a diff: gaps to fill, rules to move to enforcement, ungrounded lines to drop. Applies nothing without approval.

The skill also checks that the Karpathy guidelines are installed at `~/.claude/CLAUDE.md` and proposes deny rules and hooks for any hard prohibition it finds.

## Install

```bash
mkdir -p <repo>/.claude/skills/smart-init
cp smart-init-SKILL.md <repo>/.claude/skills/smart-init/SKILL.md
```

Run with `/smart-init [thinking|code|infra]` (argument used at creation only).

## Known limits

- The goal stamp is a plain comment: convention, not enforcement.
- `Write(CLAUDE.md)` path scoping in frontmatter is unverified against official docs.
- The trees encode opinions (notebooks/src split, Gruntwork-style modules/envs). Field-test before trusting, starting with an infra repo.

## References

Official (Anthropic):

- Claude Code best practices — https://code.claude.com/docs/en/best-practices
- Claude Code best practices, original engineering post — https://www.anthropic.com/engineering/claude-code-best-practices
- Slash commands and skills format — https://code.claude.com/docs/en/slash-commands

Behavioural guidelines:

- Karpathy guidelines (forrestchang/andrej-karpathy-skills) — https://github.com/forrestchang/andrej-karpathy-skills
- Writing a good CLAUDE.md, HumanLayer — https://www.humanlayer.dev/blog/writing-a-good-claude-md

Repository structure:

- Architecture decision records — https://github.com/joelparkerhenderson/architecture-decision-record
- Go project layout (community convention, not official Go guidance) — https://github.com/golang-standards/project-layout
- Terragrunt / Gruntwork reference architectures — https://docs.gruntwork.io
