# Bootstrapping a New Claude Desktop Project

> How to use the `project-bootstrapping` skill to scaffold a new project
> from scratch — FRAMING.md, CLAUDE.md, TASKS.md, and a system prompt —
> in a single guided session.

---

## 1 — What bootstrapping does

The `project-bootstrapping` skill creates four artefacts for a new Claude Desktop
project in a fixed sequence: a FRAMING.md (user-owned scope definition), a CLAUDE.md
(repo output defaults referencing FRAMING.md), a TASKS.md (initial backlog), and a
system prompt (copy-paste ready for Custom Instructions).

The workflow runs in three phases. Phase 1 collects your answers through an
interactive form. Phase 2 challenges them against best practices. Phase 3 generates
and writes the four artefacts in order, with a blocking framing gate between artefact
1 and artefact 2.

FRAMING.md is the foundation. It is written first and must pass a structural quality
gate before CLAUDE.md is generated. CLAUDE.md references FRAMING.md as the binding
scope definition — a weak FRAMING.md produces a broken project foundation.

---

## 2 — Prerequisites

Before triggering the bootstrapper:

- You must be working inside the **Chief of Droids** Claude Desktop project.
  The bootstrapper reads workspace skills and writes to the filesystem via the
  Filesystem MCP, which is configured in that project. Running it from any other
  project will fail silently at Step 1 if MCP is not connected.
- Filesystem MCP must be connected — verify the tools icon (hammer) is visible
  in the Claude Desktop chat header before starting.
- Have a rough idea of: what the new project is for, what it produces, what the
  first 3–5 tasks are, and the primary audience. You do not need to have the
  details worked out — the interview will surface them.

---

## 3 — How it works

The skill runs in three sequential phases. Each phase has one job.

**Phase 1 — Collect**
Claude renders a multi-section React artifact as the interview form. You fill in
seven sections covering project identity, framing (Context / Problem / Client /
Objectives / Solution / Constraints), domain and stack, deliverables, routing,
behaviour rules, and initial tasks. On submit, the form calls `sendPrompt()` to
fire your answers into the conversation as a `BOOTSTRAP_ANSWERS:` block. Claude
detects the prefix and enters Phase 2. The artifact's job ends at submit — do
not expect results inside the form.

**Phase 2 — Challenge**
Claude reads the answers and runs best-practice checks against them. Issues are
reported as Major (blocks generation until resolved) or Minor (advisory — you can
proceed or adjust). The challenge covers CLAUDE.md scope, system prompt rule
quality, workflow definition, and task actionability. You respond: fix the issues,
skip them, or override.

**Phase 3 — Generate**
Claude generates and writes four artefacts in strict sequence. Each artefact is
rendered, confirmed, and written to disk before the next is generated. FRAMING.md
is written first and then assessed by the framing gate — a blocking loop that
prevents progression to CLAUDE.md until `approve framing` is issued with zero
blocking issues. The system prompt is the only artefact not written to disk —
it is copy-paste only.

---

## 4 — Running the bootstrapper

**Step 1 — Trigger**

In the Chief of Droids project, say:

```
bootstrap project
```

Claude will attempt to read the skill's reference files via Filesystem MCP. If
MCP is unavailable it will halt immediately with a warning — do not proceed until
MCP is confirmed connected.

**Step 2 — Fill in the form**

The form artifact appears with seven sections. Work through them in order. Every
required field is marked. Use the Back button if you want to revise a section
before submitting. When all required fields are filled, click Submit. The form
calls `sendPrompt()` to send answers to the conversation — do not close the
artifact while Claude is processing.

**Step 3 — Review the challenge report**

Claude outputs a challenge table. For each issue:

- **Major** — Claude pauses and waits. Either amend the answer inline or type
  `override` with a brief reason to proceed anyway.
- **Minor** — Claude notes the recommendation. Type `fix` to apply it or `skip`
  to proceed.

If there are no issues, Claude states this and proceeds automatically.

**Step 4 — Review and confirm FRAMING.md**

