# O2 use-case format

This format formalises a candidate O2 use case so every stakeholder agrees on what is proposed, and carries exactly the inputs the scoring model needs. It is the use-case eligibility framework named in [FRAMING.md](FRAMING.md) (ROI, location). The scoring model (weights, combination formula) is a separate artefact so weights can evolve without changing this format.

## Scope

In scope. The initiative use-case brief: identity, problem, objective, light solution sketch, users, the four eligibility gates, and the scored dimensions with their drivers.

Out of scope. The full behavioural specification and the acceptance criteria, owned by the post-go refinement step. The data-requirements note, produced after go per the existing play. The scoring weights and formula, owned by the scoring model.

## Actors

- Proposers: business teams, corporate functions and service lines. They author the brief.
- Solution consumers: the same business teams. The proposer is the adopter, which is the Invite over Impose pattern working by construction.
- Decision: the proposing business team rules its own use case in or out on the normal path. ExCom arbitrates when use cases are contested, compete for capacity, or span owners. Arbitration requires briefs to be comparable, which is why the driver set is fixed.

## Rules

1. Fixed set. One driver list, the same for every use case. The proposing team rates all of them. Nobody picks which to rate.
2. Declared N/A. A driver that truly does not apply is marked not applicable with a one-line reason, visible in the brief. Silent omission is forbidden. Example: the Adoption dimension on a fully automated pipeline with no human user.
3. Prune on frequent N/A. A driver that keeps being marked N/A across briefs is wrong, not the use cases. It is dropped or folded at the next framework revision.

## Gates

A gate is a binary precondition answering one question: can this initiative move to implementation. All four must pass. Gates are re-evaluated over time, capacity especially, so a use case can become eligible later. Gates decide eligibility. The score decides priority.

| Gate | Ruling test |
|---|---|
| Data policies | Internal data governance and RGPD compliance clear. Route to the DPO or legal for the ruling, the brief records that the check was made |
| Security | Security requirements clear |
| Architecture principles | The use case does not contradict an established ADR. Building on every ADR is not required, the runway is always in progress. Contradiction is what forces rework |
| Capacity | The team's WIP limit is not reached and a lead is available to conduct the implementation |

A check that has not run yet rules as fail, recorded as pending. The gate stays binary and the use case becomes eligible when the check passes.

## Dimensions and drivers

Four dimensions: Impact, Adoption, Effort, Confidence. Reach folded into Impact as volume. The score reads as net expected adopted value: incremental value on the metric, times adoption likelihood, gated by effort and confidence. Weights live in the scoring model.

### Impact, measured

Impact is computed, not judged: (target minus baseline) times volume. A brief that cannot name its metric, baseline and target is not scorable.

| Driver | What it holds |
|---|---|
| Success metric | The one or two most important measurable quantities from the FRAMING outcome family: cost out, freed time, cycle time, revenue, margin. No more than two, comparability across briefs depends on it |
| Baseline | Current value on the metric, measured against the best existing alternative. If an incumbent already delivers the outcome, the baseline is what it delivers. This is where the counterfactual lives |
| Target | Expected value after implementation |
| Volume | Adopting population counted in users (people, not teams) times run frequency per period |

### Adoption, judged 1 to 5

Rated only where humans are in the loop, otherwise the dimension is N/A with reason. All scales run the same direction, 5 favours adoption.

| Driver | What it rates |
|---|---|
| Desire to switch | The users' pull toward the new solution: do they want it enough to leave the incumbent. Perception, not the measured delta, which lives in Impact. User trust in the output data belongs in this justification |
| Ease of use | Effort to learn and operate, for the target users |
| Workflow fit | Fits the team's existing practice or demands a new operating model. The Invite over Impose test. Planned training and support are claimed in this justification |
| Trialability | Can be piloted on a limited scope before commitment |
| Ease of switching | The real cost of moving: what the team must abandon or migrate (habits, invested spreadsheets, incumbent mastery). 5 means the move is cheap |

### Effort, sized

Estimates (T-shirt or person-weeks), converted by the scoring model. Reuse of existing silver or gold is recorded as justification of the Build estimate, not scored separately.

| Driver | What it holds |
|---|---|
| Build | One-off work to first release: gold model, agent, integration |
| Feed onboarding | Work to land data that does not land today: new canonical contracts with producers, named per feed. Cross-org negotiation work with its own lead time |
| Run | Recurring cost after go-live: maintenance, monitoring, compute |
| Time to first value | Expected duration from start to first usable increment |

### Confidence, judged 1 to 5

Resolves feasibility, risk and sponsorship. 5 favours confidence.

