# Databricks runbook: resource group to a working non-admin user

> One linear path from an empty Azure subscription to a named non-admin user
> running a query against a governed Unity Catalog table. Every step has one
> owner and one check. Run them in order and do not skip a check.
> Carved out of 2026-08-10-databricks-infra-setup-sequence.md, which stays as the
> design artefact and holds the reasoning this runbook deliberately omits.

Success here means bar 3. The user logs in, starts a serverless SQL warehouse, and reads a table they do not own. Bars 1 and 2, seeing the workspace and starting compute, both leave a user who has technically connected and can do nothing.

## Before you start

Four identities do the work. Get them lined up first, because two of them are hard to summon at short notice.

| Role | Needed for | Held by |
| :--- | :--- | :--- |
| Platform engineer | Steps 1 to 5 | Contributor on the subscription or resource group, plus Network Contributor on the VNet |
| Entra Global Admin | Steps 6 and 7 only | A real Microsoft Entra ID Global Administrator, needed once |
| Account admin | Steps 8 to 12, 15 to 17 | Created in step 7 |
| Test user | Step 18 | A named human who is not an admin anywhere |

Decisions already made, so the runbook does not ask again. Classic workspace with VNet injection. Premium tier. Serverless SQL warehouse for compute. A dedicated proving catalog rather than the auto-created workspace catalog, because the workspace catalog grants every workspace user `USE CATALOG` by default and would hide a broken grant chain instead of proving a working one.

---

## 1. Register the resource provider

Owner: platform engineer

```bash
az provider register --namespace Microsoft.Databricks
```

Check: `az provider show -n Microsoft.Databricks --query registrationState -o tsv` returns `Registered`. It can sit on `Registering` for a few minutes.

## 2. Create the resource group

Owner: platform engineer

```bash
az group create --name rg-o2-databricks --location <region>
```

Check: `az group show -n rg-o2-databricks --query properties.provisioningState -o tsv` returns `Succeeded`.

## 3. Create the VNet and the two subnets

Owner: platform engineer

Use a /21 VNet with a /23 host subnet and a /23 container subnet. The two subnets must be the same size and neither may be used by anything else.

```bash
az network vnet create \
  --resource-group rg-o2-databricks \
  --name vnet-o2-databricks \
  --address-prefix 10.10.0.0/21

az network vnet subnet create \
  --resource-group rg-o2-databricks --vnet-name vnet-o2-databricks \
  --name snet-host --address-prefix 10.10.0.0/23

az network vnet subnet create \
  --resource-group rg-o2-databricks --vnet-name vnet-o2-databricks \
  --name snet-container --address-prefix 10.10.2.0/23
```

Check: `az network vnet subnet list -g rg-o2-databricks --vnet-name vnet-o2-databricks -o table` lists both subnets with those prefixes.

## 4. Attach a NAT gateway to both subnets

Owner: platform engineer

Since 31 March 2026 new Azure VNets default to private with no outbound internet access, so the workspace has no egress until you give it one. Attach the gateway to both subnets, not just the host subnet, so your egress IPs are stable enough to allow-list later.

```bash
az network public-ip create -g rg-o2-databricks -n pip-o2-nat \
  --sku Standard --allocation-method Static

az network nat gateway create -g rg-o2-databricks -n nat-o2-databricks \
  --public-ip-addresses pip-o2-nat

az network vnet subnet update -g rg-o2-databricks \
  --vnet-name vnet-o2-databricks -n snet-host --nat-gateway nat-o2-databricks

az network vnet subnet update -g rg-o2-databricks \
  --vnet-name vnet-o2-databricks -n snet-container --nat-gateway nat-o2-databricks
```

Check: `az network vnet subnet show -g rg-o2-databricks --vnet-name vnet-o2-databricks -n snet-host --query natGateway.id -o tsv` returns an ID, and the same command for `snet-container` returns the same ID.

## 5. Deploy the workspace

Owner: platform engineer

Premium tier. Anything below it loses the group-based access control this runbook depends on.

Deploy by ARM template or Terraform, not by `az databricks workspace create`, because the CLI does not expose the VNet injection parameters. The deployment must set the custom VNet ID, the public subnet name (`snet-host`), the private subnet name (`snet-container`) and no-public-IP, which turns on secure cluster connectivity.

> ⚠️ Unverified. The exact ARM parameter names for VNet injection were not fetched in this pass. Check them against the VNet injection page before you write the template.

Check: the workspace URL opens, and the platform engineer lands inside as a workspace admin. Workspace creation adds the creator as a workspace admin outright, so if you see the admin settings gear, this passed.

## 6. Activate the account console

Owner: Entra Global Admin

