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

Setting a catalog to `ISOLATED` does not bind the current workspace. The binding
list is a separate object. Leave it empty and the catalog is reachable from no
workspace at all.

```bash
databricks -p "$P" catalogs update <catalog> --json '{"isolation_mode":"ISOLATED"}'
databricks -p "$P" catalogs get <catalog>
databricks -p "$P" workspace-bindings get-bindings catalog <catalog>
```

Then run any query against it from compute in the workspace.

Fail looks like this, and it is the expected result before the binding exists:

```
[INSUFFICIENT_PERMISSIONS] Catalog '<catalog>' is not accessible in current workspace SQLSTATE: 42501
```

Bind it:

```bash
databricks -p "$P" workspace-bindings update-bindings catalog <catalog> --json '{"add":[{"workspace_id":7405605180591006,"binding_type":"BINDING_TYPE_READ_WRITE"}]}'
```

Pass: the same query succeeds after binding, with no redeploy and no code change.

Two things this settles:

- `catalogs get` keeps working throughout. It reads the metastore, which is not
  workspace-scoped, so the CLI cannot tell you whether compute can reach the
  catalog. Only running a query can.
- Isolation is between workspaces, never between catalogs. Two catalogs bound to
  the same workspace are not separated from each other by this setting. Grants do
  that.

## Development mode renames the resources

`mode: development` on a bundle target prefixes every resource name, schemas
included. A target without a mode does not. Code that hardcodes a resource name
therefore works in one target and fails in the other.

Deploy the same bundle to a `development` target and to a plain one, then:

```bash
databricks -p "$P" bundle summary -t dev
databricks -p "$P" bundle summary -t staging
```

Observed: schema `bronze` deployed as `dev_gmourgues_bronze` in dev and as
`bronze` in staging. The job likewise carried a `[dev gmourgues]` prefix in dev
and none in staging.

Fail looks like this, from a notebook that hardcoded `bronze`:

```
[SCHEMA_NOT_FOUND] The schema `datawan_dev.bronze` cannot be found. SQLSTATE: 42704
```

Fix, in the job's `base_parameters`, so the code receives the deployed name
rather than assuming it:

```yaml
              schema: ${resources.schemas.bronze.name}
```

Pass: the identical source tree deploys and runs against both targets with no
edit between them.

## A successful deploy does not mean a usable resource

`bundle validate` accepted a `resources.schemas` block and `bundle deploy`
printed `Deployment complete!`, twice, while the run that depended on that schema
failed. The schema existed under a different name, and neither command said so.

```bash
databricks -p "$P" bundle validate -t <target>
databricks -p "$P" bundle deploy -t <target>
databricks -p "$P" bundle summary -t <target>
```

Pass: `bundle summary` names every resource the deploy created, with the name it
actually has. Treat it as the read-back, not the deploy's exit code.

The same holds for the catalog binding above: the first deploy reported success
while the catalog it targets was reachable by no workspace at all.

## Make the CI prove the federation gap

A pipeline that cannot authenticate is still worth running. It produces the token
claims a Databricks account admin needs, and Databricks names the policy it wants
in its own rejection.

`.gitlab-ci.yml`, four variables and an `id_tokens` block:

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

The decode prints the payload only, never the signature, so the log carries
claims rather than a usable credential.

Pass, in three steps, each a different error:

1. `more than one authorization method configured: env-oidc and oauth`. The CLI
   found a second candidate. `DATABRICKS_AUTH_TYPE` names the one to use.
   `DATABRICKS_CONFIG_FILE=/dev/null` alone does not fix this, and its not
   fixing it is the evidence that the profile file was never the second method.
2. `invalid_grant … TOKEN_INVALID (Ensure a valid federation policy has been
   configured)`, quoting the exact issuer, subject and audience it expects. That
   is the pass. Every link works except the policy.
3. Green, once the policy exists.

Two things this settles:

- `DATABRICKS_OIDC_TOKEN_ENV` is the right variable name for a generic OIDC
  provider. The CLI echoes it back as `oidc_token_env` in its errors.
