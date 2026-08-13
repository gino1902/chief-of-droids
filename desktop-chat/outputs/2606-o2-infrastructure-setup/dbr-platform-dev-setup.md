# Databricks dev platform setup

One path from the provisioned dev workspace to a governed bronze table that a
group member reads. Dev only. Cut from
[[dbr-platform-foundation-setup]], which stays as the reference.

Done means: an automated identity writes a table in `sqli_bronze_dev.raw`, and a
member of `SGA-RG-DATABRICKS-DEV` who did not create it reads that table.

## Fixed values

| | |
| :--- | :--- |
| Profile | `adb-7405605180591006` |
| Workspace | `https://adb-7405605180591006.6.azuredatabricks.net` |
| Subscription | `cbd4be67-d777-4841-bbf4-44d3c74d447d` |
| Resource group | `RG-DATABRICKS-DEV` |
| Region | `francecentral` |
| Metastore | `metastore_azure_francecentral`, no `storage_root` |
| Enforced tag keys | `owner`, `environment`, `cost_center`, `project` |
| Admin group | `SGA-RG-DATABRICKS-DEV` |
| Storage account | `stdbrmanagedfrasqlidev`, container `managed` |
| Catalog and schema | `sqli_bronze_dev`.`raw` |

Change the last two if your naming differs. Everything else is read from the
platform.

## Not yours to run

Raise these on day one. They have other people's lead times.

- **Storage account and container**, step 5. Platform engineer, through Terraform.
- **Storage Blob Data Contributor on the container**, step 7. Needs Owner or User
  Access Administrator. This is the one that failed on 2026-08-11.
- **A durable access connector and storage credential**, step 7. Platform
  engineer. The workspace's own connector is unreadable from here.
- **OIDC federation policy on the CI principal**, step 4. Databricks account
  admin.
- **Any Entra group that does not exist**, step 8. Entra admin. Groups are never
  created in Databricks.

## Before you start

```bash
az login
az account set --subscription cbd4be67-d777-4841-bbf4-44d3c74d447d
databricks auth login --host https://adb-7405605180591006.6.azuredatabricks.net
```

```bash
P=adb-7405605180591006
RG=RG-DATABRICKS-DEV
SUB=cbd4be67-d777-4841-bbf4-44d3c74d447d
SA=stdbrmanagedfrasqlidev
CAT=sqli_bronze_dev
GRP=SGA-RG-DATABRICKS-DEV
```

Every write is checked by reading it back, never by the command not erroring. A
first negative read can be too early. Read again before concluding anything.

---

## 1. Read metastore root storage

Decides whether step 11 must name a location for every catalog.

```bash
databricks -p "$P" metastores summary
```

Pass: `storage_root` is absent. If present, stop. Every catalog created without
an explicit location would land in a storage account belonging to the shared
metastore, and clearing the root is an account admin action affecting other
people's catalogs.

## 3. Read what Azure will refuse

Gets the tag keys step 17 has to match, and confirms the providers step 5 needs.

```bash
SCOPE="/subscriptions/$SUB/resourceGroups/$RG"

az policy assignment list --scope "$SCOPE" --disable-scope-strict-match --query "[].{name:name, policy:policyDefinitionId, enforcement:enforcementMode, params:parameters}" -o json

az provider show -n Microsoft.Storage --query registrationState -o tsv
az provider show -n Microsoft.EventGrid --query registrationState -o tsv
```

Pass: you can name every deny-effect policy and its `enforcementMode`, you can
name the scopes you could not read, and both providers say `Registered`.

Take tag keys from each assignment's `tagName` parameter, not from its name. A
`deny` policy set to `DoNotEnforce` marks resources non-compliant and blocks
nothing, so an apply succeeding proves nothing about the tags.

You hold Contributor on one resource group, so assignments above it do not
return. Unreadable is an acceptable answer. Unknown is not.

## 4. Create the CI principal

The identity the automated write at step 23 runs as.

