# Claude Code Project Configuration — Authoring Guidelines

## Purpose

Given a project requirements framing, decide where each fact, rule, command, or
procedure must materialize across the project's `.claude/` tree, then produce
the artifacts. These guidelines are the routing rubric — they are **not**
themselves project content.

## Inputs you accept

A framing document describing any subset of:

- Tech stack, frameworks, runtime, language versions
- Build / test / lint / format commands
- Project layout and naming conventions
- Coding standards (style, paradigms, banned patterns)
- Workflows (PR review, deploy, release, migration)
- Security and compliance constraints
- External integrations (databases, SaaS, internal services)
- Personal preferences vs. team conventions

## User configuration rules

Standing defaults that apply to every framing routed through this rubric.
Treat as input alongside the project-specific framing document.

### Conventions

- Version block mandatory on every workflow-authored `.md` (excludes chat
  outputs and user-owned files like `FRAMING.md`):

  | Field | Value |
  |---|---|
  | Version | 1.x |
  | Last Updated | YYYY-MM-DD |
  | Status | Draft / Review / Final |

- Increment rule: `1.0` initial, `1.x` minor, `2.0` structural rewrite.

### Safety stance

- Strict cwd scope: all reads/writes confined to cwd and subdirectories;
  out-of-cwd targets prompt every time.
- `permissions.defaultMode: acceptEdits` — auto-approve in-cwd Write / Edit /
  filesystem Bash.
- `Bash(rm *)` → `permissions.ask` (only entry in `permissions.ask`).
- Auto-memory disabled (`autoMemoryEnabled: false`) with explicit "do not
  propose memory entries" instruction in CLAUDE.md.

### Identity / scope

- **Role assignment:**

  > 🔲 To be defined — awaiting user input

- **Repo purpose:**

  > 🔲 To be defined — Claude to infer from directory content

## Routing decision

For each fact in the framing, route to exactly one destination. If a fact
matches more than one row, take the topmost row. Process facts top-down.

| Fact pattern | Destination | Why |
| :--- | :--- | :--- |
| Must NEVER run (command, path, tool, MCP action) | `.claude/settings.json` → `permissions.deny` | Hard enforcement, not behavioral guidance |
| Must prompt the user before running | `.claude/settings.json` → `permissions.ask` | Friction by design — destructive but sometimes wanted |
| Pre-approved tool/command (skip prompt) | `.claude/settings.json` → `permissions.allow` | Reduces friction, preserves audit |
| Session default for unmatched permission requests | `.claude/settings.json` → `permissions.defaultMode` | Sets prompt behaviour when no allow/deny/ask rule matches |
| Lifecycle event handler (script / HTTP / MCP / prompt / agent at a tool or session event) | `.claude/settings.json` → `hooks.<EventName>[]`; scripts conventionally live in `.claude/hooks/` | Deterministic enforcement that runs regardless of Claude's decisions |
| Environment variable, sandbox toggle, login lock | `.claude/settings.json` → `env` / `sandbox` / `forceLoginMethod` / `forceLoginOrgUUID` | Client-enforced runtime config |
| Integration with a 3rd-party service | `.mcp.json` → `mcpServers.<name>` (one entry per server) | MCP declarations |
| Multi-step on-demand procedure (covers `/slash-commands`) | `.claude/skills/{slug}/SKILL.md` | Loads only when triggered; keeps base context lean |
| Rule that applies only under specific paths | `.claude/rules/{topic}.md` with `paths:` frontmatter | Loaded when Claude reads matching files |
| Topic-cohesive ruleset, always-on | `.claude/rules/{topic}.md` (no frontmatter) | Modular organization; same priority as `.claude/CLAUDE.md` |
| Global, always-on project rule or fact | `./CLAUDE.md` (or `.claude/CLAUDE.md`) | Loaded every session |
| Personal / non-portable / sandbox URL | `./CLAUDE.local.md` (gitignored) | Local only, not shared |
| Reusable content (README, AGENTS.md) | Import via `@path` from CLAUDE.md | DRY without duplication |
| Human-only note, rationale, audit trail | HTML block comment in a CLAUDE.md / CLAUDE.local.md | Stripped from CLAUDE.md before context injection — zero tokens |

> Note on `.claude/commands/`: legacy custom-command files in `.claude/commands/`
> still load and produce the same `/name` slash command as a skill at
> `.claude/skills/name/SKILL.md`. Skills take precedence on name collision.
> Prefer skills for new work — they support supporting files, frontmatter, and
> `disable-model-invocation`.

