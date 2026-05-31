# Chief of Droids — Framework Requirements

## Purpose

Make the execution contract for knowledge and code work explicit and durable. Every unit of work has a declared identity, an input contract, an output contract, an attributable history, and an explicit closure criterion. The framework operates today for a single human operator and is required to admit a future evolution to multiple operators without rewriting its artifact contracts.

## Scope

### In Scope

- Declaration and identification of units of work
- Production, delivery, and persistence of artifacts authored by drafting and executing agents
- Lifecycle state management of units of work, including terminal-state transitions (closure, abort)
- Concurrency of multiple in-flight units of work without functional interference
- Access boundaries between operator, drafting agent, and executing agent
- Versioning of governance configuration (policies, skills, instructions, surface specifications)
- Declared and machine-verifiable structures for each artifact type
- Observability of lifecycle state, artifact content, transition history, attribution, and resource consumption
- Functional reproducibility of execution given a sealed input artifact
- Single-operator current scope, with input and output artifact contracts engineered for additive-only evolution to multiple operators

### Out of Scope

- Quantified latency, throughput, or cost targets
- Security requirements (encryption at rest, authentication mechanisms) — inherited from the operator's operating system and version control system
- Specific schemas for input and output artifacts (existence is required by FR-024; their content is design output)
- Specific lifecycle state names beyond *terminal* and *non-terminal*
- Unit of work identifier format
- Agent count, types, and roles beyond drafting and executing

## Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| operator | Human user; only actor with continuity across sessions; owns filesystem, credentials, and merge decisions | user |
| drafting agent | Bounded, ephemeral process producing the input artifact for a unit of work | upstream |
| executing agent | Bounded, ephemeral process consuming the input artifact, producing implementation outputs and the output artifact | downstream |

## Glossary

| Term | Definition | Status |
|:--|:--|:--|
| agent | A bounded, ephemeral process acting on the operator's authority within a single session. An agent has no persistence and no authority of its own; its writes execute under the operator's permissions. Contrast with *operator*. | substrate |
| artifact | Any persistent output produced during a unit of work, including the input artifact, the output artifact, and any implementation files. | substrate |
| boundary | The set of write authorities that distinguish what each agent and the operator may modify. Expressed as a path-bound or scope-bound policy in design; specified at the property level in this document. | substrate |
| canonical location | A single location designated by the framework as the authoritative source for a particular kind of information. The framework's design forbids reading or writing the same kind of information elsewhere. | substrate |
| closure criterion | The explicit condition that, when satisfied, allows a unit of work to transition to the closed terminal state. Declared at the time the input artifact is sealed (FR-023). | substrate |
| designated audience | For any artifact, the agent or actor explicitly assigned to consume it. The drafting agent's input artifact has the executing agent as its designated audience; the executing agent's output artifact has the drafting agent or the operator as its designated audience. | substrate |
| drafting agent | The agent role responsible for producing the input artifact of a unit of work. | substrate |
| executing agent | The agent role responsible for consuming the input artifact, producing the implementation outputs, and producing the output artifact. | substrate |
| execution outputs | The implementation files produced by the executing agent during a unit of work. A subset of *artifact* per the artifact definition; distinct from the *output artifact* in that execution outputs are the work product (e.g. code) while the output artifact is the report of execution. | auto-derived — verify |
| governance configuration | The set of versioned framework files that declare policies, skills, instructions, and surface specifications. Distinct from the artifacts of any particular unit of work. | substrate |
| in-flight | Describes a unit of work whose lifecycle state is not terminal — that is, work that has been declared but neither closed nor aborted. | substrate |
| input artifact | For a unit of work: the artifact written by the drafting agent and consumed by the executing agent at the start of execution. Carries the full input contract (intent, constraints, acceptance criteria, references, closure criterion). | substrate |
| lifecycle state | The current phase of a unit of work. The framework distinguishes non-terminal states (in-flight) from terminal states (closed, aborted); specific intermediate state names are design output. | substrate |
| LLM | Large Language Model. The class of model an executing agent invokes during execution; relevant here only for resource-consumption observability (FR-035). | auto-derived — verify |
| machine-verifiable | Admits an automated check that can determine, without human judgment, whether content conforms to a declared structure. | substrate |
| operator | The human user of the framework. The only actor with authority and continuity across all sessions. The operator owns the filesystem, credentials, and merge decisions; agents act under the operator's authority. | substrate |
| output artifact | For a unit of work: the artifact written by the executing agent and consumed by the drafting agent or the operator on return. Carries the report of execution against the input artifact's closure criterion. | substrate |
| role | A named function within a unit of work (drafting agent, executing agent). A single agent session may serve different roles for different units of work. | substrate |
| sealed input artifact | An input artifact whose authoring phase has ended. No further modification of its content is permitted by any party until the unit of work reaches a terminal state. | substrate |
| terminal state | A lifecycle state from which no further transitions are allowed. The terminal states are *closed* and *aborted*. | substrate |
| third-party service | Any external service used as a runtime dependency by the framework itself for state persistence. Agents invoking external services (such as LLM APIs) during execution are not the subject of FR-041: that requirement governs the framework's own state, not agent runtime behavior. | substrate |
| unit of work | A single declared, identified scope of work passing through the framework. The smallest unit to which lifecycle states, artifacts, and access rules apply. | substrate |

