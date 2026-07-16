# Middleware and O2 boundary decisions

Preparatory decision sheet for the workshop on the responsibility split between the SQLI middleware and the O2 Databricks platform.

## Workshop summary

Intent. Fix the responsibility boundary between the SQLI middleware, the extractor, IT owned, and the O2 Databricks platform, Transformation team owned, before a working session with the IS head, the middleware architect and the Databricks architect. The question the workshop settles is which requirements each side carries, anchored on the implemented ADR-009 SharePoint phase first and the ADR-008 ADLS phase as the later evolution.

Expected output. A set of decisions the three architects can work through and close in the room. One question per point. Each point states where the accepted ADRs and current Databricks practice already point, so the room confirms or overturns a default rather than starting from blank.

Scope note. The middleware build is IT owned and outside the O2 project, but it is a strong upstream dependency, so the split has to be agreed. This sheet is a cross team boundary contract, not an internal O2 design.

Out of scope, treated as givens. The behaviours a middleware needs to function are not on the agenda. Idempotence, retry, dead letter queue, communication logging and error handling, and authentication to the SaaS via the vault. They belong to the middleware by definition.

## How to read each point

Point 0 is a statement of record, already decided. Every decision point after it carries the same fields. Status, the question, why it is a decision, the settled position to ratify, the open edges as options with an owner and a trade-off, what it depends on, who owns the call, and a recommendation.

## Recommended order in the room

Take them in dependency order, not in numeric order. Point 0 is decided and frames the rest, so the working session starts at Point 1.

1. Point 1, the inbound contract, the durable artefact.
2. Points 2 and 6, source delta and cadence, decided together.
3. Point 4, sanitisation and sensitive data, needs the data classification.
4. Point 5, decoupling and the bus scope question.
5. Point 3, outbound shaping.
6. Point 7, outbound routing.
7. Point 8, volume sizing, cuts across the rest.

## Facts to establish before the workshop

These gate the decisions and are not ours to invent. Bring them in.

- Does the SaaS source expose an incremental or changed since pull. Gates Point 2.
- A per flow freshness band, near real time, hourly, daily. Gates Point 6.
- A data classification of the SaaS sources, which fields are sensitive. Gates Point 4.
- Does the middleware serve consumers beyond O2. Gates Points 5 and 7.
- Peak and surge volume per source. Gates Point 8.

---

## Point 0. Ownership and dependency contract

Status. Decided. Statement of record, not a workshop decision.

Decision. IT owns and builds the middleware. The Transformation team owns O2. The boundary between them is a contract between the two teams, with a defined change control path in both directions. Neither side changes the shared contract without the other.

Why it is here. Every later point assigns work to the middleware or to Databricks, and that assignment rests on this ownership line. It is recorded here as the frame the rest hang on. It is settled, so the room applies it rather than re-opening it.

Consequence. The landing contract in Point 1 is the versioned artefact that binds the two teams, together with its outbound mirror in Point 3. Any change to either goes through the agreed change control. The middleware is a strong upstream dependency of O2, not a part of it.

---

## Point 1. Inbound landing contract

Status. Core settled by ADR-009, three open edges.

Question. In the ADR-009 SharePoint phase, what must the middleware deliver into the landing zone: format, record granularity, filenames, and who removes files after ingest.

Why it is a decision. Databricks ingests whatever the middleware leaves in the landing zone. A mismatch drops or corrupts records silently, and it binds two teams, so it has to be written down. It is also the durable part of the boundary, because the later move to ADLS changes only the Databricks read path, not the middleware write contract.

Settled position, to ratify.
- The middleware delivers JSON, one whole record as one VARIANT. Bronze stores it raw.
- Technical cleansing sits with the middleware, before landing. Encoding, well formed JSON, record size within a 16 MB ceiling, and the agreed file shape. Malformed or oversized records are caught at the edge, not lost at ingest.
- Business cleansing, deduplication, normalisation and conforming sit in silver (ADR-001). Bronze is not cleansed.
- Landed files are not removed automatically, so cleanup is an explicit obligation, not a default.

Open edges.

