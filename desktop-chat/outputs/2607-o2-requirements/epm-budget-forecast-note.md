# EPM budget and forecast, note for a future use case

Working note, not a use case and not a draft of one. This is raw input to build the EPM actual-vs-forecast use case later, once the use-case eligibility framework exists (to be defined in a separate session). It does not follow that framework yet, and its structure is provisional.

> ⚠️ Unverified — "EPM Workday" is assumed to mean Workday Adaptive Planning. Confirm the product before circulating.

## One line

O2 gives finance and operations one trusted view of actual against forecast against budget, broken down by the company analytic axes, and it produces the operational driver figures that ground the next EPM budget and reforecast.

## Where it sits

This is the Budget-to-Report (B2R) flagship named in [FRAMING.md](FRAMING.md), the budget-to-report path that today breaks at the handovers. In the process taxonomy it covers budgeting-and-target-setting, forecasting-and-reforecasting and management-reporting-and-analysis. Per ADR-001 it is a gold use case built on a shared conformed silver, not a direct read from each producer.

The company runs its budgeting and forecasting in EPM. O2 does not replace that. O2 is the trusted-data layer around it: it conforms the actuals EPM cannot see cleanly, and it exposes the result through an agentic workflow.

## The workflow, two directions

Direction 1, consume. O2 ingests the EPM plan figures and the operational actuals, conforms both to the analytic axes in silver, and builds a gold model of actual against forecast against budget by axis and period. An agent exposes variance and its drivers to finance and operations without either team chasing figures across tools.

Direction 2, feed drivers. O2 derives the trusted driver actuals (headcount, utilisation, average day rate, cost per head, attrition, bench) in gold and exposes them so finance grounds the next EPM budget and reforecast on realised operational figures rather than manual spreadsheet inputs.

> ⚠️ Boundary constraint — ADR-010 sets the middleware-to-O2 flow as one-way inbound, and teams consume O2 as gold through agents rather than writing back into the SaaS. So O2 does not push figures into EPM. The driver hand-back is analyst-carried, or a separate IT-owned integration outside this boundary. Keep Direction 2 scoped to producing and exposing the drivers, not to writing them into EPM.

## Data required

Four groups. Groups A and C already land today. Group B is the main new feed this use case needs. Group D is derived inside O2.

### Group A, analytic dimensions (from EPM, already landing)

The six `analytic_*` files are the analytic axes themselves, not figures. They become the conformed dimensions in silver and the shared axes every B2R figure hangs off.

| File | Axis |
|------|------|
| `analytic_bu.json` | Business unit |
| `analytic_department.json` | Department |
| `analytic_entity.json` | Management entity |
| `analytic_service_line.json` | Service line |
| `analytic_site.json` | Site or location |
| `analytic_society.json` | Legal company (société) |

### Group B, EPM plan figures (required, not yet landing)

> ⚠️ Not in the current [data-sources inventory](o2-data-sources.md). Only the dimension files land today. This is a new canonical SQLI contract to define with EPM, per the demand-driven rule in ADR-010.

Planned financial figures by period and axis, with a scenario tag so budget, forecast, reforecast and any EPM-side actual are distinguishable.

| Attribute | Requirement |
|-----------|-------------|
| Grain | Monthly, per analytic axis combination, per account or nature line |
| Measures | Revenue, direct cost, margin, headcount FTE at minimum |
| Scenario | Budget, forecast, reforecast, tagged and versioned |
| Assumptions | Planned headcount, utilisation, day rate, cost per head if EPM exposes them |
| Producer | EPM |
| Cadence | Monthly plan and reforecast cycle |

### Group C, operational actuals (existing feeds)

The realised figures O2 already receives, mapped to the drivers they support.

| Actual | Source file | Producer |
|--------|-------------|----------|
| Revenue, project margin | `project_financial_report`, `project_ca_collab_report` | APP |
| Billable and worked days, utilisation | `cra_worklog`, `cra_bilan_cra_report` | APP (and Jira?) |
| Headcount and workers | `perso_workers` | ADP (APP if not FR) |
| Leave and net capacity | `perso_leave_report` | ADP |
| Bench and availability | `perso_collab_status_report` | Whoz |
| Skills and certifications for rate mix | `whoz__skill_report`, `whoz__certification_report`, `whoz__accreditation_report`, `whoz__talent_report`, `whoz__profile_report` | Whoz |

### Group D, driver actuals (derived in O2, the feed-back set)

Built in gold from Group C against the Group A axes. These are the grounded assumptions finance carries into the next EPM cycle.

| Driver | Definition | Built from |
|--------|------------|------------|
| Headcount FTE by axis | Active workers net of leave | `perso_workers`, `perso_leave_report` |
| Utilisation | Billable days over available days | `cra_worklog` against workers and leave |
| Average day rate | Revenue over billable days | `project_financial_report`, `cra_worklog` |
| Loaded cost per head | Direct cost over headcount | project financials, `perso_workers` |
| Attrition | Leavers over headcount, period on period | `perso_workers` over time |
| Bench rate | Available not staffed over headcount | `perso_collab_status_report`, `cra_worklog` |

## Gaps and open actions

- EPM plan figures (Group B) are the blocking dependency. Only the dimension files land today, so the budget and forecast lines have no feed yet. The APP to EPM data exchange has already been mapped, so the remaining work is to define the canonical contract for the plan figures with EPM, not to discover the exchange.
- Forward revenue drivers (sales pipeline, weighted bookings, backlog) have no feed. They sit in Opportunity-to-Contract or the CRM and are absent from the inventory. Needed for the forecast, less so for the budget.
- Write-back to EPM stays out of scope under ADR-010. Confirm who carries the driver figures into EPM and how.

## Success measures

- Cycle time, budget-to-report, from orchestrator workflow timestamps, per FRAMING.
- Forecast accuracy, absolute actual minus forecast over actual, by axis, tracked each cycle.
- Variance explained, the share of variance lines with an attributed driver.
- Manual effort removed, spreadsheet reconciliation steps taken out of the cycle.

<!--
Version: 1.2 | Last Updated: 2026-07-23 | Status: Note
-->
