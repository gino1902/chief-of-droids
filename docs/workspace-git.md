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
| `TASKS.md` | Cross-repo task board; history shows what work was done and when |
| `skills/` | Shared skills library; the most important thing to version — a breaking change here propagates to all projects |
| `docs/` | Operational guides and design records for the workspace framework |
| `shared/` | Assets shared across project repos (e.g. theme files) |

| Excluded | Why |
| :--- | :--- |
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
| `TASKS.md` | Task board updates (open, close, bulk transition) |
| `docs` | Any file under `docs/` |
| `shared` | Any file under `shared/` |
| `chore` | Housekeeping with no functional impact (`.gitignore`, README tweaks) |

### Examples

```
skills/writing-docs: add qa-checklist v1.1  [ref: slide-gen]
skills/managing-tasks: bump to v1.5 — write authority rules
skills: update HOW-TO-TRIGGER.md — add project-bootstrapping triggers
CLAUDE.md: add task-manager default TASKS.md path
TASKS.md: close TASK-014; add TASK-012, TASK-013
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
- TASKS.md: closed TASK-009
```

---

## 4 — Commit cadence

> 🔲 To be defined — see TASK-013.

Decision pending. Options under consideration:

- **Per-session** — commit at the end of any session that modified `skills/`,
  `CLAUDE.md`, or `TASKS.md`
- **Per-skill-version-bump** — every `<!-- version: X.Y -->` increment in a
  `SKILL.md` triggers a commit; message writes itself from the version bump
- **Weekly sweep** — fixed cadence regardless of change volume; risk of bundling
  unrelated changes

Until decided, commit manually at the end of sessions that produce material
changes. Do not let more than one session's worth of changes accumulate uncommitted.

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

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-03-20 |
| Status       | Draft      |
