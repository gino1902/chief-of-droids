AUDIT REPORT
Artifact: /Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/.claude/skills/writing-requirements/references/conventions.md
Target Environment: claude-code (inferred — file path under .claude/skills/writing-requirements/references/; loaded by parent SKILL.md which declares claude-code)
Target Model: undeclared (parent SKILL.md declares claude-opus-4-7; this reference file does not inherit declaration)
Best-Practices Ref: 2026-05-17 snapshot
Date: 2026-05-26
Auditor: claude-opus-4-7

VIOLATIONS

STR-2 Structure and separation
 Severity: Major
 Finding: top-level components (ID convention, Report format, Severity model, Failure model, Substrate-gap defaults, Iteration model) are separated only by markdown `##` headers — no XML tag boundaries.
 Location: "## ID convention ... ## Report format ... ## Severity model ... ## Failure model ... ## Substrate-gap defaults ... ## Iteration model"
 Citation: best-practices snapshot, "Structure prompts with XML tags."
 Fix: wrap top-level components in named XML tags: `<id-convention>`, `<report-format>`, `<severity-model>`, `<failure-model>`, `<substrate-gap-defaults>`, `<iteration-model>`.

RSN-1 Reasoning context
 Severity: Major
 Finding: multiple non-obvious rules carry no Reason clause — "Renumbering | Never automatic; user-driven only"; "Bare `[BLOCKING]` or `[WARNING]` tags ... are not permitted on output"; "Each invocation is a full stateless pass — no detection of first vs nth iteration. Output files are overwritten each pass."
 Location: ID convention table; Per-finding tag rules; Iteration model.
 Citation: best-practices snapshot, "Add context to improve performance."
 Fix: append Reason clauses — renumbering: "Reason: automatic renumbering would break cross-references between requirement entries and downstream consumers (traceability, change-tracking); ID changes must be visible in commit history"; bare-tags: "Reason: a bare tag forces the reader to infer resolution state; explicit suffix removes the inference and lets the Summary table tallies be derived mechanically"; stateless-pass: "Reason: per-iteration state would couple the run's output to its history, making the same substrate produce different outputs on re-run; statelessness preserves substrate-determined output."

EX-1 Examples
 Severity: Minor
 Finding: canonical ordering walk (4 numbered rules + 3 exclusions), tag rules (5 tags + bare-tag prohibition), and Report format template provide structure but no concrete worked instances showing the rules applied to a sample substrate or sample report section.
 Location: "Canonical ordering for un-IDed substrate ... 1. Within each category section, order requirements by the byte position of the first modal verb ..."; "Per-finding tag rules" table.
 Citation: best-practices snapshot, "Include 3–5 examples for best results."
 Fix: add 3 worked examples for canonical ordering (sample 3-sentence substrate → byte positions → resulting FR-NNN sequence); add a worked report section showing each tag type with realistic content.

EX-4 Demonstration where possible
 Severity: Minor
 Finding: canonical ordering exclusions (modals inside code blocks, quoted strings, section headings) are listed but not demonstrated; tag rules are listed but not demonstrated with a per-phase report section excerpt.
 Location: "Exclusions from the byte-position walk:" list; "Per-finding tag rules" table.
 Citation: best-practices snapshot, "Examples are one of the most reliable ways to steer Claude's output."
 Fix: add a worked example with all three exclusion categories present in substrate; add a worked phase section showing `[BLOCKING-UNRESOLVED]`, `[WARNING-RESOLVED]`, `[INFO]` lines in realistic context.

RSN-3 Reasoning context — chain-of-thought
 Severity: Minor
 Finding: chain-of-thought behavior is not addressed.
 Location: no CoT directive present.
 Citation: best-practices snapshot, "Leverage thinking" + "Migrating away from prefilled responses."
 Fix: add an execution rule at the top of the file — "Reason internally when resolving canonical-ordering ties and severity assignments. Emit only ID assignments, severity tags, and the Outstanding closure line per format spec; do not include reasoning narration in output."

BRN-2 Branching and edge cases
 Severity: Minor
 Finding: edge cases not enumerated — substrate where all modals fall inside excluded zones (code blocks + quoted strings + headings) producing zero candidate positions; substrate IDs with non-3-digit width (`FR-1`, `FR-12`, `FR-1234`); substrate IDs with non-canonical separators (`FR_001`).
 Location: "Canonical ordering for un-IDed substrate" rules and exclusions; ID convention table.
 Citation: in-house.
 Fix: enumerate edge cases — "If the byte-position walk yields zero candidates after exclusions, emit Warning and treat the substrate as having no IDable content; render all requirement sections as N/A."; "Non-3-digit and non-canonical-separator IDs are treated as un-IDed; Phase 4 emits Warning citing the unmatched pattern."

OUT-4 Positive framing
 Severity: Minor
 Finding: multiple negatives where positive form is unambiguous — "Do not emit `SEC-001`, `OBS-001`, or any other numeric requirement ID"; "Bare `[BLOCKING]` or `[WARNING]` tags ... are not permitted"; "No `🔲 To be defined` scaffolding"; "never a numeric ID".
 Location: Substrate-gap defaults; Per-finding tag rules.
 Citation: best-practices snapshot, "Tell Claude what to do instead of what not to do."
 Fix: convert to positive form — "Use the section heading alone (or the sentinel `SEC-NONE`/`OBS-NONE`) to record an N/A category"; "Every Blocking and Warning finding carries an explicit `-RESOLVED` or `-UNRESOLVED` suffix"; "Use `N/A` as the sole substrate-gap placeholder."

VER-1 Version declaration
 Severity: Minor
 Finding: target Claude model is not declared in the artifact.
 Location: file has no bottom metadata block.
 Citation: best-practices snapshot, "Prompting Claude Opus 4.7" + "Migration considerations."
 Fix: add a bottom metadata block including Target Model, Target Environment, Best-Practices Ref, Last Revised, Revision Source.

VER-2 Revision metadata
 Severity: Minor
 Finding: file lacks any bottom metadata block — no Version, no Last Updated, no Status, no revision provenance.
 Location: file ends at "DoD per iteration: all seven phases complete and both files written."
 Citation: in-house.
 Fix: append the complete metadata block per VER-1 fix, plus Version/Last Updated/Status fields.

SUMMARY
Total criteria: 41
Passed: 32
Failed: 9
 — Blocking: 0
 — Major: 2
 — Minor: 7
Risk level: High — do not deploy

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-26 |
| Status       | Draft      |
