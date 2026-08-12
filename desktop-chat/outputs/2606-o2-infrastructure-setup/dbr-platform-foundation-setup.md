# Databricks platform foundation setup

> One ordered sequence from a provisioned but unused workspace to a governed
> bronze table landing from ADLS. Decisions are not taken here. They arrive as
> accepted ADRs, and each step names the one it consumes.
> Upstream: [[dbr-RG-to-working-non-admin-user]], which ends where the
> provisioned baseline below begins.

This runbook assumes one configuration and does not generalise beyond it: a
Terraform-provisioned, VNet-injected, Premium workspace, automatically enabled
for Unity Catalog, where workspace admin reaches a human through an Entra group
and account admin is held elsewhere. Greenfield here means unused, not empty.
The workspace already contains infrastructure. It contains no work.

## What counts as done

Step 26 is the finish line: a service principal writes a file to ADLS, a file
event fires, Auto Loader lands a bronze table in a governed catalog, and a group
member reads it. Deployed from the repo, not from the UI.

Two weaker finish lines are easy to mistake for it.

| Stops at | Proves | Why it is not enough |
| :--- | :--- | :--- |
| A table exists in the catalog | Storage access and the catalog work | Nothing proves an event triggered it, or that anyone but its creator can read it |
| Auto Loader ran once, by hand | The ingest code works | A hand-run load is a demo. The event path is the thing that has to hold at 3am |

## Preconditions

### Entry condition

The gate is per step, not up front. An ADR must be Accepted before the first
step that consumes it, and not before. The `First consumed` column below is
therefore a deadline, one per ADR. Steps 1, 2, 3, 18, 25 and 26 consume no ADR
and can run against an empty decision record.

### ADRs

Ordered by the first step that consumes them. The `Depends on` column carries the
order they must be accepted in, which is not the same order.

| ADR | Subject | First consumed | Also consumed by | Depends on |
| :--- | :--- | :--- | :--- | :--- |
| 🔲 | Non-human identity model | 4 | 16 | — |
| 🔲 | Deployment model | 5 | Every step that changes state | — |
| 🔲 | Catalog and schema model | 5 | 7, 13, 14 | Workspace topology |
| 🔲 | Network posture | 6 | 24 | Serverless or classic posture |
| 🔲 | Access Connector and external location granularity | 7 | 8 | Catalog and schema model, Metastore root storage |
| 🔲 | File event mechanism | 8 | — | Access Connector granularity |
| 🔲 | Workspace topology | 9 | 10, 17 | — |
| 🔲 | Ownership and grant model | 9 | 12, 15, 16 | Workspace topology, Catalog and schema model |
| 🔲 | Secret scope model | 11 | — | — |
| 🔲 | Metastore root storage and MANAGED LOCATION policy | 13 | — | Workspace topology |
| 🔲 | Serverless or classic posture | 19 | 21 | — |
| 🔲 | Tagging and budget route | 19 | 20 | Serverless or classic posture |
| 🔲 | Legacy surface posture | 22 | — | — |
| 🔲 | Data protection model | 23 | — | Catalog and schema model |

Acceptance order, derived from the `Depends on` column: workspace topology first,
then metastore root storage and the catalog and schema model, then Access
Connector granularity and the ownership and grant model, then the rest.

> [!warning] Two ADRs are needed far earlier than their row suggests
> Network posture is first consumed at step 6, because serverless compute cannot
> reach a firewalled storage account without a decision on how. It depends on the
> serverless or classic posture ADR, which therefore has to be accepted before
> step 6 as well, despite showing 18 in its own row. Both are early, and network
> posture is owned outside this team. Start them first.
>
> The data protection ADR at step 23 is the one that can genuinely lag, provided
> nothing sensitive lands before it.

### Identities

| Role | Needed for | Held by |
| :--- | :--- | :--- |
| Account admin | 4, 6, 12, 15, 16, 18, 20, 23 | 🔲 |
| Workspace admin | 1, 2, 7, 9, 10, 11, 13, 14, 17, 19, 21, 22 | gmourgues@sqli.com |
| Platform engineer | 3, 5, 8, 25 | 🔲 |
| Entra admin | 9, only if the group is created in Entra rather than pulled in | 🔲 |
| Network team | 24 | 🔲 |
| Test user | 26 | 🔲 |

