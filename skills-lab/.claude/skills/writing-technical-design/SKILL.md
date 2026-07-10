---
name: writing-technical-design
description: "Turn a locked set of architecture decisions (ADRs) into the concrete artefact skeleton that renders them: the project tree, config and pipeline files, code stubs, CI file, and a README. A guided interview bridges each decision to its artefact, from the ADR (the why) to the file (the how). Use this after making-architecture-decision has locked the ADRs and the build scaffold still needs writing, in software design or data-platform design. Invoke as `writing-technical-design from <adr-dir>`. Trigger whenever the user asks to scaffold, draft, or update the technical design, the build skeleton, the asset bundle, or the artefacts that follow a set of ADRs, even if they name only the ADRs and not the word artefact. Not for making architecture decisions (that is making-architecture-decision) and not for producing a populated, runnable repo (this writes an illustrative skeleton, not the real system)."
allowed-tools: Read, Write, Edit, Glob
---
# Writing a technical design

Note: the current year is 2026. Use this when dating the artefacts.

`writing-technical-design` turns locked architecture decisions into the artefacts that render them. It reads the ADRs, then walks decision by decision and writes an illustrative artefact skeleton: the folder tree, the config and pipeline files, the code stubs, the CI file, and a README. Every artefact cites the ADR it rests on, inline, so the scaffold is traceable to the decisions that shaped it.

It sits at the bottom of a three-step pipeline. `framing-project` sets the why and for whom. `making-architecture-decision` locks the decisions as ADRs and the ADR index lists them. This skill writes the how, as artefacts, and only the how.

## From decision to artefact

The skill is a bridge with two ends and an interview between them.

The ADR is the from. It is a locked architecture decision: the platform, the medallion model, serverless compute, the deployment unit. This skill never makes one. If an artefact needs a decision that no ADR made, that is a gap, surface it and route the user to `making-architecture-decision`. Do not invent the decision in a file.

The artefact is the to. It is the concrete file that makes the decision real: a `variables.yml`, a `*.pipeline.yml`, a `bronze.py`, an `azure-pipelines.yml`, the tree they sit in. The artefact is a skeleton, not a running system. It uses placeholder names, carries an unverified warning, and logs its open decisions in the README. This is the design altitude, one below the ADR and one above the populated repo.

The interview is the bridge. For each element of each artefact, it decides how the ADR reaches the file:

- Execute. The ADR fully determines the element. Render it straight into the file and cite the ADR inline. Example: ADR-004 locks serverless, so the pipeline file gets `serverless: true` with `(ADR-004)` on the line.
- Decide. The ADR frames the element but leaves the specific open. Resolve it with the user through the interview and write the result into the file, or, if it cannot be closed now, write a placeholder and log the open decision in the README. Example: the conformed silver model is framed by ADR-001 but the entities are open.
- Mixed. Part of the file is Execute and part is Decide. Split it, render the locked part, resolve or placeholder the open part.

There is no topic map in the loop. A map may exist as a scratch note from an earlier session, and if present it is a useful accelerator, but it is not an input this skill needs. The interview derives the Execute and Decide split from the ADRs directly.

## Interaction method

Generate and guide, built for iterative change. Derive the artefact set from the ADRs, then walk artefact by artefact. For each artefact, gather its governing ADRs, work out which elements are Execute or Decide, then bridge each to its file.

For Execute elements, render the locked decision without asking, and cite the ADR inline.

For Decide elements, resolve the design decision with the user. Where the ADRs or the framing carry the answer, propose it and write it. Where they are thin, ask one focused question at a time, the way `making-architecture-decision` interviews, and write the answer into the artefact. Do not stall the whole scaffold on one thin element. Write the placeholder, log the open decision in the README, and keep moving.

The scaffold is meant to be re-run. Point the skill at an existing `artefacts/` tree to refine it. Preserve elements already resolved unless an ADR or the user changes them.

## Core principles

1. Artefacts are downstream of decisions. Render what the ADRs locked, resolve only the specifics they left open, and never reopen a locked decision in a file. A changed architecture decision goes back through supersession in `making-architecture-decision`.
2. Every artefact cites its ADR. The traceability lives inline in the file, as a comment on the line or in the module docstring, not in a separate document. An element that cites no ADR either rests on a missing decision or does not belong in the scaffold. A named product determines its own concrete identifiers, so deriving them from it is Execute, not a coin, and only a genuinely unnamed concept is a Decide.
3. The bridge has three modes. Execute renders, Decide resolves or placeholders, Mixed splits. Honour the mode element by element rather than blurring the altitudes.
4. Skeleton, not system. One of each artefact, placeholder names, an unverified warning, open decisions logged in the README. The skill designs the scaffold, it does not populate or run it.
5. Less is more. The artefact form is the design: a YAML file, a tree, a code stub carry the decision more precisely than prose. The only prose is the README. Delete any file that would carry nothing.