Kind is fixed at creation. No `applicationId` gives a Databricks managed
principal, an existing Entra application ID gives an Entra managed one. Use
Databricks managed.

```bash
databricks -p "$P" service-principals list -o json

databricks -p "$P" service-principals create --json '{"displayName":"SP-CICD-fra-sqli-dev","active":true}'

databricks -p "$P" service-principals get <scim-id>
```

Pass: `displayName` reads back as you set it, and `groups` is empty. Read again
after ten minutes, because an automation rule can add `admins` on a delay.

Keep it out of every group. Group membership comes from Entra and a Databricks
managed principal cannot join an Entra group, so its access is a direct grant at
step 13.

Deleting a principal stops its compute, fails its jobs and breaks anything shared
with Run as Owner. Deactivate instead.

The federation policy is account-level and needs an account admin, protected
branches on the GitLab project, and a real CI token decoded for its `iss` and
`sub`. Do not write a policy against GitLab's documented claim format. Read the
claims off a live token.

## 5. Create the storage account

Where the managed tables of every catalog physically live. Not a landing zone,
nothing writes files here directly.

It needs its own Terraform state. If `terraform destroy` on the workspace can
reach this account, the first workspace rebuild takes your data.

```hcl
resource "azurerm_storage_account" "managed" {
  name                     = "stdbrmanagedfrasqlidev"
  resource_group_name      = var.resource_group_name
  location                 = "francecentral"
  account_kind             = "StorageV2"
  account_tier             = "Standard"
  account_replication_type = "ZRS"
  is_hns_enabled           = true

  tags = {
    owner       = var.owner
    environment = "dev"
    cost_center = var.cost_center
    project     = var.project
  }
}

resource "azurerm_storage_container" "managed" {
  name                  = "managed"
  storage_account_id    = azurerm_storage_account.managed.id
  container_access_type = "private"
}
```

```bash
az storage account show -g "$RG" -n "$SA" --query "{hns:isHnsEnabled, repl:sku.name, tags:tags}" -o json
az storage container list --account-name "$SA" --auth-mode login --query "[].name" -o tsv
```

Pass: `isHnsEnabled` is `true`, all four tags are present, the container is
listed.

`is_hns_enabled` and the tags must be set at creation. The hierarchical namespace
can be added afterwards only by a one-way upgrade that disables writes while it
runs. Leave public network access alone.

## 7. Register the external location

A `MANAGED LOCATION` must sit inside an external location. That is the only
reason this exists.

Needs first, from the platform engineer: an access connector in a resource group
you control, and **Storage Blob Data Contributor** on the container for that
connector's identity. Nothing else. The queue, storage account and EventGrid
roles exist for file events, which this platform does not use.

```bash
databricks -p "$P" storage-credentials create --json '{"name":"sc-managed-dev","azure_managed_identity":{"access_connector_id":"<connector-resource-id>"}}'

databricks -p "$P" external-locations create --json '{"name":"el-managed-dev","url":"abfss://managed@stdbrmanagedfrasqlidev.dfs.core.windows.net/","credential_name":"sc-managed-dev"}'

databricks -p "$P" external-locations get el-managed-dev
```

Pass: the external location reads back, and this returns without error on a
warehouse:

```sql
LIST 'abfss://managed@stdbrmanagedfrasqlidev.dfs.core.windows.net/'
```

A `LIST` that fails on permissions is the role assignment missing, not the
external location.

## 8. Pull the Entra group into the workspace

Never create a group in Databricks. A group created there is a second source of
truth that nothing reconciles.

```bash
az ad group show --group "$GRP" --query "{name:displayName, id:id, onPremSync:onPremisesSyncEnabled}"
az ad group member list --group "$GRP" --query "[].{name:displayName, upn:userPrincipalName}" -o table
```

Then pull it in through Settings, Identity and access, Manage next to Groups. The
picker searches Entra. Use it to add, never to create.

```bash
databricks -p "$P" groups list -o json
```

Pass: the group is present, and its membership is not editable inside Databricks.
Editable membership means it was created there, which is a fail.

