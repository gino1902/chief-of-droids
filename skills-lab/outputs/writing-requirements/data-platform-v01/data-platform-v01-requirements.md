# SQLI Data Platform

## Purpose

The Data Platform is the central component where SQLI stores, organises, and serves enterprise data for analytics, reporting, and downstream applications. It performs raw ingestion of bulk data from the Landing Zone, transforms raw data into business-ready, standardised datasets, owns and enforces data contracts, governs enterprise data through its catalogue, enforces data-asset-level access control under RGPD and SQLI policy, and emits observability and audit signals for the data flows it manages.

## Scope

### In Scope

- Raw ingestion of bulk data from the Landing Zone
- Transformation of raw data into business-ready, standardised datasets
- Ownership of data contracts and association of every data asset with exactly one contract and one producing subsystem
- Enterprise data catalogue and governance
- Data-asset-level access control compliant with RGPD/GDPR and SQLI data access policy
- Observability of incoming and outgoing data flows in the Data Platform's scope
- Auditability and lineage of data production and consumption
- Traceability of data usage and cost per Unit and Department
- Encryption of data in transit crossing external trust boundaries
- Manual on-demand pull triggering by authorised operators
- Exposure of authorised data assets to external end-users

### Out of Scope

- Orchestration and supervision of inter-subsystem data pulls (owned by the System)
- Source-side scheduled pull execution from SaaS or cloud-tenant subsystems into the Landing Zone
- Landing Zone storage format, lifecycle, and 7-day retention
- Push of data from producing subsystems into the Landing Zone
- Active Directory authentication mechanism (the System enforces; the Data Platform consumes identity assertions)
- Observability of data exchanges not in the Data Platform's scope (managed by the System)

## Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| Landing Zone | Source of raw bulk data for ingestion | upstream |
| Producing subsystems | Originate data assets; deliver via the Landing Zone | upstream |
| Consuming subsystems | Pull business-ready, standardised datasets from the Data Platform | downstream |
| External end-users (authorised) | Consume authorised data assets directly | downstream |
| Authorised operators | Manually trigger pull actions on demand | user |
| The System (orchestrator) | Orchestrates and supervises inter-subsystem pulls; provides AD-mediated identity assertions | upstream |
| Active Directory (via the System) | Source of authenticated identity used for access decisions | upstream |
| Data owners / stewards | Accountable for data quality, classification, and contract adherence per asset | user |

## Glossary

