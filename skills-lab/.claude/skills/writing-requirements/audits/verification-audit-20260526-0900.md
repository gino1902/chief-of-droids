AUDIT REPORT
Artifact: /Users/gilllesmourgues/Workspace/chief-of-droids/skills-lab/.claude/skills/writing-requirements/references/verification.md
Target Environment: claude-code (inferred — file path under .claude/skills/writing-requirements/references/; loaded by parent SKILL.md which declares claude-code)
Target Model: undeclared (parent SKILL.md declares claude-opus-4-7; this reference file does not inherit declaration)
Best-Practices Ref: 2026-05-17 snapshot
Date: 2026-05-26
Auditor: claude-opus-4-7

VIOLATIONS

STR-2 Structure and separation
 Severity: Major
 Finding: top-level components (Acceptance Criteria, Quality Criteria scorecard, Criterion scoring rules) are separated only by markdown `##` headers — no XML tag boundaries.
 Location: "## Acceptance Criteria (§AC) ... ## Quality Criteria scorecard (§QC) ... ## Criterion scoring rules"
 Citation: best-practices snapshot, "Structure prompts with XML tags."
 Fix: wrap top-level components in named XML tags: `<acceptance-criteria>`, `<quality-scorecard>`, `<scoring-rules>`.

EX-1 Examples
 Severity: Minor
 Finding: scorecard table shows only 2 example rows (FR-001, NFR-001); criterion scoring rules describe ✓/✗ logic per criterion but provide no per-criterion worked example; below the 3–5 threshold for the scorecard rule and for each scoring criterion.
 Location: "**Scorecard table** (follows immediately after definitions):" + 2-row example; "Criterion scoring rules" section.
 Citation: best-practices snapshot, "Include 3–5 examples for best results."
 Fix: extend the scorecard example to 4–5 diverse rows (FR, NFR, ERR, IR, DR); add a worked example per scoring criterion showing the pass/fail decision applied to a sample requirement.

EX-4 Demonstration where possible
 Severity: Minor
 Finding: Bounded 3-step procedure, Atomic compound-detection, and Unambiguous undefined-term Warning are described but not demonstrated.
 Location: "How Bounded is evaluated:" 3-step block; "Atomic — Count modal verbs ..."; "Unambiguous — Emit Warning per undefined term".
 Citation: best-practices snapshot, "Examples are one of the most reliable ways to steer Claude's output."
 Fix: add a worked Bounded evaluation showing all 3 steps applied to a sample NFR; a worked Atomic compound example (multi-SHALL requirement → split recommendation); a worked Unambiguous Warning emission for a sample term not in §Glossary.

EX-5 Examples — structural diversity
 Severity: Minor
 Finding: the 2 example rows in the scorecard are structurally similar — both score ✓ on Atomic, Unambiguous, Verifiable, Traceable, differing only on Bounded N/A vs ✓. No example covers a failure row (✗ on any criterion).
 Location: scorecard 2-row example.
 Citation: best-practices snapshot, "Diverse."
 Fix: include a failing-criterion row in the extended example set per EX-1 fix — e.g., an FR with ✗ on Unambiguous (undefined term) or ✗ on Verifiable (no AC).

RSN-1 Reasoning context
 Severity: Minor
 Finding: non-obvious rules carry no Reason clause — "Bounded — Heuristic — applies to NFR-class requirements only; N/A for all others"; "Common words and RFC 2119 keywords are exempt from this check"; "Table-form entries (DR, TR) → ✓ by default (tables are structurally atomic per row)" (the parenthetical encodes principle but is not framed as "Reason:").
 Location: Bounded scoring rule; Unambiguous scoring rule; Atomic scoring rule.
 Citation: best-practices snapshot, "Add context to improve performance."
 Fix: append Reason clauses — Bounded-NFR-only: "Reason: quantitative thresholds are meaningful only for quality attributes; non-NFR requirements are verified by AC enumeration, not by threshold matching"; common-words-exempt: "Reason: common-vocabulary scoring would force every glossary to enumerate trivial nouns, drowning domain-specific terms in noise"; tables-atomic: "Reason: each row in a DR or TR table is one (field × constraint) or one (input → output) pair — the row IS the atomic unit; counting modals across rows would mis-classify the structural form."

RSN-3 Reasoning context — chain-of-thought
 Severity: Minor
 Finding: chain-of-thought behavior is not addressed.
 Location: no CoT directive present.
 Citation: best-practices snapshot, "Leverage thinking" + "Migrating away from prefilled responses."
 Fix: add an execution rule at the top of the file — "Reason internally when deriving AC from each requirement type and when scoring each criterion. Emit only AC entries, the definitions block, the scorecard table, and Warnings per format spec; do not include reasoning narration in output."

BRN-2 Branching and edge cases
 Severity: Minor
 Finding: edge cases not enumerated — requirement carrying both an NFR-class quality assertion and an SLA threshold (Bounded applies); SEC requirement using EARS form (Unwanted Behavior) — does Atomic count one SHALL? not specified; DR row with an inline modal in Notes column — does Atomic re-fire?
 Location: Atomic scoring rule; Bounded scoring rule.
 Citation: in-house.
 Fix: enumerate the cases — "EARS Unwanted Behavior contains one SHALL in the response clause; Atomic scores ✓"; "Modals inside Notes column of DR/TR tables do not count toward Atomic — only the modal in the entry-defining SHALL/MUST statement"; "An SEC requirement expressing a quality (Bounded applies) is scored on its Measurement field, not the security obligation."

VER-1 Version declaration
 Severity: Minor
 Finding: target Claude model is not declared in the artifact.
 Location: file has no bottom metadata block.
 Citation: best-practices snapshot, "Prompting Claude Opus 4.7" + "Migration considerations."
 Fix: add a bottom metadata block including Target Model, Target Environment, Best-Practices Ref, Last Revised, Revision Source.

VER-2 Revision metadata
 Severity: Minor
 Finding: file lacks any bottom metadata block — no Version, no Last Updated, no Status, no revision provenance.
 Location: file ends at "Emit Warning for each ✗ on Bounded."
 Citation: in-house.
 Fix: append the complete metadata block per VER-1 fix, plus Version/Last Updated/Status fields.

SUMMARY
Total criteria: 41
Passed: 32
Failed: 9
 — Blocking: 0
 — Major: 1
 — Minor: 8
Risk level: High — do not deploy

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-26 |
| Status       | Draft      |
