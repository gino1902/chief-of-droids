# Epic roadmap for the greenfield medallion data platform

The epic roadmap for the greenfield data platform, drafted from `track-definitions.md`. It covers the full programme, all five tracks, from the workspace type decision to the demand-driven endpoints at the tail. Every activity and every deliverable in the track definitions maps to exactly one epic here. The coverage map at the end records that mapping.

The platform is a 2026 Azure Databricks workspace on the Premium plan, with Unity Catalog and a medallion architecture (`Bronze`, `Silver`, `Gold`). Infrastructure is Terraform, using `hashicorp/azurerm` for the Azure resources and `databricks/databricks` for what lives inside the workspace. Data and AI workloads ship through Declarative Automation Bundles. CI/CD runs on Azure DevOps.

Feature names and lifecycle status were verified against current Microsoft Learn documentation for Azure Databricks on 21 August 2026. Sources are listed at the end. Premium is effectively the only plan available: new Standard workspaces have been blocked since 1 April 2026 and remaining Standard workspaces are auto-upgraded to Premium by 1 October 2026.

## How to read this roadmap

Epic type follows SAFe. Enabler epics build the architectural runway. Business epics deliver something a user can see. The blockquote under each epic heading states the runway unlocked or the value delivered.

Each epic carries an attribute line with its type, its owning track, its cadence where the track defines one, and its dependencies. The track is an ownership attribute, not a position in time. Tracks run in parallel as swimlanes and never induce work order.

The epics are numbered in dependency order, not in track order. Numbering is a reading aid. What binds delivery is the dependency line on each epic, and epics with the same dependencies can run at the same time in different swimlanes.

Dependency levels group epics by the earliest point at which they can start. A level is not a phase and not a PI. Chains inside a level are expected, so the level tells a reader roughly when an epic becomes reachable and the dependency line on the epic tells them what actually blocks it.

Two levels happen to hold a single track each. Epics 5 to 9 are all Infrastructure and platforming, and Epics 10 to 18 are all Platform engineering. That is a consequence of the dependency, not a phase: every later artefact is written into the workspace, and the track definitions describe the infrastructure block as finite and front-loaded rather than demand-ordered. The test is whether any epic waits on a track rather than on a deliverable. Where an epic needs only part of a predecessor, its dependency line says which part, so the rest of that predecessor runs in parallel.

Level 4 epics recur once per slice, so later levels overlap earlier ones for the whole life of the programme.

Platform engineering epics carry one of three cadence tags, matching the track definitions. Upfront baseline means the epic completes before the first slice starts. Standing means the epic never closes and absorbs decisions as they arrive. Runway means the epic delivers what the next slices need and extends as they need more, so it is neither designed in full upfront nor withheld until repetition has piled up. The runway is built for the plane to take off, and it extends as the plane grows.

## Dependency spine

- Level 0, head of plan. Epics 1 to 4. No technical precondition. Epic 4 is standing and stays open for the whole programme.
- Level 1, secure foundation. Epics 5 to 9. Needs the workspace type decision from Epic 1.
- Level 2, platform baseline. Epics 10 to 18. Needs the deployed workspace, not the whole of Epic 9. The test suite, remote state and rebuild proof in Epic 9 run alongside this level and gate the first slice instead. Epic 13 is the exception in this range: it is runway, so it opens here and never completes, delivering alongside every slice.
- Level 3, slice enablers. Epics 19 to 21. Needs the platform baseline and the slice backlog. Epic 19 repeats per source rather than completing across all sources.
- Level 4, the slice bundle. Epics 22 to 25. Instantiated once per slice across three tracks, with Epics 26 and 27 joining conditionally. The first instance also proves the pattern.
- Level 5, cross-slice. Epics 26 and 27. Triggered from inside a slice, binding on every slice after it.
- Level 6, measurement. Epics 28 and 29. Needs accumulated usage and at least one live endpoint.
- Level 7, demand. Epics 30 and 31. Open on a recorded demand.

## Delivery risk

Several features this roadmap depends on are not generally available on Azure. Preview and Beta status is a delivery risk for the epic built on it, so the status is stated inline on the affected acceptance criterion. The list below is the risk register at 21 August 2026 and needs re-checking before each epic starts.

- The serverless allowlist migration is already overdue. Storage accounts that allowlist serverless compute by the old subnet IDs had to move to the Azure network security perimeter and the `AzureDatabricksServerless` service tag by 9 June 2026. That date has passed, so any legacy subnet allowlist still in the estate is non-compliant today. Epic 8 remediates it.
- Three system tables the observability work reads are Public Preview on Azure: `system.access.audit`, `system.query.history` and `system.lakeflow.pipelines`. Epics 8, 23, 28 and 29 all depend on them, so the cost mart and the adoption read sit on preview tables. `system.billing.usage`, `system.billing.list_prices`, `system.lakeflow.jobs` and most of `system.compute` are generally available.
- Serverless usage policies, the mechanism that attributes serverless spend to a tag, are Public Preview. Budgets themselves are generally available, so Epics 11, 17 and 28 depend on the preview half of the attribution chain.
- Anomaly detection, which covers freshness and completeness, is Public Preview on Azure, and some of its sub-features are Beta behind the admin previews page. Data profiling, formerly Lakehouse Monitoring, is generally available. Epic 16 splits its criteria along that line.
- GRANT policies inside Unity Catalog attribute based access control are Beta, although ABAC policies themselves reached general availability around 28 April 2026. Epic 27 uses ABAC and stays off GRANT policies.
- The Multi-Agent Supervisor API in Agent Bricks is Beta, and the Custom LLM and Information Extraction agents are marked legacy. Epic 31 excludes all three.
- On-behalf-of-user resource authorisation for Databricks Apps is Public Preview on Azure. Epic 30 states the fallback.
- Lakeflow Connect managed connectors sit in different release states, so the brand name says nothing about a given connector. Epic 14 requires the state of the specific connector to be confirmed before a date is committed to a source that needs it.
- Two deprecations are announced with no date attached. Secure cluster connectivity is to become mandatory for all classic workspaces, and creating a classic workspace on a Databricks-managed virtual network is to be deprecated in favour of VNet injection. Epics 1 and 5 build for the post-deprecation shape.
- `system.operational_data` and `system.lineage` are already deprecated and return no rows. Nothing in this roadmap reads them.

---

## Epic 1. Workspace type decision

Enabler, Infrastructure and platforming. No dependency. Gates Epics 5 to 9.

> Decide and record the workspace type as an architecture decision, so that the network, storage and connectivity work that follows has a fixed target instead of being reworked once the choice is made. The working assumption is a hybrid workspace, which keeps the classic compute plane and therefore keeps both serverless and provisioned compute available. The decision has not been taken yet, so this epic records it rather than ratifying it, and it comes first because it is the one choice that can close an option permanently.

