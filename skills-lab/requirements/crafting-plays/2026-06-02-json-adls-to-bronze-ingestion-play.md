# JSON on ADLS to Databricks bronze, the permanent landing design

> The build recipe for ingesting timestamped JSON files into Databricks bronze
> when the landing zone is ADLS Gen2 and permanent. The sibling of the
> SharePoint play, written for the end-state that play told you to design for.
>
> Tech-verified against official Microsoft Learn and Databricks docs on
> 2026-06-02 (variant page updated 2026-02-09, file-arrival triggers 2026-04-15,
> external locations within the prior two weeks). One standing caveat: VARIANT
> ingestion is in Public Preview. Treat that as a governance fact for a
> permanent zone, not a blocker.

## When to trigger

The same PHP or cron extractor writes timestamped JSON files, but now it writes
them to an ADLS Gen2 container that is the permanent landing, not a temporary
hop. There is no SharePoint, no migration pending, no beta connector to tolerate.
The recognition signal is a permanent file-landing pattern on governed Azure
storage, where the only missing piece is the governed, event-driven load into
bronze.

Concrete examples:

- The forward state of the originating session, after SharePoint is retired and
  the extractor repointed to ADLS.
- Any Databricks shop where an extractor parks JSON on an ADLS Gen2 container as
  a system-of-record raw zone.

## Why it matters

The deliverable is a governed, event-driven Databricks pipeline that lands each
record raw as a VARIANT column in bronze, reads JSON straight from ADLS through
a Unity Catalog External Location, and fires on file arrival rather than on a
clock. Because the landing is permanent, two design questions that the temporary
play deferred are now live and addressed here. The fidelity question (can the
original bytes be recovered) and the trigger question (event-driven over polled).

## What this design inherits and what it drops

The SharePoint play spent half its budget steering around SharePoint defects.
On a permanent ADLS target those defects and their workarounds disappear.

| From the SharePoint play | Status on ADLS |
| :---                     | :---           |
| UC SharePoint connection, OAuth M2M, Entra app, Sites.Selected | Gone. Replaced by a UC External Location backed by a storage credential (Azure managed identity via an access connector) |
| Beta connector, DBR 17.3 floor, beta-on-production review caveat | Gone. The VARIANT type floor (DBR 15.3 for JSON) now governs alone |
| `databricks.connection` reader option | Gone. The reader points at a UC Volume or an abfss path |
| `availableNow` scheduled poll as a trigger stand-in | Replaced by a native file-arrival job trigger. The stand-in is retired |
| Name-only routing because folder filtering was unsupported | Dropped. That was a SharePoint connector limit. On ADLS you route by folder or per-type volume |
| VARIANT-only, revisit audit "only if an obligation appears" | Hardened. Fidelity is decided up front because the zone is permanent |

What carries over unchanged: `singleVariantColumn` to a `payload VARIANT`,
append-only bronze, the 16 MB VARIANT per-record cap, and `multiLine` matched to
file shape. Full-refresh versus incremental is still resolved in silver.

## The play

### Optimal workflow

1. Provision the ADLS Gen2 storage account with hierarchical namespace (HNS)
   confirmed at creation. One account per environment, never shared across dev
   and prod.
2. Register the storage in Unity Catalog. Create an access connector for Azure
   Databricks (holding a system- or user-assigned managed identity), reference
   it from a storage credential, and define an External Location mapping the
   abfss path to that credential. No mount points, no connection string, no SAS
   or account key. Mark the storage credential read-only if bronze ingest is the
   only consumer of the path.
3. Grant the managed identity its storage roles. Storage Blob Data Contributor
   for reading the files. For the file-arrival trigger to use file events
   (step 6), also grant Storage Queue Data Contributor, and Storage Account
   Contributor if you want Databricks to create the queue and event subscription
   for you. Without that last role you create the storage queue and event
   subscription yourself.
4. Confirm the file format is JSON up front. One Auto Loader path, no CSV or
   Excel branching.