| Edge | Option | Owner | Trade-off |
|:--|:--|:--|:--|
| Record granularity | One record per file | middleware | Cleanest provenance and idempotency, most files |
| | Batched records per file | middleware | Fewer files, needs an agreed split key |
| Filename uniqueness | Middleware guarantees unique names | middleware | Matches the idempotent ingest requirement |
| | Content hash dedup in bronze | Databricks | Removes the middleware obligation, adds bronze cost |
| Post ingest cleanup | Middleware deletes after confirmed ingest | middleware | Files are not auto removed, so someone must |
| | Scheduled ops job on a retention window | shared | Simpler for the middleware, needs an owner and a window |

Depends on. Point 0 for the obligations that bind IT. The SaaS response shape, single record or paged, drives the granularity choice. This point gates Point 2 and Point 6.

Owner of the call. Middleware architect proposes the delivery shape. Databricks architect confirms it ingests cleanly. IS head ratifies the IT obligations, filename uniqueness and cleanup.

Recommendation.
- Confirm JSON, whole record to a single VARIANT, as the contract that holds across both phases.
- One record per file, middleware guaranteed unique filenames. Adds no bronze cost and matches idempotency.
- Technical cleansing and the 16 MB and valid JSON checks at the middleware edge. Business cleansing stays in silver.
- Assign post ingest cleanup to the middleware, or to a named ops job on an agreed retention window.

---

## Point 2. Source side delta

Status. Open, decided by one source fact, with a clear default either way.

Question. How does the middleware avoid re-pulling and re-landing the whole SaaS dataset every cycle, and does it hold any state to do so.

Why it is a decision. Full re-pulls cost source API load, transfer, and unbounded bronze growth. Holding delta state in the middleware breaks the stateless principle and adds a recovery burden if the middleware is rebuilt or replayed. Which way it goes depends on what the source can give, and that fact has to be established before the room can close it.

Settled position, to ratify.
- The middleware stays stateless by default. Idempotent landing means the same record delivered twice lands the same result, so re-delivery and replay are safe, see Point 1.
- Bronze is append only, so deduplication and change detection on a business key are a platform job, not a middleware job.

Open edges.

| Edge | Option | Owner | Trade-off |
|:--|:--|:--|:--|
| Source capability | SaaS exposes changed since or a watermark | middleware | Middleware lands only changes, stays stateless. Best case |
| | SaaS gives full snapshot only | — | Forces the branch below |
| If snapshot only | Land full snapshot, dedup on the platform | Databricks | Middleware stays stateless, higher transfer and bronze cost |
| | Middleware stores a watermark to compute delta | middleware | Less transfer, breaks stateless, adds state and recovery ownership |

Depends on. The source capability fact, does the SaaS API expose an incremental or changed since pull. Point 1 granularity. This point gates Point 6, since pull frequency and delta size trade against each other.

Owner of the call. Middleware architect establishes the source capability and proposes the extraction mode. Databricks architect confirms platform side dedup and change handling. IS head ratifies only if middleware state is introduced.

Recommendation.
- Establish the source delta capability first. It decides the branch, so it is the one fact to bring.
- If the source supports it, pull native delta and keep the middleware stateless.
- If it does not, land full snapshots and dedup on the platform, still stateless. Introduce middleware state only if snapshot volume makes transfer or bronze cost unacceptable, and treat that as a deliberate exception with a named owner, not the default.

---

## Point 3. Outbound shaping, gold to SaaS

Status. Open. No ADR covers the outbound path, so this is the widest ground in the sheet.

Question. Who turns gold into the format each target SaaS requires and pushes it, and does gold stay SaaS neutral or carry SaaS specific shapes.

Why it is a decision. Every ADR to date is inbound ingestion. The return path, gold back out to the SaaS tools, is unspecified, and it is where the middleware earns most of its keep. If SaaS specific shaping leaks into gold, gold fragments into one variant per target and drifts, which is the same divergence ADR-001 prevents on the inbound side. If it sits in the middleware, gold stays one clean product and the middleware absorbs each target's quirks.

Starting position, to confirm or overturn.
- Gold stays SaaS neutral, one business ready product per use case (ADR-001). The middleware does the SaaS specific mapping, format and delivery. This is the outbound anti corruption layer.
- Authentication to each SaaS sits with the middleware, via the vault. Given, not re-decided.
- One hard constraint. The platform cannot write back into the inbound SharePoint path, so outbound is never a mirror of Point 1. It needs its own handoff.

