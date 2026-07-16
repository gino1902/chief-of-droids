# Capture command

This command handles adding a `book` to the `pile` from a single invocation, so that a book just heard of is saved before it is forgotten.

## In scope
- Covers taking a title, with an optional author, from the `reader`  (R-01)
- Handles appending the `book` to the `pile` as an `unread entry`  (R-01)
- Responsible for rejecting an empty title  (R-02)
- Covers appending without a duplicate check, so a matching `book` may appear more than once  (R-03)
- Responsible for persisting the new entry to the `pile file` for later commands to read  (R-04)

## Out of scope
- Listing the `pile`, owned by a later `list` command
- Editing or removing entries, owned by later edit and remove commands
- Sync and backup, excluded by the FRAMING local-only constraint (no owning component)

## Actors and consumers
- Upstream: the `reader`, typing the command at the terminal
- Downstream: the `pile file`, which later commands read

## Requirements
- The system shall append a `book` to the `pile` as an `unread entry`, so that a book just heard of is saved before it is forgotten, when the `reader` supplies a non-empty title with an optional author.  (R-01)
- The system shall reject the input, so that no invalid entry enters the `pile`, when the supplied title is empty.  (R-02) — OPEN: the observable form of rejection (error message, exit code) was not settled.
- The system shall append the `book` without checking for duplicates, so that capture stays a single frictionless step, when a matching `book` already exists in the `pile`.  (R-03)
- The system shall persist the appended entry to the `pile file`, so that a later command can read it.  (R-04) — OPEN: whether durability is guaranteed before the command returns, and any success confirmation, were not settled.

## Notes
Requirements were partially elicited; the interview stopped before the observable predicates for R-02 and R-04 were settled. The OPEN flags mark genuine gaps, not invented conditions. Terms settled this pass (no `CONCEPTS.md` present to record back to): `pile`, `pile file`, `book`, `unread entry`, `reader`.

Recommended downstream type: `generic` — the slice carries no non-functional, security, or observability requirements.

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
