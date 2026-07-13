# Ingestion to gold pipeline

## Purpose

This pipeline reads and writes data from an external `landing zone` into the `bronze` layer, then transforms it through `silver` to `gold`, so that the business is exposed trustworthy, high-quality enterprise data.

## Scope

### In Scope
- Reading and writing `landing zone` data into the `bronze` layer
- The `bronze`-to-`silver` transformation, cleansing and conforming the data
- The `silver`-to-`gold` transformation, building `enterprise entities`
- Gating publication to `gold` on `data-quality rules`

### Out of Scope
- Populating the `landing zone` (owned by IT, the middleware that pushes data)
- Data governance and the catalog / `Unity Catalog` (owned by the Platform engineering track)
- Exposing `gold` data through agentic workflows (owned by the Data exposition track)

## Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| External `landing zone` (populated by IT middleware) | Source of raw data read into `bronze` | upstream |
| Data exposition layer and its agentic workflows | Consume the `gold` layer | downstream |
| Platform engineering team | Operates and runs the pipeline | user |

## Glossary

| Term | Definition | Status |
|:--|:--|:--|
| `landing zone` | External staging area the IT middleware pushes source data into, read by `bronze` | auto-derived — verify |
| `bronze` | Raw-ingest layer preserving source data as delivered | auto-derived — verify |
| `silver` | Cleansed and conformed layer derived from `bronze` | auto-derived — verify |
| `gold` | Enterprise-entity layer exposing trusted, high-quality data | auto-derived — verify |
| `source contract` | The agreed shape a delivered file must match to be ingested | auto-derived — verify |
| `enterprise entities` | Conformed business objects built in `gold` from `silver` | auto-derived — verify |
| `quarantine` | Holding area for records that fail validation, kept out of `silver` | auto-derived — verify |
| `business key` | The natural key that uniquely identifies an enterprise entity | auto-derived — verify |
| `reference data` | Shared lookup data an enterprise entity resolves against | auto-derived — verify |
| `data-quality rules` | Validation rules gating publication to `gold` | auto-derived — verify |

## Functional Requirements

**FR-001** — WHEN a dataset is delivered to the `landing zone`, the pipeline SHALL write it into the `bronze` layer within 30 minutes, for files matching the agreed `source contract`.

**FR-002** — The pipeline SHALL write the landed data into the `bronze` layer in its exact form. _(rationale: the ingested data is preserved in its prior form, retained for audit)_

**FR-003** — WHEN `bronze` data is available, the pipeline SHALL cleanse and conform it into the `silver` layer.

**FR-004** — IF a record fails validation THEN the pipeline SHALL send it to `quarantine` rather than write it to the `silver` layer.

**FR-005** — WHEN building `enterprise entities` in the `gold` layer from the `silver` layer, the pipeline SHALL produce entities with a unique `business key` and all `reference data` resolved.

**FR-006** — WHEN publishing to the `gold` layer, the pipeline SHALL publish only data passing the defined `data-quality rules`.

**FR-007** — IF fewer than 99% of records pass the defined `data-quality rules` THEN the pipeline SHALL hold the batch for review.

**FR-008** — WHEN the same delivery is replayed, the pipeline SHALL produce `gold` records idempotently, without duplicates.

## Constraints

N/A — substrate silent on artifact-level invariants distinct from the functional requirements. Warning emitted.

## Acceptance Criteria

**FR-001**
- AC: given a dataset delivered to the `landing zone` matching the agreed `source contract`, the `bronze` layer contains it within 30 minutes of delivery.
- AC: a file not matching the `source contract` is not written to `bronze`.

**FR-002**
- AC: the record written to `bronze` is byte-identical to the delivered source record.

**FR-003**
- AC: given `bronze` data, the `silver` layer contains the cleansed and conformed records.

**FR-004**
- AC: given a record that fails validation, it appears in `quarantine` and not in `silver`.

**FR-005**
- AC: each `enterprise entity` has a unique `business key`.
- AC: each `enterprise entity` has all `reference data` resolved (no unresolved references).

**FR-006**
- AC: only records passing the defined `data-quality rules` appear in `gold`.

**FR-007**
- AC: given a batch in which fewer than 99% of records pass the `data-quality rules`, the batch is held for review and not published to `gold`.

**FR-008**
- AC: replaying the same delivery produces no duplicate `gold` records.

## Quality Criteria scorecard

| Criterion   | Definition |
|:------------|:-----------|
| Atomic      | The requirement addresses exactly one behavior, constraint, or quality attribute. It contains a single modal verb (SHALL, MUST, SHOULD, MAY). |
| Unambiguous | All terms used are defined in the Glossary or are universally understood. No term is open to more than one interpretation. |
| Verifiable  | The requirement has at least one acceptance criterion — a condition that can be confirmed through testing, inspection, or measurement. |
| Traceable   | The requirement carries a valid, unique identifier (`<CAT>-NNN`) that enables cross-referencing, impact analysis, and change tracking. |
| Bounded     | For NFR-class requirements (NFR, OBS, SEC): the requirement specifies a quantitative threshold (value, time unit, percentage, or volume). N/A for all other requirement types. |

| Req ID | Atomic | Unambiguous | Verifiable | Traceable | Bounded |
|:--|:--:|:--:|:--:|:--:|:--:|
| FR-001 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-002 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-003 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-004 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-005 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-006 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-007 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-008 | ✓ | ✓ | ✓ | ✓ | N/A |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.2        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
