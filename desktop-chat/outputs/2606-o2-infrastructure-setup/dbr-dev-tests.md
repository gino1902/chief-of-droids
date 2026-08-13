# Databricks dev tests

One entry per test. What is being tested, the play, what passes.

## Setup

```bash
P=adb-7405605180591006
RG=RG-DATABRICKS-DEV
SUB=cbd4be67-d777-4841-bbf4-44d3c74d447d
```

```bash
az login
az account set --subscription "$SUB"
databricks auth login --host https://adb-7405605180591006.6.azuredatabricks.net
```

---

## Catalog isolation without a binding

`ISOLATED` does not bind the current workspace. The binding list is a separate
object, and an empty one means no workspace at all.

```bash
databricks -p "$P" catalogs update <catalog> --json '{"isolation_mode":"ISOLATED"}'
databricks -p "$P" workspace-bindings get-bindings catalog <catalog>
```

Query it from compute. Expected fail:

```
[INSUFFICIENT_PERMISSIONS] Catalog '<catalog>' is not accessible in current workspace SQLSTATE: 42501
```

```bash
databricks -p "$P" workspace-bindings update-bindings catalog <catalog> --json '{"add":[{"workspace_id":7405605180591006,"binding_type":"BINDING_TYPE_READ_WRITE"}]}'
```

Pass: the same query succeeds, no redeploy, no code change.

- `catalogs get` works throughout. It reads the metastore, which is not
  workspace-scoped, so only a query tells you whether compute can reach the
  catalog.
- Isolation is between workspaces, never between catalogs. Grants separate
  catalogs.

## Development mode renames the resources

`mode: development` prefixes every resource name, schemas included. A target
without a mode does not.

```bash
databricks -p "$P" bundle summary -t dev
databricks -p "$P" bundle summary -t staging
```

Observed: schema `bronze` deployed as `dev_gmourgues_bronze` in dev, `bronze` in
staging. The job carried a `[dev gmourgues]` prefix in dev only.

Hardcoding the name fails in one target:

```
[SCHEMA_NOT_FOUND] The schema `datawan_dev.bronze` cannot be found. SQLSTATE: 42704
```

Fix, in the job's `base_parameters`:

```yaml
              schema: ${resources.schemas.bronze.name}
```

Pass: the same source tree deploys and runs against both targets with no edit
between them.

## A successful deploy does not mean a usable resource

`bundle validate` accepted a `resources.schemas` block and `bundle deploy`
printed `Deployment complete!`, twice, while the run that needed that schema
failed.

```bash
databricks -p "$P" bundle summary -t <target>
```

Pass: `bundle summary` names every resource with the name it actually has. Treat
it as the read-back, not the deploy's exit code.

## Make the CI prove the federation gap

A pipeline that cannot authenticate still produces the token claims an account
admin needs, and Databricks names the policy it wants in its rejection.

```yaml
variables:
  DATABRICKS_HOST: https://<workspace>.azuredatabricks.net
  DATABRICKS_CLIENT_ID: <service principal application id>
  DATABRICKS_OIDC_TOKEN_ENV: DATABRICKS_ID_TOKEN
  DATABRICKS_CONFIG_FILE: /dev/null
  DATABRICKS_AUTH_TYPE: env-oidc

validate:
  id_tokens:
    DATABRICKS_ID_TOKEN:
      aud: https://<workspace>.azuredatabricks.net
  script:
    - python3 -c "import base64,os,json; t=os.environ['DATABRICKS_ID_TOKEN'].split('.')[1]; t+='='*(-len(t)%4); print(json.dumps(json.loads(base64.urlsafe_b64decode(t)), indent=2))"
    - databricks bundle validate -t staging
```

The decode prints the payload only, never the signature.

Three errors in order, each a step forward:

1. `more than one authorization method configured: env-oidc and oauth`.
   `DATABRICKS_AUTH_TYPE` names the one to use. `DATABRICKS_CONFIG_FILE=/dev/null`
   alone does not fix it, which is how you know the profile file was never the
   second method.
2. `invalid_grant … TOKEN_INVALID (Ensure a valid federation policy has been
   configured)`, quoting the issuer, subject and audience it expects. This is the
   pass.
3. Green, once the policy exists.

- `DATABRICKS_OIDC_TOKEN_ENV` is the right variable name for a generic OIDC
  provider. The CLI echoes it back as `oidc_token_env`.
