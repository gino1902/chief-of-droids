<!-- pass C reference for project-bootstrapping -->

# Pass C — FRAMING.md

FRAMING.md is the intent anchor. It answers why the project exists, who it is for, what
success looks like, and what it delivers. It is the one artifact that is mostly supplied
by the user rather than read from the repo, and it is the source of truth that passes D
and B are derived from.

FRAMING.md is user-owned once created. Never modify it autonomously in a later session.
Reconcile it only with explicit approval, and only to fill gaps — never rewrite wholesale.

## The five questions

Ask these, keep answers tight, and write only what the user gives you. Do not pad.

1. **Why** — the problem or opportunity this project exists to address. One short paragraph.
2. **For whom** — who the work is for. The audience or beneficiary, not a job title.
3. **Success** — what makes this project done or working. Observable, not aspirational.
4. **Delivered** — what is actually produced. The concrete outputs (documents, a service,
   modules, a dataset).
5. **Constraints** — the limits and boundaries the solution must respect: technical, data,
   timeline, budget, or hard exclusions. This is the scoping signal that keeps later work
   inside its lines, so it is worth capturing even briefly.

Also confirm the goal (`thinking` / `code` / `infra`) if it was not already resolved, since
it gets stamped here and drives the later passes.

## Template

```markdown
<!-- goal: <thinking|code|infra> -->
# FRAMING — <project name>

> User-owned. Claude will not modify this file autonomously.

## Why
<one paragraph, or 🔲 if not yet defined>

## For whom
<audience / beneficiary, or 🔲>

## Success
<what done/working looks like, or 🔲>

## Delivered
<the concrete outputs, or 🔲>

## Constraints
<limits and boundaries the solution must respect, or 🔲>
```

Leave any section the user cannot answer yet marked `🔲` rather than inventing content —
an honest gap is more useful than a plausible guess, and it signals what still needs their
input before substantive work.

## Reconcile mode (FRAMING.md already exists)

- Read the goal from the `<!-- goal: ... -->` stamp. If an argument conflicts with it, stop
  and report the conflict.
- Propose a minimal diff that fills `🔲` gaps only, from what the user now tells you.
- Preserve the author's wording everywhere else. Apply only after approval.

## Note on the footer

FRAMING.md is user-owned, so it is exempt from the repo's version-block convention. A
single status line is enough if the user wants one. Do not attach the full version table.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.1        |
| Last Updated | 2026-07-07 |
| Status       | Review     |
