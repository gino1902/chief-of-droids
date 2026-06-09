# ADLS Gen2 to bronze ingestion: locked design

> Event-driven ingestion of JSON from a SaaS source into a bronze Delta table.
> Locked on option A1b, Auto Loader with managed file events.
> Pairs with 2026-06-09-adls-bronze-ingestion-design.md (the full option comparison).

This document is the locked design. The option comparison that produced it lives in the paired design doc and is not repeated here. All claims are checked against current Azure Databricks documentation (June 2026).

## Locked decision

The ingestion path is A1b, Auto Loader with managed file events, on a Unity Catalog external location. The run mode is a scheduled `Trigger.availableNow` batch. A continuous stream is used only if a sub-minute freshness SLA is set. The deciding inputs are the extractor's pull cadence and the bronze freshness target, both of which favour the scheduled batch for a periodic puller.

Two facts underpin the decision and are stated once:

- From Databricks Runtime 18.1, Auto Loader uses managed file events automatically when available (`useManagedFileEvents = if_available`). On earlier runtimes the option is set explicitly. This is documented in the File events FAQ [F], not in the file-events-explained [5] or file-notification-mode [4] pages, so verify against the FAQ.
- File events are enabled by default on new Unity Catalog external locations, with an explicit opt-out (`enable_file_events=false`). Enabling them is no longer a manual prerequisite.

## Why A1b

A1b's profile against the platform selection criteria. Ratings are 1 to 5 on how well A1b satisfies each criterion (5 best), weighted by the platform criterion weight.

| # | Criterion | Weight | Rating | Weighted | Rationale |
| :--- | :--- | ---: | ---: | ---: | :--- |
| 1 | Compute cost impact | 5 | 3 | 15 | A continuous stream bills idle between pulls. The scheduled availableNow run mode drops idle compute and lifts this toward 4 |
| 2 | Latency, event to bronze | 3 | 4 | 12 | Cache hop adds a small delay with no per-run cluster start in continuous mode. A scheduled batch adds the schedule interval |
| 3 | Scale ceiling and limits | 3 | 4 | 12 | One managed queue per external location scales to many streams when each is scoped to a per-subpath volume |
| 4 | Operational ownership | 5 | 5 | 25 | One managed stream, managed tuning and cleanup, fewest moving parts |
| 5 | Ingestion guarantee | 5 | 5 | 25 | Auto Loader exactly-once via the RocksDB checkpoint, resumable on restart |
| 6 | Maturity and longevity | 3 | 4 | 12 | Managed file events is the documented default on a current runtime, a GA mechanism |
| 7 | Source format coverage | 2 | 4 | 8 | Reads JSON through the standard Auto Loader reader, whole-record VARIANT absorbs schema drift |
| 8 | Security surface and access governance | 5 | 5 | 25 | Stays inside the governed plane on the access connector identity, no self-operated component, no orchestration layer |
| 9 | GDPR and data protection | 3 | 4 | 12 | Inherits Unity Catalog lineage, classification and governed access |
| | Total (max 170) | | | 146 | |

Verdict: A1b run as a scheduled availableNow batch is the strongest single configuration for a periodic pull extractor. It keeps idle compute low while retaining the operational-ownership and security lead the profile shows. The fallback is a continuous A1b stream, used only if a sub-minute freshness SLA appears. The pull cadence and the bronze freshness target remain the inputs that finalise the configuration.

## Glossary

Scoped to the concepts this design uses.

