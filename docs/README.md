# workspace/docs/

Workspace-level documentation. Covers framework patterns, operational guides,
and design records that apply across all projects in the workspace.

Not repo-specific — repo-level docs live in `<repo>/claude-desktop/` or
alongside the work they document.

---

## Contents

| File | What it covers |
| :--- | :--- |
| `bootstrapping-guide.md` | How to use the `project-bootstrapping` skill to scaffold a new Claude Desktop project — form, challenge, generation, file write, and post-bootstrap checklist. Includes design decisions from the 2026-03-19 session. |
| `how-to-create-a-skill.md` | Step-by-step account of how the `managing-sessions` skill was designed, challenged, built, live-run, assessed, and committed in a single 3–4 hour session on 2026-03-28. Preserves the philosophy and process for repeating with any new skill. |
| `workspace-git.md` | Workspace git convention — what is tracked, what is excluded, commit message format, cadence options, and rules for adding new project repos. |

---

## Adding a guide

- One file per topic, kebab-case filename
- Include a version block at the bottom
- Add a row to the table above on the same commit

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.2        |
| Last Updated | 2026-03-28 |
| Status       | Draft      |
