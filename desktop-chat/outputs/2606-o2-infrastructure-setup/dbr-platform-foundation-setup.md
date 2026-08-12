# Databricks platform foundation setup

> One ordered sequence from a provisioned workspace to check the readiness for work. 
> Decisions are not taken here. They arrive as accepted ADRs, and each step names the one it
> consumes.

This runbook assumes one configuration and does not generalise beyond it: a
Terraform-provisioned, VNet-injected, Premium workspace, automatically enabled
for Unity Catalog, where workspace admin reaches a human through an Entra group
and account admin is held elsewhere. The workspace already contains infrastructure. It contains no work.

## What counts as done

Step 23 is the finish line: **data arrives in a governed bronze table by an
automated path, and a group member who did not create it reads it.** Deployed
from the repo, not from the UI.

Source-neutral on purpose. The first real source is SharePoint, which is
temporary, and the mechanism will change. What must hold is the governed
destination and the read, not any one ingestion route.

## Preconditions

### Entry condition

The gate is per step, not up front. An ADR must be Accepted before the first
step that consumes it, and not before. The `First consumed` column below is
therefore a deadline, one per ADR. Steps 1, 2, 3, 16, 22 and 23 consume no ADR
and can run against an empty decision record.

### ADRs

Ordered by the first step that consumes them. The `Depends on` column carries the
order they must be accepted in, which is not the same order.

| ADR | Subject | First consumed | Also consumed by | Depends on |
| :--- | :--- | :--- | :--- | :--- |
| ✅ | Group provenance | 4 | 8, 9, 13, 14 | none |
| 🔲 | Non-human identity model | 4 | 14 | Group provenance |
| 🔲 | Deployment model | 5 | Every step that changes state | none |
| 🔲 | Catalog and schema model | 5 | 7, 11, 12 | Workspace topology |
| 🔲 | Network posture | 6 | none | Serverless or classic posture |
| 🔲 | Access Connector and external location granularity | 7 | none | Catalog and schema model, Metastore root storage |
| 🔲 | Workspace topology | 8 | 9, 15 | none |
| 🔲 | Ownership and grant model | 8 | 13, 14 | Workspace topology, Catalog and schema model |
| 🔲 | Secret scope model | 10 | none | none |
| 🔲 | Metastore root storage and MANAGED LOCATION policy | 11 | none | Workspace topology |
| 🔲 | Serverless or classic posture | 17 | 19 | none |
| 🔲 | Tagging and budget route | 17 | 18 | Serverless or classic posture |
| 🔲 | Legacy surface posture | 20a | 20b | none |
| 🔲 | Data protection model | 21 | 5 | Catalog and schema model |

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

Acceptance order, derived from the `Depends on` column: workspace topology first,
then metastore root storage and the catalog and schema model, then Access
Connector granularity and the ownership and grant model, then the rest.

> [!warning] Two ADRs are due earlier than their row suggests
> - Network posture is consumed at step 6, which is early. Serverless cannot
>   reach firewalled storage without it
> - It depends on serverless or classic posture, so that one is also due before
>   step 6 despite showing 19
> - Both are owned outside this team. Start them first
> - Only the data protection ADR at step 21 can genuinely lag, and only while
>   nothing sensitive has landed

### Identities

| Role | Needed for | Held by |
| :--- | :--- | :--- |
| Databricks account admin | 6, 16, 18, and the federation policy half of 4 | 🔲 |
| Workspace admin | 1, 2, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20a, 20b, 21 | gmourgues@sqli.com |
| Platform engineer | 3, 5, 22 | 🔲 |
| Entra admin | 8, for every group that does not already exist in Entra, and for every membership change afterwards | 🔲 |
| Test user | 23 | 🔲 |

Workspace admin is not granted to a person here. It arrives through an Entra
group and materialises as membership of the workspace `admins` group. The
control point is therefore Entra group membership, not anything inside
Databricks.

### What to ask the Databricks account admin for

Account admin here is a Databricks account console role. It is not an Azure role
and holding Owner or Contributor in Azure does not confer it.

Three steps and one half-step need it. Raise them as one request. Step numbers
are not a request, so this is what to actually ask for.

| Request | Unblocks |
| :--- | :--- |
| Serverless network access to the managed storage account, either a network security perimeter rule or a network connectivity configuration with private endpoint rules | 6 |
| Enable the system table schemas | 16 |
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

- The Databricks CLI reads metastore state with no compute running, which is the
  only way to complete step 1 before a warehouse exists
- Creating a warehouse early lands untagged compute ahead of the policies at
  step 17
