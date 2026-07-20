# Drift-check delivery test: BC-2

_These are illustrative fixtures. The subject, scripted answers, and file names below are examples to make the run concrete, not fixed requirements. The acceptance criteria carry the test._

Bootstrapping-only. One bootstrap run plus a scripted three-state check.

## Purpose

Confirm `bootstrapping-project` delivers the traceability guard into the project and wires it: `scripts/check-conventions-drift.sh` ships, is executable, byte-identical to the skill asset, and is wired into the gate. The behavioural half exercises the guard on the delivered script: a base passes, an unrecorded `CONVENTIONS.md` edit fails, and adding an ADR under `docs/adr/` makes the same state pass.

## Directory and precedence

Directory: `testing/bc2`. Precedence: none, self-contained. Best run after BC-1 is green, so a failure localises to delivery rather than generation.

## Preconditions

- A fresh session or subagent.
- Empty `testing/bc2`. Session cwd is that directory.

## Run steps

1. Bootstrap a Small code/app-backend project through Pass 4. Commit the result as the base.
2. Run the delivered `scripts/check-conventions-drift.sh .` against the base.
3. Edit `CONVENTIONS.md` (change a rule) without adding a decision record. Re-run the delivered check.
4. Add an ADR under `docs/adr/`. Re-run the delivered check. Restore the base.

## Expected outputs (under `testing/bc2`)

- `scripts/check-conventions-drift.sh` present, executable, byte-identical to the skill asset.
- The pinned gate carries the wiring line `bash scripts/check-conventions-drift.sh .`.
- Step 2 passes, step 3 fails (untraceable change), step 4 passes.

## Acceptance criteria

- The delivered script exists, is executable, and diffs empty against the skill asset.
- The gate references the script for the base pass.
- Exit codes: base pass 0, unrecorded edit non-zero, post-ADR 0.

Check: diff the delivered script against the skill asset, expect empty. Run the delivered `check-conventions-drift.sh` in the three states and assert the exit codes. One bootstrap run, disk-only checks.

## Fail conditions

- The script is missing, not executable, or diverges from the skill asset.
- The gate does not reference it.
- The unrecorded edit passes (guard blind), or the ADR does not clear it (guard stuck).

## Record

The three exit codes, and the delivered-versus-asset diff being empty.

## Note

Runs the project's own delivered guard, not the QA copy, which is what proves the guard ships rather than living only in QA. Cross-gate-style coverage of the drift-check's runner-token matching is BC-1's job, through its per-goal base pass, so BC-2 stays on one gate style and owns the style-agnostic three-state traceability logic.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-20 |
| Status       | Draft      |
