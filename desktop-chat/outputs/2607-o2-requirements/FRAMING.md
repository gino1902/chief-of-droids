---
name: Operations Orchestrator (O2)
last_updated: 2026-07-09
---

# Operations Orchestrator (O2) Framing

## Target problem

Company data is fragmented and not consistently trusted, so cross-team workflows often break at the handovers. Each team's data sits in disconnected places and tools it can't fully trust, making collaboration difficult whenever work crosses a boundary. For instance, Finance and Operations teams have issues in running a clean path from Budget and Forecast to Report, and Talent Supply are not running with a clear path, rely on too many manual tasks, multiple checks, and cannot be monitored end to end.


## Our approach

We give teams one governed source of trusted data that carries their cross-team workflows, reached by orchestrating agents around each team's existing practices rather than imposing a new operating model the way SAP or Oracle would. The data platform is the enabler underneath. The agentic workflow orchestration, fitted to how teams already work, is the bet.

## Who it's for

**Customer:** Internal operational teams across the company (HR admin, recruitment and training, finance, operations, service lines, sales, delivery, procurement, marketing, executives). The will use O2 platform to run cross-team workflows like budget-to-report and talent-request-to-deployment on trusted data without chasing it at every handover.

**Business Executives:** CEO, Executive Committee. When fully deployed, the platform adoption will result in the shift from manual work to value work for corporate teams (analysis, anticipation, risk management), the increase of managers chargeability (revenue and margin impact), and by freeing sales time for customer-facing work (bookings and revenue impact).

## What success means

**For the customer:** Teams see budget-to-report and talent-request-to-deployment end to end without chasing data, and spend more time on value tasks.

- **Cycle time, budget-to-report** - from orchestrator workflow timestamps.
- **Cycle time, talent-request-to-deployment** - from orchestrator workflow timestamps.

**For the business:** Automation and simplification convert freed time into cost taken out and value added.

- **Corp-team cost reduction** - from finance actuals as teams run leaner, targeted by end of 2027. Magnitude deliberately not committed yet.
- **Time reinvested in value work** - manager chargeability and sales customer-facing time, from a periodic survey.

## Tracks

### Company infrastructure

The company network, IAM, security, and monitoring the platform runs on. Terraform template creation and tests.

_Why it serves the approach:_ trusted data and agents need a secure, observable foundation before teams rely on them.

### Platform engineering

How the platform is built and run: Unity Catalog governance, environment configuration (landing zone, workspaces), CI/CD, the cost and usage model, and the development framework (project tree, templates, skills, decision framework).

_Why it serves the approach:_ orchestrating agents around each team's practice only stays fast and trustworthy if the platform rests on standardised, repeatable engineering.

### Data ingestion and transformation

Capturing workflows and data flows. Create ingestion pipeline. Transform data into gold layer making it consistent and trustworthy.

_Why it serves the approach:_ the enabler layer that makes one source of trusted data real.

### Data exposition, driven by customer use cases

Exposing trusted data through team-fitted agentic workflows, built use case by use case, according to a decision framework to evaluate use case elligibily (ROI, location) 

_Why it serves the approach:_ this is where the orchestration differentiator lives.

### Iterative adoption

Rolling out use case per use case. Iterative improvement based on business team usage monitoring and feedback. Invite over Impose pattern. 

_Why it serves the approach:_ modernising existing practice depends on teams adopting it in daily work.

## Not working on

- Middleware refactoring, owned by IT - the middleware that pushes data to the landing zone before extraction. Outside this project's scope, but a strong upstream dependency.