- Homebrew refuses the Databricks formula until the tap is trusted:
  `brew trust --formula databricks/tap/databricks`

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
| Workspace identity | A resource ID whose `workspaceUrl` matches your host, plus its resource group and managed resource group | In each resource group you can read: `az resource list -g <rg> --resource-type Microsoft.Databricks/workspaces`, then `az resource show --ids <id> --query "{url:properties.workspaceUrl, rg:resourceGroup, managedRg:properties.managedResourceGroupId}"` until `url` matches |
| Workspace configuration | Premium, no public IP | `az resource show --ids <id> --query "{sku:sku.name, noPublicIp:properties.parameters.enableNoPublicIp.value}"` |
| Operator Azure rights | Specifically: whether you can write role assignments, and whether you can read the managed resource group. Those two decide steps 5 and 7 | `az role assignment list --assignee <your-object-id> --all --include-groups -o table`. The `--include-groups` flag is not optional, since the grant usually arrives through a group |
| Metastore attached | A metastore in the workspace region | `databricks -p "$P" metastores summary` |
| Access connector | One, in the workspace's managed resource group, which you will not be able to read directly | `access_connector_id` in the storage credential below |
| Storage credential | One, named after the workspace, `ISOLATION_MODE_ISOLATED`, owned by `_workspace_admins_<workspace>` | `databricks -p "$P" storage-credentials list -o json` |
| External location | One, before this sequence runs. Step 7 adds more | `databricks -p "$P" external-locations list -o json` |
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

### Environment checks

Two things the baseline cannot tell you. Both cheap, both consequential.

**Someone holds Databricks account admin.**

- Three steps and one half-step need it. It does not flow from the Entra group
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
- **When to use.** One sentence, in the reader's own terms, and only on steps
  where declining is a real option. Test it by asking whether a competent reader
  could answer "not me". If nobody could, cut the field rather than write a
  sentence everyone agrees with. Absent therefore means the step is forced by an
  earlier one, and its presence is itself a signal
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

## Proven against a live workspace

Exercised 2026-08-11 and 2026-08-12 with throwaway objects, since deleted. Proves
the platform permits the step and the operator holds the rights. Does not mean
the step is done, or that the Terraform produces the same result.

| Step | What was exercised | Verdict |
| :--- | :--- | :--- |
| 1, 2, 3 | The reads, in full | Passed |
| 4 | Created a Databricks managed principal with a display name, as a workspace admin | Creation works. Federation untested |
| 5 | Created a tagged storage account with hierarchical namespace and a container | Passed, and an untagged create was refused first, so the deny policy bites |
| 6 | Nothing | Untested. Needs a Databricks account admin |
| 7 | Attempted the prerequisites | **Failed.** The operator cannot write role assignments and cannot read the access connector |
| 8, 9 | Created an account group with entitlements, as a workspace admin | The mechanism works, but the group provenance ADR now forbids creating one. The pull-in path is untested |
| 10 | Created a scope, a secret and an ACL | Passed, and it exposed that account-level principals are refused here |
| 11, 12 | Created a catalog with an explicit managed location and a schema, then wrote and read a table | Passed. The managed storage path works end to end |
| 13, 14 | Granted a group and a service principal on a catalog | Passed |
| 15 | Confirmed the binding controls are present and editable | Passed |
| 17 | Created a compute policy with an enforced tag | Passed |
| 19 | Created a serverless warehouse with tags | Passed |
| 16 | Read the `system` catalog, then called the enable endpoint | Refused. Confirms a Databricks account admin is required, and that only two schemas are on |
| 18, 21 | Nothing | Untested. Step 18 was assumed to need a Databricks account admin and does not, so a workspace admin can exercise it |
| 20a, 20b, 22, 23 | Nothing | Untested |

Step 7 is the one that failed, and it is the reason the storage path has to come
from the Terraform. See [[2026-08-11-databricks-terraform-changes]].

Steps 11 and 12 were proved against the workspace's own Unity Catalog container,
not against the durable account at step 5. The mechanism is proven, the target is
not.

## Order challenge

Each step is pushed as late as its consumers allow. A step's earliest consumer is
the first later step that cannot run without its output, and the step can sit
anywhere above that. Recorded only. The numbering below is unchanged, so a
position in this table is a finding, not an instruction.

Constraints here are relative, not absolute slots. A step held before another
moves whenever that other one moves, so a chain travels together and is only
pinned by the last consumer in it.

