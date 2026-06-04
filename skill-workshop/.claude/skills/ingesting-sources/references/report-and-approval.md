# Report and approval

Loaded at Phase 4. Defines the four tables, RowID grammar, source-quote rendering, the editable `log.md` preview, and the approval grammar for Phase 5.

## RowIDs

Each row gets a stable ID `T<table>-<n>`: `T1-1`, `T2-1`, `T3-1`, `T4-1`, numbered per table in render order. RowIDs are how the user approves, edits, and rejects rows, and how `Depends on` references other rows.

## The four tables

Render each table as conversational markdown. Editable columns: `Destination`, `Description`, and the `Action` dropdown in Table 3 and Table 4. Read-only columns: `RowID`, `Category`, `Source item`, `Existing content`, `Source page`.

**Table 1 — Modifications to existing pages**

| RowID | Category | Source item | Destination | Description | Depends on |
|---|---|---|---|---|---|

**Table 2 — Proposed page creations**

| RowID | Category | Source item | Destination | Description | Depends on |
|---|---|---|---|---|---|

**Table 3 — Conflicts**

| RowID | Category | Source item | Action | Existing content | Dates (new / existing) | ⚠️ | Destination | Description | Depends on |
|---|---|---|---|---|---|---|---|---|---|

`Action` ∈ {`replace`, `supersede`, `coexist`, `do not add`}. `Dates` shows `issued_date_new / issued_date_existing`. Set ⚠️ when newer-wins suggests `do not add`, or when either date is `unknown`.

**Table 4 — Link updates**

| RowID | Source page | Target page | Action | Depends on |
|---|---|---|---|---|

`Action` ∈ {`add`, `update`, `remove`}.

`Category` ∈ {`section`, `subsection`, `sub-subsection`, `claim`}.

## Source-quote rendering (drawer adaptation)

The spec puts the verbatim source quote in an expandable drawer behind each `Source item` title. The terminal has no drawer, so:

- The `Source item` cell shows the **title only** (kept short).
- After all tables, render a **Source quotes** section listing, per RowID that carries source content, the verbatim quote as a blockquote:

  ```
  ### Source quotes
  - **T1-1** "<verbatim quote from the source>"
  - **T3-2** "<verbatim quote from the source>"
  ```

For a new source, the title comes from Phase 1 extraction. For an existing source (re-ingest), it comes from the target page's front-matter `sources[]`.

Cap each verbatim quote at roughly 280 characters. If the relevant passage is longer, quote the load-bearing sentence and elide the rest with `[…]`. Reason: an unbounded quote dump turns the report into a copy of the source and buries the rows the user must act on.

## Worked example

A populated report for ingesting `q1-earnings.pdf` "Tesla Q1 2026 Earnings Report" (issued 2026-04-10) into a wiki that already holds `[[tesla-inc]]`:

**Table 1 — Modifications to existing pages**

| RowID | Category | Source item | Destination | Description | Depends on |
|---|---|---|---|---|---|
| T1-1 | subsection | Q1 2026 deliveries | [[tesla-inc]] | Add a "Recent deliveries" subsection under History | — |
| T1-2 | claim | Cybertruck ramp rate | [[tesla-inc]] | Update the production-rate figure in Operations | — |

**Table 2 — Proposed page creations**

| RowID | Category | Source item | Destination | Description | Depends on |
|---|---|---|---|---|---|
| T2-1 | section | Dojo supercomputer | [[dojo-supercomputer]] | New entity page for the named training system | — |

**Table 3 — Conflicts**

| RowID | Category | Source item | Action | Existing content | Dates (new / existing) | ⚠️ | Destination | Description | Depends on |
|---|---|---|---|---|---|---|---|---|---|
| T3-1 | claim | FY revenue restated | supersede | "FY2025 revenue was $X" | 2026-04-10 / 2025-02-01 | | [[tesla-inc]] | Newer filing restates the figure; keep old as superseded | — |
| T3-2 | claim | Founding year is 2003 | do not add | "founded 2003" | unknown / 2023-09-12 | ⚠️ | [[tesla-inc]] | New source's date is unknown; older wiki claim stands until confirmed | — |

**Table 4 — Link updates**

| RowID | Source page | Target page | Action | Depends on |
|---|---|---|---|---|
| T4-1 | [[tesla-inc]] | [[dojo-supercomputer]] | add | T2-1 |

### Source quotes
- **T1-1** "Q1 2026 deliveries reached 422,000 vehicles, up 13% year over year […]"
- **T3-1** "We have restated FY2025 revenue to reflect the updated lease accounting […]"

## Editable log.md entry preview

Below the tables and quotes, render the proposed `log.md` entry inside a fenced block so the user can edit it during approval. Use the entry schema in `references/applying-the-report.md`. Label it clearly:

```
### Proposed log.md entry (editable)
```
<the entry per the log schema>
```
```

## Approval grammar (Phase 5)

After rendering, stop and wait. Interpret the user's reply with these verbs (case-insensitive), addressing rows by RowID:

| Verb | Effect |
|---|---|
| `approve all` | Approve every row as shown. |
| `approve <RowID> [<RowID> ...]` | Approve the listed rows only. |
| `reject <RowID> [...]` | Reject the listed rows. |
| `edit <RowID> <column>: <value>` | Change an editable column on a row (e.g. `edit T3-2 action: supersede`). |
| `Apply` | Commit the currently approved set (runs the Phase 6 dangling check first). |
| `Cancel` | Abort; release the lock; no mutations. |

Default state of every row is unapproved. Apply acts on the approved set only. After non-trivial edits, re-show the affected rows so the user confirms before `Apply`.

Catch-all for unrecognized input:
- If an `edit` sets an `Action` value outside its enum (Table 3: `replace` / `supersede` / `coexist` / `do not add`; Table 4: `add` / `update` / `remove`), reject the edit, name the allowed values, and re-prompt. Do not infer the nearest match.
- If the reply names a RowID that does not exist, or its verb is unrecognized, say so and re-show the verb list. Do not guess the intent.

Reason: silently coercing an out-of-grammar reply lets an unreviewed action through the one control surface this pipeline has.