Workspace admin is not granted to a person here. It arrives through an Entra
group and materialises as membership of the workspace `admins` group. The
control point is therefore Entra group membership, not anything inside
Databricks.

### What to ask the account admin for

Eight steps need an account-level Databricks role that nobody running this
sequence is likely to hold. Raise them as one request rather than eight
interruptions. Step numbers are not a request, so this is what to actually ask
for.

| Request | Unblocks |
| :--- | :--- |
| A federation policy per CI service principal, once the repository and its protected branches exist | 4 |
| Serverless network access to the ADLS account, either a network security perimeter rule or a network connectivity configuration with private endpoint rules | 6 |
| Assign the metastore admin role to a named group | 12 |
| Catalog grants and service principal grants | 15, 16 |
| Enable the system table schemas | 18 |
| Create the serverless budget policy | 20 |
| Classification tags, column masks and row filters | 23 |
| Set the display name on the account-level service principal record, if it is empty | 4 |

The first two carry the longest lead times. Step 6 also needs someone on the
Azure side, so it is two people and not one.

> [!info] Three things are not on this list, and were until tested
> Creating account groups, assigning them to the workspace with entitlements, and
> binding a catalog to workspaces are all workspace admin actions. Verified in
> the UI on 2026-08-12 by doing them. Asking an account admin for any of the
> three wastes their time and yours.

### Tooling

Install before step 1, on the machine that will run the sequence.

| Tool | Needed for | Install |
| :--- | :--- | :--- |
| Databricks CLI | 1 onward | `brew tap databricks/tap && brew install databricks` |
| Azure CLI | 3, 5, 6, 8 | `brew install azure-cli` |
| Terraform | Every step that changes state | `brew install terraform` |

Authenticate the Databricks CLI with OAuth against the workspace host. The
browser opens, so run it yourself rather than from an agent session.

```bash
databricks auth login --host https://<workspace-host>
```

The Databricks CLI matters earlier than it looks. It reads metastore state
without any compute existing, which is the only way to complete step 1 before a
warehouse exists, and creating a warehouse early would land untagged compute
ahead of the policies in step 19. Homebrew will refuse the Databricks formula
until the tap is trusted: `brew trust --formula databricks/tap/databricks`.

### Provisioned baseline

The state the workspace should already be in when step 1 begins, all of it
produced upstream rather than by this sequence. Verify it before step 1, not
during. Each row has a check, because an expectation without a check is an
assumption written down.

Set `P` to your CLI profile name first. A failing row stops the sequence. It is a
question for the Terraform, not something to fix by hand here, because a manual
fix drifts from state and the next apply reverts it.

Resolve the workspace identity before anything else. Every Azure-side step takes
its scope from it, and the managed resource group is not it. That group is where
Databricks puts the objects it provisions for itself, and you will usually not be
able to read it.

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
> The workspace catalog arrives with open default grants. Every workspace user
> holds `USE CATALOG` on it, plus `USE SCHEMA`, `CREATE TABLE`, `CREATE VOLUME`,
> `CREATE MODEL`, `CREATE FUNCTION` and `CREATE MATERIALIZED VIEW` on its
> `default` schema. That is a live open door from the moment the workspace
> exists. Step 15 decides what happens to it. Do not discover it at step 26.

### Environment checks

Two things the baseline cannot tell you, both cheap, both of which have already
changed this plan once.

**Someone holds account admin.** Eight steps need it, and it does not flow from the
Entra group that makes you a workspace admin. If nobody in the account holds it,
a Microsoft Entra ID Global Administrator must sign in to the account console
once, which auto-creates their account admin role, and then delegate it under
User management, Roles tab. There is no other route. The fastest test of whether
you hold it: open `accounts.azuredatabricks.net`. An account admin lands on the
console with a left nav. Everyone else gets a workspace picker.

**Who else is on the metastore.** A metastore is one per region and it is
multi-tenant. Expect catalogs owned by people outside your workspace, created
years before it. Their names and schema names are visible to you from Catalog
Explorer without any grant, and yours are visible to them unless step 17 binds
them. A greenfield workspace does not imply a greenfield metastore.

