# Two-Tier CLAUDE.md Architecture — Design Notes

## Purpose

The component is the chief-of-droids two-tier CLAUDE.md framework operating inside Claude Desktop chat. It mirrors the project-level CLAUDE.md mechanism that Claude Code provides natively by implementing — through instruction rather than platform — the six capabilities Claude Desktop chat does not expose: skills routing, session hygiene, git versioning, available-tools registration, project brief routing, and conditional rules by file type. The architecture is structured as two tiers across three layers: Layer 1 (Project Instructions) acts as a minimal dispatcher, Layer 2 (workspace CLAUDE.md and shared skills) carries cross-project conventions, and Layer 3 (project CLAUDE.md, skills, rules, and brief) carries project-specific conventions and instructional protocols. The goal is to resolve duplication between Project Instructions and workspace CLAUDE.md and to eliminate category errors (Code-style override semantics declared in a Chat environment where no native override mechanism exists).

## Scope

### In Scope

- Layer 1 dispatcher logic at Claude Desktop Project Instructions: bootstrap, per-turn sentinel verification, always-on tool routing.
- Layer 2 workspace tier at `chief-of-droids/CLAUDE.md` and shared skills directory.
- Layer 3 project tier at `chief-of-droids/<project>/CLAUDE.md`, project skills, project `rules/` directory, and project `brief.md`.
- Bootstrap protocol: sentinel-based session binding via `recent_chats[0].uri`; single-predicate-per-turn pattern.
- Session sentinel schema: persistent JSON record keyed on session URI tracking project, load time, SHA fingerprints of bind artifacts, and resolved-skills map.
- Two-tier skill manifest with workspace-tier-wins precedence rule; authoring-time trigger collision detection; sentinel-recorded resolution map.
- Project brief lifecycle: load at bind alongside project CLAUDE.md; SHA-tracked for mid-session edit detection.
- Always-on tools (filesystem, git, fetch) routed at Layer 1; project-specific tools routed at Layer 3.
- Conditional rules by file type: path-scoped rule files at Layer 3, loaded by dispatcher on filesystem read events.

### Out of Scope

- Claude Desktop client-level MCP registration (`claude_desktop_config.json` and related desktop configuration). Substrate treats this as a prerequisite outside framework control.
- Description-as-source-of-truth replication (the "Option 1" drift-prevention scheme). Deferred per substrate.
- Session identity mechanism design itself. Parked in the companion document `docs/session-identity-recommendation.md`.
- Per-capability detailed design for session hygiene, git versioning, and conditional rules format. Substrate flags these as not-yet-specified.
- Fate of workspace-level CLAUDE.md as a separate slot vs. dissolved into project CLAUDE.md. Substrate flags as undecided.
- Rollout strategy and pilot selection. Substrate flags as open item.

### Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| User (chief-of-droids author) | Selects project at bind; authors skills, rules, briefs, and CLAUDE.md content | user |
| Claude Desktop chat client | Provides chat session context; surfaces `recent_chats[0].uri` per turn; renders prompts and anchor outputs | upstream |
| Filesystem MCP server | Reads workspace CLAUDE.md, project CLAUDE.md, project brief, sentinel, path-scoped rule files; writes sentinel records | upstream |
| `creating-skills` skill | Invoked at skill authoring time; performs corpus-wide trigger collision scan; consumes the workspace-tier-wins precedence and disjoint-trigger invariant | downstream |
| Workspace skill set | Resolved against project skill set at project bind; populates sentinel `resolved_skills` map | upstream |
| Project skill set | Resolved against workspace skill set under workspace-tier-wins; populates sentinel `resolved_skills` map | upstream |
| Path-scoped rule files | Loaded by the dispatcher on matching filesystem read events | upstream |

## Glossary

