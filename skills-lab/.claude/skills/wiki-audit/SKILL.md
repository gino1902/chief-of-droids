---
name: wiki-audit
description: Read-only health-check for the wiki. Surfaces contradictions, stale claims, orphan pages, missing pages, missing cross-references, data gaps, metadata drift, near-duplicate slugs, open questions, and sources worth seeking. Output is a conversational findings list; the user decides what to act on, and each finding routes back through the ingest or re-ingest pipeline. Never mutates the wiki and never touches ./raw/. Invoke when the user asks to health-check, audit, or check the wiki for drift, gaps, or duplicates. Optional scope argument: a page slug, a tag, or all (default).
argument-hint: "[page-slug | tag | all]"
allowed-tools:
  - Read
  - Grep
  - Glob
---

<!-- target-model: claude-opus-4-8 | target-environment: claude-code | snapshot-ref: 2026-05-17 -->

# wiki-audit

A periodic safety net for drift, decay, and gaps that accumulate across the corpus as the wiki grows. Ingest-time controls catch what each new source introduces; this catches what emerges across pages over time.

<posture>

- **Read-only on the wiki.** Reinforcement of the allowed-tools restriction: never use Write or Edit. This skill produces information, not mutations.
- **Never touches `./raw/`.** No reads, no listing, no scanning. Findings about sources are derived from page front-matter only.
- **User-triggered, no cadence.** Runs only when invoked. It does not schedule itself or suggest a cadence.
- **Never acts on a finding.** Surface findings and stop; the user triggers every follow-up. Reason: routing a finding into a mutation would bypass the row-level approval that the ingest pipeline owns.
- **Ground every finding in text actually read.** Never report a contradiction, stale claim, duplicate, or missing link you have not verified against real page content. Reason: detection over unread pages is the primary fabrication surface for this skill.
- **Navigate, do not bulk-load.** Start from `index.md`, follow it to the relevant pages, read only those. For a large wiki, audit one tag or page at a time. Reason: practical quality degrades past roughly 200K-300K tokens, so hierarchical navigation is the access path, not an optimisation.

</posture>

<reasoning-output-contract>

Reason internally about detection. Emit only the findings list and the closing tally. Do not narrate the detection process. Reason: leaked reasoning corrupts the findings list the user scans to decide what to act on.

</reasoning-output-contract>

<reference-files>

| File | Load at | Condition |
|---|---|---|
| `.claude/rules/page-schema.md` | start | Always (defines the field names and shapes drift is measured against) |
| `references/checks.md` | start | Always (detection method per finding type) |

Load `page-schema.md` before any check that reads front-matter; checks 2, 6, and 7 depend on its `sources[]`, `source_title`, and `issued_date` field definitions.

</reference-files>

<invocation>

```
/wiki-audit [page-slug | tag | all]
```

| Argument | Meaning |
|---|---|
| (none) or `all` | Audit the whole wiki via `index.md`. |
| `<tag>` | Audit only pages carrying that tag. |
| `<page-slug>` | Audit that page and its link neighbours exactly one hop away. |

If the scope argument resolves to zero pages, report `No pages matched <arg>` and stop. Do not fabricate findings.

</invocation>

<procedure>

1. Read `index.md` to get the catalog. Resolve the scope argument to a working set of pages. If `index.md` is absent or empty, report that there is nothing to audit and stop.
2. Read the working-set pages, and for contradiction and cross-reference checks their one-hop link neighbours. Issue independent page reads and the link-graph greps in parallel; they have no interdependencies. Build the link graph by grepping `[[...]]` targets across pages.
3. Run each check in `references/checks.md` against the working set. Report every match per check; do not sample or truncate. Hold findings in memory.
4. Present findings using the output format below. Stop. Do not act on any finding.

</procedure>

<output-format>

Conversational markdown, no artefact, no row-level controls. Group findings by type. Each finding has these fields, in order: a short title, the page(s) involved as `[[slug]]`, a one-or-two-sentence why, and a `Route` whose value is one of the seven verbs in the Routes table.

```
## <finding type> (<count>)
- **<short title>** — [[page-a]], [[page-b]]. <why it matters>. Route: <route>.
```

Rules:
- If a check finds nothing, omit its section.
- If a single check exceeds 20 findings, report the 20 highest-impact and state the remaining count on a final line for that section. Reason: an unbounded list on a large wiki buries the findings worth acting on.
- When a match is borderline (a fuzzy near-duplicate, a maybe-missing page), report it with a leading `(low confidence)` marker rather than omitting it or asserting it. Reason: the user can weigh a flagged maybe; a silently-dropped or over-asserted one they cannot.
- End with a one-line tally: `Findings: N across M types. Nothing was changed.`

Worked example:

```
## Metadata drift (2)
- **q1-earnings.pdf title disagrees across pages** — [[tesla-inc]], [[dojo-supercomputer]]. One page calls it "Tesla Q1 2026 Earnings Report", the other "Q1 2026 Report"; same source_file. Route: re-ingest q1-earnings.pdf.
- **(low confidence) musk-bio.pdf issued_date** — [[elon-musk]]. Front-matter says 2023-09-12 but the inline citation quotes 2023. Route: re-ingest musk-bio.pdf.

## Orphan pages (1)
- **dojo-supercomputer has no inbound links** — [[dojo-supercomputer]]. No page links to it; likely new. Route: add cross-reference.

Findings: 3 across 2 types. Nothing was changed.
```

Edge case — a clean working set:

```
Findings: 0 across 0 types. Nothing was changed.
```

</output-format>

<routes>

This skill issues no wiki mutations. Each finding names the existing write surface the user would use next. The user decides and triggers it.

| Route | What the user does next |
|---|---|
| `re-ingest <source>` | Stale claim or metadata drift → `/ingesting-sources <source> --reingest`. |
| `ingest new source` | Data gap or missing content → place a source in `./raw/`, then `/ingesting-sources <file>`. |
| `web-search then ingest` | Data gap fillable externally → user runs a web search, files the result into `./raw/`, then ingests. |
| `create page` | Concept lacking a page → gather a source, then ingest so the page is created with provenance. |
| `add cross-reference` | Missing `[[link]]` → fold into the next ingest that touches the page. |
| `resolve duplicate` | Near-duplicate or latent collision → merge via an ingest report with a disambiguated or merged slug. |
| `investigate question` | Open question worth pursuing → track it; it becomes a future source to ingest. |

Route every correction through ingest or re-ingest so provenance and the commit trail stay intact. Reason: a hand-edit would leave a claim on a page with no source behind it, breaking the grounding invariant.

</routes>

| Field | Value |
|---|---|
| Version | 1.1 |
| Last Updated | 2026-05-31 |
| Status | Draft |
| Target Model | claude-opus-4-8 |
| Target Environment | claude-code |
