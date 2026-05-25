# Wiki Framework — Brainstorm State (2026-05-25)

> Snapshot of the wiki framework design as of 2026-05-25.
> Grounds the FRAMING.md draft (`wiki-data/requirements/FRAMING.md`) into concrete design
> across three coupled sub-problems: ingest pipeline, versioning substrate, and
> page schema. Supersedes earlier v1.0 (2026-05-22) state.

---

## Context

FRAMING.md sketches a model-in-the-loop wiki: Claude ingests sources, the wiki
grows by integrating new content into existing entity/concept pages with
explicit governance. The framing left the operational mechanics implicit. This
brainstorm worked through three coupled sub-problems:

- **A** — How sources get ingested into the wiki with explicit user control
  (contradiction policy, granularity, approval mechanism).
- **B** — How wiki state is versioned and corrected over time.
- **C** — How individual pages are structured to support both ingest mechanics
  and human reading.

The design has evolved through two simplifications:

- Session 2026-05-22 (Challenge 4c): dropped the source-summary page type;
  introduced a sidecar-YAML pattern in `raw/` as the metadata layer.
- Session 2026-05-25: dropped the sidecar layer entirely; per-source metadata
  is now denormalized directly onto every citing page's front-matter.
  Concurrent decision: `raw/` is user-write-only — Claude never writes to it.

---

## Scope

The wiki lives under a single root directory (path parked; `wiki-data/` is the
current draft location). Three special files at root:

| File | Role |
| :--- | :--- |
| `index.md` | Master catalog of all pages |
| `log.md` | Chronological activity record |
| `overview.md` | High-level synthesis (out of session scope) |

Plus a `raw/` directory for immutable source files, and subdirectories
(structure parked) for entity/concept/synthesis pages.

**Out of scope this session:**

- Substrate / UI / renderer layering — operator marked "obvious"; Obsidian-first
  reading is assumed throughout.
- Subdirectory structure under wiki root.
- `overview.md` scope, generation, and maintenance mechanics.
- Categories beyond "tags as multi-categorization."

---

## Invariant — `raw/` access rule

`raw/` is closed to Claude by default. Two narrow exceptions:

**Read exception** — On ingest, Claude reads exactly the one source file named
in the trigger. No directory listing, no reads of sibling files, no scanning of
`raw/` for any purpose.

**Write exception** — None. Claude never creates, modifies, or deletes files in
`raw/`. Once the user has placed a file in `raw/`, the file content is
immutable. Renames or removals, if needed, are user actions.

**Git posture** — `raw/` is not tracked. The wiki repo's `.gitignore` excludes
`raw/`. Implications:

- Wiki commits cite raw filenames but the source files have no git presence.
  A fresh clone has dangling citations until `raw/` is restored out-of-band.
- The wiki is single-machine in posture; `raw/` backup is the user's
  responsibility outside this framework.
