# Report — chief-of-droids-3-tiers-upgrade-v02

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |   24     |    13      |
| Info     |   28     |    N/A     |

## Phase 0 — Pre-flight

- [INFO] Slug `chief-of-droids-3-tiers-upgrade-v02` validated against `^[a-z0-9-]+$`; no `req`/`reqs`/`requirement` substring present.
- [INFO] `--type technical` accepted; technical typology references loaded (`conventions.md`, `template-s2.md`, `ears.md`, `rfc2119.md`, `tables.md`, `verification.md`).
- [INFO] Substrate file `./requirements/substrates/two-tier-architecture-design-notes.md` resolved (156 lines, `.md` extension).
- [INFO] Repo root resolved at `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/` via `CLAUDE.md` discovery in cwd.
- [INFO] Output directory `requirements/chief-of-droids-3-tiers-upgrade-v02/` did not exist; created.
- [INFO] No prior `chief-of-droids-3-tiers-upgrade-v02-requirements.md` found at output path; treating as initial pass at version 0.1.

Outstanding: 0 blocking, 0 warnings, 6 info

## Phase 1 — Framing

- [INFO] Title resolved from first substrate H1: "Two-Tier CLAUDE.md Architecture — Design Notes". Emitted verbatim per skill rules (no humanisation).
- [WARNING] Slug names the architecture as a "3-tiers-upgrade" but the substrate frames it as "two tiers, three layers". Naming-axis tension surfaced; user to reconcile the slug vs substrate vocabulary in a future iteration or explicitly document the equivalence. → Unresolved
- [WARNING] No explicit "The purpose of…" formulation in substrate. Purpose paragraph inferred from substrate "Context" block and the sentence "This document proposes a two-tier architecture that resolves both [duplications and category errors]." User to verify the inferred purpose. → Resolved (user verify only)
- [WARNING] §Scope In Scope extracted from substrate's "Requirements framing" enumeration and "Architecture — two tiers, three layers" table; substrate does not use positive markers like "in scope" / "covers". Inference relied on these structural sections. → Resolved (user verify only)
- [WARNING] §Scope Out of Scope assembled from explicit deferrals ("Drift prevention … deferred", "Session identity mechanism (parked)"), Open Items, and the "Registration … outside the framework's control" statement. Coverage may be incomplete; user to confirm. → Unresolved
- [WARNING] §Actors derived primarily from upstream/downstream substrate signals (filesystem MCP, chat client, `creating-skills`, skill manifests, path-scoped rule files); only the user role is explicitly named. Verify actor list completeness. → Resolved (user verify only)

Outstanding: 0 blocking, 5 warnings, 1 info

## Phase 2 — Drafting

