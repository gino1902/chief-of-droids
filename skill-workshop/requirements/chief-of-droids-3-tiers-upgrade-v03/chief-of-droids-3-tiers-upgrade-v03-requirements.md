# Two-Tier CLAUDE.md Architecture — Design Notes

## Purpose

Define a two-tier (workspace + project) CLAUDE.md architecture for the chief-of-droids framework running in Claude Desktop chat, with a minimal dispatcher slot at Project Instructions (Layer 1). The design eliminates preamble duplication between Project Instructions and workspace CLAUDE.md, resolves category errors where Code-style override semantics were declared in a Chat environment, and provides instructional protocols for six capabilities that Claude Code supplies natively but Claude Desktop chat does not: skills routing, session hygiene, git versioning, available tools, project brief loading, and conditional rules by file type.

---

## Scope

### In Scope

- Three-layer slot model: Layer 1 (Project Instructions dispatcher), Layer 2 (`chief-of-droids/CLAUDE.md` + `chief-of-droids/skills/`), Layer 3 (`chief-of-droids/<project>/CLAUDE.md` + project `skills/`, `rules/`, and `brief.md`).
- Bootstrap protocol with per-turn sentinel verification keyed on `recent_chats[0].uri`.
- Sentinel record schema persisted at `chief-of-droids/.sessions/<urlencoded-uri>.json` and loaded on every turn.
- SHA-based drift detection for workspace CLAUDE.md, project CLAUDE.md, and project brief, with on-mismatch reload.
- Skills routing with workspace-tier precedence over project-tier, enforced by authoring-time corpus-wide trigger collision scan.
- One-way composition between tiers — project skills may reference workspace skills, not the reverse.
- Major-version bump rule for workspace skill trigger edits; removal block for workspace skills referenced by project skills.
- Always-on tool routing (filesystem, git, fetch) at Layer 1 and project-specific tool routing at Layer 3.
- Governance escape hatch via workspace pull request (not runtime override).
- Project brief loaded alongside project CLAUDE.md at bind, with SHA tracked in sentinel.

### Out of Scope

- MCP server registration in `claude_desktop_config.json` — outside the framework's control.
- Drift prevention via description-as-source-of-truth replication ("Option 1") — deferred until skill count exceeds ~25, a second author joins, or dispatcher matures.
- Session identity mechanism beyond using `recent_chats[0].uri` — parked in `docs/session-identity-recommendation.md`.
- Fate of workspace-level CLAUDE.md as a structural element (dissolve / duplicate per project / layer below project CLAUDE.md) — undecided.
- Project brief content schema and format — free-form markdown for now; conventions undecided.
- Per-capability detailed designs for session hygiene protocol, git versioning protocol, and conditional rules format.
- Audit of existing workspace CLAUDE.md and Project Instructions for "behavioral primary" rules to be moved to mechanical or once-per-session enforcement.
- Rollout strategy and pilot project selection.

---

## Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| Framework operator (user) | Selects project at session bind; authors and edits CLAUDE.md, brief, and skill files | user |
| Claude Desktop client | Provides Project Instructions slot, `recent_chats[0].uri` source, and registered MCP servers | upstream |
| Filesystem MCP server | Reads workspace CLAUDE.md, project CLAUDE.md, project brief, SKILL.md files, and sentinel JSON; writes sentinel JSON | upstream |
| Git MCP server | Versions workspace and project content; carries governance via pull request | downstream |
| `creating-skills` skill | Executes corpus-wide trigger collision scan at authoring time; enforces workspace-vs-project disjoint triggers | downstream |
| Workspace skills (Layer 2) | Loaded at Layer 2 scope; subject to major version bump on trigger edit and removal block while project references exist | downstream |
| Project skills (Layer 3) | Loaded at Layer 3 scope; may reference workspace skills (one-way) | downstream |

---

## Glossary

