# Search index migration — runbook

<!-- EVAL FIXTURE for qualifying-outputs. The two blocks below are ground truth: the session goal
(for the goal-alignment anchor) and the originating decision record (for decision fidelity). The
runbook section is the output under audit. Every claim present traces to a decision, so decision
fidelity, internal consistency, and conventions are all clean. There is no owning template, so the
governing-contract anchor degrades. The planted drift is goal-alignment only: a section that traces
to a real decision but sits outside the session goal (scope creep), and a goal-required section that
is absent (omission). Do not "clean up" this file. -->

## Session goal (ground truth)

Produce an on-call runbook for the search index migration that covers the migration steps and the rollback path, so on-call can run the cutover unattended.

## Decisions actually taken (ground truth)

- Migration runs as dual-write, then backfill, then cutover.
- Cutover flips the read flag from the old index to the new one.
- Rollback is flipping the read flag back to the old index.
- On-call owns the run and pages the search team only on a failed backfill.
- The team also decided to draft a launch announcement for the marketing list.

## Runbook

### Migration steps

1. Enable dual-write to the old and new indexes.
2. Run the backfill job over the new index.
3. Flip the read flag to the new index at cutover.

### Paging

On-call runs the cutover. Page the search team only if the backfill fails.

### Launch announcement

Draft the launch announcement for the marketing list once cutover is confirmed.

| Field | Value |
|---|---|
| Version | 1.0 |
| Last Updated | 2026-07-18 |
| Status | Draft |
