<!-- design spec for a bootstrapping-project change; not a skill file -->

# Bootstrapping conventions, fidelity over the lifecycle

Design spec for extending `bootstrapping-project` so the tree-structure philosophy, once
chosen, produces a durable and enforceable contract that stays faithful over the project's
life, and so any change to it is a traceable decision rather than silent drift.

This is a working design doc, not a skill file. It is the thing to review the skill edits
against. It does not itself change the skill.

## Why this is needed

Grounding pass over the current skill (v1.11) found a discontinuity between Pass 3 and Pass 4.

The tree philosophy is already articulated in full. `references/trees.md` carries, per goal,
a Conventions block with a dependency rule, an import rule, a promotion rule, and an
Enforcement line that names the real mechanism. For the app goals that is ESLint
`import/no-restricted-paths` zones. For infra it is `terraform fmt` and `validate` as
pre-commit hooks plus TFLint in CI. For data it is ruff and the three test layers. For
thinking there is no lint equivalent and review is the gate.

The problem is that this articulated contract never lands in a durable, project-owned
artifact, and this is by current design.

- Pass 3's only output is empty directories via `.gitkeep`. The conventions in `trees.md`
  shape the scaffolding by judgement, then evaporate. They are reference material the model
  reads, not something written into the repo.
- Pass 4 deliberately excludes them from CLAUDE.md. `references/claude-md.md` instructs one
  bullet per FRAMING constraint and, verbatim, do not synthesise extra conventions from the
  tree layout. So the import, promotion, and dependency rules are kept out of CLAUDE.md on
  purpose.
- Enforcement is only spoken aloud. The Pass 4 tail proposes deny rules and hooks in the
  close report but writes nothing. The lint config that would hold the import rules is never
  generated, and no gate wires it in.

Net effect. The day bootstrap finishes, the import rules and promotion conventions exist only
in the transcript. Nothing in the repo states them, nothing enforces them, and nothing can
later detect drift from them. That is the fidelity-over-lifecycle hole this design closes.

## What the docs settle

The point-1 question, document-only versus generate-config, is settled by Anthropic's own
guidance, which agrees with the skill's existing Enforcement beats prose principle.

- `best-practices.md`: hooks run scripts automatically and, unlike CLAUDE.md instructions
  which are advisory, are deterministic and guarantee the action happens. The canonical
  examples given are a hook that runs eslint and a hook that blocks writes to a folder.
- `best-practices.md`: the durable gate is a check that returns a signal, a linter or a script
  that diffs against a fixture.
- `best-practices.md`: allowlist the safe runner, for example `npm run lint`.

There is no basis in the docs for document-only where a lint mechanism exists. Advisory prose
is the weaker path at about 70 percent adherence against a gate's 100 percent. So the model is
both, in layers. Document the contract, generate the config that encodes it, wire the gate
that runs it. Where the philosophy has no lint equivalent, the thinking goal, the model
degrades to documented-convention-plus-review, which `trees.md` already states.

## Decisions locked this session

1. The durable contract lives in a separate `CONVENTIONS.md` at the project root, parallel to
   `CONCEPTS.md`, not folded into CLAUDE.md. This keeps CLAUDE.md under its 60-line grounding
   budget and gives the generated lint config one clear source.
2. The skill generates the lint config and the enforcing gate, approval-gated, not just a
   proposal in the close report.
3. The lifecycle drift-check is a deterministic script under `requirements/tests/checks/`,
   runnable in CI with no skill run, staying inside the `grep`, `sed`, `cut`, `sort`, `uniq`,
   `comm`, `diff`, `git`, `jq` set, no `awk` and no interpreter.
4. Implemented after review: the four skill files, `check-conventions-drift.sh`, and the test
   suite now carry the design below. This doc is the record of intent, kept in step with the
   built artifacts.

## The key resolution, enforcement is project-native

Decision 2 appears to collide with a tested invariant. `environment.md` guarantees
`settings.json` is written once in Pass 1 and is byte-identical across runs, and scenario SM-3
tests that no later pass mutates it. A Claude Code Stop hook registered in `settings.json`
would break that.

It does not have to, and avoiding it is the better design. The enforcement homes `trees.md`
already names are all project-native, none is `settings.json`. ESLint zones, a
pre-commit config, a CI workflow, TFLint. These bind every contributor, human or Claude, and
live in stack files. A Claude Code Stop hook would only gate Claude's own sessions, which is
weaker than a project gate for a lifecycle contract that the whole team must hold.

