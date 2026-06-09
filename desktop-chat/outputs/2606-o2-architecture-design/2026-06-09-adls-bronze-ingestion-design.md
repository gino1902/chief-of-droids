# Event-driven ADLS Gen2 to bronze ingestion: design

Scope: an event-driven pattern that lands JSON from a SaaS source into ADLS Gen2 and ingests it into a bronze Delta table. The pattern has a shared head, four interchangeable catch-and-ingest options (A1a, A1b, A2, B), and a shared tail. A per-option decision table and the official sources follow.

All version-sensitive claims here are checked against current Azure Databricks documentation (June 2026). Two facts shape the option choice and are stated once up front:

- From Databricks Runtime 18.1, Auto Loader uses managed file events automatically when they are available (`useManagedFileEvents = if_available`). On earlier runtimes you set the option explicitly. This automatic behaviour is documented in the File events FAQ [F]. The file-events-explained [5] and file-notification-mode [4] pages still describe setting `useManagedFileEvents=true` explicitly and have not been updated to mention the default, so do not rely on those pages to confirm it.
- File events are enabled by default on new Unity Catalog external locations, with an explicit opt-out (`enable_file_events=false`). Enabling them is no longer a manual prerequisite for new locations.

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
   scope each stream to a per-subpath UC volume, not the bare external location, to avoid
   Too many requests rate limiting on the file events service
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
   set the trigger on a per-subpath UC volume, not the external-location root, or extraneous
   root-level changes can push the trigger into a time-out error state
   + compute only on arrival (cost)         - ~1 min latency, per-run cluster start
   + good for irregular / batch arrivals    - UC required, overwrite same name does NOT trigger
                                            - exactly-once comes from Auto Loader, NOT the trigger


 --- B  Azure FUNCTION (Event Grid trigger) -> jobs/run-now -> notebook JOB -----------
   Event Grid -> Function (push, no queue), filter api==FlushWithClose, run-now with file URL
   run-now call authenticates with a PAT or OAuth token; notebook reads file + MERGE,
   storage read auth via service principal (Entra ID OAuth)
   + no Unity Catalog needed                - you own and operate Function + subscription
   + custom routing logic, any language     - 1 run per event (run-now limits, cluster start)
                                            - idempotency is YOUR job, older capture pattern


                       ===== all options converge =====
                                                              |
                                                              v
============================== SHARED TAIL (all options) ==============================

 [Bronze Delta table]
   whole-record VARIANT (DBR 15.3+, Public Preview) plus promoted columns
   (ingest_ts, source_path, business_key)
   expression depends on the ingest option: Auto Loader whole-record ingest uses the
   singleVariantColumn option; parse_json is the SQL / INSERT path. Match the expression
   to the chosen option so the tail stays consistent
   VARIANT cannot be a partition / clustering / Z-order key, nor used in compare/group/order,
   so promote any key you filter, join or cluster on into a typed column
   VARIANT path access is CASE-SENSITIVE (col:Field is not col:field), unlike JSON-string access
   VARIANT caps records at 16 MB; malformed or oversized records land in corruptRecordColumn
   under PERMISSIVE mode; whole-record VARIANT disables schema evolution and rescuedDataColumn
