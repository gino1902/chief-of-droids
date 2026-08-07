# ADR conformance cases

Method, verdicts and how to run: [README](README.md). Substrate: [`../decisions/`](../decisions/).

> Expected designs are deliberately **not filled in**. Authoring a case and deriving its answer
> are separate activities, and doing both in one pass lets the author write the case around the
> answer. Derivation is pass one, recorded per run.

---

## Vocabulary

A **supply path** has three components, and a change usually hits one without the others. The feed
configuration already carries all three.

| Component | What it is | Columns in `o2-data-sources` |
|:----------|:-----------|:-----------------------------|
| Producer | The system of origin, which owns the data | `producer` |
| Route | How it travels: relay, location, protocol | `source`, `source path`, `access-protocol` |
| Vehicle | The concrete carrier: file, pattern, format, cadence | `filename`, `cadence` |

When two vehicles feed one entity, they do so in one of two ways, and the distinction changes both
the silver logic and the failure mode:

- **Union.** Each carries some of the **rows**. Losing one means a silently short population.
- **Join.** Each carries some of the **attributes**. Losing one means a broken schema.

Every case declares which. Cardinality is fixed per case, never "one or more".

## Design elements a derivation must return

Each with its citation. An element with no citation is a Gap.

`bronze` · `feed-to-entity mapping` · `silver` · `entity contract` · `which bundle`

---

## Case 0 — control, steady state

**Given.** Entity A. One producer, one route, one vehicle. No multiplicity, so union and join do
not apply.

**Change event.** None.

**Why it exists.** Establishes what a predictable design looks like before anything is perturbed.
A record set that cannot answer this cleanly has a problem the perturbed cases will only obscure.

**Exercises.** ADR-001, ADR-005, ADR-007, ADR-009, ADR-011.

**Expected design.** _To derive._ **Verdict.** _Not run._

---

## Case 1 — one entity, two vehicles, one producer

**Given.** Entity A. One producer, one route, two vehicles. Declare per subcase whether union or
join.

| Subcase | Change event | Component |
|:--------|:-------------|:----------|
| 1.1 | The producer is replaced. Exactly one new producer supplies entity A, over a new route, with one vehicle | Producer, route and vehicle together |
| 1.2 | The two vehicles are consolidated into one. Producer and route unchanged | Vehicle only |
| 1.3 | A second producer is added alongside the first. One new vehicle, one new route. The original two vehicles remain | Producer added |

**Run each subcase twice**, once declared union and once declared join. They are different tests:
under union, 1.2 changes nothing semantically; under join, 1.2 removes a join the silver logic
performs.

**Live instance.** `hr-administration` has seven vehicles for five entities, so at least one entity
here is multi-vehicle. Which, and whether union or join, is unknown until the feed-to-entity
mapping exists.

**Exercises.** ADR-001, ADR-009, ADR-011, ADR-012.

**Run 2026-08-07**, substrate `99ae848`, two independent derivations, high agreement.
**Verdict: Conflict**, since resolved. ADR-012 gave two bundles while ADR-003, ADR-005 and
ADR-011 still said one per producer. Reconciled in `7fce688`, and a re-derivation of the bundle
field returns no conflict. Bronze, silver and contract agreed across both runs. Mapping returned
Gap. Three further gaps found, recorded below.

---

## Case 2 — one entity, two vehicles, two producers

**Given.** Entity A. Producer I with one vehicle, producer II with one vehicle. Declare union or
join per subcase.

| Subcase | Change event |
|:--------|:-------------|
| 2.1 | Producer I is replaced by exactly one new producer with one vehicle. Producer II is unchanged and remains a source |
| 2.2 | Both producers are replaced by exactly one new producer supplying entity A with one vehicle |
| 2.3 | A third producer is added with one vehicle. Producers I and II are unchanged |

**Why it differs from case 1.** Two producers means two upstream owners, two change cadences and
two negotiation counterparties. Case 1 has one of each.

**Exercises.** ADR-001, ADR-010 (the boundary and who is a party), ADR-011, and the ownership
model, which is unwritten.

**Expected design.** _To derive._ **Verdict.** _Not run._

---

## Case 3 — one vehicle, two entities

