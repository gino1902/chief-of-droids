# Databricks platform: Terraform changes required

> For whoever owns the Databricks Terraform. Assumes Azure and Terraform, assumes
> nothing about Unity Catalog.

## Evidence

- Ran the sequence in [[dbr-platform-foundation-setup]] by hand against
  `DBR-DATABRICKS-DEV`, 2026-08-11 and 2026-08-12, as a workspace admin holding
  Contributor on `RG-DATABRICKS-DEV`
- Read Microsoft Learn. Sources with dates at the end
- **Did not read your Terraform.** Nobody has pointed me at the repo. Claims below
  are about observed platform state and what it implies for code you can check
  and I cannot
- Test objects were deleted. One change remains: a display name set by hand on the
  service principal, which your next apply will drop

## Two things block the sequence

| Blocker | Scope | Fixed by |
| :--- | :--- | :--- |
| Azure rights to register managed storage with Unity Catalog | Change 1 | Code |
| A Databricks account admin role nobody holds | Four steps and one half-step, including change 5 | Nothing in code |

## What to change

| # | Change | Provider |
| :--- | :--- | :--- |
| 1 | Durable storage account for managed data, one role assignment, external locations | `azurerm` + `databricks` workspace |
| 2 | Display name on the service principal | `databricks` workspace |
| 3 | Explicit isolation and ownership on catalogs and schemas | `databricks` workspace |
| 4 | Tag or remove the pre-existing SQL warehouse | `databricks` workspace |
| 5 | Serverless network access to storage, one of two routes | `azurerm` + `databricks` account |
| 6 | Order group assignment ahead of workspace permissions | `databricks` both |
| 7 | Confirm the teardown force deletes | `azurerm` |

1 and 5 are substantial. 7 is a question about your destroy path. The rest are
arguments on resources that exist or soon will.

## Provider is configured twice

```hcl
provider "databricks" {
  alias = "workspace"
  host  = "https://adb-<id>.<n>.azuredatabricks.net"
  # no account_id
}

provider "databricks" {
  alias      = "account"
  host       = "https://accounts.azuredatabricks.net"
  account_id = var.databricks_account_id
}
```

- `account_id` on the workspace provider returns
  `invalid Databricks Account configuration`
- Everything prefixed `databricks_mws_` is account-level and needs the second alias
- The account alias needs an identity holding Databricks account admin

## Three facts behind the changes

- **Databricks never uses the caller's credentials for storage.** It uses a managed
  identity on an Azure resource called a Databricks Access Connector. Granting a
  user or service principal access to a storage account does nothing. Change 1
- **A storage path must be registered before use.** `databricks_external_location`
  pairs an ADLS path with a `databricks_storage_credential` wrapping the connector
  identity. Without it Databricks cannot touch the path whatever Azure says.
  Change 1
- **Serverless compute is not in your VNet.** It runs in a Microsoft-managed
  network, so your private endpoints do not reach it and it does not appear in
  your flow logs. Change 5

## 1. Durable storage for managed data

Not a landing zone. Nothing writes files here. This is where the managed tables
of every catalog physically live, bronze and everything after it.

- `azurerm_storage_account`, `is_hns_enabled = true`
- Containers, shape by environment, below
- One `azurerm_role_assignment` per container or per account, below
- `databricks_external_location` per container

### It must be in its own Terraform state

Not merely a separate resource. Data outlives the workspace: you rebuild the
shell, the catalogs and their files stay. If `terraform destroy` on the workspace
can reach this account, the separation is decorative and the first regeneration
takes the data.

The obvious shortcut, pointing catalogs at the workspace's own Unity Catalog
container, is the wrong answer for the same reason. That container is created by
the workspace and orphaned when it goes, leaving your data in a converted
resource group nobody manages.

### Container shape differs by environment

| | Dev | Prod |
| :--- | :--- | :--- |
| Containers | One, a path per catalog | One per catalog |
| Path | `abfss://managed@<acct>/<catalog>` | `abfss://<catalog>@<acct>/` |
| External locations | One | One per container |
| Role assignment scope | Account | Container |
| Retention and immutability | Not set | Per container |

