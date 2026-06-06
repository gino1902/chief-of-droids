AUDIT REPORT
Artifact: /Users/gilllesmourgues/Workspace/chief-of-droids/skills-lab/.claude/skills/improving-skills-predictability/SKILL.md
Target Environment: claude-code (inferred from frontmatter `allowed-tools: Read/Write/Bash` and `.claude/skills/` path; no explicit declaration)
Target Model: undeclared
Best-Practices Ref: 2026-05-17 snapshot
Date: 2026-05-17
Auditor: claude-opus-4-7

VIOLATIONS

OBL-4 Obligation language
 Severity: Minor
 Finding: judgment rule omits a Reason clause encoding the principle that governs the permitted variance.
 Location: "An invariant need not appear in every artifact — only in artifacts where the analyzed skill is expected to surface it."
 Citation: best-practices snapshot, "Add context to improve performance."
 Fix: append "Reason: an invariant's expected coverage is bounded by the analyzed skill's scope; absence outside that scope is a coverage signal, not a defect."

STR-1 Structure and separation
 Severity: Minor
 Finding: a single section co-locates rules from multiple concerns — statelessness/tolerance, output-only policy, projection-vs-measurement disclaimer, large-substrate handling, evidence grounding, and scratch-work suppression.
 Location: "## Operational notes" — six bullets spanning unrelated concerns.
 Citation: in-house
 Fix: split into named sections (Statelessness, Output policy, Projection disclosure, Large-substrate handling, Evidence grounding, Output hygiene) or relocate each bullet into the phase whose scope it governs.

STR-2 Structure and separation
 Severity: Major
 Finding: top-level components (role, invocation, instructions, examples, output-format) are separated only by markdown headers; no XML tag wraps a component.
 Location: every top-level boundary uses `##` headers; no `<instructions>`, `<examples>`, `<context>`, `<output-format>` tags appear.
 Citation: best-practices snapshot, "Structure prompts with XML tags."
 Fix: wrap top-level components in named XML tags. Retain markdown for sub-structure inside each component.

EX-1 Examples
 Severity: Major
 Finding: non-trivial format rules each carry one example rather than 3–5. Affects: phase-header stream, discovery echo block, recommendation block, dependency-annotation line, hard-fail block.
 Location: a single specimen is given for "Discovered: <N> runs × <M> artifacts ..." and for "### R-00X — <one-line title> [projected lift: +N pts]".
 Citation: best-practices snapshot, "Include 3–5 examples for best results."
 Fix: add 2–4 worked examples per format rule covering varied input shapes. For the Discovered block: full-coverage discovery, partial-coverage discovery, non-comparable-present discovery, multi-artifact discovery. For the recommendation block: high-lift, low-lift, zero-lift, dependency-laden.

EX-2 Examples
 Severity: Major
 Finding: no example demonstrates an edge case — empty discovery, malformed glob, all-non-comparable artifacts, zero-failing-dimensions rank.
 Location: every example shown is a happy-path single instance.
 Citation: best-practices snapshot, "Diverse: cover edge cases."
 Fix: add at least one edge-case example per format rule. Example: a Discovered block where every artifact is `[non-comparable]`, paired with the resulting prompt outcome.

EX-3 Examples
 Severity: Minor
 Finding: examples lack explicit directional labels — no "Correct:" / "Incorrect:" framing.
 Location: code blocks are presented as bare format specimens with no verdict header.
 Citation: in-house
 Fix: label every example "Correct:" or "Incorrect:" — the label removes residual ambiguity even when the artifact only shows targets.

EX-4 Examples
 Severity: Major
 Finding: demonstrable rules lack a worked demonstration. Affected: artifact-key derivation, comparability filter threshold, auto-confirm condition evaluation, version-token regex matching.
 Location: "for each comparable file, derive the artifact key by removing every version-token match from the basename..."; "Comparability filter: an artifact is comparable iff it is present in ≥ ⌈N/2⌉ runs (rounded up)."
 Citation: in-house; aligned with "Examples are one of the most reliable ways to steer Claude's output."
 Fix: add a worked example per rule. Example for artifact-key derivation: "Input: `slug-v01--requirements.md` → strip `v01` → `slug--requirements.md` → collapse `--` → `slug-requirements.md`." Example for comparability: "N=5, K=2 → ⌈5/2⌉=3, 2<3, non-comparable."

EX-5 Examples
 Severity: Minor
 Finding: example set lacks structural diversity — every example is a compact, single-instance, happy-path specimen.
 Location: every code block in the artifact follows the same template shape and length.
 Citation: best-practices snapshot, "Diverse."
 Fix: vary examples across length (compact vs verbose), state (full coverage vs partial), and edge case (empty, non-comparable, malformed).