- Git history records when a page first cited a source (via `ingested_date` on
  the page's front-matter), not when the source itself arrived in `raw/`.
- At every ingest start, Claude echoes a reminder of this posture to the user
  (see pipeline step 3).

This rule applies only to `raw/`. The wiki side (pages + `index.md` + `log.md`)
has the inverse rule: Claude reads and writes freely via the ingest pipeline;
no Obsidian hand-edits (see B.6).

---

## Decisions made in this brainstorm

### A. Contradiction & ingest pipeline

| # | Decision |
| :--- | :--- |
| A.1 | Detection point: at ingest, by Claude, surfaced in a report artefact before any wiki mutation. |
| A.2 | Resolution posture: defer to user. Claude proposes per-row actions; user decides. |
| A.3 | Granularity: section / subsection / sub-subsection / claim — coarsest level where action is atomic. Recursion into finer levels when 80/20 splits inside a section need different actions. |
| A.4 | Policy set: `replace`, `supersede`, `coexist`. (Earlier "evolve" label renamed to `coexist` for verb-symmetry and outcome-accuracy.) |
| A.5 | Report structure: four tables + editable `log.md` entry preview. |
| A.6 | Approval mechanism: row-level approve / edit / reject. Report rendered as artefact (per-row controls), not chat markdown. |
| A.7 | Cross-row dependency handling: `Depends on` column declared by Claude; local rejection allowed; apply blocks if approved set contains dangling references — user resolves manually. |
| A.8 | Source-item cell format: title visible; verbatim quote in expandable drawer. Title comes from extraction of raw content (for new sources) or from target-page front-matter `sources[]` lookup (for existing sources). |
| A.9 | Stale-report protection: whole-wiki lock — one pending report at a time. Lock release = commit (apply) or cancel. Lock scope is the wiki write surface (pages + `index.md` + `log.md`); `raw/` is unaffected since Claude doesn't write there. |
| A.10 | Temporal rule: "newer wins" as default heuristic (technology domain, ~80% of ingestions). Older-source-contradicting-newer-wiki → propose `do not add`. Dates surfaced in Table 3 with anomaly flag (⚠️). Existing date comes from target-page front-matter `sources[]`; new date comes from extraction of raw content at ingest. User overrides the 20%. |

**Report tables (header schemas):**

```
Table 1 — Modifications to existing pages
RowID | Category | Source item (drawer) | Destination | Description | Depends on

Table 2 — Proposed page creations
RowID | Category | Source item (drawer) | Destination | Description | Depends on

Table 3 — Conflicts
RowID | Category | Source item (drawer) | Action [replace/supersede/coexist]
      | Existing content (drawer) | Document dates (new / existing) | ⚠️
      | Destination | Description | Depends on

Table 4 — Link updates
RowID | Source page | Target page | Action [add/update/remove] | Depends on
```

`Category` ∈ {section, subsection, sub-subsection, claim}.
`Document dates` cell shows `issued_date_new / issued_date_existing`; new comes
from raw-content extraction, existing from target-page front-matter. Anomaly
flag set when "newer wins" suggests `do not add`.

**Editable fields by table:** Destination, Description, Action dropdowns. Read-only: RowID, Category, Source item, Existing content, Source page.

**Pipeline:**

```
1. User places source S in raw/ (Claude does not write to raw/; raw/ is gitignored)
2. User triggers ingest, naming S
3. Claude echoes raw/ posture reminder:
   "Note: raw/ is not under git. Source file 'S' exists only on your local
    disk. Ensure it is backed up separately if you rely on it."
   (Echoed every ingest.)
4. Wiki lock acquired (refuse if another report is pending)
5. Claude reads S (and only S) from raw/, analyses content
6. Claude identifies candidate target pages, reads each, applies policies
   (newer-wins, replace/supersede/coexist, do-not-add)
7. Claude emits Report artefact (4 tables + editable log entry)
8. User reviews row-by-row: approve / edit / reject
9. On Apply:
   a. Dangling-reference check across approved rows
   b. If inconsistent → block, user resolves
   c. If clean → mutate wiki (pages + index.md + log.md), git commit,
      release lock
10. Cancel: release lock, no mutations
```

**Operationalization deferred to ingest skill (TBD).** The `log.md` entry
schema (O.2) and the `index.md` generation mechanics (O.1) are seeded in this
doc and finalized in the skill. See Backlog cross-references.

### B. Versioning substrate

| # | Decision |
| :--- | :--- |
| B.1 | Architecture: markdown-first (provisional; revisit triggers logged below). |
| B.2 | Versioning mechanism: git. Wiki folder is a git repo. `raw/` is gitignored (see Invariant). |
| B.3 | Commit granularity: one commit per applied report (atomic, clean log). |
| B.4 | Commit message: auto-generated subject line + `log.md` entry body. |
| B.5 | Ingest serialization: a report must be applied (committed) or cancelled before the next ingest can start. Commit = lock release. |
| B.6 | Hand-edits via Obsidian: not supported on the wiki side. Ingest-only writes. (`raw/` has the inverse rule — see Invariant section: user-only writes; ungitted.) |
| B.7 | Correction path (wiki side): full ingest for everything (including typos). For per-source metadata corrections, see Trust posture below. |
| B.8 | Enforcement: convention only, documented. No file-system locks, no git hooks. |

**Revisit triggers for B.1** (would push toward hybrid or claim-first architecture):

- Cross-page queries become routine ("all claims by author X", "all pages touching entity Y").
- Structural conventions (front-matter, naming, claim formatting) start drifting.
- Sub-problem A report generation becomes hard because Claude has to parse loose markdown semantics.

### C. Page schema

| # | Decision |
| :--- | :--- |
| C.1 | Page typology: 3 types — `entity`, `concept`, `synthesis`. Source-summary page type dropped in v1.0 (replaced by inline citation + denormalized front-matter; no sidecar layer as of v1.1). |
| C.2 | Page typology is loose: Claude assigns at ingest based on source content and existing wiki shape; user overrides via report. |
| C.3 | Sources live in `raw/` as immutable files. `raw/` is user-write-only and ungitted (see Invariant section). No sidecar layer; per-source metadata is denormalized onto every citing page's front-matter. |
| C.4 | Citation links resolve directly to raw files: `[[musk-bio.pdf]]`. Obsidian backlinks work natively. |
| C.5 | Universal page shape: YAML front-matter + flexible markdown body using H2/H3 conventions. H1 = page title (front-matter `title` mirrors). |
| C.6 | Provenance: section-level attribution. Italic line `*Sources: [[source_file]] "source_title"*` immediately after each heading (section / subsection / sub-subsection). Multiple sources comma-separated. Child sections inherit parent sources unless overridden. For **claim-level** attribution where no heading anchors the citation, use markdown footnote syntax: `[^id]` inline after the claim sentence, with definitions `[^id]: [[source_file]] "source_title"` at the end of the containing section. Footnote ID scoping is parked (O.8). |
| C.7 | Front-matter `sources[]` is denormalized: list of objects with `source_file`, `source_title`, `issued_date`, `ingested_date`. Optimization for read-heavy contradiction-policy workload. Drift mitigation via cross-page consistency lint at apply (O.5). |
| C.8 | Filename: slug only; no mandated date prefix or pattern. (Applies to wiki pages; `raw/` filenames are user-chosen.) |
| C.9 | No `subtype` field; replaced by free-text `description` (one-line summary, also surfaced in `index.md`). |
| C.10 | Filed user synthesis (query answers filed back) is authored as markdown and placed in `raw/` by the user (per the user-write-only invariant). At the next ingest it is treated like any other source; per-source metadata flows into citing-page front-matter through the report. |
| C.11 | No `## Cross-references` section; rely on inline `[[wiki-links]]` + Obsidian backlinks. |
| C.12 | No page-level `status` field (supersede semantics live in section-level annotations only). |

**Page front-matter (entity / concept / synthesis):**

```yaml
---
title: Tesla, Inc.
description: American electric vehicle and clean energy company, founded 2003.
aliases: [Tesla, TSLA]
type: entity
created: 2026-05-21
updated: 2026-05-21
sources:
  - source_file: musk-bio.pdf
    source_title: Elon Musk Biography
    issued_date: 2023-09-12
    ingested_date: 2026-05-20
  - source_file: q1-earnings.pdf
    source_title: Tesla Q1 2026 Earnings Report
    issued_date: 2026-04-10
    ingested_date: 2026-04-15
tags: [auto-industry, ev]
---

# Tesla, Inc.

## Overview
*Sources: [[musk-bio.pdf]] "Elon Musk Biography"*

Body...

## History
*Sources: [[musk-bio.pdf]] "Elon Musk Biography", [[q1-earnings.pdf]] "Tesla Q1 2026 Earnings Report"*

### Founding

Inherits H2 sources.

### Recent developments
*Sources: [[q1-earnings.pdf]] "Tesla Q1 2026 Earnings Report"*

Overrides H2 sources.

The Model S launched in 2012[^musk-2012-modelS].

[^musk-2012-modelS]: [[musk-bio.pdf]] "Elon Musk Biography"
```

`raw/` source files are immutable. `raw/` is user-write-only and ungitted
(see Invariant section). All per-source metadata lives on the citing pages'
front-matter.

### Entity definition (canonical text for requirements)

> An **entity** is a named referent that exists in the world and can be the
> subject of claims: people, organizations, places, physical products, named
> systems, named datasets, named laws, named events. A **concept** is an
> abstract idea, theory, framework, method, or term-of-art defined by
> characteristics rather than identity.
>
> **Boundary heuristic:** if the thing is named and can be pointed at →
> entity. If it's an abstraction defined by properties → concept. Topics
> that are neither (e.g. "Tesla's safety record") belong as sections on an
> existing entity/concept page, or as synthesis pages if cross-source
> synthesis exists.

### index.md schema (seed — operationalization deferred to ingest skill)

| Aspect | Decision |
| :--- | :--- |
| Role | Master catalog; derived projection of page front-matter |
| Columns per page | `title`, `type`, `description`, `created`, `updated` |
| Grouping | By `tags` (multi-category via tags). A page tagged with N tags appears under N groups. |
| `aliases` | Not surfaced in `index.md`; remains in page front-matter only |
| Canonical source | Page front-matter. `index.md` is regenerated, not hand-edited |
| Generation timing | At each `Apply` of an ingest report (skill-side mechanics) |

Open mechanics (trigger plumbing, exact markdown shape, multi-tag grouping
render) are finalized in the ingest skill.

### Source-metadata corrections — Trust posture

Per-source metadata in page front-matter (`source_title`, `issued_date`) can be
wrong — Claude may have misread a date or title at first ingest. Inline
section-attribution titles and footnote-definition titles can also be wrong for
the same reason. There is no separate metadata artefact to correct (the sidecar
layer is gone); page front-matter and the inline citation lines are the only
places that carry per-source metadata.

Correction path is **full re-ingest of the source**:

1. User triggers re-ingest of the source file (by name; per the `raw/` access
   rule, Claude reads only the named file).
2. Claude re-reads the immutable raw file.
3. Claude re-extracts `source_title` and `issued_date`.
4. Claude greps citing pages (those with the source filename in their `sources[]`).
5. Claude generates a fresh report:
   - Table 1 rows: update each citing page's `sources[]` entry (new
     `source_title`, `issued_date`); update inline section-attribution lines
     and footnote definitions where the title appears.
   - `ingested_date` is **not** updated — it records when each page first
     cited the source.
