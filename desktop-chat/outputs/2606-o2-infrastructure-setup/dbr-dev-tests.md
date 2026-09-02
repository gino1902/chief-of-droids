# Databricks dev tests

One entry per test. What it needs, what is being tested, the play, what passes,
and what passing means. Run them in the order given, because the later ones
depend on objects the earlier ones create.

## Terms

Enough to read the tests. Each of these appears below without further
explanation.

| Term | What it is |
| :--- | :--- |
| Unity Catalog | The governance layer that owns catalogs, schemas, tables and the grants on them. It sits outside any single workspace. |
| Metastore | The account-level registry holding those definitions. This workspace shares one with other tenants, which is why isolation matters. |
| Catalog | The top level of a data namespace. A catalog holds schemas, a schema holds tables. |
| Schema | A group of tables inside a catalog. What most databases call a database. |
| Binding | The list of workspaces allowed to reach a catalog. A separate object from the catalog itself. |
| SQL warehouse | Managed compute that runs SQL. One must be running for any query below to return. |
| Bundle (DAB) | A folder of YAML plus code that the CLI deploys to a workspace. `databricks.yml` is its root file. |
| Target | One named deployment of a bundle, for example `dev` or `staging`. Targets can point at different catalogs. |
| Service principal | A non-human identity. It owns nothing and holds no privilege until one is granted. |
| Storage credential | The identity Unity Catalog uses to reach Azure storage, backed here by an access connector. |
| External location | A storage path Unity Catalog is allowed to use, paired with a credential. |
| Cluster policy | A rule set applied whenever compute is created. Used here to force tags onto it. |
| Lakeflow pipeline | A managed job that keeps derived tables up to date. Formerly Delta Live Tables. The module is now `pyspark.pipelines`, imported as `dp`. `dlt` still works and is no longer recommended. |

## Values

Two kinds of placeholder. The first table is what you are given, substitute
before running anything. The second is what a command hands back to you part way
through a test.

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
| `<warehouse-id>` | `ca24aadb34697d64` (the existing warehouse the queries below run on) |
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

Produced as you go. Read each from the output of the command named.

| Placeholder | Where it comes from |
| :--- | :--- |
| `<policy-id>` | Returned by `cluster-policies create`. |
| `<warehouse-id-new>` | Returned by `warehouses create` in the tagging test. Not the same warehouse as `<warehouse-id>`. |
| `<pipeline-id>` | Returned by `pipelines create`. |
| `<job-id>` | From `databricks -p <profile> jobs list`. |
| `<group-id>` | The Databricks group id from `groups list`, not the Entra object id. |
| `<runner-token>` | The `glrt-` token from GitLab, Settings, CI/CD, Runners. |
| `<client-id>`, `<client-secret>`, `<refresh-token>` | From the Entra app registration. See the SharePoint test. |

## Sign in

```bash
az login
az account set --subscription <subscription>
databricks auth login --host <host>
```

Every test below assumes this is done and that you hold workspace admin.

---

## Check what the platform will refuse before building on it

Needs: read access to the workspace and to `<rg>`. Nothing is created or
changed.

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

This tells you which tags every resource you create in that group must carry.
Miss one and the policy
refuses the request with `403` before it reaches the resource provider, unless
`enforcementMode` reads `DoNotEnforce`, in which case the create succeeds and the
resource is quietly marked non-compliant instead.

Take the keys from each assignment's `tagName` parameter rather than its name,
because the name is a label someone chose.

Assignments above the resource group do not appear unless you can read that
scope. Unreadable is an acceptable answer, unknown is not.

```bash
az provider show -n Microsoft.Storage --query registrationState -o tsv
az provider show -n Microsoft.EventGrid --query registrationState -o tsv
```

Both must read `Registered` or the storage entry fails at its first create.

Pass: you can state the `storage_root`, the tag keys, the enforcement mode, the
scopes you could not read, and both provider states.

Means: you can say where new data lands by default, which tags Azure will insist
on, and whether the storage tests can run at all. Without these three answers
the later tests fail on surprises instead of on real problems.

## Check an isolated catalog is still reachable

Needs: workspace admin. This one changes live configuration, so run it against
`<catalog>` and nothing else.

On a shared metastore every other tenant's workspace can see your catalogs, so
you set them `ISOLATED`. That does not bind your own workspace: the binding list
is a separate object, and an empty one means no workspace at all, including
yours. Get this wrong and you lock yourself out of your own data.

```bash
databricks -p <profile> catalogs update <catalog> --json '{"isolation_mode":"ISOLATED"}'
databricks -p <profile> workspace-bindings get-bindings catalog <catalog>
```

Expected: no binding for `<workspace-id>`.

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

Pass: the statement returns `"state": "SUCCEEDED"` rather than erroring. An empty
catalog lists no schemas and still passes.