Read 2026-08-12: `metastore_azure_francecentral` was created in June 2024 and
carries catalogs owned by a user who is not in this workspace, with schemas dated
October 2024. One of them is already called `bronzes`.

> [!todo] 🔲 To be defined
> What steps 1 to 3 assume about the tenant and subscription beyond the above.

## How to read a step

Each step carries the same fields.

- **Category** — gate, foundation, compute, admin, protection, acceptance
- **Owner, inputs, prerequisite, impact** — one line, machine-readable
- **Inputs** — the facts this step consumes and where each was produced, either a
  baseline row or an earlier step. A step with an unstated input is a step that
  will run against the wrong thing without telling you. Every input must name a
  producer. One that names none is a missing step
- **Prerequisite** — an ADR named here carries 🔲 until it is Accepted, and a step
  with any 🔲 prerequisite cannot start. Clearing the marker is what makes the
  step runnable. An ADR also carries its own `Depends on` chain, so accepting one
  whose dependency is still open unblocks nothing
- **Why it matters** — what this step is for and what breaks without it. Not why
  the option was chosen. That is in the ADR
- **What getting the execution wrong costs** — irreversible, lossy, rework in
  days, or adjustable
- **The play** — the commands or clicks
- **Check** — what passes or fails. A step that writes is checked by reading back
  what should have changed, not by the command not erroring. One negative
  read-back is not proof of failure: reads can lag writes and two endpoints can
  disagree, so read again and read a second surface before concluding
- **Clean up** — any check that creates something ends with the command that
  removes it, in the same step. Never leave the reader to remember. A runbook
  that leaves residue teaches the reader to leave residue, and residue in a
  shared resource group outlives the person who made it

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
- Silver and gold layers, and any transformation beyond the bronze landing
- Multi-region and disaster recovery
- Network design beyond what steps 6 and 24 require. The hub and spoke topology
  itself is upstream

## Proven against a live workspace

Exercised on 2026-08-11 and 2026-08-12 against a real workspace, using throwaway
objects that were deleted afterwards. This proves the platform permits the step
and that the operator holds the rights for it. It does not mean the step is done,
and it does not mean the Terraform will produce the same result.

| Step | What was exercised | Verdict |
| :--- | :--- | :--- |
| 1, 2, 3 | The reads, in full | Passed |
| 4 | Created a Databricks managed principal with a display name, as a workspace admin | Creation works. Federation untested |
| 5 | Created a tagged ADLS account with hierarchical namespace and a container | Passed, and an untagged create was refused first, so the deny policy bites |
| 6 | Nothing | Untested. Needs an account admin |
| 7, 8 | Attempted the prerequisites | **Failed.** The operator cannot write role assignments and cannot read the access connector |
| 9, 10 | Created an account group with entitlements, as a workspace admin | Passed |
| 11 | Created a scope, a secret and an ACL | Passed, and it exposed that account-level principals are refused here |
| 13, 14 | Created a catalog with an explicit managed location and a schema, then wrote and read a table | Passed. The managed storage path works end to end |
| 15, 16 | Granted a group and a service principal on a catalog | Passed |
| 17 | Confirmed the binding controls are present and editable | Passed |
| 19 | Created a compute policy with an enforced tag | Passed |
| 21 | Created a serverless warehouse with tags | Passed |
| 12, 18, 20, 23 | Nothing | Untested. Need an account admin |
| 22, 24, 25, 26 | Nothing | Untested |

The two that failed are the important ones. Steps 7 and 8 cannot be performed
from the operator's position at all, which is why the storage path has to come
from the Terraform. See [[2026-08-11-databricks-terraform-changes]].

---

### 1. Read metastore root storage state

`Category: gate` · `Owner: workspace admin` · `Inputs: none` · `Prerequisite: Databricks CLI authenticated` · `Impact: Adjustable`

**Why it matters**

- Step 13 branches on whether the metastore carries a root storage location
- With no root, every catalog must name an explicit `MANAGED LOCATION`
- With a root set, a catalog created without `MANAGED LOCATION` inherits it
  silently, and the managed data lands in storage you may not own
- The metastore is regional and shared, so its state was probably decided before
  your workspace existed

**What getting the execution wrong costs** The read changes nothing. Skipping it
turns step 13 from a decision into an accident.

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

