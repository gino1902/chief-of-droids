# Databricks platform foundation setup

> One ordered sequence from a provisioned workspace to check the readiness for work. 
> Decisions are not taken here. They arrive as accepted ADRs, and each step names the one it
> consumes.
>
>This runbook assumes one configuration and does not generalise beyond it: a
>Terraform-provisioned, VNet-injected, Premium workspace, automatically enabled
>for Unity Catalog, where workspace admin reaches a human through an Entra group
>and account admin is held elsewhere. The workspace already contains infrastructure. It contains no work.

## Preconditions

### Entry condition

The gate is per step, not up front. An ADR must be Accepted before the first
step that consumes it. See `First consumed` column below.

### ADRs

Ordered by the first step that consumes them. The `Depends on` column carries the
order they must be accepted in, which is not the same order.

| ADR | Subject | First consumed | Also consumed by | Depends on |
| :--- | :--- | :--- | :--- | :--- |
| ✅ | Group provenance | 4 | 8, 9, 13, 14 | none |
| 🔲 | Non-human identity model | 4 | 14 | Group provenance |
| 🔲 | Deployment model | 5 | Every step that changes state | none |
| 🔲 | Catalog and schema model | 5 | 7, 11, 12 | Workspace topology |
| 🔲 | Data protection model | 5 | 21 | Catalog and schema model |
| 🔲 | Serverless or classic posture | 6 | 17, 19 | none |
| 🔲 | Network posture | 6 | none | Serverless or classic posture |
| 🔲 | Access Connector and external location granularity | 7 | none | Catalog and schema model, Metastore root storage |
| 🔲 | Workspace topology | 8 | 9, 15 | none |
| 🔲 | Ownership and grant model | 8 | 13, 14 | Workspace topology, Catalog and schema model |
| 🔲 | Secret scope model | 10 | none | none |
| 🔲 | Metastore root storage and MANAGED LOCATION policy | 11 | none | Workspace topology |
| 🔲 | Tagging and budget route | 17 | 18 | Serverless or classic posture |
| 🔲 | Legacy surface posture | 20a | 20b | none |

> [!info] Three carry content that is settled
> - **Group provenance.** Accepted. Every group is inherited from Entra. No group
>   is created in Databricks, at account or workspace level. The workspace pulls
>   groups in and assigns them, and nothing else
> - **Metastore root storage and MANAGED LOCATION policy.** No metastore root.
>   Each catalog takes an explicit `MANAGED LOCATION` on the durable account from
>   step 5. Naming and layout are what remain open
> - **Data protection model.** It feeds step 5 as well as step 21, because Azure
>   retention and immutability are container-level settings and prod uses one
>   container per catalog. Deciding it late means changing container policy after
>   data has landed. One mechanism is already gone if step 6 takes route A: Azure
>   Backup is unsupported on an account associated with a network security
>   perimeter. Container immutability and lifecycle policies are unaffected, being
>   storage account features rather than a backup service

### Acceptance order

Derived from the `Depends on` column. Workspace topology first,
then metastore root storage and the catalog and schema model, then the data
protection model, then Access Connector granularity and the ownership and grant
model, then the rest. Serverless or classic posture and network posture form a
separate chain, in that order, and neither waits on anything above.

> [!warning] Three bind in the first two blocks, and two of them are not yours
> - Serverless or classic posture then network posture, both due before step 6.
>   Serverless cannot reach firewalled storage without them, and both are owned
>   outside this team. Start them first
> - The data protection model is due at step 5, not at step 21. Azure retention
>   and immutability are container-level settings and prod uses one container per
>   catalog, so settling it after step 5 means changing container policy on
>   containers that already hold data
> - Nothing on this list can safely lag. Every deadline in the table is the step
>   that consumes it earliest, including the two that used to read later

### Roles

#### Databricks account admin

Account admin here is a Databricks account console role. It is not an Azure role
and holding Owner or Contributor in Azure does not confer it.

Two steps and two parts of step 4 need it. Raise them as one request. Step
numbers are not a request, so this is what to actually ask for.

| Request | Unblocks |
| :--- | :--- |
| Serverless network access to the managed storage account, either a network security perimeter rule or a network connectivity configuration with private endpoint rules | 6 |
| Enable the system table schemas | 16 |
| A federation policy per CI service principal, once the repository and its protected branches exist | 4, second half only |
| Set the display name on the account-level service principal record, if it is empty | 4 |

The first carries the longest lead time and needs someone on the Azure side too,
so it is two people and not one.

#### Platform engineer

The contributor who terraforms the workspace. Everything Azure-side that this
sequence depends on and cannot reach, because neither owner role holds Azure
rights beyond Contributor on one resource group.

| Request | Unblocks |
| :--- | :--- |
| The durable storage account: hierarchical namespace and the four enforced tags at creation, containers per the environment shape, in its own Terraform state | 5 |
| The Azure side of the serverless path, route A or route B per the network posture ADR, and a record of which was taken | 6 |
| An access connector in a resource group you control, with its own storage credential, and Storage Blob Data Contributor on the containers | 7 |
| `Microsoft.Storage` registered on the subscription, if step 3 could not confirm it | 5 |
| Any deny-effect policy above the resource group scope, which step 3 cannot read from here | 3 |

The second row needs an Azure network owner as well, so it is the same two-person
request as the account admin's first row. Raise both together.

#### Entra admin

The contributor who owns the directory. Group provenance is Entra, so every group
this sequence uses either exists there already or waits on this request.

| Request | Unblocks |
| :--- | :--- |
| Every group the ownership and grant model names that the directory does not have | 8 |
| Source of authority conversion for any group where `onPremisesSyncEnabled` is true, so membership becomes cloud-managed | 8, and every membership change after it |
| Membership changes on inherited groups, permanently, since Databricks cannot edit them | 8, 13, 19, 23 |

The third row is not a one-off. It is the standing cost of the group provenance
ADR, and it lands on whoever holds this role for as long as the platform runs.

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

**Sources**

- [Admin privileges in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/admin-privileges),
  fetched 2026-08-11. The metastore privileges a workspace admin holds by default
  in an auto-enabled workspace. The page lists ten, of which the warning above
  names the four that matter here. It also states that workspace admins "can
  create objects but cannot make grants on or change ownership of existing
  objects they do not own". That is the one limit on the role.

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

- The Databricks CLI reads metastore state with no compute running, which is the
  only way to complete step 1 before a warehouse exists
- Creating a warehouse early lands untagged compute ahead of the policies at
  step 17
- Homebrew refuses the Databricks formula until the tap is trusted:
  `brew trust --formula databricks/tap/databricks`

### Provisioned baseline

State the workspace should already be in at step 1, produced upstream, not by
this sequence.

- Go on https://portal.azure.com/#home, then Resources groups. 
- Click on the RG holding the workspace resources (eg RG-DATABRICKS-DEV for instance)
- Click on the Databricks resource (DBR-DATABRICKS-DEV)
- Copy the Resource Group, Subscription id and Workspace URL (top), you will need for the tests.
- Launch Workspace
  
Capture the Workspace profile returned by the command.

```bash

URL = <url>
databricks auth login --host "$URL"

```

For the tests to follow:
- SUB=<subscription-id>
- RG=<workspace-resource-group>

> [!info] File events are on and this platform does not use them
> Provisioning enables file events on the workspace's own external location, with
> a managed AQS queue. Expect to see it. It is a reading, not a requirement.
> Nothing in this sequence writes files into storage, so nothing depends on it.

> [!warning] The baseline is not neutral
> - The workspace catalog arrives with open default grants
> - Every workspace user holds `USE CATALOG`, plus `USE SCHEMA`, `CREATE TABLE`,
>   `CREATE VOLUME`, `CREATE MODEL`, `CREATE FUNCTION` and
>   `CREATE MATERIALIZED VIEW` on its `default` schema
> - Live from the moment the workspace exists. Step 13 decides its fate. Do not
>   discover it at step 23

**Sources**

- [Admin privileges in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/admin-privileges),
  fetched 2026-08-11. The workspace catalog default grants, verbatim: every
  workspace user receives `USE CATALOG`, plus `USE SCHEMA`, `CREATE TABLE`,
  `CREATE VOLUME`, `CREATE MODEL`, `CREATE FUNCTION` and
  `CREATE MATERIALIZED VIEW` on its `default` schema. Workspace admins are its
  default owners.
- [Manage external locations](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/manage-external-locations),
  fetched 2026-08-12. File events are on by default.
- [Deploy a workspace using the Azure Portal](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace/create-workspace),
  fetched 2026-08-12. No templates or sample catalogs at creation, so anything
  else in the workspace is residue. Workspace type Hybrid means classic.

### Environment checks

Two things the baseline cannot tell you. Both cheap, both consequential.

**Someone holds Databricks account admin.**

- Two steps and two parts of step 4 need it. It does not flow from the Entra group
  that makes you a workspace admin, nor from any Azure role
- Test: open `accounts.azuredatabricks.net`. An account admin gets a console with
  a left nav, everyone else gets a workspace picker
- If nobody holds it, an Entra Global Administrator signs in once, which
  auto-creates their role, then delegates under User management, Roles. No other
  route

**Who else is on the metastore.**

- One metastore per region, and it is multi-tenant
- Expect catalogs owned by people outside your workspace, created years before it
- Their catalog and schema names are visible to you without any grant. Yours are
  visible to them unless step 15 binds them
- Read 2026-08-12: `metastore_azure_francecentral` dates from June 2024 and
  carries catalogs owned by a user outside this workspace, schemas dated October
  2024, one already called `bronzes`

> [!todo] 🔲 To be defined
> What steps 1 to 3 assume about the tenant and subscription beyond the above.

**Sources**

