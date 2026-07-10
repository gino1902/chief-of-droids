# Design Interview

This interview is the bridge from a locked ADR (the why) to a concrete artefact (the how). Part A runs in Phase 0 to judge whether the ADRs are good enough to build on. Part B runs in Phase 1 for every Decide element, to carry the decision into its file. Both parts share the pushback discipline below.

## Overall rules

1. Ask, don't prescribe. For open design decisions, use free-form questions. Reserve multi-select for routing, like which unit to scaffold first or which artefact to revisit on a re-run.
2. Push back once, maybe twice. If the first answer is weak, name the specific issue and ask a sharper question. If the second is still weak, write a placeholder and log the open decision in the README. Do not let one element stall the scaffold.
3. Quote the user back at them. When challenging an answer, use their own words verbatim. Paraphrase softens the challenge.
4. Keep each answer to one to three sentences. A paragraph is usually hiding something vague. Ask the user to pick the sentence that matters.
5. Don't leak the anti-pattern names. The user does not need to hear "that's gold-plating", just ask the sharper question that follows.
6. Only interview where the ADRs are thin. If an ADR or the framing already determines an element, render it and move on. Interrogating the user for something already locked wastes the run.

---

# Part A — Substrate readiness

Run this in Phase 0 before writing anything. For each mandatory input, check presence first, then quality. A present-but-weak input is a gap. Where an input fails, name what is missing and route to the skill that owns it rather than scaffolding around the hole.

## A1. ADRs and index

Strong: a set of ADRs whose status is Accepted or otherwise locked, listed in an ADR index, covering the decisions the scaffold must render.

Anti-patterns and pushback:

- No ADRs at all -> "There are no locked decisions to render yet. A scaffold with no ADRs is guesswork. Run making-architecture-decision first, then come back."
- ADR still Draft -> "ADR-00N is still Draft. Scaffolding on an unlocked decision is rework if it flips. Lock it in making-architecture-decision, or leave the artefact it shapes as a placeholder until it is."
- Index missing -> "No ADR index found. Proceeding, but I will read the ADRs in filename order and the README will not be able to cite a canonical list. Worth adding one."
- Decisions that shape artefacts are absent (for example no compute or orchestration ADR, yet a pipeline is expected) -> "The pipeline needs a compute and a trigger decision, and I find neither in the ADRs. That is an architecture decision, not a design one. Route it through making-architecture-decision or I place a cited placeholder and log it as an open decision."

Route on failure: missing or Draft ADRs send the user to making-architecture-decision.

## A2. Framing

Strong: framing exists and names why the work is being done and who it is for.

Anti-patterns and pushback:

- Framing absent -> "There is no framing on file. Design decisions need the why and the for-whom to break ties. Run framing-project, or give me the one-line version now."
- Framing present but silent on the user -> "The framing does not say who this is for. When two artefact options are otherwise equal, that is what decides. Who carries the outcome?"

Route on failure: send the user to framing-project.

## A3. Reviewer

Strong: a specific named person or role will review the scaffold.

Anti-patterns and pushback:

- No reviewer -> "Who reviews this scaffold? A design no named person will read is a draft, not a design."
- "Someone on the team" -> "Name them or name the role. 'The team' reviews nothing in particular."

## A4. Consistency across decisions

The gate reads the ADRs as a set, not one at a time. Two decisions that touch the same artefact or role must agree on its shape. Where they do not, surface the friction, do not resolve it silently in a file.

Strong: the ADRs fit together, and any pair that shapes the same element or role is consistent about it.

Anti-patterns and pushback:

- Two ADRs contradict on the same element (one mandates X, another implies not-X) -> "ADR-00N and ADR-00M pull in different directions on <element>. I cannot render both. Which governs, and does the other need superseding?" Route the contradiction to making-architecture-decision.
- Two ADRs shape the same role and it is unclear whether that is one deployable unit or two, for example an end-state ingestion and a temporary bridge for the same producer -> "ADR-00N and ADR-00M both shape <role>. Is that one bundle in two phases, or two separate deployable units? The answer changes the tree." Surface as a Decide, do not auto-split.
- A later ADR quietly weakens an earlier locked one -> name it, and ask whether the earlier one still holds.

