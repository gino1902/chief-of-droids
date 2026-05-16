# Two-Tier CLAUDE.md Architecture — Design Notes

## Purpose

Specify a two-tier CLAUDE.md architecture for the chief-of-droids framework operating in Claude Desktop chat. The architecture replaces the current setup — in which Project Instructions and workspace CLAUDE.md carry duplicated rules and category-confused override semantics — with three deployment layers: a minimal dispatcher in Claude Desktop Project Instructions (Layer 1), workspace conventions and shared skills in `chief-of-droids/CLAUDE.md` plus `skills/` (Layer 2), and project conventions, project skills, project rules, and a project brief under `chief-of-droids/<project>/` (Layer 3). The dispatcher implements per-turn sentinel-driven bind and SHA-mismatch reload so that substantive content is loaded once per session and re-loaded only on disk change. The framework reproduces, by instruction and mechanical check, six capabilities Claude Code provides natively: skills routing, session hygiene, git versioning, available-tool routing, project brief routing, and conditional rules by file type.

## Scope

### In Scope

- Three-layer architecture: dispatcher (Layer 1), workspace (Layer 2), project (Layer 3) — slot, location, and content responsibility per layer.
- Layer 1 minimality rule and the content boundary between Layer 1 and Layers 2 / 3.
- Tool-layer vocabulary: registration (out-of-framework), routing (Layers 1 and 3), usage (per skill).
- Always-on tool routing at Layer 1 (filesystem, git, fetch).
- Bootstrap protocol: single-predicate-per-turn pattern; sentinel read, project-prompt, three-file load, sentinel write, anchor emission, per-turn SHA verify, reload-on-mismatch.
- Sentinel schema and on-disk location.
- Project brief role, location, and SHA-tracked lifecycle.
- Skills-routing precedence: workspace tier wins; trigger-disjointness invariant; bind-time resolution map.
- Authoring-time corpus collision scan; major-version-bump on workspace trigger edit; removal block while project references exist; project-skill promotion prompt.
- Reliability budget priority order: mechanical checks > once-per-session behaviors > behavioral rules.

### Out of Scope

- Session identity mechanism beyond `recent_chats[0].uri` (parked in `docs/session-identity-recommendation.md`).
- Fate of workspace-level CLAUDE.md (dissolve, duplicate per project, or layer below project CLAUDE.md — undecided).
- Project brief content schema and format (free-form markdown; conventions undecided).
- Per-capability protocol design for: session hygiene, git versioning, conditional rules format.
- Audit of existing workspace CLAUDE.md and Project Instructions for behavioral-primary rules suitable for re-platforming onto mechanical or once-per-session enforcement.
- Rollout strategy (pilot one project before adopting framework-wide).
- Drift prevention via description-as-source-of-truth replication (Option 1) — deferred until skill count > ~25, second author joins, or dispatcher matures.
- MCP server registration in `claude_desktop_config.json` (prerequisite assumed, not controlled by the framework).

## Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| Framework user | Selects the project at first turn; issues prompts | user |
| Claude Desktop client | Hosts the session; exposes `recent_chats`; loads Project Instructions per turn | upstream |
| Filesystem MCP | Reads workspace CLAUDE.md, project CLAUDE.md, project brief, skills, rules; writes sentinel JSON | upstream / downstream |
| Git MCP | Provides status-aware git operations declared in project CLAUDE.md | upstream / downstream |
| Fetch MCP | Retrieves external URL content per workspace fetch routing | upstream |
| `creating-skills` authoring tool | Runs corpus-wide trigger collision scan at skill-authoring time | upstream |
| Workspace CLAUDE.md (`chief-of-droids/CLAUDE.md`) | Source for cross-project conventions; SHA-tracked at bind | upstream |
| Project CLAUDE.md (`<project>/CLAUDE.md`) | Source for project conventions and capability protocols; SHA-tracked at bind | upstream |
| Project brief (`<project>/brief.md`) | Source for project state and context; SHA-tracked at bind | upstream |
| Sentinel JSON (`chief-of-droids/.sessions/<urlencoded-uri>.json`) | Per-session bind state | downstream |

## Glossary

