# ADR-013 — Bronze table projection: one table per feed, named from the vehicle, generated from configuration (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-09-01 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | DE team |
| Informed | Wider data team |

---

## Context

ADR-001 says bronze is "organised along the supply path it arrives on". That fixes an axis and
leaves the granularity open, and nothing else in the set closes it.

A conformance derivation run on 2026-09-01 against this directory, following
[`../adr-conformance/README.md`](../adr-conformance/README.md), graded three of the five bronze
design elements short of Determined. The unit came back Underspecified, because "the supply path"
admits one table, two or nineteen on the current configuration. The naming rule came back a Gap,
because no record names a bronze table at all. The step from a configuration row to a table came
back Underspecified, because ADR-012 bounds itself to the repository tree and says nothing about
what a feed row produces inside a catalog.

Two further facts make the ambiguity concrete rather than theoretical. The only phrase anywhere in
the set that names a bronze granularity is a residue in ADR-011's rationale referring to a
"per-producer bronze", which points at two tables. ADR-001's 2026-08-07 revision retired that
wording from ADR-001 without replacing it, so the set's sole granularity statement now sits in a
record that does not own the question. And `o2-data-sources.md` carries `producer` and `source` as
separate columns that disagree on six rows, since the Whoz feeds are produced by Whoz and land on
the APP site, so "producer" and "supply path" are not the same partition of today's data.

The configuration this record is decided against: 21 declared feeds, 19 active, two producers, one
landing site.

---

## Options evaluated

**Option A — One table per feed, that is per landed file family**
Nineteen tables today. Each has its own Auto Loader checkpoint, its own flow and its own failure
boundary. The table name derives mechanically from the vehicle filename.

**Option B — One table per producer**
Two tables. Every feed from a producer appends into one table, with heterogeneous record shapes
sharing one VARIANT column, distinguished only by the source-file provenance.

**Option C — One table per landing root**
One table. The most literal reading of "the supply path it arrives on", since all active feeds
arrive over one connector from one site.

**Option D — One table per entity**
The shape that would match ADR-011's entity contract most directly.

**Options not pursued**
- One table per subject area. ADR-001 assigns subject area to silver explicitly, so this would put
  silver's axis on bronze.

---

## Decision

**Option A. A bronze table corresponds to one feed. Its name derives mechanically from the vehicle
filename. The set of tables is generated from the feed configuration rather than hand-written, and
the table list and the ingestion list are governed separately.**

The three parts, stated so no part is inferred:

**The unit.** One landed file family maps to one bronze table with its own checkpoint. A producer
does not map to a table, a subject area does not map to a table, and an entity does not map to a
table. The producing system remains a mapping, per ADR-011.

**The name.** Take the vehicle filename, drop the date prefix, drop the extension, lowercase, and
replace each run of non-alphanumeric characters with a single underscore. The derived name is
stored in the feed configuration, so the name is data rather than a rule re-applied by hand.

**The projection.** One ingestion pipeline defines every bronze table by iterating the feed
configuration. Two lists govern it, not one. The table list holds every feed that has ever been
ingested and never shrinks. The ingestion list holds the feeds currently ingesting, and a feed's
status moves it between them. Retiring a feed removes it from the ingestion list alone, which stops
the flow and keeps the table and its history.

### Rationale

| Criterion | A, per feed | B, per producer | C, per landing | D, per entity |
|:----------|:------------|:----------------|:---------------|:--------------|
| Checkpoint isolation per source | Yes | No, one stream over mixed globs | No | Not evaluable |
| A bad feed blocks only itself | Yes | No, blocks the producer | No, blocks everything | Not evaluable |
| Retire or backfill one feed alone | Yes | No | No | Not evaluable |
| Consistent with ADR-011, producer is a mapping | Yes | No, producer becomes structure | Neutral | Yes |
| Cost of a feed added or retired | A row | A row | A row | A row plus a mapping |
| Buildable on the 2026-09-01 configuration | Yes | Yes | Yes | No |
| Objects to operate | 19 tables, 19 checkpoints | 2 and 2 | 1 and 1 | Unknown |

D is not available rather than rejected. ADR-INDEX records that the feed-to-entity mapping does not
exist, and ADR-011 admits an entity only when a supply path exists, so nothing today can say which
feeds carry which entities. Choosing D would require inventing that mapping as a side effect of a
table-layout decision.

B and C fail on the first three criteria together, and they fail for one underlying reason. The
locked SharePoint design already requires one Auto Loader checkpoint per file pattern, so B and C
would either keep nineteen checkpoints while writing to fewer tables, which buys nothing, or
collapse to one stream reading mixed globs, which loses per-feed exactly-once tracking, per-feed
replay and per-feed retirement. B additionally makes the producer a structural fact about bronze,
which is what ADR-011 decided against and what ADR-001's 2026-08-07 revision removed.

