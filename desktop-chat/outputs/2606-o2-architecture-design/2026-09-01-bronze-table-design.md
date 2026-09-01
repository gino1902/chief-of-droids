# Bronze table design, dev_sandbox

| Field | Value |
|:------|:------|
| Date | 2026-09-01 |
| Status | Draft |
| Scope | The shape, naming, columns and generation of bronze tables for the 21 declared O2 feeds |
| Target | `dev_sandbox.bronze`, a throwaway exploration catalog |
| Grounds on | ADR-001, ADR-005, ADR-007, ADR-008, ADR-009, ADR-011, ADR-012, and both ingestion lock-ins |
| Payload basis | All 21 sample files profiled on 2026-09-01 under `2608-o2-data-sources/` |
| Storage and compute | Default storage, serverless throughout |

`dev_sandbox` is disposable by decision. Nothing here depends on the catalog name, and no
promotion path, staging target or production grant is built on it. What is being proved is the
table shape, not the environment.

Everything is created on default storage and runs on serverless. That is a constraint on this
design rather than a choice made by it, and its consequences are gathered in the next section
because several of them reach the table design.

---

## What default storage and serverless change

Creating a catalog on default storage requires a serverless workspace. That precondition was
checked and holds, confirmed 2026-09-01. The customer-managed storage account, access connector and
external location described in the infrastructure notes are not contradicted by this, since a
serverless workspace can host catalogs on default storage and on its own cloud object storage side
by side. `dev_sandbox` takes the simpler route and `datawan_dev` can keep the other one.

The constraint simplifies more than it costs.

Catalog creation loses its hardest step. `CREATE CATALOG dev_sandbox` takes no location, and the
storage credential, access connector and external location that the dev platform sequence spends
three steps on are not needed for the catalog at all. The `CREATE MANAGED STORAGE` privilege
question disappears with them. An external location is still required later for the ADR-008 ADLS
source, because serverless reaches cloud storage only through one, so this removes a step from
catalog setup and none from the eventual migration.

Managed volumes are supported on default storage, and uploading local files to one is a documented
task, so the sandbox landing volume works as designed.

Classic compute cannot touch anything in default storage. Every read and write, by a person or a
pipeline, is serverless only. ADR-004 already decided serverless, so this hardens an existing
decision rather than changing one, but it also means there is no classic escape hatch if a
serverless limitation bites.

Two serverless limits reach this design. Only `Trigger.AvailableNow` and the deprecated
`Trigger.Once` are supported, which the design already uses, though it narrows ADR-005's continuous
fallback to the pipeline's own continuous mode rather than a continuous Structured Streaming
trigger. And serverless notebooks and jobs accept only six Spark properties, which has a
consequence for clustering recorded in the column contract.

Dropping a managed table or volume on default storage keeps the files for a seven-day recovery
window before they are purged. That is a real mitigation for the sharpest failure mode in the
generation section, where a deleted configuration row drops a table. It is a week to notice, not a
reprieve, and billing continues through it.

Two limits do not bite bronze but will be asked about later. Nothing outside Databricks can read
the underlying files of a default-storage table, since FileIO access and credential vending are
both unsupported, so external engines reach data only through ODBC, JDBC or the Files API. Bronze
is consumed only by silver under ADR-001, so this costs nothing here. It lands on gold, where the
one caveat worth carrying forward is that ODBC results above roughly 5 MiB fail when front-end
Private Link is enabled, and this platform has an open network topology question.

One thing this choice must not do is generalise quietly. `dbr-to-check.md` exists to argue the
opposite case, that a catalog should sit on storage you own with an explicit managed location and
its own IaC stack, so that destroying a workspace cannot take the data with it. Default storage
catalogs are bound by default to the workspace that created them and are reachable elsewhere only
through workspace-catalog binding and serverless compute. For a catalog that is disposable by
decision, none of that matters and the simpler route is right. For dev, staging or production it
reopens the question that note was written to settle, and it should be reopened deliberately rather
than inherited from the sandbox.

