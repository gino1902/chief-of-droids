# Two-Tier CLAUDE.md Architecture — Design Notes

## Purpose

This component proposes a two-tier CLAUDE.md architecture spanning three layers — Layer 1 dispatcher in Claude Desktop Project Instructions, Layer 2 workspace (`chief-of-droids/CLAUDE.md` + shared skills), and Layer 3 project (`<project>/CLAUDE.md` + project skills, rules, brief) — for the chief-of-droids framework operating in Claude Desktop chat. The design resolves duplications observed between Project Instructions and workspace CLAUDE.md (preamble rules, citation enforcement, skill loading procedure, override language, maintenance section) and resolves category errors arising from Claude Code-style override semantics declared in a Chat environment where no native override mechanism exists. It mirrors Claude Code patterns by implementing — via instruction — the six native capabilities (skills routing, session hygiene, git versioning, available tools, project brief route, conditional rules by file type) that Claude Desktop does not provide.

## Scope

### In Scope

- Two-tier architecture spanning Layer 1 (Project Instructions dispatcher), Layer 2 (workspace `CLAUDE.md` + `skills/`), and Layer 3 (`<project>/CLAUDE.md` + `skills/` + `rules/` + `brief.md`).
- Bootstrap protocol with per-turn sentinel verification (single-predicate-per-turn pattern; no separate session-start phase).
- Sentinel record schema, file location, and lifecycle (`uri`, `project`, `loaded_at`, `workspace_md_sha`, `project_md_sha`, `brief_sha`, `resolved_skills`).
- Project brief loading at project bind alongside project `CLAUDE.md`; SHA tracking; mid-session edit triggers reload.
- Skills routing precedence rule (workspace tier wins) implemented via authoring-time hard reject on trigger collision.
- Sentinel-recorded resolution map (`{trigger, skill, tier}`) populated on project bind.
- Always-on tool routing at Layer 1; project-specific tool routing at Layer 3.
- Workspace-skill versioning rules (major bump on trigger edit) and removal-blocking rules (blocked while any project references the skill).
- Composition direction between tiers (one-way; workspace cannot reference project skills).
- Negative-trigger precedence aligned with the workspace-wins direction.
- Reliability principle prioritising mechanical checks over behavioural rules.

### Out of Scope

- Session identity mechanism (parked: companion document `docs/session-identity-recommendation.md`).
- Fate of workspace-level `CLAUDE.md` — dissolve / duplicate per project / layer below project `CLAUDE.md` (undecided).
- Project brief content schema and format (free-form markdown for now; conventions undecided).
- Per-capability design for: session hygiene protocol, git versioning protocol, conditional rules format.
- Audit of existing workspace `CLAUDE.md` and Project Instructions for "behavioural primary" rules that could be moved to mechanical or once-per-session enforcement.
- Rollout strategy (pilot one project before adopting framework-wide).
- Drift prevention via description-as-source-of-truth replication ("Option 1") — deferred pending trigger conditions (skill count >~25, second author joins, or dispatcher matures enough for incremental adoption).
- Tool registration in `claude_desktop_config.json` — outside framework control; assumed prerequisite.

## Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| Claude Desktop client | Runtime host providing chat interface and MCP registry | upstream |
| User (project owner) | Selects project on first bind; authors skills | user |
| `recent_chats[0]` API | Provides session identifier (`uri`) consumed by the bootstrap protocol | upstream |
| Workspace `CLAUDE.md` (Layer 2) | Source of cross-project conventions and shared skills, loaded at project bind | upstream |
| Project `CLAUDE.md` (Layer 3) | Source of project-specific conventions and protocols, loaded at project bind | upstream |
| Project brief (`<project>/brief.md`) | Source of project state and context, loaded at project bind | upstream |
| Project Instructions (Layer 1 / dispatcher) | Bootstrap dispatcher, sentinel verify, always-on tool routing | upstream |
| Sentinel file (`chief-of-droids/.sessions/<urlencoded-uri>.json`) | Persists bind state across turns; SHA fingerprints; resolved skills map | downstream |
| `creating-skills` skill | Enforces corpus-wide trigger collision scan at authoring time | downstream |
| Filesystem MCP server | Reads `CLAUDE.md`, project brief, sentinel; writes sentinel | downstream |
| Git MCP server | Provides explicit git protocol surface declared in project `CLAUDE.md` | downstream |
| Fetch MCP server | External URL retrieval | downstream |
| Anchor confirmation channel | User-visible bind confirmation token | user |

## Glossary

