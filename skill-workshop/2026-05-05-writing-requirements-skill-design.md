# Writing-requirements Skill — Design Handoff

## Status

> ⚠️ Stale — verify before use. The skill has shipped under project scope at `skill-workshop/.claude/skills/writing-requirements/`, not the user-scope path described below. The Discovery and Distribution rows in §Runtime and discovery no longer reflect reality.

Design phase complete. Refinement session 2026-05-05 consolidated 15 structural locks plus one pre-decision on folder layout. Nine items remain for in-draft resolution. Ready to draft `SKILL.md` in next session.

## Origin

Build `writing-requirements` skill — produces a structured software requirements artifact for one deployable component using RFC 2119 + EARS, paired with a per-pass diagnostic report.

The original framing was "lightweight"; the consolidated design is industrial-strength: 14 sections per artifact, 7 phases with full rule lists, 7-criteria quality scorecard, ID stability across iterations, dual-output write semantics. Match the example faithfully and the artifact is heavyweight by definition.

## Scope

| Element | Value |
|:--|:--|
| Skill name | `writing-requirements` |
| Skill kind | Transformation — markdown input → structured requirements artifact + diagnostic report |
| Subject | One deployable component (container, module-as-container, service, app) |
| Domain | Software requirements |
| Out of scope | Business requirements (owned by `analyzing-business-cases`); brainstorming (owned by `brainstorming-ideas`); rendering (owned by `writing-docs`); multi-container module specs (one invocation per container) |
| Composition | Stand-alone — does not call or get called by other skills; user composes manually |

## Locked design

### Runtime and discovery

| Element | Decision |
|:--|:--|
| Runtime | Claude Code only (Agent Skills mechanism) |
| Desktop role | Edit input artifacts and review outputs in chat; never invokes the skill |
| Discovery | User scope — `~/.claude/skills/writing-requirements/` |
| Source of truth | Workspace at `chief-of-droids/skills/writing-requirements/` |
| Distribution | Symlink from user scope to workspace path |
| HOW-TO-TRIGGER entry | None; skill is invisible to Desktop routing |

### Invocation

| Element | Decision |
|:--|:--|
| Trigger pattern | `writing-requirements <topic-slug> from <path>` |
| Topic slug rule | `^[a-z0-9-]+$`; not matching → hard-fail (no normalization) |
| Path semantics | Absolute or relative-to-cwd; resolved at parse time |
| Path with whitespace | Required to be quoted (single or double quotes) |
| Existence check | Resolved input path must exist; hard-fail if not |
| Substrate file type | `.md` only; other extensions → hard-fail at Phase 0.8 with remediation "Extract substrate to markdown first" |
| Parse ambiguity | Multiple `from` tokens or other ambiguity → hard-fail with canonical pattern message |

### Subject scope

| Element | Decision |
|:--|:--|
| Subject | One deployable component per invocation |
| Acceptable subject naming | "container", "module", "service", "app" — terminology is irrelevant; what matters is exactly one deployable unit |
| Module-as-one-container | In scope |
| Multi-container modules | Out of scope; user invokes the skill once per container, composes module-overview separately |
| Other components in the architecture | Appear in §3 Actors & Consumers as upstream/downstream actors (system or human) |
| Substrate scope-consistency check | None — substrate is authoritative; if user feeds module-shaped substrate, output is container-shaped regardless; user iterates if incoherent |

### Project and output resolution

| Element | Decision |
|:--|:--|
| Project anchor | Code's cwd at invocation |
| CLAUDE.md walk | From cwd, walk up; first match wins; halt at filesystem root with hard-fail if none found |
| `Default repo:` extraction | First `Default repo:` line in resolved CLAUDE.md; first backticked path after the colon |
| Multiple `Default repo:` lines | First wins; log INFO entry |
| Path validation | Extracted repo path must exist on disk; hard-fail otherwise |
| Output dir | `<repo>/requirements/<topic-slug>/` |
| Output files | `requirements.md` and `report.md` in that directory |
| Title source vs slug | Substrate provides container name (Title field at top of `requirements.md`); slug provides directory name; divergence allowed; skill does not enforce slug-title consistency |
| Cross-project input behavior | **Temporary** — cwd drives output regardless of input file location; revisit when use cases surface |

