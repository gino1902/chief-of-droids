#!/usr/bin/env python3
"""Feed a Microsoft Planner *basic* plan from a roadmap markdown file, via Graph.

Parses epics of the shape used in pi1-roadmap.md:

    ## Epic 1 (Enabler — commercial) — Procurement onboarding
    > so-that rationale ...
    Acceptance criteria:
    - criterion one
    - criterion two
      > ⚠️ Unverified — note attached to the criterion above

Each epic becomes one Planner task:
  - title        = "Epic N — <name>"
  - bucket       = PI2 if the epic body mentions "PI2 candidate", else PI1
  - notes        = the so-that blockquote + the full numbered acceptance criteria
  - checklist    = one item per criterion, truncated to Planner's 100-char limit

Idempotent: tasks are matched by title. Re-running updates bucket, notes and
checklist in place rather than duplicating.

LIMITATION: Graph /planner serves *basic* plans only. Premium plans (Project for
the web, container.type "unknownFutureValue") return 403 on write — feed those
via the Dataverse / Project API instead.

AUTH (no install needed):
  1. https://developer.microsoft.com/en-us/graph/graph-explorer  -> sign in
  2. consent to Tasks.ReadWrite (+ Group.ReadWrite.All if creating a plan)
  3. copy the token from the "Access token" tab into a file
  4. pass it with --token-file, or export GRAPH_TOKEN=...

USAGE:
  # dry run — parse and print, no writes
  python3 planner_feed.py --roadmap ../../desktop-chat/outputs/2606-o2-roadmap/pi1-roadmap.md --dry-run

  # feed an existing basic plan
  python3 planner_feed.py --roadmap PATH --plan-id <id> --token-file token.txt

  # create a fresh roster-backed plan and feed it
  python3 planner_feed.py --roadmap PATH --create --title "O2 PI1 backlog" --token-file token.txt

  # tear down a roster-backed plan created with --create
  python3 planner_feed.py --delete-plan <id> --token-file token.txt
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error, uuid

GRAPH = "https://graph.microsoft.com/v1.0"
BETA = "https://graph.microsoft.com/beta"
CHECKLIST_MAX = 100  # Planner hard limit on checklist item title length

TOKEN = None


def call(method, path, body=None, etag=None):
    url = path if path.startswith("http") else GRAPH + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    if etag:
        req.add_header("If-Match", etag)
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read().decode()
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw


# ---------------------------------------------------------------- parsing
def parse_roadmap(text):
    """Return list of {n, title, pi, note, criteria:[...]} from roadmap markdown."""
    epics = []
    # split on epic headings, keep the heading
    parts = re.split(r"^##\s+Epic\s+", text, flags=re.M)
    for chunk in parts[1:]:
        body = "Epic " + chunk
        # stop at a horizontal rule or the Sources section
        body = re.split(r"^---\s*$|^##\s+Sources", body, flags=re.M)[0]
        head = body.splitlines()[0]
        m = re.match(r"Epic\s+(\d+)\b", head)
        if not m:
            continue
        n = int(m.group(1))
        # name is the segment after the LAST " — " (skips the "(Enabler — x)" type tag)
        name = head.rsplit(" — ", 1)[-1].strip() if " — " in head else head
        title = f"Epic {n} — {name}"
        pi = "PI2" if re.search(r"PI2 candidate", body) else "PI1"
        # note = blockquote lines that appear before "Acceptance criteria:"
        before = re.split(r"Acceptance criteria:", body)[0]
        note_lines = [l.lstrip("> ").rstrip() for l in before.splitlines()
                      if l.lstrip().startswith(">")]
        note = " ".join(note_lines).strip()
        # criteria = "- " bullets after "Acceptance criteria:"
        criteria = []
        after = body.split("Acceptance criteria:", 1)
        if len(after) == 2:
            warn = None
            for raw in after[1].splitlines():
                s = raw.strip()
                if s.startswith("- "):
                    criteria.append(s[2:].strip())
                elif s.startswith(">") and criteria:
                    # ⚠️ unverified note attaches to the previous criterion
                    w = s.lstrip("> ").strip()
                    criteria[-1] = "[UNVERIFIED] " + criteria[-1] if "Unverified" in w \
                        else criteria[-1]
        epics.append({"n": n, "title": title, "pi": pi, "note": note, "criteria": criteria})
    epics.sort(key=lambda e: e["n"])
    return epics


def checklist_label(criterion):
    c = criterion
    if len(c) <= CHECKLIST_MAX:
        return c
    cut = c[:CHECKLIST_MAX - 1]
    if " " in cut:
        cut = cut[:cut.rfind(" ")]
    return cut + "…"


# ---------------------------------------------------------------- graph ops
def ensure_buckets(pid, names):
    s, bk = call("GET", f"/planner/plans/{pid}/buckets")
    existing = {b["name"]: b["id"] for b in bk.get("value", [])}
    # create missing in reverse so the first listed name sorts to the top
    for name in reversed(names):
        if name not in existing:
            s, b = call("POST", "/planner/buckets",
                        {"name": name, "planId": pid, "orderHint": " !"})
            existing[name] = b["id"]
    return existing


def write_details(tid, note, criteria):
    # fetch etag + existing checklist (retry: details lag task creation)
    etag, existing = None, {}
    for _ in range(8):
        s, det = call("GET", f"/planner/tasks/{tid}/details")
        if isinstance(det, dict) and det.get("@odata.etag"):
            etag, existing = det["@odata.etag"], det.get("checklist", {}) or {}
            break
        time.sleep(1.0)
    desc = note + "\n\nAcceptance criteria:\n" + \
        "\n".join(f"{i+1}. {c}" for i, c in enumerate(criteria))
    cl = {g: None for g in existing}  # clear any prior items
    for c in criteria:
        cl[str(uuid.uuid4())] = {"@odata.type": "microsoft.graph.plannerChecklistItem",
                                 "title": checklist_label(c), "isChecked": False}
    body = {"description": desc, "previewType": "checklist", "checklist": cl}
    s, r = call("PATCH", f"/planner/tasks/{tid}/details", body, etag=etag)
    if s not in (200, 204):
        s2, det = call("GET", f"/planner/tasks/{tid}/details")
        s, r = call("PATCH", f"/planner/tasks/{tid}/details", body, etag=det.get("@odata.etag"))
    return s


def feed(pid, epics, bucket_names):
    buckets = ensure_buckets(pid, bucket_names)
    bucket_for = {"PI1": buckets[bucket_names[0]], "PI2": buckets[bucket_names[1]]}
    s, tk = call("GET", f"/planner/plans/{pid}/tasks")
    by_title = {t["title"]: t for t in tk.get("value", [])}
    results = []
    for e in epics:
        bid = bucket_for[e["pi"]]
        if e["title"] in by_title:  # update existing
            t = by_title[e["title"]]
            if t.get("bucketId") != bid:
                call("PATCH", f"/planner/tasks/{t['id']}", {"bucketId": bid},
                     etag=t["@odata.etag"])
            tid, action = t["id"], "updated"
        else:  # create
            s, t = call("POST", "/planner/tasks",
                        {"planId": pid, "bucketId": bid, "title": e["title"]})
            if s not in (200, 201):
                results.append((e["n"], f"CREATE FAILED {s}", json.dumps(t)[:120]))
                continue
            tid, action = t["id"], "created"
        ds = write_details(tid, e["note"], e["criteria"])
        results.append((e["n"], action, f"details {ds} / {len(e['criteria'])} criteria"))
    return results


def create_roster_plan(title, my_oid):
    s, roster = call("POST", BETA + "/planner/rosters", {})
    if s not in (200, 201):
        sys.exit(f"roster create failed {s}: {roster}")
    rid = roster["id"]
    if my_oid:
        call("POST", BETA + f"/planner/rosters/{rid}/members", {"userId": my_oid})
    s, plan = call("POST", BETA + "/planner/plans",
                   {"container": {"url": f"{BETA}/planner/rosters/{rid}"}, "title": title})
    if s not in (200, 201):
        sys.exit(f"plan create failed {s}: {plan}")
    return plan["id"], rid


def delete_plan(pid):
    # roster-backed plans delete by deleting the plan, then the roster cascades;
    # retry because deletion is eventually consistent
    s, plan = call("GET", f"/planner/plans/{pid}")
    if s == 404:
        return "already gone"
    container = plan.get("container", {}).get("containerId", "")
    for _ in range(6):
        s, plan = call("GET", f"/planner/plans/{pid}")
        if s == 404:
            return "deleted"
        call("DELETE", f"/planner/plans/{pid}", etag=plan.get("@odata.etag"))
        # if roster-backed, dropping the roster cascades
        if "_" not in container:  # not premium; may be a plain roster id
            call("DELETE", BETA + f"/planner/rosters/{container}")
        time.sleep(3)
    return "still present — check manually"


# ---------------------------------------------------------------- cli
def load_token(args):
    if args.token_file and os.path.exists(args.token_file):
        return open(args.token_file).read().strip()
    if os.environ.get("GRAPH_TOKEN"):
        return os.environ["GRAPH_TOKEN"].strip()
    sys.exit("No token. Use --token-file PATH or export GRAPH_TOKEN. See header for how to get one.")


def main():
    global TOKEN
    ap = argparse.ArgumentParser(description="Feed a basic Planner plan from a roadmap markdown.")
    ap.add_argument("--roadmap", help="path to roadmap markdown")
    ap.add_argument("--plan-id", help="existing basic plan id to feed")
    ap.add_argument("--create", action="store_true", help="create a roster-backed plan first")
    ap.add_argument("--title", default="Roadmap backlog", help="title when --create")
    ap.add_argument("--my-oid", help="your Entra object id, to add yourself to the new roster")
    ap.add_argument("--buckets", default="PI1,PI2 candidates",
                    help="comma list: first=PI1 bucket, second=PI2 bucket")
    ap.add_argument("--token-file")
    ap.add_argument("--dry-run", action="store_true", help="parse and print only, no writes")
    ap.add_argument("--delete-plan", help="delete a plan id and exit")
    args = ap.parse_args()

    if args.delete_plan:
        TOKEN = load_token(args)
        print(delete_plan(args.delete_plan))
        return

    if not args.roadmap:
        ap.error("--roadmap is required (unless --delete-plan)")
    epics = parse_roadmap(open(args.roadmap).read())
    if args.dry_run:
        for e in epics:
            print(f"[{e['pi']}] {e['title']}  ({len(e['criteria'])} criteria)")
            print(f"    note: {e['note'][:90]}...")
            for c in e["criteria"]:
                tag = "  ✂" if len(c) > CHECKLIST_MAX else "   "
                print(f"  {tag} {checklist_label(c)}")
        print(f"\n{len(epics)} epics parsed. (dry run — no writes)")
        return

    TOKEN = load_token(args)
    bucket_names = [b.strip() for b in args.buckets.split(",")]
    pid = args.plan_id
    rid = None
    if args.create:
        pid, rid = create_roster_plan(args.title, args.my_oid)
        print(f"created plan {pid} (roster {rid})")
    if not pid:
        ap.error("need --plan-id or --create")
    for r in feed(pid, epics, bucket_names):
        print("  Epic", r[0], "|", r[1], "|", r[2])
    print(f"done. plan id: {pid}" + (f"  roster: {rid}" if rid else ""))


if __name__ == "__main__":
    main()