| Term | Definition | Status |
|:--|:--|:--|
| Bootstrap protocol | Per-turn sequence: read sentinel, compare uri, bind-or-verify | auto-derived — verify |
| Project bind | One-shot operation loading workspace `CLAUDE.md`, project `CLAUDE.md`, project brief; writes sentinel | auto-derived — verify |
| Sentinel | JSON record at `chief-of-droids/.sessions/<urlencoded-uri>.json` persisting per-session bind state | auto-derived — verify |
| Dispatcher | Logic carried by Layer 1 (Project Instructions) for bootstrap and per-turn verify | auto-derived — verify |
| Layer 1 | Claude Desktop Project Instructions slot | auto-derived — verify |
| Layer 2 | Workspace tier: `chief-of-droids/CLAUDE.md` and `skills/` | auto-derived — verify |
| Layer 3 | Project tier: `<project>/CLAUDE.md`, `skills/`, `rules/`, `brief.md` | auto-derived — verify |
| Workspace tier | Layer 2 in the precedence-rule context | auto-derived — verify |
| Project tier | Layer 3 in the precedence-rule context | auto-derived — verify |
| Precedence rule | Workspace tier wins on trigger collision; enforced by authoring-time hard reject | auto-derived — verify |
| Resolution map | `{trigger, skill, tier}` array recorded in sentinel on bind | auto-derived — verify |
| `resolved_skills` | Sentinel field carrying the resolution map | auto-derived — verify |
| `recent_chats[0].uri` | Session identifier read from Claude Desktop API; keys the sentinel | auto-derived — verify |
| `workspace_md_sha` / `project_md_sha` / `brief_sha` | SHA digests of bound files at load time | auto-derived — verify |
| Project brief | `<project>/brief.md` carrying project state and context; loaded at bind | auto-derived — verify |
| Anchor | User-visible token emitted on successful bind | auto-derived — verify |
| Always-on tool | Tool routed at Layer 1 and universally expected across sessions (filesystem, git, fetch) | auto-derived — verify |
| Project-specific tool | Tool routed at Layer 3, scoped to a single project | auto-derived — verify |
| Composition (one-way) | Reference direction: project may reference workspace; workspace MUST NOT reference project | auto-derived — verify |
| Negative trigger | Trigger phrase declaring "do NOT route here on phrase X" | auto-derived — verify |
| Promotion | Moving a skill from project tier to workspace tier | auto-derived — verify |
| Trigger collision | Two skills declaring overlapping trigger phrases | auto-derived — verify |
| Corpus collision scan | Mechanical scan over all skill trigger phrases performed at authoring time | auto-derived — verify |
| SHA | Cryptographic content-fingerprint digest of a file | auto-derived — verify |
| MCP | Model Context Protocol — server registration mechanism in Claude Desktop client config | auto-derived — verify |
| URI | Uniform Resource Identifier — session identifier shape returned by `recent_chats[0]` | auto-derived — verify |
| Session bind | First turn of a new session: project selection + load + sentinel write | auto-derived — verify |
| Reliability principle | Spend reliability budget on mechanical checks first, once-per-session behaviors second, behavioural rules last | auto-derived — verify |

## Functional Requirements

**FR-001** — WHEN a user turn begins the framework SHALL read the sentinel for the current session keyed on `recent_chats[0].uri`.

**FR-002** — IF the sentinel is absent or the recorded uri does not match the current `recent_chats[0].uri` THEN the framework SHALL prompt the user with "Which project?".

