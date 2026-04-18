# How to Trigger Each Skill

> **Scope:** This skills library lives at `workspace/skills/` and is shared across
> all projects in the workspace. It is **read-only** — never modified from within
> a project. Changes go through the `creating-skills` workflow only.

Load the matching skill when any trigger signal in this file is detected. No slash command or explicit invocation is required.

Load every skill whose trigger signals match the user request. Read each matched SKILL.md in full before responding. If multiple skills match, load all of them before producing any output.

If no skill trigger matches the user request, proceed without loading any skill — respond directly from CLAUDE.md context.

If a signal is ambiguous between two or more skills, load all candidate skills.

If this file is unreadable, notify the user and proceed without skill loading.

**Routing mechanism:** Claude reads this file at session bootstrap via filesystem:read_text_file. Each match triggers an explicit read of the corresponding SKILL.md. No automatic loading occurs — every load is initiated by Claude from this file's signal list.

---

## managing-tasks

Load this skill when the prompt contains any task list read, write, or state transition signal.

**Read triggers:**
- "show tasks"
- "next task"
- "what's pending"
- "what should I work on next"

**Write triggers:**
- "start task TASK-XXX"
- "done task TASK-XXX"
- "add task"
- "update task TASK-XXX"
- "bulk update tasks"

Also load when the user asks to record, close, or transition any task by ID.

---

## executing-tasks

**Pattern-based triggers (primary):**

Load this skill when the prompt matches any of:
- `% execute % task %` — e.g. "Claude execute the following task: ...", "execute TASK-025"
- `run % task %` — e.g. "run TASK-025", "run the complex task"
- `% run % task %` — e.g. "Claude run task TASK-XXX"

where `%` matches any text including empty string.

**Opt-in trigger (secondary — after managing-tasks):**

After `start TASK-XXX` transitions a task to 🟡 In Progress, ask once:
> "TASK-XXX is now In Progress. Run executing-tasks workflow, or proceed directly?"

This question fires unconditionally — task scope appearing self-evident is not a reason to skip it.
Reason: the executing-tasks workflow is high-cost; confirming opt-in prevents accidental activation on simple task state transitions.

**Does NOT trigger on:**
- `start TASK-XXX` alone — that belongs to managing-tasks
- `my intent is [...]` — too ambiguous

**What it does:**
- Scans the triggering prompt for a TASK-XXX pattern; if found, looks it up in TASKS.md
- If TASK-XXX found in TASKS.md: uses entry fields to pre-fill intent formulation
- If TASK-XXX present in prompt but not found in TASKS.md: hard stop with warning
- If TASK-XXX absent from prompt: uses prompt content as intent basis
- Confirms intent and target via elicit forms (Artifact 1 + Artifact 2)
- Classifies task type (code / research / doc / file-write / skill-authoring / framing)
- Challenges acceptance criteria before plan authoring
- Produces and approves a stepped plan
- Designs a QA suite against the plan before any sub-task executes
- Executes sub-tasks via composing skills per task type
- Verifies all outputs against the QA suite
- If TASK-XXX was found: prompts to close via managing-tasks `done task`
- If no TASK-XXX: creates entry via `add task` then closes via `done task`

**Does NOT:**
- Manage task state — that is managing-tasks
- Implement domain logic — defers to composing skills per task type
- Continue when TASK-XXX is present in prompt but not found in TASKS.md — that is always a hard stop

---

## managing-sessions

Load this skill when the prompt contains any session history analysis, pruning, or memory hygiene signal.

**Explicit triggers:**
- "manage sessions"
- "analyse sessions"
- "prune sessions"
- "session hygiene"
- "what should I keep"
- "challenge memories"
- "check memories"

**Auto-trigger (system prompt rule):**
During session bootstrap, if `recent_chats` returns ≥10 sessions, load this
skill before proceeding with any other work.

**What it does:**
- Analyses session history using `recent_chats` + `conversation_search`
- Classifies findings as `on-disk`, `not-on-disk`, or `superseded`
- Recommends a prune boundary with explicit date
- Writes findings to `.tasks/sessions-findings/` and removal log to
  `.logs/sessions-removed/` (removal log only when sessions are confirmed removed)
