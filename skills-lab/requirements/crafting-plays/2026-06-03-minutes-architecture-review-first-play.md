# Architecture review minutes, transition ingestion 2

| Date | Attendees | Reviewed |
| :--- | :--- | :--- |
| 2026-06-03 | Architecture team | First ingestion scenario, SharePoint to Databricks bronze |

## Decisions

- The landing moves from SharePoint to an Azure storage container, because of SharePoint load and cryptography limits.
- Cryptographic keys are held in a Vault (Azure Key Vault).
- Extraction is refactored to one script per SaaS.
- FinOps is owned by IT.

## Requirement

- Cold encryption at rest is an RGPD requirement for the landing zone, with customer-managed keys in the Vault.

## Actions

| Action | Owner | Status |
| :--- | :--- | :--- |
| Build the martrecruiter extraction | To be assigned | To do |
| Move extraction to one script per SaaS | To be assigned | To do |
| Provision the Azure container and the Key Vault | IT (to confirm) | To do, neither exists yet |

*Version 1.1, Draft, 2026-06-03. Relates to 2026-06-02-json-sharpoint-to-bronze-ingestion-play.md.*
