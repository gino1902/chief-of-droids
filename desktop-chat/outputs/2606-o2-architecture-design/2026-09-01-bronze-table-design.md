# Bronze table design, dev_sandbox

| Field | Value |
|:------|:------|
| Date | 2026-09-01 |
| Status | Draft |
| Target | `dev_sandbox.bronze`, a throwaway exploration catalog |
| Storage and compute | Default storage, serverless throughout |
| Decides | Nothing. The decisions are [ADR-013](decisions/ADR-013-bronze-table-projection.md) and [ADR-014](decisions/ADR-014-bronze-write-block.md). This is their detail |
| Payload basis | All 21 sample files profiled on 2026-09-01 under `2608-o2-data-sources/` |

`dev_sandbox` is disposable by decision. Nothing here depends on the catalog name, and no promotion path, staging target or production grant is built on it.

---

## Default storage and serverless

Serverless workspace confirmed 2026-09-01, so catalogs on default storage are available.

- `CREATE CATALOG dev_sandbox` takes no location. The storage credential, access connector and external location that the dev platform sequence spends three steps on are not needed for the catalog.
- An external location is still needed later for the ADR-008 ADLS source, because serverless reaches cloud storage only through one.
- Managed volumes are supported, and uploading local files to one is a documented task, so the sandbox landing volume works.
- Classic compute cannot touch anything in default storage. Every read and write is serverless, which hardens ADR-004 rather than changing it, and leaves no escape hatch if a serverless limit bites.
- Only `Trigger.AvailableNow` and the deprecated `Trigger.Once` are supported. The design already uses the first, but it narrows ADR-005's continuous fallback to the pipeline's own continuous mode.
- A dropped managed table keeps its files for 7 days before purge, which softens the generation section's sharpest failure mode. Billing continues through it.
- Nothing outside Databricks can read the underlying files, since FileIO access and credential vending are unsupported. Bronze does not care, being silver-only under ADR-001. Gold will, and ODBC results above roughly 5 MiB fail when front-end Private Link is enabled.

This choice must not generalise quietly. `dbr-to-check.md` argues the opposite case, that a catalog should sit on storage you own so destroying a workspace cannot take the data. Default storage catalogs bind by default to the workspace that created them. For a disposable catalog that is fine. For dev, staging or production it reopens that note deliberately rather than by inheritance.

---

## Unit and naming

Per [ADR-013](decisions/ADR-013-bronze-table-projection.md).

- One bronze table per feed, each with its own Auto Loader checkpoint. Not per entity, not per producer.
- 19 tables today. 21 declared feeds, 2 inactive, meaning they land and are not ingested.
- Name derives from the filename: drop the date prefix and extension, lowercase, non-alphanumeric runs to one underscore. Stored in configuration so the name is data.
- Volume is small. Roughly 473 MB of source JSON and 116,000 records a day, the size sitting in wide nested records rather than row counts. Do not size this as a large workload.

---

## Column contract

Per [ADR-014](decisions/ADR-014-bronze-write-block.md). Five columns, the same on every table.

| Column | Type | Source |
|:-------|:-----|:-------|
| `payload` | VARIANT | The whole record, via `singleVariantColumn` |
| `_source_file` | STRING | `_metadata.file_path` |
| `_source_file_mtime` | TIMESTAMP | `_metadata.file_modification_time` |
| `_ingested_at` | TIMESTAMP | Pipeline run time |
| `_snapshot_date` | DATE | Parsed from the filename date prefix |

Why `_snapshot_date` earns its place:

- Most feeds are daily full snapshots, so bronze holds repeated copies and silver's deduplication needs an as-of date.
- Five feeds are rolling current-period extracts, not snapshots, so a closed month has exactly one copy and this column is the only thing identifying it. See the exceptions below.
- A VARIANT column cannot be a clustering key, cannot partition, and carries no min or max statistics. Without this column the tables have nothing to cluster on and ADR-007 is inoperable.
- No payload in the corpus carries an extraction date, so the filename is the only carrier.

Beyond those five, promote nothing until a measured silver query calls for it. Expectations warn rather than drop, so bronze keeps malformed records.

Layout is `CLUSTER BY AUTO` per ADR-007, with `_snapshot_date` as the initial `cluster_by` hint. Expect it to do little.