- Produces a manual deletion checklist (user executes in claude.ai UI)
- Challenges userMemories against on-disk sources for contradictions

**Does NOT:**
- Delete sessions — deletion is always manual
- Modify userMemories — surfaces contradictions only

---

## architecting-data-platforms

Load this skill when the prompt contains any data platform design, architecture, or assessment signal.

**Examples:**
- "Design a medallion architecture for our HR data"
- "We're building a lakehouse on Databricks"
- "Should we use DLT or plain Workflows?"
- "Where are we in the platform project?"
- "Review our ADRs"
- "Help me build the cost model"

Also load when a phase completion signal is detected.
See `architecting-data-platforms/references/gate-activation.md` for details.

---

## reviewing-tech-claims

Load this skill only when an explicit verification qualifier appears in the prompt — not on topic alone.

**Qualifying phrases:**
- `technically verified`
- `verify against official docs`
- `tech-checked`
- `source-verified`
- `confirmed against official source`

**Example:**
- "Write a setup guide for the Filesystem MCP — technically verified"
- "tech-checked: what is the correct mlflow.prophet.log_model signature?"

Do not load this skill without one of these qualifiers. Add the qualifier when accuracy against official documentation is required.

---

## writing-docs

Load this skill when the prompt contains any request to produce a structured document, guide, brief, or report.

**Examples:**
- "Write a requirements brief for use-case-1"
- "Document this workflow"
- "Draft an ADR for the storage account design"
- "Create a runbook for the forecasting pipeline"
- "Write a playbook for our data ingestion practices"
- "Turn these notes into a reference doc"
- "Fix the formatting on this document"

For `.md` output, additionally read
`writing-docs/references/markdown-formatting.md` before writing.

For document type triggers (ADR, Requirements Brief, Runbook, Playbook), additionally read `writing-docs/references/templates.md` and copy the relevant template.

---

## creating-skills

Load this skill when the prompt contains any request to create, author, build, or define a new skill; critique or assess an existing one; enrich an existing one from catalog sources; identify skill gaps from session history; or add a new external source to the skill catalog.

**Triggers:**
- `author skill <n>` — scaffold a new SKILL.md from a user description
- `critique skill <n>` — compliance assessment of an existing SKILL.md against checklist
- `enrich skill <n>` — catalog-driven enrichment; identifies patterns missing from an existing skill
- `assess all skills` — run full assessment across all skills in `skills/`
- `recommend skills` — analyse session findings to surface skill gaps
- `add source: [URL]` — evaluate and add a new external source to `skill-sources.md`

**Natural-language equivalents (also load this skill):**
- "create a skill for..."
- "I need a skill that..."
- "build a skill for..."
- "new skill for..."
- "make a skill that..."
- "what skills should I add"
- "skill gaps from sessions"
- "what am I missing as skills"
- "what's missing from skill..."
- "improve skill from catalog"
- "add [URL] to skill sources"
- "add [URL] to the skills catalog"
- "I want to add X to the skills catalog sources"
- "evaluate [URL] as a skill source"

**Examples:**
- "author skill data-quality"
- "critique skill writing-docs"
- "enrich skill managing-tasks"
- "assess all skills"
- "I need to create a skill to manage tasks"
- "recommend skills"
- "what skills am I missing based on my sessions?"
- "what's missing from skill creating-skills"
- "add github.com/foo/bar to skill sources"
- "I want to add https://github.com/foo/bar to the skills catalog"

**Note on source fetch:**
- `author skill`, `critique skill`, `assess all skills` — always fetch official sources:
  1. `https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices`
     > ⚠️ Unverified — URL exists in official nav but content is not publicly accessible. Fetch before use; flag if unreachable.
  2. `https://github.com/anthropics/claude-code/tree/main/plugins/`
     (official Anthropic skills examples — confirmed location of bundled skills including frontend-design)
  3. `https://agentskills.io/specification`
     (Agent Skills open standard — referenced in official Anthropic Claude Code docs)
