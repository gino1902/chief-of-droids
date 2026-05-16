# Two-Tier CLAUDE.md Architecture — Design Notes

## Purpose

The component is a two-tier instructional architecture for the chief-of-droids framework that runs in Claude Desktop chat. It eliminates duplication between Claude Desktop Project Instructions (the system prompt) and workspace CLAUDE.md, and replaces Claude-Code-specific override semantics — which have no native effect in chat — with explicit instructional protocols for the six Claude-Code-native capabilities the framework must implement by instruction: skills routing, session hygiene, git versioning, available tools, project brief route, and conditional rules by file type. It specifies the three architectural layers (dispatcher / workspace / project), the bootstrap protocol with per-turn sentinel verification, the sentinel schema, the skills-routing precedence rule, the preconditions under which the design holds, and the reliability principle that motivates mechanical over behavioural enforcement.

## Scope

### In Scope

- Three-layer architecture: Layer 1 (Project Instructions dispatcher), Layer 2 (workspace CLAUDE.md + shared skills), Layer 3 (project CLAUDE.md + project skills + rules + brief)
- Layer 1 minimality — dispatcher payload restricted to bootstrap protocol, per-turn sentinel verification, and always-on tool routing
- Bootstrap protocol — single-predicate-per-turn pattern with sentinel resolution
- Sentinel schema with SHA tracking for workspace CLAUDE.md, project CLAUDE.md, and project brief
- Project brief at `<project>/brief.md` — loaded at bind, SHA-tracked, distinct from project CLAUDE.md
- Skills routing precedence — workspace tier wins; authoring-time corpus-wide trigger collision scan; sentinel resolution map at bind
- Tool layer vocabulary — registration / routing / usage as distinct concerns; always-on tools routed at Layer 1; project-specific tool routing at Layer 3
- Workspace skill versioning rules (major bump on trigger-phrase edit) and removal-blocking when referenced by any project
- One-way composition rule (workspace SHALL NOT reference project skills) and negative-trigger precedence
- Reliability principle — mechanical mechanisms preferred over behavioural ones for audit, verification, and conflict resolution

### Out of Scope

- Description-as-source-of-truth replication of skill descriptions ("Option 1") — deferred until trigger conditions met (skill count > ~25, second author, dispatcher maturity)
- Per-capability protocol specifications for session hygiene, git versioning, and conditional rules format — deferred to follow-up work
- Fate of workspace-level CLAUDE.md (dissolve / duplicate per project / layer below project CLAUDE.md) — undecided
- Project brief content schema and free-form format conventions — undecided
- Audit of existing workspace CLAUDE.md and Project Instructions for "behavioral primary" rules — separate audit pass
- Rollout strategy (pilot project vs. framework-wide adoption) — deferred
- Session identity mechanism itself — parked in `docs/session-identity-recommendation.md`
- MCP server registration — happens in `claude_desktop_config.json` outside framework control; treated as prerequisite

## Actors & Consumers

| Actor | Role | Direction |
|:------|:-----|:----------|
| User | Selects project at first turn; consumes anchor confirmations and error messages | user |
| Claude Desktop client | Reads Project Instructions on every prompt; exposes `recent_chats` session API | upstream |
| Filesystem MCP | Carries reads and writes for CLAUDE.md, brief, sentinel, skills | upstream |
| `chief-of-droids/CLAUDE.md` (workspace) | Cross-project conventions and shared-skills declaration | upstream |
| `chief-of-droids/<project>/CLAUDE.md` | Project conventions and instructional protocols for native-capability implementations | upstream |
| `chief-of-droids/<project>/brief.md` | Project state and in-flight-work context — mobile across sessions | upstream |
| `creating-skills` skill | Enforces trigger-collision rejection at skill authoring time | downstream |
| `claude_desktop_config.json` | MCP server registry — prerequisite outside framework control | upstream |
| `docs/session-identity-recommendation.md` | Source of the `recent_chats[0].uri` sentinel-keying decision | upstream |

## Glossary