---

## What this decides

The unit of a bronze table, its name, its columns, how the 21 tables are produced from one
configuration, and how the four feeds that do not fit the pattern are handled.

## What this does not decide

Catalog and schema naming across environments, which is drifting across three documents and needs
its own record. Entity mapping, which sits in silver by ADR-011. Bundle layout, which is ADR-012.
Whether the SharePoint connector composition works, which is ADR-009's open verification.

---

## The table unit is the feed

One file pattern maps to one bronze table, each with its own Auto Loader checkpoint. That is the
SharePoint lock-in's implementation note 3, and it follows from ADR-001, where bronze is aligned
along the supply path as a structural fact rather than a semantic contract, and from ADR-011, where
the entity contract sits in silver and the producing system is configuration.

So the table count is the feed count. Nineteen active feeds give nineteen tables today. Two feeds
are inactive, `analytic_bu` and `analytic_entity`, meaning they land and are not ingested, so they
get a table when their status flips to active and not before.

The counts are small. Across all 21 samples the daily volume is roughly 473 MB of source JSON
carrying about 116,000 records. The size is in wide nested records rather than in row counts, so
this design should not be sized as if it were a large workload.

---

## Table naming

The table name is derived from the filename, mechanically, with no judgement step.

Take the filename, drop the `AAAA-MM-DD__` date prefix, drop the `.json` suffix, lowercase, and
replace every run of non-alphanumeric characters with a single underscore.

A mechanical rule is worth more than a tidy one here. Any normalisation step done by hand, such as
stripping the `others_` bucket prefix or collapsing the Whoz double underscore, is a judgement that
has to be re-made every time a feed is added, and it costs the property that matters: the mapping
from landed file to table is reversible by anyone reading either end. The `others_` prefix is an
artefact of the source folder tree, and silver ignores it.

The derived name is stored in the feed configuration rather than computed in code, so the name is
data. That keeps the rule auditable and lets a name be pinned by hand if a source folder is ever
renamed upstream.

---

## Column contract

Every bronze table carries the same five columns and nothing else.

| Column | Type | Source |
|:-------|:-----|:-------|
| `payload` | VARIANT | The whole record, via `singleVariantColumn` |
| `_source_file` | STRING | `_metadata.file_path` |
| `_source_file_mtime` | TIMESTAMP | `_metadata.file_modification_time` |
| `_ingested_at` | TIMESTAMP | `current_timestamp()` at pipeline run |
| `_snapshot_date` | DATE | Parsed from the filename date prefix |

The first four are the provenance set both lock-ins already specify. The fifth is the addition this
design makes, for three reasons.

Feeds land daily, and most are full snapshots, so an append-only bronze accumulates around thirty
copies of the same content by design. Silver's deduplication needs the as-of date, and deriving it
from the filename is deterministic where relying on ingestion time breaks on any replay or backfill.

Five feeds are not full snapshots at all, and this is the sharper reason for the column.
`cra_bilan_cra_report`, `cra_worklog`, `perso_collab_status_report`, `project_ca_collab_report` and
`project_project_dataware_report` each contain exactly one period, 2026-08, across every record.
They are rolling current-period extracts. Once a month closes, the last landing of that month is
the only copy of it that will ever exist, and no later landing can reconstruct it. For those five,
`_snapshot_date` is not a convenience for deduplication, it is the only thing that says which
closed month a row belongs to, and the retention window is not a storage decision but the line
between keeping and permanently losing closed periods.

It is also the only column that can carry the table's data layout. Documentation confirms a VARIANT
column cannot be a clustering key, cannot partition a table, and collects no `minValues` or
`maxValues` statistics, so no file skipping is possible on `payload`. Without `_snapshot_date` these
tables have nothing to cluster on at all.

