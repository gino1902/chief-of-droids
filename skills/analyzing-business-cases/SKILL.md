---
name: analyzing-business-cases
description: >
  Business analysis and consulting guidance for any project — covers FRAMING
  authorship, strategic challenge, and cross-artifact consistency assessment.
  Explicit trigger only — not auto-run. Use when asked to frame a use case,
  challenge existing framing, or assess artifact consistency across a project.
  Triggers on: "build framing <use-case-id>", "challenge framing <use-case-id>",
  "assess <use-case-id>".
  Composes with: architecting-data-platforms (when use case is a data platform),
  reviewing-tech-claims (when technical claims appear in FRAMING).
---
<!-- version: 1.5 | author: chief-of-droids workspace | last_updated: 2026-03-19 -->

# Analyzing Business Cases Skill

Strategic guidance for framing use cases, challenging weak business reasoning,
and assessing consistency across project artifacts.

**Principle:** This skill owns narrative coherence, stakeholder alignment, value
articulation, and artifact-to-artifact traceability. Technical claims inside FRAMING
are delegated to architecting-data-platforms and reviewing-tech-claims — not evaluated here.

**Reference files** — read explicitly via filesystem tool when the relevant workflow
is triggered. Files are not loaded automatically:
- `template/FRAMING-template.md` — canonical workspace template; read during `build framing`;
  structural base for all FRAMING.md sections
- `references/challenge-checklist.md` — read during `build framing` and `challenge framing`
- `references/consistency-check.md` — read during `assess`

---

## Workflow: build framing

Trigger: `build framing <use-case-id>`

Steps:
1. Use filesystem tool to read `template/FRAMING-template.md` — structural base for all sections
2. Use filesystem tool to read `references/challenge-checklist.md`
3. Parse user prompt — extract: problem statement, stakeholders, expected value,
   constraints, timeline signals
4. Expand into a full FRAMING.md draft using the template sections
5. Run challenge-checklist against the draft before proposing it
6. Surface any checklist gaps as open questions to the user
7. Propose draft — await user approval before writing any file

**Expansion rules:**
- Never invent stakeholders, KPIs, or constraints not present or inferable from the prompt
- Flag assumptions explicitly: `⚠️ Assumed — confirm with user`
- Prefer concrete value statements ("reduce forecast error by X%") over generic ones ("improve forecasting")
- If the prompt is too thin to populate a section, mark it: `🔲 To be defined`

**Failure handling:**
If `template/FRAMING-template.md` is unreadable, halt:
`⚠️ FRAMING-template.md unreadable — cannot scaffold. Resolve before continuing.`
If `references/challenge-checklist.md` is unreadable, proceed but flag:
`⚠️ challenge-checklist.md unreadable — checklist validation skipped; review manually before approving draft.`

Output: `use-case-<id>/FRAMING.md` written to filesystem (on approval only)

---

## Workflow: challenge framing

Trigger: `challenge framing <use-case-id>`

Steps:
1. Use filesystem tool to read `use-case-<id>/FRAMING.md`
2. Use filesystem tool to read `references/challenge-checklist.md`
3. Run checklist against every section
4. Output a structured critique — section by section, issue by issue
5. Surface findings only — do not rewrite FRAMING.md unless user requests (see step 6)
6. If user confirms findings and requests a fix: propose edits, await approval, then write

**Failure handling:**
If `use-case-<id>/FRAMING.md` is absent, halt:
`⚠️ FRAMING.md not found for use-case-<id> — nothing to challenge.`
If `references/challenge-checklist.md` is unreadable, proceed but flag:
`⚠️ challenge-checklist.md unreadable — critique run from skill memory only.`

Output: structured critique in chat (no file write unless user requests)

---

## Workflow: assess

Trigger: `assess <use-case-id>`

Steps:
1. Use filesystem tool to read `references/consistency-check.md`
2. Use filesystem tool to list `use-case-<id>/` directory — enumerate artifacts present
3. Read all available artifacts in order:
   `use-case-<id>/FRAMING.md` → `use-case-<id>/CONSTITUTION.md` → any additional
   pipeline artifacts present (e.g. SlideMap.md, DeckReady.md, or project-specific equivalents)
   — note which are absent; skip missing artifacts, do not block
4. For each artifact transition present, run the corresponding check from consistency-check.md
5. Output a gap table: artifact pair | issue | severity | recommendation
6. Do not rewrite any artifact — surface findings only
7. If user requests fixes: delegate to the appropriate workflow for that artifact type

**Failure handling:**
If `references/consistency-check.md` is unreadable, halt:
`⚠️ consistency-check.md unreadable — cannot run assessment. Resolve before continuing.`
Missing artifacts are not failures — skip the transition and note in output.

Output: gap table in chat (no file write)

---

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

---

## Composes With

| Skill | When |
| :--- | :--- |
| `architecting-data-platforms` | When use case is a data platform design or architecture |
| `reviewing-tech-claims` | When technical claims appear in FRAMING or CONSTITUTION |
