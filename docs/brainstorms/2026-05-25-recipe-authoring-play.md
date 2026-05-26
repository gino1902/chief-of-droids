# Play — Recipe Authoring from Pattern + Test Fixture

## Source — Berkeley Task Graph pattern (adapted to project planning)
> Source: *Our Pattern Language*, UC Berkeley ParLab. Pattern: **Task Graph**.
> URL: https://patterns.eecs.berkeley.edu/?page_id=609

## Hook

A plan you want be executed by agents must be a plan you trust solid. This recipe fixes the dependency design shape, , ships per-task BDD and three suite-level rollups that verify your DAG, your exit criteria, and your critical path.

## When to trigger

- A documented planning pattern (paper, standard, established practice) exists and constrains the deliverable's shape
- A concrete requirements doc exists that can serve as a test fixture for the recipe
- The user expects a *reusable* artifact, not a one-off plan
- The user tolerates strict prescriptiveness (mandatory fields, no optional structure)

**Don't trigger when:** the pattern source is too thin to constrain (then the requirements doc would have to supply structure); only one application is foreseen (recipe overhead unjustified); the user wants a plan, not a recipe; the example dominates the pattern's force (e.g. applying Task Graph to a 3-task project — overhead wins).

## Why it matters

The naive flow is example-first: read the requirements, build a plan, retrofit a "method" afterward. That produces a project-shaped recipe — fits one project, leaks for the next. The pattern-first flow inverts this: the pattern dictates section structure, mandatory fields, and verification scenarios before any example content is admitted. The example then exercises the recipe as a black box — if it survives, the recipe is reusable; if it fails, patch the recipe, never the example.

Because the plan is executed by an agent — a skill, subagent, or claude.md-scoped session running inside Claude Code — prescriptiveness is the lever for predictability. Every task's mandatory contract (fields, BDD, granularity, antecedents) leaves no interpretive gap for the agent to fill with hallucination, omission, or off-path improvisation.

---

### Problem

How to structure an implementation plan as a static collection of atomic work items with dependencies, executing efficiently — in parallel where independent work can proceed concurrently, serially where prior work must complete first — given that tasks may have variable sizes and multiple input/output dependencies, and form a directed acyclic graph (DAG)?

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

Berkeley names three sub-patterns for breakdown (from *Patterns for Parallel Programming*, Ch 3):

- **Task Decomposition** — Identify atomic tasks that can execute concurrently.
- **Group Tasks** — Group tasks to identify temporal dependencies and truly atomic tasks.
- **Order Tasks** — Identify how tasks must be ordered to satisfy constraints among tasks.

And one for assessment:

- **Design Evaluation** — Apply per candidate plan to assess fitness against (1) agent capacity and task-overhead trade-off, (2) handoffs and task granularity in light of coordination cost, and (3) simplicity vs flexibility vs efficiency. May yield multiple iterations across alternative plans.

#### Solution components (separate from forces)

- **Workload Balancing.** The plan does *not* balance load inherently. Load is determined by the critical path through the slowest tasks. Bottleneck removal is the planner's responsibility: either (a) break a slow task into multiple parallel-eligible tasks at planning time, or (b) parallelize the task internally — spin up multiple agent instances — without changing plan topology.
- **Handoffs.** Either explicit deliverable handoff antecedent→dependent (artifact passed at completion), or control-flow synchronization on a shared artifact (review/approval gates). Execution-level concern; not mapped to the recipe.
- **Risk Handling.** Each task handles its own risks/failures; the project framework aggregates as appropriate (status reporting, escalation). Execution-level concern; not mapped.

### Variations

The recipe operates in Berkeley's *per-project variation* (Berkeley's term: 'run-time-defined-graph') — plan structure pinned by the recipe, per-project content supplied at planning time. See §Context for the invariants.

### Figure 3 — wavefront example (distilled)

