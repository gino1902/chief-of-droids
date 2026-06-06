AUDIT REPORT
Artifact: /Users/gilllesmourgues/Workspace/chief-of-droids/skills-lab/.claude/skills/improving-skills-predictability/SKILL.md
Target Environment: claude-code
Target Model: claude-opus-4-7
Best-Practices Ref: 2026-05-17 snapshot
Date: 2026-05-18
Auditor: claude-opus-4-7

VIOLATIONS

OUT-4 Output determinism — positive framing
 Severity: Minor
 Finding: Several instructions use negative framing where a positive form was available and unambiguous. Examples: "Hold all results in memory; do not write until Phase 7." (positive form: "Hold all results in memory until Phase 7."); "Read into memory only — no writes yet" (positive form: "Read into memory only."); "Numbers without evidence are not allowed." (positive form: "Every number must cite evidence."). The disambiguating-negation exception applies to some negations in the artifact (e.g., "do not abort — record it as a per-file deviation"), but the cases cited above are unambiguous in their positive form.
 Location: "Hold all results in memory; do not write until Phase 7." (Phase 3 preamble); "Read into memory only — no writes yet" (Phase 1); "Numbers without evidence are not allowed." (Phase 5)
 Citation: best-practices snapshot, "Tell Claude what to do instead of what not to do"
 Fix: rewrite the three cited lines in positive form:
   - "Hold all results in memory; do not write until Phase 7." → "Hold all results in memory until Phase 7."
   - "Read into memory only — no writes yet" → "Read into memory only."
   - "Numbers without evidence are not allowed." → "Every number must cite concrete evidence."
   Retain negative framing only where the positive form would be ambiguous (e.g., "Do not modify the analyzed skill or its outputs." — anti-pattern enumeration that the positive form does not communicate as precisely).

SUMMARY
Total criteria: 41
Passed: 40
Failed: 1
 — Blocking: 0
 — Major: 0
 — Minor: 1
Risk level: Medium — address violations before deployment

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-18 |
| Status       | Draft      |
