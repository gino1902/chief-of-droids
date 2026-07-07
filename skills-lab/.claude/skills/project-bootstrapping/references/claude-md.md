<!-- pass B reference for project-bootstrapping -->

# Pass B — CLAUDE.md

Written last, so it documents the tree that already exists rather than guessing at one.
This is the same discipline the built-in `/init` follows: describe what is there.

## Grounding test

The single rule that keeps CLAUDE.md useful: for every line, ask whether removing it would
cause Claude to make a mistake here. If not, cut it. Never invent commands, paths, or
versions — verify a command exists before you write it, and delete the line if you cannot.
Keep the whole file under 60 lines.

Purpose comes from FRAMING.md (the "why", condensed to one sentence) or from the README.
The goal stamp and Purpose are exempt from the grounding test — everything else is not.

Behavioural rules that apply everywhere (the Karpathy guidelines) do not belong here. They
live once at user level. See the tail check below.

## Skeletons

Use the skeleton for the locked goal. Fill only from what you found. Delete unfilled lines.

### thinking

```markdown
<!-- goal: thinking -->
# CLAUDE.md
## Purpose
<one sentence, from FRAMING.md>
## Structure
<where ADRs, notes, diagrams live — from the actual tree>
## How to work here
- Challenge ideas. Surface tradeoffs and counterarguments. Do not agree by default.
- Minimal-intervention edits. Preserve the author's language and structure.
- Decisions use ADR format. Accepted ADRs are never edited — supersede with a new record.
  Open questions stay marked 🔲, never silently resolved.
```

### code

```markdown
<!-- goal: code -->
# CLAUDE.md
## Purpose
<one sentence, from FRAMING.md>
## Stack
<language, package manager, versions — verified>
## Structure
<map of the tree — critical if monorepo>
## Commands
<build / single test / lint+typecheck — each verified to exist>
## Conventions
<max 5 load-bearing rules from the repo, imperative, include negatives>
```

### infra

```markdown
<!-- goal: infra -->
# CLAUDE.md
## Purpose
<one sentence, from FRAMING.md>
## Stack
<Terraform providers, bundle targets, environments>
## Structure
<modules, environment roots — from the actual tree>
## How to work here
- Plan-first: show plan/diff before any apply. If the target environment is ambiguous, stop and ask.
- Ground provider arguments in official docs. Flag unverified schema rather than guessing.
- <negative rules found in the repo: network boundaries, secret references, residency constraints>
```

## Reconcile mode (CLAUDE.md already exists)

Do not regenerate. Read the goal from the stamp. Map the existing file onto the matching
skeleton and propose a minimal diff:

- gaps to fill, marked `🔲`
- rules that belong in deny rules or hooks, to move out to enforcement
- lines that fail the grounding test, to drop (the goal stamp and Purpose are exempt)

Preserve the author's wording everywhere else. Show the diff, apply only on approval.

## Tail — enforcement and Karpathy

1. **Route hard rules to enforcement.** For any hard prohibition you found (deploy commands,
   `apply` without plan, secret paths, prod access), propose — do not silently write —
   matching `settings.json` deny rules and, where a command needs intercepting, a hook.
   Enforcement holds at 100%; prose holds at about 70%. This is also where the stack-specific
   configuration deferred from pass A gets proposed, now that the stack is known.
2. **Check the Karpathy guidelines.** If `~/.claude/CLAUDE.md` does not contain them, tell
   the user to install them there once (github.com/forrestchang/andrej-karpathy-skills).
   They are project-independent and must not be copied into a project CLAUDE.md.

## Note on the footer

The generated CLAUDE.md is a project config file, not one of this repo's workflow outputs,
so it takes the goal stamp as its first line and does not need the version-block table.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-07 |
| Status       | Review     |