| Term | Definition | Status |
|:-----|:-----------|:-------|
| MCP | Model Context Protocol — server interface exposing tools (filesystem, git, fetch, others) to the Claude Desktop client. | auto-derived — verify |
| sentinel | Per-session JSON state record stored at `chief-of-droids/.sessions/<urlencoded-uri>.json`; tracks bind project, load timestamp, file SHAs, and resolved skills map. | substrate |
| dispatcher | Layer 1 logic carried by Claude Desktop Project Instructions; runs bootstrap, per-turn sentinel verify, and always-on tool routing. | substrate |
| workspace (Layer 2) | The `chief-of-droids/` root carrying cross-project CLAUDE.md and shared `skills/`. | substrate |
| project (Layer 3) | A directory under `chief-of-droids/` carrying its own CLAUDE.md, skills, rules, and brief.md. | substrate |
| bootstrap protocol | Per-turn single-predicate sequence: read sentinel → on absence/mismatch prompt user and bind; on match verify SHAs and reload on mismatch. | substrate |
| always-on tools | Tools routed at Layer 1 for every session — filesystem, git, fetch. | substrate |
| registration | Setup step in `claude_desktop_config.json` that exposes an MCP server to sessions; outside framework control. | substrate |
| routing | Declaration in Layer 1 (always-on) or Layer 3 (project-specific) of which registered tools the framework relies on. | substrate |
| usage | Invocation pattern for a tool, described in each SKILL.md. | substrate |
| project brief | `<project>/brief.md` — mobile session state and context for the chat session; SHA-tracked in sentinel. | substrate |
| anchor | Confirmation line emitted to the user channel on successful bind, naming the bound project. | auto-derived — verify |
| resolved skills map | Array of `{trigger, skill, tier}` records populated in the sentinel at bind, fixing per-trigger skill resolution. | substrate |
| workspace-first precedence | Skill resolution rule: workspace-tier match wins; project-tier match used only when no workspace match exists. | substrate |
| trigger phrase | The user-facing phrase declared in a SKILL.md that causes a skill to be selected; corpus-wide disjoint across tiers. | substrate |
| reliability budget | The framework's effective probability mass available for correctness; spent in priority order on mechanical checks, once-per-session behaviors, behavioral rules. | substrate |
| `recent_chats[0].uri` | First (most recent) chat record's URI, used as the per-session identity key. | auto-derived — verify |
| `workspace_md_sha` | Sentinel field — SHA of `chief-of-droids/CLAUDE.md` at bind. | substrate |
| `project_md_sha` | Sentinel field — SHA of `<project>/CLAUDE.md` at bind. | substrate |
| `brief_sha` | Sentinel field — SHA of `<project>/brief.md` at bind. | substrate |
| `resolved_skills` | Sentinel field — array of `{trigger, skill, tier}` from skills bootstrap. | substrate |
| `creating-skills` | Skill that performs corpus-wide trigger collision scan at authoring time. | substrate |

## Functional Requirements

**FR-001** — WHEN a turn begins THEN the framework SHALL read the sentinel JSON for the current session keyed on `recent_chats[0].uri`.

**FR-002** — IF the sentinel is absent or its `uri` field does not match the current session THEN the framework SHALL prompt the user with the question "Which project?".

**FR-003** — WHEN the user answers the project prompt THEN the framework SHALL load `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, and `chief-of-droids/<project>/brief.md`.

**FR-004** — WHEN the three required bind files have loaded THEN the framework SHALL write a sentinel record populated with `uri`, `project`, `loaded_at`, `workspace_md_sha`, `project_md_sha`, `brief_sha`, and `resolved_skills`.

**FR-005** — WHEN bind completes successfully THEN the framework SHALL emit a load-confirmation anchor to the user channel.

**FR-006** — WHILE the sentinel is present and its `uri` matches the current session THEN the framework SHALL compare `workspace_md_sha`, `project_md_sha`, and `brief_sha` against the SHA computed from the corresponding file on disk.

**FR-007** — IF any SHA comparison reports a mismatch THEN the framework SHALL reload the corresponding file and update the matching SHA field in the sentinel.

**FR-008** — WHEN per-turn sentinel verification completes with no mismatch THEN the framework SHALL proceed silently to the user request.

**FR-009** — WHEN a project is bound THEN the framework SHALL populate the sentinel `resolved_skills` array with one `{trigger, skill, tier}` record per registered skill, applying workspace-first precedence.

**FR-010** — WHEN a new skill is authored THEN the framework SHALL run a corpus-wide trigger collision scan across workspace and project skill sets and reject the authoring on any collision.

**FR-011** — WHEN a workspace skill's trigger phrase is edited THEN the framework SHALL apply a major version bump to that workspace skill.

**FR-012** — IF removal of a workspace skill is attempted WHILE at least one project references that skill THEN the framework SHALL reject the removal.

**FR-013** — WHEN a new project-level skill is authored THEN the framework SHALL prompt the author with "Could this be a workspace skill?".

## Interface Requirements

### Inbound (IR-IN)

**IR-IN-001** — The framework MUST consume `recent_chats[0].uri` from the Claude Desktop client as the session identity input on every turn.

**IR-IN-002** — The framework MUST accept a user reply naming a project directory under `chief-of-droids/` in response to the project-selection prompt.

**IR-IN-003** — The framework MUST read `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, and `chief-of-droids/<project>/brief.md` from the filesystem at bind.