### Phase model

Seven phases, strictly sequential, no parallelism, no skips. All phase work in memory; no writes occur before Phase 6 completes successfully.

| Phase | Name | Validation only? | Outputs |
|:--|:--|:--|:--|
| 0 | Pre-flight | yes | (setup; no content) |
| 1 | Framing | no | §1 Title + Purpose; §2 Scope (in/out); §3 Actors & Consumers |
| 2 | Drafting | no | §5 FR; §6 IR; §7 DR; §8 NFR; §9 SEC; §10 ERR; §11 OBS |
| 3 | Vocabulary | no | §4 Glossary |
| 4 | Taxonomy hygiene | yes | (validation only) |
| 5 | Verification | no | §12 AC; §13 Quality Criteria scorecard |
| 6 | Format | no | §14 Version block; format pass across all sections |

Phase order is reasoning order; section order is presentation order. Glossary is produced in Phase 3 but appears as §4.

Each phase emits a closure line in its report section, always emitted even at zeros:

```
Outstanding: N blocking, M warnings, K info
```

#### Phase 0 — Pre-flight steps

| Step | Action | Failure mode |
|:--|:--|:--|
| 0.1 | Parse trigger args (slug + path); detect ambiguity | Hard-fail with canonical-pattern message |
| 0.2 | Validate slug regex `^[a-z0-9-]+$` | Hard-fail |
| 0.3 | Resolve input path; existence check | Hard-fail |
| 0.4 | CLAUDE.md walk from cwd to filesystem root | Hard-fail if none found |
| 0.5 | Extract first `Default repo:` line; backticked path; existence check on disk | Hard-fail if absent, malformed, or path missing |
| 0.6 | Resolve output dir `<repo>/requirements/<slug>/`; create if absent | Hard-fail on permission error |
| 0.7 | Read prior `requirements.md` if present (input for ID stability + version increment) | Soft Warning if unreadable; proceed as no-prior |
| 0.8 | Read input substrate file; reject non-`.md` extension | Hard-fail |

#### Phase 4 — Taxonomy hygiene checks

All findings emit Warning per the locked diagnostic-vs-gating principle.

| Check | Source |
|:--|:--|
| Each FR uses a legal EARS pattern (Ubiquitous / Event-driven / State-driven / Unwanted Behavior / Optional Feature) | Syntax routing |
| Each ERR uses Unwanted Behavior EARS and cross-links to a FR error response | Syntax routing |
| Each IR / NFR / SEC / OBS contains an RFC 2119 keyword | Syntax routing |
| Each DR / TR uses contract / rule table form (no RFC 2119, no EARS) | Syntax routing |
| ID format `<CAT>-NNN` valid per category | ID convention |
| ID sequence dense per category — no gaps | ID convention |
| Vocabulary in requirements matches Glossary entries; flag terms used but not defined | P3 output |
| No two requirements within a category share an ID | ID convention |

#### Phase 5 — Verification outputs

Single phase, dual outputs.

| Output | Source |
|:--|:--|
| §12 Acceptance Criteria | Per-requirement AC walk; Warning if requirement has no derivable AC |
| §13 Quality Criteria scorecard | Per-requirement scoring against 7 criteria — see scoring table |

Scorecard scoring rules:

| Criterion | Auto-scorable? | Approach |
|:--|:--|:--|
| Atomic | Yes | Count MUST/SHOULD/MAY per requirement; >1 → ✗ |
| Unambiguous | Partial | Flag terms not in Glossary |
| Verifiable | Yes | AC exists for this ID? ✓ / ✗ |
| Necessary | No | Substrate-dependent (source identification) — N/A |
| Feasible | No | Requires engineering review — N/A |
| Traceable | Yes | ID format valid? ✓ / ✗ |
| Bounded | Heuristic | Numeric value / time / volume / retention present? Flag if absent in NFR-class requirements |

