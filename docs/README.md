# workspace/docs/

Workspace-level documentation. Covers framework patterns, operational guides,
and design records that apply across all projects in the workspace.

Not repo-specific — repo-level docs live in `<repo>/claude-desktop/` or
alongside the work they document.

---

## Contents

| File | What it covers |
| :--- | :--- |
| `claude-tool-map.md` | Which Anthropic desktop tool to use for which job — Claude Desktop, Claude Cowork, and Claude Code compared. Decision guide and installation scope. |
| `executing-tasks-guide.md` | Reference guide for the `executing-tasks` skill — two entry paths, 11-step outer loop flowchart (Elevate theme), step-by-step descriptions, hard gates summary. |
| `how-to-create-a-skill.md` | Step-by-step account of how the `managing-sessions` skill was designed, challenged, built, live-run, assessed, and committed in a single 3–4 hour session on 2026-03-28. Preserves the philosophy and process for repeating with any new skill. |
| `mcp-tool-quirks.md` | Confirmed failure modes and workarounds for MCP tools used in this workspace — str_replace, write_file, read_multiple_files, git tools, bash_tool, and external fetch targets. Read when tool behaviour is uncertain. |
| `mermaid-example.mmd` | Scratch Mermaid diagram file — not a canonical reference. |
| `system-prompt-changelog.md` | Permanent record of all material changes to the chief-of-droids system prompt. The system prompt is not version-controlled — this file is the only recovery point. |
| `workspace-git.md` | Workspace git convention — what is tracked, what is excluded, commit message format, cadence options, and rules for adding new project repos. |

### Subdirectories

| Directory | What it covers |
| :--- | :--- |
| `claude-desktop/` | Claude Desktop setup guides, context engineering playbook, and Claude Code vs claude.ai vs Claude Desktop comparison reference. |

---

## Adding a guide

- One file per topic, kebab-case filename
- Include a version block at the bottom
- Add a row to the table above on the same commit

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.3        |
| Last Updated | 2026-04-11 |
| Status       | Draft      |
