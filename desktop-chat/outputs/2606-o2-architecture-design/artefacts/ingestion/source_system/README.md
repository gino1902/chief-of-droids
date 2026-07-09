# ingest_source_system (bronze)

Bronze ingestion bundle for one data producer (ADR-001, ADR-008). Clone per producer, renaming `source_system` throughout.

- Pattern: Auto Loader with managed file events, file-arrival trigger, `Trigger.availableNow` drain, whole-record VARIANT. See `../../../2026-06-24-adls-bronze-ingestion-design-lock-in.md` for the full locked design.
- For the SharePoint bridge variant, see `../../../2026-06-24-sharepoint-to-bronze-ingestion-lock-in.md` (ADR-009).

Validate: `databricks bundle validate -t dev`. Deploy: `databricks bundle deploy -t dev`.

`fixtures/` holds sample JSON for the unit tests (empty in the skeleton).