Beyond those five, promote nothing. The standing checks say to promote keys used for partition,
clustering, filter, join, group or order, and at 116,000 rows a day no such key exists yet. Add a
promoted column when a measured query pattern calls for one.

Layout is `CLUSTER BY AUTO` per ADR-007, with `_snapshot_date` passed as the initial key hint via
`cluster_by`. Automatic liquid clustering requires Unity Catalog managed tables and predictive
optimization, and it is documented as supported on streaming tables in Lakeflow pipelines.

Expect it to do very little here, for reasons worth stating rather than discovering. Clustering on
write fires only above a size threshold, 64 MB per transaction for a single key on a managed table,
and for streaming workloads it also needs
`spark.databricks.delta.liquid.eagerClustering.streaming.enabled`. Seventeen of the twenty-one
feeds land under 64 MB a day, so clustering on write would not fire for them regardless.

Serverless narrows that further. Serverless notebooks and jobs accept only six Spark properties and
that is not one of them. Lakeflow pipelines have their own `spark_conf` mechanism at pipeline, flow
and table level, and whether a serverless pipeline accepts this particular property is not
documented either way, so do not plan on it. Treat clustering on write as unavailable and layout as
resting entirely on predictive optimization running `OPTIMIZE` afterwards.

Predictive optimization is confirmed as supported on default storage, so the mechanism
`CLUSTER BY AUTO` depends on is present. What remains uncertain is whether it chooses to act.
Automatic key selection works from the table's historical query workload, and one documented skip
reason is that the table is not queried often. A bronze table read once a day by one silver job
sits close to that case, so expect key selection to decline on grounds other than size.

Expectations warn rather than drop, per ADR-007. Bronze keeps everything, including malformed
records.

---

## Table inventory

All 21 declared feeds, of which 19 become tables today. Record counts and sizes are from the
2026-08-05 samples and describe one day.

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
| `others_whoz_accreditation_report` | active | hr-talents | Whoz | array | 155 | 0.14 MB | profile and talent ids, attachments |
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

Every file is a pretty-printed top-level JSON array carrying a UTF-8 byte order mark, with the one
exception noted below. So `multiLine` is `true` for all of them.

Counts and shapes above were re-derived independently from the files on 2026-09-01 and match. The
largest single record anywhere in the corpus is 409,596 bytes, in `others_whoz_profile_report`, so
no array record comes close to any VARIANT size cap and the cap only ever bears on the single
`others_whoz_user_report` row. All 21 filenames share the `2026-08-05__` prefix form, so the date
rule parses uniformly, and the naming rule applied across all 21 yields 21 distinct names with no
collision.

One thing the table cannot show. Sibling feeds disagree on scalar types for the same field. `id`
and `active` are strings in `analytic_bu`, `analytic_entity`, `analytic_site` and
`analytic_society`, and integers in `analytic_department` and `analytic_service_line`. `year` and
`month` are strings in four feeds and integers in `cra_worklog`. Bronze is untouched by this,
because VARIANT stores both faithfully, which is an argument for the whole-record VARIANT rather
than against it. It lands on silver, where it is the first concrete constraint on ADR-011's entity
contract, and nothing in the current configuration records it.

---

## Generation

One ingestion pipeline defines every bronze table in a `for` loop over the feed configuration.
Databricks documents this pattern directly, including the late-binding trap where every table ends
up loading the last value in the loop, and the two correct forms that avoid it. The loop is
evaluated in serial order, and the pipeline then runs the flows in parallel.

This is what ADR-012 asks for. A producer, a route and a filename are rows. Adding a feed is a row
and a deploy, with no code diff, and nothing about a feed appears as a directory or a function name.

The pipeline file stays thin and calls into the package, per ADR-007 and the thin-notebook pattern.

Defining the table and attaching its flow are two separate steps, and they iterate over two
different lists. This matters more than it looks, see the retirement rule below.

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

`cluster_by_auto` is a real boolean argument on `create_streaming_table`, and the reference states
it can be combined with `cluster_by` to set the initial clustering keys, which is why both appear
above.

