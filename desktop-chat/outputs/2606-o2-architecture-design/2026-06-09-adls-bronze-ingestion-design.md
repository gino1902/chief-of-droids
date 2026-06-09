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
| Version | 1.3 |
| Last Updated | 2026-06-09 |
| Status | Review |