5. Keep the existing extractor and its file landing. Do not chase a managed
   connector unless a supported Lakeflow Connect connector covers the source SaaS,
   in which case the better move is to ingest the SaaS directly and retire both
   the extractor and the landing zone.
6. Land each record as a single VARIANT column with `singleVariantColumn`,
   targeting a pre-created bronze table. Decide the fidelity mechanism here, not
   later. See On fidelity, because `singleVariantColumn` and an in-row
   byte-faithful copy cannot both come from one read.
7. Enrich each row with the source filename and an ingest timestamp, then append
   to the bronze Delta table.
8. Trigger the load with a file-arrival trigger on the External Location or, for
   cleaner isolation, on a UC Volume mapped to the specific subdirectory.
   Enable file events on the External Location for performance and to lift the
   file-count cap. Run the stream in `availableNow` so each fired run drains and
   stops. Without file events the trigger still works on a best-effort
   one-minute poll, but a workspace is capped at fifty file-arrival jobs and the
   monitored path at ten thousand files.
9. Route one file type per monitored path. The trigger path cannot contain
   wildcards, so isolate each type in its own subdirectory or Volume rather than
   sharing one directory. Inside the read, `pathGlobFilter` is an optional
   secondary filter, not the routing mechanism it had to be on SharePoint.
10. Assume immutable, uniquely-named files. A same-name overwrite does not fire
    the trigger, and Auto Loader tracks by path so it would not reprocess that
    path anyway. The `YYYY-MM-DD-HH-MM` prefix satisfies this only if every
    regenerated file, full-refresh included, gets a new name.
11. Resolve full-refresh versus incremental files in silver, by deduplication or
    merge on business key plus load timestamp. Bronze stays append-only.

### Critical moves

| Move | Collapse test |
| :--- | :--- |
| File-arrival job trigger plus `availableNow`, started on arrival, draining since the last checkpoint, chosen over a scheduled poll and over an always-on stream | Skip it and you either poll on a clock (stale) or pay for an always-on stream (idle cost). The wiki confirms micro-batch, not real-time mode, for medallion ETL |
| Managed file events on the External Location, so Databricks creates and manages the queue and subscription given the role grants, instead of hand-wiring classic notifications | Skip it and you accept the fifty-job and ten-thousand-file caps of the listing-only trigger, or you hand-build the queue and event subscription |
| External Location over abfss with a managed identity, read-only credential, no mount or secret | Skip it and you retrofit security after provisioning, or fall back to deprecated mounts or keys |
| Decide fidelity at ingest, keeping both the in-row byte-faithful copy and the retained file, selected on the byte-context need | Skip it and a permanent raw zone cannot answer a replay or audit question it will eventually be asked, and adding the column later means a backfill |
| `singleVariantColumn` to VARIANT, which also removes schema evolution because the variant absorbs drift | Skip it and you fight nested-JSON schema evolution in bronze |
| Keep the existing extractor and file landing rather than re-implementing ingestion | Skip it and you re-engineer extraction for thin gain when no supported Lakeflow Connect connector covers the SaaS |

### Pits to avoid

- HNS not confirmed at account creation. Without it the account is not ADLS Gen2
  and you lose the capabilities this design assumes. Verify before provisioning.
- Mount points. They are deprecated platform-wide. Use the External Location.
- A single storage account across environments, which makes prod raw data
  reachable from dev.
- Assuming the file-arrival path needs no event infrastructure. File events run
  on a storage queue and an event subscription. Either grant the managed
  identity the roles for Databricks to create and manage them, or create them
  yourself. Without file events you inherit the fifty-job and ten-thousand-file
  caps.
- Routing by filename when each type can sit in its own subdirectory or Volume.
  On ADLS, folder and Volume routing is available and isolates the trigger root.
  The filename is not the routing mechanism it had to be on SharePoint.
- Treating VARIANT as byte-faithful. It is a normalised parsed tree, not the
  original bytes. Key order, insignificant whitespace, and duplicate keys are
  not preserved. This is why the design keeps a byte-faithful copy.