| Term | Definition | Status |
|:-----|:-----------|:-------|
| MCP | Model Context Protocol — server registry layer through which tools are exposed to a Claude Desktop session | auto-derived — verify |
| SHA | Content-addressable hash used to detect whether a tracked file has changed since the last bind | auto-derived — verify |
| `recent_chats[0].uri` | Claude Desktop session identifier — the most-recent chat URI exposed by the client API; used as the sentinel key | auto-derived — verify |
| Layer 1 | Dispatcher tier — Claude Desktop Project Instructions slot; carries bootstrap protocol, per-turn sentinel verify, and always-on tool routing | substrate |
| Layer 2 | Workspace tier — `chief-of-droids/CLAUDE.md` + shared `skills/`; cross-project conventions and shared skills | substrate |
| Layer 3 | Project tier — `chief-of-droids/<project>/CLAUDE.md`, `skills/`, `rules/`, `brief.md`; project-specific implementations | substrate |
| Registration | Step in `claude_desktop_config.json` declaring which MCP servers are available to any session — outside framework control | substrate |
| Routing | Step at which Layer 1 (universal tools) and Layer 3 (project-specific tools) declare expected tool wiring | substrate |
| Usage | Step at which skills invoke tools; the calling pattern is described per skill in its SKILL.md | substrate |
| Always-on tools | Tools routed at Layer 1 — filesystem, git, fetch | substrate |
| Bootstrap protocol | Single-predicate-per-turn pattern run at every turn that resolves sentinel state and binds the session | substrate |
| Bind | The successful completion of a load cycle for workspace CLAUDE.md, project CLAUDE.md, and project brief, followed by a sentinel write | auto-derived — verify |
| Sentinel | Per-session state file at `chief-of-droids/.sessions/<urlencoded-uri>.json` recording bind state and SHAs | substrate |
| Project brief | `<project>/brief.md` — project state and context loaded at bind, SHA-tracked, distinct from project CLAUDE.md | substrate |
| Resolved skills map | The `{trigger, skill, tier}` array recorded in the sentinel at project bind | substrate |
| Workspace tier wins | Skills-routing precedence rule — when both tiers declare the same trigger, the workspace skill is selected | substrate |
| Trigger collision | Two or more skills declaring identical trigger phrases or names across tiers | auto-derived — verify |
| Anchor | Confirmation line emitted by the framework after a successful bind | auto-derived — verify |
| Project Instructions | Claude Desktop's per-prompt system content slot — the Layer 1 carrier | auto-derived — verify |
| `creating-skills` | The framework skill that authors new skills and enforces the trigger-collision scan at authoring time | auto-derived — verify |
| Reliability budget | The bounded share of framework reliability that can be spent in priority order on mechanical, once-per-session, and behavioural mechanisms | substrate |

## Functional Requirements

**FR-001** — WHEN a turn begins the framework SHALL read the sentinel record keyed on `recent_chats[0].uri` for the current session.

**FR-002** — IF the sentinel for the current `recent_chats[0].uri` is absent or its stored uri does not match the current session's uri THEN the framework SHALL prompt the user with "Which project?".

**FR-003** — WHEN the user supplies a project name in response to the project prompt the framework SHALL load `chief-of-droids/CLAUDE.md`.

**FR-004** — WHEN the user supplies a project name in response to the project prompt the framework SHALL load `chief-of-droids/<project>/CLAUDE.md` for the selected project.

**FR-005** — WHEN the user supplies a project name in response to the project prompt the framework SHALL load `chief-of-droids/<project>/brief.md` for the selected project.

**FR-006** — WHEN the three bind artefacts (workspace CLAUDE.md, project CLAUDE.md, project brief) finish loading the framework SHALL verify that all three loads completed successfully.

**FR-007** — WHEN bind succeeds the framework SHALL write a sentinel record populated with `uri`, `project`, `loaded_at`, `workspace_md_sha`, `project_md_sha`, `brief_sha`, and `resolved_skills`.

**FR-008** — WHEN bind succeeds the framework SHALL emit an anchor confirming the load. (no ERR — rationale: Emit-shape per contract-shape coverage matrix; no completion-failure semantics)

