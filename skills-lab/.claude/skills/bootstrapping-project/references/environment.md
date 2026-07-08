<!-- pass 1 reference for bootstrapping-project -->

# Pass 1 — environment

Establishes the operating environment first, because the permission defaults set here
decide whether every later write prompts or flows. Goal-agnostic: the same baseline
applies to thinking, code, and infra projects. Stack-specific configuration (hooks, MCP,
goal-specific deny rules) is deliberately deferred to the tail of pass 4, once the stack
is actually known.

## Steps

1. If there is no `.git/`, run `git init`. This makes every subsequent artifact tracked
   and diffable, which is what makes a multi-pass, resumable bootstrap pleasant to stop
   and restart.
2. Show the baseline `settings.json` and `.gitignore` below, adjusted to the repo, before
   writing. Settings change how the harness behaves, so they are approval-gated even though
   the defaults are conservative.
3. Write `.claude/settings.json` and `.gitignore` on approval.
4. Do not create hooks, `.mcp.json`, or `.claude/agents/` now. Note them as available
   follow-ups. They depend on decisions that only land in passes 3 and 4.

`.claude/settings.json` is written exactly once — here, at the baseline. No later pass
mutates it. In particular, the pass 4 enforcement tail never adds `deny` rules to the file:
any hard prohibition discovered later is surfaced as a proposal in the close report, not
written into `settings.json` by the skill. This keeps the file deterministic across runs —
two bootstraps of the same brief produce byte-identical `settings.json`.

## Baseline `.claude/settings.json`

The baseline is deliberately small. It carries only what generalises to any project.
Explain each line to the user so they can adjust before it is written — do not present it
as fixed.

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "ask": [
      "Bash(rm *)"
    ]
  }
}
```

Why these two, and only these two:

- `defaultMode: acceptEdits` auto-approves file writes and filesystem Bash inside the
  working directory, so the passes that follow do not prompt on every write. Targets
  outside the working directory still prompt.
- `ask: Bash(rm *)` puts destructive removals behind a prompt regardless of mode. `ask`
  is chosen over `deny` on purpose: it confirms rather than hard-blocks, so the user is
  never forced to edit settings just to delete a file. Removal is the one common
  irreversible action worth a deliberate confirmation. The rule uses the space syntax
  (`rm *`), which is the form documented for Bash permission rules.

## What does not belong in the baseline

A permission is baseline only if it generalises to any project. Most of what accumulates in
a mature repo's `settings.json` does not — it encodes that repo's stack and identity, and
copying it forward pollutes every new project. Keep these out of the generated baseline:

- Domain `WebFetch` allowlists. They reflect the sources one project happens to read.
- `Skill(...)` allows and stack tools like `python3 *`. Stack- and project-specific — these
  are added in pass 4 once the stack is real, or land in `settings.local.json`.
- Hooks, MCP config, and subagents. Deferred to pass 4 for the same reason.

Offer, but do not add without being asked: an `allow` list for read-only Bash the user runs
often, `git add`/`git commit` convenience allows, or `autoMemoryEnabled: false`. That last
one flips the Claude Code default (`true`) off so Claude neither reads nor writes the auto
memory directory — a reasonable conservative choice for a fresh project, but a preference,
so surface it with that one-line rationale rather than writing it silently.

## Baseline `.gitignore`

Start minimal and stack-agnostic. A stack-specific `.gitignore` is better added in pass 3
or 4, once the tree and stack are known, so it stays grounded.

```gitignore
# OS
.DS_Store

# Claude Code local state
.claude/cache/
.claude/settings.local.json
```

`settings.local.json` is ignored because it is the per-user override layer — it should not
be committed. `settings.json` (the shared baseline you just wrote) is committed.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.3        |
| Last Updated | 2026-07-08 |
| Status       | Review     |
