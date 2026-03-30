---
name: creating-skills
description: >
  Authors new SKILL.md files from scratch, critiques and improves existing
  SKILL.md files, assesses skills against Anthropic official best practices,
  recommends new skills from session findings, and enriches existing skills
  from catalog patterns. Use when asked to create, build, author, or define
  a new skill, improve or critique an existing skill, audit skills in the
  workspace, identify skill gaps from session history, or enrich an existing
  skill from external or internal sources.
  Triggers on: "author skill", "critique skill", "enrich skill", "assess all
  skills", "create a skill", "build a skill", "I need a skill", "new skill
  for", "recommend skills", "what skills should I add", "skill gaps from
  sessions", "what am I missing as skills", "what's missing from skill",
  "improve skill from catalog".
---
<!-- version: 2.4 | author: chief-of-droids workspace | last_updated: 2026-03-30 -->

# Creating Skills Skill

Authors, critiques, enriches, assesses, and recommends SKILL.md files against Anthropic official standards.

**Principle:** Never author, assess, or enrich from memory. Always fetch from authoritative
sources before producing output. Two fetch modes apply depending on workflow:
- `author`, `critique`, `assess all skills` — fetch the three Anthropic official sources (Step 1)
- `enrich skill` — fetch sources from the `skill-sources.md` catalog (internal + external)
- `recommend skills` — no source fetch; reads session findings only

Assessment checklist lives in `references/assessment-checklist.md` —
read it via filesystem tool before any critique or assessment run.

---

## Reference Files

- `references/assessment-checklist.md` — read before any author, critique, or assess workflow
- `references/skill-sources.md` — source catalog; read during enrich and recommend-skills workflows
- `references/workflows/recommend-skills.md` — full workflow for skill gap analysis from session findings

---

## Step 0 — Environment Detection (always first, every workflow)

Before any other action, determine which environment Claude is running in.

**Detection method:** Attempt to read `references/assessment-checklist.md` via Filesystem MCP tool.
- If the read succeeds → **Claude Desktop** — Filesystem MCP is active
- If the read fails or the tool is unavailable → **Claude.ai** — Filesystem MCP is absent

**Report the result explicitly at the start of every workflow run:**
- ✅ `Environment: Claude Desktop — filesystem reads and source fetches will be attempted`
- ⚠️ `Environment: Claude.ai — Filesystem MCP unavailable; filesystem reads and official source fetch blocked`

**If Claude.ai is detected:** all filesystem-dependent steps are capped at Low for the
remainder of the workflow. Surface this once at the top; do not repeat per step.

**Result reuse:** the `references/assessment-checklist.md` content read during Step 0 is
available in context for the remainder of the workflow. Workflows that require this file
(author, critique, assess all skills) must reuse this result — do not re-read the file.

Never skip this step. Never assume the environment from context or memory.

---

## Step 1 — Official Source Fetch (author / critique / assess all skills only)

Not used by `enrich skill` or `recommend skills` — those workflows have their own source protocols.

Attempt all three fetches after environment detection. Do not skip even if the
environment is known from a prior run in the same session.

1. `https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices`
2. `https://github.com/anthropics/skills/`
3. `https://agentskills.io/specification`

**Fetch outcomes:**

| Environment | Expected result | Action |
| :--- | :--- | :--- |
| Claude Desktop | All succeed | Proceed normally |
| Claude Desktop — one fails | Partial | Flag, proceed with remaining + local checklist |
| Claude Desktop — all fail | Full failure | Flag all, proceed with local checklist only |
| Claude.ai | All blocked | Surface platform restriction, proceed with local checklist only |

**Always surface fetch status before producing any output:**
- ✅ `Official sources fetched — assessment fully verified against live docs`
- ⚠️ `One or more sources failed — assessment partially verified; gaps noted`
- ⚠️ `All sources failed — assessment run against local checklist only`

A failed fetch is acceptable. A skipped fetch is not.
Never proceed from memory alone if both fetch and local checklist are unavailable.

---

## Workflow: author skill

Trigger: `author skill <n>` | "create a skill" | "build a skill for" | "I need a skill that" | "new skill for"

Steps:
1. Run Step 0 — Environment Detection; reuse `references/assessment-checklist.md` from Step 0 result
2. Run Step 1 — Official Source Fetch
3. Apply `references/assessment-checklist.md` from Step 0 result — do not re-read
4. Ask user: what does this skill do, when should it trigger, what are its
   inputs and outputs — one question, not a form
