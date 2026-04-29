---
name: writing-docs
description: >
  Document formatting and rendering. ALWAYS invoke this skill when the user asks
  to format, render, or produce a document in `.md`, `.docx`, `.pptx`, `.xlsx`,
  HTML, React, or SVG; or when the user asks to "fix formatting", "format this",
  "render as docx", "turn this into a document", or any equivalent. Do not write
  documents directly without invoking this skill — it owns format routing, theme
  application, chrome wrapping, markdown formatting, and Mermaid QA. Content
  authoring is owned by other skills (architecting-data-platforms for ADRs,
  analyzing-business-cases for BDRs / use cases / acceptance tests / business
  requirements). Composes with: reviewing-tech-claims, pptx, docx, xlsx,
  architecting-data-platforms, analyzing-business-cases.
---
<!-- version: 3.0 | author: chief-of-droids workspace | last_updated: 2026-04-29 -->

# Writing Docs Skill

Formats and renders documents. **Does not author content for specific document
types** (ADR, BDR, requirements, use cases, runbooks, etc.) — those are owned
by domain authoring skills. This skill applies format routing, theme injection,
chrome wrapping (for `.docx`), markdown formatting, Mermaid QA, and the final
QA gate.

**Scope:** Format only. Content authoring delegates to other skills via
description-driven multi-skill activation (Anthropic Agent Skills standard).

---

## Reference Files

- `references/doc-principles.md` — read before any rendering task; writing
  principles, density, file naming
- `references/markdown-formatting.md` — read when output is `.md`
- `references/mermaid.md` — read when output contains Mermaid diagrams
- `references/theme.md` — read when output is `.docx`, `.pptx`, `.xlsx`, HTML,
  React, or SVG; routes to the appropriate Elevate theme artifact(s)
- `references/template-corporate-chrome.md` — read for **every** `.docx`
  output; wraps the doc with cover, header, footer, TOC, revision history,
  remaining issues, and appendix
- `references/qa-checklist.md` — read and run before proposing any output

**Deprecated references** (still on disk, no longer auto-loaded):

- `references/template-architecture-requirements.md` — body schema; will move
  to its owning authoring skill
- `references/qa-architecture-requirements.md` — QA for the above; same fate

---

## Workflow: format and render

Steps run for any rendering trigger:

1. **Identify** output format and confirm content provenance.
   - Output formats: `.md`, `.docx`, `.pptx`, `.xlsx`, HTML, React, SVG.
   - Content provenance: either authored by the user, or produced by a
     composing authoring skill (architecting-data-platforms,
     analyzing-business-cases, etc.) earlier in the conversation.

2. **Read principles.** Use filesystem tool to read `references/doc-principles.md`.
   — if unreadable, halt: `⚠️ doc-principles.md unreadable — cannot proceed`

3. **Format-driven routing.**

   **IF output format is `.docx`:**
   - Use filesystem tool to read `references/template-corporate-chrome.md`
   - Chrome wraps every `.docx` output (cover, header, footer, TOC, revision
     history, remaining issues, body slot, appendix). No exceptions.
   - Body content is free-form by default. If a body template exists for the
     doc type and the user explicitly references it, read it. Otherwise the
     body is the user-supplied or authoring-skill-supplied content.
   - if chrome unreadable, halt: `⚠️ template-corporate-chrome.md unreadable — cannot proceed`

   **IF output format is `.md`:**
   - Use filesystem tool to read `references/markdown-formatting.md`
   - if unreadable, flag: `⚠️ markdown-formatting.md unreadable — applying defaults`
   - If output contains Mermaid diagrams: additionally read `references/mermaid.md`
     - if unreadable, flag: `⚠️ mermaid.md unreadable — applying defaults`
     - After drafting any Mermaid diagram, run the mermaid.md QA Checklist;
       fix all failures before displaying; emit Mermaid QA Report inline.

   **IF output format is `.pptx`, `.xlsx`, HTML, React, or SVG:**
   - Theme handling per Step 4 only; no chrome.