```

## Deliverable 2: step and option table

| Design step | Associated technical elements | Benefits | Tradeoffs | When to use | When not to use | Sources |
|---|---|---|---|---|---|---|
| 1. Extract from SaaS source | External extractor app, SaaS REST client, emits JSON files | Decoupled from Databricks, any runtime, owns SaaS auth and pagination | You build and operate it, scheduling and retry are yours, no native exactly-once | Source is a SaaS API with no managed connector, or custom logic needed | A Lakeflow managed connector already covers the source | [9] |
| 2. Land file to ADLS Gen2 | ADLS Gen2 (HNS), abfss driver, CreateFile + FlushWithClose, unique filenames, cloudFiles.cleanSource (DBR 16.4 LTS+) | Durable landing, FlushWithClose gives a clean commit boundary, cleanSource (16.4 LTS+) caps source-directory storage cost and manages retention | Same-name overwrite does not retrigger, so keep unique filenames or a flag file. On the file-events paths (A1b, A2) discovery is incremental, so cleanSource is a storage-cost lever rather than a discovery-speed one. The fast-discovery benefit applies only to the directory-listing path | Always, this is the raw landing zone for the pattern | Extraction can write straight to a managed table via a connector | [1][3][10] |
| 3. Emit event (ADLS to Event Grid) | Event Grid system topic, Microsoft.Storage.BlobCreated, subscription filtered on FlushWithClose | Native push, no polling, decoupled subscribers | At-least-once delivery means duplicates are possible, HNS needs the FlushWithClose filter to avoid premature events | Any event-driven option | Auto Loader directory listing mode, or a managed connector | [2][3] |
| 4. Catch + ingest, A1b, Auto Loader managed file events (default path) | Auto Loader stream, useManagedFileEvents=true (automatic on DBR 18.1+), one managed queue per UC external location, reads cache, checkpoint exactly-once | Fewest moving parts, one queue per location, no extra creds, managed tuning and cleanup, default-on for new external locations | Cache hop adds latency, needs Unity Catalog, run at least every 7 days or it falls back to a full listing, 24h reconciliation scan, scope each stream to a per-subpath UC volume to avoid Too many requests rate limiting | Most streaming workloads on a current runtime | Sub-cache latency requirements, or no Unity Catalog | [4][5][6] |
| 4. Catch + ingest, A1a, Auto Loader classic file notification (GA) | Auto Loader stream, useNotifications=true, per-stream Event Grid sub + Azure Queue Storage auto-provisioned, reads queue directly, checkpoint exactly-once | Lowest latency with no cache hop, GA, exactly-once, fine-grained control | Per-stream queue management, you grant resource-create creds, 500 notification pipelines per storage account (ADLS), more IAM | Latency-sensitive streams where the cache hop is too slow | Many streams per account, or you want the managed default | [4][6][10] |
| 4. Catch + ingest, A2, Workflows file-arrival trigger + ephemeral job | File-arrival trigger on UC volume or external location, ~1 min best-effort, starts a job, Auto Loader inside, debounce settings, uses file events when enabled | Compute runs only on arrival, good for irregular or batch arrivals, no standing cluster | ~1 min latency, per-run cluster start, no file-count limit with file events but a 50-job and 10k-file cap without, UC required, overwrite same name does not trigger, exactly-once from Auto Loader not the trigger, set the trigger on a per-subpath volume to avoid time-outs from root-level changes | Sporadic or batched arrivals, cost-sensitive, no always-on stream wanted | Sub-minute latency, or continuous high throughput | [7] |
| 4. Catch + ingest, B, Azure Function to run-now | Event Grid subscription to Azure Function (push, no queue), filter api==FlushWithClose, jobs/run-now with file URL, run-now auth via PAT or OAuth token, notebook reads + MERGE with service-principal OAuth | No Unity Catalog needed, custom routing logic at the event, any language | You own and operate the Function and subscription, one run per event, idempotency is the job's responsibility, older pattern, no Auto Loader exactly-once unless added | Cannot use Unity Catalog, or need bespoke event routing to non-Databricks consumers | When an Auto Loader or Lakeflow path is available, or at high event rates | [8] |
| 5. Write to bronze as VARIANT | Delta bronze table, whole-record VARIANT (DBR 15.3+) via singleVariantColumn for Auto Loader or parse_json for SQL / INSERT, promoted columns (ingest_ts, source_path, business_key) | Schema-flexible semi-structured storage, replaces JSON strings, queryable | VARIANT cannot be a partition, clustering or Z-order key nor used in compare, group or order, so keys must be promoted. VARIANT path access is case-sensitive (col:Field is not col:field), unlike JSON-string access, so queries ported from JSON strings can silently miss fields. 16 MB record cap. Feature is Public Preview | Raw semi-structured JSON with expected schema drift | A stable known relational schema, or keys that must partition or cluster | [11][12] |

## Option choice, in short

| If the driver is | Choose | Because |
|---|---|---|
| Default streaming ingest on a current runtime | A1b | Managed file events is the documented default from DBR 18.1, fewest moving parts, no extra creds |
| Latency below the cache hop | A1a | Reads the queue directly, no cache hop, GA |
| Cost on irregular or batched arrivals | A2 | Compute runs only on arrival, no standing cluster |
| No Unity Catalog | B | The only option that does not require UC, at the cost of operating a Function and owning idempotency |

## Standing checks before a production commitment

Items 1 to 6 are runtime and ingestion checks. Items 7 to 11 are the storage and integrity security baseline, which sits in the shared head and applies to every option equally regardless of the option chosen.

1. Confirm the target workspace runtime is DBR 18.1 or above for the automatic file-events default. On earlier runtimes set `cloudFiles.useManagedFileEvents=true` explicitly. The automatic `if_available` behaviour is documented in the File events FAQ [F], not in the file-events-explained or file-notification-mode pages, so verify against the FAQ.
2. Confirm managed file events are enabled on the specific external location the streams read, or accept the default-on behaviour, and confirm the workspace is not gated behind an allowlist preview in your region.
3. Keep unique filenames or a flag file in step 2. Overwriting a file with the same name does not fire a notification or a file-arrival trigger.
4. Treat the VARIANT bronze write as Public Preview. Promote any key used for partition, clustering, filter, join, group or order into a typed column. VARIANT path access is case-sensitive, so match field casing exactly when promoting or querying, and audit any query ported from JSON strings.
5. For A1b and A2, scope file discovery to a per-subpath Unity Catalog volume rather than the bare external location. For A1b this avoids the Too many requests rate limit on the file events service when several streams read different subpaths under one location. For A2 it avoids the trigger timing out on extraneous root-level changes.
6. If a data-completeness SLA applies, set `cloudFiles.backfillInterval` to trigger periodic backfills against rare missed notifications. The 24h reconciliation scan and cleanSource do not by themselves guarantee completeness, and backfills do not cause duplicates.
7. Lock write access to the landing zone to the extractor identity alone, so no other principal can land a file in the first place.
8. Put the storage account on a private network, no public access, with firewall rules and private endpoints.
9. Enforce encryption at rest, platform or customer-managed keys, and in transit.
10. Validate content before the MERGE into bronze, schema and contract checks, size and type limits, and quarantine anomalies. Treat unstructured or binary uploads as untrusted.
11. Trigger ingestion only on the real commit event (FlushWithClose) from the trusted account, so a forged or premature event cannot inject data.

## Appendix: reusable option selection criteria

These criteria are for choosing a catch-and-ingest option for future sources, not only the present one. They are option-agnostic. Each new source weights them against its own needs at selection time, so no fixed weighting or winner is encoded here. Weights below are default platform weights on a 1 to 5 scale (5 high, 3 medium, 2 low), a starting point a source can override.

Two preconditions sit above the scoring. The platform mandates Unity Catalog governance, so an out-of-UC path is admissible only by explicit exception. And the storage and integrity security baseline in standing checks 7 to 11 applies to every option equally, so it is not scored here.

| # | Criterion | Definition | Weight | Why it matters |
|---|---|---|---|---|
| 1 | Compute cost impact | What the option's compute pattern costs, mainly how much idle time it bills, always-on, only on arrival, or once per event | 5 | Compute is usually the largest line in an ingestion bill. Whether a design burns it all the time or only when data arrives sets the running cost, so the choice has a direct and visible budget effect |
| 2 | Latency, event to bronze | Time from the FlushWithClose commit on the landing file to the record being queryable in bronze | 3 | How quickly landed data becomes queryable is a freshness promise to consumers. Some uses need it within seconds, others are fine with minutes, and paying for speed nobody uses is waste |
| 3 | Scale ceiling and per-account or per-location limits | The hard limits an option hits as source count grows, such as notification pipelines per storage account or queues per external location | 3 | A platform keeps adding sources. Some designs meet hard ceilings as the number of streams grows, and a ceiling reached in production becomes an outage or an urgent re-architecture, so headroom has to be known up front |
| 4 | Operational ownership | Everything the team has to build, run, tune, credential and monitor for the option to keep working | 5 | Every component a team builds has to be patched, credentialed, monitored and supported for years. Across many pipelines this running effort, not the initial build, is what decides reliability and total cost |
| 5 | Ingestion guarantee | How far an unattended run can be trusted to finish correctly, once and resumable on restart, rather than leaving correctness to code the team writes | 5 | An automated pipeline is only trustworthy if it finishes correctly on its own, without losing or duplicating records and without someone watching it. The less a team has to hand-build that safety, the lower the risk of silent data errors |
| 6 | Maturity and longevity | The option's support status, GA, default-on but still flagged preview, or documented legacy, read as deprecation risk | 3 | A choice made now is inherited by every future source. Building on a current, supported path avoids forced migrations later, and building on one being wound down stores up rework |
| 7 | Source format coverage | Whether the option can read the source format, including unstructured or binary content like documents, images and media, or formats that need parsing Auto Loader's readers do not provide | 2 | Sources do not all arrive as clean tables. Some send documents, images or other unstructured content, and the design has to take in whatever a source produces or that source cannot be onboarded |
| 8 | Security surface and access governance | The marginal security exposure the catch-and-ingest choice adds on top of the platform baseline, the identity and credential model it uses, any self-operated component it introduces to harden and patch, and whether it keeps ingestion inside the platform's governed access, lineage and audit. Excludes the storage and network baseline, which is fixed in the shared head | 5 | Every credential and self-run component an ingestion path adds is one more thing to secure, rotate and patch, and one more way in if it is neglected. Keeping ingestion inside the governed plane means it inherits central access control and audit instead of becoming something separate to police. The wider questions, who can write to the landing zone, encryption, network isolation and whether a landed file is malicious or poisoned, are just as real, but the catch-and-ingest choice does not change them |
| 9 | GDPR and data protection | How well the option supports data-subject obligations, PII classification, lineage for erasure and access requests, retention and residency | 3 | Personal data carries legal duties, classifying it, tracing where it went, deleting it on request and keeping it in the right region. The design has to support those duties so the platform can answer a regulator or a data-subject request without manual digging |

## Concept definitions

Definitions for the terms used across the diagram and tables, grouped by where they sit in the flow. Each definition is grounded in the official source carrying the same `[n]` reference as the Official sources list below. These are reference definitions, not configuration steps.

### Storage and landing

Azure Data Lake Storage Gen2 (ADLS Gen2) is not a separate service or account type. It is a set of big-data capabilities layered on an Azure Storage account, unlocked by enabling the hierarchical namespace setting on Blob Storage. Data still persists as blobs, so Blob Storage features such as access tiers and lifecycle policies remain available [1].

Hierarchical namespace (HNS) is the account setting that organises objects into a true directory tree rather than a flat blob namespace. It makes directory operations such as rename or delete single atomic metadata operations instead of per-object enumerations, and it is the prerequisite for Data Lake Storage Gen2 file-system semantics and for the Gen2 event set [1][3].

ABFS driver, addressed by the `abfss://` scheme, is the Azure Blob File System driver. It is the HDFS-compatible access layer that lets Spark and other Hadoop-ecosystem frameworks read and write ADLS Gen2 directly, surfaced through the `dfs.core.windows.net` endpoint [1].