**FR-003** — WHEN the user supplies a project selection the framework SHALL load `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, and `chief-of-droids/<project>/brief.md`.

**FR-004** — WHEN the three bind files have been read the framework SHALL verify all three loaded successfully and halt with a clear error if any failed.

**FR-005** — WHEN load verification succeeds the framework SHALL write the sentinel with the current bind state (uri, project, loaded_at, workspace_md_sha, project_md_sha, brief_sha, resolved_skills).

**FR-006** — WHEN the sentinel write completes the framework SHALL emit an anchor confirming the bind to the user channel. (no ERR — rationale: Emit-shape; no return contract from the user channel)

**FR-007** — IF the sentinel is present and the recorded uri matches the current `recent_chats[0].uri` THEN the framework SHALL compare `workspace_md_sha`, `project_md_sha`, and `brief_sha` against SHAs computed from current on-disk content of the three bound files.

**FR-008** — IF any per-file SHA comparison reports a mismatch THEN the framework SHALL reload the mismatched file and update the corresponding SHA field in the sentinel.

**FR-009** — WHEN all three per-turn SHA comparisons match the framework SHALL proceed silently to the user request. (no ERR — rationale: pass-through; no observable failure mode distinct from upstream FR-007)

**FR-010** — WHEN the project bind step executes the framework SHALL record a `resolved_skills` array of `{trigger, skill, tier}` entries in the sentinel.

**FR-011** — WHEN a skill is created or its trigger phrase is modified the `creating-skills` skill SHALL execute a corpus-wide trigger collision scan across workspace-tier and project-tier skills.

**FR-012** — IF the corpus collision scan finds an overlap between the proposed trigger phrase and any existing trigger phrase THEN `creating-skills` SHALL hard reject the change at authoring time. (no ERR — rationale: FR is itself the rejection path; no further error contract)

**FR-013** — WHEN routing a skill invocation the dispatcher SHALL resolve the trigger against workspace-tier skills first and exit on first match before considering project-tier skills. (no ERR — rationale: Select-shape over a known set)

**FR-014** — WHEN a workspace skill's trigger phrase is edited the framework SHALL apply a major-version bump to the affected workspace skill's version metadata.

**FR-015** — IF removal of a workspace skill is requested while at least one project skill or rule references it THEN the framework SHALL block the removal. (no ERR — rationale: FR is itself the rejection path)

**FR-016** — WHEN a project-tier skill is authored the framework SHALL prompt the author with "could this be workspace?" before accepting the new project-tier skill.

## Interface Requirements

### Inbound (IR-IN)

**IR-IN-001** — The framework MUST accept the session identifier returned by `recent_chats[0].uri` from the Claude Desktop client.

**IR-IN-002** — WHEN the framework prompts "Which project?" the framework MUST accept the user's free-form project-name response as the project selector.

**IR-IN-003** — The framework MUST accept on-disk markdown content of `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, and `chief-of-droids/<project>/brief.md` as bind inputs at project bind.

**IR-IN-004** — The framework MUST accept on-disk JSON content of `chief-of-droids/.sessions/<urlencoded-uri>.json` as the sentinel-read input on every turn.

### Outbound (IR-OUT)

**IR-OUT-001** — WHEN the sentinel is absent or the uri mismatches the framework SHALL emit the prompt string `"Which project?"` to the user channel.

**IR-OUT-002** — WHEN bind completes successfully the framework SHALL emit an anchor confirmation to the user channel.

**IR-OUT-003** — IF any of the three bind files fails to load THEN the framework SHALL emit a clear error message naming the offending file path and halt.

**IR-OUT-004** — The framework MUST write the sentinel JSON record to `chief-of-droids/.sessions/<urlencoded-uri>.json` on each bind and on each SHA-mismatch reload.

## Data Requirements

### Data Requirements (DR)

**DR-001** — Sentinel record

| Field | Type | Constraints | Notes |
|:--|:--|:--|:--|
| `uri` | string | REQUIRED UNIQUE | Session identifier from `recent_chats[0].uri`; sentinel key |
| `project` | string | REQUIRED | Project name supplied by the user at bind |
| `loaded_at` | timestamp | REQUIRED | ISO-8601 timestamp of the bind operation |
| `workspace_md_sha` | string | REQUIRED | SHA digest of `chief-of-droids/CLAUDE.md` content at load |
| `project_md_sha` | string | REQUIRED | SHA digest of `<project>/CLAUDE.md` content at load |
| `brief_sha` | string | REQUIRED | SHA digest of `<project>/brief.md` content at load |
| `resolved_skills` | array | REQUIRED | Array of `{trigger, skill, tier}` triples recorded at bind |

### Transformation Requirements (TR)

**TR-001** — Sentinel file path derivation

| Input | Rule | Output |
|:--|:--|:--|
| `recent_chats[0].uri` | URL-encode the uri value | `<urlencoded-uri>` |
| `<urlencoded-uri>` | Prepend `chief-of-droids/.sessions/` and append `.json` | `chief-of-droids/.sessions/<urlencoded-uri>.json` |

**TR-002** — SHA fingerprint computation for bound files

| Input | Rule | Output |
|:--|:--|:--|
| On-disk content of `chief-of-droids/CLAUDE.md` at load time | Apply SHA digest function over the full file byte content | `workspace_md_sha` field value |
| On-disk content of `<project>/CLAUDE.md` at load time | Apply SHA digest function over the full file byte content | `project_md_sha` field value |
| On-disk content of `<project>/brief.md` at load time | Apply SHA digest function over the full file byte content | `brief_sha` field value |

