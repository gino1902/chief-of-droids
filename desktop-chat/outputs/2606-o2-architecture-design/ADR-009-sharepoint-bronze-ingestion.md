# ADR-009 — SharePoint to bronze ingestion: standard connector, scheduled drain (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-07-09 |
| Status | Draft (blocked by one unverified composition, see Validation) |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | Platform / Cloud team, Security |
| Informed | Wider data team |
| Detailed design | [2026-06-24-sharepoint-to-bronze-ingestion-lock-in.md](2026-06-24-sharepoint-to-bronze-ingestion-lock-in.md) |

---

## Context

A bounded, temporary phase: ingest JSON from a SharePoint document library into bronze
while SharePoint is the landing zone, before the extractor repoints to ADLS Gen2
(ADR-008 governs the end state). SharePoint emits no storage events, so there is no
native file-arrival trigger. The full build recipe lives in the linked design.

---

## Options evaluated

**Option A — Standard SharePoint connector through a UC connection, scheduled drain**
Read directly through a Unity Catalog connection, no intermediate store. Auto Loader
lands each record as a single VARIANT and appends to bronze. A Lakeflow job clock
launches the run 2 to 3 times per day, draining with `Trigger.availableNow`. Chosen for
whole-record VARIANT output, provenance, full pipeline control, and a path-swap-only
migration to ADLS.

**Option B — Managed SharePoint connector (Lakeflow Connect)**
Managed sync and schema handling, but parses into its own schema and forecloses the
single-VARIANT route. Rejected on output shape, not capability.

**Options not pursued**
- Direct Lakeflow Connect managed connector for the SaaS, if it later becomes a
  supported source: this would retire both SharePoint and the extractor and skip this
  path entirely. A second exit beyond the ADLS migration.

---

## Decision

**Option A chosen as a disposable bridge. The design is temporary by intent: at ADLS
migration only the source path and trigger change (see the migration table in the
linked design). Benchmarked 123 of 170, trading latency, scale and maturity for speed
of delivery while SharePoint is the landing.**

### Rationale

The standard connector is chosen for output shape and control, not a capability gap.
Both connectors read JSON into Delta; only the standard one lands the whole record as
one append-only VARIANT with full control and a path-swap migration. The connector is
Beta, on a DBR 17.3 LTS floor, with a review date.

Decision basis: the linked design (carried from the paired build play), verified
against the SharePoint standard-connector and variant-ingestion docs on 2026-06-23.

---

## Validation

> ⚠️ Blocks Final: the `singleVariantColumn` combined with `databricks.connection` in a
> single read is not shown in any official example and must pass a one-file empirical
> test before this design is promoted from Draft. The gap dies at ADLS migration, where
> `singleVariantColumn` from an object-store path is the documented pattern.

Remaining standing checks in the linked design gate production, notably DBR 17.3 LTS+
with the SharePoint Beta enabled and a review date set, JSON-only format, unique
filenames, `multiLine` matched to file shape, VARIANT Public Preview handling, URL
folder scoping, manual source cleanup (`cleanSource` unsupported), OAuth M2M with
`Sites.Selected` or `Sites.Read.All`, and an idempotent ingest.

---

## Consequences

- A short-lived path that limits exposure to the one unverified composition.
- Latency is bounded by the poll interval (hours), with no event path available.
- One query reads one site; a second site means a second query and pipeline.
- Migration to ADLS changes only the read-path block; the write block is untouched.

---

## Sources

- Detailed locked design (this repo): 2026-06-24-sharepoint-to-bronze-ingestion-lock-in.md
- SharePoint standard connector — https://learn.microsoft.com/en-us/azure/databricks/ingestion/sharepoint
- SharePoint source setup overview — https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/sharepoint-source-setup-overview
- SharePoint managed connector — https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/sharepoint
- Ingest data as variant — https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant
- Configure Auto Loader for production — https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/production

---

| Field | Value |
|:------|:------|
| Version | 0.1 (draft) |
| Last Updated | 2026-07-09 |
