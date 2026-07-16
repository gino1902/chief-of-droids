# ticket-api

## Purpose
The ticket API creates and fetches support `ticket`s for `agent`s, so support work has one record per request.

## Scope
Covers creating a `ticket` from a submitted payload, and fetching a `ticket` by id. Out of scope: assignment routing (owned by the routing service); notifications (owned by the notifier).

## Actors and consumers
Upstream, the `agent` calling the API over HTTP. Downstream, the ticket store that persists a `ticket`.

## Requirements
- The system shall create a `ticket` from a submitted payload, so that the request is recorded, when the payload is valid.
- The system shall return a `ticket` by id, so that the agent reads it, when the id exists.
- A `ticket` id, once assigned, never changes. (static invariant)
- Fetch shall return within 300 ms at the 95th percentile. (non-functional)
- Only the `agent` assigned to a `ticket` may read it. (security)
- Every create emits a `ticket.created` metric. (observability)
