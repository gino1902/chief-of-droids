# Epic roadmap for the greenfield medallion data platform

Drafted from `track-definitions.md`, covering all five tracks. Every activity and deliverable there maps to exactly one epic here, recorded in the coverage map at the end.

Two series. An E epic is one body of work with fixed content, even where it stays open, as the standing and runway epics do. A G epic is a template, instantiated per slice, per shared dimension or per restricted data class, with different content each time.

So the programme is 24 fixed epics plus 6 templates. E2's backlog gives the instance count, nothing gives the effort, and a G2 endpoint is anything from a dashboard to a full front-end application. Most of the delivery volume sits behind the G set and is invisible in a count of thirty.

The platform is a 2026 Azure Databricks workspace on Premium, Unity Catalog, medallion (`Bronze`, `Silver`, `Gold`). Infrastructure is Terraform: `hashicorp/azurerm` for Azure resources, `databricks/databricks` inside the workspace. Workloads ship through Declarative Automation Bundles. CI/CD on Azure DevOps.

Feature names and lifecycle status verified against Microsoft Learn for Azure Databricks on 21 August 2026, sources at the end. Premium is effectively the only plan: new Standard workspaces blocked since 1 April 2026, existing ones auto-upgraded by 1 October 2026.

## How to read this roadmap

Epic type follows SAFe. Enabler epics build the architectural runway. Business epics deliver something a user can see. The blockquote under each epic heading states the runway unlocked or the value delivered.

Each epic's attribute line gives its type, owning track, cadence or instance key, and dependencies. The track is ownership, not position in time. Tracks run in parallel as swimlanes and never induce work order.

E epics are numbered in dependency order, not track order. The dependency line is what binds delivery, and epics with the same dependencies run in parallel in different swimlanes. G numbers carry no order: a template's position is set by the instance that opens it, and the G set sits mid-graph, not at the tail, since E21 to E24 all depend on one.

Dependency levels group epics by earliest possible start. A level is not a phase and not a PI. Chains inside a level are expected: the level says when an epic becomes reachable, the dependency line says what blocks it.

Two levels hold a single track each: E5 to E9 are all Infrastructure, E10 to E18 all Platform engineering. That follows from the dependency, not from phasing, since every later artefact is written into the workspace. The test is whether an epic waits on a track or on a deliverable. Where an epic needs only part of a predecessor, its dependency line says which part.

Level 4 holds the slice templates, which recur once per slice, so later levels overlap earlier ones for the whole life of the programme.

Platform engineering epics carry one of three cadence tags from the track definitions. Upfront baseline completes before the first slice. Standing never closes and absorbs decisions as they arrive. Runway delivers what the next slices need and extends as they need more, neither designed in full upfront nor withheld until repetition piles up: built for the plane to take off, extended as the plane grows.

## Dependency spine

- Level 0, head of plan. E1 to E4. No technical precondition. E4 is standing and stays open for the whole programme.
- Level 1, secure foundation. E5 to E9. Needs the workspace type decision from E1.
- Level 2, platform baseline. E10 to E18. Needs the deployed workspace, not the whole of E9. The test suite, remote state and rebuild proof in E9 run alongside this level and gate the first slice instead. E13 is the exception in this range: it is runway, so it opens here and never completes, delivering alongside every slice.
- Level 3, slice enablers. E19 and E20. Needs the platform baseline and the slice backlog.
- Level 4, the slice bundle. G1 to G4. Instantiated once per slice across three tracks, Data engineering, the Usage layer and Deployment, which owns two of the four. The first instance also proves the pattern.
- Level 5, cross-slice. G5 and G6. Opened by a condition a slice brings, binding on every slice already delivered.
- Level 6, measurement. E21 and E22. Needs accumulated usage and at least one live endpoint.
- Level 7, demand. E23 and E24. Open on a recorded demand.

## Delivery risk

Several features this roadmap depends on are not generally available on Azure. Status is stated inline on the affected criterion. The register below is dated 21 August 2026 and needs re-checking before each epic starts.

- The serverless allowlist migration is already overdue. Storage accounts that allowlist serverless compute by the old subnet IDs had to move to the Azure network security perimeter and the `AzureDatabricksServerless` service tag by 9 June 2026. That date has passed, so any legacy subnet allowlist still in the estate is non-compliant today. E8 remediates it.
- Three system tables the observability work reads are Public Preview on Azure: `system.access.audit`, `system.query.history` and `system.lakeflow.pipelines`. E8, G2, E21 and E22 all depend on them, so the cost mart and the adoption read sit on preview tables. `system.billing.usage`, `system.billing.list_prices`, `system.lakeflow.jobs` and most of `system.compute` are generally available.
- Serverless usage policies, the mechanism that attributes serverless spend to a tag, are Public Preview. Budgets themselves are generally available, so E11, E17 and E21 depend on the preview half of the attribution chain.
- Anomaly detection, which covers freshness and completeness, is Public Preview on Azure, and some of its sub-features are Beta behind the admin previews page. Data profiling, formerly Lakehouse Monitoring, is generally available. E16 splits its criteria along that line.
- GRANT policies inside Unity Catalog attribute based access control are Beta, although ABAC policies themselves reached general availability around 28 April 2026. G6 uses ABAC and stays off GRANT policies.
- The Multi-Agent Supervisor API in Agent Bricks is Beta, and the Custom LLM and Information Extraction agents are marked legacy. E24 excludes all three.
- On-behalf-of-user resource authorisation for Databricks Apps is Public Preview on Azure. E23 states the fallback.
- Lakeflow Connect managed connectors sit in different release states, so the brand name says nothing about a given connector. E14 requires the state of the specific connector to be confirmed before a date is committed to a source that needs it.
- Two deprecations are announced with no date attached. Secure cluster connectivity is to become mandatory for all classic workspaces, and creating a classic workspace on a Databricks-managed virtual network is to be deprecated in favour of VNet injection. E1 and E5 build for the post-deprecation shape.
- `system.operational_data` and `system.lineage` are already deprecated and return no rows. Nothing in this roadmap reads them.

---

## E1. Workspace type decision

Enabler, Infrastructure and platforming. No dependency. Gates E5 to E9.

> Decide and record the workspace type, so that everything built on it has a fixed target. The working assumption is a hybrid workspace, which keeps both serverless and provisioned compute available. The decision is not yet taken, and it comes first because it is the one choice that closes an option permanently.

