# ADR-010 — Middleware and O2 boundary: canonical SQLI data contracts, one-way inbound

| Field | Value |
|:------|:------|
| Date | 2026-07-17 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Arnaud, Cyril, Pascal, Chirojean, Gilles |
| Consolidates | [2026-07-16-middleware-o2-boundary-decisions.md](2026-07-16-middleware-o2-boundary-decisions.md) |

---

## Context

The SQLI middleware, an IT-owned extractor, feeds the O2 Databricks platform, owned by the Transformation team. The two are separate systems with separate owners, so the split of responsibility across the boundary has to be agreed and recorded. This ADR consolidates the 16 July boundary decision sheet and the 16 July Middleware x Databricks workshop into one record.

Scope is the middleware-to-O2 boundary, one way, inbound. The behaviours any middleware needs to run are assumed and not restated here: idempotence, retry, dead letter queue, logging, and authentication to the SaaS through a vault.

The workshop notes are AI-generated and to be verified. This ADR keeps only what is consistent with the decision sheet and the platform ADRs.

---

## Rationale

The key principles of the boundary, foundational first. Every decision below is consistent with these.

1. **One-way inbound, Databricks holds the truth.** Data flows one way, from the SaaS through the middleware into O2. O2 is the source of truth, and teams consume it as governed gold data through agents, not by writing back into the SaaS. This follows the medallion ownership already set for the platform: raw data per producer in bronze, cross-source cleaned and conformed in silver, business-ready views in gold (ADR-001).

2. **Two contracts, flow-down.** The boundary runs through two contracts. The SaaS-to-middleware contract sets what each source provides. The middleware-to-O2 contract sets what the middleware delivers to O2. Obligations flow down from the first to the second, so O2 never receives a stronger guarantee than the source itself gives.

3. **Canonical SQLI data contracts, subscription.** The middleware lands canonical SQLI data contracts, that is, data shaped to a format defined by SQLI, not to any SaaS proprietary format. Defining the format on the SQLI side is what keeps the platform independent of any single tool, so a tool can be swapped without reworking downstream. O2 subscribes to these contracts, and a SaaS subscribes when a use case requires it, so segmentation and distribution are optimised and each subscriber takes only what it needs.

4. **Batch landing, phased, stateless middleware.** Today the middleware lands files from a SharePoint library into bronze in scheduled batches, the implemented pattern (ADR-009), with a later move to ADLS Gen2 (ADR-008) that changes only how O2 reads, not what the middleware writes. The middleware holds no data of its own, the landing zone holds the data in transit.

5. **Demand-driven change.** Business use cases drive the requirements. A use case sets what the SaaS must provide, which sets the contract. The middleware changes only when the solutioning requires it, never speculatively.

6. **Technical segmentation only.** The middleware segments data to each subscriber's technical need, with no business rules. Business logic lives in silver.

7. **Compliance by design.** Security and data-protection rules live in the contracts and are checked by a conformance test on each side, so compliance holds by design. Personal data is filtered at the middleware, encryption and anonymisation happen before landing, and sensitive data such as bank details is excluded from the middleware except one isolated encrypted flow for a specific business case.

8. **Delta by design.** Whether a source sends all its data or only what changed is fixed per source in the contract. The middleware provides the delta when the source cannot, and silver reconciles the result.

9. **Id bridging lives in the middleware.** In the rare case where a use case must relate two SaaS records by their keys and no business field links them, the middleware carries an internal SQLI id to bridge them. O2 could have held that link instead, as a derived link in silver or a Lakebase table, but the bridge is a technical relationship with no business meaning, so it stays with the middleware.

---

## Decision

1. The middleware lands canonical SQLI data contracts as JSON batch files. O2 subscribes to them, and a SaaS subscribes when a use case requires it.
2. Each record lands as one VARIANT value and bronze keeps it raw. File names are unique, guaranteed by the middleware, which also removes the files once they are read.
3. Technical clean-up and validation happen at the middleware edge. Business clean-up, deduplication and conforming happen in silver.
4. Segmentation is technical only, shaped to each subscriber's need, with no business rules.
5. The extraction mode, all the data or only what changed, is fixed per source in the SaaS-to-middleware contract. The middleware provides the delta when the source cannot, and silver reconciles.
6. Personal data is filtered at the middleware, encryption and anonymisation happen before landing, and sensitive data is excluded except one isolated encrypted flow. Each side is tested against its contract, and both contracts are versioned and change only through the two-team control.
7. Cadence is set on both sides to meet the freshness SLO defined per O2 use case with the business.

---

## Consequences

- The middleware-to-O2 contract is the versioned artefact that binds IT and the Transformation team. Its detailed specification (file shape, naming rule, retention, and handling of oversized or malformed records) lives in the contract, not in this ADR.
- O2 gets one clean canonical view per subject, independent of SaaS formats, so a SaaS can be swapped without reworking O2.
- Because O2 never gets a stronger guarantee than the source, a gap in a SaaS surfaces as a contract limit, not as a silent data problem.
- Compliance is provable, each side's conformance test must pass before it goes live.

---

## Deferred

- **Event bus.** Revisit when a use case needs the middleware to send a command that a SaaS must act on reliably, for example a state change that must trigger an action.
- **Volumes.** Adequate at the current company size. Revisit on material growth of a source, or a new high-volume source.
- **Write-back.** O2 does not push data back into the SaaS tools. Keep it possible for a future use case.

---

## Validation

Every decision traces to a principle in the Rationale, none stands outside it. The two contracts and their conformance tests exist and pass before the SharePoint phase goes live. The unverified SharePoint read combination noted in ADR-009 passes its one-file test before that phase relies on this boundary.

---

## Sources

- Middleware x Databricks workshop, 16 July 2026, notes (AI-generated, to be verified).
- ADR-001 medallion layer ownership.
- ADR-009 SharePoint to bronze ingestion, ADR-008 ADLS to bronze ingestion.

---

| Field | Value |
|:------|:------|
| Version | 1.6 (draft) |
| Last Updated | 2026-07-17 |
