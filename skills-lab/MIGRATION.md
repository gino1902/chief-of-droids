# Migration plan: isolate skills-lab from the consumer tree

This plan carries out the architecture in `README.md`. The goal is that authoring and testing skills never contaminates day-to-day work in chief-of-droids, and that each skill has one canonical copy in any tree where Claude Code discovers skills.

Success looks like this. A Claude Code session run anywhere inside chief-of-droids no longer discovers the lab's twelve in-progress skills. No skill name resolves to two different copies within the same repository. The lab keeps its full authoring history and its release tooling still works.

## Scope

This document is the execution phase of a decision already made, not a fresh piece of analysis. The session set out to decide where skills-lab should live relative to chief-of-droids, to ground that in evidence, and to rephrase the outcome for alignment. That decision is settled: the lab moves to its own repository outside the consumer tree. What follows plans how to carry the decision out.

Naming this plainly matters. Producing a full migration plan extends the session past its original goal of deciding, into planning the migration and the surrounding skill-copy hygiene. That extension was asked for and is intended. It is recorded here as a conscious expansion of the goal rather than left as unmanaged scope drift.

## Why separation does most of the work

skills-lab is currently a subfolder of chief-of-droids and shares its git repository. Because Claude Code discovers skills on demand from nested `.claude/skills` directories below the working directory, a session started at the chief-of-droids root pulls the lab's twelve skills into context the moment it touches a file under `skills-lab/`. Several of those are drafts and several collide by name with released copies.

Moving the lab to a repository outside the chief-of-droids working tree removes this at the source. Parent-directory discovery walks up only to the repository root, and nested discovery only reaches down into subdirectories of the working tree, so a sibling repository is invisible to chief-of-droids sessions. Once the lab is out, the two same-tree collisions (`bootstrapping-project` at the root versus in the lab, and the wiki trio in the lab versus in wiki-data) no longer exist, because only one side remains in the chief-of-droids tree.

The one way a separated lab could still leak in is `--add-dir` or `/add-dir`, which is the documented exception that does load `.claude/skills` from an added directory. The guardrail is simply not to add the lab directory into a consumer session.

## Decisions, locked

These were settled in session and drive the steps below.

1. The separated repository lives at `Workspace/skills-lab`, a sibling of chief-of-droids and outside the consumer tree, which is what makes it undiscoverable to chief-of-droids sessions.

2. History is preserved with `git subtree split`, so the lab carries its authoring history into the new repository. The final adopt mechanic, meaning whether the split branch is cloned or imported into a repository, is settled by a person at the git-config gate in Phase 1. A fresh `git init` remains the fallback if a clean slate is preferred, at the cost of the authoring history.

3. `deploy.sh` is kept as the copy-at-release channel for external target projects and for the chief-of-droids root. Subfolders under the root, such as wiki-data, inherit the root's skills by parent-directory discovery and hold only skills unique to them. This inheritance rule is enforced at deploy time by the gate added in Phase 5.

4. No skills were deployed anywhere before this migration except `bootstrapping-project` into the chief-of-droids root. That single row is the entire ledger cleanup, handled in Phase 2.

## Current state, verified

Skills discoverable inside chief-of-droids today:

- The root `.claude/skills/` holds `bootstrapping-project`, a copy deployed from the lab, plus its `DEPLOYED.md` record.
- `skills-lab/.claude/skills/` holds twelve skills, the authoring source of truth.
- `wiki-data/.claude/skills/` holds `authoring-overview`, `ingesting-sources` and `wiki-audit`. This directory is gitignored, so these are untracked hand-copies that can drift from the lab source without any git trace.

Same-tree name collisions today: `bootstrapping-project` (root and lab), and the wiki trio (lab and wiki-data).

## Target topology

```
Workspace/
  skills-lab/            PRODUCER, its own repo, outside chief-of-droids
    .claude/skills/      the twelve skills, authoring source of truth
    deploy.sh            copy-at-release into consumers, gated and SHA-pinned

  chief-of-droids/       MAIN consumer, its own repo
    .claude/skills/      released shared skills, one canonical copy each
    wiki-data/           END consumer, inherits root skills by parent discovery
      .claude/skills/    only skills unique to wiki-data
```

## Phase 0: prepare and freeze

The goal is a safe starting point that can be abandoned without loss.

Work on a branch in chief-of-droids rather than on main. Confirm the tree is clean first, because the separation step reads history and an unclean tree makes the result ambiguous. Record the current skill inventory and the two collisions as the before-state, so the after-state can be checked against it.

Verification checkpoint: the branch exists, `git status` is clean, and the before-state inventory is written down.

## Phase 1: separate the lab into its own repository

The goal is a standalone lab repository outside the chief-of-droids working tree, with history preserved.

Carve the subfolder out with history, then adopt it as a sibling repository.

```
# from chief-of-droids, on the working branch
git subtree split -P skills-lab -b skills-lab-split

# create the sibling repo from that branch
git clone . ../skills-lab-new
cd ../skills-lab-new
git checkout skills-lab-split
git branch -M main
# remove branches and remotes that point back at chief-of-droids, then
# rename the directory to Workspace/skills-lab once verified
```

Human gate. Before the sibling repository takes its first commit or any push, a person validates its git config. Confirm `user.name` and `user.email` are correct for the lab, confirm the intended remote is set and points where you expect, and confirm no chief-of-droids remote or branch was carried over. Nothing is pushed and nothing is removed from chief-of-droids until this check passes.

