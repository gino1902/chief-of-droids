# Elevate — Artifact Form Theme

Canonical source: `shared/elevate-theme/tokens.json`
Derived from: `shared/elevate-theme/elevate-tokens.js`

Read this file when building any HTML or React artifact that contains a form —
inputs, textareas, buttons, pill groups, or any interactive control rendered
inline in claude.ai.

---

## Why this file exists

CSS custom properties (`var(--fc-*)`) set on a parent element are overridden by
the host dark-mode stylesheet when applied to `<input>`, `<textarea>`, or
`<button>` elements. The host applies `background-color` and `color` directly on
these elements, which has higher specificity than any rule using a variable
fallback. The result: input backgrounds go dark regardless of the intended palette.

The fix is mandatory and non-negotiable: all color-bearing properties on every
interactive element must be set via inline styles (`element.style.*`), applied
through a single `applyAll()` function. This makes the form mode-immune — it
renders identically in claude.ai light mode, dark mode, and any future host theme.

---

## Mandatory implementation pattern

### 1 — Token block

Declare all token values as a plain JS object at the top of the script. Copy hex
values from `elevate-tokens.js` — do not hardcode from memory.

```javascript
const DEFAULTS = {
  cardBg:          '#FFFAF0',  // lt2
  cardBorder:      '#425F8B',  // accent4
  text:            '#0F0E2B',  // dk2
  label:           '#425F8B',  // accent4
  inputBg:         '#FFFAF0',  // lt2
  inputBorder:     '#425F8B',  // accent4
  inputText:       '#0F0E2B',  // dk2
  pillIdleBg:      '#C5D8F6',  // accent3
  pillIdleText:    '#0F0E2B',  // dk2
  pillActiveBg:    '#1F24E9',  // accent1
  pillActiveText:  '#FFFAF0',  // lt2
  btnBg:           '#1F24E9',  // accent1
  btnText:         '#FFFAF0',  // lt2
};

const T = Object.assign({}, DEFAULTS);
```

Extend with additional keys for any role not listed above. Always annotate with
the Elevate token name as a comment.

---

### 2 — applyAll() function

A single function applies all token values to all interactive elements via
`element.style.*`. Call it once on load and again on every token change.

```javascript
function applyAll() {
  card.style.backgroundColor = T.cardBg;
  card.style.border           = '1.5px solid ' + T.cardBorder;

  labels.forEach(l => {
    l.style.color = T.label;
  });

  inputs.forEach(el => {
    el.style.backgroundColor = T.inputBg;
    el.style.color            = T.inputText;
    el.style.border           = '1px solid ' + T.inputBorder;
  });

  pills.forEach(p => {
    if (p.classList.contains('active')) {
      p.style.backgroundColor = T.pillActiveBg;
      p.style.color            = T.pillActiveText;
    } else {
      p.style.backgroundColor = T.pillIdleBg;
      p.style.color            = T.pillIdleText;
    }
  });

  submitBtn.style.backgroundColor = T.btnBg;
  submitBtn.style.color            = T.btnText;
}

applyAll();
```

**Rule:** never set `background-color`, `color`, or `border` on inputs, textareas,
or buttons via a CSS rule or CSS custom property. Always use `element.style.*`
through `applyAll()`. CSS rules on these elements will be overridden by the host
stylesheet in dark mode — `element.style.*` cannot be overridden by any external
stylesheet.

---

### 3 — Form shell

Wrap the form card in a dark navy shell. The shell uses a hardcoded `#0F0E2B`
background — this is the `dk2` token and must not be substituted. It creates a
mode-immune frame that visually anchors the form regardless of host theme.

```html
<div style="background:#0F0E2B;border-radius:12px;padding:4px;">
  <div id="form-card" style="border-radius:9px;padding:28px 28px 24px;">
    <!-- form content -->
  </div>
</div>
```

The `form-card` element is the target for `applyAll()`. Its `backgroundColor`
and `border` are set by `applyAll()` — do not set them in markup.

---

### 4 — Inline style baseline for inputs