**Given.** Entities A and B, both carried by a single vehicle from one producer over one route.

| Subcase | Change event |
|:--------|:-------------|
| 3.1 | The producer is replaced. Exactly one new producer supplies both A and B, one vehicle, new route |
| 3.2 | Entity A is **partly** re-sourced: a second producer supplies some of A's rows. B is unchanged and still arrives on the original vehicle |
| 3.3 | Entity A is **wholly** re-sourced from a new producer. B is unchanged and still arrives on the original vehicle |

**Note on 3.2 and 3.3.** These split a vehicle's entities across producers, so the vehicle stops
being a clean unit for either. 3.2 additionally makes A a union across two producers.

**Live instance.** `project-resources` has two vehicles and three entities, and `finance-fa&c` has
two vehicles and three entities. So either a vehicle carries several entities, or an entity has no
supply path and is not admissible under ADR-011. Nobody can currently tell which, and those are
very different situations.

**Exercises.** ADR-001, ADR-011 admission test, the feed-to-entity mapping, which does not exist.

**Expected design.** _To derive._ **Verdict.** _Not run._

---

## Case 4 — a supply path is lost with no replacement

**Given.** Entity A. One producer, one route, one vehicle.

**Change event.** The vehicle stops arriving. Nothing replaces it, and no date is given for one.

**Why it exists.** ADR-011 admits an entity "when a supply path exists". Nothing says what happens
when the path goes away. Does the entity leave the baseline, stay with a broken contract, or become
a declared gap?

**Live already.** Two feeds sit at `status: inactive` in the configuration while their folders
still receive a file every day, so "inactive" does not currently mean "not landing" and the term is
undefined.

**Exercises.** ADR-011, ADR-001, and the meaning of `status` in the feed configuration.

**Expected design.** _To derive._ **Verdict.** _Not run._

---

## Case 5 — the payload changes, the supply path does not

**Given.** Entity A. One producer, one route, one vehicle, all unchanged.

**Change event.** The content changes. A field is renamed, a field is added, or a type changes,
because the specifying team revised the requirement. O2 is not a party to that decision and is not
notified.

**Why it exists.** This is the most likely event of all and no case covered it. ADR-011's
translation mapping exists precisely for semantic incompatibility, and bronze's VARIANT landing
means the change surfaces at silver rather than at ingestion.

**Exercises.** ADR-011 translation mapping, ADR-007 expectations, ADR-009 VARIANT landing,
ADR-010 on who is a party to the payload specification.

**Expected design.** _To derive._ **Verdict.** _Not run._

---

## Case 6 — one vehicle crosses two subdomains

**Given.** Entities A and B on one vehicle, as in case 3, but A and B belong to **different
subdomains with different owners**.

**Change event.** Owner of A requires a change to how A is conformed. Owner of B does not, and
does not want their tables redeployed.

**Why it exists.** Every other case tests the ingestion model. This one tests the ownership model,
which is the harder half and is unwritten. It is also the case that decides whether an owner is a
real boundary or an accountability, which is the question the bundle count turns on.

**Exercises.** The unwritten ownership record, ADR-006 permissions, ADR-012.

**Run 2026-08-07**, substrate `99ae848`, two independent derivations, high agreement.
**Verdict: Conflict**, since resolved for the bundle question only. Both runs also noted the
outcome ADR-012 predicts: the silver bundle redeploys and the second owner's tables go with it,
which is that record's stated consequence, and that owner's refusal is exactly the trigger that
graduates their directory to its own bundle. **Not re-run after reconciliation.**

---

## Case 7 — the definition changes, nothing else does

**Given.** Entity A, steady state as in case 0.

**Change event.** The business rules that the entity means something different. Contractors now
count as Employees. No producer, route, vehicle or payload changes.

**Why it exists.** It separates the ingestion contract from the semantic one. Bronze does not
change, ADR-011's contract does not change, and silver does. If the record set cannot express that,
it has conflated two contracts.

**Exercises.** ADR-001 conformed definitions, the unwritten ownership record, and whether the
entity contract in ADR-011 is semantic or supply-shaped.

**Expected design.** _To derive._ **Verdict.** _Not run._

