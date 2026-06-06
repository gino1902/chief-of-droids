AUDIT REPORT
Artifact: /Users/gilllesmourgues/Workspace/chief-of-droids/skills-lab/.claude/skills/writing-requirements/SKILL.md
Target Environment: claude-code (inferred from strong contextual signals: frontmatter with name/description/allowed-tools, tool references Read/Write, relative path references/conventions.md)
Target Model: undeclared
Best-Practices Ref: 2026-05-17 snapshot
Date: 2026-05-18
Auditor: claude-opus-4-7

VIOLATIONS

STR-2 Structure and separation
 Severity: Major
 Finding: top-level components (role, instructions, examples, output-format, execution-rules) are separated only by markdown headers — no XML tag boundaries.
 Location: "## Reference files ... ## Invocation ... ## Phase model ... ## Phase 0 — Pre-flight"
 Citation: best-practices snapshot, "Structure prompts with XML tags."
 Fix: wrap top-level components in named XML tags — <role>, <invocation>, <phase-model>, <execution-rules>, <output-format>. Keep markdown inside each tag for tables and sub-structure.

EX-1 Examples
 Severity: Major
 Finding: no rule in the artifact carries 3–5 worked examples. The phase-stream output, the hard-fail format, and the title fallback rule each show one example only.
 Location: "→ Phase 0 — Pre-flight ... ✓ Wrote <slug>-requirements.md (v0.2)" (single example); title example "for slug `chief-of-droids-3-tiers-upgrade-v01`" (single example).
 Citation: best-practices snapshot, "Include 3–5 examples for best results."
 Fix: add 3–5 examples to each non-trivial format rule — invocation parsing (valid/invalid slug/missing --type/duplicate `from`), hard-fail emission across different phases, title fallback chain firing at H1/H2/frontmatter/slug, and ID stability preservation across requirement categories.

EX-2 Examples — edge cases
 Severity: Major
 Finding: examples present cover only the happy path (e.g., one well-shaped slug, one normal phase stream). Edge cases — empty substrate, malformed slug, missing --type, substrate with no H1/H2/frontmatter, ID gaps — are described in prose but never demonstrated.
 Location: "fallback: slug + Warning. ... Never humanise the slug — emit it verbatim"
 Citation: best-practices snapshot, "Diverse: cover edge cases."
 Fix: add edge-case worked examples — a substrate with no H1/H2/frontmatter showing the slug-fallback Warning verbatim; an invocation with reserved token "requirements" showing the hard-fail emission; a substrate with sparse ID sequence showing Phase 4 Warning output.

EX-4 Demonstration where possible
 Severity: Major
 Finding: multiple rules describe behavior without demonstration where demonstration is feasible. Argument parsing rules (table at line 38–45), the glossary auto-extraction rules (4 rules at Phase 3), the ID regex `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b`, and the ERR-coverage rationale format `(no ERR — rationale: <reason>)` are all stated without a worked example.
 Location: "scan substrate for declared IDs matching `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b`"
 Citation: in-house; aligned with "Examples are one of the most reliable ways to steer Claude's output."
 Fix: add concrete examples — show an ID-bearing substrate excerpt and the preserved IDs in the output; show a glossary extraction pass over a sample paragraph with the four rules firing visibly; show an ERR opt-out rationale attached to a verbatim FR entry.

EX-5 Examples — structural diversity
 Severity: Minor
 Finding: the few examples present are structurally uniform — short single-line slug strings and a single phase-stream block. No variation across input length, content domain, or edge-vs-typical case.
 Location: example set across the artifact is small and uniform.
 Citation: best-practices snapshot, "Diverse."
 Fix: when adding examples per EX-1/EX-2/EX-4, vary input shape — short and long substrates, sparse and dense ID sets, single-category and multi-category requirement sets.

RSN-1 Reasoning context
 Severity: Major
 Finding: several non-obvious rules carry no Reason clause. "No writes until Phase 6 completes." (line 16) — non-obvious atomicity guarantee. "Write order: `<slug>-requirements.md` first, then `<slug>-report.md`." (line 174) — non-obvious ordering with downstream consequence. "Commit gate suppressed for this skill; user commits post-run." (line 181) — non-obvious override of workspace default.
 Location: "No writes until Phase 6 completes."
 Citation: best-practices snapshot, "Add context to improve performance."
 Fix: append Reason clauses. Example: "No writes until Phase 6 completes. Reason: the seven phases form an all-or-nothing transaction — partial writes leave the workspace in an inconsistent state where downstream consumers cannot tell whether the run completed or was aborted mid-pipeline."