Acceptance criteria:
- Both options are documented with what each implies downstream. A hybrid workspace, which the documentation also calls a classic workspace, keeps the classic compute plane, so it needs VNet injection, secure cluster connectivity and back-end Private Link, and it keeps the serverless path alongside them. A serverless workspace, generally available on Azure since March 2026, removes the classic compute plane and with it VNet injection.
- The decision spells out what it does to compute, which is the part you cannot undo. Hybrid keeps both serverless and provisioned compute available, so the per-workload choice stays open and gets made later at the provisioning gate in E4. Serverless-only deletes provisioned compute as an option. Do not close that option as a side effect of a network preference.
- The decision spells out what it does to this roadmap. On hybrid, E5 is built in full and E8 adds the serverless path on top. On serverless-only, most of E5 has nothing to attach to and the network work moves into E8.
- Build for the two announced deprecations now: turn secure cluster connectivity on from the start, and use VNet injection instead of a Databricks-managed virtual network. Neither deprecation has a published date, so treat them as direction, not as a deadline to plan against.
- Premium is a given, not a choice. The decision notes what depends on it, namely Unity Catalog and predictive optimization.
- One type is chosen, with the reasoning and the rejected option recorded in an architecture decision, signed off by architecture and security before any infrastructure work starts.

## E2. Use case selection and ordered slice backlog

Enabler, Deployment. No dependency. Gates E20 and every slice.

> Turn use case selection into an ordered slice backlog with explicit criteria, so that delivery order is a business decision, not an accident of which source was easiest to ingest.

Acceptance criteria:
- The selection process is run with the business stakeholders and its output is a scored, ordered list of candidate use cases.
- The selection criteria and the sequencing criteria are written down and applied consistently, so the order can be defended and re-run when priorities change.
- Each backlog item names its owning business team, the report or application it replaces, and the source systems it needs.
- The first slice is identified, and its choice is justified against the criteria.
- The backlog is a living artefact with a stated re-ordering cadence and owner.

## E3. Model inventory of the production reporting estate

Enabler, Platform engineering, upfront baseline. Depends on E2 for priority order. Needs the Power BI capacity prerequisite that E18 also confirms, met from the Power BI side alone. Feeds E19 and G1.

> Catalogue the production star schemas the platform will replace and establish the access route to the live semantic models, so that parity tests and `Gold` modelling are specified from what users read today.

Acceptance criteria:
- Every production Power BI semantic model behind a backlog item from E2 is catalogued with its fact tables, dimension tables, grain, keys and measure definitions. A use case added to the backlog later extends the inventory rather than reopening this epic.
- Measure definitions are captured as DAX expressions, not as descriptions, so a parity comparison can reproduce them.
- The access route to the live semantic models is established and tested, through the XMLA endpoint on the Power BI capacity, and the credential and permission it needs are recorded. Until the Key Vault-backed scope from E7 exists, the credential is held under the interim custody route named in this epic, and moved to the scope when E7 closes.
- Application reports that are not in a semantic model, for example the reports served from APP, Smart and EPM, are inventoried by the same template with their source of figures named.
- The inventory feeds an architecture decision: which models are reproduced, which re-modelled, which retired, and whether reproduced measures become Unity Catalog metric views on `Gold` or are implemented per report.

## E4. Architecture decision log and standing decisions

Enabler, Platform engineering, standing. No dependency. Open for the whole programme.

> Establish the architecture decision log and the practice that keeps it current, so that every standing decision has one home, one owner and a stated trigger.

Acceptance criteria:
- The decision log exists with a fixed template, a numbering scheme and a review route, and it is version controlled with the platform code.
- The alerting and freshness decision records which tables are monitored, at what threshold, where an alert lands, and which monitoring mechanism carries it, given that anomaly detection is Public Preview.
- Every provisioning request for compute beyond the serverless baseline is a decision in the log that quotes measured usage numbers, and is refused if it does not. The cost mart in E21 is the source once it exists. Before then, the numbers come directly from `system.billing.usage` and `system.compute`, which populate from the first workload, and the decision names which source it quotes. This deliverable sits at a track junction and Platform engineering owns it.
- The residual-risk review from E15 runs on every pipeline before promotion and its outcome is recorded per pipeline. The checklist is built once in E15, the recurring review lives here, because the track definitions place it in the standing set.
- Each preview or Beta dependency in the delivery risk register above has a recorded decision stating whether the programme accepts it, with the fallback if the feature does not reach general availability in time.
- Each standing decision names the event that triggers it, so decisions land when the trigger fires and not on a review cycle.
- A superseded decision is marked as superseded with a pointer to the replacement, and it stays in the log.

## E5. Network foundation

Enabler, Infrastructure and platforming. Depends on E1. Shape set by the workspace type chosen there.

> Configure the network resources group and the workspace network, so that the workspace is deployed into a controlled network from the start and no workload ever runs on a default or public path.

Acceptance criteria:
- The network resources group is created with its address space planned against the workspace type chosen in E1.
- For a hybrid workspace, the workspace virtual network is provisioned by VNet injection, with subnets, delegation and routing set for the classic compute plane. A Databricks-managed virtual network is not used, since its creation path is announced for deprecation.
- Secure cluster connectivity is enabled, so classic compute nodes carry no public IP address. This is built in rather than deferred, because it is announced to become mandatory for classic workspaces.
- Front-end Azure Private Link is configured for the workspace control plane and tested from an internal client. Back-end Private Link is configured where the workspace type has a classic compute plane, noting that it requires VNet injection and secure cluster connectivity.
- Under the hybrid workspace assumed in E1, every criterion above applies and this epic is delivered in full. E8 adds the serverless connectivity path alongside it rather than replacing any of it. If E1 records a serverless workspace instead, the classic criteria above are marked not applicable and the network position moves into E8.
- The configuration is expressed in Terraform through `hashicorp/azurerm` and the Databricks provider. No resource in this epic is created through the portal.

## E6. Catalog and landing zone storage

Enabler, Infrastructure and platforming. Depends on E1. Feeds E10.

> Provision catalog and landing zone storage with the identity that reaches it, so that governed storage and a drop point exist before any pipeline is written.

Acceptance criteria:
- ADLS Gen2 storage is provisioned for catalog managed storage and for the landing zone, with the container and path layout documented.
- An Access Connector for Azure Databricks is created and its Azure managed identity is granted the storage roles at the documented scope. A service principal is not used for this, because only a managed identity can reach an ADLS Gen2 account behind a storage firewall.
- Access is tested end to end from the workspace, both read and write, and the test is repeatable.
- The storage firewall allows only the platform paths. For a hybrid workspace the access connector is allowlisted as a firewall exception or reached through trusted-services access, and serverless SQL warehouses are allowlisted separately through the network security perimeter in E8.
- A request from outside the approved paths is refused and the refusal is observed.
- Storage, access connector and role assignments are all Terraform managed, with no manually created role assignment left in place.

## E7. Identity federation, groups and secrets

Enabler, Infrastructure and platforming. Depends on E1. Feeds E10 and E12.

> Federate identity, define the account group model, and stand up service principal credentials and secrets, so that every actor is a governed identity and no credential sits in code.

