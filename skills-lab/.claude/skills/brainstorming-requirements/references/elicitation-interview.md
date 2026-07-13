# elicitation-interview

How to gather what a component slice needs, through dialogue, before `writing-requirements` formalises it. This is the Phase 1 interview guide for `brainstorming-requirements`. The companion `elicitation-template.md` governs the shape of the output; this governs how to reach it.

## Stance

Anchor every question in the FRAMING. The framing is the intent (problem, approach, who it is for, success, tracks, out of scope); the interview turns one surface of it into requirement-shaped substance.

- One question per turn. Do not stack questions.
- Ask open questions. Do not offer a menu that invents the answer, since the downstream skill will not synthesise what the dialogue did not settle.
- Do not ask about internal design, data schemas, or the wire contract between components. That is a how, out of altitude for this chain.
- A field the user genuinely leaves open is recorded as open, never invented.

## The four fields, in order

Settle these for the one chosen component. Each carries the probe that raises quality.

### 1. Purpose

Ask what the component is for, in one sentence. You need an explicit statement, not an inference from surrounding prose, because the slice must state it outright.

Probe: if the answer describes a whole track rather than one component, narrow it. "Which single deployable part of that are we refining this pass?"

### 2. Scope

Ask what the component covers. Then ask, by negation, what it does not, and who owns each excluded piece. Both directions matter: the exclusions with named owners are what make boundaries real.

Probe: for each excluded item, "who owns that instead?" An out-of-scope item with no owner is a boundary that has not actually been decided.

### 3. Actors and consumers

Ask what is upstream of the component (what feeds it, systems and human roles) and what is downstream (what consumes its output). Keep it directional.

Probe: "what triggers it, and who or what relies on what it produces?" Name systems and roles, not mechanisms.

### 4. Requirements

Ask what must be true for the component. Elicit them one behaviour at a time, and shape each into the requirement contract: actor / action / result / conditions and limitations (defined in `elicitation-template.md`). For each behaviour, make sure you have the actor that acts, the action it takes, the result it achieves ("so that <consequence>", the purpose, not the action's direct object), and the conditions or limitations under which it holds. Ask "so that what?" to surface the result if the user gives only an action.

Probe, the load-bearing one, sits in the conditions-and-limitations part: push every requirement toward an observable, testable condition. If the user says "fast", "robust", "scalable", or "reliable", ask for the number or the observable behaviour. "Within how many milliseconds?" "Reliable meaning what, observed how?" A requirement with no conditions clause cannot be turned into an acceptance criterion downstream, so it will come back as a Warning. Chasing the predicate here is what keeps the Warning count low.

## Domain language

Draw the terms you use from `CONCEPTS.md` (read in Phase 0). Do not mint a domain term that lives only in this slice. Language invented late and locally drifts, and two components end up naming the same thing differently, which is the ubiquitous-language anti-pattern in domain-driven design.

- Use the exact term from `CONCEPTS.md` when one exists for a concept, rather than a synonym.
- When the dialogue surfaces a genuinely new term, capture it with a one-line definition and record it back to `CONCEPTS.md`, under the owning context or the shared core if it means one thing everywhere. Do not leave it defined only inside the slice.
- If `CONCEPTS.md` is absent, still record the terms you settle, so a later framing run can seed it.

Every domain term the requirements lean on must reach the glossary downstream, so make sure each is either backticked or explicitly defined in the slice (see `elicitation-template.md`).

## Exit

Leave Phase 1 when purpose, scope (both directions, exclusions owned), actors and consumers, the requirements (each with a measurable predicate or explicitly flagged as open), and the domain terms (drawn from or recorded back to `CONCEPTS.md`) are settled for the component. Then emit the slice per `elicitation-template.md`.

| Field        | Value      |
|--------------|------------|
| Version      | 1.3        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