> Rules vs. skills: a rule is always-on (or path-triggered) context; a skill is
> an on-demand procedure invoked by Claude or by `/skill-name`. If the content
> constrains behavior whenever certain files are touched, use a rule. If it's
> a multi-step procedure that only sometimes applies, use a skill.

## Per-bucket authoring rules

### `./CLAUDE.md`

- Target **≤ 200 lines**. If you exceed, split into `.claude/rules/` files,
  skills, or imports before writing.
- Markdown headers + bullets. No dense paragraphs.
- Wrap groups of related rules in descriptive XML tags
  (`<safety_rules>`, `<naming_conventions>`, `<deploy_workflow>`, etc.).
  Per Anthropic's prompt-engineering guidance: "XML tags help Claude parse
  complex prompts unambiguously, especially when your prompt mixes
  instructions, context, examples, and variable inputs." Use consistent,
  descriptive tag names; nest where content has a natural hierarchy. Tags
  are read by Claude as structural anchors (the opposite of HTML comments,
  which are stripped). Source:
  `docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags`.
- Every instruction must be specific and verifiable: write `Run npm test before
  committing`, not `Test your changes`.
- Contradictions across CLAUDE.md, ancestor CLAUDE.md, `.claude/rules/`, and
  imports are resolved arbitrarily at runtime — fix them before write, do not
  let them ship.
- Open the file with an HTML comment recording: framing source, generation date,
  guidelines version. Costs zero tokens.
- After writing, run `/memory` to confirm every CLAUDE.md / CLAUDE.local.md /
  rules file you authored is discovered and loaded.

### `./CLAUDE.local.md`

- Same syntax as CLAUDE.md. Loaded last in the project's directory tree
  (appended after project CLAUDE.md). On contradiction, Claude may pick either
  arbitrarily — order biases but does not enforce override.
- Add to `.gitignore` in the same operation that writes the file.
- Never store secret values. Reference environment variable names if path
  context is needed.
- Across worktrees: a gitignored `CLAUDE.local.md` only exists in the worktree
  where you created it. To share personal instructions across worktrees,
  import from `~/.claude/` instead: `@~/.claude/my-project-overrides.md`.

### `./.claude/rules/{topic}.md`

> Verify against
> `code.claude.com/docs/en/memory#organize-rules-with-claude/rules/`.

- One topic per file. Descriptive name: `testing.md`, `security.md`,
  `api-design.md`. Subdirectories allowed (`frontend/`, `backend/`).
- Without frontmatter: loads at launch with the same priority as
  `.claude/CLAUDE.md`.
- With `paths:` frontmatter: loads only when Claude reads files matching the
  glob. This is the primary mechanism to keep startup context small.
- `paths:` accepts a YAML list or comma-separated string. Brace expansion
  works:

  ```markdown
  ---
  paths:
    - "src/api/**/*.ts"
    - "lib/**/*.{ts,tsx}"
  ---
  ```

- User-level rules live in `~/.claude/rules/` and apply to every project;
  project rules take precedence.
- Symlinks are supported — useful for sharing a rule set across repos
  (`ln -s ~/shared/security.md .claude/rules/security.md`).

### `./.claude/skills/{slug}/SKILL.md`

> Verify field names and limits against `code.claude.com/docs/en/skills`
> before finalizing frontmatter.

- Extract a procedure to a skill when it is (a) multi-step, (b) not needed in
  every session, (c) reusable across triggers. A skill at
  `.claude/skills/foo/SKILL.md` is invocable as `/foo`.
- Target ≤ 500 lines per SKILL.md; move reference material to supporting
  files in the skill directory.
- Skills can be composed: a subagent's `skills:` frontmatter field preloads
  multiple skills into its context. Use this when one workflow needs several
  skills loaded together.
- Frontmatter fields routing-relevant to configuration decisions:

  | Field | Use |
  | :--- | :--- |
  | `description` | Routing signal. Front-load distinctive trigger keywords. |
  | `when_to_use` | Appended to `description` for routing — same character budget. |
  | `disable-model-invocation: true` | Only the user can invoke. Use for destructive workflows (`/deploy`, `/commit`). This is the enforcement layer for "ask before doing X" semantics that prose alone cannot guarantee. |
  | `user-invocable: false` | Only Claude can invoke. Use for background-knowledge skills not meaningful as commands. |
  | `allowed-tools` | Tools Claude can use without prompting while the skill is active. Takes effect only after workspace trust is accepted. |
  | `paths` | Glob patterns (comma-separated string or YAML list) limiting auto-activation to matching files. |
  | `context: fork` (+ `agent`) | Run the skill body in an isolated subagent context (e.g. `Explore`, `Plan`, custom). |