CreateFile and FlushWithClose are the two Data Lake Storage Gen2 REST operations that bracket a write on an HNS account. `CreateFile` opens the file and `FlushWithClose` commits it. On an HNS account a `Microsoft.Storage.BlobCreated` event is raised for both, so filtering the subscription on `FlushWithClose` is what restricts downstream triggering to fully committed files [3].

### Eventing

Azure Event Grid system topic is the managed publisher that a Storage account uses to emit blob and Data Lake events. Subscribers (a queue, an Azure Function, a webhook) attach event subscriptions to it, giving push delivery with no polling. General-purpose v1 accounts do not support Event Grid integration [2][3].

Microsoft.Storage.BlobCreated is the event raised when a blob is created or replaced. On an HNS account it fires for the `CreateFile` and `FlushWithClose` operations, so a subscription that does not filter on `FlushWithClose` will also see the premature `CreateFile` event before data is committed [2][3].

At-least-once delivery is Event Grid's delivery guarantee: every event is delivered at least once, but retries between backend nodes mean a subscriber can receive duplicates. Consumers must therefore be idempotent, and can use the `sequencer` field to order events on the same blob name [2].

### Auto Loader and file detection

Auto Loader is the Databricks incremental ingestion source (`format("cloudFiles")`) that discovers and loads new files from cloud storage with exactly-once guarantees. It supports two detection modes and you can switch between them across stream restarts without losing those guarantees [6].