## Functional Requirements

### Declaration and artifact handling

**FR-001** — The framework SHALL allow the operator to declare a unit of work and obtain a unique persistent identifier for it.

**FR-002** — The framework SHALL allow each agent participating in a unit of work to produce the artifact designated to that agent's role.

**FR-003** — The framework SHALL deliver each artifact produced for a unit of work to its designated audience without manual relay of the artifact's content by the operator.

**FR-004** — The framework SHALL persist all artifacts and lifecycle state of in-flight units of work across termination of any agent session.

### Concurrency and resumption

**FR-005** — The framework SHALL support multiple units of work being in flight concurrently with no functional interference between them.

**FR-006** — The framework SHALL prevent more than one agent from concurrently occupying any role within the same unit of work.

**FR-007** — The framework SHALL support resumption of any in-flight unit of work in the role appropriate to its current lifecycle state.

### Termination and sealing

**FR-008** — The framework SHALL support transition of any unit of work to a terminal state by closure or by abort.

**FR-009** — WHEN a unit of work is aborted the framework SHALL preserve all artifacts produced for that unit before the abort in their state at the moment of abort.

**FR-010** — WHEN a unit of work is aborted the framework SHALL render the artifacts produced for that unit before the abort ineligible for consumption as inputs to other units of work.

**FR-011** — IF the input artifact for a unit of work is not sealed THEN the framework SHALL NOT permit execution of that unit of work to begin.

## Constraints

### Access

**FR-012** — The framework SHALL permit only the operator to initiate a unit of work, authorize the start of its execution, abort it, or close it.

**FR-013** — The drafting agent for a unit of work SHALL have write authority over that unit's input artifact.

**FR-014** — The executing agent for a unit of work SHALL have write authority over that unit's output artifact and over its execution outputs.

**FR-015** — Each artifact of a unit of work SHALL have exactly one designated writing agent.

**FR-016** — The operator SHALL have read access to all artifacts of all units of work at all lifecycle states.

**FR-017** — Each agent SHALL have read access to the artifacts of the unit of work to which it is assigned and to the framework's governance configuration.

**FR-018** — IF an agent is not assigned to a unit of work THEN the framework SHALL NOT grant that agent read access to the artifacts of that unit of work.

### Governance

**FR-019** — Each unit of work SHALL carry a unique persistent identifier from declaration through terminal state.

**FR-020** — Each artifact SHALL be immutable from the moment its authoring phase ends until the unit of work reaches a terminal state.

**FR-021** — The framework's policies, skills, instructions, and surface specifications SHALL be versioned.

**FR-022** — The boundary between each agent's write authorities SHALL be expressed in a single canonical location reviewable by the operator without starting an agent session.

**FR-023** — Each unit of work SHALL declare an explicit closure criterion at the time the input artifact is sealed.

**FR-024** — Each artifact type SHALL have a declared structure that all reading and writing agents respect.

**FR-025** — Each declared artifact structure SHALL be machine-verifiable.

**FR-026** — Modifications to the framework's own policies SHALL follow a process distinct from modifications to artifacts of in-flight units of work.

**FR-027** — The framework SHALL verify each artifact against its declared structure at the time the artifact is sealed and at the time it is delivered to its designated audience.

### Observability

**FR-028** — The lifecycle state of any unit of work SHALL be inspectable by the operator without starting an agent session.

**FR-029** — All artifacts of any unit of work SHALL be inspectable by the operator without starting an agent session.

**FR-030** — The history of lifecycle state transitions for any unit of work SHALL be preserved and inspectable.

**FR-031** — Every write to any artifact SHALL be attributable to the agent that performed it.