Claude renders FRAMING.md and asks for confirmation to write it. After the file
is written, the framing gate fires automatically. Claude re-reads FRAMING.md from
disk and runs the full 14-item assessment (7 blocking, 7 advisory).

Review the assessment output:

- **Blocking issues** — Claude cannot proceed to CLAUDE.md until these are
  resolved. Options:
  - Edit FRAMING.md yourself, then type `re-assess`
  - Ask Claude to propose fixes — type `fix B1 B3` (or `fix all`)
  - Claude proposes the edit in chat, awaits confirmation, writes to disk, then
    auto-triggers `re-assess`
- **Advisory issues** — surfaced for awareness but do not block progression.
  Address them or ignore them.

When all blocking issues are resolved, type `approve framing`. Claude re-runs the
blocking criteria inline and, if all pass, confirms and proceeds to CLAUDE.md.

**Step 5 — Review CLAUDE.md, TASKS.md, and the system prompt**

Three artefacts are generated in sequence. Each is rendered and awaits confirmation
before the file write. If anything needs adjusting, say so before confirming — Claude
will regenerate the affected artefact with your correction.

The system prompt is the final artefact. It is rendered as a copy-ready XML block.
There is no file write — copy it manually.

**Step 6 — Copy the system prompt**

Copy the system prompt artefact. In Claude Desktop, create a new project, open
Custom Instructions, and paste it in. The new project is ready for its first
session.

---

## 5 — The interview questions explained

### Section 1 — Identity

Sets the repo name and project display name. The repo name becomes the filesystem
directory — it must be lowercase with hyphens only. A format violation halts the
workflow at Step 3 before any challenge or generation runs.

### Section 2 — Project Framing

Six questions that map directly to FRAMING.md sections. Answers are substituted
verbatim into the template — write as prose, not bullet points.

| Question | FRAMING.md section | Guidance |
| :--- | :--- | :--- |
| Context | `## Context` | Stable as-is state. No problem statement here. |
| Problem | `## Problem` | What is broken or missing and why it matters. |
| Client | `## Client` | Primary audience and secondary stakeholders. |
| Objectives | `## Objectives` | Measurable outcomes, not activities. One per line. |
| Solution | `## Solution` | What you intend to build. One paragraph, approach only. |
| Constraints | `## Constraints` | Technical, data, timeline, budget, hard exclusions. |

The framing gate assesses these answers after FRAMING.md is written. Thin or
misframed answers will produce blocking gate findings — it is more efficient to
write carefully here than to fix in the gate loop.

### Section 3 — Domain & Stack

Grounds Claude in the technical or business context. Domain drives skill selection
recommendations. Stack populates the `<context>` block in the system prompt. Enter
"none" for non-technical projects.

### Section 4 — Deliverables

The most important section for CLAUDE.md quality. The minimum-necessary rule is
the CLAUDE.md length governor: answer only what Claude must know every session to
avoid mistakes. More than five distinct points here is a signal to trim — the
challenge will flag it.

### Section 5 — Routing & Repos

Declares cross-repo dependencies and which workspace skills are active for this
project. Skills load into every session — select only those that match the domain.
`managing-tasks` should almost always be selected. Selecting all skills for a
non-technical project will be flagged as Minor in the challenge.

### Section 6 — Behaviour

Hard rules go in `<rules>` — constraints that must never be violated without
explicit confirmation. Two framework defaults are inserted automatically (never
write files without confirmation, never modify FRAMING.md). Gotchas are the
highest-signal content in CLAUDE.md: one real failure mode observed in this domain
is worth more than five generic rules. An empty gotchas field will be flagged as
Minor in the challenge.

### Section 7 — Initial Tasks

Seeds the TASKS.md backlog. Each line becomes a TASK entry. State tasks as
actions ("author FRAMING.md") not goals ("have a working pipeline"). Claude
infers the target file or component from the description — review the TASKS.md
preview and correct any TBD targets before confirming the write.

---

## 6 — Rendering surfaces

The bootstrap interview form is a React artifact. Understanding where artifacts
render and what their constraints are prevents confusion when the form behaves
unexpectedly.

