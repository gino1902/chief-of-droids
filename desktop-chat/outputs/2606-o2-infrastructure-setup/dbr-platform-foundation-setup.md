# Databricks platform foundation setup

> One ordered sequence from a workspace a user can already reach to a governed
> bronze table landing from ADLS. Decisions are not taken here. They arrive as
> accepted ADRs, and each step names the one it consumes.
> Upstream: dbr-RG-to-working-non-admin-user.md, which ends where step 1 begins.

## What counts as done

Step 27 is the finish line: a service principal writes a file to ADLS, a file
event fires, Auto Loader lands a bronze table in a governed catalog, and a group
member reads it. Deployed from the repo, not from the UI.

> 🔲 To be defined — the two weaker finish lines that get mistaken for this one

## Preconditions

### Entry condition

Do not start step 1 until every ADR below is Accepted, except the two noted as
deferrable. This is the gate. It is stated once here rather than as a numbered
step, because each step also names the ADR it consumes.

### ADRs

Ordered by the first step that consumes them. The `Depends on` column carries the
order they must be accepted in, which is not the same order.

| ADR | Subject | First consumed | Also consumed by | Depends on |
| :--- | :--- | :--- | :--- | :--- |
| 🔲 | Non-human identity model | 4 | 16 | — |
| 🔲 | Deployment model | 5 | — | — |
| 🔲 | Access Connector and external location granularity | 6 | 7, 8 | Catalog and schema model, Metastore root storage |
| 🔲 | Catalog and schema model | 8 | 13, 14 | Workspace topology |
| 🔲 | File event mechanism | 9 | — | Access Connector granularity |
| 🔲 | Secret scope model | 10 | — | — |
| 🔲 | Workspace topology | 11 | 17, 22 | — |
| 🔲 | Ownership and grant model | 11 | 12, 15, 16 | Workspace topology, Catalog and schema model |
| 🔲 | Metastore root storage and MANAGED LOCATION policy | 13 | — | Workspace topology |
| 🔲 | Serverless or classic posture | 19 | 21 | — |
| 🔲 | Tagging and budget route | 19 | 20 | Serverless or classic posture |
| 🔲 | Legacy surface posture | 23 | — | — |
| 🔲 | Data protection model | 24 | — | Catalog and schema model |
| 🔲 | Network posture | 25 | — | Serverless or classic posture |

Acceptance order, derived from the `Depends on` column: workspace topology first,
then metastore root storage and the catalog and schema model, then Access
Connector granularity and the ownership and grant model, then the rest in any
order.

> Deferrable. Steps 24 and 25 consume ADRs owned outside this team. Those two may
> stay Proposed while steps 1 to 23 run, provided nothing sensitive lands before
> step 24.

### Identities

| Role | Needed for | Held by |
| :--- | :--- | :--- |
| Account admin | 🔲 | 🔲 |
| Workspace admin | 🔲 | 🔲 |
| Platform engineer | 🔲 | 🔲 |
| Entra admin | 🔲 | 🔲 |
| Network team | 🔲 | 🔲 |
| Test user | 🔲 | 🔲 |

### Environment checks

> 🔲 To be defined — what steps 1 to 3 assume about the tenant and subscription

## How to read a step

Each step carries the same five fields.

- **Category** — gate, foundation, compute, admin, protection, acceptance
- **Owner, prerequisite, impact** — one line, machine-readable
- **Why it matters** — what this step is for and what breaks without it. Not why
  the option was chosen. That is in the ADR
- **What getting the execution wrong costs** — irreversible, lossy, rework in
  days, or adjustable
- **The play** — the commands or clicks
- **Check** — what passes or fails

Impact values: `Irreversible`, `Lossy`, `Rework Nd`, `Adjustable`.

## Scope

Deliberately not here:

> 🔲 To be defined

---

### 1. Read metastore root storage state

`Category: gate` · `Owner: account admin` · `Prerequisite: none` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 2. Confirm serverless availability and enablement in region

`Category: gate` · `Owner: account admin` · `Prerequisite: none` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 3. Inventory Azure Policy, network standards, existing Entra groups

`Category: gate` · `Owner: platform engineer` · `Prerequisite: none` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 4. Create the CI/CD and Claude Code service principals