- Misreading the 16 MB cap as a hard reject. A record over 16 MB is treated like
  a corrupt record. In the default PERMISSIVE mode it is captured in the
  `corruptRecordColumn`, not loaded into the payload and not silently dropped.
- A same-name overwrite expecting to reload. It does not fire the trigger and
  Auto Loader does not reprocess the path. Only new file names ingest.
- Combining `singleVariantColumn` with an in-row byte-faithful STRING in one
  read. The whole record becomes the one VARIANT column, so true dual-land means
  reading text then parsing it instead. Casting the VARIANT back to a string is
  reparsed text, not the original bytes.
- Setting `multiLine` wrong for the file shape. Newline-delimited JSON needs it
  off, a single object or array per file needs it on.
- Forgetting VARIANT ingestion is in Public Preview. For a permanent
  system-of-record zone, record the preview status the same way the SharePoint
  play recorded its beta connector, and set a review point.

## On fidelity

The landing is permanent, so the fidelity decision is made here, not deferred.
Both byte-faithful mechanisms are part of this design and both stay on the
table. They answer different questions.

| Mechanism | Answers | Cost | Use when |
| :---      | :---    | :--- | :---     |
| Dual-land byte-faithful STRING beside VARIANT | Byte-context inside the same query as the parsed payload. You read the parsed value and the original text in one row, one scan | Roughly double the raw-payload storage, and it forecloses `singleVariantColumn` (see below) | Replay, audit, or debugging needs the original text co-located with the queryable value |
| Retain landed files in ADLS under a lifecycle policy, pointed to by `_source_file` | Byte-exact replay of the original file, addressable but not in-table | Landing-zone storage only, governed by the lifecycle policy | A byte-exact archive is needed but does not have to sit beside the parsed value at query time |

The discriminator to stress: the deciding need is whether byte-context is
required inside the same query as the parsed payload. If yes, the in-row STRING
earns its storage because the retained file alone cannot answer a single-scan
query. If the need is only replay or audit of the original, the retained file
under `_source_file` covers it more cheaply. This design keeps both because a
permanent system-of-record raw zone is likely to face both kinds of question
over its life, and retrofitting either one after the fact means a backfill.

A standing tension to manage: the lakehouse guiding principle of eliminating
silos and minimising copies pressures the in-row STRING. The retained landed
file is sanctioned, because raw retention is doctrine and every downstream layer
must be rebuildable from the ingest layer. The second in-row representation is
justified only where the byte-context-in-query need is real. Kept "just in
case", it becomes a redundant copy that drifts from the VARIANT in meaning over
time. Keep it where the need is concrete, otherwise let the retained file carry
replay and audit alone.

A constraint that decides the implementation: `singleVariantColumn` records the
entire record as the one VARIANT column, with no other source columns and no
schema. So you cannot capture a byte-faithful STRING in the same read that uses
`singleVariantColumn`. Casting the VARIANT back to a string gives the reparsed
text, not the original bytes. True in-row dual-land therefore means dropping
`singleVariantColumn` and instead reading the file text and parsing it (read as
text or `wholetext`, store `raw_text`, then `PARSE_JSON(raw_text)` into
`payload`). If you keep `singleVariantColumn` for simplicity, the retained
landed file is your only byte-faithful source. Pick one before locking the
bronze schema.

VARIANT remains the query surface in all cases. It is parsed once at write time
into a typed binary encoding, accessed by path like `payload:customer.id::int`,
and schema-flexible so one column absorbs evolving record shapes with no table
change. It gives the document faithfully and queryably, not the file byte for
byte.

## When to use it

- The extractor lands JSON on a permanent ADLS Gen2 container and ingestion into
  bronze is the missing step.
- A Unity Catalog workspace with an External Location and a storage credential
  backed by a managed identity.
- The runtime meets the VARIANT type floor (DBR 15.3 and above for JSON) and you
  accept the Public Preview status of VARIANT ingestion.
- Files arrive under new names each run, and per-record JSON sits under the
  16 MB VARIANT cap, format confirmed JSON.

## When not to use it

