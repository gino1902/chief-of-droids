# Deciding architecture: session capture

> Raw material for a future architecture-decision skill, captured from the 2026-06-24 ADLS-to-bronze lock-in session.
> This is a capture document, not a skill. It records the goal, the workflow applied, and the guidance that governed it.

## Goal

Take an architecture decision from a drafted or partially-locked state to a verified, rationalised, governed artefact. The skill governs the decision lifecycle and the quality gates around it. It does not author domain substance, that stays with the domain skill. It composes the verification and expression skills rather than duplicating them.

## Workflow

Seven phases. Phases 1 to 6 are the decision-and-write loop. Phase 7 generates the formal views from the locked artefact and runs last.

| # | Phase | What it does |
| :--- | :--- | :--- |
| 1 | Frame the decision | Score the candidate against weighted selection criteria, state the verdict and the fallbacks |
| 2 | Check against intended flow | Compare the artefact to the target flow, surface gaps and inconsistencies before editing anything |
| 3 | Verify claims | Verify every version-sensitive claim against official documentation, fetched in full, retract wrong claims openly, flag what is unverified |
| 4 | Express | Map the substance onto a fixed artefact template, render in house style |
| 5 | Rationalise | Consolidate to one canonical home per fact, demote echoes to pointers, leave the flow spine untouched |
| 6 | Govern the write | Propose, confirm, write full file, verify after write, then the commit gate (stage, show staged diff, approve, commit, push manual) |
| 7 | Generate C4 views | Render the locked artefact as layered C4 views, see the dependency flag below |

### Phase 7 detail

C4 views are generated from the already-locked, already-rationalised artefact, because the component inventory and the flow edges are the exact inputs a C4 generator needs. The mapping:

| Artefact part | C4 element |
| :--- | :--- |
| System in its environment (source, subscription, platform, governance) | Context view |
| Component inventory rows | Container view, one container per row |
| Diagram and design-step edges | Relationships between containers |
| Implementation notes on internal structure | Component view, only where a container earns decomposing |

The single hand-authored Mermaid flowchart used this session is a precursor that mixes these levels in one picture. Phase 7 formalises it into the standard layered views.

> ⚠️ Dependency not yet available. This phase depends on a future enhancement to the editing-docs skill that adds C4 generation (a `references/c4.md` covering the C4 levels, the rendering choice such as Mermaid C4 syntax versus Structurizr DSL, and the theme mapping). editing-docs at v4.2 has `references/mermaid.md` but no C4 reference. Until the enhancement ships, phase 7 falls back to the hand-authored Mermaid flowchart. The rendering-tool choice and any Mermaid C4 version constraints are unverified and must be checked against current docs when that reference is authored, not assumed now.

## Guidance

### The contract

Cross-cutting rules the loop always obeys, observed across this session.

| Rule | Meaning |
| :--- | :--- |
| Gate before write | Propose changes, await explicit confirmation, then write. Commit is a separate gate |
| Verify before finalise | No version-sensitive claim is locked until fetched from an official source. Carry an explicit unverified flag otherwise |
| Challenge before execute | Surface structural gaps and ambiguities before acting on an underspecified instruction |
| Source discipline | Cite only what was fetched in full, flag the unverified, retract a wrong claim openly when verification overturns it |
| Surgical edits | Prefer targeted edits over rewrites, keep the artefact count low, fold rather than proliferate |
| Pointers over repetition | One canonical home per fact, echoes become short pointers to it |
| Preserve the flow spine | The end-to-end flow narrative, its diagram, and the core step table are never altered by a rationalisation pass |
| Calibrate expression to artefact type | A locked design doc stays neutral and impersonal, the personality and voice guidance of a humaniser pass does not apply to it |

### The artefact template

The canonical shape of a locked architecture decision, as the session converged on it.

1. Title and a short locked-on blockquote
2. Locked decision, the chosen path, run mode, and the facts that underpin it
3. Solution benchmark, the weighted score against selection criteria, with a verdict and the fallbacks
4. Diagram, the flow
5. Design steps, a step table with technical elements, benefits, watch-outs and sources
6. Component inventory, container technology and ownership per component
7. Implementation notes, refinements that do not replace the checks
8. Standing checks before a production commitment, the canonical caution list
9. Glossary, scoped to the concepts the design uses, placed near the end as reference
10. Official sources, numbered references
11. Version block, version, last updated, status

Cautions live once in the standing checks. Design-step watch-outs and implementation notes point to a check rather than restating it.

## Open decisions for the future skill

> DECISION PENDING: standalone skill versus fold into architecting-data-platforms. The proposal is a standalone orchestration skill (deciding-architecture) that owns the lifecycle, the gates, the benchmark format and the artefact template, and calls architecting-data-platforms only for domain knowledge, reviewing-tech-claims for verification, and editing-docs for expression. The alternative folds the lifecycle into architecting-data-platforms as reference files.

> DECISION PENDING: phase 7 default. Always emit Context plus Container views, or generate C4 only on request.

## Composition

| Concern | Owner |
| :--- | :--- |
| Decision lifecycle, gates, artefact template, rationalisation, C4 phase orchestration | the future deciding-architecture skill |
| Domain substance and selection criteria | architecting-data-platforms |
| Claim verification | reviewing-tech-claims |
| Expression, house style, Mermaid, and the future C4 generation | editing-docs |

---

| Field | Value |
| :--- | :--- |
| Version | 0.1 |
| Last Updated | 2026-06-24 |
| Status | Capture |