| Term | Definition | Status |
|:--|:--|:--|
| Access control | Rules that decide who can see or use each data asset. | substrate |
| Active Directory | Microsoft's central directory of company users, passwords, and groups; relied on for identity and entitlements. | substrate |
| Auditability | The ability to reconstruct, after the fact, who did what with which data and when. | substrate |
| Authorised operator | A human role permitted to manually trigger pull actions on demand. | auto-derived — verify |
| Bulk data | A large batch of records moved together in one go. | substrate |
| Business-ready dataset | Standardised data shaped for direct consumption by business workflows; contrasted with raw data. | auto-derived — verify |
| C4 (model) | Standard four-zoom-level architecture diagramming. | substrate |
| Cloud tenant | The company's private space inside a public cloud provider. | substrate |
| Data asset | A distinct, named piece of data with an owner, contract, and quality level. | substrate |
| Data catalogue | Indexed inventory of all the data the company holds. | substrate |
| Data classification | Labelling data by sensitivity (public, internal, confidential, personal). | substrate |
| Data contract | Written agreement between producer and consumers describing format, fields, freshness, and quality. | substrate |
| Data flow | Movement of data from one system to another along a defined path. | substrate |
| Data freshness | Recency of data relative to its source; expressed as latency between source change and platform availability. | auto-derived — verify |
| Data in transit | Data while moving across a network. | substrate |
| Data leakage | Data ending up where it should not be. | substrate |
| Data Platform | The central system where SQLI stores, organises, and serves data for analytics, reporting, and downstream applications. | substrate |
| Dead-letter | Holding area for messages or records that failed to process and could not be retried. | substrate |
| Encryption | Scrambling data with a key so interceptors cannot read it without the key. | substrate |
| GDPR / RGPD | European regulation on personal data protection. | substrate |
| Heterogeneous (subsystems) | Subsystems built on different technologies that need translation to exchange data. | substrate |
| Landing Zone | Temporary storage area where raw incoming data is dropped first. | substrate |
| Latency | Delay between request and response. | substrate |
| Observability | Ability to see, from the outside, what a system is doing — logs, metrics, traces. | substrate |
| Payload | Actual content carried in a single transfer. | substrate |
| Pull (vs Push) | Pull: destination asks for data. Push: source sends without being asked. | substrate |
| Raw ingestion | Loading data into the platform exactly as it arrived, with no transformation. | substrate |
| Retention (policy) | Rule for how long data is kept before automatic deletion. | substrate |
| Retry policy | Rule for how many times and how often the system retries a failed action. | substrate |
| RPO (Recovery Point Objective) | Maximum acceptable amount of recent data lost in a failure, in time. | substrate |
| RTO (Recovery Time Objective) | Maximum acceptable downtime after a failure. | substrate |
| SaaS | Software hosted by a vendor and accessed over the internet. | substrate |
| Scheduled pull | Data transfer that runs automatically at fixed time or interval. | substrate |
| Single point of failure | Component whose breakdown brings the whole system down. | substrate |
| SLA | Formal commitment to a level of service with contractual consequences. | substrate |
| SLO | Internal target a team aims for, usually stricter than the SLA. | substrate |
| Standardised data | Data reshaped to a common format, naming, and unit convention. | substrate |
| Structured data | Data that fits cleanly in tables with defined columns. | substrate |
| Semi-structured data | Data that has some structure but stays flexible (JSON, XML). | substrate |
| Unstructured data | Data with no predefined structure. | substrate |
| Subsystem | Self-contained part of the wider system with its own job and boundary. | substrate |
| Subsystem-agnostic format | Storage format chosen so any authorised subsystem can consume it. | substrate |
| Trust boundary | Line between two zones with different security rules. | substrate |

## Functional Requirements

**FR-001** — WHEN a scheduled pull window opens the Data Platform SHALL pull bulk data from the Landing Zone for raw ingestion.

**FR-002** — The Data Platform SHALL transform raw data into business-ready, standardised datasets.

**FR-003** — The Data Platform SHALL expose business-ready, standardised datasets for consumption by authorised subsystems.

**FR-004** — WHEN an authorised operator issues an on-demand pull request the Data Platform SHALL execute the pull action.

**FR-005** — The Data Platform SHALL govern enterprise data through its catalogue.

**FR-006** — The Data Platform SHALL maintain explicit accountability for data quality per data asset.

**FR-007** — The Data Platform SHALL apply data classification per SQLI policy to every data asset.

**FR-008** — The Data Platform SHALL support consumption of authorised data assets by external end-users.

**FR-009** — The Data Platform SHALL expose data assets required for defined business workflows.

## Interface Requirements

### Inbound (IR-IN)

**IR-IN-001** — The Data Platform MUST accept identity assertions issued by Active Directory through the System for every consumer access request.

**IR-IN-002** — The Data Platform MUST accept raw bulk data pulled from the Landing Zone in a subsystem-agnostic format.

**IR-IN-003** — The Data Platform MUST accept on-demand pull trigger requests from authorised operators.

### Outbound (IR-OUT)

**IR-OUT-001** — The Data Platform MUST expose business-ready, standardised datasets for consumption by authorised subsystems.

**IR-OUT-002** — The Data Platform MUST expose its catalogue to authorised consumers for data discovery and lookup.

**IR-OUT-003** — The Data Platform MUST expose authorised data assets to authenticated external end-users.

## Data Requirements

### Data Requirements (DR)

**DR-001** — Data Contract

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|
| `asset_id` | string | REQUIRED UNIQUE | Identifier of the governed data asset |
| `producer_subsystem` | string | REQUIRED | Single producing subsystem (one per asset) |
| `schema` | object | REQUIRED | Format, fields, types per contract |
| `data_kind` | enum | REQUIRED | structured / semi-structured / unstructured |
| `classification` | enum | REQUIRED | SQLI classification label |
| `quality_owner` | string | REQUIRED | Accountable party for data quality |
| `retention_policy` | string | REQUIRED | Per SQLI retention policy beyond the Landing Zone |
| `freshness_target` | string | OPTIONAL | Source-to-availability latency target (TBD per asset) |

