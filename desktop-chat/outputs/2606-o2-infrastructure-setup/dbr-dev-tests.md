# Databricks dev tests

One entry per test. What is being tested, the play, what passes.

## Values

Every `<placeholder>` in this document resolves here. Substitute before running
anything.

| Placeholder | Value |
| :--- | :--- |
| `<profile>` | `adb-7405605180591006` |
| `<host>` | `https://adb-7405605180591006.6.azuredatabricks.net` |
| `<workspace-id>` | `7405605180591006` |
| `<account-id>` | `58bd71ac-c13e-40ea-80d3-cc4c79aee8f1` |
| `<subscription>` | `cbd4be67-d777-4841-bbf4-44d3c74d447d` |
| `<tenant>` | `20f62116-4d0c-44ac-8a45-390ca2765601` |
| `<rg>` | `RG-DATABRICKS-DEV` |
| `<region>` | `francecentral` |
| `<catalog>` | `datawan_dev` |
| `<catalog-staging>` | `datawan_staging` |
| `<catalog-own>` | `datawan_own` |
| `<schema>` | `bronze` |
| `<bundle>` | `datawan` |
| `<user>` | `gmourgues@sqli.com` |
| `<group>` | `SGA-RG-DATABRICKS-DEV` |
| `<sp-name>` | `SP-CICD-fra-sqli-dev` |
| `<sp-app-id>` | `178e0409-b9d4-43f8-93c7-3b3e29ef0326` |
| `<sp-scim-id>` | `148154309461952` |
| `<warehouse-id>` | `ca24aadb34697d64` |
| `<storage-account>` | `stdbrmanagedfrasqlidev` |
| `<container>` | `managed` |
| `<connector>` | `ac-databricks-dev` |
| `<connector-principal>` | `bf9965b5-e9c1-4d43-8d3d-79b41e98ee3f` |
| `<connection-type>` | `SHAREPOINT` |
| `<gitlab-host>` | `gitlab-paris.sqli.com` |
| `<gitlab-project>` | `gmourgues/datawan` |
| `<owner>` | `sqli` |
| `<environment>` | `dev` |
| `<cost-center>` | `TBD` |
| `<project>` | `databricks` |
| `<tags>` | `owner=<owner> environment=<environment> cost_center=<cost-center> project=<project>` |
| `<admins-group-id>` | `155326641383371` |

## Sign in

```bash
az login
az account set --subscription <subscription>
databricks auth login --host <host>
```

Every test below assumes this is done and that you hold workspace admin.

---

## Catalog isolation without a binding

`ISOLATED` does not bind the current workspace. The binding list is a separate
object, and an empty one means no workspace at all.

```bash
databricks -p <profile> catalogs update <catalog> --json '{"isolation_mode":"ISOLATED"}'
databricks -p <profile> workspace-bindings get-bindings catalog <catalog>
```

Expected:

```json
{ "bindings": [] }
```

Query the catalog:

```bash
databricks -p <profile> api post /api/2.0/sql/statements --json '{"warehouse_id":"<warehouse-id>","statement":"SHOW SCHEMAS IN <catalog>"}'
```

Expected fail:

```
[INSUFFICIENT_PERMISSIONS] Catalog '<catalog>' is not accessible in current workspace SQLSTATE: 42501
```

Bind it, then repeat the same query:

```bash
databricks -p <profile> workspace-bindings update-bindings catalog <catalog> --json '{"add":[{"workspace_id":<workspace-id>,"binding_type":"BINDING_TYPE_READ_WRITE"}]}'
```

Pass: the statement returns `"state": "SUCCEEDED"` and lists the catalog's
schemas.

- `catalogs get` works throughout. It reads the metastore, which is not
  workspace-scoped, so only a query tells you whether compute can reach the
  catalog.
- Isolation is between workspaces, never between catalogs. Grants separate
  catalogs.

## Development mode renames the resources

