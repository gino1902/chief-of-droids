# Bronze platform tests, dev_sandbox

| Field | Value |
|:------|:------|
| Date | 2026-09-01 |
| Status | Run 2026-09-02, then a second round the same day. Both questions now answered. See Results and Round 2 |
| Runs on | The Databricks workspace, profile `o2_sandbox`, warehouse `ca24aadb34697d64` |
| Run by | gmourgues@sqli.com, 2026-09-02, serverless throughout |
| Gates | [ADR-013](decisions/ADR-013-bronze-table-projection.md) leaving Draft, and the whole layer's grain |
| Format | Follows `dbr-dev-tests.md`: what it needs, what is tested, the play, what passes, what passing means |

Two tests, both cheap, both on serverless. A third is listed last and is not needed yet.

---

## Setup, once

None of this needs creating. Checked 2026-09-02: `dev_sandbox` exists as a managed catalog owned by
`SGA-Databricks-DEV-CLUSTER-Dev_TF`, and `bronze`, `landing` and
`landing.sharepoint_replica` all exist already, owned by eadeogun@sqli.com.

- Do not run `CREATE CATALOG`. The `pbi-databricks-sandbox` repo is explicit that a catalog must not
  be invented in a shared metastore, and this one is already there.
- Read access is not automatic. This identity has no `READ VOLUME` on
  `dev_sandbox.landing.sharepoint_replica`, so a test needing files creates its own throwaway schema
  and volume rather than asking for a grant on someone else's object.
- Use a synthetic file rather than a real payload. Three records with the same structural
  properties, a pretty-printed top-level array with a UTF-8 BOM, test exactly the same thing and put
  no client data in the sandbox.
- `databricks fs cp <local> dbfs:/Volumes/...` works and is verified. `databricks fs mkdir` on the
  target directory first, since `cp` does not create it.
- Statements execute through `databricks api post /api/2.0/sql/statements` with `warehouse_id`,
  `statement` and `wait_timeout`, per the `pbi-databricks-sandbox` runbook.

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

## Results, run 2026-09-02

Both tests failed. Every object created was swept, and `dev_sandbox` was left with the four schemas
it had before.

Run in a throwaway schema `dev_sandbox.zz_grain_probe` with its own volume, not in
`dev_sandbox.bronze` and not against `dev_sandbox.landing.sharepoint_replica`, which this identity
has no READ VOLUME on. The probe file was synthetic, three records with the same structural
properties as `analytic_site`, pretty-printed array with a UTF-8 BOM, so no client data entered the
sandbox.

### Test 1 failed. `singleVariantColumn` collapses the file to one row

| Read | Rows from a 3-record array | payload shape |
|:-----|---------------------------:|:--------------|
| `multiLine=true` plus `singleVariantColumn` | 1 | `ARRAY<OBJECT<active,id,name>>` |
| `multiLine=true` alone, schema inferred | 3 | one object per row, correct |
| `multiLine=false` plus `singleVariantColumn` | 17 | one per physical line, garbage |

- Confirmed on both paths. `read_files` from SQL and `cloudFiles` inside a serverless Lakeflow
  pipeline gave the same single row, so this is the reader, not the API.
- `multiLine` is not the culprit. Without `singleVariantColumn` the array explodes correctly, so the
  collapse comes from `singleVariantColumn` treating the whole multiline file as one record.
- `multiLine=false` is worse than wrong, it is silent. Seventeen rows from a three-record file, one
  per physical line of pretty-printed JSON, with no error.
- `variant_explode(payload)` recovers the elements correctly, each as
  `OBJECT<active,id,name>`. That is the available repair.

What this breaks, in the design as written:

- Every bronze table would hold one row per file rather than one row per record.
- `others_whoz_profile_report` at 196.8 MB and `project_projects_report` at 143.1 MB both exceed the
  128 MiB VARIANT cap as a single value, so under `PERMISSIVE` they would land in
  `corruptRecordColumn` and carry no data at all. The two largest feeds fail hardest.
- The clean fix is upstream. Newline-delimited JSON, one object per line, makes `multiLine=false`
  plus `singleVariantColumn` the documented happy path with no cap exposure.
- The interim fixes both cost something. Exploding in bronze breaks byte-faithfulness and still
  passes the whole file through one VARIANT, so it does not help the two large feeds. Reading with
  schema inference and wrapping each row reintroduces the schema evolution that
  `singleVariantColumn` was chosen to avoid.

### Test 2 failed. A flowless streaming table is not a valid state

- Run A, both tables declared and both fed, completed. Both tables held their row.
- Run B, one flow removed and its `create_streaming_table` kept, failed the update outright:
  `No query found for dataset dev_sandbox.zz_grain_probe.t2_loses_flow`.
- The failure is not scoped to that dataset. The whole update failed, so under this design one
  retired feed would stop ingestion for every other feed in the pipeline.
- Run C, the dataset removed from both loops, completed. **The table survived with its row intact,
  still a `STREAMING_TABLE`.**

Run C is the surprising half and it inverts the problem.

- The documented drop-on-absence did not happen. Removing a dataset entirely left the table and its
  data in place, which is the opposite of what ADR-013's two-loop split was built to prevent.
- So the retirement mechanism may be the simple one after all: remove the feed from the
  configuration and the table stays.
- ⚠️ Do not write that as a rule yet. The pipeline was in development mode, serverless, triggered,
  and no full refresh was run. Any of those could be the reason nothing was dropped. One more run in
  production mode settles it, and that is the next test rather than a conclusion.

### What was swept