Every `<input>` and `<textarea>` must carry an inline style baseline in markup.
This ensures correct rendering before the script executes (during streaming).

```html
<textarea
  style="width:100%;box-sizing:border-box;padding:10px 12px;font-size:13px;
         line-height:1.6;border-radius:6px;resize:vertical;min-height:72px;
         font-family:inherit;outline:none;
         background-color:#FFFAF0;color:#0F0E2B;border:1px solid #425F8B;">
</textarea>

<input type="text"
  style="width:100%;padding:9px 12px;font-size:13px;border-radius:6px;
         box-sizing:border-box;outline:none;font-family:inherit;
         background-color:#FFFAF0;color:#0F0E2B;border:1px solid #425F8B;" />
```

The hardcoded hex values in the baseline are the Elevate defaults (`lt2`, `dk2`,
`accent4`). `applyAll()` will overwrite them at runtime — the baseline values are
the streaming-safe fallback only.

---

## Token-to-role reference

Use this table when assigning tokens to roles. Never reassign a token to a
purpose outside its declared role.

| Role | Default token | Hex | Notes |
| :--- | :------------ | :-- | :---- |
| Card background | `lt2` | `#FFFAF0` | Warm cream — panels, cards |
| Card border | `accent4` | `#425F8B` | Steel blue muted — structural borders |
| Body text | `dk2` | `#0F0E2B` | Near-black navy — primary text |
| Label / hint text | `accent4` | `#425F8B` | Muted — secondary labels |
| Input background | `lt2` | `#FFFAF0` | Same as card bg by default |
| Input border | `accent4` | `#425F8B` | Same as card border by default |
| Input text | `dk2` | `#0F0E2B` | Same as body text |
| Pill idle background | `accent3` | `#C5D8F6` | Ice blue — inactive state |
| Pill idle text | `dk2` | `#0F0E2B` | Dark on light fill |
| Pill active background | `accent1` | `#1F24E9` | Electric blue — active/selected |
| Pill active text | `lt2` | `#FFFAF0` | Light on dark fill |
| Button background | `accent1` | `#1F24E9` | Primary CTA |
| Button text | `lt2` | `#FFFAF0` | Light on dark fill |
| Focus ring | `accent1` | `#1F24E9` | Active border on focus |
| Form shell | `dk2` | `#0F0E2B` | Hardcoded — never substituted |

---

## Picker panel (optional)

When the artifact is a design demo or configuration tool, a token picker panel
may be included alongside the form. The picker panel uses host CSS variables
(`var(--color-*)`) — it is a tooling overlay and may adapt to host light/dark
mode. It does not need to be mode-immune.

The picker exposes each role as a row of palette swatches. On swatch click,
update `T[role.key]` and call `applyAll()`.

```javascript
sw.addEventListener('click', () => {
  T[role.key] = p.hex;
  applyAll();
});
```

---

## Prohibited patterns

| Pattern | Why prohibited |
| :--- | :--- |
| `var(--fc-*)` on `<input>` or `<textarea>` background or color | Overridden by host dark-mode stylesheet — invisible in dark mode |
| CSS rule setting `background-color` on `input`, `textarea`, `button` | Same override risk |
| Hardcoding hex values not from `elevate-tokens.js` | Token drift — use the canonical source |
| Setting `form-shell` background to anything other than `#0F0E2B` (`dk2`) | Breaks mode-immune framing |
| Omitting the inline style baseline on inputs/textareas | Inputs render with host default styling during streaming |
| Calling `applyAll()` only on picker change and not on load | Form renders with UA defaults before first interaction |

---

## Scope

This pattern applies to all HTML and React artifacts containing interactive form
elements — regardless of which skill authors the artifact. It does not apply to:

- `.md` output — governed by `elevate-mermaid.md` for diagrams
- `.pptx`, `.docx`, `.xlsx` — governed by `theme1.xml` injection
- Static HTML pages with no interactive form elements — use `elevate.css`

---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.0        |
| Last Updated | 2026-04-07 |
| Status       | Draft      |
