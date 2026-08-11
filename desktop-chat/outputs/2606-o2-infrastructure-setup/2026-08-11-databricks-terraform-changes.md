# Databricks platform: Terraform changes required

> For whoever owns the Databricks Terraform. Assumes Azure and Terraform, assumes
> nothing about Unity Catalog.
> Findings come from running the sequence in [[dbr-platform-foundation-setup]]
> against `DBR-DATABRICKS-DEV` on 2026-08-11, by hand, as a workspace admin
> holding Contributor on `RG-DATABRICKS-DEV`. Everything created during that test
> was deleted afterwards. One modification remains: a display name set on the
> existing service principal.

The data platform cannot be finished from where the operator stands. Not for want
of Databricks permissions, but because the missing pieces need Azure rights the
operator does not have and cannot be given casually. So the code has to produce
them.

## What to change

| # | Change | Provider |
| :--- | :--- | :--- |
| 1 | Landing storage account, its role assignment, and the external location over it | `azurerm` and `databricks` workspace |
| 2 | `display_name` on the existing `databricks_service_principal` | `databricks` workspace |
| 3 | `isolation_mode` and `owner` on any `databricks_catalog` and `databricks_schema` | `databricks` workspace |
| 4 | Tag or remove the auto-created SQL warehouse | `databricks` workspace |
| 5 | Network connectivity config, its private endpoint rules, and its workspace binding | `databricks` account |
| 6 | Order group assignment ahead of anything granting a workspace permission | `databricks` both |

Numbers 1 and 5 are the substantial ones. The rest are arguments on resources
that already exist or soon will.

## Before anything else: the provider is configured twice

Account-level and workspace-level Databricks resources need different provider
blocks, and mixing them fails in a way that reads as a credentials problem.

```hcl
provider "databricks" {
  alias = "workspace"
  host  = "https://adb-<id>.<n>.azuredatabricks.net"
  # no account_id here
}

provider "databricks" {
  alias      = "account"
  host       = "https://accounts.azuredatabricks.net"
  account_id = var.databricks_account_id
}
```

Setting `account_id` on the workspace provider produces
`invalid Databricks Account configuration`. Everything prefixed `databricks_mws_`
is account-level and needs the second alias. That includes the whole of change 5.

The account provider also needs an identity with a Databricks account admin role,
which is not an Azure role and which nobody on the team currently holds. See
rights, below.

## Three facts that make the changes make sense

**Databricks never uses the caller's credentials to reach storage.** It uses a
managed identity on an Azure resource called a Databricks Access Connector.
Whoever runs the query, the storage read happens as that identity. Granting a
user or a service principal access to a storage account therefore does nothing.
The connector's identity is what needs the data role. This is change 1.

**A storage path must be registered inside Databricks before it can be used.**
The registration is `databricks_external_location`, which pairs an ADLS path with
a `databricks_storage_credential` that wraps the connector identity. Until it
exists, Databricks cannot touch that path whatever Azure says. Also change 1.

**Serverless compute is not in your VNet.** Classic compute runs in the injected
subnets you built. Serverless runs in a Microsoft-managed network, so your
private endpoints do not reach it and it does not appear in your flow logs. This
is change 5, and it is the reason a separate construct exists at all.

## 1. The landing storage path

Three resources, one configuration, because the middle one is what nobody can do
by hand:

- `azurerm_storage_account` with `is_hns_enabled = true`
- `azurerm_role_assignment` giving the Access Connector's principal Storage Blob
  Data Contributor on it
- `databricks_external_location` over the container, referencing the existing
  storage credential

Two things we established by trying rather than reading. A holder of Contributor
on `RG-DATABRICKS-DEV` is refused `Microsoft.Authorization/roleAssignments/write`,
which kills the second resource. And the Access Connector lives in the Databricks
managed resource group, which the same holder cannot read, so its principal ID is
not even visible to them. There is no manual path.

Two constraints on the storage account itself:

- `is_hns_enabled` cannot be turned on after creation. Getting it wrong means
  replacing the account, not amending it
- The four tags are enforced by a deny policy on that resource group. An apply
  omitting `owner`, `environment`, `cost_center` or `project` is refused and the
  error names each missing one. Confirmed by attempting it

Worth considering while you are there: `shared_access_key_enabled = false` and a
default network action of Deny. Nothing currently forces either.

## 2. Display name on the service principal

The existing `databricks_service_principal` sets `application_id` and no
`display_name`. The consequence is that every API response, audit log entry,
object owner field and permission listing shows a bare GUID rather than
`SP-Terraform-fra-sqli-dev`. The UI hides this by resolving the name through the
identity provider, so it looks fine until you read the API.

One argument. I set it by hand during the test, so it disappears at the next
apply unless the code carries it.

## 3. Isolation and ownership on catalogs

A catalog is the top-level data container. Catalogs live in a metastore, which is
regional and shared, and there is at least one other workspace on yours.

