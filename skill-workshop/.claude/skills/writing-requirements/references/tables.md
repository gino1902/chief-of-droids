# Table-form Requirements — DR and TR (T3/T4)

## Contents
- DR — Data Requirements
- TR — Transformation Requirements
- Phase 4 hygiene checks

---

## DR — Data Requirements (T3)

Data requirements define the data entities the component owns, persists, or transmits: schema, field constraints, and lifecycle.

Entry format:
```
**DR-NNN** — <entity name>

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|
| `field_name` | string / int / bool / timestamp / … | REQUIRED / OPTIONAL / UNIQUE / FK → <entity> / DEFAULT <value> / MAX <n> | Description or lifecycle note |
```

Rules:
- No RFC 2119 keywords and no EARS syntax inside DR tables.
- Constraints column values: `REQUIRED`, `OPTIONAL`, `UNIQUE`, `FK → <entity>`, `DEFAULT <value>`, `MAX <n>`, `MIN <n>`. Combine with space separation where needed (e.g. `REQUIRED UNIQUE`).
- Lifecycle notes (retention period, archival, deletion policy) belong in the Notes column or as a follow-on entry.
- One DR-NNN entry per distinct data entity or significant field grouping.
- If substrate provides no data model signal, render the DR sub-section as `N/A` + Warning.

---

## TR — Transformation Requirements (T4)

Transformation requirements define processing rules: deterministic mappings from inputs to outputs.

Entry format:
```
**TR-NNN** — <transformation name>

| Input | Rule | Output |
|:--|:--|:--|
| <input condition or value range> | <processing or decision rule> | <output result or action> |
```

Rules:
- No RFC 2119 keywords and no EARS syntax inside TR tables.
- Rule column describes the deterministic mapping or decision logic — not the implementation.
- One TR-NNN entry per discrete transformation or rule set.
- Multiple rows in a single TR-NNN table describe different input cases for the same transformation.
- If substrate provides no transformation signal, render the TR sub-section as `N/A` + Warning.

---

## Phase 4 hygiene checks (T3/T4)

| Check | Severity |
|:--|:--|
| DR entries use contract table form — no RFC 2119, no EARS | Warning |
| TR entries use rule table form — no RFC 2119, no EARS | Warning |
| DR table includes all four columns: Field, Type, Constraints, Notes | Warning if a column is missing |
| TR table includes all three columns: Input, Rule, Output | Warning if a column is missing |
| Each DR-NNN and TR-NNN entry has a descriptive name | Warning if name is absent or generic |
