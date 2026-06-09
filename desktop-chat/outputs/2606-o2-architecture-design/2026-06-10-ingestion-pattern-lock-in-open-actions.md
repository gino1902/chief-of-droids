# Open actions: ADLS bronze ingestion tech design

> Companion to the ingestion pattern lock-in play. The play is a reusable recipe and
> stays pure to its format, so these session-specific open points live here.

These are the points still open before the tech design can move from Review to Final.

## Decision-driving

1. Confirm the extractor's pull cadence and the bronze freshness SLA. This is the single variable that resolves the A2-versus-A1b fork. Periodic pulls with minute-level freshness select A2, continuous or sub-minute freshness select standalone A1b.

## Runtime and ingestion

2. Confirm the new workspace runs DBR 18.1 or above, so the automatic file-events default applies. On an earlier runtime, set `cloudFiles.useManagedFileEvents=true` explicitly.
3. Fix the bronze VARIANT write expression to match the chosen ingest option. The Auto Loader path uses `singleVariantColumn`, the SQL or INSERT path uses `parse_json`.
4. Decide per-subpath Unity Catalog volume scoping for discovery (standing check 5), to avoid the file-events rate limit on A1b and trigger time-outs on A2.
5. Decide whether a data-completeness SLA requires `cloudFiles.backfillInterval` (standing check 6).

## Security baseline (owners and confirmation needed)

6. Lock landing-zone write access to the extractor identity alone (standing check 7).
7. Private network on the storage account, no public access, firewall and private endpoints (standing check 8).
8. Encryption at rest and in transit, platform or customer-managed keys (standing check 9).
9. Content validation before the MERGE into bronze, with anomaly quarantine (standing check 10).
10. Trigger ingestion only on FlushWithClose from the trusted account (standing check 11).

## Documentation and workspace

11. Promote `2026-06-09-adls-bronze-ingestion-design.md` from Review to Final once the above are locked.
12. Weigh whether the ingestion pattern lock-in play should later be folded into the `architecting-data-platforms` skill, given the overlap noted during play authoring.

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-06-10 |
| Status | Draft |
