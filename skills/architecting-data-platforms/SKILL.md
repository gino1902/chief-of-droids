---
name: architecting-data-platforms
description: >
  Senior-level data platform architecture guidance covering Databricks,
  Azure, governance, and cost. Applies proactively for any data platform
  design, architecture trade-off, governance, cost, or Databricks/Azure
  configuration task. Composes with: reviewing-tech-claims, editing-docs.
---
<!-- version: 1.9 | author: chief-of-droids workspace | last_updated: 2026-06-03 -->

# Architecting Data Platforms Skill

Senior-level guidance on data platform architecture, Databricks, and Azure cloud
storage. Covers design decisions, trade-off frameworks, governance, cost modeling,
and anti-patterns.

**Principle:** This skill contains stable judgment patterns and workflows.
Version-sensitive technical facts (API signatures, retention thresholds, feature
availability by runtime) must be fetched from official sources — not read from this
file or memory.

---

## Mandatory Read

Use filesystem tool to read this file before producing **any** output:
- `references/qa-and-antipatterns.md` — anti-patterns radar and QA checklist; applies to all output types
  — if unreadable, flag: `⚠️ qa-and-antipatterns.md unreadable — apply default anti-pattern checks from memory`

---

## Domain Reference Files

Read explicitly via filesystem tool when advising in that domain. Files are not
loaded automatically; read each file when the relevant domain is triggered.
If a domain reference file is unreadable, flag it and proceed with caution:
`⚠️ [filename] unreadable — advice in this domain is from memory only; verify before use`

- `references/databricks-de.md` — read when advising on compute, Delta Lake, Unity Catalog, Auto Loader, DLT
- `references/databricks-ml.md` — read when advising on MLflow, Feature Store, Prophet, model drift
- `references/azure-storage.md` — read when advising on ADLS Gen2, access tiers, identity, mount points
- `references/governance.md` — read when advising on maturity levels, cost governance, ROI framework, data contracts
- `references/architecture-frameworks.md` — read when advising on paradigm selection, build vs buy, or medallion layer design
- `references/assessment-workflow.md` — read when running an Assessment Workflow (where are we?)
- `references/design-workflow.md` — read when running a gate check or Design Workflow from scratch

---

## Official Sources

Fetch these before any other source. Never cite community blogs, Medium, or GitHub
READMEs as ground truth.

| Topic | Official Source |
| :--- | :--- |
| Databricks platform | `docs.databricks.com` |
| Databricks release notes | `docs.databricks.com/release-notes` |
| Delta Lake | `docs.delta.io` |
| MLflow | `mlflow.org/docs/latest` |
| Azure Storage / ADLS Gen2 | `learn.microsoft.com/azure/storage` |
| Azure RBAC | `learn.microsoft.com/azure/role-based-access-control` |
| Azure Managed Identity | `learn.microsoft.com/azure/active-directory/managed-identities-azure-resources` |
| Prophet | `facebook.github.io/prophet/docs` |

---

## Verification Rules

Before producing any output containing version-sensitive claims, load the
`reviewing-tech-claims` skill and apply its rules — do not read
`reviewing-tech-claims/SKILL.md` directly. Invoke it as a composed skill.
`reviewing-tech-claims` is the single source of truth for verification procedure.

---

## Composes With

| Skill | When |
| :--- | :--- |
| `reviewing-tech-claims` | Any output containing version-sensitive claims (Databricks, Azure, MLflow, Prophet) — load as composed skill |
| `editing-docs` | When output is a structured document or .md file |
| `analyzing-business-cases` | When use case framing and platform architecture are both in scope |

---

## Trigger Examples

- "Design a medallion architecture for our HR data"
- "Should we use DLT or plain Workflows?"
- "Help me build the cost model for the forecasting POC"
- "Where are we in the platform project?"
- "Review our ADRs"

---

## Assessment Workflow — Where Are We?

Trigger when the user describes a platform project in progress, asks "where should
we focus", "what's missing", "are we on track", or shares existing artefacts.

Use filesystem tool to read `references/assessment-workflow.md` — full 5-step procedure:
Intake → Phase Diagnosis → Gap Analysis → Alignment Check → Prioritised Recommendations.

---

## Design Workflow — From Scratch to Final Review

Run the gate check automatically when a phase completion signal is detected.
Never wait to be asked.

Use filesystem tool to read `references/design-workflow.md` — gate check procedure and phase table:
- Gate check procedure and phase recognition patterns
- Full phase table (Phases 1–9) with deliverables and gate conditions
- Phase content detail
- Assessment output instructions
