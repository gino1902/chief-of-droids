# EARS — Behavioral Requirements (T1)

## Contents
- EARS patterns
- Pattern selection heuristics
- FR drafting rules
- Constraints drafting rules
- ERR drafting rules
- Phase 4 hygiene checks

---

## EARS patterns

| Pattern | Template | When to use |
|:--|:--|:--|
| Ubiquitous | `The <system> SHALL <action>.` | Always-true behaviors; system-level properties |
| Event-driven | `WHEN <trigger> the <system> SHALL <action>.` | Responses to external events or inputs |
| State-driven | `WHILE <state> the <system> SHALL <action>.` | Behaviors active during a persistent condition |
| Unwanted Behavior | `IF <condition> THEN the <system> SHALL <action>.` | Error cases, guard conditions, threat mitigations |
| Optional Feature | `WHERE <feature> is included the <system> SHALL <action>.` | Conditional or licensed capabilities |

RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) do not appear in EARS statements. Use `SHALL` for all mandatory behavior in EARS.

---

## Pattern selection heuristics

| Substrate signal | Pattern |
|:--|:--|
| "always", "at all times", "continuously", "invariant" | Ubiquitous |
| "when", "upon", "after", "on receipt of", "triggered by", "in response to" | Event-driven |
| "while", "during", "as long as", "in state", "when in mode" | State-driven |
| "if … then", "in case of", "on failure", "on error", "invalid", "unauthorized", "exceeds" | Unwanted Behavior |
| "if the feature is enabled", "when configured for", "optionally", "licensed" | Optional Feature |

When multiple patterns fit, prefer the most specific one. Ubiquitous is the fallback when no trigger, state, or condition is present.

---

## FR drafting rules

- One `SHALL` statement per FR-NNN entry. Split compound behaviors into separate entries.
- Scope: behaviors of the subject component itself — not behaviors expected of external systems.
- If substrate uses RFC 2119 language for a functional behavior, translate to EARS on output.
- Do not mix EARS `SHALL` and RFC 2119 keywords (`MUST`, `SHOULD`) in the same statement.
- Group by logical area if more than five entries; grouping is for readability, not an ID boundary.

---

## Constraints drafting rules

Constraints are properties of the artifact that hold outside any specific runtime event. Distinguished from FR by the binary test below.

### FR vs CON — binary decision test

| Test | Outcome |
|:--|:--|
| The requirement can be falsified only by observing the system at runtime (event, invocation, response) | FR |
| The requirement can be falsified by static inspection of the artifact (code, config, file content, structure) without running the system | CON |
| Both tests pass | Apply the tie-breaker rules below |

Operational distinction:
- **FR** = response to an event, trigger, or invocation. The system **does** something at runtime.
- **CON** = property of the artifact itself. The system **is** something.

### Tie-breaker when both tests pass

When a requirement is verifiable BOTH by static inspection AND by runtime observation, classify as follows in order — first match wins:

| # | Tie-breaker | Outcome |
|:-:|:--|:--|
| 1 | Substrate sentence contains an EARS trigger word (`WHEN`, `IF`, `WHILE`, `WHERE`) | FR |
| 2 | Substrate sentence describes a placement, location, routing target, or composition ("contains", "is routed at", "resides in", "comprises", "is declared at") | CON |
| 3 | Substrate sentence describes an obligation that holds without an event ("SHALL be disjoint", "SHALL be one-way", "SHALL win", "SHALL be retained") | CON |
| 4 | Substrate sentence describes a one-shot action with an observable response ("emit", "write", "load", "prompt", "execute") | FR |
| 5 | None of the above apply | Default to CON; emit Warning |

The tie-breaker is mechanical and applied in order. Do not skip rows. If row 1 matches, the requirement is FR regardless of whether rows 2 or 3 would also match.

### Worked examples

| Substrate text | Classification | Rationale |
|:--|:--|:--|
| "The framework SHALL prompt the user with 'Which project?'" | FR | Runtime event observable in chat output |
| "The dispatcher SHALL contain only bootstrap, sentinel verify, and tool routing." | CON | Static inspection of dispatcher content; tie-breaker row 2 |
| "WHEN bind succeeds the framework SHALL emit an anchor." | FR | Event-driven runtime response; tie-breaker row 1 |
| "Composition between tiers SHALL be one-way." | CON | Architectural invariant; tie-breaker row 3 |
| "Trigger phrases SHALL be disjoint between workspace and project skill sets." | CON | Verifiable by corpus scan; tie-breaker row 3 |
| "WHEN a workspace skill's trigger phrase is edited the workspace skill version SHALL receive a major version bump." | FR | Triggered by an edit event; tie-breaker row 1 |
| "Always-on tools (filesystem, git, fetch) SHALL be routed at Layer 1." | CON | Placement/routing target declaration; tie-breaker row 2 |
| "The framework SHALL execute a corpus-wide trigger collision scan." | FR | Action verb without placement signal; tie-breaker row 4 |
| "Workspace skills SHALL reference only other workspace skills." | CON | Static invariant on artifact references; tie-breaker row 3 |
| "The framework SHALL load workspace CLAUDE.md, project CLAUDE.md, and project brief." | FR | Acquire-shape action verb; tie-breaker row 4 |

