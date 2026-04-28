---
name: writing-docs
description: >
  Produces structured written output for any document type — guides, runbooks,
  ADRs, briefs, reports, explainers, playbooks, and any prose intended to be
  read, saved, or shared. Use when the user asks to write, document, draft,
  create, or produce any structured content — including requests like "write a
  runbook for X", "draft an ADR for Y", "turn these notes into a doc", "create
  a requirements brief", "document this workflow", or any request to produce
  output as .md, .docx, .pptx, .xlsx, HTML, React, or SVG. Also triggers when
  the user asks to fix formatting or structure on an existing document, including
  requests to "format this file", "format this diagram", or "format this document".
  Composes with: reviewing-tech-claims, pptx, docx, xlsx.
---
<!-- version: 2.2 | author: chief-of-droids workspace | last_updated: 2026-04-28 -->

# Writing Docs Skill

Produces clear, well-structured written output for any document type — technical
or non-technical, short or long, saved to disk or shared inline.

**Scope:** This skill governs document structure, information hierarchy, clarity,
and audience calibration. It applies regardless of output format.

---

## Reference Files

- `references/doc-principles.md` — read before any document authoring task;
  contains writing principles, density guidance, output format selection, and
  file naming rules
- `references/markdown-formatting.md` — read when the output is a `.md` file;
  contains table syntax, code blocks, and formatting QA checklist
- `references/mermaid.md` — read when the output contains Mermaid diagrams;
  contains diagram type selection, direction, code structure, subgraph hierarchy,
  node and edge conventions, Elevate theme implementation, rendering pitfalls,
  self-check gate, QA checklist, and test report format
- `references/theme.md` — read when the output format is docx, pptx, xlsx,
  HTML, React, or SVG; contains Elevate theme routing rules and color role table
- `references/templates.md` — read when producing an ADR, Requirements Brief,
  Runbook, or Playbook; copy the relevant template and fill all `{placeholder}` fields
- `references/template-corporate-chrome.md` — read when producing a `.docx` requiring
  cover page, revision history, and remaining-issues sections; composes with a body template
- `references/template-architecture-requirements.md` — read when producing system- or
  container-level architecture requirements; composes with corporate-chrome
- `references/qa-architecture-requirements.md` — auto-loaded by Step 8 when the
  architecture-requirements body template is active
- `references/qa-checklist.md` — read and run before proposing any output

---

## Workflow: author document

Steps (run for any document authoring trigger):
1. Identify document type, audience, and output format
2. Use filesystem tool to read `references/doc-principles.md`
   — if unreadable, halt: `⚠️ doc-principles.md unreadable — cannot proceed`
3. If document type is ADR, Requirements Brief, Runbook, Playbook, or Architecture Requirements:
   use filesystem tool to read `references/templates.md` (the index)
   — if unreadable, flag: `⚠️ templates.md unreadable — proceeding without template`
   For Architecture Requirements, additionally read both:
     - `references/template-corporate-chrome.md`
     - `references/template-architecture-requirements.md`
   For ADR / Requirements Brief / Runbook / Playbook, copy the relevant inline template from templates.md.
4. If output format is `.md`:
   use filesystem tool to read `references/markdown-formatting.md`
   — if unreadable, flag: `⚠️ markdown-formatting.md unreadable — applying defaults`
   If output contains Mermaid diagrams:
   additionally use filesystem tool to read `references/mermaid.md`
   — if unreadable, flag: `⚠️ mermaid.md unreadable — applying defaults; QA report will be emitted using built-in checklist`
   After drafting any Mermaid diagram:
   a. Run every item in the mermaid.md QA Checklist against the draft — this is a blocking self-check gate
   b. Fix all failures before displaying
   c. Emit the Mermaid QA Report (format defined in mermaid.md) in chat before displaying the diagram
   The report is mandatory — never display a Mermaid diagram without it
5. If output format is docx / pptx / xlsx / HTML / React / SVG:
   use filesystem tool to read `references/theme.md`; pass the specified theme
   artifact to the composed format skill — do not apply theme colors directly.
   If no composed format skill is active (e.g. writing HTML inline), apply the
   token values from `references/theme.md` directly in the output.
   — if unreadable, flag: `⚠️ theme.md unreadable — proceeding without theme`
6. If output contains version-sensitive technical claims:
   load the `reviewing-tech-claims` skill and apply its verification rules before writing
   — do not read `reviewing-tech-claims/SKILL.md` directly; invoke it as a composed skill
7. Author content — apply density, hierarchy, and versioning rules from doc-principles.md
8. Use filesystem tool to read `references/qa-checklist.md` and run it before proposing output
   — if unreadable, flag: `⚠️ qa-checklist.md unreadable — run manual QA before proposing`
   If body template `template-architecture-requirements.md` is in use:
     additionally read `references/qa-architecture-requirements.md` and run its per-row criteria
   — if unreadable, flag: `⚠️ qa-architecture-requirements.md unreadable — body QA skipped`

---

## Trigger Examples

- "Write a requirements brief for use-case-1"
- "Document this workflow"
- "Draft an ADR for the storage account design"
- "Create a runbook for the forecasting pipeline"
- "Turn these notes into a reference doc"
- "Fix the formatting on this document"
- "Format this file"
- "Format this diagram"
- "Create an HTML page for this content"

---

## Composes With

| Skill | When |
| :--- | :--- |
| `reviewing-tech-claims` | When output contains version-sensitive technical claims — load as composed skill, not direct file reference |
| `pptx` | When output format is `.pptx` — pass `theme1.xml` per `references/theme.md` |
| `docx` | When output format is `.docx` — pass `theme1.xml` per `references/theme.md` |
| `xlsx` | When output format is `.xlsx` — pass `theme1.xml` per `references/theme.md` |
| `html` | When output format is HTML — pass `elevate.css` per `references/theme.md` |
| `react` | When output format is React — pass `elevate-tokens.js` or `elevate-tailwind-v4.css` per `references/theme.md` |
