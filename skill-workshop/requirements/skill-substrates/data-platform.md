# SQLI – Data Platform Creation

---

# System & Containers level

## Functional

| # | Category | statement |
| --- | --- | --- |
| F1 | Data flow & integration | The System manages data flows between heterogeneous subsystems. Subsystems include SaaS applications, the Data Platform, and company cloud-tenant databases or applications. |
| F2 | Data flow & integration | Scheduled data pulls are triggered according to a predefined schedule. |
| F3 | Data flow & integration | The System pulls bulk data from source subsystems into a single Landing Zone. |
| F4 | Data flow & integration | Data in the Landing Zone is stored in a subsystem-agnostic format consumable by any authorised subsystem. |
| F5 | Data flow & integration | Consuming subsystems pull from the Landing Zone only the data required by their workflows. |
| F6 | Data flow & integration | The Data Platform pulls bulk data from the Landing Zone for raw ingestion. |
| F7 | Data flow & integration | The Data Platform transforms raw data into business-ready, standardised datasets. |
| F8 | Data flow & integration | Subsystems consume business-ready, standardised data directly from the Data Platform (use cases to be defined in the future). |
| F9 | Data flow & integration | Authorised operators can manually trigger pull actions on demand. |
| F10 | Data flow & integration | Producing subsystems can push data in the Landing Zone the Data when required (state changes, security compliance, TBC in design phase). |
| F11 | Data lifecycle | The Landing Zone retains data for 7 days, after which it is automatically erased. |
| F12 | Data lifecycle | Retention beyond the Landing Zone complies with SQLI data retention policy. |
| F13 | Data ownership & contracts | Each data asset is produced by exactly one subsystem; all others may only consume it. |
| F14 | Data ownership & contracts | Each data asset complies with one and only one data contract. |
| F15 | Data ownership & contracts | Data contracts are owned by the Data Platform. |
| F16 | Data ownership & contracts | Data may be structured, semi-structured, or unstructured. |
| F17 | Data ownership & contracts | The Data Platform exposes all data required for business workflows (use cases to be defined in the future). |
| F18 | Data ownership & contracts | Accountability for data quality is explicitly assigned per data asset. |
| F19 | Data ownership & contracts | Data classification complies with SQLI policy. |
| F20 | Consumption | Data may be consumed by authorized external end-users. |

## Governance & Access

| # | Category | statement |
| --- | --- | --- |
| G1 | Governance & access | The System orchestrates and supervises the execution of all data pulls. |
| G2 | Governance & access | The Data Platform governs all enterprise data through its catalogue. |
| G3 | Governance & access | The Data Platform enforces access control at data-asset level according to RGPD and SQLI data access policy. |
| G4 | Governance & access | The System enforces access control to the Data Platform according to SQLI user access policy (through Active Directory). |

## Observability Requirements

| # | Category | statement |
| --- | --- | --- |
| O1 | Observability | The Data Platform manages observability of incoming and outcoming data. |
| O2 | Observability | Data production and consumption are traceable (who, when, where). |
| O3 | Observability | Auditability complies with SQLI policy. |
| O4 | Observability | Data usage and costs are traceable per Unit & Departement. |
| O5 | Observability | The System manages observalibility of data exchanges not in Data Platform observability scope. |
| O6 | Observability | System observality prevents from data leakage according to SQLI data security policy. |

## Non-Functional

| # | Category | statement |
| --- | --- | --- |
| NFR1 | Reliability | On pull failure the System automatically retries according to a defined retry policy (policy **TBD**). |
| NFR2 | Reliability | Error handling & dead-letter: **TBD**. |
| NFR3 | Availability | Inter-subsystem interactions shall have no single point of failure. |
| NFR4 | Security | Data in transit crossing external trust boundaries must be encrypted. |
| NFR5 | Compliance | The System complies with GDPR and SQLI data security policy (e.g. retention, storage, RTO, RPO). |
| NFR6 | SLA | SLA targets (availability, latency, freshness): **TBD** with Business Users in design phase. |
| NFR7 | SLA | Data freshness / latency SLOs: **TBD** with Business Users in design phase. |
| NFR8 | Performance & scalability | The System supports at least 50 scheduled pulls / pulls per day. |
| NFR9 | Performance & scalability | The System supports payloads of up to 10 MB per pull. |
| NFR10 | Performance & scalability | The System supports ingestion from at least 10 distinct source subsystems. |

# Glossary

