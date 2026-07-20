<!-- version: 1.14 | author: chief-of-droids workspace | last_updated: 2026-04-13 -->

<preamble>

# Sub-Task Patterns

Read at Step 9 of the executing-tasks outer loop.

**Step 9:** For each sub-task from the Step 6 plan, run the inner-loop defined
for the classified pattern. The inner-loop runs within a single sub-task — it is
not the sub-task sequence itself. For the Test step, apply the **Inner-loop
checklist** for the classified pattern as the formal test gate.
All checklist items must pass before advancing to the next sub-task.

**TDD discipline in this file:**
Each pattern's TDD Annotations subsection carries a State-0 reference — what
"fail before writing begins" looks like for that type — and a Green constraint —
restrict changes to the minimum required for the current owned QA row. Both
annotations encode the Red → Green discipline declared in SKILL.md Step 9.
The QA Row Ownership Table (produced at SKILL.md Step 8) is the authority for
which rows are owned by the current sub-task.

Reason internally before selecting and applying a pattern. Do not surface
pattern-selection reasoning in chat output.

</preamble>

<inner-loop-qa-report-format>

## Inner Loop QA Report

After all sub-tasks complete — before Step 10 — surface a structured report.

Format:

```
## Inner Loop QA Report — [pattern] sub-task [N]

Verification confidence impact: [agreed %] → [adjusted %]

| ID | Assertion | Severity | Result | Detail |
| :--- | :--- | :--- | :--- | :--- |
| XX | [assertion text] | Blocking / Major / Minor | ✅ Pass / ❌ Fail | — or failure detail |

Summary: [N] passed · [N] failed ([N] Blocking · [N] Major · [N] Minor)
```

Example (zero failures):

```
## Inner Loop QA Report — file-write sub-task 1

Verification confidence impact: 95% → 95%

| ID | Assertion | Severity | Result | Detail |
| :--- | :--- | :--- | :--- | :--- |
| F1 | File readable via filesystem:read_text_file immediately after write | Blocking | ✅ Pass | — |
| F2 | Row/section count matches approved draft | Major | ✅ Pass | — |
| F3 | All required schema fields present | Major | ✅ Pass | — |
| F4 | Header metadata (version, last_updated) reflects current date | Minor | ✅ Pass | — |
| F5 | No old-schema artefacts present | Major | ✅ Pass | — |

Summary: 5 passed · 0 failed (0 Blocking · 0 Major · 0 Minor)
```

Example (Blocking failure — confidence floor triggered):

```
## Inner Loop QA Report — file-write sub-task 1

Verification confidence impact: 95% → 0%

| ID | Assertion | Severity | Result | Detail |
| :--- | :--- | :--- | :--- | :--- |
| F1 | File readable via filesystem:read_text_file immediately after write | Blocking | ❌ Fail | Read returned empty — write may have failed silently |
| F2 | Row/section count matches approved draft | Major | ❌ Fail | Draft had 7 rows; written file has 5 |
| F3 | All required schema fields present | Major | ✅ Pass | — |
| F4 | Header metadata (version, last_updated) reflects current date | Minor | ✅ Pass | — |
| F5 | No old-schema artefacts present | Major | ✅ Pass | — |

Summary: 3 passed · 2 failed (1 Blocking · 1 Major · 0 Minor)
```

**Severity definitions** (for inner-loop checklist items — numeric confidence impacts
defined in the Confidence Derivation Rule in `references/qa-schema.md`):

| Severity | Definition |
| :--- | :--- |
| Blocking | Failure makes the verification scenario untestable or meaningless |
| Major | Failure partially invalidates a verification scenario item |
| Minor | Quality gap — verification scenario remains valid |

</inner-loop-qa-report-format>

<patterns>

---

## Pattern: research

**Scope:** Fetch, evaluate, score, survey, or assess external or internal sources.

#### Steps

1. **Create tests** — define what a valid research output looks like:
   source reachable, content fetched, evaluation criteria applied, findings recorded.
