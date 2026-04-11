# Skills Playbook

> How to commission, build, describe, install, and maintain skills.
> Procedural. Follow this when executing a task.

**Companion doc:** `skills-reference.md` — SKILL.md spec, frontmatter fields, install prerequisites, platform comparison, templates, packaging checklist, troubleshooting, verified claims log.
Go there when you need to look something up. Stay here when you are doing something.

---

## Contents

1. Commission — the proposal interview
2. Choose — archetypes
3. Describe — making skills trigger reliably
4. Build — the skill loop
5. Install, update, commit
6. Filesystem skills via MCP (Claude Desktop)
7. Maintain — the persistence model
8. Quick reference

---

## 1. Commission — The Proposal Interview

When starting a new project, run the proposal interview before building anything. It produces a prioritised skill backlog grounded in your actual workflow gaps — not generic proposals.

### Prerequisites

The project must have both:

- `FRAMING.md` — including the **strategic deliverable**: what gets produced, for whom, for what purpose
- `CONSTITUTION.md` — including the **operational deliverable spec**: format, quality constraints, export requirements

> ⚠️ If `FRAMING.md` does not include a strategic deliverable statement, add one first. The interview output is not useful without it.

### Trigger

In your Claude project, after syncing your repo:

```
Read FRAMING.md and CONSTITUTION.md. Then run the skill-proposal
interview to help me identify which skills to build for this project.
```

### What Claude does

1. Reads `FRAMING.md` — understands strategic intent and deliverable type
2. Reads `CONSTITUTION.md` — understands quality bar and operational constraints
3. Asks 3–4 targeted questions
4. Proposes a prioritised skill backlog with rationale

### The four interview questions

| # | Question | What it surfaces |
| :--- | :--- | :--- |
| 1 | What tasks do you do manually on every generation? | Repetitive steps that belong in a skill |
| 2 | Where do deliverables most often come back with corrections? | Quality failure modes |
| 3 | What is the most common way a generated output misses the mark? | Alignment gaps — tone, structure, audience |
| 4 | Are there technical standards or conventions outputs must meet? | Compliance and consistency rules |

### What a good proposal looks like

| Priority | Skill | Trigger | Prevents |
| :---: | :--- | :--- | :--- |
| 1 | `framing-alignment` | Before any generation | Content contradicting FRAMING objectives |
| 2 | `slide-density-qa` | After generation | Slides too dense for the audience |
| 3 | `ba-requirements` | When writing requirements | Incomplete or untestable requirements |
| 4 | `financial-narrative` | Slides or docs with numbers | Inconsistent figures, unsupported claims |

Build the highest-priority skill first. One well-built skill beats three half-built ones.

---

## 2. Choose — Archetypes

Common skill types across projects. Use as starting points, not blueprints — build from your specific workflow gaps.

### BA — Business Analyst

Ensures requirements, objectives, and problem statements are complete, unambiguous, and testable.

**Build it when:** Deliverables regularly come back with "this isn't specific enough" or "how will we measure this."

**Typical trigger phrases:** "Review this requirements section" / "Check if these objectives are measurable" / "Flag assumptions in this document"

---

### UI Reviewer

Evaluates UI descriptions, mockup notes, or slide layouts against a defined visual and UX standard.

**Build it when:** Generated slides or documents have visual quality issues that repeat across generations.

**Typical trigger phrases:** "Review this slide layout" / "Check this against our design standards" / "Flag design principle violations"

---

### Coder

Applies your coding standards to generated or reviewed code — naming conventions, error handling, structure, documentation.

**Build it when:** Code generated with Claude regularly needs manual cleanup before it is usable.

**Typical trigger phrases:** "Review this script against our standards" / "Generate following our conventions" / "Check for error handling gaps"

Note: `technical-verification` (if already built) covers factual accuracy of technical documentation — it is not a substitute for a coding standards skill.

---

### QA — Quality Assurance

