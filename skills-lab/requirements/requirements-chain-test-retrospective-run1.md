# Requirements chain — test run retrospective

A row-by-row retrospective in the form `test-strategy.md` §Retrospective use prescribes: each scenario marked pass or fail, with its observed `Outstanding` line and any deviation. Companion to `test-strategy.md` (the priority table this marks up) and `requirements-chain-design.md` (what each row proves).

## Evidence basis

This retrospective is reconstructed from three sources: the git diff on the three edited test files, the artifacts left under the nine `testing/test-*` directories, and `test-strategy.md`. There is no single session to read. The strategy's §Session model requires a fresh session per scenario, so the directories are the artifacts those separate sessions left behind. Behavioural criteria that leave no end-state trace, and the three in-place mutation rows, cannot be closed from disk. They need the session transcripts.

Verdict tags: `[obs]` verified on disk, `[inf]` inferred from indirect evidence, `[beh]` a behavioural criterion with no end-state trace.

## Marked priority table

| # | Scenario | Verdict | Observed evidence / Outstanding | Deviation |
|:--|:--|:--|:--|:--|
| 1 | chain-test-small | Pass `[obs]` | link-service report `Outstanding: 0 blocking, 0 warnings, 0 info`, v0.1. No `CONCEPTS.md`, single component. Matches Small branch. | none |
| 2 | chain-test-medium | Pass `[inf]` | `CONCEPTS.md` present (shared core, three contexts, context map). Pristine v0.1 base not observable, MD-1 overwrote ingestion to v0.2. Base existence inferred from the MD-1 diff. | Real base carries five FRs, not the four the MD-1 test first assumed. |
| 3 | MD-1 iteration | Pass `[obs]` | ingestion v0.2, FR-001 to FR-006, FR-006 = retention appended, FR-001 to FR-005 stable in ID and statement. `Outstanding: 0/0/0`. | Test corrected this session: off-by-one (base 4→5, appended FR-005→FR-006). |
| 4 | MD-2 framing-update | Unverified | No distinct artifact. `FRAMING.md` present but its `last_updated` history is not observable from end-state. | Needs the transcript. |
| 5 | MD-5 reconcile | Unverified | No distinct artifact. Reconcile-not-regenerate is not confirmable from the end-state. | Needs the transcript. |
| 6 | SM-3 resume | Pass `[obs]` tree/goal, `[beh]` resume-detect | Infra tree (`modules/`, `envs/prod/`), infra `CLAUDE.md`, `settings.json` present, goal infra. "Reports Pass 1 done, re-elicits goal, does not guess from dir name" is behavioural. | Test edited this session: added the re-elicitation AC (no stamp → ask, do not infer). |
| 7 | MD-4 warnings-loop | Unverified | No distinct artifact beyond ingestion. | Needs the transcript. |
| 8 | MD-3 concepts-reuse | Pass `[obs]`, partial | Brainstorm slice reuses `owner`, `cross-team report`, `catalog` verbatim, all in `CONCEPTS.md`. `Outstanding` N/A (no report written). | Proven at brainstorm/CONCEPTS layer only. No `writing-requirements` pass. |
| 9 | MD-7 divergence | Pass `[obs]`, partial | `CONCEPTS.md` records `owner` twice (steward in Governance, analyst in Exposition) plus a context-map divergence row. Both slices present. | Same as MD-3: CONCEPTS layer only, not formalised. |
| 10 | SM-1 upgrade | Pass `[obs]` | `test-upgrade`: `CONCEPTS.md` present, filing requirements v0.2, `Outstanding: 0/0/0`. | v0.2 indicates the upgrade iterated an existing artifact. |
| 11 | MD-6 technical | Pass `[obs]` | ticket-api full technical skeleton: CON-001, ERR-001/002 traced to FR-001/002, NFR-001 (N/A + warning), NFR-002 (p95 < 300 ms), SEC-001 → ERR-002, OBS-001, Bounded criterion. `Outstanding: 0/0/0`. code/app tree. | none |
| 12 | XC-1 guards | Pass `[obs]` | Only the fixtures `spec.md` and `spec.txt` on disk, no `requirements/` written. Hard-fail wrote nothing, exactly the AC. | none |
| 13 | XC-3 degraded | Pass `[obs]` | bare-spec: seven `WARNING-UNRESOLVED` across sections, `N/A` scope and actors, SHALL line captured as FR-001, no fabrication, both files written, no hard-fail. `Outstanding: 0 blocking, 7 warnings, 0 info`. | Test edited this session: repo-root walk escaped up to `skills-lab`, a scaffold `CLAUDE.md` was added to contain output. |
| 14 | XC-2 goal-lock | Pass `[obs]` scaffold, `[beh]` stop-report | Thinking tree (`decisions/`, `diagrams/`, `notes/`, `references/`), `FRAMING.md` and `CLAUDE.md` present. "Conflicting goal stops, reports, no mutation" is behavioural. | Needs the transcript to confirm no-mutation. |
| 15 | OP-1 standalone | Pass `[obs]` | `FRAMING.md` plus capture-command brainstorm output only. No `.claude/`, no `.git/`, no `CONCEPTS.md`. Matches out-of-project. | none |

Tally: seven full `[obs]` passes (1, 3, 10, 11, 12, 13, 15), four partial passes with a `[beh]` or unformalised gap (6, 8, 9, 14), one inferred base (2), three unverified (4, 5, 7).

## The three findings that mattered

All three edits this run are the suite catching up to observed reality. That is the real output of the run.

1. Repo-root walk escapes the sandbox (XC-3). `writing-requirements` Phase 0.5 walks upward for a `CLAUDE.md` to fix the repo root. With none in the test dir it resolved the root to `skills-lab` and wrote outputs to `skills-lab/requirements/bare-spec/`, outside the intended directory. The fix was a scaffold `CLAUDE.md` in the test dir, which contains the symptom rather than closing the escape.
2. Goal does not persist across sessions (SM-3). On resume with no stamp and no goal argument, the skill must re-elicit the goal and must not infer it from the directory name. A new acceptance criterion and matching fail condition were added.
3. Off-by-one in the medium base (MD-1). The test assumed `chain-test-medium` produces FR-001 to FR-004. The real run produces five, the extra being FR-005, the IF/THEN quality-rule withholding requirement. Every count in the test shifted by one.

## Reading (inference, not observed)

Kept separate so it carries no factual weight it has not earned.

- The theme worth putting first is implicit context resolution versus explicit inputs (rows 6, 13, and the git-init open item). This is synthesis across three findings, not a stated criterion in any test.
- The git-init open item is not "decided". The nested `.git/` in every bootstrapped dir shows what the skill did, and it matches the standing memory note, but the strategy says settle it in the skill, and no such ratification is on disk.
- MD-7 reads as the strongest positive result because divergence is the hardest mechanism in the chain. That is a judgement of relative difficulty, not a measured fact.

## Open follow-ups

- Settle the context-resolution boundary in the skills (repo-root walk, goal inference, git-init), then re-run XC-3 and SM-3 to confirm the fixes hold without scaffolding.
- Recover the transcripts for MD-2, MD-4, MD-5 and the `[beh]` criteria in SM-3 and XC-2, or re-run those rows, to close the unverified cells.
- Decide whether MD-3 and MD-7 should formalise their slices through `writing-requirements`, and if so extend those two tests to assert the requirements output.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-14 |
| Status       | Draft      |