The naming rule rests on an absence confirmed rather than assumed. ADR-012's prohibition is written
against directory names, so it neither permits nor forbids deriving a table name from a filename,
and the conformance derivation confirmed that reading. Since no rule reaches it, the rule chosen is
the one that keeps the mapping reversible in both directions and removes the judgement that would
otherwise be re-made each time a feed is added. This is deliberately not the tidiest available
name. `others_whoz_profile_report` carries a source-folder bucket that means nothing to O2, and
that is accepted as the price of a mechanical rule.

The two-list projection is forced by documented behaviour rather than chosen. Lakeflow drops a
dataset from the target schema when it is absent from a later run, so a single loop over active
feeds would destroy a table and its history the moment a feed stopped being active. That is the
opposite of what retiring a feed must do.

Basis. The per-pattern checkpoint requirement and the per-feed flow isolation come from the locked
SharePoint design and from ADR-005's requirement that a transformation failure not block new data
landing. That a producer is configuration and not structure is ADR-011. That subject area belongs
to silver is ADR-001. The drop-on-absence behaviour and the `for` loop pattern are Databricks
documentation, cited below.

---

## Validation

- Every active feed row has exactly one bronze table, and the table count equals the active feed
  count. Any other number means the projection was edited by hand.
- No producer name, filename, source path or table name appears in pipeline code. Greppable.
- Adding a feed row and redeploying creates a table with no diff outside the configuration file.
- Flipping a feed's status to retired stops its flow and leaves its table and row count unchanged.
  This is the check that proves the two-list split works, and it is the one most likely to fail.
- Applying the naming rule across the whole configuration yields distinct names with no collision.
  Verified on the 2026-09-01 configuration, which produces 21 distinct names.

Reopening conditions. The feed-to-entity mapping comes into existence, which makes Option D
evaluable for the first time. Or a feed splits into several vehicles carrying one logical dataset,
which is the case this record has not tested and where per-feed tables push a union into silver.

> ⚠️ Unverified, and load-bearing for the retirement half of this decision. That a streaming table
> with no attached flow is a supported steady state whose data survives across pipeline runs is not
> documented. The pattern of `create_streaming_table` plus `@dp.append_flow` is documented, the
> persistence of a flowless table is not. Test before this record moves past Draft.

---

## Consequences

- Nineteen tables and nineteen checkpoints to operate today, growing with the feed count. This is
  the cost of the decision and it is accepted rather than argued away.
- A feed change is a configuration edit. Adding, retiring or repointing a feed touches no code and
  no directory, which is ADR-012's rule applied inside the catalog.
- Deleting a configuration row deletes a table. On default storage the files are recoverable for
  seven days, which is time to notice rather than a safety net. The row is the artefact to protect.
- The feed configuration gains columns it does not have today, at minimum the derived table name,
  the path relative to the landing root, the filename glob and the record shape. The workbook is
  the source of truth for these and it is not tracked by git.
- The status vocabulary needs a fourth value. Today it carries active, inactive and planned, where
  inactive means the feed lands and is not ingested. Retired means it was ingested and no longer
  is, which has a different consequence and cannot currently be expressed.
- Bronze table names carry source-folder artefacts that mean nothing to the business. Anyone
  reading the catalog for meaning is reading the wrong layer, which ADR-001 already implies.
- A logical dataset split across several vehicles becomes several bronze tables and one union in
  silver. No such case exists today.

---

## Sources

| Source | Bears on | Verified |
|:-------|:---------|:---------|
| [Develop pipeline code with Python](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/python-dev) | The `for` loop pattern, the late-binding trap, and the rule that a dataset absent from a later run is dropped from the target schema | 2026-09-01 |
| [create_streaming_table](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/ldp-python-ref-streaming-table) | Defining a target table separately from the flows that write it | 2026-09-01 |
| [append_flow](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/ldp-python-ref-append-flow) | Attaching an append flow to an existing streaming table | 2026-09-01 |
| [Default storage in Databricks](https://learn.microsoft.com/en-us/azure/databricks/storage/default-storage) | The seven-day recovery window on a dropped managed table | 2026-09-01 |
| ADR-001 | Bronze source-aligned along the supply path, subject area belongs to silver | in repo |
| ADR-005 | Bronze ingestion separate from transformation, a failure in one must not block new data landing | in repo |
| ADR-011 | The producing system is a mapping and not the contract | in repo |
| ADR-012 | A change in the world is a diff in a file, and the directory-name prohibition that does not reach table names | in repo |
| [`../2026-09-01-bronze-table-design.md`](../2026-09-01-bronze-table-design.md) | The detailed design and the payload evidence behind the counts. Cited as a companion, not as the decision | 2026-09-01 |

Version history is git. This record carries no version field.
