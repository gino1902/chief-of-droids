---
name: writing-technical-design
description: "Turn a locked set of architecture decisions (ADRs) into two aligned outputs: the concrete artefact skeleton that renders them (project tree, config and pipeline files, code stubs, CI file, README) and a living design document that carries the system-level how (context, goals, cross-unit design, contracts, cross-cutting concerns). A guided interview bridges each decision to its artefact and gathers the system-level design, from the ADR (the why) to the file and the doc (the how). Use this after making-architecture-decision has locked the ADRs and the build scaffold and design doc still need writing, in software design or data-platform design. Invoke as `writing-technical-design from <adr-dir>`. Trigger whenever the user asks to scaffold, draft, or update the technical design, the living design doc, the build skeleton, the asset bundle, or the artefacts that follow a set of ADRs. Not for making architecture decisions (that is making-architecture-decision) and not for producing a populated, runnable repo (this writes an illustrative skeleton, not the real system)."
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob
---
# Writing a technical design

Note: the current year is 2026. Use this when dating the artefacts.

`writing-technical-design` turns locked architecture decisions into the design that renders them. It reads the ADRs and produces two aligned outputs: an artefact skeleton (the per-file how) and a living design document (the system-level how). Every output cites the ADR it rests on, so both stay traceable to the decisions that shaped them.

It sits at the bottom of a three-step pipeline. `framing-project` sets the why and for whom. `making-architecture-decision` locks the decisions as ADRs, listed in the ADR index. This skill writes the how, and only the how.

## Two outputs and their lanes

The two outputs plus the ADRs and the README are four things describing the same system. They stay useful only if each keeps to its own altitude. A living design doc that drifts into the others' lanes becomes a summary of the ADRs, which is the failure mode this skill exists to avoid.

| Output | Owns | Must not carry |
|:-------|:-----|:---------------|
| ADRs (upstream, not written here) | Why, the decision, alternatives considered | The how |
| Living design doc | System-level how: context and scope, goals and non-goals, cross-unit design overview, system-context diagram, data flow across units, contracts between units, cross-cutting concerns (security, privacy, observability) | Per-file config, the why, operational steps |
| Artefact skeleton | Per-unit and per-file how, ADR cited inline | System-level narrative |
| README (part of the skeleton) | Operational: what is here, names to replace, open decisions, validate and run | Design rationale |

## From decision to artefact

The skill is a bridge with two ends and an interview between them.

The ADR is the from. It is a locked architecture decision. This skill never makes one. If an artefact or a design-doc section needs a decision that no ADR made, that is a gap: surface it and route the user to `making-architecture-decision`. Do not invent the decision in a file or a doc.

The artefact is one to. It is the concrete file that makes the decision real: a `variables.yml`, a `*.pipeline.yml`, a `bronze.py`, an `azure-pipelines.yml`, the tree they sit in. It is a skeleton, not a running system: placeholder names, an unverified warning, open decisions logged in the README.

The living design doc is the other to. It carries the how that no single file can show: the system in context, the goals and non-goals, how the units fit and hand data across, the contracts between them, and the cross-cutting concerns. Its shape follows the design-doc practice (context and scope, goals and non-goals, the design, cross-cutting), adapted so the why and the alternatives stay in the ADRs and the doc references them rather than re-arguing them.

The interview is the bridge. For each element it decides how the ADR reaches the output:

- Execute. The ADR fully determines the element. Render it straight and cite the ADR. Example: ADR-004 locks serverless, so the pipeline file gets `serverless: true` with `(ADR-004)` on the line.
- Decide. The ADR frames the element but leaves the specific open. Resolve it with the user and write the result, or, if it cannot be closed now, write a placeholder and log the open decision in the README. Example: the conformed silver model is framed by ADR-001 but the entities are open.
- Mixed. Part Execute, part Decide. Split it, render the locked part, resolve or placeholder the open part.

## The living design doc, and when to skip it

The doc is conditional, not automatic. Following the design-doc practice, write it only where genuine ambiguity exists at the system level or in a cross-cutting concern. If the ADRs and the artefacts already settle everything and the doc would be "merely an implementation manual," say so and emit a minimal stub (context, goals, and a pointer to the ADRs and artefacts) rather than padding it into a summary.

Keep it short. One to three pages for an incremental design, more only for a genuinely large system. The doc carries the design and its seams, not code and schemas the artefacts already hold.

## Interaction method

Generate and guide, built for iterative change. Derive the artefact set and the doc's system-level scope from the ADRs, then work through both. For each artefact, gather its governing ADRs, classify each element Execute or Decide, and bridge it to its file. For the design doc, gather the system-level and cross-cutting content the ADRs frame but no single file can show.

For Execute elements, render the locked decision without asking, and cite the ADR. For Decide elements, resolve with the user where the ADRs or framing are thin, one focused question at a time, and write the answer in. Do not stall the whole design on one thin element: write the placeholder, log the open decision, keep moving.

Never resolve a conflict or a gap silently. When two ADRs pull against each other, when an output needs a decision no ADR made, or when a re-run finds the outputs and the ADRs have drifted apart, stop and put it to the user. The user is always prompted; the skill never picks a side in a file.

## Core principles