`onPremisesSyncEnabled` true means every membership change is a ticket to whoever
owns the on-premises directory.

## 9. Assign entitlements to the group

A group pulled in at step 8 cannot be used for anything workspace-scoped until
this is done. Entitlements are no longer inherited from `users` or `admins`.

Settings, Identity and access, Groups, the group, Entitlements. Or:

```bash
databricks -p "$P" groups patch <group-id> --json '{"schemas":["urn:ietf:params:scim:api:messages:2.0:PatchOp"],"Operations":[{"op":"add","path":"entitlements","value":[{"value":"workspace-access"},{"value":"databricks-sql-access"}]}]}'

databricks -p "$P" groups get <group-id>
```

Pass: `entitlements` reads back with both values.

Defaults are not minimal. Strip what is not needed rather than assuming the
default is least privilege.

## 11. Create the catalog

```bash
databricks -p "$P" catalogs create --json '{"name":"sqli_bronze_dev","storage_root":"abfss://managed@stdbrmanagedfrasqlidev.dfs.core.windows.net/sqli_bronze_dev"}'

databricks -p "$P" catalogs get "$CAT"
```

Pass: `storage_root` reads back as the path you set. Absent means it fell back to
something you did not choose.

Setting it needs `CREATE MANAGED STORAGE` on the external location, which is a
different privilege from `CREATE CATALOG` and belongs to whoever created the
external location at step 7.

Changing the location later does not move tables that already exist. Adjustable
on an empty catalog, not adjustable one table in.

## 12. Create the schema, then write to it

This is the checkpoint. Everything after it assumes the storage path works.

```bash
databricks -p "$P" schemas create --json '{"name":"raw","catalog_name":"sqli_bronze_dev"}'
```

The schema existing proves nothing. Run this on a warehouse, from step 19, which
you may need to bring forward for this check alone:

```sql
CREATE TABLE sqli_bronze_dev.raw.probe (id INT);
INSERT INTO sqli_bronze_dev.raw.probe VALUES (1);
SELECT * FROM sqli_bronze_dev.raw.probe;
DROP TABLE sqli_bronze_dev.raw.probe;
```

Pass: the row comes back. Failure here unwinds step 11 alone. Finding out at step
23 unwinds everything.

Do not give the schema its own `MANAGED LOCATION`. It overrides the catalog's and
silently redirects files.

## 13. Grants

Nothing this sequence creates is readable by default. Reading one table needs
`USE CATALOG`, `USE SCHEMA` and `SELECT`, and none substitutes for another.

People, through the group:

```sql
GRANT USE CATALOG ON CATALOG sqli_bronze_dev TO `SGA-RG-DATABRICKS-DEV`;
GRANT USE SCHEMA ON SCHEMA sqli_bronze_dev.raw TO `SGA-RG-DATABRICKS-DEV`;
GRANT SELECT ON SCHEMA sqli_bronze_dev.raw TO `SGA-RG-DATABRICKS-DEV`;
```

The CI principal, directly, by its application ID:

```sql
GRANT USE CATALOG ON CATALOG sqli_bronze_dev TO `178e0409-b9d4-43f8-93c7-3b3e29ef0326`;
GRANT USE SCHEMA ON SCHEMA sqli_bronze_dev.raw TO `178e0409-b9d4-43f8-93c7-3b3e29ef0326`;
GRANT CREATE TABLE, MODIFY, SELECT ON SCHEMA sqli_bronze_dev.raw TO `178e0409-b9d4-43f8-93c7-3b3e29ef0326`;
```

```sql
SHOW GRANTS ON SCHEMA sqli_bronze_dev.raw;
```

Pass: both principals appear with the privileges above.

Also decide the workspace catalog here. It arrived with every workspace user
holding `USE CATALOG` and create rights on its `default` schema. Close it, keep
it or delete it, and say which. Leaving it alone is the decision that leaves it
open.

## 17. Compute policy with enforced tags

Nothing else enforces a tag on Databricks compute. The Azure policies do not
reach it.