| Term | Definition | Status |
|:--|:--|:--|
| Layer 1 (Dispatcher) | Slot at Claude Desktop Project Instructions; carries bootstrap protocol, per-turn sentinel verification, and always-on tool routing. | substrate |
| Layer 2 (Workspace) | Slot comprising `chief-of-droids/CLAUDE.md` and the shared `skills/` directory; carries cross-project conventions and shared skills. | substrate |
| Layer 3 (Project) | Slot comprising `chief-of-droids/<project>/CLAUDE.md`, project `skills/`, project `rules/`, and `brief.md`; carries project conventions plus instructional protocols for the six capabilities and the project state brief. | substrate |
| Sentinel | Per-session JSON record at `chief-of-droids/.sessions/<urlencoded-uri>.json` capturing bind state for the current chat: URI, project name, load timestamp, SHA fingerprints of bind artifacts, and resolved-skills map. | substrate |
| Project brief | Markdown document at `<project>/brief.md` carrying project state, in-flight scope, and context; loaded at bind alongside project CLAUDE.md; SHA-tracked for mid-session edit detection. | substrate |
| Always-on tools | Tools routed at Layer 1 universally for any session: filesystem, git, fetch. | substrate |
| Registration | Claude Desktop client-config-level declaration of available MCP servers (`claude_desktop_config.json`); outside framework control. | substrate |
| Routing | Framework-level declaration of which tools are expected at a tier (Layer 1 or Layer 3). | substrate |
| Usage | Per-skill invocation pattern described in `SKILL.md`. | substrate |
| Bootstrap protocol | Single-predicate-per-turn pattern run every turn by Layer 1: read sentinel → branch on absence/uri-mismatch into bind, or branch into per-turn SHA verification. | substrate |
| Workspace-tier-wins precedence | Trigger resolution rule: when both tiers match a trigger, workspace skill is invoked; project skill is shadowed. | substrate |
| MCP | Acronym used throughout substrate; expansion not provided in source text. Verify intended expansion (e.g. Model Context Protocol). | auto-derived — verify |
| PR | Pull request — used in "PR-to-workspace" governance escape hatch language. | auto-derived — verify |
| `recent_chats[0].uri` | Session identifier surfaced by the chat client; key for sentinel records. | auto-derived — verify |
| `creating-skills` | Skill that authors new skills and enforces corpus-wide trigger collision rejection. | auto-derived — verify |
| `workspace_md_sha` | Sentinel field — SHA of `chief-of-droids/CLAUDE.md` recorded at load. | auto-derived — verify |
| `project_md_sha` | Sentinel field — SHA of `<project>/CLAUDE.md` recorded at load. | auto-derived — verify |
| `brief_sha` | Sentinel field — SHA of `<project>/brief.md` recorded at load. | auto-derived — verify |
| `resolved_skills` | Sentinel field — array of `{trigger, skill, tier}` entries computed at project bind. | auto-derived — verify |
| Project Instructions | Claude Desktop system-prompt slot for project-level instructions; the physical slot that holds Layer 1. | auto-derived — verify |
| Dispatcher | The Layer 1 instructional logic; runs every turn. | auto-derived — verify |
| Path-scoped rule files | Markdown rule files at `<project>/rules/` carrying `paths:` frontmatter indicating which filesystem paths trigger their on-demand load. | auto-derived — verify |
| Anchor | One-line chat output emitted by the dispatcher on bind to confirm load and surface the resolved project name. | auto-derived — verify |
| Trigger phrase | A natural-language phrase declared in a skill's `SKILL.md` that the dispatcher matches against user prompts to invoke that skill. | auto-derived — verify |

## Functional Requirements

**FR-001** — WHEN a filesystem read of a project file occurs the dispatcher SHALL load applicable path-scoped rule files declared at Layer 3.

**FR-002** — WHEN a turn begins the framework SHALL read the sentinel record for the current session keyed on `recent_chats[0].uri`.

**FR-003** — IF the sentinel is absent or its `uri` field does not match `recent_chats[0].uri` THEN the framework SHALL prompt the user with "Which project?". (no ERR — rationale: prompt is in-band conversational; non-response is not a mechanically detectable failure surface)

