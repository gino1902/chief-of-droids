---
name: writing-requirements
description: Produces a structured requirements artifact and diagnostic report for one deployable component from a markdown substrate. Output files are written to `<CLAUDE.md parent dir>/requirements/<slug>/` and named `<slug>-requirements.md` and `<slug>-report.md`. Invoke as `writing-requirements <slug> from <path> --type generic|technical` — slug must not contain "requirement", "req", or "reqs". Use --type generic for lightweight functional requirements: skill definitions, file format specs, pre-design tech objects, migration requirements. Use --type technical for full requirements covering functional, interface, data, non-functional, security, error handling, and observability. Iterates statelessly: feed prior `<slug>-requirements.md` as substrate to refine.
allowed-tools:
  - Read
  - Write
---

<!-- target-model: claude-opus-4-7 -->

# writing-requirements

Produces two output files for one deployable component (container, service, module-as-container, app):

- `<slug>-requirements.md` — structured requirements artifact
- `<slug>-report.md` — per-phase diagnostic report

Seven phases run sequentially in memory. No writes until Phase 6 completes. Reason: per-phase intermediate state is not shaped like the final output (e.g. Phase 1 produces only Title + Scope + Actors; Phase 2 adds requirement sections); writing per-phase would leave truncated requirements and report files on disk that downstream consumers could not distinguish from a completed run.

<reference-files>

| File | Load at | Condition |
|:--|:--|:--|
| `references/conventions.md` | Phase 0 | Always |
| `references/template-s1.md` | Phase 0 | `--type generic` |
| `references/template-s2.md` | Phase 0 | `--type technical` |
| `references/ears.md` | Phase 1 | Always — both types include T1 sections |
| `references/rfc2119.md` | Phase 1 | `--type technical` only |
| `references/tables.md` | Phase 1 | `--type technical` only |
| `references/verification.md` | Phase 5 | Always |

</reference-files>

<invocation>

```
writing-requirements <topic-slug> from <path> --type generic|technical
```

`<topic-slug>` is always the first token after the skill name, before the keyword `from`. It is user-supplied and entirely independent of the input filename — do not derive it from the input path.

| Argument | Rule | On failure |
|:--|:--|:--|
| `<topic-slug>` | First token before `from`; matches `^[a-z0-9-]+$`; must not contain `requirement`, `req`, or `reqs` | Hard-fail |
| `from` | Literal keyword separator; exactly one occurrence | Hard-fail if absent or duplicated |
| `<path>` | Token immediately after `from`; absolute or cwd-relative; quote if whitespace | Hard-fail if not found |
| `--type` | `generic` or `technical`; required | Hard-fail if absent or unrecognized |
| Substrate | Must be `.md` extension | Hard-fail |

**Invocation examples**

Correct:
  writing-requirements chief-of-droids-3-tiers-upgrade-v05 from substrate.md --type technical
  → slug=chief-of-droids-3-tiers-upgrade-v05, path=substrate.md, type=technical

Correct:
  writing-requirements user-auth-flow from /abs/path/spec.md --type generic
  → slug=user-auth-flow, path=/abs/path/spec.md, type=generic

Incorrect — slug contains reserved token:
  writing-requirements payment-requirements from spec.md --type technical
  → Hard-fail Phase 0.2: slug contains "requirements"

Incorrect — missing --type:
  writing-requirements user-auth from spec.md
  → Hard-fail Phase 0.3: --type absent

Incorrect — duplicate `from`:
  writing-requirements user-auth from spec.md from extra.md --type generic
  → Hard-fail Phase 0.1: keyword `from` appears more than once

</invocation>

<phase-model>

| Phase | Name | Content produced |
|:--|:--|:--|
| 0 | Pre-flight | (validation only) |
| 1 | Framing | §Title+Purpose · §Scope · §Actors |
| 2 | Drafting | Requirement sections per active template |
| 3 | Vocabulary | §Glossary |
| 4 | Taxonomy hygiene | (validation only) |
| 5 | Verification | §Acceptance Criteria · §Quality scorecard |
| 6 | Format + write | §Version block · both files written |

Stream one header line per phase as it begins:

```
→ Phase 0 — Pre-flight
→ Phase 1 — Framing
→ Phase 2 — Drafting
→ Phase 3 — Vocabulary
→ Phase 4 — Taxonomy hygiene
→ Phase 5 — Verification
→ Phase 6 — Format
✓ Wrote <slug>-requirements.md (v0.2)
✓ Wrote <slug>-report.md (v0.2)
```

On hard-fail, replace the current phase line and stop:

```
✗ Phase <N> — <phase name>: <reason>
  context: <relevant path or arg>
  remediation: <one-line suggestion>
```

**Hard-fail examples**

Phase 0.2 (invalid slug):
  ✗ Phase 0 — Pre-flight: slug "user_auth" does not match ^[a-z0-9-]+$
    context: arg #1
    remediation: replace underscores with hyphens; use lowercase only

Phase 0.4 (substrate not found):
  ✗ Phase 0 — Pre-flight: substrate path not found
    context: ./missing.md
    remediation: check path; substrate must exist before invocation

Phase 0.10 (template unreadable):
  ✗ Phase 0 — Pre-flight: references/template-s2.md unreadable
    context: --type technical
    remediation: verify skill installation

Phase 6 (write permission):
  ✗ Phase 6 — Format: cannot write to requirements/user-auth/
    context: <repo root>/requirements/user-auth/
    remediation: check directory permissions on repo root

</phase-model>

<phase-0-preflight>

## Phase 0 — Pre-flight

| Step | Action | On failure |
|:--|:--|:--|
| 0.1 | Parse args; detect slug, path, `--type`; flag ambiguity | Hard-fail |
| 0.2 | Validate slug against `^[a-z0-9-]+$` | Hard-fail |
| 0.3 | Validate `--type` is `generic` or `technical` | Hard-fail |
| 0.4 | Resolve input path; existence check | Hard-fail |
| 0.5 | Check cwd for `CLAUDE.md` first; if absent, walk upward to filesystem root directory by directory; the parent directory of the first `CLAUDE.md` found is the repo root | Hard-fail if none found |
| 0.6 | Resolve output dir `<repo root>/requirements/<slug>/`; create if absent | Hard-fail on permission error |
| 0.7 | Read prior `<slug>-requirements.md` if present (ID stability + version increment) | Warning if unreadable; treat as no-prior |
| 0.8 | Read substrate file; reject non-`.md` extension | Hard-fail |
| 0.9 | Read `references/conventions.md` | Hard-fail if unreadable |
| 0.10 | Read `references/template-s1.md` or `references/template-s2.md` per `--type` | Hard-fail if unreadable |

</phase-0-preflight>

<phase-1-framing>

## Phase 1 — Framing

Read typology reference files per the table above, then produce:

**§ Title + Purpose**
Title: first H1 in substrate; fallback: first H2; fallback: frontmatter `title:`; fallback: slug + Warning.

The slug fallback is permitted only when all three earlier fallbacks fail (no H1, no H2, no frontmatter `title:`). If the slug fallback fires, emit Warning in the report identifying the substrate as mis-shaped. Never humanise the slug — emit it verbatim (e.g. for slug `chief-of-droids-3-tiers-upgrade-v01`, the Title is exactly `chief-of-droids-3-tiers-upgrade-v01`, not `Chief-of-Droids 3-Tier Architecture Upgrade`). The Warning carries the signal that a human-readable title is missing from the substrate; do not synthesize one.

**Title fallback examples**

H1 present → use H1:
  substrate: `# User Authentication Flow\n...`
  Title: User Authentication Flow

No H1, H2 present → use H2:
  substrate: `## Component overview\n...`
  Title: Component overview

No H1, no H2, frontmatter title present → use frontmatter:
  substrate: `---\ntitle: Payment Gateway\n---\n...`
  Title: Payment Gateway

No H1, no H2, no frontmatter title → slug verbatim + Warning:
  slug: chief-of-droids-3-tiers-upgrade-v01
  substrate: prose only, no heading, no frontmatter
  Title: chief-of-droids-3-tiers-upgrade-v01
  Report: Warning — substrate has no H1/H2/frontmatter title; slug used verbatim.