| Term | Definition | Status |
|:--|:--|:--|
| Layer 1 | Dispatcher slot held by Claude Desktop Project Instructions; carries bootstrap dispatcher logic, per-turn sentinel verification, and always-on tool routing | substrate |
| Layer 2 | Workspace tier; `chief-of-droids/CLAUDE.md` and `chief-of-droids/skills/`; carries cross-project conventions and shared skills | substrate |
| Layer 3 | Project tier; `chief-of-droids/<project>/CLAUDE.md`, `<project>/skills/`, `<project>/rules/`, and `<project>/brief.md`; carries project conventions, instructional protocols, and project state | substrate |
| Project Instructions | Claude Desktop slot that holds Layer 1 content and is read by Claude on every prompt | auto-derived — verify |
| Sentinel | Per-session JSON record at `chief-of-droids/.sessions/<urlencoded-uri>.json` recording the bind state (uri, project, file SHAs, resolved_skills) | auto-derived — verify |
| Bootstrap protocol | Per-turn sequence executed by Layer 1 that reads the sentinel, loads or reuses the CLAUDE.md hierarchy, and verifies SHA freshness | auto-derived — verify |
| Project brief | `chief-of-droids/<project>/brief.md` file holding project state and context, loaded at bind alongside project CLAUDE.md | substrate |
| Always-on tools | Filesystem, git, and fetch MCP servers routed at Layer 1 for every session | substrate |
| Workspace tier | Synonym for Layer 2 scope | auto-derived — verify |
| Project tier | Synonym for Layer 3 scope | auto-derived — verify |
| `recent_chats[0].uri` | Field exposed by Claude Desktop identifying the active chat session | auto-derived — verify |
| `creating-skills` | Authoring-time skill that performs corpus-wide trigger collision scan and enforces workspace-vs-project disjoint trigger phrases | auto-derived — verify |
| `workspace_md_sha` | Sentinel field — SHA of workspace CLAUDE.md captured at load | auto-derived — verify |
| `project_md_sha` | Sentinel field — SHA of project CLAUDE.md captured at load | auto-derived — verify |
| `brief_sha` | Sentinel field — SHA of project brief captured at load | auto-derived — verify |
| `resolved_skills` | Sentinel field — array of `{trigger, skill, tier}` entries resolved at bind | auto-derived — verify |
| Registration | MCP server availability defined in `claude_desktop_config.json` outside the framework's control | substrate |
| Routing | Layer-level declaration of which tools are scoped at which tier (Layer 1 universal vs Layer 3 project-specific) | substrate |
| Usage | Skill-level invocation of tools as described per SKILL.md | substrate |

---

## Functional Requirements

**FR-001** — WHEN a user turn begins, the framework SHALL read the sentinel keyed on `recent_chats[0].uri`.

**FR-002** — IF the sentinel is absent or the uri does not match, the framework SHALL prompt the user with `"Which project?"`. (no ERR — rationale: substrate prescribes wait-on-user with no enforced timeout failure path)

