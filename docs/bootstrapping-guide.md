# Bootstrapping a New Claude Desktop Project

> How to use the `project-bootstrapping` skill to scaffold a new project
> from scratch — system prompt, CLAUDE.md, and TASKS.md — in a single guided session.

---

## 1 — What bootstrapping does

The `project-bootstrapping` skill creates three artefacts for a new Claude Desktop
project: a system prompt ready to paste into Custom Instructions, a `CLAUDE.md`
defining repo output defaults, and a `TASKS.md` seeding the initial backlog.
It does this through a structured interview, a best-practice challenge pass, and
a confirmed filesystem write — all within a single session.

---

## 2 — Prerequisites

Before triggering the bootstrapper:

- You must be working inside the **Chief of Droids** Claude Desktop project.
  The bootstrapper reads workspace skills and writes to the filesystem via the
  Filesystem MCP, which is configured in that project. Running it from any other
  project will fail silently at Step 1 if MCP is not connected.
- Filesystem MCP must be connected — verify the tools icon (hammer) is visible
  in the Claude Desktop chat header before starting.
- Have a rough idea of: what the new project is for, what it produces, and what
  the first 3–5 tasks are. You do not need to have the details worked out — the
  interview will surface them.

---

## 3 — How it works

The skill runs in three sequential phases. Each phase has one job.

**Phase 1 — Collect**
Claude renders a multi-section form as an interactive artifact. You fill in the
answers — project identity, domain and stack, deliverable type, routing needs,
behaviour rules, and initial tasks. On submit, the form sends your answers back
to the conversation as structured text.

**Phase 2 — Challenge**
Claude reads the answers and runs a set of best-practice checks against them.
Issues are reported as Major (must fix before generation) or Minor (advisory —
you can proceed or adjust). The challenge covers CLAUDE.md scope, system prompt
rule completeness, workflow definition quality, and task actionability. You
respond: fix the issues, skip them, or override.

**Phase 3 — Generate**
Claude substitutes your answers into the output templates and renders three
artefacts in sequence: the system prompt as a copy-ready XML block, a CLAUDE.md
preview, and a TASKS.md preview. You review them, then confirm a single file
write. Claude creates the new repo directory and writes CLAUDE.md and TASKS.md.
The system prompt is copy-paste only — there is no file target for it.

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

The form artifact appears with six sections. Work through them in order. Every
required field is marked. Use the Back button if you want to revise a section
before submitting. When all required fields are filled, click Submit.

The form sends your answers to the conversation — do not close it while Claude
is processing.

**Step 3 — Review the challenge report**

Claude outputs a challenge table. For each issue:

- **Major** — Claude pauses and waits. Either amend the answer inline ("change
  Q13 to include never-modify-FRAMING.md") or type `override` to proceed anyway.
- **Minor** — Claude notes the recommendation. Type `fix` to apply it or `skip`
  to proceed.

If there are no issues, Claude states this and proceeds automatically.

**Step 4 — Review the generated artefacts**

Three artefacts appear in sequence — system prompt, CLAUDE.md, TASKS.md. Read
each one. If anything needs adjusting, say so now before the file write. Claude
will regenerate the affected artefact with your correction.

**Step 5 — Confirm the file write**

Claude proposes:

```
Will write:
  workspace/<repo-name>/CLAUDE.md
  workspace/<repo-name>/TASKS.md
Confirm? (yes / no)
```

Type `yes`. Claude creates the directory, writes both files, and confirms each
write with path and status.

**Step 6 — Copy the system prompt**

Copy the system prompt artefact. In Claude Desktop, create a new project, open
Custom Instructions, and paste it in. The new project is ready for its first
session.

---

## 5 — The interview questions explained

### Section 1 — Identity

Sets the repo name, project name, and one-sentence purpose. The repo name becomes
the filesystem directory — it must be lowercase with hyphens only. The purpose
maps directly to the `<role>` block in the system prompt. A good purpose follows
the pattern: "produces/enables [specific output] for [audience or context]."
Vague purposes ("helps with things") will be flagged in the challenge.

### Section 2 — Domain & Stack

Grounds Claude in the technical or business context of the project. The domain
drives skill selection recommendations in the challenge. The stack populates the
`<context>` block. If the project is non-technical, enter "none" for stack —
leave it blank and the template inserts a sensible default.

### Section 3 — Deliverables

The most important section for CLAUDE.md quality. The output type and format
defaults set what Claude produces by default. The quality bar defines the
acceptance standard — be specific about audience and format expectations, not
generic ("professional quality"). The minimum-necessary rule is the CLAUDE.md
length governor: answer only what Claude must know every session to avoid
mistakes. More than five distinct points here is a signal to trim.

### Section 4 — Routing & Repos

Declares whether this project ever needs to reach other repos in the workspace
and which workspace skills are relevant. Skills are loaded into every session —
select only the ones that genuinely match the domain and output type.
`managing-tasks` should almost always be selected. Selecting all six skills for
a non-technical project will be flagged as Minor in the challenge.

### Section 5 — Behaviour

Hard rules go in `<rules>` — constraints that must never be violated without
explicit confirmation. The two framework defaults (never write files without
confirmation, never modify FRAMING.md) are inserted automatically; anything you
add here is project-specific. Tone shapes the `<defaults>` block and the
CLAUDE.md tone section — be specific across at least two dimensions (e.g.
"direct and technical, no filler"). Gotchas are the highest-signal content in
CLAUDE.md: one real failure mode you have observed or expect in this domain is
worth more than five generic rules. Workflows are optional at bootstrap time —
add them after the first few sessions once patterns emerge.

### Section 6 — Initial Tasks

Seeds the TASKS.md backlog. Each line becomes a TASK entry. State tasks as
actions ("author FRAMING.md") not goals ("have a working pipeline"). Claude
infers the target file or component from the description — review the TASKS.md
preview and correct any `TBD` targets before confirming the write.

---

## 6 — After bootstrapping

**Paste the system prompt**
Open Claude Desktop, create a new project, navigate to Custom Instructions, and
paste the system prompt artefact. Save.

**Verify MCP in the new project**
Open a new conversation in the new project and run the cold session bootstrap
checklist (see `my-claude-fmk/claude-desktop/playbook/claude-project-playbook.md`
Section 12):

1. Confirm the tools icon (hammer) is visible in the chat header
2. Ask Claude: "What is the active repo and what does CLAUDE.md say?" — a correct
   answer confirms Filesystem MCP is live and routing is working
3. Ask Claude: "What workspace skills are available?" — confirms the skills path
   is reachable

**Start the first task**
In the new project, say `show tasks` — Claude reads the TASKS.md that was just
written and displays the backlog. Say `start task TASK-001` to begin.

---

## 7 — Troubleshooting

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| Skill halts at Step 1 with MCP warning | Filesystem MCP not connected | Check tools icon in chat header; verify extension is toggled on in `Customize > Connectors`; restart Claude Desktop if needed |
| Form artifact does not appear | Skill loaded but artifact render failed | Re-trigger with `bootstrap project`; if it fails again, restart Claude Desktop |
| Form submits but no challenge report appears | `sendPrompt()` fired but message not parsed as bootstrap response | Type `parse answers` — Claude will re-process the last message |
| Challenge flags a rule you disagree with | Rule is advisory (Minor) or a false positive | Type `skip` for Minor issues; type `override` with a brief reason for Major issues |
| File write fails with path error | Repo name contains spaces or special characters | The challenge should have caught this — rename in the form and resubmit, or ask Claude to regenerate with corrected repo name |
| New project cannot find workspace skills | Skills path in generated system prompt is wrong | Verify `<skills>` block points to `/home/gino/workspace/skills/` — if it points to `my-claude-fmk/claude-desktop/skills/` the template was from a stale version; fix manually in Custom Instructions |
| CLAUDE.md in new project has build commands or lint rules | Answer to Q9 or Q10 contained code tooling | The challenge should have flagged this as Major; edit CLAUDE.md directly to remove and move to a Claude Code CLAUDE.md if needed |

---

## 8 — Design decisions

Decisions made during the design and build of the `project-bootstrapping` skill
(session 2026-03-19). Recorded here as the authoritative rationale.

**Artifact collects only — challenge and generation happen in conversation**

An artifact running in the Claude.ai sandbox cannot call `Filesystem:write_file`
on the user's machine. The artifact and the Filesystem MCP are in different
execution contexts. Attempting to write files from inside an artifact silently
fails. This constraint is fundamental and not a workaround candidate — it is a
platform boundary. The clean separation (artifact = input, conversation =
reasoning, MCP = writes) is a direct consequence of this constraint, not a
design preference.

**Challenge step runs in conversation, not inside the artifact**

Challenging answers against best practices requires reasoning, not rendering.
If the challenge ran inside the artifact, the validation rules would need to be
baked into the artifact's API system prompt — creating a second source of truth
separate from `challenge-rules.md` in the skill's reference files. Any update
to the challenge rules would require updating both places. Keeping challenge in
the conversation means the rules live in one versioned file.

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
`/workspace/skills/`. The error was caught during a full skill scan and corrected
in `output-templates.md` v1.1. Any project bootstrapped before 2026-03-19 with
the old path will need the `<skills>` block in its Custom Instructions updated
manually.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-03-19 |
| Status       | Draft      |
