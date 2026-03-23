<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-03-23 -->

# Workflow: build framing

Trigger: `build framing <use-case-id>` | "frame this project" | "scope this use case"
| "what are we actually trying to solve" | "help me frame this"

## Steps

1. Use filesystem tool to read `template/FRAMING-template.md`
2. Use filesystem tool to read `references/challenge-checklist.md`
3. Parse user prompt: extract problem statement, stakeholders, expected value, constraints, timeline signals
4. Expand into a full FRAMING.md draft using the template sections
5. Run challenge-checklist against the draft before proposing it
6. Surface any checklist gaps as open questions to the user
7. Propose draft — await user approval before writing any file

## Expansion rules

- Never invent stakeholders, KPIs, or constraints not present or inferable from the prompt
- Flag assumptions explicitly: `⚠️ Assumed — confirm with user`
- Prefer concrete value statements ("reduce forecast error by X%") over generic ones
- If the prompt is too thin to populate a section, mark it: `🔲 To be defined`

## Failure handling

- `template/FRAMING-template.md` unreadable: halt — `⚠️ FRAMING-template.md unreadable — cannot scaffold. Resolve before continuing.`
- `references/challenge-checklist.md` unreadable: proceed but flag — `⚠️ challenge-checklist.md unreadable — checklist validation skipped; review manually before approving draft.`

## Output

`use-case-<id>/FRAMING.md` written to filesystem (on approval only)

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-03-23 |
| Status       | Final      |
