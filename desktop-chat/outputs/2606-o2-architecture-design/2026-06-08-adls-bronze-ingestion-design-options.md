# Event-driven ADLS Gen2 to bronze ingestion: design options

Scope: a single annotated design with the holding catch-and-ingest options (A1a, A1b, A2, B), a per-step and per-option decision table, the official documented sources, and a separately marked set of Databricks MVP community signals.

Inline tags like `[MVP-1]` point to the "Community and MVP signals" section at the end. Those signals are community or MVP commentary, not official documentation, and are listed apart from the sourced material on purpose.

Tags like `[R1]` point to the "Resolution log" section. Each `[R#]` marks a claim that has now been checked against official documentation, with the verdict and the source recorded in that section. Where a resolution refutes or corrects the original text, the original wording is kept and the correction is carried in the log, so the change is auditable.

## Deliverable 1: annotated ASCII diagram

```
============================== SHARED HEAD (all options) ==============================

 [SaaS API] --pull(REST)--> [Extractor] --write JSON--> [ADLS Gen2 landing (HNS)]
 external                   ext. app you                CreateFile + FlushWithClose, abfss://
 system                     build/operate               unique filenames (same-name overwrite
                                                         will NOT retrigger downstream) [R3 stands]
                                                         cloudFiles.cleanSource retention (DBR 16.4 LTS+)
                                                              |
                                                              | Microsoft.Storage.BlobCreated
                                                              | (Event Grid subscription filtered on FlushWithClose)
                                                              v
                                                    [Azure Event Grid system topic]
                                                    at-least-once delivery, so downstream must be idempotent
                                                              |
        [MVP-1 -> R1 CONFIRMED] from DBR 18.1 Auto Loader defaults to file events when available
                (useManagedFileEvents = if_available); file events are default-on for new
                external locations [MVP-2 -> R2 CONFIRMED]
                                                              |
                       ===== choose ONE catch + ingest option (A1a / A1b / A2 / B) =====


 --- A1a  Auto Loader stream, LEGACY file notification  (GA) -------------------------
   Event Grid sub + Azure Queue Storage provisioned PER STREAM by Auto Loader
   cloudFiles.useNotifications=true, reads the QUEUE directly, exactly-once via checkpoint
   + lowest latency (no cache hop)        - per-stream queue management, you grant create creds
   + GA, full control                     - notification limit 500 per storage account (ADLS), more IAM [R5]


 --- A1b  Auto Loader stream, MANAGED file events  [was PUBLIC PREVIEW -> R4] ----------
   ONE Databricks-managed queue per UC external location, file events service caches metadata
   cloudFiles.useManagedFileEvents=true, reads the CACHE, exactly-once via checkpoint
   listing: 24h service reconciliation scan, plus 7-day stream read-position expiry
   + 1 queue per location, no extra creds  - cache hop adds latency [R4]
   + managed tuning + cleanup, default-on  - needs UC; file events now default-on, not opt-in [R2]


 --- A2  Workflows FILE-ARRIVAL TRIGGER -> ephemeral JOB (Auto Loader inside) ---------
   trigger checks ~1 min best-effort on UC volume/external location, starts a job run
   debounce via min_time_between_triggers and wait_after_last_change, Auto Loader runs inside
   caps: file events ON no file-count limit [R6]; OFF up to 50 jobs and 10k-file location cap
   + compute only on arrival (cost)        - ~1 min latency, per-run cluster start
   + good for irregular / batch arrivals   - UC required, overwrite same name does NOT trigger [R3]
                                           - exactly-once comes from Auto Loader, NOT the trigger


 --- B  Azure FUNCTION (Event Grid trigger) -> jobs/run-now -> notebook JOB -----------
   Event Grid -> Function (push, no queue), filter api==FlushWithClose, run-now with file URL
   notebook reads file + MERGE, auth via service principal (Entra ID OAuth)
   + no Unity Catalog needed               - you own and operate Function + subscription
   + custom routing logic, any language    - 1 run per event (run-now limits, cluster start)
                                           - idempotency is YOUR job, older capture pattern


                       ===== all options converge =====
                                                              |
                                                              v
============================== SHARED TAIL (all options) ==============================

 [Bronze Delta table]
   parse_json -> VARIANT (DBR 15.3+, still PUBLIC PREVIEW) plus promoted columns [R7]
   (ingest_ts, source_path, business_key)
   VARIANT cannot be a partition / clustering / Z-order key, nor used in compare/group/order,
   so promote any key you filter, join or cluster on into a typed column
   VARIANT caps records at 16 MB; malformed or oversized records land in corruptRecordColumn
   under PERMISSIVE mode; whole-record VARIANT disables schema evolution and rescuedDataColumn [R7]
```

## Deliverable 2: step and option table

