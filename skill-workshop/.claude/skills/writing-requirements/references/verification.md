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

Score each requirement against seven criteria. Render as a single table covering all requirements.

```
| Req ID  | Atomic | Unambiguous | Verifiable | Necessary | Feasible | Traceable | Bounded |
|:--------|:------:|:-----------:|:----------:|:---------:|:--------:|:---------:|:-------:|
| FR-001  |   ✓    |      ✓      |     ✓      |    N/A    |   N/A    |     ✓     |   N/A   |
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

- ✓ if all domain-specific terms in the statement appear in §Glossary
- ✗ if one or more terms are used but not defined in §Glossary
- Emit Warning per undefined term: `FR-NNN: term "<term>" not in Glossary`

Common words and RFC 2119 keywords are exempt from this check.

### Verifiable
**Auto-scorable.**

- ✓ if a non-N/A AC entry exists for this Req ID
- ✗ if AC entry is absent or marked `N/A`

### Necessary
**N/A for all requirements.**

Cannot be determined without tracing to a source (stakeholder, regulation, use case). Mark `N/A` uniformly.

### Feasible
**N/A for all requirements.**

Cannot be assessed without design and implementation context. Mark `N/A` uniformly.

### Traceable
**Auto-scorable.**

- ✓ if the Req ID matches `<CAT>-NNN` format and the category prefix is valid
- ✗ if the ID is missing, malformed, or uses an unrecognized prefix

### Bounded
**Heuristic — NFR-class requirements only.**

Applies to: NFR, OBS, SEC entries that express a quality or SLA-type obligation.
N/A for: FR, CON, ERR, IR, DR, TR.

- ✓ if the statement or Measurement field contains a numeric value, time unit, percentage, or volume unit
- ✗ if no quantitative signal is present where measurement is expected

Emit Warning for each ✗ on Bounded in NFR-class requirements.
