# Assessment Workflow — Where Are We?

Trigger when the user describes a platform project in progress, asks "where should
we focus", "what's missing", "are we on track", or shares existing artefacts.

---

## Step 1 — Intake

Group into a single prompt. Do not proceed until all answers are collected.

```
1. What is the platform for? (domain, business objective, key consumers)
2. What phase do you think you're in? (or: describe what has been done so far)
3. What artefacts exist? (documents, diagrams, models, code repos)
4. What is the timeline pressure? (discovery, POC, production target date)
5. Who is involved? (team size, roles, stakeholders)
6. What is the blocker or question that triggered this conversation?
```

---

## Step 2 — Phase Diagnosis

Map answers to Design Workflow phases. Assign a status per phase:

| Status | Meaning |
| :--- | :--- |
| ✅ Complete | Deliverable exists and gate condition met |
| 🟡 Partial | Work started but deliverable incomplete or gate not met |
| 🔴 Missing | No evidence of phase work |
| ⏭ Not yet applicable | Correctly sequenced later phase not yet started |

Output a **Phase Status Table:**

```
| Phase | Status | Evidence | Version | Gap |
| :--- | :--- | :--- | :--- | :--- |
| 1 — Requirements | 🟡 Partial | Verbal brief, no sign-off | none | No written Requirements Brief |
| 2 — Current State | 🔴 Missing | None | — | Assessment not started |
| ...
```

**Version column rules:**
- Record the version identifier as stated by the team (e.g. v1.2, "draft", "2024-11").
- If no version exists: enter `none` — treat the document as 🟡 Partial regardless of content.
- If version exists but predates a known upstream change: flag as `stale` and note which upstream phase changed.

---

## Confidence Rule — When to Raise an Alert

Apply before Step 3 and Step 3b. Alert level depends on evidence quality, not assumption.

**Raise ⚠️ MISALIGNMENT or flag BLOCKING only when confidence is high:**
- A later-phase artefact is explicitly confirmed as existing AND an earlier gate condition is explicitly absent
- Two artefacts are both confirmed as existing AND their described content directly contradicts each other
- A document version predates a confirmed upstream change (version drift = misalignment until the team demonstrates the document was reviewed post-change)

**Mark ❓ (cannot assess) when:**
- Artefact existence is implied but not confirmed
- Gate condition is unclear from intake answers
- A contradiction could be a wording ambiguity rather than a real conflict
- Version information is absent — document maturity cannot be assessed

**Document maturity affects confidence:**
- A document with no version, no author, no date, and no sign-off is weak evidence of a completed gate — treat as 🟡 Partial, not ✅ Complete
- A document that cannot be traced to its upstream inputs (e.g. an ADR with no requirement reference) reduces alignment confidence for all downstream checks that depend on it
- A document that has not been updated since an upstream phase changed is a misalignment until the team demonstrates it was reviewed post-change — the burden of proof is on the team, not the assessor

**Senior rule:** ❓ is not a weak finding — it becomes a HIGH action in Step 4, requiring the missing artefact or version evidence to be produced before the check can be run. Never suppress a ❓ by assuming alignment.

---

## Step 3 — Gap Analysis

For each 🟡 or 🔴 phase: state the missing element, the risk of proceeding without
it, and flag any sequencing violation (downstream phase started before upstream gate
was met).

**Senior rule:** A sequencing violation is a risk, not just a gap. Name it as such.

---

## Step 3b — Alignment Check

Detect cross-phase inconsistencies — not just whether deliverables exist, but whether
they are consistent with each other.

For each pair: ✅ Aligned / ⚠️ Misaligned / ❓ Cannot assess.

| Check | What to verify |
| :--- | :--- |
| Requirements → Architecture | Every ADR traces to a stated requirement — no technology preference decisions |
| Requirements → Cost Model | Budget envelope matches TCO estimate; regulatory constraints drive cost assumptions |
| Requirements → Security | Regulatory constraints reflected in security design; data residency maps to regions |
| Architecture → Data Model | Paradigm choice reflected in layer definitions; DLT in ADR matches pipeline design |
| Architecture → Security | UC decision in ADR reflected in privilege model; no mount points if UC selected |
| Architecture → Cost Model | Compute types in ADR match types costed in Phase 6; no phantom compute |
| Data Model → Security | Classification register covers all tables; Gold confidential entities have UC row/column security |
| Data Model → Implementation Roadmap | Bronze/Silver/Gold map to Phases 1/2/3; ML scope matches Phase 4 presence/absence |
| Cost Model → Implementation Roadmap | Phase sequence matches cost phasing; no uncosted phase in roadmap |
| Security → Implementation Roadmap | Phase 0 includes UC setup, External Locations, IAM — not just storage provisioning |
| Operations Runbook → Architecture | Monitoring matches pipeline pattern chosen; model monitoring present if ML in scope |
| Final Review → All phases | Traceability matrix covers every Phase 1 requirement; no orphaned requirement |
| Document consistency (all phases) | For any two deliverables that reference each other: verify version alignment. If Phase 6 references "Architecture v1" but ADRs are now at v3, the cost model is stale regardless of content alignment. A version gap between referencing and referenced document is ⚠️ Misaligned until the team confirms the referencing document was reviewed post-change. |

**Misalignment output:**
```
⚠️ MISALIGNMENT — <Phase A> vs <Phase B>
Found in:   <deliverable or decision>
Conflict:   <what Phase A says> vs <what Phase B says>
Risk:       <consequence if not resolved>
Suggestion: <what needs to change and in which deliverable>
```

**Senior rules:**
- Security↔Requirements and Architecture↔Cost misalignments are BLOCKING by default
- ❓ findings become HIGH actions — name the missing artefact explicitly

---

## Step 4 — Prioritised Recommendations

```
1. [BLOCKING] <action> — required before <downstream phase> can proceed
   Why: <one-line risk>
   Deliverable: <what to produce>
   Owner: <role>

2. [HIGH] <action> ...
3. [MEDIUM] <action> ...
```

Three priority levels only: BLOCKING / HIGH / MEDIUM. Maximum 5 actions per assessment.

---

## Step 5 — Offer to Help

Offer one of:
- Draft a missing deliverable (Requirements Brief, ADR, Data Contract template, etc.)
- Deep-dive a specific phase
- Review an existing artefact against the phase checklist
- Run a cost model or ROI framework

Wait for the user to choose.
