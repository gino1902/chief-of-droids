# Claude Project Configuration Playbook

> Personal reference — how to configure and use a Claude Project effectively
> Based on claude.ai Projects (Sonnet 4.6)
> v3.1 — Section 11 layer interaction chains corrected (2026-03-26)

---

## Multi-Project Architecture Overview

This workspace uses **multiple Claude Desktop projects**, each with its own system prompt and a default repo. A shared workspace skills layer is available to all projects. This playbook covers how to configure each layer.

| Layer | Location | What it governs |
| :--- | :--- | :--- |
| Workspace skills | `skills/` folder (shared) | Reusable skill modules, loaded via MCP |
| System prompt | Per project, Custom Instructions | Routing + behaviour |
| Repo defaults | `CLAUDE.md` per repo | Output format, tone for all use-cases in that repo |
| Use-case rules | `CONSTITUTION.md` per use-case | Content rules for a specific use-case |
| User intent | `FRAMING.md` per use-case | Why the use-case exists (user-owned) |

Full architecture reference: `claude-desktop/context/configuration-layer-guide.md`

---

## 1. System Prompt

**What it is:** Persistent instruction block prepended to every conversation in the project. Claude reads it first, every time. In a multi-project workspace it carries **two distinct responsibilities**: routing and behaviour.

**When to use:** Anything you'd type more than twice belongs here.

**How to set it:** Project → Custom Instructions field.

**What belongs here:**

| Category | Example |
| :--- | :--- |
| Routing — default repo | `"Default repo: /workspace/my-repo/ — read CLAUDE.md on session start"` |
| Routing — override rules | `"If user says 'in slide-gen', switch to /workspace/slide-gen/"` |
| Workspace skills paths | `"Load skills from /workspace/my-claude-fmk/claude-desktop/skills/"` |
| Role / framing | `"You are reviewing as a senior network architect"` |
| Workflows | `## WORKFLOW: arch-review ...` |
| Hard rules | `"Never recommend deleting production data"` |
| Tone / verbosity | `"Be concise. No filler. Flag uncertainty explicitly."` |

**What does NOT belong here:**

- Output format rules (version blocks, default file type) → `CLAUDE.md` in the target repo
- Use-case-specific content rules → `CONSTITUTION.md`
- Project intent or goals → `FRAMING.md`
- Large reference documents → Knowledge Files
- One-off task instructions → put in the conversation
- Repo-specific content of any kind — keep system prompts generic across repos

**Routing caveat:** Routing to a specific repo only works when (a) the system prompt contains explicit path declarations and (b) the **Filesystem MCP is connected**. If MCP is disconnected, Claude cannot reach any repo and will silently fall back to training knowledge — no error is raised. Always verify MCP connection at session start.

**Length guideline:** Keep it proportionate. The system prompt loads every turn and reduces space for conversation and knowledge retrieval. No official hard limit — but bloat has a real cost. Trim anything you no longer use. See `prompt-maintenance.md` for the token audit methodology.

**Structuring tip:** Use XML tags to separate routing from behaviour — Claude parses them unambiguously:

```xml
<routing>
Default repo: /workspace/my-repo/
On session start: read CLAUDE.md from default repo
Override: if user specifies another repo, switch target path
</routing>

<role>Senior network architect reviewer</role>
<context>Azure-based infrastructure, production environment</context>
<rules>Never recommend irreversible changes without confirmation</rules>
<skills>Load from /workspace/my-claude-fmk/claude-desktop/skills/</skills>
```

---

## 2. Knowledge Files

**What it is:** Documents attached to the project that Claude can read and reference. Persistent across all conversations.

**When to use:**

- Reference material you cite often (architecture specs, data dictionaries, company context)
- Skills or workflows too long to inline in the system prompt
- Templates Claude should reuse

**How to add:** Project → Add Content → Upload files or paste text.

**Options:**

| Approach | When |
| :--- | :--- |
| Inline in system prompt | Short skill/rule, <20 lines |
| Separate knowledge file | Long skill, template, reference doc |
| One file per skill | When you have 5+ skills and want clean separation |

**Key distinction:**

| System Prompt | Knowledge File |
| :--- | :--- |
| Always fully loaded, every turn | Retrieval-based — only relevant parts pulled per reply |
| Counts against context window every turn | Lower context pressure per turn |
| For instructions and behavior | For reference material and content |

**File specs:**

