# Event-driven ADLS Gen2 to bronze ingestion: design

Scope: an event-driven pattern that lands JSON from a SaaS source into ADLS Gen2 and ingests it into a bronze Delta table. The pattern has a shared head, four interchangeable catch-and-ingest options (A1a, A1b, A2, B), and a shared tail. A per-option decision table and the official sources follow.

All version-sensitive claims here are checked against current Azure Databricks documentation (June 2026). Two facts shape the option choice and are stated once up front:

- From Databricks Runtime 18.1, Auto Loader uses managed file events automatically when they are available (`useManagedFileEvents = if_available`). On earlier runtimes you set the option explicitly.
- File events are enabled by default on new Unity Catalog external locations, with an explicit opt-out. Enabling them is no longer a manual prerequisite for new locations.

The effect is that managed file events (A1b) is the documented default ingest path on a current runtime. The other options are deliberate departures from that default for a specific reason: lower latency (A1a), cost on irregular arrivals (A2), or no Unity Catalog (B).

## Deliverable 1: annotated ASCII diagram

```
============================== SHARED HEAD (all options) ==============================

 [SaaS API] --pull(REST)--> [Extractor] --write JSON--> [ADLS Gen2 landing (HNS)]
 external                   ext. app you                CreateFile + FlushWithClose, abfss://
 system                     build/operate               unique filenames (same-name overwrite
                                                         does NOT retrigger downstream)
                                                         cloudFiles.cleanSource retention (DBR 16.4 LTS+)
                                                              |
                                                              | Microsoft.Storage.BlobCreated
                                                              | (Event Grid subscription filtered on FlushWithClose)
                                                              v
                                                    [Azure Event Grid system topic]
                                                    at-least-once delivery, so downstream must be idempotent
                                                              |
                       ===== choose ONE catch + ingest option (A1a / A1b / A2 / B) =====


 --- A1b  Auto Loader stream, MANAGED file events  (default path on DBR 18.1+) ---------
   ONE Databricks-managed queue per UC external location, file events service caches metadata
   cloudFiles.useManagedFileEvents=true (automatic from DBR 18.1), reads the CACHE,
   exactly-once via checkpoint
   listing: 24h service reconciliation scan, plus 7-day stream read-position expiry
   + 1 queue per location, no extra creds   - cache hop adds latency vs reading the queue
   + managed tuning + cleanup, default-on   - needs Unity Catalog
   + fewest moving parts                    - run at least every 7 days or it falls back to listing


 --- A1a  Auto Loader stream, CLASSIC file notification  (GA) -------------------------
   Event Grid sub + Azure Queue Storage provisioned PER STREAM by Auto Loader
   cloudFiles.useNotifications=true, reads the QUEUE directly, exactly-once via checkpoint
   + lowest latency (no cache hop)          - per-stream queue management, you grant create creds
   + full control                           - 500 notification pipelines per storage account (ADLS), more IAM
   choose only when sub-cache latency matters


 --- A2  Workflows FILE-ARRIVAL TRIGGER -> ephemeral JOB (Auto Loader inside) ---------
   trigger checks ~1 min best-effort on UC volume/external location, starts a job run
   debounce via min_time_between_triggers and wait_after_last_change, Auto Loader runs inside
   caps: file events ON, no file-count limit; OFF, up to 50 jobs and 10k files per location
   + compute only on arrival (cost)         - ~1 min latency, per-run cluster start
   + good for irregular / batch arrivals    - UC required, overwrite same name does NOT trigger
                                            - exactly-once comes from Auto Loader, NOT the trigger


 --- B  Azure FUNCTION (Event Grid trigger) -> jobs/run-now -> notebook JOB -----------
   Event Grid -> Function (push, no queue), filter api==FlushWithClose, run-now with file URL
   notebook reads file + MERGE, auth via service principal (Entra ID OAuth)
   + no Unity Catalog needed                - you own and operate Function + subscription
   + custom routing logic, any language     - 1 run per event (run-now limits, cluster start)
                                            - idempotency is YOUR job, older capture pattern


                       ===== all options converge =====
                                                              |
                                                              v
============================== SHARED TAIL (all options) ==============================

 [Bronze Delta table]
   parse_json -> VARIANT (DBR 15.3+, Public Preview) plus promoted columns
   (ingest_ts, source_path, business_key)
   VARIANT cannot be a partition / clustering / Z-order key, nor used in compare/group/order,
   so promote any key you filter, join or cluster on into a typed column
   VARIANT caps records at 16 MB; malformed or oversized records land in corruptRecordColumn
   under PERMISSIVE mode; whole-record VARIANT disables schema evolution and rescuedDataColumn
```

## Deliverable 2: step and option table

