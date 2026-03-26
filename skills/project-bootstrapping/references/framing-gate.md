<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-03-25 -->

# Framing Gate

Gate protocol run after FRAMING.md is first written in Phase 3 of the bootstrap workflow.
Blocks progression to CLAUDE.md until the user issues `approve framing`.

---

## When This Runs

After `✅ Written: [REPO_NAME]/FRAMING.md` is confirmed.
Fires automatically — no user trigger required.

---

## Path Resolution

FRAMING.md path is already known from the write step: `workspace/[REPO_NAME]/FRAMING.md`
Re-read the file via Filesystem tool before running assessment — do not assess from memory.

---

## Blocking Criteria

Seven items are blocking. All must pass before `approve framing` is accepted.
Map each item to its FRAMING-template.md section before evaluating.

| # | Item | Section | Pass condition | Fail condition |
|---|---|---|---|---|
| B1 | Problem statement is specific | `## Problem` | Names a specific broken or missing condition within the stated context | Generic ("we need better data"), symptomatic only, or section is absent |
| B2 | Root cause stated or hypothesised | `## Problem` | States or hypothesises why the problem exists — not just what it is | Describes symptoms only; no causal reasoning present |
| B3 | Primary stakeholder named or typed | `## Client` | Names a person, role, or typed audience (e.g. "CFO", "ops team") | "The business", "stakeholders", or section is absent |
| B4 | Expected value is measurable | `## Objectives` | At least one objective names a KPI, metric, or observable threshold | All objectives are activities or generic outcomes ("improve efficiency") |
| B5 | Value linked to stakeholder need | `## Objectives` + `## Client` | At least one objective is traceable to a named stakeholder from `## Client` | Objectives exist but cannot be connected to any stakeholder in `## Client` |
| B6 | Scope boundary explicit | `## Constraints` | States at least one explicit out-of-scope boundary | Constraints section lists only technical limits; no scope exclusion stated |
| B7 | No scope creep signals | all sections | A single coherent problem thread runs through Problem → Objectives → Solution | Multiple unrelated problems or objectives that do not trace to the same Problem statement |

---

## Advisory Criteria

Seven items are advisory. Surface all findings but do not block progression.

| # | Item | Section | Note |
|---|---|---|---|
| A1 | Status quo cost quantified or estimated | `## Context` + `## Problem` | Strengthens the business case — flag if absent |
| A2 | Secondary stakeholders identified | `## Client` | Useful for downstream outputs — flag if absent |
| A3 | Time-to-value estimated | `## Objectives` | Anchors delivery expectations — flag if absent |
| A4 | Constraints listed | `## Constraints` | Section can be thin and FRAMING still functions — flag if empty |
| A5 | Key assumptions named | n/a | No dedicated template section — flag if none surfaced anywhere in FRAMING |
| A6 | At least one risk identified | n/a | No dedicated template section — flag if none surfaced anywhere in FRAMING |
| A7 | No unsupported superlatives | all sections | Flag any instance of "best", "most efficient", "only solution" without supporting evidence |

---

## Assessment Output Format

```
## FRAMING Assessment — [REPO_NAME]

### Blocking issues
| # | Item | Section | Finding |
|---|---|---|---|
| B1 | Problem statement is specific | ## Problem | [pass / fail + one-line finding] |
...

### Advisory issues
| # | Item | Finding |
|---|---|---|
| A1 | Status quo cost quantified | [pass / flag + one-line finding] |
...

X blocking issues. Y advisory issues.
```

If zero blocking issues:
```
✅ No blocking issues — FRAMING is structurally sound.
[advisory findings if any]
Type `approve framing` to proceed to CLAUDE.md, or address advisory items first.
```

If blocking issues remain:
```
⛔ X blocking issue(s) — resolve before proceeding.
[findings table]
Options:
  (a) Edit FRAMING.md yourself, then type `re-assess`
  (b) Ask Claude to propose fixes — type `fix [B1, B2, ...]`
```

---

## Loop Protocol

### `re-assess`
Re-read `workspace/[REPO_NAME]/FRAMING.md` from disk.
Run full assessment (all 14 items).
Output assessment in standard format.
Do not carry forward findings from a prior loop iteration — always assess fresh.

### `fix [B-numbers]` or "fix it" or "fix all"
For each named blocking item (or all blocking items if unspecified):
1. Propose edit in chat — show exact replacement text for the relevant section
2. Await user confirmation ("yes" / "confirmed" or equivalent)
3. Write updated FRAMING.md to disk immediately on confirmation
4. Auto-trigger `re-assess` — state: `Re-assessing after edits...`

Advisory items: propose fix only if user explicitly requests it.
Never fix an item the user did not ask about.

### `approve framing`
Re-run blocking criteria assessment inline (do not rely on prior output).
If zero blocking issues: confirm and proceed — `✅ FRAMING approved — generating CLAUDE.md`
If blocking issues remain: refuse — `⛔ Cannot approve — [X] blocking issue(s) remain: [list]`

---

## Constraints

- Never skip the gate — it fires after every FRAMING.md write, including loop rewrites
- Never modify FRAMING.md without a user-initiated fix request
- Never carry assessment state between turns — always re-read and re-assess
- Advisory findings do not block `approve framing` under any circumstance

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-03-25 |
| Status       | Draft      |
