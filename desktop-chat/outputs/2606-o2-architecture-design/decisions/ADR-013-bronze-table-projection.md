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

- ADR-001 says bronze is organised "along the supply path it arrives on", which fixes an axis and leaves granularity open.
- A conformance derivation on 2026-09-01 graded the bronze unit and the feed-to-table step Underspecified, and naming a Gap.
- "Supply path" admits 1 table, 2 or 19 on today's configuration, so the ambiguity is an order of magnitude.
- The set's only granularity phrase is a residue in ADR-011 saying "per-producer bronze", pointing at 2. ADR-001 retired that wording on 2026-08-07 without replacing it.
- `o2-data-sources.md` carries `producer` and `source` as separate columns that disagree on 6 rows, since Whoz feeds are produced by Whoz and land on the APP site. Producer and supply path are not the same partition.
- Decided against 21 declared feeds, 19 active, 2 producers, 1 landing site.

## Options

- **A**, one table per feed, that is per landed file family. 19 tables, each with its own checkpoint and flow.
- **B**, one table per producer. 2 tables, mixed record shapes sharing one VARIANT column.
- **C**, one table per landing root. 1 table, the most literal reading of "supply path".
- **D**, one table per entity. The shape closest to ADR-011's entity contract.
- Not pursued, one table per subject area, because ADR-001 assigns subject area to silver.

## Decision

**Option A.** Three parts, stated so none is inferred.

**Unit.** One landed file family maps to one bronze table with its own checkpoint. A producer does not map to a table, nor does a subject area, nor an entity.

**Name.** Take the vehicle filename, drop the date prefix and the extension, lowercase, replace each run of non-alphanumeric characters with one underscore. Store the result in the feed configuration so the name is data.

**Projection.** One ingestion pipeline defines every table by iterating the active feeds in the
configuration. One loop, not two.

- Retiring a feed means removing it from the active list. Its table and history stay.
- Tested 2026-09-02 in development mode, production mode and production mode with a full refresh. In
  all three the removed dataset's table survived with its rows.
- An earlier version of this record used two lists, on the documented behaviour that a dataset
  omitted from a later run is dropped from the target schema. That behaviour did not reproduce under
  any of the three conditions, and the two-list form is separately invalid, since a streaming table
  with no attached flow fails the whole pipeline update with `No query found for dataset`.

> ⚠️ Three conditions is not exhaustive, and the documentation says otherwise. Do not treat
> non-destructive removal as guaranteed. The check sits in Validation so a platform change surfaces
> it, and evidence is in
> [`../2026-09-01-bronze-platform-tests.md`](../2026-09-01-bronze-platform-tests.md).

### Rationale

| Criterion | A, per feed | B, per producer | C, per landing | D, per entity |
|:----------|:------------|:----------------|:---------------|:--------------|
| Checkpoint isolation per source | Yes | No | No | Not evaluable |
| A bad feed blocks only itself | Yes | No | No | Not evaluable |
| Retire or backfill one feed alone | Yes | No | No | Not evaluable |
| Producer stays a mapping, per ADR-011 | Yes | No | Neutral | Yes |
| Buildable on today's configuration | Yes | Yes | Yes | No |
| Objects to operate | 19 tables, 19 checkpoints | 2 and 2 | 1 and 1 | Unknown |

- D is unavailable rather than rejected. The feed-to-entity mapping does not exist, so choosing it would mean inventing that mapping as a side effect of a table-layout decision.
- B and C fail together for one reason. The locked SharePoint design already needs one checkpoint per file pattern, so they either keep 19 checkpoints while writing fewer tables, which buys nothing, or collapse to one stream over mixed globs and lose per-feed exactly-once, replay and retirement.
- B also makes the producer structural, which is what ADR-011 decided against.
- The naming rule rests on a confirmed absence. ADR-012's prohibition is written against directory names and does not reach table names, so nothing forbids the rule and nothing else supplies one.
- Mechanical beats tidy because the alternative is a judgement re-made per feed. The price is accepted: `others_whoz_profile_report` carries a source-folder bucket that means nothing to O2.
- The projection is a single loop because removal proved non-destructive on test, and because the two-list alternative is invalid: a flowless streaming table fails the whole update.

## Validation

- Every active feed row has exactly one bronze table, and the counts match.
- No producer name, filename, source path or table name appears in pipeline code. Greppable.
- Adding a feed row and redeploying creates a table with no diff outside the configuration file.
- Removing a feed from the active list leaves its table and row count unchanged. Verified 2026-09-02 under three conditions, and the check stays because the documentation says the opposite.
- The naming rule yields distinct names with no collision. Verified on the 2026-09-01 configuration, which produces 21.

Reopens when the feed-to-entity mapping exists, making D evaluable, or when one logical dataset splits across several vehicles, which is the case this record has not tested.

## Consequences

- 19 tables and 19 checkpoints to operate today, growing with the feed count. Accepted, not argued away.
- A feed added, retired or repointed is a configuration edit touching no code and no directory.
- Deleting a configuration row deletes a table. Default storage keeps the files for 7 days, which is time to notice rather than a safety net.
- The feed configuration gains at least four columns: derived table name, path relative to the landing root, filename glob, and record shape.
- The status vocabulary does not need a fourth value for safety, since removal is non-destructive. A retired value may still be wanted to record which feeds once ingested, which is documentation rather than correctness.
- Table names carry source-folder artefacts. Anyone reading the catalog for business meaning is reading the wrong layer.
- A logical dataset split across vehicles becomes several tables and a union in silver. No such case exists today.

## Sources

| Source | Bears on | Verified |
|:-------|:---------|:---------|
| [Develop pipeline code with Python](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/python-dev) | The `for` loop pattern, the late-binding trap, and drop-on-absence | 2026-09-01 |
| [create_streaming_table](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/ldp-python-ref-streaming-table) | Defining a target table separately from its flows | 2026-09-01 |
| [append_flow](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/ldp-python-ref-append-flow) | Attaching an append flow to an existing streaming table | 2026-09-01 |
| [Default storage in Databricks](https://learn.microsoft.com/en-us/azure/databricks/storage/default-storage) | The 7-day recovery window on a dropped managed table | 2026-09-01 |
| ADR-001, ADR-005, ADR-011, ADR-012 | Supply-path alignment, ingestion separate from transformation, producer as mapping, tree strategy | in repo |
| [`../2026-09-01-bronze-table-design.md`](../2026-09-01-bronze-table-design.md) | Detailed design and payload evidence. A companion, not the decision | 2026-09-01 |

Version history is git. This record carries no version field.