**FR-003** — WHEN the user provides a project choice, the framework SHALL load `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, and `chief-of-droids/<project>/brief.md`.

**FR-004** — WHEN all three files load successfully, the framework SHALL write the sentinel populated with the current `uri`, `project`, `loaded_at`, `workspace_md_sha`, `project_md_sha`, `brief_sha`, and `resolved_skills`.

**FR-005** — WHEN the sentinel write completes, the framework SHALL emit an anchor message to the user channel confirming load.

**FR-006** — WHEN a turn begins with sentinel present and uri matching, the framework SHALL compare `workspace_md_sha`, `project_md_sha`, and `brief_sha` against the corresponding disk SHAs.

**FR-007** — IF a SHA mismatch is detected, the framework SHALL reload the affected file from disk.

**FR-008** — WHEN a file is reloaded due to SHA mismatch, the framework SHALL update the corresponding SHA field in the sentinel.

**FR-009** — WHILE the sentinel is valid and all SHAs match disk, the framework SHALL proceed silently to the user request.

**FR-010** — WHEN a skill routing query is resolved at runtime, the framework SHALL select the workspace-tier match if one exists, without inspecting project-tier matches.

**FR-011** — WHEN `creating-skills` runs, the framework SHALL execute a corpus-wide trigger collision scan over all workspace and project SKILL.md files.

**FR-012** — IF the corpus-wide trigger collision scan detects a workspace–project trigger collision, `creating-skills` SHALL reject the authoring operation.

**FR-013** — WHEN a workspace skill's trigger phrase is edited, the framework SHALL increment the major segment of that workspace skill's version.

**FR-014** — IF a project skill references a workspace skill, the framework SHALL block any removal operation targeting that workspace skill.

**FR-015** — WHEN a new project-tier skill is authored, `creating-skills` SHALL prompt the author `"could this be a workspace skill?"` before committing. (no ERR — rationale: substrate prescribes an informational prompt with no enforced failure path)

---

## Interface Requirements

### Inbound (IR-IN)

**IR-IN-001** — The framework MUST accept user-supplied input identifying the project name at bootstrap when no valid sentinel exists for the current uri.

**IR-IN-002** — The framework MUST accept filesystem reads of `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, `chief-of-droids/<project>/brief.md`, and `chief-of-droids/.sessions/<urlencoded-uri>.json`.

**IR-IN-003** — The framework MUST accept the session identifier from the `recent_chats[0].uri` source exposed by Claude Desktop.

### Outbound (IR-OUT)

**IR-OUT-001** — The framework MUST emit the prompt `"Which project?"` to the user channel when no valid sentinel exists for the current uri.

**IR-OUT-002** — The framework MUST emit an anchor confirmation message to the user channel upon successful bind.

**IR-OUT-003** — The framework MUST emit a clear error message identifying the failing step to the user channel when any bind step fails.

---

## Data Requirements

### Data Requirements (DR)

**DR-001** — Sentinel record (path `chief-of-droids/.sessions/<urlencoded-uri>.json`)

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|
| `uri` | string | REQUIRED UNIQUE | Session identifier from `recent_chats[0].uri`; UNIQUE within the `.sessions/` directory because the file name is derived from this value |
| `project` | string | REQUIRED | Selected project name |
| `loaded_at` | timestamp | REQUIRED | ISO-formatted timestamp of bind |
| `workspace_md_sha` | string | REQUIRED | SHA of workspace CLAUDE.md captured at load |
| `project_md_sha` | string | REQUIRED | SHA of project CLAUDE.md captured at load |
| `brief_sha` | string | REQUIRED | SHA of project brief captured at load |
| `resolved_skills` | array | REQUIRED | Array of `{trigger, skill, tier}` objects resolved at bind |

### Transformation Requirements (TR)

**TR-001** — Sentinel path derivation

| Input | Rule | Output |
|:--|:--|:--|
| Session uri value from `recent_chats[0].uri` | URL-encode the uri, prefix with `chief-of-droids/.sessions/`, suffix with `.json` | Sentinel filesystem path |

**TR-002** — File SHA computation

| Input | Rule | Output |
|:--|:--|:--|
| File byte content of workspace CLAUDE.md, project CLAUDE.md, or project brief | Apply the SHA hash function over the file bytes (algorithm not specified in substrate) | SHA value stored in the corresponding sentinel field at load, or compared against the stored SHA on later turns |

---

## Non-Functional Requirements

**NFR-001** — The framework SHOULD achieve workspace-vs-project skill routing reliability within the design's projected band. | Measurement: ≥ 92% collision-free skill-trigger resolutions over a representative chat corpus.

**NFR-002** — N/A — substrate silent on performance. Warning emitted.

**NFR-003** — The Project Instructions slot (Layer 1) SHOULD remain minimal — bootstrap dispatcher logic, per-turn sentinel verification, and always-on tool routing only. | Measurement: TBD (token budget threshold not specified in substrate).

---

## Security

N/A — substrate silent on Security. Warning emitted.

---

## Constraints

