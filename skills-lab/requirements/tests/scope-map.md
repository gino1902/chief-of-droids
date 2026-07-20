# Gate scope map: requirements-chain test suite

The QA Lead artifact that decides which tests fire for a given deploy. It turns the FRAMING's "efficient" goal into a concrete selection, run the slice a rework can break, not the whole matrix every time. Companion to `FRAMING.md`, which says why the suite exists, and `test-strategy.md`, which holds the scenarios themselves.

## The deploy event

The gate fires on a deploy event, defined by two inputs:

- Which chain skills changed. `bootstrapping-project`, `framing-project`, `brainstorming-requirements`, `writing-requirements`, or the `requirements-chain` package, which is the last three together. `bootstrapping-project` deploys on its own.
- Which target contexts they ship into. New project or existing, and the goal and size that matter for those skills, meaning code, data, app, infra, or thinking, and Small or Medium+.

Each reworked skill has three failure surfaces, from the FRAMING: its own behaviour, its seams to neighbours, and its behaviour in the deployed context. The map assigns scenarios to those surfaces.

## Per-skill test map

Chain order is bootstrapping, then framing, then brainstorming, then writing.

| Skill | Own-behaviour | Seams | Context axis |
|:--|:--|:--|:--|
| bootstrapping-project | MD-5 reconcile, SM-3 resume, XC-2 goal-lock, and the CONVENTIONS feature-depth as BC-1 contract generation, BC-2 drift-check, BC-3 pinned-contract, BC-4 backfill | downstream to framing: chain-test-small, chain-test-medium, SM-1 | new vs existing repo, every goal type, Small vs Medium+ |
| framing-project | MD-2 update, SM-1 convert | up from bootstrapping and down to brainstorming: chain-test-medium, MD-3, MD-7 | create vs update, Medium+ only |
| brainstorming-requirements | MD-3 reuse, MD-7 divergence, OP-1 standalone, MD-4 weak slice | CONCEPTS up from framing and slice down to writing: chain-test-medium, MD-4 | with CONCEPTS vs without, in-project vs standalone |
| writing-requirements | MD-1 iteration, MD-6 technical, XC-1 guards, XC-3 degraded | slice up from brainstorming: chain-test-small, chain-test-medium, MD-4 | generic vs technical, well-shaped vs degraded slice, first pass vs iteration, target repo-root resolution |

The full-chain scenarios, chain-test-small and chain-test-medium, belong to every row, because the deployed-context integration surface shows there.

## The gate

0. Reconcile the matrix against the current suite before selecting. Check coverage, that every scenario maps to a skill and a surface. Check validity, that every named scenario still exists and its surface still holds. Check chain shape, that the seams match the current chain order and each skill's input and output contract. Check gaps, any behaviour with a run record but no named scenario and check. A stale map under-covers silently, which is the escaped-defect risk the suite exists to prevent, so a gate run that finds the map stale stops and updates it before selecting.
1. For each reworked skill, take its own-behaviour scenarios.
2. Add its downstream seam scenarios always. Add the upstream seam only if the rework changed what the skill reads.
3. Add at least one full-chain scenario per target context.
4. Scope every selection to the contexts being deployed. Do not run infra or thinking scenarios for a code-only deploy.
5. Run bottom-up, own-behaviour, then seams, then full-chain, so a failure localises to one mechanism.

## Efficiency

- Rework `writing-requirements`, ship into one code Medium project. The gate is MD-1, MD-6, XC-1, XC-3, plus chain-test-medium. Five scenarios, not fifteen.
- Rework `bootstrapping-project`'s CONVENTIONS feature, ship into code, data, and infra. The gate is MD-5, SM-3, XC-2, both full-chain rows, plus BC-1 and BC-3 for those three stacks, BC-2 once, and BC-4 for the existing-repo case. Thinking is skipped.

## Bootstrapping depth: formalised

`bootstrapping-project`'s CONVENTIONS feature-depth is now named scenarios with checks: BC-1 contract generation (`check-conventions-contract.sh`), BC-2 drift-check delivery and traceability (`check-conventions-drift.sh`), BC-3 pinned-contract invariants (`check-pinned-contract.sh`), BC-4 backfill on reconcile (`check-diff-confined.sh`). The gap step 0 flagged is closed, the depth is selectable and assertable.

Parked, out of the gate by design: the cross-run determinism check, meaning two bootstraps of an identical brief producing byte-identical output. The FRAMING keeps variance in a separate predictability audit, run at a release boundary, not on every redeploy. BC-3 covers the gate-side one-run invariants against the pins; the two-runs-agree comparison is the audit's job.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-07-20 |
| Status       | Draft      |