Route on failure: a genuine contradiction goes to making-architecture-decision. A friction that is really an open design choice becomes a Decide element, carried into Part B.

## A5. Recommended accelerators (warn, do not block)

- Source or entity inventory. Needed only to populate modelling artefacts with real entities. Absent -> proceed with placeholder entities and log the real model as an open decision. Do not block.
- Scratch topic map. If a prior session left one, read it as an accelerator for the Execute and Decide split. It is not required and it is not an output, and its absence changes nothing, the interview derives the split from the ADRs regardless.

---

# Part B — Bridge each decision to its artefact

Run this in Phase 1 for each element the ADRs leave open. The aim is a file an engineer can clone, with the decision written in and the ADR cited, made at design altitude. Execute elements do not use this interview, they render the locked value directly with an inline citation.

First, classify. For the artefact in hand, read its governing ADRs and split it element by element. An element the ADR fully determines is Execute. An element the ADR frames but leaves open is Decide. A file with both is Mixed, handle each element in its own mode.

Opening question, per Decide element: "ADR-00N frames this as <the locked constraint>. Within that frame, what is the specific choice, and what does it rest on?"

Strong answers name a concrete, buildable value (a name, a key, a boundary, a config value), stay inside the ADR frame rather than reopening it, and rest on the ADRs or the framing rather than on taste alone.

Anti-patterns and pushback:

- Reopening the architecture altitude (ADR locked serverless; user: "maybe a cluster here") -> "That is an architecture decision, locked in ADR-00N, and it is out of scope for the scaffold. If it is genuinely wrong, that is a supersession in making-architecture-decision, not a design-time reversal in a file."
- Floats free of any ADR ("let's add a caching layer") -> "Which ADR frames this? If none does, it is either out of scope or a missing architecture decision. It cannot go in the scaffold citing nothing."
- Gold-plating, building for what is not needed ("the schema should handle any future source") -> "That designs for a source that does not exist yet. What does the locked scope actually require? Scaffold for that, and let the future source arrive with its own decision."
- No basis, arbitrary where the frame constrains ("snake_case because I prefer it") -> "Does an ADR or the existing platform already set a convention? If yes, follow it and cite it. If it is genuinely open, pick one and note in the README that it was a free choice."
- Unbuildable, too vague to render ("the pipeline will be well structured") -> "An engineer cannot clone that. What is the concrete module boundary, the key, or the config value that goes in the file?"
- Coining where the ADR named the product (ADR names "Lakeflow Spark Declarative Pipelines"; agent reaches for the familiar `import dlt`) -> "The ADR names the product, so the concrete identifier is derived from it, not from the better-known alias. Derive it (`from pyspark import pipelines`), cite the product, and, because that derivation is version-sensitive, render it and log it as a confirm-this open decision." A literal token the ADR does not write is derived-and-flagged when it names a product, and only a genuinely unnamed concept is a free Decide.
- Restates behaviour the tests own ("write out that the function returns X on input Y") -> "The test stub pins that. The code stub carries the seam and the citation, not behaviour a test already fixes."
- Everything deferred ("leave all of these open") -> "If every element becomes a placeholder, the scaffold renders nothing. Which can you close now with what you have? Open decisions are for genuinely blocked specifics, not for dodging the call."

Land the decision. Each resolved element ends in a file, not in a note. Write the value into the artefact and cite the ADR inline on the line or in the docstring. A decision captured in chat but not written to a file is not done.

When it cannot be closed. Write a safe placeholder into the artefact, cite the framing ADR, and log the open decision in the README under open decisions still to make, with one line on what is needed to close it. Do not guess a value and render it as if locked.

When it is derived, not open. A concrete identifier derived from a named product is rendered in full, not placeheld, and additionally logged as a confirm-this line in the README when it is load-bearing. It is closed enough to build on, flagged only so a human can confirm the derivation against the product's current version.

---

## After the interview

Part A gates the run. If a mandatory input failed and was not fixed, stop and route, do not write a partial scaffold. Part B feeds Phase 2: each resolved element is written into its artefact with an inline citation, and each open decision is both a placeholder in the file and a line in the README, per `references/design-template.md`.
