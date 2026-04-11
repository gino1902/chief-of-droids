# Context Layer Guide

> How to use system prompt, CLAUDE.md, CONSTITUTION.md, and FRAMING.md
> Version 2.3

---

## Philosophy

This architecture brings **Claude Code discipline to Claude Desktop** — routing, session
initialisation, and filesystem access made explicit — plus the visual and interactive
output layer Claude Code does not have: artifacts, diagrams, rendered documents.

Claude Code is optimised for codebases: it reads `CLAUDE.md` automatically, has native filesystem access, and operates as a terminal agent. What it does not have is a visual output layer. It produces text. Claude Desktop produces **artifacts, interactive widgets, diagrams, and rendered documents** — outputs that Claude Code cannot generate. This framework is built for knowledge work, documents, and structured deliverables where the visual and interactive output layer matters.

The framework borrows Claude Code's project discipline and reconstructs it explicitly in Claude Desktop:

| Claude Code (native) | This framework (explicit) |
|:---|:---|
| Auto-reads `CLAUDE.md` on session start | System prompt rule: read `CLAUDE.md` from the default repo |
| Built-in filesystem access | Filesystem MCP |
| Shared tools across sessions | `skills/` folder injected via MCP |
| Implicit project scope | Routing table declared in system prompt |
| Text output only | Artifacts, diagrams, interactive widgets, rendered docs |

**`skills/`** is workspace-wide infrastructure — shared across all projects, not owned by any one repo. Loaded once, available everywhere, maintained in one place.

**`CLAUDE.md` per repo** is the context anchor. The system prompt rule to read it on session start is what makes Claude Desktop behave like a project-aware agent rather than a stateless chatbot.

**The system prompt** is the bootstrap layer — it handles what Claude Code does automatically: session initialization, repo routing, tool availability, and skill injection. Because Claude Desktop has no native project-scoping, the system prompt carries the routing table explicitly.

**CONSTITUTION.md and FRAMING.md** add structured content governance — use-case rules and user intent — that Claude Code has no native equivalent for.

**The visual output layer** is what makes this worth building. Deliverables in this workspace are documents, reports, presentations, diagrams, and structured references — not code. Claude Desktop's artifact and visualization capabilities are the reason to invest in the framework overhead rather than switching to Claude Code.

The tradeoff is maintenance overhead: everything Claude Code does automatically, this framework maintains manually. The operational hygiene practices (cold session bootstrap, TASKS.md continuity, token audit cadence) exist precisely because there is no runtime enforcing them. That cost is deliberate — it keeps the framework portable and independent of any platform feature that could change.

---

## Overview

This framework uses five context layers across a multi-project architecture. Each layer has a distinct owner, scope, and authority. Getting the boundaries right is what keeps the system maintainable and outputs coherent across projects.

**Architecture model:** multiple Claude Desktop projects, each with its own system prompt and a default repo. A shared workspace skills layer is available to all projects. Routing to repos and skills is prompt-driven and MCP-dependent — not a native platform feature.

| Layer          | File / Location                  | Owner    | Scope                                                  | Changes when                                |
|:-------------- |:-------------------------------- |:-------- |:------------------------------------------------------ |:------------------------------------------- |
| Routing        | system prompt (per project)      | Operator | Which repo Claude targets by default; when to override | A new repo is added or routing rules change |
| Behaviour      | system prompt (per project)      | Operator | How Claude acts within the routed repo                 | Workflows or rules change                   |
| Defaults       | `CLAUDE.md` (per repo)           | Operator | What all outputs in that repo look like                | A new shared standard is needed             |
| Use-case rules | `CONSTITUTION.md` (per use-case) | Operator | What a specific use-case requires                      | Use-case goals or constraints change        |
| Intent         | `FRAMING.md` (per use-case)      | User     | Why the use-case exists                                | User intent changes                         |

