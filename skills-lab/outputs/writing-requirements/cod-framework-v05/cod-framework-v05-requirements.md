# Chief of Droids — Framework

## Purpose

Chief of Droids is a model-in-the-loop framework — governance-first and contract-explicit — in which the model executes within boundaries set by the human operator. The framework's evolution purpose is to make the execution contract for knowledge and code work explicit and durable: every unit of work declares an identity, an input contract, an output contract, an attributable history, and an explicit closure criterion. The framework operates today for a single operator and is required to admit a future evolution to multiple operators without rewriting its artifact contracts.

## Scope

### In Scope

- Declaration, identification, and lifecycle management of units of work.
- Production, delivery, and persistence of input and output artifacts between drafting and executing agents.
- Boundary definition, write-authority enforcement, and read-access rules across operator and agents.
- Versioning of governance configuration (policies, skills, instructions, surface specifications).
- Inspectability of lifecycle state, artifact content, transition history, write attribution, and resource consumption.
- Portability and durability of in-flight state across session termination and across operator machines.
- Forward-compatible artifact contracts admitting additive evolution to multiple operators.

### Out of Scope

- Quantified latency, throughput, or cost targets.
- Security mechanisms (encryption at rest, authentication) — inherited from the operator's operating system and version control system.
- Specific schemas for input and output artifacts — declared structure is required (FR-034); the schemas themselves are design output.
- Specific intermediate lifecycle state names beyond *terminal* and *non-terminal*.
- Unit-of-work identifier format.
- Agent count, types, and roles beyond drafting and executing.

## Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| Operator | Sole human user of the framework; owns filesystem, credentials, and merge decisions; the only actor with continuity across sessions. | user |
| Drafting agent | Bounded ephemeral process that produces a unit of work's input artifact and consumes its output artifact on return. | upstream |
| Executing agent | Bounded ephemeral process that consumes a unit of work's input artifact and produces its output artifact and execution outputs. | downstream |
| Governance configuration store | Source of versioned policies, skills, instructions, and surface specifications read by all agents. | upstream |
| Operator's host environment | Provides filesystem persistence, restart durability, and portability substrate for in-flight state. | downstream |

## Glossary

| Term | Definition | Status |
|:-----|:-----------|:-------|
| agent | A bounded, ephemeral process acting on the operator's authority within a single session. An agent has no persistence and no authority of its own; its writes execute under the operator's permissions. Contrast with *operator*. | substrate |
| artifact | Any persistent output produced during a unit of work, including the input artifact, the output artifact, and any implementation files. | substrate |
| boundary | The set of write authorities that distinguish what each agent and the operator may modify. Expressed as a path-bound or scope-bound policy in design; specified at the property level in this document. | substrate |
| canonical location | A single location designated by the framework as the authoritative source for a particular kind of information. The framework's design forbids reading or writing the same kind of information elsewhere. | substrate |
| closure criterion | The explicit condition that, when satisfied, allows a unit of work to transition to the closed terminal state. Declared at the time the input artifact is sealed (FR-033). | substrate |
| designated audience | For any artifact, the agent or actor explicitly assigned to consume it. The drafting agent's input artifact has the executing agent as its designated audience; the executing agent's output artifact has the drafting agent or the operator as its designated audience. | substrate |
| drafting agent | The agent role responsible for producing the input artifact of a unit of work. | substrate |
| executing agent | The agent role responsible for consuming the input artifact, producing the implementation outputs, and producing the output artifact. | substrate |
| governance configuration | The set of versioned framework files that declare policies, skills, instructions, and surface specifications. Distinct from the artifacts of any particular unit of work. | substrate |
| in-flight | Describes a unit of work whose lifecycle state is not terminal — that is, work that has been declared but neither closed nor aborted. | substrate |
| input artifact | For a unit of work: the artifact written by the drafting agent and consumed by the executing agent at the start of execution. Carries the full input contract (intent, constraints, acceptance criteria, references, closure criterion). | substrate |
| lifecycle state | The current phase of a unit of work. The framework distinguishes non-terminal states (in-flight) from terminal states (closed, aborted); specific intermediate state names are design output. | substrate |
| machine-verifiable | Admits an automated check that can determine, without human judgment, whether content conforms to a declared structure. | substrate |
| operator | The human user of the framework. The only actor with authority and continuity across all sessions. The operator owns the filesystem, credentials, and merge decisions; agents act under the operator's authority. | substrate |
| output artifact | For a unit of work: the artifact written by the executing agent and consumed by the drafting agent or the operator on return. Carries the report of execution against the input artifact's closure criterion. | substrate |
| role | A named function within a unit of work (drafting agent, executing agent). A single agent session may serve different roles for different units of work. | substrate |
| sealed input artifact | An input artifact whose authoring phase has ended. No further modification of its content is permitted by any party until the unit of work reaches a terminal state. | substrate |
| session | A single bounded interaction during which an agent executes under the operator's authority. Sessions terminate independently of unit-of-work lifecycle state. | auto-derived — verify |
| terminal state | A lifecycle state from which no further transitions are allowed. The terminal states are *closed* and *aborted*. | substrate |
| third-party service | Any external service used as a runtime dependency by the framework itself for state persistence. Agents invoking external services (such as LLM APIs) during execution are not the subject of FR-042: that requirement governs the framework's own state, not agent runtime behavior. | substrate |
| unit of work | A single declared, identified scope of work passing through the framework. The smallest unit to which lifecycle states, artifacts, and access rules apply. | substrate |

