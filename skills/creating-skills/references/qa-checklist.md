<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-04-06 -->

# QA Checklist — creating-skills

Governs: `creating-skills` skill
Format: executing-tasks severity model (Blocking / Major / Minor)
Placement: Unified — all workflows in one file; branch-exclusive items carry inline workflow labels
Branch-exclusive ratio: 17 of 38 items are workflow-specific (45%) — below 50% threshold; unified placement correct

---

## All Workflows

- [ ] **Blocking** — Environment detected and reported before any other action — every workflow
- [ ] **Blocking** — Step 0 probe file is `references/assessment-checklist.md` — stable, workflow-neutral
- [ ] **Major** — assessment-checklist.md reused from Step 0 result — not re-read in subsequent steps
- [ ] **Blocking** — Correct source mode used per workflow: official sources (author/critique/assess) | catalog pattern extraction (enrich) | catalog coverage matching + session findings (recommend) | own fetch protocol (add source)
- [ ] **Blocking** — No file written without user approval

## author skill

- [ ] **Major** — All three official source fetches attempted — status reported explicitly
- [ ] **Major** — Findings cross-referenced against fetched official docs, not checklist alone
- [ ] **Major** — Description field third person, trigger-inclusive, max 1024 chars
- [ ] **Major** — SKILL.md lean — no content that belongs in reference files
- [ ] **Major** — Test prompts proposed for new skills before writing
- [ ] **Blocking** — qa-template.md read before QA checklist authored
- [ ] **Major** — QA checklist enumerated from hard gates, reference reads, writes, and failure conditions in the drafted skill
- [ ] **Major** — Severity assigned per template definitions — no inflation
- [ ] **Major** — Placement decision rule applied — branch-exclusive ratio computed and stated before proposing
- [ ] **Major** — Minimum coverage requirements verified before proposing checklist
- [ ] **Major** — QA checklist proposed alongside skill draft — not after approval
- [ ] **Blocking** — QA checklist file(s) written on approval, not before

## critique skill

- [ ] **Major** — All three official source fetches attempted — status reported explicitly
- [ ] **Major** — Findings cross-referenced against fetched official docs, not checklist alone

## assess all skills

- [ ] **Major** — All three official source fetches attempted — status reported explicitly
- [ ] **Major** — Findings cross-referenced against fetched official docs, not checklist alone
- [ ] **Major** — Skills directory listed via filesystem tool — not enumerated from memory

## recommend skills

- [ ] **Major** — Step 0 run; Step 1 not run; skill-sources.md read for coverage matching
- [ ] **Major** — Each recommendation states source catalog match and coverage delta vs. gap identified

## add source

- [ ] **Major** — Step 0 run; Step 1 not run; add-source.md workflow read and executed as written
- [ ] **Major** — All three qualification criteria evaluated before any write
- [ ] **Minor** — Rejected sources added to Exclusion Log with criterion and reason
- [ ] **Blocking** — Write only on explicit user approval; read-back confirms write succeeded

## enrich skill

- [ ] **Major** — Steps labelled E1–E10 — no collision with global Step 0 / Step 1
- [ ] **Major** — E1 cap sets E2–E8 to `Skipped — filesystem unavailable` / Low
- [ ] **Minor** — E3 cap names Environment Detection (E1) explicitly — not "Step 1"
- [ ] **Major** — E3 cap distinguishes filesystem-Low from external-URL-Low
- [ ] **Major** — E3 reports per-source table with SKILL.md count and content status
- [ ] **Major** — SKILL.md count = 0 flags source as improper catalog entry for removal
- [ ] **Major** — E2 row count compared against full file read row count — not a hardcoded number
- [ ] **Minor** — Skipped steps emit `Skipped — <reason>` and `Low` in confidence column
- [ ] **Major** — E6 Low short-circuits E7 — E7 set to `Skipped — no candidates after filter`
- [ ] **Major** — E5 confidence rubric — Medium = ≥1 source zero patterns; Low = all sources zero patterns
- [ ] **Minor** — E6 filter denominator is pre-filter candidate count — not source count
- [ ] **Major** — Confidence report emitted before awaiting approval
- [ ] **Major** — Gap and Enrichment Opportunity columns independently legible
- [ ] **Major** — Every High-priority row has a concrete proposal with named target file
- [ ] **Major** — Approved proposals written to declared target files; workflow complete on confirmed writes

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-04-06 |
| Status       | Active     |
