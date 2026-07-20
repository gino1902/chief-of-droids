# NOTES — architecting-data-platforms (transform substrate)

Moved here 2026-07-20 from `workspace/skills/architecting-data-platforms/`, the retired Claude
Desktop library. This is transform substrate, not a live skill. It enters the requirements-chain
to be re-authored as a native `.claude/skills/` skill or reference pack.

## Why transform, not archive

The generic decision and design shell is already covered by `making-architecture-decision` and
`writing-technical-design`. What has no successor is the domain knowledge: Databricks and Azure
patterns, medallion and lakehouse design, DLT versus Workflows, governance, and cost modelling.
That domain content is the reason to keep this, and the part to preserve.

## Dependencies to resolve during transform

- Split shell from domain. Do not re-implement the Desktop phase-gate flow. Extract the durable
  domain content into a skill or a reference pack that `making-architecture-decision` and
  `writing-technical-design` compose with, rather than duplicating their decision and design work.
- Composition. Paired with `reviewing-tech-claims` (verify version-sensitive claims) and
  `editing-docs` (express ADRs and design docs), both of which also moved here. The
  `../2026-06-24-deciding-architecture-capture.md` capture already models this exact three-way
  pairing (verify at Phase 3, express at Phase 4). Align with it rather than re-deriving it.
- References. `references/gate-activation.md` and the domain templates travel with the skill.
  Keep the domain material, drop the Desktop gate mechanics.