Purpose: extract explicit purpose statement ("The purpose of…", "This component…", "This skill…"); if absent, infer from leading prose + Warning.

**§ Scope**
In Scope: extract from positive language — "in scope", "covers", "handles", "responsible for".
Out of Scope: extract from negation — "not handled", "outside this", "downstream", "upstream", "out of scope", "owned by".
Each subsection: `N/A` + Warning if signal absent. No synthesis when signal is absent.

**§ Actors & Consumers**
Extract upstream/downstream systems and human roles. `N/A` + Warning if absent.

</phase-1-framing>

<phase-2-drafting>

## Phase 2 — Drafting

Follow drafting rules in loaded typology reference files. All sections always render; `N/A` + Warning if substrate signal is absent for a section.

**ID stability:** scan substrate for declared IDs matching `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b`. Preserve matched IDs, attaching each to the nearest requirement-shaped block. Undeclared requirements get the next available sequence number per category, assigned per the canonical ordering rule in `references/conventions.md` § "Canonical ordering for un-IDed substrate".

**ID stability examples**

Declared IDs preserved:
  substrate: FR-001 ..., FR-007 ..., ERR-002 ...
  output: FR-001, FR-007, ERR-002 preserved; missing FR-002..FR-006 surfaced as Phase 4 Warning.

Undeclared requirement gets next available ID:
  substrate: FR-001 ..., (un-IDed paragraph for a second requirement)
  output: FR-001 preserved; second requirement assigned FR-002 per canonical ordering.

Mixed categories:
  substrate: FR-001 ..., NFR-001 ..., (un-IDed CON-shaped paragraph), ERR-003 ...
  output: FR-001 preserved; NFR-001 preserved; CON-001 assigned; ERR-003 preserved (ERR-001..ERR-002 absent → Phase 4 Warning).

Cross-version stability:
  prior <slug>-requirements.md: FR-001, FR-002, FR-003.
  current substrate: FR-001 (unchanged), FR-003 (modified), one new un-IDed requirement.
  output: FR-001 unchanged, FR-003 updated, new requirement → FR-002 only if FR-002 is unused in prior; else next available (FR-004).

**ERR coverage protocol (`--type technical` only):** for each FR drafted, classify the SHALL-action verb against the contract-shape matrix in `references/ears.md` § "Contract-shape coverage matrix". If the shape is Acquire / Mutate / Validate / Solicit / Transform-with-external-inputs, draft the paired ERR-NNN entry in the same Phase 2 pass. Do not defer to Phase 4 — Phase 4 only audits coverage, it does not draft. If an FR of mandatory-coverage shape is intentionally not paired with an ERR, attach an inline rationale to the FR entry: `(no ERR — rationale: <reason>)`. The rationale is the explicit opt-out; absent rationale + absent ERR is a Phase 4 Warning.

**ERR opt-out rationale example**

FR-008 The system shall validate that the input slug matches `^[a-z0-9-]+$`. (no ERR — rationale: Phase 0.2 hard-fail covers the invalid-slug surface; user does not reach the FR layer with a non-conforming slug)

</phase-2-drafting>

<phase-3-vocabulary>

## Phase 3 — Vocabulary

Auto-extract glossary candidates by running the following mechanical rules in order against the substrate. Each rule produces zero or more candidates; the union forms the glossary candidate set.

1. **Acronym rule** — every all-caps token of 2+ letters appearing in any requirement statement (e.g. `SHA`, `MCP`, `URI`).
2. **Backtick rule** — every term wrapped in backticks in any requirement statement (e.g. `recent_chats[0].uri`, `chief-of-droids/CLAUDE.md`).
3. **Capitalized noun phrase rule** — every capitalized multi-word noun phrase appearing in any requirement statement that is not a proper name and not a section heading reference (e.g. Project Instructions, Bootstrap Protocol, Resolved Skills Map).
4. **Explicit substrate definition rule** — every term explicitly defined in the substrate via `"X is defined as"`, `"X refers to"`, or `"X: <definition>"` patterns.

Entries from rules 1–3 are emitted with status `auto-derived — verify`. Entries from rule 4 are emitted with status `substrate`.

**Glossary extraction example**

