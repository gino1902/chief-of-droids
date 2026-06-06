# Play - Design a Tasks Graph Plan

> Inspired by: *Our Pattern Language*, UC Berkeley ParLab. Pattern: **Task Graph**.
> URL: https://patterns.eecs.berkeley.edu/?page_id=609

## Hook

A plan you want to be executed by agents must be a plan that brings prescriptiveness for predictability. This recipe fixes the dependency design shape, enables safe parallelism, ships per-task BDD and three suite-level rollups that verify your DAG, your exit criteria, and your critical path.

## When to trigger

- A concrete requirements doc exists that can serve as a test fixture for the recipe
- User expects a *reusable* artifact, not a one-off plan
- User requires strict prescriptiveness (mandatory fields, no optional structure)

**Don't trigger when:** the pattern source is too thin to constrain (then the requirements doc would have to supply structure); only one application is foreseen (recipe overhead unjustified); the user wants a plan, not a recipe; the example dominates the pattern's force (e.g. applying Task Graph to a 3-task project — overhead wins). Also don't trigger for interactive, model-in-the-loop work where a human drives each step and the model assists. That is a copilot workflow, not this autopilot recipe.

## Why it matters

Because the plan is executed by an agent — a skill, subagent, or claude.md-scoped session running inside Claude Code — prescriptiveness is the lever for predictability.

Every task's mandatory contract (fields, BDD, granularity, antecedents) leaves no interpretive gap for the agent to fill with hallucination, omission, or off-path improvisation. The plan design pattern dictates section structure, mandatory fields, and verification scenarios.

**Execution mode — autopilot, not copilot.** This recipe targets supervised autonomous execution. The human stays in the loop at the supervisory level: they author and approve the static plan up front, then monitor and approve at gates (§H plan approval, §C completion checks). Agents execute the locked DAG on rails. It is not a copilot recipe. It does not target interactive, model-in-the-loop work where a human drives the change step by step and the model assists turn by turn. The prescriptiveness lever (§D.2) only pays off when no human is correcting each step, so a copilot workflow would carry the authoring overhead without the return.

---

### Problem

How to structure an implementation plan as a static collection of atomic work items with dependencies, enabling efficient execution — in parallel where independent work can proceed concurrently, serially where prior work must complete first — given that tasks may have variable sizes and multiple input/output dependencies, and form a directed acyclic graph (DAG)?

### Context

Tasks with antecedents may only start when all their antecedents have completed. Handoffs happen *on completion* — partial progress doesn't stream between tasks. The graph is acyclic.

