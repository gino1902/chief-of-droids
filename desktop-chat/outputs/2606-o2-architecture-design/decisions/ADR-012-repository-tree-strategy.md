# ADR-012 — Repository tree strategy: the tree's shape follows the work, not the data (Option A)

| Field | Value |
|:------|:------|
| Date | 2026-08-07 |
| Status | Draft |
| Task | TBD |
| Decision-makers | Gino, DE lead |
| Consulted | DE team |
| Informed | Wider data team |

---

## Context

The O2 platform repository is about to be created on GitLab, and nothing decides what shape its
tree takes. ADR-001 previously asserted one bundle per producer, per subject area and per use
case, but those were consequences it never argued, and they were removed on 2026-08-06 for that
reason. Since then the question has been unowned.

What forces it now is not only the repository creation. An IT transformation programme is under
way, and the ground moves in two speeds: **producers and consumers will change over the coming
months, while the entities they supply will not.** A tree whose shape encodes the fast-moving half
churns structurally every time a supplier is replaced, and that is precisely the year ahead.

The failure mode this decision guards against is a repository whose structure has to be rewritten
by events that are only data changes.

Bounding: this record decides what governs the tree's shape. It does not decide the repository
strategy itself, which is ADR-003, nor the deployment tooling, which is ADR-002. The number of
bundles and directories is an output of the rule decided here, not part of the decision.

---

## Options evaluated

**Option A — The tree's shape follows the work**
Structure encodes how the organisation is arranged: layers, and any boundary that has its own
release gate. Facts about the data, producers, routes and vehicles, stay in configuration. A
change in the world becomes a diff in a file rather than a diff in the tree.

**Option B — The tree's shape follows the data**
Structure encodes producers, subject areas and use cases directly, one directory and one bundle
each. This is what the removed ADR-001 consequences assumed and what the `artefacts/` skeleton was
built for. Every supply-path change is a structural change.

**Option C — The tree is fixed and hand-maintained**
A layout agreed once, edited by hand as needs arise, held by written convention and code review.
No rule, no projection, no derivation.

**Options not pursued**
- One bundle for the whole platform. It contradicts ADR-005, which requires a transformation
  failure not to block new data landing in bronze, and Databricks recommends small focused bundles
  over a single large one.

---

## Decision

**Option A chosen. The repository tree is a projection of how the work is organised, not of the
data it processes. A concept becomes structure only if it changes when the organisation changes.
A concept that changes when the data changes stays configuration. A directory becomes its own
bundle only when it needs its own blast radius, which today means its own release gate.**

Stated as two tests a developer can apply without reading this record:

**A folder exists because of how we work. A row exists because of what we work on.** If it changed
tomorrow, would anyone's job change? If not, it is data, and it belongs in a file.

**A folder is for finding things. A bundle is for blast radius.** Would you want to roll this back
without rolling that back? If not, same bundle. Folders are cheap; a bundle costs a deploy path, a
rollback path and a copy of every target and permissions block.

The corollary, which is the whole strategy in one line: **a change in the world should be a diff in
a file, not a diff in the tree.**

### What this yields today

An output of the rule, recorded so the rule can be checked against something, and expected to move
as the configuration moves:

| Change | What moves |
|:-------|:-----------|
| New producer, or one replaced | A row. Nothing in the tree |
| A vehicle splits, merges or is renamed | A row. Nothing in the tree |
| The route changes for everything, as in the ADR-008 migration | Configuration. Nothing in the tree |
| A new subject area gets live data | A directory inside silver |
| A subject area gains an owner who can block its release | That directory graduates to its own bundle |
| A new layer of work exists | A new bundle |

On the 2026-08-07 configuration that is two bundles, ingestion and silver, with subject areas as
directories inside silver, and no gold until a use case ships. Nineteen active feeds across two
producers produce no directories at all.

### Rationale

| Criterion | A, follows work | B, follows data | C, hand-maintained |
|:----------|:----------------|:----------------|:-------------------|
| Survives supply-path churn without a structural change | Yes | No, every supplier change is structural | No, every change is a manual edit |
| Same substrate yields the same tree | Yes, rule-derived | Yes, rule-derived | No, depends who edits it |
| Blast radius matches a gate someone actually holds | Yes | No, boundaries nobody can exercise | Accidental |
| Repetition carried | Low | High, a copy of every target and permissions block per bundle | Variable |
| Satisfies "everything one team owns in one bundle" | Yes | No | Unaddressed |

B and C both fail the first criterion, which is the one the forcing function makes decisive. B
additionally creates boundaries nobody can exercise, paying deploy and rollback cost for gates that
do not exist. C cannot give the same tree twice, which was the original requirement.

Basis, and the parts have different standing. **No authority mandates this rule as stated**; it is
a synthesis. Its components are sourced:

