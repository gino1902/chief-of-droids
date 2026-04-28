# Corporate Document Chrome

> Composable wrapper for any corporate `.docx` deliverable. Provides cover page,
> running header/footer, TOC, revision history, remaining issues, and appendix.
> Body content is supplied by a body template (e.g. `template-architecture-requirements.md`)
> inserted at the marked slot.

## When to use

Wraps any structured corporate document where reviewers expect a versioned cover,
revision history, and outstanding-issue tracking. Pairs with one body template.

## How to compose

1. Copy this chrome verbatim.
2. Choose a body template; insert its content at the `<!-- BODY -->` marker.
3. Fill all `{placeholder}` fields.
4. Render via writing-docs → composed `docx` skill (passes `theme1.xml`).

## Cover Page

> Simple cover on white. Background `lt1` (white). Title text in `accent1`
> (electric blue). Metadata in `dk1` (black). No full-bleed; no banner; no logo
> tile. Logo top-left as a small mark.

```cover
[LOGO]

{company_name}                           ← accent1, large
{document_title}                         ← accent1, large

Reference:       {reference}             ← dk1
Classification:  {classification} – {classification_label}
Version:         {version_status} – {version_date}
```

## Running Header (every body page)

> Left: `[LOGO]` (small mark). Right: `{document_title}` in `dk2` (near-black navy). No red.

## Running Footer (every body page)

> `© {company_name} {year} | {version_status} – {date} – {classification} - {classification_label} | {page_number}`

---

## 1 Table of Contents

> Title and page break only. Populate the TOC body in Word after rendering.

---

## 2 Revision History

| Vers | Date | Modifications | Author | Validation Date | Approver |
| :--- | :--- | :--- | :--- | :--- | :--- |
| {vers} | {date} | {modifications} | {author} | {validation_date} | {approver} |

> Manually indicate each version of the document and its validation as part of project use.

---

## 3 Remaining Issues

| Label | Version | Date | Comment |
| :--- | :--- | :--- | :--- |
| {label} | {version} | {date} | {comment} |

---

<!-- BODY -->

> Insert body template content here. Body template's first heading is "## 4 {body_section_title}".
> Body template owns sub-sections 4.1, 4.2, etc.

---

## 5 Appendix

{appendix_content}

---

## Placeholder reference

| Placeholder | Source | Example |
| :--- | :--- | :--- |
| `{company_name}` | author | `Company Name` |
| `{document_title}` | author | `Data Platform Creation` |
| `{reference}` | author | `Architecture Requirements` |
| `{classification}` | author | `C2` |
| `{classification_label}` | author | `Restricted` |
| `{version_status}` | author | `DRAFT` / `v1.0` / `FINAL` |
| `{version_date}` | author | `22/04/2026` |
| `{date}` | author (footer; usually = version_date) | `28/04/2026` |
| `{year}` | author (footer; usually derived from date) | `2026` |
| `{body_section_title}` | body template | `System & Containers Level Requirements` |
| `{appendix_content}` | author | free-form |

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.2        |
| Last Updated | 2026-04-28 |
| Status       | Draft      |