**DR-002** — Data Asset

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|
| `asset_id` | string | REQUIRED UNIQUE FK → Data Contract | |
| `name` | string | REQUIRED | Human-readable name |
| `owner_subsystem` | string | REQUIRED | Producing subsystem |
| `classification` | enum | REQUIRED | Inherited from contract |
| `lifecycle_state` | enum | REQUIRED | active / deprecated / archived |
| `created_at` | timestamp | REQUIRED | |

**DR-003** — Audit Event

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|
| `event_id` | string | REQUIRED UNIQUE | |
| `actor` | string | REQUIRED | Identity from AD assertion |
| `action` | enum | REQUIRED | produce / consume / access-denied / config-change |
| `asset_id` | string | REQUIRED FK → Data Asset | |
| `timestamp` | timestamp | REQUIRED | |
| `location` | string | REQUIRED | Source or destination address |

### Transformation Requirements (TR)

**TR-001** — Raw to business-ready dataset standardisation

| Input | Rule | Output |
|:--|:--|:--|
| Raw record from Landing Zone for asset A | Apply contract-defined schema, naming, and unit convention for A; reject records that fail contract validation (route to ERR-002) | Business-ready, standardised record for asset A |

> ⚠️ Unverified — concrete transformation rules per asset are not in substrate; Rule column captures the generic mapping. Per-asset rules to be defined in design phase.

## Non-Functional Requirements

**NFR-001** — The Data Platform MUST sustain at least 50 scheduled pulls per day. | Measurement: ≥ 50 successful scheduled pulls / 24 h.

**NFR-002** — The Data Platform MUST process payloads of up to 10 MB per pull. | Measurement: max accepted payload ≥ 10 MB per pull.

**NFR-003** — The Data Platform MUST support raw ingestion from at least 10 distinct source subsystems. | Measurement: ≥ 10 distinct source subsystems concurrently configured.

**NFR-004** — Inter-subsystem interactions involving the Data Platform MUST have no single point of failure. | Measurement: TBD (redundancy / failover topology to be defined in design phase).

**NFR-005** — The Data Platform MUST meet SLA targets for availability, latency, and freshness. | Measurement: TBD with Business Users in design phase.

**NFR-006** — The Data Platform SHOULD meet internal SLO targets for data freshness stricter than the contracted SLA. | Measurement: TBD with Business Users in design phase.

## Security

**SEC-001** — The Data Platform MUST enforce access control at data-asset level per RGPD and SQLI data access policy.

**SEC-002** — The Data Platform MUST encrypt data in transit crossing external trust boundaries.

**SEC-003** — IF a data leakage condition is detected THEN the Data Platform SHALL block the affected flow and emit an audit event per SQLI data security policy.

**SEC-004** — The Data Platform MUST comply with GDPR and SQLI data security policy on retention, storage, RTO, and RPO. | Measurement: RTO and RPO thresholds TBD.

**SEC-005** — The Data Platform MUST integrate with Active Directory through the System for user authentication and authorisation.

**SEC-006** — The Data Platform MUST produce audit records compliant with SQLI auditability policy.

## Constraints

**CON-001** — The Data Platform SHALL associate each data asset with exactly one producing subsystem.

**CON-002** — The Data Platform SHALL associate each data asset with exactly one data contract.

**CON-003** — The Data Platform SHALL own all data contracts of the data assets it serves.

**CON-004** — The Data Platform SHALL accept structured, semi-structured, and unstructured data classes.

**CON-005** — The Data Platform SHALL retain data beyond the Landing Zone in compliance with SQLI data retention policy.

**CON-006** — The Data Platform SHALL accept raw ingestion only via the Landing Zone.

## Error Handling

**ERR-001** — IF a scheduled pull from the Landing Zone fails THEN the Data Platform SHALL retry per the defined retry policy. → FR-001

> ⚠️ Unverified — retry policy parameters TBD in substrate (NFR1).

**ERR-002** — IF a record cannot be successfully retried or fails contract validation THEN the Data Platform SHALL route the record to a dead-letter store and emit an error event. → FR-002

> ⚠️ Unverified — dead-letter destination and inspection workflow TBD (NFR2).