**FR-004** — WHEN the user provides a project selection the framework SHALL load `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, and `chief-of-droids/<project>/brief.md`.

**FR-005** — WHEN the three bind artifacts have completed loading the framework SHALL verify that all three were loaded successfully.

**FR-006** — WHEN bind verification succeeds the framework SHALL write the sentinel record with current bind state to `chief-of-droids/.sessions/<urlencoded-uri>.json`.

**FR-007** — WHEN bind completes the framework SHALL emit an anchor message to the chat session confirming the bound project. (no ERR — rationale: Emit contract shape per the contract-shape coverage matrix; no return value to fail on)

**FR-008** — WHEN a turn begins and a matching sentinel is present the framework SHALL compare `workspace_md_sha`, `project_md_sha`, and `brief_sha` recorded in the sentinel against freshly computed SHAs of the corresponding files on disk.

**FR-009** — IF any sentinel SHA mismatches the disk SHA THEN the framework SHALL reload the mismatched file and update the sentinel field with the fresh SHA.

**FR-010** — WHEN project bind completes the framework SHALL populate the sentinel `resolved_skills` field with the workspace+project skill resolution map under workspace-tier-wins precedence.

**FR-011** — WHEN a skill authoring action is invoked via `creating-skills` the framework SHALL execute a corpus-wide trigger-phrase collision scan across the workspace and project skill sets.

**FR-012** — WHEN a workspace skill's trigger phrase is edited the framework SHALL bump that skill's major version.

**FR-013** — WHEN removal of a workspace skill is attempted and any project skill references the workspace skill the framework SHALL hard-reject the removal.

**FR-014** — WHEN a project-skill authoring action begins via `creating-skills` the framework SHALL prompt the author with "could this be workspace?". (no ERR — rationale: prompt is advisory; non-response defaults to continued project-tier authoring)

## Interface Requirements

### Inbound (IR-IN)

**IR-IN-001** — The framework MUST accept `recent_chats[0].uri` as the session identifier surfaced by the Claude Desktop chat client on every turn.

**IR-IN-002** — The framework MUST accept the user's project selection as a free-form text response to the "Which project?" prompt.

**IR-IN-003** — The framework MUST read `chief-of-droids/CLAUDE.md` via the filesystem MCP server.

**IR-IN-004** — The framework MUST read `chief-of-droids/<project>/CLAUDE.md` via the filesystem MCP server.

**IR-IN-005** — The framework MUST read `chief-of-droids/<project>/brief.md` via the filesystem MCP server.

**IR-IN-006** — The framework MUST read the session sentinel at `chief-of-droids/.sessions/<urlencoded-uri>.json` via the filesystem MCP server.

**IR-IN-007** — WHEN a filesystem read of a project file occurs the dispatcher SHALL receive the read-event metadata sufficient to match the file path against path-scoped rule declarations.

### Outbound (IR-OUT)

**IR-OUT-001** — WHEN the sentinel is absent or its `uri` field mismatches the current session URI the framework SHALL emit the prompt "Which project?" to the user channel.

**IR-OUT-002** — WHEN session bind completes the framework SHALL emit a one-line anchor message to the user channel confirming the bound project.

**IR-OUT-003** — WHEN bootstrap fails the framework MUST emit a clear error halt message to the user channel naming the artifact that failed to load.

**IR-OUT-004** — The framework MUST write the session sentinel to `chief-of-droids/.sessions/<urlencoded-uri>.json` via the filesystem MCP server.

**IR-OUT-005** — WHEN a trigger-phrase collision is detected during a `creating-skills` invocation the framework SHALL emit a hard-reject message to the skill author naming the conflicting trigger and both involved skills.

## Data Requirements

### Data Requirements (DR)

**DR-001** — Session sentinel

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|
| `uri` | string | REQUIRED UNIQUE | From `recent_chats[0].uri`; primary key for the sentinel record |
| `project` | string | REQUIRED | Project selected by the user at bind; corresponds to a `<project>/` directory under `chief-of-droids/` |
| `loaded_at` | string (ISO-8601 timestamp) | REQUIRED | Time of session bind |
| `workspace_md_sha` | string (SHA digest) | REQUIRED | SHA of `chief-of-droids/CLAUDE.md` at load |
| `project_md_sha` | string (SHA digest) | REQUIRED | SHA of `<project>/CLAUDE.md` at load |
| `brief_sha` | string (SHA digest) | REQUIRED | SHA of `<project>/brief.md` at load |
| `resolved_skills` | array of objects | REQUIRED | Each entry: `{trigger: string, skill: string, tier: "workspace" \| "project"}` |

Lifecycle: written at bind; updated on SHA mismatch reload (FR-009) and on `resolved_skills` population (FR-010); retained for the lifetime of the chat session; not yet specified for cross-session retention or pruning.

### Transformation Requirements (TR)

**TR-001** — Sentinel path derivation

| Input | Rule | Output |
|:--|:--|:--|
| `recent_chats[0].uri` (raw URI string) | URL-encode the URI; prepend `chief-of-droids/.sessions/`; append `.json` | Filesystem path of the sentinel record for this session |

**TR-002** — Bind-artifact SHA computation

| Input | Rule | Output |
|:--|:--|:--|
| File content of `chief-of-droids/CLAUDE.md` at load | Compute SHA digest over file bytes | `workspace_md_sha` field value |
| File content of `<project>/CLAUDE.md` at load | Compute SHA digest over file bytes | `project_md_sha` field value |
| File content of `<project>/brief.md` at load | Compute SHA digest over file bytes | `brief_sha` field value |

Note: substrate does not pin the SHA algorithm (SHA-1, SHA-256, etc.). To be specified.

**TR-003** — Resolved-skills map derivation

| Input | Rule | Output |
|:--|:--|:--|
| Workspace skill manifest (set of `{trigger, skill}` declared at Layer 2) and project skill manifest (set of `{trigger, skill}` declared at Layer 3), at project bind | For each unique trigger, assign tier = `workspace` if the trigger is declared in the workspace manifest, else tier = `project`. The authoring-time disjoint-trigger invariant (CON-011) guarantees no conflict; the precedence is fail-fast tier resolution per CON-012. | `resolved_skills` array — one entry `{trigger, skill, tier}` per trigger across both manifests |

## Non-Functional Requirements

**NFR-001** — The framework MUST achieve workspace-tier-wins trigger resolution reliability of at least 92%. | Measurement: trigger resolution success rate over a representative corpus of user prompts; threshold ≥ 92% (substrate estimate 92–93%).

**NFR-002** — N/A — substrate silent on performance. Measurement: TBD.

**NFR-003** — The framework SHOULD minimize Layer 1 (Project Instructions) token footprint, since Layer 1 is read on every prompt and its cost multiplies across turns. | Measurement: TBD — substrate provides qualitative threshold only ("minimal but sufficient: bootstrap dispatcher logic, per-turn sentinel verification rule, always-on tool routing, and nothing else").

## Security

N/A — substrate silent on Security. None of the closed-enumeration categories (authentication, authorization, encryption, audit logging, rate limiting, input validation) is explicitly addressed.

## Constraints

**CON-001** — Layer 1 SHALL contain only the bootstrap dispatcher, per-turn sentinel verification logic, and always-on tool routing.

**CON-002** — Layer 2 SHALL contain cross-project conventions and shared skills only.

**CON-003** — Layer 3 SHALL contain project conventions, instructional protocols for the six capabilities, project skills, project rules, and the project brief.

**CON-004** — Layer 2 and Layer 3 CLAUDE.md files SHALL be loaded once per session bind and reloaded only on SHA mismatch detected by the per-turn verification rule.

**CON-005** — Always-on tools (filesystem, git, fetch) SHALL be routed at Layer 1.

**CON-006** — Project-specific tools SHALL be routed at Layer 3.

**CON-007** — Project selection by the user at session bind SHALL require explicit input; no default value is permitted.

**CON-008** — Each project SHALL carry a brief at `<project>/brief.md`.

**CON-009** — Project CLAUDE.md and project brief SHALL be distinct artifacts, with project CLAUDE.md carrying conventions and rules (stable) and project brief carrying state and context (mobile).

**CON-010** — WHEN both workspace and project skill sets match a trigger the workspace skill SHALL win the resolution.

**CON-011** — Trigger phrases SHALL be disjoint between workspace and project skill sets, by name and by phrase.

**CON-012** — The dispatcher SHALL implement fail-fast tier resolution: a workspace match SHALL terminate the resolution walk before any project lookup.

**CON-013** — The sentinel schema SHALL include the `resolved_skills` field.

**CON-014** — The governance escape hatch for runtime tier-precedence overrides SHALL be a pull-request-to-workspace, not a runtime override mechanism.

**CON-015** — Workspace skills SHALL reference only other workspace skills.

**CON-016** — Negative triggers SHALL respect the same workspace-tier-wins precedence direction as positive triggers.

## Error Handling

**ERR-001** — IF loading a path-scoped rule file does not complete successfully THEN the framework SHALL surface the failure to the caller and continue the user request without that rule applied. → FR-001

**ERR-002** — IF reading the session sentinel does not complete successfully (file unreadable or content malformed) THEN the framework SHALL treat the sentinel as absent and proceed to the bind branch. → FR-002

**ERR-003** — IF loading any of workspace CLAUDE.md, project CLAUDE.md, or project brief does not complete successfully THEN the framework SHALL halt with a clear error message naming the missing artifact. → FR-004

**ERR-004** — IF the bind-artifact verification does not complete successfully THEN the framework SHALL halt with a clear error message. → FR-005

**ERR-005** — IF writing the session sentinel does not complete successfully THEN the framework SHALL surface the write failure to the user and halt the bind. → FR-006

**ERR-006** — IF SHA comparison does not complete successfully for any tracked artifact THEN the framework SHALL treat that artifact as mismatched and trigger reload. → FR-008

**ERR-007** — IF reload of a tracked artifact does not complete successfully THEN the framework SHALL halt with a clear error message. → FR-009

**ERR-008** — IF populating the `resolved_skills` field does not complete successfully THEN the framework SHALL halt the bind with a clear error message. → FR-010

**ERR-009** — IF the corpus-wide trigger-phrase collision scan does not complete successfully THEN `creating-skills` SHALL hard-reject the in-flight skill authoring action. → FR-011

**ERR-010** — IF the major-version bump on a workspace-skill trigger edit does not complete successfully THEN the framework SHALL hard-reject the trigger edit. → FR-012

**ERR-011** — IF the workspace-skill reference scan does not complete successfully THEN the framework SHALL hard-reject the workspace-skill removal (fail closed). → FR-013

## Observability

N/A — substrate silent on Observability. None of the closed-enumeration categories (metric exposure, structured log emission, trace span emission, health endpoint, alert threshold) is explicitly addressed. The anchor confirmation emitted on bind (FR-007 / IR-OUT-002) is a user-channel signal classified under IR-OUT, not OBS.

## Acceptance Criteria

**FR-001**
- AC: Given a filesystem read of a project file matches a `paths:` declaration in some path-scoped rule file, the dispatcher loads that rule file before completing the read response.

**FR-002**
- AC: Given a new turn begins, the framework attempts to read `chief-of-droids/.sessions/<urlencoded-uri>.json` keyed on the current `recent_chats[0].uri` value.

**FR-003**
- AC: Given the sentinel does not exist or its `uri` field does not equal `recent_chats[0].uri`, the framework emits the literal prompt "Which project?" to the user channel.

**FR-004**
- AC: Given a user response with a project name, the framework issues three filesystem reads: workspace CLAUDE.md, project CLAUDE.md at `<project>/CLAUDE.md`, project brief at `<project>/brief.md`.

**FR-005**
- AC: Given the three reads return, the framework asserts each read returned content and not a not-found / unreadable signal.

**FR-006**
- AC: Given bind verification passes, the framework writes a sentinel JSON record at the path computed by TR-001 containing all DR-001 fields.

**FR-007**
- AC: Given bind completes, a one-line anchor message naming the bound project appears in the chat output before the user request is processed.

**FR-008**
- AC: Given a turn begins with a matching sentinel, the framework recomputes the SHA of each of workspace CLAUDE.md, project CLAUDE.md, and project brief, and compares each against the corresponding sentinel field.

**FR-009**
- AC: Given a SHA mismatch on file F, the framework reloads F and the sentinel field for F is updated to the fresh SHA on disk after the operation completes.

**FR-010**
- AC: Given project bind completes, the sentinel `resolved_skills` field is a non-empty array containing one entry per trigger across workspace and project manifests, with `tier` correctly classified.

**FR-011**
- AC: Given a new skill is authored via `creating-skills`, a corpus-wide scan of all existing trigger phrases is executed and any duplicate causes hard rejection.

**FR-012**
- AC: Given a workspace skill's trigger phrase is edited, that skill's version major segment increments by one.

**FR-013**
- AC: Given a request to remove a workspace skill while at least one project skill references it, the removal action is rejected and the workspace skill remains in place.

**FR-014**
- AC: Given a project-skill authoring action begins, the literal prompt "could this be workspace?" is surfaced to the author before the authoring is finalized.

**IR-IN-001**
- AC: The framework reads `recent_chats[0].uri` at the start of every turn and the value is non-empty.

**IR-IN-002**
- AC: The framework accepts a free-form text response to "Which project?" and uses it as the project identifier.

**IR-IN-003**
- AC: A filesystem MCP read of `chief-of-droids/CLAUDE.md` returns content.

**IR-IN-004**
- AC: A filesystem MCP read of `chief-of-droids/<project>/CLAUDE.md` returns content.

**IR-IN-005**
- AC: A filesystem MCP read of `chief-of-droids/<project>/brief.md` returns content.

**IR-IN-006**
- AC: A filesystem MCP read of `chief-of-droids/.sessions/<urlencoded-uri>.json` returns content or a not-found signal.

**IR-IN-007**
- AC: The dispatcher receives the read-event path before completing the user request, sufficient to match against `paths:` declarations.

**IR-OUT-001**
- AC: The chat output contains the literal text "Which project?" when the bind branch is entered.

**IR-OUT-002**
- AC: The chat output contains an anchor line naming the bound project after a successful bind.

**IR-OUT-003**
- AC: On bootstrap failure, the chat output names the artifact that failed to load.

**IR-OUT-004**
- AC: A filesystem MCP write of the sentinel JSON to `chief-of-droids/.sessions/<urlencoded-uri>.json` returns success.

**IR-OUT-005**
- AC: On collision detection, the rejection message names the conflicting trigger and both involved skills.

**DR-001**
- AC: A written sentinel JSON file conforms to the DR-001 field set; all REQUIRED fields are present; `uri` is unique per sentinel file.

**TR-001**
- AC: For URI `u`, the sentinel path equals `chief-of-droids/.sessions/` + `urlencode(u)` + `.json`.

**TR-002**
- AC: The SHA digest stored in `workspace_md_sha` recomputes to the same value when applied to the byte content of `chief-of-droids/CLAUDE.md` at load time. Same property for `project_md_sha` and `brief_sha`.

**TR-003**
- AC: For each `{trigger, skill, tier}` entry in `resolved_skills`, the `tier` value matches the tier from which the trigger was sourced; the entry set covers every trigger present in either manifest at bind time.

**NFR-001**
- AC: Over a representative corpus of user prompts spanning workspace and project triggers, the workspace-tier-wins resolution succeeds on at least 92% of resolution events.

**NFR-002**
- AC: N/A — no verifiable condition derivable from substrate.

**NFR-003**
- AC: N/A — no quantitative threshold provided by substrate. Verifiable once measurement is pinned.

**CON-001**
- AC: Static inspection of Project Instructions content shows only bootstrap dispatcher logic, per-turn sentinel verify rule, and always-on tool routing — no conventions, no skill manifests, no protocols.

**CON-002**
- AC: Static inspection of `chief-of-droids/CLAUDE.md` and the shared `skills/` directory contains only cross-project conventions and shared skills.

**CON-003**
- AC: Static inspection of `chief-of-droids/<project>/` contains a CLAUDE.md, a `skills/`, a `rules/`, and a `brief.md`; CLAUDE.md content covers project conventions and the six instructional protocols.

**CON-004**
- AC: Trace of a session shows Layer 2 and Layer 3 CLAUDE.md files are read once at bind; subsequent reads occur only on SHA mismatch.

**CON-005**
- AC: Static inspection of Project Instructions shows filesystem, git, and fetch routing declarations.

**CON-006**
- AC: Project-specific tool routing declarations appear in `<project>/CLAUDE.md` and not in Project Instructions.

**CON-007**
- AC: A bind flow with no user project selection halts at the prompt; no default project is bound.

**CON-008**
- AC: Each `<project>/` directory under `chief-of-droids/` contains a `brief.md` file.

**CON-009**
- AC: Static inspection shows `<project>/CLAUDE.md` content is conventions/rules-only and `<project>/brief.md` content is state/context-only; no overlap.

**CON-010**
- AC: Given a trigger declared in both manifests (test fixture), the resolution returns the workspace skill.

**CON-011**
- AC: A corpus scan across workspace and project manifests returns zero shared trigger phrases.

**CON-012**
- AC: Instrumented trace of dispatcher resolution shows project-tier lookup is skipped when a workspace-tier match is found.

**CON-013**
- AC: A written sentinel file always contains the `resolved_skills` field.

**CON-014**
- AC: The governance documentation references PR-to-workspace as the override mechanism; no runtime override mechanism is documented or implemented.

**CON-015**
- AC: A static scan of workspace `SKILL.md` files contains no references to project-scoped skill identifiers.

**CON-016**
- AC: A test case with a negative trigger declared at both tiers resolves to the workspace skill (same direction as positive triggers).

**ERR-001**
- AC: Given a path-scoped rule file is unreadable, the user request still completes; an entry surfaces the failure.

**ERR-002**
- AC: Given the sentinel file is corrupt or unreadable, the framework enters the prompt branch.

**ERR-003**
- AC: Given workspace CLAUDE.md is unreadable at bind, the chat output contains a halt message naming `chief-of-droids/CLAUDE.md`. Same for project CLAUDE.md and project brief.

**ERR-004**
- AC: Given verification fails for any of the three artifacts, the chat output contains a halt message.

**ERR-005**
- AC: Given the sentinel write fails, the chat output names the write failure and the bind does not proceed.

**ERR-006**
- AC: Given SHA computation fails for an artifact, the framework triggers reload of that artifact.

**ERR-007**
- AC: Given reload fails, the chat output contains a halt message naming the artifact.

**ERR-008**
- AC: Given `resolved_skills` population fails, the chat output contains a halt message and no sentinel is written.

**ERR-009**
- AC: Given the collision scan fails, `creating-skills` rejects the authoring action and surfaces the scan failure.

**ERR-010**
- AC: Given the version bump fails, the trigger edit is rejected and the original trigger phrase is retained.

**ERR-011**
- AC: Given the reference scan fails, the removal action is rejected; the workspace skill remains in place.

## Quality Criteria scorecard

| Criterion   | Definition |
|:------------|:-----------|
| Atomic      | The requirement addresses exactly one behavior, constraint, or quality attribute. It contains a single modal verb (SHALL, MUST, SHOULD, MAY). |
| Unambiguous | All terms used are defined in the Glossary or are universally understood. No term is open to more than one interpretation. |
| Verifiable  | The requirement has at least one acceptance criterion — a condition that can be confirmed through testing, inspection, or measurement. |
| Traceable   | The requirement carries a valid, unique identifier (`<CAT>-NNN`) that enables cross-referencing, impact analysis, and change tracking. |
| Bounded     | For NFR-class requirements (NFR, OBS, SEC): the requirement specifies a quantitative threshold (value, time unit, percentage, or volume). N/A for all other requirement types. |

| Req ID    | Atomic | Unambiguous | Verifiable | Traceable | Bounded |
|:----------|:------:|:-----------:|:----------:|:---------:|:-------:|
| FR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-003    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-004    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-005    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-006    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-007    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-008    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-009    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-010    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-011    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-012    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-013    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-014    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-001 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-002 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-003 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-004 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-005 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-006 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-007 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-001|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-002|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-003|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-004|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-005|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| DR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| TR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| TR-002    |   ✓    |      ✗      |     ✓      |     ✓     |   N/A   |
| TR-003    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| NFR-001   |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
| NFR-002   |  N/A   |     N/A     |     ✗      |     ✓     |    ✗    |
| NFR-003   |   ✓    |      ✓      |     ✗      |     ✓     |    ✗    |
| CON-001   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-002   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-003   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-004   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-005   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-006   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-007   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-008   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-009   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-010   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-011   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-012   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-013   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-014   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-015   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-016   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-001   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-002   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-003   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-004   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-005   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-006   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-007   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-008   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-009   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-010   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-011   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
