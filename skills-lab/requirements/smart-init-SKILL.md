---
name: smart-init
description: Create a goal-locked CLAUDE.md or reconcile an existing one (thinking, code, or infra variant)
argument-hint: [thinking|code|infra] (CREATE only)
allowed-tools: Read, Glob, Grep, Write
disable-model-invocation: true
---

0. Check for an existing CLAUDE.md. This sets the mode: CREATE if absent, RECONCILE if present.
   - CREATE: goal is "$ARGUMENTS". If empty or not one of thinking|code|infra, ask the user. The goal is locked at creation.
   - RECONCILE: read the goal from the `<!-- goal: ... -->` stamp in the file. Ignore "$ARGUMENTS"; if it was provided and differs from the stamp, stop and report the conflict — do not proceed. If no stamp exists (file predates this command), ask the user once and add the stamp via the step 2-bis diff — never write it directly.
1. Scan the repo: structure (2 levels max), stack. For code|infra only: build/test/validate commands.
2. CREATE mode — write CLAUDE.md from the matching skeleton, with `<!-- goal: <goal> -->` as the first line. Purpose comes from the README or the user — ask if absent. Everything else: fill only from what you found. IMPORTANT: delete any line you cannot ground — never invent commands. Keep it under 60 lines.
2-tree. CREATE mode, only if the repo has no source files — run this before step 2. For goal code, ask one sub-type question: data or app. Propose the matching tree below and create it (via .gitkeep files) only after the user approves. Step 2 then fills the Structure section from the created tree. If source files exist, skip: document the existing structure, never propose reorganisation.
2-bis. RECONCILE mode — do not regenerate. Map the existing file onto the skeleton and propose a minimal diff: (a) gaps to fill, marked 🔲, (b) rules that belong in deny rules/hooks, to move out, (c) lines failing the grounding test, to drop — the goal stamp and Purpose are exempt, as in CREATE. Preserve the author's wording everywhere else. Show the diff and apply only after the user approves.
3. If ~/.claude/CLAUDE.md does not contain the Karpathy guidelines, tell the user to install them there once (github.com/forrestchang/andrej-karpathy-skills). They are project-independent and do not belong in this file.
4. Propose (do not write) settings.json deny rules and hooks for any hard prohibition found (deploy commands, secrets paths). Hard rules belong in enforcement, not CLAUDE.md.

## Skeleton: thinking
```markdown
# CLAUDE.md
## Purpose
<one sentence>
## Structure
<where ADRs, notes, diagrams live>
## How to work here
- Challenge ideas. Surface tradeoffs and counterarguments. Do not agree by default.
- Minimal-intervention edits. Preserve the author's language and structure.
- Decisions use ADR format. Accepted ADRs are never edited — supersede with a new record. Open questions stay marked 🔲, never silently resolved.
```

## Skeleton: code
```markdown
# CLAUDE.md
## Purpose
<one sentence>
## Stack
<language, package manager, versions>
## Structure
<map — critical if monorepo>
## Commands
<build / single test / lint+typecheck — verified to exist>
## Conventions
<max 5 load-bearing rules from the repo, imperative, include negatives>
```

## Skeleton: infra
```markdown
# CLAUDE.md
## Purpose
<one sentence>
## Stack
<Terraform providers, bundle targets, environments>
## Structure
<modules, environment roots>
## How to work here
- Plan-first: show plan/diff before any apply. If the target environment is ambiguous, stop and ask.
- Ground provider arguments in official docs. Flag unverified schema rather than guessing.
- <negative rules found in the repo: network boundaries, secret references, residency constraints>
```

## Trees (CREATE on empty repo only — each directory must be justified now, not speculatively. Resolve <placeholders> from the project name, or ask.)

### thinking
```
decisions/    ADRs (NNNN-title.md), superseded, never edited
notes/        living working and meeting notes
diagrams/     Mermaid/C4 sources
references/   documents that ground the decisions
```

### code — data
```
notebooks/    exploration only, never production logic
src/<pkg>/    importable, tested logic extracted from notebooks
tests/
conf/         environment config, no secrets
```
Deferred: data/ (gitignored) at first local sample; docs/adr/ at first decision.

### code — app
```
frontend/     only if the project has a UI
backend/      only if the project has services
```
Create only the sides the project has. Deferred: shared/ at second consumer; docs/adr/ at first decision. Tests colocate per each stack's convention.

### infra
```
modules/      reusable modules, no environment values
envs/<env>/   thin composition roots (dev, uat, prod)
```
CI files live where the platform requires (.github/workflows/, azure-pipelines.yml) — no custom dir. Deferred: split envs/<env>/ into per-component roots at the second component (state blast-radius isolation within an environment, not only across); docs/adr/ at first decision. Databricks bundle variant: databricks.yml at root, resources/ instead of modules/, targets replace env roots.
