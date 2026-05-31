# Report — data-platform-v01

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |    7     |    11      |
| Info     |    6     |    N/A     |

## Phase 0 — Pre-flight

- [INFO] Slug `data-platform-v01` accepted; matches `^[a-z0-9-]+$` and excludes reserved tokens.
- [INFO] `--type technical` accepted; template-s2 + ears + rfc2119 + tables + verification loaded.
- [INFO] Repo root resolved to `/Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop` (CLAUDE.md present in cwd).
- [INFO] Output directory `requirements/data-platform-v01/` created.
- [INFO] No prior `data-platform-v01-requirements.md` found; initial version `0.1`.
- [INFO] Substrate `requirements/substrates/data-platform.md` read (10927 bytes, `.md`).

Outstanding: 0 blocking, 0 warnings, 6 info

## Phase 1 — Framing

- [INFO] Title extracted from substrate H1: "SQLI – Data Platform Creation"; component framed as "SQLI Data Platform" per slug intent.
- [WARNING] Substrate is at "System & Containers level" and uses two distinct subjects ("the System", "the Data Platform"). Requirements are produced for the Data Platform component; statements scoped to the System orchestrator are listed in Out of Scope. → Confirm component framing matches intent of slug `data-platform-v01`.
- [WARNING] Purpose statement was inferred from substrate context and Glossary entry for "Data Platform"; substrate has no explicit "The purpose of…" sentence. → Confirm Purpose paragraph reflects intent.
- [INFO] Scope In/Out lists derived from positive ("manages", "covers") and negation ("System level", "owned by") signals in F1–F20, G1–G4, O1–O6.
- [INFO] Actors & Consumers extracted from F1, F5, F8, F9, F13, F20, G4, O4 plus inferred Data owners / stewards from F18.

Outstanding: 0 blocking, 2 warnings, 2 info

## Phase 2 — Drafting

- [INFO] Substrate IDs (`F1`, `G1`, `O1`, `NFR1`, …) do not match canonical `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b` regex; ID stability not invoked. New sequence numbers assigned per category.
- [WARNING] FR-009 (from F17 "exposes all data required for business workflows") is broad — "business workflows" not enumerated in substrate; statement retained but not testable. → Either enumerate workflows in substrate or split into per-workflow FRs.
- [WARNING] NFR-004 (single point of failure, from NFR3) has no measurement in substrate; flagged `Measurement: TBD`. → Define redundancy / failover topology in design phase.
- [WARNING] NFR-005 (SLA targets, from NFR6) flagged `Measurement: TBD with Business Users`. → Capture availability, latency, freshness thresholds.
- [WARNING] NFR-006 (SLO, from NFR7) flagged `Measurement: TBD with Business Users`. → Capture freshness SLO targets.
- [WARNING] SEC-004 (GDPR / RTO / RPO compliance, from NFR5) measurement TBD for RTO and RPO numerics. → Capture RTO and RPO thresholds.
- [WARNING] ERR-001 retry policy (NFR1) and ERR-002 dead-letter destination (NFR2) parameters TBD in substrate. → Define policy parameters and DLQ workflow.
- [INFO] F12 ("retention beyond Landing Zone complies with SQLI policy") moved to CON-005 (constraint on Data Platform retention configuration) rather than FR.
- [INFO] F13/F14/F15 (one-producer / one-contract / DP-owned) moved to CON-001/002/003 as invariants rather than behaviors.
- [INFO] F4 ("Landing Zone subsystem-agnostic format") expressed as IR-IN-002 — the Data Platform's contract on the Landing Zone interface; Landing Zone behavior itself is out of scope.
- [INFO] G4 ("System enforces access control to the Data Platform via AD") expressed as IR-IN-001 + SEC-005 — the Data Platform's obligation to consume AD-mediated identity.
- [INFO] O3 (auditability) expressed as SEC-006 + OBS-004 — both audit production and audit/lineage retrieval.
- [INFO] O5 ("System manages observability of exchanges not in DP scope") not rendered as DP requirement; recorded in §Scope Out of Scope.

Outstanding: 0 blocking, 6 warnings, 6 info

## Phase 3 — Vocabulary

