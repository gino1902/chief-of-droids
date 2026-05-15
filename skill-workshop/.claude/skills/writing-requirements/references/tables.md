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

### DR scope — what qualifies

A DR entry is warranted ONLY when the substrate specifies at least one of:
- Named fields with types (the entity has a recognisable schema)
- Field constraints (`REQUIRED`, `UNIQUE`, `FK`, `MIN`, `MAX`, `DEFAULT`)
- Lifecycle declarations (retention period, archival policy, deletion rule)

### DR exclusion list — do NOT derive DR from

- Free-form markdown files referenced as inputs or outputs — these are scoped via CON (`the system SHALL load file X`) or via IR-IN (`the system MUST accept file X`). A markdown file with no field schema is not a data entity.
- Configuration values without typed fields — these are scoped via CON or substrate constants.
- Filesystem paths as standalone artifacts — paths are scoped via CON when they are structural and via TR when they are computed (see TR rules).
- File-content blobs treated as opaque payloads — scoped via IR-IN/IR-OUT.

A useful test: if the table you would draw under `**DR-NNN**` has fewer than two field rows or the rows have no typed Constraints column entries, the entity is probably not a DR. Surface it as CON instead.

### Other rules

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

### TR candidate signals

Treat the following substrate constructs as TR candidates regardless of their syntactic placement in the substrate document:

- **Encoding/decoding rules** — "X is URL-encoded then prepended with Y", "the path is computed by …", "the identifier is derived as Z(input)"
- **Hash, digest, or fingerprint computation declarations** — "the SHA of file F is computed and stored", "a content hash is derived from …"
- **Schema mappings between named formats** — "field A in source maps to field B in target", canonical form transformations
- **Decision tables with explicit input → output rows** — substrate text already organised as "given X, produce Y" tabulation
- **Derivation rules for computed fields** — "Y is derived from X by applying rule R"

### TR exclusion list — do NOT derive TR from

- Implementation algorithms internal to a single FR action (e.g. sort order inside a list operation) — these are implementation details, not contract-level transformations.
- Validation predicates with no output transformation — these are FR Validate-shape (e.g. "verify the SHA matches" is FR; "compute the SHA from file content" is TR).
- One-off conversions that the substrate mentions in passing without naming the rule.

A useful test: if the substrate names both the input and the output but leaves the rule implicit (e.g. "the framework reads X and produces Y"), the substrate may underspecify a TR — surface as TR with a Warning rather than synthesise the rule.

### Other rules

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
| DR entries describe entities with at least one typed field or lifecycle declaration | Warning if entity is a free-form markdown file or untyped blob (re-scope to CON) |
| TR entries describe transformations matching one of the candidate-signal categories | Warning if transformation has no matching category |