```mermaid
flowchart 
    subgraph claude["support.claude.ai"]
        source[("Official docs")]
    end
    subgraph shared["Shared Repository"]
        direction LR
        context["Context 
        generation"]
        skill["skills/"]
        docs["docs/"]
        context --> |generate new system prompt|skill 
        docs --> |format output| skill 
    end
    subgraph cd["Claude Desktop"]
        subgraph P1["Project: slide-gen"]
            SP1[System prompt
            default → slide-gen/] --> UP1[User prompt]
        end
        subgraph P2["Project: my-claude-fmk"]
            SP2[System prompt
            default → my-claude-fmk/] --> UP2[User prompt]
        end    
        subgraph P3["Project: name"]
            SP3[System prompt
            default → repo-3/] --> UP3[User prompt]
        end
    end
    subgraph repos["Projects Repository"]
        R1[slide-gen/
        CLAUDE.md
        CONSTITUTION.md]
        R2[my-claude-fmk/
        CLAUDE.md]
        R3[name/
        CLAUDE.md]
    end
    source --> |update|skill
    skill -.-o|injected| P1
    skill -.-o|injected| P2
    skill -.-o|injected| P3
    UP1 -->|default| R1
    UP1 -.->|override| R2
    UP2 -->|default| R2
    UP2 -.->|override| R1
    UP3 -->|default| R3
    UP3 -.->|override| R1
    UP3 -.->|override| R2
```

---

## Layer 0 — Workspace Skills

**What it governs:** reusable instruction sets shared across all projects. Skills are loaded into each project via explicit system prompt instructions + Filesystem MCP reads.

**What it does not govern:** routing, repo-specific defaults, or use-case rules.

**Key principle:** skills are workspace-wide infrastructure, not owned by any one project or repo. A skill that only makes sense for one repo belongs in that repo, not the shared workspace.

**What belongs here:** any skill that is reusable across two or more repos without modification — doc-writer, tech-reviewer, business-analyst, skill-creator.

**Maintenance note:** skills load only if (a) the system prompt instructs Claude to look for them and (b) the Filesystem MCP is connected. If MCP is disconnected, skills are silently unavailable — no error is raised.

---

## Layer 1 — System Prompt (per project)

**What it governs:** two things — routing and behaviour.

*Routing:* declares the default repo for this project and the rules for overriding to another repo. This is a prompt engineering convention, not a platform feature. Claude follows the declared paths via Filesystem MCP reads.

*Behaviour:* how Claude acts once routed — how it reads files, when it writes, what triggers a workflow, what it never does without confirmation.

**What it does not govern:** the content or format of any deliverable.

**Key principle:** system prompts should be clear and use simple, direct language at the right altitude — specific enough to guide behaviour effectively, yet flexible enough to provide strong heuristics rather than brittle hardcoded logic.

**What the system prompt defines:**

- Default repo path and override rules (routing)
- Workspace skills paths to load
- Roles and persona
- Workflow triggers and steps
- File write rules (never write without confirmation, never modify FRAMING.md)
- Defaults for tone and output style (concise, no preamble, act directly)

**What does not belong here:**

- Output format rules (version blocks, default file type) → `CLAUDE.md`
- Use-case-specific content rules → `CONSTITUTION.md`
- Project intent or goals → `FRAMING.md`
- Repo-specific content of any kind — keep system prompts generic across repos

**Maintenance note:** the system prompt is the most expensive layer to change — it governs all conversations in the project. Run a token audit (see `prompt-maintenance.md`) whenever routing rules or workflows change. Add a new repo to the routing table when a new repo is added to the workspace.

---

## Layer 2 — CLAUDE.md (per repo)

**What it governs:** shared defaults that apply to every output across every use-case in that repo, unless overridden by a CONSTITUTION.md.

**What it does not govern:** anything specific to one use-case, or routing between repos.

**Key principle:** CLAUDE.md is the repo's baseline contract. It answers: "if CONSTITUTION.md says nothing about X, what do we do?" Each repo has its own CLAUDE.md — defaults are not shared across repos.

