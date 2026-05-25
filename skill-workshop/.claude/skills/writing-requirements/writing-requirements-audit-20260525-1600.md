AUDIT REPORT
Artifact: /Users/gilllesmourgues/Workspace/chief-of-droids/skill-workshop/.claude/skills/writing-requirements/SKILL.md
Target Environment: claude-code (declared in bottom metadata block; corroborated by frontmatter name/description/allowed-tools, Read/Write tool references, relative paths to references/)
Target Model: claude-opus-4-7 (declared in HTML comment line 9 and bottom metadata block)
Best-Practices Ref: 2026-05-17 snapshot
Date: 2026-05-25
Auditor: claude-opus-4-7

VIOLATIONS

OBL-4 Obligation language
 Severity: Minor
 Finding: Purpose extraction defines a judgment rule (inference permitted when explicit statement absent) without a Reason clause explaining why inference is acceptable here while it is forbidden for Title.
 Location: "Purpose: extract explicit purpose statement ...; if absent, infer from leading prose + Warning."
 Citation: best-practices snapshot, "Add context to improve performance."
 Fix: append "Reason: Purpose is rhetorical framing recoverable from leading prose without semantic loss; Title is an identifier where fabrication would mask substrate mis-shape."

EX-2 Examples — edge cases
 Severity: Minor
 Finding: three rules show only happy-path examples; described edge cases are not demonstrated — §Scope extraction (no missing-signal example), §Actors & Consumers extraction (no missing-signal example), ERR opt-out rationale (all three examples carry rationales; the rationale-absent-with-mandatory-shape case that produces a Phase 4 Warning is described in prose only).
 Location: "**Scope extraction example** ... Extraction: In Scope: ... Out of Scope: ..."; "**Actors & Consumers extraction example** ... Upstream actors: ... Downstream consumers: ..."; "**ERR opt-out rationale examples** Validate-shape ... Mutate-shape ... Acquire-shape ..."
 Citation: best-practices snapshot, "Diverse: cover edge cases."
 Fix: add edge-case example to each affected rule — a substrate paragraph with no Scope signal showing both subsections render `N/A` + Warning; a substrate paragraph with no Actors signal showing `N/A` + Warning; an Acquire-shape FR with neither ERR nor rationale showing the Phase 4 Warning emission.

RSN-3 Reasoning context — chain-of-thought
 Severity: Minor
 Finding: chain-of-thought behavior is not explicitly addressed. The phase-stream emission format implicitly bounds intermediate output to header lines, hard-fail blocks, and the Phase 4 closure line, but the artifact never states that internal reasoning between phases must remain unsurfaced.
 Location: "Stream one header line per phase as it begins" + the emission format spec block; no companion suppression rule.
 Citation: best-practices snapshot, "Leverage thinking" + "Migrating away from prefilled responses."
 Fix: add an execution rule under `<phase-model>` — "Reason internally between phase transitions. Emit only phase-header lines, hard-fail blocks, and the closure line per format spec. Do not include reasoning narration in output."

BRN-2 Branching and edge cases
 Severity: Minor
 Finding: substrate-malformed cases described in passing are not enumerated as explicit behavior contracts — empty substrate file (0 bytes), substrate with whitespace only, IDs in non-canonical format (FR_001 with underscore separator, FR-0001 with four-digit width).
 Location: Phase 0.8 "Read substrate file; reject non-`.md` extension | Hard-fail"; Phase 2 ID regex `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b`.
 Citation: in-house.
 Fix: enumerate these cases — "Phase 0.8 also rejects empty files (0 bytes) and whitespace-only files: Hard-fail"; "non-canonical IDs (wrong separator, wrong digit width) are not matched by the ID regex and are treated as un-IDed; the next-available-ID assignment proceeds; Phase 4 emits a Warning citing the unmatched pattern."

OUT-3 Output determinism — failure modes
 Severity: Minor
 Finding: behavior on empty or whitespace-only substrate is not specified. Phase 0.8 rejects non-`.md` extension but is silent on `.md` files that contain no parseable content.
 Location: Phase 0.8 "Read substrate file; reject non-`.md` extension | Hard-fail"
 Citation: in-house.
 Fix: extend Phase 0.8 — "Reject non-`.md` extension OR empty file (0 bytes) OR whitespace-only file. Hard-fail in all three cases. Remediation: provide a substrate with at least one paragraph of prose."

OUT-4 Positive framing
 Severity: Minor
 Finding: no global positive-framing stance statement; per-section negatives ("No synthesis when signal is absent", "Never humanise the slug", "Do not defer to Phase 4", "do not derive it from the input path") remain without a single positive principle that subsumes them.
 Location: §Scope "Each subsection: `N/A` + Warning if signal absent. No synthesis when signal is absent."; §Title "Never humanise the slug"; Phase 2 "Do not defer to Phase 4"; <invocation> "do not derive it from the input path".
 Citation: best-practices snapshot, "Tell Claude what to do instead of what not to do."
 Fix: add one positive global stance near the top of the artifact, before the `<reference-files>` block — "Default to conservative emission: when substrate signal is absent or ambiguous, emit `N/A` + Warning and proceed. Synthesis, inference, and paraphrase are permitted only where a rule explicitly grants them (Purpose inference under §Title + Purpose is the sole current exception)."

TOOL-2 Parallel tool calling
 Severity: Minor
 Finding: Phase 0 issues four independent Read calls (steps 0.7, 0.8, 0.9, 0.10) without stating parallel-vs-serial discipline. The reads have no dependencies between them.
 Location: Phase 0 step table — `Read prior <slug>-requirements.md`; `Read substrate file`; `Read references/conventions.md`; `Read references/template-s1.md or references/template-s2.md`.
 Citation: best-practices snapshot, "Optimize parallel tool calling."
 Fix: add a note under the Phase 0 step table — "Reads in steps 0.7–0.10 are independent. Issue them as parallel tool calls in a single response. Reason: no read depends on another's output; serial execution wastes latency."

TOOL-3 Tool use — action stance
 Severity: Minor
 Finding: action stance is not declared. Whether the skill runs Phase 0 through Phase 6 without intermediate clarification, or pauses when substrate signal is ambiguous, is unspecified.
 Location: no action-stance statement in the artifact; phase model implies proactive execution but does not declare it.
 Citation: best-practices snapshot, "Tool usage."
 Fix: add near the `<phase-model>` block — "Action stance: proactive. On invocation, execute Phase 0 through Phase 6 without intermediate clarification prompts. Ambiguity in substrate signal is resolved by emitting `N/A` + Warning, not by halting for user input. Hard-fail conditions in Phase 0 are the sole grounds for halting."

SUMMARY
Total criteria: 41
Passed: 33
Failed: 8
 — Blocking: 0
 — Major: 0
 — Minor: 8
Risk level: High — do not deploy

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-25 |
| Status       | Draft      |
