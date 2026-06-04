# Two-Tier CLAUDE.md Architecture — Design Notes

## Context

chief-of-droids is a model-in-the-loop framework operating in Claude Desktop chat. Claude Desktop chat does not natively expose the CLAUDE.md hierarchy, skill routing, session lifecycle, or other platform behaviors that Claude Code provides.

The current setup carries duplications between Project Instructions (system prompt) and workspace CLAUDE.md — preamble rules, citation enforcement, skill loading procedure, override language, and maintenance section all appear in both layers — plus category errors (Code-style override semantics declared in a Chat environment where no native override mechanism exists). This document proposes a two-tier architecture that resolves both.

Status: design notes, not committed spec.
Companion to `docs/session-identity-recommendation.md`.

## Requirements framing

The design mirrors Claude Code by using a CLAUDE.md at the `<project>` level. The project-level CLAUDE.md must handle:

**Standard CLAUDE.md features**

- Project conventions (tone, format, naming, version blocks)
- Project rules and constraints
- Project-specific defaults

**Capabilities Claude Code provides natively that chief-of-droids must implement via instruction**

| Capability | Claude Code native mechanism | chief-of-droids implementation locus |
|---|---|---|
| Skills routing | SKILL.md description scanned at startup, prompt matched at runtime | Two-tier skill manifest (workspace + project), precedence rule, sentinel resolution map |
| Session hygiene | `/compact`, native session lifecycle, CLAUDE.md re-injection from disk | Sentinel-based session binding via `recent_chats[0].uri` |
| Git versioning | Tool-level git awareness; status-aware operations | Explicit git protocol declared in project CLAUDE.md; pre-approved writes for specific skills |
| Available tools | MCP registry built from desktop config at client startup | Always-on tools at workspace level (filesystem, git, fetch); project-specific tools at project level |
| Project brief route | `/init` command and project root auto-detection | Bootstrap dispatcher asks for project at session start; loads project brief alongside CLAUDE.md at bind |
| Conditional rules by file type | `.claude/rules/` with `paths:` frontmatter; on-demand load when matching files are read | Path-scoped rule files at project level; dispatcher loads on filesystem read |

## Architecture — two tiers, three layers

| Layer | Slot | Carries |
|---|---|---|
| Layer 1 — Dispatcher | Claude Desktop Project Instructions | Bootstrap protocol; per-turn sentinel verification; always-on tool routing |
| Layer 2 — Workspace | `chief-of-droids/CLAUDE.md` + `skills/` | Cross-project conventions; shared skills |
| Layer 3 — Project | `chief-of-droids/<project>/CLAUDE.md` + `skills/` + `rules/` + `brief.md` | Project conventions + instructional protocols for the six capabilities + project state brief |

### Layer 1 minimality

Layer 1 (Project Instructions) is read by Claude on every prompt. Its token cost multiplies across turns. Constraint: Layer 1 must be minimal but sufficient — bootstrap dispatcher logic, per-turn sentinel verification rule, always-on tool routing, and nothing else.

Substantive content (conventions, project context, skill manifests, protocols) lives in Layer 2 and Layer 3 CLAUDE.md files which are loaded once per session bind and re-loaded only on SHA mismatch detected by the per-turn verify rule. Layer 1 carries the loader; Layer 2 and Layer 3 carry the load.

### Tool layer vocabulary

Three distinct concerns conflated by "always-on tools":

- **Registration** — happens in Claude Desktop client config (`claude_desktop_config.json`), outside the framework's control. Defines which MCP servers are available to any session.
- **Routing** — Layer 1 declares which tools are universally expected and routes them at the framework level. Layer 3 may declare additional project-specific tool routing.
- **Usage** — skills invoke tools; SKILL.md describes the calling pattern per skill.

Always-on tools (filesystem, git, fetch) are routed at Layer 1. Project-specific tools are routed at Layer 3. Registration is a prerequisite the framework assumes but does not control.

### Bootstrap protocol

Single-predicate-per-turn pattern. No separate session-start phase; every turn runs the same check.

1. Read sentinel for current session, keyed on `recent_chats[0].uri` (see `session-identity-recommendation.md`).
2. **If sentinel absent or uri mismatch:**
   - Prompt user: "Which project?"
   - On user answer, load:
     - `chief-of-droids/CLAUDE.md` (workspace)
     - `chief-of-droids/<project>/CLAUDE.md` (project)
     - `chief-of-droids/<project>/brief.md` (project state brief)
   - Verify all three loaded; halt with clear error if any fails.
   - Write sentinel with current state (see schema below).
   - Emit anchor confirming load.