| Term | Definition |
| --- | --- |
| Access control | The rules that decide who can see or use each piece of data — like the badges that decide which rooms an employee can enter. |
| Active Directory | Microsoft's central directory of company users, their passwords, and the groups they belong to. Other tools rely on it to know who someone is and what they're allowed to do. |
| Auditability | The ability to reconstruct, after the fact, who did what with which data and when. Required for legal and compliance checks. |
| Bulk data | A large batch of records moved together in one go (e.g. all of yesterday's orders), as opposed to one record at a time. |
| C4 (model) | A standard way of drawing software architecture diagrams in four zoom levels: System, Container, Component, Code. "C4-friendly" requirements stay at the top zoom levels and avoid implementation detail. |
| Cloud tenant | The company's own private space inside a public cloud provider (Azure, AWS, GCP). Other companies share the same cloud but cannot see or touch what's in another tenant. |
| Data asset | A distinct, named piece of data treated as a managed object — e.g. "customer master list", "monthly sales report". Has an owner, a contract, and a quality level. |
| Data catalogue | An indexed inventory of all the data the company holds. Like a library catalogue: it lets users find what data exists, where it lives, and who owns it. |
| Data classification | Labelling data by sensitivity (public, internal, confidential, personal). The label determines who can access it and how it must be protected. |
| Data contract | A written agreement between a data producer and its consumers, describing the format, fields, freshness, and quality the producer guarantees. Like a supplier specification sheet. |
| Data flow | The movement of data from one system to another along a defined path. |
| Data in transit | Data while it is moving across a network (vs. *data at rest*, which sits in storage). |
| Data leakage | Data ending up where it should not be (wrong recipient, public website, unauthorised system). Usually accidental but always a security incident. |
| Data Platform | The central system where the company stores, organises, and serves data for analytics, reporting, and downstream applications. |
| Dead-letter | A holding area for messages or records that failed to process and could not be retried. Lets engineers inspect failures rather than lose them silently. |
| Encryption | Scrambling data with a key so that anyone intercepting it cannot read it without the key. |
| GDPR / RGPD | The European regulation on personal data protection. RGPD is the French acronym for the same law. |
| Heterogeneous (subsystems) | Subsystems built on different technologies that don't naturally speak the same language and therefore need translation to exchange data. |
| Landing Zone | A temporary storage area where raw incoming data is dropped first, before being cleaned, transformed, or used downstream. Like a goods-receiving dock. |
| Latency | The delay between when something is requested and when the answer arrives. Lower is better. |
| Observability | The ability to see, from the outside, what a system is doing — what's flowing through it, what's failing, how fast, how often. Combines logs, metrics, and traces. |
| Payload | The actual content carried in a single transfer (the file or the records), excluding the technical envelope around it. |
| Pull (vs Push) | *Pull*: the destination system asks for the data. *Push*: the source system sends the data without being asked. Scheduled transfers usually pull; real-time event notifications usually push. |
| Raw ingestion | Loading data into the platform exactly as it arrived, with no cleaning or transformation, so the original is preserved. |
| Retention (policy) | The rule for how long data is kept before being automatically deleted (e.g. "the Landing Zone keeps data 7 days"). |
| Retry policy | The rule for how many times, and how often, the system should automatically try again when an action fails. |
| RPO (Recovery Point Objective) | Maximum acceptable amount of recent data lost in a failure, measured in time. "RPO = 1 hour" means losing up to 1 hour of recent data is tolerable. |
| RTO (Recovery Time Objective) | Maximum acceptable downtime after a failure. "RTO = 4 hours" means the system must be back within 4 hours. |
| SaaS (Software as a Service) | Software hosted by a vendor and accessed over the internet (e.g. Salesforce, Workday). The customer does not install or maintain it. |
| Scheduled pull | A data transfer that runs automatically at a fixed time or interval (e.g. every night at 2am). |
| Single point of failure | A component whose breakdown brings the whole system down because there is no backup. A design flaw to be avoided. |
| SLA (Service Level Agreement) | A formal commitment to a level of service (e.g. availability, response time), with contractual or financial consequences if missed. |
| SLO (Service Level Objective) | The internal target a team aims for — usually stricter than the SLA, to leave a safety margin. |
| Standardised data | Data reshaped to a common format, naming, and unit convention so different downstream uses can consume it the same way. |
| Structured data | Data that fits cleanly in tables with defined columns (spreadsheets, relational databases). |
| Semi-structured data | Data that has some structure but stays flexible (JSON, XML). |
| Unstructured data | Data with no predefined structure (PDFs, emails, images, audio). |
| Subsystem | A self-contained part of the wider system, with its own job and boundary (e.g. a CRM application, the data warehouse). |
| Subsystem-agnostic format | A storage format chosen so that no single subsystem's technology is required to read it — any authorised subsystem can consume it. |
| Trust boundary | The line between two zones with different security rules (e.g. inside the company network vs. the public internet). Crossing one usually requires extra protection like encryption or authentication. |
