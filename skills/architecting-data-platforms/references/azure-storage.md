# Azure Cloud Storage Reference
<!-- version: 1.1 | last_updated: 2026-03-23 -->

All version-sensitive claims in this file must be verified against official sources
before use. Access tier thresholds, replication options, HNS constraints, and
pricing are subject to change.

Official sources:
- `learn.microsoft.com/azure/storage`
- `learn.microsoft.com/azure/storage/blobs/access-tiers-overview`
- `learn.microsoft.com/azure/role-based-access-control`
- `learn.microsoft.com/azure/active-directory/managed-identities-azure-resources`

---

## Storage Account Design

**Decision rules (stable — no fetch required):**

- One storage account per environment (dev / staging / prod) — never share across environments; prod data must not be accessible from dev context
- Metastore root storage account is dedicated — do not co-locate application data in the same account
- HNS (Hierarchical Namespace) is required for ADLS Gen2 — verify whether it can be enabled post-creation for current Azure offering before advising; at time of last verification, HNS could not be enabled after account creation
- Production RPO/RTO requirements determine replication tier — confirm with the security design from Phase 5

⚠️ Fetch from `learn.microsoft.com/azure/storage` before advising on:
- Current replication options (LRS / ZRS / GRS / GZRS) and regional availability
- HNS enablement constraints
- Storage account SKU options

---

## Access Tier Strategy

⚠️ Fetch from `learn.microsoft.com/azure/storage/blobs/access-tiers-overview`
before advising on minimum retention periods, retrieval costs, or early deletion
penalties — these are pricing details subject to change.

**Decision rules that do not require a fetch:**

- Never put active Delta tables on Cool or Cold tiers — random file access patterns caused by Delta's transaction log make retrieval costs unpredictable
- Automate tier transitions via Azure Blob Lifecycle Management — never manage tier assignments manually at scale
- Early deletion penalties apply when blobs are moved or deleted before the tier's minimum retention period — size lifecycle policies to avoid unintended charges
- Archive tier requires rehydration before access — confirm acceptable latency with consumers before routing any data to Archive

---

## Identity & Access — Priority Order

Stable architectural principle — does not require a fetch:

1. **Managed Identity + Unity Catalog External Location** — preferred; no secrets, no credential rotation, auditable, UC-governed
2. **Service Principal + OAuth (client credentials)** — for non-UC or cross-tenant scenarios; requires secret rotation policy
3. **SAS Token** — scoped, time-limited; acceptable for external partner access only; define expiry and scope at generation time
4. **Storage Account Key** — never use in production; grants full account access with no audit trail per operation

**Senior rule:** Any integration using SP or SAS must have a defined secret rotation
policy before go-live. "We'll handle it later" is not a policy.

---

## Secrets Management — Azure Key Vault

Use Azure Key Vault as the single secrets store for all credentials that cannot use
Managed Identity — Service Principal client secrets, SAS tokens, and any third-party
API keys used in pipelines.

⚠️ Fetch from `learn.microsoft.com/azure/key-vault` before advising on Key Vault
pricing tiers, soft-delete retention periods, or purge protection behaviour — these
are subject to change.

**Decision rules (stable — no fetch required):**

- Back Databricks Secret Scopes with Azure Key Vault — never store secrets in Databricks-native secret scopes for production workloads; Key Vault provides audit logging, rotation, and access policy enforcement that native scopes do not
- Managed Identity is the correct access method for Databricks to read from Key Vault — do not use Key Vault access policies with Service Principals if Managed Identity is available
- Rotate Service Principal client secrets on a defined schedule — define the rotation cadence and owner at Phase 5 (Security); never leave rotation as an undated future task
- SAS token expiry must be set at generation time — never generate non-expiring SAS tokens
- Key Vault must be provisioned and access policies confirmed before any pipeline that requires credentials goes to production — do not use placeholder secrets and "replace later"

**Senior rule:** A secret that is not in Key Vault is a secret that cannot be audited,
rotated centrally, or revoked instantly. If it is in a notebook, a config file, or
an environment variable, it is exposed.

---

## Mount Points — Deprecated

⚠️ DBFS mounts are deprecated platform-wide. New Databricks accounts are
provisioned without access to this feature. Migrate all existing mounts to
External Locations. Do not introduce new mount points under any circumstances.

Migration path:
1. Identify all active `/mnt/` references in notebooks and jobs
2. Create corresponding External Locations in Unity Catalog with Managed Identity
3. Update path references to `abfss://` URIs
4. Validate access via Unity Catalog privilege grants
5. Remove mount definitions

**Senior rule:** Do not schedule mount migration as a later phase — it blocks Unity
Catalog adoption and leaves the workspace in a split governance state.

---

## Network Design

⚠️ Fetch from `docs.databricks.com` before advising on VNet injection configuration,
private endpoint setup, or IP allowlisting — workspace network topology options vary
by Azure region and Databricks plan tier.

**Decision rules that do not require a fetch:**

- Production workspaces must use private endpoints or VNet injection — public endpoint access is not acceptable for data containing PII or regulated data
- Network topology must be approved as part of Phase 5 (Security) — not retrofitted post-provisioning
- IP allowlisting alone is not a substitute for private networking — flag this if proposed
