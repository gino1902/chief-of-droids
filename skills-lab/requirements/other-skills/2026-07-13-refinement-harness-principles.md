---
date: 2026-07-13
topic: refinement-harness-principles
---

# Refinement harness principles

## Problem frame
Upstream refinement (epic → feature → backlog → delivery-ready) is where business knowledge is turned into buildable work. The harness is not a new build and not a monolith: it is a methodology contract layer that existing skills-lab skills — bootstrap, brainstorm, write-requirements (names unverified against disk) — evolve to consume, plus (at orchestrator maturity) a thin orchestrator over them. This document holds the principles. Skill-level requirements are derived later, per skill, as the gap between what the skill does and what a principle demands.

Each principle carries a stage-applicability tag: [advisor], [orchestrator], [all] (both stages), or [ladder] (governs the advisor → orchestrator evolution itself). "Principles for the advisor stage" = [advisor] + [all].

## Principles

**Gate semantics**
- P1. [all] DoR/DoD exist only to evaluate readiness to move from one stage to the next. They are guidance, never hard blocks. Humans own flow decisions; the harness (at orchestrator maturity) owns flow mechanics (P12).
- P2. [all] Transition assessments carry rationale per criterion, not bare verdicts.
- P3. [all] Minimal gate set: each transition answers one question, and its criteria are the minimum evidence for that answer. Organisation-specific additions live in contract instances (P9), never in the principle set.
- P10. [all] Each stage owns one artefact template embodying the DoR/DoD essence of that stage.
- P13. [all] No producer assesses its own artefact against the contract. At advisor maturity, assessment is performed by a party other than the producing skill or session. At orchestrator maturity, it runs harness-side.

**Ownership**
- P4. [all] Every gate criterion is configured human-gate (agent proposes only) or agent-gate (agent may close). Configuration is data, not code, so ownership evolves with trust.

**Methodology**
- P5. [all] SAFe essence only: constrain deliverables, never the path. No ART, PI cadence, or ceremony modelling.
- P6. [all] Less is more: no ceremony a user must perform to get value. Methodology helps but never wins over execution and business knowledge.

**Evolution**
- P7. [ladder] Advisor maturity before orchestrator maturity (defined below). Ship advisory value first; orchestration later.
- P8. [ladder] The advisor and orchestrator stages remain distinct grounds. The orchestrator builds on advisor components unchanged; any deviation from an advisor component is an explicit transition decision recorded against both grounds, never accretion. Transitions run both ways: a component is removed by the same explicit decision mechanism when model capability makes it redundant.
- P9. [all] The methodology contract lives once, in a shared versioned reference consumed by every target skill. It is never copied into a skill body.
- P11. [all] Skills and harness are interfaced, never coupled. The DoR/DoD set is a methodology contract: versioned data a skill consumes when present. Decoupling test: (a) every skill runs with zero harness present; (b) the contract changes without editing any skill body. Both must hold.
- P12. [orchestrator] The harness owns flow mechanics as a workflow: artefact progression, stage state, and skill activation through defined paths. Control is unidirectional — the harness activates skills; skills return results via self-describing artefacts but never drive the flow. User command is the primary trigger; DoR/DoD are checks the harness runs at step boundaries. Humans own flow decisions (P1).

## Maturity ladder

| Stage | Meaning |
| :--- | :--- |
| Advisor | Each skill consumes the contract (P9, P11) and offers stage templates and advisory transition assessments (P1–P4, P10, P13) on any artefact handed to it. Skills remain standalone, no flow coupling |
| Orchestrator | A harness-side thin orchestrator owns flow mechanics and runs transition assessments (P12, P13); stage state lives in self-describing artefacts, the progression record harness-side; advisor-stage evaluator and gate config are reused unchanged (P8) |

## Conversion mechanism
Per target skill: gap analysis = principles × current skill behaviour → skill-level requirements, including a conformance dimension against the methodology contract (P11 test). Gap analyses toward the advisor stage use the [advisor] + [all] principle set. Each analysis produces one requirements document scoped to that skill's evolution toward advisor maturity (then, later, toward orchestrator maturity). Requires reading the skills — declared next work package, not part of this document.

