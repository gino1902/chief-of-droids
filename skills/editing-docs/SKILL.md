---
name: editing-docs
description: >
  Expression layer for documents. ALWAYS invoke this skill when the user asks to
  format, render, produce, edit, or shape a document in `.md`, `.docx`, `.pptx`,
  `.xlsx`, HTML, React, or SVG, or to "format this", "render as docx", "turn
  this into a document", "generate meeting minutes", "format as minutes", or any
  equivalent. This skill expresses substance authored elsewhere. It maps content
  to a defined structure, formats against best-practice styles and colours, sets
  tone for the audience, tunes verbosity, and optimises reading efficiency. It
  does not author substance. Substance is owned by domain skills
  (architecting-data-platforms for ADRs, analyzing-business-cases for BDRs, use
  cases, acceptance tests, business requirements). Every per-document-type
  expression rule lives in a `references/` template, never in this body.
  Composes with: reviewing-tech-claims, pptx, docx, xlsx,
  architecting-data-platforms, analyzing-business-cases.
---
<!-- version: 4.1 | author: chief-of-droids workspace | last_updated: 2026-06-04 -->

# Editing Docs Skill

## What this skill does

editing-docs is the expression layer. It takes substance authored elsewhere, by
a domain authoring skill or by the user, and expresses it. It never authors
substance.

Expression covers five concerns, handled together rather than as a sequence:
mapping content to a defined structure, formatting against house styles and
colours, tone for the audience, verbosity, and reading efficiency.

## Routing: two axes

Per-type expression rules never live in this body. They live in a `references/`
template, one per document type. Adding a type means adding a template, not
editing this skill.

A request resolves on two independent axes:

- Document type selects a template, if one exists (minutes maps to
  `60s-meeting-minutes.md`). No template means free-form against
  `doc-principles.md`.
- Output format selects the rendering machinery: the markdown rules, the theme
  and colours, the docx chrome, and Mermaid.

## Reference Files

Document-type expression templates:

- `references/60s-meeting-minutes.md`, read when the document is meeting minutes.
  Carries the five concerns for a 60-second minutes read.
- `references/workshop-summary-thematic.md`, read when the document is a workshop
  summary on a thematic spine. Expresses two inputs, a preparation analysis and
  room notes, against the five concerns. Requires both.

Format-mechanism references:

- `references/doc-principles.md`, the general expression defaults, read before
  any rendering task.
- `references/markdown-formatting.md`, read when output is `.md`.
- `references/mermaid.md`, read when output contains Mermaid diagrams.
- `references/theme.md`, read when output is `.docx`, `.pptx`, `.xlsx`, HTML,
  React, or SVG, routes the theme and colours.
- `references/template-corporate-chrome.md`, read for every `.docx`, wraps the
  document with cover, header, footer, TOC, revision history, remaining issues,
  and appendix.
- `references/qa-checklist.md`, the process gates, run as the internal Step 9
  gate before proposing output.

## Workflow: express and render

1. Resolve the request on both axes. Identify the substance source (an authoring
   skill earlier in the conversation, or the user), the document type, and the
   output format.
2. Read `references/doc-principles.md` for the general expression defaults. If
   unreadable, halt: `⚠️ doc-principles.md unreadable, cannot proceed`.
3. Document-type routing. If a template exists for the type, read it (see the
   document-type templates in Reference Files). It governs mapping, tone,
   verbosity, reading efficiency, and any type-specific formatting. If no template
   exists (runbook, playbook), express free-form against doc-principles.
4. Format routing.
   - `.md`: read `markdown-formatting.md`, and `mermaid.md` if the output
     contains diagrams. Run the mermaid QA checklist and fix all failures before
     displaying.
   - `.docx`: read `template-corporate-chrome.md`. Chrome wraps every docx, no
     exceptions.
   - `.pptx`, `.xlsx`, HTML, React, SVG: theme only, no chrome.
5. Placeholder gate (`.docx` only). Derive each chrome placeholder per the rules
   in `template-corporate-chrome.md`, show the full mapping as a table, flag
   every default with `> 🔲 To be defined, awaiting user input`, and wait for
   explicit confirmation. Silent defaults are prohibited.
6. Theme injection. Read `theme.md` and pass the theme artifacts per the format
   routing table. For docx, pass `theme1.xml` and the `clrSchemeMapping`. If
   unreadable, flag and proceed without theme.
7. Tech verification. If the content carries version-sensitive technical claims
   (CLI commands, API signatures, package names, install steps), compose
   `reviewing-tech-claims`. Do not read its files directly.
8. Apply expression: map to structure, format, set tone, tune verbosity,
   optimise reading efficiency. These are concurrent concerns, not an ordered
   pipeline.
9. QA gate. Read and run the process gates in `references/qa-checklist.md` before
   proposing output. This is an internal gate, not surfaced to the reader. If
   unreadable, flag and run manual QA.

## Trigger Examples

- "Render this as a docx"
- "Format this document"
- "Turn these notes into a markdown doc"
- "Generate meeting minutes from these notes"
- "Format this as minutes"
- "Summarise this workshop"
- "Fix the formatting on this file"
- "Create an HTML page for this content"

Triggers that route to an authoring skill first, then here for expression:

- "Write an ADR for X", authored by `architecting-data-platforms`, then
  expressed here.
- "Write a BDR, use case, acceptance test, or business requirement", authored by
  `analyzing-business-cases`, then expressed here.

If both authoring and expression are needed, both skills load via Anthropic's
description-driven multi-skill activation. This skill does not invoke other
skills, Claude orchestrates.

## Composes With

| Skill | When |
| :--- | :--- |
| `architecting-data-platforms` | The request is for an ADR or architecture artefact. That skill authors the substance, this skill expresses it |
| `analyzing-business-cases` | The request is for a BDR, use case, acceptance test, or business requirement. That skill authors, this skill expresses |
| `reviewing-tech-claims` | The content carries version-sensitive technical claims |
| `pptx` | Output format is `.pptx`, pass `theme1.xml` |
| `docx` | Output format is `.docx`, pass `theme1.xml` plus `settings-clrSchemeMapping.xml` |
| `xlsx` | Output format is `.xlsx`, pass `theme1.xml` |
| `html` | Output format is HTML, pass `elevate.css` |
| `react` | Output format is React, pass `elevate-tokens.js` or `elevate-tailwind-v4.css` |

## Changelog

See `CHANGELOG.md`.
