# Theme Reference — Elevate

Read this file when the output format is one of: docx, pptx, xlsx, HTML, React, SVG.
Do not load for `.md` outputs — Mermaid theme is handled in `markdown-formatting.md`.

Canonical theme source: `shared/elevate-theme/`
Authoritative spec for colors, roles, typography, and contrast: `shared/elevate-theme/tokens.json`
Human-readable reference: `shared/elevate-theme/README.md`

---

## Principle

Do not apply theme colors directly. Pass the appropriate theme file or token set
to the composed format skill. The format skill owns rendering; this skill owns
the decision to apply the theme and which artifact to pass.

When the output is an HTML or React artifact containing interactive form elements
(inputs, textareas, buttons, pill groups): read `shared/elevate-theme/elevate-artifact.md`
in addition to this file. The artifact form pattern is mandatory — CSS custom properties
on interactive elements are overridden by the host dark-mode stylesheet and must not be used.

---

## Two-layer model

Elevate has a palette layer (OOXML-compatible names) and a role layer (logical
author-facing aliases). Both live in `tokens.json`. See
`shared/elevate-theme/README.md` § "Two-layer model" for the full explanation.

| Layer | Names | Where to use |
| :---- | :---- | :---------- |
| Palette | `dk1`, `lt1`, `dk2`, `lt2`, `accent1`–`accent6` | `theme1.xml`, raw OOXML, fallbacks |
| Roles | `tx1`, `tx2`, `tx3`, `bg1`, `bg2` | Templates, generators, CSS aliases, JSX |

Authors and templates reference role names. Generators map roles → palette
when emitting OOXML or hex.

---

## Format routing

| Output format | Theme artifact(s) to pass | How to pass |
| :------------ | :------------------------ | :---------- |
| `.pptx` | `shared/elevate-theme/theme1.xml` | Instruct the pptx skill to inject into `ppt/theme/theme1.xml` |
| `.docx` | `shared/elevate-theme/theme1.xml` **+** `shared/elevate-theme/settings-clrSchemeMapping.xml` | Inject theme1.xml into `word/theme/theme1.xml`. Inject the `<w:clrSchemeMapping>` element into `word/settings.xml` as a child of `<w:settings>`, **after `<w:compat>`** — CT_Settings sequence requires clrSchemeMapping late in the element order; first-child placement fails schema validation. Both required. |
| `.xlsx` | `shared/elevate-theme/theme1.xml` | Instruct the xlsx skill to inject into `xl/theme/theme1.xml` |
| HTML / CSS (no form elements) | `shared/elevate-theme/elevate.css` | Link or import; use `var(--elevate-*)` semantic aliases |
| HTML / React (with form elements) | `shared/elevate-theme/elevate-artifact.md` | Read and apply `applyAll()` pattern — CSS vars prohibited on inputs |
| React (inline styles, no forms) | `shared/elevate-theme/elevate-tokens.js` | Import `elevateTokens`; use semantic token keys |
| React + Tailwind v3 | `shared/elevate-theme/elevate-tokens.js` | Import `tailwindElevate`; extend `theme.colors` in `tailwind.config.js` |
| React + Tailwind v4 | `shared/elevate-theme/elevate-tailwind-v4.css` | Import after `@import "tailwindcss"` |
| SVG | `shared/elevate-theme/elevate.css` | Embed `:root` block or reference CSS file; use `var(--elevate-*)` |

`.docx` is the only format requiring two artifacts. Skipping
`settings-clrSchemeMapping.xml` causes Word's built-in heading styles and
theme-aware tables to fall back to OOXML defaults (`background1` = `light1`,
`text1` = `dark1`) — wrong colours. Both must be injected on every render.

---

## Color role rules

Always apply colors according to their declared role. Never reassign a token to
a different semantic purpose. Reference `tokens.json` for canonical hex.

### Palette

| Token | Role | Correct use |
| :---- | :--- | :---------- |
| `dk1` (`#000000`) | True black — structural ink | Gridlines, strokes, rules; **not body text** |
| `lt1` (`#FFFFFF`) | Pure white — secondary background | High-contrast cards, table data rows |
| `dk2` (`#0F0E2B`) | Near-black navy | Aliased as `tx1` for primary text on light |
| `lt2` (`#FFFAF0`) | Warm cream | Aliased as `bg1` for primary background |
| `accent1` (`#1F24E9`) | Electric blue — primary brand fill | CTAs, active states; aliased as `tx3` for emphasis text |
| `accent2` (`#6DA5FF`) | Sky blue — secondary fill | Hover, table headers; aliased as `tx2` for text on dark |
| `accent3` (`#C5D8F6`) | Ice blue (light) | Tints, code-block fills, banded table rows |
| `accent4` (`#425F8B`) | Steel blue (muted) | Dividers, blockquote text, edges |
| `accent5` (`#6164EB`) | Violet-blue | Alternate accent — badges, tags |
| `accent6` (`#8E8FEC`) | Periwinkle (soft) | Soft accent — tooltips, light badges |

