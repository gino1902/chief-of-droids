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

## Gate non-determinism — grounded, pinned, one post-pin run confirms

The skill did not pin which project gate it generated. Across the runs the same code/app-backend
brief produced a husky `.husky/pre-commit` (V-small) and a `.github/workflows/lint.yml`
(the V-small confirmation re-run); data and infra chose `.pre-commit-config.yaml`. All passed the
drift-check, which greps every gate style, so correctness held, but two runs of one brief
disagreeing on the gate mechanism contradicted the suite's determinism ethos.

Fixed (2026-07-18). A grounding pass established the default gate per stack from each goal's
reference standard (husky for Node/TS app per bulletproof-react, pre-commit with
`astral-sh/ruff-pre-commit` for data, pre-commit fmt/validate/tflint plus TFLint CI for infra),
recorded with sources in the design doc. The Pass 4 tail now pins these, keeping a
reconcile-to-existing-gate escape hatch.

Double-run (2026-07-18). Two post-pin bootstraps of the identical app-backend brief
(`outputs/test-det-a`, `outputs/test-det-b`). Result is partial. The gate mechanism is now
deterministic: both chose husky, neither CI nor pre-commit, and both wire the drift-check
base pass. But two finer variances remain. The lint runner differed, `npx eslint apps` versus
`npx eslint .`, and that difference propagates into the `CONVENTIONS.md` `runner:` stanza, so the
delivered contract is not byte-consistent run to run. The husky hook body also differed, one bare
without a shebang, one with a shebang and the older `. husky.sh` sourcing line. The mechanism
wobble is fixed; the runner value and hook body are still model-chosen.

Finer pin applied and confirmed (2026-07-18, claude-md v1.9 / trees v2.5). The app husky hook is
now a byte-for-byte template (shebang, `npx eslint .`, the drift-check line, nothing else) and the
runner is pinned to canonical `npx eslint .` in both the gate and the `CONVENTIONS.md` stanza — the
flat config's `files` glob already scopes it, so `eslint apps` was a distinction without a
difference. A confirming double-run (`outputs/test-det-c`, `outputs/test-det-d`) produced a
byte-identical `.husky/pre-commit` (same SHA `ebc2885…`) and identical `runner:` stanzas, both
husky-only, both passing the drift-check. App-goal gate determinism is closed. Scope note: the
data and infra pre-commit gates are grounded and pinned by hook id (`ruff-check`/`ruff-format`,
terraform fmt/validate/tflint) but were not put through a byte-identical double-run; the app goal,
the one that wobbled, is the one confirmed.

## Delivery validation — drift-check ships with the project (2026-07-18)

Follow-on to close the highest-value lifecycle gap: the traceability guard previously lived only
in this QA suite, so a bootstrapped project could not catch an untraceable contract change on its
own. The skill now delivers the check into the project and wires it. Validated on a fresh Small
code/app-backend bootstrap (`outputs/test-deliver`, driven by a fresh subagent):

- `scripts/check-conventions-drift.sh` is delivered, executable, and byte-identical to the skill
  asset (one canonical source, QA reaches it by symlink).
- The pinned gate is husky (`.husky/pre-commit`), no CI-workflow wobble, and it carries the wiring
  line `bash scripts/check-conventions-drift.sh .` for the base pass.
- The traceability pass was documented as a CI step, not fabricated as a workflow, because no CI
  platform was confirmed in the blank repo. Grounding held.

Traceability proven with the project's own delivered script, against a committed base: the base
pass passed; an unrecorded edit to `CONVENTIONS.md` failed the check (untraceable change); adding
an ADR under `docs/adr/` made it pass. Point 2 is now enforceable inside the delivered project,
not only in QA.

## Conclusion

The feature works end to end on real skill output across all four goals and the reconcile path,
and the traceability guard now ships in the delivered project. Three issues the runs surfaced are
fixed: the runner-wired matching in the drift-check, the authoring-caveat leak in the generated
contract, gate-mechanism non-determinism (grounded and pinned per stack), and app-goal contract
determinism (fixed husky template + pinned runner, confirmed byte-identical across a double-run).
Remaining: a byte-identical double-run for the data and infra gates (grounded-pinned but not yet
proven), and by choice the headless release-gate re-run.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.6        |
| Last Updated | 2026-07-18 |
| Status       | Final      |