So the generated gate is the project's own pre-commit or CI wiring that runs the lint config,
written as stack files. `settings.json` stays frozen, SM-3 stays green, the byte-identical
guarantee holds, and enforcement lands where it enforces for everyone. The only `settings.json`
touch remains what the skill already does, an allowlist offer for the lint runner, which is
additive and already inside the Pass 1 offer set.

## The grounding constraint, an empty scaffold

The skill's grounding principle forbids writing config for tools that are not installed or
paths that do not exist. At bootstrap the tree is mostly empty `.gitkeep` scaffolding.
Per-feature and per-domain folders do not exist yet, because the skill defers them to first
use. So the concrete zones that reference those folders cannot be fully populated at bootstrap.

Enforcement therefore generates in two moments, which is also why the drift-check matters.

- At bootstrap, generate the structural boundaries that are knowable now. The unidirectional
  flow shared then features then app, the tier flow entry-points then domain then data-access,
  the rule that env roots never hold resource logic. These are structural and known from the
  philosophy the moment the goal is locked.
- Over the lifecycle, as features and domains arrive, the zones extend to cover them. The
  drift-check is what catches a new feature folder added without a matching zone.

Where the chosen stack's linter is not installed at bootstrap, the config is written with a
documented extend-per-feature marker rather than fabricating zones for absent folders or
referencing an absent tool. The close report tells the user which install step activates it.

## Artifact spec, CONVENTIONS.md

Project-root file, written by Pass 3 once the tree exists, distinct from `CONCEPTS.md`.
`CONCEPTS.md` holds the domain vocabulary. `CONVENTIONS.md` holds the structural and
dependency contract. Carries a version block per the project CLAUDE.md rule.

Contents, filled verbatim from the locked goal's `trees.md` block, not re-synthesised.

- Dependency rule. Who may depend on what.
- Import rule. How imports are written, for example direct imports and no barrel files for the
  React app goal.
- Promotion rule. How code moves between layers and when, for example a concern moves to a
  shared layer at its second consumer.
- Enforcement. The mechanism name, the config file path, and the runner command. One line per.
- A pointer line back to the goal, so the drift-check can resolve which philosophy this
  contract instantiates.

Per goal.

- thinking. The record rule, naming rule, promotion rule, and the review-is-the-gate line.
  No lint config. Enforcement is review plus, at most, a naming and immutability check.
- code, data. The notebook-imports-package dependency rule, the thin-notebook rule, the
  scratch-to-src promotion rule, ruff plus the three test layers as enforcement.
- code, app. The features-never-import-each-other dependency rule, the no-barrel import rule,
  the second-consumer promotion rule, ESLint `import/no-restricted-paths` zones as enforcement.
- infra. The composition rule, module rule, pinning rule, state-and-secrets rule, the
  module-leaves-at-first-external-consumer promotion rule, `fmt`, `validate`, TFLint as
  enforcement.

## Enforcement generation spec

After Pass 3 writes the tree and `CONVENTIONS.md`, and only for the stack the project actually
uses, generate, approval-gated.

1. The lint config encoding the structural boundaries. For app, an ESLint flat config or
   `.eslintrc` with `import/no-restricted-paths` zones for the unidirectional flow and one
   zone per existing feature and domain, plus the extend-per-feature marker. For infra, the
   TFLint config. For data, the ruff config. For thinking, nothing, review is the gate.
2. The project gate that runs it. A `.pre-commit-config.yaml`, or a husky and lint-staged
   setup, or a CI workflow step, matching what the stack already uses. Never a `settings.json`
   hook. The gate runs the runner named in `CONVENTIONS.md`.
3. An additive allowlist offer for the runner command, inside the existing Pass 1 offer set,
   not a new `settings.json` mutation path.

Show the diff, apply only on approval, degrade gracefully where a tool is not yet installed.

## Drift-check spec, the deterministic script

A script under `requirements/tests/checks/`, invoked as
`check-conventions-drift.sh <dir> [<base-commit>]`. Deterministic, no skill run, built from
`git`, `grep`, `sed`, `sort` (no `awk`, no interpreter). Exit 0 pass, 1 drift, 2 usage or lookup
error. It parses `CONVENTIONS.md`'s machine-readable enforcement stanza (`config`, `runner`,
`zoned`), the same stanza the skill writes, and runs three checks.

