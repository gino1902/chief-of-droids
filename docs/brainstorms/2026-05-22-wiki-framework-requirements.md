# Wiki Framework — Brainstorm State (2026-05-22)

> Snapshot of the wiki framework design discussion at session end on 2026-05-22.
> Grounds the FRAMING.md draft (`wiki-data/FRAMING.md`) into concrete design
> across three coupled sub-problems: ingest pipeline, versioning substrate, and
> page schema. Replaces the FRAMING.md "Next steps to discuss" section, which
> proved too narrow — the actual high-leverage tensions were upstream of those
> three items.

---

## Context

FRAMING.md sketches a model-in-the-loop wiki: Claude ingests sources, the wiki
grows by integrating new content into existing entity/concept pages with
explicit governance. The framing left the operational mechanics implicit. This
session worked through three coupled sub-problems:

- **A** — How sources get ingested into the wiki with explicit user control
  (contradiction policy, granularity, approval mechanism).
- **B** — How wiki state is versioned and corrected over time.
- **C** — How individual pages are structured to support both ingest mechanics
  and human reading.

The session reached a stable design for all three. A significant
simplification mid-session (Challenge 4c) dropped the source-summary page type
entirely, replaced by a sidecar-YAML pattern in `raw/`.

---

## Scope

The wiki lives under a single root directory (path parked; `wiki-data/` is the
current draft location). Three special files at root:

| File | Role |
| :--- | :--- |
| `index.md` | Master catalog of all pages |
| `log.md` | Chronological activity record |
| `overview.md` | High-level synthesis (out of session scope) |

Plus a `raw/` directory for immutable source files with their sidecar metadata,
and subdirectories (structure parked) for entity/concept/synthesis pages.

**Out of scope this session:**

- Substrate / UI / renderer layering — operator marked "obvious"; Obsidian-first
  reading is assumed throughout.
- Subdirectory structure under wiki root.
- `overview.md` scope, generation, and maintenance mechanics.
- Categories beyond "tags as multi-categorization."

---

## Decisions made this session

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
| A.8 | Source-item cell format: title visible; verbatim quote in expandable drawer. |
| A.9 | Stale-report protection: whole-wiki lock — one pending report at a time. Lock release = commit (apply) or cancel. |
| A.10 | Temporal rule: "newer wins" as default heuristic (technology domain, ~80% of ingestions). Older-source-contradicting-newer-wiki → propose `do not add`. Dates surfaced in Table 3 with anomaly flag (`⚠️`); user overrides the 20%. |

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
`Document dates` cell shows `issued_date_new / issued_date_existing`; anomaly flag set when "newer wins" suggests `do not add`.

**Editable fields by table:** Destination, Description, Action dropdowns. Read-only: RowID, Category, Source item, Existing content, Source page.

**Pipeline:**

```
1. User submits source S (file in raw/ or manual note)
2. Wiki lock acquired (refuse if another report is pending)
3. Claude analyses S against current wiki state
4. Claude emits Report artefact (4 tables + editable log entry)
5. User reviews row-by-row: approve / edit / reject
6. On Apply:
   a. Dangling-reference check across approved rows
   b. If inconsistent → block, user resolves
   c. If clean → mutate wiki, append log.md, git commit, release lock
7. Cancel: release lock, no mutations
```

### B. Versioning substrate

| # | Decision |
| :--- | :--- |
| B.1 | Architecture: markdown-first (provisional; revisit triggers logged below). |
| B.2 | Versioning mechanism: git. Wiki folder is a git repo. |
| B.3 | Commit granularity: one commit per applied report (atomic, clean log). |
| B.4 | Commit message: auto-generated subject line + `log.md` entry body. |
| B.5 | Ingest serialization: a report must be applied (committed) or cancelled before the next ingest can start. Commit = lock release. |
| B.6 | Hand-edits via Obsidian: not supported. Ingest-only writes. |
| B.7 | Correction path: full ingest for everything (including typos). |
| B.8 | Enforcement: convention only, documented. No file-system locks, no git hooks. |

**Revisit triggers for B.1** (would push toward hybrid or claim-first architecture):

- Cross-page queries become routine ("all claims by author X", "all pages touching entity Y").
- Structural conventions (front-matter, naming, claim formatting) start drifting.
- Sub-problem A report generation becomes hard because Claude has to parse loose markdown semantics.

### C. Page schema