**IR-IN-004** — The framework MUST read the sentinel JSON at `chief-of-droids/.sessions/<urlencoded-uri>.json` at the start of every turn.

**IR-IN-005** — The framework MUST read the on-disk content of the three SHA-tracked files at every turn for SHA recomputation.

### Outbound (IR-OUT)

**IR-OUT-001** — WHEN the sentinel is absent or its `uri` does not match the current session the framework SHALL emit the prompt "Which project?" to the user channel.

**IR-OUT-002** — WHEN bind completes successfully the framework SHALL emit a load-confirmation anchor naming the bound project to the user channel.

**IR-OUT-003** — The framework MUST write the sentinel JSON to `chief-of-droids/.sessions/<urlencoded-uri>.json` on bind and on every SHA update.

**IR-OUT-004** — IF any of the three required bind files fails to load THEN the framework SHALL emit a halt-error message naming the missing file to the user channel.

## Data Requirements

### Data Requirements (DR)

**DR-001** — Sentinel record

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|
| `uri` | string | REQUIRED UNIQUE | Session identifier from `recent_chats[0]`; used as the sentinel filename component. |
| `project` | string | REQUIRED | Selected project name; corresponds to a directory under `chief-of-droids/`. |
| `loaded_at` | timestamp | REQUIRED | ISO 8601 timestamp of the bind. |
| `workspace_md_sha` | string | REQUIRED | SHA of `chief-of-droids/CLAUDE.md` at load. |
| `project_md_sha` | string | REQUIRED | SHA of `<project>/CLAUDE.md` at load. |
| `brief_sha` | string | REQUIRED | SHA of `<project>/brief.md` at load. |
| `resolved_skills` | array<resolved_skill> | REQUIRED | Skills resolution map populated at bind; see DR-002. Lifecycle: rewritten on each bind. |

**DR-002** — resolved_skill element

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|
| `trigger` | string | REQUIRED | Trigger phrase declared in a SKILL.md. |
| `skill` | string | REQUIRED | Skill identifier (folder name or canonical ID) the trigger resolves to. |
| `tier` | enum(`workspace`,`project`) | REQUIRED | Tier in which the resolved skill lives. |

### Transformation Requirements (TR)

**TR-001** — Sentinel path derivation

| Input | Rule | Output |
|:--|:--|:--|
| `recent_chats[0].uri` (string) | URL-encode the URI, then prepend `chief-of-droids/.sessions/`, append `.json` | `chief-of-droids/.sessions/<urlencoded-uri>.json` |

**TR-002** — SHA computation for tracked files

| Input | Rule | Output |
|:--|:--|:--|
| File content of `chief-of-droids/CLAUDE.md` | Compute SHA digest | `workspace_md_sha` |
| File content of `<project>/CLAUDE.md` | Compute SHA digest | `project_md_sha` |
| File content of `<project>/brief.md` | Compute SHA digest | `brief_sha` |

**TR-003** — Skill resolution map derivation

| Input | Rule | Output |
|:--|:--|:--|
| Workspace skills set (`chief-of-droids/skills/`) and project skills set (`<project>/skills/`) | For each declared trigger across both sets, select the workspace-tier mapping when present; otherwise the project-tier mapping. Trigger phrases are corpus-disjoint by CON-011, so collisions cannot occur at runtime. | `resolved_skills` — array of `{trigger, skill, tier}` records |

## Non-Functional Requirements

**NFR-001** — The framework SHOULD achieve a skill-routing reliability of approximately 92–93%. | Measurement: ratio of correct trigger→skill resolutions over total resolutions ≥ 92% across a representative session corpus.

