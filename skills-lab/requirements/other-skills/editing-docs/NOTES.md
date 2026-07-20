# NOTES — editing-docs (transform substrate)

Moved here 2026-07-20 from `workspace/skills/editing-docs/`, the retired Claude Desktop
library. This is transform substrate, not a live skill. It enters the requirements-chain
(brainstorming-requirements, then writing-requirements) to be re-authored as a native
`.claude/skills/` skill.

## Why transform, not archive

The document-expression layer (`.md`, `.docx`, `.pptx`, `.xlsx`, HTML, React, SVG, meeting
minutes, workshop summaries, decision records) has no successor in the active `.claude/skills/`
set, which is requirements, design and wiki focused. The capability is worth keeping.

## Dependencies to resolve during transform

- Inert Desktop handoffs. The SKILL.md routes doc-type authoring to `analyzing-business-cases`
  (BDR, use cases, business requirements), which is archived. Re-home those onto its successors
  `framing-project` and `qualifying-outputs`, or drop them. Do not carry dead routing into the
  new skill.
- One home for expression. This skill is the "Express" step (Phase 4) in
  `../2026-06-24-deciding-architecture-capture.md`, which reads "map the substance onto a fixed
  artefact template, render in house style". That capture already names editing-docs as the owner
  of expression (lines 8, 76, 87) and composes it rather than duplicating it. On this axis there is
  no conflict, keep expression as the single composed home.
- The template-ownership boundary to settle. The same capture splits ownership: line 84 gives the
  "artefact template" to the future `deciding-architecture` orchestration skill, line 87 gives
  "expression, house style, Mermaid" to editing-docs. Old editing-docs bundled both, keeping
  per-document-type templates inside its own `references/` and doing the rendering. Re-authoring is
  the moment to draw the line: template structure (which sections, in what order) belongs to the
  orchestrator, editing-docs owns rendering and house style only. Miss this and the ADR template
  ends up defined in two places, the exact duplication the capture set out to avoid.
- C4 generation is a named backlog item for this skill. Phase 7 of that capture depends on a future
  editing-docs enhancement, a `references/c4.md` covering C4 levels and the rendering choice (Mermaid
  C4 syntax versus Structurizr DSL) plus theme mapping. The capture records editing-docs at v4.2 with
  `references/mermaid.md` but no C4 reference yet. Carry this as a follow-up for the ported skill; the
  rendering-tool choice and any Mermaid C4 version constraints are unverified and must be checked
  against current docs when authored, not assumed.
- Expression calibration, including humaniser applicability. The capture (line 54) records a rule
  that a locked design doc stays neutral and impersonal, so the humaniser voice pass does not apply
  to it. That is an editing-docs concern and it interacts with the org `humanizer` skill. Decide where
  the rule lives so it is not stated twice.
- References to carry. The `references/` templates are the real payload: corporate chrome and
  theme injection for `.docx` (theme1.xml + settings-clrSchemeMapping.xml), 60s meeting minutes,
  thematic workshop summary, decision-meeting, markdown-formatting. Preserve them intact through
  the port, subject to the template-ownership split above.

## Composition

Was the shared rendering layer for `architecting-data-platforms` (ADRs) and
`reviewing-tech-claims` (verified claims), both of which also moved here. Keep the three aligned
when re-authoring so the express-and-verify pairing survives.
