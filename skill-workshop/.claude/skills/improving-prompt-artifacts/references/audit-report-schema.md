# Audit Report Schema — improving-prompt-artifacts

Output format for all violation reports produced by the `improving-prompt-artifacts` skill.
Apply this schema to both single-pass reports (default audit) and per-block reports (audit --by-block).

---

## Empty or Unparseable Input

If the submitted artifact is empty or contains no parseable prompting content, produce:

```
AUDIT REPORT
Artifact: [submitted filename]

VIOLATIONS
UNAUDITABLE unauditable_input
 Finding: submitted artifact is empty or contains no parseable prompting content.
 Location: n/a
 Fix: submit a valid Claude prompting artifact.

SUMMARY
Total criteria: 41
Passed: 0
Failed: 41
Risk level: High — do not deploy
```

---

## Standard Report Structure

```
AUDIT REPORT
Artifact: [path or description]
Target Environment: [claude-code | claude-desktop | both | undeclared]
Target Model: [model id | version-neutral | undeclared]
Best-Practices Ref: [YYYY-MM-DD snapshot]
Date: [date]
Auditor: [model id]

VIOLATIONS
[For each failed criterion, output one block in this form:]

[CRITERION-ID] [section heading]
 Severity: [Blocking | Major | Minor]
 Finding: [what was found]
 Location: [quote the offending text, ≤20 words]
 Citation: [best-practices section that supports this finding, or "in-house"]
 Fix: [exact corrective action]

[If no violations are found, write: No violations found.]
```

---

## Violation Block Format

Each failed criterion produces one block:

```
[CRITERION-ID] [section heading]
 Severity: [Blocking | Major | Minor]
 Finding: [what was found]
 Location: [quote the offending text, ≤20 words]
 Citation: [best-practices section, or "in-house"]
 Fix: [exact corrective action]
```

### Severity assignment

| Severity | Use when |
|:---------|:---------|
| Blocking | Hard-rule failures that produce non-deterministic execution: undeclared output schema, no failure-mode handling, conflicting rules with no precedence, undeclared environment when environment-conditional criteria apply |
| Major | Structural defects that introduce variance but do not block execution: missing examples, missing Reason clauses, hedging in hard rules, action-stance undeclared on agentic artifacts |
| Minor | Stylistic or completeness gaps that reduce robustness but rarely change observed output: missing structural diversity in examples, missing revision metadata on audit-only runs |

### Examples

Multiple violations:

```
OBL-2 Obligation language
 Severity: Major
 Finding: modal "should" appears in a hard rule governing output format.
 Location: "you should return the result as a JSON object"
 Citation: in-house
 Fix: replace with "Return the result as a JSON object."

STR-3 Structure and separation
 Severity: Major
 Finding: two terms used for the same concept — "task" and "request" appear
 interchangeably in sections 2 and 4.
 Location: "when the task is complete" / "after the request is resolved"
 Citation: in-house
 Fix: choose one term. Replace all instances of the other.

TOOL-1 Tool use
 Severity: Major
 Finding: tool-invocation instruction uses suggestion verb where execution is intended.
 Location: "can you suggest some changes to improve this function"
 Citation: best-practices snapshot, "Tool usage"
 Fix: replace with "Change this function to improve its performance."

ENV-1 Environment and version declaration
 Severity: Blocking
 Finding: target environment is undeclared and contextual signals are mixed
 (uses both Read and filesystem:read_text_file).
 Location: no declaration present.
 Citation: in-house
 Fix: add "target-environment: claude-code" (or claude-desktop, or both) in
 the metadata table at the bottom of the artifact, then reconcile tool naming
 to match.
```

Zero violations:

```
No violations found.
```

Insufficient evidence on a single criterion:

```
VER-1 Environment and version declaration
 Severity: Major
 Finding: Insufficient evidence to assess. Model target cannot be inferred
 from artifact content.
 Location: no version declaration present.
 Citation: in-house
 Fix: declare target model in the metadata table, or state "version-neutral"
 if instructions are model-agnostic.
```

---

## Summary Block

Every report ends with a Summary block:

```
SUMMARY
Total criteria: 41
Passed: [n]
Failed: [n]
 — Blocking: [n]
 — Major: [n]
 — Minor: [n]
Risk level: [per thresholds below]
```

### Risk level thresholds

| Passed (of 41) | Pass ratio | Risk level |
|:---------------|:-----------|:-----------|
| 41 | 100% | Low — safe to deploy |
| 35–40 | 85–99% | Medium — address violations before deployment |
| Below 35 | <85% | High — do not deploy |

Override rule: any Blocking violation forces Risk level High regardless of pass ratio.

---

## Block Report Variant (--by-block workflow only)

When producing a per-block report (B1–B5), scope the Summary to the block's criteria count:

```
BLOCK REPORT — B[n] [Block Name]
Criteria evaluated: [n]
Passed: [n]
Failed: [n]
 — Blocking: [n]
 — Major: [n]
 — Minor: [n]
```

Do not apply the 41-criterion risk threshold to block reports.
Apply the full risk threshold only in the Final Summary after B5.

---

## Final Summary (--by-block workflow only)

Produced after B5:

```
FINAL AUDIT SUMMARY
Artifact: [filename]
Target Environment: [claude-code | claude-desktop | both]
Target Model: [model id | version-neutral]
Date: [date]
Mode: --by-block

Blocks completed: B1 Foundation | B2 Evidence Layer | B3 Behavior Contract | B4 Agent & Tool Discipline | B5 Deployment Gate

Total criteria: 41
Passed: [n]
Failed: [n]
 — Blocking: [n]
 — Major: [n]
 — Minor: [n]
Risk level: [per thresholds above]
```

---

## Insufficient Evidence Rule

If a criterion cannot be assessed due to insufficient evidence:
- Record: `Finding: Insufficient evidence to assess. Fix: [describe what would resolve the ambiguity].`
- Count as Failed.
- Assign severity Major unless the criterion's failure mode is explicitly Blocking (e.g., ENV-1 when environment-conditional criteria apply).

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-17 |
| Status       | Draft      |