### Role aliases

| Role | Alias of | Hex | Use |
| :--- | :------- | :-- | :-- |
| `tx1` | `dk2` | `#0F0E2B` | Primary text — body, headings, table cells |
| `tx2` | `accent2` | `#6DA5FF` | Secondary text — dark-fill contexts only |
| `tx3` | `accent1` | `#1F24E9` | Tertiary text — restricted; titles, hyperlinks, CTAs, callouts |
| `bg1` | `lt2` | `#FFFAF0` | Primary background |
| `bg2` | `lt1` | `#FFFFFF` | Secondary background |

---

## Typography

Authoritative source: `tokens.json` `typography` block. Summary below.

### Headings

| Level | Color | Size | Weight |
| :---- | :---- | ---: | :----- |
| Title | `tx1` | 22 pt | bold |
| H1 | `tx1` | 16 pt | bold |
| H2 | `tx1` | 13 pt | bold |
| H3 | `tx1` | 11 pt | bold |

All headings use `tx1` and are bold. Hierarchy is size-driven. Brand color
in headings is forbidden — readers misread it as a hyperlink.

### Body, Blockquote, Code

| Element | Color | Fill | Style | Size |
| :------ | :---- | :--- | :---- | ---: |
| Paragraph / list | `tx1` | — | regular | 11 pt |
| Blockquote | `accent4` | — | italic, indented, no border | 11 pt |
| Code block | `tx1` | `accent3` | monospace | 10 pt |
| Inline code | `tx1` | `accent3` | monospace | 11 pt |

---

## Table styling

Default table style for `.docx` and HTML tables.

| Element | Color/Fill |
| :------ | :--------- |
| Header fill | `accent2` |
| Header text | `tx1` |
| Data row fill | `bg2` |
| Banded row fill | `accent3` |
| Cell text | `tx1` |
| Borders | none |

---

## Contrast pairing rules

WCAG 2.2 SC 1.4.3 AA: 4.5:1 for normal text. Authoritative source:
`tokens.json` `contrast_pairs` block.

Text-on-fill quick reference:

| Fill | Allowed text | Forbidden text |
| :--- | :----------- | :------------- |
| `bg1`, `bg2` | `tx1`, `tx3`, `accent4`, `accent5` | `tx2` |
| `dk1`, `dk2` | `tx2`, `bg1`, `bg2` | `tx1`, `tx3` |
| `accent1` | `bg1`, `bg2` | all `tx*` |
| `accent2` | `tx1` only | everything else |
| `accent3` | `tx1`, `tx3` | `tx2` |
| `accent4` | `bg1`, `bg2` | all `tx*` |

`tx2` is only legible on dark fills.
`tx3` is restricted to specific elements (see element constraints below).

---

## Element role constraints

`tx3` (brand color) cannot be used as generic emphasis. Allowed elements:

- cover_title
- hyperlink (always with underline)
- cta_button_text (always with button shape)
- callout_label (always with non-color cue: indent + italic)

Forbidden in: body_paragraph, h1–h3, table_cell, list_item.

WCAG 2.2 SC 1.4.1 + G183: brand-color text must pair with a non-color visual cue.

---

## Font

Theme primary: **TWK Everett Light** (headings / majorFont), **TWK Everett Regular** (body / minorFont).
Monospace: Cascadia Code, Consolas, Courier New (cascading fallback).
Licensed commercial font — must be installed on the target machine.
Declared in all theme artifacts; not embedded.

**Cascade chain (HTML / CSS / SVG / React only):**

```
TWK Everett Light, Helvetica Neue, system-ui, -apple-system, Arial, sans-serif
```

Helvetica Neue sits in second position because it is the closest visual match
to TWK Everett available pre-installed on macOS — same Swiss-grotesk family,
comparable proportions and weight range. macOS users without TWK Everett
installed render in Helvetica Neue automatically. Windows machines fall through
to Arial.

**Office formats (.docx / .pptx / .xlsx) do NOT honour this chain.** When TWK
Everett is absent, Word, PowerPoint, and Excel substitute silently using their
own logic (typically Calibri or Arial), regardless of what cascade is declared.
The chain only governs HTML / CSS / SVG / React renderings. For consistent
Office rendering across machines without TWK Everett, install the font on every
target machine, or change `theme1.xml` to declare a freely available primary.

---

## Full theme documentation

See `shared/elevate-theme/README.md` for injection instructions, format-specific
usage examples, and the complete two-layer model explanation.

| Field        | Value      |
| :----------- | :--------- |
| Version      | 2.2        |
| Last Updated | 2026-04-29 |
| Status       | Draft      |