- A shell executor runs as you, with your credentials on disk, so a green
  pipeline can prove nothing. A runner with no profile on it is the only real
  answer.

## Prove a grant, in both directions, with no second person

An owner holds every privilege implicitly, so nothing they run tests a grant. The
identity that owns nothing does not have to be human: a Databricks managed
service principal with no groups and no entitlements already is one.

```yaml
    run_as:
      service_principal_name: <application id>
```

Grant less than the job needs, run, grant the rest, run again. No redeploy
between, grants are evaluated at runtime.

```bash
databricks -p "$P" grants update catalog <catalog> --json '{"changes":[{"principal":"<application id>","add":["USE_CATALOG"]}]}'
databricks -p "$P" grants update schema <catalog>.<schema> --json '{"changes":[{"principal":"<application id>","add":["USE_SCHEMA","SELECT"]}]}'
databricks -p "$P" bundle run <job> -t <target>
```

Expected fail, and the pass condition for the first half:

```
PERMISSION_DENIED: User does not have MODIFY on Table '<catalog>.<schema>.events'. SQLSTATE: 42501
```

```bash
databricks -p "$P" grants update schema <catalog>.<schema> --json '{"changes":[{"principal":"<application id>","add":["MODIFY"]}]}'
databricks -p "$P" bundle run <job> -t <target>
```

Pass: green. Same code, same identity, same job, one privilege apart.

- `run_as` needs the `servicePrincipal.user` role on the principal. Creating a
  principal makes you its manager, which is not the same thing, and the deploy
  fails `403 PERMISSION_DENIED` until you add it under the principal's
  Permissions tab.
- A deploy that fails on `run_as` leaves the job on its old definition, and the
  next run goes green as the old identity. Check `jobs get <id>` for the `run_as`
  block, not `run_as_user_name`.
- `CREATE TABLE IF NOT EXISTS` on an existing table needs no privilege. The
  denial lands on the first statement that writes.

## The group you would grant to may already be admin

Contributor or Owner on the workspace's resource group makes a workspace admin
automatically, with no Databricks group involved.

```bash
az role assignment list --scope "/subscriptions/<sub>/resourceGroups/<rg>" --include-inherited -o table
databricks -p "$P" users list -o json
databricks -p "$P" groups get <admins-group-id> -o json
```

Observed: the one group holding Contributor is the group every engineer is in, so
every member bypasses every grant. The workspace contained one user, in `admins`.

Pass: you can name a principal that is not a workspace admin and can still reach
the workspace.

## Climb the storage chain until it stops

Contributor creates everything except the role assignment. Run it anyway, the
failure is the request.

```bash
az resource list -g <rg> --query "[].{name:name, tags:tags}" -o json
```

Take the tag values from an existing resource, or Azure and Databricks cost
reporting cannot be joined.

```bash
az storage account create -g <rg> -n <account> -l <region> --sku Standard_ZRS --kind StorageV2 --hns true --tags owner=<..> environment=<..> cost_center=<..> project=<..>
az storage container create --account-name <account> -n managed --auth-mode login

az extension add --name databricks --only-show-errors
az databricks access-connector create -g <rg> -n <connector> -l <region> --identity-type SystemAssigned --tags <..>
az databricks access-connector show -g <rg> -n <connector> --query "identity.principalId" -o tsv

az role assignment create --assignee <principal-id> --role "Storage Blob Data Contributor" --scope "<account-id>/blobServices/default/containers/managed"

databricks -p "$P" storage-credentials create --json '{"name":"sc-managed-dev","azure_managed_identity":{"access_connector_id":"<connector resource id>"}}'
databricks -p "$P" external-locations create --json '{"name":"el-managed-dev","url":"abfss://managed@<account>.dfs.core.windows.net/","credential_name":"sc-managed-dev"}'
```

The same missing role, seen from both sides:

- `az role assignment create` fails `AuthorizationFailed` on
  `Microsoft.Authorization/roleAssignments/write`.
- `external-locations create` fails `403` on a `HEAD` against
  `.../validate_credential_<timestamp>`.

Stage the rest anyway. `skip_validation` exists for this:

