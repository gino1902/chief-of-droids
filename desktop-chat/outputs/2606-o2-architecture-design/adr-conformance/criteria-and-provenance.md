# Criteria register and provenance

Every criterion used to argue a decision in the 2026-08-06 and 2026-08-07 sessions, with where it
came from and how strongly it is sourced.

It exists because provenance was challenged mid-session and the answer mattered: a criterion
assembled by someone already holding a view is suspect unless the criterion itself predates the
argument. Recording the source is what lets a future reader check that rather than trust it.

**Provenance classes.** *Vendor* is Databricks documentation. *Practitioner* is a named author
publishing under their own name. *Community* is a forum, aggregator or search summary with no
single accountable author. *Internal* is our own conventions. *Derived* is reasoning done in
session with no external source, which is the class to distrust first.

---

## A. Bundle and boundary sizing

| Criterion | What it tests | Class | Source |
|:----------|:--------------|:------|:-------|
| Different products or domains | Whether the WHAT differs | Vendor | [Developer best practices](https://learn.microsoft.com/en-us/azure/databricks/developers/best-practices), "Create small bundles" |
| Different ownership or permission boundaries | Whether different people gate the release | Vendor | Same |
| Clearly different lifecycles | Whether they change on different triggers | Vendor | Same |
| Need for independent promotion or rollback | Whether reverting one must not revert the other | Vendor | Same, and "Plan for rollbacks and hotfixes" |
| Everything one team owns goes in one bundle | The merge rule, the only criterion arguing for fewer | Vendor | Same |
| Repetition carried | Near-duplicate resource files as a signal of an avoided topology decision | Internal | `.claude/skills/bootstrapping-project/references/trees.md`, code-data watch-outs |
| Every directory justified now, not speculatively | Whether a boundary serves anything that exists | Internal | Same, pass-3 rules |
| Cost if wrong | That splitting later is a state migration, not a move | **Derived** | No source. Reasoned from [Configuration reference](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/reference) on sync roots and bundle state. **Untested** |
| WHAT and HOW define the boundary | The organising lens over the others | Internal | The user's own principle, stated in session before the answer was known |

## B. Data product shape and ownership

| Criterion | What it tests | Class | Source |
|:----------|:--------------|:------|:-------|
| Smallest **independently deployable** unit | Whether a candidate boundary can actually deploy alone | Practitioner | [Data Mesh Principles](https://martinfowler.com/articles/data-mesh-principles.html), Dehghani, Dec 2020 |
| Decomposition follows organisational seams | What axis to decompose on | Practitioner | Same |
| No product owned by multiple domains | Whether ownership is unambiguous | Practitioner | Same, and [Designing data products](https://martinfowler.com/articles/designing-data-products.html), Prakash, Dec 2024 |
| Polysemes are modelled by governance, not by a canonical model | How a concept shared across domains is governed | Practitioner | [Data Mesh Principles](https://martinfowler.com/articles/data-mesh-principles.html) |
| Cohesion test: describable in one or two sentences | Whether the boundary is well-defined at all | Practitioner | [Designing data products](https://martinfowler.com/articles/designing-data-products.html) |
| Valuable on its own, without joins to another product | Whether the boundary is in the right place | Practitioner | Same |
| One denormalised table as the product grain | The size of a data product, **not of a bundle** | Practitioner | Same. See the warning below |
| Start with one team, split on cognitive load | When to federate | Practitioner | Same |
| Blueprint consistency reduces the later split cost | How to make a future split cheap | Practitioner | Same |
| A stable owner responsible for semantics, quality and operations | Whether a product should exist at all | Practitioner | [The right size of a Data Product](https://www.innoq.com/en/blog/2026/03/autonomous-data-product-size-heuristics/), innoq, Mar 2026 |
| Consumer fit: real users must exist now, not hypothetically | Whether a boundary serves anyone | Practitioner | Same |
| Bounded scope: only what is needed now | Guard against speculative scope | Practitioner | Same |
| Integration burden: smallest useful standalone unit | Whether consumers must reconstruct context | Same | Same |
| Fine-grained decomposition is costly in infrastructure | The cost side of many small units | Practitioner | [Data Mesh topologies and domain granularity](https://towardsdatascience.com/data-mesh-topologies-and-domain-granularity-65290a4ebb90/), Strengholt |
| Federation has preconditions: interoperability, metadata, governance and security standards agreed across domains | Whether an organisation is ready to federate | Practitioner | Same |
| Technical modularity without matching ownership is still monolithic | Whether a split is real or cosmetic | Practitioner | [Linking Modular Architecture to Development Teams](https://martinfowler.com/articles/linking-modular-arch.html), Foster, Thoughtworks, Jun 2023 |
| System and organisation must be decomposed together | Whether you may split artefacts ahead of teams | Practitioner | [Conway's Law](https://martinfowler.com/bliki/ConwaysLaw.html), Fowler, quoting Conway |

## C. Governance roles

| Criterion | What it tests | Class | Source |
|:----------|:--------------|:------|:-------|
| Owner, steward and custodian are three roles | Who is accountable for meaning against who implements | **Community** | DAMA-DMBOK model, but taken from practitioner blog summaries in search results, **not from DMBOK itself**. Treat as well-established practice, not as a cited standard |
| Unity Catalog owner is a group principal, not a person | That the tool's "owner" is not the business owner | Vendor | [Unity Catalog best practices](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/best-practices) |
| The schema is the permission boundary, independent of the bundle | That grants do not force a bundle split | Vendor | Same |
| Catalogs are the primary unit of data isolation | Where isolation begins | Vendor | Same |

## D. Platform mechanics used as constraints

| Constraint | Class | Source |
|:-----------|:------|:-------|
| A failed flow does not fail parallel flows in a triggered pipeline | Vendor | [Manage data quality with pipeline expectations](https://learn.microsoft.com/en-us/azure/databricks/ldp/expectations) |
| Expectations are row-level and cannot contain cross-table subqueries | Vendor | Same |
| A validation table does not gate its downstream tables | Vendor | [Expectation patterns](https://learn.microsoft.com/en-us/azure/databricks/ldp/expectation-patterns) |
| One repository with a shared folder is the recommendation | Vendor | [Sharing bundles and bundle files](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/sharing) |
| Pipelines take an editable install via `environment.dependencies`, not a built wheel | Vendor | [Bundle library dependencies](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/library-dependencies) |
| A private wheel must be downloaded locally before a bundle can reference it | Vendor | [Use a private artifact in a bundle](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/artifact-private) |
| Lineage is emitted at read and write time, so it detects and cannot prevent | Vendor | [Lineage in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/data-lineage) |
| Lineage is not preserved across renames, so a rename destroys history | Vendor | Same |
| GitLab is not among the documented CI integrations | Vendor | [CI/CD on Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/). A **verified absence**, re-check before relying on it |

## E. Conformance grading, our own

| Criterion | Class | Note |
|:----------|:------|:-----|
| Determined, Underspecified, Conflict, Gap | **Derived** | Devised in session. No external source |
| Gaps and conflicts from one pass, predictability only from variance across independent runs | **Derived** | Follows from what each verdict is a property of |
| Attribution: every design element cites a record and section | **Derived** | The rule that makes gaps visible |

---

## What to distrust, in order

**The derived rows.** Four criteria have no source: the cost of splitting later, and the three
conformance grading rules. The first is untested and, if wrong, makes starting coarse cheaper
still, so the error is conservative. The other three are method rather than fact.

**The one community row.** The owner, steward and custodian split came from search summaries of
practitioner blogs, not from DAMA-DMBOK, which is a book and not fetchable. It is widely repeated
and probably accurate, and it is still the weakest citation in the register.

**One trap worth naming.** Prakash's product grain is "a single denormalized table". Read
carelessly it argues for many bundles. It does not: a data product is roughly an entity, and a
bundle can deploy many. Confusing those two axes is exactly what produced the seven-bundle
assumption. His *phasing* guidance bears on bundles; his *sizing* guidance does not.

**One thing that answered nothing.** A Databricks community thread on medallion architecture inside
bundles was fetched and did not address whether layers should be separate bundles. A staff reply
covered folder naming and a second said only "Checking." Recorded so nobody re-fetches it hoping.

**One claim withdrawn.** That the data mesh literature invokes Conway's law. It does not. The
principles article never mentions Conway, and what it actually says is that decomposition follows
organisational seams. The claim came from a search summary and was corrected against the primary
source.

---

All external pages fetched and verified 2026-08-04, 2026-08-06 or 2026-08-07, each carrying a
last-updated date within twelve months where one is published.