- Combined `description` + `when_to_use` is truncated at **1,536 characters**
  in the skill listing (configurable via `maxSkillDescriptionChars`). The
  listing budget itself scales at 1% of the model's context window
  (configurable via `skillListingBudgetFraction`); on overflow, least-used
  skills lose their descriptions first.
- A skill that performs a destructive action must set
  `disable-model-invocation: true`. Prose warnings are not enforcement.

### `./.claude/settings.json`

> Verify key paths against `code.claude.com/docs/en/settings`.

- `permissions.deny`: blocking list (commands, file paths, tools, MCP actions).
- `permissions.ask`: prompt-before-running list. Evaluated between `deny` and
  `allow`; first match wins.
- `permissions.allow`: pre-approved list (no user prompt).
- `permissions.defaultMode`: behaviour when no allow/ask/deny rule matches.
  Values: `default` (prompt), `acceptEdits` (auto-approve edits, prompt
  otherwise), `plan` (require plan acceptance), `auto` (classifier-based
  approval — **ignored** in project/local settings as of v2.1.142, set only in
  `~/.claude/settings.json`), `dontAsk` (silent allow), `bypassPermissions`
  (skip all checks). Explicit `deny` always wins regardless of mode.
- `sandbox.enabled`: enforce filesystem isolation when the framing names
  destructive risk.
- `forceLoginMethod` / `forceLoginOrgUUID`: lock the session to a specific
  authentication method (e.g. Claude.ai vs. Anthropic API key) and/or
  organization UUID. `forceLoginOrgUUID` accepts a string or string array.
- `env`: project-scoped environment variables. Never commit secrets — reference
  external secret managers.
- `autoMemoryEnabled: false` if the framing requires deterministic context.
- `claudeMdExcludes`: glob list of ancestor CLAUDE.md files to skip. Essential
  in monorepos where other teams' instructions get picked up. Applies to
  user/project/local memory only — managed-policy files cannot be excluded.

Use `.claude/settings.local.json` (gitignored) for per-developer overrides.
Managed-policy settings (org-deployed via `managed-settings.json`) cannot be
overridden — note this in the framing review if any conflict arises.

### Hooks (in `./.claude/settings.json`)

> Verify against `code.claude.com/docs/en/hooks`.

- Hooks declare lifecycle event handlers under a top-level `hooks` key in
  settings.json. Shape:

  ```json
  {
    "hooks": {
      "<EventName>": [
        {
          "matcher": "<tool name | regex | source>",
          "hooks": [
            { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/x.sh", "if": "Bash(rm *)" }
          ]
        }
      ]
    }
  }
  ```

- Common events relevant to project framings: `SessionStart`, `Setup`,
  `UserPromptSubmit`, `UserPromptExpansion` (matches slash-command / skill
  invocation), `PreToolUse`, `PostToolUse`, `PermissionRequest`, `Stop`,
  `SubagentStart`, `SubagentStop`, `InstructionsLoaded`. The full list (~30
  events) is in the hooks doc.
- `matcher` semantics depend on the event: tool name for `Pre/PostToolUse`,
  command name for `UserPromptExpansion`, source for `SessionStart`
  (`startup` / `resume` / `clear` / `compact`), etc. Pure alphanumerics + `|`
  are exact / pipe-list match; anything else is a JS regex.
- `if` field on a handler narrows by permission-rule syntax
  (`"Bash(rm *)"`, `"Edit(*.ts)"`). Only evaluated on tool events.
- Handler `type` values: `command` (shell script), `http` (POST to URL),
  `mcp_tool` (invoke a configured MCP server tool), `prompt` (small-model
  evaluation), `agent` (subagent with tool access).
- Conventional layout: scripts in `.claude/hooks/{name}.sh`, referenced from
  settings.json via `$CLAUDE_PROJECT_DIR/.claude/hooks/{name}.sh`. The
  directory is not auto-loaded — only what settings.json references runs.