## Non-Functional Requirements

**NFR-001** — The framework MUST achieve skills-routing correctness at or above the substrate-declared baseline. | Measurement: routing-resolution success rate over the sentinel `resolved_skills` set, threshold ≥ 92%.

**NFR-002** — N/A — substrate silent on performance threshold. Warning emitted.

**NFR-003** — The Layer 1 (Project Instructions) content footprint SHOULD be minimal — read on every prompt and multiplied across turns. | Measurement: TBD — token count of Layer 1 content read per turn.

## Security

N/A — substrate silent on Security. Warning emitted. Substrate addresses none of authentication, authorization, encryption, audit logging, rate limiting, or input validation explicitly; governance controls (PR-to-workspace, hard reject on collision, blocked removal) are scoped to §Constraints and §Functional Requirements rather than §Security per the SEC derivability rules.

## Constraints

**CON-001** — Layer 1 (Claude Desktop Project Instructions) SHALL contain only bootstrap dispatcher logic, per-turn sentinel verification rule, and always-on tool routing.

**CON-002** — Substantive content (conventions, project context, skill manifests, protocols) SHALL reside in Layer 2 (`chief-of-droids/CLAUDE.md`) and Layer 3 (`chief-of-droids/<project>/CLAUDE.md`).

**CON-003** — Always-on tools (filesystem, git, fetch) SHALL be routed at Layer 1.

**CON-004** — Project-specific tools SHALL be routed at Layer 3.

**CON-005** — The framework SHALL require explicit user project selection on each new session bind, with no default project applied.

**CON-006** — The sentinel file SHALL reside at `chief-of-droids/.sessions/<urlencoded-uri>.json`.

**CON-007** — `<project>/CLAUDE.md` SHALL carry project conventions and rules; `<project>/brief.md` SHALL carry project state and context. Conventions and state SHALL remain in their respective files. (no `SHALL NOT` clause; expressed positively per the FR/CON binary test row 3)

**CON-008** — On any trigger collision detected at authoring time the workspace tier SHALL win and the project-tier change SHALL be rejected.

**CON-009** — Workspace-tier and project-tier trigger phrases SHALL be disjoint by name and phrase.

**CON-010** — Governance of cross-tier conflicts SHALL operate via pull request to the workspace tier.

**CON-011** — No runtime override path SHALL exist for the workspace-tier precedence rule.

**CON-012** — Composition between tiers SHALL be one-way: project skills may reference workspace skills; workspace skills SHALL NOT reference project skills.

**CON-013** — Negative triggers SHALL be respected with the same precedence direction as positive triggers (workspace tier wins).

**CON-014** — Framework reliability budget SHALL be allocated in priority order: mechanical checks first, once-per-session behaviours second, behavioural rules as backup only.

## Error Handling

**ERR-001** — IF the sentinel read does not complete successfully THEN the framework SHALL treat the session as unbound and proceed to the bind path. → FR-001

**ERR-002** — IF the project-selection prompt does not receive a parseable response THEN the framework SHALL halt and surface the missing-selection error to the user. → FR-002

**ERR-003** — IF any of the three bind files cannot be loaded THEN the framework SHALL halt with a clear error naming the offending file. → FR-003

**ERR-004** — IF the load-verification predicate fails for any of the three bind files THEN the framework SHALL halt with a clear error naming the file that failed verification. → FR-004

**ERR-005** — IF the sentinel write does not complete successfully THEN the framework SHALL surface the failure to the caller and halt the bind. → FR-005

**ERR-007** — IF a per-turn SHA comparison does not complete successfully THEN the framework SHALL invalidate the sentinel and trigger a fresh bind. → FR-007

**ERR-008** — IF the mismatch-driven reload or sentinel-update step does not complete successfully THEN the framework SHALL surface the failure and treat the affected file as unloaded. → FR-008

**ERR-010** — IF resolution-map recording does not complete successfully THEN the framework SHALL surface the failure and halt the bind. → FR-010

**ERR-011** — IF the corpus collision scan does not complete successfully THEN the framework SHALL surface the failure to the skill author and reject the change. → FR-011

**ERR-014** — IF the version bump does not complete successfully THEN the framework SHALL surface the failure to the author and reject the trigger edit. → FR-014

**ERR-016** — IF the author dismisses the "could this be workspace?" prompt without supplying an answer THEN the framework SHALL default to project-tier acceptance and continue. → FR-016

## Observability