## Scope boundaries
- Upstream only (epic → delivery-ready). Build/sprint and review-feedback ingestion are out of scope for now.
- The harness is a contract layer plus, at orchestrator maturity, a thin orchestrator. Never a monolith absorbing skills.
- No delivery-side tooling (sprint boards, burndown, estimation math).

## Key decisions
- P3 resolved: three transition questions — worth shaping? (epic → feature), buildable? (feature → backlog), pickable by a team? (backlog → delivery-ready) — carrying eight criteria in total. The criteria live in the contract artefact per P9, not in this document. Derived from the transition questions; the originating flowchart was brainstorm input, not an anchor.
- Maturity stages renamed advisor / orchestrator for self-explanatory reading (formerly C / B in session history, from the approach menu of the originating brainstorm).
- Interfaced, not coupled: skills standalone, DoR/DoD as methodology contract (P11). Resolves P9 in a stronger form — the shared reference is the interface artefact itself.
- Harness owns flow mechanics, humans own flow decisions (P12). User wording challenged against Anthropic's workflow pattern and revised to the control/data split: harness activates, skills return results.
- Production and evaluation separated (P13), applicable at both maturities: cross-party assessment at advisor stage, harness-side at orchestrator stage. Claude-proposed from Anthropic harness engineering (self-evaluation unreliability); not a user statement.
- Stage-applicability tags on every principle, so stage projections ("principles for the advisor stage") are reads, not interpretations. Claude-proposed after a fidelity test.
- Bidirectional component transitions in P8 (removal as capability grows). Claude-proposed from Anthropic harness engineering.
- Framework fit resolved: evolve existing skills-lab skills to consume the contract, no standalone monolith.
- Gates are guidance, not hard gates. The earlier "enforce" answer is superseded by "guidance, not hard gate" — recorded here as an explicit resolution.
- Advisor → orchestrator as maturity stages, not deliverables. Orchestration lives harness-side because orchestration inside standalone skills would violate P11.

## Dependencies / Assumptions
- [Assumption] Target skill names (bootstrap, brainstorm, write-requirements) match what exists in skills-lab. Unverified — confirm at gap-analysis time.
- [Assumption] Advisor-stage evolution is store-agnostic: skills evaluate artefacts handed to them. The store decision could still shape template formats. Revisit when resolved.

## Sources
1. anthropic.com/engineering/building-effective-agents (fetched 2026-07-13) — workflow vs agent distinction, gates as step checks, simplicity principle.
2. anthropic.com/engineering/harness-design-long-running-apps (fetched 2026-07-13) — evaluation separation, contract negotiation precedent, component-assumption expiry, file-mediated handoff.

## Outstanding questions

### Resolve before gap analysis
_(none — P3 resolved, see key decisions)_

### Deferred to gap analysis or later
- [Affects orchestrator maturity][User decision] Artefact store: markdown repo vs Jira/ADO. Blocks orchestrator-stage design only.
- [Affects P12][Technical] Stage-state representation — default: self-describing artefact frontmatter, progression record harness-side.
- [Affects P2][Technical] Assessment output format (per-criterion verdict table vs prose).
- [Affects P4, P9][Technical] Contract schema and shared-reference location; carries the eight resolved criteria with their default gate ownership.
- [Affects P9][Design] Contract shape: static per stage, or negotiated per work item (sprint-contract precedent, source 2).
- [Affects P11][Technical] Conformance checking cadence — default: at gap analysis and via qualify-pass governing-contract anchor, no runtime machinery.
- [Affects P13][Design] Cross-party assessment at advisor stage: which party (sibling skill, fresh session, qualify pass) — decide at gap analysis.

## Next steps
Run the per-skill gap analysis (conversion mechanism above). Starting skill to be decided at gap-analysis kickoff. First build step: author the contract artefact (P9) carrying the eight criteria.

<!--
Version: 2.7 | Last Updated: 2026-07-13 | Status: Draft
-->
