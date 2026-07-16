# Requirements chain — test strategy

A hat over the scenarios in this directory. It holds the execution priority, the rationale for each, and the dependency between them, so a retrospective can read one table instead of opening fifteen files. Companion to `requirements-chain-design.md`, which is the source for what each scenario is proving.

## Session model

Every scenario runs from a fresh Claude Code session. Nothing carries between scenarios in memory. The only thing that passes from one scenario to another is on-disk artifacts under `outputs/`, and the preconditions of each scenario state exactly what it expects to find there.

Two consequences shape the dependency column below:

- A shared-base scenario does not inherit another session's live state. It re-establishes its base on disk in its own session. For the Medium scenarios that means: empty `outputs/test-medium`, run `chain-test-medium` into it, then run the scenario. The base is consumed from disk, not from a warm session.
- A "passed" dependency is a diagnostic gate, not a state hand-off. When a row says "after MD-1 passed", it means run MD-1 and confirm it is green before running this one, so a failure localises. The dependent scenario still builds its own base from disk.

Directories under `outputs/` are created empty and left bare. Each scenario's setup (bootstrapping, or its own fixtures) populates its directory. No directory is pre-initialised.

## Ordering principle

Diagnosability, bottom-up. Prove each skill survives its own second run before the cross-skill loops, then the integration capstone, then pure coverage, then the negative and robustness sweeps. A failure at any tier points at one mechanism because the tiers beneath it are already green.

## Priority table

| # | Scenario (file) | Project type | Output dir | Depends on | Rationale — what it proves | Capture at run time |
|:--|:--|:--|:--|:--|:--|:--|
| 1 | chain-test-small (`chain-test-small.md`) | Small, code/data | `test-small` | none | Base. Small branch: no `CONCEPTS.md`, no Tracks, single component. | Report `Outstanding` line and version. Confirm no `CONCEPTS.md` and a single component. |
| 2 | chain-test-medium (`chain-test-medium.md`) | Medium, code/data | `test-medium` | none | Base. Medium branch: `CONCEPTS.md` + Tracks, clean extract. On-disk base for every MD-* row. | The base FR list and version, plus `CONCEPTS.md` contexts. Commit this base before any MD-* row so their effects read as diffs. |
| 3 | MD-1 (`iteration-rewrite-test.md`) | Medium, code/data | `test-medium` | fresh chain-test-medium base | Gates iteration. Re-pass: ID stability, new-ID assignment, version bump. If this fails the iterative premise is dead. | The ID-to-content map and the version chain (0.1→0.2). Confirm prior IDs byte-stable and only the next ID added. |
| 4 | MD-2 (`framing-update-test.md`) | Medium, code/data | `test-medium` | fresh chain-test-medium base | Upstream-change: framing-project update preserves unrevisited sections, bumps `last_updated`, leaves `CONCEPTS.md` alone when no boundary moves. | `FRAMING.md` `last_updated` before and after, and a `CONCEPTS.md` diff showing it was untouched. |
| 5 | MD-5 (`bootstrapping-reconcile-test.md`) | Medium, code/data | `test-medium` | fresh chain-test-medium base | Reconcile: re-run bootstrapping on an existing repo routes framing to the update branch, documents the tree, reconciles CLAUDE.md, never regenerates. | The Preamble per-pass status line, and a `CLAUDE.md` diff proving reconcile, not regenerate. |
| 6 | SM-3 (`bootstrapping-resume-test.md`) | Small, infra | `test-resume` | none (two sessions) | Resume: Pass 1 only, then a fresh session resumes at Pass 2. Also the only infra tree/skeleton coverage. Blocked partly on the git-init decision (see Open items). | `[beh]` the prompt where the skill asks for the goal (proves no inference from dir name), plus a `settings.json` diff showing it unchanged. |
| 7 | MD-4 (`warnings-refinement-loop-test.md`) | Medium, code/data | `test-medium` | fresh chain-test-medium base; after MD-1 passed | Downstream-to-upstream loop: a no-derivable-AC warning drives an elicitation refinement, the re-write clears it. | The warning on the first write and its absence on the re-write. Keep both report versions. |
| 8 | MD-3 (`concepts-reuse-test.md`) | Medium, code/data | `test-medium` | fresh chain-test-medium base | Domain-language loop: a second component reuses terms verbatim (no drift) and records a new term back to `CONCEPTS.md`. | Verbatim term reuse in the slice, and the new term appended to `CONCEPTS.md`. |
| 9 | MD-7 (`concepts-divergence-test.md`) | Medium, code/data | `test-medium` | fresh chain-test-medium base | The untested half of the domain language: one word, two meanings across two contexts, recorded under both with a context-map divergence row. Extends MD-3. | Both senses of the divergent term under their contexts, and the context-map divergence row. |
| 10 | SM-1 (`small-to-medium-upgrade-test.md`) | Small→Medium, code/data | `test-upgrade` | self-contained; after MD-1, MD-3, MD-4 passed | Capstone: the Small-to-Medium upgrade path clears vocabulary noise. Only diagnostic once its constituent mechanisms are green. | `CONCEPTS.md` created on upgrade, the vocabulary cleared, and the version bump. |
| 11 | MD-6 (`technical-formalisation-test.md`) | Medium, code/app | `test-app` | self-contained | Coverage: the full `--type technical` skeleton (CON, ERR pairs, NFR/SEC/OBS, Bounded). Off the iteration theme, so below the ladder. Only code/app tree coverage. | Every technical section present (CON, ERR pairs traced to FRs, NFR/SEC/OBS, Bounded criterion) and the report `Outstanding` line. |
| 12 | XC-1 (`writing-requirements-guards-test.md`) | none (fixtures) | `test-wr-guards` | none | Robustness: Phase 0 hard-fail guards fire and write nothing. | Directory holds only the fixtures. No `requirements/` written. |
| 13 | XC-3 (`degraded-substrate-test.md`) | none (fixtures) | `test-wr-degraded` | none | Robustness: thin substrate degrades to N/A + Warning, slug-verbatim title fallback, no fabrication, no hard-fail. Complement to XC-1. | The warning count and `N/A` sections, SHALL line as FR-001, and that outputs land in-dir, not at the `skills-lab` root (repo-root walk not settled). |
| 14 | XC-2 (`bootstrapping-goal-lock-test.md`) | Small, thinking | `test-goal-lock` | none | Robustness: a conflicting goal argument against a stamped FRAMING stops and reports, no mutation. Only thinking tree/skeleton coverage. | `[beh]` the stop-and-report message on the conflicting goal, plus a `FRAMING.md` diff showing zero mutation. |
| 15 | OP-1 (`standalone-brainstorm-test.md`) | out of project | `test-standalone-brainstorm` | none | Independent: standalone terminal brainstorm from a bare FRAMING, no project, no `CONCEPTS.md`. Runnable at any point. | Brainstorm output only. No `.claude/`, `.git/`, or `CONCEPTS.md`. |

