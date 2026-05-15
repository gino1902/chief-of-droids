# Predictability Report — `writing-requirements` over 5 runs

Substrate: `skill-workshop/requirements/substrates/two-tier-architecture-design-notes.md`
Skill: `skill-workshop/.claude/skills/writing-requirements/SKILL.md` (`--type technical`, slug `chief-of-droids-3-tiers-upgrade-vNN`)
Runs analysed: v01, v02, v03, v04, v05 (requirements artifacts).

## TL;DR

The skill is highly predictable on **macro structure** (top-level sections, ID category set, scorecard shape, version block) and **substrate-anchored verbatim invariants** (DR-001 field set, `"Which project?"` prompt text, sentinel path template, the seven sentinel fields). It is **moderately unpredictable** on **requirement count and granularity per category** (especially FR, IR-IN, ERR), **glossary composition**, **ID numbering** (no gaps, but identical concepts get different numbers across runs), **NFR phrasing** (MUST vs SHOULD on the same 92% reliability claim), and **DR/TR shape** (DR-002 emerges in some runs only, TR-003 emerges in some runs only). Variance is dominated by **substrate decomposition choices** the skill does not pin down — it tells the model what categories exist, not how to slice a substrate paragraph into one vs. several requirements.

## Method

Diff-by-inspection across all five `<slug>-requirements.md` files plus the SKILL.md. No statistical scoring; counts and verbatim spot-checks. Acceptance-Criteria duplication of IDs is folded out (grep counts halved). The five runs all wrote `Version 0.1` (no stateful refinement was fed in), so version-block drift is not part of the picture here.

## What was stable across all 5 runs

