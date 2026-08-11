# Databricks platform: Terraform changes required

> For the platform engineer who owns the Terraform. It assumes Azure and
> Terraform knowledge and no Databricks knowledge.
> Findings come from testing the sequence in [[dbr-platform-foundation-setup]]
> against the workspace `DBR-DATABRICKS-DEV` on 2026-08-11. Everything created
> during that test has been deleted. One change was not a creation and remains:
> a display name set on the existing service principal, described below.

Short answer: yes, changes are needed, and the biggest one is something that is
missing rather than something that is wrong. The storage path that the data
platform reads from does not exist in the Terraform, and nobody on the team can
create it by hand. We tried.

## Three facts about Databricks that explain the rest

Databricks does not use the caller's credentials to reach storage. It uses a
managed identity attached to an Azure resource called a Databricks Access
Connector. Whoever runs the query, the storage access happens as that identity.
Granting a person or a service principal access to a storage account therefore
achieves nothing on its own. The connector's identity is what needs the data
role.

A storage path has to be registered inside Databricks before it can be used.
The registration is called an external location and it pairs an ADLS path with
the credential above. Until it exists, Databricks cannot read or write that path
at all, whatever the Azure permissions say.

Some Databricks compute runs inside your VNet and some does not. Classic compute
runs in the injected subnets you already built. Serverless compute runs in a
Microsoft-managed network outside your spoke, so the private endpoints in your
VNet do not cover it.

## The changes

### The landing storage account and its wiring, as one configuration

Three resources have to land together:

- An ADLS Gen2 storage account
- A role assignment giving the Access Connector's managed identity Storage Blob
  Data Contributor on that account
- A Databricks external location pointing at the container

The middle one is why this cannot be manual. A workspace operator holding
Contributor on `RG-DATABRICKS-DEV` is refused
`Microsoft.Authorization/roleAssignments/write`, and cannot even read the Access
Connector, because it lives in the Databricks managed resource group. We
confirmed both by trying. So either the code does this or it does not happen.

Without it, nothing can land in the platform. This is the first half of the data
path.

### Hierarchical namespace, set at creation

`is_hns_enabled = true`. This is what makes a storage account ADLS Gen2 rather
than plain blob storage, Databricks requires it for an external location, and it
cannot be enabled after the account exists. Getting it wrong means replacing the
account rather than amending it.

### The four enforced tags, set at creation

`owner`, `environment`, `cost_center`, `project`. The deny policy on the resource
group refuses a create that omits any of them and names each one in the error.
This will fail an apply rather than warn about it. We confirmed it by attempting
an untagged create.

### A display name on the Databricks service principal

The current `databricks_service_principal` resource sets an application ID and no
display name. Every API response, audit log entry and permission listing shows a
bare GUID instead of `SP-Terraform-fra-sqli-dev`. One argument fixes it. I set
the name by hand during testing, so it will disappear at the next regeneration
unless the code sets it.

### Explicit isolation on any catalog the code creates

A catalog is the top-level container for data in Databricks. Catalogs live in a
metastore, which is regional and shared, and there is at least one other
workspace on yours. A catalog created without an isolation setting is visible
from every workspace on that metastore. What Databricks provisions for itself is
isolated; what the code creates is not, unless it says so.

### Explicit ownership on catalogs and schemas

Otherwise they belong to whichever identity ran the apply. Ownership in
Databricks carries the right to grant access to others and to transfer ownership
away, so leaving it to chance is a permissions decision made by accident. Set it
to a group.

### The starter warehouse

Provisioning creates a SQL warehouse called `Serverless Starter Warehouse` with
no tags. The Azure policy denies untagged Azure resources, but Databricks compute
is billed through Databricks and that policy does not reach it. So the estate has
untagged compute from the moment it is built, and the Databricks-side tagging
mechanisms cannot reach back and fix it. Either tag it in code or do not create
it.

### The serverless network path

This one has the longest lead time and it is untested, because it needs a
Databricks account-level role nobody on the team currently holds.

Serverless compute cannot reach a firewalled storage account through your VNet
private endpoints, because it is not in your VNet. Databricks provides an
account-level object called a network connectivity configuration. Adding a
private endpoint rule to it makes Databricks raise a private endpoint request
against your storage account, which someone on the Azure side then approves.

Two endpoints are needed, not one. One from the Databricks serverless network,
and one from your own VNet for classic compute. Building only the first breaks
clusters. Building only the second breaks serverless.

Order matters. The storage account must stay open until both endpoints are
approved. Close it first and the failures appear as permission errors rather than
network ones, which is a slow afternoon for whoever debugs it.

One thing to know if you find older internal guidance: allowlisting Databricks
serverless IP ranges on a storage firewall stopped being supported in June 2026.
Private endpoints or a network security perimeter are what remain.

### Group assignment before anything that grants a workspace permission

This only matters if the code manages Databricks groups and permissions, but if
it does, it will bite.

Databricks has two permission systems that resolve principals differently. Unity
Catalog grants, which cover data, accept a group that exists at the Databricks
account level. Workspace permissions, which cover secret scopes, warehouses,
clusters and jobs, only accept a principal that has been assigned to the
workspace.

So a group can exist, be visible in the account, hold data permissions, and still
be rejected when you try to give it access to a secret scope. We hit exactly
that. The fix is ordering: assign the group to the workspace first. If the
Terraform resources do not reference each other, the graph will not know to do
that, and an apply can fail on a race that succeeds on the retry.

### A lifecycle question, not yet a change

Workspaces are regenerated into the same persistent resource group. If the
landing storage sits in the same configuration as the workspace, a regeneration
destroys the data. It probably belongs in a separate configuration with its own
lifecycle, but that is a decision rather than a defect.

## Rights that no code change replaces

An account admin. Ten of the twenty-six setup steps need an account-level
Databricks role. It is not an Azure role, Terraform cannot grant it, and the
sequence cannot finish without someone holding it.

Role assignment rights, but only if a human is ever expected to attach storage
without a deploy. That means Role Based Access Control Administrator, scoped to
the resource group and limited to the storage data roles. The alternative answer,
that everything goes through the repo, is defensible and cheaper.

## Outside this Terraform, but worth someone knowing

Nothing in `RG-DATABRICKS-DEV` constrains storage networking. We created a
storage account reachable from the internet and no policy objected, in an estate
where the workspace itself has front-end and back-end Private Link and no public
IP. The four tag policies are the only guardrails on that resource group.

Shared key access is enabled by default on new storage accounts there.

## What was tested, and what was not

Tested by doing: creating service principals, catalogs, schemas, grants, compute
policies, a serverless SQL warehouse and secret scopes, then writing and reading
a table. All worked. The tag deny policy works. The storage path under the
workspace's own container is writable.

Not tested: the private endpoint path, the CI federation policy, and every step
that needs a Databricks account admin. Creating something by hand shows the
platform allows it. It does not show that the Terraform will produce it.

<!--
Version: 1.1 | Last Updated: 2026-08-11 | Status: Draft
-->