The Global Admin signs in to https://accounts.azuredatabricks.net with their Entra credentials. Databricks creates an account admin role for them on that first sign-in. This is the only step in the runbook that needs a Global Administrator, and it happens once for the tenant.

Check: the account console loads and the sidebar shows User management.

## 7. Delegate account admin and step the Global Admin out

Owner: Entra Global Admin

In the account console, go to User management, click the user who will run the platform, open the Roles tab, and turn on Account admin. Do this for two or three people rather than one, because everything downstream is blocked without them.

Check: a delegated account admin signs in on their own credentials and sees User management. Once that passes, remove the Global Admin from the Databricks account. They do not need to come back.

## 8. Verify automatic identity management

Owner: account admin

Account console, Security, User provisioning tab. Automatic identity management is enabled by default for accounts created after 1 August 2025, so this is almost certainly a verification and not a change. If the toggle is off, turn it on and wait. Changes take five to ten minutes.

Check: the toggle reads Enabled, and typing part of a known Entra user's name into the account console search returns them.

## 9. Create the Entra group and put the test user in it

Owner: Entra admin

One group in Microsoft Entra ID. Add the named test user as a member. Do not create it in Databricks. Automatic identity management uses Entra as the source of record, so a Databricks-side group would be a second thing to maintain and could not be updated from Entra.

Check: the group appears in the account console under User management, Groups, within about ten minutes, marked as External.

## 10. Add the group to the workspace with entitlements

Owner: account admin

This is the step the whole runbook turns on, and it is the one most likely to be done wrong from memory.

Account console, Workspaces, click the workspace, Permissions tab, Add permissions. Select the Entra group. Assign the permission level `USER`, not `ADMIN`. Then assign both of these entitlements explicitly:

- Workspace access, which covers notebooks, jobs, models and pipelines
- Databricks SQL access, which covers the SQL editor, queries, dashboards and warehouses

> ⚠️ Do not rely on the `users` group to supply these. Databricks began rolling out a change on 15 June 2026 in which entitlements are granted explicitly when a principal is added to a workspace, and the `users` and `admins` system groups no longer carry assignable entitlements. It auto-enabled on 27 July 2026 for workspaces that had not opted in or out, and is enforced everywhere on 14 September 2026. A workspace created today therefore starts in the new behaviour, where the `users` group grants nothing. Older guidance that says these entitlements arrive by default is describing the old behaviour.

Check: the group is listed on the workspace Permissions tab with both entitlements shown against it.

## 11. Verify the metastore exists and the workspace is attached

Owner: account admin

Account console, Workspaces, and read the Metastore column on your workspace's row.

Check: a metastore name is present in that column. If it is, skip step 12 and go to step 13.

> ⚠️ The setup sequence doc states the metastore is auto-created for a new account. The Azure docs do not support that as written. What is documented is that new workspaces have been automatically enabled for Unity Catalog since 9 November 2023, which covers attachment to a metastore that already exists in the region. No page states that the metastore itself is created automatically in a region that has none, and the create-metastore page still addresses exactly that case. Treat this step as a real check with a real chance of failing, not a formality.

## 12. Create the metastore and assign the workspace

Owner: account admin

Only if the Metastore column in step 11 was empty.

Account console, Catalog, create a metastore in the workspace's region. Then open the metastore, Workspaces tab, Assign to workspace, select the workspace, Assign, and confirm with Enable.

Check: run `SELECT CURRENT_METASTORE();` from the SQL editor in the workspace. It returns a metastore ID. Do the same check even if you skipped this step, because it is the only check that proves attachment from inside the workspace rather than from the console.

## 13. Create the SQL warehouse

Owner: workspace admin

In the workspace, SQL Warehouses, Create SQL warehouse. Serverless. Size small is enough to prove the path.

Check: start it and wait for the state to read Running.

## 14. Grant the group CAN USE on the warehouse

Owner: workspace admin

On the warehouse row, open the kebab menu, click Permissions, select the Entra group, and assign Can use. Can view is not enough, because those users cannot run queries. Can manage is more than the group needs.

Check: the Permissions dialog lists the group with Can use against it.

## 15. Create the proving catalog and schema

Owner: account admin

Run this from the SQL editor on the warehouse from step 13. Creating a catalog needs `CREATE CATALOG` on the metastore. An account admin can grant privileges directly on a metastore, so an account admin can give themselves this if the statement is refused.

```sql
CREATE CATALOG IF NOT EXISTS o2_proving;
CREATE SCHEMA IF NOT EXISTS o2_proving.demo;
```

Check: both statements succeed, and `o2_proving` appears in the Catalog explorer with a `demo` schema under it. No workspace binding step is needed. Catalogs are open to every workspace on the metastore by default, and this one was not created as a workspace catalog.