- `enrich skill` — fetches sources from `references/skill-sources.md` catalog (internal + external)
- `recommend skills` — skips source fetch; reads session findings only
- `add source` — runs its own fetch protocol via `references/workflows/add-source.md`; Step 1 does not apply

**Note on official source applicability:**
These sources describe the Claude Code Agent Skills mechanism (VM-based, frontmatter scanning, `disable-model-invocation`). This workspace uses Claude Desktop + Filesystem MCP — not all official behaviors apply. See CLAUDE.md `## Skills Architecture` for the full distinction before applying any guidance from these sources to skill assessment.

---

## analyzing-business-cases

Explicit trigger only — do not load on topic alone.
Reason: these skills execute multi-phase workflows with significant write operations — loading on topic ambiguity risks unintended execution.

**Triggers:**
- `build framing <project-name>` — scaffold a new FRAMING.md from a user prompt
- `challenge framing <project-name>` — critique an existing FRAMING.md
- `assess-artifacts <project-name>` — cross-artifact consistency check

**Examples:**
- "build framing my-project"
- "challenge framing my-project"
- "assess-artifacts my-project"

---

## project-bootstrapping

Explicit trigger only — do not load on topic alone.
Reason: these skills execute multi-phase workflows with significant write operations — loading on topic ambiguity risks unintended execution.

**Triggers:**
- `bootstrap project` — start a new project from scratch (full 3-phase flow)
- `new project` — alias
- `create project` — alias
- `scaffold project` — alias

**What it does:**
- Phase 1: renders a multi-step form artifact to collect project intent
- Phase 2: challenges answers against Claude best practices (blocking + advisory)
- Phase 3: generates system prompt, CLAUDE.md, and TASKS.md artifacts; writes files via MCP

**Does NOT trigger on:**
- Requests to create a skill → use `creating-skills`
- Requests to frame a use-case → use `analyzing-business-cases`
- Requests to add tasks to an existing project → use `managing-tasks`

---

## standardizing-artefacts

Explicit trigger only — do not load on topic alone.
Reason: these skills execute multi-phase workflows with significant write operations — loading on topic ambiguity risks unintended execution.

**Triggers:**
- `audit <file>` — block-by-block determinism audit of a single file; fix phase per block
- `audit <file> --full` — single-pass audit across all 4 blocks; report only, no fix phase
- `standardize <file>` — alias for `audit <file>`
- `assess determinism <file>` — alias for `audit <file>`

**What it does:**
- Accepts a file path as input (filesystem path, uploaded file, or inline paste)
- Identifies the artefact type (skill, functional-spec, technical-spec, use-case, acceptance-test, task-unit-test) and routes to the matching schema
- Reads the schema for the identified type from `references/` — every recommendation must be grounded in a schema `req_id`
- `audit <file>`: runs 4 blocks (B1 Foundation, B2 Evidence Layer, B3 Behavior Contract, B4 Deployment Gate) with per-block fix approval gates
- `audit <file> --full`: runs all 33 criteria in one pass; produces report only — fix phase requires re-running as `audit <file>`
- Does NOT check industry-standard structure, best-practice compliance, or suggest format changes unless a schema req_id requires it

**Routing boundary vs `creating-skills`:**

| | `standardizing-artefacts` | `creating-skills` |
| :--- | :--- | :--- |
| Assesses | Determinism — will an LLM execute this predictably? | Best-practice compliance — does this follow Anthropic/agentskills.io guidance? |
| Output | Determinism compliance report + rewrite | Assessment finding table |
| Owns fix phase? | Yes — rewrites the file | No — surfaces findings only |
| Triggered by | `audit <file>`, `standardize <file>` | `critique skill <n>`, `assess all skills` |

Run both for a full quality check on a skill file.

**Does NOT trigger on:**
- Requests to author a new skill → use `creating-skills`
- Requests to assess best-practice compliance → use `creating-skills`
- Requests without a file path or inline content — emits ERROR and stops

---

## brainstorming-ideas

Load this skill when the user wants to explore a feature idea, frame a problem, or think through options before deciding what to build. Load proactively whenever requirements seem unclear or a decision is being explored — not only on explicit "brainstorm" mentions.

