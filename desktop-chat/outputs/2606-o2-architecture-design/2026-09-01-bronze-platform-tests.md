# Bronze platform tests, dev_sandbox

| Field | Value |
|:------|:------|
| Date | 2026-09-01 |
| Status | Draft, not yet run |
| Runs on | The Databricks workspace. Nothing here can be checked locally |
| Gates | [ADR-013](decisions/ADR-013-bronze-table-projection.md) leaving Draft, and the whole layer's grain |
| Format | Follows `dbr-dev-tests.md`: what it needs, what is tested, the play, what passes, what passing means |

Two tests, both cheap, both on serverless. A third is listed last and is not needed yet.

---

## Setup, once

Needs a serverless workspace, confirmed 2026-09-01, and `CREATE CATALOG`.

```sql
CREATE CATALOG dev_sandbox;
CREATE SCHEMA dev_sandbox.bronze;
CREATE SCHEMA dev_sandbox.landing;
CREATE VOLUME dev_sandbox.landing.sharepoint_replica;
```

- No location on the catalog. That is the point of default storage.
- Then upload one small file to
  `/Volumes/dev_sandbox/landing/sharepoint_replica/app-reports/analytic/site/`.
- Use `analytic_site`, which is 30 records and 3 KB, from
  `2608-o2-data-sources/analytic/site/2026-08-05__analytic_site.json`.
- Catalog Explorer upload is the documented path. The CLI form
  `databricks fs cp <local> dbfs:/Volumes/dev_sandbox/landing/sharepoint_replica/...` should also
  work but is not verified here.

> ⚠️ That file is real personal-data-adjacent production data. `analytic_site` is only site names
> and ids, so it is the safest of the 21 to start with. Do not bulk-copy the corpus into the
> sandbox before settling the grants question in the design document's Governance section.

---

## Test 1, does a top-level array yield one row per element

The grain of 20 of the 21 feeds depends on this, and it is documented nowhere.

**Play, quickest signal first.**

```sql
SELECT count(*) AS rows
FROM read_files(
  '/Volumes/dev_sandbox/landing/sharepoint_replica/app-reports/analytic/site/',
  format => 'json',
  multiLine => true,
  singleVariantColumn => 'payload');
```

**Play, the path that actually ships.** Run in a serverless notebook.

```python
(spark.readStream.format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("multiLine", "true")
  .option("singleVariantColumn", "payload")
  .option("encoding", "UTF-8")
  .load("/Volumes/dev_sandbox/landing/sharepoint_replica/app-reports/analytic/site/")
  .writeStream
  .option("checkpointLocation", "/Volumes/dev_sandbox/landing/sharepoint_replica/_ckpt/t1")
  .trigger(availableNow=True)
  .toTable("dev_sandbox.bronze.t1_grain_probe")
  .awaitTermination())
```

```sql
SELECT count(*) AS rows,
       payload:id  AS sample_id,
       payload:name AS sample_name
FROM dev_sandbox.bronze.t1_grain_probe
GROUP BY ALL LIMIT 5;
```

**Pass.** 30 rows, and `sample_id` and `sample_name` return scalar values.

**Fail.** 1 row, with `payload` holding the whole array. `payload:id` returns null because the root
is an array rather than an object.

**What passing means.** The grain assumption holds and the design stands as written. It also
settles two side questions in the same run, since a BOM did not break the read and
`singleVariantColumn` works from a volume path as documented.

**What failing means.** Every bronze table is one row per file. Silver must explode all 19. Worse,
`whoz_profile_report` at 196.8 MB and `projects_report` at 143.1 MB both exceed the 128 MiB VARIANT
cap, so under `PERMISSIVE` they land in `corruptRecordColumn` and those two feeds carry no data at
all. Stop and redesign the read before building anything else.

**If it fails, the next thing to try** is dropping `singleVariantColumn` and using
`.schema("payload VARIANT")` instead, which the variant page documents as the alternative form.

---

## Test 2, does a streaming table survive losing its flow

ADR-013's retirement rule depends on this, and it is documented nowhere. Three runs, because the
third is the control that makes the first two mean something.

**Run A, both tables fed.** Pipeline source file, serverless, target `dev_sandbox.bronze`.

```python
from pyspark import pipelines as dp

for name in ["t2_keeps_flow", "t2_loses_flow"]:
    dp.create_streaming_table(name=name)

for name in ["t2_keeps_flow", "t2_loses_flow"]:
    def attach(target=name):
        @dp.append_flow(target=target)
        def _():
            return (spark.readStream.format("cloudFiles")
                    .option("cloudFiles.format", "json")
                    .option("multiLine", "true")
                    .option("singleVariantColumn", "payload")
                    .option("encoding", "UTF-8")
                    .load("/Volumes/dev_sandbox/landing/sharepoint_replica/app-reports/analytic/site/"))
    attach()
```

Then confirm both tables hold rows.

**Run B, the flow removed, the table kept.** Edit the second loop to iterate
`["t2_keeps_flow"]` only. Leave the first loop untouched, so `t2_loses_flow` is still declared by
`create_streaming_table`. Re-run the pipeline.

```sql
SELECT count(*) FROM dev_sandbox.bronze.t2_loses_flow;
```

**Run C, the control.** Now remove `t2_loses_flow` from the first loop as well, so nothing declares
it. Re-run.

**Pass.** Run B leaves the table present with its row count unchanged, and Run C drops it.

**Fail.** Run B drops the table, or empties it.

**What passing means.** The two-loop split works, retiring a feed is safe, and the fourth status
value is worth adding to the workbook. ADR-013 can lose its warning and move toward Accepted. Run C
passing is what proves the persistence in Run B came from the create call rather than from nothing
being dropped at all.

**What failing means.** There is no safe retirement mechanism in the declarative pipeline, and
retiring a feed would destroy its history. For the five current-period feeds that loss is
irreversible, since a closed month exists in exactly one landing. ADR-013's projection section needs
reopening, and the fallback to evaluate is moving retired feeds out of the pipeline and keeping
their tables outside it.

---

## Test 3, the SharePoint composition

Not needed for the sandbox and not cheap. Listed so it is not forgotten.

- Tests `singleVariantColumn` combined with `databricks.connection` in one read, which is ADR-009's
  own open verification and blocks that record's promotion from Draft.
- Needs the SharePoint Beta enabled on the workspace, a DBR 17.3 LTS floor, an Entra app
  registration with OAuth M2M, and `Sites.Selected` or `Sites.Read.All`.
- That is other people and their lead times, which is why it sits behind the first two rather than
  beside them.
- Gates the SharePoint phase only. The sandbox reads from a volume, which is the documented pattern.

---

## Cleanup

```sql
DROP TABLE IF EXISTS dev_sandbox.bronze.t1_grain_probe;
DROP TABLE IF EXISTS dev_sandbox.bronze.t2_keeps_flow;
DROP TABLE IF EXISTS dev_sandbox.bronze.t2_loses_flow;
```

Dropped managed tables on default storage keep their files for seven days before purge, and billing
continues through that window.

---

## Recording the result

Both tests answer a question carried as a warning in a record. When they run, the warning is
replaced by the outcome rather than deleted.

| Test | Warning it settles |
|:-----|:-------------------|
| 1 | The grain warning in `2026-09-01-bronze-table-design.md`, Load path section |
| 2 | The retirement warning in ADR-013, Validation section, and the matching one in the design document |

Version history is git. This document carries no version field.