Acceptance criteria:
- Both options are documented with what each implies downstream. A hybrid workspace, which the documentation also calls a classic workspace, keeps the classic compute plane, so it needs VNet injection, secure cluster connectivity and back-end Private Link, and it keeps the serverless path alongside them. A serverless workspace, generally available on Azure since March 2026, removes the classic compute plane and with it VNet injection.
- The decision spells out what it does to compute, which is the part you cannot undo. Hybrid keeps both serverless and provisioned compute available, so the per-workload choice stays open and gets made later at the provisioning gate in Epic 4. Serverless-only deletes provisioned compute as an option. Do not close that option as a side effect of a network preference.
- The decision spells out what it does to this roadmap. On hybrid, Epic 5 is built in full and Epic 8 adds the serverless path on top. On serverless-only, most of Epic 5 has nothing to attach to and the network work moves into Epic 8.
- Build for the two announced deprecations now: turn secure cluster connectivity on from the start, and use VNet injection instead of a Databricks-managed virtual network. Neither deprecation has a published date, so treat them as direction, not as a deadline to plan against.
- Premium is a given, not a choice. The decision notes what depends on it, namely Unity Catalog and predictive optimization.
- One type is chosen, with the reasoning and the rejected option recorded in an architecture decision, signed off by architecture and security before any infrastructure work starts.

## Epic 2. Use case selection and ordered slice backlog

Enabler, Deployment. No dependency. Gates Epic 21 and every slice.

> Run the upfront use case selection process and turn it into an ordered slice backlog with explicit selection and sequencing criteria, so that the delivery order is a business decision made once at the head of the plan rather than an accident of whichever source was easiest to ingest.

Acceptance criteria:
- The selection process is run with the business stakeholders and its output is a scored, ordered list of candidate use cases.
- The selection criteria and the sequencing criteria are written down and applied consistently, so the order can be defended and re-run when priorities change.
- Each backlog item names its owning business team, the report or application it replaces, and the source systems it needs.
- The first slice is identified, and its choice is justified against the criteria.
- The backlog is a living artefact with a stated re-ordering cadence and owner.

## Epic 3. Model inventory of the production reporting estate

Enabler, Platform engineering, upfront baseline. Depends on Epic 2 for priority order. Needs the Power BI capacity prerequisite that Epic 18 also confirms, met from the Power BI side alone. Feeds Epics 20 and 22.

> Catalogue the production star schemas behind the reporting estate that the platform will replace, covering facts, dimensions, grain, keys and measures, and establish the access route to the live semantic models, so that parity tests and `Gold` modelling are specified from what users actually read today instead of from a fresh interpretation of the requirement.

Acceptance criteria:
- Every production Power BI semantic model behind a backlog item from Epic 2 is catalogued with its fact tables, dimension tables, grain, keys and measure definitions. A use case added to the backlog later extends the inventory rather than reopening this epic.
- Measure definitions are captured as DAX expressions, not as descriptions, so a parity comparison can reproduce them.
- The access route to the live semantic models is established and tested, through the XMLA endpoint on the Power BI capacity, and the credential and permission it needs are recorded. Until the Key Vault-backed scope from Epic 7 exists, the credential is held under the interim custody route named in this epic, and moved to the scope when Epic 7 closes.
- Application reports that are not in a semantic model, for example the reports served from APP, Smart and EPM, are inventoried by the same template with their source of figures named.
- The inventory feeds an architecture decision on which models are reproduced, which are re-modelled and which are retired, and on whether the reproduced measures are declared as Unity Catalog metric views on `Gold` rather than re-implemented per report.

## Epic 4. Architecture decision log and standing decisions

Enabler, Platform engineering, standing. No dependency. Open for the whole programme.

> Establish the architecture decision log and the practice that keeps it current, so that every standing decision on the platform has one recorded home, one owner and a stated trigger, and no decision is taken twice or silently reversed.

Acceptance criteria:
- The decision log exists with a fixed template, a numbering scheme and a review route, and it is version controlled with the platform code.
- The alerting and freshness threshold decision is recorded, covering which tables are monitored, at what threshold, and where an alert lands, and which of the two data quality monitoring mechanisms carries it given that anomaly detection is Public Preview.
- Every provisioning request for compute beyond the serverless baseline is a decision in the log that quotes measured usage numbers, and is refused if it does not. The cost mart in Epic 28 is the source once it exists. Before then, the numbers come directly from `system.billing.usage` and `system.compute`, which populate from the first workload, and the decision names which source it quotes. This deliverable sits at a track junction and Platform engineering owns it.
- The residual-risk review from Epic 15 runs on every pipeline before promotion and its outcome is recorded per pipeline. The checklist is built once in Epic 15, the recurring review lives here, because the track definitions place it in the standing set.
- Each preview or Beta dependency in the delivery risk register above has a recorded decision stating whether the programme accepts it, with the fallback if the feature does not reach general availability in time.
- Each standing decision names the event that triggers it, so decisions land when the trigger fires and not on a review cycle.
- A superseded decision is marked as superseded with a pointer to the replacement, and it stays in the log.

## Epic 5. Network foundation

Enabler, Infrastructure and platforming. Depends on Epic 1. Shape set by the workspace type chosen there.

> Configure the network resources group and the workspace network, so that the workspace is deployed into a controlled network from the start and no workload ever runs on a default or public path.

Acceptance criteria:
- The network resources group is created with its address space planned against the workspace type chosen in Epic 1.
- For a hybrid workspace, the workspace virtual network is provisioned by VNet injection, with subnets, delegation and routing set for the classic compute plane. A Databricks-managed virtual network is not used, since its creation path is announced for deprecation.
- Secure cluster connectivity is enabled, so classic compute nodes carry no public IP address. This is built in rather than deferred, because it is announced to become mandatory for classic workspaces.
- Front-end Azure Private Link is configured for the workspace control plane and tested from an internal client. Back-end Private Link is configured where the workspace type has a classic compute plane, noting that it requires VNet injection and secure cluster connectivity.
- Under the hybrid workspace assumed in Epic 1, every criterion above applies and this epic is delivered in full. Epic 8 adds the serverless connectivity path alongside it rather than replacing any of it. If Epic 1 records a serverless workspace instead, the classic criteria above are marked not applicable and the network position moves into Epic 8.
- The configuration is expressed in Terraform through `hashicorp/azurerm` and the Databricks provider. No resource in this epic is created through the portal.

## Epic 6. Catalog and landing zone storage

Enabler, Infrastructure and platforming. Depends on Epic 1. Feeds Epic 10.

> Provision the storage that the catalog and the landing zone need, together with the managed identity and role assignments that let the catalog reach it, so that governed managed storage and an ingestion drop point both exist before any pipeline is written.

