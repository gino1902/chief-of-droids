# Databricks platform foundation setup

> One ordered sequence from a provisioned but unused workspace to a governed
> bronze table an automated path can write and a group can read. Decisions are
> not taken here. They arrive as accepted ADRs, and each step names the one it
> consumes.
> Upstream: [[dbr-RG-to-working-non-admin-user]], which ends where the
> provisioned baseline below begins.

This runbook assumes one configuration and does not generalise beyond it: a
Terraform-provisioned, VNet-injected, Premium workspace, automatically enabled
for Unity Catalog, where workspace admin reaches a human through an Entra group
and account admin is held elsewhere. Greenfield here means unused, not empty.
The workspace already contains infrastructure. It contains no work.

## What counts as done

Step 25 is the finish line: **data arrives in a governed bronze table by an
automated path, and a group member who did not create it reads it.** Deployed
from the repo, not from the UI.

Source-neutral on purpose. The first real source is SharePoint, which is
temporary, and the mechanism will change. What must hold is the governed
destination and the read, not any one ingestion route.

Two weaker finish lines are easy to mistake for it.

| Stops at | Proves | Why it is not enough |
| :--- | :--- | :--- |
| A table exists in the catalog | Storage and the catalog work | Nothing proves anyone but its creator can read it |
| Someone ran the load by hand | The ingest code works | A hand-run load is a demo. The automated path is what has to hold at 3am |

## Preconditions

### Entry condition

The gate is per step, not up front. An ADR must be Accepted before the first
step that consumes it, and not before. The `First consumed` column below is
therefore a deadline, one per ADR. Steps 1, 2, 3, 17, 24 and 25 consume no ADR
and can run against an empty decision record.

### ADRs

Ordered by the first step that consumes them. The `Depends on` column carries the
order they must be accepted in, which is not the same order.

| ADR | Subject | First consumed | Also consumed by | Depends on |
| :--- | :--- | :--- | :--- | :--- |
| 🔲 | Non-human identity model | 4 | 15 | none |
| 🔲 | Deployment model | 5 | Every step that changes state | none |
| 🔲 | Catalog and schema model | 5 | 7, 12, 13 | Workspace topology |
| 🔲 | Network posture | 6 | 23 | Serverless or classic posture |
| 🔲 | Access Connector and external location granularity | 7 | none | Catalog and schema model, Metastore root storage |
| 🔲 | Workspace topology | 8 | 9, 16 | none |
| 🔲 | Ownership and grant model | 8 | 11, 14, 15 | Workspace topology, Catalog and schema model |
| 🔲 | Secret scope model | 10 | none | none |
| 🔲 | Metastore root storage and MANAGED LOCATION policy | 12 | none | Workspace topology |
| 🔲 | Serverless or classic posture | 18 | 20 | none |
| 🔲 | Tagging and budget route | 18 | 19 | Serverless or classic posture |
| 🔲 | Legacy surface posture | 21 | none | none |
| 🔲 | Data protection model | 22 | 5 | Catalog and schema model |

> [!info] Two carry content that is settled
> - **Metastore root storage and MANAGED LOCATION policy.** No metastore root.
>   Each catalog takes an explicit `MANAGED LOCATION` on the durable account from
>   step 5. Naming and layout are what remain open
> - **Data protection model.** It feeds step 5 as well as step 22, because Azure
>   retention and immutability are container-level settings and prod uses one
>   container per catalog. Deciding it late means changing container policy after
>   data has landed

Acceptance order, derived from the `Depends on` column: workspace topology first,
then metastore root storage and the catalog and schema model, then Access
Connector granularity and the ownership and grant model, then the rest.

> [!warning] Two ADRs are due earlier than their row suggests
> - Network posture is consumed at step 6, not 24. Serverless cannot reach
>   firewalled storage without it
> - It depends on serverless or classic posture, so that one is also due before
>   step 6 despite showing 19
> - Both are owned outside this team. Start them first
> - Only the data protection ADR at step 22 can genuinely lag, and only while
>   nothing sensitive has landed

### Identities

| Role | Needed for | Held by |
| :--- | :--- | :--- |
| Account admin | 6, 11, 17, 19, and the federation policy half of 4 | 🔲 |
| Workspace admin | 1, 2, 4, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 20, 21, 22 | gmourgues@sqli.com |
| Platform engineer | 3, 5, 24 | 🔲 |
| Entra admin | 8, only if the group is created in Entra rather than pulled in | 🔲 |
| Network team | 23 | 🔲 |
| Test user | 25 | 🔲 |

Workspace admin is not granted to a person here. It arrives through an Entra
group and materialises as membership of the workspace `admins` group. The
control point is therefore Entra group membership, not anything inside
Databricks.

### What to ask the account admin for

Four steps and one half-step need an account-level Databricks role. Raise them as
one request. Step numbers are not a request, so this is what to actually ask for.

| Request | Unblocks |
| :--- | :--- |
| Serverless network access to the managed storage account, either a network security perimeter rule or a network connectivity configuration with private endpoint rules | 6 |
| Assign the metastore admin role to a named group | 11 |
| Enable the system table schemas | 17 |
| Create the serverless budget policy | 19 |
| A federation policy per CI service principal, once the repository and its protected branches exist | 4, second half only |
| Set the display name on the account-level service principal record, if it is empty | 4 |

The first carries the longest lead time and needs someone on the Azure side too,
so it is two people and not one.

> [!warning] Do not over-assign this role
> A workspace admin in an auto-enabled workspace holds `CREATE CATALOG`,
> `CREATE EXTERNAL LOCATION`, `CREATE STORAGE CREDENTIAL` and
> `CREATE SERVICE CREDENTIAL` on the metastore, owns what they create, and can
> therefore grant on it. Account groups, workspace assignment, entitlements,
> catalog bindings, catalog grants, service principal grants and service
> principal creation are all within reach without an account admin.
>
> Assume workspace admin and test. The default assumption is wrong more often
> than it is right.

### Tooling

Install before step 1, on the machine that will run the sequence.

| Tool | Needed for | Install |
| :--- | :--- | :--- |
| Databricks CLI | 1 onward | `brew tap databricks/tap && brew install databricks` |
| Azure CLI | 3, 5, 6, 7 | `brew install azure-cli` |
| Terraform | Every step that changes state | `brew install terraform` |

