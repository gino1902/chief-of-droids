# Chain test — Small project

Run this in a fresh Claude Code session, with no other chain context loaded, so the run cannot infer from prior work. This is the Small case of the two-case test (see `chain-test-medium.md` for the other, run in a separate session).

## Purpose

Exercise the chain end to end for a Small project: bootstrapping-project → brainstorming-requirements → writing-requirements. Confirm the Small size branch behaves as designed (no `CONCEPTS.md`, no Tracks, single component).

## Preconditions

- A fresh session.
- An empty project directory at `skills-lab/outputs/test-small`. Create it before starting.
- Session cwd is that directory, so bootstrapping targets it and writing-requirements resolves its repo root there. If the four skills (bootstrapping-project, framing-project, brainstorming-requirements, writing-requirements) are not offered, start from the `skills-lab` root instead and pass `outputs/test-small` as the bootstrapping target path, then keep cwd inside the test project for the writing-requirements step.

## Scripted subject — "linkjar"

A solo developer's personal URL shortener. One small backend service, one workflow, no sponsor. This is deliberately a Small-tier project.

## Run steps

### 1. bootstrapping-project

Invoke `bootstrapping-project`. Answer as scripted:

- Goal: `code`
- Pass 2 size question: **Small**
- Five framing questions (Small inline path):
  - Why: I keep losing track of long links I share, and I want short, memorable links I control.
  - For whom: myself, a solo developer.
  - Success: I can create a short link and resolve it, and I use it daily for a month.
  - Delivered: a small REST API — create a link, resolve a link — with a datastore.
  - Constraints: a single SQLite datastore, no authentication, one service.
- Pass 3 sub-type: `app`, backend only.
- Approve the proposed tree and the CLAUDE.md.

### 2. brainstorming-requirements

Invoke `brainstorming-requirements from FRAMING.md --target "link service"`. Note `CONCEPTS.md` will be absent — expected. Answer the interview as scripted:

- Purpose: the link service creates short codes for target URLs and resolves them back.
- Scope: covers creating a short code for a target URL, and resolving a code to its target. Out of scope: click analytics (owned by nothing yet, deferred); authentication (none in this project).
- Actors and consumers: upstream, the solo user over HTTP. Downstream, the SQLite datastore.
- Requirements (actor / action / result / conditions):
  - The service shall create a short code for a submitted target URL, so that the user gets a shareable link, when the URL is well-formed.
  - The service shall resolve a short code to its target URL, so that the user reaches the destination, when the code exists.
  - The service shall return a not-found response, so that the user learns the link is invalid, when the code does not exist.

Let it emit one component slice.

### 3. writing-requirements

Invoke `writing-requirements link-service from <slice-path> --type generic`, using the slice path just produced.

## Expected outputs (under `outputs/test-small`)

- `.claude/settings.json`, `.gitignore`
- `FRAMING.md` — Small shape: `<!-- goal: code -->` on line 1, the five sections, no `last_updated` frontmatter, no version footer
- no `CONCEPTS.md`
- a minimal app-backend tree (for example `apps/<domain>/` with the three tiers), deferred directories left out
- `CONVENTIONS.md` — the app structural contract (dependency, import, promotion rules) with a machine-readable enforcement stanza (`config`, `runner`, `zoned: apps/* src/features/*`), plus the generated lint config and gate for the confirmed stack
- `CLAUDE.md`, grounded, under ~60 lines, pointing at `CONVENTIONS.md` rather than restating the structural rules
- one component slice `.md`
- `requirements/link-service/link-service-requirements.md` and `link-service-report.md`

## Acceptance criteria

- All the above exist; `CONCEPTS.md` is absent; only one component is produced (no fan-out).
- `CONVENTIONS.md` exists and passes the drift-check: `check-conventions-drift.sh outputs/test-small` returns 0 (config present, runner wired, coverage green — per-domain zones only for domains that exist).
- The structural rules live in `CONVENTIONS.md`, not restated in `CLAUDE.md`; `CLAUDE.md` carries the two appended pointer lines.
- The requirements report shows no shape-defect warnings: Title, Scope, Actors extracted; requirements are SHALL/EARS; each has a derivable acceptance criterion.
- Auto-derived glossary "verify" warnings and a §Constraints N/A are acceptable.

Small signatures that must be present: FRAMING has no `last_updated` frontmatter, no `CONCEPTS.md`, no Tracks section, a single component.

## Fail conditions

- A `CONCEPTS.md` was produced (the size branch leaked).
- `CONVENTIONS.md` is missing, or the structural rules were written into `CLAUDE.md` instead.
- writing-requirements raised shape-defect warnings (scope not extracted, requirements not SHALL/EARS, title fallback fired).
- bootstrapping wrote into `skills-lab` root rather than `outputs/test-small`.

## Record

Copy the report's `Outstanding: N blocking, M warnings, K info` line, and classify each warning as shape-defect (fail) or content-gap / verify (acceptable).

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
