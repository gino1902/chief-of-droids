# Workspace Git — Convention Reference

> Version control for the workspace root: what is tracked, what is excluded,
> and how to write commits that remain useful over time.

---

## 1 — What this repo covers

The workspace git repo (`workspace/.git`) versions the shared infrastructure
that all projects in the workspace depend on. It is not a project repo —
it does not track code, build artefacts, or project deliverables.

| Tracked | Why |
| :--- | :--- |
| `CLAUDE.md` | Workspace-wide behaviour defaults; changes here affect every project |
| `skills/` | Shared skills library; the most important thing to version — a breaking change here propagates to all projects |
| `docs/` | Operational guides and design records for the workspace framework |
| `shared/` | Assets shared across project repos (e.g. theme files) |

| Excluded | Why |
| :--- | :--- |
| `.tasks/` | gitignored — TASKS.md and session findings are disk-only; task state is not version-controlled |
| `slide-gen/` | Has its own git repo and remote |
| `my-claude-fmk/` | Has its own git repo and remote |
| `datawan/` | Has its own git repo and remote |
| `*.pptx`, `*.xlsx`, `*.pdf` | Binary outputs — tracked in their project repos if needed |

The `.gitignore` at workspace root enforces these exclusions. If a new project
repo is added under `workspace/`, add it to `.gitignore` immediately — before
its first `git add`.

---

## 2 — Remote

Private GitHub repo. Push target: `origin main`.

```bash
git remote -v   # verify origin is set
git push origin main
```

If the remote has not been set yet:

```bash
git remote add origin git@github.com:<handle>/<repo-name>.git
git branch -M main
git push -u origin main
```

---

## 3 — Commit message convention

Format:

```
<scope>: <what changed>  [ref: <project>]
```

The `[ref: <project>]` suffix is optional — use it when the change was triggered
by or consumed by a specific project repo, so the cross-repo trace exists in
the workspace history.

### Scope values

| Scope | When to use |
| :--- | :--- |
| `skills/<skill-name>` | Any change inside `skills/<skill-name>/` |
| `skills` | Changes to `skills/HOW-TO-TRIGGER.md` or the library as a whole |
| `CLAUDE.md` | Workspace root behaviour defaults |
| `docs` | Any file under `docs/` |
| `shared` | Any file under `shared/` |
| `chore` | Housekeeping with no functional impact (`.gitignore`, README tweaks) |

### Examples

```
skills/writing-docs: add qa-checklist v1.1  [ref: slide-gen]
skills/managing-tasks: bump to v1.5 — write authority rules
skills: update HOW-TO-TRIGGER.md — add project-bootstrapping triggers
CLAUDE.md: add task-manager default TASKS.md path
docs: add workspace-git.md v1.0
shared: add Elevate theme colors
chore: add .gitignore exclusions for datawan/
```

### Multi-scope commits

If a single logical change touches more than one scope (e.g. a skill bump that
also requires a `HOW-TO-TRIGGER.md` update), use the primary scope as the prefix
and list the secondary changes in the body:

```
skills/project-bootstrapping: v1.1 post first-run refinements  [ref: chief-of-droids]

Also updated:
- skills/HOW-TO-TRIGGER.md: added `scaffold project` alias
```

---

## 4 — Commit cadence

Commit at the end of any session that produced a material change to `skills/`,
`CLAUDE.md`, `docs/`, or `shared/`. A session is a commit unit.

The trigger rule: **if the session wrote or modified a tracked file, commit before closing.**
Do not let more than one session's changes accumulate uncommitted.

For skill changes specifically, the commit message scope writes itself from the version bump:

```
skills/managing-tasks: bump to v1.6 — add override pattern
```

Weekly sweeps are not the primary cadence — they bundle unrelated changes and
obscure causality. Prefer per-session discipline.

---

## 5 — Adding a new project repo

When a new project repo is added under `workspace/`:

1. Add the repo directory to `workspace/.gitignore` before the first `git add`
2. Commit the `.gitignore` change: `chore: exclude <repo-name>/ from workspace git`
3. Initialise git in the new repo separately if it needs its own remote

Never nest a git repo inside this workspace repo without explicitly excluding it
in `.gitignore`. Git will track the nested `.git/` objects as regular files,
corrupting both histories silently.

---

## 6 — Git MCP integration (Claude Desktop)

`mcp-server-git` is configured as the `git-workspace` MCP server in `claude_desktop_config.json`.
It exposes git operations as structured tool calls within Claude Desktop sessions.

### Tool coverage

| Tool | Available |
| :--- | :---: |
| `git_status` | ✅ |
| `git_diff_unstaged` | ✅ |
| `git_diff_staged` | ✅ |
| `git_diff` | ✅ |
| `git_add` | ✅ |
| `git_commit` | ✅ |
| `git_reset` | ✅ |
| `git_log` | ✅ |
| `git_branch` | ✅ |
| `git_checkout` | ✅ |
| `git_create_branch` | ✅ |
| `git_show` | ✅ |
| `git_push` | ❌ not available — run manually in Terminal |

### Config entry

```json
"git-workspace": {
  "command": "/Users/gilllesmourgues/.local/bin/uvx",
  "args": ["mcp-server-git", "--repository", "/Users/gilllesmourgues/Workspace/chief-of-droids"]
}
```

### Operational rules (from CLAUDE.md `## Git`)

- Default repo: `/Users/gilllesmourgues/Workspace/chief-of-droids`
- Stage by explicit file path array — never by directory
- Run `git_diff_staged` as a mandatory gate before every commit
- Commit message requires no approval — propose and commit directly after clean diff
- Commit message format: `type(scope): description`
- Push: `git_push` unavailable via MCP — always push manually from Terminal

### Known gaps and quirks

- `git_push` unavailable — run manually: `git push origin main` in Terminal
- `git_log` occasionally unavailable at session start due to tool load order — retry via `tool_search("git log")`
- `git_diff_unstaged` returns empty for files written by Filesystem MCP even when content is on disk — stage explicitly by path rather than relying on status output
- `git_status` can report false positive modified files (CRLF/LF artefact) — confirmed harmless by empty `git_diff`
- **Correction workflow for bad staged diffs:** `git_reset` (unstages all without touching working tree) → fix on disk → `git_add` with explicit paths → `git_diff_staged` → `git_commit`

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.3        |
| Last Updated | 2026-04-12 |
| Status       | Draft      |
