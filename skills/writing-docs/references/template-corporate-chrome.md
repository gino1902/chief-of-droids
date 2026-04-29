# Corporate Document Chrome

> Wraps **every `.docx` output** produced via writing-docs. Provides cover page,
> running header/footer, TOC, revision history, remaining issues, and appendix.
> Body content is free-form by default — supplied either by the user or by the
> output of a composing authoring skill (architecting-data-platforms,
> analyzing-business-cases). A specific body template may be inserted at the
> marked slot if explicitly requested.

## When to use

Mandatory for every `.docx` rendered by writing-docs. No exceptions. Short docs
render with the same chrome as long docs — Revision History gets one row,
Remaining Issues stays empty when there are none. Reproducibility and reader
consistency are the priorities.

## How to compose

1. Copy this chrome verbatim.
2. Insert body content at the `<!-- BODY -->` marker. Body is free-form unless
   the user explicitly references a body template (e.g.
   `template-architecture-requirements.md`).
3. Fill all `{placeholder}` fields per the **Placeholder derivation rules** below.
4. Omit lines that map to optional placeholders when the source provides no value.
5. Render via writing-docs → composed `docx` skill, which receives both
   `theme1.xml` and `settings-clrSchemeMapping.xml` per `theme.md` routing.

## Cover Page

> Simple cover on white. Background `lt1` (white). Title text in `accent1`
> (electric blue). Metadata in `dk1` (black). No full-bleed; no banner; no logo
> tile. Logo top-left as a small mark.
>
> **No header. No footer. No page number.** Header and footer chrome begin on
> page 2 (first post-cover page — typically Table of Contents).

```cover
[LOGO]

{company_name}                           ← accent1, large
{document_title}                         ← accent1, large

Reference:       {reference}             ← dk1, OPTIONAL — omit the entire line if no value
Classification:  {classification} – {classification_label}
Version:         {version_status} – {version_date}
```

## Running Header (page 2 onward)

> Suppressed on page 1 (cover). No red.

| Position | Content |
| :------- | :------ |
| Left     | Logo placeholder `[LOGO]` (small mark) |
| Right    | Title placeholder `{document_title}` in `dk2` (near-black navy) |

## Running Footer (page 2 onward)

> Three-column layout. Renderer must use tab stops (left / centre / right) — not
> a table. Word table cells have minimum height and render as empty boxes.
>
> Suppressed on page 1 (cover).

| Position | Content |
| :------- | :------ |
| Left     | `© {company_name} {year}` |
| Centre   | `{version_status} – {date} – {classification} - {classification_label}` |
| Right    | `{page_number}` |

> Example: `© Company Name 2026` … `DRAFT – 29/04/2026 – C2 - Restricted` … `3`

## Renderer notes — first-page suppression

> Implementation guidance for the composed `docx` skill (or any other renderer).
> The chrome contract is declarative: cover has no chrome; page 2 onward has
> chrome. Renderers pick the technique.

Word offers three patterns; the first is canonical:

| Pattern | Mechanism | When to use |
| :------ | :-------- | :---------- |
| Different first page | `titlePg` flag on `<w:sectPr>` + empty `headers.first` / `footers.first` | Default — single section, simplest |
| Section break after cover | Two sections; section 1 has no header/footer, section 2 has them | Cover needs different page setup (orientation, margins, paper size) |
| Empty first-page chrome | Header/footer present but contain only an empty paragraph | Avoid — leaves a header/footer slot reserved on page 1 |

**Page numbering convention:** cover counts as page 1; first body page (TOC)
displays `2`. This matches Word's default behaviour with `titlePg`. If a
"renumber from body" convention is required (cover unnumbered or `i`; TOC = `1`),
that is a separate section restart and not part of this chrome.

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

## Placeholder derivation rules

> When mapping a source markdown document into this chrome, derive placeholder
> values per the rules below. Do not invent values that the source does not
> provide — for optional placeholders without a source value, omit the line.

| Placeholder | Required | Derivation |
| :--- | :--- | :--- |
| `{company_name}` | yes | Author / organisation. Not derivable from source. |
| `{document_title}` | yes | Source H1 with any trailing status suffix removed (e.g. ` - DRAFT`, ` - v1.0`, ` - FINAL`). Example: `# SQLI in 2028 - DRAFT` → `SQLI in 2028`. |
| `{reference}` | **no** | Author-provided. **Omit the cover line entirely** if no value. Never invent. |
| `{classification}` / `{classification_label}` | yes | Organisational policy (e.g. `C2` / `Restricted`). |
| `{version_status}` | yes | Source H1 status suffix if present (`DRAFT`, `v1.0`, `FINAL`); else author-supplied. |
| `{version_date}` | yes | Author / filename date prefix (e.g. `20260428_*` → `28/04/2026`). |
| `{date}` | yes | Footer date — usually equals `{version_date}`. |
| `{year}` | yes | Year component of `{date}`. |
| `{page_number}` | yes | Word `PAGE` field — auto-updated by Word per page. Renderer inserts the field, not a literal value. |
| `{body_section_title}` | yes | Provided by the body template (or, for free-form body, derived from the source H1). |
| `{appendix_content}` | yes | Free-form. Empty if the document has no appendix. |

## Placeholder reference

| Placeholder | Source | Example |
| :--- | :--- | :--- |
| `{company_name}` | author | `Company Name` |
| `{document_title}` | derived from source H1 (strip status suffix) | `Data Platform Creation` |
| `{reference}` | author (optional) | `Architecture Requirements` — omit cover line if not provided |
| `{classification}` | author | `C2` |
| `{classification_label}` | author | `Restricted` |
| `{version_status}` | source H1 suffix or author | `DRAFT` / `v1.0` / `FINAL` |
| `{version_date}` | author / filename | `22/04/2026` |
| `{date}` | author (footer; usually = version_date) | `28/04/2026` |
| `{year}` | derived from date | `2026` |
| `{page_number}` | Word `PAGE` field | `3` |
| `{body_section_title}` | body template | `System & Containers Level Requirements` |
| `{appendix_content}` | author | free-form |

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.8        |
| Last Updated | 2026-04-29 |
| Status       | Draft      |