Authenticate the Databricks CLI with OAuth against the workspace host. The
browser opens, so run it yourself rather than from an agent session.

```bash
databricks auth login --host https://<workspace-host>
```

The Databricks CLI matters earlier than it looks. It reads metastore state
without any compute existing, which is the only way to complete step 1 before a
warehouse exists, and creating a warehouse early would land untagged compute
ahead of the policies in step 18. Homebrew will refuse the Databricks formula
until the tap is trusted: `brew trust --formula databricks/tap/databricks`.

### Provisioned baseline

State the workspace should already be in at step 1, produced upstream, not by
this sequence.

- Verify before step 1, not during
- A failing row stops the sequence. It is a question for the Terraform. A manual
  fix drifts from state and the next apply reverts it
- Resolve the workspace identity first. Every Azure-side step scopes off it, and
  the managed resource group is not it. That group holds what Databricks
  provisions for itself and you will usually not be able to read it

| Expect | Expected value | Check |
| :--- | :--- | :--- |
| Workspace identity | A resource ID whose `workspaceUrl` matches your host, plus its resource group and managed resource group | `az resource list -g <rg> --resource-type Microsoft.Databricks/workspaces`, then `az resource show --ids <id> --query "{url:properties.workspaceUrl, rg:resourceGroup, managedRg:properties.managedResourceGroupId}"` |
| Workspace configuration | Premium, no public IP | `az resource show --ids <id> --query "{sku:sku.name, noPublicIp:properties.parameters.enableNoPublicIp.value}"` |
| Operator Azure rights | Enough to tell which later steps are yours | `az role assignment list --assignee <your-object-id> --all --include-groups -o table` |
| Metastore attached | A metastore in the workspace region | `databricks -p "$P" metastores summary` |
| Access connector | One, in the workspace's managed resource group, which you will not be able to read directly | `access_connector_id` in the storage credential below |
| Storage credential | One, named after the workspace, `ISOLATION_MODE_ISOLATED`, owned by `_workspace_admins_<workspace>` | `databricks -p "$P" storage-credentials list -o json` |
| External location | One, on the workspace Unity Catalog storage container | `databricks -p "$P" external-locations list -o json` |
| File events | `effective_enable_file_events: true` with a managed AQS queue | Same command as above |
| Workspace catalog | `MANAGED_CATALOG` named after the workspace, storage root inside that container | `databricks -p "$P" catalogs list -o json` |
| Your workspace admin | Direct membership of the `admins` group | `databricks -p "$P" current-user me` |
| Compute | A `Serverless Starter Warehouse` from provisioning, stopped and untagged. No clusters. Anything else is residue | `databricks -p "$P" warehouses list -o json` and `clusters list` |
| IaC repo | Exists, and the CI principal can apply to it. See [[2026-08-10-databricks-cicd-service-principal]] | 🔲 record the repo location here |

Run it as one script rather than eleven commands. A table of checks gets skimmed,
and a row that nobody runs is worse than no row, because it reads as verified.

```bash
P=<profile>
RG=<workspace-resource-group>

echo "== workspace resources =="
az resource list -g "$RG" --resource-type Microsoft.Databricks/workspaces --query "[].id" -o tsv
echo "== operator azure rights =="
az role assignment list --assignee "$(az ad signed-in-user show --query id -o tsv)" --all --include-groups -o table
echo "== metastore =="
databricks -p "$P" metastores summary
echo "== storage credentials =="
databricks -p "$P" storage-credentials list -o json
echo "== external locations =="
databricks -p "$P" external-locations list -o json
echo "== catalogs =="
databricks -p "$P" catalogs list -o json
echo "== you =="
databricks -p "$P" current-user me
echo "== compute =="
databricks -p "$P" warehouses list -o json
databricks -p "$P" clusters list -o json
```

> [!warning] The baseline is not neutral
> - The workspace catalog arrives with open default grants
> - Every workspace user holds `USE CATALOG`, plus `USE SCHEMA`, `CREATE TABLE`,
>   `CREATE VOLUME`, `CREATE MODEL`, `CREATE FUNCTION` and
>   `CREATE MATERIALIZED VIEW` on its `default` schema
> - Live from the moment the workspace exists. Step 14 decides its fate. Do not
>   discover it at step 25

### Environment checks

Two things the baseline cannot tell you. Both cheap, both consequential.

**Someone holds account admin.**

- Eight steps need it. It does not flow from the Entra group that makes you a
  workspace admin
- Test: open `accounts.azuredatabricks.net`. An account admin gets a console with
  a left nav, everyone else gets a workspace picker
- If nobody holds it, an Entra Global Administrator signs in once, which
  auto-creates their role, then delegates under User management, Roles. No other
  route

**Who else is on the metastore.**

- One metastore per region, and it is multi-tenant
- Expect catalogs owned by people outside your workspace, created years before it
- Their catalog and schema names are visible to you without any grant. Yours are
  visible to them unless step 16 binds them
- Read 2026-08-12: `metastore_azure_francecentral` dates from June 2024 and
  carries catalogs owned by a user outside this workspace, schemas dated October
  2024, one already called `bronzes`

> [!todo] 🔲 To be defined
> What steps 1 to 3 assume about the tenant and subscription beyond the above.

## How to read a step

Each step carries the same fields.

- **Category.** Gate, foundation, compute, admin, protection, acceptance
- **Owner, inputs, prerequisite, impact.** One line, machine-readable
- **Inputs.** The facts this step consumes and where each was produced, either a
  baseline row or an earlier step. Every input names a producer. One that names
  none is a missing step. A step with an unstated input runs against the wrong
  thing without telling you
- **Prerequisite.** An ADR named here carries 🔲 until Accepted, and a step with
  any 🔲 cannot start. An ADR also carries its own `Depends on` chain, so
  accepting one whose dependency is open unblocks nothing
- **Why it matters.** What the step is for and what breaks without it. Not why
  the option was chosen, which belongs in the ADR
- **What getting the execution wrong costs.** Irreversible, lossy, rework in
  days, or adjustable
- **The play.** The commands or clicks
- **Check.** What passes or fails. A step that writes is checked by reading back
  what changed, not by the command not erroring. One negative read-back is not
  proof of failure, since reads lag writes and endpoints disagree. Read again,
  and read a second surface
