---
name: brainstorming-requirements
description: Refines a FRAMING-anchored product idea, through one-question-per-turn dialogue, into a single component slice that writing-requirements can solidify with no synthesis. Elicits requirements before they are written. Invoke as `brainstorming-requirements from <framing-path> [--target <track-or-component>]`. This is the elicitation half of the pair elicit-then-write; writing-requirements is the writing half. Use when a project has a FRAMING.md and you need to turn one of its tracks or surfaces into requirement-shaped substrate ready for formalisation.
allowed-tools:
  - Read
  - Write
---

# brainstorming-requirements

Refines the what of one product surface, anchored in project FRAMING, into a component slice that is clean substrate for `writing-requirements`. It elicits requirements through dialogue; the downstream skill writes them. The governing constraint is that `writing-requirements` does not synthesise, so everything this skill wants formalised must be made explicit and correctly shaped in the slice, per `references/elicitation-template.md`.

**Thin-slice scope.** This version handles one component per run. Multi-component fan-out, a system-level cross-cutting slice, approach exploration, resume logic, and any downstream handoff beyond emitting the slice are deliberately out of scope.

**Standalone use.** Running this skill on its own, a one-shot brainstorm from a FRAMING with no project around it and no `CONCEPTS.md` beside it, is valid and terminal. It needs no bootstrapped project, and the slice it emits is the deliverable. Carrying that slice onward into `writing-requirements` is discouraged: the formalisation chain proper starts from a bootstrapped or `framing-project` project, not from a decoupled brainstorm. The Phase 2 emission still reports the downstream invocation for the in-chain case; treat it as not applying to a standalone run.

<reference-files>

| File | Load at | Condition |
|:--|:--|:--|
| `references/elicitation-interview.md` | Phase 1 | Always |
| `references/elicitation-template.md` | Phase 1 | Always |

</reference-files>

## Invocation

```
brainstorming-requirements from <framing-path> [--target <track-or-component>]
```

- `<framing-path>` — path to a FRAMING.md. Required. Read-only anchor.
- `--target` — optional name of the track or surface to refine this pass. If absent, resolve it in Phase 0 by asking.

## Phase 0 — Anchor & scope

1. Read the FRAMING.md at `<framing-path>`. Treat it as the intent anchor: the problem, the approach, who it is for, what success means, the tracks, and what is out of scope.
2. Read `CONCEPTS.md` if it sits beside the FRAMING. It is the project's domain language, the single source of terms. Use its terms in this slice; do not mint your own for concepts it already names. If it is absent, proceed, and record the terms you settle so they can seed it later.
3. If a sibling grounding file is offered by the caller (for example a process taxonomy), read it too. Do not go looking beyond what is supplied.
4. Resolve the target surface for this pass. If `--target` was given, use it. Otherwise ask which track or surface to refine, one question, offering the FRAMING tracks as the options.
5. Confirm the target is a single deployable component (a service, pipeline, app, or module). If the target is a whole track that clearly spans several components, say so and ask the user to name the one component to refine this pass. Do not split it yourself.
6. Resolve a slug for the component: lowercase, `^[a-z0-9-]+$`, and it must not contain `requirement`, `req`, or `reqs` (those collide downstream). Propose one, confirm it.

## Phase 1 — Refine (dialogue)

Load both references first: `references/elicitation-interview.md` (how to gather) and `references/elicitation-template.md` (the shape you are gathering toward).

Run the interview per `references/elicitation-interview.md`: one question per turn, grounded in the FRAMING anchor, settling purpose, scope (both directions, exclusions owned), actors and consumers, and the requirements (each pushed to a measurable predicate or flagged open). The interview guide carries the probes; follow them rather than improvising the questioning.

Exit Phase 1 per the exit condition in the interview guide.

## Phase 2 — Emit slice

Write one component slice, following `references/elicitation-template.md` exactly. In outline:

- H1 = the component name.
- One explicit purpose sentence directly under the H1.
- `## In scope` with bullets phrased using covers / handles / responsible for.
- `## Out of scope` with bullets naming the owning component (owned by …).
- `## Actors and consumers`, directional (upstream / downstream).
- `## Requirements` as `The system shall …` statements, one per bullet, each tagged with an inert `(R-NN)` origin reference.
- Wrap literal identifiers in backticks.

Emit nothing that belongs to the formaliser: no `FR`/`NFR`/`SEC`/`ERR` category IDs, no error entries, no glossary section, no interface wire contracts. Those are `writing-requirements`' job.

Recommend a downstream `--type`: `generic` unless the slice actually carries non-functional, security, or observability requirements, in which case `technical`.

Write the slice as `<slug>.md`. Default location `<cwd>/outputs/<slug>/<slug>.md` unless the caller names a folder. Report the path and the recommended `writing-requirements` invocation.

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