Acceptance criteria:
- Automatic identity management is confirmed active, syncing users, groups and service principals from Microsoft Entra ID. SCIM provisioning is not configured, since automatic identity management supersedes it and is default-on for accounts created after 1 August 2025.
- The single-tenant assumption is verified. If any in-scope directory is a different Entra tenant, that case is recorded as an exception, because automatic identity management does not support cross-tenant directories and would need SCIM with Entra B2B instead.
- The account group model is defined and documented: which groups exist, what each one is for, and which are the grant targets that E10 writes against.
- A group is assigned to the workspace, and workspace access is proven to follow group membership rather than individual assignment.
- Service principal credentials exist for CI/CD and for job execution. Azure DevOps pipelines authenticate through workload identity federation, so no client secret is stored for deployment.
- Secrets are held in Azure Key Vault-backed secret scopes, and a workload reads a secret through a scope with no credential present in source, in job configuration or in notebook state. The scope is configured against the Key Vault access policy model, since Azure RBAC is not supported for this path.
- Any dependency on the Identity Attribute Control List add-on, for syncing attributes such as title, department or cost centre, is recorded as Beta and given a fallback.

## E8. Serverless connectivity, network security and platform monitoring

Enabler, Infrastructure and platforming. Depends on E5 and E6. Its connectivity and egress criteria gate E9. Its monitoring baseline gates the first slice, not the platform baseline.

> Configure the serverless connectivity path and the security and monitoring around it, so that serverless compute reaches storage over private paths, egress is controlled, and telemetry is readable from day one.

Acceptance criteria:
- A network connectivity configuration is created and attached to the workspace, with private endpoints from serverless compute to catalog storage and to the landing zone, proven by a serverless workload reading both.
- Egress from serverless compute is restricted through a network policy to the approved destinations, and a request to an unapproved destination is blocked and the block is observed.
- Every storage account the platform reads is allowlisted through the Azure network security perimeter using the `AzureDatabricksServerless` service tag. Any legacy allowlist by serverless subnet ID is found and removed, since that path was retired on 9 June 2026 and is already non-compliant.
- Network security controls cover both the classic and the serverless connectivity path, with the difference between them written down.
- Platform monitoring reads the system tables. Per schema, record whether it needs enabling, what its retention is, and which group holds the grant. Flag `system.access.audit`, `system.query.history` and `system.lakeflow.pipelines` as Public Preview, a risk every epic that reads them inherits.
- A monitoring baseline exists before the first pipeline, so the first slice does not run unobserved.

## E9. Terraformed workspace with its test suite

Enabler, Infrastructure and platforming. Depends on E5, E6, E7 and E8. Its deployed workspace gates E10, E11, E12 and E18. Its test suite, remote state and rebuild proof gate the first slice, not the platform baseline, so Level 2 runs alongside them.

> Deliver the workspace as tested code with remote state and its own pipeline, so that the foundation is reproducible and a rebuild is a pipeline run.

Acceptance criteria:
- The workspace and every resource from E5 to E8 are generated from Terraform, held in version control, with `hashicorp/azurerm` provisioning the Azure resources and `databricks/databricks` managing what lives inside the workspace. Provider versions are pinned.
- Terraform state is remote, locked and access controlled, with the backend documented.
- The infrastructure code has its own pipeline, separate from the workload pipeline in E12, with plan on pull request and apply gated on review.
- An automated test suite runs against the deployed workspace and asserts the security properties that matter: no public compute path, private storage access, group-driven workspace access, restricted egress.
- Settings that Terraform cannot manage safely are documented in a manual checklist with an owner and a verification step. `databricks_workspace_conf` covers only a limited set of workspace settings and cannot reliably revert them on destroy, so anything set through it is listed there as effectively one-way.
- A destroy and rebuild into a clean subscription is proven at least once. Every setting that blocks a clean rebuild is named individually in the manual checklist above with the manual step that restores it, so the rebuild either passes or produces a finite list of manual steps.

## E10. Governance surface as code

Enabler, Platform engineering, upfront baseline. Depends on E6, E7 and E9. Gates E14 and G1.

> Author the governance surface as code, so that every object lands in a governed namespace with an owner and a tag, and no schema is created by hand.

Acceptance criteria:
- Catalogs, schemas and volumes are declared through `databricks_catalog`, `databricks_schema` and `databricks_volume` for the medallion layers and for the platform's own objects, with the naming standard documented.
- The landing zone is exposed as a Unity Catalog volume, with the storage credential and the external location declared here through `databricks_storage_credential` and `databricks_external_location`, referencing the access connector from E6, rather than in the infrastructure code. This deliverable sits at a track junction and Platform engineering owns it.
- Grants are written through `databricks_grant` against the account groups from E7, never individual users. Least privilege is proven by a denied attempt recorded in `system.access.audit`, which is Public Preview on Azure.
- Governed tags are defined and enforced through account-level tag policies, so an object or a workload that carries no owner and no use case tag cannot be created. The account limits of 1,000 governed tags and 500 allowed values per tag are checked against the planned taxonomy.
- Rule-based automatic tag assignment is not used, because it is Beta. Tag assignment is carried by the tag policies above and by the bundle definitions in E12.
- For every object type, one owner is named: infrastructure code or governance code. Nothing is declared twice and nothing falls between the two.
- A single pipeline run recreates the whole governance surface in an empty catalog.

## E11. Compute baseline and exception policy

Enabler, Platform engineering, upfront baseline. Depends on the deployed workspace from E9, and on E10 for the governed tags its policies enforce. Feeds E4 and E17.

> Set the compute baseline, serverless by default, and the policies for any exception, so that any departure from serverless is a recorded decision.

Acceptance criteria:
- Serverless is the declared default for Lakeflow Jobs, Lakeflow pipelines, notebooks and SQL warehouses, and the baseline states which workload types it covers.
- Compute policies exist for the exception path and enforce the governed tags from E10, so untagged classic compute cannot be launched.
- Serverless usage policies are configured to attribute serverless spend by tag. Their Public Preview status is recorded, together with the two known limits: they do not apply to classic or provisioned compute, and they do not backfill onto workloads that already exist.
- The route to request non-serverless compute is documented and runs through the provisioning gate in E4. The gate requires measured usage numbers, and the baseline states where they come from before the cost mart exists, so a slice that hits a serverless limit early has a documented route rather than a dead end.
- The escalation path is tested once against real usage numbers, so the gate is proven to be passable and not merely declared.
- A test workload launched outside the baseline is refused, and the refusal is observable.

## E12. Deployment and packaging standard

Enabler, Platform engineering, upfront baseline. Depends on E7, E9 and E10. Gates E15.

> Set the deployment and packaging standard and fix which catalog objects it owns, so that every artefact ships as a repeatable release and the two tooling boundaries never collide.