- **Clean up.** Any check that creates something ends with the command that
  removes it, in the same step. A runbook that leaves residue teaches the reader
  to leave residue, and residue in a shared resource group outlives whoever made
  it

Impact values: `Irreversible`, `Lossy`, `Rework Nd`, `Adjustable`.

A step earns its number by changing state, or by producing a read that a decision
is waiting on. Anything that merely asserts the world is as expected belongs in
the provisioned baseline instead.

## How a step is written

These rules govern every edit to this document.

- Bullets where the content is a list. Prose only for a single idea
- Cut anything a field already states. Do not restate `Impact` in words
- One idea per bullet. Bullets in the same category merge
- No justification that belongs to a later step
- No session narrative. The reader was not there
- Results tables carry readings, not conclusions
- A result observed under a working assumption names that assumption. An
  unqualified finding reads as a general truth and quietly turns a throwaway into
  a decision
- Keep only what changes the reader's behaviour. Everything else goes

## Scope

Deliberately not here:

- Workspace provisioning itself, which is upstream in
  [[dbr-RG-to-working-non-admin-user]] and in Terraform
- The CI/CD service principal, which has its own note in
  [[2026-08-10-databricks-cicd-service-principal]]
- Silver and gold layers, and any transformation beyond bronze. Their catalogs
  use the same storage account from step 5, so the shape is set here even though
  the layers are not
- Multi-region and disaster recovery
- Network design beyond what steps 6 and 23 require. The hub and spoke topology
  itself is upstream
- SharePoint, the interim landing zone. It is ingested by a Lakeflow Connect
  managed connector straight into managed tables, so it needs none of steps 5
  to 7 and no landing zone of its own. Tracked separately
- Any file-based landing zone. Nothing writes files into storage here. Should a
  producer ever need to, that brings back an external location, file events and
  three more role assignments

## Proven against a live workspace

Exercised 2026-08-11 and 2026-08-12 with throwaway objects, since deleted. Proves
the platform permits the step and the operator holds the rights. Does not mean
the step is done, or that the Terraform produces the same result.

| Step | What was exercised | Verdict |
| :--- | :--- | :--- |
| 1, 2, 3 | The reads, in full | Passed |
| 4 | Created a Databricks managed principal with a display name, as a workspace admin | Creation works. Federation untested |
| 5 | Created a tagged storage account with hierarchical namespace and a container | Passed, and an untagged create was refused first, so the deny policy bites |
| 6 | Nothing | Untested. Needs an account admin |
| 7 | Attempted the prerequisites | **Failed.** The operator cannot write role assignments and cannot read the access connector |
| 8, 9 | Created an account group with entitlements, as a workspace admin | Passed |
| 10 | Created a scope, a secret and an ACL | Passed, and it exposed that account-level principals are refused here |
| 12, 13 | Created a catalog with an explicit managed location and a schema, then wrote and read a table | Passed. The managed storage path works end to end |
| 14, 15 | Granted a group and a service principal on a catalog | Passed |
| 16 | Confirmed the binding controls are present and editable | Passed |
| 18 | Created a compute policy with an enforced tag | Passed |
| 20 | Created a serverless warehouse with tags | Passed |
| 11, 17, 19, 22 | Nothing | Untested. Need an account admin |
| 21, 23, 24, 25 | Nothing | Untested |

Step 7 is the one that failed, and it is the reason the storage path has to come
from the Terraform. See [[2026-08-11-databricks-terraform-changes]].

Steps 12 and 13 were proved against the workspace's own Unity Catalog container,
not against the durable account at step 5. The mechanism is proven, the target is
not.

---

### 1. Read metastore root storage state

`Category: gate` · `Owner: workspace admin` · `Inputs: none` · `Prerequisite: Databricks CLI authenticated` · `Impact: Adjustable`

**Why it matters**

- Step 12 branches on whether the metastore carries a root storage location
- With no root, every catalog must name an explicit `MANAGED LOCATION`
- With a root set, a catalog created without `MANAGED LOCATION` inherits it
  silently, and the managed data lands in storage you may not own
- The metastore is regional and shared, so its state was probably decided before
  your workspace existed

**What getting the execution wrong costs** The read changes nothing. Skipping it
turns step 12 from a decision into an accident.

**The play**

- The account console shows this to an account admin only
- The CLI shows it to a workspace admin, needs no compute, and is scriptable

```bash
P=<profile>
databricks -p "$P" metastores summary
```

**Check**

- Pass means you can state from output whether `storage_root` is present
- Absent needs no action
- Present means stop. Removing a root pushes it down into existing catalogs
  rather than clearing it. See
  [Manage Unity Catalog metastores](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-metastore)

Result for this deployment, read 2026-08-11:

| Field | Value |
| :--- | :--- |
| Metastore | `metastore_azure_francecentral`, `8633a12b-9fd0-4252-9276-8c78717b6584` |
| Region | `francecentral` |
| Created | 2024-06-09, by `System user` |
| `storage_root` | Absent |
| Owner | `System user` |
| Delta Sharing | `INTERNAL`, external access disabled |

Passed. No metastore root, so nothing to unwind before step 12.

### 2. Confirm serverless availability and enablement in region

`Category: gate` · `Owner: workspace admin` · `Inputs: region, from step 1` · `Prerequisite: Databricks CLI authenticated` · `Impact: Adjustable`

**Why it matters**

- Steps 18 and 19 consume the serverless or classic posture ADR, which cannot be
  decided without this
- Two independent conditions, either of which can be false alone: the region
  supports serverless, and the workspace has it enabled
- If serverless is out, step 20 becomes a classic cluster with a different
  permission model
- Step 19 loses its subject, since a serverless budget policy governs nothing
  without serverless spend

**What getting the execution wrong costs** The read is free. Assuming the answer
costs a compute policy and a budget route built around compute that does not
exist, discovered at step 20.

**The play**

- The workspace config is authoritative for enablement, the regional table for
  availability
- The config does not return the region. Take it from step 1
- Read the whole regional row. Several serverless features are regional in their
  own right
- Neither read needs an account admin or compute. Do not create a warehouse to
  find out

```bash
P=<profile>
databricks -p "$P" warehouses get-workspace-warehouse-config
```