**ERR-003** — IF an unauthorised access attempt to a data asset occurs THEN the Data Platform SHALL deny the request and emit an audit event. → FR-005

**ERR-004** — IF an on-demand pull triggered by an operator fails THEN the Data Platform SHALL surface the failure to the requesting operator with a diagnostic code. → FR-004

## Observability

**OBS-001** — The Data Platform MUST emit observability signals (logs, metrics, traces) for incoming and outgoing data flows in its scope.

**OBS-002** — The Data Platform MUST record actor, timestamp, and location for every data production and consumption event.

**OBS-003** — The Data Platform MUST track data usage and cost per Unit and Department. | Measurement: aggregation granularity ≥ Unit and Department.

**OBS-004** — The Data Platform MUST expose audit and lineage records compliant with SQLI auditability policy.

## Acceptance Criteria

**FR-001**
- AC: A scheduled pull window triggers a pull from the Landing Zone within the configured tolerance.
- AC: Pulled records appear in raw ingestion storage with payload bytes equal to the source.

**FR-002**
- AC: For a sample raw record matching contract C, the corresponding business-ready record is produced and matches the contract schema.

**FR-003**
- AC: An authorised consuming subsystem retrieves the business-ready dataset for asset A and receives data conforming to contract C.

**FR-004**
- AC: An on-demand pull request from an authorised operator results in a pull execution recorded in the audit log within the configured tolerance.

**FR-005**
- AC: Every data asset present in the platform is discoverable through the catalogue with owner, contract, and classification populated.

**FR-006**
- AC: For every data asset, a non-empty `quality_owner` is recorded and queryable.

**FR-007**
- AC: For every data asset, a `classification` label drawn from the SQLI policy enumeration is recorded.

**FR-008**
- AC: An authenticated authorised external end-user retrieves an authorised data asset and is denied for a non-authorised one.

**FR-009**
- AC: N/A — no verifiable condition derivable from substrate (business workflows not enumerated).

**IR-IN-001**
- AC: A request without a valid AD identity assertion is rejected; a request with one is processed.

**IR-IN-002**
- AC: A pull from the Landing Zone in the agreed subsystem-agnostic format is parsed without format-translation errors.

**IR-IN-003**
- AC: An on-demand pull request from an authenticated authorised operator is accepted and dispatched.

**IR-OUT-001**
- AC: A consuming subsystem call returns business-ready records conforming to the contract schema.

**IR-OUT-002**
- AC: A catalogue lookup by an authorised consumer returns the asset metadata.

**IR-OUT-003**
- AC: An external end-user access call returns the authorised data asset and is denied for non-authorised assets.

**DR-001**
- AC: Inserting a Data Contract row without `asset_id`, `producer_subsystem`, `schema`, `data_kind`, `classification`, `quality_owner`, or `retention_policy` is rejected.
- AC: Two Data Contract rows with the same `asset_id` are rejected by the UNIQUE constraint.

**DR-002**
- AC: Inserting a Data Asset whose `asset_id` does not match an existing Data Contract is rejected by the FK.

**DR-003**
- AC: Each production, consumption, and access-denied action produces an Audit Event row with all REQUIRED fields populated.

**TR-001**
- AC: Given a sample raw record from the Landing Zone matching contract C, the produced business-ready record matches the contract's standardised schema.
- AC: A raw record failing contract validation is not produced as business-ready and is routed per ERR-002.

**NFR-001**
- AC: Over a measurement window of 7 days, the daily count of successful scheduled pulls is ≥ 50.

**NFR-002**
- AC: A pull payload of 10 MB is processed without truncation or rejection.

**NFR-003**
- AC: At least 10 distinct source subsystems are concurrently configured and each produces at least one successful pull during the measurement window.

**NFR-004**
- AC: N/A — measurement TBD; redundancy / failover topology to be defined in design phase.

**NFR-005**
- AC: N/A — SLA thresholds TBD with Business Users.

**NFR-006**
- AC: N/A — SLO thresholds TBD with Business Users.

**SEC-001**
- AC: An access request to data asset A by an identity not entitled per RGPD/SQLI policy is denied and logged.

**SEC-002**
- AC: A network capture on a flow crossing an external trust boundary shows only ciphertext.

