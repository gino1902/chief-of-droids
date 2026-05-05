---
name: project-bootstrapping
description: >
  Bootstraps a new Claude Desktop project by running a structured interview UI,
  challenging answers against official best practices, and generating three
  ready-to-use artefacts: an empty FRAMING.md scaffold, a CLAUDE.md, and a system prompt.
  Use when the user says "bootstrap project", "new project", "create project",
  "scaffold project", or "set up a new Claude project".
  NOT for modifying existing projects — use managing-tasks or writing-docs instead.
---
<!-- version: 2.0 | author: chief-of-droids workspace | last_updated: 2026-05-05 -->

# Project Bootstrapping Skill

Guides the user through creating a new Claude Desktop project from scratch.
Produces three artefacts: a FRAMING.md scaffold (user-owned, populated post-bootstrap),
a CLAUDE.md (repo output defaults with FRAMING.md alignment rule), and a system prompt
(copy-paste ready for Custom Instructions).

**Principle:** The artifact collects input. The conversation challenges and generates.
The Filesystem MCP writes files. Each step has one job — do not conflate them.

**Architecture constraint:** Artifacts cannot write to the filesystem. File writes
always happen in the conversation via Filesystem MCP after the user approves output.

**Generation order:** FRAMING.md (scaffold) → CLAUDE.md → system prompt.
Each file is confirmed and written before the next is generated.
FRAMING.md is written empty; the user populates it post-bootstrap.

---

## Reference Files

- `references/project-interview.md` — question set, validation rules, and
  answer-to-output mapping; read before rendering the form artifact
- `references/challenge-rules.md` — best-practice checks to run against answers;
  read before the challenge step
- `references/output-templates.md` — FRAMING.md scaffold, CLAUDE.md, and system
  prompt templates with placeholder substitution rules; read before generation step

---

## Workflow

### Step 1 — Verify environment

Attempt to read `references/project-interview.md` via Filesystem tool.
- If read succeeds: proceed normally
- If read fails: halt — `⚠️ Filesystem MCP unavailable — project-bootstrapping skill requires filesystem access. Verify MCP connection and retry.`

Never proceed from memory if reference files are unreachable.

---

### Step 2 — Render interview form artifact

Read `references/project-interview.md` via Filesystem tool.

Render a **React artifact** implementing the interview form:
- Six sections matching the sections in `project-interview.md`
- One input per question (short text or textarea as specified)
- Section headers as visual separators with section numbers
- Progress indicator showing current section / total sections
- Next / Back navigation per section; Submit on final section
- Submit disabled until all required fields are non-empty
- On submit: call `sendPrompt()` with all answers serialised as structured text:

```
BOOTSTRAP_ANSWERS:
S1Q1_REPO_NAME: <value>
S1Q2_PROJECT_NAME: <value>
S2Q7_SOLUTION: <value>
S2Q8_CONSTRAINTS: <value>
S3Q9_DOMAIN: <value>
S3Q10_STACK: <value>
S4Q11_OUTPUT_TYPE: <value>
S4Q12_QUALITY_BAR: <value>
S4Q13_FORMAT_DEFAULTS: <value>
S4Q14_MINIMUM_NECESSARY: <value>
S5Q15_OTHER_REPOS: <value>
S5Q16_SKILLS: <value>
S6Q17_HARD_RULES: <value>
S6Q18_TONE: <value>
S6Q19_GOTCHAS: <value>
S6Q20_WORKFLOWS: <value>
```

**Artifact UX rules:**
- Clean, readable layout — no decorative chrome
- Validation at form level: required fields only; deep validation happens in Step 3
- No API calls from inside the artifact — input collection only

---

### Step 3 — Detect and parse answers

When a message arrives prefixed with `BOOTSTRAP_ANSWERS:`, parse it as the
interview response. Do not treat it as a new bootstrap trigger.

Run field validation rules from `references/project-interview.md`:
- Flag any violation inline before proceeding to the challenge step
- If S1Q1 (repo name) fails format check, stop — cannot proceed without a valid repo name

