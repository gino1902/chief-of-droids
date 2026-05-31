# Chief of Droids — Framework Requirements

Chief-of-droids is a model-in-the-loop framework — governance-first and contract-explicit — where the model executes within defined boundaries set by the human architect.
Governance and knowledge work sit in Claude Desktop. Execution sits mainly in Claude Code.
The execution contract is made explicit via a routing layer, MCP filesystem access, session hygiene, and a handoff mechanism. Claude Desktop is leveraged for its rich output layer with ephemeral artefacts.

The framework's evolution purpose is to make the execution contract for knowledge and code work explicit and durable: every unit of work has a declared identity, an input contract, an output contract, an attributable history, and an explicit closure criterion. The framework operates today for a single human operator and is required to admit a future evolution to multiple operators without rewriting its artifact contracts.

Requirements use RFC 2119 verbs (MUST / SHALL / MAY / MUST NOT). Every requirement satisfies the quality criteria stated in the final section.

## Glossary

Terms are defined in the context of this framework. Where a term is used elsewhere in this document, the meaning here governs.

| Term | Definition |
|:--|:--|
| **agent** | A bounded, ephemeral process acting on the operator's authority within a single session. An agent has no persistence and no authority of its own; its writes execute under the operator's permissions. Contrast with *operator*. |
| **artifact** | Any persistent output produced during a unit of work, including the input artifact, the output artifact, and any implementation files. |
| **boundary** | The set of write authorities that distinguish what each agent and the operator may modify. Expressed as a path-bound or scope-bound policy in design; specified at the property level in this document. |
| **canonical location** | A single location designated by the framework as the authoritative source for a particular kind of information. The framework's design forbids reading or writing the same kind of information elsewhere. |
| **closure criterion** | The explicit condition that, when satisfied, allows a unit of work to transition to the closed terminal state. Declared at the time the input artifact is sealed (GR-05). |
| **designated audience** | For any artifact, the agent or actor explicitly assigned to consume it. The drafting agent's input artifact has the executing agent as its designated audience; the executing agent's output artifact has the drafting agent or the operator as its designated audience. |
| **drafting agent** | The agent role responsible for producing the input artifact of a unit of work. |
| **executing agent** | The agent role responsible for consuming the input artifact, producing the implementation outputs, and producing the output artifact. |
| **governance configuration** | The set of versioned framework files that declare policies, skills, instructions, and surface specifications. Distinct from the artifacts of any particular unit of work. |
| **in-flight** | Describes a unit of work whose lifecycle state is not terminal — that is, work that has been declared but neither closed nor aborted. |
| **input artifact** | For a unit of work: the artifact written by the drafting agent and consumed by the executing agent at the start of execution. Carries the full input contract (intent, constraints, acceptance criteria, references, closure criterion). |
| **lifecycle state** | The current phase of a unit of work. The framework distinguishes non-terminal states (in-flight) from terminal states (closed, aborted); specific intermediate state names are design output. |
| **machine-verifiable** | Admits an automated check that can determine, without human judgment, whether content conforms to a declared structure. |
| **operator** | The human user of the framework. The only actor with authority and continuity across all sessions. The operator owns the filesystem, credentials, and merge decisions; agents act under the operator's authority. |
| **output artifact** | For a unit of work: the artifact written by the executing agent and consumed by the drafting agent or the operator on return. Carries the report of execution against the input artifact's closure criterion. |
| **role** | A named function within a unit of work (drafting agent, executing agent). A single agent session may serve different roles for different units of work. |
| **sealed input artifact** | An input artifact whose authoring phase has ended. No further modification of its content is permitted by any party until the unit of work reaches a terminal state. |
| **terminal state** | A lifecycle state from which no further transitions are allowed. The terminal states are *closed* and *aborted*. |
| **third-party service** | Any external service used as a runtime dependency by the framework itself for state persistence. Agents invoking external services (such as LLM APIs) during execution are not the subject of NFR-06: that requirement governs the framework's own state, not agent runtime behavior. |
| **unit of work** | A single declared, identified scope of work passing through the framework. The smallest unit to which lifecycle states, artifacts, and access rules apply. |

## Functional requirements

| ID | Requirement |
|:--|:--|
| FR-01 | The framework SHALL allow the operator to declare a unit of work and obtain a unique persistent identifier for it. |
| FR-02 | The framework SHALL allow each agent participating in a unit of work to produce the artifact designated to that agent's role. |
| FR-03 | The framework SHALL deliver each artifact produced for a unit of work to its designated audience without manual relay of the artifact's content by the operator. |
| FR-04 | The framework SHALL persist all artifacts and lifecycle state of in-flight units of work across termination of any agent session. |
| FR-05 | The framework SHALL support multiple units of work being in flight concurrently with no functional interference between them. |
| FR-06 | The framework SHALL prevent more than one agent from concurrently occupying any role within the same unit of work. |
| FR-07 | The framework SHALL support resumption of any in-flight unit of work in the role appropriate to its current lifecycle state. |
| FR-08 | The framework SHALL support transition of any unit of work to a terminal state by closure or by abort. |
| FR-09 | On abort of a unit of work, all artifacts produced for that unit before the abort SHALL be preserved in their state at the moment of abort, and the abort transition SHALL render those artifacts ineligible for consumption as inputs to other units of work. |
| FR-10 | The framework SHALL NOT permit execution of a unit of work to begin before that unit's input artifact has been sealed. |

## Access requirements

