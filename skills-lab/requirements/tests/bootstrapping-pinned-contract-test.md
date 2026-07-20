# Pinned-contract invariants test: BC-3

_These are illustrative fixtures. The subject, scripted answers, and file names below are examples to make the run concrete, not fixed requirements. The acceptance criteria carry the test._

Bootstrapping-only. One run per stack. Invariant checks against the pins, no repeated-run comparison.

## Purpose

Confirm the determinism pins hold as one-run invariants: the generated enforcement and the `CONVENTIONS.md` contract match the pinned templates and canonical values, so the delivered contract is stable without a cross-run diff. Cross-run byte-identity across repeated bootstraps is the separate predictability audit, not this scenario and not the gate.

## Directory and precedence

Directory: `testing/bc3-<stack>` (app, data, infra). Precedence: none, self-contained. After BC-1 is green.

## Preconditions

- A fresh session or subagent.
- Empty `testing/bc3-<stack>`. Session cwd is that directory.
- Online, so the `rev` lookup can resolve. Offline falls back to the `# TODO` marker, which is an allowed value.

## Run steps

1. Bootstrap a project of the stack through Pass 4.

## Expected outputs (under `testing/bc3-<stack>`)

- App: `.husky/pre-commit` byte-identical to the committed pinned template.
- The `CONVENTIONS.md` `runner` equals the canonical pinned value for the stack (`npx eslint .` app, `uv run ruff check .` data, `tflint` infra).
- Data: the pre-commit local drift-check hook block equals its byte-for-byte template.
- The pre-commit `rev` (data, infra) is a real resolvable upstream tag, or the offline `# TODO` marker, never a guessed value.

## Acceptance criteria

- The generated app husky hook equals the pinned template (byte-equality to a fixed committed expected artifact, a one-run invariant).
- The `runner` stanza equals the stack's canonical pinned value.
- The data local drift-check hook block equals its template.
- The `rev` resolves against `git ls-remote` for the tool repo, or is the `# TODO` marker.

Check: `checks/check-pinned-contract.sh <dir> <stack>` (new, compares the husky hook to the template, greps the runner value, matches the local hook block, resolves the rev). All one-run, no second bootstrap.

## Fail conditions

- The husky hook differs from the pinned template.
- The `runner` is not the canonical value.
- The data local hook block differs from its template.
- The `rev` is a guessed or non-resolvable tag.

## Record

The husky-to-template match, the runner value, and the resolved rev per stack.

## Note

This is the gate side of determinism, one-run invariants against the pins. The "two bootstraps of an identical brief agree" comparison lives in the predictability audit, run at a release boundary, not on every redeploy.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-20 |
| Status       | Draft      |
