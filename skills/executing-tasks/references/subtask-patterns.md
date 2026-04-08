<!-- version: 1.11 | author: chief-of-droids workspace | last_updated: 2026-04-08 -->

# Sub-Task Patterns

Read at Step 9 of the executing-tasks outer loop.

**Step 9:** For each sub-task from the Step 6 plan, run the inner loop defined
for the classified pattern. The inner loop runs within a single sub-task — it is
not the sub-task sequence itself. For the Test step, apply the **Inner-loop
checklist** for the classified pattern as the formal test gate.
All checklist items must pass before advancing to the next sub-task.

**TDD discipline in this file:**
Each pattern's Create tests step carries a State-0 reference — what "fail before
writing begins" looks like for that type. Each Write step carries a Green constraint —
restrict changes to the minimum required for the current owned QA row. Both
annotations encode the Red → Green discipline declared in SKILL.md Step 9.
The QA Row Ownership Table (produced at SKILL.md Step 8) is the authority for
which rows are owned by the current sub-task.

---

## Inner Loop QA Report

After all sub-tasks complete — before Step 10 — surface a structured report.

**Format:**

```
## Inner Loop QA Report — [pattern] sub-task [N]

Verification confidence impact: [agreed %] → [adjusted %]

| ID | Assertion | Severity | Result | Detail |
| :--- | :--- | :--- | :--- | :--- |
| XX | [assertion text] | Blocking / Major / Minor | ✅ Pass / ❌ Fail | — or failure detail |

Summary: [N] passed · [N] failed ([N] Blocking · [N] Major · [N] Minor)
```

**Severity definitions** (for inner-loop checklist items — numeric confidence impacts
defined in the Confidence Derivation Rule in `references/qa-schema.md`):

| Severity | Definition |
| :--- | :--- |
| Blocking | Failure makes the verification scenario untestable or meaningless |
| Major | Failure partially invalidates a verification scenario item |
| Minor | Quality gap — verification scenario remains valid |

---

## Pattern: research

**Scope:** Fetch, evaluate, score, survey, or assess external or internal sources.

### Inner loop

1. **Create tests** — define what a valid research output looks like:
   source reachable, content fetched, evaluation criteria applied, findings recorded.
   State-0 reference: the rows from the Step 8 ownership table assigned to this
   sub-task define the not-yet-started state — source not fetched, evaluation not
   applied. Record fail state (source absent / criteria not applied) per owned row
   before proceeding to Write.
2. **Write** — fetch source; extract relevant content; apply evaluation criteria.
   Green: fetch and evaluate only what is required to satisfy the current owned QA
   row. Advance to the next owned row only after the current row's assertion passes
   its Test step.
3. **Run** — confirm fetch succeeded; content non-empty; criteria applied to all items
4. **Test** — apply Inner-loop checklist (below) as the formal test gate
5. **Debug** — for failed fetches: retry with alternative URL or search query;
   for criteria failures: re-evaluate with explicit rationale; document exclusion if still failing
6. **Back to Write** if any Inner-loop checklist item fails

### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| R1 | All sources in scope were fetched or explicitly excluded | Blocking | Every source has a status | Any source has no status |
| R2 | Each included source has applied evaluation criteria with rationale | Major | Rationale present per source | Rating with no rationale |
| R3 | Excluded sources have documented exclusion reason | Major | Reason present | Silent exclusion |
| R4 | Findings are traceable to fetched content — not from memory | Blocking | Each finding references fetch result | Finding with no source attribution |

---

## Pattern: file-write

**Scope:** Write or overwrite a structured file (`.md`, config, schema).

### Inner loop

1. **Create tests** — define expected file properties:
   path, schema, row/section count, required fields, header format.
   State-0 reference: for each owned QA row, run `filesystem:read_text_file` on
   the target path and confirm the file is absent or does not yet satisfy the row's
   assertion. Record the observed state (file absent / field missing / schema
   non-conformant) per row before proceeding to Write.
2. **Write** — compose file content; write via Filesystem tool.
   Green: write only the minimum file content required to pass the current owned
   QA row. Do not pre-write content for future rows.