**SEC-003**
- AC: A simulated leakage signal triggers flow blocking and an audit event within the configured tolerance.

**SEC-004**
- AC: N/A — RTO and RPO thresholds TBD.

**SEC-005**
- AC: An access request without an AD identity assertion is rejected; one with a valid assertion is authorised per the user's group memberships.

**SEC-006**
- AC: For every privileged or access-denied action, an audit record is produced and is retrievable per SQLI audit policy.

**CON-001**
- AC: An attempt to register a second producer for an existing data asset is rejected.

**CON-002**
- AC: An attempt to attach a second contract to an existing data asset is rejected.

**CON-003**
- AC: All data contracts in scope are owned by the Data Platform team / role; foreign ownership is rejected at registration.

**CON-004**
- AC: A data asset of each class (structured, semi-structured, unstructured) can be onboarded successfully.

**CON-005**
- AC: A data asset retention period configured outside the SQLI policy enumeration is rejected.

**CON-006**
- AC: A raw ingestion attempt bypassing the Landing Zone is rejected.

**ERR-001**
- AC: A simulated Landing Zone pull failure produces N retries per the policy and a final outcome event.

**ERR-002**
- AC: A record failing repeated retries or contract validation appears in the dead-letter store with an error event.

**ERR-003**
- AC: An unauthorised access attempt is denied and produces an audit event with `action = access-denied`.

**ERR-004**
- AC: An on-demand pull failure produces an error response to the operator with a diagnostic code and an audit event.

**OBS-001**
- AC: For each in-scope flow, logs, metrics, and traces are emitted to the configured destinations.

**OBS-002**
- AC: For each production and consumption event, the audit / observability record contains actor, timestamp, and location.

**OBS-003**
- AC: A usage and cost report can be produced per Unit and per Department for any rolling 30-day window.

**OBS-004**
- AC: For any data asset, a lineage view is retrievable per SQLI auditability policy.

## Quality Criteria scorecard

| Criterion   | Definition |
|:------------|:-----------|
| Atomic      | The requirement addresses exactly one behavior, constraint, or quality attribute. It contains a single modal verb (SHALL, MUST, SHOULD, MAY). |
| Unambiguous | All terms used are defined in the Glossary or are universally understood. No term is open to more than one interpretation. |
| Verifiable  | The requirement has at least one acceptance criterion — a condition that can be confirmed through testing, inspection, or measurement. |
| Traceable   | The requirement carries a valid, unique identifier (`<CAT>-NNN`) that enables cross-referencing, impact analysis, and change tracking. |
| Bounded     | For NFR-class requirements (NFR, OBS, SEC): the requirement specifies a quantitative threshold (value, time unit, percentage, or volume). N/A for all other requirement types. |

| Req ID    | Atomic | Unambiguous | Verifiable | Traceable | Bounded |
|:----------|:------:|:-----------:|:----------:|:---------:|:-------:|
| FR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-003    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-004    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-005    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-006    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-007    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-008    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-009    |   ✓    |      ✗      |     ✗      |     ✓     |   N/A   |
| IR-IN-001 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-002 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-003 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-001|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-002|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-003|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| DR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| DR-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| DR-003    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| TR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| NFR-001   |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
| NFR-002   |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
| NFR-003   |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
| NFR-004   |   ✓    |      ✓      |     ✗      |     ✓     |    ✗    |
| NFR-005   |   ✓    |      ✓      |     ✗      |     ✓     |    ✗    |
| NFR-006   |   ✓    |      ✓      |     ✗      |     ✓     |    ✗    |
| SEC-001   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| SEC-002   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| SEC-003   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| SEC-004   |   ✓    |      ✓      |     ✗      |     ✓     |    ✗    |
| SEC-005   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| SEC-006   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-001   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-002   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-003   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-004   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-005   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-006   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-001   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-002   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-003   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-004   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| OBS-001   |   ✓    |      ✓      |     ✓      |     ✓     |    ✗    |
| OBS-002   |   ✓    |      ✓      |     ✓      |     ✓     |    ✗    |
| OBS-003   |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
| OBS-004   |   ✓    |      ✓      |     ✓      |     ✓     |    ✗    |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-06 |
| Status       | Draft      |
