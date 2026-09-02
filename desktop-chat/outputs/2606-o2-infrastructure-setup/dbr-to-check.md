# DBR - To check


## Make sure catalog is not on the default storage

> **Status 2026-09-02: not satisfied, and knowingly so for `dev_sandbox`.**
>
> Observed on the workspace: `dev_sandbox` is a managed catalog whose `storage_root` is
> `abfss://unity-catalog-storage@dbstorageu2vas6zgjlwwo.dfs.core.windows.net/7405605180591006/dev_sandbox`.
> That is the workspace's own managed storage account, which is exactly the arrangement the
> steps below argue against. `pbi_sandbox` and the `datawan_*` catalogs were not checked.
>
> For `dev_sandbox` this is the right trade, because it is disposable by decision and holds
> nothing that must survive a workspace rebuild. For dev, staging and production it is the
> open question this note exists to force, and it is still open.
>
> Two things this changes below. Point 3 is the one that has already been foreclosed for
> `dev_sandbox`, since a catalog's managed location is adjustable while it is empty and not
> adjustable once a table exists. And "default storage" is ambiguous in the heading: the
> workspace's managed storage account and the Databricks default-storage feature for
> serverless workspaces are different things, and only the first is in play here.
>
> Related: `../2606-o2-architecture-design/2026-09-01-bronze-table-design.md`, section
> "Storage and compute, as observed".

### How to make the catalog independent

1. Dedicated storage. Provision a storage account or bucket for the catalog in its own resource group or stack, never inside the workspace's managed resource group or Terraform state.
2. Independent credential. Create the storage credential from resources you own: an Azure Databricks access connector with a managed identity, or an AWS IAM role. Provision these alongside the storage, not the workspace.
3. Explicit managed location. Create the catalog with MANAGED LOCATION 'abfss://...' (or s3://...) on an external location backed by that storage. Then the metastore root is never used for this catalog's managed tables.
4. Split your IaC stacks. One stack (own state file) for UC objects: metastore assignment aside, that is storage credential, external location, catalog, schemas, grants. A separate stack for the workspace. terraform destroy on the workspace stack then cannot touch catalog resources. Add lifecycle { prevent_destroy = true } on the catalog and avoid force_destroy = true on databricks_catalog.
5. Mind the provider authentication. UC objects are managed through a workspace-level API, so the Terraform provider for the UC stack authenticates via some workspace host. Point it at a long-lived admin workspace, not the ephemeral one, otherwise destroying the workspace breaks your ability to plan the UC stack.
6. Workspace bindings. If the catalog's isolation mode is ISOLATED and it was bound only to the destroyed workspace, the catalog still exists but is reachable from nowhere. After attaching a new workspace to the metastore, a metastore admin rebinds it. Keeping bindings in the UC stack makes this a one-line change.
7. Account-level principals. Grant privileges to account-level groups (account SCIM), not workspace-local groups, so grants stay valid across workspace replacement. UC grants require account-level principals anyway, but legacy workspace-local groups still show up in migrated setups.

### After a workspace destruction

Attach a replacement workspace to the same metastore, bind the catalog to it, and everything (metadata, grants, lineage, data) is where you left it. The only account-level dependency is that you need at least one workspace attached to the metastore to administer UC objects, which is another argument for the admin workspace in point 5.

Sources (structure and naming worth verifying against current docs, both real):
- https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/
- https://docs.databricks.com/aws/en/data-governance/unity-catalog/best-practices

If you want, I can run a source check on the version-sensitive claims (managed location resolution order, automatic enablement behaviour, binding semantics) with the reviewing-tech-claims skill.