## Execution flow

### Phase 0: Ready-to-build gate

The scaffold cannot start on weak substrate, so the run refuses rather than guessing. Read `references/design-interview.md` and apply Part A. This load is non-optional: the substrate quality bar and the pushback lines live there, and a bare presence check lets a still-Draft ADR or an unframed project through. Judge each mandatory input on presence and then quality, and read the ADRs as a set, surfacing any contradiction or friction between decisions rather than resolving it silently in a file. If any check fails, stop, name exactly what is missing, weak, or in tension, and route the user to the skill that owns it. Do not half-write a scaffold on assumptions.

Mandatory:

- The ADRs and the ADR index, reachable and locked. Missing or still Draft → point to `making-architecture-decision`.
- Framing, the why and for whom. Missing → point to `framing-project`.
- A named reviewer for the scaffold. Missing → ask the user for one.

Recommended, warn but do not block: a source or entity inventory, needed only to populate modelling artefacts with real entities rather than placeholders. A scratch topic map, if one exists, read as an accelerator. Where these are absent, proceed with placeholders and log the gap as an open decision in the README rather than burying it.

Enumerate the ADR directory with Glob to find the ADRs and the index, then read them. These reads are independent, issue them as parallel tool calls.

Route on the output state. If an `artefacts/` tree already exists at the target, this is a refine run: enumerate it with Glob, preserve elements already resolved, and re-open only what an ADR or the user changes. Otherwise this is a first scaffold.

### Phase 1: Bridge decisions to artefacts

First derive the artefact set: from the ADRs and the tree shape in `references/design-template.md`, list the artefacts the scaffold needs. Then walk artefact by artefact. For each artefact, gather its governing ADRs, classify every element as Execute or Decide per the modes above, and run Part B of `references/design-interview.md` for each Decide element, so the decision lands in the file concrete, in-frame, and cited, rather than vague. Execute elements skip the interview and render directly. Track which ADRs each artefact cites, so the index doubles as a coverage checklist. Hold the resolved content for each artefact in memory. Do not write yet.

### Phase 2: Write the scaffold

Read `references/design-template.md` for the tree shape, the per-artefact rules, and the README convention. Assemble the artefact tree, each file citing its governing ADRs inline, placeholders where an entity or name is not yet real, and the version block at the bottom of each markdown file. Write the README last: what is here, names to replace, open decisions still to make, and the unverified warning.

Before writing, run two traceability checks against the index. Every ADR must be cited by at least one artefact, an ADR rendered nowhere is either out of scope or a gap, so log it in the README under open decisions. Every artefact must cite at least one ADR, one that cites none does not belong in the scaffold. Fix both before writing.

Write the tree under an `artefacts/` directory, a sibling of the ADR directory by default, or wherever the user names. Present the tree and the key files in chat, offer one round of edits, then write.

## What this skill does not do

- Does not make architecture decisions. Those are locked upstream in ADRs by `making-architecture-decision`. A needed-but-missing decision is a gap to route, not a choice to invent.
- Does not produce a populated, runnable repo. It writes one illustrative skeleton of each artefact, with placeholders and an unverified warning.
- Does not run or validate the artefacts. It tells the user how to validate them, it does not execute them.
- Does not reopen or rewrite a locked ADR. A changed decision goes through supersession.

## Learn more

The scaffold-and-cite approach follows the widely used engineering practice of a lean, living design that renders decisions rather than re-argues them, documented by Malte Ubl in "Design docs at Google" (https://www.industrialempathy.com/posts/design-docs-at-google/). The artefact-over-prose stance draws on Simon Brown's C4 model (https://c4model.com/) and the arc42 template (https://arc42.org/). The bias toward a skeleton and deciding at the last responsible moment draws on Kent Beck's incremental design and Martin Fowler's YAGNI (https://martinfowler.com/bliki/Yagni.html). The frozen ADR paired with a living scaffold comes from the companion `making-architecture-decision` skill.