QA skills come in focused variants. Build the one that addresses your most frequent failure first.

| Skill | What it does | When it triggers |
| :--- | :--- | :--- |
| `technical-verification` | Verifies commands, package names, API parameters, UI paths against official docs | Before any technical output |
| `unit-test` | Generates or reviews unit tests for coverage, edge cases, meaningful assertions | When writing or reviewing test files |
| `framing-alignment` | Checks every section against FRAMING.md objectives, audience, deliverable | Before finalising any generation |
| `slide-density-qa` | Checks slides for text density, claim support, audience fit | After generation, before sharing |
| `financial-narrative` | Checks numbers and projections for consistency, sourcing, caveats | Slides or docs with financial content |

---

## 3. Describe — Making Skills Trigger Reliably

The `description` field is the trigger mechanism. Claude scans all enabled skill descriptions at query time and semantically matches them to the request. It reasons about intent — it does not do keyword matching.

**The default failure mode is under-triggering.** Claude errs on the side of not loading a skill when uncertain. A vague description means the skill is effectively invisible.

### Rules for descriptions that trigger reliably

1. State what the skill does AND the specific conditions under which it applies
2. Include 2–3 example trigger phrases drawn from your real prompts
3. Add negative examples when scope overlaps with another skill: *"NOT for X — use [skill-name] instead"*
4. Keep to 200 characters maximum (safe cross-surface limit — see `skills-reference.md`)
5. Write the description last — after you have written and tested the instructions
6. Be specific enough that Claude can distinguish this skill from adjacent ones

### Weak vs. strong — example

```
# Weak — will under-trigger
description: Helps with requirements and analysis work.

# Strong — triggers reliably
description: >
  Review requirements documents for completeness, ambiguity, and
  testability. Use when asked to review requirements, check objectives,
  or flag assumptions. NOT for general document formatting.
```

### Testing a description

Before committing a skill:

- Run 3–5 real prompts you expect to trigger the skill → all should load it
- Run 2–3 prompts you expect NOT to trigger it → none should load it
- If false negatives: add more trigger phrases or make existing ones more specific
- If false positives: add exclusions ("NOT for...")

### Disabling auto-trigger (Claude Code only)

Add `disable-model-invocation: true` to SKILL.md frontmatter. The skill then only activates via `/skill-name`. Use for sensitive or destructive operations you always want to invoke explicitly.

> ✅ Description-as-trigger-mechanism, disable-model-invocation: docs.claude.com, support.claude.com (2026-03-13)

---

## 4. Build — The Skill Loop

Iteration is expected. The first version is a hypothesis. The description is usually the bottleneck — write it last and refine it most.

For SKILL.md structure, frontmatter field rules, and worked templates: see `skills-reference.md` → Sections 2 and 6.

### The loop

1. **Identify the gap** — from the proposal interview or from a real failure in a recent session
2. **Draft `SKILL.md`** — name, description placeholder, instructions body
3. **Test on real prompts** — 3–5 prompts from your actual workflow; does it change behaviour in the right direction?
4. **Test non-triggers** — 2–3 prompts that should NOT load the skill; does it stay silent?
5. **Refine the description** — apply the rules in Section 3; iterate until triggering is reliable
6. **Refine the instructions** — tighten steps, add examples, move large reference content to `references/`
7. **Install** — see Section 5
8. **Test in a live conversation** — verify end-to-end in the actual Claude Desktop / claude.ai context
9. **Commit** — see Section 5

### When to split content into references/

Move content from `SKILL.md` body to `references/` when:

- Body approaches 500 lines
- Content is looked up conditionally (e.g. domain-specific templates)
- Content changes at a different cadence than the instructions

Reference files are loaded on demand — they do not consume context on every invocation.

### Asking Claude to run the skill-creator workflow

For a guided build loop including description optimisation and scoring:

```
Run the skill-creator workflow to help me build a [skill name] skill.
```