N/A — substrate silent on Observability. Warning emitted. Substrate addresses none of metric exposure, structured log emission, trace span emission, health endpoint, or alert threshold explicitly; the anchor confirmation is scoped to §IR-OUT and the SHA fingerprints persisted in the sentinel are scoped to §DR per the OBS derivability rules.

## Acceptance Criteria

**FR-001**
- AC: On any user turn, the framework reads the file at `chief-of-droids/.sessions/<urlencoded-uri>.json` where `<urlencoded-uri>` is derived from `recent_chats[0].uri`.
- AC: The read operation is observable in tool-call telemetry as a sentinel-path filesystem read.

**FR-002**
- AC: When the sentinel is missing or its `uri` field differs from `recent_chats[0].uri`, the user channel receives the prompt text `"Which project?"`.

**FR-003**
- AC: After the user supplies a project name, the framework issues filesystem reads against the three paths `chief-of-droids/CLAUDE.md`, `chief-of-droids/<project>/CLAUDE.md`, `chief-of-droids/<project>/brief.md`.

**FR-004**
- AC: After the three reads complete, the framework asserts non-empty content for each path; on failure the framework halts and emits an error message identifying the failing path.

**FR-005**
- AC: After successful load verification, the file `chief-of-droids/.sessions/<urlencoded-uri>.json` contains a JSON record with the seven fields specified in DR-001.

**FR-006**
- AC: After the sentinel write completes, the user channel contains an anchor confirmation token referring to the bound project.

**FR-007**
- AC: On a subsequent turn with a matching sentinel `uri`, the framework computes SHA digests of the three bound files and emits a three-way comparison result against the persisted SHA fields.

**FR-008**
- AC: When any per-turn SHA comparison returns a mismatch, the corresponding file is reread and the sentinel field is overwritten with the new SHA before the user request proceeds.

**FR-009**
- AC: When all three SHA comparisons match, no user-visible output is emitted prior to the user-request response.

**FR-010**
- AC: After project bind, the sentinel `resolved_skills` field contains one entry per skill known to the dispatcher, each entry shaped as `{trigger, skill, tier}`.

**FR-011**
- AC: When `creating-skills` runs against a new or modified skill, the framework reads every trigger phrase under workspace-tier and project-tier skill directories.

**FR-012**
- AC: Given a proposed trigger phrase that overlaps with any existing trigger phrase by name or phrase, `creating-skills` exits non-zero and writes no skill artefacts.

**FR-013**
- AC: For a trigger matched by both a workspace-tier and a project-tier skill, the dispatcher resolves to the workspace-tier skill and does not invoke the project-tier skill.

**FR-014**
- AC: Editing a workspace skill's trigger phrase produces a workspace-skill version increment in the major-version segment of that skill's version metadata.

**FR-015**
- AC: When removal of a workspace skill is attempted while a project skill or rule references it, the removal operation exits non-zero and the workspace skill remains present.

**FR-016**
- AC: When a project-tier skill is being authored, the framework emits the prompt `"could this be workspace?"` to the author before the skill is accepted into the project tier.

**IR-IN-001**
- AC: The framework reads `recent_chats[0].uri` via the Claude Desktop API at the start of every turn.

**IR-IN-002**
- AC: The framework consumes the next user message after the "Which project?" prompt as the project selector value.

**IR-IN-003**
- AC: The framework reads markdown content from each of the three bind paths during the bind step.

**IR-IN-004**
- AC: The framework reads JSON content from the sentinel path at the start of every turn.

**IR-OUT-001**
- AC: The literal string `"Which project?"` appears in the user channel on the first turn of every new (unbound) session.

**IR-OUT-002**
- AC: A bind-confirmation anchor token appears in the user channel exactly once per bind operation.

**IR-OUT-003**
- AC: On any bind-file load failure, an error message identifying the failing path appears in the user channel and no further bind steps execute.

**IR-OUT-004**
- AC: The sentinel JSON record exists at `chief-of-droids/.sessions/<urlencoded-uri>.json` after every successful bind and after every SHA-mismatch reload.

**DR-001**
- AC: A bound sentinel JSON record contains all seven required fields with the documented types.
- AC: No two sentinel records share the same `uri` value.

**TR-001**
- AC: Given `recent_chats[0].uri = "https://example/chats/abc 123"`, the derived sentinel path is `chief-of-droids/.sessions/https%3A%2F%2Fexample%2Fchats%2Fabc%20123.json`.