### ID and pattern rules

- S1: use `FR-NNN` IDs continuing the FR sequence; section heading `## Constraints`.
- S2: use `CON-NNN` IDs; section heading `## Constraints`.
- Choose the EARS pattern that best matches the constraint; Ubiquitous and State-driven are most common.
- If the constraint is implementation-neutral (a non-negotiable property), use Ubiquitous.

---

## ERR drafting rules

Error handling requirements use Unwanted Behavior EARS exclusively.

Entry format:
```
**ERR-NNN** — IF <action> does not complete successfully THEN the <system> SHALL <observable error response>. → <FR-NNN>
```

The cross-link `→ FR-NNN` identifies the functional requirement whose error path this covers. The `<action>` token names the FR's SHALL action verb at the contract level — no mechanism naming (file, network, MCP, database) is permitted in the ERR text. Substitution of the underlying transport SHALL NOT require ERR rewording.

### Contract-shape coverage matrix

For each FR, classify the SHALL action by its contract shape. Mandatory ERR coverage is derived from the shape, not from any implementation it implies.

| Contract shape | Example action verbs | Mandatory ERR |
|:--|:--|:--:|
| Acquire — obtain a value the FR depends on | read, load, fetch, retrieve, resolve | yes |
| Mutate — change observable state | write, persist, record, update, delete, create | yes |
| Validate — assert a predicate over inputs | verify, check, compare, scan, match | yes |
| Solicit — wait on an external party | prompt, request, ask, await | yes |
| Transform — derive an output from inputs | compute, derive, calculate, build, generate | yes when inputs are externally sourced |
| Emit — produce a signal with no return contract | emit, surface, announce, broadcast, log | no |
| Select — choose from a known set | select, prefer, resolve from set | no |
| Declare — assert an artifact-level invariant | contain, comprise, route, expose (statically) | no |

If an FR action verb does not fit any row, classify under the closest shape and emit Warning for user review. Do not infer a shape from implementation context.

**Mandatory drafting (Phase 2):** FRs whose contract shape is Acquire, Mutate, Validate, Solicit, or Transform-with-external-inputs MUST have a paired ERR drafted in the same Phase 2 pass as the FR itself. The Phase 4 hygiene check is an audit, not a drafting step — it surfaces missing pairs but does not produce them.

**Explicit opt-out:** if an FR of mandatory-coverage shape is intentionally not paired with an ERR (because the failure mode is trivial, the action is best-effort, or the FR is a no-op wrapper), attach an inline rationale to the FR entry on the same line: `(no ERR — rationale: <reason>)`. Absent rationale + absent ERR is a Phase 4 Warning. With rationale, no Warning fires.

### Other rules

- One error condition per ERR-NNN entry.
- The response action must be concrete: log, reject, retry, surface to caller, roll back. "Handle the error" is not acceptable.
- If no corresponding FR exists for an ERR entry, emit Warning (orphan ERR).
- An FR whose contract shape mandates coverage but lacks an ERR entry AND lacks an opt-out rationale → Warning per missing ERR.

---

## Phase 4 hygiene checks (T1)

| Check | Severity |
|:--|:--|
| Each FR and CON entry uses a legal EARS pattern | Warning |
| Each ERR entry uses Unwanted Behavior EARS exclusively | Warning |
| Each ERR entry contains a cross-link to an existing FR | Warning if missing or target not found |
| Each FR and CON entry contains exactly one `SHALL` | Warning if compound (more than one `SHALL`) |
| RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) absent from EARS statements | Warning if present |
| Each FR satisfies the FR-test (falsified only by runtime observation) | Warning if requirement satisfies CON-test instead |
| Each FR classified as Acquire / Mutate / Validate / Solicit / Transform (external inputs) has corresponding ERR coverage OR an inline opt-out rationale | Warning if both missing |
| ERR text does not name implementation mechanisms (file, network, MCP, database) | Warning if mechanism leaks into ERR statement |