---

## Case 8 — the route changes, alone and for everything

**Given.** Every active entity, unchanged producers, unchanged vehicles.

**Change event.** The route changes for all of them at once: the same producers deliver the same
files by a different mechanism to a different location.

**Why it exists.** No case covered a route-only change, and this is the largest known change
coming: the ADR-009 to ADR-008 migration. Decomposing the supply path into producer, route and
vehicle is what made its absence visible.

It is also the case where the bundle-count answer may legitimately differ before and after,
since the current route has one connection to one site while the planned one lands per producer.

**Exercises.** ADR-008, ADR-009, ADR-011, ADR-012.

**Run 2026-08-07**, substrate `99ae848`, two independent derivations, high agreement.
**Verdict: Conflict**, since resolved for the bundle question only. Both runs agreed the route
change is a path-swap that touches only the read-path block, and that zero bundles change under
either count. One run independently surfaced the ADR-010 against ADR-009 file-removal question,
already logged as amendment A3. **Not re-run after reconciliation.**

---

## Coverage

| Record | Cases |
|:-------|:------|
| ADR-001 | 0, 1, 2, 3, 4, 7 |
| ADR-002 | none yet |
| ADR-003 | none yet |
| ADR-004 | **none, and expected to stay none.** Serverless compute is not perturbed by any supply-path change |
| ADR-005 | 0 |
| ADR-006 | 6 |
| ADR-007 | 0, 5 |
| ADR-008 | 8 |
| ADR-009 | 0, 1, 5, 8 |
| ADR-010 | 2, 5 |
| ADR-011 | 0, 1, 2, 3, 4, 5, 8 |
| Ownership record, unwritten | 2, 6, 7 |
| Bundle count, unowned | 1, 6, 8 |

ADR-002 and ADR-003 have no case because they decide tooling and repository shape, which no
supply-path change perturbs. That is a real coverage hole for this suite rather than a defect in
those records: a different instrument would be needed to test them.

## Findings from the first run

2026-08-07, substrate `99ae848`, cases 1, 6 and 8, two independent derivations each. Transcripts
in `runs/`, which is git-ignored, so these are the surviving record.

**The run worked.** It found a contradiction its own author could not have found by re-reading,
because a fresh process has none of the author's intent in context. That is the argument for
running derivations in independent processes rather than in the session that wrote the records.

**Agreement was high and the verdict was still Conflict.** Worth separating: high agreement means
the records are unambiguous, not that they are right. They were unambiguous and contradictory.

### G1 — Silver has no way to bind its inputs

ADR-012 forbids a producer name appearing anywhere in the tree. No record says how a silver
pipeline then binds its bronze inputs. The rule has a prohibition and no mechanism.

This is a gap in ADR-012 itself and the sharpest of the four. Remedy: either ADR-012 states the
binding mechanism, or a convention does and ADR-012 points at it.

### G2 — A retired producer's bronze data has no disposition

When a producer is replaced, nothing states whether its existing bronze tables are retained,
archived or dropped. Exercised by case 1.1 and by case 4.

Remedy: a consequence in ADR-011 or ADR-001, since it is a lifecycle question about raw data.

### G3 — A third route is uncovered

ADR-008 covers ADLS Gen2 and ADR-009 covers SharePoint. A supply path arriving by neither has no
record. Both runs on case 1 flagged it, since the case posits a new route without naming it.

Remedy: state in ADR-011 whether a new route needs its own record, or whether the entity contract
is route-agnostic by construction and any route is admissible once it lands in bronze.

### G4 — The feed-to-entity mapping does not exist

Flagged by every run. ADR-011 admits an entity "when a supply path exists" and nothing records
which vehicles carry which entities, so that admission test cannot be evaluated. Two subdomains
already have more entities than vehicles.

Remedy: the artefact itself. It is data rather than a decision.

## Known blockers on grading

Cases 1 and 3 cannot be graded against real data until G4 is closed.

Cases 6 and 8 were not re-run after the reconciliation in `7fce688`. Only the bundle field of
case 1 was. Re-run all three before treating any verdict as current.

Cases 0, 2, 3, 4, 5 and 7 have never been run.