Open edges.

| Edge | Option | Owner | Trade-off |
|:--|:--|:--|:--|
| SaaS specific mapping | Middleware adapts gold per target | middleware | Gold stays clean, middleware carries the target quirks |
| | Per SaaS gold tables on the platform | Databricks | Simpler middleware, gold fragments and drifts per target |
| Outbound handoff | Middleware pulls from gold, query or extract | middleware | Platform stays serving only, middleware controls timing |
| | Platform writes an outbound extract to a shared drop | Databricks | Symmetric to Point 1, needs a drop location and a contract |
| Trigger | Middleware polls or runs on a schedule | middleware | Simple, adds latency |
| | Gold refresh signals the middleware | shared | Fresher, needs an event contract across the boundary |

Depends on. Point 0 for ownership of the return contract. Gold definitions per use case, still to be defined on the platform side. Shares the cadence decision with Point 6 and the unit sizing with Point 7.

Owner of the call. Databricks architect fixes what gold exposes and how it is reached. Middleware architect owns the mapping to each SaaS and the delivery. IS head ratifies the return contract, the mirror of Point 0.

Recommendation.
- Keep gold SaaS neutral. Put all SaaS specific shaping, format and delivery in the middleware, as the outbound adapter.
- Make the middleware pull from gold rather than have the platform push. It keeps the platform serving only and gives the middleware control of outbound timing.
- Write a return handoff contract now, even a thin one, so outbound is not improvised at build time. It is the reverse of Point 1 and deserves the same rigour.
- Keep authentication and the vault with the middleware.

---

## Point 4. Edge sanitisation versus data quality in silver

Status. The split principle is settled in Point 1. One genuinely open decision remains, sensitive data handling before landing.

Question. What must the middleware sanitise and validate at the edge before landing, and specifically must sensitive or personal data be stripped or masked before it reaches bronze.

Why it is a decision. Bronze stores the whole record raw as VARIANT, so anything that must not live in the platform has to be removed by the middleware before it lands. That cannot be corrected later in silver, because by then it is already in bronze. This is a compliance and security boundary, not a data quality one. Separately, deciding what the middleware rejects at the edge versus what the platform quarantines sets where bad input surfaces.

Settled position, from Point 1, not re-opened here.
- Structural and technical sanitisation at the middleware edge, well formed, size bounded, contract conformant.
- Business data quality, completeness, referential integrity and conforming rules in silver (ADR-001).

Open edges.

| Edge | Option | Owner | Trade-off |
|:--|:--|:--|:--|
| Sensitive and personal data | Strip or mask before landing | middleware | Nothing sensitive enters bronze, middleware carries the classification logic |
| | Land raw, govern in the platform | Databricks | Simpler middleware, sensitive data resides in bronze and is masked in silver and Unity Catalog |
| Bad records | Middleware rejects at the edge | middleware | Malformed input never lands, rejects surface upstream |
| | Land everything, silver quarantines | Databricks | Nothing lost at the boundary, invalid business records surface in silver |

Depends on. Point 0. The Point 1 cleansing split. A data classification of the SaaS sources, which fields are sensitive, a fact to establish before the room can close the top edge.

Owner of the call. IS head and security own the sensitive data decision, because it is compliance. Middleware architect implements edge sanitisation. Databricks architect owns silver quarantine and Unity Catalog governance.

Recommendation.
- Keep the Point 1 split. Structural and security sanitisation at the edge, data quality in silver.
- Decide sensitive data by classification. If any field must not reside in bronze, strip or mask it in the middleware before landing, because bronze is raw and silver is too late. Otherwise let it land and govern it in Unity Catalog with masking in silver.
- Reject only what is structurally unusable at the edge, malformed or oversized. Let well formed but business invalid records land and be quarantined in silver, so nothing business relevant is lost at the boundary.
- Get compliance sign off on the sensitive data decision. This touches data protection, so a qualified reviewer should confirm it. This sheet is not legal advice.

---

## Point 5. Decoupling mechanism, landing zone versus message bus

Status. Settled for the O2 inbound path. Open only if the middleware must serve needs beyond O2.

Question. Is inbound decoupling done by the file landing zone the ADRs already use, or does a message bus sit in the flow, and if a bus is wanted, what actually justifies it.

