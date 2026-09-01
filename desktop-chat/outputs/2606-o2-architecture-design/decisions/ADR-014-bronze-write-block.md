# ADR-014 — Bronze write block: whole-record VARIANT plus a fixed provenance set, stated in the record (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-09-01 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | DE team, Security |
| Informed | Wider data team |
| Amends | ADR-008 and ADR-009, on the write block only |

---

## Context

Two Accepted records specify what a bronze table contains, and they specify different things.

ADR-008 Consequences: "Bronze stores the whole record as VARIANT plus promoted typed keys", and its
Validation repeats the requirement as "VARIANT treated as Public Preview with promoted key
columns". ADR-009 Option A: Auto Loader "lands each record as a single VARIANT and appends to
bronze", with no promoted-keys clause anywhere, and its Consequences state that at ADLS migration
"only the read-path block" changes and "the write block is untouched".

Those cannot all hold. If the write block is untouched at migration, then either bronze already has
promoted keys and ADR-009 omits them, or it has none and ADR-008's promoted keys are a write-block
change that ADR-009 says will not happen.

A conformance derivation on 2026-09-01 graded this element a Conflict and identified the root
cause, which is structural rather than editorial. Both records hold the bronze write shape by
reference to design documents that sit outside `decisions/` by deliberate design, and both say so
in their own Context sections. ADR-INDEX describes this as intentional concision. The consequence
is that the two Accepted records, the only two in the set, are the two carrying the least derivable
content, and no amount of rewording reaches Determined while the write block lives outside the
substrate.

Three further absences were found inside the same element. No record names the VARIANT column. No
record says whether ingestion metadata is stored in columns, so a design that adds provenance
columns and one that adds none are both compliant. And no record says which keys "promoted typed
keys" means, or of what type.

This record therefore states the write block inline rather than referring to it.

---

## Options evaluated

**Option A — Whole-record VARIANT plus a fixed provenance set, no business keys promoted until measured**
One VARIANT column holding the record, and four typed columns carrying where it came from and when.
The same five columns on every bronze table. Business keys are promoted later, on evidence, and
promoting one is an additive change rather than a redesign.

**Option B — Whole-record VARIANT plus promoted business keys per feed from the outset**
ADR-008 as written. Each feed's design names the keys it promotes.

**Option C — A single VARIANT column and nothing else**
ADR-009 as written, read literally.

---

## Decision

**Option A. Every bronze table carries these five columns and no others.**

| Column | Type | Source |
|:-------|:-----|:-------|
| `payload` | VARIANT | The whole record, via `singleVariantColumn` |
| `_source_file` | STRING | `_metadata.file_path` |
| `_source_file_mtime` | TIMESTAMP | `_metadata.file_modification_time` |
| `_ingested_at` | TIMESTAMP | Pipeline run time |
| `_snapshot_date` | DATE | Parsed from the vehicle filename |

Bronze is append-only. Expectations warn and never drop, per ADR-007, so malformed records are kept
rather than discarded.

**The reconciliation with ADR-008 and ADR-009.** ADR-008's "promoted typed keys" is read as a
standing allowance and not a requirement: bronze may carry typed columns beside the VARIANT, and
which ones is decided by evidence rather than fixed by that record. ADR-009's "the write block is
untouched" holds under this record, because the five columns above are identical in both the
SharePoint phase and the ADLS end state. Neither record is superseded. Both are amended on this one
element, and this record owns it from here.

**Promotion rule.** A business key is promoted when a measured query pattern in silver calls for
it, and not before. On the 2026-09-01 configuration no such pattern exists, because silver does not
exist.

### Rationale

| Criterion | A | B | C |
|:----------|:--|:--|:--|
| Satisfies ADR-007's `CLUSTER BY AUTO` | Yes | Yes | No, nothing to cluster on |
| Provenance available to silver | Yes | Yes | No |
| Identifies which closed period a row belongs to | Yes | Only if the key is chosen correctly | No |
| Requires knowledge that does not exist yet | No | Yes, which keys matter | No |
| Same shape across all tables, so silver has one handle | Yes | No, per-feed | Yes |
| Survives the ADLS migration unchanged | Yes | Yes | Yes |

C fails on grounds its own record supplies. ADR-009 names provenance as a reason for choosing its
option, and a table with only a VARIANT column stores none. C also breaks ADR-007. Documentation is
explicit that a VARIANT column cannot be a clustering key, cannot partition a table, and collects no
`minValues` or `maxValues` statistics, so a bronze table of VARIANT alone has no data layout at all
and `CLUSTER BY AUTO` has nothing to act on. The provenance set is not a convenience. It is what
makes an existing decision operable.