The split exists because of one documented behaviour: if a dataset defined in a previous run is
missing from the list on a later run, the pipeline drops that table from the target schema
automatically. A single loop over active feeds would therefore destroy a table and its history the
moment a feed stopped being active, which is the opposite of what retiring a feed should do. On
default storage a dropped managed table keeps its files for a seven-day recovery window, so this is
recoverable if caught within the week, which is a mitigation rather than a reason to relax the
rule.

So the table list and the ingestion list are governed separately. A feed that has ever been ingested
stays in the table list for good, and its status controls only whether a flow reads into it.
Retiring a feed stops the flow and keeps the table and its history. Deleting the row is the only
action that destroys data, and it should be treated as such.

> ⚠️ Unverified, and load-bearing. The `create_streaming_table` plus `@dp.append_flow` pattern is
> documented and the code shape above is right. What is not documented anywhere is that a streaming
> table with no attached flow is a supported steady state whose data survives across pipeline runs.
> The nearest statement, that other targets have no default flow, confirms no flow is created
> automatically and says nothing about persistence. The whole retirement rule and the fourth status
> value rest on that inference. Test it in the sandbox before writing it down as a rule: define two
> tables, attach a flow to one, run, remove the flow, run again, and check the table and its rows
> are still there.

That needs a fourth status value. The current semantics are active, inactive and planned, where
inactive means the feed lands and is not ingested. Retired means it was ingested and no longer is,
which is a different state with a different consequence, and today nothing can express it.

The feed configuration needs five columns beyond what `o2-data-sources.xlsx` carries today.

| Column | Why |
|:-------|:----|
| `table` | The derived table name, stored so the name is data rather than code |
| `relative_path` | The source path with the landing root removed, so the root is the only thing that changes at migration |
| `file_glob` | The `pathGlobFilter` pattern, since glob applies to leaf filenames only and not to directory paths |
| `multiline` | True for every feed today, but it is a property of the file and belongs in configuration |
| `record_shape` | `array` or `object_map`, which is what routes `others_whoz_user_report` |

---

## Four feeds that break the pattern

The first is `others_whoz_user_report`, which is not an array. It is a single JSON object keyed by
user id, holding 3,212 entries in 8.7 MB. Under `singleVariantColumn` it lands as one row
containing one 8.7 MB VARIANT, which is the wrong grain. The fix belongs upstream, so ask the
producer to emit an array like its five siblings. Until then, keep bronze faithful at one row per
file and explode the map in silver, because bronze inventing a grain the file does not have would
be the worse error. Size is not the immediate risk it appears to be, see the VARIANT cap
correction below.

The second is `project_financial_report`, an empty array. It is declared active and delivers zero
records, silently. Auto Loader will create the table and never populate it. Only a row-count and
freshness check surfaces this, and under ADR-007 it warns rather than fails.

The third case is size. `others_whoz_profile_report` is 197 MB and `project_projects_report` is
143 MB. Documentation confirms a file is never split across micro-batches regardless of
`maxBytesPerTrigger`, so one file is one unit of work and these two set the memory floor for the
ingestion compute. Whether a multiline JSON file is splittable across tasks within that unit is not
documented anywhere on the substrate, so plan the compute as if it is not.

The fourth is a configuration error. `o2-data-sources.md` points the accreditation feed at
`.../app-reports/others/` with no subfolder, unlike its five Whoz siblings, while the sample sits
under `others/whoz__accreditation_report/`. Glob filtering applies to leaf filenames and not to
directory paths, so the URL scope has to be right. Fix the workbook.

---

## Load path, and the two swaps that follow

In the sandbox, files load from a Unity Catalog volume rather than from SharePoint. That takes the
Beta connector, the DBR 17.3 floor and ADR-009's unverified `singleVariantColumn` with
`databricks.connection` composition off the critical path, while exercising the exact write block
that both lock-ins say survives migration untouched. The documented `singleVariantColumn` examples
read from a volume path, so this is the paved route.