Implementation plans are authored statically at planning time and *do not evolve once work begins* — tasks do not spawn new dependent tasks during execution. Conditional tasks (executing based on an antecedent's outcome — e.g. "do X if review fails") are pre-declared in the plan.

### Forces

**Universal**

| Force | Tension |
| :--- | :--- |
| Task Graph vs Other patterns | Linear waterfall or recursive decomposition (epic→story→task) may be simpler and self-distribute the workload |
| Variable vs Uniform task size | Uniform-sized tasks easier to schedule and parallelize; mixed sizes ⇒ critical path dominated by the longest task |
| Large vs Small tasks | Very small tasks ⇒ planning overhead dominates real work; very large tasks ⇒ blocks parallelism |
| Project size vs Plan overhead | Project must be large enough to justify the planning overhead of building the DAG |
| Hardcoded plan vs Per-project plan | Hardcoded template = simpler but less applicable across projects; per-project plan from a recipe = more flexible, higher authoring complexity |

**Implementation** *(operate below the plan-authoring layer; not directly mapped in the recipe)*

| Force | Tension |
| :--- | :--- |
| Task breakdown vs Agent capacity | More tasks than concurrent agent slots enables scheduling; far fewer leaves capacity idle |
| Task granularity vs Context-loading & handoff overhead | Coarse-grained tasks reduce context-switching cost but worsen workload balance |
| Task granularity vs Agent startup latency | Same trade-off, viewed from per-invocation cost (skill activation, subagent spin-up) |

### Solution

Break the work into atomic tasks with explicit dependencies. The acyclic property removes deadlock risk *(provided the tasks are truly atomic — no circular blockers)*. Hidden dependencies may cause blockers or rework, so *every* dependency must be made explicit in the plan.

Three sub-patterns for breakdown:

- **Task Decomposition** — Identify atomic tasks that can execute concurrently.
- **Group Tasks** — Group tasks to identify temporal dependencies and truly atomic tasks.
- **Order Tasks** — Identify how tasks must be ordered to satisfy constraints among tasks.

And one for assessment:

- **Design Evaluation** — Apply per candidate plan to assess fitness against (1) agent capacity and task-overhead trade-off, (2) handoffs and task granularity in light of coordination cost, and (3) simplicity vs flexibility vs efficiency. May yield multiple iterations across alternative plans.

#### Solution components (separate from forces)

- **Execution Balancing.** The plan does *not* balance execution inherently. Execution is determined by the critical path through the slowest tasks. Bottleneck removal is the planner's responsibility: either (a) break a slow task into multiple parallel-eligible tasks at planning time, or (b) parallelize the task internally — spin up multiple agent instances — without changing plan topology.
- **Handoffs.** Either explicit deliverable handoff antecedent→dependent (artifact passed at completion), or control-flow synchronization on a shared artifact (review/approval gates). Execution-level concern; not mapped to the recipe.
- **Risk Handling.** Each task handles its own risks/failures; the project framework aggregates as appropriate (status reporting, escalation). Execution-level concern; not mapped.

### Tasks Graph pattern

A 2-D graph calculation on a grid of variable size. Each node `(m, n)` depends on `(m-1, n)` and `(m, n-1)`. The dependency pattern is fixed at design time; the grid size `M × N` is only known after project design.

Dependencies form anti-diagonals — within an anti-diagonal, tasks are mutually independent and parallel-eligible.

```text
Wave 0:  (0,0)
Wave 1:  (1,0) (0,1)
Wave 2:  (2,0) (1,1) (0,2)
Wave 3:  (3,0) (2,1) (1,2) (0,3)
...
Wave M+N: (M,N)
```

Wave number = `m + n`. Peak parallelism = `min(M, N) + 1`, reached at wave `min(M, N)`. Critical path length = `M + N + 1` tasks.

---

## The recipe

> Self-contained specification — apply this to any requirements doc to produce
> an implementation plan + task graph + BDD suite.

### §A — Implementation Plan Specification (mandatory sections)

A plan document conforming to this recipe contains, in order:

| Section | Content |
| :--- | :--- |
| **Goal** | One sentence stating the change-in-the-world the plan delivers. |
| **Source requirements** | Path(s) to upstream requirement doc(s) with version pin. |
| **Scope** | Two lists: in-scope and explicit-out-of-scope. |
| **Assumptions** | Conditions assumed true; if false, plan invalidated. |
| **Exit criteria** | The observable conditions that mean the plan is *done*. |
| **Tasks[]** | Ordered list of fully prescribed task records (see §B). |
| **Task graph** | Mermaid DAG showing antecedents; followed by a wave table listing parallel-eligible cohorts per wave. |
| **Critical path** | Longest cumulative-granularity chain identified explicitly. |
| **Bottlenecks** | `L` tasks on the critical path flagged with resolution option (a) or (b) per §B Granularity. |
| **Risks** | Inherited from requirements + new plan-level risks. |
| **BDD suite** | Per-task scenarios + suite-level rollup scenarios (§C). |

### §B — Task Record Specification (mandatory fields)

Every task carries **all** fields below. A missing field is a defect.

| Field | Contract |
| :--- | :--- |
| `ID` | `T-NN` (zero-padded). Stable across revisions. |
| `Title` | ≤ 8 words. Active verb. |
| `Objective` | One sentence: what changes in the world when this task completes. |
| `Antecedents` | Explicit list of task IDs that must be complete first. `—` if Wave 0. No implicit deps. |
| `Inputs` | Concrete files / decisions consumed. Full paths. |
| `Outputs` | Concrete artifacts produced. Full paths, expected formats. |
| `Technical requirements` | Prescriptive list: tools, schemas, conventions to obey. |
| `Examples` | At least one concrete worked snippet (yaml / md / shell / mermaid). |
| `Acceptance criteria` | One or more `Given / When / Then` BDD rows. |
| `Out of scope` | Explicit no's — what the task does **not** do. |
| `Granularity` | `S` (≤ ½ day), `M` (½–2 days), `L` (> 2 days). `L` triggers a decomposition note declaring resolution: **(a)** graph-level split into multiple parallel-eligible tasks at planning time, OR **(b)** internal-parallel execution as a single task (multi-phase). Per Berkeley §Solution > Workload Balancing. **Graph topology does not evolve at run time.** |

### §C — BDD Test Suite Template

Per-task scenario (mandatory, ≥ 1 per task):

```gherkin
Scenario: T-NN — <task title>
  Given <antecedents complete; inputs exist at declared paths>
  When  <the task is executed per its technical requirements>
  Then  <output exists at <path>>
  And   <output conforms to <schema / format / convention>>
  And   <output satisfies <semantic property>>
```

Suite-level rollup scenarios (mandatory, exactly these three):

```gherkin
Scenario: DAG is acyclic
  Given the task graph as declared in §Task graph
  When  a topological sort is attempted
  Then  no cycle is detected
  And   every task has at least one path from a Wave-0 task

Scenario: All exit criteria are produced
  Given the Exit criteria list
  When  each criterion is traced back through the DAG
  Then  every criterion is the Output of at least one task

Scenario: Critical path is traversable
  Given the Critical path task sequence
  When  each task on the path is executed in order
  Then  every task's Antecedents are complete before its execution
  And   the final task's Output satisfies the Goal
```

### §D — Plan Evaluation Specification

#### §D.1 — Pre-gate (Structural Conformance)

Cheap, mechanical, recipe-mirror. Run before §D.2. Any failure here is
Blocking by definition — a plan missing structure cannot be scored for
executability.

| Check | Diagnostic | Pass condition |
| :--- | :--- | :--- |
| §A sections | All 11 sections of §A present and non-empty | All present |
| §B fields | Every task carries all 11 fields of §B | No missing field |
| Wave-0 marker | `Antecedents = —` only on Wave-0 tasks; never elsewhere | Marker consistent |
| `L` decomposition | Every `L` task carries a note declaring resolution (a) or (b) | Note present |
| §C rollups | All three suite-level scenarios present verbatim | All three present |
| §C per-task | Every task has ≥ 1 `Given/When/Then` scenario | Coverage complete |
| ID format | All task IDs match `T-NN` (zero-padded), unique, no gaps | Format clean |

A failure on any row halts evaluation. Report the failing rows in §D.4 format
with severity = Blocking and skip §D.2.

#### §D.2 — Primary scoring (Agent-Executability)

Operational diagnostics against the recipe's prescriptiveness lever. Each
property below carries one or more mechanical checks. Run all properties on
every task and on the plan as a whole.

**P1. Zero implicit dependency**
For each task `T` and each path `P` in `T.Inputs`: `P` must appear in
`Outputs` of some task in `T.Antecedents`, OR be declared in
§Source-requirements / §Assumptions as a pre-existing fixture.
*Violation*: `P` is referenced but produced by no antecedent and not
declared as a fixture.

**P2. Zero ambiguity**
Scan every field value for any of: `TBD`, `tbd`, `?` (as placeholder),
`see below`, `as appropriate`, `etc.`, `> 🔲`, free prose where the schema
requires an enumerable list, paths missing extensions or directory prefix.
*Violation*: one per occurrence, located at `<task-id>.<field>`.

**P3. Zero drift (BDD ↔ Outputs coverage)**
For each task `T`: the union of `Then` clauses across `T`'s BDD scenarios
must reference every path in `T.Outputs`.
*Violation*: an output exists with no `Then`-clause binding.

**P4. Zero hidden coupling**
For each task `T` with `|Antecedents| ≥ 2`: each entry in `T.Inputs` must
unambiguously map to exactly one antecedent's `Outputs` (one-to-one path
match, or explicit annotation `# from T-NN`).
*Violation*: an input could be produced by more than one antecedent and
the producer is not declared.