2. **Write** — fetch source; extract relevant content; apply evaluation criteria.
3. **Run** — confirm fetch succeeded; content non-empty; criteria applied to all items.
4. **Test** — apply inner-loop checklist (below) as the formal test gate.
5. **Debug** — for failed fetches: retry with alternative URL or search query;
   document exclusion with rationale if the retry still fails.
   For criteria failures: re-evaluate with explicit rationale; document exclusion
   with rationale if re-evaluation still fails.
   Reason: one retry per failed source is sufficient — a second consecutive failure
   indicates a retrieval constraint, not a transient error; document and exclude
   rather than looping indefinitely.
6. **Back to Write** if any inner-loop checklist item fails.

#### TDD Annotations (State-0 / Green)

**Step 1 State-0:** the rows from the Step 8 ownership table assigned to this
sub-task define the not-yet-started state — source not fetched, evaluation not
applied. Record fail state (source absent / criteria not applied) per owned row
before proceeding to Write.

**Step 2 Green:** fetch and evaluate only what is required to satisfy the current
owned QA row. Advance to the next owned row only after the current row's assertion
passes its Test step.

#### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| R1 | All sources in scope were fetched or explicitly excluded | Blocking | Every source has a status | Any source has no status |
| R2 | Each included source has applied evaluation criteria with rationale | Major | Rationale present per source | Rating with no rationale |
| R3 | Excluded sources have documented exclusion reason | Major | Reason present | Silent exclusion |
| R4 | Findings are traceable to fetched content — not from memory | Blocking | Each finding references fetch result | Finding with no source attribution |

Example result: `| R1 | All sources in scope were fetched or explicitly excluded | Blocking | ✅ Pass | — |`

---

## Pattern: file-write

**Scope:** Write or overwrite a structured file (`.md`, config, schema).

#### Steps

1. **Create tests** — define expected file properties:
   path, schema, row/section count, required fields, header format.
2. **Write** — compose file content; write via Filesystem tool.
3. **Run** — read file back immediately via `filesystem:read_text_file`.
4. **Test** — apply inner-loop checklist (below) as the formal test gate.
5. **Debug** — if read-back fails: retry write; if schema mismatch: fix content and
   rewrite; if row count wrong: diff draft vs written file.
6. **Back to Write** if any inner-loop checklist item fails.

#### TDD Annotations (State-0 / Green)

**Step 1 State-0:** for each owned QA row, run `filesystem:read_text_file` on the
target path and confirm the file is absent or does not yet satisfy the row's
assertion. Record the observed state (file absent / field missing / schema
non-conformant) per row before proceeding to Write.

**Step 2 Green:** write only the minimum file content required to pass the current
owned QA row. Do not pre-write content for future rows.

#### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| F1 | File readable via `filesystem:read_text_file` immediately after write | Blocking | Read succeeds, content non-empty | Read fails or empty |
| F2 | Row/section count matches approved draft | Major | Counts match | Row dropped or duplicated |
| F3 | All required schema fields present | Major | All fields found | Any field missing |
| F4 | Header metadata (version, last_updated) reflects current date | Minor | Date correct | Stale or missing |
| F5 | No old-schema artefacts present | Major | Old fields absent | Old field found |

Example result: `| F2 | Row/section count matches approved draft | Major | ❌ Fail | Draft had 9 rows; written file has 7 — two rows dropped during write |`

---

## Pattern: doc

**Scope:** Author or revise a structured document (guide, ADR, runbook, reference doc).

#### Steps

1. **Create tests** — define document completeness criteria:
   required sections, mandatory content per section, format rules (from `writing-docs`).
2. **Write** — draft document following `writing-docs` skill conventions.
3. **Run** — read draft; apply `writing-docs/references/qa-checklist.md`.
4. **Test** — apply inner-loop checklist (below) as the formal test gate.
5. **Debug** — for missing sections: add; for formatting violations: fix per `writing-docs`;
   for intent drift: trim or expand to match confirmed intent.
6. **Back to Write** if any inner-loop checklist item fails.

#### TDD Annotations (State-0 / Green)

**Step 1 State-0:** for each owned QA row, record section-absent or content-absent
as the fail state before drafting begins. No execution required — absence is the
definitional fail state.

**Step 2 Green:** draft only the sections or content blocks required for the current
owned QA row. Do not speculatively draft sections for future rows.

#### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| D1 | All sections declared in plan are present | Blocking | All sections found | Any section missing |
| D2 | Content matches confirmed intent — no drift | Major | Content within confirmed intent boundary | Content outside confirmed intent |
| D3 | `writing-docs/references/qa-checklist.md` passes | Major | No open items | Open checklist items |
| D4 | File written and readable | Blocking | Read succeeds | Read fails |

Example result: `| D3 | writing-docs/references/qa-checklist.md passes | Major | ✅ Pass | — |`

---

## Pattern: code

**Scope:** Implement, refactor, or fix code in a repo.

#### Steps

1. **Create tests** — write acceptance tests that define the expected behaviour
   before writing any implementation code (TDD: RED phase).
2. **Write** — implement minimal code to pass the acceptance tests (GREEN phase).
3. **Run** — execute tests; capture output.
4. **Test** — apply inner-loop checklist (below) as the formal test gate.
5. **Debug** — for failing tests: read error; identify root cause; fix implementation
   only (do not modify tests to pass); re-run.
   If the implementation fix does not resolve the failure after one attempt: surface —
   "Sub-task [N] Debug loop unresolved: [test ID] [error]. Options: (1) revise the
   acceptance criterion; (2) revise the implementation approach. Which do you prefer?"
   Await user choice before re-entering Write.
6. **Back to Write** if any inner-loop checklist item fails.

#### TDD Annotations (State-0 / Green)

**Step 1 State-0:** confirm all owned QA row tests fail against the current system
before entering Write. State: `"State-0 confirmed for sub-task [N]: [M] rows fail
as expected."` If any row passes before changes are made, surface as a State-0
anomaly and resolve with the user before proceeding.

**Step 2 Green:** implement only the minimum code required to pass the current
failing test. Do not implement logic not demanded by the current red test. Advance
to the next test only after the current one passes.

#### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| C1 | All acceptance tests pass | Blocking | Test suite green | Any test red |
| C2 | No existing tests broken (regression) | Blocking | Full suite green | Regression introduced |
| C3 | Implementation matches confirmed intent — no gold-plating | Major | Intent match | Out-of-scope code added |
| C4 | Code reviewed against `reviewing-tech-claims` if "verified" in confirmed intent | Major | Review complete | Review skipped. Reason: `reviewing-tech-claims` adds a source-fetch round-trip unnecessary when the confirmed intent does not require verified accuracy — scoping to "verified" keeps the inner-loop efficient for tasks without a verification obligation. |

Example result: `| C2 | No existing tests broken (regression) | Blocking | ✅ Pass | — |`

---

## Pattern: skill-authoring

**Scope:** Author a new SKILL.md or enrich/critique an existing skill.
Delegates entirely to `creating-skills` for domain logic.

#### Steps

1. **Create tests** — design assessment mock requests (2–3 realistic triggers).
2. **Write** — read `skills/creating-skills/SKILL.md` before proceeding; run the
   matched `creating-skills` workflow (author / enrich / critique as applicable);
   produce SKILL.md + reference files.
   Reason: variant selection mirrors the confirmed intent verb — 'author' maps to
   the author workflow, 'enrich' to enrich, 'critique' to critique; if the confirmed
   intent does not map cleanly to a single variant, surface the ambiguity to the
   user before proceeding.
3. **Run** — run mock requests against the draft.
4. **Test** — apply inner-loop checklist (below) as the formal test gate.
5. **Debug** — for trigger failures: revise description; for checklist failures:
   fix per critique.
6. **Back to Write** if any inner-loop checklist item fails.

#### TDD Annotations (State-0 / Green)

**Step 1 State-0:** for each owned QA row, record SKILL.md absent or the specific
criterion (section, trigger, reference file) absent as the fail state before the
`creating-skills` workflow begins.

**Step 2 Green:** produce only the SKILL.md content or reference file content
required to pass the current owned QA row. Do not speculatively author sections
for future rows.

#### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| S1 | SKILL.md frontmatter valid — `name` and `description` present and well-formed; description is specific and trigger-inclusive. Note: the official Anthropic SKILL.md spec requires only `name` and `description`; any additional fields are workspace conventions | Major | name and description present and valid | name or description absent or vague |
| S2 | Assessment checklist (`creating-skills/references/assessment-checklist.md`) rating: Pass | Blocking | Pass | Partial or Fail |
| S3 | Mock requests trigger correctly (2–3 tested) — no partial-pass | Blocking | All trigger | Any miss |
| S4 | Reference files declared in SKILL.md are written and readable | Blocking | All files present | Any file missing |
| S5 | HOW-TO-TRIGGER.md updated | Major | Entry present | Entry missing |

Example result: `| S3 | Mock requests trigger correctly (2–3 tested) — no partial-pass | Blocking | ❌ Fail | Second mock request ("run skill assessment") did not load skill — trigger pattern too narrow |`

---

## Pattern: framing

**Scope:** Build or challenge a FRAMING.md for a project or use case.
Delegates to `analyzing-business-cases` for domain logic.

#### Steps

1. **Create tests** — define what a valid FRAMING.md output looks like:
   all 6 template sections present; all 7 challenge framing Blocking criteria met;
   advisory items surfaced and acknowledged by user.
2. **Write** — run `analyzing-business-cases` workflow:
   - `build framing`: read `analyzing-business-cases/references/FRAMING-template.md`;
     scaffold FRAMING.md with user.
   - `challenge framing` only: read existing FRAMING.md via filesystem tool.
3. **Run** — apply challenge framing sub-workflow:
   read `analyzing-business-cases/references/qa-checklist.md §challenge framing`;
   apply all Blocking and Advisory criteria to FRAMING.md content; record pass/fail
   per item.
   If the §challenge framing section is absent from qa-checklist.md: halt. Surface —
   "⚠️ §challenge framing section not found in
   analyzing-business-cases/references/qa-checklist.md — verify file integrity
   before proceeding."
4. **Test** — apply inner-loop checklist (below) as the formal test gate.
5. **Debug** — for Blocking failures: read qa-checklist.md failure signal; propose
   targeted section edit; apply on explicit user confirmation; re-run challenge;
   never rewrite FRAMING.md without user instruction.
   For Advisory: surface all findings; do not block.
   Reason: advisory items are presentational quality signals, not correctness
   failures — blocking on them would prevent delivery of a structurally valid
   FRAMING.md on items the user may intentionally defer.
6. **Back to Write** if any inner-loop checklist item fails.

#### TDD Annotations (State-0 / Green)

**Step 1 State-0:** for each owned QA row, record FRAMING.md absent or the required
section absent / non-conformant as the fail state before drafting begins. No
execution required — absence is the definitional fail state.

**Step 2 Green:** draft only the FRAMING.md section(s) required for the current
owned QA row. Do not speculatively draft sections for future rows.

#### Inner-loop checklist

| ID | Assertion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- | :--- |
| FR1 | FRAMING.md written and readable via `filesystem:read_text_file` | Blocking | Read succeeds, content non-empty | Read fails or empty |
| FR2 | All 6 FRAMING-template.md sections present: Context, Problem, Client, Objectives, Solution, Constraints | Blocking | All 6 section headers found | Any section missing |
| FR3 | All 7 challenge framing Blocking criteria pass (`analyzing-business-cases/references/qa-checklist.md §challenge framing`) | Blocking | All 7 pass | Any one fails |
| FR4 | All Advisory items from `analyzing-business-cases/references/qa-checklist.md §challenge framing` surfaced to user | Major | All advisory findings listed; user acknowledged | Advisory section skipped |
| FR5 | No FRAMING.md edit applied without explicit user confirmation | Major | All edits user-confirmed | Any unrequested rewrite |

Example result: `| FR2 | All 6 FRAMING-template.md sections present | Blocking | ✅ Pass | — |`

---

## Compound Pattern: research + file-write

Apply the research inner-loop for all research sub-tasks.
When the research sub-task is complete, apply the file-write inner-loop for the
output file. Inner-loop checklists R1–R4 and F1–F5 apply to their respective
sub-tasks.

If the target file already exists at the start of the file-write inner-loop: treat
as a State-0 anomaly — surface to user before proceeding. Do not overwrite without
explicit confirmation.

</patterns>

| Field        | Value       |
|--------------|-------------|
| Version      | 1.14        |
| Last Updated | 2026-04-13  |
| Status       | Draft       |
