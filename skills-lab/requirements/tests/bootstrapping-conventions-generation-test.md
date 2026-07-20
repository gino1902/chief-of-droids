# Contract generation test — BC-1

_These are illustrative fixtures. The subject, scripted answers, and file names below are examples to make the run concrete, not fixed requirements. The acceptance criteria carry the test._

Bootstrapping-only. One run per goal. No downstream chain.

## Purpose

Exercise Pass 3 and the Pass 4 enforcement tail of `bootstrapping-project`: the skill writes `CONVENTIONS.md` at the repo root, filled verbatim from the locked goal's Conventions block in `trees.md` with no re-synthesis and no leaked `⚠️ Unverified` authoring caveat, and generates stack-native enforcement rather than a `settings.json` hook. This is the contract-generation half of the CONVENTIONS feature. The checks are one-run invariants, cross-run byte-identity is the predictability audit, not this scenario.

## Directory and precedence

Directory: `testing/bc1-<goal>`, one per goal exercised. Precedence: none, a self-contained bootstrapping run.

## Preconditions

- A fresh session or subagent, no chain context loaded.
- An empty `testing/bc1-<goal>`. Session cwd is that directory.
- The Pass 1 baseline committed in the run dir, so `settings.json` invariance reads as a diff.

## Run steps

1. Invoke `bootstrapping-project`. Goal `<goal>` (code/app, code/data, infra, or thinking), size per the goal, framing answered from a borrowed scenario's script. Run through Pass 4's enforcement tail, then stop at bootstrapping's close. Do not run the downstream chain.

## Expected outputs (under `testing/bc1-<goal>`)

- `CONVENTIONS.md` at the repo root. Its rules block equals the `trees.md` `<goal>` Conventions block verbatim, minus any `> ⚠️ Unverified` authoring blockquote.
- The stanza (`config` / `runner` / `zoned`) is present and consistent with the generated enforcement, and `zoned` names only folders that exist.
- Stack-native enforcement (eslint plus husky for app, pre-commit plus ruff for data, pre-commit plus TFLint for infra, none for thinking). No `hooks` key in `settings.json`.
- `settings.json` byte-identical to the Pass 1 baseline.
- `CLAUDE.md` carries the two pointer lines and does not restate the structural rules.

## Acceptance criteria

- `CONVENTIONS.md` exists at the root, its rules block matches the `trees.md` `<goal>` block verbatim, and no line contains "Unverified".
- The `config` / `runner` / `zoned` stanza is present and consistent with the generated enforcement, the stanza naming the config and runner the gate actually uses, and every `zoned` glob resolves to a folder that exists. The canonical `runner` value is BC-3's assertion, not this one.
- The `settings.json` diff against the Pass 1 baseline is empty, and no enforcement landed as a `settings.json` hook.
- `CLAUDE.md` holds both pointer lines and restates no rule.

Check: `checks/check-conventions-contract.sh <dir> <goal>` (new, greps the stanza, asserts no "Unverified" line, compares the rules block against the `trees.md` source). `settings.json` invariance is checked narrowly, `git diff <pass1> -- .claude/settings.json` must be empty. A fresh bootstrap rewrites the whole tree, so a whole-tree diff-confinement does not apply here. Both one-run, disk-only.

## Fail conditions

- `CONVENTIONS.md` absent, its rules re-synthesised or reworded, or it carries an "Unverified" line.
- The stanza disagrees with the generated enforcement, or a `zoned` glob names an absent folder.
- `settings.json` changed, or enforcement was written as a `settings.json` hook.
- `CLAUDE.md` restates the rules or misses a pointer.

## Record

The stanza per goal, the `CONVENTIONS.md`-to-`trees.md` verbatim match, and the empty `settings.json` diff.

## Note

One run per goal, scoped by the gate to the goals being deployed. Cross-run byte-identity is out of scope here, it belongs to the predictability audit.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-20 |
| Status       | Draft      |
