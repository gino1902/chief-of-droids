# Middleware and O2 boundary decisions

Prep sheet for the workshop on who does what between the SQLI middleware and the Databricks O2 platform.

## Workshop summary

Intent. Decide where the line sits between the middleware, the extractor owned by IT, and the O2 Databricks platform, owned by the Transformation team. This prepares a workshop with the IS head, the middleware architect and the Databricks architect. We answer one thing, which side does each job. We start from the SharePoint phase (ADR-009), live now, and treat the ADLS phase (ADR-008) as the next step.

Expected output. A short list of decisions the three architects can settle in the room. One question each. Each one says what the ADRs and Databricks practice already suggest, so the room just confirms it or changes it.

The base line. The middleware brings data in and drops it in the landing zone. Databricks takes over from there, it stores, cleans, joins and serves the data. Data flows one way, in. Databricks holds the truth.

Two contracts. The boundary runs through two contracts, linked by a flow-down principle.
- SaaS-to-middleware contract. Between the SaaS source and the middleware. Sets what the source sends, format, fields, sensitive data, and whether it sends all the data or only what changed.
- Middleware-to-O2 contract. Between the middleware and O2. Sets what the middleware drops in the landing zone.
- Flow-down. What the middleware commits to O2 comes from what the SaaS commits to the middleware. Terms flow down from the upstream contract to the downstream one, so O2 never gets a stronger guarantee than the source gives. IT owns both. The middleware-to-O2 contract is the one shared with the Transformation team, and neither side changes it without the other.

Write-back. O2 does not push data back into the SaaS tools. Consumption happens through agents reading gold. Keep write-back possible for a future need, but do not design for it now.

Scope note. The middleware is built by IT, outside the O2 project, but O2 depends on it, so the split has to be agreed. This sheet is an agreement between two teams, not an O2 internal design.

Out of scope, taken as given. What any middleware needs to run, idempotence, retry, dead letter queue, logging, error handling, and SaaS authentication via the vault. These are the middleware's by default.

## How to read each point

Each point has the same parts. Status, the question, why it matters, and what is already set. Point 4 adds a short note where the classic middleware idea and Databricks practice disagree.

## Order to take them in the room

Work through them in this order.

1. Point 1, the middleware-to-O2 contract.
2. Points 2 and 5, changed data and freshness.
3. Point 3, compliance and the contracts.
4. Point 4, do we need an event bus.

Point 6 (volumes) is deferred at the current company size, so it is not on the agenda.

## Facts to bring to the workshop

These decide the open points and are not ours to invent.

- The freshness SLO per O2 use case, agreed with the business. Feeds Point 5.
- Which fields in the SaaS sources are sensitive, so the contracts carry the rules. Feeds Point 3.
- Is there any command or state change that must be reliably acted on. Decides Point 4.

---

## Point 1. Middleware-to-O2 contract

Status. Set by the SharePoint-to-bronze pattern and the batch design. The remaining details are written into the contract, not decided in the room.

Question. In the SharePoint phase, this is a batch design. What does the middleware drop in the landing zone each run: file format, file names, and who deletes the files once they are read.

Why it matters. This is the middleware-to-O2 contract, the downstream half, and its terms flow down from the SaaS-to-middleware contract. Databricks reads whatever the middleware leaves. If it does not match, records are lost or broken and no one notices. It ties two teams, so it has to be written down. And it lasts, because moving to ADLS later changes only how Databricks reads, not what the middleware writes.

Already set, to confirm.
- It is a batch design. The middleware sends JSON in batch files, each record as one VARIANT value, drained on schedule (ADR-009, Point 5). Bronze keeps it raw.
- The middleware does the technical clean-up before dropping the file. Right encoding, valid JSON, each record under 16 MB, agreed file shape. Bad or oversized records are caught here, not lost later.
- Business clean-up, removing duplicates, joining, standardising, happens in silver, not the middleware (ADR-001).
- Files are not deleted on their own, so someone has to clean them up.

---

## Point 2. Full data or only changes

Status. Set by design. Not an open fork.

Question. Does each source send all its data every cycle, or only what changed, and who reconciles it.

Why it matters. Sending all the data every cycle is heavier than sending only what changed. But it is not an architecture choice, because the middleware already does both and the platform absorbs the difference. Which one a source uses is fixed in the SaaS-to-middleware contract.

