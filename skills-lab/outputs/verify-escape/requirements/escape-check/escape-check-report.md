# Report — escape-check

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |    0     |     9      |
| Info     |    2     |    N/A     |

## Phase 0 — Pre-flight
- [INFO] Args parsed: slug=escape-check, substrate=bare.md, --type generic; S1 template loaded.
- [WARNING-UNRESOLVED] No `CLAUDE.md` at cwd; cwd used as repo root (no upward walk). → Confirm `verify-escape/` is the intended repo root for outputs.

Outstanding: 0 blocking, 1 warnings, 1 info

## Phase 1 — Framing
- [WARNING-UNRESOLVED] Substrate has no H1/H2/frontmatter title; slug `escape-check` used verbatim as Title. → Add a human-readable title to the substrate.
- [WARNING-UNRESOLVED] No explicit purpose statement; Purpose inferred from leading prose. → Verify or replace the inferred Purpose.
- [WARNING-UNRESOLVED] §Scope In Scope: no positive-scope language found → rendered N/A. → State what the component covers.
- [WARNING-UNRESOLVED] §Scope Out of Scope: no negation-scope language found → rendered N/A. → State what is out of scope.
- [WARNING-UNRESOLVED] §Actors upstream: no upstream/role signal found → rendered N/A. → Name the source of arriving records.
- [WARNING-UNRESOLVED] §Actors downstream: no downstream signal found → rendered N/A. → Name any consumers of the stored records.

Outstanding: 0 blocking, 6 warnings, 0 info

## Phase 2 — Drafting
- [INFO] FR-001 rendered Event-driven from trigger "when it arrives"; contract shape Mutate (store). ERR pairing not applicable — generic (S1) has no ERR section.
- [WARNING-UNRESOLVED] §Constraints: substrate silent → rendered N/A. → Add artifact-level constraints if any apply.

Outstanding: 0 blocking, 1 warnings, 1 info

## Phase 3 — Vocabulary
- [WARNING-UNRESOLVED] Glossary term "record" auto-derived via backtick rule; definition pending user review. → Define `record` in the substrate (for example a `CONCEPTS.md`).

Outstanding: 0 blocking, 1 warnings, 0 info

## Phase 4 — Taxonomy hygiene
ID format valid (FR-001), sequence dense, no duplicates. Term "record" used in FR-001 is present in §Glossary — no term-absence Warning. EARS pattern legal; single SHALL; FR satisfies the FR-test.

Outstanding: 0 blocking, 0 warnings, 0 info

## Phase 5 — Verification
FR-001 scores ✓ on Atomic, Unambiguous (record present in §Glossary), Verifiable, Traceable; Bounded N/A (FR-class). AC derived.

Outstanding: 0 blocking, 0 warnings, 0 info

## Phase 6 — Format
Both files written to `verify-escape/requirements/escape-check/`. Version 0.1 (no prior).

Outstanding: 0 blocking, 0 warnings, 0 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
