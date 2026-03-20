# TASKS.md — workspace

> Workspace-level task tracker. Scope: cross-repo infrastructure, shared skills library,
> workspace-wide maintenance.
> Managed by Claude (proposed) + approved by you.
> Triggers: `show tasks` | `next task` | `start task TASK-XXX` | `done task TASK-XXX` | `add task`

---

## 🔴 Backlog

- TASK-008: First-run test of project-bootstrapping skill | target: workspace/skills/project-bootstrapping/ | scope: open Chief of Droids project, trigger `bootstrap project`, validate 7-section form renders, Phase 2 challenge fires, Phase 3 writes FRAMING.md → CLAUDE.md → TASKS.md → system prompt in sequence; record gaps for TASK-009
- TASK-009: Refine project-bootstrapping skill post first-run | target: workspace/skills/project-bootstrapping/ | scope: update SKILL.md, project-interview.md, challenge-rules.md, output-templates.md based on TASK-008 findings; bump skill version to 1.2
- TASK-010: Scope and resolve datawan/ repo | target: workspace/datawan/ | scope: empty src/, test/, mock/, public/ — determine if active, abandoned, or pre-scaffold; either add a CLAUDE.md + TASKS.md and start work, or archive
- TASK-011: Frame slide-gen/use-case-3/ | target: workspace/slide-gen/use-case-3/ | scope: orphaned content only (data-architecture-reference.md) — no FRAMING.md, CONSTITUTION.md, or TASKS.md; either frame it with `build framing use-case-3` or remove it

---

## 🟡 In Progress

---

## ✅ Done

- TASK-001: Design project-bootstrapping architecture | target: n/a (session design work) | scope: 3 options evaluated and challenged; constraints documented (artifact write limitation, API call boundary, skill-as-launcher misconception); 3-phase architecture decided: collect in artifact, challenge + generate in conversation, write via MCP | done: 2026-03-19
- TASK-002: Design and validate bootstrap questionnaire | target: workspace/skills/project-bootstrapping/references/project-interview.md | scope: 21-question form across 7 sections; gap analysis against official Claude Code best practices; FRAMING.md template mapped to Section 2 | done: 2026-03-19
- TASK-003: Author project-bootstrapping skill | target: workspace/skills/project-bootstrapping/ | scope: SKILL.md + 3 reference files; HOW-TO-TRIGGER.md updated; assessed against creating-skills checklist — Pass; workspace skills library now at 7 skills | done: 2026-03-19
- TASK-004: Fix managing-tasks TASKS.md target resolution | target: workspace/CLAUDE.md + skills/managing-tasks/SKILL.md + skills/managing-tasks/references/tasks-schema.md | scope: CLAUDE.md declares workspace default TASKS.md path; tasks-schema.md adds 3-step resolution order; SKILL.md v1.6 consolidates target resolution into shared block | done: 2026-03-19
- TASK-005: Initialise workspace/TASKS.md | target: workspace/TASKS.md | scope: file was empty — created with canonical schema, initial backlog, done tasks from session | done: 2026-03-19
- TASK-006: Migrate my-claude-fmk/TASKS.md to canonical schema | target: my-claude-fmk/TASKS.md | scope: legacy checkbox format replaced with canonical entry format; historical tasks preserved in Done | done: 2026-03-19
- TASK-007: Fix analyzing-business-cases FRAMING template location and add FRAMING.md to bootstrap workflow | target: skills/analyzing-business-cases/template/FRAMING-template.md + skills/project-bootstrapping/ | scope: template moved from slide-gen/ to workspace skills library (v1.1); project-interview.md v1.1 adds Section 2 mapped to FRAMING.md sections; output-templates.md v1.2 adds Template 0 (FRAMING.md) and FRAMING.md alignment rule in CLAUDE.md template; SKILL.md v1.1 updates to 4-artefact sequential generation order | done: 2026-03-19
- TASK-007a: Create workspace/docs/ and author bootstrapping-guide.md | target: workspace/docs/ | scope: docs/ directory created; bootstrapping-guide.md v1.0 Draft authored covering what/prerequisites/3-phase flow/step-by-step/question guide/post-bootstrap/troubleshooting/design decisions; README.md added as index | done: 2026-03-19
- TASK-007b: Scan skills library for my-claude-fmk references and fix | target: workspace/skills/project-bootstrapping/references/output-templates.md | scope: full scan of all 7 skills + HOW-TO-TRIGGER.md; one bad path found and fixed — skills path in system prompt template pointed to my-claude-fmk/claude-desktop/skills/ instead of workspace/skills/; corrected in output-templates.md v1.1 | done: 2026-03-19

---

*Last updated: 2026-03-19 — TASK-007 through TASK-007b closed; TASK-008 through TASK-011 in backlog*