| Component | Driver | What it rates |
|---|---|---|
| Feasibility | Data availability | Is the data there: feed lands, onboardable or derivable, historical depth sufficient for the method (training, trending, period-on-period), coverage across entities |
| Feasibility | Technical feasibility | Fits known platform patterns or needs invention. Includes having the skills to build it |
| Risk | Delivery risk | Dependencies, contract negotiations, unknowns. An ill-defined objective is delivery risk |
| Risk | Data quality | Is the content trustworthy and fit: accuracy, completeness, consistency, grain and cadence fit, lineage where audit demands it |
| Sponsorship | Sponsorship | Strength of business backing: named owner engaged, executive support secured |

## Overlap register

Each fact is scored once. The rulings:

| Fact | Home | Not in |
|---|---|---|
| Delta over the incumbent | Impact baseline | Adoption, which rates wanting it, not its size |
| User-side cost of moving | Adoption, ease of switching | Effort, which carries platform work only |
| Political backing | Confidence, sponsorship | Adoption |
| A missing feed | Effort carries the work, Confidence availability carries the doubt | Gates |
| Skilled resources | Confidence, technical feasibility | Effort |
| Compliance, RGPD, security, ADR | Gates | Confidence risk |
| Data trustworthiness | Objective fact in Confidence quality, user perception in Adoption justification | — |
| Staffing | Capacity gate, binary | Sponsorship driver, graded |
| Reuse | Build justification | Own driver |
| Volume | Impact | Own dimension |

## Blank template

```markdown
# Use-case brief: <title>

## Identity
| Field | Entry |
|---|---|
| Title | <active phrase naming the outcome, not the tool> |
| Placement | <mega-process / sub-processes from process-taxonomy.yaml. May span
several sub-processes when the solution sketch and the rest of the fill cover
them consistently> |
| Proposer | <business team> |
| Lead | <named person available to conduct the implementation> |
| Sponsor | <named executive owner, empty if none> |

## Problem
<2 to 3 sentences. The pain today, who is affected, how often, what it costs.
Name the incumbent: how is this need met today, by which tool or manual process.>

## Objective
<1 to 2 sentences. The outcome sought, phrased on the success metric.>

## Solution sketch
<3 to 4 lines maximum. Main path only: what is ingested, what is built, what
the agent exposes, to whom. Replaced by the full specification after go.>

## Users and beneficiaries
<Who uses the output, who owns the benefit. If no human is in the loop, say
so, it triggers the Adoption N/A rule.>

## Gates
| Gate | Ruling | Evidence |
|---|---|---|
| Data policies (incl. RGPD) | pass / fail | <DPO or governance check, logged.
Not yet run = fail, pending> |
| Security | pass / fail | <security check. Not yet run = fail, pending> |
| Architecture principles | pass / fail | <contradicts no established ADR> |
| Capacity | pass / fail | <WIP headroom, lead available> |

## Impact
| Driver | Entry |
|---|---|
| Success metric | <the 1 or 2 most important measurable quantities, no more> |
| Baseline | <current value, against the best existing alternative> |
| Target | <expected value after implementation> |
| Volume | <adopting users (people, not teams) x run frequency per period> |

## Adoption (1 to 5, one justification line each)
| Driver | Score | Justification |
|---|---|---|
| Desire to switch | | |
| Ease of use | | |
| Workflow fit | | |
| Trialability | | |
| Ease of switching | | |

## Effort
| Driver | Entry |
|---|---|
| Build | <size, note reuse of existing silver/gold here> |
| Feed onboarding | <named missing feeds and contract work> |
| Run | <recurring cost and cadence> |
| Time to first value | <duration to first usable increment> |

## Confidence (1 to 5, one justification line each)
| Driver | Score | Justification |
|---|---|---|
| Data availability | | <lands / onboardable / derivable, history, coverage> |
| Technical feasibility | | |
| Delivery risk | | |
| Data quality | | <accuracy, completeness, consistency, grain, cadence, lineage> |
| Sponsorship | | |

## N/A declarations
<Every driver marked N/A, one line of reason each. Empty means all rated.>
```

## Validation cases

The format was tested against two reference cases. EPM actual vs forecast passes all gates and scores on real headroom, with its missing Group B feed carried as feed-onboarding work and availability doubt. The PnL-report-in-EPM case fails twice, at the capacity gate and at Impact near zero, because its baseline equals what EPM already delivers. A format that cannot kill that case would not be doing its job.

<!--
Version: 1.1 | Last Updated: 2026-08-03 | Status: Draft
-->