1. Artefacts and the doc are downstream of decisions. Render what the ADRs locked, resolve only the specifics they left open, never reopen a locked decision. A changed decision goes back through supersession in `making-architecture-decision`.
2. Everything cites its ADR. In the artefacts the citation is inline, on the line or in the docstring. In the design doc it is a reference in the relevant section. An element that cites no ADR either rests on a missing decision or does not belong.
3. Keep to the lanes. The doc carries the system-level how, the artefacts the per-file how, the README the operational how, the ADRs the why. Do not let any output restate another's content.
4. Resolve once, render to all consumers. A decision that feeds more than one output is asked once, at the highest altitude it touches, and its answer is written into every output that consumes it. Never resolve the same open decision twice, once for the doc and once for the artefacts, or the two answers can diverge.
5. The doc is conditional. Produce it only where system-level or cross-cutting ambiguity is real. Otherwise emit a minimal stub. A design doc that only restates the ADRs and the artefacts should not exist.
6. Nothing silent. Conflicts, gaps, and drift are surfaced to the user, never resolved by fiat in a file.
7. Skeleton, not system. One of each artefact, placeholder names, an unverified warning, open decisions logged. The skill designs the scaffold and the doc, it does not populate or run anything.

## Execution flow

### Phase 0: Ready-to-build gate

The design cannot start on weak substrate, so the run refuses rather than guessing. Read `references/design-interview.md` and apply Part A. This load is non-optional: the substrate quality bar and the pushback lines live there. Judge each mandatory input on presence and then quality, and read the ADRs as a set, surfacing any contradiction or friction between decisions rather than resolving it silently. If any check fails, stop, name exactly what is missing, weak, or in tension, and route the user to the skill that owns it.

Mandatory:

- The ADRs and the ADR index, reachable and locked. Missing or still Draft → point to `making-architecture-decision`.
- Framing, the why and for whom. Missing → point to `framing-project`.
- A named reviewer for the design. Missing → ask the user for one.

Recommended, warn but do not block: a source or entity inventory, needed only to populate modelling artefacts with real entities. A scratch topic map, if one exists, read as an accelerator.

Enumerate the ADR directory with Glob, then read the ADRs and index as parallel calls.

Route on output state. If outputs already exist at the target, this is a refine run: go to Phase 0b. Otherwise go to Phase 1.

### Phase 0b: Reconcile (refine runs only)

When an `artefacts/` tree or a living design doc already exists, do not overwrite blindly. Diff the three: the ADRs, the design doc, and the skeleton. Apply Part A's consistency rules across all three. Report every drift, conflict, and new gap to the user as a list, and resolve each with them before refining: an ADR that changed and now conflicts with a rendered artefact, a doc section that no longer matches the tree, an artefact citing a superseded ADR, a new ADR nothing renders yet. Nothing is reconciled silently. Only once the list is resolved do you carry into Phase 1 to apply the agreed changes, preserving everything already resolved and untouched.

### Phase 1: Bridge decisions to outputs

First derive the artefact set and the doc scope. From the ADRs and the tree shape in `references/design-template.md`, list the artefacts the scaffold needs. From the ADRs and the design-doc template, decide whether the living doc is warranted (the existence gate) and which system-level and cross-cutting sections it must carry.

Then map every open decision to the outputs it feeds. A decision that feeds both an artefact element and a doc section is shared; one that feeds only one is lane-only. This mapping falls out of the ADR-to-output coverage tracking you already keep.

Then resolve once, render to all consumers. Interview each open decision a single time, at the highest altitude it touches, using the Part B rules for its artefact-facing framing and the Part C rules for its doc-facing framing, and hold one answer to write into every output that consumes it. A shared decision is never asked twice. Execute elements skip the interview and render directly with an inline citation. Where a decision cannot be closed, hold a placeholder for it and a logged open item.

Hold the resolved content in memory, keyed by decision, with the outputs each feeds. Do not write yet.

### Phase 2: Write the design

Read `references/design-template.md` for the artefact tree, the per-artefact rules, the README convention, and the living design doc template. Assemble the artefact tree, each file citing its ADRs inline, placeholders where a name is not yet real, and a version block on each markdown file. Write the README (operational) and, where warranted, the living design doc (system-level), each in its lane.

Before writing, run the traceability and lane checks. Every ADR is cited by at least one output; an ADR rendered nowhere is out of scope or a gap, logged in the README and the doc's open items. Every artefact cites at least one ADR. No output restates another's lane: the doc carries no per-file config, the README no rationale.

Write under an `artefacts/` directory and the design doc beside it, siblings of the ADR directory by default, or wherever the user names. Present the tree, the key files, and the doc outline in chat, offer one round of edits, then write.

## What this skill does not do

- Does not make architecture decisions. Those are locked upstream in ADRs. A needed-but-missing decision is a gap to route, not a choice to invent.
- Does not produce a populated, runnable repo. It writes one illustrative skeleton of each artefact and a system-level design doc, with placeholders and an unverified warning.
- Does not run or validate the artefacts. It tells the user how to validate them.
- Does not reopen or rewrite a locked ADR. A changed decision goes through supersession.
- Does not write a design doc that restates the ADRs or the artefacts. Where there is no system-level ambiguity to carry, it emits a minimal stub instead.

## Learn more

The living design doc follows Malte Ubl's "Design docs at Google" (https://www.industrialempathy.com/posts/design-docs-at-google/): context and scope, goals and non-goals, the design, cross-cutting concerns, kept short and written for a named reviewer, living through creation, review, and maintenance. It is adapted so the why and the alternatives stay in the ADRs and the doc references them. The artefact-over-prose stance draws on Simon Brown's C4 model (https://c4model.com/) and the arc42 template (https://arc42.org/). The bias toward a skeleton and deciding at the last responsible moment draws on Martin Fowler's YAGNI (https://martinfowler.com/bliki/Yagni.html). The frozen ADR paired with a living design comes from the companion `making-architecture-decision` skill.

---

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