Project-type coverage across the suite: code/data (rows 1-10), code/app (11), infra (6), thinking (14), plus the out-of-project case (15).

## Deferred — not scheduled

These are in the design doc's Deferred section because the feature is unbuilt. No scenario is scheduled until it exists.

- Multi-component fan-out (Phase 3.5).
- The system-level cross-cutting slice, and the recomposition and consistency checks (the context map as a runtime check). MD-7's divergence rows are the groundwork these will run against.
- Visual and blindspot gates (intent only, undefined in writing).
- Routing architectural boundary decisions to making-architecture-decision.
- Not scheduled by choice: the grounding-depth delta (Small surfaces more open questions than Medium). A soft comparative metric, parked unless wanted.

## Open items to resolve before a clean run

- The git-init-inside-a-repo behaviour. Bootstrapping's Pass 1 detection keys on `.git/` plus `.claude/settings.json`, but the running convention skips `git init` inside an existing repo. This affects SM-3's resume detection and any bootstrapping-based row run under `skills-lab`. Settle it in the skill, not in the tests.

## Retrospective use

After a run-through, mark each row pass or fail and attach the observed `Outstanding` line and any deviation. Read failures against the tier: a failure in a lower tier invalidates the rows above it, so fix bottom-up. Auto-derived glossary entries surface as verification-pending (`WARNING-UNRESOLVED`) after the `conventions.md` resolution-model fix; treat those as normal, not failures. For every row that runs `writing-requirements`, also confirm the report Summary reconciles with the body tagged-line counts: the Info Resolved cell equals the `[INFO]` line count, and each Warning and Blocking cell equals its suffix-line count. A mismatch is a defect, not normal variance. The standalone check is `verify-summary-info-tally.md`.

Record the Capture column as the run proceeds, not after. A clean end-state leaves no trace for behavioural rows or in-place mutation rows, so evidence not captured live cannot be recovered. Rows tagged `[beh]` in that column have no end-state artifact at all and depend entirely on the live transcript. To make in-place effects auditable, commit each shared base in `test-medium`'s own repo when `chain-test-medium` builds it; that commit is the diff reference. Each in-place row runs in a fresh session, resets `test-medium` to the base commit (`git reset --hard <base-commit> && git clean -fd`) rather than rebuilding, runs its scenario, and captures `git diff <base-commit>` as a named evidence artifact, so every change reads as a diff against a fixed, deterministic base rather than a lost delta. Resetting to a committed base also removes the base-elicitation variance that caused MD-1's off-by-one. This assumes the base carries its own repo, which the git-init open item below governs. The five diff-based rows (MD-1, MD-2, MD-3, MD-5, MD-7) carry this in their Reset-to-base and Record sections. The first run-through's marked table is in `../requirements-chain-test-retrospective-run1.md`; the second, against the tightened suite, is in `../requirements-chain-test-retrospective-run2.md`.