- Clustering on write fires only above 64 MB per transaction for one key, and 17 of 21 feeds land under that.
- It also needs `spark.databricks.delta.liquid.eagerClustering.streaming.enabled`, which is not among the six Spark properties serverless accepts. Pipelines have their own `spark_conf` mechanism and whether a serverless pipeline accepts this property is undocumented, so do not plan on it.
- Treat clustering on write as unavailable. Layout rests on predictive optimization running `OPTIMIZE`, which is confirmed supported on default storage.
- Automatic key selection works from query history, and one documented skip reason is a table not queried often. A bronze table read once a day sits close to that case.

---

## Table inventory

All 21 declared feeds, of which 19 become tables today. Counts and sizes are from the 2026-08-05 samples and describe one day.

| Table | Status | Subdomain | Producer | Shape | Records | Size | Personal data |
|:------|:-------|:----------|:---------|:------|--------:|-----:|:--------------|
| `analytic_bu` | inactive | hr-administration | APP | array | 378 | 0.24 MB | manager and HRBP names |
| `analytic_department` | active | hr-administration | APP | array | 190 | 0.06 MB | no |
| `analytic_entity` | inactive | hr-administration | APP | array | 37 | 0.04 MB | manager, HRBP, staff manager names |
| `analytic_service_line` | active | hr-administration | APP | array | 32 | 0.01 MB | no |
| `analytic_site` | active | hr-administration | APP | array | 30 | 0.003 MB | no |
| `analytic_society` | active | hr-administration | APP | array | 57 | 0.005 MB | no |
| `cra_bilan_cra_report` | active | project-resources | APP | array | 4,590 | 2.3 MB | uid, matricule |
| `cra_worklog` | active | project-resources | APP | array | 1,483 | 3.1 MB | uid, matricule, display name |
| `others_whoz_accreditation_report` | active | hr-talents | Whoz | array | 155 | 0.14 MB | profile and talent ids |
| `others_whoz_certification_report` | active | hr-talents | Whoz | array | 7,074 | 6.8 MB | profile and talent ids |
| `others_whoz_profile_report` | active | hr-talents | Whoz | array | 5,772 | 196.8 MB | yes |
| `others_whoz_skill_report` | active | hr-talents | Whoz | array | 7,961 | 71.0 MB | no, skill taxonomy |
| `others_whoz_talent_report` | active | hr-talents | Whoz | array | 3,278 | 30.4 MB | names, emails, address, phone, gender |
| `others_whoz_user_report` | active | hr-talents | Whoz | object map | 1 row, 3,212 entries | 8.7 MB | usernames as email |
| `perso_collab_status_report` | active | hr-administration | APP | array | 2,943 | 1.2 MB | uid, matricule, standard cost |
| `perso_leave_report` | active | hr-administration | APP | array | 5,159 | 1.5 MB | display name, departure dates |
| `perso_workers` | active | hr-administration | APP | array | 2,939 | 8.0 MB | full identity record |
| `project_ca_collab_report` | active | finance-fa&c | APP | array | 190 | 0.14 MB | uid, matricule, revenue |
| `project_financial_report` | active | finance-fa&c | APP | empty array | 0 | 5 bytes | none observed |
| `project_project_dataware_report` | active | project-master | APP | array | 132 | 0.18 MB | uid logins in `project_leader`, `project_commercial` |
| `project_projects_report` | active | project-master | APP | array | 73,434 | 143.1 MB | manager names, partly anonymised |

Verified independently on 2026-09-01:

- Every count and shape above was re-derived from the files and matches.
- All 21 files carry a UTF-8 byte order mark and are pretty-printed. 20 are top-level arrays, 1 is an object map.
- Largest record anywhere is 409,596 bytes, so no array record approaches any VARIANT cap.
- All 21 filenames share the same date-prefix form, and the naming rule yields 21 distinct names with no collision.

One thing the table cannot show. Sibling feeds disagree on scalar types for the same field. `id` and `active` are strings in four analytic feeds and integers in two, and `year` and `month` are strings in four feeds and integers in `cra_worklog`. Bronze is untouched, because VARIANT keeps both faithfully, which argues for the whole-record VARIANT. It lands on silver as the first concrete constraint on ADR-011's entity contract, and nothing records it today.

---

## Generation

One pipeline defines every table by looping the feed configuration, over two lists rather than one.

