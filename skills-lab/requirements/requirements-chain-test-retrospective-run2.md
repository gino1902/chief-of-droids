# Requirements chain — test run retrospective, run 2

A row-by-row retrospective of the second run-through, executed live against the tightened suite on branch `tighten-requirements-chain-tests` (R1 committed-base diffs, R5 canonical base). Companion to `requirements-chain-test-retrospective-run1.md` (the first run-through), `tests/test-strategy.md` (the priority table), and `requirements-chain-design.md` (what each row proves).

The two run-throughs are kept as separate files on purpose, so the drift between them reads directly rather than through git history. The drift column in the table below, and the Drift analysis section, are the point of this document.

Unlike run 1, which was reconstructed from surviving disk artifacts after the fact, run 2 was marked live, scenario by scenario, as each fresh session reported its result.

## Evidence basis

Each scenario ran in its own fresh Claude Code session per the strategy's §Session model, and reported its result into one coordinating session that marked it against the row's acceptance criteria in real time. The five diff-based rows (MD-1, MD-2, MD-3, MD-5, MD-7) and the two commit-diff rows (SM-3, XC-2) produced a `git diff` against a committed base, inspected live.

Integrity note. Near the end of the run the entire `outputs/` working tree was deleted by a mis-scoped `rm`. The git-tracked content (`outputs/predictability/`, `outputs/writing-requirements/`) was restored from the index. The untracked test dirs, the committed `test-medium` base at `0400673`, and the `.diff` evidence artifacts were lost. Every verdict below was captured live before the deletion, so the record is intact, but the artifacts are no longer on disk to re-inspect. This inverts run 1's basis: run 1 had the artifacts and no live log, run 2 has the live log and not the artifacts.

Verdict tags: `[obs]` observed live (the session reported the report line, diff, or end-state and it was checked against the criteria), `[beh]` a behavioural criterion confirmed from the session's live report.

## Marked priority table