| Design step | Associated technical elements | Benefits | Tradeoffs | When to use | When not to use | Documented sources |
|---|---|---|---|---|---|---|
| 1. Extract from SaaS source | External extractor app, SaaS REST client, emits JSON files | Decoupled from Databricks, any runtime, owns SaaS auth and pagination | You build and operate it, scheduling and retry are yours, no native exactly-once | Source is a SaaS API with no managed connector, or custom logic needed | A Lakeflow managed connector already covers the source | [9] |
| 2. Land file to ADLS Gen2 | ADLS Gen2 (HNS), abfss driver, CreateFile + FlushWithClose, unique filenames, cloudFiles.cleanSource (DBR 16.4 LTS+) | Durable landing, FlushWithClose gives a clean commit boundary, cleanSource caps cost and keeps discovery fast | Same-name overwrite will not retrigger [R3], file build-up slows discovery if not cleaned | Always, this is the raw landing zone for the pattern | Extraction can write straight to a managed table via a connector | [1][3][10] |
| 3. Emit event (ADLS to Event Grid) | Event Grid system topic, Microsoft.Storage.BlobCreated, subscription filtered on FlushWithClose | Native push, no polling, decoupled subscribers | At-least-once delivery means duplicates are possible, HNS needs the FlushWithClose filter to avoid premature events | Any event-driven option (A1a, A1b, A2 with file events, B) | Auto Loader directory listing mode (no events), or a managed connector | [2][3] |
| 4. Catch + ingest, Option A1a, Auto Loader legacy file notification (GA) | Auto Loader stream, useNotifications=true, per-stream Event Grid sub + Azure Queue Storage auto-provisioned, reads queue directly, checkpoint exactly-once | Lowest latency with no cache hop, GA, exactly-once, fine-grained control | Per-stream queue management, you grant resource-create creds, 500-per-storage-account notification limit (ADLS) [R5], more IAM | Very latency-sensitive streams, or when Preview is not acceptable | Many streams per account, or you want managed setup | [4][6][10] |
| 4. Catch + ingest, Option A1b, Auto Loader managed file events (preview status resolved [R4]) | Auto Loader stream, useManagedFileEvents=true, one managed queue per UC external location, file events service caches metadata, reads cache, checkpoint exactly-once [R2] | One queue per location avoids notification limits, no extra creds, managed tuning and cleanup, Databricks default from DBR 18.1 [R1] | Cache hop adds latency, run at least every 7 days or full listing, 24h service reconciliation scan, needs UC; file events now default-on [R2][R4] | Most streaming workloads, many streams per location, want managed ops | Ultra-low latency (use A1a), or no Unity Catalog | [4][5][6][13] |
| 4. Catch + ingest, Option A2, Workflows file-arrival trigger + ephemeral job | Workflows file-arrival trigger on UC volume or external location, ~1 min best-effort, starts a job, Auto Loader inside, debounce settings, uses file events if enabled | Compute runs only on arrival (cost), good for irregular or batch arrivals, no standing cluster | ~1 min latency, per-run cluster start, caps (no file-count limit with file events [R6], 50 jobs and 10k files without), UC required, overwrite same name does not trigger [R3], exactly-once from Auto Loader not the trigger | Sporadic or batched arrivals, cost-sensitive, no always-on stream wanted | Sub-minute latency, counts beyond caps, continuous high throughput | [7] |
| 4. Catch + ingest, Option B, Azure Function to run-now | Event Grid subscription to Azure Function (push, no queue), filter api==FlushWithClose, jobs/run-now with file URL, notebook reads + MERGE, service-principal OAuth | No Unity Catalog needed, custom routing logic at the event, any language | You own and operate the Function and subscription, one run per event (run-now limits, cluster start), idempotency is the job's responsibility, older pattern, no Auto Loader exactly-once unless added | Cannot use UC, need bespoke event routing, integrate non-Databricks consumers | When an Auto Loader or Lakeflow path is available, or at high event rates | [8] |
| 5. Write to bronze as VARIANT | Delta bronze table, parse_json to VARIANT (DBR 15.3+), promoted columns (ingest_ts, source_path, business_key) | Schema-flexible semi-structured storage, replaces JSON strings, queryable | VARIANT cannot be a partition, clustering or Z-order key nor used in compare, group or order, so keys must be promoted; 16 MB record cap; still Public Preview [R7] | Raw semi-structured JSON with expected schema drift | A stable known relational schema, or keys that must partition or cluster | [11][12] |

## Resolution log

Each entry records the verdict of a claim checked against official documentation on 2026-06-09. Community and MVP signals that were resolved are restated here as confirmed, refuted, or corrected, with the official source. Source URLs are listed at the foot of this section.