Passed. No metastore root, so nothing to unwind before step 13.

### 2. Confirm serverless availability and enablement in region

`Category: gate` · `Owner: workspace admin` · `Inputs: region, from step 1` · `Prerequisite: Databricks CLI authenticated` · `Impact: Adjustable`

**Why it matters**

- Steps 19 and 20 consume the serverless or classic posture ADR, which cannot be
  decided without this
- Two independent conditions, either of which can be false alone: the region
  supports serverless, and the workspace has it enabled
- If serverless is out, step 21 becomes a classic cluster with a different
  permission model
- Step 20 loses its subject, since a serverless budget policy governs nothing
  without serverless spend

**What getting the execution wrong costs** The read is free. Assuming the answer
costs a compute policy and a budget route built around compute that does not
exist, discovered at step 21.

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
- The enforced tag names bind step 19. A different vocabulary on the Databricks
  side gives two schemes and cost reporting that cannot be joined across them
- Step 8 cannot create a file event queue if `Microsoft.EventGrid` is
  unregistered, and registering it needs subscription rights the operator may not
  hold

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
> The tag policy only evaluates resource types that support tags and location. It
> does not apply to resource groups, and it skips child resources that carry no
> tags of their own, such as the network interface behind a private endpoint.
> That is why some untagged resources sit in a resource group under a deny policy
> without tripping it.

### 4. Create the CI/CD service principals

`Category: foundation` · `Owner: account admin` · `Inputs: existing service principals and their Entra records, read in the play; GitLab project and protected branches, from the baseline IaC repo row` · `Prerequisite: 🔲 ADR non-human identity model` · `Impact: Lossy`

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
> A workspace SCIM patch setting `displayName` returned nothing and exited
> cleanly. `get` showed no name immediately afterwards. Later both `list` and
> `get` reported it. The write had succeeded and the read-back was too early.
>
> So a clean exit is not a result, and one negative read-back is not proof of
> failure either. Read again before concluding.
>
> The UI is not a read-back. It resolved a name through the identity provider
> while the API had none, so it can show a value that no automated caller will
> ever see.

> [!info] Workspace admin on the deployment principal is a constraint, not a choice
> An existing automation rule places the deployment principal in `admins`, which
> is also where its `CREATE CATALOG` and `CREATE EXTERNAL LOCATION` privileges
> come from. Replacing that with explicit grants on the principal is possible and
> is parked as a note against step 15. Do not attempt it before those grants
> exist, or the next deploy fails.

> [!info] The owner splits, and here is where
> A workspace admin can create a Databricks managed service principal, and
> `displayName` is set on creation and persists. The federation policy is
> account-level and needs an account admin.
>
> Observed under one assumption: a Databricks managed principal created through
> the workspace SCIM API. Whether an Entra managed principal can be linked at
> workspace level is 🔲 untested, and the non-human identity ADR is what decides
> whether that matters.

### 5. Create the bronze ADLS storage account

`Category: foundation` · `Owner: platform engineer` · `Inputs: workspace resource group, from the baseline; enforced tag names, from step 3` · `Prerequisite: 🔲 ADR catalog and schema model, 🔲 ADR deployment model` · `Impact: Rework 3d`

**Why it matters**

- Everything downstream reads and writes here. Step 7 registers an external
  location over it, step 8 puts a file event queue on it, and step 26 lands the
  bronze table in it
- A hierarchical namespace is required for an external location and cannot be
  turned on after the account exists
- The enforced tags must be set at creation. A deny policy refuses the apply
  rather than warning

**What getting the execution wrong costs** An account without a hierarchical
namespace is replaced, not amended, and anything already written to it moves by
hand.

**The play** 🔲

**Check** 🔲

> [!warning] Do not close the network yet
> Leave public network access as it is. Step 6 decides what the end state should
> be, and it differs by route. Closing it here locks out the very connections you
> are about to create, and the failures read as permission errors rather than
> network ones.

### 6. Open the serverless path to ADLS

`Category: foundation` · `Owner: account admin` · `Inputs: ADLS resource ID, from step 5; workspace region, from step 1` · `Prerequisite: 🔲 ADR network posture` · `Impact: Rework 4d`

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

