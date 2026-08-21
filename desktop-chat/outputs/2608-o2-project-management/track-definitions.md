# Track definitions for the greenfield medallion data platform

Reference for the five tracks of the greenfield data platform, built on a 2026 Databricks workspace with a medallion architecture (`Bronze`, `Silver`, `Gold`). This document is the input for drafting the epic roadmap. Each track below opens with what it covers and why its work is scheduled the way it is, then lists its activities and its deliverables. Those two lists carry the detailed scope, at the granularity epics and their acceptance criteria are drafted from.

## What a track is

A track is a subarea of the project organisation covering one kind of expertise. Each track has one owner, the track leader. Every activity and every deliverable on the project belongs to exactly one track. Tracks run in parallel, with identified dependencies between their activities and deliverables.

A track is not a phase. Tracks never induce work order. The schedule plan is built from deliverable dependency chains, and on that plan tracks appear as swimlanes or as an ownership attribute, never as columns of time. When two tracks meet on one deliverable, the deliverable still gets exactly one owner. The junction table at the end records those assignments.

## Infrastructure & platforming

How a secure foundation is built, from network configuration and access management to a terraformed, tested workspace.

Every later artefact is written into the workspace this track delivers. Its work is finite and front-loaded, not demand-ordered.

### ⚙️ Activities

- Decide the workspace type and record it as an architecture decision, since it scopes the network and storage work that follows.
- Configure the network resources group and the workspace network.
- Provision the catalog and landing zone storage, with the managed identity and role assignments the catalog needs to reach it.
- Set up identity federation from the corporate directory, service principal credentials and the secrets mechanism.
- Set up network security and monitoring, covering both the classic and the serverless connectivity path.
- Terraform, generate and test the workspace as code, and document by hand the settings that carry no API.
- The whole block is front-loaded and finite, not demand-ordered.
- Provisioning compute for scale is not in this track. Provisioned compute exists only after an architecture decision quoting measured usage numbers.

### 📦 Deliverables

- The workspace type decision.
- The secure, terraformed workspace with its test suite, remote state and its own pipeline, plus the manual checklist for settings with no API.
- Network resources group and workspace network configuration.
- Serverless connectivity configuration with private paths to the catalog and landing zone storage.
- Catalog and landing zone storage, with the access identity and its role assignments.
- Identity federation, the account group model, service principal credentials and the secrets mechanism.
- Network security and monitoring setup, telemetry read from the platform's own system tables.

## Platform engineering

All platform components enabling use case implementation: Unity Catalog, connectors, CI-CD, cost and usage model, observability model, tags policy, architecture decisions, development framework.

Its deliverables follow three different scheduling logics, so each carries a cadence tag: upfront baseline, standing decision work, or runway.

Runway is the architectural runway, and it is governed by one principle. We build what the plane needs to take off, and no more. The runway then extends as the plane grows, so it is never finished and never built out ahead of the aircraft that will use it. A runway deliverable is therefore neither designed in full upfront nor withheld until repetition has piled up. It is built to what the next slices need, and extended when they need more.

### ⚙️ Activities

- Author the governance surface and platform services as code.
- Set the compute baseline and the policies governing any exception to it.
- Set the ingestion standard for reading the landing zone, and rule where a managed source connector applies instead.
- Set the deployment and packaging standard, and fix which catalog objects it owns and which the infrastructure code owns.
- Set the data quality standard and the data protection standard.
- Deliver the connectivity the reporting estate needs to read the platform.
- Catalogue the production star schemas before the first slice, including the access route to the live semantic models.
- Rule and record architecture decisions, among them alerting and freshness thresholds, provisioning requests, the protection policies and each extension of the development framework.
- Run the automated pipeline checks at CI and review the residual risks by checklist.
- Build the development framework as runway. Deliver the part the next slices need, then extend it as the platform grows and the slices show what they repeat.

### 📦 Deliverables

- Upfront baseline: the catalog as code with catalogs, schemas, volumes and grants, tags policy, and the group model grants are written against.
- Upfront baseline: the compute baseline, serverless by default, with policies for the exception path.
- Upfront baseline: the ingestion standard for the landing zone, and the deployment and packaging standard with its environment targets and pinned tooling.
- Upfront baseline: CI quality gates, meaning unit tests on transformation code, a validate and dev-target deploy, a sample-data smoke run and the promotion rule.
- Upfront baseline: the data quality standard, meaning expectation naming and severity, the quarantine pattern to implement, and freshness and drift monitoring on critical tables.
- Upfront baseline: the cost and usage model, its attribution chain from tags to use case, and the caveat that platform-reported figures are list-price estimates.
- Upfront baseline: reporting connectivity, meaning the serverless warehouse for BI, the connection and single sign-on configuration, and the capacity prerequisite.
- Upfront baseline: the model inventory, a catalogue of the production star schemas covering facts, dimensions, grain, keys and measures, with its access route to the live semantic models.
- Standing: the architecture decision log, the alerting and freshness decision, the provisioning gate decisions quoting measured usage numbers, the data protection policies for row filtering and masking, and the residual-risk review checklist.
- Runway: the development framework (project tree, templates, harness), built to what the next slices need rather than designed in full upfront, extended as the platform grows, with each extension decided through an architecture decision.

## Data engineering

Data transformation from ingestion to trusted, business-ready state. `Bronze`: sources ingestion, schema handling, validation, historization. `Silver`: data cleansing, standardization. `Gold`: aggregation, refinement, enrichment.