| Design step | Associated technical elements | Benefits | Tradeoffs | When to use | When not to use | Sources |
|---|---|---|---|---|---|---|
| 1. Extract from SaaS source | External extractor app, SaaS REST client, emits JSON files | Decoupled from Databricks, any runtime, owns SaaS auth and pagination | You build and operate it, scheduling and retry are yours, no native exactly-once | Source is a SaaS API with no managed connector, or custom logic needed | A Lakeflow managed connector already covers the source | [9] |
| 2. Land file to ADLS Gen2 | ADLS Gen2 (HNS), abfss driver, CreateFile + FlushWithClose, unique filenames, cloudFiles.cleanSource (DBR 16.4 LTS+) | Durable landing, FlushWithClose gives a clean commit boundary, cleanSource caps cost and keeps discovery fast | Same-name overwrite does not retrigger, so keep unique filenames or a flag file; uncleaned file build-up slows discovery | Always, this is the raw landing zone for the pattern | Extraction can write straight to a managed table via a connector | [1][3][10] |
| 3. Emit event (ADLS to Event Grid) | Event Grid system topic, Microsoft.Storage.BlobCreated, subscription filtered on FlushWithClose | Native push, no polling, decoupled subscribers | At-least-once delivery means duplicates are possible, HNS needs the FlushWithClose filter to avoid premature events | Any event-driven option | Auto Loader directory listing mode, or a managed connector | [2][3] |
| 4. Catch + ingest, A1b, Auto Loader managed file events (default path) | Auto Loader stream, useManagedFileEvents=true (automatic on DBR 18.1+), one managed queue per UC external location, reads cache, checkpoint exactly-once | Fewest moving parts, one queue per location, no extra creds, managed tuning and cleanup, default-on for new external locations | Cache hop adds latency, needs Unity Catalog, run at least every 7 days or it falls back to a full listing, 24h reconciliation scan | Most streaming workloads on a current runtime | Sub-cache latency requirements, or no Unity Catalog | [4][5][6] |
| 4. Catch + ingest, A1a, Auto Loader classic file notification (GA) | Auto Loader stream, useNotifications=true, per-stream Event Grid sub + Azure Queue Storage auto-provisioned, reads queue directly, checkpoint exactly-once | Lowest latency with no cache hop, GA, exactly-once, fine-grained control | Per-stream queue management, you grant resource-create creds, 500 notification pipelines per storage account (ADLS), more IAM | Latency-sensitive streams where the cache hop is too slow | Many streams per account, or you want the managed default | [4][6][10] |
| 4. Catch + ingest, A2, Workflows file-arrival trigger + ephemeral job | File-arrival trigger on UC volume or external location, ~1 min best-effort, starts a job, Auto Loader inside, debounce settings, uses file events when enabled | Compute runs only on arrival, good for irregular or batch arrivals, no standing cluster | ~1 min latency, per-run cluster start, no file-count limit with file events but a 50-job and 10k-file cap without, UC required, overwrite same name does not trigger, exactly-once from Auto Loader not the trigger | Sporadic or batched arrivals, cost-sensitive, no always-on stream wanted | Sub-minute latency, or continuous high throughput | [7] |
| 4. Catch + ingest, B, Azure Function to run-now | Event Grid subscription to Azure Function (push, no queue), filter api==FlushWithClose, jobs/run-now with file URL, notebook reads + MERGE, service-principal OAuth | No Unity Catalog needed, custom routing logic at the event, any language | You own and operate the Function and subscription, one run per event, idempotency is the job's responsibility, older pattern, no Auto Loader exactly-once unless added | Cannot use Unity Catalog, or need bespoke event routing to non-Databricks consumers | When an Auto Loader or Lakeflow path is available, or at high event rates | [8] |
| 5. Write to bronze as VARIANT | Delta bronze table, parse_json to VARIANT (DBR 15.3+), promoted columns (ingest_ts, source_path, business_key) | Schema-flexible semi-structured storage, replaces JSON strings, queryable | VARIANT cannot be a partition, clustering or Z-order key nor used in compare, group or order, so keys must be promoted; 16 MB record cap; feature is Public Preview | Raw semi-structured JSON with expected schema drift | A stable known relational schema, or keys that must partition or cluster | [11][12] |

## Option choice, in short

| If the driver is | Choose | Because |
|---|---|---|
| Default streaming ingest on a current runtime | A1b | Managed file events is the documented default from DBR 18.1, fewest moving parts, no extra creds |
| Latency below the cache hop | A1a | Reads the queue directly, no cache hop, GA |
| Cost on irregular or batched arrivals | A2 | Compute runs only on arrival, no standing cluster |
| No Unity Catalog | B | The only option that does not require UC, at the cost of operating a Function and owning idempotency |

## Standing checks before a production commitment

1. Confirm the target workspace runtime is DBR 18.1 or above for the automatic file-events default. On earlier runtimes set `cloudFiles.useManagedFileEvents=true` explicitly.
2. Confirm managed file events are enabled on the specific external location the streams read, or accept the default-on behaviour, and confirm the workspace is not gated behind an allowlist preview in your region.
3. Keep unique filenames or a flag file in step 2. Overwriting a file with the same name does not fire a notification or a file-arrival trigger.
4. Treat the VARIANT bronze write as Public Preview. Promote any key used for partition, clustering, filter, join, group or order into a typed column.

## Official sources

- [1] https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction
- [2] https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-event-overview
- [3] https://learn.microsoft.com/en-us/azure/event-grid/event-schema-blob-storage
- [4] https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/file-notification-mode
- [5] https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/file-events-explained
- [6] https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/file-detection-modes
- [7] https://learn.microsoft.com/en-us/azure/databricks/jobs/file-arrival-triggers
- [8] https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-events
- [9] https://learn.microsoft.com/en-us/azure/databricks/ingestion/
- [10] https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/production
- [11] https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant
- [12] https://learn.microsoft.com/en-us/azure/databricks/semi-structured/variant-json-diff
- [F] File events FAQ: https://learn.microsoft.com/azure/databricks/connect/unity-catalog/cloud-storage/file-events-faq

| Field | Value |
|---|---|
| Version | 1.0 |
| Last Updated | 2026-06-09 |
| Status | Review |
