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
<!-- version: 3.3 | author: chief-of-droids workspace | last_updated: 2026-06-03 -->

# Editing Docs Skill

## Anchoring principle

editing-docs is the expression layer. The substance of a document, its facts,
decisions, and arguments, is authored elsewhere, by a domain authoring skill or
by the user. This skill takes that substance and expresses it. It never invents
or authors substance.

Expression is five concerns, and nothing else:

1. Mapping, fitting the content to a defined structure.
2. Formatting, against best practice, styles, and colours.
3. Tone, set for the intended audience.
4. Verbosity, tuned to the need.
5. Reading efficiency, optimised for how fast the reader must absorb it.

## Where the expression rules live

The five concerns are never specified per document type in this body. They live
in a template in `references/`, one template per document type. The minutes type
lives in `references/60s-meeting-minutes.md`. Adding a document type means adding
a template, not editing this skill. This keeps the body lean and the per-type
rules in one place.

Two reference axes are kept separate.

- Document-type templates carry mapping, tone, verbosity, reading efficiency,
  and any type-specific formatting, for one document type.
- Format-mechanism references carry the rendering machinery for one output
  format, the markdown rules, the theme and colours, the docx chrome, and
  Mermaid.

A request resolves on both axes. The document type selects a template, if one
exists. The output format selects the rendering machinery.

## Reference Files

Document-type expression templates:

- `references/60s-meeting-minutes.md`, read when the document is meeting minutes.
  Carries the five concerns for a 60-second minutes read.

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
- `references/qa-checklist.md`, read and run before proposing any output.

Deprecated, these are substance rather than expression and will move to the
owning authoring skill:

- `references/template-architecture-requirements.md`
- `references/qa-architecture-requirements.md`

## Workflow: express and render

1. Resolve the request on both axes. Identify the substance source (an authoring
   skill earlier in the conversation, or the user), the document type, and the
   output format.
2. Read `references/doc-principles.md` for the general expression defaults. If
   unreadable, halt: `⚠️ doc-principles.md unreadable, cannot proceed`.
3. Document-type routing. If a template exists for the type (minutes maps to
   `60s-meeting-minutes.md`), read it. It governs mapping, tone, verbosity,
   reading efficiency, and any type-specific formatting. If no template exists
   (runbook, playbook), express free-form against doc-principles.
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
8. Apply expression in order, per the template and the principles: map to
   structure, format, set tone, tune verbosity, optimise reading efficiency.
9. QA gate. Read and run `references/qa-checklist.md` before proposing output. If
   unreadable, flag and run manual QA.

## Trigger Examples

- "Render this as a docx"
- "Format this document"
- "Turn these notes into a markdown doc"
- "Generate meeting minutes from these notes"
- "Format this as minutes"
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

## Migration Notes

- v3.3 (2026-06-03) — renamed from `writing-docs` to `editing-docs`. The folder,
  the frontmatter name, the title, and the principle statement all move to the
  new name. Cross-references across the framework (HOW-TO-TRIGGER.md,
  creating-skills, CLAUDE.md, and other skills' Composes With sections) still
  point to the old name and must be swept before routing is consistent.
- v3.2 (2026-06-03) — reanchored as the expression layer, with five named
  concerns: mapping, formatting, tone, verbosity, reading efficiency. Per-type
  expression rules now live in `references/` templates, the first being
  `60s-meeting-minutes.md`. This is distinct from the v3.0 removal of substance
  templates: v3.0 removed templates owned by authoring skills (ADR, BDR); v3.2
  introduces expression templates, which carry no substance, only how a type is
  expressed. Added meeting-minutes triggers.
- v3.1 (2026-04-29) — added Step 4 placeholder confirmation gate for `.docx`
  outputs; theme.md updated so H2/H3 are bold (consequence: heading hierarchy
  is size-driven across all levels); template-corporate-chrome.md v1.8
  reformats Running Header as a table mirroring the footer's style.
- v3.0 (2026-04-29) — repositioned from "produces structured written output" to
  "formats and renders documents". Removed inline templates branch (ADR / Brief /
  Runbook / Playbook). Authoring skills now own document-type substance via
  description-driven activation. `templates.md` deleted from references.
  `template-architecture-requirements.md` and `qa-architecture-requirements.md`
  marked deprecated; will migrate to authoring skills.
- v2.2 (2026-04-28) — chrome + arch-req body templates added.
- v2.1 — pptx/docx/xlsx/HTML/React/SVG theme routing.
