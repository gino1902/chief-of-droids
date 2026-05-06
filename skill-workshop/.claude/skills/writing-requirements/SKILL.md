---
name: writing-requirements
description: Produces a structured requirements artifact and diagnostic report for one deployable component from a markdown substrate. Output files are written to `<CLAUDE.md parent dir>/requirements/<slug>/` and named `<slug>-requirements.md` and `<slug>-report.md`. Invoke as `writing-requirements <slug> from <path> --type generic|technical` — slug must not contain "requirement", "req", or "reqs". Use --type generic for lightweight functional requirements: skill definitions, file format specs, pre-design tech objects, migration requirements. Use --type technical for full requirements covering functional, interface, data, non-functional, security, error handling, and observability. Iterates statelessly: feed prior `<slug>-requirements.md` as substrate to refine.
allowed-tools:
  - Read
  - Write
---

# writing-requirements

Produces two output files for one deployable component (container, service, module-as-container, app):

- `<slug>-requirements.md` — structured requirements artifact
- `<slug>-report.md` — per-phase diagnostic report

Seven phases run sequentially in memory. No writes until Phase 6 completes.

## Reference files

| File | Load at | Condition |
|:--|:--|:--|
| `references/conventions.md` | Phase 0 | Always |
| `references/template-s1.md` | Phase 0 | `--type generic` |
| `references/template-s2.md` | Phase 0 | `--type technical` |
| `references/ears.md` | Phase 1 | Always — both types include T1 sections |
| `references/rfc2119.md` | Phase 1 | `--type technical` only |
| `references/tables.md` | Phase 1 | `--type technical` only |
| `references/verification.md` | Phase 5 | Always |

## Invocation

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

## Phase model

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

## Phase 1 — Framing

Read typology reference files per the table above, then produce:

**§ Title + Purpose**
Title: first H1 in substrate; fallback: first H2; fallback: frontmatter `title:`; fallback: slug + Warning.
Purpose: extract explicit purpose statement ("The purpose of…", "This component…", "This skill…"); if absent, infer from leading prose + Warning.

**§ Scope**
In Scope: extract from positive language — "in scope", "covers", "handles", "responsible for".
Out of Scope: extract from negation — "not handled", "outside this", "downstream", "upstream", "out of scope", "owned by".
Each subsection: `N/A` + Warning if signal absent. No synthesis when signal is absent.

**§ Actors & Consumers**
Extract upstream/downstream systems and human roles. `N/A` + Warning if absent.

## Phase 2 — Drafting

Follow drafting rules in loaded typology reference files. All sections always render; `N/A` + Warning if substrate signal is absent for a section.

**ID stability:** scan substrate for declared IDs matching `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b`. Preserve matched IDs, attaching each to the nearest requirement-shaped block. Undeclared requirements get the next available sequence number per category.

## Phase 3 — Vocabulary

Auto-extract glossary candidates from substrate: technical nouns, domain-specific terms, acronyms, and terms used in requirements that are not self-evident. Render as §Glossary. Emit Warning for each auto-derived entry (user review required).

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

## Phase 5 — Verification

Follow `references/verification.md` for:

- **§ Acceptance Criteria** — per-requirement derivation; Warning if no derivable AC exists
- **§ Quality Criteria scorecard** — 5-criterion scoring per requirement

## Phase 6 — Format + write

Apply format pass across all sections per active template. Add version block at bottom of both output files.

**Version:** read from prior `<slug>-requirements.md` if present; increment rightmost segment (`0.1 → 0.2`). Initial value: `0.1`. Status: always `Draft`. Last Updated: current date.

**Write order:** `<slug>-requirements.md` first, then `<slug>-report.md`.

| Failure scenario | Behavior |
|:--|:--|
| `<slug>-requirements.md` write fails | Abort; no `<slug>-report.md` written; prior files intact |
| `<slug>-report.md` write fails after `<slug>-requirements.md` succeeds | Surface hard-fail; prior `<slug>-report.md` remains; user detects via version-block mismatch and re-runs |

Commit gate suppressed for this skill; user commits post-run.