```python
from pyspark import pipelines as dp
from o2_platform.bronze import ingest

for feed in ingest.materialised_feeds(config_path):   # active or retired
    dp.create_streaming_table(name=feed.table, cluster_by=["_snapshot_date"],
                              cluster_by_auto=True)

for feed in ingest.ingesting_feeds(config_path):      # active only
    def attach(feed=feed):        # bind the loop variable, or every flow reads the last feed
        @dp.append_flow(target=feed.table)
        def _():
            return ingest.read(spark, feed, landing_root)
    attach()
```

- The split is forced, not stylistic. A dataset absent from a later run is dropped from the target schema, so a single loop over active feeds would destroy a table the moment its feed stopped being active.
- Retiring a feed removes it from the ingestion list alone, stopping the flow and keeping the table.
- Deleting a configuration row deletes the table. Default storage keeps the files 7 days, which is time to notice.
- `cluster_by_auto` is a real boolean argument on `create_streaming_table`, and the reference states it combines with `cluster_by` for the initial keys.

> ⚠️ Unverified and load-bearing. That a streaming table with no attached flow is a supported steady state whose data survives is documented nowhere. The whole retirement rule rests on it. Test before writing it down as a rule.

The feed configuration needs five columns it does not have, plus a fourth status value for retired.

| Column | Why |
|:-------|:----|
| `table` | The derived name, stored so the name is data rather than code |
| `relative_path` | Path minus the landing root, so the root is the only thing that changes at migration |
| `file_glob` | The `pathGlobFilter` pattern, since glob applies to leaf filenames only |
| `multiline` | True for every feed today, but it is a property of the file |
| `record_shape` | `array` or `object_map`, which is what routes `others_whoz_user_report` |

---

## Four feeds that break the pattern

- `others_whoz_user_report` is a JSON object keyed by user id, not an array, so it lands as one row holding one 8.7 MB VARIANT. The fix belongs upstream, so ask the producer for an array. Until then keep bronze faithful at one row per file and explode the map in silver, since inventing a grain the file does not have is the worse error.
- `project_financial_report` is an empty array. Declared active, delivers zero records, silently. Only a row-count and freshness check surfaces it, warning rather than failing per ADR-007.
- `others_whoz_profile_report` at 197 MB and `project_projects_report` at 143 MB set the memory floor, since a file is never split across micro-batches. Whether a multiline JSON file is splittable within that unit is undocumented, so plan the compute as if it is not.
- The accreditation feed's configured path points at `.../app-reports/others/` with no subfolder, unlike its five Whoz siblings. Glob applies to leaf filenames only, so the URL scope must be right. Fix the workbook.

---

## Load path, and the two swaps that follow

Files load from a Unity Catalog volume rather than SharePoint, which takes the Beta connector, the DBR 17.3 floor and ADR-009's unverified composition off the critical path while exercising the write block unchanged. The documented `singleVariantColumn` examples read from a volume path.

Lay the volume out as a mirror of the SharePoint tree under `dev_sandbox.landing`, so migration is a prefix substitution rather than a rewrite. `relative_path` never changes across the three phases.

```
/Volumes/dev_sandbox/landing/sharepoint_replica/app-reports/analytic/bu/
/Volumes/dev_sandbox/landing/sharepoint_replica/app-reports/perso/workers/
/Volumes/dev_sandbox/landing/sharepoint_replica/app-reports/others/whoz__profile_report/
```

| Phase | Landing root | Read options added |
|:------|:-------------|:-------------------|
| Sandbox | `/Volumes/dev_sandbox/landing/sharepoint_replica/` | none |
| SharePoint, ADR-009 | `https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/` | `databricks.connection` |
| ADLS Gen2, ADR-008 | `abfss://<container>@<account>.dfs.core.windows.net/` | `cloudFiles.useManagedFileEvents=true` |

Common to all three: `cloudFiles.format=json`, `multiLine=true`, `singleVariantColumn=payload`, `encoding=UTF-8`, `pathGlobFilter` from the feed row, `Trigger.availableNow`, and no `schemaLocation`, which is unnecessary when no schema inference happens.

`encoding` is explicit on purpose. All 21 files carry a BOM, the reader detects encoding from it automatically, and the vendor documents that detection as unreliable with an explicit `encoding` as the remedy. The BOM and `multiLine` interaction is documented nowhere.

