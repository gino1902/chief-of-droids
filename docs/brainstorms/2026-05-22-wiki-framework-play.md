# Play — Wiki Framework Architecture Definition

## Originating prompt

> You are a Senior Requirements Discovery Facilitator and Product Operating
> Model Analyst. Your job is to guide a user through a structured
> requirement-definition conversation, turning vague intent into clear,
> testable, prioritized requirements, while exposing assumptions, gaps,
> conflicts, constraints, and decision points.
>
> I want you to consider this session as a play between the user and Claude,
> using the `/brainstorming-ideas` skill.
>
> I need you to create the play that happened during this session.
>
> Play format policy you have to meet:
>
> - hook
> - when to trigger
> - why it matters
> - outcomes
> - how we conduct the play (conversation friction, gaps between chat begin
>   and end, best practices used to close gaps, to clarify)
> - the tradeoffs (nature of the tradeoff, Claude takes a step back for this
>   in order to categorize tradeoffs)
>
> The last point is of course the most important and the one for which
> session history has to be carefully analysed.

---

## Hook

A FRAMING.md exists. The user lists three things to discuss. The model resists answering those three. Instead it pressure-tests the framing itself, surfaces six better questions, and the user picks where to start. The session closes three sub-problems and produces a complete requirements doc with explicit residual risks and revisit triggers.

## When to trigger

- Vague-intent framing document exists; operational mechanics unspecified
- User can name "what to discuss" but not "what's actually at stake"
- High-leverage tensions are hidden behind the framing's stated topics
- Multi-layered design where decisions ripple across structure / process / storage
- User is a domain peer who tolerates challenge and demands directness

Don't trigger when: framing is already operational; user wants implementation steps; stakes are low (single feature, no cross-cutting impact).

## Why it matters