- The split and merge criteria are Databricks' published guidance, in *Developer best practices*
  under "Create small bundles": split for different products or domains, different ownership or
  permission boundaries, clearly different lifecycles, or a need for independent promotion or
  rollback; and "put everything that a single team owns into one bundle".
- That producers must not be structure follows from ADR-011, which records the producing system as
  a mapping rather than as the contract.
- That system and organisation must be decomposed together is Fowler on Conway's law. That
  technical modularity without matching ownership is still monolithic is Foster. That one team
  should hold all data products until cognitive load forces a split is Prakash.
- That fine-grained decomposition carries real cost, and that its federation preconditions must be
  met first, is Strengholt. O2 meets none of them: canonicalisation is deferred with no owner and
  no owner gates a release.

---

## Validation

Compliance is mechanically checkable, which is the point of stating the rule this way.

- No producer, source, route or filename appears as a directory name anywhere in the tree.
  Greppable, and it is the rule's sharpest edge.
- The bundle count equals the number of layers with live work. Any other number means a directory
  became a bundle without a gate.
- A feed added or retired produces a diff in the feed configuration and none in the tree. Checkable
  on the merge request.
- Conformance cases 1, 6 and 8 in `../adr-conformance/cases.md` currently report a gap on this
  question. With this record they should report Determined. If they do not, this record is
  underspecified and the wording is at fault.

Conditions that reopen it:

- A subject area gains an owner who can block its release. That directory graduates to a bundle and
  the migration cost below is paid.
- One team can no longer hold all layers, which is Prakash's cognitive-load trigger.
- The ADR-008 migration lands and each producer gets its own landing prefix. The rule should still
  say producer is data, but that is the moment to re-test rather than assume.

---

## Consequences

- A supplier change, a file split, a renamed vehicle and the whole ADR-008 route migration all
  become configuration edits. The tree does not move during the year it would otherwise churn most.
- Fewer bundles means one copy of the targets, the permissions block and the variables, rather than
  one per producer and subject area.
- **One subject area cannot be rolled back without the others.** One silver bundle, one deploy. A
  bad hr change reverts finance too. Free today because nobody can exercise that boundary, real the
  day someone can.
- **Splitting later is a migration, not a move.** When a subject area gains its own gate, its
  resources move between bundles and one bundle wants to remove what the other wants to create.
  Keeping the bundle shape blueprint-consistent from the start makes the move mechanical, which is
  Prakash's mitigation, but it is not free.
- **The tree tells you less than it used to.** Reading the repository no longer reveals who supplies
  the data, because producers are rows rather than folders. Stability under churn is bought with
  at-a-glance legibility, and anyone asking where data comes from reads the configuration.
- ADR-001 is left as the record of what the layers mean, with no claim over how many bundles they
  become. That separation is what this record exists to hold.

---

## Sources

| Source | Bears on |
|:-------|:---------|
| [Developer best practices on Databricks](https://learn.microsoft.com/en-us/azure/databricks/developers/best-practices), "Create small bundles" and "Plan for rollbacks and hotfixes" | The four split criteria, the merge rule, and targeted rollback as the sizing test |
| [Sharing bundles and bundle files](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing), "Repository structure" | One repository with a shared folder as the vendor recommendation |
| [Manage data quality with pipeline expectations](https://learn.microsoft.com/en-us/azure/databricks/ldp/expectations) | A failed flow does not fail parallel flows in a triggered pipeline, which removes the resilience objection to one ingestion bundle |
| [Unity Catalog best practices](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/best-practices) | The schema is the permission boundary and is independent of the bundle, so grants do not force a split |
| [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html), Dehghani | Decomposition follows organisational seams; a data product is the smallest **independently deployable** unit |
| [Linking Modular Architecture to Development Teams](https://martinfowler.com/articles/linking-modular-arch.html), Foster | Technical modularity without matching ownership is still monolithic |
| [Conway's Law](https://martinfowler.com/bliki/ConwaysLaw.html), Fowler | System and organisation must be decomposed together, not one ahead of the other |
| [Designing data products](https://martinfowler.com/articles/designing-data-products.html), Prakash | Start with one team, split on cognitive load, and blueprint consistency reduces the later split cost |
| [Data Mesh: Topologies and domain granularity](https://towardsdatascience.com/data-mesh-topologies-and-domain-granularity-65290a4ebb90/), Strengholt | Fine-grained decomposition is costly, and its federation preconditions must be met first |
| `.claude/skills/bootstrapping-project/references/trees.md`, code-data | Every directory justified now rather than speculatively; `resources/` sprawl as a signal of an avoided topology decision |
| ADR-001, ADR-003, ADR-005, ADR-011 | Layer semantics, one repository, ingestion split from transformation, and the producing system as a mapping |

All external pages fetched and verified 2026-08-06 or 2026-08-07, each carrying a last-updated date
within twelve months where one is published.

Version history is git. This record carries no version field.
