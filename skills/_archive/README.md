# Archived skills — tombstone

The Desktop-era `skills/` library was retired on 2026-07-20. This folder is a tombstone:
it keeps the decision record and the recovery pointer, not the skill bodies. The full
content of every archived skill lives in git history and is recoverable in one command.

## Recovery

The skill directories were removed after being committed and pushed. They last existed intact at:

```
recovery SHA: d3c8f0c3f1a6426bbb6d7d7fe2b1e9edbf9af337   (on origin/main)
```

Restore any one skill with:

```
git checkout d3c8f0c -- skills/_archive/<skill>
```

For example `git checkout d3c8f0c -- skills/_archive/executing-tasks`. Browse a single file
without restoring with `git show d3c8f0c:skills/_archive/<skill>/SKILL.md`.

## Why this generation was archived

A usage review found the whole `skills/` generation frozen and superseded:

- Development frozen. Last commit touching `skills/` was 2026-07-07, while `skills-lab/`
  ran 115 commits through 2026-07-20, where the successor `.claude/skills/` collection is built.
- Dormant in Claude Code. Across 499 transcripts these skills showed no genuine task-triggered
  loads. References collapsed to one router-enumeration session, one file-editing session, and noise.
- Superseded. Every archived capability has a live `.claude/skills/` successor, or is obsolete
  under Claude Code.

Caveat on the evidence. These skills triggered only in Claude Desktop, via the HOW-TO-TRIGGER
router over Filesystem MCP. Desktop turns carry a `🧭 skills:` routing line that is the true usage
signal, but it lives in claude.ai account history, not on disk, and no data export was available.
Real Desktop volume before the freeze is therefore unmeasured. It does not change the decision:
a skill that was heavy in Desktop but is now frozen and fully succeeded still retires.

## Succession map

| Archived skill | Superseded by | Note |
| :--- | :--- | :--- |
| `project-bootstrapping` | `bootstrapping-project` (`.claude/skills/`, ~427 reads) | Direct successor. Migration already done. |
| `brainstorming-ideas` | `brainstorming-requirements` (~215) | Direct successor. |
| `analyzing-business-cases` | `framing-project` (~187) + `qualifying-outputs` (~221) | Split: framing vs pressure-test. |
| `creating-skills` | `improving-skills-predictability` (~75) + `improving-prompt-artifacts` (~64) + `skill-creator` plugin | Function split across successors. |
| `managing-tasks` | Claude Code native task tools | Platform tooling replaces it. |
| `managing-sessions` | none | Obsolete premise. Analysed Claude.ai Desktop session history, which does not apply to Claude Code. |
| `executing-tasks` | none | Retired, not ported. The quality-gate workflow is unmanageable against native task tools, the Workflow harness, and the requirements-chain. |

## Transformed — moved, not archived

Three skills with no successor were moved to `skills-lab/requirements/other-skills/` on 2026-07-20
as transform substrate, to be re-authored as native `.claude/skills/` through the requirements-chain.
Each carries a `NOTES.md`: `editing-docs`, `architecting-data-platforms`, `reviewing-tech-claims`.
The old HOW-TO-TRIGGER router moved there too, as substrate for its rewrite into a Desktop
to `.claude/skills/` bridge.

## measure-triggering.py

Kept in this folder. It parses a claude.ai data export and produces the per-skill trigger table
for these archived skills, the one measurement that on-disk transcripts could not give. It only has
value against the skills recorded here, so it lives with them rather than in a live tools directory.