- [INFO] 14 FR entries drafted in substrate byte-position order: bootstrap protocol (FR-002…FR-009) anchored at lines 60–75; skills routing thread (FR-010…FR-014) anchored at lines 117–132; conditional rules table row (FR-001) anchored at line 31.
- [INFO] 16 CON entries drafted covering layer placement, tier precedence, schema invariants, governance, and composition direction.
- [INFO] 7 IR-IN + 5 IR-OUT entries drafted; both subsections rendered.
- [INFO] 1 DR (session sentinel) + 3 TR (sentinel path derivation, SHA computation, resolved-skills map derivation) drafted.
- [INFO] 3 NFR slots rendered: NFR-001 reliability (substrate 92–93% routing estimate); NFR-002 universal performance slot (`N/A — substrate silent`); NFR-003 footprint (qualitative threshold; Measurement TBD).
- [INFO] §Security rendered as N/A — substrate addresses none of the six closed-enumeration categories. No `SEC-001` allocated.
- [INFO] §Observability rendered as N/A — substrate addresses none of the five closed-enumeration categories. Anchor confirmation (FR-007 / IR-OUT-002) classified under IR-OUT per OBS exclusion list, not OBS. No `OBS-001` allocated.
- [INFO] 11 ERR entries drafted in the same Phase 2 pass per mandatory ERR-coverage protocol: ERR-001 (FR-001 Acquire), ERR-002 (FR-002 Acquire), ERR-003 (FR-004 Acquire), ERR-004 (FR-005 Validate), ERR-005 (FR-006 Mutate), ERR-006 (FR-008 Validate), ERR-007 (FR-009 Acquire+Mutate), ERR-008 (FR-010 Mutate), ERR-009 (FR-011 Validate), ERR-010 (FR-012 Mutate), ERR-011 (FR-013 Validate).
- [INFO] 3 FR entries carry inline opt-out rationales: FR-003 (Solicit — in-band conversational prompt), FR-007 (Emit — no return contract), FR-014 (Solicit — advisory prompt).
- [WARNING] Substrate contains internal tension between the table at lines 26–31 ("Available tools | Always-on tools at workspace level") and the Tool-layer-vocabulary section at lines 47–55 ("Always-on tools … are routed at Layer 1"). Took the Tool-layer-vocabulary statement as normative (more specific and explicitly disambiguates Registration/Routing/Usage); encoded as CON-005 and IR-IN-007 / FR-001. User to confirm or revise the table at lines 26–31. → Unresolved
- [WARNING] FR-001 (path-scoped rule files load on filesystem read) drafted from the substrate table row "Conditional rules by file type | dispatcher loads on filesystem read", but substrate's Open Items section flags conditional-rules format as not-yet-specified. FR-001 may be premature; user to confirm or defer to a later iteration. → Unresolved
- [WARNING] TR-002 SHA algorithm not specified by substrate. Drafted as generic "SHA digest"; user to pin algorithm (e.g. SHA-256). → Unresolved
- [WARNING] ERR-002 semantics for "sentinel present but unreadable / malformed" inferred from substrate's "If sentinel absent or uri mismatch" branch. Substrate folds unreadable into the absent branch implicitly; user to confirm or split into a distinct error path. → Unresolved
- [WARNING] FR-013 (block workspace skill removal while referenced) contract shape interpreted as Validate-with-rejection-response. An alternate reading is Mutate-refusal; the ERR coverage (ERR-011) is equivalent under either reading but the classification affects future audit logic. → Unresolved
- [WARNING] CON-014 governance escape hatch invokes "PR-to-workspace" — substrate phrasing borrows GitHub vocabulary without specifying repository or workflow. Encoded as governance-level constraint; user to specify the actual mechanism. → Unresolved
- [WARNING] DR-001 sentinel lifecycle ("retained for the lifetime of the chat session; cross-session retention not specified") inferred from substrate context; substrate does not declare retention or pruning policy. → Unresolved
- [WARNING] TR-003 resolved-skills map derivation uses the workspace-tier-wins precedence under the CON-011 disjoint-trigger invariant. The derivation is well-defined only because of CON-011; if CON-011 is relaxed or violated, TR-003 becomes ambiguous. Dependency flagged. → Resolved (user verify only)
- [WARNING] NFR-003 footprint Measurement is TBD; substrate provides qualitative threshold only ("minimal but sufficient"). Triggers the unbounded-NFR Warning per `references/rfc2119.md` bounded heuristic. → Unresolved
- [WARNING] NFR-002 performance slot rendered as `N/A — substrate silent` per universal-slot rule for `--type technical`. Note tension with `conventions.md` rule "N/A sections SHALL NOT carry requirement IDs": prioritized the universal-slot rule from `references/rfc2119.md`. → Resolved (skill-internal precedence resolved)

Outstanding: 0 blocking, 10 warnings, 10 info

## Phase 3 — Vocabulary

- [INFO] 11 substrate-defined entries extracted (rule 4): Layer 1 (Dispatcher), Layer 2 (Workspace), Layer 3 (Project), Sentinel, Project brief, Always-on tools, Registration, Routing, Usage, Bootstrap protocol, Workspace-tier-wins precedence.
- [INFO] 13 auto-derived entries extracted (rules 1–3): MCP, PR (rule 1); `recent_chats[0].uri`, `creating-skills`, `workspace_md_sha`, `project_md_sha`, `brief_sha`, `resolved_skills` (rule 2); Project Instructions, Dispatcher, Path-scoped rule files, Anchor, Trigger phrase (rule 3).
- [INFO] Stop-word list applied: `MCP` retained (not in stop list); `URI`, `JSON`, `SHA` excluded from extraction (in stop list).
- [WARNING] Each of the 24 glossary entries requires user verification — auto-derivation may misclassify or underspecify definitions. (One warning per entry; surfaced as a single aggregate finding here per the per-entry-warning rule in `conventions.md`.) → Resolved (user verify only)

Outstanding: 0 blocking, 1 aggregated warning (covers 24 per-entry user-verify warnings), 3 info

## Phase 4 — Taxonomy hygiene