**TR-002**
- AC: The SHA fields in the sentinel match the SHA digest of the byte content of the corresponding files at the moment of load.

**NFR-001**
- AC: Skills-routing correctness measured over the sentinel `resolved_skills` set is ≥ 92%.

**NFR-002**
- AC: N/A — no verifiable condition derivable from substrate

**NFR-003**
- AC: N/A — no verifiable condition derivable from substrate (Measurement field is TBD)

**CON-001**
- AC: Static inspection of Project Instructions content shows only the three permitted sections (bootstrap dispatcher logic, per-turn sentinel verification rule, always-on tool routing).

**CON-002**
- AC: Static inspection of Project Instructions does not show conventions, project context, skill manifests, or protocols; this content appears only in Layer 2 and Layer 3 files.

**CON-003**
- AC: Layer 1 declares tool routing for filesystem, git, and fetch.

**CON-004**
- AC: Layer 1 declares no project-specific tool routing; any project-specific tool routing appears only in Layer 3.

**CON-005**
- AC: The bootstrap protocol's project-selection step has no default value; the prompt always fires on first turn of a new session.

**CON-006**
- AC: All sentinel records live under `chief-of-droids/.sessions/` with `.json` suffix and URL-encoded uri filename.

**CON-007**
- AC: `<project>/CLAUDE.md` contains conventions and rules; `<project>/brief.md` contains state and context; no convention statements appear in brief, no state statements appear in CLAUDE.md.

**CON-008**
- AC: For every recorded trigger collision in the corpus history, the rejected change is the project-tier change.

**CON-009**
- AC: Corpus scan over workspace-tier and project-tier trigger phrases returns zero overlaps.

**CON-010**
- AC: Cross-tier conflicts are resolved via merged pull requests to the workspace tier in the repository's history; no other resolution path is documented or observed.

**CON-011**
- AC: No runtime configuration knob, environment variable, or CLI flag exists that disables or inverts the workspace-tier precedence rule.

**CON-012**
- AC: Static inspection of workspace skill manifests shows no references to project skills; project skill manifests may reference workspace skills.

**CON-013**
- AC: A negative trigger declared in a workspace-tier skill prevents the matching phrase from routing to any project-tier skill bearing that phrase.

**CON-014**
- AC: Framework rules that gate audit, verification, or conflict resolution use mechanical mechanisms (filesystem reads, sentinel writes, SHA comparisons) rather than behavioural token-emission rules.

**ERR-001** — AC: On a sentinel-read failure, the framework's next observable action is initiation of the bind path.
**ERR-002** — AC: On a no-response project prompt, the framework halts and the user channel shows a missing-selection error message.
**ERR-003** — AC: On any bind-file load failure, the framework halts and the user channel shows an error naming the file.
**ERR-004** — AC: On load-verification failure, the framework halts and the user channel shows an error naming the verification target.
**ERR-005** — AC: On sentinel-write failure, the framework halts and the user channel shows a write-failure message.
**ERR-007** — AC: On SHA-comparison failure, the sentinel is treated as invalid and the bind path is initiated.
**ERR-008** — AC: On mismatch-reload failure, the framework treats the file as unloaded and the user channel shows a reload-failure message.
**ERR-010** — AC: On resolution-map-write failure, the framework halts and the user channel shows a recording-failure message.
**ERR-011** — AC: On corpus-scan failure, the skill author sees a scan-failure message and the proposed skill change is not persisted.
**ERR-014** — AC: On version-bump failure, the trigger edit is not persisted and the author sees a bump-failure message.
**ERR-016** — AC: On no-response to the "could this be workspace?" prompt, the new skill is accepted into the project tier.

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
| FR-004    |   ✗    |      ✓      |     ✓      |     ✓     |   N/A   |
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
| FR-016    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-001 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-002 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-003 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-IN-004 |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-001|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-002|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-003|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| IR-OUT-004|   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| DR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| TR-001    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| TR-002    |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| NFR-001   |   ✓    |      ✓      |     ✓      |     ✓     |    ✓    |
| NFR-002   |   ✓    |      ✓      |     ✗      |     ✓     |    ✗    |
| NFR-003   |   ✓    |      ✓      |     ✗      |     ✓     |    ✗    |
| CON-001   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-002   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-003   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-004   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-005   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-006   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-007   |   ✗    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-008   |   ✗    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-009   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-010   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-011   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-012   |   ✗    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-013   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| CON-014   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-001   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-002   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-003   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-004   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-005   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-007   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-008   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-010   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-011   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-014   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| ERR-016   |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
