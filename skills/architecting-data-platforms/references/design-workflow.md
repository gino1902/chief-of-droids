# Design Workflow — From Scratch to Final Review

---

## Gate Check Rule — Automatic Trigger

Do not wait to be asked. When a phase completion signal is detected, immediately
run the gate check for that phase before the next phase begins.

**Gate check procedure (run in order):**
1. Gate condition check — deliverable exists, is versioned, sign-off obtained, inputs traceable
2. Document maturity check — apply confidence rule; flag `none` version as 🟡 Partial
3. Relevant alignment checks — run all checks involving the completed phase deliverable
4. Surface any BLOCKING findings — do not proceed to next phase until resolved
5. Offer to write the assessment to `use-case-{id}/test/assessment-phase-{N}-{YYYY-MM-DD}.md`
   using `references/assessment-template.md` as the template

---

## Phase Recognition Patterns

Detect phase completion or next-phase start from any of these signal types:

| Signal type | Example phrases |
| :--- | :--- |
| Explicit completion | "phase 3 is done", "we finished requirements", "ADRs are approved" |
| Next phase start | "starting phase 4", "moving on to data modelling", "let's do the cost model" |
| Deliverable submission | user shares or describes a new deliverable (ADR, brief, model, runbook) |
| Gate question | "are we ready to move on?", "can we start X?", "is phase N complete?" |
| Status update | "we now have X signed off", "security design was approved yesterday" |

When signal is ambiguous — ask one targeted question to confirm before running the gate check.
Never run a gate check on an assumption.

---

## Phase Table

| Phase | Deliverable | Gate |
| :--- | :--- | :--- |
| 1 — Requirements | Requirements Brief | Signed by business + engineering sponsors |
| 2 — Current State | Current State Assessment | Maturity level agreed |
| 3 — Architecture Selection | Architecture Decision Records (ADRs) | Peer-reviewed and approved |
| 4 — Data Modelling | Data Model Document + Data Contracts | Gold schemas approved; contracts co-signed |
| 5 — Security | Security Design Document | CISO sign-off before any provisioning |
| 6 — Cost Modelling | 3-year TCO Model + ROI Summary | Finance approval |
| 7 — Implementation | Implementation Roadmap | Programme sponsor approval; Go/No-Go after Phase 1 |
| 8 — Observability | Operations Runbook | Live before first production pipeline |
| 9 — Final Review | Architecture Sign-Off Document | Residual risks logged with owners |

---

## Phase Content Detail

**Phase 1 — Requirements:** Capture business intent, data domains, consumers, volume,
latency, regulatory constraints, team maturity, budget envelope. One-pager signed by
both business and engineering sponsors before any architecture work begins.

**Phase 2 — Current State:** Inventory sources/pipelines/consumers, pain points, skill
gaps, baseline cost estimate. Assign Governance Maturity Level (see `references/governance.md`).

**Phase 3 — Architecture Selection:** Nine sequential decisions — paradigm, processing
model, storage layer, compute platform, governance layer, ingestion pattern,
transformation pattern, serving layer, ML platform. One ADR per decision.
Senior rule: every ADR must trace to a Phase 1 requirement.

**Phase 4 — Data Modelling:** Bronze ingestion contracts, Silver quality rules, Gold
entity models, data contracts at Silver→Gold boundary, schema evolution policy,
domain ownership matrix.

**Phase 5 — Security:** UC privilege matrix, External Location map, access method per
integration, secret management, network topology, data classification register.
Security model signed off before any infrastructure is provisioned.

**Phase 6 — Cost Modelling:** DBU consumption estimate, storage cost, egress cost,
engineering cost, 3-year TCO with ×2/×5 sensitivity. Compare against Phase 2 baseline.

**Phase 7 — Implementation:** Phase 0 (Foundation) is non-negotiable — do not ingest
data into an ungoverned environment, even for a POC. Phases: Foundation → Bronze →
Silver → Gold+Serving → ML → Operationalise.

**Phase 8 — Observability:** Pipeline monitoring, quality dashboards, cost alerts,
model monitoring, incident runbook, capacity review cadence. Monitoring live before
first production pipeline.

**Phase 9 — Final Review:** Traceability matrix (requirements → implemented components),
ADR compliance, cost actuals vs estimate, open items with owners.

---

## Assessment Output

When a gate check completes, produce a structured assessment and offer to write it
as a project artefact:

- **Template:** `references/assessment-template.md`
- **Output path:** `use-case-{id}/test/assessment-phase-{N}-{YYYY-MM-DD}.md`
- **Naming:** kebab-case, phase number zero-padded, ISO date — e.g. `assessment-phase-03-2026-03-10.md`
- **Never** write the assessment inside the skill repository — it is a project artefact
- **Always** propose the write path and receive explicit confirmation before writing
- The saved assessment doc becomes version evidence for future alignment checks —
  reference it by path when running document consistency checks in later phases
