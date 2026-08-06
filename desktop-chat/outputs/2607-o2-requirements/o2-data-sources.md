# O2 data sources

Feed configuration: one row per declared feed, filenames as patterns rather than dated instances. `subdomain` is a foreign key to [domain-taxonomy](domain-taxonomy.md).

`status` semantics: **active** = lands and is ingested. **inactive** = lands and is not ingested. **planned** = does not land yet.

> ⚠️ Generated from `o2-data-sources.xlsx`, which is the source of truth and is **not tracked by git** (root `.gitignore` ignores `*.xlsx`). Edit the workbook, then regenerate with `xlsx_to_md.py`.

| filename | status | subdomain | cadence | producer | source | source path | access-protocol |
|---|---|---|---|---|---|---|---|
| AAAA-MM-DD__analytic_bu.json | inactive | hr-administration | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/analytic/bu/ | HTTPS |
| AAAA-MM-DD__analytic_department.json | active | hr-administration | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/analytic/department/ | HTTPS |
| AAAA-MM-DD__analytic_entity.json | inactive | hr-administration | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/analytic/entity/ | HTTPS |
| AAAA-MM-DD__analytic_service_line.json | active | hr-administration | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/analytic/service_line/ | HTTPS |
| AAAA-MM-DD__analytic_site.json | active | hr-administration | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/analytic/site/ | HTTPS |
| AAAA-MM-DD__analytic_society.json | active | hr-administration | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/analytic/society/ | HTTPS |
| AAAA-MM-DD__cra_bilan_cra_report.json | active | project-resources | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/cra/bilan_cra_report/ | HTTPS |
| AAAA-MM-DD__cra_worklog.json | active | project-resources | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/cra/worklog/ | HTTPS |
| AAAA-MM-DD__others_whoz__accreditation_report.json | active | hr-talents | daily | Whoz | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/others/ | HTTPS |
| AAAA-MM-DD__others_whoz__certification_report.json | active | hr-talents | daily | Whoz | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/others/whoz__certification_report/ | HTTPS |
| AAAA-MM-DD__others_whoz__profile_report.json | active | hr-talents | daily | Whoz | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/others/whoz__profile_report/ | HTTPS |
| AAAA-MM-DD__others_whoz__skill_report.json | active | hr-talents | daily | Whoz | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/others/whoz__skill_report/ | HTTPS |
| AAAA-MM-DD__others_whoz__talent_report.json | active | hr-talents | daily | Whoz | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/others/whoz__talent_report/ | HTTPS |
| AAAA-MM-DD__others_whoz__user_report.json | active | hr-talents | daily | Whoz | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/others/whoz__user_report/ | HTTPS |
| AAAA-MM-DD__perso_collab_status_report.json | active | hr-administration | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/perso/collab_status_report/ | HTTPS |
| AAAA-MM-DD__perso_leave_report.json | active | hr-administration | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/perso/leave_report/ | HTTPS |
| AAAA-MM-DD__perso_workers.json | active | hr-administration | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/perso/workers/ | HTTPS |
| TBD | planned | hr-recruitment | TBD | SmartRecruiters | TBD | TBD | TBD |
| AAAA-MM-DD__project_ca_collab_report.json | active | finance-fa&c | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/project/ca_collab_report/ | HTTPS |
| AAAA-MM-DD__project_financial_report.json | active | finance-fa&c | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/project/financial_report/ | HTTPS |
| AAAA-MM-DD__project_project_dataware_report.json | active | project-master | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/project/project_dataware_report/ | HTTPS |
| AAAA-MM-DD__project_projects_report.json | active | project-master | daily | APP | APP | https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/project/projects_report/ | HTTPS |
| TBD | planned | project-control | TBD | TBD | TBD | TBD | TBD |
| TBD | planned | finance-operations | TBD | TBD | TBD | TBD | TBD |
| TBD | planned | project-delivery | TBD | TBD | TBD | TBD | TBD |
| TBD | planned | finance-planning | TBD | EPM | EPM | TBD | TBD |
| TBD | planned | finance-treasury | TBD | TBD | TBD | TBD | TBD |
| TBD | planned | finance-suppliers | TBD | TBD | TBD | TBD | TBD |
| TBD | planned | sales-clients | TBD | CRM | CRM | TBD | TBD |
| TBD | planned | sales-opportunities | TBD | CRM | CRM | TBD | TBD |
| TBD | planned | sales-commercials | TBD | Sharepoint | Sharepoint | TBD | TBD |
| TBD | planned | sales-contracts | TBD | Tomoro | Tomoro | TBD | TBD |
| TBD | planned | it-users | TBD | APP | APP | TBD | TBD |

<!--
Version: GENERATED | Last Updated: 2026-08-06 | Status: Draft
Generated by xlsx_to_md.py from o2-data-sources.xlsx. Do not hand-edit.
-->