Why it is a decision. The middleware principles assume a message bus for decoupling. The platform decouples through a file landing zone and Auto Loader instead. Running both puts two components on the same job, and someone has to own the extra one.

Settled position, to ratify.
- For the O2 inbound path, the landing zone is the decoupling mechanism. SharePoint in phase 1, ADLS with file events in phase 2. Locked by ADR-009 and ADR-008.
- The middleware stays stateless either way. The landing zone holds the in flight data, not the middleware.

Divergence to acknowledge, useful signal not an oversight. Message bus is the classic middleware default. For a batch, file based JSON pull into a lakehouse, the landing zone plus Auto Loader already gives the buffering, decoupling and replay a bus would. Databricks practice overrides the classic principle for this workload.

Open edge.

| Edge | Option | Owner | Trade-off |
|:--|:--|:--|:--|
| Bus beyond O2 | No bus, landing zone only | Databricks | Simplest, covers the O2 path, matches the ADRs |
| | Bus upstream of the landing zone, for the wider SI | middleware | Justified only by real time distribution or fan out to consumers beyond the platform. O2 still ingests from the landing zone |

Depends on. Point 0. Whether the middleware serves consumers beyond O2, a scope fact for the IS head. Cadence, Point 6, since a real time need is the main thing that would call for a bus.

Owner of the call. IS head owns the scope question. Middleware architect owns the bus if one is justified. Databricks architect confirms the landing zone covers the O2 path with no bus.

Recommendation.
- For O2, use the file landing zone as the decoupling mechanism. Do not add a message bus to the O2 path, it would duplicate what Auto Loader already provides.
- Treat a bus as a separate, wider SI decision. Adopt one only if the middleware must distribute real time events or fan out to consumers beyond the platform. If adopted it sits upstream of the landing zone and does not change the O2 inbound contract.
- Record the no bus choice as a deliberate override of the classic principle, so it is a decision on the record rather than a gap.

---

## Point 6. Cadence and freshness, real time versus batch

Status. Open, gated by a business fact. Phase 1 is batch by construction.

Question. What data freshness does each business flow need, and what pull cadence does the middleware run to meet it.

Why it is a decision. The middleware pull cadence is an explicit input to the platform ingest configuration (ADR-008). Set it without a freshness target and you either over provision, paying for compute and source API load you do not need, or under deliver against what the workflow needs. Freshness is a business fact and it differs per flow, so it has to come from the use cases.

Settled position, to ratify.
- Phase 1 is batch, hours latency, by construction. SharePoint has no event path, so the drain is scheduled a few times a day (ADR-009). No real time option exists until the ADLS move.
- Phase 2 opens event driven near real time on file arrival (ADR-008). Continuous streaming is a fallback only under a sub minute SLA, because it bills idle compute.
- Cadence is set per flow, not once globally. Simplest mode that meets the need.

Open edges.

| Edge | Option | Owner | Trade-off |
|:--|:--|:--|:--|
| Freshness per flow | Near real time | business, then middleware | Only where the workflow needs it, higher cost and cadence |
| | Hourly or few times a day | business, then middleware | Fits most operational reporting, low cost |
| Phase 2 trigger | Event driven on arrival | Databricks | Near real time, no idle compute. The default |
| | Scheduled | Databricks | Fixed cadence, simple, small latency |
| | Continuous stream | Databricks | Sub minute only, bills idle compute |

Depends on. The per flow freshness requirement from the use cases, a business input. Point 2, since pull frequency and delta size trade against each other. Point 1 granularity.

Owner of the call. Business use case owners set the freshness need. Middleware architect sets the pull cadence to meet it. Databricks architect maps it to the trigger mode and confirms the cost.

Recommendation.
- Do not set cadence in the abstract. Bring a per flow freshness target to the workshop, even rough bands, near real time, hourly, daily.
- Phase 1, accept batch a few times a day, since SharePoint offers nothing faster and no SLA forces it.
- Phase 2, default to event driven on arrival. It gives near real time without idle compute. Use scheduled only where a fixed cadence is genuinely preferred, and continuous only if a sub minute SLA is set.
- Set the middleware pull cadence and the platform trigger together per flow, since one is the input to the other.

---

## Point 7. Outbound routing and message decomposition

Status. Open, low urgency. Mostly a build now versus defer call.