- On a shell executor the job runs as you, with your credentials on disk, so a
  green pipeline may prove nothing. Here the CLI refused rather than silently
  falling back, but a runner with no profile on it is the only real answer.

## Prove a grant, in both directions, with no second person

Every check run by a workspace admin against objects they created tests nothing:
the owner holds every privilege implicitly. The acceptance test needs an identity
that owns nothing, and it does not have to be a human.

A Databricks managed service principal with no groups and no entitlements is
already that identity. Run a job as it with `run_as`, and no secret is involved.

In the bundle target:

```yaml
    run_as:
      service_principal_name: <application id>
```

Grant deliberately less than the job needs, run, then grant the rest and run
again. No redeploy between the two, grants are evaluated at runtime.

```bash
databricks -p "$P" grants update catalog <catalog> --json '{"changes":[{"principal":"<application id>","add":["USE_CATALOG"]}]}'
databricks -p "$P" grants update schema <catalog>.<schema> --json '{"changes":[{"principal":"<application id>","add":["USE_SCHEMA","SELECT"]}]}'
databricks -p "$P" bundle run <job> -t <target>
```

Expected fail, and this is the pass condition for the first half:

```
PERMISSION_DENIED: User does not have MODIFY on Table '<catalog>.<schema>.events'. SQLSTATE: 42501
```

Then:

```bash
databricks -p "$P" grants update schema <catalog>.<schema> --json '{"changes":[{"principal":"<application id>","add":["MODIFY"]}]}'
databricks -p "$P" bundle run <job> -t <target>
```

Pass: green. Same code, same identity, same job, one privilege apart.

Three things this settles:

- `run_as` needs the `servicePrincipal.user` role on the principal, held by whoever
  deploys. Creating a principal makes you its manager, which is not the same
  thing, and the deploy fails with `403 PERMISSION_DENIED` until you add it under
  the principal's Permissions tab.
- Verify `run_as` actually took before believing any result. A deploy that fails
  on the `run_as` field leaves the job on its previous definition, and the next
  run goes green as the old identity. Check `jobs get <id>` for the `run_as`
  block, not just `run_as_user_name`.
- `CREATE TABLE IF NOT EXISTS` on an existing table needs no privilege. The
  denial lands on the first statement that actually writes.

## The group you would grant to may already be admin

In Azure Databricks anyone with Contributor or Owner on the workspace's resource
group is a workspace admin automatically, with no Databricks group involved.

```bash
az role assignment list --scope "/subscriptions/<sub>/resourceGroups/<rg>" --include-inherited -o table
databricks -p "$P" users list -o json
databricks -p "$P" groups get <admins-group-id> -o json
```

Observed: the one group holding Contributor on the workspace resource group is
the group every engineer is in, so every member is a workspace admin and bypasses
every grant. The workspace contained exactly one user, in `admins`.

Pass: you can name a principal that is not a workspace admin and can still reach
the workspace. If you cannot, the human half of the acceptance test is blocked
until a group with no Azure role on that resource group exists, and the machine
identity above is the only test available.

## Climb the storage chain until it stops

Contributor on the resource group creates everything in the chain except the one
role assignment. Run it anyway: the failure locates the wall and becomes the
request.

```bash
az storage account create -g <rg> -n <account> -l <region> --sku Standard_ZRS --kind StorageV2 --hns true --tags owner=<..> environment=<..> cost_center=<..> project=<..>
az storage container create --account-name <account> -n managed --auth-mode login

az extension add --name databricks --only-show-errors
az databricks access-connector create -g <rg> -n <connector> -l <region> --identity-type SystemAssigned --tags <..>
az databricks access-connector show -g <rg> -n <connector> --query "identity.principalId" -o tsv

az role assignment create --assignee <principal-id> --role "Storage Blob Data Contributor" --scope "<account-id>/blobServices/default/containers/managed"
```

Take the tag values from an existing resource in the group rather than inventing
them, or Azure and Databricks cost reporting cannot be joined:

