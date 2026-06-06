# SQLI – Data Platform Creation

## Purpose

The Data Platform is the central system through which SQLI moves, governs, and serves enterprise data across heterogeneous subsystems. It manages scheduled and on-demand data flows from SaaS applications and cloud-tenant sources into a single Landing Zone, ingests raw data, transforms it into business-ready standardised datasets, and exposes governed data to authorised consuming subsystems and external end-users. It owns data contracts, enforces access control, and provides observability over enterprise data exchanges.

> ⚠️ Purpose paragraph inferred from substrate prose; substrate contains no explicit "purpose" statement.

## Scope

### In Scope

- Data flow management between heterogeneous subsystems (SaaS applications, the Data Platform, cloud-tenant databases or applications).
- Scheduled and on-demand bulk pulls from source subsystems into a single Landing Zone.
- Inbound pushes from producing subsystems into the Landing Zone (state changes, security compliance events).
- Landing Zone storage in a subsystem-agnostic format with 7-day retention and automatic erasure thereafter.
- Raw ingestion from the Landing Zone into the Data Platform.
- Transformation of raw data into business-ready, standardised datasets.
- Exposure of business-ready data to authorised consuming subsystems and to authorised external end-users.
- Catalogue-based governance of all enterprise data.
- Ownership and enforcement of data contracts (one contract per data asset, single-producer rule).
- Per-asset accountability for data quality.
- Data classification compliant with SQLI policy.
- Access control to the Data Platform (Active Directory) and at data-asset level (RGPD + SQLI data access policy).
- Encryption of data in transit across external trust boundaries.
- Observability of incoming and outgoing data flows; production/consumption traceability (who, when, where).
- Audit records compliant with SQLI policy.
- Usage and cost traceability per Unit and Department.
- Compliance with GDPR and SQLI data security policy (retention, storage, RTO, RPO).

### Out of Scope

- N/A

> ⚠️ Out of Scope: substrate provides no explicit out-of-scope signals. Multiple "TBD" / "in design phase" markers (F8, F17, NFR1, NFR2, NFR6, NFR7) flag deferred items, not exclusions.

## Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| SaaS application (source subsystem) | Producer of bulk source data pulled into the Landing Zone | upstream |
| Cloud-tenant database or application | Producer of bulk source data; may also consume | upstream |
| Producing subsystem | Initiates ad-hoc pushes of state changes or compliance events into the Landing Zone | upstream |
| Active Directory | Identity provider for platform access decisions | upstream |
| Consuming subsystem | Pulls business-ready data and/or Landing Zone data within its workflow scope | downstream |
| Authorised external end-user | Consumes governed data exposed by the Data Platform | downstream / user |
| Authorised operator | Triggers manual pull actions and supervises orchestration | user |
| Business User | Defines SLA and freshness/latency targets in the design phase | user |
| Monitoring consumer | Receives observability signals (flows, usage, cost, audit) | downstream |

> ⚠️ Specific subsystem identities, operator roles, and business-user roles are not enumerated in substrate; rows describe abstract roles only.

## Glossary

