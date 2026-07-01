# MS Planner interface from Claude Code, session handoff

Purpose: let a later session resume and refine the work without re-discovering the constraints. State captured 2026-06-26.

## Intent

Test whether Claude Code can feed a Microsoft Planner backlog, in the SQLI Microsoft 365 tenant, using the SQLI Claude account. The source backlog is a repo file (the O2 PI1 roadmap). The reference plan given was a Planner Premium plan.

Key identifiers:
- Reference (Premium) plan id is `11bb4316-6479-4946-8b44-c6918458a5a8`.
- Tenant id is `20f62116-4d0c-44ac-8a45-390ca2765601`.
- Org / group id is `8f8d6a4d-2a8e-4f8d-aca9-0f3d72b24c48`.
- Source backlog is `desktop-chat/outputs/2606-o2-roadmap/pi1-roadmap.md` (8 epics, PI1 is epics 1 to 6, PI2 candidates are epics 7 to 8).
- User Entra object id is `9be905f2-9916-4959-9cd9-f68b74169e71`.

## Options, decisions, open points

Routes considered for writing to Planner:
1. The claude.ai Microsoft 365 connector. Rejected. It exposes only read and search tools (mail, calendar, Teams chat, SharePoint, get_me). It has no Planner surface and no write of any kind.
2. Microsoft Graph `/planner` direct, called with a token. Chosen and proven, for basic plans only.
3. The Dataverse / Project-for-the-web API, for Premium plans. Not attempted. This is the open spike.

Decisions taken by the user:
- The source of the backlog is repo files.
- The first live test was one throwaway task. It grew to the full feed once the pipe was understood.
- The real destination should be a basic plan, not the Premium plan.
- The work should be productionised into a repeatable script. Done.
- Whether to investigate the Premium route is not decided yet. Still open.
- Keep only the clean tool in the repo, no scratchpad scripts.

Open points and issues:
- The reference O2 plan is Premium, so it cannot be fed via Graph `/planner` (403 on write). If the actual Premium plan must be the target, a Dataverse / Project-for-the-web spike is required. This is the main unresolved question.
- Auth is manual (a Graph Explorer token, roughly one hour lifetime). No unattended or service-principal auth is set up. A scheduled or automated feed would need an app registration with `Tasks.ReadWrite`, which likely needs tenant-admin consent.

## Git status

The tool is committed and the working tree is clean. `tools/planner-feed/` (`.gitignore`, `README.md`, `planner_feed.py`) was added in commit `ce54656` ("chore: add planner-feed tool and two business-plan output docs"). This corrects an earlier draft note that wrongly said the files were untracked.

## Verified constraints (do not re-litigate)

| Finding | Consequence |
| :--- | :--- |
| Connector has no Planner tools | Connector is not a write path |
| Premium plan reads on Graph but returns 403 on write. It shows `container.type` of `unknownFutureValue` and a compound `containerId` of `{org}_{premiumPlanId}` | Premium backlogs need Dataverse, not Graph `/planner` |
| Basic plans read and write fully on Graph `/planner` | This is the working pipe |
| Checklist item title max is 100 chars | Graph rejects longer titles with a schema-validation 400. Full criteria go in the notes, checklist items are truncated at a word boundary |
| Task details update needs an `If-Match` etag, and details lag task creation | Retry the etag fetch before the PATCH |
| Rosters are beta only (`/beta/planner/rosters`) | Plan, bucket, task and details calls use v1.0, roster operations use beta |
| Deleting a roster-backed plan is eventually consistent | Retry the delete until GET returns 404 |

## Activities and outputs

Activities run in the session:
- Authenticated the claude.ai Microsoft 365 connector, enumerated its tools, confirmed no Planner surface.
- Probed Graph with a Graph Explorer token. Confirmed the reference plan is Premium and returns 404 on `/planner` GET by id, yet appears read-only under `/me/planner/plans` as "O2 PI-1 Plan".
- Proved write against a basic plan. Built a roster-backed plan, fed all 8 epics with buckets, notes and checklists, verified, then deleted.
- Diagnosed the 100-char checklist limit and the details etag race.
- Productionised into a CLI, then ran a live create, feed, idempotent re-run and teardown to validate it.
- Deleted both test plans and their rosters. The tenant was left clean. Deleted the token file.

Outputs kept (in the repo, committed):
- `tools/planner-feed/planner_feed.py`, a stdlib-only CLI. It parses the roadmap, upserts tasks by title, creates buckets, and handles the etag race and the 100-char limit. Modes are `--dry-run`, `--plan-id`, `--create` and `--delete-plan`.
- `tools/planner-feed/README.md`, covering usage, the Graph Explorer auth step, and the constraints.
- `tools/planner-feed/.gitignore`, which keeps token files out of git.

Outputs discarded:
- The scratchpad build and debug scripts (`feed_planner.py`, `set_details.py`, `fixup_details.py`) and intermediate JSON. These were session-temporary and are superseded by the CLI.

## Suggested next steps for a refining session

1. Decide the real target. If a basic plan is acceptable, pick or create one and point the CLI at it. If the Premium O2 plan is mandatory, open the Dataverse spike.
2. If refining the basic-plan path, add assignees, due dates, labels or priority, and map the dependency chain (each epic depends on earlier ones) into task ordering or a start and due schedule.
3. If automating, register an Entra app with `Tasks.ReadWrite`, get admin consent, and switch the CLI from a pasted token to client-credentials or device-code auth.

<!--
Version: 1.0 | Last Updated: 2026-06-26 | Status: Draft
-->
