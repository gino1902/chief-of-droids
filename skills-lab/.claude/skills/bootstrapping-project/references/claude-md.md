<!-- pass 4 reference for bootstrapping-project -->

# Pass 4 — CLAUDE.md

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

Append two pointer lines as the final lines of every generated CLAUDE.md, regardless of goal, so
each deferral is explicit and checkable rather than a silent omission:

```markdown
> Structural conventions (import, dependency, promotion rules) live in `CONVENTIONS.md`, enforced
> by the project lint config and gate, not restated here.
> Behavioural conduct (think-before-coding, simplicity-first, surgical changes, goal-driven
> execution) lives at user level in `~/.claude/CLAUDE.md`, not duplicated here.
```

The `CONVENTIONS.md` pointer is why CLAUDE.md does not carry the tree's structural rules: they
have a durable home of their own (written in Pass 3), so CLAUDE.md references it and stays inside
its 60-line budget. The Pass 4 tail then verifies the behavioural-conduct file actually carries
those guidelines and warns if it does not.

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
<one bullet per FRAMING Constraint, in the order they appear there, each carried in imperative
form using that constraint's own wording. Do not add, merge, split, or reword them, and do not
synthesise extra conventions from the tree layout — the tree's structural rules live in
`CONVENTIONS.md`, reached via the appended pointer, not here. If FRAMING states no Constraints,
fall back to up to 5 load-bearing negatives verified in the repo.>
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

## Worked example — a filled code CLAUDE.md

This is the target shape for the `code` skeleton, filled from a brief and documenting a tree
that already exists. It embodies the fixed layout rules from `trees.md` — flat `src/` + `apps/`,
kebab-case domain folders — and it is grounded: every command is one the project actually runs,
and Conventions maps one bullet to each FRAMING Constraint, in FRAMING's order, using the
constraint's own wording. Under 60 lines. Here the brief carries five constraints (the two
architectural boundaries, the Prisma-only data-access rule, the test-placement rule, and the
auth rule), so five conventions appear — the count follows FRAMING, it is not a target, and no
convention is inferred from the tree. The `thinking` and `infra` skeletons follow the same fill
discipline, so this one example is the pattern for all three.

```markdown
<!-- goal: code -->
# CLAUDE.md

## Purpose
shift-planner builds a venue's weekly staff rota in one place and flags unfilled shifts and
double-bookings as the manager assembles the week.

## Stack
- TypeScript, package manager pnpm.
- Frontend: React with Vite, bulletproof-react layout.
- Backend: Node.js with Fastify (REST), nodebestpractices layout.
- Database: PostgreSQL via Prisma.
- Tests: Vitest (unit and component), Playwright (end-to-end); ESLint plus `tsc --noEmit`.

## Structure
- `src/` — React frontend. `app/` routes and providers, `features/` self-contained modules,
  plus `components/`, `config/`, `testing/`, `types/`, `utils/`.
- `apps/` — backend, one folder per domain (`shifts/`, `staff-members/`, `leave-requests/`),
  each split into `entry-points/api/`, `domain/`, `data-access/`.
- `e2e/` — Playwright end-to-end tests, outside `src/`.

## Commands
- Install: `pnpm install`
- Build: `pnpm build`
- Single test: `pnpm vitest run <file>`
- Lint and typecheck: `pnpm lint && pnpm tsc --noEmit`
- End-to-end: `pnpm playwright test`

## Conventions
- Frontend features are self-contained. Compose them at the `app/` layer, never import across features.
- Split each backend domain into entry-points, then domain, then data-access. Name folders for the business domain, not the framework.
- Access PostgreSQL only through Prisma. Single instance, no microservices at this stage.
- Co-locate frontend tests with source. Test backend domains through their `api/` entry-point over HTTP.
- Auth is email plus password only. No third-party auth provider yet.
```

## Reconcile mode (CLAUDE.md already exists)

Do not regenerate. Read the goal from the stamp. Map the existing file onto the matching
skeleton and propose a minimal diff:

- gaps to fill, marked `🔲`
- rules that belong in deny rules or hooks, to move out to enforcement
- lines that fail the grounding test, to drop (the goal stamp and Purpose are exempt)

Preserve the author's wording everywhere else. Show the diff, apply only on approval.

The tail below still runs in reconcile mode. On a pre-feature repo — one bootstrapped before the
contract existed, so it has a tree and a `CLAUDE.md` but no lint config, no gate, and no
`scripts/check-conventions-drift.sh` — the tail backfills all three against the existing tree.
Absence is the trigger: generate what is missing, reconcile what is present, never regenerate.

## Tail — enforcement and Karpathy

1. **Route hard rules to enforcement — propose, never write.** For any hard prohibition you
   found (deploy commands, `apply` without plan, secret paths, prod access), surface a
   matching `settings.json` deny rule and, where a command needs intercepting, a hook — as a
   proposal in this close report only. Do not edit `settings.json`: it was written once in
   pass 1 and no later pass touches it (see `environment.md`). Enforcement holds at 100%;
   prose holds at about 70% — but the user applies the enforcement, the skill does not write
   it silently. This is also where the stack-specific configuration deferred from pass 1 gets
   proposed, now that the stack is known. When you do quote a proposed deny rule, use one
   canonical glob form per command (`Bash(pnpm deploy)` and `Bash(pnpm deploy:*)`), so two
   runs proposing the same rule quote it identically rather than drifting between `deploy *`
   and `deploy:*`.
