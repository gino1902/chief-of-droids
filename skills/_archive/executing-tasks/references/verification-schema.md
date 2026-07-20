<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-04-08 -->

# Verification Schema

Read at Step 4a of the executing-tasks outer loop.
Defines the verification scenario format, scenario validation criteria,
acceptance criteria format, and acceptance criteria validation rules.

---

## Verification Scenario

### Format

Present this schema to the user when requesting scenarios:

```
S[N]
Given: [what is true before the trigger fires]
When:  [single trigger — one action or event only]
Then:  [observable system result] and/or [data change] and/or [user-visible impact]
```

One block per distinct functional behaviour introduced or changed by the task.
A single When per scenario — compound triggers must be split into separate scenarios.

### Field Definitions

| Field | Definition |
| :--- | :--- |
| S[N] | Scenario identifier — sequential integer, unique within the task |
| Given | Pre-condition: system or data state before the trigger fires — not storage location, tool name, or implementation detail |
| When | Single trigger: one action or event only |
| Then | Observable outcome: system state change, data change, or user-visible impact — not an internal quality judgment |

### Validation Criteria

Apply to each submitted scenario before accepting it:

| Criterion | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- |
| No file paths, tool calls, or assertions in any field | Blocking | None present in any field | Any present in any field |
| `When` contains exactly one trigger | Blocking | Single trigger | Compound trigger present |
| `Given` describes system or data state — not storage, tools, or implementation | Blocking | State or data described | Storage location, tool name, or implementation detail present |
| `Then` describes an observable outcome — system state, data change, or user-visible impact | Blocking | Observable outcome stated | Internal quality judgment (e.g. "the code is clean") |
| Traceable to task description or confirmed intent | Advisory | Traceable to confirmed intent | Cannot be linked to confirmed intent |

---

## Acceptance Criteria

### Format

Produce one table per confirmed scenario set:

| Scenario ID | Acceptance criterion |
| :--- | :--- |
| S[N] from Step 4a | Exact, observable condition that must hold — file, section, field, or system state |

One or more criteria per scenario. A scenario generates multiple criteria when its
`Then` clause depends on several independent conditions.

### Validation Rules

Apply to each derived criterion before presenting to the user:

| Rule | Severity | Pass | Fail |
| :--- | :--- | :--- | :--- |
| Observable — checkable with a tool call or a read | Blocking | Confirmation requires no interpretation | Criterion requires interpretation to evaluate |
| Unambiguous — only one interpretation of pass/fail | Blocking | Single pass/fail interpretation | Multiple interpretations possible |
| Traceable to its scenario | Blocking | Maps to at least one S[N] | No scenario linkage |

---

| Field        | Value       |
|:-------------|:------------|
| Version      | 1.0         |
| Last Updated | 2026-04-08  |
| Status       | Draft       |