| Step | Earliest consumer | Can sit as late as | Why it can move |
| :--- | :--- | :--- | :--- |
| 1 | 11, which branches on the root storage state | Immediately before 11 | Only step 2 reads anything from it, and only the region string, which the baseline's Azure read also yields |
| 2 | 6, through the network posture ADR's dependency on the serverless or classic ADR | Immediately before 5 | Its declared consumers are 17, 18 and 19, but the ADR chain pulls it forward to 6 |
| 3 | 5, which needs the enforced tag names at creation | Immediately before 5 | Inputs come from the baseline, not from 1 or 2 |
| 4 | 14, which grants the CI principals | Immediately before 14 | Inputs are read in the play and from the baseline IaC repo row. Independent of 1, 2 and 3 |
| 5 | 6, which needs the storage account resource ID | Immediately before 6, and 6 itself moves | Fixed relative to 6 and 7, not to the numbering. Nothing consumes the 5, 6, 7 chain until 11, so the three travel together and can sit after the identity work |
| 6 | 7, which needs a working network path | Immediately before 7, carrying 5 with it | Splits in two. The verification is pinned between 5 and 7 and moves only with that chain. The request is not: it depends on nothing in this sequence and should be raised at step 1, since it has the longest lead time and two owners |
| 7 | 11, which needs the external location that holds managed data | Immediately before 11, carrying 5 and 6 with it | End of the storage chain, and nothing between 7 and 11 touches it. The identity work at 8, 9 and 10 can run entirely in parallel |
| 8 | 9, which assigns entitlements to the groups | Immediately before 9 | Head of the identity chain, independent of storage. Raise the Entra requests at step 1 regardless: a missing group is a directory ticket, and so is converting source of authority on a synced one |
| 9 | 10, which resolves scope ACLs against workspace principals | Immediately before 10, carrying 8 with it | Moves with the identity chain. Also gates 19, but 10 comes first. Nothing in the storage chain waits on it |
| 10 | None in this sequence | Anywhere after 9, or nowhere | No later step reads a secret. If the secret scope model ADR names no consumer, this is the one step with nothing downstream of it, and 9's earliest consumer becomes 19 instead |
| 11 | 12, which creates schemas inside the catalogs | Immediately before 12 | Where the storage and identity chains finally meet. It needs 7's external location and, for the grants at 13, nothing from 8. So it can start as soon as the storage chain lands, whatever the identity chain has reached |
| 12 | 13, which grants on the catalogs and schemas | Immediately before 13 | Cannot move earlier either. Its write test needs a warehouse, so it depends backwards on 19 unless the provisioned starter warehouse is still there. That is the only backwards dependency in the sequence |
| 13 | 23, the acceptance read | Immediately before 23 | The longest slack in the sequence. Nothing between 14 and 22 reads a grant. Do it early regardless: it owns the workspace catalog decision, and that surface has been open since the workspace was created |
| 14 | 23, the automated write | Immediately before 23 | Same slack as 13, and independent of it. One grants humans, the other grants the pipeline, and neither reads the other's output |
| 15 | None in this sequence | Anywhere after 11 | The second step with nothing downstream. Binding gates other tenants, and every step here runs inside this workspace. The reason to do it early is exposure time, not order: catalogs created at 11 are visible to the whole metastore until it is done |
| 16 | 22, which reads the system tables | Immediately before 22 | Consumes nothing, so it could be first. It is a request to a Databricks account admin, and if the backfill claim holds then every day it waits is a day of history lost, which argues for raising it at step 1 with the step 6 request |
| 17 | 18, which takes the tag scheme | Immediately before 18 | Not 19. Step 19's inputs claimed to consume the compute policies, but policies do not govern SQL warehouses. That input has been removed |
| 18 | None in this sequence | Anywhere after 17 | Fourth step with nothing downstream. It feeds cost reporting, which no step here reads |
| 19 | 23, which runs as the test user | Immediately before 23 | But 12's write test needs a warehouse, so in practice it comes earlier or borrows the provisioned starter warehouse. That backwards pull is the only thing holding it in place |
| 20a | 12, whose write test is the first SQL run against these semantics | Immediately before 12 | Sits at 20 by category, not by dependency. It is the second step after 6 that is placed later than its real consumer |
| 20b | None in this sequence | Anywhere after 13 | Nothing reads a workspace setting. It pairs with 13, since together they decide whether a grant is the only way in |
| 21 | None in this sequence | Anywhere after 12, and after 20a | Nothing reads a mask. The dependency runs the other way: it needs 20a settled first, or the filters fail open without saying so |
| 22 | None in this sequence | Last, or never | Reads 16 and the tag scheme, and nothing reads it. But every day it is absent is a day of cost and access nobody is watching, and system table retention is already counting down |
| 23 | Nothing. It is the finish line | Last by definition | The only step that cannot move. Its real prerequisites are 12, 13, 14 and 19, which is four of the five steps carrying the most slack in this table |

Recorded order for the gate block: **4, 3, 1, 2**. Step 4 leads because its
federation half waits on a repository that does not exist yet, so starting it
first buys lead time on the only part with an external dependency. The rest is
tooling, not data: 1, 2 and 4 need the Databricks CLI authenticated, 3 needs the
Azure CLI, and 3 is the platform engineer's while the others are the workspace
admin's, so it can run alongside rather than after.

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