Then find the region in the Serverless availability table in
[Features with limited regional availability](https://learn.microsoft.com/en-us/azure/databricks/resources/feature-region-support).

**Check**

- Pass means `enable_serverless_compute` is `true` and the region shows a tick
  under serverless compute
- Serverless needs no enablement in most workspaces. A `false` is someone's
  deliberate act, so ask before flipping it

Result for this deployment, read 2026-08-11:

| Field | Value |
| :--- | :--- |
| `enable_serverless_compute` | `true` |
| Warehouse types enabled | `CLASSIC` and `PRO` |
| `security_policy` | `DATA_ACCESS_CONTROL` |
| Region, from `metastores summary` | `francecentral` |
| Region support | Serverless compute and SQL warehouses ✓, serverless workspaces ✓, default storage ✓, private connectivity ✓, Databricks Apps ✓ |
| Not available in `francecentral` | Model Training forecasting, Lakebase Autoscaling, serverless standalone pipelines |
| System tables in `francecentral` | ✓ |

Passed. Serverless is available and enabled.

### 3. Read what Azure will refuse

`Category: gate` · `Owner: platform engineer` · `Inputs: workspace resource group and operator role assignments, both from the baseline` · `Prerequisite: none` · `Impact: Adjustable`

Network standards are settled upstream by the Terraform and are out of this step.

**Why it matters**

- Policy denials are silent until an apply fails. A missing tag fails the
  deployment, it does not warn
- The enforced tag names bind step 18. A different vocabulary on the Databricks
  side gives two schemes and cost reporting that cannot be joined across them
- `Microsoft.Storage` must be registered before step 5 can create anything, and
  registering a provider needs subscription rights the operator may not hold.
  `Microsoft.EventGrid` matters only if a file-based landing zone is ever added

**What getting the execution wrong costs** Both reads are free. The cost is late
discovery: an apply denied at step 5, or a provider request raised at step 8 that
then waits on someone else.

**The play**

- Take the scope from the baseline workspace identity row
- Policy assignments need `--disable-scope-strict-match` or inherited ones stay
  invisible. Query `name` rather than `displayName`, which is often empty, and
  output JSON, because resource IDs truncate in tables
- Resolve each `policyDefinitionId` to its effect. An audit policy and a deny
  policy are indistinguishable in the assignment list

```bash
SUB=<subscription-id>
RG=<workspace-resource-group>

az policy assignment list --scope "/subscriptions/$SUB/resourceGroups/$RG" \
  --disable-scope-strict-match \
  --query "[].{name:name, policy:policyDefinitionId, enforcement:enforcementMode}" -o json

az policy definition show --name <definition-guid> \
  --query "{name:displayName, effect:policyRule.then.effect, mode:mode}"

az provider show -n Microsoft.EventGrid --query registrationState -o tsv
az provider show -n Microsoft.Storage --query registrationState -o tsv
```

**Check**

- You can name every deny-effect policy applying to what steps 5, 6, 8 and 24
  create, and name the scopes you could not read. Unreadable is an acceptable
  answer, unknown is not
- Both providers read `Registered`, or a request is open with someone who can
  register them

Failure is not finding no policies. Failure is not knowing.

Result for this deployment, read 2026-08-11:

| Finding | Value |
| :--- | :--- |
| Policy, resource group scope | Four assignments, all `Require a tag on resources`, effect `deny`, mode `Indexed` |
| Tags enforced | `owner`, `environment`, `cost_center`, `project` |
| Policy, above resource group | Unreadable. The operator holds Contributor on one resource group only |
| Providers | `Microsoft.EventGrid` and `Microsoft.Storage` both `Registered` |

Passed, with one scope unread. Nothing above the resource group could be checked,
so a deny policy at subscription or management group level would be invisible
here and would still stop an apply.

> [!warning] Mode `Indexed` is narrower than it sounds
> - Evaluates only resource types that support tags and location
> - Does not apply to resource groups
> - Skips child resources with no tags of their own, such as the NIC behind a
>   private endpoint. That is why untagged resources sit under a deny policy
>   without tripping it

### 4. Create the CI/CD service principals

`Category: foundation` · `Owner: workspace admin, except the federation policy which is account admin` · `Inputs: existing service principals and their Entra records, read in the play; GitLab project and protected branches, from the baseline IaC repo row` · `Prerequisite: 🔲 ADR non-human identity model` · `Impact: Lossy`

Detail on the two principal kinds, the four authentication routes and the
federation build is in [[2026-08-10-databricks-cicd-service-principal]]. This
step carries only what changes what you do here.

**Why it matters**

- Automation must not run under a person's token. A principal is scoped
  independently, can be disabled on its own, and survives the person leaving
- The kind is chosen at creation and is not cosmetic. Entra managed reaches other
  Azure resources with the same credential, Databricks managed does not
- The federation policy's subject claim is the entire security boundary. An
  unpinned subject lets any branch in the project deploy to production

**What getting the execution wrong costs**

- Deleting a principal stops its compute, fails its jobs and breaks anything
  shared with Run as Owner. Deactivate instead
- A subject pinned to a mutable path breaks when the group is renamed, and a
  future project reusing that path would match the policy

**The identity model**

| Identity | Kind | Rationale |
| :--- | :--- | :--- |
| Infra Terraform | 🔲 unverified, see the result table | Authenticates to Azure and Databricks in the same run, which is the case that would justify Entra managed |
| CI/CD bundle deploy | Databricks managed, one per environment, OIDC federation | No secret to rotate, and one environment can be revoked alone |
| Claude Code | None. It runs as the human, over user-to-machine OAuth | See below |

Claude Code gets no principal of its own:

- Attribution stays on a person
- It can never exceed your rights
- Revocation is already solved, because access arrives and leaves with the Entra
  group

The cost, stated so it is a decision rather than an oversight: Claude Code cannot
act when you are not there, and its actions are indistinguishable from yours in
the audit log. Either of those becoming a problem is the trigger to revisit.

**The play**

- Read what already exists before creating anything. A deployment principal
  usually exists before this step
- Check the display name through the API, not the UI. The UI resolves a name from
  the identity provider even when the SCIM attribute is empty, and it is the
  empty attribute that audit logs, `created_by` and every automated query will
  report
- Create the CI principals as Databricks managed, one per environment
- Do not put them in `admins`
- Federation policies are account-level and come last, because the subject cannot
  be written until the repository and its protected branches exist
- Decode a real CI token and read its `iss` and `sub` before writing any policy.
  This is the verification step, not a precaution

```bash
P=<profile>
databricks -p "$P" service-principals list -o json
az ad sp show --id <application-id> --query "{name:displayName, appId:appId}"
```

**Check** A write is checked by reading back the thing that should have changed,
not by the command not erroring.

- `service-principals get` returns the display name you set
- If it does not, wait and read again. The write propagates on a delay and an
  immediate read can show nothing. Only a name that appears and then reverts
  means Entra is the source and the change belongs there
- No CI principal appears in `admins`
- A pipeline run on a non-protected branch fails to authenticate against the
  production policy

Result for this deployment, read 2026-08-11:

| Finding | Value |
| :--- | :--- |
| Existing principal | Application ID `9ff3bc2c-c77a-436a-a8b1-a740cd61cae0`. Entra holds an application of that ID named `SP-Terraform-fra-sqli-dev`, created 2026-07-30 |
| How Databricks holds it | Source reads Databricks, and the record carries an `External Id (from identity provider)`. 🔲 which kind it is, unverified |
| Name | Shown in the UI, resolved through the identity provider reference. The SCIM `displayName` attribute is empty, so the CLI, the API and `created_by` all report the application ID |
| Group membership | `admins`, `users`, and the Databricks-created users clone |
| Entitlements | Admin access, unrestricted cluster creation, instance pool creation, all directly assigned and editable on the detail page |
| CI principals | None |
| Creating one | A workspace admin created a Databricks managed principal through the SCIM API. `displayName` was accepted on creation and persisted |
| Its default entitlements | `workspace-access` and `databricks-sql-access`, neither requested |

Not passed. No CI principals exist, and their federation policies cannot be
written until the repository and its protected branches do.

> [!warning] Read back, and allow for lag
> - A SCIM patch setting `displayName` returned nothing and exited cleanly. `get`
>   showed no name. Later both `list` and `get` had it. The write had succeeded
>   and the read was too early
> - A clean exit is not a result. One negative read-back is not proof of failure
> - The UI is not a read-back. It resolved the name through the identity provider
>   while the API had none, so it can show a value no automated caller will see

> [!info] Workspace admin on the deployment principal is a constraint
> - An automation rule places it in `admins`, which is where its `CREATE CATALOG`
>   and `CREATE EXTERNAL LOCATION` come from
> - Explicit grants are the narrower alternative, parked at step 14
> - Do not demote before those grants exist, or the next deploy fails

> [!info] Where the owner splits
> - A workspace admin can create a Databricks managed principal, and
>   `displayName` sticks on creation
> - The federation policy is account-level and needs an account admin
> - Observed only for a Databricks managed principal created through the SCIM
>   API. Linking an Entra managed one at workspace level is 🔲 untested

### 5. Create the durable storage account for managed data

`Category: foundation` · `Owner: platform engineer` · `Inputs: enforced tag names, from step 3` · `Prerequisite: 🔲 ADR catalog and schema model, 🔲 ADR deployment model` · `Impact: Rework 3d`

Not a landing zone. Nothing writes files here directly. This is where the managed
tables of every catalog physically live.

**Why it matters**

- Data outlives the workspace. Terraform rebuilds the shell, and the catalogs and
  their files must not be rebuilt with it
- The workspace's own Unity Catalog container is the obvious shortcut and the
  wrong answer. It is created by the workspace and orphaned when the workspace
  goes, leaving your data in a converted resource group nobody manages
- A hierarchical namespace is required and cannot be turned on after the account
  exists
- The enforced tags must be set at creation. A deny policy refuses the apply
  rather than warning

**What getting the execution wrong costs** An account without a hierarchical
namespace is replaced, not amended. Data already written moves by hand.

> [!warning] This belongs in its own Terraform state
> Not merely a separate resource. If `terraform destroy` on the workspace can
> reach this account, the separation is decorative and the first regeneration
> takes the data with it.

> [!info] Container shape differs by environment
> | | Dev | Prod |
> | :--- | :--- | :--- |
> | Containers | One, a path per catalog | One per catalog |
> | Path | `abfss://managed@<acct>/<catalog>` | `abfss://<catalog>@<acct>/` |
> | External locations, step 7 | One | One per container |
> | Role assignment | Account scope | Container scope |
> | Azure retention and immutability | Not set | Per container, per the data protection ADR |
>
> Container-scoped grants in prod are the point of per-catalog containers. One
> account-scoped grant makes the split decorative.
>
> Drive the shape from a variable in one module rather than two configurations,
> or a prod apply exercises a path dev has never run.

**The play** 🔲

**Check** 🔲

> [!warning] Do not close the network yet
> Leave public network access as it is. Step 6 decides what the end state should
> be, and it differs by route. Closing it here locks out the very connections you
> are about to create, and the failures read as permission errors rather than
> network ones.

### 6. Open the serverless path to the managed storage account

`Category: foundation` · `Owner: account admin` · `Inputs: storage account resource ID, from step 5; workspace region, from step 1` · `Prerequisite: 🔲 ADR network posture` · `Impact: Rework 4d`

**Why it matters**

- Serverless compute runs in the Databricks-managed plane, not in your VNet. A
  storage account with a firewall refuses it, and the failure reads as a
  permissions error
- Two routes exist and they end in different states. Choosing is what the network
  posture ADR is for
- Either route also affects classic compute, which reaches the storage account
  from your VNet and needs its own path. Doing one and not the other breaks half
  your compute
- Allowlisting Databricks serverless subnet IDs stopped being supported on
  9 June 2026, so older internal guidance is wrong

**What getting the execution wrong costs** Both routes need someone on the Azure
side, so a mistake costs another round with another person rather than a retry.

**The play** 🔲

**Check** 🔲

> [!warning] Two routes, opposite end states
> **Route A, network security perimeter.** Recommended for storage in the
> workspace region.
> - Associate the account with a perimeter, leave it in transition mode
> - Inbound rule for the regional `AzureDatabricksServerless` service tag
> - End state: public network access stays on **Enabled from selected networks**.
>   Secured by Perimeter stops serverless reading external locations and returns
>   `PERMISSION_DENIED`
>
> **Route B, private endpoints via NCC.** For dedicated private connectivity.
> - NCC in the workspace region, attached to the workspace
> - One private endpoint rule per subresource. `dfs` for Unity Catalog, `blob`
>   for model serving
> - Each rule sits `PENDING` until someone with rights on the storage account
>   approves it in the portal
> - A separate private endpoint from your own VNet, for classic compute
> - End state: public network access **Disabled**
>
> Applying route A's rules and then route B's end state is the mistake that looks
> like a permissions bug.

> [!info] Either route
> - Enable **Allow trusted Microsoft services** on the storage account. Route A
>   cannot connect without it. Under route B's Disabled end state it is probably
>   inert, 🔲 unverified
> - Route B limits: 10 NCCs per region, 100 private endpoints per region, 50
>   workspaces per NCC. Databricks bills networking costs for serverless
>   connections
> - Whether network security perimeter exists in France Central is 🔲 unverified.
>   If not, route B is the only option

### 7. Register the external locations over it

`Category: foundation` · `Owner: workspace admin` · `Inputs: the containers, from step 5; a working network path, from step 6; an access connector and storage credential` · `Prerequisite: 🔲 ADR catalog and schema model, 🔲 ADR Access Connector granularity, 🔲 ADR deployment model` · `Impact: Rework 3d`

**Why it matters**

- A `MANAGED LOCATION` must sit inside an external location. That is the only
  reason these exist. No files land in them directly
- One per container, so one in dev and one per catalog in prod
- The connector identity needs **Storage Blob Data Contributor** and nothing
  else. The queue, storage account and EventGrid roles exist for file events,
  which this platform does not use

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

Confirm the input before starting. `isHnsEnabled` must be true.

```bash
az storage account list -g <resource-group> \
  --query "[].{name:name, hns:isHnsEnabled, publicNet:publicNetworkAccess}" -o table
```

> [!info] Which access connector
> - The existing one sits in the workspace's managed resource group, so its
>   principal ID is not readable by the operator and it dies with the workspace
> - A connector in a resource group you control is the durable choice, and needs
>   its own storage credential
> - The granularity ADR decides. Either way the role assignment is one, not four

### 8. Create account groups, including the metastore admin group

`Category: foundation` · `Owner: workspace admin, with an Entra admin only if the group must be created in Entra` · `Inputs: existing Entra groups and their sync mode, read in the play below` · `Prerequisite: 🔲 ADR workspace topology, 🔲 ADR ownership and grant model` · `Impact: Adjustable`

**Why it matters**

- Entra is the source of record for identity here, which is how workspace admin
  reaches a human at all. A group that already exists in Entra should be pulled
  in rather than duplicated, because a Databricks-side copy is a second thing to
  maintain and cannot be updated from Entra
- A workspace admin can do either from Settings, Identity and access, Manage next
  to Groups. The picker searches Entra directly and offers to create a new
  account group. An Entra admin is needed only when the group has to originate in
  Entra
- The house convention is usually one group per resource group, which models
  deployment rights rather than data access. This step adds a data-shaped set
  alongside, not instead
- Synced groups make this a ticket to whoever owns the on-premises directory.
  Cloud-only groups make it self-service

**What getting the execution wrong costs** 🔲

**The play** Inventory first, then create. The inventory half is written. The
creation half waits on the two ADRs.

- Filter directory reads. An unfiltered group list returns the whole tenant,
  including groups belonging to unrelated engagements
- Read `onPremisesSyncEnabled` on any group you intend to reuse

```bash
az ad group show --group <group-name> \
  --query "{name:displayName, id:id, onPremSync:onPremisesSyncEnabled}"
az ad group member list --group <group-name> \
  --query "[].{name:displayName, upn:userPrincipalName}" -o table
```

🔲 Creation half, once the ADRs land.

**Check** 🔲

Inventory result for this deployment, read 2026-08-11:

| Finding | Value |
| :--- | :--- |
| Group behind workspace admin | `SGA-RG-DATABRICKS-DEV` |
| Sync mode | Cloud-only, `onPremisesSyncEnabled` unset |
| Grants | Contributor on `RG-DATABRICKS-DEV` |
| Members | Two |
| Convention | One group per resource group |

### 9. Assign entitlements to each group

`Category: admin` · `Owner: workspace admin` · `Inputs: the groups, from step 8` · `Prerequisite: 🔲 ADR workspace topology` · `Impact: Adjustable`

> [!warning] This step is why the two after it work
> - Workspace permissions resolve against principals that exist in the workspace.
>   An Entra group does not, until assigned here
> - The ACLs at step 10 and the warehouse permissions at step 20 both depend on it
> - Two principal namespaces: Unity Catalog grants accept account-level
>   principals, workspace permissions do not. Any step granting a workspace
>   permission needs this one first

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Defaults are not minimal
> - A principal created through the SCIM API arrives with `workspace-access` and
>   `databricks-sql-access` unrequested. Observed, Databricks managed
> - One arriving another way gets a different set. The IdP-linked deployment
>   principal holds `allow-cluster-create` and `allow-instance-pool-create`
> - A new group defaults to Consumer access, Databricks SQL access and Workspace
>   access all on
> - Strip what is not needed rather than assuming the default is least privilege

> [!warning] Entitlements are no longer inherited from system groups
> - From 15 June 2026, entitlements are granted explicitly when a principal is
>   added to a workspace. `users` and `admins` no longer carry assignable ones
> - Auto-enabled 27 July 2026 for workspaces that had not opted in or out.
>   Enforced everywhere 14 September 2026
> - A workspace provisioned today starts in the new behaviour. Guidance saying
>   entitlements arrive by default describes the old one

### 10. Create secret scopes and scope ACLs

`Category: foundation` · `Owner: workspace admin` · `Inputs: the principals that receive scope ACLs, from step 8, usable here only once assigned to the workspace at step 9` · `Prerequisite: 🔲 ADR secret scope model` · `Impact: Rework 2d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] Secret ACLs use a different principal namespace
> - A Unity Catalog grant accepts `account users`. A secret scope ACL rejects it
> - Scope ACLs need a workspace principal, such as `users`
> - So a group from step 8 cannot hold an ACL until step 9 assigns it
> - Observed by attempting both principals against a live scope

### 11. Set the metastore admin to the group

`Category: foundation` · `Owner: account admin` · `Inputs: the metastore admin group, from step 8; the metastore ID, from step 1` · `Prerequisite: 🔲 ADR ownership and grant model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Starting state
> No metastore admin is assigned. The metastore reports `System user` as owner,
> which is what an automatically provisioned metastore looks like. Assignment is
> account admin only, and it is not something a workspace admin can work around.

### 12. Create catalogs with explicit MANAGED LOCATION

`Category: foundation` · `Owner: workspace admin` · `Inputs: metastore root storage state, from step 1; the external location that will hold managed data, from step 7` · `Prerequisite: 🔲 ADR metastore root storage, 🔲 ADR catalog and schema model` · `Impact: Lossy`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] What you create is open, what Databricks provisions is not
> - A catalog created here arrives `OPEN` and owned by the person who ran the
>   command. Observed, as a workspace admin through the CLI
> - The workspace catalog provisioning created is `ISOLATED` and owned by a group
> - Step 16 closes the first, step 14 owns the second

