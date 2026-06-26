# O2 platform roadmap — PI1

Context: greenfield Azure Databricks, account created June 2026, Premium tier. All product and feature names verified against current official Microsoft Learn documentation for Azure Databricks (see sources). This file holds eight epics, ordered by dependency.

The first ingestion pattern reads JSON from a SharePoint document library into a bronze Delta table through a Unity Catalog connection (standard SharePoint connector, scheduled Auto Loader drain), per the locked design in `2026-06-24-sharepoint-to-bronze-ingestion-lock-in.md`. CI/CD runs on Azure DevOps, chosen over GitHub Actions for ecosystem compliance and integration with existing Azure DevOps tooling.

## Scope and sequencing

The epics depends on the ones before it.

- Epics 1 to 6, the commercial, architecture, infrastructure, CI/CD and governance foundations.
- Epics 7 and 8, the cost and usage reporting. They depend on the full foundation and on accumulated billing data.

Pre-GA risk: several features this roadmap relies on are still Public Preview on Azure as of June 2026, namely the `system.access.audit` table, serverless usage policies, and Budgets. The first ingestion pattern also depends on the SharePoint standard connector, which is Beta on a Databricks Runtime 17.3 LTS floor. These are usable but not yet generally available, so treat their stability and SLA as a delivery risk for any epic or workload that depends on them.

Epic type follows SAFe: enabler epics build the architectural runway, business epics deliver visible value. The "so that" clause states the runway unlocked (enablers) or the value delivered (business).

---

## Epic 1 (Enabler — commercial) — Procurement onboarding

> Establish the commercial and account foundation for Azure Databricks: the Azure subscription and billing account, the purchase vehicle, the Databricks account, and the access roles for the provisioning teams, so that the platform can be built and billed. This gates every epic that follows.

Acceptance criteria:
- An Azure subscription and billing account are in place, with the purchase vehicle confirmed (Enterprise Agreement, Microsoft Customer Agreement, or pay-as-you-go).
- The Azure Databricks account is created on the Premium tier, the only option for new workspaces from 1 April 2026.
- The Microsoft Entra ID tenant is identified and provisioning roles are assigned to the platform teams.

## Epic 2 (Enabler — architecture) — Solution architecture document

> Produce and sign off the solution architecture for the Azure Databricks platform, covering topology, networking, identity, storage, and the IaC and CI/CD approach, so that infrastructure and delivery decisions are agreed before build and rework is avoided. Depends on Epic 1.

Acceptance criteria:
- Target topology is documented: workspaces, regions, and the single Unity Catalog metastore per region.
- Network design is decided: VNet injection, secure cluster connectivity (no public IP), Azure Private Link, and serverless egress through the Azure network security perimeter (NSP) with the `AzureDatabricksServerless` service tag.
- Identity design is decided: Microsoft Entra ID as the identity provider with automatic identity management (the greenfield default, enabled by default for accounts created after 1 August 2025), and the service principal model for automation.
- Storage design is decided: ADLS Gen2 with an Access Connector for Azure Databricks as the managed-identity storage credential.
- Tooling is decided: ARM or Bicep for Azure infrastructure, Terraform for infrastructure resources including the workspace, networking and Unity Catalog, and Declarative Automation Bundles for data and AI workloads (jobs, pipelines, notebooks, models).
- The document is reviewed and signed off by architecture and security stakeholders.

## Epic 3 (Enabler — infrastructure) — Infrastructure setup

> Deploy the Azure plumbing for the platform: the Azure Databricks workspace, network isolation, ADLS Gen2 storage with its access connector, the Unity Catalog metastore, and Entra ID identity wiring, so that a secure, network-isolated platform is ready to host governed workloads. Depends on Epics 1 and 2.

Acceptance criteria:
- The Azure Databricks workspace is deployed on the Premium tier via ARM or Bicep, not manual portal clicks. Premium is required because Unity Catalog only attaches Premium workspaces.
- Networking is in place: VNet injection, secure cluster connectivity (no public IP), Private Link for the workspace, and serverless egress controlled by NSP with the `AzureDatabricksServerless` service tag.
- ADLS Gen2 storage is provisioned, with an Access Connector for Azure Databricks (managed identity) configured.
- A Unity Catalog metastore exists for the region, with the storage credential registered. If a metastore already exists in the region, the workspace is assigned to it through the account console.
- Microsoft Entra ID is wired up as the identity provider with automatic identity management.
- The whole deployment is reproducible from version-controlled IaC.