> [!warning] Two routes, and blending them is the failure mode
> **Route A, network security perimeter.** What Databricks recommends for storage
> in the workspace region. Associate the account with a perimeter, leave it in
> transition mode, add an inbound rule for the regional
> `AzureDatabricksServerless` service tag. End state: keep public network access
> on **Enabled from selected networks**. Setting it to Secured by Perimeter stops
> serverless reading external locations and returns `PERMISSION_DENIED`.
>
> **Route B, private endpoints through a network connectivity configuration.** For
> dedicated private connectivity. Create the NCC in the workspace region, attach
> it to the workspace, add one private endpoint rule per subresource, `dfs` for
> Unity Catalog and `blob` as well for model serving. Each rule sits `PENDING`
> until someone with rights on the storage account approves it in the portal. Add
> a separate private endpoint from your own VNet for classic compute. End state:
> only now set public network access to **Disabled**.
>
> The end states are opposites. Applying route A's rule set and then route B's end
> state is the mistake that looks like a permissions bug.

> [!info] Either route
> Enable **Allow trusted Microsoft services to access this resource** on the
> storage account. File events need it and Databricks cannot connect without it
> once public access is restricted.
>
> Route B limits: 10 NCCs per region, 100 private endpoints per region, 50
> workspaces per NCC. Databricks bills networking costs when serverless connects
> to your resources. Whether network security perimeter is available in France
> Central is 🔲 unverified; if it is not, route B is the only option.

### 7. Register the ADLS external location

`Category: foundation` · `Owner: workspace admin` · `Inputs: access connector and storage credential, from the baseline; the bronze ADLS container, from step 5; an established private endpoint path, from step 6` · `Prerequisite: 🔲 ADR catalog and schema model, 🔲 ADR Access Connector granularity, 🔲 ADR deployment model` · `Impact: Rework 3d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

Confirm the input exists before starting. `isHnsEnabled` must be true.

```bash
az storage account list -g <resource-group> \
  --query "[].{name:name, hns:isHnsEnabled, publicNet:publicNetworkAccess}" -o table
```

> [!info] Starting state
> The access connector and storage credential already exist and are covered by
> the baseline, which is why neither is a step. If the granularity ADR calls for
> a second access connector, that work returns here rather than as a step of its
> own.
>
> Read 2026-08-11: no storage account yet in `RG-DATABRICKS-DEV`.

### 8. Enable file events on the new external location

`Category: foundation` · `Owner: platform engineer` · `Inputs: the external location, from step 7` · `Prerequisite: 🔲 ADR file event mechanism, 🔲 ADR Access Connector granularity` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] This step verifies rather than enables
> File events are on by default for every new external location, so the one
> created at step 7 probably already has them. What this step confirms is that
> they actually configured, because they silently do not when the storage
> credential lacks the roles below. If the credential is short, external location
> creation shows a validation warning and offers Force create, which produces a
> location with file events off.

> [!warning] File events need three more role assignments than reading does
> All on the Access Connector's managed identity. Three on the storage account,
> one on the resource group containing it.
>
> | Role | Scope |
> | :--- | :--- |
> | Storage Blob Data Contributor | Storage account |
> | Storage Queue Data Contributor | Storage account |
> | Storage Account Contributor | Storage account |
> | EventGrid Data Contributor | Resource group |
>
> Without the last two you configure the queue and the Event Grid subscription by
> hand for every location, and Databricks will not support that setup. Also
> enable Allow trusted Microsoft services on the storage account.
>
> Two live Microsoft pages disagree on the fourth role. The June 2026 ADLS page
> calls it EventGrid EventSubscription Contributor, the August 2026 page calls it
> EventGrid Data Contributor. The fresher name is written here. If file events
> fail to configure, check that first.
>
> None of these can be granted by the operator. See step 7.

### 9. Create account groups, including the metastore admin group

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

### 10. Assign entitlements to each group

`Category: admin` · `Owner: workspace admin` · `Inputs: the groups, from step 9` · `Prerequisite: 🔲 ADR workspace topology` · `Impact: Adjustable`

> [!warning] This step is why the two after it work
> Workspace-level permissions resolve against principals that exist in the
> workspace, and a group created in Entra does not until it is assigned here. So
> the ACLs at step 11 and the warehouse permissions at step 21 both depend on
> this step having run.
>
> It sits at 10 for that reason and not for narrative tidiness. Databricks has
> two principal namespaces: Unity Catalog grants accept account-level principals,
> workspace permissions do not. Any step granting a workspace permission needs
> this one first.

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Defaults are not minimal
> A service principal created through the workspace SCIM API arrives holding
> `workspace-access` and `databricks-sql-access` without being asked. Observed on
> a Databricks managed principal. One arriving another way gets a different set:
> the identity-provider-linked deployment principal holds `allow-cluster-create`
> and `allow-instance-pool-create` instead. Strip what a principal does not need
> rather than assuming the default is least privilege.

> [!warning] Entitlements are no longer inherited from system groups
> Databricks began rolling out a change on 15 June 2026 in which entitlements are
> granted explicitly when a principal is added to a workspace, and the `users`
> and `admins` system groups no longer carry assignable entitlements. It
> auto-enabled on 27 July 2026 for workspaces that had not opted in or out, and
> is enforced everywhere on 14 September 2026. A workspace provisioned today
> starts in the new behaviour. Guidance saying these entitlements arrive by
> default is describing the old one.

### 11. Create secret scopes and scope ACLs

`Category: foundation` · `Owner: workspace admin` · `Inputs: the principals that receive scope ACLs, from step 9, usable here only once assigned to the workspace at step 10` · `Prerequisite: 🔲 ADR secret scope model` · `Impact: Rework 2d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] Secret ACLs use a different principal namespace from Unity Catalog
> A Unity Catalog grant accepts `account users`. A secret scope ACL rejects it
> and requires a principal that exists in the workspace, such as `users`. A group
> created in Entra at step 9 therefore cannot hold a scope ACL until step 10 has
> assigned it to the workspace.
>
> Observed by attempting both principals against a live scope.