| # | Decision |
| :--- | :--- |
| C.1 | Page typology: 3 types — `entity`, `concept`, `synthesis`. Source-summary page type dropped (replaced by sidecar pattern). |
| C.2 | Page typology is loose: Claude assigns at ingest based on source content and existing wiki shape; user overrides via report. |
| C.3 | Sources live in `raw/` as immutable files, each with a sidecar YAML for metadata. No source-summary page. |
| C.4 | Citation links resolve directly to raw files: `[[musk-bio.pdf]]`. Obsidian backlinks work natively. |
| C.5 | Universal page shape: YAML front-matter + flexible markdown body using H2/H3 conventions. H1 = page title (front-matter `title` mirrors). |
| C.6 | Provenance: section-level attribution. Italic line `*Sources: [[a]], [[b]]*` immediately after each heading. Child sections inherit parent sources unless overridden. |
| C.7 | Front-matter `sources[]` is denormalized: list of objects with `id`, `ingested`, `issued`. Optimization for read-heavy contradiction-policy workload. Drift handled via Trust posture (full re-ingest if source metadata needs correction). |
| C.8 | Filename: slug only; no mandated date prefix or pattern. |
| C.9 | No `subtype` field; replaced by free-text `description` (one-line summary, also surfaced in `index.md`). |
| C.10 | Filed user synthesis (query answers filed back) goes into `raw/` as markdown + sidecar (`source_format: synthesis`, `source_author: <user>`). Treated like any other source by the pipeline. |
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
  - id: musk-bio
    ingested: 2026-05-20
    issued: 2023-09-12
  - id: q1-earnings
    ingested: 2026-04-15
    issued: 2026-04-10
tags: [auto-industry, ev]
---

# Tesla, Inc.

## Overview
*Sources: [[musk-bio.pdf]]*

Body...

## History
*Sources: [[musk-bio.pdf]], [[q1-earnings.pdf]]*

### Founding

Inherits H2 sources.

### Recent developments
*Sources: [[q1-earnings.pdf]]*