Claude will walk through: intent capture → interview → draft → test → evaluate → refine.

---

## 5. Install, Update, Commit

### Install (claude.ai and Claude Desktop)

1. ZIP the skill folder — root of ZIP must be the skill folder, not loose files
2. **Customize > Skills** → **"+"** → **"Upload a skill"** → upload ZIP
3. Toggle on

For full prerequisites and troubleshooting: see `skills-reference.md` → Section 3.

### Install (Claude Code)

Place the skill folder at `~/.claude/skills/your-skill/` (personal) or `.claude/skills/your-skill/` (project). No upload required — Claude Code discovers it automatically.

### Update (claude.ai and Claude Desktop)

Skills cannot be edited in place:

1. Edit `SKILL.md` in your local source folder
2. Re-ZIP the folder
3. **Customize > Skills** → click skill → "..." → Delete
4. Upload new ZIP → toggle on
5. Commit updated source (see below)

### Commit to your repo

```bash
# Commit the source folder — not the ZIP
git add claude-desktop/skills/your-skill-name/
git commit -m "skills: add/update your-skill-name — [one-line reason]"
git push origin main
```

**Recommended source structure:**

```
my-claude-fmk/
└── claude-desktop/
    └── skills/
        ├── your-skill/
        │   └── SKILL.md
        └── another-skill/
            ├── SKILL.md
            └── references/
                └── checklist.md
```

> ✅ Install path verified: support.claude.com (2026-03-13)
> ⚠️ Old path "Settings → Extensions → Install Extension" + .skill file is stale — do not use

---

## 6. Filesystem Skills via MCP (Claude Desktop)

Uploaded skills (ZIP → Customize > Skills) are not the only delivery mechanism for Claude Desktop. If the Filesystem MCP is connected, Claude can load skills directly from the repo — no upload, no ZIP, no toggle.

This is the pattern used in this workspace: skill source files live in `my-claude-fmk/claude-desktop/skills/` and the system prompt instructs Claude to read them from that path.

### How it works

The system prompt declares a skills path. When Claude starts a session, it reads the SKILL.md files from that directory into context on demand — matching them to your requests the same way uploaded skills work, but sourcing them from the filesystem instead of the installed skills store.

Minimal system prompt snippet:

```xml
<skills>
Load workspace skills from: /home/[wsl-user]/workspace/my-claude-fmk/claude-desktop/skills/
For each subdirectory, read SKILL.md and treat it as an available skill.
Fallback if path is unavailable: notify the user, then proceed without skills.
</skills>
```

**What "loading" means here:** Claude reads the SKILL.md file content into the active context window when it determines the skill is relevant. This is functionally equivalent to uploaded skills — same progressive disclosure model, same description-driven triggering — but the source is the filesystem, not the installed skills store.

### Uploaded skills vs. filesystem skills — when to use which

| | Uploaded skills (ZIP) | Filesystem skills (MCP) |
| :--- | :--- | :--- |
| **MCP dependency** | None — always available | Requires Filesystem MCP connected |
| **Update workflow** | Delete → re-ZIP → re-upload | Edit SKILL.md in repo → done |
| **Persistence** | Survives session reset, reinstall risk | Lives in git — most durable |
| **Sharing** | Per-user only (standard plans) | Shared via git — anyone who clones the repo gets them |
| **Scope** | Available in all projects for that user | Available in projects where the system prompt declares the path |
| **Best for** | Skills with no MCP dependency requirement; stable skills you rarely edit | Skills under active development; skills shared across team via git |

### Failure mode

If the Filesystem MCP disconnects, filesystem skills silently vanish — Claude cannot reach the path and will not automatically flag the gap in conversation. The system prompt snippet above includes an explicit fallback instruction (`notify the user`) to surface this.

Verify MCP is live at session start:
- Tools icon (hammer) visible in the Claude Desktop chat header
- Ask Claude: *"What skills are available from the workspace skills path?"* — a correct answer confirms MCP and path are reachable

