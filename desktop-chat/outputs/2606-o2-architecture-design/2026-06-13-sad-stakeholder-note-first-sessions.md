# Solution architecture and procurement onboarding, first-sessions stakeholder note, minutes

| Date | Attendees | Reviewed |
| :--- | :--- | :--- |
| 2026-06-13 (edit) | CISO, IS/IT, Infra, Legal, Procurement | Landing Zone decision and open actions from the first round of sessions |

## Decision

- Landing Zone stays on SharePoint (option B), not the target blob-storage pattern, because the go-live date must be secured and there is no dev capacity for the API rework a move would force. The change stays limited to an API addition, but the SharePoint retention strategy (30 days) must be reviewed against the storage limit.

## Actions

Owners are inferred from what each item is, not labelled in the source. Three rows carry a confirm flag in the Owner column where ownership is unclear. IDs are stable, so they do not change when rows or blocks are reordered.

### Procurement onboarding

| ID | Owner | Action | Status |
| :--- | :--- | :--- | :---: |
| A01 | CISO / Security | Databricks security assessment: data at rest, data in transit, data processing and handling, IAM, security certifications and assurance, risk assessment, GRC | To do |
| A10 | Legal / Data protection | Record of personal data processing activities | To do |
| A12 | Procurement | Vendor onboarding process | To do |

### Solution architecture

| ID | Owner | Action | Status |
| :--- | :--- | :--- | :---: |
| A02 | CISO / Security | Access log management | To do |
| A03 | CISO / Security | Certificate and secrets management: strategy, access rights, renewal rules | To do |
| A06 | IS/IT | Validate data flows required for O2 ingestion | To do |
| A07 | IS/IT 🔲 confirm: IS/IT or Architecture | Identify data exchanged between APP and EPM, APP and Unit4, Unit4 and OpenERP | To do |
| A08 | Infra 🔲 confirm: Infra or CISO | Risk analysis: VM cron sizing to guarantee the SQLI extractor service (RTO, RPO, other) | To do |
| A09 | Infra 🔲 confirm: Infra or IS/IT | Network flow diagram | To do |
| A11 | Legal / Data protection | Review SharePoint retention policy with Mathieu (30-day consequence of the Landing Zone decision) | To do |
| A13 | Architecture (data architect) | Finish identifying and building future data flows from HRIS | To do |
| A14 | Architecture (data architect) | Data flow diagram | To do |
| A15 | Architecture (data architect) | Design target data exposition flows: from Landing Zone, from Databricks | To do |

Source: first-round sessions with CISO, IS/IT, Infra, Legal, Procurement. Relates to the Solution Architecture Document (in progress).

<!--
Version: 1.9 | Last Updated: 2026-06-13 | Status: Draft
-->
