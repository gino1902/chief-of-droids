# Report — data-platform-v02

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    0     |     0      |
| Warning  |    19    |     12     |
| Info     |    5     |    N/A     |

## Phase 0 — Pre-flight

- [INFO] Slug `data-platform-v02` validated; `--type technical` validated; substrate `requirements/substrates/data-platform.md` resolved and readable.
- [INFO] CLAUDE.md found at `skills-lab/CLAUDE.md`; output directory `requirements/data-platform-v02/` created.
- [INFO] No prior `data-platform-v02-requirements.md` present → fresh pass; initial version `0.1`.
- [INFO] A sibling `requirements/data-platform-v01/` exists under a different slug. Per stateless iteration model, it is not consulted for ID stability or version increment.
- [INFO] Substrate IDs (`F1..F20`, `G1..G4`, `O1..O6`, `NFR1..NFR10`) do not match the canonical stability regex `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b`. All output IDs newly assigned.

Outstanding: 0 blocking, 0 warnings, 5 info

## Phase 1 — Framing

- [WARNING] Purpose paragraph inferred from substrate prose; substrate has no explicit "The purpose of…" / "This component…" statement → user review required.
- [WARNING] Out of Scope subsection rendered `N/A` — substrate provides no negation signals ("not handled", "outside this", "out of scope", etc.). Multiple TBD markers (F8, F17, NFR1, NFR2, NFR6, NFR7) flag deferred items, not exclusions.
- [WARNING] Actors table lists abstract roles only — substrate does not enumerate concrete subsystem identities, operator personas, or business-user roles. Rows labelled with abstract role names; refine in design phase.

Outstanding: 0 blocking, 3 warnings, 0 info

## Phase 2 — Drafting

- [INFO] Distribution: FR×17 · CON×7 · IR-IN×4 · IR-OUT×4 · DR×0 (N/A) · TR×0 (N/A) · NFR×8 · SEC×4 · ERR×2 · OBS×5 — 51 requirements total.
- [WARNING] FR-005 reformulated from substrate F5 — substrate phrased consumer-side behavior ("Consuming subsystems pull… only the data required by their workflows"); FR scope is the System's behavior. Statement rewritten as a System-side exposure obligation.
- [WARNING] FR-010 reformulated from substrate F10 — same rationale (producer-side language → System-side acceptance behavior).
- [WARNING] FR-011 / FR-012 split from substrate F11 (compound: "retains data for 7 days, after which it is automatically erased").
- [WARNING] FR-008 carries deferred caveat — substrate notes "use cases to be defined in the future"; exposure obligation rendered, downstream use-case enumeration deferred.
- [WARNING] FR-014 — same deferred-use-case caveat as FR-008.
- [WARNING] §7 Data Requirements (DR) rendered `N/A` — substrate provides no field-level data model.
- [WARNING] §7 Transformation Requirements (TR) rendered `N/A` — substrate references existence of transformation (F7) but specifies no input → rule → output mapping.
- [WARNING] NFR-001..NFR-005 carry `Measurement: TBD` — substrate explicitly defers retry policy (NFR1), dead-letter policy (NFR2), availability target (NFR3), SLA targets (NFR6), and SLO targets (NFR7).
- [WARNING] Substrate F12 (compliance with retention policy) routed to CON-001 — compliance constraint, not a measurable quality attribute.
- [WARNING] Substrate F13–F15, F18–F19, NFR5 routed to §Constraints — non-functional but constraint-shaped (single-producer rule, single-contract rule, contract ownership, quality accountability, classification compliance, GDPR/SQLI security policy compliance).
- [WARNING] Substrate G3, G4, NFR4, O6 routed to §Security — access-control, encryption, and leakage-prevention obligations.

Outstanding: 0 blocking, 11 warnings, 1 info

## Phase 3 — Vocabulary

- [INFO] §Glossary contains 41 substrate-sourced entries (preserved verbatim where possible; some descriptions condensed for readability).
- [WARNING] 15 auto-derived glossary entries added (status `auto-derived — verify`): `Authorised operator`, `Authorised subsystem`, `Authorised external end-user`, `Producing subsystem`, `Consuming subsystem`, `Source subsystem`, `Business-ready data`, `Business workflow`, `Unit & Department`, `SQLI data retention policy`, `SQLI data security policy`, `SQLI data access policy`, `SQLI user access policy`, `SQLI data classification policy`, `SQLI audit policy`. User review required.

Outstanding: 0 blocking, 1 warning (covering 15 entries), 1 info

## Phase 4 — Taxonomy hygiene

Common checks:

- [INFO] All IDs match `<CAT>-NNN` format with valid category prefixes.
- [INFO] Sequences are dense per category (no gaps): FR 001..017, CON 001..007, IR-IN 001..004, IR-OUT 001..004, NFR 001..008, SEC 001..004, ERR 001..002, OBS 001..005.
- [INFO] No duplicate IDs within any category.
- [INFO] Glossary covers all domain-specific terms used in requirements (39 substrate + 15 auto-derived). Common terms (data, system, request, payload-size, day, etc.) exempt.

T1 (EARS) checks — FR / CON / ERR:

- [INFO] All FR / CON entries use a legal EARS pattern (Ubiquitous or Event-driven).
- [INFO] All ERR entries use Unwanted Behavior EARS exclusively.
- [INFO] Both ERR entries carry a `→ FR-NNN` cross-link to an existing FR.
- [INFO] All FR / CON / ERR entries contain exactly one `SHALL`.
- [INFO] No RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) appear inside EARS statements.
- [WARNING] Coverage: most FRs lack a corresponding ERR. Substrate defines explicit error handling only for pull failure (NFR1 → ERR-001) and dead-letter (NFR2 → ERR-002). FR-001, FR-004..FR-005, FR-007..FR-017 have no ERR counterpart. Acceptable at this maturity level; expand in design phase.

T2 (RFC 2119) checks — IR / NFR / SEC / OBS:

- [INFO] Each IR / NFR / SEC / OBS entry contains at least one RFC 2119 keyword (or, for IR-IN-002 / IR-IN-004, an Event-driven EARS construction explicitly permitted by the IR drafting rules).
- [INFO] Every NFR contains a Measurement field.
- [WARNING] NFR-001..NFR-005 Measurement field is `TBD` — flagged per the bounded-NFR heuristic. Quantitative thresholds required for design-phase closure.
- [INFO] EARS `SHALL` does not appear in pure RFC 2119 statements (IR-IN-001, IR-IN-003, IR-OUT-001..004, all NFRs, SEC-001..003, all OBS).
- [INFO] IR-IN and IR-OUT sub-sections both rendered with at least one entry each.

T3 / T4 (DR / TR) checks:

- [WARNING] DR sub-section rendered `N/A` — substrate provides no field-level data model. Hygiene checks (column completeness, no RFC 2119 / EARS in tables) skipped — no entries.
- [WARNING] TR sub-section rendered `N/A` — substrate provides no transformation rule mapping. Hygiene checks skipped.

Outstanding: 0 blocking, 4 warnings, 9 info

## Phase 5 — Verification

- [INFO] Acceptance Criteria derived for all 51 requirements; multi-AC for FR-008 and FR-014 where substrate "use cases TBD" caveat warranted an explicit `N/A for completeness` AC alongside the obligation-side AC.
- [WARNING] Acceptance criteria for NFR-001..NFR-005 explicitly carry "Quantitative thresholds: TBD" — confirms ✗ on Bounded for those rows in the scorecard.

Quality scorecard summary:

| Category | Atomic ✓ | Unambiguous ✓ | Verifiable ✓ | Traceable ✓ | Bounded ✓ | Bounded ✗ | Bounded N/A |
|:---------|:--------:|:-------------:|:------------:|:-----------:|:---------:|:---------:|:-----------:|
| FR (17)        |   17   |     17     |     17     |    17    |    —    |    —    |    17    |
| IR-IN (4)      |    4   |      4     |      4     |     4    |    —    |    —    |     4    |
| IR-OUT (4)     |    4   |      4     |      4     |     4    |    —    |    —    |     4    |
| NFR (8)        |    8   |      8     |      8     |     8    |    3    |    5    |    —     |
| SEC (4)        |    4   |      4     |      4     |     4    |    —    |    —    |     4    |
| CON (7)        |    7   |      7     |      7     |     7    |    —    |    —    |     7    |
| ERR (2)        |    2   |      2     |      2     |     2    |    —    |    —    |     2    |
| OBS (5)        |    5   |      5     |      5     |     5    |    —    |    —    |     5    |
| **Total (51)** | **51** |   **51**   |   **51**   |  **51**  |  **3**  |  **5**  |  **43**  |

- [INFO] All 51 requirements pass Atomic, Unambiguous, Verifiable, Traceable.
- [WARNING] 5 NFRs (NFR-001..NFR-005) fail Bounded due to substrate-explicit TBD measurements.

Outstanding: 0 blocking, 6 warnings (5 NFR Bounded ✗ + 1 AC TBD note), 1 info

## Phase 6 — Format

- [INFO] Format pass applied; section order, heading levels, table syntax, and EARS / RFC 2119 mode per section conform to template-s2.
- [INFO] Version block appended; values: `0.1` / `2026-05-07` / `Draft`.
- [INFO] Write order: requirements file first, report file second. Both writes completed.

Outstanding: 0 blocking, 0 warnings, 3 info

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.1        |
| Last Updated | 2026-05-07 |
| Status       | Draft      |