**P5. Zero off-path improvisation**
For each task `T`: `T.Out of scope` is non-empty; `T.Technical requirements`
uses imperative verbs (`must`, `use`, `obey`, `produce`, `apply`) and
contains no advisory hedges (`could`, `may`, `consider`, `if appropriate`,
`as needed`).
*Violation*: empty `Out of scope`, or any advisory hedge in
`Technical requirements`.

#### §D.3 — Severity Classification

| Severity | Rule |
| :--- | :--- |
| **Blocking** | Any §D.1 failure; any P1 violation; any P3 violation |
| **Major** | Any P2 violation in `Inputs` / `Outputs` / `Antecedents` / `Acceptance criteria`; any P4 violation |
| **Minor** | Any P2 violation in `Objective` / `Title` / `Out of scope`; any P5 violation |

Rationale for the split: P1 and P3 break execution itself (the agent cannot
find inputs, or cannot verify outputs). P2-on-contract-fields and P4 force
the agent into interpretation on the execution path. P2-on-prose and P5
weaken predictability without blocking execution.

#### §D.4 — Violation Table (output format for §E.1)

Emit a single table, ordered by Severity (Blocking → Major → Minor) then by
task ID. This is the input artefact for §E.1 iter-1 / iter-2 / iter-3.

| ID | Severity | Property | Location | Diagnostic |
| :--- | :--- | :--- | :--- | :--- |
| V-01 | Blocking | P1 | T-04.Inputs | `/specs/schema.yaml` referenced; no antecedent produces it; not declared in §Assumptions |
| V-02 | Major | P2 | T-07.Outputs | `report.md` — no directory prefix |
| V-03 | Minor | P5 | T-02.Technical requirements | "may apply linting rules" — advisory hedge |