Directory listing mode discovers new files by listing the input directory. It needs no notification setup beyond read access, but its discovery cost grows with directory size [6].

File notification mode discovers files from cloud notification and queue services rather than by listing, which is more performant and scalable. Databricks recommends it over directory listing for most workloads. It comes in two forms, managed file events and classic [6].

Managed file events (`cloudFiles.useManagedFileEvents=true`) is the recommended file-notification form. A single Databricks-managed service sets up one shared Event Grid subscription and queue per Unity Catalog external location, reads the notifications, and caches file metadata. Auto Loader then discovers new files by reading that cache rather than listing storage [5].

The `useManagedFileEvents = if_available` default applies from Databricks Runtime 18.1 and above: Auto Loader automatically uses managed file events when they are available on the location, with no code change. On earlier runtimes you set `cloudFiles.useManagedFileEvents` to `true` explicitly. This automatic behaviour is documented only in the File events FAQ [F].

File events cache behaviour has three timings worth knowing. On its first run, and after migration or any change that invalidates its position, a stream does a full directory listing to establish a read position in the cache. Subsequent runs read incrementally from the cache. The stored read position expires if Auto Loader is not run for more than seven days, forcing a full listing on the next run. As a safety net the service performs a full directory reconciliation listing roughly every 24 hours while at least one stream is consuming, to catch any missed notifications [5].

