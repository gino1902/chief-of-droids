# ticket-api

## Purpose
The ticket API creates and fetches support tickets for agents, so that support work has one record per request. It records a ticket from a submitted payload and returns a ticket by id.

## Scope

### In Scope
- Creating a ticket from a submitted payload
- Fetching a ticket by id

### Out of Scope
- Assignment routing (owned by the routing service)
- Notifications (owned by the notifier)

## Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| agent | Calls the API over HTTP; submits payloads and reads tickets | upstream |
| ticket store | Persists a ticket | downstream |

## Glossary

| Term | Definition | Status |
|:-----|:-----------|:-------|
| ticket | A support record created per request and persisted by the ticket store. | auto-derived — verify |
| agent | The caller that submits payloads to and reads tickets from the API over HTTP. | auto-derived — verify |
| `ticket.created` | The metric emitted on each ticket creation. | auto-derived — verify |

## Functional Requirements

**FR-001** — WHEN a valid payload is submitted, the system SHALL create a ticket from the payload.

**FR-002** — WHEN an existing ticket id is requested, the system SHALL return the corresponding ticket.

## Interface Requirements

### Inbound (IR-IN)

**IR-IN-001** — The system MUST accept a ticket payload from the agent over HTTP.

**IR-IN-002** — The system MUST accept a ticket id from the agent over HTTP.

### Outbound (IR-OUT)

**IR-OUT-001** — The system MUST return the ticket to the agent.

## Data Requirements

### Data Requirements (DR)

N/A — substrate provides no typed data-model signal (no named fields, constraints, or lifecycle declarations). Warning emitted.

### Transformation Requirements (TR)

N/A — substrate provides no transformation signal. Warning emitted.

## Non-Functional Requirements

**NFR-001** — N/A — substrate silent on reliability/correctness. Warning emitted.

**NFR-002** — The system SHOULD return a requested ticket within 300 ms at the 95th percentile. | Measurement: p95 fetch latency ≤ 300 ms

## Security

**SEC-001** — The system MUST permit only the agent assigned to a ticket to read that ticket.

## Constraints

**CON-001** — The system SHALL keep a ticket id unchanged once it is assigned.

## Error Handling

**ERR-001** — IF a create does not complete successfully THEN the system SHALL reject the create and surface an error to the agent. → FR-001

**ERR-002** — IF a requested ticket id does not resolve to a ticket THEN the system SHALL surface a not-found error to the agent. → FR-002

## Observability

**OBS-001** — The system MUST emit a `ticket.created` metric on each ticket creation.

## Acceptance Criteria

**FR-001**
- AC: given a valid payload, a ticket is created and persisted to the ticket store.
- AC: the created ticket derives from the submitted payload.

**FR-002**
- AC: given an existing ticket id, the corresponding ticket is returned.

**IR-IN-001**
- AC: a ticket payload sent by the agent over HTTP is accepted.

**IR-IN-002**
- AC: a ticket id sent by the agent over HTTP is accepted.

**IR-OUT-001**
- AC: the requested ticket is returned to the agent.

**NFR-002**
- AC: measured p95 fetch latency is ≤ 300 ms under representative load.

**SEC-001**
- AC: the agent assigned to a ticket is permitted to read it.
- AC: an agent not assigned to a ticket is denied read access.

**CON-001**
- AC: a ticket id is identical across repeated reads after assignment.

**ERR-001**
- AC: given a create that does not complete, an error is surfaced to the agent and no ticket is persisted.

**ERR-002**
- AC: given a ticket id that resolves to no ticket, a not-found error is surfaced to the agent.

**OBS-001**
- AC: each successful create emits exactly one `ticket.created` metric.

## Quality Criteria scorecard

| Criterion   | Definition |
|:------------|:-----------|
| Atomic      | The requirement addresses exactly one behavior, constraint, or quality attribute. It contains a single modal verb (SHALL, MUST, SHOULD, MAY). |
| Unambiguous | All terms used are defined in the Glossary or are universally understood. No term is open to more than one interpretation. |
| Verifiable  | The requirement has at least one acceptance criterion — a condition that can be confirmed through testing, inspection, or measurement. |
| Traceable   | The requirement carries a valid, unique identifier (`<CAT>-NNN`) that enables cross-referencing, impact analysis, and change tracking. |
| Bounded     | For NFR-class requirements (NFR, OBS, SEC): the requirement specifies a quantitative threshold (value, time unit, percentage, or volume). N/A for all other requirement types. |

| Req ID     | Atomic | Unambiguous | Verifiable | Traceable | Bounded |
|:-----------|:------:|:-----------:|:----------:|:---------:|:-------:|
| FR-001     |   ✓    |     ✗       |     ✓      |     ✓     |   N/A   |
| FR-002     |   ✓    |     ✓       |     ✓      |     ✓     |   N/A   |
| IR-IN-001  |   ✓    |     ✓       |     ✓      |     ✓     |   N/A   |
| IR-IN-002  |   ✓    |     ✓       |     ✓      |     ✓     |   N/A   |
| IR-OUT-001 |   ✓    |     ✓       |     ✓      |     ✓     |   N/A   |
| NFR-001    |  N/A   |    N/A      |    N/A     |     ✓     |   N/A   |
| NFR-002    |   ✓    |     ✓       |     ✓      |     ✓     |    ✓    |
| SEC-001    |   ✓    |     ✓       |     ✓      |     ✓     |   N/A   |
| CON-001    |   ✓    |     ✓       |     ✓      |     ✓     |   N/A   |
| ERR-001    |   ✓    |     ✓       |     ✓      |     ✓     |   N/A   |
| ERR-002    |   ✓    |     ✓       |     ✓      |     ✓     |   N/A   |
| OBS-001    |   ✓    |     ✓       |     ✓      |     ✓     |   N/A   |

Notes:
- FR-001 Unambiguous ✗ — see Phase 4 term-absence Warning for "payload".
- NFR-001 is the substrate-silent universal reliability slot; only Traceable applies (valid ID).
- SEC-001 and OBS-001 are NFR-class but express access-control and metric-presence obligations, not quality/SLA thresholds; Bounded is N/A.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