Acceptance criteria:
- Declarative Automation Bundles define jobs, pipelines and notebooks as code, with the project layout and the naming standard documented. The name is used as the documentation now writes it, following the rename from Databricks Asset Bundles on 16 March 2026.
- The bundle deployment engine is chosen explicitly and recorded as a decision. New bundles default to the direct deployment engine, generally available since 10 June 2026 on CLI 1.3.0 and later, rather than the older Terraform-based engine. The decision says whether bundle deployment stays separate from the infrastructure Terraform in E9. To move an existing bundle onto the new engine, run `databricks bundle migrate`.
- Environment targets exist for development, staging and production, deploying from the same bundle definitions with per-target configuration only.
- The Databricks CLI version and every tooling version are pinned, and the pipeline fails on an unpinned or drifted version rather than resolving to the latest.
- Deployment authenticates as a service principal through workload identity federation from E7, with no stored client secret.
- The tooling boundary is fixed and documented: which catalog objects the infrastructure code owns, which the governance code in E10 owns, and which the bundle owns. This deliverable sits at a track junction and Platform engineering owns it.
- A sample job deploys end to end through the pipeline into all three targets as proof.

## E13. Development framework as runway

Enabler, Platform engineering, runway. Depends on E12. Numbered here because that is all it needs to start, but it never completes: the first delivery lands with the first slice, and each extension lands with the slice that asks for it, so it runs alongside the slice bundle for the whole programme.

> Build the development framework to what the next slices need and extend it as the platform grows, so that no slice starts from nothing and nothing is designed before a slice asks for it.

Acceptance criteria:
- The first delivery carries what the first slice needs to start and no more: the project tree and the templates that slice will actually use, aligned to the bundle layout from E12.
- Each later extension names the slice that asked for it and what it adds, so the framework's growth is traceable to demand.
- Each extension is decided through an architecture decision in E4, stating what moves into the framework and what deliberately stays per slice.
- The framework is delivered as a versioned artefact a slice can install.
- A slice migrated onto a new version still passes its parity tests, so an extension is proven to change structure and not results.
- The framework is never a precondition of a slice. A slice can be delivered while an extension it asked for has not landed yet.

## E14. Ingestion standard for the landing zone

Enabler, Platform engineering, upfront baseline. Depends on E10 and E12. Gates G1.

> Set the ingestion standard for the landing zone and rule where a managed connector applies instead, so that every source is ingested the same way and the choice is made once.

Acceptance criteria:
- The default ingestion pattern is Auto Loader reading the Unity Catalog volume from E10, with the standard specifying incremental file discovery, checkpoint location, schema inference and evolution mode, and retention of the `_rescued_data` column.
- The standard says when to use a Lakeflow Connect managed connector instead of reading the landing zone. Connectors sit in different release states, so check the status of the specific connector before committing a date to any source that depends on it.
- Idempotency and reprocessing behaviour are specified, so a re-run after a failure produces no duplicates in `Bronze`.
- The standard states what `Bronze` records and what it never does, in particular that it is append-only and applies no business logic.
- Pipeline code targets `from pyspark import pipelines as dp`, not the legacy `import dlt`. The standard notes that classic billing records may still carry a Delta Live Tables prefix after the rename to Lakeflow pipelines.
- A reference implementation exists against a sample drop and is the template the first slice starts from.

## E15. CI quality gates and residual-risk review

Enabler, Platform engineering, upfront baseline. Depends on E12. Gates G1.

> Establish the CI quality gates and the residual-risk review that covers what automation cannot check, so that no pipeline reaches production untested, undeployed or unreviewed.

Acceptance criteria:
- Unit tests on transformation code run on every merge request and block the merge on failure.
- `databricks bundle validate` and a deploy to the development target run on every merge request.
- A smoke run against sample data executes the deployed artefact and asserts its output, so a deployable but broken pipeline is caught before promotion.
- The promotion rule from development to staging to production is enforced by the pipeline itself, so a promotion that skips a stage fails.
- The parity comparator's own tests run on every merge, so the tool that proves parity is itself tested. This deliverable sits at a track junction and Platform engineering owns it.
- The residual-risk review checklist exists as a versioned artefact and is exercised once against the first pipeline that reaches promotion. Running it on every later pipeline is a standing obligation carried by E4, so this epic can close while the review continues. This deliverable sits at a track junction and Platform engineering owns it.

## E16. Data quality standard

Enabler, Platform engineering, upfront baseline. Depends on E10 and E14. Gates G1.

> Set the data quality standard, so that every slice enforces quality the same way and a quality failure is visible and actionable.

Acceptance criteria:
- Expectation naming and severity are defined against the three Lakeflow pipelines expectation actions, and the behaviour of each is stated: warn keeps the row and records the violation, drop removes the row, fail stops the update.
- The quarantine pattern is specified and implemented as a reusable component. It is a recipe over expectations rather than a product feature, so the standard states where rejected records land, what metadata travels with them, and who is accountable for clearing the queue.
- Drift and distribution monitoring on critical tables uses data profiling, the generally available capability formerly called Lakehouse Monitoring.
- Freshness and completeness monitoring uses anomaly detection, and its Public Preview status on Azure is recorded, with the fallback stated: a freshness assertion in the pipeline itself if the preview cannot be relied on. Thresholds and alert routing come from the standing decision in E4.
- Validation metrics are emitted per run and are queryable, so quality over time is a measurable trend and not a per-run log line.
- The standard states which checks are mandatory in every slice and which are optional, so a slice cannot quietly ship with no expectations at all.

## E17. Cost and usage model

Enabler, Platform engineering, upfront baseline. Depends on E2, E10 and E11. Feeds E21.

> Define the cost and usage model and its attribution chain from tag to use case, so that spend lands on an owning team, with the limits of the platform's own figures stated up front.

Acceptance criteria:
- The attribution chain is defined end to end: from the governed tags enforced in E10 and the serverless usage policies in E11, through `system.billing.usage`, to the use case and the owning team.
- The mapping from tag values to use cases and teams is a maintained artefact with an owner, not a query written once.
- Budgets are configured in the account console with alerts at agreed thresholds. Budgets are generally available, while the tag-based attribution that makes them useful for chargeback rests on serverless usage policies, which are Public Preview, and that split is recorded.
- The workload types where identity or tag attribution does not populate are listed, and their usage is classified as unattributable rather than forced onto an owner.
- The model records that platform-reported cost is a list-price estimate computed from `system.billing.usage` joined to `system.billing.list_prices`, and names the Azure invoice as the authoritative billed figure.
- The model is proven against a test workload whose usage is traced from `system.billing.usage` back to a named use case.

## E18. Reporting connectivity

Enabler, Platform engineering, upfront baseline. Depends on E9 and E10. Gates E19 and G2.