2. **Generate the structural enforcement — write config and gate, not `settings.json`.** The
   `CONVENTIONS.md` contract written in pass 3 states the import, dependency, and promotion
   rules; now that the stack is confirmed, make them a 100% gate. Generate, approval-gated: the
   lint config encoding the structural boundaries (ESLint `import/no-restricted-paths` zones for
   the app goals, TFLint for infra, ruff for data) and the project gate that runs it. Pin the
   gate per stack so two runs of the same brief agree, grounded in each goal's reference standard:
   a husky pre-commit hook for the Node/TS app goals (bulletproof-react's recommendation), whose
   body is the pinned template below and whose lint runner is the canonical `npx eslint .` — the
   flat config's `files` glob already scopes it to `apps/`, so there is one right form, not
   `eslint apps` versus `eslint .`; a `.pre-commit-config.yaml` using `astral-sh/ruff-pre-commit`
   (official hook ids `ruff-check` and `ruff-format`) for the data goal; a `.pre-commit-config.yaml`
   with terraform fmt, validate, tflint plus TFLint in CI for infra. If the repo already has a gate
   installed, reconcile to it rather than forcing the default — the pin only removes the free
   choice on a blank repo. These are stack files, so writing them does not touch `settings.json`,
   whose pass-1 freeze stands. Constrain generation two ways: only for tooling the confirmed stack actually
   uses, and only zones for folders that exist — where per-feature or per-domain folders are
   still deferred, leave a documented extend-per-feature marker rather than fabricating zones for
   absent paths (the grounding test applies to config too). Record the config file path and the
   runner command back into `CONVENTIONS.md` so the drift-check can bind the two. The `thinking`
   goal has no lint equivalent; its gate is review, so generate no config and say so in the
   report. An additive allowlist offer for the runner (for example `Bash(pnpm lint)`) is fine —
   that is the existing pass-1 offer path, not a new mutation.

   **Pinned app hook — write byte-for-byte, do not paraphrase.** Model-authored prose in the gate
   is what makes two runs of one brief diverge, so the app husky hook has a fixed body. For the
   app goal, `.husky/pre-commit` is exactly:
   ```sh
   #!/usr/bin/env sh
   npx eslint .
   bash scripts/check-conventions-drift.sh .
   ```
   No `. husky.sh` sourcing line (deprecated husky v8 style), no comment prose, no `eslint apps`
   variant. The second line is the drift-check base pass from step 3, already in the template so
   the file is complete and identical run to run. `CONVENTIONS.md` records `runner: npx eslint .`
   to match.
3. **Deliver and wire the lifecycle drift-check — the guard ships with the project.** The
   contract's whole point is fidelity over the project's life, so the check that guards it must
   live in the project, not only in the skill author's test suite. Copy the skill's
   `assets/check-conventions-drift.sh` to `scripts/check-conventions-drift.sh` in the project and
   make it executable. Wire its base pass — existence and coverage, run with no base argument — as
   the line `bash scripts/check-conventions-drift.sh .`. For the app goal that line is already in
   the pinned husky template above, so do not add it twice; for the pre-commit and CI gates, add it
   as a local hook or step. Either way every commit then catches a config that stopped existing or
   a new domain or feature folder with no zone. The traceability pass needs a base commit to diff against, which only a pull request has,
   so document its exact invocation `bash scripts/check-conventions-drift.sh . <base>` (base is
   the branch's merge target) as the CI step to add, and generate that CI step only where the
   project's CI platform is confirmed — never fabricate a workflow for an unknown platform, the
   grounding test again. The `thinking` goal ships the script too: its config and coverage are
   none, but the traceability guard over `CONVENTIONS.md` and `decisions/` still applies.
4. **Resolve the conduct reference — check, read, apply.** The skill instantiates the *project*
   CLAUDE.md, so the apply target is that file — never the user's global config, and the skill
   installs nothing into the user's environment.
   - **Check** whether the user-level behavioural conduct exists (default location
     `~/.claude/CLAUDE.md`).
   - **Read** it to confirm the location and that it carries the guidelines.
   - **Apply** the appended pointer lines into the project CLAUDE.md: the `CONVENTIONS.md`
     pointer always, and the behavioural-conduct pointer pointing at that location.
   If the conduct is absent, do not fabricate the reference — omit the conduct pointer and
   surface a warning in the close report telling the user to install the guidelines at user level
   (github.com/forrestchang/andrej-karpathy-skills). They are project-independent: the project
   file references them, it never holds or installs them. The `CONVENTIONS.md` pointer is
   unaffected — that file is always written in pass 3.

## Note on the footer

The generated CLAUDE.md is a project config file, not one of this repo's workflow outputs,
so it takes the goal stamp as its first line and does not need the version-block table.

---

| Field        | Value      |
|--------------|------------|
| Version      | 1.10       |
| Last Updated | 2026-07-18 |
| Status       | Review     |
