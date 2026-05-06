# Template — Technical (S2)

Fifteen sections, always rendered. `N/A` if substrate signal absent.

| # | Section | ID prefix | Syntax |
|:--|:--|:--|:--|
| 1 | Title + Purpose | — | Prose |
| 2 | Scope | — | In/Out lists or `N/A` |
| 3 | Actors & Consumers | — | Table |
| 4 | Glossary | — | Table |
| 5 | Functional Requirements | `FR-NNN` | EARS |
| 6 | Interface Requirements | `IR-IN-NNN` / `IR-OUT-NNN` | RFC 2119 + Event-driven EARS |
| 7 | Data Requirements | `DR-NNN` / `TR-NNN` | Contract / Rule tables |
| 8 | Non-Functional Requirements | `NFR-NNN` | RFC 2119 + measurement |
| 9 | Security | `SEC-NNN` | RFC 2119 + Unwanted Behavior EARS |
| 10 | Constraints | `CON-NNN` | EARS |
| 11 | Error Handling | `ERR-NNN` | Unwanted Behavior EARS |
| 12 | Observability | `OBS-NNN` | RFC 2119 |
| 13 | Acceptance Criteria | — | Per-requirement |
| 14 | Quality Criteria scorecard | — | Per-requirement table |
| 15 | Version block | — | Table |

---

## §1 Title + Purpose

```markdown
# <component name>

## Purpose
<one paragraph>
```

---

## §2 Scope

```markdown
## Scope

### In Scope
- <item>

### Out of Scope
- <item>
```

Both subsections render even if one is `N/A`.

---

## §3 Actors & Consumers

Table with columns: Actor | Role | Direction.

Direction values: `upstream`, `downstream`, `user`.

---

## §4 Glossary

```markdown
| Term | Definition | Status |
|:-----|:-----------|:-------|
| term | definition | auto-derived — verify |
| term | definition | substrate |
```

One row per term. Status values: `auto-derived — verify` for auto-extracted terms; `substrate` for terms explicitly defined in the input.

---

## §5 Functional Requirements

```markdown
**FR-NNN** — [EARS statement]
```

---

## §6 Interface Requirements

Two sub-sections, both always rendered:

```markdown
### Inbound (IR-IN)
**IR-IN-NNN** — [RFC 2119 statement or Event-driven EARS]

### Outbound (IR-OUT)
**IR-OUT-NNN** — [RFC 2119 statement or Event-driven EARS]
```

---

## §7 Data Requirements

Two sub-sections, both always rendered:

```markdown
### Data Requirements (DR)
**DR-NNN** — <entity name>

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|

### Transformation Requirements (TR)
**TR-NNN** — <transformation name>

| Input | Rule | Output |
|:--|:--|:--|
```

See `references/tables.md` for column rules.

---

## §8 Non-Functional Requirements

```markdown
**NFR-NNN** — [RFC 2119 statement] | Measurement: [metric and threshold]
```

---

## §9 Security

```markdown
**SEC-NNN** — [RFC 2119 statement or Unwanted Behavior EARS]
```

---

## §10 Constraints

```markdown
**CON-NNN** — [EARS statement]
```

---

## §11 Error Handling

```markdown
**ERR-NNN** — [Unwanted Behavior EARS] → <FR-NNN>
```

---

## §12 Observability

```markdown
**OBS-NNN** — [RFC 2119 statement]
```

---

## §13 Acceptance Criteria

See `references/verification.md`.

---

## §14 Quality Criteria scorecard

See `references/verification.md`.

---

## §15 Version block

```markdown
| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.x        |
| Last Updated | YYYY-MM-DD |
| Status       | Draft      |
```
