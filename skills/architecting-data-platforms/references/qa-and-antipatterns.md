# Anti-Patterns and QA Checklist

Read this file when reviewing or producing any data platform architecture output.

---

## Anti-Patterns (Senior Radar)

| Anti-pattern | Signal | Correct approach |
| :--- | :--- | :--- |
| All-purpose clusters in production | High compute spend, shared contention | Job clusters per workload |
| Mount points in any workspace | `/mnt/` paths in notebooks or jobs | Migrate to External Locations |
| Features computed in training notebooks | Train/serve skew; no reuse | Databricks Feature Store |
| Single storage account for all environments | Prod data accessible from dev | One account per environment |
| Schema-on-read without contracts | Silent downstream breakage | Data contracts at Silver → Gold |
| MLflow experiments per user | Lost history, no governance | Use-case-scoped naming convention |
| Promoting models without champion/challenger | Undetected regressions in production | Shadow mode + staged promotion |
| HNS not confirmed at account creation | Loss of ADLS Gen2 capabilities | Verify HNS status before provisioning |
| Security design after provisioning | Security retrofitted, not designed | Phase 5 before any infrastructure |

---

## QA Checklist

- [ ] Paradigm recommendation states org maturity and team size assumptions
- [ ] Build vs buy assessed on all four axes
- [ ] Version-sensitive claims fetched from official sources — not from memory or skill content
- [ ] Azure resource terminology correct (storage account, container — not "bucket")
- [ ] Unity Catalog vs legacy HMS distinction explicit where relevant
- [ ] Mount points flagged as deprecated platform-wide
- [ ] MLflow registry promotion policy stated as a governance decision
- [ ] Storage access method follows priority order (Managed Identity > SP > SAS > Key)
- [ ] Cost governance levers addressed for compute and storage recommendations
- [ ] Governance maturity level stated before recommending tooling
- [ ] Source freshness checked — flag anything older than 12 months
