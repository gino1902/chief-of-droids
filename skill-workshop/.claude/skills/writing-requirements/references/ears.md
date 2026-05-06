# EARS — Behavioral Requirements (T1)

## Contents
- EARS patterns
- Pattern selection heuristics
- FR drafting rules
- Constraints drafting rules
- ERR drafting rules
- Phase 4 hygiene checks

---

## EARS patterns

| Pattern | Template | When to use |
|:--|:--|:--|
| Ubiquitous | `The <system> SHALL <action>.` | Always-true behaviors; system-level properties |
| Event-driven | `WHEN <trigger> the <system> SHALL <action>.` | Responses to external events or inputs |
| State-driven | `WHILE <state> the <system> SHALL <action>.` | Behaviors active during a persistent condition |
| Unwanted Behavior | `IF <condition> THEN the <system> SHALL <action>.` | Error cases, guard conditions, threat mitigations |
| Optional Feature | `WHERE <feature> is included the <system> SHALL <action>.` | Conditional or licensed capabilities |

RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) do not appear in EARS statements. Use `SHALL` for all mandatory behavior in EARS.

---

## Pattern selection heuristics

| Substrate signal | Pattern |
|:--|:--|
| "always", "at all times", "continuously", "invariant" | Ubiquitous |
| "when", "upon", "after", "on receipt of", "triggered by", "in response to" | Event-driven |
| "while", "during", "as long as", "in state", "when in mode" | State-driven |
| "if … then", "in case of", "on failure", "on error", "invalid", "unauthorized", "exceeds" | Unwanted Behavior |
| "if the feature is enabled", "when configured for", "optionally", "licensed" | Optional Feature |

When multiple patterns fit, prefer the most specific one. Ubiquitous is the fallback when no trigger, state, or condition is present.

---

## FR drafting rules

- One `SHALL` statement per FR-NNN entry. Split compound behaviors into separate entries.
- Scope: behaviors of the subject component itself — not behaviors expected of external systems.
- If substrate uses RFC 2119 language for a functional behavior, translate to EARS on output.
- Do not mix EARS `SHALL` and RFC 2119 keywords (`MUST`, `SHOULD`) in the same statement.
- Group by logical area if more than five entries; grouping is for readability, not an ID boundary.

---

## Constraints drafting rules

Constraints are conditions that bound design or implementation choices without specifying functional behavior directly.

- S1: use `FR-NNN` IDs continuing the FR sequence; section heading `## Constraints`.
- S2: use `CON-NNN` IDs; section heading `## Constraints`.
- Choose the EARS pattern that best matches the constraint; Ubiquitous and State-driven are most common.
- If the constraint is implementation-neutral (a non-negotiable property), use Ubiquitous.

---

## ERR drafting rules

Error handling requirements use Unwanted Behavior EARS exclusively.

Entry format:
```
**ERR-NNN** — IF <error condition> THEN the <system> SHALL <response action>. → <FR-NNN>
```

The cross-link `→ FR-NNN` identifies the functional requirement whose error path this covers.

Rules:
- One error condition per ERR-NNN entry.
- The response action must be concrete: log, reject, retry, surface to caller, roll back. "Handle the error" is not acceptable.
- Every FR that has an error path SHOULD have a corresponding ERR entry; emit Warning if absent.
- If no corresponding FR exists for an ERR entry, emit Warning (orphan ERR).

---

## Phase 4 hygiene checks (T1)

| Check | Severity |
|:--|:--|
| Each FR and CON entry uses a legal EARS pattern | Warning |
| Each ERR entry uses Unwanted Behavior EARS exclusively | Warning |
| Each ERR entry contains a cross-link to an existing FR | Warning if missing or target not found |
| Each FR and CON entry contains exactly one `SHALL` | Warning if compound (more than one `SHALL`) |
| RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) absent from EARS statements | Warning if present |