Passed. No metastore root, so nothing to unwind before step 11.

### 2. Confirm serverless availability and enablement in region

`Category: gate` · `Owner: workspace admin` · `Inputs: region, from step 1` · `Prerequisite: Databricks CLI authenticated` · `Impact: Adjustable`

**When to use** When you do not want to design steps 17, 18 and 19 around
serverless that this region may not offer.

**Why it matters**

- Steps 17 and 19 consume the serverless or classic posture ADR, which cannot be
  decided without this
- Serverless SQL warehouses and serverless compute for notebooks, jobs and
  pipelines are separate mechanisms on separate configuration paths. Step 19
  needs the first, step 17 the second, and this step reads both
- Neither is switched on. Warehouses require the Premium plan and a supporting
  region, compute requires Unity Catalog and a supporting region, and a workspace
  meeting those has them already. Region is the condition that actually varies
- If serverless is out, step 19 becomes a pro SQL warehouse rather than a classic
  cluster, so the permission model is unchanged. What changes is location: pro
  and classic compute sits in your Azure subscription, which makes step 6's
  serverless path unnecessary and a path from your own VNet mandatory
- Step 18 loses its subject, since a serverless budget policy governs nothing
  without serverless spend

**What getting the execution wrong costs** The read is free. Assuming the answer
costs a compute policy and a budget route built around compute that does not
exist, discovered at step 19.

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

**When to use** When you want step 5's storage account created rather than
refused, and step 17 to enforce the same tag names Azure already does.

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

`Category: foundation` · `Owner: workspace admin, except the federation policy which is Databricks account admin` · `Inputs: existing service principals and their Entra records, read in the play; GitLab project and protected branches, from the baseline IaC repo row` · `Prerequisite: 🔲 ADR non-human identity model` · `Impact: Lossy`

Detail on the two principal kinds, the four authentication routes and the
federation build is in [[2026-08-10-databricks-cicd-service-principal]]. This
step carries only what changes what you do here.

**When to use** When you want automation that outlives the person who set it up
and that you can revoke one environment at a time.

**Why it matters**

- Automation must not run under a person's token. A principal is scoped
  independently, can be disabled on its own, and survives the person leaving
- The kind is a creation-time choice and it is not cosmetic. Entra managed
  authenticates to Databricks and to other Azure resources on one credential,
  which is the only case Databricks endorses it for. Databricks managed is the
  recommendation for everything else
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
- Do not plan to put them in a group either. Group provenance is Entra, and a
  Databricks managed principal cannot join an Entra group. Grant them directly
  at step 14, or make them Entra managed and accept the app registration
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
> - Explicit grants are the narrower alternative, parked at step 13
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

### 6. Confirm the serverless path to the managed storage account

`Category: gate` · `Owner: workspace admin to verify, Databricks account admin with an Azure network owner to build` · `Inputs: storage account resource ID, from step 5; workspace region, from step 1; the route taken, from the network posture ADR` · `Prerequisite: 🔲 ADR network posture` · `Impact: Rework 4d`

The path is not built here. Route A is entirely Azure-side and route B is built in
the Databricks account console, and both are owned outside this sequence. What
belongs here is the request, the record of which route was taken, and the proof
that it works.

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
| Built where | Azure portal only | Databricks account console, then an Azure-side approval |
| Mechanism | Perimeter left in transition mode, inbound rule for the regional `AzureDatabricksServerless` service tag | One private endpoint rule per subresource, `dfs` for Unity Catalog and `blob` for model serving |
| Waits on | Nothing after the rule is added | Each rule sits `PENDING` until someone with rights on the account approves it |
| End state | Public network access stays **Enabled from selected networks** | Public network access may be set to **Disabled**, which the source presents as optional hardening |
| Classic compute | Allow its IPs on the resource | Give it its own private endpoint from your VNet |

Secured by Perimeter is the trap in route A. It stops serverless reading external
locations and returns `PERMISSION_DENIED`. Applying route A's rules and then route
B's end state is the mistake that looks like a permissions bug.

> [!todo] 🔲 The build detail has no home yet
> The step-by-step for both routes belongs with step 7's storage work in
> [[2026-08-11-databricks-terraform-changes]], and has not been written there.
> Until it is, the table above is the only record of it. Do not delete it first.

**Check** Both compute planes, separately, because they take different paths.

- From serverless: `LIST 'abfss://<container>@<account>.dfs.core.windows.net/'`
  returns without error
- From a classic cluster: the same statement succeeds
- Route B only: every private endpoint rule reads `ESTABLISHED`, never `PENDING`