Container-scoped grants in prod are the point of the split. One account-scoped
grant makes it decorative. Retention and immutability are container-level
settings in Azure and cannot be applied per path, which is the other reason prod
splits.

Drive the shape from a variable in one module rather than two configurations, or
a prod apply exercises a path dev has never run.

### One role, not four

**Storage Blob Data Contributor**, on the access connector's managed identity.

Storage Queue Data Contributor, Storage Account Contributor and EventGrid Data
Contributor exist only for file events, and file events exist only when raw files
land in storage. Nothing lands here, so all three drop, and so does the
disagreement between two Microsoft pages over the EventGrid role name.

If a producer ever writes files rather than calling an API, all three come back
and that disagreement matters again.

### Decide the access connector

Tracked in the runbook as the Access Connector and external location granularity
ADR.

| Option | Consequence |
| :--- | :--- |
| Reuse the existing connector | Fewest resources, but it sits in the workspace's managed resource group. Unreadable by the operator, and it dies with the workspace |
| New connector in a resource group you control | `azurerm_databricks_access_connector` plus its own `databricks_storage_credential`. Durable, and creating one needs only Contributor on a resource group |

Given the whole point of change 1 is durability, the second is the consistent
answer.

### Established by trying

- Contributor on `RG-DATABRICKS-DEV` is refused
  `Microsoft.Authorization/roleAssignments/write`
- The Access Connector is in the managed resource group, unreadable by the same
  holder, so its principal ID is invisible to them
- An untagged create is refused by deny policy, naming each missing tag

### Storage account constraints

- `is_hns_enabled` can be added after creation, but only through a one-way
  migration that disables writes while it runs and fails validation if immutable
  storage, soft delete, snapshots or encryption scopes are enabled, or if page
  blobs are present. Set it at creation. Getting it wrong is a migration under a
  write freeze rather than a replacement, which is cheaper than previously stated
  here and still not something to schedule
- Four tags at creation: `owner`, `environment`, `cost_center`, `project`
- Keep the account name to 44 characters or fewer if change 5 takes route A. A
  perimeter association is named `{resourceName}-{perimeter-guid}` and must fit
  Azure's 80-character field
- Consider `shared_access_key_enabled = false` and a default network action of
  Deny. Nothing currently forces either

## 2. Display name on the service principal

- SCIM record for `9ff3bc2c-c77a-436a-a8b1-a740cd61cae0` had no `displayName`
  until I set one
- While empty, every API response, audit entry, object owner and permission
  listing showed the bare application ID
- The UI hid it by resolving through the identity provider
- If the resource does not set `display_name`, the next apply drops it again

## 3. Isolation and ownership on catalogs

Catalogs live in a metastore that is regional and multi-tenant. Yours has been in
use since 2024 and carries catalogs owned outside this project, one already named
`bronzes`.

- **Isolation takes two resources.** Set `isolation_mode` to isolated **and**
  create a `databricks_catalog_workspace_binding` for every workspace that should
  reach it, including your own. Isolation alone hides the catalog from everybody
- Observed: a catalog created through the CLI arrives `OPEN`. The one Databricks
  provisioned is `ISOLATED`
- **Set `owner` to a group.** Unset, the catalog belongs to whichever identity ran
  the apply, and ownership carries the right to grant access and transfer
  ownership away

## 4. Pre-existing warehouse

- `Serverless Starter Warehouse` exists, stopped, untagged, created by the
  deployment principal on 2026-08-10. Whether your code or Databricks made it is
  visible to you and not to me
- Azure tag policy does not reach it. Databricks compute bills through Databricks
- Compute policies enforce tags on clusters and jobs, not warehouses
- A warehouse accepts tags at creation, confirmed. Editing an existing one is
  untested

## 5. Serverless network path

Two routes, opposite end states. Blending them breaks serverless and reports it as
a permissions error.