**CON-001** — The Project Instructions slot (Layer 1) SHALL contain only bootstrap dispatcher logic, per-turn sentinel verification, and always-on tool routing declarations.

**CON-002** — Substantive content (conventions, project context, skill manifests, protocols) SHALL reside in workspace and project CLAUDE.md files, not in Project Instructions.

**CON-003** — The workspace tier SHALL comprise `chief-of-droids/CLAUDE.md` and `chief-of-droids/skills/`.

**CON-004** — Each project tier SHALL comprise `chief-of-droids/<project>/CLAUDE.md`, `chief-of-droids/<project>/skills/`, `chief-of-droids/<project>/rules/`, and `chief-of-droids/<project>/brief.md`.

**CON-005** — Always-on tools (filesystem, git, fetch) SHALL be routed at Layer 1.

**CON-006** — Project-specific tools SHALL be routed at Layer 3.

**CON-007** — Workspace-tier skill matches SHALL take precedence over project-tier matches on trigger resolution.

**CON-008** — Workspace and project skill trigger phrases SHALL be disjoint by name and by phrase.

**CON-009** — Skill composition between tiers SHALL be one-way from project to workspace.

**CON-010** — Workspace skills SHALL NOT reference project skills.

**CON-011** — Negative-trigger resolution SHALL follow the same workspace-wins precedence direction as positive-trigger resolution.

**CON-012** — Each project directory SHALL declare a `brief.md` file at `chief-of-droids/<project>/brief.md`.

**CON-013** — Governance overrides SHALL be implemented as workspace-level pull requests, not as runtime overrides in the dispatcher or project files.

---

## Error Handling

**ERR-001** — IF read of the sentinel does not complete successfully THEN the framework SHALL surface a clear error and halt the turn. → FR-001

**ERR-002** — IF load of any of workspace CLAUDE.md, project CLAUDE.md, or project brief does not complete successfully THEN the framework SHALL surface an error identifying the failing file and halt the bind. → FR-003

**ERR-003** — IF the sentinel write does not complete successfully THEN the framework SHALL surface a clear error and abort the bind without leaving partial state. → FR-004

**ERR-004** — IF the SHA comparison against disk does not complete successfully for a tracked file THEN the framework SHALL surface a clear error and treat the file as needing reload. → FR-006

**ERR-005** — IF the file reload does not complete successfully THEN the framework SHALL surface a clear error identifying the affected file and halt the turn. → FR-007

**ERR-006** — IF the sentinel SHA-field update does not complete successfully THEN the framework SHALL surface a clear error and retain the prior sentinel state. → FR-008

**ERR-007** — IF the corpus-wide trigger collision scan does not complete successfully THEN `creating-skills` SHALL reject the authoring operation. → FR-011

**ERR-008** — IF the major-version bump does not complete successfully THEN the framework SHALL block persistence of the workspace skill trigger edit. → FR-013

---

## Observability

N/A — substrate silent on Observability. Warning emitted.

---

## Acceptance Criteria

**FR-001**
- AC: Given a turn begins, the framework attempts a filesystem read at the sentinel path derived from the current `recent_chats[0].uri` prior to any other bootstrap step.

**FR-002**
- AC: Given the sentinel is absent or the uri does not match, the framework emits `"Which project?"` to the user channel.