**FR-009** — IF the sentinel for the current `recent_chats[0].uri` is present and its stored uri matches THEN the framework SHALL compare `workspace_md_sha`, `project_md_sha`, and `brief_sha` against the on-disk content hash of each corresponding artefact.

**FR-010** — IF a SHA mismatch is detected for any of workspace CLAUDE.md, project CLAUDE.md, or project brief THEN the framework SHALL reload the affected artefact and update its SHA in the sentinel.

**FR-011** — WHEN a skill is being authored or its trigger phrase modified the `creating-skills` skill SHALL execute a corpus-wide trigger-collision scan over all workspace-tier and project-tier skills.

**FR-012** — IF the trigger-collision scan finds a trigger name or phrase shared between a workspace-tier skill and any project-tier skill THEN the `creating-skills` skill SHALL hard-reject the authoring attempt. (no ERR — rationale: this FR is itself an Unwanted-Behavior response to FR-011; pairing it with an ERR would be recursive)

**FR-013** — WHEN a skill trigger is resolved at runtime the dispatcher SHALL select the workspace-tier match if one exists and otherwise select the project-tier match. (no ERR — rationale: Select-shape per contract-shape coverage matrix)

**FR-014** — WHEN a workspace-tier skill's trigger phrase is edited the framework SHALL bump the workspace-tier skill's version by one major increment.

**FR-015** — IF a removal of a workspace-tier skill is attempted while any project-tier skill references it THEN the framework SHALL block the removal. (no ERR — rationale: this FR is itself an Unwanted-Behavior response that guards skill removal; no further error response defined)

## Interface Requirements

### Inbound (IR-IN)

**IR-IN-001** — The framework MUST read `recent_chats[0].uri` from the Claude Desktop session API at the start of every turn.

**IR-IN-002** — The framework MUST accept a free-form project-name string supplied by the user in response to the "Which project?" prompt.

**IR-IN-003** — The framework MUST read `chief-of-droids/CLAUDE.md` as a markdown document via the Filesystem MCP.

**IR-IN-004** — The framework MUST read `chief-of-droids/<project>/CLAUDE.md` as a markdown document via the Filesystem MCP.

**IR-IN-005** — The framework MUST read `chief-of-droids/<project>/brief.md` as a markdown document via the Filesystem MCP.

**IR-IN-006** — The framework MUST read the per-session sentinel JSON record at `chief-of-droids/.sessions/<urlencoded-uri>.json` via the Filesystem MCP.

### Outbound (IR-OUT)

**IR-OUT-001** — The framework MUST emit the prompt "Which project?" to the user channel when sentinel is absent or its stored uri does not match.

**IR-OUT-002** — The framework MUST emit an anchor confirming load to the user channel after a successful bind.

**IR-OUT-003** — The framework MUST emit a clear error message identifying the missing artefact to the user channel when any bind-time load fails.

**IR-OUT-004** — The framework MUST write the per-session sentinel JSON record at `chief-of-droids/.sessions/<urlencoded-uri>.json` via the Filesystem MCP.

## Data Requirements

### Data Requirements (DR)

**DR-001** — Sentinel record

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|
| `uri` | string | REQUIRED UNIQUE | Session identifier from `recent_chats[0].uri`; primary key |
| `project` | string | REQUIRED | Selected project name as supplied by the user at bind |
| `loaded_at` | timestamp | REQUIRED | ISO-8601 timestamp at which bind completed |
| `workspace_md_sha` | string | REQUIRED | Content hash of `chief-of-droids/CLAUDE.md` at load time |
| `project_md_sha` | string | REQUIRED | Content hash of `<project>/CLAUDE.md` at load time |
| `brief_sha` | string | REQUIRED | Content hash of `<project>/brief.md` at load time |
| `resolved_skills` | array | REQUIRED | Array of resolved-skill records (see DR-002); populated at bind |

**DR-002** — Resolved-skill record (element of `resolved_skills` array)

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|
| `trigger` | string | REQUIRED | Trigger phrase or skill name as declared in SKILL.md |
| `skill` | string | REQUIRED | Resolved skill identifier (canonical path or name) |
| `tier` | enum | REQUIRED | One of `workspace`, `project` |