6. User approves, applies.

Re-ingest may surface unrelated content changes Claude missed first time —
user rejects rows that aren't wanted.

### Claude role in this project

Act as a Knowledge Curation Architect for a persistent markdown wiki.
Your mission is to build and maintain a curated information base from immutable raw sources. For every new document, extract key claims, entities, concepts, definitions, relationships, contradictions, open questions, and source references. Integrate them into the existing wiki by updating relevant pages, creating new pages only when needed, resolving duplication, flagging conflicts, and preserving traceability to the original sources.
Prioritize accuracy, freshness, structure, reuse, and long-term maintainability over quick summarization.

---

## Open items

| # | Item | Status | Notes |
| :--- | :--- | :--- | :--- |
| O.1 | `index.md` generation mechanics | Deferred to ingest skill | Trigger, generator, markdown shape, multi-tag grouping render. Seed spec retained under section C; finalized in skill. |
| O.2 | `log.md` entry schema | Deferred to ingest skill | Date, source, row counts, references; shape of editable preview in report. Seeded under A.5; finalized in skill. |
| O.3 | `overview.md` | Deferred to overview skill | Scope, generation, maintenance. No spec fragments in this doc — skill starts from scratch. |
| O.4 | Subdirectory structure under wiki root | Deferred (later) | Categorization layout for pages. |
| O.5 | Cross-page front-matter `sources[]` consistency lint at apply | Open | Every citing page should agree on (`source_title`, `issued_date`) for the same `source_file`. Mismatches block apply and surface for user resolution. Also extends to inline citation-line title strings vs front-matter `source_title`. |
| O.6 | Naming-collision handling | Open | When Claude proposes a slug that already exists (suffix? disambiguator? user prompt?) |
| O.7 | Section-attribution and footnote parser strictness | Open | How strict the `*Sources: [[a]] "Title"*` and `[^id]: [[a]] "Title"` formats must be; malformed-line handling. Elevated importance because the section-attribution / footnote lines are now the only inline carriers of source-title. |
| O.8 | Footnote ID scoping | Open | Page-scoped or section-scoped? ID format convention (e.g. `[^musk-2012-modelS]`). Where footnote definitions live (end of containing section vs end of page). |
| O.9 | Inline title vs front-matter title divergence | Open | If the inline title and front-matter `source_title` for the same `source_file` ever differ on the same page, which one wins? Lint surfaces; resolution is user-side at apply time. |
| O.10 | `raw/` git lifecycle | **Resolved** | `raw/` is gitignored. Question collapses. See Invariant — Git posture. |