| # | Scenario | Run 2 verdict | Observed evidence (run 2) | Drift vs run 1 |
|:--|:--|:--|:--|:--|
| 1 | chain-test-small | Pass `[obs]` | `0 blocking, 4 warnings, 0 info`, all acceptable (1 §Constraints N/A, 3 auto-glossary verify). No `CONCEPTS.md`, single component. | Run 1 was `0/0/0`. The four acceptable warnings are the resolution-model accounting, not a regression. |
| 2 | chain-test-medium | Pass `[obs]` | Base now observed and committed at `0400673`. Canonical FR list FR-001 to FR-005 (FR-005 the IF/THEN quality-rule withholding requirement). `CONCEPTS.md` context-structured, three Track contexts. `0/9/0`, all acceptable. | Run 1 base was `[inf]` (inferred from the MD-1 diff). Now `[obs]`. Off-by-one closed: five FRs confirmed canonical, not four. |
| 3 | MD-1 iteration | Pass `[obs]` | v0.1 to 0.2, FR-001 to FR-005 byte-stable as diff context, FR-006 the sole added ID (retention). `md-1.diff` additive only. | Run 1 `[obs]` but reconstructed. Now diff-provable, and R5's relative-ID phrasing verified (nothing keyed on a hard-coded count). |
| 4 | MD-2 framing-update | Pass `[obs]` | `md-2.diff` a single FRAMING.md hunk (the "Our approach" section). `CONCEPTS.md` and every other section absent. Stamp and frontmatter intact. | Run 1 Unverified (needed the transcript). The committed-base diff closed it. Caveat: the `last_updated`-advances AC is untestable on a same-day base. |
| 5 | MD-5 reconcile | Pass `[obs]` | Empty `md-5.diff` (true no-op reconcile). Pass 2 took the framing-project update branch, no size question, no inline reconcile. `settings.json` and tree untouched. | Run 1 Unverified. The 0-line diff is decisive proof of reconcile-not-regenerate, which the end-state alone could not show. |
| 6 | SM-3 resume | Pass `[obs]` + `[beh]` confirmed | Preamble detected Pass 1 done, resumed at Pass 2, re-elicited the goal (not inferred from the dir name), infra tree, `settings.json` unchanged (61-line diff = the four new Pass 2 to 4 files only). | Run 1 `[obs]` tree/goal, `[beh]` resume-detect unverified. Resume-detect and re-elicitation now confirmed live. |
| 7 | MD-4 warnings-loop | Pass `[obs]` | Pass one flagged the vague FR-002 with a no-derivable-AC warning; pass two cleared it after the 30-minute predicate landed. Warnings 5 to 4, v0.1 to 0.2, FR-001 stable. | Run 1 Unverified. The chain's most load-bearing dotted arrow now has live evidence. |
| 8 | MD-3 concepts-reuse | Pass `[obs]`, CONCEPTS layer | Verbatim reuse of `gold layer` and `cross-team report`, `report definition` written back to the Exposition block. `md-3.diff` +29 / -0 (zero deletion lines). | Run 1 partial at the CONCEPTS layer. Now diff-provable additive. Still not formalised through writing-requirements (R3 parked). |
| 9 | MD-7 divergence | Pass `[obs]`, CONCEPTS layer | `owner` under both contexts with distinct definitions, context-map divergence row, Run 1's Governance entry preserved. `md-7.diff` 75 lines, all insertions, no synonym, not in shared core. | Run 1 partial at the CONCEPTS layer. The additive-only diff now proves the preservation property. R3 parked. |
| 10 | SM-1 upgrade | Pass `[obs]` | Small branch fired (no `CONCEPTS.md`, no Tracks), upgrade reached Medium+ shape, undefined-term warnings 4 to 0, v0.1 to 0.2. framing-project converted the five-question doc via a clean Phase 1b path, no reconciliation. | Run 1 `[obs]` at `0/0/0`. Now the mitigation is measured (the 4 to 0 delta) rather than asserted. |
| 11 | MD-6 technical | Pass `[obs]` with defect | Full S2 skeleton: FR, CON (id invariant), NFR (p95 ≤ 300 ms, Bounded ✓), SEC and OBS (content, Bounded ✗ with warnings, correct), ERR-001/002 paired to their FRs, no undefined-term. `0 blocking, 14 warnings` (all acceptable). Defect: Summary Info tally reports 5 but the body carries 7 `[INFO]` lines. | Run 1 `[obs]` at `0/0/0`. The 14 warnings are resolution-model accounting. The Info-tally defect surfaced only under live counting, which run 1's reconstruction could not do. |
| 12 | XC-1 guards | Pass `[obs]` | Six sub-cases hard-failed at the correct Phase 0 step (0.2 slug x2, 0.3 type x2, 0.4 path, 0.8 extension), no output files. Sub-case 6 created no dir (Phase 0.6 has no mkdir); the walk resolved to `skills-lab` but never wrote. | Run 1 `[obs]`. New detail: the test's "Expected outputs" wrongly predicts an empty `requirements/user-auth/` for sub-case 6. |
| 13 | XC-3 degraded | Pass `[obs]` + escape re-confirmed | Title fell back to the slug `bare-spec` verbatim, Scope/Actors/Glossary/Constraints all `N/A` + Warning, the SHALL line kept as FR-001, `record` flagged undefined with no fabricated definition, both files written, `0/8/1`. Unscaffolded run wrote to `skills-lab/requirements/bare-spec/` (deleted). | Run 1 hit the same escape and contained it with a scaffold `CLAUDE.md`. Run 2 re-confirmed the escape live against the current skill and pinned the fix to Phase 0.5. |
| 14 | XC-2 goal-lock | Pass `[obs]` + `[beh]` confirmed | Thinking tree only, conflict report printed verbatim (stamp `thinking` versus argument `code`), `xc-2.diff` empty (0-byte, clean `git status`). | Run 1 `[obs]` scaffold, `[beh]` stop-report unverified for no-mutation. The empty diff now proves zero mutation. |
| 15 | OP-1 standalone | Pass `[obs]` | File-anchored Phase 0 confirmed (read `FRAMING.md` from disk, no sibling `CONCEPTS.md`, proceeded). Self-contained slice, all terms backticked or defined. Terminal. Two of four requirements carried predicates, two correctly flagged OPEN rather than invented. | Run 1 `[obs]` but chat-anchored in the first attempt this run. The clean re-run closed the file-anchored Phase 0 gap and demonstrated the flag-open contract. |