4. **Theme injection.** Use filesystem tool to read `references/theme.md`.

   **IF output format is `.docx`:**
   - Pass two artifacts to the composed `docx` skill:
     - `shared/elevate-theme/theme1.xml` → inject into `word/theme/theme1.xml`
     - `shared/elevate-theme/settings-clrSchemeMapping.xml` → inject the
       `<w:clrSchemeMapping>` element as a child of `<w:settings>` in
       `word/settings.xml`
   - Both required. Skipping the mapping causes Word's built-in styles to
     fall back to OOXML defaults and render wrong colours.

   **IF output format is `.pptx` or `.xlsx`:**
   - Pass `shared/elevate-theme/theme1.xml` to the composed format skill.

   **IF output format is HTML, React, or SVG:**
   - Apply the theme artifact per `theme.md` format routing table.
   - For artifacts with interactive form elements: additionally read
     `shared/elevate-theme/elevate-artifact.md` and apply the `applyAll()`
     pattern.

   — if theme.md unreadable, flag: `⚠️ theme.md unreadable — proceeding without theme`

5. **Tech verification.** If the content contains version-sensitive technical
   claims (CLI commands, API signatures, package names, install steps),
   verify against official documentation. Load `reviewing-tech-claims` as a
   composed skill — do not read its files directly.

6. **Apply formatting** rules from doc-principles.md (density, hierarchy,
   versioning) to the content received from the authoring skill or user.

7. **QA gate.** Use filesystem tool to read `references/qa-checklist.md` and
   run it before proposing output.
   — if unreadable, flag: `⚠️ qa-checklist.md unreadable — run manual QA`

---

## Trigger Examples

- "Render this as a docx"
- "Format this document"
- "Turn these notes into a markdown doc"
- "Fix the formatting on this file"
- "Format this diagram"
- "Create an HTML page for this content"
- "Produce a Word doc from the strategy paper"

**Triggers that should NOT route here directly** (route to authoring skills first):

- "Write an ADR for X" → triggers `architecting-data-platforms` (ADR authoring),
  then this skill for rendering
- "Write a BDR / use case / acceptance test / business requirement" → triggers
  `analyzing-business-cases` first, then this skill for rendering

If both authoring and formatting are needed, both skills load via Anthropic's
description-driven multi-skill activation. This skill does not invoke other
skills — Claude orchestrates.

---

## Composes With

| Skill | When |
| :--- | :--- |
| `architecting-data-platforms` | When the request is for an ADR or architecture artefact — that skill produces content; this skill formats |
| `analyzing-business-cases` | When the request is for a BDR, use case, acceptance test, or business requirement — that skill produces content; this skill formats |
| `reviewing-tech-claims` | When output contains version-sensitive technical claims |
| `pptx` | When output format is `.pptx` — pass `theme1.xml` |
| `docx` | When output format is `.docx` — pass `theme1.xml` + `settings-clrSchemeMapping.xml` |
| `xlsx` | When output format is `.xlsx` — pass `theme1.xml` |
| `html` | When output format is HTML — pass `elevate.css` |
| `react` | When output format is React — pass `elevate-tokens.js` or `elevate-tailwind-v4.css` |

---

## Migration Notes

- v3.0 (2026-04-29) — repositioned from "produces structured written output" to
  "formats and renders documents". Removed inline templates branch (ADR / Brief /
  Runbook / Playbook). Authoring skills now own document-type templates via
  description-driven activation. `templates.md` deleted from references.
  `template-architecture-requirements.md` and `qa-architecture-requirements.md`
  marked deprecated; will migrate to authoring skills.
- v2.2 (2026-04-28) — chrome + arch-req body templates added.
- v2.1 — pptx/docx/xlsx/HTML/React/SVG theme routing.