Common to both:

- Allowlisting Databricks serverless IP ranges stopped being supported 9 June 2026
- Both affect classic compute, which needs its own path from your VNet

### Route A, network security perimeter

Databricks recommends this for storage in the workspace region. Backbone traffic,
no data processing charges.

- Create a perimeter in the workspace region, note the profile ID
- Associate the storage account, leave it in **transition** mode
- Inbound rule, source type Service Tag, regional
  `AzureDatabricksServerless.<region>`
- **End state: Public network access stays on Enabled from selected networks.** Not
  Secured by Perimeter, which stops serverless reading external locations and
  returns `PERMISSION_DENIED`
- Needs a Databricks account admin, Contributor or Owner on the resource, and
  rights to create perimeter resources
- Two constraints that arrive with the perimeter: Azure Backup is unsupported on
  an associated storage account, and object replication and static websites are
  too. The first lands on the data protection decision
- Databricks and Azure Storage disagree about transition mode. Databricks
  "recommends remaining in transition mode indefinitely". The Azure Storage page
  calls it a staging step and says it is "crucial" to reach enforced. Enforced
  mode stops honouring trusted services and can deny service endpoint traffic
  "even when an inbound rule allows 0.0.0.0/0", which is how classic compute
  usually reaches storage from your VNet. Databricks has the better argument here,
  but a security review citing the Azure page will challenge it

### Route B, private endpoints via NCC

- `databricks_mws_network_connectivity_config` in the workspace region
- `databricks_mws_ncc_private_endpoint_rule` per subresource. `dfs` for Unity
  Catalog, `blob` for model serving
- `databricks_mws_ncc_binding` to the workspace
- A second private endpoint from your own VNet for classic compute
- **End state: Public network access Disabled**, after both are approved. The
  source presents this as optional hardening rather than a requirement, so route B
  works without it. Route A's end state, by contrast, is prescribed
- Not a single apply. Each rule sits `PENDING` until someone with rights on the
  storage account approves it in the portal
- Requires the Premium plan and a Databricks account admin
- Limits: 10 NCCs per region, 100 private endpoints per region, 50 workspaces per
  NCC. Databricks bills networking costs for serverless connections

> Network security perimeter is generally available in all Azure public cloud
> regions, so France Central is covered and route A is open. Read 2026-08-12,
> closing an earlier open question.

### Allow trusted Microsoft services

- Route A cannot connect without it, in transition mode. Enforced mode ignores
  trusted services entirely, which is one more reason to stay in transition
- Under route B's Disabled end state, network rules do not apply and the setting
  is probably inert. 🔲 Unverified. Enable it anyway, do not rely on it

## 6. Group assignment before workspace permissions

Applies only if the code manages Databricks groups and permissions.

- Unity Catalog grants accept an account-level group
- Workspace permissions, covering secret scopes, warehouses, clusters and jobs,
  only accept a principal assigned to the workspace
- Observed: `account users` worked on a catalog grant, was refused on a secret
  scope ACL, where the workspace-level `users` group worked
- The Terraform resource is `databricks_mws_permission_assignment`, account-level,
  even though a workspace admin does the same thing in the UI
- Without a reference between resources the graph will not order them. The apply
  fails, then succeeds on retry

## 7. Confirm the teardown force deletes

A question, not an instruction. I cannot see your destroy path.

Deleting a workspace retains:

- The workspace catalog
- The managed resource group, converted to an ordinary one
- The storage container holding Unity Catalog data
- The access connector

So each regeneration without force deletion leaves a resource group, a storage
account, an access connector and a catalog on a metastore other teams use.

Force deletion is opt-in:

- Checkbox in the Azure portal workspace delete flow
- `az databricks workspace delete --force-deletion`
- `Remove-AzDatabricksWorkspace -ForceDeletion`
- `az group delete --force-deletion-types Microsoft.Databricks/workspaces`

Deleting the resource group through the portal UI does **not** force delete.
Check what `terraform destroy` does, since azurerm passes no force flag unless
told.

