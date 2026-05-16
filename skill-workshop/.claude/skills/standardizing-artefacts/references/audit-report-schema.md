<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-04-11 -->

# Audit Report Schema — standardizing-artefacts

Output format for all violation reports produced by the `standardizing-artefacts` skill.
Apply this schema to both block reports (audit workflow) and full reports (audit --full workflow).

---

## Empty or Unparseable Input

If the submitted file is empty or contains no parseable instruction content, produce:

```
AUDIT REPORT
File: [submitted filename]

VIOLATIONS
UNAUDITABLE unauditable_input
Finding: submitted file is empty or contains no parseable instruction content.
Location: n/a
Fix: submit a valid Claude Desktop instruction file.

SUMMARY
Total criteria: 33
Passed: 0
Failed: 33
Risk level: High — do not deploy
```

---

## Standard Report Structure

```
AUDIT REPORT
File: [project name or description]
Date: [date]
Auditor: [model or human]

VIOLATIONS
[For each failed criterion, output one block in this form:]

[CRITERION-ID] [section heading — e.g., Obligation language]
 Finding: [what was found]
 Location: [quote the offending text, 20 words max]
 Fix: [exact corrective action]

[If no violations are found, write: No violations found.]
```

---

## Violation Block Format

Each failed criterion produces one block:

```
[CRITERION-ID] [section heading]
 Finding: [what was found]
 Location: [quote the offending text, 20 words max]
 Fix: [exact corrective action]
```

### Examples

Multiple violations, multi-line fix context:

```
OBL-2 Obligation language
 Finding: modal "should" appears in a hard rule governing output format.
 Location: "you should return the result as a JSON object"
 Fix: replace with "Return the result as a JSON object."

STR-3 Structure and separation
 Finding: two terms used for the same concept: "task" and "request" appear
 interchangeably in sections 2 and 4.
 Location: "when the task is complete" / "after the request is resolved"
 Fix: choose one term. Replace all instances of the other. Define the chosen
 term in the definitions section.

OUT-5 Output determinism
 Finding: no uncertainty handling defined. Low-confidence output behavior
 is unspecified.
 Location: no instruction present.
 Fix: add "If evidence is insufficient to complete a field, set the field to
 null. Do not infer or fabricate."
```

Zero violations:

```
No violations found.
```

Insufficient evidence on a single criterion:

```
DSK-1 Claude Desktop specifics
 Finding: Insufficient evidence to assess. File type cannot be determined
 from submitted content.
 Location: no file type declaration present.
 Fix: add a comment at the top of the file declaring its type, e.g.
 "# File type: Project Instructions"
```

---

## Summary Block

Every report ends with a Summary block:

```
SUMMARY
Total criteria: 33
Passed: [n]
Failed: [n]
Risk level:
 33 passed → Low — safe to deploy
 28–32 passed → Medium — address violations before deployment
 Below 28 → High — do not deploy
```

### Risk level thresholds

| Passed | Risk level |
|:-------|:-----------|
| 33 | Low — safe to deploy |
| 28–32 | Medium — address violations before deployment |
| Below 28 | High — do not deploy |

---

## Block Report Variant (audit workflow only)

When producing a per-block report (B1–B4), scope the Summary to the block's criteria count:

```
BLOCK REPORT — B[n] [Block Name]
Criteria evaluated: [n]
Passed: [n]
Failed: [n]
```

Do not apply the 33-criterion risk threshold to block reports.
Apply the full risk threshold only in the Final Summary after B4.

---

## Insufficient Evidence Rule

If a criterion cannot be assessed due to insufficient evidence:
- Record: `Finding: Insufficient evidence to assess. Fix: [describe what would resolve the ambiguity].`
- Count as Failed.