> [!warning] A general egress test proves nothing here
> Reaching public endpoints from a serverless notebook, such as
> `login.microsoftonline.com`, exercises Databricks' internet egress. This step
> is about a firewalled account inside your subscription, which is a different
> path under different controls. Only the `LIST` above tests it.

> [!info] Either route
> - Enable **Allow trusted Microsoft services** on the storage account. Route A
>   cannot connect without it in transition mode. Under route B's Disabled end
>   state it is probably inert, 🔲 unverified
> - Route B limits: 10 NCCs per region, 100 private endpoints per region, 50
>   workspaces per NCC. Databricks bills networking costs for serverless
>   connections
> - Route A is available here. Network security perimeter is generally available
>   in all Azure public cloud regions, Storage is an onboarded resource type, and
>   ADLS Gen2 is covered for HTTPS operations. Read 2026-08-12, closing an earlier
>   open question about France Central

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

### 7. Register the external locations over it

`Category: foundation` · `Owner: workspace admin` · `Inputs: the containers, from step 5; a working network path, from step 6; an access connector and storage credential` · `Prerequisite: 🔲 ADR catalog and schema model, 🔲 ADR Access Connector granularity, 🔲 ADR deployment model` · `Impact: Rework 3d`

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
>   principal ID is not readable by the operator and it dies with the workspace
> - A connector in a resource group you control is the durable choice, and needs
>   its own storage credential
> - The granularity ADR decides. Either way the role assignment is one, not four

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

### 16. Enable the system table schemas

`Category: foundation` · `Owner: Databricks account admin` · `Inputs: metastore ID, from step 1` · `Prerequisite: none` · `Impact: Lossy`

**When to use** When you want audit, billing or lineage data to exist later, and
you accept that enabling it lands on every workspace sharing this metastore.

**Why it matters**

- Audit, billing and lineage history begins at enablement and never backfills.
  ⚠️ Unverified — the system tables page documents retention but says nothing
  about data from before enablement, and this step's whole urgency rests on it
- Step 22 consumes it, so being late costs history and holds up monitoring.
  Nothing else in the sequence reads it
- Retention is a rolling window, and not a uniform one. 365 days for audit and
  billing, 180 for MLflow, 90 for node timeline, 30 for inbound network events,
  indefinite for a handful. Anything needed beyond its window has to be copied out
- Enabling them does not make them readable. Account admins and metastore admins
  have access by default, everyone else needs `USE CATALOG` on `system` plus
  `USE SCHEMA` and `SELECT` on each schema. That grant lands on step 22's owner

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

> ⚠️ Unverified. The enable call could not be run from this position. Only the
> refusal is proven.

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

### 17. Create compute policies with enforced tags

`Category: compute` · `Owner: workspace admin` · `Inputs: the tag names enforced by Azure Policy, from step 3` · `Prerequisite: 🔲 ADR serverless or classic posture, 🔲 ADR tagging and budget route` · `Impact: Rework 5d`

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

### 18. Create the serverless usage policy

`Category: compute` · `Owner: workspace admin. A billing admin only to see every policy in the account` · `Inputs: the tag scheme, from step 17` · `Prerequisite: 🔲 ADR tagging and budget route` · `Impact: Lossy`

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
  alphabetically. That is a misattribution nobody notices until the bill

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 19. Create SQL warehouses and set permissions

`Category: compute` · `Owner: workspace admin` · `Inputs: the groups that get CAN USE, from step 8, usable here only once assigned to the workspace at step 9` · `Prerequisite: 🔲 ADR serverless or classic posture` · `Impact: Adjustable`

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

### 22. Configure monitoring and alerting

`Category: protection` · `Owner: platform engineer for the system tables, Databricks account admin for account-wide budgets` · `Inputs: the system tables, from step 16; the tag scheme, from steps 17 and 18` · `Prerequisite: none` · `Impact: Adjustable`

**When to use** When cost or access has to be noticed without someone thinking to
look.

**Why it matters**

- It has a horizon. System table retention runs from 30 days to 365 by table, so
  anything monitoring must answer beyond that window has to be copied somewhere
  else before it ages out
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
  metastores. Account console navigation for step 1. Re-read 2026-08-12 for the
  removal semantics: the path cannot be modified once set, only removed and
  re-added, by an account admin. Removal pushes the root down into catalogs that
  have no storage root of their own, as their catalog-level managed location,
  without interrupting access, and may create an external location named
  `prior_metastore_root_location`. Afterwards every catalog must name a dedicated
  location registered as an external location, which is what step 11 relies on.
- [Specify a managed storage location in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/managed-storage).
  Managed storage precedence, and `ALTER CATALOG SET MANAGED LOCATION` on
  Databricks Runtime 18.1 and above, which affects only objects created after
  the change.

Added 2026-08-11 for step 2:

- [Connect to serverless compute](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/).
  Serverless is available by default in most workspaces and needs no enablement,
  provided Unity Catalog is on and the region supports it. Re-read 2026-08-12:
  the page covers notebooks, jobs and Lakeflow pipelines only, and states that
  serverless SQL warehouses, model serving and AI features use serverless
  infrastructure independently and have their own configuration paths. Step 2.
- [Set up serverless SQL warehouses](https://learn.microsoft.com/en-us/azure/databricks/admin/sql/serverless).
  Fetched 2026-08-12. Enabled by default. The requirements are the Premium plan
  and a supporting region. Cluster policies are not supported on serverless
  warehouses, which is the source for step 17's note. Storage firewalls must
  admit the serverless compute nodes, which is step 6.
- [Features with limited regional availability](https://learn.microsoft.com/en-us/azure/databricks/resources/feature-region-support).
  The serverless, system tables and ingestion tables by region.
- [SQL warehouse types](https://learn.microsoft.com/en-us/azure/databricks/compute/sql-warehouse/warehouse-types).
  Classic, pro and serverless capabilities, and the differing UI and API
  defaults, used at step 19.

Added 2026-08-11 for step 6:

- [Serverless compute plane networking](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/).
  What an NCC is, and the end of serverless subnet allowlisting on 9 June 2026.
- [Configure private connectivity to Azure resources](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-private-link).
  NCC creation, private endpoint rules, the Azure-side approval, the limits, and
  the requirement that classic compute also use private endpoints once a
  resource is restricted. Re-read 2026-08-12: "If you configure your Azure
  resource to only accept connections from private endpoints, any connection to
  the resource from your classic Databricks compute resources also must use
  private endpoints." Route B also requires the Premium plan and an account
  admin. Setting public network access to Disabled is presented as optional
  hardening, not as a required end state.

Fetched 2026-08-12, for the owner corrections and the file event roles:

- [Manage groups](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-groups).
  Workspace admins can create account groups and assign them to a workspace. The
  group provenance ADR uses only the second half. Steps 8 and 9.
- [Automatic identity management](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/automatic-identity-management/).
  On by default for accounts created after 1 August 2025. Entra is the source of
  truth and membership of a synced group cannot be updated in Databricks.
  Carried from [[2026-08-10-databricks-cicd-service-principal]], verified there.
  Step 8, and the service principal consequence at step 4.
- [Workspace-catalog binding](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/access-control/workspace-catalog-binding).
  Binding needs metastore admin, catalog owner or `MANAGE`, not account admin.
  Step 15.
- [Manage service principals](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/manage-service-principals).
  Creation is documented, renaming an existing principal is not. Step 4. Re-read
  2026-08-12: deactivation is named as preferable to removal, which is "a
  destructive action", and deletion stops compute, fails jobs and breaks Run as
  Owner sharing. Workspace admins cannot delete an account-level principal.
- [Service principals](https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/service-principals).
  Fetched 2026-08-12 for step 4. Databricks managed is the recommendation for
  Databricks automation, Entra ID managed only where a process "must authenticate
  with Azure Databricks and other Azure resources at the same time". The creator
  becomes service principal manager, which does not confer the service principal
  user role needed to run jobs as it.
- [Manage external locations](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/manage-external-locations).
  File events on by default, and the four role assignments. Only one of the four
  survives now that no files land in storage. Dated 2026-08-11, and it
  contradicts the June ADLS page on the EventGrid role name.
- [Configure an Azure network security perimeter](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-firewall-config).
  Route A, and why Secured by Perimeter breaks serverless. Step 6. Re-read
  2026-08-12: route A also hits classic compute, "Configuring a firewall also
  affects connectivity from classic compute resources. You must also update your
  resource access rules to allow the IPs for connections from classic compute
  resources." The service tag works only against Azure Storage in the workspace's
  region, the regional tag is preferred over the global one, and transition mode
  is recommended indefinitely rather than as a staging step.
- [Delete a workspace](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace/delete-workspace).
  The workspace catalog, managed resource group, storage and access connector all
  survive deletion unless force deleted. Re-read 2026-08-12: Databricks "converts
  the managed resource group into a regular resource group", retaining the Unity
  Catalog container and the access connector in it, which is step 5's second
  bullet verbatim. Deleting the resource group through the portal does not force
  delete it. Step 5.
- [Upgrade Azure Blob Storage with Azure Data Lake Storage capabilities](https://learn.microsoft.com/en-us/azure/storage/blobs/upgrade-to-data-lake-storage-gen2-how-to).
  Fetched 2026-08-12 for step 5. A hierarchical namespace can be enabled after
  creation. "An upgrade is one-way." Writes are disabled during it, and it will
  not pass validation while immutable storage, soft delete, blob snapshots or
  encryption scopes are enabled, or while page blobs are present.
- [Deploy a workspace using the Azure Portal](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace/create-workspace).
  No templates or sample catalogs at creation. Workspace type Hybrid means
  classic.
- [Monitor account activity with system tables](https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/).
  Enablement is per metastore and needs privilege model 1.0. The page names no
  role for enabling, so the account admin requirement at step 16 rests on the
  endpoint refusal, not on the documentation. Re-read 2026-08-12: each table has
  a free retention period, 30 to 365 days or indefinite depending on the table,
  and querying needs `USE CATALOG` on `system` plus `USE SCHEMA` and `SELECT` on
  each schema for anyone who is not an account or metastore admin. The page does
  not state whether data predating enablement is available, which is why step 16
  carries a flag.

Added 2026-08-12 for step 22, which had no source of its own:

- [Create and monitor budgets](https://learn.microsoft.com/en-us/azure/databricks/admin/account-settings/budgets).
  Account admin to create and manage, or a workspace admin through Governance Hub
  for workspaces they administer. Budgets are scoped by workspace, product and
  custom tag, carry up to four thresholds each, and alert by email. "Do not use
  this feature as a way to ensure an absolute spend cap on final billed amounts."
  Notification can lag usage by up to 24 hours, and `system.billing.usage` updates
  every few hours, so the three sources disagree at any given moment by design.

Added 2026-08-12 for step 21, which had no source of its own:

- [Row filters and column masks](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/filters-and-masks/).
  Table-level filters and masks are "managed by the table owner" or a user with
  `MANAGE`, which resolves that step's owner. Databricks recommends ABAC policies
  instead, attached at catalog or schema level from governed tags, which "table
  owners can't override or remove". With ANSI mode disabled, a parameter type
  mismatch silently casts to `NULL` so a row filter can return every row, and the
  page recommends enabling ANSI mode so the cast raises instead. Views, time
  travel, clones, path-based access and several `MERGE` cases are unsupported.

Added 2026-08-12 for step 20, which had no source of its own:

- [Manage your workspace](https://learn.microsoft.com/en-us/azure/databricks/admin/workspace-settings/).
  The settings surface this step covers, including the DBFS file browser, the
  upload data UI, the web terminal, user isolation enforcement, workspace access
  for Databricks personnel, and Restrict workspace admins.
- [ANSI compliance in Databricks Runtime](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-ansi-compliance).
  `spark.sql.ansi.enabled` defaults to true and is "Enabled by default in Apache
  Spark 4.0 and Databricks Runtime 17.0 and above", so this workspace's
  `ansi_mode: false` diverges from it. Invalid casts return null rather than
  throwing, and integer overflow wraps. `spark.sql.storeAssignmentPolicy` is
  independent and defaults to `ANSI`.

Added 2026-08-12 for step 19:

- [Access control lists](https://learn.microsoft.com/en-us/azure/databricks/security/auth/access-control/).
  The SQL warehouse ACL table gives `CAN USE` both start and run queries, and gives
  `CAN MONITOR` the same two plus the monitoring tab, so `CAN MONITOR` is not
  read-only. Creating a warehouse needs workspace admin or unrestricted cluster
  creation. On clusters, `CAN ATTACH TO` attaches to a running one and `CAN RESTART`
  is what starts a stopped one. Also the secret scope ACL levels for step 10.

Added 2026-08-12 for step 18, which had no source of its own:

- [Attribute usage with serverless usage policies](https://learn.microsoft.com/en-us/azure/databricks/admin/usage/budget-policies).
  Public Preview, and renamed from budget policy. It applies cost attribution tags
  and does not cap spend. "You must be a workspace admin to create serverless usage
  policies", with the billing admin role needed only to view every policy in the
  account. It covers notebooks, jobs, pipelines, serving endpoints, Lakebase and
  Apps, never SQL warehouses, and "do not apply tags to classic compute resources".
  Changes affect only usage initiated afterwards, existing assets are not assigned
  a policy automatically, and a user with several policies who picks none gets the
  first alphabetically.

Added 2026-08-12 for step 17, which had no source of its own:

- [Create and manage compute policies](https://learn.microsoft.com/en-us/azure/databricks/admin/clusters/policies).
  Policies limit a user or group's compute creation, cap resources per user and
  DBUs per hour, and carry a Tags section for custom tag rules. They need the
  Premium plan. Editing a policy does not update existing compute automatically,
  but `Enforce all` does, on next restart for all-purpose and immediately for jobs
  compute. A user with unrestricted cluster creation also gets the Unrestricted
  policy and "can create fully configurable compute resources". The page describes
  all-purpose and jobs compute only, never SQL warehouses.

Added 2026-08-12 for step 12, which the managed storage page above only half
covered:

- [Create schemas](https://learn.microsoft.com/en-us/azure/databricks/schemas/create-schema).
  Creating a schema needs `USE CATALOG` and `CREATE SCHEMA` on the parent catalog,
  plus `CREATE MANAGED STORAGE` on the external location if it names its own
  managed location. "Every Unity Catalog catalog automatically includes a
  system-provided read-only `INFORMATION_SCHEMA`", and the page names no other
  automatic schema.
- [What are catalogs in Azure Databricks?](https://learn.microsoft.com/en-us/azure/databricks/catalogs/).
  The three-level namespace, and the distinction between the workspace catalog and
  the workspace's default catalog setting. Neither is a per-catalog `default`
  schema, which is why step 12 does not claim one exists. Also step 13's
  inheritance bullet: "Users with `SELECT` on a catalog can read any table in the
  catalog", and a user "cannot access that table unless they also have the
  `USE CATALOG` privilege on the catalog that contains the table".

Added 2026-08-12 for step 8:

- [Configure Group Source of Authority (SOA) in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/hybrid/how-to-group-source-of-authority-configure).
  A synced group is read-only in the cloud, "any write attempts to the group in
  the cloud fail", and its fields are greyed out in the admin centre. Source of
  authority can be converted per group with a Graph PATCH setting
  `isCloudManaged`, needing Hybrid Administrator, the
  `Group-OnPremisesSyncBehavior.ReadWrite.All` scope, an Entra Free licence and a
  current sync client. Nested groups convert one at a time, lowest first. After
  conversion `onPremisesSyncEnabled` reads null, the same as a cloud-native group.

Added 2026-08-12 for step 6, on the Azure side of route A:

- [What is a network security perimeter?](https://learn.microsoft.com/en-us/azure/private-link/network-security-perimeter-concepts).
  Generally available in all Azure public cloud regions, so route A is open in
  France Central. Storage is an onboarded resource type. Service endpoint traffic
  "is not supported" and "can be denied even when an inbound rule allows
  0.0.0.0/0". Resource names are limited to 44 characters for a perimeter
  association to fit, which binds step 5's naming.
- [Network Security Perimeter for Azure Storage](https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security-perimeter).
  Perimeter rules override the account's own firewall. ADLS Gen2 is covered for
  HTTPS operations. Enforced mode does not honour trusted services. Azure Backup,
  object replication and static websites are unsupported on an associated
  account. This page's advice to move to enforced mode contradicts the Databricks
  page's advice to stay in transition.

Added 2026-08-12, settling what "Databricks-managed" means and whether it removes
steps 5 to 7:

- [Managed versus external assets in Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/managed-versus-external).
  Managed means Unity Catalog owns the location and lifecycle, not that Databricks
  holds the data. "The data files always remain in your cloud account."
- [Connect to cloud object storage using Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/).
  An external location is a path plus a storage credential, and assigning a managed
  storage location "must reference an external location object". Also warns that
  granting identities direct storage access to managed tables bypasses Unity
  Catalog, and that direct storage access is unsupported for managed tables.
- [Default storage in Databricks](https://learn.microsoft.com/en-us/azure/databricks/storage/default-storage).
  Storage in the Databricks account. Catalogs on it are "only available in
  serverless workspaces" and classic compute cannot interact with it, so it is
  unavailable to this VNet-injected workspace.

Added 2026-08-12 for step 3, which had no source of its own:

- [Azure Policy deny effect](https://learn.microsoft.com/en-us/azure/governance/policy/concepts/effect-deny).
  Deny prevents the request before it is sent to the resource provider and returns
  `403 (Forbidden)`. Existing resources matching a deny definition are marked
  non-compliant rather than removed.
- [Azure resource providers and types](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-providers-and-types).
  A subscription must be registered for a provider before its resources can be
  created, and `/register/action` is included in the Contributor and Owner roles.
  The page does not state the scope that permission is needed at, which is why
  step 3 carries a flag. It also states that ARM template and Bicep deployments
  auto-register the providers they declare, which says nothing about Terraform.

Carried from [[dbr-RG-to-working-non-admin-user]], verified there on 2026-08-10:

- [Workspace entitlements and the 15 June 2026 system group change](https://learn.microsoft.com/en-us/azure/databricks/security/auth/entitlements),
  used at step 9.

> [!todo] ✅ Every step now carries a source
> Steps 11, 20a, 20b, 21, 22 and 23 came off the unsourced list on 2026-08-12.
> What remains before status leaves Draft is the empty fields, not the sourcing:
> `The play` and `Check` are still `🔲` on steps 5, 7, 9, 10, 11, 12, 13, 14, 15,
> 17, 18, 19, 20a, 20b, 21, 22 and 23.

<!--
Version: 2.0 | Last Updated: 2026-08-12 | Status: Draft
-->
