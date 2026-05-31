# Chief of Droids Framework

## Purpose

Chief of Droids is a model-in-the-loop framework — governance-first and contract-explicit — in which the model executes within defined boundaries set by the human operator. Its purpose is to make the execution contract for knowledge and code work explicit and durable: every unit of work carries a declared identity, an input contract, an output contract, an attributable history, and an explicit closure criterion. The framework operates today for a single operator and is required to admit a future evolution to multiple operators without rewriting its artifact contracts.

## Scope

### In Scope

N/A

### Out of Scope

- Quantified latency, throughput, or cost targets — single-operator scope; no SLA exists.
- Security obligations covered by the operator's operating system and version control system (encryption at rest, authentication mechanisms).
- Specific schemas for input and output artifacts — schema declaration is mandated; specific schemas are design output.
- Specific lifecycle state names beyond *terminal* and *non-terminal* — named intermediate states are design output.
- The format of the unit-of-work identifier — uniqueness and persistence are mandated; format is design output.
- Agent count, types, and roles beyond drafting and executing — additional roles can be derived without altering the requirements.

## Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| Operator | The human user; sole authority to declare, authorize execution start, abort, and close any unit of work | user |
| Drafting agent | Authors the input artifact for a unit of work | upstream |
| Executing agent | Consumes the input artifact; produces execution outputs and the output artifact | downstream |

## Glossary

| Term | Definition | Status |
|:--|:--|:--|
| agent | A bounded, ephemeral process acting on the operator's authority within a single session. An agent has no persistence and no authority of its own; its writes execute under the operator's permissions. | substrate |
| artifact | Any persistent output produced during a unit of work, including the input artifact, the output artifact, and any implementation files. | substrate |
| boundary | The set of write authorities that distinguish what each agent and the operator may modify. Expressed as a path-bound or scope-bound policy in design; specified at the property level in this document. | substrate |
| canonical location | A single location designated by the framework as the authoritative source for a particular kind of information. Reading or writing the same kind of information elsewhere is forbidden. | substrate |
| closure criterion | The explicit condition that, when satisfied, allows a unit of work to transition to the closed terminal state. Declared at the time the input artifact is sealed. | substrate |
| designated audience | For any artifact, the agent or actor explicitly assigned to consume it. | substrate |
| drafting agent | The agent role responsible for producing the input artifact of a unit of work. | substrate |
| executing agent | The agent role responsible for consuming the input artifact, producing the implementation outputs, and producing the output artifact. | substrate |
| execution outputs | The implementation files produced by the executing agent during a unit of work, distinct from the output artifact (which is the execution report). | auto-derived — verify |
| governance configuration | The set of versioned framework files that declare policies, skills, instructions, and surface specifications. Distinct from the artifacts of any particular unit of work. | substrate |
| in-flight | Describes a unit of work whose lifecycle state is not terminal — that is, work declared but neither closed nor aborted. | substrate |
| input artifact | The artifact written by the drafting agent and consumed by the executing agent at the start of execution. Carries the full input contract (intent, constraints, acceptance criteria, references, closure criterion). | substrate |
| lifecycle state | The current phase of a unit of work. The framework distinguishes non-terminal states (in-flight) from terminal states (closed, aborted); specific intermediate state names are design output. | substrate |
| machine-verifiable | Admits an automated check that can determine, without human judgment, whether content conforms to a declared structure. | substrate |
| operator | The human user of the framework. The only actor with authority and continuity across all sessions. The operator owns the filesystem, credentials, and merge decisions. | substrate |
| output artifact | The artifact written by the executing agent and consumed by the drafting agent or the operator on return. Carries the report of execution against the input artifact's closure criterion. | substrate |
| role | A named function within a unit of work (drafting agent, executing agent). A single agent session may serve different roles for different units of work. | substrate |
| sealed input artifact | An input artifact whose authoring phase has ended. No further modification of its content is permitted by any party until the unit of work reaches a terminal state. | substrate |
| terminal state | A lifecycle state from which no further transitions are allowed. The terminal states are *closed* and *aborted*. | substrate |
| third-party service | Any external service used as a runtime dependency by the framework itself for state persistence. | substrate |
| unit of work | A single declared, identified scope of work passing through the framework. The smallest unit to which lifecycle states, artifacts, and access rules apply. | substrate |

## Functional Requirements

**FR-001** — The framework SHALL allow the operator to declare a unit of work and obtain a unique persistent identifier for that unit of work.

**FR-002** — The framework SHALL allow each agent participating in a unit of work to produce the artifact designated to that agent's role.

**FR-003** — The framework SHALL deliver each artifact produced for a unit of work to its designated audience without manual relay of the artifact's content by the operator.

**FR-004** — The framework SHALL persist all artifacts and lifecycle state of in-flight units of work across termination of any agent session.

**FR-005** — The framework SHALL support multiple units of work being in flight concurrently with no functional interference between them.

