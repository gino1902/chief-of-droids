# System Prompt Changelog

Records all material changes to the chief-of-droids Claude Desktop project system prompt.
The system prompt is not version-controlled — this file is the only recovery point.
Read before making any system prompt edit; update immediately after any confirmed change.

Entries are chronological (oldest first). Source: session findings files under `.tasks/sessions-findings/`.

---

## 2026-03-19 — Initial system prompt build

Full system prompt authored from scratch and applied to the Chief of Droids Claude Desktop project Custom Instructions.

Blocks added: `<role>` as peer-calibrated domain role (business architect / framework architect); `<context>` populated with workspace framing and the "Claude Code discipline to Claude Desktop" architectural claim; `<rules>` and `<skills>` blocks authored. This was the first working system prompt for the project.

Source: session "Setting up Claude framework context" (2026-03-19), promoted from `.tasks/sessions-findings/2026-03-28-workspace-findings.md`.

---

## 2026-03-20 — Git rules added

Two rules added to the `<rules>` block:

1. `git: default repo /home/gino/workspace; sub-repos: my-claude-fmk | slide-gen | datawan → /home/gino/workspace/<n>; "all repos" → run all repos`
2. `git: commit requires explicit -m approval — present proposed message and wait for confirmation before staging or committing`

Source: session "Git status command" (2026-03-20), promoted from `.tasks/sessions-findings/2026-03-28-workspace-findings.md`.

---

## 2026-03-26 — Full system prompt overhaul

Complete rewrite of all blocks. Changes included: stale UI paths fixed; citation rule extended with fetch-fail fallback (`> ⚠️ Unverified — check against official docs`); token audit rule added (prompt-maintenance workflow); MCP per-read failure surfacing rule added; `<role>` rewritten as peer-calibrated domain role with explicit domain framing.

Source: session "Rephrasing resource pooling" (2026-03-26), promoted from `.tasks/sessions-findings/2026-03-28-workspace-findings.md`.

---

## 2026-03-26 — File edit rule added

Rule added to `<rules>` block: `File edits: use filesystem:read_text_file → filesystem:write_file; str_replace is unavailable in this environment`.

Trigger: Claude narrated a tool fallback mid-response, revealing the absence of an explicit constraint. Rule added to prevent silent fallback behaviour.

Source: session "Elevate theme colors file" (2026-03-26), promoted from `.tasks/sessions-findings/2026-03-28-workspace-findings.md`.

---

## 2026-04-03 — Three rules migrated from system prompt to CLAUDE.md

Three operational rules removed from the system prompt `<rules>` block and moved to `CLAUDE.md` as dedicated sections. Established the principle that all operational conventions live in CLAUDE.md (version-controlled, MCP-editable) and the system prompt holds only bootstrap instructions, hard behavioral rails, and pre-approvals.

Rules moved:
- Git workflow rule (now `## Git` section in CLAUDE.md)
- File edit pattern rule (now `## File Edits` section in CLAUDE.md)
- Token audit trigger rule (now `## Maintenance` section in CLAUDE.md)

Source: session "Interactive commit workflow with diff preview" (2026-04-03), promoted from `.tasks/sessions-findings/2026-04-11-chief-of-droids-findings.md`.

---

## 2026-04-03 — Path-declaration rule removed

The rule declaring default repo paths and sub-repo lists was removed from the system prompt `<rules>` block entirely.

Rationale: the git MCP toolchain already owns repo path validation via `.git` detection; declaring paths in the system prompt is redundant noise that creates a maintenance liability.

Source: session "Git repository management setup" (2026-04-03), promoted from `.tasks/sessions-findings/2026-04-11-chief-of-droids-findings.md`.

---

## 2026-04-03 — Per-file git diff workflow refined

The commit diff workflow rule was corrected: run `git_status` first to enumerate staged files, then call `git_diff_staged` per file individually before committing. Previous behaviour showed a single unified blob which broke per-file diff visibility.

This change was made to CLAUDE.md (not the system prompt directly) as part of the 2026-04-03 operational rules migration — included here because it corrects prior system prompt-level git discipline.

Source: session "Git repository management setup" (2026-04-03), promoted from `.tasks/sessions-findings/2026-04-11-chief-of-droids-findings.md`.

---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.0        |
| Last Updated | 2026-04-11 |
| Status       | Draft      |
