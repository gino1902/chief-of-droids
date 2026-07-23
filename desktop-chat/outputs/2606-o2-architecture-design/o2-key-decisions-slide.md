---
marp: true
size: 16:9
paginate: false
---

# O2 platform — 7 key architecture decisions

| Decision | What it means |
|:---------|:--------------|
| Bronze per producer | Raw, source-aligned data, one bundle per producer, minimal validation, consumed only by silver not analysts. |
| Silver conforming layer | Single shared layer where cross-source cleaning, joins and conformed definitions happen once, preventing divergence structurally. |
| Gold per use case | Aggregations and dimensional models built only from silver, one boundary per business use case. |
| SharePoint ingestion | Standard connector drains SharePoint to bronze as whole-record VARIANT, a disposable bridge until ADLS migration. |
| One-way inbound | Data flows inbound only, O2 holds the truth and teams cannot write back into any SaaS for now. |
| Canonical data contracts | Middleware lands SQLI-defined canonical contracts, tool-independent, so any SaaS can be swapped without reworking downstream. |
| Compliance by design | Personal data filtered, encrypted and anonymised at the middleware before landing, each side conformance-tested. |

<!--
Version: 1.0 | Last Updated: 2026-07-23 | Status: Draft
-->