Overrides H2 sources.
```

**Sidecar YAML (per `raw/` source):**

```yaml
# raw/musk-bio.yaml
title: Elon Musk Biography
description: Walter Isaacson biography of Musk; Tesla chapters 8-14 most relevant.
aliases: [musk-bio-isaacson, isaacson-musk]
source_format: pdf            # pdf | url | docx | video | podcast | note | synthesis | ...
source_url: https://...        # optional
source_file: raw/musk-bio.pdf  # optional (absent for url-only sources)
source_author: Walter Isaacson
issued_date: 2023-09-12
ingested_date: 2026-05-20
```

For `source_format: note`, `source_url` and `source_file` are absent; `issued_date` defaults to `ingested_date` if not specified.

`raw/` source files are immutable. Sidecar YAML is mutable but written only by the ingest pipeline (no hand-edits per B.6).

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

### index.md schema

| Aspect | Decision |
| :--- | :--- |
| Role | Master catalog; derived projection of page front-matter |
| Columns per page | `title`, `type`, `description`, `created`, `updated` |
| Grouping | By `tags` (multi-category via tags). A page tagged with N tags appears under N groups. |
| `aliases` | Not surfaced in `index.md`; remains in page front-matter only |
| Canonical source | Page front-matter. `index.md` is regenerated, not hand-edited |
| Generation timing | At each `Apply` of an ingest report (open mechanism — see Open items) |

### Source-metadata corrections — Trust posture

Sidecar YAML can be wrong (Claude misread a date, etc.). Correction path is
**full re-ingest of the source**: Claude re-reads the immutable raw file,
generates a fresh report. Table 1 modification rows propagate updated dates
to every citing page's denormalized `sources[]`. User approves, applies, done.

No special "source correction" ingest type. Existing pipeline handles
propagation. Re-ingest may surface other content changes Claude missed first
time — user rejects rows that aren't wanted.


### Claude role in this project

Act as a Knowledge Curation Architect for a persistent markdown wiki.
Your mission is to build and maintain a curated information base from immutable raw sources. For every new document, extract key claims, entities, concepts, definitions, relationships, contradictions, open questions, and source references. Integrate them into the existing wiki by updating relevant pages, creating new pages only when needed, resolving duplication, flagging conflicts, and preserving traceability to the original sources.
Prioritize accuracy, freshness, structure, reuse, and long-term maintainability over quick summarization.

---

## Open items (deferred)

| # | Item | Notes |
| :--- | :--- | :--- |
| O.1 | `index.md` generation mechanics | Triggered when, by what, markdown shape, multi-tag grouping rendering |
| O.2 | `log.md` entry schema | Date, source, row counts, references — shape of the editable preview in report |
| O.3 | `overview.md` | Scope, generation, maintenance |
| O.4 | Subdirectory structure under wiki root | Categorization layout for pages |
| O.5 | Sidecar YAML lint at apply | Verify denormalized front-matter `sources[].issued` matches sidecar `issued_date`; surface drift in apply blocker |
| O.6 | Naming-collision handling | When Claude proposes a slug that already exists (suffix? disambiguator? user prompt?) |
| O.7 | Section-attribution parser strictness | How strict the `*Sources: [[a]], [[b]]*` format must be; malformed-line handling |

---

## Residual risks (flagged, not resolved)

| # | Risk |
| :--- | :--- |
| R.1 | `Depends on` is Claude-declared — apply-time dangling check is only as good as Claude's declaration. Mitigation candidate: post-apply integrity scan (out of scope). |
| R.2 | Section-attribution italic-line format is fragile; relies on strict pipeline adherence and not being hand-edited. |
| R.3 | Front-matter `sources[]` denormalization can drift if pipeline has bugs. Lint at apply (O.5) is the planned mitigation. |
| R.4 | "Convention only" enforcement of ingest-only writes (B.8) is willpower-dependent. Pre-ingest dirty-tree check is a candidate future tripwire if discipline slips. |
| R.5 | Manual notes have no source-format-based policy distinction. `source_format` is surfaced in reports; user judgment handles the cases that matter. |
| R.6 | Re-ingest (for source-metadata correction) may surface unrelated content changes — user must reject rows they don't want. Mildly annoying; accepted trade-off. |
| R.7 | The framing case where "newer wins" is wrong (primary sources, foundational texts, historical records) — surfaced in Table 3 dates column for user override; defaults still favor newer. |

---

## Limitations (not flagged, not resolved)

### Context window degradation

Multiple users reported that quality degrades when the wiki grows beyond what fits in context. Despite 1M+ token context windows, practical degradation starts around 200K-300K tokens. The LLM starts missing connections or producing inconsistent pages.

Mitigation: This is why the index/navigation pattern matters. Instead of loading the entire wiki, the LLM reads index.md (a few thousand tokens), identifies relevant pages, and reads only those. Hierarchical navigation sidesteps brute-force context stuffing.

### Model collapse risk

User **devnullbrain** raised concerns about information degradation through repeated LLM rewriting — the wiki version of model collapse. Each rewrite potentially introduces subtle errors that compound over time.

Mitigation: The immutable raw/ layer is the safeguard. Every claim in the wiki should trace back to a source in raw/. Lint operations check for drift. And Git provides full history to identify when claims changed.

### Complexity ceiling

User **kubb** warned that these systems collapse beyond certain complexity thresholds when neither the agent nor the developer maintains sufficient comprehension of the whole.

Mitigation: This is a real constraint. The pattern works best for personal/team knowledge at the 50-200 source scale. Beyond that, you likely need the extensions from LLM Wiki v2 (hybrid search, multi-agent governance) or a proper RAG pipeline.

---

## Backlog cross-references

| Task / file | Relationship to this work |
| :--- | :--- |
| `wiki-data/FRAMING.md` | Source framing for this brainstorm. This document grounds the framing into operational design. Three of the original "Next steps to discuss" items (sources format, categories, tools) are substantially covered. Two remain: `overview.md`, and subdirectory structure. |
| Ingest skill (TBD) | The Sub-problem A pipeline needs to be encoded as a skill (`ingesting-sources` or similar). Report artefact rendering, row-level approval, apply mechanics — all skill territory. |
| `managing-tasks` skill | Each Apply produces a git commit; managing-tasks writes are pre-approved per CLAUDE.md. Tasks created during ingest (e.g. "review O.5 lint") flow through normal task hygiene. |

---

## Resume hint

Open a new session in the Chief of Droids Claude Desktop project, then prompt:

> Resume the wiki framework brainstorm. Read
> `docs/brainstorms/2026-05-22-wiki-framework-requirements.md`.
> Pick up at the next open item (start with O.1 — index.md generation mechanics).
> Use brainstorming-ideas skill in resume mode.

The brainstorming-ideas skill Phase 0 resume check will find this file,
acknowledge the state, and continue from the chosen open item.

---

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-05-22 |
| Status | Draft |