### Maintenance advantage

Filesystem skills have no upload cycle. Edit the SKILL.md in your editor, save, and the next conversation picks up the change automatically. Git history is the version log. No stale uploaded version to chase down.

```bash
# Edit skill, then commit
git add claude-desktop/skills/your-skill/SKILL.md
git commit -m "skills: update your-skill — [reason]"
git push origin main
# Next Claude Desktop session: change is live
```

> ⚠️ Filesystem skills and uploaded skills are independent. Having a skill in both places does not cause a conflict — Claude may load both descriptions. If both are toggled on, keep their descriptions identical to avoid drift.

---

## 7. Maintain — The Persistence Model

Four layers. Know which one you are working in before acting.

```
Claude's container (ephemeral)
│  Resets after every session. Where Claude drafts SKILL.md content.
│  Nothing here survives unless you explicitly save it.
│
↓ Download / copy to local
│
Your Windows filesystem (durable)
│  Your repo working tree, Downloads folder.
│  Survives session resets. Your ownership layer.
│  Nothing is safe until it is here.
│
↓ ZIP + upload via Customize > Skills
│
Claude Desktop / claude.ai skills (persistent, per-user)
│  Toggled-on skills auto-load in every conversation.
│  Survives session resets.
│  Does NOT survive Claude Desktop reinstall — re-upload ZIPs after reinstall.
│  Private to your account — not shared org-wide.
│
↓ git commit + push
│
GitHub repo (most durable)
└─ Version-controlled source of truth.
   Survives reinstalls, new machines, team sharing.
   Commit the source folder, not the ZIP.
```

**Rule:** The upload activates the skill. The commit preserves it. Nothing is permanent until it is committed.

**MCP and skills are independent.** Skills uploaded via Customize > Skills remain available whether or not MCP is connected. Workspace skills loaded from the filesystem via system prompt instructions require MCP — if MCP is disconnected they are silently unavailable. Claude Desktop may surface a connection error toast, but not always. Verify MCP connection with the tools icon in the chat header.

> ✅ Per-user scope, no cross-session data persistence: support.claude.com (2026-03-13)
> ✅ MCP silent failure behaviour: GitHub issues #31864, #25751 (2026-03-13)

---

## 8. Quick Reference

| Task | Where |
| :--- | :--- |
| Upload a new skill | **Customize > Skills** → "+" → Upload a skill |
| Toggle skill on/off | **Customize > Skills** → toggle |
| Delete a skill | **Customize > Skills** → click skill → "..." → Delete |
| Update a skill | Delete old → re-ZIP source → upload new |
| Commit to repo | `git add skills/your-skill/` → commit → push |
| Run proposal interview | See Section 1 — requires FRAMING.md + CONSTITUTION.md |
| Build a new skill | Section 4, or ask Claude to run the skill-creator workflow |
| Filesystem skills via MCP | Section 6 |
| SKILL.md spec and templates | `skills-reference.md` |
| Troubleshooting | `skills-reference.md` → Section 8 |

---

*See `skills-reference.md` for: SKILL.md spec, frontmatter fields, install prerequisites, platform comparison, templates, packaging checklist, troubleshooting, verified claims log.*

---

| Field | Value |
| :--- | :--- |
| Version | 1.1 |
| Last Updated | 2026-03-26 |
| Status | Final |

*v1.0 — Restructured from skills-usage-guide.md (v2.0) and skills-guide.md (v1.0). Reorganised as playbook — procedural content only. Section order follows task execution sequence: commission → choose → describe → build → install → maintain. Description discipline elevated to standalone section (Section 3). Persistence model updated. SKILL.md anatomy removed — cross-reference to skills-reference.md. Companion doc header added.*
*v1.1 — Version block bumped to reflect substantive changes made in prior session: Section 5 install paths updated (Customize > Skills); Section 6 workspace MCP pattern documented as primary delivery model for this workspace.*