| Term | Definition | Status |
|:-----|:-----------|:-------|
| Access control | The rules that decide who can see or use each piece of data — like the badges that decide which rooms an employee can enter. | substrate |
| Active Directory | Microsoft's central directory of company users, their passwords, and the groups they belong to. Other tools rely on it to know who someone is and what they're allowed to do. | substrate |
| Auditability | The ability to reconstruct, after the fact, who did what with which data and when. Required for legal and compliance checks. | substrate |
| Bulk data | A large batch of records moved together in one go (e.g. all of yesterday's orders), as opposed to one record at a time. | substrate |
| C4 (model) | A standard way of drawing software architecture diagrams in four zoom levels: System, Container, Component, Code. | substrate |
| Cloud tenant | The company's own private space inside a public cloud provider (Azure, AWS, GCP). | substrate |
| Data asset | A distinct, named piece of data treated as a managed object — e.g. "customer master list", "monthly sales report". Has an owner, a contract, and a quality level. | substrate |
| Data catalogue | An indexed inventory of all the data the company holds. | substrate |
| Data classification | Labelling data by sensitivity (public, internal, confidential, personal). | substrate |
| Data contract | A written agreement between a data producer and its consumers, describing the format, fields, freshness, and quality the producer guarantees. | substrate |
| Data flow | The movement of data from one system to another along a defined path. | substrate |
| Data in transit | Data while it is moving across a network (vs. *data at rest*, which sits in storage). | substrate |
| Data leakage | Data ending up where it should not be (wrong recipient, public website, unauthorised system). | substrate |
| Data Platform | The central system where the company stores, organises, and serves data for analytics, reporting, and downstream applications. | substrate |
| Dead-letter | A holding area for messages or records that failed to process and could not be retried. | substrate |
| Encryption | Scrambling data with a key so that anyone intercepting it cannot read it without the key. | substrate |
| GDPR / RGPD | The European regulation on personal data protection. RGPD is the French acronym for the same law. | substrate |
| Heterogeneous (subsystems) | Subsystems built on different technologies that don't naturally speak the same language and therefore need translation to exchange data. | substrate |
| Landing Zone | A temporary storage area where raw incoming data is dropped first, before being cleaned, transformed, or used downstream. | substrate |
| Latency | The delay between when something is requested and when the answer arrives. | substrate |
| Observability | The ability to see, from the outside, what a system is doing — what's flowing through it, what's failing, how fast, how often. | substrate |
| Payload | The actual content carried in a single transfer (the file or the records), excluding the technical envelope around it. | substrate |
| Pull (vs Push) | *Pull*: the destination system asks for the data. *Push*: the source system sends the data without being asked. | substrate |
| Raw ingestion | Loading data into the platform exactly as it arrived, with no cleaning or transformation. | substrate |
| Retention (policy) | The rule for how long data is kept before being automatically deleted. | substrate |
| Retry policy | The rule for how many times, and how often, the system should automatically try again when an action fails. | substrate |
| RPO (Recovery Point Objective) | Maximum acceptable amount of recent data lost in a failure, measured in time. | substrate |
| RTO (Recovery Time Objective) | Maximum acceptable downtime after a failure. | substrate |
| SaaS (Software as a Service) | Software hosted by a vendor and accessed over the internet. | substrate |
| Scheduled pull | A data transfer that runs automatically at a fixed time or interval. | substrate |
| Single point of failure | A component whose breakdown brings the whole system down because there is no backup. | substrate |
| SLA (Service Level Agreement) | A formal commitment to a level of service, with contractual or financial consequences if missed. | substrate |
| SLO (Service Level Objective) | The internal target a team aims for — usually stricter than the SLA. | substrate |
| Standardised data | Data reshaped to a common format, naming, and unit convention so different downstream uses can consume it the same way. | substrate |
| Structured data | Data that fits cleanly in tables with defined columns. | substrate |
| Semi-structured data | Data that has some structure but stays flexible (JSON, XML). | substrate |
| Unstructured data | Data with no predefined structure (PDFs, emails, images, audio). | substrate |
| Subsystem | A self-contained part of the wider system, with its own job and boundary. | substrate |
| Subsystem-agnostic format | A storage format chosen so that no single subsystem's technology is required to read it. | substrate |
| Trust boundary | The line between two zones with different security rules. Crossing one usually requires extra protection like encryption or authentication. | substrate |
| Authorised operator | A human user permitted by SQLI user access policy to trigger and supervise data pulls. | auto-derived — verify |
| Authorised subsystem | A subsystem permitted by access policy to read data from the Landing Zone or the Data Platform. | auto-derived — verify |
| Authorised external end-user | A non-employee user permitted to consume data exposed by the Data Platform. | auto-derived — verify |
| Producing subsystem | A subsystem in the role of source for a given data asset; uniquely produces that asset under the single-producer rule. | auto-derived — verify |
| Consuming subsystem | A subsystem in the role of consumer for a given data asset; pulls only what its workflow requires. | auto-derived — verify |
| Source subsystem | The subsystem from which a scheduled or on-demand pull retrieves data. Used interchangeably with "producing subsystem" in the pull direction. | auto-derived — verify |
| Business-ready data | Data that has been cleaned, standardised, and shaped to be directly usable by business workflows without additional transformation by the consumer. | auto-derived — verify |
| Business workflow | An end-to-end process that consumes data from the Data Platform to deliver a business outcome (reporting, analytics, operational decision). | auto-derived — verify |
| Unit & Department | Internal SQLI organisational units used for cost and usage attribution. | auto-derived — verify |
| SQLI data retention policy | Internal policy defining retention periods and erasure rules for data held beyond the Landing Zone. Referenced; document not provided in substrate. | auto-derived — verify |
| SQLI data security policy | Internal policy defining security obligations including data leakage prevention. Referenced; document not provided in substrate. | auto-derived — verify |
| SQLI data access policy | Internal policy defining access-control rules at data-asset level. Referenced; document not provided in substrate. | auto-derived — verify |
| SQLI user access policy | Internal policy defining user authentication and authorisation rules; enforced via Active Directory. Referenced; document not provided in substrate. | auto-derived — verify |
| SQLI data classification policy | Internal policy defining classification labels and obligations. Referenced; document not provided in substrate. | auto-derived — verify |
| SQLI audit policy | Internal policy defining audit-record content, retention, and access. Referenced; document not provided in substrate. | auto-derived — verify |

## Functional Requirements

**FR-001** — The System SHALL manage data flows between heterogeneous subsystems including SaaS applications, the Data Platform, and company cloud-tenant databases or applications.

**FR-002** — WHEN a predefined schedule fires the System SHALL trigger the corresponding scheduled data pull.

**FR-003** — WHEN a scheduled or on-demand pull executes the System SHALL pull bulk data from the source subsystem into the single Landing Zone.

**FR-004** — The System SHALL store data in the Landing Zone in a subsystem-agnostic format consumable by any authorised subsystem.

**FR-005** — The System SHALL expose Landing Zone data such that each consuming subsystem accesses only the data required by its workflows.

**FR-006** — WHEN raw ingestion executes the Data Platform SHALL pull bulk data from the Landing Zone into raw storage.

**FR-007** — The Data Platform SHALL transform raw data into business-ready, standardised datasets.

**FR-008** — The Data Platform SHALL expose business-ready, standardised data for direct consumption by authorised subsystems.

**FR-009** — WHEN an authorised operator submits a manual pull request the System SHALL execute the requested pull on demand.

**FR-010** — WHEN a producing subsystem initiates a push event (state change or compliance event) the System SHALL accept the pushed data into the Landing Zone.

**FR-011** — The Landing Zone SHALL retain data for 7 days from ingestion.

**FR-012** — WHEN data in the Landing Zone exceeds 7 days from ingestion the System SHALL automatically erase it.

**FR-013** — The System SHALL support structured, semi-structured, and unstructured data.

**FR-014** — The Data Platform SHALL expose all data required for business workflows.

**FR-015** — The Data Platform SHALL allow authorised external end-users to consume data.

**FR-016** — The System SHALL orchestrate and supervise the execution of all data pulls.

**FR-017** — The Data Platform SHALL govern all enterprise data through its catalogue.

> ⚠️ FR-005 and FR-010 reformulated: substrate phrases consumer/producer behavior; FR scope is the System's behavior. Statements rewritten as System-side capability obligations.

> ⚠️ FR-008 and FR-014: substrate notes "use cases to be defined in the future" — exposure obligation is rendered; the consumer-side use-case enumeration is deferred.

> ⚠️ FR-011 / FR-012 split from substrate F11 (compound: retain + automatically erase).

## Interface Requirements

### Inbound (IR-IN)

**IR-IN-001** — The System MUST accept bulk data pulls from source subsystems (SaaS applications and company cloud-tenant databases or applications) into the Landing Zone.

**IR-IN-002** — WHEN a producing subsystem initiates a push (state change or compliance event) the System SHALL accept the inbound payload into the Landing Zone.

**IR-IN-003** — The System MUST accept user identity assertions from Active Directory for platform access decisions.

**IR-IN-004** — WHEN an authorised operator submits a manual pull request the System SHALL accept the request through an operator-facing interface.

### Outbound (IR-OUT)

**IR-OUT-001** — The Data Platform MUST expose Landing Zone data to authorised subsystems in a subsystem-agnostic format.

**IR-OUT-002** — The Data Platform MUST expose business-ready, standardised data to authorised consuming subsystems.

**IR-OUT-003** — The Data Platform MUST expose data to authorised external end-users.

**IR-OUT-004** — The System MUST expose observability signals (data flow events, production/consumption traces, usage and cost telemetry, audit records) to authorised monitoring consumers.

> ⚠️ Substrate provides no protocol, schema, or format specification for any interface — IR statements describe obligation only; concrete contracts are deferred to design phase.

## Data Requirements

### Data Requirements (DR)

N/A

> ⚠️ Substrate provides no field-level data model (no schema, no field constraints, no entity definitions beyond glossary descriptions). DR section deferred.

### Transformation Requirements (TR)

N/A

> ⚠️ Substrate references the existence of "transformation into business-ready, standardised datasets" (F7) but specifies no input → rule → output mapping. TR section deferred.

## Non-Functional Requirements

**NFR-001** — The System MUST automatically retry failed data pulls in accordance with a defined retry policy. | Measurement: TBD — retry count and back-off interval to be defined.

**NFR-002** — The System SHOULD route records that fail after retry exhaustion to a dead-letter store. | Measurement: TBD.

**NFR-003** — Inter-subsystem interactions MUST have no single point of failure. | Measurement: TBD — target availability percentage to be defined.

**NFR-004** — The System SHOULD meet defined SLA targets for availability, latency, and freshness. | Measurement: TBD with Business Users in design phase.

**NFR-005** — The System SHOULD meet defined data freshness and latency SLOs. | Measurement: TBD with Business Users in design phase.

**NFR-006** — The System MUST support at least 50 pulls per day. | Measurement: ≥ 50 pulls per 24-hour window.

**NFR-007** — The System MUST support pull payloads up to 10 MB. | Measurement: payload size ≤ 10 MB per pull.

**NFR-008** — The System MUST support ingestion from at least 10 distinct source subsystems. | Measurement: ≥ 10 source subsystems concurrently registered for ingestion.

> ⚠️ NFR-001..NFR-005 carry `Measurement: TBD` — substrate explicitly defers the quantitative threshold. Bounded scoring is ✗ until threshold is defined.

## Security

**SEC-001** — The Data Platform MUST enforce access control at data-asset level in compliance with RGPD and SQLI data access policy.

**SEC-002** — The System MUST enforce access control to the Data Platform via Active Directory in compliance with SQLI user access policy.

**SEC-003** — Data in transit crossing external trust boundaries MUST be encrypted.

**SEC-004** — IF an observability output would expose data classified as sensitive in violation of SQLI data security policy THEN the System SHALL redact or suppress that output. → ERR-002

## Constraints

**CON-001** — The System SHALL retain data beyond the Landing Zone in compliance with SQLI data retention policy.

**CON-002** — The System SHALL ensure each data asset is produced by exactly one subsystem, with all other subsystems acting as consumers of that asset.

**CON-003** — The System SHALL ensure each data asset complies with exactly one data contract.

**CON-004** — The Data Platform SHALL own all data contracts.

**CON-005** — The System SHALL assign accountability for data quality explicitly per data asset.

**CON-006** — The System SHALL ensure data classification complies with SQLI data classification policy.

**CON-007** — The System SHALL comply with GDPR and SQLI data security policy regarding retention, storage, RTO, and RPO.

## Error Handling

**ERR-001** — IF a scheduled or on-demand data pull fails THEN the System SHALL automatically retry per the defined retry policy. → FR-003

**ERR-002** — IF a record fails processing after retry exhaustion THEN the System SHALL route it to a dead-letter store for engineer inspection. → FR-006

> ⚠️ ERR-002 derives from substrate NFR2 ("Error handling & dead-letter: TBD"); the response action is rendered, the policy detail is deferred.

> ⚠️ Substrate defines no error paths for the majority of FRs (FR-001, FR-004..FR-005, FR-007..FR-017). Coverage is intentionally minimal at this maturity level; expand in design phase.

## Observability

**OBS-001** — The Data Platform MUST emit observability signals for incoming and outgoing data flows.

**OBS-002** — The System MUST record data production and consumption events with who, when, and where attributes.

**OBS-003** — The System MUST produce audit records compliant with SQLI audit policy.

**OBS-004** — The System MUST trace data usage and cost attribution per Unit and Department.

**OBS-005** — The System MUST emit observability signals for data exchanges that fall outside the Data Platform's observability scope.

## Acceptance Criteria

**FR-001**
- AC: For each pair of heterogeneous subsystems within the configured topology (SaaS, Data Platform, cloud-tenant), at least one managed data flow can be enumerated from the System's flow registry.

**FR-002**
- AC: Given a schedule entry due at time T, the System triggers the corresponding pull within the schedule's tolerance window of T.

**FR-003**
- AC: A scheduled or on-demand pull moves the source subsystem's bulk payload into the single Landing Zone, observable as a Landing Zone record with the expected record count.

**FR-004**
- AC: A Landing Zone object is readable by an authorised consumer using a generic reader (no source-subsystem-specific driver required).

**FR-005**
- AC: When consumer A and consumer B have distinct workflow scopes, a query by A returns only A's authorised slice of Landing Zone data, not B's.

**FR-006**
- AC: After raw ingestion runs, the raw storage layer contains a record set matching the corresponding Landing Zone object's records.

**FR-007**
- AC: Given a raw dataset, the Data Platform produces a business-ready dataset whose schema, naming, and units conform to the standardised target.

**FR-008**
- AC: An authorised consuming subsystem can read business-ready datasets directly from the Data Platform's serving interface.
- AC: N/A for downstream use-case completeness — substrate defers use-case enumeration.

**FR-009**
- AC: When an authorised operator submits a manual pull request, a corresponding pull execution is recorded and completes (or fails and is logged).

**FR-010**
- AC: When a producing subsystem pushes a payload tagged as state change or compliance event, the payload appears in the Landing Zone within the inbound channel's defined acceptance window.

**FR-011**
- AC: A Landing Zone record ingested at time T is readable for at least 7 × 24 hours after T.

**FR-012**
- AC: A Landing Zone record ingested at time T is no longer readable after T + 7 days; an erasure event is recorded.

**FR-013**
- AC: The System ingests at least one structured, one semi-structured, and one unstructured payload without rejection.

**FR-014**
- AC: For each business workflow registered in the catalogue, the data assets it consumes are exposed by the Data Platform.
- AC: N/A for completeness — substrate defers use-case enumeration.

**FR-015**
- AC: An authorised external end-user authenticated per policy can read the data assets entitled to them.

**FR-016**
- AC: For every data pull, an orchestration record (start, end, outcome) is present in the supervision log.

**FR-017**
- AC: For every data asset persisted in the Data Platform, a catalogue entry exists with owner, contract, and classification.

**IR-IN-001**
- AC: The Landing Zone receives bulk pulls from at least one SaaS source and at least one cloud-tenant source via the inbound interface.

**IR-IN-002**
- AC: A push from a producing subsystem identified as a state-change/compliance event is accepted and persisted in the Landing Zone.

**IR-IN-003**
- AC: A platform login presents an Active Directory identity assertion; the System grants or denies based on AD-resolved group membership.

**IR-IN-004**
- AC: An operator-facing interface accepts a manual pull request and produces a request identifier for traceability.

**IR-OUT-001**
- AC: An authorised subsystem can read Landing Zone data via the outbound interface using the agreed subsystem-agnostic format.

**IR-OUT-002**
- AC: An authorised consuming subsystem can read business-ready datasets via the platform's serving interface.

**IR-OUT-003**
- AC: An authorised external end-user can read data via the externally exposed interface.

**IR-OUT-004**
- AC: A monitoring consumer subscribed to the observability channel receives flow, usage, cost, and audit signals.

**NFR-001**
- AC: A failed pull is automatically retried until the retry policy's stop condition is met. Quantitative thresholds: TBD.

**NFR-002**
- AC: After retry exhaustion, the failed record is present in the dead-letter store and absent from the live processing path.

**NFR-003**
- AC: Each inter-subsystem interaction path can be traced to at least two redundant components or paths in the deployment diagram. Quantitative availability target: TBD.

**NFR-004**
- AC: SLA dashboard reports availability, latency, and freshness against agreed targets. Targets: TBD.

**NFR-005**
- AC: Freshness and latency SLOs are reported per dataset against agreed targets. Targets: TBD.

**NFR-006**
- AC: A 24-hour test window completes ≥ 50 pulls without capacity-related failures.

**NFR-007**
- AC: A pull with a 10 MB payload completes successfully; a pull with > 10 MB is handled per the documented payload-size policy.

**NFR-008**
- AC: At least 10 distinct source subsystems are registered concurrently in the ingestion catalogue and execute pulls within a 24-hour window.

**SEC-001**
- AC: A request to read a data asset is granted only to subjects whose RGPD/SQLI-data-access-policy entitlement covers that asset; denials are logged.

**SEC-002**
- AC: A login bypassing Active Directory is rejected; an AD-authenticated session is granted scoped per SQLI user access policy.

**SEC-003**
- AC: A network capture across an external trust boundary shows ciphertext only; an attempted cleartext flow is blocked.

**SEC-004**
- AC: An observability event whose payload would include data classified as sensitive in violation of policy is emitted with the sensitive content redacted or is suppressed.

**CON-001**
- AC: Audit reports show that data retained beyond the Landing Zone respects SQLI retention rules per data class.

**CON-002**
- AC: For any data asset, exactly one subsystem appears as producer in the catalogue; all other subsystems with access appear as consumers.

**CON-003**
- AC: For any data asset, exactly one active data contract is referenced in the catalogue.

**CON-004**
- AC: Every data contract record's owner field resolves to the Data Platform team.

**CON-005**
- AC: Every data asset has a non-empty quality-accountability field in the catalogue.

**CON-006**
- AC: Every data asset has a classification label drawn from the SQLI classification taxonomy.

**CON-007**
- AC: Independent compliance review confirms GDPR and SQLI data security policy conformance for retention, storage, RTO, and RPO.

**ERR-001**
- AC: A failure injected into a pull triggers automatic retry events; pull either succeeds within retry budget or is recorded as terminal failure.

**ERR-002**
- AC: A record forced through retry exhaustion is found in the dead-letter store with sufficient diagnostic context.

**OBS-001**
- AC: Inbound and outbound data flow events are present in the observability stream during a controlled traffic test.

**OBS-002**
- AC: Each production and consumption event in the observability stream carries identity, timestamp, and source/destination attributes.

**OBS-003**
- AC: Audit records produced during a controlled exercise pass review against SQLI audit policy criteria.

**OBS-004**
- AC: Usage and cost dashboards attribute spend and traffic to the originating Unit and Department.

**OBS-005**
- AC: Data exchanges configured outside the Data Platform observability scope are nonetheless visible through the System-level observability stream.

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
| FR-001     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-002     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-003     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-004     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-005     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-006     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-007     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-008     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-009     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-010     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-011     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-012     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-013     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-014     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-015     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-016     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-017     |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-001  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-002  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-003  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-004  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-001 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-002 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-003 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-004 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| NFR-001    |   ✓    |      ✓      |     ✓      |     ✓     |    ✗    |
| NFR-002    |   ✓    |      ✓      |     ✓      |     ✓     |    ✗    |
| NFR-003    |   ✓    |      ✓      |     ✓      |     ✓     |    ✗    |
| NFR-004    |   ✓    |      ✓      |     ✓      |     ✓     |    ✗    |
| NFR-005    |   ✓    |      ✓      |     ✓      |     ✓     |    ✗    |
| NFR-006    |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
| NFR-007    |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
| NFR-008    |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
| SEC-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| SEC-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| SEC-003    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| SEC-004    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-003    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-004    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-005    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-006    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-007    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| OBS-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| OBS-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| OBS-003    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| OBS-004    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| OBS-005    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-07 |
| Status       | Draft      |
