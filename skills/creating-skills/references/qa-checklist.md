<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-04-06 -->

# QA Checklist — creating-skills

Governs: `creating-skills` skill
Format: table (Severity / Maps to / Item / Pass / Fail signal)
Placement: Unified — all workflows in one file; items grouped under workflow section headings
Branch-exclusive ratio: 17 of 38 items are workflow-specific (45%) — below 50% threshold; unified placement correct

---

## All Workflows

| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Blocking | Environment detection | Environment detected and reported before any other action | Detection result explicitly stated at top of workflow output | Workflow output produced without environment statement — halt and re-run Step 0 |
| Blocking | Reference file read | Step 0 probe file is `references/assessment-checklist.md` | assessment-checklist.md content loaded via filesystem read | Different file used for probe — surface misconfiguration and halt |
| Major | Reference file read | assessment-checklist.md reused from Step 0 result — not re-read in subsequent steps | No second filesystem read of assessment-checklist.md within the same workflow run | File re-read mid-workflow — flag redundant token cost |
| Blocking | Source mode routing | Correct source mode used per workflow: official sources (author/critique/assess) \| catalog pattern extraction (enrich) \| catalog coverage matching + session findings (recommend) \| own fetch protocol (add source) | Source mode matches the active workflow — no cross-contamination | Wrong source mode applied — halt, surface the correct mode for the active workflow |
| Blocking | Output write gate | No file written without user approval | Every filesystem write is preceded by explicit user confirmation in the same turn | File written before approval — surface write as unauthorised |

## author skill

| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Major | Official source fetch | All three official source fetches attempted — status reported explicitly | Fetch status for all three sources appears in output before any assessment | One or more sources not attempted — flag missing fetch, note reduced verification confidence |
| Major | Output quality | Findings cross-referenced against fetched official docs, not checklist alone | Assessment cites fetched source content, not only checklist items | Assessment references checklist only — flag as partially verified |
| Major | Output quality | Description field third person, trigger-inclusive, max 1024 chars | Drafted description is third-person, includes trigger phrases, ≤1024 chars | Violation present — flag specific field and return for correction |
| Major | Output quality | SKILL.md lean — no content that belongs in reference files | No bulk content (tables >10 rows, long workflows, large examples) inline in SKILL.md | Bulk content found inline — propose extraction to reference file |
| Major | Output quality | Test prompts proposed for new skills before writing | 2–3 realistic trigger prompts included in proposal | Test prompts absent — do not proceed to write without them |
| Blocking | Reference file read | qa-template.md read before QA checklist authored | qa-template.md filesystem read occurs before any QA item is drafted | QA checklist authored without reading template — halt QA authoring, read template first |
| Major | Output quality | QA checklist enumerated from hard gates, reference reads, writes, and failure conditions in the drafted skill | Each QA item traces to a specific element in the skill draft | Items present with no traceable source — remove or justify |
| Major | Output quality | Severity assigned per template definitions — no inflation | Blocking reserved for hard gates and silent failure risks; Major for quality/accuracy; Minor for style | Inflation detected — downgrade affected items and note reason |
| Major | Output quality | Placement decision rule applied — branch-exclusive ratio computed and stated before proposing | Ratio stated in checklist header; unified or split decision matches threshold | Ratio absent or decision does not match threshold — recompute and correct |
| Major | Output quality | Minimum coverage requirements verified before proposing checklist | All minimum Blocking items present per template requirements | Coverage gap — add missing items before proposing |
| Major | Hard gate | QA checklist proposed alongside skill draft — not after approval | Skill draft and QA checklist appear in the same proposal turn | QA checklist absent from proposal — do not request approval without it |
| Blocking | Output write gate | QA checklist file(s) written on approval, not before | Filesystem write of qa-checklist.md follows explicit user approval | File written before approval — surface as unauthorised |

## critique skill

| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Major | Official source fetch | All three official source fetches attempted — status reported explicitly | Fetch status for all three sources appears in output before any assessment | One or more sources not attempted — flag missing fetch, note reduced verification confidence |
| Major | Output quality | Findings cross-referenced against fetched official docs, not checklist alone | Assessment cites fetched source content, not only checklist items | Assessment references checklist only — flag as partially verified |

## assess all skills

| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Major | Official source fetch | All three official source fetches attempted — status reported explicitly | Fetch status for all three sources appears in output before any assessment | One or more sources not attempted — flag missing fetch, note reduced verification confidence |
| Major | Output quality | Findings cross-referenced against fetched official docs, not checklist alone | Assessment cites fetched source content, not only checklist items | Assessment references checklist only — flag as partially verified |
| Major | Path detection | Skills directory listed via filesystem tool — not enumerated from memory | Filesystem list_directory call present before skill loop begins | Skills enumerated from memory — halt, run filesystem list first |