Already set, to confirm.
- The middleware already handles both, all the data or only the changes. Which one per source is written into the SaaS-to-middleware contract, not chosen at runtime.
- Once that contract sets it for a source, it does not change, except through its change control.
- What lands in O2 is the same either way, per the middleware-to-O2 contract. Bronze keeps every record as VARIANT.
- Silver reconciles it, adding new records, updating changed ones, or removing duplicates, per entity. Silver already owns this (ADR-001), so it fits.

---

## Point 3. Compliance and the contracts

Status. Set by design, through the contract flow-down from SaaS. Not an open compliance debate.

Question. Where in the two contracts do the security and data-policy rules sit, and is each side tested against its contract.

Why it matters. Bronze stores records raw, so what is allowed to land has to be clear up front. But it is not decided record by record. Both contracts carry the company's security and data policies, and the rules flow down from the SaaS-to-middleware contract into the middleware-to-O2 contract. A test on each side checks conformance, so compliance is by design.

Already set, to confirm.
- Both contracts carry the security and data-policy rules. Policy flows down from the SaaS-to-middleware contract to the middleware-to-O2 contract.
- The middleware checks what it receives against the SaaS-to-middleware contract, at the edge.
- Databricks checks what lands against the middleware-to-O2 contract, at ingestion. Both are compliant by design.
- The split stays, technical and security checks at the middleware edge, data quality in silver (ADR-001).

Note. The security and data policies come from the company's policy owners. This sheet applies them, it does not set them.

---

## Point 4. Do we need an event bus

Status. Deferred. Revisit only when a use case needs a command reliably acted on by a SaaS.

Question. Is the file landing zone enough, or is a message bus needed.

Why it matters. The landing zone and a message bus do different jobs. Confusing them adds a component no one needs.

Already set, to confirm.
- The landing zone is a shared store, read by pull. Any other consumer can read the same store, so fan-out is by adding readers.
- A message bus does a different job. It is needed when commands must be processed with a reliable action, for example a state change that must be acted on.
- The middleware keeps no data of its own either way. The landing zone holds the data in transit.

Where the classic idea and Databricks differ. The classic middleware reaches for a message bus by default. Here the landing zone already covers data sharing by pull, so a bus is only for commands that must be acted on reliably, which O2 does not have today.

---

## Point 5. Data freshness

Status. Set by config and monitoring. Waiting only on the SLO per use case.

Question. How fresh does each use case's data need to be, and how is that kept.

Why it matters. Freshness is end to end, it depends on how often the middleware brings data in and how often Databricks loads it. Get it wrong and a use case works on stale data, or you pay for speed no one needs. But it is not a hard architectural choice, it is a schedule on each side plus a target to watch.

Already set, to confirm.
- How often the data refreshes is a schedule on both sides. The middleware schedules when it brings data in, Databricks schedules or triggers when it loads it.
- Freshness is an SLO per O2 use case, agreed with the business. It is an O2 requirement that flows down as the freshness target on the middleware. O2 monitoring alerts when the SLO is breached.
- Phase 1 refreshes a few times a day, because SharePoint cannot signal new files (ADR-009). Phase 2 on ADLS can load when new files arrive (ADR-008).

---

## Point 6. Volumes

Status. Deferred. At the current company size, volume is not a concern.

Why deferred. The landing zone holds a surge of data and serverless loads it with no idle cost, and at today's company size that is comfortably enough. Nothing to size and nothing to decide now.

Revisit when. A single source grows materially, or a new high-volume source arrives. Then set peak and surge figures and check the load keeps up. One record per file (Point 1) means many files, so watch the file count if that day comes.

---

## References

- ADR-001 medallion layer ownership, ADR-004 serverless compute, ADR-008 ADLS to bronze ingestion, ADR-009 SharePoint to bronze ingestion. This folder.
- FRAMING.md, O2 framing. `2607-o2-requirements`.
- Ingest data as semi-structured variant type, Azure Databricks. https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant
- Ingest files from SharePoint, Azure Databricks. https://learn.microsoft.com/en-us/azure/databricks/ingestion/sharepoint

<!--
Version: 1.0 | Last Updated: 2026-07-16 | Status: Draft
-->
