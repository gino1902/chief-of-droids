# Architecture Requirements — Body Template

> Body schema for system-and-container-level architecture requirement documents.
> Composes with `template-corporate-chrome.md` at the chrome's `<!-- BODY -->` slot.
> QA: `qa-architecture-requirements.md` is loaded automatically by writing-docs Step 8.

## When to use

Author is producing system + container level architectural requirements. Output is
a `.docx` reviewed by architects, business sponsors, and engineering leads.

## Composition contract

- Inserted into `template-corporate-chrome.md` at `<!-- BODY -->`.
- Top-level heading is "## 4 System & Containers Level Requirements" — chrome reserves 1–3.
- Sub-sections are 4.1–4.4, fixed: Functional / Governance & Access / Observability / NFR.
- Each sub-section is a single requirements table, not bullets.

---

## 4 System & Containers Level Requirements

### 4.1 Functional Requirements

| ID | Requirement | Suggested rephrasing/fix |
| :--- | :--- | :--- |
| {ID} | {requirement statement} | {rephrasing if needed; blank if accepted as-is} |

### 4.2 Governance & Access Requirements

| ID | Requirement | Suggested rephrasing/fix |
| :--- | :--- | :--- |
| {ID} | {requirement statement} | {rephrasing if needed; blank if accepted as-is} |

### 4.3 Observability Requirements

| ID | Requirement | Suggested rephrasing/fix |
| :--- | :--- | :--- |
| {ID} | {requirement statement} | {rephrasing if needed; blank if accepted as-is} |

### 4.4 Non-Functional Requirements

| ID | Requirement | Suggested rephrasing/fix |
| :--- | :--- | :--- |
| {ID} | {requirement statement} | {rephrasing if needed; blank if accepted as-is} |

---

## Authoring rules

- One requirement per row — atomic.
- "Suggested rephrasing/fix" is empty when the requirement passes QA as written.
- "Suggested rephrasing/fix" is filled when QA flags an issue and a corrected wording is proposed in place of removal.
- ID convention is author choice; suggestion: `FR-NN` / `GOV-NN` / `OBS-NN` / `NFR-NN` per sub-section.
- Sub-section count and titles are fixed. Add categories only by amending this template, not per-document.

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.0        |
| Last Updated | 2026-04-28 |
| Status       | Draft      |
