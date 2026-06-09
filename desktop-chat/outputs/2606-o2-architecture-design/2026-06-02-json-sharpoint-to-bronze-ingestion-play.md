# JSON on SharePoint to Databricks bronze, from a running manual setup

> The concrete build recipe for automating an existing, manually-ingested
> SharePoint-to-Databricks JSON flow. The specific instance of the general
> temporary-landing-zone play.
>
> ⚠️ Unverified. Treat as provisional until validated against a second instance.

## When to trigger

A PHP or cron extractor already writes timestamped JSON files to a SharePoint document library, and today those files are loaded into Databricks by hand. You want to automate ingestion into bronze as a quick win, knowing SharePoint is a temporary landing that will move to ADLS later. The recognition signal is a working-but-manual setup: the extractor runs, the files arrive, and the only missing piece is the governed, scheduled load.

Concrete examples:

- The originating session: 5 JSON files, 2 to 3 imports per day, names prefixed YYYY-MM-DD-HH-MM, some files regenerated in full and some incremental, loaded manually today.
- Any Databricks shop where a SaaS extractor parks JSON on a SharePoint library and a person runs the ingest notebook on demand.

## Why it matters

The deliverable is a governed, scheduled Databricks pipeline that replaces the manual step, reads JSON straight from SharePoint with no intermediate store, lands each record raw as a VARIANT column in bronze, and is built so the later ADLS migration swaps only the source path and the trigger. It also steers around the two wrong turns the format and the connector invite, which cost real time in the session.

## The play

### Optimal workflow

1. Confirm SharePoint is temporary, and keep it as the landing for now. Do not pre-stage to ADLS for the quick win.
2. Create a Unity Catalog SharePoint connection using OAuth machine-to-machine, scoped with Sites.Selected, read-only. Enable the connector Beta and run on Databricks Runtime 17.3 or above.
3. Confirm the file format is JSON up front. This gives one Auto Loader path and removes any CSV or Excel branching.
4. Land each record as a single VARIANT column with the singleVariantColumn option. Pre-create the bronze table as payload VARIANT plus provenance columns.
5. Enrich each row with the source filename and an ingest timestamp, then append to the bronze Delta table.
6. Run as a scheduled job, 2 to 3 times per day, with the stream in availableNow mode so it drains and stops. The schedule is the temporary stand-in for the future file-arrival trigger.
7. Route each of the files with pathGlobFilter on the name suffix. Folder-path filtering is not supported, so the name carries the routing.
8. Resolve full-refresh versus incremental files in silver, by deduplication or merge on business key plus load timestamp. Bronze stays append-only.

### Critical moves

| Move | Collapse test |
| :--- | :--- |
| Pinning the format as JSON, collapsing the earlier CSV-via-Auto-Loader plus Excel-via-COPY-INTO split into one path | Skip it and the design carries a needless dual path and a double-beta dependency |
| singleVariantColumn to VARIANT, which also removes schema evolution as a concern because the variant absorbs drift | Skip it and you fight nested-JSON schema evolution in bronze |
| Reading SharePoint directly through the UC connection, with no ADLS hop for the quick win | Skip it and you build a bridge you will delete at migration |
| availableNow scheduled run as the trigger stand-in, over a source-agnostic loader | Skip it and the ADLS migration becomes a rewrite |

### Pits to avoid

- Designing for CSV and Excel before confirming the format is JSON. This was the actual detour in the session.
- Treating VARIANT as byte-faithful. It is a normalised parsed tree, not the original bytes. Key order, insignificant whitespace, and duplicate keys are not preserved.
- The 16 MB VARIANT per-record cap, which is stricter than the connector 100 MB file cap. A single-object file between 16 and 100 MB passes the connector but is rejected by VARIANT.
- Setting multiLine wrong for the file shape. Newline-delimited JSON needs it off, a single object or array needs it on.
- Expecting a file-arrival trigger to watch SharePoint. It sees only Unity-Catalog-governed storage.
- Running a beta connector on a production path with no review date set.
- Putting cron or the connection inside a [Container: ...] label. Both are trigger or relationship metadata, not containers.

## When to use it

- The extractor already lands JSON on SharePoint and ingestion is manual today.
- A Unity Catalog workspace on DBR 17.3 or above, with the ability to register an Entra app for machine-to-machine auth.
- Files and per-record JSON sit under the size caps, and the format is confirmed JSON.
- The temporary landing is accepted, so a beta connector is tolerable for a bounded phase.

## When not to use it

- The format is not JSON, or is mixed. Re-open the format-path decision first.
- Byte-exact audit or replay is required. Land the raw bytes as a STRING column, or dual-land alongside VARIANT.
- Records exceed 16 MB. The single VARIANT column will reject them.
- SharePoint is permanent. Go to ADLS plus a file-arrival trigger now and skip the beta connector.
- The SaaS is a supported Lakeflow Connect managed connector. Ingest the SaaS directly and retire both SharePoint and the extractor.

## Expected outcome