A 2-D wavefront calculation on a grid of variable size. Each cell `(m, n)` depends on `(m-1, n)` and `(m, n-1)`. The dependency pattern is fixed at design time; the grid size `M × N` is only known at run time.

Dependencies form anti-diagonals — within an anti-diagonal, tasks are mutually independent and parallel-eligible.

```
Wave 0:  (0,0)
Wave 1:  (1,0) (0,1)
Wave 2:  (2,0) (1,1) (0,2)
Wave 3:  (3,0) (2,1) (1,2) (0,3)
...
Wave M+N: (M,N)
```

Wave number = `m + n`. Peak parallelism = `min(M, N) + 1`, reached at wave `min(M, N)`. Critical path length = `M + N + 1` tasks.

### Mapping to plan authoring (the recipe's source elements)

> Berkeley implementation-level concerns (Hardware capacity, Sharing Data,
> Error Handling) are below the plan-authoring layer and intentionally not
> mapped — they belong to execution, not planning.

| Berkeley concept | Source section | Recipe instrument |
| :--- | :--- | :--- |
| Known dependency pattern + run-time-determined instance count | Variations + Fig 3 | Plan declares antecedents at authoring; per-project task count emerges per application |
| Variable vs Uniform task size | Forces (universal) | Mandatory `{S, M, L}` granularity tag per task |
| Task granularity vs Startup overhead (force family) | Forces (implementation) | `L` tasks flagged for resolution per Load Balancing |
| Critical path through slowest tasks | Solution > Workload Balancing | Mandatory identification (granularity-weighted) in the plan |
| Bottleneck removal (graph-split OR internal-parallel) | Solution > Workload Balancing | Per-`L`-task decomposition note specifying which option applies |
| Task Decomposition / Group / Order | Solution | Recipe §D steps 2–4, verbatim |
| Design Evaluation (evaluate-then-revise loop) | Solution | Recipe §D step 9 inspiration; criteria differ (recipe = requirement coverage, not hardware fit); ≥ 2 count is workspace-empirical |
| Wavefront cohorts (Fig 3 anti-diagonals) | Variations + Fig 3 | Mandatory wave annotation as a separate plan section ("wave" = convention) |

---

## The recipe

> Self-contained specification — apply this to any requirements doc to produce
> an implementation plan + task graph + BDD suite. Identical to Part 1 of the
> first applied plan.

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

### §D — Construction procedure

1. **Read** the source requirements end-to-end.
2. **Task Decomposition** *(Berkeley)* — list every concrete artifact the requirements imply must exist.
3. **Group Tasks** *(Berkeley)* — collapse artifacts sharing inputs/outputs; split tasks mixing unrelated outputs.
4. **Order Tasks** *(Berkeley)* — for each task, name its antecedents from the artifact list. Mark wave number: **0** if no antecedents; otherwise **max(wave of antecedents) + 1**. *(For Fig 3, this yields wave(m,n) = m + n.)*
5. **Granularity pass** — flag any `L` task; resolve per §B Granularity option (a) or (b).
6. **Critical path** — find the longest cumulative-granularity chain.
7. **Bottleneck callouts** — any `L` task on the critical path is a primary decomposition candidate (Berkeley §Solution > Workload Balancing).
8. **BDD pass** — author per-task scenarios; verify the three rollups hold.
9. **Challenge pass** *(silent, ≥ 2 iterations)* — borrows the evaluate-then-revise loop from Berkeley *Design Evaluation*; the criteria differ (Berkeley = hardware fit; recipe = requirement coverage + risk consumption). The ≥ 2 count is workspace-empirical. Re-read against requirements; verify every requirement decision and residual risk is consumed by a task or explicitly out-of-scope.

---

## Outcomes