Acceptance criteria:
- ADLS Gen2 storage is provisioned for catalog managed storage and for the landing zone, with the container and path layout documented.
- An Access Connector for Azure Databricks is created and its Azure managed identity is granted the storage roles at the documented scope. A service principal is not used for this, because only a managed identity can reach an ADLS Gen2 account behind a storage firewall.
- Access is tested end to end from the workspace, both read and write, and the test is repeatable.
- The storage firewall allows only the platform paths. For a hybrid workspace the access connector is allowlisted as a firewall exception or reached through trusted-services access, and serverless SQL warehouses are allowlisted separately through the network security perimeter in Epic 8.
- A request from outside the approved paths is refused and the refusal is observed.
- Storage, access connector and role assignments are all Terraform managed, with no manually created role assignment left in place.

## Epic 7. Identity federation, groups and secrets

Enabler, Infrastructure and platforming. Depends on Epic 1. Feeds Epics 10 and 12.

> Federate identity from the corporate directory, define the account group model, and stand up service principal credentials and the secrets mechanism, so that every human and every automated actor on the platform is a governed identity and no credential is held in code or in a notebook.

Acceptance criteria:
- Automatic identity management is confirmed active, syncing users, groups and service principals from Microsoft Entra ID. SCIM provisioning is not configured, since automatic identity management supersedes it and is default-on for accounts created after 1 August 2025.
- The single-tenant assumption is verified. If any in-scope directory is a different Entra tenant, that case is recorded as an exception, because automatic identity management does not support cross-tenant directories and would need SCIM with Entra B2B instead.
- The account group model is defined and documented: which groups exist, what each one is for, and which are the grant targets that Epic 10 writes against.
- A group is assigned to the workspace, and workspace access is proven to follow group membership rather than individual assignment.
- Service principal credentials exist for CI/CD and for job execution. Azure DevOps pipelines authenticate through workload identity federation, so no client secret is stored for deployment.
- Secrets are held in Azure Key Vault-backed secret scopes, and a workload reads a secret through a scope with no credential present in source, in job configuration or in notebook state. The scope is configured against the Key Vault access policy model, since Azure RBAC is not supported for this path.
- Any dependency on the Identity Attribute Control List add-on, for syncing attributes such as title, department or cost centre, is recorded as Beta and given a fallback.

## Epic 8. Serverless connectivity, network security and platform monitoring

Enabler, Infrastructure and platforming. Depends on Epics 5 and 6. Its connectivity and egress criteria gate Epic 9. Its monitoring baseline gates the first slice, not the platform baseline.

> Configure the serverless connectivity path and the network security and monitoring around it, so that serverless compute reaches the catalog and the landing zone over private paths, egress is controlled, and the platform's own telemetry is readable from day one.

Acceptance criteria:
- A network connectivity configuration is created and attached to the workspace, with private endpoints from serverless compute to catalog storage and to the landing zone, proven by a serverless workload reading both.
- Egress from serverless compute is restricted through a network policy to the approved destinations, and a request to an unapproved destination is blocked and the block is observed.
- Every storage account the platform reads is allowlisted through the Azure network security perimeter using the `AzureDatabricksServerless` service tag. Any legacy allowlist by serverless subnet ID is found and removed, since that path was retired on 9 June 2026 and is already non-compliant.
- Network security controls cover both the classic and the serverless connectivity path, with the difference between them written down.
- Platform monitoring reads the system tables. Per schema, record whether it needs enabling, what its retention is, and which group holds the grant. Flag `system.access.audit`, `system.query.history` and `system.lakeflow.pipelines` as Public Preview, a risk every epic that reads them inherits.
- A monitoring baseline exists before the first pipeline, so the first slice does not run unobserved.

## Epic 9. Terraformed workspace with its test suite

Enabler, Infrastructure and platforming. Depends on Epics 5, 6, 7 and 8. Its deployed workspace gates Epics 10, 11, 12 and 18. Its test suite, remote state and rebuild proof gate the first slice, not the platform baseline, so Level 2 runs alongside them.

> Deliver the workspace as tested code with remote state and its own pipeline, plus a hand-written checklist for the settings that carry no usable API, so that the whole foundation is reproducible and a drift or a rebuild is handled by a pipeline run.

Acceptance criteria:
- The workspace and every resource from Epics 5 to 8 are generated from Terraform, held in version control, with `hashicorp/azurerm` provisioning the Azure resources and `databricks/databricks` managing what lives inside the workspace. Provider versions are pinned.
- Terraform state is remote, locked and access controlled, with the backend documented.
- The infrastructure code has its own pipeline, separate from the workload pipeline in Epic 12, with plan on pull request and apply gated on review.
- An automated test suite runs against the deployed workspace and asserts the security properties that matter: no public compute path, private storage access, group-driven workspace access, restricted egress.
- Settings that Terraform cannot manage safely are documented in a manual checklist with an owner and a verification step. `databricks_workspace_conf` covers only a limited set of workspace settings and cannot reliably revert them on destroy, so anything set through it is listed there as effectively one-way.
- A destroy and rebuild into a clean subscription is proven at least once. Every setting that blocks a clean rebuild is named individually in the manual checklist above with the manual step that restores it, so the rebuild either passes or produces a finite list of manual steps.

## Epic 10. Governance surface as code

Enabler, Platform engineering, upfront baseline. Depends on Epics 6, 7 and 9. Gates Epics 14 and 22.

> Author the governance surface as code, meaning the catalogs, schemas, volumes and grants, the tags policy, and the group model the grants are written against, so that every object the platform later creates lands inside a governed namespace with an owner and a tag, and no schema is ever created by hand.

Acceptance criteria:
- Catalogs, schemas and volumes are declared through `databricks_catalog`, `databricks_schema` and `databricks_volume` for the medallion layers and for the platform's own objects, with the naming standard documented.
- The landing zone is exposed as a Unity Catalog volume, with the storage credential and the external location declared here through `databricks_storage_credential` and `databricks_external_location`, referencing the access connector from Epic 6, rather than in the infrastructure code. This deliverable sits at a track junction and Platform engineering owns it.
- Grants are written through `databricks_grant` against the account groups from Epic 7, never against individual users, and least privilege is proven by a denied access attempt recorded in `system.access.audit`, noting that this table is Public Preview on Azure.
- Governed tags are defined and enforced through account-level tag policies, so an object or a workload that carries no owner and no use case tag cannot be created. The account limits of 1,000 governed tags and 500 allowed values per tag are checked against the planned taxonomy.
- Rule-based automatic tag assignment is not used, because it is Beta. Tag assignment is carried by the tag policies above and by the bundle definitions in Epic 12.
- For every object type, one owner is named: infrastructure code or governance code. Nothing is declared twice and nothing falls between the two.
- A single pipeline run recreates the whole governance surface in an empty catalog.

## Epic 11. Compute baseline and exception policy