| Surface | What renders | Interactive | sendPrompt() works | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Chat tab (inline) | Artifact renders embedded in conversation | Yes | Yes | Default in Claude Desktop; form submits answers to conversation |
| Artifact panel (claude.ai) | Artifact renders in right-hand pane, separate from thread | Yes | Yes | Cleanest separation from chat; not always available in Desktop layouts |
| Code tab (Claude Desktop) | Source code of the artifact only — not rendered | No | No | Display-only viewer; cannot run interactive forms |
| Standalone HTML file on disk | Full form rendered in browser, independent of Claude | Yes | No — clipboard or local endpoint instead | Durable; survives session close; requires manual answer-paste step |

`sendPrompt(text)` is a claude.ai sandbox function available inside React
artifacts. When the form's Submit button is clicked, it calls `sendPrompt()`
with the serialised answers as structured text — this fires a message into the
conversation as if the user had typed it. Claude detects the `BOOTSTRAP_ANSWERS:`
prefix and enters Phase 2.

`sendPrompt()` only works when the artifact is rendered inside the claude.ai
sandbox (Chat tab or Artifact panel). It is not available in the Code tab
(display-only) or in a standalone HTML file on disk. For the HTML file option,
the submit action copies answers to clipboard for manual paste into the Desktop
chat instead.

---

## 7 — Artifact persistence

Artifacts generated during the bootstrap session are not automatically saved
between sessions.

| Scope | What persists | Duration | Mechanism |
| :--- | :--- | :--- | :--- |
| Within a conversation | Artifact stays in the thread, referenceable | Until conversation is deleted | Conversation history |
| Across conversations | Nothing — artifacts do not carry over | Zero | None |
| storage API (`window.storage`) | Data written by the artifact (e.g. partial form answers) | Persistent across sessions | claude.ai sandbox key-value store — data only, not the rendered artifact |
| File on disk | HTML file written via Filesystem MCP | Permanent | `workspace/tools/` — opened directly in browser, no Claude session required |

The storage API can persist partial form answers between sessions — the form
could pre-fill from a previous incomplete run — but it cannot auto-launch. The
artifact must be re-rendered by Claude each session before storage data is
readable.

For a fully durable, session-independent form, the HTML file on disk is the
correct approach. `sendPrompt()` is not available from a file on disk; the
submit action uses clipboard instead.

Prompt caching (`cache_control` in the Anthropic API) is a server-side
token-reuse mechanism, not artifact storage. It has no effect on whether
artifacts persist between sessions.

---

## 8 — After bootstrapping

**Paste the system prompt**
Open Claude Desktop, create a new project, navigate to Custom Instructions, and
paste the system prompt artefact. Save.

**Verify MCP in the new project**
Open a new conversation in the new project and run the cold session bootstrap
checklist:

1. Confirm the tools icon (hammer) is visible in the chat header
2. Ask Claude: "What is the active repo and what does CLAUDE.md say?" — a correct
   answer confirms Filesystem MCP is live and routing is working
3. Confirm FRAMING.md is also read at session start — the generated CLAUDE.md
   includes a `## FRAMING.md Alignment` block that instructs Claude to read it
   on every session start and flag any out-of-scope requests
4. Ask Claude: "What workspace skills are available?" — confirms the skills path
   is reachable

**Start the first task**
Say `show tasks` — Claude reads the TASKS.md that was just written and displays
the backlog. Say `start task TASK-001` to begin.

---