- Coverage. For each `prefix/*` glob in `zoned`, list the prefix's immediate child folders from
  `git ls-files` (via `grep` and `sed`), then require each folder's path to appear in the lint
  config (`grep -F`). A folder with no zone is a new-feature-without-enforcement drift. Skipped
  when `zoned: none`.
- Traceability, the heart of point 2. If `CONVENTIONS.md` or the lint config changed since
  `<base-commit>` but no decision record was added in the same range, flag an untraceable
  change. Compute with `git diff --name-only <base-commit> --` against the contract and config
  paths, and against `decisions/` or the deferred `docs/adr/` path. Contract changed and no
  record added is the drift signal.
- Existence. The config file named in the stanza exists (`test -f`), and the tool the runner
  names is wired into a project gate (`grep` over `.pre-commit-config.yaml`, `package.json`,
  `.husky`, CI workflows). Match on the tool token, not the whole runner command, so a gate that
  invokes the tool by framework hook id (pre-commit `id: ruff`) registers as well as one that
  runs the full command (husky `npx eslint .`). Skipped when `config: none` (thinking).

At bootstrap coverage is trivially satisfied because features and domains are mostly deferred.
The check earns its keep over the project's life, in CI, as folders are added and as the
contract is edited. The thinking goal runs coverage as naming-and-immutability only, since it
has no lint config, and still runs traceability and existence.

## Traceable change binding

Changing a convention or a lint zone routes through a decision record. `decisions/` for the
thinking goal, the deferred `docs/adr/` for code and infra, created at that first decision.
The rule the drift-check enforces mechanically. `CONVENTIONS.md` and its lint config move
together, and a change to either since the base without a corresponding record is drift. This
is the exact point-2 invariant, an intentional change is deliberate and traceable, an
unrecorded change is caught.

## Changes required, to plan against

Skill files.

- `SKILL.md`. Add the `CONVENTIONS.md` output to the Pass 3 description and the enforcement
  step. Adjust the principle wording so Enforcement beats prose is honoured for the tree
  conventions, not only for hard prohibitions. Add the drift-check as a named lifecycle
  capability. Version bump.
- `references/trees.md`. Point each goal's Conventions block at the `CONVENTIONS.md` output and
  the generated config, so the reference and the artifact do not drift from each other.
- `references/claude-md.md`. Reverse the exclusion. CLAUDE.md gains a one-line pointer to
  `CONVENTIONS.md` rather than restating the rules, keeping its 60-line budget. The do-not-
  synthesise-from-tree instruction stays for the FRAMING-constraint bullets, the pointer is
  separate.
- `references/environment.md`. Clarify that the freeze covers Claude's `settings.json` only,
  not the project's own lint config or gate files, which are stack files written later.

Tests.

- Add a scenario proving `CONVENTIONS.md` is emitted by Pass 3 with the right per-goal rules,
  and that the enforcement step generates config plus gate for a stack that has the tooling.
- Add the `check-conventions-drift.sh` script and wire it into the executable-checks table.
- SM-3 stays as-is and still passes, since `settings.json` is untouched. Confirm this rather
  than assume it.

## Invariants preserved

- `settings.json` byte-identical across runs. Enforcement is project-native, so no Pass mutates
  it. SM-3 stays green.
- Grounding. No config is written for absent tools or non-existent paths. The extend-per-feature
  marker replaces fabrication.
- Reconcile never regenerate. `CONVENTIONS.md`, like every other artifact, is reconciled on a
  re-run, not overwritten.
- One goal per repo. The contract instantiates a single goal's philosophy.

## Open and deferred

- Which app linter to standardise on when both ESLint zones and `eslint-plugin-boundaries` are
  viable. `trees.md` already prefers `import/no-restricted-paths`, so follow that and note the
  alternative, do not add a choice point.
- The data and infra drift-check coverage rules are lighter than app, since their boundaries
  are fewer and folder-driven less. Coverage for them checks module and env-root structure
  rather than per-feature zones. Detail this when editing, not now.
- Whether the skill should offer to backfill `CONVENTIONS.md` into an already-bootstrapped repo
  on a reconcile run. Likely yes, via the existing reconcile path, but confirm scope before
  building.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-07-16 |
| Status       | Review     |
