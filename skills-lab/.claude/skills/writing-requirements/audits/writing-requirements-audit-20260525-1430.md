AUDIT REPORT
Artifact: /Users/gilllesmourgues/Workspace/chief-of-droids/skills-lab/.claude/skills/writing-requirements/SKILL.md
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

EX-1 Examples
 Severity: Major
 Finding: three non-trivial format rules carry only one example each; range below the 3–5 threshold for the rule shape.
 Location: Phase 3 glossary extraction (one walkthrough); Phase 2 ERR opt-out rationale (one entry); Phase 4 sparse-ID edge case (one substrate excerpt).
 Citation: best-practices snapshot, "Include 3–5 examples for best results."
 Fix: add two further examples to each — glossary needs an all-stop-word paragraph + a substrate-defined-term paragraph; ERR opt-out needs a Mutate-shape FR with rationale + an Acquire-shape FR with rationale; Phase 4 needs duplicate-ID + missing-glossary-term variants.

EX-2 Examples — edge cases
 Severity: Minor
 Finding: Phase 3 and Phase 2 ERR sections show only happy-path examples; the empty-paragraph, all-stop-word, and contract-shape-without-rationale edge cases described in prose are never demonstrated.
 Location: Phase 3 "Sample paragraph from substrate"; Phase 2 "FR-008 ... (no ERR — rationale: ...)"
 Citation: best-practices snapshot, "Diverse: cover edge cases."
 Fix: add at least one edge-case example per affected rule — an all-stop-word paragraph showing empty glossary result; an Acquire-shape FR missing both ERR and rationale showing Phase 4 Warning emission.

EX-4 Demonstration where possible
 Severity: Major
 Finding: several rules describe behavior demonstrable inline but show no example — §Scope extraction patterns, §Actors & Consumers extraction, §Purpose inference fallback, Phase 5 AC derivation, version increment chain.
 Location: "In Scope: extract from positive language — 'in scope', 'covers'..."; "**§ Actors & Consumers** Extract upstream/downstream..."; "Follow `references/verification.md` for: §Acceptance Criteria ..."; "increment rightmost segment (`0.1 → 0.2`). Initial value: `0.1`."
 Citation: best-practices snapshot, "Examples are one of the most reliable ways to steer Claude's output."
 Fix: add worked examples — a Scope paragraph with positive/negative phrasings and resulting In/Out partitions; an Actors paragraph with upstream/downstream/role split; a Purpose inference from leading prose; a per-requirement AC derivation example; a 3-run version chain (no prior → 0.1; 0.1 → 0.2; 0.2 → 0.3).

RSN-1 Reasoning context
 Severity: Major
 Finding: four non-obvious rules carry no Reason clause; principle for unlisted edge cases is unrecoverable.
 Location: slug reserved tokens "must not contain `requirement`, `req`, or `reqs`"; "Initial value: `0.1`. Status: always `Draft`"; "Adding a term requires editing this list"; "absent rationale + absent ERR is a Phase 4 Warning".
 Citation: best-practices snapshot, "Add context to improve performance."
 Fix: append Reason clauses encoding intent — slug-token: "Reason: these tokens collide with output filename `<slug>-requirements.md` producing self-referential paths like `payment-requirements-requirements.md`"; Status-Draft: "Reason: outputs are iteratively re-fed as substrate; Final status is set by the user post-review, never by the skill"; stop-word list: "Reason: list immutability is the audit trail — every addition is reviewed in commit history rather than mutating silently per run"; ERR opt-out: "Reason: explicit rationale forces the engineer to acknowledge the coverage gap is intentional, preventing accidental ERR omission from passing silently."

RSN-3 Reasoning context — chain-of-thought
 Severity: Minor
 Finding: chain-of-thought behavior is not explicitly addressed; the phase-stream emission implicitly bounds intermediate output, but the artifact never states whether internal reasoning may appear outside phase-header lines and hard-fail blocks.
 Location: "Stream one header line per phase as it begins" + emission format spec; no companion suppression rule.
 Citation: best-practices snapshot, "Leverage thinking" + "Migrating away from prefilled responses."
 Fix: add an execution rule near the phase-model section — "Reason internally between phase transitions. Emit only phase-header lines, hard-fail blocks, and the closure line per format spec. Do not include reasoning narration."