| Claim | Status |
| :--- | :--- |
| Individual files up to 30MB | ⚠️ Unverified — check support.claude.com before relying on this |
| Accepted formats: PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB | ⚠️ Unverified — format list changes; verify before use |
| JSON and XLSX supported (XLSX requires code execution enabled) | ✅ Verified: support.claude.com 2026-03-13 |
| Unlimited files per project | ⚠️ Unverified — check support.claude.com before relying on this |
| Large knowledge bases activate RAG mode automatically | ✅ Verified: support.claude.com 2026-03-13 |

Claude retrieves only what fits within the active context window per answer. RAG mode expands effective capacity beyond the context window limit for large knowledge bases.

> Note: The 30MB limit, format list, and file count cap are high-volatility claims — Anthropic updates these without versioned changelogs. Re-verify at support.claude.com before citing them in documentation.

---

## 3. Skills

**What it is:** Folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. Skills are the official Anthropic mechanism — uploaded as ZIP files via Customize > Skills, or loaded from the filesystem via MCP in the workspace skills pattern.

**Two skill models in this workspace:**

| Model | How it works | When to use |
| :--- | :--- | :--- |
| **Workspace skills** | Folder at `skills/` path, loaded by the system prompt via Filesystem MCP | Default pattern — skills reusable across multiple projects, under active development |
| **Uploaded skills** | ZIP file uploaded via Customize > Skills, stored per-user | Skills with no MCP dependency; stable skills rarely edited |

**Workspace skills caveat:** Workspace skills only load if (a) the system prompt instructs Claude to read them from the filesystem path and (b) the **Filesystem MCP is connected**. If MCP is disconnected, workspace skills are silently unavailable. Uploaded skills are unaffected by MCP status.

For full install, update, and maintenance procedures for both models: see `skills-playbook.md`.

---

## 4. Workflows

**What it is:** A named chain of skills executed in sequence. Defined once, invoked by keyword.

**When to use:** Multi-step tasks you run repeatedly.

**How to define:**

```
## WORKFLOW: arch-review
Trigger: user says "run arch-review"
Steps:
1. sizing-estimate skill on input
2. risk-review skill on result of step 1
3. summary skill on combined output
Final output format: [executive summary + risk table + sizing estimate]
```

**Parameterized variant:**

```
"run arch-review on [diagram] for [environment]"
```

Claude threads the variables through each step automatically.

**Chaining patterns:**

| Pattern | Description |
| :--- | :--- |
| Linear | A → B → C, each step feeds the next |
| Parallel + merge | Run A and B on same input, combine outputs |
| Conditional | `"if risk score > high, also run compliance-check"` |
| Recursive | Feed output back as input (e.g. critique → improve → critique) |

**Limit:** Long chains with verbose skills will eat your context window. Beyond 4–5 steps → move to API orchestration.

---

## 5. Guardrails

**What it is:** Rules that constrain Claude's behavior in this project. Defined in the system prompt.

**Hard rules (never violated):**

```
- Never recommend irreversible infrastructure changes without explicit confirmation
- Never output credentials or secrets, even as examples
- Always flag when a question is outside your defined scope
```

**Soft preferences (default behavior, overridable):**

```
- Default to concise responses unless asked for detail
- Assume production context unless stated otherwise
- Prefer options over single recommendations
```

**Failure modes to anticipate and guard against:**

| Failure | Guardrail |
| :--- | :--- |
| Sycophancy | `"Disagree with me when I'm wrong. Flag it explicitly."` |
| Hallucinating specifics | `"If uncertain, say so. Don't invent version numbers or names."` |
| Scope creep | `"Stay within [domain]. Flag out-of-scope requests."` |
| Verbose filler | `"No preamble. No summary of what you're about to do. Just do it."` |

---

## 6. Framing Patterns

**What it is:** How you set up the task context. Alternatives to the overused `"You are a..."` persona.

**Options:**

| Pattern | Example | Best for |
| :--- | :--- | :--- |
| Goal-first | `"The goal is X. Here's context..."` | Outcome-focused tasks |
| Constraint-first | `"Never do Y. Given that, help with..."` | Guardrail-heavy tasks |
| Audience framing | `"This is for a non-technical CFO."` | Tone/complexity shaping |
| Context dump | `"50-person SaaS, Series A, migrating monolith..."` | Rich situational grounding |
| Collaborative | `"Push back where you disagree."` | Reducing sycophancy |
| Task-only | `"Review this and flag risks."` | Simple, direct tasks |
| Format-as-frame | Provide a template, Claude fills it | Output structure control |

**Rule of thumb:** Persona (`"you are..."`) is rarely the best choice. Goal-first + context dump is stronger for most professional work.