> [!warning] Why `Lossy` and not `Irreversible`
> - `ALTER CATALOG SET MANAGED LOCATION` exists on Databricks SQL and Runtime
>   18.1 and above, so the setting is changeable
> - It does not move managed tables and volumes that already exist
> - The setting is adjustable, the data already written is not. Academic on an
>   empty catalog, not academic one table in

### 13. Create schemas

`Category: foundation` · `Owner: workspace admin` · `Inputs: the catalogs, from step 12` · `Prerequisite: 🔲 ADR catalog and schema model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** The schema existing proves nothing. Write to it.

- Create a table, insert a row, read it back, drop the table
- Pass means the managed location is genuinely writable, not merely registered

This is the one checkpoint in the sequence and it earns its place here. Steps 14
to 26 all assume the storage path works. Finding out at step 25 that it does not
means unwinding twelve steps of grants, bindings and compute that were built on a
path Unity Catalog could never write to.

```bash
databricks -p "$P" api post /api/2.0/sql/statements --json @<file>
```

with a statement of `CREATE TABLE <catalog>.<schema>.probe (id INT)`, then an
`INSERT`, then a `SELECT`, then `DROP TABLE`. A warehouse has to exist to run it,
so either use one that is already there or bring step 20 forward for this check
alone.

### 14. Apply catalog-level grants

`Category: foundation` · `Owner: catalog owner, a workspace admin for anything created here` · `Inputs: the catalogs and schemas, from steps 12 and 13; the groups, from step 8` · `Prerequisite: 🔲 ADR ownership and grant model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] Starting state
> This step also owns the workspace catalog decision. Close it, keep it, or
> delete it, and say so explicitly. Leaving it alone is a decision too, and it is
> the one that leaves every workspace user able to create tables in it.