`mode: development` prefixes every resource name, schemas included. A target
without a mode does not, so code that hardcodes a name works in one target and
fails in the other.

Build the bundle. `databricks.yml`:

```yaml
bundle:
  name: <bundle>

include:
  - resources/*.yml

variables:
  catalog:
    description: Catalog this target writes to

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: <host>
    variables:
      catalog: <catalog>

  staging:
    workspace:
      host: <host>
      root_path: /Workspace/Users/<sp-app-id>/.bundle/<bundle>/staging
    variables:
      catalog: <catalog-staging>
```

`resources/bronze.yml`:

```yaml
resources:
  schemas:
    bronze:
      catalog_name: ${var.catalog}
      name: <schema>

  jobs:
    bronze_load:
      name: <bundle>-bronze-load
      tasks:
        - task_key: load
          notebook_task:
            notebook_path: ../src/bronze_load.py
            base_parameters:
              catalog: ${var.catalog}
```

`src/bronze_load.py`, with the schema hardcoded, which is the mistake this test
exposes:

```python
# Databricks notebook source
dbutils.widgets.text("catalog", "")
catalog = dbutils.widgets.get("catalog")

spark.sql(f"CREATE TABLE IF NOT EXISTS {catalog}.<schema>.events (id BIGINT, label STRING, loaded_at TIMESTAMP)")
spark.sql(f"INSERT INTO {catalog}.<schema>.events VALUES (1, 'from bundle', current_timestamp())")
display(spark.sql(f"SELECT * FROM {catalog}.<schema>.events"))
```

```bash
databricks -p <profile> bundle deploy -t dev
databricks -p <profile> bundle summary -t dev
databricks -p <profile> bundle summary -t staging
```

Expected: the dev summary prefixes both the schema and the job with `dev_` and
the local part of `<user>`. The staging summary carries no prefix.

```bash
databricks -p <profile> bundle run bronze_load -t dev
```

Expected fail:

```
[SCHEMA_NOT_FOUND] The schema `<catalog>.<schema>` cannot be found. SQLSTATE: 42704
```

Fix it by passing the deployed name rather than assuming it. In
`resources/bronze.yml`, under `base_parameters`:

```yaml
              schema: ${resources.schemas.bronze.name}
```

And in the notebook, read it and use it in place of the literal:

```python
dbutils.widgets.text("schema", "")
schema = dbutils.widgets.get("schema")
```

```bash
databricks -p <profile> bundle deploy -t dev
databricks -p <profile> bundle run bronze_load -t dev
databricks -p <profile> bundle deploy -t staging
databricks -p <profile> bundle run bronze_load -t staging
```

Pass: both runs report `TERMINATED SUCCESS`, from one source tree with no edit
between them.

- `bundle validate` passed and `bundle deploy` printed `Deployment complete!`
  through every failed run above. Read `bundle summary` to know what exists, not
  the deploy's exit code.

## CI authentication over OIDC

The pipeline authenticates as a service principal with no secret anywhere. Until
a federation policy exists it cannot succeed, but it still produces the token
claims needed to write that policy.

Push the bundle repo to `https://<gitlab-host>/<gitlab-project>.git`, then give
the project a runner. In GitLab: Settings, CI/CD, Runners, New project runner,
tick **Run untagged jobs**. Copy the `glrt-` token, then:

```bash
brew install gitlab-runner
gitlab-runner register --url https://<gitlab-host> --token <runner-token>
brew services start gitlab-runner
```

Answer `shell` for the executor. The docker executor needs a daemon at
`/var/run/docker.sock`, which recent Docker Desktop no longer symlinks.

`.gitlab-ci.yml`:

```yaml
variables:
  DATABRICKS_HOST: <host>
  DATABRICKS_CLIENT_ID: <sp-app-id>
  DATABRICKS_OIDC_TOKEN_ENV: DATABRICKS_ID_TOKEN
  DATABRICKS_CONFIG_FILE: /dev/null
  DATABRICKS_AUTH_TYPE: env-oidc

default:
  before_script:
    - export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

validate:
  id_tokens:
    DATABRICKS_ID_TOKEN:
      aud: <host>
  script:
    - python3 -c "import base64,os,json; t=os.environ['DATABRICKS_ID_TOKEN'].split('.')[1]; t+='='*(-len(t)%4); print(json.dumps(json.loads(base64.urlsafe_b64decode(t)), indent=2))"
    - databricks bundle validate -t staging
```

The decode prints the payload only, never the signature, so the log carries
claims rather than a usable credential.

```bash
git add .gitlab-ci.yml
git commit -m "ci: oidc validate"
git push
```

Expected, and this is the pass while no federation policy exists:

```
Error: failed during request visitor: env-oidc auth: Post "<host>/oidc/v1/token": {"error":"invalid_grant", ... "error_description":"Failed to process token: TOKEN_INVALID (Ensure a valid federation policy has been configured). Valid federation policy for provided token: {issuer: 'https://<gitlab-host>', subject: 'project_path:<gitlab-project>:ref_type:branch:ref:main', audience: '<host>'}"}
```

Every link works and Databricks names the policy it wants. Take `iss`, `sub` and
`aud` from the decoded payload above it in the log, not from GitLab's
documentation, and send them to whoever creates the policy. Once it exists the
same push returns `Validation OK!`.

Why those two variables are in the file:

- Without `DATABRICKS_AUTH_TYPE` the CLI finds two candidates and refuses:
  `more than one authorization method configured: env-oidc and oauth`.
- `DATABRICKS_CONFIG_FILE=/dev/null` does not fix that on its own, which is how
  you know the local profile was never the second method. It is there so a shell
  runner cannot fall back to your credentials.

`DATABRICKS_OIDC_TOKEN_ENV` is the right variable name for a generic OIDC
provider. The CLI echoes it back as `oidc_token_env`.

## Run a job as a service principal to test a grant

You own everything you created here, and an owner holds every privilege on it. So
your own queries never test a grant, they only test that you are the owner.

Anyone with Contributor or Owner on the workspace's resource group is a workspace
admin too, with no Databricks group involved, and bypasses every grant the same
way. Check who that is:

```bash
az role assignment list --scope "/subscriptions/<subscription>/resourceGroups/<rg>" --include-inherited -o table
databricks -p <profile> users list -o json
```

Observed: `<group>` holds Contributor on `<rg>` and every engineer is in it, so no
human in this workspace qualifies. Use a service principal. It owns nothing,
holds nothing, and needs every privilege granted explicitly.

```bash
databricks -p <profile> service-principals create --json '{"displayName":"<sp-name>","active":true}'
databricks -p <profile> service-principals get <sp-scim-id> -o json
```

Read it back: `displayName` as you set it, `groups` empty, no entitlements. Read
again after ten minutes, because an automation rule can add `admins` on a delay
and an admin would defeat the whole test. An `externalId` on the record would
mean the principal came from Entra; its absence is the Databricks-managed
signature.

Give yourself permission to run jobs as that principal. In the workspace:
Settings, Identity and access, Service principals, `<sp-name>`, Permissions,
Grant access, `<user>`, **Service principal: User**. Creating a principal makes
you its manager, which does not include this, and the deploy fails `403
PERMISSION_DENIED` without it.

Add `run_as` to the staging target in `databricks.yml`:

```yaml
    run_as:
      service_principal_name: <sp-app-id>
```

```bash
databricks -p <profile> bundle deploy -t staging
```

Grant less than the job needs:

```bash
databricks -p <profile> grants update catalog <catalog-staging> --json '{"changes":[{"principal":"<sp-app-id>","add":["USE_CATALOG"]}]}'
databricks -p <profile> grants update schema <catalog-staging>.<schema> --json '{"changes":[{"principal":"<sp-app-id>","add":["USE_SCHEMA","SELECT"]}]}'
databricks -p <profile> bundle run bronze_load -t staging
```