| Artifact | Count |
| :--- | :--- |
| Recipe — mandatory plan sections | 11 |
| Recipe — mandatory task-record fields | 11 |
| Recipe — per-task BDD template | 1 |
| Recipe — mandatory suite-level rollup scenarios | 3 (exactly) |
| Recipe — construction procedure steps | 9 (incl. ≥ 2 silent challenge passes at step 9) |
| Applied plan — fully prescribed tasks | 21 |
| Applied plan — waves | 12 |
| Applied plan — critical path tasks | 11 |
| Applied plan — bottleneck callouts | 2 |
| Applied plan — carried risks (with `where addressed` mapping) | 5 |
| Applied plan — new plan-level risks | 4 |
| Silent challenge passes executed | 2 |
| Plan structural adjustments produced by challenges | 7 (Pass 1: 4 · Pass 2: 3) |
| Source-audit passes against Berkeley | 4 (v1.2 + v1.3 + v1.4 + v1.5); 27 issues caught & fixed (10 · 8 · 5 · 4). **Lock condition met at v1.5: substantive drift = 0.** |

Output format: `<scope>/plans/YYYY-MM-DD-<topic>-implementation-plan.md` (single doc — recipe + applied plan, atomic at N=1).
Pairs with: `docs/conventions/play-format.md` (structural spec for plays) · `wiki-data/plans/2026-05-25-wiki-framework-implementation-plan.md` (first applied plan — the example fixture).

## How we conducted the play

### Conversation friction observed

| Pattern | Where | What it produced |
| :--- | :--- | :--- |
| User redirected after first deliverable | Between recipe doc write and play request | Repositioned the play scope — recipe-authoring as subject, wiki framework as example. Saved authoring a wiki-shaped retrospective. |
| Procedure prompt mixed visible and silent steps | First prompt | Required disambiguating deliverables (recipe spec, BDD template, final md plan) from internal moves (silent challenges, adjustments). |
| Ambiguous deliverable target ("generate md plan" — chat or file?) | End of recipe authoring | Resolved by producing inline + proposing path; user confirmed; same pattern reused twice more for the meta-spec and this play. |
| Silent passes invisible in output | Recipe §D step 9 | Created risk that the iteration loop looks like one-shot generation. Mitigated by encoding iteration as a *recipe requirement*, not a session ritual. |
| User pushed self-containment requirement | After draft play proposed | Forced embedding of Berkeley pattern summary + recipe inline. Increased play length ~70 %; eliminated external dependency for the pattern. |
| User ran first source-audit pass | After embed-and-write proposal | Caught 10 issues (misattribution of load balancing as a "force", "waves" as Berkeley vocabulary, run-time decomposition contradiction, others). Hardened Berkeley fidelity. |
| User ran second source-audit pass + asked for drift measurement | After v1.2 proposal | Caught 8 residual issues (wave formula bug, Design Evaluation framing, mapping table imprecision, others). Drift measurement showed structural convergence at v1.2; v1.3 fixes are content-level. |
| User ran third source-audit pass with formalized drift dimensions | After v1.3 proposal | Caught 5 issues (1 substantive: arithmetic count error; 4 precision: missed Berkeley qualifiers, hard-coded version range). Trend confirmed dimensional convergence; substantive drift persistent at 1/pass. |
| User ran fourth source-audit pass | After v1.4 proposal | Caught 4 issues (0 substantive; 4 precision: implementation-force wording, Design Evaluation criteria grouping, Variations phrasing, Fig 3 caveat softening). **Substantive drift = 0 ⇒ lock condition met.** |
| Tool routing forks | Each input read | Negligible — bootstrap rules picked `fetch` for the URL, native image visibility for Figure 3, `filesystem:read_text_file` for the requirements doc. |

### Gaps between begin and end

