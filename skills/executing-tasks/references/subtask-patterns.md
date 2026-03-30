<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-03-30 -->

# Sub-Task Patterns

Read at Steps 5 and 7 of the executing-tasks outer loop.

Defines the inner execution loop and verify checklist for each task type.
Step 5 uses the verify checklist as the QA suite baseline.
Step 7 uses the inner loop for sub-task execution.

---

## Pattern: research

**Scope:** Fetch, evaluate, score, survey, or assess external or internal sources.

### Inner loop

1. **Create tests** — define what a valid research output looks like:
   source reachable, content fetched, evaluation criteria applied, findings recorded
2. **Write** — fetch source; extract relevant content; apply evaluation criteria
3. **Run** — confirm fetch succeeded; content non-empty; criteria applied to all items
4. **Test** — check each finding against test from step 1;
   flag any source that returned no content or failed the criteria gate
5. **Debug** — for failed fetches: retry with alternative URL or search query;
   for criteria failures: re-evaluate with explicit rationale; document exclusion if still failing
6. **Back to Write** if any source remains unresolved

### Verify checklist (QA suite baseline)

| ID | Assertion | Pass | Fail |
|:---|:----------|:-----|:-----|
| R1 | All sources in scope were fetched or explicitly excluded | Every source has a status | Any source has no status |
| R2 | Each included source has applied evaluation criteria with rationale | Rationale present per source | Rating with no rationale |
| R3 | Excluded sources have documented exclusion reason | Reason present | Silent exclusion |
| R4 | Findings are traceable to fetched content — not from memory | Each finding references fetch result | Finding with no source attribution |

---

## Pattern: file-write

**Scope:** Write or overwrite a structured file (`.md`, config, schema).

### Inner loop

1. **Create tests** — define expected file properties:
   path, schema, row/section count, required fields, header format
2. **Write** — compose file content; write via Filesystem tool
3. **Run** — read file back immediately via `filesystem:read_text_file`
4. **Test** — verify: file readable, content non-empty, schema matches, required fields present,
   row/section count matches draft
5. **Debug** — if read-back fails: retry write; if schema mismatch: fix content and rewrite;
   if row count wrong: diff draft vs written file
6. **Back to Write** if any test fails

### Verify checklist (QA suite baseline)

| ID | Assertion | Pass | Fail |
|:---|:----------|:-----|:-----|
| F1 | File readable via `filesystem:read_text_file` immediately after write | Read succeeds, content non-empty | Read fails or empty |
| F2 | Row/section count matches approved draft | Counts match | Row dropped or duplicated |
| F3 | All required schema fields present | All fields found | Any field missing |
| F4 | Header metadata (version, last_updated) reflects current date | Date matches 2026-03-30 | Stale or missing |
| F5 | No old-schema artefacts present | Old fields absent | Old field found |

---

## Pattern: doc

**Scope:** Author or revise a structured document (guide, ADR, runbook, reference doc).

### Inner loop

1. **Create tests** — define document completeness criteria:
   required sections, mandatory content per section, format rules (from `writing-docs`)
2. **Write** — draft document following `writing-docs` skill conventions
3. **Run** — read draft; apply `writing-docs` QA checklist
4. **Test** — verify all required sections present; no formatting violations;
   content matches scope from task entry
5. **Debug** — for missing sections: add; for formatting violations: fix per `writing-docs`;
   for scope drift: trim or expand to match task scope
6. **Back to Write** if QA checklist has open items

### Verify checklist (QA suite baseline)

| ID | Assertion | Pass | Fail |
|:---|:----------|:-----|:-----|
| D1 | All sections declared in plan are present | All sections found | Any section missing |
| D2 | Content matches task scope — no drift | Content within scope | Content outside scope |
| D3 | writing-docs QA checklist passes | No open items | Open checklist items |
| D4 | File written and readable | Read succeeds | Read fails |

---

## Pattern: code

**Scope:** Implement, refactor, or fix code in a repo.

### Inner loop

1. **Create tests** — write acceptance tests that define the expected behaviour
   before writing any implementation code (TDD: RED phase)
2. **Write** — implement minimal code to pass the acceptance tests (GREEN phase)
3. **Run** — execute tests; capture output
4. **Test** — all acceptance tests pass; no regressions in existing test suite
5. **Debug** — for failing tests: read error; identify root cause; fix implementation only
   (do not modify tests to pass); re-run
6. **Back to Write** if tests still fail after fix

### Verify checklist (QA suite baseline)

| ID | Assertion | Pass | Fail |
|:---|:----------|:-----|:-----|
| C1 | All acceptance tests pass | Test suite green | Any test red |
| C2 | No existing tests broken (regression) | Full suite green | Regression introduced |
| C3 | Implementation matches scope — no gold-plating | Scope match | Out-of-scope code added |
| C4 | Code reviewed against `reviewing-tech-claims` if "verified" in scope | Review complete | Review skipped |

---

## Pattern: skill-authoring

**Scope:** Author a new SKILL.md or enrich/critique an existing skill.
Delegates entirely to `creating-skills` for domain logic.

### Inner loop

Defer to `creating-skills` workflow (author / enrich / critique as applicable).
The executing-tasks inner loop wraps the creating-skills workflow as a single sub-task.

1. **Create tests** — design assessment mock requests (2–3 realistic triggers)
2. **Write** — run creating-skills workflow; produce SKILL.md + reference files
3. **Run** — run mock requests against the draft
4. **Test** — mock requests trigger correctly; assessment-checklist passes (Pass rating)
5. **Debug** — for trigger failures: revise description; for checklist failures: fix per critique
6. **Back to Write** if assessment rating is not Pass

### Verify checklist (QA suite baseline)

| ID | Assertion | Pass | Fail |
|:---|:----------|:-----|:-----|
| S1 | SKILL.md frontmatter valid (name, description, pushy, trigger-inclusive) | All fields valid | Any field invalid |
| S2 | Assessment checklist rating: Pass | Pass | Partial or Fail |
| S3 | Mock requests trigger correctly (2–3 tested) | All trigger | Any miss |
| S4 | Reference files declared in SKILL.md are written and readable | All files present | Any file missing |
| S5 | HOW-TO-TRIGGER.md updated | Entry present | Entry missing |

---

## Compound Pattern: research + file-write

Apply research inner loop for all research sub-tasks.
When research phase is complete, apply file-write inner loop for the output file.
QA suite combines R1–R4 and F1–F5.