## Executable checks

The disk-checkable invariants have scripts under `tests/checks/`, run against a scenario's outputs after the run. They are deterministic, need no skill run, and stay inside the `grep`/`sed`/`git` set. `<dir>` is the scenario's output dir, `<base>` the committed base commit (see `chain-test-medium.md` §Record). Rows with no script, and the `[beh]` halves, stay manual until the Phase 2 driver and R2's decision stamp exist.

| # Row | Check | Invocation, or why manual |
|:--|:--|:--|
| 1 small | tally | `check-summary-tally.sh <dir>/requirements/link-service/link-service-report.md` |
| 2 medium | tally | `check-summary-tally.sh <dir>/requirements/ingestion-pipeline/ingestion-pipeline-report.md` |
| 3 MD-1 | tally, plus ID-stability | tally on the report; ID-stability (base FRs byte-stable, one new next-ID) not yet scripted, check by hand |
| 4 MD-2 | diff-confined | `check-diff-confined.sh <dir> <base> FRAMING.md` |
| 5 MD-5 | diff-confined | `check-diff-confined.sh <dir> <base> CLAUDE.md` |
| 6 SM-3 | diff-confined, plus `[beh]` | no-mutation of `settings.json` is diff-checkable against the pass-1 commit; re-elicitation is `[beh]`, manual |
| 7 MD-4 | tally | `check-summary-tally.sh` on each pass's report |
| 8 MD-3 | diff-confined | `check-diff-confined.sh --no-deletions <dir> <base> CONCEPTS.md 'report-builder/*'` |
| 9 MD-7 | diff-confined | `check-diff-confined.sh --no-deletions <dir> <base> CONCEPTS.md 'steward-assignment/*' 'report-ownership/*'` |
| 10 SM-1 | tally | `check-summary-tally.sh` on the re-pass report |
| 11 MD-6 | tally | `check-summary-tally.sh <dir>/requirements/ticket-api/ticket-api-report.md` |
| 12 XC-1 | none yet | manual: no `requirements/` written, each sub-case cites the correct hard-fail phase |
| 13 XC-3 | diff-confined, tally, structural | script the confinement and tally; title-equals-slug and `N/A` sections are structural greps, not yet scripted |
| 14 XC-2 | diff-confined, plus `[beh]` | zero-mutation: `check-diff-confined.sh <dir> <step1>` with no allowed globs (empty diff passes); stop-report is `[beh]`, manual |
| 15 OP-1 | none yet | manual: slice self-contained (terms backticked or defined), no `requirements/` dir |

Three scripts cover most rows because the invariants are shared, not per-row: `check-summary-tally.sh` for every report-producing row, `check-diff-confined.sh` for the committed-base confinement rows, and `check-conventions-drift.sh` for the bootstrapping rows that reach Pass 3.

## CONVENTIONS.md invariant

Every bootstrapping run that reaches Pass 3 writes `CONVENTIONS.md` (the durable structural contract) with a machine-readable enforcement stanza, and the Pass 4 tail generates the project-native lint config and gate that hold it. `settings.json` stays byte-identical, so SM-3's no-mutation check is unaffected by this feature and still passes as written.

`check-conventions-drift.sh <dir> [<base>]` is the lifecycle check for this contract, deterministic and disk-only, built from git, grep, sed, sort. It asserts three things: the config file named in the stanza exists and its runner is wired into a gate (existence), every folder under a zoned prefix has its path in the config (coverage), and any change to the contract or config since `<base>` is traced to a decision record under `decisions/` or `docs/adr/` (traceability). At bootstrap coverage is trivially green because per-feature and per-domain folders are still deferred; the check earns its keep over the project's life as folders arrive and as the contract is edited. The thinking goal sets `config: none`, `runner: review`, `zoned: none`, so only traceability runs.

Applicable rows: chain-test-small (1), chain-test-medium (2), MD-5 (5), SM-3 (6, infra), SM-1 (10), MD-6 (11, code/app), XC-2 (14, thinking). For the committed-base rows among these (MD-5, and the medium base at row 2), pass the base commit to exercise traceability; the others run existence and coverage with no base. Remaining test work, not done in this pass: a dedicated emission scenario that asserts the per-goal stanza values verbatim, and updating each applicable row's Capture column to record the `CONVENTIONS.md` stanza and the drift-check result.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.7        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