Enabler, Platform engineering, upfront baseline. Depends on the deployed workspace from Epic 9, and on Epic 10 for the governed tags its policies enforce. Feeds Epics 4 and 17.

> Set the compute baseline, serverless by default, and the policies governing any exception to it, so that cost and configuration are controlled by default and any departure from serverless is a recorded decision.

Acceptance criteria:
- Serverless is the declared default for Lakeflow Jobs, Lakeflow pipelines, notebooks and SQL warehouses, and the baseline states which workload types it covers.
- Compute policies exist for the exception path and enforce the governed tags from Epic 10, so untagged classic compute cannot be launched.
- Serverless usage policies are configured to attribute serverless spend by tag. Their Public Preview status is recorded, together with the two known limits: they do not apply to classic or provisioned compute, and they do not backfill onto workloads that already exist.
- The route to request non-serverless compute is documented and runs through the provisioning gate in Epic 4. The gate requires measured usage numbers, and the baseline states where they come from before the cost mart exists, so a slice that hits a serverless limit early has a documented route rather than a dead end.
- The escalation path is tested once against real usage numbers, so the gate is proven to be passable and not merely declared.
- A test workload launched outside the baseline is refused, and the refusal is observable.

## Epic 12. Deployment and packaging standard

Enabler, Platform engineering, upfront baseline. Depends on Epics 7, 9 and 10. Gates Epic 15.

> Set the deployment and packaging standard for all data and AI workloads, with its environment targets and pinned tooling, and fix which catalog objects it owns against those the infrastructure code owns, so that every artefact after this point ships as a reviewable, repeatable release and the two tooling boundaries never collide.

Acceptance criteria:
- Declarative Automation Bundles define jobs, pipelines and notebooks as code, with the project layout and the naming standard documented. The name is used as the documentation now writes it, following the rename from Databricks Asset Bundles on 16 March 2026.
- The bundle deployment engine is chosen explicitly and recorded as a decision. New bundles default to the direct deployment engine, generally available since 10 June 2026 on CLI 1.3.0 and later, rather than the older Terraform-based engine. The decision says whether bundle deployment stays separate from the infrastructure Terraform in Epic 9. To move an existing bundle onto the new engine, run `databricks bundle migrate`.
- Environment targets exist for development, staging and production, deploying from the same bundle definitions with per-target configuration only.
- The Databricks CLI version and every tooling version are pinned, and the pipeline fails on an unpinned or drifted version rather than resolving to the latest.
- Deployment authenticates as a service principal through workload identity federation from Epic 7, with no stored client secret.
- The tooling boundary is fixed and documented: which catalog objects the infrastructure code owns, which the governance code in Epic 10 owns, and which the bundle owns. This deliverable sits at a track junction and Platform engineering owns it.
- A sample job deploys end to end through the pipeline into all three targets as proof.

## Epic 13. Development framework as runway

Enabler, Platform engineering, runway. Depends on Epic 12. Numbered here because that is all it needs to start, but it never completes: the first delivery lands with the first slice, and each extension lands with the slice that asks for it, so it runs alongside the slice bundle for the whole programme.

> Build the development framework, meaning the project tree, the templates and the harness, to what the next slices need, and extend it as the platform grows, so that no slice starts from nothing and no part of the framework is designed before there is a slice asking for it.

Acceptance criteria:
- The first delivery carries what the first slice needs to start and no more: the project tree and the templates that slice will actually use, aligned to the bundle layout from Epic 12.
- Each later extension names the slice that asked for it and what it adds, so the framework's growth is traceable to demand.
- Each extension is decided through an architecture decision in Epic 4, stating what moves into the framework and what deliberately stays per slice.
- The framework is delivered as a versioned artefact a slice can install.
- A slice migrated onto a new version still passes its parity tests, so an extension is proven to change structure and not results.
- The framework is never a precondition of a slice. A slice can be delivered while an extension it asked for has not landed yet.

## Epic 14. Ingestion standard for the landing zone

Enabler, Platform engineering, upfront baseline. Depends on Epics 10 and 12. Gates Epics 19 and 22.

> Set the ingestion standard for reading the landing zone and rule where a managed source connector applies instead, so that every source is ingested the same way, and the choice between reading a drop point and using a connector is made once as a standard rather than per source by whoever writes the pipeline.

Acceptance criteria:
- The default ingestion pattern is Auto Loader reading the Unity Catalog volume from Epic 10, with the standard specifying incremental file discovery, checkpoint location, schema inference and evolution mode, and retention of the `_rescued_data` column.
- The standard says when to use a Lakeflow Connect managed connector instead of reading the landing zone. Connectors sit in different release states, so check the status of the specific connector before committing a date to any source that depends on it.
- Idempotency and reprocessing behaviour are specified, so a re-run after a failure produces no duplicates in `Bronze`.
- The standard states what `Bronze` records and what it never does, in particular that it is append-only and applies no business logic.
- Pipeline code targets the current declarative pipelines API, `from pyspark import pipelines as dp`, rather than the legacy `import dlt`, and the standard notes that classic billing records may still carry a Delta Live Tables prefix after the rename to Lakeflow pipelines.
- A reference implementation exists against a sample drop and is the template the first slice starts from.

## Epic 15. CI quality gates and residual-risk review

Enabler, Platform engineering, upfront baseline. Depends on Epic 12. Gates Epic 22.

> Establish the automated quality gates every change passes at CI, together with the residual-risk review that covers what automation cannot check, so that no pipeline reaches production without tested transformation code, a validated deployment and a reviewed list of residual risks.

Acceptance criteria:
- Unit tests on transformation code run on every merge request and block the merge on failure.
- `databricks bundle validate` and a deploy to the development target run on every merge request.
- A smoke run against sample data executes the deployed artefact and asserts its output, so a deployable but broken pipeline is caught before promotion.
- The promotion rule from development to staging to production is enforced by the pipeline itself, so a promotion that skips a stage fails.
- The parity comparator's own tests run on every merge, so the tool that proves parity is itself tested. This deliverable sits at a track junction and Platform engineering owns it.
- The residual-risk review checklist exists as a versioned artefact and is exercised once against the first pipeline that reaches promotion. Running it on every later pipeline is a standing obligation carried by Epic 4, so this epic can close while the review continues. This deliverable sits at a track junction and Platform engineering owns it.

## Epic 16. Data quality standard

Enabler, Platform engineering, upfront baseline. Depends on Epics 10 and 14. Gates Epic 22.

> Set the data quality standard, meaning expectation naming and severity, the quarantine pattern to implement, and freshness and drift monitoring on critical tables, so that every slice enforces quality the same way and a quality failure is visible and actionable instead of silent.