**NFR-002** — N/A — substrate silent on Performance (latency, throughput).

**NFR-003** — Layer 1 (Claude Desktop Project Instructions) content SHOULD be minimal but sufficient — limited to bootstrap dispatcher logic, per-turn sentinel verification rule, and always-on tool routing. | Measurement: TBD — substrate states the principle but does not provide a quantitative token-budget threshold.

## Security

N/A — substrate silent on Security. Warning emitted.

The substrate addresses none of the closed-enumeration categories (authentication, authorization, encryption, audit logging, rate limiting, input validation). Governance via PR-to-workspace and the no-runtime-override rule are scoped as CON-014 per the SEC exclusion list.

## Constraints

**CON-001** — The framework SHALL comprise three architectural layers occupying the slots: Layer 1 (Dispatcher) in Claude Desktop Project Instructions; Layer 2 (Workspace) in `chief-of-droids/CLAUDE.md` plus `skills/`; Layer 3 (Project) in `chief-of-droids/<project>/CLAUDE.md` plus `skills/`, `rules/`, and `brief.md`.

**CON-002** — Layer 1 (Project Instructions) SHALL contain only the bootstrap dispatcher logic, the per-turn sentinel verification rule, and always-on tool routing.

**CON-003** — Substantive content — conventions, project context, skill manifests, capability protocols — SHALL reside in Layer 2 and Layer 3 CLAUDE.md files.

**CON-004** — Always-on tools (filesystem, git, fetch) SHALL be routed at Layer 1.

**CON-005** — Project-specific tool routing SHALL be declared at Layer 3.

**CON-006** — User project selection SHALL occur once per session at the first turn; no default project SHALL be assumed.

**CON-007** — Sentinel files SHALL reside at `chief-of-droids/.sessions/<urlencoded-uri>.json`.

**CON-008** — The project brief SHALL reside at `<project>/brief.md`.

**CON-009** — The project brief SHALL carry mobile session state and context and SHALL be distinct in role from the project CLAUDE.md, which carries stable conventions and rules.

**CON-010** — The framework's reliability budget SHALL be spent in priority order: mechanical checks first, once-per-session behaviors second, behavioral rules as backup only.

**CON-011** — Trigger phrases SHALL be disjoint by name and phrase between workspace and project skill sets.

**CON-012** — Composition between skill tiers SHALL be one-way: workspace skills SHALL NOT reference project skills.

**CON-013** — Negative skill triggers SHALL be respected with the same workspace-first precedence as positive triggers.

**CON-014** — The governance escape hatch SHALL be a workspace-PR mechanism; runtime overrides of workspace skills SHALL NOT be permitted.

## Error Handling

**ERR-001** — IF reading the sentinel does not complete successfully THEN the framework SHALL surface the read error and treat the session as unbound. → FR-001

**ERR-002** — IF the user-prompt solicitation does not return a project answer THEN the framework SHALL halt and refrain from binding. → FR-002

**ERR-003** — IF any of the three required bind files does not load successfully THEN the framework SHALL halt with a clear error identifying the missing file. → FR-003

**ERR-004** — IF writing the sentinel does not complete successfully THEN the framework SHALL surface the write error and treat the session as unbound. → FR-004

**ERR-006** — IF a SHA comparison does not complete successfully THEN the framework SHALL surface the comparison error and treat the tracked content as out-of-date. → FR-006

**ERR-007** — IF reload-on-mismatch does not complete successfully THEN the framework SHALL halt with a clear error identifying the file that failed to reload. → FR-007

**ERR-009** — IF population of `resolved_skills` does not complete successfully THEN the framework SHALL halt the bind with a clear error. → FR-009

**ERR-010** — IF the corpus-wide trigger collision scan detects a conflict THEN the framework SHALL hard-reject the skill authoring with a conflict diagnostic naming the conflicting trigger and both skills. → FR-010

**ERR-011** — IF the major version bump cannot be applied THEN the framework SHALL hard-reject the trigger edit. → FR-011

**ERR-012** — IF a workspace skill removal is attempted while at least one project references that skill THEN the framework SHALL reject the removal and enumerate the referencing projects. → FR-012

**ERR-013** — IF the author does not respond to the workspace-promotion prompt THEN the framework SHALL proceed with project-skill authoring and emit a Warning. → FR-013

