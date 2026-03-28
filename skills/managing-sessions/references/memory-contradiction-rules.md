<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-03-28 -->

# Memory Contradiction Rules

Patterns to apply when challenging userMemories against on-disk workspace sources.
Read this file before every `challenge memories` workflow run.

The skill reads on-disk sources only — it does not modify userMemories.
All findings are surfaced to the user for manual resolution via
claude.ai Settings → Memory.

---

## Contents

- [Risk Levels](#risk-levels)
- [Rule 1 — Path Format Contradiction](#rule-1--path-format-contradiction)
- [Rule 2 — Skill Name Staleness](#rule-2--skill-name-staleness)
- [Rule 3 — Write Authority Contradiction](#rule-3--write-authority-contradiction)
- [Rule 4 — Tool Availability Claim](#rule-4--tool-availability-claim)
- [Rule 5 — Superseded Design Decision](#rule-5--superseded-design-decision)
- [Rule 6 — Missing Known Gap](#rule-6--missing-known-gap)
- [Rule 7 — Plan Gating Claim](#rule-7--plan-gating-claim)
- [Output Format](#output-format)
- [Maintenance](#maintenance)

---

## Risk Levels

- **High** — memory claim actively contradicts current on-disk state; if acted on,
  would cause incorrect behaviour (wrong paths, wrong patterns, wrong rules)
- **Medium** — memory claim is partially stale or imprecise; may cause confusion
  but unlikely to cause a hard failure
- **Low** — memory claim is outdated framing or phrasing but functionally harmless

---

## Rule Set

### Rule 1 — Path Format Contradiction

**Check:** Does any memory claim reference a file path?
**Against:** All path references in `CLAUDE.md`, skill files, and `docs/`.
**Flag if:** Memory uses UNC path format (`\\wsl.localhost\...`) where
on-disk sources require POSIX format (`/home/gino/workspace/...`).
**Risk:** High — UNC paths fail silently in Filesystem MCP tool parameters.

---

### Rule 2 — Skill Name Staleness

**Check:** Does any memory claim reference a skill by name?
**Against:** `skills/HOW-TO-TRIGGER.md` — the canonical skill inventory.
**Flag if:** Memory references a skill name not present in `HOW-TO-TRIGGER.md`,
or uses a pre-rename name (e.g. `task-manager` instead of `managing-tasks`).
**Risk:** High — wrong skill name causes routing failure.

---

### Rule 3 — Write Authority Contradiction

**Check:** Does any memory claim state a write authority rule?
  (e.g. "Claude writes tasks without asking", "pre-approved", "requires confirmation")
**Against:** Active system prompt `<rules>` block (in context) and
`skills/managing-tasks/references/tasks-schema.md`.
**Flag if:** Memory claim contradicts the current declared write authority.
**Risk:** High — incorrect write authority causes unexpected file writes or
unnecessary confirmation loops.

---

### Rule 4 — Tool Availability Claim

**Check:** Does any memory claim state that a tool is available or unavailable?
  (e.g. "git_push is available", "str_replace works", "edit_file is reliable")
**Against:** Confirmed tool behaviour in `docs/` or session log findings.
**Flag if:** Memory claims a tool works when workspace history confirms it fails
(e.g. `str_replace` silent failure, `git_push` unavailable via MCP).
**Risk:** High — acting on a false tool-availability claim causes silent failures.

---

### Rule 5 — Superseded Design Decision

**Check:** Does any memory claim describe a design decision, workflow, or
architectural approach?
**Against:** `CLAUDE.md` version block date, skill file version blocks,
`docs/` document version blocks.
**Flag if:** Memory describes a design that was explicitly replaced in a
later-dated on-disk version (e.g. early UNC-path-only assumption superseded
by POSIX-path rule; pre-gerund skill names; old task schema format).
**Risk:** Medium — superseded decisions can re-surface as apparent alternatives
and waste session time re-litigating settled choices.

---

### Rule 6 — Missing Known Gap

**Check:** Does any memory claim state that a file or document exists?
  (e.g. "mcp-tool-quirks.md exists", "system-prompt-changelog.md is current")
**Against:** Filesystem directory listing of `docs/` and `my-claude-fmk/`.
**Flag if:** Memory references a file that does not exist on disk.
**Risk:** Medium — skill workflows that depend on these files will fail;
`what-to-capture.md` identifies both as known gaps as of 2026-03-28.

---

### Rule 7 — Plan Gating Claim

**Check:** Does any memory claim state which Claude.ai plan tier a feature requires?
  (e.g. "skills require Pro", "available on all plans")
**Against:** Most recent verified fetch from
`platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`.
**Flag if:** Memory claim has not been re-verified against live docs within
the last 90 days, OR contradicts the last verified on-disk value in the active
project's skills reference documentation (read via Filesystem tool —
do not assume a hardcoded path; locate the file by searching `docs/` or
`claude-desktop/setup/` in the active project).
**Risk:** Medium — plan gating changes without notice; stale claims mislead
framework setup decisions.

---

## Output Format

For each rule triggered, output one row in the contradiction table:

| Memory claim | Rule triggered | On-disk state | Risk | Recommendation |
|:-------------|:---------------|:--------------|:-----|:---------------|
| [exact claim from memory] | Rule N — [name] | [current on-disk value] | High/Med/Low | [action for user] |

Recommendation values:
- `Update memory` — user should edit this memory entry in claude.ai Settings → Memory
- `Verify then update` — re-fetch official source before deciding; memory may be
  correct if docs have since changed
- `No action if harmless` — Low risk; flag for awareness only

---

## Maintenance

Add a new rule when:
- A recurring class of memory contradiction is observed across sessions
- A new on-disk source becomes authoritative for a category of workspace behaviour

Remove a rule when:
- The category it covers no longer applies to this workspace
- The on-disk source it checks against no longer exists

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-03-28 |
| Status       | Draft      |