Question. When outbound data serves more than one SaaS, or an aggregate record must be split into units, does the middleware do the decomposition and routing, and is that built now or deferred.

Why it is a decision. The middleware principles keep decomposition as an option for future SI needs, splitting an aggregate of candidate, address and skills into separate messages, for example. Building it before a second consumer exists is speculative. Leaving no room for it means retrofitting the outbound path later.

Settled position, to ratify.
- Inbound data model segmentation is silver's job, conformed by subject area (ADR-001), not the middleware. See Points 1 and 4.
- Outbound splitting and routing to targets is a middleware job when it is needed, as the extension of the outbound adapter in Point 3.

Open edges.

| Edge | Option | Owner | Trade-off |
|:--|:--|:--|:--|
| Multi target routing | Build now | middleware | Ready for a second consumer, speculative until one exists |
| | Defer until a second target is real | middleware | No speculative complexity, small retrofit later |
| Aggregate decomposition | Gold exposes the units pre separated | Databricks | Middleware routes, does not split. Cleaner |
| | Middleware splits the aggregate | middleware | Needed only when gold cannot pre separate |

Depends on. Point 3 for the outbound contract. Whether a second outbound consumer is on the roadmap, a scope fact. Point 0.

Owner of the call. IS head on scope, is a second consumer coming. Middleware architect owns routing if built. Databricks architect decides whether gold exposes aggregates or pre split units.

Recommendation.
- Build the outbound adapter from Point 3 so routing can be added per target cleanly, but do not build multi target decomposition until a second consumer is real.
- Prefer gold to expose the units the consumers need, so the middleware routes rather than splits. Splitting in the middleware is the fallback when gold cannot pre separate.
- Revisit when a second SaaS target appears, as a per target extension, not a rebuild.

---

## Point 8. Scalability and volume sizing

Status. Open sizing input, not a design choice. Both sides scale by construction, the target has to be set.

Question. What peak and surge volume must the inbound boundary absorb, and does either side need protection beyond what the landing zone and serverless compute already give.

Why it is a decision. Scalability is a given for both components, but scalable means nothing without a figure. The surge target decides whether the default mechanisms are enough or whether the middleware needs rate limiting and the platform needs throughput tuning. It is a number to bring, not a design to invent.

Settled position, to ratify.
- The landing zone buffers inbound, so a surge lands as files and is drained by the platform with no backpressure onto the middleware or the SI. This is the main surge absorber, see Point 5.
- Platform compute is serverless and event driven (ADR-004, ADR-008), so it scales the drain without idle cost.
- The middleware stays stateless, which is what lets it scale horizontally under load.

Open edges.

| Edge | Option | Owner | Trade-off |
|:--|:--|:--|:--|
| Volume target | Establish peak and surge per source | business, then both | A fact to bring, gates the rest |
| Extra protection | None beyond landing zone and serverless | shared | Fits if the target is within default throughput |
| | Middleware rate limiting or batching | middleware | Needed only if a source bursts beyond the drain window |

Depends on. The volume figures from the sources and use cases. Point 1 granularity, since file count rises under surge. Point 6 cadence.

Owner of the call. Business and source owners provide the volume figures. Middleware architect confirms absorption and any rate limiting. Databricks architect confirms drain throughput.

Recommendation.
- Bring peak and surge volume figures per source to the workshop. Without them scalable cannot be signed off.
- Lean on the landing zone as the surge buffer and serverless as the elastic drain. They cover most surge with no extra work.
- Add middleware rate limiting or batching only if a source can burst beyond what the drain clears in the freshness window. Treat it as an exception with a figure behind it.
- Watch file count under surge, since one record per file from Point 1 multiplies files, and confirm the drain and trigger handle that rate.

---

## References

- ADR-001 medallion layer ownership, ADR-004 serverless compute, ADR-008 ADLS to bronze ingestion, ADR-009 SharePoint to bronze ingestion. This folder.
- FRAMING.md, O2 framing. `2607-o2-requirements`.
- Ingest data as semi-structured variant type, Azure Databricks. https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant
- Ingest files from SharePoint, Azure Databricks. https://learn.microsoft.com/en-us/azure/databricks/ingestion/sharepoint

<!--
Version: 1.1 | Last Updated: 2026-07-16 | Status: Draft
-->
