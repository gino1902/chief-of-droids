# Design Interview

This interview bridges locked ADRs (the why) to two aligned outputs: the artefact skeleton (the per-file how) and the living design doc (the system-level how). Part A runs in Phase 0 to judge whether the ADRs are good enough to build on, and again in Phase 0b to reconcile existing outputs. Part B carries a decision into an artefact. Part C carries a decision into the living design doc. A single decision that feeds both is run once and rendered into both, see the resolve-once rule below.

## Overall rules

1. Ask, don't prescribe. For open design decisions, use free-form questions. Reserve multi-select for routing, like which unit to scaffold first or which section to revisit.
2. Push back once, maybe twice. If the first answer is weak, name the specific issue and ask a sharper question. If the second is still weak, write a placeholder and log the open decision. Do not let one element stall the design.
3. Quote the user back at them. When challenging an answer, use their own words verbatim.
4. Keep each answer to one to three sentences. A paragraph is usually hiding something vague.
5. Don't leak the anti-pattern names. Just ask the sharper question that follows.
6. Only interview where the ADRs are thin. If an ADR or the framing already determines an element, render it and move on.
7. Nothing silent. Every conflict, gap, or drift is put to the user. The skill never resolves one in a file on its own.
8. Resolve once, render to all consumers. Before interviewing, map each open decision to the outputs it feeds. A decision that feeds both an artefact element and a doc section is shared: ask it a single time, at the highest altitude it touches, apply the Part B and Part C pushback as relevant, and hold one answer to write into both. Never ask the same open decision twice, or the doc and the artefacts can diverge on it.

---

# Part A — Substrate readiness and reconciliation

Run this in Phase 0 before writing, and again in Phase 0b to reconcile existing outputs. For each mandatory input, check presence first, then quality. A present-but-weak input is a gap. Where an input fails, name what is missing and route to the skill that owns it.

## A1. ADRs and index

Strong: a set of ADRs whose status is Accepted or otherwise locked, listed in an index, covering the decisions the design must render.

Anti-patterns and pushback:

- No ADRs at all -> "There are no locked decisions to render yet. Run making-architecture-decision first, then come back."
- ADR still Draft -> "ADR-00N is still Draft. Scaffolding on an unlocked decision is rework if it flips. Lock it, or leave the artefact it shapes as a placeholder until it is."
- Index missing -> "No ADR index found. Proceeding in filename order, but the outputs cannot cite a canonical list. Worth adding one."
- Decisions that shape outputs are absent -> "The pipeline needs a compute and a trigger decision, and I find neither. That is an architecture decision, not a design one. Route it through making-architecture-decision or I place a cited placeholder and log it as open."

Route on failure: missing or Draft ADRs send the user to making-architecture-decision.

## A2. Framing

Strong: framing exists and names why the work is being done and who it is for.

Anti-patterns and pushback:

- Framing absent -> "There is no framing on file. Design decisions need the why and the for-whom to break ties. Run framing-project, or give me the one-line version now."
- Framing silent on the user -> "The framing does not say who this is for. When two options are otherwise equal, that is what decides. Who carries the outcome?"

Route on failure: send the user to framing-project.

## A3. Reviewer

Strong: a specific named person or role will review the design.

Anti-patterns and pushback:

- No reviewer -> "Who reviews this? A design no named person will read is a draft, not a design."
- "Someone on the team" -> "Name them or name the role. 'The team' reviews nothing in particular."

## A4. Consistency across decisions

Read the ADRs as a set, not one at a time. Two decisions that touch the same output or role must agree. Where they do not, surface the friction, do not resolve it silently.

Anti-patterns and pushback:

- Two ADRs contradict on the same element -> "ADR-00N and ADR-00M pull in different directions on <element>. I cannot render both. Which governs, and does the other need superseding?" Route to making-architecture-decision.
- Two ADRs shape the same role, unclear if one unit or two -> "ADR-00N and ADR-00M both shape <role>. One unit in two phases, or two deployable units? The answer changes the tree." Surface as a Decide, do not auto-split.
- A later ADR quietly weakens an earlier locked one -> name it, ask whether the earlier still holds.

## A5. Reconciliation across outputs (Phase 0b, refine runs)

On a re-run, an artefact tree or a living doc already exists. Diff three things, the ADRs, the doc, and the skeleton, and report every mismatch to the user before changing anything. Resolve each with them; reconcile nothing silently.

Anti-patterns and pushback:

- An ADR changed since the outputs were written -> "ADR-00N changed since this was scaffolded. The <artefact / doc section> that cites it no longer matches. Update it to the new decision, or is the output right and the citation stale?"
- The doc and the skeleton disagree -> "The design doc says <X> about <unit>, the skeleton renders <Y>. One is wrong. Which holds?"
- An artefact cites a superseded ADR -> "This cites ADR-00N, which ADR-00M superseded. Re-point it to the current decision?"
- A new ADR nothing renders -> "ADR-00P is locked but no artefact or doc section renders it. In scope for this design, or deliberately out?"

## A6. Recommended accelerators (warn, do not block)

- Source or entity inventory. Needed only to populate modelling artefacts with real entities. Absent -> proceed with placeholders and log the real model as open.
- Scratch topic map. If a prior session left one, read it as an accelerator. Not required, not an output.

---

# Part B — Carry a decision into an artefact

