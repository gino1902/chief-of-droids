# Verification — AC and Quality Scorecard

## Contents
- Acceptance Criteria (§AC)
- Quality Criteria scorecard (§QC)
- Criterion scoring rules

---

## Acceptance Criteria (§AC)

Derive one or more acceptance criteria per requirement where possible.

Entry format:
```
**<REQ-ID>**
- AC: <verifiable condition>
- AC: <verifiable condition>
```

**Derivation approach by requirement type:**

| Type | AC derivation |
|:--|:--|
| FR, CON (EARS) | Derive from the `SHALL` action: what an observer can verify in a test |
| ERR (Unwanted Behavior EARS) | Derive from the error condition and response: given condition X, system produces Y |
| IR (RFC 2119) | Derive from the `MUST`/`SHOULD` contract: the interface accepts / emits the specified payload |
| NFR (RFC 2119 + measurement) | Derive from the Measurement field: the metric meets the stated threshold under the stated conditions |
| SEC (RFC 2119 or EARS) | Derive from the security obligation: access is granted/denied, audit record is produced |
| OBS (RFC 2119) | Derive from the observability statement: the metric, log, or trace is emitted as specified |
| DR (contract table) | Derive from field constraints: required fields present, unique constraints enforced, FK valid |
| TR (rule table) | Derive from the Input → Output mapping: given input row, output matches expected result |

If no derivable AC exists for a requirement, emit Warning and render:
```
**<REQ-ID>**
- AC: N/A — no verifiable condition derivable from substrate
```

---

## Quality Criteria scorecard (§QC)

Render a definitions block first, then the scorecard table.

**Definitions block** (render verbatim in output):

```
| Criterion   | Definition |
|:------------|:-----------|
| Atomic      | The requirement addresses exactly one behavior, constraint, or quality attribute. It contains a single modal verb (SHALL, MUST, SHOULD, MAY). |
| Unambiguous | All terms used are defined in the Glossary or are universally understood. No term is open to more than one interpretation. |
| Verifiable  | The requirement has at least one acceptance criterion — a condition that can be confirmed through testing, inspection, or measurement. |
| Traceable   | The requirement carries a valid, unique identifier (`<CAT>-NNN`) that enables cross-referencing, impact analysis, and change tracking. |
| Bounded     | For NFR-class requirements (NFR, OBS, SEC): the requirement specifies a quantitative threshold (value, time unit, percentage, or volume). N/A for all other requirement types. |
```

**Scorecard table** (follows immediately after definitions):

```
| Req ID  | Atomic | Unambiguous | Verifiable | Traceable | Bounded |
|:--------|:------:|:-----------:|:----------:|:---------:|:-------:|
| FR-001  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| NFR-001 |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
```

---

## Criterion scoring rules

### Atomic
**Auto-scorable.**

Count modal verbs per requirement statement: `SHALL`, `MUST`, `SHOULD`, `MAY`.
- Exactly 1 modal → ✓
- More than 1 modal → ✗ (compound requirement; flag for splitting)
- Table-form entries (DR, TR) → ✓ by default (tables are structurally atomic per row)

### Unambiguous
**Heuristic.**

- ✓ if every domain term in the statement appears in §Glossary
- ✗ if one or more domain terms are used but not defined in §Glossary
- Do not emit a Warning here. The term-absence Warning is emitted once, by the Phase 4 "Terms used in requirements are present in §Glossary" check. This criterion consumes that same finding to set the ✗ score and references it (e.g. "Unambiguous ✗ — see Phase 4 term-absence Warning"). One absent term is one Warning across the run, counted in Phase 4, never re-emitted here.

A domain term is any noun or noun phrase naming a thing the requirement acts on or produces — its objects, inputs, and outputs. Exempt — never counted as domain terms — are only this closed set: the terms in the Phase 3 stop-word list; the RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) and EARS keywords (`SHALL`, `WHEN`, `WHILE`, `IF`, `THEN`, `WHERE`); and the EARS subject, meaning the component under specification (the `system` in `the system SHALL …`). Everything else the requirement names and the Glossary does not define scores ✗.

Do not widen the exemption to an open notion of "common words". That open exemption is exactly what lets an undefined domain object pass silently — for example a lowercase `record` in `the system SHALL store each record`, which is a domain term (the object the requirement acts on), not a common word. The skill flags such a term; it never invents a definition. The upstream fix is to define it in `CONCEPTS.md`, not to exempt it here.

### Verifiable
**Auto-scorable.**

- ✓ if a non-N/A AC entry exists for this Req ID
- ✗ if AC entry is absent or marked `N/A`

### Traceable
**Auto-scorable.**

- ✓ if the Req ID matches `<CAT>-NNN` format and the category prefix is valid
- ✗ if the ID is missing, malformed, or uses an unrecognized prefix

### Bounded
**Heuristic — applies to NFR-class requirements only; N/A for all others.**

NFR-class: NFR, OBS, SEC when expressing a quality or SLA-type obligation.
N/A for: FR, CON, ERR, IR, DR, TR.

**How Bounded is evaluated:**

Step 1 — Identify whether the requirement is NFR-class. If not, mark `N/A` and stop.

Step 2 — Scan the requirement statement and its Measurement field (if present) for a quantitative signal:
- Numeric value (e.g. `200`, `99.9`, `10`)
- Time unit (e.g. `ms`, `seconds`, `minutes`, `hours`, `days`)
- Percentage (e.g. `%`, `percent`)
- Volume or size unit (e.g. `MB`, `GB`, `requests`, `records`)

Step 3 — Score:
- ✓ if at least one quantitative signal is found
- ✗ if none is found — the requirement is unbounded (e.g. "The system MUST respond quickly")

Emit Warning for each ✗ on Bounded.