Sample paragraph from substrate:
  "The Bootstrap Protocol reads `recent_chats[0].uri` via the MCP server (HTTP transport) and resolves it against the Resolved Skills Map."

Rules firing:
  Rule 1 (Acronym) → MCP, HTTP
  Rule 2 (Backtick) → recent_chats[0].uri
  Rule 3 (Capitalized noun phrase) → Bootstrap Protocol, Resolved Skills Map
  Rule 4 (Explicit substrate definition) → (none in this paragraph)

Stop-word filter applied:
  HTTP → dropped (in stop-word list)

Resulting glossary entries:
  MCP — auto-derived — verify
  recent_chats[0].uri — auto-derived — verify
  Bootstrap Protocol — auto-derived — verify
  Resolved Skills Map — auto-derived — verify

**Stop-word list** — exclude the following universally-understood terms from extraction regardless of which rule matched. Adding a term requires editing this list.

```
JSON, XML, YAML, CSV, HTTP, HTTPS, URL, URI, UUID, UTF-8, ASCII, ISO-8601,
SHA, MD5, TLS, SSL, API, CLI, GUI, SDK, OS, RAM, CPU, ID, IP
```

Emit Warning for each glossary entry (user review required regardless of source rule).

</phase-3-vocabulary>

<phase-4-taxonomy>

## Phase 4 — Taxonomy hygiene

Common checks — always run:

| Check | Severity |
|:--|:--|
| ID format `<CAT>-NNN` valid per category | Warning |
| ID sequence dense per category (no gaps) | Warning |
| No duplicate IDs within a category | Warning |
| Terms used in requirements are present in §Glossary | Warning |

Typology-specific checks: follow rules in loaded typology reference files.

Emit closure line at end of Phase 4 always, even at zero findings:

```
Outstanding: N blocking, M warnings, K info
```

**Edge-case example — sparse ID sequence**

Substrate excerpt:
  FR-001 The system shall accept a slug argument.
  FR-007 The system shall validate substrate format.

Phase 4 emission:
  Warning — FR category: declared IDs FR-001, FR-007; sequence gap detected (FR-002..FR-006 absent).
  Outstanding: 0 blocking, 1 warning, 0 info

</phase-4-taxonomy>

<phase-5-verification>

## Phase 5 — Verification

Follow `references/verification.md` for:

- **§ Acceptance Criteria** — per-requirement derivation; Warning if no derivable AC exists
- **§ Quality Criteria scorecard** — 5-criterion scoring per requirement

</phase-5-verification>

<phase-6-format-write>

## Phase 6 — Format + write

Apply format pass across all sections per active template. Add version block at bottom of both output files.

**Version:** read from prior `<slug>-requirements.md` if present; increment rightmost segment (`0.1 → 0.2`). Initial value: `0.1`. Status: always `Draft`. Last Updated: current date.

**Write order:** `<slug>-requirements.md` first, then `<slug>-report.md`. Reason: `<slug>-requirements.md` is the user-facing deliverable; `<slug>-report.md` is its diagnostic. Writing the diagnostic first would let a successful report appear on disk before its referent deliverable existed, misleading any user who inspects the requirements file to confirm the run's outcome.

| Failure scenario | Behavior |
|:--|:--|
| `<slug>-requirements.md` write fails | Abort; no `<slug>-report.md` written; prior files intact |
| `<slug>-report.md` write fails after `<slug>-requirements.md` succeeds | Surface hard-fail; prior `<slug>-report.md` remains; user detects via version-block mismatch and re-runs |

Commit gate suppressed for this skill; user commits post-run. Reason: this skill is iterative — prior `<slug>-requirements.md` is intended to be fed back as substrate to refine the next pass. Prompting at every Phase 6 write would interrupt the iteration loop with redundant commit decisions on still-Draft content; the user batches commits after review instead.

</phase-6-format-write>

| Field                | Value                                |
|----------------------|--------------------------------------|
| Target Model         | claude-opus-4-7                      |
| Target Environment   | claude-code                          |
| Best-Practices Ref   | 2026-05-17 snapshot                  |
| Last Revised         | 2026-05-22                           |
| Revision Source      | improving-prompt-artifacts skill     |
