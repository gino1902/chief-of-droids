# Re-ingest — source-metadata correction path

Loaded at Phase 0 when the trigger carries `--reingest`. Used when per-source metadata already on the wiki is wrong: a misread `source_title` or `issued_date` in front-matter `sources[]`, or in an inline `*Sources:*` line or footnote definition. There is no separate metadata artefact to fix; the page front-matter and citation lines are the only carriers, so the correction is a full re-read of the immutable source.

This path reuses the main pipeline's report, approval, apply, and commit machinery. It changes only how rows are generated.

## Flow

1. **Re-read** exactly `./raw/<raw-filename>` (the `raw/` ask rule prompts; approve the single named file). Re-extract `source_title` and `issued_date` from the immutable source.
2. **Find citing pages.** `Grep` the wiki for pages whose front-matter `sources[]` contains this `source_file`. Read only those pages. Do not scan `./raw/`.
3. **Generate correction rows** (Table 1 — Modifications), one set per citing page:
   - Update the page's `sources[]` entry: new `source_title`, new `issued_date`.
   - Update every inline `*Sources: [[<source_file>]] "<old title>"*` line and every footnote definition `[^id]: [[<source_file>]] "<old title>"` on that page to the corrected title.
   - **Do not** change `ingested_date`. It records when the page first cited the source and is fixed for the life of the page.
   - Bump `updated` on each touched page.
4. **Surface incidental content.** Re-reading can surface content the first ingest missed. Propose it as ordinary Table 1 / Table 2 / Table 3 rows so the user can accept or reject it independently of the metadata fix. Reason: a corrected read of the immutable source is authoritative, so newly-found items are legitimate proposals, but they are separate decisions from the title/date correction.
5. **Report, approve, apply** through the normal Phases 4-6. The commit subject uses the `reingest(<source-stem>): ...` form.

## Guardrails

- Metadata-correction rows and incidental-content rows are separate rows with their own RowIDs, so the user can take the title/date fix while rejecting unrelated content changes.
- If the re-extracted `source_title` / `issued_date` match what is already on every citing page, report that there is nothing to correct and offer Cancel.
- The same `source_file` must end with identical `source_title` and `issued_date` across all citing pages after apply; if the report would leave them divergent, flag it before Apply.