## Functional Requirements

### Unit of work — declaration and lifecycle

**FR-001** — The framework SHALL allow the operator to declare a unit of work and assign it a unique persistent identifier.

**FR-002** — The framework SHALL allow each agent participating in a unit of work to produce the artifact designated to that agent's role.

**FR-003** — The framework SHALL deliver each artifact produced for a unit of work to its designated audience without requiring the operator to relay the artifact's content manually.

**FR-004** — The framework SHALL persist all artifacts and lifecycle state of in-flight units of work across termination of any agent session.

**FR-005** — The framework SHALL support multiple units of work being in flight concurrently without functional interference between them.

**FR-006** — IF a second agent attempts to occupy a role already occupied within the same unit of work, THEN the framework SHALL prevent that occupation.

**FR-007** — The framework SHALL support resumption of any in-flight unit of work in the role appropriate to its current lifecycle state.

**FR-008** — The framework SHALL support transition of any unit of work to a terminal state by closure or by abort.

**FR-009** — WHEN a unit of work is aborted, the framework SHALL preserve all artifacts produced for that unit before the abort in the state they held at the moment of abort.

**FR-010** — WHEN a unit of work is aborted, the framework SHALL render the artifacts of that unit ineligible for consumption as inputs to other units of work.

**FR-011** — IF execution of a unit of work is requested before that unit's input artifact has been sealed, THEN the framework SHALL refuse the execution request.

### Inspectability and observability

**FR-012** — The framework SHALL allow the operator to inspect the lifecycle state of any unit of work without starting an agent session.

**FR-013** — The framework SHALL allow the operator to inspect any artifact of any unit of work without starting an agent session.

**FR-014** — The framework SHALL preserve the history of lifecycle state transitions for every unit of work and expose it for inspection.

**FR-015** — The framework SHALL attribute every write to any artifact to the agent that performed the write.

**FR-016** — The framework SHALL allow the operator to detect, post-hoc, any violation of the boundaries declared by the access constraints.

**FR-017** — The framework SHALL allow the operator to enumerate all units of work in any lifecycle state without prior knowledge of their identifiers.

**FR-018** — The framework SHALL provide any reader of an artifact a means to verify whether the artifact's content has changed since the artifact was sealed.

**FR-019** — The framework SHALL expose to the operator the resource consumption of each unit of work execution, including at minimum LLM token usage and wall-clock execution time.

### Artifact verification

**FR-020** — WHEN an artifact's authoring phase ends, the framework SHALL verify the artifact against its declared structure.

**FR-021** — WHEN an artifact is delivered to its designated audience, the framework SHALL verify the artifact against its declared structure.

## Constraints

### Access authority

**FR-022** — The framework SHALL allow only the operator to declare, authorize the start of execution for, abort, or close a unit of work.

**FR-023** — The framework SHALL grant the drafting agent of a unit of work write authority over that unit's input artifact.

**FR-024** — The framework SHALL grant the executing agent of a unit of work write authority over that unit's output artifact and over its execution outputs.

**FR-025** — The framework SHALL designate exactly one writing agent for each artifact of a unit of work.

**FR-026** — The framework SHALL grant the operator read access to all artifacts of all units of work at all lifecycle states.

**FR-027** — The framework SHALL grant each agent read access to the artifacts of the unit of work to which the agent is assigned and to the governance configuration.

**FR-028** — The framework SHALL deny each agent read access to artifacts of any unit of work to which the agent is not assigned.

