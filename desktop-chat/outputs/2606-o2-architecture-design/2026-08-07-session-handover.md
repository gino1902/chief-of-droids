# Session handover, `o2-sources`

> Written 2026-08-07 at the close of the `o2-sources` session, which ran 2026-08-04 to 2026-08-07.
> Read this first, then [the carry-over note](2026-08-06-carry-over-technical-design.md) for the
> ADR sequence and the design run.

---

## Do this first

**Push. 40 commits are ahead of upstream and exist only on local disk.** That includes ADR-011,
five corrected records, the ingestion landscape, the discovery note and the conformance suite.
Nothing else on this page is worth as much as that command.

**Take the ingestion landscape to the teams.** It is the highest-value action only a person can
take, and it is the document's own stated purpose: completeness of the entities, accuracy of the
lineage, and whether ownership boundaries match system boundaries. ADR-011 rests on it as a
baseline, so sign-off converts its basis from asserted to confirmed. It would also settle four open
gaps at once: whether `Absence` and `Payroll` have producers, whether Unit4 can gain an outbound
path, and where `User` actually comes from, given `whoz__user_report` lands daily while the chart
attributes it to APP.

---

## What this session produced

**A decision record.** [ADR-011](decisions/ADR-011-ingestion-baseline-entity-contract.md), the
ingestion baseline: contract on entities, producing system as configuration, translation mappings
where semantics are incompatible. Written through the `making-architecture-decision` interview
rather than assembled, and its discriminator changed under challenge, from lifespan to semantic
incompatibility, because the Anti-Corruption Layer pattern discriminates on semantics and says
nothing about lifespan.

**A consistency sweep over five records.** ADR-003 was retained rather than deprecated, since the
deprecation had been aimed at one incidental CI clause and would have discarded a vendor-recommended
decision. ADR-002 took sole ownership of the CI platform choice. ADR-007's delivery mechanism was
wrong and now says no wheel is built at all, since jobs only orchestrate. ADR-006's approval gate
moved to GitLab terms. ADR-INDEX records the sweep.

**The ingestion landscape**,
[2026-08-06-sqli-system-ingestion-view.md](../2607-o2-requirements/2026-08-06-sqli-system-ingestion-view.md),
converged over several rounds with the two workbooks until the entity vocabulary closed: every chart
label resolves to a taxonomy entity, all 43 entity names unique and singular.

**A discovery note** carrying 15 findings and 4 proposed decisions, none approved, plus the verified
platform mechanics so they are not re-derived.

**A play**, in `skills-lab`, capturing the DKDK method that produced the findings.

---

## What the parallel session changed, and what it supersedes

Four commits landed from another session while this one was open: `935f462`, `62b09c5`, `dcf32fe`,
`a8c9f6c`. They restructured the folder and added a conformance suite. Three consequences matter.

**`decisions/` is now an isolated substrate.** All twelve records moved into it, and the suite's
README states the rule: that directory holds decision records and the index, nothing else, because
"anything placed inside becomes part of the substrate and would be ingested as if it were a
decision". So design documents, trackers and handovers like this one stay outside it. Every
relative link survived the move; I checked all of them.

**The role vocabulary is answered, differently and better than I proposed.** The suite defines
Producer, Route and Vehicle mapped to workbook columns: producer is the system of origin, route is
`source` plus `source path` plus `access-protocol`, vehicle is `filename` plus `cadence`. That is
richer than the producer-source-relay-consumer set the carry-over note still describes as pending,
and it closes discovery-note F13. **Treat the carry-over note's role-vocabulary paragraph as
superseded.**

**ADR-011's validation section overlaps the suite.** ADR-011 describes its checks in prose, and the
suite tests the same ground mechanically through change events, producer replaced, vehicle
consolidated, supply path lost. Worth deciding whether ADR-011 should cite the suite rather than
restate it.

---

## Open, in the order I would take them

| # | Item | Why it is where it is |
|:--|:-----|:----------------------|
| 1 | Push | Everything else is recoverable, this is not |
| 2 | Landscape review with the teams | Only a person can do it, and it validates ADR-011's basis |
| 3 | Reconcile ADR numbering across sessions | Cheap now, a merge conflict later. Numbers are deliberately not reserved, since a reservation in one session is invisible to another |
| 4 | Nine producer rows in `o2-data-sources.xlsx` | Largest remaining chart-versus-workbook divergence. Also `Sharepoint` still appears as a producer when it is the landing zone, and `CRM` stands where MS Dynamics belongs |
| 5 | The ownership record | Resumes at interview section 3. The hard part is below |
| 6 | The Unity Catalog record | Nothing captured beyond the analysis in the carry-over note |

**Why the ownership record needs a fresh session rather than a tired one.** One physical person
appears as three contractual roles owned by three different domains: Employee in
`hr-administration`, Subcontractor in `finance-suppliers`, Candidate in `hr-recruitment`, described
by Talent Profile in `hr-talents` and accounted for by User in `it-users`. The physical person is not
modelled at all. Under the chosen federated model that is five owners and no arbiter, which
practitioner guidance says a polyseme cannot have. It is an accepted limit rather than a solved
problem and its reopening condition has to be written down deliberately.

---

## Deliberate non-goals, so nobody reopens them by accident

**Locking the ADRs.** All Draft except ADR-008. Freezing decisions that rest on unread payloads and
an unresolved identity question would be worse than carrying them as Draft.

**Reading the payloads.** Parked. Consequence to keep in view: the feed configuration is keyed at
subdomain and the landscape at entity, so no entity-level claim in the chart can currently be
validated against the feed config. That gap closes only with the payload read.

**Building the generator or validator** for the workbook pair. Waits on the editing-architecture
decision, AD-4 in the discovery note.

**Version blocks.** Removed from records in this folder; git history is the version record.

---

## Two things stated plainly rather than buried

The two workbooks are the source of truth and are git-ignored, so they have no history. Their
*content* is committed as generated markdown, so a disk loss costs the editable form rather than the
information. Annoying, not serious.

Neither `making-architecture-decision` nor `writing-technical-design` is deployed to this
repository. Both live in `skills-lab/.claude/skills/` and both carry `disable-model-invocation:
true`, so each must be invoked explicitly and neither is reachable from a session scoped to
`chief-of-droids` alone.