3. **Run** — read file back immediately via `filesystem:read_text_file`
4. **Test** — apply Inner-loop checklist (below) as the formal test gate
5. **Debug** — if read-back fails: retry write; if schema mismatch: fix content and rewrite;
   if row count wrong: diff draft vs written file
6. **Back to Write** if any Inner-loop checklist item fails

### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| F1 | File readable via `filesystem:read_text_file` immediately after write | Blocking | Read succeeds, content non-empty | Read fails or empty |
| F2 | Row/section count matches approved draft | Major | Counts match | Row dropped or duplicated |
| F3 | All required schema fields present | Major | All fields found | Any field missing |
| F4 | Header metadata (version, last_updated) reflects current date | Minor | Date correct | Stale or missing |
| F5 | No old-schema artefacts present | Major | Old fields absent | Old field found |

---

## Pattern: doc

**Scope:** Author or revise a structured document (guide, ADR, runbook, reference doc).

### Inner loop

1. **Create tests** — define document completeness criteria:
   required sections, mandatory content per section, format rules (from `writing-docs`).
   State-0 reference: for each owned QA row, record section-absent or content-absent
   as the fail state before drafting begins. No execution required — absence is the
   definitional fail state.
2. **Write** — draft document following `writing-docs` skill conventions.
   Green: draft only the sections or content blocks required for the current owned
   QA row. Do not speculatively draft sections for future rows.
3. **Run** — read draft; apply `writing-docs` QA checklist
4. **Test** — apply Inner-loop checklist (below) as the formal test gate
5. **Debug** — for missing sections: add; for formatting violations: fix per `writing-docs`;
   for intent drift: trim or expand to match confirmed intent
6. **Back to Write** if any Inner-loop checklist item fails

### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| D1 | All sections declared in plan are present | Blocking | All sections found | Any section missing |
| D2 | Content matches confirmed intent — no drift | Major | Content within confirmed intent boundary | Content outside confirmed intent |
| D3 | writing-docs QA checklist passes | Major | No open items | Open checklist items |
| D4 | File written and readable | Blocking | Read succeeds | Read fails |

---

## Pattern: code

**Scope:** Implement, refactor, or fix code in a repo.

### Inner loop

1. **Create tests** — write acceptance tests that define the expected behaviour
   before writing any implementation code (TDD: RED phase). Confirm all owned QA
   row tests fail against the current system before entering Write. State:
   `"State-0 confirmed for sub-task [N]: [M] rows fail as expected."` If any row
   passes before changes are made, surface as a State-0 anomaly and resolve with
   the user before proceeding.
2. **Write** — implement minimal code to pass the acceptance tests (GREEN phase).
   Green: implement only the minimum code required to pass the current failing test.
   Do not implement logic not demanded by the current red test. Advance to the next
   test only after the current one passes.
3. **Run** — execute tests; capture output
4. **Test** — apply Inner-loop checklist (below) as the formal test gate
5. **Debug** — for failing tests: read error; identify root cause; fix implementation only
   (do not modify tests to pass); re-run
6. **Back to Write** if any Inner-loop checklist item fails

### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| C1 | All acceptance tests pass | Blocking | Test suite green | Any test red |
| C2 | No existing tests broken (regression) | Blocking | Full suite green | Regression introduced |
| C3 | Implementation matches confirmed intent — no gold-plating | Major | Intent match | Out-of-scope code added |
| C4 | Code reviewed against `reviewing-tech-claims` if "verified" in confirmed intent | Major | Review complete | Review skipped |

---

## Pattern: skill-authoring

**Scope:** Author a new SKILL.md or enrich/critique an existing skill.
Delegates entirely to `creating-skills` for domain logic.

### Inner loop

Defer to `creating-skills` workflow (author / enrich / critique as applicable).
The executing-tasks inner loop wraps the creating-skills workflow as a single sub-task.

