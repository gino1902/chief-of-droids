---
date: 2026-04-19
topic: persona-reference-library
---

# Persona Reference Library

## Problem Frame

A reference library of structurally-identical executive personas is needed to benchmark sales materials across many engagements. No personas exist; no spec governs their construction. Ad-hoc authoring would drift across entries and destroy the library's value as a comparable reference set.

## Requirements

**Library scope and lifecycle**
- R1. The library starts with 5 personas: `cmo`, `cio`, `cdo`, `cco-customer`, `cco-commercial`. Additions are occasional (1-2 over time), not continuous.
- R2. Each persona is built one-at-a-time as a discrete task against the canonical spec, never in batch.
- R3. The spec itself is the durable, versioned, reusable artifact. No skill is authored.

**Library layout**
- R4. The library lives at `shared/personas/` and contains: `README.md` (overview + library roster), `SPEC.md` (canonical persona spec), `coverage-map.md` (persona x AI-themes matrix), and one `<role-key>.md` per persona.
- R5. The library roster in `README.md` records each persona's filename, role key, version, and build date.

**Persona file structure - dual consumed (human + Claude)**
- R6. Each persona file is structured markdown with anchored headers and tables - human-readable, parseable by Claude without special tooling.
- R7. Each persona file contains, in this order: (1) EU specific topics, (2) 7 core dimensions, (3) 6 AI-theme blocks, (4) 4 role-tailored probes, (5) build metadata (date + sources actually used).
- R8. Each persona file carries its own version block per workspace convention.

**Persona content - EU specific topics**
- R9. Each persona opens with a standalone section titled `EU Specific Topics`, placed before any dimension content. The section contains one statement per topic — exactly four topics, in this order: GDPR, works councils, data sovereignty, legacy ecosystems. Each statement expresses how the role reads the topic (concern, constraint, opportunity) in one or two sentences.

**Persona content - dimensions**
- R10. Each persona defines 7 dimensions with fixed cardinality: Core objective (1), KPIs (4), Triggers (4), Pain points (4), Buying role (1 primary + 1 optional secondary), Objections (4), Language (3 keywords).
- R11. Dimensions are consistent with the role matrix (Primary Responsibilities, Decision Rights, KPIs anchor, Exclusion Rules). The role matrix is normative; cross-role contamination is forbidden.
- R12. Each dimension is supported by >=1 source from the source catalog at construction time. Block-level support suffices. The output carries no inline citations; on challenge, the LLM must name the sources used for any dimension (traceability semantics).
- R13. Semantic constraints: KPIs quantifiable; triggers externally-observable events (the event that produces buying intent, not the intent itself); pain points each mapped to one of {org, tech, data, process}; objections decision-blocking.
- R14. Lexical constraints: no duplicates or synonyms within a list; no cross-role contamination; vocabulary matches role register.

**Persona content - AI themes**
- R15. Each persona explicitly addresses all 6 AI themes, restated per role (theme framing adapts to the persona; not uniform across roles).
- R16. Each AI-theme block contains exactly 4 fields: Value (<=15 words, tied to >=1 KPI), Trigger (observable event), Objection (role-consistent risk), Source (exactly 1, no reuse across themes preferred). Total: 6 x 4 = 24 normalized elements per persona.

**Persona content - probes (stress-test)**
- R17. Each persona ends with a Probes section: exactly 4 role-tailored probes. Each probe = one observable sales-material move -> expected persona reaction, drawn from {objection raised, trigger fires, unblocks consideration, neutral}.
- R18. Probes are drawn from real, named sales-material patterns - not abstract scenarios - to avoid encoding bias.

**Construction**
- R19. The LLM consumes the full source catalog at construction time. The catalog is evidentiary input, not a per-item citation requirement.
- R20. When a catalog source fails to fetch, the LLM proceeds and annotates the persona with `> WARNING Unverified - source X unreachable`.

**Drift handling**
- R21. Each persona stamps its build date and a short list of sources actually used. Staleness is eyeballed; refresh is fully discretionary. No catalog versioning.

**Coverage map**
- R22. `coverage-map.md` is an N x 6 matrix of persona x AI themes with per-cell role-framing summary. Regenerated on every persona add or refresh.

## Success Criteria
- Two persona files chosen at random show identical structure: same headers, same dimension count, same field count per theme block, same probe count.
- Re-building an existing persona from scratch against the spec produces an entry with the same shape (not necessarily identical content).
- Reading any persona file, the role-specific objections, KPIs, and language register are immediately recognisable as belonging to that role and no other.
- Loading a persona file into Claude's context for a downstream benchmark workflow requires no preprocessing or special parsing.

## Scope Boundaries
- Benchmarking protocol is explicitly out of scope. The persona is input; scoring sales material against it is a separate workstream.
- No skill is authored - the spec is the reusable artifact, not a workflow.
- No batch generation - each persona is built individually.
- No catalog versioning, no automated drift detection.
- No inline citations on dimensions - traceability is on-challenge only.

## Key Decisions
- Real deliverable: reference library, not benchmarking workflow. Personas are the durable asset.
- Lifecycle: core set + occasional additions (5-7 total). Skill ceremony unjustified at this volume.
- Dual consumer (human + Claude) drives structured-markdown format with anchored headers and tables.
- Source-support contract: AC3 = traceability semantics (no inline citations); AC9 = inline source field on theme blocks only; fetch-fail = flag-and-proceed.
- AC7 reframed and resolved as 4 role-tailored probes per persona - the stress-test becomes useful reference content rather than an abstract self-coherence check.
- `<files>` = role matrix (normative input), distinct from the source catalog (construction-time evidentiary input).
- Drift handling = stamp-and-eyeball. No catalog versioning.
- Per-persona version block + library-wide roster in README.
- Priority-topics block is renamed "EU Specific Topics" and rendered as a standalone section (option 1 of three shapes considered) placed before any dimension content.

## Dependencies / Assumptions
- The role matrix at the top of the source plan is treated as normative and stable. Changes invalidate the library.
- The source catalog is reachable enough - fetch failures are tolerated per R20, but the spec assumes a meaningful majority is accessible.
- The 6 AI themes are stable at build time. Theme additions or renames cascade to all personas (per R15) and require a coverage-map regen.

## Outstanding Questions

### Resolve Before Planning
*(none)*

### Deferred to Planning
- [Affects R4][Operational] Where exactly does the polished `SPEC.md` get authored - directly into `shared/personas/`, or first as a draft elsewhere then moved?
- [Affects R6][Technical] Final persona-file template (header anchors, table layouts) - to be designed at execution time.
- [Affects R18][Needs research] Source for the "real, named sales-material patterns" used to seed probes - your own decks, public B2B material, or both - to be sourced when the first persona is built.
- [Affects R22][Technical] Coverage map representation - flat table, expandable per cell, or one-table-per-theme - decide at first build.

## Next Steps
Continue in this conversation to outline an implementation plan.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.2        |
| Last Updated | 2026-04-19 |
| Status       | Draft      |