- `catalogs get` works throughout. It reads the metastore, which is not
  workspace-scoped, so only a query tells you whether compute can reach the
  catalog.
- Isolation is between workspaces, never between catalogs. Grants separate
  catalogs.

Means: other tenants on the shared metastore cannot reach your data and your own
workspace still can. A catalog set to isolated with no binding is unreachable by
everyone, yourself included.

## Check the same code deploys to two targets

Needs: workspace admin and a local clone of the `<bundle>` repo. Work inside
that repo, not in a scratch directory.

Dev and staging run the same source tree against different catalogs. What breaks
that is `mode: development`, which prefixes every resource name, schemas
included. A target without a mode does not, so anything hardcoding a name works
in one target and fails in the other.

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

Means: one source tree serves dev and staging with no manual edit between them.
Promoting to staging cannot carry a dev-only name along with it.

## Check the CI pipeline can authenticate without a secret

Needs: Maintainer on the GitLab project, and a machine that can run a GitLab
runner. No Databricks account admin yet, that is the next test.

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

Means: the pipeline holds no Databricks secret anywhere. The error it returns is
the exact federation policy to request, so the ask you send the account admin is
precise rather than approximate.

## Check a grant is enforced against someone who owns nothing

Needs: workspace admin, plus the UI step below before the deploy will work.

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

Means: access is decided by grants rather than by ownership. Whatever you can
read as yourself tells you nothing about what a colleague or a job can read.

## Check managed tables can live on storage you own

Needs: Contributor on `<rg>` for the creates, and Owner or User Access
Administrator for the role assignment. Those are usually two different people,
so raise the role request early.

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

Means: the data outlives the workspace. Delete or rebuild the workspace and the
tables are still sitting in a resource group your team controls.

## Check tags land on compute and on warehouses

Needs: workspace admin. `<cost-center>` is still `TBD` and the policy fixes it
as a literal value, so set the real one before creating the policy or every
cluster it governs carries a wrong tag.

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
databricks -p <profile> warehouses set-permissions <warehouse-id-new> --json '{"access_control_list":[{"group_name":"<group>","permission_level":"CAN_USE"}]}'
databricks -p <profile> warehouses get <warehouse-id-new> -o json
```

Pass: the `custom_tags` read back and `<group>` holds `CAN_USE`.

It starts `RUNNING` and bills until auto-stop, so stop it when you are done:

```bash
databricks -p <profile> warehouses stop <warehouse-id-new>
```

Compute created before the policy existed stays untagged and no policy reaches
back to fix it. The provisioned starter warehouse is the usual case.

Means: compute spend can be attributed to a project and an environment. Enforced
automatically on clusters and jobs, manual on warehouses, so any warehouse
someone creates by hand will be untagged and invisible on the bill.

## Check the group came from Entra and not from Databricks

Needs: directory read in Entra and workspace admin. The pull-in step is UI only,
there is no CLI route without account admin.

Both kinds look the same in the workspace. A group created in Databricks has its
own membership list that nobody syncs, so two answers to who has access appear
and drift apart. Three fields tell you which kind you have.

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

Means: there is one membership list, held in Entra, so an access review there is
the truth. A Databricks-created group would give you a second list that nobody
syncs and that quietly drifts.

## Check a source connector exists before asking for credentials

Needs: workspace admin. Both calls are rejected, so nothing is created.

Every Lakeflow Connect source needs credentials someone else has to produce. Two
rejected calls tell you whether the connector exists on this workspace and
exactly which credentials to ask for, without setting anything up.

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

Means: you know the connector exists on this workspace and exactly which
credentials to request, before anyone starts an app registration that might turn
out to be the wrong shape.

## Check an Azure VM can reach GitLab and the workspace

Needs: access to Azure Cloud Shell. Running this from your own machine proves
nothing.

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

Means: a runner can sit in Azure and reach both endpoints outbound, so it needs
no private endpoint and no inbound rule of its own.

## Check a serverless pipeline actually runs in this region

Needs: workspace admin and a catalog you can write to.

Lakeflow Connect ingestion runs on serverless pipelines. Regional availability
tables are not always right, and a restriction bites when compute starts rather
than when you create the pipeline, so create one and run it.

`probe_pipeline.py`, three lines.

```python
# Databricks notebook source
from pyspark import pipelines as dp


@dp.materialized_view
def probe():
    return spark.range(1)