> Deliver the connectivity the reporting estate needs to read the platform, so that every endpoint has one supported route in and users keep their own identity through it.

Acceptance criteria:
- A serverless SQL warehouse is provisioned for BI workloads, sized against the baseline in E11 and tagged per E10, and allowlisted through the network security perimeter per E8.
- Publishing to the Power BI service from Azure Databricks is the one supported route, configured and documented as such, so no team builds a second one.
- Single sign-on is configured through Microsoft Entra ID DirectQuery, so a report reads with the end user's identity and Unity Catalog grants apply to them rather than to a shared service account.
- The capacity prerequisite is confirmed with the owning team and recorded as a dependency with a named owner: a Power BI Premium, Premium Per User or Fabric capacity, with the XMLA endpoint set to read write. Data must be in Unity Catalog, since the Hive metastore is not supported on this path.
- The newer federated single sign-on path through the ADBC driver is explicitly out of scope, because it is Public Preview and documented for AWS only, with no Azure guidance.
- A production report reads a `Gold` table through the full path as proof, and an unauthorised user is refused on the same path.
- This deliverable sits at a track junction and Platform engineering owns it, consumed by every endpoint the Usage layer builds or repoints.

## E19. Parity comparator and tolerance model

Enabler, Data engineering. Depends on E3, E15 and E18. Gates every slice roll out. Accepted against the first slice's development target, so it does not wait on production `Gold`.

> Build the parity comparator and its tolerance model, so that a slice reproducing a figure users read today can prove it, at report grain and filter context, pass or fail per run.

Acceptance criteria:
- The comparator reads two figures and compares them at report grain and filter context: the reference from the live source users read today, a Power BI semantic model over XMLA or an application report from APP, Smart or EPM, and the platform figure from `Gold`.
- Acceptance runs against the first slice's `Gold` tables in the development target, so no production data is required to close this epic. Per-run evidence in production begins with the first slice.
- A tolerance is defined per measure type, with the reasoning recorded: exact for counts and keys, stated bounds for sums, currency and derived ratios.
- Filter context is part of the comparison, so a measure that matches in total but diverges by dimension slice fails rather than passes.
- Each run produces pass or fail evidence per measure, retained and attributable to a code version and a data state.
- The comparator is packaged as a reusable component with its own unit tests, which run at CI per E15.
- The reference access route from E3 is used, and its credential is held in the Key Vault-backed secret scope from E7.

## E20. Slice definition of done and readiness gate

Enabler, Deployment. Depends on E2, E16 and E19. Gates every slice.

> Define the slice definition of done and the readiness gate, so that a slice opens only when its preconditions are met and closes only with proven data, a consumer and an adoption route.

Acceptance criteria:
- The definition of done lists every condition a slice must meet to close, covering data, quality evidence, parity evidence, a live endpoint, an enabled business team and a retired predecessor.
- The readiness gate lists every condition a slice must meet to start, covering a named business owner, an identified reference figure, available source access, and a landing zone contract for every source the slice reads. The gate checks the contract exists. Agreeing it is work inside G1.
- The gate has a named owner who can refuse to open a slice, and a refusal is recorded with its reason.
- Both artefacts are applied to the first slice's gate, which is what closes this epic. Revising them after the first slice runs is a standing decision in E4, not a condition of this epic, so the second slice is never blocked waiting for the first to close.
- The definition of done is the same for every slice, and any exception is an architecture decision in E4 rather than a local negotiation.

---

## E21. Cost mart

Business, Data engineering. Depends on E17, G1 and G2, and on accumulated usage data.

> Build the cost mart over the platform's own usage data, joined to the use case and team mapping, so that spend and adoption are readable in one place and every provisioning decision can quote a number.

Acceptance criteria:
- The mart models `system.billing.usage` and `system.billing.list_prices`, both generally available, joined to the use case and team mapping from E17.
- Job and pipeline activity comes from `system.lakeflow`, and compute activity from `system.compute`. The mart records which of these schemas are generally available and which are Public Preview, since `system.lakeflow.pipelines` and parts of `system.compute` are preview on Azure.
- Query activity comes from `system.query.history` and endpoint activity from `system.access.audit`, both Public Preview. The mart states the consequence: a schema change or a preview gap breaks a view rather than silently returning fewer rows, and the views are written to fail loudly.
- Endpoint usage telemetry from G2 is modelled into the mart, so adoption and cost sit in the same model.
- Cost is readable by use case, by team and by workload type, and a given cost line can be traced back to a named job, pipeline, warehouse or endpoint.
- Usage that cannot be attributed is reported as unattributed, with its share visible, rather than distributed across owners. Classic compute is expected here, since serverless usage policies do not cover it.
- The list-price caveat from E17 is surfaced in the mart itself, so a reader cannot mistake an estimate for a billed figure.
- `system.operational_data` and `system.lineage` are not read, since both are deprecated and return no rows.
- The mart is the source E4 provisioning decisions and E22 adoption reads both quote. It is built with the same quality discipline as a slice, but it is not one: it replaces no report, has no reference figure to compare against and no business team to invite, so the slice definition of done does not apply to it.
- This deliverable sits at a track junction and Data engineering owns it.

## E22. Adoption measurement

Business, Deployment. Depends on G2 and E21.

> Define the per-team adoption metrics and read them periodically from the cost mart, so that a stalling use case is visible early enough to act on.

Acceptance criteria:
- Adoption metrics are defined per team, with each metric stating its numerator, its denominator and its observation window.
- The metric definitions state what counts as active use, so a scheduled refresh is not mistaken for a user reading a report. Human activity is separated from service principal activity in the source data.
- The periodic read runs on a stated cadence against the cost mart, and its output goes to the track leaders and the business owners.
- A metric that falls below a stated threshold triggers a conversation with the owning team, and the trigger and route are documented.
- Any endpoint with no telemetry is reported as unmeasurable rather than as unused, and the preview status of the underlying audit and query history tables is carried into how confidently the numbers are presented.

## E23. Custom applications on Gold

Business, Usage layer. Depends on E18 and G1, opened on first demand.

> Build custom applications on `Gold` where a dashboard cannot serve the need, so that interaction and write-back use cases have a route, without building app infrastructure ahead of a request.

Acceptance criteria:
- A recorded demand exists and says why an AI/BI Dashboard cannot serve it.
- The application is a Databricks App, a containerised service on serverless compute. It reaches its SQL warehouse, job, Genie Agent, secret, volume and Unity Catalog table through declared app resources, not ad hoc connections.
- Identity handling is decided explicitly. On-behalf-of-user resource authorisation is Public Preview on Azure. If the app must read as the end user, record the preview dependency in E4. The fallback is a service principal identity, with the narrower grants that implies.
- The application ships through the packaging standard from E12, with the same CI gates from E15.
- Its usage telemetry is registered and feeds the cost mart on the same basis as G2.
- The application is delivered only against the recorded demand above, and its scope is bounded by what that demand states.