## recommend skills

| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Major | Source mode routing | Step 0 run; Step 1 not run; skill-sources.md read for coverage matching | Step 0 output present; no official source fetch attempted; skill-sources.md read confirmed | Step 1 attempted — flag incorrect source mode for this workflow |
| Major | Output quality | Each recommendation states source catalog match and coverage delta vs. gap identified | Every recommendation row includes source match (or "no match") and coverage delta | Recommendation row missing match or delta — incomplete output, flag and complete |

## add source

| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Major | Source mode routing | Step 0 run; Step 1 not run; add-source.md workflow read and executed as written | Step 0 output present; no official source fetch attempted; add-source.md filesystem read confirmed | Step 1 attempted or add-source.md not read — flag and correct routing |
| Major | Hard gate | All three qualification criteria evaluated before any write | Criteria 1 (fetch), 2 (SKILL.md check), 3 (score threshold) all appear in output before write | Write attempted without completing all three criteria — halt, complete criteria first |
| Minor | Output quality | Rejected sources added to Exclusion Log with criterion and reason | Each rejected source appears in Exclusion Log with criterion number and one-line reason | Rejection not logged — add to Exclusion Log before closing workflow |
| Blocking | Output write gate | Write only on explicit user approval; read-back confirms write succeeded | Filesystem write follows explicit approval; read-back of skill-sources.md occurs in same turn | Write before approval or no read-back — surface as unauthorised or unverified |

## enrich skill

| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Major | Output quality | Steps labelled E1–E10 — no collision with global Step 0 / Step 1 | All enrich steps use E-prefix labels in output | Step labelled without E-prefix — rename to avoid collision |
| Major | Failure handling | E1 cap sets E2–E8 to `Skipped — filesystem unavailable` / Low | When E1 confidence is Low, all E2–E8 rows show `Skipped — filesystem unavailable` and `Low` | Cap not applied — surface missing cap and restate affected rows |
| Minor | Output quality | E3 cap names Environment Detection (E1) explicitly — not "Step 1" | E3 cap text references "E1" or "Environment Detection" — not "Step 1" | "Step 1" used in E3 cap — correct label to E1 |
| Major | Failure handling | E3 cap distinguishes filesystem-Low from external-URL-Low | E3 output separately states filesystem source status and external URL source status | Combined into single Low — split and restate per source type |
| Major | Output quality | E3 reports per-source table with SKILL.md count and content status | E3 output contains table with Source / SKILL.md count / Content returned / Confidence columns | Table absent or missing columns — regenerate E3 per template |
| Major | Output quality | SKILL.md count = 0 flags source as improper catalog entry for removal | Any source with SKILL.md count = 0 is explicitly flagged for removal from skill-sources.md | Count = 0 not flagged — surface removal recommendation |
| Major | Output quality | E2 row count compared against full file read row count — not a hardcoded number | E2 output states loaded row count vs. full-file row count as two distinct numbers | Hardcoded number used — restate using actual file read counts |
| Minor | Output quality | Skipped steps emit `Skipped — <reason>` and `Low` in confidence column | Each skipped step row contains `Skipped — <reason>` in Test result and `Low` in Confidence | Skipped step shows empty or dash — add required text |
| Major | Failure handling | E6 Low short-circuits E7 — E7 set to `Skipped — no candidates after filter` | When E6 confidence is Low, E7 row shows `Skipped — no candidates after filter` | E7 attempted after E6 Low — halt E7, apply short-circuit |
| Major | Output quality | E5 confidence rubric — Medium = ≥1 source zero patterns; Low = all sources zero patterns | E5 confidence matches rubric: Medium when ≥1 source yields zero patterns; Low when all sources yield zero | Confidence does not match rubric — correct to match |
| Minor | Output quality | E6 filter denominator is pre-filter candidate count — not source count | E6 ratio states `retained / pre-filter candidates` — not `retained / source count` | Source count used as denominator — restate with correct denominator |
| Major | Output quality | Confidence report emitted before awaiting approval | Confidence report table appears in output before any approval prompt | Approval requested without confidence report — emit report first |
| Major | Output quality | Gap and Enrichment Opportunity columns independently legible | Gap column alone conveys the deficiency without requiring the Opportunity column | Gap column requires Opportunity to be understood — rewrite Gap to be self-contained |
| Major | Output quality | Every High-priority row has a concrete proposal with named target file | Each High row includes a concrete edit with target file path | High row without proposal — draft proposal before surfacing |
| Major | Output write gate | Approved proposals written to declared target files; workflow complete on confirmed writes | Each approved proposal is written to the file named in its E8 proposal; write confirmed | Write to different file or write not confirmed — surface discrepancy |

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-04-06 |
| Status       | Active     |