```bash
az resource list -g <rg> --query "[].{name:name, tags:tags}" -o json
```

Then the Databricks half, which needs no Azure rights:

```bash
databricks -p "$P" storage-credentials create --json '{"name":"sc-managed-dev","azure_managed_identity":{"access_connector_id":"<connector resource id>"}}'
databricks -p "$P" external-locations create --json '{"name":"el-managed-dev","url":"abfss://managed@<account>.dfs.core.windows.net/","credential_name":"sc-managed-dev"}'
```

Observed, and this is the pass condition when the role is missing:

- `az role assignment create` fails `AuthorizationFailed` on
  `Microsoft.Authorization/roleAssignments/write`.
- `external-locations create` fails with a `403` on a `HEAD` against
  `.../validate_credential_<timestamp>`.

Both are the same missing role, seen from the two sides. Everything else in the
chain passed, so the request is one command by one other person.

Three things this settles:

- Creating an access connector needs only Contributor. Granting it a role does
  not. Those are different rights and they usually sit with different people.
- `external-locations create` validates by reaching the path, which is why the
  missing role surfaces here rather than at first query. The API's
  `skip_validation` flag is the proof that validation is the default.
- The role goes on the container, so it is one assignment per container. Dev with
  one container and a path per catalog needs one. Prod with a container per
  catalog needs one each.

## Compute policy and warehouse tags

Compute policies govern clusters and jobs. They cannot touch a SQL warehouse, so
warehouse tags are set at creation and nothing enforces them.

```bash
databricks -p "$P" cluster-policies create --json '{"name":"dev-tagged","definition":"{\"custom_tags.owner\":{\"type\":\"fixed\",\"value\":\"<..>\"},\"custom_tags.environment\":{\"type\":\"fixed\",\"value\":\"dev\"},\"custom_tags.cost_center\":{\"type\":\"fixed\",\"value\":\"<..>\"},\"custom_tags.project\":{\"type\":\"fixed\",\"value\":\"<..>\"}}"}'
databricks -p "$P" cluster-policies get <policy-id> -o json

databricks -p "$P" warehouses create --json '{"name":"wh-dev","cluster_size":"2X-Small","warehouse_type":"PRO","enable_serverless_compute":true,"auto_stop_mins":10,"min_num_clusters":1,"max_num_clusters":1,"tags":{"custom_tags":[{"key":"owner","value":"<..>"}]}}'
databricks -p "$P" warehouses set-permissions <id> --json '{"access_control_list":[{"group_name":"<group>","permission_level":"CAN_USE"}]}'
```

Pass: `cluster-policies get` returns the four tags in its `definition`, and the
warehouse reads back with its `custom_tags` and the group holding `CAN_USE`. The
create response echoes only a policy id, so it proves nothing on its own.

Two things this settles:

- `max_num_clusters` has no API default. Omitting it fails with `0 is not a valid
  value`, though the UI fills it in for you.
- A warehouse starts `RUNNING` at creation and bills until auto-stop. Stop it
  explicitly if the test is done.

The provisioned starter warehouse is untagged and no policy can reach back to fix
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

Three things this settles:

- `storage_root` absent means every catalog must name an explicit
  `MANAGED LOCATION`. Present means a catalog created without one silently
  inherits storage belonging to the shared metastore.
- Take tag keys from each assignment's `tagName` parameter, not from its name.
  The name is a label chosen by whoever assigned it.
- A `deny` policy at `DoNotEnforce` marks resources non-compliant and blocks
  nothing, so a successful apply proves nothing about tags. Observed: four
  assignments, all `deny`, all `DoNotEnforce`.

Assignments above the resource group do not return without read access there.
Unreadable is an acceptable answer. Unknown is not.

## Create a service principal and read back what it carries

```bash
databricks -p "$P" service-principals list -o json
databricks -p "$P" service-principals create --json '{"displayName":"<name>","active":true}'
databricks -p "$P" service-principals get <scim-id> -o json
```