```bash
databricks -p "$P" external-locations create --json '{"name":"el-managed-dev","url":"abfss://managed@<account>.dfs.core.windows.net/","credential_name":"sc-managed-dev","skip_validation":true}'
databricks -p "$P" catalogs create --json '{"name":"<catalog>","storage_root":"abfss://managed@<account>.dfs.core.windows.net/<catalog>"}'
databricks -p "$P" catalogs update <catalog> --json '{"isolation_mode":"ISOLATED"}'
databricks -p "$P" workspace-bindings update-bindings catalog <catalog> --json '{"add":[{"workspace_id":<id>,"binding_type":"BINDING_TYPE_READ_WRITE"}]}'
databricks -p "$P" schemas create --json '{"name":"bronze","catalog_name":"<catalog>"}'

databricks -p "$P" api post /api/2.0/sql/statements --json '{"warehouse_id":"<id>","statement":"CREATE TABLE <catalog>.bronze.probe (id INT)"}'
```

All of it passes. The write fails
`INVALID_STATE.UC_CLOUD_STORAGE_ACCESS_FAILURE`, proving the role is the only
missing piece. Rerun that statement once it is granted.

- Creating an access connector needs only Contributor. Granting it a role does
  not. Different rights, usually different people.
- `external-locations create` validates by reaching the path, which is why the
  role surfaces here rather than at first query.
- One assignment per container. Dev with one container needs one, prod with a
  container per catalog needs one each.

## Compute policy and warehouse tags

Compute policies govern clusters and jobs, never SQL warehouses, so warehouse
tags are set at creation and nothing enforces them.

```bash
databricks -p "$P" cluster-policies create --json '{"name":"dev-tagged","definition":"{\"custom_tags.owner\":{\"type\":\"fixed\",\"value\":\"<..>\"},\"custom_tags.environment\":{\"type\":\"fixed\",\"value\":\"dev\"},\"custom_tags.cost_center\":{\"type\":\"fixed\",\"value\":\"<..>\"},\"custom_tags.project\":{\"type\":\"fixed\",\"value\":\"<..>\"}}"}'
databricks -p "$P" cluster-policies get <policy-id> -o json

databricks -p "$P" warehouses create --json '{"name":"wh-dev","cluster_size":"2X-Small","warehouse_type":"PRO","enable_serverless_compute":true,"auto_stop_mins":10,"min_num_clusters":1,"max_num_clusters":1,"tags":{"custom_tags":[{"key":"owner","value":"<..>"}]}}'
databricks -p "$P" warehouses set-permissions <id> --json '{"access_control_list":[{"group_name":"<group>","permission_level":"CAN_USE"}]}'
```

Pass: `cluster-policies get` returns the four tags in its `definition`, and the
warehouse reads back with its `custom_tags` and the group holding `CAN_USE`. The
create response echoes only a policy id.

- `max_num_clusters` has no API default. Omitting it fails with `0 is not a valid
  value`, though the UI fills it in.
- A warehouse starts `RUNNING` at creation and bills until auto-stop.
- The provisioned starter warehouse is untagged and no policy reaches back to fix
  it. Delete it or tag it, and record which.

## The platform reads

Three reads that decide what later steps must do. None changes state.

```bash
databricks -p "$P" metastores summary

SCOPE="/subscriptions/<sub>/resourceGroups/<rg>"
az policy assignment list --scope "$SCOPE" --disable-scope-strict-match --query "[].{name:name, policy:policyDefinitionId, enforcement:enforcementMode, params:parameters}" -o json
az provider show -n Microsoft.Storage --query registrationState -o tsv
az provider show -n Microsoft.EventGrid --query registrationState -o tsv
```

Pass: you can state whether `storage_root` is present, name every deny-effect
policy with its `enforcementMode`, name the scopes you could not read, and both
providers say `Registered`.

- `storage_root` absent means every catalog must name an explicit
  `MANAGED LOCATION`. Present means a catalog created without one silently
  inherits storage belonging to the shared metastore.
- Take tag keys from each assignment's `tagName` parameter, not from its name.
- A `deny` policy at `DoNotEnforce` blocks nothing, so a successful apply proves
  nothing about tags. Observed: four assignments, all `deny`, all `DoNotEnforce`.
- Assignments above the resource group do not return without read access there.
  Unreadable is an acceptable answer. Unknown is not.

## Create a service principal and read back what it carries

```bash
databricks -p "$P" service-principals create --json '{"displayName":"<name>","active":true}'
databricks -p "$P" service-principals get <scim-id> -o json
```

Pass: `displayName` reads back as set, `groups` is empty, re-read after ten
minutes in case an automation rule adds `admins` on a delay.