## E24. Agent and workflow endpoints

Business, Usage layer. Depends on G1, G6 and E21, opened on first demand.

> Deliver agent and workflow endpoints on `Gold` once a demand arrives, with the stack settled by an architecture decision, so that the platform meets those use cases without committing to a stack first.

Acceptance criteria:
- The first demand is recorded with its use case, its user group and the figures or actions it needs.
- An architecture decision in E4 settles the stack, comparing the low-code Agent Bricks route against code-first custom agent authoring on MLflow 3. The decision uses current naming, since the Mosaic AI Agent Framework branding is retired and workflow orchestration is now Lakeflow Jobs.
- Three options are out of scope unless the decision explicitly accepts their status: the Agent Bricks Multi-Agent Supervisor API, which is Beta, and the Custom LLM and Information Extraction agents, which are marked legacy. The Knowledge Assistant is generally available on Azure and is the default starting point, subject to a region check for the workspace region.
- The endpoint reads `Gold` through governed access under the requesting user's identity where the stack supports it, and protection policies from G6 apply.
- Agent and service principal activity is distinguishable from human activity in the cost mart, so agent cost and agent adoption are separately readable.
- Its usage telemetry is registered and feeds the cost mart on the same basis as G2.
- The endpoint is delivered only against the recorded demand above, and its scope is bounded by what that demand states.

---

## Generic epics

The six below are templates, not work items you can schedule once. Each is a shape plus a rule for when a new instance opens.

The slice is the driver. Four open once per slice, in backlog order from E2. The other two open on a condition a slice brings: a shared dimension, or a restricted data class.

They close per instance, never globally, so their criteria read as acceptance criteria per instance.

Instance size is not uniform, and G2 is where the variance sits: a dashboard instance is small, a front-end application is a full build with its own identity handling, telemetry and CI. The backlog gives the count, not the effort.

### Binding templates

Most templates close per instance. The slice ships and nothing about it obliges the slices before it.

G5 and G6 do not. Each owns a shared artefact that later work builds on, and each gains entries for the life of the programme. Extending a shared dimension re-runs every prior slice's parity tests. Adding a restricted data class means a new policy, a proof that restricted and unrestricted reads both behave, and a regression pass over every measure reading that column.

So the cost of an entry is not the entry. It is the re-proof of everything built on the artefact, and it grows with each slice delivered. A dimension registered at slice two is cheap. The same one at slice nine pays for eight parity re-runs.

This is the mirror of the runway principle in E13. Runway is extended for a plane that has not taken off, so its cost is forward-looking and paid once. A binding artefact is extended for a platform already flying, so its cost is paid again by everything in the air. Both stay open. Only the binding kind gets cheaper for being early.

In SAFe terms both are enabler epics keeping the architectural runway current, which is why neither closes. The regression obligation is not a SAFe concept, it is this programme's. The sequencing rule that follows: register a conformed dimension in the earliest slice that could plausibly need it, not the first that actually does.

### Instantiation contract

| Epic | Instance key | Opens when | Count driven by | Content from |
| :--- | :----------- | :--------- | :-------------- | :----------- |
| G1 | one slice | the slice passes the readiness gate in E20 | slices in the backlog from E2 | the use case selected in E2 |
| G2 | one slice | the slice's `Gold` tables pass parity in G1 | slices in the backlog from E2 | the owning team's reporting need |
| G3 | one slice | the slice's endpoint is live | slices in the backlog from E2 | the owning business team |
| G4 | one slice | the owning team signs the endpoint fit to roll out in G3 | slices in the backlog from E2 | the superseded report and its consumers |
| G5 | one shared dimension | a slice first needs a dimension a later slice will reuse | dimensions shared across slices | the slice that first needs it |
| G6 | one restricted data class | a slice first carries data in that class | restricted classes across the estate | the data owner and the protection standard |

Slices overlap, with one exception. A later slice starts as soon as it passes the readiness gate. The exception is a shared dimension: once G5 registers one, two slices sharing it serialise on any extension, because the extension re-runs prior parity tests. This constrains scheduling from the second slice onward.

## G1. Slice data delivery, Bronze to Gold

Business, Data engineering, instantiated per slice. Depends on E10, E14, E15, E16, E19 and E20. From the second slice onward it is also bound by the register in G5.

> Drive one report's data from `Bronze` through `Silver` to `Gold`, orchestrated, quality-checked and proven at parity, so that a real consumer reads trusted data and quality is proven under real consumption.

Acceptance criteria per instance:
- For each source this slice reads, a landing zone contract exists or is agreed now, naming the producing team and its owner. A source contracted by an earlier slice is reused, not renegotiated.
- The contract states arrival: the volume path and file naming convention, the expected cadence, the format and encoding, and what a late or missing drop means.
- The contract states ordering and duplicate handling: whether order is guaranteed, whether a file can be re-dropped, and what the consumer must do when it is.
- The contract states the schema and the change process, so a producer-side change is announced rather than discovered by a failing run or absorbed silently into `_rescued_data`.
- A contract breach is detectable by the pipeline and raises an alert naming the producer, not the platform.
- `Bronze` ingests from the landing zone volume with Auto Loader per the standard in E14, append-only, with schema evolution handled and `_rescued_data` retained and queryable.
- `Silver` cleanses and standardises, and holds the history of changing records with the historisation approach stated per entity.
- `Gold` aggregates, refines and enriches into the slice's target tables, modelled against the inventory from E3. Whether reproduced measures are declared as Unity Catalog metric views over `Gold` or implemented in the target tables follows the decision taken in E3, and the slice does not settle it locally.
- All tables are Unity Catalog managed tables with liquid clustering, using `CLUSTER BY AUTO` unless a measured reason to pin the keys is recorded. No maintenance job is scheduled, because predictive optimization is default-on for accounts created on or after 11 November 2024 and runs `OPTIMIZE`, `VACUUM` and `ANALYZE` on managed tables.
- Expectations from E16 are applied at every layer, and validation metrics per run are emitted and queryable.
- A Lakeflow Job orchestrates the slice end to end, with its schedule, retries, notification routing and a stated freshness target.
- The backfill and full-refresh procedure is documented and executed at least once, and its exit condition is a parity re-run that passes.
- The parity tests for this report run inside the pipeline and pass within tolerance. A fix and re-run does not invalidate the evidence, because evidence is attributed to a code version and a data state. This deliverable sits at a track junction and Data engineering owns it.
- Every table, job and pipeline carries the governed tags from E10, so the slice appears in cost attribution from its first run.

## G2. Slice endpoint