After the sibling repository is confirmed good, remove `skills-lab/` from chief-of-droids in a commit, so the lab no longer lives in the consumer tree.

`deploy.sh` needs no edit. It derives its own root from the script location and runs git against whatever repository contains it, so it keeps working from the new location and its SHAs now come from the lab's own history.

Verification checkpoint: the sibling repository holds all twelve skills and the lab files, its `git log` shows the authoring history, and a Claude Code session started at the chief-of-droids root no longer lists the lab skills after touching a former-lab path. The `bootstrapping-project` collision is gone because only the root copy remains in chief-of-droids.

## Phase 2: one canonical copy per shared skill at the root

The goal is that any skill meant to be shared across chief-of-droids lives at the root and nowhere below it.

The root already holds `bootstrapping-project`. Decide which other lab skills, if any, are genuinely shared across chief-of-droids work rather than needed only in one subfolder. Deploy those to the root from the lab with `deploy.sh`, which enforces the footer-status gate so no draft lands. Do not deploy a skill to the root only to satisfy one subfolder, because every root skill is then discovered by every chief-of-droids session and adds to the instruction load.

The root's `bootstrapping-project` is a pre-migration copy whose recorded SHA no longer resolves against the new lab repository. Make it clean rather than leave it dangling. After the new lab repository exists and has at least one commit, delete `chief-of-droids/.claude/skills/bootstrapping-project`, re-baseline `chief-of-droids/.claude/skills/DEPLOYED.md` by removing the stale pre-migration row, then redeploy from the new lab with `deploy.sh` so the fresh row carries a SHA that resolves. Deleting the directory alone is not enough, because `deploy.sh` appends to `DEPLOYED.md` rather than rewriting it, so the stale row would otherwise survive next to the new one.

Verification checkpoint: the root `.claude/skills/` contains exactly the intended shared set, each present once, each with a `DEPLOYED.md` row recording its version.

## Phase 3: remove internal duplicates and drift

The goal is that wiki-data's three skills are traceable and single-sourced rather than untracked hand-copies.

The wiki trio is wiki-specific, so keep it in wiki-data rather than lifting it to the root. Replace the untracked hand-copies with a gated deploy from the lab, so each carries a recorded version and cannot silently drift.

```
# from the relocated lab
bash deploy.sh ../chief-of-droids/wiki-data authoring-overview ingesting-sources wiki-audit
```

If wiki-data's `.claude/skills` should stay gitignored, keep it so. The deploy records the version in `DEPLOYED.md` regardless, which is the traceability that the hand-copies lacked.

Verification checkpoint: each wiki skill in wiki-data matches a known lab version, and a session started in wiki-data discovers the root's shared skills by inheritance plus the wiki trio locally, with no directory-qualified duplicate variants.

## Phase 4: confirm the distribution channel

The goal is a single, documented way that released skills reach consumers.

Keep `deploy.sh` as the release channel for external target projects and for the chief-of-droids root. Confirm the ledgers still record correctly from the new lab location. Update `DEPLOYING.md` so its paths reflect the lab as a sibling repository rather than an inner folder.

Verification checkpoint: a test deploy from the relocated lab into a scratch target lands the skill, passes the gates, and writes both ledger rows.

## Phase 5: guardrails against regression

The goal is that the separation does not quietly undo itself.

Update `chief-of-droids/README.md`, which still lists `skills-lab/` as an inner folder and points at an inner `deploy.sh`, to describe the lab as a sibling repository. Add a short note in the chief-of-droids project instructions that no `.claude/skills` directory inside chief-of-droids may hold a skill whose name also exists at another discoverable tier, and that the lab directory must not be added to a consumer session with `--add-dir`.

Add a collision gate to `deploy.sh`. Before copying, it walks up from the target path to the enclosing git root and refuses, or warns, if any `.claude/skills` on that path already holds the skill being deployed, because the target would inherit that copy and the deploy would recreate the same-tree collision. The gate applies only to targets inside a repository whose root carries the skill, not to external target repositories or to the root itself.

Verification checkpoint: the README and project instructions reflect the new topology, the collision gate refuses a duplicate deploy in a test, and a scan finds no skill name present at two discoverable tiers within chief-of-droids.

## Phase 6: end-to-end verification

Re-run the before-state checks from Phase 0 as after-state checks.

Confirm that a session at the chief-of-droids root lists no lab skills. Confirm that no skill name resolves to two copies within chief-of-droids. Confirm that the lab repository still authors and deploys. Compare against the recorded before-state and note anything that changed unexpectedly.

## Rollback

Until the removal commit in Phase 1 is merged to main, rollback is discarding the working branch and deleting the sibling repository. The original tree is untouched. After merge, restoring the inner folder means reverting the removal commit, though the cleaner recovery is to redeploy needed skills from the lab rather than to reabsorb it.

## Caveats

Deploy SHAs recorded before the migration point at chief-of-droids history, not the lab's. The existing `DEPLOYED.md` row for `bootstrapping-project` at `53663ce` resolves against chief-of-droids, and `git subtree split` rewrites commit hashes, so that SHA will not resolve in the new lab repository. Either re-baseline the ledgers with a note that pre-migration versions resolve against chief-of-droids history, or accept that pre-migration rows are historical only. New deploys after the move resolve cleanly against the lab.

| Field        | Value      |
|--------------|------------|
| Version      | 1.2        |
| Last Updated | 2026-07-21 |
| Status       | Draft      |