**Explicit triggers:**
- "let's brainstorm"
- "brainstorm [topic]"
- "help me think through [X]"
- "I'm not sure what to build"
- "what should we build"
- "I have an idea for [X]"

**Natural-language triggers:**
- Vague or ambitious feature requests
- Problems presented with multiple valid solutions
- Prompts where the user is thinking out loud
- Requests to explore or frame something before implementation

**Examples:**
- "Let's brainstorm a notification redesign"
- "I'm not sure what to build for the reporting dashboard — help me think it through"
- "What should we do about the onboarding flow?"
- "Help me figure out what the search feature should do"

**Does NOT trigger on:**
- Implementation requests ("implement the CSV export button") → direct work, no brainstorm needed
- Factual lookups ("what does the users table schema look like?") → direct answer
- Scoped defect work ("define acceptance criteria for the login bug fix") → use `analyzing-business-cases` or proceed directly

**What it does:**
- Phase 0: resume check, domain classification (Software / Non-software / Neither), scope classification (Lightweight / Standard / Deep)
- Phase 1: context scan + product pressure test + collaborative dialogue (one question at a time)
- Phase 2: 2–3 concrete approaches with pros/cons and recommendation
- Phase 3: write requirements document to `docs/brainstorms/YYYY-MM-DD-<topic>-requirements.md`
- Phase 4: handoff to planning, direct work, or save-and-stop

Non-software domain branches to `references/universal-brainstorming.md` — facilitation-only, no requirements document.

**Does NOT:**
- Implement code — explicit scope boundary
- Produce a plan — planning is a handoff output, not part of this skill

---

## Combining skills

Skills compose automatically. Load all skills whose triggers match the request.

| Task | Skills loaded |
| :--- | :--- |
| Write a tech-verified architecture doc as `.md` | `architecting-data-platforms` + `reviewing-tech-claims` + `writing-docs` |
| Document a phase deliverable | `writing-docs` |
| Verify a CLI command | `reviewing-tech-claims` |
| Platform assessment | `architecting-data-platforms` |
| Write a runbook with verified commands | `writing-docs` + `reviewing-tech-claims` |
| Write a playbook | `writing-docs` |
| Author or assess a skill | `creating-skills` |
| Enrich a skill from catalog | `creating-skills` |
| Identify skill gaps from session history | `creating-skills` |
| Add a new source to skill catalog | `creating-skills` |
| Frame or challenge a use case | `analyzing-business-cases` |
| Frame a data platform use case | `analyzing-business-cases` + `architecting-data-platforms` |
| Frame + write the document | `analyzing-business-cases` + `writing-docs` |
| Read, add, or transition tasks | `managing-tasks` |
| Execute an existing task with quality workflow | `managing-tasks` + `executing-tasks` |
| Execute a new task without a prior TASKS.md entry | `executing-tasks` + `managing-tasks` (at close) |
| Execute a skill-authoring task | `managing-tasks` + `executing-tasks` + `creating-skills` |
| Execute a doc task | `managing-tasks` + `executing-tasks` + `writing-docs` |
| Bootstrap a new Claude Desktop project | `project-bootstrapping` |
| Analyse, prune, or audit session history | `managing-sessions` |
| Capture session value then write a doc | `managing-sessions` + `writing-docs` |
| Session prune surfaces open tasks | `managing-sessions` + `managing-tasks` |
| Session prune then identify skill gaps | `managing-sessions` + `creating-skills` |
| Audit artefact determinism | `standardizing-artefacts` |
| Audit artefact determinism + best-practice compliance | `standardizing-artefacts` + `creating-skills` |
| Brainstorm a feature or decision before building | `brainstorming-ideas` |
| Brainstorm then write a structured doc | `brainstorming-ideas` + `writing-docs` |
| Frame a use case via brainstorm | `brainstorming-ideas` + `analyzing-business-cases` |


| Field        | Value       |
|--------------|-------------|
| Version      | 1.11        |
| Last Updated | 2026-04-18  |
| Status       | Draft       |
