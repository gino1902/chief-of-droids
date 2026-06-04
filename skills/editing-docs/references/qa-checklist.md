<!-- version: 3.0 | author: chief-of-droids workspace | last_updated: 2026-06-04 -->

# Editing Docs QA Checklist

Run the process gates below before proposing any output (workflow Step 9).
Mechanical checks that must hold regardless of document type. This is an internal
gate. Do not surface it to the reader.

Expression quality (clarity, audience fit, focus, readability, shape) is native
to the model and is no longer checked here. The gate enforces only the
non-derivable house contract.

## Process gates

- [ ] `references/doc-principles.md` read before expressing.
- [ ] Substance came from an authoring skill or the user, not invented here.
- [ ] If a document-type template exists, it was read and applied (minutes maps
  to `references/60s-meeting-minutes.md`).
- [ ] Output format selected deliberately, not defaulted.
- [ ] If `.md`: `references/markdown-formatting.md` read and applied.
- [ ] If output is `.docx`, `.pptx`, `.xlsx`, HTML, React, or SVG:
  `references/theme.md` read and the Elevate theme artifact passed to the
  composed format skill.
- [ ] If `.docx`: placeholder derivation table displayed and confirmed (or
  corrected) before rendering.
- [ ] If HTML or React with form elements (inputs, textareas, buttons, pill
  groups): `shared/elevate-theme/elevate-artifact.md` read and the `applyAll()`
  inline-style pattern applied. CSS custom properties on interactive elements
  are prohibited.
- [ ] If version-sensitive technical claims are present: `reviewing-tech-claims`
  loaded and applied.
- [ ] Version block present on any document that will be referenced.
