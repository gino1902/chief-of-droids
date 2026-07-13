---
name: Operations Orchestrator (O2) Concepts
last_updated: 2026-07-13
---

# Operations Orchestrator (O2) — Domain language

Single source of the project's domain language. Terms are defined here so downstream work references them rather than reinventing them. New terms are recorded back here, never left in one requirements slice.

## Shared core

Terms with one meaning everywhere in the project.

| Term | Definition |
|:--|:--|
| `landing zone` | External staging area, populated by the IT middleware, that the platform reads source data from |
| `bronze` | Raw-ingest medallion layer preserving source data as delivered |
| `silver` | Cleansed and conformed medallion layer derived from `bronze` |
| `gold` | Enterprise-entity medallion layer exposing trusted, high-quality data |
| `trusted data` | Data the business can rely on without reconciling it at each handover |
| `cross-team workflow` | A workflow that crosses team boundaries, for example budget-to-report or talent-request-to-deployment |

## Contexts

One block per bounded context (a FRAMING track). A term may appear in more than one context with a different meaning; the context map records the relationship.

### Data ingestion and transformation

| Term | Definition |
|:--|:--|
| `source contract` | The agreed shape a delivered file must match to be ingested |
| `enterprise entity` | A conformed business object built in `gold` from `silver` |
| `business key` | The natural key that uniquely identifies an `enterprise entity` |
| `reference data` | Shared lookup data an `enterprise entity` resolves against |
| `data-quality rule` | A validation rule gating publication to `gold` |
| `quarantine` | Holding area for records that fail validation, kept out of `silver` |

### Data exposition

| Term | Definition |
|:--|:--|
| `agentic workflow` | A team-fitted workflow, orchestrated by agents, that exposes `gold` data to a use case |
| `use case eligibility` | The decision-framework test (ROI, location) for admitting a use case |

## Context map

Relationships between contexts: which owns a term, which consumes it, where the same word diverges.

| From | To | Relationship |
|:--|:--|:--|
| IT middleware (out of scope) | Data ingestion and transformation | Owns population of the `landing zone`, upstream of ingestion |
| Data ingestion and transformation | Data exposition | Exposition consumes the `gold` layer produced by ingestion |
| Platform engineering | all contexts | Owns governance and the catalog (`Unity Catalog`) the layers are registered in |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
