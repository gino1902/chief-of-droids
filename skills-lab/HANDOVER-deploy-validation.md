# Handover: deploy mechanism validation

Pick up the deploy mechanism where the first smoke deploy left it. The goal is to
exercise the four paths that first run did not cover, so the mechanism can be
promoted from `Review` to `Final` with each path validated at least once.

## Where things stand

- First real run: 2026-07-19, `bootstrapping-project` deployed into
  `chief-of-droids` at version `53663ce`. Happy path only.
- Validated so far: footer gate (`Review` passes), clean-tree guard, copy,
  both ledgers, discoverability in the target.
- `DEPLOYING.md` is at Version 1.2, Status `Review`. Its "First run" section
  lists the same four untried paths recorded below.
- `skills-lab/testing/` is gitignored, so skill test runs no longer dirty the
  tree. The clean-tree guard therefore stays green between test runs.

## The tool

Run from `skills-lab/`:

```
bash deploy.sh <target-repo> <skill-or-package>... [--force]
```

`deploy.sh` resolves its lab root and `packages/` from its own location, so the
skill and package names are looked up under `skills-lab/.claude/skills/` and
`skills-lab/packages/` regardless of where you invoke it.

Two gates run before any copy, both blocking unless `--force`:

- Footer status. A skill whose `SKILL.md` footer `Status` is `Draft` or missing
  is refused. `Review` and `Final` pass.
- Clean tree. If the repo containing `skills-lab` has uncommitted changes, deploy
  is blocked, because the recorded SHA would not reconstruct what shipped. Note
  this guard reads the `chief-of-droids` repo, since `skills-lab` is a subdirectory
  of it, not a separate repo.

## The four paths to exercise

Do each once. Use a throwaway target repo for anything that would leave a Draft
skill or a broken state in a real project.

### 1. Package deploy

- Goal. Confirm a package expands to its skill list and deploys each at one SHA.
- Setup. `packages/requirements-chain.txt` lists `framing-project`,
  `brainstorming-requirements`, `writing-requirements`. Confirm all three carry a
  `Review` or `Final` footer first, or the gate blocks the whole run.
- Run. `bash deploy.sh <target> requirements-chain`
- Pass. All three skills land in the target. `DEPLOYED.md` gains one row per skill
  with the Package column set to `requirements-chain`. `DEPLOYMENTS.md` gains one
  run row listing all three skills at the same SHA.

### 2. Force override

- Goal. Confirm `--force` overrides both gates and says so loudly.
- Setup. Trigger each gate in turn. For the footer gate, point at a skill whose
  footer `Status` is `Draft` or absent. For the clean-tree guard, leave an
  uncommitted change in the repo.
- Run. `bash deploy.sh <target> <draft-skill> --force`
- Pass. A WARNING line prints for the overridden gate and the copy proceeds. The
  same run without `--force` aborts with the matching abort message and copies
  nothing. Do this against a throwaway target so no Draft skill lands anywhere
  real.

### 3. Separate-repo target

- Goal. Exercise the two-repos shape `DEPLOYING.md` describes, where the target is
  a repo distinct from the one holding `skills-lab`. The first run deployed into
  the enclosing repo, which is not that shape.
- Setup. Create or pick a separate git repo as the target. Bootstrapping a small
  one with the `bootstrapping-project` skill is the natural way to get a valid
  `.claude/` baseline.
- Run. `bash deploy.sh <other-repo-abs-path> bootstrapping-project`
- Pass. The skill lands in that repo's `.claude/skills/`, its own `DEPLOYED.md` is
  created there, and `skills-lab/DEPLOYMENTS.md` appends the run. Confirm the
  clean-tree guard still reads the `chief-of-droids` repo, not the target.

### 4. Overwrite an existing copy

- Goal. Confirm re-deploying a skill already present in the target replaces it
  cleanly and records a second run.
- Setup. `chief-of-droids` already holds `bootstrapping-project` from the first
  run, so it is a ready overwrite target. To prove stale files are removed, add a
  throwaway file inside the deployed copy before re-running, then confirm it is
  gone afterwards.
- Run. `bash deploy.sh /Users/gilllesmourgues/Workspace/chief-of-droids bootstrapping-project`
- Pass. The destination is replaced with no leftover files (the copy step does
  `rm -rf` on the destination first). `DEPLOYED.md` gains a second row for the
  skill, since the record is append-only and keeps history rather than
  de-duplicating. `DEPLOYMENTS.md` gains a second run row.

## When all four pass

Update `DEPLOYING.md`: note each path as exercised, move Status to `Final`, and
bump the version block. Record the validating runs in `DEPLOYMENTS.md` as they
happen (the script does this automatically).

## Records touched by any run

- `skills-lab/DEPLOYMENTS.md`, outbound ledger, one row per run.
- `<target>/.claude/skills/DEPLOYED.md`, install record, one row per skill.

Both are written by the script. Committing them is a separate step, as it was for
the first run.

---

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-07-19 |
| Status       | Draft      |