Acceptance criteria:
- Expectation naming and severity are defined against the three Lakeflow pipelines expectation actions, and the behaviour of each is stated: warn keeps the row and records the violation, drop removes the row, fail stops the update.
- The quarantine pattern is specified and implemented as a reusable component. It is a recipe over expectations rather than a product feature, so the standard states where rejected records land, what metadata travels with them, and who is accountable for clearing the queue.
- Drift and distribution monitoring on critical tables uses data profiling, the generally available capability formerly called Lakehouse Monitoring.
- Freshness and completeness monitoring uses anomaly detection, and its Public Preview status on Azure is recorded, with the fallback stated: a freshness assertion in the pipeline itself if the preview cannot be relied on. Thresholds and alert routing come from the standing decision in Epic 4.
- Validation metrics are emitted per run and are queryable, so quality over time is a measurable trend and not a per-run log line.
- The standard states which checks are mandatory in every slice and which are optional, so a slice cannot quietly ship with no expectations at all.

## Epic 17. Cost and usage model

Enabler, Platform engineering, upfront baseline. Depends on Epics 2, 10 and 11. Feeds Epic 28.

> Define the cost and usage model and its attribution chain from tag to use case, so that platform spend can be attributed to an owning use case and team, with the limits of the platform's own reported figures stated up front.

Acceptance criteria:
- The attribution chain is defined end to end: from the governed tags enforced in Epic 10 and the serverless usage policies in Epic 11, through `system.billing.usage`, to the use case and the owning team.
- The mapping from tag values to use cases and teams is a maintained artefact with an owner, not a query written once.
- Budgets are configured in the account console with alerts at agreed thresholds. Budgets are generally available, while the tag-based attribution that makes them useful for chargeback rests on serverless usage policies, which are Public Preview, and that split is recorded.
- The workload types where identity or tag attribution does not populate are listed, and their usage is classified as unattributable rather than forced onto an owner.
- The model records that platform-reported cost is a list-price estimate computed from `system.billing.usage` joined to `system.billing.list_prices`, and names the Azure invoice as the authoritative billed figure.
- The model is proven against a test workload whose usage is traced from `system.billing.usage` back to a named use case.

## Epic 18. Reporting connectivity

Enabler, Platform engineering, upfront baseline. Depends on Epics 9 and 10. Gates Epics 20 and 23.

> Deliver the connectivity the reporting estate needs to read the platform, meaning the serverless warehouse for BI, the connection and single sign-on configuration, and the capacity prerequisite, so that every endpoint the Usage layer builds or repoints has one supported route in and users keep their own identity through it.

Acceptance criteria:
- A serverless SQL warehouse is provisioned for BI workloads, sized against the baseline in Epic 11 and tagged per Epic 10, and allowlisted through the network security perimeter per Epic 8.
- Publishing to the Power BI service from Azure Databricks is the one supported route, configured and documented as such, so no team builds a second one.
- Single sign-on is configured through Microsoft Entra ID DirectQuery, so a report reads with the end user's identity and Unity Catalog grants apply to them rather than to a shared service account.
- The capacity prerequisite is confirmed with the owning team and recorded as a dependency with a named owner: a Power BI Premium, Premium Per User or Fabric capacity, with the XMLA endpoint set to read write. Data must be in Unity Catalog, since the Hive metastore is not supported on this path.
- The newer federated single sign-on path through the ADBC driver is explicitly out of scope, because it is Public Preview and documented for AWS only, with no Azure guidance.
- A production report reads a `Gold` table through the full path as proof, and an unauthorised user is refused on the same path.
- This deliverable sits at a track junction and Platform engineering owns it, consumed by every endpoint the Usage layer builds or repoints.

## Epic 19. Landing zone contracts per source

Enabler, Data engineering. Depends on Epics 2 and 14. Repeats per source, ahead of the first slice that reads that source.

> Agree the landing zone contract for each source in the backlog, covering arrival, ordering and duplicate handling, so that ingestion is written against a stated guarantee rather than against observed behaviour that changes without notice.

Acceptance criteria:
- Each source has a written contract naming the producing team and its owner. The unit of completion is one source, so this epic closes per source and never requires the whole estate to be contracted before the first slice starts.
- The contract states arrival: the volume path and file naming convention, the expected cadence, the format and encoding, and what a late or missing drop means.
- The contract states ordering and duplicate handling: whether order is guaranteed, whether a file can be re-dropped, and what the consumer must do when it is.
- The contract states the schema and the change process, so a producer-side change is announced rather than discovered by a failing run or absorbed silently into `_rescued_data`.
- A contract breach is detectable by the pipeline and raises an alert naming the producer, not the platform.
- Contracts are agreed in backlog order, and the readiness gate in Epic 21 checks only the contracts for the sources the slice actually reads, so no slice waits on a contract it does not need.

## Epic 20. Parity comparator and tolerance model

Enabler, Data engineering. Depends on Epics 3, 15 and 18. Gates every slice roll out. Accepted against the first slice's development target, so it does not wait on production `Gold`.

> Build the parity comparator and the tolerance model it applies, so that every slice reproducing a figure users read today can prove it does, at report grain and filter context, with a pass or fail per run instead of an opinion.

Acceptance criteria:
- The comparator reads the reference figure from the live source users read today, a Power BI semantic model through the XMLA endpoint or an application report from APP, Smart or EPM, and the platform figure from `Gold`, and compares them at report grain and filter context.
- Acceptance runs against the first slice's `Gold` tables in the development target, so no production data is required to close this epic. Per-run evidence in production begins with the first slice.
- A tolerance is defined per measure type, with the reasoning recorded: exact for counts and keys, stated bounds for sums, currency and derived ratios.
- Filter context is part of the comparison, so a measure that matches in total but diverges by dimension slice fails rather than passes.
- Each run produces pass or fail evidence per measure, retained and attributable to a code version and a data state.
- The comparator is packaged as a reusable component with its own unit tests, which run at CI per Epic 15.
- The reference access route from Epic 3 is used, and its credential is held in the Key Vault-backed secret scope from Epic 7.

## Epic 21. Slice definition of done and readiness gate

Enabler, Deployment. Depends on Epics 2, 16, 19 and 20. Gates every slice.

> Define the slice definition of done and the readiness gate each slice passes before it starts, so that a slice is only opened when its preconditions are met and only closed when it has proven data, a consumer and an adoption route.

Acceptance criteria:
- The definition of done lists every condition a slice must meet to close, covering data, quality evidence, parity evidence, a live endpoint, an enabled business team and a retired predecessor.
- The readiness gate lists every condition a slice must meet to start, covering an agreed landing zone contract, a named business owner, an identified reference figure and available source access.
- The gate has a named owner who can refuse to open a slice, and a refusal is recorded with its reason.
- Both artefacts are applied to the first slice's gate, which is what closes this epic. Revising them after the first slice runs is a standing decision in Epic 4, not a condition of this epic, so the second slice is never blocked waiting for the first to close.
- The definition of done is the same for every slice, and any exception is an architecture decision in Epic 4 rather than a local negotiation.