| Term | Meaning |
| :--- | :--- |
| ADLS Gen2 | Azure Data Lake Storage Gen2, a set of capabilities on Azure Blob Storage unlocked by the hierarchical namespace. The raw landing zone here |
| HNS | Hierarchical namespace, the storage-account setting that gives file-system semantics, directory atomicity and the Data Lake event set |
| abfss / dfs endpoint | The ABFS driver and the `dfs.core.windows.net` endpoint through which Databricks reads ADLS Gen2 |
| CreateFile / FlushWithClose | The Data Lake Gen2 write operations. FlushWithClose marks the file fully committed, the only safe trigger boundary |
| Event Grid system topic | The Azure Event Grid topic that publishes storage events for the account |
| Microsoft.Storage.BlobCreated | The storage event raised on file creation, filtered on FlushWithClose so it fires only on a committed file |
| File events (managed) | A Databricks service that listens to storage notifications, caches file metadata, and serves discovery to Auto Loader. One managed queue per external location |
| External location | A Unity Catalog object that grants governed access to a cloud storage path |
| UC volume | A Unity Catalog volume mapping a subpath. Discovery is scoped to a per-subpath volume to keep file events efficient |
| Auto Loader | The Databricks incremental file-ingestion engine (`cloudFiles`), exactly-once via checkpoint |
| cloudFiles.useManagedFileEvents | The Auto Loader option that reads from the managed file events cache. Automatic on DBR 18.1+ |
| Trigger.availableNow | A batch trigger that processes all files present at start, then stops. The locked run mode |
| Checkpoint (RocksDB) | The Auto Loader state store that tracks discovered files and gives exactly-once and resume-on-restart |
| cloudFiles.cleanSource | The Auto Loader option that archives or deletes processed source files (DBR 16.4 LTS+). A storage-cost lever here |
| cloudFiles.backfillInterval | The Auto Loader option that triggers periodic backfills against rare missed notifications, without duplicates |
| VARIANT | The semi-structured column type (DBR 15.3+, Public Preview) holding the whole JSON record |
| singleVariantColumn | The Auto Loader option that ingests the whole record into one VARIANT column |
| corruptRecordColumn | The column that captures malformed or oversized (>16 MB) records under PERMISSIVE mode |
| Promoted columns | Typed columns extracted alongside the VARIANT (ingest_ts, source_path, business_key) for keys used to filter, join, cluster or partition |
| Access connector / managed identity | The Azure managed identity, via the Databricks access connector, that authorises the file events service against storage |
| Lakeflow job | The Databricks job that runs the Auto Loader stream on schedule |

## Diagram

```text
 [SaaS API] --pull(REST)--> [Extractor] --write JSON--> [ADLS Gen2 landing (HNS)]
 external                   ext. app                    CreateFile + FlushWithClose, abfss://
 system                     already running             unique filenames (same-name overwrite
                                                         does NOT retrigger discovery)
                                                         cloudFiles.cleanSource retention (DBR 16.4 LTS+)
                                                              |
                                                              | Microsoft.Storage.BlobCreated
                                                              | (Event Grid subscription filtered on FlushWithClose)
                                                              v
                                                    [Azure Event Grid system topic]
                                                    at-least-once delivery, so the ingest must be idempotent
                                                              |
                                                              v
 [Auto Loader stream, MANAGED file events]
   ONE Databricks-managed queue per UC external location, file events service caches metadata
   cloudFiles.useManagedFileEvents=true (automatic from DBR 18.1), reads the CACHE
   run mode: Trigger.availableNow on a schedule (continuous only for a sub-minute SLA)
   exactly-once via RocksDB checkpoint
   scope each stream to a per-subpath UC volume to avoid file-events rate limiting
   listing: 24h service reconciliation scan, plus 7-day stream read-position expiry
                                                              |
                                                              v
 [Bronze Delta table]
   singleVariantColumn -> whole-record VARIANT (DBR 15.3+, Public Preview) plus promoted columns
   (ingest_ts, source_path, business_key)
   VARIANT cannot be a partition / clustering / Z-order key, nor used in compare/group/order,
   so promote any key you filter, join or cluster on into a typed column
   VARIANT path access is CASE-SENSITIVE (col:Field is not col:field)
   VARIANT caps records at 16 MB; malformed or oversized records land in corruptRecordColumn
   under PERMISSIVE mode; whole-record VARIANT disables schema evolution and rescuedDataColumn
```

## Design steps