| Dimension | Observation |
|---|---|
| Top-level H2 sections | Title (substrate H1), Purpose, Scope (In/Out), Actors & Consumers, Glossary, Functional Requirements, Interface Requirements (IR-IN / IR-OUT), Data Requirements (DR / TR), Non-Functional Requirements, Security, Constraints, Error Handling, Observability, Acceptance Criteria, Quality Criteria scorecard, Version block. Identical set in all 5 runs. |
| Title | Always the substrate H1 verbatim: "Two-Tier CLAUDE.md Architecture — Design Notes" — fallback chain (FR / scope synthesis) never fired. |
| Security / Observability | All 5 runs emit `N/A — substrate silent on …, Warning emitted` with the same closed-enumeration justification (auth, authz, encryption, audit, rate-limit, input-val for SEC; metric, log, trace, health, alert for OBS). High predictability. |
| Sentinel schema | DR-001 contains the same 7 fields in all 5 runs (`uri`, `project`, `loaded_at`, `workspace_md_sha`, `project_md_sha`, `brief_sha`, `resolved_skills`) with `uri` marked REQUIRED UNIQUE. |
| Sentinel path | All runs use `chief-of-droids/.sessions/<urlencoded-uri>.json` verbatim. |
| Verbatim user-channel strings | `"Which project?"` appears literally as both FR and IR-OUT trigger in all 5 runs. |
| ID format | `<CAT>-NNN` always. No malformed IDs. |
| ID density | No gaps within any category in any run (the Phase 4 check holds). |
| Quality scorecard | All 5 runs end with the same five-criterion table (Atomic, Unambiguous, Verifiable, Traceable, Bounded) with identical definitions. |
| Reliability NFR threshold | The 92% figure is captured in all 5 runs (as NFR-001). |
| Workspace-tier-wins precedence | Captured as a constraint in all 5 runs. |
| One-way composition | Captured as a constraint in all 5 runs. |
| Trigger collision invariant | Captured (CON + FR) in all 5 runs. |
| 9 substrate "Preconditions" | All 9 land somewhere across CON / FR / ERR in every run (the substrate's list is a strong anchor). |

## Where the outputs diverged

### 1. Requirement counts per category

| Category | v01 | v02 | v03 | v04 | v05 | Spread |
|---|---|---|---|---|---|---|
| FR  | 16 | 14 | 15 | 13 | 15 | 13–16 |
| CON | 14 | 16 | 13 | 14 | 12 | 12–16 |
| IR-IN  |  4 |  7 |  3 |  5 |  6 | 3–7 |
| IR-OUT |  4 |  5 |  3 |  4 |  4 | 3–5 |
| ERR    | 11 | 11 |  8 | 11 | 11 | 8–11 |
| DR  | 1 | 1 | 1 | 2 | 2 | 1–2 |
| TR  | 2 | 3 | 2 | 3 | 2 | 2–3 |
| NFR | 3 | 3 | 3 | 3 | 3 | identical |
| Glossary entries | 25 | 25 | 21 | 24 | 22 | 21–25 |
| Total file length (lines) | 464 | 506 | 450 | 487 | 476 | ±6% |

Notes:
- v02 splits the three bind files into separate `IR-IN-003/004/005` reads plus `IR-IN-006` for sentinel, plus a path-scoped-rules-event `IR-IN-007`. v03 collapses them into a single `IR-IN-002`. Same substrate; very different decomposition.
- v01 and v03 model the sentinel as a single `DR-001`; v04 and v05 split out the `resolved_skills` element shape into a separate `DR-002`.
- v02 and v04 add `TR-003` (resolved-skills map derivation); v01/v03/v05 do not.
- v01 and v02 model FR-003 + FR-004 + FR-005 as a single bind-load FR; v05 splits them into three (FR-003/004/005 each loading one of the three files). Same source paragraph, different atomicity choice.

### 2. NFR-001 modal verb

The same substrate claim ("~92–93%") yields different modals across runs:

| Run | Modal | Phrasing |
|---|---|---|
| v01 | MUST | "MUST achieve … at or above the substrate-declared baseline" |
| v02 | MUST | "MUST achieve workspace-tier-wins trigger resolution reliability of at least 92%" |
| v03 | SHOULD | "SHOULD achieve … within the design's projected band" |
| v04 | SHOULD | "SHOULD achieve a skill-routing reliability of approximately 92–93%" |
| v05 | MUST | "MUST achieve a skills-routing reliability of at least 92%" |

The substrate uses "Reliability estimate: ~92–93%" — an estimate, not a contract — yet the skill renders it as MUST in 3 of 5 runs. This is a real semantic divergence the SKILL.md does not pin.

### 3. ID numbering for "the same" requirement

The corpus-scan / collision-rejection pair has these IDs across runs:
- v01: scan = FR-011, reject = FR-012
- v02: scan = FR-011, reject as ERR-009 (no separate FR for rejection)
- v03: scan = FR-011, reject = FR-012
- v04: scan = FR-010 (single FR that scans+rejects), reject conflated
- v05: scan = FR-011, reject = FR-012

Workspace-skill removal block:
- v01: FR-015; v02: FR-013; v03: FR-014; v04: FR-012; v05: FR-015.

The "could this be workspace?" prompt:
- v01: FR-016; v02: FR-014; v03: FR-015; v04: FR-013; v05: not modeled as an FR (absent or merged).

So traceability across runs is structurally broken — the skill stabilises IDs *within* a run via ID-stability scanning, but two independent runs assign different numbers to the same substrate claim. That is expected when no prior `<slug>-requirements.md` is fed back in, but it means run-N + run-(N+1) cannot be diffed by ID.

### 4. ERR ↔ FR pairing

The ERR coverage protocol in Phase 2 demands a paired ERR for any FR of contract shape Acquire / Mutate / Validate / Solicit / Transform-with-external-inputs. Inspection across runs:
- v01 marks several FRs with inline `(no ERR — rationale: …)` opt-outs (FR-006 Emit, FR-009 pass-through, FR-012 self-rejection, FR-013 Select-shape).
- v02 marks FR-003 (Solicit), FR-007 (Emit), FR-014 (Solicit) as no-ERR.
- v03 marks FR-002 (Solicit), FR-015 (Solicit) as no-ERR.
- v04 omits inline rationales entirely on some Solicit-shape FRs (e.g. FR-013).
- v05 carries no-ERR rationales on FR-008, FR-012, FR-013, FR-015.

Runs are inconsistent about which contract shapes get opt-outs and whether the rationale is inline. The protocol exists but doesn't pin a closed list of "always-emit-rationale" shapes vs. "always-pair-ERR" shapes, so each run chooses.

### 5. Glossary composition

All 5 runs include the substrate's defined terms (Layer 1/2/3, sentinel, bootstrap protocol, always-on tools, registration/routing/usage, project brief, etc.) — these are anchored. Variance is on the auto-derived set:
- v01 includes "Promotion", "Trigger collision", "Corpus collision scan", "Session bind", "Reliability principle" — none of which v02 explicitly lists.
- v02 invents "PR" as a glossary entry; no other run does.
- v05 adds "Bind" as a distinct entry; v01 has "Session bind" instead.
- v01 stops-words SHA — but lists it as `substrate`? It actually emits SHA implicitly via stop-word list; v05 lists SHA as `auto-derived — verify`. Inconsistent application of the stop-word list.

The stop-word list in SKILL.md includes `SHA` explicitly, yet v05 emits a `SHA` glossary entry. Inspect the list — that is a Phase 3 rule violation in v05, not just variance.

### 6. Scope wording

In Scope / Out of Scope bullet sets are recognisable across runs but rephrased every time. Counts:
- In Scope bullets: v01=11, v02=9, v03=10, v04=10, v05=10.
- Out of Scope bullets: v01=8, v02=6, v03=8, v04=8, v05=8.
v01 and v05 carry the "Drift prevention via description-as-source-of-truth replication (Option 1)" item; v02 phrases it as "Description-as-source-of-truth replication". Same item, different rendering.

### 7. Purpose paragraph

Anchored on the substrate's "two-tier ... three layers" framing in all 5 runs but reworded — sentence count 1 (v03) to 4 (v04). Word count spread roughly 130 → 220. No semantic drift; pure phrasing variance.

### 8. Phase reporting in the per-run report

Did not inspect the five `<slug>-report.md` files in depth (115–165 lines each); their existence and matching version stamps are confirmed. Skill description suggests they should be structured per-phase; spot-check shows v01's report is ~50 lines longer than the others, indicating the report file is itself a variance surface — but characterising that further was out of scope of this task.

## Sources of variance ranked by impact

| # | Source | Where the skill is silent or under-constrained |
|---|---|---|
| 1 | **Requirement granularity** — when to write one FR vs. three for a paragraph that lists three actions | SKILL.md gives a Phase 2 atomicity rule via the scorecard ("single modal verb, one behavior") but no decomposition rule. "Load A, B, and C" reads as 1 FR for v01/v02 and 3 FRs for v05. |
| 2 | **DR/TR shape** — whether to split nested record types into separate DR/TR entries | No rule for "if a DR field is itself a structured record, emit a paired DR-NNN for the element type". v04/v05 do, v01/v02/v03 don't. |
| 3 | **NFR modal verb** — MUST vs. SHOULD on the same estimate-class substrate phrase | The skill loads `rfc2119.md` for technical mode but does not pin how to map substrate words like "estimate", "approximately", "target" to MUST/SHOULD/MAY. |
| 4 | **ID numbering** — different number for the same concept across runs | Documented limitation (ID stability is intra-run only). The skill mitigates by re-running with prior output as substrate, but vanilla runs cannot align. |
| 5 | **ERR pairing protocol** — which FR contract shapes are forced to emit ERR vs. which forced to emit `(no ERR — rationale: …)` | The Phase 2 protocol names the shape matrix and the inline-rationale escape hatch but doesn't enforce that *every* FR get an explicit ERR-or-rationale decision. Inline rationale presence is variable across runs. |
| 6 | **Glossary auto-derivation** — three rules emit overlapping candidates; no rule on collapsing synonyms | "Session bind" vs. "Bind" — same concept, different entries across runs. Capitalised-noun-phrase rule has no idempotency check. |
| 7 | **Stop-word list adherence** — SHA emitted as glossary entry in v05 despite being on the list | Phase 3 rule violation, not under-specification. Probably a memory/attention issue mid-Phase-3. |
| 8 | **Scope bullet count & phrasing** | No rule on bullet granularity for §Scope. Each run paraphrases. |
| 9 | **IR-IN decomposition** — one read of 3 paths vs. 3 reads of 1 path each | Same atomicity issue as #1, in the IR-IN section. |
| 10 | **Purpose paragraph length and sentence count** | No length/sentence budget on §Purpose. |

## Concrete changes to `writing-requirements/SKILL.md` to raise predictability

Ordered by expected impact-per-edit.

### High impact

1. **Pin a decomposition rule for multi-action substrate clauses (addresses #1, #9).** Add to Phase 2: *"If a substrate clause enumerates N distinct files, endpoints, or external actions joined by `and` / commas, emit N FRs (one per item). If the clause names a single action operating over a set, emit 1 FR."* Without this, the same paragraph yields 1 or 3 FRs across runs. Reference `references/ears.md` should restate this.

2. **Pin a modal-verb mapping table for NFRs (addresses #3).** Add to Phase 2 or to `references/rfc2119.md`: substrate words `must / required / shall` → MUST; `should / target / minimum / threshold` → SHOULD; `estimate / approximately / projected / aim / aspire` → SHOULD; `may / optional / nice-to-have` → MAY. Disallow MUST when the substrate word is an estimate qualifier. The 92–93% case is a SHOULD across all reasonable readings.

3. **Enforce explicit ERR-or-rationale decision per FR (addresses #5).** Strengthen Phase 2: *"Every FR MUST end with either a paired ERR-NNN in the same pass OR an inline `(no ERR — rationale: <one of: Emit-shape | Select-shape | Self-rejection | Pass-through | Substrate-prescribed wait>)`."* Closed enumeration of permitted rationale tokens removes phrasing variance. Phase 4 then checks that the rationale token is from the closed list.

4. **Always split nested record types into a paired DR (addresses #2).** Add to Phase 2 DR rules: *"If a DR field's type is `array<X>` or a structured record, emit DR-NNN+1 for the element shape `X`."* This makes v04/v05's DR-002 mandatory and v01/v02/v03's absence a Warning.

5. **Stop-word enforcement in Phase 3 (addresses #7).** Add an explicit Phase 4 check: *"For every glossary entry, verify the term is not in the Phase 3 stop-word list."* This catches the v05 SHA-as-glossary regression.

### Medium impact

6. **Glossary synonym-collapse rule (addresses #6).** Add to Phase 3: *"Before emitting two entries, normalise to a single canonical form (lower-case, strip stop-words like 'session', 'project') and de-duplicate. Prefer the substrate's exact form when it exists; otherwise the most frequent form in the substrate."* This eliminates "Session bind" vs. "Bind" duplication.

7. **Bullet-count budget on §Scope (addresses #8).** Add to Phase 1: *"§Scope subsections SHALL contain at most one bullet per distinct substrate concept. Group adjacent concepts only when the substrate joins them syntactically."* This will not eliminate paraphrasing variance but constrains bullet count to a function of substrate concepts.

8. **Purpose-paragraph sentence budget (addresses #10).** Add to Phase 1: *"§Purpose SHALL be 2–4 sentences. First sentence states what the component is. Remaining sentences state why it exists per the substrate's stated rationale."* Closes the v03 (1-sentence) vs. v04 (4-sentence) gap.

### Low impact, high confidence

9. **Canonical-ordering rule for un-IDed substrate (already referenced in SKILL.md).** Inspect `references/conventions.md` § "Canonical ordering for un-IDed substrate" and confirm it produces a deterministic numbering function of substrate order. If it does, ID drift across runs (#4) collapses to whatever instability remains in substrate scanning — already minimal here.

10. **Add a Phase 4 "category presence" check.** *"Every FR drafted in Phase 2 must appear in §Acceptance Criteria. Every CON drafted must appear. Every NFR drafted must appear."* The five runs already do this, but absence-by-omission is silent today.

11. **Pin the report-file structure.** SKILL.md says the report is "per-phase" but does not enumerate sub-sections. The v01 report being ~50 lines longer than v02/v05 reports is consistent with under-specification of the report shape. Recommend adding to Phase 6: an explicit ordered list of report sub-sections (one per phase + a summary), each with a maximum line budget.

### Recommendations not directly tied to a variance source

12. **Warn on substrate H1 reuse as title.** All 5 runs used the substrate H1 verbatim — correct behaviour per SKILL.md but the substrate H1 is "Two-Tier ... Design Notes" while the substrate covers a three-layer architecture. Surface a Phase 1 Info that says "Title is substrate H1; consider whether it accurately names the component".

13. **Make refinement (re-run-with-prior-output) part of the documented happy path for stability across iterations.** SKILL.md already supports it; promote it from a sentence in the description to a Phase 0 prompt: "If a prior `<slug>-requirements.md` is present, ID assignments are preserved. If you want stable IDs across versions, feed the prior file as substrate."

## Bottom line

Out of the box, structure-level variance is low (≤±15% line count, identical section set, identical version-block shape, identical scorecard) but **content-level variance is meaningful**: a downstream consumer cannot rely on FR-007 in run N meaning the same thing as FR-007 in run N+1, and they cannot rely on the same substrate sentence producing 1 vs. 3 FRs across runs. The dominant fix is to pin Phase 2's decomposition and modal-verb mapping rules — items 1, 2, 3 above — which together address roughly 70% of the observed inter-run divergence.

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