```bash
databricks -p "$P" cluster-policies create --json '{
  "name": "dev-tagged",
  "definition": "{\"custom_tags.owner\":{\"type\":\"fixed\",\"value\":\"<you>\"},\"custom_tags.environment\":{\"type\":\"fixed\",\"value\":\"dev\"},\"custom_tags.cost_center\":{\"type\":\"fixed\",\"value\":\"<cc>\"},\"custom_tags.project\":{\"type\":\"fixed\",\"value\":\"<proj>\"}}"
}'

databricks -p "$P" cluster-policies list -o json
```

Pass: the policy reads back with all four tags fixed.

It does not cover SQL warehouses. Warehouse tags are set at step 19 and nothing
enforces them. Compute created before this policy stays untagged for good,
including the provisioned starter warehouse.

## 19. Create the warehouse

```bash
databricks -p "$P" warehouses create --json '{"name":"wh-dev","cluster_size":"2X-Small","warehouse_type":"PRO","enable_serverless_compute":true,"auto_stop_mins":10,"tags":{"custom_tags":[{"key":"owner","value":"<you>"},{"key":"environment","value":"dev"},{"key":"cost_center","value":"<cc>"},{"key":"project","value":"<proj>"}]}}'

databricks -p "$P" warehouses set-permissions <warehouse-id> --json '{"access_control_list":[{"group_name":"SGA-RG-DATABRICKS-DEV","permission_level":"CAN_USE"}]}'

databricks -p "$P" warehouses get <warehouse-id>
```

Pass: the warehouse reads back with its four tags, and the group holds `CAN_USE`.

For serverless from the API you must set `warehouse_type` to `PRO` **and**
`enable_serverless_compute` to `true`. The API default is classic, unlike the UI.

`CAN USE` both starts the warehouse and runs queries. `CAN MONITOR` does the same
despite reading as observational, so it is the wrong grant for anyone who should
only look.

Delete or tag the provisioned `Serverless Starter Warehouse`. It is untagged and
step 17 cannot reach back to fix it.

## 23. Acceptance test

Two identities, and neither of them is you. Every earlier check passed for a
workspace admin who owns what they created, so not one of them tested a grant.

The write, as the CI principal, from the repo rather than the UI:

```sql
CREATE TABLE sqli_bronze_dev.raw.acceptance (id INT, loaded_at TIMESTAMP);
INSERT INTO sqli_bronze_dev.raw.acceptance VALUES (1, current_timestamp());
```

The read, as a member of `SGA-RG-DATABRICKS-DEV` who did not create it, on their
own credentials:

```sql
SELECT * FROM sqli_bronze_dev.raw.acceptance;
```

Pass: both. Either can pass while the other fails.

## When it fails

| What you see | Where it broke |
| :--- | :--- |
| Storage authorisation error on write | Step 7, the connector identity lacks Storage Blob Data Contributor |
| Pipeline cannot write the table | Step 11 or 12, no usable managed location, or the external location is missing |
| Table created but the group cannot see the catalog | Step 13, `USE CATALOG` missing |
| Catalog visible but the table is not | Step 13, `USE SCHEMA` missing |
| Table visible but the query is denied | Step 13, `SELECT` missing |
| Group member has no warehouse to run on | Step 19, no `CAN USE` |
| Group member cannot open the SQL editor at all | Step 9, `databricks-sql-access` not assigned |
| Works for you, fails for them | You are a workspace admin. Test on their credentials or you are testing nothing |

## Not verified

Three commands here are written from the API shape rather than checked against
the documentation. Expect to adjust them.

- `groups patch` at step 9. The UI path is certain, the SCIM patch body is not.
- `cluster-policies create` at step 17, specifically the escaped `definition`
  string.
- `azurerm_storage_container.storage_account_id` at step 5. That is azurerm v4
  syntax. On v3 it is `storage_account_name`.

<!--
Version: 0.1 | Last Updated: 2026-08-13 | Status: Draft
-->
