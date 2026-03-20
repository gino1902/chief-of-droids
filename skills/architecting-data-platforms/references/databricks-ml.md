# Databricks — ML Engineering Reference

All version-sensitive claims in this file must be verified against official sources
before use. Do not treat this file as authoritative for API signatures, registry
behaviour, or feature availability by runtime.

Official sources:
- `mlflow.org/docs/latest`
- `docs.databricks.com` (Feature Store, Model Serving, AutoML)
- `docs.databricks.com/release-notes` (Prophet and package availability by runtime)
- `facebook.github.io/prophet/docs`

---

## MLflow Lifecycle

⚠️ Fetch from `mlflow.org/docs/latest` before advising on:

- `log_model` / `log_artifact` signatures — parameter names change across versions
- Model registry stage names and transition APIs
- Experiment and run APIs
- Autologging behaviour per framework

**Decision rules that do not require a fetch:**

- Experiment naming must be tied to use case and team — not individual users; enforce via naming convention in cluster policy or MLflow project config
- Registry promotion policy (who approves stage transitions) must be defined before any model reaches production — this is a governance decision, not a technical one
- Model artifact retention must align with the organisation's data retention policy — define explicitly, do not rely on platform defaults
- Serving endpoint autoscaling and fallback behaviour must be defined at design time, not post-deployment

---

## Feature Store

⚠️ Fetch from `docs.databricks.com` before advising on Feature Store APIs, online
store configuration, or point-in-time lookup syntax — these have changed significantly
across platform versions.

**Decision rules that do not require a fetch:**

- Feature Store is warranted when: features are reused across models or teams; point-in-time correctness is required (forecasting, fraud, recommendations); feature lineage is an audit requirement
- Computing features inside training notebooks without registering them creates silent train/serve skew — always flag this as an anti-pattern
- Feature Store tables must be owned by the platform team, not individual model owners

---

## Prophet on Databricks

⚠️ Fetch from `docs.databricks.com/release-notes` before advising on Prophet
availability. Package inclusion varies by Databricks Runtime version. Fetch from
`mlflow.org/docs/latest` before writing any `mlflow.prophet` API calls — parameter
names have changed across releases.

**Decision rules that do not require a fetch:**

- Prophet input DataFrame requires columns `ds` (datetime) and `y` (float) — validate schema before fit
- Log Prophet models via MLflow integration, not as raw pickle artifacts — enables registry governance
- Seasonality mode (additive vs multiplicative) is a design decision, not a default — document rationale in the experiment run
- MAPE or equivalent accuracy metric must be logged alongside the model — never register a model without a tracked accuracy metric

---

## Model Drift & Retraining

**Decision rules (stable — no fetch required):**

- Drift detection trigger must be defined at design time: statistical threshold (PSI, KS test) or business KPI degradation — not left to the model owner post-deployment
- Retraining cadence must be documented: scheduled (time-based) vs triggered (drift-based) — both require a defined owner and approval step
- Champion/challenger pattern required before promoting any model to production — new model runs in shadow mode, challenger metrics compared to champion before cutover
- Rollback procedure must be defined: registry stage revert + endpoint redeploy — test the rollback path before go-live, not after an incident
