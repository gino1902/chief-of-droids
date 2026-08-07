# ADR-008 — ADLS Gen2 to bronze ingestion: Auto Loader with managed file events (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Accepted (design locked, standing checks open before production) |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | Platform / Cloud team, Security |
| Informed | Wider data team |
| Detailed design | [2026-06-24-adls-bronze-ingestion-design-lock-in.md](../2026-06-24-adls-bronze-ingestion-design-lock-in.md) |

---

## Context

An external extractor pulls JSON from a SaaS API and lands files in ADLS Gen2. We need
the launch and drain mechanism that moves those files into a bronze Delta table, for a
periodic-pull source. The full option comparison and benchmark live in the linked
design lock-in; this record captures the decision only.

---

## Options evaluated

**Option A — File-arrival trigger launching a `Trigger.availableNow` drain**
Auto Loader on managed file events, on a Unity Catalog external location. A Lakeflow job
file-arrival trigger launches the run and it drains with `Trigger.availableNow`. The
cluster runs only when new files arrive, so there is no idle compute and no fixed
schedule interval.

**Option B — Scheduled `Trigger.availableNow` batch**
Same drain, launched on a fixed cadence rather than on arrival. Fallback where a fixed
cadence is preferred over event-driven launch.

**Option C — Continuous stream**
Lowest latency via the cache hop with no per-run cluster start, but bills idle compute
between pulls. Fallback only if a sub-minute freshness SLA is set.

---

## Decision

**Option A chosen. Fallbacks are Option B where a fixed cadence is preferred and
Option C only under a sub-minute freshness SLA. The extractor's pull cadence and the
bronze freshness target are the inputs that finalise the configuration.**

### Rationale

Benchmarked 151 of 170 against the platform selection criteria, leading on operational
ownership, ingestion guarantee and security surface. Event-driven launch removes idle
compute without going continuous, keeping the managed-path operational and security
lead. Full scoring is in the linked design.

Decision basis: the linked design lock-in, verified against current Azure Databricks
documentation for Auto Loader file events and file-arrival triggers (June 2026).

---

## Validation

The standing checks in the linked design gate production, notably runtime DBR 18.1+ for
the automatic managed-file-events default, file events enabled on the external location,
unique filenames, VARIANT treated as Public Preview with promoted key columns,
per-subpath UC volume scoping, a run at least every 7 days, and an idempotent ingest.
The storage and integrity security baseline (items 9 to 13) applies regardless.

---

## Consequences

- Ingestion is event-driven with batch drain, no idle compute, exactly-once via the
  Auto Loader RocksDB checkpoint.
- The file events service (service-owned Event Grid subscription plus storage queue,
  one pair per external location) is managed, not operated by us.
- Bronze stores the whole record as VARIANT plus promoted typed keys.
- Migration levers are the file-arrival trigger's minimum-time-between-runs and
  wait-after-last-change settings.

---

## Sources

- Detailed locked design (this repo): 2026-06-24-adls-bronze-ingestion-design-lock-in.md
- Auto Loader with file events overview — https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/file-events-explained
- Trigger jobs when new files arrive — https://learn.microsoft.com/en-us/azure/databricks/jobs/file-arrival-triggers
- Manage external locations (file events) — https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/manage-external-locations
- Ingest data as variant — https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant
- File events FAQ — https://learn.microsoft.com/azure/databricks/connect/unity-catalog/cloud-storage/file-events-faq

---

| Field | Value |
|:------|:------|
| Version | 0.1 (draft) |
| Last Updated | 2026-07-09 |
