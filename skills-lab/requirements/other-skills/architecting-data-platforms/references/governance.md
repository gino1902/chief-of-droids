# Governance & Cost Reference

Stable judgment patterns — these do not require fetch verification unless a specific
tool's feature availability or pricing is being cited.

---

## Data Governance Maturity Levels

| Level | Characteristics |
| :--- | :--- |
| 0 — Ad hoc | No catalog, no lineage, access by convention |
| 1 — Reactive | Catalog exists; access control manual; lineage partial |
| 2 — Managed | Unity Catalog enforced; lineage automated; quality monitored |
| 3 — Proactive | Data contracts enforced; SLAs measured; drift detected automatically |
| 4 — Self-service | Federated ownership; domain-published; governed mesh |

**Senior rule:** Recommend governance investments proportional to current maturity.
Jumping from Level 0 to Level 4 tooling without process change fails — the org
will revert to Level 0 behaviour within the new tooling.

**Application:** Always assign a maturity level during Phase 2 (Current State
Assessment) before proposing any governance tooling in Phase 3 or beyond.

---

## Cost Governance on Databricks / Azure

### Key Levers

- **Cluster auto-termination:** Enforce via cluster policy on all all-purpose clusters. Platform default is higher than most teams need — reduce to match actual usage patterns. Specific thresholds must be verified at `docs.databricks.com` as they may change.
- **Spot / preemptible instances:** Use for non-critical batch jobs; never for streaming or interactive workloads where interruption causes data loss or user impact.
- **DBU optimisation:** Right-size compute per workload type. Memory-bound jobs are commonly over-provisioned on worker count — profile before sizing.
- **Storage lifecycle policies:** Automate tier transitions via Azure Blob Lifecycle Management. Manual tier management at scale is error-prone and creates early deletion penalty exposure.
- **Unity Catalog cost attribution:** Tag catalogs and schemas to cost centers. Use Azure Cost Management + Databricks billing APIs for chargeback reporting.

### Cost Governance Process

A senior architect must define these at platform design time — not post-launch:

1. Budget alert thresholds in Azure Cost Management (workspace-level and subscription-level)
2. DBU budget per environment — dev/staging must have hard caps
3. Quarterly cluster right-sizing review cadence
4. Ownership of cost anomaly response (who is paged, what is the SLA to investigate)

---

## Platform ROI Framework

Use when presenting a data platform investment to finance or ExCom.

| Step | Content |
| :--- | :--- |
| 1 — Baseline cost | Current state: tooling licenses, engineering labor, incident cost, manual process cost |
| 2 — Capability value | Revenue uplift, decision speed improvement, risk reduction, compliance value |
| 3 — Platform cost | DBU licensing, storage, egress, engineering (build + ongoing ops) |
| 4 — Time to value | Phased delivery map; earliest business value delivery date (target: 0–90 days) |
| 5 — Exit / risk cost | Cost and consequence of not building — make the status quo cost explicit |

**Senior rule:** Never present a platform ROI without a phased delivery map. A
single-number 3-year ROI without delivery milestones will not survive ExCom scrutiny.

**Senior rule:** Exit/risk cost (Step 5) is the most persuasive element for risk-averse
sponsors — quantify it before leading with capability value.

---

## Data Contract Governance

Data contracts are a governance instrument, not just a schema agreement. They must
be owned, versioned, and enforced — not treated as documentation.

**Minimum contract elements:**

- Schema: column names, types, nullability, format
- Semantics: field definitions, business rules, grain
- SLA: freshness commitment, availability commitment, quality threshold
- Versioning policy: what constitutes a breaking change; deprecation notice period
- Signatories: named producer team lead and consumer team lead

**Enforcement pattern:**

- Breaking changes require a new contract version and co-sign before deployment
- SLA breaches trigger an incident — not a best-effort fix
- Contracts are stored in version control alongside the pipeline code that produces the data

**Anti-pattern:** Treating data contracts as one-time documentation produced during
Phase 4 and never revisited. Contracts must evolve with the data model.