## Observability

N/A — substrate silent on Observability. Warning emitted.

The substrate addresses none of the closed-enumeration categories (metric exposure, structured log emission with retention, distributed trace span, health endpoint, alert threshold). The load-confirmation anchor is scoped to IR-OUT-002; tracked SHAs are scoped to DR-001; halt-error messages are scoped to ERR.

## Acceptance Criteria

**FR-001**
- AC: At every turn, before any other processing, the framework attempts a filesystem read of `chief-of-droids/.sessions/<urlencoded(recent_chats[0].uri)>.json`.

**FR-002**
- AC: When the sentinel is absent, the next user-channel message is the literal string `Which project?`.
- AC: When the sentinel exists but its `uri` field differs from `recent_chats[0].uri`, the next user-channel message is the literal string `Which project?`.

**FR-003**
- AC: After a positive user answer naming `<project>`, three filesystem reads have occurred for `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, and `chief-of-droids/<project>/brief.md`.

**FR-004**
- AC: After successful bind, `chief-of-droids/.sessions/<urlencoded-uri>.json` exists and parses as JSON containing the seven fields specified in DR-001 with REQUIRED satisfied.

**FR-005**
- AC: After successful bind, the user channel contains one anchor line that names the bound project.

**FR-006**
- AC: For each turn after bind, three SHA computations occur over the three tracked files and three field-level comparisons against the sentinel values are recorded.

**FR-007**
- AC: Given a tracked file whose on-disk content has changed since bind, after the turn the corresponding sentinel SHA equals the freshly computed SHA of the on-disk file.

**FR-008**
- AC: For a turn with no SHA mismatch, no framework-emitted output precedes the response to the user request.

**FR-009**
- AC: After bind, the sentinel `resolved_skills` array contains one record per registered skill across both tiers, each carrying `trigger`, `skill`, `tier`.

**FR-010**
- AC: Given a workspace skill set and a project skill set that share a trigger phrase, an authoring attempt that would introduce the collision is rejected before the SKILL.md is committed.

**FR-011**
- AC: A commit that changes the trigger phrase of a workspace skill is accompanied by a version-metadata update that increments the major version segment.

**FR-012**
- AC: An attempt to remove a workspace skill referenced by any project produces a rejection diagnostic and does not delete the skill files.

**FR-013**
- AC: On a new SKILL.md creation under `<project>/skills/`, the authoring flow surfaces the prompt "Could this be a workspace skill?" before the SKILL.md is committed.

**IR-IN-001**
- AC: Each turn, the framework accesses `recent_chats[0].uri` exactly once for sentinel keying.

**IR-IN-002**
- AC: A user reply containing exactly one token matching an existing `chief-of-droids/<project>/` directory satisfies the project-selection input contract.

**IR-IN-003**
- AC: The three filesystem reads at bind target paths matching `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, and `chief-of-droids/<project>/brief.md`.

**IR-IN-004**
- AC: Each turn, the framework reads the sentinel JSON file at the URL-encoded path before any other action.

**IR-IN-005**
- AC: Each turn, the framework reads the three tracked files' on-disk content for SHA recomputation when sentinel verify is active.

**IR-OUT-001**
- AC: The prompt `Which project?` appears on the user channel only when the sentinel is absent or its `uri` does not match.

**IR-OUT-002**
- AC: The load-confirmation anchor appears on the user channel only after the three bind reads and the sentinel write have completed.

**IR-OUT-003**
- AC: After bind, the sentinel JSON exists at the URL-encoded path; after any SHA update, the file's `loaded_at` or relevant SHA field has been rewritten.

**IR-OUT-004**
- AC: When any bind read fails, the user channel contains a halt-error message naming the failing file path.

**DR-001**
- AC: Sentinel JSON parses and contains all seven REQUIRED fields with matching types; `uri` is unique across the `.sessions/` directory.

**DR-002**
- AC: Each `resolved_skills` element parses as `{trigger: string, skill: string, tier: "workspace" | "project"}`; non-conforming records cause sentinel verify to fail.

**TR-001**
- AC: Given URI `u`, the derived path equals `chief-of-droids/.sessions/<urlencode(u)>.json` for any URL-encoded representation defined by the encoder.

**TR-002**
- AC: Given identical input file content, the SHA outputs are byte-identical across runs.