**FR-006** — The framework SHALL prevent more than one agent from concurrently occupying any role within the same unit of work.

**FR-007** — The framework SHALL support resumption of any in-flight unit of work in the role appropriate to its current lifecycle state.

**FR-008** — The framework SHALL support transition of any unit of work to a terminal state by closure or by abort.

**FR-009** — WHEN a unit of work is aborted the framework SHALL preserve all artifacts produced for that unit before the abort in their state at the moment of abort.

**FR-010** — WHEN a unit of work is aborted the framework SHALL render its preserved artifacts ineligible for consumption as inputs to other units of work.

**FR-011** — IF a unit of work's input artifact has not been sealed THEN the framework SHALL NOT permit execution of that unit of work to begin.

## Constraints

### Access controls

**FR-012** — The framework SHALL restrict initiating, authorizing the start of execution, aborting, and closing of any unit of work to the operator.

**FR-013** — The framework SHALL grant the drafting agent for a unit of work write authority over that unit's input artifact.

**FR-014** — The framework SHALL grant the executing agent for a unit of work write authority over that unit's output artifact and its execution outputs.

**FR-015** — The framework SHALL designate exactly one writing agent for each artifact of a unit of work.

**FR-016** — The framework SHALL grant the operator read access to all artifacts of all units of work at all lifecycle states.

**FR-017** — The framework SHALL grant each agent read access to the artifacts of the unit of work to which it is assigned and to the governance configuration.

**FR-018** — IF an agent attempts to read an artifact of a unit of work to which it is not assigned THEN the framework SHALL deny the read.

### Governance

**FR-019** — The framework SHALL ensure each unit of work carries a unique persistent identifier from declaration through its terminal state.

**FR-020** — The framework SHALL prevent modification of any artifact from the moment its authoring phase ends until the unit of work reaches a terminal state.

**FR-021** — The framework SHALL version its policies, skills, instructions, and surface specifications.

**FR-022** — The framework SHALL express the boundary between each agent's write authorities in a single canonical location reviewable by the operator without starting an agent session.

**FR-023** — WHEN a unit of work's input artifact is sealed the framework SHALL ensure that unit's closure criterion is declared.

**FR-024** — The framework SHALL declare a structure for each artifact type that all reading and writing agents conform to.

**FR-025** — The framework SHALL ensure each declared artifact structure is machine-verifiable.

**FR-026** — The framework SHALL govern modifications to its own policies through a process distinct from modifications to artifacts of in-flight units of work.

**FR-027** — WHEN an artifact is sealed the framework SHALL verify it against its declared structure.

**FR-028** — WHEN an artifact is delivered to its designated audience the framework SHALL verify it against its declared structure.

### Observability

**FR-029** — The framework SHALL make the lifecycle state of any unit of work inspectable by the operator without starting an agent session.

**FR-030** — The framework SHALL make all artifacts of any unit of work inspectable by the operator without starting an agent session.

**FR-031** — The framework SHALL preserve the history of lifecycle state transitions for any unit of work and make that history inspectable.

**FR-032** — The framework SHALL attribute every write to any artifact to the agent that performed it.

**FR-033** — The framework SHALL make violations of the boundary defined by access requirements detectable by the operator post-hoc.

**FR-034** — The framework SHALL allow the operator to enumerate all units of work in any lifecycle state without prior knowledge of their identifiers.

**FR-035** — The framework SHALL provide a means for any reader of an artifact to verify whether the artifact's content has changed since the artifact was sealed.

**FR-036** — The framework SHALL make the resource consumption of any unit of work execution — including, at minimum, LLM token usage and wall-clock execution time — observable by the operator.

### Operational properties

**FR-037** — The framework SHALL preserve the state and artifacts of any in-flight unit of work across restart of the operator's machine.

**FR-038** — IF a failure occurs during the execution of one unit of work THEN the framework SHALL NOT alter the state of any other unit of work.

**FR-039** — The framework SHALL admit migration of its state to a different operator machine without loss of in-flight units of work.

**FR-040** — The framework SHALL admit evolution of its input and output artifact contracts to multiple operators by additive extension only — additions of optional fields or new artifact types — without removing, renaming, or making required any field present in the original contract.

**FR-041** — WHEN a unit of work is re-executed given the same sealed input artifact the framework SHALL produce an output artifact that satisfies the same closure criterion.

**FR-042** — The framework SHALL operate without a runtime dependency on any third-party service for state persistence.

**FR-043** — The framework SHALL ensure writes to any artifact are atomic with respect to operator-observable state.

**FR-044** — IF an artifact is in the middle of being written THEN the framework SHALL NOT expose its partial state to any reader.

## Acceptance Criteria

**FR-001**
- AC: A declaration request from the operator returns a unit-of-work identifier.
- AC: The returned identifier is distinct from identifiers issued for any prior unit of work.

**FR-002**
- AC: An agent assigned to a role can write the artifact designated to that role and the write succeeds.