5 auto-scored + 2 N/A; heuristic calibration (Bounded thresholds, Unambiguous detection) resolves in-draft.

### Section list — `requirements.md`

14 sections, all always rendered, `N/A` if substrate signal absent. Methodology boilerplate (RFC 2119 keyword definitions, EARS pattern table, generic Quality Criteria definitions) is documented in `SKILL.md`, never rendered in the artifact.

| # | Section | Owning phase |
|:--|:--|:--|
| 1 | Title + Purpose | 1 |
| 2 | Scope (in / out) | 1 |
| 3 | Actors & Consumers | 1 |
| 4 | Glossary | 3 |
| 5 | Functional Requirements (FR) | 2 |
| 6 | Interface Requirements (IR-IN / IR-OUT) | 2 |
| 7 | Data Requirements (DR + TR) | 2 |
| 8 | Non-Functional Requirements (NFR) | 2 |
| 9 | Security (SEC) | 2 |
| 10 | Error Handling (ERR) | 2 |
| 11 | Observability (OBS) | 2 |
| 12 | Acceptance Criteria (AC) | 5 |
| 13 | Quality Criteria scorecard | 5 |
| 14 | Version block | 6 |

### Syntax routing per category (Phase 2)

| Category | Syntax |
|:--|:--|
| FR | EARS — all 5 patterns |
| ERR | EARS — Unwanted Behavior dominant; cross-link to FR error responses |
| IR | RFC 2119 statements; Event-driven EARS where naturally fits |
| NFR | RFC 2119 + measurement column; no EARS |
| SEC | RFC 2119; Unwanted Behavior EARS where applicable |
| OBS | RFC 2119 |
| DR | Contract tables; no RFC 2119, no EARS |
| TR | Rule tables (input → rule → output); no RFC 2119, no EARS |

### ID convention

| Element | Decision |
|:--|:--|
| Format | `<CATEGORY>-NNN`, three-digit zero-padded; IR splits to `IR-IN-NNN` / `IR-OUT-NNN`; transformations use `TR-NNN` |
| Sequence | Per-category, dense; gaps allowed when prior pass deletes an ID |
| Stability across iterations | Skill reads prior `requirements.md` if present and preserves declared IDs; new requirements get next sequence per category; removed requirements vacate the slot — no tombstones |
| Renumbering | Never automatic; user-driven only |
| Stability mechanism | Substrate-declared IDs — skill matches regex `\b(FR\|IR-IN\|IR-OUT\|IR\|DR\|TR\|NFR\|SEC\|ERR\|OBS)-\d{3}\b` anywhere in substrate; matched IDs preserved on output, attached to nearest requirement-shaped block; undeclared requirements get next sequence per category |
| Canonical iteration mechanism | User feeds prior `requirements.md` (with edits) back as substrate; IDs round-trip naturally. Free-form substrate without IDs starts fresh; ID stability is opt-in via substrate format |

### Quality and severity model

| Element | Decision |
|:--|:--|
| Axes | output-shape requirement / input-substrate detection / gap-policy = `N/A` |
| Severity — Blocking | Emitted content violates a mandatory output-shape rule |
| Severity — Warning | Substrate gap yielded `N/A` or default assumption |
| Severity — Info | Trace events, scope-signal detection, conditional category gating |
| Diagnostic vs gating | Severity is purely diagnostic; never gates writes |
| Substrate-gap default | `N/A` in section; no `🔲 To be defined` flags, no scaffolding |

Severity assignment for Phase 4 hygiene findings and Phase 5 scorecard findings — in-draft.

### Failure model