| ID | Requirement |
|:--|:--|
| AR-01 | Only the operator MAY initiate, authorize the start of execution for, abort, or close a unit of work. |
| AR-02 | The drafting agent for a unit of work SHALL have write authority over that unit's input artifact. |
| AR-03 | The executing agent for a unit of work SHALL have write authority over that unit's output artifact and over its execution outputs. |
| AR-04 | Each artifact of a unit of work SHALL have exactly one designated writing agent. |
| AR-05 | The operator SHALL have read access to all artifacts of all units of work at all lifecycle states. |
| AR-06 | Each agent SHALL have read access to the artifacts of the unit of work to which it is assigned and to the framework's governance configuration; agents SHALL NOT have read access to artifacts of units of work to which they are not assigned. |

## Governance requirements

| ID | Requirement |
|:--|:--|
| GR-01 | Each unit of work SHALL carry a unique persistent identifier from declaration through terminal state. |
| GR-02 | Each artifact SHALL be immutable from the moment its authoring phase ends until the unit of work reaches a terminal state. |
| GR-03 | The framework's policies, skills, instructions, and surface specifications SHALL be versioned. |
| GR-04 | The boundary between each agent's write authorities SHALL be expressed in a single canonical location reviewable by the operator without starting an agent session. |
| GR-05 | Each unit of work SHALL declare an explicit closure criterion at the time the input artifact is sealed. |
| GR-06 | Each artifact type SHALL have a declared structure that all reading and writing agents respect. |
| GR-07 | Each declared artifact structure SHALL be machine-verifiable. |
| GR-08 | Modifications to the framework's own policies SHALL follow a process distinct from modifications to artifacts of in-flight units of work. |
| GR-09 | The framework SHALL verify each artifact against its declared structure at the time the artifact is sealed and at the time it is delivered to its designated audience. |

## Observability requirements

| ID | Requirement |
|:--|:--|
| OR-01 | The lifecycle state of any unit of work SHALL be inspectable by the operator without starting an agent session. |
| OR-02 | All artifacts of any unit of work SHALL be inspectable by the operator without starting an agent session. |
| OR-03 | The history of lifecycle state transitions for any unit of work SHALL be preserved and inspectable. |
| OR-04 | Every write to any artifact SHALL be attributable to the agent that performed it. |
| OR-05 | Violations of the boundary defined by access requirements SHALL be detectable by the operator post-hoc. |
| OR-06 | The operator SHALL be able to enumerate all units of work in any lifecycle state without prior knowledge of their identifiers. |
| OR-07 | The framework SHALL provide a means for any reader of an artifact to verify whether the artifact's content has changed since the artifact was sealed. |
| OR-08 | The resource consumption of any unit of work execution — including, at minimum, LLM token usage and wall-clock execution time — SHALL be observable by the operator. |

## Non-functional requirements

| ID | Requirement |
|:--|:--|
| NFR-01 | The state and artifacts of any in-flight unit of work SHALL survive restart of the operator's machine. |
| NFR-02 | A failure during the execution of one unit of work SHALL NOT alter the state of any other unit of work. |
| NFR-03 | The framework's state SHALL be portable to a different operator machine without loss of in-flight units of work. |
| NFR-04 | The framework's input and output artifact contracts SHALL admit a future evolution to multiple operators by additive extension only — additions of optional fields or new artifact types — without removing, renaming, or making required any field present in the original contract. |
| NFR-05 | Re-execution of a unit of work given the same sealed input artifact SHALL produce an output artifact that satisfies the same closure criterion (functional reproducibility — outcome, not bit-for-bit). |
| NFR-06 | The framework SHALL operate without a runtime dependency on any third-party service for state persistence. |
| NFR-07 | Writes to any artifact SHALL be atomic with respect to operator-observable state. A reader SHALL NEVER observe a partial state of an artifact that is in the middle of being written. |

## Quality criteria

Every requirement in this document is held to the following criteria:

- **Non-ambiguous** — single defensible interpretation, RFC 2119 verbs, no weasel words ("appropriate", "reasonable", "as needed").
- **Complete** — each category covers its full scope without known gaps.
- **Design-independent** — no requirement names a specific technology, tool, file system layout, transport, or implementation choice.
- **Atomic** — each requirement is a single sentence asserting a single property; conjunctions, where present, are over the same property.
- **C4-friendly** — every requirement lives at System Context or Container level; none drills to Component or Code level.

## Explicitly out of scope

The following concerns are intentionally not requirements at this stage. They may be added later if scope evolves.

| Concern | Reason for exclusion |
|:--|:--|
| Quantified latency, throughput, or cost targets | Single-operator scope; perceived performance suffices and no SLA exists. Reconsider when there is more than one operator or a stated SLA. |
| Security requirements (encryption at rest, authentication mechanisms) | Inherited from the operator's operating system and version control system. The framework introduces no new attack surface that warrants additional requirements at this scope. |
| Specific schemas for input and output artifacts | GR-06 mandates that schemas exist and be declared; the schemas themselves are design output, not requirements. |
| Specific lifecycle state names beyond *terminal* and *non-terminal* | FR-08 mandates terminal-state transitions; the named intermediate states are design output. |
| Unit of work identifier format | GR-01 mandates uniqueness and persistence; the identifier format is design output. |
| Agent count, types, and roles beyond drafting and executing | The current contract is sufficient for the framework's stated scope. Additional roles can be introduced as derivatives of these two without altering the requirements. |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.2        |
| Last Updated | 2026-05-05 |
| Status       | Draft      |