Lay the volume out as a mirror of the SharePoint tree, under `dev_sandbox.landing`:

```
/Volumes/dev_sandbox/landing/sharepoint_replica/app-reports/analytic/bu/
/Volumes/dev_sandbox/landing/sharepoint_replica/app-reports/perso/workers/
/Volumes/dev_sandbox/landing/sharepoint_replica/app-reports/others/whoz__profile_report/
```

Mirroring is what makes the migration a prefix substitution in configuration rather than a rewrite.
`relative_path` never changes across all three phases, only the root and the read options do.

| Phase | Landing root | Read options added |
|:------|:-------------|:-------------------|
| Sandbox | `/Volumes/dev_sandbox/landing/sharepoint_replica/` | none |
| SharePoint, ADR-009 | `https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/` | `databricks.connection` |
| ADLS Gen2, ADR-008 | `abfss://<container>@<account>.dfs.core.windows.net/` | `cloudFiles.useManagedFileEvents=true` |

Common to all three: `cloudFiles.format=json`, `multiLine=true`, `singleVariantColumn=payload`,
`encoding=UTF-8`, `pathGlobFilter` from the feed row, `Trigger.availableNow`, and no
`schemaLocation`, which is confirmed as unnecessary when no schema inference happens.

`encoding` is set explicitly and deliberately. All 21 files carry a UTF-8 byte order mark, and the
JSON reader detects encoding from the BOM automatically, but the vendor documents that detection as
unreliable and names an explicit `encoding` option as the remedy. The interaction between a BOM and
`multiLine` is documented nowhere, so the cheap option is to stop relying on detection.

> ⚠️ The single largest untested assumption in this design. Twenty of the twenty-one feeds are a
> top-level JSON array, and the whole design assumes that reading such a file with `multiLine=true`
> yields one row per array element. That behaviour is not stated on any Azure Databricks page
> checked. It is what Spark does, and the design is unremarkable if it holds, but if it does not,
> every bronze table is one row per file and the grain of the entire layer is wrong. It costs one
> file and one run to settle, so settle it first, before the connector composition and before
> anything else on this page.

---

## Governance

Use one bronze schema rather than one per producer. The schema is the permission boundary, one team
owns all layers, and there are two producers today. It splits when a producer needs grants the
others do not have, and that is the reopening condition.

Bronze is closed at the grant level. Grant `SELECT` to the pipeline principal and the engineering
group and to nobody else, which is what ADR-001 implies when it says bronze is consumed by silver
and not by analysts.

An earlier version of this section argued that closure was forced, on the grounds that a column
mask cannot reach a field inside a VARIANT. That is false and the correction matters. Unity Catalog
ABAC supports mask functions that take a VARIANT and return a VARIANT, branching on shape with
`schema_of_variant()` and rebuilding the object with `to_variant_object(named_struct(...))`, so a
single field can be redacted while the rest of the record survives. The documented example redacts
an email and keeps the other fields. Separately, `create_streaming_table` accepts a `row_filter`
argument in Public Preview, and dynamic views are the documented route for exposing a reshaped view
of a table to people without access to the base table, though a view cannot itself carry a mask.

So two field-level controls exist at bronze, and closure is a choice rather than a consequence.
That is a better position to be in, because it means the day someone has a legitimate reason to
read bronze, the answer is a mask rather than a refusal. It also removes the argument that fields
must be promoted out of the VARIANT to be governable.

Sixteen of the twenty-one feeds carry personal data of some kind, which is more than the ten this
section previously claimed. The gap is the difference between direct identifiers, such as the names,
email and phone in `perso_workers`, and pseudonymous ones, such as the `uid` logins that
`project_project_dataware_report` carries in `project_leader` and `project_commercial` and that join
straight back to `perso_workers`. Erasure and retention scope is sixteen, not ten, and the narrower
reading should not be doing that work silently.

