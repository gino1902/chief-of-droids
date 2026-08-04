# ADR-010 — Middleware and O2 boundary: canonical SQLI data contracts, one-way inbound

| Field | Value |
|:------|:------|
| Date | 2026-07-17 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Arnaud, Cyril, Pascal, Chirojean, Gilles |
| Consolidates | [2026-07-16-middleware-o2-boundary-decisions.md](2026-07-16-middleware-o2-boundary-decisions.md) |
| Amended | 2026-08-04, see [Amendment](#amendment-2026-08-04) before relying on principle 3 or decision 1 |

> ⚠️ Read the amendment first. Principle 3 and decision 1 are written in the present
> tense and describe an agreed target that is deferred, not the current state.

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

## Amendment 2026-08-04

> ⚠️ Amendment proposed, not agreed. The decisions above were taken on 16 July by five
> named decision-makers. Nothing in this section reverses or edits them. It records a fact
> discovered on 2026-08-04 that contradicts the present tense of principle 3 and decision 1,
> and leaves the revision to the five.

Source: [data-sources discovery note](../2607-o2-requirements/2026-08-04-data-sources-discovery-note.md).

### What was discovered

Payloads are specified by the IS team, per file, per source application. Middleware
implements that specification and delivers. Canonicalisation across source applications is
deferred until further notice, and the cause is that no owner exists for a
cross-application model, not middleware capacity.

Principle 3 and decision 1 therefore describe an agreed target in a state of deferral, not
the current state. Read them as deferred.

Two senses of canonical, kept distinct because they were being conflated:

| Sense | In scope of ADR-010 | State |
|:------|:--------------------|:------|
| Data shaped to a SQLI-defined format rather than a SaaS proprietary format, for tool independence | Yes, this is principle 3's intent | Deferred |
| Cross-application enterprise semantics, one agreed meaning per business concept | No, never in scope here | Deferred, and no owner exists |

The second sense lands in silver by ADR-001, which remains correct. The consequence is that
O2's silver definitions become the company's de facto enterprise model, held by a team with
no mandate to define company semantics.

### Open questions raised, not answered

| # | Question | Why it matters |
|:--|:---------|:---------------|
| A1 | Does the personal-data filtering and anonymisation in decision 6 destroy the IS user identifier | That identifier is the only candidate join key across APP and Whoz, and it is personal data. If the middleware strips or anonymises it, no cross-source person entity is buildable by any route |
| A2 | Does principle 9 extend to person identity, or is person identity a business entity outside its scope | Both premises behind principle 9 are unsettled for this case. See "On A2" below. Recorded as AD-2 in the discovery note |
| A3 | Decision 2 states the middleware removes files once read. ADR-009's standing checks require manual source cleanup because `cleanSource` is unsupported | The two may describe different actors, but as written they read as conflicting. Verify before the SharePoint phase goes live |

### On A2

What is established: no business field links an APP record and a Whoz record for the same
person. The only candidate is an IS user identifier, and whether that identifier is present
in both payloads is itself unverified until a sample is read.

Principle 9 rests on two premises. Neither is settled for this case, and the ADR should not
be read as having ruled on person identity.

| Premise | Evidence state | What would settle it |
|:--------|:---------------|:---------------------|
| The case is rare | Unknown. One candidate use case needs a cross-producer person, and demand has not been counted in either direction. One instance neither proves nor disproves rare | Count, across the use-case pipeline, how many candidate use cases must relate records from two producers where no business field links them. A brief's placement and solution sketch already reveal this, so demand becomes countable as briefs accumulate |
| The bridge is a technical relationship with no business meaning | Contested judgement, not a fact. Arguable in both directions for an identity spanning payroll, staffing and delivery | A ruling by whoever owns the definition. That owner is itself an open item |

Because neither premise is settled, principle 9 is neither confirmed nor contradicted here.
What can be decided now is an interim rule that prejudges none of the three options in AD-2:

No cross-source person entity is built until A1 is answered and demand has been counted
across several briefs. Until then use cases stay within a single producer, and
`key_strategy` on any person entity reads blocked, naming both reasons. Leaving the interim
rule unstated is the failure mode, because delivery work would settle the question by
accident.

### Revalidation

The deferral has no date. Re-test at each ADR review: ask IS whether an owner for the
cross-application model has been appointed. Appointment is the trigger to revise principle 3
from deferred back to active, and to revisit whether conforming stays in silver.

---

## Sources

- Middleware x Databricks workshop, 16 July 2026, notes (AI-generated, to be verified).
- ADR-001 medallion layer ownership.
- ADR-009 SharePoint to bronze ingestion, ADR-008 ADLS to bronze ingestion.
- Data-sources discovery note, 4 August 2026 (amendment only).

---

| Field | Value |
|:------|:------|
| Version | 1.7 (draft) |
| Last Updated | 2026-08-04 |
