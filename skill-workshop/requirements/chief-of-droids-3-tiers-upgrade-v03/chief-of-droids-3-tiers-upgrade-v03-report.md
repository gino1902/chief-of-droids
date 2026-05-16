# Report — chief-of-droids-3-tiers-upgrade-v03

## Summary

| Severity | Resolved | Unresolved |
|:--|:--:|:--:|
| Blocking | 0 | 0 |
| Warning  | 14 | 4 |
| Info     | 6 | N/A |

## Phase 0 — Pre-flight

- [INFO] Slug `chief-of-droids-3-tiers-upgrade-v03` valid; contains none of the banned tokens (`requirement`, `req`, `reqs`).
- [INFO] `--type technical` resolved; loaded `template-s2.md`, `ears.md`, `rfc2119.md`, `tables.md`, `verification.md`.
- [INFO] Substrate `./requirements/substrates/two-tier-architecture-design-notes.md` resolved relative to cwd.
- [INFO] Repo root resolved at `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/` (first ancestor containing `CLAUDE.md`).
- [INFO] No prior `chief-of-droids-3-tiers-upgrade-v03-requirements.md` found at output path; initial version is `0.1`. Sibling directories `chief-of-droids-3-tiers-upgrade-v01/` and the standalone `chief-of-droids-3-tiers-upgrade-gap-analysis.md` are slug-distinct and not consulted for ID stability.
- [INFO] Output directory `requirements/chief-of-droids-3-tiers-upgrade-v03/` created.

Outstanding: 0 blocking, 0 warnings, 6 info

## Phase 1 — Framing

- [INFO] Title taken from substrate H1: `Two-Tier CLAUDE.md Architecture — Design Notes`. Slug fallback not used.
- [INFO] Purpose synthesised from substrate Context section ("This document proposes a two-tier architecture that resolves both") combined with the six-capabilities table from "Requirements framing".
- [WARNING] In Scope and Out of Scope lists derived from positive language ("must handle", "must implement via instruction", "covered by", "deferred", "parked", "outside the framework's control"); items reflect substrate signal verbatim. User should verify completeness for the v03 cut.
- [INFO] Actors & Consumers extracted from substrate references to user prompts (operator), Claude Desktop client (`recent_chats[0].uri`, Project Instructions slot), filesystem MCP, git MCP, `creating-skills`, and workspace/project skill cross-references.

Outstanding: 0 blocking, 1 warning, 2 info

## Phase 2 — Drafting

- [INFO] No substrate-declared `<CAT>-NNN` IDs detected; fresh canonical ordering applied per `conventions.md` § "Canonical ordering for un-IDed substrate".
- [WARNING] FR-002 (Solicit shape) and FR-015 (Solicit shape) intentionally not paired with an ERR. Inline opt-out rationale attached on each entry: substrate prescribes wait-on-user / informational prompt with no enforced failure path. No Phase 4 Warning fires.
- [WARNING] FR-007 split into separate Acquire (reload) and Mutate (sentinel SHA update — FR-008) entries per the "one SHALL per entry" rule. The substrate sentence "On any mismatch, reload that file and update sentinel." combines two SHALL actions in one sentence.
- [WARNING] CON-009 ("Skill composition between tiers SHALL be one-way from project to workspace.") and CON-010 ("Workspace skills SHALL NOT reference project skills.") split from the single substrate sentence "Composition strictly one-way (workspace cannot reference project skills)." Split was needed to keep one modal verb per CON entry.
- [WARNING] FR-013 phrased as `MUST increment the major segment`. Substrate text "major bump on trigger edit" does not specify whether the version is `<major>.<minor>` or `<major>.<minor>.<patch>`; "major" is taken as the leftmost segment.
- [INFO] ERR coverage derived from contract-shape matrix:
  - Acquire: FR-001 → ERR-001; FR-003 → ERR-002; FR-007 → ERR-005.
  - Mutate: FR-004 → ERR-003; FR-008 → ERR-006; FR-013 → ERR-008.
  - Validate: FR-006 → ERR-004; FR-011 → ERR-007.
  - Solicit (opt-out): FR-002, FR-015.
  - Emit / Select / Unwanted (no ERR): FR-005, FR-009, FR-010, FR-012, FR-014.

Outstanding: 0 blocking, 4 warnings, 2 info

## Phase 3 — Vocabulary

- [INFO] Glossary extracted by mechanical rules in order:
  - Backtick rule produced `recent_chats[0].uri`, `creating-skills`, `workspace_md_sha`, `project_md_sha`, `brief_sha`, `resolved_skills`, and file-path tokens (paths surfaced inline in requirements; not added as separate glossary entries because they are values, not concepts).
  - Capitalized noun-phrase rule produced `Project Instructions`, `Workspace tier`, `Project tier`, `Sentinel`, `Bootstrap protocol`, `Always-on tools`, `Project brief`.
  - Numbered-layer phrases `Layer 1`, `Layer 2`, `Layer 3` matched the capitalized noun-phrase rule.
  - Acronym rule did not produce any non-stop-worded acronym used in a requirement statement (SHA, URI, MCP are either stop-worded or appear only in glossary definitions, not in requirement statements).
  - Explicit substrate-definition rule produced `Registration`, `Routing`, `Usage` (defined under "Tool layer vocabulary"), and the three Layer definitions.
- [WARNING] Status `auto-derived — verify` applied to all rule-1/2/3 entries (12 entries). User review required.
- [INFO] Status `substrate` applied to 7 entries explicitly defined by the substrate (`Layer 1`, `Layer 2`, `Layer 3`, `Project brief`, `Always-on tools`, `Registration`, `Routing`, `Usage`).