- Security: command hooks execute in the user's shell with full credentials
  and filesystem access. There is no sandboxing. Treat any project hook as
  trusted code from your repo's contributors. Enterprises can lock down with
  `allowManagedHooksOnly: true` in managed settings.
- Use a hook (not a CLAUDE.md instruction) when the framing says "always run X
  before tool Y" or "block any rm of paths outside cwd" — CLAUDE.md is
  context, hooks are enforcement.

### `./.mcp.json`

> Verify schema against `code.claude.com/docs/en/mcp`.

- Top-level shape: `{ "mcpServers": { "<name>": { ... } } }`. Each server
  entry requires a `type` field (`http`, `stdio`, or `streamable-http`; `sse`
  is **deprecated** — use `http` where available) plus transport-specific
  fields: `url` (+ optional `headers`) for remote transports; `command`
  (+ `args`, `env`) for `stdio`.
- Environment-variable expansion is supported in `command`, `args`, `env`,
  `url`, and `headers`: `${VAR}` or `${VAR:-default}`. A required variable
  with no default fails config parse.
- Do not declare an MCP server unless the framing names a workflow that
  requires it. Speculative declarations bloat startup and widen attack surface.
- `.mcp.json` is strict JSON — no comments permitted. Record the justifying
  workflow for each server either as an HTML comment in the project CLAUDE.md
  near where the server is referenced, or in a sibling
  `.claude/mcp-workflows.md` audit file. Required for later pruning.

### Imports (`@` syntax)

- Use to: interop with `AGENTS.md` (`@AGENTS.md`), share content across
  worktrees (`@~/.claude/foo.md`), reuse READMEs (`@README`).
- Relative paths resolve to the importing file's location, not the working
  directory.
- Max 5 hops.
- Imported files are expanded into context at launch — they cost tokens. They
  are NOT lazy-loaded.

## Output protocol

When you apply these guidelines to a framing:

1. **`./CLAUDE.md`** — draft, then write directly to disk. One confirm prompt
   after the full file is drafted: `Confirm write to ./CLAUDE.md?`.
2. **All other artifacts** (`./.claude/rules/*.md`,
   `./.claude/skills/*/SKILL.md`, `./.claude/settings.json`, `./.mcp.json`,
   `./CLAUDE.local.md`) — produce each as a separate fenced code block in chat,
   labelled with its target path. Write to disk only on explicit per-file
   approval.
3. **`.gitignore`** — propose the diff covering `CLAUDE.local.md` and
   `.claude/settings.local.json`. Do not write without confirmation.

## Verification checklist

Before declaring the project configured:

- `CLAUDE.md` line count ≤ 200.
- No fact appears in more than one bucket.
- Every `paths:` frontmatter (in `.claude/rules/` or `.claude/skills/`) uses
  valid glob syntax.
- Every skill referenced from CLAUDE.md exists at the declared path.
- `permissions.deny` covers every "must never run" item from the framing.
- `permissions.ask` covers every "prompt before running" item.
- `permissions.defaultMode` is set if the framing dictates a non-`default`
  behaviour; `auto` lives in user settings, never project/local.
- Every hook command path exists and is executable; matcher syntax is valid
  for its event type.
- Every destructive skill has `disable-model-invocation: true`.
- `.gitignore` excludes `CLAUDE.local.md` and `*.local.json` settings.
- CLAUDE.md opens with an HTML comment recording framing source, date,
  guidelines version.
- No CLAUDE.md contradicts an ancestor CLAUDE.md; if an override is intended,
  document it in a comment.
- `/memory` in a fresh session lists every CLAUDE.md, CLAUDE.local.md, and
  rules file you authored.

## Refusal triggers

Stop and surface the issue rather than produce a degraded config when:

- The framing demands behavioral enforcement of a destructive action. CLAUDE.md
  is context, not policy. Route to `permissions.deny` + sandbox + (for skills)
  `disable-model-invocation: true` + (for lifecycle enforcement) a `PreToolUse`
  hook, or refuse.
- The framing requests `defaultMode: bypassPermissions` or `dontAsk` without a
  sandbox guarantee. Demand justification or refuse.
- The framing names an MCP integration with no documented workflow. Demand the
  workflow before declaring the server.
- The framing asks for secrets in CLAUDE.md or `.mcp.json`. Refuse; route to
  environment variables or a secret manager.

| Field        | Value       |
|--------------|-------------|
| Version      | 1.9         |
| Last Updated | 2026-05-25  |
| Status       | Draft       |