Pass: `displayName` reads back as set, `groups` is empty, and you re-read after
ten minutes in case an automation rule adds `admins` on a delay.

Two things this settles:

- `displayName` persists when set at creation through the SCIM API. A later patch
  can succeed and read back empty for a while, so a single negative read is not
  proof of failure.
- A Databricks managed principal arrived with **no** entitlements at all, not the
  `workspace-access` and `databricks-sql-access` recorded elsewhere. Nothing in
  the sequence gives a CI principal entitlements, because entitlements are
  assigned to groups and these principals are deliberately kept out of groups.

An `externalId` on the record means the principal came from Entra. Its absence is
the Databricks-managed signature.

## Pull an Entra group in, and prove it was pulled not created

```bash
az ad group show --group <group> --query "{name:displayName, id:id, onPremSync:onPremisesSyncEnabled}"
databricks -p "$P" groups list -o json
databricks -p "$P" groups get <group-id> -o json
```

The pull-in itself is UI only: Settings, Identity and access, Groups, Manage, Add
group. The picker searches Entra. The account-level CLI route needs an account
admin.

Pass, three things together:

- `meta.resourceType` reads `Group`, not `WorkspaceGroup`. A group created inside
  Databricks returns the latter, so the two objects are distinguishable.
- `externalId` matches the Entra object id.
- No `members` field is returned at all, so membership cannot be edited here.
  Editable membership means it was created rather than pulled, which is a fail.

Observed: the group arrived carrying `workspace-access`, `databricks-sql-access`
and `workspace-consume`, none requested. Entitlements are assigned when the
principal is added to the workspace rather than inherited from `users`, so check
what arrived rather than assuming the default is minimal.

`onPremisesSyncEnabled` true means every membership change is a ticket to whoever
owns the on-premises directory.

## Probe a connection type without setting it up

Find out whether a Lakeflow Connect source exists on this workspace before
requesting app registrations for it. Differential test, because an empty options
map is rejected before the type is checked.

```bash
databricks -p "$P" connections create --json '{"name":"probe-bogus","connection_type":"NOT_A_REAL_TYPE","options":{"a":"b"}}'
databricks -p "$P" connections create --json '{"name":"probe-x","connection_type":"<TYPE>","options":{"a":"b"}}'
```

Pass: the two errors differ. A bogus type returns
`Missing required field: connection_type`. A real one names the options it wants.

Observed for `SHAREPOINT`:

```
CONNECTION/CONNECTION_SHAREPOINT must include the following option(s): tenant_id,client_id,client_secret,refresh_token.
```

So the type exists, and it needs an Entra app registration, admin consent and a
user OAuth flow to mint the refresh token. It takes a `client_secret` and offers
no federation alternative, which is worth deciding rather than discovering.

Neither probe creates anything.

## Where the CI runner can sit

The runner polls two endpoints outbound: GitLab and the Databricks control plane.
Whichever is harder to reach decides where it lives.

```bash
dig +short <gitlab-host>
dig +short <gitlab-host> @8.8.8.8
```

Different answers mean split-horizon DNS. Observed: an RFC1918 address
internally, Cloudflare addresses publicly, so the host is internet-facing and an
Azure runner has a path.

Then from Azure Cloud Shell, not from your own machine, which would take the
internal route and prove nothing:

```bash
curl -sSI https://<gitlab-host> | head -1
```

Pass: `200` or `302`. A `403` means a WAF or Cloudflare Access is filtering, and
the runner's egress needs allowlisting or the runner sits on-prem.

Not yet tested, and it matters equally: whether an Azure VM reaches the workspace
host, given the workspace already has private endpoints and a
`privatelink.azuredatabricks.net` private DNS zone.

On the executor, for a local runner: the docker executor needs a daemon at
`/var/run/docker.sock`, which recent Docker Desktop no longer symlinks. The shell
executor avoids it but runs as you, with your credentials on disk, which is its
own hazard.

<!--
Version: 0.1 | Last Updated: 2026-08-13 | Status: Draft
-->