3. **If sentinel present and uri matches:**
   - Compare `workspace_md_sha` / `project_md_sha` / `brief_sha` against disk.
   - On any mismatch, reload that file and update sentinel.
   - Proceed silently to user request.

User chooses project once per session, at step 2 of the first turn. No default; explicit selection required.

### Sentinel schema

Path: `chief-of-droids/.sessions/<urlencoded-uri>.json`

Fields:

- `uri` — session identifier from `recent_chats[0]`
- `project` — selected project name
- `loaded_at` — ISO timestamp of bind
- `workspace_md_sha` — SHA of `chief-of-droids/CLAUDE.md` at load
- `project_md_sha` — SHA of `<project>/CLAUDE.md` at load
- `brief_sha` — SHA of `<project>/brief.md` at load
- `resolved_skills` — array of `{trigger, skill, tier}` from skills bootstrap

### Project brief

Each project carries a brief at `<project>/brief.md`. Role: contextualize the chat session — what the project is, current state, scope of in-flight work, relevant constraints. Loaded by the bootstrap protocol at project bind alongside project CLAUDE.md. SHA tracked in sentinel; mid-session edit triggers reload.

The brief is distinct from project CLAUDE.md: CLAUDE.md carries conventions and rules (stable); brief carries state and context (mobile). Separating them lets the brief evolve session-to-session without dirtying the conventions layer.

## Reliability principle

Framework reliability budget should be spent in this priority order:

1. **Mechanical checks** — filesystem reads, sentinel writes, corpus scans, SHA comparisons. Deterministic given correct inputs.
2. **Once-per-session behaviors** — at bootstrap, when context is freshest and adherence highest.
3. **Behavioral rules as backup, not primary** — instructional framing reinforces mechanical checks but should not be the sole guarantee for anything that matters.

Implication: any condition relying on "Claude will reliably emit/check/refuse X on every turn" has a probability ceiling well below 100%, degrading with context length and competing rules. Where audit, verification, or conflict resolution is needed, prefer mechanical mechanisms (filesystem state) over behavioral mechanisms (token emission patterns).

This principle motivates the skills-routing design below (sentinel resolution map instead of per-turn anchor warnings) and should be applied across other framework rules during a separate audit pass — flagged in Open Items.

## Skills routing — design decisions from this session

Precedence rule: **workspace tier wins** (Option 2, hardened).

Implementation:

- Hard reject at authoring time on trigger collision (`creating-skills` enforces; workspace and project trigger phrases must be disjoint by name and phrase).
- Sentinel records `{trigger → skill, tier}` resolution map on project bind.
- Runtime collisions impossible by construction; audit is mechanical (filesystem read), not behavioral (Claude emits anchor token).
- Reliability estimate: ~92–93%.

Drift prevention (description-as-SoT replication, "Option 1") deferred. Trigger conditions for revisit: skill count >~25, second author joins, or dispatcher matures enough for incremental adoption.

## Preconditions for the design to work

1. `creating-skills` runs corpus-wide trigger collision scan; hard reject on conflict.
2. Dispatcher implements fail-fast tier resolution (workspace match → exit).
3. Sentinel schema implemented including `resolved_skills` on bind.
4. Governance escape hatch documented (PR-to-workspace, not runtime override).
5. Workspace skill trigger changes versioned (major bump on trigger edit).
6. Workspace skill removal blocked while any project references it.
7. Composition strictly one-way (workspace cannot reference project skills).
8. Negative triggers respected with same precedence direction.
9. Project-skill authoring asks "could this be workspace?" (promotion > parallel).

## Open items

- Session identity mechanism (parked: `docs/session-identity-recommendation.md`).
- Fate of workspace-level CLAUDE.md (dissolve / duplicate per project / layer below project CLAUDE.md — undecided).
- Project brief content schema and format (free-form markdown for now; conventions undecided).
- Per-capability design not yet specified for: session hygiene protocol, git versioning protocol, conditional rules format.
- Audit existing workspace CLAUDE.md and Project Instructions for "behavioral primary" rules that could be moved to mechanical or once-per-session enforcement.
- Rollout strategy (pilot one project before adopting framework-wide).

## Related artifacts

- `chief-of-droids/docs/session-identity-recommendation.md`
- `chief-of-droids/docs/claude-md-applicability-matrix.md`

---

| Field        | Value       |
|--------------|-------------|
| Version      | 1.0         |
| Last Updated | 2026-05-14  |
| Status       | Draft       |