## Open decision, not a change

Workspaces regenerate into a persistent resource group. Landing storage in the
same configuration as the workspace dies with each regeneration. Probably belongs
in its own configuration. Your call.

## Rights no code change replaces

| Right | Why |
| :--- | :--- |
| Databricks account admin | Four steps and one half-step, plus the account provider alias. Not an Azure role. The first in a tenant must be created by an Entra Global Administrator signing in to the account console once |
| Role Based Access Control Administrator, scoped to the resource group, limited to storage data roles | Only if a human should ever attach storage without a deploy. The alternative, apply-only, is cheaper |

## Outside this Terraform

- Nothing in `RG-DATABRICKS-DEV` constrains storage networking. A storage account
  reachable from the internet was created and no policy objected, in an estate
  where the workspace has front-end and back-end Private Link and no public IP
- Shared key access is on by default for new storage accounts there

## Tested and not tested

Eleven of the 24 steps exercised. Full coverage table in
[[dbr-platform-foundation-setup]] under "Proven against a live workspace". That
runbook split its admin settings step on 2026-08-12, so it now runs 1 to 19, 20a,
20b, 21, 22, 23.

**Worked**, as a workspace admin: service principal, account group with
entitlements, tagged ADLS account with hierarchical namespace and container,
catalog with explicit managed location, schema, grants to a group and a service
principal, cluster policy, serverless warehouse with tags, secret scope with ACL,
table written and read. Deny policy fired on an untagged create. Catalog binding
controls present and editable.

**Failed**: the role assignment and the access connector read behind change 1.

**Not tested**: either network route, the CI federation policy, every step needing
a Databricks account admin.

Doing something by hand shows the platform allows it. It does not show your
Terraform will produce it.

## Sources

Microsoft Learn unless noted. Page dates shown.

Fetched 2026-08-11:

- [Serverless compute plane networking](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/), 2026-08-07
- [Configure private connectivity to Azure resources](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-private-link), 2026-08-04. Route B
- [Connect to an ADLS Gen2 external location](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/external-locations-adls), 2026-06-10. Older EventGrid role name
- [Specify a managed storage location](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/managed-storage), 2026-08-04
- [Admin privileges in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/admin-privileges), 2026-06-23
- [Databricks administration overview](https://learn.microsoft.com/en-us/azure/databricks/admin/admin-concepts), 2026-07-28

Fetched 2026-08-12, carried from the runbook's sourcing pass:

- [Upgrade Azure Blob Storage with Azure Data Lake Storage capabilities](https://learn.microsoft.com/en-us/azure/storage/blobs/upgrade-to-data-lake-storage-gen2-how-to), 2025-11-03. The one-way hierarchical namespace migration, correcting change 1
- [What is a network security perimeter?](https://learn.microsoft.com/en-us/azure/private-link/network-security-perimeter-concepts), 2026-07-08. Generally available in all public cloud regions, the 44-character name limit, service endpoint traffic unsupported
- [Network Security Perimeter for Azure Storage](https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security-perimeter), 2025-07-27. Enforced mode ignores trusted services, Azure Backup unsupported, and the transition-mode advice that contradicts Databricks

Fetched 2026-08-12:

- [Manage external locations](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/manage-external-locations), 2026-08-11. The four file event roles, only one of which this platform needs
- [Configure an Azure network security perimeter](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-firewall-config), 2026-08-07. Route A
- [Delete a workspace](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace/delete-workspace), 2026-07-21. Change 7
- [Manage groups](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-groups), 2026-07-22
- [Workspace-catalog binding](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/access-control/workspace-catalog-binding), 2026-08-11
- [Manage service principals](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-service-principals), 2026-06-22
- [Databricks Terraform provider](https://github.com/databricks/terraform-provider-databricks/blob/master/docs/index.md), provider alias split and resource names

<!--
Version: 4.1 | Last Updated: 2026-08-12 | Status: Draft
-->
