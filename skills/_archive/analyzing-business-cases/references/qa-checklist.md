<!-- version: 2.0 | author: chief-of-droids workspace | last_updated: 2026-04-03 -->

# QA Checklist

Structured QA reference for the analyzing-business-cases skill.
One section per workflow. Each item carries severity, artifact/section mapping, and pass/fail criteria.

**Severity (global — applies identically across all sections):**
- Blocking — workflow halts; output cannot be emitted until resolved
- Advisory — finding surfaced to user; workflow continues

---

## Authoring rules

Apply these rules when adding or modifying workflow sections.

1. One workflow = one QA section. Section header must match the workflow name exactly.
2. Add the new section as `## <workflow-name>`
3. Place Blocking rows before Advisory rows within each section
4. Any item that is Blocking in `challenge framing` must also appear as Advisory in `build framing` — build framing is a scaffolding workflow where gaps are marked `🔲`, not halted; challenge framing is the definitive quality gate where the same gap becomes Blocking
5. Update SKILL.md reference table: add the new workflow as a consumer of this file
6. Update the workflow file: add a step to read `references/qa-checklist.md`, specifying the relevant section by name

---

## build framing

> All items are Advisory — build framing is a scaffolding workflow. Gaps are marked `🔲 To be defined`, not blocking.
> Items 1–4 mirror the Blocking items in challenge framing (rule 4 above).
> Maps to: section names in FRAMING-template.md. "Cross-cutting" applies across all sections.
> Coverage: Problem, Client, Objectives, Constraints. Context and Solution are excluded —
> Context is stable background (no quality gate needed); Solution is intentionally thin at framing stage.

| Severity | Maps to | Item | Pass | Fail signal |
|---|---|---|---|---|
| Advisory | Problem | Problem statement specific and bounded | Single bounded problem; root-cause-anchored | Generic improvement goal; multiple problems; "we want to..." — mark `🔲` |
| Advisory | Problem | Root cause stated or hypothesised — not just symptoms | Causation present or explicitly hypothesised | Symptoms described without cause — mark `🔲` |
| Advisory | Client | Primary stakeholder (decision-maker) named or typed | Role or individual identified | Absent — mark `🔲` |
| Advisory | Objectives | Expected value measurable — KPI, metric, or threshold named | Specific metric or observable outcome present | "improve" / "better" / vague — mark `🔲` |
| Advisory | Problem | Status quo cost quantified or estimated | Numeric estimate or order-of-magnitude range | Qualitative description only — flag as open question |
| Advisory | Client | Secondary stakeholders (impacted, consulted) identified | At least one secondary role named | Absent — flag as open question |
| Advisory | Objectives | Time-to-value estimated — not open-ended | Timeline horizon or milestone present | Absent — flag as open question |
| Advisory | Constraints | At least one constraint listed | Budget, timeline, org, or technical constraint named | Absent — flag as open question |

---

## challenge framing

> This is the definitive quality gate. Items 1–4 mirror the Advisory items in build framing, promoted to Blocking.
> Maps to: section names in FRAMING-template.md. "Cross-cutting" applies across all sections.
> Coverage: Problem, Client, Objectives, Constraints. Context and Solution are excluded —
> Context is stable background (no quality gate needed); Solution is intentionally thin at framing stage.

| Severity | Maps to | Item | Pass | Fail signal |
|---|---|---|---|---|
| Blocking | Problem | Problem statement specific and bounded | Single bounded problem; root-cause-anchored | Generic / multi-problem |
| Blocking | Problem | Root cause stated or hypothesised | Causation or hypothesis present | Symptoms only |
| Blocking | Client | Primary stakeholder (decision-maker) named or typed | Role or individual identified | Absent |
| Blocking | Objectives | Expected value measurable — KPI, metric, or threshold named | Specific metric or observable outcome | Vague outcome |
| Blocking | Constraints | Scope boundary explicit — out-of-scope items stated | At least one explicit exclusion present | Implied scope only; no exclusion stated |
| Blocking | Problem + Constraints | No scope creep — single focused problem across all sections | One problem, consistent throughout | Multiple unrelated problems; "also" / "and we also need" |
| Blocking | Objectives | Value linked to a stakeholder need — not a technology capability | Each objective traces to a named stakeholder in Client section | Tech-led objective: "X enables us to use Y" |
| Advisory | Problem | Status quo cost estimated | Numeric or order-of-magnitude estimate | Qualitative only |
| Advisory | Client | Secondary stakeholders identified | At least one secondary role named | Absent |
| Advisory | Objectives | Time-to-value estimated | Horizon or milestone present | Absent |
| Advisory | Constraints | Constraints listed | At least one constraint across budget, timeline, org, technical | Absent |
| Advisory | Cross-cutting | Key assumptions named — not buried in narrative | `⚠️ Assumed` flags present or dedicated section | Assumptions implied in narrative without surfacing |
| Advisory | Cross-cutting | At least one risk or dependency identified | Risk, dependency, or external blocker named | None present |
| Advisory | Cross-cutting | No unsupported superlatives | No "best / only / most efficient / leading" without citation | Superlative present without evidence |

---

## assess-artifacts

> Maps to: "Execution" = workflow execution context; artifact pair notation = transition being checked.

| Severity | Maps to | Item | Pass | Fail signal |
|---|---|---|---|---|
| Blocking | Execution | `challenge-framing.md` read via filesystem tool before step 4 | Filesystem read completed | challenge-framing invoked from memory |
| Blocking | Execution | No artifact rewritten during assess-artifacts — findings only | Output is gap table only | Artifact modified or rewrite proposed without user request |
| Blocking | Any artifact | Each artifact is versioned and dated | Version and date present on all artifacts read | Unversioned or undated artifact present — content checks suspended |
| Blocking | FRAMING → CLAUDE.md | Objective in CLAUDE.md matches FRAMING problem statement | Direct traceability present | Objective diverges or is absent |
| Blocking | FRAMING → CLAUDE.md | Target audience in CLAUDE.md matches FRAMING stakeholder map | Audience consistent across both | Mismatch or CLAUDE.md audience absent |
| Blocking | FRAMING → CLAUDE.md | No new scope introduced in CLAUDE.md not present in FRAMING | Scope boundary consistent | New problem or feature added in CLAUDE.md |
| Blocking | Any artifact | Each artifact section maps to a CLAUDE.md item or a FRAMING objective | Every section has explicit traceability | Orphaned section — no FRAMING or CLAUDE.md anchor |
| Advisory | Execution | Missing artifacts skipped — not blocked | Absent artifacts noted in gap table; assess-artifacts continues | Assess-artifacts halted due to missing artifact |
| Advisory | Execution | Gap table complete — all four columns per row | All rows have: Transition / Maturity / Content / Blocking issues | Column missing or row incomplete |
| Advisory | FRAMING → CLAUDE.md | Architecture Selection Criteria traceable to FRAMING constraints | Each criterion maps to a FRAMING constraint | Criterion present but untraceable |

| Field        | Value      |
|--------------|------------|
| Version      | 2.0        |
| Last Updated | 2026-04-03 |
| Status       | Final      |
