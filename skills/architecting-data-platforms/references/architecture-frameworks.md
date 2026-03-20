# Architecture Frameworks Reference

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
