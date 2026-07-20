# Archived skills

Seven skills from the Desktop-era `skills/` library, archived on 2026-07-20. They are kept for
reference, not for triggering.

## Why this generation was archived

A usage review found the whole `skills/` generation frozen and superseded:

- Development frozen. Last commit touching `skills/` was 2026-07-07. Meanwhile `skills-lab/`
  ran 115 commits through 2026-07-20, where the successor `.claude/skills/` collection is built.
- Dormant in Claude Code. Across 499 Claude Code transcripts these skills showed no genuine
  task-triggered loads. Their references collapse to one router-enumeration session, one
  file-editing session, and measurement noise.
- Superseded. Every archived capability has a live `.claude/skills/` successor carrying real
  traffic, or is obsolete under Claude Code.

Caveat on the evidence. These skills triggered only in Claude Desktop, via the HOW-TO-TRIGGER
router over Filesystem MCP. Desktop turns carry a `🧭 skills:` routing line that is the true
usage signal, but it lives in claude.ai account history, not on disk, and a data export was not
available. So real Desktop volume before the freeze is unmeasured. It does not change the
decision: a skill that was heavy in Desktop but is now frozen and fully succeeded still retires.
`measure-triggering.py` in this folder produces the per-skill trigger table if a claude.ai
export ever becomes available.

## Succession map

| Archived skill | Superseded by | Note |
| :--- | :--- | :--- |
| `project-bootstrapping` | `bootstrapping-project` (`.claude/skills/`, ~427 reads) | Direct successor. Migration already done. |
| `brainstorming-ideas` | `brainstorming-requirements` (~215) | Direct successor. |
| `analyzing-business-cases` | `framing-project` (~187) + `qualifying-outputs` (~221) | Split: framing vs pressure-test. |
| `creating-skills` | `improving-skills-predictability` (~75) + `improving-prompt-artifacts` (~64) + `skill-creator` plugin | Function split across successors. |
| `managing-tasks` | Claude Code native task tools | Platform tooling replaces it. |
| `managing-sessions` | none | Obsolete premise. Analysed Claude.ai Desktop session history, which does not apply to Claude Code. |
| `executing-tasks` | none | Retired, not ported. The quality-gate workflow (intent, plan, QA, verify) is unmanageable against native task tools, the Workflow harness, and the requirements-chain. |

## Transformed — not here

Three skills were not archived. They cover a capability with no live successor and were moved to
`skills-lab/requirements/other-skills/` on 2026-07-20 as transform substrate, to be re-authored as
native `.claude/skills/` through the requirements-chain. Each carries a `NOTES.md` recording its
dependencies and dedupe points.

- `editing-docs` — document-expression layer (docx, pptx, xlsx, minutes, decision records).
- `architecting-data-platforms` — Databricks / Azure / governance domain knowledge.
- `reviewing-tech-claims` — verification of technical claims against official docs, ✅ / ⚠️ markers.

## HOW-TO-TRIGGER.md is not archived

The router stays live at `skills/HOW-TO-TRIGGER.md`. The target architecture keeps the official
Claude Code config (`.claude/skills/`) as the single source of truth and wires Claude Desktop to it
through an updated HOW-TO-TRIGGER, rather than the old per-`skills/` routing. The rewrite is tracked
as a task.

## How to restore one

```
git mv skills/_archive/<skill> skills/<skill>
```
Prior router content is recoverable from git history before the 2026-07-20 archive commit.
