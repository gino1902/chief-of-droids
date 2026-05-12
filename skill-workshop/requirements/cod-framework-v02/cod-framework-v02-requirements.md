# Chief of Droids Framework

## Purpose

Chief-of-Droids is a model-in-the-loop framework — governance-first and contract-explicit — in which the model executes within boundaries set by the human operator. The framework's purpose is to make the execution contract for knowledge and code work explicit and durable: every unit of work has a declared identity, an input contract, an output contract, an attributable history, and an explicit closure criterion. Governance and knowledge work sit on the operator's authoring surface; execution sits on the operator's execution surface. The framework operates today for a single human operator and admits a future evolution to multiple operators without rewriting its artifact contracts.

## Scope

### In Scope

- Declaration, identification, and lifecycle of units of work
- Production, sealing, delivery, and inspection of input and output artifacts
- Boundaries between operator and agent write authorities
- Persistence of in-flight artifacts and lifecycle state across agent sessions and machine restarts
- Concurrent execution of multiple units of work without functional interference
- Versioning of the framework's own policies, skills, instructions, and surface specifications
- Observability of lifecycle state, artifact content, attributable writes, and resource consumption

### Out of Scope

- Quantified latency, throughput, or cost targets
- Security requirements (encryption at rest, authentication mechanisms)
- Specific schemas for input and output artifacts
- Specific lifecycle state names beyond *terminal* and *non-terminal*
- Unit-of-work identifier format
- Agent count, types, and roles beyond drafting and executing

## Actors & Consumers

| Actor | Role | Direction |
|:--|:--|:--|
| Operator | Human user; sole authority for initiating, authorizing, aborting, and closing units of work | user |
| Drafting agent | Bounded, ephemeral process producing the input artifact of a unit of work | user |
| Executing agent | Bounded, ephemeral process consuming the input artifact and producing the output artifact and execution outputs | user |
| LLM API | External service invoked by agents during execution | downstream |

## Glossary

| Term | Definition | Status |
|:--|:--|:--|
| agent | A bounded, ephemeral process acting on the operator's authority within a single session. An agent has no persistence and no authority of its own; its writes execute under the operator's permissions. | substrate |
| artifact | Any persistent output produced during a unit of work, including the input artifact, the output artifact, and any implementation files. | substrate |
| boundary | The set of write authorities that distinguish what each agent and the operator may modify. Expressed as a path-bound or scope-bound policy in design; specified at the property level in this document. | substrate |
| canonical location | A single location designated by the framework as the authoritative source for a particular kind of information. The framework's design forbids reading or writing the same kind of information elsewhere. | substrate |
| closure criterion | The explicit condition that, when satisfied, allows a unit of work to transition to the closed terminal state. Declared at the time the input artifact is sealed. | substrate |
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
| terminal state | A lifecycle state from which no further transitions are allowed. The terminal states are *closed* and *aborted*. | substrate |
| third-party service | Any external service used as a runtime dependency by the framework itself for state persistence. Agents invoking external services (such as LLM APIs) during execution are not the subject of FR-040: that requirement governs the framework's own state, not agent runtime behavior. | substrate |
| unit of work | A single declared, identified scope of work passing through the framework. The smallest unit to which lifecycle states, artifacts, and access rules apply. | substrate |
| abort | The lifecycle transition by which a unit of work reaches the *aborted* terminal state without completion of its closure criterion. | auto-derived — verify |
| execution outputs | The implementation files produced by the executing agent during execution of a unit of work, distinct from the output artifact. | auto-derived — verify |
| agent session | A single uninterrupted period during which an agent process is active under the operator's authority. | auto-derived — verify |

## Functional Requirements

### Lifecycle of a unit of work

**FR-001** — The framework SHALL allow the operator to declare a unit of work and obtain a unique persistent identifier for it.

**FR-002** — The framework SHALL allow each agent participating in a unit of work to produce the artifact designated to that agent's role.

**FR-003** — The framework SHALL deliver each artifact produced for a unit of work to its designated audience without manual relay of the artifact's content by the operator.

**FR-004** — The framework SHALL persist all artifacts and lifecycle state of in-flight units of work across termination of any agent session.

**FR-005** — The framework SHALL support multiple units of work being in flight concurrently with no functional interference between them.

**FR-006** — The framework SHALL prevent more than one agent from concurrently occupying any role within the same unit of work.

**FR-007** — The framework SHALL support resumption of any in-flight unit of work in the role appropriate to its current lifecycle state.

**FR-008** — The framework SHALL support transition of any unit of work to a terminal state by closure or by abort.

**FR-009** — WHEN a unit of work is aborted the framework SHALL preserve all artifacts produced for that unit before the abort in their state at the moment of abort.

**FR-010** — WHEN a unit of work is aborted the framework SHALL render those preserved artifacts ineligible for consumption as inputs to other units of work.

**FR-011** — IF the input artifact of a unit of work has not been sealed THEN the framework SHALL NOT permit execution of that unit of work to begin.