### 12. Set the metastore admin to the group

`Category: foundation` · `Owner: account admin` · `Inputs: the metastore admin group, from step 9; the metastore ID, from step 1` · `Prerequisite: 🔲 ADR ownership and grant model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Starting state
> No metastore admin is assigned. The metastore reports `System user` as owner,
> which is what an automatically provisioned metastore looks like. Assignment is
> account admin only, and it is not something a workspace admin can work around.

### 13. Create catalogs with explicit MANAGED LOCATION

`Category: foundation` · `Owner: workspace admin` · `Inputs: metastore root storage state, from step 1; the external location that will hold managed data, from step 7` · `Prerequisite: 🔲 ADR metastore root storage, 🔲 ADR catalog and schema model` · `Impact: Lossy`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] What you create is open, what Databricks provisions is not
> A catalog created here arrives with `isolation_mode: OPEN`, visible to every
> workspace on the metastore, and owned by the person who ran the command. The
> workspace catalog that provisioning created is `ISOLATED` and owned by a group.
> Step 17 closes the first, step 15 owns the second. Observed by creating a
> catalog as a workspace admin through the CLI.

> [!warning] Impact downgraded from Irreversible, and why that is not a reprieve
> `ALTER CATALOG SET MANAGED LOCATION` exists on Databricks SQL and Runtime 18.1
> and above, so the setting is changeable. It does not move managed tables and
> volumes that already exist. The setting is adjustable, the data already written
> is not, which is `Lossy` rather than `Irreversible`. On an empty catalog the
> distinction is academic. One table in, and it is not.

### 14. Create schemas

`Category: foundation` · `Owner: workspace admin` · `Inputs: the catalogs, from step 13` · `Prerequisite: 🔲 ADR catalog and schema model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** The schema existing proves nothing. Write to it.

- Create a table, insert a row, read it back, drop the table
- Pass means the managed location is genuinely writable, not merely registered

This is the one checkpoint in the sequence and it earns its place here. Steps 15
to 26 all assume the storage path works. Finding out at step 26 that it does not
means unwinding twelve steps of grants, bindings and compute that were built on a
path Unity Catalog could never write to.

```bash
databricks -p "$P" api post /api/2.0/sql/statements --json @<file>
```

with a statement of `CREATE TABLE <catalog>.<schema>.probe (id INT)`, then an
`INSERT`, then a `SELECT`, then `DROP TABLE`. A warehouse has to exist to run it,
so either use one that is already there or bring step 21 forward for this check
alone.