## 16. Create the table the user will read

Owner: account admin

```sql
CREATE TABLE IF NOT EXISTS o2_proving.demo.connectivity_check
  (checked_on DATE, note STRING);

INSERT INTO o2_proving.demo.connectivity_check
  VALUES (current_date(), 'runbook proof row');
```

Check: `SELECT * FROM o2_proving.demo.connectivity_check;` returns one row for the account admin.

## 17. Grant the read chain to the group

Owner: account admin

Three privileges, one statement, granted at catalog level so it covers current and future schemas and tables underneath.

```sql
GRANT USE CATALOG, USE SCHEMA, SELECT ON CATALOG o2_proving TO `<entra-group-name>`;
```

All three are required and none substitutes for another. `SELECT` alone on the table is not enough to read it without `USE CATALOG` on the parent catalog and `USE SCHEMA` on the parent schema. Backtick the group name if it contains a hyphen. Underscores do not need backticks.

Check: `SHOW GRANTS ON CATALOG o2_proving;` lists the group three times, once for each privilege.

## 18. The user logs in and does work

Owner: the named test user, on their own credentials, unassisted

They open the workspace URL, sign in with Entra, open the SQL editor, select the warehouse, and run:

```sql
SELECT * FROM o2_proving.demo.connectivity_check;
```

Check: the row comes back. That is the whole runbook proved end to end. If it does, the identity chain, the workspace assignment, the entitlements, the warehouse permission, the metastore attachment and the grant chain are all working, because a failure in any one of them stops this query.

---

## When it fails at step 18

Read the error rather than re-running the earlier steps.

| What the user sees | Where it actually broke |
| :--- | :--- |
| Cannot sign in, or no workspace listed | Step 10, the group is not assigned to the workspace |
| Signs in but the SQL editor is missing | Step 10, the Databricks SQL access entitlement was not assigned |
| SQL editor opens but no warehouse is selectable | Step 14, the group has no Can use on the warehouse |
| Warehouse runs but the catalog is invisible | Step 17, `USE CATALOG` is missing |
| Catalog visible, table not | Step 17, `USE SCHEMA` is missing |
| Table visible, query denied | Step 17, `SELECT` is missing |

## Scope

Deliberately not here: the GitLab CI/CD service principal, which has its own note, the governance model, catalog design beyond the one proving catalog, Private Link, exfiltration controls, multi-region, and ADLS Gen2 with storage credentials and external locations. Step 15 creates a managed catalog on metastore root storage, so no external storage is needed to reach bar 3.

## Sources

Verified against Microsoft Learn on 2026-08-10. Steps 1 to 5 and 6 to 8 restate the setup sequence doc, which carries its own per-claim verification. Steps 10, 13 to 14 and 15 to 17 were verified for this runbook, because the two existing notes stop at identity and cover none of them.

- Workspace entitlements, exact names, and the 15 June 2026 change to system group entitlements: https://learn.microsoft.com/en-us/azure/databricks/security/auth/entitlements
- SQL warehouse permission levels, Can use for running queries: https://learn.microsoft.com/en-us/azure/databricks/compute/sql-warehouse/create
- Access control ACL tables for warehouses, compute and notebooks: https://learn.microsoft.com/en-us/azure/databricks/security/auth/access-control/
- First account admin, Global Admin first sign-in, delegation: https://learn.microsoft.com/en-us/azure/databricks/admin/admin-concepts
- Automatic identity management, default on after 1 August 2025, Entra as source of record: https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/automatic-identity-management/
- Groups, workspace assignment via the Permissions tab, USER and ADMIN levels: https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-groups
- Metastore verification, CURRENT_METASTORE, account console Metastore column: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/setup-uc
- Enabling a workspace for Unity Catalog, assign to workspace steps: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/enable-workspaces
- Creating a metastore, and the case where a region has none: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/create-metastore
- Privilege model, USE CATALOG plus USE SCHEMA plus SELECT all required, inheritance: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/access-control/permissions-concepts
- Privileges reference, per-privilege definitions: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/access-control/privileges-reference
- Who can grant, GRANT syntax: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/
- Principal syntax and backticking rules: https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-principal
- Creating a catalog, CREATE CATALOG on the metastore: https://learn.microsoft.com/en-us/azure/databricks/catalogs/create-catalog
- Catalogs open to all workspaces by default: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/access-control/workspace-catalog-binding
- VNet injection, subnet floor, NAT gateway and the 31 March 2026 egress default: https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/vnet-inject

<!--
Version: 1.0 | Last Updated: 2026-08-10 | Status: Draft
-->
