# Network flow matrix workshop — prep document

Solution: Azure Databricks (classic and/or serverless, TBD) + Lakebase.
Landing zone: SharePoint (temporary ingestion bridge, per locked design doc).
Tenant: existing Azure tenant, Entra ID / SSO in place.

Deliverable: ingress/egress network flow matrix, current-state or target-state (confirm with sponsor).

---

## 1. Inputs

### 1.1 Pre-work (collect before workshop)

| # | Item | Owner | Status |
| :-- | :-- | :-- | :-- |
| 1 | SharePoint→Databricks ingestion mechanism | You / data engineering lead | Resolved — see 1.4 |
| 2 | IP space / IPAM allocation for Databricks subnets | Landing Zone / network team | 🔲 To be defined |
| 3 | Azure Firewall / hub egress policy (existing FQDN allowlists, NVA routing) | Landing Zone / network team | 🔲 To be defined |
| 4 | Lakebase feature scope (Data API only vs direct Postgres client access) | Data engineering lead | 🔲 To be defined |

### 1.2 Live inputs (presented at workshop open)

- Tenant/Entra SSO context, existing hub-spoke topology diagram — owner: you.

### 1.3 Locked ingestion design (SharePoint → bronze)

Source: `2026-06-24-sharepoint-to-bronze-ingestion-lock-in.md` (v1.3, Draft).

- Path: external extractor (non-Databricks, already running) → writes JSON to SharePoint document library → Databricks reads via **standard SharePoint connector** through a **Unity Catalog connection** (Beta, DBR 17.3 LTS floor).
- Trigger: **scheduled poll**, 2–3 runs/day, `Trigger.availableNow`. No event path — SharePoint emits no storage events, so no Event Grid, no file-arrival trigger, no notification queue.
- Auth: OAuth M2M, service principal via Entra app registration, scoped `Sites.Selected` or `Sites.Read.All`.
- Temporary: this bridges to a future ADLS Gen2 external location (no connector, native file-arrival trigger). Matrix should carry both states.

### 1.4 Flow rows — SharePoint ingestion

| Flow ID | Source | Destination | Protocol | Direction | Trigger | Auth | Status |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| SP-01 | Extractor (external) | SharePoint document library | HTTPS (M365) | Inbound to M365 | Continuous/cron, extractor-owned | Extractor's own SharePoint write identity | Current |
| SP-02 | Databricks (Auto Loader, UC connection) | SharePoint document library | HTTPS, Graph-backed connector | Outbound from Databricks | Scheduled poll, 2–3×/day | OAuth M2M, Entra app SP, Sites.Selected/Sites.Read.All | Current — Beta, temporary |
| SP-03 (future) | Databricks (external location) | ADLS Gen2 | Private endpoint / ABFSS | Outbound | Native file-arrival | Managed identity / storage RBAC | Target state, not yet built |

### 1.5 Egress path and allowlist for SP-02 — resolution status

- **No official Databricks doc states a specific FQDN/egress requirement for the SharePoint connector.** The connector page (Ingest files from SharePoint, MS Learn, updated 2026-06-09) covers connection setup, OAuth scopes, path types, limitations — no networking section.
- General Azure Databricks egress guidance (NAT Gateway / Azure Firewall for classic, NCC/network policy for serverless) is generic, not SharePoint-specific.
- Authoritative source for the underlying M365 destination: **Microsoft 365 IP/URL web service**, `ServiceAreas=SharePoint` — a live API, not a static list, updated monthly with 30-day advance notice for new entries. (https://learn.microsoft.com/en-us/microsoft-365/enterprise/microsoft-365-ip-web-service)
- Starting pattern to test: `<tenant>.sharepoint.com` wildcard, port 443. Whether the connector also calls a Graph API domain (e.g. `graph.microsoft.com`) directly is not documented.

> **That link is your own architecture decision to document, not something Microsoft has pre-answered.** No Databricks doc cross-references the M365 endpoint feed for this connector — resolving SP-02's exact destination set is on you and the network team, not resolvable from documentation alone.

**Action, not a workshop-day decision:**
1. Deploy connector in test workspace with egress open, capture actual destinations via `system.access.outbound_network`.
2. Cross-check captured FQDNs against the M365 SharePoint service-area feed.
3. Lock Firewall/NCC rule only after empirical capture — do not allowlist blind.
4. Treat the allowlist as a monthly-poll dependency, not a static entry (Microsoft's own warning: missed updates can cause outages).

> 🔲 To be defined — Graph API domain confirmation for SP-02, owner: you + network team.

### 1.6 Lakebase — flow rows (pending 1.1 #4 confirmation)

| Flow ID | Source | Destination | Protocol/Port | Auth | Control point | Notes |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| LB-01 | External Postgres client (psql/ORM/BI tool) | Lakebase endpoint (regional conn string) | TCP 5432 | OAuth token or Postgres password | Service Direct Private Link (NCC, preview) | Only if client is outside workspace |
| LB-02 | Lakebase Data API caller | Workspace front-end (`databricks_ui_api`) | HTTPS 443 | OAuth/Entra via workspace SSO | Standard inbound Private Link | No 5432 needed |
| LB-03 | Databricks Apps / Feature Store (in-workspace) | Lakebase | Internal | Workspace identity | None — stays in workspace network | No extra endpoint |
| LB-04 | Client (no Private Link / public access) | Lakebase Autoscaling public IPs | TCP 5432 | OAuth/password | Client-side firewall allowlist | Only if Private Link not enforced |

> ⚠️ Unverified — Lakebase Private Link / NCC support is Public Preview and preview-gated in the account console; re-check before workshop.

---

## 2. Decisions to make

| # | Topic | Owner (drives) | Contributors |
| :-- | :-- | :-- | :-- |
| 1 | Compute mode: classic (VNet-injected) vs serverless vs mixed, given Lakebase constraint | Databricks platform owner + Landing Zone (LZ has IP veto) | Security, FinOps |
| 2 | Egress control model: Azure Firewall/NAT GW (classic) vs NCC (serverless), or both | Security/compliance | Network team |
| 3 | Private Link scope: enforce private-only, or public with IP allowlist (per flow: workspace UI, Data API, Postgres 5432) | Security/compliance | Databricks platform owner |
| 4 | Current-state audit vs target-state design matrix | Sponsor | You |

Dependencies to weigh in decision 1:
- IP address space (classic needs 2 dedicated subnets, min /26, permanently reserved).
- On-prem/ExpressRoute reachability requirement (serverless NCC support for this is unverified — check before treating as settled).
- Egress control granularity (classic: full FQDN inspection via Firewall; serverless: NCC, coarser).
- Existing hub-spoke firewall policy and consistency with other workspaces in the tenant.
- Lakebase is serverless-first — mixed mode is likely regardless of main compute choice.

---

## 3. Draft matrix (Excel)

Columns:

```
Flow ID | Source | Destination | Protocol | Port | Direction | Purpose | Auth mechanism | Control point (NSG/FW/NCC/PE) | Data classification | Status (current/target)
```

Populate from sections 1.4 and 1.6 once decisions in section 2 are locked. Build after Topic 2 closes, not before — compute mode and egress model determine which control-point column values are even valid.

---

## 4. Sign-off (post-draft)

| # | Topic | Owner |
| :-- | :-- | :-- |
| 1 | Review draft matrix against actual firewall rules / NSG configs, correct discrepancies | Network team + Security, with you |

---

*Status: Draft. Prepared ahead of workshop — not for distribution outside the working group without review.*
