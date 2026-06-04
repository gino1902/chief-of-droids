<!-- version: 2.0 | author: chief-of-droids workspace | last_updated: 2026-06-03 -->

# Editing Docs QA Checklist

Run as the gate before proposing any output (workflow Step 9). The five
expression-quality criteria below are also the QA report shown to the reader
after the artifact is delivered (workflow Step 10), each marked pass or flag
with a one-line note.

## Expression quality

The five criteria the expression layer is accountable for. Each maps to one of
the skill's concerns. Adapted from the Clemson University Writing Lab revision
guidance (source below), filtered to expression only, with its substance
criteria (evidence quality, argument strength) excluded.

- [ ] **Clarity and coherence** (mapping): ideas land in a logical order, each
  section connects to the next, and no passage is ambiguous.
- [ ] **Audience fit** (tone): the document is pitched for the intended reader
  and is clear for that reader specifically.
- [ ] **Consistency and focus** (formatting, verbosity): style, tone, and
  formatting are consistent throughout, and tangential content is cut so nothing
  distracts from the central message.
- [ ] **Readability and flow** (reading efficiency): sentences and paragraphs
  read smoothly, nothing is awkward or stilted, and the document is scannable at
  the speed its type demands.
- [ ] **Requirements and shape met** (formatting, mapping): format, length, and
  structural requirements are satisfied, the opening states the point, and the
  close lands it.

## Process gates

Mechanical checks that must hold regardless of document type.

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

## Source

Expression criteria adapted from the Clemson University Writing Lab, "Revising
Your Drafts":
https://www.clemson.edu/centers-institutes/writing/writing-resources/writing-resources/revising.html