Classic file notification mode (`cloudFiles.useNotifications=true`) is the older form, in which Auto Loader provisions a dedicated Event Grid subscription and Azure Queue Storage queue per stream and reads that queue directly. It gives the lowest latency by avoiding the cache hop, but you manage a queue per stream, grant resource-creation credentials, and live within the limit of 500 notification pipelines per ADLS storage account [4].

Checkpoint and exactly-once: Auto Loader records its progress in a checkpoint location (kept outside the data path). The checkpoint is what lets a stream resume after a restart and process each file exactly once, independent of the detection mode. A `foreachBatch` sink, by contrast, gives only at-least-once [6][7].

Unity Catalog external location is the governed object that maps a cloud storage path to a storage credential under Unity Catalog. File events are configured on the external location, and from the FAQ they are enabled by default on new external locations, with `enable_file_events=false` as the explicit opt-out [4][F].

Unity Catalog volume is a governed storage abstraction within a catalog and schema. Databricks recommends pointing Auto Loader and file-arrival triggers at a per-subpath volume rather than the bare external location, so file discovery is scoped to the relevant objects. This is the structural fix for both the Too many requests rate limit and the trigger time-out problem [5][4].

Too many requests is the file events service rate limit, raised when several Auto Loader streams read different subpaths under one external location and the service has to iterate all objects to serve each stream. Scoping each stream to its own Unity Catalog volume resolves it [4].

`cloudFiles.backfillInterval` schedules periodic backfills so Auto Loader re-lists to catch the rare file a notification missed, which matters when a data-completeness SLA applies. Backfills do not create duplicates. The option is unsupported, and unnecessary, with managed file events, where backfill is handled automatically [4].

