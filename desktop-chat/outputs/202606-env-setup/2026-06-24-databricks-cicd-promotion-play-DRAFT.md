# Promoting a Databricks platform from dev to prod with CI/CD

## Read first

This is a draft scaffold, not a finished play. The structure and the bundle facts are verified against official docs, but the promotion mechanics were never run, so the load-bearing parts are placeholders. A real first run fills them. Treat every `<!-- COLLECT -->` marker as a required input. The `✅` markers flag facts verified this session and get stripped at finalisation, leaving the Sources table as the record.

<!-- TO BE REMOVED before this play is considered complete:
The fastest way to fill it is to run the play once, in a sandbox, treating the run as a note-taking exercise. The First run section below says how. Open question for the author: file this scaffold to the outputs folder as a draft, or hold it inline until a run produces the content?
-->

## First run

<!-- TO BE REMOVED once the placeholders are filled. This section bootstraps the scaffold. It is not part of the reusable recipe. -->

Run the play once before trusting it. The goal of the first run is to fill the placeholders and confirm or drop the candidate pits, not to ship anything. Optimise for capturing notes.

Setup:

- Use the smallest workload, one notebook in one job. A real payload only adds noise. Swap it for a real one once the path is proven.
- Stand up three throwaway targets, not your real O2 environments. A first run will misconfigure something, and you do not want that against real prod or HR data.
- Register one service principal per target, minimal scope, OAuth secret in the CI secret store. This exercises step 7.
- Pick one CI platform and commit to it for the run. Azure DevOps fits an Entra-centric Azure shop. The choice fills the precondition in When to use it.
- Keep the sandbox targets in the EU region, so you do not learn a pattern that breaks residency on the real platform.

Run it twice. First lap without gates, to see the bundle move dev to test to prod. Second lap with the gates added, to prove the controls. Walk the ten workflow steps in order each lap, and write down what each `COLLECT` asks for as you go. Break one prod deploy on purpose to test rollback.

What the run fills:

| First-run action | Fills |
| :--- | :--- |
| Write the manual pain you are replacing, before you start | When to trigger, examples |
| Record the branch-to-target mapping and trigger events | Step 2, branch model tradeoff |
| Record the gate you put before test and prod | Steps 5 and 6, gate critical move |
| Record how config differed per target | Step 8, target-config tradeoff |
| Break and recover a prod deploy | Step 10, rollback, rollback pit |
| Log every misstep you hit | Pits to avoid |
| Record the version check that proved same-artefact promotion | Expected outcome |

## When to trigger

You have a Databricks platform with separate dev, test, and prod environments and you want changes to flow between them through an automated, gated pipeline rather than by hand. The signal is that promotion is manual today. Someone copies notebooks, recreates jobs, or edits config per environment, and you want a repeatable, auditable path instead.

Concrete examples:

<!-- COLLECT: at least one real instance, e.g. "a pipeline change tested in dev had to be hand-recreated in prod, and the configs drifted" -->
<!-- COLLECT: a second example showing the signal in a different shape -->

## Why it matters

Manual promotion across three environments drifts and cannot be audited. A change validated in dev is not guaranteed to be the change that lands in prod, and no record shows who promoted what. This play replaces hand promotion with a defined artefact, automated stages, and approval gates. The deliverable is a pipeline that builds once, validates in lower environments, and deploys the same artefact to prod under controlled identity.

## The play

### Optimal workflow

1. Choose the deployment artefact. ✅ The Databricks-native unit is **Declarative Automation Bundles** (DABs, formerly Databricks Asset Bundles), a YAML-defined project deployed as a single bundle to a target. <!-- COLLECT: DABs alone, or DABs for workloads plus Terraform for infra -->
2. Define the source control model. <!-- COLLECT: branch strategy, which branch maps to which target, what event starts the pipeline -->
3. Build and validate. ✅ Run `databricks bundle validate` on every PR to catch config errors. <!-- COLLECT: lint and unit tests, the runner, any wheel packaging -->
4. Deploy to the dev target in development mode. ✅ Development mode prefixes resources with `[dev <user>]`, pauses their schedules and triggers, and marks pipelines as development, so dev deploys stay isolated and inert. <!-- COLLECT: what runs after deploy, pass and fail criteria -->
5. Promote to the test target in production mode or no mode. ✅ Avoid development mode here, or test will be dev-prefixed and paused and will not mirror prod. <!-- COLLECT: the gate, who approves, checks that must pass first -->
6. Promote to the prod target in production mode under a stricter gate. ✅ Production mode blocks overriding declared cluster definitions and requires `run_as` and permissions to be set. <!-- COLLECT: prod approval mechanism, change-control link, approvers -->
7. Authenticate each deploy as a service principal. ✅ Databricks recommends a service principal for production, set via `run_as`, authenticated with OAuth M2M, credentials injected at runtime as CI environment variables, not in `databricks.yml`. <!-- COLLECT: which principal per target, secret store, rotation (OAuth secrets last up to 730 days) -->
8. Deploy the same built bundle to each target, varying only config. ✅ Targets define workspace host and mode, credentials are injected at runtime, so the artefact carries through unchanged. <!-- COLLECT: how config differs per target and how it is parameterised -->
9. Verify the deploy. <!-- COLLECT: post-deploy smoke test or health check per target -->
10. Define rollback. <!-- COLLECT: rollback mechanism and how prod recovers from a bad deploy -->

