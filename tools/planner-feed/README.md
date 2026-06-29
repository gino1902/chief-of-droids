# planner-feed

Feed a Microsoft Planner **basic** plan from a roadmap markdown file, via Microsoft Graph. Built to push the O2 PI1 roadmap epics into Planner, but works for any roadmap of the same shape.

## What it does

Each `## Epic N …` section in the roadmap becomes one Planner task:

| Planner field | Source |
| :--- | :--- |
| Title | `Epic N — <name>` (name taken after the last ` — ` in the heading) |
| Bucket | `PI2` if the epic body mentions "PI2 candidate", else `PI1` |
| Notes | the `> so that…` blockquote, plus the full numbered acceptance criteria |
| Checklist | one item per criterion, truncated to Planner's 100-char limit |

Runs are idempotent. Tasks are matched by title, so re-running updates bucket, notes and checklist in place instead of creating duplicates.

## Hard constraint: basic plans only

Graph `/planner` serves **basic** plans. **Premium** plans (Project for the web, `container.type` = `unknownFutureValue`) return **403 on write** even with a valid `Tasks.ReadWrite` token. They can be read but not fed this way. To feed a Premium plan you need the Dataverse / Project-for-the-web API, not this tool.

The claude.ai Microsoft 365 connector is **not** a route either: it exposes only read/search tools (mail, calendar, Teams chat, SharePoint), no Planner surface at all.

## Auth (no install)

1. Open https://developer.microsoft.com/en-us/graph/graph-explorer and sign in.
2. Consent to `Tasks.ReadWrite` (and `Group.ReadWrite.All` if you use `--create`).
3. Copy the token from the **Access token** tab into a file, e.g. `token.txt`.
4. Pass it with `--token-file token.txt`, or `export GRAPH_TOKEN=…`.

The token is short-lived (~1 h). Do not commit it (`token.txt` is gitignored below).

## Usage

```bash
# parse and preview only — no token, no writes
python3 planner_feed.py --roadmap ../../desktop-chat/outputs/2606-o2-roadmap/pi1-roadmap.md --dry-run

# feed an existing basic plan
python3 planner_feed.py --roadmap PATH --plan-id <planId> --token-file token.txt

# create a fresh roster-backed plan and feed it (--my-oid adds you as a member so it shows in your Planner)
python3 planner_feed.py --roadmap PATH --create --title "O2 PI1 backlog" \
  --my-oid <your-entra-object-id> --token-file token.txt

# tear down a roster-backed plan created with --create
python3 planner_feed.py --delete-plan <planId> --token-file token.txt
```

Get a plan id: `GET https://graph.microsoft.com/v1.0/me/planner/plans` in Graph Explorer, or run `--create` which prints one.

## Notes / gotchas baked in

- Updating task **details** requires an `If-Match` etag, and the details object lags task creation — the script retries the etag fetch.
- Checklist item titles max **100 chars** (Graph rejects longer with a schema-validation 400). Full criteria live in the notes; checklist items are truncated at a word boundary.
- Rosters are a **beta** Graph feature (`/beta/planner/rosters`); plan/bucket/task/details calls use `v1.0`.
- Stdlib only — no pip install.
