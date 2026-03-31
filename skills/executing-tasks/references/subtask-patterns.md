<!-- version: 1.3 | author: chief-of-droids workspace | last_updated: 2026-03-31 -->

# Sub-Task Patterns

Read at Step 7 of the executing-tasks outer loop.

**Step 7:** For each sub-task, use the inner loop for execution. For the Test step,
apply the **Inner-loop checklist** for the classified pattern as the formal test gate.
All checklist items must pass before advancing to the next sub-task.

---

## Inner Loop QA Report

After all sub-tasks complete — before Step 8 — surface a structured report.

**Format:**

```
## Inner Loop QA Report — [pattern] sub-task [N]

Verification confidence impact: [agreed %] → [adjusted %]

| ID | Assertion | Severity | Result | Detail |
| :--- | :--- | :--- | :--- | :--- |
| XX | [assertion text] | Blocking / Major / Minor | ✅ Pass / ❌ Fail | — or failure detail |

Summary: [N] passed · [N] failed ([N] Blocking · [N] Major · [N] Minor)
```

**Severity definitions:**

| Severity | Definition | Confidence impact |
| :--- | :--- | :--- |
| Blocking | Failure makes the verification scenario untestable or meaningless | Drops to 0% |
| Major | Failure partially invalidates a verification scenario item | Drops 20–40% per item |
| Minor | Quality gap — verification scenario remains valid | Drops <10% per item |

**Behaviour rule:**

- Always surface the report after sub-tasks complete
- All passed → proceed to Step 8 automatically
- Any failure → surface report, state adjusted confidence %, wait for explicit user input before proceeding

---

## Pattern: research

**Scope:** Fetch, evaluate, score, survey, or assess external or internal sources.

### Inner loop

1. **Create tests** — define what a valid research output looks like:
   source reachable, content fetched, evaluation criteria applied, findings recorded
2. **Write** — fetch source; extract relevant content; apply evaluation criteria
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
   path, schema, row/section count, required fields, header format
2. **Write** — compose file content; write via Filesystem tool
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
   required sections, mandatory content per section, format rules (from `writing-docs`)
2. **Write** — draft document following `writing-docs` skill conventions
3. **Run** — read draft; apply `writing-docs` QA checklist
4. **Test** — apply Inner-loop checklist (below) as the formal test gate
5. **Debug** — for missing sections: add; for formatting violations: fix per `writing-docs`;
   for scope drift: trim or expand to match task scope
6. **Back to Write** if any Inner-loop checklist item fails

### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| D1 | All sections declared in plan are present | Blocking | All sections found | Any section missing |
| D2 | Content matches task scope — no drift | Major | Content within scope | Content outside scope |
| D3 | writing-docs QA checklist passes | Major | No open items | Open checklist items |
| D4 | File written and readable | Blocking | Read succeeds | Read fails |

---

## Pattern: code

**Scope:** Implement, refactor, or fix code in a repo.

### Inner loop

1. **Create tests** — write acceptance tests that define the expected behaviour
   before writing any implementation code (TDD: RED phase)
2. **Write** — implement minimal code to pass the acceptance tests (GREEN phase)
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
| C3 | Implementation matches scope — no gold-plating | Major | Scope match | Out-of-scope code added |
| C4 | Code reviewed against `reviewing-tech-claims` if "verified" in scope | Major | Review complete | Review skipped |

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
4. **Test** — apply Inner-loop checklist (below) as the formal test gate
5. **Debug** — for trigger failures: revise description; for checklist failures: fix per critique
6. **Back to Write** if any Inner-loop checklist item fails

### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| S1 | SKILL.md frontmatter valid (name, description, pushy, trigger-inclusive) | Major | All fields valid | Any field invalid |
| S2 | Assessment checklist rating: Pass | Blocking | Pass | Partial or Fail |
| S3 | Mock requests trigger correctly (2–3 tested) — no partial-pass | Blocking | All trigger | Any miss |
| S4 | Reference files declared in SKILL.md are written and readable | Blocking | All files present | Any file missing |
| S5 | HOW-TO-TRIGGER.md updated | Major | Entry present | Entry missing |

---

## Compound Pattern: research + file-write

Apply research inner loop for all research sub-tasks.
When research phase is complete, apply file-write inner loop for the output file.
Inner-loop checklists R1–R4 and F1–F5 apply to their respective sub-tasks.