**TR-003**
- AC: For every trigger present in the workspace skills set, the resolved record's `tier` is `workspace`; for every trigger present only in a project skills set, the resolved record's `tier` is `project`.

**NFR-001**
- AC: Over a representative corpus of trigger-bearing user prompts, the framework resolves to the correct skill in ≥ 92% of cases.

**NFR-002**
- AC: N/A — no verifiable condition derivable from substrate.

**NFR-003**
- AC: Layer 1 content can be enumerated and shown to contain only the three permitted concerns (dispatcher, sentinel verify rule, always-on tool routing). Quantitative budget — TBD.

**CON-001**
- AC: Inspection of Project Instructions, `chief-of-droids/CLAUDE.md`, and `<project>/CLAUDE.md` shows the layer-to-slot mapping in the §Architecture table.

**CON-002**
- AC: Project Instructions, when read in full, contains exactly the three permitted concerns and no other substantive content.

**CON-003**
- AC: Project Instructions contains no conventions, project context, skill manifest, or capability protocol; those concerns appear in Layer 2 / Layer 3 CLAUDE.md files.

**CON-004**
- AC: Project Instructions contains explicit routing declarations for filesystem, git, and fetch.

**CON-005**
- AC: Each project's Layer 3 CLAUDE.md declares the project-specific tools it relies on; Layer 1 does not.

**CON-006**
- AC: At bootstrap, the framework prompts the user for project selection and binds only after a user answer; no implicit default is bound.

**CON-007**
- AC: Sentinel files appear under `chief-of-droids/.sessions/` with filenames `<urlencoded-uri>.json`.

**CON-008**
- AC: Each project directory under `chief-of-droids/` contains a `brief.md` file.

**CON-009**
- AC: In each project, the CLAUDE.md content scope (conventions, rules) and the brief.md content scope (state, context) do not overlap.

**CON-010**
- AC: Framework design and skill specifications reflect the priority order — mechanical checks > once-per-session behaviors > behavioral rules.

**CON-011**
- AC: A corpus-wide scan over workspace and project skill sets returns no shared trigger phrase.

**CON-012**
- AC: A corpus-wide scan of workspace SKILL.md files returns no references to project-level skills.

**CON-013**
- AC: For any trigger phrase declared as negative in a workspace skill, the same trigger phrase in any project skill is overridden by the workspace declaration.

**CON-014**
- AC: Workspace governance documentation specifies that workspace changes proceed via PR; no documented runtime-override mechanism exists.

**ERR-001**
- AC: Given a filesystem error on sentinel read, the framework surfaces the error and treats the session as unbound (no project context loaded).

**ERR-002**
- AC: Given no user answer to the project prompt within the turn, the framework halts without writing a sentinel.

**ERR-003**
- AC: Given any one of the three bind reads failing, the user channel contains a halt-error message naming the failing file and no sentinel is written.

**ERR-004**
- AC: Given a filesystem error on sentinel write, the framework surfaces the error and treats the session as unbound.

**ERR-006**
- AC: Given a SHA computation or comparison failure, the framework surfaces the error and treats the tracked content as out-of-date.

**ERR-007**
- AC: Given a reload-on-mismatch read failure, the user channel contains a halt-error message naming the file that failed to reload.

**ERR-009**
- AC: Given a failure to populate `resolved_skills`, the framework halts the bind with a clear error.

**ERR-010**
- AC: Given a trigger collision detected by the scan, the authoring rejection diagnostic names the conflicting trigger phrase and both skills.

**ERR-011**
- AC: Given a failed attempt to bump major version on a workspace skill trigger edit, the trigger edit is rejected and the workspace skill files are unchanged.

**ERR-012**
- AC: Given a removal attempt against a workspace skill referenced by ≥ 1 project, the rejection diagnostic enumerates the referencing project names.

**ERR-013**
- AC: Given no author response to the workspace-promotion prompt, the project-skill authoring proceeds and a Warning is logged.

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
| IR-IN-001 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-002 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-003 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-004 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-005 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-001|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-002|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-003|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-004|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| DR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| DR-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| TR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| TR-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| TR-003    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| NFR-001   |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
| NFR-002   |  N/A   |     N/A     |    N/A     |     ✓     |   N/A   |
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
| CON-013   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-014   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-001   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-002   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-003   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-004   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-006   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-007   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-009   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-010   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-011   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-012   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-013   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