> [!info] Parked from step 4
> - The deployment principal gets `CREATE CATALOG` and `CREATE EXTERNAL LOCATION`
>   from `admins`, along with everything else a workspace admin can do
> - Granting those two directly is the narrower alternative
> - If taken up, the grants land here and the demotion follows this step, never
>   before it
> - The demotion is one checkbox, Admin access, on the principal's detail page
>   under Workspace settings, Identity and access

### 15. Grant the service principals their catalog access

`Category: foundation` · `Owner: catalog owner, a workspace admin for anything created here` · `Inputs: the CI principals, from step 4; the catalogs and schemas, from steps 12 and 13` · `Prerequisite: 🔲 ADR ownership and grant model, 🔲 ADR non-human identity model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 16. Apply catalog to workspace bindings

`Category: foundation` · `Owner: catalog owner, which is a workspace admin for anything created here` · `Inputs: the catalogs, from step 12; the list of workspaces on this metastore, from the baseline` · `Prerequisite: 🔲 ADR workspace topology` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Starting state
> - Objects created upstream are `ISOLATION_MODE_ISOLATED`, bound to this
>   workspace
> - Anything this sequence creates is open unless bound
> - Open means open to a multi-tenant metastore carrying other teams' catalogs,
>   not to one anonymous sibling workspace
> - Binding is the only thing stopping your catalog names appearing in their
>   Catalog Explorer

### 17. Enable the system table schemas

`Category: foundation` · `Owner: account admin` · `Inputs: none` · `Prerequisite: none` · `Impact: Lossy`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] Run as soon as an account admin is available
> - It sits at 18 for narrative reasons, not because it waits on anything
> - Consumes no ADR, depends on no step
> - System tables collect from enablement and never backfill. Every late day is
>   audit and billing history that does not exist

### 18. Create compute policies with enforced tags

`Category: compute` · `Owner: workspace admin` · `Inputs: the tag names enforced by Azure Policy, from step 3` · `Prerequisite: 🔲 ADR serverless or classic posture, 🔲 ADR tagging and budget route` · `Impact: Rework 5d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] This does not cover SQL warehouses
> - Compute policies govern clusters and jobs only
> - Serverless SQL spend is tagged by the budget policy at step 19, account admin
>   work
> - A warehouse accepts tags at creation and nothing enforces them
> - Four mechanisms across the estate: Azure Policy on Azure resources, compute
>   policies on clusters and jobs, budget policies on serverless, per-warehouse
>   tags. One vocabulary, nothing reconciling them
> - Steps 18 and 19 are complementary. This one alone leaves serverless spend
>   unattributable

