# Architecture Frameworks Reference
<!-- version: 1.2 | last_updated: 2026-03-23 -->

Stable judgment patterns — these do not require fetch verification unless a
specific platform's current feature availability is being cited.

---

## Platform Paradigm Selection

| Paradigm | When to choose | When to avoid |
| :--- | :--- | :--- |
| Lakehouse (Databricks) | Unified batch + streaming + ML; cost-sensitive; schema evolution needed | Purely relational BI with no ML ambition |
| Cloud Data Warehouse (Synapse, BigQuery, Snowflake) | SQL-first, BI-heavy, low engineering capacity | High-volume streaming, complex ML pipelines |
| Data Mesh | Multiple autonomous domains, federated ownership, large org | Small teams, immature data culture, no platform team |
| Lambda Architecture | Proven streaming + batch separation needed | Adds ops complexity — prefer Kappa if streaming can reprocess |
| Kappa Architecture | Single streaming pipeline handles real-time and historical | Reprocessing cost prohibitive at scale |

**Senior rule:** Never recommend a paradigm without stating the org maturity and team
size assumptions behind it.

---

## Build vs Buy

Evaluate on four axes:

1. **Differentiation** — commodity infrastructure or business differentiator?
2. **Maintenance burden** — who owns upgrades, patches, incident response?
3. **Time to value** — managed services compress delivery; custom builds defer it.
4. **Lock-in risk** — assess portability and exit cost explicitly.

---

## Medallion Architecture — Senior View

```
Bronze (raw ingest) → Silver (cleaned, typed, deduplicated) → Gold (business-ready)
```

| Layer | Ownership | Schema | Quality gate |
| :--- | :--- | :--- | :--- |
| Bronze | Platform / ingestion team | Schema-on-read or inferred | None — preserve raw |
| Silver | Domain / data engineering | Schema-on-write, enforced | DLT Expectations or equivalent |
| Gold | Analytics / product | Curated, versioned | Business-validated; SLA-bound |

- Gold proliferation into domain-specific variants (Gold-CRM, Gold-Finance) is normal
  at scale — manage via Unity Catalog schemas, not additional medallion layers.
- DLT Expectations failure mode (warn / drop / fail) must be classified at design time.

---

## Data Warehousing Pattern on Databricks

For organisations with strong BI and SQL analytics requirements, Gold can be structured
as a dimensional model rather than a flat wide-table layer. This is a modeling decision
within Gold — it does not add a medallion layer.

**Modeling options within Gold:**

| Model | When to choose | When to avoid |
| :--- | :--- | :--- |
| Dimensional (facts + dimensions) | BI-heavy consumption; multiple teams querying shared entities; stable business definitions | Exploratory analytics; ML feature pipelines where wide tables are preferred |
| Wide tables | ML feature pipelines; self-service analytics with flexible slicing | Enterprise BI where shared dimension definitions matter |
| Data marts | Domain-scoped cuts of Gold (e.g. Finance mart, Sales mart) for high-concurrency departmental BI | Don't create a mart for every consumer — manage via Unity Catalog schemas, not schema proliferation |

**Decision rules:**

- Dimensional modeling with facts and dimensions is appropriate when Gold serves a traditional BI workload with high-concurrency SQL queries via Databricks SQL
- Data marts are domain variants of Gold — manage via Unity Catalog schemas; do not introduce an additional medallion layer above Gold
- Model outputs from ML pipelines (e.g. scored predictions, feature outputs) are stored alongside warehouse data as native queryable assets — no data movement required
- Databricks SQL with Photon and serverless compute handles high-concurrency BI queries directly from Gold — no separate data copy to an external warehouse is needed

**Senior rule:** Decide modeling approach at Phase 4 (Data Modelling) — not during
implementation. A late switch from wide tables to dimensional adds significant rework.

---

## Lakehouse Federation — Federate vs Ingest

Lakehouse Federation provides governed query access to external systems (e.g. PostgreSQL,
MySQL, Salesforce, Redshift) without physically moving data into the lakehouse.