RSN-3 Reasoning context — chain-of-thought
 Severity: Minor
 Finding: chain-of-thought behavior is unspecified. The artifact runs seven sequential phases internally but does not state whether intermediate reasoning should appear in chat output or be suppressed beyond the phase-header stream.
 Location: no CoT instruction present.
 Citation: best-practices snapshot, "Leverage thinking."
 Fix: add an explicit instruction. Example: "Reason internally between phases. Surface only the phase header line per Phase. Do not narrate intermediate decisions in chat."

OUT-2 Output length and bounds
 Severity: Minor
 Finding: output length is unbounded. The two output files inherit their bounds implicitly from `template-s1.md` / `template-s2.md`; the artifact itself states no upper bound for sections, glossary entries, or report findings.
 Location: no explicit length bound stated.
 Citation: best-practices snapshot, "Response length and verbosity."
 Fix: add explicit bounds where unbounded growth is a defect — cap glossary candidate count, cap Warning emission per phase, or explicitly state "no upper bound; bound is set by substrate content" if unbounded is intentional.

OUT-4 Positive framing
 Severity: Minor
 Finding: instructions use negative framing where positive form was possible.
 Location: "Never humanise the slug — emit it verbatim" / "do not derive it from the input path" / "No writes until Phase 6 completes" / "Do not defer to Phase 4" / "No synthesis when signal is absent" / "Commit gate suppressed for this skill"
 Citation: best-practices snapshot, "Tell Claude what to do instead of what not to do."
 Fix: rewrite positively where unambiguous.
   Incorrect: "Never humanise the slug — emit it verbatim"
   Correct:   "Emit the slug verbatim as the Title."
   Incorrect: "do not derive it from the input path"
   Correct:   "Derive the slug from the first positional token; treat the input path as unrelated."
   Retain negative framing only where the positive form is genuinely ambiguous (e.g., "No writes until Phase 6 completes" — positive form would be longer and weaker).

TOOL-2 Parallel tool calling
 Severity: Minor
 Finding: parallel-vs-serial discipline is unspecified for the multiple Read calls the skill issues. Phase 0 alone reads up to four files (substrate, prior requirements, conventions.md, one template) plus the EARS/RFC/tables references in Phase 1.
 Location: "Read substrate file" / "Read prior `<slug>-requirements.md`" / "Read `references/conventions.md`" / "Read `references/template-s1.md` or `references/template-s2.md`"
 Citation: best-practices snapshot, "Optimize parallel tool calling."
 Fix: add explicit guidance. Example: "Within a single phase, issue all independent Read calls in parallel — substrate, prior requirements file, and reference files have no dependency between them. Cross-phase reads remain sequential."

TOOL-3 Tool use — action stance
 Severity: Minor
 Finding: the artifact does not declare action stance (proactive vs conservative) on ambiguous inputs. It hard-fails on parsing ambiguity (good), but on softer cases — e.g., when a substrate signal is borderline (extractable vs synthesizable) — the stance is "no synthesis when signal is absent" inline but not stated globally.
 Location: no global stance declaration.
 Citation: best-practices snapshot, "Tool usage."
 Fix: add a global stance statement. Example: "Default to conservative action: when substrate signal is absent or ambiguous, emit `N/A + Warning`. Do not infer, synthesize, or paraphrase to fill gaps."

VER-1 Version declaration
 Severity: Major
 Finding: target Claude model version is undeclared. The artifact contains version-sensitive surfaces — literalism (OBL-5), proactive-by-default behavior (TOOL-3), explicit ERR-coverage protocol that depends on the model's ability to apply matrix-style classification.
 Location: no version declaration in frontmatter or version block.
 Citation: best-practices snapshot, "Prompting Claude Opus 4.7" + "Migration considerations."
 Fix: add `target-model: claude-opus-4-7` (or `version-neutral` with rationale) to frontmatter or the bottom metadata table.

VER-2 Revision metadata
 Severity: Minor
 Finding: the artifact's bottom metadata block carries only Version / Last Updated / Status fields. Missing: Target Model, Target Environment, Best-Practices Ref, Revision Source.
 Location: no revision metadata block present in the artifact (no full metadata table at file end).
 Citation: in-house
 Fix: when fixes are applied via this skill, append the full metadata block at the bottom — Target Model, Target Environment, Best-Practices Ref, Last Revised, Revision Source. Audit-only runs flag Minor.

SUMMARY
Total criteria: 41
Passed: 28
Failed: 13
 — Blocking: 0
 — Major: 6
 — Minor: 7
Risk level: High — do not deploy

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-18 |
| Status       | Draft      |
