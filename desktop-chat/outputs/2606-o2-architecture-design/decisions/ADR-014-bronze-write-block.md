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

- ADR-008 Consequences: "Bronze stores the whole record as VARIANT plus promoted typed keys", repeated in its Validation as "promoted key columns".
- ADR-009 Option A: Auto Loader "lands each record as a single VARIANT", with no promoted-keys clause, and its Consequences say that at migration "the write block is untouched".
- Both cannot hold. Either bronze has promoted keys and ADR-009 omits them, or it has none and ADR-008's keys are a write-block change ADR-009 says will not happen.
- A conformance derivation on 2026-09-01 graded this a Conflict.
- Root cause is structural. Both records hold the write block by reference to design documents outside `decisions/`, and both say so. The only two Accepted records carry the least derivable content, and no rewording fixes that.
- Three absences sit inside the same element. No record names the VARIANT column, none says whether ingestion metadata is stored in columns, and none says which keys "promoted typed keys" means.

This record states the write block inline rather than referring to it.

## Options

- **A**, whole-record VARIANT plus a fixed provenance set, no business keys promoted until measured.
- **B**, whole-record VARIANT plus promoted business keys per feed from the outset. ADR-008 as written.
- **C**, a single VARIANT column and nothing else. ADR-009 read literally.

## Decision

> ⚠️ The column contract below stands. How `payload` gets populated does not, as of 2026-09-02.
> `singleVariantColumn` with `multiLine=true` puts the whole file in one VARIANT, giving one row per
> file rather than one row per record, verified on both `read_files` and `cloudFiles`. Two feeds
> would additionally exceed the 128 MiB cap as a single value and carry no data at all. Evidence and
> the available repairs are in
> [`../2026-09-01-bronze-platform-tests.md`](../2026-09-01-bronze-platform-tests.md). The grain
> question needs settling, most cleanly by asking the producer for newline-delimited JSON, before
> this record leaves Draft.

**Option A. Every bronze table carries these five columns and no others.**

| Column | Type | Source |
|:-------|:-----|:-------|
| `payload` | VARIANT | The whole record, via `singleVariantColumn` |
| `_source_file` | STRING | `_metadata.file_path` |
| `_source_file_mtime` | TIMESTAMP | `_metadata.file_modification_time` |
| `_ingested_at` | TIMESTAMP | Pipeline run time |
| `_snapshot_date` | DATE | Parsed from the vehicle filename |

- Bronze is append-only, and expectations warn rather than drop per ADR-007, so malformed records are kept.
- A business key is promoted when a measured silver query pattern calls for it, and not before. None exists today, because silver does not exist.

**Reconciliation.** ADR-008's "promoted typed keys" is read as a standing allowance, not a requirement, so bronze may carry typed columns and which ones is decided on evidence. ADR-009's "write block untouched" holds, because these five columns are identical in both phases. Neither record is superseded. Both are amended on this element, which this record now owns.

### Rationale

| Criterion | A | B | C |
|:----------|:--|:--|:--|
| Satisfies ADR-007's `CLUSTER BY AUTO` | Yes | Yes | No, nothing to cluster on |
| Provenance available to silver | Yes | Yes | No |
| Identifies which closed period a row belongs to | Yes | Only if the key is chosen right | No |
| Needs knowledge that does not exist yet | No | Yes | No |
| One shape across all tables | Yes | No | Yes |

- C fails on grounds its own record supplies, since ADR-009 names provenance as a reason for choosing its option and a bare VARIANT stores none.
- C also breaks ADR-007. A VARIANT column cannot be a clustering key, cannot partition, and carries no `minValues` or `maxValues`, so a VARIANT-only table has no data layout and `CLUSTER BY AUTO` has nothing to act on. The provenance set is what makes an existing decision operable.
- B asks a question nobody can answer today. Promoting a column later is additive, so deferring is cheap and guessing wrong leaves a column that misleads the next reader.

`_snapshot_date` needs its own argument, being in neither existing record.

- Most feeds are full snapshots landing daily, so bronze accumulates repeated copies and silver's deduplication needs an as-of date.
- Five feeds are not snapshots. `cra_bilan_cra_report`, `cra_worklog`, `perso_collab_status_report`, `project_ca_collab_report` and `project_project_dataware_report` each carry exactly one period and are rolling current-period extracts.
- For those five, once a month closes the last landing is the only copy that will ever exist, and this column is the only thing saying which closed month a row describes.
- The filename is the only carrier. No payload in the 21-file corpus contains an extraction date, and ingestion time breaks on replay.

## Validation

- Every bronze table has exactly these five columns. A sixth means a promotion happened, and the merge request must carry the evidence for it.
- All tables share the same five columns. Divergence means a per-feed write block crept back.
- `_snapshot_date` is non-null on every row, and its distinct count equals the landing dates ingested.
- The write block is byte-identical across the SharePoint and ADLS phases, which is the check proving ADR-009's untouched-write-block claim.
- An oversized record lands in `corruptRecordColumn` under `PERMISSIVE` rather than vanishing. Theoretical today, since the largest record in the corpus is 410 KB.

Reopens when a measured silver query justifies a promoted key, which is expected rather than failure, or if a payload is found carrying a reliable extraction date.

## Consequences

- Silver reads one shape across every bronze table instead of 19 bespoke ones.
- Nothing in bronze is queryable by business key without a VARIANT path expression. Intended under ADR-001, and a real cost when debugging.
- Source schema drift is absorbed with no pipeline change, because there is no schema to evolve. Drift is also invisible until silver trips over it.
- Layout depends entirely on `_snapshot_date`. Drop it and the tables have no clustering key at all.
- Retention pulls two ways and must be set deliberately. Repeated daily landings of personal data argue for a short window, and the five current-period feeds argue against, because a short window destroys closed months nothing can rebuild.
- Field-level governance is available at bronze and is not blocked by the VARIANT. Unity Catalog ABAC supports mask functions taking and returning VARIANT, so one field can be redacted while the record survives. Bronze stays grant-closed under ADR-001, but that is now a choice rather than a limitation.

## Sources

| Source | Bears on | Verified |
|:-------|:---------|:---------|
| [Ingest data as semi-structured variant type](https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant) | `singleVariantColumn`, no schema evolution, oversized records to `corruptRecordColumn` | 2026-09-01 |
| [Variant type support for Iceberg and Delta Lake](https://learn.microsoft.com/en-us/azure/databricks/tables/features/variant) | GA on DBR 15.4 LTS and above, no clustering key, no partition, no min or max statistics, 128 MiB cap above DBR 17.1 | 2026-09-01 |
| [Use liquid clustering for tables](https://learn.microsoft.com/en-us/azure/databricks/tables/clustering) | Supported key types, `CLUSTER BY AUTO` on streaming tables in pipelines | 2026-09-01 |
| [ABAC common patterns](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/abac/common-patterns) | VARIANT-based masking, single-field redaction inside a VARIANT | 2026-09-01 |
| ADR-007, ADR-008, ADR-009, ADR-013 | Layout and expectations, the two conflicting statements, and the unit this applies to | in repo |
| 21 payload samples, read 2026-09-01 | The five current-period feeds, no extraction date in any payload, 410 KB largest record | 2026-09-01 |

Version history is git. This record carries no version field.
