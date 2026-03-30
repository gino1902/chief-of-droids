<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-03-30 -->

# Skill Sources

Reference catalog used by the `enrich skill` and `recommend skills` workflows.

**Consumed by:**
- `enrich skill` workflow (E2–E3) — pattern extraction: identifies authoring patterns
  present in catalog sources that are absent from the skill under review
- `references/workflows/recommend-skills.md` (Step 1 and Step 5) — coverage matching:
  checks whether a gap identified in session findings already has a source catalog entry,
  and states the coverage delta vs. the gap

**Role:** Completeness instrument — surfaces patterns present in comparable skills
that may be absent from the skill under review, and matches session-identified gaps
against known sources. Not a correctness standard; use `assessment-checklist.md`
for conformance assessment.

**Updated by:** manual addition after a verified source qualifies (see Qualification below)

---

## Qualification Rules

A source is added to this catalog only when:
1. It has been fetched and verified to be reachable (not a 404 or auth wall)
2. It contains a skill pattern, workflow template, or domain coverage relevant
   to the chief-of-droids workspace context
3. It has been assessed against the creating-skills SKILL.md principles
   (specificity, no standard-knowledge duplication, token-cost justified)

Sources that fail fetch or do not provide skill-authoring value are excluded.

---

## Catalog

| Name | Address | Catalog | Guide | Score (/5) | Notes |
|:-----|:--------|:--------|:------|:-----------|:------|
| Anthropic Skills Best Practices | https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices | ✅ | ✅ | 5 | Primary source — official Anthropic authoring guide; covers frontmatter, description, structure, instructions, composition |
| Anthropic Skills GitHub Repo | https://github.com/anthropics/skills/ | ✅ | ✅ | 5 | Primary source — reference skill implementations; use for structural pattern matching |
| AgentSkills Specification | https://agentskills.io/specification | ✅ | ✅ | 4 | Specification-level detail on skill discovery and trigger patterns; useful for description and trigger design |
| Workspace: managing-sessions | /home/gino/workspace/skills/managing-sessions/ | ✅ | ✅ | 5 | Internal pattern — workflow-class skill with multi-pass confidence model, findings file output, tool-failure handling; use as template for similar workflow-class skills |
| Workspace: managing-tasks | /home/gino/workspace/skills/managing-tasks/ | ✅ | ✅ | 5 | Internal pattern — CRUD workflow with schema + QA checklist composition; use as template for stateful write skills |
| Workspace: creating-skills | /home/gino/workspace/skills/creating-skills/ | ✅ | ✅ | 5 | Internal pattern — environment detection, official source fetch, assessment integration; use as template for skills that compose with external verification |

---

## Column Definitions

| Column | Meaning |
|:-------|:--------|
| Name | Human-readable source label |
| Address | Full URL or absolute filesystem path |
| Catalog | ✅ Source contains a catalog of patterns or skills; ❌ does not |
| Guide | ✅ Source contains authoring guidance or workflow templates; ❌ does not |
| Score (/5) | Usefulness for skill authoring in this workspace — 5 = primary; 1 = marginal |
| Notes | Domain focus and recommended use case |

---

## Adding a New Source

To add a source:
1. Fetch the URL — confirm it returns content (not 404, not auth wall)
2. Confirm it contains skill-authoring patterns or domain content not already covered
3. Add a row following the existing format
4. Update `last_updated` in the header comment
5. Do not add sources that duplicate existing higher-scored entries