- [INFO] Substrate Glossary reproduced with `Status: substrate` for terms used in requirements. 41 substrate entries retained.
- [WARNING] Auto-derived: "Authorised operator" — used in FR-004 / IR-IN-003 but not defined in substrate Glossary. → Confirm definition.
- [WARNING] Auto-derived: "Business-ready dataset" — used in FR-002 / FR-003 / IR-OUT-001 / TR-001; substrate has "Standardised data" but not the joined term. → Confirm whether "business-ready" is synonymous with "standardised" or carries an additional contract-readiness semantic.
- [WARNING] Auto-derived: "Data freshness" — used in NFR-005 / NFR-006 / DR-001 (`freshness_target`); substrate uses "freshness" inline without definition. → Confirm definition.

Outstanding: 0 blocking, 3 warnings, 1 info

## Phase 4 — Taxonomy hygiene

- [INFO] ID format check passed for all categories: FR (1–9), IR-IN (1–3), IR-OUT (1–3), DR (1–3), TR (1), NFR (1–6), SEC (1–6), CON (1–6), ERR (1–4), OBS (1–4). No duplicates.
- [INFO] Sequence density check passed: each category dense from `001` upward.
- [INFO] EARS pattern check: FR-001/FR-004 Event-driven; FR-002/FR-003/FR-005…FR-009 Ubiquitous; CON-001…CON-006 Ubiquitous; ERR-001…ERR-004 Unwanted Behavior; SEC-003 Unwanted Behavior. All legal.
- [INFO] One-`SHALL` check: each FR/CON/ERR/EARS-form SEC entry contains exactly one `SHALL`.
- [INFO] RFC 2119 keyword check: all IR/NFR/OBS and RFC-form SEC entries contain `MUST` or `SHOULD`. EARS `SHALL` not mixed in those statements.
- [INFO] ERR cross-link check: ERR-001→FR-001, ERR-002→FR-002, ERR-003→FR-005, ERR-004→FR-004; all targets exist.
- [INFO] DR / TR table-form check: no RFC 2119 keywords or EARS syntax inside tables; column sets complete (Field/Type/Constraints/Notes; Input/Rule/Output).
- [INFO] IR-IN and IR-OUT both rendered with non-empty content.
- [WARNING] NFR Measurement field bounded-heuristic: NFR-004, NFR-005, NFR-006 carry no numeric / time / percentage / volume signal; explicitly flagged `TBD`. → User verification required before Measurement is finalised.
- [WARNING] Bounded-heuristic on SEC-004: RTO and RPO referenced without thresholds. → Add numeric values.
- [WARNING] Bounded-heuristic on OBS-001, OBS-002, OBS-004: observability obligations without quantitative thresholds. → Either add thresholds (e.g., metrics emission interval) or accept as qualitative obligations.
- [INFO] Glossary completeness for Unambiguous criterion: 41 substrate + 3 auto-derived terms cover all domain-specific nouns used in requirements; "business workflows" (FR-009) remains undefined.
- [WARNING] Glossary gap: "business workflows" — used in FR-009; not defined in Glossary. → Define or scope out FR-009.

Outstanding: 0 blocking, 5 warnings, 8 info

## Phase 5 — Verification

- [INFO] Acceptance Criteria derived for all 44 requirements per `references/verification.md`.
- [WARNING] FR-009 — AC marked `N/A` (no enumerable business workflows in substrate); Verifiable scored ✗. → Resolves once business workflows are enumerated.
- [WARNING] NFR-004 / NFR-005 / NFR-006 — AC marked `N/A` (Measurement TBD); Verifiable scored ✗ and Bounded scored ✗. → Resolves once thresholds are captured.
- [WARNING] SEC-004 — AC marked `N/A` (RTO/RPO thresholds TBD); Verifiable scored ✗ and Bounded scored ✗. → Resolves once thresholds are captured.
- [INFO] Quality Criteria scorecard: 44 rows, 5 columns; Bounded `N/A` for FR/CON/ERR/IR/DR/TR per spec.
- [INFO] Atomic auto-score: every entry contains exactly one modal verb.
- [INFO] Traceable auto-score: every Req ID matches `<CAT>-NNN`.
- [INFO] Unambiguous heuristic: only FR-009 fails (term "business workflows" undefined).

Outstanding: 0 blocking, 5 warnings, 5 info

## Phase 6 — Format

- [INFO] Format pass applied: all 14 content sections plus version block render in template order; section headings match template-s2 levels.
- [INFO] Version block written: `0.1`, `2026-05-06`, `Draft`.
- [INFO] Write order honoured: `data-platform-v01-requirements.md` written first, then this report.

Outstanding: 0 blocking, 0 warnings, 3 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-06 |
| Status       | Draft      |