| Begin state | End state |
| :--- | :--- |
| Berkeley URL + Fig 3 image + wiki requirements v1.4 | Reusable recipe with mandatory section + field contracts |
| No task-graph format convention in the workspace | Wave-annotated Mermaid DAG with explicit critical path + bottleneck callouts |
| BDD template implicit in workspace style | Explicit Given/When/Then template + 3 mandatory suite-level rollups |
| Wiki requirements Resume hint listing 4 next steps | 21-task plan covering steps 1–3; step 4 parked deliberately |
| Risks tracked in requirements only (R.1–R.10) | Risks carried into plan with `where addressed` column + 4 new plan-level risks (P.1–P.4) |
| No artifact for play structure | Play meta-spec at `docs/conventions/play-format.md` (this play's enabling precondition) |
| Recipe + pattern reachable only via external URL + plan doc | Self-supporting play, audited across 4 passes against Berkeley until substantive drift = 0 ⇒ locked |

### Best practices used to close gaps

1. **Read the pattern paper before the example.** Berkeley fetched first; wiki requirements second. The recipe's section vocabulary (critical path, granularity, load balancing, bottleneck removal) came from the pattern, not the example.
2. **Map the article's signature figure to the recipe's central concept.** Figure 3 wavefront = known dependency pattern + run-time-determined instance count. Translated into: recipe shape pinned at authoring; per-project task count emerges per application.
3. **Mandatory-field task record with zero optional fields.** A missing field is a defect, not a stylistic choice. Forces the recipe to be falsifiable.
4. **Exactly three suite-level BDD rollups.** DAG acyclic + Exit criteria reachable + Critical path traversable. Verify structural properties that per-task BDDs cannot catch.
5. **Silent challenge passes encoded as a recipe step.** Recipe §D step 9 mandates ≥ 2 challenge iterations. The procedure survives the session.
6. **Two iteration passes adjusted the applied plan and graph, not the recipe.** *Findings below are reconstructed from the plan's final shape — the passes themselves were silent.* Pass 1 (4 adjustments): monolithic Wave 2 broken up, parallel-eligibility of wiki-audit and overview surfaced, dust-grained HOW-TO-TRIGGER tasks consolidated, user-prereq on dry-run ingest declared. Pass 2 (3 adjustments): critical-path identification added, per-task example coverage enforced, T-06 split into skeleton + finalize to expose the parallel Wave 6.
7. **Wave annotation as a separate section.** Edges encode dependency; waves encode parallelism. Separating them made critical path identification trivial.
8. **Granularity tag {S, M, L} from Berkeley's granularity force family.** Berkeley names four granularity-related forces (Variable vs Uniform, Large vs Small, Task granularity vs Startup & Comm, Task granularity vs Startup Latency); the recipe collapses them into one tag because plan-authoring doesn't need PE-level distinctions. Cheap signal, expensive omission.
9. **Carry risks from upstream with a "where addressed" column.** Every upstream R.x must map to a plan task or be re-declared as residual. Traceability.
10. **Path proposal + explicit user confirmation before directory creation.** Workspace rule honored. Saved a regenerate cycle for the wrong path.
11. **Embed → audit → re-audit → measure drift → lock when substantive drift hits zero.** Self-supporting embedding is necessary but not sufficient; each embed needs a source-audit pass to catch misattribution before it ossifies; drift between revisions across (structural, substantive, precision, length) dimensions is the stability signal; *lock when one full pass yields zero substantive issues*. Precision drift below the lock threshold is asymptotic noise and out-of-band.
12. **Prescribe for predictability when execution is agentic.** The recipe's mandatory fields, BDD, and granularity tags exist not for aesthetic discipline but because agent execution drifts without a prescriptive contract. Every field that's not mandatory becomes an interpretive gap; every interpretive gap is a hallucination opportunity. Lock the contract; let the agent fill the content.

---

## Tradeoffs — the categorization

Six categories. Each names what the recipe author chose between when constructing the deliverable.

### T1. Prescriptiveness vs Adaptability

How strict the recipe pins each structural element.

| Decision | Strict pole | Adaptive pole | Choice (locked) |
| :--- | :--- | :--- | :--- |
| Task-record fields | 11 mandatory, no optional | Mandatory core + optional extras | All 11 mandatory |
| Per-task BDD | ≥ 1 mandatory | Sample BDDs, author's choice | Mandatory ≥ 1 |
| Granularity | Enum {S, M, L} | Free text | Enum |
| Wave annotation | Mandatory separate section | Implicit from edges | Mandatory |
| Out-of-scope per task | Mandatory field | Implicit by absence | Mandatory |
| Suite-level rollups | Exactly three named scenarios | "At least one" | Exactly three |

**Meta-observation:** prescriptive on shape, flexible on content — and the split is governed by *agent execution*. Shape leaves no interpretive room (predictability); content is per-project so the agent earns its keep there. Shape is the architect's lever for determinism; content is where agent autonomy is welcome.

### T2. Compile-time vs Run-time decomposition

Berkeley's central tension applied to the recipe itself.

| Decision | Compile-time pole | Run-time pole | Choice (locked) |
| :--- | :--- | :--- | :--- |
| Graph topology | Pinned at planning | Discovered during execution | Pinned at planning (Berkeley invariant) |
| Wave assignment | At planning | Deferred to scheduler | At planning |
| Granularity | Estimated at planning | Measured post-hoc | At planning |
| Bottleneck callouts | At planning | Surfaced during execution | At planning |
| `L`-task resolution | Graph-split at planning | Internal-parallel execution (single task, multi-phase) | Either — declared at planning per §B Granularity. *Graph never evolves at runtime, per Berkeley.* |

**Meta-observation:** planning-time bias matches Berkeley's invariant ("the task graph does not evolve during execution"). The two `L`-task resolution options (graph-split OR internal-parallel) are both declared at planning time; neither defers graph evolution to runtime. Wavefront-style: pattern is known at planning, instance count is data-driven at apply time. The recipe encodes the same posture it preaches.

### T3. Pattern-source vs Empirical-source

Where the recipe's structure was lifted from.

| Element | Pattern-source pole | Empirical-source pole | Choice (locked) |
| :--- | :--- | :--- | :--- |
| Critical path, granularity, load balancing, bottleneck removal | Berkeley | Workspace conventions | Berkeley |
| Task Decomposition / Group / Order | Berkeley (§Solution) | — | Berkeley, verbatim |
| Design Evaluation (inspiration for §D step 9) | Berkeley | — | Berkeley (loop structure only — criteria differ) |
| Challenge-pass iteration count (≥ 2) | — | Workspace habit | Empirical |
| Wave annotation (anti-diagonal cohort labelling) | — (Berkeley says "wavefront" but does not name cohorts) | Parallel-programming convention | Convention |
| BDD template (Given/When/Then) | — | Workspace style | Empirical |
| Version blocks, "Out of scope" field, Markdown tone | — | Workspace CLAUDE.md | Empirical |

**Meta-observation:** structural skeleton from Berkeley; field-level prescriptiveness and iteration discipline from empirical workspace conventions; "wave" labelling from parallel-programming convention. Three sources, layered. Berkeley provides the *forces and solution components*; the workspace provides the *contract format*; convention provides the *visual cohort vocabulary*. Misattributing any of the three weakens recipe authority — four successive source-audit passes (v1.2 through v1.5) caught and fixed misattributions; lock achieved at v1.5 when substantive drift hit zero.

### T4. Coverage vs Conciseness

How much per-task detail to require.

| Decision | Coverage pole | Conciseness pole | Choice (locked) |
| :--- | :--- | :--- | :--- |
| Task fields | 11 mandatory | Minimal 4–5 | 11 |
| BDD per task | ≥ 1 mandatory | Suite-only | Per-task ≥ 1 |
| Examples per task | ≥ 1 mandatory | Optional | Mandatory |
| Output structure | Single doc (recipe + applied) | Split into two docs | Single doc |
| Wave structure | Both edge list AND wave table | One or the other | Both |

**Meta-observation:** coverage wins where the field is *structural* (missing data costs verification); conciseness wins where the choice is *organizational* (a redundant doc costs reading). Different axes, opposite signs.

### T5. Silent challenge vs Visible challenge

How the iteration loop appears in the output.

| Decision | Silent pole | Visible pole | Choice (locked) |
| :--- | :--- | :--- | :--- |
| Challenge trace | Hidden from output | Inline in plan | Hidden (per prompt) |
| Adjustments | Invisible | Diff log appended | Invisible in the plan; reconstructed in the play (BP6) |
| Procedure requirement | Spoken in chat only | Encoded in recipe | Encoded (§D step 9) |
| Drift measurement | Implicit | Quantified across revisions | Quantified across revisions per the drift table |

**Meta-observation:** procedure-level visibility, output-level silence, play-level reconstruction, *meta-level drift quantification*. The recipe requires ≥ 2 challenge passes; the plan does not show them; the play reconstructs them as a numbered list; the play's revision history quantifies stabilization. Discipline survives without trace overhead; retrospective insight survives without bloating the deliverable; the drift trend tells us when the recipe is locked.

### T6. Atomic deliverable vs Layered deliverables

Where the recipe (and pattern) live across artifacts.

| Decision | Atomic pole | Layered pole | Choice (locked) |
| :--- | :--- | :--- | :--- |
| Recipe in the plan doc | Part 1 inline | Linked from a convention | Atomic (the session) |
| Recipe in the play | Embedded as §The recipe | Linked to the plan doc | Atomic |
| Berkeley pattern in the play | Distilled inline | Linked to URL | Atomic |
| Play meta-spec | Inline with the play | Separate convention doc | Layered (`docs/conventions/play-format.md`) |
| Future plans | Reference an extracted recipe | Re-inline | Layered — once recipe is validated (N ≥ 3) |

**Meta-observation:** atomic where the artifact must survive external decay (URLs change, file paths drift) — Berkeley summary + recipe live inside the play. Layered where the artifact is internal infrastructure with high churn — the play meta-spec lives in `docs/conventions/`. The choice is governed by *fragility of the external link*, not by aesthetic preference for short docs. Drift risk between embedded and original: real, mitigated by source-audit passes (BP11). Each audit is cheaper than the next migration of the original.

---

## Meta-meta-observation

Across all six categories, one consistent posture:

> **Pin the structure before reading the example. The example tests the recipe; it doesn't define it.**

Pin: section vocabulary from Berkeley (critical path, granularity, load balancing, bottleneck removal), mandatory-field task records, exactly-three rollup scenarios, planning-time graph topology, wave annotation by convention, embedded pattern summary, audited iteratively against source until substantive drift hits zero. Loosen: per-field content, task granularity values, project domain, where the recipe ultimately lives once validated.

Works because the pattern paper carried enough force to constrain the recipe before any example was admitted. Would not survive a pattern source too thin to define section vocabulary — at which point **T3 (Pattern-source vs Empirical-source)** collapses into pure empirical authoring, and the recipe becomes example-shaped rather than pattern-shaped. The signature move is gone.

Also breaks if the example is too small for the pattern's overhead. Berkeley's own warning: *"The problem must be large enough to justify the overhead of creating the graph."* Single-task projects do not warrant a Task Graph recipe.

---

| Field | Value |
| :--- | :--- |
| Version | 1.8 |
| Last Updated | 2026-05-25 |
| Status | **Locked** for Berkeley conceptual fidelity (forces, solution components, invariants). v1.6 added agent-execution rationale; v1.7 adapted §Source vocabulary to project planning + corrected agent characterization; v1.8 is a clarity pass on residual jargon (planning-pattern phrasing, per-project variation framing, project-shaped recipe, self-distribute workload; drops Fig 3 terminology caveat). Surface vocabulary planning-native; Berkeley structure preserved. |
| Pairs with | `wiki-data/plans/2026-05-25-wiki-framework-implementation-plan.md` (first applied plan, the example fixture) · `docs/conventions/play-format.md` (structural spec for plays) |