Data quality proves itself only on real data under real consumption, so the track delivers vertical slices that each end at a consumer, instead of completing one layer across all sources.

### ⚙️ Activities

- Deliver slices. The schedule unit is one report's data driven from `Bronze` through `Silver` to `Gold`.
- Agree the landing zone contract per source, covering arrival, ordering and duplicate handling.
- `Bronze` per slice: ingest from the landing zone, append-only, with schema handling and rescued records.
- `Silver` per slice: cleanse, standardize and hold the history of changing records.
- `Gold` per slice: aggregate, refine and enrich into the slice's target tables.
- Register and reuse conformed dimensions across slices.
- Run the parity tests in every slice that reproduces a figure users read today, in a report or in an application.
- Orchestrate each slice end to end and re-run it after a fix without invalidating its parity evidence.
- Build the cost mart over the platform's own usage data.
- Table maintenance is not scoped as work. Managed tables with clustering keys leave compaction to the platform.

### 📦 Deliverables

- Landing zone contract per source.
- Per slice: `Bronze`, `Silver` and `Gold` tables on managed storage with clustering keys, rescued records and validation metrics.
- Per slice: the orchestrating job with schedule, retries, notification routing and a stated freshness target.
- Per slice: the backfill and full-refresh procedure, with a parity re-run as its exit.
- The parity tests, comparing measure values at report grain and filter context against the figures users read today, whether a live Power BI semantic model or an application report such as APP, Smart or EPM, with a stated tolerance per measure type and pass or fail evidence per run.
- The conformed dimension register with its surrogate key strategy, and the rule that extending a shared dimension re-runs every prior slice's parity tests.
- The cost mart, views over the platform's billing, query history and audit data joined to the use case and team mapping.

## Usage layer

The endpoints users interact with: AI/BI, agents, workflows. Endpoints are Databricks built-in functionality, for example Dashboard, or custom apps consuming the `Gold` layer.

A consumer must exist at the end of every slice for usage feedback to start early, and one endpoint per slice is enough for that.

### ⚙️ Activities

- Build one endpoint per slice, dashboard first.
- Grant the slice's consumer group access to its `Gold` schema.
- Register the usage telemetry source for every endpoint, so adoption becomes measurable.
- Build custom apps and agent and workflow endpoints as demand arrives.
- Stay thin early. The track builds nothing ahead of demand.

### 📦 Deliverables

- One endpoint per slice.
- Per endpoint: the consumer group and its grants on the slice's `Gold` schema.
- Per endpoint: the registered usage telemetry source feeding the cost mart, with the grant that lets Deployment read it.
- Custom apps consuming the `Gold` layer.
- Agent and workflow endpoints, their stack settled by an architecture decision triggered by the first demand.

## Deployment

Drives use case adoption from an upfront selection process to roll out, through iterative improvement based on business team usage monitoring and feedback. Invite over Impose.

The name reads as an end phase, but the track bookends the plan: selection sits at the head and the invitation and feedback loop runs inside every slice. Its owner is staffed from day one.

### ⚙️ Activities

- Run the upfront use case selection process, at the head of the plan.
- Order the slice backlog and gate each slice on its readiness before it starts.
- Per slice: invite the owning business team, run its enablement, monitor usage, capture feedback.
- Read adoption from the cost mart against the metrics this track defines.
- Retire the superseded report and its refresh path once a slice is rolled out.
- Improve live use cases iteratively, then roll out.

### 📦 Deliverables

- The ordered slice backlog with its selection and sequencing criteria, and the per-slice readiness gate.
- The slice definition of done, applied to every slice.
- Per slice: the invitation, the team enablement session and the access request route.
- The per-team adoption metric definitions and the periodic adoption read from the cost mart.
- Per slice: retirement of the superseded report and its refresh path.
- Roll out of each use case.

## Deliverables at track junctions

Each deliverable below sits where tracks meet and has exactly one owner.

| Deliverable                    | Junction                                                                                                                                                                        | Owner                |
| :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------- |
| Landing zone volume            | Infrastructure delivers the storage and the access identity, Platform engineering declares the credential, the external location and the volume, Data engineering reads from it | Platform engineering |
| Model inventory                | Reads the production Power BI semantic models and feeds an architecture decision                                                                                                | Platform engineering |
| Reporting connectivity         | Delivered as a platform service, consumed by every endpoint the Usage layer repoints                                                                                            | Platform engineering |
| Parity tests per report        | Specified from the model inventory and the consumed application reports, run inside Data engineering pipelines, gate roll out                                                   | Data engineering     |
| Parity tests CI gate           | Runs the parity comparator's own tests on every merge                                                                                                                           | Platform engineering |
| Conformed dimension register   | Built inside the slice that first needs a shared dimension, binding on every later slice                                                                                        | Data engineering     |
| Cost mart                      | Reads the platform's usage data, Deployment reads adoption from it, provisioning decisions quote it                                                                             | Data engineering     |
| Endpoint usage telemetry       | Registered by the Usage layer, modelled into the cost mart, read by Deployment                                                                                                  | Usage layer          |
| Residual-risk review checklist | A CI review artefact applied to every pipeline                                                                                                                                  | Platform engineering |
| Deployment tooling boundary    | Fixes which catalog objects the infrastructure code owns and which the packaging tooling owns                                                                                   | Platform engineering |
| Provisioning gate              | An architecture decision quoting measured usage numbers, requested by the workload's track                                                                                      | Platform engineering |

| Field        | Value      |
|--------------|------------|
| Version      | 1.2        |
| Last Updated | 2026-08-21 |
| Status       | Draft      |
