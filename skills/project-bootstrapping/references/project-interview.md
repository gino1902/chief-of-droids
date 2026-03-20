<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-03-19 -->

# Project Interview — Question Set & Validation Rules

Used by the `project-bootstrapping` skill to render the interview form artifact
and validate answers before the challenge step.

The framing section (Section 2) is derived from the canonical FRAMING.md template
at `skills/analyzing-business-cases/template/FRAMING-template.md`. Questions map
one-to-one to FRAMING.md sections — answers are used to generate FRAMING.md directly.

---

## Contents

- Question Set
- Field Validation Rules
- Scope Note
- Answer-to-Output Mapping

---

## Question Set

### Section 1 — Identity

| ID | Label | Input type | Required |
| :--- | :--- | :--- | :--- |
| S1Q1 | Repo name (lowercase, hyphens — e.g. `my-project`) | Short text | Yes |
| S1Q2 | Project name (human-readable) | Short text | Yes |

---

### Section 2 — Project Framing

*Answers in this section populate FRAMING.md directly. Write as prose — not bullet points.*

| ID | FRAMING.md section | Label & guidance | Input type | Required |
| :--- | :--- | :--- | :--- | :--- |
| S2Q3 | Context | Describe the stable state — business environment, key processes, value streams. Write as if everything is functioning. No problem statement here. | Textarea | Yes |
| S2Q4 | Problem | What is broken, missing, or suboptimal within the context above, and why it matters. Only what would not be true if things were working correctly. | Textarea | Yes |
| S2Q5 | Client | Who is this for? Primary audience (decision-maker or end user) and secondary stakeholders. Technical, business, or mixed? | Textarea | Yes |
| S2Q6 | Objectives | Business value outcomes expected. State as measurable or observable results, not activities. One outcome per line. | Textarea | Yes |
| S2Q7 | Solution | What you intend to build or implement to address the problem. One paragraph maximum. Approach only — no implementation detail, no feature list. | Textarea | Yes |
| S2Q8 | Constraints | Limits and boundaries the solution must respect: technical, data, timeline, budget, hard exclusions. | Textarea | No |

---

### Section 3 — Domain & Stack

| ID | Label | Input type | Required |
| :--- | :--- | :--- | :--- |
| S3Q9 | Domain (e.g. data engineering, business analysis, content, software, finance…) | Short text | Yes |
| S3Q10 | Tech stack — tools, platforms, languages (or "none" if non-technical) | Textarea | No |

---

### Section 4 — Deliverables

| ID | Label | Input type | Required |
| :--- | :--- | :--- | :--- |
| S4Q11 | Primary output type (e.g. `.md` docs, `.pptx`, code, reports, diagrams…) | Short text | Yes |
| S4Q12 | Output quality bar — what makes an output acceptable vs. rejected? | Textarea | No |
| S4Q13 | Output format defaults (e.g. always `.md`, always include version block, always English…) | Textarea | No |
| S4Q14 | Minimum-necessary rule — what must Claude know every session to avoid mistakes? | Textarea | Yes |

---

### Section 5 — Routing & Repos

| ID | Label | Input type | Required |
| :--- | :--- | :--- | :--- |
| S5Q15 | Other repos this project needs to reach (repo name + condition), or "none" | Textarea | No |
| S5Q16 | Workspace skills needed (tick all that apply): managing-tasks / writing-docs / architecting-data-platforms / reviewing-tech-claims / creating-skills / analyzing-business-cases / project-bootstrapping / all / none | Textarea | Yes |

---

### Section 6 — Behaviour

| ID | Label | Input type | Required |
| :--- | :--- | :--- | :--- |
| S6Q17 | Hard rules — what must Claude never do without explicit confirmation? | Textarea | No |
| S6Q18 | Tone & verbosity (e.g. direct/technical, formal/casual, verbose/concise) | Short text | Yes |
| S6Q19 | Gotchas — known failure modes or things Claude typically gets wrong in this domain | Textarea | No |
| S6Q20 | Workflows — named multi-step workflows (trigger + steps), or "none yet" | Textarea | No |

---

### Section 7 — Initial Tasks

| ID | Label | Input type | Required |
| :--- | :--- | :--- | :--- |
| S7Q21 | First 3–5 tasks for TASKS.md Backlog (rough descriptions, one per line) | Textarea | Yes |

---

## Field Validation Rules

Applied in Step 3 of the skill workflow — not inside the artifact.

| Field | Rule | Failure message |
| :--- | :--- | :--- |
| S1Q1 repo name | Lowercase letters, hyphens, digits only. No spaces, no uppercase, no special chars. | `⚠️ Repo name must be lowercase with hyphens only (e.g. my-project)` |
| S2Q3 context | Must be non-empty. Flag if <20 words — likely too thin to produce a useful FRAMING.md. | `⚠️ Context is very short — describe the as-is landscape in at least 2–3 sentences` |
| S2Q4 problem | Must be non-empty. Flag if it restates the context without naming a delta. | `⚠️ Problem must describe what is broken or missing, not restate the context` |
| S2Q6 objectives | Must contain at least one measurable outcome. Flag if answer contains only activities ("implement X", "build Y"). | `⚠️ Objectives must be outcomes (what will be true), not activities (what will be done)` |
| S4Q14 minimum-necessary | Must be non-empty. If answer is >300 chars, flag potential CLAUDE.md bloat. | `⚠️ Minimum-necessary rule is long — consider what can move to a skill or conversation` |
| S7Q21 initial tasks | Must contain at least 1 task. Each line treated as one task. | `⚠️ At least one initial task is required` |

---

## Scope Note

This file defines the question set only. The artifact layout is generated by
Claude from this spec — Claude determines layout, styling, and input types.
The challenge logic lives in `challenge-rules.md`, not here.

---

## Answer-to-Output Mapping

| Answer field | Output file | Section |
| :--- | :--- | :--- |
| S1Q1 | FRAMING.md, CLAUDE.md, TASKS.md, system prompt | repo name / routing |
| S1Q2 | FRAMING.md title, CLAUDE.md title, TASKS.md title | headers |
| S2Q3–S2Q8 | FRAMING.md | Context / Problem / Client / Objectives / Solution / Constraints |
| S3Q9 | CLAUDE.md, system prompt | domain / context block |
| S3Q10 | system prompt | stack / context block |
| S4Q11–S4Q14 | CLAUDE.md | format, quality bar, tone, minimum-necessary |
| S5Q15 | system prompt | routing override block |
| S5Q16 | system prompt, CLAUDE.md | skills block |
| S6Q17–S6Q20 | system prompt, CLAUDE.md | rules, tone, gotchas, workflows |
| S7Q21 | TASKS.md | backlog entries |