### Critical moves

| Move | What collapses without it | Status |
| :--- | :--- | :--- |
| Same bundle promoted across targets, config varied only | Dev and prod diverge, and validation in dev proves nothing about prod | ✅ Verified |
| Service-principal prod deploy via OAuth M2M | Humans hold prod credentials and the audit trail blurs | ✅ Verified |
| Mode set per target, not assumed | The wrong mode silently changes how resources deploy, so a lower target stops mirroring prod or prod loses its config lock | ✅ Verified |
| Approval gate before the prod target | An unreviewed change reaches production | <!-- COLLECT: the gate mechanism --> |

### Pits to avoid

Verified and stated:

- Confusing a target with a mode. Dev, test, and prod are three targets. Development and production are the two modes. Set the mode per target deliberately, because the wrong one changes deploy behaviour without warning.
- Hard-coding authentication in `databricks.yml`. The docs warn this reduces reusability and risks exposing service principal IDs. Inject credentials at runtime as CI environment variables.

From the first run:

<!-- COLLECT: real missteps. Candidates to confirm or drop:
- secrets committed to the repo instead of injected as CI variables
- config hardcoded per target instead of parameterised
- a service principal shared across targets, breaking isolation
- deploying a branch that was not the validated bundle
- no rollback path, so a bad prod deploy has no recovery
-->

## When to use it

- You have separate dev, test, and prod Databricks targets and want automated, gated promotion.
- Changes are code or config that can be version-controlled and bundled.
- ✅ The Databricks CLI v0.218.0 or above is installed on the runner, and workspace files are enabled, on by default from DBR 11.3 LTS.
- <!-- COLLECT: the CI platform, GitHub Actions or Azure DevOps -->

## When not to use it

- A single target with no promotion path.
- Ad-hoc, exploratory work not meant to reach prod.
- <!-- COLLECT: counter-cases that look like CI/CD but break the recipe -->

## Expected outcome

| Promise | How to check |
| :--- | :--- |
| The bundle in prod is the bundle validated in dev | <!-- COLLECT: version or hash match across targets --> |
| No human holds standing prod deploy access | ✅ The audit log shows the service principal as the deploying identity |
| Prod config cannot be overridden at deploy time | ✅ Production mode rejects cluster-definition overrides, checkable by attempting one |
| Every promotion is gated and recorded | <!-- COLLECT: where the approval and the deploy are logged --> |

## Tradeoffs

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Artefact format | Terraform, broad infra | Declarative Automation Bundles, Databricks-native | <!-- COLLECT: common answer is DABs for workloads, Terraform for infra --> |
| Branch model | Trunk-based | Gitflow | <!-- COLLECT --> |
| Prod gate | Fully automated | Manual approval | <!-- COLLECT: where on the line, and what it cost --> |
| Target config | One bundle, parameterised per target | Per-target bundles | <!-- COLLECT --> |
| Auth storage | Hard-coded in databricks.yml | Runtime env vars from CI secrets | Runtime env vars. Verified recommendation, keeps bundles reusable and hides principal IDs |

## Sources

Verified against official Microsoft Learn documentation, fetched 2026-06-24, pages updated March to April 2026.

| Topic verified | Source |
| :--- | :--- |
| Declarative Automation Bundles, name, purpose, CLI prerequisite | https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/ |
| Deployment modes, development and production behaviours | https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/deployment-modes |
| Authentication, OAuth M2M, service principals, runtime env vars | https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/authentication |
| Validate and deploy per target | https://learn.microsoft.com/en-us/answers/questions/5898485 |

## Version block

| Field | Value |
| :--- | :--- |
| Version | 0.4 (scaffold, iteration 4) |
| Last Updated | 2026-06-24 |
| Status | Draft, incomplete |
| Pairs with | O2 SAD Environment strategy and Segregation of rights blocks. CI/CD deliverable to be linked once a first run produces it |
