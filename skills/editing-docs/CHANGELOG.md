# Editing Docs Changelog

History moved out of `SKILL.md` to keep the skill body lean. The body carries
instruction only; this file carries history.

- v4.2 (2026-06-04) — wired the decision-meeting expression template, which had
  been committed as a file but referenced nowhere. Listed it in Reference Files,
  added a meeting-type disambiguation rule to workflow Step 3 (decision-meeting
  for meetings run to decide with prepared inputs, workshop-summary-thematic for
  exploratory, 60s-meeting-minutes for general outcomes), added trigger phrases
  to the SKILL description and Trigger Examples, and registered it in
  HOW-TO-TRIGGER.md (ownerless-template list and quick-reference table). Fixed
  the stale back-reference in workshop-summary-thematic.md (v1.3), which still
  routed decision meetings to the minutes template instead of decision-meeting.
  Swept the residual writing-docs naming in template-corporate-chrome.md (v1.9)
  and the authoring wording in doc-principles.md left over from the v3.3 rename,
  and added html and react to the SKILL frontmatter composes line.
- v4.1 (2026-06-04) — wired the workshop-summary (thematic spine) expression
  template. Added triggers and the Combining-skills row in HOW-TO-TRIGGER.md
  (1.16), listed the template in Reference Files, and generalised the two
  single-example phrasings (SKILL Step 3, qa-checklist gate, now 3.1) from the
  minutes-only example to the template list, so adding the next type touches one
  list, not three call sites. The template requires two inputs, a preparation
  analysis and room notes; if only raw notes exist, minutes is the correct route.
- v4.0 (2026-06-04) — cut craft-teaching weight and the surfaced generic-QA
  loop. Removed workflow Step 10 (QA report shown to the reader): a self-graded
  generic-writing rubric on every deliverable was noise for the reader and
  contradicted concern 5, reading efficiency. De-proceduralised Step 8: the five
  concerns are concurrent, not an ordered pipeline. Step 9 now runs the process
  gates only. The five expression-quality criteria (generic writing craft,
  native to a capable model, adapted from a university writing lab) were dropped
  from `references/qa-checklist.md` (v3.0), along with the orphaned source
  citation. Compressed the anchoring-principle and five-concerns prose into a
  short block. Moved this migration history out of the SKILL.md body into this
  file. Routing core, house artefacts, placeholder governance gate, and theme
  injection are unchanged — those are the non-derivable contract and were kept.
- v3.4 (2026-06-03) — revamped `references/qa-checklist.md` (v2.0) around five
  expression-quality criteria (clarity and coherence, audience fit, consistency
  and focus, readability and flow, requirements and shape met), adapted from the
  Clemson University Writing Lab revision guidance and filtered to expression
  only. Added workflow Step 10: display the QA report to the reader after the
  artifact is delivered, not just run it as an internal gate. Removed the orphan
  `evals.json` (no runner consumed it) and both deprecated substance references
  (`template-architecture-requirements.md`, `qa-architecture-requirements.md`),
  whose substance is owned by architecting-data-platforms. The deprecated block
  is now empty and has been dropped.
- v3.3 (2026-06-03) — renamed from `writing-docs` to `editing-docs`. The folder,
  the frontmatter name, the title, and the principle statement all move to the
  new name. Cross-references across the framework (HOW-TO-TRIGGER.md,
  creating-skills, CLAUDE.md, and other skills' Composes With sections) still
  point to the old name and must be swept before routing is consistent.
- v3.2 (2026-06-03) — reanchored as the expression layer, with five named
  concerns: mapping, formatting, tone, verbosity, reading efficiency. Per-type
  expression rules now live in `references/` templates, the first being
  `60s-meeting-minutes.md`. This is distinct from the v3.0 removal of substance
  templates: v3.0 removed templates owned by authoring skills (ADR, BDR); v3.2
  introduces expression templates, which carry no substance, only how a type is
  expressed. Added meeting-minutes triggers.
- v3.1 (2026-04-29) — added Step 4 placeholder confirmation gate for `.docx`
  outputs; theme.md updated so H2/H3 are bold (consequence: heading hierarchy
  is size-driven across all levels); template-corporate-chrome.md v1.8
  reformats Running Header as a table mirroring the footer's style.
- v3.0 (2026-04-29) — repositioned from "produces structured written output" to
  "formats and renders documents". Removed inline templates branch (ADR / Brief /
  Runbook / Playbook). Authoring skills now own document-type substance via
  description-driven activation. `templates.md` deleted from references.
  `template-architecture-requirements.md` and `qa-architecture-requirements.md`
  marked deprecated; will migrate to authoring skills.
- v2.2 (2026-04-28) — chrome + arch-req body templates added.
- v2.1 — pptx/docx/xlsx/HTML/React/SVG theme routing.