Use these rules for the artefact-facing side of any open decision that feeds an artefact. The aim is a file an engineer can clone, with the decision written in and the ADR cited. Execute elements do not use this interview, they render the locked value directly with an inline citation.

First classify. For the artefact in hand, read its governing ADRs and split it element by element. Fully determined by the ADR is Execute. Framed but left open is Decide. A file with both is Mixed.

Opening question, per Decide element: "ADR-00N frames this as <the locked constraint>. Within that frame, what is the specific choice, and what does it rest on?"

Strong answers name a concrete, buildable value, stay inside the ADR frame, and rest on the ADRs or framing rather than taste.

Anti-patterns and pushback:

- Reopening the architecture altitude (ADR locked serverless; user: "maybe a cluster here") -> "That is locked in ADR-00N and out of scope for the design. If it is genuinely wrong, that is a supersession in making-architecture-decision, not a file-level reversal."
- Floats free of any ADR ("let's add a caching layer") -> "Which ADR frames this? If none does, it is out of scope or a missing architecture decision. It cannot go in citing nothing."
- Gold-plating ("the schema should handle any future source") -> "That designs for a source that does not exist. What does the locked scope require? Scaffold for that."
- No basis where the frame constrains ("snake_case because I prefer it") -> "Does an ADR or the platform already set a convention? If yes, follow and cite it. If open, pick one and note in the README it was a free choice."
- Unbuildable ("the pipeline will be well structured") -> "An engineer cannot clone that. What is the concrete module boundary, key, or config value?"
- Coining where the ADR named the product -> "The ADR names the product, so derive the concrete identifier from it, not the better-known alias. Render it, cite the product, and flag it confirm-this because the derivation is version-sensitive."
- Restates behaviour the tests own -> "The test stub pins that. The code stub carries the seam and the citation, not behaviour a test fixes."
- Everything deferred ("leave all of these open") -> "If every element becomes a placeholder, the scaffold renders nothing. Which can you close now?"

Land the decision in the file, cite the ADR inline. When it cannot be closed, write a safe placeholder, cite the framing ADR, log the open decision in the README. When it is a derived identifier from a named product, render it in full and log a confirm-this line.

---

# Part C — Carry a decision into the living design doc

Use these rules for the doc-facing side of any decision that feeds a doc section, and to build the doc's own sections. The aim is a short, system-level doc that carries the how no single file can show, in its lane, referencing the ADRs rather than restating them.

## C0. Existence gate

Before interviewing the sections, decide whether the doc should exist at all. It is warranted by ambiguity in the shared band (unit boundaries, seam contracts, data model) or in a doc-only concern (cross-cutting: security, privacy, observability at the system level). One or the other is enough.

- If such ambiguity exists, write the doc. If none does, emit a minimal stub (context, goals, and pointers to the ADRs and artefacts) and stop.

Anti-patterns and pushback:

- Doc would restate the ADRs -> "Everything here is already decided in the ADRs. A doc that repeats them is a summary, not a design. I will write a minimal stub that points to them unless there is a system-level question they leave open. Is there one?"
- Doc would be an implementation manual -> "That is per-file detail the artefacts already carry. The doc's job is the cross-unit and cross-cutting view. What of that is still open?"

## C1. Sections

Interview only the sections where the ADRs are thin. A section that draws on a shared decision uses the answer already resolved for the artefacts, per the resolve-once rule, it is not asked again. Each section stays in the doc's lane: system-level how, not the why, not per-file config, not operational steps.

- Context and scope. The landscape the system sits in and where its edges are. Opening: "In a few lines, what is the landscape this fits into, and where are its edges?"
- Goals and non-goals. Bullet lists. Non-goals matter as much as goals. Opening: "What must this design achieve, and what is explicitly out of scope?"
- Design, system level. How the units fit and hand data across, with a system-context diagram where topology is the point. Draws on the shared boundary and data-model decisions. Opening: "How do the units connect, and how does data move between them?"
- Contracts between units. Schema, keys, casing, promotion rules, provenance at the seams. A shared decision with the artefacts. Opening: "What is the contract at each seam between units?"
- Cross-cutting concerns. Security, privacy, observability across the whole. Usually doc-only. Opening: "How are security, privacy, and observability handled across units, not file by file?"

Strong answers are concrete, span more than one unit, stay at the system level, and cite the ADRs that frame them.

Anti-patterns and pushback:

- Restates an ADR's rationale -> "That is the why, and it lives in ADR-00N. The doc references it. What is the how at the system level?"
- Drops to per-file detail -> "That is in the artefact. The doc carries the cross-unit view. What spans the units here?"
- Bloat past a few pages of a small design -> "This is running long for the size of the change. What is the load-bearing part a reviewer must see? Cut the rest."
- Re-lists alternatives -> "Alternatives considered live in the ADRs. The doc states the chosen design and points to the ADR for the alternatives."
- A section with nothing system-level to say -> "Nothing here is open at the system level. Drop the section rather than pad it."

Land each section in the doc with its ADR references. Log any system-level question that cannot be closed as an open item in the doc and, if it blocks an artefact, in the README too.

---

## After the interview

Part A gates the run and, on a re-run, reconciles the outputs; if a mandatory input failed or a conflict was not resolved, stop and route, do not write a partial design. Each open decision is resolved once and its answer written into every output that consumes it, artefacts via Part B, the doc via Part C, per `references/design-template.md`. Each open decision that could not be closed is a placeholder plus a logged line, in the README for an artefact and in the doc's open items for a system-level one.
