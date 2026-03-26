---
name: project-bootstrapping
description: >
  Bootstraps a new Claude Desktop project by running a structured interview UI,
  challenging answers against official best practices, and generating four
  ready-to-use artefacts: a FRAMING.md, a CLAUDE.md, a TASKS.md, and a system prompt.
  Use when the user says "bootstrap project", "new project", "create project",
  "scaffold project", or "set up a new Claude project".
  NOT for modifying existing projects — use managing-tasks or writing-docs instead.
---
<!-- version: 1.2 | author: chief-of-droids workspace | last_updated: 2026-03-25 -->

# Project Bootstrapping Skill

Guides the user through creating a new Claude Desktop project from scratch.
Produces four artefacts: a FRAMING.md (user-owned scope definition), a CLAUDE.md
(repo output defaults with FRAMING.md alignment rule), a TASKS.md (initial backlog),
and a system prompt (copy-paste ready for Custom Instructions).

**Principle:** The artifact collects input. The conversation challenges and generates.
The Filesystem MCP writes files. Each step has one job — do not conflate them.

**Architecture constraint:** Artifacts cannot write to the filesystem. File writes
always happen in the conversation via Filesystem MCP after the user approves output.

**Generation order:** FRAMING.md → CLAUDE.md → TASKS.md → system prompt.
Each file is confirmed and written before the next is generated. FRAMING.md must
pass the framing gate before CLAUDE.md is written — CLAUDE.md references it.

---

## Reference Files

- `references/project-interview.md` — question set, validation rules, and
  answer-to-output mapping; read before rendering the form artifact
- `references/challenge-rules.md` — best-practice checks to run against answers;
  read before the challenge step
- `references/output-templates.md` — FRAMING.md, CLAUDE.md, TASKS.md, and system
  prompt templates with placeholder substitution rules; read before generation step
- `references/framing-gate.md` — blocking/advisory criteria, loop protocol, and
  assessment output format; read before running the framing gate after FRAMING.md is written

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
- Seven sections matching the sections in `project-interview.md`
- Section 2 (Project Framing) renders with per-question guidance text drawn
  from the question labels — these map directly to FRAMING.md sections
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
S2Q3_CONTEXT: <value>
S2Q4_PROBLEM: <value>
S2Q5_CLIENT: <value>
S2Q6_OBJECTIVES: <value>
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
S7Q21_INITIAL_TASKS: <value>
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

**Artefact 1 — FRAMING.md**

Render as a markdown artifact:
- Title: `FRAMING.md — [PROJECT_NAME]`
- Note above: "User-owned scope definition — you may edit this directly. Claude will propose edits only when you request them, and will never modify FRAMING.md autonomously."

Ask: "Write FRAMING.md to `workspace/[REPO_NAME]/FRAMING.md`? (yes / no)"

On confirmation: write file. Confirm: `✅ Written: workspace/[REPO_NAME]/FRAMING.md`

**Run framing gate immediately after write:**
Read `references/framing-gate.md` via Filesystem tool.
Re-read `workspace/[REPO_NAME]/FRAMING.md` from disk.
Run full assessment per gate protocol.
Output assessment in standard format.
Enter assessment loop — do not proceed to Artefact 2 until user issues `approve framing`
with zero blocking issues.

---

**Artefact 2 — CLAUDE.md**

Render as a markdown artifact:
- Title: `CLAUDE.md — [PROJECT_NAME]`
- Note above: "Repo output defaults — includes standing instruction to read FRAMING.md at session start."

Ask: "Write CLAUDE.md to `workspace/[REPO_NAME]/CLAUDE.md`? (yes / no)"

On confirmation: write file. Confirm: `✅ Written: workspace/[REPO_NAME]/CLAUDE.md`

---

**Artefact 3 — TASKS.md**

Render as a markdown artifact:
- Title: `TASKS.md — [PROJECT_NAME]`

Ask: "Write TASKS.md to `workspace/[REPO_NAME]/TASKS.md`? (yes / no)"

On confirmation: write file. Confirm: `✅ Written: workspace/[REPO_NAME]/TASKS.md`

---

**Artefact 4 — System Prompt**

Render as a code artifact (language: xml):
- Title: `system-prompt-[REPO_NAME].xml`
- Note above: "Paste this into Claude Desktop → New Project → Custom Instructions"

No file write — system prompt has no canonical filesystem location.

---

### Step 6 — Close

After all four artefacts are delivered, provide next-step instructions:

1. Copy the system prompt artefact into a new Claude Desktop project's Custom Instructions
2. Open a new conversation in the new project
3. Verify MCP connection — confirm the tools icon (hammer) is visible
4. Ask Claude: "What is the active repo and what does CLAUDE.md say?" — confirms routing and MCP
5. Say `show tasks` to confirm TASKS.md is readable
6. Say `start task TASK-001` to begin

---

## Gotchas

- **Artifact cannot write files.** All writes happen in the conversation via Filesystem MCP.
- **sendPrompt() sends to the conversation.** The artifact's job ends at submit.
  Do not try to display challenge results inside the artifact.
- **Repo name validation must happen in Step 3, not in the artifact.**
- **Do not regenerate the artifact after submit.** Re-rendering the form resets state.
- **FRAMING.md must pass the framing gate before CLAUDE.md is generated.** CLAUDE.md's
  alignment rule references FRAMING.md — a structurally weak FRAMING.md produces a
  broken project foundation.
- **FRAMING.md is user-owned after `approve framing` is issued.** During the gate loop,
  Claude may propose and write edits on user request. Once the user approves and the
  workflow proceeds to CLAUDE.md, FRAMING.md is user-owned — Claude must never propose
  modifications to it in any subsequent session unless explicitly asked.
- **Framing gate always re-reads from disk.** Never assess FRAMING.md from memory or
  from a prior turn's output — re-read the file on every `re-assess` and every
  `approve framing` call.

---

## Composes With

| Skill | When |
| :--- | :--- |
| `analyzing-business-cases` | During framing gate — `challenge-framing` workflow provides the checklist and assessment pattern; after bootstrap, for deeper framing refinement |
| `managing-tasks` | After file write — user may immediately want to start TASK-001 |
| `writing-docs` | If user requests additional project documentation beyond the four bootstrap artefacts |