Empty table = plan passes evaluation; proceed to step 11 with the empty
table (iterations are still run to confirm stability against zero
violations).

### §E — Violations Fix

#### §E.1 — Challenge Pass

Build a fix queue containing violations from the table §D.4.

**For each violation in the queue:**, run *- silently - 3 iterations iter-1, iter-2, iter-3)* the following workflow
1. Read the violation block verbatim from table §D.4. Do not paraphrase, summarize, or restate. Reason: paraphrase drifts wording across runs; the violation table is the canonical text the user reviewed.
2. For iter-1: for each violation, Claude generates silently the verbatim fix block in order close gap against criteria, and self-challenge the fix block again the fix-intent: does it address exactly the violation, no more no less? Silently flag scope creep (extra edge cases, unrelated rules, prose expansion). 
3. For iter-2: for each violation, Claude propose silently propose a second concrete replacement that addresses the challenges from iter-1. 
4. For iter-3: for each violation, Claude propose a third concrete replacement that addresses the challenges from iter-2. For each violation, the three drafts will be analyzed in §X.
5. For each violation, analyse the three drafts as a set and assign one of three verdicts. Generate the verdict explicitly.
- **Stable** — iter-3 self-challenge passes both axes AND iter-2 and iter-3 share the same insertion location, the same structural shape, and the same set of named surfaces being added. Differences are wording polish only.
- **Drifting** — iter-3 self-challenge fails on at least one axis, but the trajectory iter-1 → iter-2 → iter-3 shows convergence (each iteration removes prior failures or stabilises at least one of: insertion location, structural shape, named surfaces).
- **Divergent** — the three structural attributes (insertion location, structural shape, set of named surfaces) do not stabilise across iter-2/iter-3, OR each iteration introduces a new variance surface its predecessor did not.

#### §E.2 — Violations Fix Table

Generate **silently** the violations fix table,
| ID | Severity | Property | Location | Diagnostic | Recommendation | verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |  

### §F — Generate Report

Generate the Violation Fix table and reporting table. 

Reporting table includes: 
- number of tasks - mentionnioning number of L, M, S, 
- number of leaves - i.e. tasks with no dependants, 
- critical path — i.e. find the longest cumulative-granularity chain, 
- bottleneck callouts — i.e. `L` task on the critical path, because it might be is a primary decomposition candidate,
- 

### §G — Construction procedure

1. **Read** the source requirements end-to-end.
2. **Task Decomposition** — silently list every concrete artifact the requirements imply must exist.
3. **Group Tasks** — collapse artifacts sharing inputs/outputs; split tasks mixing unrelated outputs.
4. **Order Tasks** — for each task, silently name its antecedents from the artifact list. Mark wave number: **0** if no antecedents; otherwise **max(wave of antecedents) + 1**. *(For Fig 3, this yields wave(m,n) = m + n.)*
5. **Granularity Pass** — silently flag any `L` task; resolve per §B Granularity option (a) or (b).
6. **Critical Path** — find the longest cumulative-granularity chain.
7.  **Generate Task Graph** - silently generate in mermaid format the task graph resulting from steps 2. to 5. from the Construction procedure.
8.  **Generate Plan** - silently generate the whole plan in mardown.
9.  **BDD Pass** — author per-task scenarios; verify the three rollups hold.
10. **Evaluate Plan** — Run the §D evaluation pass. §D.1 pre-gate runs first; any Blocking pre-gate violation halts evaluation and surfaces directly to step 11 (no step 11 iterations on a structurally broken plan). Otherwise score against §D.2, classify per §D.3, emit the violation table per §D.4 for consumption by step 11.
11. **Recommend violations fix** - Run §E.1 and then silently generate §E.2 table. Keep it in context.
12. **Create Report Artifact** - Run the §F. and write the report artifact. Output format: `<scope>/plans/YYYY-MM-DD-<topic>-report.md`.
13. **Create Plan Artifact** - Write the plan in a .md file including the task graphs generated in step 7. Output format: `<scope>/plans/YYYY-MM-DD-<topic>-implementation-plan.md`.

