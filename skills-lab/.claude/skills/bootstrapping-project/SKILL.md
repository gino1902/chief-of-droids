---
name: bootstrapping-project
description: >
  Bootstraps a Claude Code project in four ordered, resumable passes:
  environment (git init + .claude/ baseline config), FRAMING.md (intent anchor —
  why, for whom, what success is, what is delivered, what constraints apply), project tree, then
  CLAUDE.md written last to document the tree that now exists. Use this whenever
  the user wants to bootstrap, scaffold, set up, initialize, or start a new
  project or repo, or configure a repo's Claude setup. Trigger even when the user
  names only one piece ("init CLAUDE.md", "set up permissions", "add a FRAMING",
  "scaffold the folders") — the skill sequences the rest and resumes wherever the
  repo already is. NOT for editing product code inside an already-bootstrapped
  repo, and NOT for Claude Desktop projects (this is Claude Code only).
argument-hint: "[thinking|code|infra] [target-path]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

<!-- target-environment: claude-code | target-model: claude-opus-4-8 -->
<!-- claude aligned to project type; same for tone; framing delegated to framing-project for Medium+ (Pass 2) -->

# bootstrapping-project

Bootstraps a Claude Code project through four passes that always run in the same order:

1. **Pass 1 — environment.** `git init` and a baseline `.claude/` configuration.
2. **Pass 2 — FRAMING.md.** The intent anchor: why, for whom, what success is, what is delivered, what constraints apply.
3. **Pass 3 — project tree.** The source layout that will hold the deliverables named in Pass 2.
4. **Pass 4 — CLAUDE.md.** Written last, so it documents a tree that already exists.

The order is locked and load-bearing. Pass 1 comes first because its permission defaults
unblock frictionless writes for every pass after it. Pass 2 comes before anything derived
from it, so intent is settled at the cheapest point to change your mind. Pass 3 turns that
intent into folders. Pass 4 is last so CLAUDE.md describes real paths and commands rather
than guessing them — the same reason the built-in `/init` documents an existing repo
instead of inventing one.

## Principles

These come from the `smart-init` requirements and shape every pass. Explaining them
here so the model applies them by judgement, not by rote.

- **Less is more.** Instruction-following degrades as instruction count grows. Generated
  files stay short (FRAMING.md and CLAUDE.md each aim for under 60 lines) and every line
  must be grounded in the repo or in what the user told you. If a line would not change
  what Claude does, cut it.
- **Enforcement beats prose.** A hard prohibition ("never deploy", "never touch prod")
  belongs in `settings.json` deny rules or a hook, which enforce at 100%, not in CLAUDE.md
  prose, which is followed about 70% of the time. When you find a hard rule, route it to
  enforcement and propose it — do not just write it as a sentence.
- **Reconcile, never regenerate.** An artifact that already exists is never overwritten.
  It is reconciled through a minimal, approval-gated diff that preserves the author's
  wording. This is also what makes the skill resumable.
- **Goal-locked.** The project goal (thinking / code / infra) is decided once, stamped,
  and read by every later pass. It selects the tree and the CLAUDE.md skeleton.
- **One goal per repo.** A repo holds a single goal, and the stamp enforces it. When a
  project spans goals (an app and its infrastructure, a data platform and a service) that is
  more than one repo, each bootstrapped separately with its own CLAUDE.md and permissions.
  The boundary is deliberate: things that differ in lifecycle, blast radius, access control,
  or how Claude should work here do not belong in one tree, because merging them forces the
  strictest rule on everyone and ties their fates together. Compose across repos by reference
  (a CLAUDE.md pointer), never by merging trees. Collapsing the boundary is a choice the user
  makes explicitly — splitting a merged repo later is the expensive direction.

## Reference files

Load the file for the pass you are running, not all of them up front.

| File | Load when | Holds |
|:--|:--|:--|
| `references/environment.md` | Pass 1 | Baseline `settings.json`, `.gitignore`, git-init steps, what to defer |
| `references/framing.md` | Pass 2 | FRAMING.md template, the five framing questions, goal stamp, reconcile rules |
| `references/trees.md` | Pass 3 | Per-goal project trees and their deferred directories |
| `references/claude-md.md` | Pass 4 | Per-goal CLAUDE.md skeletons, grounding test, enforcement + Karpathy checks |

## Preamble — orient, then resume

Run this before any pass.

1. **Resolve the target.** Default to the current working directory. If a path was passed
   as the second argument, use it. State which directory you are bootstrapping.
2. **Detect what already exists**, to know which passes are done and where to resume:
   - Pass 1: a `.git/` directory at the target root and a `.claude/settings.json`.
   - Pass 2: a `FRAMING.md` at the repo root.
   - Pass 3: any source files or a scaffolded tree (more than just config and framing).
   - Pass 4: a `CLAUDE.md` at the repo root.
3. **Resolve the goal.**
   - If `FRAMING.md` exists, read the goal from its `<!-- goal: ... -->` stamp. This is
     the locked goal. If an argument was passed that conflicts with the stamp, stop and
     report the conflict — do not proceed.
   - Otherwise, take the goal from the first argument if it is one of `thinking`, `code`,
     `infra`. If absent or invalid, ask the user once. Hold it — it gets stamped in pass 2.
4. **Report status and resume at the first incomplete pass.** Show a short line per pass
   (done / to do) and start at the earliest one that is not done. The user can override
   and target a specific pass, including re-running a done pass in reconcile mode.