Outstanding: 0 blocking, 1 warning, 2 info

## Phase 4 — Taxonomy hygiene

Common checks:

- [INFO] ID format check: all 47 identifiers conform to `<CAT>-NNN`.
- [INFO] ID sequence density: FR-001..015 (15 entries, dense), CON-001..013 (13 entries, dense), ERR-001..008 (8 entries, dense), IR-IN-001..003 (3, dense), IR-OUT-001..003 (3, dense), DR-001 (1), TR-001..002 (2, dense), NFR-001..003 (3, dense). No gaps.
- [INFO] Duplicate-ID check: none within any category.
- [INFO] Glossary-coverage check: domain-specific terms used in requirement statements (`Layer 1/2/3`, `Project Instructions`, sentinel field names, `creating-skills`, `recent_chats[0].uri`, `Always-on tools`, `Workspace tier`, `Project tier`, `Project brief`) are all present in §Glossary.

EARS / RFC 2119 checks:

- [INFO] One-SHALL-per-entry: FR-001..015 and CON-001..013 each carry exactly one modal verb after the FR-007 split and CON-009/010 split.
- [INFO] ERR section uses Unwanted Behavior EARS exclusively; every entry carries a cross-link `→ FR-NNN` that resolves to an FR in this artifact.
- [INFO] RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) absent from FR/CON/ERR EARS statements; SHALL only.
- [INFO] FR-test (falsified only by runtime observation) satisfied for FR-001..015; CON-test (falsified by static inspection) satisfied for CON-001..013. No misclassification.
- [INFO] ERR contract-shape coverage matrix audit: every mandatory-coverage FR is either paired with an ERR or carries an inline opt-out rationale (FR-002, FR-015). No bare coverage gap.

T2 (RFC 2119) checks:

- [INFO] Each IR/NFR entry contains at least one RFC 2119 keyword (`MUST` or `SHOULD`).
- [INFO] IR-IN and IR-OUT sub-sections both rendered.
- [INFO] NFR-001 (Reliability) and NFR-002 (Performance) universal slots both present.
- [WARNING] NFR-002 rendered as `N/A — substrate silent on performance` per the universal-slot rule; Atomic / Unambiguous / Bounded score `N/A` or `✗` accordingly.
- [WARNING] NFR-003 Measurement field set to `TBD`; no numeric threshold available from substrate. Bounded scores `✗`.
- [INFO] SEC and OBS sections rendered as `N/A` text; no numeric ID (`SEC-001`, `OBS-001`) emitted.

T3/T4 (table-form) checks:

- [INFO] DR-001 uses contract table form with the four required columns (Field, Type, Constraints, Notes); no EARS or RFC 2119 keywords inside the table.
- [INFO] TR-001 and TR-002 use rule table form with the three required columns (Input, Rule, Output).
- [WARNING] TR-002 Rule column carries an underspecified transformation — substrate references "SHA" without naming the hash algorithm (SHA-1 / SHA-256 / other). Surfaced as TR with Warning per `tables.md` § "TR exclusion list" guidance for substrate-named-but-rule-implicit transformations.

Closed-enumeration checks:

- [WARNING] §Security rendered `N/A — substrate silent on Security` — substrate addresses none of categories (a)–(f) (authentication, authorization, encryption, audit logging, rate limiting, input validation). Per `rfc2119.md` § "Empty-section rule".
- [WARNING] §Observability rendered `N/A — substrate silent on Observability` — substrate addresses none of categories (a)–(e) (metric exposure, structured log emission, trace span emission, health endpoint, alert threshold). The anchor-message emission (FR-005) is correctly scoped to IR-OUT-002, not OBS, per the OBS exclusion list. The sentinel SHA fields are correctly scoped to DR-001, not OBS.

Outstanding: 0 blocking, 5 warnings, 15 info

## Phase 5 — Verification

- [INFO] AC entries derived per `verification.md` derivation table for every requirement except NFR-002 (N/A — substrate silent) and NFR-003 (no quantitative threshold).
- [WARNING] NFR-002 Verifiable scores `✗`; the requirement has no derivable AC because the substrate provides no performance signal.
- [WARNING] NFR-003 Verifiable scores `✗`; the requirement has no derivable AC because the Measurement field is `TBD`.
- [WARNING] NFR-003 Bounded scores `✗`; no quantitative signal in Measurement. User should specify a token budget threshold or accept the requirement as advisory.
- [INFO] Quality scorecard rendered with 47 rows. Atomic / Unambiguous / Verifiable / Traceable / Bounded scored per the rules in `verification.md`.
- [INFO] NFR-001 scores `✓` on Bounded (`≥ 92%` is a percentage signal per the canonical mapping table in `rfc2119.md`).

Outstanding: 0 blocking, 3 warnings, 3 info

## Phase 6 — Format

- [INFO] Format pass applied across all 15 sections per `template-s2.md`. Headings use the canonical anchors; tables use the canonical column sets.
- [INFO] Version block set to `Version: 0.1`, `Last Updated: 2026-05-15`, `Status: Draft`. Initial-version rule applied (no prior `chief-of-droids-3-tiers-upgrade-v03-requirements.md` was found at the output path).
- [INFO] Write order: `chief-of-droids-3-tiers-upgrade-v03-requirements.md` first, then this report.

Outstanding: 0 blocking, 0 warnings, 3 info

---

| Field        | Value      |
|:--|:--|
| Version      | 0.1        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