### Transformation Requirements (TR)

**TR-001** — Sentinel-path derivation

| Input | Rule | Output |
|:--|:--|:--|
| `recent_chats[0].uri` (string) | URL-encode the input, prepend `chief-of-droids/.sessions/`, append `.json` | Filesystem path of the per-session sentinel record |

**TR-002** — Bind-artefact SHA derivation

| Input | Rule | Output |
|:--|:--|:--|
| Content of workspace CLAUDE.md at load time | Compute content hash (algorithm not specified by substrate — TBD) | Value stored as `workspace_md_sha` |
| Content of project CLAUDE.md at load time | Compute content hash (algorithm not specified by substrate — TBD) | Value stored as `project_md_sha` |
| Content of project brief at load time | Compute content hash (algorithm not specified by substrate — TBD) | Value stored as `brief_sha` |

## Non-Functional Requirements

**NFR-001** — The framework MUST achieve a skills-routing reliability of at least 92%. | Measurement: ≥ 92% successful routing decisions over a representative session corpus (corpus and sampling window TBD per substrate).

**NFR-002** — N/A — substrate silent on performance (latency, response time, throughput). Warning emitted.

**NFR-003** — The Layer 1 dispatcher SHOULD minimise per-turn token footprint relative to substantive content that could otherwise be placed there. | Measurement: TBD — substrate states "minimal but sufficient" without a numeric threshold.

## Security

N/A — substrate silent on Security. The substrate addresses none of authentication, authorization, encryption, audit logging, rate limiting, or input validation. Governance controls (PR-to-workspace escape hatch, trigger-collision rejection, removal blocking) are scoped as Constraints, not Security. Warning emitted.

## Constraints

**CON-001** — The Layer 1 dispatcher SHALL contain only bootstrap-protocol logic, per-turn sentinel verification, and always-on tool routing.

**CON-002** — Always-on tools (filesystem, git, fetch) SHALL be routed at Layer 1.

**CON-003** — Project-specific tool routing SHALL be declared at Layer 3.

**CON-004** — Substantive content (conventions, project context, skill manifests, protocols) SHALL reside in Layer 2 and Layer 3 — not Layer 1.

**CON-005** — Workspace-tier skills SHALL take precedence over project-tier skills when both tiers declare the same trigger.

**CON-006** — Workspace and project trigger phrases SHALL be disjoint by name and phrase.

**CON-007** — Skill composition between tiers SHALL be one-way — workspace-tier skills SHALL NOT reference project-tier skills.

**CON-008** — Negative triggers SHALL be resolved with the same precedence direction as positive triggers (workspace-tier wins).

**CON-009** — The framework SHALL require explicit user project selection per session — no default project is permitted.

**CON-010** — Project brief content SHALL reside in `<project>/brief.md`, separate from `<project>/CLAUDE.md`.

**CON-011** — Per-turn audit, verification, and conflict resolution SHALL rely on mechanical mechanisms (filesystem state, SHA comparison, sentinel resolution) rather than behavioural mechanisms (token emission patterns, anchor warnings).

**CON-012** — The governance escape hatch SHALL be a pull request against the workspace tier — never a runtime override.

## Error Handling

**ERR-001** — IF the sentinel read does not complete successfully THEN the framework SHALL treat the session as unbound and continue to the project-prompt path. → FR-001

**ERR-002** — IF the user does not supply a project name in response to the project prompt THEN the framework SHALL halt bind and surface a missing-input error to the user channel. → FR-002

**ERR-003** — IF the load of workspace CLAUDE.md does not complete successfully THEN the framework SHALL halt bind and surface a clear error identifying the workspace artefact. → FR-003

**ERR-004** — IF the load of project CLAUDE.md does not complete successfully THEN the framework SHALL halt bind and surface a clear error identifying the project artefact. → FR-004

**ERR-005** — IF the load of the project brief does not complete successfully THEN the framework SHALL halt bind and surface a clear error identifying the brief artefact. → FR-005

**ERR-006** — IF the verify step finds that any of the three bind artefacts did not load successfully THEN the framework SHALL halt bind and surface a clear error identifying the missing artefact. → FR-006