- Without `isolation_mode` set to isolated, a catalog is visible from every
  workspace on that metastore. What Databricks provisions for itself is isolated.
  What you create is not. Use `databricks_catalog_workspace_binding` if you need
  it bound to more than one
- Without `owner`, the catalog belongs to whichever identity ran the apply, which
  in your case is the deployment principal. Ownership carries the right to grant
  access and to transfer ownership away, so leaving it unset is a permissions
  decision made by accident. Set it to a group

## 4. The auto-created warehouse

Workspace provisioning creates a SQL warehouse called
`Serverless Starter Warehouse` carrying no tags. Your Azure tag policy does not
reach it, because Databricks compute is billed through Databricks rather than
through Azure resource metering. So the estate has untagged compute from the
moment it is built, and nothing on the Databricks side can retroactively tag it.

Either give it tags or stop it being created.

## 5. The serverless network path

Three account-level resources:

- `databricks_mws_network_connectivity_config` in the workspace region
- `databricks_mws_ncc_private_endpoint_rule`, one per storage subresource. `dfs`
  for Unity Catalog, plus `blob` if you use model serving
- `databricks_mws_ncc_binding` attaching it to the workspace

Adding a private endpoint rule makes Databricks raise a private endpoint request
against your storage account. It sits `PENDING` until someone with rights on that
account approves it in the portal, then reaches `ESTABLISHED`. So this is not a
single apply, it is an apply, a human, and then a wait.

Two things that will cost an afternoon if missed.

You need two endpoints, not one. One from the Databricks serverless network via
the NCC, and one from your own VNet for classic compute. Build only the first and
clusters break. Build only the second and serverless breaks. Databricks is
explicit that once a resource only accepts private endpoint connections, classic
compute must use one too.

Order matters. Leave the storage account open until both are approved. Close it
first and every failure surfaces as a permissions error rather than a network
one.

If you find older internal guidance: allowlisting Databricks serverless IP ranges
on a storage firewall stopped being supported on 9 June 2026. Private endpoints
through an NCC, or a network security perimeter allowlisting the
`AzureDatabricksServerless` service tag, are what remain.

Limits, in case they bite: ten NCCs per region per account, one hundred private
endpoints per region, fifty workspaces per NCC. France Central supports this.
Databricks bills networking costs for serverless connections to your resources.

## 6. Group assignment before workspace permissions

This only applies if the code manages Databricks groups and permissions, and if
it does it will bite once and be baffling.

Databricks resolves principals two different ways. Unity Catalog grants, which
cover data, accept a group that exists at the account level.
`databricks_grants` will happily take one. Workspace permissions, which cover
secret scopes, warehouses, clusters and jobs, only accept a principal that has
been assigned to the workspace by `databricks_mws_permission_assignment`.

So a group can exist, hold data permissions, and still be rejected outright when
you attach it to a secret scope. We hit exactly that: the account-level principal
was refused, the workspace-level one worked. If your resources do not reference
each other, the dependency graph has no reason to order them, and the apply fails
on a race that then succeeds on retry.

## A lifecycle question, not a change

Workspaces are regenerated into a persistent resource group. If the landing
storage sits in the same configuration as the workspace, a regeneration destroys
the data. It probably belongs in its own configuration, but that is a decision
rather than a defect and it is not mine to make.

## Rights that no code change replaces

**A Databricks account admin.** Ten of the twenty-six setup steps need one, and
so does the account provider alias above. It is not an Azure role, Terraform
cannot grant it, and the first one in a tenant has to be created by an Entra
Global Administrator signing in to the account console once. Nobody on the team
demonstrably holds it today.

**Role assignment rights, but only if a human should ever attach storage without
a deploy.** That means Role Based Access Control Administrator, scoped to the
resource group and constrained to the storage data roles. The alternative, that
storage only ever gets attached by an apply, is defensible and cheaper.

## Outside this Terraform

Nothing in `RG-DATABRICKS-DEV` constrains storage networking. We created a
storage account reachable from the internet and no policy objected, in an estate
where the workspace itself has front-end and back-end Private Link and no public
IP. The four tag policies are the only guardrails on that resource group.

Shared key access is on by default for new storage accounts there.

## What was tested and what was not

Tested by doing, as a workspace admin: creating a service principal, a catalog
with an explicit managed location, a schema, grants to both a group and a service
principal, a cluster policy, a serverless SQL warehouse, and a secret scope with
an ACL. Then writing a table and reading it back. All worked. The tag deny policy
works. The storage path under the workspace's own container is writable.

Not tested: the private endpoint path, the CI federation policy, and every step
needing a Databricks account admin. Doing something by hand shows the platform
allows it. It does not show the Terraform will produce it.

<!--
Version: 2.0 | Last Updated: 2026-08-11 | Status: Draft
-->
