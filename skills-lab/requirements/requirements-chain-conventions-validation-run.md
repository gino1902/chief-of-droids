# CONVENTIONS.md feature — validation run

Retrospective for the live validation of the `CONVENTIONS.md` + enforcement + drift-check
feature (bootstrapping-project v1.12). Plan and pass criteria are in
`tests/test-strategy.md` §Conventions feature — validation run. This doc records what was run
and what was found.

## Objective

Close the gap the feature shipped with: the drift-check was proven only against synthetic
fixtures, and "the skill emits this stanza and generates this config" was instruction-level, not
observed. This run observes it against real skill output.

## Mechanism as run

Six bootstrapping-only runs, one per distinct drift-check behaviour. Each was produced by a fresh
`general-purpose` subagent driving `bootstrapping-project` with the borrowed scenario's scripted
inputs — no inherited context from the design work, so it could not reverse-engineer the expected
output. QA ran `check-conventions-drift.sh` and captured evidence. Runs stopped at bootstrapping's
close (the feature lives in Pass 3 + the Pass 4 tail); the downstream chain was not exercised.

Known fidelity deviation: subagents share this harness and repo, not a separate Claude Code
process. A headless `claude -p` or manual re-run is the release-gate tier, deferred until the
Phase 2 driver exists. Date: 2026-07-17.

## Results

All six PASS.

| Run | Goal | Subject | Stanza (`config` / `runner` / `zoned`) | Drift-check |
|:--|:--|:--|:--|:--|
| V-small | code/app backend | linkjar | `eslint.config.js` / `npx eslint .` / `apps/*` | PASS — existence + coverage (`apps/links`) |
| V-data | code/data | insight-hub | `pyproject.toml` / `ruff check .` / `none` | PASS — existence (after the fix below) |
| V-infra | infra | edge-dns | `.tflint.hcl` / `tflint` / `none` | PASS — existence |
| V-app | code/app | helpdesk | `eslint.config.js` / `npx eslint .` / `apps/*` | PASS — coverage, all 3 domains zoned |
| V-think | thinking | arch-notes | `none` / `review` / `none` | PASS — existence and coverage skipped |
| V-recon | code/data reconcile | insight-hub base | unchanged | PASS — reconcile no-op, traceability clean |

Cross-run invariants confirmed on every run:

- `settings.json` byte-identical to the Pass 1 baseline, no `hooks` key. Enforcement landed as
  stack files (husky, `.pre-commit-config.yaml`, `pyproject.toml [tool.ruff]`, `.tflint.hcl`),
  never as a `settings.json` hook. The freeze held.
- `CLAUDE.md` carried both appended pointer lines and did not restate the structural rules; the
  rules lived in `CONVENTIONS.md`.
- The per-goal stanza matched the strategy exactly, including the side-conditional `zoned`
  (`apps/*` for the two backends, never a `src/features/*` glob for an absent frontend).
- V-app generated one `import/no-restricted-paths` zone per scaffolded `apps/<domain>/`
  (`ticketing`, `identity-and-access`, `platform-and-observability`) plus the layer zones, with a
  documented extend-per-folder marker for the still-deferred `libraries/`. Grounding held: no
  zones for absent folders.

## Defect found and fixed

V-data failed the drift-check on the first pass. The runner-wired check grepped for the whole
runner string (`ruff check .`), but a pre-commit gate references the tool by hook id (`id: ruff`),
never by the full command. V-small (husky runs the literal `npx eslint .`) and V-infra (hook id
`terraform_tflint` contains `tflint`) had passed only by substring luck.

Fix: `check-conventions-drift.sh` now matches on the tool token — the first runner word that is
not a launcher (`npx`, `uv`, `run`, …), a flag, or a bare path — instead of the whole command.
Re-verified across all four gate styles (husky command, pre-commit ruff, pre-commit tflint,
thinking/none): all green, no regression. This is the finding the live run existed to catch; a
fixture-only test would have kept the substring coincidence hidden.

## Traceability proven both ways

On real V-data output, against the committed base: a contract edit with no decision record failed
the check (untraceable change), and adding an ADR under `docs/adr/` made the same state pass. The
base was then restored pristine. Both branches of the point-2 invariant hold on real output, not
just fixtures.

## Quality finding — found and fixed

The verbatim-copy rule pulled trees.md's internal "⚠️ Unverified" authoring caveat straight into
the deliverable `CONVENTIONS.md` (seen in V-small and V-data). An authoring note aimed at the
model was sitting in a user-facing contract.

Fixed in trees.md v2.3: the Pass 3 fill rule now drops the `> ⚠️ Unverified …` blockquotes on
copy, and the reconcile path strips one a prior run left behind. Confirmed by a fresh V-small
re-run (into `outputs/test-small-fix`): the generated `CONVENTIONS.md` carries no "Unverified"
line and still passes the drift-check — that run also wired a CI-workflow gate
(`.github/workflows/lint.yml`), a third gate style, exercising the runner-wired fix once more.

## Conclusion

The feature works end to end on real skill output across all four goals and the reconcile path.
Both issues the run surfaced are fixed and re-verified: the runner-wired matching in the
drift-check, and the authoring-caveat leak in the generated contract. Remaining by choice: the
headless release-gate re-run.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-07-17 |
| Status       | Final      |