Expected fail:

```
PERMISSION_DENIED: User does not have MODIFY on Table '<catalog-staging>.<schema>.events'. SQLSTATE: 42501
```

Grant the rest and rerun. No redeploy, grants are evaluated at runtime:

```bash
databricks -p <profile> grants update schema <catalog-staging>.<schema> --json '{"changes":[{"principal":"<sp-app-id>","add":["MODIFY"]}]}'
databricks -p <profile> bundle run bronze_load -t staging
```

Pass: `TERMINATED SUCCESS`. Same code, same identity, same job, one privilege
apart.

- A deploy that fails on `run_as` leaves the job on its old definition, and the
  next run goes green as the old identity. Check `jobs get <job-id>` for the `run_as`
  block, not `run_as_user_name`.
- `CREATE TABLE IF NOT EXISTS` on an existing table needs no privilege. The
  denial lands on the first statement that writes.

## Put managed tables on your own storage account

Everything on the workspace's own container dies with the workspace. This puts
managed tables on a storage account in a resource group you control.

Read the tag keys the resource group already uses. A deny policy on missing tags
will refuse the create otherwise:

```bash
az resource list -g <rg> --query "[].{name:name, tags:tags}" -o json
```

```bash
az storage account create -g <rg> -n <storage-account> -l <region> --sku Standard_ZRS --kind StorageV2 --hns true --tags <tags>
az storage container create --account-name <storage-account> -n <container> --auth-mode login

az extension add --name databricks --only-show-errors
az databricks access-connector create -g <rg> -n <connector> -l <region> --identity-type SystemAssigned --tags <tags>
az databricks access-connector show -g <rg> -n <connector> --query "identity.principalId" -o tsv
```

`--hns true` and the tags must be set at creation. Adding the hierarchical
namespace afterwards is a one-way upgrade that disables writes while it runs.

Grant the connector's identity the one role Unity Catalog needs, using the
principal id the last command returned:

```bash
az role assignment create --assignee <connector-principal> --role "Storage Blob Data Contributor" --scope "/subscriptions/<subscription>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage-account>/blobServices/default/containers/<container>"
```

Expected fail unless you hold Owner or User Access Administrator:

```
(AuthorizationFailed) ... does not have authorization to perform action 'Microsoft.Authorization/roleAssignments/write'
```

The rest needs no Azure rights, so build it now. `skip_validation` is required
because creating an external location validates it by reaching the path, which
cannot work until the role exists:

```bash
databricks -p <profile> storage-credentials create --json '{"name":"sc-managed-dev","azure_managed_identity":{"access_connector_id":"/subscriptions/<subscription>/resourceGroups/<rg>/providers/Microsoft.Databricks/accessConnectors/<connector>"}}'

databricks -p <profile> external-locations create --json '{"name":"el-managed-dev","url":"abfss://<container>@<storage-account>.dfs.core.windows.net/","credential_name":"sc-managed-dev","skip_validation":true}'

databricks -p <profile> catalogs create --json '{"name":"<catalog-own>","storage_root":"abfss://<container>@<storage-account>.dfs.core.windows.net/<catalog-own>"}'
databricks -p <profile> catalogs update <catalog-own> --json '{"isolation_mode":"ISOLATED"}'
databricks -p <profile> workspace-bindings update-bindings catalog <catalog-own> --json '{"add":[{"workspace_id":<workspace-id>,"binding_type":"BINDING_TYPE_READ_WRITE"}]}'
databricks -p <profile> schemas create --json '{"name":"<schema>","catalog_name":"<catalog-own>"}'
```

All of those pass. Now write:

```bash
databricks -p <profile> api post /api/2.0/sql/statements --json '{"warehouse_id":"<warehouse-id>","statement":"CREATE TABLE <catalog-own>.<schema>.probe (id INT)"}'
```

Expected fail:

