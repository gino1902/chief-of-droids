<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-04-06 -->

# QA Checklist Template

Reference for the `author skill` workflow in `creating-skills`.
Read this file before authoring a QA checklist for any new skill.

**Purpose:** defines the item format, severity model, placement decision rule,
and minimum coverage requirements for skill QA checklists. Every skill authored
by `creating-skills` must have a QA checklist conforming to this template.

---

## Item Format

Each checklist item is a table row with five columns:

```markdown
| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Blocking / Major / Minor | Hard gate / Output quality / Style | What must be true | Observable condition that constitutes passing | What Claude surfaces or does on failure |
```

**Column definitions:**

| Column | Content |
|:-------|:--------|
| Severity | One of three labels: `Blocking`, `Major`, `Minor` |
| Maps to | The workflow element this item governs — hard gate, reference file read, output write, path detection, failure handling, etc. |
| Item | The assertion — what must hold; observable outcome, not a process step |
| Pass | Exact condition that constitutes passing — checkable without inference |
| Fail signal | What Claude must surface or do when this item does not hold |

**Severity definitions:**

| Severity | Meaning | Fail behaviour |
|:---------|:--------|:---------------|
| Blocking | Hard gate or silent failure risk — execution must not continue if this fails | Halt and surface specific violation before proceeding |
| Major | Output quality or trigger accuracy degrades if this fails | Flag finding; do not present output as fully reliable |
| Minor | Style or optimisation issue | Note opportunistically; does not block output |

**Rules:**
- Every item must be independently verifiable — Pass column fully defines what passing looks like
- Items describe observable outcomes, not process steps
- No severity inflation — a preference is Minor, a correctness gate is Blocking
- Blocking items must be traceable to a hard gate, silent failure risk, or data-loss condition in the skill's workflow
- Fail signal must prescribe a specific action — not "handle appropriately"

---

## Placement Decision Rule

After authoring the full item table, apply this rule to determine file placement:

**Step 1 — Count branch-exclusive items.**
An item is branch-exclusive if it applies to one workflow or path only
(e.g. Path 1 only, `author skill` only, framing workflow only).

**Step 2 — Compute the branch-exclusive ratio.**

```
branch-exclusive items ÷ total items
```

**Step 3 — Apply threshold.**

| Ratio | Placement |
|:------|:----------|
| < 50% branch-exclusive | **Unified** — single `references/qa-checklist.md`; group items under workflow section headings |
| ≥ 50% branch-exclusive | **Split** — one file per workflow branch; see naming convention below |

**Split file naming convention:**

```
references/qa-checklist-[workflow-name].md
```

Examples:
- `references/qa-checklist-author.md`
- `references/qa-checklist-critique.md`
- `references/qa-checklist-path1.md`

Each split file must open with a one-line scope statement:

```
<!-- Scope: [workflow or path name] only -->
```

When split files are used, SKILL.md's Reference Files section must list each
file individually with its scope stated.

---

## Minimum Coverage Requirements

### All skills

| Area | Minimum Blocking items |
|:-----|:----------------------|
| Trigger detection | 1 — correct trigger fires; wrong trigger does not |
| Reference file reads | 1 per declared reference file — read confirmed before use |
| Output written only on approval | 1 — no write without explicit user confirmation |
| Failure handling | 1 — missing file or tool error surfaced, not silently skipped |

### Workflow-class skills (>3 sequential steps, conditional branching, or stateful output)

All-skills minimums apply, plus:

| Area | Minimum items |
|:-----|:-------------|
| Hard gates | 1 Blocking per hard gate declared in the workflow |
| Path/branch coverage | 1 Major per distinct path — correct path detected and followed |
| Completion condition | 1 Blocking — "done" is explicit, not implicit end-of-list |
| Cross-step data flow | 1 Major per step whose output is consumed by a later step |

### Reference-and-apply skills (formatters, domain advisors, single-pass tools)

All-skills minimums apply. Workflow-class additions do not apply.

---

## Checklist File Header

Every `qa-checklist.md` (unified or split) must open with this header block,
filled in for the skill being authored:

```markdown
<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: YYYY-MM-DD -->

# QA Checklist — [skill name]

Governs: `[skill-name]` skill
Format: table (Severity / Maps to / Item / Pass / Fail signal)
Placement: Unified | Split ([list split files if applicable])
Branch-exclusive ratio: N of M items are branch-specific (N%) — [below/above] 50% threshold; [unified/split] placement correct
```

---

## Authoring Sequence (within `author skill` workflow)

1. Draft the skill body and all workflow steps first
2. Read this template (`references/qa-template.md`)
3. Enumerate all hard gates, reference file reads, output writes, and failure
   conditions from the drafted skill
4. For each: assign severity, identify Maps to element, write Pass condition, write Fail signal
5. Apply the placement decision rule — compute ratio, choose unified or split
6. Draft the checklist file(s) with the required header
7. Verify minimum coverage requirements are met before proposing to user
8. Propose checklist alongside the skill draft — do not write either without
   explicit user approval

---

## Anti-Patterns

| Anti-pattern | Correct approach |
|:-------------|:----------------|
| Severity inflation — labelling preferences as Blocking | Reserve Blocking for hard gates and silent failure risks only |
| Untraceable Blocking items | Every Blocking item must point to a specific gate or failure mode in the skill |
| Process steps as items ("Claude reads the file") | Items describe outcomes ("Reference file read before workflow step executes") |
| Vague Pass column ("item holds") | Pass must be independently checkable without reading any other column |
| Vague Fail signal ("handle error") | Fail signal must prescribe a specific action: halt, flag, return to user, etc. |
| Duplicate items with different labels | Merge into one item at the higher severity |
| Checklist describes the happy path only | Include at least one item per declared failure condition |

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-04-06 |
| Status       | Active     |