**ERR-007** — IF the sentinel write does not complete successfully THEN the framework SHALL halt bind and surface a sentinel-write-failure error to the user channel. → FR-007

**ERR-008** — IF the SHA comparison does not complete successfully THEN the framework SHALL surface a verification-failure error to the user channel. → FR-009

**ERR-009** — IF the reload-and-update step does not complete successfully THEN the framework SHALL surface a reload-failure error to the user channel. → FR-010

**ERR-010** — IF the corpus-wide trigger-collision scan does not complete successfully THEN the `creating-skills` skill SHALL hard-reject the authoring attempt with a scan-failure error. → FR-011

**ERR-011** — IF the workspace-tier skill version bump does not complete successfully THEN the framework SHALL halt the trigger-phrase edit and surface a version-bump-failure error to the user channel. → FR-014

## Observability

N/A — substrate silent on Observability. The substrate addresses none of named metric exposure, structured log emission with retention, trace spans, health probes, or alert thresholds. The anchor (FR-008 / IR-OUT-002) is a user-channel confirmation and is correctly scoped to IR-OUT, not OBS. Warning emitted.

## Acceptance Criteria

**FR-001**
- AC: At the start of every turn, the framework issues a read against the sentinel path derived from `recent_chats[0].uri`.

**FR-002**
- AC: When the sentinel is absent or its stored uri does not match, the prompt "Which project?" appears in the user channel.

**FR-003**
- AC: Following a user project response, the framework issues a Filesystem read for `chief-of-droids/CLAUDE.md` and returns its content.

**FR-004**
- AC: Following a user project response, the framework issues a Filesystem read for `chief-of-droids/<selected-project>/CLAUDE.md` and returns its content.

**FR-005**
- AC: Following a user project response, the framework issues a Filesystem read for `chief-of-droids/<selected-project>/brief.md` and returns its content.

**FR-006**
- AC: All three bind artefacts return content with no error; if any errors, bind halts before sentinel write.

**FR-007**
- AC: After successful bind, the sentinel record exists at the computed path and contains all seven required fields.

**FR-008**
- AC: After successful bind, an anchor line confirming load appears in the user channel.

**FR-009**
- AC: With a matching sentinel, the framework computes the on-disk SHA of each of the three bind artefacts and compares each against the corresponding sentinel field.

**FR-010**
- AC: When any SHA differs from its sentinel value, the affected artefact is re-read and the corresponding sentinel field updated within the same turn.

**FR-011**
- AC: Authoring a new or modified skill triggers a scan of all workspace and project skill trigger phrases before persistence.

**FR-012**
- AC: When the scan returns a collision, `creating-skills` returns a rejection and does not persist the new or edited skill.

**FR-013**
- AC: When a trigger matches in both tiers, the dispatcher's resolved skill is the workspace-tier instance and the project-tier alternative is not loaded.

**FR-014**
- AC: Edit to a workspace-tier skill's trigger phrase results in the workspace-tier skill's version block showing a major-version increment relative to the prior version.

**FR-015**
- AC: Attempted removal of a workspace-tier skill while any project-tier skill references it returns a block decision and leaves the workspace-tier skill in place.

**IR-IN-001**
- AC: The `recent_chats` call returns at least one entry exposing a `.uri` field.

**IR-IN-002**
- AC: The user's free-form text response is captured verbatim and used as the project identifier in subsequent load paths.

**IR-IN-003**
- AC: The Filesystem read for `chief-of-droids/CLAUDE.md` returns its content as text.

**IR-IN-004**
- AC: The Filesystem read for `chief-of-droids/<project>/CLAUDE.md` returns its content as text.

**IR-IN-005**
- AC: The Filesystem read for `chief-of-droids/<project>/brief.md` returns its content as text.

**IR-IN-006**
- AC: The Filesystem read for the computed sentinel path either returns a JSON record or returns a not-found result.

**IR-OUT-001**
- AC: The prompt "Which project?" is emitted to the user channel when sentinel is absent or uri mismatches.

**IR-OUT-002**
- AC: The anchor line appears in the user channel immediately after sentinel write completes.