Business, Usage layer, instantiated per slice. Depends on E18 and G1. Instance size varies with the endpoint type, from a dashboard to a front-end application.

> Build the slice's endpoint with its consumer group grants and registered telemetry, so that a consumer exists at the end of every slice and adoption is measurable from day one.

Acceptance criteria per instance:
- One endpoint exists for the slice, built as an AI/BI Dashboard unless an architecture decision in E4 says otherwise. A Genie Agent is added on the same `Gold` schema only where natural-language follow-up is asked for, using the current name after the rename from Genie Spaces in July 2026.
- The endpoint reads `Gold` through the serverless SQL warehouse from E18, not through a private path of its own.
- The slice's consumer group exists and holds grants on the slice's `Gold` schema only, and a user outside the group is refused.
- The endpoint's usage telemetry source is registered and Deployment holds the grant to read it, so the cost mart can model it when E21 is built. This epic does not wait on the mart. This deliverable sits at a track junction and the Usage layer owns it.
- The telemetry sources are named: dashboard views from `system.access.audit`, query activity from `system.query.history` on its `dashboard_id` column, and Genie activity from `service_name = 'aibiGenie'`. Both tables are Public Preview on Azure, and the usage-monitoring guidance carries a preview banner too, so the endpoint ships with that risk on the record.
- The endpoint reproduces the figures of the report it replaces, cross-checked against the parity evidence from G1 rather than assumed from it.
- Exactly one endpoint is delivered for the slice, in whatever form that slice needs, dashboard or application. An endpoint demanded later against a `Gold` schema whose slice has already closed is not this epic, it is E23 or E24.

## G3. Slice invitation and enablement

Business, Deployment, instantiated per slice. Depends on E20 and G2.

> Invite the owning team, run its enablement, then monitor usage and capture feedback, so that adoption is invited rather than imposed and the next iteration follows what the team does.

Acceptance criteria per instance:
- The owning business team is invited, with the invitation naming what changes for them and what does not.
- An enablement session is run with the team, and what was covered and who attended is recorded.
- The access request route is documented and open, and a request from a team member is served through it end to end, ending in an account group membership rather than a direct grant.
- Usage is monitored from the endpoint's telemetry after go-live, over a stated observation window.
- Feedback is captured in a form that can be triaged into the backlog, and the triage outcome is visible to the team that raised it.
- Feedback from the observation window is triaged, and each item is either delivered or scheduled with a date. The owning business team signs that the endpoint is fit to roll out, which is the stopping rule for iteration and the condition G4 reads.

## G4. Slice roll out and predecessor retirement

Business, Deployment, instantiated per slice. Depends on G1, G2 and G3.

> Roll out the use case and retire the report it replaces with its refresh path, so that the platform becomes the single source for that figure and nothing runs twice.

Acceptance criteria per instance:
- Roll out is declared only when the slice meets the definition of done from E20 in full.
- The superseded report is retired, with the retirement communicated to its known consumers ahead of the date.
- The refresh path feeding the superseded report is decommissioned, including its schedule, its gateway where it has one, and its credential, so no orphaned job keeps running and no stale dataset keeps refreshing.
- Any consumer of the superseded report that was not in the invited team is identified before retirement and routed to the new endpoint.

## G5. Conformed dimension register

Enabler, Data engineering, instantiated per shared dimension. Depends on G1. Binding: every entry obliges every slice already delivered.

> Register the conformed dimensions and their surrogate key strategy, so that dimensions are reused across slices and a change to a shared one has a known, enforced cost.

Acceptance criteria per instance:
- The register exists and records, per conformed dimension, its grain, its business key, its surrogate key strategy and its owning slice.
- The surrogate key strategy is stated once and applied consistently, including how late-arriving and unknown members are handled.
- A second slice reuses a registered dimension rather than building its own, and the reuse is visible in Unity Catalog lineage.
- The rule that extending a shared dimension re-runs every prior slice's parity tests is written into the register and enforced by the pipeline.
- A dimension extension is exercised at least once, with the prior slices' parity re-run passing before the change is promoted.
- This deliverable sits at a track junction and Data engineering owns it.

## G6. Data protection policies

Enabler, Platform engineering, instantiated per restricted data class. Depends on E10 and E19. Binding: every entry obliges every slice already delivered.

> Set the data protection standard and implement the row filtering and column masking it calls for, so that sensitive data is restricted at the governance layer, not by copying tables per audience.

Acceptance criteria per instance:
- The standard states what classes of data are restricted, and which control applies to each: row filtering, column masking, or exclusion from `Gold` altogether.
- Rules that must hold across many tables are implemented as Unity Catalog attribute based access control policies, keyed off the governed tags from E10, which is what the documentation now recommends over per-table controls. Table-level row filters and column masks are used where a rule genuinely applies to one table.
- GRANT policies inside ABAC are not used, since they are Beta. If a requirement can only be met that way, it becomes a decision in E4 with its risk stated.
- Policies apply through the account groups from E7, never to individual users.
- A restricted read is proven: a member of an unprivileged group sees filtered rows or masked values, and a member of a privileged group sees the full value.
- Policies are declared as code alongside the governance surface in E10, so they redeploy with it.
- The standard states the interaction between protection policies and the parity tests, so a masked column does not silently fail a parity comparison. The comparator from E19 runs under an identity that can see the unmasked value, and any measure that cannot be compared that way is excluded from parity with the reason recorded per measure.
- The epic stays open. Each later slice that brings a new restricted data class classifies it, attaches its policy and records the decision, so nothing arriving at slice seven is left without a home.

## Open question for the track leaders

One tension is unresolved and should be settled before the plan is committed.

The track definitions apply the runway principle to the development framework: build what the plane needs to take off, then extend the runway as the plane grows. E13 follows it.

The same principle would apply to four deliverables scheduled as upfront baseline: the ingestion standard, the data quality standard with its quarantine pattern, the parity tolerance model, and the slice definition of done. Each is a repeated pattern written before a single slice has run, and each is a hard precondition of G1. Twenty epics stand between the head of the plan and the first row of real data, in a programme whose premise is that quality proves itself only under real consumption.

The track definitions tag those four as upfront baseline, so this roadmap keeps them there rather than overrule the source. The question for the track leaders is whether the runway tag fits them better. Governance, identity, the deployment boundary and the CI gates have a safety argument for landing in full first, because data should not land in an ungoverned namespace and code should not ship unreviewed. Runway logic does not soften that. The other four are patterns a slice would teach us. Answering this changes Level 2 and the date of the first slice.

## What this roadmap deliberately does not schedule