> ⚠️ The single largest untested assumption here. Twenty of 21 feeds are a top-level JSON array, and the whole design assumes `multiLine=true` yields one row per array element. No Azure Databricks page states it. If it does not hold, every bronze table is one row per file and the grain of the layer is wrong. One file settles it, so settle it first.

---

## Governance

- One bronze schema, not one per producer. The schema is the permission boundary, one team owns all layers, and there are two producers. It splits when a producer needs different grants.
- Bronze is closed at grant level. `SELECT` to the pipeline principal and the engineering group, nobody else, which is what ADR-001 implies.
- Closure is a choice, not a limitation. Unity Catalog ABAC supports mask functions taking and returning VARIANT, so a single field can be redacted while the record survives, and `create_streaming_table` accepts a `row_filter` in Public Preview. An earlier version of this section argued closure was forced because a mask cannot reach inside a VARIANT. That was false.
- 16 of 21 feeds carry personal data, not the 10 previously claimed. The gap is direct identifiers, such as the names and phone in `perso_workers`, against pseudonymous ones, such as the `uid` logins in `project_project_dataware_report` that join straight back to `perso_workers`. Erasure and retention scope is 16.
- Personal data lands in the clear, contradicting ADR-010 decision 6, which says it is filtered and anonymised at the middleware. Anonymisation is selective: `projects_report` shows `customer_manager.id` as `anonymous6190` while the person feeds are fully identified. This needs the ADR-010 decision-makers rather than absorbing here.
- Retention pulls two ways. Repeated daily landings of personal data argue for a short window, and the five current-period feeds argue against, because a short window destroys closed months nothing can rebuild. Resolve deliberately. Deleting records from a streaming table with deletion vectors is a documented procedure, not a `DELETE`.
- The sandbox holds real personal data. The samples are production extracts, git-ignored for that reason. Disposable describes the catalog's lifespan, not its governance. Either apply the grants a real catalog would get, or cut the samples to a non-identifying subset before copying.

---

## Validation

Three empirical tests come first, in this order, because each can invalidate the design rather than merely fail it. They run on the workspace, not locally, and the runnable versions are in [2026-09-01-bronze-platform-tests.md](2026-09-01-bronze-platform-tests.md).

1. One file, top-level array, `multiLine=true`, `singleVariantColumn`. Does it yield one row per array element? If not, the grain of the whole layer is wrong.
2. Two tables in one pipeline, a flow on one, then the flow removed and the pipeline re-run, with a third run removing the declaration as the control. Do the table and its rows survive? If not, the retirement rule does not work.
3. `singleVariantColumn` with `databricks.connection` on one SharePoint file, which is ADR-009's own open verification. Not needed for the sandbox, needed before the SharePoint phase.

Then the standing checks.

- One table per active feed row, each with exactly the five contract columns, and no table disappears when a feed is retired.
- No table name, producer name, filename or source path appears in pipeline code. Greppable.
- Adding a feed row and redeploying creates a table with no diff outside the configuration file.
- Row count per `_snapshot_date` is non-zero for every active feed, which catches `project_financial_report` and any later silent emptying.
- Re-running over the same landing produces no new rows.
- A filename reused within a day is not reloaded at `allowOverwrites=false`, so a full-refresh regeneration must carry a new name. A producer contract item, not a platform setting.

---

## Conformance against the records

A blind derivation ran on 2026-09-01 against `decisions/` at SHA `7fce688`, per `adr-conformance/README.md`, in a process that never saw this document.

| Element | Verdict then | Now |
|:--------|:-------------|:----|
| Unit | Underspecified, admits 1, 2 or 19 tables | Closed by ADR-013 |
| Name | Gap, no record names a bronze table | Closed by ADR-013 |
| Columns | Conflict, ADR-008 says VARIANT plus promoted keys, ADR-009 says a single VARIANT | Closed by ADR-014 |
| Layout | Determined, `CLUSTER BY AUTO` | Unchanged, this design conforms |
| Production | Underspecified, the config-row-to-table step is unwritten | Closed by ADR-013 |

The durable lesson: the conflict existed because both Accepted records held the write block by reference to a document the conformance suite is not allowed to read. A record that delegates its substance outside `decisions/` is untestable however well the delegation is written.

---

## Corrections to existing records

Four claims in the ADR set are stale against documentation verified 2026-09-01.