- [Databricks administration overview](https://learn.microsoft.com/en-us/azure/databricks/admin/admin-concepts),
  fetched 2026-08-11. Establishing the first account admin, and what a
  non-account-admin sees.

## How to read a step

Impact values: `Irreversible`, `Lossy`, `Rework Nd`, `Adjustable`.

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
- Network design beyond what step 6 requires. The hub and spoke topology
  itself is upstream
- SharePoint, the interim landing zone. It is ingested by a Lakeflow Connect
  managed connector straight into managed tables, so it needs none of steps 5
  to 7 and no landing zone of its own. Tracked separately
- Any file-based landing zone. Nothing writes files into storage here. Should a
  producer ever need to, that brings back an external location, file events and
  three more role assignments
- Default storage, meaning storage in Databricks' own account rather than yours.
  Closed, not open: "Creating catalogs on default storage is only available in
  serverless workspaces", and this workspace is VNet-injected, therefore classic.
  Classic compute cannot read default storage at all. It is not the way to avoid
  steps 5 to 7

> [!info] Three things are called storage, and only one of them takes a firewall
> - **Managed tables.** Unity Catalog picks the path and owns the file lifecycle,
>   but the files are yours and stay yours: "The data files always remain in your
>   cloud account. Unity Catalog determines where within your account they are
>   stored, but does not transfer them to Azure Databricks or own them"
> - **External location.** A governance object pairing a path with a storage
>   credential. It is required for managed storage too, not only for external
>   tables: "When you assign a managed storage location to a metastore, catalog,
>   or schema, you must reference an external location object". The word external
>   describes the object, never the table type
> - **Default storage.** Databricks' own account. Ruled out above
> - So the firewall at step 6 exists because managed data still sits in your
>   storage account, and serverless compute reaches across the network to read and
>   write those files. Unity Catalog hands out the path and the credential, it does
>   not carry the bytes

**Sources**

- [Managed versus external assets in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/managed-versus-external),
  fetched 2026-08-12. Managed means Unity Catalog owns the location and the
  lifecycle, not that Databricks holds the data. "The data files always remain in
  your cloud account."
- [Connect to cloud object storage using Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/),
  fetched 2026-08-12. An external location is a path plus a storage credential,
  and assigning a managed storage location "must reference an external location
  object".
- [Default storage in Databricks](https://learn.microsoft.com/en-us/azure/databricks/storage/default-storage),
  fetched 2026-08-12. Catalogs on it are "only available in serverless
  workspaces" and classic compute cannot interact with it, so it is unavailable
  to this VNet-injected workspace.

## Run order - to review

A step number is an identifier, not a position. Numbers stay fixed so every
`from step N` reference holds, and this section says what order to run them in.
What each step requires is in its own `Inputs` field, which names a producer for
every input. That is the constraint. This is the plan.

The driver is fail fast. A test that can condemn a workspace generation sits as
early as its inputs allow, and work that only rearranges permissions sits after
it.

| Block | Steps | Why here |
| :--- | :--- | :--- |
| 0, condemn or continue | The provisioned baseline, 1, the resource group scope of 3, 20a | Every read is free, and a failure is a question for the Terraform rather than something to fix by hand. 20a joins them because it requires nothing and step 12 cannot write before it is settled |
| 1, requests | The account admin's four asks, the platform engineer's five, the Entra admin's three | Other people's queues. Raised on day one and then left running. Step 6's carries two owners, and step 16 loses a day of history for every day it waits |
| 2, build | Storage: 5, 6's verification, 7, 11. Identity: 4, 8, 9. Compute: 17, then 19 | Storage and identity are independent until they meet at 11. Compute joins them so that step 12 runs on tagged compute |
| 3, checkpoint | 12 | Its write test proves the managed location and the serverless path from step 6 in one statement. Failure unwinds 11 alone, not the grants |
| 4, exposure and permissions | 15, 13, 14, 20b | 15 leads, because catalogs created at 11 are visible across the metastore until bound. 13 carries the workspace catalog decision, open since the workspace was created |
| 5, cost and protection | 18, 21, 22 | Nothing reads 18 except 22, and 21 needs 12 and 20a both settled |
| 6, acceptance | 10, only if its ADR names a consumer, then 23 | Step 10 is the one step with nothing downstream of it here |

Putting compute in block 2 costs three things, stated so they are chosen rather
than discovered.

- Two ADRs come due earlier. Serverless or classic posture and tagging and budget
  route are needed in block 2 rather than at step 17. With network posture already
  due before step 6, three ADRs bind inside the first two blocks and two of them
  are owned outside this team
- Tagged means tagged by hand. Compute policies do not govern SQL warehouses, so
  step 19 sets the warehouse tags at creation and nothing enforces them
- The provisioned starter warehouse is decided in block 2, not left to step 19. A
  tagged warehouse exists before step 12, so the untagged one has no remaining use

Two dependencies run backwards against the numbering and both land on step 12. It
needs the SQL semantics from 20a and compute from 19. Block 0 and block 2 resolve
them, which is the whole reason the blocks exist.

---

### 1. Read metastore root storage state

`Category: gate` · `Owner: workspace admin` · `Inputs: none` · `Prerequisite: Databricks CLI authenticated` · `Impact: Adjustable`

**When to use** When you do not want your catalogs falling back to a storage root
you do not own.

**Why it matters**

- Step 11 branches on whether the metastore carries a root storage location
- Automatic enablement creates no root, so absent is the expected reading
- With no root, every catalog must name a dedicated location of its own,
  registered in Unity Catalog as an external location
- With a root set, a catalog created without `MANAGED LOCATION` falls back to it,
  so your managed data lands in a storage account belonging to the shared
  metastore. That defeats the isolation step 5 exists to give you
- Clearing it is an account admin action on a metastore other workspaces are
  attached to, so it is a request to someone else and it changes their catalogs
  too

**What getting the execution wrong costs** The read changes nothing. Skipping it
turns step 11 from a decision into an accident.

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
  rather than clearing it, and it is an account admin action. The semantics are
  in the source below

**Sources**

- [Manage Unity Catalog metastores](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-metastore),
  fetched 2026-08-11, re-read 2026-08-12. Metastore-level storage is optional and
  absent from automatically created metastores, so absent is the expected
  reading. Account console navigation. The removal semantics: the path
  cannot be modified once set, only removed and re-added, by an account admin.
  Removal pushes the root down into catalogs that have no storage root of their
  own, as their catalog-level managed location, without interrupting access, and
  may create an external location named `prior_metastore_root_location`.


### 3. Read what Azure will refuse

`Category: gate` · `Owner: workspace admin for the resource group scope, platform engineer for anything above it` · `Inputs: workspace resource group and operator role assignments, both from the baseline` · `Prerequisite: none` · `Impact: Adjustable`

Network standards are settled upstream by the Terraform and are out of this step.

**When to use** When you want to verify step 5's storage is still present after Workspace regeneration, and step 17 to enforce the same tag names Azure already does.

**Why it matters**

- A deny policy blocks the request before it reaches the resource provider and
  returns `403 (Forbidden)`. Nothing warns you first, so a policy you did not read
  surfaces as a failed apply
- The enforced tag names bind step 17. A different vocabulary on the Databricks
  side gives two schemes and cost reporting that cannot be joined across them
- `Microsoft.Storage` must be registered on the subscription before step 5 creates
  anything
- `/register/action` comes with Contributor or Owner, at a scope the source does
  not name. If it is subscription scope then the operator cannot do it, holding
  Contributor on one resource group — ⚠️ Unverified

**What getting the execution wrong costs** Both reads are free. The cost is late
discovery: an apply denied at step 5, or a provider registration request raised
there that then waits on someone else.

**The play**

- Take the scope from the baseline workspace identity row
- Policy assignments need `--disable-scope-strict-match` or inherited ones stay
  invisible. Query `name` rather than `displayName`, which is often empty, and
  output JSON, because resource IDs truncate in tables
- Resolve each `policyDefinitionId` to its effect. An audit policy and a deny
  policy are indistinguishable in the assignment list
- Read `enforcementMode` alongside the effect. A `deny` assignment set to
  `DoNotEnforce` marks resources non-compliant and blocks nothing
- Read each assignment's `tagName` parameter rather than trusting its name. The
  name is a label chosen by whoever assigned it and need not match the key the
  policy enforces, and step 17 has to match the key

```bash
SUB=<subscription-id>
RG=<workspace-resource-group>

SCOPE="/subscriptions/$SUB/resourceGroups/$RG"

az account set --subscription "$SUB"

echo "== assignments =="
az policy assignment list --scope "$SCOPE" --disable-scope-strict-match \
  --query "[].{name:name, policy:policyDefinitionId, enforcement:enforcementMode, params:parameters}" -o json

echo "== definitions =="
az policy assignment list --scope "$SCOPE" --disable-scope-strict-match \
  --query "[].policyDefinitionId" -o tsv | sort -u | sed 's|.*/||' | while read -r d; do
    echo "-- $d"
    az policy definition show --name "$d" \
      --query "{name:displayName, effect:policyRule.then.effect, mode:mode}" -o json
  done

echo "== providers =="
az provider show -n Microsoft.EventGrid --query registrationState -o tsv
az provider show -n Microsoft.Storage  --query registrationState -o tsv
```

**Check**

- You can name every deny-effect policy applying to what steps 5, 6 and 7 create,
  and name the scopes you could not read. Unreadable is an acceptable answer,
  unknown is not
- Every deny assignment's `enforcementMode` is known. Under `DoNotEnforce` a
  step 5 apply that succeeds proves nothing about the tags, so the tag names
  still bind step 17 while nothing at this scope stops an untagged create
- The tag keys are taken from the `tagName` parameters, character for character,
  and step 17 uses those
- Both providers read `Registered`, or a request is open with someone who can
  register them

**Sources**

- [Azure Policy deny effect](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-deny),
  fetched 2026-08-12. Deny prevents the request before it reaches the resource
  provider and returns `403 (Forbidden)`. Existing resources matching a deny
  definition are marked non-compliant rather than removed.
- [Azure resource providers and types](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-providers-and-types),
  fetched 2026-08-12. A subscription must be registered for a provider before its
  resources can be created, and `/register/action` is included in Contributor and
  Owner. The page does not state the scope that permission is needed at, which is
  why this step carries a flag. It also states that ARM template and Bicep
  deployments auto-register the providers they declare, which says nothing about
  Terraform.

### 4. Create the CI/CD service principals

`Category: foundation` · `Owner: workspace admin, except the federation policy which is Databricks account admin` · `Inputs: existing service principals and their Entra records, read in the play; GitLab project and protected branches, from the baseline IaC repo row` · `Prerequisite: 🔲 ADR non-human identity model` · `Impact: Lossy`

Detail on the principal kinds, the authentication routes and the federation build
is in [[2026-08-10-databricks-cicd-service-principal]].

**Why it matters**

- Automation must not run under a person's token. A principal is scoped
  independently, can be disabled on its own, and survives the person leaving
- The kind is fixed at creation. No `applicationId` gives a Databricks managed
  principal, an existing Entra application ID gives an Entra managed one
- The federation policy's subject claim is the entire security boundary. An
  unpinned subject lets any branch in the project deploy to production

**What getting the execution wrong costs** Deleting a principal stops its
compute, fails its jobs and breaks anything shared with Run as Owner. Deactivate
instead.

**The identity model**

| Identity | Kind | Rationale |
| :--- | :--- | :--- |
| Infra Terraform | Entra sourced, carries an `externalId` | Authenticates to Azure and Databricks in the same run |
| CI/CD bundle deploy | Databricks managed, one per environment, OIDC federation | No secret to rotate, and one environment can be revoked alone |
| Claude Code | None. It runs as the human, over user-to-machine OAuth | Attribution stays on a person and it cannot exceed your rights. The cost is that it cannot act when you are not there |

**The play**

- Read what exists first. A deployment principal usually predates this step
- Read names through the API, not the UI. The UI resolves a name from the
  identity provider even when the SCIM attribute is empty, and it is the empty
  attribute that `created_by` and every automated query report
- Create one Databricks managed principal per environment, `displayName` set at
  creation
- Keep them out of `admins` and out of every group. Group provenance is Entra and
  a Databricks managed principal cannot join an Entra group, so their access is a
  direct grant at step 14
- The federation policy comes last. It is account-level, and its subject cannot
  be written before the repository and its protected branches exist
- Decode a real CI token and read its `iss` and `sub` before writing the policy

```bash
P=<profile>

databricks -p "$P" service-principals list -o json

databricks -p "$P" service-principals create \
  --json '{"displayName":"SP-CICD-<region>-<org>-<env>","active":true}'

databricks -p "$P" service-principals get <scim-id>
```

**Check** Read back rather than trusting a clean exit. The create response only
echoes what you sent, and it carries neither `groups` nor `entitlements`.

- `displayName` is what you set. If it is missing, wait and read again. A SCIM
  write can succeed and read back empty for a while
- `groups` is empty, read again after ten minutes. An automation rule can add
  `admins` on a delay
- A pipeline run on a non-protected branch fails to authenticate against the
  production policy

> [!info] Do not demote the Terraform principal
> Its `admins` membership is where its `CREATE CATALOG` and
> `CREATE EXTERNAL LOCATION` come from. Explicit grants are the narrower
> alternative, parked at step 13. Demoting before those grants exist fails the
> next deploy.

**Sources**

- [Service principals](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/service-principals),
  fetched 2026-08-12. Databricks managed is the recommendation for Databricks
  automation, Entra ID managed only where a process "must authenticate with Azure
  Databricks and other Azure resources at the same time". That test is the identity
  model table above. The creator becomes service principal manager, which does not
  confer the service principal user role needed to run jobs as it.
- [Manage service principals](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-service-principals),
  fetched 2026-08-12. Creation is documented, renaming an existing principal is
  not. Deactivation is named as preferable to removal, which is "a destructive
  action": deletion stops compute, fails jobs and breaks Run as Owner sharing. A
  workspace admin cannot delete an account-level principal.
- [Automatic identity management](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/automatic-identity-management/),
  fetched 2026-08-12. Why a Databricks managed principal cannot join an Entra
  group, so these identities are granted directly at step 14. Carried from
  [[2026-08-10-databricks-cicd-service-principal]], verified there.

### 5. Create the durable storage account for managed data

`Category: foundation` · `Owner: platform engineer` · `Inputs: enforced tag names, from step 3` · `Prerequisite: 🔲 ADR catalog and schema model, 🔲 ADR deployment model` · `Impact: Rework 3d`

Not a landing zone. Nothing writes files here directly. This is where the managed
tables of every catalog physically live.

**When to use** When you want your managed tables to still exist, in a resource
group you control, after Terraform destroys and rebuilds the workspace.

**Why it matters**

- Data outlives the workspace. Terraform rebuilds the shell, and the catalogs and
  their files must not be rebuilt with it
- The workspace's own Unity Catalog container is the obvious shortcut and the
  wrong answer. It is created by the workspace and orphaned when the workspace
  goes, leaving your data in a converted resource group nobody manages
- A hierarchical namespace is required. It can be added afterwards, but only by a
  one-way upgrade that disables writes while it runs and will not start while
  immutable storage or soft delete is enabled, so set it at creation
- The enforced tags must be set at creation. A deny policy refuses the apply
  rather than warning

**What getting the execution wrong costs** An account without a hierarchical
namespace is replaced, not amended. Data already written moves by hand.

**The play**

- Its own Terraform state, not merely a separate resource. If `terraform destroy`
  on the workspace can reach this account, the separation is decorative and the
  first regeneration takes the data
- `is_hns_enabled = true` and the four enforced tags, both at creation
- Keep the account name to 44 characters or fewer if step 6 takes route A. A
  perimeter association is named `{resourceName}-{perimeter-guid}` and has to fit
  Azure's 80-character field. No such limit under route B
- Containers by environment:

| | Dev | Prod |
| :--- | :--- | :--- |
| Containers | One, a path per catalog | One per catalog |
| Path | `abfss://managed@<acct>/<catalog>` | `abfss://<catalog>@<acct>/` |
| External locations, step 7 | One | One per container |
| Role assignment | Account scope | Container scope |
| Azure retention and immutability | Not set | Per container, per the data protection ADR |

- Container-scoped grants in prod are the point of per-catalog containers. One
  account-scoped grant makes the split decorative
- Drive the shape from a variable in one module rather than two configurations,
  or a prod apply exercises a path dev has never run
- Leave public network access alone. Step 6 sets the end state and it differs by
  route. Closing it here locks out the connections you are about to create, and
  the failures read as permission errors rather than network ones
- 🔲 Resource blocks and the apply

**Check** 🔲

**Sources**

- [Delete a workspace](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace/delete-workspace),
  fetched 2026-08-12. Databricks "converts the managed resource group into a
  regular resource group", retaining the Unity Catalog container and the access
  connector in it. That is this step's second bullet. Deleting the resource group
  through the portal does not force delete it.
- [Upgrade Azure Blob Storage with Azure Data Lake Storage capabilities](https://learn.microsoft.com/en-us/azure/storage/blobs/upgrade-to-data-lake-storage-gen2-how-to),
  fetched 2026-08-12. A hierarchical namespace can be enabled after creation, but
  "an upgrade is one-way", writes are disabled while it runs, and it will not pass
  validation while immutable storage, soft delete, blob snapshots or encryption
  scopes are enabled, or while page blobs are present.
- [What is a network security perimeter?](https://learn.microsoft.com/en-us/azure/private-link/network-security-perimeter-concepts),
  fetched 2026-08-12. Resource names are limited to 44 characters for a perimeter
  association to fit, which binds the naming here under route A.

### 6. Confirm the serverless path to the managed storage account

`Category: gate` · `Owner: workspace admin to verify, Databricks account admin with an Azure network owner to build` · `Inputs: storage account resource ID, from step 5; workspace region, from step 1; the route taken, from the network posture ADR` · `Prerequisite: 🔲 ADR network posture` · `Impact: Rework 4d`

The path is not built here. Route A is built in the Azure portal and route B in
the Databricks account console, and both are owned outside this sequence. Neither
is purely Azure work: route A's own requirements list a Databricks account admin
alongside Contributor or Owner on the resource and rights to create perimeter
resources. What belongs here is the request, the record of which route was taken,
and the proof that it works.

**When to use** When the posture ADR picked serverless and the step 5 account is
firewalled, since nothing you write from your own VNet can admit serverless.

**Why it matters**

- Serverless has no presence in your VNet, so subnet rules, service endpoints and
  your own private endpoints cannot reach it. It is admitted only by source
  identity, the service tag in route A, or by an endpoint Databricks creates and
  you approve, route B. That is why this step needs a Databricks account admin and
  not only your network team
- Every managed table read and write crosses that boundary. A firewalled account
  refuses it, and the failure reads as a permissions error
- Two routes, not three. Accounts allowlisting serverless subnet IDs had to move
  to a perimeter by 9 June 2026, so any guidance still offering that is stale.
  The two that remain have opposite end states and the network posture ADR picks
  one
- Classic and pro compute is the opposite case. It runs on VMs inside your VNet
  and reaches the account by ordinary means, so it is not what this step covers.
  Either route still breaks it unless it gets its own path
- Nobody else will prove it. The two routes are configured by two different people
  in two different consoles, and neither of them can run a query as this workspace

**What getting the execution wrong costs** Both routes need someone on the Azure
side, so a mistake costs another round with another person rather than a retry. A
false pass here is worse: the next thing to touch this path is step 12's write
test, with grants and bindings already built on it.

**The play**

- Raise the request. It is the first row of what to ask the Databricks account
  admin for, and it carries the longest lead time in the sequence
- Record which route was taken. The two have incompatible end states and a later
  reader cannot tell them apart from the storage account alone
- Verify from serverless, below. That is the only part of this step you own

| | Route A, network security perimeter | Route B, private endpoints via NCC |
| :--- | :--- | :--- |
| Use when | Storage sits in the workspace region | Dedicated private connectivity is required |
| Built where | Azure portal, by someone who is also a Databricks account admin | Databricks account console, then an Azure-side approval |
| Mechanism | Perimeter left in transition mode, inbound rule for the regional `AzureDatabricksServerless` service tag | One private endpoint rule per subresource, `dfs` for Unity Catalog and `blob` for model serving |
| Waits on | Nothing after the rule is added | Each rule sits `PENDING` until someone with rights on the account approves it |
| End state | Public network access stays **Enabled from selected networks** | Public network access may be set to **Disabled**, which the source presents as optional hardening |
| Classic compute | Allow its IPs on the resource | Give it its own private endpoint from your VNet |

Secured by Perimeter is the trap in route A. It stops serverless reading external
locations and returns `PERMISSION_DENIED`, typically
`Request for user delegation key is not authorized`. Applying route A's rules and
then route B's end state is the mistake that looks like a permissions bug. Azure
recommends Secured by Perimeter for resources in a perimeter and Databricks
explicitly tells you not to set it, so the portal will nudge you towards the
break.

The build itself is change 5 in [[2026-08-11-databricks-terraform-changes]], with
the Terraform resource names for route B and the portal steps for route A. The
table above is the summary you need to raise the request and record the answer,
not a second copy of the procedure.

**Check** Both compute planes, separately, because they take different paths.

- From serverless: `LIST 'abfss://<container>@<account>.dfs.core.windows.net/'`
  returns without error
- From a classic cluster: the same statement succeeds
- Route B only: every private endpoint rule reads `ESTABLISHED`, never `PENDING`

The `LIST` cannot run before step 7. Serverless reaches storage through a Unity
Catalog external location rather than through credentials in Spark properties, so
an external location must already cover the path and the caller needs
`READ FILES` on it. Step 7 declares this step as an input, so register the
external location first and verify afterwards. The two steps interleave rather
than queue.

Diagnostics live on the perimeter, not on the storage account. Configure
diagnostic settings on the network security perimeter to see which rule allowed or
denied a request. The storage account's own `StorageRead` and `StorageWrite`
categories record data access and never record perimeter rule evaluation, so a
denied request leaves no trace where you would look for it first.

> [!warning] A general egress test proves nothing here
> Reaching public endpoints from a serverless notebook, such as
> `login.microsoftonline.com`, exercises Databricks' internet egress. This step
> is about a firewalled account inside your subscription, which is a different
> path under different controls. Only the `LIST` above tests it.

> [!info] Either route
> - **Allow trusted Microsoft services** on the storage account. Re-read
>   2026-08-13: the route A page does not mention it, and describes transition mode
>   as evaluating perimeter rules first and falling back to the resource firewall,
>   which says nothing about trusted services either way. ⚠️ Unverified in both
>   directions now, where it previously read as a requirement. Do not treat it as
>   one until a source says so
> - Route B limits: 10 NCCs per region, 100 private endpoints per region, 50
>   workspaces per NCC. Databricks bills networking costs for serverless
>   connections
> - Route A is available here. Network security perimeter is generally available
>   in all Azure public cloud regions, Storage is an onboarded resource type, and
>   ADLS Gen2 is covered for HTTPS operations. Read 2026-08-12, closing an earlier
>   open question about France Central
> - Route A covers serverless SQL warehouses, jobs, notebooks, Lakeflow pipelines
>   and model serving endpoints. The service tag is supported only for perimeter
>   inbound rules targeting Azure Storage in the workspace's own region, so it does
>   nothing for any other resource type
> - Prefer the regional tag, `AzureDatabricksServerless.<region>`, over the global
>   one. Some regions keep secondary artifact storage in a different region, and
>   those need a second tag

> [!warning] The two publishers disagree about transition mode
> - Databricks: "Azure Databricks recommends remaining in transition mode
>   indefinitely for most use cases"
> - Azure Storage: transition mode "should serve only as a transitional step",
>   and "it's crucial to transition to a fully secure configuration as soon as
>   possible with the access mode set to Enforced"
> - The network posture ADR has to settle it, and a security review citing the
>   Azure page will challenge the Databricks answer
> - Enforced mode is not a free upgrade. It stops honouring trusted services, and
>   service endpoint traffic "can be denied even when an inbound rule allows
>   0.0.0.0/0", which is how classic compute in a VNet-injected workspace usually
>   reaches storage. Both are why Databricks says stay in transition
> - Azure Backup is not supported on an account associated with a perimeter,
>   which lands on the data protection ADR at step 21

**Sources**

- [Serverless compute plane networking](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/),
  fetched 2026-08-11. What an NCC is, and the end of serverless subnet
  allowlisting on 9 June 2026, leaving two routes and not three.
- [Configure private connectivity to Azure resources](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-private-link),
  fetched 2026-08-11, re-read 2026-08-12. Route B: NCC creation, private endpoint
  rules, the Azure-side approval, and the limits. "If you configure your Azure
  resource to only accept connections from private endpoints, any connection to
  the resource from your classic Databricks compute resources also must use
  private endpoints." Route B needs the Premium plan and an account admin, and
  setting public network access to Disabled is presented as optional hardening
  rather than a required end state.
- [Configure an Azure network security perimeter](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-firewall-config),
  fetched 2026-08-12, re-read 2026-08-13, page dated 2026-08-07. Route A, and why
  Secured by Perimeter breaks serverless: it returns `PERMISSION_DENIED`, "such as
  `Request for user delegation key is not authorized`", and the page says to keep
  the resource on Enabled from selected networks "even though Azure recommends
  Secured by Perimeter for resources in a perimeter". Route A requires an Azure
  Databricks account administrator, Contributor or Owner on the resource, and
  rights to create perimeter resources. Perimeter coverage is serverless SQL
  warehouses, jobs, notebooks, Lakeflow pipelines and model serving endpoints. The
  service tag is "supported only for NSP inbound rules targeting Azure Storage
  (including ADLS Gen2) in the workspace's region". The verification `LIST` needs
  an external location covering the path and `READ FILES` on it. Diagnostic
  settings belong on the perimeter, since resource logs "do not record NSP rule
  evaluation". The regional tag is preferred over the global one, and transition
  mode is recommended indefinitely rather than as a staging step. The page does not
  mention Allow trusted Microsoft services at all. "Configuring a firewall also
  affects connectivity from classic compute resources. You must also update your
  resource access rules to allow the IPs for connections from classic compute
  resources."
- [What is a network security perimeter?](https://learn.microsoft.com/en-us/azure/private-link/network-security-perimeter-concepts),
  fetched 2026-08-12. Generally available in all Azure public cloud regions, so
  route A is open in France Central. Storage is an onboarded resource type.
  Service endpoint traffic "is not supported" and "can be denied even when an
  inbound rule allows 0.0.0.0/0".
- [Network Security Perimeter for Azure Storage](https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security-perimeter),
  fetched 2026-08-12. Perimeter rules override the account's own firewall. ADLS
  Gen2 is covered for HTTPS operations. Enforced mode does not honour trusted
  services. Azure Backup, object replication and static websites are unsupported
  on an associated account. This page's advice to move to enforced mode is the
  Azure half of the disagreement above.
- [Set up serverless SQL warehouses](https://learn.microsoft.com/en-us/azure/databricks/admin/sql/serverless),
  fetched 2026-08-12. Storage firewalls must admit the serverless compute nodes.

### 7. Register the external locations over it

`Category: foundation` · `Owner: workspace admin` · `Inputs: the containers, from step 5; a working network path, from step 6; the workspace's own access connector and storage credential, from the baseline, or a durable pair from the platform engineer, which no step here produces` · `Prerequisite: 🔲 ADR catalog and schema model, 🔲 ADR Access Connector granularity, 🔲 ADR deployment model` · `Impact: Rework 3d`

**Why it matters**

- A `MANAGED LOCATION` must sit inside an external location. That is the only
  reason these exist. No producer writes files into them, though the query engine
  writes every managed table file there
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
>   principal ID is not readable by the operator. It survives the workspace rather
>   than dying with it, in a resource group Databricks converts to an ordinary one,
>   unless the workspace is force deleted. Unmanaged and unreadable, not absent
> - A connector in a resource group you control is the durable choice, and needs
>   its own storage credential. No step here creates it. It is a request to the
>   platform engineer, raised with the rest of the storage chain
> - The granularity ADR decides. Either way the role assignment is one, not four

**Sources**

- [Manage external locations](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/manage-external-locations),
  fetched 2026-08-12. File events are on by default, and the four role assignments
  they need. Only Storage Blob Data Contributor survives now that no files land in
  storage. The page is dated 2026-08-11 and contradicts the June ADLS page on the
  EventGrid role name.
- [Connect to cloud object storage using Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/),
  fetched 2026-08-12. An external location is a path plus a storage credential,
  and a managed storage location "must reference an external location object".
  Nothing else puts these here.
- [Delete a workspace](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace/delete-workspace),
  fetched 2026-08-13. "The DBFS storage account and access connector in the
  managed resource group are retained unless you force delete them", and
  Databricks "converts the managed resource group into a regular resource group".
  So the workspace's own connector outlives the workspace unless force deletion is
  chosen explicitly, by the portal checkbox, `-ForceDeletion`, `--force-deletion`
  or `--force-deletion-types`.

### 8. Pull the Entra groups into the account

`Category: foundation` · `Owner: workspace admin to pull in, Entra admin to create anything missing` · `Inputs: the group names the grant model needs, from the ownership and grant ADR; their sync mode, read in the play below` · `Prerequisite: ✅ ADR group provenance, 🔲 ADR workspace topology, 🔲 ADR ownership and grant model` · `Impact: Adjustable`

**Why it matters**

- The group provenance ADR forbids creating a group in Databricks, so a group
  that does not exist in Entra blocks this step until an Entra admin makes it.
  That is a directory ticket with directory lead time, not workspace work
- The house convention is one group per resource group, which models deployment
  rights rather than data access. The grant model needs a data-shaped set as
  well, and those are the groups most likely to be missing
- Sync mode decides who can change membership later. Cloud-only groups are
  self-service in Entra. A group synced from on-premises is read-only in the
  cloud, so every membership change is a ticket to whoever owns that directory
- That last one is not permanent. Source of authority can be converted per group,
  which makes it cloud-managed and editable. It needs a Hybrid Administrator and
  a current sync client, so it is still someone else's action, but it is one
  request rather than one per membership change

**What getting the execution wrong costs**

- A group created in Databricks by mistake is a second source of truth. Its
  membership drifts from Entra and nothing reconciles the two
- Membership is not editable from the Databricks side for an inherited group, so
  a wrong member is fixed in Entra and waits for the sync

**The play**

- Filter directory reads. An unfiltered group list returns the whole tenant,
  including groups belonging to unrelated engagements
- Read `onPremisesSyncEnabled` on every group the grant model names

```bash
az ad group show --group <group-name> \
  --query "{name:displayName, id:id, onPremSync:onPremisesSyncEnabled}"
az ad group member list --group <group-name> \
  --query "[].{name:displayName, upn:userPrincipalName}" -o table
```

- Anything the grant model names and the directory does not have goes to the
  Entra admin now, as one request, before the workspace work starts
- Pull each existing group in from Settings, Identity and access, Manage next to
  Groups. The picker searches Entra. Use it to add, never to create
- Confirm from the CLI that what arrived is what you expected

```bash
databricks -p "$P" account groups list \
  --filter 'displayName sw "<prefix>"' -o json | grep '"displayName"'
```

**Check**

- Pass means every group the grant model names is present in the account and
  none of them originated in Databricks
- A group whose members you can edit inside Databricks was created there. That
  is a fail, not a convenience

> [!warning] Automatic identity management makes membership read-only
> - It is on by default for accounts created after 1 August 2025, which includes
>   this one, and it makes Entra the source of truth for membership
> - Membership of a synced group cannot be updated from Databricks
> - The consequence lands on step 4. A Databricks managed service principal
>   cannot join an Entra group, so the CI identities are granted directly at
>   step 14 rather than through a group, or they are made Entra managed instead
> - That choice belongs to the non-human identity ADR, which now depends on this
>   one

Inventory result for this deployment, read 2026-08-11:

| Finding | Value |
| :--- | :--- |
| Group behind workspace admin | `SGA-RG-DATABRICKS-DEV` |
| Sync mode | Cloud-only, `onPremisesSyncEnabled` unset |
| Grants | Contributor on `RG-DATABRICKS-DEV` |
| Members | Two |
| Convention | One group per resource group |

**Sources**

- [Manage groups](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-groups),
  fetched 2026-08-12. Workspace admins can create account groups and assign them
  to a workspace. The group provenance ADR uses only the second half, so this
  step pulls in rather than creates.
- [Automatic identity management](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/automatic-identity-management/),
  fetched 2026-08-12. On by default for accounts created after 1 August 2025.
  Entra is the source of truth and membership of a synced group cannot be updated
  in Databricks. Carried from
  [[2026-08-10-databricks-cicd-service-principal]], verified there.
- [Configure Group Source of Authority (SOA) in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/hybrid/how-to-group-source-of-authority-configure),
  fetched 2026-08-12. A synced group is read-only in the cloud, "any write
  attempts to the group in the cloud fail", and its fields are greyed out in the
  admin centre. Source of authority converts per group with a Graph PATCH setting
  `isCloudManaged`, needing Hybrid Administrator, the
  `Group-OnPremisesSyncBehavior.ReadWrite.All` scope, an Entra Free licence and a
  current sync client. Nested groups convert one at a time, lowest first. After
  conversion `onPremisesSyncEnabled` reads null, the same as a cloud-native group.

### 9. Assign entitlements to each group

`Category: admin` · `Owner: workspace admin` · `Inputs: the groups, from step 8` · `Prerequisite: 🔲 ADR workspace topology` · `Impact: Adjustable`

**Why it matters**

- Two principal namespaces. Unity Catalog grants accept account-level principals,
  workspace permissions do not, so a group pulled in at step 8 stays unusable for
  anything workspace-scoped until it is assigned here
- Step 10's warning is the evidence: `account users` was accepted on a catalog
  grant and refused on a scope ACL, where the workspace-level `users` group
  worked
- The two that fail without it are the scope ACLs at step 10 and the warehouse
  permissions at step 19

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

**Sources**

- [Workspace entitlements](https://learn.microsoft.com/en-us/azure/databricks/security/auth/entitlements),
  verified 2026-08-10 in [[dbr-RG-to-working-non-admin-user]]. The 15 June 2026
  system group change and its enforcement dates.
- [Manage groups](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-groups),
  fetched 2026-08-12. Assigning an account group to a workspace.

### 10. Create secret scopes and scope ACLs

`Category: foundation` · `Owner: workspace admin` · `Inputs: the principals that receive scope ACLs, from step 8, usable here only once assigned to the workspace at step 9` · `Prerequisite: 🔲 ADR secret scope model` · `Impact: Rework 2d`

**When to use** When something here holds a credential that federation and managed
identity cannot carry for it.

**Why it matters**

- Nothing in this sequence has produced such a credential. The CI principals
  federate and hold no secret, Unity Catalog reaches storage through the access
  connector identity rather than the caller's, and SharePoint arrives through a
  managed connector. The secret scope model ADR has to name a consumer or this
  step has no subject
- Scope ACLs resolve workspace principals, not account ones, so a group pulled in
  at step 8 is unusable here until step 9 assigns it

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] Observed
> `account users` is accepted on a catalog grant and rejected on a scope ACL,
> where the workspace-level `users` group works. Tested against a live scope.

**Sources**

- [Access control lists](https://learn.microsoft.com/en-us/azure/databricks/security/auth/access-control/),
  fetched 2026-08-12. The secret scope ACL levels.

### 11. Create catalogs with explicit MANAGED LOCATION

`Category: foundation` · `Owner: workspace admin` · `Inputs: metastore root storage state, from step 1; the external location that will hold managed data, from step 7` · `Prerequisite: 🔲 ADR metastore root storage, 🔲 ADR catalog and schema model` · `Impact: Lossy`

**Why it matters**

- The catalog is the unit of data isolation and of workspace binding
- `MANAGED LOCATION` is set here, and changing it later leaves existing tables
  behind in the old location
- Setting it needs `CREATE MANAGED STORAGE` on the external location, which is a
  different privilege from `CREATE CATALOG`. Whoever creates the external location
  at step 7 owns it and holds this. If that is the Terraform principal rather than
  a person, the person running this step has to be granted it first

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] What you create is open, what Databricks provisions is not
> - A catalog created here arrives `OPEN` and owned by the person who ran the
>   command. Observed, as a workspace admin through the CLI
> - The workspace catalog provisioning created is `ISOLATED` and owned by a group
> - Step 15 closes the first, step 13 owns the second

> [!warning] Why `Lossy` and not `Irreversible`
> - `ALTER CATALOG SET MANAGED LOCATION` exists on Databricks SQL and Runtime
>   18.1 and above, so the setting is changeable
> - It does not move managed tables and volumes that already exist
> - The setting is adjustable, the data already written is not. Academic on an
>   empty catalog, not academic one table in

**Sources**

- [Manage Unity Catalog metastores](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-metastore),
  fetched 2026-08-11, re-read 2026-08-12. With no metastore root, every catalog
  must name a dedicated location registered as an external location. That is the
  branch this step takes.
- [Specify a managed storage location in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/managed-storage),
  fetched 2026-08-11. Managed storage precedence, and
  `ALTER CATALOG SET MANAGED LOCATION` on Databricks Runtime 18.1 and above, which
  affects only objects created after the change. That is the whole of why this step
  is `Lossy` rather than `Irreversible`.

### 12. Create schemas

`Category: foundation` · `Owner: workspace admin` · `Inputs: the catalogs, from step 11` · `Prerequisite: 🔲 ADR catalog and schema model` · `Impact: Adjustable`

**Why it matters**

- The schema is the smallest thing you can grant on without granting the whole
  catalog. `USE SCHEMA` is separate from `USE CATALOG`, so where the schema
  boundaries fall decides what step 13 is able to hand out
- A schema can carry its own `MANAGED LOCATION`, which overrides the catalog's.
  Set deliberately that isolates one schema's files. Set by accident it silently
  redirects them, and step 11's warning about tables left behind applies again one
  level down
- Creating one needs `USE CATALOG` and `CREATE SCHEMA` on the parent catalog, and
  `CREATE MANAGED STORAGE` on the external location if it names a location of its
  own

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** The schema existing proves nothing. Write to it.

- Create a table, insert a row, read it back, drop the table
- Pass means the managed location is genuinely writable, not merely registered

This is the one checkpoint in the sequence and it earns its place here. Steps 13
to 23 all assume the storage path works. Finding out at step 23 that it does not
means unwinding eleven steps of grants, bindings and compute that were built on a
path Unity Catalog could never write to.

```bash
databricks -p "$P" api post /api/2.0/sql/statements --json @<file>
```

with a statement of `CREATE TABLE <catalog>.<schema>.probe (id INT)`, then an
`INSERT`, then a `SELECT`, then `DROP TABLE`. A warehouse has to exist to run it,
so either use one that is already there or bring step 19 forward for this check
alone.

**Sources**

- [Create schemas](https://learn.microsoft.com/en-us/azure/databricks/schemas/create-schema),
  fetched 2026-08-12. Creating a schema needs `USE CATALOG` and `CREATE SCHEMA` on
  the parent catalog, plus `CREATE MANAGED STORAGE` on the external location if it
  names its own managed location. "Every Unity Catalog catalog automatically
  includes a system-provided read-only `INFORMATION_SCHEMA`", and the page names no
  other automatic schema.
- [Specify a managed storage location in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/managed-storage),
  fetched 2026-08-11. A schema-level managed location overrides the catalog's, the
  precedence this step warns about.
- [What are catalogs in Azure Databricks?](https://learn.microsoft.com/en-us/azure/databricks/catalogs/),
  fetched 2026-08-12. The three-level namespace, and the distinction between the
  workspace catalog and the workspace's default catalog setting. Neither is a
  per-catalog `default` schema, so this step does not claim one exists.

### 13. Apply catalog-level grants

`Category: foundation` · `Owner: catalog owner, a workspace admin for anything created here` · `Inputs: the catalogs and schemas, from steps 11 and 12; the groups, from step 8` · `Prerequisite: 🔲 ADR ownership and grant model` · `Impact: Adjustable`

**Why it matters**

- Nothing this sequence creates is readable by default. Grants are the entire
  access model
- Reading one table needs `USE CATALOG`, `USE SCHEMA` and `SELECT`. None
  substitutes for another
- Grants inherit downward. `SELECT` on a catalog reads every table in it, and the
  catalog owner holds every privilege on everything inside it. What you grant here
  is blunt by construction

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

**Sources**

- [What are catalogs in Azure Databricks?](https://learn.microsoft.com/en-us/azure/databricks/catalogs/),
  fetched 2026-08-12. Grants inherit downward: "Users with `SELECT` on a catalog
  can read any table in the catalog", and a user "cannot access that table unless
  they also have the `USE CATALOG` privilege on the catalog that contains the
  table".
- [Admin privileges in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/admin-privileges),
  fetched 2026-08-11. The workspace catalog's default grants, the surface this step
  has to close, keep or delete.

### 14. Grant the service principals their catalog access

`Category: foundation` · `Owner: catalog owner, a workspace admin for anything created here` · `Inputs: the CI principals, from step 4; the catalogs and schemas, from steps 11 and 12` · `Prerequisite: 🔲 ADR ownership and grant model, 🔲 ADR non-human identity model` · `Impact: Adjustable`

**Why it matters**

- A Databricks managed service principal cannot join an Entra group, and the group
  provenance ADR permits no other kind. So these grants are direct, one per
  principal per object, and none of it scales the way step 13's group grants do.
  Making the principals Entra managed instead is the only thing that changes that,
  and that belongs to the non-human identity ADR
- What they need is catalog privilege, not storage access. Unity Catalog reaches
  the files through its own credential rather than the caller's, and Databricks is
  explicit that "Direct storage access is not supported for Unity Catalog managed
  tables"

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

**Sources**

- [Connect to cloud object storage using Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/),
  fetched 2026-08-12. Granting identities direct storage access to managed tables
  bypasses Unity Catalog, and "Direct storage access is not supported for Unity
  Catalog managed tables". So these principals get catalog privilege rather than a
  role assignment.
- [Automatic identity management](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/automatic-identity-management/),
  fetched 2026-08-12. Why a Databricks managed principal cannot join an Entra
  group, so these grants are direct and do not scale the way step 13's do.

### 15. Apply catalog to workspace bindings

`Category: foundation` · `Owner: catalog owner, which is a workspace admin for anything created here` · `Inputs: the catalogs, from step 11; the list of workspaces on this metastore, from the baseline` · `Prerequisite: 🔲 ADR workspace topology` · `Impact: Adjustable`

**When to use** When you do not want the other tenants on this metastore reaching
your catalogs, or reading their names.

**Why it matters**

- The metastore is multi-tenant and a catalog is reachable from all of it unless
  bound. "Catalogs are shared with all workspaces attached to the current
  metastore unless you specify a binding"
- Binding is the only thing that stops your catalog names appearing in another
  team's Catalog Explorer. Names leak without any grant, which the environment
  read at the top of this document confirms in both directions

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Starting state
> Objects created upstream are already `ISOLATION_MODE_ISOLATED`. Anything this
> sequence creates is open unless bound.

**Sources**

- [Workspace-catalog binding](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/access-control/workspace-catalog-binding),
  fetched 2026-08-12. Binding needs metastore admin, catalog owner or `MANAGE`, not
  account admin, so this step stays inside the workspace admin's reach.
- [What are catalogs in Azure Databricks?](https://learn.microsoft.com/en-us/azure/databricks/catalogs/),
  fetched 2026-08-12. "Catalogs are shared with all workspaces attached to the
  current metastore unless you specify a binding."

### 16. Enable the system table schemas

`Category: foundation` · `Owner: Databricks account admin` · `Inputs: metastore ID, from step 1` · `Prerequisite: none` · `Impact: Lossy`

**When to use** When you want audit, billing or lineage data to exist later, and
you accept that enabling it lands on every workspace sharing this metastore.

**Why it matters**

- Audit, billing and lineage history begins at enablement and never backfills.
  ⚠️ Unverified after a targeted re-read on 2026-08-13. The page documents
  per-table retention and says nothing either way about data from before
  enablement, and this step's whole urgency rests on it. One cheap test settles it:
  enable one schema and query for a timestamp older than the enablement
- Step 22 consumes it, so being late costs history and holds up monitoring.
  Nothing else in the sequence reads it
- Retention is a rolling window, and not a uniform one. 365 days for audit and
  billing, 180 for MLflow, 90 for node timeline and model serving usage, 30 for
  inbound network events, 13 months for data classification results, indefinite for
  node types, pricing, workspaces and data quality monitoring
- Anything needed beyond its window has to be copied out, and the publisher
  discourages exactly that. Databricks "highly discourages you from moving this data
  outside the platform because it can expose sensitive data and put your deployment
  at risk", and puts the security of anything exported on you. So the retention
  window is a real constraint rather than an inconvenience to engineer around, and
  going past it is a decision with an owner
- A firewalled environment may need one more thing. Enabling system tables "might
  need network access to the system tables Blob storage endpoint", which is the same
  class of problem as step 6 and is not covered by step 6's work
- Enabling them does not make them readable. Default access belongs to users
  holding the account admin and metastore admin roles together, not either one
  alone. Everyone else needs `USE CATALOG` on `system` plus `USE SCHEMA` and
  `SELECT` on each schema
- This metastore has no metastore admin. It was created by automatic enablement, so
  the role was never assigned, and an account admin alone cannot grant on a catalog
  they do not own. Assigning a metastore admin is therefore part of this request,
  not a later tidy-up. Without it nobody can read what this step enables
- Make the grants here, in the same request. Step 22's owner cannot make them for
  themselves

**What getting the execution wrong costs**

- Every day unenabled is a day of audit and billing history that cannot be
  recovered
- Enablement is per metastore, not per workspace, so it lands on every workspace
  sharing that metastore

**The play**

- Read the current state first. A workspace admin can do this much:

```bash
P=<profile>
databricks -p "$P" schemas list system -o json | grep '"name"'
```

- Anything beyond `information_schema` and `ai` is already enabled
- The enablement endpoint is account-scoped and refuses a workspace admin on
  read as well as write:

```bash
databricks -p "$P" api get \
  /api/2.0/unity-catalog/metastores/<metastore-id>/systemschemas
# Error: User is not an account admin for Account.
```

- An account admin lists the schemas with their states, then enables each wanted
  schema by name

```bash
databricks api put \
  /api/2.0/unity-catalog/metastores/<metastore-id>/systemschemas/<schema>
```

- Then grant, once per schema, as the metastore admin. Enabling without granting
  leaves the data collected and unreadable

```sql
GRANT USE CATALOG ON CATALOG system TO `<group>`;
GRANT USE SCHEMA ON SCHEMA system.access TO `<group>`;
GRANT SELECT ON SCHEMA system.access TO `<group>`;
```

- Repeat the two schema grants for every schema enabled above. Backtick the
  principal. A service principal is named by its application ID, not its display
  name

> ⚠️ Unverified. Neither the enable call nor the grants could be run from this
> position. Only the refusal is proven. The `GRANT` syntax follows the documented
> pattern for catalogs and schemas rather than an example for `system`.

**Check**

- Re-run the `schemas list` read. Each enabled schema appears in the `system`
  catalog
- A schema stays `UNAVAILABLE` where the region or tier does not carry it

Result for this deployment, read 2026-08-11:

| Field | Value |
| :--- | :--- |
| Schemas visible in `system` | `information_schema`, `ai` |
| `access`, `billing`, `compute`, `lakeflow`, `query` | Not present |
| `systemschemas` endpoint as workspace admin | Refused, not an account admin |

> [!warning] The metastore is shared
> - Enabling a schema starts collection for every workspace on the metastore
> - The request goes to whoever owns the metastore, not to any account admin
> - It sits here for reading order and waits on nothing, so raise it as soon as
>   an account admin is available

**Sources**

- [System tables reference](https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/),
  fetched 2026-08-12, re-read 2026-08-13, page dated 2026-08-10. Enablement is per
  metastore and the metastore "needs to be on Unity Catalog Privilege Model Version
  1.0". "Users with both the account admin and metastore admin roles have access to
  system tables by default", and the page notes in the same section that an account
  created after November 9, 2023 "might not have a metastore admin by default". To
  allow anyone else, "the admin must grant users the following permissions:
  `USE CATALOG` on the system catalog, `USE SCHEMA` on the system schemas, and
  `SELECT` on the system schemas". Retention is per table, 30 days to indefinite.
  Exports carry a warning: Databricks "highly discourages you from moving this data
  outside the platform". Enabling "might need network access to the system tables
  Blob storage endpoint". `system.operational_data` and `system.lineage` are
  deprecated and empty. Still silent on whether data predating enablement is
  available, after a targeted re-read, which is why this step keeps its flag.
- [Manage privileges in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/),
  fetched 2026-08-13. The `GRANT` pattern this step's play follows,
  `GRANT <privilege-type> ON <securable-type> <securable-name> TO <principal>`, with
  worked examples on a catalog and a schema. Grants can be made by the object owner,
  the owner of the containing catalog or schema, a holder of `MANAGE`, or a metastore
  admin. An account admin can grant on a metastore but is not listed as able to grant
  on a catalog they do not own, which is why a metastore admin has to exist first. A
  principal goes in backticks, and a service principal is named by its
  applicationId.
- [Admin privileges in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/admin-privileges),
  fetched 2026-08-11. Lists "Enable system tables" among the account admin
  capabilities, "Enable system tables and control who can access them". That is the
  documentary basis for this step's owner, and the endpoint refusal above confirms
  it from the other direction.
- [Features with limited regional availability](https://learn.microsoft.com/en-us/azure/databricks/resources/feature-region-support),
  fetched 2026-08-11. System tables by region.

### 17. Create compute policies with enforced tags

`Category: compute` · `Owner: workspace admin` · `Inputs: the tag names enforced by Azure Policy, from step 3` · `Prerequisite: 🔲 ADR serverless or classic posture, 🔲 ADR tagging and budget route` · `Impact: Rework 5d`

Serverless compute and serverless SQL warehouses are available in
`francecentral` and enabled on the workspace. Steps 18 and 19 take it from here.

**When to use** When someone will create clusters.

**Why it matters**

- Untagged compute is unattributable spend, and a policy cannot reach compute
  created without one. That is what leaves the provisioned starter warehouse and
  anything predating this step untagged for good
- Revising a policy later is a different matter and is supported. Compute already
  under it goes out of compliance and `Enforce all` updates it, immediately for
  jobs compute and on next restart for all-purpose
- Policies limit what users can create, cap compute resources per user and cap
  DBUs per hour. That is the main lever on cluster cost, with the budget policy at
  step 18 covering what it cannot reach
- Unrestricted cluster creation defeats all of it. A principal holding that
  entitlement also gets the Unrestricted policy and "can create fully configurable
  compute resources". The deployment principal read at step 4 holds exactly that

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] This does not cover SQL warehouses
> - Compute policies govern clusters and jobs only
> - Step 18 does not pick up the difference. A serverless usage policy covers
>   notebooks, jobs, pipelines and serving endpoints, and not SQL warehouses
> - A warehouse accepts tags at creation and nothing enforces them, which leaves
>   step 19 as the only place serverless warehouse spend is ever attributed
> - Four mechanisms across the estate: Azure Policy on Azure resources, compute
>   policies on clusters and jobs, serverless usage policies on serverless
>   notebooks and jobs, per-warehouse tags. One vocabulary, nothing reconciling
>   them
> - Steps 17 and 18 are complementary and still do not cover everything between
>   them

**Sources**

- [Create and manage compute policies](https://learn.microsoft.com/en-us/azure/databricks/admin/clusters/policies),
  fetched 2026-08-12. Policies limit a user or group's compute creation, cap
  resources per user and DBUs per hour, and carry a Tags section for custom tag
  rules. They need the Premium plan. Editing a policy does not update existing
  compute automatically, but `Enforce all` does, on next restart for all-purpose and
  immediately for jobs compute. A user with unrestricted cluster creation also gets
  the Unrestricted policy and "can create fully configurable compute resources". The
  page describes all-purpose and jobs compute only, never SQL warehouses.
- [Set up serverless SQL warehouses](https://learn.microsoft.com/en-us/azure/databricks/admin/sql/serverless),
  fetched 2026-08-12. Cluster policies are not supported on serverless warehouses.
  That is the other half of the coverage gap above.
- [Attribute usage with serverless usage policies](https://learn.microsoft.com/en-us/azure/databricks/admin/usage/budget-policies),
  fetched 2026-08-12. What step 18 covers and does not, and therefore where the gap
  between the two mechanisms falls.

### 18. Create the serverless usage policy

`Category: compute` · `Owner: workspace admin, or a holder of Serverless usage policy: Manager. The account-level billing admin role to see and manage every policy in the account` · `Inputs: the tag scheme, plus serverless availability and enablement, both from step 17` · `Prerequisite: 🔲 ADR tagging and budget route` · `Impact: Lossy`

Called a budget policy until recently. The documentation now says serverless usage
policy, which describes it better.

**When to use** When serverless notebooks, jobs, pipelines or serving endpoints
run here and their cost has to be attributed to something.

**Why it matters**

- It attributes, it does not cap. The policy is a set of tags applied to the
  serverless activity of the users assigned to it, landing in
  `system.billing.usage` and in Azure cost analysis. Spend limits are a separate
  budgets feature
- It does not cover SQL warehouses. Serverless warehouse spend is attributed by
  the tags set on the warehouse itself at step 19, and by nothing else
- Nothing is retroactive. Tags apply only to usage initiated after the change, and
  existing notebooks, jobs and pipelines are not assigned a policy when their owner
  is granted one. Each has to be updated by hand
- A user holding several policies who selects none gets whichever sorts first
  alphabetically. That is a misattribution nobody notices until the bill. Assigning
  exactly one policy per user removes it outright, because a single assignment
  applies automatically with nothing to select
- Two attribution holes survive any assignment scheme. A pipeline triggered by a
  job does not inherit the job's policy and needs its own, and a policy ID stored
  on an asset outlives the policy itself, applying no tags and reporting no error

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

**Sources**

- [Attribute usage with serverless usage policies](https://learn.microsoft.com/en-us/azure/databricks/admin/usage/budget-policies),
  fetched 2026-08-12, re-read 2026-08-13, page dated 2026-07-10. Still Public
  Preview, and renamed from budget policy. It applies cost attribution tags and does
  not cap spend. "You must be a workspace admin to create serverless usage
  policies", non-admins can manage one with Serverless usage policy: Manager, and
  the billing admin role is needed to view and manage all policies in the account,
  not only to view them. It covers notebooks, jobs, pipelines, serving endpoints,
  Lakebase and Apps, never SQL warehouses, and "Serverless usage policies do not
  apply tags to classic compute resources". "Policy changes are only applied to
  usage initiated after the policy update", existing assets are not assigned a
  policy automatically, and "If a user doesn't select a policy, the setting defaults
  to whichever policy comes first alphabetically". A single assigned policy "is
  automatically applied to the user's newly created resources". Two silent gaps:
  "Pipelines triggered by jobs do not inherit the job's serverless usage policy",
  and "Policy IDs stored with an asset remain even if the policy is deleted. These
  policies do not apply any tags." Development-mode pipelines take 24 hours to pick
  up a tag change.

### 19. Create SQL warehouses and set permissions

`Category: compute` · `Owner: workspace admin` · `Inputs: the groups that get CAN USE, from step 8, usable here only once assigned to the workspace at step 9; serverless availability and enablement, from step 17` · `Prerequisite: 🔲 ADR serverless or classic posture` · `Impact: Adjustable`

**Why it matters**

- What the acceptance test runs on, and what step 12's write test needs before
  that. Nothing else in the sequence produces compute
- `CAN USE` both starts the warehouse and runs queries on it. The cluster
  equivalent is `CAN RESTART`, because `CAN ATTACH TO` alone cannot start a
  stopped one
- `CAN MONITOR` also starts the warehouse and runs queries. It reads as
  observational and is not, so it is the wrong grant for anyone who should only
  look
- Creating a warehouse needs workspace admin or unrestricted cluster creation,
  the same entitlement that step 17 notes defeats every compute policy

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!warning] The workspace does not start policy-clean
> - A `Serverless Starter Warehouse` exists from provisioning, stopped, untagged
> - Step 17 cannot reach back and tag it
> - Decide: delete, tag or keep. Record which
> - Compute created before the policies stays untagged. Nothing fixes it after

> [!warning] The API default is not the UI default
> - UI default: serverless. API default: classic
> - For serverless from the API, set `warehouse_type` to `pro` **and**
>   `enable_serverless_compute` to `true`
> - Set both explicitly. This runbook deploys from the repo, not the UI

**Sources**

- [Access control lists](https://learn.microsoft.com/en-us/azure/databricks/security/auth/access-control/),
  fetched 2026-08-12. The SQL warehouse ACL table gives `CAN USE` both start and run
  queries, and gives `CAN MONITOR` the same two plus the monitoring tab, so
  `CAN MONITOR` is not read-only. Creating a warehouse needs workspace admin or
  unrestricted cluster creation. On clusters, `CAN ATTACH TO` attaches to a running
  one and `CAN RESTART` is what starts a stopped one.
- [SQL warehouse types](https://learn.microsoft.com/en-us/azure/databricks/compute/sql-warehouse/warehouse-types),
  fetched 2026-08-11. Classic, pro and serverless capabilities, and the differing UI
  and API defaults.

### 20a. Settle the SQL semantics

`Category: admin` · `Owner: workspace admin` · `Inputs: the current warehouse config, read in the play` · `Prerequisite: 🔲 ADR legacy surface posture` · `Impact: Rework 10d`

**When to use** When the same query has to mean the same thing on every kind of
compute here.

**Why it matters**

- `ansi_mode` is `false` on this workspace while ANSI mode is "Enabled by default
  in Apache Spark 4.0 and Databricks Runtime 17.0 and above". The same SQL then
  behaves differently by compute: an invalid cast returns null here and throws
  there, and integer overflow wraps instead of erroring
- Changing it later is a migration, not a toggle. Every query written against the
  old behaviour has to be re-checked, which is what the ten days is
- It has to be settled before step 12 writes anything, not after step 23 reads it.
  Moving it afterwards invalidates the acceptance test rather than following it

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

> [!info] Starting state
> - `ansi_mode` is `false` at workspace level. Not merely legacy: it is an
>   override against the current platform default, which is on
> - Decide whether it stays and record why, rather than inheriting it by accident
> - Read with `databricks -p "$P" warehouses get-workspace-warehouse-config`
> - `spark.sql.storeAssignmentPolicy` is a separate setting and defaults to
>   `ANSI` regardless, so table inserts already reject bad casts even here

**Sources**

- [ANSI compliance in Databricks Runtime](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-ansi-compliance),
  fetched 2026-08-12. `spark.sql.ansi.enabled` defaults to true and is "Enabled by
  default in Apache Spark 4.0 and Databricks Runtime 17.0 and above", so this
  workspace's `ansi_mode: false` diverges from it. Invalid casts return null rather
  than throwing, and integer overflow wraps.
  `spark.sql.storeAssignmentPolicy` is independent and defaults to `ANSI`.

### 20b. Close the routes around Unity Catalog

`Category: admin` · `Owner: workspace admin` · `Inputs: the current workspace settings, read in the play` · `Prerequisite: 🔲 ADR legacy surface posture` · `Impact: Rework 10d`

**When to use** When you want the grants at step 13 to be the only route to the
data.

**Why it matters**

- The DBFS file browser, the upload data UI, the web terminal, no-isolation
  shared clusters and access for Databricks personnel are each a way to reach
  data without going through Unity Catalog, and therefore around every grant made
  at step 13
- Restrict workspace admins belongs here too. It is the only setting on the list
  that constrains the role every other step in this runbook runs as, including
  creating tokens on behalf of the service principals from step 4
- Leaving the defaults is a decision as much as changing them, and it is the one
  that leaves the routes open

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

**Sources**

- [Manage your workspace](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace-settings/),
  fetched 2026-08-12. The settings this step covers: the DBFS file browser, the upload
  data UI, the web terminal, user isolation enforcement, workspace access for
  Databricks personnel, and Restrict workspace admins.

### 21. Apply classification tags, column masks, row filters

`Category: protection` · `Owner: the table owner, or a user with MANAGE` · `Inputs: the schemas and tables to protect, from step 12; the groups the masks discriminate between, from step 8; settled SQL semantics, from step 20a` · `Prerequisite: 🔲 ADR data protection model` · `Impact: Rework 8d`

**When to use** When some readers must not see rows or values that others can.

**Why it matters**

- `ansi_mode` is `false` here, and that makes these controls fail open. If a
  filter's parameter type does not match the column, the value is silently cast to
  `NULL` and no error is raised, so a filter testing for `NULL` returns every row
  instead of filtering. Step 20a is a prerequisite for this step, not an unrelated
  setting
- Databricks recommends ABAC policies over what this step's title describes. They
  attach at catalog or schema level, apply automatically from governed tags, and
  table owners "can't override or remove them". Table-level masks are the reverse:
  the table owner applies them and can take them off again
- The owner is the table owner or someone with `MANAGE`. Workspace admin does not
  confer it, which is why this step's owner differs from almost every other step
- They remove capability as well as adding protection. No masks on views, no time
  travel, no deep or shallow clones, no path-based access, and `MERGE` is
  restricted

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

**Sources**

- [Row filters and column masks](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/filters-and-masks/),
  fetched 2026-08-12. Table-level filters and masks are "managed by the table owner"
  or a user with `MANAGE`, which resolves this step's owner. Databricks recommends
  ABAC policies instead, attached at catalog or schema level from governed tags, which
  "table owners can't override or remove". With ANSI mode disabled, a parameter type
  mismatch silently casts to `NULL` so a row filter can return every row, and the page
  recommends enabling ANSI mode so the cast raises instead. Views, time travel,
  clones, path-based access and several `MERGE` cases are unsupported.
- [Network Security Perimeter for Azure Storage](https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security-perimeter),
  fetched 2026-08-12. Azure Backup is unsupported on an account associated with a
  perimeter, which removes one mechanism from the data protection ADR if step 6 takes
  route A. Container immutability and lifecycle policies are unaffected, being storage
  account features rather than a backup service.

### 22. Configure monitoring and alerting

`Category: protection` · `Owner: workspace admin for the system tables, once granted on system by an account or metastore admin at step 16, Databricks account admin for account-wide budgets` · `Inputs: the system tables, from step 16; the tag scheme, from steps 17 and 18` · `Prerequisite: none` · `Impact: Adjustable`

**When to use** When cost or access has to be noticed without someone thinking to
look.

**Why it matters**

- It has a horizon. System table retention runs from 30 days to indefinite by
  table, with most at 365, so anything monitoring must answer beyond a table's own
  window has to be copied somewhere else before it ages out. Step 16 records why
  copying it out is not a free choice
- Budgets alert, they do not cap. Databricks is explicit that they are not "a way
  to ensure an absolute spend cap on final billed amounts", and notification can
  trail usage by up to 24 hours
- Budgets discriminate by workspace, product and custom tag. That is what the
  tagging at steps 17, 18 and 19 was for, and spend that arrived untagged cannot
  be separated out here afterwards
- The owner splits three ways. Reading the system tables needs the grants from
  step 16, an account-wide budget needs a Databricks account admin, and a
  workspace admin can only cover workspaces they administer, through Governance
  Hub

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

**Sources**

- [Create and monitor budgets](https://learn.microsoft.com/en-us/azure/databricks/admin/account-settings/budgets),
  fetched 2026-08-12. Account admin to create and manage, or a workspace admin through
  Governance Hub for workspaces they administer. Budgets are scoped by workspace,
  product and custom tag, carry up to four thresholds each, and alert by email. "Do not
  use this feature as a way to ensure an absolute spend cap on final billed amounts."
  Notification can lag usage by up to 24 hours, and `system.billing.usage` updates every
  few hours, so the three sources disagree at any given moment by design.
- [System tables reference](https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/),
  fetched 2026-08-12, re-read 2026-08-13. The per-table retention window, 30 days to
  indefinite, which sets this step's horizon, and the grants a reader who holds
  neither the account admin nor the metastore admin role needs. Also the reason
  copying data out to beat retention is not a free choice.

### 23. Acceptance test

`Category: acceptance` · `Owner: test user` · `Inputs: a principal that can write to the bronze schema, from step 4 with its grants from step 14; the bronze catalog and schema, from steps 11 and 12; the grants that let a group read them, from step 13; a warehouse the test user can use, from step 19; the test user's group membership and entitlements, from steps 8 and 9` · `Prerequisite: none` · `Impact: Adjustable`

**Why it matters**

- The only step run as someone who is not an admin. Every earlier check passed
  for a workspace admin who owns what they created, and "catalog owners have all
  privileges on the catalog and the objects in the catalog", so not one of them
  tested a grant
- Two identities, not one. The automated write proves step 14's grants on the CI
  principal, and the read proves step 13's grants reaching a person through a
  group. Either can pass while the other fails

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

**Sources**

- [What are catalogs in Azure Databricks?](https://learn.microsoft.com/en-us/azure/databricks/catalogs/),
  fetched 2026-08-12, re-read 2026-08-13. "Catalog owners have all privileges on the
  catalog and the objects in the catalog, and they can grant access to any object in
  the catalog". No earlier check in this runbook therefore tested a grant.

---

## When it fails at step 23

Read the error rather than re-running the earlier steps.

| What you see | Where it actually broke |
| :--- | :--- |
| A serverless query cannot reach the storage account, and the error reads as permissions | Step 6, the private endpoint rule is `PENDING` rather than `ESTABLISHED`, public network access was closed before approval, or the account was set to Secured by Perimeter |
| A classic cluster cannot reach the storage account but serverless can | Step 6, the path from your own VNet is missing |
| The ingestion pipeline cannot write the table | Step 11 or 12, the catalog or schema has no usable managed location, or step 7's external location is missing |
| Writes fail with a storage authorisation error | Step 7, the connector identity lacks Storage Blob Data Contributor on that container |
| The table is created but the group cannot see the catalog | Step 13, `USE CATALOG` is missing |
| The catalog is visible but the table is not | Step 13, `USE SCHEMA` is missing |
| The table is visible but the query is denied | Step 13, `SELECT` is missing |
| The group member has no warehouse to run on | Step 19, no `CAN USE` on the warehouse |
| The group member cannot open the SQL editor at all | Step 9, the Databricks SQL access entitlement was not assigned explicitly |
| Everything works for you and nothing works for them | You are a workspace admin. Test as the test user, on their credentials, or you are testing nothing |

> [!todo] 🔲 What remains before status leaves Draft
> - The empty fields, not the sourcing. `The play` and `Check` are still `🔲` on
>   steps 5, 7, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20a, 20b, 21, 22 and 23
> - Every source now sits under the step or section it backs, with the date it was
>   fetched. A source consumed by several steps appears in full under each

<!--
Version: 3.3 | Last Updated: 2026-08-13 | Status: Draft
-->
