# Doc Principles Reference

Read this file before any document expression task.

---

## Writing Principles

1 — Identify audience, type, and scope before writing.

2 — Lead with the conclusion; exception: procedural docs follow task sequence.

3 — One concept per section — split if two, merge if duplicate.

4 — **Match density to document type.**

| Document type | Appropriate density |
| :--- | :--- |
| Requirements Brief | Dense — every sentence carries information |
| ADR | Structured and concise — context / decision / consequences only |
| Runbook | Step-by-step — numbered, no ambiguity, operator-executable |
| Explainer | Progressive — start simple, add complexity only as needed |
| Assessment report | Evidence-first — findings before recommendations |
| Reference doc | Scannable — tables, lists, short paragraphs |

5 — **Calibrate to the reader.**
- Write to the least-expert likely reader unless the audience is confirmed specialist
- Define terms on first use in any document longer than one page
- Never assume the reader has read a related document — link it and state the dependency

6 — **Version and trace every deliverable.**

Every document that will be referenced by another document must have:
- A version identifier (v1.0, date, or commit reference)
- An author and date
- A statement of what upstream inputs it was based on

Documents without version information cannot be used as alignment evidence.

---

## Output Format Selection

Choose format before writing — do not default to Markdown without considering
alternatives.

| Output | When to use |
| :--- | :--- |
| Markdown `.md` | Files to be committed, rendered in GitHub/Obsidian/VS Code, or used as skill/reference content |
| Plain prose | Inline chat responses, emails, short briefs not saved to disk |
| Structured sections (no file) | Assessment outputs delivered in conversation before writing to disk |
| DOCX | Formal deliverables requiring tracked changes, comments, or executive distribution |
| PPTX | Slide-based presentations and visual storytelling |
| XLSX | Tabular data, structured matrices, financial models |
| HTML | Web-rendered output, interactive documents, browser-based delivery |
| React | Component-based interactive UI, dashboards, artifact-rendered output |
| SVG | Diagrams, illustrations, and scalable visual assets |

For DOCX, PPTX, XLSX, HTML, React, and SVG outputs: read `references/theme.md`
and apply the Elevate theme — see step 5 of the workflow.

When the output is `.md`: read `references/markdown-formatting.md` before writing.
Do not apply Markdown-specific rules from memory.

---

## File Naming

Kebab-case. Numeric prefix for ordered sets.

```
00-overview.md
01-setup.md
02-reference.md
assessment-phase-03-2026-03-10.md
```