RSN-1 Reasoning context
 Severity: Major
 Finding: non-obvious design decisions lack Reason clauses. Affected rules include worst-of-artifact aggregation, the ⌈N/2⌉ comparability threshold, the strict argument-resolution auto-accept ban, the ±5-point cross-run tolerance, and the 100% projection cap.
 Location: "Score is the minimum across comparable artifacts (worst-of)"; "an artifact is comparable iff it is present in ≥ ⌈N/2⌉ runs"; "No auto-accept — the user must confirm every proposed value even when there is a single high-confidence candidate"; "identical scores within ±5 points per (dimension, artifact) cell"; "Never project above 100%."
 Citation: best-practices snapshot, "Add context to improve performance."
 Fix: append a Reason clause to each. Example: "Reason: worst-of surfaces the artifact that constrains the skill's predictability — averaging masks a regression in a single artifact behind better-performing peers."

BRN-3 Branching and edge cases
 Severity: Minor
 Finding: the discovery prompt branches on three inputs but provides no catch-all for unrecognized inputs.
 Location: "Proceed with these artifacts? [y / refine / abort]" — mappings cover only y, refine, abort.
 Citation: in-house
 Fix: add an ELSE clause. Example: "Any other input — re-prompt with the same options without re-running discovery."

OUT-4 Output determinism
 Severity: Minor
 Finding: multiple instructions use negative framing where a positive form was available.
 Location: "Never silently dropped" — "Do not modify the analyzed skill or its outputs" — "Never project above 100%" — "Do not re-run the skill" — "No scratch work in the output" — "Numbers without evidence are not allowed".
 Citation: best-practices snapshot, "Tell Claude what to do instead of what not to do."
 Fix: rewrite to positive form. "Never project above 100%" → "Cap projected scores at 100%." "Do not modify the analyzed skill or its outputs" → "Write only the report file. Leave the analyzed skill and its outputs unchanged."

TOOL-2 Tool use
 Severity: Major
 Finding: parallel-tool-call discipline is unspecified. The skill drives multi-file reads in Phase 1 (skill files, substrate, N runs × M artifacts) with no guidance on parallel vs serial execution.
 Location: "Phase 1 — Ingest" — "Read into memory only — no writes yet" with bulleted file lists and no parallelism directive.
 Citation: best-practices snapshot, "Optimize parallel tool calling."
 Fix: add explicit guidance. Example: "Issue independent Read calls in parallel within each ingest sub-step (skill files, substrate, all runs). Sequence only where a value resolved in one read narrows the next."

DEF-2 Defaults and conflicts
 Severity: Minor
 Finding: two confirmation rules use overlapping language with no precedence declaration. The argument-resolution rule bans auto-accept; the discovery rule defines a strict auto-confirm condition. The scope distinction is implicit.
 Location: "The user must confirm every proposed value; never auto-accept." (Invocation section) / "Auto-confirm condition (strict). If all three hold ... skip the prompt" (Phase 0 step 3).
 Citation: in-house
 Fix: tighten scope on the never-auto-accept rule. Example: "The user must confirm every proposed argument value (outputs/skill/substrate/files); never auto-accept argument resolutions. Discovery confirmation is governed by the auto-confirm condition in Phase 0 step 3."

VER-1 Environment and version declaration
 Severity: Major
 Finding: target model is undeclared. Artifact contains version-sensitive instructions (literal scope statements, default-verbosity-adjacent length bounds, action stance per resolution surface, output-hygiene rules on CoT suppression).
 Location: bottom metadata table contains Version / Last Updated / Status only — no Target Model field.
 Citation: best-practices snapshot, "Prompting Claude Opus 4.7" + "Migration considerations."
 Fix: add "Target Model: claude-opus-4-7" to the metadata table, or declare "version-neutral" and verify each version-sensitive surface remains valid across Claude 4.x models.

VER-2 Environment and version declaration
 Severity: Minor
 Finding: revision metadata block is incomplete. Target Model, Target Environment, Best-Practices Ref, and Revision Source fields are absent.
 Location: bottom metadata table — fields present: Version, Last Updated, Status.
 Citation: in-house
 Fix: append the missing fields:
   | Target Model         | claude-opus-4-7                  |
   | Target Environment   | claude-code                      |
   | Best-Practices Ref   | 2026-05-17 snapshot              |
   | Revision Source      | improving-prompt-artifacts skill |

SUMMARY
Total criteria: 41
Passed: 26
Failed: 15
 — Blocking: 0
 — Major: 7
 — Minor: 8
Risk level: High — do not deploy

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-17 |
| Status       | Draft      |