| Tag | Original claim | Verdict | How it resolves |
|---|---|---|---|
| R1 | [MVP-1] newer runtimes may flip the Auto Loader default toward file notification mode | Confirmed | The official File events FAQ states that from Databricks Runtime 18.1 and above, Auto Loader automatically uses file events when available, with the default `useManagedFileEvents = if_available`. The signal is now official. Affects step 3 and step 4 (A1a, A1b). Source [F]. |
| R2 | [MVP-2] file events enabled by default on new external locations | Confirmed | The File events FAQ states file events are enabled by default on new external locations, with an explicit opt-out path. The manual "enable file events" step for A1b and for file-events-backed A2 is no longer required on new external locations. Source [F]. |
| R3 | [MVP-3] a TRIGGER ON UPDATE capability relaxes the same-name-overwrite limitation | Refuted as framed | The file-arrival-triggers page still states that overwriting an existing file with the same name does not trigger a run, confirmed by current docs and Databricks employee replies. The "TRIGGER ON UPDATE" referent is the separate Table update triggers feature (fires on Delta table updates, not blob overwrite) and does not relax the file constraint. The unique-filename requirement in step 2 stands. Sources [7][F]. |
| R4 | A1b is Public Preview, pre-GA | Corrected | Current official docs carry no Public Preview qualifier on managed file events. The File events FAQ (updated 2026-05-26) treats them as a default-on standard feature, and DBR 18.1 uses them by default. The pre-GA objection recorded against A1b is stale. Note: an allowlist-gated Public Preview was the position earlier in 2026, so confirm enablement on the target workspace before committing. Sources [4][5][F]. |
| R5 | A1a carries "per-container notification limits" | Corrected | The file-notification-mode page gives the classic ADLS notification limit as 500 per storage account, not per container. Source [4]. |
| R6 | A2 supports "up to 1000 jobs with file events" | Unverified | The file-arrival-triggers page states there is no file-count limit when file events are enabled, and a 50-job plus 10k-file cap when they are not. It does not state a 1000-job cap. The 1000 figure is not in the cited source. Locate the source or drop the number before relying on it. Source [7]. |
| R7 | Step 5 VARIANT claims (DBR 15.3+, key constraints, Public Preview) | Confirmed, with additions | The variant ingestion page confirms VARIANT JSON at DBR 15.3+, the partition/clustering/Z-order and compare/group/order constraints, and that the feature remains Public Preview. It adds two constraints worth carrying: a 16 MB per-record cap, and that malformed or oversized records land in `corruptRecordColumn` under PERMISSIVE mode, while whole-record VARIANT disables schema evolution and does not support `rescuedDataColumn`. Source [11]. |

Resolution sources (official):
- [F] File events FAQ (Azure): https://learn.microsoft.com/azure/databricks/connect/unity-catalog/cloud-storage/file-events-faq — verified via the canonical FAQ at https://docs.databricks.com/gcp/en/connect/unity-catalog/cloud-storage/file-events-faq (last updated 2026-05-26)
- [4] https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/file-notification-mode
- [5] https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/file-events-explained
- [7] https://learn.microsoft.com/en-us/azure/databricks/jobs/file-arrival-triggers
- [11] https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant

## Documented sources (official)

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
- [13] https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/

## Community and MVP signals (resolved 2026-06-09; see Resolution log)

These came from Databricks MVP and community channels. All three have now been checked against official documentation and the verdicts are recorded in the Resolution log above. They are retained here for provenance.

- [MVP-1 -> R1, confirmed] From a newer runtime (reported as DBR 18.1), Auto Loader defaults to file notification mode rather than directory listing. Confirmed by the official File events FAQ: from DBR 18.1, Auto Loader uses file events when available (`useManagedFileEvents = if_available`).
- [MVP-2 -> R2, confirmed] When a new external location is created, file events are reported to be enabled by default. Confirmed by the File events FAQ: file events are enabled by default on new external locations, with an explicit opt-out.
- [MVP-3 -> R3, refuted as framed] A `TRIGGER ON UPDATE` capability is reported as recently introduced to address same-name overwrite. The same-name-overwrite limitation still stands in current official docs. The likely referent is Table update triggers, a different, table-level feature that does not relax the file constraint.

Community sources:
- Databricks MVP article, "Databricks is event-driven" (Hubert-Dudek): https://community.databricks.com/t5/mvp-articles/databricks-is-event-driven/m-p/149517
- Databricks community thread confirming managed file notification mode in Public Preview since 2025, with a Databricks employee reply on setup: https://community.databricks.com/t5/data-engineering/implementing-adb-autoloader-with-managed-file-notification-mode/td-p/121939

## How to verify (signals now resolved)

The three signals are resolved against official docs as of 2026-06-09 (see Resolution log). The standing verification tasks before a production commitment are:

1. Confirm the target workspace runtime is DBR 18.1 or above for the automatic file-events default; on earlier runtimes set `cloudFiles.useManagedFileEvents=true` explicitly.
2. Confirm managed file events are enabled (or accept the default-on behaviour) on the specific external location the streams will read, and confirm the workspace is not gated behind an allowlist preview for your region [R4].
3. Keep the unique-filename or flag-file pattern in step 2; the same-name-overwrite limitation is not relaxed [R3].

| Field | Value |
|---|---|
| Version | 1.1 |
| Last Updated | 2026-06-09 |
| Status | Review |