Never proceed from memory if a reference file is unreachable — say so and stop.

## Pass 1 — environment

Goal-agnostic. Establishes the operating environment and the permission defaults that
make later writes frictionless.

1. Read `references/environment.md`.
2. If there is no `.git/` at the target root, confirm with the user that the project should
   own its own repo, then run `git init`. A `.git/` in an enclosing parent directory does not
   count — init the project's own repo at the target root unless the user declines.
3. Compose the baseline `.claude/settings.json` and a baseline `.gitignore` from the
   templates in the reference. Show both before writing — settings change behaviour, so
   they are approval-gated even though the templates are conservative.
4. Write them on approval. `settings.json` is written exactly once, here — no later pass
   mutates it (the pass 4 tail proposes enforcement, it does not write it). Do **not**
   scaffold hooks, MCP config, or subagents now. Those depend on the stack, which is not
   known yet. They are proposed at the tail of pass 4.

## Pass 2 — FRAMING.md

The intent anchor, and the one file that is mostly user-supplied rather than repo-grounded.
FRAMING.md is user-owned after creation — never modify it autonomously in a later session.

1. Read `references/framing.md`.
2. If `FRAMING.md` exists, route the rework by how it was created so it matches the creation
   branch. If the frontmatter carries a `last_updated` key (a `framing-project` doc), invoke
   the `framing-project` skill and let its update phase handle the rework. Otherwise (the Small
   five-question doc — goal stamp on line one, no `last_updated`) reconcile inline: propose a
   minimal diff for gaps only, keep the author's wording, apply on approval. Either way, do not
   ask the size question on this path, and preserve the goal stamp. Then continue to Pass 3.
3. Otherwise, ask once whether this is a **Small** project (solo or short-lived, one workflow,
   no formal sponsor) or **Medium+** (multiple teams or tracks, a sponsor, real budget). This
   only chooses how framing is produced. It is not stamped and does not change the goal.
4. **Small — frame inline.** Ask the five framing questions (why, for whom, what success is,
   what is delivered, what constraints apply). Keep answers tight. Leave any unanswered section
   marked `🔲` rather than inventing content. Write FRAMING.md with the goal stamp as the first
   line. The Small path deliberately skips `CONCEPTS.md` — a solo, single-workflow project does
   not need a domain-language artifact. If it later grows, a `framing-project` run seeds one.
5. **Medium+ — delegate to `framing-project`.** Invoke the `framing-project` skill (via the
   Skill tool) and let it run its interview, write FRAMING.md, and seed the companion
   `CONCEPTS.md` (the domain language). Do not duplicate the interview yourself. `framing-project` does not write the goal stamp, so when it returns, inject
   `<!-- goal: <locked-goal> -->` immediately after the YAML frontmatter if it is not already
   there. `framing-project` writes at the working-directory root — if you are bootstrapping a
   different target path, run it from that directory or move the produced FRAMING.md into the
   target.
6. Either path keeps the goal locked in the Preamble. Later passes read the goal from the stamp
   by pattern, not by line position, so it works whether the stamp is line one (Small) or just
   under the frontmatter (Medium+).

## Pass 3 — project tree

1. Read `references/trees.md`.
2. If the repo already has source files, do not propose a reorganisation. Document the
   existing structure so pass 4 can describe it, and skip creation.
3. If the repo is empty of source, propose the tree matching the locked goal (for `code`,
   ask the one sub-type question: data or app). Create the directories via `.gitkeep` only
   after the user approves. Leave deferred directories deferred — each directory must be
   justified now, not speculatively.

## Pass 4 — CLAUDE.md

Written last so it documents the tree that now exists.

1. Read `references/claude-md.md`.
2. If `CLAUDE.md` exists, reconcile against the matching skeleton: fill gaps, move hard
   rules to enforcement, drop ungrounded lines. Preserve wording. Apply on approval.
   Otherwise create it from the skeleton for the locked goal.
3. Fill only from what you found in the repo and from FRAMING.md. Delete any line you
   cannot ground — never invent commands or paths. Keep it under 60 lines.
4. **Tail — enforcement and Karpathy.** For any hard prohibition you found, propose matching
   `settings.json` deny rules and hooks in this close report — never write them into
   `settings.json`, which was written once in pass 1 and is not touched again. Quote each
   proposed deny rule in one canonical glob form so runs do not drift on the pattern. If
   `~/.claude/CLAUDE.md` does not carry the Karpathy behavioural guidelines, tell the user to
   install them there once — they are project-independent and do not belong in a project
   CLAUDE.md.

## Close

Report what each pass produced and what was deferred (stack-specific hooks, MCP, any
`🔲` framing gaps). Remind the user that FRAMING.md is theirs to complete before
substantive work.

## Gotchas

- **The order is not negotiable.** Resuming means picking up at the first incomplete pass,
  not reordering. Pass 1 appears first even on resume because its permissions matter to the rest.
- **FRAMING.md is user-owned.** Reconcile it only with approval, and never rewrite it wholesale.
- **CLAUDE.md is grounded, not aspirational.** It is written after the tree exists precisely
  so its paths and commands are real. If you cannot verify a command, drop the line.
- **Hard rules do not live in prose.** Route them to deny rules and hooks, and propose them.
- **This is Claude Code, not Desktop.** No artifacts, no Filesystem MCP, no system-prompt XML.
  Files are written directly with the file tools.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.9        |
| Last Updated | 2026-07-13 |
| Status       | Review     |