**FR-032** — Violations of the boundary defined by access requirements SHALL be detectable by the operator post-hoc.

**FR-033** — The operator SHALL be able to enumerate all units of work in any lifecycle state without prior knowledge of their identifiers.

**FR-034** — The framework SHALL provide a means for any reader of an artifact to verify whether the artifact's content has changed since the artifact was sealed.

**FR-035** — The resource consumption of any unit of work execution — including, at minimum, LLM token usage and wall-clock execution time — SHALL be observable by the operator.

### Non-functional

**FR-036** — The state and artifacts of any in-flight unit of work SHALL survive restart of the operator's machine.

**FR-037** — IF a failure occurs during the execution of one unit of work THEN the framework SHALL NOT alter the state of any other unit of work.

**FR-038** — The framework's state SHALL be portable to a different operator machine without loss of in-flight units of work.

**FR-039** — The framework's input and output artifact contracts SHALL admit a future evolution to multiple operators by additive extension only — additions of optional fields or new artifact types — without removing, renaming, or making required any field present in the original contract.

**FR-040** — Re-execution of a unit of work given the same sealed input artifact SHALL produce an output artifact that satisfies the same closure criterion.

**FR-041** — The framework SHALL operate without a runtime dependency on any third-party service for state persistence.

**FR-042** — Writes to any artifact SHALL be atomic with respect to operator-observable state.

**FR-043** — IF an artifact is being written THEN the framework SHALL NOT expose a partial state of that artifact to any reader.

## Acceptance Criteria

**FR-001**
- AC: When the operator invokes the declaration interface, the framework returns an identifier and persists the unit of work record.
- AC: Two consecutive declarations produce two distinct identifiers.
- AC: A declared unit of work's identifier remains the same after framework restart.

**FR-002**
- AC: When the drafting agent runs against a unit of work in input-authoring state, it can write to that unit's input artifact.
- AC: When the executing agent runs against a unit of work in execution state, it can write to that unit's output artifact.

**FR-003**
- AC: After the drafting agent seals the input artifact, the executing agent reads it without operator copy-paste of its content.
- AC: After the executing agent seals the output artifact, the drafting agent or the operator reads it without operator copy-paste of its content.

**FR-004**
- AC: Terminating an agent session mid-flight, then reopening, reveals the same lifecycle state and artifact contents that existed prior to termination.

**FR-005**
- AC: With two units of work declared and in different lifecycle states, advancing one does not change the lifecycle state of the other.
- AC: The artifacts of one unit of work do not appear in the artifact list of any other unit of work.

**FR-006**
- AC: An attempt to assign a second agent to an already-occupied role for the same unit of work is rejected.

**FR-007**
- AC: A unit of work with sealed input enters the executing-agent role on resume; a unit of work in input-authoring state enters the drafting-agent role on resume.

**FR-008**
- AC: Closure transitions a unit of work to *closed*; further state transitions for that unit are rejected.
- AC: Abort transitions a unit of work to *aborted*; further state transitions for that unit are rejected.

**FR-009**
- AC: After abort, the content of every artifact produced before the abort is byte-identical to its content immediately prior to abort.

**FR-010**
- AC: An attempt to declare a new unit of work taking an aborted unit's artifact as input is rejected.

**FR-011**
- AC: An attempt to start execution of a unit of work whose input artifact is not sealed returns a denial.

**FR-012**
- AC: Each of {declare, authorize-start, abort, close} invoked by an agent is denied.
- AC: Each of {declare, authorize-start, abort, close} invoked by the operator succeeds when preconditions are met.

**FR-013**
- AC: A drafting agent's write to its assigned unit's input artifact succeeds.
- AC: A drafting agent's write to a different unit's input artifact is denied.

**FR-014**
- AC: An executing agent's write to its assigned unit's output artifact succeeds.
- AC: An executing agent's write to its assigned unit's execution outputs succeeds.

**FR-015**
- AC: A query for the designated writer of any given artifact returns exactly one agent role.

**FR-016**
- AC: The operator can read any artifact of any unit of work in any lifecycle state (declared, sealed, executing, closed, aborted).

**FR-017**
- AC: An agent assigned to a unit of work reads that unit's artifacts and reads the governance configuration.

**FR-018**
- AC: An agent's read against an unassigned unit's artifact is denied.

**FR-019**
- AC: The identifier returned at declaration is identical to the identifier observable at the terminal-state record.
- AC: No two units of work — across all lifecycle states, present or past — share the same identifier.