Tally: 15 of 15 pass. Every cell is `[obs]` or `[obs]` plus a `[beh]` confirmed live. Run 1's split was seven full `[obs]`, four partial or `[beh]`, one `[inf]`, three unverified.

## The findings that mattered

1. The tightening closed every weak cell. Run 1's three unverified rows (MD-2, MD-5, MD-4) and its inferred base all read as observed in run 2, because the committed-base diff supplies an end-state artifact where behavioural and mutation criteria previously left none. MD-5 is the clearest case: reconcile-not-regenerate went from "not confirmable from the end-state" to a zero-line diff.
2. A new formaliser defect surfaced that run 1 had masked. `writing-requirements --type technical` undercounts the Summary Info tally, reporting 5 when the body carries 7 `[INFO]` lines. Live counting caught it; run 1's `0/0/0` reconstruction could not.
3. The repo-root-walk escape was re-confirmed live against the current skill. With no local `CLAUDE.md`, Phase 0.5 climbed to `skills-lab` and wrote outputs there. The fix belongs in the skill's Phase 0.5 root resolution, not in a per-test scaffold.
4. The git-init open item is empirically settled. `bootstrapping-project` gates `git init` behind user confirmation and treats a parent `.git/` as not counting, which is why each test dir carried its own repo only after a confirmed init.

## Drift analysis, run 1 to run 2

- Coverage drift. Eight non-full cells in run 1 (three unverified, one inferred, four partial or `[beh]`) all resolved to observed in run 2. This is attributable to the tightening, the committed-base diffs and the canonical base, not to any skill change.
- Warning-count drift. Several rows show more warnings than run 1: small 0 to 4, medium 0 to 9, technical 0 to 14, degraded 7 to 8. Every added warning is acceptable-category (auto-glossary verify entries and `N/A` sections), reflecting the `conventions.md` resolution-model change that now surfaces auto-derived glossary entries as `WARNING-UNRESOLVED`. None is a regression.
- Base drift. Run 1 assumed four FRs for the medium base and carried an off-by-one through every MD count. Run 2 confirms five canonical FRs, committed and diffed. R5 removed the drift class at its source.
- New-defect drift. The MD-6 Info-tally defect is visible only in run 2, because it was found by live counting rather than end-state reconstruction.
- No behavioural regressions. Every skill behaviour run 1 observed, run 2 re-observed identically or with stronger evidence.

## Reading, inference not observed

Kept separate so it carries no factual weight it has not earned.

- The tightening's value concentrates in the diff-based rows. The committed base converts "trust the transcript" into "read the diff", which is exactly what moved MD-2 and MD-5 from unverified to decisive.
- The MD-6 Info-tally defect points at a general gap: no row asserts that the Summary tallies reconcile with the body counts. An automatic reconcile check would catch a whole class of tally bugs.
- OP-1's two attempts illustrate interview-depth sensitivity. Predicates settle only as far as the interview runs, and the skill correctly flags the rest open. Not a defect, but a reminder that a standalone brainstorm's completeness tracks interview depth.

## Open follow-ups

- Parked tightening decisions from the session analysis. R2, a durable oracle for the two `[beh]` rows, now less urgent since both were confirmed live, but still transcript-dependent. R3, whether MD-3 and MD-7 should formalise through writing-requirements or stay scoped to the CONCEPTS layer. R4, unmask the XC-3 and SM-3 defects in the tests now that the escape is re-confirmed.
- Skill fixes. The `writing-requirements` Summary Info tally (MD-6). The `writing-requirements` Phase 0.5 repo-root anchoring (XC-3 escape).
- Test-doc corrections. The XC-1 "Expected outputs" empty-dir prediction, since no dir is created. The MD-2 `last_updated`-advances AC, untestable on a same-day base, so backdate the base or reword the AC.
- Re-run hygiene. The mid-run deletion argues for committing or relocating `.diff` evidence out of `outputs/` promptly, since `outputs/` is disposable scratch and a stray `rm` takes the evidence with it.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