---

## The slice bundle, Epics 22 to 25

Epics 22 to 25 are the recurring unit of delivery. One instance of all four is what a slice means. They sit in three tracks, Data engineering, the Usage layer and Deployment, which owns two of the four. Epics 26 and 27 join a slice conditionally, when it is the first to need a shared dimension or to carry restricted data. A slice is one report's data driven from `Bronze` through `Silver` to `Gold`, its endpoint, its invited business team and its roll out.

They are written once here and instantiated once per slice, in the order set by the backlog in Epic 2. The first instance carries extra weight because it proves the pattern, and the review after it feeds Epic 4 and Epic 13.

Slices overlap, with one exception. A later slice starts as soon as it passes the readiness gate, without waiting for its predecessor to close. The exception is a shared dimension: once Epic 26 registers one, extending it re-runs every prior slice's parity tests, so two slices that share a dimension serialise on that extension. It is stated here because it constrains scheduling from the second slice onward.

## Epic 22. Slice data delivery, Bronze to Gold

Business, Data engineering. Depends on Epics 10, 14, 15, 16, 20 and 21, and on the Epic 19 contract for each source it reads. From the second slice onward it is also bound by the register in Epic 26. Repeats per slice.

> Deliver one report's data end to end, from ingestion into `Bronze`, through cleansing and historisation in `Silver`, to the aggregated and enriched tables in `Gold`, orchestrated, quality-checked and proven at parity, so that a real consumer reads trusted data and quality is proven on real data under real consumption rather than on a layer completed in isolation.

Acceptance criteria:
- `Bronze` ingests from the landing zone volume with Auto Loader per the standard in Epic 14, append-only, with schema evolution handled and `_rescued_data` retained and queryable.
- `Silver` cleanses and standardises, and holds the history of changing records with the historisation approach stated per entity.
- `Gold` aggregates, refines and enriches into the slice's target tables, modelled against the inventory from Epic 3. Whether reproduced measures are declared as Unity Catalog metric views over `Gold` or implemented in the target tables follows the decision taken in Epic 3, and the slice does not settle it locally.
- All tables are Unity Catalog managed tables with liquid clustering, using `CLUSTER BY AUTO` unless a measured reason to pin the keys is recorded. No maintenance job is scheduled, because predictive optimization is default-on for accounts created on or after 11 November 2024 and runs `OPTIMIZE`, `VACUUM` and `ANALYZE` on managed tables.
- Expectations from Epic 16 are applied at every layer, and validation metrics per run are emitted and queryable.
- A Lakeflow Job orchestrates the slice end to end, with its schedule, retries, notification routing and a stated freshness target.
- The backfill and full-refresh procedure is documented and executed at least once, and its exit condition is a parity re-run that passes.
- The parity tests for this report run inside the pipeline and pass within tolerance. A fix and re-run does not invalidate the evidence, because evidence is attributed to a code version and a data state. This deliverable sits at a track junction and Data engineering owns it.
- Every table, job and pipeline carries the governed tags from Epic 10, so the slice appears in cost attribution from its first run.

## Epic 23. Slice endpoint

Business, Usage layer. Depends on Epics 18 and 22. Repeats per slice.

> Build one endpoint per slice, dashboard first, with its consumer group grants and its registered usage telemetry, so that a consumer exists at the end of every slice, feedback starts early, and adoption becomes measurable from the first day the endpoint is live.

Acceptance criteria:
- One endpoint exists for the slice, built as an AI/BI Dashboard unless an architecture decision in Epic 4 says otherwise. A Genie Agent is added on the same `Gold` schema only where natural-language follow-up is asked for, using the current name after the rename from Genie Spaces in July 2026.
- The endpoint reads `Gold` through the serverless SQL warehouse from Epic 18, not through a private path of its own.
- The slice's consumer group exists and holds grants on the slice's `Gold` schema only, and a user outside the group is refused.
- The endpoint's usage telemetry source is registered and Deployment holds the grant to read it, so the cost mart can model it when Epic 28 is built. This epic does not wait on the mart. This deliverable sits at a track junction and the Usage layer owns it.
- The telemetry sources are named: dashboard views from `system.access.audit`, query activity from `system.query.history` on its `dashboard_id` column, and Genie activity from `service_name = 'aibiGenie'`. Both tables are Public Preview on Azure, and the usage-monitoring guidance carries a preview banner too, so the endpoint ships with that risk on the record.
- The endpoint reproduces the figures of the report it replaces, cross-checked against the parity evidence from Epic 22 rather than assumed from it.
- Exactly one endpoint is delivered for the slice. A second endpoint on the same `Gold` schema is a separate demand and belongs to Epic 30 or Epic 31.

## Epic 24. Slice invitation and enablement

Business, Deployment. Depends on Epics 21 and 23. Repeats per slice.

> Invite the owning business team to the slice's endpoint, run its enablement and open the access route, then monitor usage and capture feedback, so that adoption is invited rather than imposed and the next iteration is driven by what the team actually does with it.

Acceptance criteria:
- The owning business team is invited, with the invitation naming what changes for them and what does not.
- An enablement session is run with the team, and what was covered and who attended is recorded.
- The access request route is documented and open, and a request from a team member is served through it end to end, ending in an account group membership rather than a direct grant.
- Usage is monitored from the endpoint's telemetry after go-live, over a stated observation window.
- Feedback is captured in a form that can be triaged into the backlog, and the triage outcome is visible to the team that raised it.
- Feedback from the observation window is triaged, and each item is either delivered or scheduled with a date. The owning business team signs that the endpoint is fit to roll out, which is the stopping rule for iteration and the condition Epic 25 reads.

## Epic 25. Slice roll out and predecessor retirement

Business, Deployment. Depends on Epics 22, 23 and 24. Repeats per slice.

> Roll out the use case and retire the report it replaces together with its refresh path, so that the platform becomes the single source for that figure and the programme stops paying to run two versions of the same truth.

Acceptance criteria:
- Roll out is declared only when the slice meets the definition of done from Epic 21 in full.
- The superseded report is retired, with the retirement communicated to its known consumers ahead of the date.
- The refresh path feeding the superseded report is decommissioned, including its schedule, its gateway where it has one, and its credential, so no orphaned job keeps running and no stale dataset keeps refreshing.
- Any consumer of the superseded report that was not in the invited team is identified before retirement and routed to the new endpoint.

## Epic 26. Conformed dimension register

Enabler, Data engineering. Depends on Epic 22, opened by the first slice that needs a shared dimension. Binding on every later slice.

> Register the conformed dimensions and their surrogate key strategy, built inside the slice that first needs a shared dimension, so that dimensions are reused across slices instead of re-derived per slice, and a change to a shared dimension has a known and enforced cost.

