# Bootstrapping resume test — SM-3

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this across two fresh sessions. It also diversifies project type: this is the only infra-goal scenario, so it exercises the infra tree and CLAUDE.md skeleton.

## Purpose

Exercise `bootstrapping-project` resume. Interrupt it after Pass 1, then re-invoke in a new session and confirm the Preamble detects Pass 1 as done and resumes at Pass 2 rather than redoing environment setup. The straight chain tests ran all four passes in one sitting, so resume detection was never triggered.

## Directory and precedence

Directory: `outputs/test-resume`, created by this test in its first session.

Precedence: self-contained. Two sessions, session one does Pass 1 only, session two resumes. No dependency on other scenarios.

## Preconditions

- Two fresh sessions, back to back.
- The directory `skills-lab/outputs/test-resume` exists and is empty. Session cwd is that directory in both sessions.

## Scripted subject — "edge-dns"

A solo infra project: Terraform for one person's personal edge and DNS configuration. Genuinely Small (solo, no sponsor), goal `infra`.

## Run steps

### Session one — Pass 1 only

Invoke `bootstrapping-project`. Goal `infra`. Complete Pass 1 only: approve the baseline `.claude/settings.json` and `.gitignore`. Then stop, do not proceed to Pass 2. End the session.

At this point `outputs/test-resume` holds only `.claude/settings.json` and `.gitignore` (and `.git` if init ran), and no `FRAMING.md`, tree, or `CLAUDE.md`.

### Session two — resume

In a new session, cwd still `outputs/test-resume`, re-invoke `bootstrapping-project`.

Expected: the Preamble detects Pass 1 done (settings present), reports it, and resumes at Pass 2. Continue as a Small infra project:

- Pass 2 size: Small (inline five-question framing).
  - Why: my edge and DNS config drifts by hand-editing in the console, and I cannot tell what changed.
  - For whom: me, solo.
  - Success: every change goes through a reviewed plan, for a month, with no console hand-edits.
  - Delivered: Terraform modules and thin per-environment roots.
  - Constraints: one cloud account; plan before every apply.
- Pass 3: the infra tree (`modules/`, `envs/<env>/`), no code sub-type question.
- Pass 4: the infra `CLAUDE.md` skeleton (plan-first, ground provider args, negative rules found in the repo).

## Expected outputs (under `outputs/test-resume`)

- From session one: `.claude/settings.json`, `.gitignore`.
- From session two: `FRAMING.md` (five-question Small, `<!-- goal: infra -->` on line one), an infra tree anchor (`modules/`, `envs/<env>/`), and `CLAUDE.md` on the infra skeleton.

## Acceptance criteria

- On resume, the skill reports Pass 1 as done and starts at Pass 2. It does not re-run `git init` or rewrite `settings.json`.
- The goal is `infra` throughout, and the tree matches the infra skeleton (`modules/`, `envs/<env>/`), not a code tree.
- `CLAUDE.md` uses the infra skeleton with a plan-first rule.
- `settings.json` from session one is unchanged after session two.

## Fail conditions

- Resume redoes Pass 1 (rewrites `settings.json` or re-inits git).
- The skill fails to detect prior state and starts from scratch.
- A code tree is scaffolded instead of the infra tree.

## Record

Note the per-pass status line the Preamble prints on resume, and confirm `settings.json` is unchanged between sessions.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