## 9 — Troubleshooting

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| Skill halts at Step 1 with MCP warning | Filesystem MCP not connected | Check tools icon in chat header; verify extension is toggled on in `Customize > Connectors`; restart Claude Desktop if needed |
| Form artifact does not appear | Skill loaded but artifact render failed | Re-trigger with `bootstrap project`; if it fails again, restart Claude Desktop |
| Form submits but no challenge report appears | `sendPrompt()` fired but message not parsed as bootstrap response | Type `parse answers` — Claude will re-process the last message |
| Challenge flags a rule you disagree with | Rule is advisory (Minor) or a false positive | Type `skip` for Minor issues; type `override` with a brief reason for Major issues |
| File write fails with path error | Repo name contains spaces or special characters | The challenge should have caught this — rename in the form and resubmit, or ask Claude to regenerate with the corrected repo name |
| New project cannot find workspace skills | Skills path in generated system prompt is wrong | Verify `<skills>` block points to `/Users/gilllesmourgues/Workspace/chief-of-droids/skills/` — if it points to an old path, the template was from a stale version; fix manually in Custom Instructions |
| CLAUDE.md in new project has build commands or lint rules | Answer to Section 3 or 4 contained code tooling | The challenge should have flagged this as Major; edit CLAUDE.md directly to remove and move to a Claude Code CLAUDE.md if needed |
| Framing gate blocks on valid FRAMING.md | Gate criteria not met — re-read findings carefully | Run `fix all` to let Claude propose edits, or edit FRAMING.md directly and type `re-assess` |
| `approve framing` refused despite fixing issues | Claude carrying stale assessment state | Type `re-assess` to force a fresh disk read before typing `approve framing` again |
| Framing gate fix loop does not auto-trigger re-assess | Claude missed the auto-trigger | Type `re-assess` manually after confirming any fix write |

---

## 10 — Design decisions

Decisions made during the design and build of the `project-bootstrapping` skill.
Recorded here as the authoritative rationale.

**Artifact collects only — challenge and generation happen in conversation**

An artifact running in the claude.ai sandbox cannot call `Filesystem:write_file`
on the user's machine. The artifact and the Filesystem MCP are in different
execution contexts. Attempting to write files from inside an artifact silently
fails. This constraint is fundamental and not a workaround candidate — it is a
platform boundary. The clean separation (artifact = input collection via
`sendPrompt()`, conversation = reasoning and generation, MCP = file writes) is a
direct consequence of this constraint, not a design preference.

**Challenge step runs in conversation, not inside the artifact**

Challenging answers against best practices requires reasoning, not rendering.
If the challenge ran inside the artifact, the validation rules would need to be
baked into the artifact's API system prompt — creating a second source of truth
separate from `challenge-rules.md` in the skill's reference files. Keeping
challenge in the conversation means the rules live in one versioned file.

**FRAMING.md is artefact 1 and the binding scope definition**

FRAMING.md is generated first because CLAUDE.md references it. A CLAUDE.md
written before FRAMING.md exists has no scope anchor — every output defaults to
Claude's general judgment rather than the project's stated objectives and
constraints. The generation order (FRAMING.md → CLAUDE.md → TASKS.md → system
prompt) is not arbitrary; each file depends on the one before it.

**Framing gate sits between artefact 1 and artefact 2**

The gate is placed after FRAMING.md is written and before CLAUDE.md is generated,
not after all four artefacts, because CLAUDE.md's `## FRAMING.md Alignment`
section explicitly references FRAMING.md. Generating CLAUDE.md against a
structurally weak FRAMING.md produces a misaligned project foundation that is
harder to correct after the fact than catching the issue at the gate. The system
prompt and TASKS.md do not have the same direct dependency — they are generated
after the gate has passed.

**Skills cannot launch artifacts — they instruct Claude to render them**

Skills are instruction sets. A skill whose instructions tell Claude to render an
artifact is not a skill that "launches" an artifact — Claude generates the
artifact as a conversational action when it reads the skill's render instructions.
This distinction matters for how the SKILL.md is written: the artifact spec lives
in `SKILL.md` as instructions to Claude, not as a separate maintained artifact
file.

**Workspace skills path**

Early versions of the output template hardcoded
`/workspace/my-claude-fmk/claude-desktop/skills/` as the skills path in generated
system prompts. This was incorrect — the workspace skills library lives at
`/workspace/skills/`. The error was caught during a full skill scan (TASK-007b)
and corrected in `output-templates.md` v1.1. Any project bootstrapped before
2026-03-19 with the old path will need the `<skills>` block in its Custom
Instructions updated manually.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.2        |
| Last Updated | 2026-04-12 |
| Status       | Draft      |