**FR-003**
- AC: After an artifact is produced, its designated audience can consume it without the operator manually transferring the artifact's content.

**FR-004**
- AC: After termination of an agent session, the artifacts and lifecycle state of any in-flight unit of work that the session participated in remain readable.

**FR-005**
- AC: Two units of work executed in parallel each reach their declared lifecycle states without altering each other's artifacts or state.

**FR-006**
- AC: An attempt to assign a second agent to a role already occupied within the same unit of work is rejected.

**FR-007**
- AC: A unit of work in lifecycle state X can be resumed in the role appropriate to state X.

**FR-008**
- AC: A unit of work can be transitioned to *closed*; the resulting state is terminal.
- AC: A unit of work can be transitioned to *aborted*; the resulting state is terminal.

**FR-009**
- AC: After an abort transition, every artifact produced before the abort is present and readable in its pre-abort state.

**FR-010**
- AC: An attempt to consume an aborted unit's preserved artifact as input to another unit of work is rejected.

**FR-011**
- AC: An attempt to begin execution of a unit of work whose input artifact is not sealed is rejected.

**FR-012**
- AC: An attempt by a non-operator actor to declare, authorize execution start, abort, or close a unit of work is rejected.

**FR-013**
- AC: The drafting agent assigned to a unit of work can write that unit's input artifact; any other agent attempting the same write is rejected.

**FR-014**
- AC: The executing agent assigned to a unit of work can write that unit's output artifact and its execution outputs; any other agent attempting these writes is rejected.

**FR-015**
- AC: For every artifact, exactly one agent role is recorded as its designated writer.

**FR-016**
- AC: The operator can read any artifact of any unit of work regardless of lifecycle state.

**FR-017**
- AC: An agent assigned to a unit of work can read its artifacts and the governance configuration.

**FR-018**
- AC: An attempt by an agent to read an artifact of a unit of work to which it is not assigned is rejected.

**FR-019**
- AC: A unit of work's identifier is unchanged from declaration through its terminal state and is unique across all units of work.

**FR-020**
- AC: An attempt to modify an artifact after its authoring phase ends and before the unit of work reaches a terminal state is rejected.

**FR-021**
- AC: The framework's policies, skills, instructions, and surface specifications each carry a version identifier.

**FR-022**
- AC: The boundary between agents' write authorities is documented in a single location reviewable by the operator without starting an agent session.

**FR-023**
- AC: At the moment an input artifact is sealed, the closure criterion for that unit of work is recorded.

**FR-024**
- AC: For each artifact type, a structure declaration exists; read and write operations conforming to it succeed and non-conforming ones are rejected.

**FR-025**
- AC: For each declared artifact structure, an automated check exists that determines conformance without human judgment.

**FR-026**
- AC: The procedure for modifying framework policies is distinct from the procedure for modifying artifacts of in-flight units of work.

**FR-027**
- AC: When an artifact is sealed, a structural verification result is recorded before sealing completes.

**FR-028**
- AC: When an artifact is delivered to its designated audience, a structural verification result is recorded before delivery completes.

**FR-029**
- AC: The operator can read the lifecycle state of any unit of work without starting an agent session.

**FR-030**
- AC: The operator can read all artifacts of any unit of work without starting an agent session.

**FR-031**
- AC: For any unit of work, the sequence of lifecycle state transitions is preserved and readable post-hoc.

**FR-032**
- AC: For every write to any artifact, a record exists identifying the agent that performed the write.

**FR-033**
- AC: After a boundary violation, the operator can identify the violating write through post-hoc inspection.

**FR-034**
- AC: The operator can obtain a list of all units of work in any lifecycle state without supplying prior identifiers.

**FR-035**
- AC: A reader of an artifact can determine whether the artifact's content has changed since it was sealed.

**FR-036**
- AC: For any unit of work execution, LLM token usage and wall-clock execution time are readable by the operator.

**FR-037**
- AC: After restart of the operator's machine, the state and artifacts of any in-flight unit of work are present and readable.

**FR-038**
- AC: A failure injected into the execution of one unit of work leaves the artifacts and lifecycle state of all other units of work unchanged.

**FR-039**
- AC: After migration of the framework's state to a different operator machine, all in-flight units of work present pre-migration are present and resumable post-migration.

**FR-040**
- AC: Across versions of the input/output artifact contracts, no field present in the original contract is removed, no field is renamed, and no previously optional field is made required.

**FR-041**
- AC: Re-execution of a unit of work given the same sealed input artifact yields an output artifact that satisfies the same closure criterion.

**FR-042**
- AC: The framework's state persistence operates without invoking any third-party service.

**FR-043**
- AC: At every observable moment, the operator-visible state of any artifact is either the pre-write state or the post-write state, not an intermediate state.

**FR-044**
- AC: While an artifact is being written, any concurrent read returns the pre-write state.

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
