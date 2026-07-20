# NOTES — reviewing-tech-claims (transform substrate)

Moved here 2026-07-20 from `workspace/skills/reviewing-tech-claims/`, the retired Claude Desktop
library. This is transform substrate, not a live skill. It enters the requirements-chain to be
re-authored as a native `.claude/skills/` skill.

## Why transform, not archive

It verifies technical claims against official documentation and emits inline ✅ Verified /
⚠️ Unverified markers. No skill in the active `.claude/skills/` set does external-source
fact-checking. `qualifying-outputs` audits internal drift and consistency, which is a different
job, so the two do not overlap and this capability has no successor.

## Dependencies to resolve during transform

- One home for verification. This skill is the "verify claims" step (Phase 3) already described
  in `../2026-06-24-deciding-architecture-capture.md`. Dedupe so the verification workflow and the
  ✅ / ⚠️ marker convention live in one place, not split between that capture and this skill.
- Composition. Paired with `editing-docs` (express) and `architecting-data-platforms` (author),
  both of which also moved here, for version-sensitive claims such as package names, CLI commands,
  API signatures, config syntax, install steps, and UI paths. Keep the three aligned when
  re-authoring.
- References. `references/verification-workflow.md` and `references/workflows/update-comparison-guide.md`
  carry the method. `evals.json` is a ready test set for the ported skill.