**FR-003**
- AC: Given the user provides a project name, the framework reads `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, and `chief-of-droids/<project>/brief.md` and completes all three reads before any sentinel write.

**FR-004**
- AC: Given the three files load successfully, the sentinel JSON file is written with all seven fields populated (`uri`, `project`, `loaded_at`, `workspace_md_sha`, `project_md_sha`, `brief_sha`, `resolved_skills`).

**FR-005**
- AC: Given the sentinel write completes, an anchor message confirming load appears in the user channel within the same turn.

**FR-006**
- AC: Given a turn begins with a valid sentinel, the framework computes the disk SHA for each of workspace CLAUDE.md, project CLAUDE.md, and project brief, and compares each against the stored sentinel value.

**FR-007**
- AC: Given a SHA mismatch is detected for one tracked file, the framework re-reads that file from disk in the same turn.

**FR-008**
- AC: Given a file is reloaded due to SHA mismatch, the corresponding SHA field in the sentinel is updated to the new value.

**FR-009**
- AC: Given the sentinel is valid and all SHAs match disk, the framework emits no bootstrap message and proceeds directly to the user request.

**FR-010**
- AC: Given a skill trigger that would match both a workspace and a project skill, the framework resolves to the workspace skill without evaluating the project skill.

**FR-011**
- AC: Given `creating-skills` is invoked, a read of all workspace and project SKILL.md files is performed and trigger phrases are collected for collision evaluation.

**FR-012**
- AC: Given the scan detects a workspace–project trigger phrase collision, `creating-skills` exits non-zero without authoring the offending skill.

**FR-013**
- AC: Given a workspace skill's trigger phrase changes between two commits, the workspace skill's manifest version's major segment is incremented.

**FR-014**
- AC: Given any project skill references a workspace skill, a remove operation on that workspace skill is rejected.

**FR-015**
- AC: Given a new project-tier skill is being authored, `creating-skills` emits the `"could this be a workspace skill?"` prompt before commit.

**IR-IN-001**
- AC: Given a `"Which project?"` prompt, the framework accepts a user-supplied project name and proceeds to the load step.

**IR-IN-002**
- AC: Given the bind step requests workspace CLAUDE.md, project CLAUDE.md, brief.md, and sentinel JSON, each filesystem read returns content (or a clear error).

**IR-IN-003**
- AC: Given a session, the framework reads `recent_chats[0].uri` and uses it as the session identifier in subsequent sentinel operations.

**IR-OUT-001**
- AC: Given sentinel absent or uri mismatch, `"Which project?"` appears in the user channel.

**IR-OUT-002**
- AC: Given a successful bind, an anchor confirmation message appears in the user channel.

**IR-OUT-003**
- AC: Given any bind step failure, an error message identifying the failing step appears in the user channel.

**DR-001**
- AC: A sentinel file conforms to the schema — all seven REQUIRED fields are present, `uri` is UNIQUE within `.sessions/` (enforced by file-name derivation), and field types match the table.

**TR-001**
- AC: Given input uri `https://claude.ai/chat/abc-123`, the output path is `chief-of-droids/.sessions/https%3A%2F%2Fclaude.ai%2Fchat%2Fabc-123.json`.

**TR-002**
- AC: Given the same file byte content, two SHA computations produce the same SHA value (deterministic). Algorithm choice is verified once during implementation freeze.

**NFR-001**
- AC: Across a representative chat corpus, the rate of collision-free skill-trigger resolutions is ≥ 92%.

**NFR-002**
- AC: N/A — no verifiable condition derivable from substrate.

**NFR-003**
- AC: N/A — no quantitative threshold defined; measurement TBD.

**CON-001**
- AC: Static inspection of the Project Instructions content reveals only bootstrap dispatcher logic, per-turn sentinel verification rule, and always-on tool routing — no convention text, project context, skill manifests, or other protocol bodies.

**CON-002**
- AC: Static inspection confirms cross-project conventions reside in `chief-of-droids/CLAUDE.md` and project conventions reside in `<project>/CLAUDE.md`; none of those bodies are duplicated in Project Instructions.

**CON-003**
- AC: Static inspection confirms the workspace tier consists of `chief-of-droids/CLAUDE.md` and `chief-of-droids/skills/`.

**CON-004**
- AC: Static inspection confirms each project directory contains `CLAUDE.md`, `skills/`, `rules/`, and `brief.md`.

**CON-005**
- AC: Static inspection of Project Instructions confirms filesystem, git, and fetch tool routing declarations.

**CON-006**
- AC: Static inspection of `<project>/CLAUDE.md` confirms project-specific tool declarations are scoped to that project.

