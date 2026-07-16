# escape-check

## Purpose

Store each incoming record on arrival. (Inferred from leading prose; no explicit purpose statement in substrate.)

---

## Scope

### In Scope
- N/A — no positive-scope language found in substrate. Warning emitted.

### Out of Scope
- N/A — no negation-scope language found in substrate. Warning emitted.

---

## Actors & Consumers

| Actor | Role | Direction |
|:------|:-----|:----------|
| N/A | N/A | N/A |

Substrate names no upstream/role or downstream signal. Warning emitted.

---

## Glossary

| Term | Definition | Status |
|:-----|:-----------|:-------|
| record | Auto-derived from backtick usage in FR-001; definition pending user review. | auto-derived — verify |

---

## Functional Requirements

**FR-001** — WHEN a record arrives the system SHALL store the record.

---

## Constraints

N/A — substrate silent on constraints. Warning emitted.

---

## Acceptance Criteria

**FR-001**
- AC: given a record arrives, the store afterward contains that record.

---

## Quality Criteria scorecard

| Criterion   | Definition |
|:------------|:-----------|
| Atomic      | The requirement addresses exactly one behavior, constraint, or quality attribute. It contains a single modal verb (SHALL, MUST, SHOULD, MAY). |
| Unambiguous | All terms used are defined in the Glossary or are universally understood. No term is open to more than one interpretation. |
| Verifiable  | The requirement has at least one acceptance criterion — a condition that can be confirmed through testing, inspection, or measurement. |
| Traceable   | The requirement carries a valid, unique identifier (`<CAT>-NNN`) that enables cross-referencing, impact analysis, and change tracking. |
| Bounded     | For NFR-class requirements (NFR, OBS, SEC): the requirement specifies a quantitative threshold (value, time unit, percentage, or volume). N/A for all other requirement types. |

| Req ID | Atomic | Unambiguous | Verifiable | Traceable | Bounded |
|:-------|:------:|:-----------:|:----------:|:---------:|:-------:|
| FR-001 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