| Type | Trigger | Behavior |
|:--|:--|:--|
| Hard fail | Input/output unreachable, parse error, CLAUDE.md walk fails, `Default repo:` missing or invalid, non-`.md` substrate, write error | Halt; chat-visible error; no outputs; DoD not met |
| Soft issue | Substrate gap, ambiguous input, defaulted assumption, scope signal absent | Recorded in report; phase continues; both files written at end |

Hard-fail message format:

```
[writing-requirements] Phase <N> hard fail: <reason>
  context: <relevant path or arg>
  remediation: <one-line suggestion>
```

### Iteration model

| Element | Decision |
|:--|:--|
| Pass model | Stateless — same seven-phase pass per invocation |
| Inheritance | Override; input drives current pass; prior decisions in output get re-evaluated |
| Convergence | User-driven across iterations; skill never claims convergence |
| DoD per iteration | All seven phases complete + both files written |
| ID stability | Opt-in via substrate-declared IDs; see ID convention |

### Default substrate-gap behavior

| Missing | Skill behavior |
|:--|:--|
| Scope signal (regulatory, SLA, multi-actor, interface, etc.) | `N/A` in relevant section; Warning entry in report |
| Glossary | Auto-extract candidates from input; flag as Warning (auto-derived, user review required) |
| §2 Out of Scope | Bounded extraction from explicit negation language ("not handled here", "outside this", "downstream", "upstream", "out of scope", "owned by"); no synthesis when negation absent — empty section + Warning |
| §2 In Scope | Bounded extraction from positive scope language ("in scope", "covers", "responsible for", "handles"); symmetric with Out of Scope; `N/A` + Warning if absent |

### Version handling

| Element | Decision |
|:--|:--|
| Version block location | Bottom of both `requirements.md` and `report.md` (per CLAUDE.md mandate) |
| Shared vs independent | Shared — same value on both files per pass |
| Version source | Existing `<repo>/requirements/<topic>/requirements.md` if present |
| Initial value | `0.1` (no prior output exists) |
| Increment rule | Rightmost segment +1 per pass (e.g., `0.1 → 0.2 → 0.3`); user manually promotes major boundaries |
| Status field | Always `Draft` from skill; user manually flips to `Review` / `Final` |
| Last Updated | Pass timestamp |
| Input artifact's version | Ignored for output versioning |

### Write semantics

| Element | Decision |
|:--|:--|
| Atomicity | In-memory atomic — all phases run in memory; no writes occur before Phase 6 completes successfully |
| Phase 6 write order | `requirements.md` first, then `report.md` |
| Write failure on `requirements.md` | Abort; no `report.md` write attempted; prior iteration intact |
| Write failure on `report.md` after `requirements.md` succeeded | Hard-fail surfaced; current `requirements.md` reflects current pass; prior `report.md` remains; user detects via shared-version-block mismatch and re-runs to converge |
| Mid-skill failure before Phase 6 | Prior iteration's files left intact; no writes attempted |
| Commit gate | Suppressed for this skill (declared exception in `SKILL.md`); user commits post-skill |
| Reports across iterations | Overwritten per iteration; user owns commit discipline for history |

### Streaming

Per-phase chat output, entry headers only:

```
→ Phase 0 — Pre-flight
→ Phase 1 — Framing
→ Phase 2 — Drafting
→ Phase 3 — Vocabulary
→ Phase 4 — Taxonomy hygiene
→ Phase 5 — Verification
→ Phase 6 — Format
✓ Wrote requirements.md (v0.2)
✓ Wrote report.md (v0.2)
```

No exit lines, no progress within phase, no content streamed. Hard-fail streaming format — in-draft.

### Frontmatter (Code Agent Skills)

| Element | Decision |
|:--|:--|
| Description shape | Directive opening + scope (mention "one deployable component / container") + invocation form + iteration note (final wording at draft time) |
| `allowed-tools` | Filesystem read/write only |
| Tools NOT used | Web fetch, shell, MCP servers, code execution |

### Skill folder layout (pre-decision)

