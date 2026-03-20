---
name: writing-docs
description: >
  Produces structured written output for any document type — guides, runbooks,
  ADRs, briefs, reports, explainers, playbooks, and any prose intended to be
  read, saved, or shared. Use when producing any structured document regardless
  of format or length. Composes with: reviewing-tech-claims.
---
<!-- version: 1.6 | author: chief-of-droids workspace | last_updated: 2026-03-19 -->

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
  contains table syntax, code blocks, Mermaid, and formatting QA checklist
- `references/templates.md` — read when producing an ADR, Requirements Brief,
  Runbook, or Playbook; copy the relevant template and fill all `{placeholder}` fields
- `references/qa-checklist.md` — read and run before proposing any output

---

## Workflow: author document

Steps (run for any document authoring trigger):
1. Identify document type, audience, and output format
2. Use filesystem tool to read `references/doc-principles.md`
   — if unreadable, halt: `⚠️ doc-principles.md unreadable — cannot proceed`
3. If document type is ADR, Requirements Brief, Runbook, or Playbook:
   use filesystem tool to read `references/templates.md` and copy the relevant template
   — if unreadable, flag: `⚠️ templates.md unreadable — proceeding without template`
4. If output format is `.md`:
   use filesystem tool to read `references/markdown-formatting.md`
   — if unreadable, flag: `⚠️ markdown-formatting.md unreadable — applying defaults`
5. If output contains version-sensitive technical claims:
   load the `reviewing-tech-claims` skill and apply its verification rules before writing
   — do not read `reviewing-tech-claims/SKILL.md` directly; invoke it as a composed skill
6. Author content — apply density, hierarchy, and versioning rules from doc-principles.md
7. Use filesystem tool to read `references/qa-checklist.md` and run it before proposing output
   — if unreadable, flag: `⚠️ qa-checklist.md unreadable — run manual QA before proposing`

---

## Trigger Examples

- "Write a requirements brief for use-case-1"
- "Document this workflow"
- "Draft an ADR for the storage account design"
- "Create a runbook for the forecasting pipeline"
- "Turn these notes into a reference doc"

---

## Composes With

| Skill | When |
| :--- | :--- |
| `reviewing-tech-claims` | When output contains version-sensitive technical claims — load as composed skill, not direct file reference |