`Category: foundation` · `Owner: account admin` · `Prerequisite: ADR non-human identity model` · `Impact: Lossy`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 5. Bootstrap the IaC repo and wire the CI principal

`Category: admin` · `Owner: platform engineer` · `Prerequisite: ADR deployment model` · `Impact: Rework 15d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 6. Create the Access Connector and assign ADLS roles

`Category: foundation` · `Owner: platform engineer` · `Prerequisite: ADR Access Connector granularity` · `Impact: Rework 3d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 7. Register the storage credential

`Category: foundation` · `Owner: account admin` · `Prerequisite: ADR Access Connector granularity` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 8. Register external locations

`Category: foundation` · `Owner: account admin` · `Prerequisite: ADR catalog and schema model, ADR Access Connector granularity` · `Impact: Rework 3d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 9. Register the Event Grid provider and grant queue roles

`Category: foundation` · `Owner: platform engineer` · `Prerequisite: ADR file event mechanism` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 10. Create secret scopes and scope ACLs

`Category: foundation` · `Owner: workspace admin` · `Prerequisite: ADR secret scope model` · `Impact: Rework 2d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 11. Create account groups, including the metastore admin group

`Category: foundation` · `Owner: Entra admin` · `Prerequisite: ADR workspace topology, ADR ownership and grant model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 12. Set the metastore admin to the group

`Category: foundation` · `Owner: account admin` · `Prerequisite: ADR ownership and grant model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 13. Create catalogs with explicit MANAGED LOCATION

`Category: foundation` · `Owner: account admin` · `Prerequisite: ADR metastore root storage, ADR catalog and schema model` · `Impact: Irreversible`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 14. Create schemas

`Category: foundation` · `Owner: account admin` · `Prerequisite: ADR catalog and schema model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 15. Apply catalog-level grants

`Category: foundation` · `Owner: account admin` · `Prerequisite: ADR ownership and grant model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 16. Grant the service principals their catalog access

`Category: foundation` · `Owner: account admin` · `Prerequisite: ADR ownership and grant model, ADR non-human identity model` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 17. Apply catalog to workspace bindings

`Category: foundation` · `Owner: account admin` · `Prerequisite: ADR workspace topology` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 18. Enable the system table schemas

`Category: foundation` · `Owner: account admin` · `Prerequisite: none` · `Impact: Lossy`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 19. Create compute policies with enforced tags

`Category: compute` · `Owner: workspace admin` · `Prerequisite: ADR serverless or classic posture, ADR tagging and budget route` · `Impact: Rework 5d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 20. Create the serverless budget policy

`Category: compute` · `Owner: account admin` · `Prerequisite: ADR tagging and budget route` · `Impact: Lossy`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 21. Create SQL warehouses and set permissions

`Category: compute` · `Owner: workspace admin` · `Prerequisite: ADR serverless or classic posture` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 22. Assign entitlements to each group

`Category: admin` · `Owner: account admin` · `Prerequisite: ADR workspace topology` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 23. Apply admin settings

`Category: admin` · `Owner: workspace admin` · `Prerequisite: ADR legacy surface posture` · `Impact: Rework 10d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 24. Apply classification tags, column masks, row filters

`Category: protection` · `Owner: account admin` · `Prerequisite: ADR data protection model` · `Impact: Rework 8d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 25. Apply the network posture

`Category: protection` · `Owner: network team` · `Prerequisite: ADR network posture` · `Impact: Rework 4d`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 26. Configure monitoring and alerting

`Category: protection` · `Owner: platform engineer` · `Prerequisite: none` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

### 27. Acceptance test

`Category: acceptance` · `Owner: test user` · `Prerequisite: none` · `Impact: Adjustable`

**Why it matters** 🔲

**What getting the execution wrong costs** 🔲

**The play** 🔲

**Check** 🔲

---

## When it fails at step 27

| What you see | Where it actually broke |
| :--- | :--- |
| 🔲 | 🔲 |

## Sources

> 🔲 To be defined — verify per claim before status leaves Draft

<!--
Version: 0.3 | Last Updated: 2026-08-11 | Status: Skeleton
-->