`SKILL.md + references/` from the start. The locked design has matured to industrial-strength scope; SKILL.md will almost certainly cross 600 lines. Plan for split rather than re-organizing post-draft.

Candidate references:

| File | Content |
|:--|:--|
| `output-shape.md` | Per-section content rules, syntax routing per category |
| `verification-rules.md` | Phase 4 hygiene + Phase 5 scorecard heuristics |
| `severity-model.md` | Blocking / Warning / Info definitions and assignment rules |
| `template-requirements.md` | Skeleton for `requirements.md` |
| `template-report.md` | Skeleton for `report.md` |

### CLAUDE.md updates required (workspace)

1. `## Skills Architecture` section — add inline exception clause naming `writing-requirements` as Code-targeted runtime exception.
2. Symlink install procedure for Code-targeted skills:
   ```bash
   ln -s ~/Workspace/chief-of-droids/skills/<skill-name> ~/.claude/skills/<skill-name>
   ```

Both updates are made when the skill ships, not before.

## Parked — resolve in-draft

| # | Item | Notes |
|:--|:--|:--|
| 1 | Phase rule lists recast under three axes | Original counts: P1≈10, P2≈9 (now per-category × 7), P3≈4, P4=8 (locked above), P5≈8 (now AC + scorecard), P6≈9. User reviews holistically at draft, not rule-by-rule pre-draft. |
| 2 | `report.md` format | Mark for revision when standard report format is established (separate concern). |
| 3 | Phase 5 scorecard scoring heuristics | Bounded thresholds, Unambiguous detection rules. Need calibration against actual artifacts. |
| 4 | Severity assignment for Phase 4 hygiene + Phase 5 scorecard findings | Pattern emerges naturally during draft. |
| 5 | Streaming format on hard-fail | `✗` line vs `→` replacement; failure block placement. |
| 6 | Title field extraction heuristic | First H1; fallback hierarchy (H2; frontmatter `title:`; slug + Warning). |
| 7 | Phase 1 framing detection rules | Detection patterns for Title, Purpose, In Scope, Out of Scope, Actors. |
| 8 | Frontmatter description final wording | Compose once SKILL.md draft surfaces actual operational language. |
| 9 | EARS pattern selection within FR / ERR | Heuristics for choosing among the 5 patterns based on substrate signals. |

Provisional `report.md` structure sketch (subject to revision under item 2):

```
# Report — <topic>

Roll-up: X blocking, Y warnings, Z info across 7 phases.

## Phase 0 — Pre-flight
[BLOCKING] <description> → <remediation>
[WARNING] <description> → <remediation>
[INFO] <description>

Outstanding: N blocking, M warnings, K info

## Phase 1 — Framing
...
```

## Design principles

These principles drove the locked decisions; preserve them when resolving parked items.

| Principle | Implication |
|:--|:--|
| Stateless transformation | Every invocation is a full pass; no detection of "first vs nth iteration"; no in-skill convergence logic |
| User-driven convergence | Skill provides diagnostics; user judges done-ness; skill never marks `Final` |
| In-memory atomicity | Failure leaves prior iteration intact for any failure before Phase 6; sequential write failures during Phase 6 surfaced explicitly via shared-version-block mismatch |
| Predictable structure | Conditional sections render with `N/A` rather than being omitted; closure line always emitted, even at zeros |
| Severity is diagnostic | Never gates writes; user iterates based on report content |
| Hard fail vs soft issue | Hard = halt, no outputs; soft = recorded, both files written |
| Override on iteration | Input drives current pass; ID stability opt-in via substrate-declared IDs |
| One deployable unit per pass | Subject is exactly one container/module-as-container/service/app; multi-container modules require separate invocations |
| Methodology in skill, not artifact | RFC 2119 / EARS / generic quality criteria definitions documented in `SKILL.md`; never rendered in artifacts |

| Field        | Value       |
|:--|:--|
| Version      | 2.0         |
| Last Updated | 2026-05-05  |
| Status       | Draft       |
