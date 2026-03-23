---
name: analyzing-business-cases
description: >
  Frames use cases, challenges weak business reasoning, and assesses artifact
  consistency across projects. Load this skill whenever a user wants to define,
  scope, or pressure-test a project — including vague or early-stage requests.
  Triggers on: "build framing", "challenge framing", "assess <use-case-id>",
  "frame this project", "scope this use case", "challenge this proposal",
  "does this make business sense", "what are we actually trying to solve",
  "is the framing solid", "new use case". Explicit command aliases:
  "build framing <id>", "challenge framing <id>", "assess <id>".
  Composes with: architecting-data-platforms (when use case is a data platform),
  reviewing-tech-claims (when technical claims appear in FRAMING).
---
<!-- version: 1.6 | author: chief-of-droids workspace | last_updated: 2026-03-23 -->

# Analyzing Business Cases Skill

Strategic guidance for framing use cases, challenging weak business reasoning,
and assessing consistency across project artifacts.

**Principle:** This skill owns narrative coherence, stakeholder alignment, value
articulation, and artifact-to-artifact traceability. Technical claims inside FRAMING
are delegated to architecting-data-platforms and reviewing-tech-claims — not evaluated here.

## Reference files

Read explicitly via filesystem tool when the relevant workflow is triggered. Not loaded automatically.

| File | When to read |
|---|---|
| `template/FRAMING-template.md` | During `build framing` — structural base for all sections |
| `references/challenge-checklist.md` | During `build framing` and `challenge framing` |
| `references/consistency-check.md` | During `assess` |
| `references/workflows/build-framing.md` | Full procedure for `build framing` |
| `references/workflows/challenge-framing.md` | Full procedure for `challenge framing` |
| `references/workflows/assess.md` | Full procedure for `assess` |

## Workflows

### build framing
Trigger: `build framing <use-case-id>` | "frame this project" | "scope this use case" | "what are we actually trying to solve"
Read `references/workflows/build-framing.md` for the full procedure.

### challenge framing
Trigger: `challenge framing <use-case-id>` | "challenge this proposal" | "is the framing solid" | "does this make business sense"
Read `references/workflows/challenge-framing.md` for the full procedure.

### assess
Trigger: `assess <use-case-id>`
Read `references/workflows/assess.md` for the full procedure.

## QA Checklist

- [ ] Reference files read via filesystem tool — not from memory
- [ ] FRAMING problem statement is specific and root-cause-anchored
- [ ] Value articulation is measurable and stakeholder-linked
- [ ] Scope boundary is explicit
- [ ] Assumptions surfaced — not buried
- [ ] All artifact transitions pass consistency-check before proceeding
- [ ] No rewrite of FRAMING.md without explicit user instruction
- [ ] No file written without user approval
- [ ] Technical claims in FRAMING delegated to architecting-data-platforms / reviewing-tech-claims

## Composes With

| Skill | When |
|---|---|
| `architecting-data-platforms` | When use case is a data platform design or architecture |
| `reviewing-tech-claims` | When technical claims appear in FRAMING or CONSTITUTION |

| Field        | Value      |
|--------------|------------|
| Version      | 1.6        |
| Last Updated | 2026-03-23 |
| Status       | Final      |