```
[ErrorClass=INVALID_STATE.UC_CLOUD_STORAGE_ACCESS_FAILURE] Failed to access cloud storage
```

Pass: the same statement returns `"state": "SUCCEEDED"` once the role assignment
exists. Nothing else changes.

- Creating an access connector needs only Contributor. Granting it a role does
  not. Different rights, usually different people.
- Databricks never reaches storage as the caller. It authenticates as the
  connector identity, so without that role every query fails for everyone,
  admins included.
- `external-locations create` validates by reaching the path, which is why the
  role surfaces here rather than at first query.
- The role goes on the container, so it is one assignment per container. Prod
  with a container per catalog needs one each.

## Tag compute and warehouses

Databricks compute is the largest line on the bill. Untagged, you cannot say
which project or environment spent it, and the tags on your Azure resources do
not carry across.

This checks two things:

- a compute policy forces the tags your resource group requires onto every
  cluster and job created under it
- a SQL warehouse carries the same tags, but only because you set them at
  creation, since no policy reaches a warehouse

After running it you know tagging is enforced on clusters and jobs, and manual on
warehouses.

Read the tags the resource group requires rather than assuming them:

```bash
az policy assignment list --scope "/subscriptions/<subscription>/resourceGroups/<rg>" --disable-scope-strict-match --query "[].{name:name, params:parameters}" -o json
```

**The policy.**

```bash
databricks -p <profile> cluster-policies create --json '{"name":"dev-tagged","definition":"{\"custom_tags.owner\":{\"type\":\"fixed\",\"value\":\"<owner>\"},\"custom_tags.environment\":{\"type\":\"fixed\",\"value\":\"<environment>\"},\"custom_tags.cost_center\":{\"type\":\"fixed\",\"value\":\"<cost-center>\"},\"custom_tags.project\":{\"type\":\"fixed\",\"value\":\"<project>\"}}"}'
databricks -p <profile> cluster-policies get <policy-id> -o json
```

The create returns a policy id and nothing else, so the second command is the
read-back. Pass: every tag present, each `"type": "fixed"`.

**The warehouse.** `max_num_clusters` has no API default, and omitting it fails
with `0 is not a valid value` even though the UI fills it in.

```bash
databricks -p <profile> warehouses create --json '{"name":"wh-dev","cluster_size":"2X-Small","warehouse_type":"PRO","enable_serverless_compute":true,"auto_stop_mins":10,"min_num_clusters":1,"max_num_clusters":1,"tags":{"custom_tags":[{"key":"owner","value":"<owner>"},{"key":"environment","value":"<environment>"},{"key":"cost_center","value":"<cost-center>"},{"key":"project","value":"<project>"}]}}'
databricks -p <profile> warehouses set-permissions <warehouse-id> --json '{"access_control_list":[{"group_name":"<group>","permission_level":"CAN_USE"}]}'
databricks -p <profile> warehouses get <warehouse-id> -o json
```

Pass: the `custom_tags` read back and `<group>` holds `CAN_USE`.

It starts `RUNNING` and bills until auto-stop, so stop it when you are done:

```bash
databricks -p <profile> warehouses stop <warehouse-id>
```

Compute created before the policy existed stays untagged and no policy reaches
back to fix it. The provisioned starter warehouse is the usual case.

## Find out what the platform will refuse before you build on it

Three reads. They cost nothing and they decide how the later entries have to be
written. Skipping them means discovering the answers as failed applies.

```bash
databricks -p <profile> metastores summary
```

Look for `storage_root`. Absent means every catalog you create must name its own
`MANAGED LOCATION`, which is what the storage entry does. Present means a catalog
created without one silently inherits storage belonging to the shared metastore,
and your data lands somewhere you do not own.

```bash
az policy assignment list --scope "/subscriptions/<subscription>/resourceGroups/<rg>" --disable-scope-strict-match --query "[].{name:name, effect:policyDefinitionId, enforcement:enforcementMode, params:parameters}" -o json
```