A framing document captures intent but rarely captures the actual hard questions. Answering "your three questions" wastes time confirming what the architect half-decided. The play inverts the flow: the model surfaces design forks; the user picks sequence. Catches upstream decisions before downstream ones, forces explicit choices on hidden assumptions, produces a requirements doc with traceable rationale, leaves a confidence map (what's locked, what's parked, what's risky).

## Outcomes

| Artifact | Count |
| :--- | :--- |
| Numbered decisions across 3 sub-problems | 30 (A.1–A.10, B.1–B.8, C.1–C.12) |
| Open items with explicit deferral rationale | 7 |
| Residual risks acknowledged in writing | 7 |
| Major mid-session simplifications | 1 (source-summary page dropped) |
| Architectural revisit triggers logged | 1 (markdown-first → claim-first conditions) |
| Canonical text fragments produced | 1 (entity definition) |
| Resume hints for next session | 1 |

Output format: `docs/brainstorms/YYYY-MM-DD-<topic>-requirements.md`.

## How we conducted the play

### Conversation friction observed

| Pattern | Where | What it produced |
| :--- | :--- | :--- |
| User said "I am lost" mid-thread | Challenge 4c on source-summary purpose | Triggered reset; produced the session's biggest simplification |
| User pushed back on dismissal | "Reassess your Dolt analysis" with link | Honest reconsideration; revealed an unconsidered architectural fork |
| User redirected synthesis-mode → deliberate-mode | "Go to challenge, one by one" | Slowed pace, deeper engagement per item |
| User answered different question than asked | M3 ingest-serialization vs hand-edits | Model separated tangled scenarios, re-asked |
| Brief interrupts ("resume session") | Between turns | State recap, no recovery overhead |

### Gaps between begin and end

| Begin state | End state |
| :--- | :--- |
| FRAMING.md with 3 stated topics + a wiki vision | 30 numbered decisions covering ingest, version, schema |
| Implicit assumption of "Claude reconciles contradictions" | Explicit defer-to-user posture with row-level approval artefact |
| Vague "Obsidian/Marp/Dolt to discuss" tools list | Markdown-first + git locked; Dolt declined with revisit triggers logged |
| 4 implicit page types | 3 explicit page types + sidecar pattern for sources |
| No correction path for typos | Full ingest for everything; convention-only enforcement |
| No formal residual-risk tracking | 7 named residual risks in the requirements doc |

### Best practices used to close gaps

1. **Pressure-test the framing before answering its questions.** Session opened by listing six high-leverage tensions hidden behind the framing's three stated topics; user picked first.
2. **Decompose tangled questions.** "Dolt vs git vs none" → storage substrate × versioning mechanism (two dimensions). "Hand-edits vs ingest" → serialization vs hand-edit-correction (two scenarios).
3. **Concrete drafts as forcing functions.** When schema discussion went abstract, the model proposed a concrete YAML → critiqued it → second-passed it → locked.
4. **Multi-pass refinement.** First pass = propose. Second pass = self-critique. Third pass = lock with explicit residual risks. Used for the page schema.
5. **Sequencing by dependency.** A → B → C across sub-problems; within each, upstream (detection, posture) before downstream (granularity, format).
6. **Defer with rationale.** Items punted always carried explicit reasons; "out of scope" never bare.
7. **Honest mistakes acknowledged mid-session.** "Correction to something I said earlier: source-summary body is not consulted by Claude after ingest" — no defensiveness, recompute downstream.
8. **Revisit triggers logged for provisional decisions.** Markdown-first locked with three named conditions that would reopen the choice.
9. **One question at a time, multi-select buttons.** Minimal typing; mutually exclusive options.

---

## Tradeoffs — the categorization

Stepping back: every individual decision in this session was an instance of one of **six tradeoff categories**. The categories matter more than the decisions; future revisits will be navigated by recognizing which category a question belongs to.

### T1. Strictness vs Friction

Governance rigour vs operational cost.

| Decision | Strict pole | Cheap pole | Chosen |
| :--- | :--- | :--- | :--- |
| A.4 Policy set | supersede (full audit) | replace (lossy) | All 3 available, user picks per-row |
| A.6 Approval | row-level edit | whole-report yes/no | row-level edit |
| A.7 Cross-row deps | block apply if dangling | warn-only | block |
| A.9 Stale-report | whole-wiki lock | revalidate at apply | whole-wiki lock |
| B.6 Hand-edits | ingest-only | freely allowed | ingest-only |
| B.7 Correction path | full ingest for typos | hand-edit fixes | full ingest |
| B.8 Enforcement | FS locks + hooks | convention only | convention only |

**Meta-observation:** consistently *strict on the design, weak on enforcement*. Convention is the relief valve. Sustainable only as long as the architect remains the bottleneck.

### T2. Performance vs Normalization

Where to put information so reads are cheap but writes don't drift.

| Decision | Normalized pole | Denormalized pole | Chosen |
| :--- | :--- | :--- | :--- |
| C.7 `sources[]` in front-matter | IDs only, lookup needed | Full {id, dates} objects | Denormalized |
| C.7 Drift handling | Lint / immutable | Trust posture | Trust + re-ingest as correction path |
| created/updated dates | Derive from sources[] | Store explicitly | Store explicitly |
| index.md | Derived view | Co-canonical | Derived view |

**Meta-observation:** denormalize where reads dominate (contradiction policy per ingest); normalize where reads are rare. Drift bounded not by infrastructure but by *the ingest pipeline being the only writer*. Cheap because that constraint already exists.

### T3. Determinism vs Flexibility

How much structure to enforce vs how much to leave for emergent convention.

| Decision | Determinism pole | Flexibility pole | Chosen |
| :--- | :--- | :--- | :--- |
| C.1 Page typology | Enumerated 4 types | Free string | Loose, 3 types, Claude-assigned |
| C.9 Subtype | Enumerated list | Replaced by description | Description (flexibility wins) |
| A.10 Temporal rule | Hard rule | Surface-only | Hard default + user override |
| C.2 Type assignment | Schema-required | Claude judgment | Claude judgment |

**Meta-observation:** loose everywhere *except interfaces between layers* (front-matter shape, report-table schema). Internal structure is loose; boundary contracts are strict.

### T4. Honesty vs Reader Experience

When the truthful answer is uglier than the convenient one.

| Decision | Honest pole | Convenient pole | Chosen |
| :--- | :--- | :--- | :--- |
| A.4 Conflict resolution | Show conflict | Reconcile silently | All policies available, no synthesis |
| A.10 Temporal rule | Surface dates only | "Older = reject" silent | Hard default + visible dates for override |
| C.6 Attribution placement | Per-claim footnotes | Page footer only | Section-level (middle ground) |

**Meta-observation:** never picked silent reconciliation. Every conflict-resolution choice preserved the conflict *somewhere* — in the page (supersede), in the report (defer), in front-matter (multi-source `sources[]`). The reader can always reconstruct what disagreement existed.

### T5. Build vs Reuse

Lean on existing tools or design from scratch.

| Decision | Build pole | Reuse pole | Chosen |
| :--- | :--- | :--- | :--- |
| B.1 Architecture | Claim-first DB | Markdown files | Markdown (reuse Obsidian/git) |
| B.2 Versioning | Custom mechanism | Git | Git |
| C.3 Source representation | Source-summary page | File + sidecar | Sidecar (reuse FS) |
| C.11 Cross-references | Manual section | Obsidian backlinks | Reuse backlinks |

**Meta-observation:** consistently reused commodity infrastructure (git, Obsidian, filesystem semantics); designed custom mechanics only where the existing tools couldn't fit (the report artefact, the row-approval model). Decided by "does this need invariants the tool can't enforce?"

### T6. Eager vs Lazy

When to compute vs when to store.

| Decision | Eager pole | Lazy pole | Chosen |
| :--- | :--- | :--- | :--- |
| index.md | Generated at apply | Generated on demand | At apply (eager) |
| `sources[]` dates | Materialized in page | Read from sidecar | Materialized |
| Backlinks | Stored in page | Computed by Obsidian | Computed |
| created/updated | Stored | Derived from sources[] | Stored |

**Meta-observation:** eager where Claude consumes during ingest (read-heavy contradiction policy); lazy where the reader consumes (Obsidian renders backlinks for free). The boundary is "who consumes this data."

---

### Meta-meta-observation

Across all six categories, one consistent posture:

> **Lock the strict choice on what the data IS. Loosen the choice on how it gets ENFORCED.**

Strict: ingest-only writes, row-level approval, denormalization for read efficiency, eager index generation, section-level provenance, no silent reconciliation.
Loose: convention-only enforcement, loose typology, free-text descriptions, Claude-judged assignments, hand-edit prohibition by social contract not file lock.

Works because the architect is a single bottleneck with strong discipline. Would not survive multi-user scaling — at which point **T1 (Strictness vs Friction)** and **T5 (Build vs Reuse)** reopen for a second pass.

---

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-05-22 |
| Status | Draft |
| Pairs with | `2026-05-22-wiki-framework-requirements.md` |