5. Draft SKILL.md using the canonical structure:
   - YAML frontmatter: `name` (lowercase, hyphens, max 64 chars), `description`
     (third person, trigger-inclusive, max 1024 chars, "pushy")
   - Body: principle statement, reference file declarations, workflows
   Apply rules from fetched official sources and checklist — not from memory
6. Run assessment-checklist against the draft before proposing it
7. Surface checklist gaps as open questions
8. Propose test prompts (2-3 realistic triggers) for manual validation
9. Await user approval before writing any file

Output: `skills/<n>/SKILL.md` written to filesystem (on approval only)

---

## Workflow: critique skill

Trigger: `critique skill <n>`

**Scope:** compliance assessment only — does not run catalog enrichment.
To identify enrichment opportunities, run `enrich skill <n>` separately.

Steps:
1. Run Step 0 — Environment Detection; reuse `references/assessment-checklist.md` from Step 0 result
2. Run Step 1 — Official Source Fetch
3. Apply `references/assessment-checklist.md` from Step 0 result — do not re-read
4. Read `skills/<n>/SKILL.md` and any files in `skills/<n>/references/`
5. Run assessment-checklist — section by section, cross-referenced against fetched official docs
6. Output structured critique: `issue | severity | recommendation`
7. Surface findings only — do not rewrite unless user requests (see step 8)
8. If user requests fixes: propose edits, await approval, then write

Output: structured critique in chat (no file write unless requested)

---

## Workflow: enrich skill

Trigger: `enrich skill <n>` | "what's missing from skill <n>" | "improve skill <n> from catalog"

**Scope:** catalog-driven enrichment only — does not run the assessment checklist.
To check structural compliance, run `critique skill <n>` separately.

**Note on preconditions:** No structural gate is enforced. If SKILL.md read reveals
obvious blocking issues (missing frontmatter, empty body), surface a one-line note:
"Structural issues detected — consider running `critique skill <n>` before enriching."
Then proceed.

**Step labelling:** enrich steps are prefixed E1–E10 to distinguish them from the
global Step 0 and Step 1 shared across all workflows.

Steps:

**E1. Environment Detection**
Run Step 0. Record environment and filesystem availability.
*Test:* Step 0 read of `references/assessment-checklist.md` succeeded or failed.
*Confidence:* `High` — read succeeded (Claude Desktop) | `Low` — read failed or tool unavailable (Claude.ai).
*Cap:* If Low → all subsequent filesystem-dependent steps are capped at Low. Surface once here;
do not repeat per step. Set E2–E8 test result to `Skipped — filesystem unavailable` and
confidence to `Low`. Skip to E9 (Confidence Report).

**E2. Read `references/skill-sources.md` — build source list**
Read `references/skill-sources.md` via filesystem tool.
*Test:* Count table rows in the loaded content and compare to table rows in the full file read.
*Confidence:* `High` — all rows loaded | `Medium` — partial read (row count in loaded content
less than row count in full file) | `Low` — file unreadable or empty.

**E3. Fetch each source and count SKILL.md files**
For each source in the catalog:
- URL entries: fetch via web_fetch; parse response to count SKILL.md files found
  (e.g. for GitHub repos, parse the directory listing in the fetched HTML)
- Filesystem path entries: list directory via filesystem tool; count SKILL.md files found

Aggregate internal filesystem sources into a single Workspace row.
SKILL.md count = 0 for any source means it is not a valid skill catalog entry —
flag it for removal from `skill-sources.md` regardless of its `Catalog` column value.

*Test:* Per source — content returned and non-empty; SKILL.md count recorded.
Aggregate workspace sources: ✅ all paths readable | ⚠️ some paths failed | ❌ all paths failed.

*Confidence:* `High` — all sources returned content | `Medium` — ≥1 failed, ≥1 succeeded | `Low` — all failed.

*Cap logic:*
- If E1 confidence is Low (filesystem unavailable) → filesystem path entries cannot be read;
  external URL fetches may still proceed. If all URLs also fail → E3 confidence is Low
  and enrichment cannot proceed — set E4–E8 test result to `Skipped — no sources available`,
  confidence to `Low`, and go to E9.
- If E1 confidence is High but all external URLs fail → E3 confidence is Low for external
  sources only; internal filesystem sources remain available. Flag external coverage as
  unavailable and continue with internal sources.

Report E3 as a per-source table:

```
E3. Source fetch results:

| Source | SKILL.md count | Content returned | Confidence |
|:-------|:---------------|:-----------------|:-----------|
| Anthropic Best Practices | <N> | ✅ / ❌ | High/Low |
| Anthropic GitHub Repo    | <N> | ✅ / ❌ | High/Low |
| AgentSkills Spec         | <N> | ✅ / ❌ | High/Low |
| Workspace (internal)     | <N> | ✅ / ⚠️ / ❌ | High/Medium/Low |

Sources with SKILL.md count = 0: flag as improper catalog entry — recommend removal from skill-sources.md.
Sources with Content returned = ❌: flag as unreachable — verify separately.

E3 overall confidence: <lowest per-source confidence>
```

**E4. Read skill files**
Read `skills/<n>/SKILL.md`. Then read each file declared in its Reference Files section.
*Test:* SKILL.md present and non-empty. For each declared reference file, confirm read succeeded.
List any declared-but-unread files explicitly.
*Confidence:* `High` — SKILL.md + all declared references read | `Medium` — SKILL.md read, ≥1 reference missing | `Low` — SKILL.md unreadable.

**E5. Pattern extraction**
For each successfully fetched source, identify patterns, trigger designs, workflow structures,
or reference file conventions not present in the skill.
*Test:* For each source that returned content, count distinct patterns extracted.
Flag any source that returned content but yielded zero patterns — extraction may have failed silently.
*Confidence:* `High` — ≥1 pattern extracted per source | `Medium` — ≥1 source yielded zero patterns despite returning content | `Low` — all sources yielded zero patterns.

**E6. Filter**
Exclude: patterns the skill deliberately omits (infer scope from `description` frontmatter field),
standard-knowledge content with no token-cost justification.
*Test:* Count candidates before filter (pre-filter count) and after filter (retained count).
If >80% of pre-filter candidates removed → flag: filter may be over-broad or `description`
field is too vague to anchor exclusions reliably. If `description` is too vague to anchor
exclusions, ask the user one scoping question before filtering — do not proceed with an
unanchored filter.
*Confidence:* `High` — filter removed <80% of pre-filter candidates, remaining items are scope-justified |
`Medium` — filter removed ≥80% of pre-filter candidates, scope anchor weak | `Low` — filter removed 100%.
*Short-circuit:* If E6 confidence is Low (zero candidates retained) → set E7 test result to
`Skipped — no candidates after filter`, E7 confidence to `Low`, and proceed directly to E8.

**E7. Output gap table**
Produce the enrichment table. Every row must populate all five columns.
*Test:* Verify all five columns populated per row. Any row with empty Gap or empty
Enrichment Opportunity is incomplete — fix before surfacing.
*Confidence:* `High` — all rows fully populated | `Medium` — ≥1 row has incomplete columns | `Low` — table empty.

```
Enrichment opportunities for skill: <n>
Sources scanned: <list with fetch status per source>

| Gap | Enrichment Opportunity | Source | Applies to | Priority |
|:----|:-----------------------|:-------|:-----------|:---------|
| <what is absent or broken, stated specifically> | <what to add or change> | <source name> | SKILL.md / references/x.md | High/Med/Low |
```

**Gap** and **Enrichment Opportunity** are independently legible — a reader
should understand the deficiency from Gap alone without reading the Opportunity column.

**E8. High-priority proposals**
For each High-priority row, propose a concrete edit: target file + proposed text.
A High-priority row without a concrete proposal is a workflow defect — do not surface it.
*Test:* Verify every High-priority row has a concrete proposal with a named target file.
Count High rows with proposals vs. total High rows.
*Confidence:* `High` — all High rows have concrete proposals | `Medium` — some High rows missing proposals | `Low` — no High rows or no proposals drafted.

**E9. Confidence Report**
Emit after E8, before awaiting approval.
Skipped steps (due to E1 or E3 cap, or E6 short-circuit): set Test result to
`Skipped — <reason>` and Confidence to `Low`.

```
Enrichment Confidence Report — skill: <n>

| Step | Test result | Confidence |
|:-----|:------------|:-----------|
| E1. Environment       | <Claude Desktop / Claude.ai> | High/Low |
| E2. Source list       | <N>/<full file row count> rows loaded | High/Medium/Low |
| E3. Source fetch      | see E3 per-source table above | High/Medium/Low |
| E4. Skill files       | SKILL.md + <N>/<declared total> references read | High/Medium/Low |
| E5. Pattern extraction| <N>/<source total> sources yielded ≥1 pattern | High/Medium/Low |
| E6. Filter            | <retained>/<pre-filter count> candidates retained (<pct>%) | High/Medium/Low |
| E7. Gap table         | <N> rows / <N> fully populated | High/Medium/Low |
| E8. Proposals         | <N>/<High row total> High rows have proposals | High/Medium/Low |

Overall: <lowest confidence across all steps>
Limiting factors: <steps that degraded from High, or "none">
Interpretation: <one sentence — what the overall rating means and whether a re-run is warranted>
```