- VARIANT is generally available, while ADR-008, ADR-009 and both lock-ins carry it as Public Preview. Standard SQL type from DBR 15.3, and 15.4 LTS or above to read or write tables with variant support enabled.
- The record cap is 128 MiB on the targeted runtime, 16 MiB only on DBR 17.1 and below, and ADR-009 sets a 17.3 LTS floor. The two documentation pages disagree, so confirm on the target runtime before relying on it.
- The pipelines module is `pyspark.pipelines`, not `dlt`. This corrects `thin-notebook-entrypoint-pattern.md` and the glossary line in `dbr-dev-tests.md`.
- `cloudFiles.cleanSource` exists from DBR 16.4, so ADR-009's manual-cleanup claim is a SharePoint connector limitation rather than a missing feature. TASK-097 turns on that distinction.

---

## Open items

- TASK-092 asked for a payload read before any format could be written, and blocked four tasks. All 21 are profiled here, so the field inventory can be written into `2607-o2-requirements/` and the dependents unblocked.
- The feed-to-entity mapping is still missing. This design does not need it, since bronze projects from feeds. It becomes blocking at silver.
- The samples bear on ADR-010 amendment A1 and TASK-093, whether anonymisation destroys the cross-producer join key. It does not here. APP carries `uid` and `matricule`, `perso_workers` carries `mail`, Whoz carries `username` as email. A sample observation, not a measured match rate, so it narrows the question rather than closing it.
- Catalog and schema naming needs its own decision. Three documents say three different things: `sqli_bronze_dev.raw`, `datawan_dev.bronze` and `dev_sandbox.bronze`. A catalog's managed location is adjustable while empty and not adjustable one table in.

---

## Sources

| Source | Bears on | Verified |
|:-------|:---------|:---------|
| [Ingest data as semi-structured variant type](https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant) | `singleVariantColumn`, volume-path example, no schema evolution, oversized records to `corruptRecordColumn` | 2026-09-01 |
| [Variant type support for Iceberg and Delta Lake](https://learn.microsoft.com/en-us/azure/databricks/tables/features/variant) | GA status, DBR floor, 128 MiB cap, no clustering key, no statistics | 2026-09-01 |
| [Develop pipeline code with Python](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/python-dev) | `pyspark.pipelines`, the `for` loop pattern, late binding, drop-on-absence | 2026-09-01 |
| [create_streaming_table](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/ldp-python-ref-streaming-table) | `cluster_by_auto` and `cluster_by`, `row_filter`, no default flow | 2026-09-01 |
| [append_flow](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/ldp-python-ref-append-flow) | The documented pairing with `create_streaming_table` | 2026-09-01 |
| [Use liquid clustering for tables](https://learn.microsoft.com/en-us/azure/databricks/tables/clustering) | `CLUSTER BY AUTO`, size thresholds, streaming eager clustering, skip reasons | 2026-09-01 |
| [Auto Loader options](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/options) | `multiLine`, `pathGlobFilter`, `allowOverwrites`, `schemaLocation`, files never split across micro-batches | 2026-09-01 |
| [Read JSON files](https://learn.microsoft.com/en-us/azure/databricks/query/formats/json) | BOM auto-detection and its documented unreliability | 2026-09-01 |
| [ABAC common patterns](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/abac/common-patterns) | VARIANT-based masking, single-field redaction | 2026-09-01 |
| [Row filters and column masks](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/filters-and-masks/) | A view cannot carry a mask, dynamic views as the alternative | 2026-09-01 |
| [Default storage in Databricks](https://learn.microsoft.com/en-us/azure/databricks/storage/default-storage) | Serverless-workspace requirement, no location on create, managed volumes, 7-day recovery, no FileIO or credential vending | 2026-09-01 |
| [Serverless compute limitations](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations) | Supported triggers, external locations required, most Spark configurations unsupported | 2026-09-01 |
| [Set Spark configuration properties](https://learn.microsoft.com/en-us/azure/databricks/spark/conf) | The six properties serverless accepts, and the pipeline `spark_conf` mechanism | 2026-09-01 |
| ADR-001, ADR-005, ADR-007, ADR-008, ADR-009, ADR-011, ADR-012, ADR-013, ADR-014 | Layer roles, pipeline separation, layout, the two ingestion paths, entity contract, tree strategy, and the two bronze records | in repo |
| 21 payload samples under `2608-o2-data-sources/` | Every count, size, shape and personal-data observation, re-derived independently | 2026-09-01 |

Version history is git. This document carries no version field.
