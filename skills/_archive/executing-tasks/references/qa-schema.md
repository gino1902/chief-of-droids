<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-04-08 -->

# QA Schema

Read at Step 7 of the executing-tasks outer loop.
Defines the QA suite row format, severity taxonomy, Confidence Derivation Rule,
QA Row Ownership Table format, and traceability matrix format.
Content applies at Steps 7, 8, 9, and 10.

---

## QA Suite Row Format

| Field | Definition |
| :--- | :--- |
| ID | Unique test identifier — e.g. QA-01, QA-02 |
| Scenario | S[N] reference(s) from Step 4a — at least one required per row |
| Severity | Blocking / Major / Minor — see Severity Taxonomy below |
| Assertion | What is being checked — one condition per row |
| Pass condition | Exact observable state that constitutes a pass |
| Fail condition | Exact observable state that constitutes a fail |
| Artifact | File path, section, or system component under test |

Minimum: one row per acceptance criterion from Step 4b.
A row with no Scenario reference is invalid and must be removed or reassigned before the suite is confirmed.

---

## Severity Taxonomy

| Severity | Definition |
| :--- | :--- |
| Blocking | Test covers a criterion whose failure makes the associated verification scenario untestable |
| Major | Test covers a criterion that partially validates the scenario |
| Minor | Test covers a style or advisory criterion |

Assign Severity per the acceptance criterion each test row covers.

---

## Confidence Derivation Rule

Applies at Step 9 (per-sub-task inner-loop checklist) and Step 10 (full QA suite).

**Computation:**
- Start: 100%
- Any Blocking failure: Confidence = 0% (hard floor — cannot recover in the current run)
- Per Major failure: −20%
- Per Minor failure: −3%

**Report format:**
```
Confidence: [N]% — [B] Blocking / [M] Major / [m] Minor failures
```

**Gate:** Confidence ≥ 95% is required to advance at Steps 9 and 10; below 95% blocks the current step.

Threshold interpretation: ≥ 95% = 0 Blocking + 0 Major + at most 1 Minor failure.

---

## QA Row Ownership Table

Produced at Step 8. Format:

| Sub-task | QA Row IDs | Acceptance criterion IDs |
| :--- | :--- | :--- |
| Sub-task N | QA-X, QA-Y | Criterion IDs from Step 4b |

**Constraints:**
- Every QA row must map to exactly one sub-task.
- A QA row whose assertion spans multiple sub-tasks' outputs: flag as ambiguous; resolve
  by splitting the row or assigning to the sub-task that produces the primary artifact.
- A QA row that cannot be assigned to any sub-task: plan gap — return to Step 6 before proceeding.

---

## Traceability Matrix

Produced at Step 10. Format:

| Scenario | Acceptance criteria | QA tests | Scenario status |
| :--- | :--- | :--- | :--- |
| S[N] from Step 4a | Criterion IDs from Step 4b | Test IDs from Step 7 | ✅ Pass / ❌ Fail |

**Rules:**
- Scenario status = ✅ only if all QA tests mapped to that scenario pass.
- Any scenario from Step 4a with no QA test mapped: block — return to Step 7 to close
  the gap. Do not proceed with an unmapped scenario.
- Any scenario status = ❌: the outer loop is not closed. Treat as a Blocking failure
  regardless of individual test severity.

---

| Field        | Value       |
|:-------------|:------------|
| Version      | 1.0         |
| Last Updated | 2026-04-08  |
| Status       | Draft       |