**Overall** = lowest single-step confidence.
**Limiting factors** = steps that degraded below High.
**Interpretation** = actionable sentence on output reliability.

**E10. Await approval. On approval: write.**
Write approved proposals to their target files (SKILL.md or specific reference file
as declared in the High-priority proposal). One write per target file — batch all
approved changes to the same file into a single write operation.
Workflow is complete when all approved writes are confirmed.

Output: enrichment table + confidence report in chat. Approved proposals written to
target files declared in E8 (SKILL.md or `references/<file>.md` as applicable).

---

## Workflow: assess all skills

Trigger: `assess all skills`

Steps:
1. Run Step 0 — Environment Detection; reuse `references/assessment-checklist.md` from Step 0 result
2. Run Step 1 — Official Source Fetch
3. Apply `references/assessment-checklist.md` from Step 0 result — do not re-read
4. Use filesystem tool to list the `skills/` directory — do not enumerate from memory
5. For each skill: read SKILL.md, run checklist cross-referenced against fetched official docs
6. Output gap table: skill | issue | severity | recommendation
7. Overall summary: Pass / Partial / Fail per skill
8. Do not rewrite any skill — surface findings only
9. If user requests fixes on a specific skill: delegate to `critique skill <n>`

Output: gap table in chat (no file write)

---

## Workflow: recommend skills

Trigger: `recommend skills` | "what skills should I add" | "skill gaps from sessions" | "what am I missing as skills"

Full workflow in: `references/workflows/recommend-skills.md`

Summary:
1. Run Step 0 — Environment Detection
2. Read `references/workflows/recommend-skills.md` via filesystem tool
3. Read `references/skill-sources.md` via filesystem tool
4. Execute the workflow as written — do not paraphrase or abbreviate steps
5. Do NOT run Step 1 (official source fetch) for this workflow —
   the recommend-skills workflow is session-analysis based, not skill-authoring;
   fetching Anthropic docs is not relevant to gap extraction

Output: `.tasks/skill-recommendations/YYYY-MM-DD-recommend-skills.md`

---

## Composes With

| Skill | When |
| :--- | :--- |
| `writing-docs` | When authoring reference files or structured documentation alongside a new skill |

---

## QA Checklist

- [ ] Environment detected and reported before any other action — every workflow
- [ ] Step 0 probe file is `references/assessment-checklist.md` — stable, workflow-neutral
- [ ] assessment-checklist.md reused from Step 0 result — not re-read in subsequent steps
- [ ] Correct fetch mode used for workflow: official sources (author/critique/assess) vs. catalog (enrich)
- [ ] All three official source fetches attempted — status reported explicitly (author / critique / assess only)
- [ ] Findings cross-referenced against fetched official docs, not checklist alone
- [ ] Description field third person, trigger-inclusive, max 1024 chars
- [ ] SKILL.md lean — no content that belongs in reference files
- [ ] Test prompts proposed for new skills before writing
- [ ] No file written without user approval
- [ ] recommend skills: Step 0 run; Step 1 not run
- [ ] enrich workflow: steps labelled E1–E10 — no collision with global Step 0 / Step 1
- [ ] enrich workflow: E1 cap sets E2–E8 to `Skipped — filesystem unavailable` / Low
- [ ] enrich workflow: E3 cap names Environment Detection (E1) explicitly — not "Step 1"
- [ ] enrich workflow: E3 cap distinguishes filesystem-Low from external-URL-Low
- [ ] enrich workflow: E3 reports per-source table with SKILL.md count and content status
- [ ] enrich workflow: SKILL.md count = 0 flags source as improper catalog entry for removal
- [ ] enrich workflow: E2 row count compared against full file read row count — not a hardcoded number
- [ ] enrich workflow: skipped steps emit `Skipped — <reason>` and `Low` in confidence column
- [ ] enrich workflow: E6 Low short-circuits E7 — E7 set to `Skipped — no candidates after filter`
- [ ] enrich workflow: E5 confidence rubric — Medium = ≥1 source zero patterns; Low = all sources zero patterns
- [ ] enrich workflow: E6 filter denominator is pre-filter candidate count — not source count
- [ ] enrich workflow: confidence report emitted before awaiting approval
- [ ] enrich workflow: Gap and Enrichment Opportunity columns independently legible
- [ ] enrich workflow: every High-priority row has a concrete proposal with named target file
- [ ] enrich workflow: approved proposals written to declared target files; workflow complete on confirmed writes