B asks a question nobody can answer today. Choosing per-feed business keys requires knowing which
fields silver will filter and join on, and silver has not been built. Promoting a column later is
additive, so the cost of deferring is low and the cost of guessing wrong is a column that misleads
whoever reads the table next.

`_snapshot_date` deserves its own argument, because it is the one column not present in either
existing record. Feeds land daily and most are full snapshots, so bronze accumulates repeated copies
by design and silver's deduplication needs an as-of date. Five feeds are not snapshots at all.
`cra_bilan_cra_report`, `cra_worklog`, `perso_collab_status_report`, `project_ca_collab_report` and
`project_project_dataware_report` each carry exactly one period and are rolling current-period
extracts, so once a month closes, the last landing of that month is the only copy that will ever
exist. For those five the column is the only thing that says which closed month a row describes.
Deriving it from the filename is deterministic where ingestion time breaks on replay, and the
filename is the only available carrier, since no payload in the corpus contains an extraction date.

Basis. The VARIANT clustering and statistics limits, the `singleVariantColumn` mechanics and the
`_metadata` fields are Databricks documentation, cited below. The five-feed finding and the absence
of an extraction date in any payload come from reading all 21 payloads on 2026-09-01. The
requirement that layout be `CLUSTER BY AUTO` is ADR-007.

---

## Validation

- Every bronze table has exactly these five columns. A table with a sixth means a promotion happened
  without the evidence this record requires, and the merge request should carry that evidence.
- Every bronze table has the same five columns as every other. Divergence means a per-feed write
  block crept back in.
- `_snapshot_date` is non-null on every row, and distinct values per table equal the number of
  distinct landing dates ingested.
- The write block is byte-identical between the SharePoint phase and the ADLS phase, which is the
  check that proves ADR-009's untouched-write-block claim under this record.
- A record too large for the VARIANT cap lands in `corruptRecordColumn` under `PERMISSIVE` rather
  than being silently lost. Currently theoretical, since the largest record in the corpus is 410 KB.

The decision reopens when a measured silver query pattern justifies a promoted key, which is
expected rather than a failure, or if a payload is found carrying its own reliable extraction date,
which would make `_snapshot_date` derivable from content rather than from a filename.

---

## Consequences

- Silver reads one shape across every bronze table, so the conforming layer takes a uniform handle
  rather than nineteen bespoke ones.
- Nothing in bronze is queryable by business key without a VARIANT path expression. That is intended,
  since ADR-001 makes bronze silver-only, and it is a real cost for anyone debugging.
- Schema drift in a source is absorbed with no pipeline change, because there is no schema to evolve.
  The cost is that drift is also invisible until silver trips over it.
- Layout depends entirely on `_snapshot_date`, so if that column were ever dropped, the tables would
  have no clustering key at all.
- Retention on bronze now pulls in two directions and must be set deliberately. Personal data across
  repeated daily landings argues for a short window. The five current-period feeds argue the other
  way, because a window shorter than the gap between month close and the next read destroys closed
  months that nothing can rebuild.
- Field-level governance at bronze is available and is not blocked by the VARIANT. Unity Catalog
  ABAC supports mask functions taking and returning VARIANT, so a single field can be redacted while
  the record survives. Bronze is still closed at grant level under ADR-001, but that is now a choice
  rather than a limitation, and the option exists the day someone has a legitimate reason to read it.

---

## Sources

| Source | Bears on | Verified |
|:-------|:---------|:---------|
| [Ingest data as semi-structured variant type](https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant) | `singleVariantColumn`, no schema evolution, `rescuedDataColumn` unsupported, oversized records to `corruptRecordColumn` | 2026-09-01 |
| [Variant type support for Iceberg and Delta Lake](https://learn.microsoft.com/en-us/azure/databricks/tables/features/variant) | VARIANT is generally available on DBR 15.4 LTS and above, cannot be a clustering key or partition column, carries no min or max statistics, 128 MiB cap above DBR 17.1 | 2026-09-01 |
| [Use liquid clustering for tables](https://learn.microsoft.com/en-us/azure/databricks/tables/clustering) | Supported clustering key types, `CLUSTER BY AUTO` on streaming tables in pipelines | 2026-09-01 |
| [ABAC common patterns](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/abac/common-patterns) | VARIANT-based masking functions, single-field redaction inside a VARIANT | 2026-09-01 |
| ADR-007 | `CLUSTER BY AUTO` as the layout, expectations warn at bronze | in repo |
| ADR-008, ADR-009 | The two conflicting write-block statements this record reconciles | in repo |
| ADR-013 | The unit this write block applies to | in repo |
| 21 payload samples, read 2026-09-01 | The five current-period feeds, the absence of any extraction date in any payload, the 410 KB largest record | 2026-09-01 |

Version history is git. This record carries no version field.