- Pipeline `zz-bronze-flowless-probe`, deleted.
- Workspace source under `/Users/gmourgues@sqli.com/zz_probe/`, deleted.
- Schema `dev_sandbox.zz_grain_probe` with its two tables and its volume, dropped cascade.
- Verified afterwards: `dev_sandbox` shows `bronze`, `default`, `information_schema`, `landing`, and
  the workspace lists no pipelines.

### Test 3 not run

Still gated on the SharePoint Beta, the Entra app registration and the permission scopes. Unchanged.

---

## Round 2, 2026-09-02, the options the first round left untested

Same throwaway-and-sweep pattern. Two files this time, the pretty-printed array the producer sends
today and a newline-delimited version of the same three records, plus a third file carrying explicit
nulls inside a nested object, which mirrors `projects_report`.

### The grain: only two routes are both correct and faithful

| Route | Rows from 3 records | Explicit nulls | Whole file through one VARIANT |
|:------|--------------------:|:---------------|:-------------------------------|
| NDJSON, `multiLine=false` plus `singleVariantColumn` | 3, correct | preserved | no |
| `singleVariantColumn` then `variant_explode` | 3, correct | preserved | yes, so the two large feeds fail |
| Schema inference then `to_variant_object(struct(* EXCEPT (_rescued_data)))` | 3, correct | preserved | no |
| Schema inference then `parse_json(to_json(struct(*)))` | 3, correct | **destroyed** | no |
| `schema => 'payload VARIANT'` | 3, but all NULL | not applicable | no |
| `schemaHints => 'payload VARIANT'` | 3, payload column empty | not applicable | no |

- The two documented alternatives I had flagged as "next thing to try" are both dead ends, and both
  fail in a way that looks like success. `schema => 'payload VARIANT'` returns the right row count
  with every payload NULL, because the records have no field called `payload`. `schemaHints` simply
  adds an empty column beside the inferred ones. A row count alone would have passed either.
- `parse_json(to_json(struct(*)))` is disqualified on fidelity. `to_json` drops null-valued fields,
  so `{"delivery_manager":{"id":null,"display_name":null}}` becomes `{"delivery_manager":{}}`.
  `projects_report` carries exactly that shape, so this route would silently alter the data.
- `to_variant_object` preserves nulls exactly. With `struct(*)` it carries a `_rescued_data` artefact
  into the payload, and `struct(* EXCEPT (_rescued_data))` removes it without naming any feed's
  columns, so the form stays generic.
- NDJSON was confirmed end to end, not just in SQL. A serverless pipeline read it through Auto Loader
  with `singleVariantColumn` and produced three rows per table.

**So the upstream ask is worth making, and the interim exists if it is refused.** NDJSON keeps
`singleVariantColumn` and needs no schema inference. The `to_variant_object` route works for all 21
feeds including the two that exceed the cap, at the cost of schema inference, a schema location and
a `_rescued_data` column to exclude.

### Retirement: drop-on-absence did not reproduce under any condition

| Condition | Removed dataset's table |
|:----------|:------------------------|
| Development mode, triggered | survived with its rows |
| Production mode, triggered | survived with its rows |
| Production mode, full refresh | survived with its rows |

- Three conditions, no drop. The documented behaviour, that a dataset omitted from a later run is
  dropped automatically from the target schema, did not occur in any of them.
- So ADR-013's two-loop split is not just invalid, it is unnecessary. A single loop over active feeds
  is correct, and retiring a feed means removing its row.
- The fourth status value is no longer needed for safety. It may still be wanted to record which
  feeds once ingested, which is a documentation choice rather than a correctness one.
- ⚠️ State the divergence rather than declaring the documentation wrong. Three conditions is not
  exhaustive, and the behaviour may be scoped to materialized views, or to a case these runs did not
  reach. What is safe to rely on is that removal is not destructive here, and the check belongs in
  the validation set so a platform change surfaces it.

### Swept

Pipelines `zz-bronze-flowless-probe` and `zz-prod-retire-probe` deleted, workspace sources under
`/Users/gmourgues@sqli.com/zz_probe/` deleted, schema `dev_sandbox.zz_grain_probe` dropped cascade
with its tables and volume. Verified: `dev_sandbox` shows its original four schemas and the workspace
lists no pipelines.

---

## Test 4, what an oversized file actually does

Not run. Moved here from the landing-audit handover, because it is a sandbox test rather than an
audit of the landing zone.

**Why it matters.** It decides whether an oversized read is a loss you can detect or one you cannot.
`whoz_profile_report` at 196.8 MB and `projects_report` at 143.1 MB exceed the 128 MiB cap when the
whole file becomes one VARIANT. No individual record is near the cap, the largest in the corpus is
410 KB, so this bites the file and not the record.

**Only under a rejected route.** `singleVariantColumn` with `multiLine=true`, and the
`variant_explode` repair built on it. Neither surviving route, NDJSON or `to_variant_object`, has any
cap exposure. So this is worth knowing and is not on the critical path.

**Play.** Generate a synthetic file just over 128 MiB, a top-level array of small repeated records,
no client data. Read it with `singleVariantColumn` and `multiLine=true`.

**What to observe, in this order.**

- Does it produce a row at all, with `payload` null, or no row?
- Is there anything in the table that identifies the failure, given the target has no
  `corruptRecordColumn` declared?
- Does the Auto Loader checkpoint mark the file processed, so that a rerun after a fix skips it?

The third is the one that matters. If the file is consumed and the rows are absent, then fixing the
code does not recover the data and the file must be renamed or the checkpoint cleared.

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