Acceptance criteria:
- The register exists and records, per conformed dimension, its grain, its business key, its surrogate key strategy and its owning slice.
- The surrogate key strategy is stated once and applied consistently, including how late-arriving and unknown members are handled.
- A second slice reuses a registered dimension rather than building its own, and the reuse is visible in Unity Catalog lineage.
- The rule that extending a shared dimension re-runs every prior slice's parity tests is written into the register and enforced by the pipeline.
- A dimension extension is exercised at least once, with the prior slices' parity re-run passing before the change is promoted.
- This deliverable sits at a track junction and Data engineering owns it.

## Epic 27. Data protection policies

Enabler, Platform engineering, standing. Depends on Epics 10 and 20, triggered by the first slice with restricted data. Reopens for every later slice that brings a new restricted data class.

> Set the data protection standard and implement the row filtering and column masking it calls for, so that sensitive data is restricted at the governance layer rather than by building a separate restricted copy of a table per audience.

Acceptance criteria:
- The standard states what classes of data are restricted, and which control applies to each: row filtering, column masking, or exclusion from `Gold` altogether.
- Rules that must hold across many tables are implemented as Unity Catalog attribute based access control policies, keyed off the governed tags from Epic 10, which is what the documentation now recommends over per-table controls. Table-level row filters and column masks are used where a rule genuinely applies to one table.
- GRANT policies inside ABAC are not used, since they are Beta. If a requirement can only be met that way, it becomes a decision in Epic 4 with its risk stated.
- Policies apply through the account groups from Epic 7, never to individual users.
- A restricted read is proven: a member of an unprivileged group sees filtered rows or masked values, and a member of a privileged group sees the full value.
- Policies are declared as code alongside the governance surface in Epic 10, so they redeploy with it.
- The standard states the interaction between protection policies and the parity tests, so a masked column does not silently fail a parity comparison. The comparator from Epic 20 runs under an identity that can see the unmasked value, and any measure that cannot be compared that way is excluded from parity with the reason recorded per measure.
- The epic stays open. Each later slice that brings a new restricted data class classifies it, attaches its policy and records the decision, so nothing arriving at slice seven is left without a home.

## Epic 28. Cost mart

Business, Data engineering. Depends on Epics 17, 22 and 23, and on accumulated usage data.

> Build the cost mart over the platform's own usage data, joined to the use case and team mapping, so that spend, query activity and endpoint adoption are all readable from one modelled place and every provisioning decision can quote a measured number.

Acceptance criteria:
- The mart models `system.billing.usage` and `system.billing.list_prices`, both generally available, joined to the use case and team mapping from Epic 17.
- Job and pipeline activity comes from `system.lakeflow`, and compute activity from `system.compute`. The mart records which of these schemas are generally available and which are Public Preview, since `system.lakeflow.pipelines` and parts of `system.compute` are preview on Azure.
- Query activity comes from `system.query.history` and endpoint activity from `system.access.audit`, both Public Preview. The mart states the consequence: a schema change or a preview gap breaks a view rather than silently returning fewer rows, and the views are written to fail loudly.
- Endpoint usage telemetry from Epic 23 is modelled into the mart, so adoption and cost sit in the same model.
- Cost is readable by use case, by team and by workload type, and a given cost line can be traced back to a named job, pipeline, warehouse or endpoint.
- Usage that cannot be attributed is reported as unattributed, with its share visible, rather than distributed across owners. Classic compute is expected here, since serverless usage policies do not cover it.
- The list-price caveat from Epic 17 is surfaced in the mart itself, so a reader cannot mistake an estimate for a billed figure.
- `system.operational_data` and `system.lineage` are not read, since both are deprecated and return no rows.
- The mart is the source Epic 4 provisioning decisions and Epic 29 adoption reads both quote. It is built with the same quality discipline as a slice, but it is not one: it replaces no report, has no reference figure to compare against and no business team to invite, so the slice definition of done does not apply to it.
- This deliverable sits at a track junction and Data engineering owns it.

## Epic 29. Adoption measurement

Business, Deployment. Depends on Epics 23 and 28.

> Define the per-team adoption metrics and read them periodically from the cost mart, so that adoption is measured per team and a stalling use case is visible early enough to act on.

Acceptance criteria:
- Adoption metrics are defined per team, with each metric stating its numerator, its denominator and its observation window.
- The metric definitions state what counts as active use, so a scheduled refresh is not mistaken for a user reading a report. Human activity is separated from service principal activity in the source data.
- The periodic read runs on a stated cadence against the cost mart, and its output goes to the track leaders and the business owners.
- A metric that falls below a stated threshold triggers a conversation with the owning team, and the trigger and route are documented.
- Any endpoint with no telemetry is reported as unmeasurable rather than as unused, and the preview status of the underlying audit and query history tables is carried into how confidently the numbers are presented.

## Epic 30. Custom applications on Gold

Business, Usage layer. Depends on Epics 18 and 22, opened on first demand.

> Build custom applications consuming the `Gold` layer where a dashboard cannot serve the need, so that use cases requiring interaction or write-back have a route, without the track building application infrastructure ahead of a real request.

Acceptance criteria:
- A recorded demand exists and says why an AI/BI Dashboard cannot serve it.
- The application is built as a Databricks App, which runs as a containerised service on serverless compute, and consumes its SQL warehouse, job, Genie Agent, secret, volume and Unity Catalog table resources through the app's declared resources rather than through ad hoc connections.
- Identity handling is decided explicitly. On-behalf-of-user resource authorisation is Public Preview on Azure, so if the application must read as the end user, the preview dependency is recorded in Epic 4, and the fallback is a service principal identity with the narrower grants that implies.
- The application ships through the packaging standard from Epic 12, with the same CI gates from Epic 15.
- Its usage telemetry is registered and feeds the cost mart on the same basis as Epic 23.
- The application is delivered only against the recorded demand above, and its scope is bounded by what that demand states.

## Epic 31. Agent and workflow endpoints

Business, Usage layer. Depends on Epics 22, 27 and 28, opened on first demand.

> Deliver agent and workflow endpoints over the `Gold` layer once a demand arrives, with the stack settled by an architecture decision triggered by that first demand, so that the platform meets agentic and workflow use cases without committing to a stack before there is a use case to judge it against.

