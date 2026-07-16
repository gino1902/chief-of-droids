# Technical formalisation test — MD-6

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this in a fresh session. It diversifies project type: this is the code/app Medium+ scenario, and it is the only one that drives the full technical formaliser.

## Purpose

Exercise the `--type technical` skeleton of `writing-requirements`, which the two straight tests never touched (both were generic). A slice carrying non-functional, security, and observability requirements should produce the S2 sections (Constraints as `CON`, Interface, Data, Transformation, `NFR`, `SEC`, `ERR`, `OBS`), draw the paired `ERR` entries from the FR contract shapes, and score Bounded on the NFR-class requirements. It runs on a code/app Medium+ base so the domain naturally carries auth, latency, and metrics.

## Directory and precedence

Directory: `outputs/test-app`, created by this test (self-contained mini-chain: bootstrap, then brainstorm, then formalise).

Precedence: none against the Medium data base. Sequence it after the iteration ladder if the goal is still iteration coverage; promote it earlier only if the goal switches to formaliser coverage.

## Preconditions

- A fresh session.
- The directory `skills-lab/outputs/test-app` exists and is empty. Session cwd is that directory.

## Scripted subject — "helpdesk"

A Medium+ support-ticket service. Multiple teams, a sponsor. Goal `code`, sub-type app. Tracks: Ticketing; Identity and access; Platform and observability.

## Run steps

### 1. bootstrapping-project (Medium+, code/app)

Invoke `bootstrapping-project`. Goal `code`, Pass 2 size Medium+ (delegates to framing-project), sub-type app. Frame helpdesk with the three Tracks above, and let framing-project seed `CONCEPTS.md`. Approve the app tree and CLAUDE.md.

### 2. brainstorming-requirements (a technical component)

Invoke `brainstorming-requirements from FRAMING.md --target "ticket API"`, a component of the Ticketing track. Draw terms from `CONCEPTS.md` and settle new ones back. Elicit a slice that deliberately carries all the technical flavours, so the formaliser has signal in every S2 section:

- Functional: create a `ticket`; fetch a `ticket` by id.
- A static invariant (feeds `CON`): a `ticket` id, once assigned, never changes.
- Non-functional (feeds `NFR`): fetch returns within 300 ms at the 95th percentile.
- Security (feeds `SEC`): only the `agent` assigned to a `ticket` may read it.
- Observability (feeds `OBS`): every create emits a `ticket.created` metric.

Because the slice carries non-functional, security, and observability requirements, brainstorming should recommend `--type technical`. Emit the slice at `outputs/ticket-api/ticket-api.md`.

### 3. writing-requirements (technical)

Invoke `writing-requirements ticket-api from outputs/ticket-api/ticket-api.md --type technical`.

## Expected outputs (under `outputs/test-app`)

- the Medium+ app project (FRAMING with Tracks, CONCEPTS, app tree, CLAUDE.md).
- `CONVENTIONS.md` — the app structural contract with an enforcement stanza (`config` the ESLint config, `runner` the lint command, `zoned: apps/* src/features/*`), plus the generated ESLint `import/no-restricted-paths` config and gate. This is the only scenario that meaningfully exercises zone coverage, since the app tree scaffolds one `apps/<domain>/` per business domain.
- the `ticket-api` slice.
- `requirements/ticket-api/ticket-api-requirements.md` and `-report.md`, on the S2 template.

## Acceptance criteria

- Every S2 section that has substrate signal renders as content, not `N/A`: `FR`, `CON` (the id invariant), `NFR` (the latency threshold), `SEC` (the read-authorisation rule), `OBS` (the created metric). Sections with no signal (for example `IR`, `DR`, `TR`) may render `N/A` with a Warning, which is acceptable.
- ERR coverage: each FR of Acquire, Mutate, or Validate shape (create, fetch) has a paired `ERR` entry drawn in the same pass, or an inline opt-out rationale.
- Bounded scores ✓ on the `NFR` latency requirement (the 300 ms threshold). The `SEC` (read-authorisation) and `OBS` (metric emission) requirements as scripted carry no quantitative threshold, so Bounded scores ✗ and each emits a Bounded Warning. That is correct scoring, not a defect. If you want Bounded ✓ across all three, give the `SEC` and `OBS` requirements numeric thresholds in the slice.
- `CONVENTIONS.md` exists and passes the drift-check: `check-conventions-drift.sh outputs/test-app` returns 0. Every scaffolded `apps/<domain>/` has a matching `import/no-restricted-paths` zone in the ESLint config (coverage), and the runner is wired into the project gate. A scaffolded domain with no zone is a coverage failure — that is the feature working.
- The structural rules live in `CONVENTIONS.md`, not restated in `CLAUDE.md`; the ESLint config and gate are stack files, so `settings.json` stays byte-identical.
- No undefined-term warnings, since `CONCEPTS.md` governs the vocabulary.
- The report Summary reconciles with the body: the Info Resolved cell equals the count of `[INFO]` lines, and the Warning and Blocking Resolved and Unresolved cells equal their `[<SEVERITY>-RESOLVED]` and `[<SEVERITY>-UNRESOLVED]` line counts. Run 2 found the Info count undercounting here; the standalone check is `verify-summary-info-tally.md`.

## Fail conditions

- `CONVENTIONS.md` is missing, a scaffolded `apps/<domain>/` has no zone in the ESLint config (coverage gap), or the structural rules were written into `CLAUDE.md` instead.
- A technical section collapses to `N/A` despite the slice carrying that flavour of requirement (signal lost).
- An Acquire/Mutate/Validate FR has neither a paired `ERR` nor an opt-out rationale (Phase 4 warning).
- The NFR renders unbounded (Bounded ✗) when the slice gave a 300 ms threshold.
- Any undefined-term warning, or a shape-defect warning (scope not extracted, a non-EARS requirement, or a title fallback). Bounded ✗ warnings on the non-quantitative `SEC` and `OBS` requirements are expected and are not failures.
- Any Summary count disagrees with the body tagged-line count, for example the Info Resolved cell differs from the number of `[INFO]` lines.

## Record

Copy the report's Summary and the `Outstanding` line, and confirm each S2 section's disposition (content versus `N/A`). Note the ERR pairs drawn and any opt-out rationale. Expect the auto-derived glossary entries to appear as `WARNING-UNRESOLVED` (verification-pending) on the `Outstanding` line. That is normal after the resolution-model fix in `conventions.md`, not a failure.

## Note

This is the highest pure-coverage scenario. It sits below the iteration ladder because it proves formaliser breadth, not iteration behaviour. It also exercises the code/app bootstrapping tree, which no other scenario does.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.2        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