BRN-2 Branching and edge cases
 Severity: Minor
 Finding: malformed-input edge cases described in passing are not enumerated — empty substrate file, substrate with whitespace only, IDs in non-canonical format (FR_001, FR-0001), substrate matching .md extension but containing non-markdown bytes.
 Location: Phase 0.8 "Read substrate file; reject non-`.md` extension"; Phase 2 ID regex `\b(FR|...)-\d{3}\b`.
 Citation: in-house.
 Fix: enumerate the silent-pass cases — "empty substrate (0 bytes): hard-fail Phase 0.8"; "substrate with whitespace only: Phase 1 emits Warning, all sections N/A"; "IDs with non-canonical separator (FR_001) or non-canonical width (FR-0001): treated as un-IDed, assigned next available; Phase 4 Warning surfaces the mismatch."

OUT-3 Output determinism — failure modes
 Severity: Minor
 Finding: behavior on empty substrate not explicitly specified; Phase 0.8 rejects non-.md extension but does not state what happens when the .md file is 0 bytes or whitespace-only.
 Location: Phase 0.8 "Read substrate file; reject non-`.md` extension | Hard-fail"
 Citation: in-house.
 Fix: extend Phase 0.8 — "Reject non-`.md` extension OR empty file (0 bytes) OR whitespace-only file. Hard-fail in all three cases. Remediation: provide a substrate with at least one paragraph of prose."

OUT-4 Positive framing
 Severity: Minor
 Finding: no global positive-framing stance statement; per-section negatives ("No synthesis when signal is absent", "Do not infer", "Never humanise the slug") remain without a single positive principle that subsumes them.
 Location: §Scope "Each subsection: `N/A` + Warning if signal absent. No synthesis when signal is absent."; §Title "Never humanise the slug"; Phase 2 "Do not defer to Phase 4".
 Citation: best-practices snapshot, "Tell Claude what to do instead of what not to do."
 Fix: add one positive global stance near the top of the artifact — "Default to conservative emission: when substrate signal is absent or ambiguous, emit `N/A` + Warning and proceed. Synthesis, inference, and paraphrase are permitted only where a rule explicitly grants them (Purpose inference under §Title + Purpose is the sole current exception)."

TOOL-2 Parallel tool calling
 Severity: Minor
 Finding: artifact drives multiple Read calls in Phase 0 (substrate + conventions.md + template-s1/s2.md + optionally prior `<slug>-requirements.md`) without stating parallel-vs-serial discipline.
 Location: Phase 0 steps 0.7–0.10 — four independent Read operations with no dependency ordering.
 Citation: best-practices snapshot, "Optimize parallel tool calling."
 Fix: add to Phase 0 — "Reads in steps 0.7–0.10 are independent (no dependencies between them). Issue them as parallel tool calls in a single response. Reason: latency reduction; no read depends on another's output."

TOOL-3 Tool use — action stance
 Severity: Minor
 Finding: action stance is not declared; whether the skill runs the full pipeline by default or pauses for clarification on ambiguous substrate is unspecified.
 Location: no action-stance statement; phase model implies proactive execution but is not declared.
 Citation: best-practices snapshot, "Tool usage."
 Fix: add near the phase model — "Action stance: proactive. On invocation, execute Phase 0 through Phase 6 without intermediate clarification prompts. Ambiguity in substrate signal is resolved by emitting `N/A` + Warning, not by halting for user input. Hard-fail conditions in Phase 0 are the sole grounds for halting."

SUMMARY
Total criteria: 41
Passed: 30
Failed: 11
 — Blocking: 0
 — Major: 3
 — Minor: 8
Risk level: High — do not deploy

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-25 |
| Status       | Draft      |