| Promise | How to check |
| :--- | :--- |
| The manual ingestion step is replaced by a governed scheduled job | The manual run no longer exists and a scheduled job owns the load |
| Bronze holds payload VARIANT plus provenance, append-only | The table schema is payload VARIANT, source filename, ingest timestamp, and no row is mutated in place |
| The later ADLS migration changes only the load path and the trigger | A diff of the loader shows changes confined to the .load() target and the trigger configuration |

## Tradeoffs

Connector and path

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Read path | DIY Graph or ADLS bridge | Native UC SharePoint connector | Native connector, direct read, no ADLS hop |
| Replace the extractor | UC HTTP connection with http_request to call the SaaS directly | Keep the PHP extractor and SharePoint | Keep the extractor. http_request is a per-call primitive, not an ingestion source, SOAP makes it clumsy, and it re-implements extraction for thin gain |

Format and representation

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Format path | CSV plus Excel dual path | Single JSON path | Single JSON Auto Loader path |
| Raw type | Inferred struct with schema evolution | VARIANT single column | VARIANT, since there is no audit-byte need, which also makes evolution moot |
| Fidelity | Byte-exact STRING | Queryable VARIANT | VARIANT, revisit only if an audit obligation appears |

Triggering

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Trigger | Native file-arrival | Scheduled poll | Scheduled poll with availableNow, because SharePoint cannot fire the native trigger |

## On the VARIANT type

VARIANT is a single column type that holds a whole JSON-like value (object, array, scalar, or nested mix) as a parsed binary structure, queryable in place. 

Three properties matter here. It is parsed, not text: the JSON is decoded once at write time into a typed binary encoding, so the string "42" and the number 42 stay distinguishable. It is not the source file byte for byte. 

It is accessed by path, like payload:customer.id with a cast such as ::int, and those reads are cheap because the parse already happened rather than on every query. 

It is schema-flexible, so one column absorbs differing and evolving record shapes with no table change, which is why schema evolution drops out of this design. 

The caveat under Pits to avoid still holds: VARIANT is a normalised parse, not the original bytes, so it gives the document faithfully and queryably, not the file byte for byte.

## Reference implementation

One file pattern maps to one bronze table, each with its own checkpoint. Repeat the block per file, or wrap it in a loop over a list of (glob, table) pairs. The schedule and availableNow mode make this a fire-drain-stop job, not an always-on stream.

PySpark, Auto Loader streaming:

```python
from pyspark.sql.functions import col, current_timestamp

# Pre-create bronze: one VARIANT column plus provenance
spark.sql("""
  CREATE TABLE IF NOT EXISTS bronze.orders_raw (
    payload       VARIANT,
    _source_file  STRING,
    _ingested_at  TIMESTAMP
  )
""")

df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("databricks.connection", "my_sharepoint_conn")  # the UC SharePoint connection
    .option("singleVariantColumn", "payload")               # whole record into one VARIANT
    .option("pathGlobFilter", "*-orders.json")              # routes one of the files (name-only)
    .option("multiLine", "true")                            # true for one object/array per file, off for NDJSON
    .load("https://<tenant>.sharepoint.com/sites/<site>/<library>"))

out = df.select(
    col("payload"),
    col("_metadata.file_path").alias("_source_file"),
    current_timestamp().alias("_ingested_at"))

(out.writeStream
    .option("checkpointLocation", "<checkpoint-path>/orders")
    .trigger(availableNow=True)        # drain everything new since last run, then stop
    .toTable("bronze.orders_raw"))
```

SQL equivalent, for a Lakeflow declarative pipeline:

```sql
CREATE OR REFRESH STREAMING TABLE bronze.orders_raw AS
SELECT *, _metadata.file_path AS _source_file, current_timestamp() AS _ingested_at
FROM STREAM read_files(
  'https://<tenant>.sharepoint.com/sites/<site>/<library>',
  `databricks.connection` => 'my_sharepoint_conn',
  format             => 'json',
  singleVariantColumn => 'payload',
  pathGlobFilter     => '*-orders.json',
  multiLine          => true);
```

Notes:

- With singleVariantColumn there is no schema to infer, so no schemaLocation is needed. The checkpointLocation alone tracks which files have been processed.
- Set multiLine to match the file shape. Newline-delimited JSON needs it off, a single object or array per file needs it on.
- Each record must stay under the 16 MB VARIANT cap, stricter than the connector 100 MB file cap.
- Combining singleVariantColumn with databricks.connection is the logical composition but is not shown together in an official example. Test on one file before committing (see Open verification items).

## Version block

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-06-02 |
| Status | Draft |
| Pairs with | c4-sharepoint-databricks-bronze.pptx, 2026-06-02-temporary-landing-zone-bronze-ingestion-play.md |

## Open verification items carried from the session

- Combining singleVariantColumn with the databricks.connection option is the logical composition but was not found in an official example together. Confirm or test on one file before committing.
- VARIANT availability and its Auto Loader interaction assume DBR 15.3 or above for the type. The connector itself requires DBR 17.3 or above, so the higher floor governs.
- The SQL http_request function version floor came from a community source, not official docs.
