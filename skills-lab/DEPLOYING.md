# Deploying skills

The lightest mechanism that covers deploying skills from skills-lab into another
project, with traceability on both sides. One script, plain-text packages, and an
append-only record at each end. Git is the source-side version ledger.

## Typical use

Two repos, two roles. skills-lab stays the source of truth and release point; the
new project is the destination.

1. Bootstrap the new project. From `Workspace/chief-of-droids/`, create the new
   repo (usually with the `bootstrapping-project` skill), which lays down its
   `.claude/` baseline.
2. Deploy skills into it. From `skills-lab/`, run `deploy.sh` pointing at the new
   repo and name the skills or a package. They land in the new project's
   `.claude/skills/`, and both ledgers record what shipped, at which version,
   when.

Bootstrap first, deploy second.

## Deploy

```
bash deploy.sh <target-repo> <skill-or-package>... [--force]
```

Examples:

```
bash deploy.sh ../my-app writing-requirements          # one skill
bash deploy.sh ../my-app requirements-chain            # a package
bash deploy.sh ../my-app framing-project wiki-audit    # several by name
```

Each argument is either a skill directory name under `.claude/skills/`, or a
package name matching `packages/<name>.txt`.

## Versioning (SHA only)

The version of every deployed skill is the skills-lab short commit SHA at deploy
time. That single value reconstructs exactly what shipped:

```
git show <sha>:.claude/skills/<skill>/SKILL.md
```

To see whether a deployed copy is behind, compare its recorded SHA with `HEAD`:

```
git diff <sha> HEAD -- .claude/skills/<skill>/
```

No per-skill version numbers to bump. Committing your skill edits is the whole
versioning act.

## Packaging

A package is a named list of skills. One file per package under `packages/`, one
skill directory name per line, `#` for comments. Deploying a package deploys each
line at the current SHA. Group skills that are used together, for example the
`requirements-chain` package (framing → brainstorming → writing).

## Gates

Two checks run before anything is copied, and nothing is copied if either fails
(unless `--force`):

- **Footer status.** A skill whose `SKILL.md` footer `Status` is `Draft` or is
  missing is refused. A draft skill landing in a real project could be trusted as
  ready and cause a mistake. `Review` and `Final` pass.
- **Clean tree.** If skills-lab has uncommitted changes, the SHA cannot
  reconstruct what ships, so deploy is blocked.

The deploy never rewrites the copied files. The "deployed" state lives in the
records below, not stamped into the skill, so `git show <sha>` always matches the
bytes that landed.

## Records (governance)

- **Source, `DEPLOYMENTS.md`** — outbound ledger. One row per deploy run: date,
  target, skills, version.
- **Target, `<target>/.claude/skills/DEPLOYED.md`** — install record. One row per
  skill: skill, version, package, date, source.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-07-16 |
| Status       | Review     |
