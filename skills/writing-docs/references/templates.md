# Document Templates Reference

Read this file when the user requests an ADR, Requirements Brief, Runbook, or Playbook.
Copy the relevant template and fill in all `{placeholder}` fields.
Apply formatting rules from `markdown-formatting.md` for `.md` output.

## Templates

1. [Architecture Decision Record (ADR)](#architecture-decision-record-adr)
2. [Requirements Brief](#requirements-brief)
3. [Runbook](#runbook)
4. [Playbook](#playbook)
5. [Corporate Document Chrome](./template-corporate-chrome.md) — composable wrapper for `.docx` deliverables
6. [Architecture Requirements](./template-architecture-requirements.md) — body schema; composes with chrome

---

## Architecture Decision Record (ADR)

```markdown
# ADR-{NNN} — {Decision Title}

> Status: Draft | Proposed | Approved | Superseded by ADR-{NNN}
> Author: {name / role}
> Date: {YYYY-MM-DD}
> Version: {X.X}
> Requirement ref: {Phase 1 requirement ID or section}

---

## Context

{One paragraph. Describe the situation that forced a decision. State the constraints,
drivers, and options that were on the table. Do not state the decision here.}

## Decision

{One or two sentences. State what was decided, not why. Start with "We will…"}

## Consequences

### Positive
- {Outcome enabled by this decision}
- {Outcome enabled by this decision}

### Negative / Trade-offs
- {Constraint or cost accepted by this decision}
- {Constraint or cost accepted by this decision}

### Risks
- {Risk introduced; note owner and mitigation if known}

## References
- {Link or path to upstream requirement}
- {Link or path to related ADR, design doc, or official source}

---

*Approved by: {name / role} — {YYYY-MM-DD}*
```

---

## Requirements Brief

```markdown
# Requirements Brief — {Project or Use Case Name}

> Version: {X.X}
> Author: {name / role}
> Date: {YYYY-MM-DD}
> Status: Draft | Under Review | Signed Off
> Signed by: {business sponsor} · {engineering sponsor}

---

## Objective

{One paragraph. State the business problem and the outcome expected from the platform
or system. Avoid solution framing — describe what must be true, not how to achieve it.}

## Scope

### In scope
- {Data domain, capability, or workload}
- {Data domain, capability, or workload}

### Out of scope
- {Explicitly excluded item — prevents scope creep}
- {Explicitly excluded item}

## Data Domains and Consumers

| Domain | Source systems | Primary consumers | Volume estimate | Latency requirement |
| :--- | :--- | :--- | :--- | :--- |
| {domain} | {sources} | {teams / products} | {rows/day or GB/day} | {batch / near-RT / RT} |

## Regulatory and Compliance Constraints

{List each constraint with its source (regulation, policy, or contractual obligation).
If none: state "None identified at this stage."}

| Constraint | Source | Impact |
| :--- | :--- | :--- |
| {constraint} | {regulation / policy} | {what it limits or requires} |

## Team and Maturity

| Dimension | Current state |
| :--- | :--- |
| Team size | {N engineers, N analysts} |
| Data engineering maturity | {Level 0–4 — see governance.md} |
| Cloud maturity | {description} |
| Tooling in use today | {list} |

## Budget Envelope

{State the approved or target budget range. If not yet defined: state "TBD — to be
established in Phase 6 Cost Modelling."}

## Success Criteria

{How will we know the platform is delivering value? State measurable outcomes.}

| Criterion | Measure | Target | Timeline |
| :--- | :--- | :--- | :--- |
| {criterion} | {metric} | {value} | {date or phase} |

## Open Questions

| # | Question | Owner | Due |
| :--- | :--- | :--- | :--- |
| 1 | {question} | {name / role} | {date} |

---

*This document must be signed by both business and engineering sponsors before
any architecture work begins (Phase 3 gate condition).*
```

---

## Runbook

```markdown
# Runbook — {Pipeline or System Name}

> Version: {X.X}
> Author: {name / role}
> Date: {YYYY-MM-DD}
> Scope: {what this runbook covers}
> Audience: {operators / on-call engineers / data engineers}

---

## Prerequisites

- {Access, permission, or tool required before starting}
- {Access, permission, or tool required before starting}

## Environment Reference

| Item | Value |
| :--- | :--- |
| Workspace URL | {url} |
| Job / pipeline name | {name} |
| Storage account | {name} |
| Key Vault | {name} |
| Log location | {path or URL} |

---

## Procedure — {Task Name}

### Step 1 — {Step title}

{Exact command or action. No ambiguity. Operator-executable as written.}

```{language}
{command}
```

Expected output: `{what success looks like}`

---

### Step 2 — {Step title}

{Action.}

Expected output: `{what success looks like}`

---

## Failure Modes and Recovery

| Symptom | Likely cause | Recovery action |
| :--- | :--- | :--- |
| {error or alert} | {cause} | {exact steps to recover} |
| {error or alert} | {cause} | {exact steps to recover} |

## Escalation

| Condition | Escalate to | Contact |
| :--- | :--- | :--- |
| {condition} | {role} | {Slack / email} |

---

*Review cadence: {monthly / quarterly / on pipeline change}*
*Last reviewed: {YYYY-MM-DD} by {name}*
```

---

## Playbook

```markdown
# Playbook — {Playbook Title}

> Version: {X.X}
> Author: {name / role}
> Date: {YYYY-MM-DD}
> Status: Draft | Under Review | Approved
> Audience: {intended readers}

---

## Table of Contents

<!-- Dynamic — update after all plays are finalized -->
1. [Introduction](#introduction)
2. [Play: {Play Name}](#play-{kebab-case-play-name})
3. [Play: {Play Name}](#play-{kebab-case-play-name})
<!-- Add one entry per play; anchor = "play-" + kebab-case of play name -->

---

## Introduction

### What is a Playbook?

A playbook is a collection of proven practices that empowers our team to act with
confidence in nearly any situation they encounter. By providing a clear framework
for action, it fosters autonomy and a shared purpose, ensuring we achieve consistent
results every time.

To make a playbook truly effective, every individual "play" needs to be structured
around four essential elements that turn instructions into an actionable strategy.

- **Triggers** — defining exactly when to act, grounding the play in a sense of
  awareness so you know when the situation demands a response.
- **Actions** — outlining what specifically needs to be done, allowing clear
  execution in the heat of the moment.
- **Benefits** — establishing how to know when the task is finished, ensuring the
  play reaches a definitive state of completion.
- **Why the play matters** — giving the team the purpose and judgment needed to
  adapt if things don't go exactly as planned.

### Summary

{Dynamic — 2–4 sentences. State what domain or problem this playbook addresses,
what the plays cover collectively, and who it is written for.}

---

## Play: {Play Name}

### Why it matters

{One paragraph. State the problem this play addresses and why ignoring it has
consequences.}

### How it works

{Describe the mechanics — what you do, in what order, with what inputs and outputs.
Use a numbered list if sequence matters.}

### Benefits

- {Outcome or advantage this play delivers}

### Trade-offs

- {Cost, constraint, or limitation accepted when using this play}

### When to use it

- {Condition or context where this play is the right choice}

### When not to use it

- {Condition or context where this play is the wrong choice or actively harmful}

---

<!-- Repeat the Play block for each additional play -->
<!-- Anchor convention: id = "play-" + kebab-case of play name
     Example: "Play: Handle Late-Arriving Data" → #play-handle-late-arriving-data -->
```

---

## Usage Notes

- **ADR:** One ADR per decision. Never combine two decisions into one ADR. Every ADR must reference its upstream Phase 1 requirement.
- **Requirements Brief:** Must be signed before Phase 3 begins. Budget envelope may be TBD at draft stage but must be resolved before Phase 6.
- **Runbook:** Steps must be operator-executable as written — no assumed context. Test each step before marking the runbook live.
- **Version rule (all types):** No version = cannot serve as alignment evidence. Assign v1.0 at first draft; increment on any substantive change.
- **Playbook:** Table of Contents is dynamic — update after all plays are finalized. Anchor format: `#play-{kebab-case-play-name}`. Introduction § *What is a Playbook?* is static boilerplate — do not rewrite per use case. Summary is dynamic — rewrite to describe this playbook's domain, plays, and audience. Order plays from most foundational to most advanced. Each play must be self-contained — readable without prior plays.
- **Corporate Document Chrome:** Use for any `.docx` requiring versioned cover, revision history, and remaining-issues tracking. Pair with one body template inserted at the `<!-- BODY -->` slot. Chrome reserves sections 1–3 (TOC, Revision History, Remaining Issues) and section 5 (Appendix); body template owns section 4. TOC section is title + page break only; populate the TOC in Word after rendering.
- **Architecture Requirements:** Body schema for system- and container-level architecture requirements. Always composes with Corporate Document Chrome. Sub-sections are fixed: Functional / Governance & Access / Observability / NFR. QA file `qa-architecture-requirements.md` activates automatically via SKILL.md Step 8.