---

## §H — Optional execution via agent teams (opt-in)

Execution-layer concern, separate from the recipe proper. §A–§G produce the artifacts. §H describes how a skill built from this recipe *may* hand the produced plan to a Claude Code agent team for parallel execution. It is off by default.

> **Default stays single-agent.** A skill built from this recipe must not start an agent team unless the user explicitly asks for team execution. Absent that request, the plan is executed per its waves by a single agent (sequential across waves, internal-parallel within a task per §B Granularity option (b)).

The fit is structural: the recipe already produces a static DAG with per-wave parallel-eligible cohorts (§Task graph), explicit antecedents per task (§B), and a per-task BDD contract (§C). An agent team's shared task list, self-claim model, and completion gates map onto those directly.

#### §H.1 — Activation gate (preconditions)

The skill verifies all rows before proposing team execution. The env var cannot be flipped mid-session (it is read at launch), so the skill detects state and, if the user asks for a team while the feature is off, instructs the user to enable it and restart rather than attempting to set it itself.

| Precondition | Value | Where |
| :--- | :--- | :--- |
| Explicit user request | User asks for team execution in plain language | Conversation |
| Feature flag | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = "1"` | `settings.json` `env` block, or shell env (set before launch) |
| Claude Code version | `>= 2.1.32` | `claude --version` |
| Display mode | `teammateMode` one of `in-process`, `auto` (default), `tmux` | `~/.claude/settings.json` |
| Split-pane prerequisite | tmux or iTerm2 (with `it2` CLI) | Only if split panes wanted |
| Cost acknowledgement | User accepts higher token cost (each teammate carries its own context window) | Conversation |

`settings.json` form:

```json
{
  "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }
}
```

#### §H.2 — Plan-to-team mapping

| Recipe artifact (§A/§B) | Agent team construct |
| :--- | :--- |
| `Tasks[]` records | Pre-seeded shared task list, one entry per `T-NN`. No task created at run time. |
| `Antecedents` | Blocked-until predicate. A task is claimable only when every antecedent is complete (mirrors §B Antecedents). |
| Wave table cohort | The set of tasks that become claimable together. Peak concurrent claims per wave = `min(M, N) + 1` (§Tasks Graph pattern). |
| Self-claim | After finishing, a teammate pulls the next unblocked, unassigned task. File-locking prevents two teammates claiming the same `T-NN`. |
| Critical path | Tasks on the path are claimed first (lead assigns, or labels them priority). |
| Lead role | Owns the plan, assigns or lets teammates self-claim, approves plans. Authors no new tasks (the DAG is static). |
| `L` task, resolution (b) | A single team task whose teammate may run internal-parallel phases. Topology unchanged. |

#### §H.3 — Team start (plain language)

The user starts a team by describing the goal and asking for one, optionally naming teammate count and models. Example seeded from the plan's Goal and wave 0:

```text
Execute the implementation plan at <scope>/plans/<date>-<topic>-implementation-plan.md
as an agent team. Seed the shared task list from its Tasks[] section, one task per
T-NN, with antecedents as blocking dependencies. Let teammates self-claim unblocked
tasks. Spawn 3 teammates. Require plan approval before any teammate edits files.
```

#### §H.4 — Invariant enforcement with hooks

The recipe's hard invariants map onto the three agent-team hook events. Each gate exits with code `2` to block the action and return feedback to the offending teammate.

| Hook event | Recipe invariant enforced | Gate action (exit 2 = block) |
| :--- | :--- | :--- |
| `TaskCreated` | "Graph topology does not evolve at run time" (§B Granularity, §Context) | Reject any task whose ID is not pre-declared in the plan's `Tasks[]`. The static DAG is the only source of tasks. |
| `TaskCompleted` | Per-task BDD contract (§C) and declared `Outputs` (§B) | Reject completion unless the task's `Then` clauses hold: every declared `Outputs` path exists and conforms. Mirrors §C per-task scenario. |
| `TeammateIdle` | Critical-path progress, no idle capacity | Assign the next unblocked wave task (critical-path tasks first), or hold the teammate if the wave is exhausted. |

#### §H.5 — Operational controls

| Control | Mechanism | Recipe use |
| :--- | :--- | :--- |
| Display mode | `in-process` (default) all teammates in main terminal, or split panes via tmux/iTerm2 | Operator preference. No effect on the DAG. |
| Cycle teammates | `Shift+Down` in in-process mode (wraps to lead after the last) | Inspect a teammate working a given `T-NN`. |
| Direct message | Cycle to a teammate (in-process) or click its pane (split) and type | Steer one teammate without routing through the lead. |
| Plan approval | Ask the lead to require approval. Teammate stays in read-only plan mode until the lead approves or rejects with feedback | Apply to critical-path or `L` tasks where an off-path choice is costly (mirrors §D.2 P5, zero off-path improvisation). |

#### §H.6 — Limitations (surface to the user before starting)

- Experimental. Known rough edges in session resumption, task coordination, and shutdown.
- No nested teams. A teammate cannot spawn its own team. Only the lead manages the team.
- Token cost is materially higher than a single session (per-teammate context windows).
- Requires Claude Code `>= 2.1.32`. Split panes require tmux or iTerm2.

> Speculative note: these constraints are accurate as of the documented release (`agent-teams.md`, v2.1.32). Experimental behaviour can change. The skill should re-check `claude --version` and the docs at activation rather than trusting this section verbatim.

Source: https://code.claude.com/docs/en/agent-teams.md and https://code.claude.com/docs/en/hooks-guide.md

---

## Open point

O.1 - Plan construction workflow must be explicit.

O.2 - §H agent-team execution is opt-in and execution-layer. A skill built from this recipe owns the activation decision. Confirm before promotion to the skill whether team seeding (§H.3) should be a scripted step or remain plain-language.

---

## Tradeoffs

| Axis | Task Graph | Waterfall | Scrum | Kanban |
| :--- | :--- | :--- | :--- | :--- |
| Structure | DAG with parallel branches and convergence | Linear phase chain | Prioritized backlog | Pull-based swim lanes |
| Plan stability | Static — locked at planning time | Static — gated by phase sign-offs | Re-planned every sprint | Continuously evolving |
| Dependencies | Explicit; dominant; drive execution order | Implicit; phase-sequential | Downplayed in favor of priority | Minimized; tasks typically independent |
| Estimation | Deterministic granularity `{S, M, L}` | Phase-duration estimates | Velocity / story points (empirical) | Lead time, cycle time (throughput-driven) |
| Parallelism | Uncapped — every parallel-eligible cohort runs | None within a phase | Bounded by team and sprint | WIP-limited to expose bottlenecks |
| Runtime task spawning | Forbidden — graph fixed before execution | Forbidden between phases | Expected — bugs and refactors emerge mid-sprint | Continuous — backlog flows in |
| Critical path | Native; mandatory artifact | Adjunct technique (CPM / Gantt) | Not a core concept | Not a core concept |
| Underlying unknown | Work size and dependency shape | Phase duration | Requirement priority | Throughput and bottleneck location |

**Closest cousin:** Waterfall — both pre-plan everything and forbid mid-execution restructuring. Task Graph differs by admitting arbitrary DAG topology (Waterfall is linear), gating on antecedent completion (not phase sign-off), and treating critical path as a mandatory artifact (not an adjunct).

**Fundamental incompatibilities:** Scrum (plan evolves every sprint; new tasks expected at runtime) and Kanban (no fixed plan; pull-based flow over fixed DAG).

**Best fit:** work shape knowable up front; requirements stable; dependencies dominate over priority shifts; critical path matters more than throughput — framework implementation, infrastructure rollouts, regulated software, well-bounded migrations.

**Poor fit:** ongoing product development (Scrum territory), ops and maintenance flow (Kanban territory).

---

| Field | Value |
| :--- | :--- |
| Version | 1.2 |
| Last Updated | 2026-06-06 |
| Status | Draft. Adds explicit autopilot (human-in-the-loop) execution-mode boundary in Why it matters and When to trigger, on top of 1.1 §H agent-team execution. Recipe derived from backlog/2026-05-25-recipe-authoring-play.md |