---

### Step 4 — Challenge answers

Read `references/challenge-rules.md` via Filesystem tool.

Run every rule against the parsed answers. Output a **challenge report**:

```
## Challenge Report

| # | Field | Issue | Severity | Recommendation |
|---|-------|-------|----------|----------------|

X issues found. Propose fixes? (yes / no / skip)
```

- Zero issues: state "No issues found — proceeding to generation." and continue
- Issues present: wait for user response
  - `yes` → apply recommendations, show amended values, proceed to Step 5
  - `no` or `skip` → proceed to Step 5 with original answers
- Never auto-apply fixes without surfacing them first

---

### Step 5 — Generate and write artefacts (sequential)

Read `references/output-templates.md` via Filesystem tool.
Substitute all `[PLACEHOLDER]` values. Scan output for unfilled placeholders before
rendering each artefact — flag any that could not be filled and ask the user.

**Create repo directory first:**
Before generating any artefact, create `workspace/[REPO_NAME]/` via Filesystem tool.
- If directory already exists: flag — `⚠️ workspace/[REPO_NAME]/ already exists — files may be overwritten. Confirm? (yes / no)`

Then generate and write in this order:

---

**Artefact 1 — FRAMING.md (scaffold)**

Render the empty scaffold from Template 1 in `output-templates.md`.
Substitute `[PROJECT_NAME]` and `[DATE]` only — all section bodies remain
`> 🔲 To be defined — awaiting user input`.

Write directly to `workspace/[REPO_NAME]/FRAMING.md` after directory creation.
Confirm: `✅ Written: workspace/[REPO_NAME]/FRAMING.md (scaffold — populate before substantive work)`

No artifact rendering, no framing gate — FRAMING.md is user-owned from creation.

---

**Artefact 2 — CLAUDE.md**

Render as a markdown artifact:
- Title: `CLAUDE.md — [PROJECT_NAME]`
- Note above: "Repo output defaults — includes standing instruction to read FRAMING.md at session start."

Ask: "Write CLAUDE.md to `workspace/[REPO_NAME]/CLAUDE.md`? (yes / no)"

On confirmation: write file. Confirm: `✅ Written: workspace/[REPO_NAME]/CLAUDE.md`

---

**Artefact 3 — System Prompt**

Render as a code artifact (language: xml):
- Title: `system-prompt-[REPO_NAME].xml`
- Note above: "Paste this into Claude Desktop → New Project → Custom Instructions"

No file write — system prompt has no canonical filesystem location.

---

### Step 6 — Close

After all three artefacts are delivered, provide next-step instructions:

1. Copy the system prompt artefact into a new Claude Desktop project's Custom Instructions
2. Open a new conversation in the new project
3. Verify MCP connection — confirm the tools icon (hammer) is visible
4. Fill in `FRAMING.md` before substantive work — every section currently flagged `🔲 To be defined`

---

## Gotchas

- **Artifact cannot write files.** All writes happen in the conversation via Filesystem MCP.
- **sendPrompt() sends to the conversation.** The artifact's job ends at submit.
  Do not try to display challenge results inside the artifact.
- **Repo name validation must happen in Step 3, not in the artifact.**
- **Do not regenerate the artifact after submit.** Re-rendering the form resets state.
- **FRAMING.md is user-owned from creation.** Never modify FRAMING.md autonomously
  in any session — even when it is still a scaffold with "🔲 To be defined" markers.
- **Empty FRAMING.md does not block bootstrap.** The traceability rule in CLAUDE.md
  fires immediately — the user is responsible for populating FRAMING.md before
  substantive work begins. Step 6 surfaces this expectation.

---

## Composes With

| Skill | When |
| :--- | :--- |
| `managing-tasks` | After bootstrap — user may want to define tasks before starting work |
| `writing-docs` | If user requests additional project documentation beyond the bootstrap artefacts |