---

## 7. Memory

**What it is:** Claude auto-generates persistent memories from conversations in a project. Visible and editable.

**Where to find it:** Project → Memory (or conversation header).

**When to push something to memory manually:**

- Your role, team context, recurring constraints
- Decisions already made ("we chose Postgres, stop suggesting alternatives")
- Preferences that always apply ("always output JSON, never YAML")

**What to avoid storing:**

- Sensitive data, credentials, PII
- Instructions that could override safety behavior
- Volatile data that changes often

**Practical use:** After a long onboarding conversation, explicitly say: `"Summarize the key decisions and context from this conversation as memory items."` Then clean up the result.

---

## 8. Invocation Patterns

**What it is:** How you trigger skills and workflows efficiently.

**Patterns:**

| Pattern | Example | When |
| :--- | :--- | :--- |
| Keyword trigger | `"run arch-review"` | Named workflows |
| Parameterized | `"run arch-review on [X] for [Y]"` | Variable inputs |
| Implicit | Input matches, Claude auto-triggers | Simple, well-defined tasks |
| Stacked | `"run skill-A then skill-B"` | Ad-hoc chaining |
| Override | `"run risk-review but skip the table format"` | One-off adjustment |

**Tip:** Define your trigger keywords clearly in the system prompt. Ambiguous triggers cause Claude to guess.

---

## 9. Context Window Management

**What it is:** The total tokens Claude can see in one turn. System prompt + retrieved knowledge file content + conversation history + your message.

**Plan limits:**

| Plan | Context Window |
| :--- | :--- |
| Pro | 200K tokens (~500 pages) |
| Team | 200K tokens |
| Enterprise | 500K tokens (specific models) |

**What eats it:**

| Source | Impact |
| :--- | :--- |
| System prompt | Every turn, always fully loaded |
| Long conversation history | Grows unbounded |
| Knowledge file retrieval | Relevant chunks per turn |
| Verbose skill definitions | Multiplied across turns |

**How to stay lean:**

- Keep system prompt proportionate — trim unused skills and rules
- Start a new conversation when the thread gets long
- Summarize old context: `"Summarize this conversation in 200 words, I'll use it as context in a new thread"`
- Put large reference docs in knowledge files, not the system prompt
- Remove skills you no longer use

**Signal that you're hitting limits:** Claude starts forgetting earlier instructions or ignoring parts of the system prompt.

---

## 10. When to Leave claude.ai

**Stay in claude.ai when:** Tasks are interactive, exploratory, or one-off.

**Move to API when:**

| Need | Solution |
| :--- | :--- |
| Automate a chain of calls | Python/Node script, one call per skill |
| Process batches of inputs | Batch API |
| Trigger on events | n8n, Make, or custom webhook |
| Log and audit outputs | API with structured responses |
| Chain 5+ skills reliably | API orchestration, each step explicit |
| Build a tool for others | API-powered app or artifact |

**Move to Claude Code when:**

- Tasks involve your local codebase
- You need file system access
- You want to run and test code in a loop

**Quick decision:**

```
Interactive + exploratory → claude.ai Project
Repeatable + automated   → API
Codebase-connected       → Claude Code
```

---

## 11. Layer Model — CLAUDE.md, CONSTITUTION.md, FRAMING.md

The architecture overview table names five layers. Three of them — CLAUDE.md, CONSTITUTION.md, and FRAMING.md — are files you create and maintain in each repo. This section explains what belongs in each and how they interact.

### The three repo-level files

**`CLAUDE.md`** — repo defaults. One per repo, at the repo root. Defines output format, tone, version block rules, and flagging conventions that apply to every use-case in that repo. Claude reads this at session start when the system prompt instructs it to. Never use-case-specific. Never contains routing rules (those belong in the system prompt).

```
What belongs: output format (default file type, version block structure), tone,
flagging rules ([ASSUMPTION], [UNVERIFIED]), layer boundary notes
What does NOT belong: routing, use-case content rules, project intent
```

**`CONSTITUTION.md`** — use-case rules. One per use-case, inside the use-case folder. Defines content rules, quality constraints, required sections, and verification requirements specific to that use-case. Takes precedence over CLAUDE.md for everything it covers. Claude-editable — updated as the use-case evolves.

```
What belongs: audience, content rules (required/allowed/forbidden), output structure,
verification requirements, research scan sources, version history
What does NOT belong: project intent (that's FRAMING.md), repo-wide defaults (that's CLAUDE.md)
```