**What belongs here:** output format standards, tone, language, structural conventions, and any rule that applies to every use-case in this repo without exception.

**What does not belong here:**

- Anything that only applies to one use-case → `CONSTITUTION.md`
- Project goals or problems → `FRAMING.md`
- Rules specific to another repo → that repo's `CLAUDE.md`

**Maintenance note:** Before adding anything to CLAUDE.md, ask: "does this apply to every use-case in this repo?" If not, it belongs in CONSTITUTION.md. If it would apply identically across all repos, consider whether it belongs in a workspace skill instead.

---

## Layer 3 — CONSTITUTION.md (per use-case)

**What it governs:** the rules that make a specific use-case's outputs valid and in-scope.

**What it does not govern:** how Claude behaves (system prompt), what format outputs take (CLAUDE.md), or rules from another repo.

**Key principle:** CONSTITUTION.md overrides CLAUDE.md. It is the highest-authority document on content — but only for its own use-case within its own repo. It is derived from FRAMING.md and must stay aligned with it.

**Cross-repo note:** when an explicit override routes Claude to another repo, the target repo's CLAUDE.md and CONSTITUTION.md apply — not the originating project's. The originating system prompt governs behaviour only; content rules follow the routed repo.

**What belongs here:** root problem alignment, objective scope, mandatory outcome linkage, output quality criteria — anything that is specific to this use-case and would not be valid word-for-word in another use-case.

**What does not belong here:**

- Generic output format rules → `CLAUDE.md`
- Flagging and version block mechanics → `CLAUDE.md`
- Project intent in the user's own words → `FRAMING.md`

**Maintenance note:** run `revise constitution <use-case-id>` whenever FRAMING.md changes. Never edit CONSTITUTION.md directly without first reading FRAMING.md. Flag any conflict between the two before writing.

---

## Layer 4 — FRAMING.md

**What it governs:** the authoritative statement of why this use-case exists — problems, objectives, expected improvements.

**What it does not govern:** anything about how Claude operates or what outputs look like.

**Key principle:** FRAMING.md is user-owned and immutable by Claude. It is the source of truth that all other layers derive from. Every claim in CONSTITUTION.md must be traceable here.

**What belongs here:**

- The root problems the use-case addresses
- The primary and secondary objectives
- The expected improvements or success criteria
- Any non-goals or explicit scope exclusions

**What does not belong here:**

- Output rules of any kind
- Workflow instructions
- Anything Claude should enforce — that goes in CONSTITUTION.md

**Maintenance note:** Only the user edits FRAMING.md. If Claude identifies a conflict between FRAMING.md and CONSTITUTION.md, it flags it and proposes a constitution revision — it never proposes a change to FRAMING.md.

---

## Precedence Chains

The layers govern two distinct axes. Conflating them is the source of most precedence confusion.

### Content authority — which layer's content rules win

When content rules conflict, the higher layer in this chain wins:

```
CONSTITUTION.md     ← highest content authority (use-case scope)
    ↓ overrides
CLAUDE.md           ← repo defaults (all use-cases in this repo)
    ↓ overrides
system prompt       ← tone/style defaults declared in <defaults>
```

### Derivation — which layer is the source of truth

Content rules must be traceable upward through this chain:

```
FRAMING.md          ← source of truth (user intent, immutable)
    ↓ derived from
CONSTITUTION.md     ← use-case rules (must align with FRAMING.md)
```

CLAUDE.md has no derivation relationship with FRAMING.md or CONSTITUTION.md. It is set independently as the repo-wide baseline and appears only in the content authority chain above, not here.

### System prompt — a separate axis

The system prompt governs **routing and behaviour**, not content. Its rules sit on a different axis from the content chain and are not overridden by any content layer:

- Behavioural rules (e.g. "never write without confirmation", "never modify FRAMING.md") apply regardless of what any content layer says.
- Routing rules (default repo, override conditions) are resolved before content layers are consulted — they determine *which* CLAUDE.md and CONSTITUTION.md apply.
- Tone and style defaults in `<defaults>` are the one overlap: they can be overridden by CLAUDE.md or CONSTITUTION.md, which is intentional.

### Workspace skills — injected, not authoritative

Skills are loaded into context by the system prompt via MCP. They provide expertise and workflow instructions but carry no authority over content rules — they operate within whatever CONSTITUTION.md and CLAUDE.md define.

---

## Decision Guide — Where Does This Belong?

| Question                                                         | Layer                     |
|:---------------------------------------------------------------- |:------------------------- |
| Which repo does this project target by default?                  | System prompt (routing)   |
| When should Claude override to another repo?                     | System prompt (routing)   |
| How should Claude respond when a trigger fires?                  | System prompt (behaviour) |
| What files can Claude write, and when?                           | System prompt (behaviour) |
| Is this skill reusable across multiple repos?                    | Workspace skills          |
| What should every output in this repo contain?                   | CLAUDE.md (that repo)     |
| What tone and structure apply across all use-cases in this repo? | CLAUDE.md (that repo)     |
| What problems must this use-case's outputs address?              | CONSTITUTION.md           |
| What objectives must outputs serve?                              | CONSTITUTION.md           |
| What does the user need and why?                                 | FRAMING.md                |
| What improvements is the user trying to achieve?                 | FRAMING.md                |

---

## Lessons Learned

**Lesson 1 — CONSTITUTION scope creep** (slide-gen, use-case-1)

CONSTITUTION.md accumulated generic output rules (default .md format, version block structure, flagging conventions) that had nothing to do with the use-case's specific goals. Fix: generic output standards moved to CLAUDE.md, CONSTITUTION.md scoped to use-case content only.

Rule derived: if a rule in CONSTITUTION.md would be valid word-for-word in any other use-case in the same repo, it belongs in CLAUDE.md.

**Lesson 2 — Routing is not automatic** (framework-level)

Default repo routing only works when (a) the system prompt contains explicit path declarations and (b) the Filesystem MCP is connected. If MCP is disconnected, Claude cannot reach any repo and will not raise an error — it will silently fall back to its training knowledge. Always verify MCP connection at session start.

**Lesson 3 — Cross-repo content rules do not travel** (framework-level)

When Claude is routed to another repo via an explicit override, the originating project's CLAUDE.md does not apply to that repo's outputs. The target repo's own CLAUDE.md governs. Do not put cross-repo content expectations in the system prompt — they belong in each repo's CLAUDE.md.

---

## Authoring a New Use-Case

1. User writes `FRAMING.md` — problems, objectives, expected improvements
2. Trigger `revise constitution <use-case-id>` — Claude reads FRAMING.md and generates a scoped CONSTITUTION.md
3. Claude flags any gap or conflict between the two before writing
4. CLAUDE.md requires no changes unless a new shared default is needed
5. System prompt requires no changes unless a new workflow or routing rule is needed

## Adding a New Repo to the Workspace

1. Create the repo with a `CLAUDE.md` defining its output defaults
2. Add the repo path to the routing table in each project's system prompt that needs to reach it
3. Run a token audit on each updated system prompt (see `prompt-maintenance.md`)
4. Verify Filesystem MCP has read/write access to the new repo path
5. Test routing with a dry-run prompt before committing the system prompt change

---

*Cross-reference: `prompt-maintenance.md` for token audit methodology. Each repo's `CLAUDE.md` for repo-level defaults.*

---

| Field        | Value      |
|:------------ |:---------- |
| Version      | 2.3        |
| Last Updated | 2026-03-26 |
| Status       | Final      |

*v2.3 — Layer 4 FRAMING.md section: slide-gen use-case content removed; replaced with generic field descriptions. Derivation chain: CLAUDE.md removed — it has no derivation relationship with FRAMING.md or CONSTITUTION.md; clarifying note added.*
