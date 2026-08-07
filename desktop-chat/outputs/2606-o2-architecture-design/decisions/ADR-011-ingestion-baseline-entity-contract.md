# ADR-011 - Ingestion baseline: contract on entities with the producing system as configuration (Option C)

| Field | Value |
|:------|:------|
| Date | 2026-08-06 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Product Architect (Gino) |
| Consulted | DE lead, IT transformation lead |
| Informed | IS lead, IT team, Data team |

---

## Context

O2 must decide what it treats as its ingestion baseline. The IT transformation programme is in
flight and will change producers and consumers over the coming months, while the entities
themselves stay stable. Building on a moving topology risks rework; waiting for the programme to
settle stalls the platform.

Three constraints bound it. The IS data architecture is inconsistent, and APP is a twenty-year-old
in-house system spanning most of the estate. O2 cannot change any of it, since applications,
producers and entities are inputs. And an entity enters the baseline only when a supply path to it
exists, which is forced rather than chosen: finance is the live instance, because Unit4 has no
outbound path. The failure mode this guards against is binding the platform to a topology that is
known to be moving, so that every producer change lands as rework in transformation logic.

---

## Options evaluated

**Option A - Adopt the current topology as the baseline**
Build on what exists today and absorb the churn as the programme moves producers.

**Option B - Wait for the transformation programme**
Let producers and consumers settle before committing to any ingestion design.

**Option C - Contract on entities, producing system as configuration**
The baseline names which entities O2 ingests; which system supplies each is a mapping that can
change without rework.

**Options not pursued**
- Fixing the IS architecture first: O2 cannot change it, so this is not O2's decision to take.
- Connecting O2 directly to each source system: ADR-010 sets the boundary as one-way inbound
  through the middleware.

---

## Decision

**Option C. The baseline is a set of entities, each admitted when a supply path exists, with the
producing system recorded as a mapping rather than as the contract. A translation mapping is
introduced where a producer's semantics are incompatible with O2's model; semantic incompatibility
is the primary test and lifespan is secondary, deciding only whether a mapping is permanent or
retired, not whether it exists. Mappings translate only. Conforming logic stays in silver.**

### Rationale

| Criterion | Option A | Option B | Option C |
|:----------|:---------|:---------|:---------|
| Time to first value | Fast | Deferred until the programme lands | Fast |
| Producer-change containment | None, a producer move is rework | Not applicable, nothing is built | Contained, a producer move is a mapping edit |
| Cost of the indirection | None | None | A mapping to maintain, validate and keep honest |

C matches A on time to first value and beats it on containment, which is the criterion the forcing
function makes decisive. It loses on the third driver, and that cost is accepted deliberately
rather than argued away: the indirection is real and an unmaintained mapping is worse than none.

Basis: the Anti-Corruption Layer pattern, sections "Context and problem" and "When to use this
pattern", which grounds the mechanism and supplies the discriminator, since it prescribes the layer
where "two or more subsystems have different semantics" and warns against it where there are no
significant semantic differences. ADR-001 supports the placement, because bronze is source-aligned
while silver produces the conformed enterprise view, so an entity contract above a per-producer
bronze is consistent with the layer model. ADR-010 principle 5, demand-driven change, supports
admitting entities as paths appear. No authority mandates treating lifespan as a secondary factor;
that part is judgement about this estate, and the reference discriminates on semantics alone.

---

## Validation

A producer change closes as a mapping edit with no change to silver entity definitions. If a
producer moves and the merge request touches silver logic, the decision did not hold for that case,
and this is the check that can prove it wrong rather than merely prove intent.

Supporting invariants: a producing system name appears only in the mapping and never in silver
transformation code, checkable by lint in CI; every entity in the baseline has a named producing
system and no entity is admitted without a supply path, checkable by a validator against the
landscape; and each producer carries its semantic-compatibility classification recorded rather than
implicit, since that judgement has no external test.

The decision reopens when a producer change forces a silver change, which is failure rather than
drift, or when the mapping stops being maintained. It re-baselines rather than reopens when the
transformation programme replaces a producer, and when any application gains an outbound path,
admitting its entities to the baseline. Unit4 is the current instance, with Determine and Neo
behind it since they reach O2 only through Unit4.

---

## Consequences

- A producer change becomes a mapping edit rather than rework, which is the point of the decision.
- Every semantically incompatible producer needs a mapping that is maintained, validated and kept
  honest. An unmaintained mapping is worse than none.
- Bronze stays source-aligned along the supply path, so a producer change is a mapping edit and
  a configuration edit, while silver's entity definitions hold. It does not create or retire a
  bundle: under ADR-012 a producer is configuration and never a directory. An earlier version of
  this line said a producer change means a new bronze bundle, which ADR-012 contradicts.
- Someone must classify each producer as semantically compatible or not, and that judgement has no
  external test. Getting it wrong on APP is the expensive direction.
- Finance cannot be ingested at all until an application gains an outbound path, so the supply-path
  constraint bites immediately rather than theoretically.
- The baseline will move while the transformation programme runs, so it carries a re-baseline
  trigger rather than a claim of stability.

---

## Sources

- Anti-Corruption Layer pattern, sections "Context and problem", "When to use this pattern",
  "Problems and considerations" - https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer
- ADR-001 medallion layer ownership, for bronze source-aligned and silver as the conformed
  enterprise view.
- ADR-010 middleware and O2 boundary, principle 5, demand-driven change.
- ADR-009 SharePoint to bronze ingestion, for the disposable-bridge precedent behind lifespan as a
  secondary factor.
- SQLI System, O2 Ingestion View, [2026-08-06-sqli-system-ingestion-view.md](../../2607-o2-requirements/2026-08-06-sqli-system-ingestion-view.md),
  which defines the baseline: 16 source applications, 31 entities on ingestion edges, three
  manual-entry paths. Cited as a locked C4 System Landscape rather than a design document, unlike
  the ADR-008 and ADR-009 companions, since it describes what exists rather than proposing how to
  build.

Version history is git. This record carries no version field.