**IR-OUT-003**
- AC: When any bind-time load fails, an error message identifying the failing artefact appears in the user channel.

**IR-OUT-004**
- AC: A sentinel JSON record is created or updated at the computed path following each successful bind or SHA-mismatch reload.

**DR-001**
- AC: A sentinel record validates against the seven-field schema with `uri` unique across the sentinel directory.

**DR-002**
- AC: Each entry in `resolved_skills` carries `trigger`, `skill`, and `tier`; `tier` is one of `workspace` or `project`.

**TR-001**
- AC: For any `recent_chats[0].uri` value, applying URL-encode + prefix + suffix yields a path that is byte-identical across independent runs.

**TR-002**
- AC: For any artefact content, the SHA derivation yields a hash that is byte-identical across independent runs.

**NFR-001**
- AC: A representative routing-corpus replay yields a success rate of ≥ 92%.

**NFR-002**
- AC: N/A — no verifiable condition derivable from substrate.

**NFR-003**
- AC: A token-count audit of Layer 1 stays within a defined budget (threshold TBD per substrate).

**CON-001**
- AC: A content audit of Layer 1 finds only bootstrap protocol, per-turn sentinel verification, and always-on tool routing.

**CON-002**
- AC: Layer 1 carries routing declarations for filesystem, git, and fetch and no other tools.

**CON-003**
- AC: Project-specific tool routing declarations appear only in Layer 3 files.

**CON-004**
- AC: Layer 1 contains no conventions, project context, skill manifests, or protocols.

**CON-005**
- AC: When a trigger matches in both tiers, the resolved skill belongs to the workspace tier.

**CON-006**
- AC: A corpus-wide name-and-phrase scan returns zero collisions between workspace-tier and project-tier skills.

**CON-007**
- AC: A static scan of workspace-tier SKILL.md files returns no references to project-tier skills.

**CON-008**
- AC: A negative-trigger collision between tiers resolves to the workspace-tier rule.

**CON-009**
- AC: No default project is encoded; bind cannot proceed without an explicit user project response.

**CON-010**
- AC: Project state and context appear in `<project>/brief.md`, and `<project>/CLAUDE.md` carries only conventions and rules.

**CON-011**
- AC: A documentation audit classifies each framework rule as mechanical, once-per-session, or behavioural, with audit-bearing rules in the mechanical bucket.

**CON-012**
- AC: No runtime override path exists for the precedence rule; tier changes require a workspace-tier pull request.

**ERR-001**
- AC: An IO failure on sentinel read results in fall-through to the project-prompt path within the same turn.

**ERR-002**
- AC: When the user response is empty, bind halts and a missing-input error appears in the user channel.

**ERR-003**
- AC: A load failure for workspace CLAUDE.md halts bind and produces an error identifying the workspace artefact.

**ERR-004**
- AC: A load failure for project CLAUDE.md halts bind and produces an error identifying the project artefact.

**ERR-005**
- AC: A load failure for the project brief halts bind and produces an error identifying the brief artefact.

**ERR-006**
- AC: When the verify step finds any artefact missing, bind halts and an error identifying the missing artefact appears in the user channel.

**ERR-007**
- AC: A sentinel-write failure halts bind and produces a sentinel-write-failure error in the user channel.

**ERR-008**
- AC: A SHA-comparison failure produces a verification-failure error in the user channel.

**ERR-009**
- AC: A reload-and-update failure produces a reload-failure error in the user channel.

**ERR-010**
- AC: A scan failure during authoring produces a scan-failure rejection in the `creating-skills` response.

**ERR-011**
- AC: A version-bump failure halts the trigger-phrase edit and produces a version-bump-failure error in the user channel.

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
| FR-015    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-001 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-002 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-003 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-004 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-005 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-006 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-001 |  ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-002 |  ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-003 |  ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-004 |  ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| DR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| DR-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| TR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| TR-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| NFR-001   |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
| NFR-002   |  N/A   |     N/A     |     ✗      |     ✓     |   N/A   |
| NFR-003   |   ✓    |      ✓      |     ✓      |     ✓     |    ✗    |
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
