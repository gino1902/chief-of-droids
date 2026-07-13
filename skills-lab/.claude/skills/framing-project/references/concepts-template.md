# Concepts Template

Loaded by `SKILL.md` after `FRAMING.md` is written. Seeds or updates `CONCEPTS.md`, a companion to `FRAMING.md` at the repo root that carries the project's domain language.

## What CONCEPTS.md is

`CONCEPTS.md` is the single source of the project's domain language, the ubiquitous language in domain-driven design terms. It is defined here, at framing, so downstream requirements work references it rather than reinventing terms. Language minted late and locally drifts, and two components end up naming the same thing differently, which is the classic ubiquitous-language failure. New terms surfaced downstream are recorded back here, not left in one requirements slice.

It is context-structured, not one flat glossary. Domain-driven design holds that a term is consistent within a bounded context, not necessarily across the whole system: the same word can mean different things in two contexts. So the file carries a shared core (terms with one meaning everywhere), one block per context, and a context map for the relationships between them. The contexts are the FRAMING tracks, each track being a domain of work and therefore a candidate bounded context.

## Rules for filling in

- Seed only terms already surfaced in the framing answers. Do not run a separate vocabulary interview; framing stays short. Downstream skills grow the language.
- Put a term in the shared core only if it means one thing across every context. Otherwise place it under the context that owns it.
- Use the user's own language. A definition is one line.
- Set `last_updated` to today's ISO date. Set `name` to the project name.
- On an update run, preserve existing terms and add or refine only where framing changed.

## Template

The block below is the literal file to write (minus this line and the fences). One `### context` block per track. Delete the context-map rows only if there is genuinely one context.

~~~markdown
---
name: {{project_name}} Concepts
last_updated: {{YYYY-MM-DD}}
---

# {{project_name}} — Domain language

Single source of the project's domain language. Terms are defined here so downstream work references them rather than reinventing them. New terms are recorded back here, never left in one requirements slice.

## Shared core

Terms with one meaning everywhere in the project.

| Term | Definition |
|:--|:--|
| {{term}} | {{one line}} |

## Contexts

One block per bounded context (a FRAMING track). A term may appear in more than one context with a different meaning; the context map records the relationship.

### {{Track / context name}}

| Term | Definition |
|:--|:--|
| {{term}} | {{one line}} |

## Context map

Relationships between contexts: which owns a term, which consumes it, where the same word diverges.

| From | To | Relationship |
|:--|:--|:--|
| {{context}} | {{context}} | {{owns / consumes / shared term X means … here vs … there}} |
~~~

## Post-write checklist

- [ ] Frontmatter present with `name` and `last_updated` (today, ISO).
- [ ] One context block per FRAMING track.
- [ ] Every term is either in the shared core or under exactly one context.
- [ ] Shared-core terms genuinely mean one thing across all contexts.
- [ ] Context map has a row for each cross-context relationship (owner, consumer, or divergent term).

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
