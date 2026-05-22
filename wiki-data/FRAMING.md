# wiki-data — Project framing

## Context

The project builds a curated, trusted, and continuously maintained information base that becomes the organization's reference layer for answering questions, validating claims, and reusing knowledge across documents, teams, and decisions.

Unlike query-time RAG, which retrieves relevant chunks and answers each question from scratch, the solution is to build a persistent markdown wiki from sources, continuously integrating updates, contradictions, entities, and synthesis. This ensures query result quality, with consistent, accurate, and fresh information.

## Roles

User role is to feed the raw sources — a curated collection of documents in different formats: PDF, data, images, HTML.

Claude's role is to build the wiki incrementally from the raw sources and to provide the user with QA reports.

## Implementation

Three workflows to build:

### Ingest

User drops a new source into the raw collection and tells the LLM to process it. Claude reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10–15 wiki pages.

Sources are ingested one at a time — human in the loop. User reads the summaries, checks the updates, and guides Claude on what to emphasize.

Later, when the workflow is reliable, a batch-ingest solution with less supervision will be implemented.

### Query

User asks / routes questions against the wiki. Claude searches for relevant pages, reads them, and synthesizes an answer with citations. Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (using Marp tool), a chart (using matplotlib tool), a canvas.

Upon user decision on Claude's prompt, valuable answers can be filed back into the wiki as new pages.

### Lint

User asks the LLM to health-check the wiki.

Health criteria — not limited to; Claude may propose more:

- No contradictions between pages
- No stale claims that newer sources have superseded
- No orphan pages with no inbound links
- Every important concept mentioned has its own page
- No missing cross-references
- No data gaps that could be filled with a web search

The LLM is good at suggesting new questions to investigate and new sources to look for. This keeps the wiki healthy as it grows.

> Note: propose

## Special files

Two special files will support wiki navigation and activity tracking.

### index.md

Content-oriented file. It's a catalog of everything in the wiki — each page listed with a link, a one-line summary, and metadata like date or source count. Organized by category.

Claude updates it on every ingest. When answering a query, Claude reads the index first to find relevant pages, then drills into them.

### log.md

Chronological content file. It's an append-only record of what happened and when: ingests, queries, lint passes.

Each entry starts with a consistent prefix (e.g. `## [2026-04-02] ingest | Article Title`).

A simple Unix tool — `grep "^## \[" log.md | tail -N` — can give the user the last N entries or updated entries.

The log gives a timeline of the wiki's evolution and helps Claude understand what's been done recently.

### category

Park for now.

## Implementation guidelines

- CLAUDE.md must be authored by Claude, based on https://code.claude.com/docs/en/memory
- Auto memory is disabled
- User-only information must go between `<!-- ... -->`
- Project settings must be configured

## Next steps to discuss

1. Discuss raw sources format and the best way to store them, and how Claude should convert them into the wiki.
   - Example: what do we do for an image — does Claude describe it, or convert it into a JSON file with metadata? How does Claude decide?
   - Another example: any skill to recommend for handling the conversion?
   - What is the best way to organize the sources? Per format?
   - Possible formats:
     - URLs (web pages, articles, YouTube videos, GitHub repos, anything Firecrawl can reach)
     - Files (PDF, DOCX, PPTX, XLSX, TXT, MD, HTML, CSV, images, audio)
     - Browser bookmark, Twitter/X bookmark, Apple Notes / Upnote exports
2. Discuss the categories, based on the information domain area. A special chat is required for that.
3. Tools to be discussed; see if there are better alternatives:
   - Obsidian along with its Web Clipper, graph view, and Dataview
   - Marp as a markdown-based slide deck format (HTML use?)
   - Dolt (https://docs.dolthub.com/) instead of `log.md` file