1. **Create tests** — design assessment mock requests (2–3 realistic triggers).
   State-0 reference: for each owned QA row, record SKILL.md absent or the specific
   criterion (section, trigger, reference file) absent as the fail state before
   the creating-skills workflow begins.
2. **Write** — run creating-skills workflow; produce SKILL.md + reference files.
   Green: produce only the SKILL.md content or reference file content required to
   pass the current owned QA row. Do not speculatively author sections for future rows.
3. **Run** — run mock requests against the draft
4. **Test** — apply Inner-loop checklist (below) as the formal test gate
5. **Debug** — for trigger failures: revise description; for checklist failures: fix per critique
6. **Back to Write** if any Inner-loop checklist item fails

### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| S1 | SKILL.md frontmatter valid — `name` and `description` present and well-formed; description is specific and trigger-inclusive. Note: the official Anthropic SKILL.md spec requires only `name` and `description`; any additional fields are workspace conventions | Major | name and description present and valid | name or description absent or vague |
| S2 | Assessment checklist (`creating-skills/references/assessment-checklist.md`) rating: Pass | Blocking | Pass | Partial or Fail |
| S3 | Mock requests trigger correctly (2–3 tested) — no partial-pass | Blocking | All trigger | Any miss |
| S4 | Reference files declared in SKILL.md are written and readable | Blocking | All files present | Any file missing |
| S5 | HOW-TO-TRIGGER.md updated | Major | Entry present | Entry missing |

---

## Pattern: framing

**Scope:** Build or challenge a FRAMING.md for a project or use case.
Delegates to `analyzing-business-cases` for domain logic.

### Inner loop

1. **Create tests** — define what a valid FRAMING.md output looks like:
   all 6 template sections present; all 7 challenge framing Blocking criteria met;
   advisory items surfaced and acknowledged by user.
   State-0 reference: for each owned QA row, record FRAMING.md absent or the required
   section absent / non-conformant as the fail state before drafting begins. No
   execution required — absence is the definitional fail state.
2. **Write** — run `analyzing-business-cases` workflow:
   - `build framing`: read `FRAMING-template.md`; scaffold FRAMING.md with user
   - `challenge framing` only: read existing FRAMING.md via filesystem tool.
   Green: draft only the FRAMING.md section(s) required for the current owned QA
   row. Do not speculatively draft sections for future rows.
3. **Run** — apply challenge framing sub-workflow:
   read `analyzing-business-cases/references/qa-checklist.md §challenge framing`;
   apply all Blocking and Advisory criteria to FRAMING.md content; record pass/fail per item
4. **Test** — apply Inner-loop checklist (below) as the formal test gate
5. **Debug** — for Blocking failures: read qa-checklist.md failure signal; propose
   targeted section edit; apply on explicit user confirmation; re-run challenge;
   never rewrite FRAMING.md without user instruction.
   For Advisory: surface all findings; do not block
6. **Back to Write** if any Inner-loop checklist item fails

### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| FR1 | FRAMING.md written and readable via `filesystem:read_text_file` | Blocking | Read succeeds, content non-empty | Read fails or empty |
| FR2 | All 6 FRAMING-template.md sections present: Context, Problem, Client, Objectives, Solution, Constraints | Blocking | All 6 section headers found | Any section missing |
| FR3 | All 7 challenge framing Blocking criteria pass (`qa-checklist.md §challenge framing`) | Blocking | All 7 pass | Any one fails |
| FR4 | All Advisory items from `qa-checklist.md §challenge framing` surfaced to user | Major | All advisory findings listed; user acknowledged | Advisory section skipped |
| FR5 | No FRAMING.md edit applied without explicit user confirmation | Major | All edits user-confirmed | Any unrequested rewrite |

---

## Compound Pattern: research + file-write

Apply research inner loop for all research sub-tasks.
When the research sub-task is complete, apply the file-write inner loop for the output file.
Inner-loop checklists R1–R4 and F1–F5 apply to their respective sub-tasks.


| Field        | Value       |
|--------------|-------------|
| Version      | 1.11        |
| Last Updated | 2026-04-08  |
| Status       | Draft       |
