<!-- version: 1.2 | author: chief-of-droids workspace | last_updated: 2026-04-02 -->

# Workflow: build framing

Trigger: `build framing <project-name>` | "frame this project" | "scope this use case"
| "what are we actually trying to solve" | "help me frame this"

## Steps

1. Use filesystem tool to read `template/FRAMING-template.md`
2. Use filesystem tool to read `references/qa-checklist.md`
3. Parse user prompt: extract problem statement, stakeholders, expected value, constraints, timeline signals
4. Expand into a full FRAMING.md draft using the template sections
5. Run qa-checklist against the draft before proposing it
6. Surface any checklist gaps as open questions to the user
7. Propose draft — await user approval before writing any file

## Expansion rules

- Never invent stakeholders, KPIs, or constraints not present or inferable from the prompt
- Flag assumptions explicitly: `⚠️ Assumed — confirm with user`
- Prefer concrete value statements ("reduce forecast error by X%") over generic ones
- If the prompt is too thin to populate a section, mark it: `🔲 To be defined`

## Failure handling

- `template/FRAMING-template.md` unreadable: halt — `⚠️ FRAMING-template.md unreadable — cannot scaffold. Resolve before continuing.`
- `references/qa-checklist.md` unreadable: proceed but flag — `⚠️ qa-checklist.md unreadable — checklist validation skipped; review manually before approving draft.`

## Output

`[REPO_NAME]/FRAMING.md` written to filesystem (on approval only)

| Field        | Value      |
|--------------|------------|
| Version      | 1.2        |
| Last Updated | 2026-04-02 |
| Status       | Final      |