Personal data lands in the clear, which contradicts ADR-010 as written. Decision 6 of that record
states personal data is filtered at the middleware with encryption and anonymisation before
landing. The samples show anonymisation is selective rather than global. `projects_report` carries
`customer_manager.id` as `anonymous6190`, while `perso_workers` carries names, email, gender,
nationality, postal code, city and phone in full, and `whoz_talent_report` carries emails, address
and phone. This needs to reach the ADR-010 decision-makers rather than being absorbed here.

Retention has to be settled before the first load, and it now pulls in two directions rather than
one. An append-only bronze of daily snapshots of personal data means an erasure request requires
rewriting history across every landing that person appears in, which argues for a short window. The
five current-period feeds argue the other way, because a window shorter than the gap between month
close and the next read destroys closed months that nothing can rebuild. Those two pressures have to
be resolved deliberately rather than by picking a default. Note also that permanently deleting
records from a streaming table with deletion vectors enabled is a documented procedure with its own
steps rather than a `DELETE`.

The sandbox holds real personal data. The 21 samples are production extracts, git-ignored for that
reason, and copying them into a volume puts real personal data into `dev_sandbox`. Disposable
describes the catalog's lifespan and says nothing about how it should be governed. Either apply the
same grants a real catalog would get, or cut the samples down to a non-identifying subset before the
copy. Take that decision deliberately, since otherwise the personal data sits in a catalog nobody is
tracking.

---

## Validation

Three empirical tests come before any of the checks below, because each one can invalidate the
design rather than merely fail it. Run them in this order, cheapest and most decisive first.

1. One file, top-level array, `multiLine=true`, `singleVariantColumn`. Does it yield one row per
   array element? If not, the grain of the whole layer is wrong.
2. Two tables in one pipeline, a flow attached to one, then the flow removed and the pipeline
   re-run. Do the table and its rows survive? If not, the retirement rule does not work.
3. `singleVariantColumn` with `databricks.connection` on one SharePoint file, which is ADR-009's
   own open verification. Not needed for the sandbox, needed before the SharePoint phase.

Each check below has an observable failure mode.

- One table exists per active feed row, every one has exactly the five contract columns and no
  others, and no table disappears when a feed is retired.
- No table name, producer name, filename or source path appears anywhere in pipeline code. This is
  greppable, and it is the compliance check ADR-012 names first.
- Adding a feed row and redeploying creates a table with no diff outside the configuration file.
- Row count per `_snapshot_date` is non-zero for every active feed, which is the check that catches
  `project_financial_report` and any later silent emptying.
- Re-running the pipeline over the same landing produces no new rows, which is the idempotency check
  the standing checks require.
- A file whose name is reused within a day is not reloaded at `allowOverwrites=false`, so a
  full-refresh regeneration must carry a new filename. That is a producer contract item, not a
  platform setting.

---

## Corrections to existing records

Four claims in the current ADR set are stale against documentation verified on 2026-09-01.

VARIANT is generally available, while ADR-008, ADR-009 and both lock-ins carry it as Public Preview.
It is a standard SQL type from Databricks Runtime 15.3, and reading or writing tables with variant
support enabled requires 15.4 LTS or above.

The record cap is 128 MiB on the runtime this platform targets. It is 16 MiB on Databricks Runtime
17.1 and below and 128 MiB above it, and ADR-009 sets a 17.3 LTS floor. The two documentation pages
disagree here, since the ingestion page still states 16 MB flatly while the table feature page
carries the version split, so confirm the cap on the target runtime before relying on it. The
oversized-record behaviour matters either way, because an oversized record lands in
`corruptRecordColumn` under `PERMISSIVE` rather than in the payload.

The pipelines module is now `pyspark.pipelines`. The `dlt` module has been replaced and Databricks
recommends `from pyspark import pipelines as dp`. This corrects the unverified warning in
`thin-notebook-entrypoint-pattern.md` and the glossary line in `dbr-dev-tests.md`.

