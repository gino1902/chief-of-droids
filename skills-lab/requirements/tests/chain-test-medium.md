# Chain test — Medium+ project

Run this in a fresh Claude Code session, separate from the Small case (`chain-test-small.md`), so the two runs cannot contaminate each other and neither carries prior chain context.

## Purpose

Exercise the chain end to end for a Medium+ project: bootstrapping-project (delegating Pass 2 to framing-project) → brainstorming-requirements → writing-requirements. Confirm the Medium+ size branch behaves as designed (`CONCEPTS.md` present and context-structured, Tracks present, terms governed).

## Preconditions

- A fresh session.
- An empty project directory at `skills-lab/testing/test-medium`. Create it before starting.
- Session cwd is that directory (same cwd caveat as the Small test: if the skills are not offered, start from `skills-lab` root and pass `testing/test-medium` as the bootstrapping target, keeping cwd inside the test project for the writing-requirements step).

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
- Requirements: elicit the requirements the scope implies, in the actor / action / result / conditions contract, using the terms defined in `CONCEPTS.md` (backticked or defined so they reach the glossary). For any new term, record it back to `CONCEPTS.md`. The current canonical base carries five (FR-001 to FR-005, the last being the IF/THEN quality-rule withholding requirement); record the resulting FR list as the base reference (see Record) rather than treating any count as fixed in advance.

Let it emit one component slice.

### 3. writing-requirements

Invoke `writing-requirements ingestion-pipeline from <slice-path> --type generic`.

## Expected outputs (under `testing/test-medium`)

- `.claude/settings.json`, `.gitignore`
- `FRAMING.md` — framing-project shape: YAML frontmatter with `last_updated`, two to four Tracks, and the injected `<!-- goal: code -->` stamp after the frontmatter
- `CONCEPTS.md` — context-structured: a shared core, one context block per Track, a context map
- a data-bundle tree anchor
- `CONVENTIONS.md` — the data structural contract (dependency, thin-notebook, promotion rules) with a machine-readable enforcement stanza (`config` the ruff config, `runner` the lint command, `zoned: none` — ruff is file-level, not zone-level), plus the generated lint config for the confirmed stack
- `CLAUDE.md`, grounded, pointing at `CONVENTIONS.md` rather than restating the structural rules
- one component slice `.md`, with domain terms drawn from `CONCEPTS.md`
- `requirements/ingestion-pipeline/ingestion-pipeline-requirements.md` and `ingestion-pipeline-report.md`

## Acceptance criteria

- All the above exist; `CONCEPTS.md` is present and context-structured; the slice's domain terms trace back to `CONCEPTS.md`.
- `CONVENTIONS.md` exists and passes the drift-check: `check-conventions-drift.sh testing/test-medium` returns 0 (`zoned: none`, so existence runs and coverage is skipped). The structural rules are in `CONVENTIONS.md`, not restated in `CLAUDE.md`.
- The requirements report extracts clean: no undefined-term warnings, no shape-defect warnings. A §Constraints N/A is acceptable.

Medium+ signatures that must be present: FRAMING has `last_updated` frontmatter and a Tracks section; a context-structured `CONCEPTS.md` exists; the slice's terms are sourced from it.

## Fail conditions

- `CONCEPTS.md` is missing, or FRAMING has no Tracks (the Medium+ branch did not fire).
- `CONVENTIONS.md` is missing, or the structural rules were written into `CLAUDE.md` instead.
- The report shows undefined-term warnings for terms that are defined in `CONCEPTS.md` (the term-drawing discipline did not hold).
- Any shape-defect warning (scope not extracted, requirements not SHALL/EARS, title fallback fired).
- bootstrapping wrote into `skills-lab` root rather than `testing/test-medium`.

## Record

Copy the report's `Outstanding: N blocking, M warnings, K info` line, and classify each warning. Compare against the Small run: the expected difference is that Medium+ carries a governed `CONCEPTS.md` and Tracks, and its report has no undefined-term warnings.

Record the base FR list: the IDs and a one-line summary of each functional requirement this run produced. This is the canonical base every MD-* row reads, so downstream assertions reference these IDs and this count, never a number hard-coded in the downstream test. Commit the base in `test-medium`'s own repo before running any MD-* row (its HEAD becomes the diff reference `<base-commit>`), per `test-strategy.md` §Retrospective use, so each MD row resets to it and an off-by-one in a downstream count surfaces as a diff against a fixed reference rather than silent drift. `CONVENTIONS.md` and its generated lint config are part of this committed base; the diff-confined MD rows leave them untouched, so they must stay absent from those rows' diffs, and MD-5's reconcile leaves them unchanged.

## Note

Multi-component fan-out is deferred, so this test runs a single component (the ingestion pipeline). The Tracks in `FRAMING.md` name the other candidate components, but the test does not fan out over them.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.3        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