Acceptance criteria:
- The first demand is recorded with its use case, its user group and the figures or actions it needs.
- An architecture decision in Epic 4 settles the stack, comparing the low-code Agent Bricks route against code-first custom agent authoring on MLflow 3. The decision uses current naming, since the Mosaic AI Agent Framework branding is retired and workflow orchestration is now Lakeflow Jobs.
- Three options are out of scope unless the decision explicitly accepts their status: the Agent Bricks Multi-Agent Supervisor API, which is Beta, and the Custom LLM and Information Extraction agents, which are marked legacy. The Knowledge Assistant is generally available on Azure and is the default starting point, subject to a region check for the workspace region.
- The endpoint reads `Gold` through governed access under the requesting user's identity where the stack supports it, and protection policies from Epic 27 apply.
- Agent and service principal activity is distinguishable from human activity in the cost mart, so agent cost and agent adoption are separately readable.
- Its usage telemetry is registered and feeds the cost mart on the same basis as Epic 23.
- The endpoint is delivered only against the recorded demand above, and its scope is bounded by what that demand states.

---

## Open question for the track leaders

One tension in this roadmap is not resolved, and it should be settled before the plan is committed.

The track definitions apply the runway principle to the development framework: build what the plane needs to take off, then extend the runway as the plane grows. Epic 13 follows it.

The same principle would apply to four other deliverables that this roadmap schedules as upfront baseline: the ingestion standard, the data quality standard with its quarantine pattern, the parity tolerance model, and the slice definition of done. Each is a repeated pattern written before a single slice has run, and each is a hard precondition of Epic 22. Twenty epics stand between the head of the plan and the first row of real data, in a programme whose premise is that quality proves itself only on real data under real consumption.

The track definitions tag those four as upfront baseline, so this roadmap keeps them there rather than overruling the source. The question for the track leaders is whether the runway tag fits them better. Four of the upfront set have a safety argument for landing in full before the first slice: governance, identity, the deployment boundary and the CI gates, because data should not land in an ungoverned namespace and code should not ship unreviewed. Runway logic does not soften that argument. The other four are patterns a slice would teach us. Answering this changes the shape of Level 2 and the date of the first slice, so it is worth deciding deliberately rather than by default.

## What this roadmap deliberately does not schedule

- Provisioned compute for scale. It exists only after an architecture decision in Epic 4 that quotes measured usage numbers from the cost mart, so no epic assumes it.
- Table maintenance. Predictive optimization is default-on for this account and runs `OPTIMIZE`, `VACUUM` and `ANALYZE` on Unity Catalog managed tables, so no epic schedules a maintenance job.
- SCIM provisioning. Automatic identity management supersedes it and is default-on, so it is configured only if a cross-tenant directory turns up in Epic 7.
- The development framework designed in full upfront. Epic 13 builds it as runway, to what the next slices need, extending as they need more.
- Usage layer capability ahead of demand. Epics 30 and 31 open on a recorded demand, and Epic 23 delivers exactly one endpoint per slice.
- A second endpoint on a slice's `Gold` schema. That is a new demand and belongs to Epic 30 or Epic 31, not to the slice that created the schema.
- Features whose only documented path is Public Preview or Beta and for which a generally available alternative exists. Named per epic, with the ADBC federated single sign-on path in Epic 18 and ABAC GRANT policies in Epic 27 as the two clearest cases.
## Coverage map

Every deliverable in `track-definitions.md` and the epic that carries it.

| Track | Deliverable | Epic |
| :---- | :---------- | :--- |
| Infrastructure and platforming | Workspace type decision | 1 |
| Infrastructure and platforming | Network resources group and workspace network | 5 |
| Infrastructure and platforming | Catalog and landing zone storage, access identity, role assignments | 6 |
| Infrastructure and platforming | Identity federation, account group model, service principal credentials, secrets | 7 |
| Infrastructure and platforming | Serverless connectivity with private paths | 8 |
| Infrastructure and platforming | Network security and monitoring, telemetry from system tables | 8 |
| Infrastructure and platforming | Terraformed workspace, test suite, remote state, pipeline, manual checklist | 9 |
| Platform engineering | Catalog as code, tags policy, group model grants | 10 |
| Platform engineering | Compute baseline and exception policies | 11 |
| Platform engineering | Deployment and packaging standard, environment targets, pinned tooling | 12 |
| Platform engineering | Ingestion standard for the landing zone | 14 |
| Platform engineering | CI quality gates and promotion rule | 15 |
| Platform engineering | Residual-risk review checklist, built once | 15 |
| Platform engineering | Residual-risk review, run per pipeline | 4 |
| Platform engineering | Data quality standard | 16 |
| Platform engineering | Cost and usage model and attribution chain | 17 |
| Platform engineering | Reporting connectivity | 18 |
| Platform engineering | Model inventory | 3 |
| Platform engineering | Architecture decision log, alerting and freshness, provisioning gates | 4 |
| Platform engineering | Data protection policies for row filtering and masking | 27 |
| Platform engineering | Development framework, built as runway | 13 |
| Data engineering | Landing zone contract per source | 19 |
| Data engineering | Per slice `Bronze`, `Silver`, `Gold` tables | 22 |
| Data engineering | Per slice orchestrating job | 22 |
| Data engineering | Per slice backfill and full-refresh procedure | 22 |
| Data engineering | Parity tests, comparator and tolerance model | 20 |
| Data engineering | Parity tests, per report run and evidence | 22 |
| Data engineering | Conformed dimension register | 26 |
| Data engineering | Cost mart | 28 |
| Usage layer | One endpoint per slice | 23 |
| Usage layer | Consumer group and its grants on the slice `Gold` schema | 23 |
| Usage layer | Registered usage telemetry source per endpoint | 23 |
| Usage layer | Custom applications consuming `Gold` | 30 |
| Usage layer | Agent and workflow endpoints | 31 |
| Deployment | Ordered slice backlog with selection and sequencing criteria | 2 |
| Deployment | Per-slice readiness gate | 21 |
| Deployment | Slice definition of done | 21 |
| Deployment | Per slice invitation, enablement session, access request route | 24 |
| Deployment | Per-team adoption metric definitions and periodic read | 29 |
| Deployment | Per slice retirement of the superseded report and its refresh path | 25 |
| Deployment | Roll out of each use case | 25 |

## Junction deliverables

The eleven deliverables that sit where tracks meet, with the epic that carries them. Owners are taken from the junction table in `track-definitions.md` and are not reassigned here.

| Deliverable | Epic | Owner |
| :---------- | :--- | :---- |
| Landing zone volume | 10 | Platform engineering |
| Model inventory | 3 | Platform engineering |
| Reporting connectivity | 18 | Platform engineering |
| Parity tests per report | 22 | Data engineering |
| Parity tests CI gate | 15 | Platform engineering |
| Conformed dimension register | 26 | Data engineering |
| Cost mart | 28 | Data engineering |
| Endpoint usage telemetry | 23 | Usage layer |
| Residual-risk review checklist | 15, standing review in 4 | Platform engineering |
| Deployment tooling boundary | 12 | Platform engineering |
| Provisioning gate | 4 | Platform engineering |

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
Version: 1.2 | Last Updated: 2026-08-21 | Status: Draft
-->
