# Theme Reference — Elevate

Read this file when the output format is one of: docx, pptx, xlsx, HTML, React, SVG.
Do not load for `.md` outputs — Mermaid theme is handled in `markdown-formatting.md`.

Canonical theme source: `shared/elevate-theme/`

---

## Principle

Do not apply theme colors directly. Pass the appropriate theme file or token set
to the composed format skill. The format skill owns rendering; this skill owns
the decision to apply the theme and which artifact to pass.

---

## Format routing

| Output format | Theme artifact to pass | How to pass |
| :------------ | :--------------------- | :---------- |
| `.pptx` | `shared/elevate-theme/theme1.xml` | Instruct the pptx skill to inject into `ppt/theme/theme1.xml` |
| `.docx` | `shared/elevate-theme/theme1.xml` | Instruct the docx skill to inject into `word/theme/theme1.xml` |
| `.xlsx` | `shared/elevate-theme/theme1.xml` | Instruct the xlsx skill to inject into `xl/theme/theme1.xml` |
| HTML / CSS | `shared/elevate-theme/elevate.css` | Link or import; use `var(--elevate-*)` semantic aliases |
| React (inline styles) | `shared/elevate-theme/elevate-tokens.js` | Import `elevateTokens`; use semantic token keys |
| React + Tailwind v3 | `shared/elevate-theme/elevate-tokens.js` | Import `tailwindElevate`; extend `theme.colors` in `tailwind.config.js` |
| React + Tailwind v4 | `shared/elevate-theme/elevate-tailwind-v4.css` | Import after `@import "tailwindcss"` |
| SVG | `shared/elevate-theme/elevate.css` | Embed `:root` block or reference CSS file; use `var(--elevate-*)` |

---

## Color role rules

Always apply colors according to their declared role. Never reassign a token to
a different semantic purpose.

| Token | Role | Correct use |
| :---- | :--- | :---------- |
| `dk1` / `--elevate-color-text` | Primary dark / text | Body text, labels, primary content |
| `lt1` / `--elevate-color-background` | Primary light / background | Page, slide, canvas background |
| `dk2` / `--elevate-color-surface-dark` | Near-black navy | Dark surfaces, section headers, borders |
| `lt2` / `--elevate-color-surface` | Warm cream | Cards, panels, secondary backgrounds |
| `accent1` / `--elevate-color-brand` | Electric blue — primary brand | CTAs, active states, primary highlights |
| `accent2` / `--elevate-color-brand-light` | Sky blue | Secondary elements, hover states |
| `accent3` / `--elevate-color-brand-lightest` | Ice blue (light) | Tints, background washes, tertiary fills |
| `accent4` / `--elevate-color-brand-muted` | Steel blue (muted) | Dividers, muted labels, edges, connectors |
| `accent5` / `--elevate-color-brand-alt` | Violet-blue | Alternate accent — badges, tags |
| `accent6` / `--elevate-color-brand-soft` | Periwinkle (soft) | Soft accent — tooltips, light badges |
| `hyperlink` / `--elevate-color-link` | Hyperlink | Interactive links |
| `followedHyperlink` / `--elevate-color-link-visited` | Followed link | Visited links |

---

## Font

Theme font: **TWK Everett Light** (headings / majorFont), **TWK Everett Regular** (body / minorFont).
Licensed commercial font — must be installed on the target machine.
Declared in all theme artifacts; not embedded. Office and browsers substitute silently if absent.

---

## Full theme documentation

See `shared/elevate-theme/README.md` for injection instructions, format-specific
usage examples, and the complete color role reference.