### Access

**FR-012** — The framework SHALL permit only the operator to initiate, authorize the start of execution for, abort, or close a unit of work.

**FR-013** — The framework SHALL grant the drafting agent of a unit of work write authority over that unit's input artifact.

**FR-014** — The framework SHALL grant the executing agent of a unit of work write authority over that unit's output artifact and execution outputs.

**FR-015** — The framework SHALL designate exactly one writing agent for each artifact of a unit of work.

**FR-016** — The framework SHALL grant the operator read access to all artifacts of all units of work in any lifecycle state.

**FR-017** — The framework SHALL grant each agent read access only to the artifacts of the unit of work to which the agent is assigned and to the framework's governance configuration.

### Governance

**FR-018** — Each unit of work SHALL carry a unique persistent identifier from declaration through terminal state.

**FR-019** — Each artifact SHALL be immutable from the moment its authoring phase ends until the unit of work reaches a terminal state.

**FR-020** — The framework's policies, skills, instructions, and surface specifications SHALL be versioned.

**FR-021** — The boundary between each agent's write authorities SHALL be expressed in a single canonical location reviewable by the operator without starting an agent session.

**FR-022** — Each unit of work SHALL declare an explicit closure criterion at the time the input artifact is sealed.

**FR-023** — Each artifact type SHALL have a declared structure that all reading and writing agents respect.

**FR-024** — Each declared artifact structure SHALL be machine-verifiable.

**FR-025** — Modifications to the framework's own policies SHALL follow a process distinct from modifications to artifacts of in-flight units of work.

**FR-026** — The framework SHALL verify each artifact against its declared structure at the time the artifact is sealed and at the time it is delivered to its designated audience.

### Observability

**FR-027** — The lifecycle state of any unit of work SHALL be inspectable by the operator without starting an agent session.

**FR-028** — All artifacts of any unit of work SHALL be inspectable by the operator without starting an agent session.

**FR-029** — The history of lifecycle state transitions for any unit of work SHALL be preserved and inspectable by the operator.

**FR-030** — Every write to any artifact SHALL be attributable to the agent that performed it.

**FR-031** — Violations of the boundary defined by the access requirements SHALL be detectable by the operator post-hoc.

**FR-032** — The framework SHALL allow the operator to enumerate all units of work in any lifecycle state without prior knowledge of their identifiers.

**FR-033** — The framework SHALL provide a means for any reader of an artifact to verify whether the artifact's content has changed since the artifact was sealed.

**FR-034** — The resource consumption of any unit-of-work execution — including, at minimum, LLM token usage and wall-clock execution time — SHALL be observable by the operator.

## Constraints

**FR-035** — The state and artifacts of any in-flight unit of work SHALL survive restart of the operator's machine.

**FR-036** — A failure during the execution of one unit of work SHALL NOT alter the state of any other unit of work.

**FR-037** — The framework's state SHALL be portable to a different operator machine without loss of in-flight units of work.

**FR-038** — The framework's input and output artifact contracts SHALL admit a future evolution to multiple operators by additive extension only — additions of optional fields or new artifact types — without removing, renaming, or making required any field present in the original contract.

**FR-039** — Re-execution of a unit of work given the same sealed input artifact SHALL produce an output artifact that satisfies the same closure criterion (functional reproducibility — outcome, not bit-for-bit).

**FR-040** — The framework SHALL operate without a runtime dependency on any third-party service for state persistence.

**FR-041** — Writes to any artifact SHALL be atomic with respect to operator-observable state, such that no reader observes a partial state of an artifact in the middle of being written.

## Acceptance Criteria

**FR-001**
- AC: After the operator issues a declaration command, the framework returns a non-empty identifier string and the unit of work is enumerable in the in-flight set.
- AC: Two consecutive declarations issued by the operator return two distinct identifier values.

**FR-002**
- AC: An agent assigned the drafting role can write to the input-artifact location of its assigned unit of work and the write succeeds.
- AC: An agent assigned the executing role can write to the output-artifact location of its assigned unit of work and the write succeeds.

**FR-003**
- AC: When the drafting agent seals the input artifact, the executing agent's reads of that artifact return the sealed content without operator action.
- AC: When the executing agent produces the output artifact, the drafting agent or operator can read that artifact without operator-mediated content transfer.

**FR-004**
- AC: After the agent session that produced an in-flight artifact terminates, a subsequent inspection by the operator returns the artifact's content unchanged.
- AC: After agent-session termination, the lifecycle state of each in-flight unit of work is recoverable on next inspection.

**FR-005**
- AC: With N units of work in flight (N ≥ 2), an action against unit A produces no observable change in the artifacts or lifecycle state of unit B.

**FR-006**
- AC: An attempt to assign a second agent to a role already occupied within the same unit of work is rejected.

**FR-007**
- AC: For an in-flight unit of work in lifecycle state S, the operator can resume work and the framework places the resuming agent in the role appropriate to S.