## Epic 4 (Enabler — infrastructure) — CI/CD pipeline

> Establish version-controlled, repeatable deployment for all Databricks code and resources using Declarative Automation Bundles and a service-principal-authenticated Azure DevOps pipeline, so that every change after this point ships as a reviewable, automated release across environments. Depends on Epic 3, and is the delivery mechanism for Epics 5 to 8.

Acceptance criteria:
- A source repository and branching model are established for Databricks code and configuration.
- Declarative Automation Bundles (formerly Databricks Asset Bundles) define jobs, pipelines and resources as code.
- An Azure Pipelines (Azure DevOps) pipeline runs `databricks bundle deploy`. Azure DevOps is chosen over GitHub Actions for ecosystem compliance and integration with existing Azure DevOps tooling.
- Deployment authenticates as a Microsoft Entra service principal. The documented default uses OAuth M2M (client ID and secret); workload identity federation through an Azure DevOps service connection is the recommended secret-free alternative and is preferred where supported.
- Separate dev, test and prod targets deploy through the same bundle definitions.
- A sample job deploys end-to-end through the pipeline as proof.

## Epic 5 (Enabler — infrastructure) — Unity Catalog governance foundation

> Establish Unity Catalog as the single governance layer for the workspace: catalogs and schemas, managed tables and storage, external locations and storage credentials, identity, access grants, lineage, and connections to external data sources, so that all data and AI assets are governed under one model for security, discovery, semantics, and connectivity. Depends on Epic 3.

Acceptance criteria:
- New workloads run against a Unity Catalog catalog, not the legacy Hive metastore.
- Managed tables and volumes are created in Unity Catalog with a defined managed storage location on ADLS Gen2.
- External locations and storage credentials are configured via the Access Connector for Azure Databricks and access-tested against ADLS Gen2.
- A Unity Catalog connection to the source SharePoint document library is configured for the first ingestion pattern, using the standard SharePoint connector authenticated as an OAuth M2M service principal (Entra app, Sites.Selected or Sites.Read.All scope).
- Microsoft Entra ID with automatic identity management syncs users and groups from the identity provider, so no manual SCIM provisioning is needed. Assigning a synced group to a workspace is still a separate manual step.
- Access grants enforce least privilege. An unauthorised access attempt is denied and recorded in `system.access.audit`.
  > ⚠️ Unverified — the cited audit-log source documents the `response.statusCode` field but does not state that denied/unauthorised attempts produce audit rows; confirm the audit behaviour for denied access before relying on it for the test.
- Column-level lineage is captured automatically for a sample pipeline.
  > ⚠️ Unverified — column-level lineage is not covered by any source cited for this epic; verify against the Unity Catalog data lineage documentation before sign-off.

## Epic 6 (Enabler — compliance) — Cost and usage attribution model

> Define and enforce the cost-attribution model on top of Unity Catalog: a tag taxonomy and naming standard, applied through cluster policies and serverless usage policies, so that every workload carries the identity and ownership tags that all cost and usage reporting depends on. Depends on Epic 5.

Acceptance criteria:
- A tag taxonomy and naming standard are documented and agreed with the owning teams.
- Cluster policies enforce mandatory tags, so untagged compute cannot be launched.
- Serverless usage policies apply tags to serverless workloads (notebooks, Lakeflow Jobs, Lakeflow Spark Declarative Pipelines, serving endpoints, apps). Tags apply automatically when a user is assigned a single policy. A user with multiple policies must select the applicable policy at creation.
- A test workload's usage appears in `system.billing.usage` with the mandated `custom_tags` populated.

## Epic 7 (Business) — Cost monitoring and ownership for compute and storage

> Build cost observability across Databricks compute (all-purpose clusters, jobs compute, SQL warehouses, serverless) and storage (Unity Catalog managed tables and the underlying ADLS Gen2 storage), using the `system.billing.usage` and `system.billing.list_prices` system tables, so that DBU and dollar cost can be attributed to an owner and controlled through Budgets and serverless usage policies. Depends on Epics 5 and 6. PI2 candidate.