### 19. Create the serverless budget policy

`Category: compute` · `Owner: account admin` · `Inputs: the tag scheme, from step 18` · `Prerequisite: 🔲 ADR tagging and budget route` · `Impact: Lossy`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 20. Create SQL warehouses and set permissions

`Category: compute` · `Owner: workspace admin` · `Inputs: the compute policies, from step 18; the groups that get CAN USE, from step 8, usable here only once assigned to the workspace at step 9` · `Prerequisite: 🔲 ADR serverless or classic posture` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] The workspace does not start policy-clean
> - A `Serverless Starter Warehouse` exists from provisioning, stopped, untagged
> - Step 18 cannot reach back and tag it
> - Decide: delete, tag or keep. Record which
> - Compute created before the policies stays untagged. Nothing fixes it after

> [!warning] The API default is not the UI default
> - UI default: serverless. API default: classic
> - For serverless from the API, set `warehouse_type` to `pro` **and**
>   `enable_serverless_compute` to `true`
> - Set both explicitly. This runbook deploys from the repo, not the UI

### 21. Apply admin settings

`Category: admin` · `Owner: workspace admin` · `Inputs: the current workspace settings, read in the play` · `Prerequisite: 🔲 ADR legacy surface posture` · `Impact: Rework 10d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Starting state
> - `ansi_mode` is `false` at workspace level. A legacy surface, and this step's
>   ADR owns it
> - Decide whether it stays and record why, rather than inheriting it by accident
> - Read with `databricks -p "$P" warehouses get-workspace-warehouse-config`

### 22. Apply classification tags, column masks, row filters

`Category: protection` · `Owner: 🔲 unverified, probably the catalog or table owner` · `Inputs: the schemas and tables to protect, from step 13; the groups the masks discriminate between, from step 8` · `Prerequisite: 🔲 ADR data protection model` · `Impact: Rework 8d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 23. Extend the network posture