This tells you which tags every `az create` must carry, and whether the policy
actually blocks anything. Take the keys from each assignment's `tagName`
parameter rather than its name, because the name is a label someone chose.
`enforcementMode: DoNotEnforce` means the policy marks resources non-compliant
and blocks nothing, so a create succeeding tells you nothing about your tags.

Assignments above the resource group do not appear unless you can read that
scope. Unreadable is an acceptable answer, unknown is not.

```bash
az provider show -n Microsoft.Storage --query registrationState -o tsv
az provider show -n Microsoft.EventGrid --query registrationState -o tsv
```

Both must read `Registered` or the storage entry fails at its first create.

Pass: you can state the `storage_root`, the tag keys, the enforcement mode, the
scopes you could not read, and both provider states.

## Get an Entra group into the workspace without creating a second one

People get access through Entra groups. If a group is created inside Databricks
instead of pulled from Entra, its membership drifts and nothing reconciles the
two, so you end up with two answers to who has access. This gets a group in and
proves which kind you got.

Read it in Entra first:

```bash
az ad group show --group <group> --query "{name:displayName, id:id, onPremSync:onPremisesSyncEnabled}"
```

`onPremisesSyncEnabled` true means the group is read-only in the cloud and every
membership change is a ticket to whoever owns the on-premises directory.

Pull it in through the UI: Settings, Identity and access, Groups, Manage, Add
group. The picker searches Entra. Use it to add, never to create. There is no CLI
route without account admin.

```bash
databricks -p <profile> groups get <group-id> -o json
```

Pass, three things together:

- `meta.resourceType` reads `Group`. A group created inside Databricks returns
  `WorkspaceGroup`, which is how you tell them apart.
- `externalId` matches the Entra object id from the first command.
- No `members` field comes back, so membership cannot be edited here. If you can
  edit it, it was created rather than pulled, which is the failure this test
  exists to catch.

Check the `entitlements` it arrived with. Observed: `workspace-access`,
`databricks-sql-access` and `workspace-consume`, none of them requested. The
default is not minimal.

## Find out what a source connector needs before requesting anything

A Lakeflow Connect source needs credentials from someone else, usually an app
registration and admin consent. Before raising that, check the connector exists
on this workspace and find out exactly which credentials it wants.

Two creates, one with a type that cannot exist. Neither creates anything, because
both are rejected:

```bash
databricks -p <profile> connections create --json '{"name":"probe-bogus","connection_type":"NOT_A_REAL_TYPE","options":{"a":"b"}}'
databricks -p <profile> connections create --json '{"name":"probe-x","connection_type":"<connection-type>","options":{"a":"b"}}'
```

The dummy `options` map matters: an empty one is rejected before the type is
checked, so both calls would return the same error and tell you nothing.

Pass: the two errors differ. A type that does not exist returns `Missing required
field: connection_type`. A real one names the options it wants.

Observed for `SHAREPOINT`:

```
CONNECTION/CONNECTION_SHAREPOINT must include the following option(s): tenant_id,client_id,client_secret,refresh_token.
```

That is the request: an Entra app registration, admin consent, a client secret,
and a user OAuth flow to mint the refresh token. Note there is no federation
option, so this route needs a secret.

## Can an Azure VM reach GitLab and the workspace

The runner polls both outbound. Test before anyone builds a VM, because the
answer decides whether it can sit in Azure at all.

```bash
dig +short <gitlab-host>
dig +short <gitlab-host> @8.8.8.8
```

Different answers mean split-horizon DNS. Observed: an RFC1918 address
internally, Cloudflare publicly, so the host is internet-facing and reachable
from outside the corporate network.

From Azure Cloud Shell, not your own machine, which takes the internal route and
proves nothing:

```bash
curl -sSI https://<gitlab-host> | head -1
curl -sSI <host> | head -1
```