**CON-007**
- AC: Static inspection of the dispatcher resolution logic confirms workspace-tier matches return before any project-tier evaluation.

**CON-008**
- AC: Static inspection of the union of workspace and project SKILL.md trigger phrases confirms no exact-match overlap on name or phrase.

**CON-009**
- AC: Static inspection of skill cross-references confirms only project-to-workspace references exist.

**CON-010**
- AC: Static scan of workspace skill bodies confirms no path or symbol reference to any project-tier skill.

**CON-011**
- AC: Static inspection of dispatcher logic confirms negative-trigger evaluation follows the same workspace-first rule.

**CON-012**
- AC: Static inspection confirms `brief.md` exists in every project directory enumerated under the workspace.

**CON-013**
- AC: Static inspection confirms no runtime override path exists in dispatcher or skill resolution logic that bypasses workspace authority.

**ERR-001**
- AC: Given a filesystem read of the sentinel returns an error, a clear error message appears in the user channel and the turn is halted.

**ERR-002**
- AC: Given any of the three file loads returns an error, an error message identifying the failing file appears in the user channel and the bind is halted.

**ERR-003**
- AC: Given the sentinel write returns an error, a clear error appears in the user channel, the bind is aborted, and no partial sentinel state is left on disk.

**ERR-004**
- AC: Given SHA computation against disk returns an error for a tracked file, a clear error appears in the user channel and the file is treated as needing reload.

**ERR-005**
- AC: Given a SHA-driven reload returns an error, a clear error identifying the affected file appears in the user channel and the turn is halted.

**ERR-006**
- AC: Given the sentinel SHA-field update returns an error, the prior sentinel state is retained and a clear error appears in the user channel.

**ERR-007**
- AC: Given the corpus scan returns an error, `creating-skills` exits non-zero without committing the authoring operation.

**ERR-008**
- AC: Given the major-version bump operation returns an error, the workspace skill trigger edit is not persisted.

---

## Quality Criteria scorecard

| Criterion   | Definition |
|:--|:--|
| Atomic      | The requirement addresses exactly one behavior, constraint, or quality attribute. It contains a single modal verb (SHALL, MUST, SHOULD, MAY). |
| Unambiguous | All terms used are defined in the Glossary or are universally understood. No term is open to more than one interpretation. |
| Verifiable  | The requirement has at least one acceptance criterion — a condition that can be confirmed through testing, inspection, or measurement. |
| Traceable   | The requirement carries a valid, unique identifier (`<CAT>-NNN`) that enables cross-referencing, impact analysis, and change tracking. |
| Bounded     | For NFR-class requirements (NFR, OBS, SEC): the requirement specifies a quantitative threshold (value, time unit, percentage, or volume). N/A for all other requirement types. |

| Req ID    | Atomic | Unambiguous | Verifiable | Traceable | Bounded |
|:--|:--:|:--:|:--:|:--:|:--:|
| FR-001    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-002    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-003    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-004    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-005    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-006    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-007    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-008    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-009    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-010    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-011    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-012    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-013    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-014    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| FR-015    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| IR-IN-001 |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| IR-IN-002 |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| IR-IN-003 |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| IR-OUT-001|   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| IR-OUT-002|   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| IR-OUT-003|   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| DR-001    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| TR-001    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| TR-002    |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| NFR-001   |   ✓   |   ✓   |   ✓   |   ✓   |   ✓   |
| NFR-002   |  N/A  |  N/A  |   ✗   |   ✓   |   ✗   |
| NFR-003   |   ✓   |   ✓   |   ✗   |   ✓   |   ✗   |
| CON-001   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-002   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-003   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-004   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-005   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-006   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-007   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-008   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-009   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-010   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-011   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-012   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| CON-013   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| ERR-001   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| ERR-002   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| ERR-003   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| ERR-004   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| ERR-005   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| ERR-006   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| ERR-007   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |
| ERR-008   |   ✓   |   ✓   |   ✓   |   ✓   |  N/A  |

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