⚠️ Fetch from `docs.databricks.com` before advising on supported source systems,
connector availability, or performance characteristics — these evolve with platform releases.

**Decision rules (stable — no fetch required):**

| Scenario | Use Federation | Use Ingestion (Auto Loader / CDC) |
| :--- | :--- | :--- |
| Exploratory queries on live operational data | Yes | No — ingestion overhead not justified |
| Joining lakehouse data with a live external system ad hoc | Yes | No |
| High-volume analytical workloads on external data | No — query performance degrades at scale | Yes — ingest and optimise locally |
| Data that must participate in DLT pipelines or quality checks | No — Federation is read-only query layer | Yes |
| Data that must be governed by Unity Catalog lineage end-to-end | No — lineage stops at the Federation boundary | Yes |
| Operational reporting where latency of a full ingest cycle is unacceptable | Yes — if volume is manageable | No |

**Senior rule:** Federation is a query shortcut, not a data platform substitute.
Any data that needs transformation, quality enforcement, or long-term retention
must be ingested — not federated. Never position Federation as an alternative to
a Bronze ingest layer for production analytical workloads.

---

## API and Integration Contract Standards

Data platforms expose and consume data through APIs and event streams. Two ratified
standards govern how those interfaces are described and contracted. Surface both
during Phase 3 (Architecture Selection) and Phase 4 (Data Modelling).

⚠️ Fetch from official sources before advising on specific syntax, version features,
or tooling support — both evolve independently of Databricks runtime releases.

| Standard | Use when | Official source |
| :--- | :--- | :--- |
| OpenAPI | Describing RESTful APIs — data product endpoints, serving layer APIs, platform REST interfaces | `spec.openapis.org` |
| AsyncAPI | Describing event-driven and streaming interfaces — Kafka topics, Event Hubs channels, WebSocket feeds, message-driven data products | `asyncapi.com/docs/reference/specification` |

**Decision rules (stable — no fetch required):**

- Use OpenAPI to describe any RESTful serving layer endpoint — Gold-layer data products exposed as APIs, model inference endpoints, platform management APIs. OpenAPI contracts belong in Phase 4 alongside data contracts.
- Use AsyncAPI to describe event-driven interfaces — Kafka topics, Event Hubs channels, streaming data products. AsyncAPI is the correct contract format when consumers need to know message schema, channel address, and protocol bindings, not just REST endpoints.
- Never use OpenAPI to describe a Kafka topic or an Event Hubs channel — the protocol model is wrong. AsyncAPI is the correct standard for message-driven interfaces.
- Use both OpenAPI and AsyncAPI when a data product exposes both REST and event-driven interfaces — they compose; one does not replace the other.

**Senior rule:** API contracts (OpenAPI / AsyncAPI) are Phase 4 deliverables, not
post-launch documentation. A data product without a machine-readable contract is
not a data product — it is a table with an undocumented access pattern.

### Emerging Convention: llms.txt

**Maturity status:** Community proposal (Answer.AI, Sept 2024). No formal standards
body. No confirmed support from any major LLM provider as of early 2026. Widely
adopted by developer-focused documentation sites (Anthropic, Cloudflare, Stripe,
Vercel) but not yet an enforced protocol.

**What it does:** A Markdown-structured file at `/llms.txt` on a domain root that
gives AI agents a curated map of the site's most relevant documentation and API
endpoints — reducing the need for agents to parse complex HTML or crawl multiple pages.

**When to surface it:** Raise `llms.txt` when AI agent or LLM-powered tooling
consumption is an explicit requirement — typically identified in Phase 1
(Requirements). Do not surface it as a default architecture decision.

**Decision rules:**

- If the platform or its data products will be consumed by AI agents, recommend adding `/llms.txt` as a low-effort discoverability layer alongside the OpenAPI / AsyncAPI contracts — not as a substitute for them.
- Do not position `llms.txt` as equivalent to OpenAPI or AsyncAPI — it is a documentation hint, not a machine-executable contract.
- Treat it as forward-looking infrastructure: low cost to add, no confirmed return, but aligned with the direction of AI-native consumption patterns.

**Official source:** `llmstxt.org`