### Governance and structural properties

**FR-029** — The framework SHALL carry a unique persistent identifier with each unit of work from declaration through terminal state.

**FR-030** — WHILE a unit of work has not reached a terminal state, the framework SHALL keep each of its artifacts immutable from the moment that artifact's authoring phase ends.

**FR-031** — The framework SHALL maintain its policies, skills, instructions, and surface specifications under version control.

**FR-032** — The framework SHALL express the boundary between agents' write authorities in a single canonical location reviewable by the operator without starting an agent session.

**FR-033** — WHEN the input artifact of a unit of work is sealed, the framework SHALL require an explicit closure criterion to be declared for that unit.

**FR-034** — The framework SHALL associate each artifact type with a declared structure that all reading and writing agents respect.

**FR-035** — The framework SHALL ensure each declared artifact structure is machine-verifiable.

**FR-036** — The framework SHALL apply a process for modifications to its own policies that is distinct from the process for modifications to artifacts of in-flight units of work.

### Durability, isolation, portability, reproducibility

**FR-037** — The framework SHALL preserve the state and artifacts of every in-flight unit of work across restart of the operator's machine.

**FR-038** — IF the execution of one unit of work fails, THEN the framework SHALL leave the state of every other unit of work unchanged.

**FR-039** — The framework SHALL keep its state portable to a different operator machine without loss of any in-flight unit of work.

**FR-040** — The framework SHALL admit future evolution of its input and output artifact contracts to multiple operators by additive extension only — by addition of optional fields or of new artifact types — without removing, renaming, or making required any field present in the original contract.

**FR-041** — WHEN a unit of work is re-executed against the same sealed input artifact, the framework SHALL produce an output artifact that satisfies the original closure criterion.

**FR-042** — The framework SHALL operate without a runtime dependency on any third-party service for state persistence.

**FR-043** — The framework SHALL ensure every write to any artifact is atomic with respect to operator-observable state.

**FR-044** — IF an artifact is in the middle of being written, THEN the framework SHALL prevent any reader from observing a partial state of that artifact.

## Acceptance Criteria

**FR-001**
- AC: Operator command issued in absence of any prior unit of work returns a non-empty identifier; the same identifier persists across session restart.
- AC: Two consecutive declarations return distinct identifiers.

**FR-002**
- AC: A drafting agent assigned to a unit of work can write that unit's input artifact.
- AC: An executing agent assigned to a unit of work can write that unit's output artifact.

**FR-003**
- AC: An artifact written by an upstream agent appears available to the designated downstream agent without operator copy-paste of its content.

**FR-004**
- AC: After agent session termination, the artifact and lifecycle state of an in-flight unit of work remain readable in the next session.

**FR-005**
- AC: Two units of work declared and progressed in parallel each reach their next lifecycle state without any cross-effect on the other's artifacts or state.

**FR-006**
- AC: A second agent attempting to occupy an already-occupied role within the same unit of work receives a refusal; the original occupant remains.

**FR-007**
- AC: A unit of work in any non-terminal state can be resumed; the resuming agent is dispatched into the role appropriate to that state.

**FR-008**
- AC: From any non-terminal state, an operator-initiated close transitions the unit to *closed*.
- AC: From any non-terminal state, an operator-initiated abort transitions the unit to *aborted*.

**FR-009**
- AC: After abort, the byte content of every artifact produced before abort matches its content immediately prior to the abort transition.

**FR-010**
- AC: After abort, an attempt to consume an aborted unit's artifact as input to a new unit is refused.

**FR-011**
- AC: An execution-start request issued against a unit whose input artifact is not sealed is refused.

**FR-012**
- AC: The lifecycle state of any unit of work is readable without invoking any agent session.

**FR-013**
- AC: The content of any artifact of any unit of work is readable without invoking any agent session.

**FR-014**
- AC: For any unit of work, the ordered list of lifecycle state transitions (with timestamp and prior/next state) is retrievable.

**FR-015**
- AC: Every write to an artifact is recorded with the identity of the agent that performed it.

**FR-016**
- AC: A write performed outside an agent's declared write authority is detectable by the operator after the fact via inspection.

**FR-017**
- AC: An operator-issued enumeration command returns every unit of work currently in any lifecycle state, without requiring identifiers as input.

**FR-018**
- AC: Given a sealed artifact, a reader can compute or retrieve a verifier that distinguishes the sealed content from any subsequent modification.

**FR-019**
- AC: For each completed unit of work execution, the operator can retrieve the LLM token count and the wall-clock execution time.