> ⚠️ Unverified — `cloudFiles.cleanSource` (the source-file retention and cleanup option, DBR 16.4 LTS+) was not separately fetched. Check against the Auto Loader options documentation before relying on its exact behaviour.

### Triggers and jobs

File-arrival trigger is a Databricks Jobs trigger that starts a job run when new files arrive at a Unity Catalog volume or external location. It checks on a best-effort basis about every minute and incurs no cost beyond cloud listing. It requires Unity Catalog and becomes far more scalable when the location has file events enabled. Only genuinely new files trigger a run, an overwrite with the same name does not [7].

`min_time_between_triggers` and `wait_after_last_change` are the file-arrival trigger's debounce settings. The first sets the minimum wait after a previous run completes before another can start, controlling run frequency. The second waits for a quiet period after the last file arrival, so a batch arriving together is processed as one run [7].

50-job and 10,000-file caps apply only when the location does not have file events enabled: at most 50 jobs can use a file-arrival trigger on such a location, and the monitored path can hold up to 10,000 files. With file events enabled there is no file-count limit, but a trigger on a subpath can enter a time-out error state if there is heavy extraneous change at the external-location root, which is why a dedicated per-subpath volume is recommended [7].

Azure Function (Event Grid trigger), in option B, is a self-operated push consumer. Event Grid delivers the blob event straight to the Function with no intervening queue, the Function filters on `api == FlushWithClose`, and it then calls the Databricks Jobs API to start a run. It is the only option here that needs no Unity Catalog, at the cost of you owning the Function, its subscription, and idempotency [3].

> ⚠️ Unverified — `jobs/run-now` (the Databricks Jobs REST endpoint that option B calls to start a run, with PAT or OAuth authentication) and the option B Function tutorial [8] were not fetched. Check the run-now call shape and its run-rate limits against the Databricks Jobs API documentation before building option B.

### Bronze table and VARIANT

VARIANT is the semi-structured Databricks type (Databricks Runtime 15.3 and above for JSON, in Public Preview) for storing a whole record without a fixed schema. It is a standard SQL type on Delta-backed tables and is the recommended replacement for storing semi-structured data as JSON strings [11].

`singleVariantColumn` is the Auto Loader and `COPY INTO` option that loads the entire source record into one VARIANT column. It is the whole-record ingest path used in this design's tail. `parse_json` is the SQL and DataFrame function that converts a JSON string into VARIANT, used on the INSERT or CTAS path instead [11].

PERMISSIVE mode and `corruptRecordColumn`: VARIANT cannot encode malformed records, and treats records over the 16 MB limit like corrupt records. In the default PERMISSIVE processing mode, both land in the `corruptRecordColumn` rather than failing the batch [11].

`rescuedDataColumn` disabled: because a whole-record VARIANT ingest captures the entire record in one column, no schema evolution happens during ingestion and the rescued-data column is not supported on that path [11].

VARIANT case sensitivity: all VARIANT path elements are matched case-sensitively, so `col:Field` and `col:field` address different fields. JSON-string access is case-insensitive, so a query ported from JSON strings to VARIANT can silently return nothing if the field casing does not match exactly. The `[*]` array-unpacking syntax is also unsupported, and VARIANT encodes nulls differently from JSON strings [12].

VARIANT operational limits: a VARIANT column cannot be used as a partition, clustering, or Z-order key, and cannot be used in comparison, grouping, ordering, or set operations. Any field you filter, join, group, order, or cluster on must therefore be promoted into a typed column alongside the VARIANT [11].

Promoted columns are the typed columns extracted from the record and stored next to the VARIANT (in this design `ingest_ts`, `source_path`, `business_key`). They exist because VARIANT cannot be used for the operations above, and because extracting frequently queried fields accelerates queries and improves storage layout [11].

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
| Version | 1.4 |
| Last Updated | 2026-06-10 |
| Status | Review |