**`FRAMING.md`** — user intent. One per use-case, inside the use-case folder. Explains why the use-case exists — strategic deliverable, audience, goals, constraints. Author-owned. **Never modified by Claude under any circumstances.** Claude reads it to understand intent; it does not write to it.

```
What belongs: strategic deliverable, target audience, goals, non-goals,
key constraints, why this use-case exists
What does NOT belong: content rules, output format, Claude instructions of any kind
```

### How they interact

The layers operate on two distinct axes — conflating them is the source of most confusion.

**Content authority** — which layer's rules win when they conflict:

```
CONSTITUTION.md    ← highest content authority (use-case scope)
    ↓ overrides
CLAUDE.md          ← repo defaults (all use-cases in this repo)
    ↓ overrides
system prompt      ← tone/style defaults in <defaults> only
```

**Derivation** — which layer is the source of truth for content:

```
FRAMING.md         ← source of truth (user intent, immutable)
    ↓ derived from
CONSTITUTION.md    ← use-case rules (must align with FRAMING.md)
```

CLAUDE.md is set independently as the repo-wide baseline — it has no derivation relationship with FRAMING.md or CONSTITUTION.md.

The system prompt governs **routing and behaviour**, not content. Its behavioural rules (e.g. "never write without confirmation") cannot be overridden by any content layer regardless of what CONSTITUTION.md or CLAUDE.md say. Routing rules determine which CLAUDE.md and CONSTITUTION.md apply before any content layer is consulted.

### When to create each file

| File | Create when |
| :--- | :--- |
| `CLAUDE.md` | Setting up a new repo — before any use-case work begins |
| `CONSTITUTION.md` | Starting a new use-case — before generating any output |
| `FRAMING.md` | Starting a new use-case — write this first, before CONSTITUTION.md |

If FRAMING.md does not exist and Claude is asked to run the skill-proposal interview or generate any strategic output, stop and create it first. The output will not be grounded without it.

### CONSTITUTION.md required sections

A CONSTITUTION.md missing any of these sections is incomplete and should block generation:

| Section | Purpose |
| :--- | :--- |
| Audience Override | Tone, assumed knowledge, translation rules |
| Content Rules | Required, allowed, forbidden per output |
| Output Structure | Layout, required vs. optional sections |
| Verification Requirement | Which sources are authoritative for this use-case |
| Research Scan Sources | URLs to fetch before any web search ("none" if not applicable) |
| Version History | Version, date, change log |

Full architecture reference: `claude-desktop/context/configuration-layer-guide.md`

---

## 12. Operational Hygiene

Four recurring maintenance moves that keep the workspace working reliably across sessions.

### Cold session bootstrap

Every new Claude Desktop conversation starts cold — no memory of previous sessions, no tools pre-loaded. Before issuing any repo-dependent instruction, run this checklist:

1. **Verify MCP** — tools icon (hammer) visible in the chat header. If missing, check `Customize > Connectors` and restart Claude Desktop.
2. **Bootstrap tools** — if your system prompt references filesystem tools, issue a tool_search call first: `tool_search("read file filesystem")`. This ensures Filesystem MCP tools are loaded before any file read is attempted.
3. **Confirm active repo** — ask Claude: *"What is the active repo and what does CLAUDE.md say?"* A correct answer confirms routing and MCP are working.
4. **Verify skills** — ask Claude: *"What workspace skills are available?"* If the answer is "none" and skills should be present, MCP is not reaching the skills path.

If any step fails, fix before proceeding. Do not work around a broken bootstrap — stale fallbacks produce silent errors.

> Lesson from slide-gen TASK-036: tools must be loaded before HOW-TO-TRIGGER.md (or any skill file) is read. A single `tool_search` line in the system prompt's `<skills>` block fixes this reliably.

### TASKS.md as continuity mechanism

Claude has no memory between sessions. TASKS.md is the continuity layer — it records what is pending, what is done, and why decisions were made. Treat it as a first-class document, not a scratchpad.

Conventions that work:

- One TASKS.md per repo at the root; use-case tasks in `use-case-n/TASKS.md`
- Every task has: ID, description, target file, scope note, done date when closed
- Close tasks immediately when done — not at session end
- Add a `[DECISION]` note inline when a task produces a non-obvious choice
- Start every session with: *"show tasks"* — Claude reads TASKS.md and reports pending work
- End every session by verifying TASKS.md reflects actual state

The TASKS.md format is also the handoff protocol. If you switch machines, share the repo, or resume after a long gap, TASKS.md tells Claude exactly where things stand without a long onboarding conversation.