### 15. Apply catalog-level grants

`Category: foundation` · `Owner: account admin` · `Inputs: the catalogs and schemas, from steps 13 and 14; the groups, from step 9` · `Prerequisite: 🔲 ADR ownership and grant model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] Starting state
> This step also owns the workspace catalog decision. Close it, keep it, or
> delete it, and say so explicitly. Leaving it alone is a decision too, and it is
> the one that leaves every workspace user able to create tables in it.

> [!info] Parked from step 4
> The deployment principal holds `CREATE CATALOG` and `CREATE EXTERNAL LOCATION`
> through membership of `admins`, which also gives it everything else a workspace
> admin can do. Granting those two privileges to the principal directly is the
> narrower alternative. If it is taken up, the grants land here and the demotion
> follows this step, never before it. The demotion itself is one checkbox,
> Admin access, on the principal's detail page under Workspace settings,
> Identity and access.

### 16. Grant the service principals their catalog access

`Category: foundation` · `Owner: account admin` · `Inputs: the CI principals, from step 4; the catalogs and schemas, from steps 13 and 14` · `Prerequisite: 🔲 ADR ownership and grant model, 🔲 ADR non-human identity model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 17. Apply catalog to workspace bindings

`Category: foundation` · `Owner: catalog owner, which is a workspace admin for anything created here` · `Inputs: the catalogs, from step 13; the list of workspaces on this metastore, from the baseline` · `Prerequisite: 🔲 ADR workspace topology` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Starting state
> The objects created upstream are already `ISOLATION_MODE_ISOLATED`, so they are
> bound to this workspace rather than open to the metastore. Anything this
> sequence creates is open by default unless bound.
>
> Open means open to a multi-tenant metastore carrying other teams' catalogs, not
> to one anonymous sibling workspace. Binding is the only thing that stops your
> catalog names appearing in their Catalog Explorer.

### 18. Enable the system table schemas

`Category: foundation` · `Owner: account admin` · `Inputs: none` · `Prerequisite: none` · `Impact: Lossy`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] Run this as early as an account admin is available
> It sits at 18 because that is where it fits the narrative, not because it has
> to wait. System tables collect from the moment they are enabled and never
> backfill, so every day it is late is a day of audit and billing history that
> does not exist. It consumes no ADR and depends on no other step.

### 19. Create compute policies with enforced tags

`Category: compute` · `Owner: workspace admin` · `Inputs: the tag names enforced by Azure Policy, from step 3` · `Prerequisite: 🔲 ADR serverless or classic posture, 🔲 ADR tagging and budget route` · `Impact: Rework 5d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] This does not cover SQL warehouses
> Compute policies govern clusters and jobs. Serverless SQL spend is tagged by
> the budget policy at step 20, which is account admin work. A warehouse also
> accepts tags directly at creation, and nothing enforces them.
>
> So four tagging mechanisms exist across the estate: Azure Policy on Azure
> resources, compute policies on clusters and jobs, budget policies on
> serverless, and per-warehouse tags set by whoever creates the warehouse. They
> share one vocabulary and nothing reconciles them. Steps 19 and 20 are
> complementary, not alternatives, and doing this one alone leaves serverless
> spend unattributable.

### 20. Create the serverless budget policy

`Category: compute` · `Owner: account admin` · `Inputs: the tag scheme, from step 19` · `Prerequisite: 🔲 ADR tagging and budget route` · `Impact: Lossy`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 21. Create SQL warehouses and set permissions

`Category: compute` · `Owner: workspace admin` · `Inputs: the compute policies, from step 19; the groups that get CAN USE, from step 9, usable here only once assigned to the workspace at step 10` · `Prerequisite: 🔲 ADR serverless or classic posture` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] The workspace does not start policy-clean
> A `Serverless Starter Warehouse` already exists from provisioning, stopped and
> carrying no tags. Step 19 cannot reach back and tag it. Decide whether it is
> deleted, tagged or kept, and record which. Compute created before the policies
> exist stays untagged, and nothing fixes that after the fact.

> [!warning] The API default is not the UI default
> Through the UI the default warehouse type is serverless. Through the SQL
> warehouses API with default parameters it is classic. To get serverless from
> the API, set `warehouse_type` to `pro` and `enable_serverless_compute` to
> `true`. Set both explicitly rather than relying on either default, because this
> runbook deploys from the repo and not from the UI.

### 22. Apply admin settings

`Category: admin` · `Owner: workspace admin` · `Inputs: the current workspace settings, read in the play` · `Prerequisite: 🔲 ADR legacy surface posture` · `Impact: Rework 10d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Starting state
> The workspace SQL config already carries one non-default that belongs to this
> step's ADR: `ansi_mode` is set to `false` at workspace level. That is a legacy
> surface. Decide whether it stays, and record why, rather than leaving it as an
> accident of provisioning. Read it with
> `databricks -p "$P" warehouses get-workspace-warehouse-config`.