`cloudFiles.cleanSource` exists from Databricks Runtime 16.4. ADR-009's claim that source cleanup
stays manual is specific to the SharePoint standard connector rather than a missing platform
feature. That distinction is worth stating precisely, since TASK-097 turns on whether ADR-009 and
ADR-010 describe different actors.

---

## Conformance against the records

An independent derivation was run on 2026-09-01 against `decisions/` at SHA `7fce688`, following
the method in `adr-conformance/README.md`, in a process that never saw this document. Its verdicts
on the five design elements are worth carrying here, because four of them say this document decides
more than the records do.

| Element | Verdict | What it means for this design |
|:--------|:--------|:------------------------------|
| Unit | Underspecified | "Organised along the supply path it arrives on" fixes an axis and no granularity. It admits one table, two, or nineteen. This design chose nineteen |
| Name | Gap | No record names a bronze table. ADR-012's prohibition is scoped to directory names, so it neither permits nor forbids the rule used here |
| Columns | Conflict | ADR-008 says VARIANT plus promoted typed keys, ADR-009 says a single VARIANT. Both are Accepted, both write bronze |
| Layout | Determined | `CLUSTER BY AUTO`, no partitioning. This design conforms |
| Production | Underspecified | Dataset type, pipeline, compute, trigger and deployment all trace. The step from a configuration row to a table does not |

Four of those five verdicts are now closed. ADR-013 decides the unit, the naming rule and the
projection from configuration to tables. ADR-014 states the write block inline and reconciles the
conflict, reading ADR-008's promoted typed keys as a standing allowance rather than a requirement
and confirming ADR-009's untouched-write-block claim, since the five columns are identical across
both phases. This document is the companion detail behind those two records rather than a
substitute for them, which is the relationship ADR-008 and ADR-009 have with their own lock-ins,
except that the decisions now live in the substrate rather than outside it.

That last point is the durable lesson. The conflict existed because both Accepted records held the
write block by reference to a document the conformance suite is not allowed to read. A record that
delegates its substance outside `decisions/` is untestable however well the delegation is written.

The unit verdict is sharper than it looks. The only phrase anywhere in the substrate that names a
bronze granularity is a residue in ADR-011's rationale referring to a per-producer bronze, which
points at two tables rather than nineteen. ADR-001's 2026-08-07 revision retired that wording from
ADR-001 without replacing it, so the set's only granularity statement now sits in a record that does
not own the question, and it disagrees with this design.

The root cause behind the name, columns and production verdicts is structural rather than editorial.
ADR-008 and ADR-009 both hold the bronze write shape by reference to design documents that sit
outside `decisions/` by deliberate design, and both say so in their own Context sections. No amount
of tightening reaches Determined while that holds. The remedy is a record that states the bronze
write block, and this document is the input to writing it rather than a substitute for it.

---

## Open items

TASK-092 asked for a payload read before any format could be written, and it was blocking four
other tasks. The samples are on disk and this document profiles all 21, so the field inventory it
asked for can now be written into `2607-o2-requirements/` and the dependent tasks unblocked.

The feed-to-entity mapping is still missing, and this design does not need it, because bronze is per
feed. It becomes blocking at silver, where the entity contract lives.

The samples also bear on ADR-010 amendment A1 and TASK-093, which ask whether middleware
anonymisation destroys the only cross-producer join key. In these files it does not. APP feeds
carry `uid` and `matricule`, `perso_workers` carries `mail`, and Whoz carries `username` as an
email on the user report plus `emails` on talent, so an email bridge between APP and Whoz looks
available. This is a sample observation and not a measured match rate across the population, so it
narrows the question rather than closing it.