### System prompt token audit cadence

System prompts accumulate bloat. Rules get added, old skills stay in, routing paths become stale. A bloated system prompt costs tokens every turn and degrades instruction-following.

Trigger a token audit when:
- The system prompt grows by more than ~200 tokens
- You add a new workflow or skill block
- Claude starts ignoring parts of the system prompt
- It has been more than 4–6 weeks since the last audit

The four-step audit pattern (from `prompt-maintenance.md`):
1. **Challenge sections** — for each block, ask: does this still apply? Is this in the right layer?
2. **Measure** — count tokens, identify the heaviest blocks
3. **Verify behavioural scope** — does removing a block change Claude's behaviour? If not, remove it
4. **Verify against official docs** — UI paths and product claims go stale; re-check any that are more than 3 months old

Full methodology: `claude-desktop/context/prompt-maintenance.md`

### Stale content risk

Anthropic product UI paths, feature names, plan availability, and install instructions change frequently. Any documentation that references these will drift.

Practical rules:
- Mark every product claim with a verification date: `> ✅ Verified: [source] [date]`
- Re-verify any claim older than 3 months before relying on it
- Never copy UI paths from memory — fetch the current official doc
- Official sources: `support.claude.com`, `docs.claude.com`, `code.claude.com/docs`
- When a claim can't be verified, mark it explicitly: `> ⚠️ Unverified — check before use`

> Lesson from TASK-005: install paths, settings menu locations, and plan gating all changed between v1.0 docs and the 2026-03-13 verification pass. Several claims that appeared correct were stale by one or two UI reorganisations.

---

## Quick-Start Template: System Prompt Structure

Use XML tags to separate sections — Claude parses them unambiguously:

```xml
<routing>
Default repo: /workspace/[repo-name]/
On session start: read CLAUDE.md from default repo
Override: if user says "in [other-repo]", switch to /workspace/[other-repo]/
Note: routing requires Filesystem MCP to be connected
</routing>

<role>
[One sentence: what this project assistant does]
</role>

<context>
[2-3 sentences: who you are, your stack, your constraints]
</context>

<rules>
- [Hard rule 1]
- [Hard rule 2]
- Never write files without confirmation
- Never modify FRAMING.md
</rules>

<defaults>
- [Tone/verbosity]
- [Assumptions to make]
</defaults>

<skills>
Load workspace skills from: /workspace/my-claude-fmk/claude-desktop/skills/
[Or define inline: ## SKILL: [name] / Trigger: [when] / Steps: [numbered]]
</skills>

<workflows>
## WORKFLOW: [name]
Trigger: [keyword]
Steps: [skill chain]
Output: [final format]
</workflows>
```

**Note on output format defaults:** Do NOT put output format rules (version blocks, file types) in the system prompt. These belong in `CLAUDE.md` in the target repo. The system prompt governs routing and behaviour only.

---

## Examples

Full worked examples are stored separately. Each example includes a system prompt file and a `CONSTITUTION.md` knowledge file, ready to drop into a project.

| Example | Files | Description |
| :--- | :--- | :--- |
| Routing System Prompt Template | `examples/routing-system-prompt-template.md` | Generic reusable system prompt for the multi-project routing architecture. Covers default repo declaration, repo override rules, skills injection, workflow skeleton, field-by-field guidance, and MCP dependency checklist. Starting point for any new project. |
| Data Engineering — Headless | `examples/data-eng-headless-system-prompt.md` `examples/data-eng-headless-CONSTITUTION.md` | Headless pipeline assistant (dbt, Spark, Delta Lake, Azure Databricks). JSON-only outputs, medallion architecture, CONSTITUTION.md pattern for rules. |
| Headless Web App Builder | `examples/headless-webapp-system-prompt.md` `examples/headless-webapp-CONSTITUTION.md` | Build assistant for a headless app backed by Unity Catalog. FastAPI intermediary, Azure Event Hub (bidirectional), MS Teams Adaptive Card notifications (workflow + monitoring), schema-sync tooling. Explicit output modes: developer, ci, tool. |

---

| Field        | Value      |
|:------------ |:---------- |
| Version      | 3.1        |
| Last Updated | 2026-03-26 |
| Status       | Final      |

*v3.1 — Section 11 "How they interact": single mixed chain replaced with two-axis model (content authority / derivation), consistent with context-layers-guide.md v2.3. System prompt axis clarified as separate. CLAUDE.md correctly removed from derivation chain.*
