# CONSTITUTION.md — Headless Web App Builder (Databricks + Azure + Teams)

> Example file for the Claude Project Configuration Playbook
> Domain: Full-Stack / Data Engineering — Unity Catalog as source of truth
>
> Upload this file as a knowledge file named `CONSTITUTION.md` in your project.
> Reference it from the system prompt with a single line:
> `Apply all rules defined in CONSTITUTION.md at all times.`

---

## Output Mode Rules

Every skill and workflow invocation must declare an output mode explicitly.
Claude must refuse to generate if output mode is missing — return:
`{ "blocked": true, "reason": "output mode not specified", "valid_modes": ["developer", "ci", "tool"] }`

| Mode | Format | Use |
| :--- | :--- | :--- |
| developer | Annotated code/markdown with rationale, flags, and inline comments | Human review and decision-making |
| ci | Clean code or JSON, no prose, no comments, linting-ready | CI pipelines, automated deployment |
| tool | Ready-to-use payload for a specific tool (Postman, Teams, Event Hub) | Direct import or post, no modification needed |

---

## Schema Rules

- Unity Catalog schema is the only source of truth — never invent, assume, or rename fields
- If a referenced table or column is not in the provided schema, return:
  `{ "blocked": true, "missing_schema": "[table_name]" }`
- Nullability must be preserved exactly — never make a nullable field required
- Column types must map to their exact Python/Pydantic equivalents — no lossy casting
- Immutable columns (`created_at`, `id`, `source_system`) must always be read-only in API contracts
- Schema drift (diff between versions) must always produce a `breaking: true|false` flag per field

---

## API Contract Rules

- All contracts are OpenAPI 3.1 JSON — no other format
- No invented endpoints — every endpoint must map to a real Unity Catalog entity
- PATCH must only include mutable fields — never expose immutable columns as writable
- Every response must include a structured error envelope:
  `{ "error": true, "code": "...", "message": "...", "field": "..." }`
- Breaking changes (field removal, type change, nullable → required) must be flagged explicitly
  with `{ "breaking": true, "impact": "..." }` before generating

---

## Code Generation Rules

- All Python code is 3.11+ — use match/case, typed dicts, and dataclasses where appropriate
- No raw SQL strings — all Databricks SQL queries must be parameterized
- No auth implementation — generate a dependency injection stub and flag: `# AUTH_REQUIRED`
- No TODO comments in ci mode — either implement or block with a structured flag
- FastAPI routers must be modular — one router per entity, never a monolithic routes file
- All Pydantic models must have `model_config = ConfigDict(strict=True)`

---

## Event Rules

- All events use the shared envelope: `{ event_id, event_type, direction, timestamp, source, payload }`
- Event type naming: `domain.entity.action` — e.g. `orders.invoice.created`
- Direction must always be explicit: `ingress` | `egress` — never implicit
- Ingress and egress payloads share the schema contract — differences must be flagged
- No fire-and-forget events — every event definition must include an error/dead-letter strategy

---

## Teams Notification Rules

- Workflow notifications (human-to-human): must include requester identity, action summary,
  and at least one actionable button (approve/reject) pointing to a FastAPI endpoint
- Monitoring notifications (system-to-manager): Claude must reason about the data first —
  never relay raw metrics without a narrative summary
- Narrative summaries: 2-3 sentences max, audience-appropriate, no technical jargon for managers
- All Teams payloads are Adaptive Cards — no legacy MessageCard format
- Severity must always be indicated: `{ "severity": "info" | "warning" | "critical" }`
- Never post PII in a Teams card — flag any field that could contain PII with `# PII_RISK`

---

## Schema Sync Rules

- The sync script must always produce a structured diff — never overwrite silently
- Breaking changes found during sync must block the workflow and require explicit confirmation
- Sync artifacts (exported schemas) must be versioned with a timestamp suffix
- CI sync pipelines must fail loudly on breaking changes — no silent passes
- The sync script must be idempotent — safe to run multiple times without side effects