- Provisioned compute for scale. It exists only after an architecture decision in E4 that quotes measured usage numbers from the cost mart, so no epic assumes it.
- Table maintenance. Predictive optimization is default-on for this account and runs `OPTIMIZE`, `VACUUM` and `ANALYZE` on Unity Catalog managed tables, so no epic schedules a maintenance job.
- SCIM provisioning. Automatic identity management supersedes it and is default-on, so it is configured only if a cross-tenant directory turns up in E7.
- The development framework designed in full upfront. E13 builds it as runway, to what the next slices need, extending as they need more.
- Usage layer capability ahead of demand. E23 and E24 open on a recorded demand, and G2 delivers exactly one endpoint per slice.
- A second endpoint on a slice's `Gold` schema. That is a new demand and belongs to E23 or E24, not to the slice that created the schema.
- Features whose only documented path is Public Preview or Beta and for which a generally available alternative exists. Named per epic, with the ADBC federated single sign-on path in E18 and ABAC GRANT policies in G6 as the two clearest cases.
## Coverage map

Every deliverable in `track-definitions.md` and the epic that carries it.

| Track | Deliverable | Epic |
| :---- | :---------- | :--- |
| Infrastructure and platforming | Workspace type decision | E1 |
| Infrastructure and platforming | Network resources group and workspace network | E5 |
| Infrastructure and platforming | Catalog and landing zone storage, access identity, role assignments | E6 |
| Infrastructure and platforming | Identity federation, account group model, service principal credentials, secrets | E7 |
| Infrastructure and platforming | Serverless connectivity with private paths | E8 |
| Infrastructure and platforming | Network security and monitoring, telemetry from system tables | E8 |
| Infrastructure and platforming | Terraformed workspace, test suite, remote state, pipeline, manual checklist | E9 |
| Platform engineering | Catalog as code, tags policy, group model grants | E10 |
| Platform engineering | Compute baseline and exception policies | E11 |
| Platform engineering | Deployment and packaging standard, environment targets, pinned tooling | E12 |
| Platform engineering | Ingestion standard for the landing zone | E14 |
| Platform engineering | CI quality gates and promotion rule | E15 |
| Platform engineering | Residual-risk review checklist, built once | E15 |
| Platform engineering | Residual-risk review, run per pipeline | E4 |
| Platform engineering | Data quality standard | E16 |
| Platform engineering | Cost and usage model and attribution chain | E17 |
| Platform engineering | Reporting connectivity | E18 |
| Platform engineering | Model inventory | E3 |
| Platform engineering | Architecture decision log, alerting and freshness, provisioning gates | E4 |
| Platform engineering | Data protection policies for row filtering and masking | G6 |
| Platform engineering | Development framework, built as runway | E13 |
| Data engineering | Landing zone contract per source | G1 |
| Data engineering | Per slice `Bronze`, `Silver`, `Gold` tables | G1 |
| Data engineering | Per slice orchestrating job | G1 |
| Data engineering | Per slice backfill and full-refresh procedure | G1 |
| Data engineering | Parity tests, comparator and tolerance model | E19 |
| Data engineering | Parity tests, per report run and evidence | G1 |
| Data engineering | Conformed dimension register | G5 |
| Data engineering | Cost mart | E21 |
| Usage layer | One endpoint per slice | G2 |
| Usage layer | Consumer group and its grants on the slice `Gold` schema | G2 |
| Usage layer | Registered usage telemetry source per endpoint | G2 |
| Usage layer | Custom applications consuming `Gold` | E23 |
| Usage layer | Agent and workflow endpoints | E24 |
| Deployment | Ordered slice backlog with selection and sequencing criteria | E2 |
| Deployment | Per-slice readiness gate | E20 |
| Deployment | Slice definition of done | E20 |
| Deployment | Per slice invitation, enablement session, access request route | G3 |
| Deployment | Per-team adoption metric definitions and periodic read | E22 |
| Deployment | Per slice retirement of the superseded report and its refresh path | G4 |
| Deployment | Roll out of each use case | G4 |

## Junction deliverables

The eleven deliverables that sit where tracks meet, with the epic that carries them. Owners are taken from the junction table in `track-definitions.md` and are not reassigned here.

| Deliverable | Epic | Owner |
| :---------- | :--- | :---- |
| Landing zone volume | E10 | Platform engineering |
| Model inventory | E3 | Platform engineering |
| Reporting connectivity | E18 | Platform engineering |
| Parity tests per report | G1 | Data engineering |
| Parity tests CI gate | E15 | Platform engineering |
| Conformed dimension register | G5 | Data engineering |
| Cost mart | E21 | Data engineering |
| Endpoint usage telemetry | G2 | Usage layer |
| Residual-risk review checklist | E15, standing review in E4 | Platform engineering |
| Deployment tooling boundary | E12 | Platform engineering |
| Provisioning gate | E4 | Platform engineering |

## Sources

All verified against current Microsoft Learn documentation for Azure Databricks on 21 August 2026.

- [Workspace types and administration](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace/)
- [Classic compute plane networking](https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/)
- [Serverless network security](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/)
- [Azure managed identities for Unity Catalog storage](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/azure-managed-identities)
- [Automate Unity Catalog setup with Terraform](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/terraform/automate-uc)
- [Databricks Terraform provider](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/terraform/)
- [Automatic identity management](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/automatic-identity-management/)
- [Declarative Automation Bundles release notes](https://learn.microsoft.com/en-us/azure/databricks/release-notes/dev-tools/bundles)
- [Lakeflow Connect](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/)
- [Auto Loader schema inference and evolution](https://learn.microsoft.com/en-us/azure/databricks/ingestion/cloud-object-storage/auto-loader/schema)
- [Lakeflow pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/)
- [Data quality monitoring](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/data-quality-monitoring/)
- [Serverless usage policies](https://learn.microsoft.com/en-us/azure/databricks/admin/usage/budget-policies)
- [Predictive optimization](https://learn.microsoft.com/en-us/azure/databricks/optimizations/predictive-optimization)
- [Governed tags](https://learn.microsoft.com/en-us/azure/databricks/admin/governed-tags/)
- [Attribute based access control](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/abac/)
- [System tables](https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/)
- [Budgets](https://learn.microsoft.com/en-us/azure/databricks/admin/account-settings/budgets)
- [Publish to the Power BI service](https://learn.microsoft.com/en-us/azure/databricks/partners/bi/power-bi/service)
- [Metric views](https://learn.microsoft.com/en-us/azure/databricks/uc-semantics/metric-views/basic-modeling)
- [Monitor dashboard usage](https://learn.microsoft.com/en-us/azure/databricks/dashboards/monitor-usage)
- [Databricks Apps key concepts](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-apps/key-concepts)
- [Build custom agents](https://learn.microsoft.com/en-us/azure/databricks/agents/custom-agents/build-agents)
- [Lakeflow Jobs](https://learn.microsoft.com/en-us/azure/databricks/jobs/)

<!--
Version: 1.3 | Last Updated: 2026-08-23 | Status: Draft
-->