```

Updated 2026-09-02. This test was written with `import dlt` and `@dlt.table`, which still
work, so the original is not broken. `dlt` has been replaced by `pyspark.pipelines` and
Databricks recommends the new module, which is what a serverless pipeline ran on this
workspace with on 2026-09-02. The decorator changed too: `@dp.table` is for a streaming
read and `@dp.materialized_view` for a batch read, and `spark.range(1)` is a batch read.
That decorator choice is from the documentation and has not been re-run here.

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

That ownership split was confirmed again on 2026-09-02 from the other direction. Removing
a dataset from a running pipeline's source also leaves its table and rows in place, in
development mode, production mode and production mode with a full refresh. Documentation
says an omitted dataset is dropped from the target schema, and it did not happen in any of
the three. Evidence in
[`../2606-o2-architecture-design/2026-09-01-bronze-platform-tests.md`](../2606-o2-architecture-design/2026-09-01-bronze-platform-tests.md),
and the consequence for the bronze layer is in ADR-013.

Means: serverless pipelines really do run in `<region>`, so Lakeflow Connect
ingestion is buildable here rather than only on paper.

## Check the role assignment actually covers the container

Needs: the role assignment from the storage test to have been granted. This is
that test's retest, not a new one.

The role list is not proof. A role granted at storage account or resource group
scope covers the container without appearing on it, and a role on the container
can still be the wrong one. The write either works or it does not.

```bash
az role assignment list --scope "/subscriptions/<subscription>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage-account>/blobServices/default/containers/<container>" --include-inherited --query "[].{principal:principalId, role:roleDefinitionName, scope:scope}" -o table

databricks -p <profile> api post /api/2.0/sql/statements --json '{"warehouse_id":"<warehouse-id>","statement":"CREATE TABLE <catalog-own>.<schema>.probe (id INT)"}'
databricks -p <profile> tables delete <catalog-own>.<schema>.probe
```

Pass: `"state": "SUCCEEDED"` instead of `UC_CLOUD_STORAGE_ACCESS_FAILURE`.

Means: Unity Catalog can write to your container. Until this passes, every query
against `<catalog-own>` fails for everyone, admins included.

## Check the pipeline authenticates once the federation policy exists

Needs: a Databricks account admin to have created the policy from the claims the
earlier CI test printed.

A Databricks account admin writes the policy, and a wrong issuer, subject or
audience produces the same rejection as no policy at all. Only a run tells you it
took.

```bash
git commit --allow-empty -m "ci: retry"
git push
```

Pass: the `validate` job prints `Validation OK!` instead of `TOKEN_INVALID`.

Means: CI authenticates as a service principal with no stored secret. There is
nothing to rotate and nothing to leak.

## Check jobs run on the shared runner rather than yours

Needs: the shared runner to exist on a VM, built by whoever owns that VM.

Once a runner exists on a VM, your local one is still registered and will keep
picking jobs up. A green pipeline then tells you nothing about theirs.

```bash
brew services stop gitlab-runner
git commit --allow-empty -m "ci: retry on the shared runner"
git push
```

Pass: the job runs, and its first log line names their runner rather than
`mac-local`.

Means: the pipeline works for the team rather than only while your laptop is
awake and registered.

## Check the SharePoint connection can be created

Needs: an Entra admin to have created the app registration, granted admin
consent, issued the client secret and run the user OAuth flow for the refresh
token.

The app registration, its consent and its secret are all done by an Entra admin,
and the only way to know they produced the right thing is to build the connection
with them.

```bash
databricks -p <profile> connections create --json '{"name":"sharepoint","connection_type":"<connection-type>","options":{"tenant_id":"<tenant>","client_id":"<client-id>","client_secret":"<client-secret>","refresh_token":"<refresh-token>"}}'
```

`<client-id>`, `<client-secret>` and `<refresh-token>` come from the registration
and are deliberately not in the values table.

Pass: the connection is created rather than listing missing options.

Means: the credentials you were handed are the right ones and ingestion from
SharePoint can be built on them.

## Clean up

The pipeline test removes what it made. Nothing else does. Run this once the
tests have served their purpose, oldest scratch first, or the next person
inherits a bill and a set of half-configured objects.

```bash
databricks -p <profile> warehouses delete <warehouse-id-new>
databricks -p <profile> cluster-policies delete <policy-id>
databricks -p <profile> service-principals delete <sp-scim-id>
databricks -p <profile> schemas delete <catalog-own>.<schema>
databricks -p <profile> catalogs delete <catalog-own> --force
databricks -p <profile> external-locations delete el-managed-dev
databricks -p <profile> storage-credentials delete sc-managed-dev
az storage account delete -g <rg> -n <storage-account> --yes
az databricks access-connector delete -g <rg> -n <connector> --yes
```

Leave `<catalog>` and `<catalog-staging>` alone. They hold the bundle's schema
and job, which the two-target and grants tests reuse. Deleting the storage
account destroys the tables in `<catalog-own>` and there is no undo.

<!--
Version: 0.2 | Last Updated: 2026-08-27 | Status: Draft
-->