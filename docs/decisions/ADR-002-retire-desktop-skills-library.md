# ADR-002 — retire the Desktop skills library (workspace/skills/)

| Field | Value |
|:------|:------|
| Date | 2026-07-20 |
| Status | Decided |
| Tasks | TASK-087, TASK-088, TASK-089, TASK-090, TASK-091 |
| Supersedes | the `workspace/skills/` library and its `HOW-TO-TRIGGER.md` router |

---

## Context

`workspace/skills/` was a Claude Desktop skills library of ten skills, dispatched by a
`HOW-TO-TRIGGER.md` router read over Filesystem MCP at Desktop session bootstrap. A usage
review found the whole generation frozen and superseded:

- Development frozen. Last commit touching `skills/` was 2026-07-07, while `skills-lab/` ran
  115 commits through 2026-07-20, where the successor `.claude/skills/` collection is built.
- Dormant in Claude Code. Across 499 Claude Code transcripts these skills showed no genuine
  task-triggered loads. References collapsed to one router-enumeration session, one file-editing
  session, and measurement noise.
- Superseded. Every capability has a live `.claude/skills/` successor carrying real traffic, or
  is obsolete under Claude Code.

Caveat on the evidence. These skills triggered only in Claude Desktop, where each turn carries a
`🧭 skills:` routing line that is the true usage signal. That signal lives in claude.ai account
history, not on disk, and no data export was available (no rights), so real Desktop volume before
the freeze is unmeasured. It does not change the decision: a skill that was heavy in Desktop but is
now frozen and fully succeeded still retires.

## Decision

Retire the library. Delete `workspace/skills/` in full rather than keep an archive folder, on the
principle that version control is the archive. Split the ten skills three ways:

- Seven retired outright, recoverable from git history.
- Three with no successor moved to `skills-lab/requirements/other-skills/` as transform substrate,
  to be re-authored as native `.claude/skills/` through the requirements-chain. Each carries a
  `NOTES.md` of dependencies and dedupe points.
- The `HOW-TO-TRIGGER.md` router moved to the same location as substrate for its rewrite into a
  Desktop to `.claude/skills/` bridge.

The target architecture keeps official Claude Code config (`.claude/skills/`) as the single source
of truth, with Desktop wired to it through the rewritten bridge.

## Succession map (retired seven)

| Retired skill | Superseded by |
| :--- | :--- |
| `project-bootstrapping` | `bootstrapping-project` (`.claude/skills/`) |
| `brainstorming-ideas` | `brainstorming-requirements` |
| `analyzing-business-cases` | `framing-project` + `qualifying-outputs` |
| `creating-skills` | `improving-skills-predictability` + `improving-prompt-artifacts` + `skill-creator` plugin |
| `managing-tasks` | Claude Code native task tools |
| `managing-sessions` | none — obsolete premise (Claude.ai Desktop session hygiene) |
| `executing-tasks` | none — retired, the quality-gate workflow is unmanageable against native task tools, the Workflow harness, and the requirements-chain |

## Transformed three (in migration)

`editing-docs`, `architecting-data-platforms`, `reviewing-tech-claims`. Located at
`skills-lab/requirements/other-skills/`, each with a `NOTES.md`. Ports tracked by TASK-087..089.

## Recovery

The full content of every deleted file is in git history. It last existed intact at:

```
d3c8f0c3f1a6426bbb6d7d7fe2b1e9edbf9af337   (on origin/main)
```

Find and restore:

```
git log --all --full-history -- 'skills/**'          # locate history
git show d3c8f0c:skills/_archive/<skill>/SKILL.md     # read a file
git checkout d3c8f0c -- skills/_archive/<skill>        # restore a directory
```

The SHA is a convenience. `git log --all --full-history` finds the content without it.
`measure-triggering.py`, a script that parses a claude.ai export into a per-skill trigger table
for the retired skills, was removed with the library and is recoverable the same way if an export
ever becomes available.

## Consequences

- `workspace/skills/` no longer exists. References to it in docs, ADR-001, root CLAUDE.md, and
  `desktop-chat/CLAUDE.md` are now stale and are cleaned up under TASK-091.
- The Desktop bootstrap read of `skills/HOW-TO-TRIGGER.md` no longer resolves. Desktop falls back to
  no skill loading until the bridge rewrite (TASK-090) ships at a chosen live path.
- Skill authoring is now single-track: native `.claude/skills/`, built through the requirements-chain.