- The format is not JSON, or is mixed. Re-open the format-path decision first.
- Records exceed 16 MB. They land in the corrupt-record column rather than the
  payload. Split records upstream or store the STRING copy only.
- Files are regenerated under the same name. File-arrival plus Auto Loader will
  not reload them. Switch to a name-versioning scheme upstream first.
- The SaaS is covered by a supported Lakeflow Connect managed connector. Ingest
  the SaaS directly and retire both the landing zone and the extractor. (For
  this instance the SaaS is not covered, so the extractor and file landing
  stay.)
- Latency must be sub-minute and steady. A file-arrival trigger checks on a
  best-effort one-minute interval. For lower latency, move to a continuous
  stream and accept the always-on cluster.

## Expected outcome

| Promise | How to check |
| :--- | :--- |
| Bronze loads on file arrival, not on a clock, with no idle compute between drops | The job has a file-arrival trigger on the External Location or Volume with file events enabled, no cron schedule, and no cluster runs between arrivals |
| Every produced file is ingested once | File names are unique per run, and the Auto Loader checkpoint lists every produced file as processed with none skipped |
| Oversized records are surfaced, not lost | The `corruptRecordColumn` is monitored, and any record over 16 MB appears there rather than vanishing from the payload |
| Bronze holds payload VARIANT plus provenance, append-only, with a byte-faithful copy where the byte-context need is real | The table schema is payload VARIANT, source filename, ingest timestamp (and raw_text STRING where dual-land was chosen), and no row is mutated in place |
| The original bytes are recoverable | Either a query returns raw_text beside payload in one scan, or the landed file is still addressable in ADLS via _source_file |
| Storage access uses no secret material | The External Location resolves through a managed identity access connector, with no SAS, key, or connection string in any notebook or job |

## Tradeoffs

Access and path

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Read path | Mount point or connection string | UC External Location, abfss via Volume or path | External Location, governed, no mount, no secret. Volume preferred for trigger isolation |
| Storage credential | Service principal or SAS or key | Managed identity (access connector) | Managed identity, no secret to rotate, read-only for the ingest path |

Format and representation

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Raw type | Inferred struct with schema evolution | VARIANT single column | VARIANT, evolution drops out |
| Fidelity | VARIANT only | Byte-faithful copy kept | Both kept. In-row STRING for byte-context-in-query (foreclosing singleVariantColumn), retained file for cheap byte-exact replay |

Triggering

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Trigger | Scheduled poll | Always-on stream | File-arrival trigger plus availableNow, with managed file events. Event-driven start, no idle cluster |
| File discovery | Listing-only, no file events | Managed file events | Managed file events. Lifts the file-count and job caps, at the cost of a queue, a subscription, and the Storage Queue and Storage Account role grants |

## Reference implementation

One file type maps to one monitored path and one bronze table, each with its own
checkpoint. Isolate each type in its own subdirectory or Volume, because the
trigger path takes no wildcards. The file-arrival job trigger starts the run,
`availableNow` drains everything new since the checkpoint and stops.

Primary pattern, `singleVariantColumn`, payload plus provenance (byte-exact
replay via the retained landed file):

```python
from pyspark.sql.functions import col, current_timestamp

# Pre-create bronze: VARIANT query surface plus provenance
spark.sql("""
  CREATE TABLE IF NOT EXISTS bronze.orders_raw (
    payload       VARIANT,
    _source_file  STRING,
    _ingested_at  TIMESTAMP
  )
""")

# Prefer a UC Volume mapped to the orders subdirectory (isolates the trigger root).
# A direct abfss path also works when covered by the External Location:
#   "abfss://landing@<account>.dfs.core.windows.net/orders/"
src = "/Volumes/<catalog>/<schema>/landing/orders/"

df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("singleVariantColumn", "payload")          # whole record into one VARIANT
    .option("cloudFiles.useManagedFileEvents", "true") # uses file events; requires them enabled on the location
    .option("multiLine", "true")                        # true for one object/array per file, off for NDJSON
    .load(src))

out = df.select(
    col("payload"),
    col("_metadata.file_path").alias("_source_file"),
    current_timestamp().alias("_ingested_at"))

(out.writeStream
    .option("checkpointLocation", "/Volumes/<catalog>/<schema>/chk/orders/")
    .trigger(availableNow=True)        # drain everything new since last run, then stop
    .toTable("bronze.orders_raw"))
```

