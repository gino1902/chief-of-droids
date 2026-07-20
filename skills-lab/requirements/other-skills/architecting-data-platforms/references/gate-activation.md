# Gate Activation — How It Works

The gate check in `data-platform-architect` is triggered automatically when Claude
detects a phase completion or next-phase start signal. No explicit command is needed.

## What activates it

Say anything that signals a phase is done or the next is starting:

- "Phase 3 is done"
- "We finished the requirements brief"
- "ADRs are approved, moving on"
- "Starting the security design"
- "Are we ready for phase 5?"
- Share or describe a new deliverable

Claude will recognise the signal, confirm if ambiguous, then run the gate check
before proceeding.

## What the gate check produces

1. Gate condition result for the completed phase
2. Document maturity assessment (version, sign-off, traceability)
3. Relevant alignment checks
4. BLOCKING findings surfaced — next phase does not start until resolved
5. Offer to write the assessment to `use-case-{id}/test/assessment-phase-{N}-{YYYY-MM-DD}.md`

## To write the assessment doc

Confirm when Claude offers. It will propose the exact path and wait for approval
before writing. The saved doc becomes version evidence for future alignment checks.

## To run a full assessment at any time

Trigger the Assessment Workflow directly:

> "Where are we?" / "What's missing?" / "Are we on track?"

Claude will run intake (Step 1) and produce a full Phase Status Table across all phases.