---

## Residual risks (flagged, not resolved)

| # | Risk |
| :--- | :--- |
| R.1 | `Depends on` is Claude-declared — apply-time dangling check is only as good as Claude's declaration. Mitigation candidate: post-apply integrity scan (out of scope). |
| R.2 | Section-attribution italic-line format and footnote-definition format are fragile; relies on strict pipeline adherence and not being hand-edited. Elevated since the sidecar layer is gone — these lines plus front-matter `sources[]` are the only metadata carriers. |
| R.3 | Front-matter `sources[]` denormalization can drift across pages (different titles or dates for the same `source_file`). Cross-page consistency lint at apply (O.5) is the planned mitigation. |
| R.4 | "Convention only" enforcement of the `raw/` access rule (B.6, B.8) is willpower-dependent — covers both the read constraint (only the named file per ingest, no listing or sibling reads) and the write constraint (no writes ever). `raw/` being ungitted means git is not even a passive witness if discipline slips. Pre-ingest dirty-tree check is a candidate future tripwire. |
| R.5 | File format is informational only — inferred from filename extension. No policy distinction by format. Manual notes, PDFs, transcripts, etc. all flow through the same ingest pipeline; user judgment handles the cases where format matters. |
| R.6 | Re-ingest (for source-metadata correction) may surface unrelated content changes — user must reject rows they don't want. Mildly annoying; accepted trade-off. |
| R.7 | The framing case where "newer wins" is wrong (primary sources, foundational texts, historical records) — surfaced in Table 3 dates column for user override; defaults still favor newer. |
| R.8 | Inline citation-line title and front-matter `source_title` for the same `source_file` can diverge on the same page (typo in one but not the other). Lint at apply (O.5 extension) is the mitigation. |
| R.9 | `raw/` ungitted → no portability. A fresh clone has dangling citations until `raw/` is restored out-of-band. Single-machine posture assumed. Every-ingest echo (pipeline step 3) keeps this visible to the user. |