**FR-008**
- AC: A close command issued by the operator on a unit of work satisfying its closure criterion transitions the unit to the *closed* terminal state.
- AC: An abort command issued by the operator on an in-flight unit of work transitions the unit to the *aborted* terminal state.

**FR-009**
- AC: Given a unit of work with artifacts A1…An produced before abort, after the abort transition each Ai is readable and its content matches its pre-abort state byte-for-byte.

**FR-010**
- AC: After abort, an attempt to declare a new unit of work consuming an artifact of the aborted unit as its input is rejected.

**FR-011**
- AC: An attempt to start execution of a unit of work whose input artifact is not sealed is rejected.

**FR-012**
- AC: Initiating, authorizing start of execution for, aborting, or closing a unit of work, when attempted by any actor other than the operator, is rejected.

**FR-013**
- AC: The drafting agent of a unit of work performs a write to its input artifact and the write succeeds.
- AC: A non-drafting agent attempting to write to the same input artifact is rejected.

**FR-014**
- AC: The executing agent of a unit of work performs a write to its output artifact and to its execution outputs and both writes succeed.
- AC: A non-executing agent attempting to write to those locations is rejected.

**FR-015**
- AC: For every artifact of a unit of work, the framework's records identify exactly one designated writing agent.

**FR-016**
- AC: Read attempts by the operator on any artifact of any unit of work in any lifecycle state succeed.

**FR-017**
- AC: An agent reads an artifact of its assigned unit of work and the read succeeds.
- AC: An agent reads the framework's governance configuration and the read succeeds.
- AC: An agent attempting to read an artifact of an unassigned unit of work is denied.

**FR-018**
- AC: For each unit of work, the identifier obtained at declaration is unchanged at every later inspection until terminal state.
- AC: Two distinct units of work never share the same identifier.

**FR-019**
- AC: After authoring of an artifact ends, an attempt to modify its content by any party is rejected until the unit of work reaches a terminal state.

**FR-020**
- AC: Each policy, skill, instruction, and surface specification of the framework carries a version identifier.

**FR-021**
- AC: A single document or set of documents at one canonical location declares the boundary between each agent's write authorities.
- AC: The operator inspects that location without starting an agent session and the content is returned.

**FR-022**
- AC: At the moment the input artifact of a unit of work is sealed, the unit of work has an explicit closure criterion attached.

**FR-023**
- AC: Each artifact type referenced in the framework has an associated structure declaration; agents reading or writing artifacts of that type honor the declaration.

**FR-024**
- AC: For each declared artifact-structure declaration, an automated check returns conformant / non-conformant for a given artifact instance.

**FR-025**
- AC: A modification to a framework policy follows a documented process distinct from the process used to modify in-flight artifacts.

**FR-026**
- AC: At the moment of sealing, the framework runs the structural check on the artifact and reports the result.
- AC: At the moment of delivery to the designated audience, the framework runs the structural check on the artifact and reports the result.

**FR-027**
- AC: The operator inspects the lifecycle state of a unit of work without starting an agent session and the state value is returned.

**FR-028**
- AC: The operator inspects each artifact of a unit of work without starting an agent session and the artifact content is returned.

**FR-029**
- AC: For each unit of work, an enumeration of lifecycle state transitions, in order of occurrence, is retrievable by the operator.

**FR-030**
- AC: For any artifact, the record of its writes identifies the agent that performed each write.

**FR-031**
- AC: Given a write that violates an access boundary, the operator finds a record of that violation by inspection after the fact.

**FR-032**
- AC: The operator issues an enumeration command without supplying any unit-of-work identifier and receives the list of all units of work in any lifecycle state.

**FR-033**
- AC: A reader of a sealed artifact obtains a verdict (changed / unchanged) on whether the artifact content differs from its sealed state.

**FR-034**
- AC: For each completed unit-of-work execution, the operator retrieves the LLM token usage value.
- AC: For each completed unit-of-work execution, the operator retrieves the wall-clock execution time value.

**FR-035**
- AC: After the operator's machine restarts, the artifacts and lifecycle state of every in-flight unit of work present before the restart are recoverable.

**FR-036**
- AC: A failure injected into the execution of unit A produces no observable change in the artifacts or lifecycle state of any other unit B.

**FR-037**
- AC: The framework's state is transferred to a second operator machine and every in-flight unit of work present on the source is present and operable on the destination.

**FR-038**
- AC: A future revision of the artifact contracts that adds optional fields or new artifact types validates against the original contracts.
- AC: Any revision that removes a field, renames a field, or changes an optional field to required is rejected by the contract-evolution process.

**FR-039**
- AC: A unit of work is executed twice with the same sealed input artifact; both executions produce output artifacts that satisfy the unit's closure criterion.

**FR-040**
- AC: The framework's state-persistence path performs no calls to any third-party service during runtime.

**FR-041**
- AC: A reader observing an artifact during a concurrent write sees either the pre-write content or the post-write content, never a partial state.

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

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-06 |
| Status       | Draft      |
