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

### Foundational rules

- One `SHALL` statement per FR-NNN entry. Split compound behaviors into separate entries.
- Scope: behaviors of the subject component itself — not behaviors expected of external systems.
- If substrate uses RFC 2119 language for a functional behavior, translate to EARS on output.
- Do not mix EARS `SHALL` and RFC 2119 keywords (`MUST`, `SHOULD`) in the same statement.
- Group by logical area if more than five entries; grouping is for readability, not an ID boundary.

### Granularity rules — fold vs split

"One SHALL per FR" is necessary but not sufficient. Cascade operations, multi-artifact actions, and tightly-coupled action+consequence pairs all satisfy single-SHALL at both a coarse and a fine rendering. The three rules below resolve the fold-vs-split choice deterministically. They apply at the substrate-walk stage of Phase 2 before SHALL statements are written.

**G-1 — One FR per `(trigger × atomic outcome)` pair.** An outcome is *atomic* if a single acceptance criterion can verify it. If verifying the outcome requires two independent assertions, the FR carries two outcomes and must split.

**G-2 — Cascades split by trigger, not by step.** When step *n+1* fires *only as the deterministic consequence* of step *n* completing — no separate predicate, no independent failure mode — it folds into step *n*'s FR. When step *n+1* has its own predicate (different `WHEN`/`IF` antecedent), the trigger differs from step *n*'s and the FR splits.

**G-3 — Multi-artifact symmetry folds.** When one trigger acts on N artifacts of the same kind under a shared failure contract ("all or none"), it renders as one FR with N targets, not N FRs.

### Sub-rules

**G-1a — Negative outcomes.** A negative outcome (absence of output, absence of side effect) renders as an FR only when substrate explicitly names the absence as a contract step. Its AC is the negative assertion (`"no tokens emitted before X"`). It carries no ERR pair — emit `(no ERR — rationale: pass-through; no observable failure distinct from upstream FR-NNN)`.

**G-1b — Dual-aspect rendering.** When a substrate statement can be characterized as both active dispatch behavior AND a structural invariant, render BOTH: an FR for the action (`WHEN <trigger> the system SHALL <act>`) AND a CON for the invariant (`<X> SHALL be <invariant>`). Folding into either alone drops contract coverage on the un-rendered axis. G-1b applies when substrate names both flavors as separate sentences (e.g., "Precedence rule: workspace tier wins" + "Dispatcher implements fail-fast tier resolution"); the FR vs CON tie-breaker below selects the primary placement when only one flavor is named.

**G-2a — Genuine vs trivial predicates.** A predicate is *genuine* only when it can return false at a moment the prior step's predicate cannot. `WHEN loads complete` is genuine because all three loads can succeed AND verification can still fail (file loaded but empty). `WHEN step n returns nominally` is trivial and does not count as a separate trigger.

### Decision table

For each candidate FR boundary in substrate, walk this table in order; first decision wins.

| # | Question | If yes | If no |
|:-:|:--|:--|:--|
| Q1 | Does the candidate share a trigger with the prior step? | Continue to Q2 | **Split** (different trigger) |
| Q2 | Is the candidate the deterministic consequence of the prior step (no genuine predicate per G-2a)? | **Fold** (G-2 consequence) | Continue to Q3 |
| Q3 | Is the candidate's outcome verifiable by a single AC that also verifies the prior step? | **Fold** (G-1 atomic) | **Split** (G-1 independent AC) |
| Q4 | When the candidate is one trigger over N artifacts: do all N artifacts share kind + failure semantics? | **Fold** across targets (G-3) | **Split** per target |

### Worked examples — chief-of-droids two-tier substrate

| Substrate text | Decision walk | Rendering |
|:--|:--|:--|
| "load `chief-of-droids/CLAUDE.md`, `<project>/CLAUDE.md`, `<project>/brief.md`" (one trigger, same kind, all-or-none failure: "halt if any fails") | Q4 yes | **1 FR**, 3 targets in SHALL clause |
| "Verify all three loaded; halt with clear error if any fails" after the 3-file load | Q1 shares trigger? No — `WHEN loads complete` is genuine (G-2a; verify can fail when load succeeded). Split. | **1 FR**, separate from load FR |
| "On any mismatch, reload that file and update sentinel" | Q1 shares trigger (SHA-mismatch detected). Q2 update is deterministic consequence of reload (no genuine predicate). Fold. | **1 FR** combining reload + update |
| "`creating-skills` runs corpus-wide trigger collision scan; hard reject on conflict" | Q1 shares trigger? Reject fires on `IF collision detected`, a separate predicate from `WHEN scan runs`. Split. | **2 FRs** (scan + hard-reject) |
| "Precedence rule: workspace tier wins" (invariant) PLUS "Dispatcher implements fail-fast tier resolution (workspace match → exit)" (active dispatch) — two substrate sentences, two flavors | G-1b: both flavors named in substrate. | **1 FR** (workspace-first dispatch) + **1 CON** (precedence invariant) |
| "Proceed silently to user request" | Negative outcome named in substrate as a step → G-1a. | **1 FR**, AC = negative assertion, no ERR pair |
| "Sentinel schema implemented including `resolved_skills` on bind" | Q1 shares trigger with sentinel write (bind completes). Q2 deterministic? Q3 resolved_skills correctness has an AC independent of sentinel-schema-write AC. Split. | **1 FR** for resolved_skills population, separate from sentinel-write FR |

### Anti-patterns

- **Splitting multi-artifact reads under one trigger.** Rendering "Load workspace CLAUDE.md" + "Load project CLAUDE.md" + "Load project brief" as three FRs violates G-3 when failure is all-or-none.
- **Folding action + independent-failure consequence.** Rendering "Load files AND verify AND write sentinel" as one FR violates G-2 when verify can fail when load succeeded, or write can fail when verify passed.
- **Dropping the FR for a dual-aspect rule.** Rendering only the CON for "workspace-tier wins" while dropping the dispatcher's active behavior violates G-1b — the active resolver path becomes contract-invisible.
- **Omitting negative-outcome FRs that substrate names.** Dropping "proceed silently" when substrate carries it produces an incomplete contract — violates G-1a.
- **Splitting a deterministic-consequence pair.** Rendering "reload" and "update sentinel" as two FRs when update fires unconditionally on reload violates G-2.

### Out of scope for granularity rules

These axes affect total requirement count but are **not** decided by G-1/G-2/G-3:
- In-scope vs out-of-scope inclusion (does this capability belong in this requirements doc at all) — owned by Phase 1 scope extraction.
- ERR coverage spread — owned by the contract-shape coverage matrix below.
- CON / IR / DR / NFR enumeration — owned by their respective derivability rules.

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

When a requirement is verifiable BOTH by static inspection AND by runtime observation, classify as follows in order — first match wins. **Note:** the tie-breaker selects placement for a single substrate statement. When substrate names both flavors of the same rule (active behavior AND invariant) in separate sentences, FR drafting rule G-1b applies instead and renders both.

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
| FR boundaries follow the granularity decision table (Q1–Q4) | Warning if a candidate boundary fails the walk |
| Compound multi-artifact FRs (G-3 fold) declare every target in the SHALL clause | Warning if fold leaves targets implicit |
| Cascade FRs (G-2 fold) name both the action and its deterministic consequence in the SHALL clause | Warning if the consequence is invisible at output |
| Substrate carries both active and invariant flavors of the same rule (G-1b); both FR and CON rendered | Warning if only one flavor is rendered |
| Negative-outcome FRs (G-1a) carry the `(no ERR — rationale: pass-through ...)` opt-out | Warning if absent |

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