**FR-020**
- AC: When an artifact's authoring phase ends, a structure-verification check runs and its result is observable.

**FR-021**
- AC: When an artifact is delivered to its designated audience, a structure-verification check runs and its result is observable.

**FR-022**
- AC: Declare, start, abort, and close commands issued by any actor other than the operator are refused.

**FR-023**
- AC: The drafting agent of a unit of work can write that unit's input artifact; no other agent can.

**FR-024**
- AC: The executing agent of a unit of work can write that unit's output artifact and execution outputs; no other agent can.

**FR-025**
- AC: For every artifact of every unit of work, exactly one agent identity is recorded as its writer.

**FR-026**
- AC: The operator can read every artifact of every unit of work in every lifecycle state.

**FR-027**
- AC: An agent assigned to a unit of work can read that unit's artifacts and the governance configuration.

**FR-028**
- AC: An agent attempting to read an artifact of a unit of work to which it is not assigned is refused.

**FR-029**
- AC: A unit of work's identifier at declaration matches its identifier at every subsequent observation up to and including the terminal state.

**FR-030**
- AC: While a unit of work is non-terminal, an attempt to modify a sealed artifact is refused.

**FR-031**
- AC: Each policy, skill, instruction, and surface-specification file carries a version that increments on revision.

**FR-032**
- AC: A single, locatable resource describes the write-authority boundary; the operator can read it without starting an agent session.

**FR-033**
- AC: Sealing the input artifact of a unit of work without a declared closure criterion is refused.

**FR-034**
- AC: Each artifact type has a declared structure available to readers and writers.

**FR-035**
- AC: Each declared artifact structure can be checked by an automated verifier without human judgment.

**FR-036**
- AC: The procedure for modifying governance configuration is documented as distinct from the procedure for modifying artifacts of in-flight units of work.

**FR-037**
- AC: After a restart of the operator's machine, every in-flight unit of work and its artifacts are present and readable.

**FR-038**
- AC: Inducing a failure during the execution of one unit of work leaves the artifacts and state of every other unit of work bit-identical to the pre-failure observation.

**FR-039**
- AC: A relocation of the framework's state to a different operator machine produces every in-flight unit of work and its artifacts at the destination, with no loss.

**FR-040**
- AC: An evolution of the artifact contract that only adds optional fields or new artifact types is admitted; an evolution that removes, renames, or promotes-to-required any original field is rejected.

**FR-041**
- AC: Re-executing a unit of work against the same sealed input artifact produces an output artifact that satisfies the original closure criterion.

**FR-042**
- AC: With every external network dependency disabled, the framework's state persistence operates unchanged.

**FR-043**
- AC: For any in-progress write to an artifact, the operator-observable state transitions atomically from pre-write to post-write.

**FR-044**
- AC: A reader sampling an artifact during a write operation either receives the pre-write content or the post-write content, never an intermediate state.

## Quality Criteria scorecard

| Criterion   | Definition |
|:------------|:-----------|
| Atomic      | The requirement addresses exactly one behavior, constraint, or quality attribute. It contains a single modal verb (SHALL, MUST, SHOULD, MAY). |
| Unambiguous | All terms used are defined in the Glossary or are universally understood. No term is open to more than one interpretation. |
| Verifiable  | The requirement has at least one acceptance criterion — a condition that can be confirmed through testing, inspection, or measurement. |
| Traceable   | The requirement carries a valid, unique identifier (`<CAT>-NNN`) that enables cross-referencing, impact analysis, and change tracking. |
| Bounded     | For NFR-class requirements (NFR, OBS, SEC): the requirement specifies a quantitative threshold (value, time unit, percentage, or volume). N/A for all other requirement types. |

| Req ID  | Atomic | Unambiguous | Verifiable | Traceable | Bounded |
|:--------|:------:|:-----------:|:----------:|:---------:|:-------:|
| FR-001  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-002  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-003  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-004  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-005  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-006  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-007  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-008  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-009  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-010  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-011  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-012  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-013  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-014  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-015  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-016  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-017  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-018  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-019  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-020  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-021  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-022  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-023  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-024  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-025  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-026  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-027  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-028  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-029  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-030  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-031  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-032  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-033  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-034  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-035  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-036  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-037  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-038  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-039  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-040  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-041  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-042  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-043  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |
| FR-044  |   ✓    |      ✓      |     ✓      |     ✓     |   N/A   |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-06 |
| Status       | Draft      |