**FR-020**
- AC: An attempt to modify an artifact whose authoring phase has ended is rejected, until the unit of work reaches a terminal state.

**FR-021**
- AC: Each governance configuration file carries a version identifier; modification yields a new version distinguishable from prior versions.

**FR-022**
- AC: The operator opens the boundary specification in a non-agent context and reads the full policy.

**FR-023**
- AC: A unit of work whose input artifact is sealed has a non-empty closure criterion; absence of a declared closure criterion at seal time is rejected.

**FR-024**
- AC: Each artifact type has a declared structure document referenced by reading and writing agents.

**FR-025**
- AC: A verifier program runs against an artifact of a given type and returns conform/non-conform without human judgment.

**FR-026**
- AC: The change process for governance configuration is documented separately from, and distinct from, the change process for in-flight artifacts.

**FR-027**
- AC: At the moment an artifact is sealed, the verifier runs and emits a pass/fail result.
- AC: At the moment an artifact is delivered to its designated audience, the verifier runs and emits a pass/fail result.

**FR-028**
- AC: The operator opens an inspection surface in a non-agent context and observes the lifecycle state of any unit of work.

**FR-029**
- AC: The operator opens an inspection surface in a non-agent context and reads any artifact of any unit of work.

**FR-030**
- AC: For any unit of work, the operator retrieves an ordered list of all prior lifecycle state transitions.

**FR-031**
- AC: For any persisted artifact write, an attribution record names the agent role that performed the write.

**FR-032**
- AC: An out-of-boundary write produces a detectable record visible to the operator after the fact.

**FR-033**
- AC: The operator queries an enumeration surface and receives the full list of unit-of-work identifiers and their current lifecycle states.

**FR-034**
- AC: A reader of any artifact obtains a verification result indicating whether the content matches the sealed state.

**FR-035**
- AC: For any executed unit of work, the operator obtains the LLM token usage and the wall-clock execution time of that execution.

**FR-036**
- AC: After a restart of the operator's machine, the framework's in-flight units of work and their artifacts are present and unchanged.

**FR-037**
- AC: Inducing a failure during execution of unit A leaves unit B's lifecycle state and artifacts unchanged.

**FR-038**
- AC: After moving the framework's state to a different operator machine, the in-flight units of work resume in the same lifecycle state with the same artifact contents.

**FR-039**
- AC: Inspecting any new artifact contract version reveals only added optional fields or added artifact types relative to the original contract; no field has been removed, renamed, or made required.

**FR-040**
- AC: Two executions of the same sealed input artifact each produce an output artifact whose evaluation against the closure criterion passes.

**FR-041**
- AC: With all third-party services unreachable, the framework reads, writes, and persists state correctly.

**FR-042**
- AC: A reader observing an artifact during a write sees either the pre-write state or the post-write state, never a partial state.

**FR-043**
- AC: Concurrent reader and writer interactions on the same artifact never expose a partial artifact to the reader.

## Quality Criteria scorecard

| Criterion   | Definition |
|:------------|:-----------|
| Atomic      | The requirement addresses exactly one behavior, constraint, or quality attribute. It contains a single modal verb (SHALL, MUST, SHOULD, MAY). |
| Unambiguous | All terms used are defined in the Glossary or are universally understood. No term is open to more than one interpretation. |
| Verifiable  | The requirement has at least one acceptance criterion — a condition that can be confirmed through testing, inspection, or measurement. |
| Traceable   | The requirement carries a valid, unique identifier (`<CAT>-NNN`) that enables cross-referencing, impact analysis, and change tracking. |
| Bounded     | For NFR-class requirements (NFR, OBS, SEC): the requirement specifies a quantitative threshold (value, time unit, percentage, or volume). N/A for all other requirement types. |

| Req ID | Atomic | Unambiguous | Verifiable | Traceable | Bounded |
|:--|:--:|:--:|:--:|:--:|:--:|
| FR-001 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-002 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-003 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-004 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-005 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-006 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-007 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-008 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-009 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-010 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-011 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-012 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-013 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-014 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-015 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-016 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-017 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-018 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-019 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-020 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-021 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-022 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-023 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-024 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-025 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-026 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-027 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-028 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-029 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-030 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-031 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-032 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-033 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-034 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-035 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-036 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-037 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-038 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-039 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-040 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-041 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-042 | ✓ | ✓ | ✓ | ✓ | N/A |
| FR-043 | ✓ | ✓ | ✓ | ✓ | N/A |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-06 |
| Status       | Draft      |
