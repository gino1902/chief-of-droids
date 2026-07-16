# Verify Summary Info tally — writing-requirements fix check

_Targeted verification of a single skill fix, not a chain scenario. It confirms the `conventions.md` reconciliation invariant: the §Summary Info Resolved count equals the number of `[INFO]` lines in the report body. Run it after the fix at commit `115b30d`._

## Purpose

Run 2 (MD-6, `--type technical`) found `writing-requirements` undercounting the Summary Info tally: the Summary read 5 while the body carried 7 `[INFO]` lines. The fix extends the report-format reconciliation invariant so Info is counted from the body, not tallied independently. This check reproduces the discriminating condition, a technical report with several `[INFO]` lines, and confirms the counts now reconcile.

## Directory and precedence

Directory: `outputs/verify-info-tally`, created by this check.

Precedence: none against the chain suite. Independent, single-skill. Run after the `conventions.md` fix is in place.

## Preconditions

- A fresh session.
- The directory `skills-lab/outputs/verify-info-tally` exists and is empty. Session cwd is that directory.
- Add a minimal `CLAUDE.md` to the directory (one line is enough) so the Phase 0.5 repo-root walk anchors here and outputs do not escape to the `skills-lab` root. This is setup scaffold, not a skill artifact.
- Create the slice fixture `ticket-api.md` below. It carries functional, invariant, non-functional, security, and observability signals, so the technical formaliser renders several S2 sections and the report emits several `[INFO]` trace lines.

```markdown
# ticket-api

## Purpose
The ticket API creates and fetches support `ticket`s for `agent`s, so support work has one record per request.

## Scope
Covers creating a `ticket` from a submitted payload, and fetching a `ticket` by id. Out of scope: assignment routing (owned by the routing service); notifications (owned by the notifier).

## Actors and consumers
Upstream, the `agent` calling the API over HTTP. Downstream, the ticket store that persists a `ticket`.

## Requirements
- The system shall create a `ticket` from a submitted payload, so that the request is recorded, when the payload is valid.
- The system shall return a `ticket` by id, so that the agent reads it, when the id exists.
- A `ticket` id, once assigned, never changes. (static invariant)
- Fetch shall return within 300 ms at the 95th percentile. (non-functional)
- Only the `agent` assigned to a `ticket` may read it. (security)
- Every create emits a `ticket.created` metric. (observability)
```

## Run steps

### 1. Formalise the slice, technical

Invoke `writing-requirements ticket-api from ticket-api.md --type technical`.

## Verification

Run these against the emitted `requirements/ticket-api/ticket-api-report.md`:

1. Count the body `[INFO]` lines:
   ```
   grep -c "\[INFO\]" requirements/ticket-api/ticket-api-report.md
   ```
2. Read the §Summary Info Resolved cell.
3. Read the report-level `Outstanding:` line's `info` figure.

## Acceptance criteria

- The §Summary Info Resolved cell equals the `grep -c "\[INFO\]"` count exactly. This is the fix under test: no undercount, no overcount.
- Info Unresolved is `N/A`.
- The report-level `Outstanding:` `info` figure equals the Summary Info Resolved cell.
- Regression check, the other severities still reconcile: the Summary Warning Resolved and Unresolved cells equal the counts of `[WARNING-RESOLVED]` and `[WARNING-UNRESOLVED]` lines respectively, and the Blocking cells likewise. The fix must not have disturbed these.

## Fail conditions

- The Summary Info Resolved cell differs from the body `[INFO]` line count (the original defect, or a new over/undercount).
- Info Unresolved is populated with anything other than `N/A`.
- Any Warning or Blocking Summary cell no longer matches its suffix-line count (regression from the fix).

## Record

Note the `[INFO]` line count, the Summary Info Resolved cell, and the `Outstanding:` info figure, and confirm all three agree. Note the Warning and Blocking reconciliation held.

## Note

This verifies the fix behaviourally on the discriminating condition (a technical report with several `[INFO]` lines). The durable regression guard is separate: a Summary-reconciles-body acceptance criterion added to MD-6 and, in principle, every chain row, so future runs catch tally drift without this standalone check.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