- [INFO] ID-format check: all IDs match `<CAT>-NNN`; categories valid (FR, CON, IR-IN, IR-OUT, DR, TR, NFR, ERR).
- [INFO] ID-sequence density check: FR-001…014 dense; CON-001…016 dense; IR-IN-001…007 dense; IR-OUT-001…005 dense; TR-001…003 dense; NFR-001…003 dense; ERR-001…011 dense; DR-001 single. No gaps.
- [INFO] Duplicate-ID check: zero duplicates within any category.
- [INFO] EARS-pattern legality (FR, CON, ERR): all FR and CON entries use one of the five EARS patterns; all ERR entries use Unwanted Behavior form.
- [INFO] One-SHALL-per-statement check (FR, CON): every FR and CON contains exactly one `SHALL` modal verb.
- [INFO] No RFC 2119 keywords inside EARS statements (FR, CON, ERR): confirmed.
- [INFO] No EARS `SHALL` inside pure RFC 2119 statements (NFR, IR RFC-form lines): confirmed.
- [INFO] ERR cross-link check: every ERR entry contains a `→ FR-NNN` cross-link, and every referenced FR exists.
- [INFO] FR test (falsified only by runtime observation): all FRs satisfy the FR test under the binary decision and tie-breaker rules in `references/ears.md`.
- [INFO] ERR mechanism-naming check: no ERR text names file, network, MCP, or database mechanisms — error responses are stated at the contract level.
- [INFO] ERR coverage protocol: every FR of mandatory-coverage shape (Acquire, Mutate, Validate, Solicit, Transform-external-inputs) is either paired with an ERR or carries an explicit inline rationale (FR-003, FR-007, FR-014).
- [INFO] NFR universal slots: NFR-001 (Reliability) and NFR-002 (Performance) both present.
- [INFO] NFR canonical-mapping check: NFR-001 (reliability), NFR-002 (performance, N/A), NFR-003 (footprint — substrate signal "minimal", "token cost") follow the canonical mapping table in `references/rfc2119.md`.
- [INFO] §Security and §Observability N/A renders carry no numeric IDs.
- [INFO] DR/TR table-column completeness: DR-001 includes Field, Type, Constraints, Notes; TR-001…003 each include Input, Rule, Output.
- [INFO] DR exclusion rule: only DR-001 (session sentinel) qualifies as a data entity with typed fields; no markdown-file-as-DR pollution.
- [INFO] TR candidate-signal check: TR-001 (path derivation), TR-002 (hash computation), TR-003 (rule-table derivation) all match candidate categories in `references/tables.md`.
- [WARNING] Glossary coverage gap — some terms used in requirement statements may not yet be explicitly defined in §Glossary: "fail-fast tier resolution" (used in CON-012 — implicit from prose, definition not surfaced as a glossary row), "negative trigger" (used in CON-016 — substrate refers to it without defining), "tier" (used pervasively but only defined implicitly via Layer 1/2/3 entries). User to add explicit rows or accept the implicit definitions. → Unresolved
- [WARNING] NFR-003 Measurement is TBD; substrate provides no numeric threshold. Counts as an unbounded NFR per the bounded heuristic in `references/rfc2119.md`. → Unresolved
- [WARNING] TR-002 carries the same SHA-algorithm gap surfaced in Phase 2; restated here as a Phase 4 hygiene finding for traceability. → Unresolved (carries forward)

Outstanding: 0 blocking, 3 warnings, 17 info

## Phase 5 — Verification

- [INFO] Acceptance Criteria derived for all 60 requirement entries (14 FR + 7 IR-IN + 5 IR-OUT + 1 DR + 3 TR + 3 NFR + 16 CON + 11 ERR). NFR-002 and NFR-003 AC entries explicitly `N/A`.
- [INFO] Quality Criteria scorecard rendered for all 60 requirement entries.
- [INFO] Atomic auto-score: all entries pass except NFR-002 (N/A — no statement to score).
- [INFO] Unambiguous heuristic score: TR-002 marked ✗ on Unambiguous (SHA algorithm not pinned; "SHA digest" is open to multiple interpretations).
- [INFO] Verifiable auto-score: NFR-002 and NFR-003 marked ✗ (no derivable AC due to missing quantitative threshold).
- [INFO] Bounded heuristic score: NFR-001 ✓ (92%); NFR-002 ✗ (no signal); NFR-003 ✗ (TBD).
- [WARNING] NFR-002 and NFR-003 fail Verifiable and Bounded scores — flagged on the scorecard. Triggers the unbounded-NFR Warning per the bounded heuristic. → Unresolved (carries forward from Phase 4)
- [WARNING] TR-002 fails Unambiguous on the scorecard — same root cause as the SHA-algorithm gap surfaced in Phase 2/4. → Unresolved (carries forward)

Outstanding: 0 blocking, 2 warnings (carry-forwards), 6 info

## Phase 6 — Format

- [INFO] Version block applied to both output files: Version 0.1, Last Updated 2026-05-15, Status Draft.
- [INFO] Output files written in order: `chief-of-droids-3-tiers-upgrade-v02-requirements.md` then `chief-of-droids-3-tiers-upgrade-v02-report.md`.

Outstanding: 0 blocking, 0 warnings, 2 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