Dual-land variant, byte-faithful in-row (drops `singleVariantColumn`):

```python
from pyspark.sql.functions import col, current_timestamp, parse_json

spark.sql("""
  CREATE TABLE IF NOT EXISTS bronze.orders_raw (
    payload       VARIANT,
    raw_text      STRING,
    _source_file  STRING,
    _ingested_at  TIMESTAMP
  )
""")

# Read each file as whole text to preserve the original bytes, then parse into VARIANT.
df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "text")
    .option("wholetext", "true")
    .option("cloudFiles.useManagedFileEvents", "true")
    .load("/Volumes/<catalog>/<schema>/landing/orders/"))

out = df.select(
    parse_json(col("value")).alias("payload"),
    col("value").alias("raw_text"),
    col("_metadata.file_path").alias("_source_file"),
    current_timestamp().alias("_ingested_at"))

(out.writeStream
    .option("checkpointLocation", "/Volumes/<catalog>/<schema>/chk/orders/")
    .trigger(availableNow=True)
    .toTable("bronze.orders_raw"))
```

Notes:

- With `singleVariantColumn` there is no schema to infer, so no `schemaLocation`
  is needed. The `checkpointLocation` alone tracks which files have been
  processed. The dual-land text variant likewise needs only the checkpoint.
- `cloudFiles.useManagedFileEvents` makes Auto Loader discover files through the
  External Location's file events rather than directory listing. It requires
  file events enabled on the location. Drop it to fall back to listing, which is
  fine under the ten-thousand-file cap.
- Set the file-arrival trigger on the Databricks Job, pointing at the same
  monitored path. The trigger starts the run, the stream drains in
  `availableNow`.
- The trigger path cannot contain wildcards. Use one subdirectory or Volume per
  file type. `pathGlobFilter` can still narrow inside the read if needed.
- Each record must stay under the 16 MB VARIANT cap. Oversized records land in
  the corrupt-record column under PERMISSIVE mode.
- `_metadata.file_path` is the standard Databricks file-metadata column.

## Verification log

The play was produced in two passes. The first reformulated the SharePoint play
onto ADLS and locked the critical decisions, now carried in Critical moves
(v1.0). The second cross-checked them against the internal Azure-Databricks wiki
and tech-verified against official docs, folding the challenges and corrections
into Optimal workflow, Pits to avoid, Expected outcome, and Tradeoffs
(v1.1 to v1.5).

Sources verified on 2026-06-02:

- VARIANT type, JSON support from DBR 15.3, the 16 MB cap and corrupt-record
  behaviour, `singleVariantColumn`, and the Public Preview status. Microsoft
  Learn, Ingest data as semi-structured variant type (updated 2026-02-09).
  https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant
- File-arrival triggers, file events, the one-minute best-effort poll, the
  fifty-job and ten-thousand-file caps, the same-name overwrite behaviour, and
  the `availableNow` drain pattern. Microsoft Learn, Trigger jobs when new files
  arrive (updated 2026-04-15).
  https://learn.microsoft.com/en-us/azure/databricks/jobs/file-arrival-triggers
- External Location, storage credential, managed identity access connector, and
  the Storage Blob, Storage Queue, and Storage Account role grants. Microsoft
  Learn, Manage external locations and Use Azure managed identities in Unity
  Catalog (Feb to Mar 2026).
  https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/manage-external-locations
  https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/azure-managed-identities

Still to confirm or monitor:

- VARIANT ingestion leaving Public Preview. Re-check before treating the
  permanent zone as GA-backed.

## Version block

| Field | Value |
| :--- | :--- |
| Version | 1.5 |
| Last Updated | 2026-06-02 |
| Status | Draft |
| Pairs with | 2026-06-02-json-sharpoint-to-bronze-ingestion-play.md |
