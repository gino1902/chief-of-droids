---
name: authoring-overview
description: Generate or refresh ./wiki/overview.md, the high-level synthesis and reading entry-point for the wiki. Navigates via index.md, identifies themes and the most central pages, reads a representative subset, and writes a narrative map that links to the pages it summarises. Regenerated on demand; it is a snapshot, not live. Owns overview.md exclusively. Read-only on every other page and on ./raw/. Commits the single file. Invoke when the user asks to generate, refresh, or rebuild the wiki overview.
disable-model-invocation: true
argument-hint: "[focus-tag]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash(git add *)
  - Bash(git commit *)
  - Bash(git status *)
---

<!-- target-model: claude-opus-4-8 | target-environment: claude-code | snapshot-ref: 2026-05-17 -->

# authoring-overview

Owns `./wiki/overview.md`: the high-level synthesis that tells a reader what the wiki holds and how its pieces relate, and serves as a hierarchical entry-point into the pages. It is a derived snapshot, regenerated on demand.

<posture>

- **Owns `overview.md` only.** This is the sole skill that writes `overview.md`. It writes no other page, never writes `index.md` or `log.md`, and never touches `./raw/`.
- **Reads every other page read-only.** Synthesise from pages; leave them unchanged.
- **Ground every statement in read text.** Summarise a page only from content you have opened. For a page you did not read, link it under a theme by its tag and title, but do not assert what it claims. Reason: synthesising from a title alone fabricates content the page may not support.
- **Traceability one hop.** Every claim in the overview links to the `[[pages]]` it summarises; the overview cites pages, not raw files. Reason: pages already carry provenance to `./raw/`, so citing raw here would duplicate that link and risk drift.
- **Navigate, do not bulk-load.** Read a representative subset, not the whole wiki. Reason: practical quality degrades past roughly 200K-300K tokens, and the overview's job is orientation, so link-graph coverage matters more than per-page completeness.

</posture>

<reasoning-output-contract>

Reason internally about theme and centre selection. Do not include reasoning steps in `overview.md` or in the user-facing confirmation. Reason: the overview is a clean reading surface; leaked selection reasoning clutters it.

</reasoning-output-contract>

<reference-files>

| File | Load at | Condition |
|---|---|---|
| `references/overview-template.md` | Write step | Always (section structure to fill) |

</reference-files>

<invocation>

```
/authoring-overview [focus-tag]
```

| Argument | Meaning |
|---|---|
| (none) | Synthesise the whole wiki. |
| `<focus-tag>` | Bias the synthesis toward pages carrying that tag while still situating them in the whole. Reason: a focused overview still needs the surrounding context to be a map rather than a fragment. |

If `<focus-tag>` matches no pages, report that and stop without writing.

</invocation>

<preconditions>

Resolve these before any synthesis:

1. No ingest report is pending (the wiki lock). If one is, the wiki is mid-flight; decline and ask the user to Apply or Cancel the ingest first.
2. `index.md` exists and is non-empty. If it is absent or empty, there is nothing to synthesise; tell the user and stop without writing.
3. `index.md` is parseable. If it is present but unparseable, stop and report the parse failure; do not synthesise from a partial read.

</preconditions>

<synthesis>

1. **Find themes and centres.** Group pages by tag to get themes. Build the link graph by grepping `[[...]]` targets across pages, running the independent reads and greps in parallel. The most-linked entity and concept pages are the centres.
2. **Read selectively.** Read all central pages, and one representative page per theme; read a second only when the theme spans clearly distinct sub-topics. Reason: one page anchors a theme's gist, a second adds range only when the theme is genuinely split.
3. **Scope of effort.** Surface every theme that has at least two pages. List key entities and key concepts with at least two inbound links, ordered by inbound-link count descending, capped at the top 10 of each. Keep each theme to one paragraph of at most three sentences. Reason: explicit cutoffs and caps remove the run-to-run variance that "representative" and "tight" otherwise leave to inference.
4. **Handle a sparse or flat wiki.** If no clear themes or centres emerge (a flat link graph, or pages with no tags), state that the wiki is too sparse or unstructured to synthesise and list the pages flatly rather than inventing groupings. Reason: inventing structure that the corpus does not support is a fabrication surface.
5. **Write `overview.md`.** Fill the structure in `references/overview-template.md`. Link every theme, entity, and concept to its `[[page]]`. Keep it a map: a reader should scan it and know where to go next, not read the pages over again.

</synthesis>

<commit>

Stage and commit `./wiki/overview.md` alone:

```
git add ./wiki/overview.md
git commit -m "overview: regenerate"
```

Confirm: `✓ overview.md regenerated and committed`. If the wiki was unchanged since the last overview and the content would be identical, say so and skip the commit. Proceed without asking once invoked; the only stop conditions are a pending lock, an absent or unparseable `index.md`, and a focus-tag that matches no pages.

</commit>

<staleness>

`overview.md` is a snapshot from its last generation, not a live view. Treat the linked pages as ground truth on any conflict; a statement in the overview is valid only as of its generation date, because later ingests change pages without re-deriving the overview. The header states this, and the user regenerates when they want it fresh. This skill does not auto-run at ingest time and does not schedule itself.

</staleness>

| Field | Value |
|---|---|
| Version | 1.1 |
| Last Updated | 2026-05-31 |
| Status | Draft |
| Target Model | claude-opus-4-8 |
| Target Environment | claude-code |