---

## Limitations (not flagged, not resolved)

### Context window degradation

Multiple users reported that quality degrades when the wiki grows beyond what fits in context. Despite 1M+ token context windows, practical degradation starts around 200K-300K tokens. The LLM starts missing connections or producing inconsistent pages.

Mitigation: This is why the index/navigation pattern matters. Instead of loading the entire wiki, the LLM reads `index.md` (a few thousand tokens), identifies relevant pages, and reads only those. Hierarchical navigation sidesteps brute-force context stuffing.

### Model collapse risk

User **devnullbrain** raised concerns about information degradation through repeated LLM rewriting — the wiki version of model collapse. Each rewrite potentially introduces subtle errors that compound over time.

Mitigation: The immutable `raw/` layer is the safeguard. Every claim in the wiki should trace back to a source in `raw/`. Lint operations check for drift (cross-page consistency on `sources[]` per O.5). And Git provides full history to identify when claims changed.

### Complexity ceiling

User **kubb** warned that these systems collapse beyond certain complexity thresholds when neither the agent nor the developer maintains sufficient comprehension of the whole.

Mitigation: This is a real constraint. The pattern works best for personal/team knowledge at the 50-200 source scale. Beyond that, you likely need the extensions from LLM Wiki v2 (hybrid search, multi-agent governance) or a proper RAG pipeline.