`Category: protection` · `Owner: network team` · `Inputs: the established serverless path, from step 6` · `Prerequisite: 🔲 ADR network posture` · `Impact: Rework 4d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Starting state
> - Already in place from upstream: VNet injection, secure cluster connectivity,
>   front-end and back-end Private Link, route-table egress
> - The serverless path to ADLS is step 6, not here
> - Left here: whatever the ADR asks beyond those. Exfiltration controls,
>   firewall rules on other resources, anything the hub owner requires
> - If the ADR asks for none, close this step with a recorded decision

### 24. Configure monitoring and alerting

`Category: protection` · `Owner: platform engineer` · `Inputs: the system tables, from step 17` · `Prerequisite: none` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 25. Acceptance test

`Category: acceptance` · `Owner: test user` · `Inputs: a principal that can write to ADLS, from step 4 with its storage access from the role assignments at step 7; the bronze catalog and schema, from steps 12 and 13; a warehouse the test user can use, from step 20; the test user's group membership and entitlements, from steps 8 and 9` · `Prerequisite: none` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

---

## When it fails at step 25

Read the error rather than re-running the earlier steps.

| What you see | Where it actually broke |
| :--- | :--- |
| A serverless query cannot reach the storage account, and the error reads as permissions | Step 6, the private endpoint rule is `PENDING` rather than `ESTABLISHED`, public network access was closed before approval, or the account was set to Secured by Perimeter |
| A classic cluster cannot reach the storage account but serverless can | Step 6, the path from your own VNet is missing |
| The ingestion pipeline cannot write the table | Step 12 or 13, the catalog or schema has no usable managed location, or step 7's external location is missing |
| Writes fail with a storage authorisation error | Step 7, the connector identity lacks Storage Blob Data Contributor on that container |
| The table is created but the group cannot see the catalog | Step 14, `USE CATALOG` is missing |
| The catalog is visible but the table is not | Step 14, `USE SCHEMA` is missing |
| The table is visible but the query is denied | Step 14, `SELECT` is missing |
| The group member has no warehouse to run on | Step 20, no `CAN USE` on the warehouse |
| The group member cannot open the SQL editor at all | Step 9, the Databricks SQL access entitlement was not assigned explicitly |
| Everything works for you and nothing works for them | You are a workspace admin. Test as the test user, on their credentials, or you are testing nothing |

## Sources

Fetched and verified on the dates shown. Preconditions rests on all of them, not
on any one.

Fetched 2026-08-11:

- [Databricks administration overview](https://learn.microsoft.com/en-us/azure/databricks/admin/admin-concepts).
  Establishing the first account admin, and what a non-account-admin sees.
- [Admin privileges in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/admin-privileges).
  The workspace admin privilege list for auto-enabled workspaces, and the
  workspace catalog default grants.
- [Manage Unity Catalog metastores](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-metastore).
  Metastore-level storage is optional and absent from automatically created
  metastores. Account console navigation for steps 1 and 11.
- [Specify a managed storage location in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/managed-storage).
  Managed storage precedence, and `ALTER CATALOG SET MANAGED LOCATION` on
  Databricks Runtime 18.1 and above, which affects only objects created after
  the change.

Added 2026-08-11 for step 2:

- [Connect to serverless compute](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/).
  Serverless is available by default in most workspaces and needs no enablement,
  provided Unity Catalog is on and the region supports it.
- [Features with limited regional availability](https://learn.microsoft.com/en-us/azure/databricks/resources/feature-region-support).
  The serverless, system tables and ingestion tables by region.
- [SQL warehouse types](https://learn.microsoft.com/en-us/azure/databricks/compute/sql-warehouse/warehouse-types).
  Classic, pro and serverless capabilities, and the differing UI and API
  defaults, used at step 20.

Added 2026-08-11 for step 6:

- [Serverless compute plane networking](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/).
  What an NCC is, and the end of serverless subnet allowlisting on 9 June 2026.
- [Configure private connectivity to Azure resources](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-private-link).
  NCC creation, private endpoint rules, the Azure-side approval, the limits, and
  the requirement that classic compute also use private endpoints once a
  resource is restricted.

Fetched 2026-08-12, for the owner corrections and the file event roles:

- [Manage groups](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-groups).
  Workspace admins can create account groups and assign them to a workspace.
  Steps 8 and 9.
- [Workspace-catalog binding](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/access-control/workspace-catalog-binding).
  Binding needs metastore admin, catalog owner or `MANAGE`, not account admin.
  Step 16.
- [Manage service principals](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-service-principals).
  Creation is documented, renaming an existing principal is not. Step 4.
- [Manage external locations](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/manage-external-locations).
  File events on by default, and the four role assignments. Only one of the four
  survives now that no files land in storage. Dated 2026-08-11, and it
  contradicts the June ADLS page on the EventGrid role name.
- [Configure an Azure network security perimeter](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-firewall-config).
  Route A, and why Secured by Perimeter breaks serverless. Step 6.
- [Delete a workspace](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace/delete-workspace).
  The workspace catalog, managed resource group, storage and access connector all
  survive deletion unless force deleted.
- [Deploy a workspace using the Azure Portal](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace/create-workspace).
  No templates or sample catalogs at creation. Workspace type Hybrid means
  classic.

Carried from [[dbr-RG-to-working-non-admin-user]], verified there on 2026-08-10:

- [Workspace entitlements and the 15 June 2026 system group change](https://learn.microsoft.com/en-us/azure/databricks/security/auth/entitlements),
  used at step 9.

> [!todo] 🔲 Steps 11, 15, 16, 20, 22 to 26 are not yet sourced
> Verify per claim before status leaves Draft.

<!--
Version: 0.9 | Last Updated: 2026-08-11 | Status: Draft
-->