| Design step | Technical elements | Benefits | Watch-outs | Sources |
| :--- | :--- | :--- | :--- | :--- |
| 1. Extract from SaaS source | External extractor (already running), SaaS REST client, emits JSON files | Decoupled from Databricks, owns SaaS auth and pagination | Scheduling and retry are the extractor's, no native exactly-once upstream | [7] |
| 2. Land file to ADLS Gen2 | ADLS Gen2 (HNS), abfss driver, CreateFile + FlushWithClose, unique filenames, cloudFiles.cleanSource (DBR 16.4 LTS+) | Durable landing, FlushWithClose gives a clean commit boundary, cleanSource caps source-directory storage cost | Same-name overwrite does not retrigger discovery, so keep unique filenames. Discovery is incremental, so cleanSource is a storage-cost lever, not a discovery-speed one | [1][3][8] |
| 3. Emit event, ADLS to Event Grid | Event Grid system topic, Microsoft.Storage.BlobCreated, subscription filtered on FlushWithClose | Native push, no polling, decoupled | At-least-once delivery means duplicates are possible, HNS needs the FlushWithClose filter to avoid premature events | [2][3] |
| 4. Catch and ingest, managed file events | Auto Loader stream, useManagedFileEvents=true (automatic on DBR 18.1+), one managed queue per UC external location, per-subpath volume, reads cache, Trigger.availableNow on a schedule, RocksDB checkpoint exactly-once | Fewest moving parts, one queue per location, no extra creds, managed tuning and cleanup, default-on, exactly-once | Cache hop adds latency, run at least every 7 days or it falls back to a full listing, 24h reconciliation scan, scope to a per-subpath volume to avoid rate limiting | [4][5][6] |
| 5. Write to bronze as VARIANT | Delta bronze table, singleVariantColumn whole-record VARIANT (DBR 15.3+), promoted columns (ingest_ts, source_path, business_key) | Schema-flexible semi-structured storage, replaces JSON strings, queryable | VARIANT cannot be a partition, clustering or Z-order key nor used in compare, group or order, so promote keys. Path access is case-sensitive. 16 MB record cap. Public Preview | [9][10] |

## Standing checks before a production commitment

Items 1 to 7 are runtime and ingestion checks. Items 8 to 12 are the storage and integrity security baseline, which applies regardless of the design.

1. Confirm the target workspace runtime is DBR 18.1 or above for the automatic file-events default. On an earlier runtime set `cloudFiles.useManagedFileEvents=true` explicitly. Verify the automatic behaviour against the File events FAQ [F].
2. Confirm managed file events are enabled on the external location the stream reads, or accept the default-on behaviour, and confirm the workspace is not gated behind a regional allowlist preview.
3. Keep unique filenames or a flag file. Overwriting a file with the same name does not fire a notification.
4. Treat the VARIANT bronze write as Public Preview. Promote any key used for partition, clustering, filter, join, group or order into a typed column. Match field casing exactly, since path access is case-sensitive.
5. Scope discovery to a per-subpath Unity Catalog volume rather than the bare external location, to avoid the Too many requests rate limit when several streams read different subpaths under one location.
6. Run the stream at least once every 7 days, or the stored read position expires and Auto Loader falls back to a full directory listing. A scheduled availableNow run satisfies this.
7. If a data-completeness SLA applies, set `cloudFiles.backfillInterval` for periodic backfills against rare missed notifications. Backfills do not cause duplicates.
8. Lock write access to the landing zone to the extractor identity alone, so no other principal can land a file.
9. Put the storage account on a private network, no public access, with firewall rules and private endpoints.
10. Enforce encryption at rest, platform or customer-managed keys, and in transit.
11. Validate content before the write into bronze, schema and contract checks, size and type limits, and quarantine anomalies. Treat unstructured or binary uploads as untrusted.
12. Trigger ingestion only on the real commit event (FlushWithClose) from the trusted account, so a forged or premature event cannot inject data.

## Official sources

| Ref | Topic | Link |
| :--- | :--- | :--- |
| 1 | ADLS Gen2 introduction | [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction) |
| 2 | Blob storage events overview | [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-event-overview) |
| 3 | Blob storage event schema | [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/event-grid/event-schema-blob-storage) |
| 4 | Auto Loader file notification mode | [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/file-notification-mode) |
| 5 | Auto Loader with file events overview | [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/file-events-explained) |
| 6 | Auto Loader file detection modes | [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/file-detection-modes) |
| 7 | Standard connectors in Lakeflow Connect | [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/databricks/ingestion/) |
| 8 | Configure Auto Loader for production | [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/production) |
| 9 | Ingest data as variant | [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant) |
| 10 | Variant versus JSON strings | [learn.microsoft.com](https://learn.microsoft.com/en-us/azure/databricks/semi-structured/variant-json-diff) |
| F | File events FAQ | [learn.microsoft.com](https://learn.microsoft.com/azure/databricks/connect/unity-catalog/cloud-storage/file-events-faq) |

---

| Field | Value |
| :--- | :--- |
| Version | 1.1 |
| Last Updated | 2026-06-10 |
| Status | Review |