---

## Backlog cross-references

| Task / file | Relationship to this work |
| :--- | :--- |
| `wiki-data/requirements/FRAMING.md` | Source framing for this brainstorm. This document grounds the framing into operational design. Three of the original "Next steps to discuss" items (sources format, categories, tools) are substantially covered. Two remain: `overview.md`, and subdirectory structure. |
| Ingest skill (TBD) | The Sub-problem A pipeline needs to be encoded as a skill (`ingesting-sources` or similar). Report artefact rendering, row-level approval, apply mechanics — all skill territory. Extraction of `source_title` and `issued_date` from raw content is part of the pipeline contract. **Absorbs operationalization of `index.md` generation (O.1) and `log.md` entry schema (O.2); seeds for both retained in this doc.** |
| Overview skill (TBD) | Owns `overview.md` scope, generation, and maintenance (O.3). No spec seeds in this doc — skill starts from scratch. |
| `managing-tasks` skill | Each Apply produces a git commit; managing-tasks writes are pre-approved per CLAUDE.md. Tasks created during ingest (e.g. "review O.5 lint") flow through normal task hygiene. |

---

## Resume hint

Open a new session in the Chief of Droids Claude Desktop project, then prompt:

> Resume the wiki framework brainstorm. Read
> `wiki-data/requirements/2026-05-22-wiki-framework-requirements.md`.
> Pick up at the next active open item (O.5 — cross-page consistency lint —
> is a natural next; O.6–O.9 are smaller and also open). O.1, O.2, O.3 have
> moved out to skill scope; O.4 deferred; O.10 resolved.
> Use brainstorming-ideas skill in resume mode.

The brainstorming-ideas skill Phase 0 resume check will find this file,
acknowledge the state, and continue from the chosen open item.

---

## Changelog

| From | To | Date | Change |
| :--- | :--- | :--- | :--- |
| — | v1.0 | 2026-05-22 | Initial requirements doc — three sub-problems resolved; source-summary page type dropped; sidecar-YAML pattern introduced for source metadata. |
| v1.0 | v1.1 | 2026-05-25 | Sidecar layer dropped entirely; per-source metadata denormalized to page front-matter. Front-matter `sources[]` schema: `source_file`, `source_title`, `issued_date`, `ingested_date`. New invariant: `raw/` is user-write-only. Section-attribution syntax extended with inline `"source_title"`. Claim-level attribution via markdown footnote syntax added. Pipeline step 5 (read affected pages) made explicit. Trust posture rewritten around front-matter as canonical. O.5 reframed; O.8, O.9, O.10 added. R.5 reframed; R.8 added. FRAMING.md path updated to `wiki-data/requirements/FRAMING.md` (file moved). |
| v1.1 | v1.2 | 2026-05-25 | `raw/` invariant renamed write rule → **access rule** and rewritten as closed-by-default with two narrow exceptions: read on ingest (only the named file — no listing, no sibling reads, no scans) and no write exception. R.4 expanded to cover both read and write constraints under convention-only enforcement. Pipeline step 2 names S explicitly; step 4 emphasises "and only S". Trust posture step 1 references the access rule. |
| v1.2 | v1.3 | 2026-05-25 | `raw/` git posture defined: untracked (gitignored). Every-ingest echo of the posture added as pipeline step 3 (subsequent steps renumbered). O.10 resolved (collapsed by ungitted `raw/`). O.1 and O.2 deferred to ingest skill; spec fragments retained as skill seeds and annotated in-doc. O.3 deferred to a new overview skill (added to Backlog). O.4 marked deferred (later). R.4 expanded: ungitted `raw/` removes git as passive witness. R.9 added: portability lost on clone; every-ingest echo keeps it visible. Open items table gained a Status column. Resume hint updated. |

---

| Field | Value |
| :--- | :--- |
| Version | 1.3 |
| Last Updated | 2026-05-25 |
| Status | Draft |