Acceptance criteria:
- A dashboard reports DBU and dollar cost by compute type and by storage, sourced from `system.billing.usage` joined to `system.billing.list_prices`.
- Cost is broken down by owner and team using the tags defined in Epic 6.
- Budgets are configured with alerts at defined spend thresholds.
- A given cost line can be traced back to a specific cluster, SQL warehouse, or job.
- Policy-level filtering uses `usage_metadata.usage_policy_id`. The older `usage_metadata.budget_policy_id` field is deprecated.

## Epic 8 (Business) — Usage attribution for ingestion and consumption

> Build usage monitoring that attributes ingestion (Auto Loader, Lakeflow Spark Declarative Pipelines, Lakeflow Jobs) and consumption (SQL warehouse queries, Model Serving model and agent endpoints) to an identity, using `system.billing.usage` `identity_metadata` and correlating control-plane actor data from `system.access.audit`, so that DBUs are traceable to a user or service principal (agent) for the workload types that expose identity. Depends on Epics 5, 6 and 7. PI2 candidate.

Acceptance criteria:
- Ingestion usage is attributed to a user or service principal for each pipeline and job, via `identity_metadata.run_as` (populated for jobs compute, serverless compute for jobs, serverless compute for notebooks, Lakeflow Spark Declarative Pipelines, Foundation Model Fine-tuning, predictive optimization and data quality monitoring). The first ingestion pattern, the scheduled SharePoint-to-bronze Auto Loader job, is attributed via its `run_as` service principal.
- Consumption usage is attributed to an identity: SQL warehouse usage via `identity_metadata.owned_by`, and Model Serving / agent endpoints where an identity field is populated.
- Identity resolution is best-effort, not total. The `identity_metadata` struct (`run_as`, `owned_by`, `created_by`) populates only for certain workload types, so usage without an identity field (for example all-purpose compute or plain model-serving endpoints) is flagged as unattributable rather than forced onto an owner. The `system.access.audit` table names the actor of control-plane actions but holds no usage quantities, so it corroborates an identity rather than attributing billed usage on its own.
  > ⚠️ Unverified — confirm the join path between `system.access.audit` and `system.billing.usage` before relying on it; the cited sources document no shared key.
- Agent activity (service principals) is distinguishable from human user activity wherever `run_as` / `created_by` populates.

---

## Sources

All verified against current Microsoft Learn documentation for Azure Databricks (June 2026).

- [Azure Databricks account and subscription](https://learn.microsoft.com/en-us/azure/databricks/admin/account-settings/account)
- [Standard tier retirement](https://learn.microsoft.com/en-us/azure/databricks/admin/account-settings/standard-tier)
- [Infrastructure-as-code deployment guide](https://learn.microsoft.com/en-us/azure/databricks/lakehouse-architecture/deployment-guide/iac)
- [Workspace ARM template deployment](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace/arm-template)
- [VNet injection](https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/vnet-inject)
- [Secure cluster connectivity](https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/secure-cluster-connectivity)
- [Serverless network security and NSP firewall](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-nsp-firewall)
- [Microsoft Entra ID automatic identity management](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/automatic-identity-management/)
- [Access Connector for Azure Databricks (managed identity)](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/azure-managed-identities)
- [Enable a workspace for Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/enable-workspaces)
- [Create a Unity Catalog metastore](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/create-metastore)
- [Billable usage system table](https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/billing)
- [Pricing system table](https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/pricing)
- [Audit log system table](https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/audit-logs)
- [Attribute usage with serverless usage policies](https://learn.microsoft.com/en-us/azure/databricks/admin/usage/budget-policies)
- [Create and monitor budgets](https://learn.microsoft.com/en-us/azure/databricks/admin/account-settings/budgets)
- [Declarative Automation Bundles](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/)
- [CI/CD with Azure DevOps](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/ci-cd/azure-devops)
- [Authenticate with Azure DevOps](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth/auth-with-azure-devops)
- [Service principals for CI/CD](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth/service-principals)
- [SharePoint standard connector](https://learn.microsoft.com/en-us/azure/databricks/ingestion/sharepoint)
- [Standard connectors in Lakeflow Connect](https://learn.microsoft.com/en-us/azure/databricks/ingestion/)
- [SharePoint source setup overview](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/sharepoint-source-setup-overview)

---

<!--
Version: 1.9 | Last Updated: 2026-06-26 | Status: Draft
-->
