# Requirements chain — status

Where the framing → elicitation → formalisation work stands. Companion to `requirements-chain-design.md`.

## Done

- brainstorming-requirements skill built (fresh, thin): `SKILL.md` plus `elicitation-interview.md` (how to gather) and `elicitation-template.md` (the shape to gather toward). Three phases: anchor and scope, interview, emit one component slice.
- Requirement contract defined: actor / action / result ("so that") / conditions and limitations, mapping onto EARS downstream.
- The elicit-then-write seam proven end to end on a real framing (O2, ingestion-to-gold pipeline). Core mapping extracts clean; every requirement yields a derivable acceptance criterion.
- Domain-language wiring across the full chain:
  - framing-project seeds a context-structured `CONCEPTS.md` (shared core, one block per track as a bounded context, a context map), via new `references/concepts-template.md`.
  - brainstorming-requirements consumes `CONCEPTS.md` and records new terms back; the DDD anti-pattern note sits in the interview's vocabulary step; the template's glossary discipline widened to all domain terms.
  - writing-requirements left untouched.
- Re-run with `CONCEPTS.md` in place: unresolved warnings fell from 7 to 1. The six undefined-term warnings cleared; the survivor is a benign §Constraints content gap.
- Design documented in `requirements-chain-design.md`, including a flow diagram and DDD sources.

## Test artifacts

- `outputs/seam-test-o2/` — the emitted slice and the test `CONCEPTS.md`.
- `requirements/ingestion-to-gold-pipeline/` — the requirements artifact and diagnostic report (v0.2).

## Remaining

- Decide whether the ingestion pipeline should state an invariant (the one-way `bronze`→`silver`→`gold` flow) as a constraint, to clear the last warning.
- Run the `--type technical` pass to exercise the non-functional, security, error-handling, and observability path (the generic pass covered only functional).
- Multi-component fan-out in brainstorming-requirements: one product-scope framing splitting into per-component slices.
- The system-level cross-cutting slice (latency, security, observability) and the recomposition and consistency checks, owned by an orchestrator above writing-requirements. The context map is that consistency check.
- Route architectural boundary decisions to making-architecture-decision, not brainstorming.
- Housekeeping: framing-project's SKILL.md carries no version block (pre-existing); decide whether to retrofit. Nothing is committed yet.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