Catalog and schema naming needs its own decision. Three documents now say three different things:
`sqli_bronze_dev.raw` in the dev platform setup, `datawan_dev.bronze` in the dev tests, and
`dev_sandbox.bronze` here. Layer-in-catalog and layer-in-schema are different models, and ADR-006
puts the environment in the catalog. A catalog's managed location is adjustable while it is empty
and not adjustable one table in, so this wants settling before the first real environment exists.

---

## Sources

| Source | Bears on | Verified |
|:-------|:---------|:---------|
| [Ingest data as semi-structured variant type](https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant) | `singleVariantColumn` syntax, volume-path example, no schema evolution, `rescuedDataColumn` unsupported, oversized records to `corruptRecordColumn` | 2026-09-01 |
| [Variant type support for Apache Iceberg and Delta Lake](https://learn.microsoft.com/en-us/azure/databricks/tables/features/variant) | GA status, DBR 15.4 LTS floor, 128 MiB cap above DBR 17.1, no clustering key, no partition, no min or max statistics | 2026-09-01 |
| [Develop pipeline code with Python](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/python-dev) | `pyspark.pipelines` import, `@dp.table`, the `for` loop pattern, the late-binding trap, and the additive-list warning | 2026-09-01 |
| [Use liquid clustering for tables](https://learn.microsoft.com/en-us/azure/databricks/tables/clustering) | `CLUSTER BY AUTO` on streaming tables in Lakeflow pipelines, predictive optimization requirement, supported key types, why small tables are skipped | 2026-09-01 |
| [Spark API options reference, Auto Loader](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/options) | `multiLine`, `pathGlobFilter` on leaf names only, `allowOverwrites`, `schemaLocation` needed only for inference, files never split across micro-batches, `cleanSource` from DBR 16.4 | 2026-09-01 |
| [create_streaming_table](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/ldp-python-ref-streaming-table) | `cluster_by_auto` and `cluster_by` arguments, `row_filter` in Public Preview, no default flow on other targets | 2026-09-01 |
| [append_flow](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/ldp-python-ref-append-flow) | `create_streaming_table` plus `@dp.append_flow` as the documented pair, flows target streaming tables or sinks | 2026-09-01 |
| [ABAC common patterns](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/abac/common-patterns) | VARIANT-based masking functions taking and returning VARIANT, `schema_of_variant()` and `to_variant_object()`, single-field redaction | 2026-09-01 |
| [Row filters and column masks](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/filters-and-masks/) | A view cannot carry a mask, dynamic views are the documented alternative for reshaping access | 2026-09-01 |
| [Read JSON files](https://learn.microsoft.com/en-us/azure/databricks/query/formats/json) | BOM-based encoding auto-detection and its documented unreliability, explicit `encoding` as the remedy | 2026-09-01 |
| [Default storage in Databricks](https://learn.microsoft.com/en-us/azure/databricks/storage/default-storage) | Serverless-workspace requirement, no location on `CREATE CATALOG`, managed volumes supported, classic compute excluded, seven-day recovery window, no FileIO or credential vending, ODBC and Private Link caveat | 2026-09-01 |
| [Serverless compute limitations](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations) | Only `Trigger.AvailableNow` and `Trigger.Once`, external locations required for cloud storage, most Spark configurations unsupported | 2026-09-01 |
| [Set Spark configuration properties](https://learn.microsoft.com/en-us/azure/databricks/spark/conf) | The six properties serverless accepts, and the separate `spark_conf` mechanism for Lakeflow pipelines | 2026-09-01 |
| ADR-001, ADR-005, ADR-007, ADR-008, ADR-009, ADR-011, ADR-012 | Layer roles, pipeline and job separation, dataset types and clustering, the two ingestion paths, entity contract, tree strategy | in repo |
| 21 payload samples under `2608-o2-data-sources/` | Every record count, size, shape and personal-data observation in this document, re-derived independently | 2026-09-01 |
| `adr-conformance/README.md` and a blind derivation at SHA `7fce688` | The five verdicts in the conformance section | 2026-09-01 |

Version history is git. This document carries no version field.
