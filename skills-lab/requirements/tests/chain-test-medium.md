# Chain test — Medium+ project

Run this in a fresh Claude Code session, separate from the Small case (`chain-test-small.md`), so the two runs cannot contaminate each other and neither carries prior chain context.

## Purpose

Exercise the chain end to end for a Medium+ project: bootstrapping-project (delegating Pass 2 to framing-project) → brainstorming-requirements → writing-requirements. Confirm the Medium+ size branch behaves as designed (`CONCEPTS.md` present and context-structured, Tracks present, terms governed).

## Preconditions

- A fresh session.
- An empty project directory at `skills-lab/outputs/test-medium`. Create it before starting.
- Session cwd is that directory (same cwd caveat as the Small test: if the skills are not offered, start from `skills-lab` root and pass `outputs/test-medium` as the bootstrapping target, keeping cwd inside the test project for the writing-requirements step).

## Scripted subject — "insight-hub"

A mid-size company's governed data platform. Multiple teams and tracks, a sponsor, real budget. Deliberately a Medium+ tier project.

## Run steps

### 1. bootstrapping-project

Invoke `bootstrapping-project`. Answer as scripted:

- Goal: `code`
- Pass 2 size question: **Medium+** (this delegates framing to framing-project)
- framing-project interview:
  - Target problem: analysts in finance and operations cannot trust cross-team data; every report is reconciled by hand, so numbers disagree between teams.
  - Our approach: one governed data platform on a medallion architecture, delivered use case by use case, so teams consume trusted data without reconciling it.
  - Who it's for — customer: analysts in finance and operations assembling cross-team reports. Business: the Head of Data sponsors it; the owned outcome is cutting manual reconciliation.
  - What success means — customer: an analyst pulls a cross-team report without hand-reconciliation. Business: reconciliation hours cut by half within two quarters.
  - Tracks: Ingestion and transformation; Governance and platform; Exposition and reporting.
  - Not working on: source-system changes, owned by the app teams.
- Let framing-project write `FRAMING.md` and seed `CONCEPTS.md`; bootstrapping then injects the `<!-- goal: code -->` stamp after the frontmatter.
- Pass 3 sub-type: `data`.
- Approve the tree and the CLAUDE.md.

### 2. brainstorming-requirements

Invoke `brainstorming-requirements from FRAMING.md --target "ingestion pipeline"`. It should read `CONCEPTS.md` in Phase 0 and draw terms from it. Answer the interview as scripted:

- Purpose: the ingestion pipeline reads source deliveries into the bronze layer and transforms them through silver to gold, so the business gets trusted enterprise data.
- Scope: covers reading landing-zone deliveries into bronze, the bronze-to-silver and silver-to-gold transformations, and gating publication to gold on quality rules. Out of scope: populating the landing zone (owned by the source app teams); governance and the catalog (owned by the Governance and platform track); exposing gold (owned by the Exposition and reporting track).
- Actors and consumers: upstream, the landing zone. Downstream, the Exposition and reporting track consumes gold. Operator, the platform team.
- Requirements: elicit three to five in the actor / action / result / conditions contract, using the terms defined in `CONCEPTS.md` (backticked or defined so they reach the glossary). For any new term, record it back to `CONCEPTS.md`.

Let it emit one component slice.

### 3. writing-requirements

Invoke `writing-requirements ingestion-pipeline from <slice-path> --type generic`.

## Expected outputs (under `outputs/test-medium`)

- `.claude/settings.json`, `.gitignore`
- `FRAMING.md` — framing-project shape: YAML frontmatter with `last_updated`, two to four Tracks, and the injected `<!-- goal: code -->` stamp after the frontmatter
- `CONCEPTS.md` — context-structured: a shared core, one context block per Track, a context map
- a data-bundle tree anchor
- `CLAUDE.md`, grounded
- one component slice `.md`, with domain terms drawn from `CONCEPTS.md`
- `requirements/ingestion-pipeline/ingestion-pipeline-requirements.md` and `ingestion-pipeline-report.md`

## Acceptance criteria

- All the above exist; `CONCEPTS.md` is present and context-structured; the slice's domain terms trace back to `CONCEPTS.md`.
- The requirements report extracts clean: no undefined-term warnings, no shape-defect warnings. A §Constraints N/A is acceptable.

Medium+ signatures that must be present: FRAMING has `last_updated` frontmatter and a Tracks section; a context-structured `CONCEPTS.md` exists; the slice's terms are sourced from it.

## Fail conditions

- `CONCEPTS.md` is missing, or FRAMING has no Tracks (the Medium+ branch did not fire).
- The report shows undefined-term warnings for terms that are defined in `CONCEPTS.md` (the term-drawing discipline did not hold).
- Any shape-defect warning (scope not extracted, requirements not SHALL/EARS, title fallback fired).
- bootstrapping wrote into `skills-lab` root rather than `outputs/test-medium`.

## Record

Copy the report's `Outstanding: N blocking, M warnings, K info` line, and classify each warning. Compare against the Small run: the expected difference is that Medium+ carries a governed `CONCEPTS.md` and Tracks, and its report has no undefined-term warnings.

## Note

Multi-component fan-out is deferred, so this test runs a single component (the ingestion pipeline). The Tracks in `FRAMING.md` name the other candidate components, but the test does not fan out over them.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
