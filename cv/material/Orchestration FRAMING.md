---
name: Operations Orchestrator (O2)
last_updated: 2026-09-06
---

# Operations Orchestrator (O2) Framing

## Target problem

Company data is fragmented and not consistently trusted, so cross-team workflows often break at the handovers. Each team's data sits in disconnected places and tools it can't fully trust, making collaboration difficult whenever work crosses a boundary. For instance, Finance and Operations teams have issues in running a clean path from Budget and Forecast to Report, and Talent Supply are not running with a clear path, rely on too many manual tasks, multiple checks, and cannot be monitored end to end.


## Our approach

We give teams one governed source of trusted data that carries their cross-team workflows, reached by orchestrating agents around each team's existing practices rather than imposing a new operating model the way SAP or Oracle would. The data platform is the enabler underneath. The agentic workflow orchestration, fitted to how teams already work, is the bet.

## Who it's for

**Customer:** Internal operational teams across the company (HR admin, recruitment and training, finance, operations, service lines, sales, delivery, procurement, marketing, executives). They will use the O2 platform to run cross-team workflows like budget-to-report and talent-request-to-deployment on trusted data without chasing it at every handover.

**Business Executives:** CEO, Executive Committee. When fully deployed, the platform adoption will result in the shift from manual work to value work for corporate teams (analysis, anticipation, risk management), the increase of managers chargeability (revenue and margin impact), and by freeing sales time for customer-facing work (bookings and revenue impact).

## What success means

**For the customer:** Teams see budget-to-report and talent-request-to-deployment end to end without chasing data, and spend more time on value tasks.

- **Cycle time, budget-to-report** - from orchestrator workflow timestamps.
- **Cycle time, talent-request-to-deployment** - from orchestrator workflow timestamps.

**For the business:** Automation and simplification convert freed time into cost taken out and value added.

- **Corp-team cost reduction** - from finance actuals as teams run leaner, targeted by end of 2027. Magnitude deliberately not committed yet.
- **Time reinvested in value work** - manager chargeability and sales customer-facing time, from a periodic survey.

## Tracks

### Infrastructure & platforming

How a secure foundation is built, from network configuration and access management to a terraformed, tested workspace. Finite and front-loaded work that every later artefact is written into.

_Why it serves the approach:_ teams, data and agents need a foundation that deploys the same way every time, keeps time-to-market short, carries POC and production alike, and stays secure and observable throughout.

### Platform engineering

All platform components enabling use case implementation: Unity Catalog, connectors, CI/CD, the cost and usage model, the observability model, tags policy, architecture decisions, and the development framework built as runway (project tree, templates, harness), extended only as slices need it.

_Why it serves the approach:_ orchestrating agents around each team's practice only stays fast and trustworthy if the platform rests on standardised, repeatable engineering.

### Data engineering

Data transformation from ingestion to trusted, business-ready state across `Bronze`, `Silver` and `Gold`, delivered as vertical slices that each end at a consumer, with parity tests against the figures users read today.

_Why it serves the approach:_ the enabler layer that makes one source of trusted data real, proven on real data under real consumption.

### Usage layer

The endpoints users interact with: AI/BI, agents, workflows. One endpoint per slice, dashboard first, with custom apps and agent and workflow endpoints built as demand arrives.

_Why it serves the approach:_ this is where the orchestration differentiator lives, and where usage feedback starts.

### Deployment

Drives use case adoption from an upfront selection process to roll out, through iterative improvement based on business team usage monitoring and feedback. Invite over Impose. Selection sits at the head of the plan and the feedback loop runs inside every slice.

_Why it serves the approach:_ modernising existing practice depends on teams adopting it in daily work.

## Not working on

- Middleware refactoring, owned by IT - the middleware that pushes data to the landing zone before extraction. Outside this project's scope, but a strong upstream dependency.
