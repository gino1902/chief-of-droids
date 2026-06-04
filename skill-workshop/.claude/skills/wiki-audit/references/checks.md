# Checks — detection method per finding type

Each check is read-only. Run against the working set resolved from the scope argument. Report what is found; never fix it here.

## 1. Contradictions across pages

The slower-cadence net for direct disagreements that ingest-time detection missed. Compare claims on related pages (same entity/concept, or pages linked to each other) for statements that cannot both be true. Report the two pages and the conflicting claims. Route: `re-ingest <source>` of the source behind the wrong claim, or a fresh ingest if a newer source settles it.

## 2. Stale claims

A page rests on an older source while a newer source elsewhere in the corpus supersedes that claim, but the page was never updated. Detect by finding claims that overlap across pages, then comparing the `issued_date`s in each page's front-matter `sources[]`. The page citing the older source on a contradicted point is stale. Route: `re-ingest <source>` or ingest the newer source into the stale page.

## 3. Orphan pages

Pages with no inbound `[[wiki-link]]` from any other page. Build the link graph by grepping `[[...]]` targets across all pages, then list pages that are never a target. Report every orphan, marking new or root pages as expected rather than defects. Reason: inbound-link absence is a graph property, not an error; a brand-new page and a deliberate root are legitimate zero-inbound states. Route: `add cross-reference`.

## 4. Missing pages (concepts mentioned in passing)

Entities or concepts named repeatedly across pages but lacking a page of their own. Detect recurring capitalized noun phrases or quoted terms that appear on multiple pages with no matching slug or alias. Report the term and the pages that mention it. Route: `create page`.

## 5. Missing cross-references

A name that matches an existing page's slug or alias but appears as bare text instead of a `[[link]]`. Detect by checking, for each existing page title/alias, whether other pages mention it in prose without linking. Report the mention site and the page it should link to. Route: `add cross-reference`.

## 6. Data gaps

Points where the wiki is thin and external information could fill the gap: open questions left on pages, `issued_date: unknown` entries, or claims that clearly want a figure, date, or source the wiki does not hold. Route: `web-search then ingest` (or `ingest new source`). The audit only flags the gap; it does not search.

## 7. Metadata drift

The same `source_file` carrying different `source_title` or `issued_date` in different places. Two sub-checks:

- **Cross-page:** grep every page's front-matter `sources[]` for the source filename; compare titles and dates across pages.
- **Same-page:** compare a page's front-matter `source_title` against the title quoted in its inline `*Sources:*` lines and footnote definitions.

Report the divergent values and locations. Route: `re-ingest <source>` (the correction path reconciles all citing pages).

Demonstration (cross-page drift on one `source_file`):

```
[[tesla-inc]]      sources[]: { source_file: q1-earnings.pdf, source_title: "Tesla Q1 2026 Earnings Report", issued_date: 2026-04-10 }
[[dojo-supercomputer]] sources[]: { source_file: q1-earnings.pdf, source_title: "Q1 2026 Report",            issued_date: 2026-04-09 }
```

Same `source_file`, two titles and two dates → one finding, Route `re-ingest q1-earnings.pdf`.

## 8. Latent slug collisions and near-duplicates

Pages whose slugs, titles, or aliases are close enough to be the same referent (or to collide). Detect by comparing slugs and titles for near-identity and by spotting two pages that describe the same thing under different slugs. Report the candidate pair. Route: `resolve duplicate` (merge through an ingest report).

## 9. Open questions worth investigating

Questions the corpus raises but does not answer, surfaced on pages or implied by gaps. Distinct from data gaps in that the answer may not be a quick lookup. Report the question and where it arose. Route: `investigate question`.

## 10. Sources worth seeking

Where a specific kind of source would materially strengthen the wiki: a primary document behind a second-hand claim, a more recent report than the newest one cited, an authoritative reference for a contested point. Report what to look for and why. Route: `ingest new source` once obtained.