- `displayName` persists when set at creation. A later patch can succeed and read
  back empty for a while.
- The principal arrived with no entitlements at all. Nothing in the sequence gives
  a CI principal any, because entitlements go to groups and these principals are
  deliberately kept out of groups.
- An `externalId` means the principal came from Entra. Its absence is the
  Databricks-managed signature.

## Pull an Entra group in, and prove it was pulled not created

UI only: Settings, Identity and access, Groups, Manage, Add group. The picker
searches Entra. The account-level CLI route needs an account admin.

```bash
az ad group show --group <group> --query "{name:displayName, id:id, onPremSync:onPremisesSyncEnabled}"
databricks -p "$P" groups get <group-id> -o json
```

Pass, three together:

- `meta.resourceType` reads `Group`, not `WorkspaceGroup`. A group created inside
  Databricks returns the latter.
- `externalId` matches the Entra object id.
- No `members` field is returned, so membership cannot be edited here. Editable
  membership means it was created rather than pulled, which is a fail.

Observed: the group arrived carrying `workspace-access`, `databricks-sql-access`
and `workspace-consume`, none requested. Check what arrived rather than assuming
the default is minimal.

`onPremisesSyncEnabled` true means every membership change is a ticket to whoever
owns the on-premises directory.

## Probe a connection type without setting it up

Differential test, because an empty options map is rejected before the type is
checked. Neither probe creates anything.

```bash
databricks -p "$P" connections create --json '{"name":"probe-bogus","connection_type":"NOT_A_REAL_TYPE","options":{"a":"b"}}'
databricks -p "$P" connections create --json '{"name":"probe-x","connection_type":"<TYPE>","options":{"a":"b"}}'
```

Pass: the errors differ. A bogus type returns `Missing required field:
connection_type`. A real one names the options it wants.

Observed for `SHAREPOINT`:

```
CONNECTION/CONNECTION_SHAREPOINT must include the following option(s): tenant_id,client_id,client_secret,refresh_token.
```

So it needs an Entra app registration, admin consent and a user OAuth flow. It
takes a `client_secret` and offers no federation alternative.

## Where the CI runner can sit

The runner polls two endpoints outbound: GitLab and the Databricks control plane.
Whichever is harder to reach decides where it lives.

```bash
dig +short <gitlab-host>
dig +short <gitlab-host> @8.8.8.8
```

Different answers mean split-horizon DNS. Observed: RFC1918 internally,
Cloudflare publicly, so the host is internet-facing.

From Azure Cloud Shell, not your own machine, which takes the internal route:

```bash
curl -sSI https://<gitlab-host> | head -1
curl -sSI https://<workspace-host> | head -1
```

Pass: any HTTP response. Observed `302` and `404`. A `403` means a WAF or an IP
access list, a timeout means public access is closed. Step 6 can change the
second.

For a local runner, the docker executor needs a daemon at
`/var/run/docker.sock`, which recent Docker Desktop no longer symlinks.

## Serverless pipelines in the region

Lakeflow Connect runs on serverless pipelines, so whether they work here decides
whether that ingestion route is open at all.

```python
# Databricks notebook source
import dlt


@dlt.table
def probe():
    return spark.range(1)
```

```bash
databricks -p "$P" workspace import /Users/<you>/probe_pipeline --file probe_pipeline.py --format SOURCE --language PYTHON --overwrite

databricks -p "$P" pipelines create --json '{"name":"probe-serverless","serverless":true,"catalog":"<catalog>","schema":"<schema>","libraries":[{"notebook":{"path":"/Users/<you>/probe_pipeline"}}]}'

databricks -p "$P" pipelines start-update <pipeline-id>
databricks -p "$P" pipelines get <pipeline-id> -o json | grep -E '"state"|"message"'
```

Pass: `COMPLETED`, pipeline back to `IDLE`. Observed 2026-08-13 in
`francecentral`. Creation alone proves nothing, a regional restriction bites when
compute starts.

```bash
databricks -p "$P" pipelines delete <pipeline-id>
databricks -p "$P" workspace delete /Users/<you>/probe_pipeline
databricks -p "$P" tables delete <catalog>.<schema>.probe
```

The third line matters: deleting a pipeline leaves its tables behind, orphaned
rather than dropped.

<!--
Version: 0.1 | Last Updated: 2026-08-13 | Status: Draft
-->