### 23. Apply classification tags, column masks, row filters

`Category: protection` · `Owner: account admin` · `Inputs: the schemas and tables to protect, from step 14; the groups the masks discriminate between, from step 9` · `Prerequisite: 🔲 ADR data protection model` · `Impact: Rework 8d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 24. Extend the network posture

`Category: protection` · `Owner: network team` · `Inputs: the established serverless path, from step 6` · `Prerequisite: 🔲 ADR network posture` · `Impact: Rework 4d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Starting state
> VNet injection, secure cluster connectivity, front-end and back-end Private
> Link and route-table egress are already in place from upstream and belong to
> the provisioned baseline. The serverless path to ADLS is step 6. What is left
> here is whatever the ADR asks for beyond those: exfiltration controls, firewall
> rules on other resources, and anything the hub owner requires. If the ADR asks
> for none of it, this step closes with a recorded decision rather than a change.

### 25. Configure monitoring and alerting

`Category: protection` · `Owner: platform engineer` · `Inputs: the system tables, from step 18` · `Prerequisite: none` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 26. Acceptance test

`Category: acceptance` · `Owner: test user` · `Inputs: a principal that can write to ADLS, from step 4 with its storage access from the role assignments at step 7; the bronze catalog and schema, from steps 13 and 14; a warehouse the test user can use, from step 21; the test user's group membership and entitlements, from steps 9 and 10` · `Prerequisite: none` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

---

## When it fails at step 26

Read the error rather than re-running the earlier steps.

| What you see | Where it actually broke |
| :--- | :--- |
| The service principal cannot write to ADLS | Step 7, or the Azure role assignment behind the access connector |
| A serverless query cannot reach the storage account, and the error reads as permissions | Step 6, the private endpoint rule is `PENDING` rather than `ESTABLISHED`, or public network access was closed before it was approved |
| A classic cluster cannot reach the storage account but serverless can | Step 6, the private endpoint from your own VNet is missing |
| The file lands but no event fires | Step 8, file events are not enabled on the location created at step 7 |
| The event fires but Auto Loader cannot read the queue | Step 8, the queue role assignment |
| Auto Loader runs but cannot write the table | Step 13 or 14, the catalog or schema has no usable managed location |
| The table is created but the group cannot see the catalog | Step 15, `USE CATALOG` is missing |
| The catalog is visible but the table is not | Step 15, `USE SCHEMA` is missing |
| The table is visible but the query is denied | Step 15, `SELECT` is missing |
| The group member has no warehouse to run on | Step 21, no `CAN USE` on the warehouse |
| The group member cannot open the SQL editor at all | Step 10, the Databricks SQL access entitlement was not assigned explicitly |
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
  metastores. Account console navigation for steps 1 and 12.
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
  defaults, used at step 21.

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
  Steps 9 and 10.
- [Workspace-catalog binding](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/access-control/workspace-catalog-binding).
  Binding needs metastore admin, catalog owner or `MANAGE`, not account admin.
  Step 17.
- [Manage service principals](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-service-principals).
  Creation is documented, renaming an existing principal is not. Step 4.
- [Manage external locations](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/manage-external-locations).
  File events on by default, and the four role assignments. Step 8. Dated
  2026-08-11 and it contradicts the June ADLS page on the EventGrid role name.
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
  used at step 10.

> [!todo] 🔲 Steps 12, 15, 16, 20, 22 to 26 are not yet sourced
> Verify per claim before status leaves Draft.

<!--
Version: 0.9 | Last Updated: 2026-08-11 | Status: Draft
-->