Pass: any HTTP response from both. Observed `302` and `404`. A `403` means a WAF
or an IP access list. A timeout means public access is closed and the runner
needs a private endpoint of its own.

## Check a serverless pipeline actually runs in this region

Lakeflow Connect ingestion runs on serverless pipelines. Regional availability
tables are not always right, and a restriction bites when compute starts rather
than when you create the pipeline, so create one and run it.

`probe_pipeline.py`, three lines:

```python
# Databricks notebook source
import dlt


@dlt.table
def probe():
    return spark.range(1)
```

```bash
databricks -p <profile> workspace import /Users/<user>/probe_pipeline --file probe_pipeline.py --format SOURCE --language PYTHON --overwrite

databricks -p <profile> pipelines create --json '{"name":"probe-serverless","serverless":true,"catalog":"<catalog>","schema":"<schema>","libraries":[{"notebook":{"path":"/Users/<user>/probe_pipeline"}}]}'

databricks -p <profile> pipelines start-update <pipeline-id>
databricks -p <profile> pipelines get <pipeline-id> -o json | grep -E '"state"|"message"'
```

Give it a minute. Serverless pipeline startup is slower than a warehouse.

Pass: `"state": "COMPLETED"` on the update and the pipeline back to `IDLE`.
Observed 2026-08-13 in `<region>`.

```bash
databricks -p <profile> pipelines delete <pipeline-id>
databricks -p <profile> workspace delete /Users/<user>/probe_pipeline
databricks -p <profile> tables delete <catalog>.<schema>.probe
```

The last line matters. Deleting a pipeline leaves its tables behind: the pipeline
owns the definition and the refresh, Unity Catalog owns the table, so the table
is orphaned rather than dropped.

## Check the role assignment actually covers the container

Someone else grants the connector's identity its role, and they may grant it at
storage account or resource group scope rather than on the container. That works,
but it does not show up where you would look for it, so check the write rather
than the role list.

```bash
az role assignment list --scope "/subscriptions/<subscription>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage-account>/blobServices/default/containers/<container>" --include-inherited --query "[].{principal:principalId, role:roleDefinitionName, scope:scope}" -o table

databricks -p <profile> api post /api/2.0/sql/statements --json '{"warehouse_id":"<warehouse-id>","statement":"CREATE TABLE <catalog-own>.<schema>.probe (id INT)"}'
databricks -p <profile> tables delete <catalog-own>.<schema>.probe
```

Pass: `"state": "SUCCEEDED"` instead of `UC_CLOUD_STORAGE_ACCESS_FAILURE`.

## Check the pipeline authenticates once the federation policy exists

A Databricks account admin writes the policy, and a wrong issuer, subject or
audience produces the same rejection as no policy at all. Only a run tells you it
took.

```bash
git commit --allow-empty -m "ci: retry"
git push
```

Pass: the `validate` job prints `Validation OK!` instead of `TOKEN_INVALID`.

## Check jobs run on the shared runner rather than yours

Once a runner exists on a VM, your local one is still registered and will keep
picking jobs up. A green pipeline then tells you nothing about theirs.

```bash
brew services stop gitlab-runner
git commit --allow-empty -m "ci: retry on the shared runner"
git push
```

Pass: the job runs, and its first log line names their runner rather than
`mac-local`.

## Check the SharePoint connection can be created

The app registration, its consent and its secret are all done by an Entra admin,
and the only way to know they produced the right thing is to build the connection
with them.

```bash
databricks -p <profile> connections create --json '{"name":"sharepoint","connection_type":"<connection-type>","options":{"tenant_id":"<tenant>","client_id":"<client-id>","client_secret":"<client-secret>","refresh_token":"<refresh-token>"}}'
```

`<client-id>`, `<client-secret>` and `<refresh-token>` come from the registration
and are deliberately not in the values table.

Pass: the connection is created rather than listing missing options.

<!--
Version: 0.1 | Last Updated: 2026-08-13 | Status: Draft
-->
