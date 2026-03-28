# Skill Recommendations — 2026-03-28

## Source

| Field | Value |
|:------|:------|
| Findings file | 2026-03-28-workspace-findings.md |
| Findings confidence | High |
| Sessions analysed | 20 |
| Run date | 2026-03-28 |

---

## Recommendations

| Candidate skill | Signal type | Sessions | Confidence | Source match | Pattern available |
|:----------------|:------------|:---------|:-----------|:-------------|:------------------|
| `recording-decisions` — capture ADRs, design decisions, and evaluation outcomes to disk; prevent unrecorded decisions that recur across sessions | Untracked domain + Manual workaround | 3 | High | DAIR.AI + Anthropic Skills Repo | Yes |
| `promoting-findings` — workflow to promote `not-on-disk` content from session findings files to canonical docs (e.g. `mcp-tool-quirks.md`, `system-prompt-changelog.md`) | Manual workaround | 4 | High | None | No — build from workspace patterns only |
| `enforcing-tool-constraints` — encodes known tool failure modes as constraints Claude reads at session start; prevents `str_replace` recurrence and similar | Repeated correction | 2 | High | Anthropic Skills Repo | Yes |

---

## Discarded Signals

| Signal | Reason discarded |
|:-------|:-----------------|
| All 5 findings in `-2` file | All `on-disk` — produced in the same session as the findings file |
| `recording-framework-description` | Single-occurrence task, not a repeatable skill pattern — belongs as TASK-025/026 scope, not a skill |
| Workspace git Option A, Win32 installer, creating-skills URL correction, session summaries convention | Already `on-disk` in target files |
| Packmind evaluation outcome | Single-occurrence decision record — belongs as a docs/ ADR entry, not a skill |

---

## Next Steps

For each High confidence recommendation:

**`recording-decisions`**
- Run `author skill recording-decisions`
- Reference: DAIR.AI prompt engineering guide (decision documentation patterns) + Anthropic Skills Repo (SKILL.md structure)
- Scope: triggers on "record decision", "this is an ADR", "log this decision", "capture outcome"; writes structured decision entries to `docs/decisions/` or inline ADR files

**`promoting-findings`**
- Run `author skill promoting-findings`
- No external source — model on `managing-sessions` output workflow (session-log-schema.md pattern)
- Scope: reads a findings file, identifies `not-on-disk` entries, promotes verbatim to target canonical doc; updates `Promoted to` column

**`enforcing-tool-constraints`**
- Run `author skill enforcing-tool-constraints`
- Reference: Anthropic Skills Repo (constraint pattern from production skills)
- Scope: loaded at session bootstrap; encodes known-bad tool patterns as standing instructions; covers `str_replace`, `filesystem:write_file` silent failure, `read_multiple_files` bootstrap issue, `git_diff_unstaged` bypass

---

## Test Run Notes

> These notes are for TASK-034 — not part of the canonical output schema

First run (against `-2` file): zero candidates survived Step 3 — correct behaviour;
findings file confidence was High but all findings were `on-disk`.

Second run (against original file): 3 High-confidence candidates produced.
Signal extraction, confidence scoring, and source catalog match all executed correctly.

Two workflow gaps identified during testing:
1. Step 3 discard rule "appears only once and shows no recurrence pattern" required
   judgment about corroboration by Known Gaps table — the rule as written does not
   make this explicit. Candidate 4 (`recording-framework-description`) was discarded
   correctly but the rule text should encode the Known Gaps corroboration exception
   more clearly.
2. Step 5 source catalog match is keyword-based — `promoting-findings` matched no
   source despite being a legitimate High-confidence candidate. The workflow correctly
   flagged "no external source — build from workspace patterns only" but this should
   not lower confidence. Current draft does not penalise confidence for no source match;
   confirmed correct.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-03-28 |
| Status       | Draft      |
